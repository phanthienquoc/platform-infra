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
scheduled_run_result = (ROOT / "scripts" / "verify-scheduled-run-result.py").read_text(encoding="utf-8")
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

# A manual plan must be strictly read-only. Namespace creation is desired-state drift,
# not a prerequisite that the plan is allowed to satisfy by mutating the cluster.
reconcile_script = (ROOT / "scripts" / "reconcile-vps.sh").read_text(encoding="utf-8")
run_diff_block = reconcile_script.split("run_diff() {", 1)[1].split("\n}\n\ncase", 1)[0]
if re.search(r"(?m)^\s*(?:run_kubectl|sudo).*\b(?:apply|create)\b", run_diff_block):
    fail("reconcile-vps.sh run_diff must not create or apply Kubernetes resources.")
for required in (
    "required_namespaces=(k3s-debug microfe-platform tce-prod)",
    "grep -Eqi 'NotFound|not found'",
    "return 2",
    "Read-only plan reports namespace drift",
):
    if required not in run_diff_block:
        fail(f"Read-only reconcile namespace preflight is missing: {required}")
plan_case = reconcile_script.split("  plan)\n", 1)[1].split("  apply)\n", 1)[0]
if "run_diff" not in plan_case or re.search(r"\b(?:apply|create)\b", plan_case):
    fail("reconcile-vps.sh plan must only perform the read-only diff path.")
apply_case = reconcile_script.split("  apply)\n", 1)[1].split("\n  *)", 1)[0]
if "run_diff" not in apply_case or "run_kubectl apply -k environments/prod" not in apply_case:
    fail("Only explicit reconcile-vps.sh apply may apply the production Kustomize root.")

# The platform runner is self-hosted and reuses its checkout. All reconcile scripts
# below are tracked as non-executable files; invoke them through bash instead of
# chmod'ing the checkout and leaking mode changes into subsequent jobs.
non_executable_scripts = (
    "reconcile-vps.sh",
    "validate-ghcr-pull-access.sh",
    "verify-tce-gitops-release.sh",
    "guard-reconcile-images.sh",
    "publish-microfe-deployment-event.sh",
    "verify-workload-health.sh",
    "verify-tce-gitops-images.sh",
)
for script in non_executable_scripts:
    if f"chmod +x scripts/{script}" in reconcile:
        fail(f"reconcile-vps.yml must not chmod tracked script {script} on the persistent runner.")
    if f"./scripts/{script}" in reconcile:
        fail(f"reconcile-vps.yml must invoke tracked script {script} through bash.")
required_bash_invocations = (
    "bash scripts/reconcile-vps.sh plan",
    "bash scripts/reconcile-vps.sh apply",
    'TARGET_APP=all GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" bash scripts/validate-ghcr-pull-access.sh',
    "bash scripts/verify-tce-gitops-release.sh",
    "bash scripts/guard-reconcile-images.sh check",
    "bash scripts/publish-microfe-deployment-event.sh",
    "bash scripts/verify-workload-health.sh",
    "bash scripts/verify-tce-gitops-images.sh",
)
for invocation in required_bash_invocations:
    if invocation not in reconcile:
        fail(f"reconcile-vps.yml is missing safe bash invocation: {invocation}")
if "Checkout is not clean; refusing to use persistent self-hosted workspace." not in reconcile:
    fail("The primary reconcile job must reject a dirty self-hosted checkout before using it.")
if reconcile.count("name: Verify clean runner worktree") != 4:
    fail("Every application lane checkout must reject pre-existing self-hosted worktree changes.")
if reconcile.count("name: Verify runner worktree remains clean") != 5:
    fail("The reconcile job and all four application lanes must verify their worktrees remain clean.")

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

# Recovery is the independent observer for the schedule watchdog itself. This check is
# warning-only so a missing watchdog never blocks the recovery controller's fallback work.
watchdog_observer_marker = "      - name: Observe schedule watchdog workflow state\n"
if watchdog_observer_marker not in recovery:
    fail("Recovery must observe the schedule watchdog's enabled state.")
watchdog_observer = recovery.split(watchdog_observer_marker, 1)[1].split("\n      - name:", 1)[0]
for required in (
    "actions/workflows/reconcile-schedule-watchdog.yml",
    "state=unavailable",
    '[[ "$state" != "active" ]]',
    "::warning::",
    "continuing recovery",
):
    if required not in watchdog_observer:
        fail(f"Schedule watchdog state observation is incomplete: {required}")
if "exit 1" in watchdog_observer:
    fail("Schedule watchdog state observation must remain warning-only and never block recovery.")
if recovery.find(watchdog_observer_marker) > recovery.find("- name: Resolve GitHub Actions API reference clock"):
    fail("Schedule watchdog state must be observed before reconciliation recovery begins.")

watchdog_recovery_gate = """             (github.event.workflow_run.workflow_id == 402675709 &&
              github.event.workflow_run.event == 'schedule' &&
              github.event.workflow_run.conclusion == 'failure')"""
if watchdog_recovery_gate not in recovery:
    fail("A failed native scheduled freshness watchdog must trigger the existing recovery controller; successful/diagnostic watchdog runs must not.")
if "github.event.workflow_run.run_attempt == 1" not in recovery:
    fail("Recovery must ignore workflow_run rerun attempts; only the original completed run may drive freshness recovery.")
if "github.run_attempt == 1" not in recovery:
    fail("The recovery controller itself must ignore rerun attempts to prevent replay.")

# Native recovery cadence must not be displaced by workflow_run, push, manual or TCE-heartbeat events.
expected_recovery_concurrency = """concurrency:
  group: scheduled-ops-delivery-recovery-${{ github.event_name == 'schedule' && 'schedule' || 'diagnostic' }}
  cancel-in-progress: false
"""
if expected_recovery_concurrency not in recovery:
    fail("Native scheduled recovery must use a concurrency group isolated from non-schedule diagnostics.")

