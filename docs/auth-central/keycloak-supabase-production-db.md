# Keycloak production database on Supabase PostgreSQL

## Goal

Configure production Keycloak to use the existing Supabase PostgreSQL project through JDBC, isolated from the existing application schemas. This is different from NestJS using `@supabase/supabase-js`.

Verified connected project metadata:
- Project ref: `gtqovpusfyyvxpeezxlo`
- Region: `ap-southeast-1`
- PostgreSQL 17
- Existing active application tables include NestJS Auth, TCE, Media and other application data. Keycloak must not create its tables in the existing `public` application schema.

## Obtain the JDBC connection string

In Supabase Dashboard, open the project and select **Connect**. Choose the PostgreSQL/JDBC tab. In the Session pooler section, copy the JDBC URL if available. Do not copy credentials into Git or chat.

The user's screenshot shows the Session pooler screen and a JDBC selector. The exact host, pooler username and password remain secrets; use the URL copied from Dashboard, not a reconstructed URL.

Official documentation:
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/platform/ssl-enforcement
- https://www.keycloak.org/server/db

For a persistent Keycloak server:
- Direct connection, port 5432, is suitable if the Kubernetes VPS supports IPv6 (or the project has IPv4 connectivity).
- Supavisor Session Pooler, port 5432, is the alternative for persistent clients on IPv4-only networks.
- Do not choose transaction pooler port 6543 as the default without testing Keycloak/JDBC session behavior.

Illustrative URL shape only:
```text
jdbc:postgresql://<host>:5432/postgres?sslmode=require
```

Copy the project-specific JDBC string from the Dashboard, including its correct hostname, username parameters and SSL settings. Prefer certificate/hostname verification if available. Do not use plaintext or permit SSL fallback.

## Production runtime configuration

Use a **separate Keycloak Deployment and Secret**. The existing `microfe-auth` NestJS service must remain untouched.

Keycloak runtime settings to wire after confirming the pinned Keycloak release's supported options:
- `KC_DB=postgres`
- `KC_DB_URL` = JDBC URL copied from Supabase Connect, with TLS required
- `KC_DB_USERNAME` = dedicated database role for Keycloak (not the Supabase API service-role key)
- `KC_DB_PASSWORD` = database password for that role
- Configure the `keycloak` schema using only a setting supported by the pinned Keycloak release; validate this exact option in its documentation before deploying.

Never use `SUPABASE_SERVICE_ROLE_KEY` as a JDBC password. It is an API key, not a PostgreSQL credential.

Store JDBC URL, username and password as GitHub Actions **production Environment Secrets** or an approved external secret manager. Provision them to a distinct Kubernetes Secret through a protected workflow that reads secret values via stdin. Never place them in Git, ConfigMaps, PR text, dispatch payloads, workflow outputs, artifacts or logs.

## Isolation and production gate

Before any production rollout:
1. Confirm the project is approved for Keycloak and verify Supabase plan, connection headroom, the cluster's network/IP mode, TLS CA and backup/PITR restore path.
2. Pin a supported Keycloak release and verify compatibility with PostgreSQL 17 and the exact JDBC schema configuration.
3. Create an isolated `keycloak` schema and a dedicated least-privilege database role. Verify the role cannot read/write existing application tables.
4. Test Keycloak database initialization/migrations, restart persistence, login/session behavior, health/readiness and backup/restore in an approved non-production target first.
5. Add a separate Keycloak Deployment/Service, dedicated Secret references, health probes, resource limits, proxy/hostname/TLS settings and restricted admin access after those checks.
6. Do not change `auth.mrcute.space` ingress or cut over TCE/Media as part of this DB change. Existing NestJS Auth, TCE and Media must keep operating unchanged until an independently reviewed migration and rollback plan is approved.

No database DDL, role creation, credential creation, Kubernetes secret mutation, live Keycloak deploy, DNS/Ingress change, or user/session migration is performed by this documentation PR.
