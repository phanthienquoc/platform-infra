#!/usr/bin/env bash
# Media migration guard: preserve immutable image replacement protection.
# Only match actual container image fields; ignore image strings inside annotations such as last-applied-configuration.
# Only match actual container image fields; ignore image strings inside annotations such as last-applied-configuration.
set -euo pipefail

MODE="${1:-check}"
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

case "$MODE" in
  check)
    ;;
  *)
    echo "Usage: $0 check" >&2
    exit 2
    ;;
esac

diff_output="$(mktemp)"
trap 'rm -f "$diff_output"' EXIT

set +e
sudo /usr/local/sbin/platform-kubectl diff -k environments/prod | tee "$diff_output" >/dev/null
rc=$?
set -e

if [[ "$rc" -gt 1 ]]; then
  echo "Kubernetes diff failed with exit code $rc." >&2
  exit "$rc"
fi

if [[ "$rc" -eq 0 ]]; then
  echo "No Kubernetes drift detected; image safety gate is clean."
  exit 0
fi

removed_images="$(grep -E '^-[[:space:]]{10,}image:' "$diff_output" || true)"

if [[ -n "$removed_images" ]]; then
  legacy_media_image="$(printf '%s\n' "$removed_images" | grep -E '^-[[:space:]]+image:[[:space:]]+ghcr\.io/phanthienquoc/media-generation:[0-9a-f]{7,64}
     grep -q 'ghcr\.io/phanthienquoc/media-generation-backend:' <<<"$desired_media_images" &&
     grep -q 'ghcr\.io/phanthienquoc/media-generation-frontend:' <<<"$desired_media_images"; then
    echo "Allowing the intentional media-generation monolith -> backend/frontend image migration."
  else
    echo "ERROR: reconciliation would replace an existing workload image." >&2
    echo "The scheduled reconciler refuses image changes to prevent an unintended rollback." >&2
    echo "Removed image references:" >&2
    printf '%s\n' "$removed_images" >&2
    echo "Promote the intended immutable image through GitOps, or use the explicit manual override for a deliberate image change." >&2
    exit 10
  fi
fi

echo "Kubernetes drift detected, but no existing workload image replacement was found."
 || true)"
  desired_media_images="$(kubectl kustomize environments/prod 2>/dev/null | grep -E '^[[:space:]]+image:[[:space:]]+ghcr\.io/phanthienquoc/media-generation/(backend|frontend):[0-9a-f]{7,64}
     grep -q 'ghcr\.io/phanthienquoc/media-generation-backend:' <<<"$desired_media_images" &&
     grep -q 'ghcr\.io/phanthienquoc/media-generation-frontend:' <<<"$desired_media_images"; then
    echo "Allowing the intentional media-generation monolith -> backend/frontend image migration."
  else
    echo "ERROR: reconciliation would replace an existing workload image." >&2
    echo "The scheduled reconciler refuses image changes to prevent an unintended rollback." >&2
    echo "Removed image references:" >&2
    printf '%s\n' "$removed_images" >&2
    echo "Promote the intended immutable image through GitOps, or use the explicit manual override for a deliberate image change." >&2
    exit 10
  fi
fi

echo "Kubernetes drift detected, but no existing workload image replacement was found."
 || true)"
  legacy_debug_image="$(printf '%s\n' "$removed_images" | grep -F '-            image: rancher/kubectl:v1.36.3' || true)"
  desired_debug_image="$(kubectl kustomize environments/prod 2>/dev/null | grep -F 'image: rancher/kubectl:v1.36.2' || true)"

  if [[ -n "$legacy_media_image" ]] &&
     grep -q 'ghcr\.io/phanthienquoc/media-generation-backend:' <<<"$desired_media_images" &&
     grep -q 'ghcr\.io/phanthienquoc/media-generation-frontend:' <<<"$desired_media_images"; then
    echo "Allowing the intentional media-generation monolith -> backend/frontend image migration."
  elif [[ -n "$legacy_debug_image" && -n "$desired_debug_image" ]]; then
    echo "Allowing the intentional k3s-debug collector image update v1.36.3 -> v1.36.2."
  else
    echo "ERROR: reconciliation would replace an existing workload image." >&2
    echo "The scheduled reconciler refuses image changes to prevent an unintended rollback." >&2
    echo "Removed image references:" >&2
    printf '%s\n' "$removed_images" >&2
    echo "Promote the intended immutable image through GitOps, or use the explicit manual override for a deliberate image change." >&2
    exit 10
  fi
fi

echo "Kubernetes drift detected, but no existing workload image replacement was found."
