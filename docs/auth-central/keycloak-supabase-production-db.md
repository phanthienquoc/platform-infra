# Keycloak production database on Supabase PostgreSQL

## Goal

Configure production Keycloak to use the existing Supabase PostgreSQL project through JDBC, isolated from existing application schemas. This is distinct from NestJS using `@supabase/supabase-js`.

Verified connected project metadata:
- Project ref: `gtqovpusfyyvxpeezxlo`
- Region: `ap-southeast-1`
- PostgreSQL 17
- Direct connection supplied by the operator: host `db.gtqovpusfyyvxpeezxlo.supabase.co`, port `5432`, database `postgres`, username currently shown as `postgres`.
- Existing active application tables include NestJS Auth, TCE, Media and other application data. Keycloak must not create tables in the existing `public` application schema.

## JDBC URL

The JDBC URL shape for the supplied direct connection is:

```text
jdbc:postgresql://db.gtqovpusfyyvxpeezxlo.supabase.co:5432/postgres?sslmode=require
```

No database password was supplied or stored in this repository. Do not send the password in chat or commit it to Git.

Official documentation:
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/platform/ssl-enforcement
- https://www.keycloak.org/server/db

Network decision:
- Direct connection port 5432 works when the Kubernetes VPS supports IPv6 or the project has appropriate IPv4 connectivity.
- If the VPS is IPv4-only, copy the project's **Session Pooler** JDBC URL from Supabase Connect; use port 5432 and its pooler-specific username. Do not guess the pooler hostname/username.
- Do not select transaction pooler port 6543 as the default without compatibility testing.
- Require TLS; prefer CA/hostname verification when supported.

## Production runtime configuration

Use a **separate Keycloak Deployment and Secret**. The existing `microfe-auth` NestJS service must remain untouched.

After the connection path is confirmed and a dedicated role is created, configure:
- `KC_DB=postgres`
- `KC_DB_URL` = JDBC URL above (or the actual Session Pooler URL if direct networking is unsuitable)
- `KC_DB_USERNAME` = dedicated least-privilege role for Keycloak, rather than the broad `postgres` account
- `KC_DB_PASSWORD` = database password for that role
- Configure the `keycloak` schema using only a setting supported by the pinned Keycloak release; validate the exact supported option before deployment.

Never use `SUPABASE_SERVICE_ROLE_KEY` as a JDBC password. It is an API key, not a PostgreSQL credential.

Store JDBC URL, username and password as GitHub Actions **production Environment Secrets** or an approved external secret manager. Provision them to a distinct Kubernetes Secret through a protected workflow that reads values via stdin. Never put secrets in Git, ConfigMaps, PR text, dispatch payloads, workflow outputs, artifacts or logs.

## Isolation and production gate

Before any production rollout:
1. Confirm the Kubernetes VPS network supports the selected connection, and verify Supabase plan/connection headroom, TLS CA and backup/PITR restore path.
2. Pin a supported Keycloak release and verify compatibility with PostgreSQL 17 and the exact JDBC schema configuration.
3. Create an isolated `keycloak` schema and dedicated least-privilege database role. Verify the role cannot read/write existing application tables.
4. Test database initialization/migrations, restart persistence, login/session behavior, health/readiness and backup/restore in an approved non-production target first.
5. Add a separate Keycloak Deployment/Service, dedicated Secret references, health probes, resource limits, proxy/hostname/TLS settings and restricted admin access after checks.
6. Do not change `auth.mrcute.space` ingress or cut over TCE/Media as part of this database change. Existing NestJS Auth, TCE and Media must keep operating unchanged until a separately reviewed migration and rollback plan is approved.

No database DDL, role creation, credential creation, Kubernetes Secret mutation, live Keycloak deployment, DNS/Ingress change, or user/session migration is performed by this documentation PR.
