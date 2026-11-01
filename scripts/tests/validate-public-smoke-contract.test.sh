#!/usr/bin/env bash
set -euo pipefail

smoke_script="ops/scripts/smoke.sh"

grep -Fq "check_url 'auth-health' 'https://auth.mrcute.space/api/health' '2*'" "$smoke_script"
grep -Fq "check_url 'auth-ready' 'https://auth.mrcute.space/api/ready' '2*'" "$smoke_script"
grep -Fq "check_url 'auth-me-unauthenticated' 'https://auth.mrcute.space/auth/me' '401'" "$smoke_script"
grep -Fq "check_url 'tce-api-health' 'https://tce.mrcute.space/api/health' '2*'" "$smoke_script"
grep -Fq "check_url 'tce-frontend' 'https://tce.mrcute.space/' '2*'" "$smoke_script"

auth_ready_count="$(grep -Fc "check_url 'auth-ready'" "$smoke_script")"
[[ "$auth_ready_count" -eq 2 ]] || {
  echo "Expected Auth readiness in both TCE and all scopes; found $auth_ready_count" >&2
  exit 1
}

if grep -Fq "https://auth.mrcute.space/health" "$smoke_script"; then
  echo "Obsolete unprefixed Auth health endpoint remains in the smoke contract." >&2
  exit 1
fi

echo "Public TCE/Auth smoke endpoint contract validation passed."
