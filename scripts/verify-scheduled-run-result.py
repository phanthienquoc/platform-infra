#!/usr/bin/env python3
"""Fail closed when the latest scheduled reconciliation completed unsuccessfully."""

from __future__ import annotations

import argparse
import json
import sys


def evaluate(run: dict, event: str, run_id: str, run_url: str) -> int:
    status = str(run.get("status") or "")
    conclusion = str(run.get("conclusion") or "pending")

    if status not in {"queued", "waiting", "requested", "pending", "in_progress", "completed"}:
        print(f"::error::Scheduled reconcile #{run_id} returned an unknown status={status or 'missing'}.")
        return 1

    if status != "completed":
        print(
            f"::notice::Scheduled reconcile #{run_id} is still {status}; "
            "completion has not been verified."
        )
        return 0

    if conclusion == "success":
        print(
            f"Scheduled reconcile result passed for run #{run_id}: "
            f"status={status} conclusion={conclusion}."
        )
        print(f"Run evidence: {run_url}")
        return 0

    message = (
        f"latest scheduled reconcile run #{run_id} completed with "
        f"conclusion={conclusion}; run evidence: {run_url}"
    )
    if event == "push":
        print(f"::warning::Read-only API smoke succeeded; {message}.")
        return 0

    print(f"::error::Scheduled reconcile result failed: {message}.")
    return 1


def self_test() -> int:
    cases = [
        ("successful scheduled run", {"status": "completed", "conclusion": "success"}, "schedule", 0),
        ("failed scheduled run", {"status": "completed", "conclusion": "failure"}, "schedule", 1),
        ("cancelled manual run", {"status": "completed", "conclusion": "cancelled"}, "workflow_dispatch", 1),
        ("timed out scheduled run", {"status": "completed", "conclusion": "timed_out"}, "schedule", 1),
        ("failed run during read-only push smoke", {"status": "completed", "conclusion": "failure"}, "push", 0),
        ("queued scheduled run remains pending", {"status": "queued", "conclusion": None}, "schedule", 0),
        ("in-progress scheduled run remains pending", {"status": "in_progress", "conclusion": None}, "schedule", 0),
        ("unknown run status fails closed", {"status": "unexpected", "conclusion": None}, "schedule", 1),
    ]
    failures = 0
    for label, run, event, expected in cases:
        actual = evaluate(run, event, "123", "https://github.com/example/run/123")
        if actual != expected:
            print(f"FAIL: {label}: expected exit {expected}, got {actual}")
            failures += 1
        else:
            print(f"PASS: {label}")
    if failures:
        print(f"{failures} scheduled-run result regression case(s) failed.")
        return 1
    print(f"All {len(cases)} scheduled-run result regression cases passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event")
    parser.add_argument("--run-id")
    parser.add_argument("--run-url")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.event or not args.run_id or not args.run_url:
        parser.error("--event, --run-id and --run-url are required unless --self-test is used")
    try:
        run = json.load(sys.stdin)
        if not isinstance(run, dict):
            raise ValueError("GitHub Actions run response must be a JSON object")
        return evaluate(run, args.event, args.run_id, args.run_url)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"::error::{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
