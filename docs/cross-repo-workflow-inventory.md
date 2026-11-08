# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 17:31 ICT / 10:31 UTC**

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `ab2696c2`; PR #1453 merged after exact-head manifest/workflow/Keycloak checks all passed. Post-merge manifest validation #42471706415 and Keycloak CI #42471706467 PASS; workflow lint #42471706454 still running. Fresh read-only inspection #42471706668 triggered but `Inspect VPS` is still in progress. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42458256899 failed four probes (503); native WF-12 #42452308083 failed freshness; WF-07 #42453060493 PASS. |
| StockDividend | CI/tests; ARM64 publisher uses full-SHA and `prod-v<version>-<full-sha>` tags, matching SHA-256 digests and `linux/arm64`; weekend scraper cron `0 1 * * 0,6` UTC has fail-closed key preflight. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `e6469ac6`; PR #38 merged; CI #42440810105 PASS 7/7. Native scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock Admin/desired Backend remain ARM64 ImagePullBackOff. |
| Media Generation | CI/tests; app-owned ARM64 publisher with version/full-SHA tags and digest verification; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS. Fresh snapshot shows backend/frontend Running 1/1 and dedicated Media runner active/enabled; backup/DNS/runner-registration evidence still incomplete. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS. PR #75 ready, #76 draft; exact-head CI #40446492086/#41329425940 PASS. Supabase merge-trigger effects remain gated. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 10:31Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42467231073 FAIL at 09:27:03Z before cert-manager fix; gap 24,773s; ~64m old. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42452273701 PASS at 05:49:40Z; gap 21,396s; ~281m old. Fresh push inspection #42468887549 is not native. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42467080859 FAIL at 09:24:53Z; gap 25,092s; ~66m old. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42466737776 PASS at 09:20:06Z; gap 24,958s; ~71m old. |

Only original `event=schedule`, master, attempt 1, exact workflow path and full source SHA count as native. Manual, push, workflow_run and repository_dispatch remain separate. Push smoke reports schedule observations as warnings; it does not assert cadence acceptance.

## Reconciliation and production health

- Native reconcile #42439099803 PASS but stale. Workflow_dispatch reconcile #42452324950 PASS at 05:50:26Z on prior master SHA `5513c0bc...`; GHCR preflight, Auth runtime Secret, shared pull credentials and scoped image-pull restart passed.
- Manifest apply and image-change guard skipped; no image promotion or production rollout. Recovery #42453078467 verified TCE heartbeat and avoided duplicate fallback because reconciliation and inspection were recent.
- TCE/Auth are intentional zero-replica maintenance; lane success is not live-service health. Stock/Media remain outside active rollout scope.

## TCE schedule and health

- WF-06 remains `*/15 * * * *`; latest native #42432710149 stale; manual #42452331522 failed all four strict probes with HTTP 503.
- WF-12 remains `7,22,37,52 * * * *`; native #42452308083 failed WF-06 freshness. WF-07 scheduled #42453060493 PASS; WF-12 workflow_run #42453071754 failed stale-WF-06 gate; WF-13 #42453081086 recovered; Platform heartbeat #42453078467 passed.
- Keep strict HTTP 200 checks and TCE market-scan schedule unchanged. No replica scaling without explicit owner approval.

## Latest K3s inspection and protected decommission

- Formal read-only snapshot #42452273701 generated 05:49:48Z. Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; RAM ~19 GiB available, disk 56%/~21 GiB free.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1. Stock Admin (two pods) and desired Backend pod ImagePullBackOff on `12d63b4`; kubelet reports no matching platform manifest. Old Stock Backend and Frontend on `23b2878` remain Running.
- TCE/Auth/Keycloak remain 0/0. Stock/Media namespaces Active; no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership are unverified.
- Docker 29.1.3; 20 images/9.195 GB, ~5.773 GB reclaimable; host containerd.io 2.2.1; `restart_required=yes`. No cleanup, upgrade, reboot or decommission.
- Platform and Media runner services active/enabled; runner-registration audit remains outstanding.

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


## Latest execution evidence — 2026-11-08 16:55 ICT / 09:55 UTC

