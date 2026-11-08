#!/usr/bin/env bash
set -euo pipefail

SERVICE="actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service"
PROCESS_PATTERN='[/]opt/media-actions-runner/bin/Runner.Listener'

fail() {
  echo "::error::$*" >&2
  exit 1
}

command -v systemctl >/dev/null 2>&1 || fail "systemctl is unavailable; cannot prove the dedicated Media runner is retired."
command -v pgrep >/dev/null 2>&1 || fail "pgrep is unavailable; cannot prove the dedicated Media runner process is absent."

service_state="$(systemctl is-active "$SERVICE" 2>/dev/null || true)"
case "$service_state" in
  inactive|failed|unknown)
    ;;
  active|activating|deactivating|reloading)
    fail "Dedicated Media runner service is still $service_state; stop it before namespace deletion."
    ;;
  *)
    fail "Unable to determine dedicated Media runner service state (state=${service_state:-empty}); refusing namespace deletion."
    ;;
esac

service_enabled="$(systemctl is-enabled "$SERVICE" 2>/dev/null || true)"
case "$service_enabled" in
  disabled|masked|masked-runtime|not-found)
    ;;
  enabled|enabled-runtime|linked|linked-runtime|alias|static|indirect|generated|transient|bad|"")
    fail "Dedicated Media runner unit is still enabled or has an unsafe/unknown enablement state (state=${service_enabled:-empty}); disable or remove the unit before namespace deletion."
    ;;
  *)
    fail "Unrecognized Media runner unit enablement state (state=$service_enabled); refusing namespace deletion."
    ;;
esac

if pgrep -f "$PROCESS_PATTERN" >/dev/null 2>&1; then
  fail "A Media Runner.Listener process is still present; refusing namespace deletion."
fi

# A typed confirmation is not proof that the repository-level runner was
# unregistered. Require a read-only, narrowly scoped token and verify the
# exact runner name against the Media repository's authoritative runner list.
AUDIT_TOKEN="${MEDIA_RUNNER_AUDIT_TOKEN:-}"
[[ -n "$AUDIT_TOKEN" ]] || fail "MEDIA_RUNNER_AUDIT_TOKEN is missing; cannot verify GitHub runner registration."
command -v curl >/dev/null 2>&1 || fail "curl is unavailable; cannot verify GitHub runner registration."
command -v jq >/dev/null 2>&1 || fail "jq is unavailable; cannot verify GitHub runner registration."
unset MEDIA_RUNNER_AUDIT_TOKEN

REPOSITORY="phanthienquoc/media-generation"
RUNNER_NAME="media-generation-k3s-01"
API_URL="https://api.github.com/repos/$REPOSITORY/actions/runners"
fetch_runner_page() {
  local page="$1"
  local url response
  url="$API_URL?per_page=100&page=$page"
  if ! response="$(printf 'header = "Accept: application/vnd.github+json"\nheader = "Authorization: Bearer %s"\nheader = "X-GitHub-Api-Version: 2022-11-28"\n' "$AUDIT_TOKEN" |
    curl --fail --silent --show-error --config - "$url")"; then
    fail "GitHub runner registration API failed for $REPOSITORY (page $page); refusing namespace deletion."
  fi
  jq -e 'type == "object" and (.total_count | type == "number") and (.runners | type == "array")' <<< "$response" >/dev/null ||
    fail "GitHub runner registration API returned an invalid response; refusing namespace deletion."
  printf '%s' "$response"
}

first_page="$(fetch_runner_page 1)"
total_count="$(jq -er '.total_count | numbers' <<< "$first_page")" ||
  fail "GitHub runner registration response has no valid total_count."
page_count=$(( (total_count + 99) / 100 ))
(( page_count >= 1 )) || page_count=1
for ((page = 1; page <= page_count; page++)); do
  if [[ "$page" == "1" ]]; then
    page_json="$first_page"
  else
    page_json="$(fetch_runner_page "$page")"
  fi
  if jq -e --arg runner "$RUNNER_NAME" '.runners[]? | select(.name == $runner)' <<< "$page_json" >/dev/null; then
    unset AUDIT_TOKEN first_page page_json
    fail "GitHub still lists $REPOSITORY runner $RUNNER_NAME; refusing namespace deletion."
  fi
done
unset AUDIT_TOKEN first_page page_json

echo "Verified $REPOSITORY has no registered runner named $RUNNER_NAME; the local service is inactive, disabled/masked or absent, and no Runner.Listener process remains."
