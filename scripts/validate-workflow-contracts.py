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

# Manual production promotion must originate from master; non-master dispatches fail visibly.
if "if: github.event_name == 'workflow_dispatch' && github.ref != 'refs/heads/master'" not in promotion:
    fail("Manual GitOps promotion must fail closed when dispatched from a non-master ref.")
if "github.event_name != 'workflow_dispatch' || github.ref == 'refs/heads/master'" not in promotion:
    fail("The application promotion job must only run manual promotions from master.")

# Promotion PR auto-merge must fail closed without required checks and pin the exact verified head.
if promotion.count("No required") < 2 or promotion.count("refusing to merge") < 2:
    fail("Both promotion PR merge paths must refuse to merge when no required checks are configured.")
if promotion.count("current_required_count") < 4:
    fail("Both promotion PR check-polling loops must fail closed if required checks disappear or cannot be queried.")
if "No required promotion PR checks are configured.\n" in promotion or "No required PR checks are configured; continuing to merge gate." in promotion:
    fail("Promotion PR checks must not treat an empty required-check list as success.")
if promotion.count("gh pr view \"$PR_NUMBER\" --repo") < 4 or promotion.count("--json headRefOid --jq '.headRefOid'") < 4:
    fail("Both promotion paths must capture and re-check the promotion PR head SHA.")
if promotion.count("steps.validate-pr-checks.outputs.head_sha") < 2 or promotion.count('--match-head-commit "$HEAD_SHA"') < 2:
    fail("Both promotion merges must be pinned to the exact PR head that passed checks.")
if 'gh pr update-branch "$PR_NUMBER"' in promotion:
    fail("Promotion must not update a PR branch after checks and then merge without revalidation.")

# Promotion PR workflows must run under a credential that triggers PR checks; GITHUB_TOKEN can suppress them.
if promotion.count("token: ${{ secrets.PLATFORM_INFRA_AUTOMATION_TOKEN }}") < 2:
    fail("Both promotion PR creation paths must use PLATFORM_INFRA_AUTOMATION_TOKEN so required PR checks can run.")
if promotion.count("GH_TOKEN: ${{ secrets.PLATFORM_INFRA_AUTOMATION_TOKEN }}") < 4:
    fail("Both promotion paths must use PLATFORM_INFRA_AUTOMATION_TOKEN to read required checks and merge the verified head.")
if promotion.count("name: Require GitOps PR automation token") < 2:
    fail("Both promotion paths must fail clearly before PR creation when PLATFORM_INFRA_AUTOMATION_TOKEN is missing.")
if "checks: read" not in promotion or "statuses: read" not in promotion:
    fail("Promotion workflow must have read access to GitHub check runs and commit statuses.")
credentials = (ROOT / "docs" / "credentials-key.md").read_text(encoding="utf-8")
if "`PLATFORM_INFRA_AUTOMATION_TOKEN`" not in credentials:
    fail("credentials-key.md must document PLATFORM_INFRA_AUTOMATION_TOKEN and its required permissions.")

# MicroFE digest promotions must use the shared GitOps promotion workflow.
if "microfe-images-published" not in promotion:
    fail("gitops-image-promotion.yml must consume microfe-images-published.")
if "RELEASE_INPUT: ${{ github.event.client_payload.release }}" not in promotion:
    fail("MicroFE promotion must require a release label correlated with the source commit.")
if '[[ "$RELEASE_INPUT" == "$EXPECTED_RELEASE" ]]' not in promotion:
    fail("MicroFE release label must be checked against the full source commit SHA.")
if "github.event.client_payload.release || github.event.client_payload.commit" not in promotion:
    fail("Promotion run name must expose the correlated MicroFE release label.")
for field in ("auth_digest", "shell_digest", "ws_digest"):
    if field not in promotion:
        fail(f"Shared MicroFE promoter is missing expected payload field: {field}")

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

# GHCR pull credentials are passed through curl config. Normalize only terminal
# line endings and reject embedded whitespace/quotes to avoid malformed directives.
ghcr_probe = (ROOT / "scripts" / "validate-ghcr-pull-access.sh").read_text(encoding="utf-8")
if "GHCR_TOKEN=\"${GHCR_TOKEN%
ghcr_step = reconcile.split("- name: Bootstrap GHCR pull credentials", 1)[1].split(
    "- name: Restart workloads blocked on image pulls", 1
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

print("Workflow contract validation passed.")
\\n'}\"" not in ghcr_probe or "GHCR_TOKEN=\"${GHCR_TOKEN%
ghcr_step = reconcile.split("- name: Bootstrap GHCR pull credentials", 1)[1].split(
    "- name: Restart workloads blocked on image pulls", 1
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

print("Workflow contract validation passed.")
\\r'}\"" not in ghcr_probe:
    fail("GHCR preflight must strip terminal CR/LF characters from copied secret values.")
if "contains embedded whitespace or quotes" not in ghcr_probe:
    fail("GHCR preflight must reject embedded whitespace/quotes instead of passing malformed credentials to curl.")

# GHCR pulls use one platform-owned credential across production namespaces.
bootstrap_script = (ROOT / "scripts" / "bootstrap-runner.sh").read_text(encoding="utf-8")
ghcr_step = reconcile.split("- name: Bootstrap GHCR pull credentials", 1)[1].split(
    "- name: Restart workloads blocked on image pulls", 1
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

print("Workflow contract validation passed.")
