# Credentials and Token Scope Guide

Last reviewed: 2026-10-31

This file documents credential purpose and safe selection only. **Never store secret values, PATs, passwords, environment files, or token fragments in this repository.**

## Can `GHCR_READ_TOKEN` replace `PLATFORM_INFRA_AUTOMATION_TOKEN`?

**No. Keep them separate.**

- `GHCR_READ_TOKEN` is a registry credential used by `reconcile-vps.yml` to authenticate to GHCR and pull/read private container packages. Its documented minimum scope is `read:packages`, with package access to every production image and the correct `GHCR_USERNAME`.
- `PLATFORM_INFRA_AUTOMATION_TOKEN` is used by `gitops-image-promotion.yml` to create/update GitOps promotion commits or pull requests, inspect required checks, and squash-merge only a verified PR head. It requires repository permissions on `phanthienquoc/platform-infra`: `Contents: write`, `Pull requests: write`, `Checks: read`, and `Commit statuses: read`.
- Successful GHCR Registry V2 preflight proves registry/package access for the checked packages; it does **not** prove GitHub repository Contents, Pull Requests, Checks, or Commit Status permissions.
- Reusing a read-only package token for GitOps writes should fail due to insufficient scope and weakens separation of duties. Do not change the promotion workflow to use `GHCR_READ_TOKEN` as a fallback.
- Do not rotate or replace a working GHCR token merely to resolve promotion failures. The current deployment evidence shows GHCR access recovered while promotion stops at the missing `PLATFORM_INFRA_AUTOMATION_TOKEN` secret.

## Required configuration

Configure `PLATFORM_INFRA_AUTOMATION_TOKEN` as a protected secret in the `production` GitHub Environment of `phanthienquoc/platform-infra`. Use a dedicated fine-grained PAT scoped to that repository and the permissions listed above. Verify the secret exists in the correct Environment without exposing its value.

Keep these credentials distinct:
- `GHCR_READ_TOKEN`: registry read access only.
- `PLATFORM_INFRA_AUTOMATION_TOKEN`: GitOps promotion PR/write/check permissions.
- `PLATFORM_INFRA_TOKEN`: TCE/StockDividend release handoff; not a GHCR credential.
- `PLATFORM_INFRA_DISPATCH_TOKEN`: Media/Auth release handoff; not a GHCR credential.

## Verification checklist

1. Verify GHCR access using the existing registry preflight; never print the token.
2. Verify promotion token configuration in GitHub Environment settings; secret values are intentionally not readable through the GitHub connector.
3. Retry the promotion workflow only after the dedicated token is configured.
4. Verify the resulting PR's exact head SHA and required checks before squash merge.
5. Never paste credentials into issues, chat, logs, artifacts, or repository files.
