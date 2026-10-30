# SSO Auto-Onboarding Controller — Plan and Operations

Status: implementation baseline (2026-10-30)

## Goal

Make `platform-infra` the source of truth for approved Keycloak OIDC clients. A new application is onboarded by adding one reviewed manifest; after that manifest reaches `master`, GitHub Actions validates it and reconciles that one client against Keycloak. No application-specific edits to the controller workflow are needed.

## Current architecture

- Identity Provider: Keycloak at `https://sso.mrcute.space`, realm `mrcute`.
- Central session/API integration remains owned by the existing NestJS Auth service at `https://auth.mrcute.space`.
- Registry: `config/sso/apps/<app-id>.json`.
- Validation: `scripts/validate-sso-registry.py` (stdlib-only; safe for pull requests).
- Reconciliation: `scripts/reconcile-keycloak-client.py` (idempotent, one manifest per invocation).
- Automation: `.github/workflows/sso-auto-onboarding.yml`.
- Existing Keycloak admin credentials are read only from the protected GitHub `production` Environment.

## New-repository flow

1. Add `config/sso/apps/<app-id>.json` with repository ownership, exact HTTPS callback/logout URLs, origins and API audience.
2. Open a PR. The SSO registry validator checks every manifest, including exact-host allowlists, uniqueness, repository ownership and forbidden wildcard redirects.
3. Merge the PR. The workflow validates the registry again and reconciles only the manifest files changed by that push.
4. The reconciler creates or updates one public OIDC client with Authorization Code flow, PKCE S256, no implicit flow, no direct grants and no service account. It then verifies the resulting client contract.
5. A protected `production` Environment can require an approval before the workflow receives production credentials. Keep that protection enabled.
6. App teams still need to integrate OIDC/session handling and pass their application-level login/logout and API authorization tests. Creating a Keycloak client alone does not migrate an application to SSO.

## Security invariants

- Only repositories under `phanthienquoc/` and HTTPS hosts under `mrcute.space` are accepted by the initial policy. Expand the policy deliberately if another owner/domain is approved.
- Redirect URIs, web origins and post-logout redirects must be explicit; wildcard values are rejected.
- Browser apps use public clients and PKCE S256. No client secret is created or stored for browser apps.
- API audience is added to access tokens only, never ID tokens.
- No user accounts, roles, groups, app data, Supabase schemas, passwords or runtime secrets are created or modified by this workflow.
- Removing a manifest does not delete a live Keycloak client. Destructive deprovisioning is deliberately out of scope.
- Admin API tokens and response bodies are never printed. Provisioning is scoped to the `mrcute` realm and a single client ID.
- Do not enable SSO in an application just because its Keycloak client exists. App rollout/rollback and end-to-end validation remain separate gates.

## Rollout plan

### Phase 1 — registry and safe reconciliation (implemented here)
- Add schema-by-code validation, one manifest for the already documented TCE client, idempotent client reconciler, PR validation and post-merge reconciliation.
- Reconcile only changed manifest files to avoid touching unrelated clients.
- Use the protected production Environment for all writes.

### Phase 2 — central Auth integration
- Audit the current NestJS Auth session exchange and its client allowlist.
- Add a registry-backed allowlist only after confirming its runtime configuration and failure semantics.
- Add a dry-run diff and explicit verification for session exchange, issuer, audience and token lifetime.
- Do not change the shared JWT secret or user provisioning behavior as part of client onboarding.

### Phase 3 — repository discovery and SDK
- Add scheduled GitHub repository discovery that reports unregistered repositories and opens a proposal PR; never provision a client based solely on repository creation.
- Publish a shared OIDC integration contract/SDK and reusable app workflow.
- Add staging smoke tests, drift reporting and controlled deprovisioning with an explicit approval path.

## Operations

- Validate locally: `python3 scripts/validate-sso-registry.py`.
- Validate a single manifest: `python3 scripts/validate-sso-registry.py config/sso/apps/<app-id>.json`.
- Run a read-only configuration preview: `python3 scripts/reconcile-keycloak-client.py --manifest config/sso/apps/<app-id>.json --dry-run` with no Keycloak credentials required.
- Manual apply: dispatch `SSO auto-onboarding`, select `apply`, and provide the app ID. This uses the protected `production` Environment.
- Check the workflow run and the final `client_contract_valid=true` output. Never paste credentials or access tokens into logs/issues.

## Acceptance criteria

- Invalid JSON, duplicate IDs/client IDs/repositories/redirect URIs, wildcard redirects, non-HTTPS URLs, unapproved repository owners and hosts outside the allowlist fail validation.
- Pull requests cannot write to Keycloak.
- A merge affecting a manifest reconciles only changed manifest(s); unrelated clients remain untouched.
- Re-running reconciliation is idempotent.
- Reconciler refuses ambiguous client matches and never deletes clients.
- Existing TCE client ID, exact callback, origin, logout redirect and API audience contract are retained.
- Existing application users, roles, app data and central Auth behavior remain unchanged.
