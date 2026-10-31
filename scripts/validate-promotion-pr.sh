#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"
: "${PR_HEAD_SHA:?PR_HEAD_SHA is required}"
: "${PR_BRANCH:?PR_BRANCH is required}"
: "${REPOSITORY:?REPOSITORY is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

[[ "$PR_HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || {
  echo "::error::Promotion PR head must be a full 40-character SHA."
  exit 1
}
[[ "$PR_BRANCH" == automation/promote-* ]] || {
  echo "::error::Unexpected promotion PR branch: $PR_BRANCH"
  exit 1
}

started_epoch="$(date -u +%s)"
dispatch_payload="$(jq -n --arg ref "$PR_BRANCH" '{ref: $ref}')"
curl --fail --silent --show-error \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$REPOSITORY/actions/workflows/validate-manifests.yml/dispatches" \
  -d "$dispatch_payload" >/dev/null

deadline=$((SECONDS + 900))
validation_run=""
validation_conclusion=""
validation_url=""

while (( SECONDS < deadline )); do
  runs_json="$(curl --fail --silent --show-error -G \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GH_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/$REPOSITORY/actions/workflows/validate-manifests.yml/runs" \
    --data-urlencode "branch=$PR_BRANCH" \
    --data-urlencode "event=workflow_dispatch" \
    --data-urlencode "per_page=20")"

  validation_run="$(jq -c --arg sha "$PR_HEAD_SHA" \
    '[.workflow_runs[]? | select(.head_sha == $sha and .event == "workflow_dispatch")] | sort_by(.created_at) | last // empty' \
    <<< "$runs_json")"

  if [[ -n "$validation_run" ]]; then
    created_at="$(jq -r '.created_at' <<< "$validation_run")"
    created_epoch="$(date -u -d "$created_at" +%s)"
    if (( created_epoch >= started_epoch )); then
      status="$(jq -r '.status' <<< "$validation_run")"
      if [[ "$status" == "completed" ]]; then
        validation_conclusion="$(jq -r '.conclusion // empty' <<< "$validation_run")"
        validation_url="$(jq -r '.html_url' <<< "$validation_run")"
        if [[ "$validation_conclusion" != "success" ]]; then
          echo "::error::Exact-head manifest validation failed for $PR_HEAD_SHA: $validation_url (conclusion=$validation_conclusion)"
          exit 1
        fi
        echo "Exact-head manifest validation passed: $validation_url"
        break
      fi
    fi
  fi
  sleep 10
done

if [[ -z "$validation_run" || "$validation_conclusion" != "success" ]]; then
  echo "::error::Timed out waiting for validate-manifests success on exact promotion PR head $PR_HEAD_SHA; leaving PR open."
  exit 1
fi

pr_json="$(curl --fail --silent --show-error \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$REPOSITORY/pulls/$PR_NUMBER")"

[[ "$(jq -r '.state' <<< "$pr_json")" == "open" ]] || {
  echo "::error::Promotion PR is no longer open; refusing merge."
  exit 1
}
[[ "$(jq -r '.head.sha' <<< "$pr_json")" == "$PR_HEAD_SHA" ]] || {
  echo "::error::Promotion PR head changed after validation; refusing merge."
  exit 1
}
[[ "$(jq -r '.head.ref' <<< "$pr_json")" == "$PR_BRANCH" ]] || {
  echo "::error::Promotion PR branch changed after validation; refusing merge."
  exit 1
}
[[ "$(jq -r '.base.ref' <<< "$pr_json")" == "master" ]] || {
  echo "::error::Promotion PR base is not master; refusing merge."
  exit 1
}

echo "head_sha=$PR_HEAD_SHA" >> "$GITHUB_OUTPUT"
