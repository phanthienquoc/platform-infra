#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$ROOT/scripts/verify-retired-production-manifests.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

make_root() {
  local root="$1"
  mkdir -p "$root/environments/prod" "$root/platform" "$root/apps"
}

expect_failure() {
  local label="$1"
  local root="$2"
  if RETIRED_MANIFESTS_ROOT="$root" bash "$SCRIPT" >/dev/null 2>&1; then
    echo "FAIL: retired production reference was accepted: $label" >&2
    exit 1
  fi
}

clean="$tmp/clean"
make_root "$clean"
cat > "$clean/environments/prod/kustomization.yaml" <<'YAML'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../apps/tce-dashboard/overlays/prod
YAML
mkdir -p "$clean/apps/tce-dashboard/overlays/prod"
cat > "$clean/apps/tce-dashboard/overlays/prod/deployment.yaml" <<'YAML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tce-dashboard
  namespace: tce-prod
spec:
  template:
    spec:
      containers:
        - name: web
          image: ghcr.io/phanthienquoc/tce-dashboard/web:prod-v1.2.3-abcdef0
YAML
RETIRED_MANIFESTS_ROOT="$clean" bash "$SCRIPT" >/dev/null

retired_tree="$tmp/retired-tree"
make_root "$retired_tree"
mkdir -p "$retired_tree/apps/stockdividend"
expect_failure "retired StockDividend tree" "$retired_tree"

retired_namespace="$tmp/retired-namespace"
make_root "$retired_namespace"
cat > "$retired_namespace/platform/namespace.yaml" <<'YAML'
apiVersion: v1
kind: Namespace
metadata:
  name: media-prod
YAML
expect_failure "retired Media namespace manifest" "$retired_namespace"

retired_namespace_binding="$tmp/retired-namespace-binding"
make_root "$retired_namespace_binding"
cat > "$retired_namespace_binding/platform/deployment.yaml" <<'YAML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legacy
  namespace: stock-prod
YAML
expect_failure "retired Stock namespace" "$retired_namespace_binding"

retired_image="$tmp/retired-image"
make_root "$retired_image"
cat > "$retired_image/apps/deployment.yaml" <<'YAML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legacy
  namespace: tce-prod
spec:
  template:
    spec:
      containers:
        - name: legacy
          image: ghcr.io/phanthienquoc/media-generation/backend:prod-v1.2.3-abcdef0
YAML
expect_failure "retired Media GHCR image" "$retired_image"

missing_active_path="$tmp/missing-active-path"
mkdir -p "$missing_active_path/environments/prod" "$missing_active_path/apps"
if RETIRED_MANIFESTS_ROOT="$missing_active_path" bash "$SCRIPT" >/dev/null 2>&1; then
  echo "FAIL: missing active platform manifest path was accepted" >&2
  exit 1
fi

echo "Retired production manifest guard tests passed (1 positive, 5 negative cases)."
