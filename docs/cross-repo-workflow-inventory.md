# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 15:57 ICT / 08:57 UTC**

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `f779f74d`; PR #1439/#1440/#1441 merged; #1441 exact-head #42461666616 and post-merge #42461706752 PASS. Native schedules remain stale. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42458256899 failed four strict probes with 503; native WF-12 #42452308083 failed freshness. Workflow_run #42458270339 passed heartbeat delivery only. |
| StockDividend | CI/tests; ARM64 publisher uses full-SHA and `prod-v<version>-<full-sha>` tags, matching SHA-256 digests and `linux/arm64`; weekend scraper cron `0 1 * * 0,6` UTC has fail-closed key preflight. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `e6469ac6`; PR #38 merged; CI #42440810105 PASS 7/7. Native scraper #42457182511 failed closed before dependency installation because `VNSTOCK_API_KEY` is missing. |
| Media Generation | CI/tests; app-owned ARM64 publisher with version/full-SHA tags and digest verification; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS. Last K3s snapshot #42458425146 showed backend/frontend 1/1 but is now >75m old; no new publisher/digest handoff. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS. PR #75 ready, #76 draft; exact-head CI #40446492086/#41329425940 PASS. Supabase migration/integration effects remain gated. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 08:57Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42439099803 PASS at 02:34:10Z; gap 12,390s; age ~384m. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42452273701 PASS at 05:49:40Z; gap 21,396s; age ~188m. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42438566387 FAIL at 02:26:41Z; gap 12,395s; age ~391m. Push smoke #42454041525 diagnostic only. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42438384072 PASS at 02:24:08Z; gap 12,313s; age ~394m. |

No newer native Platform schedule event appears through 08:57Z. Only original `event=schedule`, master, attempt 1 and exact workflow path count as native. Manual, push, workflow_run and repository_dispatch are separate. Push smoke is diagnostic-only.

## Reconciliation and production health

- Latest native reconcile #42439099803 PASS at 02:34:10Z is stale by ~384m. Manual reconciliation #42458288651 passed at 07:19Z: GHCR access and Auth runtime Secret verification passed; shared `ghcr-pull` unchanged; no GitOps drift; manifest apply and image promotion skipped.
- Manual recovery #42458395401 passed after reconciliation. Neither manual run counts as native schedule evidence or a production rollout.
- TCE/Auth were explicitly reported as intentional zero-replica maintenance (no live health asserted); active MicroFE health passed. Stock/Media remain outside active rollout scope.

## TCE schedule and health

- WF-06 remains `*/15 * * * *`; latest native #42458256899 at 07:18:37Z failed all four strict HTTP 200 probes: TCE web, TCE API, Auth liveness and Auth readiness each returned 503. Job logs confirm the status codes.
- WF-12 remains `7,22,37,52 * * * *`; latest native #42452308083 at 05:50:11Z failed freshness. Workflow_run #42458270339 passed heartbeat/delivery at 07:18Z but is not native cadence evidence and does not establish endpoint health.
- WF-07 latest native #42453060493 passed at 06:01:55Z. Keep strict HTTP 200 checks and TCE market-scan schedule unchanged. No replica scaling without explicit owner approval and rollback plan.

## Latest K3s inspection and protected decommission

- Latest committed read-only snapshot is `debug/vps-latest.md`, generated at 07:21:07Z by manual inspection #42458425146. At 08:57Z it is ~97m old, beyond the 75m snapshot-age budget; do not treat it as current cluster health.
- Last-known snapshot: node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; ~19 GiB RAM available and disk 56%/~21 GiB free. Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1.
- Stock Admin (two pods) and desired Backend on `12d63b4` were ImagePullBackOff with `no match for platform in manifest`; old Backend and Frontend remained Running. TCE/Auth/Keycloak were intentional 0/0.
- Stock/Media namespaces Active; no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership remain unverified. Docker 29.1.3, host containerd.io 2.2.1, ~5.77 GB reclaimable, `restart_required=yes`. Platform/Media runner services active/enabled; registration audit remains outstanding.
- No cleanup, upgrade, reboot, runner retirement or decommission. Obtain a fresh read-only inspection before any rollout or deletion decision.

## Cross-repo release boundaries

- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance gates, GitOps promotion/reconciliation, rollout and health.
- TCE/Auth sender/receiver payloads remain digest-bound and statically aligned. Stock #38 contract is merged; Media/Stock have no active Platform dispatch while retired.
- No new publisher run, GHCR publication, digest handoff or production image promotion in this review.
- No duplicate direct SSH/Compose deployment authority. Stock/Media deletion remains protected by backup, DNS, runner retirement, production approval and fresh PVC/PV/VolumeSnapshot gates.


## Latest execution evidence — 2026-11-08 13:57 ICT / 06:57 UTC

