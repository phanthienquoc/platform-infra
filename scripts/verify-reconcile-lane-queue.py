#!/usr/bin/env python3
"""Detect long runner-assignment delays in scheduled reconciliation deployment lanes.

Input is the GitHub Actions jobs API response on stdin. All timestamps are compared
against the watchdog run's GitHub API created_at timestamp, never the hosted clock.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime


def epoch(value: str) -> int:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid GitHub Actions timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"GitHub Actions timestamp has no timezone: {value!r}")
    return int(parsed.timestamp())


def evaluate(
    payload: dict,
    reference_epoch: int,
    max_queue_minutes: int,
    event_name: str,
    reconcile_created_at: str | None = None,
    max_reconcile_age_minutes: int = 45,
) -> int:
    jobs = payload.get("jobs")
    if not isinstance(jobs, list):
        raise ValueError("GitHub Actions jobs response must contain a jobs array")

    stale_reconcile = False
    if reconcile_created_at:
        reconcile_age_seconds = reference_epoch - epoch(reconcile_created_at)
        if reconcile_age_seconds < 0:
            raise ValueError("scheduled reconciliation creation timestamp is in the future")
        stale_reconcile = reconcile_age_seconds > max_reconcile_age_minutes * 60
        if stale_reconcile:
            print(
                "::notice::Latest scheduled reconciliation is stale "
                f"(age={reconcile_age_seconds // 60}m > {max_reconcile_age_minutes}m); "
                "the freshness gate already reports this run, so historical runner-assignment "
                "delays are not re-enforced. Still-queued unassigned lanes remain actionable."
            )

    delayed: list[tuple[int, str, int, str, str, int]] = []
    unmeasurable: list[str] = []
    for job in jobs:
        name = str(job.get("name") or "")
        if not name.startswith("Deploy lane — "):
            continue

        status = str(job.get("status") or "")
        runner_id = int(job.get("runner_id") or 0)
        attempt = int(job.get("run_attempt") or 1)
        if attempt > 1:
            unmeasurable.append(name)
            continue

        # Once the parent reconciliation itself is outside the freshness budget,
        # its completed/assigned historical delay is already covered by the stale-run
        # failure. Re-reporting that same delay on every workflow_run creates a
        # permanent watchdog failure. A lane still waiting for assignment remains
        # actionable and is evaluated below.
        if stale_reconcile and status in ("in_progress", "completed") and runner_id > 0:
            continue

        created_at = job.get("created_at")
        if not created_at:
            if status in ("queued", "in_progress"):
                raise ValueError(f"deployment lane has no job creation timestamp: {name}")
            continue
        created_epoch = epoch(str(created_at))

        if status in ("queued", "waiting") or (status == "in_progress" and runner_id == 0):
            # Still waiting for a runner assignment/start; measure until the watchdog's
            # GitHub API reference time so completed workflow lanes are not required.
            delay_seconds = reference_epoch - created_epoch
            delay_kind = "unassigned"
        elif status in ("in_progress", "completed") and runner_id > 0:
            started_at = job.get("started_at")
            if not started_at:
                raise ValueError(f"assigned deployment lane has no started_at timestamp: {name}")
            delay_seconds = epoch(str(started_at)) - created_epoch
            delay_kind = "runner-assignment"
        else:
            # Skipped/cancelled lanes and completed jobs without a runner are not
            # evidence of runner backlog.
            continue

        if delay_seconds < 0:
            raise ValueError(f"deployment lane queue timestamp is in the future or inconsistent: {name}")
        delay_minutes = delay_seconds // 60
        if delay_seconds > max_queue_minutes * 60:
            delayed.append(
                (
                    int(job.get("id") or 0),
                    name,
                    delay_minutes,
                    str(created_at),
                    delay_kind,
                    runner_id,
                )
            )

    for name in unmeasurable:
        print(f"::notice::Deployment lane rerun queue is not measurable from the original attempt timestamp: {name}")

    if not delayed:
        print(
            "No scheduled deployment lane exceeded "
            f"the {max_queue_minutes}-minute runner queue budget."
        )
        return 0

    severity = "warning" if event_name == "push" else "error"
    for job_id, name, delay_minutes, queued_at, delay_kind, runner_id in delayed:
        print(
            f"::{severity}::Deployment lane #{job_id} ({name}) exceeded the runner queue budget: "
            f"delay={delay_minutes}m kind={delay_kind} runner_id={runner_id} "
            f"created_at={queued_at} budget={max_queue_minutes}m."
        )

    if event_name == "push":
        print("::warning::Read-only watchdog push smoke reports queue telemetry without failing the post-merge smoke.")
        return 0

    print("::error::Refusing to report scheduled deployment lanes healthy after a runner queue-budget breach.")
    return 1


def self_test() -> int:
    reference = epoch("2026-11-02T17:00:00Z")
    cases = [
        (
            "completed lanes with short assignment delay are healthy",
            {"jobs": [{"id": 1, "name": "Deploy lane — TCE Dashboard", "status": "completed", "runner_id": 2, "created_at": "2026-11-02T16:59:00Z", "started_at": "2026-11-02T16:59:20Z"}]},
            "schedule",
            0,
        ),
        (
            "queued lane inside budget is tolerated",
            {"jobs": [{"id": 2, "name": "Deploy lane — Auth", "status": "queued", "runner_id": 0, "created_at": "2026-11-02T16:50:00Z"}]},
            "schedule",
            0,
        ),
        (
            "queued lane exactly at the 15-minute boundary is tolerated",
            {"jobs": [{"id": 11, "name": "Deploy lane — TCE Dashboard", "status": "queued", "runner_id": 0, "created_at": "2026-11-02T16:45:00Z"}]},
            "schedule",
            0,
        ),
        (
            "queued lane 15m01s beyond the budget fails scheduled enforcement",
            {"jobs": [{"id": 12, "name": "Deploy lane — Keycloak", "status": "queued", "runner_id": 0, "created_at": "2026-11-02T16:44:59Z"}]},
            "schedule",
            1,
        ),
        (
            "assigned lane 15m01s beyond the budget fails scheduled enforcement",
            {"jobs": [{"id": 13, "name": "Deploy lane — Auth", "status": "completed", "runner_id": 7, "created_at": "2026-11-02T16:44:59Z", "started_at": "2026-11-02T17:00:00Z"}]},
            "schedule",
            1,
        ),
        (
            "queued lane beyond budget fails scheduled enforcement",
            {"jobs": [{"id": 3, "name": "Deploy lane — MicroFE Shell / WS", "status": "queued", "runner_id": 0, "created_at": "2026-11-02T16:40:00Z"}]},
            "schedule",
            1,
        ),
        (
            "push smoke warns without failing",
            {"jobs": [{"id": 4, "name": "Deploy lane — Keycloak", "status": "queued", "runner_id": 0, "created_at": "2026-11-02T16:40:00Z"}]},
            "push",
            0,
        ),
        (
            "completed lane preserves historical runner assignment delay",
            {"jobs": [{"id": 5, "name": "Deploy lane — Auth", "status": "completed", "runner_id": 2, "created_at": "2026-11-02T16:27:00Z", "started_at": "2026-11-02T16:58:00Z"}]},
            "schedule",
            1,
        ),
        (
            "assigned but still queued lane is measured from creation",
            {"jobs": [{"id": 6, "name": "Deploy lane — Auth", "status": "queued", "runner_id": 2, "created_at": "2026-11-02T16:30:00Z"}]},
            "schedule",
            1,
        ),
        (
            "unrelated queued jobs are ignored",
            {"jobs": [{"id": 7, "name": "deployment-lane-summary", "status": "queued", "runner_id": 0, "created_at": "2026-11-02T16:30:00Z"}]},
            "schedule",
            0,
        ),
        (
            "rerun queue age is not inferred from the original attempt",
            {"jobs": [{"id": 8, "name": "Deploy lane — Auth", "status": "queued", "runner_id": 0, "run_attempt": 2, "created_at": "2026-11-02T16:30:00Z"}]},
            "schedule",
            0,
        ),
    ]

    failures = 0
    for label, payload, event_name, expected in cases:
        actual = evaluate(payload, reference, 15, event_name)
        if actual != expected:
            print(f"FAIL: {label}: expected exit {expected}, got {actual}")
            failures += 1
        else:
            print(f"PASS: {label}")
    stale_reconcile = "2026-11-02T16:00:00Z"
    stale_completed = {
        "jobs": [
            {
                "id": 9,
                "name": "Deploy lane — Auth",
                "status": "completed",
                "runner_id": 2,
                "created_at": "2026-11-02T16:27:00Z",
                "started_at": "2026-11-02T16:58:00Z",
            }
        ]
    }
    actual = evaluate(
        stale_completed,
        reference,
        15,
        "workflow_run",
        reconcile_created_at=stale_reconcile,
        max_reconcile_age_minutes=45,
    )
    if actual != 0:
        print("FAIL: stale reconciliation does not re-enforce completed historical queue delay")
        failures += 1
    else:
        print("PASS: stale reconciliation suppresses repeated historical queue failure")

    stale_queued = {
        "jobs": [
            {
                "id": 10,
                "name": "Deploy lane — TCE Dashboard",
                "status": "queued",
                "runner_id": 0,
                "created_at": "2026-11-02T16:40:00Z",
            }
        ]
    }
    actual = evaluate(
        stale_queued,
        reference,
        15,
        "workflow_run",
        reconcile_created_at=stale_reconcile,
        max_reconcile_age_minutes=45,
    )
    if actual != 1:
        print("FAIL: stale reconciliation still detects a currently unassigned lane")
        failures += 1
    else:
        print("PASS: stale reconciliation still fails for a currently unassigned lane")

    if failures:
        print(f"{failures} deployment-lane queue regression case(s) failed.")
        return 1
    print(f"All {len(cases)} deployment-lane queue regression cases passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-epoch", type=int)
    parser.add_argument("--max-queue-minutes", type=int, default=15)
    parser.add_argument("--event", default="schedule")
    parser.add_argument("--reconcile-created-at")
    parser.add_argument("--max-reconcile-age-minutes", type=int, default=45)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.reference_epoch is None:
        parser.error("--reference-epoch is required unless --self-test is used")
    if not args.reconcile_created_at:
        parser.error("--reconcile-created-at is required unless --self-test is used")
    if args.max_queue_minutes < 0:
        parser.error("--max-queue-minutes must be non-negative")
    if args.max_reconcile_age_minutes < 0:
        parser.error("--max-reconcile-age-minutes must be non-negative")
    try:
        payload = json.load(sys.stdin)
        return evaluate(
            payload,
            args.reference_epoch,
            args.max_queue_minutes,
            args.event,
            reconcile_created_at=args.reconcile_created_at,
            max_reconcile_age_minutes=args.max_reconcile_age_minutes,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"::error::{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
