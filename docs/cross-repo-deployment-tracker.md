# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 07:01 ICT (2026-11-05 00:01 UTC)
Platform Infra master at checkpoint: 8170761b5d9cc98bfeec291294ef9e1f4c21bac2

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | 8170761b5d9cc98bfeec291294ef9e1f4c21bac2 | #1222, #544, #541, #539 (all draft) | Native inspection #41934713847 (event=schedule) PASS at 06:33:56 ICT; snapshot PR #1246 merged as 3bc0921. PR #1247 added a native-recovery-event regression guard; exact-head lint #41938079392 and validate #41938079362 PASS. Post-merge push validations #41938159895/#41938159872 were queued at checkpoint. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d | None | Native WF-07 Backup #41936628258 PASS at 06:48:44 ICT. Native WF-06 #41932031987 FAIL at 06:13:49 ICT: TCE API/web and Auth liveness/readiness all HTTP 503. Native WF-12 #41928632194 FAIL at 05:49:42 ICT; workflow_run #41932063303 PASS at 06:14:02 ICT for heartbeat/delivery forwarding, not native schedule evidence. |
| phanthienquoc/stockdividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Scraper/Admin/Backend full-source-SHA images have verified linux/arm64 digests. Publisher explicitly keeps production GitOps promotion disabled; handoff validation and paired digest dispatch are SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None | Media CI #41617592783 PASS. Latest inspected runtime has backend/frontend 1/1 with digest-pinned imageIDs. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft | Auth service CI #41670642852 PASS. PR #75/#76 last exact-head validation runs #40446492086/#41329425940 PASS but historical; Supabase Preview remains SKIPPED and migration/production gate remains closed. |

Current Platform Infra PR heads and last returned validation runs:
- #1222 draft, head f018e39eda52770539fc10671fba0d04baec8046; validate-manifests #41821355040 PASS. The PR remains unsafe for deployment: it still proposes Docker/Kubernetes mutation tools, the previously reviewed source/installer newline defects and missing SHELL_UID/GID forwarding remain unresolved, and reproducible build/tests/lockfile evidence is absent.
- #544 draft, head c95e7daecb83b65577b54303427fe4ea81adfe06; validate-manifests #38575430454 PASS.
- #541 draft, head b8f7c6ba04e3d971336a899b2efd5894662083b3; validate-manifests #38567431761 PASS.
- #539 draft, head 2dc48b97017ecb08e49682633303a2f1d5e991a1; validate-manifests #38548718033 PASS.
- #1247 merged at master SHA 8170761b5d9cc98bfeec291294ef9e1f4c21bac2 after exact-head lint/validate PASS. Its post-merge push validations were still queued at checkpoint.
- The older PR-associated runs listed above are historical evidence, not new production-health evidence.

Current Platform Infra PR heads and last returned validation runs:
- #1222 draft, head f018e39eda52770539fc10671fba0d04baec8046; validate-manifests #41821355040 PASS. The PR remains unsafe for deployment: it still proposes Docker/Kubernetes mutation tools, the previously reviewed source/installer newline defects and missing SHELL_UID/GID forwarding remain unresolved, and reproducible build/tests/lockfile evidence is absent.
- #544 draft, head c95e7daecb83b65577b54303427fe4ea81adfe06; validate-manifests #38575430454 PASS.
- #541 draft, head b8f7c6ba04e3d971336a899b2efd5894662083b3; validate-manifests #38567431761 PASS.
- #539 draft, head 2dc48b97017ecb08e49682633303a2f1d5e991a1; validate-manifests #38548718033 PASS.
- These are the last PR-associated runs returned for the exact heads, not new post-merge or production-health evidence. Combined-status lookup returned no status contexts for the current master heads.

## Current actions

