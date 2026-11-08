# Cross-repo production deployment readiness

Current review: **2026-11-08 06:58 ICT / 2026-11-07 23:58 UTC**

This is the rolling operational summary. Preserve timestamped evidence under [docs/cross-repo-deployment-checkpoints](cross-repo-deployment-checkpoints/).

## Five-repository state

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `fe5c0deba7c955167060c4ddb35229eacbf6aa04` | #1314/#544/#541/#539 (draft planning/docs) | PR #1427 merged; native inspection #42427239949 PASS. Native reconcile #42423799465 PASS but 12,392s inter-arrival and 50m41s current age exceed 45m. Native watchdog #42423187797 FAIL; recovery #42423100821 PASS. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-12 #42427247349 FAIL because WF-06 is stale. Latest native WF-06 #42417660167 FAIL; manual WF-06 #42427267317 also reports four HTTP 503 endpoints. WF-13 recovery #42427257920 PASS. |
| StockDividend | `783ae36f128ba5dffeba8ac1d242602f160ecfd0` | None | CI #42375688209 PASS (7/7). Weekend scraper #42349150261 FAIL closed because `VNSTOCK_API_KEY` is missing. Next cron: 2026-11-08 01:00Z / 08:00 ICT. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS; no recent immutable publisher run/digest handoff. Backend/frontend and dedicated runner remain active in K3s. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft; migration/integration gated | CI #42215394539 PASS. PR #75 validate PASS / Supabase Preview skipped; PR #76 validate PASS / Supabase Preview skipped. No recent release/digest handoff. |

## Recent Platform PRs

