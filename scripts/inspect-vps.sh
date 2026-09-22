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
  . /etc/os-release && echo "os: $PRETTY_NAME"
  echo "hostname: $(hostname)"
  echo
  echo "## Resources"
  nproc
  free -h
  df -h /
  uptime
  echo
  echo "## Runner"
  id github-runner 2>/dev/null || true
  ps -eo user,pid,pcpu,pmem,etime,cmd | grep -E "[R]unner.Listener|[R]unner.Worker" | head -20 || true
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
  sudo /usr/local/sbin/platform-kubectl get services -A || true
  sudo /usr/local/sbin/platform-kubectl get ingress -A || true
  echo
  echo "## K3s service"
  systemctl is-active k3s || true
  systemctl is-enabled k3s || true
} >"$OUT"
echo "Wrote $OUT"
