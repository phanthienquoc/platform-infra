#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/verify-auth-dispatch-payload.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
event_file="$tmp_dir/event.json"

sample_sha=0123456789abcdef0123456789abcdef01234567
sample_digest=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

make_valid() {
  jq -n \
    --arg sha "$sample_sha" \
    --arg digest "$sample_digest" \
    '{
      action: "auth-image-published",
      client_payload: {
        app: "auth-service",
        auth_digest: $digest,
        commit: $sha,
        component: "auth",
        source_event: "workflow_dispatch",
        source_head_sha: $sha,
        source_run_attempt: "1",
        source_run_id: "42000000001",
        source_workflow_path: ".github/workflows/release.yml",
        tag: ("prod-v1.2.3-" + $sha)
      }
    }' > "$event_file"
}

expect_failure() {
  local label="$1"
  if bash "$validator" "$event_file" >/dev/null 2>&1; then
    echo "Expected Auth dispatch payload rejection: $label" >&2
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
jq '.client_payload.component = "api"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "wrong component"

make_valid
jq '.client_payload.auth_digest = "sha256:invalid"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "invalid image digest"

make_valid
jq '.client_payload.commit = "short"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "invalid source commit"

make_valid
jq '.client_payload.source_head_sha = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "source head and commit mismatch"

make_valid
jq '.client_payload.source_run_id = "0"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "zero source run ID"

make_valid
jq '.client_payload.source_run_id = 42000000001' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "non-string source run ID"

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
jq '.client_payload.tag = "prod-v1.2.3-short"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "malformed release tag"

make_valid
jq '.client_payload.tag = "prod-v1.2.3-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "release tag not bound to source commit"

make_valid
jq '.client_payload.source_run_attempt = 1' "$event_file" > "$tmp_dir/invalid.json"
mv "$tmp_dir/invalid.json" "$event_file"
expect_failure "non-string source run attempt"

printf '%s\n' "Auth exact dispatch payload contract tests passed."