# Keep the sole production apply authority globally serialized across all event types.
expected_reconcile_concurrency = """concurrency:
  group: platform-vps-reconcile
  cancel-in-progress: false
"""
if expected_reconcile_concurrency not in reconcile:
    fail("Production reconcile-vps must retain one cross-event concurrency group to serialize all applies.")
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
watchdog_age_budget = re.search(
    r'(?m)^[ \t]*MAX_WATCHDOG_AGE_MINUTES:[ \t]*"([0-9]+)"',
    watchdog,
)
if watchdog_age_budget is None:
    fail("The schedule watchdog must declare MAX_WATCHDOG_AGE_MINUTES.")
if int(watchdog_age_budget.group(1)) != watchdog_schedule_gap * 3:
    fail("MAX_WATCHDOG_AGE_MINUTES must equal three maximum watchdog schedule intervals.")

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
    "--retry 4 --retry-delay 2 --retry-max-time 45 --max-time 15 --retry-connrefused",
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
if "--retry-all-errors" in recovery:
    fail("TCE heartbeat verification must not retry permanent 4xx/authentication failures.")
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
    "scripts/verify-tce-schedule-delivery.py",
    "scripts/verify-scheduled-run-result.py",
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
if "- scripts/resolve-push-deployment-scope.sh" not in reconcile_push_paths:
    fail("Changes to the push-scope resolver must trigger the sole production reconciliation workflow.")
scope_resolver = (ROOT / "scripts" / "resolve-push-deployment-scope.sh").read_text(encoding="utf-8")
if "assert_scope all scripts/resolve-push-deployment-scope.sh" not in scope_resolver:
    fail("Push-scope resolver changes must resolve to the cluster-wide reconciliation scope.")
