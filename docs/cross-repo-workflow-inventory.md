# Cross-Repository Workflow Inventory

Last reviewed: 2026-11-11 12:04 ICT (2026-11-11 05:04:56 UTC).

This is the compact current workflow inventory. The previous append-only inventory is preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md. Historical timestamped workflow checkpoints remain under docs/cross-repo-workflow-inventory-checkpoints/.

## Ownership and production authority

| Repository | Owns | Must not own |
|---|---|---|
| TCE-dashboard | App CI, tests, build verification, immutable TCE/MicroFE GHCR publication, public app health probes and app-specific backup/integration checks | Production manifests, shared pull credentials, production GitOps apply, K3s rollout or direct SSH/Compose deployment |
| StockDividend | App CI, tests, native ARM64 immutable image publication, scraper and safe credential preflight | Platform manifests, shared GHCR credentials, direct Kubernetes/SSH/Compose production deployment |
| Media Generation | App CI, tests and immutable image publication | Platform manifests, shared pull credentials, direct production deployment |
| phanthienquoc-authentication | Auth CI, tests, release/provenance and immutable app publication | Shared pull credentials, production manifests, direct production apply |
| platform-infra | Production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout, runtime inspection and health verification | App source tests/builds or app-owned image publication |

Platform reconcile-vps.yml is the single production apply authority. Platform inspect-vps.yml is read-only. Manual reconcile dispatch has no image-change override; only the provenance-verified gitops-promoted-ready repository_dispatch may bypass the image guard after the originating promotion run and required jobs are verified. Do not add competing SSH/Compose deployment authorities in app repositories.

## Platform Infra workflow files on master

| Workflow file | Responsibility / preservation |
|---|---|
| bootstrap-runner.yml | Allowlisted self-hosted runner bootstrap and scoped operational policy |
| configure-keycloak-no-email-registration.yml | Keycloak configuration utility |
| configure-keycloak-resend-smtp.yml | Transactional email configuration utility |
| decommission-stock-media.yml | Guarded decommission workflow; retain approval and evidence gates |
| gitops-image-promotion.yml | Verify app source-run provenance and promote approved immutable digests |
| inspect-vps.yml | Read-only K3s/VPS inspection; never production apply |
| keycloak-auth-production-smoke.yml | Keycloak/Auth production smoke utility |
| keycloak-ci.yml | Keycloak CI |
| provision-auth-runtime-secret.yml | Scoped Auth runtime Secret provisioning and verification |
| provision-keycloak-tce-client.yml | Keycloak TCE client provisioning |
| reconcile-observability.yml | Observability reconciliation |
| reconcile-schedule-watchdog.yml | Read-only native schedule freshness watchdog |
| reconcile-vps.yml | Sole production manifest reconciliation/apply authority; image-change bypass only for provenance-verified gitops-promoted-ready dispatch; recursive Keycloak Markdown excluded from push trigger; resolver-only edits do not auto-apply |
| recover-stale-ops.yml | Scheduled and receipt-backed recovery controller; recursive Keycloak operator Markdown excluded from push recovery |
| runtime-secret-readiness.yml | Runtime Secret readiness validation |
| smoke-production.yml | Production smoke checks |
| sso-auto-onboarding.yml | SSO onboarding utility |
| staging-dry-run.yml | Staging dry-run |
| validate-github-actions.yml | Workflow, payload and contract validation |
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

