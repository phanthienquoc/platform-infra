#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$ROOT"
output="${1:-/tmp/platform-infra-network.yaml}"
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

grep -q '^kind: Service$' "$output" || { echo "Expected application Services were not rendered."; exit 1; }
if grep -nE '^  type: (LoadBalancer|NodePort)$' "$output"; then
  echo "Non-ClusterIP Services found."
  exit 1
fi

ingress_count="$(grep -c '^kind: Ingress$' "$output" || true)"
if [ "$ingress_count" -ne 2 ]; then
  echo "Expected exactly 2 production Ingress resources after Stock/Media retirement, found $ingress_count."
  exit 1
fi

mapfile -t hosts < <(grep -Eo '[A-Za-z0-9.-]+\.mrcute\.space' "$output" | sort -u)
allowed='
tce.mrcute.space
auth.mrcute.space
sso.mrcute.space
app.mrcute.space
ws.mrcute.space
'
for host in "${hosts[@]}"; do
  grep -qx "$host" <<< "$allowed" || { echo "Unexpected externally routable host: $host"; exit 1; }
done

echo "Validated network boundaries: ClusterIP Services, $ingress_count approved Ingress resources."
