#!/usr/bin/env bash
# Remove only clearly unused, unpinned K3s/containerd images.
# Dry-run is the default. Never prune volumes, running containers, Docker data,
# or images referenced by any Pod/Container.
set -euo pipefail

DRY_RUN="${DRY_RUN:-true}"
KEEP_UNUSED_IMAGES="${KEEP_UNUSED_IMAGES:-10}"
KCTL="${KCTL:-/usr/local/sbin/platform-kubectl}"
CRI="${CRI:-/usr/local/bin/crictl}"
[ -x "$CRI" ] || CRI="$(command -v crictl || true)"
[ -n "$CRI" ] && [ -x "$CRI" ] || { echo "crictl not found" >&2; exit 2; }
[ -x "$KCTL" ] || { echo "kubectl wrapper not found: $KCTL" >&2; exit 2; }
[[ "$KEEP_UNUSED_IMAGES" =~ ^[0-9]+$ ]] && [ "$KEEP_UNUSED_IMAGES" -ge 1 ] || { echo "KEEP_UNUSED_IMAGES must be >= 1" >&2; exit 2; }
[[ "$DRY_RUN" == true || "$DRY_RUN" == false ]] || { echo "DRY_RUN must be true or false" >&2; exit 2; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
sudo "$KCTL" get pods -A -o json > "$tmp/pods.json"
sudo "$CRI" ps -a -o json > "$tmp/containers.json"
sudo "$CRI" images -o json > "$tmp/images.json"

# Keep all image IDs referenced by Pod specs (including init/ephemeral containers).
jq -r '.items[] | .spec.initContainers[]?.image, .spec.containers[]?.image, .spec.ephemeralContainers[]?.image' "$tmp/pods.json" | sort -u > "$tmp/pod-image-refs.txt"
# Keep every image used by a currently existing container, including terminated containers.
jq -r '.containers[]? | .imageRef // empty' "$tmp/containers.json" | sort -u > "$tmp/container-image-ids.txt"

# Resolve Pod image refs (tags and digests) to immutable local IDs.
jq -r --slurpfile refs "$tmp/pod-image-refs.txt" '
  .images[]? |
  select(any(.repoTags[]?; . as $tag | $refs[0][] == $tag) or
         any(.repoDigests[]?; . as $digest | $refs[0][] == $digest)) |
  .id
' "$tmp/images.json" | sort -u > "$tmp/pod-image-ids.txt"
# Fail closed when a Pod spec reference cannot be mapped to a local image ID.
missing_refs=0
while IFS= read -r ref; do
  [ -n "$ref" ] || continue
  if ! jq -e --arg ref "$ref" 'any(.images[]?; any(.repoTags[]?; . == $ref) or any(.repoDigests[]?; . == $ref))' "$tmp/images.json" >/dev/null; then
    echo "Cannot resolve Pod image reference; refusing all cleanup: $ref" >&2
    missing_refs=1
  fi
done < "$tmp/pod-image-refs.txt"
[ "$missing_refs" -eq 0 ] || exit 3

missing_refs=0
while IFS= read -r ref; do
  [ -n "$ref" ] || continue
  if ! jq -e --arg ref "$ref" '
    any(.images[]?;
      any(.repoTags[]?; . == $ref) or any(.repoDigests[]?; . == $ref)
    )
  ' "$tmp/images.json" >/dev/null; then
    echo "Cannot resolve Pod image reference; refusing cleanup: $ref" >&2
    missing_refs=1
  fi
done < "$tmp/pod-image-refs.txt"
[ "$missing_refs" -eq 0 ] || exit 3

jq -r '.images[]? | select((.repoTags // []) | length > 0) |
  [.id, ((.repoTags // []) | join(",")), (.size // 0), (.pinned // false), (.createdAt // "")] | @tsv
' "$tmp/images.json" | sort -t $'\t' -k5,5r > "$tmp/all-images.tsv"

: > "$tmp/unused.tsv"
while IFS=$'\t' read -r id tags size pinned created; do
  [ -n "$id" ] || continue
  [ "$pinned" = false ] || continue
  grep -Fxq "$id" "$tmp/container-image-ids.txt" && continue
  grep -Fxq "$id" "$tmp/pod-image-ids.txt" && continue
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$tags" "$size" "$pinned" "$created" >> "$tmp/unused.tsv"
done < "$tmp/all-images.tsv"

count="$(wc -l < "$tmp/unused.tsv" | tr -d ' ')"
remove_count=$((count > KEEP_UNUSED_IMAGES ? count - KEEP_UNUSED_IMAGES : 0))
echo "unused_images=$count retain=$KEEP_UNUSED_IMAGES remove=$remove_count dry_run=$DRY_RUN"
head -n "$remove_count" "$tmp/unused.tsv" | while IFS=$'\t' read -r id tags size pinned created; do
  printf 'candidate id=%s tags=%s size_bytes=%s created=%s\n' "$id" "$tags" "$size" "$created"
done
[ "$remove_count" -gt 0 ] || exit 0
[ "$DRY_RUN" = true ] && { echo "DRY RUN: no images removed."; exit 0; }

# Re-check Pod refs and all containers immediately before each deletion.
head -n "$remove_count" "$tmp/unused.tsv" | while IFS=$'\t' read -r id tags size pinned created; do
  [ -n "$id" ] || continue
  sudo "$KCTL" get pods -A -o json > "$tmp/pods-current.json"
  sudo "$CRI" ps -a -o json > "$tmp/containers-current.json"
  grep -Fxq "$id" <(jq -r '.containers[]? | .imageRef // empty' "$tmp/containers-current.json") && {
    echo "Skip image still referenced by container: $id"; continue;
  }
  # Resolve Pod refs again; if any refs fail resolution, abort conservatively.
  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    if jq -e --arg ref "$ref" 'any(.images[]?; any(.repoTags[]?; . == $ref) or any(.repoDigests[]?; . == $ref))' "$tmp/images.json" >/dev/null; then
      :
    else
      echo "Pod image ref unresolved during final safety check; aborting: $ref" >&2
      exit 3
    fi
  done < <(jq -r '.items[] | .spec.initContainers[]?.image, .spec.containers[]?.image, .spec.ephemeralContainers[]?.image' "$tmp/pods-current.json")
  mapfile -t refs_now < <(jq -r '.items[] | .spec.initContainers[]?.image, .spec.containers[]?.image, .spec.ephemeralContainers[]?.image' "$tmp/pods-current.json")
  keep=false
  for ref in "${refs_now[@]}"; do
    if jq -e --arg id "$id" --arg ref "$ref" '
      any(.images[]?; .id == $id and
        (any(.repoTags[]?; . == $ref) or any(.repoDigests[]?; . == $ref)))
    ' "$tmp/images.json" >/dev/null; then keep=true; break; fi
  done
  [ "$keep" = false ] || { echo "Skip image referenced by current Pod: $id"; continue; }
  echo "Removing unused K3s image: $id ($tags)"
  sudo "$CRI" rmi "$id"
done
echo "K3s/containerd unused-image cleanup completed."
