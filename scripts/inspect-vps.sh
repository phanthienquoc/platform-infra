#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-debug/vps-latest.md}"
mkdir -p "$(dirname "$OUT")"
{
  echo "# VPS inspection"
  echo
  echo "Generated: $(date -Is)"
  echo
  echo "## Host"
  echo "uname: $(uname -a)"
  echo "arch: $(uname -m)"
  # shellcheck disable=SC1091
  . /etc/os-release && echo "os: $PRETTY_NAME"
  echo "hostname: $(hostname)"
  echo
  echo "## Resources"
  nproc
  free -h
  df -h /
  disk_usage_pct="$(df --output=pcent / | tail -n 1 | tr -dc '0-9')"
  case "$disk_usage_pct" in
    ''|*[!0-9]*) echo "disk_pressure: unknown" ;;
    *)
      if [ "$disk_usage_pct" -ge 90 ]; then
        echo "disk_pressure: critical (${disk_usage_pct}%)"
      elif [ "$disk_usage_pct" -ge 80 ]; then
        echo "disk_pressure: warning (${disk_usage_pct}%)"
      else
        echo "disk_pressure: normal (${disk_usage_pct}%)"
      fi
      ;;
  esac
  uptime
  echo
  echo "## Runner"
  id github-runner 2>/dev/null || true
  pgrep -af "Runner.Listener|Runner.Worker" | head -20 || true
  systemctl list-units --type=service --all | grep -Ei "actions.runner|github" || true
  echo "runner_service: $(systemctl is-active actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service 2>/dev/null || true)"
  echo "runner_service_enabled: $(systemctl is-enabled actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service 2>/dev/null || true)"
  echo
  echo "## Docker"
  docker --version 2>/dev/null || true
  docker info --format "Server={{.ServerVersion}} RootDir={{.DockerRootDir}}" 2>/dev/null || true
  echo
  echo "## Updates"
  apt list --upgradable 2>/dev/null | sed -n "1,80p" || true
  echo
  echo "restart_required: $(test -f /var/run/reboot-required && echo yes || echo no)"
  echo
  echo "## K3s"
  sudo /usr/local/sbin/platform-kubectl version || true
  sudo /usr/local/sbin/platform-kubectl get nodes -o wide || true
  sudo /usr/local/sbin/platform-kubectl get namespaces || true
  sudo /usr/local/sbin/platform-kubectl get pods -A -o wide || true
  sudo /usr/local/sbin/platform-kubectl get deployments -A || true
  echo
  echo "### Pod failure evidence"
  sudo /usr/local/sbin/platform-kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{.state.waiting.reason}{"\t"}{.state.waiting.message}{"\n"}{end}{end}' 2>/dev/null |
    grep -E $'\t(ImagePullBackOff|ErrImagePull|CrashLoopBackOff|CreateContainerConfigError|CreateContainerError|RunContainerError)\t' || true
  echo
  echo "### Recent failure events"
  sudo /usr/local/sbin/platform-kubectl get events -A --sort-by='.lastTimestamp' 2>/dev/null |
    grep -Ei 'Failed|BackOff|Unhealthy|Pull|Probe|OOM|Forbidden|Unauthorized' |
    tail -n 120 || true
  echo
  echo "### GitOps drift"
  set +e
  sudo /usr/local/sbin/platform-kubectl diff -k environments/prod >/dev/null 2>&1
  drift_rc=$?
  set -e
  case "$drift_rc" in
    0) echo "status: clean" ;;
    1) echo "status: drift-detected" ;;
    *) echo "status: diff-error" ; echo "exit_code: $drift_rc" ;;
  esac
  echo
  echo "### Images"
  sudo /usr/local/sbin/platform-kubectl get deployments -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,IMAGES:.spec.template.spec.containers[*].image' --no-headers 2>/dev/null || true
  sudo /usr/local/sbin/platform-kubectl get services -A || true
  sudo /usr/local/sbin/platform-kubectl get ingress -A || true
  echo
  echo "### Ingress hosts"
  sudo /usr/local/sbin/platform-kubectl get ingress -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,HOSTS:.spec.rules[*].host' --no-headers 2>/dev/null || true
  echo
  echo "## K3s service"
  systemctl is-active k3s || true
  systemctl is-enabled k3s || true
  echo
  echo "## Keycloak diagnostics (read-only; namespace=microfe-platform)"
  KCTL=/usr/local/sbin/platform-kubectl
  sudo "$KCTL" get deployment keycloak -n microfe-platform -o wide 2>&1 || true
  sudo "$KCTL" get pods -n microfe-platform -o wide 2>&1 | grep -i keycloak || true
  sudo "$KCTL" get services -n microfe-platform 2>&1 | grep -i keycloak || true
  echo
  echo "### Keycloak recent diagnostic log lines (last 2h; redacted)"
  if sudo "$KCTL" get deployment keycloak -n microfe-platform >/dev/null 2>&1; then
    sudo "$KCTL" logs deployment/keycloak -n microfe-platform --since=2h --tail=200 2>&1 |
      grep -Ei 'error|exception|timeout|timed out|database|jdbc|liquibase|admin.?api|unauthorized|forbidden|realm|connection refused|connection reset|readiness|liveness' |
      sed -E 's/((password|token|secret|authorization|client_secret)[=: ]+)[^ ,;\"]+/\1[REDACTED]/Ig; s/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/[EMAIL]/g; s#(postgres(ql)?://)[^/@ ]+:[^/@ ]+@#\1[REDACTED]@#Ig' |
      cut -c1-500 | tail -n 80 || true
  else
    echo "Keycloak deployment not found in microfe-platform."
  fi
  echo
  echo "### Public OIDC endpoint probes (status and latency only; response bodies omitted)"
  for endpoint in \
    "https://sso.mrcute.space/realms/master/.well-known/openid-configuration" \
    "https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration"; do
    printf '%s ' "$endpoint"
    curl --silent --show-error --output /dev/null --connect-timeout 5 --max-time 10 \
      --write-out 'http_code=%{http_code} time_total=%{time_total}s remote_ip=%{remote_ip}\n' \
      "$endpoint" 2>&1 || true
  done
} >"$OUT"
scripts/inspect-vps-runtime.sh "$OUT"
echo "Wrote $OUT"
