#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

manifest="apps/tce-dashboard/overlays/prod/kustomization.yaml"

desired_web="$(awk '
  /name: ghcr.io\/phanthienquoc\/tce-dashboard\/web$/ {found=1; next}
  found && /newTag:/ {print $2; exit}
' "$manifest")"
desired_service="$(awk '
  /name: ghcr.io\/phanthienquoc\/tce-dashboard\/service$/ {found=1; next}
  found && /newTag:/ {print $2; exit}
' "$manifest")"

test -n "$desired_web"
test -n "$desired_service"

live_json="$(mktemp)"
trap 'rm -f "$live_json"' EXIT

sudo /usr/local/sbin/platform-kubectl get deployments -n tce-prod -o json | tee "$live_json" >/dev/null

live_web="$(jq -r '.items[] | select(.metadata.name=="tce-frontend") | .spec.template.spec.containers[] | select(.name=="frontend") | .image' "$live_json")"
live_service="$(jq -r '.items[] | select(.metadata.name=="tce-service") | .spec.template.spec.containers[] | select(.name=="service") | .image' "$live_json")"

expected_web="ghcr.io/phanthienquoc/tce-dashboard/web:$desired_web"
expected_service="ghcr.io/phanthienquoc/tce-dashboard/service:$desired_service"

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
