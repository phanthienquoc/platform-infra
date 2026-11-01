# GitHub Credentials Key Inventory

**Audited:** 2026-11-01  
**Purpose:** Reusable index of GitHub Actions secret and variable names referenced by workflows across TCE Dashboard, StockDividend, Authentication, and Platform Infra.  
**Safety:** This document intentionally contains names and usage metadata only. It MUST NOT contain credential values, environment-file contents, generated tokens, or copies of GitHub secret values.

## Source coverage

Inventoried the workflow files currently present in these repositories:

- [TCE Dashboard workflows](https://github.com/phanthienquoc/TCE-dashboard/tree/master/.github/workflows)
- [StockDividend workflows](https://github.com/phanthienquoc/stockdividend/tree/master/.github/workflows)
- [Authentication workflows](https://github.com/phanthienquoc/phanthienquoc-authentication/tree/master/.github/workflows)
- [Platform Infra workflows](https://github.com/phanthienquoc/platform-infra/tree/master/.github/workflows)

GitHub Actions can resolve secrets/variables from repository, organization, and environment scopes. A workflow reference proves the name is used, not which configuration scope supplies its value. Verify scope in GitHub Settings before rotating or moving keys.

## Quick index — GitHub Secrets

| Name | Referenced in | Purpose / handling |
|---|---|---|
| `BINANCE_TESTNET_API_KEY` | TCE Dashboard: `wf-07-tce-integration-check.yml` | Binance **testnet-only** integration checks; never use production credentials for this key. |
| `BINANCE_TESTNET_API_SECRET` | TCE Dashboard: `wf-07-tce-integration-check.yml` | Binance testnet secret paired with the testnet API key. |
| `GHCR_READ_TOKEN` | Platform Infra: `gitops-image-promotion.yml`, `reconcile-vps.yml` | Canonical read-only credential stored in the protected `production` Environment and used by both GHCR-consuming promotion jobs plus production reconciliation. Use a **classic PAT** owned by the configured `GHCR_USERNAME`, with `read:packages`, package-level access to every required private image across `microfe-platform`, `stock-prod`, `tce-prod`, and `media-prod`, and SSO authorization where required. A non-empty secret is not proof of registry access; the workflow distinguishes registry-login rejection from manifest/package access denial. No `GITHUB_TOKEN` fallback. Jobs consuming this Environment secret must declare `environment: production`. |
| `JWT_SECRET` | TCE Dashboard: `wf-01-tce-build-verify.yml`; Platform Infra: `provision-auth-runtime-secret.yml`, `reconcile-vps.yml` | Server-side JWT signing secret. Platform Infra consumes it from the protected `production` Environment when provisioning the Auth runtime. Do not print or rotate casually; coordinate session compatibility. |
| `KEYCLOAK_ADMIN_PASSWORD` | Platform Infra: `reconcile-vps.yml` | Keycloak administrator password. Treat as high sensitivity. |
| `KEYCLOAK_ADMIN_USERNAME` | Platform Infra: `reconcile-vps.yml` | Keycloak administrator login identifier; currently referenced through the secret context. |
| `KEYCLOAK_DB_PASSWORD` | Platform Infra: `reconcile-vps.yml` | Keycloak database credential. |
| `KEYCLOAK_DB_URL` | Platform Infra: `reconcile-vps.yml` | Keycloak database connection URL; may itself embed credentials, so never log it. |
| `KEYCLOAK_DB_USERNAME` | Platform Infra: `reconcile-vps.yml` | Keycloak database username; currently referenced through the secret context. |
| `MFA_ENCRYPTION_KEY` | TCE Dashboard: `wf-01-tce-build-verify.yml`; Platform Infra: `provision-auth-runtime-secret.yml`, `reconcile-vps.yml` | Backend MFA-encryption key. Platform Infra maps the production Environment secret into the Auth runtime secret. Preserve ciphertext compatibility. |
| `MFA_ENCRYPTION_KEY_PROD` | TCE Dashboard: `wf-10-tce-k3s-bootstrap.yml` | Separate TCE production bootstrap key name; do not assume it is a synonym for `MFA_ENCRYPTION_KEY`. |
| `MFA_ENCRYPTION_KEY_STG` | TCE Dashboard: `wf-10-tce-k3s-bootstrap.yml` | Separate TCE staging bootstrap key name; do not reuse the production value by assumption. |
| `PLATFORM_INFRA_TOKEN` | TCE Dashboard: `wf-03-tce-production-deploy.yml`, `wf-08b-tce-microfe-build-publish.yml`; StockDividend: `wf-platform-infra-release.yml` | Cross-repository release/GitOps handoff token. StockDividend requires `Contents: write` access to `phanthienquoc/platform-infra` for `repository_dispatch`; TCE workflows use it for their release handoff. This is separate from `GHCR_READ_TOKEN` and Authentication's `PLATFORM_INFRA_DISPATCH_TOKEN`. |
| `Platform-infra-token` | Platform Infra: `.github/workflows/mirror-locally-uncensored.yml` | Cross-repository mirror write credential for `phanthienquoc/locally-uncensored-private`; the latest scheduled run observed it resolving empty. Requires target-repository `Contents: write`; the connector cannot verify secret configuration. Do not substitute GHCR or application dispatch credentials without scope verification. |
| `PLATFORM_INFRA_DISPATCH_TOKEN` | Media Generation: `wf-03-media-production-deploy.yml`; Authentication: `release.yml` | Cross-repository release handoff token used to dispatch release events to Platform Infra. Media also queries Platform Infra Actions runs to verify the handoff, so its repository secret needs `Contents: write` and `Actions: read` on `phanthienquoc/platform-infra`; Auth needs dispatch permission (`Contents: write`). Same secret name does not imply the repositories use the same token value. Keep it distinct from TCE/StockDividend's `PLATFORM_INFRA_TOKEN` . |
| `RUNNER_REGISTRATION_PAT` | Platform Infra: `bootstrap-runner.yml` | PAT used to request a short-lived self-hosted runner registration token. Prefer minimal repository/action-runner administration scope; never store the generated short-lived token. |
| `SUPABASE_SERVICE_ROLE_KEY` | TCE Dashboard: `wf-01-tce-build-verify.yml`; Platform Infra: `provision-auth-runtime-secret.yml`, `reconcile-vps.yml` | Privileged Supabase backend credential. Keep server-only; never expose in frontend, logs, artifacts, command output, or this inventory. |
| `SUPABASE_URL` | TCE Dashboard: `wf-01-tce-build-verify.yml`; Platform Infra: `provision-auth-runtime-secret.yml`, `reconcile-vps.yml` | Supabase project URL used by backend runtime. May be non-secret configuration, but retain the currently configured protected source until environment ownership is verified. |
| `TELEGRAM_BOT_TOKEN` | Platform Infra: `reconcile-vps.yml` | Telegram bot credential used for infrastructure notifications; referenced via the **secret** context here. |
| `VPS_HOST` | Platform Infra: `bootstrap-runner.yml` | VPS endpoint used for runner bootstrap SSH. Currently stored under the secret context. |
| `VPS_SSH_PRIVATE_KEY` | TCE Dashboard: `wf-01-tce-build-verify.yml`, `wf-04-tce-k3s-cleanup.yml`, `wf-06-tce-healthcheck.yml`, `wf-07-tce-backup.yml`, `wf-09-nginx-readonly-audit.yml`, `wf-09-tce-vps-safe-setup.yml`, `wf-10-tce-k3s-bootstrap.yml`; Platform Infra: `bootstrap-runner.yml` | SSH private key for VPS access. Never commit, echo, upload as an artifact, or broaden runner permissions. |
| `VPS_USER` | Platform Infra: `bootstrap-runner.yml` | SSH login user for runner bootstrap; currently stored under the secret context. |


## Quick index — GitHub Variables

| Name | Referenced in | Purpose / handling |
|---|---|---|
| `GHCR_USERNAME` | Platform Infra: `reconcile-vps.yml` | GHCR username used with the read token; falls back to `github.repository_owner` when unset. |
| `TELEGRAM_BOT_TOKEN` | TCE Dashboard: `wf-03-tce-production-deploy.yml` | Telegram notification bot token referenced through the **variable** context in TCE. Same name is referenced as a **secret** in Platform Infra; these are separate GitHub configuration scopes/types and must not be assumed to have the same value. Prefer secret storage for bot tokens and plan any migration deliberately. |
| `TELEGRAM_CHAT_ID` | TCE Dashboard: `wf-03-tce-production-deploy.yml`; Platform Infra: `reconcile-vps.yml` | Telegram destination/chat identifier referenced through the variable context; validate whether it is repository-, organization-, or environment-scoped. |

## GitHub-provided workflow token

| Name / expression | Referenced in | Purpose / handling |
|---|---|---|
| `GITHUB_TOKEN` / `github.token` | TCE Dashboard: `wf-00-tce-legacy-actions-cleanup.yml`, `wf-02-tce-prettier-format.yml`, `wf-03-tce-production-deploy.yml`, `wf-08b-tce-microfe-build-publish.yml`; Authentication: `release.yml`; Platform Infra: `reconcile-vps.yml` fallback, `gitops-image-promotion.yml`, `recover-stale-ops.yml` | GitHub Actions-generated workflow token. It is not a long-lived PAT to copy between repositories. Platform Infra GitOps uses Actions/Contents/Pull Requests permissions only; schedule recovery uses Actions write/Contents read only; GHCR reads are performed with `GHCR_READ_TOKEN`, not GITHUB_TOKEN package permissions. |

## Common runtime mapping

The following are the shared Auth runtime values referenced by Platform Infra's `provision-auth-runtime-secret.yml` and `reconcile-vps.yml`, and are provisioned into Kubernetes Secret `microfe-auth-secrets` in namespace `microfe-platform`:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET`
- `MFA_ENCRYPTION_KEY`

These are sourced from Platform Infra's protected GitHub Actions Environment named `production`. The workflow validates presence, passes values directly to the approved secret-provisioning command with shell tracing disabled, unsets the variables, and verifies the resulting Kubernetes Secret without displaying values. Keep this pattern; do not create committed Secret manifests.

## Naming inconsistencies and recommended follow-up

1. **Release handoff and automation tokens differ:** TCE and StockDividend use `PLATFORM_INFRA_TOKEN`; Media Generation and Authentication use repository-level `PLATFORM_INFRA_DISPATCH_TOKEN` secrets; Platform Infra GitOps promotion uses its workflow-scoped `GITHUB_TOKEN` with least-privilege Actions/Contents/Pull Requests permissions and an explicit exact-head `workflow_dispatch` validation. Media's dispatch verifier also reads Actions runs, so its token needs `Actions: read` in addition to dispatch permission. These names and roles do not imply that the repositories share a token value. Do not reuse any application handoff token as the Kubernetes GHCR pull credential.
2. **Telegram token storage differs:** TCE reads `TELEGRAM_BOT_TOKEN` via `vars`; Platform Infra reads the same key via `secrets`. Avoid placing a bot token in an unprotected variable; migrate through a carefully tested change if TCE still needs it.
3. **MFA key names differ by purpose:** `MFA_ENCRYPTION_KEY`, `MFA_ENCRYPTION_KEY_PROD`, and `MFA_ENCRYPTION_KEY_STG` are not interchangeable without verifying each workflow's environment/cluster mapping.
4. **Secret names do not prove configured existence:** this is a source-code inventory. The GitHub connector used for this audit cannot read secret values and this inventory does not claim to validate which keys are configured in repository, organization, or environment settings.
5. **Credential values stay out of Git:** store values only in GitHub Secrets/Environment Secrets or the appropriate secret manager. Never add values to this file, workflow outputs, issue comments, build artifacts, or plaintext manifests.
6. **Official references:** [GitHub Actions secret naming/scope](https://docs.github.com/en/actions/reference/security/secrets), [GitHub Actions variable naming](https://docs.github.com/en/actions/reference/workflows-and-actions/variables), and [GitHub secrets context including the automatic GITHUB_TOKEN](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#secrets-context).

## Workflow references

### TCE Dashboard

- `wf-00-tce-legacy-actions-cleanup.yml`
- `wf-01-tce-build-verify.yml`
- `wf-02-tce-backend-unit-test.yml`
- `wf-02-tce-prettier-format.yml`
- `wf-03-tce-production-deploy.yml`
- `wf-04-tce-k3s-cleanup.yml`
- `wf-06-tce-healthcheck.yml`
- `wf-07-tce-backup.yml`
- `wf-07-tce-integration-check.yml`
- `wf-08b-tce-microfe-build-publish.yml`
- `wf-09-nginx-readonly-audit.yml`
- `wf-09-tce-vps-safe-setup.yml`
- `wf-10-tce-k3s-bootstrap.yml`
- `wf-11-tce-mobile-landscape-viewport.yml`

### StockDividend

- `deploy.yml`
- `wf-platform-infra-release.yml`
- `run_scraper.yml`

### Authentication

- `ci.yml`
- `release.yml`
- `web-ci.yml`

### Platform Infra

- `bootstrap-runner.yml`
- `gitops-image-promotion.yml`
- `inspect-vps.yml`
- `keycloak-ci.yml`
- `provision-auth-runtime-secret.yml`
- `reconcile-observability.yml`
- `reconcile-vps.yml`
- `runtime-secret-readiness.yml`
- `smoke-production.yml`
- `staging-dry-run.yml`
- `validate-github-actions.yml`
- `validate-manifests.yml`
- `validate-metrics.yml`
- `validate-recovery-readiness.yml`
- `vps-image-cleanup.yml`

## Change policy

Update this inventory when a workflow adds, renames, removes, or changes the scope of a secret/variable reference. Re-audit actual workflow expressions rather than assuming a key still exists. Do not modify or rotate runtime credentials as part of updating this documentation.


## GHCR token is not a GitOps automation token

A successful `GHCR_READ_TOKEN` registry preflight verifies only GHCR authentication and package access. It does not grant repository or Actions permissions. Platform Infra GitOps promotion uses the workflow-scoped `GITHUB_TOKEN`; keep `GHCR_READ_TOKEN` read-only and never use it as a GitOps write fallback. See [credentials.md](credentials.md) for the scope matrix and exact-head validation flow.
