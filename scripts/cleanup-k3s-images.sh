#!/usr/bin/env bash
# Remove only clearly unused, unpinned K3s/containerd images.
# Dry-run is the default. Never prune volumes, running containers, Docker data,
# or images referenced by any Pod/Container.
set -euo pipefail

DRY_RUN="${DRY_RUN:-true}"
KEEP_UNUSED_IMAGES="${KEEP_UNUSED_IMAGES:-10}"
KCTL="${KCTL:-/usr/local/sbin/platform-kubectl}"
CRI="${CRI:-/usr/local/sbin/platform-crictl}"
[ -x "$CRI" ] || { echo "restricted CRI wrapper not found: $CRI" >&2; exit 2; }
[ -x "$KCTL" ] || { echo "kubectl wrapper not found: $KCTL" >&2; exit 2; }
if ! [[ "$KEEP_UNUSED_IMAGES" =~ ^[0-9]+$ ]] || [ "$KEEP_UNUSED_IMAGES" -lt 1 ]; then
  echo "KEEP_UNUSED_IMAGES must be >= 1" >&2
  exit 2
fi
[[ "$DRY_RUN" == true || "$DRY_RUN" == false ]] || { echo "DRY_RUN must be true or false" >&2; exit 2; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
sudo "$KCTL" get pods -A -o json | tee "$tmp/pods.json" >/dev/null
sudo "$CRI" ps | tee "$tmp/containers.json" >/dev/null
sudo "$CRI" images | tee "$tmp/images.json" >/dev/null

# Keep every image used by a currently existing container, including terminated containers.
jq -r '.containers[]? | .imageRef // empty' "$tmp/containers.json" | sort -u > "$tmp/container-image-ids.txt"

# Docker Hub references are normalized by the runtime (for example, nats:tag
# becomes docker.io/library/nats:tag). Normalize both Pod specs and CRI names
# before resolving refs to immutable local IDs.
canonical_image_ref() {
  local ref="$1"
  local name suffix="" last_component first_component

  if [[ "$ref" == *@* ]]; then
    suffix="@${ref#*@}"
    name="${ref%@*}"
  else
    name="$ref"
    last_component="${name##*/}"
    if [[ "$last_component" == *:* ]]; then
      suffix=":${last_component##*:}"
      name="${name%:*}"
    else
      suffix=":latest"
    fi
  fi

  if [[ "$name" == index.docker.io/* ]]; then
    name="docker.io/${name#index.docker.io/}"
  fi

  if [[ "$name" != */* ]]; then
    name="docker.io/library/$name"
  else
    first_component="${name%%/*}"
    if [[ "$first_component" != *.* && "$first_component" != *:* && "$first_component" != "localhost" ]]; then
      name="docker.io/$name"
    fi
  fi

  printf '%s%s\n' "$name" "$suffix"
}

resolve_pod_image_ids() {
  local pods_json="$1"
  local images_json="$2"
  local output_file="$3"
  local refs_file="$tmp/pod-refs.$$.txt"
  local raw_map="$tmp/image-ref-map-raw.$$.tsv"
  local map_file="$tmp/image-ref-map.$$.tsv"
  local local_refs="$tmp/local-image-refs.$$.txt"
  local id ref normalized missing_refs=0

  jq -r '
    .items[] as $pod
    | ($pod.spec.initContainers[]?.image, $pod.spec.containers[]?.image, $pod.spec.ephemeralContainers[]?.image)
    | select(type == "string" and length > 0)
    | [($pod.status.phase // "Unknown"), .] | @tsv
  ' "$pods_json" | sort -u > "$refs_file"
  jq -r '.images[]? as $image | $image.id as $id | ($image.repoTags[]?, $image.repoDigests[]?) as $ref | [$id, $ref] | @tsv' "$images_json" > "$raw_map"

  : > "$map_file"
  while IFS=$'\t' read -r id ref; do
    [[ -n "$id" && -n "$ref" ]] || continue
    normalized="$(canonical_image_ref "$ref")"
    printf '%s\t%s\n' "$id" "$normalized" >> "$map_file"
  done < "$raw_map"
  cut -f2 "$map_file" | sort -u > "$local_refs"

  : > "$output_file"
  while read -r phase ref; do
    [[ -n "$ref" ]] || continue
    normalized="$(canonical_image_ref "$ref")"
    if ! grep -Fxq "$normalized" "$local_refs"; then
      case "$phase" in
        Succeeded|Failed)
          # Terminal Pods may retain their original spec after containerd has
          # garbage-collected the image. Existing CRI containers are protected
          # separately through container-image-ids.txt, including exited ones.
          echo "Ignoring unresolved image reference for terminal Pod phase=$phase; no local CRI image matched: $ref (normalized=$normalized)" >&2
          continue
          ;;
        *)
          echo "Cannot resolve non-terminal Pod image reference; refusing cleanup: phase=$phase ref=$ref (normalized=$normalized)" >&2
          missing_refs=1
          continue
          ;;
      esac
    fi
    awk -F '\t' -v ref="$normalized" '$2 == ref { print $1 }' "$map_file" >> "$output_file"
  done < "$refs_file"

  rm -f "$refs_file" "$raw_map" "$map_file" "$local_refs"
  [[ "$missing_refs" -eq 0 ]] || return 3
  sort -u -o "$output_file" "$output_file"
}

resolve_pod_image_ids "$tmp/pods.json" "$tmp/images.json" "$tmp/pod-image-ids.txt" || exit 3
# Fail closed above if any Pod reference cannot be mapped to a local image ID.

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
  sudo "$KCTL" get pods -A -o json | tee "$tmp/pods-current.json" >/dev/null
  sudo "$CRI" ps | tee "$tmp/containers-current.json" >/dev/null
  sudo "$CRI" images | tee "$tmp/images-current.json" >/dev/null
  grep -Fxq "$id" <(jq -r '.containers[]? | .imageRef // empty' "$tmp/containers-current.json") && {
    echo "Skip image still referenced by container: $id"; continue;
  }
  resolve_pod_image_ids "$tmp/pods-current.json" "$tmp/images-current.json" "$tmp/pod-image-ids-current.txt" || {
    echo "Current Pod image references could not be resolved; aborting cleanup." >&2
    exit 3
  }
  grep -Fxq "$id" "$tmp/pod-image-ids-current.txt" && {
    echo "Skip image still referenced by current Pod: $id"; continue;
  }
  echo "Removing unused K3s image: $id ($tags)"
  sudo "$CRI" rmi "$id"
done
echo "K3s/containerd unused-image cleanup completed."
\\t' read -r phase ref; do
    [[ -n "$ref" ]] || continue
    normalized="$(canonical_image_ref "$ref")"
    if ! grep -Fxq "$normalized" "$local_refs"; then
      case "$phase" in
        Succeeded|Failed)
          # Terminal Pods may retain their original spec after containerd has
          # garbage-collected the image. Existing CRI containers are protected
          # separately through container-image-ids.txt, including exited ones.
          echo "Ignoring unresolved image reference for terminal Pod phase=$phase; no local CRI image matched: $ref (normalized=$normalized)" >&2
          continue
          ;;
        *)
          echo "Cannot resolve non-terminal Pod image reference; refusing cleanup: phase=$phase ref=$ref (normalized=$normalized)" >&2
          missing_refs=1
          continue
          ;;
      esac
    fi
    awk -F '\\t' -v ref="$normalized" '$2 == ref { print $1 }' "$map_file" >> "$output_file"
  done < "$refs_file"

  rm -f "$refs_file" "$raw_map" "$map_file" "$local_refs"
  [[ "$missing_refs" -eq 0 ]] || return 3
  sort -u -o "$output_file" "$output_file"
}

