# Cross-repo production deployment readiness

Current review: **2026-11-08 10:00 ICT / 2026-11-08 03:00 UTC**

Rolling operational summary. Preserve timestamped evidence under `docs/cross-repo-deployment-checkpoints/`.

## Repository state and open PRs

| Repository | Master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `50c7b5a22760e2393668c4367d9e8297e1970aae` | #1314, #544, #541, #539 (draft planning/docs) | Inspection PR #1432 merged after exact-head manifest validation #42438611543 PASS. Latest scheduled reconcile #42439099803 PASS; native inter-arrival budgets still fail. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Latest native WF-06 #42432710149 failed all four HTTP 200 probes (HTTP 503); latest native WF-12 #42427247349 failed stale-health gate. |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | PR #38 merged. Exact-head CI #42437287197 passed 7/7, including ARM64 build. Post-merge master CI #42440810105 is running (5/7 complete; ARM64 and scraper container builds still in progress at review). Scraper remains blocked by missing `VNSTOCK_API_KEY`. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS. Latest formal K3s inspection still shows backend/frontend and dedicated runner active; no recent publisher/digest handoff. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | CI #42215394539 PASS. PR #75/#76 validation PASS; Supabase Preview skipped. #75 remains gated on migration/integration side effects. |

Open Platform PRs #1314, #544, #541 and #539 are draft planning/documentation work, not deployment changes. No open cross-repo deployment PR remains on Platform.

## Platform PR and validation evidence

