# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-10-30 (UTC)
Reference contract: [Generic Production Release Pattern (WF-03)](GENERIC-WF03-RELEASE-PATTERN.md)

## Target operating model

- **Application repositories** own source tests, build verification, immutable ARM64 GHCR images, and release dispatch only.
- **platform-infra** owns production Kustomize manifests, shared GHCR pull credentials, image validation/promotion, reconciliation, rollout health checks, and deployment notifications.
- Never let an application repository both deploy directly to the VPS and request GitOps promotion for the same production runtime.
- Production health is only PASS when current Kubernetes rollout and application health evidence is available.

## Repository readiness

| Repository | Role | Current evidence | Status | Next action |
|---|---|---|---|---|
| `phanthienquoc/TCE-dashboard` | Reference application | `wf-03-tce-production-deploy.yml` is manual-dispatch only; immutable `prod-v<semver>-<sha>` tags; native ARM64 build; platform-infra promotion | Reference; runtime still needs live verification | Keep WF-01/02 validation separate from WF-03 release; confirm current GHCR/GitOps/K3s state |
| `phanthienquoc/platform-infra` | Shared production deployment authority | Shared `ghcr-pull` contract merged in PR #817; canonical `GHCR_READ_TOKEN` promotion validation merged in PR #819 (master commit `92c17f4`). Live inspection at 2026-10-30T14:08Z shows GHCR 403s for MicroFE Shell/WS and StockDividend backend/admin; Keycloak is 0/1 and public OIDC discovery returns HTTP 503 with database pool checkout timeouts | Credential contract merged; production runtime is degraded and not healthy | Verify GHCR_READ_TOKEN has `read:packages` plus access to every private production package; verify scheduled reconciliation and image pulls; resolve Keycloak database connection checkout failures; rerun smoke and verify all rollouts before declaring healthy |
| `phanthienquoc/stockdividend` | Production application | PR #7 merged to `master` on 2026-10-30 (merge commit `735d5dd`); direct SSH/Docker Compose deployment removed and only backend/admin GitOps dispatch remains. Post-merge StockDividend CI passed, but image build `41068677403` failed because pip could not install quarantined PyPI package `vnstock`; downstream promotion `41068883593` was skipped. PR #8 now pins Vnstock 5.0.1 from its official package index and adds no-push image-build CI | GitOps-only change merged; scraper image publishing blocked; no new production promotion occurred | Verify PR #8's no-push container build and all checks, merge only when green, then verify post-merge image publication → promotion → rollout/health; investigate the separate scheduled scraper failures |
| `phanthienquoc/media-generation` | Production FE/BE application | Single `wf-03-media-production-deploy.yml`; native ARM64 builds, immutable `prod-v<semver>-<sha>` tag, platform-infra release path | Workflow exists; end-to-end runtime not verified in this review | Verify dispatch contract, GHCR tags/digests, paired FE/BE GitOps convergence, and K3s rollout |
| `phanthienquoc/phanthienquoc-authentication` | Production Auth service + web CI | `release.yml` is manual-dispatch only, builds ARM64 Auth image and dispatches `image-published`; `ci.yml` and path-filtered `web-ci.yml` cover validation | Workflow structure appears intentional; runtime not verified | Confirm image path/tag and protected dispatch token, then verify GitOps and live Auth health |

## Current runtime blockers (2026-10-30)

