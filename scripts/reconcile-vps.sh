#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
KUBECTL_BIN="${PLATFORM_KUBECTL_BIN:-/usr/local/sbin/platform-kubectl}"
CERT_MANAGER_MANIFEST_FILE="$ROOT/platform/cert-manager/cert-manager.yaml"
CERT_MANAGER_MANIFEST_PREPARED=false

cd "$ROOT"

cleanup() {
  if [[ "$CERT_MANAGER_MANIFEST_PREPARED" == true ]]; then
    rm -f "$CERT_MANAGER_MANIFEST_FILE"
  fi
}
trap cleanup EXIT

prepare_cert_manager_manifest() {
  bash scripts/prepare-cert-manager-manifest.sh "$CERT_MANAGER_MANIFEST_FILE"
  CERT_MANAGER_MANIFEST_PREPARED=true
}

run_kubectl() {
  sudo "$KUBECTL_BIN" "$@"
}

run_diff() {
  local rc namespace output
  local required_namespaces=(k3s-debug microfe-platform tce-prod)
  local missing_namespaces=()

  [[ -s "$CERT_MANAGER_MANIFEST_FILE" ]] || {
    echo "Verified cert-manager release manifest is unavailable; refusing to diff." >&2
    return 2
  }

  # The checksum-verified release is materialized at the local Kustomize path.
  # Both diff and apply continue through the existing restricted platform-kubectl
  # wrapper and the single environments/prod GitOps authority.
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
    prepare_cert_manager_manifest
    echo "== Read-only Kubernetes diff =="
    run_diff
    ;;
  apply)
    prepare_cert_manager_manifest
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

    echo "== Applying checksum-verified cert-manager release and production manifests =="
    run_kubectl apply -k environments/prod

    echo "Manifest reconciliation completed successfully."
    echo "Application rollout verification is intentionally handled by the workflow per target application."
    ;;
  *)
    echo "Usage: $0 {plan|apply}" >&2
    exit 2
    ;;
esac
