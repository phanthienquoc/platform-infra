#!/usr/bin/env bash
set -euo pipefail

output="${1:-/tmp/platform-infra-rendered.yaml}"
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
