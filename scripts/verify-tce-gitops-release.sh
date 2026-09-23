#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

manifest="apps/tce-dashboard/overlays/prod/kustomization.yaml"

extract_tag() {
  local image_name="$1"
  awk -v image_name="$image_name" '
    $0 ~ "name: " image_name "$" {found=1; next}
    found && /newTag:/ {print $2; exit}
  ' "$manifest"
}

web_tag="$(extract_tag 'ghcr.io/phanthienquoc/tce-dashboard/web')"
service_tag="$(extract_tag 'ghcr.io/phanthienquoc/tce-dashboard/service')"

test -n "$web_tag"
test -n "$service_tag"

case "$web_tag" in
  prod-v[0-9]*.[0-9]*.[0-9]*-[0-9a-f]*) ;;
  *) echo "ERROR: invalid TCE frontend release tag: $web_tag" >&2; exit 1 ;;
esac

case "$service_tag" in
  prod-v[0-9]*.[0-9]*.[0-9]*-[0-9a-f]*) ;;
  *) echo "ERROR: invalid TCE service release tag: $service_tag" >&2; exit 1 ;;
esac

echo "TCE frontend release: $web_tag"
echo "TCE service release:  $service_tag"

if [[ "$web_tag" != "$service_tag" ]]; then
  echo "ERROR: TCE frontend and service must be promoted as one immutable release." >&2
  echo "Refusing reconciliation with mixed TCE release tags." >&2
  exit 1
fi

echo "TCE GitOps release pairing passed: $web_tag"
