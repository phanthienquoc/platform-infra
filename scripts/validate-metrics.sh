#!/usr/bin/env bash
set -euo pipefail

KUBECTL="${KUBECTL:-sudo /usr/local/sbin/platform-kubectl}"

run_kubectl() {
  # shellcheck disable=SC2086
  $KUBECTL "$@"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "::error::Required command not found: $1" >&2
    exit 1
  }
}

require_command awk
require_command grep

api_status="$(run_kubectl get apiservice v1beta1.metrics.k8s.io -o jsonpath='{range .status.conditions[?(@.type=="Available")]}{.status}{"\n"}{end}')"
if [ "$api_status" != "True" ]; then
  echo "::error::metrics.k8s.io APIService is not Available (status=${api_status:-unknown})." >&2
  exit 1
fi

echo "metrics.k8s.io APIService: Available"

run_kubectl api-resources --api-group=metrics.k8s.io >/dev/null
run_kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes >/dev/null
run_kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/tce-prod/pods >/dev/null
run_kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/stock-prod/pods >/dev/null

echo "metrics.k8s.io API: node and workload metrics endpoints reachable"

for namespace in tce-prod stock-prod; do
  deployments="$(run_kubectl get deployments -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')"
  test -n "$deployments" || {
    echo "::error::No deployments found in namespace $namespace." >&2
    exit 1
  }

  while IFS= read -r deployment; do
    [ -n "$deployment" ] || continue
    container_count="$(run_kubectl get deployment "$deployment" -n "$namespace" -o jsonpath='{range .spec.template.spec.containers[*]}{.name}{"\n"}{end}' | wc -l)"
    request_count="$(run_kubectl get deployment "$deployment" -n "$namespace" -o jsonpath='{range .spec.template.spec.containers[*]}{.resources.requests.cpu}{"\t"}{.resources.requests.memory}{"\n"}{end}' | awk 'NF==2{count++} END{print count+0}')"
    if [ "$request_count" -ne "$container_count" ]; then
      echo "::error::$namespace/$deployment is missing CPU and/or memory requests for one or more containers." >&2
      exit 1
    fi
    echo "HPA resource prerequisite: $namespace/$deployment requests present for $container_count container(s)"
  done <<< "$deployments"
done

hpa_api="$(run_kubectl api-resources --api-group=autoscaling | awk '$1=="horizontalpodautoscalers" {print $1}')"
test "$hpa_api" = "horizontalpodautoscalers" || {
  echo "::error::autoscaling API resources are unavailable." >&2
  exit 1
}

echo "autoscaling API: HorizontalPodAutoscaler resource available"
echo "Metrics/HPA prerequisites validated without mutating the cluster."
