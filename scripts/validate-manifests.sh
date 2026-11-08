#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$ROOT"
output="${1:-/tmp/platform-infra-rendered.yaml}"
manifest="$ROOT/platform/cert-manager/cert-manager.yaml"
CERT_MANAGER_MANIFEST_PREPARED=false
cleanup() {
  if [[ "$CERT_MANAGER_MANIFEST_PREPARED" == true ]]; then
    rm -f "$manifest"
  fi
}
trap cleanup EXIT

bash scripts/prepare-cert-manager-manifest.sh "$manifest"
CERT_MANAGER_MANIFEST_PREPARED=true
kubectl kustomize environments/prod > "$output"
kubectl apply --dry-run=client --validate=strict -f "$output"

if grep -nE '^kind: Secret$|^[[:space:]]+data:' "$output"; then
  echo 'Rendered manifests must not contain Secret objects or inline secret data.' >&2
  exit 1
fi

if grep -E '^[[:space:]]+image:' "$output" | grep -Ev ':[0-9a-f]{7,64}$'; then
  echo 'Application images must use immutable Git-SHA tags.' >&2
  exit 1
fi

echo "Validated $output"
