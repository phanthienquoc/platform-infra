# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 19:05 ICT / 12:05 UTC**

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns validators, native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master 25c5e390; PR #1461 merged, exact-head #42478273907 and post-merge #42478553173 PASS. Reconcile #42474936543 PASS with no drift/apply/promotion; inspection #42475079478 PASS. |
| TCE Dashboard | App-owned CI/tests; manual WF-03 ARM64 immutable web/service publisher with digest verification and validated tce-release-requested handoff; WF-08B MicroFE ARM64 publisher and digest-bound Platform handoff; WF-06/WF-07/WF-12/WF-13 health, integration, watchdog and recovery. Manual WF-09 is a safe VPS inspection/setup utility that creates isolated directories and uploads source only to the development path. WF-10 is explicitly staging-only (workflow_call/dispatch), bootstraps tce-stg and its staging Secret; it does not target tce-prod. | No production SSH/Compose/K3s apply authority. Platform alone owns production manifests, runtime Secrets, image promotion/reconciliation and health. Preserve WF-09/WF-10 as scoped manual staging/bootstrap utilities; do not treat them as production deployment lanes. | Master 7ab52078; no open PR. Native WF-06 #42458256899 failed four HTTP 503 probes; native WF-12 #42452308083 failed freshness; WF-07 #42453060493 PASS. No newer native WF-06/WF-12 event; TCE/Auth remain 0/0. Market-scan schedule unchanged. |
| StockDividend | CI/tests; deploy.yml is the app-owned ARM64 GHCR publisher: master push emits full-SHA and prod-v<version>-<full-SHA> tags for Scraper/Admin/Backend; workflow_dispatch is blocked unless STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true. No Platform handoff. Weekend scraper cron remains separate and fail-closed on VNSTOCK_API_KEY. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No production SSH/Compose deployment authority. | Master e6469ac6; PR #38 merged; CI #42440810105 PASS 7/7 (non-publishing CI). Native scraper #42457182511 ran and failed closed on empty VNSTOCK_API_KEY before dependency install/ingestion. Stock Admin/desired Backend remain ARM64 ImagePullBackOff on 12d63b4; no new publisher/digest evidence. |
| Media Generation | CI/tests; WF-03 app-owned master-push/manual publisher builds ARM64 and publishes immutable version/full-SHA images with digest verification. No Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. No direct SSH/Compose production deployment authority in WF-03. | Master 54f3a76a; CI #42239703151 PASS (last recorded app CI). Inspection #42475079478 shows backend/frontend 1/1 and storage-clean in-cluster preflight; dedicated Media runner remains active/listening. PR #1458 remote registration guard merged; audit token, external backup and DNS evidence remain unverified. |
| Authentication | CI/tests; release.yml is workflow_dispatch-only app publisher: verifies source, builds ARM64 with provenance/SBOM, verifies SHA/version tags and sends auth-image-published. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master cb907a63; PR #75 merged after exact-head CI #42478511082 PASS (ARM64 non-publishing build, Supabase Preview skipped); post-merge CI #42478653766 running. Supabase project ACTIVE_HEALTHY; 84/84 migration version/name parity, no migration count change observed after merge. PR #76 remains draft. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence at 10:40Z |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42467231073 FAIL at 09:27:03Z before cert-manager fix; gap 24,773s; ~73m old. |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42452273701 PASS at 05:49:40Z; gap 21,396s; ~290m old. Fresh push inspection #42468887549 is not native. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42467080859 FAIL at 09:24:53Z; gap 25,092s; ~75m old. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42466737776 PASS at 09:20:06Z; gap 24,958s; ~80m old. |
| vps-image-cleanup.yml | `30 3 * * 0` | N/A (weekly dry-run) | #42472343489 PASS at 10:39:26Z (~7h09 after cron); DRY_RUN=true, 8 unused, retain 10, remove 0. |

Only original `event=schedule`, master, attempt 1, exact workflow path and full source SHA count as native. Manual, push, workflow_run and repository_dispatch remain separate. Push smoke reports schedule observations as warnings; it does not assert cadence acceptance.

## Reconciliation and production health

