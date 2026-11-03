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
header_file=""
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
    --dump-header|-D)
      i=$((i+1))
      header_file="${args[$i]}"
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
  if [[ -n "$header_file" ]]; then
    printf 'HTTP/1.1 200 OK\r\nDocker-Content-Digest: %s\r\n\r\n' "${GHCR_TEST_MANIFEST_DIGEST:-sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}" > "$header_file"
  fi
  printf '{"schemaVersion":2,"manifests":[{"platform":{"os":"linux","architecture":"arm64"}}]}\n'
  exit 0
fi

echo "unexpected GHCR test URL: $url" >&2
exit 22
MOCK
chmod +x "$tmp_dir/bin/curl"

scope_log="$tmp_dir/scopes.log"
manifest_log="$tmp_dir/manifests.log"
: > "$scope_log"
: > "$manifest_log"
image="ghcr.io/phanthienquoc/microfe-shell:0123456789abcdef0123456789abcdef01234567"
expected_url="https://ghcr.io/v2/phanthienquoc/microfe-shell/manifests/0123456789abcdef0123456789abcdef01234567"
expected_digest="sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
if ! env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_MANIFEST_LOG="$manifest_log" GHCR_TEST_MANIFEST_DIGEST="$expected_digest" GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret GHCR_IMAGE_REFERENCE="$image" GHCR_EXPECTED_DIGEST="$expected_digest" bash "$validator" >"$tmp_dir/success.log" 2>&1; then
  cat "$tmp_dir/success.log" >&2
  echo "Expected exact GHCR manifest validation to pass." >&2
  exit 1
fi
grep -Fxq 'repository:phanthienquoc/microfe-shell:pull' "$scope_log"
grep -Fxq "$expected_url" "$manifest_log"
grep -Fq "Verified GHCR tag-to-digest mapping: $image -> $expected_digest." "$tmp_dir/success.log"
if grep -q 'test-only-secret\|test-only-scoped-token' "$tmp_dir/success.log"; then
  echo "Exact manifest validator leaked a test token." >&2
  exit 1
fi


: > "$scope_log"
: > "$manifest_log"
if env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_MANIFEST_LOG="$manifest_log" GHCR_TEST_MANIFEST_DIGEST="$expected_digest" GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret GHCR_IMAGE_REFERENCE="$image" GHCR_EXPECTED_DIGEST="sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" bash "$validator" >"$tmp_dir/mismatch.log" 2>&1; then
  echo "Expected a tag-to-digest mismatch to fail validation." >&2
  exit 1
fi
grep -Fq "expected sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" "$tmp_dir/mismatch.log"
: > "$scope_log"
: > "$manifest_log"
if env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_MANIFEST_LOG="$manifest_log" GHCR_TEST_DENY_REFERENCE="$expected_url" GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret GHCR_IMAGE_REFERENCE="$image" bash "$validator" >"$tmp_dir/denied.log" 2>&1; then
  echo "Expected exact manifest denial to fail validation." >&2
  exit 1
fi
grep -Fq "Cannot read exact GHCR manifest $image" "$tmp_dir/denied.log"
if grep -q 'test-only-secret\|test-only-scoped-token' "$tmp_dir/denied.log"; then
  echo "Failed exact manifest validation leaked a test token." >&2
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

echo "GHCR exact-image manifest validation regression tests passed."
