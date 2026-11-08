# Cross-repo production deployment readiness

Current review: **2026-11-08 12:59 ICT / 2026-11-08 05:59 UTC**

Rolling operational summary. Timestamped evidence is archived under `docs/cross-repo-deployment-checkpoints/`. Native schedule events are distinguished from manual, workflow_run and repository_dispatch fallbacks.

## Repository state and open PRs

| Repository | Master SHA | Open PRs | Latest evidence |
|---|---|---|---|
| Platform Infra | `7db5471cf3bead65d36c61e3ce622b2b56e00f62` | #1435 (this refresh), #1437 (watchdog diagnostics), #1314, #544, #541, #539 (draft planning/docs) | Inspection PR #1436 merged at current master. Native inspection #42452273701 PASS at 05:49:40Z. PR #1437 adds all-schedule failure aggregation; exact-head checks are queued. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-06 #42432710149 still stale and failed; manual WF-06 #42452331522 failed all four HTTP 200 probes with 503. Native WF-12 #42452308083 ran at 05:50:11Z but failed its stale-WF-06 gate. |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | Master CI #42440810105 PASS 7/7 after PR #38. Scraper #42349150261 failed closed because `VNSTOCK_API_KEY` was empty; no Sunday 01:00Z scraper run appears in the recent Actions history. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS. Fresh K3s inspection #42452273701 shows backend/frontend 1/1 Running and dedicated Media runner active. No new publisher/digest handoff. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | CI #42215394539 PASS. Supabase Preview skipped on prior PR validation; #75 remains gated on merge-triggered migration/integration side effects. |

Platform PR #1436 is merged; #1435 is being refreshed against current master. #1437 is a separate workflow-diagnostics change. TCE, Stock and Media have no open PRs. Authentication #75/#76 remain open and must not be merged solely on CI status.

## Platform PR and validation evidence

