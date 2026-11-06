#!/usr/bin/env python3
"""Validate cross-workflow contracts that generic YAML/Action linters cannot prove."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"


def read(name: str) -> str:
    return (WORKFLOW_DIR / name).read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"::error::{message}")
    raise SystemExit(1)


def schedule_max_minute_gap(workflow_text: str, workflow_name: str) -> int:
    schedule = re.search(
        r"(?ms)^  schedule:[ \t]*\n(?P<body>.*?)(?=^  [A-Za-z_][A-Za-z0-9_-]*:[ \t]*$|\Z)",
        workflow_text,
    )
    if schedule is None:
        fail(f"{workflow_name} must declare an explicit schedule for freshness validation.")
    cron = re.search(r'(?m)^[ \t]*-[ \t]*cron:[ \t]*"([^"]+)"', schedule.group("body"))
    if cron is None:
        fail(f"{workflow_name} must declare a quoted cron expression.")
    fields = cron.group(1).split()
    if len(fields) != 5:
        fail(f"{workflow_name} cron must contain five fields.")
    minute_field = fields[0]
    if re.fullmatch(r"\*/[1-9][0-9]*", minute_field):
        return int(minute_field[2:])
    if not re.fullmatch(r"[0-9]+(?:,[0-9]+)*", minute_field):
        fail(
            f"{workflow_name} minute cron field must use a numeric list or */N step; "
            "extend the freshness contract parser before changing its schedule."
        )
    minutes = sorted({int(value) for value in minute_field.split(",")})
    if not minutes or any(value < 0 or value > 59 for value in minutes):
        fail(f"{workflow_name} cron minute values must be between 0 and 59.")
    gaps = [right - left for left, right in zip(minutes, minutes[1:])]
    gaps.append(minutes[0] + 60 - minutes[-1])
    return max(gaps)

reconcile = read("reconcile-vps.yml")
promotion = read("gitops-image-promotion.yml")
recovery = read("recover-stale-ops.yml")
watchdog = read("reconcile-schedule-watchdog.yml")
inspection = read("inspect-vps.yml")
lane_queue = (ROOT / "scripts" / "verify-reconcile-lane-queue.py").read_text(encoding="utf-8")
provision = read("provision-keycloak-tce-client.yml")
cleanup = read("vps-image-cleanup.yml")

# Read-only validation of the optional VPS MCP must not trigger a production recovery/apply cycle.
if '"!scripts/validate-vps-control-mcp-contract.py"' not in recovery:
    fail("Read-only VPS MCP contract validation must be excluded from recovery push triggers.")

# The private locally-uncensored mirror is intentionally detached by owner request.
# Keep it out of the active workflow set until the owner explicitly asks to restore it.
if (WORKFLOW_DIR / "mirror-locally-uncensored.yml").exists():
    fail("locally-uncensored mirror must remain detached until explicit owner authorization.")
for active_workflow in (recovery, watchdog):
    if "mirror-locally-uncensored" in active_workflow or "Mirror locally-uncensored into private repository" in active_workflow:
        fail("Recovery/watchdog must not subscribe to the detached locally-uncensored mirror.")


# Manual reconciliation must be non-mutating unless an operator explicitly
# selects apply. Scheduled, push and authenticated promotion events keep their
# existing automatic apply behavior; this contract does not change cron cadence.
manual_dispatch = reconcile.split("  workflow_dispatch:", 1)[1].split("  repository_dispatch:", 1)[0]
expected_manual_mode = """      mode:
        description: "Reconciliation mode (manual dispatch defaults to read-only plan; choose apply explicitly)"
        required: true
        default: plan
        type: choice
"""
if expected_manual_mode not in manual_dispatch:
    fail("Manual reconcile-vps dispatch must default to read-only plan; apply must be an explicit operator choice.")
if "github.event_name == 'schedule' || github.event_name == 'push' || github.event_name == 'repository_dispatch') && 'apply'" not in reconcile:
    fail("Scheduled, push and authenticated GitOps reconciliation must retain their existing automatic apply mode.")

# The promotion workflow defaults to read-only. Grant write scopes only to the
# jobs that create/merge GitOps PRs or emit the final repository_dispatch.
top_level_permissions = promotion.split("permissions:\n", 1)[1].split("\nconcurrency:", 1)[0].strip()
if top_level_permissions != "contents: read":
    fail("GitOps promotion must default GITHUB_TOKEN to contents:read only.")


def promotion_job_block(job_name: str) -> str:
    marker = f"  {job_name}:\n"
    if marker not in promotion:
        fail(f"GitOps promotion is missing job {job_name}.")
    tail = promotion.split(marker, 1)[1]
    next_job = re.search(r"(?m)^  [A-Za-z0-9_-]+:\s*$", tail)
    return tail[:next_job.start()] if next_job else tail


guard_job = promotion_job_block("reject-non-master-manual-run")
if not re.search(r"(?m)^    permissions: \{\}\s*$", guard_job):
    fail("The non-master manual rejection job must have no GITHUB_TOKEN permissions.")

coordinator_job = promotion_job_block("coordinate-tce-release")
coordinator_permissions = re.search(
    r"(?ms)^    permissions:\n(?P<body>(?:^      [a-z-]+: [a-z]+\n)+)",
    coordinator_job,
)
if coordinator_permissions is None or coordinator_permissions.group("body").strip() != "contents: write":
    fail("The TCE release coordinator may write repository dispatches but must not receive Actions or pull-request write scopes.")

for job_name in ("promote-microfe-digests", "promote-tce-digests", "promote"):
    job = promotion_job_block(job_name)
    permissions = re.search(
        r"(?ms)^    permissions:\n(?P<body>(?:^      [a-z-]+: [a-z]+\n)+)",
        job,
    )
    expected = {"actions": "write", "contents": "write", "pull-requests": "write"}
    actual = {}
    if permissions is not None:
        for line in permissions.group("body").splitlines():
            key, value = line.strip().split(":", 1)
            actual[key] = value.strip()
    if actual != expected:
        fail(f"GitOps PR promotion job {job_name} must explicitly retain only its required Actions/Contents/Pull requests write scopes.")

# Automated inspection and GitOps promotion PRs must use the verified Node24 action release.
create_pull_request_pin = "peter-evans/create-pull-request@5f6978faf089d4d20b00c7766989d076bb2fc7f1  # v8.1.1"
legacy_create_pull_request_pin = "peter-evans/create-pull-request@22a9089034f40e5a961c8808d113e2c98fb63676"
if inspection.count(create_pull_request_pin) != 1:
    fail("VPS inspection PR creation must use peter-evans/create-pull-request v8.1.1 pinned to its immutable Node24 commit.")
if promotion.count(create_pull_request_pin) != 3:
    fail("All three GitOps promotion PR creation paths must use peter-evans/create-pull-request v8.1.1 pinned to its immutable Node24 commit.")
if legacy_create_pull_request_pin in inspection or legacy_create_pull_request_pin in promotion:
    fail("A legacy Node20 peter-evans/create-pull-request pin remains in a production workflow.")

# Inspection snapshots use an attempt-specific branch to avoid force-pushing a stale
# automation branch; recovery retries only transient GitHub workflow-dispatch 5xx errors.
if "branch: automation/vps-inspection-${{ github.run_id }}-${{ github.run_attempt }}" not in inspection:
    fail("VPS inspection PRs must use a run/attempt-specific branch.")
if 'EXPECTED_BRANCH="automation/vps-inspection-${RUN_ID}-${RUN_ATTEMPT}"' not in inspection:
    fail("VPS inspection PR validation must enforce the exact run/attempt-specific branch.")

# Inspection merge must tolerate bounded GitHub API 5xx/network failures without
# ever relaxing the exact validated PR-head check or merging a changed branch.
for required in (
    "max_merge_attempts=3",
    "merge_confirmed=false",
    "for ((attempt = 1; attempt <= max_merge_attempts; attempt++)); do",
    'current_head" == "$PR_HEAD_SHA"',
    'merge_http_status" =~ ^(000|500|502|503|504)$',
    "retry_delay=$((attempt * 5))",
    '[[ "$merge_confirmed" == "true" ]]'
):
    if required not in inspection:
        fail(f"VPS inspection transient-merge retry contract is missing: {required}")

# Every inspection API GET must retry transient 5xx/network failures while
# leaving authentication, not-found, and other 4xx responses as hard failures.
for required in (
    "github_api_get()",
    "local max_get_attempts=3",
    'status" =~ ^(000|500|502|503|504)$',
    'encoded_branch="$(printf \'%s\' "$PR_BRANCH" | jq -sRr @uri)"',
    'runs_json="$(github_api_get "$runs_url" "$RUNNER_TEMP/inspection-validation-runs.json")"',
    'github_api_get "https://api.github.com/repos/$REPOSITORY/pulls/$PR_NUMBER"',
):
    if required not in inspection:
        fail(f"VPS inspection transient-GET retry contract is missing: {required}")
if "HTTP (500|502|503|504)" not in recovery:
    fail("Read-only inspection recovery must retry transient GitHub HTTP 5xx dispatch failures.")

if not re.search(r"(?m)^  workflow_dispatch:", provision):
    fail("Keycloak provisioning must retain its explicit manual workflow_dispatch entry point.")
if re.search(r"(?m)^  push:", provision):
    fail("Privileged Keycloak realm/client provisioning must not run automatically on push; use the manual production workflow.")
cleanup_push_paths = cleanup.split("  push:", 1)[1].split("  workflow_dispatch:", 1)[0]
if '".github/workflows/vps-image-cleanup.yml"' in cleanup_push_paths:
    fail("Editing the image-cleanup workflow itself must not start a cleanup job; script/test pushes remain dry-run only.")
expected_recovery_sources = """    workflows:
      - "reconcile-vps"
      - "inspect-vps"
      - "Reconcile Schedule Freshness Watchdog"
