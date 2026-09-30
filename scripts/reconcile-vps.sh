#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"

cd "$ROOT"

run_diff() {
  local rc

  # kubectl diff performs server-side dry-run requests against namespaced
  # resources, so a first reconciliation cannot diff them until their
  # declaratively-managed Namespace objects exist.
  for namespace_manifest in \
    apps/stockdividend/base/namespace.yaml \
    apps/tce-dashboard/base/namespace.yaml \
    apps/media-generation/base/namespace.yaml; do
    echo "== Ensuring namespace from $namespace_manifest =="
    sudo /usr/local/sbin/platform-kubectl apply -f "$namespace_manifest"
  done

  if sudo /usr/local/sbin/platform-kubectl diff -k environments/prod; then
    rc=0
  else
    rc=$?
  fi
  if [[ "$rc" -gt 1 ]]; then
    echo "Kubernetes diff failed with exit code $rc" >&2
    return "$rc"
  fi
  if [[ "$rc" -eq 1 ]]; then
    echo "Kubernetes drift detected."
    return 1
  fi
  echo "Kubernetes state matches the repository."
  return 0
}

case "$MODE" in
  plan)
    echo "== Kubernetes diff =="
    run_diff
    ;;
  apply)
    echo "== Preflight Kubernetes diff =="
    set +e
    run_diff
    diff_rc=$?
    set -e

    case "$diff_rc" in
      0)
        echo "No Kubernetes drift detected; skipping production apply."
        exit 0
        ;;
      1)
        echo "Drift detected; applying environments/prod."
        ;;
      *)
        echo "Kubernetes preflight diff failed; refusing production apply." >&2
        exit "$diff_rc"
        ;;
    esac

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
