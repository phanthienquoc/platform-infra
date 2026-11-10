# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 04:03 ICT (2026-11-10 21:03:30 UTC).

This is the compact current readiness view. Historical append-only content is preserved under `docs/archive/`; timestamped checkpoints remain under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `299bf14e1213b624e67d4f89c3ceb473fff8ddcf` | #1314, #544, #541, #539 (draft / owner decision) | PR #1597 merged; exact-head validation #42890936726 passed and post-merge validation #42891093718 passed on current master. |
| phanthienquoc/TCE-dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | none | Current-head health run #42888337472 failed all four public probes at HTTP 503; WF-12 schedule-delivery job #42888256364 failed. Backend unit tests #42822853137 passed. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Current-head CI #42610360402 passed, including non-publishing ARM64 builds. Scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. No production publisher run or digest handoff. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Current-head CI #42539512417 passed. Latest K3s inspection is now stale; the last snapshot showed backend/frontend 1/1 and an active dedicated runner. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft / owner decision) | Current-head auth-service-ci #42654579277 passed. Auth runtime Secret was verified in reconciliation #42887561360 with values suppressed; Auth remains 0/0 maintenance, not live health. |

### Recent Platform changes

- PR #1597 merged as `299bf14e1213b624e67d4f89c3ceb473fff8ddcf` at 2026-11-10 20:01:23Z. Exact-head `validate-manifests` #42890936726 passed on head `b944eb3195a6645e52b67d1748f174db51790768`; post-merge `validate-manifests` #42891093718 passed on the merge SHA.
- PR #1596 merged as `67732ddee261bd70a42f96735462761353e01fb4`; it updates only `debug/vps-latest.md`.
- PR #1595 merged as `b629d406ae1199b0b279909da6dd801013af9261`; exact-head and post-merge validations passed.
- PR #1594 merged as `0b7adf163e306691d584bfa2b81260e07de81511`; exact-head and post-merge validations passed.
- PR #1593 merged as `c81ec47005f47963323b933153199a433301f830`; exact-head and post-merge validations passed.
- PR #1592 merged as `ec57bb3a67920a83f48a33959d7be484c48352fc`; post-merge validation passed.
- PR #1590 was closed without merge because its branch was behind master and readiness evidence had become stale; checkpoint files were preserved.

Open owner-decision drafts remain: Platform #1314 (mail plan), #544 (Keycloak activation), #541 (Keycloak database), #539 (central identity architecture), and Authentication #76 (migration drift investigation). Their latest exposed PR-head checks are successful or intentionally skipped, but the drafts remain unmerged pending owner decisions and side-effect review. Do not merge them based on CI alone. Legacy combined-status contexts are not a substitute for inspecting Actions check-runs.

## Native schedule freshness

Reference time: 2026-11-10 21:03:30 UTC (2026-11-11 04:03:30 ICT). Only first-attempt `event=schedule` runs on `master` count. Manual, push, pull_request, workflow_run and repository_dispatch events are not native schedule substitutes.

| Lane | Latest native run | Previous native run | Latest result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42854065227 | #42778829676 | success / 16:23:35 | 16795 | 30424 | 2700 |
| Platform inspection | #42887151366 | #42809278936 | success / 19:37:38 | 5152 | 28677 | 4500 |
| Platform recovery | #42848981485 | #42777251549 | success / 15:52:52 | 18638 | 29378 | 2700 |
| Platform watchdog | #42850178931 | #42777386082 | failure / 15:59:51 | 18219 | 29729 | 2700 |
| TCE WF-06 | #42872071366 | #42799497774 | failure / 18:08:09 | 10521 | 27554 | 1500 |
| TCE WF-12 | #42867304730 | #42795292155 | failure / 17:40:12 | 12198 | 27647 | 1500 |

At this reference, all six current ages and all six inter-arrival gaps exceed their unchanged budgets. The latest inspection snapshot and latest reconciliation are also stale relative to their respective evidence budgets. A recent manual run or successful unrelated schedule does not reset these six lane measurements.

Separate TCE integration schedule WF-07 #42888228034 succeeded at 19:44:10Z. This confirms that a different TCE scheduled workflow executed; it does not satisfy WF-06/WF-12 cadence or public health. TCE WF-12 workflow_run #42888256364 failed its WF-06 freshness inspection, while its heartbeat dispatch step succeeded. WF-13 fallback #42888287235 succeeded but is not a native schedule event.

