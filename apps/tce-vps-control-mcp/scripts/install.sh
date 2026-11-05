#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="/opt/tce-vps-control-mcp"
CONFIG_DIR="/etc/tce-vps-control-mcp"
AUDIT_DIR="/var/log/tce-vps-control-mcp"

if [[ "$EUID" -ne 0 ]]; then
  echo "Run this installer with sudo." >&2
  exit 1
fi

command -v node >/dev/null || { echo "Node.js 22+ is required; install it before running this script." >&2; exit 1; }
node -e 'process.exit(Number(process.versions.node.split(".")[0]) >= 22 ? 0 : 1)' || {
  echo "Node.js 22+ is required." >&2
  exit 1
}
command -v npm >/dev/null || { echo "npm is required." >&2; exit 1; }

getent group tce-mcp >/dev/null 2>&1 || groupadd --system tce-mcp
id tce-mcp >/dev/null 2>&1 || useradd --system --gid tce-mcp --home-dir /var/lib/tce-vps-control-mcp --create-home --shell /usr/sbin/nologin tce-mcp
getent group tce-shell >/dev/null 2>&1 || groupadd --system tce-shell
id tce-shell >/dev/null 2>&1 || useradd --system --gid tce-shell --home-dir /var/lib/tce-shell --create-home --shell /usr/sbin/nologin tce-shell
[[ "$(id -gn tce-mcp)" == "tce-mcp" ]] || { echo "tce-mcp must use its dedicated primary group." >&2; exit 1; }
[[ "$(id -gn tce-shell)" == "tce-shell" ]] || { echo "tce-shell must use its dedicated primary group." >&2; exit 1; }

install -d -o root -g root -m 0755 "$INSTALL_DIR"
install -d -o root -g root -m 0750 "$CONFIG_DIR"
install -d -o tce-mcp -g tce-mcp -m 0700 "$AUDIT_DIR"
install -d -o tce-shell -g tce-shell -m 0750 /var/lib/tce-shell

[[ -f "$APP_DIR/package-lock.json" ]] || {
  echo "package-lock.json is required; refusing a non-reproducible production installation." >&2
  exit 1
}
cp -a "$APP_DIR/package.json" "$APP_DIR/package-lock.json" "$APP_DIR/tsconfig.json" "$APP_DIR/src" "$INSTALL_DIR/"
chown -R root:root "$INSTALL_DIR"
cd "$INSTALL_DIR"
npm ci --include=dev --ignore-scripts --no-audit --no-fund
npm run build
npm prune --omit=dev

install -o root -g root -m 0755 "$APP_DIR/ops/tce-mcp-docker" /usr/local/sbin/tce-mcp-docker
install -o root -g root -m 0440 "$APP_DIR/ops/tce-vps-control-mcp.sudoers" /etc/sudoers.d/tce-vps-control-mcp
visudo -cf /etc/sudoers.d/tce-vps-control-mcp
install -o root -g root -m 0644 "$APP_DIR/ops/tce-vps-control-mcp.service" /etc/systemd/system/tce-vps-control-mcp.service

if [[ ! -f "$CONFIG_DIR/server.env" ]]; then
  token="$(openssl rand -hex 32)"
  cat > "$CONFIG_DIR/server.env" <<EOF
HOST=127.0.0.1
PORT=8765
MCP_BEARER_TOKEN=$token
AUDIT_FILE=/var/log/tce-vps-control-mcp/audit.jsonl
KUBECTL_PATH=/usr/local/bin/kubectl
KUBECONFIG=/etc/tce-vps-control-mcp/kubeconfig
ALLOWED_CWD_ROOTS=/srv,/var/log,/tmp
EOF
  chmod 0600 "$CONFIG_DIR/server.env"
  chown root:tce-mcp "$CONFIG_DIR/server.env"
  echo "A new bearer token was generated in $CONFIG_DIR/server.env. Do not paste it into chat or commit it."
else
  echo "Existing server.env preserved."
fi

systemctl daemon-reload
systemctl enable --now tce-vps-control-mcp
systemctl --no-pager --full status tce-vps-control-mcp