- `ci.yml` — app CI/tests, including non-publishing native ARM64 builds for scraper/admin/backend.
- `deploy.yml` — app-owned, gated native ARM64 immutable image publisher. Code review confirms the workflow requires a native `ubuntu-24.04-arm` runner, publishes scraper/admin/backend with full-source-SHA and `prod-v<semver>-<sha>` tags, verifies `linux/arm64` descriptors and digest equality for both tags, and refuses existing immutable tags. Manual publication requires `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`. The workflow does not dispatch to Platform; approved digests are handed off separately. No publication was run in this checkpoint.
- `run_scraper.yml` — weekend scraper with fail-closed `VNSTOCK_API_KEY` preflight and side-effect-free `preflight_only=true` path.

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
4. Only the `gitops-promoted-ready` repository_dispatch may authorize workload image replacement, and only after Platform validates the originating promotion run, required job results, release identity, source commit and digest-pinned image references. Manual `reconcile-vps.yml` dispatch exposes no image-change override.
5. Manual, scheduled and push-triggered reconciliation remain subject to `guard-reconcile-images.sh`; non-image manifest changes can still be applied through the single Platform apply authority.
6. Platform validates digest references, reconciles production manifests and verifies rollout/health only with fresh runtime evidence.
7. Shared `ghcr-pull` credentials are Platform-owned; app workflows must not rotate or mutate them.
8. Repository-level pre-push tag-absence guards and digest checks do not prove GHCR server-side immutable-tag policy. Registry-side enforcement remains unverified.

## Preservation decisions

- Keep all CI, test, security, formatting, release, backup, integration, manual and scheduled workflows listed above.
- No workflow is confirmed redundant or obsolete in this review.
- Do not merge owner-decision drafts or trigger a production publisher merely to make the inventory appear complete.
- Do not add duplicate direct SSH/Compose deployment authorities.
- Do not change the TCE market-scan schedule.

## Latest verification — 2026-11-11 07:02 ICT / 00:02:43 UTC

- Master refs at the 00:02:43Z snapshot, read directly from Git refs: Platform `ad54469d6cf0d2c3362d6105f50fa9131dadf8a5`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. All remain drafts/owner decisions. Exact-head `validate` checks pass on all five; Authentication Supabase Preview is skipped. No open PRs in TCE, Stock or Media.
- PR #1601 merged at `72ed11ef`, removing manual `allow_image_changes`. PR #1602 merged at `8b11d662`, adding read-only inspection evidence. PR #1603 merged at `98bc3d8c`, excluding Keycloak Markdown from reconcile/recovery push scope and making resolver-only edits fail closed. PR #1604 merged at `ad54469d`, refreshing readiness docs. Exact-head and post-merge checks for #1603 and #1604 passed; latest post-merge manifest validation is #42921972012 PASS.
- Historical push run #42920184478 (event=push, created 23:04:13Z, completed 23:04:57Z) misclassified `platform/keycloak/README.md`, applied the Keycloak resource set and executed the narrow Auth/Keycloak scale-to-zero action. No pre-scale replica snapshot exists, so the exact state transition is unknown. PR #1603 added path exclusions and resolver-only fail-closed regression coverage. No reconcile/recovery push run was created by the #1603/#1604 merges.
- Latest Platform recovery receipt #42922588369 (event=repository_dispatch, 23:20:48Z) verified TCE WF-06 heartbeat #42922537816. Reconcile fallback was skipped because the last reconcile activity #42920184478 was 15 minutes old at recovery time. The recovery controller found the existing read-only inspection fallback #42920320410 still fresh (age 13 minutes at that run), so no additional inspection was dispatched. This is not a native schedule delivery or a new reconciliation.
- Current native schedule evidence at 00:02:43Z (only first-attempt event=schedule on master counts): Platform reconcile #42909757881 age 7607s / gap 19941s; inspection #42887151366 age 15905s / gap 28677s; recovery #42906791198 age 8735s / gap 20656s; watchdog #42908417737 age 8120s / gap 20852s; TCE WF-06 #42922537816 age 2535s / gap 18739s; TCE WF-12 #42915709227 age 5334s / gap 17617s. All six age and gap budgets fail. TCE WF-06 failed strict HTTP 200 checks; WF-12 failed freshness. Separate TCE WF-07 backup #42924677977 succeeded at 23:35:49Z but does not replace either health lane.
- Current cron expressions were re-read from the actual workflow files: Platform reconcile `7,22,37,52 * * * *`; inspection `2,32 * * * *`; recovery `10,25,40,55 * * * *`; watchdog `12,27,42,57 * * * *`; TCE WF-06 `*/15 * * * *`; TCE WF-12 `7,22,37,52 * * * *`. Keycloak recursive Markdown exclusions remain in reconcile/recovery push filters. No cron or market-scan schedule changed.
- Fresh read-only inspection #42920320410 generated `debug/vps-latest.md` at 23:05:16Z; age 3447s at this reference, within the 4500s budget. Host ARM64 Ubuntu 22.04.5, uptime 193 days, 19 GiB RAM available, root disk 56% used / 20 GiB free, `restart_required=yes`; K3s node Ready, v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Workloads in that snapshot: Media backend/frontend 1/1 with registry-resolved digest evidence; MicroFE Shell/WS/NATS 1/1; TCE frontend/service 0/0; Auth/Keycloak 0/0; OIDC discovery HTTP 503. Stock Admin has two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod on `12d63b4` (no ARM64 platform match); legacy Backend/Frontend 1/1 on `23b2878`, but no RepoDigest evidence for promotion.
- Storage preflight reports no Stock/Media PVC or VolumeSnapshot references; `k3s-debug/k3s-debug-logs` remains bound. Media runner service/listener active/enabled; remote runner unregister, backup/retention and authoritative DNS ownership remain unverified.
- Latest reconcile run #42920184478 is now 3466s old; manual reconciliation #42915749236 is 5318s old. Prior manual reconciliation verified GHCR read access, Auth runtime Secret (values suppressed), unchanged shared `ghcr-pull`, clean GitOps drift and skipped apply/image replacement/rollout. Recovery #42922588369 is a repository_dispatch receipt, not a native scheduled reconciliation.
- TCE native WF-06 #42922537816 failed all four public endpoint jobs; Auth readiness log observed HTTP 503 versus required HTTP 200. WF-12 #42915709227 failed because native WF-06 evidence is stale. TCE backend tests previously passed. Stock CI #42610360402 passed; scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. Media CI #42539512417 and Auth CI #42654579277 passed.
- Branch-protection detail GET returned 403 for all five repositories. Rulesets GET returned `[]` for four public repositories; private Stock rulesets GET returned 403 with a plan limitation. Effective inherited rulesets remain unverified; administrator confirmation is required.
- GHCR server-side immutable-tag enforcement remains unverified. Pre-push tag-absence guards and digest equality do not prove registry-side enforcement.
- No new image publication, digest promotion, production apply, rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
- Preserve all useful CI/test/security, formatting, release, backup, integration, manual and scheduled workflows. No workflow is confirmed redundant or obsolete. Do not add direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Retired Stock/Media GitOps and K3s status — 2026-11-11 07:56 ICT

