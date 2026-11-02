#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

manifest="apps/tce-dashboard/overlays/prod/kustomization.yaml"
desired_web_ref="$(python3 scripts/resolve-tce-gitops-image-refs.py --file "$manifest" --component web)"
desired_service_ref="$(python3 scripts/resolve-tce-gitops-image-refs.py --file "$manifest" --component service)"

to_image_reference() {
  local component="$1"
  local reference="$2"
  case "$reference" in
    tag:*) printf 'ghcr.io/phanthienquoc/tce-dashboard/%s:%s' "$component" "${reference#tag:}" ;;
    digest:*) printf 'ghcr.io/phanthienquoc/tce-dashboard/%s@%s' "$component" "${reference#digest:}" ;;
    *) echo "ERROR: invalid resolved TCE reference: $reference" >&2; return 1 ;;
  esac
}

expected_web="$(to_image_reference web "$desired_web_ref")"
expected_service="$(to_image_reference service "$desired_service_ref")"

live_json="$(mktemp)"
trap 'rm -f "$live_json"' EXIT

sudo /usr/local/sbin/platform-kubectl get deployments -n tce-prod -o json | tee "$live_json" >/dev/null

live_web="$(jq -r '.items[] | select(.metadata.name=="tce-frontend") | .spec.template.spec.containers[] | select(.name=="frontend") | .image' "$live_json")"
live_service="$(jq -r '.items[] | select(.metadata.name=="tce-service") | .spec.template.spec.containers[] | select(.name=="service") | .image' "$live_json")"

echo "TCE frontend:"
echo "  desired: $expected_web"
echo "  live:    $live_web"
echo "TCE service:"
echo "  desired: $expected_service"
echo "  live:    $live_service"

if [[ "$live_web" != "$expected_web" ]]; then
  echo "ERROR: tce-frontend is not running the GitOps image." >&2
  exit 1
fi

if [[ "$live_service" != "$expected_service" ]]; then
  echo "ERROR: tce-service is not running the GitOps image." >&2
  exit 1
fi

echo "TCE GitOps image verification passed."
