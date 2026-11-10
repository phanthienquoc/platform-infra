# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 01:58 ICT (2026-11-10 18:58:22 UTC).

This is the compact current readiness view. Historical append-only content is preserved under `docs/archive/`; timestamped checkpoints remain under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `0b7adf163e306691d584bfa2b81260e07de81511` | #1314, #544, #541, #539 (owner-decision drafts) | PR #1594 merged; exact-head `validate-manifests` #42874425371 and post-merge #42874531654 passed. Latest reconciliation #42872159201 and K3s inspection #42863102352 are now stale. |
| phanthienquoc/TCE-dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | none | Latest native WF-06 #42872071366 failed all four public HTTP 200 probes (each returned 503); WF-12 #42867304730 failed/stale. WF-02/WF-05 previously passed. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Stock CI #42610360402 passed, including non-publishing ARM64 builds. Scraper schedule #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. No production publisher run or new digest. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Media CI #42539512417 passed. Last K3s inspection #42863102352 showed backend/frontend 1/1, but the snapshot is stale; Media runner service/listener was active in that snapshot. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft / owner decision) | auth-service-ci #42654579277 passed. Auth runtime Secret was provisioned/verified in reconciliation #42872159201 with values suppressed; Auth remains 0/0 maintenance, not live health. |

### Recent Platform changes

- PR #1592 merged as `ec57bb3a67920a83f48a33959d7be484c48352fc`; post-merge validation passed.
- PR #1593 merged as `c81ec47005f47963323b933153199a433301f830`; exact-head #42873684350 and post-merge #42873912468 passed.
- PR #1594 merged as `0b7adf163e306691d584bfa2b81260e07de81511`; exact-head #42874425371 and post-merge #42874531654 passed. Current Platform master is this SHA.
- PR #1590 was closed without merge because its branch was behind master and readiness data had become stale; its checkpoint files were preserved in PR #1592.
- TCE PR #1036 remains merged as `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; its regression contract requires exactly four approved public endpoints and HTTP 200.

Open owner-decision drafts remain: Platform #1314 (mail plan), #544 (Keycloak activation), #541 (Keycloak database plan), #539 (central identity architecture), and Authentication #76 (migration drift investigation). Do not merge these without the relevant owner decision and side-effect review. Their combined-status status-context endpoints returned no legacy statuses; this is not proof that required check-runs passed or that the drafts are merge-ready.

## Native schedule freshness

Reference time: 2026-11-10 18:58:22 UTC (2026-11-11 01:58:22 ICT). Only first-attempt `event=schedule` runs on `master` count. Manual, push, pull_request, workflow_run and repository_dispatch events are not native schedule substitutes.

| Lane | Latest native run | Result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile | #42854065227 | success / 16:23:35 | 9287 | 30424 | 2700 |
| Platform inspection | #42809278936 | success / 11:39:41 | 26321 | 29694 | 4500 |
| Platform recovery | #42848981485 | success / 15:52:52 | 11130 | 29378 | 2700 |
| Platform watchdog | #42850178931 | failure / 15:59:51 | 10711 | 29729 | 2700 |
| TCE WF-06 | #42872071366 | failure / 18:08:09 | 3013 | 27554 | 1500 |
| TCE WF-12 | #42867304730 | failure / 17:40:12 | 4690 | 27647 | 1500 |

All six current ages and all six inter-arrival gaps exceed their unchanged budgets. The newest native Platform reconcile is 9287s old against 2700s; the newest K3s inspection is 26321s old against 4500s. TCE WF-06 is 3013s old against 1500s and WF-12 is 4690s old against 1500s.

The most recent native schedule event in each lane is unchanged since the previous checkpoint. Platform reconcile #42854065227 ran at 16:23:35Z; inspection #42809278936 at 11:39:41Z; recovery #42848981485 at 15:52:52Z; watchdog #42850178931 at 15:59:51Z. TCE WF-06 #42872071366 ran at 18:08:09Z and WF-12 #42867304730 at 17:40:12Z. The latest TCE WF-06 run failed all four approved HTTP 200 probes.

