# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 04:59 ICT (2026-11-10 21:59:33 UTC).

This is the compact current readiness view. Historical append-only content is preserved under docs/archive; timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 925397ca9a4f6180450eed03d1e1da167bd50666 | #1314, #544, #541, #539 (draft / owner decision) | PR #1599 merged at 925397ca. Exact-head validate #42907375231 passed. Native reconciliation #42909757881 succeeded on current master; GitOps drift=false and apply/rollout skipped. |
| phanthienquoc/TCE-dashboard | c4602be3b0a7b624bdb9cd41519cfc70a14d92ab | none | Backend unit tests #42822853137 passed. Manual public health #42888337472 failed all four probes at HTTP 503 (expected 200). Latest native WF-06 #42872071366 and WF-12 #42867304730 failed. |
| phanthienquoc/stockdividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 passed all seven jobs, including non-publishing ARM64 builds and release-hold contract. Scraper schedule #42457182511 failed closed because VNSTOCK_API_KEY was absent. No production publisher run or digest handoff. |
| phanthienquoc/media-generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 passed. Inspection #42907109988 shows Media backend/frontend 1/1 and digest-pinned; dedicated runner service/listener remains active. |
| phanthienquoc/phanthienquoc-authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (draft / owner decision) | Auth CI #42654579277 passed; Supabase Preview intentionally skipped. Reconciliation #42909757881 verified Auth runtime Secret with values suppressed; Auth remains 0/0 maintenance, not live health. |

## Open PRs and exact-head checks

- Platform #1314: head db152c9a; validate PASS; draft mail-service plan remains owner decision.
- Platform #544: head c95e7dae; validate PASS; draft Keycloak activation status remains owner decision.
- Platform #541: head b8f7c6ba; validate PASS; draft Keycloak database change remains owner decision and side-effect gated.
- Platform #539: head 2dc48b97; validate PASS; draft central identity architecture remains owner decision.
- Authentication #76: head f19cacb0; validate PASS; Supabase Preview skipped; migration drift investigation remains owner decision.
- No open PRs in TCE, Stock or Media. Do not merge owner-decision drafts solely because CI passes.

## Recent Platform changes

- PR #1599 merged as 925397ca9a4f6180450eed03d1e1da167bd50666. It updates only debug/vps-latest.md from read-only inspection #42907109988. Exact-head validate-manifests run #42907375231 passed. No separate post-merge validate-manifests check-run was found; the subsequent native reconciliation #42909757881 ran on the new master SHA and succeeded.
- PR #1598 remains the prior readiness checkpoint merge at 518d6e1a08c2cde68e2ab7a24c4ca99a485fcb0d.
- Earlier compact tracker and workflow inventory history remains preserved in docs/archive and timestamped checkpoint directories.
- Current master refs were read directly for all five repositories before this checkpoint.

## Native schedule freshness

Reference time: 2026-11-10 21:59:33 UTC (2026-11-11 04:59:33 ICT). Only first-attempt event=schedule runs on master count. Manual, push, pull_request, workflow_run and repository_dispatch events are not native schedule substitutes.

| Lane | Latest native run | Previous native run | Latest result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42909757881 | #42854065227 | success / 21:55:56 | 217 | 19941 | 2700 |
| Platform inspection | #42887151366 | #42809278936 | success / 19:37:38 | 8515 | 28677 | 4500 |
| Platform recovery | #42906791198 | #42848981485 | success / 21:37:08 | 1345 | 20656 | 2700 |
| Platform watchdog | #42908417737 | #42850178931 | failure / 21:47:23 | 730 | 20852 | 2700 |
| TCE WF-06 | #42872071366 | #42799497774 | failure / 18:08:09 | 13884 | 27554 | 1500 |
| TCE WF-12 | #42867304730 | #42795292155 | failure / 17:40:12 | 15561 | 27647 | 1500 |

All six inter-arrival gaps exceed their unchanged budgets. Current-age budget is currently met by Platform reconcile, recovery and watchdog; native Platform inspection and both TCE health lanes remain stale. The successful native reconcile and recovery events do not erase their excessive inter-arrival gaps.

A separate read-only inspection fallback #42907109988 ran by workflow_dispatch and generated debug/vps-latest.md at 21:39:20Z. At this reference it is 1213s old, within the 4500s read-only evidence budget. This fallback is useful current operator evidence but does not reset native inspection schedule freshness.

Separate TCE integration schedule WF-07 #42888228034 succeeded at 19:44:10Z. It does not satisfy WF-06/WF-12 cadence or public health. TCE WF-12 workflow_run #42888256364 failed its freshness check; WF-13 fallback #42888287235 succeeded but is not a native schedule event.

Configured schedules remain unchanged:
- Platform reconcile: 7,22,37,52 * * * *
- Platform inspection: 2,32 * * * *
- Platform recovery: 10,25,40,55 * * * *
- Platform watchdog: 12,27,42,57 * * * *
- TCE WF-06: */15 * * * *
- TCE WF-12: 7,22,37,52 * * * *

Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current runtime evidence