Configured schedules remain unchanged:
- Platform reconcile: `7,22,37,52 * * * *`
- Platform inspection: `2,32 * * * *`
- Platform recovery: `10,25,40,55 * * * *`
- Platform watchdog: `12,27,42,57 * * * *`
- TCE WF-06: `*/15 * * * *`
- TCE WF-12: `7,22,37,52 * * * *`

Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497) — GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for all six schedule workflows. At 21:03:30Z all six current ages and inter-arrival gaps exceed budget. TCE WF-07 #42888228034 succeeded as a separate scheduled integration workflow; it does not satisfy WF-06/WF-12 or Platform cadence.
2. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575) — branch API reports `protected=false` for `master` on all five repositories. Branch-protection detail GET returns HTTP 403. Repository rulesets GET returned `[]` for Platform, TCE, Media and Authentication; Stock rulesets GET returned HTTP 403 due plan limitation. Effective inherited organization ruleset coverage remains unverified. Administrator must confirm and enforce PR-only/required-check/force-push protections.
3. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872) — latest TCE manual health run #42888337472 failed all four public probes at HTTP 503 (expected 200). Latest K3s snapshot #42887151366 is stale and last showed TCE/Auth/Keycloak zero-replica maintenance plus public OIDC 503. Owners must diagnose runtime, provide approved immutable release digests and rollback references, and explicitly approve recovery. Keep HTTP 200 as the only healthy public response.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42) — scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. Stock owner must provision it through repository/organization secrets and run `preflight_only=true` before ingestion. Never put the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43) — Stock owner must approve a source release and explicitly enable the manual publication gate. Native ARM64 publisher and non-publishing CI builds exist, but no production publication/digest handoff exists. K3s last showed historical tag `12d63b4` failing ARM64 platform resolution. Never overwrite historical tags.
6. Media promotion remains blocked pending an authorized `PLATFORM_INFRA_AUTOMATION_TOKEN` and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Platform operator must obtain a fresh read-only K3s inspection; latest snapshot #42887151366 is 5142s old, beyond the 4500s inspection budget. Host maintenance/restart requires separate approval. TCE owner must verify the SSH host fingerprint before any SSH-based maintenance.
8. Registry administrator must verify GHCR server-side immutable-tag policy. Repository pre-push tag-absence guards and digest equality do not prove registry-side enforcement.

## Current runtime blockers

- Latest read-only K3s snapshot is [#42887151366](https://github.com/phanthienquoc/platform-infra/actions/runs/42887151366), generated at 2026-11-10 19:37:48Z. At the 21:03:30Z reference it is 5142s old, beyond the 4500s inspection budget. It is stale evidence, not a continuous live feed.
- Node `tce-k3s-01` was Ready, ARM64, Ubuntu 22.04.5 and K3s v1.36.3+k3s1; disk usage 56% (~20 GiB free), available RAM ~19 GiB. Host reported `restart_required: yes` and multiple OS/kernel/container-runtime packages upgradable. Restart/upgrade remains gated by explicit operator maintenance approval.
- Last-known Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. Media workloads were digest-pinned. TCE frontend/service and Auth were intentional 0/0 maintenance; Keycloak was 0/0 and its diagnostic timed out. Zero replicas are not healthy service.
- Stock Admin had two 0/1 pods in `ImagePullBackOff` using `admin:12d63b4`. The desired Stock Backend image was `backend:12d63b4`; its new pod was 0/1 `ImagePullBackOff` with `no match for platform in manifest`. A legacy Backend pod remained 1/1 on `backend:23b2878`; Frontend was 1/1 on `user:23b2878`. Cached `23b2878` images had no RepoDigest in the snapshot, so local image IDs are not registry digest evidence.
- Both public Keycloak OIDC discovery probes returned HTTP 503; Keycloak was 0/0 and its diagnostic timed out. TCE service diagnostics section contained no recent diagnostic lines in this snapshot.
- Media runner service/listener remained active and enabled. GitHub runner registration cannot be inferred from host inspection; remote unregister, backup/retention and DNS ownership evidence remain required. Active Platform manifests contain no retired Stock/Media namespace or image references, but cluster namespaces/workloads remain and decommission is incomplete.
- Latest reconciliation [#42887561360](https://github.com/phanthienquoc/platform-infra/actions/runs/42887561360) completed SUCCESS at 19:40:11Z via `workflow_dispatch` (not native schedule). At 21:03:30Z it is 4999s old, beyond the 2700s evidence budget. At execution it verified Auth runtime Secret keys with values suppressed, left shared `ghcr-pull` Secrets unchanged, found no image-pull failures in MicroFE Auth/Shell/WS or TCE service/frontend, and verified TCE desired/live tag pairing `prod-v0.1.0-e75e338`. GitOps drift was false; manifest apply and rollout were skipped. MicroFE active health passed; TCE/Auth were explicitly classified as intentional zero-replica maintenance; Keycloak was skipped.
- Latest manual TCE WF-06 [#42888337472](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42888337472) ran at 19:44:50Z and returned HTTP 503 on all four approved endpoints: TCE web, TCE API, Auth liveness and Auth readiness. Each endpoint still expects HTTP 200. The Auth liveness job log explicitly recorded HTTP 503 against expected 200. This manual run is not native schedule acceptance.
- Latest native TCE WF-06 #42872071366 ran at 18:08:09Z and failed; WF-12 #42867304730 ran at 17:40:12Z and failed schedule freshness. Separate native TCE WF-07 #42888228034 succeeded at 19:44:10Z; WF-12 workflow_run #42888256364 failed freshness and its heartbeat dispatch step succeeded. WF-13 fallback #42888287235 succeeded, but none of these is a WF-06/WF-12 native cadence substitute.
- Stock scraper schedule [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) remains failed closed because `VNSTOCK_API_KEY` was absent; no ingestion or image publication is claimed.
- GHCR server-side immutable-tag enforcement remains unverified. Stock publisher source contract and ARM64 non-publishing CI passed, but no production publication or digest handoff occurred.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the single production apply authority; `inspect-vps.yml` remains read-only.
- Latest known reconciliation reported no GitOps drift and correctly skipped manifest apply/rollout. No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, shared credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
- Preserve useful CI/test/security workflows and purposeful manual/release/scheduled jobs. No workflow was removed or confirmed redundant/obsolete.
- TCE market-scan schedule unchanged.

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