- Platform master: `9f6618f8736ab14d58595436faa87944cc45bb4d`; latest push smoke #42454041525 PASS, warning-only. Native reconcile #42439099803, watchdog #42438566387 and recovery #42438384072 remain outside cadence budgets; native inspection #42452273701 is within age budget but its 21,396s inter-arrival gap exceeds the 75m cadence budget.
- TCE: WF-07 scheduled #42453060493 PASS; WF-12 #42452308083 and its workflow_run freshness check fail; WF-13 #42453081086 recovers heartbeat delivery. Manual WF-06 #42452331522 remains 4/4 HTTP 503. No TCE replicas are changed.
- Stock: master CI #42440810105 PASS. Scraper #42349150261 failed closed on empty `VNSTOCK_API_KEY`; the next Sunday scheduled run is not visible at 06:57Z, but prior Saturday delivery was delayed until 06:56:29Z, so continue observing rather than declaring a missed delivery yet.
- Media: latest recorded master CI #42239703151 PASS; no new publisher evidence.
- Authentication: master CI #42215394539 PASS; PR #75 exact-head CI #40446492086 PASS but merge remains gated by Supabase Deploy-to-production integration behavior; PR #76 exact-head CI #41329425940 PASS and remains draft.
- Open PRs: Platform #1314/#544/#541/#539; Authentication #75/#76. TCE, Stock and Media have none.
- No GHCR publish/promotion, production manifest mutation, workload scaling, decommission, DNS/database/storage change, runner retirement or host maintenance. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 15:04 ICT / 08:04 UTC

- Platform master `564d94bb9134195a0643274f8656d95161b47e02`; inspection PR #1440 merged at exact validated head `9cdfaddc66fbcb21a6ea7a78e05f44551726fa69` (merge SHA `564d94bb9134195a0643274f8656d95161b47e02`). Read-only inspection #42458425146 succeeded; exact-head manifest validation #42458510940 passed.
- Manual reconcile #42458288651: GHCR pull access and Auth runtime Secret verification passed; shared `ghcr-pull` unchanged; no manifest drift, so apply skipped. TCE/Auth are intentional zero-replica maintenance (no live health asserted); active MicroFE health passed. No image promotion.
- Platform native schedule latests: reconcile #42439099803, inspection #42452273701, watchdog #42438566387, recovery #42438384072. At 08:04Z all exceed their 45/75/45/45m freshness budgets. Manual fallback runs do not count. Cron and budgets unchanged.
- TCE WF-06 native #42458256899 failed all four strict HTTP 200 probes with HTTP 503. WF-12 workflow_run #42458270339 confirmed WF-06 active and fresh at its own run time (age/queue 0m) and delivered authenticated Platform heartbeat; by 08:04Z the 25m age budget is exceeded again. Latest native WF-12 #42452308083 remains stale/failing. WF-13 #42458270097 passed recovery.
- Stock scraper scheduled run #42457182511 failed closed before dependency installation because `VNSTOCK_API_KEY` is empty. Stock master CI #42440810105 PASS 7/7. No credential change or ingestion.
- Media CI #42239703151 and Auth CI #42215394539 remain PASS. Auth PR #75/#76 exact-head CI #40446492086/#41329425940 PASS; Supabase merge-trigger effect remains a gate.
- Fresh K3s snapshot #1440: node Ready/ARM64; Media and MicroFE workloads Running 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff for `12d63b4` (no ARM64 manifest); old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. Runner services active/enabled, registration audit outstanding. No Stock/Media VolumeSnapshot references; external backup/DNS ownership unverified. Host restart required; no maintenance performed.
- App repos retain tests/builds and immutable GHCR publication ownership. Platform retains manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication, digest handoff, production apply, scaling, decommission, DNS/database/storage change, or direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 15:57 ICT / 08:57 UTC

- Current master heads: Platform `f779f74d7176437a85e183ca00dd44e704023a3e`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Auth `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.
- Open PRs: Platform #1314/#544/#541/#539 (draft); Auth #75 (ready) and #76 (draft); TCE/Stock/Media none.
- Platform PR #1441 merged; exact-head #42461666616 and post-merge #42461706752 passed. Latest native Platform schedule events remain reconcile #42439099803, inspection #42452273701, watchdog #42438566387 and recovery #42438384072; all exceed freshness budgets at 08:57Z.
- TCE native WF-06 #42458256899 failed 4/4 with HTTP 503; native WF-12 #42452308083 failed freshness. Workflow_run #42458270339 passed heartbeat delivery but is not native.
- Stock native scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was empty. Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; no new publisher/digest handoff.
- Last K3s snapshot #42458425146 is >75m old. Last-known Stock ARM64 ImagePullBackOff and intentional TCE/Auth zero replicas remain unverified by a fresh snapshot.
- No production mutation or host maintenance; TCE market-scan schedule unchanged.