- Native reconcile #42439099803 PASS but stale. Workflow_dispatch reconcile #42452324950 PASS at 05:50:26Z on prior master SHA `5513c0bc...`; GHCR preflight, Auth runtime Secret, shared pull credentials and scoped image-pull restart passed.
- Manifest apply and image-change guard skipped; no image promotion or production rollout. Recovery #42453078467 verified TCE heartbeat and avoided duplicate fallback because reconciliation and inspection were recent.
- TCE/Auth are intentional zero-replica maintenance; lane success is not live-service health. Stock/Media remain outside active rollout scope.

## TCE schedule and health

- WF-06 remains `*/15 * * * *`; latest native #42432710149 stale; manual #42452331522 failed all four strict probes with HTTP 503.
- WF-12 remains `7,22,37,52 * * * *`; native #42452308083 failed WF-06 freshness. WF-07 scheduled #42453060493 PASS; WF-12 workflow_run #42453071754 failed stale-WF-06 gate; WF-13 #42453081086 recovered; Platform heartbeat #42453078467 passed.
- Keep strict HTTP 200 checks and TCE market-scan schedule unchanged. No replica scaling without explicit owner approval.

## Latest K3s inspection and protected decommission

- Formal read-only snapshot #42452273701 generated 05:49:48Z. Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; RAM ~19 GiB available, disk 56%/~21 GiB free.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1. Stock Admin (two pods) and desired Backend pod ImagePullBackOff on `12d63b4`; kubelet reports no matching platform manifest. Old Stock Backend and Frontend on `23b2878` remain Running.
- TCE/Auth/Keycloak remain 0/0. Stock/Media namespaces Active; no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership are unverified.
- Docker 29.1.3; 20 images/9.195 GB, ~5.773 GB reclaimable; host containerd.io 2.2.1; `restart_required=yes`. No cleanup, upgrade, reboot or decommission.
- Platform and Media runner services active/enabled; runner-registration audit remains outstanding.

## Cross-repo release boundaries

- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance gates, GitOps promotion/reconciliation, rollout and health.
- TCE/Auth sender/receiver payloads remain digest-bound and statically aligned. Stock #38 contract is merged; Media/Stock have no active Platform dispatch while retired.
- No new publisher run, GHCR publication, digest handoff or production image promotion in this review.
- No duplicate direct SSH/Compose deployment authority. Stock/Media deletion remains protected by backup, DNS, runner retirement, production approval and fresh PVC/PV/VolumeSnapshot gates.


## Latest execution evidence — 2026-11-08 13:57 ICT / 06:57 UTC

- Platform master: `9f6618f8736ab14d58595436faa87944cc45bb4d`; latest push smoke #42454041525 PASS, warning-only. Native reconcile #42439099803, watchdog #42438566387 and recovery #42438384072 remain outside cadence budgets; native inspection #42452273701 is within age budget but its 21,396s inter-arrival gap exceeds the 75m cadence budget.
- TCE: WF-07 scheduled #42453060493 PASS; WF-12 #42452308083 and its workflow_run freshness check fail; WF-13 #42453081086 recovers heartbeat delivery. Manual WF-06 #42452331522 remains 4/4 HTTP 503. No TCE replicas are changed.
- Stock: master CI #42440810105 PASS. Scraper #42349150261 failed closed on empty `VNSTOCK_API_KEY`; the next Sunday scheduled run is not visible at 06:57Z, but prior Saturday delivery was delayed until 06:56:29Z, so continue observing rather than declaring a missed delivery yet.
- Media: latest recorded master CI #42239703151 PASS; no new publisher evidence.
- Authentication: master CI #42215394539 PASS; PR #75 exact-head CI #40446492086 PASS but merge remains gated by Supabase Deploy-to-production integration behavior; PR #76 exact-head CI #41329425940 PASS and remains draft.
- Open PRs: Platform #1314/#544/#541/#539; Authentication #75/#76. TCE, Stock and Media have none.
- No GHCR publish/promotion, production manifest mutation, workload scaling, decommission, DNS/database/storage change, runner retirement or host maintenance. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 15:04 ICT / 08:04 UTC

