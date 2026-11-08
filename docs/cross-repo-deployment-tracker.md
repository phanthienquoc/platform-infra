# Cross-repo production deployment readiness

Current review: **2026-11-08 08:08 ICT / 2026-11-08 01:08 UTC**

This is the rolling operational summary. Preserve timestamped evidence under docs/cross-repo-deployment-checkpoints/.

## Five-repository state

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | 4b829d7390be0cde0915c40c748b9c9ebdf1f091 | #1314, #544, #541, #539 (planning/docs) | PR #1429 merged; post-merge validation #42432731313 PASS. TCE heartbeat recovery #42432731030 PASS; existing-authority fallback reconciliation #42432741608 PASS. Native Platform schedules remain stale. |
| TCE Dashboard | 7ab52078c4250829e158f05b2695ceb9d11bdbe3 | None | Native WF-06 #42432710149 failed all four strict HTTP 200 probes with HTTP 503. Workflow_run watchdog #42432723982 and recovery #42432723943 passed; neither is native schedule evidence. |
| StockDividend | 783ae36f128ba5dffeba8ac1d242602f160ecfd0 | None | CI #42375688209 PASS (7/7). Scraper #42349150261 failed closed because VNSTOCK_API_KEY is missing. No new scheduled scraper run for 2026-11-08 01:00Z was present by this review. |
| Media Generation | 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d | None | CI #42239703151 PASS; no recent immutable publisher run/digest handoff. Backend/frontend and dedicated runner remain active in K3s. |
| Authentication | 3b60ff46b8959d18aee1956f99d6b62589b8b9c5 | #75 ready, #76 draft; migration/integration gated | CI #42215394539 PASS. PR #75 validate PASS / Supabase Preview skipped; #76 validate PASS / Supabase Preview skipped. No recent release/digest handoff. |

## Recent Platform PR

