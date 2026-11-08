#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "\${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$ROOT/scripts/prepare-cert-manager-manifest.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
workspace="$tmp/workspace"
mkdir -p "$workspace/platform/cert-manager" "$tmp/bin"
curl_log="$tmp/curl-args.log"
output="$tmp/output"

cat > "$tmp/bin/curl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$@" > "$CURL_ARGS_LOG"
exit 22
MOCK
chmod +x "$tmp/bin/curl"

set +e
env GH_TOKEN=test-token PATH="$tmp/bin:$PATH" GITHUB_WORKSPACE="$workspace" CURL_ARGS_LOG="$curl_log" \
  bash "$SCRIPT" "$workspace/platform/cert-manager/cert-manager.yaml" > "$output" 2>&1
token_rc=$?
set -e
[[ "$token_rc" -ne 0 ]] || { echo "FAIL: mock download unexpectedly succeeded" >&2; exit 1; }
grep -Fxq "Authorization: Bearer test-token" "$curl_log"
if grep -Fq "test-token" "$output"; then
  echo "FAIL: release token was printed to command output" >&2
  exit 1
fi

: > "$curl_log"
set +e
env -u GH_TOKEN PATH="$tmp/bin:$PATH" GITHUB_WORKSPACE="$workspace" CURL_ARGS_LOG="$curl_log" \
  bash "$SCRIPT" "$workspace/platform/cert-manager/cert-manager.yaml" > "$output" 2>&1
anonymous_rc=$?
set -e
[[ "$anonymous_rc" -ne 0 ]] || { echo "FAIL: mock anonymous download unexpectedly succeeded" >&2; exit 1; }
if grep -Fq "Authorization: Bearer" "$curl_log"; then
  echo "FAIL: anonymous/local invocation unexpectedly supplied an Authorization header" >&2
  exit 1
fi
if grep -Fq "test-token" "$output"; then
  echo "FAIL: token leaked into command output" >&2
  exit 1
fi
if compgen -G "$workspace/platform/cert-manager/.cert-manager.yaml.*" >/dev/null; then
  echo "FAIL: temporary release asset was not cleaned up" >&2
  exit 1
fi

echo "Cert-manager release API auth regression passed; optional token is sent privately and never logged."