- StockDividend and Media Generation remain application repositories for CI/tests and their own gated image publishers, but their production manifest trees and image/namespace references have been removed from the active Platform GitOps scope. The current tree has no `apps/stockdividend` or `apps/media-generation` manifest tree; `scripts/verify-retired-production-manifests.sh` fails if those trees or Stock/Media references reappear under `environments/prod`, `platform` or `apps`.
- Keep `.github/workflows/decommission-stock-media.yml` and its helper/test scripts. This is the sole guarded namespace retirement path, not an application deployment workflow. Its plan mode is read-only. Delete mode requires the production environment, exact typed confirmations, stable HTTPS backup and DNS evidence references, local Media runner stopped/disabled with no listener, authoritative GitHub runner registration absence verified using the scoped audit token, and a fresh namespace/PV/PVC/VolumeSnapshot preflight.
- Inspection #42932368784 generated the latest read-only snapshot at 00:34:17Z. The embedded Stock/Media storage preflight returned `storage-clean`: no PVC, PV claim or VolumeSnapshot/VolumeSnapshotContent references in `stock-prod` or `media-prod`. Both namespaces remain Active and workloads remain present. The separate `k3s-debug/k3s-debug-logs` PVC is Bound and must be preserved.
- The Media runner service is active/enabled and its listener process is present. GitHub runner registration is not inferred from host inspection. External DB/object-storage backup/retention and authoritative DNS/provider ownership are still unverified. The explicit decommission workflow plan mode has not been dispatched; the inspection ran the underlying read-only namespace/storage preflight.
- No delete-mode execution, namespace/PVC/PV deletion, runner stop/disable/unregister, external-data mutation, DNS change, credential rotation or host restart occurred. Do not publish/promote Stock or Media production images while the approved retirement is pending.
- Preserve TCE/Auth workloads and TCE market-scan schedule. The decommission workflow must remain narrowly scoped to `stock-prod` and `media-prod`.

