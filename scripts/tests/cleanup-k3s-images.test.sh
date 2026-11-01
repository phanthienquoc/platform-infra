#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cleanup_script="$repo_root/scripts/cleanup-k3s-images.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin"

cat > "$tmp/pods.json" <<'JSON'
{"items":[{"spec":{"initContainers":[],"containers":[{"image":"ghcr.io/example/app:stable"},{"image":"nats:2.12-alpine"},{"image":"rancher/klipper-helm:v0.13.3-build20260727"}],"ephemeralContainers":[]}}]}
JSON
cat > "$tmp/containers.json" <<'JSON'
{"containers":[{"imageRef":"sha256:used"}]}
JSON
cat > "$tmp/images.json" <<'JSON'
{"images":[
  {"id":"sha256:used","repoTags":["ghcr.io/example/app:stable"],"repoDigests":[],"size":100,"pinned":false,"createdAt":"2026-11-01T00:00:00Z"},
  {"id":"sha256:used-nats","repoTags":["docker.io/library/nats:2.12-alpine"],"repoDigests":[],"size":100,"pinned":false,"createdAt":"2026-11-01T00:00:00Z"},
  {"id":"sha256:used-rancher","repoTags":["docker.io/rancher/klipper-helm:v0.13.3-build20260727"],"repoDigests":[],"size":100,"pinned":false,"createdAt":"2026-11-01T00:00:00Z"},
  {"id":"sha256:unused-new","repoTags":["ghcr.io/example/unused:new"],"repoDigests":[],"size":200,"pinned":false,"createdAt":"2026-11-01T02:00:00Z"},
  {"id":"sha256:unused-old","repoTags":["ghcr.io/example/unused:old"],"repoDigests":[],"size":300,"pinned":false,"createdAt":"2026-11-01T01:00:00Z"}
]}
JSON

cat > "$tmp/bin/sudo" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
exec "$@"
SH
cat > "$tmp/bin/platform-kubectl" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if [[ "$*" == "get pods -A -o json" ]]; then
  cat "$MOCK_FIXTURE_DIR/pods.json"
else
  echo "unexpected kubectl arguments: $*" >&2
  exit 64
fi
SH
cat > "$tmp/bin/platform-crictl" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
case "$*" in
  "ps") cat "$MOCK_FIXTURE_DIR/containers.json" ;;
  "images") cat "$MOCK_FIXTURE_DIR/images.json" ;;
  *) echo "unexpected CRI arguments: $*" >&2; exit 64 ;;
esac
SH
chmod +x "$tmp/bin/sudo" "$tmp/bin/platform-kubectl" "$tmp/bin/platform-crictl"
export MOCK_FIXTURE_DIR="$tmp"

output="$(
  PATH="$tmp/bin:$PATH" \
  KCTL="$tmp/bin/platform-kubectl" \
  CRI="$tmp/bin/platform-crictl" \
  DRY_RUN=true KEEP_UNUSED_IMAGES=1 \
  bash "$cleanup_script"
)"
grep -Fq "unused_images=2 retain=1 remove=1 dry_run=true" <<< "$output"
grep -Fq "candidate id=sha256:unused-new" <<< "$output"
for referenced_id in sha256:used sha256:used-nats sha256:used-rancher; do
  if grep -Fq "candidate id=$referenced_id" <<< "$output"; then
    echo "Referenced image was incorrectly selected for cleanup: $referenced_id" >&2
    exit 1
  fi
done
if grep -Fq "Removing unused K3s image" <<< "$output"; then
  echo "Dry-run unexpectedly attempted image deletion." >&2
  exit 1
fi

# A terminal Pod may retain a spec reference after containerd has removed the image.
# Its exited container is absent from CRI ps -a, so no local image ID can be deleted.
cat > "$tmp/pods.json" <<'JSON'
{"items":[
  {"status":{"phase":"Running"},"spec":{"initContainers":[],"containers":[{"image":"ghcr.io/example/app:stable"}],"ephemeralContainers":[]}},
  {"status":{"phase":"Succeeded"},"spec":{"initContainers":[],"containers":[{"image":"rancher/klipper-helm:v0.13.3-build20260727"}],"ephemeralContainers":[]}}
]}
JSON
cat > "$tmp/images.json" <<'JSON'
{"images":[
  {"id":"sha256:used","repoTags":["ghcr.io/example/app:stable"],"repoDigests":[],"size":100,"pinned":false,"createdAt":"2026-11-01T00:00:00Z"},
  {"id":"sha256:unused-new","repoTags":["ghcr.io/example/unused:new"],"repoDigests":[],"size":200,"pinned":false,"createdAt":"2026-11-01T02:00:00Z"},
  {"id":"sha256:unused-old","repoTags":["ghcr.io/example/unused:old"],"repoDigests":[],"size":300,"pinned":false,"createdAt":"2026-11-01T01:00:00Z"}
]}
JSON
terminal_output="$(
  PATH="$tmp/bin:$PATH" \
  KCTL="$tmp/bin/platform-kubectl" \
  CRI="$tmp/bin/platform-crictl" \
  DRY_RUN=true KEEP_UNUSED_IMAGES=1 \
  bash "$cleanup_script" 2>&1
)"
grep -Fq "Ignoring unresolved image reference for terminal Pod phase=Succeeded" <<< "$terminal_output"
grep -Fq "unused_images=2 retain=1 remove=1 dry_run=true" <<< "$terminal_output"
if grep -Fq "candidate id=sha256:used" <<< "$terminal_output"; then
  echo "Running Pod image was incorrectly selected after terminal Pod fallback." >&2
  exit 1
fi

# An unresolved Pod image reference must fail closed before any deletion.
cat > "$tmp/pods.json" <<'JSON'
{"items":[{"status":{"phase":"Running"},"spec":{"initContainers":[],"containers":[{"image":"ghcr.io/example/missing:tag"}],"ephemeralContainers":[]}}]}
JSON
set +e
PATH="$tmp/bin:$PATH" \
KCTL="$tmp/bin/platform-kubectl" \
CRI="$tmp/bin/platform-crictl" \
DRY_RUN=true KEEP_UNUSED_IMAGES=1 \
bash "$cleanup_script" >"$tmp/unresolved.out" 2>"$tmp/unresolved.err"
status=$?
set -e
[[ "$status" -eq 3 ]] || {
  echo "Expected unresolved Pod reference to exit 3, got $status." >&2
  cat "$tmp/unresolved.err" >&2
  exit 1
}
grep -Fq "Cannot resolve non-terminal Pod image reference" "$tmp/unresolved.err"

echo "K3s image cleanup regression tests passed."
