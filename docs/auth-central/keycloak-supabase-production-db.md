# Keycloak production database on Supabase PostgreSQL

## Goal

Configure the production Keycloak workload to use the existing Supabase PostgreSQL project as its **own isolated database/schema**, through the PostgreSQL JDBC driver. This is distinct from NestJS using `@supabase/supabase-js`.

Target Supabase project currently visible in the connected account:
- Project ref: `gtqovpusfyyvxpeezxlo`
- Region: `ap-southeast-1`
- PostgreSQL 17
- The project already stores application data for Auth, TCE, Media and other workloads. Do not use the existing `public` application tables as Keycloak storage.

## Where to obtain the JDBC URL

Open the project dashboard and choose **Connect**. Select the PostgreSQL connection options and copy the JDBC URL from the JDBC tab if shown. The Supabase JDBC example documents the session pooler on port `5432` for persistent connections from IPv4-only environments; a direct connection on port `5432` is suitable for persistent servers when the runtime network supports IPv6. Do not choose transaction pooler mode (port `6543`) as the initial Keycloak connection without compatibility tests.

Official docs:
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/platform/ssl-enforcement

## Required production configuration

Use a dedicated JDBC connection secret, separate from the existing NestJS SDK credentials:

- `KC_DB=postgres`
- `KC_DB_URL` = JDBC URL for the chosen direct or session-mode PostgreSQL endpoint, database `postgres`, SSL required.
- `KC_DB_USERNAME` = database role for Keycloak, not the `service_role` API key.
- `KC_DB_PASSWORD` = database password for that database role.
- `KC_DB_SCHEMA=keycloak` (only if the selected Keycloak release supports configuring schema this way; verify exact supported option for the pinned release before deployment).

The URL must be TLS-protected. Prefer CA/hostname verification when supported by the selected driver and connection setup; at minimum explicitly require SSL, never allow a plaintext fallback.

## Required isolation and access checks

Before production rollout:
1. Review current Supabase project plan, connection limits/headroom, network family from the Kubernetes VPS, SSL CA and backup/PITR settings.
2. Verify the pinned Keycloak release's PostgreSQL 17 compatibility and supported JDBC schema configuration.
3. Create a dedicated database role with only the permissions needed for the isolated Keycloak schema; do not reuse the Supabase `service_role` API key or expose it as a password.
4. Create an isolated `keycloak` schema and ensure no Keycloak tables land in `public`. Verify that the Keycloak database role can create/update objects in that schema but has no unnecessary application-data privileges.
5. Confirm the Keycloak startup migrations, health/readiness, restart persistence, backup and restore in a dedicated non-production environment before any production switch.
6. Keep existing NestJS Auth / TCE / Media workloads and their current `microfe-auth-secrets` unchanged. Keycloak should be a separate Deployment and use a separate Secret, not replace the existing `microfe-auth` service until a reviewed migration and rollback plan is complete.
7. Store the connection values as GitHub Actions **production Environment Secrets** or an approved external secret manager, then provision a Kubernetes Secret through an allowlisted protected workflow. Never place connection strings or passwords in Git, PR descriptions, ConfigMaps, logs, workflow outputs, realm exports or public variables.

## Release / rollout gate

This PR must only add documentation/manifest wiring and safe validation. It must not create or expose production credentials, run production database DDL, start a production Keycloak Deployment, change ingress/routing, or migrate users/sessions automatically. Those actions require confirmed JDBC parameters, verified role/schema isolation, health tests, and an explicit production rollout approval.

## Connection string shape

Examples are illustrative only; replace placeholders in the protected secret store, not in this file:

```text
jdbc:postgresql://db.<project-ref>.supabase.co:5432/postgres?sslmode=require
```

For a Supavisor session pooler, copy the project-specific JDBC/session URL from the Connect panel rather than inventing its hostname or username. The exact URI may include a pooler-specific username and must be percent-encoded if password characters require it.
