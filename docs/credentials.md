# Credentials and Token Scope Guide

Last reviewed: 2026-11-01

This file documents credential purpose and safe selection only. **Never store secret values, PATs, passwords, environment files, or token fragments in this repository.**

## GitOps promotion and GHCR credentials are separate

- `GHCR_READ_TOKEN` is a registry credential used by `gitops-image-promotion.yml` and `reconcile-vps.yml` to authenticate to GHCR and pull/read private container packages. Its documented minimum scope is `read:packages`, with package access to every production image and the correct `GHCR_USERNAME`.
- Platform Infra GitOps promotion uses the workflow-scoped `GITHUB_TOKEN` with explicit `actions: write`, `contents: write`, and `pull-requests: write` permissions. It does **not** need `packages` permission: private registry reads use `GHCR_READ_TOKEN` through package-scoped Registry V2 preflight. It creates the promotion PR, explicitly dispatches `validate-manifests.yml` on the PR branch, waits for a successful run tied to the exact head SHA, rechecks the open PR/head/base, then squash-merges with an exact-head guard.
- The scheduled-ops recovery workflow uses its own workflow-scoped `GITHUB_TOKEN` with `actions: write` and `contents: read` only. It may dispatch the existing `reconcile-vps.yml` or read-only `inspect-vps.yml` after their latest master run exceeds the configured freshness budget; it never runs kubectl/SSH/Compose itself and does not grant package permissions.
- GitHub suppresses most workflow runs caused by a `GITHUB_TOKEN`-created PR. The explicit `workflow_dispatch` validation is therefore mandatory; never replace it with an assumption that a PR check will start automatically.
- `GHCR_READ_TOKEN` cannot replace `GITHUB_TOKEN`: the former grants package reads only, while the latter receives repository/action permissions from the workflow. Do not use the GHCR token as a GitOps write credential or add a PAT fallback.
- `PLATFORM_INFRA_AUTOMATION_TOKEN` is no longer referenced by the active promotion workflow. Do not configure a new PAT for this path; existing unused secrets need not be rotated or deleted by this change.
- `Platform-infra-token` is referenced by `.github/workflows/mirror-locally-uncensored.yml` to push refs/history to `phanthienquoc/locally-uncensored-private`. The latest scheduled run observed this secret resolving empty; configure it only with the target repository's required `Contents: write` access. Do not substitute `GHCR_READ_TOKEN` or an application release-handoff token without independently verifying its scope.

## Cross-repository application handoff credentials

Keep application dispatch credentials separate from platform-owned GHCR pull access:
- `PLATFORM_INFRA_TOKEN`: TCE Dashboard and StockDividend release handoff to Platform Infra; requires `Contents: write` on `phanthienquoc/platform-infra` for repository dispatch.
- `PLATFORM_INFRA_DISPATCH_TOKEN`: Media Generation and Authentication release handoff. Media also reads Platform Infra Actions runs to verify dispatch correlation, so its repository secret needs `Contents: write` and `Actions: read`; Authentication needs dispatch permission (`Contents: write`). The same secret name does not imply the repositories share a token value.

## Other production credentials

- `GHCR_USERNAME`: package owner/login paired with `GHCR_READ_TOKEN`; keep package visibility and access least-privileged.
- `RUNNER_REGISTRATION_PAT`: Platform Infra runner bootstrap only; use minimal runner-registration permissions and never store generated short-lived runner tokens.
- `KEYCLOAK_DB_PASSWORD`, `KEYCLOAK_DB_URL`, `KEYCLOAK_DB_USERNAME`, `KEYCLOAK_ADMIN_USERNAME`, and `KEYCLOAK_ADMIN_PASSWORD`: protected Keycloak runtime credentials; keep out of logs, artifacts, manifests, and Git.

## Verification checklist

1. Verify GHCR access using the existing package-scoped registry preflight; never print the token.
2. Verify the GitOps workflow's declared permissions and exact-head validation run; secret values are intentionally not readable through the GitHub connector.
3. Confirm each application repository's own dispatch credential is configured in its repository/environment scope before authorizing a release.
4. Verify the resulting GitOps PR head SHA, exact-head manifest validation, merge SHA, reconciliation, K3s rollout, and application health before reporting promotion complete.
5. Never paste credentials into issues, chat, logs, artifacts, or repository files.
