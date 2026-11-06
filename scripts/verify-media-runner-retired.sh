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

echo "Dedicated Media runner service is inactive and disabled/masked/not installed, with no Runner.Listener process. GitHub registration remains operator-attested by the required typed confirmation."
