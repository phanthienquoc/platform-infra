#!/usr/bin/env python3
"""Fail closed on unauthenticated or uncorrelated GitOps-ready reconciliation dispatches."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROMOTION_WORKFLOW = ".github/workflows/gitops-image-promotion.yml"
SHA = re.compile(r"^[0-9a-f]{40}$")
PROD_RELEASE = re.compile(r"^prod-v[0-9]+\.[0-9]+\.[0-9]+-([0-9a-f]{40})$")
MICROFE_RELEASE = re.compile(r"^microfe-([0-9a-f]{7})$")
PAYLOAD_KEYS = {
    "app",
    "component",
    "release",
    "source_commit",
    "promotion_run_id",
    "promotion_run_attempt",
    "promotion_workflow_path",
    "promotion_head_sha",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_unique_successful_job(jobs: list, expected_name: str, *, prefix: bool = False) -> None:
    matching_jobs = [
        job
        for job in jobs
        if isinstance(job, dict)
        and isinstance(job.get("name"), str)
        and (
            job["name"].startswith(expected_name)
            if prefix
            else job["name"] == expected_name
        )
    ]
    require(
        len(matching_jobs) == 1,
        f"Promotion run must contain exactly one required job matching {expected_name!r}; found {len(matching_jobs)}.",
    )
    job = matching_jobs[0]
    require(
        job.get("status") == "completed" and job.get("conclusion") == "success",
        f"Required promotion job {job.get('name')!r} is not completed-success "
        f"(status={job.get('status')!r}, conclusion={job.get('conclusion')!r}).",
    )


def validate(event: dict, promotion_run: dict, promotion_jobs: dict) -> None:
    require(event.get("action") == "gitops-promoted-ready", "Unsupported repository_dispatch action.")
    payload = event.get("client_payload")
    require(isinstance(payload, dict), "GitOps-ready dispatch must include an object client_payload.")
    missing = sorted(PAYLOAD_KEYS - set(payload))
    extra = sorted(set(payload) - PAYLOAD_KEYS)
    require(not missing, f"GitOps-ready payload is missing fields: {', '.join(missing)}.")
    require(not extra, f"GitOps-ready payload contains unsupported fields: {', '.join(extra)}.")

    app = payload["app"]
    component = payload["component"]
    release = payload["release"]
    source_commit = payload["source_commit"]
    require(isinstance(source_commit, str) and SHA.fullmatch(source_commit) is not None,
            "source_commit must be a full lowercase 40-character SHA.")

    if app in ("auth-service", "tce-dashboard"):
        require(component == ("auth" if app == "auth-service" else "release"),
                f"Unsupported component for {app}: {component!r}.")
        match = PROD_RELEASE.fullmatch(release if isinstance(release, str) else "")
        require(match is not None and match.group(1) == source_commit,
                f"{app} release must be a prod-v<semver>-<full-source-SHA> tag bound to source_commit.")
        require(promotion_run.get("event") in ("repository_dispatch", "workflow_dispatch"),
                "Auth/TCE promotion run must originate from a supported GitHub Actions dispatch.")
    elif app == "microfe":
        require(component == "release", "MicroFE GitOps-ready component must be release.")
        match = MICROFE_RELEASE.fullmatch(release if isinstance(release, str) else "")
        require(match is not None and match.group(1) == source_commit[:7],
                "MicroFE release label must equal microfe- plus the source commit's first seven characters.")
        require(promotion_run.get("event") == "repository_dispatch",
                "MicroFE promotion must originate from a repository_dispatch run.")
    else:
        raise ValueError(f"Retired or unsupported GitOps-ready application: {app!r}.")

    run_id = payload["promotion_run_id"]
    attempt = payload["promotion_run_attempt"]
    require(isinstance(run_id, str) and re.fullmatch(r"[1-9][0-9]*", run_id) is not None,
            "promotion_run_id must be a positive numeric Actions run ID.")
    require(isinstance(attempt, str) and re.fullmatch(r"[1-9][0-9]*", attempt) is not None,
            "promotion_run_attempt must be a positive numeric Actions attempt.")
    require(payload["promotion_workflow_path"] == PROMOTION_WORKFLOW,
            "promotion_workflow_path is not the approved GitOps promotion workflow.")
    promotion_head_sha = payload["promotion_head_sha"]
    require(isinstance(promotion_head_sha, str) and SHA.fullmatch(promotion_head_sha) is not None,
            "promotion_head_sha must be a full lowercase 40-character SHA.")

    require(str(promotion_run.get("id", "")) == run_id,
            "Promotion run ID does not match the referenced Actions run.")
    require(promotion_run.get("path") == PROMOTION_WORKFLOW,
            "Referenced Actions run did not execute the approved GitOps promotion workflow.")
    require(promotion_run.get("head_branch") == "master",
            "GitOps promotion workflow run must originate from master.")
    require(promotion_run.get("head_sha") == promotion_head_sha,
            "Promotion workflow head SHA does not match the dispatch payload.")
    require(str(promotion_run.get("run_attempt", "")) == attempt,
            "Promotion workflow attempt does not match the dispatch payload.")
    require(promotion_run.get("status") == "completed",
            "GitOps promotion workflow run has not completed.")
    require(promotion_run.get("conclusion") == "success",
            f"GitOps promotion workflow run did not succeed (conclusion={promotion_run.get('conclusion')!r}).")

    jobs = promotion_jobs.get("jobs") if isinstance(promotion_jobs, dict) else None
    require(isinstance(jobs, list), "Promotion run jobs response must contain a jobs array.")
    if app == "microfe":
        require_unique_successful_job(
            jobs,
            "Promote MicroFE image digests as one GitOps change",
        )
    elif app == "tce-dashboard":
        require_unique_successful_job(jobs, "Promote TCE web/service digests atomically")
        require_unique_successful_job(jobs, "Coordinate TCE release")
    else:
        require_unique_successful_job(jobs, "Promote auth-service /", prefix=True)


def self_test() -> None:
    source = "a" * 40
    head = "b" * 40
    base_run = {
        "id": 12345,
        "path": PROMOTION_WORKFLOW,
        "head_branch": "master",
        "head_sha": head,
        "run_attempt": 1,
        "event": "repository_dispatch",
        "status": "completed",
        "conclusion": "success",
    }

    def case(app: str, component: str, release: str, event_name: str = "repository_dispatch") -> tuple[dict, dict, dict]:
        payload = {
            "app": app,
            "component": component,
            "release": release,
            "source_commit": source,
            "promotion_run_id": "12345",
            "promotion_run_attempt": "1",
            "promotion_workflow_path": PROMOTION_WORKFLOW,
            "promotion_head_sha": head,
        }
        run = {**base_run, "event": event_name}
        if app == "microfe":
            jobs = [{"name": "Promote MicroFE image digests as one GitOps change", "status": "completed", "conclusion": "success"}]
        elif app == "tce-dashboard":
            jobs = [
                {"name": "Promote TCE web/service digests atomically", "status": "completed", "conclusion": "success"},
                {"name": "Coordinate TCE release", "status": "completed", "conclusion": "success"},
            ]
        else:
            jobs = [{"name": "Promote auth-service / auth", "status": "completed", "conclusion": "success"}]
        return {"action": "gitops-promoted-ready", "client_payload": payload}, run, {"jobs": jobs}

    positive = [
        case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch"),
        case("auth-service", "auth", f"prod-v1.2.3-{source}", "repository_dispatch"),
        case("tce-dashboard", "release", f"prod-v2.0.1-{source}"),
        case("microfe", "release", f"microfe-{source[:7]}"),
    ]
    for event, run, jobs in positive:
        validate(event, run, jobs)

    negative = []
    event, run, jobs = case("stockdividend", "release", f"prod-v1.2.3-{source}")
    negative.append((event, run, jobs))
    event, run, jobs = case("media-generation", "release", f"prod-v1.2.3-{source}")
    negative.append((event, run, jobs))
    event, run, jobs = case("tce-dashboard", "auth", f"prod-v1.2.3-{source}")
    negative.append((event, run, jobs))
    event, run, jobs = case("microfe", "release", "microfe-fffffff")
    negative.append((event, run, jobs))
    event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{'c' * 40}", "workflow_dispatch")
    negative.append((event, run, jobs))
    event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "push")
    negative.append((event, run, jobs))
    event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch")
    event["client_payload"]["unexpected"] = "must-not-pass"
    negative.append((event, run, jobs))
    for field, value in (
        ("promotion_run_id", "not-a-run"),
        ("promotion_run_attempt", "0"),
        ("promotion_workflow_path", ".github/workflows/other.yml"),
        ("promotion_head_sha", "short"),
        ("source_commit", "short"),
    ):
        event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch")
        event["client_payload"][field] = value
        negative.append((event, run, jobs))
    for field, value in (
        ("id", 99999),
        ("path", ".github/workflows/other.yml"),
        ("head_branch", "feature"),
        ("head_sha", "c" * 40),
        ("run_attempt", 2),
        ("status", "in_progress"),
        ("conclusion", "failure"),
    ):
        event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch")
        run[field] = value
        negative.append((event, run, jobs))
    event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch")
    event["action"] = "other-event"
    negative.append((event, run, jobs))

    event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch")
    jobs["jobs"][0]["conclusion"] = "failure"
    negative.append((event, run, jobs))
    event, run, jobs = case("tce-dashboard", "release", f"prod-v1.2.3-{source}")
    jobs["jobs"] = jobs["jobs"][:1]
    negative.append((event, run, jobs))
    event, run, jobs = case("microfe", "release", f"microfe-{source[:7]}")
    jobs["jobs"] = []
    negative.append((event, run, jobs))

    # A successful duplicate must not hide an ambiguous or partially failed promotion job.
    event, run, jobs = case("microfe", "release", f"microfe-{source[:7]}")
    jobs["jobs"].append({**jobs["jobs"][0], "conclusion": "failure"})
    negative.append((event, run, jobs))
    event, run, jobs = case("tce-dashboard", "release", f"prod-v1.2.3-{source}")
    jobs["jobs"].append(dict(jobs["jobs"][1]))
    negative.append((event, run, jobs))
    event, run, jobs = case("auth-service", "auth", f"prod-v1.2.3-{source}", "workflow_dispatch")
    jobs["jobs"].append(dict(jobs["jobs"][0]))
    negative.append((event, run, jobs))

    for event, run, jobs in negative:
        try:
            validate(event, run, jobs)
        except ValueError:
            continue
        raise SystemExit("GitOps-ready dispatch self-test accepted an invalid payload or promotion run.")
    print(f"GitOps-ready dispatch contract self-tests passed ({len(positive)} positive, {len(negative)} negative cases).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--event", type=Path)
    parser.add_argument("--promotion-run", type=Path)
    parser.add_argument("--promotion-jobs", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.event is None or args.promotion_run is None or args.promotion_jobs is None:
        parser.error("--event, --promotion-run and --promotion-jobs are required unless --self-test is used.")
    try:
        event = json.loads(args.event.read_text(encoding="utf-8"))
        promotion_run = json.loads(args.promotion_run.read_text(encoding="utf-8"))
        promotion_jobs = json.loads(args.promotion_jobs.read_text(encoding="utf-8"))
        validate(event, promotion_run, promotion_jobs)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"::error::GitOps-ready dispatch validation failed: {exc}", file=sys.stderr)
        return 1
    payload = event["client_payload"]
    print(
        "Validated GitOps-ready dispatch: "
        f"app={payload['app']} component={payload['component']} "
        f"release={payload['release']} promotion_run_id={payload['promotion_run_id']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
