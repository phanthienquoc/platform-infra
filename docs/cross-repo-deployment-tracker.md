## Execution delta — 2026-11-09 22:19 ICT / 15:19 UTC

- Platform master is now `542e3d37f95bd6c77231a9e5b4f9798ab24b03b6` after PR [#1525](https://github.com/phanthienquoc/platform-infra/pull/1525) squash-merged. Exact validated head: `c24c3cc9ac6300e9ee429c0fa0c8912c2f2bff85`; exact-head `validate-manifests` #42643198502, `validate-github-actions` #42643198496 and `keycloak-ci` #42643198522 all PASS. Post-merge push runs #42643433458, #42643433572 and #42643433668 also PASS.
- PR #1525 closes a decommission safety gap: the shared `scripts/verify-retired-production-manifests.sh` guard now rejects reintroduced Stock/Media manifest trees, namespaces and GHCR image references. Manifest validation uses the same guard; `decommission-stock-media-namespaces.sh` executes it in both plan and delete preflight. Regression output: 1 positive and 5 negative cases PASS; workflow contract validation PASS. Namespace deletion remains manual-only and still requires backup/DNS/runner attestations, GitHub runner unregister verification and fresh storage preflight.
- Post-merge `inspect-vps` push run #42643433567 was still in progress at the last query (15:19:08Z). It is read-only and does not count as native schedule acceptance. Until it completes and a new snapshot is committed, the latest `debug/vps-latest.md` remains generated at 09:37:36Z; at this checkpoint it is approximately 5h41m old and exceeds the 4,500s freshness budget.
- Post-merge `Recover Stale Scheduled Ops` run #42643433651 completed successfully on a push event; it is not a native schedule run. Platform master push validation runs #42643433458/#42643433572 and Keycloak CI #42643433668 passed.
- Other master heads: TCE `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `b71834758d278e50e6ce07b5086fe45e9d9b3350`.
- Open owner-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. TCE, Stock and Media have no open PRs.
- TCE application build/format/test runs #42586355695/#42586356008/#42586355696 PASS. Native WF-06 #42594757482 and manual WF-06 #42594805077 fail all four strict public probes with HTTP 503 (TCE API/web and Auth readiness/liveness); WF-12 #42587926693 reports stale schedule delivery. TCE/Auth remain intentional 0/0; no scaling or health-check weakening.
- Stock master CI #42610360402 PASS 7/7, including ARM64 non-publishing build and scraper preflight contract. The latest scraper schedule failure #42457182511 ran old source SHA `e6469ac6617142b349144101a1192cb6aa7104ad`; it does not prove the current master credential state. Current-master authenticated VNSTOCK preflight and production digest publication remain unverified.
- Media master CI #42539512417 PASS; latest verified Media publisher run #41158598649 is historical (2026-10-31). No current production digest handoff is verified. Media runner service/listener remained active in the stale snapshot; remote GitHub registration, external backup/retention and DNS ownership remain unverified.
- Authentication master CI #42586362115 PASS; no current production publisher run/digest handoff is verified.
- Fresh native schedule evidence is recorded in issue [#1497 comment #6743653448](https://github.com/phanthienquoc/platform-infra/issues/1497#issuecomment-6743653448). All six Platform/TCE native inter-arrival gaps and ages exceed existing budgets. Administrator scheduler enqueue/delivery telemetry remains outstanding; repository run history cannot distinguish delayed, dropped or never-enqueued ticks.
- Scheduled reconciliation #42575932602 completed successfully with preflight success, drift=false and manifest apply correctly skipped. Auth runtime Secret required keys were verified; TCE/Auth remained intentional 0/0. This does not establish live public health.
- No production GHCR publication, digest promotion, manifest apply, rollout, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only; no direct SSH/Compose authority. Preserve cron/freshness budgets and the TCE market-scan schedule.

Checkpoint: `docs/cross-repo-deployment-checkpoints/2026-11-09-2219-ict.md`.

## Execution delta — 2026-11-09 21:25 ICT / 14:25 UTC

- Platform master is now `81191ee478c97a436a1f91feacf1f042c90d8a27` after PR [#1523](https://github.com/phanthienquoc/platform-infra/pull/1523) merged at this SHA. PR #1523 exact-head `validate-manifests` #42634259014 PASS; post-merge master push #42634355055 PASS. Its 21:22 checkpoint correctly captured the pre-merge Platform head `49e5e764`; this delta records the resulting master head.
- PR #1522 remains merged at `49e5e764f6aca5108ac6d01166aef5a274f8e644`. Its exact-head `validate-github-actions` #42633638893 and `validate-manifests` #42633638946 PASS; post-merge #42633860020/#42633860140 PASS. Dispatch verifier requires unique completed-success promotion jobs; self-tests report 4 positive and 26 negative cases.
- Other master heads unchanged: TCE `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `b71834758d278e50e6ce07b5086fe45e9d9b3350`.
- Open owner-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE, Stock or Media.
- TCE latest strict health evidence remains WF-06 #42594757482 (native) and #42594805077 (manual), with all four public probes HTTP 503; WF-12 #42587926693 remains failed freshness evidence. TCE/Auth remain intentional 0/0; no scaling or health-check weakening.
- Stock master CI #42610360402 PASS 7/7; current-master authenticated VNSTOCK preflight and production digest publication remain unverified. Media master CI #42539512417 PASS; Auth master CI #42586362115 PASS. No production publisher run/digest handoff was verified for these apps.
- Scheduler evidence and limitations are recorded in issue #1497 comment #6742393810. TCE latest visible native WF-06/WF-12 events are still #42594757482/#42587926693; Platform latest unfiltered first page contains no schedule event but is pagination-limited. Administrator scheduler enqueue/delivery telemetry remains required. Preserve all cron/freshness budgets and TCE market-scan schedule.
- Latest K3s snapshot remains generated at 09:37:36Z and is stale beyond 4,500s; do not authorize rollout/decommission from it. No new read-only inspection was available in this run.
- No production publication/promotion/apply/rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only; no direct SSH/Compose authority.

Checkpoint: `docs/cross-repo-deployment-checkpoints/2026-11-09-2125-ict.md`.

## Execution delta — 2026-11-09 21:22 ICT / 14:21:58 UTC

- Current master heads: Platform `49e5e764f6aca5108ac6d01166aef5a274f8e644`; TCE `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `b71834758d278e50e6ce07b5086fe45e9d9b3350`.
- Platform PR [#1522](https://github.com/phanthienquoc/platform-infra/pull/1522) merged by squash at `49e5e764f6aca5108ac6d01166aef5a274f8e644`, exact validated head `a1cd335baebdd582f033bcc6ca64034577699b9d`. Exact-head `validate-github-actions` #42633638893 and `validate-manifests` #42633638946 PASS. Post-merge master push #42633860020 and #42633860140 PASS. The GitOps-ready dispatch verifier now requires exactly one matching completed-success promotion job for MicroFE, each of the two TCE jobs, and Auth; duplicate-name evidence is rejected. Self-tests: 4 positive and 26 negative cases.
- Open human-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. TCE, StockDividend and Media Generation have no open PRs. No owner-gated PR was merged.
- TCE latest application checks remain WF-01 #42586355695, WF-05 #42586355696 and WF-02 #42586356008 PASS. Native WF-06 #42594757482 and manual WF-06 #42594805077 fail; job logs for the four public probes confirm HTTP 503 for TCE API, TCE web, Auth readiness and Auth liveness. WF-12 native #42587926693 failed; its workflow_run recovery/watchdog runs are not native schedule acceptance.
- Stock master CI #42610360402 PASS 7/7, including the side-effect-free scraper credential-preflight and non-publishing ARM64 build checks. No current-master authenticated VNSTOCK preflight, production publication or digest handoff was performed. The older scraper failure #42457182511 used commit `e6469ac` and is not proof of current master secret state.
- Media master CI #42539512417 PASS; no production publisher run or Platform handoff. Authentication master CI #42586362115 PASS; no production release publisher run.
- Native TCE schedule evidence visible in the latest 30-run page: WF-06 #42594757482 at 09:36:43Z (age 17,115s at 14:21:58Z) and WF-12 #42587926693 at 08:42:40Z (age 20,358s); both exceed the existing 1,500s budgets. Platform's latest unfiltered Actions API first page contains 30 items but no schedule event (9 push, 15 pull_request, 4 workflow_run, 1 repository_dispatch, 1 workflow_dispatch). This first-page observation is not proof that no later native event exists; the connector does not expose the filtered event=schedule query. Last fully filtered Platform evidence remains comment #6740838807 at 13:04:20Z. Issue #1497 received new evidence/limitation comment #6742393810.
- Latest committed K3s inspection file remains generated at 09:37:36Z; age is 17,062s at this checkpoint, beyond the 4,500s freshness budget. Last recorded node was Ready/ARM64, disk 56%, RAM ~19 GiB, host restart required; Stock desired workloads had ImagePullBackOff; TCE/Auth/Keycloak were intentional 0/0; Media/MicroFE were 1/1. This stale snapshot cannot authorize rollout, cleanup or decommission.
- Last previously verified scheduled reconciliation #42575932602 had drift=false, Auth runtime Secret provisioned/verified, shared `ghcr-pull` unchanged, and manifest apply/promotion/rollout skipped. Do not conflate that internal reconciliation result with public TCE health.
- No production GHCR publication, digest promotion, manifest apply, rollout, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority was added. TCE market-scan schedule unchanged.

Checkpoint: `docs/cross-repo-deployment-checkpoints/2026-11-09-2122-ict.md`.

## Execution delta — 2026-11-09 20:04 ICT / 13:04:20 UTC

- Current master heads: Platform `f9984d4dcac473164102d5217ff2a177877fad34`; TCE `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `b71834758d278e50e6ce07b5086fe45e9d9b3350`.
- Platform PR #1520 exact-head #42614267017 and post-merge master push #42614397667 PASS. Latest master app runs: TCE WF-02 #42586356008 PASS with native/manual WF-06 and native WF-12 failures; Stock CI #42610360402 PASS 7/7; Media CI #42539512417 PASS; Auth CI #42586362115 PASS.
- Open human-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE, Stock or Media. Current combined commit-status queries for draft heads returned no status contexts; do not infer check success.
- Native `event=schedule` query at 13:04:20Z (master, attempt 1 only) confirms gaps/ages: Platform reconcile 24,326s/22,200s; inspection 27,768s/12,412s; recovery 22,459s/24,623s; watchdog 22,698s/24,266s; TCE WF-06 27,454s/12,457s; WF-12 25,452s/15,700s. All exceed budgets. Issue #1497 received fresh evidence comment #6740838807; administrator scheduler delivery evidence remains outstanding. No cron/freshness or TCE market-scan schedule changes.
- Latest K3s inspection #42594848960 succeeded, but `debug/vps-latest.md` was generated 09:37:36Z and is 12,404s old at checkpoint, beyond 4,500s freshness. Node was Ready/ARM64, disk 56%, RAM ~19 GiB, restart required; Platform and Media runner services active; Media/MicroFE 1/1; Stock desired workloads ImagePullBackOff; TCE/Auth/Keycloak 0/0; public OIDC 503. Stale snapshot cannot authorize rollout/decommission.
- Scheduled reconciliation #42575932602 (06:54:20Z) completed with mode=apply, target=all, allow_image_changes=false. Logs confirm Auth runtime Secret provisioned and verified; shared `ghcr-pull` unchanged; no blocked image pulls in MicroFE/TCE; diff clean; manifest apply skipped; Auth/TCE/MicroFE rollout checks skipped; Keycloak skipped. This internal lane success is distinct from TCE public WF-06 HTTP 503 failures.
- Stock current-master credential preflight is still unverified; prior scraper failure #42457182511 used old SHA `e6469ac`. No production publisher/digest handoff. Auth/TCE remain tag-pinned and fail-closed pending digest promotion. Stock/Media remain retired from Platform GitOps but workloads still exist; decommission gates remain open.
- No production publication/promotion/apply/rollout/scaling/deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

Checkpoint: `docs/cross-repo-deployment-checkpoints/2026-11-09-2004-ict.md`.

---

## Execution delta — 2026-11-09 19:00 ICT / 11:59:26 UTC

- Platform master `5647035abe2f787185a8089970b7f67312170f8a`; PR #1519 exact-head validate-manifests #42610714863 PASS and post-merge master push #42610795648 PASS. PR #1518 post-merge #42609219961 PASS.
- TCE master `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; WF-01P #42586355695, WF-02 #42586356008 and WF-05 #42586355696 PASS. Native WF-06 #42594757482 and manual WF-06 #42594805077 fail all four strict endpoint checks; manual logs confirm HTTP 503 for TCE API/web and Auth readiness/liveness.
- Stock master `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; PR #41 exact-head CI #42609809654 and post-merge master CI #42610360402 both PASS 7/7. Native ARM64 build validation used non-publishing mode. No production publisher run or digest handoff. Last scraper failure #42457182511 used older commit `e6469ac`; current master secret state is unverified.
- Media master `dcd698699c65ba6e73f6b43838975144777131c3`; master CI #42539512417 PASS. Dedicated runner remained active/enabled/listener-present in the latest inspection snapshot; remote registration absence is unverified.
- Authentication master `b71834758d278e50e6ce07b5086fe45e9d9b3350`; master CI #42586362115 PASS; PR #76 remains draft.
- Open PRs: Platform #1314/#544/#541/#539 (drafts) and Auth #76 (draft); no open PRs in TCE, Stock or Media.
- Native schedule evidence as of 11:59:26Z: Platform reconcile/inspection/recovery/watchdog gaps 24,326s/27,768s/22,459s/22,698s; TCE WF-06/WF-12 gaps 27,454s/25,452s. All six exceed existing budgets and ages. Issue #1497 received evidence comment #6739589506; administrator enqueue/delivery telemetry is still required.
- Latest K3s inspection #42594848960 generated `debug/vps-latest.md` at 09:37:36Z and is 8,510s old (>75m budget). Do not use for rollout/decommission authorization. Last observed Stock desired `12d63b4` has no matching ARM64 manifest; TCE/Auth/Keycloak 0/0; Media runner active.
- Reconciliation #42595146384 was workflow_dispatch: `ALLOW_IMAGE_CHANGES=false`, drift=false, apply skipped; TCE/Auth intentional zero-replica maintenance; MicroFE active health gate passed; Auth runtime Secret keys present; Keycloak lane skipped. Recovery #42595660819 was repository_dispatch. Neither is native schedule acceptance.
- No production publication/promotion, manifest apply, rollout, scaling, namespace/storage deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` sole production apply authority; `inspect-vps.yml` read-only. TCE market-scan schedule unchanged.

## 2026-11-09 19:00 ICT readiness checkpoint

See [checkpoint](cross-repo-deployment-checkpoints/2026-11-09-1900-ict.md) for exact run IDs, inter-arrival gaps, ages, K3s snapshot limits, owner actions and safety evidence.

## Execution delta — 2026-11-09 18:23 ICT

### Repository heads, PRs and validation evidence

- Platform Infra master: `4348742602f6be4ba4ead0893026f21704053fdb`. PR [#1518](https://github.com/phanthienquoc/platform-infra/pull/1518) squash-merged at this SHA from exact head `d6169ae151a6d0dc5a8cb5f257f7a7f4c644a86f`; exact-head `validate-manifests` [#42608166754](https://github.com/phanthienquoc/platform-infra/actions/runs/42608166754) PASS. The connector does not expose post-merge push/schedule/dispatch runs for this master commit; no post-merge result is claimed.
- PR [#1517](https://github.com/phanthienquoc/platform-infra/pull/1517) remains merged at `f480b8e3fbca130e0d64277983a9c12e55a470f7`. Exact-head #42607555613/#42607555700 and post-merge #42607717790/#42607718023 all PASS. The final delete step re-audits the exact Media runner immediately before namespace deletion and unsets the read-only audit token before invoking the namespace script; it does not stop/unregister the runner or delete namespaces.
- TCE Dashboard master: `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; last verified WF-01 #42586355695, WF-02 #42586356008 and WF-05 #42586355696 PASS. Latest confirmed strict WF-06 failure #42594757482 returned HTTP 503 from all four public TCE/Auth probes; WF-12 #42587926693 remains stale-delivery evidence.
- StockDividend master: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; PR [#41](https://github.com/phanthienquoc/stockdividend/pull/41) squash-merged at this SHA from exact head `b212fa0c4f2e2640230977b3d4c8184a7130998e`. Exact-head StockDividend CI [#42609809654](https://github.com/phanthienquoc/stockdividend/actions/runs/42609809654) completed PASS 7/7, including the release/preflight contract and native ARM64 non-publishing builds. The PR changed only the validator; no scraper dispatch or production publication occurred. The connector does not expose post-merge push runs for this commit.
- Media Generation master: `dcd698699c65ba6e73f6b43838975144777131c3`; last verified application CI #42539512417 PASS.
- Authentication master: `b71834758d278e50e6ce07b5086fe45e9d9b3350`; last verified CI #42586362115 PASS.
- Open human-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. Stock PR #41 is merged; TCE, StockDividend and Media Generation have no open PRs.

### Stock scraper preflight contract hardening

- The existing manual `run_scraper.yml` supports `preflight_only=true`: it checks `VNSTOCK_API_KEY`, verifies an authenticated non-guest VNStock tier, and guards Chromium installation and scraper ingestion with `preflight_only != true`.
- PR #41 merged at `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` from exact head `b212fa0c4f2e2640230977b3d4c8184a7130998e`; exact-head CI #42609809654 passed all seven jobs, including native ARM64 non-publishing builds.
- `scripts/validate-production-release-contract.sh` now enforces the exact eight-step scraper job sequence, so an added/renamed/reordered step fails CI until explicitly reviewed. MongoDB and Telegram credentials must appear exactly once and only inside the final scraper-ingestion step. No post-merge push result is claimed.
- This is validator-only. No scraper dispatch, credential read, ingestion, MongoDB/Telegram write, GHCR publication or Platform handoff was performed. The weekend schedule remains `0 1 * * 0,6`.

### Schedule, reconciliation and runtime evidence

- Latest complete native schedule evidence in the tracker remains 11:17:20Z on 2026-11-09; all six Platform/TCE gaps and ages exceeded their existing budgets. Issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) remains open for authoritative GitHub administrator enqueue/delivery evidence. The available commit-workflow-runs connector is PR-event filtered; empty master results do not prove no newer scheduled runs exist.
- Reconciliation #42595146384 was `workflow_dispatch`, not native schedule: Auth runtime Secret provisioned/verified, shared `ghcr-pull` unchanged, drift=false, manifest apply and image promotion skipped. Recovery #42595660819 was `repository_dispatch` fallback, not native schedule acceptance.
- Latest K3s snapshot remains `debug/vps-latest.md`, generated 2026-11-09T09:37:36Z. It is now beyond the 75-minute inspection budget. Node Ready/ARM64, disk 56% (~21 GiB free), RAM ~19 GiB, host restart required; Media/MicroFE 1/1 with digest evidence; Stock desired tag `12d63b4` lacks a matching ARM64 manifest; TCE/Auth/Keycloak 0/0. Do not use this stale snapshot to authorize rollout or decommission.
- Media runner was active/enabled in that snapshot. External backup/retention, authoritative DNS ownership and remote runner registration remain unverified. The final runner audit guard is defense in depth only; no runner retirement or namespace deletion occurred.

### Next actions and safety

1. GitHub administrator: provide authoritative schedule enqueue/delivery evidence for #1497; preserve cron and freshness budgets.
2. Stock owner: run the manual `preflight_only=true` workflow against current master to verify `VNSTOCK_API_KEY` and authenticated tier without ingestion; separately approve ARM64 publication and digest capture.
3. TCE/Auth owners: resolve HTTP 503 and approve recovery/rollback before restoring replicas.
4. Media owner/operator: verify external backup/retention, authoritative DNS ownership and remote runner registration before protected decommission.
5. Platform operator: obtain a fresh read-only K3s inspection before any runtime mutation; host maintenance requires an approved window and rollback plan.

No production GHCR publication, digest promotion, production manifest apply, rollout, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred in this execution. The earlier Auth runtime Secret provisioning in #42595146384 remains the only confirmed production mutation in the latest reconciliation evidence; shared `ghcr-pull` was unchanged. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

Last reviewed: **2026-11-09 18:23 ICT**

# Cross-Repository Production Deployment Tracker

## Execution delta — 2026-11-09 18:17 ICT / 11:17 UTC

### Platform PR #1517 merged — final Media runner retirement re-audit

- PR [#1517](https://github.com/phanthienquoc/platform-infra/pull/1517) squash-merged at `f480b8e3fbca130e0d64277983a9c12e55a470f7` from exact head `37d99cb3b7fda0db8d27235da6e3d24550f6858b`.
- Exact-head `validate-github-actions` [#42607555613](https://github.com/phanthienquoc/platform-infra/actions/runs/42607555613) PASS; `validate-manifests` [#42607555700](https://github.com/phanthienquoc/platform-infra/actions/runs/42607555700) PASS.
- Post-merge push `validate-github-actions` [#42607717790](https://github.com/phanthienquoc/platform-infra/actions/runs/42607717790) PASS; `validate-manifests` [#42607718023](https://github.com/phanthienquoc/platform-infra/actions/runs/42607718023) PASS.
- A superseded exact-head attempt #42607277216 exposed an outdated workflow-contract assertion that required a one-line `run:` command. The workflow was intentionally converted to a multiline final step; the validator assertion was corrected to check the command and enforce ordering. The final exact-head and post-merge checks above are all green.
- The final destructive step now re-runs `verify-media-runner-retired.sh` (local service inactive/disabled, no listener process, and exact Media repository runner absent from the paginated GitHub Actions runner API), then unsets `MEDIA_RUNNER_AUDIT_TOKEN` before invoking `decommission-stock-media-namespaces.sh delete`. Earlier audit and fresh storage preflight remain. The root-owned wrapper still requires all four typed attestations and independently rechecks PVC/PV/VolumeSnapshot constraints and preservation of TCE/MicroFE namespaces.
- This closes a check/use gap in the protected delete job. It does not stop/unregister the runner or delete either namespace. External backup/retention, DNS ownership and remote runner evidence remain operator prerequisites.

### Repository heads, open PRs and current CI

- Platform Infra master: `f480b8e3fbca130e0d64277983a9c12e55a470f7`; PR #1517 merged.
- TCE Dashboard: `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; master WF-01 #42586355695, WF-02 #42586356008, WF-05 #42586355696 PASS.
- StockDividend: `1a18cabf32c6cc5f85f4157b5142a6d9d9b5`; master CI #42533562194 PASS 7/7, ARM64 image builds non-publishing.
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`; master CI #42539512417 PASS.
- Authentication: `b71834758d278e50e6ce07b5086fe45e9d9b3350`; master CI #42586362115 PASS.
- Open human-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. TCE, StockDividend and Media Generation have no open PRs.

### Native schedule and runtime evidence refresh — 2026-11-09 11:17:20 UTC

No new native schedule run appeared after the 11:02:35Z query. Only `event=schedule`, `master`, attempt 1 is counted.

| Workflow | Latest native run | Inter-arrival gap | Age at 11:17:20Z | Existing budget |
|---|---:|---:|---:|---:|
| Platform reconcile | #42575932602 | 24,326s | 15,780s | 2,700s |
| Platform inspection | #42594848960 | 27,768s | 5,992s | 4,500s |
| Platform recovery | #42571777920 | 22,459s | 18,203s | 2,700s |
| Platform watchdog | #42572369962 | 22,698s | 17,846s | 2,700s |
| TCE WF-06 | #42594757482 | 27,454s | 6,037s | 1,500s |
| TCE WF-12 | #42587926693 | 25,452s | 9,280s | 1,500s |

All current ages and inter-arrival gaps remain beyond budget. Platform watchdog #42595132043 failed on stale native reconcile/recovery and all four Platform gap checks. It separately observed TCE WF-06 #42594757482 was delivered natively, but all four endpoint probes returned HTTP 503. Issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) contains the 11:02Z administrator request and exact evidence. No cron, freshness budget, strict health probe or TCE market-scan schedule changed.

### Reconciliation and app-owner blockers

- Reconciliation #42595146384 was workflow_dispatch, not native schedule: `mode=apply`, `target_app=all`, `allow_image_changes=false`; Auth runtime Secret provisioned/verified; shared `ghcr-pull` unchanged; no image-pull failures for active MicroFE/TCE deployments; drift=false; manifest apply and image promotion skipped. TCE/Auth zero-replica maintenance was not treated as live health; Keycloak skipped.
- Recovery #42595660819 was repository_dispatch fallback and is not native schedule acceptance.
- Stock `.github/workflows/run_scraper.yml` already exposes manual `workflow_dispatch` input `preflight_only=true`: it checks `VNSTOCK_API_KEY` and authenticated non-guest VNStock entitlement, then skips Chromium and ingestion. The last scheduled scraper failure #42457182511 was on older SHA `e6469ac`; current secret state remains unverified. Exact next action: Stock owner runs this manual preflight against current master, then separately approves any ARM64 publication.
- Latest K3s snapshot #1515 / `debug/vps-latest.md` generated 09:37:36Z is now ~100m old, beyond the 75m inspection budget. Node Ready/ARM64, disk 56%, RAM ~19 GiB, restart required; Media/MicroFE 1/1 with digest evidence; Stock desired tag `12d63b4` has no matching ARM64 manifest; TCE/Auth/Keycloak 0/0. Do not use the stale snapshot to authorize rollout/decommission.
- Media runner service was active/enabled in the snapshot. External backup/retention, DNS ownership and remote runner registration remain unverified. No runner retirement or namespace deletion.

No production GHCR publication, digest promotion, manifest apply, rollout, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

## Execution delta — 2026-11-09 18:02 ICT / 11:02 UTC

### Repository heads, PRs and current master checks

- Platform Infra: `7c6f2b3239067bb81024fc12758bba33c1df2c4b`; latest master push validation [#42599052606](https://github.com/phanthienquoc/platform-infra/actions/runs/42599052606) PASS.
- TCE Dashboard: `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; master WF-01 #42586355695, WF-02 #42586356008 and WF-05 #42586355696 PASS.
- StockDividend: `1a18cabf32c6cc5f85f4157b5142a6d9d9b5`; master CI [#42533562194](https://github.com/phanthienquoc/stockdividend/actions/runs/42533562194) PASS 7/7; ARM64 image builds in this run used `push=false`.
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`; master CI [#42539512417](https://github.com/phanthienquoc/media-generation/actions/runs/42539512417) PASS.
- Authentication: `b71834758d278e50e6ce07b5086fe45e9d9b3350`; master CI [#42586362115](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42586362115) PASS.

Open human-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. New Platform safety PR #1517 is open from `fix/decommission-media-runner-final-audit-20261109-1802-ict`; it re-runs the Media runner retirement audit in the final namespace-delete step, unsets the audit token before invoking the namespace script, and extends the workflow contract validator. Exact-head checks are being run; no decommission operation is part of the PR. TCE, StockDividend and Media Generation have no open PRs.

### Latest reconciliation and recovery — keep event types distinct

- Platform reconciliation [#42595146384](https://github.com/phanthienquoc/platform-infra/actions/runs/42595146384) was a `workflow_dispatch`, not a native scheduled run. Inputs were `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- It provisioned and verified the Auth runtime Secret; the shared `ghcr-pull` Secret was unchanged. The image-pull restart helper found no image-pull failures for the active MicroFE and TCE deployments. GitOps drift was false, so manifest apply and image promotion were skipped.
- TCE and Auth workload-health jobs explicitly recognized intentional zero-replica maintenance and did not assert live health. Keycloak lane was skipped. The Stock desired pods still showed ImagePullBackOff for tag `12d63b4`; this reconcile did not publish or promote a Stock image.
- Recovery [#42595660819](https://github.com/phanthienquoc/platform-infra/actions/runs/42595660819) was a `repository_dispatch` fallback and succeeded. It is not native schedule acceptance.

### Native schedule evidence — 2026-11-09 11:02:35 UTC

Only `event=schedule`, `master`, attempt 1 was counted. All inter-arrival gaps and current ages exceed existing budgets.

| Workflow | Latest native run | Inter-arrival gap | Age at 11:02:35Z | Existing budget |
|---|---:|---:|---:|---:|
| Platform reconcile | #42575932602 | 24,326s | 14,895s | 2,700s |
| Platform inspection | #42594848960 | 27,768s | 5,107s | 4,500s |
| Platform recovery | #42571777920 | 22,459s | 17,318s | 2,700s |
| Platform watchdog | #42572369962 | 22,698s | 16,961s | 2,700s |
| TCE WF-06 | #42594757482 | 27,454s | 5,152s | 1,500s |
| TCE WF-12 | #42587926693 | 25,452s | 8,395s | 1,500s |

Platform watchdog [#42595132043](https://github.com/phanthienquoc/platform-infra/actions/runs/42595132043) failed on stale native reconciliation (165m), stale native recovery (205m) and all four Platform inter-arrival checks. It separately observed native TCE WF-06 #42594757482 was delivered, but that run failed all four public probes: TCE web/API and Auth liveness/readiness returned HTTP 503. Service health is separate from schedule delivery. Issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) was updated with this evidence; administrator scheduler enqueue/delivery evidence is still required. No runner queue saturation is established.

No cron expression, freshness budget, strict HTTP 200 check or TCE market-scan schedule was changed.

### K3s and decommission readiness

- Latest read-only snapshot remains PR #1515 / `debug/vps-latest.md`, generated 2026-11-09T09:37:36Z. It is 85m old at this checkpoint, beyond the 75m inspection budget; obtain a fresh read-only inspection before any runtime mutation.
- Snapshot: K3s node Ready/ARM64; disk 56% (~21 GiB free); available RAM ~19 GiB; host `restart_required=yes`. Media and MicroFE workloads 1/1 with digest evidence. Stock Admin×2 and desired Backend image pulls fail for `12d63b4` (no matching `linux/arm64` manifest); legacy Stock workloads 1/1 do not have RepoDigest promotion evidence. TCE/Auth/Keycloak remain 0/0.
- Media and Platform runner services were active/enabled in the snapshot. External backup/retention, authoritative DNS ownership and remote Media runner registration remain unverified. In-cluster PVC/PV/snapshot cleanliness does not authorize namespace deletion.
- PR #1517 adds a final-step re-audit of the dedicated Media runner's local service/process state and GitHub repository runner registration, immediately before namespace deletion. The token is unset before the namespace script runs. This is defense in depth only; no runner stop/unregister or namespace deletion occurred.

### Next actions and safety

1. GitHub administrator: provide authoritative schedule enqueue/delivery evidence for #1497; keep cron and budgets unchanged.
2. Stock owner: run current-master safe credential preflight; then approve a new full-source-SHA ARM64 publication and capture registry digest evidence. The old scraper failure #42457182511 used an older source SHA and does not establish current secret state.
3. TCE/Auth owners: resolve the four HTTP 503 probes and approve recovery/rollback before replica restoration.
4. Media owner/operator: verify external backup/retention, DNS ownership and remote runner registration before protected decommission.
5. Platform operator: obtain a fresh read-only K3s snapshot before any runtime mutation; host restart/package maintenance requires an approved window and rollback plan.

No production GHCR publication, digest promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred in this checkpoint. Auth runtime Secret provisioning during reconciliation #42595146384 is the confirmed production mutation; `ghcr-pull` remained unchanged. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

Last reviewed: **2026-11-09 18:17 ICT / 2026-11-09 11:17 UTC**

## Execution delta — 2026-11-09 17:00 ICT / 10:00 UTC

### Repository and PR state

Current default-branch heads:
- Platform Infra: `9530a7abd61b2b79b8c51cd9ea698ea44dc49e59` (inspection snapshot #1515)
- TCE Dashboard: `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`
- StockDividend: `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5`
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`
- Authentication: `b71834758d278e50e6ce07b5086fe45e9d9b3350`

Open human-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. TCE Dashboard, StockDividend and Media Generation have no open PRs. No draft was merged.

The current Platform master includes inspection snapshot commit #1515 (`9530a7ab`). It updates `debug/vps-latest.md` from 08:38:41Z to **09:37:36Z** and changes inspection evidence only; no production manifest or workload was changed.

### Workflow and check evidence re-read

- Platform PR #1514 exact-head `validate-manifests` run [#42591267072](https://github.com/phanthienquoc/platform-infra/actions/runs/42591267072) PASS. PR #1512 exact-head `validate-manifests` [#42587680995](https://github.com/phanthienquoc/platform-infra/actions/runs/42587680995) PASS. The PR-only run connector does not expose post-merge push/schedule/dispatch runs for current master; no such post-merge result is claimed for #1514 or inspection #1515.
- TCE PR #1032 exact-head runs WF-01P #42585765728, WF-02 #42585765734, WF-05 #42585765722 and WF-08B #42585765835 all PASS. WF-08B's two test jobs passed; publisher and dispatch jobs were skipped as expected for a PR event, so this is not production publication evidence.
- StockDividend CI [#42533247153](https://github.com/phanthienquoc/stockdividend/actions/runs/42533247153) passed all seven jobs. Its ARM64 image builds were non-publishing; immutable GHCR publication was not exercised by this run.
- Media application test/build [#42539297802](https://github.com/phanthienquoc/media-generation/actions/runs/42539297802) PASS.
- Authentication service CI [#42585818369](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42585818369) PASS, including native ARM64 non-publishing build and release-contract validation.
- Combined-status queries for the five current master SHAs returned no status entries. The connected workflow-run view is PR-event filtered; empty results do not prove that newer push, schedule or repository_dispatch runs do not exist.

Historical run-ID correction: the TCE WF-08B exact-head run is **#42585765835**, not #42585865835. The latter was a typo in the 15:15 checkpoint and has been corrected there and in rolling references.

### Fresh read-only K3s inspection

Source: `debug/vps-latest.md`, generated **2026-11-09T09:37:36Z** (16:37:36 ICT).

- Node `tce-k3s-01` Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2. Disk 56% (~21 GiB free), available RAM ~19 GiB; host still reports `restart_required: yes`.
- Docker inventory: 20 images, 9.195 GB total; 5.773 GB reported reclaimable. No cleanup was performed.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry digest evidence.
- Stock Admin has two 0/1 ImagePullBackOff pods; desired Stock Backend has a 0/1 pull failure. Events explicitly say tag `12d63b4` has no matching `linux/arm64` manifest. Legacy Stock Backend/Frontend remain 1/1 on older tags, but do not provide registry RepoDigest evidence suitable for promotion.
- TCE frontend/service, MicroFE Auth and Keycloak remain intentional 0/0. Both public OIDC discovery probes return HTTP 503; this is not live health.
- Stock and Media namespaces have no PVC, PV claim or VolumeSnapshot references in this inspection. The unrelated `k3s-debug` namespace still owns a PVC/PV. Stock/Media namespaces still contain Secrets/TLS credentials, Services, Ingresses, Deployments and ReplicaSets; storage-clean does not authorize namespace deletion.
- Both Platform and Media runner services are active/enabled with listeners present. Remote GitHub runner registration is not inferred from host process state.
- GitOps drift is reported clean. Ingress hostnames remain; DNS ownership must be checked against authoritative provider records before decommission.

This snapshot is fresh enough for current diagnosis, but it does not authorize production rollout, namespace deletion, runner retirement, DNS changes or host maintenance.

### Native schedule and service blockers

Issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) remains open. Latest authoritative all-event schedule evidence available in the tracker remains 05:02:47Z; the current all-event cadence is unverified because this connector does not expose a complete Actions run enumeration or scheduler enqueue evidence. Preserve all cron expressions and freshness budgets.

TCE WF-06 #42548397383 remains the last confirmed strict health failure: four public probes returned HTTP 503. Stock's prior scraper failure #42457182511 checked out older source commit `e6469ac`; it does not establish the current master secret state. Do not infer `VNSTOCK_API_KEY` is currently missing without a current safe preflight.

### Exact next actions

1. GitHub administrator: provide authoritative schedule enqueue/delivery evidence for issue #1497; do not change cron or freshness budgets.
2. Stock owner: run safe credential preflight against current master; separately approve a new full-source-SHA ARM64 image publication, then capture immutable registry digests. Do not overwrite tag `12d63b4`.
3. TCE/Auth service owners: diagnose HTTP 503 and approve recovery/rollback before restoring any replicas.
4. Media owner/operator: verify external backup/retention, DNS ownership and remote runner registration before protected decommission.
5. Platform operator: use the fresh snapshot for diagnosis only; require a new read-only inspection immediately before any later runtime mutation and an approved host maintenance window.

No production GHCR publication, digest promotion, manifest apply, rollout, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

## Execution delta — 2026-11-09 16:03 ICT / 09:03 UTC

- Platform PR [#1512](https://github.com/phanthienquoc/platform-infra/pull/1512) squash-merged at `296665e832964124f34fd768bafbfa8bddd925d9` from exact head `a428a7d50e84711a31ab9abbc71166e05b1f3297`; exact-head validate-manifests #42587680995 PASS. This docs-only PR did not trigger validate-github-actions; post-merge push CI is not exposed by the connected run view.
- Corrected the TCE WF-08B exact-head run reference to **#42585765835**. The PR-only run list confirms this ID; the two MicroFE tests passed and publisher/dispatch jobs were skipped as expected for a PR event. The prior typo #42585765835 returned 404.
- Current masters: Platform `296665e8`, TCE `65af89f6`, Stock `1a18cabf`, Media `dcd69869`, Auth `b7183475`. Open human-decision drafts: Platform #1314/#544/#541/#539 and Auth #76; no open PRs in TCE/Stock/Media.
- Latest inspection snapshot #1513: `debug/vps-latest.md` generated `2026-11-09T08:38:41Z`; node Ready/ARM64, disk 56%, ~21 GiB free, RAM ~19 GiB, restart_required=yes. Media/MicroFE 1/1 with digest evidence; Stock Admin and desired Backend pulls fail (ARM64 manifest mismatch); TCE/Auth/Keycloak 0/0; public OIDC probes HTTP 503. Media runner service active/enabled; remote registration remains unverified.
- TCE #1032, Auth #91 and Platform #1511 exact-head checks remain PASS; positive source_run_attempt attestation is enforced for TCE, MicroFE and Auth. No production publication or dispatch was performed.
- Native schedule evidence is unchanged from issue #1497 comment #6732680029 at 05:02:47Z; current cadence is unverified. No cron/freshness changes and no TCE market-scan schedule change.
- No production promotion/apply/rollout, scale, decommission, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the only production apply authority.

Last reviewed: **2026-11-09 15:15 ICT / 2026-11-09 08:15 UTC**

This rolling tracker distinguishes native schedule events from manual, push, workflow_run and repository_dispatch fallbacks. Timestamped evidence is archived under `docs/cross-repo-deployment-checkpoints/`.

## Publisher run-attempt provenance — 2026-11-09 15:15 ICT / 08:15 UTC

- TCE PR #1032 squash-merged at 65af89f69ffe0d844a9b63e2434bc3f8cedfebb7 from exact head d9b5dc6995555f62c2b368e68d054666edfbfd38. Exact-head WF-01P #42585765728, WF-02 #42585765734, WF-05 #42585765722 and WF-08B #42585765835 all PASS.
- Authentication PR #91 squash-merged at b71834758d278e50e6ce07b5086fe45e9d9b3350 from exact head 00ce65bb68d06570f49643e8d788c1eb9d407d99. Exact-head auth-service-ci #42585818369 PASS.
- Platform PR #1511 squash-merged at 3d9063a8a233092e312bd1acc1100017e89147f4 from exact head ab8d7daa5cef14fb58d42b5a10e09fd38d47fc06. Exact-head validate-github-actions #42587040047 PASS and validate-manifests #42587039974 PASS. Earlier exact-head attempts exposed corrected workflow-contract assertions and one corrected MicroFE invalid-input fixture; only the final exact-head checks are acceptance evidence.
- Current masters: Platform 3d9063a8; TCE 65af89f6; StockDividend 1a18cabf; Media Generation dcd69869; Authentication b7183475.
- Active app publishers now include positive source_run_attempt: TCE WF-03 and WF-08B use GITHUB_RUN_ATTEMPT; Auth release uses github.run_attempt. Platform compares the payload value with run_attempt from the public Actions run API before accepting TCE, MicroFE or Auth promotion. Missing, malformed, non-positive or mismatched attempts fail closed. Regression tests cover missing and mismatched attempts.
- TCE, Auth and Platform PR checks were verified on the exact heads above. The connected run/status view does not expose post-merge push/schedule/dispatch runs for the new master commits; post-merge CI is therefore not claimed.
- Open human-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. TCE, StockDividend and Media Generation have no open PRs.

No production release dispatch, GHCR publication, GitOps digest promotion, manifest apply, rollout, scale, namespace deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.

## Post-merge and fresh-inspection delta — 2026-11-09 14:12 ICT / 07:12 UTC

- Platform PR [#1507](https://github.com/phanthienquoc/platform-infra/pull/1507) squash-merged at `a619815db94db2a407f9abf8d9e19595bcdc1146` from exact head `e65dbb62b541870aff3704dcabf0faa6913f923d`.
- Exact-head `validate-github-actions` [#42577373795](https://github.com/phanthienquoc/platform-infra/actions/runs/42577373795) PASS. The lint job completed actionlint, yamllint, shellcheck, ops regression tests, immutable image-change contract tests and workflow-contract checks.
- Exact-head `validate-manifests` [#42577373702](https://github.com/phanthienquoc/platform-infra/actions/runs/42577373702) PASS. Merge was performed after verifying the exact head and both required checks.
- Current Platform master is `1433711b25926d528f16df4f727a8e0929ea354c`, inspection snapshot PR #1508. PR #1507 post-merge push CI is not exposed by the connected run/status view and remains unverified.
- New read-only snapshot `debug/vps-latest.md` generated `2026-11-09T07:10:37Z` (14:10:37 ICT): node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin 0/1 and desired Backend pod ImagePullBackOff because GHCR has no matching platform manifest; legacy Stock Backend/Frontend 1/1 but without RepoDigest; TCE/Auth/Keycloak 0/0; both OIDC realm probes HTTP 503.
- In-cluster Stock/Media preflight remains storage-clean (no target PVC/PV claims or VolumeSnapshot references), but both namespaces remain Active and contain namespaced Secrets/TLS credentials, Services, Ingresses, Deployments and many ReplicaSets. Deleting namespaces removes those resources. External backup/retention, credential rotation/ownership, authoritative DNS and Media runner retirement remain blockers.
- Media runner service remains active/enabled with Listener present; remote registration is not inferred. Preserve the shared Platform runner. Host still reports `restart_required=yes`; no upgrade/reboot or cleanup.

No decommission dispatch, production image publication/promotion, manifest apply, scaling, namespace deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.



# Cross-repository deployment checkpoint — 2026-11-09 14:00 ICT / 07:00 UTC

## Repository state and open pull requests

Heads observed before this PR:
- Platform Infra: `1a9c9b9b1c3cb550f9904f65a50ed87df0c157cb` (inspection snapshot PR #1506 merged after PR #1505).
- TCE Dashboard: `ddf5811a7994aab08236028cff04e0a78ffd2e3e`.
- StockDividend: `1a18cabf32c6cc5f85f4157b5142a6d9d0d9d9b5`.
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`.
- Authentication: `047abc08e123d8bde7678104899d00aa8782624a`.

Open human-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. TCE, StockDividend and Media Generation have no open PRs. No draft was merged.

## Workflow/check evidence re-read

- Platform PR #1505 exact-head validation [#42570696070](https://github.com/phanthienquoc/platform-infra/actions/runs/42570696070) completed successfully (validate job success; failure-report job skipped). Platform PR #1504 post-merge validation [#42565271145](https://github.com/phanthienquoc/platform-infra/actions/runs/42565271145) completed successfully. The current-master PR-only workflow/status connectors return no entries for merge commits; that is not evidence that no push/schedule/dispatch runs exist. The inspection snapshot was committed by PR #1506, but its run ID/check suite was not independently exposed in this read.
- TCE unit test run [#42538802541](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42538802541) passed. Native WF-06 [#42548397383](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42548397383) still has four strict public health failures: Auth readiness/liveness and TCE API/web. Re-read job logs show Auth readiness and TCE API returned HTTP 503 where HTTP 200 is required.
- Stock CI [#42533562194](https://github.com/phanthienquoc/stockdividend/actions/runs/42533562194) passed all seven jobs, including ARM64 build with publication disabled. Scraper run [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) failed closed on an empty `VNSTOCK_API_KEY`, but it checked out older commit `e6469ac`; current master secret state is not established.
- Media application test/build [#42539512417](https://github.com/phanthienquoc/media-generation/actions/runs/42539512417) passed.
- Authentication ARM64 non-publishing build and validation [#42539350154](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42539350154) passed.
- No latest all-event Actions run enumeration was available. Native schedule acceptance remains unverified beyond the 05:02:47Z evidence recorded in issue #1497; preserve cron expressions and all freshness budgets.

## Fresh K3s inspection — PR #1506 snapshot

Source: `debug/vps-latest.md`, generated `2026-11-09T06:16:06Z`, master inspection commit `1a9c9b9b1c3cb550f9904f65a50ed87df0c157cb`.

- Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% (~21 GiB free), available RAM ~19 GiB, uptime 191d16h; `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with RepoDigest evidence.
- Stock Admin 0/1 (two ImagePullBackOff pods on `12d63b4`); newer Backend pod ImagePullBackOff on the same tag; legacy Backend and Frontend 1/1 on `23b2878`. The legacy cached Stock images have no RepoDigest and cannot be promoted.
- TCE frontend/service, Auth and Keycloak remain intentional 0/0. Both public OIDC realm probes returned HTTP 503.
- In-cluster Stock/Media preflight is storage-clean: no target PVC/PV claims or VolumeSnapshot references. Namespace inventory still includes namespace-scoped Secrets/TLS credentials and many workloads/ReplicaSets; deletion removes them. External backup/retention, credential ownership/rotation and authoritative DNS review remain outstanding.
- Stock and Media Ingress hostnames remain. Dedicated Media runner is active/enabled with Listener present; remote registration is not inferred. Preserve the shared Platform runner.
- Host has pending package updates and `restart_required=yes`; no cleanup, package upgrade or reboot.

## Concrete contract hardening in this PR

A review found a defense-in-depth gap: the protected workflow checked the Media runner retirement attestation and remote GitHub runner absence, but the final delete script and root-owned wrapper consumed only three of the four operator confirmations. The PR propagates and validates the fourth `RUNNER_RETIREMENT` value in the final workflow step, namespace script and root-owned `platform-kubectl` wrapper, and adds negative tests for missing/mismatched runner attestations. The workflow's remote read-only runner API check remains mandatory; the typed token is not treated as cryptographic proof.

## Current blockers and exact next actions

1. GitHub administrator: provide all-event schedule enqueue/delivery evidence for issue #1497; no cron/freshness budget changes.
2. Platform operator: obtain/retain a fresh read-only inspection before any rollout/decommission/maintenance decision.
3. Stock owner: verify current `VNSTOCK_API_KEY`, run safe preflight on master, then approve full-source-SHA ARM64 publication and registry digest capture.
4. TCE/Auth owners: investigate HTTP 503 and approve recovery/rollback before any replica restoration or digest-promotion activation.
5. Media owner/operator: idle/stop/disable/unregister the dedicated runner; verify absence via the read-only audit token; review external backup/retention and authoritative DNS/provider records.
6. Platform operator: host package/reboot maintenance only in an approved window with rollback and retention evidence.

No production publication, promotion, manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.



# Cross-repo deployment checkpoint — 2026-11-09 13:00 ICT

## Repository state and pull requests

Default-branch heads re-read at 2026-11-09 13:00 ICT / 06:00 UTC:

| Repository | Master SHA | Open PRs |
|---|---|---|
| phanthienquoc/platform-infra | `3ecb4fd12de5105ebd3214ee4bf15c8e68f1b751` | #1314, #544, #541, #539 (draft/human decisions) |
| phanthienquoc/TCE-dashboard | `ddf5811a7994aab08236028cff04e0a78ffd2e3e` | None |
| phanthienquoc/stockdividend | `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5` | None |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | None |
| phanthienquoc/phanthienquoc-authentication | `047abc08e123d8bde7678104899d00aa8782624a` | #76 (draft; migration integration side effect not yet verified) |

Platform PR #1504 merged at 2026-11-09T05:05:18Z as master commit `3ecb4fd12de5105ebd3214ee4bf15c8e68f1b751`. Its exact-head `validate-manifests` run #42565213174 completed successfully. Post-merge run #42565271145 also completed successfully; its validate job rendered 78 Kubernetes objects and passed manifest, Auth GitOps, immutable image, secret, Keycloak and network-boundary checks.

## Latest verified workflow-job evidence

| Repository | Run | Job evidence |
|---|---|---|
| Platform Infra | [#42565213174](https://github.com/phanthienquoc/platform-infra/actions/runs/42565213174) | Exact-head validation PASS |
| Platform Infra | [#42565271145](https://github.com/phanthienquoc/platform-infra/actions/runs/42565271145) | Post-merge validation PASS |
| TCE Dashboard | [#42538802541](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42538802541) | Backend unit tests PASS |
| TCE Dashboard | [#42548397383](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42548397383) | Native WF-06: Auth readiness, Auth liveness, TCE API and TCE web jobs all FAIL; readiness log explicitly reports HTTP 503 versus expected 200 |
| StockDividend | [#42533562194](https://github.com/phanthienquoc/stockdividend/actions/runs/42533562194) | All 7 CI jobs PASS, including ARM64 build with publication disabled |
| StockDividend | [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) | Scraper fails closed because `VNSTOCK_API_KEY` was empty; log checked out older commit `e6469ac`, not current master `1a18cabf`, so current secret state is unverified |
| Media Generation | [#42539512417](https://github.com/phanthienquoc/media-generation/actions/runs/42539512417) | Application test/build PASS |
| Authentication | [#42539350154](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42539350154) | ARM64 non-publishing build and validation PASS |

The connected commit-run wrapper only returns pull-request-triggered runs; querying current master SHAs returned no runs, and combined commit-status queries returned no status entries. Therefore the run IDs above are the latest job evidence independently re-queried in this execution, not proof that no newer push/schedule/dispatch runs exist. Do not infer absence of newer runs from the empty PR-only response.

## Native schedule delivery

The latest complete native-event enumeration available in issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) is the 2026-11-09 05:02:47Z snapshot. At that time all six Platform/TCE native inter-arrival gaps exceeded their existing budgets. No newer all-event Actions run listing or authoritative scheduler enqueue evidence was available in this execution; current cadence therefore remains unverified, not newly measured. Keep issue #1497 open for the GitHub Actions administrator. Preserve every cron expression and freshness budget; do not count manual, push, workflow_run or repository_dispatch events as native acceptance.

TCE WF-06 #42548397383 remains a confirmed service-health failure distinct from schedule delivery: all four strict public probes failed, with the Auth readiness job explicitly returning HTTP 503. TCE/Auth/Keycloak 0/0 maintenance is not live health. Do not weaken HTTP 200 checks or restore replicas without service-owner approval and rollback.

## K3s and GitOps freshness

The current tracked `debug/vps-latest.md` is still generated at `2026-11-09T01:54:48Z` (inspection #42548015626). At this checkpoint it is more than four hours old and is stale for rollout, decommission, host maintenance or deletion authorization. The connected GitHub actions do not expose a workflow-dispatch operation, so no fresh read-only inspection was triggered here. Obtain a new `inspect-vps` run before any runtime decision.

Last known snapshot only:
- K3s node Ready/ARM64; disk 56% (~21 GiB free), available RAM ~19 GiB, host restart required.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1 with digest evidence.
- Stock desired Admin/Backend tags `12d63b4` had ARM64 image-pull failures; legacy cached image evidence is not a RepoDigest promotion proof.
- TCE/Auth/Keycloak were intentional 0/0.
- Dedicated Media runner service was active/enabled with listener present; remote registration, external backup/retention and authoritative DNS ownership remain unverified.

Last known reconciliation is workflow_dispatch #42546651537, not a native scheduled run: Auth runtime Secret was provisioned and verified, shared `ghcr-pull` unchanged, drift false, and manifest apply, image promotion and rollout skipped. This is not fresh reconciliation or live health evidence.

## Ownership and next actions

1. **GitHub Actions administrator:** provide authoritative schedule enqueue/delivery evidence for issue #1497 and restore consecutive native events within existing budgets.
2. **Platform operator:** trigger a fresh read-only `inspect-vps` through the authorized GitHub Actions UI/API and archive the result before rollout/decommission/maintenance.
3. **Stock owner:** verify current `VNSTOCK_API_KEY` secret state, run the side-effect-free credential preflight on current master, then approve full-source-SHA ARM64 publication and capture Admin/Backend/Scraper registry digests. Do not promote `12d63b4` or cached `23b2878`.
4. **TCE/Auth owners:** investigate HTTP 503 and 0/0 maintenance; approve recovery/rollback, publish app-owned images, merge digest-pinned Platform promotion PRs, then verify health before scaling.
5. **Media owner/operator:** verify external backup/retention, authoritative DNS and remote runner registration; retire only the dedicated Media runner after idle-state and approval checks. Preserve the shared Platform runner.
6. **Platform operator:** schedule host package/reboot maintenance only with a maintenance window, rollback and retention evidence.

App repositories continue to own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials/runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout and health verification. Workflow-level pre-push tag guards are not GHCR server-side immutability; registry digest and ARM64 verification remain mandatory.

No production image publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred in this checkpoint. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority was added. TCE market-scan schedule unchanged.


## Previous checkpoint — 2026-11-09 08:59 ICT / 01:59 UTC (reconciliation evidence corrected in the 09:05 checkpoint below)

### Repository state, open PRs and latest checks

- **Platform Infra:** master `e5288041c509669b84ef7405af48e7036020c61a`. Read-only inspection #42548015626 succeeded and generated `debug/vps-latest.md` at 01:54:48Z; automated inspection PR [#1496](https://github.com/phanthienquoc/platform-infra/pull/1496) merged at this master SHA after its inspection/validation steps passed. Latest workflow_dispatch reconcile #42546651537 PASS with `mode=apply`, `target_app=all`, `allow_image_changes=false`; Auth runtime Secret provisioned/verified, `ghcr-pull` unchanged, no drift, apply/promotion/rollout skipped. Latest native scheduled reconcile remains #42538596496. Native watchdog #42537967026 failed cadence acceptance; workflow_run watchdog #42548211945 also failed.
- **TCE Dashboard:** master `ddf5811a7994aab08236028cff04e0a78ffd2e3e`; no open PR. Core WF-01 #42538802539, WF-02 #42538802538 and WF-05 #42538802541 PASS. Latest native WF-06 #42548397383 failed all four strict public checks with HTTP 503. Manual WF-06 #42546655501 also failed 4/4. Native WF-12 #42546629459 failed because the previous WF-06 run was 10,647s old; measured queue wait was 0m.
- **StockDividend:** master `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5`; no open PR. CI #42533562194 passed all seven jobs, including native ARM64 builds with publishing disabled. Weekend scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is empty. No production publication or digest handoff is evidenced.
- **Media Generation:** master `dcd698699c65ba6e73f6b43838975144777131c3`; no open PR. CI #42539512417 PASS. The latest K3s snapshot still shows backend/frontend 1/1 with RepoDigest evidence; the dedicated Media runner remains active/enabled with Runner.Listener present.
- **Authentication:** master `047abc08e123d8bde7678104899d00aa8782624a`; PR #76 remains draft. CI #42539350154 PASS. Auth/Keycloak remain intentional 0/0 maintenance; a verified runtime Secret does not establish live health.
- **Open human-decision drafts:** Platform #1314, #544, #541 and #539; Authentication #76. TCE, StockDividend and Media Generation have no open PRs. No draft was merged or promoted.

### Native schedule acceptance — still outside existing budgets

Only original `event=schedule`, master, attempt 1 runs with the exact workflow path count. Manual, push, workflow_run and repository_dispatch events do not count.

| Workflow | Latest native run | Previous native run | Gap | Existing budget |
|---|---|---|---:|---:|
| Platform reconcile | #42538596496 PASS, 00:08:54Z | #42521088881, 20:37:39Z | 12,675s | 2,700s |
| Platform inspection | #42548015626 PASS, 01:54:40Z | #42530192980, 22:25:47Z | 12,533s | 4,500s |
| Platform recovery | #42537793367 PASS, 23:59:38Z | #42520213983, 20:27:31Z | 12,727s | 2,700s |
| Platform watchdog | #42537967026 FAIL, 00:01:36Z | #42520452305, 20:30:24Z | 12,672s | 2,700s |
| TCE WF-06 | #42548397383 FAIL, 01:59:09Z | #42531446260, 22:41:01Z | 11,888s | 1,500s |
| TCE WF-12 | #42546629459 FAIL, 01:38:28Z | #42527713763, 21:56:51Z | 13,297s | 1,500s |

Platform watchdog #42548211945 failed native inter-arrival checks. The latest inspection proves the inspection workflow can execute, but not that its cadence has recovered. WF-12 #42546629459 measured 0m runner queue wait and found WF-06 age 10,647s (177m27s). Runner saturation is not established as the cause.

GitHub issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) now tracks the external schedule-delivery investigation with exact run IDs, gaps, budgets and acceptance criteria. Preserve all cron expressions and freshness budgets; do not use fallback events as native acceptance.

### Latest read-only K3s snapshot — 2026-11-09 01:54:48Z

Source: [inspection #42548015626](https://github.com/phanthienquoc/platform-infra/actions/runs/42548015626), committed by inspection PR #1496 as `debug/vps-latest.md`.

- Node `tce-k3s-01` is Ready, ARM64, K3s v1.36.3+k3s1, K3s containerd 2.3.2-k3s2. Host has 4 CPUs, 19 GiB available RAM, 56% disk usage (~21 GiB free), and 191 days uptime.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running. Media and MicroFE images have RepoDigest evidence.
- Stock Admin has two non-ready pods (one ErrImagePull, one ImagePullBackOff); desired Stock Backend is ImagePullBackOff. Kubelet reports no matching platform manifest for `stockdividend/admin:12d63b4` and `stockdividend/backend:12d63b4`. Legacy Backend/Frontend are 1/1, but cached `23b2878` images lack RepoDigest and are not promotion evidence.
- TCE frontend/service, Auth service and Keycloak remain 0/0. This is intentional maintenance, not live health.
- Stock/Media namespace storage preflight shows no Stock/Media PVC/PV claims or VolumeSnapshot references; only the unrelated `k3s-debug` PVC/PV appears. External backup/retention and authoritative DNS ownership remain unverified.
- Platform and Media runner services are active/enabled and both Runner.Listener processes are present. Media runner remote registration has not been audited.
- Host reports `restart_required=yes`; Docker 29.1.3 has 5.773 GB reclaimable, host containerd.io 2.2.1 has 2.4.2-3 available. No cleanup, package upgrade, reboot or maintenance was performed.

### Latest reconciliation and safety boundary

Latest confirmed reconciliation is workflow_dispatch #42546651537 (01:38:43Z; `mode=apply`, `target_app=all`, `allow_image_changes=false`). GHCR read access passed for Auth/MicroFE/TCE; Auth runtime Secret was provisioned and verified; shared `ghcr-pull` was unchanged; no manifest drift was detected; manifest apply and image promotion were skipped. MicroFE health passed; TCE/Auth lanes recognized intentional 0/0 maintenance without asserting live health; rollouts and Keycloak lane were skipped. Recovery #42546778524 passed. Later heartbeat recovery #42548422877 passed and correctly avoided duplicate fallback because reconciliation #42546651537 was 19m old and inspection #42548015626 was 4m old. Latest native scheduled reconciliation remains #42538596496.

App repositories own tests/builds and immutable GHCR publication; Platform alone owns production manifests, shared pull credentials, runtime Secrets, digest/provenance validation, GitOps promotion/reconciliation, rollout and health verification. No production image was published/promoted, no manifest was applied, no workload was scaled, and no Stock/Media namespace or runner was deleted.

### Exact next actions

1. **GitHub Actions administrator:** investigate issue #1497; provide authoritative schedule enqueue/delivery evidence and restore consecutive native runs within existing budgets.
2. **Stock owner:** provision `VNSTOCK_API_KEY`; run the side-effect-free scraper preflight; then approve and execute the ARM64 publisher, capturing all Admin/Backend/Scraper registry digests. Do not promote `12d63b4` or cached `23b2878` images.
3. **TCE/Auth service owners:** investigate the four HTTP 503 paths while TCE/Auth/Keycloak remain 0/0. Keep strict HTTP 200 health checks; any replica restoration requires approval and rollback plan.
4. **Media owner:** provide least-privilege runner audit credentials, verify remote registration, external backup/retention and authoritative DNS before runner retirement or decommission.
5. **Platform operator:** plan host maintenance only with a window, rollback and retention evidence.

Do not alter TCE market-scan scheduling. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No duplicate direct SSH/Compose deployment authority.

## Latest execution — 2026-11-09 09:05 ICT / 02:05 UTC

### PR #1498 — merged and validated

[PR #1498](https://github.com/phanthienquoc/platform-infra/pull/1498) was squash-merged at 02:04:40Z as `346ecfed57fdd1179abda8c114574d9e3dd575a3` from exact head `320e13d04c6317c645cceb1caa0c82d92ccebe27`. Exact-head `validate-manifests` #42548807576 PASS; post-merge `validate-manifests` #42548906576 PASS. It refreshes the cross-repo tracker, workflow inventory and 08:59 checkpoint. Issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497) tracks native schedule-delivery investigation.

### Latest reconciliation and recovery — distinguish native from fallback

- Latest completed reconciliation is **workflow_dispatch #42546651537** (01:38:43Z, source master `3ea55b827c85c2e2e815fecaa067a99edc0ed043`), not the older native schedule run. Exact inputs: `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- Reconcile job succeeded: GHCR read access verified for Auth/MicroFE/TCE; Auth runtime Secret was provisioned and verified (values suppressed); shared `ghcr-pull` was unchanged; scoped image-pull recovery step completed; no manifest drift was detected; production manifest apply and image promotion were skipped.
- MicroFE health verification passed. TCE and Auth lanes passed by explicitly recognizing intentional 0/0 maintenance; they do not assert live health. TCE/Auth rollout steps and Keycloak lane were skipped. Final deployment gate passed.
- Post-reconciliation recovery controller #42546778524 succeeded.
- Later TCE heartbeat recovery [#42548422877](https://github.com/phanthienquoc/platform-infra/actions/runs/42548422877) succeeded for source WF-06 #42548397383. It found reconciliation #42546651537 only 19m old and inspection #42548015626 only 4m old, so it correctly avoided duplicate reconciliation/inspection dispatch. This fallback success is not native schedule acceptance.
- Latest native scheduled reconciliation remains #42538596496 PASS at 00:08:54Z; do not conflate it with workflow_dispatch #42546651537.

### Current schedule, service and runtime blockers

All six native inter-arrival gaps remain outside existing budgets: Platform reconcile 12,675s/2,700s; inspection 12,533s/4,500s; recovery 12,727s/2,700s; watchdog 12,672s/2,700s; TCE WF-06 11,888s/1,500s; TCE WF-12 13,297s/1,500s. Latest TCE WF-06 #42548397383 ran but all four strict endpoints returned HTTP 503. WF-12 #42546629459 found WF-06 age 10,647s with 0m queue wait. Preserve cron and freshness budgets.

Latest K3s inspection remains #42548015626 (snapshot generated 01:54:48Z): node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin×2 and desired Backend not ready because desired `12d63b4` tags have no matching ARM64 manifest; cached Stock `23b2878` images lack RepoDigest; TCE/Auth/Keycloak remain intentional 0/0. Media/Platform runners active/enabled; external backup/retention, DNS ownership and Media runner remote registration remain unverified. Host `restart_required=yes`; no cleanup/upgrade/reboot.

Stock CI #42533562194 passed all seven jobs with ARM64 builds set to push=false; scraper #42457182511 failed closed on empty `VNSTOCK_API_KEY`. Media CI #42539512417 and Auth CI #42539350154 PASS. Open human-decision drafts remain Platform #1314/#544/#541/#539 and Auth #76.

Safety: no production image publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. The only confirmed production mutation in the latest reconciliation was Auth runtime Secret provisioning; shared `ghcr-pull` was unchanged. `reconcile-vps.yml` remains the sole apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

## Repository readiness

| Repository | Master SHA | Open PRs | Readiness evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `346ecfed57fdd1179abda8c114574d9e3dd575a3` | #1314/#544/#541/#539 (draft planning/docs) | PR #1498 merged at `346ecfed`; exact-head #42548807576 and post-merge #42548906576 PASS. Latest workflow_dispatch reconciliation #42546651537 PASS: Auth runtime Secret provisioned/verified, shared `ghcr-pull` unchanged, no drift, apply/promotion/rollout skipped. Native schedule gaps remain outside budget; issue #1497 tracks investigation. |
| phanthienquoc/TCE-dashboard | `ddf5811a7994aab08236028cff04e0a78ffd2e3e` | None | Core CI WF-01 #42538802539, WF-02 #42538802538 and WF-05 #42538802541 PASS. Native WF-06 #42548397383 fails 4/4 HTTP 503; WF-12 #42546629459 fails stale-WF-06 delivery with 0m queue wait. TCE/Auth remain 0/0; market-scan schedule unchanged. |
| phanthienquoc/stockdividend | `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5` | None | CI #42533562194 all 7 jobs PASS, including non-publishing ARM64 builds. Scraper #42457182511 fails closed on empty `VNSTOCK_API_KEY`. No production publication/digest handoff; K3s desired `12d63b4` lacks ARM64 manifest and cached `23b2878` images lack RepoDigest. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | None | CI #42539512417 PASS. Latest inspection #42548015626 shows backend/frontend 1/1 with RepoDigest; dedicated Media runner remains active/enabled/listener-present. Protected decommission remains blocked by runner, backup/retention and DNS evidence. |
| phanthienquoc/phanthienquoc-authentication | `047abc08e123d8bde7678104899d00aa8782624a` | #76 (draft) | CI #42539350154 PASS. Auth/Keycloak remain intentional 0/0; runtime Secret verified by last reconcile but no live health or activation is asserted. |

## Previous checkpoint — 2026-11-09 08:31 ICT / 01:31 UTC (superseded by the 08:59 checkpoint above)

### GitOps promotion provenance and digest binding

Platform PR [#1493](https://github.com/phanthienquoc/platform-infra/pull/1493) was squash-merged at `891a07c06bc541f2df420d6d085d77f49121602d` from exact head `e97e9a536bf7390a03ff2c2269e49f9e63708500`.

- Exact-head checks: `validate-github-actions` #42545953263, `validate-manifests` #42545953756 and `keycloak-ci` #42545953254 all PASS.
- Post-merge checks: #42546040759, #42546040835 and #42546040757 all PASS.
- The reconcile gate fetches the exact originating promotion run and its Actions jobs (`actions/runs/{run_id}/jobs?per_page=100`). It rejects malformed/truncated job evidence unless API `total_count` equals the returned job count.
- It requires the app-specific completed-successful jobs: MicroFE digest promotion; both TCE paired promotion and release coordinator; or Auth promotion. A successful no-op workflow envelope is insufficient.
- It resolves the expected current GitOps image set (Auth 1, TCE 2, MicroFE 2), requires exactly one valid digest-pinned entry per image, verifies the immutable source tag against the exact manifest digest, then re-verifies the digest reference for `linux/arm64`.
- These read-only checks run before Auth runtime Secret provisioning or shared `ghcr-pull` mutation. Helpers remain excluded from recovery push bootstrap.

No production ready-event was replayed or dispatched by this change. No image was published/promoted, no manifest was applied and no workload was rolled out.

### Native schedule acceptance — still outside budget

Latest original `event=schedule` runs returned by GitHub Actions API:

| Workflow | Latest native run | Previous native run | Inter-arrival gap | Existing budget |
|---|---|---|---:|---:|
| Platform reconcile | #42538596496 PASS, 00:08:54Z | #42521088881, 20:37:39Z | 12,675s | 2,700s |
| Platform inspection | #42530192980 PASS, 22:25:47Z | #42510125328, 18:27:47Z | 14,280s | 4,500s |
| Platform recovery | #42537793367 PASS, 23:59:38Z | #42520213983, 20:27:31Z | 12,727s | 2,700s |
| Platform watchdog | #42537967026 FAIL, 00:01:36Z | #42520452305, 20:30:24Z | 12,672s | 2,700s |
| TCE WF-06 | #42531446260 FAIL, 22:41:01Z | #42512468931, 18:56:20Z | 13,481s | 1,500s |
| TCE WF-12 | #42527713763 FAIL, 21:56:51Z | #42507582654, 17:58:14Z | 14,317s | 1,500s |

No newer native schedule events appeared in this inspection. TCE WF-06 logs report HTTP 503 from four public health endpoints; WF-12's heartbeat succeeded but native WF-06 freshness failed. Platform inspection queue telemetry previously reported 0m, so runner queue saturation is not established as the cause. Manual, push, workflow_run and repository_dispatch events do not count as native acceptance. Preserve every cron and freshness budget; GitHub administrator investigation remains required.

### Runtime and production boundary

- Latest reconciliation #42538596496 PASS: GHCR read access PASS; Auth runtime Secret verified; shared `ghcr-pull` unchanged; `drift=false`; manifest apply, image promotion and rollout skipped.
- Latest committed K3s snapshot remains inspection #42530192980, generated 22:25:55Z. It is stale at this review and must not be described as current health. It last showed node Ready/ARM64, Media/MicroFE 1/1, Stock Admin×2 and desired Backend ImagePullBackOff on missing ARM64 manifest, and TCE/Auth/Keycloak intentional 0/0.
- Stock scraper remains blocked by missing `VNSTOCK_API_KEY`; no ARM64 publication or digest handoff is evidenced.
- Media runner remains active/enabled/listener-present. Remote runner registration, external backup/retention and authoritative DNS ownership are still unverified; protected decommission remains blocked.
- Open human-decision drafts remain Platform #1314/#544/#541/#539 and Auth #76. TCE, Stock and Media have no open PRs.

`reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority, cron/freshness change, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

## Current actions

1. **GitHub Actions administrator:** investigate native schedule delivery for Platform reconcile/inspection/watchdog/recovery and TCE WF-06/WF-12. Preserve cron expressions and freshness budgets; do not count manual, push, workflow_run or repository_dispatch fallbacks as native acceptance.
2. **Stock owner:** provision `VNSTOCK_API_KEY`, run the side-effect-free `preflight_only=true` scraper check, prove authenticated non-guest entitlement, then run the ARM64 publisher and capture Admin/Backend/Scraper registry digests. Do not promote the cached `23b2878` tags or broken `12d63b4` tags.
3. **Platform/Stock:** use the new inspection warning for GHCR cache tags without RepoDigest; require publisher-run provenance plus registry digest and ARM64 manifest evidence before any promotion.
4. **TCE/Auth service owners:** investigate four public HTTP 503 paths and Keycloak OIDC 503 while TCE/Auth/Keycloak remain intentional 0/0. Any replica restoration needs explicit approval and rollback plan.
5. **Media owner:** provision the least-privilege `MEDIA_RUNNER_AUDIT_TOKEN`, then separately stop/disable and unregister the runner; provide external backup/retention and authoritative DNS/provider evidence before decommission.
6. **Auth/Supabase owner:** continue PR #76 schema-drift and merge-trigger side-effect investigation; keep it draft until evidence is complete.
7. **Platform operator:** schedule Docker/containerd/OS maintenance only with a maintenance window, rollback and retention evidence; no cleanup, upgrade or reboot in this checkpoint.

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


## Latest cross-repo execution — 2026-11-08 21:07 ICT / 14:07 UTC

### Repository state, PRs and latest workflow evidence

All five default branches, open PRs, recent Actions runs, this tracker and the workflow inventory were inspected before changes.

| Repository | Default-branch head | Open PRs | Latest relevant CI/workflow evidence |
|---|---|---|---|
| Platform Infra | `4031089f19a0dfbbea7d73196ac6fd771aaa0b39` | #1314, #544, #541, #539 (planning/docs) | post-merge `validate-manifests` #42484497462 PASS; latest recovery #42484949353 PASS; latest workflow_run diagnostics #42484968404/#42484972617 skipped |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | none | WF-07 native schedule #42484929411 PASS; WF-12 workflow_run #42484941935 FAIL on stale WF-06; fallback WF-06 #42484965082 FAIL (four public endpoints HTTP 503) |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | none | CI #42440810105 PASS; scheduled scraper #42457182511 FAIL closed because `VNSTOCK_API_KEY` is missing |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | none | CI #42239703151 PASS; no newer publisher or deployment run |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 (draft) | master CI #42478653766 PASS; PR #76 remains draft pending Supabase merge-trigger side-effect/schema-drift investigation |

### Native schedule acceptance — still failing

| Platform workflow | Latest native run | Previous native run | Inter-arrival gap | Budget | Result |
|---|---:|---:|---:|---:|---|
| reconcile-vps | #42467231073, 09:27:03Z, FAIL | #42439099803 | 24,773s | 2,700s | FAIL |
| inspect-vps | #42483869620, 13:12:46Z, PASS | #42452273701 | 26,586s | 4,500s | cadence FAIL; snapshot currently within 75m age budget |
| recover-stale-ops | #42466737776, 09:20:06Z, PASS | #42438384072 | 24,958s | 2,700s | FAIL |
| reconcile-schedule-watchdog | #42467080859, 09:24:53Z, FAIL | #42438566387 | 25,092s | 2,700s | FAIL |

The latest workflow_run watchdog #42484055575 also failed for these measured native inter-arrival gaps. Its TCE WF-06/WF-12 observations are warning-only and do not turn a manual or workflow_run event into native schedule evidence. Do not relax cron or freshness budgets to obtain a green result.

### TCE heartbeat and Platform recovery — live payload accepted

- TCE WF-07 native schedule #42484929411 completed PASS at 13:25:55Z.
- TCE WF-12 workflow_run #42484941935 completed FAIL at 13:26:05Z because the latest native WF-06 run remained #42458256899 (07:18:37Z), age 367m against the 25m budget. The latest native WF-12 run remains #42479336350 (12:15:00Z), also outside its 25m budget.
- WF-13 #42484952892 completed PASS and the read-only WF-06 fallback #42484965082 was dispatched; the four public probes (TCE web, TCE API, Auth liveness, Auth readiness) each returned HTTP 503.
- Platform repository_dispatch recovery #42484949353 completed PASS. Its log verifies source repository `phanthienquoc/TCE-dashboard`, source workflow `.github/workflows/wf-07-tce-integration-check.yml`, source run #42484929411, attempt 1, source SHA `7ab52078c4250829e158f05b2695ceb9d11bdbe3`, and heartbeat run #42484941935. It observed the recent fallback reconciliation #42484067445 (last activity 13:16:58Z, age 9m) and native inspection #42483869620 (age 13m), so correctly dispatched no duplicate fallbacks.
- This is evidence that the TCE-to-Platform repository_dispatch payload and recovery receiver worked. It is not evidence that native Platform/TCE cadence or public service health has recovered.

### Latest reconciliation and K3s snapshot

- Platform fallback reconciliation #42484067445 completed PASS at 13:15:18Z with `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR access preflight and Auth runtime Secret provisioning/verification passed; no manifest drift was found, so production manifest apply and image promotion were skipped. MicroFE/TCE/Auth lane gates passed with rollouts skipped for unchanged/zero-replica state; Keycloak lane was skipped.
- Native read-only inspection #42483869620 generated `debug/vps-latest.md` at 13:12:54Z. At this checkpoint it is approximately 54m old, within the 75m snapshot-age budget. Node `tce-k3s-01` is Ready/ARM64, K3s `v1.36.3+k3s1`, runtime `containerd://2.3.2-k3s2`; disk 56% with 21 GiB available and RAM 19 GiB available. Docker 29.1.3 reports 20 images / 9.195 GB with 5.773 GB reclaimable; no cleanup was run.
- Media backend/frontend and MicroFE Shell/WS/NATS remain 1/1 in the snapshot. Stock Admin (two pods) and desired Backend remain ImagePullBackOff on legacy `12d63b4`; legacy Stock Backend and Frontend remain 1/1. TCE/Auth/Keycloak remain intentional zero-replica maintenance. Public OIDC probes return HTTP 503.
- Media and Platform runner services/listeners remain active. Stock/Media in-cluster storage preflight is clean, but external backup/retention and authoritative DNS ownership remain unverified. GitOps drift is clean. Host updates/restart requirements are not authorized for this run.

### Publisher and credential dependencies

- Stock `deploy.yml` statically verifies native ARM64 build execution, `linux/arm64` for Scraper/Admin/Backend, full-40-character source-SHA tags, version+full-SHA tags, and equality of each immutable tag pair's registry digest. No new Stock publisher run or GHCR digest evidence exists; do not update Platform image references or promote.
- Stock scheduled scraper #42457182511 failed before dependency installation, entitlement verification and ingestion because `VNSTOCK_API_KEY` is absent. Preserve fail-closed behavior; Stock owner must provision the secret and run `preflight_only=true` before ingestion.
- Media runner audit token `MEDIA_RUNNER_AUDIT_TOKEN`, external backup/retention and authoritative DNS ownership remain unverified. Do not stop/unregister the runner or decommission namespaces.
- Auth PR #76 remains draft; no production migration, release or publisher dispatch was performed.

### Authority and safety

- App repositories continue to own tests/builds and immutable GHCR publication. Platform Infra remains sole owner of production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose production authority was added and no workflow was removed.
- No image publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host upgrade/reboot occurred.
- TCE market-scan schedule is unchanged.

### Exact next actions

1. GitHub Actions administrator: investigate native schedule delivery/large inter-arrival gaps; keep existing cron and freshness budgets unchanged.
2. Stock owner: add `VNSTOCK_API_KEY`, run `run_scraper.yml` with `preflight_only=true`, then authorize normal ingestion and an app-owned ARM64 publisher run.
3. TCE/Auth service owner: provide an approved recovery/rollback plan for the four public HTTP 503 probes before any replica or production state change.
4. Platform owner: verify `MEDIA_RUNNER_AUDIT_TOKEN`; Media/Stock owners must provide external backup/retention and DNS evidence before decommission.
5. Auth/Supabase owner: continue PR #76 schema-drift and merge-trigger side-effect investigation; keep it draft until evidence is complete.
## Latest cross-repo execution — 2026-11-08 21:57 ICT / 14:57 UTC

### Repository and pull-request state

- Platform Infra master is `ab458a525f18c1397fa52ca639e5a2abd6c9a536`. Inspection PR #1467's generated snapshot is present on master. Open Platform PRs remain #1314, #544, #541 and #539 (planning/documentation); TCE, Stock and Media have no open PRs; Authentication PR #76 remains draft/open.
- TCE master: `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock: `e6469ac6617142b349144101a1192cb6aa7104ad`; Media: `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Authentication: `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1`.
- Latest Platform commit #1467 is an automated read-only VPS inspection snapshot generated at `2026-11-08T14:28:32Z`. Its commit is on master; the GitHub connector returned no legacy combined statuses and its commit-workflow lookup is PR-event-only. Do not infer a run ID, event type or check conclusion for #1467 from the commit alone.

### New read-only inspection contract change proposed

- The latest CRI inventory contains Stock cached tags `backend:23b2878` and `user:23b2878` with empty RepoDigest fields. The image IDs are local runtime identifiers, not registry digests or promotion evidence.
- Added a read-only `GHCR image digest coverage` section to `scripts/inspect-vps.sh`. It warns when a cached GHCR-tagged image has no RepoDigest and explicitly says local image IDs cannot authorize promotion. It does not fail inspection, delete images, or change deployment state.
- Added output validation in `.github/workflows/inspect-vps.yml` and a static contract assertion in `scripts/validate-workflow-contracts.py`. This change is on the dedicated branch `docs/deployment-readiness-2026-11-08-2157-ict`; exact-head checks are pending after PR creation.

### Latest K3s snapshot — PR #1467

- Snapshot generated at 14:28:32Z; about 29 minutes old at this review, within the 75-minute snapshot-age budget. Event provenance for this snapshot was not surfaced, so it is not counted as native schedule acceptance.
- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`; disk 56% (~21 GiB free), available RAM ~19 GiB; host uptime ~191 days; `restart_required=yes`. Docker 29.1.3 has 20 images / 9.195 GB, with ~5.773 GB reclaimable. No cleanup or maintenance performed.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with digest-resolved GHCR RepoDigests.
- Stock Admin has two ImagePullBackOff pods and the desired Backend has one ImagePullBackOff pod on `12d63b4`; kubelet reports no matching platform manifest. Legacy Backend and Frontend remain 1/1 on `23b2878`. CRI inventory shows blank RepoDigest for cached Stock tags `backend:23b2878` and `user:23b2878`; no fresh Stock registry digest/publisher evidence is established.
- TCE frontend/service, Auth service and Keycloak remain 0/0. Public Keycloak OIDC probes return HTTP 503. Platform and Media runner services are active/enabled; Media Listener is present.
- Storage inventory shows only the unrelated `k3s-debug` PVC/PV; Stock/Media VolumeSnapshot references are none. External backup/retention and authoritative DNS ownership remain unverified.

### Latest known workflow evidence and limitations

- TCE WF-07 native schedule #42484929411 PASS. WF-12 heartbeat #42484941935 reached Platform recovery #42484949353 PASS; this proves the authenticated dispatch/recovery path, not WF-06 native health or schedule cadence.
- Latest recorded native TCE WF-06 #42458256899 failed four public endpoints with HTTP 503. Latest recorded native WF-12 #42479336350 detected stale WF-06. Fallback WF-06 #42479362379 also returned four HTTP 503s.
- Latest recorded Platform native reconcile #42467231073 FAIL, inspection #42452273701 PASS, watchdog #42467080859 FAIL, recovery #42466737776 PASS; all are stale against 45/75/45/45-minute budgets. Native inspection #42483869620 produced a fresh earlier snapshot, but the next snapshot commit #1467 has no surfaced event type. Do not count it as native schedule evidence.
- Stock scraper #42457182511 failed closed before dependency installation/ingestion because `VNSTOCK_API_KEY` was empty. Stock master CI #42440810105 passed 7/7 but is non-publishing. No new Stock publisher/digest handoff is verified.
- Media CI #42239703151 and Auth master CI #42478653766 are the latest recorded app CI passes; no new Media/Auth publisher run is verified. Auth PR #76 remains draft.
- The available GitHub connector can inspect repositories, PRs, commits and PR-triggered commit workflow runs, but does not expose repository-wide latest Actions run listing/check-runs in this session. Empty combined-status responses are not treated as successful checks; the exact-head PR checks for the new inspection contract must be queried after opening the PR.

### Safety and ownership

- App repositories continue to own tests/builds and immutable GHCR publication. Platform Infra remains the sole owner of production manifests, shared GHCR pull credentials, source/digest/provenance verification, GitOps promotion/reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No duplicate direct SSH/Compose production authority was added and no workflow was removed.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host upgrade/reboot occurred. TCE market-scan schedule unchanged.
## Latest execution update — 2026-11-08 22:14 ICT / 15:14 UTC

- Platform master advanced to `819215cc0c6b295f746e1a43cd6747df4fe292b8` through automated inspection PR #1469. Snapshot `debug/vps-latest.md` generated at `2026-11-08T15:10:12Z` (22:10:12 ICT); its event type and run ID were not surfaced, so it is not counted as native schedule acceptance.
- PR #1468 remains merged at `45fae050df626641ddfca3ededcff3cbf9f388b3`; exact-head `validate-github-actions` #42493255493 and `validate-manifests` #42493255334 both PASS. The read-only inspection code was exercised by the subsequent PR #1469 snapshot: `GHCR image digest coverage` emitted `status: warning` and listed `stockdividend/backend:23b2878` and `stockdividend/user:23b2878` with blank RepoDigest. This validates the new diagnostic on live inspection output; it does not prove a publisher digest.
- PR #1470 was closed unmerged as superseded when inspection PR #1469 advanced master; its docs are being refreshed from current master on this branch. Current open Platform PRs remain #1314/#544/#541/#539 (planning/docs).
- K3s: node `tce-k3s-01` Ready/ARM64; disk 56% (~21 GiB free), RAM ~19 GiB available, uptime ~191 days 1 hour, `restart_required=yes`. Media backend/frontend and MicroFE Shell/WS/NATS 1/1. Stock Admin has one `ImagePullBackOff` and one `ErrImagePull`; desired Backend remains `ImagePullBackOff` on `12d63b4`; legacy Backend/Frontend 1/1 on `23b2878`. TCE/Auth/Keycloak 0/0; public OIDC 503. Platform and Media runner services active; Media Listener present.
- Stock CRI inventory has no RepoDigest for cached `backend:23b2878`/`user:23b2878`; these are not promotion evidence. Scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; no new publisher run or immutable digest handoff is verified.
- TCE WF-07 native #42484929411 PASS; WF-12 heartbeat #42484941935 and Platform recovery #42484949353 PASS. Native WF-06 #42458256899 remains four HTTP 503s; native WF-12 #42479336350 stale. Platform native reconcile/watchdog/recovery latest recorded runs remain outside freshness budgets; inspection PR #1469 event provenance unknown.
- The GitHub connector still does not expose repository-wide latest Actions run/check-run listing. PR #1468 exact-head checks are directly verified; no post-merge check conclusion is inferred from empty combined-status data.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

## Latest cross-repo execution — 2026-11-08 22:55 ICT / 15:55 UTC

- Current master heads: Platform `e9f079603dcdfe5ecf9c23296009bb4d3a17f9a1`; TCE `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; Stock `e6469ac6617142b349144101a1192cb6aa7104ad`; Media `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; Auth `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1`.
- Open PRs: Platform #1314/#544/#541/#539 draft; Auth #76 draft; TCE/Stock/Media none. Platform #1471 merged; exact-head manifest validation #42493913586 and post-merge master validation #42493968964 passed.
- TCE WF-06 schedule #42489680372 failed four public probes with HTTP 503. WF-12 workflow_run #42489702686 verified the exact scheduled source run/attempt/SHA and dispatched a successful authenticated heartbeat. WF-13 #42489702690 dispatched read-only fallback #42489720607, which again returned four 503s.
- Platform receiver #42489711753 successfully verified the TCE heartbeat after PR #1463's bounded 5xx retry fix. It dispatched the existing reconcile authority at SHA `fb921e9e712fcf6c2d478e674bb5f732480c7942`, mode=apply, target_app=all, allow_image_changes=false.
- Reconciliation #42489725488 passed GHCR access checks, provisioned/verified Auth runtime Secret, left shared `ghcr-pull` unchanged, verified TCE release pairing, prepared checksum-pinned cert-manager v1.21.1 and found no GitOps drift. Manifest apply/image promotion/rollout were skipped. MicroFE health passed; TCE/Auth were explicitly classified as zero-replica maintenance with no live-health assertion.
- Native Platform schedule remains stale: latest reconcile #42467231073, inspection #42483869620, watchdog #42467080859, recovery #42466737776. The 22:10 snapshot is fresh enough for snapshot-age budget but came from a push-triggered inspection, not native cron. TCE WF-06 native #42489680372 and WF-12 native #42479336350 also exceed cadence budgets; workflow_run heartbeats do not count as native schedule evidence.
- K3s snapshot generated 15:10:12Z: node Ready/ARM64; Media and MicroFE active workloads 1/1; Stock Admin/new Backend ImagePullBackOff on 12d63b4; cached Stock backend/user 23b2878 have blank RepoDigest; TCE/Auth/Keycloak 0/0 and OIDC 503; Media runner active. External backup/DNS evidence remains absent.
- Stock scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`; no new Stock/Media/Auth/TCE publisher digest handoff. Auth PR #76 remains draft. No workflow removed, no duplicate SSH/Compose authority, and TCE market-scan schedule unchanged.


## Cross-repo execution — 2026-11-08 23:56 ICT / 16:56 UTC

### Repository state and open PRs

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | `eac9ca7eafca1cd1399b5237188be6dda4675880` | #1314, #544, #541, #539 (planning/documentation) |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 draft; head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` |

Platform inspection PR #1473 was generated by manual `workflow_dispatch` run #42498449089 and merged at `eac9ca7eafca1cd1399b5237188be6dda4675880`. It changed only `debug/vps-latest.md`; it is not native-schedule evidence.

### Platform Actions and reconciliation

- Native reconcile #42499043683: SUCCESS, `schedule`, 2026-11-08 16:16:27Z.
- Native recovery #42498266478: SUCCESS, `schedule`, 16:07:26Z.
- Native watchdog #42498640135: FAILURE, `schedule`, 16:11:47Z. Its exact log reports historic inter-arrival gaps: reconcile 24,773s (45m budget), inspection 26,586s (75m), recovery 24,440s (45m), watchdog 24,414s (45m). This is an observed schedule-delivery gap, not an API retry failure.
- Watchdog workflow_run #42499184691 also failed against the same stale history; #42499221194 was skipped by its guard.
- Latest native inspection remains #42483869620 at 13:12:46Z, older than the 75-minute native cadence budget. Manual inspection #42498449089 completed at 16:09:36Z and generated the current snapshot at 16:09:45Z; that snapshot is fresh by age but does not restore native inspection cadence.
- Reconcile #42499043683 verified GHCR pull access for Auth, MicroFE Shell/WS and TCE web/service; provisioned and verified the Auth runtime Secret with values suppressed; left shared `ghcr-pull` Secrets unchanged; found no Kubernetes drift; and correctly skipped manifest apply, image promotion and rollout. Auth, TCE and MicroFE lane jobs succeeded; Keycloak lane was skipped. Stock/Media remain outside routine Platform GitOps ownership.
- The schedule watchdog is correctly retaining the existing 45/75/45/45-minute budgets. Do not weaken acceptance or alter cron to manufacture a green result. Require a second consecutive native run within budget before claiming cadence recovery.

### TCE health and publisher state

- Latest native WF-06 #42489680372: FAILURE at 14:24:47Z. The TCE web job log confirms HTTP 503 (expected 200); the other three matrix jobs also failed. No newer native WF-06 run appears in the latest 100 repository runs.
- Latest native WF-12 #42479336350: FAILURE at 12:15Z. WF-12 #42489702686 succeeded as a `workflow_run` heartbeat, not as a native scheduled run.
- Native WF-07 #42484929411: SUCCESS at 13:25:55Z.
- Latest build verification #42337126761: SUCCESS (Nov 7); no newer TCE publisher/release run appears in the latest 100 Actions runs.
- K3s snapshot continues to show TCE/Auth workloads at intentional 0/0. The 503s are not a reason to scale them automatically; service-owner recovery/activation approval remains required. TCE market-scan schedule is unchanged.

### StockDividend immutable publisher evidence and current blocker

- Latest publisher run found: [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933), SUCCESS on 2026-11-03 02:04:58Z, source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`.
- Its job log proves native `linux/arm64` publication and verifies full-source-SHA plus version+SHA tags against registry digests:
  - Scraper: `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`
  - Admin: `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`
  - Backend: `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`
- This publication is stale relative to current Stock master `e6469ac6617142b349144101a1192cb6aa7104ad`; no publisher run for current master was found. The existing `deploy.yml` uses an ARM64 runner, publishes `linux/arm64`, and checks immutable tag/digest equality.
- Current K3s desired Admin/Backend tags `12d63b4` still fail with `no match for platform in manifest`. Cached Backend/User `23b2878` images have no CRI RepoDigest and are not promotion evidence.
- Scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is missing. This blocks scraper ingestion/entitlement verification; it is separate from the image publisher and must not be described as the cause of the publisher's age.
- Next action: Stock owner provisions the API key and runs the scraper preflight; app owner publishes from the intended current source SHA; collect new GHCR digests and ARM64 manifest evidence before any promotion.

### Media and Authentication publisher state

- Media CI #42239703151: SUCCESS (Nov 6). Latest production publisher found in the latest 100 runs is #41158598649, SUCCESS on Oct 31, source SHA `32f3bf56e1f44c65a5d98f35bed0547f398f8e90`; no newer Media publisher run.
- Auth CI #42478653766: SUCCESS (Nov 8). Latest release found is manual run #41040510320, SUCCESS on Oct 30, source SHA `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`; no newer Auth publisher run. PR #76 remains draft because Supabase merge-trigger side effects and schema drift remain unresolved.
- No new immutable TCE/Stock/Media/Auth publisher handoff or Platform digest promotion was observed in this run.

### Decommission and runtime safety

- The latest K3s snapshot was generated 16:09:45Z by manual inspection #42498449089. Node `tce-k3s-01` is Ready/ARM64, K3s `v1.36.3+k3s1`; disk 56% (~21 GiB free), available RAM ~19 GiB, `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running. Stock Admin×2 and desired Backend remain ImagePullBackOff/ErrImagePull on `12d63b4`; legacy Backend and Frontend remain 1/1. TCE/Auth/Keycloak remain 0/0; public OIDC probes return 503.
- In-cluster Stock/Media storage preflight is clean (no PVC/PV claims or VolumeSnapshot references). This does not prove external DB/object-storage backups, retention or ownership.
- Dedicated Media runner service is active/enabled and `Runner.Listener` is present. `MEDIA_RUNNER_AUDIT_TOKEN` existence is not verified. The manual-only `decommission-stock-media.yml` delete path still requires a fresh plan, exact typed confirmations, protected production Environment, remote GitHub runner absence, external backup/retention review and authoritative DNS ownership review.
- No namespace/workload/PVC/PV deletion, runner stop/unregister, DNS/database/storage mutation, image promotion, workload scaling or host upgrade/reboot was performed. Preserve the shared Platform runner and existing production authority boundaries.

### Ownership and controls

- App repositories own tests/builds and immutable GHCR publication.
- Platform Infra alone owns production manifests, shared GHCR pull credentials, source/digest verification, GitOps promotion/reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No workflow was removed; no duplicate direct SSH/Compose deployment authority was introduced; TCE market-scan schedule unchanged.


## Cross-repo execution — 2026-11-09 01:03 ICT / 2026-11-08 18:03 UTC

### Repository state and pull requests

| Repository | Current master SHA | Open PRs |
|---|---|---|
| Platform Infra | b0f791422dc9fb5056a77b7dfbfb01deba36d6f2 | #1314, #544, #541, #539 (draft planning/docs) |
| TCE Dashboard | 7ab52078c4250829e158f05b2695ceb9d11bdbe3 | None |
| StockDividend | e6469ac6617142b349144101a1192cb6aa7104ad | None |
| Media Generation | 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d | None |
| Authentication | cb907a63df0e0441b54b7b930ecdbfa97a5e52e1 | #76 (draft) |

Platform inspection PR #1475 was squash-merged at b0f791422dc9fb5056a77b7dfbfb01deba36d6f2. Its exact-head manifest validation was #42507931004 (workflow_dispatch, SUCCESS) against PR head d1dd17cd8932d83b4795fa6e9d344cb37d811809. The inspection workflow log confirms it merged only after exact-head validation. No post-merge validation run was visible at this checkpoint; the PR changed only debug/vps-latest.md. The new snapshot blob is b45229cbca95d22b8084cbfb71767c12c725f759 and was generated at 18:00:37Z.

Latest open PR scope was reviewed: #1314 managed mailbox plan; #544 Keycloak activation status; #541 Keycloak DB preparation; #539 identity architecture ADR; Auth #76 migration-drift investigation. These remain draft and were not merged or retargeted because they are outside the immediate deployment dependency chain and retain explicit human/production safety gates.

### Latest workflow runs and native schedule evidence

Platform latest operational runs:
- Native reconcile #42499043683: SUCCESS, schedule, 16:16:27Z.
- Native recovery #42498266478: SUCCESS, schedule, 16:07:26Z.
- Native schedule watchdog #42498640135: FAILURE, schedule, 16:11:47Z.
- Latest native inspection #42483869620: SUCCESS, schedule, 13:12:46Z; stale at this checkpoint.
- Manual reconcile #42507600702: SUCCESS, workflow_dispatch, 17:58:28Z.
- Manual inspection #42507763937: SUCCESS, workflow_dispatch, 18:00:28Z; produced the 18:00:37Z snapshot and PR #1475.
- Exact-head manifest validation #42507931004: SUCCESS, workflow_dispatch, 18:02:19Z.

The native watchdog log for #42498640135 recorded historic inter-arrival gaps:
- reconcile-vps.yml: 24,773s (45-minute budget);
- inspect-vps.yml: 26,586s (75-minute budget);
- recover-stale-ops.yml: 24,440s (45-minute budget);
- reconcile-schedule-watchdog.yml: 24,414s (45-minute budget).
It also recorded TCE WF-06 gap 25,570s and WF-12 gap 23,089s, both above the 25-minute observation budget. Later single native runs do not yet establish consecutive within-budget cadence. At 18:03Z the latest Platform native reconcile/recovery/watchdog/inspection observations were still older than their respective freshness budgets. The log establishes inter-arrival failures, not whether GitHub scheduler delivery, runner availability, or another upstream condition caused them. Do not weaken budgets or change cron as a workaround.

TCE latest native runs:
- WF-12 #42507582654: FAILURE, schedule, 17:58:14Z; its verification job found the last native WF-06 run #42489680372 at 14:24:47Z, age 213m against the 25m budget.
- WF-06 #42489680372: FAILURE, schedule, 14:24:47Z; all four public probes returned HTTP 503.
- WF-07 #42484929411: SUCCESS, schedule, 13:25:55Z.
- WF-13 #42507595891: SUCCESS, workflow_run; dispatched the read-only WF-06 fallback #42507608317.
- WF-06 fallback #42507608317: FAILURE; TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503.

The WF-12 heartbeat job for #42507582654 successfully dispatched event tce-schedule-heartbeat to Platform. Platform receiver #42507589119 completed successfully and validated the authenticated dispatch path. It observed the last master reconciliation #42499043683 at age 100m, then dispatched the existing reconciliation authority. The correlated fallback reconciliation was #42507600702 with ref master, mode apply, target_app all, allow_image_changes false. No new image-promotion inputs were supplied. The subsequent reconciliation found no drift and skipped apply, promotion and rollout.

TCE WF-06 remains on its existing every-15-minute schedule and WF-12 remains at 7,22,37,52. No TCE market-scan workflow or schedule was changed.

Stock latest scheduled scraper run #42457182511 (07:03:12Z) failed closed because VNSTOCK_API_KEY is missing. Stock CI #42440810105 passed. Media CI #42239703151 passed. Authentication CI #42478653766 passed. No new app publisher run or current-master immutable digest handoff was observed.

### Reconciliation and shared credentials

Manual Platform reconciliation #42507600702 completed successfully:
- GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE web/service.
- Auth runtime Secret was provisioned and verified with secret values suppressed.
- Shared ghcr-pull credentials were unchanged.
- GitOps drift was false.
- Manifest apply, image promotion and rollout were correctly skipped.
- Auth, TCE and MicroFE lanes completed; Keycloak lane was skipped.

The native reconciliation #42499043683 had also passed earlier with no drift. No production manifest or image changed in either run.

### K3s snapshot — 2026-11-08 18:00:37Z

Node tce-k3s-01 is Ready on ARM64, K3s v1.36.3+k3s1, Ubuntu 22.04.5 LTS, kernel 6.8.0-1049-oracle. Disk usage is 56% with about 21 GiB free; available RAM is about 19 GiB. Host uptime is 191 days and restart_required=yes. Docker reports 20 images / 9.195 GB, with 5.773 GB reclaimable. No cleanup, package upgrade or reboot was performed.

| Workload | Observed state |
|---|---|
| cert-manager and core K3s services | Running 1/1 |
| Media backend/frontend | Running 1/1 each |
| MicroFE Shell/WS/NATS | Running 1/1 each |
| Stock Admin | Two pods ImagePullBackOff on tag 12d63b4 |
| Stock Backend | Existing 23b2878 pod 1/1; new 12d63b4 pod ImagePullBackOff |
| Stock frontend/user | 23b2878 pod 1/1 |
| TCE frontend/service | 0/0 |
| Auth runtime / Keycloak | 0/0 |

The Stock 12d63b4 Admin/Backend pulls report no matching platform in manifest on the ARM64 node. The cached Stock backend:23b2878 and user:23b2878 entries have blank RepoDigest; their local image IDs are not registry digests or promotion evidence. GHCR digest coverage remains warning. Media backend/frontend and MicroFE Shell/WS have registry RepoDigests; their active pods are healthy. Auth image has a RepoDigest in CRI inventory, but no new release/promotion was performed.

Public TCE and OIDC endpoints return HTTP 503 while TCE/Auth/Keycloak workloads are explicitly at 0/0 maintenance. Do not infer that scaling them is authorized. Service-owner approval and a reviewed recovery plan remain required.

In-cluster Stock/Media storage preflight is clean: no Stock/Media PVC/PV claims or VolumeSnapshot references were found; the separate k3s-debug PVC remains. This does not prove external database/object-storage backup, retention or DNS ownership.

Media runner service is active/enabled and Runner.Listener is present. Platform runner is also active. GitHub runner registration, MEDIA_RUNNER_AUDIT_TOKEN, external backup/retention and authoritative DNS ownership remain unverified. Do not retire the runner or run decommission delete mode.

### Immutable publisher evidence and app ownership

- Stock last verified publisher #41563856933 is from 2026-11-03, source SHA 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec. It verified ARM64 Scraper/Admin/Backend digest equality for full-SHA and version+SHA tags, but it is stale versus Stock master e6469ac6617142b349144101a1192cb6aa7104ad. No current-master publisher evidence exists. Missing VNSTOCK_API_KEY blocks scraper ingestion/entitlement verification, not the image build itself.
- Media last verified publisher #41158598649 is from 2026-10-31, source SHA 32f3bf56e1f44c65a5d98f35bed0547f398f8e90. Its ARM64 publication succeeded, but prior Platform promotion #41158826992 failed because the release did not converge on GitOps master. Current K3s Media pods are running pinned digests. No new handoff was observed.
- Auth last verified manual release #41040510320 is from 2026-10-30, source SHA ceb2688d6277b10f1bfe7652223d1d295b7e49d9. Auth CI #42478653766 passed; PR #76 remains draft. No new release/promotion was observed.
- TCE has no newer publisher evidence than the previously recorded build verification; its active workloads remain intentionally 0/0.

App repositories continue to own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared GHCR pull credentials, source/digest verification, GitOps promotion/reconciliation, rollout and health verification.

### Exact next actions and safety

1. GitHub administrator: investigate missing/delayed native schedule events using Actions schedule/runner telemetry; require consecutive within-budget native runs before declaring cadence recovered. Do not change existing cron or freshness budgets.
2. Stock owner: provision VNSTOCK_API_KEY, run safe preflight, then publish from the intended current source SHA and provide verified ARM64 digests before any Platform promotion.
3. TCE/Auth service owners: approve and execute a recovery/activation plan for the 0/0 services before expecting public health probes to return 200; no automatic scaling.
4. Media owner: provide runner audit-token verification, external backup/retention evidence and authoritative DNS ownership before any runner or namespace decommission.
5. Auth owner: continue PR #76 investigation; keep draft until the Supabase integration side-effect gate is resolved.

No production manifest apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host upgrade/reboot occurred. No workflow was removed and no duplicate direct SSH/Compose production authority was introduced. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only. TCE market-scan schedule unchanged.


## Latest cross-repo execution — 2026-11-09 02:00 ICT / 19:00 UTC

### Repository heads and open pull requests

- Platform Infra master: `e412faffc669a766176adccec7207c5cc02306f5`. Inspection PR [#1477](https://github.com/phanthienquoc/platform-infra/pull/1477) was squash-merged at this SHA. Its exact validated head was `874cedfb52b9bdacc7c3fc5eba1ccde41dddb859`; exact-head `validate-manifests` [#42510263923](https://github.com/phanthienquoc/platform-infra/actions/runs/42510263923) passed. The inspection snapshot was generated at 18:27:55Z. No separate post-merge validation run for the inspection-only commit was observed.
- TCE Dashboard master: `7ab52078c4250829e158f05b2695ceb9d11bdbe3`; no open PR.
- StockDividend master: `e6469ac6617142b349144101a1192cb6aa7104ad`; no open PR.
- Media Generation master: `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`; no open PR.
- Authentication master: `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1`; draft PR [#76](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/76) remains open.
- Platform draft PRs #1314/#544/#541/#539 remain open and unmerged. Their latest recorded `validate-manifests` runs passed respectively: #42161859747, #38575430454, #38567431761 and #38548718033. PR #544 currently reports mergeable=false; do not force-update or merge these planning/approval-gated PRs. Auth PR #76's latest `auth-service-ci` #41329425940 passed. TCE, Stock and Media have no open PRs.

### Native schedule evidence (event= schedule only)

Platform latest native runs and immediately preceding native runs:

| Workflow | Latest native run | Previous native run | Inter-arrival gap | Budget |
|---|---|---|---:|---:|
| Reconcile | [#42499043683](https://github.com/phanthienquoc/platform-infra/actions/runs/42499043683), SUCCESS, 16:16:27Z | #42467231073, 09:27:03Z | 24,564s | 2,700s |
| Inspection | [#42510125328](https://github.com/phanthienquoc/platform-infra/actions/runs/42510125328), SUCCESS, 18:27:47Z | #42483869620, 13:12:46Z | 18,901s | 4,500s |
| Recovery | [#42498266478](https://github.com/phanthienquoc/platform-infra/actions/runs/42498266478), SUCCESS, 16:07:26Z | #42466737776, 09:20:06Z | 24,440s | 2,700s |
| Schedule watchdog | [#42498640135](https://github.com/phanthienquoc/platform-infra/actions/runs/42498640135), FAILURE, 16:11:47Z | #42467080859, 09:24:53Z | 24,414s | 2,700s |

The watchdog gaps are about 5.25–6.82 hours, materially above the existing budgets. Inspection is currently the freshest native lane, but its latest inter-arrival gap also exceeded its 75-minute budget. Recent `workflow_dispatch`, `workflow_run` and `repository_dispatch` executions are not native schedule evidence. Do not change cron or weaken freshness/queue budgets; the evidence proves missing/delayed schedule events, not a code-level cause.

TCE native schedule evidence:

| Workflow | Latest native run | Previous native run | Inter-arrival gap | Budget/result |
|---|---|---|---:|---|
| WF-06 | [#42512468931](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42512468931), FAILURE, 18:56:20Z | #42489680372, 14:24:47Z | 16,293s | 900s cadence; all four public probes failed |
| WF-12 | [#42507582654](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42507582654), FAILURE, 17:58:14Z | #42479336350, 12:15:00Z | 20,594s | 900s cadence; watchdog reported WF-06 age 213m |
| WF-07 integration | [#42484929411](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42484929411), SUCCESS, 13:25:55Z | #42453060493, 06:01:55Z | 26,640s | Historical gap exceeds its observed cadence |

WF-06 #42512468931 is newer than the WF-12 schedule run; it does not retroactively make WF-12's native cadence healthy. The subsequent WF-12 `workflow_run` event and Platform heartbeat are separate event types.

### Reconciliation and dispatch evidence

- TCE WF-06 #42512468931 failed all four public probes (TCE web, TCE API, Auth liveness and Auth readiness). The observed endpoints remain HTTP 503 while TCE/Auth are intentionally zero-replica maintenance; this is not a reason to scale workloads automatically.
- TCE WF-12's heartbeat path was accepted by Platform. The receiver/recovery chain dispatched the existing `reconcile-vps.yml` authority; the correlated manual reconciliation was [#42512502763](https://github.com/phanthienquoc/platform-infra/actions/runs/42512502763), `workflow_dispatch`, SUCCESS, with `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- Reconciliation verified GHCR read access and Auth runtime Secret presence; `ghcr-pull` was unchanged. GitOps drift was false, so manifest apply was skipped. MicroFE active health passed; TCE and Auth were explicitly recognized as zero-replica maintenance; Keycloak was skipped. No image promotion or rollout occurred.
- Recovery [#42512617350](https://github.com/phanthienquoc/platform-infra/actions/runs/42512617350) completed successfully after verifying the source reconciliation. It was `workflow_dispatch`, not a native schedule run.

### App CI, publisher and credentials

- Stock CI [#42440810105](https://github.com/phanthienquoc/stockdividend/actions/runs/42440810105) passed. Scheduled scraper [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) failed closed because repository secret `VNSTOCK_API_KEY` is absent. This blocks scraper entitlement/ingestion, not the image build. No new current-master publisher/digest evidence exists; the previously verified publisher is stale versus current master.
- Media CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) passed. No new publisher run was observed; current K3s Media images remain digest-pinned.
- Auth CI [#42478653766](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42478653766) passed. No new release/promotion was observed; PR #76 remains draft.
- TCE has no new publisher run or digest handoff. Preserve app ownership of tests/builds/immutable GHCR publication; Platform alone owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health.

### Latest read-only K3s and Stock/Media decommission evidence

Source: native inspection [#42510125328](https://github.com/phanthienquoc/platform-infra/actions/runs/42510125328), snapshot generated `2026-11-08T18:27:55Z`, committed by inspection PR #1477.

- Node `tce-k3s-01` is Ready/ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk 56% (~21 GiB free), available RAM ~19 GiB. Host uptime is 191 days and `restart_required=yes`; Docker reports 20 images/9.195 GB, 5.773 GB reclaimable. No cleanup, package upgrade or reboot occurred.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running.
- Stock Admin×2 and the newer Backend remain ImagePullBackOff on `12d63b4` because the registry has no matching ARM64 manifest. Older Stock Backend and Frontend remain 1/1 on legacy tags.
- TCE/Auth runtime and Keycloak remain 0/0 maintenance. No live health is claimed for those lanes.
- The inspection itself ran `scripts/decommission-stock-media-namespaces.sh plan`: both target namespaces are present, `tce-prod` and `microfe-platform` are present, and the fresh in-cluster preflight reports no Stock/Media PVC, PV claim or VolumeSnapshot references (`storage-clean`). It made no changes.
- The same snapshot shows the dedicated Media runner service active/enabled and `Runner.Listener` present. GitHub repository runner registration is not inferred by the host snapshot. Stock Ingresses still publish `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space`, `api.mrcute.space`; Media Ingress still publishes `media.mrcute.space`.
- In-cluster storage-clean is not proof of external database/object-storage backup, retention or ownership. Authoritative DNS/provider ownership and external-data retention remain unverified. The protected delete workflow additionally requires the dedicated Media runner to be stopped, disabled and unregistered, a valid read-only `MEDIA_RUNNER_AUDIT_TOKEN`, exact typed confirmations and the protected production Environment.

### Exact next actions and safety

1. GitHub administrator: investigate native schedule delivery/runner telemetry. Require consecutive within-budget native runs; do not use manual/dispatch runs as substitutes and do not change TCE market-scan or existing cron schedules.
2. Stock owner: provision `VNSTOCK_API_KEY` in Stock repository Actions secrets and run the safe preflight. Separately publish the intended current source SHA and supply verified ARM64 full-SHA/version+SHA digest evidence before any Platform promotion.
3. TCE/Auth service owners: approve an explicit recovery/activation plan for the intentional 0/0 lanes before public HTTP 503 can be treated as an actionable deployment failure. No automatic scaling.
4. Media owner/operator: confirm the dedicated runner is idle, stop/disable it, unregister it from the Media repository and provide the read-only audit token. Confirm external backup/retention and authoritative DNS/provider ownership. Then run the protected decommission plan again and, only with all gates satisfied, delete exactly `stock-prod` and `media-prod`.
5. Auth owner: continue PR #76 schema/migration drift investigation; keep it draft until Supabase side-effect gates are resolved.

No production manifest/image change, workload scaling, namespace/PVC/PV deletion, runner stop/unregister, DNS/database/storage mutation or host maintenance occurred. No workflow was removed or duplicate direct SSH/Compose production authority added. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


# Cross-repo deployment checkpoint — 2026-11-09 03:16 ICT / 2026-11-08 20:16 UTC

## Repository state and pull requests

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | `5197840226b49d790cb99c4caeb8377526e6fed8` | #1314, #544, #541, #539 — all draft |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 — draft |

Platform PR #1479 and #1480 are merged; read-only inspection PR #1481 is merged. No application repository source head changed in this execution.

## Concrete implementation and validation

### PR #1479 — require successful scheduled reconciliation

- [PR #1479](https://github.com/phanthienquoc/platform-infra/pull/1479), merge SHA `01a3b4ba4ebcf481bd532bbc367533da9f2791a3`.
- Added `scripts/verify-scheduled-run-result.py`; the schedule watchdog now checks the latest reconciliation's completed conclusion after freshness validation. A recent `failure`, `cancelled`, `timed_out`, or unknown status no longer passes as merely fresh.
- Queued/in-progress runs remain explicitly pending while the existing runner-queue gate continues to inspect unassigned lanes. Push-only read-only API smoke remains warning-only.
- Eight regression cases cover success, failure, cancellation, timeout, push warning, queued, in-progress and unknown status.
- Exact-head `validate-github-actions` [#42518862616](https://github.com/phanthienquoc/platform-infra/actions/runs/42518862616) and `validate-manifests` [#42518862627](https://github.com/phanthienquoc/platform-infra/actions/runs/42518862627) passed.
- Post-merge [#42518955884](https://github.com/phanthienquoc/platform-infra/actions/runs/42518955884) and [#42518955893](https://github.com/phanthienquoc/platform-infra/actions/runs/42518955893) passed.

### PR #1480 — keep read-only verifier out of production recovery triggers

- [PR #1480](https://github.com/phanthienquoc/platform-infra/pull/1480), merge SHA `9bb69b446d6aa161aae13c7efe4648af92691641`.
- Excluded `scripts/verify-scheduled-run-result.py` from the broad `scripts/**` push path in `recover-stale-ops.yml`.
- Extended `validate-workflow-contracts.py` so this read-only helper remains excluded from production reconciliation bootstrap.
- Exact-head `validate-github-actions` [#42519090963](https://github.com/phanthienquoc/platform-infra/actions/runs/42519090963) and `validate-manifests` [#42519090975](https://github.com/phanthienquoc/platform-infra/actions/runs/42519090975) passed.
- Post-merge [#42519197247](https://github.com/phanthienquoc/platform-infra/actions/runs/42519197247) and [#42519197245](https://github.com/phanthienquoc/platform-infra/actions/runs/42519197245) passed.

### PR #1481 — fresh read-only K3s inspection

- [PR #1481](https://github.com/phanthienquoc/platform-infra/pull/1481), merge SHA `5197840226b49d790cb99c4caeb8377526e6fed8`.
- Inspection [#42519127338](https://github.com/phanthienquoc/platform-infra/actions/runs/42519127338) completed successfully and generated `debug/vps-latest.md` at `2026-11-08T20:14:51Z`.
- Exact inspection PR validation [#42519280294](https://github.com/phanthienquoc/platform-infra/actions/runs/42519280294) passed. This is a manual/read-only inspection, not native schedule evidence; no separate post-merge validation run was observed for the snapshot-only merge.

## Recovery/reconciliation side effect and result

The #1479 helper file initially matched the recovery controller's broad `scripts/**` push filter. The resulting read-only push smoke [#42518955934](https://github.com/phanthienquoc/platform-infra/actions/runs/42518955934) and recovery [#42518955895](https://github.com/phanthienquoc/platform-infra/actions/runs/42518955895) completed successfully; recovery dispatched the existing production authority [#42518969801](https://github.com/phanthienquoc/platform-infra/actions/runs/42518969801) with `mode=apply`, `target_app=all`, `allow_image_changes=false`.

The reconciliation logs provide evidence that:
- Shared `ghcr-pull` was unchanged across namespaces.
- Auth runtime Secret was provisioned/verified; secret values were not logged.
- GHCR read access passed.
- `reconcile-vps.sh plan` reported Kubernetes state matches repository state (`drift=false`).
- Production manifest apply and rollout were skipped; no image promotion occurred.
- Active TCE/Auth/MicroFE lanes were checked with maintenance-aware semantics; TCE/Auth/Keycloak remained zero-replica and were not scaled.
- Recovery after reconciliation [#42519090505](https://github.com/phanthienquoc/platform-infra/actions/runs/42519090505) passed and dispatched a read-only inspection.

PR #1480 now prevents this read-only helper from triggering another production reconciliation on future pushes. The observed run itself made no manifest/image change.

## Native schedule acceptance — event=schedule only

At 20:16 UTC, the latest native Platform events remain:

| Workflow | Latest native run | Inter-arrival gap | Budget | Age at review |
|---|---|---:|---:|---:|
| Reconcile | [#42499043683](https://github.com/phanthienquoc/platform-infra/actions/runs/42499043683), success, 16:16:27Z | 24,564s | 2,700s | ~240m |
| Inspection | [#42510125328](https://github.com/phanthienquoc/platform-infra/actions/runs/42510125328), success, 18:27:47Z | 18,901s | 4,500s | ~109m |
| Recovery | [#42498266478](https://github.com/phanthienquoc/platform-infra/actions/runs/42498266478), success, 16:07:26Z | 24,440s | 2,700s | ~249m |
| Watchdog | [#42498640135](https://github.com/phanthienquoc/platform-infra/actions/runs/42498640135), failure, 16:11:47Z | 24,414s | 2,700s | ~245m |

All four native cadence budgets remain violated. The new manual inspection #42519127338 and manual recovery/reconciliation runs are not native schedule evidence.

TCE native evidence remains:
- WF-06 [#42512468931](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42512468931), failure at 18:56:20Z; previous native run #42489680372, gap 16,293s vs 900s cadence. Four public probes returned HTTP 503.
- WF-12 [#42507582654](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42507582654), failure at 17:58:14Z; previous native run #42479336350, gap 20,594s vs 900s cadence; watchdog found WF-06 stale.
- WF-07 [#42484929411](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42484929411) passed at 13:25:55Z, but its historical gap is 26,640s.
- Subsequent `workflow_run`, `workflow_dispatch` and `repository_dispatch` heartbeat/recovery activity does not satisfy native schedule acceptance.

No cron, freshness budget or TCE market-scan schedule changed.

## Latest K3s snapshot — manual read-only inspection

Source: PR #1481 snapshot generated `2026-11-08T20:14:51Z`.

- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`.
- Disk 56% (~21 GiB free); available RAM ~19 GiB; host uptime 191 days; `restart_required=yes`.
- Docker: 20 images, 9.195 GB; 5.773 GB reported reclaimable. No cleanup, upgrade or reboot.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with digest evidence.
- Stock Admin has two ImagePullBackOff pods on `12d63b4`; the desired Backend on `12d63b4` also fails with `no match for platform in manifest`. Legacy Backend and Frontend remain 1/1 on `23b2878`; their cached images have blank RepoDigest and are not promotion evidence.
- TCE frontend/service, Auth `microfe-auth` and Keycloak remain 0/0. Keycloak readiness timed out; both public OIDC discovery probes returned HTTP 503. No scaling was authorized.
- Media backend/frontend images, Auth image, TCE images and MicroFE images have registry digest evidence. Stock cached backend/user tags `23b2878` still lack RepoDigest.
- Read-only Stock/Media decommission preflight reports no target PVC/PV claims or VolumeSnapshot references (`storage-clean`); `tce-prod` and `microfe-platform` remain present.
- Media runner service is still active/enabled and `Runner.Listener` is present. GitHub runner registration is not inferred by host inspection.
- External database/object-storage backup, retention and authoritative DNS/provider ownership remain unverified. The target namespaces and workloads are still present; no delete mode ran.

## App repository evidence and blockers

- Stock master CI [#42440810105](https://github.com/phanthienquoc/stockdividend/actions/runs/42440810105) passed. Scheduled scraper [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) failed closed because `VNSTOCK_API_KEY` is missing. This blocks authenticated scraper ingestion, not image build/publish by itself. No current-master immutable ARM64 publisher evidence exists.
- Media CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) passed; no new publisher run. Runtime images remain digest-pinned.
- Auth CI [#42478653766](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42478653766) passed; PR #76 remains draft. No new release/promotion evidence.
- TCE has no new publisher/digest handoff; WF-06 endpoints remain HTTP 503 while TCE/Auth are intentionally 0/0.

## Exact next actions

1. GitHub administrator: investigate native schedule event delivery and runner/scheduler telemetry. Require consecutive within-budget native events; do not change cron or TCE market-scan schedule.
2. Stock owner: add `VNSTOCK_API_KEY` to Stock Actions secrets, run safe preflight, then publish the selected current source SHA as immutable ARM64 images with full-SHA/version+SHA tags and matching registry digests.
3. TCE/Auth service owners: approve an explicit recovery/activation plan for intentional 0/0 lanes before treating HTTP 503 as an actionable deployment failure. No automatic scaling.
4. Media owner/operator: verify runner idle state, stop/disable/unregister the Media runner, provide read-only audit token, and confirm external backup/retention plus authoritative DNS ownership. Then re-run protected decommission preflight and only delete exactly `stock-prod` and `media-prod` when all gates pass.
5. Auth owner: continue PR #76 schema/migration drift and Supabase side-effect investigation; keep draft until resolved.
6. Platform operator: schedule host maintenance separately; no unattended reboot or package/containerd upgrade.

No production image promotion, manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host upgrade/reboot occurred in this execution. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No workflow was removed and no direct SSH/Compose production authority was added. TCE market-scan schedule unchanged.


## Latest cross-repo execution — 2026-11-09 03:56 ICT / 2026-11-08 20:56 UTC

### Repository state and open pull requests

- Platform Infra master is the base for this checkpoint; the latest observed master workflow SHA is `0c29f9c38964d6e78ac0295a0073bf571b62116f`. Open draft PRs #1314 (managed mail plan), #544 (Keycloak activation status; currently mergeable=false), #541 (Keycloak/Supabase DB preparation), and #539 (identity architecture ADR) remain human-review decisions and were not merged.
- TCE Dashboard master `7ab52078c4250829e158f05b2695ceb9d11bdbe3`: no open PRs.
- StockDividend master `e6469ac6617142b349144101a1192cb6aa7104ad`: no open PRs.
- Media Generation master `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d`: no open PRs.
- Authentication master `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1`: PR #76 remains draft; its migration/schema drift and Supabase side-effect investigation is not approved for merge.

### Latest workflow and check evidence

| Repository | Latest relevant evidence | Result |
|---|---|---|
| Platform Infra | Reconcile schedule #42521088881 at 20:37:39Z | PASS |
| Platform Infra | Watchdog workflow_run #42521222353 at 20:39:19Z | FAIL: stale native inspection and historical inter-arrival gaps |
| Platform Infra | Recovery workflow_run #42521222393 | PASS |
| Platform Infra | Recovery workflow_dispatch #42521201349 | PASS |
| TCE Dashboard | WF-06 schedule #42512468931; manual fallback #42512497073 | FAIL: TCE API, TCE web, Auth liveness and Auth readiness all HTTP 503 |
| TCE Dashboard | WF-12 schedule #42507582654 | FAIL: WF-06 schedule freshness exceeded |
| StockDividend | Scraper schedule #42457182511 | FAIL closed: missing repository secret `VNSTOCK_API_KEY` |
| StockDividend | CI #42440810105 | PASS |
| Media Generation | CI #42239703151 | PASS; no current-master publisher run observed |
| Authentication | CI #42478653766 | PASS; no new release/promotion run observed |

The latest Platform watchdog failure was not a GitOps apply failure. Its logs recorded native schedule inter-arrival gaps:
- reconcile-vps: 15,672s vs 2,700s budget;
- inspect-vps: 18,901s vs 4,500s budget;
- recover-stale-ops: 15,605s vs 2,700s budget;
- reconcile-schedule-watchdog: 15,517s vs 2,700s budget.
The inspection-delivery step also failed because the latest native inspection remained stale. Recovery delivery/result verification passed. TCE WF-06 and WF-12 gaps were 16,293s and 20,594s respectively against the 1,500s observation budget. These are scheduler-delivery/cadence observations; do not change cron or freshness budgets to mask them.

### Stock publisher contract clarification

The current Stock `.github/workflows/deploy.yml` is a native ARM64 immutable publisher:
- master pushes build/publish Scraper, Admin and Backend with full 40-character source-SHA and `prod-v<version>-<sha>` tags, then verify ARM64 manifests and equal registry digests for both tags;
- manual `workflow_dispatch` publication is explicitly blocked unless repository variable `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`;
- when the variable is false, a master push may still publish immutable artifacts but does not send a Platform handoff;
- missing `VNSTOCK_API_KEY` blocks authenticated scraper ingestion only; it is not the publisher's image-build credential.
No secret or release variable was changed, and no manual production publication was attempted. No current-master publisher digest evidence was observed.

### Runtime and safety

- Latest committed K3s inspection snapshot is from PR #1481, generated `2026-11-08T20:14:51Z`; at this checkpoint it is ~42 minutes old and remains within the 75-minute snapshot-age budget, but it is a manual inspection and does not satisfy native inspection cadence.
- Node `tce-k3s-01` remains Ready/ARM64, K3s `v1.36.3+k3s1`; disk 56% (~21 GiB free), available RAM ~19 GiB, host uptime 191 days and `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. Stock Admin×2 and desired Backend remained ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend remained 1/1 on `23b2878`. TCE/Auth/Keycloak remained 0/0 maintenance; public probes returned HTTP 503. Media runner service remained active/enabled with `Runner.Listener` present.
- In-cluster Stock/Media storage preflight was storage-clean, but external backup/retention, authoritative DNS ownership, Media runner remote registration audit and `MEDIA_RUNNER_AUDIT_TOKEN` remain unverified. No namespace or runner deletion is authorized.
- The prior read-only helper change caused one recovery-triggered reconciliation; it found `drift=false`, kept shared `ghcr-pull` unchanged, verified Auth runtime Secret and GHCR read access, and skipped apply/promotion/rollout. PR #1480 now excludes that read-only helper from recovery push triggers.

### Exact next actions

1. GitHub administrator: inspect native schedule event delivery and runner/scheduler telemetry; require consecutive within-budget native runs. Preserve all cron and freshness budgets.
2. Stock owner: provide `VNSTOCK_API_KEY` for scraper preflight; separately select/approve a current source SHA and allow a master push or explicitly authorize the protected manual publication variable before expecting a current-master immutable publisher run.
3. TCE/Auth owners: decide whether to activate the intentionally zero-replica services and approve a recovery plan; do not auto-scale from public 503 probes.
4. Media owner/operator: verify idle state, stop/disable/unregister the Media runner, provide the read-only audit token, and confirm external backup/retention and authoritative DNS ownership before protected decommission.
5. Auth owner: continue PR #76 schema/migration drift and Supabase side-effect investigation; keep draft.
6. Platform operator: plan host maintenance separately; no unattended reboot or package/containerd upgrade.

No production manifest apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host upgrade/reboot occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No workflow was removed and no direct SSH/Compose production authority was added. TCE market-scan schedule unchanged.


## Latest cross-repo execution — 2026-11-09 04:56 ICT / 2026-11-08 21:56 UTC

## Repository heads and pull requests

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | `da24edc6019ac18be2f298eed06803848362aa68` | #1314, #544, #541, #539 (all draft; human decisions) |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 draft |

Platform PR #1483 was squash-merged at `66bb04310da59920c793ecfd6139eb2aff82b508`; exact-head validation #42522879989 and post-merge validation #42522928075 passed. The four open Platform planning/architecture PRs remain drafts and were not merged.

## Latest workflow and check evidence

| Repository | Run | Result | Evidence |
|---|---|---|---|
| Platform Infra | #42522928075 validate-manifests | PASS | Post-merge validation for #1483 |
| Platform Infra | #42520452305 native watchdog | FAIL | Native schedule freshness/inter-arrival gaps |
| Platform Infra | #42521088881 native reconcile | PASS | 20:37:39Z; later than watchdog's inspected source |
| Platform Infra | #42520213983 native recovery | PASS | 20:27:31Z |
| TCE Dashboard | #42527713763 WF-12 native schedule | FAIL | WF-06 schedule stale; heartbeat job passed |
| TCE Dashboard | #42527723683 WF-13 recovery | PASS | Dispatched read-only WF-06 fallback |
| TCE Dashboard | #42527735064 WF-06 manual fallback | FAIL | All four public probes still HTTP 503 |
| StockDividend | #42440810105 CI | PASS | Master CI |
| StockDividend | #42457182511 weekend scraper | FAIL closed | Missing `VNSTOCK_API_KEY` before dependency installation |
| Media Generation | #42239703151 CI | PASS | No new publisher run |
| Authentication | #42478653766 CI | PASS | PR #76 remains draft; no new release/promotion |

## TCE heartbeat and Platform recovery chain

TCE WF-12 #42527713763 ran natively at 21:56:51Z. Its heartbeat job succeeded and sent a payload identifying:

- source repository `phanthienquoc/TCE-dashboard`;
- source event `schedule`;
- workflow `.github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml`;
- source/heartbeat run ID `42527713763`;
- attempt `1`;
- source and heartbeat SHA `7ab52078c4250829e158f05b2695ceb9d11bdbe3`.

Platform receiver/recovery #42527720332 validated the source run against the TCE Actions API and succeeded. Because the latest master reconciliation was 77 minutes old, recovery dispatched the existing sole production authority:

```text
ref=master
sha=66bb04310da59920c793ecfd6139eb2aff82b508
mode=apply
target_app=all
allow_image_changes=false
```

Reconciliation #42527730424 completed successfully. Logs confirm:

- GHCR pull access passed for Auth, MicroFE Shell/WS and TCE service/web packages.
- Auth runtime Secret was provisioned and verified; secret values were suppressed.
- Shared `ghcr-pull` was unchanged.
- The blocked-image-pull helper inspected only active core workloads in `microfe-platform` and `tce-prod`; it found no image-pull failures and did not restart Stock/Media workloads.
- Kubernetes diff returned `drift=false`; manifest apply, image promotion and rollout were skipped.
- No workload scaling occurred.

The reconciliation therefore verified shared runtime prerequisites but did not activate TCE/Auth or change desired production manifests.

A recovery-triggered read-only inspection #42527885366 was still in progress at this checkpoint. It is a `workflow_dispatch` run and does not count as native inspection cadence.

## Native schedule acceptance — schedule events only

At 21:56:51Z, latest native Platform evidence and measured gaps were:

| Workflow | Latest native run | Gap | Budget | Age at review |
|---|---|---:|---:|---:|
| Reconcile | #42521088881, 20:37:39Z, success | 15,672s | 2,700s | ~79m |
| Inspection | #42510125328, 18:27:47Z, success | 18,901s | 4,500s | ~209m |
| Recovery | #42520213983, 20:27:31Z, success | 15,605s | 2,700s | ~89m |
| Watchdog | #42520452305, 20:30:24Z, failure | 15,517s | 2,700s | ~86m |

The watchdog log measured the latest inspection self-hosted runner queue wait at `0m`. This does not prove why GitHub omitted later native events, but it provides no evidence that the inspection runner queue caused the observed multi-hour gap. The remaining issue is native schedule event delivery/cadence; GitHub administrator investigation is required. Do not change cron expressions or freshness budgets.

TCE native evidence:

- WF-06 #42512468931 at 18:56:20Z failed; inter-arrival gap was 16,293s against the 1,500s budget. WF-12 measured it 180 minutes old with queue wait 0m.
- WF-12 #42527713763 at 21:56:51Z failed because WF-06 was stale. Its inter-arrival gap from #42507582654 was 14,317s against the 1,500s budget.
- The WF-06 fallback #42527735064 also failed all four public HTTP 200 probes (TCE web, TCE API, Auth liveness, Auth readiness) with HTTP 503.

Manual, push, workflow_run and repository_dispatch runs remain separate from native schedule acceptance.

## Latest K3s snapshot and runtime limits

The latest committed snapshot is PR #1484, generated at 21:59:12Z and fresh at the 05:01 ICT review. Inspection #42527885366 completed successfully; validation #42528039006 passed. This is a manual recovery inspection, not native schedule evidence.

Snapshot #1481 recorded:

- Node `tce-k3s-01` Ready/ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`.
- Disk 56% (~21 GiB free), available RAM ~19 GiB, host uptime 191 days, `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1.
- Stock Admin has one `ImagePullBackOff` and one `ErrImagePull`; desired Backend remains `ImagePullBackOff` on `12d63b4`; legacy Backend/Frontend 1/1 on `23b2878`.
- TCE frontend/service, Auth and Keycloak 0/0.
- Media runner service active/enabled with `Runner.Listener` present.
- Stock/Media storage preflight clean (no target PVC/PV/VolumeSnapshot references), but external backup/retention, authoritative DNS/provider ownership and remote runner registration remain unverified.

No namespace or runner deletion is authorized.

## App-owned publication contracts

- Stock `deploy.yml` remains app-owned, native ARM64 and uses full-SHA plus version/full-SHA tags, verifies ARM64 manifests and digest equality for Scraper/Admin/Backend. Manual publication remains gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`. Its master push trigger ignores `.github/**`, so the workflow-only master change at `e6469ac6` did not itself trigger a publisher run; this is expected path-filter behavior, not evidence of a failed image build. No current-master publisher digest was observed. Registry-side GHCR tag immutability is not certified; promotion must remain digest-pinned.
- Stock scraper failure is independent: `VNSTOCK_API_KEY` is absent and the scheduled job stopped before installing dependencies. The owner must provide the key and run `preflight_only=true`; do not place the key in logs or use it as an image-publisher credential.
- Media master CI passes; no new publisher run. GitOps handoff remains retired. Runner retirement, audit token, external backup/retention and DNS evidence are outstanding.
- Auth master CI passes; PR #76 remains draft pending schema/migration and Supabase side-effect evidence. No new release/digest promotion.
- TCE has no new publisher/digest handoff. WF-06/WF-12 health failures reflect the zero-replica maintenance lanes and public 503s; no automatic scaling.

## Exact next actions

1. GitHub administrator: inspect native schedule event delivery and scheduler telemetry; require consecutive within-budget native runs without changing cron or budgets.
2. Stock owner: provide `VNSTOCK_API_KEY`, run safe preflight and confirm a current source SHA for ARM64 publication. Manual publication requires explicit release-variable approval.
3. TCE/Auth service owners: approve or reject a documented activation/recovery plan and rollback before any replica restoration.
4. Media owner/operator: verify idle state, stop/disable/unregister the runner, provide read-only audit token, and confirm external backup/retention plus authoritative DNS/provider ownership before protected decommission.
5. Auth/Supabase owner: continue PR #76 schema/migration drift and merge-trigger side-effect investigation; keep draft.
6. Platform operator: schedule host maintenance separately with rollback and retention evidence.

## Safety and ownership

- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance verification, GitOps promotion/reconciliation, rollout and health.
- In this run, Auth runtime Secret was provisioned/verified and GHCR access was checked; shared `ghcr-pull` was unchanged. Manifest apply, image promotion, rollout, workload scaling, Stock/Media restart, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation and host maintenance did not occur.
- No workflow was removed and no duplicate direct SSH/Compose production authority was added.
- TCE market-scan schedule unchanged.



## Inspection completion — 2026-11-09 05:01 ICT / 2026-11-08 22:01 UTC

The recovery-triggered read-only inspection #42527885366 completed successfully. Its snapshot was committed by inspection PR #1484, merged at `da24edc6019ac18be2f298eed06803848362aa68`; inspection validation #42528039006 passed. The snapshot was generated at `2026-11-08T21:59:12Z`, so it is fresh at this review. This was a `workflow_dispatch` inspection, not native schedule evidence.

Latest snapshot confirms:
- `tce-k3s-01` Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk 56% (~21 GiB free), available RAM ~19 GiB, host uptime 191 days and `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS remain 1/1.
- Stock Admin has one `ImagePullBackOff` and one `ErrImagePull`; desired Stock Backend remains `ImagePullBackOff` on `12d63b4`; legacy Backend/Frontend remain 1/1.
- TCE frontend/service, Auth and Keycloak remain 0/0.
- Media runner service remains active/enabled with `Runner.Listener` present.
- Stock/Media decommission preflight reports `storage-clean`: no target PVC/PV claims or VolumeSnapshot references. The snapshot explicitly says DNS ownership is not inferred and GitHub runner registration is not inferred by host inspection. External backup/retention evidence remains outstanding.

No decommission or host maintenance was performed. A fresh snapshot does not clear the runner, DNS or external-data gates.


## Latest cross-repo execution — 2026-11-09 06:01 ICT / 2026-11-08 23:01 UTC

### Repository heads and open pull requests

| Repository | Current master | Open PRs / state |
|---|---|---|
| Platform Infra | `6fe49e88255d9bfa5f1511b5a2f0c9280178e6a2` | #1314, #544, #541, #539 remain draft/human-decision PRs; inspection PR #1486 merged |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None |
| StockDividend | `4be26f41072ec8d749ea8b92f1a517c714d2a214` | #39 merged; #40 open, CI in progress |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 remains draft |

Platform #1486 is the latest inspection-only commit. It merged at `6fe49e88255d9bfa5f1511b5a2f0c9280178e6a2`; no production manifest was changed. Existing Platform planning/architecture drafts were not promoted or merged.

### Latest workflow and check evidence

| Repository / workflow | Latest relevant run | Result and meaning |
|---|---|---|
| Platform native reconcile | #42521088881, 20:37:39Z | PASS, but 15,672s inter-arrival gap vs 2,700s budget |
| Platform native inspection | #42530192980, 22:25:47Z | PASS; 14,280s gap vs 4,500s budget |
| Platform native recovery | #42520213983, 20:27:31Z | PASS; 15,605s gap vs 2,700s budget |
| Platform native watchdog | #42520452305, 20:30:24Z | FAIL; 15,517s gap vs 2,700s budget |
| Platform manual reconciliation | #42530382496, 22:28:12Z | PASS; preflight and drift check passed, manifest apply/image promotion/rollout skipped |
| Platform latest workflow_run | #42531502429, 22:41:43Z | SKIPPED; not native schedule evidence |
| TCE WF-06 native | #42531446260, 22:41:01Z | FAIL; all four public endpoint jobs failed; logs confirm TCE web/API and Auth readiness HTTP 503 |
| TCE WF-12 native | #42527713763, 21:56:51Z | FAIL; 14,317s inter-arrival gap vs 1,500s budget; heartbeat/recovery path is separate from native cadence |
| TCE WF-07 native integration | #42528513790, 22:06:09Z | PASS |
| StockDividend post-merge CI | #42533163812 | IN PROGRESS; four jobs passed, Scraper container and native ARM64 image builds still running at checkpoint |
| StockDividend PR #40 CI | #42533247153 | IN PROGRESS; syntax and release-contract jobs passed; build jobs still running |
| StockDividend scraper | #42457182511, 07:03:12Z | FAIL closed because `VNSTOCK_API_KEY` is absent; this is ingestion, not image publication |
| Media Generation CI | #42239703151 | PASS; no new current-master publisher run |
| Authentication CI | #42478653766 | PASS; no new release/digest handoff |

The Platform watchdog log reports: reconcile 15,672s, inspection 14,280s, recovery 15,605s and watchdog 15,517s. Native cadence remains outside budget even though the latest inspection completed. Do not substitute workflow_dispatch/workflow_run/repository_dispatch events for native schedule acceptance. Do not change cron expressions or freshness budgets. TCE WF-06 and WF-12 gaps also remain outside budget.

### StockDividend immutable publication contract

- PR #39, `feat(release): prevent overwriting immutable GHCR source tags`, merged by squash at `4be26f41072ec8d749ea8b92f1a517c714d2a214` after all seven exact-head CI jobs passed on `0f7bdd38244e556a9989897830acbb7864e987cb`.
- The publisher now checks all six full-SHA and version/full-SHA tags for Scraper/Admin/Backend before the first push, serializes by source SHA without cancelling an active publish, and keeps CI ARM64 builds non-publishing. This is workflow-level overwrite prevention, not GHCR server-side tag immutability; digest-pinned Platform promotion remains required.
- Post-merge master CI #42533163812 was still running at this checkpoint; no production publication was triggered by the workflow/script-only change (publisher path filters exclude these paths).
- Follow-up PR #40, head `78fe5bbffd97d999258df3a09a1e76c8d119e16b`, narrows missing-tag matching. It removes the unsafe generic `not found` match so ambiguous `repository not found` and HTTP 401 responses fail closed. PR CI #42533247153 was still running; do not merge until all required jobs pass on the current exact head.
- No current-master registry publication/digest evidence was created by either PR. Manual publication remains gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`.

### Latest K3s inspection — read-only

Inspection #42530192980 completed successfully and generated `debug/vps-latest.md` at `2026-11-08T22:25:55Z`; inspection PR #1486 merged as Platform master `6fe49e88255d9bfa5f1511b5a2f0c9280178e6a2`.

- Node `tce-k3s-01`: Ready/ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk 56% (~21 GiB free), available RAM ~19 GiB, host uptime 191 days, `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS: 1/1 Running with registry digests.
- Stock Admin ×2 and desired Backend on `12d63b4`: ImagePullBackOff/ErrImagePull; snapshot records no ARM64 match in registry manifests. Legacy Backend and Frontend remain 1/1 with RepoDigest.
- TCE frontend/service, Auth and Keycloak remain 0/0 maintenance. Public TCE and OIDC probes return HTTP 503.
- `stock-prod` and `media-prod` storage preflight is `storage-clean` (no target PVC/PV/VolumeSnapshot references), but both namespaces/workloads remain present.
- Media runner service remains active/enabled and `Runner.Listener` is present. Host inspection does not prove remote GitHub runner registration; authoritative DNS ownership and external backup/retention remain unverified.

### Reconciliation and preservation

Manual reconciliation #42530382496 ran with `ref=master`, `mode=apply`, `target_app=all`, `allow_image_changes=false`. Logs verify GHCR read access for Auth, MicroFE Shell/WS and TCE packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` remained unchanged; drift was false; manifest apply, image promotion and rollout were skipped. Auth's zero-replica maintenance lane was explicitly not asserted healthy; Keycloak lane was skipped.

App repositories continue to own tests/builds and immutable GHCR publication. Platform Infra remains the sole owner of production manifests, shared pull credentials, source/digest verification, GitOps promotion/reconciliation, rollout and health verification. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only.

### Exact next actions

1. Wait for post-merge Stock CI #42533163812 and PR #40 CI #42533247153; merge #40 only after verifying the exact current head and every required check.
2. Stock owner: provide `VNSTOCK_API_KEY`, run safe scraper preflight, and separately approve a current-source ARM64 publication. Do not treat the scraper key as a publisher credential.
3. GitHub administrator: investigate native schedule delivery/cadence; require consecutive within-budget native runs without changing cron or budgets.
4. TCE/Auth service owners: approve or reject a documented activation/recovery plan and rollback before any replica restoration.
5. Media owner/operator: stop/disable/unregister the Media runner and provide remote audit, external backup/retention and authoritative DNS ownership evidence before protected decommission.
6. Platform operator: plan host maintenance separately; no unattended reboot or package/containerd upgrade.

No image promotion, manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this execution. The authorized reconciliation did provision/verify the Auth runtime Secret; shared `ghcr-pull` was unchanged. No workflow was removed and no direct SSH/Compose production authority was added. TCE market-scan schedule unchanged.


## Stock publisher hardening merged — 2026-11-09 06:07 ICT / 2026-11-08 23:07 UTC

- Platform documentation PR #1487 merged at `28dbb1d7efa63c8e9ab62b5b6ccf51a2aa49007f`. Exact-head validation #42533385383 and post-merge validation #42533449555 both passed. The tracker/inventory checkpoint records the 06:01 cross-repo state and current K3s snapshot.
- StockDividend PR #39 merged at `4be26f41072ec8d749ea8b92f1a517c714d2a214`; its exact-head seven-job CI #42528788805 passed and post-merge master CI #42533163812 subsequently passed all seven jobs.
- StockDividend follow-up PR #40 merged at `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5` after exact-head CI #42533247153 passed all seven checks, including native ARM64 non-publishing builds. It removes the unsafe generic `not found` matcher; ambiguous `repository not found` and HTTP 401 now fail closed. This closes the registry-error-classification follow-up.
- Post-merge Stock CI #42533562194 was triggered on the new master and remained in progress at this checkpoint. It is a CI-only push run; no `deploy.yml` publisher run was triggered by the workflow/script-only changes. Do not claim post-merge CI complete until this run concludes.
- Stock master is now `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5`. No Stock production image publication, Platform handoff or GitOps promotion occurred.

Native Platform schedule evidence is unchanged: reconcile #42521088881 (15,672s gap/2,700s budget), inspection #42530192980 (14,280s/4,500s), recovery #42520213983 (15,605s/2,700s), watchdog #42520452305 (15,517s/2,700s, FAIL). TCE native WF-06 #42531446260 and WF-12 #42527713763 remain outside the 1,500s budget and fail; WF-06 public probes return HTTP 503. No cron or freshness budget change.

Platform #1487 post-merge validation passed; Platform master is `28dbb1d7efa63c8e9ab62b5b6ccf51a2aa49007f`. Open human-decision drafts remain Platform #1314/#544/#541/#539 and Auth #76; TCE, Stock and Media have no open PRs after Stock #40 merge.

No production manifest apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. Latest read-only K3s snapshot remains inspection #42530192980: node Ready/ARM64; Media/MicroFE 1/1 digest-pinned; Stock Admin×2 and desired Backend on `12d63b4` still ImagePullBackOff without ARM64 manifest; TCE/Auth/Keycloak 0/0; Media runner active/enabled/listener-present; Stock/Media storage preflight clean but external backup/retention, DNS ownership and remote runner registration unverified. Auth runtime Secret was provisioned/verified by reconciliation #42530382496; shared `ghcr-pull` unchanged; drift=false; apply/promotion/rollout skipped.

Exact next actions: (1) verify post-merge Stock CI #42533562194 to completion; (2) Stock owner supplies `VNSTOCK_API_KEY` and runs safe ingestion preflight separately from image publication; (3) GitHub administrator investigates native schedule delivery; (4) TCE/Auth owners decide activation/rollback; (5) Media owner completes runner, external-data and DNS evidence before protected decommission; (6) Platform operator schedules host maintenance separately. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only; TCE market-scan schedule unchanged.


---

## Latest cross-repo execution — 2026-11-09 07:08 ICT

The current checkpoint and evidence are archived in [2026-11-09-0708-ict.md](cross-repo-deployment-checkpoints/2026-11-09-0708-ict.md). Key changes since 06:07 ICT: Platform inspection PR #1489 merged at ecafca5f594f9984baa294ee679afed6afd245bb; fresh read-only K3s snapshot #42537975671 generated at 00:01:52Z and validation #42538111845 passed; Stock master CI #42533562194 is now confirmed PASS; TCE PR #1031 adds fail-closed GHCR tag preflight and is still under exact-head CI review. Native Platform/TCE schedule cadence remains outside budget. The full run IDs, gaps, runtime state, ownership boundaries and exact next actions are in the checkpoint.


## Post-checkpoint execution update — 2026-11-09 07:11 ICT / 00:11 UTC

TCE Dashboard PR #1031 was squash-merged at ddf5811a7994aab08236028cff04e0a78ffd2e3e after verifying the exact PR head 80c24eb1914bcfed924a3d90be4113294144b10d and all required PR checks. WF-01P #42538473285 passed, including the release-contract validator and mocked GHCR absence tests; WF-02 #42538473275 and WF-05 #42538473166 passed. The duplicate push runs #42538448641/#42538448647 also passed. The skipped PR auto-format step was non-blocking; the push auto-format run passed. No image publication or Platform dispatch occurred.

Post-merge TCE CI is now running on the new master SHA: WF-01 #42538802539, WF-02 #42538802538 and WF-05 #42538802541 were in progress at the last check. Do not mark the post-merge app CI lane green until all three finish. TCE WF-03 remains manual-only/master-only; the new tag guard only runs during an explicitly approved release and blocks existing/ambiguous tags before either GHCR push.

Platform tracker/inventory PR #1490 remains open at exact head c132840342d0c92859114eaea14fec899c268735. Exact-head validate-manifests #42538755907 passed before this post-checkpoint update; a new validation run is required after the update is committed. Platform master remains ecafca5f594f9984baa294ee679afed6afd245bb. No Platform production manifests or runtime state changed.

Native schedule gaps, K3s snapshot #42537975671, Stock/Media/Auth blockers and all safety boundaries remain as recorded in the 07:08 ICT checkpoint. TCE market-scan schedule unchanged.


## Cross-repo publisher guard update — 2026-11-09 07:18 ICT / 00:18 UTC

TCE Dashboard PR #1031 merged at ddf5811a7994aab08236028cff04e0a78ffd2e3e after exact-head validation. Its post-merge master CI is now fully green: WF-01 #42538802539 PASS, WF-02 #42538802538 PASS and WF-05 #42538802541 PASS. No TCE release was dispatched and no image was published.

Authentication PR #90 merged at 047abc08e123d8bde7678104899d00aa8782624a after exact-head PR CI #42539110908 passed. The CI log confirms 26 test suites/135 tests passed, typecheck/build passed, native ARM64 non-publishing build passed, and the Auth immutable GHCR preflight tests passed. Post-merge master CI #42539350154 was still in progress at the last check. Auth release remains manual-only; no image was published and no Platform dispatch occurred.

Media Generation PR #74 is open at exact head 5ed0d0bbf7bbd5942fa5a865f7e5c2de4ee72411. It adds a fail-closed pre-push guard for frontend/backend prod-vX.Y.Z-full-SHA tags, same-source non-cancelling concurrency, mocked negative tests, and paths-ignore for helper/test-only changes so they cannot trigger the production publisher. PR CI #42539297802 and push CI #42539276866 were still in progress. Media remains retired from Platform GitOps ownership; this PR does not change runtime/runner state or send a Platform dispatch.

The latest native Platform reconciliation is #42538596496 at 00:08:54Z, success. Its follow-on watchdog workflow_run #42538746501 failed native cadence acceptance. Updated observed gaps: reconcile 12,675s vs 2,700s; inspection 14,280s vs 4,500s; recovery 12,727s vs 2,700s; watchdog 12,672s vs 2,700s. TCE WF-06/WF-12 observations remain 13,481s/14,317s vs 1,500s. Inspection queue wait was 0m and no deployment lane exceeded 15m; no runner queue saturation evidence. Native schedule delivery remains a GitHub administrator blocker; cron and budgets are unchanged.

Reconciliation #42538596496 verified shared ghcr-pull unchanged, Auth runtime Secret present/verified with values suppressed, active MicroFE/TCE scopes without image-pull failures, drift=false, apply skipped and image changes disabled. Auth remains intentional 0/0; no live Auth health was asserted. Latest K3s snapshot remains read-only inspection #42537975671 at 00:01:52Z; no newer snapshot was committed in this delta.

Platform docs PR #1490 was validated at head 914f5abef2a3f5da65791d05dcc51042a2ba8dc5 by #42538879776 PASS before this delta. The new tracker/inventory/checkpoint commit requires a fresh exact-head validation before merge. Platform master remains ecafca5f594f9984baa294ee679afed6afd245bb. TCE market-scan schedule unchanged.


## Media guard merge update — 2026-11-09 07:20 ICT / 00:20 UTC

Media Generation PR #74 was squash-merged at dcd698699c65ba6e73f6b43838975144777131c3 after exact-head validation on 5ed0d0bbf7bbd5942fa5a865f7e5c2de4ee72411. PR CI #42539297802 passed; logs confirm the Media release-contract validator and mocked immutable-tag preflight tests passed. Post-merge Media CI #42539512417 was still in progress; its release-contract validation step had passed and dependency installation was running. The helper/test-only paths are excluded from the production publisher trigger; no Media image publication or Platform dispatch occurred.

Authentication post-merge CI #42539350154 completed successfully on master 047abc08e123d8bde7678104899d00aa8782624a. Auth PR #90 remains merged; no Auth release was dispatched. TCE post-merge CI remains fully green on ddf5811a7994aab08236028cff04e0a78ffd2e3e. Stock post-merge CI #42533562194 remains PASS 7/7.

Platform documentation PR #1490 currently includes the 07:18 checkpoint. Its latest exact-head validation #42539467189 was running on head c4f36d0db6f5ddb8f25b53baba1c3183a17ac066 before this delta; the new checkpoint/inventory commit requires another exact-head validation. Platform master remains ecafca5f594f9984baa294ee679afed6afd245bb. No production state changed. TCE market-scan schedule unchanged.


---

## Cross-repo completion checkpoint — 2026-11-09 07:22 ICT

Platform PR #1490 merged at dd1bca11e3c59c92f920ec5e4896fb8d643be272; exact-head validation #42539583925 and post-merge validation #42539638207 passed. TCE #1031, Auth #90 and Media #74 publisher guards are merged; their post-merge CI runs all passed. Stock #39/#40 guards remain merged and master CI #42533562194 passed 7/7. The full current heads, open PRs, schedule gaps, K3s snapshot, reconciliation evidence, owner blockers and safety boundaries are recorded in [2026-11-09-0722-ict.md](cross-repo-deployment-checkpoints/2026-11-09-0722-ict.md). Native Platform/TCE schedule cadence remains outside budget; no cron/freshness change. TCE market-scan schedule unchanged.


## Cross-repo execution — 2026-11-09 07:57 ICT / 2026-11-09 00:57 UTC

### Current repository and workflow state

- Platform Infra master is `2ab93d7736f520383764b9cb0f739d98a6696f58`; latest master validation #42539863349 PASS. Open human-decision drafts #1314/#544/#541/#539 remain unmerged.
- TCE Dashboard master is `ddf5811a7994aab08236028cff04e0a78ffd2e3e`; no open PRs. Its post-merge CI #42538802539/#42538802538/#42538802541 passed. Native WF-06 #42531446260 and WF-12 #42527713763 still fail.
- StockDividend master is `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5`; CI #42533562194 passed. Scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was empty; no secret was changed.
- Media Generation master is `dcd698699c65ba6e73f6b43838975144777131c3`; post-merge CI #42539512417 passed. No runner/runtime or Platform ownership change occurred.
- Authentication master is `047abc08e123d8bde7678104899d00aa8782624a`; CI #42539350154 passed. PR #76 remains draft.
- App-owned workflow-level GHCR tag guards are merged in Stock #39/#40, TCE #1031, Auth #90 and Media #74. These guards prevent workflow-level tag overwrites but are not GHCR server-side immutable-tag enforcement; registry digest verification and digest-pinned Platform promotion remain mandatory.

### Native schedule acceptance — still blocked

| Workflow | Latest native event | Previous native event | Observed gap | Existing budget |
|---|---|---|---:|---:|
| Platform reconcile | #42538596496, 00:08:54Z, success | #42521088881, 20:37:39Z | 12,675s | 2,700s |
| Platform inspection | #42530192980, 22:25:47Z, success | #42510125328 | 14,280s | 4,500s |
| Platform recovery | #42537793367, 23:59:38Z, success | #42520213983, 20:27:31Z | 12,727s | 2,700s |
| Platform watchdog | #42537967026, 00:01:36Z, failure | #42520452305, 20:30:24Z | 12,672s | 2,700s |
| TCE WF-06 | #42531446260, 22:41:01Z, failure | #42512468931, 18:56:20Z | 13,481s | 1,500s |
| TCE WF-12 | #42527713763, 21:56:51Z, failure | #42507582654, 17:58:14Z | 14,317s | 1,500s |

TCE WF-06 job logs confirm HTTP 503 from TCE web, TCE API, Auth readiness and Auth liveness. WF-12's heartbeat job succeeded but its WF-06 schedule-delivery verification failed. Platform inspection queue wait telemetry was 0m in the latest watchdog evidence; there is no demonstrated runner-queue saturation cause. Manual, push, workflow_run and repository_dispatch events do not count as native schedule acceptance. Do not alter cron expressions or freshness budgets; GitHub administrator investigation remains required.

### Last known K3s state — stale snapshot, not current health

The latest committed read-only snapshot is inspection #42530192980, generated at 22:25:55Z. At 00:57Z it is about 151 minutes old, beyond the 75-minute snapshot budget. It last showed node `tce-k3s-01` Ready/ARM64, disk 56% (~21 GiB free), RAM ~19 GiB available and host uptime 191 days. Media backend/frontend and MicroFE Shell/WS/NATS were 1/1; Stock Admin×2 and desired Backend remained ImagePullBackOff on tags without a matching ARM64 manifest; TCE/Auth/Keycloak remained 0/0. Treat this as historical evidence only until a new inspection completes.

The last recorded reconciliation #42538596496 succeeded with no GitOps drift; shared `ghcr-pull` remained unchanged, Auth runtime Secret was verified, and manifest apply, image promotion and rollout were skipped. No newer production apply or rollout is evidenced in the current run history.

### New deployment contract under review

Branch `fix/gitops-promotion-dispatch-provenance-20261109-0757-ict` adds a fail-closed second-stage contract for the production-capable `gitops-promoted-ready` event:

- MicroFE, TCE and Auth promotion producers attach full app source SHA plus the originating Platform promotion run ID/attempt, workflow path and head SHA.
- `reconcile-vps.yml` reads Actions metadata and waits for that exact promotion run to complete successfully on master before it can proceed with repository-dispatch apply/image-change behavior.
- `scripts/verify-gitops-ready-dispatch.py` allowlists only Auth/TCE/MicroFE, validates component/release/source-SHA binding, rejects unknown payload keys, and verifies the exact run ID, attempt, workflow path, master branch, head SHA, event, completed status and success conclusion.
- The validator has 4 positive and 20 negative self-test cases. The existing GitOps promotion workflow remains the only producer of these ready events. The new read-only helper is excluded from recovery push bootstrap, and GitHub Actions CI executes its regression tests.
- The change is still on a dedicated branch and has not been applied to production. Exact-head CI and manifest validation must pass before merge.

### Exact next actions and safety boundary

1. Validate the exact head of the GitOps dispatch-provenance PR; merge only if all required checks pass on the current head.
2. GitHub administrator: investigate native schedule event delivery without changing cron or budgets.
3. Stock owner: provide `VNSTOCK_API_KEY`, run the safe scraper preflight, then separately approve an ARM64 publication from a current source SHA.
4. TCE/Auth owners: approve or reject a documented recovery/rollback plan before any replica restoration; 0/0 is not live health.
5. Media owner/operator: stop/disable/unregister the runner and provide remote audit, external backup/retention and authoritative DNS ownership evidence before protected decommission.
6. Platform operator: plan host maintenance separately with a maintenance window and rollback; no unattended reboot/upgrade.

No image publication, image promotion, manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred in this execution. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority was added. TCE market-scan schedule unchanged.


## Post-merge follow-up — 2026-11-09 08:10 ICT / 01:10 UTC

- Platform PR [#1492](https://github.com/phanthienquoc/platform-infra/pull/1492) was squash-merged at exact head `e1d55deb801a1c081cdb7591ac5cd90e57840cb7`, producing master `a614b3a6549cdccd2d5f2c9af3e86245df5a58ce`.
- Exact-head checks all passed: `validate-manifests` #42543963303, `validate-github-actions` #42543963257 and `keycloak-ci` #42543963209.
- Post-merge checks all passed: `validate-manifests` #42544069779, `validate-github-actions` #42544069795 and `keycloak-ci` #42544069796.
- A second review found that a successful workflow-run envelope alone could still describe a no-op promotion workflow whose app-specific promotion job was skipped. Dedicated branch `fix/gitops-promotion-job-attestation-20261109-0812-ict` now requires the expected promotion job(s) to be completed-successful: MicroFE digest promotion; both TCE paired promotion and coordinator; or Auth promotion. PR #1493 also resolves the current GitOps manifest's digest-pinned images, verifies the immutable source tag resolves to each exact manifest digest, and re-reads the digest reference through the existing GHCR ARM64 verifier before any runtime Secret or shared pull-credential mutation. Auth/TCE manifests currently remain tag-pinned until a successful digest promotion is merged, so a ready event fails closed until that state is corrected.
- The dispatch validator has 4 positive and 23 negative self-test cases, including skipped/missing/failed app-specific promotion jobs. A second image-reference validator covers 5 positive digest extractions and 6 negative cases. The reconcile preflight fetches the exact Actions jobs endpoint, then validates the current digest-pinned manifest against GHCR tag-to-digest and ARM64 evidence. No production event or reconciliation was dispatched.

### Schedule and runtime status at this checkpoint

No newer native Platform or TCE schedule events appeared after the recorded runs through 01:10Z. Latest Platform native reconcile #42538596496 (00:08:54Z), inspection #42530192980 (22:25:47Z), recovery #42537793367 (23:59:38Z) and watchdog #42537967026 (00:01:36Z) remain outside freshness/cadence expectations; watchdog is failed. TCE WF-06 #42531446260 and WF-12 #42527713763 remain failed. Do not count post-merge CI, workflow_run or recovery dispatches as native schedule acceptance.

Latest committed K3s snapshot #42530192980 (22:25:55Z) is stale; no new inspection or production rollout was triggered. Last known reconciliation #42538596496 was no-drift and skipped apply/promotion/rollout. Stock scraper still lacks `VNSTOCK_API_KEY`; TCE/Auth remain intentional 0/0; Media runner and external backup/DNS evidence remain owner-blocked.

No cron/freshness change, production image publication/promotion, manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


## PR #1493 extension — manifest and registry digest binding — 2026-11-09 08:14 ICT

A further review closed the replay/tampering gap between a successful promotion job and the release values supplied in the ready-event payload. The repository-dispatch preflight now also:

1. Resolves the expected image set from the app allowlist: Auth (1 image), TCE (web + service) or MicroFE (shell + WS).
2. Requires exactly one digest field per expected image in the current GitOps Kustomize manifest; a `newTag`-only entry, duplicate image/digest, missing entry or malformed digest fails closed.
3. Binds Auth/TCE release tags to the full source SHA and MicroFE's release label to the source SHA prefix, while using the full source SHA as the MicroFE registry tag.
4. Calls the existing `validate-ghcr-image-reference.sh` for each immutable source tag with `GHCR_EXPECTED_DIGEST`, then for the digest reference itself. This revalidates exact registry mapping and `linux/arm64` availability.
5. Runs after the read-only GHCR access preflight and before Auth runtime Secret provisioning or shared `ghcr-pull` mutation.

The helper initially had 5 positive extraction and 6 negative contract cases and is included in GitHub Actions regression tests. It is excluded from recovery push bootstrap. PR #1493 was subsequently squash-merged at `891a07c06bc541f2df420d6d085d77f49121602d`; the statement that it remained unmerged was only true at this historical 08:14 checkpoint. No production event, registry write, manifest apply or rollout was executed by that change.


## Manifest image identity hardening — 2026-11-09 10:04 ICT / 03:04 UTC

### PR #1500 — squash-merged and exact-head validated

[PR #1500](https://github.com/phanthienquoc/platform-infra/pull/1500) was squash-merged at `640eab00e13ff1460c47f394138598da98e096cb` from exact head `046d323593c0546a5119895c77ff945456874b54`, based on master `c0c4417c8b317ced59444d61d2671edf879f646a`.

Review found that `verify-gitops-ready-image-refs.py` verified the digest for each allowlisted `- name:` but did not bind optional Kustomize `newName:` to that same repository and did not reject additional image entries in the manifest. A `newName` override could therefore redirect the rendered image while the preflight verified the original GHCR repository.

The merged change adds:
- Exactly one `images:` section and an exact per-app image-name set; missing, duplicate, malformed or unexpected image entries fail closed.
- Optional `newName:` must equal the allowlisted repository; duplicate, malformed or redirected overrides fail closed.
- Regression coverage expands from 5 positive / 6 negative to 5 positive / 12 negative cases.
- Workflow-contract validation asserts the image-set and repository-identity checks remain present. The existing GitHub Actions workflow runs the helper self-test.

Exact-head validation on SHA `046d323593c0546a5119895c77ff945456874b54`: `validate-github-actions` #42555164957 PASS (including actionlint, yamllint, shellcheck, ops regression, 5 positive/12 negative image-ref tests and workflow-contract validation); `validate-manifests` #42555164890 PASS. PR mergeability was true and squash merge used the exact expected head. No post-merge workflow run was available in this inspection, so post-merge validation remains pending.

Current master Auth and TCE manifests are still tag-pinned before a release promotion; the authenticated ready-event gate intentionally rejects them until the app-specific promotion workflow has merged digest-pinned manifest changes. MicroFE is already digest-pinned. This PR changes only read-only validation and does not alter normal scheduled reconciliation.

### Current cross-repo evidence and blockers

- Platform master at branch base: `c0c4417c8b317ced59444d61d2671edf879f646a`; open human-decision drafts #1314/#544/#541/#539 remain unmerged. New PR #1500 is validation-only.
- TCE master `ddf5811a7994aab08236028cff04e0a78ffd2e3e`; Stock master `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5`; Media master `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication master `047abc08e123d8bde7678104899d00aa8782624a`. App publisher guards remain merged; no production publication is evidenced.
- Native schedule delivery remains tracked by issue [#1497](https://github.com/phanthienquoc/platform-infra/issues/1497). Do not change cron expressions, freshness budgets or TCE market-scan scheduling. Fallback dispatches do not count as native schedule acceptance.
- Latest recorded K3s inspection remains #42548015626 (generated 01:54:48Z); it is stale for current readiness. No new rollout or health claim is made. Last known reconciliation #42546651537 was workflow_dispatch, not native schedule; it provisioned/verified Auth runtime Secret, left shared `ghcr-pull` unchanged, found no drift and skipped manifest apply, image promotion and rollout.
- Stock still needs `VNSTOCK_API_KEY` and an owner-approved ARM64 publication; TCE/Auth remain intentional 0/0 pending service-owner recovery/rollback approval; Media runner retirement remains blocked by remote registration, backup/retention and DNS evidence.

No production image publication/promotion, manifest apply, workload scaling, credential mutation, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Post-merge follow-up — 2026-11-09 10:12 ICT / 03:12 UTC

Platform PR [#1500](https://github.com/phanthienquoc/platform-infra/pull/1500) was squash-merged at `640eab00e13ff1460c47f394138598da98e096cb` from exact head `046d323593c0546a5119895c77ff945456874b54`. Exact-head `validate-github-actions` #42555164957 and `validate-manifests` #42555164890 both completed successfully. The GitHub Actions log confirms the GitOps image-ref helper passed 5 positive extraction and 12 negative contract cases, and `validate-workflow-contracts.py` passed. Master now contains the exact image-set and `newName` repository-binding checks. No post-merge run was visible during this inspection; do not claim post-merge validation yet.

Current Platform master: `640eab00e13ff1460c47f394138598da98e096cb`. Open human-decision drafts remain #1314/#544/#541/#539; Auth PR #76 remains draft. The docs follow-up branch `docs/cross-repo-post-merge-1500-20261109-1012-ict` records this checkpoint.

The Auth and TCE production manifests remain tag-pinned at master until their app-specific digest promotion jobs run and merge. Their authenticated ready events remain fail-closed until the digest-pinned manifest is present and registry tag-to-digest/ARM64 checks pass. MicroFE is already digest-pinned. This does not affect normal scheduled reconciliation.

No production image publication/promotion, manifest apply, workload scaling, credential mutation, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## Execution checkpoint — 2026-11-09 11:00 ICT / 04:00 UTC

### Current repository heads and open pull requests

| Repository | Current master | Open PRs |
|---|---|---|
| Platform Infra | \`f23f272a746dd1991f868630c57c914f2ebac1b4\` | #1314, #544, #541, #539 (all draft / human decision) |
| TCE Dashboard | \`ddf5811a7994aab08236028cff04e0a78ffd2e3e\` | None |
| StockDividend | \`1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5\` | None |
| Media Generation | \`dcd698699c65ba6e73f6b43838975144777131c3\` | None |
| Authentication | \`047abc08e123d8bde7678104899d00aa8782624a\` | #76 (draft / migration decision) |

Open Platform draft heads were inspected: #1314 \`db152c9a17416d1a7f82165597dfe478321bd055\`, #544 \`c95e7daecb83b65577b54303427fe4ea81adfe06\`, #541 \`b8f7c6ba04e3d971336a899b2efd5894662083b3\`, and #539 \`2dc48b97017ecb08e49682633303a2f1d5e991a1\`. Their visible PR-triggered manifest validations (#42161859747, #38575430454, #38567431761 and #38548718033 respectively) completed successfully, but all remain drafts and are not deployment approval. Authentication #76 head \`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58\` has visible CI #41329425940 PASS; it also remains draft. No draft was merged.

### PR #1502 — root-scoped GitOps image parsing

[PR #1502](https://github.com/phanthienquoc/platform-infra/pull/1502) was squash-merged at \`f23f272a746dd1991f868630c57c914f2ebac1b4\` from exact head \`51dd0b5e1c1bc804a0a24b4b57437175f19176f7\`, based on master \`26c22833a1485f7aef92dbb944d02479b85ae034\`.

Review found that the previous image-ref validator searched all \`- name:\` lines after finding an \`images:\` line. A root \`images:\` section could be empty while an image-shaped item under a different Kustomize section was counted as an image transformer. The ready-event preflight could therefore extract a digest from the wrong section.

The merged parser now:
- Requires exactly one root-level \`images:\` section.
- Parses only direct image entries within that section; unrelated \`- name:\` items in \`configMapGenerator\` and other sections are ignored.
- Rejects nested/mis-scoped entries, empty image blocks, unsupported fields, duplicate fields and malformed indentation.
- Keeps exact per-app allowlists, \`newName\` repository binding, one tag/digest pin per image and digest-only acceptance for ready events.
- Adds one positive section-isolation case and four additional negative cases (5 positive extraction, 1 scope-isolation, 16 negative cases).

Exact-head validation on \`51dd0b5e1c1bc804a0a24b4b57437175f19176f7\`:
- \`validate-github-actions\` #42559803093 — PASS (actionlint, yamllint, shellcheck, ops regression, path-scoped deployment tests, image-change tests and workflow-contract checks).
- \`validate-manifests\` #42559803103 — PASS (Kustomize render, Auth contract, secret policy, immutable image policy, isolated Keycloak and network boundaries).

The earlier superseded head \`11ec4a907795a449c76a87b17a7f3b9af19b1f9e\` failed #42559716184 because the direct \`extract_digest\` self-test did not independently reject a redirected \`newName\`; that guard was restored on the final head and the exact-head checks passed. The final merge was protected by expected-head SHA and used squash. The connector exposes PR-triggered runs only; no post-merge push run or post-merge combined status was available for the merge SHA at this checkpoint. Do not claim post-merge CI PASS until independently observed.

### Cross-repo publication and GitOps state

- App-owned workflow-level GHCR overwrite guards remain merged in StockDividend #39/#40, TCE #1031, Authentication #90 and Media #74. They are not GHCR server-side immutable-tag enforcement. No production image publication or digest handoff is evidenced in this checkpoint.
- Platform remains sole owner of production manifests, shared GHCR pull credentials, promotion provenance/digest/ARM64 verification, GitOps reconciliation, rollout and health.
- StockDividend and Media Generation remain retired from active Platform GitOps ownership; their app repositories and packages are not deleted.
- Current Auth and TCE production Kustomize overlays remain tag-pinned; the authenticated GitOps-ready event requires a digest-pinned manifest and exact source-tag-to-digest/ARM64 evidence, so their ready events remain fail-closed until promotion merges. MicroFE remains digest-pinned.
- Last known reconciliation evidence remains workflow_dispatch #42546651537 (not native schedule): GHCR read access passed, Auth runtime Secret was provisioned/verified, shared \`ghcr-pull\` was unchanged, drift was false, and manifest apply/image promotion/rollout were skipped. This is not a fresh runtime check.

### Native schedules and runtime evidence

- Native schedule investigation remains open in [issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497). Its last authoritative native evidence recorded in the issue is through 01:59 UTC on 2026-11-09; no newer all-event schedule listing is exposed by the current connector. Schedule recovery is therefore unproven. Do not treat PR/push/workflow_dispatch/recovery events as native acceptance.
- Preserve every existing cron expression and freshness budget. No TCE market-scan schedule change.
- The current \`debug/vps-latest.md\` was generated at \`2026-11-09T01:54:48Z\`; at this checkpoint it is over three hours old and stale for rollout/decommission authorization. It last reported ARM64 node Ready, disk 56% (~21 GiB free), available RAM ~19 GiB and \`restart_required=yes\`.
- That snapshot reported Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin×2 and desired Backend on \`12d63b4\` ImagePullBackOff due to missing ARM64 manifest; legacy Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0. Public OIDC probes returned 503; 0/0 is maintenance, not live health.
- The dedicated Media runner service was active/enabled with \`Runner.Listener\` present. In-cluster Stock/Media PVC/PV/VolumeSnapshot preflight was clean, but this does not prove external database/object-storage backups, retention or DNS/provider ownership. The remote Media runner registration still requires the read-only audit-token check.
- The protected \`decommission-stock-media.yml\` delete path was not run. It remains blocked by runner retirement/remote absence, external backup/retention review, authoritative DNS ownership review, fresh same-window storage plan, exact typed confirmations and protected production Environment approval.

### Exact next actions

1. GitHub administrator: investigate native schedule delivery under issue #1497; provide authoritative delayed/dropped/enqueue evidence without changing cron or budgets.
2. Stock owner: provide \`VNSTOCK_API_KEY\`, run authenticated safe \`preflight_only=true\`, approve a current full-source-SHA ARM64 publication, and capture registry digest evidence before any Platform promotion.
3. TCE/Auth owners: approve recovery/rollback plans; complete app-owned digest publication and Platform digest-promotion PRs before ready-event activation or replica restoration.
4. Media owner/operator: verify the dedicated runner is idle, stop/disable/unregister only that runner, retain required logs, verify remote absence with \`MEDIA_RUNNER_AUDIT_TOKEN\`, and independently confirm external backup/retention and authoritative DNS ownership. Preserve the shared Platform runner.
5. Platform operator: obtain a fresh read-only K3s inspection before any decommission decision; host package/reboot maintenance remains a separate approved window.

No production image publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred in this checkpoint. \`reconcile-vps.yml\` remains the sole production apply authority; \`inspect-vps.yml\` remains read-only. No direct SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Execution checkpoint — 2026-11-09 12:02 ICT / 05:02 UTC

### Repository state, pull requests and latest checks

All five default branches were re-read. Current master heads:

| Repository | Master SHA |
|---|---|
| Platform Infra | 4e5d77df98fd86adac8670170440c0201d6f2be5 |
| TCE Dashboard | ddf5811a7994aab08236028cff04e0a78ffd2e3e |
| StockDividend | 1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5 |
| Media Generation | dcd698699c65ba6e73f6b43838975144777131c3 |
| Authentication | 047abc08e123d8bde7678104899d00aa8782624a |

Open PRs were re-read with current metadata:
- Platform Infra #1314, #544, #541 and #539 remain open drafts; these are mail/Keycloak/identity human-decision items and were not merged.
- Authentication #76 remains an open draft for migration-drift planning.
- TCE Dashboard, StockDividend and Media Generation have no open PRs.

Latest visible master CI evidence:
- Platform PR #1502 post-merge: validate-github-actions #42559897903 PASS; validate-manifests #42559897980 PASS. Platform PR #1503 documentation post-merge validate-manifests #42560097448 PASS. The #1502 exact-head runs #42559803093/#42559803103 also PASS.
- TCE master WF-05 #42538802541 PASS. Latest native WF-06 #42548397383 FAIL; native WF-12 #42546629459 FAIL.
- StockDividend master CI #42533562194 PASS (7/7). Scheduled scraper #42457182511 fails at “Require VNStock API key before installing dependencies”; Python setup, dependency installation, entitlement check and scraping were correctly skipped. No secret value was exposed or changed.
- Media Generation master CI #42539512417 PASS.
- Authentication master CI #42539350154 PASS.
- All four app-owned GHCR pre-push guard changes remain merged. These are workflow-level overwrite guards, not GHCR server-side immutable-tag enforcement. No new production publication or digest handoff is evidenced.

### Native schedule evidence at 2026-11-09 05:02:47 UTC

The Actions API was queried with event=schedule for Platform Infra and TCE Dashboard. No newer native run was returned for any of these six workflows; non-schedule events were excluded.

| Workflow | Latest native run | Last event UTC | Gap at checkpoint | Budget |
|---|---:|---:|---:|---:|
| Platform reconcile | #42538596496 | 00:08:54 | 17,633s | 2,700s |
| Platform inspection | #42548015626 | 01:54:40 | 11,287s | 4,500s |
| Platform recovery | #42537793367 | Nov 8 23:59:38 | 18,189s | 2,700s |
| Platform watchdog | #42537967026 | 00:01:36 | 18,071s | 2,700s |
| TCE WF-06 | #42548397383 | 01:59:09 | 11,018s | 1,500s |
| TCE WF-12 | #42546629459 | 01:38:28 | 12,259s | 1,500s |

All six are outside their existing budgets. Platform issue #1497 received a new evidence comment (comment ID 6732680029) requesting authoritative GitHub Actions scheduler delivery evidence. The issue remains open and administrator-owned. Do not infer runner saturation: the available previous queue telemetry was zero minutes. Do not change cron expressions, freshness budgets or TCE market-scan scheduling.

TCE WF-06 #42548397383 job evidence confirms all four public probes failed: Auth readiness, Auth liveness, TCE API and TCE web. This is service-health failure distinct from scheduler delivery. TCE/Auth intentional 0/0 maintenance is not live health; do not weaken strict probes or restore replicas without service-owner approval.

### Latest K3s evidence and freshness

The tracked debug/vps-latest.md (blob 30399ae4a266af8b9341a7ae980e3dfd43b884fa) and scheduled inspection #42548015626 were generated at 2026-11-09T01:54:48Z. At 05:02:47Z this evidence is 3h07m59s old and is stale for rollout/decommission authorization. No fresh inspection could be dispatched through the available GitHub read/write actions in this run.

Last observed host/node state:
- K3s v1.36.3+k3s1, ARM64 Ubuntu 22.04.5; node Ready.
- Disk 56%, approximately 21 GiB free; available RAM approximately 19 GiB.
- restart_required=yes; Docker reclaimable approximately 5.773 GB; containerd.io 2.4.2-3 available versus installed 2.2.1-1.
- Platform and dedicated Media runner services both active/enabled; Media Runner.Listener process present.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1 with digest evidence.
- Stock Admin x2 and desired Backend tag 12d63b4 remain ErrImagePull/ImagePullBackOff with no imageID. Legacy Backend/Frontend are 1/1, but the old Backend imageID is not a registry RepoDigest proof.
- TCE/Auth/Keycloak remain 0/0 in maintenance. Stock/Media namespaces and pods remain present.
- The snapshot is not current runtime health and does not authorize maintenance, deletion or rollout.

### GitOps and ownership

- Platform PR #1502’s root-scoped image parser and exact image allowlist/repository binding passed exact-head and post-merge checks.
- Auth and TCE production overlays remain tag-pinned until app-owned digest publication and Platform digest-promotion PRs are completed. Their ready-event gate must remain fail-closed. MicroFE remains digest-pinned.
- StockDividend and Media Generation remain retired from active Platform GitOps ownership; their repositories and workloads are not thereby deleted.
- Last known reconciliation #42546651537 was workflow_dispatch, not native schedule: Auth runtime Secret was provisioned/verified, shared ghcr-pull unchanged, drift=false, manifest apply/image promotion/rollout skipped. This is not a fresh reconciliation or rollout.
- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only. No duplicate SSH/Compose deployment authority.

### Exact next actions

1. GitHub administrator: provide authoritative schedule-event delivery/enqueue evidence for issue #1497; preserve cron and budgets.
2. Platform operator: obtain a fresh read-only K3s inspection before any rollout/decommission decision; schedule host package/reboot maintenance separately with rollback.
3. Stock owner: provide VNSTOCK_API_KEY, run safe authenticated preflight, approve full-source-SHA ARM64 publication and provide registry digest evidence before Platform promotion.
4. TCE/Auth owners: approve recovery/rollback plans, publish current app-owned images, merge digest-pinned promotion PRs, then verify health before any replica restoration.
5. Media owner/operator: audit idle state and remote registration, stop/disable/unregister only the dedicated Media runner after approval, retain logs, and verify external backup/retention and authoritative DNS ownership. Preserve the shared Platform runner.

No production image publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host reboot/upgrade occurred in this checkpoint. TCE market-scan schedule unchanged.
