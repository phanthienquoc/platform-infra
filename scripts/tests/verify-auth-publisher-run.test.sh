#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-auth-publisher-run.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/bin"

cat > "$tmp_dir/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
for arg in "$@"; do
  case "$arg" in
    *Authorization*) echo "Unexpected cross-repository credential passed to public Auth API." >&2; exit 4 ;;
  esac
done
url="${!#}"
if [[ "$url" == "$MOCK_JOBS_API_URL" ]]; then
  cat "$MOCK_JOBS_RESPONSE_FILE"
  exit 0
fi
[[ "$url" == "$MOCK_API_URL" ]] || exit 5
count=0
[[ -f "$MOCK_CURL_COUNT_FILE" ]] && count="$(cat "$MOCK_CURL_COUNT_FILE")"
count=$((count + 1))
printf '%s' "$count" > "$MOCK_CURL_COUNT_FILE"
if [[ "$count" -eq 1 && -n "${MOCK_CURL_FIRST_RESPONSE:-}" ]]; then
  cat "$MOCK_CURL_FIRST_RESPONSE"
else
  cat "$MOCK_CURL_RESPONSE_FILE"
fi
MOCK
chmod +x "$tmp_dir/bin/curl"

sample_sha=0123456789abcdef0123456789abcdef01234567
sample_run_id=42000000001
sample_repo=phanthienquoc/phanthienquoc-authentication
sample_path=.github/workflows/release.yml
sample_api_url="https://api.github.com/repos/$sample_repo/actions/runs/$sample_run_id"

make_run() {
  local status="$1"
  local conclusion="$2"
  local repo="${3:-$sample_repo}"
  local head_repo="${4:-$sample_repo}"
  local path="${5:-$sample_path}"
  local event="${6:-workflow_dispatch}"
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
  jq -n '{
    jobs: [
      {name:"Verify auth service",status:"completed",conclusion:"success",steps:[
        {name:"Run npm install --package-lock-only --ignore-scripts --no-audit --no-fund",conclusion:"success"},
        {name:"Run npm ci --ignore-scripts --no-audit --no-fund",conclusion:"success"},
        {name:"Run npm test",conclusion:"success"},
        {name:"Run npm run typecheck",conclusion:"success"},
        {name:"Run npm run build",conclusion:"success"}
      ]},
      {name:"Build and publish ARM64 image with version and SHA tags",status:"completed",conclusion:"success",steps:[
        {name:"Validate release and promotion contract",conclusion:"success"},
        {name:"Build and publish image",conclusion:"success"},
        {name:"Verify published digest and ARM64 manifest",conclusion:"success"},
        {name:"Request Auth image promotion in platform-infra",conclusion:"success"}
      ]}
    ]
  }'
}

run_validator() {
  rm -f "$tmp_dir/count"
  PATH="$tmp_dir/bin:$PATH" \
    MOCK_CURL_COUNT_FILE="$tmp_dir/count" \
    MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
    MOCK_JOBS_API_URL="$sample_api_url/jobs?per_page=100" \
    MOCK_JOBS_RESPONSE_FILE="$tmp_dir/jobs.json" \
    MOCK_CURL_FIRST_RESPONSE="${MOCK_CURL_FIRST_RESPONSE:-}" \
    MOCK_API_URL="$sample_api_url" \
    SOURCE_RUN_ID="$sample_run_id" \
    SOURCE_RUN_ATTEMPT=1 \
    SOURCE_WORKFLOW_PATH="$sample_path" \
    SOURCE_EVENT=workflow_dispatch \
    SOURCE_HEAD_SHA="$sample_sha" \
    SOURCE_COMMIT="$sample_sha" \
    AUTH_PROVENANCE_MAX_ATTEMPTS=2 \
    AUTH_PROVENANCE_RETRY_DELAY_SECONDS=0 \
    bash "$validator"
}

expect_failure() {
  local label="$1"
  if run_validator >/dev/null 2>&1; then
    echo "Expected Auth provenance validation failure: $label" >&2
    exit 1
  fi
}

