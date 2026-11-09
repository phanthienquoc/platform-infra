#!/usr/bin/env bash
set -euo pipefail

SOURCE_APP="${SOURCE_APP:-}"
SOURCE_REPOSITORY="${SOURCE_REPOSITORY:-}"
SOURCE_RUN_ID="${SOURCE_RUN_ID:-}"
SOURCE_RUN_ATTEMPT="${SOURCE_RUN_ATTEMPT:-}"
SOURCE_WORKFLOW_PATH="${SOURCE_WORKFLOW_PATH:-}"
SOURCE_EVENT="${SOURCE_EVENT:-}"
SOURCE_HEAD_SHA="${SOURCE_HEAD_SHA:-}"
SOURCE_COMMIT="${SOURCE_COMMIT:-}"
MAX_ATTEMPTS="${TCE_MICROFE_PROVENANCE_MAX_ATTEMPTS:-12}"
RETRY_DELAY_SECONDS="${TCE_MICROFE_PROVENANCE_RETRY_DELAY_SECONDS:-5}"

fail() {
  echo "::error::$*" >&2
  exit 1
}

[[ "$SOURCE_APP" == "microfe" ]] || fail "MicroFE publisher app is not approved."
[[ "$SOURCE_REPOSITORY" == "phanthienquoc/TCE-dashboard" ]] || fail "MicroFE publisher repository is not approved."
[[ "$SOURCE_RUN_ID" =~ ^[0-9]+$ ]] || fail "MicroFE publisher run ID must be numeric."
[[ "$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$ ]] || fail "MicroFE publisher run attempt must be a positive integer."
[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/wf-08b-tce-microfe-build-publish.yml" ]] || fail "MicroFE publisher workflow path is not approved."
[[ "$SOURCE_EVENT" == "push" || "$SOURCE_EVENT" == "workflow_dispatch" ]] || fail "MicroFE publisher event must be push or workflow_dispatch."
[[ "$SOURCE_HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "MicroFE publisher head must be a full 40-character SHA."
[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ && "$SOURCE_HEAD_SHA" == "$SOURCE_COMMIT" ]] || fail "MicroFE publisher head does not match the published image commit."
[[ "$MAX_ATTEMPTS" =~ ^[1-9][0-9]*$ ]] || fail "TCE_MICROFE_PROVENANCE_MAX_ATTEMPTS must be a positive integer."
[[ "$RETRY_DELAY_SECONDS" =~ ^[0-9]+$ ]] || fail "TCE_MICROFE_PROVENANCE_RETRY_DELAY_SECONDS must be a non-negative integer."

API_BASE="https://api.github.com/repos/$SOURCE_REPOSITORY/actions/runs/$SOURCE_RUN_ID"

fetch_json() {
  curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 15 \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "$1"
}

retry_or_fail() {
  local message="$1"
  local attempt="$2"
  if (( attempt == MAX_ATTEMPTS )); then
    fail "$message"
  fi
  echo "$message (attempt $attempt/$MAX_ATTEMPTS); retrying."
  sleep "$RETRY_DELAY_SECONDS"
}

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if ! source_run="$(fetch_json "$API_BASE" 2>/dev/null)"; then
    retry_or_fail "Unable to fetch public TCE MicroFE source run #$SOURCE_RUN_ID." "$attempt"
    continue
  fi

  run_id="$(jq -r '.id // empty' <<< "$source_run")"
  run_attempt="$(jq -r '.run_attempt // empty' <<< "$source_run")"
  repository="$(jq -r '.repository.full_name // empty' <<< "$source_run")"
  head_repository="$(jq -r '.head_repository.full_name // empty' <<< "$source_run")"
  workflow_path="$(jq -r '.path // empty' <<< "$source_run")"
  event="$(jq -r '.event // empty' <<< "$source_run")"
  branch="$(jq -r '.head_branch // empty' <<< "$source_run")"
  head_sha="$(jq -r '.head_sha // empty' <<< "$source_run")"
  status="$(jq -r '.status // empty' <<< "$source_run")"
  conclusion="$(jq -r '.conclusion // empty' <<< "$source_run")"

  [[ "$run_id" == "$SOURCE_RUN_ID" ]] || fail "GitHub Actions returned a different MicroFE source run ID."
  [[ "$run_attempt" == "$SOURCE_RUN_ATTEMPT" ]] || fail "MicroFE source run attempt does not match the dispatch payload."
  [[ "$repository" == "$SOURCE_REPOSITORY" && "$head_repository" == "$SOURCE_REPOSITORY" ]] || fail "MicroFE source run repository identity does not match."
  [[ "$workflow_path" == "$SOURCE_WORKFLOW_PATH" ]] || fail "MicroFE source run #$SOURCE_RUN_ID used an unexpected workflow path."
  [[ "$event" == "$SOURCE_EVENT" ]] || fail "MicroFE source run #$SOURCE_RUN_ID event does not match the dispatch payload."
  [[ "$branch" == "master" ]] || fail "MicroFE source run #$SOURCE_RUN_ID did not run from master."
  [[ "$head_sha" == "$SOURCE_HEAD_SHA" ]] || fail "MicroFE source run #$SOURCE_RUN_ID SHA does not match the immutable image commit."

  case "$status" in
    queued)
      retry_or_fail "MicroFE source run #$SOURCE_RUN_ID is still queued" "$attempt"
      continue
      ;;
    in_progress|completed) ;;
    *)
      fail "MicroFE source run #$SOURCE_RUN_ID has unexpected status=${status:-missing}."
      ;;
  esac

  if [[ "$status" == "completed" && "$conclusion" != "success" ]]; then
    fail "MicroFE publisher run #$SOURCE_RUN_ID completed with conclusion=${conclusion:-missing}; refusing GitOps promotion."
  fi

  if ! jobs_json="$(fetch_json "$API_BASE/jobs?per_page=100" 2>/dev/null)"; then
    retry_or_fail "Unable to fetch jobs for MicroFE source run #$SOURCE_RUN_ID." "$attempt"
    continue
  fi

  jobs_ready=true
  while IFS= read -r job_name; do
    [[ -n "$job_name" ]] || continue
    job="$(jq -c --arg name "$job_name" '[.jobs[] | select(.name == $name)] | last // {}' <<< "$jobs_json")"
    job_status="$(jq -r '.status // empty' <<< "$job")"
    job_conclusion="$(jq -r '.conclusion // empty' <<< "$job")"
    if [[ "$job_status" != "completed" || "$job_conclusion" != "success" ]]; then
      jobs_ready=false
      break
    fi
  done <<'REQUIRED_JOBS'
Test MicroFE Auth
Test MicroFE WebSocket
Validate Platform Infra release handoff credential
Build and publish MicroFE WebSocket image
Build and publish MicroFE Shell image
REQUIRED_JOBS

  [[ "$jobs_ready" == "true" ]] || {
    retry_or_fail "Required MicroFE test/build/publish jobs are not all completed successfully for run #$SOURCE_RUN_ID" "$attempt"
    continue
  }

  dispatch_job="$(jq -c '[.jobs[] | select(.name == "Dispatch immutable image promotion and verify production")] | last // {}' <<< "$jobs_json")"
  dispatch_status="$(jq -r '.status // empty' <<< "$dispatch_job")"
  dispatch_conclusion="$(jq -r '.conclusion // empty' <<< "$dispatch_job")"

  if [[ "$status" == "in_progress" ]]; then
    [[ "$dispatch_status" == "in_progress" ]] || {
      retry_or_fail "MicroFE source run #$SOURCE_RUN_ID has not reached its dispatch-and-verify job" "$attempt"
      continue
    }
  else
    [[ "$dispatch_status" == "completed" && "$dispatch_conclusion" == "success" ]] || {
      fail "Completed MicroFE source run #$SOURCE_RUN_ID did not complete dispatch-and-verify successfully."
    }
  fi

  echo "Verified MicroFE publisher provenance: repository=$repository workflow=$workflow_path event=$event branch=$branch run=$run_id attempt=$run_attempt sha=$head_sha status=$status."
  echo "Verified all required MicroFE tests and immutable image-publish jobs completed successfully."
  exit 0
done

fail "MicroFE publisher run #$SOURCE_RUN_ID was not verified."
