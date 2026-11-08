#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
EXPECTED_DEST="$ROOT/platform/cert-manager/cert-manager.yaml"
DEST="${1:-$EXPECTED_DEST}"

CERT_MANAGER_VERSION="v1.21.1"
# GitHub Release API asset digest for cert-manager.yaml at v1.21.1.
CERT_MANAGER_MANIFEST_SHA256="5f6a499b8c1857d57f560f536e0dcc830914b45c420899fe7ad0692c8624e408"
CERT_MANAGER_MANIFEST_URL="https://api.github.com/repos/cert-manager/cert-manager/releases/assets/494156333"

if [[ "$DEST" != "$EXPECTED_DEST" ]]; then
  echo "Refusing to write cert-manager manifest outside the declared Kustomize path: $DEST" >&2
  exit 2
fi
if [[ -e "$DEST" ]]; then
  if printf '%s  %s\n' "$CERT_MANAGER_MANIFEST_SHA256" "$DEST" | sha256sum --check --status; then
    echo "Existing cert-manager manifest already matches the pinned release digest."
    exit 0
  fi
  echo "Refusing to overwrite an existing cert-manager manifest with an unexpected digest: $DEST" >&2
  exit 2
fi

tmp_file="$(mktemp "$ROOT/platform/cert-manager/.cert-manager.yaml.XXXXXX")"
cleanup() {
  [[ ! -e "$tmp_file" ]] || rm -f "$tmp_file"
}
trap cleanup EXIT

curl_args=(
  --fail --silent --show-error --location
  --header "Accept: application/octet-stream"
  --header "X-GitHub-Api-Version: 2022-11-28"
  --retry 3 --retry-all-errors
  --connect-timeout 10 --max-time 120
)
if [[ -n "${GH_TOKEN:-}" ]]; then
  curl_args+=(--header "Authorization: Bearer ${GH_TOKEN}")
fi

curl "${curl_args[@]}" "$CERT_MANAGER_MANIFEST_URL" --output "$tmp_file"

if ! printf '%s  %s\n' "$CERT_MANAGER_MANIFEST_SHA256" "$tmp_file" | sha256sum --check --status; then
  echo "::error::Downloaded cert-manager ${CERT_MANAGER_VERSION} manifest failed its pinned SHA-256 check." >&2
  exit 1
fi

install -m 0644 "$tmp_file" "$DEST"
echo "Prepared checksum-verified cert-manager ${CERT_MANAGER_VERSION} manifest."
