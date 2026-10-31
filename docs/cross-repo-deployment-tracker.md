# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-10-31 (StockDividend PR #13 merged with exact-head CI green; GHCR preflight retry #41147425844 attempt 2 now reaches package probes but receives HTTP 403 for all nine images; Auth HTTP 503 remains confirmed)
Reference contract: [Generic Production Release Pattern (WF-03)](GENERIC-WF03-RELEASE-PATTERN.md)

## Target operating model

- **Application repositories** own source tests, build verification, immutable ARM64 GHCR images, and release dispatch only.
- **platform-infra** owns production Kustomize manifests, shared GHCR pull credentials, image validation/promotion, reconciliation, rollout health checks, and deployment notifications.
- Never let an application repository both deploy directly to the VPS and request GitOps promotion for the same production runtime.
- Production health is only PASS when current Kubernetes rollout and application health evidence is available.

## Repository readiness

| Repository | Role | Current evidence | Status | Next action |
|---|---|---|---|---|
| `phanthienquoc/TCE-dashboard` | Reference application | PR #1002 (`4fbce98`) merged release-label payload validation and run correlation. Production run [41131346295](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41131346295) published three immutable images; retry attempt 2 detected central promotion [41132410638](https://github.com/phanthienquoc/platform-infra/actions/runs/41132410638), where exact Shell/WS manifest checks passed but the promotion stopped because `PLATFORM_INFRA_AUTOMATION_TOKEN` was empty. | Release payload and image validation pass; promotion handoff is fail-closed on missing Platform Infra automation token | Configure the Platform Infra `production` Environment token and restore StockDividend package access before rerunning TCE's verification job with the existing artifacts. Preserve market-scan schedule. |
| `phanthienquoc/platform-infra` | Shared production deployment authority | PR #854 (`0b08765`) pinned and checksum-verified kubectl v1.36.3; PR #858 (`e57d527`) hardened GHCR token parsing; PR #860 (`bf5b860`) refreshed runtime evidence. Post-merge reconciliation [#41147425844](https://github.com/phanthienquoc/platform-infra/actions/runs/41147425844) attempt 2 passed token-format validation but received HTTP 403 from the GHCR token endpoint for all nine production images (Auth, Media FE/BE, MicroFE Shell/WS, StockDividend Admin/Backend, TCE Service/Web). No cluster credential mutation or rollout occurred. `PLATFORM_INFRA_AUTOMATION_TOKEN` was empty in promotion #41132410638. | Validation CI passes; shared registry credential/identity is rejected for every package, promotion token and Auth health remain blockers | Verify `GHCR_USERNAME` matches the classic PAT owner; replace `GHCR_READ_TOKEN` with the intended valid classic PAT with `read:packages`, package access and required SSO authorization. Then rerun the fail-closed preflight before any reconciliation. Configure promotion automation token and verify fresh K3s/HTTP health. |
| `phanthienquoc/stockdividend` | Production application | PR #12 (`2b0883e`) added the fail-closed `PLATFORM_INFRA_TOKEN` preflight. PR #13 (`0b0c6bde`) is now squash-merged after all five exact-head checks passed, adding an explicit `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true` gate for production image publication and downstream promotion; CI/build verification remains enabled. Latest central GHCR probe [#41147425844](https://github.com/phanthienquoc/platform-infra/actions/runs/41147425844) returned 403 for both StockDividend packages as well as all other production images. The connector cannot read the current repository variable value or secret contents. | Release path is guarded by explicit opt-in; registry access remains blocked | Verify the release-enable repository variable is not set to `true` while credentials are unresolved. Configure repository-level `PLATFORM_INFRA_TOKEN` with `Contents: write` on Platform Infra, restore valid shared GHCR pull access, and only then re-enable production release. |
| `phanthienquoc/media-generation` | Production FE/BE application | PR #61 (`708f893`) merged master-only release gate and CI. Release [41086293818](https://github.com/phanthienquoc/media-generation/actions/runs/41086293818) published immutable `prod-v0.3.0-708f893` images from `708f89331f144572cc97c561fc6b44aa25827453`: frontend digest `sha256:f3fdaabee9a07b9e6952827fcb8f5101a42387caecda2d67f68e4e796787b2ed`, backend digest `sha256:a1c83be171093bcdafaf414a8eb2d227f87e260f19b043ad9d5119cfcaaf4c0e`. Earlier promotions [41086645186](https://github.com/phanthienquoc/platform-infra/actions/runs/41086645186) and [41086648628](https://github.com/phanthienquoc/platform-infra/actions/runs/41086648628) failed before GitOps mutation. New package-level preflight in [41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) confirms both Media packages are readable with the configured token, but the global reconciliation remains blocked by StockDividend package permissions. PR #62 (`b445f71`) excludes workflow/docs-only releases. | Immutable images published and package access verified; no new promotion/rollout verified | After repairing the two StockDividend package permissions, rerun promotion/reconciliation using the existing Media digests, then verify rollout and HTTP health. |
| `phanthienquoc/phanthienquoc-authentication` | Production Auth service + web CI | `release.yml` is manual-dispatch only, builds ARM64 Auth image and dispatches `image-published`; `ci.yml` and path-filtered `web-ci.yml` cover validation. Open PRs #75 and #76 have passing `validate` checks on their current heads but remain unmerged because the Supabase GitHub integration has `Deploy to production` enabled and migration drift remains unresolved | Workflow structure appears intentional; runtime not verified | Confirm image path/tag and protected dispatch token, then verify GitOps and live Auth health |