Configured schedules remain unchanged:
- Platform reconcile: `7,22,37,52 * * * *`
- Platform inspection: `2,32 * * * *`
- Platform recovery: `10,25,40,55 * * * *`
- Platform watchdog: `12,27,42,57 * * * *`
- TCE WF-06: `*/15 * * * *`
- TCE WF-12: `7,22,37,52 * * * *`

Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497) — GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for the six schedule workflows. At 18:58:22Z all six current ages and inter-arrival gaps exceed budget. Repository run history alone cannot distinguish scheduler delay, enqueue failure, dropped event or runner delivery failure.
2. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575) — branch metadata previously reported `protected=false` on all five master branches. Effective required-check/PR-only enforcement is not verified; administrator must confirm inherited ruleset coverage and branch policy.
3. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872) — TCE/Auth owners must diagnose HTTP 503 and Keycloak/OIDC, provide approved immutable release digests and rollback references, and explicitly approve recovery. Keep HTTP 200 as the only healthy public response. TCE/Auth/Keycloak zero replicas are intentional maintenance, not healthy service.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42) — latest observed scraper schedule #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. Stock owner must provision it through repository/organization secrets and run `preflight_only=true` before ingestion. Never put the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43) — Stock owner must approve a source release and explicitly enable the manual publication gate. The publisher contract and ARM64 non-publishing CI builds are present, but no production publication/digest handoff exists. Never overwrite historical tag `12d63b4`.
6. Media promotion remains blocked pending an authorized `PLATFORM_INFRA_AUTOMATION_TOKEN` and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Platform operator must obtain a fresh read-only K3s inspection, then separate host maintenance/restart approval. TCE owner must verify the SSH host fingerprint before any SSH-based maintenance.
8. Registry administrator must verify GHCR server-side immutable-tag policy. Repository pre-push tag-absence guards and digest equality do not prove registry-side enforcement.

## Current runtime blockers

- Latest read-only K3s snapshot is [#42863102352](https://github.com/phanthienquoc/platform-infra/actions/runs/42863102352), generated at 17:15:51Z. At the 18:58:22Z reference it is 6151s old, beyond the 4500s inspection budget by 1651s. Treat every workload detail below as last-known evidence, not live state.
- Last-known node `tce-k3s-01` was Ready, ARM64, K3s v1.36.3+k3s1; disk usage was 56% (~20 GiB free), available RAM ~19 GiB, and host reported `restart_required=yes`. Host restart remains gated by operator approval.
- Last-known Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. TCE frontend/service, Auth and Keycloak were 0/0 intentional maintenance. Stock Admin was 0/1 with two `ImagePullBackOff` pods; desired Stock Backend was 0/1 `ErrImagePull`; legacy Backend and Frontend were 1/1.
- Stock Admin and desired Backend still referenced historical `12d63b4`; kubelet reported `no match for platform in manifest` on the ARM64 node. Cached Stock `23b2878` tags had no RepoDigest in the snapshot, so local image IDs are not registry digest evidence.
- Both public Keycloak OIDC discovery probes returned HTTP 503; Keycloak was 0/0 and its diagnostic timed out. The stale snapshot does not establish live TCE/Auth health.
- Media runner service/listener was active in the snapshot; GitHub runner registration is not inferred by host inspection. Decommission preflight found no Stock/Media PVC or VolumeSnapshot references in the active Platform manifest tree; the remaining `k3s-debug` PVC is unrelated. Namespaces/workloads and runner services still exist, so decommission is not complete.
- Latest reconciliation [#42872159201](https://github.com/phanthienquoc/platform-infra/actions/runs/42872159201) completed at 18:08:40Z and is now 2982s old, beyond the 2700s evidence budget. At that run, `mode=apply`, `target_app=all`, `allow_image_changes=false`; GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE web/service packages; Auth runtime Secret provision/verification succeeded with values suppressed; shared `ghcr-pull` remained unchanged; GitOps drift=false. Manifest apply, image replacement and rollout were skipped. MicroFE active health passed; TCE/Auth were explicitly classified as intentional zero-replica maintenance; Keycloak was skipped.
- Latest recovery controller [#42872433627](https://github.com/phanthienquoc/platform-infra/actions/runs/42872433627) completed SUCCESS at 18:10:16Z and is now 2886s old, beyond its 2700s freshness budget. It did not create a new K3s snapshot because the existing inspection was within budget at that run's reference time.
- Latest native scheduled reconcile [#42854065227](https://github.com/phanthienquoc/platform-infra/actions/runs/42854065227) succeeded at 16:23:35Z but is now 9287s old. The fresher #42872159201 run was `workflow_dispatch`, not a native schedule event.
- Latest native TCE WF-06 [#42872071366](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42872071366) executed at 18:08:09Z and returned HTTP 503 on all four approved endpoints (TCE web, TCE API, Auth liveness, Auth readiness), each expecting HTTP 200. It is now 3013s old, beyond the 1500s age budget. WF-12 #42867304730 is 4690s old and failed schedule freshness. WF-13 #42872110559 is workflow_run recovery, not native schedule acceptance.
- Stock scraper schedule [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) failed closed because `VNSTOCK_API_KEY` was missing; no ingestion or image publication is claimed.
- GHCR server-side immutable-tag enforcement remains unverified. Stock publisher source contract was inspected and ARM64 CI builds passed, but no new production digest exists to promote.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, shared credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
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
