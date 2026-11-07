# Cross-repo production deployment readiness

Current review: **2026-11-08 04:55 ICT / 2026-11-07 21:55 UTC**

This is the rolling operational summary. Detailed immutable run/PR checkpoints are retained in [docs/cross-repo-deployment-checkpoints](cross-repo-deployment-checkpoints/); do not delete those historical records when refreshing this file.

## Five-repository state

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | 206597ce321f9e228317120b100f65649a82f06c | #1314/#544/#541/#539 (draft planning/docs) | Inspection #42417844482 PASS; inspection PR #1421 merged at this SHA; validation #42417934488 PASS; manual reconcile #42417693554 PASS; recovery #42417863091 PASS. |
| TCE Dashboard | 7ab52078c4250829e158f05b2695ceb9d11bdbe3 | None | Native WF-06 #42417660167 FAIL (four public endpoints HTTP 503); native WF-07 #42417842240 PASS; latest native WF-12 #42411262379 FAIL/stale; workflow_run WF-12 #42417856773 PASS is not native evidence. |
| StockDividend | 783ae36f128ba5dffeba8ac1d242602f160ecfd0 | None | CI #42375688209 PASS (7/7); weekend scraper #42349150261 FAIL closed because VNSTOCK_API_KEY is missing. |
| Media Generation | 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d | None | CI #42239703151 PASS; no new immutable publisher/digest handoff. |
| Authentication | 3b60ff46b8959d18aee1956f99d6b62589b8b9c5 | #75 ready, #76 draft; both Supabase migration-gated | CI #42215394539 PASS; no new release/digest handoff. |

Platform PR #1421 (automated read-only inspection update) merged at 21:53:06 UTC from head b4997657bbcb913a7a21868abdd35e4f1531c351, producing master 206597ce321f9e228317120b100f65649a82f06c. Validation #42417934488 passed. The PR updates debug/vps-latest.md only.

## Native schedule delivery — event=schedule only

| Platform workflow | Latest native run | Result | Age at review | Budget |
|---|---|---|---:|---:|
| reconcile-vps.yml | #42407410735, 19:41:08Z | PASS | 2h14m31s | 45m |
| inspect-vps.yml | #42409592778, 20:08:29Z | PASS | 1h47m10s | 75m |
| reconcile-schedule-watchdog.yml | #42406561460, 19:30:43Z | FAIL | 2h24m56s | 45m |
| recover-stale-ops.yml | #42406469813, 19:29:42Z | PASS | 2h25m57s | 45m |

Latest inter-arrival gaps remain outside existing budgets: reconcile 14,624s; inspection 16,311s; watchdog 15,011s; recovery 15,306s. No newer Platform event=schedule was returned. Newer manual, push, workflow_run and repository_dispatch events do not count as native schedule delivery. Do not lower budgets or change cron expressions.

TCE schedule evidence:
- Native WF-06 #42417660167 at 21:49:14Z failed all four strict HTTP 200 probes with HTTP 503 (TCE web/API and Auth liveness/readiness). It is currently recent, but the gap from prior native WF-06 #42399835467 at 18:09:17Z was 13,197s (3h39m57s), above the 1,500s/25m budget. Another native cycle is needed to establish in-budget cadence.
- Native WF-12 #42411262379 at 20:29:03Z is stale and failed the WF-06 freshness check. Its prior native run #42392155494 at 16:36:34Z gives a 13,949s gap (3h52m29s), above its 1,500s budget. Workflow_run #42417856773 succeeded at 21:51:42Z but is not native schedule evidence; WF-13 #42417869841 was skipped.
- Native WF-07 #42417842240 at 21:51:31Z passed.
- Keep WF-06/WF-12 cron and strict HTTP 200 expectations unchanged. TCE market-scan schedule unchanged.

Stock weekend scraper cron remains 0 1 * * 0,6 UTC. The latest native scraper failed at the missing-secret preflight before dependencies or ingestion. Stock owner must add VNSTOCK_API_KEY and run preflight_only=true; do not ingest before authenticated non-guest entitlement passes. Media/Auth do not require native publisher schedules.

