#!/usr/bin/env bash
set -euo pipefail

EVENT_FILE="${1:-${GITHUB_EVENT_PATH:-}}"

fail() {
  echo "::error::$*" >&2
  exit 1
}

[[ -n "$EVENT_FILE" && -f "$EVENT_FILE" ]] || fail "GitHub repository-dispatch event file is unavailable."
command -v jq >/dev/null 2>&1 || fail "jq is required to validate the Auth dispatch payload."

jq -e '
  . as $event
  | ($event.client_payload // null) as $payload
  | ($payload | type == "object")
    and ($event.action == "auth-image-published")
    and ($payload | keys == [
      "app",
      "auth_digest",
      "commit",
      "component",
      "source_event",
      "source_head_sha",
      "source_run_attempt",
      "source_run_id",
      "source_workflow_path",
      "tag"
    ])
    and ($payload.app | type == "string" and . == "auth-service")
    and ($payload.component | type == "string" and . == "auth")
    and ($payload.auth_digest | type == "string" and test("^sha256:[0-9a-f]{64}$"))
    and ($payload.commit | type == "string" and test("^[0-9a-f]{40}$"))
    and ($payload.source_event | type == "string" and . == "workflow_dispatch")
    and ($payload.source_head_sha | type == "string" and test("^[0-9a-f]{40}$"))
    and ($payload.source_head_sha == $payload.commit)
    and ($payload.source_run_attempt | type == "string" and test("^[1-9][0-9]*$"))
    and ($payload.source_run_id | type == "string" and test("^[1-9][0-9]*$"))
    and ($payload.source_workflow_path | type == "string" and . == ".github/workflows/release.yml")
    and ($payload.tag | type == "string" and test("^prod-v[0-9]+\\.[0-9]+\\.[0-9]+-[0-9a-f]{40}$"))
    and ($payload.tag | endswith("-" + $payload.commit))
' "$EVENT_FILE" >/dev/null || fail "Auth repository-dispatch client_payload does not match the exact approved schema."

echo "Verified exact Auth repository-dispatch client_payload schema and provenance fields."
