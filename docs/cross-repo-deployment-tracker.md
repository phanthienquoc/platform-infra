# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 15:01 ICT (2026-11-05 08:01 UTC)
Platform Infra master at checkpoint: 543dc4c4cca08ae7261f9d53aabaf5df6d39bb3a
Latest checkpoint: docs/cross-repo-workflow-inventory-checkpoints/2026-11-05-1501-ict.md

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | 543dc4c4cca08ae7261f9d53aabaf5df6d39bb3a | #1222, #544, #541, #539 (all draft) | Post-merge validate-manifests #41984819070 PASS; native inspection #41980605875 PASS at 13:28 but stale; native reconcile #41950932898 and manual reconcile #41980764155 failed Stock health. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d | None | WF-07 native #41982802263 PASS; WF-12 workflow_run #41982820872 failed WF-06 freshness but heartbeat HTTP 204; WF-06 #41962074678 failed four strict HTTP 200 probes with 503. |
| phanthienquoc/stockdividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; full-SHA Scraper/Admin/Backend digests verified; production promotion gate disabled and paired dispatch skipped. |
| phanthienquoc/media-generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None | CI #41617592783 PASS; last snapshot shows backend/frontend 1/1 and digest-pinned, but snapshot is stale. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft | CI #41670642852 PASS; Supabase deploy-to-production integration/migration provenance gate remains closed. |

## Current operational status

- **Platform schedule delivery is still incomplete:** native inspection #41980605875 passed at 13:28:06 ICT, but no subsequent native inspect run appears in the current schedule history. Native reconcile #41950932898 (08:47), recovery #41949145532 (08:31), and watchdog #41951133668 (08:49) remain the latest scheduled runs. The 13:29 workflow_run watchdog #41980748672 confirms reconcile workflow enabled, no runner queue delay, and stale native reconcile/recovery; it does not establish why GitHub stopped delivering those schedule events.
- **Snapshot is stale:** `debug/vps-latest.md` was generated 13:28:14 ICT and is about 93 minutes old at 15:01, beyond the 75-minute budget. Do not represent it as current live health.
- **TCE schedule/health:** WF-07 native #41982802263 passed at 13:47 and WF-12 forwarded an authenticated Platform heartbeat (HTTP 204), but WF-12 #41982820872 failed because WF-06 #41962074678 was 196 minutes old. WF-06's four strict probes returned 503. Platform recovery #41982836006 was repository_dispatch fallback, not native recovery.
- **Stock publication is healthy but production promotion is intentionally gated:** publisher #41563856933 verified linux/arm64 immutable full-SHA digests for all three components. Its promotion gate was disabled and atomic digest dispatch skipped. Production still references old `12d63b4` tags with no ARM64 manifest. Do not describe this as a failed new publisher.
- **Latest K3s point-in-time evidence (13:28):** node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, ~19 GiB available RAM, host restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; TCE/Auth/Keycloak 0/0.
- **Controlled reconciliation side effects:** #41980764155 provisioned/verified Auth runtime Secret and shared GHCR pull credentials; manifest apply and image changes were skipped; Stock health failed. Do not describe this run as read-only.
- **Auth remains blocked:** #75 is test/docs only but owner-provided Supabase integration evidence says Deploy to production is ON for master and the branch has unresolved MIGRATIONS_FAILED history. Do not merge #75/#76 or run migrations until effects/provenance are resolved.

## Current PR heads and validation

- Platform #1222 draft: `f018e39eda52770539fc10671fba0d04baec8046`, #41821355040 PASS (historical); blocked on mutation authority, shell UID/GID isolation and reproducible tests/build/lockfile/ShellCheck.
- Platform #544 draft: `c95e7daecb83b65577b54303427fe4ea81adfe06`, #38575430454 PASS (historical).
- Platform #541 draft: `b8f7c6ba04e3d971336a899b2efd5894662083b3`, #38567431761 PASS (historical).
- Platform #539 draft: `2dc48b97017ecb08e49682633303a2f1d5e991a1`, #38548718033 PASS (historical).
- Authentication #75 ready: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`, #40446492086 PASS (historical); merge blocked by Supabase production side-effect gate.
- Authentication #76 draft: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`, #41329425940 PASS (historical); migration planning is not authorization.

## Exact next actions

1. Obtain a fresh read-only K3s inspection; the 13:28 snapshot is stale. Verify the next native Platform schedule slots (inspection 15:02, reconcile 15:07, recovery 15:10, watchdog 15:12 ICT) without changing cron expressions.
2. Keep Stock paired Admin/Backend promotion disabled until explicit production release authorization and protected source-run Actions:read provenance are available.
3. Keep TCE/Auth desired replicas 0/0 and strict HTTP 200 gates; investigate WF-06 schedule delivery and 503 endpoints without activating workloads.
4. Resolve Auth Supabase production integration side effects and migration provenance before merging #75/#76 or running migrations.
5. Keep Platform MCP PR #1222 draft until mutation authority, shell isolation and reproducible build/test/security evidence are complete.
6. Wait for an approved VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

## Ownership and safety invariants

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve useful CI, test, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No image promotion, production manifest apply, database migration, desired replica change, host package upgrade, reboot or cron change occurred in this checkpoint. Earlier controlled reconciliation #41980764155 did provision Auth runtime Secret and shared GHCR pull credentials; do not describe it as read-only.
- TCE market-scan schedule remains unchanged.


## Checkpoint update — 2026-11-05 07:56 ICT (00:56 UTC)

This update supersedes older status rows above where timestamps differ. Repository refs, open PRs, latest Actions runs, exact-head check-runs, native schedule event history and the current tracker were inspected directly.

### Repository heads, PRs and checks

| Repository | Current master | Open PRs | Latest verified run/check evidence |
|---|---|---|---|
| Platform Infra | `420ff3091867b35772472a1ab54efd74d9e5c255` | #1222, #544, #541, #539 (all draft) | Master `validate-manifests` #41938463049 PASS (push, 07:03:36 ICT). PR #1222 exact-head validate PASS; #544/#541/#539 checks PASS but historical. |
| TCE Dashboard | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Latest schedule WF-07 Backup #41936628258 PASS (06:48:44 ICT); WF-06 #41932031987 FAIL; WF-12 #41928632194 FAIL. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 PASS and immutable publisher #41563856933 PASS (2026-11-03); promotion gate disabled and paired dispatch SKIPPED. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS (2026-11-03); last inspected backend/frontend 1/1, digest-pinned. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS (2026-11-03). #75/#76 validate PASS; both Supabase Preview checks SKIPPED. |

