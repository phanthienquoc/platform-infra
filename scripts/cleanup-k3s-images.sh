#!/usr/bin/env bash
# Safely remove old, unused K3s/containerd images. Dry-run by default.
set -euo pipefail
DRY_RUN="${DRY_RUN:-true}"
KEEP_UNUSED_IMAGES="${KEEP_UNUSED_IMAGES:-10}"
KCTL="${KCTL:-/usr/local/sbin/platform-kubectl}"
CRI="/usr/local/bin/crictl"
[ -x "$CRI" ] || CRI="$(command -v crictl || true)"
[ -n "$CRI" ] && [ -x "$CRI" ] || { echo "crictl not found" >&2; exit 2; }
[ -x "$KCTL" ] || { echo "kubectl wrapper not found: $KCTL" >&2; exit 2; }
[[ "$KEEP_UNUSED_IMAGES" =~ ^[0-9]+$ ]] && [ "$KEEP_UNUSED_IMAGES" -ge 1 ] || { echo "KEEP_UNUSED_IMAGES must be >= 1" >&2; exit 2; }
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
sudo "$KCTL" get pods -A -o json > "$tmp/pods.json"
sudo "$CRI" ps -a -o json > "$tmp/containers.json"
sudo "$CRI" images -o json > "$tmp/images.json"
jq -r '.items[] | .spec.initContainers[]?.image, .spec.containers[]?.image, .spec.ephemeralContainers[]?.image' "$tmp/pods.json" | sort -u > "$tmp/pod-images.txt"
jq -r '.containers[]? | .imageRef // empty' "$tmp/containers.json" | sort -u > "$tmp/container-image-ids.txt"
# Resolve live pod tags/digests to immutable CRI IDs; do not delete if resolution is ambiguous.
jq -r --slurpfile refs "$tmp/pod-images.txt" '
  .images[]? |
  select(any(.repoTags[]?; . as $tag | $refs[0][] == $tag) or any(.repoDigests[]?; . as $digest | $refs[0][] == $digest)) |
  .id
' "$tmp/images.json" | sort -u > "$tmp/pod-image-ids.txt"
jq -r '.images[]? | select((.repoTags // []) | length > 0) | [.id, ((.repoTags // []) | join(",")), (.size // 0), (.pinned // false)] | @tsv' "$tmp/images.json" > "$tmp/all.tsv"
: > "$tmp/unused.tsv"
while IFS=$'\t' read -r id tags size pinned; do
  [ -n "$id" ] || continue
  [ "$pinned" = "false" ] || continue
  grep -Fxq "$id" "$tmp/container-image-ids.txt" && continue
  grep -Fxq "$id" "$tmp/pod-image-ids.txt" && continue
  # If any tag resolves to a Pod image, keep the image.
  keep=false
  IFS=',' read -ra tag_array <<< "$tags"
  for tag in "${tag_array[@]}"; do
    grep -Fxq "$tag" "$tmp/pod-images.txt" && keep=true
  done
  [ "$keep" = false ] && printf '%s\t%s\t%s\n' "$id" "$tags" "$size" >> "$tmp/unused.tsv"
done < "$tmp/all.tsv"
# Sort unused image candidates newest-first using CRI createdAt, then retain newest N.
jq -r '.images[]? | [.id, (.repoTags // [] | join(",")), (.size // 0), (.pinned // false), (.createdAt // "")] | @tsv' "$tmp/images.json" |
  awk -F '\t' 'NR==FNR {allowed[$1]=1; next} allowed[$1] {print}' "$tmp/unused.tsv" - |
  sort -t $'\t' -k5,5r > "$tmp/sorted-unused.tsv"
count="$(wc -l < "$tmp/sorted-unused.tsv" | tr -d ' ')"
remove_count=$((count > KEEP_UNUSED_IMAGES ? count - KEEP_UNUSED_IMAGES : 0))
echo "unused_images=$count retain=$KEEP_UNUSED_IMAGES remove=$remove_count dry_run=$DRY_RUN"
head -n "$remove_count" "$tmp/sorted-unused.tsv" | cut -f1-4
[ "$remove_count" -gt 0 ] || exit 0
[ "$DRY_RUN" = "true" ] && { echo "DRY RUN: no images removed."; exit 0; }
head -n "$remove_count" "$tmp/sorted-unused.tsv" | while IFS=$'\t' read -r id tags size pinned created; do
  [ -n "$id" ] || continue
  # Re-check running/all containers immediately before deletion.
  sudo "$CRI" ps -a -o json |
    jq -e --arg id "$id" 'any(.containers[]?; .imageRef == $id)' >/dev/null && { echo "Skip in-use $id"; continue; }
  echo "Removing unused image $id ($tags)"
  sudo "$CRI" rmi "$id"
done
echo "Containerd image cleanup done."