## Latest verification — 2026-11-11 07:56 ICT / 00:56:58 UTC

- Direct Git refs: Platform `0faec01a5ad0f7c7349a1dd9d22750e80d32756f`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. Exact-head validation runs #42161859747, #38575430454, #38567431761, #38548718033 and #41329425940 all completed successfully. All remain drafts/owner decisions. No open PRs in TCE, Stock or Media.
- Platform PR #1607 was generated by native scheduled inspection #42932368784 and squash-merged at `0faec01a`; only `debug/vps-latest.md` changed. Exact-head validation was part of the inspection workflow; no post-merge manifest validation was triggered because deployment files did not change.
- Manual reconcile #42932691349 succeeded with GHCR read preflight, Auth runtime Secret verified (values suppressed), shared `ghcr-pull` unchanged, managed MicroFE/TCE pull checks clean, TCE release pairing passed and GitOps drift=false. Manifest apply, image replacement and rollout were skipped. Stock ImagePullBackOff pods remained; Stock is outside the managed pull helper and is in the approved retirement scope.
- Recovery #42932880278 succeeded as workflow_dispatch for source reconcile #42932691349. It verified the source completion and found the reconciliation and native inspection recent; no fallback reconcile or inspection was dispatched. This is not native schedule delivery.
- Latest native schedule metrics at 00:56:58Z: Platform reconcile #42909757881 age 10862s/gap 19941s; inspection #42932368784 age 1369s/gap 17791s; recovery #42906791198 age 11990s/gap 20656s; watchdog #42908417737 age 11375s/gap 20852s; TCE WF-06 #42922537816 age 5790s/gap 18739s; TCE WF-12 #42915709227 age 8589s/gap 17617s. All six inter-arrival gaps fail; five current-age budgets fail. Manual and workflow_run fallbacks are not counted.
- Current inspection: K3s node Ready (ARM64, v1.36.3+k3s1, containerd 2.3.2-k3s2), disk 56% / 20 GiB free, RAM 19 GiB available, restart required. Media and MicroFE core pods 1/1; TCE/Auth/Keycloak 0/0 maintenance; public OIDC both realms HTTP 503. Stock Admin (two pods) and desired Backend (one pod) ImagePullBackOff on `12d63b4` due no ARM64 platform match; legacy Backend/Frontend remain running but cached tags have no RepoDigest.
- TCE native WF-06 #42922537816 failed all four strict HTTP 200 endpoint checks; WF-12 #42915709227 failed freshness. Stock CI #42610360402 passed; scraper #42457182511 failed closed due missing `VNSTOCK_API_KEY`. Media CI #42539512417 and Auth CI #42654579277 passed.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred.
- Preserve all CI/test/security, formatting, release, backup, integration, manual and scheduled workflows. No workflow is confirmed redundant or obsolete. Do not add direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 08:05 ICT / 01:05:25 UTC

