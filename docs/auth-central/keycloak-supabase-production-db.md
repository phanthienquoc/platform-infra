# Keycloak production database on Supabase PostgreSQL

## Goal

Configure production Keycloak to use the existing Supabase PostgreSQL project through JDBC, isolated from existing application schemas. This is distinct from NestJS using `@supabase/supabase-js`.

## Approved architecture

- Keycloak is the central OIDC/SAML identity provider.
- Public Keycloak hostname: `https://sso.mrcute.space`.
- Existing `https://auth.mrcute.space` remains routed to the current NestJS Auth API. Do not repoint or replace that route in this change.
- TCE, Media and other apps continue operating with their current auth integration until each receives a separately reviewed migration and rollback plan.
- Keycloak runs as its own Deployment and Service in namespace `microfe-platform`; it must not share the NestJS Auth Deployment, runtime Secret, database role, or application tables.
- This PR is preparatory. It does not activate the Keycloak workload, change DNS/Ingress, provision Kubernetes Secrets, mutate Supabase, or migrate users/sessions.

## Verified database target

- Project ref: `gtqovpusfyyvxpeezxlo`
- Region: `ap-southeast-1`
- PostgreSQL 17
- Selected connection: **Supavisor Session Pooler**, port `5432`.
- Host: `aws-1-ap-southeast-1.pooler.supabase.com`
- Database: `postgres`
- Current pooler username supplied by operator: `postgres.gtqovpusfyyvxpeezxlo`
- Existing active application tables include NestJS Auth, TCE, Media and other application data. Keycloak must not create tables in the existing `public` application schema.

## JDBC URL

```text
jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
```

Use the pooler username as the separate `KC_DB_USERNAME` value:

```text
postgres.gtqovpusfyyvxpeezxlo
```

No database password is stored in this repository. Do not send it in chat or commit it to Git.

Official documentation:
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/platform/ssl-enforcement
- https://www.keycloak.org/server/db

This is a persistent Session Pooler connection on port 5432, not the transaction pooler on port 6543. Require TLS; prefer CA/hostname verification when supported by the selected driver configuration.

## GitHub production Environment Secrets

The operator reports creating these five secrets in GitHub. The screenshot alone does not establish whether they are repository-level or in the `production` Environment, so verify their scope against the workflow's `environment: production`:

- `KEYCLOAK_DB_URL`
- `KEYCLOAK_DB_USERNAME`
- `KEYCLOAK_DB_PASSWORD`
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

The database password and admin password must remain protected values. Never print them, pass them in dispatch payloads, place them in manifests, or expose them in logs/artifacts. The bootstrap admin credential should be rotated/disabled according to the selected Keycloak release's supported bootstrap procedure after initial setup. A public SPA using Authorization Code + PKCE does not need a client secret; confidential server-side clients need separate per-client secrets.

## Production runtime configuration

Use a separate Keycloak Deployment and Kubernetes Secret. The existing `microfe-auth` NestJS service must remain untouched.

Expected database configuration:
- `KC_DB=postgres`
- `KC_DB_URL` from the protected `KEYCLOAK_DB_URL` secret
- `KC_DB_USERNAME` from `KEYCLOAK_DB_USERNAME`
- `KC_DB_PASSWORD` from `KEYCLOAK_DB_PASSWORD`
- Configure the `keycloak` schema using only an option verified against the exact pinned Keycloak release. Validate the selected release and PostgreSQL 17 compatibility before activation.

Do not use `SUPABASE_SERVICE_ROLE_KEY` as a JDBC password. It is an API key, not a PostgreSQL credential.

## Required gates before enabling production

1. **Database isolation:** create an isolated `keycloak` schema and a dedicated least-privilege database role. Verify that it cannot read/write existing application tables. The currently configured `postgres.*` pooler identity is broad and must not be the long-term production runtime identity.
2. **Connectivity:** verify Session Pooler connectivity and TLS from the Kubernetes VPS; confirm connection headroom, Supabase plan limits, and backup/PITR restore path.
3. **Version:** pin a supported Keycloak release and verify PostgreSQL 17 compatibility, schema configuration, hostname/proxy settings, and health endpoints for that exact release.
4. **Secret delivery:** provision a distinct Kubernetes Secret through a protected workflow that consumes GitHub Environment secrets via stdin. No inline Kubernetes Secret data in Git.
5. **Non-production test:** test schema initialization/migrations, restart persistence, login/session behavior, health/readiness, and backup/restore in an approved non-production target.
6. **Ingress/DNS:** only after gates 1–5 pass, add a dedicated `sso.mrcute.space` route and TLS certificate to Keycloak. Keep `auth.mrcute.space` unchanged.
7. **Rollout/rollback:** deploy the Keycloak workload separately, verify readiness and external OIDC discovery, and document rollback before production activation.

## Explicit exclusions

This documentation PR performs no database DDL, role creation, credential creation, Kubernetes Secret mutation, live Keycloak deployment, DNS/Ingress change, or user/session migration. Do not merge this preparatory documentation as if it deploys Keycloak.