- Latest read-only K3s snapshot is inspection fallback #42907109988, generated 2026-11-10 21:39:20Z. At the 21:59:33Z reference it is 1213s old and within the 4500s evidence budget. The latest native scheduled inspection remains #42887151366 and is stale.
- Node tce-k3s-01 was Ready, ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1 and containerd 2.3.2-k3s2. Disk usage was 56% (~20 GiB free), available RAM ~19 GiB, and restart_required=yes. Host maintenance/restart and OS/container-runtime upgrades remain gated by explicit operator approval.
- Last-known Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. Media image references were digest-pinned. TCE frontend/service, Auth and Keycloak were 0/0 maintenance; zero replicas are not healthy service. The Keycloak deployment lane was skipped in the latest reconciliation.
- Stock Admin had two 0/1 pods in ImagePullBackOff using admin:12d63b4. Desired Stock Backend was 0/1 ImagePullBackOff using backend:12d63b4 with no match for platform in manifest. Legacy Backend and Frontend remained 1/1 on tags 23b2878. The cached legacy Stock images had no RepoDigest, so local image IDs are not registry digest or promotion evidence.
- The snapshot reported no Stock/Media PVC or VolumeSnapshot references, but Stock workloads and namespaces still existed. This is not decommission completion and does not authorize namespace or workload deletion.
- Media runner service/listener remained active and enabled. Host inspection cannot prove remote GitHub runner registration state; remote unregister, backup/retention and DNS ownership evidence remain required.
- Native reconciliation #42909757881 completed SUCCESS at 21:55:56Z on master SHA 925397ca. Logs verified runner policy v15, GHCR read access for auth-service/auth, microfe-shell, microfe-ws, tce-dashboard/service and tce-dashboard/web, Auth runtime Secret keys with values suppressed, and unchanged shared ghcr-pull Secrets. No image-pull failures were found in the MicroFE Auth/Shell/WS or TCE service/frontend scopes. TCE desired/live images paired at prod-v0.1.0-e75e338. GitOps drift=false; manifest apply, image replacement and workload rollout were correctly skipped.
- Reconciliation observed the K3s node Ready and Stock Admin/desired Backend image-pull failures. MicroFE was active. TCE and Auth deployment lanes were explicitly classified as intentional zero-replica maintenance; their lane success does not assert live workload health.
- TCE manual health run #42888337472 returned HTTP 503 on all four approved endpoints: TCE web, TCE API, Auth liveness and Auth readiness. Each endpoint still requires HTTP 200. Do not weaken the health contract.
- Stock scraper #42457182511 failed closed before dependency installation because VNSTOCK_API_KEY was absent. No ingestion or production image publication is claimed.
- GHCR server-side immutable-tag enforcement remains unverified. App-side tag-absence guards, architecture checks and digest equality do not prove registry-side enforcement.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497): GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for all six schedule workflows. At 21:59:33Z all six inter-arrival gaps exceed budget; the native inspection lane and both TCE health lanes are also stale by age.
2. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872): TCE/Auth owners must diagnose HTTP 503 and provide approved immutable release digests, rollback references and explicit recovery approval. Platform operator must continue read-only inspection and obtain separate host maintenance approval before restart/upgrade.
3. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575): Last verified branch metadata reported protected=false for all five master branches; branch-protection detail GET returned 403 and effective inherited rulesets remain unverified. GitHub administrator must confirm PR-only, required checks, force-push and deletion protections.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42): Stock owner must provision VNSTOCK_API_KEY through repository/organization secrets and run preflight_only=true before ingestion. Never place the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43): Stock owner must approve a source release and explicitly enable the manual publisher gate. Native ARM64 publisher and non-publishing CI builds exist, but no production publication or digest handoff exists. Never overwrite historical tags.
6. Media promotion remains blocked pending an authorized PLATFORM_INFRA_AUTOMATION_TOKEN and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Registry administrator must verify GHCR server-side immutable-tag policy. TCE owner must verify SSH host fingerprint before any SSH-based maintenance.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- reconcile-vps.yml remains the single production apply authority; inspect-vps.yml remains read-only.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
- Preserve useful CI/test/security workflows and purposeful manual/release/scheduled jobs. No workflow was removed or confirmed redundant/obsolete.
- TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only tracker preserved at docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md.
- Previous full append-only workflow inventory preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md.
- Timestamped deployment checkpoints: docs/cross-repo-deployment-checkpoints/.
- Workflow ownership and file inventory: docs/cross-repo-workflow-inventory.md.
- Schedule investigation: https://github.com/phanthienquoc/platform-infra/issues/1497
- TCE/Auth recovery: https://github.com/phanthienquoc/platform-infra/issues/872
- Branch governance: https://github.com/phanthienquoc/platform-infra/issues/1575
- Stock scraper credential: https://github.com/phanthienquoc/stockdividend/issues/42
- Stock ARM64 release: https://github.com/phanthienquoc/stockdividend/issues/43
