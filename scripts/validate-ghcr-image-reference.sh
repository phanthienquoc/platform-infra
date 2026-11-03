#!/usr/bin/env bash
set -euo pipefail

GHCR_USERNAME="${GHCR_USERNAME:-}"
GHCR_TOKEN="${GHCR_TOKEN:-}"
GHCR_IMAGE_REFERENCE="${GHCR_IMAGE_REFERENCE:-}"
GHCR_EXPECTED_DIGEST="${GHCR_EXPECTED_DIGEST:-}"

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

if [[ -n "$GHCR_EXPECTED_DIGEST" && ! "$GHCR_EXPECTED_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]]; then
  echo "::error::GHCR_EXPECTED_DIGEST must use sha256:<64 lowercase hex>." >&2
  exit 1
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
headers_file="$(mktemp)"
trap 'unset bearer_token; rm -f "$headers_file"' EXIT

manifest_url="https://ghcr.io/v2/${package}/manifests/${selector}"
manifest_json=""
if ! manifest_json="$(curl --dump-header "$headers_file" --fail --silent --show-error --connect-timeout 10 --max-time 20 --retry 2 --retry-delay 1 \
  -H "Authorization: Bearer $bearer_token" \
  -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.docker.distribution.manifest.v2+json" \
  "$manifest_url")"; then
  echo "::error::Cannot read exact GHCR manifest $GHCR_IMAGE_REFERENCE. Verify the immutable tag/digest exists and the PAT owner can pull this package; no GitOps mutation should proceed." >&2
  exit 1
fi

if [[ -n "$GHCR_EXPECTED_DIGEST" ]]; then
  actual_digest="$(awk 'tolower($1) == "docker-content-digest:" { gsub("\r", "", $2); digest=$2 } END { print digest }' "$headers_file")"
  if [[ "$actual_digest" != "$GHCR_EXPECTED_DIGEST" ]]; then
    echo "::error::GHCR tag $GHCR_IMAGE_REFERENCE resolved to ${actual_digest:-no Docker-Content-Digest header}, expected $GHCR_EXPECTED_DIGEST." >&2
    exit 1
  fi
  echo "Verified GHCR tag-to-digest mapping: $GHCR_IMAGE_REFERENCE -> $actual_digest."
fi

# Multi-platform indexes expose architecture on each manifest descriptor.
if jq -e '.manifests | type == "array"' <<< "$manifest_json" >/dev/null 2>&1; then
  if ! jq -e '[.manifests[]? | select(.platform.os == "linux" and .platform.architecture == "arm64")] | length > 0' <<< "$manifest_json" >/dev/null; then
    platforms="$(jq -r '[.manifests[]? | select(.platform != null) | "\(.platform.os // "unknown")/\(.platform.architecture // "unknown")"] | unique | join(", ")' <<< "$manifest_json")"
    echo "::error::GHCR image $GHCR_IMAGE_REFERENCE does not publish linux/arm64 in its manifest index (found: ${platforms:-no platform descriptors})." >&2
    exit 1
  fi
  echo "Verified exact GHCR manifest: $GHCR_IMAGE_REFERENCE (linux/arm64 manifest index)."
else
  # Single-platform OCI/Docker manifests store OS and architecture in the config blob.
  config_digest="$(jq -er '.config.digest // empty' <<< "$manifest_json" 2>/dev/null || true)"
  if [[ ! "$config_digest" =~ ^sha256:[0-9a-f]{64}$ ]]; then
    echo "::error::GHCR manifest for $GHCR_IMAGE_REFERENCE is neither an image index nor a valid single-image manifest." >&2
    exit 1
  fi

  config_json=""
  if ! config_json="$(curl --fail --silent --show-error --connect-timeout 10 --max-time 20 --retry 2 --retry-delay 1 \
    -H "Authorization: Bearer $bearer_token" \
    -H "Accept: application/vnd.oci.image.config.v1+json, application/vnd.docker.container.image.v1+json" \
    "https://ghcr.io/v2/$package/blobs/$config_digest")"; then
    echo "::error::Could not read the image config for $GHCR_IMAGE_REFERENCE; refusing to infer its platform." >&2
    exit 1
  fi

  image_os="$(jq -r '.os // empty' <<< "$config_json")"
  image_arch="$(jq -r '.architecture // empty' <<< "$config_json")"
  if [[ "$image_os" != "linux" || "$image_arch" != "arm64" ]]; then
    echo "::error::GHCR image $GHCR_IMAGE_REFERENCE does not support linux/arm64 (resolved config: ${image_os:-unknown}/${image_arch:-unknown})." >&2
    exit 1
  fi
  echo "Verified exact GHCR manifest: $GHCR_IMAGE_REFERENCE (single-image config linux/arm64)."
fi