make_jobs > "$tmp_dir/jobs.json"
make_run in_progress "" > "$tmp_dir/in-progress.json"
make_run completed success > "$tmp_dir/response.json"
MOCK_CURL_FIRST_RESPONSE="$tmp_dir/in-progress.json" run_validator >/dev/null
[[ "$(cat "$tmp_dir/count")" == "2" ]]

make_run completed success > "$tmp_dir/response.json"
unset MOCK_CURL_FIRST_RESPONSE
run_validator >/dev/null

make_run completed success "$sample_repo" "$sample_repo" "$sample_path" workflow_dispatch master "$sample_sha" 42000000002 > "$tmp_dir/response.json"
expect_failure "run ID mismatch"
make_run completed success > "$tmp_dir/response.json"
jq '.run_attempt = 2' "$tmp_dir/response.json" > "$tmp_dir/response-invalid.json" && mv "$tmp_dir/response-invalid.json" "$tmp_dir/response.json"
expect_failure "run attempt mismatch"
make_run completed success > "$tmp_dir/response.json"
jq 'del(.run_attempt)' "$tmp_dir/response.json" > "$tmp_dir/response-invalid.json" && mv "$tmp_dir/response-invalid.json" "$tmp_dir/response.json"
expect_failure "missing run attempt"
make_run completed success another-owner/authentication > "$tmp_dir/response.json"
expect_failure "repository mismatch"
make_run completed success "$sample_repo" another-owner/authentication > "$tmp_dir/response.json"
expect_failure "head repository mismatch"
make_run completed success "$sample_repo" "$sample_repo" .github/workflows/other.yml > "$tmp_dir/response.json"
expect_failure "workflow path mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push > "$tmp_dir/response.json"
expect_failure "event mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" workflow_dispatch main > "$tmp_dir/response.json"
expect_failure "branch mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" workflow_dispatch master aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa > "$tmp_dir/response.json"
expect_failure "SHA mismatch"
make_run completed failure > "$tmp_dir/response.json"
expect_failure "failed publisher conclusion"

make_run completed success > "$tmp_dir/response.json"
make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Verify auth service")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "skipped application verification job"

for required_step in \
  "Run npm install --package-lock-only --ignore-scripts --no-audit --no-fund" \
  "Run npm ci --ignore-scripts --no-audit --no-fund" \
  "Run npm test" \
  "Run npm run typecheck" \
  "Run npm run build"; do
  make_jobs > "$tmp_dir/jobs.json"
  jq --arg step "$required_step" '(.jobs[] | select(.name == "Verify auth service") | .steps[] | select(.name == $step)).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
  mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
  expect_failure "skipped Auth verification step: $required_step"
done

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Build and publish ARM64 image with version and SHA tags") | .steps[] | select(.name == "Build and publish image")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "skipped image publication step"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Build and publish ARM64 image with version and SHA tags") | .steps[] | select(.name == "Verify published digest and ARM64 manifest")).conclusion = "failure"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "failed digest and ARM64 verification step"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Build and publish ARM64 image with version and SHA tags") | .steps[] | select(.name == "Request Auth image promotion in platform-infra")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "skipped Platform dispatch step"

make_jobs > "$tmp_dir/jobs.json"
jq '.jobs += [.jobs[] | select(.name == "Build and publish ARM64 image with version and SHA tags")]' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "duplicate publisher job"

make_jobs > "$tmp_dir/jobs.json"
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID=not-a-run SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid Auth source run ID to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" bash "$validator" >/dev/null 2>&1; then
  echo "Expected unsupported Auth source event to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa bash "$validator" >/dev/null 2>&1; then
  echo "Expected Auth source commit mismatch to fail before API access." >&2
  exit 1
fi

if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_RUN_ATTEMPT=0 SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid Auth source run attempt to fail before API access." >&2
  exit 1
fi

echo "Auth publisher-run provenance contract tests passed."
