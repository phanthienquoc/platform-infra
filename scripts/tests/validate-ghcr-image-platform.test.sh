#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/validate-ghcr-image-reference.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/bin"

cat > "$tmp_dir/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
cat >/dev/null
args=("$@")
url="${args[${#args[@]}-1]}"
scope=""
auth_header=""
for ((i=0; i<${#args[@]}; i++)); do
  case "${args[$i]}" in
    --data-urlencode)
      i=$((i+1))
      case "${args[$i]}" in
        scope=*) scope="${args[$i]#scope=}" ;;
      esac
      ;;
    -H|--header)
      i=$((i+1))
      case "${args[$i]}" in
        Authorization:*) auth_header="${args[$i]}" ;;
      esac
      ;;
  esac
done

if [[ "$url" == "https://ghcr.io/token" ]]; then
  printf '%s\n' "$scope" >> "$GHCR_TEST_SCOPE_LOG"
  printf '{"token":"test-only-scoped-token"}\n'
  exit 0
fi

if [[ "$url" == https://ghcr.io/v2/*/manifests/* ]]; then
  printf '%s\n' "$url" >> "$GHCR_TEST_MANIFEST_LOG"
  if [[ "$auth_header" != "Authorization: Bearer test-only-scoped-token" ]]; then
    echo "missing or invalid scoped bearer token" >&2
    exit 22
  fi
  if [[ "${GHCR_TEST_DENY_REFERENCE:-}" == "$url" ]]; then
    echo "simulated exact manifest denial" >&2
    exit 22
  fi
  case "${GHCR_TEST_SCENARIO:-index-arm64}" in
    index-arm64)
      printf '{"schemaVersion":2,"manifests":[{"platform":{"os":"linux","architecture":"arm64"}}]}\n'
      ;;
    index-amd64)
      printf '{"schemaVersion":2,"manifests":[{"platform":{"os":"linux","architecture":"amd64"}}]}\n'
      ;;
    single-arm64|single-amd64)
      printf '{"schemaVersion":2,"config":{"digest":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}\n'
      ;;
    unknown)
      printf '{"schemaVersion":2}\n'
      ;;
    *)
      echo "unknown test scenario" >&2
      exit 22
      ;;
  esac
  exit 0
fi

if [[ "$url" == https://ghcr.io/v2/*/blobs/* ]]; then
  printf '%s\n' "$url" >> "$GHCR_TEST_BLOB_LOG"
  if [[ "$auth_header" != "Authorization: Bearer test-only-scoped-token" ]]; then
    echo "missing or invalid scoped bearer token for config blob" >&2
    exit 22
  fi
  case "${GHCR_TEST_SCENARIO:-index-arm64}" in
    single-arm64) printf '{"os":"linux","architecture":"arm64"}\n' ;;
    single-amd64) printf '{"os":"linux","architecture":"amd64"}\n' ;;
    *) echo "unexpected config blob request" >&2; exit 22 ;;
  esac
  exit 0
fi

echo "unexpected GHCR test URL: $url" >&2
exit 22
MOCK
chmod +x "$tmp_dir/bin/curl"

scope_log="$tmp_dir/scopes.log"
manifest_log="$tmp_dir/manifests.log"
blob_log="$tmp_dir/blobs.log"
: > "$scope_log"
: > "$manifest_log"
: > "$blob_log"

run_case() {
  local scenario="$1"
  local reference="$2"
  local expected_status="$3"
  local label="$4"
  local actual_status=0
  if env PATH="$tmp_dir/bin:$PATH" \
    GHCR_TEST_SCOPE_LOG="$scope_log" \
    GHCR_TEST_MANIFEST_LOG="$manifest_log" \
    GHCR_TEST_BLOB_LOG="$blob_log" \
    GHCR_TEST_SCENARIO="$scenario" \
    GHCR_USERNAME=test-user \
    GHCR_TOKEN=test-only-secret \
    GHCR_IMAGE_REFERENCE="$reference" \
    bash "$validator" >"$tmp_dir/$label.log" 2>&1; then
    actual_status=0
  else
    actual_status=$?
  fi
  if [[ "$actual_status" -ne "$expected_status" ]]; then
    cat "$tmp_dir/$label.log" >&2
    echo "Expected $label to exit $expected_status, got $actual_status." >&2
    exit 1
  fi
  if grep -q 'test-only-secret\|test-only-scoped-token' "$tmp_dir/$label.log"; then
    echo "$label leaked a registry token." >&2
    exit 1
  fi
}

image="ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-abcdef123456789"
expected_url="https://ghcr.io/v2/phanthienquoc/media-generation/frontend/manifests/prod-v0.3.0-abcdef123456789"
run_case index-arm64 "$image" 0 index-arm64
grep -Fxq 'repository:phanthienquoc/media-generation/frontend:pull' "$scope_log"
grep -Fxq "$expected_url" "$manifest_log"
grep -Fq 'linux/arm64 manifest index' "$tmp_dir/index-arm64.log"

digest="sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
run_case index-arm64 "ghcr.io/phanthienquoc/media-generation/frontend@$digest" 0 digest-index-arm64
grep -Fxq "https://ghcr.io/v2/phanthienquoc/media-generation/frontend/manifests/$digest" "$manifest_log"

run_case single-arm64 "ghcr.io/phanthienquoc/stockdividend/admin:full-source-sha" 0 single-arm64
grep -Fq '/blobs/sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "$blob_log"
grep -Fq 'single-image config linux/arm64' "$tmp_dir/single-arm64.log"

run_case index-amd64 "$image" 1 index-amd64
grep -Fq 'does not publish linux/arm64 in its manifest index' "$tmp_dir/index-amd64.log"

run_case single-amd64 "ghcr.io/phanthienquoc/stockdividend/admin:wrong-arch" 1 single-amd64
grep -Fq 'does not support linux/arm64' "$tmp_dir/single-amd64.log"

run_case unknown "ghcr.io/phanthienquoc/stockdividend/admin:unknown-manifest" 1 unknown
grep -Fq 'neither an image index nor a valid single-image manifest' "$tmp_dir/unknown.log"

: > "$scope_log"
: > "$manifest_log"
if env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_MANIFEST_LOG="$manifest_log" GHCR_TEST_BLOB_LOG="$blob_log" GHCR_TEST_DENY_REFERENCE="$expected_url" GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret GHCR_IMAGE_REFERENCE="$image" bash "$validator" >"$tmp_dir/denied.log" 2>&1; then
  echo "Expected exact manifest denial to fail validation." >&2
  exit 1
fi
grep -Fq "Cannot read exact GHCR manifest $image" "$tmp_dir/denied.log"
if grep -q 'test-only-secret\|test-only-scoped-token' "$tmp_dir/denied.log"; then
  echo "Failed exact manifest validation leaked a registry token." >&2
  exit 1
fi

: > "$scope_log"
: > "$manifest_log"
if env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_MANIFEST_LOG="$manifest_log" GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret GHCR_IMAGE_REFERENCE="ghcr.io/another-owner/private/image:tag" bash "$validator" >"$tmp_dir/invalid.log" 2>&1; then
  echo "Expected an unapproved image owner to be rejected." >&2
  exit 1
fi
if [ -s "$scope_log" ] || [ -s "$manifest_log" ]; then
  echo "Invalid image reference unexpectedly made a registry request." >&2
  exit 1
fi
if grep -q 'test-only-secret\|test-only-scoped-token' "$tmp_dir/invalid.log"; then
  echo "Invalid image validation leaked a test token." >&2
  exit 1
fi

echo "GHCR exact-image and linux/arm64 platform validation regression tests passed."