- Platform master `564d94bb9134195a0643274f8656d95161b47e02`; inspection PR #1440 merged at exact validated head `9cdfaddc66fbcb21a6ea7a78e05f44551726fa69` (merge SHA `564d94bb9134195a0643274f8656d95161b47e02`). Read-only inspection #42458425146 succeeded; exact-head manifest validation #42458510940 passed.
- Manual reconcile #42458288651: GHCR pull access and Auth runtime Secret verification passed; shared `ghcr-pull` unchanged; no manifest drift, so apply skipped. TCE/Auth are intentional zero-replica maintenance (no live health asserted); active MicroFE health passed. No image promotion.
- Platform native schedule latests: reconcile #42439099803, inspection #42452273701, watchdog #42438566387, recovery #42438384072. At 08:04Z all exceed their 45/75/45/45m freshness budgets. Manual fallback runs do not count. Cron and budgets unchanged.
- TCE WF-06 native #42458256899 failed all four strict HTTP 200 probes with HTTP 503. WF-12 workflow_run #42458270339 confirmed WF-06 active and fresh at its own run time (age/queue 0m) and delivered authenticated Platform heartbeat; by 08:04Z the 25m age budget is exceeded again. Latest native WF-12 #42452308083 remains stale/failing. WF-13 #42458270097 passed recovery.
- Stock scraper scheduled run #42457182511 failed closed before dependency installation because `VNSTOCK_API_KEY` is empty. Stock master CI #42440810105 PASS 7/7. No credential change or ingestion.
- Media CI #42239703151 and Auth CI #42215394539 remain PASS. Auth PR #75/#76 exact-head CI #40446492086/#41329425940 PASS; Supabase merge-trigger effect remains a gate.
- Fresh K3s snapshot #1440: node Ready/ARM64; Media and MicroFE workloads Running 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff for `12d63b4` (no ARM64 manifest); old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. Runner services active/enabled, registration audit outstanding. No Stock/Media VolumeSnapshot references; external backup/DNS ownership unverified. Host restart required; no maintenance performed.
- App repos retain tests/builds and immutable GHCR publication ownership. Platform retains manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication, digest handoff, production apply, scaling, decommission, DNS/database/storage change, or direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 16:55 ICT / 09:55 UTC

- Platform master `1f7e5cd8`; open PR #1452 fixes the decommission preflight sudo boundary. The older docs PR #1442 is superseded by this refreshed tracker and should not be merged.
- Native Platform schedules: reconcile #42467231073 failed on the pre-fix cert-manager remote Kustomize URL; inspection #42452273701 pass but stale; watchdog #42467080859 failed; recovery #42466737776 passed. Inter-arrival gaps 24,773s / 21,396s / 25,092s / 24,958s exceed 45/75/45/45m budgets. Manual/push/workflow_run runs are not native evidence.
- Cert-manager bootstrap now downloads the pinned v1.21.1 release asset through the GitHub API and checks SHA-256 before local Kustomize rendering. Validation #42468403916/#42468403911 passed; post-fix push reconcile #42468465293 passed with no drift and apply skipped.
- Fresh inspection #42468887549 generated `debug/vps-latest.md` at 09:50:50Z. Node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff on `12d63b4` (no matching platform manifest); old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. Only k3s-debug PVC/PV is listed; no Stock/Media VolumeSnapshot references. Decommission preflight itself stopped on a permission error before target namespace inventory; PR #1452 fixes wrapper invocation via sudo.
- TCE WF-06 #42458256899 failed four HTTP 503 probes; WF-12 #42452308083 failed freshness; WF-07 #42453060493 passed. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; Auth PR #75/#76 remain gated by Supabase integration behavior.
- App repositories continue to own tests/builds and immutable GHCR publication. Platform alone owns manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication, digest handoff or production promotion was observed.
- No production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 17:15 ICT / 10:15 UTC