- Direct master refs: Platform 010558ada7c36738a287ed38ae107d260f63ebf9; TCE c4602be3b0a7b624bdb9cd41519cfc70a14d92ab; Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61; Media dcd698699c65ba6e73f6b43838975144777131c3; Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f.
- PR #1608 refreshed the deployment tracker/inventory and Stock/Media retirement evidence, merging at Platform master 010558ada7c36738a287ed38ae107d260f63ebf9. Latest Platform master run #42935987763 (validate-manifests, push) completed SUCCESS at 01:02:54Z. No production reconcile/recovery push run followed the docs-only merge.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. Exact-head checks: #1314 #42161859747 PASS; #544 #38575430454 PASS; #541 #38567431761 PASS; #539 #38548718033 PASS; Auth #76 #41329425940 validate PASS, Supabase Preview skipped. All remain drafts/owner decisions. No open PRs in TCE, Stock or Media.
- Latest workflow evidence: TCE native WF-06 #42922537816 and manual WF-06 #42922596353 both failed all four public endpoint checks (503 vs 200); native WF-12 #42915709227 failed freshness; WF-07 backup #42924677977 succeeded but is not a health substitute. Stock CI #42610360402 passed; scraper #42457182511 failed closed on absent VNSTOCK_API_KEY. Media CI #42539512417 and Auth CI #42654579277 passed.
- Native schedule reference: 01:05:25Z. Platform reconcile #42909757881 age 11369s/gap 19941s; inspection #42932368784 age 1876s/gap 17791s; recovery #42906791198 age 12497s/gap 20656s; watchdog #42908417737 age 11882s/gap 20852s; TCE WF-06 #42922537816 age 6297s/gap 18739s; TCE WF-12 #42915709227 age 9096s/gap 17617s. All six inter-arrival gaps fail; five current-age budgets fail. Only first-attempt event=schedule on master counts. Manual and workflow_run fallbacks do not substitute.
- Cron expressions remain unchanged: Platform reconcile 7,22,37,52 * * * *; inspection 2,32 * * * *; recovery 10,25,40,55 * * * *; watchdog 12,27,42,57 * * * *; TCE WF-06 */15 * * * *; TCE WF-12 7,22,37,52 * * * *. TCE market-scan schedule unchanged.
- Freshest full K3s inspection #42932368784 generated debug/vps-latest.md at 00:34:17Z, age 1,868s at this reference and still within the 4,500s budget. Node Ready (ARM64, K3s v1.36.3+k3s1), disk 56% / ~20 GiB free, ~19 GiB RAM available, host restart required. Media backend/frontend and MicroFE core 1/1; TCE/Auth/Keycloak 0/0 maintenance; OIDC discovery 503; Stock Admin (two pods) and desired Backend ImagePullBackOff on 12d63b4 due missing ARM64 platform descriptor. No reboot or workload mutation.
- Stock/Media production manifests remain retired from active Platform GitOps. Both namespaces/workloads remain present pending the guarded decommission. Storage preflight from inspection found no target PVC/PV/VolumeSnapshot references; preserve the separate Bound k3s-debug/k3s-debug-logs PVC. Dedicated Media runner service/listener remains active/enabled; remote unregister, external backup/retention and authoritative DNS ownership remain unverified. Delete mode remains blocked.
- GHCR read access and Auth runtime Secret were verified by manual reconciliation #42932691349; shared ghcr-pull unchanged; GitOps drift clean; apply/image replacement/rollout skipped. Recovery receipt #42932880278 reused fresh existing inspection and did not dispatch a new inspection or reconciliation.
- No new image publication, digest promotion, production apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation or host restart occurred in this checkpoint. Preserve CI/test/security/release/backup/integration/manual/scheduled workflows; no workflow confirmed obsolete; no duplicate SSH/Compose authority.


## Latest verification — 2026-11-11 09:02 ICT / 02:02:00 UTC

