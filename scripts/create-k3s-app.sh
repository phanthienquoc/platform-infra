#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <app-name> <namespace> <ghcr-image> <container-port> [service-port]"
  exit 1
}
[ $# -ge 4 ] || usage
APP_NAME="$1"; NAMESPACE="$2"; GHCR_IMAGE="$3"; CONTAINER_PORT="$4"; SERVICE_PORT="${5:-$CONTAINER_PORT}"
CONTAINER_NAME="$APP_NAME"
DEST="apps/$APP_NAME"

[ ! -e "$DEST" ] || { echo "Refusing to overwrite existing $DEST" >&2; exit 1; }
mkdir -p "$DEST/base" "$DEST/overlays/prod"
cp templates/k3s-app/base/kustomization.yaml "$DEST/base/kustomization.yaml"
cp templates/k3s-app/base/namespace.yaml "$DEST/base/namespace.yaml"
cp templates/k3s-app/base/deployment.yaml "$DEST/base/deployment.yaml"
cp templates/k3s-app/base/service.yaml "$DEST/base/service.yaml"
cp templates/k3s-app/overlays/prod/kustomization.yaml "$DEST/overlays/prod/kustomization.yaml"

find "$DEST" -type f -print0 | xargs -0 sed -i \
  -e "s|<APP_NAME>|$APP_NAME|g" \
  -e "s|<APP_NAMESPACE>|$NAMESPACE|g" \
  -e "s|<GHCR_IMAGE>|$GHCR_IMAGE|g" \
  -e "s|<CONTAINER_NAME>|$CONTAINER_NAME|g" \
  -e "s|<CONTAINER_PORT>|$CONTAINER_PORT|g" \
  -e "s|<SERVICE_PORT>|$SERVICE_PORT|g" \
  -e 's|<IMAGE_TAG>|REPLACE_WITH_GIT_SHA|g'

echo "Created $DEST"
echo "Next: add $DEST/overlays/prod to environments/prod/kustomization.yaml and wire image promotion/reconcile."
