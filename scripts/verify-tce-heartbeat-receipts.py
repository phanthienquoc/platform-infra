#!/usr/bin/env python3
"""Normalize successful Platform TCE-heartbeat receipts into verified source run history."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
RUN_NAME = re.compile(
    r"^Recover Stale Scheduled Ops — repository_dispatch / source "
    r"([1-9][0-9]*)(?: / (?P<path>\.github/workflows/[A-Za-z0-9._/-]+\.yml))?$"
)
RECEIVER_PATH = ".github/workflows/recover-stale-ops.yml"
ALLOWED_WORKFLOWS = {
    ".github/workflows/wf-06-tce-healthcheck.yml",
    ".github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml",
}


def parse_timestamp(value: object, label: str) -> int:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} has no usable created_at timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} has an invalid created_at timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} created_at timestamp has no timezone")
    return int(parsed.timestamp())


def positive_int(value: object, label: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a positive integer") from exc
    if result <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return result


def normalize_receipts(
    receipts: object,
    workflow_path: str,
    branch: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    if workflow_path not in ALLOWED_WORKFLOWS:
        raise ValueError(f"workflow_path is not an approved TCE health schedule: {workflow_path}")
    if branch != "master":
        raise ValueError("TCE heartbeat history must be restricted to master")
    if not isinstance(receipts, list):
        raise ValueError("receipt payload must contain a receipts array")

    verified: dict[int, tuple[int, dict[str, Any]]] = {}
    warnings: list[str] = []

    for index, item in enumerate(receipts):
        try:
            if not isinstance(item, dict):
                raise ValueError("receipt entry is not an object")
            receipt = item.get("receipt")
            source = item.get("source_run")
            if not isinstance(receipt, dict) or not isinstance(source, dict):
                raise ValueError("receipt entry is missing receipt or source_run metadata")

            if receipt.get("event") != "repository_dispatch":
                raise ValueError("Platform receipt event is not repository_dispatch")
            if receipt.get("path") != RECEIVER_PATH:
                raise ValueError("Platform receipt was not created by recover-stale-ops.yml")
            if receipt.get("head_branch") != branch:
                raise ValueError("Platform receipt is not on master")
            if positive_int(receipt.get("run_attempt", 1), "Platform receipt run_attempt") != 1:
                raise ValueError("Platform receipt is a rerun")
            if receipt.get("conclusion") != "success":
                raise ValueError("Platform heartbeat receiver did not complete successfully")

            run_name = receipt.get("display_title") or receipt.get("name") or ""
            match = RUN_NAME.fullmatch(run_name) if isinstance(run_name, str) else None
            if match is None:
                raise ValueError("Platform receipt run-name does not carry a source run ID and workflow path")
            source_run_id = positive_int(match.group(1), "source run ID")
            source_path = match.group("path")
            if source_path is not None and source_path != workflow_path:
                raise ValueError("Platform receipt belongs to a different TCE workflow")

            positive_int(receipt.get("id"), "Platform receipt ID")
            if positive_int(source.get("id"), "TCE source run ID") != source_run_id:
                raise ValueError("TCE source run ID does not match the Platform receipt run-name")
            if source.get("path") != workflow_path:
                raise ValueError("TCE source run workflow path does not match the receipt")
            if source.get("event") != "schedule":
                raise ValueError("TCE source run event is not schedule")
            if source.get("head_branch") != branch:
                raise ValueError("TCE source run is not on master")
            if positive_int(source.get("run_attempt", 1), "TCE source run_attempt") != 1:
                raise ValueError("TCE source run is a rerun")
            source_sha = source.get("head_sha")
            if not isinstance(source_sha, str) or not FULL_SHA.fullmatch(source_sha):
                raise ValueError("TCE source run does not carry a full commit SHA")

            source_created = parse_timestamp(source.get("created_at"), "TCE source run")
            receipt_created = parse_timestamp(receipt.get("created_at"), "Platform receipt")
            if receipt_created < source_created:
                raise ValueError("Platform heartbeat receipt predates its TCE source run")

            existing = verified.get(source_run_id)
            if existing is None or receipt_created > existing[0]:
                verified[source_run_id] = (receipt_created, source)
        except ValueError as exc:
            warnings.append(f"receipt[{index}] ignored: {exc}")

    runs = [item[1] for item in verified.values()]
    runs.sort(key=lambda run: parse_timestamp(run.get("created_at"), "TCE source run"))
    return runs, warnings


def self_test() -> None:
    path = ".github/workflows/wf-06-tce-healthcheck.yml"
    sha = "a" * 40

    def make(run_id: int, created_at: str, **overrides: object) -> dict[str, Any]:
        receipt = {
            "id": run_id + 1000,
            "name": f"Recover Stale Scheduled Ops — repository_dispatch / source {run_id} / {path}",
            "event": "repository_dispatch",
            "path": RECEIVER_PATH,
            "head_branch": "master",
            "run_attempt": 1,
            "conclusion": "success",
            "created_at": created_at,
        }
        source = {
            "id": run_id,
            "path": path,
            "event": "schedule",
            "head_branch": "master",
            "head_sha": sha,
            "run_attempt": 1,
            "created_at": created_at,
            "status": "completed",
            "conclusion": "failure",
        }
        receipt.update(overrides.pop("receipt", {}))
        source.update(overrides.pop("source", {}))
        return {"receipt": receipt, "source_run": source}

    valid, warnings = normalize_receipts(
        [make(101, "2026-11-10T01:00:05Z"), make(102, "2026-11-10T01:15:05Z")],
        path,
        "master",
    )
    assert [run["id"] for run in valid] == [101, 102]
    assert not warnings

    invalid_cases = [
        make(103, "2026-11-10T01:30:05Z", receipt={"event": "workflow_dispatch"}),
        make(104, "2026-11-10T01:45:05Z", receipt={"conclusion": "failure"}),
        make(105, "2026-11-10T02:00:05Z", receipt={"run_attempt": 2}),
        make(106, "2026-11-10T02:15:05Z", source={"event": "workflow_dispatch"}),
        make(107, "2026-11-10T02:30:05Z", source={"head_branch": "feature/test"}),
        make(108, "2026-11-10T02:45:05Z", source={"head_sha": "abc1234"}),
        make(109, "2026-11-10T03:00:05Z", source={"path": ".github/workflows/other.yml"}),
        make(110, "2026-11-10T03:15:05Z", source={"run_attempt": 2}),
        make(111, "2026-11-10T03:30:05Z", source={"id": 999}),
        make(112, "2026-11-10T03:45:05Z", receipt={"head_branch": "feature/test"}),
        make(113, "2026-11-10T04:00:05Z", receipt={"name": "untrusted source 113"}),
        make(115, "2026-11-10T04:30:05Z", source={"created_at": "2026-11-10T04:30:06Z"}),
    ]
    valid_after_rejection, warnings = normalize_receipts(invalid_cases, path, "master")
    assert valid_after_rejection == []
    assert len(warnings) == len(invalid_cases)

    wf12 = ".github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml"
    other_path = make(114, "2026-11-10T04:15:05Z")
    other_path["receipt"]["name"] = (
        f"Recover Stale Scheduled Ops — repository_dispatch / source 114 / {wf12}"
    )
    other_path["source_run"]["path"] = wf12
    only_wf12, _ = normalize_receipts([other_path], wf12, "master")
    assert [run["id"] for run in only_wf12] == [114]

    legacy = make(116, "2026-11-10T04:45:05Z")
    legacy["receipt"]["name"] = "Recover Stale Scheduled Ops — repository_dispatch / source 116"
    legacy_runs, legacy_warnings = normalize_receipts([legacy], path, "master")
    assert [run["id"] for run in legacy_runs] == [116]
    assert not legacy_warnings

    duplicate = make(101, "2026-11-10T01:00:06Z")
    deduped, _ = normalize_receipts([make(101, "2026-11-10T01:00:05Z"), duplicate], path, "master")
    assert len(deduped) == 1 and deduped[0]["id"] == 101

    print("TCE heartbeat receipt history self-tests passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts-file")
    parser.add_argument("--workflow-path")
    parser.add_argument("--branch", default="master")
    parser.add_argument("--output-runs-file")
    parser.add_argument("--warn-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.receipts_file or not args.workflow_path or not args.output_runs_file:
        parser.error("--receipts-file, --workflow-path and --output-runs-file are required")

    output_path = Path(args.output_runs_file)
    try:
        payload = json.loads(Path(args.receipts_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("receipt payload must be a JSON object")
        runs, warnings = normalize_receipts(payload.get("receipts"), args.workflow_path, args.branch)
        output_path.write_text(
            json.dumps({"workflow_runs": runs}, indent=2) + "\n",
            encoding="utf-8",
        )
        for warning in warnings:
            print(f"::notice::{warning}")
        if not runs:
            print(
                f"::warning::No successful, verified Platform heartbeat receipt is available "
                f"for {args.workflow_path}; cross-repository schedule history is unverified."
            )
        else:
            print(
                f"Verified {len(runs)} TCE schedule heartbeat receipt(s) for {args.workflow_path}; "
                "source metadata was checked by run ID."
            )
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        output_path.write_text('{"workflow_runs":[]}\n', encoding="utf-8")
        severity = "warning" if args.warn_only else "error"
        print(f"::{severity}::Unable to normalize TCE heartbeat receipts: {exc}")
        return 0 if args.warn_only else 1


if __name__ == "__main__":
    sys.exit(main())