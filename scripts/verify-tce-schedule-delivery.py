#!/usr/bin/env python3
"""Observe native TCE WF-06 delivery from verified Platform heartbeat receipts.

The input is normalized source-run metadata recovered from successful
Platform-owned heartbeat receipts. This is advisory and does not gate
Platform reconciliation. It does not assert public endpoint health.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime

EXPECTED_PATH = ".github/workflows/wf-06-tce-healthcheck.yml"
EXPECTED_BRANCH = "master"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def parse_timestamp(value: object) -> int:
    if not isinstance(value, str) or not value:
        raise ValueError("scheduled run has no usable created_at timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid scheduled run created_at timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError("scheduled run created_at timestamp has no timezone")
    return int(parsed.timestamp())


def verify_response(
    http_status: str,
    payload: object,
    reference_epoch: int,
    max_age_minutes: int,
) -> tuple[dict[str, object], int]:
    if http_status != "200":
        raise ValueError(f"TCE heartbeat source-history input returned status {http_status}; schedule delivery is unverified")
    if reference_epoch <= 0:
        raise ValueError("watchdog reference epoch must be a positive GitHub Actions API timestamp")
    if max_age_minutes <= 0:
        raise ValueError("maximum schedule age must be positive")
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
        if run.get("path") != EXPECTED_PATH:
            continue
        if run.get("head_branch") != EXPECTED_BRANCH:
            continue

        try:
            attempt = int(run.get("run_attempt", 1))
        except (TypeError, ValueError) as exc:
            raise ValueError("matching WF-06 schedule run has an invalid run_attempt") from exc
        if attempt != 1:
            continue

        run_id = run.get("id")
        if not isinstance(run_id, int) or run_id <= 0:
            raise ValueError("matching WF-06 schedule run has an invalid run id")
        head_sha = run.get("head_sha")
        if not isinstance(head_sha, str) or not FULL_SHA.fullmatch(head_sha):
            raise ValueError(f"matching WF-06 schedule run #{run_id} does not carry a full source SHA")
        created_epoch = parse_timestamp(run.get("created_at"))
        candidates.append((created_epoch, run))

    if not candidates:
        raise ValueError(
            "no original native WF-06 schedule run for master is present in the latest Actions history"
        )

    created_epoch, latest = max(candidates, key=lambda item: item[0])
    age_seconds = reference_epoch - created_epoch
    if age_seconds < 0:
        raise ValueError("latest native WF-06 schedule run is newer than the watchdog API reference clock")
    if age_seconds > max_age_minutes * 60:
        raise ValueError(
            f"native WF-06 schedule is stale: latest run #{latest['id']} is "
            f"{age_seconds}s old; budget={max_age_minutes * 60}s"
        )
    return latest, age_seconds


def self_test() -> None:
    reference = int(datetime.fromisoformat("2026-11-06T10:59:00+00:00").timestamp())
    base_run: dict[str, object] = {
        "id": 12345,
        "event": "schedule",
        "path": EXPECTED_PATH,
        "head_branch": "master",
        "head_sha": "a" * 40,
        "run_attempt": 1,
        "created_at": "2026-11-06T10:50:00Z",
        "status": "completed",
        "conclusion": "failure",
        "html_url": "https://github.com/phanthienquoc/TCE-dashboard/actions/runs/12345",
    }

    latest, age = verify_response("200", {"workflow_runs": [base_run]}, reference, 25)
    assert latest["id"] == 12345
    assert age == 9 * 60
    assert latest["conclusion"] == "failure"  # delivery remains fresh; endpoint health is separate

    def expect_error(label: str, status: str, payload: object) -> None:
        try:
            verify_response(status, payload, reference, 25)
        except ValueError:
            return
        raise AssertionError(f"expected {label} to fail")

    expect_error("stale schedule", "200", {"workflow_runs": [{**base_run, "created_at": "2026-11-06T10:30:00Z"}]})
    expect_error("missing schedule", "200", {"workflow_runs": []})
    expect_error("dispatch-only history", "200", {"workflow_runs": [{**base_run, "event": "workflow_dispatch"}]})
    expect_error("wrong branch", "200", {"workflow_runs": [{**base_run, "head_branch": "feature/test"}]})
    expect_error("rerun attempt", "200", {"workflow_runs": [{**base_run, "run_attempt": 2}]})
    expect_error("future timestamp", "200", {"workflow_runs": [{**base_run, "created_at": "2026-11-06T11:00:00Z"}]})
    expect_error("short source SHA", "200", {"workflow_runs": [{**base_run, "head_sha": "abc1234"}]})
    expect_error("API rate limit", "403", {})
    expect_error("missing read token", "missing-token", {})
    print("TCE native schedule delivery verifier self-tests passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-file", help="JSON file returned by the GitHub Actions runs API")
    parser.add_argument("--http-status", default="200", help="HTTP status returned by the public GitHub API request")
    parser.add_argument("--reference-epoch", type=int, help="Current watchdog run created_at epoch from the GitHub API")
    parser.add_argument("--max-age-minutes", type=int, default=25)
    parser.add_argument("--warn-only", action="store_true", help="Report an observation warning without failing the watchdog")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    try:
        if not args.runs_file or args.reference_epoch is None:
            raise ValueError("--runs-file and --reference-epoch are required")
        with open(args.runs_file, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        latest, age_seconds = verify_response(
            args.http_status,
            payload,
            args.reference_epoch,
            args.max_age_minutes,
        )
        run_id = latest["id"]
        status = latest.get("status", "unknown")
        conclusion = latest.get("conclusion") or "pending"
        run_url = latest.get("html_url") or "URL unavailable"
        print(
            f"Native TCE WF-06 schedule delivered: run #{run_id}, "
            f"age={age_seconds}s, status={status}, conclusion={conclusion}."
        )
        print(f"Schedule evidence: {run_url}")
        print("This observation verifies native schedule delivery only; it does not assert public endpoint health.")
        if status == "completed" and conclusion != "success":
            print(
                f"::warning::TCE WF-06 run #{run_id} was delivered on schedule but concluded "
                f"{conclusion}; public endpoint health remains a separate signal."
            )
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        severity = "warning" if args.warn_only else "error"
        print(f"::{severity}::TCE native WF-06 schedule observation: {exc}")
        return 0 if args.warn_only else 1


if __name__ == "__main__":
    sys.exit(main())
