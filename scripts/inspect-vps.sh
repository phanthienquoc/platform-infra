#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-debug/vps-latest.md}"
mkdir -p "$(dirname "$OUT")"
KCTL=/usr/local/sbin/platform-kubectl
{
  echo "# VPS inspection"; echo; echo "Generated: $(date -Is)"; echo
  echo "## Host"
  uname -a
  echo "arch: $(uname -m)"
  if [ -r /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    echo "os: $PRETTY_NAME"
  fi
  echo "hostname: $(hostname)"
  echo
  echo "## Resources"; nproc; free -h; df -h /; df -h /var/lib/rancher/k3s/agent/containerd /var/lib/docker 2>/dev/null || true
  disk_usage_pct="$(df --output=pcent / | tail -n 1 | tr -dc '0-9')"
  if [[ "$disk_usage_pct" =~ ^[0-9]+$ ]]; then
    if [ "$disk_usage_pct" -ge 90 ]; then echo "disk_pressure: critical (${disk_usage_pct}%)"; elif [ "$disk_usage_pct" -ge 80 ]; then echo "disk_pressure: warning (${disk_usage_pct}%)"; else echo "disk_pressure: normal (${disk_usage_pct}%)"; fi
  else echo "disk_pressure: unknown"; fi
  uptime; echo; echo "### Top disk consumers"; sudo du -xhd1 /var/lib/rancher/k3s /var/lib/docker /var/log 2>/dev/null | sort -h | tail -n 30 || true
  echo; echo "## Runner"; id github-runner 2>/dev/null || true; pgrep -af "Runner.Listener|Runner.Worker" | head -20 || true
  systemctl list-units --type=service --all | grep -Ei "actions.runner|github" || true
  echo "runner_service: $(systemctl is-active actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service 2>/dev/null || true)"
  echo "runner_service_enabled: $(systemctl is-enabled actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service 2>/dev/null || true)"
  echo; echo "## Docker"; docker --version 2>/dev/null || true; docker info --format "Server={{.ServerVersion}} RootDir={{.DockerRootDir}}" 2>/dev/null || true; sudo docker system df 2>/dev/null || true
  echo; echo "## Updates"; apt list --upgradable 2>/dev/null | sed -n "1,80p" || true; echo "restart_required: $(test -f /var/run/reboot-required && echo yes || echo no)"
  echo; echo "## K3s"; sudo "$KCTL" version || true; sudo "$KCTL" get nodes -o wide || true; sudo "$KCTL" get namespaces || true; sudo "$KCTL" get pods -A -o wide || true; sudo "$KCTL" get deployments -A || true
  echo; echo "### Pod failure evidence"
  sudo "$KCTL" get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{.state.waiting.reason}{"\t"}{.state.waiting.message}{"\n"}{end}{end}' 2>/dev/null | grep -E $'\t(ImagePullBackOff|ErrImagePull|CrashLoopBackOff|CreateContainerConfigError|CreateContainerError|RunContainerError)\t' || true
  echo; echo "### Recent failure events"
  sudo "$KCTL" get events -A --sort-by='.lastTimestamp' 2>/dev/null | grep -Ei 'Failed|BackOff|Unhealthy|Pull|Probe|OOM|Forbidden|Unauthorized' | tail -n 120 || true
  echo; echo "### TCE service diagnostics (last 2h; redacted)"
  if sudo "$KCTL" get deployment tce-service -n tce-prod >/dev/null 2>&1; then
    sudo "$KCTL" get pods -n tce-prod -l app=tce-service -o wide || true
    while IFS= read -r pod; do
      [ -n "$pod" ] || continue
      echo "-- pod $pod describe --"
      sudo "$KCTL" describe pod "$pod" -n tce-prod 2>&1 | grep -Ei '^(Name:|Start Time:|Status:|IP:|Controlled By:|Containers:|\s+Image:|\s+State:|\s+Last State:|\s+Reason:|\s+Exit Code:|\s+Restart Count:|\s+Started:|\s+Finished:|\s+Ready:|\s+Liveness:|\s+Readiness:|\s+Startup:|Events:|\s+Warning|\s+Normal)' | tail -n 100 || true
      for mode in current previous; do
        echo "### $mode logs for $pod"
        if [ "$mode" = previous ]; then sudo "$KCTL" logs "$pod" -n tce-prod -c service --previous --since=2h --tail=200 2>&1; else sudo "$KCTL" logs "$pod" -n tce-prod -c service --since=2h --tail=200 2>&1; fi |
          grep -Ei 'error|exception|fatal|failed|timeout|timed out|connection refused|ECONN|EAI_AGAIN|listen|starting|started|health|migration|supabase|mongo|auth' |
          sed -E 's/((password|token|secret|authorization|client_secret|service_role_key)[=: ]+)[^ ,;"]+/\1[REDACTED]/Ig; s/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/[EMAIL]/g; s#(postgres(ql)?://)[^/@ ]+:[^/@ ]+@#\1[REDACTED]@#Ig' | cut -c1-500 | tail -n 120 || true
      done
    done < <(sudo "$KCTL" get pods -n tce-prod -l app=tce-service -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n')
  else echo "TCE service deployment not found."; fi
  echo; echo "### CRI image inventory"
  if [ -x /usr/local/bin/crictl ]; then sudo /usr/local/bin/crictl images 2>&1 | head -n 100 || true; sudo /usr/local/bin/crictl ps -a 2>&1 | head -n 100 || true
  elif command -v crictl >/dev/null 2>&1; then sudo crictl images 2>&1 | head -n 100 || true; sudo crictl ps -a 2>&1 | head -n 100 || true
  else echo "crictl not found"; fi
  echo; echo "### GitOps drift"; set +e; sudo "$KCTL" diff -k environments/prod >/dev/null 2>&1; drift_rc=$?; set -e
  case "$drift_rc" in 0) echo "status: clean";; 1) echo "status: drift-detected";; *) echo "status: diff-error"; echo "exit_code: $drift_rc";; esac
  echo; echo "### Images"; sudo "$KCTL" get deployments -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,IMAGES:.spec.template.spec.containers[*].image' --no-headers 2>/dev/null || true
  sudo "$KCTL" get services -A || true; sudo "$KCTL" get ingress -A || true
  echo; echo "## K3s service"; systemctl is-active k3s || true; systemctl is-enabled k3s || true
  echo; echo "### K3s recent warnings (last 2h)"
  sudo journalctl -u k3s --since "2 hours ago" --no-pager -p warning 2>/dev/null | sed -E 's/((password|token|secret|authorization|client_secret)[=: ]+)[^ ,;"]+/\1[REDACTED]/Ig' | cut -c1-500 | tail -n 120 || true
  echo; echo "## Keycloak diagnostics"
  sudo "$KCTL" get deployment keycloak -n microfe-platform -o wide 2>&1 || true
  if sudo "$KCTL" get deployment keycloak -n microfe-platform >/dev/null 2>&1; then
    sudo "$KCTL" logs deployment/keycloak -n microfe-platform --since=2h --tail=200 2>&1 |
      grep -Ei 'error|exception|timeout|timed out|database|jdbc|liquibase|admin.?api|unauthorized|forbidden|realm|connection refused|connection reset|readiness|liveness' |
      sed -E 's/((password|token|secret|authorization|client_secret)[=: ]+)[^ ,;"]+/\1[REDACTED]/Ig; s/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/[EMAIL]/g; s#(postgres(ql)?://)[^/@ ]+:[^/@ ]+@#\1[REDACTED]@#Ig' | cut -c1-500 | tail -n 80 || true
  else echo "Keycloak deployment not found."; fi
  echo; echo "### Public OIDC probes (status and latency only)"
  for endpoint in "https://sso.mrcute.space/realms/master/.well-known/openid-configuration" "https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration"; do
    printf '%s ' "$endpoint"; curl --silent --show-error --output /dev/null --connect-timeout 5 --max-time 10 --write-out 'http_code=%{http_code} time_total=%{time_total}s remote_ip=%{remote_ip}\n' "$endpoint" 2>&1 || true
  done
} >"$OUT"
echo "Wrote $OUT"
