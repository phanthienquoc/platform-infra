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
)
for lane in required_lanes:
    if lane not in reconcile:
        fail(f"reconcile-vps.yml is missing independent deployment lane: {lane.strip()}")

# Auth rollout must not be part of the MicroFE Shell/WS lane.
microfe_lane = reconcile.split("  deploy-microfe:", 1)[1].split("  deploy-tce-dashboard:", 1)[0]
if "rollout status deployment/microfe-auth" in microfe_lane:
    fail("MicroFE lane must not wait for the independent Auth rollout.")

if "Verify Auth workload health" not in reconcile or "Verify MicroFE workload health" not in reconcile:
    fail("Auth and MicroFE lanes must retain workload health verification.")

print("Workflow contract validation passed.")
