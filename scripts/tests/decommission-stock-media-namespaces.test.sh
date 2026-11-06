#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$ROOT/scripts/decommission-stock-media-namespaces.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fake="$tmp/platform-kubectl"
log="$tmp/log"

cat > "$fake" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$FAKE_LOG"
case "$*" in
  "get namespace tce-prod"|"get namespace microfe-platform") exit 0 ;;
  "inventory-namespace stock-prod"|"inventory-namespace media-prod") exit 0 ;;
  "get namespaces -o json")
    if [[ "${MOCK_MISSING_NS:-0}" == "1" ]]; then
      printf '%s\n' '{"items":[{"metadata":{"name":"stock-prod"}},{"metadata":{"name":"tce-prod"}},{"metadata":{"name":"microfe-platform"}}]}'
    else
      printf '%s\n' '{"items":[{"metadata":{"name":"stock-prod"}},{"metadata":{"name":"media-prod"}},{"metadata":{"name":"tce-prod"}},{"metadata":{"name":"microfe-platform"}}]}'
    fi
    ;;
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
    [[ "$first" == "DELETE-STOCK-PROD-AND-MEDIA-PROD" ]]
    [[ "$second" == "BACKUP-AND-EXTERNAL-DATA-REVIEWED" ]]
    echo "DELETE_OK" >> "$FAKE_LOG"
    ;;
  *)
    echo "unexpected mock command: $*" >&2
    exit 99
    ;;
esac
MOCK
chmod +x "$fake"

PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" plan
if CONFIRMATION=wrong DATA_RETENTION_REVIEW=wrong PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: invalid confirmation was accepted" >&2
  exit 1
fi
if MOCK_PVC=1 PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: PVC presence did not block deletion" >&2
  exit 1
fi
if MOCK_PV=1 PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED bash "$SCRIPT" delete >/dev/null 2>&1; then
  echo "FAIL: PV claim presence did not block deletion" >&2
  exit 1
fi
if MOCK_MISSING_NS=1 PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" plan >/dev/null 2>&1; then
  echo "FAIL: missing target namespace did not block decommission" >&2
  exit 1
fi
CONFIRMATION=DELETE-STOCK-PROD-AND-MEDIA-PROD DATA_RETENTION_REVIEW=BACKUP-AND-EXTERNAL-DATA-REVIEWED PLATFORM_KUBECTL_BIN="$fake" FAKE_LOG="$log" bash "$SCRIPT" delete
grep -q '^DELETE_OK$' "$log"
echo "Stock/Media decommission preflight and confirmation tests passed."
