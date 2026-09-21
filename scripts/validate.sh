#!/usr/bin/env bash
set -euo pipefail

command -v kubectl >/dev/null || { echo 'kubectl is required'; exit 1; }

find kubernetes -type f -name '*.yaml' -print0 | while IFS= read -r -d '' file; do
  echo "Checking ${file}"
  kubectl apply --dry-run=client --validate=false -f "${file}" >/dev/null
done

echo 'Manifest syntax checks completed.'
