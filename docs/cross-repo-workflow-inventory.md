# Cross-Repository Workflow Inventory

Last reviewed: 2026-11-11 00:18 ICT (2026-11-10 17:18:32 UTC)

This is the compact current workflow inventory. The previous append-only inventory is preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md. Historical timestamped workflow checkpoints remain under docs/cross-repo-workflow-inventory-checkpoints/.

## Ownership and production authority

| Repository | Owns | Must not own |
|---|---|---|
| TCE-dashboard | App CI, tests, build verification, immutable TCE/MicroFE GHCR publication, public app health probes and app-specific backup/integration checks | Production manifests, shared pull credentials, production GitOps apply, K3s rollout or direct SSH/Compose deployment |
| StockDividend | App CI, tests, native ARM64 immutable image publication, scraper and safe credential preflight | Platform manifests, shared GHCR credentials, direct Kubernetes/SSH/Compose production deployment |
| Media Generation | App CI, tests and immutable image publication | Platform manifests, shared pull credentials, direct production deployment |
| phanthienquoc-authentication | Auth CI, tests, release/provenance and immutable app publication | Shared pull credentials, production manifests, direct production apply |
| platform-infra | Production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout, runtime inspection and health verification | App source tests/builds or app-owned image publication |

Platform reconcile-vps.yml is the single production apply authority. Platform inspect-vps.yml is read-only. Do not add competing SSH/Compose deployment authorities in app repositories.

## Platform Infra workflow files on master

| Workflow file | Responsibility / preservation |
|---|---|
| bootstrap-runner.yml | Allowlisted self-hosted runner bootstrap and scoped operational policy |
| configure-keycloak-no-email-registration.yml | Keycloak configuration utility |
| configure-keycloak-resend-smtp.yml | Transactional email configuration utility |
| decommission-stock-media.yml | Guarded decommission workflow; retain approval and evidence gates |
| gitops-image-promotion.yml | Verify app source-run provenance and promote approved immutable digests |
| inspect-vps.yml | Read-only K3s/VPS inspection; force-updates only the local remote-tracking ref when rebasing snapshots; never production apply |
| keycloak-auth-production-smoke.yml | Keycloak/Auth production smoke utility |
| keycloak-ci.yml | Keycloak CI |
| provision-auth-runtime-secret.yml | Scoped Auth runtime Secret provisioning and verification |
| provision-keycloak-tce-client.yml | Keycloak TCE client provisioning |
| reconcile-observability.yml | Observability reconciliation |
| reconcile-schedule-watchdog.yml | Read-only native schedule freshness watchdog |
| reconcile-vps.yml | Sole production manifest reconciliation/apply authority |
| recover-stale-ops.yml | Scheduled and receipt-backed recovery controller |
| runtime-secret-readiness.yml | Runtime Secret readiness validation |
| smoke-production.yml | Production smoke checks |
| sso-auto-onboarding.yml | SSO onboarding utility |
| staging-dry-run.yml | Staging dry-run |
| validate-github-actions.yml | Workflow, payload and contract validation; installs actionlint v1.7.12 from official release with checksum verification |
| validate-manifests.yml | Production manifest and deployment contract validation |
| validate-metrics.yml | Metrics validation |
| validate-recovery-readiness.yml | Recovery readiness contract |
| validate-tce-vps-control-mcp.yml | TCE VPS control MCP contract |
| verify-keycloak-tce-client.yml | Keycloak client verification |
| vps-image-cleanup.yml | Guarded image cleanup utility |
| vps-manual-operations.yml | Allowlisted manual operations |

## TCE Dashboard workflow files on master

| Workflow file | Responsibility / preservation |
|---|---|
| wf-01-tce-build-verify.yml | TCE build verification |
| wf-01p-tce-web-pr-build.yml | PR-scoped web build |
| wf-02-tce-backend-unit-test.yml | Backend unit tests |
| wf-02-tce-prettier-format.yml | Formatting validation |
| wf-03-tce-production-deploy.yml | App-owned, gated immutable production publisher |
| wf-06-tce-healthcheck.yml | Strict public HTTP 200 health checks; preserve the four approved endpoints |
| wf-07-tce-backup.yml | Scheduled backup; preserve |
| wf-07-tce-integration-check.yml | Scheduled integration check |
| wf-08b-tce-microfe-build-publish.yml | App-owned MicroFE image build/publication |
| wf-09-nginx-readonly-audit.yml | Read-only Nginx audit utility |
| wf-09-tce-vps-safe-setup.yml | Manual safe setup utility; not production apply authority |
| wf-10-tce-k3s-bootstrap.yml | Staging/bootstrap utility; keep separately gated |
| wf-11-tce-mobile-landscape-viewport.yml | UI/viewport validation |
| wf-12-tce-healthcheck-schedule-watchdog.yml | Native schedule freshness watchdog and heartbeat |
| wf-13-tce-healthcheck-recovery.yml | Healthcheck recovery utility |

## StockDividend workflow files on master

- ci.yml — app CI/tests.
- deploy.yml — app-owned manual/release-gated native ARM64 immutable image publisher; not direct production deployment.
- run_scraper.yml — weekend scraper with fail-closed VNSTOCK_API_KEY preflight.

## Media Generation workflow files on master

- ci.yml — app CI/tests.
- wf-03-media-production-deploy.yml — app-owned immutable image publication and Platform promotion handoff; production promotion remains token/owner gated.

## Authentication workflow files on master

