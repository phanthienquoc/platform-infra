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


reconcile = read("reconcile-vps.yml")
promotion = read("gitops-image-promotion.yml")
inspection = read("inspect-vps.yml")
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
if "EVENT_BACKEND_DIGEST" not in promotion or "EVENT_ADMIN_DIGEST" not in promotion:
    fail("StockDividend atomic promotion must consume backend and admin digests.")
if '[[ "$BACKEND_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]' not in promotion:
    fail("StockDividend backend digest must be validated before GHCR access.")
if '[[ "$ADMIN_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]' not in promotion:
    fail("StockDividend admin digest must be validated before GHCR access.")
if "Update Kustomize image tag or paired digests" not in promotion:
    fail("StockDividend/Media digest promotion must update both production image entries atomically.")
if "stockdividend/release" not in promotion or "digest: {digest}" not in promotion:
    fail("StockDividend promotion must pin both images by registry digest, not only mutable tags.")
if "EVENT_COMMIT" not in promotion or "EVENT_BACKEND_DIGEST" not in promotion or "EVENT_ADMIN_DIGEST" not in promotion:
    fail("StockDividend promotion must resolve source commit and both image digests from the dispatch payload.")

# Media Generation publishes one paired digest event and promotion pins both images atomically.
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

# Promotion must validate package-level authorization and the exact immutable tag/digest before GitOps mutation.
if 'TARGET_APP=microfe GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" bash scripts/validate-ghcr-pull-access.sh' not in promotion:
    fail("MicroFE promotion must validate GHCR package pull access before registry login.")
if 'TARGET_APP="$APP" GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" bash scripts/validate-ghcr-pull-access.sh' not in promotion:
    fail("Application promotion must validate GHCR package pull access before registry login.")

# Docker's registry-wide login endpoint can be denied even when scoped package reads work.
# Verify the exact tag/digest directly with a package-scoped Registry V2 bearer token instead.
if "docker login ghcr.io" in promotion or "docker manifest inspect" in promotion:
    fail("Promotion must not depend on registry-wide Docker login for private GHCR reads.")
if 'GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" GHCR_IMAGE_REFERENCE="$image" bash scripts/validate-ghcr-image-reference.sh' not in promotion:
    fail("MicroFE promotion must verify each exact immutable image digest through Registry V2.")
if 'GHCR_USERNAME="$GHCR_USERNAME" GHCR_TOKEN="$GHCR_TOKEN" GHCR_IMAGE_REFERENCE="$IMAGE" bash scripts/validate-ghcr-image-reference.sh' not in promotion:
    fail("Application promotion must verify the exact immutable tag through Registry V2.")
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

# Deployment tracker structural contract: keep all five repositories and action section present.
tracker = (ROOT / "docs" / "cross-repo-deployment-tracker.md").read_text(encoding="utf-8")
if "PLATFORM_INFRA_AUTOMATION_TOKEN" in promotion and "PLATFORM_INFRA_AUTOMATION_TOKEN" not in tracker:
    fail("Tracker must record the automation token required by the promotion workflow.")

if not tracker.startswith("# Cross-Repository Production Deployment Tracker"):
    fail("Cross-repo deployment tracker title is missing.")
if "Last reviewed:" not in tracker or "## Repository readiness" not in tracker or "## Current actions" not in tracker or "## Current runtime blockers" not in tracker:
    fail("Cross-repo deployment tracker must retain its review date, readiness table, current actions, and runtime blockers.")
for repository in (
    "phanthienquoc/platform-infra",
    "phanthienquoc/TCE-dashboard",
    "phanthienquoc/stockdividend",
    "phanthienquoc/media-generation",
    "phanthienquoc/phanthienquoc-authentication",
):
    if repository not in tracker:
        fail(f"Cross-repo deployment tracker is missing repository: {repository}")


# Auth shutdown must be an isolated, allowlisted maintenance operation.
if "rollout-status-v12-scoped-image-pull-restart" not in bootstrap_script:
    fail("Runner bootstrap must publish the versioned scoped image-pull restart policy.")
if '  scale)' not in bootstrap_script or 'scale deployment/microfe-auth deployment/keycloak --replicas=0 -n microfe-platform' not in bootstrap_script:
    fail("Runner bootstrap must allow only the exact Auth/Keycloak scale-to-zero command.")

if "rollout-status-v12-scoped-image-pull-restart" not in reconcile:
    fail("Production reconciliation must require the v12 scoped image-pull restart runner policy.")
auth_provision = read("provision-auth-runtime-secret.yml")
if "rollout-status-v12-scoped-image-pull-restart" not in auth_provision:
    fail("Standalone Auth secret provisioning must accept the current v12 runner policy.")

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
    "stock-prod stock-frontend",
    "media-prod media-generation",
    "media-prod media-generation-frontend",
):
    if required_deployment not in restart_block:
        fail(f"Runner image-pull recovery is missing a production Deployment mapping: {required_deployment}")

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
if "workflow_run:" not in watchdog or "      - inspect-vps" not in watchdog or "      - reconcile-vps" not in watchdog:
    fail("The watchdog must run after scheduled reconciliation and inspection completions as a schedule-delivery fallback.")
if "      - completed" not in watchdog or "github.event.workflow_run.event == 'schedule'" not in watchdog:
    fail("The watchdog fallback must be limited to completed scheduled reconcile-vps/inspect-vps runs.")
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

# A merge of the watchdog itself must exercise the read-only API path immediately.
# This push-only smoke mode may warn about stale/missing schedule data, but normal
# scheduled/manual/fallback invocations must continue to fail closed on stale data.
if '  push:\n    branches: [master]\n    paths:\n      - ".github/workflows/reconcile-schedule-watchdog.yml"' not in watchdog:
    fail("The watchdog must run a path-scoped post-merge API smoke check on master.")
if watchdog.count('if [[ "$GITHUB_EVENT_NAME" == "push" ]]; then') != 3:
    fail("Only the watchdog's empty-history, queue-delay, and stale-history guards may be warn-only for push smoke runs.")
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
if "WATCHDOG_REFERENCE_EPOCH=$reference_epoch" not in watchdog or "WATCHDOG_REFERENCE_EPOCH" not in watchdog:
    fail("The watchdog must pass its API reference timestamp to inspection queue diagnostics.")
if "date -u +%s" in watchdog:
    fail("The watchdog must not compare GitHub API timestamps with the hosted runner wall clock.")

print("Workflow contract validation passed.")