Open PR exact heads:
- Platform #1222 `f018e39eda52770539fc10671fba0d04baec8046`; validate PASS at 2026-11-04T11:30:16Z. Still unsafe: proposed Docker/Kubernetes mutation tools, malformed newline defects, missing SHELL_UID/GID forwarding and no reproducible lockfile/build/test/ShellCheck evidence.
- Platform #544 `c95e7daecb83b65577b54303427fe4ea81adfe06`; validate PASS at 2026-10-14T13:52:17Z; draft.
- Platform #541 `b8f7c6ba04e3d971336a899b2efd5894662083b3`; validate PASS at 2026-10-14T12:54:46Z; draft.
- Platform #539 `2dc48b97017ecb08e49682633303a2f1d5e991a1`; validate PASS at 2026-10-14T10:19:24Z; draft.
- Auth #75 `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; validate PASS at 2026-10-27T03:52:49Z, Supabase Preview SKIPPED.
- Auth #76 `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; validate PASS at 2026-11-01T17:04:06Z, Supabase Preview SKIPPED.

### Native schedule delivery

Filtered Actions history by `event=schedule`; fallback events and reruns are not counted.

| Platform workflow | Latest native schedule run | Result |
|---|---|---|
| inspect-vps | #41934713847, 06:33:56 ICT | PASS; latest native inspection |
| reconcile-vps | #41917440202, 04:35:01 ICT | FAIL; StockDividend health lane |
| recover-stale-ops | #41914511298, 04:16:19 ICT | PASS but stale |
| reconcile-schedule-watchdog | #41918315745, 04:40:44 ICT | FAIL; inspection freshness |

No newer Platform `event=schedule` run was present in Actions history by 07:56 ICT. The latest Platform master push validation #41938463049 is not schedule evidence. Workflow_run recovery #41934894417 succeeded at 06:35:15 ICT, but it is not a native recovery tick. The latest workflow_run watchdog #41934894419 failed recovery freshness.

TCE schedule history:
- WF-07 Backup #41936628258, 06:48:44 ICT: PASS.
- WF-06 #41932031987, 06:13:49 ICT: FAIL; all four strict public checks returned HTTP 503 (TCE web, TCE API, Auth liveness, Auth readiness).
- WF-12 #41928632194, 05:49:42 ICT: FAIL at scheduled WF-06 delivery inspection.
- WF-12 workflow_run #41932063303, 06:14:02 ICT: heartbeat forwarding PASS, but not a native WF-12 schedule event.
- No newer TCE `event=schedule` run was present by 07:56 ICT. Keep strict HTTP 200 and all TCE cron declarations, especially the market-scan schedule, unchanged.

### K3s evidence and age

The latest committed read-only snapshot `debug/vps-latest.md` was generated at 2026-11-04T23:34:04Z (06:34:04 ICT), about 82 minutes old at this checkpoint. It is therefore outside the 75-minute inspection freshness budget and must not be represented as current live health.

At snapshot time:
- Node `tce-k3s-01`: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available RAM about 19 GiB.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1.
- Stock Admin: two Pods 0/1 ImagePullBackOff on `admin:12d63b4`; current Backend replica 0/1 ImagePullBackOff on `backend:12d63b4`; previous Backend and Frontend 1/1 on `23b2878`.
- TCE frontend/service and MicroFE Auth/Keycloak: 0/0. Public Keycloak OIDC probes returned HTTP 503.
- Host `restart_required=yes`; no reboot or package upgrade was performed.

Reconcile #41917440202 confirms shared GHCR credential preflight and GitOps patch operations succeeded without image changes (`ALLOW_IMAGE_CHANGES=false`). The runner helper explicitly classified Stock Admin/Backend `no match for platform in manifest` as permanent and skipped rollout restarts. The Stock health lane correctly failed; no retry churn or false-green status was introduced.

### Release gates and next actions

- StockDividend publisher #41563856933 verified immutable linux/arm64 artifacts, but its production promotion gate is explicitly disabled. Platform handoff validation and atomic Admin/Backend digest dispatch were SKIPPED. Keep promotion disabled until release authorization and protected Actions:read access are verified; do not promote one image independently.
- TCE/Auth remain intentionally 0/0 in the last snapshot. Do not activate workloads or weaken HTTP 200 checks without explicit deployment authorization.
- Auth PRs remain gated because Supabase Preview is SKIPPED and the connected integration target/migration side effect is not authoritatively verified. Do not merge #75/#76 or run migrations on this evidence.
- Keep #1222 draft; it is not a safe alternate deployment authority.
- Next concrete action: verify the enabled state and event delivery for the four Platform scheduled workflows and TCE WF-06/WF-12, then obtain a fresh read-only K3s inspection. Continue Stock paired-release work only after release authorization is available.
- No production manifest, image, credential, database, Pod, replica, host or cron mutation occurred in this checkpoint. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. `locally-uncensored-private` remains retired. TCE market-scan schedule unchanged.

Evidence:
- Platform master validation #41938463049: https://github.com/phanthienquoc/platform-infra/actions/runs/41938463049
- Native Platform inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Native Platform recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- Native Platform watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- TCE WF-06 #41932031987: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987
- TCE WF-12 #41928632194: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194
- TCE WF-07 Backup #41936628258: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment readiness checkpoint — 2026-11-05 09:00 ICT / 02:00 UTC

## Repository state and pull requests

All five default-branch refs, open PRs, latest Actions runs and the current deployment tracker were re-read for this checkpoint.

| Repository | Master SHA | Open PRs | Latest verified CI / run evidence |
|---|---|---|---|
| Platform Infra | `76dad0be9a3aab4130dbd25b7c2c00deb8e24d9e` | #1222, #544, #541, #539 (all draft) | Inspection snapshot PR #1251 exact-head validation #41949516885 PASS; PR #1251 merged. Native recovery #41949145532 PASS; native reconcile #41950932898 FAIL only in Stock health; native watchdog #41951133668 FAIL because native inspection is stale. |
| TCE Dashboard | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Latest native schedule WF-07 Backup #41936628258 PASS at 06:48:44 ICT. WF-06 #41932031987 FAIL at 06:13:49 ICT; WF-12 #41928632194 FAIL at 05:49:42 ICT. No newer TCE schedule run in the inspected Actions history. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS on 2026-11-03. Production promotion remains explicitly disabled; paired handoff/dispatch SKIPPED. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS on 2026-11-03. Latest snapshot shows backend/frontend 1/1 and digest-pinned. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS on 2026-11-03. Exact-head PR checks #40446492086/#41329425940 PASS but historical; Supabase Preview remains SKIPPED. |

