# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 13:57 ICT / 06:57 UTC**

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `374222f2`; PR #1437 merged after exact-head #42453536660/#42453536676 PASS; post-merge #42453579947/#42453579869 PASS. Push smoke #42453579901 PASS but warning-only; PR #1438 corrects its summary. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42432710149 stale; manual #42452331522 failed four probes (503). Native WF-12 #42452308083 failed WF-06 freshness. WF-07 scheduled #42453060493 PASS and Platform heartbeat accepted. |
| StockDividend | CI/tests; ARM64 publisher uses full-SHA and `prod-v<version>-<full-sha>` tags, matching SHA-256 digests and `linux/arm64`; weekend scraper cron `0 1 * * 0,6` UTC has fail-closed key preflight. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `e6469ac6`; PR #38 merged; CI #42440810105 PASS 7/7. Scraper #42349150261 failed closed because `VNSTOCK_API_KEY` was empty. |
| Media Generation | CI/tests; app-owned ARM64 publisher with version/full-SHA tags and digest verification; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS. Inspection #42452273701 shows backend/frontend Running 1/1 and dedicated runner active. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS. PR #75 ready, #76 draft; prior validation PASS/Supabase Preview skipped. Migration/integration effects remain gated. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 06:09Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42439099803 PASS at 02:34:10Z; gap 12,390s; ~215m old. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42452273701 PASS at 05:49:40Z; gap 21,396s; ~20m old. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42438566387 FAIL at 02:26:41Z; gap 12,395s; ~223m old. Push smoke #42453579901 diagnostic only. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42438384072 PASS at 02:24:08Z; gap 12,313s; ~225m old. |

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
