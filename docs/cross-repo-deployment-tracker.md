# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 02:56 ICT (2026-11-10 19:56:40 UTC).

This is the compact current readiness view. Historical append-only content is preserved under `docs/archive/`; timestamped checkpoints remain under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | \`67732ddee261bd70a42f96735462761353e01fb4\` | #1314, #544, #541, #539 (owner-decision drafts) | Inspection PR #1596 merged; exact-head \`validate-manifests\` #42887430642 passed. Fresh K3s inspection #42887151366 and reconciliation #42887561360 are available. |
| phanthienquoc/TCE-dashboard | \`c4602be3b0a7b624bdb9cd41519cfc70a14d92ab\` | none | Manual WF-06 #42888337472 failed all four public probes at HTTP 503 (expected 200). Latest native WF-06 #42872071366 and WF-12 #42867304730 remain stale/failing. |
| phanthienquoc/stockdividend | \`b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61\` | none | Stock CI #42610360402 passed, including non-publishing ARM64 builds. Scraper #42457182511 failed closed because \`VNSTOCK_API_KEY\` was absent. No production publisher run or new digest. |
| phanthienquoc/media-generation | \`dcd698699c65ba6e73f6b43838975144777131c3\` | none | Media CI #42539512417 passed. Fresh inspection #42887151366 showed backend/frontend 1/1 with digest-pinned images; dedicated runner service/listener remains active. |
| phanthienquoc/phanthienquoc-authentication | \`eab85fab32d7c9baef750c1fedbb93deb8c1333f\` | #76 (draft / owner decision) | auth-service-ci #42654579277 passed. Auth runtime Secret was verified in reconciliation #42887561360 with values suppressed; Auth remains 0/0 maintenance, not live health. |

### Recent Platform changes

- PR #1595 merged as \`b629d406ae1199b0b279909da6dd801013af9261\`; exact-head #42881044656 and post-merge #42881164425 passed.
- PR #1596 merged as \`67732ddee261bd70a42f96735462761353e01fb4\` at 2026-11-10 19:39:50Z. It updates only \`debug/vps-latest.md\`. The inspection workflow created PR #1596 from run #42887151366; exact-head \`validate-manifests\` #42887430642 passed on head \`36f02e48982100fc7309215e5bc0ee43f6c20434\`. No post-merge \`validate-manifests\` run on the new master SHA was observed in the latest Actions history.
- PR #1594 merged as \`0b7adf163e306691d584bfa2b81260e07de81511\`; exact-head #42874425371 and post-merge #42874531654 passed.
- PR #1593 merged as \`c81ec47005f47963323b933153199a433301f830\`; exact-head #42873684350 and post-merge #42873912468 passed.
- PR #1592 merged as \`ec57bb3a67920a83f48a33959d7be484c48352fc\`; post-merge validation passed.
- PR #1590 was closed without merge because its branch was behind master and readiness data had become stale; checkpoint files were preserved.
- TCE PR #1036 remains merged as \`c4602be3b0a7b624bdb9cd41519cfc70a14d92ab\`; its regression contract requires exactly four approved public endpoints and HTTP 200.

Open owner-decision drafts remain: Platform #1314 (mail plan), #544 (Keycloak activation), #541 (Keycloak database plan), #539 (central identity architecture), and Authentication #76 (migration drift investigation). Do not merge these without the relevant owner decision and side-effect review. Legacy combined-status contexts are not a substitute for inspecting Actions check-runs.

## Native schedule freshness

Reference time: 2026-11-10 19:56:40 UTC (2026-11-11 02:56:40 ICT). Only first-attempt \`event=schedule\` runs on \`master\` count. Manual, push, pull_request, workflow_run and repository_dispatch events are not native schedule substitutes.

| Lane | Latest native run | Previous native run | Latest result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42854065227 | #42778829676 | success / 16:23:35 | 12785 | 30424 | 2700 |
| Platform inspection | #42887151366 | #42809278936 | success / 19:37:38 | 1142 | 28677 | 4500 |
| Platform recovery | #42848981485 | #42777251549 | success / 15:52:52 | 14628 | 29378 | 2700 |
| Platform watchdog | #42850178931 | #42777386082 | failure / 15:59:51 | 14209 | 29729 | 2700 |
| TCE WF-06 | #42872071366 | #42799497774 | failure / 18:08:09 | 6511 | 27554 | 1500 |
| TCE WF-12 | #42867304730 | #42795292155 | failure / 17:40:12 | 8188 | 27647 | 1500 |

At this reference, five of six current ages exceed budget; Platform inspection is the only lane currently within its age budget. All six inter-arrival gaps exceed their unchanged budgets. A recent manual run or a successful unrelated schedule does not reset these six lane measurements.

A separate TCE integration schedule, WF-07 #42888228034, succeeded at 19:44:10Z. This is useful evidence that some native TCE scheduled work executes, but it is not WF-06/WF-12 and does not satisfy their health or cadence contracts. Platform inspection #42887151366 also succeeded natively at 19:37:38Z.

Configured schedules remain unchanged:
- Platform reconcile: \`7,22,37,52 * * * *\`
- Platform inspection: \`2,32 * * * *\`
- Platform recovery: \`10,25,40,55 * * * *\`
- Platform watchdog: \`12,27,42,57 * * * *\`
- TCE WF-06: \`*/15 * * * *\`
- TCE WF-12: \`7,22,37,52 * * * *\`

Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497) — GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for the six schedule workflows. At 19:56:40Z, five current ages and all six inter-arrival gaps exceed budget. TCE WF-07 #42888228034 succeeded as a separate scheduled integration workflow; this shows schedule activity but does not satisfy WF-06/WF-12 or the Platform lanes.
2. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575) — branch API reports \`protected=false\` for \`master\` on all five repositories. Branch-protection detail GET returns HTTP 403 for all five. Repository rulesets GET returns \`[]\` for Platform, TCE, Media and Authentication; Stock rulesets GET returns HTTP 403 due plan limitation. Effective inherited organization ruleset coverage is not independently verified. Administrator must confirm and enforce PR-only/required-check/force-push protections.
3. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872) — latest TCE manual health run #42888337472 failed all four public probes at HTTP 503 (expected 200). The latest inspection #42887151366 still shows TCE/Auth/Keycloak zero-replica maintenance and public OIDC 503. Owners must diagnose runtime, provide approved immutable release digests and rollback references, and explicitly approve recovery. Keep HTTP 200 as the only healthy public response.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42) — scraper #42457182511 failed closed because \`VNSTOCK_API_KEY\` was absent. Stock owner must provision it through repository/organization secrets and run \`preflight_only=true\` before ingestion. Never put the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43) — Stock owner must approve a source release and explicitly enable the manual publication gate. Publisher source contract and ARM64 non-publishing CI builds are present, but no production publication/digest handoff exists. K3s still cannot pull historical \`12d63b4\` on ARM64. Never overwrite historical tags.
6. Media promotion remains blocked pending an authorized \`PLATFORM_INFRA_AUTOMATION_TOKEN\` and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Platform operator must obtain the next fresh read-only K3s inspection, then separate host maintenance/restart approval. Latest inspection reports \`restart_required: yes\` and multiple pending OS/container-runtime updates. TCE owner must verify the SSH host fingerprint before any SSH-based maintenance.
8. Registry administrator must verify GHCR server-side immutable-tag policy. Repository pre-push tag-absence guards and digest equality do not prove registry-side enforcement.

## Current runtime blockers

- Latest read-only K3s snapshot is [#42887151366](https://github.com/phanthienquoc/platform-infra/actions/runs/42887151366), generated at 2026-11-10 19:37:48Z. At the 19:56:40Z reference it is 1132s old, within the 4500s inspection budget. Treat it as a timestamped snapshot, not a continuous live feed.
- Node \`tce-k3s-01\` was Ready, ARM64, K3s v1.36.3+k3s1; disk usage 56% (~20 GiB free), available RAM ~19 GiB. Host reports \`restart_required: yes\`; multiple OS, kernel and container-runtime packages are upgradable. Restart/upgrade remains gated by explicit operator maintenance approval.
- Last-known Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. Media workloads use registry digest-pinned images. TCE frontend/service and Auth were intentional 0/0 maintenance; Keycloak was 0/0 and its diagnostic timed out. Zero replicas are not healthy service.
- Stock Admin has two 0/1 pods in \`ImagePullBackOff\` using \`admin:12d63b4\`. The desired Stock Backend image is \`backend:12d63b4\`; its new pod is 0/1 \`ImagePullBackOff\` with \`no match for platform in manifest\`. A legacy Backend pod remains 1/1 on \`backend:23b2878\`; the Frontend is 1/1 on \`user:23b2878\`. The two cached \`23b2878\` images have no RepoDigest in the snapshot, so local image IDs are not registry digest evidence.
- Both public Keycloak OIDC discovery probes returned HTTP 503; Keycloak was 0/0 and its diagnostic timed out. TCE service diagnostics section contained no recent diagnostic lines in this snapshot.
- Media runner service/listener remains active and enabled. GitHub runner registration is not inferred by host inspection; remote unregister, backup/retention and DNS ownership evidence remain required. The active Platform manifest tree has no retired Stock/Media namespace or image references, but cluster namespaces/workloads remain and decommission is incomplete.
- Latest reconciliation [#42887561360](https://github.com/phanthienquoc/platform-infra/actions/runs/42887561360) completed SUCCESS at 19:40:11Z (workflow_dispatch; not a native schedule). It verified Auth runtime Secret keys with values suppressed, left shared \`ghcr-pull\` Secrets unchanged in MicroFE/TCE namespaces, found no image-pull failures in MicroFE Auth/Shell/WS or TCE service/frontend, and verified TCE desired/live image tags match \`prod-v0.1.0-e75e338\`. GitOps drift was false; manifest apply and rollout were skipped. MicroFE active health passed; TCE/Auth were explicitly classified as intentional zero-replica maintenance; Keycloak was skipped. Stock image-pull failures remain outside the active Platform manifest scope.
- Latest manual TCE WF-06 [#42888337472](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42888337472) ran at 19:44:50Z and returned HTTP 503 on all four approved endpoints: TCE web, TCE API, Auth liveness and Auth readiness. Each endpoint still expects HTTP 200. This manual run is not native schedule acceptance.
- Latest native TCE WF-06 #42872071366 ran at 18:08:09Z and failed; WF-12 #42867304730 ran at 17:40:12Z and failed schedule freshness. Separate native TCE integration WF-07 #42888228034 succeeded at 19:44:10Z.
- Stock scraper schedule [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) remains failed closed because \`VNSTOCK_API_KEY\` was absent; no ingestion or image publication is claimed.
- GHCR server-side immutable-tag enforcement remains unverified. Stock publisher source contract and ARM64 non-publishing CI were inspected, but no new production digest exists to promote.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- \`reconcile-vps.yml\` remains the single production apply authority; \`inspect-vps.yml\` remains read-only.
- Latest reconciliation reported no GitOps drift and correctly skipped manifest apply/rollout. No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, shared credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
- Preserve useful CI/test/security workflows and purposeful manual/release/scheduled jobs. No workflow was removed or confirmed redundant/obsolete.
- TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only tracker preserved at `docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md`.
- Previous full append-only workflow inventory preserved at `docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md`.
- Timestamped deployment checkpoints: `docs/cross-repo-deployment-checkpoints/`.
- Workflow ownership and file inventory: `docs/cross-repo-workflow-inventory.md`.
- Schedule investigation: https://github.com/phanthienquoc/platform-infra/issues/1497
- TCE/Auth recovery: https://github.com/phanthienquoc/platform-infra/issues/872
- Branch governance: https://github.com/phanthienquoc/platform-infra/issues/1575
- Stock scraper credential: https://github.com/phanthienquoc/stockdividend/issues/42
- Stock ARM64 release: https://github.com/phanthienquoc/stockdividend/issues/43
