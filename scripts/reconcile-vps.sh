#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"

cd "$ROOT"

case "$MODE" in
  plan)
    echo "== Kubernetes diff =="
    sudo /usr/local/sbin/platform-kubectl diff -k environments/prod
    ;;
  apply)
    echo "== Applying environments/prod =="
    sudo /usr/local/sbin/platform-kubectl apply -k environments/prod

    echo "== Waiting for application rollouts =="
    sudo /usr/local/sbin/platform-kubectl rollout status deployment/stock-backend -n stock-prod
    sudo /usr/local/sbin/platform-kubectl rollout status deployment/stock-frontend -n stock-prod
    sudo /usr/local/sbin/platform-kubectl rollout status deployment/tce-service -n tce-prod
    sudo /usr/local/sbin/platform-kubectl rollout status deployment/tce-frontend -n tce-prod
    ;;
  *)
    echo "Usage: $0 {plan|apply}" >&2
    exit 2
    ;;
esac
