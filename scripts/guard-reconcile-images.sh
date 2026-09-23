#!/usr/bin/env bash
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
sudo /usr/local/sbin/platform-kubectl diff -k environments/prod >"$diff_output"
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

removed_images="$(grep -E '^-([[:space:]]+)image:' "$diff_output" || true)"

if [[ -n "$removed_images" ]]; then
  echo "ERROR: reconciliation would replace an existing workload image." >&2
  echo "The scheduled reconciler refuses image changes to prevent an unintended rollback." >&2
  echo "Removed image references:" >&2
  printf '%s\n' "$removed_images" >&2
  echo "Promote the intended immutable image through GitOps, or use the explicit manual override for a deliberate image change." >&2
  exit 10
fi

echo "Kubernetes drift detected, but no existing workload image replacement was found."
