#!/usr/bin/env bash
set -euo pipefail

GHCR_USERNAME="${GHCR_USERNAME:-}"
GHCR_TOKEN="${GHCR_TOKEN:-}"
GHCR_IMAGE_REFERENCE="${GHCR_IMAGE_REFERENCE:-}"

if [[ -z "$GHCR_USERNAME" || -z "$GHCR_TOKEN" || -z "$GHCR_IMAGE_REFERENCE" ]]; then
  echo "::error::GHCR_USERNAME, GHCR_TOKEN, and GHCR_IMAGE_REFERENCE are required for exact image verification." >&2
  exit 1
fi

if [[ "$GHCR_IMAGE_REFERENCE" != ghcr.io/phanthienquoc/* ]]; then
  echo "::error::Only approved phanthienquoc GHCR image references can be verified." >&2
  exit 1
fi

reference="${GHCR_IMAGE_REFERENCE#ghcr.io/}"
if [[ "$reference" == *@* ]]; then
  package="${reference%@*}"
  selector="${reference#*@}"
  if [[ ! "$selector" =~ ^sha256:[0-9a-f]{64}$ ]]; then
    echo "::error::Digest reference must use sha256:<64 lowercase hex>." >&2
    exit 1
  fi
else
  if [[ "$reference" != *:* ]]; then
    echo "::error::Image reference must include an immutable tag or sha256 digest." >&2
    exit 1
  fi
  package="${reference%:*}"
  selector="${reference##*:}"
  if [[ ! "$selector" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$ ]]; then
    echo "::error::Image tag is malformed." >&2
    exit 1
  fi
fi

if [[ ! "$package" =~ ^phanthienquoc/[a-z0-9._/-]+$ || "$package" == *..* || "$package" == *//* || "$package" == */ ]]; then
  echo "::error::GHCR package path is malformed." >&2
  exit 1
fi

token_response=""
if ! token_response="$(printf 'user = "%s:%s"\n' "$GHCR_USERNAME" "$GHCR_TOKEN" |
  curl --config - --get --silent --show-error --fail --connect-timeout 10 --max-time 20 --retry 2 --retry-delay 1 \
    --data-urlencode "service=ghcr.io" \
    --data-urlencode "scope=repository:${package}:pull" \
    "https://ghcr.io/token")"; then
  echo "::error::Could not obtain a pull-scoped GHCR token for $package; verify PAT read:packages and package access." >&2
  exit 1
fi

bearer_token=""
if ! bearer_token="$(printf '%s' "$token_response" | jq -er '.token // .access_token // empty' 2>/dev/null)" || [[ -z "$bearer_token" ]]; then
  echo "::error::GHCR returned no usable pull-scoped token for $package." >&2
  unset token_response bearer_token
  exit 1
fi
unset token_response

manifest_url="https://ghcr.io/v2/${package}/manifests/${selector}"
if ! curl --fail --silent --show-error --connect-timeout 10 --max-time 20 \
  -H "Authorization: Bearer $bearer_token" \
  -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.docker.distribution.manifest.v2+json" \
  "$manifest_url" >/dev/null; then
  echo "::error::Cannot read exact GHCR manifest $GHCR_IMAGE_REFERENCE. Verify the immutable tag/digest exists and the PAT owner can pull this package; no GitOps mutation should proceed." >&2
  unset bearer_token
  exit 1
fi
unset bearer_token

echo "Verified exact GHCR manifest: $GHCR_IMAGE_REFERENCE"
