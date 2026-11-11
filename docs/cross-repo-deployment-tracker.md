# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 07:02 ICT (2026-11-11 00:02:43 UTC).

This is the compact current readiness view. Historical append-only content is preserved under docs/archive; timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `ad54469d6cf0d2c3362d6105f50fa9131dadf8a5` | #1314, #544, #541, #539 (all draft / owner decision) | PR #1604 merged at `ad54469d`; exact-head #42921837403 and post-merge #42921972012 passed. Latest recovery receipt #42922588369 was repository_dispatch, not native schedule. |
| phanthienquoc/TCE-dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | none | Native WF-06 #42922537816 failed public HTTP 200 contract (Auth readiness observed 503; all four endpoint jobs failed). Native WF-12 #42915709227 failed freshness. Separate scheduled WF-07 backup #42924677977 passed; it does not satisfy WF-06/WF-12 cadence. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 passed, including non-publishing ARM64 builds and release-hold contract. Scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. No production publisher run or digest handoff. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 passed. Inspection #42920320410 shows backend/frontend 1/1 with registry-resolved digest evidence; Media runner service/listener remains active. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft / owner decision) | Auth CI #42654579277 passed; Supabase Preview intentionally skipped. Inspection #42920320410 shows Auth 0/0 maintenance and public OIDC HTTP 503; this is not live health at the current reference. |

## Open PRs and exact-head checks

- Platform #1314: head `db152c9a17416d1a7f82165597dfe478321bd055`; `validate` PASS; draft managed-mail plan remains owner decision.
- Platform #544: head `c95e7daecb83b65577b54303427fe4ea81adfe06`; `validate` PASS; Keycloak activation remains secret/DNS/owner gated.
- Platform #541: head `b8f7c6ba04e3d971336a899b2efd5894662083b3`; `validate` PASS; Keycloak database plan remains owner decision; no DB mutation.
- Platform #539: head `2dc48b97017ecb08e49682633303a2f1d5e991a1`; `validate` PASS; identity architecture remains an unapproved draft.
- Authentication #76: head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; `validate` PASS; Supabase Preview skipped; migration drift plan remains owner decision.
- No open PRs in TCE, Stock or Media. All listed PRs remain drafts; do not merge owner-decision work solely because checks pass.

## Recent Platform changes

