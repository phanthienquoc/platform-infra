#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
helper="$tmp/namespace-storage-snapshot-refs.sh"
fake="$tmp/kubectl"

awk '
  /^namespace_storage_snapshot_refs\(\) \{$/ { capture=1 }
  capture { print }
  capture && /^}$/ { exit }
' "$ROOT/scripts/bootstrap-runner.sh" > "$helper"
grep -q '^namespace_storage_snapshot_refs() {$' "$helper"

cat > "$fake" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
case "$*" in
  "api-resources --api-group=snapshot.storage.k8s.io --verbs=list --namespaced -o name")
    if [[ "${MOCK_NO_CRD:-0}" != "1" ]]; then
      printf '%s\n' "volumesnapshots.snapshot.storage.k8s.io"
    fi
    ;;
  "get volumesnapshots.snapshot.storage.k8s.io -n stock-prod -o name")
    if [[ "${MOCK_SNAPSHOT:-0}" == "1" ]]; then
      printf '%s\n' "volumesnapshot.snapshot.storage.k8s.io/stock-snapshot"
    fi
    ;;
  "api-resources --api-group=snapshot.storage.k8s.io --verbs=list --namespaced=false -o name")
    if [[ "${MOCK_NO_CRD:-0}" != "1" ]]; then
      printf '%s\n' "volumesnapshotcontents.snapshot.storage.k8s.io"
    fi
    ;;
  "get volumesnapshotcontents.snapshot.storage.k8s.io -o json")
    if [[ "${MOCK_NO_CRD:-0}" == "1" ]]; then
      echo '{"items":[]}'
    elif [[ "${MOCK_CONTENT_TARGET:-0}" == "1" ]]; then
      echo '{"items":[{"metadata":{"name":"stock-content"},"spec":{"volumeSnapshotRef":{"namespace":"stock-prod"}}},{"metadata":{"name":"other-content"},"spec":{"volumeSnapshotRef":{"namespace":"other"}}}]}'
    else
      echo '{"items":[{"metadata":{"name":"other-content"},"spec":{"volumeSnapshotRef":{"namespace":"other"}}}]}'
    fi
    ;;
  *)
    echo "unexpected kubectl command: $*" >&2
    exit 99
    ;;
esac
MOCK
chmod +x "$fake"

KUBECTL=("$fake")
source "$helper"

output="$(MOCK_SNAPSHOT=1 MOCK_CONTENT_TARGET=1 namespace_storage_snapshot_refs stock-prod)"
grep -Fq 'volumesnapshot.snapshot.storage.k8s.io/stock-snapshot' <<< "$output"
grep -Fq 'volumesnapshotcontent.snapshot.storage.k8s.io/stock-content' <<< "$output"
if grep -Fq 'other-content' <<< "$output"; then
  echo "FAIL: unrelated VolumeSnapshotContent was attributed to stock-prod" >&2
  exit 1
fi

output="$(namespace_storage_snapshot_refs stock-prod)"
[[ -z "$output" ]] || {
  echo "FAIL: snapshot content belonging to another namespace was reported" >&2
  exit 1
}

output="$(MOCK_NO_CRD=1 namespace_storage_snapshot_refs stock-prod)"
[[ -z "$output" ]] || {
  echo "FAIL: absent snapshot CRDs should produce an empty inventory" >&2
  exit 1
}

if namespace_storage_snapshot_refs default >/dev/null 2>&1; then
  echo "FAIL: snapshot inventory accepted an unapproved namespace" >&2
  exit 1
fi

echo "Namespace VolumeSnapshot and VolumeSnapshotContent inventory tests passed."
