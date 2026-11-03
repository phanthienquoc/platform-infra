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
if [[ "$*" == *"/jobs?per_page=100"* ]]; then
  cat "$MOCK_GH_JOBS_RESPONSE_FILE"
  exit 0
fi
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

make_jobs() {
  jq -n '{
    jobs: [
      {name:"Require master for production image publication",status:"completed",conclusion:"success",steps:[
        {name:"Reject non-master release refs",conclusion:"success"}
      ]},
      {name:"Gate production GitOps promotion",status:"completed",conclusion:"success",steps:[
        {name:"Require explicit production promotion enablement",conclusion:"success"}
      ]},
      {name:"build-and-push",status:"completed",conclusion:"success",steps:[
        {name:"Verify native ARM64 runner",conclusion:"success"},
        {name:"Build and push Scraper",conclusion:"success"},
        {name:"Build and push Admin",conclusion:"success"},
        {name:"Build and push Backend",conclusion:"success"},
        {name:"Verify immutable image manifests for ARM64",conclusion:"success"}
      ]},
      {name:"Validate Platform Infra release handoff before promotion",status:"completed",conclusion:"success",steps:[
        {name:"Require token and verify Platform Infra repository access",conclusion:"success"}
      ]},
      {name:"Dispatch atomic StockDividend digest promotion",status:"completed",conclusion:"success",steps:[
        {name:"Dispatch atomic StockDividend digest promotion",conclusion:"success"}
      ]}
    ]
  }'
}

run_validator() {
  rm -f "$tmp_dir/count"
  PATH="$tmp_dir/bin:$PATH" \
    STOCKDIVIDEND_ACTIONS_READ_TOKEN=test-token \
    MOCK_GH_COUNT_FILE="$tmp_dir/count" \
    MOCK_GH_RESPONSE_FILE="$tmp_dir/response.json" \
    MOCK_GH_JOBS_RESPONSE_FILE="$tmp_dir/jobs.json" \
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

make_jobs > "$tmp_dir/jobs.json"

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

# A successful workflow conclusion is insufficient if any critical release-gate/handoff/dispatch step was skipped.
make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Require master for production image publication") | .steps[] | select(.name == "Reject non-master release refs")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "master ref validation step skipped"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Gate production GitOps promotion") | .steps[] | select(.name == "Require explicit production promotion enablement")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "production release gate step skipped"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Validate Platform Infra release handoff before promotion") | .steps[] | select(.name == "Require token and verify Platform Infra repository access")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "Platform Infra access verification step skipped"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Dispatch atomic StockDividend digest promotion") | .steps[] | select(.name == "Dispatch atomic StockDividend digest promotion")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "atomic digest dispatch step skipped"

# A successful workflow conclusion is insufficient if any required publish/handoff job or step did not succeed.
make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Dispatch atomic StockDividend digest promotion")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "release dispatch job skipped"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "build-and-push") | .steps[] | select(.name == "Verify immutable image manifests for ARM64")).conclusion = "failure"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "ARM64 immutable manifest verification failed"

make_jobs > "$tmp_dir/jobs.json"
jq 'del(.jobs[] | select(.name == "Validate Platform Infra release handoff before promotion"))' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "missing release handoff job"

make_jobs > "$tmp_dir/jobs.json"

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

if PATH="$tmp_dir/bin:$PATH" STOCKDIVIDEND_ACTIONS_READ_TOKEN='' \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected missing read-only StockDividend Actions token to fail before API access." >&2
  exit 1
fi

echo "StockDividend publisher-run provenance contract tests passed."
