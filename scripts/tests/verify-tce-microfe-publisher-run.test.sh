#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-tce-microfe-publisher-run.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/bin"

cat > "$tmp_dir/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
for arg in "$@"; do
  case "$arg" in
    Authorization*) echo "Unexpected credential passed to public TCE Actions API." >&2; exit 4 ;;
  esac
done
url="${!#}"
case "$url" in
  "$MOCK_RUN_URL") cat "$MOCK_RUN_FILE" ;;
  "$MOCK_JOBS_URL") cat "$MOCK_JOBS_FILE" ;;
  *) echo "Unexpected URL: $url" >&2; exit 5 ;;
esac
MOCK
chmod +x "$tmp_dir/bin/curl"

sample_sha=0123456789abcdef0123456789abcdef01234567
sample_run_id=41154490073
sample_repo=phanthienquoc/TCE-dashboard
sample_path=.github/workflows/wf-08b-tce-microfe-build-publish.yml
sample_run_url="https://api.github.com/repos/$sample_repo/actions/runs/$sample_run_id"
sample_jobs_url="$sample_run_url/jobs?per_page=100"

make_run() {
  local status="$1"
  local conclusion="$2"
  local repo="${3:-$sample_repo}"
  local head_repo="${4:-$sample_repo}"
  local path="${5:-$sample_path}"
  local event="${6:-push}"
  local branch="${7:-master}"
  local sha="${8:-$sample_sha}"
  local id="${9:-$sample_run_id}"
  local run_attempt="${10:-1}"
  jq -n \
    --arg id "$id" \
    --arg run_attempt "$run_attempt" \
    --arg repo "$repo" \
    --arg head_repo "$head_repo" \
    --arg path "$path" \
    --arg event "$event" \
    --arg branch "$branch" \
    --arg sha "$sha" \
    --arg status "$status" \
    --arg conclusion "$conclusion" \
    '{id:($id|tonumber),run_attempt:($run_attempt|tonumber),repository:{full_name:$repo},head_repository:{full_name:$head_repo},path:$path,event:$event,head_branch:$branch,head_sha:$sha,status:$status,conclusion:$conclusion}'
}

make_jobs() {
  local build_conclusion="${1:-success}"
  local dispatch_status="${2:-in_progress}"
  local dispatch_conclusion="${3:-}"
  jq -n \
    --arg build_conclusion "$build_conclusion" \
    --arg dispatch_status "$dispatch_status" \
    --arg dispatch_conclusion "$dispatch_conclusion" '
    {jobs:[
      {name:"Test MicroFE Auth",status:"completed",conclusion:"success"},
      {name:"Test MicroFE WebSocket",status:"completed",conclusion:"success"},
      {name:"Validate Platform Infra release handoff credential",status:"completed",conclusion:"success"},
      {name:"Build and publish MicroFE WebSocket image",status:"completed",conclusion:$build_conclusion},
      {name:"Build and publish MicroFE Shell image",status:"completed",conclusion:"success"},
      {name:"Dispatch immutable image promotion and verify production",status:$dispatch_status,conclusion:(if $dispatch_conclusion == "" then null else $dispatch_conclusion end)}
    ]}'
}

run_validator() {
  PATH="$tmp_dir/bin:$PATH" \
    MOCK_RUN_FILE="$tmp_dir/run.json" \
    MOCK_JOBS_FILE="$tmp_dir/jobs.json" \
    MOCK_RUN_URL="$sample_run_url" \
    MOCK_JOBS_URL="$sample_jobs_url" \
    SOURCE_APP=microfe \
    SOURCE_REPOSITORY="$sample_repo" \
    SOURCE_RUN_ID="$sample_run_id" \
    SOURCE_RUN_ATTEMPT=1 \
    SOURCE_WORKFLOW_PATH="$sample_path" \
    SOURCE_EVENT=push \
    SOURCE_HEAD_SHA="$sample_sha" \
    SOURCE_COMMIT="$sample_sha" \
    TCE_MICROFE_PROVENANCE_MAX_ATTEMPTS=1 \
    TCE_MICROFE_PROVENANCE_RETRY_DELAY_SECONDS=0 \
    bash "$validator"
}

