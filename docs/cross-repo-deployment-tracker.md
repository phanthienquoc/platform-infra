# Cross-Repository Production Deployment Tracker

Last reviewed: **2026-11-08 19:05 ICT / 12:05 UTC**

This rolling tracker distinguishes native schedule events from manual, push, workflow_run and repository_dispatch fallbacks. Timestamped evidence is archived under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Master SHA | Open PRs | Readiness evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 25c5e390161c5410517f5360885281abd4c1ff49 | #1314/#544/#541/#539 (draft planning/docs) | PR #1461 merged at 25c5e390 after exact-head validation #42478273907 PASS; post-merge master validation #42478553173 PASS. PRs #1458/#1459/#1460 remain merged. Latest reconciliation #42474936543 PASS with no drift/apply/promotion; latest inspection #42475079478 PASS. |
| phanthienquoc/TCE-dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-06 #42458256899 failed four HTTP 503 probes; native WF-12 #42452308083 failed freshness; WF-07 integration #42453060493 PASS. No newer native WF-06/WF-12 event. TCE/Auth remain intentional 0/0; no live health asserted. |
| phanthienquoc/stockdividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | Master CI #42440810105 PASS 7/7, including non-publishing ARM64 build. Native scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is empty; logs confirm dependency installation, entitlement check and ingestion were skipped. Legacy Admin and desired Backend remain ImagePullBackOff on `12d63b4` (no linux/arm64 manifest). |
| phanthienquoc/media-generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS. Inspection #42475079478 shows backend/frontend 1/1 and in-cluster storage preflight clean; dedicated runner remains active/listening. PR #1458's remote runner-registration guard is merged, but `MEDIA_RUNNER_AUDIT_TOKEN`, external backup/retention and authoritative DNS evidence remain unverified. |
| phanthienquoc/phanthienquoc-authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 draft/open | PR #75 merged at `cb907a63` after exact-head CI #42478511082 PASS (validation + ARM64 non-publishing build; Supabase Preview skipped). Post-merge master CI #42478653766 is running. Supabase project remains ACTIVE_HEALTHY; 84/84 migration versions match repository; no migration count change observed after merge. PR #76 remains draft. |

## Current actions

1. **Platform/cert-manager:** PR #1453 merged as ab2696c2d08945af0dc86145ade00ec973510ae1. Exact-head #42470921373/#42470921319/#42470921336 passed; post-merge #42471706415 (manifest), #42471706454 (workflow lint) and #42471706467 (Keycloak) all passed. Optional read-only GH_TOKEN authenticates the checksum-pinned release asset API; the token is not logged and PR write permission is isolated.
2. **Platform/decommission:** PR #1452 merged and the sudo fix is now verified by read-only inspection #42471706668. Snapshot debug/vps-latest.md generated 10:30:37Z; inspection PR #1454 exact head aea66b05d0418cdcff745dbd13cdd852536492b2 passed #42471833649 and merged at 77207c26536cb005b2cbcbaf19945ded5069c0df. Preflight reached both target namespaces and passed storage-clean: no Stock/Media PVC claims, PV claims or VolumeSnapshot references. The Media runner is still active/enabled/listening; external backup/retention and authoritative DNS ownership remain unverified, so no decommission.
3. **Platform reconciliation:** recovery-dispatched run #42471718647 completed SUCCESS with mode=apply, target_app=all, allow_image_changes=false. GHCR access for Auth, MicroFE and TCE images passed; Auth runtime Secret was provisioned/verified; shared ghcr-pull unchanged. ServiceAccount/deployment patches were no-op, no active Auth/MicroFE/TCE image-pull failures were found, TCE release pairing passed, preflight reported no drift and production manifest apply was skipped. MicroFE, TCE and Auth lanes plus final gate passed; recovery-controller notification job completed successfully in #42471978667.
4. **GitHub Actions administrator:** investigate missing/delayed native Platform and TCE WF-06/WF-12 schedule delivery; preserve cron and freshness budgets.
5. **Platform owner:** audit runner registrations and GitHub audit log after the earlier short-lived registration-token exposure window.
6. **TCE/service owner:** investigate four HTTP 503 endpoints; any replica restoration requires explicit approval and rollback plan.
7. **Stock owner:** add `VNSTOCK_API_KEY`, run `run_scraper.yml` with `preflight_only=true`, and verify authenticated non-guest entitlement before ingestion.
8. **Auth/Supabase owner:** verify integration target and merge-triggered migration effects before PR #75; keep #76 draft.
9. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence; retire and unregister the dedicated Media runner before namespace deletion.
10. **Platform operator:** schedule Docker/containerd maintenance with rollback/retention evidence before cleanup, upgrade or reboot.

## Current runtime blockers

- **Cert-manager release asset API:** PR #1453 resolved the post-merge HTTP 403 with optional read-only GitHub token propagation. Exact-head and post-merge manifest validation, workflow lint and Keycloak checks all PASS; latest tracker and workflow-ownership PRs #1455/#1456 also passed exact-head validation and post-merge manifest validation #42472161449/#42472328823.
- **Native schedule delivery:** no newer native Platform/TCE schedule events appeared through 10:38Z. Latest Platform native runs remain reconcile #42467231073 (09:27:03Z, FAIL), inspection #42452273701 (05:49:40Z, PASS), watchdog #42467080859 (09:24:53Z, FAIL), recovery #42466737776 (09:20:06Z, PASS). At 10:40Z their ages are ~73m / 290m / 75m / 80m against 45/75/45/45m budgets; inter-arrival gaps remain ~24,773s / 21,396s / 25,092s / 24,958s. TCE WF-06 #42458256899 and WF-12 #42452308083 remain stale. Manual/push/workflow_run events do not count.
- **TCE/Auth health:** WF-06 #42458256899 returned HTTP 503 for TCE web, TCE API, Auth liveness and Auth readiness. K3s shows TCE frontend/service, Auth and Keycloak at intentional 0/0; no live health is asserted and no replicas are scaled.
- **Stock scraper:** native run #42457182511 failed closed because `VNSTOCK_API_KEY` was empty before dependency installation. Safe preflight must pass before ingestion.
- **Stock legacy workloads:** snapshot #42468887549 shows two Stock Admin pods and the desired Backend pod in ImagePullBackOff on `12d63b4`; kubelet reports `no match for platform in manifest`. Older Backend and Frontend remain Running 1/1. Stock remains retired from active Platform GitOps.
- **Stock/Media decommission:** fresh inspection #42471706668 confirms the sudo boundary works and the read-only storage preflight passes: no PVC/PV claims or VolumeSnapshot references in stock-prod or media-prod; tce-prod and microfe-platform were preserved. This is not deletion approval: external backup/retention and authoritative DNS/provider evidence are still missing, and the dedicated Media runner remains active/enabled with listener present.
- **Authentication migration:** PR #75/#76 must not merge solely on CI; Supabase merge-triggered migration/integration effects remain unverified.
- **Host maintenance:** snapshot reports Docker 29.1.3, host containerd.io 2.2.1 with 2.4.2-3 available, ~5.77 GB reclaimable and `restart_required=yes`; no maintenance window/rollback evidence exists.

## Platform PR and validation evidence

