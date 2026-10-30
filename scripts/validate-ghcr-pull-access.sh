#!/usr/bin/env bash
set -euo pipefail

TARGET_APP="${TARGET_APP:-all}"
GHCR_USERNAME="${GHCR_USERNAME:-}"
GHCR_TOKEN="${GHCR_TOKEN:-}"

if [[ -z "$GHCR_USERNAME" || -z "$GHCR_TOKEN" ]]; then
  echo "::error::GHCR_USERNAME and GHCR_READ_TOKEN are required for pull-access preflight." >&2
  exit 1
fi

if [ "$TARGET_APP" = "keycloak" ]; then
  echo "Keycloak uses quay.io; GHCR pull-access preflight is not applicable."
  exit 0
fi

case "$TARGET_APP" in
  all|auth-service|tce-dashboard|stockdividend|media-generation|microfe) ;;
  *)
    echo "::error::Unsupported deployment scope for GHCR pull-access preflight: $TARGET_APP" >&2
    exit 1
    ;;
esac

mapfile -t all_packages < <(
  {
    grep -hE '^[[:space:]]*name:[[:space:]]*ghcr\.io/' apps/*/overlays/prod/kustomization.yaml platform/auth-service/kustomization.yaml 2>/dev/null || true
    find platform/microfe -type f \( -name '*.yaml' -o -name '*.yml' \) -print0 |
      xargs -0 -r grep -hE '^[[:space:]]*image:[[:space:]]*ghcr\.io/' || true
  } |
    sed -E 's/^[[:space:]]*(name:|image:)[[:space:]]*ghcr\.io\///; s/[[:space:]]*$//' |
    sed -E 's/:([^/:]+)$//' |
    sort -u
)

packages=()
for package in "${all_packages[@]}"; do
  include=0
  case "$TARGET_APP" in
    all) include=1 ;;
    auth-service)
      [[ "$package" == phanthienquoc/auth-service/* ]] && include=1
      ;;
    tce-dashboard)
      [[ "$package" == phanthienquoc/tce-dashboard/* ]] && include=1
      ;;
    stockdividend)
      [[ "$package" == phanthienquoc/stockdividend/* ]] && include=1
      ;;
    media-generation)
      [[ "$package" == phanthienquoc/media-generation/* ]] && include=1
      ;;
    microfe)
      [[ "$package" == phanthienquoc/microfe-* ]] && include=1
      ;;
  esac
  if [ "$include" -eq 1 ]; then
    packages+=("$package")
  fi
done

if [ "${#packages[@]}" -eq 0 ]; then
  echo "::error::No GHCR production packages found for target $TARGET_APP; refusing to rotate pull credentials." >&2
  exit 1
fi

failed=0
for package in "${packages[@]}"; do
  # Read the bearer token response only through grep; never print or persist it.
  if printf 'user = "%s:%s"\n' "$GHCR_USERNAME" "$GHCR_TOKEN" |
    curl --config - --get --silent --show-error --fail \
      --connect-timeout 10 --max-time 20 --retry 2 --retry-delay 1 \
      --data-urlencode "service=ghcr.io" \
      --data-urlencode "scope=repository:${package}:pull" \
      "https://ghcr.io/token" |
    grep -Eq '"(token|access_token)"[[:space:]]*:[[:space:]]*"[^"]+"'; then
    echo "Verified GHCR pull authorization for ghcr.io/$package"
  else
    echo "::error::GHCR_READ_TOKEN cannot obtain pull access for ghcr.io/$package; verify classic PAT read:packages scope and package-level access." >&2
    failed=1
  fi
done

if [ "$failed" -ne 0 ]; then
  echo "::error::GHCR pull-access preflight failed; cluster pull credentials were not changed and blocked pods were not restarted." >&2
  exit 1
fi

echo "GHCR pull-access preflight passed for target $TARGET_APP."
