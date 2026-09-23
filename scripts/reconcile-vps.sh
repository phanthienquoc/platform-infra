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

    echo "Manifest reconciliation completed successfully."
    echo "Application rollout verification is intentionally handled by the workflow per target application."
    ;;
  *)
    echo "Usage: $0 {plan|apply}" >&2
    exit 2
    ;;
esac
