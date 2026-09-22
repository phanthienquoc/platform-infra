#!/usr/bin/env bash
set -euo pipefail

output="${1:-/tmp/platform-infra-network.yaml}"
kubectl kustomize environments/prod > "$output"

fail=0
service_docs=0
service_bad=0
ingress_docs=0
in_service=0

while IFS= read -r line; do
  case "$line" in
    "kind: Service")
      service_docs=$((service_docs + 1))
      in_service=1
      ;;
    "kind: Ingress")
      ingress_docs=$((ingress_docs + 1))
      in_service=0
      ;;
    "kind: "*)
      in_service=0
      ;;
  esac

  if [[ "$in_service" -eq 1 && "$line" =~ ^[[:space:]]*type:[[:space:]]*(.*)$ ]]; then
    service_type="${BASH_REMATCH[1]}"
    if [[ "$service_type" != "ClusterIP" ]]; then
      echo "Non-ClusterIP Service found: $service_type" >&2
      service_bad=$((service_bad + 1))
    fi
  fi
done < "$output"

if [[ "$service_docs" -eq 0 ]]; then
  echo 'Expected application Services were not rendered.' >&2
  fail=1
fi

if [[ "$service_bad" -ne 0 ]]; then
  fail=1
fi

# The production boundary is intentionally limited to the two known public hosts.
allowed_hosts='^(tce\.mrcute\.space|stockdividend\.mrcute\.space)$'
while IFS= read -r host; do
  if [[ -n "$host" && ! "$host" =~ $allowed_hosts ]]; then
    echo "Unexpected externally routable host: $host" >&2
    fail=1
  fi
done < <(
  grep -E '(^|[[:space:]-])host:[[:space:]]*[A-Za-z0-9.-]+' "$output" \
    | sed -E 's/.*host:[[:space:]]*([A-Za-z0-9.-]+).*/\1/'
  grep -E 'hosts:[[:space:]]*\[[^]]*\]' "$output" \
    | sed -E 's/.*hosts:[[:space:]]*\[([^]]*)\].*/\1/' \
    | tr ',' '\n' \
    | tr -d '[]"'
)

if [[ "$ingress_docs" -ne 2 ]]; then
  echo "Expected exactly 2 production Ingress resources, found $ingress_docs." >&2
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "Validated network boundaries in $output: Services remain internal ClusterIP and only the two approved public hosts are routable."