Open PR exact heads remain unchanged:
- Platform #1222: `f018e39eda52770539fc10671fba0d04baec8046`; last PR validation #41821355040 PASS (historical). Still draft and unsafe: proposed Docker/Kubernetes mutation tools, unresolved shell/newline and UID/GID isolation issues, and no reproducible lockfile/build/test/ShellCheck evidence.
- Platform #544: `c95e7daecb83b65577b54303427fe4ea81adfe06`; #38575430454 PASS (historical, draft).
- Platform #541: `b8f7c6ba04e3d971336a899b2efd5894662083b3`; #38567431761 PASS (historical, draft).
- Platform #539: `2dc48b97017ecb08e49682633303a2f1d5e991a1`; #38548718033 PASS (historical, draft).
- Auth #75: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; #40446492086 PASS (historical, ready).
- Auth #76: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; #41329425940 PASS (historical, draft).

## Platform native schedule evidence

Native schedule events are separated from workflow_dispatch, workflow_run and repository_dispatch. A fallback can refresh a snapshot or run reconciliation, but it cannot satisfy native schedule freshness.

| Workflow | Latest native schedule | Result at 09:00 ICT |
|---|---|---|
| inspect-vps | #41934713847 at 06:33:56 ICT | PASS but stale; no later event=schedule observed |
| recover-stale-ops | #41949145532 at 08:31:53 ICT | PASS |
| reconcile-vps | #41950932898 at 08:47:55 ICT | FAIL in StockDividend health lane |
| reconcile-schedule-watchdog | #41951133668 at 08:49:44 ICT | FAIL because latest native inspect run was 135 minutes old |

Details:
- The scheduled recovery controller #41949145532 successfully detected stale reconciliation and dispatched the existing GitOps authority as workflow_dispatch #41949160533. Payload evidence in its log: `ref=master`, source SHA `bba0cf2e8dafaf312fea45b8c8a9c93d22aa5ec0`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. The fallback is not native schedule evidence.
- Reconcile #41950932898 had no runner queue delay. Shared preflight and reconciliation job succeeded; no manifest drift was detected, so manifest apply and rollout restarts were skipped. Auth runtime Secret provision/verification completed; Auth, TCE, MicroFE and Media health lanes succeeded. Stock health failed on Admin and new Backend ImagePullBackOff. The final lane summary correctly failed.
- The Stock lane log identifies `ghcr.io/phanthienquoc/stockdividend/admin:12d63b4` (two Pods) and `backend:12d63b4` (one Pod) with `no match for platform in manifest`. `ALLOW_IMAGE_CHANGES=false`; no image was promoted and rollout restart was skipped.
- Watchdog #41951133668 verified `inspect-vps` and `reconcile-vps` are active and found no scheduled reconciliation runner queue delay. It accepted native recovery #41949145532 (17 minutes old at watchdog time) but failed native inspection freshness: latest native inspect #41934713847 was 135 minutes old, beyond the 75-minute budget.
- The manual read-only inspection #41949431808 ran at 08:34:27 ICT and generated snapshot at 08:34:36 ICT. Recovery workflow_dispatch #41949390240 completed the fallback path. Inspection PR #1251 merged exact head `e063193f1bdb8383a06ee9af891450753793f313` as master commit `76dad0be9a3aab4130dbd25b7c2c00deb8e24d9e`. This fresh fallback snapshot does not clear the native inspect schedule blocker.
- Recovery workflow_run #41951186498 succeeded and explicitly observed the fresh workflow_dispatch inspection fallback #41949431808 (14 minutes old at its reference time); it did not conflate that fallback with native schedule evidence. Watchdog workflow_run #41951186419 also failed native inspection freshness.

## Latest K3s snapshot

`debug/vps-latest.md` was generated at 2026-11-05T01:34:36Z (08:34:36 ICT), about 26 minutes old at this checkpoint; it is within the 75-minute snapshot freshness budget but is still point-in-time evidence.

- Node `tce-k3s-01`: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available RAM about 19 GiB.
- Media backend/frontend: 1/1. MicroFE Shell/WS and NATS: 1/1.
- Stock Admin: two Pods 0/1 ImagePullBackOff on tag `12d63b4`; new Backend Pod 0/1 ImagePullBackOff on `12d63b4`; previous Backend and Frontend 1/1.
- TCE frontend/service: 0/0. MicroFE Auth and Keycloak: 0/0. Public Keycloak OIDC discovery probes returned HTTP 503.
- Host `restart_required=yes`; Docker/containerd and Ubuntu package upgrades remain pending. No reboot or upgrade was performed.

## TCE, Stock, Media and Auth gates

- TCE WF-06 #41932031987 failed four strict public probes (TCE API, TCE web, Auth liveness and Auth readiness) with HTTP 503 instead of HTTP 200. WF-12 native #41928632194 failed; workflow_run #41932063303 passed heartbeat forwarding only. WF-07 Backup #41936628258 passed. No newer TCE schedule event was present by this checkpoint. Preserve all TCE cron declarations, especially the market-scan schedule; do not weaken HTTP 200.
- Stock publisher #41563856933 published immutable linux/arm64 artifacts for source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`: Scraper `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`; Admin `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`; Backend `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. Publisher gate explicitly disables production promotion; handoff validation and paired Admin/Backend dispatch are SKIPPED. No release authorization is inferred.
- Media CI #41617592783 PASS; snapshot shows both production workloads 1/1 with digest-pinned imageIDs.
- Auth CI #41670642852 PASS. PR #75/#76 checks are historical and Supabase Preview remains SKIPPED; migration provenance and production integration target/effects are unverified. Do not merge on these checks or run migrations.

## Next dependency-safe actions

1. Confirm the next native `inspect-vps` scheduled event. If still absent, investigate GitHub Actions schedule delivery and workflow enabled state; do not count manual fallback as native evidence or change cron without a diagnosed cause.
2. Keep the Stock paired promotion gate closed until explicit release authorization and protected `STOCKDIVIDEND_ACTIONS_READ_TOKEN` access are confirmed. Then promote both Admin and Backend digests atomically through Platform GitOps.
3. Keep TCE/Auth health gates strict and workloads at their last declared 0/0 until activation is explicitly authorized; investigate 503 without manufacturing a green result.
4. Verify Auth Supabase deployment binding and migration provenance before merging #75/#76 or running migrations.
5. Keep #1222 draft until Docker/Kubernetes mutation authority is removed or brought under the single GitOps authority, UID/GID isolation is enforced, and reproducible build/test/lockfile/ShellCheck evidence exists.
6. Wait for a maintenance window before host upgrades or reboot.

