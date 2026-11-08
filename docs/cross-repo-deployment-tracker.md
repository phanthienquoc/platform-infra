# Cross-repo production deployment readiness

Current review: **2026-11-08 09:04 ICT / 2026-11-08 02:04 UTC**

Rolling operational summary. Preserve timestamped evidence under `docs/cross-repo-deployment-checkpoints/`.

## Repository state and open PRs

| Repository | Master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `06342dcea22a22b622d9d83361c160578e0fdbd3` | #1314, #544, #541, #539 (draft planning/docs) | PR #1430 is merged at this SHA. Master validation #42433130386 PASS. Latest reconciliation fallback #42432741608 PASS; native schedules stale. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-06 #42432710149 failed all four strict HTTP 200 probes with HTTP 503. Manual WF-06 #42432739134 also failed. |
| StockDividend | `783ae36f128ba5dffeba8ac1d242602f160ecfd0` | None | CI #42375688209 PASS (7/7). Scraper #42349150261 failed closed because VNSTOCK_API_KEY is absent; no 2026-11-08 01:00Z scheduled run appeared in latest run history. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS; no recent immutable publisher run/digest handoff. Backend/frontend and dedicated runner were still active in latest K3s evidence. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | CI #42215394539 PASS. PR #75 validate PASS / Supabase Preview skipped; #76 validate PASS / Supabase Preview skipped. Merge remains gated on migration/integration side effects. |

Open Platform PRs are unchanged: #1314, #544, #541 and #539. They are draft planning/documentation work, not deployment changes.

## Platform PR and validation evidence

