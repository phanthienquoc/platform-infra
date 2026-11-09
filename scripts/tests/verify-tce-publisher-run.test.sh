#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-tce-publisher-run.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/bin"

cat > "$tmp_dir/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
for arg in "$@"; do
  case "$arg" in
    *Authorization*) echo "Unexpected cross-repository credential passed to public TCE API." >&2; exit 4 ;;
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
sample_run_id=123456789
sample_repo=phanthienquoc/TCE-dashboard
sample_path=.github/workflows/wf-03-tce-production-deploy.yml
sample_release="prod-v1.2.3-$sample_sha"
sample_web_digest="sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
sample_service_digest="sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
export WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest"
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
      {name:"Require master for production release",status:"completed",conclusion:"success",steps:[]},
      {name:"Notify Telegram — release started",status:"completed",conclusion:"success",steps:[]},
      {name:"Resolve production image tag",status:"completed",conclusion:"success",steps:[
        {name:"Resolve immutable release tag",conclusion:"success"}
      ]},
      {name:"Build frontend (native ARM64)",status:"completed",conclusion:"success",steps:[
        {name:"Verify native architecture",conclusion:"success"},
        {name:"Build frontend image",conclusion:"success"},
        {name:"Verify frontend architecture",conclusion:"success"},
        {name:"Export and validate frontend image",conclusion:"success"},
        {name:"Upload frontend image",conclusion:"success"}
      ]},
      {name:"Build backend (native ARM64)",status:"completed",conclusion:"success",steps:[
        {name:"Validate backend inputs",conclusion:"success"},
        {name:"Verify native architecture",conclusion:"success"},
        {name:"Build backend image",conclusion:"success"},
        {name:"Verify backend architecture",conclusion:"success"},
        {name:"Export and validate backend image",conclusion:"success"},
        {name:"Upload backend image",conclusion:"success"}
      ]},
      {name:"Publish immutable images and promote platform-infra",status:"completed",conclusion:"success",steps:[
        {name:"Download exact release artifacts",conclusion:"success"},
        {name:"Load and validate exact release images",conclusion:"success"},
        {name:"Login to GHCR",conclusion:"success"},
        {name:"Set up Buildx for registry digest inspection",conclusion:"success"},
        {name:"Publish exact release images",conclusion:"success"},
        {name:"Verify immutable registry digests and ARM64 manifests",conclusion:"success"},
        {name:"Validate TCE release handoff contract",conclusion:"success"},
        {name:"Notify platform-infra",conclusion:"success"},
        {name:"Verify platform-infra release workflow",conclusion:"success"}
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
    RELEASE="$sample_release" \
    WEB_DIGEST="$sample_web_digest" \
    SERVICE_DIGEST="$sample_service_digest" \
    TCE_PROVENANCE_MAX_ATTEMPTS=2 \
    TCE_PROVENANCE_RETRY_DELAY_SECONDS=0 \
    bash "$validator"
}

expect_failure() {
  local label="$1"
  if run_validator >/dev/null 2>&1; then
    echo "Expected TCE provenance validation failure: $label" >&2
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

make_run completed success "$sample_repo" "$sample_repo" "$sample_path" workflow_dispatch master "$sample_sha" 123456790 > "$tmp_dir/response.json"
expect_failure "run ID mismatch"
make_run completed success > "$tmp_dir/response.json"
jq '.run_attempt = 2' "$tmp_dir/response.json" > "$tmp_dir/response-invalid.json" && mv "$tmp_dir/response-invalid.json" "$tmp_dir/response.json"
expect_failure "run attempt mismatch"
make_run completed success > "$tmp_dir/response.json"
jq 'del(.run_attempt)' "$tmp_dir/response.json" > "$tmp_dir/response-invalid.json" && mv "$tmp_dir/response-invalid.json" "$tmp_dir/response.json"
expect_failure "missing run attempt"
make_run completed success another-owner/TCE-dashboard > "$tmp_dir/response.json"
expect_failure "repository mismatch"
make_run completed success "$sample_repo" another-owner/TCE-dashboard > "$tmp_dir/response.json"
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
jq 'del(.jobs[] | select(.name == "Build backend (native ARM64)"))' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "missing backend build job"

make_jobs > "$tmp_dir/jobs.json"
jq '(.jobs[] | select(.name == "Build frontend (native ARM64)")).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "skipped frontend build job"

make_jobs > "$tmp_dir/jobs.json"
jq '.jobs += [.jobs[] | select(.name == "Publish immutable images and promote platform-infra")]' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
expect_failure "duplicate publisher job"

for spec in \
  "Build frontend (native ARM64)|Build frontend image" \
  "Build frontend (native ARM64)|Verify frontend architecture" \
  "Build frontend (native ARM64)|Export and validate frontend image" \
  "Build backend (native ARM64)|Build backend image" \
  "Build backend (native ARM64)|Verify backend architecture" \
  "Build backend (native ARM64)|Export and validate backend image" \
  "Publish immutable images and promote platform-infra|Load and validate exact release images" \
  "Publish immutable images and promote platform-infra|Publish exact release images" \
  "Publish immutable images and promote platform-infra|Verify immutable registry digests and ARM64 manifests" \
  "Publish immutable images and promote platform-infra|Notify platform-infra" \
  "Publish immutable images and promote platform-infra|Verify platform-infra release workflow"; do
  job="${spec%%|*}"
  step="${spec#*|}"
  make_jobs > "$tmp_dir/jobs.json"
  jq --arg job "$job" --arg step "$step" '(.jobs[] | select(.name == $job) | .steps[] | select(.name == $step)).conclusion = "skipped"' "$tmp_dir/jobs.json" > "$tmp_dir/jobs-invalid.json"
  mv "$tmp_dir/jobs-invalid.json" "$tmp_dir/jobs.json"
  expect_failure "skipped required publisher step: $job / $step"
done

make_jobs > "$tmp_dir/jobs.json"
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID=0 SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" RELEASE="$sample_release" \
  WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected zero TCE source run ID to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID=not-a-run SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" RELEASE="$sample_release" \
  WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid TCE source run ID to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=push \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" RELEASE="$sample_release" \
  WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected unsupported TCE source event to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa RELEASE="$sample_release" \
  WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected TCE source commit mismatch to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" RELEASE=prod-v1.2.3-deadbee \
  WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected TCE release/source SHA mismatch to fail before API access." >&2
  exit 1
fi
if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" RELEASE="$sample_release" \
  WEB_DIGEST=sha256:bad SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected malformed TCE web digest to fail before API access." >&2
  exit 1
fi

if PATH="$tmp_dir/bin:$PATH" MOCK_CURL_COUNT_FILE="$tmp_dir/count" MOCK_CURL_RESPONSE_FILE="$tmp_dir/response.json" \
  SOURCE_RUN_ID="$sample_run_id" SOURCE_RUN_ATTEMPT=0 SOURCE_WORKFLOW_PATH="$sample_path" SOURCE_EVENT=workflow_dispatch \
  SOURCE_HEAD_SHA="$sample_sha" SOURCE_COMMIT="$sample_sha" RELEASE="$sample_release" \
  WEB_DIGEST="$sample_web_digest" SERVICE_DIGEST="$sample_service_digest" bash "$validator" >/dev/null 2>&1; then
  echo "Expected invalid TCE source run attempt to fail before API access." >&2
  exit 1
fi

echo "TCE publisher-run provenance, build, immutable GHCR and dispatch contract tests passed."
