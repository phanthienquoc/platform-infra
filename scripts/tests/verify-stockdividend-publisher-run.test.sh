#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-stockdividend-publisher-run.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/bin"

cat > "$tmp_dir/bin/gh" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
[[ "${1:-}" == "api" ]] || exit 2
[[ "${GH_TOKEN:-}" == "test-token" ]] || exit 3
count=0
[[ -f "$MOCK_GH_COUNT_FILE" ]] && count="$(cat "$MOCK_GH_COUNT_FILE")"
count=$((count + 1))
printf '%s' "$count" > "$MOCK_GH_COUNT_FILE"
if [[ "$count" -eq 1 && -n "${MOCK_GH_FIRST_RESPONSE:-}" ]]; then
  cat "$MOCK_GH_FIRST_RESPONSE"
else
  cat "$MOCK_GH_RESPONSE_FILE"
fi
MOCK
chmod +x "$tmp_dir/bin/gh"

sample_sha=0123456789abcdef0123456789abcdef01234567
sample_run_id=41314359012
sample_repo=phanthienquoc/stockdividend
sample_path=.github/workflows/deploy.yml

make_run() {
  local status="$1"
  local conclusion="$2"
  local repo="${3:-$sample_repo}"
  local path="${4:-$sample_path}"
  local event="${5:-push}"
  local branch="${6:-master}"
  local sha="${7:-$sample_sha}"
  local id="${8:-$sample_run_id}"
  jq -n \
    --arg id "$id" \
    --arg repo "$repo" \
    --arg path "$path" \
    --arg event "$event" \
    --arg branch "$branch" \
    --arg sha "$sha" \
    --arg status "$status" \
    --arg conclusion "$conclusion" \
    '{id:($id|tonumber),repository:{full_name:$repo},head_repository:{full_name:$repo},path:$path,event:$event,head_branch:$branch,head_sha:$sha,status:$status,conclusion:$conclusion}'
}

run_validator() {
  rm -f "$tmp_dir/count"
  PATH="$tmp_dir/bin:$PATH" \
    STOCKDIVIDEND_ACTIONS_READ_TOKEN=test-token \
    MOCK_GH_COUNT_FILE="$tmp_dir/count" \
    MOCK_GH_RESPONSE_FILE="$tmp_dir/response.json" \
    MOCK_GH_FIRST_RESPONSE="${MOCK_GH_FIRST_RESPONSE:-}" \
    SOURCE_RUN_ID="$sample_run_id" \
    SOURCE_WORKFLOW_PATH="$sample_path" \
    SOURCE_EVENT=push \
    SOURCE_HEAD_SHA="$sample_sha" \
    SOURCE_COMMIT="$sample_sha" \
    STOCKDIVIDEND_PROVENANCE_MAX_ATTEMPTS=2 \
    STOCKDIVIDEND_PROVENANCE_RETRY_DELAY_SECONDS=0 \
    bash "$validator"
}

expect_failure() {
  local label="$1"
  if run_validator >/dev/null 2>&1; then
    echo "Expected provenance validation failure: $label" >&2
    exit 1
  fi
}

# A source run that is still in progress must be polled until its successful completion.
make_run in_progress "" > "$tmp_dir/in-progress.json"
make_run completed success > "$tmp_dir/response.json"
MOCK_GH_FIRST_RESPONSE="$tmp_dir/in-progress.json" run_validator >/dev/null
[[ "$(cat "$tmp_dir/count")" == "2" ]]

# A completed successful publisher run is accepted.
make_run completed success > "$tmp_dir/response.json"
unset MOCK_GH_FIRST_RESPONSE
run_validator >/dev/null

# Every identity field and the final conclusion are fail-closed.
make_run completed success "$sample_repo" "$sample_path" push master "$sample_sha" 41314359013 > "$tmp_dir/response.json"
expect_failure "run ID mismatch"
make_run completed success another-owner/stockdividend > "$tmp_dir/response.json"
expect_failure "repository mismatch"
make_run completed success "$sample_repo" .github/workflows/other.yml > "$tmp_dir/response.json"
expect_failure "workflow path mismatch"
make_run completed success "$sample_repo" "$sample_path" workflow_dispatch > "$tmp_dir/response.json"
expect_failure "event mismatch"
make_run completed success "$sample_repo" "$sample_path" push main > "$tmp_dir/response.json"
expect_failure "branch mismatch"
make_run completed success "$sample_repo" "$sample_path" push master aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa > "$tmp_dir/response.json"
expect_failure "SHA mismatch"
make_run completed failure > "$tmp_dir/response.json"
expect_failure "failed publisher conclusion"

if PATH="$tmp_dir/bin:$PATH" STOCKDIVIDEND_ACTIONS_READ_TOKEN=test-token \
  SOURCE_RUN_ID=not-a-run SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid source run ID to fail before API access." >&2
  exit 1
fi

if PATH="$tmp_dir/bin:$PATH" STOCKDIVIDEND_ACTIONS_READ_TOKEN=test-token \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=schedule \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected unsupported source event to fail before API access." >&2
  exit 1
fi

if PATH="$tmp_dir/bin:$PATH" STOCKDIVIDEND_ACTIONS_READ_TOKEN= \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected missing read-only StockDividend Actions token to fail before API access." >&2
  exit 1
fi

echo "StockDividend publisher-run provenance contract tests passed."