- [PR #1430](https://github.com/phanthienquoc/platform-infra/pull/1430) is merged; merge SHA and current master are `06342dcea22a22b622d9d83361c160578e0fdbd3`.
- Exact-head validation #42433095783: PASS.
- Post-merge validation #42433130386: PASS.
- No open cross-repo deployment PR remains on Platform at this review.
- This checkpoint and rolling summaries are documentation-only; no application manifests, image tags, schedules, secrets, replicas, DNS, storage or host state are changed.

## Platform native schedule delivery

Only original `event=schedule` runs on master, attempt 1, with the exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch are separate evidence classes.

| Workflow | Native cron (UTC) | Latest native run | Result | Inter-arrival gap | Age at review | Budget |
|---|---|---|---|---:|---:|---:|
| reconcile-vps.yml | `7,22,37,52 * * * *` | [#42423799465](https://github.com/phanthienquoc/platform-infra/actions/runs/42423799465), 2026-11-07 23:07:40Z | PASS | 12,392s | ~2h56m | 45m |
| inspect-vps.yml | `2,32 * * * *` | [#42427239949](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949), 2026-11-07 23:53:04Z | PASS | 13,475s | ~2h11m | 75m |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | [#42423187797](https://github.com/phanthienquoc/platform-infra/actions/runs/42423187797), 2026-11-07 23:00:06Z | FAIL | 12,563s | ~3h04m | 45m |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | [#42423100821](https://github.com/phanthienquoc/platform-infra/actions/runs/42423100821), 2026-11-07 22:58:55Z | PASS | 12,553s | ~3h05m | 45m |

No newer native Platform schedule run appears in the latest Actions history inspected at 02:04Z. Watchdog logs previously confirmed `reconcile-vps.yml` was enabled, but no scheduled reconcile run fell inside the 45m budget. This is schedule delivery/freshness evidence, not proof that a workflow is disabled. Do not lower budgets, alter cron or count fallback/manual events as native delivery.

## Recovery and reconciliation evidence

- TCE native WF-06 [#42432710149](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42432710149) emitted a schedule heartbeat at 01:05:27Z. Platform recovery [#42432731030](https://github.com/phanthienquoc/platform-infra/actions/runs/42432731030) validated the payload and dispatched the existing reconcile authority.
- [Reconciliation fallback #42432741608](https://github.com/phanthienquoc/platform-infra/actions/runs/42432741608) ran on master SHA `4b829d7390be0cde0915c40c748b9c9ebdf1f091` with `mode=apply`, `target_app=all`, `allow_image_changes=false`; final deployment gate PASS.
- Job steps show GHCR pull access preflight PASS for Auth, MicroFE Shell/WS and TCE web/service; Auth runtime Secret provision/verification PASS with values suppressed; shared `ghcr-pull` bootstrap reported unchanged; TCE release pairing PASS.
- GitOps preflight reported no drift. Production manifest apply and image-change guard were skipped. Scoped image-pull restart policy step completed; Auth/MicroFE/TCE lane rollout checks were skipped where no rollout was required. MicroFE health passed; Auth and TCE were explicitly treated as intentional zero-replica maintenance, not live service health. Keycloak lane skipped.
- Reconciliation inventory at 01:06:14Z observed Media backend/frontend and MicroFE Shell/WS/NATS Running; Stock Admin and desired Stock Backend pods remained ImagePullBackOff; an older Stock Backend pod and Stock Frontend remained Running.
- Post-reconciliation recovery [#42432855950](https://github.com/phanthienquoc/platform-infra/actions/runs/42432855950) passed, but it did not dispatch an inspection fallback because the native inspection was 74m old at its 01:07:40Z reference time. That inspection is now stale; obtain a fresh read-only inspection through the existing authority.

## TCE schedule and service health

- Native WF-06 [#42432710149](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42432710149), 2026-11-08 01:05:27Z, failed all four independent public probes: TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 (expected 200). Job log for Auth readiness confirms HTTP 503.
- Its gap from prior native WF-06 #42417660167 was 11,773s, above the 25m freshness budget.
- Manual WF-06 #42432739134 also failed.
- Native WF-12 [#42427247349](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42427247349) at 23:53:10Z remains the latest native watchdog run and failed its stale-WF-06 gate. Workflow_run WF-12 #42432723982 and WF-13 #42432723943 passed, but neither is native schedule evidence or endpoint health.
- Keep WF-06 cron (`*/15 * * * *`), WF-12 cron and strict HTTP 200 expectations unchanged. **TCE market-scan schedule unchanged.**

## Stock, Media and Authentication

### StockDividend
- CI #42375688209: 7/7 PASS.
- Scraper #42349150261 failed at `Require VNStock API key before installing dependencies`; job log shows `VNSTOCK_API_KEY` empty. Dependency installation, entitlement verification and ingestion were correctly skipped.
- Exact next action: Stock owner adds repository secret `VNSTOCK_API_KEY`, runs `run_scraper.yml` with `preflight_only=true`, and verifies authenticated non-guest entitlement before ingestion. Do not fabricate or transfer secret values.
- Weekend scraper cron remains `0 1 * * 0,6` UTC. No 2026-11-08 01:00Z run appeared in the latest Actions run history.

### Media Generation
- CI #42239703151 PASS; no fresh immutable publisher run/digest handoff.
- Latest formal K3s inspection showed Media backend/frontend and dedicated Media runner active. Keep runner and namespace until external backup/retention, DNS ownership and runner retirement evidence are supplied.

### Authentication
- Master CI #42215394539 PASS.
- PR #75 head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`: validate PASS; Supabase Preview skipped (2026-10-27). PR remains open and ready.
- PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`: validate PASS; Supabase Preview skipped (2026-11-01). PR remains draft.
- Do not merge #75 until the Supabase integration target and merge-triggered migration effects are verified with the owner.

## Latest K3s evidence and limitations

Latest formal read-only inspection remains [#42427239949](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949), generated at 2026-11-07 23:53:12Z. It is stale at this review; no fresh inspection artifact was found.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- RAM ~19 GiB available; disk 56%, ~20 GiB available.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1; updates available and `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform runner and dedicated Media runner active/enabled.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1.
- TCE frontend/service, Auth service and Keycloak remain intentional 0/0.
- Stock Admin has two ImagePullBackOff pods on `12d63b4`; desired Stock Backend pod on `12d63b4` ImagePullBackOff while older `23b2878` pod remains Running; Stock Frontend Running on `23b2878`. Kubelet previously reported no ARM64 manifest for `12d63b4`.
- `stock-prod` and `media-prod` remain Active. Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB, Bound); no Stock/Media VolumeSnapshot references. This does not prove external backup/retention completeness or DNS ownership.
- The 01:06:14Z reconciliation inventory corroborates workload state but is not a replacement for fresh read-only inspection.

## Immutable publication and dispatch contracts

- TCE WF-03 remains manual-only; app repo owns ARM64 builds, full-SHA/version tags, web/service digest verification and `tce-release-requested`. Platform validates source-run identity and digest-bound payloads and owns production promotion/reconciliation.
- Authentication `release.yml` remains manual-only; app repo owns ARM64 publication, provenance/SBOM and digest verification before `auth-image-published`. Platform owns runtime Secrets, manifests, promotion and rollout.
- Stock deploy workflow retains ARM64/full-SHA publication checks, but Stock is retired from active Platform GitOps and has no active production handoff.
- Media WF-03 retains ARM64/full-SHA digest verification and intentionally sends no Platform dispatch while retired from active GitOps.
- No fresh app publisher run, digest/provenance handoff or production image promotion was observed in this review. Static workflow review is not publication evidence.

## Owners and exact next actions

1. **Platform owner:** audit runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived registration-token validity window. PR #1416 masks future output; registry cleanliness is not certified.
2. **GitHub Actions administrator:** investigate delayed/missed Platform native schedule delivery. Keep 45/75/45/45m budgets and require in-budget original native cycles.
3. **Platform operator:** obtain a fresh read-only K3s inspection through `inspect-vps.yml`; do not use reconciliation as a substitute for formal inspection.
4. **TCE/service owner:** investigate four HTTP 503 endpoints and restore native WF-06/WF-12 cadence. Obtain explicit approval before any replica change.
5. **Stock owner:** add `VNSTOCK_API_KEY`, run safe preflight, confirm authenticated non-guest entitlement, and investigate the missing 2026-11-08 01:00Z scraper event before ingestion.
6. **Auth/Supabase owner:** verify the connected GitHub integration target/effect before merging PR #75; keep #76 draft.
7. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence. Retire the dedicated Media runner (idle, stopped, disabled and unregistered) before namespace deletion.
8. **Platform operator:** schedule a maintenance window for Docker/containerd upgrade/reboot. Do not clean images without retention and rollback evidence.

Stock/Media decommission remains manual-only. Deletion requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

## Authority and safety boundary

- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout and health.
- No duplicate direct SSH/Compose deployment authority.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this review.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0904-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0904-ict.md)