## Current runtime blockers (2026-10-31)

- **Latest MicroFE release attempt:** TCE production run [41131346295](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41131346295) published immutable digests for source `4fbce9880a5ce11ea408ffe5c0fca4acb4b2da6d`. Retry attempt 2 triggered central promotion [41132410638](https://github.com/phanthienquoc/platform-infra/actions/runs/41132410638); scoped package access and exact Shell/WS manifests passed, then the `Require GitOps PR automation token` step failed because `PLATFORM_INFRA_AUTOMATION_TOKEN` was empty. No promotion PR was created in that attempt; stale PR [#850](https://github.com/phanthienquoc/platform-infra/pull/850) remains closed without merge. No GitOps manifest merge, reconciliation, or K3s rollout occurred.

- **Workflow-only release side effects:** merge of StockDividend PR #10 triggered image build [41086093700](https://github.com/phanthienquoc/stockdividend/actions/runs/41086093700), which succeeded; its promotion [41087133466](https://github.com/phanthienquoc/stockdividend/actions/runs/41087133466) failed because `PLATFORM_INFRA_TOKEN` was empty. Merge of Media PR #61 triggered release [41086293818](https://github.com/phanthienquoc/media-generation/actions/runs/41086293818); immutable images were published but both component promotions failed GHCR manifest access before GitOps mutation. PR #11 and PR #62 are now merged with path exclusions, preventing recurrence. Neither run has evidence of a GitOps rollout.

- **Latest read-only K3s evidence:** [debug/vps-latest.md](https://github.com/phanthienquoc/platform-infra/blob/master/debug/vps-latest.md) was refreshed by merged inspection PR [#859](https://github.com/phanthienquoc/platform-infra/pull/859) at `2026-10-30T23:06:32Z` (2026-10-31 06:06:32 Vietnam time). Node `tce-k3s-01` was Ready, disk pressure normal (55%), and both runner services were active; this proves service state, not that every queued workflow ran. TCE frontend/service and Media frontend were 1/1. Media backend, Keycloak, and MicroFE Auth were 0/1. MicroFE Shell (`0.1.0`) and WS (`RELEASE_SHA`) references returned registry NotFound; StockDividend admin/backend image pulls returned HTTP 403. The Keycloak log now explicitly shows Supabase/Supavisor circuit-breaker errors `ECIRCUITBREAKER: too many authentication failures`, followed by `EAUTHQUERY: connection to database not available`. Treat this as a credential/authentication-path blocker requiring verification of the protected Keycloak DB username/password and pooler target—not as proof that a password should be changed blindly. GitOps drift being clean does not imply application health. No newer post-promotion rollout or HTTP health verification is evidenced; production remains NOT HEALTHY/UNVERIFIED.

- **GHCR pulls and Environment scope:** PR #827 (`f22b649`) moved preflight before secret provisioning/mutation; PR #829 (`482468f`) binds GHCR-consuming jobs to protected Environment `production`; PR #834 (`ea34644`) improved diagnostics; PR #839 (`52c8de0`) added a package-scoped Registry V2 `tags/list` probe; PR #858 (`e57d527`) now rejects malformed copied token values. The post-merge reconcile [#41147425844](https://github.com/phanthienquoc/platform-infra/actions/runs/41147425844) failed before any package probe with `GHCR_READ_TOKEN contains embedded whitespace or quotes`. Therefore the earlier result from [#41140628682](https://github.com/phanthienquoc/platform-infra/actions/runs/41140628682)—seven packages readable and StockDividend admin/backend HTTP 403—remains useful historical evidence but is not a fresh result under the current token parser. First re-save the secret as the raw token only, without wrapping quotes or any line breaks, then rerun preflight. If the two StockDividend packages still return 403, grant the PAT owner read access to both private packages. Keep the workflow fail-closed and never expose token values.
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
| `wf-08b-tce-microfe-build-publish.yml` | KEEP | Shell/WS immutable image publication is still required. The workflow also builds `microfe-auth`, but production Kustomize deploys the canonical `auth-service/auth` image and the shared promoter does not apply `auth_digest`; audit the legacy Auth subjob/payload separately before removing it. |
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

- [x] Merge Platform Infra PR #849 (`f64c180`) to require `TARGET_APP=all` before reconciling shared `ghcr-pull`; exact-head `validate`, `lint`, and Keycloak boundary checks passed, and all three post-merge validations passed. Targeted rollout lanes remain independent after this global credential-safety gate.

- [x] Merge Platform Infra PR #848 (`9941591`) to replace Docker registry-wide login with exact package-scoped `manifests/<tag-or-digest>` probes, validate the MicroFE release label against the source SHA, and provide a non-empty run-name fallback; exact-head checks and post-merge `validate`/`lint` passed.
- [x] Merge TCE PR #1002 (`4fbce98`) to send and validate `release=microfe-<7-char SHA>` and correlate central promotion by release label. Production run [41131346295](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41131346295) published three immutable images; retry [41132410638](https://github.com/phanthienquoc/platform-infra/actions/runs/41132410638) then failed closed because `PLATFORM_INFRA_AUTOMATION_TOKEN` was empty. No promotion PR was created and no GitOps merge or K3s reconciliation occurred.
- [x] Merge Platform Infra PR #851 (`f7eb2f7`) to use `PLATFORM_INFRA_AUTOMATION_TOKEN` for promotion PR creation, check inspection, and verified merge; post-merge validation passed.
- [ ] Configure `PLATFORM_INFRA_AUTOMATION_TOKEN` in the Platform Infra `production` Environment with `Contents: write`, `Pull requests: write`, `Checks: read`, and `Commit statuses: read`. Latest retry [#41132410638](https://github.com/phanthienquoc/platform-infra/actions/runs/41132410638) confirms it is empty. After setting it and fixing the StockDividend package 403s, rerun the failed TCE job [124326296630](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41131346295); this reuses published image artifacts rather than rebuilding.

- [x] Merge StockDividend PR #9 with squash after all four exact-head CI jobs passed (merge commit `42ed9ec`).
- [x] Merge platform-infra PR #827 after `validate-github-actions`, `validate-manifests` and Keycloak manifest/boundary CI passed (merge commit `f22b649`); GHCR preflight now precedes Auth runtime Secret provisioning.
- [ ] Repair GHCR package permissions: the latest package-level probe in [reconcile run 41111284264](https://github.com/phanthienquoc/platform-infra/actions/runs/41111284264) passed for seven production images but returned HTTP 403 for `stockdividend/admin` and `stockdividend/backend`. Grant the configured PAT owner read access to those two packages, then rerun preflight; never expose the token.
- [x] Merge platform-infra PR #834 (`ea34644`) adding package-scope GHCR preflight before Docker login, clearer fail-closed diagnostics, credential guidance, and a regression contract; exact-head and post-merge `validate-github-actions`/`validate-manifests` passed. Runtime credential access remains unverified until the preflight/promotion is rerun after the secret is repaired.
- [x] Merge StockDividend PR #12 (`2b0883e`) to preflight `PLATFORM_INFRA_TOKEN` and verify Platform Infra repository access before image publication; all four exact-head CI checks passed. The merge changed only `.github/**`, so it did not trigger a production image build.
- [ ] Configure/verify the **repository-level Actions secret** `PLATFORM_INFRA_TOKEN` in StockDividend (`wf-platform-infra-release.yml` does not bind an Environment), with `Contents: write` access to `phanthienquoc/platform-infra`; the last release run [41087133466](https://github.com/phanthienquoc/stockdividend/actions/runs/41087133466) observed an empty token. No newer release run has verified the secret.
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
- [x] Merge Platform Infra PR #854 (`0b08765`) to install checksum-verified kubectl v1.36.3 before MicroFE Kustomize rendering and enforce the dependency in `validate-workflow-contracts.py`. Exact-head checks and post-merge validation passed: [validate #41135749415](https://github.com/phanthienquoc/platform-infra/actions/runs/41135749415), [lint #41135749561](https://github.com/phanthienquoc/platform-infra/actions/runs/41135749561). No production mutation occurred; credential blockers remain.
- [ ] Coordinate a legacy MicroFE Auth publication cleanup across TCE and Platform Infra: TCE `wf-08b` still builds/publishes `microfe-auth` and sends `auth_digest`, while the production Deployment uses `ghcr.io/phanthienquoc/auth-service/auth:<immutable-tag>` and the shared promoter only validates the legacy digest format. Keep this workflow for Shell/WS; remove only the unused Auth image build/payload after updating both sides and their contract tests. No removal is made by this tracker-only change.
- [ ] Resolve MicroFE Shell/WS image references before rollout: current manifest-resolved tags `0.1.0` and `RELEASE_SHA` returned registry `NotFound` in the latest VPS snapshot. Identify the publishing source and a verified immutable image digest; do not replace tags with guesses.
- [ ] Review any workflow marked REVIEW using recent run evidence and consumers before deleting it.
- [ ] Continue hourly tracking; do not alter TCE market-scan scheduling.

- [x] Merge Platform Infra PR #857 (`9785b9e`) to require a successful shared preflight and an explicit `true`/`false` drift output before the final reconciliation gate can report success. Exact-head `validate`, `lint`, and Keycloak boundary checks passed. The scheduled reconcile [#41140628682](https://github.com/phanthienquoc/platform-infra/actions/runs/41140628682) failed closed on StockDividend package HTTP 403s; no pull credentials, manifests, or workloads were mutated.

- [ ] Harden GHCR preflight credential parsing: scheduled reconcile [#41140628682](https://github.com/phanthienquoc/platform-infra/actions/runs/41140628682) emitted repeated curl config line-2 warnings consistent with a terminal line ending in `GHCR_READ_TOKEN`. PR removes a terminal CR/LF safely and rejects embedded whitespace/quotes before any package probe; this does not change package permissions or bypass the fail-closed StockDividend 403s.


## Latest scheduled review (2026-10-31 06:56 Vietnam time)

- PR #858 is merged; exact-head validation passed. The follow-up VPS snapshot in PR #859 is newer than the previous 20:49Z snapshot and still shows StockDividend package 403s, MicroFE image references that do not exist, Media backend and Auth workloads not Ready, and Keycloak database authentication failures. Do not label production healthy.
- StockDividend is **not disabled as a repository or workload**. Its CI/build remains useful, and the old backend/frontend pods were still running in the latest snapshot. Keep release/promotion fail-closed while the two package permissions and `PLATFORM_INFRA_TOKEN` are unresolved; do not remove StockDividend from the global pull-credential contract because the shared credential applies to its namespace too.
- Next operator actions: (1) grant the `GHCR_READ_TOKEN` owner package read access to both StockDividend packages and verify `GHCR_USERNAME`; (2) configure `PLATFORM_INFRA_AUTOMATION_TOKEN` in Platform Infra Environment `production`; (3) configure StockDividend repository-level `PLATFORM_INFRA_TOKEN`; (4) verify Keycloak DB username/password and pooler endpoint through protected settings without printing or rotating secrets blindly; (5) rerun preflight and only then promote/reconcile and capture new rollout plus HTTP health evidence.


## Latest workflow evidence (2026-10-30T23:58Z / 2026-10-31 06:58 ICT)

- Platform Infra PR #860 was squash-merged as `bf5b860c37b86f4e7d54097f23aa7c432c6f2fb9`. Post-merge manifest validation [#41147545909](https://github.com/phanthienquoc/platform-infra/actions/runs/41147545909) and workflow validation [#41147425870](https://github.com/phanthienquoc/platform-infra/actions/runs/41147425870) passed. Observability follow-up [#41147464351](https://github.com/phanthienquoc/platform-infra/actions/runs/41147464351) passed.
- The first post-merge reconcile [#41147425844](https://github.com/phanthienquoc/platform-infra/actions/runs/41147425844) failed closed at `Validate GHCR pull access before mutating cluster credentials`. The log redacted the secret and reported only that `GHCR_READ_TOKEN` contains embedded whitespace or quotes. No package probes, shared pull-secret mutation, manifest apply, or rollout occurred. Correct the secret through protected GitHub Settings; do not print or retrieve its value.
- Latest TCE scheduled healthcheck [#41143292633](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41143292633) failed: TCE web returned HTTP 200, while `https://auth.mrcute.space/api/health` and `/api/ready` both returned HTTP 503. This agrees with the read-only VPS snapshot showing Auth not Ready. Do not mark Auth/TCE end-to-end production health PASS.
- StockDividend CI [#41131370110](https://github.com/phanthienquoc/stockdividend/actions/runs/41131370110) passed all four test/build jobs. Media CI [#41086891867](https://github.com/phanthienquoc/media-generation/actions/runs/41086891867) passed. Auth release [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) succeeded at image/release workflow level, but this is not live Auth readiness evidence.


## Latest workflow evidence (2026-10-31T00:36Z / 2026-10-31 07:36 ICT)

- **GHCR preflight retry:** reconciliation [#41147425844](https://github.com/phanthienquoc/platform-infra/actions/runs/41147425844), attempt 2, passed the token parser and attempted all nine package scopes. The GHCR token endpoint returned HTTP 403 for every package: `auth-service/auth`, Media backend/frontend, MicroFE Shell/WS, StockDividend admin/backend, and TCE service/web. The preflight stopped before provisioning/rotating the cluster pull Secret, applying manifests, or restarting pods. This supersedes the earlier attempt-1 note that only reported malformed token formatting. Because all package scopes now fail, check `GHCR_USERNAME` against the classic PAT owner, PAT validity and `read:packages`, required SSO authorization, and package access. Never expose the token; rerun preflight before reconciliation.

- **StockDividend release gate:** PR [#13](https://github.com/phanthienquoc/stockdividend/pull/13) was squash-merged at `0b0c6bde1772338db6d4cf9584bd74f827b594c2` after all five checks on exact head `1b2dc7a91cd0ea2a30985a9df3273866c25e5d68` passed: Admin production build, Backend test/build, Scraper syntax, Scraper container build, and Production release hold contract. The new gate requires repository variable `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true` before production image publication and promotion can run. The connected GitHub interface did not expose the repository-variable value, so verify it is not already set to `true` while credentials are unresolved. CI/build verification and currently running workloads are not disabled.

- **Health remains blocked:** TCE healthcheck [#41143292633](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41143292633) has TCE web HTTP 200 but Auth liveness and readiness both HTTP 503. No new successful production reconciliation or post-rollout health evidence is available. Do not mark production healthy or alter the TCE market-scan schedule.
