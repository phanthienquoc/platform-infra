#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
validator="$repo_root/scripts/validate-ghcr-pull-access.sh"
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
      auth_header="${args[$i]}"
      ;;
  esac
done

if [[ "$url" == "https://ghcr.io/token" ]]; then
  printf '%s\n' "$scope" >> "$GHCR_TEST_SCOPE_LOG"
  package="${scope#repository:}"
  package="${package%:pull}"
  if [ "${GHCR_TEST_DENY_TOKEN_PACKAGE:-}" = "$package" ]; then
    echo "simulated token endpoint denial" >&2
    exit 22
  fi
  printf '{"token":"test-only-token"}\n'
  exit 0
fi

if [[ "$url" == https://ghcr.io/v2/*/tags/list\?n=1 ]]; then
  package="${url#https://ghcr.io/v2/}"
  package="${package%%/tags/list*}"
  printf '%s\n' "$package" >> "$GHCR_TEST_RESOURCE_LOG"
  if [ "$auth_header" != "Authorization: Bearer test-only-token" ]; then
    echo "missing or invalid scoped bearer token" >&2
    exit 22
  fi
  if [ "${GHCR_TEST_DENY_RESOURCE_PACKAGE:-}" = "$package" ]; then
    echo "simulated package resource denial" >&2
    exit 22
  fi
  printf '{"name":"%s","tags":["test-tag"]}\n' "$package"
  exit 0
fi

echo "unexpected GHCR test URL: $url" >&2
exit 22
MOCK
chmod +x "$tmp_dir/bin/curl"

scope_log="$tmp_dir/scopes.log"
resource_log="$tmp_dir/resources.log"
: > "$scope_log"
: > "$resource_log"
if ! env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_RESOURCE_LOG="$resource_log" GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret TARGET_APP=stockdividend bash "$validator" >"$tmp_dir/success.log" 2>&1; then
  cat "$tmp_dir/success.log" >&2
  echo "Expected stockdividend package access preflight to pass." >&2
  exit 1
fi

grep -Fxq 'repository:phanthienquoc/stockdividend/admin:pull' "$scope_log"
grep -Fxq 'repository:phanthienquoc/stockdividend/backend:pull' "$scope_log"
grep -Fxq 'phanthienquoc/stockdividend/admin' "$resource_log"
grep -Fxq 'phanthienquoc/stockdividend/backend' "$resource_log"
if grep -Eq 'media-generation|tce-dashboard|auth-service' "$scope_log" "$resource_log"; then
  echo "Targeted preflight checked unrelated packages." >&2
  cat "$scope_log" "$resource_log" >&2
  exit 1
fi
if grep -q 'test-only-secret\|test-only-token' "$tmp_dir/success.log"; then
  echo "Preflight leaked a test token to output." >&2
  exit 1
fi

: > "$scope_log"
: > "$resource_log"
if env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_RESOURCE_LOG="$resource_log" GHCR_TEST_DENY_TOKEN_PACKAGE=phanthienquoc/stockdividend/admin GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret TARGET_APP=stockdividend bash "$validator" >"$tmp_dir/token-failure.log" 2>&1; then
  echo "Expected denied token authorization to fail the preflight." >&2
  exit 1
fi
grep -Fq 'cannot obtain pull access for ghcr.io/phanthienquoc/stockdividend/admin' "$tmp_dir/token-failure.log"
if grep -q 'test-only-secret\|test-only-token' "$tmp_dir/token-failure.log"; then
  echo "Failed token preflight leaked a test token to output." >&2
  exit 1
fi

: > "$scope_log"
: > "$resource_log"
if env PATH="$tmp_dir/bin:$PATH" GHCR_TEST_SCOPE_LOG="$scope_log" GHCR_TEST_RESOURCE_LOG="$resource_log" GHCR_TEST_DENY_RESOURCE_PACKAGE=phanthienquoc/stockdividend/admin GHCR_USERNAME=test-user GHCR_TOKEN=test-only-secret TARGET_APP=stockdividend bash "$validator" >"$tmp_dir/resource-failure.log" 2>&1; then
  echo "Expected package resource denial to fail even when the token endpoint returned a token." >&2
  exit 1
fi
grep -Fq 'cannot read ghcr.io/phanthienquoc/stockdividend/admin' "$tmp_dir/resource-failure.log"
grep -Fxq 'phanthienquoc/stockdividend/admin' "$resource_log"
if grep -q 'test-only-secret\|test-only-token' "$tmp_dir/resource-failure.log"; then
  echo "Failed package preflight leaked a test token to output." >&2
  exit 1
fi

echo "GHCR pull-access preflight regression tests passed."
MOCK