# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 01:19 ICT (2026-11-10 18:19:05 UTC)

This is the compact current readiness view. Historical append-only content is preserved under `docs/archive/`; timestamped checkpoints remain under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `c81ec47005f47963323b933153199a433301f830` | #1314, #544, #541, #539 (owner-decision drafts) | PR #1593 merged; exact-head validation #42873684350 and post-merge validate-manifests #42873912468 passed. Latest manual reconciliation #42872159201 and recovery #42872433627 succeeded; no manifest drift, apply/rollout skipped. |
| phanthienquoc/TCE-dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | none | WF-02 #42822853121 and WF-05 #42822853137 passed. Latest native WF-06 #42872071366 executed at 18:08:09Z but all four public endpoints returned HTTP 503 (expected 200); WF-12 #42867304730 remains failed/stale. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Stock CI #42610360402 passed, including ARM64 non-publishing builds. Scraper schedule #42457182511 failed closed because VNSTOCK_API_KEY was absent. No production publisher run or new digest. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Media CI #42539512417 passed. Last K3s inspection #42863102352 showed backend/frontend 1/1; Media runner service/listener remained active. No new publication or promotion. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft / owner decision) | auth-service-ci #42654579277 passed. Auth runtime Secret was provisioned/verified in reconciliation #42872159201 with values suppressed; Auth remains 0/0 maintenance, not live health. |

### Recent Platform changes

- PR #1587 merged as `ec8b91f1fb9c66740562d50cc73c4b68c6cb8422` after exact-head manifest validation.
- PR #1588 merged as `bfd0ea66ee005bd47b4dbcc85ced6428d78d9f44`; it fixed the inspection workflow's runner-local remote-tracking ref update and pinned actionlint v1.7.12 with checksum verification.
- Inspection-only PR #1589 merged as `61bbb9c0927ba43902f59344c38b289d493934b3`.
- Inspection-only PR #1591 merged as `0ee1fd060616571ef3790286bb7ea7d7723ed31d`; it updated only `debug/vps-latest.md` from run #42863102352. No production manifest changed.
- PR #1592 merged as `ec57bb3a67920a83f48a33959d7be484c48352fc` at 17:38:58Z; post-merge `validate-manifests` run #42867109200 passed.
- PR #1593 merged as `c81ec47005f47963323b933153199a433301f830`; exact-head `validate-manifests` #42873684350 and post-merge run #42873912468 passed. Current Platform master is this SHA.
- Previous checkpoint PR #1590 was closed without merge because its branch was behind the current master and its readiness data had become stale. Its 00:11/00:18 checkpoint files are preserved in the replacement checkpoint branch.
- TCE PR #1036 remains merged as `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; its regression contract requires exactly four approved public endpoints and HTTP 200.

Open owner-decision drafts remain: Platform #1314 (mail plan), #544 (Keycloak activation), #541 (Keycloak database plan), #539 (central identity architecture), and Authentication #76 (migration drift investigation). Do not merge these without the relevant owner decision and side-effect review.

## Native schedule freshness

Reference time: 2026-11-10 18:19:05 UTC (2026-11-11 01:19 ICT). Only first-attempt `event=schedule` runs on `master` count. Manual, push, pull_request, workflow_run and repository_dispatch events are not native schedule substitutes.

| Lane | Latest native run | Result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile | #42854065227 | success / 16:23:35 | 6930 | 30424 | 2700 |
| Platform inspection | #42809278936 | success / 11:39:41 | 23964 | 29694 | 4500 |
| Platform recovery | #42848981485 | success / 15:52:52 | 8773 | 29378 | 2700 |
| Platform watchdog | #42850178931 | failure / 15:59:51 | 8354 | 29729 | 2700 |
| TCE WF-06 | #42872071366 | failure / 18:08:09 | 656 | 27554 | 1500 |
| TCE WF-12 | #42867304730 | failure / 17:40:12 | 2333 | 27647 | 1500 |

All six inter-arrival gaps exceed their unchanged budgets. Five current ages also exceed budget; TCE WF-06 is 656s old (within its 1500s age budget), but its inter-arrival gap is 27554s and all four public probes returned HTTP 503. TCE WF-12 is 2333s old (beyond 1500s) and its 27647s inter-arrival gap fails.

TCE WF-06 native schedule #42872071366 executed at 18:08:09Z but failed all four HTTP 200 health probes. WF-13 recovery #42872110559 is workflow_run, and WF-06 dispatch #42872140547 is workflow_dispatch; neither substitutes for native schedule cadence. Platform reconciliation #42872159201 and recovery #42872433627 are workflow_dispatch events, not native schedule acceptance.

