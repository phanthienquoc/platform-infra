#!/usr/bin/env bash
set -euo pipefail
curl -fsS https://tce.mrcute.space/api/health >/dev/null
curl -fsS https://tce.mrcute.space/ >/dev/null
curl -fsS https://admin.mrcute.space/ >/dev/null