## Ownership and safety

- App repositories own tests, builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, provenance, paired digest promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No direct SSH/Compose/MCP mutation authority was added. `locally-uncensored-private` remains retired.
- The scheduled reconcile executed its Auth runtime Secret provision/verification step, but no manifest drift was found and production manifest apply was skipped. Do not represent this checkpoint as having made zero production-side operations.
- No production image promotion, manifest apply, database migration, Pod/replica change, host reboot or package upgrade was initiated by this documentation update. TCE market-scan schedule unchanged.

## Evidence

- Inspection snapshot PR #1251: https://github.com/phanthienquoc/platform-infra/pull/1251
- Manual read-only inspection #41949431808: https://github.com/phanthienquoc/platform-infra/actions/runs/41949431808
- Inspection exact-head validation #41949516885: https://github.com/phanthienquoc/platform-infra/actions/runs/41949516885
- Native recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Recovery reconciliation fallback #41949160533: https://github.com/phanthienquoc/platform-infra/actions/runs/41949160533
- Native reconciliation #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Watchdog workflow_run #41951186419: https://github.com/phanthienquoc/platform-infra/actions/runs/41951186419
- Recovery workflow_run #41951186498: https://github.com/phanthienquoc/platform-infra/actions/runs/41951186498
- Native TCE WF-07 Backup #41936628258: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258
- Native TCE WF-06 #41932031987: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987
- Native TCE WF-12 #41928632194: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194
- TCE workflow_run heartbeat forwarding #41932063303: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932063303
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


## Live checkpoint — 2026-11-05 10:04 ICT / 03:04 UTC

### Exact repository and workflow evidence

