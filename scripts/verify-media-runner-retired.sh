#!/usr/bin/env bash
set -euo pipefail

SERVICE="actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service"
PROCESS_PATTERN='[/]opt/media-actions-runner/bin/Runner.Listener'

fail() {
  echo "::error::$*" >&2
  exit 1
}

command -v systemctl >/dev/null 2>&1 || fail "systemctl is unavailable; cannot prove the dedicated Media runner is stopped."
command -v pgrep >/dev/null 2>&1 || fail "pgrep is unavailable; cannot prove the dedicated Media runner process is absent."

service_state="$(systemctl is-active "$SERVICE" 2>/dev/null || true)"
case "$service_state" in
  inactive|failed|unknown)
    ;;
  active|activating|deactivating|reloading)
    fail "Dedicated Media runner service is still $service_state; stop and unregister it before namespace deletion."
    ;;
  *)
    fail "Unable to determine dedicated Media runner service state (state=${service_state:-empty}); refusing namespace deletion."
    ;;
esac

if pgrep -f "$PROCESS_PATTERN" >/dev/null 2>&1; then
  fail "A Media Runner.Listener process is still present; refusing namespace deletion."
fi

echo "Dedicated Media runner service is inactive and no Runner.Listener process remains. GitHub registration remains operator-attested by the required typed confirmation."
