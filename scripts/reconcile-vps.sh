#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
KUBECTL_BIN="${PLATFORM_KUBECTL_BIN:-/usr/local/sbin/platform-kubectl}"

# cert-manager publishes its install bundle as a GitHub Release asset, not a
# Kustomize remote base. Pin both the release and GitHub's asset SHA-256 so the
# controller/CRDs remain reproducible and are applied before local CR objects.
CERT_MANAGER_VERSION="v1.21.1"
CERT_MANAGER_MANIFEST_SHA256="5f6a499b8c1857d57f560f536e0dcc830914b45c420899fe7ad0692c8624e408"
CERT_MANAGER_MANIFEST_URL="https://github.com/cert-manager/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml"
CERT_MANAGER_TMP_DIR=""
CERT_MANAGER_MANIFEST_FILE=""

cd "$ROOT"

cleanup() {
  if [[ -n "$CERT_MANAGER_TMP_DIR" && -d "$CERT_MANAGER_TMP_DIR" ]]; then
    rm -rf "$CERT_MANAGER_TMP_DIR"
  fi
}
trap cleanup EXIT

prepare_cert_manager_manifest() {
  CERT_MANAGER_TMP_DIR="$(mktemp -d)"
  CERT_MANAGER_MANIFEST_FILE="$CERT_MANAGER_TMP_DIR/cert-manager.yaml"

  curl --fail --silent --show-error --location \
    --retry 3 --retry-all-errors \
    --connect-timeout 10 --max-time 120 \
    "$CERT_MANAGER_MANIFEST_URL" \
    --output "$CERT_MANAGER_MANIFEST_FILE"

  if ! printf '%s  %s\n' "$CERT_MANAGER_MANIFEST_SHA256" "$CERT_MANAGER_MANIFEST_FILE" | sha256sum --check --status; then
    echo "::error::Downloaded cert-manager ${CERT_MANAGER_VERSION} manifest failed its pinned SHA-256 check." >&2
    exit 1
  fi
  echo "Verified cert-manager ${CERT_MANAGER_VERSION} release manifest SHA-256."
}

run_kubectl() {
  sudo "$KUBECTL_BIN" "$@"
}

run_diff() {
  local rc namespace output
  local required_namespaces=(k3s-debug microfe-platform tce-prod)
  local missing_namespaces=()
  local drift_detected=false

  [[ -s "$CERT_MANAGER_MANIFEST_FILE" ]] || {
    echo "Verified cert-manager release manifest is unavailable; refusing to diff." >&2
    return 2
  }

  # The controller/CRD bundle is a pinned release artifact outside Kustomize.
  # Diff it separately, then diff the local CR objects and application overlays.
  if run_kubectl diff -f "$CERT_MANAGER_MANIFEST_FILE"; then
    :
  else
    rc=$?
    case "$rc" in
      1) drift_detected=true ;;
      *) echo "cert-manager release diff failed with exit code $rc." >&2; return "$rc" ;;
    esac
  fi

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
    :
  else
    rc=$?
    case "$rc" in
      1) drift_detected=true ;;
      *) echo "Kubernetes production Kustomize diff failed with exit code $rc." >&2; return "$rc" ;;
    esac
  fi

  if [[ "$drift_detected" == true ]]; then
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
        echo "Drift detected; applying the pinned cert-manager release and environments/prod."
        ;;
      *)
        echo "Kubernetes preflight diff failed; refusing production apply." >&2
        exit "$diff_rc"
        ;;
    esac

    echo "== Applying checksum-verified cert-manager ${CERT_MANAGER_VERSION} release =="
    run_kubectl apply -f "$CERT_MANAGER_MANIFEST_FILE"

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
