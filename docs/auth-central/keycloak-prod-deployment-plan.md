# Keycloak production deployment plan

> **Status: PLAN ONLY / BLOCKED — NOT APPROVED FOR PRODUCTION ACTIVATION.**
>
> The shared Supabase project `gtqovpusfyyvxpeezxlo` is explicitly a **non-production validation target only**. It is not an approved production Keycloak database. Do not use its project ref, pooler username, or connection settings in the GitHub `production` Environment or a production rollout. Production activation requires a separately provisioned and verified database target, documented backup/PITR and restore path, and a reviewed rollout/rollback plan.

## Architecture decision
- Keycloak external URL: https://sso.mrcute.space
- Existing NestJS Auth API remains https://auth.mrcute.space and is not rerouted.
- The existing Supabase PostgreSQL project `gtqovpusfyyvxpeezxlo` is for **non-production validation only**, using Supavisor Session Pooler, database `postgres`, and isolated schema `keycloak`.
- **Production database target: not yet identified or approved.** Do not point a production Keycloak workload at the shared non-production project.
- Keycloak is a separate workload and is targeted explicitly through a dedicated deployment lane. TCE/Media integration is not migrated in this PR.

## Supabase implementation state
- Schema `keycloak` was created and verified empty before workload implementation in the shared non-production project.
- Login role `keycloak_runtime` was created as `LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS` for non-production validation only.
- It has database CONNECT and schema USAGE/CREATE on `keycloak`; it has no membership in privileged application roles. Live privilege queries confirmed no SELECT/INSERT/UPDATE/DELETE rights on `public.users`, and no USAGE on `auth`, `storage`, or `extensions`.
- The role **has no password yet**. The operator must set a unique secret through a protected database administration channel and use the identical value only in the approved non-production GitHub Environment secret. This password must never be sent in chat, written in migration SQL, or committed to Git.
- Keycloak role must not be the `postgres` owner connection. Inspect effective grants/extension PUBLIC access and verify TLS JDBC connectivity before any activation.

## GitHub implementation branch
Branch: `feat/keycloak-prod-deployment`

Files added:
- `platform/keycloak/deployment.yaml`: separate Keycloak Deployment and ClusterIP Service, image `quay.io/keycloak/keycloak:26.8.1`, production start mode, pinned hostname, separate DB schema, bounded pool and probes.
- `platform/keycloak/kustomization.yaml`, `ingress.yaml`, `certificate.yaml`: isolated SSO route/certificate for `sso.mrcute.space`.
- `platform/keycloak/README.md`: deployment contract and safety gates.
- `scripts/bootstrap-runner.sh`: proposed v10 allowlist actions for stdin-only Secret provisioning, Secret verification and a Keycloak-only Kustomize apply/rollout/read path.
- `.github/workflows/reconcile-vps.yml`: explicit `target_app=keycloak` deployment lane; skips regular environment apply and skips actions that restart/alter other app workloads.
- `scripts/verify-workload-health.sh`, `scripts/validate-workflow-contracts.py`, `.github/workflows/validate-manifests.yml`: Keycloak health/manifest/workflow contract validation.
- Existing shared ingress still routes `auth.mrcute.space` to `microfe-auth`; new SSO route is a separate resource inside `platform/keycloak`, not included in regular app reconciliation.

## Non-production validation Environment secret references
The following connection settings refer only to the shared non-production project. Do not place them in GitHub Environment `production` or reuse them for a production deployment.
- `KEYCLOAK_DB_URL` = `jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require`
- `KEYCLOAK_DB_USERNAME` = `keycloak_runtime.gtqovpusfyyvxpeezxlo` (Supavisor username syntax)
- `KEYCLOAK_DB_PASSWORD` = password set on `keycloak_runtime` using a protected database admin channel
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

The earlier screenshot showed secret names only; it did not prove their values or that they are in the intended Environment. The workflow does not read secret values through the GitHub connector. Never paste passwords in chat. The bootstrap admin credential should be rotated/disabled according to the selected Keycloak release's supported bootstrap procedure after initial setup. A public SPA using Authorization Code + PKCE does not need a client secret; confidential server-side clients need separate per-client secrets.

## Production gates before first activation
1. **Production target separation:** provision and verify a dedicated production database target. Do not reuse `gtqovpusfyyvxpeezxlo`. Confirm connection budget, backup/PITR and restore path before production activation.
2. **Database isolation:** use a dedicated least-privilege login role and isolated `keycloak` schema. Verify that it cannot read/write existing application tables.
3. **Connectivity:** verify Session Pooler connectivity and TLS from the Kubernetes VPS; confirm connection headroom, Supabase plan limits, and backup/PITR restore path.
4. **Version:** pin a supported Keycloak release and verify PostgreSQL 17 compatibility, schema configuration, hostname/proxy settings, and health endpoints for that exact release.
5. **Secret delivery:** provision a distinct Kubernetes Secret through a protected workflow that consumes GitHub Environment secrets via stdin. No inline Kubernetes Secret data in Git. Production secrets must reference only the separately approved production database.
6. **Non-production test:** test schema initialization/migrations, restart persistence, login/session behavior, health/readiness, and backup/restore in an approved non-production target.
7. **Ingress/DNS:** only after gates 1–5 pass, add a dedicated `sso.mrcute.space` route and TLS certificate to Keycloak. Keep `auth.mrcute.space` unchanged.
8. **Rollout/rollback:** deploy the Keycloak workload separately, verify readiness and external OIDC discovery, and document rollback before integrating any app clients.

## Not done yet
- No DB password was set on the shared non-production `keycloak_runtime` role.
- No Keycloak Kubernetes Secret was provisioned.
- No Keycloak workload/ingress/certificate has been applied to the live cluster.
- DNS has not been verified.
- No app client, user or session migration has been performed.