- PR #1452 merged to Platform master `7ccd527e`; exact-head `validate-github-actions` #42469900529 and `validate-manifests` #42469900449 passed. Its post-merge `validate-manifests` push #42469989585 then failed on HTTP 403 from the pinned GitHub Release asset API. PR #1453 adds optional GH_TOKEN support to the helper and every workflow caller, with a regression test and a separate PR-comment job so PR-controlled code has only `contents: read`.
- Post-merge `validate-github-actions` #42469989622 passed. Reconciliation #42469998524 passed GHCR pull preflight, Auth runtime Secret verification, shared pull credential check and targeted lanes; no drift meant no production manifest apply, image promotion or rollout.
- Native schedule evidence is unchanged: reconcile #42467231073 FAIL (09:27:03Z, ~48m old), inspection #42452273701 PASS (05:49:40Z, ~265m old), watchdog #42467080859 FAIL (09:24:53Z, ~50m old), recovery #42466737776 PASS (09:20:06Z, ~55m old). Inter-arrival gaps 24,773s / 21,396s / 25,092s / 24,958s exceed the 45/75/45/45m budgets. Manual/push/workflow_run events are not native schedule evidence.
- Latest K3s snapshot #42468887549 remains the fresh push inspection at 09:50:50Z: node Ready/ARM64; Media/MicroFE Running 1/1; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; older Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. It predates the #1452 sudo fix; a new read-only inspection must confirm the preflight now reaches target namespace inventory.
- TCE WF-06 #42458256899 failed four HTTP 503 probes; WF-12 #42452308083 failed freshness. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; Auth PR #75/#76 remain gated.
- App repos retain tests/builds and immutable GHCR publication ownership. Platform retains manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication/digest handoff, manifest apply, workload scaling, decommission, DNS/database/storage change or host maintenance. TCE market-scan schedule unchanged.


## Latest execution update — 2026-11-08 17:31 ICT / 10:31 UTC

- Platform master `ab2696c2` includes merged PR #1453. Exact-head checks #42470921373/#42470921319/#42470921336 passed. Post-merge manifest validation #42471706415 and Keycloak CI #42471706467 passed; post-merge workflow lint #42471706454 remained in progress at the review cutoff.
- The cert-manager bootstrap helper now uses optional `GH_TOKEN` for the pinned GitHub Release asset API, preserves SHA-256 verification and avoids logging the token. The validation job retains `contents: read`; PR-comment write permission is isolated in a separate job without checkout.
- Read-only inspection #42471706668 was triggered by the helper/preflight path filter and remained in progress at the `Inspect VPS` step. It must complete before claiming the #1452 sudo boundary works against live K3s inventory.
- Native schedule events remain unchanged: Platform reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776; TCE WF-06 #42458256899 and WF-12 #42452308083. Ages exceed their configured freshness budgets; push/manual/workflow_run fallbacks are not native evidence. Cron and budgets unchanged.
- No new app image publication or digest handoff. Stock scraper #42457182511 fails closed on missing `VNSTOCK_API_KEY`; TCE WF-06 has four HTTP 503 probes; Media CI and Auth CI remain last recorded PASS. No production manifest apply, image promotion, workload scaling, decommission, runner retirement or host maintenance.


## Latest execution update — 2026-11-08 17:34 ICT / 10:34 UTC

- PR #1453 merged on Platform master ab2696c2 after exact-head #42470921373/#42470921319/#42470921336 passed. Post-merge #42471706415 (manifest), #42471706454 (workflow lint) and #42471706467 (Keycloak) passed. The cert-manager helper now uses optional read-only GH_TOKEN for the pinned release asset API while preserving SHA-256 verification and isolating PR-write permission.
- Read-only inspection #42471706668 completed; exact-head inspection PR #1454 passed #42471833649 and merged at 77207c26536cb005b2cbcbaf19945ded5069c0df. The sudo decommission preflight reached both retired namespaces, confirmed preserved namespaces, and found no Stock/Media PVC/PV claims or VolumeSnapshot references. This confirms storage-clean preflight only; backup/DNS and Media runner unregistration are still missing.
- Recovery-dispatched reconcile #42471718647: target all, apply mode, image changes disabled. GHCR access and Auth runtime Secret checks passed; shared pull secret unchanged; no-op ServiceAccount/deployment patches; no active Auth/MicroFE/TCE image-pull failures; TCE release pairing passed; GitOps drift false and production apply skipped. MicroFE, TCE and Auth health lanes passed, with Auth/TCE zero-replica maintenance explicitly not represented as live health. Final deployment lane gate passed; recovery-controller notification job remained queued.
- K3s snapshot 10:30:37Z: node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff on 12d63b4; older Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; public OIDC 503; GitOps drift clean.
- Native schedule latests remain Platform #42467231073/#42452273701/#42467080859/#42466737776 and TCE #42458256899/#42452308083. All relevant freshness budgets remain exceeded. No cron or freshness budget changed.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/storage deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## Direct deployment authority audit — 2026-11-08 17:38 ICT / 10:38 UTC

