#!/usr/bin/env bash
set -euo pipefail

SOURCE_RUN_ID="${SOURCE_RUN_ID:-}"
SOURCE_WORKFLOW_PATH="${SOURCE_WORKFLOW_PATH:-}"
SOURCE_EVENT="${SOURCE_EVENT:-}"
SOURCE_HEAD_SHA="${SOURCE_HEAD_SHA:-}"
SOURCE_COMMIT="${SOURCE_COMMIT:-}"
RELEASE="${RELEASE:-}"
WEB_DIGEST="${WEB_DIGEST:-}"
SERVICE_DIGEST="${SERVICE_DIGEST:-}"
MAX_ATTEMPTS="${TCE_PROVENANCE_MAX_ATTEMPTS:-12}"
RETRY_DELAY_SECONDS="${TCE_PROVENANCE_RETRY_DELAY_SECONDS:-5}"

fail() {
  echo "::error::$*" >&2
  exit 1
}

[[ "$SOURCE_RUN_ID" =~ ^[0-9]+$ ]] || fail "TCE source run ID must be numeric."
[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/wf-03-tce-production-deploy.yml" ]] || fail "TCE source workflow path is not approved."
[[ "$SOURCE_EVENT" == "workflow_dispatch" ]] || fail "TCE source event must be workflow_dispatch."
[[ "$SOURCE_HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "TCE source head must be a full 40-character SHA."
[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ && "$SOURCE_HEAD_SHA" == "$SOURCE_COMMIT" ]] || fail "TCE source head does not match the published image commit."
[[ "$RELEASE" =~ ^prod-v[0-9]+[.][0-9]+[.][0-9]+-[0-9a-f]{40}$ && "$RELEASE" == *-"$SOURCE_HEAD_SHA" ]] || fail "TCE immutable release tag must contain the full source SHA."
[[ "$WEB_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "TCE web digest must be sha256:<64 lowercase hex>."
[[ "$SERVICE_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "TCE service digest must be sha256:<64 lowercase hex>."
[[ "$MAX_ATTEMPTS" =~ ^[1-9][0-9]*$ ]] || fail "TCE_PROVENANCE_MAX_ATTEMPTS must be a positive integer."
[[ "$RETRY_DELAY_SECONDS" =~ ^[0-9]+$ ]] || fail "TCE_PROVENANCE_RETRY_DELAY_SECONDS must be a non-negative integer."

API_URL="https://api.github.com/repos/phanthienquoc/TCE-dashboard/actions/runs/$SOURCE_RUN_ID"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if ! source_run="$(curl --fail-with-body --silent --show-error \
    --connect-timeout 5 --max-time 15 \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "$API_URL" 2>/dev/null)"; then
    if (( attempt == MAX_ATTEMPTS )); then
      fail "Unable to fetch public TCE source run #$SOURCE_RUN_ID from the GitHub Actions API."
    fi
    echo "Waiting for public TCE source run #$SOURCE_RUN_ID to become visible (attempt $attempt/$MAX_ATTEMPTS)."
    sleep "$RETRY_DELAY_SECONDS"
    continue
  fi

  run_id="$(jq -r '.id // empty' <<< "$source_run")"
  repository="$(jq -r '.repository.full_name // empty' <<< "$source_run")"
  head_repository="$(jq -r '.head_repository.full_name // empty' <<< "$source_run")"
  workflow_path="$(jq -r '.path // empty' <<< "$source_run")"
  event="$(jq -r '.event // empty' <<< "$source_run")"
  branch="$(jq -r '.head_branch // empty' <<< "$source_run")"
  head_sha="$(jq -r '.head_sha // empty' <<< "$source_run")"
  status="$(jq -r '.status // empty' <<< "$source_run")"
  conclusion="$(jq -r '.conclusion // empty' <<< "$source_run")"

  [[ "$run_id" == "$SOURCE_RUN_ID" ]] || fail "GitHub Actions returned a different TCE run ID."
  [[ "$repository" == "phanthienquoc/TCE-dashboard" && "$head_repository" == "phanthienquoc/TCE-dashboard" ]] || fail "TCE source run repository identity does not match."
  [[ "$workflow_path" == "$SOURCE_WORKFLOW_PATH" ]] || fail "TCE source run #$SOURCE_RUN_ID used an unexpected workflow path."
  [[ "$event" == "$SOURCE_EVENT" ]] || fail "TCE source run #$SOURCE_RUN_ID event does not match the dispatch payload."
  [[ "$branch" == "master" ]] || fail "TCE source run #$SOURCE_RUN_ID did not run from master."
  [[ "$head_sha" == "$SOURCE_HEAD_SHA" ]] || fail "TCE source run #$SOURCE_RUN_ID SHA does not match the immutable image commit."

  case "$status" in
    completed)
      [[ "$conclusion" == "success" ]] || fail "TCE publisher run #$SOURCE_RUN_ID completed with conclusion=${conclusion:-missing}; refusing GitOps promotion."
      echo "Verified successful TCE publisher run #$SOURCE_RUN_ID: workflow=$workflow_path event=$event branch=$branch sha=$head_sha release=$RELEASE."
      exit 0
      ;;
    queued|in_progress)
      if (( attempt == MAX_ATTEMPTS )); then
        fail "TCE publisher run #$SOURCE_RUN_ID did not complete within the provenance verification window (status=$status)."
      fi
      echo "Waiting for TCE publisher run #$SOURCE_RUN_ID to complete (attempt $attempt/$MAX_ATTEMPTS; status=$status)."
      sleep "$RETRY_DELAY_SECONDS"
      ;;
    *)
      fail "TCE publisher run #$SOURCE_RUN_ID has unexpected status=${status:-missing}."
      ;;
  esac
done

fail "TCE publisher run #$SOURCE_RUN_ID was not verified."
