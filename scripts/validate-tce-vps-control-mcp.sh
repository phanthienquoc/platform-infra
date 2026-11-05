#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$ROOT/apps/tce-vps-control-mcp"
SRC="$APP/src/index.ts"
INSTALL="$APP/scripts/install.sh"
RBAC="$APP/ops/k8s-rbac.yaml"
DOCKER="$APP/ops/tce-mcp-docker"
SUDOERS="$APP/ops/tce-vps-control-mcp.sudoers"
README="$APP/README.md"
SERVICE="$APP/ops/tce-vps-control-mcp.service"

for file in "$SRC" "$INSTALL" "$RBAC" "$DOCKER" "$SUDOERS" "$README" "$SERVICE"; do
  test -s "$file" || { echo "Missing required MCP contract file: $file" >&2; exit 1; }
done

grep -Fq 'await realpath(requested)' "$SRC"
grep -Fq 'sudo", ["-n", "-u", "tce-shell", "-H", "--", "/bin/bash", "-lc", command]' "$SRC"
grep -Fq 'mode: 0o600' "$SRC"
! grep -Eq 'docker_restart|k8s_rollout_restart' "$SRC"
! grep -Eq 'verbs:[[:space:]]*\[[^]]*patch' "$RBAC"
! grep -Eq '^[[:space:]]*restart\)' "$DOCKER"
grep -Fq 'npm ci --include=dev --ignore-scripts --no-audit --no-fund' "$INSTALL"
grep -Fq 'package-lock.json is required' "$INSTALL"
grep -Fq 'groupadd --system tce-shell' "$INSTALL"
grep -Fq 'tce-mcp ALL=(tce-shell) NOPASSWD: /bin/bash -lc *' "$SUDOERS"
grep -Fq 'reconcile-vps.yml' "$README"
grep -Fq 'UMask=0077' "$SERVICE"
bash -n "$INSTALL"
bash -n "$DOCKER"

echo "TCE VPS Control MCP read-only/least-privilege contract passed."
