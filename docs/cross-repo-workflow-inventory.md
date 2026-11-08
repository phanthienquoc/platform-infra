# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 12:59 ICT / 2026-11-08 05:59 UTC**

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `7db5471c`; inspection PR #1436 merged from #42452273701. PR #1435 is refreshed against current master; PR #1437 aggregates all native schedule failures, validation queued. Native reconcile #42439099803, watchdog #42438566387 and recovery #42438384072 remain stale; native inspection #42452273701 is fresh by age but its 21,396s inter-arrival gap exceeds 75m. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42432710149 remains stale; manual #42452331522 failed four HTTP 200 probes (503). Native WF-12 #42452308083 failed WF-06 freshness (17,084s age, queue 0m) and sent Platform heartbeat successfully. |
| StockDividend | CI/tests; ARM64 deploy publisher uses full-SHA and `prod-v<version>-<full-sha>` tags, verifies matching SHA-256 digests and `linux/arm64`; weekend scraper cron `0 1 * * 0,6` UTC has fail-closed `VNSTOCK_API_KEY` preflight and `preflight_only` mode. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `e6469ac6`; PR #38 merged; master CI #42440810105 PASS 7/7. Scraper #42349150261 failed closed because `VNSTOCK_API_KEY` was empty; no Sunday 01:00Z run in recent history. |
| Media Generation | CI/tests; app-owned ARM64 publisher with version/full-SHA tags and digest verification; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS. Inspection #42452273701 shows backend/frontend Running 1/1 and dedicated runner active; no recent publisher/digest handoff. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags against one digest and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS. PR #75 ready and #76 draft; prior validation PASS/Supabase Preview skipped. #75 remains gated on Supabase integration and merge-triggered migration effects. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 05:59Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42439099803 PASS at 02:34:10Z; inter-arrival 12,390s; ~205m old. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42452273701 PASS at 05:49:40Z; inter-arrival 21,396s; ~9m old. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42438566387 FAIL at 02:26:41Z; inter-arrival 12,395s; ~212m old. Workflow_run #42452390618 at 05:51:27Z also failed but is not native. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42438384072 PASS at 02:24:08Z; inter-arrival 12,313s; ~215m old. Workflow_dispatch #42452477069 PASS at 05:52:49Z is fallback only. |

Only original `event=schedule`, master, attempt 1, exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch remain separate. Do not lower freshness budgets or count fallbacks as native delivery.

## Reconciliation and production health

- Native reconcile #42439099803 PASS but stale. Workflow_dispatch reconciliation #42452324950 PASS at 05:50:26Z on prior master SHA `5513c0bc...`; GHCR preflight, Auth runtime Secret, shared pull credentials and scoped image-pull restart steps passed.
- Manifest apply and image-change guard were skipped; no image promotion or production rollout. Recovery controller #42452477069 verified recent reconciliation and fresh inspection without duplicate dispatch.
- TCE/Auth are intentional zero-replica maintenance; lane success is not live-service health. Stock/Media remain outside active rollout scope.

## TCE schedule and health

- WF-06 remains `*/15 * * * *`; latest native #42432710149 is stale and failed. Manual #42452331522 returned HTTP 503 from all four strict probes.
- WF-12 remains `7,22,37,52 * * * *`; latest native #42452308083 failed because WF-06 age was 17,084s vs 1,500s budget, with queue wait 0m. Platform heartbeat succeeded; WF-13 recovery #42452318480 is workflow_run, not native.
- Keep strict HTTP 200 checks and TCE market-scan schedule unchanged. No replica scaling without explicit owner approval.

## Latest K3s inspection and protected decommission

- Formal read-only snapshot #42452273701 generated 05:49:48Z. Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; RAM ~19 GiB available, disk 56%/~21 GiB free.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1. Stock Admin (two pods) and desired Stock Backend pod ImagePullBackOff on `12d63b4`; kubelet reports no matching platform manifest. Old Stock Backend and Frontend on `23b2878` remain Running.
- TCE/Auth/Keycloak remain 0/0. Stock/Media namespaces remain Active; no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership are unverified.
- Docker 29.1.3; 20 images/9.195 GB, ~5.773 GB reclaimable; host containerd.io 2.2.1; `restart_required=yes`. No cleanup, upgrade, reboot or decommission.
- Platform and Media runner services active/enabled; runner-registration audit remains outstanding.

## Cross-repo release boundaries

- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance gates, GitOps promotion/reconciliation, rollout and health.
- TCE/Auth sender/receiver payloads remain digest-bound and statically aligned. Stock #38 contract is merged; Media/Stock have no active Platform dispatch while retired.
- No new publisher run, GHCR publication, digest handoff or production image promotion in this review.
- No duplicate direct SSH/Compose deployment authority. Stock/Media deletion remains protected by backup, DNS, runner retirement, production approval and fresh PVC/PV/VolumeSnapshot gates.
