#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
bootstrap_script="$repo_root/scripts/bootstrap-runner.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin" "$tmp/fixtures"

# Extract the exact production wrapper emitted by the approved bootstrap script.
awk '/^cat >\/usr\/local\/sbin\/platform-kubectl <<.EOF.$/ { capture=1; next } capture && /^EOF$/ { exit } capture { print }' \
  "$bootstrap_script" > "$tmp/platform-kubectl"
test -s "$tmp/platform-kubectl"

# Replace only the binary path in the extracted test copy; production has no env override.
sed -i "s|^KUBECTL=(/usr/local/bin/k3s kubectl)$|KUBECTL=(\"$tmp/bin/mock-kubectl\")|" \
  "$tmp/platform-kubectl"
grep -Fq "KUBECTL=(\"$tmp/bin/mock-kubectl\")" "$tmp/platform-kubectl"

cat > "$tmp/bin/mock-kubectl" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail

[[ "${1:-}" == "-n" ]] || { echo "unexpected kubectl arguments: $*" >&2; exit 64; }
namespace="$2"
case "${3:-}/${4:-}" in
  get/deployment)
    deployment="$5"
    printf '{"spec":{"selector":{"matchLabels":{"app":"%s"}}}}\n' "$deployment"
    ;;
  get/pods)
    selector="$6"
    deployment="${selector#app=}"
    fixture="$MOCK_FIXTURE_DIR/$MOCK_MODE-$deployment.json"
    [[ -f "$fixture" ]] || { echo "missing fixture: $fixture" >&2; exit 65; }
    cat "$fixture"
    ;;
  rollout/restart)
    deployment="${5#deployment/}"
    printf '%s/%s\n' "$namespace" "$deployment" >> "$MOCK_RESTART_LOG"
    ;;
  *)
    echo "unexpected kubectl arguments: $*" >&2
    exit 64
    ;;
esac
MOCK
chmod +x "$tmp/bin/mock-kubectl"

export MOCK_FIXTURE_DIR="$tmp/fixtures"
export MOCK_RESTART_LOG="$tmp/restarts.log"
: > "$MOCK_RESTART_LOG"

write_waiting_fixture() {
  local mode="$1"
  local deployment="$2"
  local reason="$3"
  local message="$4"
  printf '{"items":[{"status":{"containerStatuses":[{"name":"app","state":{"waiting":{"reason":"%s","message":"%s"}}}],"initContainerStatuses":[]}}]}\n' \
    "$reason" "$message" > "$MOCK_FIXTURE_DIR/$mode-$deployment.json"
}

write_empty_fixture() {
  local mode="$1"
  local deployment="$2"
  printf '{"items":[]}\n' > "$MOCK_FIXTURE_DIR/$mode-$deployment.json"
}

run_helper() {
  local mode="$1"
  MOCK_MODE="$mode" "$tmp/platform-kubectl" restart-blocked-image-pulls stockdividend
}

# Permanent architecture/manifest errors must not create replacement Pods.
write_waiting_fixture permanent stock-admin ImagePullBackOff "no match for platform in manifest"
write_waiting_fixture permanent stock-backend ErrImagePull "manifest unknown"
write_waiting_fixture permanent stock-frontend ImagePullBackOff "manifest not found"
permanent_output="$(run_helper permanent 2>&1)"
grep -Fq "Permanent image-pull failure" <<< "$permanent_output"
grep -Fq "skipping rollout restart" <<< "$permanent_output"
[[ ! -s "$MOCK_RESTART_LOG" ]] || {
  echo "Permanent image-pull failures unexpectedly triggered a rollout restart." >&2
  cat "$MOCK_RESTART_LOG" >&2
  exit 1
}

# Transient authentication, network and rate-limit failures remain retryable
# because reconciliation refreshes the shared GHCR pull Secret before this helper.
write_waiting_fixture transient stock-admin ImagePullBackOff "failed to fetch oauth token: 401 Unauthorized after pull-secret refresh"
write_waiting_fixture transient stock-backend ErrImagePull "connection reset by peer"
write_waiting_fixture transient stock-frontend ImagePullBackOff "429 Too Many Requests"
: > "$MOCK_RESTART_LOG"
transient_output="$(run_helper transient 2>&1)"
grep -Fq "Transient image-pull failure" <<< "$transient_output"
expected_restarts=$'stock-prod/stock-admin\nstock-prod/stock-backend\nstock-prod/stock-frontend'
actual_restarts="$(cat "$MOCK_RESTART_LOG")"
[[ "$actual_restarts" == "$expected_restarts" ]] || {
  echo "Transient failures did not restart exactly the selected StockDividend Deployments." >&2
  printf 'expected:\n%s\nactual:\n%s\n' "$expected_restarts" "$actual_restarts" >&2
  exit 1
}

# A Deployment with mixed permanent and transient Pod errors is fail-closed:
# restarting it would still create Pods for the permanent bad image reference.
cat > "$MOCK_FIXTURE_DIR/mixed-stock-admin.json" <<'JSON'
{"items":[{"status":{"containerStatuses":[
  {"name":"permanent","state":{"waiting":{"reason":"ImagePullBackOff","message":"no match for platform in manifest"}}},
  {"name":"transient","state":{"waiting":{"reason":"ErrImagePull","message":"connection reset by peer"}}}
]}}]}
JSON
write_empty_fixture mixed stock-backend
write_empty_fixture mixed stock-frontend
: > "$MOCK_RESTART_LOG"
mixed_output="$(run_helper mixed 2>&1)"
grep -Fq "skipping rollout restart" <<< "$mixed_output"
[[ ! -s "$MOCK_RESTART_LOG" ]] || {
  echo "Mixed permanent/transient errors unexpectedly triggered a rollout restart." >&2
  cat "$MOCK_RESTART_LOG" >&2
  exit 1
}

# Non-image-pull waiting reasons must not trigger this recovery path.
write_waiting_fixture unrelated stock-admin CrashLoopBackOff "application process exited"
write_empty_fixture unrelated stock-backend
write_empty_fixture unrelated stock-frontend
: > "$MOCK_RESTART_LOG"
unrelated_output="$(run_helper unrelated 2>&1)"
grep -Fq "No image-pull failures for stock-prod/stock-admin" <<< "$unrelated_output"
[[ ! -s "$MOCK_RESTART_LOG" ]] || {
  echo "A non-image-pull failure unexpectedly triggered a rollout restart." >&2
  cat "$MOCK_RESTART_LOG" >&2
  exit 1
}

echo "Permanent/transient image-pull restart regression tests passed."
