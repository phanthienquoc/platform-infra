#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

manifest="apps/tce-dashboard/overlays/prod/kustomization.yaml"
python3 scripts/resolve-tce-gitops-image-refs.py --file "$manifest" --validate-pair