- [PR #1429](https://github.com/phanthienquoc/platform-infra/pull/1429) squash-merged as 4b829d7390be0cde0915c40c748b9c9ebdf1f091.
- Exact PR head: df4970f61c1ded80b48e39bc7888affe0102f6c6.
- Exact-head validation #42428112841: PASS.
- Post-merge master validation #42432731313: PASS.
- Changed only the deployment tracker, workflow inventory and timestamped checkpoint. No production manifests, application images, schedules, secrets, workload replicas, DNS, storage or host state changed.

## Platform native schedule delivery

Only original event=schedule runs on master, attempt 1, with the exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch remain separate evidence classes.

| Workflow | Latest native run | Result | Inter-arrival gap | Age at review | Budget |
|---|---|---|---:|---:|---:|
| reconcile-vps.yml | [#42423799465, 23:07:40Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42423799465) | PASS | 12,392s | 2h00m31s | 45m |
| inspect-vps.yml | [#42427239949, 23:53:04Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949) | PASS | 13,475s | 75m07s | 75m |
| reconcile-schedule-watchdog.yml | [#42423187797, 23:00:06Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42423187797) | FAIL | 12,563s | 2h08m05s | 45m |
| recover-stale-ops.yml | [#42423100821, 22:58:55Z](https://github.com/phanthienquoc/platform-infra/actions/runs/42423100821) | PASS | 12,553s | 2h09m16s | 45m |

No newer native Platform schedule event appeared in the latest Actions query. The inspection age crossed its 75m run-age budget just after the last recovery check; recovery #42432855950 checked at 01:07:40Z, observed 74m, and correctly did not dispatch a fallback at that time. Re-evaluate on the next recovery cycle. Do not count fallback/manual runs as native delivery or lower freshness budgets.

## Recovery and production reconciliation evidence

- TCE native WF-06 #42432710149 (2026-11-08 01:05:27Z) produced an authenticated schedule heartbeat. Platform recovery [#42432731030](https://github.com/phanthienquoc/platform-infra/actions/runs/42432731030) validated the source payload and dispatched the existing reconcile authority.
- [Reconciliation fallback #42432741608](https://github.com/phanthienquoc/platform-infra/actions/runs/42432741608) ran on master SHA 4b829d7390be0cde0915c40c748b9c9ebdf1f091 with mode=apply, target_app=all and allow_image_changes=false. All jobs and the final deployment gate passed.
- GHCR pull access preflight passed for Auth, MicroFE Shell/WS and TCE web/service. Auth runtime Secret was provisioned and verified with values suppressed. Both observed ghcr-pull Secrets were unchanged. TCE release pairing passed.
- GitOps preflight reported drift=false. Production manifest apply, image-change guard and rollout were skipped. MicroFE health passed. Auth and TCE were explicitly verified as intentional zero-replica maintenance; no live service health is asserted. Keycloak lane was skipped.
- The reconciliation log at 01:06:14Z observed Media backend/frontend and MicroFE Shell/WS/NATS Running; Stock Admin pods and the desired Stock Backend pod remained ImagePullBackOff; an older Stock Backend pod and Stock Frontend remained Running.
- Post-reconciliation recovery [#42432855950](https://github.com/phanthienquoc/platform-infra/actions/runs/42432855950) passed. Its inspection-age check saw native inspection #42427239949 at 74m at reference time 01:07:40Z, so it did not dispatch a read-only fallback. This does not repair native schedule delivery.

## TCE schedule and service health

- Native WF-06 [#42432710149](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42432710149) at 01:05:27Z failed all four independent public probes: TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 (expected 200).
- Its gap from the previous native WF-06 #42417660167 was 11,773s, above the 25m freshness budget.
- Native WF-12 [#42427247349](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42427247349) at 23:53:10Z remains the latest native WF-12 run and failed the stale-WF-06 gate; its gap from #42411262379 was 12,247s.
- WF-12 workflow_run diagnostic #42432723982 and WF-13 recovery #42432723943 passed after the new WF-06 event. These are workflow_run evidence, not native schedule delivery or endpoint health.
- Manual WF-06 #42432739134 also failed. Keep WF-06 cron, WF-12 cron and strict HTTP 200 expectations unchanged. **TCE market-scan schedule unchanged.**

## Latest K3s and runtime evidence

The latest formal read-only native inspection remains [#42427239949](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949), which generated debug/vps-latest.md at 2026-11-07 23:53:12Z and was merged through PR #1427. No newer inspection artifact is available.

- Node tce-k3s-01: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- RAM about 19 GiB available; disk 56%, about 20 GiB available.
- Docker 29.1.3; 20 images / 9.195 GB, about 5.773 GB reclaimable. Host containerd.io 2.2.1; updates available and restart_required=yes. No cleanup, upgrade or reboot.
- Platform and dedicated Media runner services active/enabled.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1.
- TCE frontend/service, Auth service and Keycloak remain intentional 0/0.
- Stock Admin has two ImagePullBackOff pods on 12d63b4; kubelet previously reported no ARM64 manifest. Stock Backend has an older 23b2878 pod Running and a desired 12d63b4 pod ImagePullBackOff. Stock Frontend remains Running on 23b2878.
- stock-prod and media-prod remain Active. Only reported PVC/PV is k3s-debug/k3s-debug-logs (1 GiB, Bound); no Stock/Media VolumeSnapshot references. This does not prove external backup/retention completeness or DNS ownership.
- The 01:06:14Z reconciliation inventory corroborated the pod states above but is not a replacement for a fresh read-only inspection artifact.

## Immutable publication and dispatch contracts

- TCE WF-03 remains manual-only; the app repo owns ARM64 builds, full-SHA/version tags, web/service digest verification and tce-release-requested. Platform validates digest-bound payloads and owns production promotion/reconciliation.
- Authentication release.yml remains manual-only; the app repo owns ARM64 publication, provenance/SBOM and digest verification before auth-image-published. Platform owns runtime Secrets, manifests, promotion and rollout.
- Stock deploy.yml retains ARM64/full-SHA publication checks, but Stock is retired from active Platform GitOps and has no active production handoff.
- Media WF-03 retains ARM64/full-SHA digest verification and intentionally sends no Platform dispatch while retired from active GitOps.
- No fresh app publisher run, digest/provenance handoff or production image promotion was observed in this checkpoint. Static workflow review is not publication evidence.

## Ownership, blockers and exact next actions

1. Platform owner: audit runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived registration-token validity window. PR #1416 masks future output; registry cleanliness is not certified.
2. GitHub Actions administrator: investigate delayed/missed Platform native schedule delivery. Keep 45/75/45/45m budgets and require in-budget original native cycles.
3. TCE/service owner: investigate four HTTP 503 endpoints and restore native WF-06/WF-12 cadence. Obtain explicit approval before any replica change.
4. Stock owner: add VNSTOCK_API_KEY, run run_scraper.yml with preflight_only=true, and confirm authenticated non-guest entitlement before ingestion. The expected 2026-11-08 01:00Z scraper schedule run was not present in Actions history by 01:08Z; re-check delivery and secret state.
5. Auth/Supabase owner: verify the connected GitHub integration target/effect before merging PR #75; keep #76 draft. Both validation jobs pass but Supabase Preview is skipped, and merge-triggered migration effects remain unresolved.
6. Stock/Media owners: provide external backup/retention and authoritative DNS/provider evidence. Retire the dedicated Media runner (idle, stopped, disabled and unregistered) before namespace deletion.
7. Platform operator: schedule a maintenance window for Docker/containerd upgrade/reboot. Do not clean images without retention and rollback evidence.

Stock/Media decommission remains manual-only. Deletion requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

## Authority and safety boundary

- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
- The only reconciliation in this checkpoint used the existing authority with allow_image_changes=false. GHCR preflight passed, shared ghcr-pull was unchanged, GitOps drift was clean, and manifest apply/rollout were skipped.
- No GHCR publication/promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.
- No duplicate direct SSH/Compose deployment authority was added.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0808-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0808-ict.md)
