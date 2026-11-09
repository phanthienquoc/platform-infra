#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-plan}"
KUBECTL_BIN="${PLATFORM_KUBECTL_BIN:-/usr/local/sbin/platform-kubectl}"
KUBECTL_SUDO="${PLATFORM_KUBECTL_SUDO:-sudo}"
KUBECTL=("$KUBECTL_SUDO" "$KUBECTL_BIN")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_NAMESPACES=(stock-prod media-prod)

run_kubectl() {
  "${KUBECTL[@]}" "$@"
}

preflight() {
  bash "$SCRIPT_DIR/verify-retired-production-manifests.sh"
  local namespaces_json namespace pvc_json pvc_count pv_json pv_claims namespace_inventory snapshot_refs ingress_json
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
    echo "### Namespaced objects and storage snapshot references in $namespace (names only; no Secret/ConfigMap values)"
    namespace_inventory="$(run_kubectl inventory-namespace "$namespace")"
    printf '%s\n' "$namespace_inventory"
    snapshot_refs="$(grep -E '^(volumesnapshot|volumesnapshotcontent)\.snapshot\.storage\.k8s\.io/' <<< "$namespace_inventory" || true)"
    [[ -z "$snapshot_refs" ]] || {
      echo "VolumeSnapshot references remain for $namespace; backup/reclaim review is required:" >&2
      printf '%s\n' "$snapshot_refs" >&2
      return 1
    }
    echo "### Ingress hosts/TLS secret references and published addresses (names only): $namespace"
    ingress_json="$(run_kubectl get ingress -n "$namespace" -o json)"
    if jq -e '.items | length > 0' <<< "$ingress_json" >/dev/null; then
      jq -r '
        .items[]?
        | [
            .metadata.name // "",
            ([.spec.rules[]?.host] | unique | join(",")),
            ([.spec.tls[]?.hosts[]?] | unique | join(",")),
            ([.spec.tls[]?.secretName] | unique | join(",")),
            ([.status.loadBalancer.ingress[]? | (.ip // .hostname // "")] | map(select(length > 0)) | unique | join(","))
          ]
        | @tsv
      ' <<< "$ingress_json"
    else
      echo "none"
    fi
    echo "DNS ownership is not inferred; reconcile these hostnames with authoritative DNS/provider records before deletion."
    echo "### Common workload status: $namespace"
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
  echo "Preflight passed: target namespaces have no PVCs, PV claims or VolumeSnapshot references."
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
    [[ "${DNS_OWNERSHIP_REVIEW:-}" == "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED" ]] || {
      echo "DNS_OWNERSHIP_REVIEW must equal AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED." >&2
      exit 2
    }
    [[ "${RUNNER_RETIREMENT:-}" == "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED" ]] || {
      echo "RUNNER_RETIREMENT must equal MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED; no namespace was changed." >&2
      exit 2
    }
    preflight
    printf '%s\n%s\n%s\n%s\n' "$CONFIRMATION" "$DATA_RETENTION_REVIEW" "$DNS_OWNERSHIP_REVIEW" "$RUNNER_RETIREMENT" | "${KUBECTL[@]}" decommission-stock-media
    ;;
  *)
    echo "Usage: $0 plan|delete" >&2
    exit 2
    ;;
esac
