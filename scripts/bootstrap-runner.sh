#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${REPO_URL:-https://github.com/phanthienquoc/platform-infra}"
RUNNER_NAME="${RUNNER_NAME:-platform-k3s-01}"
RUNNER_USER="${RUNNER_USER:-github-runner}"
RUNNER_DIR="${RUNNER_DIR:-/opt/actions-runner}"
LABELS="${RUNNER_LABELS:-self-hosted,linux,arm64,platform-infra,k3s,vps}"
: "${RUNNER_TOKEN:?Set RUNNER_TOKEN to the short-lived GitHub runner registration token}"
if [[ "$(id -u)" -ne 0 ]]; then echo "Run with sudo -E bash $0"; exit 1; fi
if [[ "$(uname -m)" != "aarch64" ]]; then echo "This bootstrap expects ARM64/aarch64."; exit 1; fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y curl jq tar ca-certificates libicu70 libssl3 libkrb5-3 zlib1g
id -u "$RUNNER_USER" >/dev/null 2>&1 || useradd --create-home --shell /bin/bash "$RUNNER_USER"
usermod -aG docker "$RUNNER_USER" 2>/dev/null || true
install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$RUNNER_DIR"
DOWNLOAD_URL="$(curl -fsSL https://api.github.com/repos/actions/runner/releases/latest | jq -r '.assets[] | select(.name | test("actions-runner-linux-arm64-.*\\.tar\\.gz$")) | .browser_download_url' | head -1)"
[[ -n "$DOWNLOAD_URL" ]] || { echo "Unable to resolve ARM64 runner download URL."; exit 1; }
if [[ ! -f "$RUNNER_DIR/.runner" ]]; then
  rm -rf "$RUNNER_DIR"/*
  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT
  curl -fsSL "$DOWNLOAD_URL" -o "$tmp"
  tar -xzf "$tmp" -C "$RUNNER_DIR"
  chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"
  sudo -u "$RUNNER_USER" "$RUNNER_DIR/config.sh" --unattended --url "$REPO_URL" --token "$RUNNER_TOKEN" --name "$RUNNER_NAME" --labels "$LABELS" --work "_work" --replace
fi
cat >/usr/local/sbin/platform-kubectl <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

KUBECTL=(/usr/local/bin/k3s kubectl)

case "${1:-}" in
  version)
    [[ "$#" -eq 1 ]] || exit 2
    exec "${KUBECTL[@]}" version --client
    ;;
  get)
    shift
    case "${1:-}" in
      nodes|namespaces|ns|pods|po|deployments|deploy|services|svc|ingress|ingresses|jobs|cronjobs|pv|pvc)
        exec "${KUBECTL[@]}" get "$@"
        ;;
    esac
    ;;
  diff|apply)
    [[ "${2:-}" == "-k" && "${3:-}" == "environments/prod" && "${4:-}" == "" ]] || {
      echo "platform-kubectl: only -k environments/prod is allowed for $1" >&2
      exit 2
    }
    exec "${KUBECTL[@]}" "$1" -k environments/prod
    ;;
  rollout)
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/stock-backend" && "${4:-}" == "-n" && "${5:-}" == "stock-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/stock-backend -n stock-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/stock-frontend" && "${4:-}" == "-n" && "${5:-}" == "stock-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/stock-frontend -n stock-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/tce-service" && "${4:-}" == "-n" && "${5:-}" == "tce-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/tce-service -n tce-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/tce-frontend" && "${4:-}" == "-n" && "${5:-}" == "tce-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/tce-frontend -n tce-prod --timeout=180s
    ;;
esac

echo "platform-kubectl: command is not allowlisted" >&2
exit 2
EOF
chmod 0755 /usr/local/sbin/platform-kubectl
cat >/etc/sudoers.d/platform-infra-runner <<EOF
$RUNNER_USER ALL=(root) NOPASSWD: /usr/local/sbin/platform-kubectl *
EOF
chmod 0440 /etc/sudoers.d/platform-infra-runner
visudo -cf /etc/sudoers.d/platform-infra-runner
chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"

# svc.sh expects to be invoked from the runner root.
cd "$RUNNER_DIR"

# Keep bootstrap idempotent: a registered runner may already have a service.
if find /etc/systemd/system -maxdepth 1 -type f -name 'actions.runner.*.service' -print -quit | grep -q .; then
  echo "Runner service already installed; reusing existing service."
else
  ./svc.sh install "$RUNNER_USER"
fi

./svc.sh start

echo "Runner bootstrap complete: $RUNNER_NAME"
