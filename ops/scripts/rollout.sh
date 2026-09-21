#!/usr/bin/env bash
set -euo pipefail
NS=${1:?namespace}
APP=${2:?deployment}
kubectl -n "$NS" rollout status deployment/"$APP" --timeout=180s
kubectl -n "$NS" get deployment,pod,svc -o wide
