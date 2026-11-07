#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
KUBECTL_BIN="${PLATFORM_KUBECTL_BIN:-/usr/local/sbin/platform-kubectl}"

cd "$ROOT"

run_kubectl() {
  sudo "$KUBECTL_BIN" "$@"
}

run_diff() {
  local rc namespace output
  local required_namespaces=(k3s-debug microfe-platform tce-prod)
  local missing_namespaces=()

  # kubectl diff cannot reliably inspect namespaced objects before their
  # declaratively-managed Namespace resources exist. Check those prerequisites
  # without creating anything; a missing Namespace is desired-state drift.
  for namespace in "${required_namespaces[@]}"; do
    if output="$(run_kubectl get namespace "$namespace" -o name 2>&1)"; then
      continue
    fi

    if grep -Eqi 'NotFound|not found' <<< "$output"; then
      missing_namespaces+=("$namespace")
      continue
    fi

    echo "Unable to verify required namespace $namespace; refusing to infer drift." >&2
    printf '%s\n' "$output" >&2
    return 2
  done

  if (( ${#missing_namespaces[@]} > 0 )); then
    printf 'Required namespace(s) absent from the live cluster: %s\n' "${missing_namespaces[*]}"
    echo "Read-only plan reports namespace drift; only explicit apply may create declared resources."
    return 1
  fi

  if run_kubectl diff -k environments/prod; then
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
    echo "== Read-only Kubernetes diff =="
    run_diff
    ;;
  apply)
    echo "== Preflight read-only Kubernetes diff =="
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
    run_kubectl apply -k environments/prod

    echo "Manifest reconciliation completed successfully."
    echo "Application rollout verification is intentionally handled by the workflow per target application."
    ;;
  *)
    echo "Usage: $0 {plan|apply}" >&2
    exit 2
    ;;
esac
