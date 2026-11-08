#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$ROOT/scripts/verify-media-runner-retired.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin"

cat > "$tmp/bin/systemctl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
SERVICE="actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service"
case "$1" in
  is-active)
    [[ "$2" == "$SERVICE" ]]
    state="${MOCK_SERVICE_STATE:-inactive}"
    printf '%s\n' "$state"
    case "$state" in
      inactive|failed|unknown) exit 3 ;;
      *) exit 0 ;;
    esac
    ;;
  is-enabled)
    [[ "$2" == "$SERVICE" ]]
    state="${MOCK_SERVICE_ENABLED:-disabled}"
    printf '%s\n' "$state"
    case "$state" in
      enabled|enabled-runtime|linked|linked-runtime|alias) exit 0 ;;
      *) exit 1 ;;
    esac
    ;;
  *)
    echo "Unexpected systemctl command: $*" >&2
    exit 2
    ;;
esac
MOCK

cat > "$tmp/bin/pgrep" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
[[ "$1" == "-f" ]]
[[ "$2" == '[/]opt/media-actions-runner/bin/Runner.Listener' ]]
if [[ "${MOCK_LISTENER_PRESENT:-0}" == "1" ]]; then
  exit 0
fi
exit 1
MOCK
cat > "$tmp/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
for arg in "$@"; do
  [[ "$arg" != *"${MOCK_EXPECTED_TOKEN:-test-token}"* ]] || {
    echo "Token must not appear in curl argv." >&2
    exit 90
  }
done
config="$(cat)"
[[ "$config" == *"Authorization: Bearer ${MOCK_EXPECTED_TOKEN:-test-token}"* ]] || {
  echo "Expected authorization header was not supplied through curl stdin config." >&2
  exit 91
}
url="${@: -1}"
[[ "$url" == https://api.github.com/repos/phanthienquoc/media-generation/actions/runners?per_page=100\&page=* ]]
if [[ "${MOCK_API_FAIL:-0}" == "1" ]]; then
  exit 22
fi
case "$url" in
  *"page=1")
    if [[ "${MOCK_API_PAGINATION:-0}" == "1" ]]; then
      printf '%s\\n' '{"total_count":101,"runners":[]}'
    elif [[ "${MOCK_API_RUNNER_PRESENT:-0}" == "1" ]]; then
      printf '%s\\n' '{"total_count":1,"runners":[{"id":42,"name":"media-generation-k3s-01","status":"offline","busy":false}]}'
    else
      printf '%s\\n' '{"total_count":0,"runners":[]}'
    fi
    ;;
  *"page=2")
    printf '%s\\n' '{"total_count":101,"runners":[{"id":42,"name":"media-generation-k3s-01","status":"offline","busy":false}]}'
    ;;
  *)
    echo "Unexpected runner API URL: $url" >&2
    exit 92
    ;;
esac
MOCK
chmod +x "$tmp/bin/systemctl" "$tmp/bin/pgrep" "$tmp/bin/curl"

run_guard() {
  PATH="$tmp/bin:$PATH" \
    MEDIA_RUNNER_AUDIT_TOKEN="${MEDIA_RUNNER_AUDIT_TOKEN:-test-token}" \
    MOCK_EXPECTED_TOKEN=test-token \
    MOCK_SERVICE_STATE="${MOCK_SERVICE_STATE:-inactive}" \
    MOCK_SERVICE_ENABLED="${MOCK_SERVICE_ENABLED:-disabled}" \
    MOCK_LISTENER_PRESENT="${MOCK_LISTENER_PRESENT:-0}" \
    MOCK_API_RUNNER_PRESENT="${MOCK_API_RUNNER_PRESENT:-0}" \
    MOCK_API_PAGINATION="${MOCK_API_PAGINATION:-0}" \
    MOCK_API_FAIL="${MOCK_API_FAIL:-0}" \
    bash "$SCRIPT"
}
expect_failure() {
  local label="$1"
  if run_guard >/dev/null 2>&1; then
    echo "FAIL: unsafe runner state was accepted: $label" >&2
    exit 1
  fi
}

MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=disabled run_guard >/dev/null
MOCK_SERVICE_STATE=failed MOCK_SERVICE_ENABLED=masked run_guard >/dev/null
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=masked-runtime run_guard >/dev/null
MOCK_SERVICE_STATE=unknown MOCK_SERVICE_ENABLED=not-found run_guard >/dev/null

MOCK_SERVICE_STATE=active expect_failure "active service"
MOCK_SERVICE_STATE=activating expect_failure "activating service"
MOCK_SERVICE_STATE=deactivating expect_failure "deactivating service"
MOCK_SERVICE_STATE=reloading expect_failure "reloading service"
MOCK_SERVICE_STATE=unexpected expect_failure "unrecognized service state"
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=enabled expect_failure "enabled service unit"
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=enabled-runtime expect_failure "runtime-enabled service unit"
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=static expect_failure "static service unit"
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=linked expect_failure "linked service unit"
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=unknown expect_failure "unknown enablement state"
MOCK_SERVICE_STATE=inactive MOCK_SERVICE_ENABLED=disabled MOCK_LISTENER_PRESENT=1 expect_failure "listener process still running"
MOCK_API_RUNNER_PRESENT=1 expect_failure "GitHub runner remains registered"
MOCK_API_FAIL=1 expect_failure "GitHub runner API unavailable"
MOCK_API_PAGINATION=1 expect_failure "GitHub runner appears on a later API page"
if PATH="$tmp/bin:$PATH" env -u MEDIA_RUNNER_AUDIT_TOKEN bash "$SCRIPT" >/dev/null 2>&1; then
  echo "FAIL: missing GitHub runner audit token was accepted" >&2
  exit 1
fi

echo "Dedicated Media runner retirement guard tests passed."
