#!/usr/bin/env bash
set -euo pipefail

SOURCE_RUN_ID="${SOURCE_RUN_ID:-}"
SOURCE_RUN_ATTEMPT="${SOURCE_RUN_ATTEMPT:-}"
SOURCE_WORKFLOW_PATH="${SOURCE_WORKFLOW_PATH:-}"
SOURCE_EVENT="${SOURCE_EVENT:-}"
SOURCE_HEAD_SHA="${SOURCE_HEAD_SHA:-}"
SOURCE_COMMIT="${SOURCE_COMMIT:-}"
MAX_ATTEMPTS="${AUTH_PROVENANCE_MAX_ATTEMPTS:-12}"
RETRY_DELAY_SECONDS="${AUTH_PROVENANCE_RETRY_DELAY_SECONDS:-5}"

fail() {
  echo "::error::$*" >&2
  exit 1
}

[[ "$SOURCE_RUN_ID" =~ ^[1-9][0-9]*$ ]] || fail "Auth source run ID must be a positive integer."
[[ "$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$ ]] || fail "Auth source run attempt must be a positive integer."
[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/release.yml" ]] || fail "Auth source workflow path is not approved."
[[ "$SOURCE_EVENT" == "workflow_dispatch" ]] || fail "Auth production publisher must originate from workflow_dispatch."
[[ "$SOURCE_HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "Auth source head must be a full 40-character SHA."
[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ && "$SOURCE_HEAD_SHA" == "$SOURCE_COMMIT" ]] || fail "Auth source head does not match the published image commit."
[[ "$MAX_ATTEMPTS" =~ ^[1-9][0-9]*$ ]] || fail "AUTH_PROVENANCE_MAX_ATTEMPTS must be a positive integer."
[[ "$RETRY_DELAY_SECONDS" =~ ^[0-9]+$ ]] || fail "AUTH_PROVENANCE_RETRY_DELAY_SECONDS must be a non-negative integer."

API_URL="https://api.github.com/repos/phanthienquoc/phanthienquoc-authentication/actions/runs/$SOURCE_RUN_ID"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if ! source_run="$(curl --fail-with-body --silent --show-error \
    --connect-timeout 5 --max-time 15 \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "$API_URL" 2>/dev/null)"; then
    if (( attempt == MAX_ATTEMPTS )); then
      fail "Unable to fetch public Auth source run #$SOURCE_RUN_ID from the GitHub Actions API."
    fi
    echo "Waiting for public Auth source run #$SOURCE_RUN_ID to become visible (attempt $attempt/$MAX_ATTEMPTS)."
    sleep "$RETRY_DELAY_SECONDS"
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

  [[ "$run_id" == "$SOURCE_RUN_ID" ]] || fail "GitHub Actions returned a different Auth run ID."
  [[ "$run_attempt" == "$SOURCE_RUN_ATTEMPT" ]] || fail "Auth source run attempt does not match the dispatch payload."
  [[ "$repository" == "phanthienquoc/phanthienquoc-authentication" && "$head_repository" == "phanthienquoc/phanthienquoc-authentication" ]] || fail "Auth source run repository identity does not match."
  [[ "$workflow_path" == "$SOURCE_WORKFLOW_PATH" ]] || fail "Auth source run #$SOURCE_RUN_ID used an unexpected workflow path."
  [[ "$event" == "$SOURCE_EVENT" ]] || fail "Auth source run #$SOURCE_RUN_ID event does not match the dispatch payload."
  [[ "$branch" == "master" ]] || fail "Auth source run #$SOURCE_RUN_ID did not run from master."
  [[ "$head_sha" == "$SOURCE_HEAD_SHA" ]] || fail "Auth source run #$SOURCE_RUN_ID SHA does not match the immutable image commit."

  case "$status" in
    completed)
      [[ "$conclusion" == "success" ]] || fail "Auth publisher run #$SOURCE_RUN_ID completed with conclusion=${conclusion:-missing}; refusing GitOps promotion."

      jobs_api_url="$API_URL/jobs?per_page=100"
      if ! jobs_response="$(curl --fail-with-body --silent --show-error \
        --connect-timeout 5 --max-time 15 \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "$jobs_api_url" 2>/dev/null)"; then
        fail "Unable to fetch Auth source run #$SOURCE_RUN_ID job evidence from the public GitHub Actions API."
      fi

      verify_job_success() {
        local expected_name="$1"
        local job
        job="$(jq -c --arg name "$expected_name" '[.jobs[]? | select(.name == $name)] | if length == 1 then .[0] else empty end' <<< "$jobs_response")"
        [[ -n "$job" ]] || fail "Auth publisher run #$SOURCE_RUN_ID is missing or duplicates required job: $expected_name."
        local job_status job_conclusion
        job_status="$(jq -r '.status // empty' <<< "$job")"
        job_conclusion="$(jq -r '.conclusion // empty' <<< "$job")"
        [[ "$job_status" == "completed" && "$job_conclusion" == "success" ]] || fail "Auth publisher job '$expected_name' is not completed-success (status=$job_status conclusion=$job_conclusion)."
      }

      verify_step_success() {
        local job_name="$1"
        local expected_step="$2"
        local step
        step="$(jq -c --arg job "$job_name" --arg name "$expected_step" '[.jobs[]? | select(.name == $job) | .steps[]? | select(.name == $name)] | if length == 1 then .[0] else empty end' <<< "$jobs_response")"
        [[ -n "$step" ]] || fail "Auth publisher run #$SOURCE_RUN_ID is missing or duplicates required step '$expected_step' in '$job_name'."
        local step_conclusion
        step_conclusion="$(jq -r '.conclusion // empty' <<< "$step")"
        [[ "$step_conclusion" == "success" ]] || fail "Auth publisher step '$expected_step' in '$job_name' did not succeed (conclusion=$step_conclusion)."
      }

      verify_job_success "Verify auth service"
      verify_step_success "Verify auth service" "Run npm install --package-lock-only --ignore-scripts --no-audit --no-fund"
      verify_step_success "Verify auth service" "Run npm ci --ignore-scripts --no-audit --no-fund"
      verify_step_success "Verify auth service" "Run npm test"
      verify_step_success "Verify auth service" "Run npm run typecheck"
      verify_step_success "Verify auth service" "Run npm run build"
      verify_job_success "Build and publish ARM64 image with version and SHA tags"
      verify_step_success "Build and publish ARM64 image with version and SHA tags" "Validate release and promotion contract"
      verify_step_success "Build and publish ARM64 image with version and SHA tags" "Build and publish image"
      verify_step_success "Build and publish ARM64 image with version and SHA tags" "Verify published digest and ARM64 manifest"
      verify_step_success "Build and publish ARM64 image with version and SHA tags" "Request Auth image promotion in platform-infra"

      echo "Verified successful Auth publisher run #$SOURCE_RUN_ID attempt=$run_attempt: workflow=$workflow_path event=$event branch=$branch sha=$head_sha; application verification, ARM64 publication, digest validation and Platform dispatch succeeded."
      exit 0
      ;;
    queued|in_progress)
      if (( attempt == MAX_ATTEMPTS )); then
        fail "Auth publisher run #$SOURCE_RUN_ID did not complete within the provenance verification window (status=$status)."
      fi
      echo "Waiting for Auth publisher run #$SOURCE_RUN_ID to complete (attempt $attempt/$MAX_ATTEMPTS; status=$status)."
      sleep "$RETRY_DELAY_SECONDS"
      ;;
    *)
      fail "Auth publisher run #$SOURCE_RUN_ID has unexpected status=${status:-missing}."
      ;;
  esac
done

fail "Auth publisher run #$SOURCE_RUN_ID was not verified."
