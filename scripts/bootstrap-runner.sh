#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${REPO_URL:-https://github.com/phanthienquoc/platform-infra}"
RUNNER_NAME="${RUNNER_NAME:-platform-k3s-01}"
RUNNER_USER="${RUNNER_USER:-github-runner}"
RUNNER_DIR="${RUNNER_DIR:-/opt/actions-runner}"
LABELS="${RUNNER_LABELS:-self-hosted,linux,arm64,platform-infra,k3s,vps}"
: "${RUNNER_TOKEN:?Set RUNNER_TOKEN to the short-lived GitHub runner registration token}"
if [[ "$(id -u)" -ne 0 ]]; then echo "Run with sudo -E bash $0"; exit 1; fi
if [[ "$(uname -m)" != "aarch64" ]]; then echo "This bootstrap expects ARM64/aarch64."; exit 1; fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y curl jq tar ca-certificates libicu70 libssl3 libkrb5-3 zlib1g
id -u "$RUNNER_USER" >/dev/null 2>&1 || useradd --create-home --shell /bin/bash "$RUNNER_USER"
usermod -aG docker "$RUNNER_USER" 2>/dev/null || true
install -d -o "$RUNNER_USER" -g "$RUNNER_USER" "$RUNNER_DIR"
DOWNLOAD_URL="$(curl -fsSL https://api.github.com/repos/actions/runner/releases/latest | jq -r '.assets[] | select(.name | test("actions-runner-linux-arm64-.*\\.tar\\.gz$")) | .browser_download_url' | head -1)"
[[ -n "$DOWNLOAD_URL" ]] || { echo "Unable to resolve ARM64 runner download URL."; exit 1; }
if [[ ! -f "$RUNNER_DIR/.runner" ]]; then
  rm -rf "${RUNNER_DIR:?}"/*
  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' EXIT
  curl -fsSL "$DOWNLOAD_URL" -o "$tmp"
  tar -xzf "$tmp" -C "$RUNNER_DIR"
  chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"
  sudo -u "$RUNNER_USER" "$RUNNER_DIR/config.sh" --unattended --url "$REPO_URL" --token "$RUNNER_TOKEN" --name "$RUNNER_NAME" --labels "$LABELS" --work "_work" --replace
fi
cat >/usr/local/sbin/platform-kubectl <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

KUBECTL=(/usr/local/bin/k3s kubectl)

case "${1:-}" in
  version)
    [[ "$#" -eq 1 ]] || exit 2
    exec "${KUBECTL[@]}" version --client
    ;;
  get)
    shift
    case "${1:-}" in
      nodes|namespaces|ns|pods|po|deployments|deployment|deploy|services|svc|ingress|ingresses|jobs|cronjobs|pv|pvc)
        exec "${KUBECTL[@]}" get "$@"
        ;;
    esac
    ;;
  policy-version)
    [[ "$#" -eq 1 ]] || exit 2
    echo "platform-kubectl policy: rollout-status-v10-keycloak-secret-provision"
    exit 0
    ;;
  reconcile-ghcr-pull)
    [[ "$#" -eq 1 ]] || {
      echo "platform-kubectl: reconcile-ghcr-pull takes no arguments" >&2
      exit 2
    }
    IFS= read -r ghcr_username || true
    IFS= read -r ghcr_token || true
    [[ -n "$ghcr_username" && -n "$ghcr_token" ]] || {
      echo "platform-kubectl: GHCR credentials must be provided on stdin" >&2
      exit 2
    }
    for namespace in microfe-platform stock-prod; do
      "${KUBECTL[@]}" -n "$namespace" create secret docker-registry ghcr-pull \
        --docker-server=ghcr.io \
        --docker-username="$ghcr_username" \
        --docker-password="$ghcr_token" \
        --dry-run=client -o yaml | "${KUBECTL[@]}" apply -f -
      "${KUBECTL[@]}" -n "$namespace" patch serviceaccount default \
        --type="merge" \
        -p '{"imagePullSecrets":[{"name":"ghcr-pull"}]}'
    done
    exit 0
    ;;
  provision-auth-secret)
    [[ "$#" -eq 1 ]] || {
      echo "platform-kubectl: provision-auth-secret takes no arguments; values must be provided on stdin" >&2
      exit 2
    }
    # Read four newline-delimited values from stdin. Never echo them or enable shell tracing.
    IFS= read -r supabase_url || true
    IFS= read -r supabase_service_role_key || true
    IFS= read -r jwt_secret || true
    IFS= read -r mfa_encryption_key || true
    [[ -n "$supabase_url" && -n "$supabase_service_role_key" && -n "$jwt_secret" && -n "$mfa_encryption_key" ]] || {
      unset supabase_url supabase_service_role_key jwt_secret mfa_encryption_key
      echo "platform-kubectl: all four Auth runtime values are required; values suppressed" >&2
      exit 2
    }
    [[ "$supabase_url" == https://* ]] || {
      unset supabase_url supabase_service_role_key jwt_secret mfa_encryption_key
      echo "platform-kubectl: SUPABASE_URL must use HTTPS; values suppressed" >&2
      exit 2
    }
    [[ "${#jwt_secret}" -ge 32 ]] || {
      unset supabase_url supabase_service_role_key jwt_secret mfa_encryption_key
      echo "platform-kubectl: JWT_SECRET must contain at least 32 characters; values suppressed" >&2
      exit 2
    }
    # Values flow only through stdin and a pipe; no command-line args, temp files, output, or logs.
    if ! {
      printf 'SUPABASE_URL=%s\n' "$supabase_url"
      printf 'SUPABASE_SERVICE_ROLE_KEY=%s\n' "$supabase_service_role_key"
      printf 'JWT_SECRET=%s\n' "$jwt_secret"
      printf 'MFA_ENCRYPTION_KEY=%s\n' "$mfa_encryption_key"
    } | "${KUBECTL[@]}" -n microfe-platform create secret generic microfe-auth-secrets --from-env-file=/dev/stdin --dry-run=client -o yaml | "${KUBECTL[@]}" apply -f - >/dev/null; then
      unset supabase_url supabase_service_role_key jwt_secret mfa_encryption_key
      echo "platform-kubectl: failed to provision Auth runtime Secret; values suppressed" >&2
      exit 1
    fi
    unset supabase_url supabase_service_role_key jwt_secret mfa_encryption_key
    echo "Auth runtime Secret provisioned in microfe-platform; values suppressed."
    exit 0
    ;;
  verify-auth-secret)
    [[ "$#" -eq 1 ]] || {
      echo "platform-kubectl: verify-auth-secret takes no arguments" >&2
      exit 2
    }

    secret_json="$("${KUBECTL[@]}" -n microfe-platform get secret microfe-auth-secrets -o json 2>/dev/null)" || {
      echo "platform-kubectl: missing microfe-auth-secrets in namespace microfe-platform; run the protected platform-infra production provisioning workflow" >&2
      exit 1
    }
    for key in SUPABASE_URL SUPABASE_SERVICE_ROLE_KEY JWT_SECRET MFA_ENCRYPTION_KEY; do
      printf '%s' "$secret_json" | jq -e --arg key "$key" '.data[$key] != null and .data[$key] != ""' >/dev/null || {
        echo "platform-kubectl: microfe-auth-secrets is missing required key: $key" >&2
        exit 1
      }
    done
    unset secret_json
    echo "Auth runtime Secret exists and contains all required keys; values suppressed."
    exit 0
    ;;
  provision-keycloak-secret)
    [[ "$#" -eq 1 ]] || {
      echo "platform-kubectl: provision-keycloak-secret takes no arguments; values must be provided on stdin" >&2
      exit 2
    }
    # Read only protected values from stdin. Never echo, trace or put credentials in argv/files.
    IFS= read -r keycloak_db_url || true
    IFS= read -r keycloak_db_username || true
    IFS= read -r keycloak_db_password || true
    IFS= read -r keycloak_admin_username || true
    IFS= read -r keycloak_admin_password || true
    if [[ "$keycloak_db_url" != "jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require" ||
          "$keycloak_db_username" != "keycloak_runtime" ||
          "${#keycloak_db_password}" -lt 32 ||
          -z "$keycloak_admin_username" ||
          "${#keycloak_admin_password}" -lt 24 ]]; then
      unset keycloak_db_url keycloak_db_username keycloak_db_password keycloak_admin_username keycloak_admin_password
      echo "platform-kubectl: Keycloak credentials failed validation; values suppressed" >&2
      exit 2
    fi
    if ! {
      printf 'KEYCLOAK_DB_URL=%s\n' "$keycloak_db_url"
      printf 'KEYCLOAK_DB_USERNAME=%s\n' "$keycloak_db_username"
      printf 'KEYCLOAK_DB_PASSWORD=%s\n' "$keycloak_db_password"
      printf 'KEYCLOAK_ADMIN_USERNAME=%s\n' "$keycloak_admin_username"
      printf 'KEYCLOAK_ADMIN_PASSWORD=%s\n' "$keycloak_admin_password"
    } | "${KUBECTL[@]}" -n microfe-platform create secret generic keycloak-runtime-secrets --from-env-file=/dev/stdin --dry-run=client -o yaml | "${KUBECTL[@]}" apply -f - >/dev/null; then
      unset keycloak_db_url keycloak_db_username keycloak_db_password keycloak_admin_username keycloak_admin_password
      echo "platform-kubectl: failed to provision Keycloak runtime Secret; values suppressed" >&2
      exit 1
    fi
    unset keycloak_db_url keycloak_db_username keycloak_db_password keycloak_admin_username keycloak_admin_password
    echo "Keycloak runtime Secret provisioned; values suppressed."
    exit 0
    ;;
  verify-keycloak-secret)
    [[ "$#" -eq 1 ]] || exit 2
    secret_json="$("${KUBECTL[@]}" -n microfe-platform get secret keycloak-runtime-secrets -o json 2>/dev/null)" || {
      echo "platform-kubectl: keycloak-runtime-secrets is missing" >&2
      exit 1
    }
    for key in KEYCLOAK_DB_URL KEYCLOAK_DB_USERNAME KEYCLOAK_DB_PASSWORD KEYCLOAK_ADMIN_USERNAME KEYCLOAK_ADMIN_PASSWORD; do
      printf '%s' "$secret_json" | jq -e --arg key "$key" '.data[$key] != null and .data[$key] != ""' >/dev/null || {
        unset secret_json
        echo "platform-kubectl: keycloak-runtime-secrets is missing required key: $key" >&2
        exit 1
      }
    done
    username="$(printf '%s' "$secret_json" | jq -r '.data.KEYCLOAK_DB_USERNAME | @base64d')"
    url="$(printf '%s' "$secret_json" | jq -r '.data.KEYCLOAK_DB_URL | @base64d')"
    unset secret_json
    [[ "$username" == "keycloak_runtime.gtqovpusfyyvxpeezxlo" && "$url" == "jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require" ]] || {
      unset username url
      echo "platform-kubectl: Keycloak runtime Secret has invalid DB target/user; values suppressed" >&2
      exit 1
    }
    unset username url
    echo "Keycloak runtime Secret exists and passed key/target validation; values suppressed."
    exit 0
    ;;
  restart-blocked-image-pulls)
    [[ "$#" -eq 1 ]] || exit 2
    restart_if_blocked() {
      local namespace="$1"
      shift
      local blocked
      blocked="$("${KUBECTL[@]}" -n "$namespace" get pods -o jsonpath='{range .items[*]}{.status.containerStatuses[*].state.waiting.reason}{"\n"}{end}' 2>/dev/null | grep -E '(ImagePullBackOff|ErrImagePull)' || true)"
      if [[ -n "$blocked" ]]; then
        echo "Image pull failures detected in $namespace; restarting fixed production workloads."
        "${KUBECTL[@]}" -n "$namespace" rollout restart "$@"
      else
        echo "No image-pull failures in $namespace."
      fi
    }
    restart_if_blocked microfe-platform deployment/microfe-auth deployment/microfe-shell deployment/microfe-ws
    restart_if_blocked stock-prod deployment/stock-admin deployment/stock-backend
    exit 0
    ;;
  logs)
    if [[ "${2:-}" == "deployment/media-generation" && "${3:-}" == "-n" && "${4:-}" == "media-prod" && ( "${5:-}" == "--tail=200" || "${5:-}" == "--previous" ) ]]; then
      if [[ "${5:-}" == "--previous" ]]; then exec "${KUBECTL[@]}" logs deployment/media-generation -n media-prod --previous --tail=200; fi
      exec "${KUBECTL[@]}" logs deployment/media-generation -n media-prod --tail=200
    fi
    if [[ "${2:-}" == "deployment/media-generation-frontend" && "${3:-}" == "-n" && "${4:-}" == "media-prod" && ( "${5:-}" == "--tail=200" || "${5:-}" == "--previous" ) ]]; then
      if [[ "${5:-}" == "--previous" ]]; then exec "${KUBECTL[@]}" logs deployment/media-generation-frontend -n media-prod --previous --tail=200; fi
      exec "${KUBECTL[@]}" logs deployment/media-generation-frontend -n media-prod --tail=200
    fi
    echo "platform-kubectl: only media-generation logs in media-prod are allowed" >&2
    exit 2
    ;;
  apply)
    if [[ "${2:-}" == "-f" && "${4:-}" == "" ]]; then
      case "${3:-}" in
        platform/microfe/namespace.yaml|apps/stockdividend/base/namespace.yaml|apps/tce-dashboard/base/namespace.yaml|apps/media-generation/base/namespace.yaml)
          exec "${KUBECTL[@]}" apply -f "${3}"
          ;;
      esac
    fi
    if [[ "${2:-}" == "-k" && "${3:-}" == "platform/keycloak" && "${4:-}" == "" ]]; then
      exec "${KUBECTL[@]}" apply -k platform/keycloak
    fi
    [[ "${2:-}" == "-k" && "${3:-}" == "environments/prod" && "${4:-}" == "" ]] || {
      echo "platform-kubectl: only approved GitOps namespace manifests, -k environments/prod, or -k platform/keycloak are allowed for apply" >&2
      exit 2
    }
    exec "${KUBECTL[@]}" apply -k environments/prod
    ;;
  diff)
    [[ "${2:-}" == "-k" && "${3:-}" == "environments/prod" && "${4:-}" == "" ]] || {
      echo "platform-kubectl: only -k environments/prod is allowed for diff" >&2
      exit 2
    }
    exec "${KUBECTL[@]}" diff -k environments/prod
    ;;
  port-forward)
    [[ "${2:-}" == "-n" && "${3:-}" == "microfe-platform" && "${4:-}" == "svc/microfe-ws" && "${5:-}" == "18080:8080" && "${6:-}" == "" ]] || {
      echo "platform-kubectl: only the approved MicroFE WS event port-forward is allowed" >&2
      exit 2
    }
    exec "${KUBECTL[@]}" -n microfe-platform port-forward svc/microfe-ws 18080:8080
    ;;
  describe-media)
    [[ "$#" -eq 1 ]] || exit 2
    exec "${KUBECTL[@]}" describe deployment/media-generation -n media-prod
    ;;
  rollout)
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/stock-admin" && "${4:-}" == "-n" && "${5:-}" == "stock-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/stock-admin -n stock-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/stock-backend" && "${4:-}" == "-n" && "${5:-}" == "stock-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/stock-backend -n stock-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/stock-frontend" && "${4:-}" == "-n" && "${5:-}" == "stock-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/stock-frontend -n stock-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/tce-service" && "${4:-}" == "-n" && "${5:-}" == "tce-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/tce-service -n tce-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/tce-frontend" && "${4:-}" == "-n" && "${5:-}" == "tce-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/tce-frontend -n tce-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/media-generation" && "${4:-}" == "-n" && "${5:-}" == "media-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/media-generation -n media-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/media-generation-frontend" && "${4:-}" == "-n" && "${5:-}" == "media-prod" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/media-generation-frontend -n media-prod --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/microfe-auth" && "${4:-}" == "-n" && "${5:-}" == "microfe-platform" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/microfe-auth -n microfe-platform --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/microfe-shell" && "${4:-}" == "-n" && "${5:-}" == "microfe-platform" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/microfe-shell -n microfe-platform --timeout=180s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/keycloak" && "${4:-}" == "-n" && "${5:-}" == "microfe-platform" && "${6:-}" == "--timeout=300s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/keycloak -n microfe-platform --timeout=300s
    [[ "${2:-}" == "status" && "${3:-}" == "deployment/microfe-ws" && "${4:-}" == "-n" && "${5:-}" == "microfe-platform" && "${6:-}" == "--timeout=180s" && "${7:-}" == "" ]] && exec "${KUBECTL[@]}" rollout status deployment/microfe-ws -n microfe-platform --timeout=180s
    ;;
  get)
    [[ "${2:-}" == "ingress" && "${3:-}" == "keycloak-public" && "${4:-}" == "-n" && "${5:-}" == "microfe-platform" && "${6:-}" == "" ]] && exec "${KUBECTL[@]}" get ingress keycloak-public -n microfe-platform
    [[ "${2:-}" == "ingress" && "${3:-}" == "microfe-public" && "${4:-}" == "-n" && "${5:-}" == "microfe-platform" && "${6:-}" == "" ]] && exec "${KUBECTL[@]}" get ingress microfe-public -n microfe-platform
    ;;
esac

echo "platform-kubectl: command is not allowlisted" >&2
exit 2
EOF
chmod 0755 /usr/local/sbin/platform-kubectl
echo "platform-kubectl policy: rollout-status-v10-keycloak-secret-provision"
cat >/etc/sudoers.d/platform-infra-runner <<EOF
$RUNNER_USER ALL=(root) NOPASSWD: /usr/local/sbin/platform-kubectl *
EOF
chmod 0440 /etc/sudoers.d/platform-infra-runner
visudo -cf /etc/sudoers.d/platform-infra-runner
chown -R "$RUNNER_USER:$RUNNER_USER" "$RUNNER_DIR"

# svc.sh expects to be invoked from the runner root.
cd "$RUNNER_DIR"

# Keep bootstrap idempotent: a registered runner may already have a service.
if find /etc/systemd/system -maxdepth 1 -type f -name 'actions.runner.*.service' -print -quit | grep -q .; then
  echo "Runner service already installed; reusing existing service."
else
  ./svc.sh install "$RUNNER_USER"
fi

./svc.sh start

echo "Runner bootstrap complete: $RUNNER_NAME"