- TCE WF-09 (workflow_dispatch only) performs read-only VPS inspection, creates isolated TCE directories, and uploads source only to /home/ubuntu/tce/development/source.tmp. Its own output says existing Docker containers, nginx, ports and mrcute.space are not modified. Preserve as a manual setup utility; it is not a production deployment authority.
- TCE WF-10 (workflow_call/workflow_dispatch) is explicitly commented staging-only. Its Kubernetes mutations are limited to creating/labeling namespace tce-stg and creating the tce-auth staging Secret. It does not reference tce-prod or microfe-platform. Preserve as staging bootstrap; do not route production releases through it.
- TCE WF-03 is the app-owned ARM64 immutable publisher and validated repository_dispatch sender to Platform. It does not SSH to the VPS.
- Stock deploy.yml is an app-owned ARM64 image publisher. Master pushes may publish full-SHA and version/full-SHA tags; manual publication is blocked unless the explicit repository variable is enabled. It does not hand off production deployment to Platform from this workflow.
- Media WF-03 is an app-owned ARM64 immutable publisher; Media is retired from active Platform GitOps and no Platform handoff is sent. No SSH/Compose authority is added.
- Authentication release.yml is workflow_dispatch-only and app-owned; Platform remains the sole production manifest/Secret/reconcile/rollout authority.
- No workflow was removed. Useful manual staging, release and scheduled jobs are preserved. No direct SSH/Compose production deployment authority was added; TCE market-scan schedule unchanged.


## Scheduled image cleanup safety contract — 2026-11-08 17:40 ICT / 10:40 UTC

- vps-image-cleanup.yml runs weekly Sunday 03:30 UTC. Scheduled and push-triggered runs are forced to DRY_RUN=true; only explicit workflow_dispatch can set dry_run=false.
- Latest native run #42472343489 completed PASS at 10:39:26Z, about 7h09 after the cron time. KEEP_UNUSED_IMAGES=10; script found 8 unused images and remove_count=0. No images were removed.
- The script inventories all Pods and CRI containers, protects images referenced by existing containers (including terminated ones), excludes pinned images, fails closed if a non-terminal Pod reference cannot be resolved, and rechecks Pod/container references before each deletion. The destructive manual path was not invoked.
- This workflow is purposeful maintenance, not a production deployment authority; preserve it and keep it separate from native deployment cadence acceptance.



## Media runner decommission verification contract — PR #1458 (open)

- App ownership is unchanged: Media Generation owns source/tests/builds and immutable image publication; Platform owns only the protected K3s decommission workflow after GitOps ownership retirement.
- The delete-mode workflow now runs both local checks (systemd inactive and disabled/masked/absent; no `Runner.Listener`) and a remote read-only GitHub repository runner-list check for exact runner name `media-generation-k3s-01`.
- Required Platform Actions secret: `MEDIA_RUNNER_AUDIT_TOKEN`. It must be a fine-grained token or GitHub App installation token with repository **Administration: read** on `phanthienquoc/media-generation` only. The verifier calls only `GET /repos/phanthienquoc/media-generation/actions/runners`, paginates, suppresses the token, and fails closed on missing credentials, API/JSON failure or a matching runner. It does not have or request runner deletion permission.
- Operator still performs the stop/disable and GitHub unregister flow separately. The workflow verifies the result; it never stops or unregisters the runner.
- Plan mode remains read-only and token-free. Delete mode retains production Environment approval, typed namespace/backup/DNS attestations, fresh same-run storage preflight and fixed namespace allowlist.
- PR #1458 adds regression coverage for absent/present runner, pagination, missing token and API failure. It is open pending exact-head validation; no decommission was dispatched.
- This contract does not change app publisher ownership, GHCR credentials, GitOps promotion, production apply authority, direct SSH/Compose boundaries or the TCE market-scan schedule.



## Runner audit guard — merged Platform PR #1458

