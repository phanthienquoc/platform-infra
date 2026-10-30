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

# MicroFE digest promotions must use the shared GitOps promotion workflow.
if "microfe-images-published" not in promotion:
    fail("gitops-image-promotion.yml must consume microfe-images-published.")
for field in ("auth_digest", "shell_digest", "ws_digest"):
    if field not in promotion:
        fail(f"Shared MicroFE promoter is missing expected payload field: {field}")
if (WORKFLOW_DIR / "reconcile-microfe.yml").exists():
    fail("Dedicated reconcile-microfe.yml must be removed.")
if "gitops-promoted-ready" not in reconcile:
    fail("reconcile-vps.yml must consume the shared GitOps promotion event.")
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

print("Workflow contract validation passed.")