for required in (
    "apps/**/*.md|apps/**/docs/*",
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

# The read-only CRI inventory must distinguish a local GHCR cache tag from a
# registry-resolved digest. A local image ID is never promotion evidence.
for required in (
    'echo; echo "### GHCR image digest coverage"',
    'select(any((.repoTags // [])[]?; startswith("ghcr.io/")))',
    'select((.repoDigests // []) | length == 0)',
    "local image IDs are not registry digests or promotion evidence",
):
    if required not in inspection_script:
        fail(f"VPS inspection is missing GHCR cache digest evidence: {required}")
if 'grep -q "^### GHCR image digest coverage$"' not in inspection:
    fail("inspect-vps output validation must require the GHCR digest coverage section.")

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

# Remaining Platform image validators must cover TCE, Auth and MicroFE without retired Stock/Media image lanes.
for required in (
    "tce-dashboard/(web|service)",
    "auth-service/auth",
    "microfe-(auth|shell|ws)",
):
    if required not in manifest_validation:
        fail(f"Manifest validation is missing an active immutable image contract: {required}")

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
if "if: (github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/master') || (github.event_name == 'repository_dispatch' && github.event.action == 'auth-image-published')" not in promotion:
    fail("The Auth application promotion job must allow only manual master promotion or the provenance-bound Auth dispatch.")

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

# The generic promotion receiver is Auth-only; TCE and MicroFE use dedicated jobs.
if promotion.count("          SOURCE_RUN_ATTEMPT: ${{ github.event.client_payload.source_run_attempt }}") != 2:
    fail("TCE and MicroFE promotion jobs must receive the source Actions run attempt.")
if "- auth-image-published" not in promotion:
    fail("GitOps promotion must consume the Auth immutable-digest event.")
if "stockdividend-images-published" in promotion or "media-images-published" in promotion:
    fail("Retired StockDividend/Media publisher events must not be accepted by platform-infra.")
for required in (
    "EVENT_AUTH_DIGEST: ${{ github.event.client_payload.auth_digest }}",
    "EVENT_SOURCE_RUN_ID: ${{ github.event.client_payload.source_run_id }}",
    "EVENT_SOURCE_RUN_ATTEMPT: ${{ github.event.client_payload.source_run_attempt }}",
    "EVENT_SOURCE_WORKFLOW_PATH: ${{ github.event.client_payload.source_workflow_path }}",
    "EVENT_SOURCE_EVENT: ${{ github.event.client_payload.source_event }}",
    "EVENT_SOURCE_HEAD_SHA: ${{ github.event.client_payload.source_head_sha }}",
    '[[ "$APP" == "auth-service" && "$COMPONENT" == "auth" ]]',
    '[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/release.yml" ]]',
    '[[ "$SOURCE_EVENT" == "workflow_dispatch" ]]',
    '[[ "$SOURCE_HEAD_SHA" =~ ^[0-9a-f]{40}$ && "$SOURCE_HEAD_SHA" == "$SOURCE_COMMIT" ]]',
    '[[ "$AUTH_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]',
    "Verify Auth publisher run provenance",
    "bash scripts/verify-auth-publisher-run.sh",
    "python3 scripts/promote-auth-image-digest.py",
    'GHCR_IMAGE_REFERENCE="$IMAGE:$immutable_tag"',
    'GHCR_IMAGE_REFERENCE="$IMAGE@$AUTH_DIGEST"',
    "git show origin/master:platform/auth-service/kustomization.yaml",
    "gitops-promoted-ready",
):
    if required not in promotion:
        fail(f"Auth immutable promotion contract is missing: {required}")
if promotion.index("Verify Auth publisher run provenance") > promotion.index("Validate promoted image in GHCR"):
    fail("Auth source-run provenance must pass before any promoted image is read or GitOps PR is created.")
for required in ("auth_digest:", "source_commit:", "INPUT_AUTH_DIGEST: ${{ inputs.auth_digest }}", "INPUT_SOURCE_COMMIT: ${{ inputs.source_commit }}"):
    if required not in promotion:
        fail(f"Manual Auth promotion must require immutable digest/source inputs: {required}")

# The legacy generic image-published event allowed tag-only Auth handoffs.
# Current in-scope producers use the provenance-bound auth-image-published contract.
if "- image-published" in promotion:
    fail("Generic image-published dispatch is retired; Auth must use auth-image-published with source-run provenance.")
if "if: (github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/master') || (github.event_name == 'repository_dispatch' && github.event.action == 'auth-image-published')" not in promotion:
    fail("Auth promotion job must accept only manual master runs or the provenance-bound auth-image-published event.")
if 'if [[ "$GITHUB_EVENT_NAME" == "repository_dispatch" && "$EVENT_ACTION" != "auth-image-published" ]]; then' not in promotion:
    fail("Auth promotion input resolver must reject every unsupported repository_dispatch event.")
if "only auth-image-published with publisher provenance" not in promotion:
    fail("Auth promotion must fail closed for legacy or unknown dispatch actions.")

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
    "SOURCE_RUN_ATTEMPT",
    "SOURCE_WORKFLOW_PATH",
    "SOURCE_EVENT",
    "SOURCE_HEAD_SHA",
    "SOURCE_COMMIT",
    "repository.full_name",
    "head_repository.full_name",
    "conclusion",
    '[[ "$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$ ]]',
    '[[ "$run_attempt" == "$SOURCE_RUN_ATTEMPT" ]]',
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
microfe_provenance_tests = (ROOT / "scripts" / "tests" / "verify-tce-microfe-publisher-run.test.sh").read_text(encoding="utf-8")
for required in ("SOURCE_RUN_ATTEMPT=1", 'run_attempt:($run_attempt|tonumber)', 'expect_failure "run attempt mismatch"', 'expect_failure "missing run attempt"'):
    if required not in microfe_provenance_tests:
        fail(f"MicroFE publisher provenance tests must cover exact run-attempt binding: {required}")

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
if "needs: promote-tce-digests" not in promotion.split("  coordinate-tce-release:", 1)[1].split("  promote:", 1)[0]:
    fail("TCE release coordinator must wait for the atomic digest promotion job.")
if "WEB_DIGEST_ON_MASTER" not in promotion or "SERVICE_DIGEST_ON_MASTER" not in promotion:
    fail("TCE coordinator must verify both promoted digests on master before reconciliation.")
tce_provenance = (ROOT / "scripts" / "verify-tce-publisher-run.sh").read_text(encoding="utf-8")
for required in (
    "https://api.github.com/repos/phanthienquoc/TCE-dashboard/actions/runs/$SOURCE_RUN_ID",
    '[[ "$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$ ]]',
    '[[ "$run_attempt" == "$SOURCE_RUN_ATTEMPT" ]]',
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

tce_provenance_tests = (ROOT / "scripts" / "tests" / "verify-tce-publisher-run.test.sh").read_text(encoding="utf-8")
for required in (
    'jobs_api_url="$API_URL/jobs?per_page=100"',
    "SOURCE_RUN_ATTEMPT=1",
    'run_attempt:($run_attempt|tonumber)',
    'expect_failure "run attempt mismatch"',
    'expect_failure "missing run attempt"',
    'verify_job_success "Require master for production release"',
    'verify_job_success "Notify Telegram — release started"',
    'verify_job_success "Resolve production image tag"',
    'verify_step_success "Resolve production image tag" "Resolve immutable release tag"',
    'verify_job_success "Build frontend (native ARM64)"',
    'verify_step_success "Build frontend (native ARM64)" "$step"',
    'verify_job_success "Build backend (native ARM64)"',
    'verify_step_success "Build backend (native ARM64)" "$step"',
    'verify_job_success "Publish immutable images and promote platform-infra"',
    'verify_step_success "Publish immutable images and promote platform-infra" "$step"',
    '"Verify frontend architecture"',
    '"Verify backend architecture"',
    '"Verify immutable registry digests and ARM64 manifests"',
    '"Notify platform-infra"',
    '"Verify platform-infra release workflow"',
):
    if required not in tce_provenance:
        fail(f"TCE source-run verifier must validate required publisher job/step: {required}")
for required in (
    'Build frontend (native ARM64)',
    'Build backend (native ARM64)',
    'Publish immutable images and promote platform-infra',
    'Resolve immutable release tag',
    'Build frontend image',
    'Verify frontend architecture',
    'Build backend image',
    'Verify backend architecture',
    'Verify immutable registry digests and ARM64 manifests',
    'Notify platform-infra',
    'Verify platform-infra release workflow',
    'missing backend build job',
    'duplicate publisher job',
    'skipped required publisher step',
):
    if required not in tce_provenance_tests:
        fail(f"TCE provenance regression tests must cover publisher job/step evidence: {required}")
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
if 'TARGET_APP=all GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" bash scripts/validate-ghcr-pull-access.sh' not in ghcr_preflight_block:
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
if "pv|pvc" not in bootstrap_allowlist or "storageclasses" not in bootstrap_allowlist or "all|nodes" not in bootstrap_allowlist:
    fail("The read-only platform-kubectl allowlist must permit all/PVC/PV/StorageClass inventory queries.")

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
if (
    'for immutable_tag in "$SOURCE_COMMIT" "$TAG"; do' not in promotion
    or 'GHCR_EXPECTED_DIGEST="$AUTH_DIGEST" GHCR_IMAGE_REFERENCE="$IMAGE:$immutable_tag" bash scripts/validate-ghcr-image-reference.sh' not in promotion
    or 'GHCR_IMAGE_REFERENCE="$IMAGE@$AUTH_DIGEST" bash scripts/validate-ghcr-image-reference.sh' not in promotion
):
    fail("Application promotion must verify both full-SHA/release tags against the attested digest and verify the immutable digest through Registry V2.")

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
for namespace in ("microfe-platform", "tce-prod"):
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
if "rollout-status-v15-core-workloads" not in bootstrap_script:
    fail("Runner bootstrap must publish the versioned scoped image-pull restart policy.")
if '  scale)' not in bootstrap_script or 'scale deployment/microfe-auth deployment/keycloak --replicas=0 -n microfe-platform' not in bootstrap_script:
    fail("Runner bootstrap must allow only the exact Auth/Keycloak scale-to-zero command.")

if "rollout-status-v15-core-workloads" not in reconcile:
    fail("Production reconciliation must require the current v15 core-workload runner policy.")

# Keep operator-facing diagnostics aligned with the enforced runner policy version.
for required in (
    "Runner policy v15 (core platform workloads) is ready.",
    "Waiting for runner bootstrap policy v15",
    "Runner policy is not updated to core-workload v15",
):
    if required not in reconcile:
        fail(f"Reconciliation diagnostics are missing the current v14 policy label: {required}")
if "runner bootstrap policy v13" in reconcile or "image-pull restart v13" in reconcile:
    fail("Reconciliation diagnostics must not report the retired v13 runner policy after v15 is required.")
auth_provision = read("provision-auth-runtime-secret.yml")
if "rollout-status-v15-core-workloads" not in auth_provision:
    fail("Standalone Auth secret provisioning must accept the current v15 runner policy.")

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
    "microfe)","auth-service)","tce-dashboard)","all)",
):
    if required_target not in restart_block:
        fail(f"Runner image-pull recovery is missing an explicit target mapping: {required_target}")
for required_deployment in (
    "microfe-platform microfe-shell",
    "microfe-platform microfe-ws",
    "microfe-platform microfe-auth",
    "tce-prod tce-service",
    "tce-prod tce-frontend",
):
    if required_deployment not in restart_block:
        fail(f"Runner image-pull recovery is missing a production Deployment mapping: {required_deployment}")

# Retired app trees and runtime contracts must be absent from the production GitOps surface.
for retired_path in ("apps/stockdividend", "apps/media-generation"):
    if (ROOT / retired_path).exists():
        fail(f"Retired production manifest tree must be absent: {retired_path}")
production_root = (ROOT / "environments" / "prod" / "kustomization.yaml").read_text(encoding="utf-8")
certificates = (ROOT / "platform" / "cert-manager" / "certificates.yaml").read_text(encoding="utf-8")
auth_service_config = (ROOT / "platform" / "auth-service" / "configmap.yaml").read_text(encoding="utf-8")
network_boundaries = (ROOT / "scripts" / "validate-network-boundaries.sh").read_text(encoding="utf-8")
if "Expected exactly 2 production Ingress resources" not in network_boundaries:
    fail("Network-boundary validation must expect only the remaining TCE and MicroFE Ingress resources.")
for retired_host in ("mrcute.space", "www.mrcute.space", "admin.mrcute.space", "api.mrcute.space", "media.mrcute.space"):
    if f"\n{retired_host}\n" in network_boundaries:
        fail(f"Retired Stock/Media hostname remains allowed in production network validation: {retired_host}")
for retired_reference in ("stock-prod", "media-prod", "stockdividend", "media-generation"):
    if retired_reference in production_root or retired_reference in certificates or retired_reference in auth_service_config:
        fail(f"Retired app reference remains in active production manifests: {retired_reference}")

# Namespace deletion is a separate manual-only, storage-gated operation.
decommission_workflow = read("decommission-stock-media.yml")
decommission_script = (ROOT / "scripts" / "decommission-stock-media-namespaces.sh").read_text(encoding="utf-8")
decommission_wrapper = bootstrap_script
for required in (
    "workflow_dispatch:",
    "mode:",
    "default: plan",
    "options:",
    "validate_mode:",
    "permissions: {}",
    "inputs.mode == 'plan'",
    "inputs.mode == 'delete'",
    "Report dedicated Media runner state",
    "Run fresh read-only storage preflight",
    "Delete only the two approved namespaces",
    "DELETE-STOCK-PROD-AND-MEDIA-PROD",
    "BACKUP-AND-EXTERNAL-DATA-REVIEWED",
    "dns_ownership_review:",
    "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED",
    "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED",
    "environment: production",
):
    if required not in decommission_workflow:
        fail(f"Guarded namespace decommission workflow is missing: {required}")
if "push:" in decommission_workflow or "schedule:" in decommission_workflow or "repository_dispatch:" in decommission_workflow:
    fail("Namespace decommission must remain manual-only.")

plan_job_start = decommission_workflow.find("  plan:")
delete_job_start = decommission_workflow.find("  decommission:")
if not (0 <= plan_job_start < delete_job_start):
    fail("Read-only plan job must be separate from the destructive decommission job.")
plan_job = decommission_workflow[plan_job_start:delete_job_start]
delete_job = decommission_workflow[delete_job_start:]
if "bash scripts/decommission-stock-media-namespaces.sh plan" not in plan_job:
    fail("Plan mode must run the read-only namespace/storage preflight.")
if "bash scripts/decommission-stock-media-namespaces.sh delete" in plan_job:
    fail("Plan mode must never invoke namespace deletion.")
if "DELETE-STOCK-PROD-AND-MEDIA-PROD" in plan_job or "BACKUP-AND-EXTERNAL-DATA-REVIEWED" in plan_job or "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED" in plan_job or "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED" in plan_job:
    fail("Read-only plan mode must not require destructive operator attestations.")
if "environment: production" in plan_job:
    fail("Read-only plan mode must not request the production deployment environment.")
for required in (
    "Validate exact deletion confirmations",
    "DNS_OWNERSHIP_REVIEW",
    "Verify dedicated Media runner is retired in GitHub and on the VPS",
    "MEDIA_RUNNER_AUDIT_TOKEN: ${{ secrets.MEDIA_RUNNER_AUDIT_TOKEN }}",
    "run: bash scripts/verify-media-runner-retired.sh",
    "Run fresh read-only storage preflight",
    "Delete only the two approved namespaces",
    "run: bash scripts/decommission-stock-media-namespaces.sh delete",
    "environment: production",
):
    if required not in delete_job:
        fail(f"Destructive decommission job is missing: {required}")
runner_guard_step = delete_job.find("name: Verify dedicated Media runner is retired in GitHub and on the VPS")
storage_preflight_step = delete_job.find("name: Run fresh read-only storage preflight")
namespace_delete_step = delete_job.find("name: Delete only the two approved namespaces")
if not (0 <= runner_guard_step < storage_preflight_step < namespace_delete_step):
    fail("Dedicated Media runner state must be checked before destructive storage preflight and namespace deletion.")
delete_step = delete_job[namespace_delete_step:]
if "RUNNER_RETIREMENT: ${{ inputs.runner_retirement }}" not in delete_step:
    fail("The validated Media runner retirement attestation must reach the final namespace delete script.")
runner_guard_script = (ROOT / "scripts" / "verify-media-runner-retired.sh").read_text(encoding="utf-8")
for required in (
    "actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service",
    "systemctl is-active",
    "systemctl is-enabled",
    "disabled|masked|masked-runtime|not-found",
    "Runner.Listener",
    "pgrep -f",
    "MEDIA_RUNNER_AUDIT_TOKEN",
    "phanthienquoc/media-generation",
    "media-generation-k3s-01",
    "curl --fail --silent --show-error --config -",
    "page_count",
    "select(.name == $runner)",
    "refusing namespace deletion",
):
    if required not in runner_guard_script:
        fail(f"Dedicated Media runner retirement guard is missing: {required}")
for required in (
    "inventory-namespace",
    "get all -n",
    "get ingress -n",
    "Ingress hosts/TLS secret references",
    "DNS ownership is not inferred",
    "get pvc -n",
    "get pv -o json",
    "get storageclasses -o wide",
    "PVC inventory is not empty",
    "PV claims remain",
    "VolumeSnapshot references remain",
    "volumesnapshotcontent",
    "volumesnapshot|volumesnapshotcontent",
    "decommission-stock-media",
    "DNS_OWNERSHIP_REVIEW",
    "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED",
    "RUNNER_RETIREMENT",
    "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED",
):
    if required not in decommission_script:
        fail(f"Namespace decommission preflight is missing: {required}")
for required in (
    'KUBECTL_SUDO="${PLATFORM_KUBECTL_SUDO:-sudo}"',
    'KUBECTL=("$KUBECTL_SUDO" "$KUBECTL_BIN")',
):
    if required not in decommission_script:
        fail(f"Namespace decommission preflight must run the root-owned wrapper through sudo: {required}")
for required in (
    "decommission-stock-media)",
    "DELETE-STOCK-PROD-AND-MEDIA-PROD",
    "BACKUP-AND-EXTERNAL-DATA-REVIEWED",
    "dns_review",
    "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED",
    "runner_retirement",
    "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED",
    "PVCs remain",
    "PV claims remain",
    "namespace_storage_snapshot_refs()",
    'namespace_storage_snapshot_refs "$namespace"',
    "volumesnapshots.snapshot.storage.k8s.io",
    "volumesnapshotcontents.snapshot.storage.k8s.io",
    "VolumeSnapshot references remain",
    "delete namespace stock-prod media-prod",
):
    if required not in decommission_wrapper:
        fail(f"Root-owned namespace decommission guard is missing: {required}")
inspect_script = (ROOT / "scripts" / "inspect-vps.sh").read_text(encoding="utf-8")
for required in ("Stock/Media VolumeSnapshot references (names only)", 'inventory-namespace "$namespace"', "volumesnapshot|volumesnapshotcontent"):
    if required not in inspect_script:
        fail(f"VPS inspection must expose decommission snapshot references: {required}")
decommission_test = (ROOT / "scripts" / "tests" / "decommission-stock-media-namespaces.test.sh").read_text(encoding="utf-8")
for required in ("MOCK_SNAPSHOT", "MOCK_SNAPSHOT_CONTENT", "namespaced VolumeSnapshot", "cluster-scoped VolumeSnapshotContent", "DNS_OWNERSHIP_REVIEW", "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED", "RUNNER_RETIREMENT", "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED", "missing Media runner retirement attestation", "invalid Media runner retirement attestation"):
    if required not in decommission_test:
        fail(f"Decommission storage regression tests must cover snapshot references: {required}")
for required in ("fake_sudo", "PLATFORM_KUBECTL_SUDO", "SUDO_LOG", "Verified default decommission preflight invokes the root-owned wrapper through sudo."):
    if required not in decommission_test:
        fail(f"Decommission regression tests must cover privileged wrapper invocation: {required}")
snapshot_test = ROOT / "scripts" / "tests" / "namespace-storage-snapshot-refs.test.sh"
if not snapshot_test.is_file():
    fail("Namespace storage snapshot regression test is missing.")
if "scripts/tests/namespace-storage-snapshot-refs.test.sh" not in github_actions:
    fail("Namespace storage snapshot regression test must run in validate-github-actions.")
if "scripts/tests/decommission-stock-media-namespaces.test.sh" not in github_actions:
    fail("Namespace decommission safety regression tests must run in validate-github-actions.")
if "scripts/tests/verify-media-runner-retired.test.sh" not in github_actions:
    fail("Media runner retirement guard regression tests must run in validate-github-actions.")
if "Reject retired StockDividend and Media production manifests" not in read("validate-manifests.yml"):
    fail("Manifest validation must reject reintroduced StockDividend/Media production trees.")

runner_bootstrap = read("bootstrap-runner.yml")
runner_token_mask = runner_bootstrap.find('echo "::add-mask::$token"')
runner_token_output = runner_bootstrap.find('printf \'token=%s\\n\' "$token" >> "$GITHUB_OUTPUT"')
if runner_token_mask < 0 or runner_token_output < 0 or runner_token_mask > runner_token_output:
    fail("Short-lived runner registration token must be masked before it is written to GITHUB_OUTPUT.")
if "bootstrap-media-runner.sh" in runner_bootstrap:
    fail("Shared Platform runner bootstrap must not provision the retired dedicated Media runner.")
bootstrap_verification_parts = runner_bootstrap.split(
    "name: Verify runner service and read-only cluster access", 1
)
if len(bootstrap_verification_parts) != 2:
    fail("Runner bootstrap must retain its read-only runner/cluster verification step.")
bootstrap_verification = bootstrap_verification_parts[1]
for forbidden in (
    "platform-kubectl apply",
    "kubectl create namespace",
    "kubectl apply -f -",
    "platform-kubectl diff -k",
):
    if forbidden in bootstrap_verification:
        fail(f"Runner bootstrap must not mutate or reconcile production Kubernetes resources: {forbidden}")
if "reconcile-vps.yml is the sole production apply authority" not in bootstrap_verification:
    fail("Runner bootstrap must explicitly defer all production manifest changes to reconcile-vps.yml.")
for retired_helper in (
    "bootstrap-media-runner.sh",
    "verify-media-publisher-run.sh",
    "verify-stockdividend-publisher-run.sh",
    "verify-stockdividend-gitops-digests.py",
):
    if (ROOT / "scripts" / retired_helper).exists():
        fail(f"Retired Stock/Media helper must be removed: {retired_helper}")
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
    "platform/keycloak/*",
    "environments/prod/*",
):
    if path_contract not in push_scope_contract:
        fail(f"Push deployment scope resolver is missing path mapping: {path_contract}")