resolve_pod_image_ids "$tmp/pods.json" "$tmp/images.json" "$tmp/pod-image-ids.txt" || exit 3
# Fail closed above if any Pod reference cannot be mapped to a local image ID.

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
  sudo "$KCTL" get pods -A -o json | tee "$tmp/pods-current.json" >/dev/null
  sudo "$CRI" ps | tee "$tmp/containers-current.json" >/dev/null
  sudo "$CRI" images | tee "$tmp/images-current.json" >/dev/null
  grep -Fxq "$id" <(jq -r '.containers[]? | .imageRef // empty' "$tmp/containers-current.json") && {
    echo "Skip image still referenced by container: $id"; continue;
  }
  resolve_pod_image_ids "$tmp/pods-current.json" "$tmp/images-current.json" "$tmp/pod-image-ids-current.txt" || {
    echo "Current Pod image references could not be resolved; aborting cleanup." >&2
    exit 3
  }
  grep -Fxq "$id" "$tmp/pod-image-ids-current.txt" && {
    echo "Skip image still referenced by current Pod: $id"; continue;
  }
  echo "Removing unused K3s image: $id ($tags)"
  sudo "$CRI" rmi "$id"
done
echo "K3s/containerd unused-image cleanup completed."
\t' read -r phase ref; do
    [[ -n "$ref" ]] || continue
    normalized="$(canonical_image_ref "$ref")"
    if ! grep -Fxq "$normalized" "$local_refs"; then
      case "$phase" in
        Succeeded|Failed)
          # Terminal Pods may retain their original spec after containerd has
          # garbage-collected the image. Existing CRI containers are protected
          # separately through container-image-ids.txt, including exited ones.
          echo "Ignoring unresolved image reference for terminal Pod phase=$phase; no local CRI image matched: $ref (normalized=$normalized)" >&2
          continue
          ;;
        *)
          echo "Cannot resolve non-terminal Pod image reference; refusing cleanup: phase=$phase ref=$ref (normalized=$normalized)" >&2
          missing_refs=1
          continue
          ;;
      esac
    fi
    awk -F '\t' -v ref="$normalized" '$2 == ref { print $1 }' "$map_file" >> "$output_file"
  done < "$refs_file"

  rm -f "$refs_file" "$raw_map" "$map_file" "$local_refs"
  [[ "$missing_refs" -eq 0 ]] || return 3
  sort -u -o "$output_file" "$output_file"
}