- Platform Infra master is 8ae797a0bd69be772a590515d73dfce0e45a820e (commit #1253, generated by inspection automation at 02:57:53Z). Latest read-only inspection #41958436222 ran by workflow_dispatch at 02:56:44Z and succeeded; validation #41958510609 completed successfully at 02:57:28Z. These are not native schedule events.
- Platform Infra open PRs: #1222, #544, #541, #539; all remain draft. PR #1222 head f018e39eda52770539fc10671fba0d04baec8046; its only returned check validate #41821355040 is historical PASS, but its Docker/Kubernetes mutation scope, shell isolation and reproducible build/test gaps remain release blockers.
- TCE master 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; no open PRs. WF-12 native #41958165099 ran at 02:54:09Z and failed freshness. Its log verifies WF-06 is active, but latest WF-06 scheduled run #41932031987 is 23:13:49Z (220 minutes old at watchdog time). WF-06 source cron remains */15 * * * *; latest known public smoke failed four strict HTTP 200 checks with HTTP 503. WF-12 heartbeat forwarding succeeded; that does not make the schedule check pass.
- StockDividend master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; no open PRs. CI #41563856934 and publisher #41563856933 succeeded. Production paired promotion remains disabled; current Admin and Backend tag 12d63b4 has no ARM64 manifest. No image or manifest change is authorized.
- Media master e4c7d8990aafc7d837e918c9caf39722d623de7c; no open PRs. CI #41617592783 succeeded; snapshot imageIDs are digest-pinned.
- Authentication master f978a3f378ee22d4630909c2d182275b21ac9e9a; PR #75 is ready, #76 draft. Their latest returned validate checks passed, but Supabase Preview checks were SKIPPED. No migration or production activation is authorized.

### Native schedule delivery (only event=schedule counts)

| Workflow | Latest verified native run | Result and interpretation |
|---|---|---|
| Platform inspect-vps | #41934713847 at 2026-11-04 23:33:56Z | PASS, but stale. Manual inspection #41958436222 at 02:56:44Z succeeded and produced the current snapshot; it is not native schedule evidence. |
| Platform reconcile-vps | #41950932898 at 2026-11-05 01:47:55Z | FAIL only in Stock health. Manual reconcile #41958192072 at 02:54:23Z also failed Stock health; the health log confirms no match for platform in manifest for Admin/Backend tag 12d63b4. |
| Platform recover-stale-ops | #41949145532 at 2026-11-05 01:31:53Z | PASS. Manual recovery #41958394974 at 02:56:20Z succeeded after the manual reconcile failure; it is not native schedule evidence. |
| Platform reconcile-schedule-watchdog | #41951133668 at 2026-11-05 01:49:44Z | FAIL: native inspection freshness exceeded 75 minutes. Its recovery freshness step passed against #41949145532. |
| TCE WF-06 | #41932031987 at 2026-11-04 23:13:49Z | FAIL on public endpoint HTTP 503; at WF-12 run #41958165099 it was 220m old, beyond the 25m schedule freshness budget. Workflow-enabled check passed (state=active). |
| TCE WF-12 | #41958165099 at 2026-11-05 02:54:09Z | FAIL on stale WF-06 schedule delivery. Authenticated heartbeat dispatch succeeded but is not a substitute for WF-06 native delivery. |
| TCE WF-07 Backup | #41936628258 at 2026-11-04 23:48:44Z | PASS; separate from WF-07 third-party integration and from WF-06 service health. |

### Latest K3s snapshot

- debug/vps-latest.md generated at 2026-11-05T02:56:52Z (09:56:52 ICT) by manual inspection #41958436222; PR #1253 committed it at Platform master 8ae797a0bd69be772a590515d73dfce0e45a820e. At this checkpoint the snapshot is about 8 minutes old, inside the 75-minute freshness budget.
- Node tce-k3s-01: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available memory about 19 GiB.
- Media backend/frontend, MicroFE Shell/WS and NATS are 1/1 and digest-pinned. Stock Admin (two Pods) and new Backend remain ImagePullBackOff on 12d63b4; old Backend and Frontend are 1/1. TCE/Auth/Keycloak desired replicas remain 0/0. Public Keycloak OIDC remains HTTP 503.
- Host restart_required=yes; Docker/containerd/Ubuntu upgrades remain pending. No reboot or package upgrade.

### Safety and next actions

1. Confirm native schedule event delivery for inspect, reconcile, recovery, watchdog and TCE WF-06/WF-12 independently; do not count manual, workflow_run or repository_dispatch events.
2. Keep Stock promotion disabled until explicit release authorization and protected StockDividend Actions:read provenance access are confirmed; preserve atomic Admin/Backend digest pairing.
3. Keep strict HTTP 200 gates and TCE/Auth 0/0 desired state unchanged until a separately authorized service activation.
4. Keep Auth Supabase migration provenance/target review as a pre-merge gate.
5. Obtain a maintenance window before host package upgrades/reboot.

No production image, manifest, credential, database, Pod, replica or host mutation was performed. reconcile-vps.yml remains the sole production apply authority; app repos own build/test/immutable GHCR; Platform Infra owns GitOps, pull credentials, promotion and rollout. Preserve useful CI, security, backup, manual and scheduled workflows. No cron expression was changed; the TCE market-scan schedule is unchanged.


## Audit correction — production-side effects of reconcile run #41958192072 (2026-11-05 10:10 ICT)

The prior 10:04 checkpoint incorrectly described the reconcile run as having no credential mutation. The run was a workflow_dispatch with mode=apply, target_app=all and ALLOW_IMAGE_CHANGES=false. Its job-step API records the following successful steps:

- Validate GHCR pull access before mutating cluster credentials.
- Provision Auth runtime Secret from the platform-infra production Environment.
- Bootstrap shared GHCR pull credentials.
- Execute the managed image-pull-blocked workload restart policy.
- Verify cluster after reconciliation.

The shared preflight reported DRIFT=false; Apply production manifests and post-apply drift verification were skipped. Therefore, this run did perform controlled production credential reconciliation (Auth runtime Secret and shared GHCR pull Secret), despite making no production manifest/image-reference change. The Stock lane still failed: Admin and new Backend remained ImagePullBackOff on tag 12d63b4 because the ARM64 manifest is absent. The run did not establish Stock recovery or a healthy overall deployment.

Do not describe this reconcile as zero production-side operations. The evidence does not show a database migration, image digest promotion, manifest apply, desired replica change or host reboot. The workflow-step summary shows the managed restart step completed, but this audit does not infer that every blocked Pod was restarted; the subsequent inspection still shows the Stock Admin/Backend failures.



## Live checkpoint — 2026-11-05 11:04 ICT / 04:04 UTC

### Repository and PR state

- Platform Infra master: `c0d5c5ff18472800f15b352cd950c4c3d959cd1f`. Open PRs #1222, #544, #541 and #539 remain draft. Exact PR-head workflow runs returned: #1222 validate-manifests #41821355040 PASS; #544 #38575430454 PASS; #541 #38567431761 PASS; #539 #38548718033 PASS. These are historical checks. #1222 remains blocked by Docker/Kubernetes mutation scope, shell UID/GID isolation, newline defects and missing reproducible build/test/lockfile/ShellCheck evidence.
- TCE Dashboard master: `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`; no open PRs.
- StockDividend master: `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no open PRs.
- Media Generation master: `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no open PRs.
- Authentication master: `f978a3f378ee22d4630909c2d182275b21ac9e9a`; PR #75 ready and #76 draft. Their exact-head Auth CI runs #40446492086 and #41329425940 passed historically. Supabase Preview remains SKIPPED; #75 remains blocked by unknown Supabase deployment binding/migration side effect, and #76 remains draft.

### Latest Platform workflow and native schedule evidence

- Manual reconcile #41962132547 ran at 2026-11-05 03:31:30Z (10:31:30 ICT), event=workflow_dispatch, ref=master, mode=apply, target_app=all, ALLOW_IMAGE_CHANGES=false. Shared reconciliation and preflight succeeded; no GitOps manifest drift was found, so production manifest apply and post-apply drift verification were skipped.
- The same reconcile completed controlled production credential work: GHCR pull access validation, Auth runtime Secret provisioning/verification, shared GHCR pull credential bootstrap and the managed image-pull restart policy. The restart policy explicitly skipped Stock Admin and Backend because their errors are permanent `no match for platform in manifest`; no rollout restart was performed for those two workloads. No image digest promotion, manifest apply, database migration, replica change or host reboot is evidenced.
- Stock health lane and final deployment gate failed correctly. Media, MicroFE, TCE internal workload and Auth lanes passed their configured checks; Keycloak lane was skipped.
- Manual recovery #41962345391 at 10:33 ICT succeeded. It found the prior manual inspection fallback #41958436222 still fresh (about 35 minutes old), avoided a duplicate inspection dispatch, and explicitly retained the native inspection schedule as stale. This is workflow_dispatch, not native schedule evidence.
- Latest native Platform schedule events remain: inspect-vps #41934713847 (06:33:56 ICT, success but stale); reconcile-vps #41950932898 (08:47:55 ICT, failure in Stock health); recovery #41949145532 (08:31:53 ICT, success); watchdog #41951133668 (08:49:44 ICT, failure on native inspection freshness). No later `event=schedule` run was returned through 11:04 ICT. Workflow_dispatch, workflow_run and repository_dispatch fallbacks do not satisfy native cadence.
- Reconcile #41962132547's live cluster listing at 10:32 ICT: node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Media backend/frontend, MicroFE Shell/WS and NATS 1/1; two Stock Admin Pods and the new Stock Backend Pod ImagePullBackOff; previous Stock Backend and Stock Frontend 1/1. No TCE/Auth Pods appeared in the live Pod listing; the latest committed inspection still records their desired workloads at 0/0.
- The latest committed read-only snapshot remains #41958436222 at 09:56:52 ICT. It is about 68 minutes old at this checkpoint and approaching the 75-minute freshness budget. Host restart_required=yes; no package upgrade or reboot.

### TCE schedule and endpoint evidence

- Native WF-06 #41962074678 ran at 10:30:58 ICT (event=schedule) and failed all four strict public HTTP 200 probes: TCE API `https://tce.mrcute.space/api/health`, TCE web `https://tce.mrcute.space/`, Auth liveness `https://auth.mrcute.space/api/health`, and Auth readiness `https://auth.mrcute.space/api/ready` each returned HTTP 503.
- WF-12 workflow_run #41962097006 ran at 10:31:50 ICT and passed its schedule-delivery check. Its job log confirms WF-06 is active and a recent scheduled WF-06 run exists. This establishes that WF-06 native schedule delivery resumed at 10:30; it does not establish endpoint health or a native WF-12 schedule event.
- Latest native WF-12 scheduled run remains #41958165099 at 09:54:09 ICT (failure on then-stale WF-06 delivery). WF-07 Backup #41936628258 at 06:48:44 ICT remains PASS.
- Preserve strict HTTP 200 and do not change TCE cron declarations or market-scan schedule.

### App publication and release gates

- Stock CI #41563856934 and immutable ARM64 publisher #41563856933 remain the latest successful Stock runs (2026-11-03). Publisher produced full-source-SHA-tagged Scraper/Admin/Backend ARM64 artifacts and registry digests; production paired Admin/Backend promotion remains explicitly disabled and handoff/dispatch remain SKIPPED. Production tags `12d63b4` still lack an ARM64 manifest. No release authorization is inferred.
- Media CI #41617592783 PASS (2026-11-03); live reconcile listing confirms both production workloads 1/1 with digest-pinned images.
- Auth CI #41670642852 PASS (2026-11-03); no Supabase Preview evidence or migration authorization.

### Next dependency-safe actions

1. Obtain a fresh read-only inspection before the 75-minute freshness budget expires, while separately continuing to require a new native `event=schedule` inspection run. Do not count the manual fallback as native delivery.
2. Investigate Platform scheduled-event delivery after 08:49 ICT. Prior watchdog logs confirmed inspect-vps and reconcile-vps were active and no runner queue delay was detected; no evidence justifies changing cron expressions.
3. Keep Stock paired promotion disabled until explicit release authorization and protected StockDividend Actions:read provenance access are confirmed. Promote Admin and Backend only as one atomic digest-pinned release.
4. Keep TCE/Auth public HTTP 200 gates strict and desired replicas at 0/0 until separately authorized activation. WF-06 schedule delivery is fresh again; public endpoints remain unhealthy.
5. Keep Auth #75/#76 behind Supabase binding and migration-provenance review. Keep Platform #1222 draft until the mutation boundary and reproducible security/build checks are resolved.
6. Wait for a VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

### Evidence

- Platform master: https://github.com/phanthienquoc/platform-infra/commit/c0d5c5ff18472800f15b352cd950c4c3d959cd1f
- Manual reconcile #41962132547: https://github.com/phanthienquoc/platform-infra/actions/runs/41962132547
- Manual recovery #41962345391: https://github.com/phanthienquoc/platform-infra/actions/runs/41962345391
- Native Platform inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform reconcile #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native Platform recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Native Platform watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Native TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 workflow_run #41962097006: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962097006
- Native TCE WF-12 #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852

No cron expression, production manifest, image reference, database, desired replica, host package or reboot setting was changed by this checkpoint. TCE market-scan schedule remains unchanged.


# Cross-repo deployment checkpoint — 2026-11-05 11:58 ICT / 04:58 UTC

## Repository state and PRs

| Repository | Current master | Open PRs | Latest relevant Actions evidence |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `afb49ba5dcc95f273b940463fe4cdd8d92001bd2` | #1222, #544, #541, #539 (all draft) | PR #1256 merged; exact-head validation #41965908624 PASS; post-merge `validate-manifests` #41965978011 PASS. |
| `phanthienquoc/TCE-dashboard` | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Native WF-06 #41962074678 (10:30:58 ICT) delivered but failed all four public HTTP 200 probes with 503. WF-12 workflow_run #41962097006 PASS; latest native WF-12 #41958165099 (09:54 ICT) failed freshness. |
| `phanthienquoc/stockdividend` | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and immutable publisher #41563856933 PASS (Nov 3); paired production promotion remains disabled and un-dispatched. |
| `phanthienquoc/media-generation` | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS (Nov 3); last live reconcile listing #41962132547 showed backend/frontend 1/1. |
| `phanthienquoc/phanthienquoc-authentication` | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 PASS (Nov 3); PR #75/#76 CI passed historically; Supabase Preview remains SKIPPED. |

Platform open PR heads were re-read:
- #1222 draft: `f018e39eda52770539fc10671fba0d04baec8046`; exact-head validation #41821355040 PASS (historical). Keep blocked on mutation authority, shell UID/GID enforcement, newline defects and reproducible lockfile/build/test/ShellCheck evidence.
- #544 draft: `c95e7daecb83b65577b54303427fe4ea81adfe06`; #38575430454 PASS (historical).
- #541 draft: `b8f7c6ba04e3d971336a899b2efd5894662083b3`; #38567431761 PASS (historical).
- #539 draft: `2dc48b97017ecb08e49682633303a2f1d5e991a1`; #38548718033 PASS (historical).
- Authentication #75 ready: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; #40446492086 PASS (historical).
- Authentication #76 draft: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; #41329425940 PASS (historical).

## Platform Infra schedule and deployment evidence

The latest native `event=schedule` runs returned by GitHub Actions are unchanged from the 11:04 checkpoint:

| Workflow | Latest native scheduled run | Result at run time |
|---|---|---|
| `inspect-vps.yml` | #41934713847, 06:33:56 ICT | PASS; now stale |
| `recover-stale-ops.yml` | #41949145532, 08:31:53 ICT | PASS |
| `reconcile-vps.yml` | #41950932898, 08:47:55 ICT | Shared reconcile passed; Stock health lane failed |
| `reconcile-schedule-watchdog.yml` | #41951133668, 08:49:44 ICT | FAIL: no native inspection run within 75 minutes |

At 11:58 ICT these native events are approximately 325m, 206m, 190m and 188m old respectively. No newer Platform `event=schedule` run was returned. The watchdog's inspection-delivery step failed on inspection freshness; the step checks workflow state before freshness, so the failure was not reported as a disabled `inspect-vps` workflow. Do not infer why GitHub stopped delivering the scheduled event.

Latest Platform master validation after PR #1256:
- Exact-head #41965908624: PASS.
- PR #1256 merged as `afb49ba5dcc95f273b940463fe4cdd8d92001bd2`.
- Post-merge `validate-manifests` #41965978011: PASS.
- PR #1256: https://github.com/phanthienquoc/platform-infra/pull/1256

Latest operational reconcile evidence remains manual dispatch #41962132547 (10:31 ICT), not a native schedule. Its shared preflight, GHCR access validation, Auth runtime Secret provisioning, shared GHCR pull credential bootstrap and managed restart-policy steps succeeded. GitOps drift was false, so production manifest apply was skipped. Stock Admin and new Backend were classified as permanent architecture mismatches and were not restarted; Stock health and final deployment gate failed. Manual recovery #41962345391 (10:33 ICT) passed but did not constitute native cron evidence.

## TCE schedule and health

- WF-06 native schedule #41962074678 at 10:30:58 ICT is the latest scheduled run. Its four public probes all returned HTTP 503: TCE web, TCE API, Auth liveness and Auth readiness.
- WF-12 workflow_run #41962097006 passed after WF-06, but it is a workflow_run event, not native WF-12 cron evidence.
- Latest native WF-12 remains #41958165099 at 09:54:09 ICT, failed because WF-06 schedule delivery was stale at that time.
- WF-07 Backup #41936628258 at 06:48:44 ICT remains the latest returned successful native backup run.
- At 11:58 ICT WF-06's last native run is about 87 minutes old and WF-12's last native run about 124 minutes old. Keep strict HTTP 200 and schedule-freshness checks. Do not change any TCE cron declaration or the market-scan schedule.

## K3s and app release gates

The committed `debug/vps-latest.md` snapshot was generated at 2026-11-05T02:56:52Z (09:56:52 ICT), so it is about 122 minutes old at this checkpoint and is not current live-health evidence. It records:
- Node `tce-k3s-01` Ready / ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2.
- Disk 56%; available RAM about 19 GiB; `restart_required=yes`.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin (two Pods) and new Backend 0/1 ImagePullBackOff; old Backend and Frontend 1/1.
- TCE/Auth/Keycloak desired state 0/0; public Keycloak endpoints HTTP 503.

The last live cluster listing in reconcile #41962132547 at 10:32 ICT corroborated the Stock ImagePullBackOff and Media/MicroFE/NATS 1/1 states, but is now about 86 minutes old. No fresh K3s inspection was available in the current Actions history.

- **StockDividend:** successful publisher #41563856933 verified immutable ARM64 artifacts for Scraper/Admin/Backend, but production Admin/Backend still reference tag `12d63b4` without an ARM64 manifest. Production paired handoff/dispatch are SKIPPED. Keep promotion disabled until explicit release authorization and protected Actions:read provenance access are confirmed; never promote only one of Admin/Backend.
- **Media Generation:** latest CI #41617592783 PASS; last live reconcile showed backend/frontend 1/1 with digest-pinned images.
- **Authentication:** latest master CI #41670642852 PASS; #75/#76 remain gated on Supabase deployment binding and migration provenance. No Preview or migration authorization is evidenced.

## Exact next actions

1. Obtain a fresh read-only K3s inspection and separately restore/verify native `inspect-vps` schedule delivery. The current connected GitHub operations expose read/search and PR writes but no workflow-dispatch action; no manual inspection dispatch was initiated in this run.
2. Investigate GitHub scheduled-event delivery for Platform inspect/reconcile/recovery/watchdog and TCE WF-06/WF-12. Preserve cron expressions; do not count manual, workflow_run or repository_dispatch as native schedule evidence.
3. Keep Stock Admin/Backend promotion disabled until explicit authorization and paired immutable digest provenance are available.
4. Keep TCE/Auth public HTTP 200 gates strict and desired replicas 0/0 until separately authorized activation.
5. Keep Auth #75/#76 behind Supabase binding and migration-provenance review; keep Platform #1222 draft.
6. Wait for an approved VPS maintenance window before package upgrades or reboot.

No production manifest/image promotion, database migration, desired replica change, host package upgrade, reboot or cron change was performed by this documentation checkpoint. The earlier reconcile #41962132547 did perform controlled Auth runtime Secret and shared GHCR credential reconciliation; it must not be described as read-only. `reconcile-vps.yml` remains the sole production apply authority; app repositories own tests/builds/immutable GHCR; Platform Infra owns manifests, shared pull credentials, promotion, reconciliation, rollout and health verification. Preserve useful CI/security/backup/manual/release/scheduled workflows and do not introduce direct SSH/Compose/MCP mutation authority. The TCE market-scan schedule remains unchanged.

### Evidence

- PR #1256: https://github.com/phanthienquoc/platform-infra/pull/1256
- Exact-head validation #41965908624: https://github.com/phanthienquoc/platform-infra/actions/runs/41965908624
- Post-merge validation #41965978011: https://github.com/phanthienquoc/platform-infra/actions/runs/41965978011
- Native Platform inspect #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Native Platform reconcile #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native Platform watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Manual Platform reconcile #41962132547: https://github.com/phanthienquoc/platform-infra/actions/runs/41962132547
- Manual Platform recovery #41962345391: https://github.com/phanthienquoc/platform-infra/actions/runs/41962345391
- Native TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 workflow_run #41962097006: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962097006
- Native TCE WF-12 #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment checkpoint — 2026-11-05 15:01 ICT / 08:01 UTC

## Repository heads, open PRs and latest Actions evidence

| Repository | Current master | Open PRs | Latest verified evidence |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `543dc4c4cca08ae7261f9d53aabaf5df6d39bb3a` | #1222, #544, #541, #539 (all draft) | Post-merge `validate-manifests` #41984819070 PASS after PR #1260; latest native inspection #41980605875 PASS at 13:28 but now stale; manual reconcile #41980764155 failed Stock health. |
| `phanthienquoc/TCE-dashboard` | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | WF-07 native schedule #41982802263 PASS; WF-12 workflow_run #41982820872 failed WF-06 freshness but heartbeat dispatch returned HTTP 204; latest WF-06 native #41962074678 failed all four public HTTP 200 probes with 503. |
| `phanthienquoc/stockdividend` | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and publisher #41563856933 PASS; publisher log verifies Scraper/Admin/Backend linux/arm64 digests. Production promotion gate and paired dispatch were explicitly skipped. |
| `phanthienquoc/media-generation` | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS; latest K3s snapshot at 13:28 shows backend/frontend 1/1 and digest-pinned, but snapshot is stale at this checkpoint. |
| `phanthienquoc/phanthienquoc-authentication` | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS; Supabase GitHub integration is owner-reported as deploy-to-production ON and migration state remains unresolved, so #75/#76 remain gated. |

### Open PR heads and latest exact-head checks

- Platform #1222 draft, head `f018e39eda52770539fc10671fba0d04baec8046`: #41821355040 PASS (historical); keep draft because Docker/Kubernetes mutation scope, shell UID/GID isolation and reproducible build/test/lockfile/ShellCheck evidence remain unresolved.
- Platform #544 draft, head `c95e7daecb83b65577b54303427fe4ea81adfe06`: #38575430454 PASS (historical).
- Platform #541 draft, head `b8f7c6ba04e3d971336a899b2efd5894662083b3`: #38567431761 PASS (historical).
- Platform #539 draft, head `2dc48b97017ecb08e49682633303a2f1d5e991a1`: #38548718033 PASS (historical).
- Authentication #75 ready, head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`: #40446492086 PASS (historical); no merge because the connected Supabase GitHub integration is configured to deploy to production and the migration state/binding is not reconciled.
- Authentication #76 draft, head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`: #41329425940 PASS (historical); planning is not migration authorization.

## Platform native schedule and recovery evidence

Filtered Actions history by `event=schedule`; workflow_dispatch, workflow_run and repository_dispatch events are not counted as native cron delivery.

| Workflow | Latest native schedule | Result |
|---|---|---|
| `inspect-vps.yml` | #41980605875, 13:28:06 ICT | PASS; generated snapshot at 13:28:14 ICT. At 15:01 it is about 93 minutes old, beyond the 75-minute freshness budget. |
| `reconcile-vps.yml` | #41950932898, 08:47:55 ICT | FAIL in Stock health; about 373 minutes old. |
| `recover-stale-ops.yml` | #41949145532, 08:31:53 ICT | PASS at run time; about 389 minutes old, beyond the 45-minute budget. |
| `reconcile-schedule-watchdog.yml` | #41951133668, 08:49:44 ICT | FAIL at run time; about 371 minutes old. |

The later workflow_run watchdog #41980748672 at 13:29:27 ICT confirms:
- `reconcile-vps` workflow enabled check PASS.
- Native reconciliation #41950932898 was 281 minutes old at watchdog reference time; the watchdog correctly failed the 45-minute freshness gate.
- Native inspection #41980605875 was 1 minute old and its runner queue wait was 0 minutes.
- Native recovery #41949145532 was 297 minutes old and failed the 45-minute freshness gate.
- No reconciliation deployment-lane queue exceeded the 15-minute budget.

This evidence points to missing/stale scheduled event delivery, not a disabled reconcile workflow or a self-hosted runner queue delay. Do not change cron expressions to hide the gap.

## TCE schedule and public health

- WF-06 latest native schedule #41962074678 at 10:30:58 ICT; all four endpoints failed strict HTTP 200 checks with HTTP 503: TCE web, TCE API, Auth liveness and Auth readiness.
- WF-12 latest native schedule #41958165099 at 09:54:09 ICT; it failed WF-06 freshness.
- WF-07 native schedule #41982802263 at 13:47:35 ICT passed Binance Testnet public/private checks; order integration was skipped by design.
- WF-12 workflow_run #41982820872 at 13:47:46 ICT failed because the latest native WF-06 was 196 minutes old against a 25-minute budget. Its independent Platform heartbeat job succeeded with HTTP 204 and carried source workflow path `.github/workflows/wf-07-tce-integration-check.yml`, source run #41982802263 attempt 1, TCE master SHA `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`, and heartbeat run #41982820872 attempt 1.
- Platform recovery #41982836006 (repository_dispatch) accepted that heartbeat and succeeded. It is fallback coordination, not native Platform recovery schedule evidence.
- Keep strict HTTP 200 and the existing 25-minute freshness gate. Do not change any TCE cron declaration or the market-scan schedule.

## K3s snapshot and operational reconciliation

Snapshot `debug/vps-latest.md` generated at `2026-11-05T06:28:14Z` / 13:28:14 ICT; approximately 93 minutes old at this checkpoint and therefore stale for the 75-minute inspection budget.

At snapshot time:
- Node `tce-k3s-01`: Ready / ARM64; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Disk 56%; available RAM about 19 GiB; Docker 29.1.3; host `restart_required=yes`.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1 with digest-pinned images.
- Stock Admin: two Pods 0/1 ImagePullBackOff on `admin:12d63b4`; new Backend Pod 0/1 ImagePullBackOff on `backend:12d63b4`; previous Backend and Frontend remain 1/1 on older `23b2878` images.
- The failed Stock images have no resolved digest; containerd reports `no match for platform in manifest`.
- TCE frontend/service and MicroFE Auth/Keycloak remain desired 0/0. Public OIDC probes returned HTTP 503.

Manual reconcile #41980764155 (13:29:35 ICT) used `mode=apply`, `target_app=all`, `ALLOW_IMAGE_CHANGES=false`:
- GHCR access preflight, Auth runtime Secret provisioning, shared GHCR pull credential bootstrap and managed image-pull restart policy succeeded.
- Media, MicroFE, TCE and Auth lanes passed; Keycloak lane was skipped.
- Stock health failed; final deployment gate failed.
- Production manifest apply and image changes were skipped; no image promotion or manifest apply is evidenced.
- This was controlled credential reconciliation, not a read-only run.

## Immutable Stock publication evidence

Stock publisher #41563856933 (master SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`) completed successfully on a native ARM64 runner. The publisher log explicitly verified the full-source-SHA tags with linux/arm64 support and immutable registry digests:

| Component | Immutable tag | Verified digest |
|---|---|---|
| Scraper | `sha-50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2` |
| Admin | `sha-50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e` |
| Backend | `sha-50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a` |

The same run explicitly reported production GitOps promotion disabled; the Platform handoff validation and atomic digest dispatch jobs were skipped. Therefore the current production `12d63b4` mismatch is a stale/unpromoted production reference, not evidence that the new publisher failed. Keep paired Admin/Backend promotion disabled until explicit release authorization and protected source-run Actions:read provenance are available.

## Exact next actions

1. Obtain a fresh read-only K3s inspection; the 13:28 snapshot is now stale. Verify the next native Platform schedule slots (inspection 15:02, reconcile 15:07, recovery 15:10, watchdog 15:12 ICT) without changing cron expressions. If native delivery is still absent, use only the existing recovery/inspection fallback authority when its policy allows; never count fallback as native schedule evidence.
2. Keep Stock paired Admin/Backend promotion disabled until explicit production release authorization and protected publisher-run Actions:read access are confirmed. The current full-SHA ARM64 digests are available but are not promotion authorization.
3. Keep TCE/Auth desired replicas 0/0 and strict HTTP 200 gates; investigate the missing WF-06 native delivery and 503 endpoints without activating workloads.
4. Keep Auth #75/#76 gated until Supabase production integration side effects and migration provenance are authoritatively reconciled.
5. Keep Platform MCP PR #1222 draft until mutation authority, shell UID/GID isolation and reproducible build/test/security evidence are complete.
6. Wait for an approved VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, production manifest apply, database migration, desired replica change, host package upgrade, reboot or cron expression change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

### Evidence

- Platform master/post-merge validation #41984819070: https://github.com/phanthienquoc/platform-infra/actions/runs/41984819070
- PR #1260: https://github.com/phanthienquoc/platform-infra/pull/1260
- Native Platform inspection #41980605875: https://github.com/phanthienquoc/platform-infra/actions/runs/41980605875
- Platform watchdog workflow_run #41980748672: https://github.com/phanthienquoc/platform-infra/actions/runs/41980748672
- Manual Platform reconcile #41980764155: https://github.com/phanthienquoc/platform-infra/actions/runs/41980764155
- TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 native #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- TCE WF-07 #41982802263: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41982802263
- TCE WF-12 workflow_run #41982820872: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41982820872
- Platform heartbeat recovery #41982836006: https://github.com/phanthienquoc/platform-infra/actions/runs/41982836006
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Authentication CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
