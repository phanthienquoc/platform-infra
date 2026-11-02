#!/usr/bin/env bash
set -euo pipefail

SOURCE_RUN_ID="${SOURCE_RUN_ID:-}"
SOURCE_WORKFLOW_PATH="${SOURCE_WORKFLOW_PATH:-}"
SOURCE_EVENT="${SOURCE_EVENT:-}"
SOURCE_HEAD_SHA="${SOURCE_HEAD_SHA:-}"
SOURCE_COMMIT="${SOURCE_COMMIT:-}"
STOCKDIVIDEND_ACTIONS_READ_TOKEN="${STOCKDIVIDEND_ACTIONS_READ_TOKEN:-}"
MAX_ATTEMPTS="${STOCKDIVIDEND_PROVENANCE_MAX_ATTEMPTS:-12}"
RETRY_DELAY_SECONDS="${STOCKDIVIDEND_PROVENANCE_RETRY_DELAY_SECONDS:-5}"

fail() {
  echo "::error::$*" >&2
  exit 1
}

[[ "$SOURCE_RUN_ID" =~ ^[0-9]+$ ]] || fail "StockDividend source run ID must be numeric."
[[ -n "$STOCKDIVIDEND_ACTIONS_READ_TOKEN" ]] || fail "Configure STOCKDIVIDEND_ACTIONS_READ_TOKEN with Actions: read on the private StockDividend repository."
[[ "$SOURCE_WORKFLOW_PATH" == ".github/workflows/deploy.yml" ]] || fail "StockDividend source workflow path is not approved."
[[ "$SOURCE_EVENT" == "push" || "$SOURCE_EVENT" == "workflow_dispatch" ]] || fail "StockDividend source event must be push or workflow_dispatch."
[[ "$SOURCE_HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "StockDividend source head must be a full 40-character SHA."
[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ && "$SOURCE_HEAD_SHA" == "$SOURCE_COMMIT" ]] || fail "StockDividend source head does not match the published image commit."
[[ "$MAX_ATTEMPTS" =~ ^[1-9][0-9]*$ ]] || fail "STOCKDIVIDEND_PROVENANCE_MAX_ATTEMPTS must be a positive integer."
[[ "$RETRY_DELAY_SECONDS" =~ ^[0-9]+$ ]] || fail "STOCKDIVIDEND_PROVENANCE_RETRY_DELAY_SECONDS must be a non-negative integer."

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if ! source_run="$(GH_TOKEN="$STOCKDIVIDEND_ACTIONS_READ_TOKEN" gh api "repos/phanthienquoc/stockdividend/actions/runs/$SOURCE_RUN_ID" 2>/dev/null)"; then
    if (( attempt == MAX_ATTEMPTS )); then
      fail "Unable to fetch StockDividend source run #$SOURCE_RUN_ID from the GitHub Actions API."
    fi
    echo "Waiting for StockDividend source run #$SOURCE_RUN_ID to become visible (attempt $attempt/$MAX_ATTEMPTS)."
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

  [[ "$run_id" == "$SOURCE_RUN_ID" ]] || fail "GitHub Actions returned a different StockDividend run ID."
  [[ "$repository" == "phanthienquoc/stockdividend" && "$head_repository" == "phanthienquoc/stockdividend" ]] || fail "StockDividend source run repository identity does not match."
  [[ "$workflow_path" == "$SOURCE_WORKFLOW_PATH" ]] || fail "StockDividend source run #$SOURCE_RUN_ID used an unexpected workflow path."
  [[ "$event" == "$SOURCE_EVENT" ]] || fail "StockDividend source run #$SOURCE_RUN_ID event does not match the dispatch payload."
  [[ "$branch" == "master" ]] || fail "StockDividend source run #$SOURCE_RUN_ID did not run from master."
  [[ "$head_sha" == "$SOURCE_HEAD_SHA" ]] || fail "StockDividend source run #$SOURCE_RUN_ID SHA does not match the immutable image commit."

  case "$status" in
    completed)
      [[ "$conclusion" == "success" ]] || fail "StockDividend publisher run #$SOURCE_RUN_ID completed with conclusion=${conclusion:-missing}; refusing GitOps promotion."
      echo "Verified successful StockDividend publisher run #$SOURCE_RUN_ID: workflow=$workflow_path event=$event branch=$branch sha=$head_sha."
      exit 0
      ;;
    queued|in_progress)
      if (( attempt == MAX_ATTEMPTS )); then
        fail "StockDividend publisher run #$SOURCE_RUN_ID did not complete within the provenance verification window (status=$status)."
      fi
      echo "Waiting for StockDividend publisher run #$SOURCE_RUN_ID to complete (attempt $attempt/$MAX_ATTEMPTS; status=$status)."
      sleep "$RETRY_DELAY_SECONDS"
      ;;
    *)
      fail "StockDividend publisher run #$SOURCE_RUN_ID has unexpected status=${status:-missing}."
      ;;
  esac
done

fail "StockDividend publisher run #$SOURCE_RUN_ID was not verified."