- Platform master `1f7e5cd8`; open PR #1452 fixes the decommission preflight sudo boundary. The older docs PR #1442 is superseded by this refreshed tracker and should not be merged.
- Native Platform schedules: reconcile #42467231073 failed on the pre-fix cert-manager remote Kustomize URL; inspection #42452273701 pass but stale; watchdog #42467080859 failed; recovery #42466737776 passed. Inter-arrival gaps 24,773s / 21,396s / 25,092s / 24,958s exceed 45/75/45/45m budgets. Manual/push/workflow_run runs are not native evidence.
- Cert-manager bootstrap now downloads the pinned v1.21.1 release asset through the GitHub API and checks SHA-256 before local Kustomize rendering. Validation #42468403916/#42468403911 passed; post-fix push reconcile #42468465293 passed with no drift and apply skipped.
- Fresh inspection #42468887549 generated `debug/vps-latest.md` at 09:50:50Z. Node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff on `12d63b4` (no matching platform manifest); old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. Only k3s-debug PVC/PV is listed; no Stock/Media VolumeSnapshot references. Decommission preflight itself stopped on a permission error before target namespace inventory; PR #1452 fixes wrapper invocation via sudo.
- TCE WF-06 #42458256899 failed four HTTP 503 probes; WF-12 #42452308083 failed freshness; WF-07 #42453060493 passed. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; Auth PR #75/#76 remain gated by Supabase integration behavior.
- App repositories continue to own tests/builds and immutable GHCR publication. Platform alone owns manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication, digest handoff or production promotion was observed.
- No production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 17:15 ICT / 10:15 UTC

- PR #1452 merged to Platform master `7ccd527e`; exact-head `validate-github-actions` #42469900529 and `validate-manifests` #42469900449 passed. Its post-merge `validate-manifests` push #42469989585 then failed on HTTP 403 from the pinned GitHub Release asset API. PR #1453 adds optional GH_TOKEN support to the helper and every workflow caller, with a regression test and a separate PR-comment job so PR-controlled code has only `contents: read`.
- Post-merge `validate-github-actions` #42469989622 passed. Reconciliation #42469998524 passed GHCR pull preflight, Auth runtime Secret verification, shared pull credential check and targeted lanes; no drift meant no production manifest apply, image promotion or rollout.
- Native schedule evidence is unchanged: reconcile #42467231073 FAIL (09:27:03Z, ~48m old), inspection #42452273701 PASS (05:49:40Z, ~265m old), watchdog #42467080859 FAIL (09:24:53Z, ~50m old), recovery #42466737776 PASS (09:20:06Z, ~55m old). Inter-arrival gaps 24,773s / 21,396s / 25,092s / 24,958s exceed the 45/75/45/45m budgets. Manual/push/workflow_run events are not native schedule evidence.
- Latest K3s snapshot #42468887549 remains the fresh push inspection at 09:50:50Z: node Ready/ARM64; Media/MicroFE Running 1/1; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; older Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. It predates the #1452 sudo fix; a new read-only inspection must confirm the preflight now reaches target namespace inventory.
- TCE WF-06 #42458256899 failed four HTTP 503 probes; WF-12 #42452308083 failed freshness. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; Auth PR #75/#76 remain gated.
- App repos retain tests/builds and immutable GHCR publication ownership. Platform retains manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication/digest handoff, manifest apply, workload scaling, decommission, DNS/database/storage change or host maintenance. TCE market-scan schedule unchanged.


## Latest execution update — 2026-11-08 17:31 ICT / 10:31 UTC

- Platform master `ab2696c2` includes merged PR #1453. Exact-head checks #42470921373/#42470921319/#42470921336 passed. Post-merge manifest validation #42471706415 and Keycloak CI #42471706467 passed; post-merge workflow lint #42471706454 remained in progress at the review cutoff.
- The cert-manager bootstrap helper now uses optional `GH_TOKEN` for the pinned GitHub Release asset API, preserves SHA-256 verification and avoids logging the token. The validation job retains `contents: read`; PR-comment write permission is isolated in a separate job without checkout.
- Read-only inspection #42471706668 was triggered by the helper/preflight path filter and remained in progress at the `Inspect VPS` step. It must complete before claiming the #1452 sudo boundary works against live K3s inventory.
- Native schedule events remain unchanged: Platform reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776; TCE WF-06 #42458256899 and WF-12 #42452308083. Ages exceed their configured freshness budgets; push/manual/workflow_run fallbacks are not native evidence. Cron and budgets unchanged.
- No new app image publication or digest handoff. Stock scraper #42457182511 fails closed on missing `VNSTOCK_API_KEY`; TCE WF-06 has four HTTP 503 probes; Media CI and Auth CI remain last recorded PASS. No production manifest apply, image promotion, workload scaling, decommission, runner retirement or host maintenance.
