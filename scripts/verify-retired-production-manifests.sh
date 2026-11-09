#!/usr/bin/env bash
set -euo pipefail

ROOT="$(printenv RETIRED_MANIFESTS_ROOT 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

fail() {
  echo "::error::$*" >&2
  exit 1
}

for retired_path in apps/stockdividend apps/media-generation; do
  if [[ -e "$ROOT/$retired_path" ]]; then
    fail "Retired production manifest tree must be absent: $retired_path"
  fi
done

for active_path in environments/prod platform apps; do
  [[ -d "$ROOT/$active_path" ]] || fail "Active production manifest path is missing: $active_path"
  set +e
  matches="$(grep -R -nE 'stock-prod|media-prod|ghcr\.io/phanthienquoc/(stockdividend|media-generation)' "$ROOT/$active_path" 2>&1)"
  status=$?
  set -e
  if (( status == 0 )); then
    printf '%s\n' "$matches" >&2
    fail "Retired StockDividend/Media namespace or image references remain under $active_path."
  elif (( status > 1 )); then
    printf '%s\n' "$matches" >&2
    fail "Unable to inspect active production manifest path: $active_path (grep exit=$status)."
  fi
done

echo "Active production manifest tree contains no retired StockDividend/Media namespace or image references."