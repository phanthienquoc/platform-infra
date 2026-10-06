#!/usr/bin/env bash
set -euo pipefail

output="${1:-/tmp/platform-infra-network.yaml}"
kubectl kustomize environments/prod > "$output"

grep -q '^kind: Service$' "$output" || { echo "Expected application Services were not rendered."; exit 1; }
if grep -nE '^  type: (LoadBalancer|NodePort)$' "$output"; then
  echo "Non-ClusterIP Services found."
  exit 1
fi

ingress_count="$(grep -c '^kind: Ingress$' "$output" || true)"
if [ "$ingress_count" -ne 4 ]; then
  echo "Expected exactly 4 production Ingress resources, found $ingress_count."
  exit 1
fi

mapfile -t hosts < <(grep -Eo '[A-Za-z0-9.-]+\.mrcute\.space' "$output" | sort -u)
allowed='
tce.mrcute.space
mrcute.space
www.mrcute.space
admin.mrcute.space
api.mrcute.space
media.mrcute.space
auth.mrcute.space
app.mrcute.space
ws.mrcute.space
'
for host in "${hosts[@]}"; do
  grep -qx "$host" <<< "$allowed" || { echo "Unexpected externally routable host: $host"; exit 1; }
done

echo "Validated network boundaries: ClusterIP Services, $ingress_count approved Ingress resources."