- [PR #1436](https://github.com/phanthienquoc/platform-infra/pull/1436) merged the fresh read-only inspection snapshot at master SHA `7db5471cf3bead65d36c61e3ce622b2b56e00f62`; source run [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701) passed inspection, snapshot validation, exact inspection PR-head validation and squash merge.
- [PR #1435](https://github.com/phanthienquoc/platform-infra/pull/1435) previously passed exact-head validation [#42449461420](https://github.com/phanthienquoc/platform-infra/actions/runs/42449461420), but its branch was based on the previous master `5513c0bc...`. This refresh rebases its documentation-only change onto current master and replaces the stale 12:02 evidence.
- [PR #1437](https://github.com/phanthienquoc/platform-infra/pull/1437) changes only `.github/workflows/reconcile-schedule-watchdog.yml`. It aggregates all Platform native schedule-gap results instead of stopping at the first failed verifier. Exact-head validation runs [#42453182985](https://github.com/phanthienquoc/platform-infra/actions/runs/42453182985) and [#42453182986](https://github.com/phanthienquoc/platform-infra/actions/runs/42453182986) were queued at review.
- No application manifests, image references, schedule expressions, secrets, replicas, DNS, storage or host state are changed by this readiness refresh.

## Platform native schedule delivery

Only original `event=schedule`, master, attempt 1 runs with the exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch events remain separate.

| Workflow | Native cron (UTC) | Latest native run | Result | Inter-arrival gap | Age at 05:59Z | Budget |
|---|---|---|---|---:|---:|---:|
| `reconcile-vps.yml` | `7,22,37,52 * * * *` | [#42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803), 02:34:10Z | PASS | 12,390s | ~205m | 45m |
| `inspect-vps.yml` | `2,32 * * * *` | [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701), 05:49:40Z | PASS | 21,396s | ~9m | 75m |
| `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | [#42438566387](https://github.com/phanthienquoc/platform-infra/actions/runs/42438566387), 02:26:41Z | FAIL | 12,395s | ~212m | 45m |
| `recover-stale-ops.yml` | `10,25,40,55 * * * *` | [#42438384072](https://github.com/phanthienquoc/platform-infra/actions/runs/42438384072), 02:24:08Z | PASS | 12,313s | ~215m | 45m |

The fresh inspection #42452273701 is within its current age budget, but its 21,396s gap from prior native inspection #42427239949 still violates the 75m inter-arrival contract. A workflow_run watchdog [#42452390618](https://github.com/phanthienquoc/platform-infra/actions/runs/42452390618) at 05:51:27Z is not native; it confirmed reconcile enabled, queue/runner diagnostics and latest inspection freshness, then failed on stale native reconcile/recovery and the first inter-arrival check.

The recovery controller [#42452477069](https://github.com/phanthienquoc/platform-infra/actions/runs/42452477069) passed as workflow_dispatch at 05:52:49Z. It observed a recent reconciliation fallback and the fresh native inspection, so it avoided duplicate dispatches. This does not repair native cadence. The last native reconcile remains #42439099803; the last native recovery remains #42438384072.

The workflow-enabled, queue and runner-assignment checks passed; no excessive runner queue was identified. The evidence points to GitHub Actions native schedule delivery/freshness, not a reason to change runner assignment. Preserve all cron expressions, concurrency isolation and 45/75/45/45m budgets.

## Latest reconciliation and GHCR credentials

- Latest native reconcile [#42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803) passed at 02:34:10Z but is outside its 45m freshness budget.
- Latest reconciliation overall [#42452324950](https://github.com/phanthienquoc/platform-infra/actions/runs/42452324950) was a successful `workflow_dispatch` at 05:50:26Z on older source SHA `5513c0bc61f999e48e257169ae7b133c65fa8191`; it is not native schedule evidence and predates inspection master `7db5471c`.
- That fallback passed GHCR pull-access preflight, Auth runtime Secret provision/verification, shared GHCR pull-credential bootstrap, image-pull restart step and TCE release pairing. Manifest apply and image-change guard were skipped; no image promotion or production manifest change occurred.
- Recovery controller #42452477069 verified the recent reconciliation and fresh native inspection and did not dispatch duplicate fallbacks.
- TCE and Auth remain intentional zero-replica maintenance. A green maintenance lane is not a claim of live endpoint health. No Stock/Media workload was brought back into active Platform GitOps.

## TCE schedule and service health

- WF-06 cron remains `*/15 * * * *`. Latest native WF-06 [#42432710149](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42432710149) was created at 01:05:27Z and failed its four strict public HTTP 200 probes.
- Manual WF-06 [#42452331522](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42452331522) at 05:50:31Z also failed all four endpoints: TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503.
- WF-12 cron remains `7,22,37,52 * * * *`. Latest native WF-12 [#42452308083](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42452308083) at 05:50:11Z failed because latest native WF-06 was 17,084s old (284m) against a 25m budget; its queue wait was 0m and WF-06 enabled check passed.
- WF-12 sent its authenticated heartbeat to Platform successfully. WF-13 recovery [#42452318480](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42452318480) passed as workflow_run; neither is native WF-06 evidence.
- Latest K3s snapshot shows TCE frontend/service and Auth/Keycloak at intentional 0/0. Do not scale them without service-owner approval and a reviewed rollback plan. Keep strict HTTP 200 checks and all TCE schedules unchanged.

## StockDividend

- PR #38 is merged at `e6469ac6617142b349144101a1192cb6aa7104ad`; master CI [#42440810105](https://github.com/phanthienquoc/stockdividend/actions/runs/42440810105) PASS 7/7, including ARM64 non-publishing builds.
- Publisher now emits full-SHA and `prod-v<version>-<full-sha>` tags for scraper/admin/backend, verifies both tags resolve to one SHA-256 digest and expose `linux/arm64`, and no longer creates new mutable `latest`, short-SHA or plain-semver aliases. Registry-side tag immutability enforcement is not certified; existing tags were not deleted.
- Weekend scraper cron remains `0 1 * * 0,6` UTC. Last recorded scraper run [#42349150261](https://github.com/phanthienquoc/stockdividend/actions/runs/42349150261) failed closed because `VNSTOCK_API_KEY` was empty. No Sunday 2026-11-08 01:00Z run appeared in the recent Actions history.
- Exact next action: Stock owner supplies `VNSTOCK_API_KEY`, runs `run_scraper.yml` with `preflight_only=true`, and verifies authenticated non-guest entitlement before ingestion. Stock remains retired from active Platform GitOps; no production handoff or workload mutation is authorized.

## Media Generation

- Master CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) PASS (last recorded app CI).
- Fresh inspection #42452273701 shows backend/frontend 1/1 Running with digest-resolved image IDs and the dedicated Media runner service active/enabled.
- Media remains retired from active Platform GitOps, but legacy namespace/workloads and runner remain present. No new publisher/digest handoff.
- Do not remove namespace or runner until external backup/retention, authoritative DNS/provider ownership, runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight are recorded.

## Authentication

- Master CI [#42215394539](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215394539) PASS (last recorded app CI).
- PR #75 head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` remains ready/open; PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` remains draft/open. Prior validation passed; Supabase Preview was skipped.
- Keep both gated: the connected Supabase integration is reported as Deploy to production ON, while merge-triggered migration behavior has not been authoritatively confirmed safe. Do not merge either solely on CI status.

## Latest K3s inspection and host state

Latest formal read-only inspection [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701) generated `debug/vps-latest.md` at 2026-11-08 05:49:48Z and merged through inspection PR #1436. This snapshot is current within the 75m age budget at review, but the native inter-arrival gap remains outside budget.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- RAM ~19 GiB available; disk 56%, ~21 GiB available.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1; available updates include containerd.io 2.4.2-3 and Docker 29.9.3; `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform and dedicated Media runner services are active/enabled. Runner registration/audit-log review after the earlier short-lived token exposure remains outstanding.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1.
- Stock Admin: two pods ImagePullBackOff on `12d63b4`; desired Stock Backend pod on `12d63b4` ImagePullBackOff while old `23b2878` backend remains Running 1/1; Stock Frontend Running on `23b2878`. Kubelet events say `no match for platform in manifest`; failed pods have no resolved image digest.
- TCE frontend/service, Auth service and Keycloak remain intentional 0/0. No live TCE/Auth health is asserted.
- `stock-prod` and `media-prod` namespaces remain Active. No Stock/Media VolumeSnapshot references were found; this does not prove external backup/retention or DNS ownership. No namespace/PVC/PV deletion or runner retirement.
- No host cleanup, upgrade or reboot.

## Immutable publication and dispatch ownership

- TCE WF-03 remains manual-only; TCE owns ARM64 build, full-SHA/version tags, web/service digest verification and `tce-release-requested`. Platform verifies source-run identity and digest-bound payloads before GitOps promotion.
- Authentication `release.yml` remains manual-only; Auth owns ARM64 publication, provenance/SBOM and digest verification before `auth-image-published`. Platform owns runtime Secrets, manifests, promotion, rollout and health.
- Stock PR #38 enforces full-SHA + version/full-SHA tags and digest equality for all three components; no Platform dispatch because Stock is retired from active GitOps.
- Media retains app-owned ARM64 publication/digest checks and intentionally sends no Platform dispatch while retired.
- No new publisher run, GHCR publication, digest handoff or production image promotion was observed in this review.

## Exact next actions

1. **GitHub Actions administrator:** investigate persistent native schedule delivery gaps for Platform and TCE WF-06/WF-12. Preserve cron, native-event filters and all freshness budgets; the latest checks show workflow-enabled and queue/runner diagnostics passing.
2. **Platform operator:** continue read-only `inspect-vps.yml` and reconcile through existing authority; monitor the next native cycles. Manual fallbacks do not satisfy native cadence.
3. **Platform owner:** audit runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived registration-token validity window.
4. **TCE/service owner:** investigate HTTP 503 and decide whether/when to restore replicas with explicit approval and rollback plan.
5. **Stock owner:** add `VNSTOCK_API_KEY`, run safe preflight, verify authenticated non-guest entitlement and investigate missing scheduled delivery before ingestion.
6. **Auth/Supabase owner:** verify integration target and merge-triggered migration effects before PR #75; keep #76 draft.
7. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence; retire the dedicated Media runner (idle, stopped, disabled and unregistered) before namespace deletion.
8. **Platform operator:** schedule Docker/containerd maintenance with rollback/retention evidence before cleanup, upgrade or reboot.

Stock/Media decommission remains manual-only. Deletion requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight.

## Authority and safety boundary

- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout and health.
- No duplicate direct SSH/Compose deployment authority.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this review.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-1259-ict.md](cross-repo-deployment-checkpoints/2026-11-08-1259-ict.md)
