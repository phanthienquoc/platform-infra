# Keycloak self-registration rollout

## Goal
Provide a shared account registration experience at https://sso.mrcute.space for the central SSO realm, while keeping the existing NestJS Auth API at https://auth.mrcute.space unchanged.

## Current verified baseline
- Keycloak 26.8.1 is running in namespace `microfe-platform`.
- Public OIDC discovery for `/realms/master/.well-known/openid-configuration` returns HTTP 200.
- This proves the service and discovery endpoint work; it does not prove self-registration, email verification, password reset, SMTP delivery, or application client authorization.

## UX
Use Keycloak's built-in account console/login pages initially (no custom theme required for the first safe release):
- Login page has a Register link.
- Registration collects email, username (or email-as-username, according to realm policy), first name, last name, password, and password confirmation.
- Email verification is required before the account is considered verified.
- Forgot-password flow sends a reset email.
- User-facing errors do not reveal whether an email is already registered.

A branded custom Keycloak theme can be a separate iteration after the end-to-end flow works.

## Realm and access policy
- Do not enable public self-registration on the `master` realm. Keep it reserved for Keycloak administration.
- Create a dedicated application realm named `mrcute` for shared application identities.
- Enable self-registration and email verification only on `mrcute`.
- New accounts receive no administrator privileges and no project-specific roles by default.
- Create separate OIDC clients for the three applications; configure exact redirect URIs and web origins per app. Do not use wildcard redirect URIs.
- Keep `auth.mrcute.space` and the existing NestJS Auth API unchanged during rollout.

## Email prerequisites (blocking gate)
Before enabling public registration, configure valid SMTP settings in the `mrcute` realm using a dedicated mail account/provider. Store SMTP credentials only in a protected secret store; never commit credentials or print them in workflow logs. Verify:
1. SMTP connection succeeds over TLS.
2. Verification email arrives and its link works over HTTPS.
3. Password-reset email arrives and its link works.
4. Expired/invalid links fail safely.
5. Rate limits / abuse controls are in place (at minimum edge rate limiting and monitoring).

SMTP provider/host, port, sender address, and credentials have not yet been supplied or verified. Therefore public self-registration must remain disabled until this gate is completed.

## Implementation sequence
1. Configure the `mrcute` realm and its email/password policies through the Keycloak Admin Console or a reviewed, idempotent Admin API provisioning job.
2. Configure SMTP through a protected admin path; do not put SMTP credentials in GitOps manifests.
3. Enable registration and email verification for `mrcute` only.
4. Add one OIDC client per app with exact callback URLs and least-privilege role mappings.
5. Test registration, verification, login, logout, password reset, duplicate email, invalid token, and direct access to each app.
6. Enable public registration only after all tests pass.

## Acceptance criteria
- `https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration` returns HTTP 200 with issuer `https://sso.mrcute.space/realms/mrcute`.
- Login page exposes a Register link for the `mrcute` realm.
- Registration creates a user only in `mrcute`; the user must verify their email.
- New users do not gain admin roles or automatic access to all three apps.
- Password reset email works end to end.
- Existing `master` realm administration and `auth.mrcute.space` remain unaffected.

## Operational note
The first Keycloak bootstrap took longer than the existing 300-second deployment rollout wait. Before the next Keycloak deployment, update both the GitHub workflow and the installed `platform-kubectl` allowlist together to use a 900-second timeout, then verify the exact allowlisted command. Updating only the workflow would be rejected by the wrapper.
