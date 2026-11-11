# Cross-Repository Workflow Inventory

Last reviewed: 2026-11-11 18:09 ICT (fresh read-only K3s inspection).

This is the compact current workflow inventory. The previous append-only inventory is preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md. Historical timestamped workflow checkpoints remain under docs/cross-repo-workflow-inventory-checkpoints/.

## Historical verification — 2026-11-11 15:09 ICT / 08:09:56 UTC

- Direct master refs: Platform `48c9cf344c40fb76b1c720149d67bbced29e9255`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Authentication #76, all draft/owner decisions; none in TCE/Stock/Media. Last exact-head validation runs remain PASS for the unchanged heads; Auth Supabase Preview is skipped.
- Platform native inspection #42981286761 succeeded and generated inspection PR #1620, merged at current master #48c9cf34. Manual reconciliation #42981589486 succeeded: GHCR read preflight passed for five managed packages; Auth runtime Secret provision/verification passed with values suppressed; shared `ghcr-pull` unchanged; TCE desired/live release pairing passed; drift=false; manifest apply and image replacement skipped. TCE/Auth zero replicas are intentional maintenance, not healthy. Recovery #42981775331 succeeded without duplicate fallback dispatch. Watchdog #42981569803 failed on stale native cadence; no scheduled runner queue exceeded 15 minutes in its sample.
- TCE native WF-06 #42949191917 and WF-12 #42944415193 remain failed/stale. Manual WF-06 #42972014911 confirms four strict endpoints returned 503 instead of 200. WF-07 integration schedule #42971954835 passed but does not replace health lanes. Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Native cadence reference 08:09:56Z: Platform reconcile #42942147668 age 22,596s/gap 14,244s; inspection #42981286761 age 1,730s/gap 25,617s; recovery #42939222343 age 24,079s/gap 13,889s; watchdog #42940581820 age 23,403s/gap 13,950s; TCE WF-06 #42949191917 age 18,915s/gap 12,853s; TCE WF-12 #42944415193 age 21,441s/gap 13,126s. All six inter-arrival budgets fail; five of six current-age budgets fail. Keep all cron expressions and the TCE market-scan schedule unchanged.
- Fresh read-only K3s snapshot #42981286761 generated at 07:41:14Z and is 1,722s old at reference (within 4,500s). Node Ready/ARM64; K3s v1.36.3+k3s1; disk 56% / ~20 GiB free; ~19 GiB RAM available; host restart required. Media and MicroFE core pods 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1. Media runner service/listener active; retirement evidence incomplete.
- No new app image publication or digest promotion. No GitOps drift, manifest apply, image replacement or workload rollout in reconciliation #42981589486. Shared pull Secret unchanged; Auth runtime Secret provision/verification succeeded. No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot.
- Preserve CI/test/security, app-owned immutable publishers, release, backup, integration, manual and scheduled workflows. No workflow confirmed obsolete. No direct SSH/Compose authority. Platform remains the only production apply authority.

## Post-merge verification — 2026-11-11 15:18 ICT

- Platform master advanced documentation-only to `9c2e4e0efb54aad29bcdb82afeaf06c187c60499` through PR #1621.
- Exact-head validation #42985848211 and post-merge master validation #42985958377 both PASS.
- Only `validate-manifests` ran after the docs-only merge; no production reconcile/recovery push run was triggered.
- The 15:09 ICT workflow checkpoint remains the latest operational snapshot; this addendum updates only the Platform master SHA and merge receipt.
- Workflow ownership and production authority boundaries are unchanged; no workflow was removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.

## Post-merge verification — 2026-11-11 15:20 ICT

- Platform master advanced documentation-only to `8f95ddd8729eae6fee662e3a395f083be4fc21b0` through PR #1622.
- Exact-head validation #42986144723 and post-merge master validation #42986252700 both PASS.
- Only `validate-manifests` ran after the docs-only merge; no production reconcile/recovery push was triggered.
- The 15:09 ICT operational checkpoint remains the latest runtime/schedule evidence.
- Workflow ownership and production authority boundaries are unchanged; no workflow was removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.

## Historical verification — 2026-11-11 15:25 ICT / 08:25:10 UTC

- Platform master: `c811ed79f22505c074eaa9b08b0e8a61e59db08a`; TCE: `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media: `dcd698699c65ba6e73f6b43838975144777131c3`; Auth: `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform PR #1623 exact-head #42986594992 and post-merge #42986698420 PASS. Current open owner-decision PRs: Platform #1314/#544/#541/#539 and Auth #76; no TCE/Stock/Media PRs.
- Platform native inspection #42981286761 PASS; native recovery #42986496462 PASS; native watchdog #42986833403 FAIL on stale cadence. Manual reconciliation #42986517013 PASS: GHCR preflight, Auth Secret verification, shared pull Secret unchanged, no drift, no manifest apply/image replacement. Recovery #42986712253 PASS with no duplicate fallback dispatch.
- TCE native WF-06 #42949191917 and WF-12 #42944415193 remain stale/failed; manual WF-06 #42972014911 returned HTTP 503 on all four strict probes. TCE/Auth are intentional 0/0 maintenance. Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Native schedule reference 08:25:10Z: reconcile #42942147668 age 23,510s/gap 14,244s; inspection #42981286761 age 2,644s/gap 25,617s; recovery #42986496462 age 171s/gap 24,822s; watchdog #42986833403 age 20s/gap 24,297s; TCE WF-06 #42949191917 age 19,829s/gap 12,853s; TCE WF-12 #42944415193 age 22,355s/gap 13,126s. All six inter-arrival gaps fail; three current-age budgets fail. Preserve cron and TCE market-scan schedule.
- Fresh K3s snapshot #42981286761 age 2,636s / 4,500s. Node Ready/ARM64; disk 56% / ~20 GiB free; ~19 GiB RAM; restart required. Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1. Media runner active; retirement evidence incomplete.
- App repos retain CI/build/immutable publication ownership; Platform remains sole production apply authority. No image publication, digest promotion, manifest apply, workload rollout, destructive retirement, credential rotation, host reboot or DNS/database/storage mutation. Auth runtime Secret provision/verification succeeded; shared `ghcr-pull` unchanged. No workflow removed or SSH/Compose authority added.

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