if "apps/stockdividend/*|apps/media-generation/*" not in push_scope_contract:
    fail("Retired app manifest paths must trigger cluster-wide decommission reconciliation.")
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
watchdog_concurrency = watchdog.split("concurrency:", 1)[1].split("\njobs:", 1)[0]
if "group: reconcile-schedule-freshness-watchdog-${{ github.event_name }}" not in watchdog_concurrency:
    fail("The watchdog must isolate native schedule enforcement from workflow_run/push/manual diagnostics so event-driven runs cannot replace a pending scheduled run.")
if "cancel-in-progress: false" not in watchdog_concurrency:
    fail("The watchdog must not cancel an in-progress run when another event of the same class arrives.")
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
if "bash scripts/tests/reconcile-vps.test.sh" not in actions_validation:
    fail("Workflow validation must execute the read-only plan/single-apply regression test.")
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
if watchdog.count('if [[ "$GITHUB_EVENT_NAME" == "push" ]]; then') != 12:
    fail("Only the watchdog's empty-history, disabled-workflow, queue-delay, stale-history, inspection-result, recovery-result, and native schedule-history API guards may be warn-only for push smoke runs.")
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

for required in (
    'python3 scripts/verify-scheduled-run-result.py',
    '--event "$GITHUB_EVENT_NAME"',
    '--run-id "$run_id"',
    '--run-url "$run_url"',
):
    if required not in reconcile_freshness_block:
        fail(f"Scheduled reconciliation result gate is missing: {required}")
