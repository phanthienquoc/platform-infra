#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
KUBECTL_BIN="${PLATFORM_KUBECTL_BIN:-/usr/local/sbin/platform-kubectl}"
KUBECTL=("$KUBECTL_BIN")
TARGET_NAMESPACES=(stock-prod media-prod)

run_kubectl() {
  "${KUBECTL[@]}" "$@"
}

preflight() {
  local namespaces_json namespace pvc_json pvc_count pv_json pv_claims
  echo "### Platform namespace preservation check"
  for namespace in tce-prod microfe-platform; do
    run_kubectl get namespace "$namespace" >/dev/null
    echo "Preserved namespace present: $namespace"
  done

  namespaces_json="$(run_kubectl get namespaces -o json)"
  pv_json="$(run_kubectl get pv -o json)"
  for namespace in "${TARGET_NAMESPACES[@]}"; do
    jq -e --arg namespace "$namespace" '.items | any(.metadata.name == $namespace)' <<< "$namespaces_json" >/dev/null || {
      echo "Expected namespace $namespace is missing; stop for manual reconciliation." >&2
      return 1
    }
    echo
    echo "### Inventory: $namespace"
    run_kubectl get all -n "$namespace" -o wide
    run_kubectl get pvc -n "$namespace" -o wide
    pvc_json="$(run_kubectl get pvc -n "$namespace" -o json)"
    pvc_count="$(jq -r '.items | length' <<< "$pvc_json")"
    [[ "$pvc_count" == "0" ]] || {
      echo "PVC inventory is not empty in $namespace; backup/reclaim review is required." >&2
      return 1
    }
    pv_claims="$(jq -r --arg namespace "$namespace" '.items[]? | select(.spec.claimRef.namespace == $namespace) | [.metadata.name, .spec.persistentVolumeReclaimPolicy, .spec.storageClassName] | @tsv' <<< "$pv_json")"
    [[ -z "$pv_claims" ]] || {
      echo "PV claims remain for $namespace; backup/reclaim review is required:" >&2
      printf '%s\n' "$pv_claims" >&2
      return 1
    }
  done
  echo
  echo "### StorageClass inventory"
  run_kubectl get storageclasses -o wide
  echo "Preflight passed: target namespaces have no PVCs or PV claims."
}

case "$MODE" in
  plan)
    preflight
    echo "Read-only preflight complete. No Kubernetes resources were changed."
    ;;
  delete)
    [[ "${CONFIRMATION:-}" == "DELETE-STOCK-PROD-AND-MEDIA-PROD" ]] || {
      echo "CONFIRMATION must equal DELETE-STOCK-PROD-AND-MEDIA-PROD." >&2
      exit 2
    }
    [[ "${DATA_RETENTION_REVIEW:-}" == "BACKUP-AND-EXTERNAL-DATA-REVIEWED" ]] || {
      echo "DATA_RETENTION_REVIEW must equal BACKUP-AND-EXTERNAL-DATA-REVIEWED." >&2
      exit 2
    }
    preflight
    printf '%s\n%s\n' "$CONFIRMATION" "$DATA_RETENTION_REVIEW" | "${KUBECTL[@]}" decommission-stock-media
    ;;
  *)
    echo "Usage: $0 plan|delete" >&2
    exit 2
    ;;
esac