1. PR #1242 merged the recovery event-classification fix. Recovery now separates native event=schedule evidence from workflow_dispatch fallback activity and ignores reruns. Exact-head #41923196096/#41923196112 and post-merge #41923323345/#41923323244 all PASS.
2. A post-merge native inspection cycle is now directly confirmed: #41934713847 ran with event=schedule at 23:33:56Z (06:33:56 ICT), succeeded, generated a read-only snapshot, and created inspection PR #1246. PR #1246 merged its exact snapshot head as master SHA 3bc0921c4e1e753356c1930a26cd0cf0ab3a9e2d. This proves inspect-vps native delivery resumed; it does not prove native recovery, reconcile or watchdog schedules resumed.
3. PR #1247 added a regression guard requiring the watchdog recovery query to use event=schedule on master, rejecting fallback-event filters. Exact-head lint #41938079392 and validate #41938079362 PASS; PR #1247 squash-merged as 8170761b5d9cc98bfeec291294ef9e1f4c21bac2. Post-merge validations #41938159895/#41938159872 were queued at checkpoint.
4. The watchdog workflow_run #41934894419 correctly failed recovery freshness: latest native scheduled recovery #41914511298 was 138 minutes old, beyond the 45-minute budget. The recovery workflow_run #41934894417 succeeded after inspection #41934713847, but workflow_run success is not native schedule evidence and does not clear the recovery cron blocker.
5. Keep verifying native Platform schedule delivery independently for inspect-vps, reconcile-vps, recover-stale-ops and reconcile-schedule-watchdog. Do not count workflow_dispatch, workflow_run, repository_dispatch or reruns as native schedule evidence.
6. Keep StockDividend production promotion disabled. The publisher explicitly logs that promotion is disabled; handoff validation and paired digest dispatch were skipped. Do not enable promotion without explicit release authorization and protected Actions:read access. Preserve atomic Admin/Backend pairing.
7. Preserve strict HTTP 200 checks while TCE service availability is unresolved. TCE frontend/service and Auth/Keycloak desired replicas remain 0/0; heartbeat forwarding is not service health.
8. Resolve Auth Supabase integration target/effects and migration provenance before merging #75/#76, running migrations or activating Auth/Keycloak.
9. Obtain a VPS maintenance window before pending Ubuntu, Docker and containerd upgrades or reboot.
10. Keep optional VPS MCP PR #1222 in draft until its mutation paths are removed or brought under the single GitOps authority, shell UID/GID isolation is actually enforced, and reproducible build/test/lockfile checks pass.

## Current runtime blockers

- **K3s snapshot:** debug/vps-latest.md was generated at 2026-11-04T23:34:04Z (2026-11-05 06:34:04 ICT) by native scheduled inspection #41934713847 and merged by PR #1246 as master SHA 3bc0921c4e1e753356c1930a26cd0cf0ab3a9e2d. At 07:01 ICT it is about 27 minutes old. Node tce-k3s-01 was Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, available memory about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Two Stock Admin Pods and the new Stock Backend Pod were ImagePullBackOff; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0. Public Keycloak OIDC probes returned HTTP 503. This is point-in-time evidence, not continuous health.
- **StockDividend:** Production Admin and new Backend still reference tag 12d63b4, which has no ARM64 manifest (containerd reports no match for platform in manifest). The successful publisher #41563856933 verified these immutable linux/arm64 digests for source SHA 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec:
  - Scraper: sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2
  - Admin: sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e
  - Backend: sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a
  The publisher release gate explicitly disables production GitOps promotion. Handoff validation and paired digest dispatch are SKIPPED. No production promotion is authorized by this evidence.
- **TCE/Auth/Keycloak:** The 06:34 ICT snapshot shows TCE frontend/service and MicroFE Auth/Keycloak at 0/0. Native WF-06 #41932031987 at 06:13:49 ICT failed all four strict public endpoint probes: https://tce.mrcute.space/api/health, https://tce.mrcute.space/, https://auth.mrcute.space/api/health and https://auth.mrcute.space/api/ready returned HTTP 503 instead of HTTP 200. Native WF-12 #41928632194 at 05:49:42 ICT failed delivery/freshness verification; workflow_run #41932063303 at 06:14:02 ICT passed heartbeat forwarding and WF-06 delivery verification but is not a native schedule event.
- **Media/MicroFE:** Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 in the 06:34 ICT snapshot. Media and MicroFE imageIDs are digest-pinned. Latest Media CI #41617592783 passed.
- **Host maintenance:** restart_required: yes. The host is Ubuntu 22.04.5 ARM64 with Docker 29.1.3 and K3s containerd 2.3.2-k3s2. Pending package upgrades include containerd 2.4.2 and Docker 29.9.3. No reboot or package upgrade was performed.

## Native schedule evidence

| Workflow | Cron (unchanged) | Latest positively verified native schedule evidence | Result |
|---|---|---|---|
| inspect-vps.yml | 2,32 * * * * | #41934713847 at 06:33:56 ICT | PASS, event=schedule. Read-only snapshot PR #1246 merged at exact validated snapshot head; K3s snapshot generated 06:34:04 ICT. |
| reconcile-vps.yml | 7,22,37,52 * * * * | #41917440202 at 04:35:01 ICT | FAIL in StockDividend health lane. Manual reconcile #41932100148 at 06:14:18 ICT also failed Stock health; it is not native schedule evidence. |
| recover-stale-ops.yml | 10,25,40,55 * * * * | #41914511298 at 04:16:19 ICT | PASS, but stale. Workflow_run recovery #41934894417 at 06:35:15 ICT succeeded after inspection; it does not count as native schedule delivery. |
| reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | #41918315745 at 04:40:44 ICT | FAIL: native inspection freshness exceeded 75 minutes. Latest workflow_run watchdog #41934894419 at 06:35:15 ICT correctly failed because native recovery #41914511298 was 138 minutes old, beyond the 45-minute recovery budget. |