expect_failure() {
  local label="$1"
  if run_validator >/dev/null 2>&1; then
    echo "Expected MicroFE provenance validation failure: $label" >&2
    exit 1
  fi
}

# A running source workflow is accepted only after every test/build/publish job
# succeeded and the dispatch-and-verify job is actually in progress.
make_run in_progress "" > "$tmp_dir/run.json"
make_jobs success in_progress > "$tmp_dir/jobs.json"
run_validator >/dev/null

# A completed successful publisher run is accepted only when dispatch verification passed.
make_run completed success > "$tmp_dir/run.json"
make_jobs success completed success > "$tmp_dir/jobs.json"
run_validator >/dev/null

# Reject mismatched source identity and event provenance.
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push master "$sample_sha" 41246414187 > "$tmp_dir/run.json"
expect_failure "run ID mismatch"
make_run completed success > "$tmp_dir/run.json"
jq '.run_attempt = 2' "$tmp_dir/run.json" > "$tmp_dir/run-invalid.json" && mv "$tmp_dir/run-invalid.json" "$tmp_dir/run.json"
expect_failure "run attempt mismatch"
make_run completed success > "$tmp_dir/run.json"
jq 'del(.run_attempt)' "$tmp_dir/run.json" > "$tmp_dir/run-invalid.json" && mv "$tmp_dir/run-invalid.json" "$tmp_dir/run.json"
expect_failure "missing run attempt"
make_run completed success another-owner/TCE-dashboard > "$tmp_dir/run.json"
expect_failure "repository mismatch"
make_run completed success "$sample_repo" another-owner/TCE-dashboard > "$tmp_dir/run.json"
expect_failure "head repository mismatch"
make_run completed success "$sample_repo" "$sample_repo" .github/workflows/other.yml > "$tmp_dir/run.json"
expect_failure "workflow path mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" workflow_dispatch > "$tmp_dir/run.json"
expect_failure "event mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push main > "$tmp_dir/run.json"
expect_failure "branch mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push master aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa > "$tmp_dir/run.json"
expect_failure "SHA mismatch"
make_run completed failure > "$tmp_dir/run.json"
expect_failure "failed source run"

# Reject missing/failed publisher jobs and an in-progress run that has not reached dispatch.
make_run in_progress "" > "$tmp_dir/run.json"
make_jobs failure in_progress > "$tmp_dir/jobs.json"
expect_failure "failed image build"
make_jobs success queued > "$tmp_dir/jobs.json"
expect_failure "dispatch job not in progress"
make_run completed success > "$tmp_dir/run.json"
make_jobs success completed failure > "$tmp_dir/jobs.json"
expect_failure "failed dispatch verification"

# Invalid payload values must fail before the public API is queried.
if PATH="$tmp_dir/bin:$PATH" \
  SOURCE_APP=other SOURCE_REPOSITORY="$sample_repo" SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" \
  SOURCE_EVENT=push SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid MicroFE source app to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" \
  SOURCE_REPOSITORY="$sample_repo" SOURCE_RUN_ID=not-a-run SOURCE_WORKFLOW_PATH="$sample_path" \
  SOURCE_EVENT=push SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid MicroFE source run ID to fail before API access." >&2
  exit 1
fi

if PATH="$tmp_dir/bin:$PATH" \
  SOURCE_REPOSITORY="$sample_repo" SOURCE_RUN_ID=0 SOURCE_WORKFLOW_PATH="$sample_path" \
  SOURCE_EVENT=push SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected zero MicroFE source run ID to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" \
  SOURCE_REPOSITORY="$sample_repo" SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" \
  SOURCE_EVENT=schedule SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected unsupported MicroFE source event to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" \
  SOURCE_REPOSITORY="$sample_repo" SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" \
  SOURCE_EVENT=push SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected MicroFE source commit mismatch to fail before API access." >&2
  exit 1
fi

if PATH="$tmp_dir/bin:$PATH" \
  SOURCE_APP=microfe SOURCE_REPOSITORY="$sample_repo" SOURCE_RUN_ID="$sample_run_id" SOURCE_RUN_ATTEMPT=0 SOURCE_WORKFLOW_PATH="$sample_path" \
  SOURCE_EVENT=push SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid MicroFE source run attempt to fail before API access." >&2
  exit 1
fi

echo "MicroFE publisher-run provenance contract tests passed."
