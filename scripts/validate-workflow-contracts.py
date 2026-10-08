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
microfe_reconcile = read("reconcile-microfe.yml")

# MicroFE is published by TCE-dashboard and consumed here through repository_dispatch.
if "microfe-images-published" not in microfe_reconcile:
    fail("reconcile-microfe.yml must consume microfe-images-published.")
for field in ("auth_digest", "shell_digest", "ws_digest"):
    if field not in microfe_reconcile:
        fail(f"MicroFE reconciler is missing expected payload field: {field}")

if "microfe-images-published" in reconcile:
    fail("reconcile-vps.yml must not consume microfe-images-published; reconcile-microfe.yml owns that event.")

# Scheduled reconciliation logic must have a matching schedule trigger.
if "github.event_name == 'schedule'" in reconcile and not re.search(
    r'(?m)^\s*schedule:\s*$', reconcile
):
    fail(
        "reconcile-vps.yml references github.event_name == 'schedule' "
        "but does not declare an on.schedule trigger."
    )

# Production reconciliation must retain a final hard failure gate.
if "name: Fail if targeted deployment failed" not in reconcile:
    fail("reconcile-vps.yml is missing its final deployment failure gate.")

# Protected deployment verification must not be silently disabled.
required_steps = (
    "Verify MicroFE rollout",
    "Verify TCE rollout",
    "Verify media-generation rollout",
    "Verify targeted workload health",
)
for step in required_steps:
    if step not in reconcile:
        fail(f"reconcile-vps.yml is missing required verification step: {step}")

print("Workflow contract validation passed.")