for required in (
    'if status not in {"queued", "waiting", "requested", "pending", "in_progress", "completed"}:',
    '"unknown run status fails closed"',
    'if status != "completed":',
    'if conclusion == "success":',
    'if event == "push":',
    'return 1',
    '"failed scheduled run"',
    '"cancelled manual run"',
):
    if required not in scheduled_run_result:
        fail(f"Scheduled reconciliation result verifier is missing: {required}")
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


# Platform independently observes TCE's native WF-06 schedule delivery.
# This is advisory only: TCE schedule failure must not trigger a production reconcile loop.
tce_schedule_verifier = ROOT / "scripts" / "verify-tce-schedule-delivery.py"
if not tce_schedule_verifier.is_file():
    fail("The cross-repo TCE native schedule verifier is missing.")
tce_schedule_verifier_text = tce_schedule_verifier.read_text(encoding="utf-8")
if "python3 scripts/verify-tce-schedule-delivery.py --self-test" not in github_actions:
    fail("Workflow validation must execute TCE native schedule delivery regression fixtures.")
if 'MAX_TCE_WF06_AGE_MINUTES: "25"' not in watchdog:
    fail("The Platform watchdog must use the same 25-minute native WF-06 freshness budget as TCE WF-12.")
tce_schedule_step = watchdog.find("name: Observe native TCE WF-06 schedule delivery")
if tce_schedule_step < 0 or "if: always()" not in watchdog[tce_schedule_step:]:
    fail("The Platform watchdog must observe TCE native schedule delivery even when another diagnostic fails.")
