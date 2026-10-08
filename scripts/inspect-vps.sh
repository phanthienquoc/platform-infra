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
  # shellcheck source=/etc/os-release
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
} >"$OUT"
echo "Wrote $OUT"
