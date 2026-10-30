#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
health_gate="$repo_root/scripts/verify-workload-health.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

cat > "$tmp_dir/kubectl-mock" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail

action="${1:-}"
resource="${2:-}"
shift 2
while [ "$#" -gt 0 ]; do
  case "$1" in
    -n|-l|-o)
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

[ "$action" = "get" ] || exit 2

case "$resource" in
  pods)
    case "$HEALTH_GATE_TEST_SCENARIO" in
      healthy)
        printf 'pod-1\t\tRunning\ttrue:: \n'
        ;;
      terminating-only)
        printf 'pod-1\t2026-10-30T13:00:00Z\tRunning\ttrue:: \n'
        ;;
      image-pull)
        printf 'pod-1\t\tPending\tfalse:ImagePullBackOff: \n'
        ;;
      no-pods)
        exit 0
        ;;
      *)
        exit 3
        ;;
    esac
    ;;
  deployments)
    case "$HEALTH_GATE_TEST_SCENARIO" in
      healthy)
        printf 'stock-admin\t1\t1\t1\n'
        ;;
      terminating-only|image-pull|no-pods)
        printf 'stock-admin\t1\t0\t0\n'
        ;;
      *)
        exit 3
        ;;
    esac
    ;;
  *)
    exit 2
    ;;
esac
MOCK

chmod +x "$tmp_dir/kubectl-mock"

run_case() {
  local scenario="$1"
  local expected_status="$2"
  local actual_status=0

  if HEALTH_GATE_TEST_SCENARIO="$scenario" \
    HEALTH_GATE_KUBECTL_BIN="$tmp_dir/kubectl-mock" \
    TARGET_APP=stockdividend \
    "$health_gate" >"$tmp_dir/$scenario.log" 2>&1; then
    actual_status=0
  else
    actual_status=$?
  fi

  if [ "$actual_status" -ne "$expected_status" ]; then
    cat "$tmp_dir/$scenario.log" >&2
    echo "Expected $scenario to exit $expected_status, got $actual_status." >&2
    exit 1
  fi
}

run_case healthy 0
run_case terminating-only 1
run_case image-pull 1
run_case no-pods 1

echo "Workload health gate regression tests passed."