- [PR #1435](https://github.com/phanthienquoc/platform-infra/pull/1435) merged at `f1791584f9e02fe0e0d2e43308239ee95c7b4a97`; exact-head manifest validation #42453399594 and post-merge #42453440188 PASS.
- [PR #1437](https://github.com/phanthienquoc/platform-infra/pull/1437) merged at current master `374222f2c9685528c6783c480e5df01e22b457de`; exact-head checks #42453536660/#42453536676 PASS.
- Post-merge checks #42453579947 (manifests) and #42453579869 (workflow contracts) PASS. Push smoke #42453579901 PASS and emitted warnings for all four Platform gaps plus TCE WF-06/WF-12 gaps.
- The merged watchdog's push smoke ended with "All Platform native schedule inter-arrival checks passed" because `--warn-only` returns zero. That wording is misleading; PR #1438 corrects it. Warning annotations did list the gaps.

## Native schedule acceptance

Only original `event=schedule`, master, attempt 1 runs with exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch remain separate.

| Workflow | Native cron (UTC) | Latest native run | Result | Inter-arrival gap | Age at 10:40Z | Budget |
|---|---|---:|---:|---:|---:|---:|
| `reconcile-vps.yml` | `7,22,37,52 * * * *` | [#42467231073](https://github.com/phanthienquoc/platform-infra/actions/runs/42467231073), 09:27:03Z | FAIL (pre-fix cert-manager render) | 24,773s | ~73m | 45m |
| `inspect-vps.yml` | `2,32 * * * *` | [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701), 05:49:40Z | PASS | 21,396s | ~290m | 75m |
| `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | [#42467080859](https://github.com/phanthienquoc/platform-infra/actions/runs/42467080859), 09:24:53Z | FAIL | 25,092s | ~75m | 45m |
| `recover-stale-ops.yml` | `10,25,40,55 * * * *` | [#42466737776](https://github.com/phanthienquoc/platform-infra/actions/runs/42466737776), 09:20:06Z | PASS | 24,958s | ~80m | 45m |

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


---

## Latest execution update — 2026-11-08 15:04 ICT / 08:04 UTC

Repository state was re-read from GitHub before this checkpoint. Current master heads: Platform Infra `564d94bb9134195a0643274f8656d95161b47e02`, TCE Dashboard `7ab52078c4250829e158f05b2695ceb9d11bdbe3`, StockDividend `e6469ac6617142b349144101a1192cb6aa7104ad`, Media Generation `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`, Authentication `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.

### Open pull requests

- Platform Infra: #1314, #544, #541, #539 (all draft planning/documentation); inspection PR #1440 is merged.
- TCE Dashboard: none.
- StockDividend: none.
- Media Generation: none.
- Authentication: #75 ready/open, #76 draft/open. Their exact-head Auth CI runs #40446492086 and #41329425940 both report success; #75 remains gated by the unverified Supabase GitHub integration merge-trigger side effect.

### Latest Actions evidence

- Platform inspection [#42458425146](https://github.com/phanthienquoc/platform-infra/actions/runs/42458425146) completed successfully. It created inspection PR #1440 on branch `automation/vps-inspection-42458425146-1`; exact head `9cdfaddc66fbcb21a6ea7a78e05f44551726fa69` passed [manifest validation #42458510940](https://github.com/phanthienquoc/platform-infra/actions/runs/42458510940) and was squash-merged at `564d94bb9134195a0643274f8656d95161b47e02`. The PR changed only `debug/vps-latest.md`.
- Manual Platform reconciliation [#42458288651](https://github.com/phanthienquoc/platform-infra/actions/runs/42458288651) completed successfully with `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR pull access passed; Auth runtime Secret was provisioned/verified; shared `ghcr-pull` was unchanged; TCE release pairing passed. Preflight found no manifest drift, so production apply and drift apply were skipped. TCE and Auth health lanes explicitly reported intentional zero-replica maintenance and asserted no live health; active MicroFE health passed. This is not a production image promotion.
- Platform manual recovery #42458395401 passed after reconciliation; workflow_run watchdog/recovery diagnostics #42458307657/#42458317037 were skipped by their event gates. The latest Platform manifest validator #42458510940 passed on the exact inspection PR head. Combined commit-status queries returned no status contexts for the five current master SHAs; use the cited Actions runs as the available evidence.
- Platform latest native schedule runs remain reconcile #42439099803 (02:34:10Z, PASS), inspection #42452273701 (05:49:40Z, PASS), watchdog #42438566387 (02:26:41Z, FAIL), and recovery #42438384072 (02:24:08Z, PASS). At 08:04Z all four exceed their 45/75/45/45-minute freshness budgets. Inter-arrival gaps remain 12,390s / 21,396s / 12,395s / 12,313s. Manual inspection #42458425146 and manual reconciliation #42458288651 do not count as native schedule evidence. Cron and budgets are unchanged.
- TCE native WF-06 [#42458256899](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42458256899) ran at 07:18:37Z and failed all four public endpoint probes (TCE web, TCE API, Auth liveness, Auth readiness: HTTP 503). Manual WF-06 #42458279806 also failed. WF-12 workflow_run #42458270339 passed its delivery check: workflow active, latest scheduled WF-06 age 0m and queue 0m at that run, and Platform heartbeat accepted. WF-13 recovery #42458270097 passed. This confirms WF-06 delivery occurred at 07:18Z, not service health; by 08:04Z the latest WF-06 schedule is again older than the 25m freshness budget. Latest native WF-12 remains #42452308083 (05:50:11Z, failed/stale). WF-07 latest native #42453060493 passed at 06:01:55Z.
- Stock weekend scraper native schedule [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) was created at 07:03:12Z and failed before dependency installation because repository secret `VNSTOCK_API_KEY` was empty. The fail-closed behavior is correct; no key value was read or changed. Stock master CI #42440810105 remains PASS 7/7.
- Media master CI #42239703151 remains PASS; no new publisher run or digest handoff. Authentication master CI #42215394539 remains PASS; PR #75/#76 exact-head CI runs pass but the Supabase integration gate remains unresolved.

### Fresh K3s/host snapshot

The latest read-only inspection snapshot in `debug/vps-latest.md` was generated at 07:21:07Z and merged through PR #1440. At 08:04Z it is about 44 minutes old (inside the 75m snapshot-age budget), although native inspection cadence remains stale.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; ~19 GiB RAM available, disk 56% with ~21 GiB free.
- Media backend/frontend and MicroFE Shell/WS/NATS: Running 1/1. Platform and Media runner services: active/enabled; runner registration/audit review after prior token exposure remains outstanding.
- Stock Admin: two pods ImagePullBackOff; desired Stock Backend pod ImagePullBackOff on image `12d63b4`, while the older Backend and Frontend remain Running 1/1 on `23b2878`. Kubelet reports `no match for platform in manifest` for the failed image.
- TCE frontend/service, Auth service and Keycloak: intentional 0/0. Health-gate logs explicitly say no live workload health is asserted for these scopes.
- Stock/Media namespaces remain Active. No Stock/Media VolumeSnapshot references were found; only the k3s-debug PVC was listed. External backup/retention and DNS ownership are still unverified.
- Docker 29.1.3; 20 images / 9.195 GB with ~5.773 GB reclaimable. Host containerd.io 2.2.1 has an available update to 2.4.2-3; `restart_required=yes`. No cleanup, upgrade, reboot or decommission was performed.

### Current blockers and next actions

1. GitHub Actions administrator: investigate missing/delayed native Platform schedules; do not change cron or freshness budgets to mask delivery gaps.
2. Platform owner: audit runner registrations and GitHub audit log after the earlier registration-token exposure.
3. TCE service owner: investigate four HTTP 503 endpoints. No replica restoration without explicit approval and rollback plan; preserve strict HTTP 200 health checks.
4. Stock owner: add `VNSTOCK_API_KEY` as a repository secret, run `run_scraper.yml` with `preflight_only=true`, and verify authenticated non-guest entitlement before ingestion.
5. Supabase owner: authoritatively verify PR #75 merge-triggered integration/migration behavior before merge; keep #76 draft.
6. Stock/Media owners: provide external backup/retention and DNS/provider ownership evidence; retire the dedicated Media runner and complete fresh PVC/PV/VolumeSnapshot preflight before any decommission.
7. Platform operator: plan Docker/containerd maintenance with rollback and retention evidence before cleanup, upgrade or reboot.

No GHCR publication/promotion, production manifest mutation, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority was added. TCE market-scan schedule unchanged.


---

## Latest execution update — 2026-11-08 16:55 ICT / 09:55 UTC

Repository heads and open PRs were re-read from GitHub. Platform master is `1f7e5cd8ca52c34fc1fe57b90324137325188a5b`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Authentication `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.

- Open PRs: Platform #1452 (this fix), #1314/#544/#541/#539 (draft planning/docs); Authentication #75 ready and #76 draft; TCE/Stock/Media none. The older Platform documentation PR #1442 is being superseded because its 15:57Z snapshot is stale and its exact-head validation used the pre-cert-manager-fix base.
- PR #1452 branch `fix/decommission-preflight-sudo-20261108-1655-ict` changes only the decommission preflight script, its regression test and workflow-contract validator. The fresh inspection log for #42468887549 showed `error loading config file /etc/rancher/k3s/k3s.yaml: permission denied`; the script was invoking the root-owned wrapper without sudo. The fix defaults to `sudo /usr/local/sbin/platform-kubectl` and uses a fake sudo shim in tests. No Kubernetes delete operation was invoked.
- Native Platform schedule evidence: reconcile #42467231073 failed at 09:27:03Z on the old remote cert-manager URL; inspection #42452273701 passed at 05:49:40Z; watchdog #42467080859 failed at 09:24:53Z; recovery #42466737776 passed at 09:20:06Z. Inter-arrival gaps remain 24,773s / 21,396s / 25,092s / 24,958s. Current latest ages at 09:55Z are ~28m / 245m / 30m / 35m. Cadence acceptance still fails; cron and budgets are unchanged.
- Cert-manager failure is fixed on master by commit `312ab704`: the release asset is downloaded via the GitHub Release asset API, SHA-256 checked, and materialized locally for Kustomize. Fix-branch validations #42468403916/#42468403911 passed. Post-fix push-auto reconciliation #42468465293 passed: checksum-verified manifest prepared, Kubernetes state matched the repo, no drift; production apply and image promotion were skipped. The native #42467231073 failure predates this fix.
- Latest Platform push-auto reconciliation #42468465293 completed all targeted gates. GHCR pull preflight and Auth runtime Secret provisioning/verification passed; shared `ghcr-pull` remained unchanged. No drift, so no manifest apply, image promotion or rollout was performed. Zero-replica TCE/Auth lanes are not represented as live health.
- Latest read-only K3s inspection #42468887549 completed at 09:50:43Z; snapshot generated 09:50:50Z. Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; ~19 GiB RAM available, disk 56%/~21 GiB free. Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1. Stock Admin (two pods) and desired Backend on `12d63b4` ImagePullBackOff (`no match for platform in manifest`); older Stock Backend/Frontend Running 1/1. TCE frontend/service, Auth and Keycloak 0/0. Only the k3s-debug PVC/PV was listed; no Stock/Media PVC, PV claim or VolumeSnapshot references appeared in the snapshot. The decommission preflight stopped before target-namespace inventory due to the permission issue now fixed by #1452.
- Host snapshot: Docker 29.1.3; 20 images / 9.195 GB with ~5.773 GB reclaimable; host containerd.io 2.2.1 with 2.4.2-3 available; `restart_required=yes`. Platform and Media runner services active/enabled. No cleanup, upgrade, reboot or runner retirement.
- TCE native WF-06 #42458256899 (07:18:37Z) failed all four public HTTP 200 probes with 503; WF-12 native #42452308083 (05:50:11Z) failed freshness; WF-07 #42453060493 passed at 06:01:55Z. Workflow_run heartbeat success does not count as native cadence or service health.
- Stock native scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; master CI #42440810105 PASS 7/7 and is non-publishing. Media CI #42239703151 PASS. Auth CI #42215394539 PASS; PR #75/#76 exact-head CI #40446492086/#41329425940 PASS, but Supabase merge-trigger effects remain gated.
- No new GHCR publication, digest handoff or production promotion. No production manifest mutation, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


---

## Latest execution update — 2026-11-08 17:15 ICT / 10:15 UTC

- Platform master is `7ccd527ed2989c772f7ba7b2e0a97e1d615086ee`. PR #1452 merged after exact-head validation #42469900529 and #42469900449 passed. PR #1442 is closed as superseded. PR #1453 is open for the post-merge cert-manager release API 403.
- Post-merge `validate-github-actions` #42469989622 passed. Post-merge `validate-manifests` #42469989585 failed because `curl` received HTTP 403 from `api.github.com/repos/cert-manager/cert-manager/releases/assets/494156333` on four retries; render and SHA validation did not run. PR #1453 adds optional `GH_TOKEN` handling, passes the read-only token only to trusted helper callers, and moves PR-write permission to a separate no-checkout failure-comment job.
- Platform reconciliation [#42469998524](https://github.com/phanthienquoc/platform-infra/actions/runs/42469998524) completed successfully. GHCR pull access, Auth runtime Secret provision/verification, shared pull credentials and targeted deployment lanes passed. No GitOps drift, so production manifest apply, image promotion and rollout steps were skipped. TCE/Auth 0/0 does not establish live service health.
- The native Platform schedule history has not advanced since #42467231073/#42452273701/#42467080859/#42466737776. At 10:15Z all four latest events are beyond their age budgets; inter-arrival gaps remain 24,773s / 21,396s / 25,092s / 24,958s. Cron and budgets are unchanged. Native TCE WF-06/WF-12 remain stale; WF-06 last returned four HTTP 503s.
- Freshest K3s snapshot remains #42468887549 at 09:50:50Z. Node Ready/ARM64; Media and MicroFE workloads Running 1/1; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. The snapshot predates the #1452 sudo fix, so the decommission preflight still needs a new read-only run. No resource deletion or host maintenance.
- Stock scraper #42457182511 still fails closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 PASS. Auth CI #42215394539 PASS; PR #75/#76 remain gated by Supabase integration behavior.
- No new GHCR publication, digest handoff or production image promotion. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


---

## Latest execution update — 2026-11-08 17:31 ICT / 10:31 UTC

- Repository heads, open PRs, latest workflow runs and this tracker were re-read before implementation. Platform master is `ab2696c2d08945af0dc86145ade00ec973510ae1`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Authentication `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.
- Open PRs after merge: Platform #1314/#544/#541/#539 (draft planning/docs); Authentication #75 ready and #76 draft; TCE, Stock and Media none. Platform #1452 and #1453 are merged.
- PR #1453 [merged](https://github.com/phanthienquoc/platform-infra/pull/1453) at `ab2696c2d08945af0dc86145ade00ec973510ae1`, after exact-head #42470921373 (manifest validation), #42470921319 (workflow validation) and #42470921336 (Keycloak CI) all passed on head `3c1ff97d446473e94369fbfad560dafa21ad7f9e`. The change supplies optional read-only `GH_TOKEN` to the checksum-pinned cert-manager release asset downloader, redacts it from output, tests authenticated and anonymous paths, and isolates PR-comment write permission in a separate no-checkout job with only `pull-requests: write`.
- Post-merge runs on exact master SHA `ab2696c2`: manifest validation #42471706415 PASS (including checksum-pinned release preparation and Kustomize render); Keycloak CI #42471706467 PASS; workflow lint #42471706454 still in progress. Recovery push #42471706448 is still in progress and is not native schedule evidence.
- The PR #1453 path filter triggered fresh read-only inspection #42471706668. At the last check, its `Inspect VPS` step was still running; the new snapshot has not yet verified the #1452 sudo fix or produced a namespace inventory. The previous snapshot #42468887549 (09:50:50Z) remains the last completed K3s evidence: node Ready/ARM64; Media and MicroFE 1/1; Stock Admin and desired Backend ImagePullBackOff on `12d63b4`; older Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. No decommission is authorized from this snapshot.
- Native Platform schedule history has not advanced: reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776. At 10:31Z their ages are ~64m/~281m/~66m/~71m, beyond 45/75/45/45m freshness budgets. Inter-arrival gaps remain ~24,773s/~21,396s/~25,092s/~24,958s. Native TCE WF-06 #42458256899 still failed four HTTP 503 probes; WF-12 #42452308083 remains stale. No cron or freshness budget changed.
- Stock scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7 but is non-publishing. Media CI #42239703151 and Authentication CI #42215394539 PASS; Auth PR #75/#76 remain gated by Supabase merge-trigger effects.
- No new GHCR publication/digest handoff, production image promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


---

## Latest execution update — 2026-11-08 17:34 ICT / 10:34 UTC

- Current repository heads: Platform Infra 77207c26536cb005b2cbcbaf19945ded5069c0df; TCE Dashboard 7ab52078c4250829e158f05b2695ceb9d11bdbe3; StockDividend e6469ac6617142b349144101a1192cb6aa7104ad; Media Generation 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d; Authentication 3b60ff46b8959d18aee1956f99d6b62589b8b9c5. Open PRs: Platform #1455 (this tracker PR), #1314/#544/#541/#539 (draft); Auth #75 ready and #76 draft; TCE/Stock/Media none.
- PR #1453 merged at ab2696c2d08945af0dc86145ade00ec973510ae1 after exact-head manifest/workflow/Keycloak checks #42470921373/#42470921319/#42470921336 all passed. Post-merge #42471706415/#42471706454/#42471706467 all passed.
- Read-only inspection #42471706668 completed successfully and created snapshot at 10:30:37Z. Inspection PR #1454 exact head aea66b05d0418cdcff745dbd13cdd852536492b2 passed #42471833649 and squash-merged at 77207c26536cb005b2cbcbaf19945ded5069c0df. The sudo preflight reached stock-prod and media-prod, preserved tce-prod and microfe-platform, and returned storage-clean: no target PVC claims, PV claims or VolumeSnapshot references. The Media runner remains active/enabled/listening; backup/retention and authoritative DNS ownership are still unverified.
- Latest K3s snapshot: node tce-k3s-01 Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2. Media backend/frontend 1/1 Running; MicroFE Shell/WS/NATS 1/1 Running; Stock Admin (two pods) and desired Backend on 12d63b4 remain ImagePullBackOff (no matching ARM64 manifest), while old Backend 23b2878 and Frontend 23b2878 remain 1/1 Running. TCE frontend/service, Auth and Keycloak remain 0/0. Public OIDC probes returned HTTP 503. GitOps drift is clean.
- Recovery-dispatched reconciliation #42471718647 used mode=apply, target_app=all, allow_image_changes=false. GHCR access checks for Auth/MicroFE/TCE passed; Auth runtime Secret was provisioned/verified; shared ghcr-pull unchanged; ServiceAccount and deployment patches were no-op. The scoped blocked-image-pull restart found no failures in active Auth/MicroFE/TCE scopes. TCE release pairing passed. Preflight returned drift=false; production manifest apply and rollout were skipped. MicroFE, TCE and Auth lanes passed, including intentional zero-replica maintenance handling; final deployment lane gate passed. The recovery-controller notification job was still queued at the cutoff, so the top-level workflow had not yet reached completed.
- Native schedule history remains unchanged: Platform reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776; TCE WF-06 #42458256899 and WF-12 #42452308083. At 10:34Z Platform ages are ~67m/~284m/~69m/~74m, beyond 45/75/45/45m budgets; cadence gaps remain ~24,773s/~21,396s/~25,092s/~24,958s. TCE WF-06 still has four HTTP 503 probes and WF-12 remains stale. No cron/freshness budget changed.
- Stock scraper #42457182511 remains fail-closed on missing VNSTOCK_API_KEY; Stock CI #42440810105 PASS 7/7 but non-publishing. Media CI #42239703151 and Auth CI #42215394539 remain last recorded PASS; Auth PR #75/#76 remain gated by Supabase merge-trigger effects.
- No new GHCR publication/digest handoff, image promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only. TCE market-scan schedule unchanged.


## Scheduled image-cleanup evidence (not a cadence gate)

- Platform workflow vps-image-cleanup.yml has native cron 30 3 * * 0 (Sunday 03:30 UTC). The latest scheduled run [#42472343489](https://github.com/phanthienquoc/platform-infra/actions/runs/42472343489) was created at 10:39:26Z on Sunday 2026-11-08, about 7h09 after the cron time; this is additional evidence of delayed native schedule delivery.
- The schedule expression forces DRY_RUN=true for all non-workflow_dispatch events. The run completed PASS with KEEP_UNUSED_IMAGES=10 and output unused_images=8, retain=10, remove=0, dry_run=true. No images were removed.
- The script protects images referenced by Pods and all CRI containers, excludes pinned images, fails closed on unresolved non-terminal Pod references, and rechecks Pod/container references immediately before any deletion. A destructive cleanup requires an explicit manual workflow_dispatch with dry_run=false; none was invoked.


---

## Latest execution update — 2026-11-08 17:40 ICT / 10:40 UTC

- Platform master at this review: c473432c54b4a4a4fad5d7751a867738e1e2e300. PR #1455 merged at 4062cda; PR #1456 merged at c473432. Exact-head manifest validation #42472097818/#42472292633 and post-merge validation #42472161449/#42472328823 all PASS. Open Platform PRs remain #1314/#544/#541/#539 (draft planning/docs).
- The workflow-ownership audit confirms TCE WF-09 is a manual safe setup utility that uploads source only to the development path; WF-10 is explicitly staging-only and creates tce-stg plus its staging Secret. Preserve both; neither is a production deployment authority. Stock deploy.yml is an app-owned ARM64 immutable publisher with a manual-publication hold; Media WF-03 and Auth release.yml are also app-owned publishers. No workflow was removed.
- Fresh K3s snapshot #42471706668 (10:30:37Z) confirms node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin (two pods) and desired Backend on 12d63b4 ImagePullBackOff; old Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; OIDC HTTP 503; GitOps drift clean. Stock/Media storage preflight passed; Media runner remains active.
- Recovery-dispatched reconciliation #42471718647 completed SUCCESS; GHCR access and Auth runtime Secret checks passed; shared ghcr-pull unchanged; no active Auth/MicroFE/TCE pull failures; TCE release pairing passed; drift=false and production apply skipped; MicroFE/TCE/Auth lanes and final gate passed. Recovery controller #42471978667 completed SUCCESS.
- Weekly cleanup #42472343489 was scheduled for Sunday 03:30 UTC but created at 10:39:26Z (~7h09 late). It ran with DRY_RUN=true, KEEP_UNUSED_IMAGES=10 and found 8 unused images; remove_count=0. No images removed. The cleanup workflow is intentionally preserved; manual destructive mode was not invoked.
- Native Platform schedules remain reconcile #42467231073, inspection #42452273701, watchdog #42467080859 and recovery #42466737776; TCE WF-06 #42458256899 and WF-12 #42452308083. Platform ages at 10:40Z are ~73m/~290m/~75m/~80m, beyond 45/75/45/45m budgets. TCE WF-06 still has four HTTP 503 probes. No cron or freshness budget changed.
- Stock scraper #42457182511 remains fail-closed on missing VNSTOCK_API_KEY; Stock CI #42440810105 PASS 7/7 but non-publishing. Media CI #42239703151 and Auth CI #42215394539 remain PASS. Auth PR #75/#76 remain open; Supabase merge-trigger side-effect gate unresolved.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only. TCE market-scan schedule unchanged.



## Latest execution update — 2026-11-08 18:04 ICT / 11:04 UTC

- Re-inspected all five default-branch heads and open PRs. Platform master is `0636f70b4d08a951c9436d2e5642130c0dbe7b53`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Authentication `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.
- Open PRs: Platform #1314/#544/#541/#539 (draft planning/docs) and new #1458 (runner-retirement guard); Authentication #75 (ready/open) and #76 (draft); TCE, Stock and Media have no open PRs.
- Platform latest recorded validation #42472499466 PASS on master; latest weekly image-cleanup schedule #42472343489 PASS at 10:39:26Z, about 7h09 after its 03:30Z cron, with DRY_RUN=true and remove_count=0. No cleanup occurred.
- Native Platform schedule evidence remains reconcile #42467231073, inspection #42452273701, watchdog #42467080859 and recovery #42466737776. At 11:04Z their ages are approximately 97m/5h14m/99m/104m, beyond 45/75/45/45m budgets. Manual, push and workflow_run fallbacks are not native schedule acceptance.
- TCE latest native WF-06 #42458256899 failed strict HTTP 200 probes (four HTTP 503 endpoints); WF-12 native #42452308083 failed freshness. Workflow_run recovery #42458270097 passed but does not establish live service health. TCE/Auth remain intentional zero-replica maintenance; no scaling authorized.
- Stock scraper native run #42457182511 failed closed because `VNSTOCK_API_KEY` is missing. Stock master CI #42440810105 PASS 7/7 but is non-publishing. Media CI #42239703151 and Auth CI #42215394539 are the latest recorded PASS. No new immutable GHCR publication/digest handoff was observed.
- Latest K3s snapshot remains read-only inspection #42471706668 (10:30:37Z): node Ready/ARM64; Media and MicroFE workloads 1/1; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; TCE/Auth/Keycloak 0/0. It is not a new native inspection event.
- PR #1458 on branch `fix/verify-media-runner-registration-before-decommission-20261108` adds a read-only GitHub API check that the exact Media runner name `media-generation-k3s-01` is absent from `phanthienquoc/media-generation`, in addition to local systemd/Listener checks. Delete mode will require Platform secret `MEDIA_RUNNER_AUDIT_TOKEN` with fine-grained repository Administration:read on Media only; missing secret/API failure/registered runner fails closed. The token cannot unregister the runner. Plan mode remains read-only and does not require it.
- Backup/external-data ownership and authoritative DNS approval remain unverified. No namespace/PVC/PV deletion, runner stop/unregister, DNS/database/storage mutation, production manifest apply, workload scaling, image promotion or host maintenance occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.



## Execution follow-up — 2026-11-08 18:20 ICT / 11:20 UTC

### Merged changes

- Platform PR [#1458](https://github.com/phanthienquoc/platform-infra/pull/1458) merged by squash at `098cf54de9e2223bc97db57cca6fbee8334fc80c`. Exact head `892166b7b64aceea2e5d7b73ddd6f5e9cd83a5e3); exact-head `validate-github-actions` #42474849755 PASS and `validate-manifests` #42474849751 PASS; post-merge #42474925147 and #42474925187 PASS.
- PR [#1459](https://github.com/phanthienquoc/platform-infra/pull/1459) merged the read-only K3s inspection snapshot at `ef7a1a15b94acdaf7c46cbecb4aa2391cb90b0f8`. Its exact-head manifest validation #42475211696 PASS. It changed only `debug/vps-latest.md`; no workload or production manifest was changed.
- Current Platform master: `ef7a1a15b94acdaf7c46cbecb4aa2391cb90b0f8`.

### Reconciliation and rollout evidence

- Recovery-triggered reconciliation [#42474936543](https://github.com/phanthienquoc/platform-infra/actions/runs/42474936543) completed SUCCESS after a stale-schedule fallback. It used `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- GHCR pull preflight passed for Auth, MicroFE Shell/WS and TCE service/web. The shared `ghcr-pull` Secret was reported `unchanged` in both `microfe-platform` and `tce-prod`. Auth runtime Secret was provisioned and verified; values were suppressed.
- Production preflight found no GitOps manifest drift; production manifest apply and image promotion were correctly skipped. No image digest changed.
- Auth, MicroFE and TCE deployment lanes completed SUCCESS. Auth/MicroFE/TCE rollout steps were skipped because no rollout was required; TCE health verifier explicitly reported intentional zero-replica maintenance and **did not assert live workload health**. Keycloak lane remained skipped. The final deployment-lane gate passed.
- TCE GitOps image verification confirmed desired/live pair `prod-v0.1.0-e75e338` for web and service. This verifies the pinned pair, not endpoint availability.

### Fresh read-only K3s snapshot

Source: inspection fallback [#42475079478](https://github.com/phanthienquoc/platform-infra/actions/runs/42475079478), generated `2026-11-08T11:17:34Z`, committed through PR #1459.

- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`; disk 56% (~21 GiB free), available RAM ~19 GiB.
- `media-prod`: backend/frontend each 1/1 Running. `microfe-platform`: Shell/WS/NATS each 1/1 Running; Auth/Keycloak 0/0. `tce-prod`: frontend/service 0/0 maintenance.
- `stock-prod`: two Admin Pods and the newer Backend Pod remain ImagePullBackOff on `12d63b4`; kubelet explicitly reports no matching `linux/arm64` manifest. Older Backend and Frontend remain 1/1 Running.
- No Stock/Media PVC/PV claim or VolumeSnapshot/VolumeSnapshotContent reference was listed. This is in-cluster storage evidence only; external backup/retention and authoritative DNS ownership remain unverified.
- Dedicated Media runner service and `Runner.Listener` are still active. The shared Platform runner is also active and must remain untouched. The Media Ingress still publishes `media.mrcute.space`; Stock Ingress still publishes the four retired Stock hostnames.
- Public OIDC probes for `sso.mrcute.space` returned HTTP 503 while Keycloak/Auth are 0/0. Do not report OIDC as live/healthy.

### Decommission runner guard

- PR #1458 adds local systemd/Listener checks plus a paginated read-only GitHub runner-list query for exact runner `media-generation-k3s-01` in `phanthienquoc/media-generation`.
- Protected delete mode requires Platform secret `MEDIA_RUNNER_AUDIT_TOKEN`, a fine-grained GitHub token or App installation token with repository **Administration: read** on Media only. Missing token, API/JSON error or a still-registered runner blocks deletion. It cannot unregister or delete the runner.
- Secret configuration itself is not readable through this audit and has not been verified. Plan mode remains read-only and does not need the token. No delete-mode run, runner stop/unregister or namespace deletion occurred.

### Cross-repository blockers

- Native Platform schedules remain stale: reconcile #42467231073 (09:27:03Z), inspection #42452273701 (05:49:40Z), watchdog #42467080859 (09:24:53Z), recovery #42466737776 (09:20:06Z). At 11:20Z they exceed the 45/75/45/45-minute budgets. The 11:17 inspection is `workflow_dispatch`, not native schedule evidence. Do not change cron or freshness budgets.
- Native TCE WF-06 #42458256899 (07:18:37Z) failed four HTTP 503 endpoint probes; WF-12 #42452308083 (05:50:11Z) failed freshness. WF-07 integration #42453060493 passed. TCE market-scan schedule unchanged.
- Stock scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is missing. Stock CI #42440810105 passed 7/7 but is non-publishing; no new immutable GHCR publisher run/digest handoff was observed. App owner must add the key and run authenticated `preflight_only=true` before ingestion.
- Media CI #42239703151 and Auth CI #42215394539 remain the latest recorded PASS. Authentication PR #75 remains gated on Supabase merge-trigger side-effect evidence; #76 remains draft.
- Platform weekly cleanup #42472343489 passed with `DRY_RUN=true`, `remove_count=0`, but ran ~7h09 after its 03:30Z cron. It is purposeful maintenance and remains enabled.

### Current open PRs

- Platform: #1314, #544, #541, #539 (draft planning/docs). #1458 and #1459 are merged.
- Authentication: #75 ready/open, #76 draft.
- TCE Dashboard, StockDividend and Media Generation: none.

No namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation, production manifest apply, workload scaling, GHCR publication/promotion or host maintenance occurred in this execution. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.


## Latest execution update — 2026-11-08 18:55 ICT / 11:55 UTC

### Repository state, pull requests and latest checks

All five default-branch heads and open pull requests were re-read before this update.

| Repository | Default branch head | Open PRs | Latest master CI evidence |
|---|---|---|---|
| Platform Infra | `a0c1e3ee6cf0cb3d9f168227e6fdfd1a6e5ebdfd` | #1314/#544/#541/#539 (draft docs/planning) | #42475493117 `validate-manifests` PASS; check-run `validate` success |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Latest native health evidence remains WF-06 #42458256899 FAIL; all four endpoint check-runs failed |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | CI #42440810105 PASS 7/7; scraper #42457182511 FAIL closed |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS (last recorded app CI) |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready/open; #76 draft/open | CI #42215394539 PASS; PR #75/#76 exact-head validation PASS, Supabase Preview skipped |

Platform PRs #1458, #1459 and #1460 are merged. #1460 is reflected in current master `a0c1e3ee6cf0cb3d9f168227e6fdfd1a6e5ebdfd`; its PR validation #42475445877 and post-merge master validation #42475493117 passed. No open PR exists in TCE, Stock or Media.

### Native schedule acceptance (11:55 UTC)

Only `event=schedule` runs on master are counted. Manual, push, workflow_run and repository_dispatch events remain separate.

| Platform workflow | Latest native run | Result | Age at 11:55Z | Budget | Inter-arrival gap |
|---|---|---|---:|---:|---:|
| `reconcile-vps.yml` | [#42467231073](https://github.com/phanthienquoc/platform-infra/actions/runs/42467231073), 09:27:03Z | FAIL on pre-cert-manager-fix SHA | ~148m | 45m | 24,773s |
| `inspect-vps.yml` | [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701), 05:49:40Z | PASS, stale | ~365m | 75m | 21,396s |
| `reconcile-schedule-watchdog.yml` | [#42467080859](https://github.com/phanthienquoc/platform-infra/actions/runs/42467080859), 09:24:53Z | FAIL | ~150m | 45m | 25,092s |
| `recover-stale-ops.yml` | [#42466737776](https://github.com/phanthienquoc/platform-infra/actions/runs/42466737776), 09:20:06Z | PASS, stale | ~155m | 45m | 24,958s |

No newer native Platform event was returned by the `event=schedule` query. The latest post-fix Platform master validation #42475493117 is a push event, not native schedule evidence. The weekly cleanup [#42472343489](https://github.com/phanthienquoc/platform-infra/actions/runs/42472343489) ran with `DRY_RUN=true`, retained 10, found 8 unused images and removed 0; it is a purposeful maintenance workflow and remains enabled.

TCE native evidence is unchanged: WF-06 #42458256899 (07:18:37Z) failed all four strict HTTP 200 probes; WF-12 #42452308083 (05:50:11Z) failed schedule freshness; WF-07 integration #42453060493 (06:01:55Z) passed. At 11:55Z these events are ~276m, ~365m and ~353m old respectively. WF-06/WF-12 cadence and health remain distinct: WF-06 was delivered once but endpoints returned 503. TCE market-scan schedule was not changed.

Stock weekend scraper [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) was created 07:03:12Z and failed before ingestion because `VNSTOCK_API_KEY` is missing. The run is not evidence of a missed event; it is evidence that the scheduled job ran and failed closed.

### Production reconciliation and K3s

- Recovery-dispatched reconciliation [#42474936543](https://github.com/phanthienquoc/platform-infra/actions/runs/42474936543) completed SUCCESS at 11:15:29Z with `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR access checks passed for Auth, MicroFE and TCE; Auth runtime Secret was provisioned/verified; shared `ghcr-pull` remained unchanged. GitOps drift was false, so manifest apply, image promotion and rollout were correctly skipped. Recovery controller #42475042844 also completed SUCCESS.
- Read-only K3s inspection [#42475079478](https://github.com/phanthienquoc/platform-infra/actions/runs/42475079478) completed at 11:17:34Z; age at this review is ~38m, within the 75m snapshot-age budget, but its native inter-arrival cadence remains outside budget. Node `tce-k3s-01` is Ready/ARM64; disk 56% (~21 GiB free), available RAM ~19 GiB.
- Media backend/frontend and MicroFE Shell/WS/NATS are Running 1/1. Stock Admin (two Pods) and desired Backend remain ImagePullBackOff on `12d63b4` because the manifest has no matching `linux/arm64` platform; older Stock Backend and Frontend remain Running 1/1. TCE frontend/service, Auth and Keycloak remain intentional 0/0; no live service health is asserted.
- In-cluster preflight found no Stock/Media PVC/PV claims or VolumeSnapshot references. This does not prove external backup/retention or DNS ownership. Media runner systemd service and Listener remain active. The merged PR #1458 checks GitHub runner registration using `MEDIA_RUNNER_AUDIT_TOKEN`; secret existence has not been verified and no delete-mode run occurred.

### Cross-repo release contracts and owner dependencies

- App repositories continue to own tests/builds and immutable GHCR publication. Platform owns production manifests, shared pull credentials, runtime Secrets, provenance/digest validation, GitOps promotion/reconciliation, rollout and health.
- No new application publisher run, GHCR digest publication, digest-bound handoff or production image promotion was observed in this review. Stock CI's ARM64 job is non-publishing; the old `12d63b4` image issue therefore remains unresolved until a controlled app-owned publication and registry digest/ARM64 verification.
- TCE/Auth 503s align with intentional zero-replica maintenance; restoration requires service-owner approval and a rollback plan. No scaling was performed.
- Stock owner must provision `VNSTOCK_API_KEY`, run `preflight_only=true`, and confirm authenticated non-guest entitlement before ingestion.
- Auth PR #75 changes only documentation and test files (no migration files in the PR diff), but Supabase GitHub integration target and merge-triggered production migration behavior remain unverified. PR #75 is not merged; #76 remains draft.
- Media decommission remains blocked on secret configuration for `MEDIA_RUNNER_AUDIT_TOKEN`, remote runner absence, external backup/retention, authoritative DNS/provider ownership, and final approval. No runner stop/unregister or namespace deletion.
- No production manifest mutation, workload scaling, GHCR publication/promotion, PVC/PV/namespace deletion, DNS/database/storage mutation, runner retirement or host maintenance occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.


## Latest execution update — 2026-11-08 19:05 ICT / 12:05 UTC

### Changes merged this run

- Platform PR [#1461](https://github.com/phanthienquoc/platform-infra/pull/1461) merged by squash at `25c5e390161c5410517f5360885281abd4c1ff49`. Exact-head validation #42478273907 PASS; post-merge `validate-manifests` #42478553173 PASS.
- Authentication PR [#75](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/75) merged by squash at `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1`. Updated `AUTH-OPS-007` with current read-only Supabase migration parity and deployment-side-effect analysis. Exact-head run #42478511082 passed validation and native ARM64 non-publishing build; Supabase Preview was skipped. Post-merge Auth master CI #42478653766 is still running at this checkpoint. PR #76 remains draft.

### Auth/Supabase merge-side-effect verification

- Supabase project `gtqovpusfyyvxpeezxlo` remains `ACTIVE_HEALTHY`, PostgreSQL `17.6.1.084`, ap-southeast-1. Branch-list API reports default `main`, Git branch `master`, status `FUNCTIONS_DEPLOYED`.
- Authentication `master:supabase/migrations` contains 84 SQL files; Supabase migration-list API returns 84 applied versions. Exact version/name comparison is 84/84 with no pending local migration and no applied version lacking a repository file.
- Repository `supabase/` contains only `migrations/`; no `functions/`, `config.toml` or `seed.sql`. PR #75 changed docs/tests only. The earlier 2026-10-27 `MIGRATIONS_FAILED` observation is not reproduced by current project/branch metadata or migration parity.
- Owner-provided Dashboard evidence still reports GitHub integration connected to this repository root, branch `master`, Deploy to production ON. Supabase docs state that each connected-branch commit runs the deployment DAG and applies only pending migrations, configured seed files and changed Edge Functions. For this merge, no pending migration, seed/config or Edge Function inputs were present. The migration ledger remained at 84 after merge and project status remained ACTIVE_HEALTHY on recheck.
- The external GitHub integration's own deployment log is not exposed by the available read-only API. Therefore record no migration change observed, but do not claim the external integration run itself was independently inspected. Auth release workflow was not dispatched; no GHCR publication or Platform handoff occurred.

### Latest schedule and runtime state

| Workflow | Latest native evidence | Age at 12:05Z | Budget | Status |
|---|---|---:|---:|---|
| Platform reconcile | #42467231073, 09:27:03Z | ~158m | 45m | Failed on old cert-manager URL; no post-fix native run |
| Platform inspection | #42452273701, 05:49:40Z | ~375m | 75m | PASS but stale |
| Platform watchdog | #42467080859, 09:24:53Z | ~160m | 45m | FAIL |
| Platform recovery | #42466737776, 09:20:06Z | ~165m | 45m | PASS but stale |
| TCE WF-06 | #42458256899, 07:18:37Z | ~286m | 25m freshness | 4× HTTP 503 |
| TCE WF-12 | #42452308083, 05:50:11Z | ~375m | 25m freshness | FAIL |
| TCE WF-07 integration | #42453060493, 06:01:55Z | ~363m | workflow contract | PASS |
| Stock scraper | #42457182511, 07:03:12Z | ~302m | scheduled run | Fail-closed: missing secret |

No newer native Platform or TCE schedule event was returned. The latest successful Platform post-merge validation #42478553173 is a push event and is not native schedule evidence. Do not change cron or freshness budgets; TCE market-scan schedule remains unchanged.

- Stock job log confirms `VNSTOCK_API_KEY` was empty. The preflight failed before Python setup, dependency installation, entitlement verification or ingestion. No data was ingested.
- Latest read-only K3s inspection #42475079478 snapshot is 11:17:34Z, ~47m old at this review (within 75m age budget, but not native cadence acceptance). Node Ready/ARM64; disk 56% (~21 GiB free), RAM ~19 GiB available. Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin and desired Backend ImagePullBackOff on `12d63b4`; older Stock Backend/Frontend 1/1; TCE/Auth/Keycloak intentional 0/0.
- Reconciliation #42474936543 and recovery #42475042844 PASS; GHCR access and Auth runtime Secret checks passed, shared `ghcr-pull` unchanged, no GitOps drift, manifest apply/image promotion/rollout skipped.
- Media runner remains active; remote registration guard is merged, but token secret existence is unverified. External backup/retention and authoritative DNS evidence remain missing.

No production manifest mutation, workload scaling, GHCR publication/promotion, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this update. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.


## Latest execution update — 2026-11-08 20:01 ICT / 13:01 UTC

- Current master SHAs: Platform `192187fffb416dba326055c1a729510d48cb612a`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Authentication `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1`.
- Open PRs: Platform #1314/#544/#541/#539 (draft); Authentication #76 (draft); no open PRs in TCE, Stock or Media.
- Platform latest master validation #42478871584 PASS. Native schedule events remain reconcile #42467231073 FAIL, inspection #42452273701 PASS but stale, watchdog #42467080859 FAIL, recovery #42466737776 PASS but stale. All exceed their 45/75/45/45-minute freshness budgets; no later native Platform schedule event was found in paged Actions history.
- TCE WF-12 native #42479336350 failed its stale-WF-06 freshness check but successfully dispatched a heartbeat. WF-13 #42479348862 validated that failure and dispatched read-only WF-06 fallback #42479362379. The fallback returned HTTP 503 for all four strict public probes (TCE web/API and Auth liveness/readiness). Schedule delivery and live service health remain separate.
- Platform heartbeat receiver #42479344664 failed while fetching the public TCE Actions run API: logs show repeated HTTP 500 responses for run #42479336350. Payload/source fields passed initial validation; API lookup failed closed. A rerun was requested but attempt 2 was skipped by the existing first-attempt-only guard, so no second validation or dispatch occurred.
- A dedicated branch `fix/retry-transient-tce-heartbeat-api-500-20261108-2001-ict` adds bounded retries for transient 5xx/connection failures to `fetch_tce_run()`, and static assertions that permanent 4xx responses are not retried indiscriminately. PR validation is pending; no production path or schedule was changed.
- Stock scraper #42457182511 failed closed before ingestion because `VNSTOCK_API_KEY` is missing. Stock CI #42440810105 passed but did not publish. Media CI #42239703151 passed; no new publisher/decommission evidence. Auth master CI #42478653766 passed; #76 remains draft.
- Latest K3s snapshot #42475079478 is now older than the 75-minute snapshot-age budget; do not treat it as current health. Its recorded state remains Media/MicroFE 1/1, Stock Admin/desired Backend ImagePullBackOff, and TCE/Auth/Keycloak 0/0.
- Reconciliation #42474936543 passed credential/GHCR preflight, found no drift and skipped manifest apply/image promotion/rollout. No fresh inspection, new immutable publication, digest handoff, production mutation, scaling, decommission, DNS/database/storage change, runner retirement or host maintenance occurred.
- TCE market-scan schedule is unchanged. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only.

- Follow-up after checkpoint creation: Platform PR [#1463](https://github.com/phanthienquoc/platform-infra/pull/1463) is now open from the dedicated branch; initial exact head `b7550187f317fb36999757038ad1fa631a07a908`. `validate-github-actions` and `validate-manifests` started on that exact head and were in progress at the first status read. Re-check current head before any merge.

## Post-merge follow-up — 2026-11-08 20:14 ICT / 13:14 UTC

- Platform PR [#1463](https://github.com/phanthienquoc/platform-infra/pull/1463) merged by squash at `c70fc63d52d1e1dfd789e8fe7adc15a47cb9615a`; exact head was `33e61ebbbdcaf3523b008457eef71da490626d1a`.
- Exact-head `validate-github-actions` #42483745382 PASS and `validate-manifests` #42483745326 PASS. Post-merge master `validate-github-actions` #42483862284 PASS and `validate-manifests` #42483862226 PASS.
- The merged recovery receiver now retries transient GitHub Actions API 5xx/connection-refused failures with a bounded retry window, while retaining `curl --fail` and no `--retry-all-errors`; permanent 4xx/authentication failures remain fail-closed.
- A new Platform `inspect-vps.yml` native schedule run #42483869620 was created on the merge SHA and was still `in_progress` at this checkpoint. The prior native inspection #42452273701 was 05:49:40Z; the inter-arrival gap to #42483869620 is approximately 7h23m, still outside the 75-minute cadence budget. Do not claim a completed K3s snapshot until #42483869620 completes and its artifact/snapshot is validated.
- No newer native Platform reconcile/watchdog/recovery run was observed: #42467231073 FAIL, #42467080859 FAIL, #42466737776 PASS but stale. Schedule delivery remains unresolved despite the new inspection run.
- TCE WF-12 #42479336350 successfully delivered its heartbeat; Platform receiver #42479344664 failed on repeated GitHub API HTTP 500. The requested rerun was skipped at attempt 2 by the existing first-attempt-only guard. TCE WF-13 #42479348862 dispatched read-only WF-06 fallback #42479362379; all four endpoints returned HTTP 503.
- Static publisher/receiver review: TCE WF-03 and Auth release are manual app-owned ARM64 publishers with full-SHA-bound tags and digest verification before digest-bound Platform events; Stock deploy verifies full-SHA and version+SHA tags for Scraper/Admin/Backend but has no active Platform handoff while retired; Media WF-03 verifies ARM64 release digest and intentionally sends no Platform handoff while retired. Platform receiver verifies TCE/Auth source run identity, tag-to-digest mapping and ARM64 before GitOps promotion. No new publisher run or actual GHCR digest handoff was observed.
- Stock scraper #42457182511 remains fail-closed due missing `VNSTOCK_API_KEY`; Auth master CI #42478653766 PASS and PR #76 remains draft. Media CI #42239703151 PASS.
- No production manifest apply, image promotion, workload scaling, decommission, DNS/database/storage mutation, runner retirement or host maintenance occurred. TCE market-scan schedule unchanged.

## Completed K3s inspection follow-up — 2026-11-08 20:15 ICT / 13:15 UTC

- Native Platform inspection [#42483869620](https://github.com/phanthienquoc/platform-infra/actions/runs/42483869620) completed SUCCESS. It generated `debug/vps-latest.md` at 13:12:54Z and created inspection PR [#1464](https://github.com/phanthienquoc/platform-infra/pull/1464), which was validated and squash-merged at `ba01c42299490eff839c41326c894e0d59650ab6`.
- Snapshot is now fresh, but native inspection cadence is still not accepted: prior native inspection #42452273701 was 05:49:40Z; inter-arrival gap was 26,586s (~7h23m), exceeding the 4,500s/75m budget.
- K3s node `tce-k3s-01` remains Ready, ARM64, K3s `v1.36.3+k3s1`; container runtime `containerd://2.3.2-k3s2`. Disk 56% (21 GiB available), RAM 19 GiB available. Docker 29.1.3 reports 20 images/9.195 GB with 5.773 GB reclaimable; 12 containers active; no cleanup performed.
- Media backend/frontend and MicroFE Shell/WS/NATS are Running 1/1. Stock Admin (two pods) and desired Backend remain ImagePullBackOff on `12d63b4`; legacy Stock Backend and Frontend remain Running 1/1. TCE/Auth/Keycloak remain zero-replica; Keycloak readiness timed out and both public OIDC probes returned HTTP 503.
- Media runner service and Listener remain active/enabled; Platform runner is also active. In-cluster Stock/Media storage preflight remains clean (no PVC/PV claims or VolumeSnapshot references), but external backup/retention and authoritative DNS are still unverified.
- GitOps drift is clean; cert-manager v1.21.1 bootstrap manifest checksum was verified. Host reports `restart_required=yes`; containerd/Docker/OS updates are available. No upgrade/reboot authorized.
- No production manifest apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.
