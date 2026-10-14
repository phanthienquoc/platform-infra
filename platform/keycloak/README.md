# Keycloak — Auth Central

Public hostname: https://sso.mrcute.space

The existing NestJS Auth API continues to own https://auth.mrcute.space. It remains unchanged by this rollout. TCE, Media and other consumers are not migrated in this PR.

## Runtime configuration

The Deployment pins Keycloak to `quay.io/keycloak/keycloak:26.8.1` and uses production `start`, not `start-dev`. It uses the Supavisor Session Pooler URL via a protected Kubernetes Secret, `KC_DB_SCHEMA=keycloak`, bounded connection-pool sizing, health/metrics endpoints and forwarded headers for TLS termination at Traefik.

Required GitHub Environment `production` secrets:
- `KEYCLOAK_DB_URL`
- `KEYCLOAK_DB_USERNAME` = `keycloak_runtime.gtqovpusfyyvxpeezxlo` (Supavisor username syntax)
- `KEYCLOAK_DB_PASSWORD`
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

Provisioning will materialize these into Kubernetes Secret `keycloak-runtime-secrets` through stdin only. Secret values must never be written to manifests, workflow outputs, logs, artifacts or dispatch payloads.

## Supabase database state

The isolated schema `keycloak` exists. The dedicated login role `keycloak_runtime` was created with `LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`, and it has `CONNECT` on database `postgres` and `USAGE, CREATE` on schema `keycloak`. It is not a member of privileged app roles. Live privilege checks confirmed it has no SELECT/INSERT/UPDATE/DELETE permission on `public.users`, and no usage on `auth`, `storage` or `extensions` schemas.

The database login **does not yet have a password**. Set a strong unique password through a protected database administration channel and set the same value in GitHub Environment secret `KEYCLOAK_DB_PASSWORD`. For the Supavisor pooler connection, the **connection username** in GitHub must be `keycloak_runtime.gtqovpusfyyvxpeezxlo`; the actual PostgreSQL role is named `keycloak_runtime`. Never paste it into chat or commit it. The schema remains owned by the database owner; Keycloak can create/alter its own objects within `keycloak` using its schema privileges. Verify effective grants and TLS connection before rollout.

## Deployment guardrails

1. The production workflow refuses rollout unless `KEYCLOAK_DB_USERNAME=keycloak_runtime.gtqovpusfyyvxpeezxlo`, the DB URL equals the chosen Session Pooler URL, and all five secrets are present with minimum password lengths.
2. The dedicated workflow target `keycloak` provisions only the Keycloak Secret and applies only `platform/keycloak`; it does not apply `environments/prod` or restart other workloads.
3. The self-hosted VPS wrapper must be updated from policy v9 to v10 by running the reviewed `scripts/bootstrap-runner.sh` through the normal platform administration process. Until that server-side allowlist is updated, the new Keycloak provisioning/apply commands are intentionally rejected.
4. DNS for `sso.mrcute.space` must resolve to the existing Traefik public IP so cert-manager can issue TLS. DNS is not controlled by these manifests.
5. After initial bootstrap, follow Keycloak's supported procedure for rotating/removing bootstrap admin credentials; do not rely on bootstrap variables as an ongoing user-management mechanism.

## Activation status

The isolated manifests and workflow are proposed on the deployment branch but are not merged or live. No Keycloak Kubernetes Secret, production workload, public ingress activation, app client, or user/session migration has been performed.
