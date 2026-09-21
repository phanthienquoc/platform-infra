#!/usr/bin/env bash
set -euo pipefail

command -v kubectl >/dev/null || { echo 'kubectl is required'; exit 1; }

if [[ "${ALLOW_APPLY:-}" != "true" ]]; then
  echo 'Refusing to apply. Review manifests, then rerun with ALLOW_APPLY=true.'
  exit 1
fi

kubectl apply -f kubernetes/core/namespaces.yaml
kubectl apply -f kubernetes/core
kubectl apply -f kubernetes/values/config.example.yaml
kubectl apply -f kubernetes/apps/stock-prod
kubectl apply -f kubernetes/apps/tce-prod