- Direct Git ref reads confirm current master SHAs: Platform `ad54469d6cf0d2c3362d6105f50fa9131dadf8a5`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1601 merged at `72ed11ef`, removing manual `allow_image_changes`. Its historical push reconciliation #42920184478 misclassified Keycloak README and executed the narrow Auth/Keycloak scale-to-zero action; no pre-scale replica snapshot was captured, so the exact state transition is unknown.
- PR #1602 merged at `8b11d662`, adding read-only inspection evidence #42920320410.
- PR #1603 merged at `98bc3d8c`, excluding recursive Keycloak Markdown from reconcile/recovery push triggers and making resolver-only changes fail closed. Exact-head checks #42921447020, #42921447003 and #42921446835 passed; post-merge #42921556638, #42921556488 and #42921556572 passed. No reconcile/recovery push run was created by this merge.
- PR #1604 merged at `ad54469d`, refreshing tracker/inventory. Exact-head #42921837403 and post-merge #42921972012 passed.
- Latest Platform recovery receipt [#42922588369](https://github.com/phanthienquoc/platform-infra/actions/runs/42922588369) was `repository_dispatch`, source TCE WF-06 #42922537816. Logs verified the source heartbeat; reconcile fallback was skipped because #42920184478 was only 15 minutes old at recovery time. A read-only inspection fallback was dispatched and correlated to #42920320410. This is not a native schedule delivery and did not prove a new reconciliation.
- Current Platform master is `ad54469d`; latest post-merge manifest validation #42921972012 passed. Later #42922638144 was a skipped `workflow_run` recovery event, not a deployment.

## Native schedule freshness

Reference time: 2026-11-11 00:02:43 UTC (07:02:43 ICT). Only first-attempt `event=schedule` runs on master count for cadence acceptance.

| Lane | Latest native run | Previous native run | Latest created UTC | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42909757881 | #42854065227 | 2026-11-10 21:55:56 | 7607 | 19941 | 2700 |
| Platform inspection | #42887151366 | #42809278936 | 2026-11-10 19:37:38 | 15905 | 28677 | 4500 |
| Platform recovery | #42906791198 | #42848981485 | 2026-11-10 21:37:08 | 8735 | 20656 | 2700 |
| Platform watchdog | #42908417737 | #42850178931 | 2026-11-10 21:47:23 | 8120 | 20852 | 2700 |
| TCE WF-06 | #42922537816 | #42872071366 | 2026-11-10 23:20:28 | 2535 | 18739 | 1500 |
| TCE WF-12 | #42915709227 | #42867304730 | 2026-11-10 22:33:49 | 5334 | 17617 | 1500 |

All six current-age and inter-arrival budgets are exceeded. TCE WF-06 #42922537816 failed its strict HTTP 200 contract; WF-12 #42915709227 failed freshness. TCE WF-07 backup #42924677977 succeeded at 23:35:49Z but is a separate workflow and does not satisfy WF-06/WF-12 cadence. Heartbeats, workflow_run recovery and workflow_dispatch/repository_dispatch fallbacks do not substitute for native schedule delivery.

The six cron expressions were re-read from the current workflow files and remain unchanged. Do not change cron, freshness budgets or TCE market-scan scheduling to hide delivery gaps.

## Current runtime blockers

- Fresh full read-only K3s inspection [#42920320410](https://github.com/phanthienquoc/platform-infra/actions/runs/42920320410) generated `debug/vps-latest.md` at 2026-11-10 23:05:16Z; age 3447s at the current reference, within the 4500s budget (about 17m33s remaining).
- Host: ARM64 Ubuntu 22.04.5, uptime 193 days, RAM 23 GiB total / 19 GiB available, root disk 45 GiB with 20 GiB free (56% used), `restart_required=yes`. Kernel/containerd/Docker and other package updates are available; no restart or package upgrade was performed.
- K3s node `tce-k3s-01` Ready, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Media backend/frontend 1/1 and digest-pinned; MicroFE Shell/WS/NATS 1/1. TCE frontend/service 0/0; Auth and Keycloak 0/0. Public OIDC discovery for both realms returns HTTP 503 in this snapshot.
- Stock Admin has two 0/1 ImagePullBackOff pods; desired Backend has one 0/1 ImagePullBackOff pod on historical tag `12d63b4`, kubelet reports `no match for platform in manifest`. Legacy Backend and Frontend remain 1/1 on `23b2878`; their cached image IDs do not provide registry RepoDigest evidence.
- Media runner service/listener active and enabled. Remote GitHub runner unregister, backup/retention and authoritative DNS ownership remain unverified.
- Storage preflight is `storage-clean`: no Stock/Media PVC or VolumeSnapshot references; separate `k3s-debug/k3s-debug-logs` PVC remains bound. This does not authorize namespace or workload deletion.
- Last reconcile workflow run [#42920184478](https://github.com/phanthienquoc/platform-infra/actions/runs/42920184478) was a push event at 23:04:13Z, last activity 23:04:57Z; age 3466s at this reference, beyond the 2700s reconciliation budget. It is the historical Keycloak README-triggered side-effect run; PR #1603 subsequently fixed the path/resolver guard. No newer reconciliation apply is evidenced.
- Manual reconciliation [#42915749236](https://github.com/phanthienquoc/platform-infra/actions/runs/42915749236) at 22:34:05Z succeeded with GHCR preflight, Auth runtime Secret verified (values suppressed), shared `ghcr-pull` unchanged, GitOps drift=false and apply/image replacement/rollout skipped. It is now stale (5318s old).
- Recovery [#42922588369](https://github.com/phanthienquoc/platform-infra/actions/runs/42922588369) at 23:20:48Z succeeded as `repository_dispatch`; it did not create a new reconcile run. It dispatched the read-only inspection fallback #42920320410.
- GHCR server-side immutable-tag enforcement remains unverified. Repository-level tag-absence guards and digest equality do not prove registry-side enforcement.
- Stock scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was empty. No Stock production image publication or digest handoff exists.
- TCE native WF-06 #42922537816 failed all four endpoint jobs against required HTTP 200; Auth readiness log explicitly observed HTTP 503. TCE WF-12 #42915709227 failed due stale native WF-06 evidence.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497): GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for all six schedule workflows. At 00:02:43Z all six current-age and inter-arrival gaps exceed budget.
2. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872): TCE/Auth owners must diagnose HTTP 503 and provide approved immutable release digests, rollback references and explicit recovery approval. Platform operator must run a fresh read-only inspection before the current snapshot expires and obtain separate host maintenance approval before restart/upgrade.
3. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575): Branch-protection detail GET returned 403 on all five repositories. Repository rulesets GET returned `[]` for four public repositories; private Stock rulesets GET returned 403 with a plan limitation. Effective inherited organization rulesets remain unverified. GitHub administrator must confirm PR-only, required checks, force-push and deletion protections.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42): Stock owner must provision `VNSTOCK_API_KEY` through repository/organization secrets and run `preflight_only=true` before ingestion. Never place the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43): Stock owner must approve a source release and explicitly enable the manual publisher gate. Native ARM64 publisher and non-publishing CI builds exist, but no production publication or digest handoff exists. Never overwrite historical tags.
6. Media promotion remains blocked pending an authorized `PLATFORM_INFRA_AUTOMATION_TOKEN` and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Registry administrator must verify GHCR server-side immutable-tag policy. TCE owner must verify SSH host fingerprint before any SSH-based maintenance.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the single production apply authority; `inspect-vps.yml` remains read-only. The current master workflow files retain the original cron expressions.
- PR #1601 is merged at `72ed11ef`; manual `allow_image_changes` input is removed. Only provenance-verified `gitops-promoted-ready` repository_dispatch may bypass the workload image guard.
- PR #1603 is merged at `98bc3d8c`; recursive Keycloak Markdown is excluded from reconcile/recovery push triggers and resolver-only edits fail closed. The earlier push run #42920184478 did execute the narrow Auth/Keycloak scale-to-zero command after README misclassification; pre-scale replica state was not captured. The regression is guarded, and no subsequent reconcile/recovery push run was created by PR #1603/#1604.
- PR #1604 is merged at `ad54469d`; exact-head and post-merge manifest validation passed.
- No new image publication, digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this update.
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
