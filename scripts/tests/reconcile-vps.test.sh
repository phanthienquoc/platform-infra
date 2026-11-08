#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cat > "$TMP/sudo" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
exec "$@"
SH

cat > "$TMP/curl" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
output=""
while (($#)); do
  case "$1" in
    --output) output="$2"; shift 2 ;;
    *) shift ;;
  esac
done
[[ -n "$output" ]] || { echo "fake curl requires --output" >&2; exit 2; }
printf 'apiVersion: v1\nkind: Namespace\nmetadata:\n  name: cert-manager\n' > "$output"
SH

cat > "$TMP/sha256sum" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "--check" && "${2:-}" == "--status" ]]; then
  cat >/dev/null
  [[ "${SHA256_FAIL:-0}" != "1" ]]
  exit $?
fi
exec /usr/bin/sha256sum "$@"
SH

cat > "$TMP/platform-kubectl" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$CALL_LOG"

if [[ "$1" == "get" && "$2" == "namespace" ]]; then
  namespace="$3"
  if [[ "${NAMESPACE_ERROR:-}" == "$namespace" ]]; then
    echo "Unable to connect to the server: connection refused" >&2
    exit 1
  fi
  if [[ "${MISSING_NAMESPACE:-}" == "$namespace" ]]; then
    echo "Error from server (NotFound): namespaces \"$namespace\" not found" >&2
    exit 1
  fi
  echo "namespace/$namespace"
  exit 0
fi

if [[ "$1" == "diff" ]]; then
  exit "${DIFF_EXIT:-0}"
fi

if [[ "$1" == "apply" ]]; then
  exit 0
fi

echo "Unexpected fake platform-kubectl invocation: $*" >&2
exit 64
SH

chmod +x "$TMP/sudo" "$TMP/curl" "$TMP/sha256sum" "$TMP/platform-kubectl"

run_script() {
  local mode="$1"
  shift
  : > "$TMP/calls"
  local rc=0
  env \
    PATH="$TMP:$PATH" \
    PLATFORM_KUBECTL_BIN="$TMP/platform-kubectl" \
    CALL_LOG="$TMP/calls" \
    GITHUB_WORKSPACE="$ROOT" \
    "$@" \
    bash "$ROOT/scripts/reconcile-vps.sh" "$mode" || rc=$?
  if [[ -e "$ROOT/platform/cert-manager/cert-manager.yaml" ]]; then
    echo "Generated cert-manager manifest was not cleaned up after reconciliation." >&2
    return 1
  fi
  return "$rc"
}

assert_no_apply() {
  if grep -Eq '(^|[[:space:]])apply([[:space:]]|$)' "$TMP/calls"; then
    echo "Unexpected Kubernetes mutation in read-only path:" >&2
    cat "$TMP/calls" >&2
    exit 1
  fi
}

assert_one_production_apply() {
  local count
  count="$(grep -F -c 'apply -k environments/prod' "$TMP/calls" || true)"
  [[ "$count" == "1" ]] || {
    echo "Expected exactly one production Kustomize apply, found $count:" >&2
    cat "$TMP/calls" >&2
    exit 1
  }
}

# A clean plan performs namespace reads and a diff, never an apply.
if run_script plan; then rc=0; else rc=$?; fi
[[ "$rc" == "0" ]]
grep -Fq 'get namespace k3s-debug -o name' "$TMP/calls"
grep -Fq 'get namespace microfe-platform -o name' "$TMP/calls"
grep -Fq 'get namespace tce-prod -o name' "$TMP/calls"
grep -Fq 'diff -k environments/prod' "$TMP/calls"
assert_no_apply

# A release asset checksum mismatch fails closed before any cluster read or mutation.
if run_script plan SHA256_FAIL=1; then rc=0; else rc=$?; fi
[[ "$rc" == "1" ]]
assert_no_apply

# Missing declared namespaces are reported as drift without being created.
if run_script plan MISSING_NAMESPACE=tce-prod; then rc=0; else rc=$?; fi
[[ "$rc" == "1" ]]
if grep -Fq 'diff -k environments/prod' "$TMP/calls"; then
  echo "Missing namespace should short-circuit before kubectl diff." >&2
  exit 1
fi
assert_no_apply

# Explicit apply creates declared namespaces only through the production Kustomize root.
if run_script apply MISSING_NAMESPACE=tce-prod; then rc=0; else rc=$?; fi
[[ "$rc" == "0" ]]
assert_one_production_apply

# An API/connectivity error is not misclassified as missing-namespace drift.
if run_script apply NAMESPACE_ERROR=tce-prod; then rc=0; else rc=$?; fi
[[ "$rc" == "2" ]]
assert_no_apply

# A diff API error fails closed and never reaches apply.
if run_script apply DIFF_EXIT=2; then rc=0; else rc=$?; fi
[[ "$rc" == "2" ]]
assert_no_apply

# Actual drift permits one explicit apply.
if run_script apply DIFF_EXIT=1; then rc=0; else rc=$?; fi
[[ "$rc" == "0" ]]
assert_one_production_apply

# A clean explicit apply is a no-op.
if run_script apply DIFF_EXIT=0; then rc=0; else rc=$?; fi
[[ "$rc" == "0" ]]
assert_no_apply

echo "reconcile-vps read-only plan and single-apply regression tests passed."