- **GHCR pulls:** the latest self-hosted VPS inspection reports `ImagePullBackOff` with HTTP 403 authorization failures for `ghcr.io/phanthienquoc/microfe-shell:0.1.0`, `microfe-ws:RELEASE_SHA`, and StockDividend backend/admin images. The code path reconciles the shared `ghcr-pull` secret, but actual token/package access still needs verification; do not place token values in logs or Git.
- **Keycloak/OIDC:** the production smoke run returned HTTP 503 for OIDC discovery. The VPS inspection shows Keycloak 0/1 with Supabase/PostgreSQL session-pool checkout timeouts (`ECHECKOUTTIMEOUT`) and a down cluster-health check. No database or credential mutation was performed in this pass.
- **StockDividend image build:** post-merge image publication failed because pip could not resolve the quarantined PyPI `vnstock` project. The follow-up is [StockDividend PR #8](https://github.com/phanthienquoc/stockdividend/pull/8); its CI builds the scraper image without publishing.

## Workflow inventory and disposition

Disposition meanings:
- **KEEP**: distinct CI, release, maintenance, security, or operational function.
- **CHANGE**: deployment authority or release contract must be aligned.
- **REVIEW**: potentially redundant or one-off; do not delete until current consumers and recent usage are verified.
- **REMOVE**: confirmed no-op/obsolete duplicate with no remaining consumer.

### TCE-dashboard

| Workflow | Disposition | Reason |
|---|---|---|
| `wf-01-tce-build-verify.yml` | KEEP | Build and production-config validation, not the production release |
| `wf-01p-tce-web-pr-build.yml` | KEEP | PR-scoped web build |
| `wf-02-tce-backend-unit-test.yml` | KEEP | Backend tests |
| `wf-02-tce-prettier-format.yml` | KEEP | Formatting checks |
| `wf-03-tce-production-deploy.yml` | KEEP | Canonical manual production release |
| `wf-04-tce-k3s-cleanup.yml` | KEEP | Cluster cleanup maintenance |
| `wf-06-tce-healthcheck.yml` | KEEP | Health checks |
| `wf-07-tce-backup.yml` | KEEP | Backup |
| `wf-07-tce-integration-check.yml` | KEEP | Integration checks; distinct from backup |
| `wf-08b-tce-microfe-build-publish.yml` | KEEP | MicroFE image publication |
| `wf-09-nginx-readonly-audit.yml` | KEEP | Read-only audit |
| `wf-09-tce-vps-safe-setup.yml` | KEEP | VPS setup |
| `wf-10-tce-k3s-bootstrap.yml` | KEEP | K3s bootstrap |
| `wf-11-tce-mobile-landscape-viewport.yml` | KEEP | UI/viewport validation |
| `wf-00-tce-legacy-actions-cleanup.yml` | REMOVE (PR #980) | Manual-only one-off utility that deletes historical non-WF workflow runs; not needed for CI/release/deployment and potentially destructive. PR #980 removes the workflow definition without deleting any existing run history. |

### StockDividend

| Workflow | Disposition | Reason |
|---|---|---|
| `.github/workflows/deploy.yml` | KEEP | PR #7 merged 2026-10-30; builds and publishes immutable full-SHA image tags without direct VPS deployment |
| `.github/workflows/wf-platform-infra-release.yml` | KEEP | PR #7 merged 2026-10-30; dispatches only supported backend/admin components using the full SHA from the successful build |
| `.github/workflows/run_scraper.yml` | KEEP | Scheduled/manual scraper execution is a separate task; no equivalent K3s scraper workload was found in the production Kustomize overlay |

### Media Generation

| Workflow | Disposition | Reason |
|---|---|---|
| `.github/workflows/wf-03-media-production-deploy.yml` | KEEP | Only listed workflow; owns FE/BE release and promotion |

### Authentication

| Workflow | Disposition | Reason |
|---|---|---|
| `.github/workflows/ci.yml` | KEEP | Backend/service validation |
| `.github/workflows/web-ci.yml` | KEEP | Path-filtered web validation |
| `.github/workflows/release.yml` | KEEP | Explicit manual Auth image publication and GitOps dispatch; release verification is a required safety gate |

### Platform Infra

| Workflow | Disposition | Reason |
|---|---|---|
| `bootstrap-runner.yml` | KEEP | Installs/updates allowlisted VPS helper |
| `gitops-image-promotion.yml` | KEEP | Central image validation and GitOps promotion |
| `reconcile-vps.yml` | KEEP | Production reconciliation |
| `inspect-vps.yml` | KEEP | VPS inspection |
| `smoke-production.yml`, `keycloak-auth-production-smoke.yml` | KEEP | Production smoke verification |
| `validate-github-actions.yml`, `validate-manifests.yml`, `validate-metrics.yml`, `validate-recovery-readiness.yml` | KEEP | Distinct validation gates |
| `runtime-secret-readiness.yml`, `provision-auth-runtime-secret.yml` | KEEP | Runtime secret readiness/provisioning |
| `configure-keycloak-no-email-registration.yml`, `configure-keycloak-resend-smtp.yml`, `provision-keycloak-tce-client.yml`, `verify-keycloak-tce-client.yml` | KEEP | Separate Keycloak configuration/verification operations |
| `reconcile-observability.yml`, `staging-dry-run.yml` | KEEP | Observability and staging verification |
| `vps-image-cleanup.yml` | KEEP | VPS disk/image maintenance |
| `mirror-locally-uncensored.yml` | REVIEW | Appears unrelated to application deployment; retain unless its owner confirms it is obsolete |
| Any other listed workflow | REVIEW | Inspect triggers and consumers before deletion; no other confirmed duplicate was established during this pass |

## Deployment invariants

1. Every production image tag referenced by a dispatch payload must be published by the same run.
2. A GitOps event must target an app/component accepted by `gitops-image-promotion.yml`.
3. Application repos must not mutate production directly over SSH when platform-infra owns the K3s workload.
4. Build/test workflows must not publish or deploy production images on ordinary PRs.
5. Keep credentials in GitHub Secrets/Environments or Kubernetes Secrets; never put values in logs, payloads, or manifests.
6. A workflow being present or a dispatch succeeding is not proof of production health; verify image pull, rollout, readiness, ingress and application health.

## Current actions

- [ ] Merge and validate StockDividend PR #7 after required checks pass.
- [ ] Verify the StockDividend immutable image tags exist in GHCR.
- [ ] Verify platform-infra promotion PRs update only supported Kustomize components.
- [ ] Verify StockDividend Deployment rollout and HTTP health on the live cluster.
- [ ] Verify Media FE/BE release pairing and rollout.
- [ ] Verify Auth image promotion and production smoke.
- [ ] Review any workflow marked REVIEW using recent run evidence and consumers before deleting it.
- [ ] Continue hourly tracking; do not alter TCE market-scan scheduling.
