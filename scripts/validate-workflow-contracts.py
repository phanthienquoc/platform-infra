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
microfe = read("microfe-build-publish.yml")

# MicroFE publisher emits this repository_dispatch event, and reconcile must consume it.
publisher_event = re.search(
    r'event_type:\s*"([^"]+)"|"event_type"\s*:\s*"([^"]+)"|event_type="([^"]+)"',
    microfe,
)
if not publisher_event:
    fail("microfe-build-publish.yml does not declare a repository_dispatch event_type")

published_event = next(group for group in publisher_event.groups() if group)
if published_event not in reconcile:
    fail(
        "Workflow contract mismatch: microfe-build-publish.yml emits "
        f"{published_event!r}, but reconcile-vps.yml does not listen for it."
    )

# The repository_dispatch consumer must use the payload fields the producer promises.
for field in ("commit", "auth_digest", "shell_digest", "ws_digest"):
    if field not in microfe:
        fail(f"MicroFE publisher payload is missing expected field: {field}")

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
