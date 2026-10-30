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
scope=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --data-urlencode)
      case "$2" in
        scope=*) scope="${2#scope=}" ;;
      esac
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done
printf '%s\n' "$scope" >> "$GHCR_TEST_SCOPE_LOG"
package="${scope#repository:}"
package="${package%:pull}"
if [ "${GHCR_TEST_DENY_PACKAGE:-}" = "$package" ]; then
  echo "simulated package authorization failure" >&2
  exit 22
fi
printf '{"token":"test-only-token"}\n'
MOCK
chmod +x "$tmp_dir/bin/curl"

scope_log="$tmp_dir/scopes.log"
: > "$scope_log"
if ! PATH="$tmp_dir/bin:$PATH" \
  GHCR_TEST_SCOPE_LOG="$scope_log" \
  GHCR_USERNAME=test-user \
  GHCR_TOKEN=test-only-secret \
  TARGET_APP=stockdividend \
  bash "$validator" >"$tmp_dir/success.log" 2>&1; then
  cat "$tmp_dir/success.log" >&2
  echo "Expected stockdividend package access preflight to pass." >&2
  exit 1
fi

grep -Fxq 'repository:phanthienquoc/stockdividend/admin:pull' "$scope_log"
grep -Fxq 'repository:phanthienquoc/stockdividend/backend:pull' "$scope_log"
if grep -Eq 'media-generation|tce-dashboard|auth-service' "$scope_log"; then
  echo "Targeted preflight checked unrelated packages." >&2
  cat "$scope_log" >&2
  exit 1
fi
if grep -q 'test-only-secret' "$tmp_dir/success.log"; then
  echo "Preflight leaked a test token to output." >&2
  exit 1
fi

: > "$scope_log"
if PATH="$tmp_dir/bin:$PATH" \
  GHCR_TEST_SCOPE_LOG="$scope_log" \
  GHCR_TEST_DENY_PACKAGE=phanthienquoc/stockdividend/admin \
  GHCR_USERNAME=test-user \
  GHCR_TOKEN=test-only-secret \
  TARGET_APP=stockdividend \
  bash "$validator" >"$tmp_dir/failure.log" 2>&1; then
  echo "Expected denied package access to fail the preflight." >&2
  exit 1
fi

grep -Fq 'cannot obtain pull access for ghcr.io/phanthienquoc/stockdividend/admin' "$tmp_dir/failure.log"
if grep -q 'test-only-secret' "$tmp_dir/failure.log"; then
  echo "Failed preflight leaked a test token to output." >&2
  exit 1
fi

echo "GHCR pull-access preflight regression tests passed."