- ci.yml — service CI/tests.
- release.yml — app-owned release and immutable publication/provenance.
- web-ci.yml — web CI/tests.

## Native schedule contracts

Only first-attempt event=schedule runs on master count for cadence acceptance. Push, pull_request, workflow_run, workflow_dispatch and repository_dispatch are not native schedule substitutes.

| Workflow | Current cron | Existing age/gap budget |
|---|---|---:|
| Platform reconcile-vps.yml | 7,22,37,52 * * * * | 2700s |
| Platform inspect-vps.yml | 2,32 * * * * | 4500s |
| Platform recover-stale-ops.yml | 10,25,40,55 * * * * | 2700s |
| Platform reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | 2700s |
| TCE wf-06-tce-healthcheck.yml | */15 * * * * | 1500s |
| TCE wf-12-tce-healthcheck-schedule-watchdog.yml | 7,22,37,52 * * * * | 1500s |

Current native evidence and exact age/gap values are in docs/cross-repo-deployment-tracker.md. Do not change cron, freshness budgets or TCE market-scan scheduling to hide delivery gaps.

## Publication and GitOps contract

1. App repository builds/tests and publishes immutable full-source-SHA plus version/source-SHA tags.
2. Publisher verifies architecture descriptors and registry-resolved digest equality before dispatch.
3. Platform verifies source workflow path, source SHA, run ID, attempt, release tag and image digests; it does not trust mutable tags or caller-supplied payloads alone.
4. Platform validates digest references, reconciles production manifests and verifies rollout/health only with fresh runtime evidence.
5. Shared ghcr-pull credentials are Platform-owned; app workflows must not rotate or mutate them.
6. Repository-level pre-push tag-absence guards and digest checks do not prove GHCR server-side immutable-tag policy. Registry-side enforcement remains unverified.

## Preservation decisions

- Keep all CI, test, security, formatting, release, backup, integration, manual and scheduled workflows listed above.
- No workflow is confirmed redundant or obsolete in this review.
- Do not merge owner-decision drafts or trigger a production publisher merely to make the inventory appear complete.
- Do not add duplicate direct SSH/Compose deployment authorities.
- Do not change the TCE market-scan schedule.

## Latest verification — 2026-11-11 00:18 ICT / 17:18:32 UTC

- Platform master is `61bbb9c0927ba43902f59344c38b289d493934b3`. PR #1587 and #1588 are merged. PR #1589 is the inspection-only auto-merge produced by workflow #42862329716; all inspection, output validation, latest-master rebase, PR creation and exact-head validation steps passed. Snapshot `debug/vps-latest.md` was generated at 17:11:28Z.
- PR #1588 fixed the persistent runner's non-fast-forward update of its local `refs/remotes/origin/master` by force-updating only that remote-tracking ref. It also pins actionlint v1.7.12 to the official Linux release and verifies the official checksum manifest and archive before execution. Exact-head `validate-github-actions` #42862175393 and `validate-manifests` #42862174503 both passed.
- Last completed K3s inspection snapshot is 424s old at this reference, within the 4500s freshness budget. K3s node Ready/ARM64; disk 56% with ~20 GiB free; available RAM ~19 GiB. Media backend/frontend and MicroFE Shell/WS/NATS are 1/1. TCE frontend/service, Auth and Keycloak are 0/0 maintenance. Stock Admin is 0/1 (two ImagePullBackOff pods) and desired Backend 0/1 on historical `12d63b4`; existing Backend/Frontend remain 1/1. Both public OIDC discovery probes return HTTP 503; Keycloak diagnostic timed out while deployment is 0/0. Host restart_required=yes.
- GitOps drift is clean. Protected decommission preflight found no Stock/Media namespace/image refs in the active Platform production manifest tree; no Stock/Media VolumeSnapshot refs or PVCs were found (only `k3s-debug` PVC exists), and preserved `tce-prod` and `microfe-platform` remain. Media runner service/listener is still active; GitHub runner registration and DNS ownership are not inferred. Decommission remains gated on remote unregister, backup/retention and DNS evidence.
- GHCR digest coverage remains warning: cached Stock backend/user tags `23b2878` lack RepoDigest; local image IDs are not registry digests or publication evidence. Stock Admin/desired Backend continue to fail with `no match for platform in manifest` on `12d63b4`.
- Last reconciliation #42849053816 completed at 15:55:16Z and is 4996s old, outside the 2700s evidence budget. It verified GHCR read access, Auth runtime Secret presence with values suppressed, shared `ghcr-pull` unchanged and GitOps drift=false; production apply, image replacement and rollout were skipped.
- Last-confirmed native schedule inventory is from 15:57:57Z. The connected workflow-run reader exposes PR-triggered runs only; later native schedule events cannot be enumerated here. Last-confirmed event ages are recorded in the deployment tracker and must not be treated as proof no later event occurred. Cron and freshness budgets remain unchanged.
- TCE WF-06 #42799497774 still records four HTTP 503 responses against strict expected HTTP 200. Stock CI #42610360402, Media CI #42539512417 and Auth CI #42654579277 remain the last successful master CI evidence; Stock scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`.
- No image publication, digest promotion, production apply, workload rollout/scaling, credential rotation, DNS/database/storage mutation, runner retirement or host reboot occurred. TCE market-scan schedule unchanged.
## Historical evidence

- Previous full append-only inventory preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md.
- Timestamped workflow checkpoints: docs/cross-repo-workflow-inventory-checkpoints/.
- Current readiness and runtime blockers: docs/cross-repo-deployment-tracker.md.