- Direct master refs: Platform `fbb479fc7e6415eeec8ef34fdaccf039f5477e17`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. No open PRs in TCE, Stock or Media. All listed PRs remain drafts/owner decisions; exact-head `validate` checks pass; Auth Supabase Preview is skipped.
- Platform PR #1610 is the latest inspection-only merge at `fbb479fc`. Source inspection #42942360712 and exact-head validation #42942563353 passed. It only updated `debug/vps-latest.md`; no post-merge master validation run was observed for this debug-only change.
- Latest app CI evidence: TCE backend CI previously passed, but native WF-06 #42922537816 failed four strict public HTTP 200 probes with 503 and WF-12 #42915709227 failed freshness. Stock CI #42610360402 passed; scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is empty. Media CI #42539512417 and Auth CI #42654579277 passed. No new Stock/Media/Auth image publication was run.
- Native cadence at 02:02:00Z: Platform reconcile #42942147668 age 520s / gap 14,244s; inspection #42932368784 age 5,271s / gap 17,791s; recovery #42939222343 age 2,003s / gap 13,889s; watchdog #42940581820 age 1,327s / gap 13,950s; TCE WF-06 #42922537816 age 9,692s / gap 18,739s; TCE WF-12 #42915709227 age 12,491s / gap 17,617s. All six inter-arrival gaps fail. Current age passes only for three Platform lanes. Manual inspection #42942360712 generated a fresh snapshot at 01:55:21Z but does not count as native schedule delivery.
- Watchdog logs show no sampled scheduled deployment lane above the 15-minute runner queue budget, while inter-arrival gaps remain 3.8–5.2 hours. Scheduler enqueue/delivery telemetry is not available through the repository workflow; GitHub administrator investigation remains a blocker.
- Fresh K3s snapshot: node Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% / ~20 GiB free; ~19 GiB RAM available; restart required. Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1. Public OIDC discovery both realms HTTP 503.
- Stock/Media remain outside active Platform GitOps manifest scope but their namespaces/workloads remain pending the guarded retirement workflow. Storage preflight reports no target PVC/PV/VolumeSnapshot references; preserve Bound `k3s-debug/k3s-debug-logs`. Media runner service/listener remains active/enabled; remote unregister, external backup/retention and DNS ownership are not verified.
- Native reconciliation #42942147668 verified GHCR read access for five managed packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, observed TCE release pairing and clean GitOps drift, and skipped manifest apply/rollout. MicroFE health passed; TCE/Auth remain intentional zero-replica maintenance; Keycloak skipped.
- Do not alter cron, freshness budgets, TCE market-scan schedule or deployment ownership. Preserve CI/test/security/release/backup/integration/manual/scheduled workflows. No workflow is confirmed redundant or obsolete; no duplicate SSH/Compose authority was introduced.


## Latest verification — 2026-11-11 10:01 ICT / 03:01:03 UTC

- Direct master refs: Platform `1accff7fd7cc1ae733513dfa7eb6067a660f030a`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Authentication #76; no open PRs in TCE, Stock or Media. All remain draft/owner-decision. No workflow file was added or removed in this checkpoint.
- Platform manual reconciliation #42949244537 (workflow_dispatch, mode=apply, target=all, image changes disabled) succeeded with clean drift. GHCR preflight and Auth runtime Secret verification passed; shared `ghcr-pull` was unchanged. TCE desired/live image pairing matched `prod-v0.1.0-e75e338`. MicroFE was healthy; TCE/Auth were explicit zero-replica maintenance; Keycloak was skipped. Apply and rollout were skipped.
- Recovery receipt #42949413722 verified reconciliation #42949244537 and found native inspection #42932368784 stale. It reused the fresh manual inspection fallback #42942360712 (age 59m at 02:57Z) and did not dispatch a duplicate inspection. The fallback is 3,942s old at the 03:01:03Z reference and has only 558s remaining within the 4,500s limit. Fallback receipts do not satisfy native schedule cadence.
- Native schedule reference 03:01:03Z: Platform reconcile #42942147668 age 4,063s / gap 14,244s; inspection #42932368784 age 8,814s / gap 17,791s; recovery #42939222343 age 5,546s / gap 13,889s; watchdog #42940581820 age 4,870s / gap 13,950s; TCE WF-06 #42949191917 age 382s / gap 12,853s; TCE WF-12 #42944415193 age 2,908s / gap 13,126s. All six gaps fail; only TCE WF-06 current age passes. Watchdog runner-queue sample was below 15 minutes but does not provide scheduler enqueue/delivery telemetry.
- TCE native WF-06 #42949191917 and manual WF-06 #42949231253 failed strict HTTP 200 checks: TCE web, TCE API, Auth liveness and Auth readiness returned 503. WF-12 #42944415193 failed freshness. Preserve the strict health contract.
- Last-known K3s fallback #42942360712: node Ready/ARM64; disk 56% / ~20 GiB free; ~19 GiB RAM available; restart required. Media and MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1. Media runner remains active; retirement evidence incomplete. Snapshot expires at approximately 03:10:21Z if no newer inspection arrives.
- Keep the existing app-owned publisher workflows and Platform's single production apply authority. No app-owned direct SSH/Compose deploy authority was added. No workflow was confirmed redundant/obsolete. Do not change cron, freshness budgets or TCE market-scan schedule.


