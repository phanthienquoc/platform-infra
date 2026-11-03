#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-media-publisher-run.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/bin"

cat > "$tmp_dir/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
for arg in "$@"; do
  case "$arg" in
    *Authorization*) echo "Unexpected cross-repository credential passed to public Media API." >&2; exit 4 ;;
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
sample_run_id=41158598649
sample_repo=phanthienquoc/media-generation
sample_path=.github/workflows/wf-03-media-production-deploy.yml
sample_api_url="https://api.github.com/repos/$sample_repo/actions/runs/$sample_run_id"

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
  jq -n \
    --arg id "$id" \
    --arg repo "$repo" \
    --arg head_repo "$head_repo" \
    --arg path "$path" \
    --arg event "$event" \
    --arg branch "$branch" \
    --arg sha "$sha" \
    --arg status "$status" \
    --arg conclusion "$conclusion" \
    '{id:($id|tonumber),repository:{full_name:$repo},head_repository:{full_name:$head_repo},path:$path,event:$event,head_branch:$branch,head_sha:$sha,status:$status,conclusion:$conclusion}'
}

make_jobs() {
  jq -n '{
    jobs: [
      {name:"Require master for production release",status:"completed",conclusion:"success"},
      {name:"Resolve production image tag",status:"completed",conclusion:"success"},
      {name:"Build frontend (native ARM64)",status:"completed",conclusion:"success",steps:[
        {name:"Verify native architecture",conclusion:"success"},
        {name:"Build frontend image",conclusion:"success"},
        {name:"Verify frontend architecture",conclusion:"success"},
        {name:"Export and validate frontend image",conclusion:"success"}
      ]},
      {name:"Build backend (native ARM64)",status:"completed",conclusion:"success",steps:[
        {name:"Validate backend inputs",conclusion:"success"},
        {name:"Verify native architecture",conclusion:"success"},
        {name:"Build backend image",conclusion:"success"},
        {name:"Verify backend architecture",conclusion:"success"},
        {name:"Export and validate backend image",conclusion:"success"}
      ]},
      {name:"Publish immutable images and promote platform-infra",status:"completed",conclusion:"success",steps:[
        {name:"Load and validate exact release images",conclusion:"success"},
        {name:"Publish exact release images",conclusion:"success"},
        {name:"Verify immutable registry digests and ARM64 manifests",conclusion:"success"},
        {name:"Notify platform-infra",conclusion:"success"}
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
    SOURCE_WORKFLOW_PATH="$sample_path" \
    SOURCE_EVENT=push \
    SOURCE_HEAD_SHA="$sample_sha" \
    SOURCE_COMMIT="$sample_sha" \
    MEDIA_PROVENANCE_MAX_ATTEMPTS=2 \
    MEDIA_PROVENANCE_RETRY_DELAY_SECONDS=0 \
    bash "$validator"
}

expect_failure() {
  local label="$1"
  if run_validator >/dev/null 2>&1; then
    echo "Expected Media provenance validation failure: $label" >&2
    exit 1
  fi
}

make_jobs > "$tmp_dir/jobs.json"

# A publisher still in progress must be polled until successful completion.
make_run in_progress "" > "$tmp_dir/in-progress.json"
make_run completed success > "$tmp_dir/response.json"
MOCK_CURL_FIRST_RESPONSE="$tmp_dir/in-progress.json" run_validator >/dev/null
[[ "$(cat "$tmp_dir/count")" == "2" ]]

# A completed successful publisher run is accepted.
make_run completed success > "$tmp_dir/response.json"
unset MOCK_CURL_FIRST_RESPONSE
run_validator >/dev/null

# Every source identity field and final conclusion must fail closed.
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push master "$sample_sha" 41246414187 > "$tmp_dir/response.json"
expect_failure "run ID mismatch"
make_run completed success another-owner/media-generation > "$tmp_dir/response.json"
expect_failure "repository mismatch"
make_run completed success "$sample_repo" another-owner/media-generation > "$tmp_dir/response.json"
expect_failure "head repository mismatch"
make_run completed success "$sample_repo" "$sample_repo" .github/workflows/other.yml > "$tmp_dir/response.json"
expect_failure "workflow path mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" workflow_dispatch > "$tmp_dir/response.json"
expect_failure "event mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push main > "$tmp_dir/response.json"
expect_failure "branch mismatch"
make_run completed success "$sample_repo" "$sample_repo" "$sample_path" push master aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa > "$tmp_dir/response.json"
expect_failure "SHA mismatch"
make_run completed failure > "$tmp_dir/response.json"
expect_failure "failed publisher conclusion"

# A successful run must still prove both native ARM64 builds and the exact digest/dispatch steps.
make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Publish immutable images and promote platform-infra") | .steps[] | select(.name == "Verify immutable registry digests and ARM64 manifests")).conclusion = "failure"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "immutable GHCR digest verification failed"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Build backend (native ARM64)")).conclusion = "failure"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "backend ARM64 build failed"

make_jobs > "$tmp_dir/jobs.json"
jq 'del(.jobs[] | select(.name == "Publish immutable images and promote platform-infra"))' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "missing Platform publication/dispatch job"

make_jobs > "$tmp_dir/jobs.json"

# Invalid payload values must fail before any public API request.
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID=not-a-run SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid Media source run ID to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=schedule \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected unsupported Media source event to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  bash "$validator" >/dev/null 2>&1; then
  echo "Expected Media source commit mismatch to fail before API access." >&2
  exit 1
fi

echo "Media publisher-run provenance contract tests passed."
