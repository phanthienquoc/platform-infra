# Cross-Repository Production Deployment Tracker

Last reviewed: **2026-11-08 13:09 ICT / 06:09 UTC**

This rolling tracker distinguishes native schedule events from manual, push, workflow_run and repository_dispatch fallbacks. Timestamped evidence is archived under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Master SHA | Open PRs | Readiness evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `374222f2c9685528c6783c480e5df01e22b457de` | #1438 (this update), #1314, #544, #541, #539 (draft planning/docs) | PR #1435 and #1437 merged. Exact-head and post-merge checks passed. PR #1438 corrects push-smoke summary wording and refreshes tracker. |
| phanthienquoc/TCE-dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-06 #42432710149 stale; manual #42452331522 failed four strict HTTP 200 probes with 503. Native WF-12 #42452308083 failed stale-WF-06 freshness. WF-07 scheduled #42453060493 passed and heartbeat reached Platform. |
| phanthienquoc/stockdividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | PR #38 merged; master CI #42440810105 PASS 7/7. Scraper #42349150261 failed closed because `VNSTOCK_API_KEY` was empty; Sunday 01:00Z run absent. |
| phanthienquoc/media-generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS. Inspection #42452273701 shows backend/frontend 1/1 Running and dedicated Media runner active. |
| phanthienquoc/phanthienquoc-authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | CI #42215394539 PASS. Supabase Preview skipped; #75 remains gated on merge-triggered migration/integration side effects. |

## Current actions

1. **Platform/GitHub Actions:** PR #1438 makes push-only watchdog output explicitly warning-only when native schedule gaps exist. Preserve strict non-push failure semantics, cron, concurrency and 45/75/45/45m budgets.
2. **GitHub Actions administrator:** investigate native schedule delivery gaps across Platform and TCE WF-06/WF-12; workflows are enabled and queue diagnostics show no excessive delay.
3. **Platform owner:** audit runner registrations and GitHub audit log after the earlier short-lived registration-token exposure window.
4. **TCE/service owner:** investigate four HTTP 503 endpoints; any replica restoration requires explicit approval and rollback plan.
5. **Stock owner:** add `VNSTOCK_API_KEY`, run `run_scraper.yml` with `preflight_only=true`, and verify authenticated non-guest entitlement before ingestion.
6. **Auth/Supabase owner:** verify integration target and merge-triggered migration effects before PR #75; keep #76 draft.
7. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence; retire the dedicated Media runner before namespace deletion.
8. **Platform operator:** schedule Docker/containerd maintenance with rollback/retention evidence before cleanup, upgrade or reboot.

## Current runtime blockers

- **Native schedule delivery:** Platform native reconcile/watchdog/recovery exceed freshness budgets; inspection #42452273701 is fresh by age but its inter-arrival gap is 21,396s versus 75m. TCE WF-06 was 17,798s (296m) old at WF-12 run #42453071754 against 25m, with queue 0m and enabled check passing.
- **TCE/Auth health:** four public endpoints returned HTTP 503. K3s snapshot shows TCE frontend/service and Auth/Keycloak intentional 0/0; no live health is asserted and no replicas are scaled.
- **Stock scraper:** missing `VNSTOCK_API_KEY`; safe preflight must pass before ingestion. No Sunday 2026-11-08 01:00Z run appears in recent Actions history.
- **Stock legacy workloads:** Admin (two pods) and desired Backend pod ImagePullBackOff on `12d63b4`; kubelet reports no matching platform manifest. Stock remains retired from active Platform GitOps.
- **Stock/Media decommission:** external backup/retention, authoritative DNS ownership and fresh PVC/PV/VolumeSnapshot evidence are incomplete; Media runner retirement is not proven.
- **Authentication migration:** PR #75/#76 must not merge solely on CI; Supabase Deploy to production is reported ON and merge-triggered migration effects remain unverified.
- **Host maintenance:** Docker/containerd updates are available and `restart_required=yes`; no maintenance window/rollback evidence exists.

## Platform PR and validation evidence