Configured schedules remain unchanged:
- Platform reconcile: `7,22,37,52 * * * *`
- Platform inspection: `2,32 * * * *`
- Platform recovery: `10,25,40,55 * * * *`
- Platform watchdog: `12,27,42,57 * * * *`
- TCE WF-06: `*/15 * * * *`
- TCE WF-12: `7,22,37,52 * * * *`

Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497) — GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for the six schedule workflows. At 18:19:05Z all six inter-arrival gaps exceed budget; five current ages exceed budget. TCE WF-06 has a new native run within its age budget, but its gap remains 27554s and health probes fail. Repository run history cannot distinguish scheduler delay, enqueue failure, dropped event or runner delivery failure.
2. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575) — branch metadata reports `protected=false` on all five master branches. Platform repository rulesets GET returned an empty list; branch-protection detail GET returned HTTP 403, and private Stock rulesets reads are plan-restricted. Effective required-check/PR-only enforcement is not verified. Administrator must confirm effective policy.
3. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872) — TCE/Auth owners must diagnose HTTP 503 and Keycloak/OIDC, provide approved immutable release digests and rollback references, and explicitly approve recovery. Keep HTTP 200 as the only healthy public response. TCE/Auth/Keycloak zero replicas are intentional maintenance, not healthy service.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42) — latest observed scraper schedule #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. Stock owner must provision it through repository/organization secrets and run `preflight_only=true` before ingestion. Never put the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43) — Stock owner must approve a source release and explicitly enable the manual publication gate. The publisher contract and ARM64 non-publishing CI builds are present, but no production publication/digest handoff exists. Never overwrite historical tag `12d63b4`.
6. Media promotion remains blocked pending an authorized `PLATFORM_INFRA_AUTOMATION_TOKEN` and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Platform operator must keep using fresh read-only inspection, then obtain separate host maintenance/restart approval. TCE owner must verify the SSH host fingerprint before any SSH-based maintenance.
8. Registry administrator must verify GHCR server-side immutable-tag policy. Repository pre-push tag-absence guards and digest equality do not prove registry-side enforcement.

## Current runtime blockers

- Latest read-only K3s snapshot is [#42863102352](https://github.com/phanthienquoc/platform-infra/actions/runs/42863102352), generated at 17:15:51Z. At the 18:19:05Z reference it is 3794s old, within the 4500s inspection budget by 706s; it is approaching expiry and remains inspection-only.
- Node `tce-k3s-01` is Ready, ARM64, K3s v1.36.3+k3s1; disk usage is 56% (~20 GiB free), available RAM ~19 GiB, and host reports `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1. TCE frontend/service, Auth and Keycloak are 0/0 intentional maintenance. Stock Admin is 0/1 with two `ImagePullBackOff` pods; desired Stock Backend is 0/1 `ErrImagePull`; legacy Backend and Frontend remain 1/1.
- Stock Admin and desired Backend still reference historical `12d63b4`; kubelet reports `no match for platform in manifest` on the ARM64 node. Cached Stock `23b2878` tags have no RepoDigest in the snapshot, so local image IDs are not registry digest evidence.
- Both public Keycloak OIDC discovery probes return HTTP 503; Keycloak is 0/0 and its diagnostic timed out. The snapshot does not establish live TCE/Auth health.
- Media runner service/listener is active; GitHub runner registration is not inferred by host inspection. Decommission preflight found no Stock/Media PVC or VolumeSnapshot references in the active Platform manifest tree; the remaining `k3s-debug` PVC is unrelated. Namespaces/workloads and runner services still exist, so decommission is not complete.
- Latest reconciliation [#42872159201](https://github.com/phanthienquoc/platform-infra/actions/runs/42872159201) completed at 18:08:40Z (625s old, within the 2700s evidence budget), with `mode=apply`, `target_app=all`, `allow_image_changes=false`. Logs verified read access to Auth, MicroFE Shell/WS and TCE web/service GHCR packages; Auth runtime Secret provision/verification succeeded with values suppressed; shared `ghcr-pull` remained unchanged. No image-pull failures were found for MicroFE Auth/Shell/WS or TCE service/frontend. GitOps drift=false, so production manifest apply, image replacement and rollout were skipped. MicroFE active health passed; TCE/Auth were explicitly classified as intentional zero-replica maintenance; Keycloak was skipped.
- Latest recovery controller [#42872433627](https://github.com/phanthienquoc/platform-infra/actions/runs/42872433627) completed SUCCESS at 18:10:16Z. It confirmed the existing read-only inspection fallback #42863102352 was 52m old at its own reference and did not dispatch a duplicate inspection. No new K3s snapshot was created.
- Latest native scheduled reconcile [#42854065227](https://github.com/phanthienquoc/platform-infra/actions/runs/42854065227) succeeded at 16:23:35Z but is 6930s old, beyond the 2700s evidence budget. The fresher #42872159201 run is `workflow_dispatch`, not a native schedule event.
- Latest native TCE WF-06 [#42872071366](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42872071366) executed at 18:08:09Z but all four approved public endpoints returned HTTP 503 (TCE web, TCE API, Auth liveness, Auth readiness), each expecting HTTP 200. Its current age is within budget, but its inter-arrival gap is not. WF-12 #42867304730 remains failed/stale. WF-13 #42872110559 is workflow_run recovery, not native schedule acceptance.
- Stock scraper schedule [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) failed closed because `VNSTOCK_API_KEY` was missing; no ingestion or image publication is claimed.
- GHCR server-side immutable-tag enforcement remains unverified.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Stock publisher contract was inspected but not executed; no new Stock digest exists to promote.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, shared credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
- Reconciliation #42872159201 provisioned/verified the Auth runtime Secret with values suppressed; shared `ghcr-pull` was unchanged.
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
