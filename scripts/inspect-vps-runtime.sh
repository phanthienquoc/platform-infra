#!/usr/bin/env bash
# Extra diagnostics appended to the VPS snapshot. Logs are filtered and redacted.
set -u
OUT="${1:?output path required}"
KCTL=/usr/local/sbin/platform-kubectl
{
  echo
  echo "## Storage detail"
  sudo du -sh /var/lib/rancher/k3s/agent/containerd /var/lib/docker 2>/dev/null || true
  sudo du -h -d 1 /var/lib/rancher/k3s/agent/containerd 2>/dev/null | sort -h | tail -n 12 || true
  echo
  echo "## Containerd image cache"
  sudo crictl images 2>&1 | head -n 100 || true
  echo
  echo "## TCE service runtime diagnostics"
  sudo "$KCTL" get deployment tce-service -n tce-prod -o wide 2>&1 || true
  sudo "$KCTL" get pods -n tce-prod -l app=tce-service -o wide 2>&1 || true
  sudo "$KCTL" get events -n tce-prod --sort-by=.lastTimestamp 2>&1 | grep -Ei 'tce-service|Failed|BackOff|Unhealthy|Probe|OOM|Killing' | tail -n 80 || true
  for pod in $(sudo "$KCTL" get pods -n tce-prod -l app=tce-service -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
    echo
    echo "### TCE service logs: $pod (current)"
    sudo "$KCTL" logs -n tce-prod "$pod" -c service --tail=200 2>&1
    echo "### TCE service logs: $pod (previous)"
    sudo "$KCTL" logs -n tce-prod "$pod" -c service --previous --tail=200 2>&1
  done
} 2>&1 |
sed -E 's/((password|token|secret|authorization|client_secret)[=: ]+)[^ ,;"]+/\1[REDACTED]/Ig; s/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/[EMAIL]/g; s#(postgres(ql)?://)[^/@ ]+:[^/@ ]+@#\1[REDACTED]@#Ig' |
cut -c1-500 >> "$OUT"
