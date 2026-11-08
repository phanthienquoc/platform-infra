#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
EXPECTED_DEST="$ROOT/platform/cert-manager/cert-manager.yaml"
DEST="${1:-$EXPECTED_DEST}"

CERT_MANAGER_VERSION="v1.21.1"
# GitHub Release API asset digest for cert-manager.yaml at v1.21.1.
CERT_MANAGER_MANIFEST_SHA256="5f6a499b8c1857d57f560f536e0dcc830914b45c420899fe7ad0692c8624e408"
CERT_MANAGER_MANIFEST_URL="https://github.com/cert-manager/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml"

if [[ "$DEST" != "$EXPECTED_DEST" ]]; then
  echo "Refusing to write cert-manager manifest outside the declared Kustomize path: $DEST" >&2
  exit 2
fi
if [[ -e "$DEST" ]]; then
  echo "Refusing to overwrite an existing cert-manager manifest: $DEST" >&2
  exit 2
fi

tmp_file="$(mktemp "$ROOT/platform/cert-manager/.cert-manager.yaml.XXXXXX")"
cleanup() {
  [[ ! -e "$tmp_file" ]] || rm -f "$tmp_file"
}
trap cleanup EXIT

curl --fail --silent --show-error --location \
  --retry 3 --retry-all-errors \
  --connect-timeout 10 --max-time 120 \
  "$CERT_MANAGER_MANIFEST_URL" \
  --output "$tmp_file"

if ! printf '%s  %s\n' "$CERT_MANAGER_MANIFEST_SHA256" "$tmp_file" | sha256sum --check --status; then
  echo "::error::Downloaded cert-manager ${CERT_MANAGER_VERSION} manifest failed its pinned SHA-256 check." >&2
  exit 1
fi

install -m 0644 "$tmp_file" "$DEST"
echo "Prepared checksum-verified cert-manager ${CERT_MANAGER_VERSION} manifest."
