# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 09:04 ICT / 2026-11-08 02:04 UTC**

Rolling inventory only; timestamped run/PR evidence remains under `docs/cross-repo-deployment-checkpoints/`.

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `06342dce`; PR #1430 merged; post-merge validation #42433130386 PASS. Latest fallback reconciliation #42432741608 PASS; no manifest drift; native schedules stale and formal inspection stale. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42432710149 and manual #42432739134 failed all four strict HTTP 200 probes with HTTP 503. Workflow_run watchdog/recovery passes are not native delivery. |
| StockDividend | CI/tests; ARM64 deploy workflow publishes full-SHA tags and verifies registry digests; weekend scraper cron has fail-closed `VNSTOCK_API_KEY` preflight and `preflight_only` mode. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `783ae36f`; CI #42375688209 7/7 PASS. Scraper #42349150261 failed before dependencies/ingestion because `VNSTOCK_API_KEY` is empty. No 2026-11-08 01:00Z scheduled run appeared in latest history. |
| Media Generation | CI/tests; WF-03 builds ARM64, publishes version + full-SHA immutable tags and verifies digests; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS; backend/frontend and dedicated runner remain active in latest formal K3s inspection; no recent publisher/digest handoff. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags against one digest and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS. PR #75 validate PASS/Supabase Preview skipped; #76 validate PASS/Supabase Preview skipped. #75 remains open pending integration side-effect verification; #76 remains draft. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 2026-11-08 02:04Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42423799465 PASS; 12,392s inter-arrival; ~2h56m old. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42427239949 PASS; 13,475s inter-arrival; ~2h11m old. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42423187797 FAIL; 12,563s inter-arrival; ~3h04m old. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42423100821 PASS; 12,553s inter-arrival; ~3h05m old. |

Only original `event=schedule`, master, attempt 1, exact workflow path and full source SHA are native evidence. Manual, push, workflow_run and repository_dispatch remain separate. Do not lower freshness budgets or count fallbacks as native delivery.

TCE-triggered recovery #42432731030 validated native WF-06 heartbeat #42432710149 and dispatched existing reconcile-vps #42432741608 on master SHA `4b829d` with `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR access preflight passed for Auth/MicroFE/TCE; Auth runtime Secret was provisioned/verified with values suppressed; observed shared `ghcr-pull` Secrets were unchanged. TCE release pairing passed. GitOps drift=false, so manifest apply and image-change guard were skipped. The scoped image-pull restart policy step completed; lane rollout checks were skipped where no rollout was required. MicroFE health passed; Auth/TCE were explicitly treated as zero-replica maintenance, not live health. Post-reconcile recovery #42432855950 passed but did not dispatch inspection fallback at its 01:07:40Z reference time because inspection age was 74m.

## Cross-repo schedules and release boundaries

- TCE WF-06 remains `*/15 * * * *`; WF-12 remains `7,22,37,52 * * * *`. Four endpoints returned HTTP 503 on native WF-06 #42432710149. Manual WF-06 #42432739134 also failed. Workflow_run watchdog/recovery passes are not native delivery or endpoint health. TCE market-scan schedule unchanged.
- Stock weekend scraper remains `0 1 * * 0,6` UTC. Job log confirms `VNSTOCK_API_KEY` was empty; `preflight_only=true` must pass with authenticated non-guest entitlement before ingestion. No expected 2026-11-08 01:00Z scheduled run appeared in latest Actions history.
- Media/Auth publisher jobs are purposeful manual/release workflows; do not convert them into scheduled production deployment authorities.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, digest/provenance gates, GitOps promotion/reconciliation, rollout and health.

## Latest production evidence and limitations

- Latest formal read-only K3s inspection remains #42427239949, generated at 2026-11-07 23:53:12Z; stale at this review. No newer inspection artifact was found.
- Node tce-k3s-01 Ready/ARM64; K3s v1.36.3+k3s1; runtime containerd 2.3.2-k3s2; disk 56% (~20 GiB free), RAM ~19 GiB available.
- Media backend/frontend and MicroFE Shell/WS/NATS Running. TCE/Auth/Keycloak remain intentional 0/0.
- Stock Admin has two ImagePullBackOff pods on `12d63b4`; Stock Backend has an older `23b2878` pod Running and a desired `12d63b4` pod ImagePullBackOff; Stock Frontend Running on `23b2878`. Kubelet previously reported no ARM64 manifest for `12d63b4`.
- Stock/Media namespaces remain Active. Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB); no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership unverified.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1 with updates available; `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform runner and dedicated Media runner active/enabled. Runner policy rejects Stock/Media restart or rollout authority.
- No new immutable publisher run/digest handoff or production image promotion.

## Protected decommission and security

Stock/Media remain retired from active Platform GitOps but legacy namespaces/workloads are still present. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider ownership attestation, dedicated Media runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight.

A prior short-lived runner registration token appeared in an Actions environment dump. PR #1416 masks it before output and later bootstrap verification showed masked output. Platform owner must still inspect runner registrations and GitHub audit log; registry cleanliness is not certified.

## Authority boundary

- `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only.
- No duplicate direct SSH/Compose deployment authority.
- Stock/Media deletion, runner retirement, DNS/database/storage changes and host maintenance remain gated on explicit evidence and owner approval.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0904-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0904-ict.md)
