# Keycloak self-registration without email verification

This opt-in workflow enables public self-registration in the `mrcute` realm without requiring an email verification link.

## Apply

1. Open **Actions → Configure Keycloak Registration Without Email Verification**.
2. Select **Run workflow** on `master`.
3. Enter `ENABLE` in the confirmation field and run it.
4. Confirm the run succeeds and prints all `keycloak_no_email_*=true` checks.

It uses the existing `production` GitHub Environment secrets `KEYCLOAK_ADMIN_USERNAME` and `KEYCLOAK_ADMIN_PASSWORD`; no SMTP or Resend configuration is needed.

## Important access limitation

This only changes Keycloak registration. It does **not** create a TCE application account or bypass TCE's existing OIDC requirements for `email_verified=true` and an existing `ACTIVE` account. A user may be able to register at Keycloak but still be denied access to TCE. Do not remove those TCE checks globally: doing so could let an unverified email impersonate an existing account. Provision the application account through the trusted admin/onboarding flow.

Password-reset email remains disabled because no SMTP provider is configured. Registration is enabled only in the `mrcute` realm; the `master` realm is not changed.
