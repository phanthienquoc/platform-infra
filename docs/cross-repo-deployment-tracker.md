# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 05:55 ICT (2026-11-10 22:55:22 UTC).

This is the compact current readiness view. Historical append-only content is preserved under docs/archive; timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 89b39427c78510cdcf30326a30737fe9bbe0f4c2 | #1314, #544, #541, #539 (draft / owner decision); #1601 (image-change provenance guard, validation pending) | PR #1600 merged at 89b394. Latest manual reconciliation #42915749236 succeeded on current master; GHCR preflight and Auth Secret verification passed, shared ghcr-pull unchanged, drift=false, apply/rollout skipped. |
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

- Direct Git ref read confirms Platform master `89b39427c78510cdcf30326a30737fe9bbe0f4c2`; the other four master refs remain TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3`, and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1600 is the latest merged readiness checkpoint at `89b39427c78510cdcf30326a30737fe9bbe0f4c2`; post-merge manifest validation #42911038235 passed.
- Latest manual reconciliation [#42915749236](https://github.com/phanthienquoc/platform-infra/actions/runs/42915749236) ran on current master at 22:34:05Z with `mode=apply`, `target_app=all`, and `ALLOW_IMAGE_CHANGES=false`. Logs verify five GHCR package reads, Auth runtime Secret provision/verification with values suppressed, unchanged shared `ghcr-pull`, no managed MicroFE/TCE image-pull failures, and TCE desired/live pairing. GitOps drift=false; production apply, image replacement and rollout were skipped.
- Reconciliation #42915749236 recorded the K3s node Ready and current workload inventory. Auth/TCE were explicitly classified as intentional zero-replica maintenance; MicroFE health passed; Keycloak was skipped. Stock Admin and desired Backend still had ImagePullBackOff pods.
- Recovery [#42915997996](https://github.com/phanthienquoc/platform-infra/actions/runs/42915997996) succeeded as workflow_dispatch, correlated to reconciliation #42915749236. It is not native schedule evidence.
- New PR [#1601](https://github.com/phanthienquoc/platform-infra/pull/1601) removes the manual image-change bypass and adds regression coverage. Until it merges, current master still contains the old manual input; do not use that input or manually bypass the image guard.
- Earlier checkpoint history remains preserved in docs/archive and timestamped checkpoint directories.

## Native schedule freshness

Reference time: 2026-11-10 22:55:22 UTC (2026-11-11 05:55:22 ICT). Only first-attempt event=schedule runs on master count. Manual, push, pull_request, workflow_run and repository_dispatch events are not native schedule substitutes.

| Lane | Latest native run | Previous native run | Latest result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42909757881 | #42854065227 | success / 21:55:56 | 3566 | 19941 | 2700 |
| Platform inspection | #42887151366 | #42809278936 | success / 19:37:38 | 11864 | 28677 | 4500 |
| Platform recovery | #42906791198 | #42848981485 | success / 21:37:08 | 4694 | 20656 | 2700 |
| Platform watchdog | #42908417737 | #42850178931 | failure / 21:47:23 | 4079 | 20852 | 2700 |
| TCE WF-06 | #42872071366 | #42799497774 | failure / 18:08:09 | 17233 | 27554 | 1500 |
| TCE WF-12 | #42915709227 | #42867304730 | failure / 22:33:49 | 1293 | 17617 | 1500 |

All six inter-arrival gaps exceed their unchanged budgets. Five of six current-age budgets are exceeded; TCE WF-12 is only 1293s old but its run failed because native WF-06 is stale. Platform watchdog #42908417737 reports the four Platform inter-arrival failures and TCE WF-06/WF-12 warnings.

TCE WF-12 #42915709227 successfully dispatched its authenticated heartbeat; Platform receiver #42915725335 accepted it. The heartbeat/receiver pair is not a substitute for a native WF-06 schedule. WF-12 logs report the latest native WF-06 #42872071366 was 15940s old at its 22:33:55Z reference, beyond the 25-minute budget.

TCE manual health run [#42915762180](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42915762180) failed all four approved endpoints at HTTP 503 against expected HTTP 200. It is workflow_dispatch, not native schedule evidence.

A manual Platform reconcile and its recovery are useful fallback evidence but do not reset native schedule freshness. Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

Configured schedules remain unchanged:
- Platform reconcile: 7,22,37,52 * * * *
- Platform inspection: 2,32 * * * *
- Platform recovery: 10,25,40,55 * * * *
- Platform watchdog: 12,27,42,57 * * * *
- TCE WF-06: */15 * * * *
- TCE WF-12: 7,22,37,52 * * * *

Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current runtime blockers

- Latest full read-only host inspection fallback #42907109988 generated `debug/vps-latest.md` at 21:39:20Z. At the 22:55:22Z reference it is 4562s old, just beyond the 4500s budget; its disk/RAM/restart measurements are stale and cannot authorize maintenance or reboot.
- More recent workload/node evidence comes from reconciliation #42915749236 at 22:34:27Z (1255s old at this reference): `tce-k3s-01` was Ready, ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2. This reconcile log does not provide fresh disk/RAM measurements.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. TCE frontend/service and Auth were 0/0 intentional maintenance; Keycloak lane was skipped. Zero replicas are not live service health.
- Stock Admin had two 0/1 ImagePullBackOff pods; desired Stock Backend had one 0/1 ImagePullBackOff pod. Legacy Backend and Frontend remained 1/1. The historical `12d63b4` image-platform mismatch remains unresolved; shared GHCR read access is not the cause. Do not promote cached local image IDs without RepoDigest evidence.
- Reconciliation #42915749236 verified GHCR read access for `auth-service/auth`, `microfe-shell`, `microfe-ws`, `tce-dashboard/service` and `tce-dashboard/web`. Auth runtime Secret was provisioned and verified with values suppressed; shared `ghcr-pull` remained unchanged. Managed MicroFE/TCE image-pull helpers reported no failures. TCE desired/live images paired at `prod-v0.1.0-e75e338`. GitOps drift=false; manifest apply, image replacement and workload rollout were correctly skipped.
- TCE manual WF-06 #42915762180 returned HTTP 503 for TCE web, TCE API, Auth liveness and Auth readiness; every endpoint still requires HTTP 200. WF-12 #42915709227 failed because the latest native WF-06 delivery was stale.
- Stock scraper #42457182511 failed closed before dependencies/ingestion because repository secret `VNSTOCK_API_KEY` was empty. No scraper ingestion or production image publication is claimed.
- Media runner service/listener remains active. Remote GitHub runner unregister, backup/retention and authoritative DNS ownership are not proven. Previous PVC/VolumeSnapshot observations are stale; no decommission or deletion is authorized.
- GHCR server-side immutable-tag enforcement remains unverified. App-side tag-absence guards, architecture checks and digest equality do not prove registry-side enforcement.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497): GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for all six schedule workflows. At 22:55:22Z all six inter-arrival gaps exceed budget; five lanes exceed current-age budgets and WF-12 failed because WF-06 is stale.
2. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872): TCE/Auth owners must diagnose HTTP 503 and provide approved immutable release digests, rollback references and explicit recovery approval. Platform operator must continue read-only inspection and obtain separate host maintenance approval before restart/upgrade.
3. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575): Last verified branch metadata reported protected=false for all five master branches; branch-protection detail GET returned 403 and effective inherited rulesets remain unverified. GitHub administrator must confirm PR-only, required checks, force-push and deletion protections.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42): Stock owner must provision VNSTOCK_API_KEY through repository/organization secrets and run preflight_only=true before ingestion. Never place the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43): Stock owner must approve a source release and explicitly enable the manual publisher gate. Native ARM64 publisher and non-publishing CI builds exist, but no production publication or digest handoff exists. Never overwrite historical tags.
6. Media promotion remains blocked pending an authorized PLATFORM_INFRA_AUTOMATION_TOKEN and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Registry administrator must verify GHCR server-side immutable-tag policy. TCE owner must verify SSH host fingerprint before any SSH-based maintenance.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the single production apply authority; `inspect-vps.yml` remains read-only.
- PR #1601 proposes removing the manual `allow_image_changes` input. On current master, the old input still exists until that PR passes exact-head checks and merges. Do not use it. After merge, only the provenance-verified `gitops-promoted-ready` repository dispatch can bypass the workload image guard; manual/scheduled/push reconciliation remains image-guarded.
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
