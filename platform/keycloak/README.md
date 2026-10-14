# Keycloak — Auth Central

Public hostname: https://sso.mrcute.space

The existing NestJS Auth API continues to own https://auth.mrcute.space. Do not repoint it to Keycloak as part of this deployment.

## Runtime configuration

The Deployment pins Keycloak to 26.4.7 and uses the production `start` command (not `start-dev`). Database connections use the Supavisor Session Pooler URL stored in a protected Kubernetes Secret. It sets `KC_DB_SCHEMA=keycloak`, bounded connection-pool sizing, health/metrics endpoints and HTTPS-terminating ingress proxy headers.

GitHub Environment `production` secrets required by the protected reconciliation workflow:
- `KEYCLOAK_DB_URL`
- `KEYCLOAK_DB_USERNAME`
- `KEYCLOAK_DB_PASSWORD`
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

The reconciliation workflow materializes these into the Kubernetes Secret `keycloak-runtime-secrets` via stdin only; values must never be rendered into GitOps manifests, outputs, logs, artifacts or dispatch payloads.

## Rollout conditions

1. Set `KEYCLOAK_DB_USERNAME` to the dedicated PostgreSQL login role `keycloak_runtime` and `KEYCLOAK_DB_PASSWORD` to that role's password. Do not use the project owner `postgres` role as the long-term runtime account.
2. The DB role needs ownership of schema `keycloak` and permission to create/alter its own tables, but must not receive memberships in `postgres`, `service_role`, or other privileged roles.
3. Reconciliation must refuse rollout if any Keycloak secrets are missing or the DB username is not the dedicated role.
4. DNS for `sso.mrcute.space` must resolve to the existing Traefik public IP before cert-manager can issue TLS.
5. First deployment can take several minutes while Keycloak initializes schema. Readiness gates the public route, and `auth.mrcute.space` stays untouched.

## Database setup

The schema `keycloak` has been created in the linked Supabase project and verified empty. The initial migration attempt to create a login role was blocked because the connected migration executor could not `SET ROLE keycloak_runtime`; no DB role password was stored or committed. Before production rollout, create `keycloak_runtime` with `LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`, set a strong unique password through a protected database channel, make it owner of schema `keycloak`, and then set the matching GitHub Environment secret. Do not place a password in migration SQL or repository files.

## Production safety

This configuration is a proposed GitOps deployment. Do not merge or apply it until the runtime role/password, GitHub Environment secret scope, DNS and database connection have been independently validated.