## Latest K3s snapshot and reconciliation

Read-only inspection #42417844482 succeeded and generated debug/vps-latest.md at 21:51:41Z. The snapshot is approximately four minutes old at this review.

- Node tce-k3s-01: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- Disk 56% used (about 20 GiB free); RAM available about 19 GiB.
- Media backend/frontend and MicroFE Shell/WS/NATS: Running.
- Stock Admin (two pods) and newer Stock Backend: ImagePullBackOff on tag 12d63b4; kubelet reports no matching ARM64 platform manifest. Older Stock Backend and Stock Frontend remain Running on 23b2878.
- TCE frontend/service, Auth and Keycloak remain intentional 0/0 maintenance. Public OIDC probes return HTTP 503.
- Platform and dedicated Media runner services are active/enabled; Media runner is not retired.
- Storage inventory shows only k3s-debug/k3s-debug-logs PVC/PV (1Gi); no Stock/Media VolumeSnapshot references were reported. This does not establish external backup/retention ownership.
- stock-prod and media-prod namespaces remain Active. Their Ingress host inventory requires separate authoritative DNS/provider owner review.
- Docker 29.1.3 and host containerd.io 2.2.1 have newer packages available; restart_required=yes. No upgrade/reboot or image cleanup was performed.

Manual reconcile #42417693554 completed successfully with ALLOW_IMAGE_CHANGES=false. Its job log confirms:
- GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE web/service.
- Auth runtime Secret provision/verification passed with values suppressed.
- Shared ghcr-pull remained unchanged.
- GitOps preflight found no manifest drift; production manifest apply and rollout were skipped.
- Stock Admin and newer Backend ImagePullBackOff remained visible.

Repository-dispatch recovery #42417863091 succeeded; this is not native schedule evidence.

## Ownership and immutable release contract

No new application publisher run, registry digest/provenance handoff or production image promotion was observed.

- TCE, Stock, Media and Auth own their application tests/builds and immutable GHCR publication where applicable.
- Platform Infra alone owns production manifests, shared GHCR pull credentials, runtime Secret provisioning, source/digest/provenance validation, GitOps promotion/reconciliation, rollout and health verification.
- Stock and Media remain retired from active Platform GitOps. Do not reintroduce their images/workloads.
- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml is read-only. No duplicate direct SSH/Compose deployment authority.

## Blockers and exact next actions

1. Platform owner: inspect GitHub runner registrations and audit log for unexpected registrations during the earlier short-lived runner registration-token validity window. Later masking/bootstrap verification passed, but the current connector cannot read the registration list; registry cleanliness is not certified.
2. GitHub Actions administrator: investigate missed Platform native schedule delivery; require another original native cycle and in-budget inter-arrival for each workflow. Do not count fallback/manual events.
3. TCE/GitHub Actions owner: observe next native WF-06/WF-12 cycles. Service owner must approve restoration before any replica change; retain strict HTTP 200 gates.
4. Stock owner: add VNSTOCK_API_KEY and run scraper preflight_only=true; no ingestion before authenticated non-guest entitlement passes.
5. Auth/Supabase owner: resolve migration provenance and integration side effects before PR #75/#76 are retargeted or merged.
6. Stock/Media owners: provide external backup/retention and authoritative DNS/provider evidence; retire the dedicated Media runner (idle, stopped, disabled, unregistered) before any namespace deletion.
7. Platform operator: use fresh read-only inspection for subsequent decisions; Docker/containerd upgrade/reboot requires a separate maintenance window.

Protected Stock/Media decommission remains manual-only. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, new secret write, DNS/database/storage mutation or host maintenance occurred in this review. Auth runtime Secret provisioning/verification in #42417693554 was performed by the existing authorized reconciliation workflow; values were suppressed. TCE market-scan schedule unchanged.

Detailed evidence: docs/cross-repo-deployment-checkpoints/2026-11-08-0455-ict.md
