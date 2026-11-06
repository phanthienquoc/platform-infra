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
[[ "$1" == "is-active" ]]
[[ "$2" == "actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service" ]]
printf '%s\n' "${MOCK_SERVICE_STATE:-inactive}"
case "${MOCK_SERVICE_STATE:-inactive}" in
  inactive|failed|unknown) exit 3 ;;
  *) exit 0 ;;
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
chmod +x "$tmp/bin/systemctl" "$tmp/bin/pgrep"

run_guard() {
  PATH="$tmp/bin:$PATH" MOCK_SERVICE_STATE="${MOCK_SERVICE_STATE:-inactive}" \
    MOCK_LISTENER_PRESENT="${MOCK_LISTENER_PRESENT:-0}" bash "$SCRIPT"
}
expect_failure() {
  local label="$1"
  if run_guard >/dev/null 2>&1; then
    echo "FAIL: active/unknown runner state was accepted: $label" >&2
    exit 1
  fi
}

MOCK_SERVICE_STATE=inactive MOCK_LISTENER_PRESENT=0 run_guard >/dev/null
MOCK_SERVICE_STATE=failed MOCK_LISTENER_PRESENT=0 run_guard >/dev/null
MOCK_SERVICE_STATE=unknown MOCK_LISTENER_PRESENT=0 run_guard >/dev/null
MOCK_SERVICE_STATE=active expect_failure "active service"
MOCK_SERVICE_STATE=activating expect_failure "activating service"
MOCK_SERVICE_STATE=deactivating expect_failure "deactivating service"
MOCK_SERVICE_STATE=reloading expect_failure "reloading service"
MOCK_SERVICE_STATE=unexpected expect_failure "unrecognized service state"
MOCK_SERVICE_STATE=inactive MOCK_LISTENER_PRESENT=1 expect_failure "listener process still running"

echo "Dedicated Media runner retirement guard tests passed."
