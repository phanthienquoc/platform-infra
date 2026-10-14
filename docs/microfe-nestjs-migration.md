# MicroFE NestJS Auth rollout contract

MicroFE Auth is a standalone NestJS + TypeScript service. NestJS owns authentication and authorization business logic; Supabase is used only as the persistence layer through the server-side Supabase client. Do not use Supabase Auth or Realtime.

## Runtime configuration
- Required secret values: `SUPABASE_SERVICE_ROLE_KEY`, `JWT_SECRET`, and `MFA_ENCRYPTION_KEY`.
- Required non-secret setting: `SUPABASE_URL` (GitHub Actions Variable preferred; an existing Kubernetes ConfigMap/Secret value may be used as fallback).
- Source runtime configuration from GitHub Actions Secrets/Variables first. If absent, fall back to existing `microfe-auth-secrets` and approved legacy TCE Kubernetes secret/config keys. Never log, decode for logs, or commit secret values.
- Required secrets must fail closed if no valid GitHub or Kubernetes source exists. Never generate fake credentials or use placeholder values for secrets.
- Keep auth business logic, cookie names/domain, API routes, password-hash compatibility, and existing user/session tables unchanged.
- Use the existing Supabase project and existing `public.users`, `public.refresh_sessions`, `public.mfa_recovery_codes`, `public.auth_passkey_challenges`, and `public.auth_passkey_credentials` tables. Do not create duplicate user/session tables.
- Apply the reviewed `supabase/migrations/20261012000000_auth_persistence_rpcs.sql` to the intended Supabase project before enabling the RPC-backed persistence paths. Confirm table/column compatibility first.
- Keep the service-role key server-side only. It must never be exposed to browser bundles, client responses, or logs.
- Preserve immutable SHA/digest image promotion.

## GitHub Actions configuration
Secrets (preferred; aliases may be supported):
- `SUPABASE_SERVICE_ROLE_KEY` or `MICROFE_SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET` or `MICROFE_JWT_SECRET`
- `MFA_ENCRYPTION_KEY` or `MICROFE_MFA_ENCRYPTION_KEY`

Variables:
- `SUPABASE_URL` or `MICROFE_SUPABASE_URL`
- Optional non-secret auth settings: CORS origins, JWT issuer/audience and TTLs, passkey RP ID/name/origin.

## Production rollout gates
1. Auth repository CI passes: tests, typecheck, build, and Docker image build.
2. Confirm Supabase project URL and target schema before applying the RPC migration.
3. Apply and verify `supabase/migrations/20261012000000_auth_persistence_rpcs.sql` using the approved migration process; do not run schema mutations implicitly during deployment.
4. Exercise signup/login, refresh rotation and replay/revocation, MFA recovery-code single-use, MFA challenge single-use, passkey challenge single-use/counter compare-and-set, CSRF and cookie behavior against a non-production project.
5. Verify required credentials exist by key name only; do not expose values.
6. Kustomize render and immutable image digest validation pass.
7. Rollout readiness/liveness and HTTPS checks pass before traffic cutover.

No production deploy or traffic cutover until all gates pass. Missing credentials may use an approved existing secret/config fallback; if no valid source exists, stop and report the exact missing key names.
