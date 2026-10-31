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
deployment_selector=""
shift 2
while [ "$#" -gt 0 ]; do
  case "$1" in
    -n|-o)
      shift 2
      ;;
    -l)
      if [ "$resource" = "deployments" ]; then
        deployment_selector="${2:-}"
      fi
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
        printf 'pod-1||Running|true:: \n'
        ;;
      terminating-only)
        printf 'pod-1|2026-10-30T13:00:00Z|Running|true:: \n'
        ;;
      image-pull)
        printf 'pod-1||Pending|false:ImagePullBackOff: \n'
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
    # Simulate the real manifests: scoped Deployments do not carry the same
    # metadata labels as their pod templates.
    [ -z "$deployment_selector" ] || exit 0
    case "$HEALTH_GATE_TEST_SCENARIO" in
      healthy)
        case "$TARGET_APP" in
          stockdividend) printf 'stock-admin|1|1|1\n' ;;
          auth-service) printf 'microfe-auth|1|1|1\n' ;;
          keycloak) printf 'keycloak|1|1|1\n' ;;
          microfe)
            printf 'microfe-shell|1|1|1\n'
            printf 'microfe-ws|1|1|1\n'
            ;;
          *) exit 3 ;;
        esac
        ;;
      terminating-only|image-pull|no-pods)
        printf 'stock-admin|1|0|0\n'
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
  local target_app="${3:-stockdividend}"
  local actual_status=0

  if HEALTH_GATE_TEST_SCENARIO="$scenario" \
    HEALTH_GATE_KUBECTL_BIN="$tmp_dir/kubectl-mock" \
    TARGET_APP="$target_app" \
    bash "$health_gate" >"$tmp_dir/$scenario-$target_app.log" 2>&1; then
    actual_status=0
  else
    actual_status=$?
  fi

  if [ "$actual_status" -ne "$expected_status" ]; then
    cat "$tmp_dir/$scenario-$target_app.log" >&2
    echo "Expected $scenario/$target_app to exit $expected_status, got $actual_status." >&2
    exit 1
  fi
}

run_case healthy 0 stockdividend
run_case terminating-only 1 stockdividend
run_case image-pull 1 stockdividend
run_case no-pods 1 stockdividend
run_case healthy 0 auth-service
run_case healthy 0 keycloak
run_case healthy 0 microfe
echo "Workload health gate regression tests passed."