## Historical verification — 2026-11-11 07:02 ICT / 00:02:43 UTC

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

## Historical verification — 2026-11-11 07:56 ICT / 00:56:58 UTC

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


## Historical verification — 2026-11-11 08:05 ICT / 01:05:25 UTC

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


## Historical verification — 2026-11-11 09:02 ICT / 02:02:00 UTC

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


## Historical verification — 2026-11-11 10:01 ICT / 03:01:03 UTC

- Direct master refs: Platform `1accff7fd7cc1ae733513dfa7eb6067a660f030a`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Authentication #76; no open PRs in TCE, Stock or Media. All remain draft/owner-decision. No workflow file was added or removed in this checkpoint.
- Platform manual reconciliation #42949244537 (workflow_dispatch, mode=apply, target=all, image changes disabled) succeeded with clean drift. GHCR preflight and Auth runtime Secret verification passed; shared `ghcr-pull` was unchanged. TCE desired/live image pairing matched `prod-v0.1.0-e75e338`. MicroFE was healthy; TCE/Auth were explicit zero-replica maintenance; Keycloak was skipped. Apply and rollout were skipped.
- Recovery receipt #42949413722 verified reconciliation #42949244537 and found native inspection #42932368784 stale. It reused the fresh manual inspection fallback #42942360712 (age 59m at 02:57Z) and did not dispatch a duplicate inspection. The fallback is 3,942s old at the 03:01:03Z reference and has only 558s remaining within the 4,500s limit. Fallback receipts do not satisfy native schedule cadence.
- Native schedule reference 03:01:03Z: Platform reconcile #42942147668 age 4,063s / gap 14,244s; inspection #42932368784 age 8,814s / gap 17,791s; recovery #42939222343 age 5,546s / gap 13,889s; watchdog #42940581820 age 4,870s / gap 13,950s; TCE WF-06 #42949191917 age 382s / gap 12,853s; TCE WF-12 #42944415193 age 2,908s / gap 13,126s. All six gaps fail; only TCE WF-06 current age passes. Watchdog runner-queue sample was below 15 minutes but does not provide scheduler enqueue/delivery telemetry.
- TCE native WF-06 #42949191917 and manual WF-06 #42949231253 failed strict HTTP 200 checks: TCE web, TCE API, Auth liveness and Auth readiness returned 503. WF-12 #42944415193 failed freshness. Preserve the strict health contract.
- Last-known K3s fallback #42942360712: node Ready/ARM64; disk 56% / ~20 GiB free; ~19 GiB RAM available; restart required. Media and MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1. Media runner remains active; retirement evidence incomplete. Snapshot expires at approximately 03:10:21Z if no newer inspection arrives.
- Keep the existing app-owned publisher workflows and Platform's single production apply authority. No app-owned direct SSH/Compose deploy authority was added. No workflow was confirmed redundant/obsolete. Do not change cron, freshness budgets or TCE market-scan schedule.


## Historical verification — 2026-11-11 10:55 ICT / 03:55:46 UTC

- Direct master refs: Platform `9848cdeb97a29ff3833378013f4932e6558cb933`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314/#544/#541/#539; Authentication #76; none in TCE/Stock/Media. Heads unchanged from the exact-head validation evidence recorded in the deployment tracker. All remain drafts/owner decisions.
- Latest workflow evidence: Platform master push validation #42950290166 PASS; TCE native WF-06 #42949191917 and manual #42949231253 failed four strict 503 probes; native WF-12 #42944415193 failed freshness; Stock CI #42610360402 PASS and scraper #42457182511 failed closed; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes have stale current-age and inter-arrival evidence at 03:55:46Z. Exact run IDs, ages, gaps and budgets are recorded in the deployment tracker. Do not count manual/workflow_run/repository_dispatch fallback receipts as native schedule delivery.
- Latest K3s snapshot #42942360712 is 7,225s old and exceeds the 4,500s freshness budget. Latest manual reconciliation #42949244537 is 3,636s old and exceeds its 2,700s budget. Prior GHCR/Secret/drift results are historical; no current rollout authorization is inferred.
- Preserve application-owned build/publish and Platform-only production apply boundaries. Stock/Media remain in guarded retirement scope; no republish, delete, runner retirement, credential rotation, host restart or DNS/database/storage mutation occurred. Preserve all useful workflows; none was confirmed redundant/obsolete. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Historical verification — 2026-11-11 12:04 ICT / 05:04:56 UTC

- Direct master refs: Platform Infra `bfa50827eacdb6675f718593c0b38cf693a38b01`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Current open PRs: Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. All remain drafts/owner decisions. Exact-head checks on those PRs are successful; Auth Supabase Preview is skipped. Do not merge owner-decision work without approval.
- Latest master CI: Platform validation #42956212725 PASS; TCE native WF-06 #42949191917 and manual #42949231253 fail all four strict public probes (HTTP 503 vs 200); WF-12 native #42944415193 fails freshness; Stock CI #42610360402 PASS and scraper #42457182511 fails closed on empty `VNSTOCK_API_KEY`; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes at 05:04:56Z: reconcile #42942147668 age 11,496s/gap 14,244s; inspection #42932368784 age 16,247s/gap 17,791s; recovery #42939222343 age 12,979s/gap 13,889s; watchdog #42940581820 age 12,303s/gap 13,950s; TCE WF-06 #42949191917 age 7,815s/gap 12,853s; TCE WF-12 #42944415193 age 10,341s/gap 13,126s. Every current-age and inter-arrival check exceeds its budget. Fallback receipts do not count.
- Latest K3s inspection #42942360712 is 11,375s old against 4,500s. Last manual reconciliation #42949244537 is 7,786s old against 2,700s. Both are stale; prior GHCR/Secret/drift results are historical and do not authorize rollout.
- Direct branch reads report `protected=false` for all five master branches. Repository metadata allows squash, merge commits and rebase on all five; administrator must confirm effective inherited rulesets and enforce squash-only/PR-only policy.
- App repositories retain ownership of CI/builds and immutable image publication. Platform remains the sole production apply authority. No new publication, promotion, apply, rollout, retirement, credential/DNS/database/storage mutation or host restart occurred. Preserve useful workflows; none was confirmed redundant/obsolete. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Post-checkpoint merge verification — 2026-11-11 12:08 ICT

