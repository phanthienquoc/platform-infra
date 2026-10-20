# Keycloak — Auth Central

Public hostname: https://sso.mrcute.space

The existing NestJS Auth API continues to own https://auth.mrcute.space and is not modified by this rollout. Application OIDC clients are intentionally a separate reviewed task.

## Runtime configuration

Keycloak is pinned to `quay.io/keycloak/keycloak:26.8.1`, runs production `start`, and uses the Supavisor Session Pooler with `KC_DB_SCHEMA=keycloak`. Credentials are provisioned into Kubernetes Secret `keycloak-runtime-secrets` through stdin only.

Required GitHub Environment `production` secrets:
- `KEYCLOAK_DB_URL`
- `KEYCLOAK_DB_USERNAME` = `keycloak_runtime.gtqovpusfyyvxpeezxlo`
- `KEYCLOAK_DB_PASSWORD`
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

Never write secret values to manifests, workflow outputs, logs, artifacts or dispatch payloads. If any password has been exposed, rotate it through the appropriate protected administration channel.

## Database requirements

The database role `keycloak_runtime` must have a strong unique password, and the GitHub Environment secret `KEYCLOAK_DB_PASSWORD` must contain the same value. The Supavisor connection username is `keycloak_runtime.gtqovpusfyyvxpeezxlo`; the PostgreSQL role itself is named `keycloak_runtime`. The isolated schema `keycloak` must be writable by this role without granting access to application schemas. Validate the database connection before rollout.

## Realm policy

The idempotent Admin API provisioner creates or updates the dedicated `mrcute` realm and enforces:
- Self-registration enabled only in `mrcute`; the `master` realm remains admin-only.
- Email verification disabled; SMTP is not required for signup.
- Password reset by email disabled until SMTP is configured.
- Duplicate email addresses disabled, username editing disabled, brute-force protection enabled.
- Minimum 12-character password policy, excluding the username.
- User/admin event logging enabled.
- No application-specific roles or OIDC clients are created by this change.

Email ownership is not verified in this phase. The registration URL is protected by a dedicated Traefik rate-limit middleware (5 requests/minute/IP, burst 10). Monitor Keycloak security events and Traefik rate-limit responses after activation. Do not add wildcard redirect URIs when application clients are configured later.

## Deployment and validation

Use workflow dispatch `reconcile-vps.yml` with `mode=apply`, `target_app=keycloak`, and `allow_image_changes=false`. This path provisions only Keycloak's Secret, applies only `platform/keycloak`, waits for Keycloak readiness, then invokes the idempotent realm provisioner and verifies the live realm policy. It does not reconcile the shared production stack or change `auth.mrcute.space`.

The provisioner authenticates with the production Environment admin credentials and does not print tokens or response bodies. It preserves existing `mrcute` clients and unrelated realm settings. If Admin API authentication fails, stop and verify that the configured bootstrap account remains a valid persistent admin; do not work around this by enabling registration on `master`.

The self-hosted VPS wrapper currently allowlists Keycloak rollout with `--timeout=300s`; previous bootstrap exceeded that window. Update the workflow and installed wrapper policy together before increasing the timeout, and verify the exact allowlisted command. The deployment job must also verify DNS/TLS and OIDC discovery before provisioning.

## Scope and limitations

This change does not create app-specific OIDC clients, configure SMTP, enable email verification, or change the existing NestJS Auth API. Registration is public; rate limiting and event logging reduce but do not eliminate abuse risk. Review operational alerts and abuse monitoring before promoting this flow broadly.
