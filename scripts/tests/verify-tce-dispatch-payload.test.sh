#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-tce-dispatch-payload.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
event_file="$tmp_dir/event.json"

sample_sha=0123456789abcdef0123456789abcdef01234567
sample_web_digest=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
sample_service_digest=sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

make_valid() {
  jq -n \
    --arg sha "$sample_sha" \
    --arg web_digest "$sample_web_digest" \
    --arg service_digest "$sample_service_digest" \
    '{
      action: "tce-release-requested",
      client_payload: {
        app: "tce-dashboard",
        release: ("prod-v1.2.3-" + $sha),
        web_digest: $web_digest,
        service_digest: $service_digest,
        source_run_id: "42670000001",
        source_run_attempt: "1",
        source_workflow_path: ".github/workflows/wf-03-tce-production-deploy.yml",
        source_event: "workflow_dispatch",
        source_head_sha: $sha
      }
    }' > "$event_file"
}

expect_failure() {
  local label="$1"
  if bash "$validator" "$event_file" >/dev/null 2>&1; then
    echo "Expected TCE dispatch payload rejection: $label" >&2
    exit 1
  fi
}

make_valid
bash "$validator" "$event_file" >/dev/null

make_valid
jq '.action = "unexpected-action"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "wrong repository-dispatch action"

make_valid
jq 'del(.client_payload.source_run_attempt)' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "missing required payload key"

make_valid
jq '.client_payload.unexpected = "value"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "unexpected payload key"

make_valid
jq '.client_payload.app = "stockdividend"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "wrong application"

make_valid
jq '.client_payload.release = "prod-v1.2.3-short"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "malformed release tag"

make_valid
jq '.client_payload.release = "prod-v1.2.3-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "release tag not bound to source head"

make_valid
jq '.client_payload.web_digest = "sha256:invalid"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "invalid web digest"

make_valid
jq '.client_payload.service_digest = "sha256:invalid"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "invalid service digest"

make_valid
jq '.client_payload.source_head_sha = "short"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "invalid source head SHA"

make_valid
jq '.client_payload.source_run_id = "0"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "zero source run ID"

make_valid
jq '.client_payload.source_run_id = 42670000001' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "non-string source run ID"

make_valid
jq '.client_payload.source_run_attempt = 1' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "non-string source run attempt"

make_valid
jq '.client_payload.source_head_sha = "0123456789ABCDEF0123456789ABCDEF01234567"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "uppercase source head SHA"

make_valid
jq '.client_payload.source_run_attempt = "0"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "zero source run attempt"

make_valid
jq '.client_payload.source_workflow_path = ".github/workflows/other.yml"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "unapproved source workflow"

make_valid
jq '.client_payload.source_event = "push"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "non-manual publisher event"

make_valid
jq 'del(.client_payload)' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "missing client payload"

make_valid
jq '.client_payload = []' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "non-object client payload"

printf '%s\n' "TCE exact dispatch payload contract tests passed."
