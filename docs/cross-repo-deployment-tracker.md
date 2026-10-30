# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-10-31 (after PR #844 post-merge validation)
Reference contract: [Generic Production Release Pattern (WF-03)](GENERIC-WF03-RELEASE-PATTERN.md)

## Target operating model

- **Application repositories** own source tests, build verification, immutable ARM64 GHCR images, and release dispatch only.
- **platform-infra** owns production Kustomize manifests, shared GHCR pull credentials, image validation/promotion, reconciliation, rollout health checks, and deployment notifications.
- Never let an application repository both deploy directly to the VPS and request GitOps promotion for the same production runtime.
- Production health is only PASS when current Kubernetes rollout and application health evidence is available.

## Repository readiness

| Repository | Role | Current evidence | Status | Next action |
|---|---|---|---|---|
| `phanthienquoc/TCE-dashboard` | Reference application | `wf-03-tce-production-deploy.yml` remains manual-dispatch only; PR #989 (`7af67b1`) merged a `refs/heads/master` release gate before notifications/builds; immutable `prod-v<semver>-<sha>` tags and platform-infra promotion remain. Open PR #928 has passing head checks but is held pending authoritative verification of Supabase GitHub integration side effects and migration provenance | Release-ref contract fixed; runtime still needs live verification | Confirm current GHCR/GitOps/K3s state and fresh HTTP health evidence |
| `phanthienquoc/platform-infra` | Shared production deployment authority | Shared `ghcr-pull` contract (#817), canonical `GHCR_READ_TOKEN` validation (#819), fail-closed health gate (#823), preflight ordering (#827), promotion Environment binding (#829), GHCR diagnostics (#834), package-scoped Registry V2 probe (#839, `52c8de0`), reconciliation path coverage (#842, `1b93c98`), and hosted offline manifest/Keycloak validation (#844, merge `c04f577`) are merged. PR #844 exact-head `validate`, `lint`, and Keycloak boundary checks passed; post-merge runs [validate #41128324100](https://github.com/phanthienquoc/platform-infra/actions/runs/41128324100), [lint #41128323776](https://github.com/phanthienquoc/platform-infra/actions/runs/41128323776), and [Keycloak boundary #41128323812](https://github.com/phanthienquoc/platform-infra/actions/runs/41128323812) also passed. The 2026-10-30T20:49:38Z VPS snapshot confirms runner services active and node Ready, but shows Media backend 0/1, Keycloak/Auth 0/1, StockDividend admin/backend image pull 403, and MicroFE Shell/WS image tags returning NotFound. Latest package preflight [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) can read seven packages but gets HTTP 403 for both StockDividend packages and failed before cluster mutation. | CI validation is now off the production runner; runtime remains unhealthy and promotion is blocked by package access and missing image tags | Grant the configured GHCR PAT owner read access to `stockdividend/admin` and `/backend`; verify/publish valid immutable MicroFE Shell/WS images before changing their manifest tags; configure StockDividend `PLATFORM_INFRA_TOKEN`; then run package preflight, promotion, reconciliation, and fresh rollout/HTTP health checks. Investigate Keycloak/Supavisor timeout separately. |
| `phanthienquoc/stockdividend` | Production application | PR #7 removed direct SSH/Docker Compose deployment; PR #8 fixed scraper image build. Image publication [41072359809](https://github.com/phanthienquoc/stockdividend/actions/runs/41072359809) passed for backend/admin/scraper with full source-SHA tags. PR #9 (`42ed9ec`), #10 (`08a4733`) and #11 (`982657b`) are merged; #11 excludes workflow/docs-only pushes and gates manual publishing to master. Promotion [41087133466](https://github.com/phanthienquoc/stockdividend/actions/runs/41087133466) failed closed because `PLATFORM_INFRA_TOKEN` was empty. Latest central preflight [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) also denied package reads for StockDividend admin and backend (HTTP 403). | Image publication passed; cross-repo handoff token missing and GHCR package access denied; no promotion/rollout verified | Configure repository-level `PLATFORM_INFRA_TOKEN` with `Contents: write` on `phanthienquoc/platform-infra`; grant the GHCR PAT owner read access to both StockDividend packages; rerun handoff and verify GitOps/K3s/HTTP health. |
| `phanthienquoc/media-generation` | Production FE/BE application | PR #61 (`708f893`) merged master-only release gate and CI. Release [41086293818](https://github.com/phanthienquoc/media-generation/actions/runs/41086293818) published immutable `prod-v0.3.0-708f893` images from `708f89331f144572cc97c561fc6b44aa25827453`: frontend digest `sha256:f3fdaabee9a07b9e6952827fcb8f5101a42387caecda2d67f68e4e796787b2ed`, backend digest `sha256:a1c83be171093bcdafaf414a8eb2d227f87e260f19b043ad9d5119cfcaaf4c0e`. Earlier promotions [41086645186](https://github.com/phanthienquoc/platform-infra/actions/runs/41086645186) and [41086648628](https://github.com/phanthienquoc/platform-infra/actions/runs/41086648628) failed before GitOps mutation. New package-level preflight in [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) confirms both Media packages are readable with the configured token, but the global reconciliation remains blocked by StockDividend package permissions. PR #62 (`b445f71`) excludes workflow/docs-only releases. | Immutable images published and package access verified; no new promotion/rollout verified | After repairing the two StockDividend package permissions, rerun promotion/reconciliation using the existing Media digests, then verify rollout and HTTP health. |
| `phanthienquoc/phanthienquoc-authentication` | Production Auth service + web CI | `release.yml` is manual-dispatch only, builds ARM64 Auth image and dispatches `image-published`; `ci.yml` and path-filtered `web-ci.yml` cover validation. Open PRs #75 and #76 have passing `validate` checks on their current heads but remain unmerged because the Supabase GitHub integration has `Deploy to production` enabled and migration drift remains unresolved | Workflow structure appears intentional; runtime not verified | Confirm image path/tag and protected dispatch token, then verify GitOps and live Auth health |

## Current runtime blockers (2026-10-31)

- **Workflow-only release side effects:** merge of StockDividend PR #10 triggered image build [41086093700](https://github.com/phanthienquoc/stockdividend/actions/runs/41086093700), which succeeded; its promotion [41087133466](https://github.com/phanthienquoc/stockdividend/actions/runs/41087133466) failed because `PLATFORM_INFRA_TOKEN` was empty. Merge of Media PR #61 triggered release [41086293818](https://github.com/phanthienquoc/media-generation/actions/runs/41086293818); immutable images were published but both component promotions failed GHCR manifest access before GitOps mutation. PR #11 and PR #62 are now merged with path exclusions, preventing recurrence. Neither run has evidence of a GitOps rollout.

- **Latest read-only K3s evidence:** [debug/vps-latest.md](https://github.com/phanthienquoc/platform-infra/blob/master/debug/vps-latest.md) was generated at `2026-10-30T20:49:38Z`. Node `tce-k3s-01` was `Ready`, disk pressure normal (55%), and both GitHub runner services were active/enabled; this proves service state, not that every queued workflow had been claimed. TCE frontend/service and Media frontend were 1/1, while Media backend, Keycloak, and MicroFE Auth were 0/1. MicroFE Shell (`0.1.0`) and WS (`RELEASE_SHA`) image references returned registry `NotFound`; StockDividend admin/backend image pulls returned HTTP 403. GitOps drift was reported clean, but this is not evidence that application health is good. The latest central reconcile [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) failed at package preflight before changing cluster pull credentials or applying manifests. No fresh post-promotion rollout or HTTP health verification is evidenced; do not mark production healthy.
- **GHCR pulls and Environment scope:** the earlier Media promotions [41086645186](https://github.com/phanthienquoc/platform-infra/actions/runs/41086645186) and [41086648628](https://github.com/phanthienquoc/platform-infra/actions/runs/41086648628) failed before GitOps mutation. PR #827 (`f22b649`) moved preflight before secret provisioning/mutation; PR #829 (`482468f`) binds GHCR-consuming jobs to protected Environment `production`; PR #834 (`ea34644`) improved diagnostics; PR #839 (`52c8de0`) added a package-scoped Registry V2 `tags/list` probe. The latest production preflight [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) proves the configured token can read seven packages (Auth, Media FE/BE, MicroFE Shell/WS, and TCE service/web) but cannot read `ghcr.io/phanthienquoc/stockdividend/admin` or `/backend` (HTTP 403). This is a package-level permission gap, not a blanket GHCR outage. Grant the PAT owner access to both private StockDividend packages; retain fail-closed behavior until all required package probes pass. Never expose token values.
- **TCE/Auth public health:** the TCE healthcheck job [41070484265](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41070484265/job/124199238643) recorded TCE web HTTP 200 but Auth `/api/health` and `/api/ready` HTTP 503 at `2026-10-30T17:02Z`. The newer VPS snapshot at `18:45:15Z` independently shows both `sso.mrcute.space/realms/master/.well-known/openid-configuration` and `/realms/mrcute/.well-known/openid-configuration` returning HTTP 503. Require fresh HTTP 200 evidence for all relevant endpoints before marking Auth/OIDC healthy.
- **Keycloak/OIDC and Supavisor:** Keycloak-only reconcile [41074713911](https://github.com/phanthienquoc/platform-infra/actions/runs/41074713911) previously timed out with 0/1 updated replicas. A read-only Supabase log query for `2026-10-30T13:00Z`–`17:03Z` found 16,830 Supavisor errors for `keycloak_runtime`, including 3,851 authentication timeouts, 3,820 checkout timeouts, and 4,884 checkout failures. The fresh `18:43`–`18:45Z` pod logs continue to show `FATAL: Failed to connect to database: {:error, :timeout}` and health-check executor queue exhaustion; both OIDC probes remain HTTP 503. Root cause is still unconfirmed; inspect pooler/database telemetry and Keycloak JDBC URL/port/connection mode before production changes. Do not rotate credentials or rerun a Keycloak rollout blindly.
- **Health gate false-green:** reconcile run `41062653406` returned success after affected pods were terminating and image pulls had failed. PR #823 (`357434d`) hardened the gate to reject empty active-pod sets and compare desired/ready/updated Deployment replicas. The latest reconciliation then failed earlier at GHCR token preflight, so the health gate has still not produced fresh post-fix runtime evidence.
- **StockDividend promotion:** image publication [41072359809](https://github.com/phanthienquoc/stockdividend/actions/runs/41072359809) succeeded. Promotion [41087133466](https://github.com/phanthienquoc/stockdividend/actions/runs/41087133466) failed because repository-level `PLATFORM_INFRA_TOKEN` was empty, so no `repository_dispatch` was sent. The central package probe also returned HTTP 403 for StockDividend admin/backend. These are independent blockers: configure `PLATFORM_INFRA_TOKEN` with `Contents: write` on `phanthienquoc/platform-infra` and grant the configured GHCR PAT owner read access to both private packages; rerun promotion only after both are addressed.

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

- [ ] Make GHCR preflight global before reconciling the shared pull Secret: `reconcile-vps.yml` bootstraps `ghcr-pull` across production namespaces for any non-Keycloak target, so a target-scoped check could pass for MicroFE while StockDividend admin/backend still return 403 and then rotate the shared credential anyway. Require `TARGET_APP=all` for the preflight; keep targeted rollout lanes independent after the global credential-safety gate.

- [ ] Fix MicroFE promotion verification end to end: TCE workflow run [41129701152](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41129701152) published Shell digest `sha256:518c5a1d558b57fe2d228c0abf1d5facab16d92911353c5da83d66ad4325a338` and WS digest `sha256:6cf4551554a67157363f9be07a17ecacc48f18d4b3babdbde4354682ae9d3250` for source commit `8aa31375680430e02e2a6450012c5476bfe07c0e`. Central promotion [41129871311](https://github.com/phanthienquoc/platform-infra/actions/runs/41129871311) passed scoped package `tags/list` checks but failed at Docker registry-wide `/v2/` login with `denied`; no GitOps mutation occurred. TCE verification [41129701152](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41129701152) also failed to detect the central run because it matched `.name == "GitOps Image Promotion"` exactly while release-correlated run names include a suffix. This PR replaces Docker login/manifest-inspect with exact package-scoped `manifests/<tag-or-digest>` probes, exposes a release fallback in the run name, and validates `release == microfe-<source SHA prefix>`. TCE follow-up [PR #1002](https://github.com/phanthienquoc/TCE-dashboard/pull/1002) is open to send that release label, validate the payload before dispatch, and correlate the central run by release before promotion can be observed end to end.

- [x] Merge StockDividend PR #9 with squash after all four exact-head CI jobs passed (merge commit `42ed9ec`).
- [x] Merge platform-infra PR #827 after `validate-github-actions`, `validate-manifests` and Keycloak manifest/boundary CI passed (merge commit `f22b649`); GHCR preflight now precedes Auth runtime Secret provisioning.
- [ ] Repair GHCR package permissions: the latest package-level probe in [reconcile run 41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) passed for seven production images but returned HTTP 403 for `stockdividend/admin` and `stockdividend/backend`. Grant the configured PAT owner read access to those two packages, then rerun preflight; never expose the token.
- [x] Merge platform-infra PR #834 (`ea34644`) adding package-scope GHCR preflight before Docker login, clearer fail-closed diagnostics, credential guidance, and a regression contract; exact-head and post-merge `validate-github-actions`/`validate-manifests` passed. Runtime credential access remains unverified until the preflight/promotion is rerun after the secret is repaired.
- [ ] Configure/verify the **repository-level Actions secret** `PLATFORM_INFRA_TOKEN` in StockDividend (`wf-platform-infra-release.yml` does not bind an Environment), with `Contents: write` access to `phanthienquoc/platform-infra`; rerun promotion `41087133466` only after the secret is available.
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
- [x] Verify StockDividend image publication completed; promotion run `41087133466` attempt 2 (18:13 UTC) again showed an empty `PLATFORM_INFRA_TOKEN`, so no `repository_dispatch` was sent and no GitOps rollout was triggered.
- [ ] Add/verify StockDividend repository-level `PLATFORM_INFRA_TOKEN` (`Contents: write` on `phanthienquoc/platform-infra`) and fix GHCR read access for the private StockDividend admin/backend packages; these are separate blockers.
- [x] Harden automatic GitOps promotion merges: manual dispatch is master-only, missing required checks fail closed, both promotion paths re-check the exact PR head, and squash merge uses `--match-head-commit`; failed merge no longer updates the branch and retries without revalidation.
- [x] Merge platform-infra PR #839 (`52c8de0`) after exact-head `validate` and `lint` passed; package-level Registry V2 read verification is active. The post-merge reconcile [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) ran and failed closed on StockDividend package 403s; post-merge GitHub Actions and manifest validations [41111284192](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284192) and [41111284231](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284231) passed.
- [x] Merge platform-infra PR #842 (`1b93c98`) after exact-head `validate`, Keycloak manifest/boundary, and `lint` checks passed; push reconciliation now watches all production manifest subtrees and preserves `workflow_dispatch`, `repository_dispatch`, and the 15-minute schedule. Post-merge validation for `1b93c98` is queued as of 2026-10-31 20:06 UTC.
- [x] Merge platform-infra PR #844 (`c04f577`) after exact-head `validate`, `lint`, and Keycloak manifest/boundary checks passed; offline validation now runs on `ubuntu-latest`, with pinned `kubectl` v1.36.3 checksum verification and explicit PyYAML installation. Post-merge validation on `c04f577` passed: [validate #41128324100](https://github.com/phanthienquoc/platform-infra/actions/runs/41128324100), [lint #41128323776](https://github.com/phanthienquoc/platform-infra/actions/runs/41128323776), and [Keycloak boundary #41128323812](https://github.com/phanthienquoc/platform-infra/actions/runs/41128323812).
- [ ] Resolve MicroFE Shell/WS image references before rollout: current manifest-resolved tags `0.1.0` and `RELEASE_SHA` returned registry `NotFound` in the latest VPS snapshot. Identify the publishing source and a verified immutable image digest; do not replace tags with guesses.
- [ ] Review any workflow marked REVIEW using recent run evidence and consumers before deleting it.
- [ ] Continue hourly tracking; do not alter TCE market-scan scheduling.