## Latest verification — 2026-11-11 10:55 ICT / 03:55:46 UTC

- Direct master refs: Platform `9848cdeb97a29ff3833378013f4932e6558cb933`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314/#544/#541/#539; Authentication #76; none in TCE/Stock/Media. Heads unchanged from the exact-head validation evidence recorded in the deployment tracker. All remain drafts/owner decisions.
- Latest workflow evidence: Platform master push validation #42950290166 PASS; TCE native WF-06 #42949191917 and manual #42949231253 failed four strict 503 probes; native WF-12 #42944415193 failed freshness; Stock CI #42610360402 PASS and scraper #42457182511 failed closed; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes have stale current-age and inter-arrival evidence at 03:55:46Z. Exact run IDs, ages, gaps and budgets are recorded in the deployment tracker. Do not count manual/workflow_run/repository_dispatch fallback receipts as native schedule delivery.
- Latest K3s snapshot #42942360712 is 7,225s old and exceeds the 4,500s freshness budget. Latest manual reconciliation #42949244537 is 3,636s old and exceeds its 2,700s budget. Prior GHCR/Secret/drift results are historical; no current rollout authorization is inferred.
- Preserve application-owned build/publish and Platform-only production apply boundaries. Stock/Media remain in guarded retirement scope; no republish, delete, runner retirement, credential rotation, host restart or DNS/database/storage mutation occurred. Preserve all useful workflows; none was confirmed redundant/obsolete. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 12:04 ICT / 05:04:56 UTC

- Direct master refs: Platform Infra `bfa50827eacdb6675f718593c0b38cf693a38b01`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Current open PRs: Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. All remain drafts/owner decisions. Exact-head checks on those PRs are successful; Auth Supabase Preview is skipped. Do not merge owner-decision work without approval.
- Latest master CI: Platform validation #42956212725 PASS; TCE native WF-06 #42949191917 and manual #42949231253 fail all four strict public probes (HTTP 503 vs 200); WF-12 native #42944415193 fails freshness; Stock CI #42610360402 PASS and scraper #42457182511 fails closed on empty `VNSTOCK_API_KEY`; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes at 05:04:56Z: reconcile #42942147668 age 11,496s/gap 14,244s; inspection #42932368784 age 16,247s/gap 17,791s; recovery #42939222343 age 12,979s/gap 13,889s; watchdog #42940581820 age 12,303s/gap 13,950s; TCE WF-06 #42949191917 age 7,815s/gap 12,853s; TCE WF-12 #42944415193 age 10,341s/gap 13,126s. Every current-age and inter-arrival check exceeds its budget. Fallback receipts do not count.
- Latest K3s inspection #42942360712 is 11,375s old against 4,500s. Last manual reconciliation #42949244537 is 7,786s old against 2,700s. Both are stale; prior GHCR/Secret/drift results are historical and do not authorize rollout.
- Direct branch reads report `protected=false` for all five master branches. Repository metadata allows squash, merge commits and rebase on all five; administrator must confirm effective inherited rulesets and enforce squash-only/PR-only policy.
- App repositories retain ownership of CI/builds and immutable image publication. Platform remains the sole production apply authority. No new publication, promotion, apply, rollout, retirement, credential/DNS/database/storage mutation or host restart occurred. Preserve useful workflows; none was confirmed redundant/obsolete. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.