tce_schedule_block = watchdog[tce_schedule_step:].split("\n      - name:", 1)[0]
for required in (
    'TCE_API_BASE="https://api.github.com/repos/phanthienquoc/TCE-dashboard/actions/workflows"',
    'tce_runs_url="${TCE_API_BASE}/wf-06-tce-healthcheck.yml/runs?event=schedule&per_page=10"',
    '--http-status "$api_status"',
    '--reference-epoch "${reference_epoch:-0}"',
    '--max-age-minutes "$MAX_TCE_WF06_AGE_MINUTES"',
    "--warn-only",
):
    if required not in tce_schedule_block:
        fail(f"Platform TCE schedule observation is missing: {required}")
for required in (
    'run.get("event") != "schedule"',
    'run.get("path") != EXPECTED_PATH',
    'run.get("head_branch") != EXPECTED_BRANCH',
    'if attempt != 1:',
    'FULL_SHA.fullmatch(head_sha)',
    'age_seconds > max_age_minutes * 60',
    'latest native WF-06 schedule run is newer than the watchdog API reference clock',
):
    if required not in tce_schedule_verifier_text:
        fail(f"TCE schedule verifier is missing its native-event safety check: {required}")
if "it does not assert public endpoint health" not in tce_schedule_verifier_text:
    fail("TCE schedule delivery must remain separate from public endpoint health.")


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
    '[[ "$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$ ]]',
    '[[ "$run_attempt" == "$SOURCE_RUN_ATTEMPT" ]]',
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
    "SOURCE_RUN_ATTEMPT=1",
    'run_attempt:($run_attempt|tonumber)',
    'expect_failure "run attempt mismatch"',
    'expect_failure "missing run attempt"',
):
    if required not in auth_verifier_tests.read_text(encoding="utf-8"):
        fail(f"Auth publisher provenance tests must cover required verification step: {required}")