- [PR #1435](https://github.com/phanthienquoc/platform-infra/pull/1435) merged at `f1791584f9e02fe0e0d2e43308239ee95c7b4a97`; exact-head manifest validation #42453399594 and post-merge #42453440188 PASS.
- [PR #1437](https://github.com/phanthienquoc/platform-infra/pull/1437) merged at current master `374222f2c9685528c6783c480e5df01e22b457de`; exact-head checks #42453536660/#42453536676 PASS.
- Post-merge checks #42453579947 (manifests) and #42453579869 (workflow contracts) PASS. Push smoke #42453579901 PASS and emitted warnings for all four Platform gaps plus TCE WF-06/WF-12 gaps.
- The merged watchdog's push smoke ended with "All Platform native schedule inter-arrival checks passed" because `--warn-only` returns zero. That wording is misleading; PR #1438 corrects it. Warning annotations did list the gaps.

## Native schedule acceptance

Only original `event=schedule`, master, attempt 1 runs with exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch remain separate.

| Workflow | Native cron (UTC) | Latest native run | Result | Inter-arrival gap | Age at 06:09Z | Budget |
|---|---|---|---:|---:|---:|---:|
| `reconcile-vps.yml` | `7,22,37,52 * * * *` | [#42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803), 02:34:10Z | PASS | 12,390s | ~215m | 45m |
| `inspect-vps.yml` | `2,32 * * * *` | [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701), 05:49:40Z | PASS | 21,396s | ~20m | 75m |
| `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | [#42438566387](https://github.com/phanthienquoc/platform-infra/actions/runs/42438566387), 02:26:41Z | FAIL | 12,395s | ~223m | 45m |
| `recover-stale-ops.yml` | `10,25,40,55 * * * *` | [#42438384072](https://github.com/phanthienquoc/platform-infra/actions/runs/42438384072), 02:24:08Z | PASS | 12,313s | ~225m | 45m |

Push smoke #42453579901 reported warnings for all four Platform gaps and TCE WF-06/WF-12 gaps (11,773s and 21,421s). It is diagnostic only and does not satisfy native cadence acceptance.

TCE WF-06 latest native remains #42432710149; WF-12 latest native remains #42452308083. WF-07 scheduled integration #42453060493 passed at 06:01:55Z; its WF-12 workflow_run #42453071754 failed stale-WF-06 freshness and WF-13 #42453081086 recovered. Platform recovery #42453078467 authenticated the heartbeat and avoided duplicate fallback dispatches.

## Reconciliation and GHCR credentials

- Native reconcile #42439099803 passed at 02:34:10Z but is outside its 45m freshness budget.
- Workflow_dispatch reconciliation #42452324950 passed at 05:50:26Z on prior master SHA `5513c0bc...`; not native evidence.
- GHCR pull preflight, Auth runtime Secret provision/verification, shared pull-credential bootstrap, scoped image-pull restart and TCE release pairing passed. Manifest apply and image-change guard skipped; no image promotion or production manifest change.
- Platform recovery #42453078467 verified the TCE WF-07 source and WF-12 heartbeat; at 06:02Z it observed reconciliation 9m old and fresh native inspection, so no duplicate fallback was dispatched.
- TCE/Auth remain intentional zero-replica maintenance; a green maintenance lane is not live-service health.

## TCE schedule and service health

- WF-06 cron remains `*/15 * * * *`. Native #42432710149 failed; manual #42452331522 at 05:50:31Z failed all four strict HTTP 200 probes with 503.
- WF-12 cron remains `7,22,37,52 * * * *`. Native #42452308083 failed stale-WF-06 freshness. Workflow_run #42453071754 measured WF-06 age 17,798s (296m), queue 0m, workflow enabled.
- WF-07 scheduled #42453060493 passed; authenticated heartbeat reached Platform. WF-13 #42453081086 and Platform recovery #42453078467 passed; these do not repair native WF-06 cadence.
- Do not scale TCE/Auth replicas without owner approval and rollback plan. TCE market-scan schedule unchanged.

## StockDividend

- PR #38 merged; master CI #42440810105 PASS 7/7, including ARM64 non-publishing builds.
- Publisher uses full-SHA and `prod-v<version>-<full-sha>` tags, digest equality and ARM64 checks; registry-side tag immutability enforcement is not certified.
- Weekend scraper cron remains `0 1 * * 0,6` UTC. #42349150261 failed closed because `VNSTOCK_API_KEY` was empty; no Sunday 01:00Z run appeared in recent history.
- Stock owner must supply the key, run `preflight_only=true`, verify authenticated non-guest entitlement before ingestion. Stock remains retired from active Platform GitOps.

## Media Generation

- Master CI #42239703151 PASS (last recorded app CI).
- Inspection #42452273701 shows backend/frontend 1/1 Running with digest-resolved image IDs and dedicated Media runner active/enabled.
- Media remains retired from active Platform GitOps, but legacy namespace/workloads and runner remain present. No new publisher/digest handoff.
- Do not remove namespace/runner until external backup/retention, authoritative DNS/provider ownership, runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight.

## Authentication

- Master CI #42215394539 PASS (last recorded app CI).
- PR #75 remains ready/open; PR #76 remains draft/open. Prior validation passed; Supabase Preview skipped.
- Keep both gated until Supabase integration target and merge-triggered migration effects are authoritatively verified safe.

## Latest K3s inspection and host state

Read-only inspection #42452273701 generated `debug/vps-latest.md` at 05:49:48Z and merged via PR #1436. Snapshot age is ~20m, within the 75m age budget; inter-arrival cadence remains outside budget.

- Node `tce-k3s-01` Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2.
- RAM ~19 GiB available; disk 56%, ~21 GiB available.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1; updates available; `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform and Media runner services active/enabled. Runner registration/audit-log review after earlier token exposure remains outstanding.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1.
- Stock Admin: two pods ImagePullBackOff on `12d63b4`; desired Backend pod on `12d63b4` ImagePullBackOff while old `23b2878` backend remains Running 1/1; Frontend Running on `23b2878`. Kubelet reports `no match for platform in manifest`.
- TCE frontend/service, Auth service and Keycloak intentional 0/0; no live health asserted.
- `stock-prod` and `media-prod` namespaces Active; no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership are not proven. No decommission or host maintenance.

## Immutable publication and dispatch ownership

- TCE WF-03 remains manual-only; app repo owns ARM64 build, full-SHA/version tags, web/service digest verification and `tce-release-requested`. Platform validates source-run identity and digest-bound payloads before GitOps promotion.
- Auth `release.yml` remains manual-only; app repo owns ARM64 publication, provenance/SBOM and digest verification before `auth-image-published`. Platform owns runtime Secrets, manifests, promotion, rollout and health.
- Stock PR #38 enforces full-SHA + version/full-SHA tags and digest equality for all three components; no Platform dispatch while retired.
- Media retains app-owned ARM64 publication/digest checks and intentionally sends no Platform dispatch while retired.
- No new publisher run, GHCR publication, digest handoff or production image promotion.

## Authority and safety boundary

- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout and health.
- No duplicate direct SSH/Compose deployment authority.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this review.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-1309-ict.md](cross-repo-deployment-checkpoints/2026-11-08-1309-ict.md)


---

## Current execution update — 2026-11-08 13:57 ICT / 06:57 UTC

Repository heads and open PRs were re-read before this update. Platform master is `9f6618f8736ab14d58595436faa87944cc45bb4d`; this checkpoint branch is based on that exact head. Current open PRs: Platform Infra #1314/#544/#541/#539; Authentication #75/#76. TCE, StockDividend and Media Generation have no open PRs.

### Latest Actions evidence

- Platform latest push smoke [#42454041525](https://github.com/phanthienquoc/platform-infra/actions/runs/42454041525) passed at 06:16:09Z on master `9f6618f8`. It is diagnostic-only and emitted warning-only schedule observations; it is not native schedule acceptance.
- Platform native reconcile [#42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803) passed at 02:34:10Z; latest native watchdog [#42438566387](https://github.com/phanthienquoc/platform-infra/actions/runs/42438566387) failed at 02:26:41Z; latest native recovery [#42438384072](https://github.com/phanthienquoc/platform-infra/actions/runs/42438384072) passed at 02:24:08Z. Their native inter-arrival gaps remain 12,390s / 12,395s / 12,313s against 2,700s budgets. No later native run appears in the current Actions history.
- Platform native inspection [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701) passed at 05:49:40Z. Its snapshot age is ~68m at this review, inside the 75m age budget, but the native inter-arrival gap is 21,396s against 4,500s. Do not confuse freshness-by-age with cadence acceptance.
- TCE native WF-07 [#42453060493](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42453060493) passed at 06:01:55Z. WF-12 [#42452308083](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42452308083) failed at 05:50:11Z; workflow_run watchdog #42453071754 failed freshness; WF-13 recovery #42453081086 passed. Latest manual WF-06 #42452331522 still returned HTTP 503 on all four strict probes. WF-06 latest native remains #42432710149.
- Stock master CI [#42440810105](https://github.com/phanthienquoc/stockdividend/actions/runs/42440810105) passed. Latest scraper schedule [#42349150261](https://github.com/phanthienquoc/stockdividend/actions/runs/42349150261) failed closed due to missing `VNSTOCK_API_KEY`. The Sunday 2026-11-08 scheduled run is not yet visible at 06:57Z; because the previous Saturday run was itself created at 06:56:29Z, record this as delayed/not-yet-observed rather than declaring a missed run at this instant.
- Media master CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) passed (latest recorded app CI; no new publisher run).
- Authentication master CI [#42215394539](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215394539) passed. PR #75 exact head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` has Auth CI #40446492086 PASS; PR #76 exact head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` has Auth CI #41329425940 PASS. PR #75 remains gated by the owner-confirmed Supabase GitHub integration with Deploy to production enabled on master; #76 remains draft. A green CI run does not resolve the external integration side-effect gate.

### Current safety disposition

- Latest K3s snapshot remains read-only inspection #42452273701. It is within age budget but not new enough to establish current health beyond that snapshot. Previously observed Stock ARM64 ImagePullBackOff, Media/MicroFE running, and TCE/Auth intentional 0/0 remain the latest recorded workload evidence.
- No new GHCR publication, digest handoff or production promotion is present. Stock CI is non-publishing.
- No production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation, host cleanup/upgrade/reboot, or direct SSH/Compose deployment authority was used.
- Next dependency-safe actions remain: GitHub Actions administrator investigates native schedule delivery; Platform owner audits runner registration after token exposure; Stock owner provisions `VNSTOCK_API_KEY` and runs `preflight_only=true`; service owners investigate TCE/Auth 503 under an approved activation/rollback plan; Supabase owner verifies PR #75 merge-triggered integration behavior; app owners supply backup/DNS/runner evidence before Stock/Media decommission.
- TCE market-scan schedule unchanged.
