#!/usr/bin/env python3
"""Detect missed native schedule intervals even when the latest run looks fresh."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def parse_timestamp(value: object) -> int:
    if not isinstance(value, str) or not value:
        raise ValueError("native schedule run has no usable created_at timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid native schedule created_at timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError("native schedule created_at timestamp has no timezone")
    return int(parsed.timestamp())


def verify_interarrival(
    http_status: str,
    payload: object,
    workflow_path: str,
    branch: str,
    reference_epoch: int,
    max_gap_minutes: int,
) -> tuple[dict[str, object], dict[str, object] | None, int | None]:
    if http_status != "200":
        raise ValueError(f"GitHub Actions API returned HTTP {http_status}; native schedule history is unverified")
    if not workflow_path.startswith(".github/workflows/"):
        raise ValueError("workflow_path must identify a repository workflow file")
    if not branch:
        raise ValueError("branch must not be empty")
    if reference_epoch <= 0:
        raise ValueError("reference_epoch must be a positive GitHub Actions API timestamp")
    if max_gap_minutes <= 0:
        raise ValueError("max_gap_minutes must be positive")
    if not isinstance(payload, dict):
        raise ValueError("GitHub Actions response must be a JSON object")

    runs = payload.get("workflow_runs")
    if not isinstance(runs, list):
        raise ValueError("GitHub Actions response is missing workflow_runs")

    candidates: list[tuple[int, dict[str, object]]] = []
    for run in runs:
        if not isinstance(run, dict):
            continue
        if run.get("event") != "schedule":
            continue
        if run.get("path") != workflow_path or run.get("head_branch") != branch:
            continue
        try:
            attempt = int(run.get("run_attempt", 1))
        except (TypeError, ValueError) as exc:
            raise ValueError("matching native schedule run has an invalid run_attempt") from exc
        if attempt != 1:
            continue

        run_id = run.get("id")
        if not isinstance(run_id, int) or run_id <= 0:
            raise ValueError("matching native schedule run has an invalid run id")
        head_sha = run.get("head_sha")
        if not isinstance(head_sha, str) or not FULL_SHA.fullmatch(head_sha):
            raise ValueError(f"matching native schedule run #{run_id} does not carry a full source SHA")
        created_epoch = parse_timestamp(run.get("created_at"))
        candidates.append((created_epoch, run))

    if not candidates:
        raise ValueError(f"no original native schedule run for {workflow_path} on {branch} is present in Actions history")

    candidates.sort(key=lambda item: item[0])
    latest_epoch, latest = candidates[-1]
    if latest_epoch > reference_epoch:
        raise ValueError(f"latest native schedule run #{latest['id']} is newer than the watchdog API reference clock")

    if len(candidates) < 2:
        raise ValueError(
            f"only one original native schedule run for {workflow_path} is available; "
            "at least two runs are required to verify the inter-arrival contract"
        )

    previous_epoch, previous = candidates[-2]
    gap_seconds = latest_epoch - previous_epoch
    if gap_seconds <= 0:
        raise ValueError("native schedule run timestamps are not strictly increasing")
    budget_seconds = max_gap_minutes * 60
    if gap_seconds > budget_seconds:
        raise ValueError(
            f"native schedule inter-arrival gap for {workflow_path} is {gap_seconds}s "
            f"between runs #{previous['id']} and #{latest['id']}; budget={budget_seconds}s"
        )
    return latest, previous, gap_seconds


def self_test() -> None:
    reference = int(datetime.fromisoformat("2026-11-07T02:00:00+00:00").timestamp())

    def run(run_id: int, created_at: str, **overrides: object) -> dict[str, object]:
        value: dict[str, object] = {
            "id": run_id,
            "event": "schedule",
            "path": ".github/workflows/reconcile-vps.yml",
            "head_branch": "master",
            "head_sha": "a" * 40,
            "run_attempt": 1,
            "created_at": created_at,
            "status": "completed",
            "conclusion": "success",
            "html_url": f"https://github.com/example/actions/runs/{run_id}",
        }
        value.update(overrides)
        return value

    latest, previous, gap = verify_interarrival(
        "200",
        {"workflow_runs": [run(1, "2026-11-07T01:30:00Z"), run(2, "2026-11-07T01:45:00Z")]},
        ".github/workflows/reconcile-vps.yml",
        "master",
        reference,
        20,
    )
    assert latest["id"] == 2 and previous is not None and previous["id"] == 1
    assert gap == 15 * 60

    # A fresh latest run must not hide a multi-hour gap since the previous native run.
    def expect_error(label: str, status: str, payload: object) -> None:
        try:
            verify_interarrival(
                status,
                payload,
                ".github/workflows/reconcile-vps.yml",
                "master",
                reference,
                20,
            )
        except ValueError:
            return
        raise AssertionError(f"expected {label} to fail")

    expect_error(
        "long inter-arrival gap",
        "200",
        {"workflow_runs": [run(3, "2026-11-06T22:00:00Z"), run(4, "2026-11-07T01:50:00Z")]},
    )
    expect_error("dispatch-only history", "200", {"workflow_runs": [run(5, "2026-11-07T01:50:00Z", event="workflow_dispatch")]})
    expect_error("wrong workflow path", "200", {"workflow_runs": [run(6, "2026-11-07T01:50:00Z", path=".github/workflows/other.yml")]})
    expect_error("wrong branch", "200", {"workflow_runs": [run(7, "2026-11-07T01:50:00Z", head_branch="feature/test")]})
    expect_error("rerun-only history", "200", {"workflow_runs": [run(8, "2026-11-07T01:50:00Z", run_attempt=2)]})
    expect_error("future latest run", "200", {"workflow_runs": [run(9, "2026-11-07T02:01:00Z")]})
    expect_error("short source SHA", "200", {"workflow_runs": [run(10, "2026-11-07T01:50:00Z", head_sha="abc1234")]})
    expect_error("API rate limit", "403", {})
    expect_error("missing read token", "missing-token", {})

    expect_error(
        "single-run history",
        "200",
        {"workflow_runs": [run(11, "2026-11-07T01:50:00Z")]},
    )
    print("Native schedule inter-arrival verifier self-tests passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-file")
    parser.add_argument("--http-status", default="200")
    parser.add_argument("--workflow-path")
    parser.add_argument("--branch", default="master")
    parser.add_argument("--reference-epoch", type=int)
    parser.add_argument("--max-gap-minutes", type=int, default=45)
    parser.add_argument("--warn-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    try:
        if not args.runs_file or not args.workflow_path or args.reference_epoch is None:
            raise ValueError("--runs-file, --workflow-path and --reference-epoch are required")
        with Path(args.runs_file).open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        latest, previous, gap = verify_interarrival(
            args.http_status,
            payload,
            args.workflow_path,
            args.branch,
            args.reference_epoch,
            args.max_gap_minutes,
        )
        if previous is None or gap is None:
            print(
                f"::notice::Only one original native schedule run for {args.workflow_path} is available; "
                "inter-arrival gap is not yet measurable."
            )
        else:
            print(
                f"Native schedule inter-arrival passed for {args.workflow_path}: "
                f"previous=#{previous['id']} latest=#{latest['id']} gap={gap}s "
                f"budget={args.max_gap_minutes * 60}s."
            )
        print(f"Latest native schedule evidence: {latest.get('html_url', 'URL unavailable')}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        severity = "warning" if args.warn_only else "error"
        print(f"::{severity}::Native schedule inter-arrival observation: {exc}")
        return 0 if args.warn_only else 1


if __name__ == "__main__":
    sys.exit(main())