"""
if expected_recovery_sources not in recovery or "types: [completed]" not in recovery:
    fail("Recovery controller must run after master reconciliation, scheduled inspection, and schedule-watchdog completion.")

watchdog_recovery_gate = """             (github.event.workflow_run.workflow_id == 402675709 &&
              github.event.workflow_run.event == 'schedule' &&
              github.event.workflow_run.conclusion == 'failure')"""
if watchdog_recovery_gate not in recovery:
    fail("A failed native scheduled freshness watchdog must trigger the existing recovery controller; successful/diagnostic watchdog runs must not.")
if "github.event.workflow_run.run_attempt == 1" not in recovery:
    fail("Recovery must ignore workflow_run rerun attempts; only the original completed run may drive freshness recovery.")
if "github.run_attempt == 1" not in recovery:
    fail("The recovery controller itself must ignore rerun attempts to prevent replay.")
global_latest_runs_query = 'runs="$(gh api -X GET "repos/${GITHUB_REPOSITORY}/actions/runs" -F branch=master -F per_page=100)"'
if recovery.count(global_latest_runs_query) < 1:
    fail("Recovery must query the master Actions run page for reconciliation activity.")
for required in (
    '--arg workflow_path ".github/workflows/reconcile-vps.yml"',
    '.path == $workflow_path',
    '.head_branch == "master"',
    'sort_by(.created_at) | last // empty',
):
    if required not in recovery:
        fail(f"Recovery reconciliation latest-run selection is missing: {required}")
for obsolete in (
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/reconcile-vps.yml/runs" -F branch=master -F per_page=100',
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/inspect-vps.yml/runs" -F branch=master -F per_page=100',
):
    if obsolete in recovery:
        fail(f"Recovery freshness must not use stale workflow-specific pagination: {obsolete}")

if "repository_dispatch:" not in recovery or "types: [tce-schedule-heartbeat]" not in recovery:
    fail("Recovery controller must accept the authenticated cross-repository TCE schedule heartbeat.")

# Keep the freshness watchdog aligned with the native recovery cadence. The
# budget is exactly three maximum schedule intervals: two missed ticks can be
# observed, while a third missed tick fails closed instead of hiding stale ops.
recovery_schedule_gap = schedule_max_minute_gap(recovery, "recover-stale-ops")
watchdog_schedule_gap = schedule_max_minute_gap(watchdog, "reconcile-schedule-watchdog")
if watchdog_schedule_gap > recovery_schedule_gap:
    fail("The schedule freshness watchdog must run at least as frequently as the recovery controller.")
recovery_age_budget = re.search(
    r'(?m)^[ \t]*MAX_RECOVERY_AGE_MINUTES:[ \t]*"([0-9]+)"',
    watchdog,
)
if recovery_age_budget is None:
    fail("The schedule watchdog must declare MAX_RECOVERY_AGE_MINUTES.")
if int(recovery_age_budget.group(1)) != recovery_schedule_gap * 3:
    fail(
        "MAX_RECOVERY_AGE_MINUTES must equal three maximum recovery schedule intervals "
        "so missed native schedule delivery remains observable."
    )

# The watchdog must measure recovery freshness from native schedule runs only.
# workflow_run / workflow_dispatch successes are useful fallback evidence but cannot
# satisfy the independent cron-delivery contract.
native_recovery_endpoint = '"repos/${GITHUB_REPOSITORY}/actions/workflows/recover-stale-ops.yml/runs"'
if watchdog.count(native_recovery_endpoint) != 1:
    fail("The schedule watchdog must query the recovery workflow's run history exactly once.")
native_recovery_query = watchdog.split(native_recovery_endpoint, 1)[1].split(")", 1)[0]
for required in ("-f event=schedule", "-f branch=master", "-F per_page=1"):
    if required not in native_recovery_query:
        fail(f"The schedule watchdog native recovery query is missing: {required}")
if "-f event=workflow_run" in native_recovery_query or "-f event=workflow_dispatch" in native_recovery_query:
    fail("The schedule watchdog must not count fallback events as native recovery schedule evidence.")

for required in (
    "github.event.action == 'tce-schedule-heartbeat'",
    "github.event.client_payload.source_repository == 'phanthienquoc/TCE-dashboard'",
    "github.event.client_payload.source_event == 'schedule'",
    "github.event.client_payload.source_run_attempt == '1'",
    "github.event.client_payload.heartbeat_run_attempt == '1'",
    "github.event.client_payload.source_workflow_path == '.github/workflows/wf-06-tce-healthcheck.yml'",
    "github.event.client_payload.source_workflow_path == '.github/workflows/wf-07-tce-integration-check.yml'",
    "github.event.client_payload.source_workflow_path == '.github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml'",
    "- name: Validate external TCE schedule heartbeat payload",
    "SOURCE_RUN_ID: ${{ github.event.client_payload.source_run_id }}",
    "SOURCE_RUN_ATTEMPT: ${{ github.event.client_payload.source_run_attempt }}",
    "SOURCE_HEAD_SHA: ${{ github.event.client_payload.source_head_sha }}",
    "HEARTBEAT_RUN_ID: ${{ github.event.client_payload.heartbeat_run_id }}",
    "HEARTBEAT_RUN_ATTEMPT: ${{ github.event.client_payload.heartbeat_run_attempt }}",
    "HEARTBEAT_HEAD_SHA: ${{ github.event.client_payload.heartbeat_head_sha }}",
    "phanthienquoc/TCE-dashboard",
    "TCE heartbeat SHAs must be full commit IDs",
    "fetch_tce_run()",
    "api.github.com/repos/$SOURCE_REPOSITORY/actions/runs/$1",
    "source_run_path",
    "source_run_event",
    "source_run_branch",
    "source_run_sha",
    "source_run_attempt",
    '[[ "$source_run_event" == "schedule"',
    '"$source_run_branch" == "master"',
    '"$source_run_sha" == "$SOURCE_HEAD_SHA"',
    'if [[ "$SOURCE_RUN_ATTEMPT" != "1" || "$HEARTBEAT_RUN_ATTEMPT" != "1" ]]; then',
    '[[ "$source_run_attempt" == "1" && "$source_run_attempt" == "$SOURCE_RUN_ATTEMPT" ]]',
    "Direct WF-12 schedule heartbeat must identify the same source and heartbeat run.",
    "WF-06/WF-07 heartbeat source must be completed before forwarding.",
    "heartbeat_run_path",
    "heartbeat_run_attempt",
    '[[ "$heartbeat_run_path" == ".github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml" ]]',
    '[[ "$heartbeat_run_attempt" == "1" && "$heartbeat_run_attempt" == "$HEARTBEAT_RUN_ATTEMPT" ]]',
    '[[ "$heartbeat_run_event" == "workflow_run" ]]',
    '[[ "$heartbeat_run_event" == "schedule" ]]',
    '"$heartbeat_run_sha" == "$HEARTBEAT_HEAD_SHA"',
):
    if required not in recovery:
        fail(f"External TCE schedule heartbeat contract is missing: {required}")
if not re.search(r"(?m)^  push:\n    branches: \[master\]\n    paths:", recovery):
    fail("Recovery controller must bootstrap from deployment-relevant master pushes.")
for required_path in (
    'apps/**',
    'platform/**',
    'environments/prod/**',
    'scripts/**',
):
    if required_path not in recovery:
        fail(f"Recovery push bootstrap is missing deployment path filter: {required_path}")

recovery_push_paths = recovery.split("  push:", 1)[1].split("  workflow_dispatch:", 1)[0]
if '"!apps/**/*.md"' not in recovery_push_paths:
    fail("Recovery push must exclude Markdown-only app documentation from production bootstrap.")
if "'!apps/tce-vps-control-mcp/**'" not in recovery_push_paths:
    fail("Recovery push must exclude the diagnostics-only VPS MCP from production bootstrap.")
if '".github/workflows/reconcile-vps.yml"' in recovery_push_paths:
    fail("Changes to the production apply workflow must be validated but must not auto-dispatch production reconciliation.")
if '".github/workflows/recover-stale-ops.yml"' in recovery_push_paths:
    fail("Editing the recovery controller itself must not trigger a production reconciliation.")
if '".github/workflows/inspect-vps.yml"' in recovery_push_paths:
    fail("Read-only inspect-vps workflow edits must not trigger production reconciliation.")
for excluded_path in (
    "scripts/inspect-vps.sh",
    "scripts/verify-reconcile-lane-queue.py",
    "scripts/validate-workflow-contracts.py",
    "scripts/validate-network-boundaries.sh",
    "scripts/validate-auth-gitops-contract.py",
    "scripts/resolve-push-deployment-scope.sh",
):
    if f'"!{excluded_path}"' not in recovery_push_paths:
        fail(f"Recovery push must exclude read-only CI/watchdog helper: {excluded_path}")

for required in (
    "source_run_id:",
    "source_head_sha:",
    "SOURCE_RUN_ID: ${{ inputs.source_run_id }}",
    "SOURCE_HEAD_SHA: ${{ inputs.source_head_sha }}",
    '.path // empty',
    "source_status",
    'source_status" == "completed"',
):
    if required not in recovery:
        fail(f"Recovery controller is missing completed-source-run verification: {required}")

if "  notify-recovery-controller:" not in reconcile:
    fail("Reconciliation must notify the recovery controller after its deployment lanes finish.")
recovery_notify = reconcile.split("  notify-recovery-controller:", 1)[1]
for required in (
    "needs:",
    "- deployment-lane-summary",
    "needs.reconcile.outputs.mode == 'apply'",
    "actions: write",
    "gh workflow run recover-stale-ops.yml",
    "SOURCE_RUN_ID: ${{ github.run_id }}",
    "SOURCE_HEAD_SHA: ${{ github.sha }}",
    '--arg source_run "$SOURCE_RUN_ID"',
    '.display_title == ("Recover Stale Scheduled Ops — workflow_dispatch / source " + $source_run)',
    "expected_display_title=",
    '.path == ".github/workflows/recover-stale-ops.yml"',
):
    if required not in recovery_notify:
        fail(f"Post-reconciliation recovery dispatch is missing: {required}")
run_name = " ".join(recovery.split("run-name:", 1)[1].split("'on':", 1)[0].split())
if not all(
    source in run_name
    for source in (
        "inputs.source_run_id",
        "github.event.client_payload.source_run_id",
        "github.event.workflow_run.id",
        "'none'",
        " / source ",
    )
):
    fail("Recovery workflow run-name must expose the exact source run id for workflow_dispatch, repository_dispatch, and workflow_run correlation.")
if 'and .head_sha == $sha' in recovery_notify:
    fail("Post-reconciliation recovery correlation must not compare the recovery workflow SHA to the source reconciliation SHA; master may advance between dispatch and run creation.")

if "github.event.workflow_run.head_branch == 'master'" not in recovery:
    fail("Recovery controller must ignore non-master workflow completion events.")
if "run-name: Reconcile VPS —" not in reconcile:
    fail("Reconciliation must retain its descriptive dynamic run-name contract.")

# App documentation may live beside production overlays, but must never trigger a
# production reconciliation or be misclassified as a workload change.
reconcile_push_paths = reconcile.split("  push:", 1)[1].split("\\n\\npermissions:", 1)[0]
if "- apps/**" not in reconcile_push_paths or "- '!apps/**/*.md'" not in reconcile_push_paths:
    fail("Production reconciliation push paths must exclude Markdown-only app documentation.")
if "'!apps/tce-vps-control-mcp/**'" not in reconcile_push_paths:
    fail("Production reconciliation push paths must exclude the diagnostics-only VPS MCP.")
scope_resolver = (ROOT / "scripts" / "resolve-push-deployment-scope.sh").read_text(encoding="utf-8")
for required in (
    "apps/**/*.md|apps/**/docs/*",
    "assert_failure apps/stockdividend/README.md",
    "assert_failure apps/stockdividend/docs/production-runtime.md",
    "apps/tce-vps-control-mcp/*",
    "assert_failure apps/tce-vps-control-mcp/package.json",
    "assert_scope tce-dashboard apps/tce-dashboard/overlays/prod/kustomization.yaml apps/tce-vps-control-mcp/package.json",
):
    if required not in scope_resolver:
        fail(f"Push scope resolver must ignore app documentation: {required}")
if "github.event.workflow_run.name == 'reconcile-vps'" in recovery:
    fail("Recovery must not compare workflow_run.name to the workflow name when reconcile-vps uses a dynamic run-name.")
if "github.event.workflow_run.workflow_id == 364209709" not in recovery:
    fail("Recovery must identify reconcile-vps completions by workflow_run.workflow_id.")
if "github.event.workflow_run.workflow_id == 364209707" not in recovery or "github.event.workflow_run.event == 'schedule'" not in recovery:
    fail("Only scheduled master inspection completions may trigger reconciliation recovery.")
if "github.event.workflow_run.workflow_id == 402675709" not in recovery:
    fail("Recovery must identify schedule-watchdog completions by workflow_run.workflow_id.")
if "github.event.workflow.path" in recovery:
    fail("Recovery workflow_run guards must not use the absent top-level github.event.workflow.path field.")
source_verification_index = recovery.find("- name: Verify and await source reconciliation completion")
reference_clock_index = recovery.find("- name: Resolve GitHub Actions API reference clock")
if source_verification_index < 0 or reference_clock_index < 0 or source_verification_index > reference_clock_index:
    fail("Recovery must verify/await its source reconciliation before resolving the freshness reference clock.")
for required in (
    "id: source",
    "SOURCE_COMPLETED_AT: ${{ steps.source.outputs.completed_at }}",
    "source_completed_at=",
    ".updated_at // .run_started_at // .created_at",
    "source_epoch > reference_epoch",
):
    if required not in recovery:
        fail(f"Recovery reference clock must include the completed source run timestamp: {required}")
guard_reconcile = (ROOT / "scripts" / "guard-reconcile-images.sh").read_text(encoding="utf-8")
github_actions = read("validate-github-actions.yml")
inspection_script = (ROOT / "scripts" / "inspect-vps.sh").read_text(encoding="utf-8")
manifest_validation = read("validate-manifests.yml")

# The image guard must detect YAML image fields regardless of indentation and test the parser offline.
if "grep -E '^-[[:space:]]+image:" not in guard_reconcile:
    fail("Image guard must detect removed container image fields at any YAML indentation.")
if "{10,}image:" in guard_reconcile:
    fail("Image guard must not use the old over-restrictive indentation threshold.")
if "bash scripts/guard-reconcile-images.sh --self-test" not in github_actions:
    fail("GitHub Actions validation must execute the image guard parser regression test.")

# VPS inspection must capture runtime container imageIDs, including init containers.
for required in ("### Pod imageID evidence", "containerStatuses", "initContainerStatuses", ".status.imageID"):
    if required not in inspection_script:
        fail(f"VPS inspection is missing runtime image identity evidence: {required}")

# The fresh VPS snapshot must expose the installed allowlisted runner policy.
for required in ('sudo "$KCTL" policy-version', "runner_policy:"):
    if required not in inspection_script:
        fail(f"VPS inspection is missing live runner policy evidence: {required}")

# Production MicroFE manifests must never accept the old placeholder tags.
for placeholder in (
    "ghcr.io/phanthienquoc/microfe-shell:0.1.0",
    "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA",
):
    if placeholder in manifest_validation:
        fail(f"Manifest validation must reject the retired MicroFE placeholder: {placeholder}")
for digest_reference in (
    "ghcr.io/phanthienquoc/microfe-shell@sha256:*",
    "ghcr.io/phanthienquoc/microfe-ws@sha256:*",
):
    if digest_reference not in manifest_validation:
        fail(f"Manifest validation must accept verified immutable MicroFE digests: {digest_reference}")

# Application GitOps promotions may use immutable digest references as well as legacy full-SHA release tags.
for required in (
    "(backend|admin)(:[0-9a-f]{7,64}|@sha256:[0-9a-f]{64})",
    "(backend|frontend)(:([0-9a-f]{7,64}|prod-v[0-9]+\\.[0-9]+\\.[0-9]+-[0-9a-f]{7,64})|@sha256:[0-9a-f]{64})",
):
    if required not in manifest_validation:
        fail(f"Manifest validation is missing immutable application digest support: {required}")

# The VPS inspection automation must validate the exact generated PR head before merge.
if "workflow_dispatch:" not in manifest_validation:
    fail("Manifest validation must expose workflow_dispatch for exact-head inspection validation.")
if 'pull_request:\n    paths-ignore:\n      - "debug/vps-latest.md"' not in manifest_validation:
    fail("Debug snapshot-only PRs must not create a jobless manifest-validation run.")
if "/actions/workflows/validate-manifests.yml/dispatches" not in inspection:
    fail("VPS inspection must explicitly dispatch manifest validation before merge.")
if 'event == "workflow_dispatch"' not in inspection or "Exact-head manifest validation passed" not in inspection:
    fail("VPS inspection must wait for a successful exact-head validation run.")
if "sha: $sha" not in inspection or "PR_HEAD_SHA" not in inspection:
    fail("VPS inspection must pin the squash merge to the validated PR head SHA.")
if 'payload=\'{"merge_method":"squash"}\'' in inspection:
    fail("VPS inspection must not use the legacy unguarded immediate merge payload.")
if "inspection-merge-response.json" not in inspection or "merge_http_status" not in inspection:
    fail("VPS inspection must capture the merge API status and response body for actionable diagnostics.")
for required in ("after_merge_head", "after_merge_merged", "merge_commit_sha", "leaving it open"):
    if required not in inspection:
        fail(f"VPS inspection merge handling is missing exact-head/idempotency guard: {required}")
if "Merged inspection PR head does not match the exact validated SHA" not in inspection:
    fail("VPS inspection must verify the merged PR head still matches the exact validated SHA.")

# A rerun may execute from an older workflow SHA. Rebase the generated snapshot
# onto the live master tip before creating the PR, so exact-head validation is
# never followed by a predictable stale-base merge conflict.
inspection_rebase_step = inspection.find("name: Rebase inspection snapshot on latest master")
inspection_create_step = inspection.find("name: Create inspection PR")
if inspection_rebase_step < 0 or inspection_create_step <= inspection_rebase_step:
    fail("VPS inspection must rebase its generated snapshot onto current master before creating the PR.")
inspection_rebase_block = inspection[inspection_rebase_step:inspection_create_step]
for required in (
    "if: steps.changes.outputs.changed == 'true'",
    "GH_TOKEN: ${{ github.token }}",
    'cp debug/vps-latest.md "$RUNNER_TEMP/vps-latest.md"',
    "x-access-token:%s",
    "base64 | tr -d",
    'http.https://github.com/.extraheader=AUTHORIZATION: basic $auth_header',
    "fetch --no-tags origin refs/heads/master:refs/remotes/origin/master",
    "git checkout --force -B master refs/remotes/origin/master",
    'install -m 0644 "$RUNNER_TEMP/vps-latest.md" debug/vps-latest.md',
    "Unexpected worktree changes while rebasing inspection snapshot onto latest master.",
):
    if required not in inspection_rebase_block:
        fail(f"VPS inspection latest-master rebase contract is missing: {required}")
if "gh auth setup-git" in inspection_rebase_block:
    fail("VPS inspection rebase must not depend on the GitHub CLI on its self-hosted runner.")


# Manual production promotion must originate from master; non-master dispatches fail visibly.
if "if: github.event_name == 'workflow_dispatch' && github.ref != 'refs/heads/master'" not in promotion:
    fail("Manual GitOps promotion must fail closed when dispatched from a non-master ref.")
if "github.event_name != 'workflow_dispatch' || github.ref == 'refs/heads/master'" not in promotion:
    fail("The application promotion job must only run manual promotions from master.")

# StockDividend's publisher emits the full 40-character source SHA; reject abbreviated tags.
stockdividend_tag_block = re.search(
    r"(?s)            stockdividend\)\n(.*?)\n              ;;",
    promotion,
)
if stockdividend_tag_block is None or '[[ "$TAG" =~ ^[0-9a-f]{40}$ ]]' not in stockdividend_tag_block.group(1):
    fail("StockDividend promotion must require a full 40-character source commit SHA.")
if "StockDividend tag must be a full 40-character source commit SHA" not in promotion:
    fail("StockDividend promotion must explain its full-SHA requirement.")
full_sha_pattern = re.compile(r"^[0-9a-f]{40}$")
if not full_sha_pattern.fullmatch("a" * 40):
    fail("StockDividend full-SHA validator rejected a valid source SHA.")
for invalid_tag in ("a" * 7, "a" * 39, "a" * 41, "g" * 40):
    if full_sha_pattern.fullmatch(invalid_tag):
        fail(f"StockDividend full-SHA validator accepted an invalid tag length/character: {invalid_tag}")

# Promotion PRs use the repository-scoped GITHUB_TOKEN. Because GITHUB_TOKEN-created
# PRs do not trigger pull_request workflows, explicitly dispatch manifest validation on
# the exact PR branch and require a successful run for the exact head before merging.
promotion_pr_validator = (ROOT / "scripts" / "validate-promotion-pr.sh").read_text(encoding="utf-8")
if promotion.count("actions: write") < 2:
    fail("Both promotion jobs must have Actions write permission to dispatch exact-head validation.")
if promotion.count("token: ${{ github.token }}") < 2:
    fail("Both promotion PR creation paths must use the repository-scoped GITHUB_TOKEN.")
if promotion.count("GH_TOKEN: ${{ github.token }}") < 4:
    fail("Both promotion paths must use GITHUB_TOKEN for validation and exact-head merge.")
if promotion.count("bash scripts/validate-promotion-pr.sh") < 2:
    fail("Both promotion paths must validate the exact PR head with the shared validator.")
if promotion.count("name: Validate exact promotion PR head") < 2:
    fail("Both promotion paths must run exact-head manifest validation before merge.")
if promotion.count("steps.validate-pr-checks.outputs.head_sha") < 2 or promotion.count('--match-head-commit "$HEAD_SHA"') < 2:
    fail("Both promotion merges must be pinned to the exact PR head that passed validation.")
if "PLATFORM_INFRA_AUTOMATION_TOKEN" in promotion or "gh pr checks" in promotion:
    fail("GitOps promotion must not depend on the removed automation PAT or suppressed PR-triggered checks.")
for required in (
    "actions/workflows/validate-manifests.yml/dispatches",
    '--data-urlencode "event=workflow_dispatch"',
    ".head_sha == $sha",
    ".head_branch == $branch",
    '.event == "workflow_dispatch"',
    "validation_conclusion",
    "head.sha",
    "head.ref",
):
    if required not in promotion_pr_validator:
        fail(f"Exact-head promotion validator is missing required guard: {required}")
if "GITHUB_TOKEN" not in (ROOT / "docs" / "credentials.md").read_text(encoding="utf-8"):
    fail("credentials.md must document the workflow-scoped GITHUB_TOKEN promotion model.")
credentials_key = (ROOT / "docs" / "credentials-key.md").read_text(encoding="utf-8")
if "`PLATFORM_INFRA_AUTOMATION_TOKEN`" in credentials_key:
    fail("credentials-key.md must not list the retired GitOps automation PAT.")

# StockDividend publishes a paired, digest-only promotion payload after all ARM64 images verify.
if "stockdividend-images-published" not in promotion:
    fail("GitOps promotion must consume the atomic StockDividend digest event.")

# Pin the receiver side of the cross-repository publisher payload contract. The
# StockDividend repository self-test validates the sender's jq payload shape.
stock_dispatch_types = promotion.split("  repository_dispatch:", 1)[1].split(
    "  workflow_dispatch:", 1
)[0]
if "- stockdividend-images-published" not in stock_dispatch_types:
    fail("GitOps promotion must subscribe to the exact StockDividend publisher event type.")
for required in (
    "EVENT_ACTION: ${{ github.event.action }}",
    "EVENT_APP: ${{ github.event.client_payload.app }}",
    "EVENT_COMMIT: ${{ github.event.client_payload.commit }}",
    "EVENT_BACKEND_DIGEST: ${{ github.event.client_payload.backend_digest }}",
    "EVENT_ADMIN_DIGEST: ${{ github.event.client_payload.admin_digest }}",
    "EVENT_SOURCE_RUN_ID: ${{ github.event.client_payload.source_run_id }}",
    "EVENT_SOURCE_WORKFLOW_PATH: ${{ github.event.client_payload.source_workflow_path }}",
    "EVENT_SOURCE_EVENT: ${{ github.event.client_payload.source_event }}",
    "EVENT_SOURCE_HEAD_SHA: ${{ github.event.client_payload.source_head_sha }}",
):
    if required not in promotion:
        fail(f"StockDividend publisher payload receiver is missing binding: {required}")
stock_event_block = promotion.split(
    'if [[ "$EVENT_ACTION" == "stockdividend-images-published" ]]; then', 1
)[1].split('elif [[ "$EVENT_ACTION" == "media-images-published" ]]; then', 1)[0]
for required in (
    'APP="$EVENT_APP"',
    'COMPONENT="release"',
    'TAG="$EVENT_COMMIT"',
    'SOURCE_COMMIT="$EVENT_COMMIT"',
    'BACKEND_DIGEST="$EVENT_BACKEND_DIGEST"',
    'ADMIN_DIGEST="$EVENT_ADMIN_DIGEST"',
    'SOURCE_RUN_ID="$EVENT_SOURCE_RUN_ID"',
    'SOURCE_WORKFLOW_PATH="$EVENT_SOURCE_WORKFLOW_PATH"',
    'SOURCE_EVENT="$EVENT_SOURCE_EVENT"',
    'SOURCE_HEAD_SHA="$EVENT_SOURCE_HEAD_SHA"',
    '[[ "$APP" == "stockdividend" ]]',
    '[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/deploy.yml" ]]',
    '[[ "$SOURCE_EVENT" == "push" || "$SOURCE_EVENT" == "workflow_dispatch" ]]',
    '[[ "$SOURCE_HEAD_SHA" =~ ^[0-9a-f]{40}$ && "$SOURCE_HEAD_SHA" == "$TAG" && "$SOURCE_HEAD_SHA" == "$SOURCE_COMMIT" ]]',
    '[[ "$BACKEND_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]',
    '[[ "$ADMIN_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]',
):
    if required not in stock_event_block:
        fail(f"StockDividend publisher payload receiver is missing validation: {required}")
if "EVENT_BACKEND_DIGEST" not in promotion or "EVENT_ADMIN_DIGEST" not in promotion:
    fail("StockDividend atomic promotion must consume backend and admin digests.")
if '[[ "$BACKEND_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]' not in promotion:
    fail("StockDividend backend digest must be validated before GHCR access.")
if '[[ "$ADMIN_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]' not in promotion:
    fail("StockDividend admin digest must be validated before GHCR access.")
if "Update Kustomize image tag or paired digests" not in promotion:
    fail("StockDividend/Media digest promotion must update both production image entries atomically.")
if "stockdividend/release" not in promotion or "scripts/promote-paired-image-digests.py" not in promotion:
    fail("StockDividend/Media paired releases must use the tested immutable digest-promotion helper.")

paired_digest_helper = (ROOT / "scripts" / "promote-paired-image-digests.py").read_text(encoding="utf-8")
for required in (
    '"stockdividend": {',
    '"media-generation": {',
    'def promote_text(',
    'def promote_file(',
    'if len(fields) != 1:',
    'duplicate image entry:',
    'os.replace(temporary_path, path)',
    'def self_test()',
    'Paired StockDividend/Media digest-promotion self-tests passed.',
):
    if required not in paired_digest_helper:
        fail(f"Paired image digest-promotion helper is missing contract: {required}")
if "python3 scripts/promote-paired-image-digests.py --self-test" not in read("validate-manifests.yml"):
    fail("Paired StockDividend/Media digest-promotion regression tests must run in validate-manifests.")
if "EVENT_COMMIT" not in promotion or "EVENT_BACKEND_DIGEST" not in promotion or "EVENT_ADMIN_DIGEST" not in promotion:
    fail("StockDividend promotion must resolve source commit and both image digests from the dispatch payload.")

# Independently bind each StockDividend full-SHA registry tag to the digest in
# the cross-repository dispatch payload before accepting the digest reference.
stockdividend_ghcr_validation = promotion.split(
    "      - name: Validate promoted image in GHCR", 1
)[1].split("      - name: Update Kustomize image tag or paired digests", 1)[0]
for required in (
    'if [[ "$APP" == "stockdividend" || "$APP" == "media-generation" ]]; then',
    'tag_reference="$image:$TAG"',
    'GHCR_EXPECTED_DIGEST="$digest"',
    'GHCR_IMAGE_REFERENCE="$tag_reference"',
    'GHCR_IMAGE_REFERENCE="$digest_reference"',
    "bash scripts/validate-ghcr-image-reference.sh",
):
    if required not in stockdividend_ghcr_validation:
        fail(f"StockDividend GHCR promotion must verify full-SHA tag-to-digest correlation: {required}")
if stockdividend_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$tag_reference"') > stockdividend_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$digest_reference"'):
    fail("StockDividend full-SHA tag-to-digest verification must run before digest-reference validation.")

# StockDividend reconciliation dispatch must wait for the exact paired digests on master.
stockdividend_readiness = promotion.split("      - name: Determine release readiness", 1)[1].split(
    "      - name: Trigger VPS reconciliation", 1
)[0]
for required in (
    'ADMIN_DIGEST: ${{ steps.input.outputs.admin_digest }}',
    'if [ "$APP" = "stockdividend" ]; then',
    'if [ "$COMPONENT" != "release" ]; then',
    'FILE="apps/stockdividend/overlays/prod/kustomization.yaml"',
    "git fetch --no-tags origin master",
    "python3 scripts/verify-stockdividend-gitops-digests.py",
    '--backend-digest "$BACKEND_DIGEST"',
    '--admin-digest "$ADMIN_DIGEST"',
    "refusing reconciliation dispatch",
):
    if required not in stockdividend_readiness:
        fail(f"StockDividend paired digest convergence gate is missing: {required}")
merge_promotion_index = promotion.index("      - name: Merge promotion PR")
readiness_index = promotion.index("      - name: Determine release readiness")
reconciliation_dispatch_index = promotion.index("      - name: Trigger VPS reconciliation")
if not merge_promotion_index < readiness_index < reconciliation_dispatch_index:
    fail("StockDividend digest convergence must be verified after the promotion PR merge and before reconciliation dispatch.")
if "python3 scripts/verify-stockdividend-gitops-digests.py --self-test" not in read("validate-github-actions.yml"):
    fail("StockDividend GitOps digest-pair regression tests must run in validate-github-actions.")
if "ready=true" not in stockdividend_readiness or "git fetch --no-tags origin master" not in stockdividend_readiness:
    fail("StockDividend readiness must be based on the GitOps master digest pair, not only the promotion PR merge response.")

# StockDividend handoffs must be tied to a real, successful publisher Actions run.
for required in (
    "EVENT_SOURCE_RUN_ID",
    "EVENT_SOURCE_WORKFLOW_PATH",
    "EVENT_SOURCE_EVENT",
    "EVENT_SOURCE_HEAD_SHA",
    'SOURCE_RUN_ID="$EVENT_SOURCE_RUN_ID"',
    'SOURCE_WORKFLOW_PATH="$EVENT_SOURCE_WORKFLOW_PATH"',
    'SOURCE_EVENT="$EVENT_SOURCE_EVENT"',
    'SOURCE_HEAD_SHA="$EVENT_SOURCE_HEAD_SHA"',
    "Verify StockDividend publisher run provenance",
    "STOCKDIVIDEND_ACTIONS_READ_TOKEN: ${{ secrets.STOCKDIVIDEND_ACTIONS_READ_TOKEN }}",
    "bash scripts/verify-stockdividend-publisher-run.sh",
):
    if required not in promotion:
        fail(f"StockDividend promotion is missing source-run provenance contract: {required}")
if promotion.index("Verify StockDividend publisher run provenance") > promotion.index("Validate promoted image in GHCR"):
    fail("StockDividend source-run provenance must pass before any promoted image is read or GitOps PR is created.")
stockdividend_provenance = (ROOT / "scripts" / "verify-stockdividend-publisher-run.sh").read_text(encoding="utf-8")
for required in (
    "STOCKDIVIDEND_ACTIONS_READ_TOKEN",
    'GH_TOKEN="$STOCKDIVIDEND_ACTIONS_READ_TOKEN" gh api "repos/phanthienquoc/stockdividend/actions/runs/$SOURCE_RUN_ID"',
    "phanthienquoc/stockdividend/actions/runs/$SOURCE_RUN_ID",
    '"$repository" == "phanthienquoc/stockdividend"',
    '"$head_repository" == "phanthienquoc/stockdividend"',
    '"$workflow_path" == "$SOURCE_WORKFLOW_PATH"',
    '"$event" == "$SOURCE_EVENT"',
    '"$branch" == "master"',
    '"$head_sha" == "$SOURCE_HEAD_SHA"',
    '"$conclusion" == "success"',
    'actions/runs/$SOURCE_RUN_ID/jobs?per_page=100',
    "verify_job_success",
    "verify_step_success",
    "Require master for production image publication",
    "Gate production GitOps promotion",
    "build-and-push",
    "Validate Platform Infra release handoff before promotion",
    "Dispatch atomic StockDividend digest promotion",
    "Verify native ARM64 runner",
    "Build and push Scraper",
    "Build and push Admin",
    "Build and push Backend",
    "Verify immutable image manifests for ARM64",
    'verify_step_success "Require master for production image publication" "Reject non-master release refs"',
    'verify_step_success "Gate production GitOps promotion" "Require explicit production promotion enablement"',
    'verify_step_success "Validate Platform Infra release handoff before promotion" "Require token and verify Platform Infra repository access"',
    'verify_step_success "Dispatch atomic StockDividend digest promotion" "Dispatch atomic StockDividend digest promotion"',
):
    if required not in stockdividend_provenance:
        fail(f"StockDividend source-run verifier is missing required metadata guard: {required}")
stockdividend_provenance_tests = (ROOT / "scripts" / "tests" / "verify-stockdividend-publisher-run.test.sh").read_text(encoding="utf-8")
for required in (
    'expect_failure "master ref validation step skipped"',
    'expect_failure "production release gate step skipped"',
    'expect_failure "Platform Infra access verification step skipped"',
    'expect_failure "atomic digest dispatch step skipped"',
):
    if required not in stockdividend_provenance_tests:
        fail(f"StockDividend provenance tests are missing skipped-step regression: {required}")
if "scripts/tests/verify-stockdividend-publisher-run.test.sh" not in (ROOT / ".github" / "workflows" / "validate-github-actions.yml").read_text(encoding="utf-8"):
    fail("StockDividend source-run provenance regression tests must run in validate-github-actions.")
if "STOCKDIVIDEND_ACTIONS_READ_TOKEN" not in (ROOT / "docs" / "credentials.md").read_text(encoding="utf-8") or "STOCKDIVIDEND_ACTIONS_READ_TOKEN" not in (ROOT / "docs" / "credentials-key.md").read_text(encoding="utf-8"):
    fail("The private StockDividend Actions read token must be documented in both credential inventories.")


# Media Generation publishes a paired digest event tied to a real, successful publisher Actions run.

if "media-release-requested" in promotion:
    fail("Legacy Media tag-only dispatch is retired; only the paired digest event is accepted.")
for obsolete in ("  fanout-media-release:", "  coordinate-media-release:"):
    if obsolete in promotion:
        fail(f"Obsolete Media tag-only promotion job remains: {obsolete.strip()}")

if "media-images-published" not in promotion:
    fail("GitOps promotion must consume the paired Media digest event.")
if "EVENT_FRONTEND_DIGEST" not in promotion or "EVENT_BACKEND_DIGEST" not in promotion:
    fail("Media digest promotion must consume frontend and backend digest payload fields.")
if "media-generation/release" not in promotion:
    fail("Media digest promotion must use the paired release target, not independent component updates.")
if '[[ "$FRONTEND_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]' not in promotion:
    fail("Media frontend digest must be validated before GHCR access.")
if '[[ "$BACKEND_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]' not in promotion:
    fail("Media backend digest must be validated before GHCR access.")
if '[[ "$TAG" == *-"$SOURCE_COMMIT" ]]' not in promotion:
    fail("Media release label must correlate to its full source commit SHA.")

# Media's full-SHA release tag must independently resolve to each digest in
# the paired dispatch payload before the digest-only reference is accepted.
media_ghcr_validation = promotion.split(
    "      - name: Validate promoted image in GHCR", 1
)[1].split("      - name: Update Kustomize image tag or paired digests", 1)[0]
for required in (
    'if [[ "$APP" == "stockdividend" || "$APP" == "media-generation" ]]; then',
    'tag_reference="$image:$TAG"',
    'GHCR_EXPECTED_DIGEST="$digest"',
    'GHCR_IMAGE_REFERENCE="$tag_reference"',
    'GHCR_IMAGE_REFERENCE="$digest_reference"',
):
    if required not in media_ghcr_validation:
        fail(f"Media GHCR promotion must verify full-SHA release tag-to-digest correlation: {required}")
if media_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$tag_reference"') > media_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$digest_reference"'):
    fail("Media release tag-to-digest verification must run before digest-reference validation.")
for required in (
    "EVENT_SOURCE_RUN_ID",
    "EVENT_SOURCE_WORKFLOW_PATH",
    "EVENT_SOURCE_EVENT",
    "EVENT_SOURCE_HEAD_SHA",
    'SOURCE_RUN_ID="$EVENT_SOURCE_RUN_ID"',
    'SOURCE_WORKFLOW_PATH="$EVENT_SOURCE_WORKFLOW_PATH"',
    'SOURCE_EVENT="$EVENT_SOURCE_EVENT"',
    'SOURCE_HEAD_SHA="$EVENT_SOURCE_HEAD_SHA"',
    '[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/wf-03-media-production-deploy.yml" ]]',
    '[[ "$SOURCE_EVENT" == "push" || "$SOURCE_EVENT" == "workflow_dispatch" ]]',
    "Verify Media publisher run provenance",
    "bash scripts/verify-media-publisher-run.sh",
):
    if required not in promotion:
        fail(f"Media promotion is missing source-run provenance contract: {required}")
if promotion.index("Verify Media publisher run provenance") > promotion.index("Validate promoted image in GHCR"):
    fail("Media source-run provenance must pass before any promoted image is read or GitOps PR is created.")
media_provenance = (ROOT / "scripts" / "verify-media-publisher-run.sh").read_text(encoding="utf-8")
for required in (
    "https://api.github.com/repos/phanthienquoc/media-generation/actions/runs/$SOURCE_RUN_ID",
    '"$repository" == "phanthienquoc/media-generation"',
    '"$head_repository" == "phanthienquoc/media-generation"',
    '"$workflow_path" == "$SOURCE_WORKFLOW_PATH"',
    '"$event" == "$SOURCE_EVENT"',
    '"$branch" == "master"',
    '"$head_sha" == "$SOURCE_HEAD_SHA"',
    '"$conclusion" == "success"',
    '$API_URL/jobs?per_page=100',
    "verify_job_success",
    "verify_step_success",
    "Require master for production release",
    "Resolve production image tag",
    "Build frontend (native ARM64)",
    "Build backend (native ARM64)",
    "Publish immutable images and promote platform-infra",
    "Verify native architecture",
    "Build frontend image",
    "Verify frontend architecture",
    "Export and validate frontend image",
    "Validate backend inputs",
    "Build backend image",
    "Verify backend architecture",
    "Export and validate backend image",
    "Load and validate exact release images",
    "Publish exact release images",
    "Verify immutable registry digests and ARM64 manifests",
    "Notify platform-infra",
):
    if required not in media_provenance:
        fail(f"Media source-run verifier is missing required metadata guard: {required}")
if "Authorization" in media_provenance:
    fail("Public Media source-run verification must not introduce a cross-repository credential.")
if "scripts/tests/verify-media-publisher-run.test.sh" not in (ROOT / ".github" / "workflows" / "validate-github-actions.yml").read_text(encoding="utf-8"):
    fail("Media source-run provenance regression tests must run in validate-github-actions.")
if "MEDIA_FRONTEND_REF" not in reconcile or "MEDIA_BACKEND_REF" not in reconcile:
    fail("Shared reconciliation must resolve both Media image references.")
if "digest:sha256:[0-9a-f]{64}" not in reconcile:
    fail("Shared reconciliation must validate digest-pinned Media image references.")
if "Resolve paired Media image references" not in reconcile:
    fail("Shared reconciliation must support paired Media tags and digests.")

# MicroFE digest promotions must use the shared GitOps promotion workflow.
if "microfe-images-published" not in promotion:
    fail("gitops-image-promotion.yml must consume microfe-images-published.")
if "RELEASE_INPUT: ${{ github.event.client_payload.release }}" not in promotion:
    fail("MicroFE promotion must require a release label correlated with the source commit.")
if '[[ "$RELEASE_INPUT" == "$EXPECTED_RELEASE" ]]' not in promotion:
    fail("MicroFE release label must be checked against the full source commit SHA.")
if "github.event.client_payload.release || github.event.client_payload.commit" not in promotion:
    fail("Promotion run name must expose the correlated MicroFE release label.")
for field in ("shell_digest", "ws_digest"):
    if field not in promotion:
        fail(f"Shared MicroFE promoter is missing required payload field: {field}")
if 'for digest in "$SHELL_DIGEST" "$WS_DIGEST"; do' not in promotion:
    fail("MicroFE promotion must require Shell and WebSocket digests.")
if 'if [[ -n "${AUTH_DIGEST:-}" ]]; then' not in promotion:
    fail("Legacy auth_digest must be optional so Shell/WS-only releases remain valid.")

microfe_provenance = (ROOT / "scripts" / "verify-tce-microfe-publisher-run.sh").read_text(encoding="utf-8")
microfe_job = promotion.split("  promote-microfe-digests:", 1)[1].split("  fanout-tce-release:", 1)[0]
provenance_step = microfe_job.find("name: Verify TCE MicroFE publisher provenance")
ghcr_step = microfe_job.find("name: Validate promoted MicroFE images in GHCR")
if provenance_step < 0 or ghcr_step < 0 or provenance_step > ghcr_step:
    fail("MicroFE source-run provenance must be verified before GHCR digest promotion.")
for required in (
    "SOURCE_APP",
    "SOURCE_REPOSITORY",
    "SOURCE_RUN_ID",
    "SOURCE_WORKFLOW_PATH",
    "SOURCE_EVENT",
    "SOURCE_HEAD_SHA",
    "SOURCE_COMMIT",
    "repository.full_name",
    "head_repository.full_name",
    "conclusion",
    "Build and publish MicroFE WebSocket image",
    "Build and publish MicroFE Shell image",
    "Dispatch immutable image promotion and verify production",
):
    if required not in microfe_provenance:
        fail(f"MicroFE source-run provenance verifier is missing required guard: {required}")
if "Authorization" in microfe_provenance:
    fail("Public TCE source-run verification must not introduce a cross-repository credential.")

microfe_ghcr_validation = microfe_job.split(
    "name: Validate promoted MicroFE images in GHCR", 1
)[1].split("name: Update MicroFE Kustomize image digests", 1)[0]
for required in (
    "SOURCE_COMMIT: ${{ steps.digests.outputs.source_commit }}",
    "for component in shell ws; do",
    'image="ghcr.io/phanthienquoc/microfe-$component"',
    'digest_var="${component^^}_DIGEST"',
    'expected="${!digest_var}"',
    'GHCR_EXPECTED_DIGEST="$expected"',
    'GHCR_IMAGE_REFERENCE="$image:$SOURCE_COMMIT"',
    'GHCR_IMAGE_REFERENCE="$image@$expected"',
    "bash scripts/validate-ghcr-image-reference.sh",
):
    if required not in microfe_ghcr_validation:
        fail(f"MicroFE receiver is missing full-SHA tag-to-digest validation: {required}")
if microfe_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$image:$SOURCE_COMMIT"') > microfe_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$image@$expected"'):
    fail("MicroFE full-SHA tag-to-digest verification must run before digest-reference validation.")

if "scripts/tests/verify-tce-microfe-publisher-run.test.sh" not in (ROOT / ".github" / "workflows" / "validate-github-actions.yml").read_text(encoding="utf-8"):
    fail("MicroFE publisher provenance regression tests must run in validate-github-actions.")

# Promotion renders the updated MicroFE Kustomization; do not rely on an ambient runner kubectl.
microfe_job = promotion.split("  promote-microfe-digests:", 1)[1].split("  fanout-tce-release:", 1)[0]
kubectl_install_index = microfe_job.find("name: Install pinned kubectl for MicroFE manifest render")
kustomize_render_index = microfe_job.find("kubectl kustomize platform/microfe")
if kubectl_install_index < 0 or kustomize_render_index < 0 or kubectl_install_index > kustomize_render_index:
    fail("MicroFE promotion must install pinned kubectl before rendering the updated Kustomization.")
for required in (
    "KUBECTL_VERSION: v1.36.3",
    "sha256sum --check",
    "sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl",
):
    if required not in microfe_job:
        fail(f"MicroFE promotion is missing pinned kubectl installation contract: {required}")
if (WORKFLOW_DIR / "reconcile-microfe.yml").exists():
    fail("Dedicated reconcile-microfe.yml must be removed.")
if "gitops-promoted-ready" not in reconcile:
    fail("reconcile-vps.yml must consume the shared GitOps promotion event.")
if "run-name:" not in reconcile or "github.event.client_payload.app" not in reconcile or "github.event.client_payload.release" not in reconcile:
    fail("reconcile-vps.yml must expose target app and release in its run name for release verification.")
if "microfe" not in reconcile:
    fail("reconcile-vps.yml must retain MicroFE deployment scope support.")

# TCE release must promote the verified web/service digest pair atomically.
tce_promotion = promotion.split("  promote-tce-digests:", 1)[1].split(
    "  coordinate-tce-release:", 1
)[0]
for required in (
    "github.event.action == 'tce-release-requested'",
    "github.event.client_payload.web_digest",
    "github.event.client_payload.service_digest",
    "Verify TCE release payload and publisher provenance",
    "bash scripts/verify-tce-publisher-run.sh",
    "TARGET_APP=tce-dashboard",
    "docker buildx imagetools inspect",
    "scripts/validate-ghcr-image-reference.sh",
    "apps/tce-dashboard/overlays/prod/kustomization.yaml",
    "scripts/promote-tce-image-digests.py",
    "Create TCE paired digest promotion PR",
    "Merge TCE paired digest promotion PR",
):
    if required not in tce_promotion:
        fail(f"TCE digest promotion is missing required contract: {required}")
if tce_promotion.index("Verify TCE release payload and publisher provenance") > tce_promotion.index("Validate TCE GHCR pull access"):
    fail("TCE publisher provenance must pass before GHCR access or image promotion.")
if tce_promotion.index("Verify TCE tag-to-digest mapping") > tce_promotion.index("Update TCE production image digests"):
    fail("TCE registry tag/digest correlation must pass before GitOps mutation.")
if "needs: promote-tce-digests" not in promotion.split("  coordinate-tce-release:", 1)[1].split("  fanout-media-release:", 1)[0]:
    fail("TCE release coordinator must wait for the atomic digest promotion job.")
if "WEB_DIGEST_ON_MASTER" not in promotion or "SERVICE_DIGEST_ON_MASTER" not in promotion:
    fail("TCE coordinator must verify both promoted digests on master before reconciliation.")
tce_provenance = (ROOT / "scripts" / "verify-tce-publisher-run.sh").read_text(encoding="utf-8")
for required in (
    "https://api.github.com/repos/phanthienquoc/TCE-dashboard/actions/runs/$SOURCE_RUN_ID",
    '"$repository" == "phanthienquoc/TCE-dashboard"',
    '"$head_repository" == "phanthienquoc/TCE-dashboard"',
    '"$workflow_path" == "$SOURCE_WORKFLOW_PATH"',
    '"$event" == "$SOURCE_EVENT"',
    '"$branch" == "master"',
    '"$head_sha" == "$SOURCE_HEAD_SHA"',
    '"$conclusion" == "success"',
    '[[ "$WEB_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]',
    '[[ "$SERVICE_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]',
):
    if required not in tce_provenance:
        fail(f"TCE source-run verifier is missing required provenance/digest guard: {required}")
if "Authorization" in tce_provenance:
    fail("Public TCE source-run verification must not introduce a cross-repository credential.")
if "scripts/tests/verify-tce-publisher-run.test.sh" not in (ROOT / ".github" / "workflows" / "validate-github-actions.yml").read_text(encoding="utf-8"):
    fail("TCE source-run provenance regression tests must run in validate-github-actions.")
if "promote-tce-image-digests.py --self-test" not in (ROOT / ".github" / "workflows" / "validate-github-actions.yml").read_text(encoding="utf-8"):
    fail("TCE paired digest promotion script self-tests must run in validate-github-actions.")

# TCE reconciliation and live image verification must support both legacy tag pairs and digest pairs.
tce_ref_resolver = (ROOT / "scripts" / "resolve-tce-gitops-image-refs.py").read_text(encoding="utf-8")
for required in (
    'IMAGES = {',
    'newTag:',
    'digest:',
    'TCE web/service references must both be tags or both be digests',
    'TCE legacy web/service tags must be identical',
    'sha256:[0-9a-f]{64}',
):
    if required not in tce_ref_resolver:
        fail(f"TCE GitOps image-reference resolver is missing: {required}")
for script_path in ("verify-tce-gitops-release.sh", "verify-tce-gitops-images.sh"):
    script_text = (ROOT / "scripts" / script_path).read_text(encoding="utf-8")
    if "resolve-tce-gitops-image-refs.py" not in script_text:
        fail(f"{script_path} must use the shared tag/digest-aware TCE reference resolver.")
    if "--validate-pair" not in script_text:
        fail(f"{script_path} must reject mixed TCE tag/digest release pairs.")
if "resolve-tce-gitops-image-refs.py --self-test" not in (ROOT / ".github" / "workflows" / "validate-github-actions.yml").read_text(encoding="utf-8"):
    fail("TCE tag/digest resolver regression tests must run in validate-github-actions.")

# Scheduled reconciliation logic must have a matching schedule trigger.
if "github.event_name == 'schedule'" in reconcile and not re.search(
    r"(?m)^\s*schedule:\s*$", reconcile
):
    fail(
        "reconcile-vps.yml references github.event_name == 'schedule' "
        "but does not declare an on.schedule trigger."
    )

# The shared apply job and the aggregate lane gate must both fail hard on errors.
if "name: Fail if shared reconciliation failed" not in reconcile:
    fail("reconcile-vps.yml is missing its shared reconciliation failure gate.")
shared_gate = reconcile.split("name: Fail if shared reconciliation failed", 1)[1].split(
    "  deploy-auth-service:", 1
)[0]
if "PREFLIGHT_STATUS: ${{ steps.preflight.outcome }}" not in shared_gate:
    fail("The shared reconciliation gate must inspect the preflight step outcome.")
if 'if [ "$PREFLIGHT_STATUS" != "success" ]' not in shared_gate:
    fail("A failed preflight must never be reported as a successful no-drift reconciliation.")
if 'case "$DRIFT" in' not in shared_gate or '            *)' not in shared_gate:
    fail("The shared reconciliation gate must reject missing or invalid drift outputs.")
if "name: Deployment lane summary / final gate" not in reconcile:
    fail("reconcile-vps.yml is missing its final deployment lane failure gate.")

# Each application must have an independent rollout/health lane.
required_lanes = (
    "  deploy-auth-service:",
    "  deploy-microfe:",
    "  deploy-tce-dashboard:",
    "  deploy-stockdividend:",
    "  deploy-media-generation:",
    "  deploy-keycloak:",
)
for lane in required_lanes:
    if lane not in reconcile:
        fail(f"reconcile-vps.yml is missing independent deployment lane: {lane.strip()}")

# Auth rollout must not be part of the MicroFE Shell/WS lane.
microfe_lane = reconcile.split("  deploy-microfe:", 1)[1].split("  deploy-tce-dashboard:", 1)[0]
if "rollout status deployment/microfe-auth" in microfe_lane:
    fail("MicroFE lane must not wait for the independent Auth rollout.")

if "Verify Auth workload health" not in reconcile or "Verify MicroFE workload health" not in reconcile or "Verify Keycloak workload health" not in reconcile:
    fail("Auth and MicroFE lanes must retain workload health verification.")

# Keycloak must have a dedicated target and must not be added to regular app reconciliation.
keycloak_lane = reconcile.split("  deploy-keycloak:", 1)[1].split("  deploy-tce-dashboard:", 1)[0]
if 'needs.reconcile.outputs.target_app == \'keycloak\'' not in keycloak_lane:
    fail("Keycloak lane must require explicit target_app=keycloak.")
if "apply -k platform/keycloak" not in keycloak_lane:
    fail("Keycloak lane must use its isolated Kustomize path.")
if "provision-keycloak-secret" not in keycloak_lane:
    fail("Keycloak lane must provision its separate runtime Secret.")

# Validate private-image pull access before any runtime Secret or pull credential mutation.
preflight_index = reconcile.find("name: Validate GHCR pull access before mutating cluster credentials")
auth_secret_index = reconcile.find("name: Provision Auth runtime Secret from platform-infra Environment")
if preflight_index < 0 or auth_secret_index < 0 or preflight_index > auth_secret_index:
    fail("GHCR pull-access preflight must run before provisioning the Auth runtime Secret.")

# The GHCR pull Secret is shared across namespaces, so every apply must validate all referenced packages.
ghcr_preflight_block = reconcile.split("name: Validate GHCR pull access before mutating cluster credentials", 1)[1].split(
    "- name: Provision Auth runtime Secret from platform-infra Environment", 1
)[0]
if 'TARGET_APP=all GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" ./scripts/validate-ghcr-pull-access.sh' not in ghcr_preflight_block:
    fail("Every non-Keycloak apply must validate all production GHCR packages before reconciling the shared pull Secret.")

# GHCR pull preflight must safely handle copied secret line endings before using curl config.
ghcr_probe = (ROOT / "scripts" / "validate-ghcr-pull-access.sh").read_text(encoding="utf-8")
if "sed 's/\\r$//'" not in ghcr_probe:
    fail("GHCR preflight must normalize a terminal CR from copied secret values.")
if "contains embedded whitespace or quotes" not in ghcr_probe:
    fail("GHCR preflight must reject embedded whitespace/quotes instead of passing malformed credentials to curl.")

# Read-only inspection must expose PVC/PV reclaim-policy and claim-binding evidence before namespace retirement.
for required in (
    'echo; echo "### Persistent storage inventory"',
    'sudo "$KCTL" get pvc -A -o wide',
    'sudo "$KCTL" get pv -o wide',
):
    if required not in inspection_script:
        fail(f"VPS inspection is missing persistent storage evidence: {required}")
bootstrap_allowlist = (ROOT / "scripts" / "bootstrap-runner.sh").read_text(encoding="utf-8")
if "pv|pvc" not in bootstrap_allowlist:
    fail("The read-only platform-kubectl allowlist must permit PVC and PV inventory queries.")

# GHCR pulls use one platform-owned credential across production namespaces.
bootstrap_script = (ROOT / "scripts" / "bootstrap-runner.sh").read_text(encoding="utf-8")
ghcr_step = reconcile.split("- name: Bootstrap GHCR pull credentials", 1)[1].split(
    "- name: Restart target workloads blocked on image pulls", 1
)[0]
if "${{ secrets.GHCR_READ_TOKEN }}" not in ghcr_step:
    fail("reconcile-vps.yml must use the canonical GHCR_READ_TOKEN secret.")
if "secrets.GITHUB_TOKEN" in ghcr_step or "Platform-infra-token" in ghcr_step:
    fail("GHCR bootstrap must not silently fall back to a cross-repository-inadequate token.")
if "secrets.GHCR_READ_TOKEN || github.token" in promotion:
    fail("gitops-image-promotion.yml must not fall back to github.token for private GHCR packages.")
if promotion.count("GHCR_TOKEN: ${{ secrets.GHCR_READ_TOKEN }}") < 2:
    fail("Both GitOps promotion paths must use canonical GHCR_READ_TOKEN.")

# Registry reads use the dedicated GHCR_READ_TOKEN, never the workflow GITHUB_TOKEN.
for workflow_name, workflow in (("reconcile-vps.yml", reconcile), ("gitops-image-promotion.yml", promotion)):
    if re.search(r"(?m)^\s+packages:\s+(?:read|write)\s*$", workflow):
        fail(f"{workflow_name} must not grant GITHUB_TOKEN package permissions; GHCR reads use GHCR_READ_TOKEN.")

# Promotion must validate package-level authorization and the exact immutable tag/digest before GitOps mutation.
if 'TARGET_APP=microfe GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" bash scripts/validate-ghcr-pull-access.sh' not in promotion:
    fail("MicroFE promotion must validate GHCR package pull access before registry login.")
if 'TARGET_APP="$APP" GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" bash scripts/validate-ghcr-pull-access.sh' not in promotion:
    fail("Application promotion must validate GHCR package pull access before registry login.")

# Docker's registry-wide login endpoint can be denied even when scoped package reads work.
# Verify the exact tag/digest directly with a package-scoped Registry V2 bearer token instead.
if "docker login ghcr.io" in promotion or "docker manifest inspect" in promotion:
    fail("Promotion must not depend on registry-wide Docker login for private GHCR reads.")
if 'GHCR_IMAGE_REFERENCE="$image@$expected"' not in promotion or "bash scripts/validate-ghcr-image-reference.sh" not in promotion:
    fail("MicroFE promotion must verify each exact immutable image digest through Registry V2.")
if 'GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" GHCR_IMAGE_REFERENCE="$IMAGE" bash scripts/validate-ghcr-image-reference.sh' not in promotion:
    fail("Application promotion must verify the exact immutable tag through Registry V2.")

ghcr_image_validator = (ROOT / "scripts" / "validate-ghcr-image-reference.sh").read_text(encoding="utf-8")
for required in (
    ".manifests[]?",
    ".platform.os == \"linux\"",
    ".platform.architecture == \"arm64\"",
    ".config.digest",
    "/blobs/",
    ".architecture",
    ".os",
):
    if required not in ghcr_image_validator:
        fail(f"Exact GHCR image validation must enforce linux/arm64 support: {required}")
if "validate-ghcr-image-platform.test.sh" not in github_actions:
    fail("GitHub Actions validation must run the exact GHCR linux/arm64 platform regression tests.")
if "github.event.action || github.event_name" not in promotion:
    fail("GitOps promotion run names must identify dispatch events that omit app/component fields.")

# The canonical GHCR credential is stored in the protected production Environment.
# Every job that consumes it must bind that Environment or the secret resolves empty.
promotion_lines = promotion.splitlines()
for job_name in ("promote-microfe-digests", "promote"):
    start = next((i for i, line in enumerate(promotion_lines) if line == f"  {job_name}:"), None)
    if start is None:
        fail(f"Could not find GHCR-consuming promotion job: {job_name}")
    end = next(
        (i for i in range(start + 1, len(promotion_lines))
         if promotion_lines[i].startswith("  ")
         and not promotion_lines[i].startswith("    ")
         and promotion_lines[i].endswith(":")),
        len(promotion_lines),
    )
    block = "\n".join(promotion_lines[start:end])
    if "    environment: production" not in block:
        fail(f"{job_name} must bind the production Environment to read GHCR_READ_TOKEN.")
for namespace in ("microfe-platform", "stock-prod", "tce-prod", "media-prod"):
    if namespace not in bootstrap_script.split("ghcr_namespaces=(", 1)[-1].split(")", 1)[0]:
        fail(f"GHCR pull reconciliation is missing production namespace: {namespace}")
if 'patch deployment "$deployment"' not in bootstrap_script or 'imagePullSecrets' not in bootstrap_script:
    fail("GHCR pull reconciliation must normalize GHCR workload imagePullSecrets.")

# Deployment tracker structural contract: keep the file non-empty, the five repositories
# in the readiness table, and the current action/runtime sections available to operators.
tracker_path = ROOT / "docs" / "cross-repo-deployment-tracker.md"
if not tracker_path.is_file() or tracker_path.stat().st_size == 0:
    fail("Cross-repo deployment tracker must exist and must not be empty.")
tracker = tracker_path.read_text(encoding="utf-8")
if "PLATFORM_INFRA_AUTOMATION_TOKEN" in promotion and "PLATFORM_INFRA_AUTOMATION_TOKEN" not in tracker:
    fail("Tracker must record the automation token required by the promotion workflow.")

if "# Cross-Repository Production Deployment Tracker" not in tracker:
    fail("Cross-repo deployment tracker title is missing.")
required_tracker_sections = (
    "Last reviewed:",
    "## Repository readiness",
    "## Current actions",
    "## Current runtime blockers",
)
if any(section not in tracker for section in required_tracker_sections):
    fail("Cross-repo deployment tracker must retain its review date, readiness table, current actions, and runtime blockers.")
readiness_section = tracker.split("## Repository readiness", 1)[1].split("\n## ", 1)[0]
for repository in (
    "phanthienquoc/platform-infra",
    "phanthienquoc/TCE-dashboard",
    "phanthienquoc/stockdividend",
    "phanthienquoc/media-generation",
    "phanthienquoc/phanthienquoc-authentication",
):
    if repository not in readiness_section:
        fail(f"Cross-repo deployment readiness table is missing repository: {repository}")


# Auth shutdown must be an isolated, allowlisted maintenance operation.
if "rollout-status-v14-stockdividend-managed-workloads" not in bootstrap_script:
    fail("Runner bootstrap must publish the versioned scoped image-pull restart policy.")
if '  scale)' not in bootstrap_script or 'scale deployment/microfe-auth deployment/keycloak --replicas=0 -n microfe-platform' not in bootstrap_script:
    fail("Runner bootstrap must allow only the exact Auth/Keycloak scale-to-zero command.")

if "rollout-status-v14-stockdividend-managed-workloads" not in reconcile:
    fail("Production reconciliation must require the current v14 managed-workload runner policy.")

# Keep operator-facing diagnostics aligned with the enforced runner policy version.
for required in (
    "Runner policy v14 (managed StockDividend workloads) is ready.",
    "Waiting for runner bootstrap policy v14",
    "Runner policy is not updated to managed-workload v14",
):
    if required not in reconcile:
        fail(f"Reconciliation diagnostics are missing the current v14 policy label: {required}")
if "runner bootstrap policy v13" in reconcile or "image-pull restart v13" in reconcile:
    fail("Reconciliation diagnostics must not report the retired v13 runner policy after v14 is required.")
auth_provision = read("provision-auth-runtime-secret.yml")
if "rollout-status-v14-stockdividend-managed-workloads" not in auth_provision:
    fail("Standalone Auth secret provisioning must accept the current v14 runner policy.")

restart_step = reconcile.split("- name: Restart target workloads blocked on image pulls", 1)[1].split(
    "- name: Validate TCE release pairing", 1
)[0]
if 'restart-blocked-image-pulls "$TARGET_APP"' not in restart_step:
    fail("Reconciliation must pass the resolved target app to image-pull recovery.")
if "restart-blocked-image-pulls\n" in restart_step:
    fail("Reconciliation must not invoke image-pull recovery without an explicit scope.")

restart_block = bootstrap_script.split("  restart-blocked-image-pulls)", 1)[1].split(
    "  logs)", 1
)[0]
if '[[ "$#" -eq 2 ]]' not in restart_block or "unsupported image-pull restart scope" not in restart_block:
    fail("Runner image-pull recovery must accept exactly one allowlisted scope.")
if "local selector" not in restart_block or "matchLabels" not in restart_block:
    fail("Runner image-pull recovery must inspect only pods selected by each target Deployment.")
if 'rollout restart "deployment/$deployment"' not in restart_block:
    fail("Runner image-pull recovery must restart only the Deployment with a blocked image pull.")
for required in (
    "waiting_failures",
    "permanent_failures",
    "no match for platform in manifest",
    "manifest unknown",
    "manifest not found",
    "ascii_downcase",
    "Permanent image-pull failure",
    "Transient image-pull failure",
):
    if required not in restart_block:
        fail(f"Runner image-pull recovery is missing permanent/transient error handling: {required}")
for required_target in (
    "microfe)","auth-service)","tce-dashboard)","stockdividend)","media-generation)","all)",
):
    if required_target not in restart_block:
        fail(f"Runner image-pull recovery is missing an explicit target mapping: {required_target}")
for required_deployment in (
    "microfe-platform microfe-shell",
    "microfe-platform microfe-ws",
    "microfe-platform microfe-auth",
    "tce-prod tce-service",
    "tce-prod tce-frontend",
    "stock-prod stock-admin",
    "stock-prod stock-backend",
    "media-prod media-generation",
    "media-prod media-generation-frontend",
):
    if required_deployment not in restart_block:
        fail(f"Runner image-pull recovery is missing a production Deployment mapping: {required_deployment}")

# StockDividend's current source tree and production Kustomize/Ingress own only
# Admin and Backend. Keep the legacy stock-frontend Pod untouched, but exclude
# that unowned Deployment from rollout, restart, rollback, and health authorities.
health_gate = (ROOT / "scripts" / "verify-workload-health.sh").read_text(encoding="utf-8")
runner_script_content = (ROOT / "scripts" / "bootstrap-runner.sh").read_text(encoding="utf-8")
readiness_script_content = (ROOT / "scripts" / "validate-recovery-readiness.sh").read_text(encoding="utf-8")
stockdividend_readme = (ROOT / "apps" / "stockdividend" / "README.md").read_text(encoding="utf-8")
if 'app in (stock-admin,stock-backend)' not in health_gate:
    fail("StockDividend health checks must be scoped to the GitOps-owned Admin and Backend pods.")
if "deployment/stock-frontend" in reconcile:
    fail("The StockDividend rollout lane must not wait for the unowned legacy stock-frontend Deployment.")
if "stock-prod stock-frontend" in runner_script_content or "deployment/stock-frontend" in runner_script_content:
    fail("Runner image-pull recovery must not restart or expose rollout authority for legacy stock-frontend.")
if "deployment/stock-frontend stock-prod" in readiness_script_content:
    fail("Recovery readiness must not require rollback history for the unowned legacy stock-frontend Deployment.")
if "stock-frontend" not in stockdividend_readme or "legacy" not in stockdividend_readme.lower():
    fail("StockDividend runtime documentation must identify the legacy stock-frontend ownership boundary.")

runner_bootstrap = read("bootstrap-runner.yml")
if '      - "scripts/bootstrap-runner.sh"' not in runner_bootstrap:
    fail("A runner helper change must trigger the approved VPS runner bootstrap workflow.")
if "platform/keycloak/**" not in reconcile:
    fail("Keycloak manifest changes must trigger the shared reconcile workflow.")
if "name: Resolve push deployment scope" not in reconcile:
    fail("Every production manifest push must resolve an app-specific rollout scope from the complete changed-file diff.")
if 'if: ${{ github.event_name == \'push\' }}' not in reconcile:
    fail("Push deployment scope resolution must run only for push events.")
if 'git diff --name-only "$before" "$GITHUB_SHA"' not in reconcile:
    fail("Push-scope resolution must inspect the complete before-to-head diff.")
if "bash scripts/resolve-push-deployment-scope.sh" not in reconcile:
    fail("The reconcile workflow must use the tested path-scope resolver.")
push_scope_script = ROOT / "scripts" / "resolve-push-deployment-scope.sh"
if not push_scope_script.is_file():
    fail("The push deployment scope resolver script is missing.")
push_scope_contract = push_scope_script.read_text(encoding="utf-8")
for path_contract in (
    "platform/microfe/*",
    "platform/auth-service/*",
    "apps/tce-dashboard/*",
    "apps/stockdividend/*",
    "apps/media-generation/*",
    "platform/keycloak/*",
    "environments/prod/*",
):
    if path_contract not in push_scope_contract:
        fail(f"Push deployment scope resolver is missing path mapping: {path_contract}")
if "Unclassified production-trigger path" not in push_scope_contract:
    fail("Unknown push paths must fail closed instead of silently reconciling every application.")
for ignored_path_contract in (
    ".github/workflows/*",
    "scripts/validate-*.py",
    "scripts/tests/*",
    "docs/*",
    "debug/vps-latest.md",
):
    if ignored_path_contract not in push_scope_contract:
        fail(f"Push scope resolver must ignore non-deployment metadata path: {ignored_path_contract}")
if "assert_failure .github/workflows/validate-manifests.yml" not in push_scope_contract:
    fail("Ignored metadata-only changes must not silently select a production deployment scope.")
if "KEYCLOAK_REPLICAS_OVERRIDE" not in push_scope_contract or "auth-shutdown" not in push_scope_contract:
    fail("Keycloak-only pushes must retain the isolated replica-aware Auth shutdown/Keycloak rollout contract.")
if "name: Verify Auth and Keycloak shutdown state" not in reconcile:
    fail("Auth shutdown must verify desired/ready/updated replicas are zero and no matching pods remain.")
if 'if [ "$TARGET_APP" = "auth-shutdown" ]; then' not in reconcile:
    fail("Auth shutdown must bypass shared GitOps apply and remain scoped to the two Auth workloads.")
shutdown_block = reconcile.split("name: Apply Auth and Keycloak shutdown only", 1)[1].split("name: Preflight diff", 1)[0]
if 'sudo /usr/local/sbin/platform-kubectl apply -k platform/keycloak' not in shutdown_block:
    fail("Auth shutdown must reconcile only the dedicated Keycloak resource set before scaling workloads.")
if 'scale deployment/microfe-auth deployment/keycloak --replicas=0 -n microfe-platform' not in shutdown_block:
    fail("Auth shutdown target is missing its exact allowlisted scale command.")
for step_name in (
    "Validate GHCR pull access before mutating cluster credentials",
    "Bootstrap GHCR pull credentials",
    "Restart target workloads blocked on image pulls",
):
    start = reconcile.find(f"- name: {step_name}")
    if start < 0:
        fail(f"Missing shared maintenance step: {step_name}")
    end = reconcile.find("\n      - name:", start + 10)
    block = reconcile[start:end if end >= 0 else len(reconcile)]
    if "steps.scope.outputs.target_app != 'auth-shutdown'" not in block.split("run:", 1)[0]:
        fail(f"{step_name} must not run for auth-shutdown because it mutates or restarts shared workloads.")


# A read-only watchdog detects missing scheduled reconcile events independently.
watchdog = read("reconcile-schedule-watchdog.yml")
def scheduled_crons(workflow: str) -> list[str]:
    return re.findall(r'(?m)^ *- *cron: *"([^"]+)"', workflow)


if scheduled_crons(reconcile) != ["7,22,37,52 * * * *"]:
    fail("reconcile-vps must retain a 15-minute cadence offset to minutes 7/22/37/52.")
if scheduled_crons(watchdog) != ["12,27,42,57 * * * *"]:
    fail("The read-only watchdog must run 5 minutes after each offset reconciliation slot.")
if scheduled_crons(inspection) != ["2,32 * * * *"]:
    fail("VPS inspection must retain its 30-minute cadence at minutes 2 and 32.")

if scheduled_crons(recovery) != ["10,25,40,55 * * * *"]:
    fail("Scheduled ops recovery must retain its independent 15-minute offset.")
if "actions: write" not in recovery or "contents: read" not in recovery:
    fail("Scheduled ops recovery must use only Actions write and Contents read permissions.")
for required in (
    "gh workflow run reconcile-vps.yml",
    "-f mode=apply",
    "-f allow_image_changes=false",
    "-f target_app=all",
    "gh workflow run inspect-vps.yml",
    ".updated_at // .run_started_at // .created_at",
    ".run_started_at // .created_at",
    "gh api -X GET",
    "head_sha == $sha",
    "Dispatch payload: ref=master sha=$dispatch_sha",
    "sort_by(.created_at) | last // empty",
    "steps.reconcile.outputs.busy != 'true'",
):
    if required not in recovery:
        fail(f"Scheduled ops recovery contract is missing: {required}")
for forbidden in ("platform-kubectl", "scripts/reconcile-vps.sh", "kubectl apply", "docker compose", "ssh "):
    if forbidden in recovery:
        fail(f"Schedule recovery must dispatch existing GitHub workflows only, not deploy directly: {forbidden}")
if "workflow_run:" not in watchdog or "      - inspect-vps" not in watchdog or "      - reconcile-vps" not in watchdog or "      - Recover Stale Scheduled Ops" not in watchdog:
    fail("The watchdog must run after scheduled reconciliation, inspection, and recovery-controller completions.")
if "      - completed" not in watchdog or "github.event.workflow_run.event == 'schedule'" not in watchdog:
    fail("The watchdog fallback must be limited to completed scheduled reconcile-vps/inspect-vps/recovery runs.")
if '"/repos/${GITHUB_REPOSITORY}/actions/workflows/reconcile-vps.yml/runs"' in watchdog:
    fail("The watchdog gh api endpoint must not start with a slash.")
if '"repos/${GITHUB_REPOSITORY}/actions/workflows/reconcile-vps.yml/runs"' not in watchdog:
    fail("The watchdog must query the reconcile-vps workflow-specific run history.")
if "-X GET" not in watchdog:
    fail("The watchdog must explicitly use GET when passing event/per_page query parameters.")
if "event=schedule" not in watchdog or "MAX_AGE_MINUTES: \"45\"" not in watchdog:
    fail("The watchdog must check scheduled events and fail after 45 minutes without one.")
if "actions: read" not in watchdog or "contents: read" not in watchdog:
    fail("The schedule watchdog must use read-only repository permissions.")
for forbidden in ("contents: write", "packages: write", "pull-requests: write",
                  "platform-kubectl", "scripts/reconcile-vps.sh"):
    if forbidden in watchdog:
        fail(f"The read-only schedule watchdog must not mutate production or request write access: {forbidden}")
if "No scheduled reconcile-vps run is available" not in watchdog:
    fail("The watchdog must fail closed when no scheduled reconcile evidence exists.")


# Production image changes must pass the changed-reference guard in both validation lanes.
image_change_contract = ROOT / "scripts" / "validate-image-change-contract.py"
if not image_change_contract.is_file():
    fail("Changed production image-reference contract script is missing.")
if "validate-image-change-contract.py --self-test" not in manifest_validation:
    fail("Manifest validation must run the immutable image-change contract fixtures.")
if 'validate-image-change-contract.py "$BASE_SHA" "$HEAD_SHA"' not in manifest_validation:
    fail("Manifest validation must inspect changed production image references on pull requests.")
actions_validation = read("validate-github-actions.yml")
if "validate-image-change-contract.py --self-test" not in actions_validation:
    fail("Workflow validation must run immutable image-change contract regression fixtures.")
restart_test = ROOT / "scripts" / "tests" / "restart-blocked-image-pulls.test.sh"
if not restart_test.is_file():
    fail("Permanent image-pull restart regression test is missing.")
if "bash scripts/tests/restart-blocked-image-pulls.test.sh" not in actions_validation:
    fail("Workflow validation must execute permanent/transient image-pull restart regression tests.")

# A merge of the watchdog itself must exercise the read-only API path immediately.
# This push-only smoke mode may warn about stale/missing schedule data, but normal
# scheduled/manual/fallback invocations must continue to fail closed on stale data.
if '  push:\n    branches: [master]\n    paths:\n      - ".github/workflows/reconcile-schedule-watchdog.yml"' not in watchdog:
    fail("The watchdog must run a path-scoped post-merge API smoke check on master.")
if watchdog.count('if [[ "$GITHUB_EVENT_NAME" == "push" ]]; then') != 11:
    fail("Only the watchdog's empty-history, disabled-workflow, queue-delay, stale-history, inspection-result, and recovery-result guards may be warn-only for push smoke runs.")
if '::warning::Read-only API smoke succeeded' not in watchdog:
    fail("The watchdog push smoke must clearly label stale/missing schedule or queue data as a warning, not health success.")
if '::error::No scheduled reconcile-vps run within ${MAX_AGE_MINUTES} minutes.' not in watchdog:
    fail("Scheduled/manual watchdog runs must still fail closed when reconciliation history is stale.")



# The read-only watchdog must distinguish a disabled reconciliation workflow from
# an active workflow whose scheduled run history is stale or missing.
workflow_state_step = watchdog.find("name: Verify reconcile-vps workflow is enabled")
latest_run_step = watchdog.find("name: Inspect latest scheduled reconcile run")
if workflow_state_step < 0 or latest_run_step < 0 or workflow_state_step > latest_run_step:
    fail("The watchdog must verify reconcile-vps is enabled before evaluating schedule freshness.")
if '"repos/${GITHUB_REPOSITORY}/actions/workflows/reconcile-vps.yml"' not in watchdog:
    fail("The watchdog must query reconcile-vps workflow metadata through the Actions API.")
if 'state="$(jq -r \'.state // empty\' <<< "$workflow")"' not in watchdog:
    fail("The watchdog must inspect the workflow enabled state returned by GitHub.")
if 'if [[ "$state" != "active" ]]; then' not in watchdog or "scheduled events cannot be relied on" not in watchdog:
    fail("The watchdog must fail closed with an explicit diagnostic when reconcile-vps is disabled.")
if 'MAX_QUEUE_MINUTES: "15"' not in watchdog or "run_started_at" not in watchdog or "queue_seconds" not in watchdog:
    fail("The watchdog must measure scheduled reconciliation runner queue delay and enforce a 15-minute queue budget.")
reconcile_queue_block = watchdog.split("name: Inspect latest scheduled reconcile run", 1)[1].split(
    "name: Report latest scheduled inspection runner queue delay", 1
)[0]
inspection_queue_block = watchdog.split("name: Report latest scheduled inspection runner queue delay", 1)[1].split(
    "name: Verify scheduled inspection delivery", 1
)[0]
for block, label in ((reconcile_queue_block, "reconciliation"), (inspection_queue_block, "inspection")):
    if "run_attempt" not in block or "if (( run_attempt > 1 )); then" not in block or "not measurable" not in block:
        fail(f"The watchdog must avoid inferring {label} runner queue time from a re-run attempt's original created_at.")
    if "queue_seconds > MAX_QUEUE_MINUTES * 60" not in block:
        fail(f"The watchdog must compare {label} runner queue budgets in exact seconds.")
    if "queue_minutes > MAX_QUEUE_MINUTES" in block:
        fail(f"The watchdog must not truncate {label} runner queue time to whole minutes.")
if "delay_seconds > max_queue_minutes * 60" not in lane_queue:
    fail("Deployment-lane queue validation must compare exact elapsed seconds against its budget.")
if "delay_minutes > max_queue_minutes" in lane_queue:
    fail("Deployment-lane queue validation must not truncate elapsed time to whole minutes.")
if "inspect-vps.yml/runs" not in watchdog or "Report latest scheduled inspection runner queue delay" not in watchdog:
    fail("The watchdog must report inspection runner queue delay to distinguish runner backlog from missing schedule events.")
inspection_queue_step = watchdog.find("name: Report latest scheduled inspection runner queue delay")
if inspection_queue_step < 0 or "if: always()" not in watchdog[inspection_queue_step:]:
    fail("Inspection queue diagnostics must run even when the reconciliation freshness step fails.")
if 'WATCHDOG_REFERENCE_EPOCH:-' not in watchdog or 'actions/runs/${GITHUB_RUN_ID}' not in watchdog[inspection_queue_step:]:
    fail("Inspection queue diagnostics must fetch an API-clock reference when the freshness step exits early.")


# Watchdog freshness and queue calculations must compare timestamps from the
# GitHub Actions API, not the hosted runner wall clock (observed one-hour skew).
if 'actions/runs/${GITHUB_RUN_ID}' not in watchdog:
    fail("The watchdog must fetch its own run metadata as the GitHub API clock reference.")
if "age_seconds=$((reference_epoch - created_epoch))" not in watchdog:
    fail("Scheduled reconciliation freshness must use the GitHub API reference timestamp.")
reconcile_freshness_block = watchdog.split("name: Inspect latest scheduled reconcile run", 1)[1].split(
    "name: Report latest scheduled inspection runner queue delay", 1
)[0]
if "age_seconds > MAX_AGE_MINUTES * 60" not in reconcile_freshness_block:
    fail("Scheduled reconciliation freshness must compare exact elapsed seconds against its budget.")
if "age_minutes > MAX_AGE_MINUTES" in reconcile_freshness_block:
    fail("Scheduled reconciliation freshness must not truncate elapsed time to whole minutes.")
if "WATCHDOG_REFERENCE_EPOCH=$reference_epoch" not in watchdog or "WATCHDOG_REFERENCE_EPOCH" not in watchdog:
    fail("The watchdog must pass its API reference timestamp to inspection queue diagnostics.")
if "date -u +%s" in watchdog:
    fail("The watchdog must not compare GitHub API timestamps with the hosted runner wall clock.")

# Scheduled inspection delivery has its own cadence budget in addition to queue telemetry.
if 'MAX_INSPECTION_AGE_MINUTES: "75"' not in watchdog:
    fail("The watchdog must enforce a 75-minute freshness budget for the 30-minute inspection schedule.")
inspection_freshness_step = watchdog.find("name: Verify scheduled inspection delivery")
if inspection_freshness_step < 0 or "if: always()" not in watchdog[inspection_freshness_step:]:
    fail("Scheduled inspection freshness must be checked even when reconciliation freshness fails.")
inspection_freshness_block = watchdog[inspection_freshness_step:].split("\n      - name:", 1)[0]
for required in (
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/inspect-vps.yml"',
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/inspect-vps.yml/runs"',
    'event=schedule',
    'age_seconds=$((reference_epoch - created_epoch))',
    'age_seconds > MAX_INSPECTION_AGE_MINUTES * 60',
    '::error::No scheduled inspect-vps run within ${MAX_INSPECTION_AGE_MINUTES} minutes.',
    '::warning::Read-only API smoke succeeded; scheduled inspect-vps is stale.',
    'if [[ "$status" != "completed" ]]',
    'if [[ "$conclusion" != "success" ]]',
    '::error::Scheduled inspect-vps run #${run_id} failed with conclusion=${conclusion}.',
    '::warning::Read-only API smoke succeeded; latest scheduled inspect-vps run concluded',
):
    if required not in inspection_freshness_block:
        fail(f"Scheduled inspection freshness contract is missing: {required}")
if "age_minutes > MAX_INSPECTION_AGE_MINUTES" in inspection_freshness_block:
    fail("Scheduled inspection freshness must not truncate elapsed time to whole minutes.")

# Native scheduled inspection evidence and manual fallback activity must never be conflated.
inspection_recovery_step = recovery.find("name: Recover missing inspection delivery")
if inspection_recovery_step < 0:
    fail("Recovery controller must retain its read-only inspection fallback.")
inspection_recovery_block = recovery[inspection_recovery_step:].split("\n      - name:", 1)[0]
for required in (
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/inspect-vps.yml/runs"',
    "-f event=schedule",
    "native_latest=",
    "native_conclusion=",
    "MAX_INSPECTION_AGE_MINUTES * 60 + 1",
    "-f event=workflow_dispatch",
    "fallback_latest=",
    "fallback_conclusion=",
    "Native inspection schedule remains stale",
    "does not satisfy native schedule freshness",
    "dispatching the existing read-only inspection workflow.",
):
    if required not in inspection_recovery_block:
        fail(f"Inspection recovery native/fallback separation contract is missing: {required}")
if 'repos/${GITHUB_REPOSITORY}/actions/runs" -F branch=master' in inspection_recovery_block:
    fail("Inspection recovery must not use an unfiltered all-event run list as native schedule evidence.")
if "event=workflow_dispatch" in inspection_recovery_block.split("fallback_runs=", 1)[0]:
    fail("Manual workflow_dispatch activity must not participate in native inspection freshness.")
if "event=schedule" not in inspection_recovery_block.split("fallback_runs=", 1)[0]:
    fail("Native inspection freshness must query only event=schedule runs.")

# The recovery controller is a separate scheduled safety net and must be monitored too.
if "      - Recover Stale Scheduled Ops" not in watchdog:
    fail("The watchdog must run after native scheduled recovery-controller completions.")
if "github.event.workflow_run.event == 'schedule'" not in watchdog:
    fail("Workflow-run watchdog invocations must only follow native scheduled source workflows.")
if 'MAX_RECOVERY_AGE_MINUTES: "45"' not in watchdog:
    fail("The watchdog must enforce a 45-minute freshness budget for the 15-minute recovery schedule.")
recovery_watchdog_step = watchdog.find("name: Verify scheduled recovery controller delivery and result")
if recovery_watchdog_step < 0 or "if: always()" not in watchdog[recovery_watchdog_step:]:
    fail("Recovery-controller delivery/result verification must run even when another watchdog check fails.")
recovery_watchdog_block = watchdog[recovery_watchdog_step:]
for required in (
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/recover-stale-ops.yml"',
    '"repos/${GITHUB_REPOSITORY}/actions/workflows/recover-stale-ops.yml/runs"',
    "event=schedule",
    "branch=master",
    "MAX_RECOVERY_AGE_MINUTES",
    "age_seconds > MAX_RECOVERY_AGE_MINUTES * 60",
    '[[ "$conclusion" != "success" ]]',
    '::error::Scheduled recovery-controller run #${run_id} failed with conclusion=${conclusion}.',
    '::warning::Read-only API smoke succeeded; latest scheduled recovery-controller run concluded',
):
    if required not in recovery_watchdog_block:
        fail(f"Scheduled recovery-controller watchdog contract is missing: {required}")
if "age_minutes > MAX_RECOVERY_AGE_MINUTES" in recovery_watchdog_block:
    fail("Scheduled recovery freshness must not truncate elapsed time to whole minutes.")


# Canonical Auth release handoff must prove the exact publisher run and pin the registry digest.
auth_digest_verifier = ROOT / "scripts" / "verify-auth-publisher-run.sh"
if not auth_digest_verifier.is_file():
    fail("Auth publisher provenance verifier is missing.")
auth_digest_promoter = ROOT / "scripts" / "promote-auth-image-digest.py"
if not auth_digest_promoter.is_file():
    fail("Auth digest promotion helper is missing.")
auth_verifier_text = auth_digest_verifier.read_text(encoding="utf-8")
for required in (
    'verify_step_success "Verify auth service" "Run npm install --package-lock-only --ignore-scripts --no-audit --no-fund"',
    'verify_step_success "Verify auth service" "Run npm ci --ignore-scripts --no-audit --no-fund"',
    'verify_step_success "Verify auth service" "Run npm test"',
    'verify_step_success "Verify auth service" "Run npm run typecheck"',
    'verify_step_success "Verify auth service" "Run npm run build"',
):
    if required not in auth_verifier_text:
        fail(f"Auth publisher provenance must require successful application verification step: {required}")
auth_verifier_tests = ROOT / "scripts" / "tests" / "verify-auth-publisher-run.test.sh"
if not auth_verifier_tests.is_file():
    fail("Auth publisher provenance regression tests are missing.")
for required in (
    "Run npm install --package-lock-only --ignore-scripts --no-audit --no-fund",
    "Run npm ci --ignore-scripts --no-audit --no-fund",
    "Run npm test",
    "Run npm run typecheck",
    "Run npm run build",
):
    if required not in auth_verifier_tests.read_text(encoding="utf-8"):
        fail(f"Auth publisher provenance tests must cover required verification step: {required}")
for required in (
    "auth-image-published",
    "EVENT_AUTH_DIGEST: ${{ github.event.client_payload.auth_digest }}",
    'SOURCE_WORKFLOW_PATH="$EVENT_SOURCE_WORKFLOW_PATH"',
    '[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/release.yml" ]]',
    '[[ "$SOURCE_EVENT" == "workflow_dispatch" ]]',
    "run: bash scripts/verify-auth-publisher-run.sh",
    "GHCR_EXPECTED_DIGEST",
    "promote-auth-image-digest.py",
):
    if required not in promotion:
        fail(f"Auth immutable digest promotion contract is missing: {required}")
if "bash scripts/tests/verify-auth-publisher-run.test.sh" not in actions_validation:
    fail("Workflow validation must execute Auth publisher provenance regression tests.")
if "python3 scripts/promote-auth-image-digest.py --self-test" not in manifest_validation:
    fail("Manifest validation must execute Auth digest promotion helper regression tests.")
ghcr_reference_validator = ROOT / "scripts" / "validate-ghcr-image-reference.sh"
if "GHCR_EXPECTED_DIGEST" not in ghcr_reference_validator.read_text(encoding="utf-8"):
    fail("GHCR reference validation must support tag-to-digest correlation.")

# Canonical Auth release promotion must independently correlate both immutable
# producer tags (full source SHA and versioned full-SHA tag) to the dispatch digest.
auth_ghcr_validation = promotion.split(
    "name: Validate promoted image in GHCR", 1
)[1].split("name: Update Kustomize image tag or paired digests", 1)[0]
for required in (
    "SOURCE_COMMIT: ${{ steps.input.outputs.source_commit }}",
    '[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ ]]',
    '[[ "$TAG" =~ ^prod-v[0-9]+[.][0-9]+[.][0-9]+-[0-9a-f]{40}$ ]]',
    '"${TAG##*-}" == "$SOURCE_COMMIT"',
    'for immutable_tag in "$SOURCE_COMMIT" "$TAG"; do',
    'GHCR_EXPECTED_DIGEST="$AUTH_DIGEST"',
    'GHCR_IMAGE_REFERENCE="$IMAGE:$immutable_tag"',
    'GHCR_IMAGE_REFERENCE="$IMAGE@$AUTH_DIGEST"',
):
    if required not in auth_ghcr_validation:
        fail(f"Auth receiver must verify both immutable tags against the dispatched digest: {required}")
if auth_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$IMAGE:$immutable_tag"') > auth_ghcr_validation.index('GHCR_IMAGE_REFERENCE="$IMAGE@$AUTH_DIGEST"'):
    fail("Auth full-SHA and versioned tags must be correlated before the digest-only reference is accepted.")

# Auth must be validated from the effective production render, not raw source YAML.
auth_contract = ROOT / "scripts" / "validate-auth-gitops-contract.py"
if not auth_contract.is_file():
    fail("Rendered Auth GitOps contract validator is missing.")
if "python3 scripts/validate-auth-gitops-contract.py --self-test" not in manifest_validation:
    fail("Manifest validation must execute Auth GitOps contract regression tests.")
if "python3 scripts/validate-auth-gitops-contract.py /tmp/platform-infra-rendered.yaml" not in manifest_validation:
    fail("Manifest validation must validate the rendered Auth GitOps resources.")
if manifest_validation.find("name: Render production manifests") > manifest_validation.find("name: Validate rendered Auth GitOps contract"):
    fail("Auth GitOps contract validation must run after production manifests are rendered.")

# The watchdog must inspect downstream deployment-lane jobs, not only the top-level
# workflow run queue. This catches a single VPS runner that stops accepting later lanes.
lane_queue_script = ROOT / "scripts" / "verify-reconcile-lane-queue.py"
if not lane_queue_script.is_file():
    fail("The read-only deployment-lane queue verifier is missing.")
if "python3 scripts/verify-reconcile-lane-queue.py --self-test" not in actions_validation:
    fail("Workflow validation must execute deployment-lane queue regression fixtures.")
lane_queue_step = watchdog.find("name: Verify scheduled reconciliation deployment-lane runner assignment")
if lane_queue_step < 0 or "if: always()" not in watchdog[lane_queue_step:]:
    fail("Deployment-lane queue diagnostics must run even when schedule freshness fails.")
for required in (
    "actions/runs/${run_id}/jobs",
    "MAX_QUEUE_MINUTES",
    "MAX_AGE_MINUTES",
    "WATCHDOG_REFERENCE_EPOCH",
    '--reconcile-created-at "$reconcile_created_at"',
    '--max-reconcile-age-minutes "$MAX_AGE_MINUTES"',
    "verify-reconcile-lane-queue.py",
    "persist-credentials: false",
):
    if required not in watchdog:
        fail(f"Deployment-lane queue watchdog contract is missing: {required}")
lane_queue_contract = lane_queue_script.read_text(encoding="utf-8")
if 'startswith("Deploy lane — ")' not in lane_queue_contract or 'job.get("runner_id")' not in lane_queue_contract:
    fail("The deployment-lane queue verifier must inspect only named deployment lanes without an assigned runner.")
if "stale_reconcile" not in lane_queue_contract or 'status in ("in_progress", "completed") and runner_id > 0' not in lane_queue_contract:
    fail("The deployment-lane queue verifier must avoid re-failing historical assigned delays after the parent reconciliation is stale.")
if "Still-queued unassigned lanes remain actionable." not in lane_queue_contract:
    fail("Stale reconciliation handling must continue enforcing currently unassigned deployment lanes.")

# Optional VPS MCP must remain read-only and subordinate to the sole GitOps apply authority.
vps_mcp_contract = ROOT / "scripts" / "validate-vps-control-mcp-contract.py"
if not vps_mcp_contract.is_file():
    fail("The optional VPS MCP GitOps-only contract validator is missing.")
for required in (
    "python3 scripts/validate-vps-control-mcp-contract.py --self-test",
    "python3 scripts/validate-vps-control-mcp-contract.py",
):
    if required not in manifest_validation:
        fail(f"Manifest validation must execute the VPS MCP deployment-boundary contract: {required}")

print("Workflow contract validation passed.")
