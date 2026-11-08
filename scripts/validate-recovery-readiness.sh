#!/usr/bin/env bash
set -euo pipefail

# Read-only recovery readiness validation for the single-node production cluster.
# This validates that GitOps state can be reconstructed and that current workloads
# retain rollback history without executing rollback/apply operations.

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"
CERT_MANAGER_MANIFEST_FILE="$ROOT/platform/cert-manager/cert-manager.yaml"
CERT_MANAGER_MANIFEST_PREPARED=false
cleanup() {
  if [[ "$CERT_MANAGER_MANIFEST_PREPARED" == true ]]; then
    rm -f "$CERT_MANAGER_MANIFEST_FILE"
  fi
}
trap cleanup EXIT
bash scripts/prepare-cert-manager-manifest.sh "$CERT_MANAGER_MANIFEST_FILE"
CERT_MANAGER_MANIFEST_PREPARED=true

KUBECTL="${KUBECTL:-sudo /usr/local/sbin/platform-kubectl}"

run_kubectl() {
  # shellcheck disable=SC2086
  $KUBECTL "$@"
}

for command in awk grep; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "::error::Required command not found: $command" >&2
    exit 1
  }
done

echo "== GitOps reconstruction validation =="
run_kubectl kustomize environments/prod >/dev/null
run_kubectl apply --dry-run=server -k environments/prod >/dev/null
echo "Server-side dry-run accepted the repository production manifests."

echo
echo "== Rollback history =="
for target in \
  "deployment/tce-service tce-prod" \
  "deployment/tce-frontend tce-prod"; do
  read -r resource namespace <<< "$target"
  echo "-- $namespace/$resource --"
  run_kubectl rollout history "$resource" -n "$namespace" >/dev/null
  run_kubectl get "$resource" -n "$namespace" -o jsonpath='{.metadata.generation}{"\t"}{.status.observedGeneration}{"\n"}'
done

echo
echo "== ReplicaSet retention =="
namespaces=(tce-prod)
for namespace in "${namespaces[@]}"; do
  run_kubectl get rs -n "$namespace" --sort-by=.metadata.creationTimestamp -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,DESIRED:.spec.replicas,AGE:.metadata.creationTimestamp'
done

echo
echo "Recovery readiness validated: manifests reconstructable by server-side dry-run and rollback history is inspectable."
echo "No apply, rollout undo, restart, scale, or Secret read was performed."