- `decommission-stock-media.yml` delete mode now verifies the Media runner both locally and remotely. Local checks require the exact service to be inactive and disabled/masked/absent and no `Runner.Listener` process.
- Remote check: `GET /repos/phanthienquoc/media-generation/actions/runners`, paginated, exact runner name `media-generation-k3s-01`. It is read-only and fails closed on missing credentials, HTTP/API failure, malformed JSON or a matching runner.
- Required Platform Actions secret: `MEDIA_RUNNER_AUDIT_TOKEN`, fine-grained token/App installation token with **Administration: read** on `phanthienquoc/media-generation` only. No runner deletion permission. Secret existence is not verified by this audit.
- Operator must separately stop/disable and unregister the Media runner. The workflow does not do those actions. Plan mode remains read-only and token-free.
- PR #1458 merged at `098cf54de9e2223bc97db57cca6fbee8334fc80c`; exact-head and post-merge workflow validations passed. No decommission was dispatched.

## Latest Platform runtime evidence — 2026-11-08 18:20 ICT

- Reconcile fallback #42474936543: GHCR preflight PASS; shared `ghcr-pull` unchanged in both active GHCR namespaces; Auth runtime Secret provisioned/verified; no GitOps drift; manifest apply/image promotion skipped. Auth/MicroFE/TCE lanes passed with rollouts skipped; TCE remains zero-replica maintenance, so no live health was asserted.
- Read-only inspection #42475079478 / PR #1459: K3s node Ready ARM64; Media and MicroFE active pods 1/1; Stock Admin/new Backend ImagePullBackOff due missing ARM64 manifest for `12d63b4`; TCE/Auth/Keycloak 0/0; OIDC 503; dedicated Media runner still active/enabled; no Stock/Media PVC/PV/VolumeSnapshot references.
- PR #1459 merged at `ef7a1a15b94acdaf7c46cbecb4aa2391cb90b0f8` after exact-head manifest validation #42475211696 passed. Only `debug/vps-latest.md` changed.


## Latest review — 2026-11-08 18:55 ICT / 11:55 UTC

- Platform master is `a0c1e3ee6cf0cb3d9f168227e6fdfd1a6e5ebdfd`; latest post-merge `validate-manifests` #42475493117 passed. Open Platform PRs #1314/#544/#541/#539 remain draft planning/docs. TCE/Stock/Media have no open PRs; Authentication has #75 ready and #76 draft.
- Native Platform schedule runs remain reconcile #42467231073 (FAIL, pre-cert-manager fix), inspection #42452273701 (PASS but stale), watchdog #42467080859 (FAIL), recovery #42466737776 (PASS but stale). At 11:55Z ages are approximately 148m/365m/150m/155m against 45/75/45/45m budgets. Latest post-fix push validation is not native schedule evidence. Cron and budgets are unchanged.
- Native TCE WF-06 #42458256899 returned four HTTP 503s; WF-12 #42452308083 failed freshness; WF-07 integration #42453060493 passed. No TCE market-scan schedule changes.
- Stock scraper #42457182511 ran on schedule but failed closed due missing `VNSTOCK_API_KEY`; no ingestion. Stock CI #42440810105 is 7/7 PASS but does not publish images.
- Media runner remains active; #1458's remote registration gate is merged, but token configuration and external backup/DNS evidence are not verified. No decommission.
- Auth master CI and both PR validation runs pass; Supabase Preview is skipped. PR #75 has no migration files in its diff, but the integration's production target/merge behavior is still not authoritatively established.
- Reconciliation #42474936543 and recovery #42475042844 passed with no drift, no manifest apply and no image promotion. Read-only inspection #42475079478 passed; its snapshot is ~38m old, within the age budget but not evidence of native inspection cadence.
- No new immutable GHCR publication, digest handoff or production promotion was observed. Keep app-owned publishers and Platform-only production authority boundaries unchanged.


## Latest review — 2026-11-08 19:05 ICT / 12:05 UTC