resolve_pod_image_ids "$tmp/pods.json" "$tmp/images.json" "$tmp/pod-image-ids.txt" || exit 3
# Fail closed above if any Pod reference cannot be mapped to a local image ID.

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
  sudo "$KCTL" get pods -A -o json | tee "$tmp/pods-current.json" >/dev/null
  sudo "$CRI" ps | tee "$tmp/containers-current.json" >/dev/null
  sudo "$CRI" images | tee "$tmp/images-current.json" >/dev/null
  grep -Fxq "$id" <(jq -r '.containers[]? | .imageRef // empty' "$tmp/containers-current.json") && {
    echo "Skip image still referenced by container: $id"; continue;
  }
  resolve_pod_image_ids "$tmp/pods-current.json" "$tmp/images-current.json" "$tmp/pod-image-ids-current.txt" || {
    echo "Current Pod image references could not be resolved; aborting cleanup." >&2
    exit 3
  }
  grep -Fxq "$id" "$tmp/pod-image-ids-current.txt" && {
    echo "Skip image still referenced by current Pod: $id"; continue;
  }
  echo "Removing unused K3s image: $id ($tags)"
  sudo "$CRI" rmi "$id"
done
echo "K3s/containerd unused-image cleanup completed."
\\t' read -r phase ref; do
    [[ -n "$ref" ]] || continue
    normalized="$(canonical_image_ref "$ref")"
    if ! grep -Fxq "$normalized" "$local_refs"; then
      case "$phase" in
        Succeeded|Failed)
          # Terminal Pods may retain their original spec after containerd has
          # garbage-collected the image. Existing CRI containers are protected
          # separately through container-image-ids.txt, including exited ones.
          echo "Ignoring unresolved image reference for terminal Pod phase=$phase; no local CRI image matched: $ref (normalized=$normalized)" >&2
          continue
          ;;
        *)
          echo "Cannot resolve non-terminal Pod image reference; refusing cleanup: phase=$phase ref=$ref (normalized=$normalized)" >&2
          missing_refs=1
          continue
          ;;
      esac
    fi
    awk -F '\\t' -v ref="$normalized" '$2 == ref { print $1 }' "$map_file" >> "$output_file"
  done < "$refs_file"

  rm -f "$refs_file" "$raw_map" "$map_file" "$local_refs"
  [[ "$missing_refs" -eq 0 ]] || return 3
  sort -u -o "$output_file" "$output_file"
}

resolve_pod_image_ids "$tmp/pods.json" "$tmp/images.json" "$tmp/pod-image-ids.txt" || exit 3
# Fail closed above if any Pod reference cannot be mapped to a local image ID.

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
  sudo "$KCTL" get pods -A -o json | tee "$tmp/pods-current.json" >/dev/null
  sudo "$CRI" ps | tee "$tmp/containers-current.json" >/dev/null
  sudo "$CRI" images | tee "$tmp/images-current.json" >/dev/null
  grep -Fxq "$id" <(jq -r '.containers[]? | .imageRef // empty' "$tmp/containers-current.json") && {
    echo "Skip image still referenced by container: $id"; continue;
  }
  resolve_pod_image_ids "$tmp/pods-current.json" "$tmp/images-current.json" "$tmp/pod-image-ids-current.txt" || {
    echo "Current Pod image references could not be resolved; aborting cleanup." >&2
    exit 3
  }
  grep -Fxq "$id" "$tmp/pod-image-ids-current.txt" && {
    echo "Skip image still referenced by current Pod: $id"; continue;
  }
  echo "Removing unused K3s image: $id ($tags)"
  sudo "$CRI" rmi "$id"
done
echo "K3s/containerd unused-image cleanup completed."
