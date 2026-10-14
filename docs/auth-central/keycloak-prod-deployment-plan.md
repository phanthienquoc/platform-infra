# Keycloak production deployment plan

## Decision
- Keycloak external URL: https://sso.mrcute.space
- Existing NestJS Auth API remains https://auth.mrcute.space and must not be rerouted.
- Supabase PostgreSQL project `gtqovpusfyyvxpeezxlo`, Supavisor Session Pooler, database `postgres`, isolated schema `keycloak`.
- Keycloak workload is separate from NestJS Auth. Existing TCE/Media integration remains unchanged.

## Current status from implementation
- Supabase schema `keycloak` created; no tables existed in it at verification.
- Supabase migration API could create the schema, but role creation failed with `must be able to SET ROLE "keycloak_runtime"`. No DB role password was included in any migration. The dedicated runtime role must be created through an approved DB administration path before any rollout.
- GitHub deployment branch `feat/keycloak-prod-deployment` contains the initial Deployment, Service, Kustomize file, ingress, certificate, and README. This is not yet wired into production overlay or reconciliation because the existing self-hosted runner has a strict kubectl command allowlist.
- Secret values are not accessible through GitHub connector APIs; do not infer their values or write them to repository files.
- DNS for `sso.mrcute.space` has not been verified.
- No production Keycloak workload has been applied.

## Required GitHub Environment secrets
These must be in the `production` Environment because the workflow uses `environment: production`:
- `KEYCLOAK_DB_URL` = `jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require`
- `KEYCLOAK_DB_USERNAME` = `keycloak_runtime.gtqovpusfyyvxpeezxlo` (PostgreSQL role is `keycloak_runtime`; Supavisor Session Pooler requires `<role>.<project-ref>`)
- `KEYCLOAK_DB_PASSWORD` = password of the dedicated `keycloak_runtime` DB role, not the Supabase owner password
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

The previously shown secret screenshot proves only names exist, not values or scope. Do not paste passwords in chat.

## Release and runtime
Keycloak image currently proposed: `quay.io/keycloak/keycloak:26.4.7`; verify release support and image availability before apply. Runtime config sets `KC_DB=postgres`, `KC_DB_SCHEMA=keycloak`, health/metrics, bounded pool (max 10), `start` (never `start-dev`), external hostname and forwarded headers. Public DNS/TLS requires DNS to resolve to the existing Traefik public address.

## Production gates
1. Create `keycloak_runtime` as a unique login role with no superuser/create-db/create-role/replication/bypass-RLS privileges and no membership in privileged roles. Set a unique password outside Git and make it owner of only schema `keycloak`. Do not use the `postgres` owner role long term.
2. Query effective schema/table privileges to confirm it cannot read or write existing application schemas; inspect inherited PUBLIC grants / extensions such as `net` too.
3. Add a protected reconciliation action that provisions `keycloak-runtime-secrets` from GitHub Environment secrets via stdin only; extend the self-hosted runner allowlist in `scripts/bootstrap-runner.sh` and its sudo policy version in sync. Secret values must never appear in process args, logs, Git, artifacts, output variables or dispatch payloads.
4. Add the Keycloak resource to the prod Kustomize tree, but do not apply until secret provision + role checks and manifest validation pass.
5. Add a separate `sso.mrcute.space` TLS ingress / cert only after DNS verification. Keep existing `auth.mrcute.space` ingress backend unchanged.
6. Extend manifest validation/network allowlists and workflow contract test for a separate Keycloak deployment lane. Ensure unrelated Auth/TCE/Media lanes do not block each other.
7. Verify rollout/readiness, `https://sso.mrcute.space/realms/master/.well-known/openid-configuration`, TLS, DB persistence after restart, and rollback before integrating client apps.

## Not implemented yet
- No Keycloak DB login role/password.
- No Keycloak Kubernetes Secret.
- No production overlay entry or runner allowlist change yet.
- No DNS/Ingress activated.
- No app client or user/session migration.