- Platform master advanced documentation-only from `bfa50827...` to `0191e968d11a3b9096ddd24d46fa8daeb03fec3a` through PR #1614.
- Exact-head validation #42963714334 and post-merge validation #42963772141 both PASS.
- No production reconcile/recovery push run was triggered by the documentation-only merge. Workflow ownership and production authority boundaries are unchanged.


## Latest verification delta — 2026-11-11 12:58 ICT / 05:58:04 UTC

This checkpoint supersedes the 12:08 ICT compact readiness values above. It is based on direct Git refs, current open-PR metadata, first-page Actions run history (up to 100 runs per repository), exact-head workflow evidence for open PRs, and decoded job logs. Runtime evidence is explicitly freshness-bounded.

### Direct repository state and open PRs

- Direct `refs/heads/master` reads: Platform Infra `b88399f0b593f3e336db4d28b38d364c99215ce3`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform open PRs: #1314 head `db152c9a17416d1a7f82165597dfe478321bd055`; #544 `c95e7daecb83b65577b54303427fe4ea81adfe06`; #541 `b8f7c6ba04e3d971336a899b2efd5894662083b3`; #539 `2dc48b97017ecb08e49682633303a2f1d5e991a1`. Authentication open PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`. No open PRs in TCE, Stock or Media.
- Exact-head validations for those five PRs remain successful: #1314 run #42161859747; #544 #38575430454; #541 #38567431761; #539 #38548718033; Auth #76 #41329425940. Auth Supabase Preview is skipped. All five remain drafts/owner decisions; do not merge Keycloak/database/identity/migration decisions without owner approval.
- Platform PR #1614 merged at `0191e968d11a3b9096ddd24d46fa8daeb03fec3a`; PR #1615 merged at current master `b88399f0b593f3e336db4d28b38d364c99215ce3`. Their exact-head and post-merge validation runs passed.
- Latest Platform master run is [#42963960326](https://github.com/phanthienquoc/platform-infra/actions/runs/42963960326), `validate-manifests`, push on current master SHA, SUCCESS at 05:10:33Z. No later Platform run appears in the queried 100-run page.
- Latest app evidence in queried run history: TCE manual WF-06 #42949231253 failed; native WF-06 #42949191917 failed; native WF-12 #42944415193 failed. Stock CI #42610360402 passed; scraper schedule #42457182511 failed closed. Media CI #42539512417 passed. Authentication CI #42654579277 passed. These app runs are older than this checkpoint; no new image publication/digest handoff was observed.

### Native schedule freshness

Reference: 2026-11-11 05:58:04 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run and repository_dispatch receipts do not substitute.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 14684 | 14244 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 19435 | 17791 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 16167 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 15491 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 11003 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 13529 | 13126 | 1500 |

All six current-age and all six inter-arrival checks exceed their budgets. The latest Platform native reconcile/recovery/watchdog runs use pre-current-master SHA `b5fceb3e...`; native inspection uses `d89bcf7e...`. No native scheduled run has validated current Platform master `b88399f0...`. TCE schedule runs use current TCE master but fail health/freshness. Preserve all cron expressions, budgets and the TCE market-scan schedule.

### TCE endpoint evidence

- Manual WF-06 [#42949231253](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42949231253) contains four independent failed endpoint jobs. Decoded logs show TCE web `https://tce.mrcute.space/` = HTTP 503; TCE API `/api/health` = 503; Auth liveness `/api/health` = 503; Auth readiness `/api/ready` = 503. All expected HTTP 200. Curl completed with retries; this is an upstream health failure, not runner initialization. The response body was not surfaced, so root cause remains unproven. Keep strict HTTP 200 contracts; do not scale or promote without owner-approved immutable digest, rollback reference and recovery approval.

### Stock and Media

- Stock CI #42610360402 passed. Scraper schedule #42457182511 failed closed because `VNSTOCK_API_KEY` was empty; the credential gate stopped before dependency installation/ingestion. Do not place the key in Git/logs/chat. Stock remains in the approved retirement scope; do not publish/promote replacement images while that scope remains active without an owner decision.
- Media CI #42539512417 passed. Media remains in guarded retirement scope. Remote runner unregister, external DB/object-storage backup/retention and authoritative DNS/provider ownership are not verified.
- Preserve the Bound `k3s-debug/k3s-debug-logs` PVC. No namespace/PVC/PV deletion or runner retirement is authorized by this checkpoint.

### K3s and GitOps — stale evidence only

- Latest read-only inspection fallback [#42942360712](https://github.com/phanthienquoc/platform-infra/actions/runs/42942360712) is `workflow_dispatch`, created 01:55:12Z (age 14572s at reference); its embedded snapshot was generated 01:55:21Z (age 14563s), far beyond the 4500s inspection budget. Latest native inspection #42932368784 is 19435s old.
- Latest native reconciliation [#42942147668](https://github.com/phanthienquoc/platform-infra/actions/runs/42942147668) is 14684s old; last manual reconciliation #42949244537 is 10974s old, beyond the 2700s budget. Recovery receipt #42949413722 is 10881s old. These are historical, not current rollout authorization.
- Native reconciliation job logs show `mode=apply`, `target_app=all`, `allow_image_changes=false`; shared `ghcr-pull` was unchanged, managed MicroFE/TCE image-pull checks reported no failures, TCE release pairing matched `prod-v0.1.0-e75e338`, and GitOps drift was false. The idempotent manifest/credential reconciliation returned `patched (no change)` / `unchanged`; the subsequent drift gate skipped any further manifest apply. No image replacement or workload rollout is evidenced. Deployment lane summary explicitly classified Auth as intentional zero-replica maintenance, MicroFE as healthy, TCE as maintenance, and Keycloak as skipped. Stock remains outside the managed GHCR pull helper/active GitOps scope.
- Last-known inspection: ARM64 node `tce-k3s-01` Ready, K3s v1.36.3+k3s1, Ubuntu 22.04.5, disk 56% / about 20 GiB free, RAM about 19 GiB available, host restart required. Media/MicroFE were 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4` due no ARM64 platform descriptor; legacy Stock Backend/Frontend 1/1 without RepoDigest promotion evidence. Do not present this as live health.
- No fresh K3s snapshot or reconciliation was obtained in this run. Platform operator must run `inspect-vps.yml` read-only before any deployment decision. This does not authorize reboot, rollout or deletion.

### Branch governance and merge methods

- Direct `GET /branches/master` reports `protected=false` for all five repositories at this checkpoint.
- Repository metadata reports `allow_squash_merge=true`, `allow_merge_commit=true`, and `allow_rebase_merge=true` for all five repositories. Squash is available but merge-commit and rebase remain enabled, contrary to the intended squash-only standard.
- Branch-protection detail GET returns HTTP 403 for all five through the current integration. Effective inherited organization ruleset enforcement is therefore not positively established by this run.
- GitHub administrator must configure/confirm PR-only updates, required CI/deployment-contract checks, block force-push and deletion, disable merge-commit/rebase, and verify effective organization ruleset coverage. Continue dedicated branches, exact-head checks and expected-head squash merges until confirmed.

### Exact next actions and safety

1. Platform operator: run a fresh read-only `inspect-vps.yml`; do not reboot/upgrade the host or mutate production using stale receipts.
2. GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry for six lanes and enforce/confirm master protection plus squash-only merge settings.
3. TCE/Auth owners: diagnose four HTTP 503 endpoints and provide approved immutable release digest, rollback reference and explicit recovery approval.
4. Stock owner: decide whether scraper remains in service or stays in retirement scope; if retained, provision `VNSTOCK_API_KEY` only via Actions Secrets and run safe `preflight_only=true`.
5. Media/Platform owners: complete external backup/retention, DNS ownership and remote runner stop/disable/unregister evidence before guarded deletion.
6. Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new GHCR publication, digest promotion, effective production manifest change, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred in this checkpoint. Preserve all useful CI/test/security, release, backup, integration, manual and scheduled workflows; none is confirmed redundant/obsolete. Do not add direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 13:03 ICT

- PR #1616 squash merge SHA: `14e79f1c90f8390636f13a06a899c0de0ab85bd0`.
- Exact-head validation #42969674108 PASS; post-merge master validation #42969724857 PASS.
- Only `validate-manifests` ran after the docs-only merge. No production reconcile/recovery push run was triggered.
- App repositories remain CI/build/immutable-publication owners; Platform remains the only production apply authority.
- No workflow was removed; no SSH/Compose deployment authority added; TCE market-scan schedule unchanged.


## Latest operational evidence — 2026-11-11 14:03 ICT / 07:03:57 UTC

### Current repository refs and open PRs

- Platform Infra master `e6d6213ea5441622a314d1ccacfc3d5fe358fe40`; open PRs #1314/#544/#541/#539, all drafts/owner decisions. Exact-head `validate` checks PASS.
- TCE Dashboard master `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; no open PRs. WF-06 manual #42972014911 failed four strict HTTP 200 probes; native WF-06 #42949191917 and native WF-12 #42944415193 remain stale. WF-07 schedule #42971954835 succeeded but is not a health-lane substitute.
- StockDividend master `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; no open PRs. CI #42610360402 passed; scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was empty. Stock remains guarded retirement scope.
- Media Generation master `dcd698699c65ba6e73f6b43838975144777131c3`; no open PRs. CI #42539512417 passed; K3s backend/frontend are 1/1 and digest-pinned; dedicated runner service remains active/enabled.
- Authentication master `eab85fab32d7c9baef750c1fedbb93deb8c1333f`; open PR #76 is a draft migration-drift plan. Exact-head validate PASS and Supabase Preview skipped. Auth runtime remains intentional 0/0 maintenance.

### Current runtime/credential evidence

- Inspection #42972248777 is a read-only workflow_dispatch fallback generated 06:25:00Z; age 2,337s at reference, within the 4,500s budget. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 56% / ~20 GiB free, ~19 GiB RAM available, host restart required. Preserve the Bound debug PVC.
- Media and MicroFE core workloads 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1 without RepoDigest. Target Stock/Media namespaces have no PVC/PV claim or VolumeSnapshot references in read-only preflight; Media remote runner unregister, external backup/retention and DNS ownership remain unverified.
- Reconciliation #42972016233 age 2,464s at reference, within 2,700s budget. GHCR read preflight passed for five managed packages; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged. No managed image-pull failures; clean diff/drift; manifest apply, image replacement and rollout skipped. MicroFE healthy; TCE/Auth maintenance; Keycloak skipped.
- TCE/Auth/OIDC HTTP 503 results are consistent with zero-replica maintenance. Preserve strict HTTP 200 probes; never mark zero-replica maintenance as live healthy.

### Native schedule state

At 07:03:57Z, all six configured health/reconciliation lanes exceed current-age and inter-arrival budgets. Latest native runs: Platform reconcile #42942147668, inspection #42932368784, recovery #42939222343, watchdog #42940581820; TCE WF-06 #42949191917 and WF-12 #42944415193. Exact ages, gaps and budgets are in the deployment tracker. Do not count manual/workflow_run/repository_dispatch fallbacks as native delivery. Preserve all cron expressions and the TCE market-scan schedule.

### Workflow preservation and authority

No workflow was added or removed in this checkpoint. Keep CI, tests, security, app-owned immutable publication, release, backup, integration, manual and scheduled workflows. App repositories remain responsible for tests/builds and immutable GHCR publication; Platform remains the sole production manifest, shared credential, GitOps promotion/reconciliation, rollout and health authority. No duplicate direct SSH/Compose authority is permitted.


## Historical verification — 2026-11-11 15:35 ICT / 08:35:19 UTC

- Platform master `cfeb5dbf74a625f443d44141bd4c719f47ec60a3`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1624 squash-merged at `cfeb5dbf...`; exact-head #42987271290 PASS and post-merge master #42988178995 PASS. Post-merge run contains `validate-manifests` only; no production reconcile/recovery push was triggered.
- Open owner-decision PRs remain Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. Exact-head `validate` checks pass; Auth Supabase Preview skipped. Do not merge without owner approval.
- Platform native lanes: reconcile #42942147668, inspection #42981286761, recovery #42986496462, watchdog #42986833403. TCE health lanes: WF-06 #42949191917 and WF-12 #42944415193. All six inter-arrival budgets fail; three current-age budgets fail. Manual and workflow_run fallbacks do not count as native delivery.
- Freshness-bounded runtime evidence: inspection #42981286761 age 3245s / 4500s; manual reconciliation #42986517013 age 771s / 2700s; recovery #42986712253 age 683s / 2700s. Node Ready/ARM64; Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1 without RepoDigest. Preserve the Bound debug PVC.
- Reconciliation #42986517013: GHCR read preflight PASS, Auth runtime Secret verified with values suppressed, shared `ghcr-pull` unchanged, TCE image pairing PASS, drift=false, apply/image replacement/rollout skipped. Recovery #42986712253 avoided duplicate fallback dispatch.
- TCE manual WF-06 #42972014911 returned HTTP 503 on all four strict public probes while K3s reports TCE/Auth/Keycloak 0/0 maintenance. Keep HTTP 200 health contract; maintenance is not healthy.
- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; digest-pinned workloads running and runner still active. Auth CI #42654579277 PASS; Auth remains maintenance.
- Preserve app-owned tests/builds/immutable publishers and Platform-only production apply. No workflow removed, no direct SSH/Compose authority, no production mutation, no credential/DNS/database/storage change, no reboot. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 15:40 ICT / 08:40:35 UTC

- Platform master `8419328596b1a96340dd48fd439d08c77f04da38`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Auth `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1625 exact-head #42988772690 PASS and post-merge master #42988867666 PASS. Only `validate-manifests` ran after merge; no production reconciliation/recovery push was triggered.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 and Auth #76; none in TCE/Stock/Media. Exact-head `validate` checks pass; Auth Supabase Preview skipped.
- Six native schedule lanes: Platform reconcile #42942147668, inspection #42981286761, recovery #42986496462, watchdog #42986833403; TCE WF-06 #42949191917 and WF-12 #42944415193. All six inter-arrival gaps fail; three current-age budgets fail. Do not count manual or workflow_run fallbacks as native delivery.
- K3s inspection #42981286761 age 3561s / 4500s; manual reconciliation #42986517013 age 1087s / 2700s; recovery #42986712253 age 999s / 2700s. Node Ready/ARM64; Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1 without RepoDigest. Preserve the Bound debug PVC.
- Reconciliation: GHCR preflight PASS, Auth runtime Secret verified, shared `ghcr-pull` unchanged, TCE pairing PASS, drift=false, apply/image replacement/rollout skipped. Recovery avoided duplicate fallback dispatch.
- TCE strict HTTP 200 probes still returned 503 in the last manual WF-06 run while K3s shows zero replicas. Preserve strict health contract; maintenance is not healthy.
- Stock CI PASS; scraper fails closed on empty `VNSTOCK_API_KEY`. Media CI PASS; digest-pinned workloads running; runner still active. Auth CI PASS; Auth remains maintenance.
- Preserve app-owned tests/builds/immutable GHCR publication and Platform-only production apply. No workflow removed, no SSH/Compose authority, no production mutation, no credential/DNS/database/storage changes, no host reboot. TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-11 15:55 ICT / 08:55:27 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest relevant workflow evidence | Ownership / preserved lanes |
|---|---|---|---|
| Platform Infra | `4cb217722b77c190886cb2ce1c28fe26802bce19` | `validate-manifests` #42989295172 PASS on current master; native reconcile #42942147668, inspection #42981286761, recovery #42986496462, watchdog #42986833403. | Sole production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health authority. Preserve native schedules, manual reconciliation, recovery, watchdog, inspection, CI/contract validation, backup/cleanup and purposeful dispatch jobs. |
| TCE Dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | Native WF-06 #42949191917 FAIL; native WF-12 #42944415193 FAIL; latest manual WF-06 #42972014911 FAIL; WF-07 integration #42971954835 PASS; WF-07 backup #42924677977 PASS. | Owns application tests/builds and immutable image publication. Preserve WF-06 strict HTTP 200 probes, WF-12 freshness watchdog, WF-13 recovery, WF-07 integration and backup. Do not count integration/backup as health-lane substitutes. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; weekend scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty. | Owns app tests/builds/publication if service retention is approved. Keep scraper fail-closed; no secret in Git/logs/chat; no image publication while approved retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last K3s snapshot #42981286761 showed backend/frontend 1/1 with registry digest references and runner service/listener active. | Owns tests/builds/immutable publication. Preserve CI/release workflows. Runner retirement remains gated on remote unregister, backup/retention and DNS ownership. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; last reconciliation #42986517013 verified runtime Secret with values suppressed; Auth remains 0/0 maintenance. | Owns Auth tests/builds/immutable publication. Preserve CI, security and release contracts. Zero replicas and OIDC 503 are not live health. |

### Open PR and governance inventory

- Platform open drafts: #1314, #544, #541, #539. Authentication open draft: #76. No open PRs in TCE, Stock or Media.
- Exact-head checks: Platform drafts each `validate=success`; Auth #76 `validate=success`, Supabase Preview skipped. Keep all owner-decision drafts unmerged.
- All five master branches report `protected=false` and no required status checks; all five repository metadata records allow squash, merge commits and rebase. Effective inherited rulesets remain unverified. Administrator action is required; no repository setting was changed.
- No workflow was removed or added. No direct SSH/Compose deployment authority was introduced. TCE market-scan schedule and all existing cron expressions are unchanged.


## Post-merge workflow inventory receipt — 2026-11-11 16:00 ICT

- Platform master now `37a5624a325c570df0fc689b4f6ecde5f9bae89e` after docs-only PR #1627.
- Exact-head validation #42991422461 PASS; post-merge `validate-manifests` #42991499455 PASS.
- No reconcile/recovery push was triggered. Production apply authority remains Platform only; app repositories retain tests/builds/immutable GHCR publication ownership.
- Last K3s snapshot #42981286761 is expired; last successful reconciliation #42986517013 is within its age budget but ran on older SHA `8f95ddd872...`. Neither authorizes a new rollout against current master.
- Preserve CI/test/security, app publication, release, backup, integration, manual and scheduled jobs. No workflow removal/addition, no SSH/Compose authority, and no TCE market-scan schedule change.


## Latest workflow inventory verification — 2026-11-11 16:58 ICT / 09:58:55 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `e6b7156d191ff3ae9bcb8ff66f1b2a5259de331e` | Native reconcile #42993779924 SUCCESS (pre-merge SHA `c557b3f`); read-only inspection #42994074939 SUCCESS via workflow_dispatch and PR #1629 squash-merged; exact-head validation #42994322789 PASS; recovery #42996312662 SUCCESS; watchdog workflow_run #42996353169 SKIPPED. | Sole production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and health authority. Preserve native schedules, manual reconciliation, recovery, watchdog, inspection, CI/contract validation, backup/cleanup and purposeful dispatch jobs. |
| TCE Dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | Native WF-06 #42949191917 stale/failed; native WF-12 #42996293386 failed because WF-06 age was 399m; manual WF-06 #42996339882 failed four strict HTTP 200 probes (503); WF-13 #42996315416 recovery success. | Owns app tests/builds, immutable TCE/MicroFE GHCR publication, strict public health probes, backup and integration checks. Preserve WF-06/WF-12/WF-13, WF-07 backup/integration and release-gated publishers. Do not count fallback/integration/backup as native health delivery. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. K3s desired Stock Admin/Backend pods ImagePullBackOff; legacy Backend/Frontend 1/1. | Owns app tests/builds and native ARM64 immutable publication only if service retention is approved. Preserve fail-closed scraper and gated publisher; no secret in Git/logs/chat and no publication while retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; K3s backend/frontend 1/1 with registry digest references; dedicated Media runner service/listener active/enabled. | Owns tests/builds/immutable publication. Preserve CI/release workflows. Runner retirement remains gated on remote unregister, backup/retention and DNS ownership. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth remains 0/0 maintenance; runtime Secret provision/verification succeeded in #42993779924 with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release contracts. Zero replicas and OIDC/health 503 are not live health. |

### Open PR and governance inventory

- Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76; no open PRs in TCE, Stock or Media. Exact-head `validate` checks remain PASS on the unchanged heads; Auth Supabase Preview is skipped. Keep these drafts unmerged pending their stated owner decisions.
- All five direct `branches/master` API responses report `protected=false`, `protection.enabled=false`, and no required status checks (`enforcement_level=off`, empty contexts/checks). Repository settings allow squash, merge commits and rebase. Effective inherited organization ruleset evaluation remains a separate administrator task.
- No workflow was added or removed. Preserve app CI/tests/security, immutable publishers, backup, integration, manual/release and scheduled jobs. No direct SSH/Compose deployment authority. TCE market-scan schedule and all existing cron expressions remain unchanged.

### Freshness and production authority

- Six native cadence lanes all exceed inter-arrival budgets. Current-age budgets fail for Platform inspection/recovery/watchdog and TCE WF-06; Platform reconciliation and TCE WF-12 are still within current-age budgets at the 09:58:55Z reference. Do not count workflow_dispatch, workflow_run or repository_dispatch as native schedule delivery.
- Read-only K3s snapshot #42994074939 is 2,415s old / 4,500s budget. Native reconciliation #42993779924 is 2,550s old / 2,700s budget but ran on pre-merge SHA `c557b3f`, not current master `e6b7156d`. It found no drift and skipped apply/image replacement/rollout; Auth runtime Secret provision/verification succeeded, shared `ghcr-pull` remained unchanged.
- No new app image publication or digest promotion. No current-master production apply or workload rollout. Keep Platform `reconcile-vps.yml` as the single production apply authority; `inspect-vps.yml` remains read-only. No SSH/Compose authority in app repos.

## Post-merge workflow inventory receipt — 2026-11-11 16:58 ICT

- Platform master advanced documentation-only through PR #1630 to `1bd6ea38fcc4591da16422868ac03124704ea293`.
- Exact-head validation #43000595633 PASS; post-merge master validation #43000748526 PASS.
- Post-merge run contains `validate-manifests` only; no production reconcile/recovery push was triggered.
- The 16:58 operational snapshot remains the latest runtime/schedule evidence; this receipt updates only the Platform master SHA and validation provenance.
- Workflow ownership and production authority boundaries are unchanged. No workflow was added/removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.

## Latest verification — 2026-11-11 18:01 ICT / 11:01:52 UTC

### Current refs and workflow ownership

| Repository | Current master | Latest evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `ff401dadb1cac5b0647c1a4187fe171b2cfbc937` | Current-master manual reconcile #43003088695 SUCCESS; recovery #43003328970 SUCCESS; current-master manifest validation #43001011228 PASS. Native schedule lanes remain stale. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps reconciliation, rollout and health authority. Preserve native schedules, read-only inspection, manual plan/apply, recovery, watchdog, validation, backup and guarded operations. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | PR #1037 merged; exact-head WF-01P #43008284677, WF-02 #43008284672, WF-05 #43008284792, WF-08B #43008284695 PASS. Post-merge WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 queued/in progress. Native WF-06 #43003016447 failed four HTTP 200 probes with 503. | Owns tests/builds/immutable GHCR publication, strict public health probes, integration/backup and maintenance-aware recovery. WF-13 honors `TCE_MAINTENANCE_MODE=true` only to suppress redundant read-only fallback; WF-06/12 remain strict and scheduled. WF-01P runs the health-recovery contract validator. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Desired Stock Admin/Backend ImagePullBackOff; legacy Backend/Frontend 1/1. | Owns app tests/builds/native ARM64 immutable publication only if owner approves retention. Keep scraper fail-closed; no secret in Git/logs/chat and no image publication while retirement remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last partial K3s inventory showed backend/frontend 1/1 and runner active. Full inspection is stale. | Owns tests/builds/immutable publication. Preserve CI/release. Runner retirement remains gated on remote unregister, backup/retention and DNS ownership. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth is intentional 0/0 maintenance; runtime Secret provision/verification succeeded in #43003088695 with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release. Zero replicas and OIDC/health 503 are not live health. |

### Open PRs and branch governance

- Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. Exact-head validation runs remain PASS: #42161859747, #38575430454, #38567431761, #38548718033 and Auth #41329425940 (Supabase Preview skipped). TCE #1037 is merged; no open PRs remain in Stock or Media.
- Direct `branches/master` API responses still report `protected=false`, `protection.enabled=false`, and required status checks enforcement off/empty on all five repositories. Repository settings permit squash, merge commit and rebase. Administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.
- No workflow was removed or added in this checkpoint. App repositories own tests/builds/immutable publication; Platform remains sole production apply authority. No direct SSH/Compose authority. TCE market-scan schedule unchanged.

### TCE maintenance-aware recovery contract

- TCE PR #1037 merged at `5b425bdeab457e943bcecf1831836fc698e24394`. WF-13 now reads the repository Actions variable `TCE_MAINTENANCE_MODE`; `true` suppresses only the redundant read-only WF-06 fallback. It does not change WF-06 expected HTTP 200 status, WF-12 schedule monitoring or cron expressions.
- `scripts/validate-tce-health-recovery-contract.sh` is run by WF-01P and checks workflow YAML, both maintenance guards, four HTTP 200 endpoints and unchanged WF-06/WF-12 schedules. Exact-head PR validation passed.
- Repository variable value was not changed or verified. An authorized TCE repository administrator must set `TCE_MAINTENANCE_MODE=true` while zero-replica maintenance is intentional; unset/set false after reactivation.

### Runtime and schedule evidence

- Current-master reconciliation #43003088695 passed GHCR read preflight for five packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, verified TCE pairing `prod-v0.1.0-e75e338`, found drift=false and skipped manifest apply/image replacement/rollout. Its post-check pod inventory showed Media/MicroFE 1/1, TCE/Auth/Keycloak 0/0 maintenance, Stock Admin/desired Backend ImagePullBackOff and legacy Stock Backend/Frontend 1/1.
- Last full read-only inspection #42994074939 is older than the 4,500s budget. Partial node/pod output from #43003088695 is not a substitute for full disk/RAM/storage/runner inventory. Obtain a fresh inspect before any production decision.
- All six native schedule lanes exceed both current-age and inter-arrival budgets at 11:01:52Z. Do not count manual/workflow_run/repository_dispatch as native delivery. Keep every cron expression and TCE market-scan schedule unchanged.


## Post-merge workflow inventory receipt — 2026-11-11 18:05 ICT

- Platform master advanced documentation-only through PR #1632 to `c49bb0f1f1df71f403c64cc17fada8d4ab99bc31`.
- Exact-head `validate-manifests` #43008866804 PASS; post-merge master `validate-manifests` #43008949806 PASS.
- Only `validate-manifests` ran after the Platform docs-only merge; no production reconciliation/recovery push was triggered.
- TCE master `5b425bdeab457e943bcecf1831836fc698e24394`: post-merge WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 all PASS after PR #1037. No GHCR publication was triggered.
- The 18:01 ICT operational/schedule snapshot remains the latest runtime evidence; this receipt updates only current refs and validation provenance.
- Workflow ownership and production authority boundaries are unchanged. No workflow removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.


## Fresh K3s inspection inventory — 2026-11-11 18:09 ICT

- Inspection #42994074939 attempt 2 SUCCESS; snapshot generated 11:06:54Z and was 152s old at the 11:09:26Z reference. Inspection-only PR #1634 auto-squash-merged after exact-head validation #43009458775 PASS; current Platform master `388f96b7f7b0c97f461691b5862aff83b7d0b4f2`.
- Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Ubuntu 22.04.5; RAM 23Gi total/19Gi available; disk 45G/56% used/20G available; pressure normal. Host restart required; kernel/containerd/Docker updates pending. Do not reboot or clean images without approval.
- Platform and Media runner services active/enabled. Docker has 5.773GB reclaimable image data; no cleanup performed. Preserve `k3s-debug/k3s-debug-logs` PVC/PV (Bound, 1Gi, RWO, local-path).
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry digests. TCE/Auth/Keycloak are 0/0 maintenance, not healthy. Stock Admin (2) and desired Backend (1) remain ImagePullBackOff on tag `12d63b4` with no registry digest; legacy Backend/Frontend 1/1 have only local image IDs and are not promotion evidence.
- All six native schedule current-age/inter-arrival budgets fail. Manual inspection rerun is not native schedule evidence. TCE market-scan schedule unchanged.
- Platform #1632/#1633 validations and post-merge validations PASS; inspection PR #1634 exact-head validation PASS. TCE #1037 exact-head and post-merge checks PASS. No workflow removed, no SSH/Compose authority, Platform remains sole production apply authority.


## Latest workflow inventory verification — 2026-11-11 19:01 ICT / 12:01:39 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest workflow evidence | Ownership / preserved lanes |
|---|---|---|---|
| Platform Infra | `8da047c223a2c10b5e0dd6a08aa8770fbc7f92c1` | `validate-manifests` #43009993417 PASS. Native reconcile #42993779924 (schedule/success), inspection #42981286761 (schedule/success), recovery #42986496462 (schedule/success), watchdog #42986833403 (schedule/failure). | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and health verification. Preserve reconcile, read-only inspection, recovery, watchdog, manifest/contract validation, backup and guarded maintenance workflows. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | Master WF-01 #43008514423 PASS, WF-05 #43008514459 PASS, WF-02 #43008514481 PASS. Native WF-06 #43003016447 FAIL (four HTTP 503 probes); native WF-12 #42996293386 FAIL (WF-06 source stale, queue 0m). | Owns app tests/builds/immutable GHCR publication, strict public health probes, integration/backup and maintenance-aware recovery. Preserve WF-06 HTTP 200, WF-12 schedule watchdog, WF-13 maintenance-aware fallback, WF-07 integration/backup and release publishers. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scheduled scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty. | Owns app tests/builds/native ARM64 immutable publication only if retention is approved. Preserve fail-closed scraper and gated publisher; no secret in Git/logs/chat and no publication while retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last full K3s snapshot shows backend/frontend 1/1 with registry digest references; runner service/listener active. | Owns tests/builds/immutable publication. Preserve CI/release. Runner retirement requires remote unregister, backup/retention and DNS ownership evidence. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth remains 0/0 maintenance; Auth runtime Secret was provisioned/verified in historical reconciliation #43003088695 with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release. Zero replicas and OIDC/health 503 are not live health. |

### Open PRs and checks

- Platform open owner-decision drafts: #1314, #544, #541 and #539; TCE/Stock/Media have no open PRs; Authentication draft #76 remains open.
- Exact-head PR validation evidence: Platform #1314 #42161859747 PASS, #544 #38575430454 PASS, #541 #38567431761 PASS, #539 #38548718033 PASS; Auth #76 #41329425940 PASS (Supabase Preview skipped by design). Keep these drafts unmerged pending their documented owner decisions.
- Current master refs were read directly from `refs/heads/master`. Direct branch-protection GET returned 403 for all five repositories; repository metadata allows squash, merge commit and rebase. Do not claim effective inherited rulesets are absent; administrator verification is required.

### Schedule and runtime evidence

- At 12:01:39Z, all six native schedule lanes exceed both current-age and inter-arrival budgets. Latest run IDs/gaps: Platform reconcile #42993779924 / 26,585s; inspection #42981286761 / 25,617s; recovery #42986496462 / 24,822s; watchdog #42986833403 / 24,297s; TCE WF-06 #43003016447 / 26,842s; WF-12 #42996293386 / 26,503s. Do not count manual, push, `workflow_run` or `repository_dispatch` as native delivery.
- Watchdog logs confirm the four Platform schedule inter-arrival failures. WF-12 logs report WF-06 source #42949191917 age 399m and queue 0m. WF-06 logs confirm all four public endpoints returned 503 rather than the required 200.
- K3s snapshot #42994074939 was generated 11:06:54Z; age 3,285s / 4,500s budget at reference, expires 12:21:54Z. Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock desired Admin/Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1 without registry RepoDigest. Preserve the Bound debug PVC.
- Reconciliation #43003088695 succeeded on old SHA `ff401dad`, not current master `8da047c2`; it found no drift, verified GHCR read access and Auth runtime Secret, left shared `ghcr-pull` unchanged, and skipped apply/image replacement/rollout. It is older than the 20-minute recovery freshness window. Run current-master `reconcile-vps.yml` in `mode=plan` before any deployment decision.
- TCE `TCE_MAINTENANCE_MODE` Actions variable could not be read through the current connector; its value remains unverified. Keep WF-06 strict and WF-12 active. Do not change the TCE market-scan schedule.

### Authority and safety

- App repositories retain tests/builds and immutable GHCR publication. Platform Infra remains the only production manifest/credential/GitOps apply, rollout and health authority.
- No workflow removed or added, no direct SSH/Compose authority, no new image publication or digest promotion, no current-master production apply, no workload rollout, no namespace/PVC/PV deletion, no runner retirement, no credential rotation, no DNS/database/storage mutation and no host reboot.


## Post-merge workflow inventory receipt — 2026-11-11 19:09 ICT / 12:09:43 UTC

- Platform master is `815f87e14832d35970f3e43b8e9c309301b0fc81` after docs-only PR #1636 and corrective PR #1637. Exact-head validations #43017483631 and #43017776105 PASS; post-merge `validate-manifests` runs #43017580624 and #43017854916 PASS. Only manifest validation ran after both merges; no production reconcile/recovery push was triggered.
- PR #1637 corrected the three interval pairs by exact run timestamps: Platform reconcile #42942147668 → #42993779924 = 26,585s; TCE WF-06 #42949191917 → #43003016447 = 26,842s; TCE WF-12 #42944415193 → #42996293386 = 26,503s. The other Platform gaps remain inspection 25,617s, recovery 24,822s and watchdog 24,297s.
- No new native schedule run appeared by 12:09:43Z. All six current-age budgets and all six inter-arrival budgets remain failed. Do not count manual, push, `workflow_run` or `repository_dispatch` as native schedule delivery.
- K3s snapshot #42994074939 is 3,769s old / 4,500s budget at the reference, with 731s remaining. Platform operator must refresh read-only inspection before 12:21:54Z. Last reconciliation #43003088695 is 6,429s old and is on pre-current SHA `ff401dad`; run current-master `mode=plan` before any apply decision.
- Ownership boundaries unchanged: app repositories own tests/builds/immutable GHCR publication; Platform Infra alone owns production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health verification. No workflow removed/added, no SSH/Compose authority, no production mutation, and TCE market-scan schedule unchanged.
