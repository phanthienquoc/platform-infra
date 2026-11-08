# Cross-Repository Production Deployment Tracker

Last reviewed: **2026-11-08 17:15 ICT / 10:15 UTC**

This rolling tracker distinguishes native schedule events from manual, push, workflow_run and repository_dispatch fallbacks. Timestamped evidence is archived under `docs/cross-repo-deployment-checkpoints/`.

## Repository readiness

| Repository | Master SHA | Open PRs | Readiness evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `7ccd527ed2989c772f7ba7b2e0a97e1d615086ee` | #1453 (cert-manager API auth), #1314/#544/#541/#539 (draft planning/docs); #1452 merged, #1442 closed | #1452 exact-head checks passed and merged. Post-merge validate-manifests #42469989585 failed on GitHub Release API HTTP 403; PR #1453 adds optional token auth and isolates PR-write permission. Post-merge reconciliation #42469998524 passed with no drift/apply. |
| phanthienquoc/TCE-dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Latest native WF-06 #42458256899 failed all four strict probes with HTTP 503; native WF-12 #42452308083 failed freshness; WF-07 #42453060493 passed earlier. No newer native TCE schedule event observed through 10:15Z. |
| phanthienquoc/stockdividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | Master CI #42440810105 PASS 7/7. Scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is missing. Fresh snapshot shows Admin and desired Backend ImagePullBackOff on `12d63b4` (no matching ARM64 manifest); older Backend/Frontend remain Running. |
| phanthienquoc/media-generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS. Snapshot #42468887549 shows backend/frontend Running 1/1; dedicated Media runner active/enabled. Decommission still requires external backup, DNS and runner-registration evidence. |
| phanthienquoc/phanthienquoc-authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | Master CI #42215394539 PASS; exact-head PR CI #40446492086/#41329425940 PASS. Supabase merge-triggered migration/integration effects remain unverified; no merge. |

## Current actions

1. **Platform/cert-manager:** PR #1453 fixes post-merge manifest validation's HTTP 403 from the pinned GitHub Release asset API by using optional `GH_TOKEN` on trusted callers. It keeps the validation job at `contents: read` and moves PR-comment write permission to a separate job.
2. **Platform/decommission:** PR #1452 merged as `7ccd527ed2989c772f7ba7b2e0a97e1d615086ee`; exact-head `validate-github-actions` #42469900529 and `validate-manifests` #42469900449 passed. The sudo boundary is fixed, but a post-merge read-only inspection has not yet re-run the Stock/Media preflight.
3. **Platform reconciliation:** workflow_dispatch #42469998524 passed; GHCR pull access, Auth runtime Secret and shared pull credential checks passed. No GitOps drift, so manifest apply and rollout were skipped.
4. **GitHub Actions administrator:** investigate missing/delayed native Platform and TCE WF-06/WF-12 schedule delivery; preserve cron and freshness budgets.
5. **Platform owner:** audit runner registrations and GitHub audit log after the earlier short-lived registration-token exposure window.
6. **TCE/service owner:** investigate four HTTP 503 endpoints; any replica restoration requires explicit approval and rollback plan.
7. **Stock owner:** add `VNSTOCK_API_KEY`, run `run_scraper.yml` with `preflight_only=true`, and verify authenticated non-guest entitlement before ingestion.
8. **Auth/Supabase owner:** verify integration target and merge-triggered migration effects before PR #75; keep #76 draft.
9. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence; retire and unregister the dedicated Media runner before namespace deletion.
10. **Platform operator:** schedule Docker/containerd maintenance with rollback/retention evidence before cleanup, upgrade or reboot.

## Current runtime blockers

