#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$ROOT/scripts/decommission-stock-media-namespaces.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fake="$tmp/platform-kubectl"
log="$tmp/log"
fake_sudo="$tmp/sudo"
sudo_log="$tmp/sudo-log"

cat > "$fake_sudo" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
echo "sudo $*" >> "$SUDO_LOG"
exec "$@"
MOCK
chmod +x "$fake_sudo"
export PLATFORM_KUBECTL_SUDO="$fake_sudo"
export SUDO_LOG="$sudo_log"

cat > "$fake" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$FAKE_LOG"
case "$*" in
  "get namespace tce-prod"|"get namespace microfe-platform") exit 0 ;;
  "inventory-namespace stock-prod"|"inventory-namespace media-prod")
    [[ "${MOCK_SNAPSHOT:-0}" != "1" ]] || printf "%s\n" "volumesnapshot.snapshot.storage.k8s.io/keep-me"
    [[ "${MOCK_SNAPSHOT_CONTENT:-0}" != "1" ]] || printf "%s\n" "volumesnapshotcontent.snapshot.storage.k8s.io/keep-me"
    exit 0
    ;;
  "get namespaces -o json")
    if [[ "${MOCK_MISSING_NS:-0}" == "1" ]]; then
      printf '%s\n' '{"items":[{"metadata":{"name":"stock-prod"}},{"metadata":{"name":"tce-prod"}},{"metadata":{"name":"microfe-platform"}}]}'
    else
      printf '%s\n' '{"items":[{"metadata":{"name":"stock-prod"}},{"metadata":{"name":"media-prod"}},{"metadata":{"name":"tce-prod"}},{"metadata":{"name":"microfe-platform"}}]}'
    fi
    ;;
  "get ingress -n stock-prod -o json")
    printf '%s\n' '{"items":[{"metadata":{"name":"stock","namespace":"stock-prod"},"spec":{"rules":[{"host":"stock.example.test"}],"tls":[{"hosts":["stock.example.test"],"secretName":"stock-example-tls"}]},"status":{"loadBalancer":{"ingress":[{"ip":"10.0.0.120"}]}}}]}'
    ;;
  "get ingress -n media-prod -o json") printf '%s\n' '{"items":[]}' ;;
  "get all -n stock-prod -o wide"|"get all -n media-prod -o wide"|"get pvc -n stock-prod -o wide"|"get pvc -n media-prod -o wide"|"get storageclasses -o wide") exit 0 ;;
  "get pvc -n stock-prod -o json"|"get pvc -n media-prod -o json")
    if [[ "${MOCK_PVC:-0}" == "1" ]]; then printf '%s\n' '{"items":[{"metadata":{"name":"keep-me"}}]}'; else printf '%s\n' '{"items":[]}'; fi
    ;;
  "get pv -o json")
    if [[ "${MOCK_PV:-0}" == "1" ]]; then
      printf '%s\n' '{"items":[{"metadata":{"name":"pv-stock"},"spec":{"claimRef":{"namespace":"stock-prod"},"persistentVolumeReclaimPolicy":"Retain","storageClassName":"local-path"}}]}'
    else
      printf '%s\n' '{"items":[]}'
    fi
    ;;
  "decommission-stock-media")
    IFS= read -r first
    IFS= read -r second
    IFS= read -r third
    IFS= read -r fourth
    [[ "$first" == "DELETE-STOCK-PROD-AND-MEDIA-PROD" ]]
    [[ "$second" == "BACKUP-AND-EXTERNAL-DATA-REVIEWED" ]]
    [[ "$third" == "AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED" ]]
    [[ "$fourth" == "MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED" ]]
    echo "DELETE_OK" >> "$FAKE_LOG"
    ;;
  *)
    echo "unexpected mock command: $*" >&2
    exit 99
    ;;
esac
MOCK
chmod +x "$fake"

plan_output="$(PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" plan)"
printf '%s\n' "$plan_output"
grep -Fq "stock.example.test" <<< "$plan_output"
grep -Fq "stock-example-tls" <<< "$plan_output"
grep -Fq "DNS ownership is not inferred" <<< "$plan_output"
grep -Fq "get ingress -n stock-prod -o json" "$log"
grep -Fq "sudo $fake get namespace tce-prod" "$sudo_log"
echo "Verified default decommission preflight invokes the root-owned wrapper through sudo."
if CONFIRMATION=wrong DATA_RETENTION_REVIEW=wrong DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: invalid confirmation was accepted" >&2
  exit 1
fi
if CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=wrong PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: missing/invalid authoritative DNS ownership attestation was accepted" >&2
  exit 1
fi
if CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: missing Media runner retirement attestation was accepted" >&2
  exit 1
fi
if CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED RUNNER_RETIREMENT=wrong PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: invalid Media runner retirement attestation was accepted" >&2
  exit 1
fi
if MOCK_PVC=1 PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED RUNNER_RETIREMENT=MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: PVC presence did not block deletion" >&2
  exit 1
fi
if MOCK_PV=1 PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED RUNNER_RETIREMENT=MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: PV claim presence did not block deletion" >&2
  exit 1
fi
if MOCK_MISSING_NS=1 PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" plan >/dev/null 2>&1; then
  echo "FAIL: missing target namespace did not block decommission" >&2
  exit 1
fi
if MOCK_SNAPSHOT=1 CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED RUNNER_RETIREMENT=MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: namespaced VolumeSnapshot did not block deletion" >&2
  exit 1
fi
if MOCK_SNAPSHOT_CONTENT=1 CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED RUNNER_RETIREMENT=MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: cluster-scoped VolumeSnapshotContent did not block deletion" >&2
  exit 1
fi
if grep -q "^decommission-stock-media$" "$log"; then
  echo "FAIL: snapshot preflight invoked the root namespace deletion command" >&2
  exit 1
fi
CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED DNS_OWNERSHIP_REVIEW=AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED RUNNER_RETIREMENT=MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete
grep -q '^DELETE_OK$' "$log"
echo "Stock/Media decommission preflight and confirmation tests passed."
