#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/phanthienquoc/media-generation"
RUNNER_NAME="media-generation-k3s-01"
RUNNER_USER="media-runner"
RUNNER_DIR="/opt/media-actions-runner"
LABELS="self-hosted,linux,arm64,media-generation,k3s,vps"

: "${RUNNER_TOKEN:?Set RUNNER_TOKEN to the short-lived GitHub runner registration token}"
if [[ "$(id -u)" -ne 0 ]]; then echo "Run with sudo -E bash $0"; exit 1; fi
[[ "$(uname -m)" == "aarch64" ]] || { echo "This bootstrap expects ARM64/aarch64."; exit 1; }

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y curl jq tar ca-certificates libicu70 libssl3 libkrb5-3 zlib1g

id -u "$RUNNER_USER" >/dev/null 2>&1 || useradd --create-home --shell /bin/bash "$RUNNER_USER"
install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$RUNNER_DIR"

DOWNLOAD_URL="$(curl -fsSL https://api.github.com/repos/actions/runner/releases/latest |
  jq -r '.assets[] | select(.name | test("actions-runner-linux-arm64-.*\\.tar\\.gz$")) | .browser_download_url' | head -1)"
[[ -n "$DOWNLOAD_URL" ]] || { echo "Unable to resolve ARM64 runner download URL."; exit 1; }

if [[ ! -f "$RUNNER_DIR/.runner" ]]; then
  rm -rf "$RUNNER_DIR"/*
  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT
  curl -fsSL "$DOWNLOAD_URL" -o "$tmp"
  tar -xzf "$tmp" -C "$RUNNER_DIR"
  chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"
  sudo -u "$RUNNER_USER" "$RUNNER_DIR/config.sh" --unattended     --url "$REPO_URL"     --token "$RUNNER_TOKEN"     --name "$RUNNER_NAME"     --labels "$LABELS"     --work "_work"     --replace
fi

cat >/usr/local/sbin/media-kubectl <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
KUBECTL=(/usr/local/bin/k3s kubectl)

case "${1:-}" in
  ensure-namespace)
    [[ "$#" -eq 1 ]] || exit 2
    printf '%s\n' 'apiVersion: v1' 'kind: Namespace' 'metadata:' '  name: media-prod' |
      "${KUBECTL[@]}" apply -f -
    ;;
  sync-secret)
    [[ "$#" -eq 1 ]] || exit 2
    "${KUBECTL[@]}" create secret generic media-generation-secrets       -n media-prod       --from-env-file=/dev/stdin       --dry-run=client       -o yaml |
      "${KUBECTL[@]}" apply -f -
    "${KUBECTL[@]}" get secret media-generation-secrets -n media-prod >/dev/null
    ;;
  *)
    echo "media-kubectl: command is not allowlisted" >&2
    exit 2
    ;;
esac
EOF
chmod 0755 /usr/local/sbin/media-kubectl

cat >/etc/sudoers.d/media-generation-runner <<EOF
$RUNNER_USER ALL=(root) NOPASSWD: /usr/local/sbin/media-kubectl *
EOF
chmod 0440 /etc/sudoers.d/media-generation-runner
visudo -cf /etc/sudoers.d/media-generation-runner

cd "$RUNNER_DIR"
if [[ ! -f "$RUNNER_DIR/.service" ]]; then
  ./svc.sh install "$RUNNER_USER"
fi
./svc.sh start
chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"

echo "Media runner bootstrap complete: $RUNNER_NAME"
