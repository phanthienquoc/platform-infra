#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
workflow="$repo_root/.github/workflows/decommission-stock-media.yml"
wrapper="$repo_root/scripts/bootstrap-runner.sh"

for required in \
  "workflow_dispatch:" \
  "environment: production" \
  "DECOMMISSION stock-prod media-prod" \
  "I UNDERSTAND THE OPERATION ABORTS ON ANY PVC OR PV CLAIM" \
  "EXTERNAL DATA STORES AND DNS WILL BE LEFT IN PLACE" \
  "MEDIA RUNNER WILL REMAIN ACTIVE FOR SEPARATE CLEANUP" \
  "platform-kubectl decommission-stock-media"; do
  grep -Fq "$required" "$workflow" || {
    echo "Missing decommission workflow contract: $required" >&2
    exit 1
  }
done

if grep -Eq '^[[:space:]]*(push|schedule):' "$workflow"; then
  echo "Namespace deletion must never be triggered by push or schedule." >&2
  exit 1
fi

for required in \
  "  decommission-stock-media)" \
  'for namespace in stock-prod media-prod; do' \
  'get pvc -n "$namespace" -o json' \
  'get pv -o json' \
  'delete namespace "$namespace" --wait=true --timeout=180s' \
  'for namespace in tce-prod microfe-platform; do' \
  '"${KUBECTL[@]}" get namespace "$namespace"'; do
  grep -Fq "$required" "$wrapper" || {
    echo "Missing guarded runner contract: $required" >&2
    exit 1
  }
done

if grep -Eq 'delete (pvc|pv)|kubectl[[:space:]]+delete[[:space:]]+--all' "$wrapper"; then
  echo "Decommission wrapper must never delete PVCs, PVs, or all resources generically." >&2
  exit 1
fi

echo "Stock/Media namespace decommission contract tests passed."
