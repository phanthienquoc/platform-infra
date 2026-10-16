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

## Self-registration policy (proposed)

- Use a dedicated application realm named mrcute; keep the master realm admin-only.
- Enable user self-registration only for `mrcute`.
- Set email verification to disabled for this initial phase; SMTP is not a prerequisite.
- Do not grant administrator or application-specific roles to newly registered users by default.
- Password reset via email is not available until SMTP is configured.
- Email ownership is not verified in this phase. Before public registration is enabled, add edge rate limiting and abuse monitoring, and validate registration/login/password policy end to end.
- Create each app's OIDC client with exact redirect URIs and least-privilege role mappings in a separate reviewed step. Do not use wildcard redirect URIs.
- Do not enable public registration on master.

## Deployment guardrails

1. The production workflow refuses rollout unless `KEYCLOAK_DB_USERNAME=keycloak_runtime.gtqovpusfyyvxpeezxlo`, the DB URL equals the chosen Session Pooler URL, and all five secrets are present with minimum password lengths.
2. The dedicated workflow target `keycloak` provisions only the Keycloak Secret and applies only `platform/keycloak`; it does not apply `environments/prod` or restart other workloads.
3. The self-hosted VPS wrapper currently contains the Keycloak secret provision and apply allowlist, but Keycloak rollout is still allowlisted only for `--timeout=300s`. Previous bootstrap exceeded that window; update workflow and installed wrapper together before increasing it, then verify the exact allowlisted command.
4. DNS for `sso.mrcute.space` must resolve to the existing Traefik public IP so cert-manager can issue TLS. DNS is not controlled by these manifests.
5. Bootstrap admin secrets do not configure realm self-registration. Realm/client provisioning must be performed by a reviewed, idempotent Admin API job or an authenticated, controlled admin-console procedure. Never put admin credentials in Git, workflow outputs or logs.

## Activation status

This repository currently has Keycloak runtime infrastructure manifests, but no realm provisioning configuration or job is included here. This document records the desired policy only; it does not create the `mrcute` realm, enable registration, create app OIDC clients, or activate production registration. The database password is also a blocking runtime prerequisite noted above.
