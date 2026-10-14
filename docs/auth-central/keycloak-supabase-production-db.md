# Keycloak production database on Supabase PostgreSQL

## Goal

Configure production Keycloak to use the existing Supabase PostgreSQL project through JDBC, isolated from existing application schemas. This is distinct from NestJS using `@supabase/supabase-js`.

Verified connected project metadata:
- Project ref: `gtqovpusfyyvxpeezxlo`
- Region: `ap-southeast-1`
- PostgreSQL 17
- Selected connection: **Supavisor Session Pooler**, port `5432`.
- Host supplied by operator: `aws-1-ap-southeast-1.pooler.supabase.com`
- Database: `postgres`
- Supavisor username supplied by operator: `postgres.gtqovpusfyyvxpeezxlo`
- Existing active application tables include NestJS Auth, TCE, Media and other application data. Keycloak must not create tables in the existing `public` application schema.

## JDBC URL

JDBC URL shape for the selected Session Pooler connection:

```text
jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
```

Use the pooler username as the separate `KC_DB_USERNAME` value:
```text
postgres.gtqovpusfyyvxpeezxlo
```

No database password was supplied or stored in this repository. Do not send it in chat or commit it to Git.

Official documentation:
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/platform/ssl-enforcement
- https://www.keycloak.org/server/db

This is a persistent Session Pooler connection on port 5432, not the transaction pooler on port 6543. Require TLS; prefer CA/hostname verification when supported by the selected driver configuration.

## Production runtime configuration

Use a **separate Keycloak Deployment and Secret**. The existing `microfe-auth` NestJS service must remain untouched.

After the dedicated least-privilege database role/schema are provisioned and tested, configure:
- `KC_DB=postgres`
- `KC_DB_URL=jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require`
- `KC_DB_USERNAME=postgres.gtqovpusfyyvxpeezxlo` (current project-level pooler user supplied by operator; replace with a dedicated least-privilege role if Supabase configuration supports it for this setup)
- `KC_DB_PASSWORD` = database password, held only in protected secret storage
- Configure the `keycloak` schema using only a setting supported by the pinned Keycloak release; validate the exact supported option before deployment.

Never use `SUPABASE_SERVICE_ROLE_KEY` as a JDBC password. It is an API key, not a PostgreSQL credential.

Store JDBC URL, username and password as GitHub Actions **production Environment Secrets** or an approved external secret manager. Provision them to a distinct Kubernetes Secret through a protected workflow that reads values via stdin. Never put secrets in Git, ConfigMaps, PR text, dispatch payloads, workflow outputs, artifacts or logs.

## Isolation and production gate

Before any production rollout:
1. Verify the Supavisor Session Pooler endpoint and TLS connectivity from the Kubernetes VPS; verify Supabase plan/connection headroom, TLS CA and backup/PITR restore path.
2. Pin a supported Keycloak release and verify compatibility with PostgreSQL 17 and the exact JDBC schema configuration.
3. Create an isolated `keycloak` schema and dedicated least-privilege database role. Verify the role cannot read/write existing application tables. Do not run Keycloak as the broad `postgres` owner long-term.
4. Test database initialization/migrations, restart persistence, login/session behavior, health/readiness and backup/restore in an approved non-production target first.
5. Add a separate Keycloak Deployment/Service, dedicated Secret references, health probes, resource limits, proxy/hostname/TLS settings and restricted admin access after checks.
6. Do not change `auth.mrcute.space` ingress or cut over TCE/Media as part of this database change. Existing NestJS Auth, TCE and Media must keep operating unchanged until a separately reviewed migration and rollback plan is approved.

No database DDL, role creation, credential creation, Kubernetes Secret mutation, live Keycloak deployment, DNS/Ingress change, or user/session migration is performed by this documentation PR.
