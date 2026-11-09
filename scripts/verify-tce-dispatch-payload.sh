#!/usr/bin/env bash
set -euo pipefail

EVENT_FILE="\${1:-\${GITHUB_EVENT_PATH:-}}"

fail() {
  echo "::error::$*" >&2
  exit 1
}

[[ -n "$EVENT_FILE" && -f "$EVENT_FILE" ]] || fail "GitHub TCE repository-dispatch event file is unavailable."
command -v jq >/dev/null 2>&1 || fail "jq is required to validate the TCE dispatch payload."

jq -e '
  . as $event
  | ($event.client_payload // null) as $payload
  | ($payload | type == "object")
    and ($event.action == "tce-release-requested")
    and ($payload | keys == [
      "app",
      "release",
      "service_digest",
      "source_event",
      "source_head_sha",
      "source_run_attempt",
      "source_run_id",
      "source_workflow_path",
      "web_digest"
    ])
    and ($payload.app | type == "string" and . == "tce-dashboard")
    and ($payload.release | type == "string" and test("^prod-v[0-9]+\\.[0-9]+\\.[0-9]+-[0-9a-f]{40}$"))
    and ($payload.web_digest | type == "string" and test("^sha256:[0-9a-f]{64}$"))
    and ($payload.service_digest | type == "string" and test("^sha256:[0-9a-f]{64}$"))
    and ($payload.source_run_id | type == "string" and test("^[1-9][0-9]*$"))
    and ($payload.source_run_attempt | type == "string" and test("^[1-9][0-9]*$"))
    and ($payload.source_workflow_path | type == "string" and . == ".github/workflows/wf-03-tce-production-deploy.yml")
    and ($payload.source_event | type == "string" and . == "workflow_dispatch")
    and ($payload.source_head_sha | type == "string" and test("^[0-9a-f]{40}$"))
    and ($payload.release | endswith("-" + $payload.source_head_sha))
' "$EVENT_FILE" >/dev/null || fail "TCE repository-dispatch client_payload does not match the exact approved schema."

echo "Verified exact TCE repository-dispatch client_payload schema and provenance fields."