- **Manifest validation:** post-merge push run #42469989585 failed in `Render production manifests`; the GitHub Release asset API returned HTTP 403 on four curl attempts. SHA-256 validation and Kustomize rendering were not reached. PR #1453 supplies an optional read-only token and tests token redaction; exact-head checks are pending.
- **Native schedule delivery:** latest reconcile #42467231073 (09:27:03Z) failed before the cert-manager fix; watchdog #42467080859 (09:24:53Z) failed; recovery #42466737776 (09:20:06Z) passed; inspection #42452273701 (05:49:40Z) passed but is stale. At 10:15Z their ages are ~48m / 265m / 50m / 55m against 45/75/45/45m budgets. Inter-arrival gaps remain ~24,773s / 21,396s / 25,092s / 24,958s. Native cadence and age acceptance remain failed; manual/push/workflow_run fallbacks do not count.
- **TCE/Auth health:** WF-06 #42458256899 returned HTTP 503 for TCE web, TCE API, Auth liveness and Auth readiness. K3s shows TCE frontend/service, Auth and Keycloak at intentional 0/0; no live health is asserted and no replicas are scaled.
- **Stock scraper:** native run #42457182511 failed closed because `VNSTOCK_API_KEY` was empty before dependency installation. Safe preflight must pass before ingestion.
- **Stock legacy workloads:** snapshot #42468887549 shows two Stock Admin pods and the desired Backend pod in ImagePullBackOff on `12d63b4`; kubelet reports `no match for platform in manifest`. Older Backend and Frontend remain Running 1/1. Stock remains retired from active Platform GitOps.
- **Stock/Media decommission:** PR #1452 fixes the preflight sudo boundary, but no post-merge inspection has confirmed the namespace inventory. External backup/retention, DNS ownership and Media runner unregistration remain unverified; no deletion is authorized.
- **Authentication migration:** PR #75/#76 must not merge solely on CI; Supabase merge-triggered migration/integration effects remain unverified.
- **Host maintenance:** snapshot reports Docker 29.1.3, host containerd.io 2.2.1 with 2.4.2-3 available, ~5.77 GB reclaimable and `restart_required=yes`; no maintenance window/rollback evidence exists.

## Platform PR and validation evidence

- [PR #1435](https://github.com/phanthienquoc/platform-infra/pull/1435) merged at `f1791584f9e02fe0e0d2e43308239ee95c7b4a97`; exact-head manifest validation #42453399594 and post-merge #42453440188 PASS.
- [PR #1437](https://github.com/phanthienquoc/platform-infra/pull/1437) merged at current master `374222f2c9685528c6783c480e5df01e22b457de`; exact-head checks #42453536660/#42453536676 PASS.
- Post-merge checks #42453579947 (manifests) and #42453579869 (workflow contracts) PASS. Push smoke #42453579901 PASS and emitted warnings for all four Platform gaps plus TCE WF-06/WF-12 gaps.
- The merged watchdog's push smoke ended with "All Platform native schedule inter-arrival checks passed" because `--warn-only` returns zero. That wording is misleading; PR #1438 corrects it. Warning annotations did list the gaps.

## Native schedule acceptance

Only original `event=schedule`, master, attempt 1 runs with exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch remain separate.

| Workflow | Native cron (UTC) | Latest native run | Result | Inter-arrival gap | Age at 10:15Z | Budget |
|---|---|---:|---:|---:|---:|---:|
| `reconcile-vps.yml` | `7,22,37,52 * * * *` | [#42467231073](https://github.com/phanthienquoc/platform-infra/actions/runs/42467231073), 09:27:03Z | FAIL (pre-fix cert-manager render) | 24,773s | ~48m | 45m |
| `inspect-vps.yml` | `2,32 * * * *` | [#42452273701](https://github.com/phanthienquoc/platform-infra/actions/runs/42452273701), 05:49:40Z | PASS | 21,396s | ~265m | 75m |
| `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | [#42467080859](https://github.com/phanthienquoc/platform-infra/actions/runs/42467080859), 09:24:53Z | FAIL | 25,092s | ~50m | 45m |
| `recover-stale-ops.yml` | `10,25,40,55 * * * *` | [#42466737776](https://github.com/phanthienquoc/platform-infra/actions/runs/42466737776), 09:20:06Z | PASS | 24,958s | ~55m | 45m |

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