- [PR #1424](https://github.com/phanthienquoc/platform-infra/pull/1424) merged as `8e64f0710c857c53284be6e2ad3e675307d8ceef`; exact-head and post-merge validation passed.
- [PR #1425](https://github.com/phanthienquoc/platform-infra/pull/1425) merged as `769c558f2ded93979f6857ba35d5954404d25949`; read-only inspection snapshot only.
- [PR #1426](https://github.com/phanthienquoc/platform-infra/pull/1426) merged as `178e70157be3b0e347ac366fafe54c221c9df4cc`; exact-head #42424250124 and post-merge #42424282141 passed.
- [PR #1427](https://github.com/phanthienquoc/platform-infra/pull/1427) merged as current master `fe5c0deba7c955167060c4ddb35229eacbf6aa04`; exact inspection PR head `f7bfc3aa3ae2b93c3252820a3afaf3450a4fad2c`, manifest validation #42427319306 PASS. Changed `debug/vps-latest.md` only.

No PR above changed production manifests, application images, schedules, or workload replica counts.

## Platform native schedule delivery

Only original `event=schedule` runs on master count as native evidence. Manual, push, workflow_run and repository_dispatch are tracked separately.

| Workflow | Latest native run | Result | Inter-arrival gap | Current age | Budget |
|---|---|---|---:|---:|---:|
| reconcile-vps.yml | [#42423799465, 23:07:40Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42423799465) | PASS | 12,392s | 50m41s | 45m |
| inspect-vps.yml | [#42427239949, 23:53:04Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949) | PASS | 13,475s | 5m17s | 75m |
| reconcile-schedule-watchdog.yml | [#42423187797, 23:00:06Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42423187797) | FAIL | 12,563s | 58m15s | 45m |
| recover-stale-ops.yml | [#42423100821, 22:58:55Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42423100821) | PASS | 12,553s | 59m26s | 45m |

A fresh inspection event arrived at 23:53Z, but the gap from #42409592778 remains 13,475s (3h44m35s), far above the 75m inter-arrival budget. The latest workflow_run watchdog #42427358673 at 23:54:46Z failed the freshness/inter-arrival gate; it is not native evidence.

Recovery evidence:
- Native recovery #42423100821 passed, but its age now exceeds the 45m budget.
- TCE-triggered Platform recovery #42427253726 (repository_dispatch) validated the external heartbeat and dispatched [reconcile fallback #42427264491](https://github.com/phanthienquoc/platform-infra/actions/runs/42427264491) in `workflow_dispatch` apply mode, `target_app=all`, `allow_image_changes=false`.
- Fallback reconciliation passed; GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` was unchanged. The v15 core-only image-pull restart helper ran. GitOps preflight found no drift, so manifest apply and rollout were skipped.
- Recovery workflow_dispatch #42427458035 passed at 23:56:07Z. This is fallback activity, not native schedule evidence.

Keep native freshness budgets at 45/75/45/45 minutes. Do not lower budgets or count fallback/manual runs as cron delivery.

## TCE schedule and service health

- Native WF-06 [#42417660167](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42417660167) at 21:49:14Z remains the latest native healthcheck. Its gap from #42399835467 was 13,197s (3h39m57s); it failed all four strict HTTP 200 probes.
- Manual WF-06 [#42427267317](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42427267317) at 23:53:27Z also failed all four endpoints: TCE web, TCE API, Auth liveness and Auth readiness returned HTTP 503.
- Native WF-12 [#42427247349](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42427247349) at 23:53:10Z failed because native WF-06 delivery is stale. Its authenticated Platform heartbeat dispatch succeeded; WF-13 recovery #42427257920 succeeded. Heartbeat transport is not service health or native WF-06 delivery.
- WF-12 native gap from #42411262379 was 12,247s (3h24m07s), above its 1,500s budget.
- WF-07 backup #42419031555 and integration #42417842240 passed.

Keep WF-06/WF-12 schedules and strict HTTP 200 expectations unchanged. **TCE market-scan schedule unchanged.**

## Latest K3s snapshot

Read-only native inspection [#42427239949](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949) generated `debug/vps-latest.md` at 2026-11-07 23:53:12Z and was merged through PR #1427.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- RAM 23 GiB total / ~19 GiB available. Disk 45 GiB total / 26 GiB used / 20 GiB available (56%, normal pressure).
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. No cleanup performed.
- Host updates include Docker 29.9.3 and containerd.io 2.4.2-3; installed containerd.io 2.2.1-1. `restart_required=yes`. No upgrade/reboot.
- Platform and dedicated Media runner services are active/enabled; runner policy is `rollout-status-v15-core-workloads`.
- Media backend/frontend: Running 1/1. MicroFE Shell/WS/NATS: Running 1/1.
- TCE frontend/service, Auth service and Keycloak remain intentional 0/0 maintenance.
- Stock Admin: 0/1; both observed pods are ImagePullBackOff on `12d63b4`, with kubelet reporting no ARM64 manifest.
- Stock Backend: deployment reports 1/1 available, but a pod on desired image `12d63b4` is ImagePullBackOff while an older `23b2878` pod remains Running. Do not treat the desired revision as healthy.
- Stock Frontend: 1/1 Running on `23b2878`.
- `stock-prod` and `media-prod` remain Active. Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB, Bound); no Stock/Media VolumeSnapshot references. This does not prove external backup/retention completeness or DNS ownership.

The runner's v15 `restart-blocked-image-pulls` policy allowlists only core `microfe-platform` and `tce-prod` deployments; the regression test explicitly rejects Stock/Media restart or rollout authority. Stock/Media remain outside active GitOps.

## Immutable publication and dispatch contracts

- TCE WF-03 is manual-only; app repo owns ARM64 builds, full-SHA/version tags, web/service digest verification and `tce-release-requested`. Platform validates the digest-bound receiver payload and owns promotion/reconciliation.
- Authentication `release.yml` is manual-only; app repo owns ARM64 publication, provenance/SBOM and digest verification before `auth-image-published`. Platform owns runtime Secrets, manifests, promotion and rollout.
- Stock `deploy.yml` retains ARM64/full-SHA publication checks, but Stock is retired from active Platform GitOps and has no active production handoff.
- Media WF-03 retains ARM64/full-SHA digest verification and intentionally sends no Platform dispatch while retired from active GitOps.
- No fresh app publisher run, digest/provenance handoff or production image promotion was observed in this checkpoint. Static workflow review is not publication evidence.

## Ownership, blockers and exact next actions

1. **Platform owner:** audit runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived registration-token validity window. PR #1416 masks the token before output and later bootstrap verification showed masked output; registry cleanliness is not certified.
2. **GitHub Actions administrator:** investigate delayed/missed Platform native schedule delivery. Keep the existing budgets and require in-budget original native cycles.
3. **TCE/service owner:** investigate four HTTP 503 endpoints and restore native WF-06 cadence. Obtain explicit approval before any replica change.
4. **Stock owner:** add `VNSTOCK_API_KEY`, run `run_scraper.yml` with `preflight_only=true`, and confirm authenticated non-guest entitlement before ingestion. Without the secret, the next weekend cron will fail closed.
5. **Auth/Supabase owner:** resolve migration provenance and connected GitHub integration side effects before PR #75/#76 are retargeted or merged.
6. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence. Retire the dedicated Media runner (idle, stopped, disabled and unregistered) before namespace deletion.
7. **Platform operator:** schedule a maintenance window for Docker/containerd upgrade/reboot. Do not clean images without retention and rollback evidence.

Stock/Media decommission remains manual-only. Deletion requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

## Authority and safety boundary

- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- The only fallback reconciliation in this checkpoint ran through that authority with `allow_image_changes=false`; GitOps drift was clean, so manifest apply and rollout were skipped.
- The authorized reconciliation workflow provisioned/verified the Auth runtime Secret with values suppressed; shared `ghcr-pull` was explicitly unchanged.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.
- No duplicate direct SSH/Compose deployment authority was added.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0658-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0658-ict.md)
