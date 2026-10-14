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

## Exact GitHub repository settings

### Add to `phanthienquoc/platform-infra` → Settings → Secrets and variables → Actions

These are the **minimum required deployment settings** because platform-infra owns the GitOps/deployment workflow.

**Repository Actions Secrets**
| Name | Required | Notes |
|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY` | Yes, unless a valid Kubernetes fallback exists | Server-side Supabase privileged key; never expose to frontend |
| `JWT_SECRET` | Yes, unless a valid Kubernetes fallback exists | Must be a strong, existing production-compatible signing secret |
| `MFA_ENCRYPTION_KEY` | Yes, unless a valid Kubernetes fallback exists | Must match the key used to encrypt any existing MFA secrets |

**Repository Actions Variables**
| Name | Required | Notes |
|---|---|---|
| `SUPABASE_URL` | Yes, unless a valid Kubernetes fallback exists | Project URL; non-secret |

For this deployment, the expected Supabase project URL is `https://gtqovpusfyyvxpeezxlo.supabase.co`. Set it as a Variable, not a Secret, unless repository policy requires otherwise.

**Optional Actions Variables** (only add overrides when defaults are not correct)
| Name | Purpose |
|---|---|
| `MICROFE_AUTH_CORS_ORIGINS` | Allowed browser origins |
| `MICROFE_AUTH_JWT_ISSUER` | JWT issuer |
| `MICROFE_AUTH_JWT_AUDIENCE` | JWT audience |
| `MICROFE_AUTH_JWT_ACCESS_TTL_SECONDS` | Access-token TTL |
| `MICROFE_AUTH_JWT_REFRESH_TTL_SECONDS` | Refresh-token TTL |
| `MICROFE_AUTH_PASSKEY_RP_ID` | WebAuthn relying-party ID |
| `MICROFE_AUTH_PASSKEY_RP_NAME` | WebAuthn relying-party display name |
| `MICROFE_AUTH_PASSKEY_ORIGIN` | Exact allowed WebAuthn origin |

Legacy aliases accepted by the infra workflow, if used instead of canonical names:
- Secrets: `MICROFE_SUPABASE_SERVICE_ROLE_KEY`, `MICROFE_JWT_SECRET`, `MICROFE_MFA_ENCRYPTION_KEY`
- Variable: `MICROFE_SUPABASE_URL`

Prefer the canonical names above; do not create both canonical and alias entries unless there is a concrete workflow compatibility need.

### Add to `phanthienquoc/phanthienquoc-authentication` → Settings → Secrets and variables → Actions

Do **not** duplicate production deployment secrets here just because the app uses them at runtime. Add secrets/variables to this repository only if its own GitHub Actions workflows run integration tests against Supabase or perform a deployment.

If needed for an integration-test workflow, use test-project credentials only:
- Secrets: `SUPABASE_SERVICE_ROLE_KEY`, `JWT_SECRET`, `MFA_ENCRYPTION_KEY`
- Variable: `SUPABASE_URL`

Do not put production secrets into pull-request workflows that run on untrusted forks. Unit tests/typecheck/build should use mocks and should not need production credentials.

## Kubernetes fallback

If a GitHub Actions value is absent, deployment may use the already-approved existing Kubernetes sources:
- `microfe-auth-secrets` in the Auth workload namespace for the canonical Auth secret keys.
- Approved legacy TCE secrets/config keys where the existing workflow explicitly supports those mappings.
- The existing Kubernetes config/secret source for `SUPABASE_URL`.

The workflow must validate that every required value exists after fallback resolution and fail closed if any required value is missing. Never fabricate credentials or print secret values.

## Production rollout gates
1. Auth repository CI passes: tests, typecheck, build, and Docker image build.
2. Confirm Supabase project URL and target schema before applying the RPC migration.
3. Apply and verify the required Supabase RPC migration(s) using the approved migration process; do not run schema mutations implicitly during deployment.
4. Exercise signup/login, refresh rotation and replay/revocation, MFA recovery-code single-use, MFA challenge single-use, passkey challenge single-use/counter compare-and-set, CSRF and cookie behavior against a non-production project.
5. Verify required credentials exist by key name only; do not expose values.
6. Kustomize render and immutable image digest validation pass.
7. Rollout readiness/liveness and HTTPS checks pass before traffic cutover.

No production deploy or traffic cutover until all gates pass. Missing credentials may use an approved existing secret/config fallback; if no valid source exists, stop and report the exact missing key names.
