#!/usr/bin/env bash
set -euo pipefail

# Live validation for metrics-server / HPA prerequisites.
# Read-only: this script does not create or modify cluster resources.

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Required command not found: $1" >&2
    exit 2
  }
}

require_cmd kubectl
require_cmd jq

namespaces=(tce-prod stock-prod)

echo "== metrics API service =="
kubectl get apiservice v1beta1.metrics.k8s.io -o wide

api_available="$(kubectl get apiservice v1beta1.metrics.k8s.io -o jsonpath='{range .status.conditions[*]}{.type}={.status}{"\n"}{end}' | awk -F= '$1=="Available"{print $2; exit}')"

if [[ "$api_available" != "True" ]]; then
  echo "metrics.k8s.io APIService is not Available=True." >&2
  exit 1
fi

echo
echo "== metrics API smoke check =="
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes >/dev/null
kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods >/dev/null

echo
echo "== current node metrics =="
kubectl top nodes

echo
echo "== current pod metrics =="
kubectl top pods -A

echo
echo "== HPA inventory =="
kubectl get hpa -A

echo
echo "== workload resource requests =="
for namespace in "${namespaces[@]}"; do
  echo "-- $namespace --"
  kubectl get deploy -n "$namespace" -o json | jq -r '.items[] | .metadata.name as $name | ($name + "\t" + ([.spec.template.spec.containers[] | select(.resources.requests.cpu == null or .resources.requests.memory == null) | .name] | join(",")))' |
  while IFS=$'\t' read -r deployment missing; do
    if [[ -n "$missing" ]]; then
      echo "MISSING requests: deployment=$deployment containers=$missing" >&2
      exit 1
    fi
    echo "OK: $deployment"
  done
done

echo
echo "Metrics-server API and HPA prerequisites passed in the target namespaces."
echo "This command is read-only; no production resource was changed."