- Platform master `25c5e390161c5410517f5360885281abd4c1ff49`; PR #1461 merged after exact-head validation #42478273907 PASS and post-merge #42478553173 PASS.
- Authentication PR #75 merged at `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` after updated exact-head validation #42478511082 passed. Auth master push CI #42478653766 is still running. PR #76 remains draft.
- Read-only Supabase recheck: project ACTIVE_HEALTHY, branch status FUNCTIONS_DEPLOYED; repository migration files and remote ledger match 84/84. No migration count change was observed after merge. The external integration run log is not available through the read-only API; do not claim it was independently inspected. No Auth release workflow was dispatched.
- Native Platform schedule events remain reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776; all exceed 45/75/45/45m freshness budgets. Native TCE WF-06 #42458256899 returned 4×503; WF-12 #42452308083 failed freshness; WF-07 #42453060493 passed. No cron/budget changes.
- Stock scraper #42457182511 ran but failed closed because VNSTOCK_API_KEY was empty; dependency installation, entitlement verification and ingestion were skipped. Stock CI #42440810105 is 7/7 PASS but non-publishing.
- K3s inspection #42475079478 is ~47m old and within its snapshot age budget; workload state remains Media/MicroFE 1/1, Stock Admin/desired Backend ImagePullBackOff, TCE/Auth/Keycloak 0/0. No decommission or rollout change.
- Reconciliation #42474936543 and recovery #42475042844 passed with no drift, no manifest apply and no image promotion. No new app publisher or digest handoff.
- Media runner remains active; decommission waits for audit token, external backup/retention and DNS ownership. Keep app-owned publishing and Platform-only production apply boundaries.


## Latest cross-repo execution — 2026-11-08 20:01 ICT / 13:01 UTC

### Current repository and workflow state

| Repository | Master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `192187fffb416dba326055c1a729510d48cb612a` | #1314/#544/#541/#539 (draft) | validate-manifests #42478871584 PASS; heartbeat receiver #42479344664 failed on GitHub API 500 |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | WF-12 #42479336350 schedule/FAIL; WF-13 #42479348862 PASS; fallback WF-06 #42479362379 FAIL 4×503 |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | scraper #42457182511 fail-closed on missing `VNSTOCK_API_KEY`; CI #42440810105 PASS/non-publishing |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS; no new publisher run |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 draft | master CI #42478653766 PASS |

### Schedule, heartbeat and service health

- Platform native schedule latest evidence: reconcile #42467231073 FAIL (09:27:03Z); inspection #42452273701 PASS (05:49:40Z); watchdog #42467080859 FAIL (09:24:53Z); recovery #42466737776 PASS (09:20:06Z). All are stale against 45/75/45/45-minute budgets. No newer native schedule event appeared in the paged Actions history.
- TCE WF-12 #42479336350 ran on native schedule and correctly detected stale WF-06. Its authenticated Platform heartbeat dispatch was accepted. WF-13 #42479348862 then dispatched one deduplicated read-only WF-06 fallback, correlated to exact master SHA. Fallback #42479362379 returned 503 for TCE web, TCE API, Auth liveness and Auth readiness.
- Platform receiver #42479344664 could not complete the source-run API lookup: repeated HTTP 500 from the public GitHub Actions run endpoint. It failed closed before source reconciliation/freshness recovery. Rerun attempt 2 was skipped by the first-attempt-only guard.
- A bounded retry change is proposed in branch `fix/retry-transient-tce-heartbeat-api-500-20261108-2001-ict`: four retries, 45-second retry window, 15-second request timeout and connection-refused retry; permanent 4xx remain fail-closed. No payload identity, permissions, cron, freshness budget or production authority change.
- Stock scheduled scraper ran and failed closed before ingestion because `VNSTOCK_API_KEY` is missing. No new immutable GHCR publisher/digest evidence exists for Stock, TCE, Media or Auth in this review.

### Runtime/deployment boundary

- Latest K3s snapshot #42475079478 is older than the 75-minute snapshot-age budget at this checkpoint; no current health claim should be derived from it. Last recorded workloads: Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin and desired Backend ImagePullBackOff on `12d63b4` due missing ARM64 manifest; TCE/Auth/Keycloak intentional 0/0.
- Reconciliation #42474936543 passed GHCR access and Auth runtime Secret checks, left shared `ghcr-pull` unchanged, found no GitOps drift and skipped apply/promotion/rollout.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE/Stock/Media/Auth app repositories own tests/builds and immutable image publication; Platform owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health verification.
- Preserve useful CI/security/test workflows and purposeful manual/release/scheduled jobs. No workflow was removed. No production mutation, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.
