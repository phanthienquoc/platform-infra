# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-10-30 16:07 UTC
Reference contract: [Generic Production Release Pattern (WF-03)](GENERIC-WF03-RELEASE-PATTERN.md)

## Target operating model

- **Application repositories** own source tests, build verification, immutable ARM64 GHCR images, and release dispatch only.
- **platform-infra** owns production Kustomize manifests, shared GHCR pull credentials, image validation/promotion, reconciliation, rollout health checks, and deployment notifications.
- Never let an application repository both deploy directly to the VPS and request GitOps promotion for the same production runtime.
- Production health is only PASS when current Kubernetes rollout and application health evidence is available.

## Repository readiness

| Repository | Role | Current evidence | Status | Next action |
|---|---|---|---|---|
| `phanthienquoc/TCE-dashboard` | Reference application | `wf-03-tce-production-deploy.yml` remains manual-dispatch only; PR #989 (`7af67b1`) merged a `refs/heads/master` release gate before notifications/builds; immutable `prod-v<semver>-<sha>` tags and platform-infra promotion remain | Release-ref contract fixed; runtime still needs live verification | Confirm current GHCR/GitOps/K3s state and fresh HTTP health evidence |
| `phanthienquoc/platform-infra` | Shared production deployment authority | Shared `ghcr-pull` contract (#817), canonical `GHCR_READ_TOKEN` validation (#819), fail-closed health gate (#823), preflight-before-secret ordering (#827, `f22b649`), and promotion Environment binding (PR #829, `482468f`) are merged. Operator reports secret configuration, and promotion logs confirm the secret is non-empty, but `docker manifest inspect` is denied for both Media frontend/backend packages in runs [41086645186](https://github.com/phanthienquoc/platform-infra/actions/runs/41086645186) and [41086648628](https://github.com/phanthienquoc/platform-infra/actions/runs/41086648628). Latest Keycloak reconcile [41074713911](https://github.com/phanthienquoc/platform-infra/actions/runs/41074713911) still timed out after 300 seconds with 0/1 updated replicas. | GHCR credential/package access is denied for Media images; Keycloak is not healthy | Replace/repair `GHCR_READ_TOKEN` with a credential that has `read:packages` and access to each required private package; check package access and SSO authorization. Then rerun promotion and a narrow app reconciliation. Investigate Keycloak readiness and Supabase pooler timeouts separately. |
| `phanthienquoc/stockdividend` | Production application | PR #7 removed direct SSH/Docker Compose deployment; PR #8 fixed the scraper image build. Image publication run [41072359809](https://github.com/phanthienquoc/stockdividend/actions/runs/41072359809) passed for backend/admin/scraper with full source-SHA tags. Promotion run [41073550431](https://github.com/phanthienquoc/stockdividend/actions/runs/41073550431) failed closed because `PLATFORM_INFRA_TOKEN` was empty. PR #9 (`42ed9ec`) and PR #10 (`08a4733`) are merged. PR #11 (`982657b`) is merged after all four exact-head CI jobs passed; it excludes workflow/docs-only pushes and gates manual publishing to master. The pre-guard workflow-only build [41086093700](https://github.com/phanthienquoc/stockdividend/actions/runs/41086093700) remains in flight. | GitOps promotion token remains blocked/unverified; pre-guard build outcome under review; live rollout unverified | Verify `PLATFORM_INFRA_TOKEN`, inspect the in-flight build/promotion outcome, then verify future workflow-only changes do not publish images. |
| `phanthienquoc/media-generation` | Production FE/BE application | PR #61 (`708f893`) merged a master-only release gate and push/PR CI; exact-head backend tests, typecheck and frontend/backend build passed. Workflow-only merge triggered release [41086293818](https://github.com/phanthienquoc/media-generation/actions/runs/41086293818); immutable frontend/backend images were published and dispatch accepted. Platform Infra promotion runs [41086645186](https://github.com/phanthienquoc/platform-infra/actions/runs/41086645186) and [41086648628](https://github.com/phanthienquoc/platform-infra/actions/runs/41086648628) both failed at GHCR manifest access (`Get https://ghcr.io/v2/: denied`) before GitOps mutation. PR #62 (`b445f71`) is merged after both exact-head CI runs passed; workflow/docs-only pushes are now excluded from automatic production release. | Images published, but promotion blocked by GHCR access denial; no GitOps rollout verified | Fix `GHCR_READ_TOKEN` package access, rerun the paired promotions, then verify GitOps, K3s rollout and HTTP health. |
| `phanthienquoc/phanthienquoc-authentication` | Production Auth service + web CI | `release.yml` is manual-dispatch only, builds ARM64 Auth image and dispatches `image-published`; `ci.yml` and path-filtered `web-ci.yml` cover validation | Workflow structure appears intentional; runtime not verified | Confirm image path/tag and protected dispatch token, then verify GitOps and live Auth health |

## Current runtime blockers (2026-10-30)

- **Workflow-only release side effects:** merge of StockDividend PR #10 triggered image build [41086093700](https://github.com/phanthienquoc/stockdividend/actions/runs/41086093700); merge of Media PR #61 triggered release [41086293818](https://github.com/phanthienquoc/media-generation/actions/runs/41086293818). Media images were published, but both Platform Infra component promotions failed GHCR manifest access before GitOps mutation. StockDividend's pre-guard build is still in flight. PR #11 and PR #62 are now merged with path exclusions. Confirm final StockDividend run outcome before treating runtime as unchanged.

- **GHCR pulls and Environment scope:** the prior VPS inspection reported `ImagePullBackOff`/HTTP 403 for MicroFE and StockDividend images; run [41071497800](https://github.com/phanthienquoc/platform-infra/actions/runs/41071497800) failed closed because `GHCR_READ_TOKEN` was unset at that time. After configuration, Media promotion jobs received a non-empty token but GHCR returned `denied` while inspecting both private Media images; this points to invalid token permissions, package access, or SSO authorization. PR #827 (`f22b649`) moved the read-only preflight before secret provisioning/mutation, and PR #829 (`482468f`) binds both GHCR-consuming promotion jobs to the protected `production` Environment. Repair token/package access, then rerun the paired promotions and a narrow app reconciliation. Never expose token values in logs or Git.
- **TCE/Auth public health:** scheduled TCE healthcheck run [41070484265](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41070484265) reported TCE web HTTP 200, but both Auth `/api/health` and `/api/ready` returned HTTP 503. The healthcheck is correctly failing; investigate the Auth service/DB readiness and require fresh HTTP 200 evidence before declaring the Auth lane healthy.
- **Keycloak/OIDC:** production smoke previously returned HTTP 503 for OIDC discovery. Latest Keycloak-only reconcile [41074713911](https://github.com/phanthienquoc/platform-infra/actions/runs/41074713911) provisioned the runtime Secret and applied unchanged resources, but `deployment/keycloak` stayed at 0/1 updated replicas for 300 seconds and the lane failed. Supavisor logs at 2026-10-30T14:13Z showed `ECHECKOUTTIMEOUT`/`ECHECKOUTFAILED` for `keycloak_runtime`; read-only Supabase diagnostics also timed out. Inspect pod events/readiness and database connectivity before another rollout; do not declare OIDC healthy without fresh HTTP 200.
- **Health gate false-green:** reconcile run `41062653406` returned success after affected pods were terminating and image pulls had failed. PR #823 (`357434d`) hardened the gate to reject empty active-pod sets and compare desired/ready/updated Deployment replicas. The latest reconciliation then failed earlier at GHCR token preflight, so the health gate has still not produced fresh post-fix runtime evidence.
- **StockDividend promotion:** image-publish run [41072359809](https://github.com/phanthienquoc/stockdividend/actions/runs/41072359809) succeeded. Promotion run [41073550431](https://github.com/phanthienquoc/stockdividend/actions/runs/41073550431) still fails visibly because `PLATFORM_INFRA_TOKEN` was empty; PR #9 (`42ed9ec`) made this fail closed, and PR #10 (`08a4733`) prevents non-master builds from reaching production promotion. Configure/verify this secret in the StockDividend repository, distinct from `GHCR_READ_TOKEN`, then rerun the failed promotion job.

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
| `wf-00-tce-legacy-actions-cleanup.yml` | REMOVE (merged PR #980, commit `07031dc`) | Manual-only one-off utility that deleted historical non-WF workflow runs; not needed for CI/release/deployment and potentially destructive. The workflow definition is removed; existing run history was not deleted. |

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
- [x] Merge platform-infra PR #827 after `validate-github-actions`, `validate-manifests` and Keycloak manifest/boundary CI passed (merge commit `f22b649`); GHCR preflight now precedes Auth runtime Secret provisioning.
- [ ] Repair `GHCR_READ_TOKEN` so it can read the private Media frontend/backend packages, then rerun promotion to prove GHCR access; follow with a narrow app reconciliation for remaining packages. Never expose its value.
- [ ] Configure/verify StockDividend repository Actions secret `PLATFORM_INFRA_TOKEN` with `Contents: write` access to `phanthienquoc/platform-infra`; never expose its value, then rerun failed promotion run `41073550431`.
- [x] Merge platform-infra PR #829 (`482468f`) binding both GHCR-consuming promotion jobs to the `production` Environment; exact-head PR checks and post-merge `validate-github-actions`/`validate-manifests` passed. GHCR runtime validation remains pending because the latest reconciliation targeted Keycloak.
- [ ] Verify the StockDividend immutable image tags exist in GHCR, then verify GitOps promotion, K3s rollout and HTTP health.
- [ ] Investigate Auth `/api/health` and `/api/ready` returning HTTP 503 in TCE healthcheck run `41070484265`; require fresh HTTP 200 evidence.
- [ ] Verify Media FE/BE release pairing and rollout.
- [ ] Verify Auth image promotion and production smoke after the Auth runtime blocker is resolved.
- [x] Merge StockDividend PR #10 (`08a4733`) after all four exact-head CI jobs passed; promotion now rejects successful builds not originating from `master`.
- [x] Merge TCE Dashboard PR #989 (`7af67b1`) after exact-head Prettier and backend unit checks passed; production release now requires `refs/heads/master`.
- [x] Merge Media PR #61 (`708f893`) after exact-head CI passed backend tests, typecheck, and frontend/backend build; it adds a master-only release gate and push/PR CI.
- [x] Merge StockDividend PR #11 (`982657b`) after all four exact-head CI jobs passed; workflow/docs-only pushes no longer trigger production image builds.
- [x] Merge Media PR #62 (`b445f71`) after both exact-head CI runs passed; workflow/docs-only pushes no longer trigger automatic production releases.
- [ ] Verify final outcome of pre-guard StockDividend run `41086093700` and confirm whether its promotion was accepted; Media promotion is blocked by GHCR access denial.
- [ ] Review any workflow marked REVIEW using recent run evidence and consumers before deleting it.
- [ ] Continue hourly tracking; do not alter TCE market-scan scheduling.
