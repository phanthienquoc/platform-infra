#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"

cd "$ROOT"

run_diff() {
  set +e
  sudo /usr/local/sbin/platform-kubectl diff -k environments/prod
  local rc=$?
  set -e
  if [[ "$rc" -gt 1 ]]; then
    echo "Kubernetes diff failed with exit code $rc" >&2
    return "$rc"
  fi
  if [[ "$rc" -eq 1 ]]; then
    echo "Kubernetes drift detected."
  else
    echo "Kubernetes state matches the repository."
  fi
}

wait_rollout() {
  local deployment="$1"
  local namespace="$2"

  set +e
  sudo /usr/local/sbin/platform-kubectl rollout status "deployment/${deployment}" -n "$namespace" --timeout=180s
  local rc=$?
  set -e

  if [[ "$rc" -eq 0 ]]; then
    return 0
  fi

  echo "Rollout failed or timed out for ${namespace}/${deployment}; collecting safe diagnostics." >&2
  echo "== Deployment state: ${namespace}/${deployment} ==" >&2
  sudo /usr/local/sbin/platform-kubectl get deployments -n "$namespace" -o wide >&2 || true
  echo "== Pod state: ${namespace} ==" >&2
  sudo /usr/local/sbin/platform-kubectl get pods -n "$namespace" -o wide >&2 || true
  echo "Rollout diagnostics complete; no secret-bearing resources are queried." >&2

  return "$rc"
}

case "$MODE" in
  plan)
    echo "== Kubernetes diff =="
    run_diff
    ;;
  apply)
    echo "== Preflight Kubernetes diff =="
    run_diff

    echo "== Applying environments/prod =="
    sudo /usr/local/sbin/platform-kubectl apply -k environments/prod

    echo "== Waiting for application rollouts =="

    rollout_rc=0

    if ! wait_rollout stock-backend stock-prod; then
      rollout_rc=1
    fi

    if ! wait_rollout stock-frontend stock-prod; then
      rollout_rc=1
    fi

    if ! wait_rollout tce-service tce-prod; then
      rollout_rc=1
    fi

    if ! wait_rollout tce-frontend tce-prod; then
      rollout_rc=1
    fi

    if [[ "$rollout_rc" -ne 0 ]]; then
      echo "One or more application rollouts failed; all rollout checks were attempted." >&2
      exit "$rollout_rc"
    fi
    ;;
  *)
    echo "Usage: $0 {plan|apply}" >&2
    exit 2
    ;;
esac