The recovery event-classification fix is merged and a post-merge native inspection schedule event is now verified. Native recovery, reconcile and watchdog delivery remain stale; the latest workflow_run recovery success is not a substitute for a native scheduled run. PR #1247 adds a regression guard so the watchdog can only count event=schedule recovery runs.

TCE native schedule evidence:
- WF-07 TCE Backup #41936628258 at 06:48:44 ICT: SUCCESS. This is the backup workflow, not the separate third-party integration workflow.
- WF-07 TCE 3rd-Party Integration Check #41900042968 at 02:45:37 ICT: SUCCESS; Binance private API check passed and third-party order integration was skipped.
- WF-06 #41932031987 at 06:13:49 ICT: FAIL; TCE API, TCE web, Auth liveness and Auth readiness all returned HTTP 503 instead of HTTP 200.
- WF-12 native schedule #41928632194 at 05:49:42 ICT: FAIL on WF-06 delivery/freshness verification.
- WF-12 workflow_run #41932063303 at 06:14:02 ICT: PASS for WF-06 schedule-delivery verification and authenticated Platform heartbeat notification. It is not a native WF-12 schedule event.
- Preserve all TCE cron declarations, especially the market-scan schedule.

## Credential and dispatch contract

- GHCR pull access is separate from GitOps/repository dispatch. GHCR_READ_TOKEN is package-scoped read:packages access paired with GHCR_USERNAME and package access to every production image.
- STOCKDIVIDEND_ACTIONS_READ_TOKEN is only for Platform Infra to read private StockDividend publisher run metadata. Store it in the protected production Environment with Actions:read only; do not grant Contents write, Packages or workflow-dispatch.
- TCE and Stock use separate per-repository PLATFORM_INFRA_TOKEN values. TCE requires Contents:write and Actions:read on Platform Infra because WF-08B correlates Platform runs and WF-12 sends schedule heartbeats. Stock requires Contents:write for repository dispatch; neither requires Packages or workflow-dispatch.
- Media and Authentication use separate per-repository PLATFORM_INFRA_DISPATCH_TOKEN values. Media requires Contents:write and Actions:read for dispatch correlation; Authentication requires Contents:write.
- Active Platform promotion uses workflow-scoped GITHUB_TOKEN for GitOps PR/validation/merge permissions and GHCR_READ_TOKEN for registry reads. PLATFORM_INFRA_AUTOMATION_TOKEN is obsolete and must not be reintroduced.
- Never store secret values, PATs, passwords, environment files or token fragments in Git or logs.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- reconcile-vps.yml is the sole production apply authority. inspect-vps.yml is read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot or cron expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Recovery event-classification fix PR #1242: https://github.com/phanthienquoc/platform-infra/pull/1242
- Native-recovery watchdog regression guard PR #1247: https://github.com/phanthienquoc/platform-infra/pull/1247
- PR #1247 exact-head lint #41938079392: https://github.com/phanthienquoc/platform-infra/actions/runs/41938079392
- PR #1247 exact-head validate #41938079362: https://github.com/phanthienquoc/platform-infra/actions/runs/41938079362
- PR #1247 post-merge validate-github-actions #41938159895: https://github.com/phanthienquoc/platform-infra/actions/runs/41938159895
- PR #1247 post-merge validate-manifests #41938159872: https://github.com/phanthienquoc/platform-infra/actions/runs/41938159872
- Native scheduled inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Inspection snapshot PR #1246: https://github.com/phanthienquoc/platform-infra/pull/1246
- Latest K3s snapshot: https://github.com/phanthienquoc/platform-infra/blob/master/debug/vps-latest.md
- Latest native reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Manual reconcile #41932100148 (Stock health failure): https://github.com/phanthienquoc/platform-infra/actions/runs/41932100148
- Latest watchdog failure #41934894419: https://github.com/phanthienquoc/platform-infra/actions/runs/41934894419
- Workflow_run recovery #41934894417 (success, not native schedule): https://github.com/phanthienquoc/platform-infra/actions/runs/41934894417
- Latest positively verified native recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- TCE WF-07 Backup #41936628258: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258
- TCE native WF-06 #41932031987: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987
- TCE native WF-12 #41928632194: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194
- TCE workflow_run heartbeat/delivery #41932063303: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932063303
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75: https://github.com/phanthienquoc/phanthienquoc-authentication/pull/75
- Auth PR #76: https://github.com/phanthienquoc/phanthienquoc-authentication/pull/76
- Platform MCP PR #1222: https://github.com/phanthienquoc/platform-infra/pull/1222

## Latest workflow inventory checkpoint

[2026-11-05 07:01 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0701-ict.md) records the post-merge native inspection event, recovery/watchdog freshness failure, new watchdog regression guard, latest K3s snapshot, five-repository heads and remaining production release gates.
