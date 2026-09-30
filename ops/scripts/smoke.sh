#!/usr/bin/env bash
set -euo pipefail

scope="${1:-tce-dashboard}"

check_url() {
  local name="$1"
  local url="$2"
  local expected="$3"
  local status

  status="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 15 "$url")"
  case "$status" in
    $expected)
      printf 'PASS %-20s %s [%s]\n' "$name" "$url" "$status"
      ;;
    *)
      printf 'FAIL %-20s %s [%s, expected %s]\n' "$name" "$url" "$status" "$expected" >&2
      return 1
      ;;
  esac
}

case "$scope" in
  'tce-dashboard')
    check_url 'tce-api-health' 'https://tce.mrcute.space/api/health' '2*'
    check_url 'tce-frontend' 'https://tce.mrcute.space/' '2*'
    ;;
  'stockdividend')
    check_url 'stock-admin' 'https://admin.mrcute.space/' '2*'
    check_url 'media-generation' 'https://media.mrcute.space/' '2*'
    ;;
  'media-generation')
    check_url 'media-generation' 'https://media.mrcute.space/' '2*'
    ;;
  'all')
    check_url 'tce-api-health' 'https://tce.mrcute.space/api/health' '2*'
    check_url 'tce-frontend' 'https://tce.mrcute.space/' '2*'
    check_url 'stock-admin' 'https://admin.mrcute.space/' '2*'
    ;;
  *)
    echo "Unsupported smoke scope: $scope" >&2
    exit 2
    ;;
esac
