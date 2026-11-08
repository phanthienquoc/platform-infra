# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 11:00 ICT / 2026-11-08 04:00 UTC**

Rolling inventory only; timestamped run/PR evidence remains under `docs/cross-repo-deployment-checkpoints/`.

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `11b0b86a`; PR #1433 merged after exact-head #42441046772 and post-merge #42441085003 PASS. Latest native reconcile #42439099803 PASS but ~91m old; inspection #42427239949 ~4h12m old; watchdog #42438566387 FAIL and recovery #42438384072 PASS are also stale. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42432710149 and manual #42432739134 failed four HTTP 200 probes (503); native WF-12 #42427247349 failed stale-health gate. |
| StockDividend | CI/tests; ARM64 deploy publisher uses full-SHA and `prod-v<version>-<full-sha>` tags, verifies matching SHA-256 digests and `linux/arm64`; weekend scraper cron has fail-closed `VNSTOCK_API_KEY` preflight and `preflight_only` mode. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `e6469ac6`; PR #38 merged. Exact-head CI #42437287197 7/7 PASS; post-merge CI #42440810105 in progress (5/7 at review). Scraper #42349150261 failed closed because `VNSTOCK_API_KEY` was empty. |
| Media Generation | CI/tests; WF-03 builds ARM64, publishes version + full-SHA tags and verifies digests; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS; backend/frontend and dedicated runner remain active in fresh inspection #42438528386; no recent publisher/digest handoff. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags against one digest and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS. PR #75 validation PASS/Supabase Preview skipped; #76 validation PASS/Supabase Preview skipped. #75 remains open pending integration side-effect verification; #76 remains draft. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 2026-11-08 04:00Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42439099803 PASS at 02:34:10Z; inter-arrival 12,390s (budget 2,700s); ~91m old at review. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42427239949 PASS at 23:53:04Z; inter-arrival 13,475s; ~4h12m old at review. Manual read-only inspection #42438528386 PASS at 02:26:17Z is separate. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42438566387 FAIL at 02:26:41Z; inter-arrival 12,395s; ~98m old at review. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42438384072 PASS at 02:24:08Z; inter-arrival 12,313s; ~101m old at review. |

Only original `event=schedule`, master, attempt 1, exact workflow path and full source SHA are native evidence. Manual, push, workflow_run and repository_dispatch remain separate. Do not lower freshness budgets or count fallbacks as native delivery.

Watchdog #42438566387 confirmed `reconcile-vps.yml` was active but failed the inspection freshness and native inter-arrival checks; its log identifies a 12,392s gap between #42407410735 and #42423799465. The later native reconcile #42439099803 succeeded but its gap from #42423799465 is 12,390s, still outside 45m. No native scheduled inspection newer than #42427239949 appears in the reviewed history. Recovery #42438384072 and post-reconcile recovery paths succeeded; the manual inspection fallback is not native schedule evidence.

## Reconciliation and production health

- [Reconcile #42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803) ran on master with `mode=apply`, `target_app=all`, `allow_image_changes=false`; final deployment gate PASS.
- GHCR access preflight passed for Auth, MicroFE Shell/WS and TCE web/service. Auth runtime Secret provision/verification passed with values suppressed. Shared pull-credential reconciliation completed.
- GitOps preflight found no drift; manifest apply and image-change guard were skipped. MicroFE health passed. TCE/Auth are intentional zero-replica maintenance; their successful lane checks are not live-service health. Stock/Media remain outside active rollout scope.
- No new image promotion or production rollout occurred.

## Cross-repo schedules and release boundaries

- TCE WF-06 remains `*/15 * * * *`; WF-12 cron and strict HTTP 200 health expectations remain unchanged. Four endpoints returned HTTP 503 on native WF-06 #42432710149; manual WF-06 #42432739134 also failed. Workflow_run watchdog/recovery passes are not native delivery or endpoint health. TCE market-scan schedule unchanged.
- Stock weekend scraper remains `0 1 * * 0,6` UTC. Job log confirms `VNSTOCK_API_KEY` was empty; `preflight_only=true` must pass with authenticated non-guest entitlement before ingestion. No 2026-11-08 01:00Z scheduled run appeared in latest run history.
- Media/Auth publisher jobs are purposeful manual/release workflows; do not convert them into scheduled production deployment authorities.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, digest/provenance gates, GitOps promotion/reconciliation, rollout and health.

## Latest production evidence and limitations

- Latest formal read-only K3s inspection [#42438528386](https://github.com/phanthienquoc/platform-infra/actions/runs/42438528386), generated 2026-11-08 02:26:17Z and merged via inspection PR #1432; approximately 98m old at 04:04Z review. Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2; disk 56% (~21 GiB free), RAM ~19 GiB available.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1. TCE/Auth/Keycloak remain intentional 0/0.
- Stock Admin has two ImagePullBackOff pods on `12d63b4`; desired Stock Backend pod on `12d63b4` ImagePullBackOff while older `23b2878` pod remains Running; Stock Frontend Running on `23b2878`. Failed Stock pod imageID values are absent; prior kubelet event identified no ARM64 manifest for `12d63b4`.
- Stock/Media namespaces remain Active. Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB); no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership unverified.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1 with updates available; `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform runner and dedicated Media runner active/enabled. Runner policy rejects Stock/Media restart or rollout authority.
- No new app publisher run/digest handoff or production image promotion. Stock PR #38 CI builds were non-publishing.

## Protected decommission and security

Stock/Media remain retired from active Platform GitOps but legacy namespaces/workloads are still present. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider ownership attestation, dedicated Media runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight.

A prior short-lived runner registration token appeared in an Actions environment dump. PR #1416 masks it before output and later bootstrap verification showed masked output. Platform owner must still inspect runner registrations and GitHub audit log; registry cleanliness is not certified.

## Authority boundary

- `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only.
- No duplicate direct SSH/Compose deployment authority.
- Stock/Media deletion, runner retirement, DNS/database/storage changes and host maintenance remain gated on explicit evidence and owner approval.
- TCE market-scan schedule unchanged.


## 11:00 ICT evidence refresh

- Current masters: Platform `11b0b86a971a1c106d1420930def8d4df80fd99a`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Auth `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.
- Open PRs: Platform #1314/#544/#541/#539 (draft); Auth #75 (ready) and #76 (draft); no open PRs in TCE, Stock or Media.
- Platform master validation #42441085003 PASS; Stock master CI #42440810105 PASS 7/7. No new Media/Auth CI or app publisher run.
- Stock immutable publisher contract is merged: full SHA + `prod-v<version>-<full-sha>`, same SHA-256 digest, ARM64 manifest. CI builds were non-publishing; GHCR publication and registry-side tag immutability are not proven.
- Platform native schedules remain outside freshness budgets; latest exact schedule runs and gaps are listed above. Do not count fallbacks as native delivery.
- TCE WF-06 #42432710149 remains HTTP 503 on all four endpoints; WF-12 #42427247349 is stale. TCE market-scan schedule remains unchanged.
- Stock weekend scraper cron remains `0 1 * * 0,6` UTC; expected 2026-11-08 01:00Z event is absent. Prior run #42349150261 failed closed because `VNSTOCK_API_KEY` was empty. Owner must provision secret and pass `preflight_only=true` before ingestion.
- Auth #75/#76 checks remain validation PASS/Supabase Preview SKIPPED; both are based on an older master SHA and stay gated on migration/integration review.
- No fresh K3s inspection after #42438528386 (02:26:17Z); current cluster health cannot be asserted from the aged snapshot.