for required in (
    "auth-image-published",
    "EVENT_SOURCE_RUN_ATTEMPT: ${{ github.event.client_payload.source_run_attempt }}",
    "SOURCE_RUN_ATTEMPT: ${{ steps.input.outputs.source_run_attempt }}",
    "EVENT_AUTH_DIGEST: ${{ github.event.client_payload.auth_digest }}",
    'SOURCE_WORKFLOW_PATH="$EVENT_SOURCE_WORKFLOW_PATH"',
    'SOURCE_RUN_ATTEMPT="$EVENT_SOURCE_RUN_ATTEMPT"',
    '[[ "$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$ ]]',
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
)[1].split("name: Update Auth Kustomize image digest", 1)[0]
for required in (
    "SOURCE_COMMIT: ${{ steps.input.outputs.source_commit }}",
    '[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ ]]',
    '[[ "$TAG" =~ ^prod-v[0-9]+[.][0-9]+[.][0-9]+-[0-9a-f]{40}$ && "${TAG##*-}" == "$SOURCE_COMMIT" ]]',
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

# Native schedule delivery must detect long gaps between consecutive original schedule events,
# even when a delayed latest run makes the ordinary age check look fresh.
# Native schedule delivery must detect long gaps between consecutive original schedule events,
# even when a delayed latest run makes the ordinary age check look fresh.
native_schedule_gap_script = ROOT / "scripts" / "verify-native-schedule-gap.py"
if not native_schedule_gap_script.is_file():
    fail("The native schedule inter-arrival verifier is missing.")
if "python3 scripts/verify-native-schedule-gap.py --self-test" not in actions_validation:
    fail("Workflow validation must execute native schedule inter-arrival regression fixtures.")
native_schedule_gap_step = watchdog.find("name: Verify native schedule inter-arrival gaps")
if native_schedule_gap_step < 0 or "if: always()" not in watchdog[native_schedule_gap_step:]:
    fail("Native schedule inter-arrival diagnostics must run even when freshness checks fail.")
native_schedule_gap_block = watchdog[native_schedule_gap_step:]
for required in (
    'verify_platform_schedule_gap reconcile-vps.yml "$MAX_AGE_MINUTES"',
    'verify_platform_schedule_gap inspect-vps.yml "$MAX_INSPECTION_AGE_MINUTES"',
    'verify_platform_schedule_gap recover-stale-ops.yml "$MAX_RECOVERY_AGE_MINUTES"',
    'verify_platform_schedule_gap reconcile-schedule-watchdog.yml "$MAX_WATCHDOG_AGE_MINUTES"',
    '--workflow-path ".github/workflows/wf-06-tce-healthcheck.yml"',
    '--max-gap-minutes "$MAX_TCE_WF06_AGE_MINUTES"',
    '--workflow-path ".github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml"',
    '--max-gap-minutes "$MAX_TCE_WF12_GAP_MINUTES"',
    'per_page=100',
):
    if required not in watchdog:
        fail(f"Native schedule inter-arrival watchdog contract is missing: {required}")
tce_wf06_gap_observer = native_schedule_gap_block.split('tce_runs_file="$RUNNER_TEMP/tce-wf06-scheduled-runs.json"', 1)[1]
if '--workflow-path ".github/workflows/wf-06-tce-healthcheck.yml"' not in tce_wf06_gap_observer or "--warn-only" not in tce_wf06_gap_observer:
    fail("TCE WF-06 schedule inter-arrival observation must remain warning-only for Platform.")
tce_wf12_gap_observer = native_schedule_gap_block.split('tce_wf12_runs_file="$RUNNER_TEMP/tce-wf12-scheduled-runs.json"', 1)[1]
if '--workflow-path ".github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml"' not in tce_wf12_gap_observer or "--warn-only" not in tce_wf12_gap_observer:
    fail("TCE WF-12 schedule inter-arrival observation must remain warning-only for Platform.")

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

# A production-capable GitOps-ready event must be tied to a completed successful
# Platform promotion run on master, not merely to a caller-supplied event payload.
reconcile_permissions = reconcile.split("permissions:\n", 1)[1].split("\n\nconcurrency:", 1)[0]
if reconcile_permissions != "  actions: read\n  contents: read":
    fail("reconcile-vps must grant only Actions read plus Contents read for promotion-run verification.")
promotion_guard = "      - name: Validate GitOps promotion dispatch provenance\n"
promotion_guard_index = reconcile.find(promotion_guard)
scope_step_index = reconcile.find("      - name: Resolve push deployment scope\n")
if promotion_guard_index < 0 or scope_step_index <= promotion_guard_index:
    fail("GitOps-ready dispatch provenance must be checked before deployment scope or production preflight.")
for required in (
    "PROMOTION_RUN_ID: ${{ github.event.client_payload.promotion_run_id }}",
    "actions/runs/${PROMOTION_RUN_ID}",
    "actions/runs/${PROMOTION_RUN_ID}/jobs?per_page=100",
    "python3 scripts/verify-gitops-ready-dispatch.py",
    "--event \"$GITHUB_EVENT_PATH\"",
    "--promotion-run \"$RUNNER_TEMP/gitops-promotion-run.json\"",
    "--promotion-jobs \"$RUNNER_TEMP/gitops-promotion-jobs.json\"",
    "deadline=$((SECONDS + 180))",
):
    if required not in reconcile:
        fail(f"reconcile-vps is missing the GitOps promotion-run verification contract: {required}")
if "jq -r '.total_count // empty' <<< \"$jobs_json\"" not in reconcile:
    fail("reconcile-vps must read the Actions jobs total_count before trusting promotion job evidence.")
if "jq -r 'if (.jobs | type) == \"array\" then (.jobs | length) else -1 end' <<< \"$jobs_json\"" not in reconcile:
    fail("reconcile-vps must require a valid Actions jobs array.")
if '"$total_jobs" != "$returned_jobs"' not in reconcile:
    fail("reconcile-vps must reject truncated or incomplete Actions job evidence.")

dispatch_blocks = (
    promotion.split("      - name: Trigger shared VPS reconciliation\n", 1)[1].split("\n\n  promote-tce-digests:", 1)[0],
    promotion.split("      - name: Wait for paired GitOps release\n", 1)[1].split("\n\n\n  promote:", 1)[0],
    promotion.split("      - name: Trigger VPS reconciliation\n", 1)[1].split("\n# yamllint enable", 1)[0],
)
for index, block in enumerate(dispatch_blocks, start=1):
    for field in ("source_commit", "promotion_run_id", "promotion_run_attempt", "promotion_workflow_path", "promotion_head_sha"):
        if field not in block:
            fail(f"GitOps-ready producer {index} is missing dispatch field {field}.")
dispatch_validator = (ROOT / "scripts" / "verify-gitops-ready-dispatch.py").read_text(encoding="utf-8")
for required in (
    "PAYLOAD_KEYS",
    "promotion_workflow_path",
    "promotion_head_sha",
    "Retired or unsupported GitOps-ready application",
    "promotion_run.get(\"conclusion\") == \"success\"",
    "promotion_run.get(\"head_branch\") == \"master\"",
    "Promote MicroFE image digests as one GitOps change",
    "Promote TCE web/service digests atomically",
    "Coordinate TCE release",
    "Promote auth-service /",
):
    if required not in dispatch_validator:
        fail(f"GitOps-ready dispatch validator is missing required fail-closed check: {required}")
if "python3 scripts/verify-gitops-ready-dispatch.py --self-test" not in github_actions:
    fail("GitHub Actions validation must run the GitOps-ready dispatch positive/negative regression tests.")
if '"!scripts/verify-gitops-ready-dispatch.py"' not in recovery_push_paths:
    fail("The read-only GitOps-ready dispatch validator must not trigger production recovery on push.")


image_ref_guard = "      - name: Verify GitOps-ready release tags against current pinned digests\n"
image_ref_guard_index = reconcile.find(image_ref_guard)
secret_provision_index = reconcile.find("      - name: Provision Auth runtime Secret from platform-infra Environment\n")
if image_ref_guard_index < 0 or secret_provision_index <= image_ref_guard_index:
    fail("GitOps-ready tag-to-digest verification must run before any runtime Secret or pull-credential mutation.")
for required in (
    "python3 scripts/verify-gitops-ready-image-refs.py",
    "--source-commit \"$SOURCE_COMMIT\"",
    "GHCR_EXPECTED_DIGEST=\"$digest\"",
    "bash scripts/validate-ghcr-image-reference.sh",
):
    if required not in reconcile:
        fail(f"reconcile-vps is missing the GitOps-ready manifest/tag digest binding: {required}")
image_ref_validator = (ROOT / "scripts" / "verify-gitops-ready-image-refs.py").read_text(encoding="utf-8")
for required in (
    "parse_image_entries",
    'line == "images:"',
    "root-level images section",
    "Only direct image entries and supported image fields are allowed under images",
    "GitOps image set does not exactly match the allowlist",
    "must resolve to the allowlisted repository",
):
    if required not in image_ref_validator:
        fail(f"GitOps-ready image-ref validator is missing fail-closed rule: {required}")
if "python3 scripts/verify-gitops-ready-image-refs.py --self-test" not in github_actions:
    fail("GitHub Actions validation must run GitOps-ready image-ref regression tests.")
if '"!scripts/verify-gitops-ready-image-refs.py"' not in recovery_push_paths:
    fail("The read-only GitOps-ready image-ref validator must not trigger production recovery on push.")

print("Workflow contract validation passed.")
