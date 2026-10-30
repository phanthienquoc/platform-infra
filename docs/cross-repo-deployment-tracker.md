# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-10-30 14:31 UTC
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
| `phanthienquoc/platform-infra` | Shared production deployment authority | Shared `ghcr-pull` contract (#817), canonical `GHCR_READ_TOKEN` promotion validation (#819), and fail-closed rollout health gate (#823) are merged. Latest `reconcile-vps` run [41071497800](https://github.com/phanthienquoc/platform-infra/actions/runs/41071497800) failed at 2026-10-30T14:27Z in GHCR pull-access preflight because `GHCR_READ_TOKEN` is empty; credential bootstrap, manifest apply and all app lanes were skipped. `validate-manifests` and workflow lint passed on master `a5bb9874a9333b8e52f0debf8c9d0b72d40f8c7b` | Fail-closed behavior confirmed; runtime still unverified/degraded, not healthy | Configure `GHCR_READ_TOKEN` in the production Environment with `read:packages` and access to every private package; then rerun reconciliation, verify the GHCR preflight and inspect fresh rollout/HTTP health evidence. Separately resolve Keycloak/Supabase pooler timeouts |
| `phanthienquoc/stockdividend` | Production application | PR #7 removed direct SSH/Docker Compose deployment; PR #8 fixed the scraper image build. Master image publish run [41069557885](https://github.com/phanthienquoc/stockdividend/actions/runs/41069557885) passed. Promotion run [41071385957](https://github.com/phanthienquoc/stockdividend/actions/runs/41071385957) misleadingly concluded success while skipping dispatch because `PLATFORM_INFRA_TOKEN` was absent. PR #9 was then squash-merged as `42ed9ec`; all four exact-head CI jobs passed and the release workflow now fails closed on missing token or non-SHA tag | Image build passed; GitOps promotion is blocked on secret configuration; live rollout unverified | Configure StockDividend Actions secret `PLATFORM_INFRA_TOKEN` with `Contents: write` on `phanthienquoc/platform-infra`; rerun/trigger promotion and verify dispatch, GitOps image tags, K3s rollout and HTTP health. Do not treat the prior promotion run as successful deployment |
| `phanthienquoc/media-generation` | Production FE/BE application | Single `wf-03-media-production-deploy.yml`; native ARM64 builds, immutable `prod-v<semver>-<sha>` tag, platform-infra release path | Workflow exists; end-to-end runtime not verified in this review | Verify dispatch contract, GHCR tags/digests, paired FE/BE GitOps convergence, and K3s rollout |
| `phanthienquoc/phanthienquoc-authentication` | Production Auth service + web CI | `release.yml` is manual-dispatch only, builds ARM64 Auth image and dispatches `image-published`; `ci.yml` and path-filtered `web-ci.yml` cover validation | Workflow structure appears intentional; runtime not verified | Confirm image path/tag and protected dispatch token, then verify GitOps and live Auth health |

## Current runtime blockers (2026-10-30)

- **GHCR pulls:** the latest self-hosted VPS inspection reported `ImagePullBackOff` with HTTP 403 authorization failures for `ghcr.io/phanthienquoc/microfe-shell:0.1.0`, `microfe-ws:RELEASE_SHA`, and StockDividend backend/admin images. The subsequent `reconcile-vps` run [41071497800](https://github.com/phanthienquoc/platform-infra/actions/runs/41071497800) failed closed in `validate-ghcr-pull-access.sh` because `GHCR_READ_TOKEN` was unset; no credential bootstrap, manifest apply or application deployment lane ran. Configure the production Environment secret with `read:packages` plus access to each private package, then retry. Never expose token values in logs or Git.
- **TCE/Auth public health:** scheduled TCE healthcheck run [41070484265](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41070484265) reported TCE web HTTP 200, but both Auth `/api/health` and `/api/ready` returned HTTP 503. The healthcheck is correctly failing; investigate the Auth service/DB readiness and require fresh HTTP 200 evidence before declaring the Auth lane healthy.
- **Keycloak/OIDC:** the production smoke run returned HTTP 503 for OIDC discovery. Supavisor logs at 2026-10-30T14:13Z show `ECHECKOUTTIMEOUT` and `ECHECKOUTFAILED` for `keycloak_runtime`, including upstream database authentication timeouts; read-only Supabase SQL/advisor diagnostics also timed out. No database or credential mutation was performed; pool/DB tuning remains unverified.
- **Health gate false-green:** reconcile run `41062653406` returned success after affected pods were terminating and image pulls had failed. PR #823 (`357434d`) hardened the gate to reject empty active-pod sets and compare desired/ready/updated Deployment replicas. The latest reconciliation then failed earlier at GHCR token preflight, so the health gate has still not produced fresh post-fix runtime evidence.
- **StockDividend promotion:** master image-publish run `41069557885` completed successfully. Promotion run `41071385957` exited success while logging that `PLATFORM_INFRA_TOKEN` was not configured and skipping GitOps dispatch. PR #9 (`42ed9ec`) is now merged with a fail-closed check, so a future missing-token promotion should fail visibly rather than green-skip. Configure the secret before retrying; rollout remains unverified.

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

- [x] Merge StockDividend PR #9 with squash after all four exact-head CI jobs passed (merge commit `42ed9ec`).
- [ ] Configure `GHCR_READ_TOKEN` in the platform-infra production Environment with `read:packages` and access to every private production package; never expose its value.
- [ ] Configure StockDividend Actions secret `PLATFORM_INFRA_TOKEN` with `Contents: write` access to `phanthienquoc/platform-infra`; never expose its value.
- [ ] Retry platform-infra GHCR preflight/reconciliation after secret configuration; verify no app lanes run until preflight passes.
- [ ] Verify the StockDividend immutable image tags exist in GHCR, then verify GitOps promotion, K3s rollout and HTTP health.
- [ ] Investigate Auth `/api/health` and `/api/ready` returning HTTP 503 in TCE healthcheck run `41070484265`; require fresh HTTP 200 evidence.
- [ ] Verify Media FE/BE release pairing and rollout.
- [ ] Verify Auth image promotion and production smoke after the Auth runtime blocker is resolved.
- [ ] Review any workflow marked REVIEW using recent run evidence and consumers before deleting it.
- [ ] Continue hourly tracking; do not alter TCE market-scan scheduling.