- [PR #1432](https://github.com/phanthienquoc/platform-infra/pull/1432) is merged at master SHA `50c7b5a22760e2393668c4367d9e8297e1970aae`.
- Inspection source run [#42438528386](https://github.com/phanthienquoc/platform-infra/actions/runs/42438528386) completed successfully.
- Exact-head manifest validation [#42438611543](https://github.com/phanthienquoc/platform-infra/actions/runs/42438611543) PASS for inspection PR head `d9972201b5e4ecc91b67189365e0d2d97766fac1`.
- PR #1432 merge commit: `50c7b5a22760e2393668c4367d9e8297e1970aae`.
- This readiness update is documentation-only; no application manifests, image tags, schedules, secrets, replicas, DNS, storage or host state are changed.

## Platform native schedule delivery

Only original `event=schedule` runs on master, attempt 1, with the exact workflow path and full source SHA count as native evidence. Manual, push, workflow_run and repository_dispatch are separate evidence classes.

| Workflow | Native cron (UTC) | Latest native run | Result | Inter-arrival gap | Age at review | Budget |
|---|---|---|---|---:|---:|---:|
| reconcile-vps.yml | `7,22,37,52 * * * *` | [#42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803), 2026-11-08 02:34:10Z | PASS | 12,390s | ~26m | 45m |
| inspect-vps.yml | `2,32 * * * *` | [#42427239949](https://github.com/phanthienquoc/platform-infra/actions/runs/42427239949), 2026-11-07 23:53:04Z | PASS | 13,475s | ~3h07m | 75m |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | [#42438566387](https://github.com/phanthienquoc/platform-infra/actions/runs/42438566387), 2026-11-08 02:26:41Z | FAIL | 12,395s | ~33m | 45m |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | [#42438384072](https://github.com/phanthienquoc/platform-infra/actions/runs/42438384072), 2026-11-08 02:24:08Z | PASS | 12,313s | ~36m | 45m |

The watchdog log confirms `reconcile-vps.yml` was active and reports a 12,392s native gap between #42407410735 and #42423799465 against the 2,700s budget. A later native reconcile #42439099803 succeeded, but its gap from #42423799465 is also 12,390s, still outside budget. The latest watchdog run predates #42439099803 and has not yet evaluated that newer pair.

The latest native scheduled inspection remains #42427239949 and is stale. A separate read-only `workflow_dispatch` inspection [#42438528386](https://github.com/phanthienquoc/platform-infra/actions/runs/42438528386) completed at 02:26:17Z and refreshed `debug/vps-latest.md`; it is operational evidence, not native cron evidence. Recovery run #42438384072 and the post-reconcile recovery path completed, but fallbacks do not satisfy native cadence acceptance.

Do not lower freshness/inter-arrival budgets, change cron to manufacture green status, or count manual/workflow_run/repository_dispatch as native delivery. The schedule-delivery issue remains for GitHub Actions administration; workflow state was observed active and queue diagnostics did not identify an excessive runner queue.

## Latest reconciliation and credentials

- Latest native reconciliation [#42439099803](https://github.com/phanthienquoc/platform-infra/actions/runs/42439099803) completed PASS on master SHA `50c7b5a22760e2393668c4367d9e8297e1970aae`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- GHCR pull-access preflight passed for Auth, MicroFE Shell/WS and TCE web/service.
- Auth runtime Secret was provisioned and verified with values suppressed.
- Shared GHCR pull credential reconciliation completed; no image-change promotion was authorized.
- GitOps preflight found no manifest drift; manifest apply and image-change guard were correctly skipped.
- MicroFE health passed. TCE and Auth remain intentional zero-replica maintenance; lane success is not a claim of live TCE/Auth service health. Stock/Media remain outside active rollout scope.
- Deployment lane final gate PASS. No new image promotion or production rollout occurred.

## TCE schedule and service health

- Latest native WF-06 [#42432710149](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42432710149), 2026-11-08 01:05:27Z, failed all four strict HTTP 200 probes: TCE web, TCE API, Auth liveness and Auth readiness returned HTTP 503.
- Latest manual WF-06 [#42432739134](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42432739134) also failed.
- Latest native WF-12 [#42427247349](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42427247349), 2026-11-07 23:53:10Z, failed stale-WF-06 freshness. Workflow_run recovery/watchdog passes are not native schedule evidence or endpoint health.
- No newer native TCE WF-06/WF-12 event appeared in the latest Actions history reviewed.
- Keep WF-06 and WF-12 cron and strict HTTP 200 expectations unchanged. **TCE market-scan schedule unchanged.** Do not increase replicas without explicit service-owner approval and a reviewed recovery plan.

## StockDividend

- [PR #38](https://github.com/phanthienquoc/stockdividend/pull/38) merged at `e6469ac6617142b349144101a1192cb6aa7104ad`.
- PR exact head `04ec376ecee191e979c7a4c6c40a39b0ba0d9c02`; CI [#42437287197](https://github.com/phanthienquoc/stockdividend/actions/runs/42437287197) passed 7/7, including the production ARM64 non-publishing builds.
- Publisher now emits full 40-character SHA and `prod-v<version>-<full-sha>` tags for scraper/admin/backend; verifies both tags resolve to one SHA-256 digest and expose `linux/arm64`. It no longer creates mutable `latest`, short-SHA or plain-semver aliases. Existing registry tags were not deleted. Registry-side tag immutability enforcement is not certified.
- Post-merge master CI [#42440810105](https://github.com/phanthienquoc/stockdividend/actions/runs/42440810105) was still running at review: 5/7 checks complete, with ARM64 production build and scraper container build in progress. CI uses non-publishing builds; this is not GHCR publication evidence.
- Weekend scraper [#42349150261](https://github.com/phanthienquoc/stockdividend/actions/runs/42349150261) failed closed at the required `VNSTOCK_API_KEY` check; dependency installation, entitlement check and ingestion were skipped. No 2026-11-08 01:00Z native scraper run appeared in the latest run history.
- Exact next action: Stock owner supplies repository secret `VNSTOCK_API_KEY`, runs `run_scraper.yml` with `preflight_only=true`, and verifies authenticated non-guest entitlement before ingestion.
- Stock remains retired from active Platform GitOps; no active production handoff or workload mutation is authorized.

## Media Generation

- Master CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) PASS; no open PR and no fresh immutable publisher/digest handoff.
- Latest formal inspection shows backend/frontend Running 1/1 and the dedicated Media runner service active/enabled.
- Media remains retired from active Platform GitOps, but legacy namespace/workloads and runner are not decommissioned.
- Do not remove namespace or runner until external backup/retention, authoritative DNS/provider ownership, runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight are recorded.

## Authentication

- Master CI [#42215394539](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215394539) PASS.
- PR #75 head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`: validation PASS; Supabase Preview skipped. Keep open until Supabase integration target and merge-triggered migration side effects are verified with the owner.
- PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`: validation PASS; Supabase Preview skipped. Keep draft.
- Do not merge either PR solely on CI status; migration/integration authority remains gated.

## Latest K3s inspection and host state

Latest formal read-only inspection [#42438528386](https://github.com/phanthienquoc/platform-infra/actions/runs/42438528386), generated 2026-11-08 02:26:17Z and merged via inspection PR #1432. It is a fresh read-only snapshot, separate from native scheduled inspection evidence.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- RAM ~19 GiB available; disk 56%, ~21 GiB available.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1; package updates include containerd.io 2.4.2-3 and Docker 29.9.3; `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform and dedicated Media runner services active/enabled.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1.
- Stock Admin: two pods ImagePullBackOff on `12d63b4`. Desired Stock Backend pod on `12d63b4` ImagePullBackOff while older `23b2878` pod remains Running 1/1; Stock Frontend Running on `23b2878`. Inspection imageID evidence shows no digest for the failed Stock pods. Prior kubelet event identified missing ARM64 manifest for `12d63b4`.
- TCE frontend/service, Auth service and Keycloak remain intentional 0/0; no live health is asserted.
- Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB, Bound); no Stock/Media VolumeSnapshot references. This does not prove external backup/retention completeness or DNS ownership.
- `stock-prod` and `media-prod` namespaces remain Active. No namespace/PVC/PV deletion or runner retirement.

## Immutable publication and dispatch contracts

- TCE WF-03 remains manual-only; app repo owns ARM64 builds, full-SHA/version tags, web/service digest verification and `tce-release-requested`. Platform validates source-run identity and digest-bound payloads, then owns production promotion/reconciliation.
- Authentication `release.yml` remains manual-only; app repo owns ARM64 publication, provenance/SBOM and SHA/version digest verification before `auth-image-published`. Platform owns runtime Secrets, manifests, promotion and rollout.
- Stock PR #38 now enforces full-SHA + version/full-SHA tags and digest equality for all three components; no Platform dispatch because Stock is retired from active GitOps.
- Media WF-03 retains ARM64/full-SHA digest verification and intentionally sends no Platform dispatch while retired.
- Static sender/receiver contract checks are not live publication evidence. No new publisher run, production image promotion or digest handoff was observed in this review.

## Owners and exact next actions

1. **GitHub Actions administrator:** investigate delayed/missed native Platform schedule delivery; preserve 45/75/45/45m budgets and require in-budget original native cycles.
2. **Platform operator:** continue fresh read-only inspection through `inspect-vps.yml`; do not use reconciliation as a substitute for formal inspection.
3. **Platform owner:** audit runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived registration-token validity window. PR #1416 masks future output; registry cleanliness is not certified.
4. **TCE/service owner:** investigate four HTTP 503 endpoints and restore native WF-06/WF-12 cadence. Obtain explicit approval before any replica change.
5. **Stock owner:** add `VNSTOCK_API_KEY`, run safe preflight, confirm authenticated non-guest entitlement, and investigate missing native scraper delivery before ingestion.
6. **Auth/Supabase owner:** verify integration target and merge-triggered migration effects before PR #75; keep #76 draft.
7. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence. Retire the dedicated Media runner (idle, stopped, disabled and unregistered) before namespace deletion.
8. **Platform operator:** schedule a maintenance window for Docker/containerd upgrade/reboot. Do not clean images without retention and rollback evidence.

Stock/Media decommission remains manual-only. Deletion requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

## Authority and safety boundary

- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout and health.
- No duplicate direct SSH/Compose deployment authority.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this review.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-1000-ict.md](cross-repo-deployment-checkpoints/2026-11-08-1000-ict.md)
