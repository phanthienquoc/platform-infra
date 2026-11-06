## Current review — 2026-11-06 13:03 ICT (2026-11-06 06:03 UTC)

This checkpoint revalidates all five default branches, open PRs, recent Actions runs, the TCE schedule/health failures, and the latest committed read-only K3s snapshot. It records observed state only; it does not authorize image publication, replica changes, runner retirement, or namespace deletion.

### Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `fb5c28f99148e6d4af8c43ffa2685c24e76635e5` | #1314 draft; #544/#541/#539 drafts | PRs #1320, #1321 and #1322 are merged; current master validation passes. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Strict public probes remain HTTP 503; WF-06 native schedule delivery is stale. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | Master CI passes ARM64 build-only checks for Admin, Backend and Scraper; no authorized GHCR publication observed. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | Latest master CI passes (historical run); no new publisher. Workloads remain active pending approved retirement. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | Master CI passes ARM64 build-only; release remains manual-only. |

### Platform Infra state

- PR #1322 updated the tracker/inventory after #1320 storage inventory and #1321 read-only inspection. Current master is `fb5c28f99148e6d4af8c43ffa2685c24e76635e5`.
- Latest master validation [#42168557657](https://github.com/phanthienquoc/platform-infra/actions/runs/42168557657) completed SUCCESS on this exact SHA. PR #1322 exact-head validation [#42168470421](https://github.com/phanthienquoc/platform-infra/actions/runs/42168470421) also passed before merge.
- Latest production reconcile in current run history remains [#42167232258](https://github.com/phanthienquoc/platform-infra/actions/runs/42167232258), SUCCESS at 05:14:26Z on an earlier commit, with `ALLOW_IMAGE_CHANGES=false`. Later PRs changed inspection/docs rather than production image or workload manifests; no new apply was required by this checkpoint.
- Unrelated open drafts: Platform #1314 mail-service plan and #544/#541/#539 Keycloak documentation. Authentication #75/#76 remain open. No PR is open in TCE, StockDividend or Media.

### TCE health and schedule delivery — exact failure diagnosis

- WF-06 workflow file remains active and its schedule declaration is unchanged at `*/15 * * * *`. The public health contract still expects HTTP 200 for all four endpoints.
- Latest observed native scheduled WF-06 run is [#42133793538](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133793538), created 2026-11-06 00:01:48Z, conclusion FAILURE.
- WF-06 [#42158243093](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158243093) at 03:43:21Z is a `workflow_dispatch` fallback, not a native schedule. Its four independent jobs all returned HTTP 503 (expected 200): TCE web, TCE API `/api/health`, Auth liveness `/api/health`, and Auth readiness `/api/ready`.
- WF-12 [#42158209117](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158209117) ran on its own native schedule at 03:43:01Z. It confirmed WF-06 is active, then detected that the latest native scheduled WF-06 run was 221 minutes old (budget 25 minutes). Its authenticated Platform heartbeat dispatch succeeded; the schedule-freshness job correctly failed.
- WF-13 [#42158228852](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158228852) completed the read-only fallback dispatch. A fallback dispatch is explicitly not native schedule evidence and did not restore HTTP 200 health.
- The committed K3s snapshot still reports TCE frontend/service and Auth/Keycloak desired at 0/0. The 503s are therefore consistent with the recorded inactive runtime state; do not weaken the 200 assertions or turn a dispatch fallback into a green native schedule.
- This is a GitHub scheduled-event delivery gap plus intentionally inactive public services, not evidence that the app CI/build is failing. Do not change any TCE market-scan schedule or cron declaration.

### Other app CI and release evidence

- StockDividend master CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) SUCCESS, including ARM64 build-only checks for Admin, Backend and Scraper. These jobs use non-publishing CI and do not prove a GHCR release, digest, provenance or production authorization. The deployed Stock Admin/new Backend image issue remains unresolved; no promotion of tag `12d63b4`.
- Media Generation master CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) SUCCESS but is historical. No new release/publisher run or Platform handoff was observed.
- Authentication master CI [#42167100692](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42167100692) SUCCESS, including ARM64 build-only validation. No new publisher run, registry digest/provenance or promotion was observed. Keep PR #75/#76 gated by authoritative Supabase production integration side-effect/migration evidence.

### Latest committed K3s/storage evidence

- Latest read-only inspection remains [#42168105492](https://github.com/phanthienquoc/platform-infra/actions/runs/42168105492), snapshot generated 2026-11-06 05:23:12Z. No newer inspect-vps run was present in the inspected Platform Actions history.
- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk 56%, about 19 GiB available RAM, `restart_required=yes`. No reboot/upgrade is authorized.
- GitOps drift clean. Media backend/frontend remain 1/1 Running. Stock Admin (two Pods) and newer Backend remain ImagePullBackOff; legacy Backend/Frontend remain 1/1.
- Only `k3s-debug/k3s-debug-logs` PVC/PV appears in the snapshot; no Stock/Media PVC/PV claims or VolumeSnapshot/VolumeSnapshotContent references were listed. This does not prove external database/object-storage backups or DNS/data ownership.
- Dedicated Media runner is still active and enabled with `/opt/media-actions-runner/bin/Runner.Listener` present. Decommission guard must continue to block. Do not touch the shared Platform runner.

### Dependency-safe next actions

1. Investigate missing native WF-06 schedule events through GitHub Actions scheduling/operational support; retain the existing 15-minute healthcheck cadence and strict HTTP 200 probes. WF-13 fallback is recovery-only, not schedule proof.
2. Keep TCE/Auth services at their declared 0/0 until the service owner authorizes activation; do not change TCE market-scan schedule.
3. Operator verifies the dedicated Media runner is idle, then stops/disables/unregisters only that runner and confirms no Listener remains. No automation may attest this on the operator's behalf.
4. Repeat read-only K3s/storage preflight in the same maintenance window and obtain backup/external-data/DNS ownership review before considering the protected namespace-decommission workflow.
5. Keep Stock/Auth promotion blocked until an authorized publisher run proves exact full-source SHA, GHCR digest, ARM64 manifest and provenance; routine reconcile keeps image changes disabled.

**Ownership and safety:** app repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No production image, desired replica, namespace, PVC/PV, DNS, external database, runner, host or TCE market-scan schedule was changed by this checkpoint.

---

## Workflow inventory runtime update — 2026-11-06 12:26 ICT / 05:26 UTC

- **Default-branch heads:** Platform Infra `70dc56818596dd329e0eb055394d2bfde125b8ac`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `3aeaf519b7a786d13dcecee763acaca357c47ddd`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `3a8031196f21c4240b617bbd0a623fce2dc56c5e`.
- **Open PRs:** Platform #1314 (draft mail-service plan) and #544/#541/#539 (Keycloak documentation drafts); Authentication #75 (ready) and #76 (draft); no PRs in TCE, StockDividend or Media Generation. Platform #1320/#1321 merged after exact-head validation.
- **Platform PR #1320:** added names-only Stock/Media VolumeSnapshot and VolumeSnapshotContent inventory to the read-only VPS snapshot, using the root-owned `platform-kubectl inventory-namespace` wrapper. Exact-head `validate-manifests` #42167697233 and `validate-github-actions` #42167697100 PASS; squash merge `7943360e08e12d882c762484f95570682a1ef041`.
- **Platform PR #1321:** refreshed `debug/vps-latest.md` through read-only `inspect-vps` #42168105492. Inspection generated at 05:23:12Z, exact inspection PR validation #42168230639 PASS, squash merge `70dc56818596dd329e0eb055394d2bfde125b8ac`. Post-merge manifest/action validation #42168105545/#42168105411 PASS.
- **Platform production:** latest returned reconcile #42167232258 PASS at 05:14:26Z with `ALLOW_IMAGE_CHANGES=false`; it predates the two read-only inspection merges. No production reconcile or image promotion was needed for these changes. Recovery/watchdog workflow_run events after inspection were skipped by guards, not native schedule evidence.
- **K3s snapshot #42168105492:** node Ready/ARM64, K3s v1.36.3+k3s1, disk 56%, ~19 GiB available RAM, GitOps drift clean, restart_required=yes. Media backend/frontend 1/1; Stock Admin 0/1 with two ImagePullBackOff Pods, new Backend tag `12d63b4` ImagePullBackOff (no ARM64 manifest), old Backend/Frontend 1/1. TCE frontend/service and Auth/Keycloak desired 0/0. Do not reboot or change replicas.
- **Storage/decommission evidence:** only `k3s-debug/k3s-debug-logs` PVC/PV is listed; Stock/Media VolumeSnapshot references are `none`. This does not establish external database/object-storage backup or ownership. Media runner service remains active/enabled and `Runner.Listener` exists; retirement guard still blocks decommission. No namespace/resource/storage/runner deletion was performed.
- **TCE:** WF-06 #42158243093 fails all four public HTTP probes with 503. WF-12 #42158209117 fails stale native schedule freshness despite successful Platform heartbeat. WF-13 #42158228852 successfully dispatches a read-only fallback that also fails health. Keep strict HTTP 200 checks; do not alter market-scan cron.
- **Stock:** master CI #42167088130 PASS, including native ARM64 non-publishing builds for Admin/Backend/Scraper. The exploratory branch run #42166117405 is superseded by the same contract now on master. No new GHCR publication, digest/provenance, release authorization or production promotion; deployed tag `12d63b4` remains invalid for ARM64.
- **Media:** master CI #42136991059 PASS (historical); no new publisher. Keep app CI/publisher ownership and no Platform dispatch.
- **Authentication:** master CI #42167100692 PASS, including native ARM64 non-publishing build and architecture check. Release remains manual-only; no new publisher/digest/provenance. PR #75/#76 still gated on Supabase production integration side-effect evidence and exact-head checks.
- **Ownership:** preserve app-owned CI/tests/builds and immutable GHCR publication; Platform-owned manifests, shared pull credentials, digest/provenance validation, GitOps promotion/reconcile, rollout and health. `reconcile-vps.yml` is the sole production apply authority; `inspect-vps.yml` is read-only. Preserve useful CI/security/manual/release/scheduled jobs and avoid duplicate SSH/Compose deployment paths. TCE market-scan schedule unchanged.

### Next actions

1. Operator retires only the dedicated Media runner after verifying it is idle; unregister and verify no Listener remains.
2. Obtain same-window fresh storage inventory and independent external-data/backup/DNS review before protected namespace decommission.
3. Fix TCE healthcheck schedule delivery without changing market-scan cron or weakening HTTP 200 assertions.
4. Keep Stock/Auth image publication and promotion gated until fresh authorized publisher evidence proves full-SHA tag, registry digest, ARM64 manifest and provenance.


## Workflow inventory runtime update — 2026-11-06 10:21 ICT / 03:21 UTC

- **Default-branch heads:** Platform Infra `40db4f6378d7f9cf21d830100fe0548e2197cc65`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `6fcefa6b3792dab92b6d5c438001633d25f1ca28`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. Platform PR #1310 (runner-state guard) and #1311 (readiness evidence) are merged.
- **Platform validation/reconcile:** master manifest validation [#42156021306](https://github.com/phanthienquoc/platform-infra/actions/runs/42156021306) PASS on exact head `40db4f6378d7f9cf21d830100fe0548e2197cc65`. Production reconcile [#42155789344](https://github.com/phanthienquoc/platform-infra/actions/runs/42155789344) PASS on prior head `a75980906ddec00c84dc64112fa87835906a6569`; MicroFE/Auth/TCE lanes and final gate passed, Keycloak skipped.
- **TCE:** native WF-06 [#42133793538](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133793538) failed all four public probes with HTTP 503; WF-12 [#42133822319](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133822319) passed; read-only WF-13 fallback [#42133822204](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133822204) passed. No publisher run or production promotion. Do not change market-scan cron.
- **StockDividend:** CI [#42137523269](https://github.com/phanthienquoc/stockdividend/actions/runs/42137523269) PASS; no new immutable publisher or release.
- **Media Generation:** CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) PASS; no production release/handoff.
- **Authentication:** service CI [#41670642852](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852) PASS on 2026-11-03; no newer publisher run. #75/#76 remain gated by Supabase production side-effect/migration evidence.
- **Runtime/decommission:** latest inspection [#42154756357](https://github.com/phanthienquoc/platform-infra/actions/runs/42154756357), snapshot time 03:09:17Z, shows Media runner service and Listener process active; Media workloads 1/1; Stock Admin/new Backend ImagePullBackOff and older Backend/Frontend 1/1; no target PVC/PV claims. Protected namespace workflow is not eligible to run while runner guard fails. No namespace deletion occurred.
- **Ownership:** app repos retain tests/builds/immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health. Stock/Media app-to-Platform handoffs and Platform GitOps ownership are retired. Preserve useful CI/security/manual/release/scheduled workflows.
- **Outstanding:** retire the dedicated Media runner safely and verify GitHub unregistration; perform fresh same-window storage preflight; keep TCE/Auth legacy-tag migration blocked until authorized exact-source publisher runs and registry digests are verified; investigate TCE/Auth HTTP 503 under zero-replica state without modifying TCE market-scan schedules.

## Workflow inventory runtime update — 2026-11-06 10:18 ICT (2026-11-06 03:18 UTC)

Incremental inventory update to the 10:10 checkpoint below. Platform master is now `a75980906ddec00c84dc64112fa87835906a6569` after PR #1310; the four app-repository heads and their open-PR state are unchanged.

- Platform PR [#1310](https://github.com/phanthienquoc/platform-infra/pull/1310) adds a fail-closed guard to the manual Stock/Media namespace workflow. Before storage preflight or deletion it checks that the exact dedicated Media systemd service is inactive and that no `/opt/media-actions-runner/bin/Runner.Listener` process remains. GitHub runner unregistration remains a required operator attestation; the guard does not claim to verify the GitHub registration.
- Exact PR head `b32b75e4923d9f59ec8a8cc823828e7f5c2c6ba2` passed `validate-github-actions` [#42155669711](https://github.com/phanthienquoc/platform-infra/actions/runs/42155669711) and `validate-manifests` [#42155669700](https://github.com/phanthienquoc/platform-infra/actions/runs/42155669700); PR #1310 was squash-merged as `a75980906ddec00c84dc64112fa87835906a6569`.
- The latest read-only inspection snapshot #1308 (2026-11-06T03:09:17Z) still shows the Media runner service active. Therefore, the new guard would currently stop the manual decommission workflow before namespace deletion. It does not stop or unregister the runner.
- The same snapshot shows only the `k3s-debug` PVC/PV claim and no target-namespace PVC/PV claims. The workflow will still repeat its same-window storage preflight; backup/external-data review and runner retirement remain mandatory.
- Stock/Media namespaces, Services, Ingresses and workloads remain in K3s. Media backend/frontend are 1/1; Stock Admin and the newer Backend remain ImagePullBackOff because their ARM64 image manifests are unavailable; older Stock Backend and legacy Frontend remain 1/1. No workload or namespace was deleted.
- TCE and Auth still use legacy production tags in GitOps. No new publisher release or digest promotion was initiated. TCE schedule and all cron declarations remain unchanged.

Next action: the service owner must review backups/external-data ownership, stop the dedicated Media runner when idle, unregister it from the Media repository, and then use the protected manual workflow with its exact typed confirmations. Do not remove the shared Platform runner or delete PV/external data/DNS/GHCR packages.

---

## Workflow inventory runtime update — 2026-11-06 10:10 ICT (2026-11-06 03:10 UTC)

This inventory checkpoint follows the successful merge of Platform PR #1307. It records current repository heads, exact-head validation, the remaining digest-promotion and K3s decommission gates, and the latest live cluster evidence retrieved in this pass.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `221d928575a9d9999827fcce5625f2cc06c9f9c6` | #544/#541/#539 drafts | PR #1307 merged; TCE source publisher job/step provenance is now enforced. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; WF-02 and WF-05 checks passed. No production release dispatched. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 removed the retired Platform handoff; CI passed. Publisher remains build/publish-only. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 removed the retired Platform handoff; CI passed. Publisher remains build/publish-only. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | PR #87 established digest/provenance handoff; #75/#76 remain gated on Supabase integration and migration review. |

### Exact workflow and merge evidence

- Platform inspection-only PR [#1308](https://github.com/phanthienquoc/platform-infra/pull/1308) refreshed `debug/vps-latest.md` at 2026-11-06T03:09:17Z. It confirms the Media runner is still active, no target-namespace PVC/PV claims are present, Media backend/frontend are 1/1, and Stock Admin/new Backend still have permanent ARM64 image-manifest pull failures. This snapshot changes no production manifests.

- Platform PR [#1307](https://github.com/phanthienquoc/platform-infra/pull/1307) strengthened `verify-tce-publisher-run.sh`: a successful top-level TCE Actions run is no longer sufficient. The verifier now requires the exact release dependency jobs, native ARM64 frontend/backend build and artifact-integrity steps, GHCR publication, registry digest/ARM64 verification, and Platform dispatch correlation to be completed-success.
- Exact PR head `248802e05fa397b37d573749bf75be8bc57e2e45` passed `validate-github-actions` [#42154577734](https://github.com/phanthienquoc/platform-infra/actions/runs/42154577734) and `validate-manifests` [#42154577576](https://github.com/phanthienquoc/platform-infra/actions/runs/42154577576). PR #1307 was squash-merged as `67e8d8746934ec40b60b0fe0f62c5e4b3bcccfc2`.
- Platform production reconcile [#42150629183](https://github.com/phanthienquoc/platform-infra/actions/runs/42150629183) completed SUCCESS: policy v15 verified, scope `all`, mode `apply`, `ALLOW_IMAGE_CHANGES=false`; MicroFE, TCE and Auth lanes passed, Keycloak lane skipped, and post-apply GitOps drift was clean. Recovery controller [#42150853420](https://github.com/phanthienquoc/platform-infra/actions/runs/42150853420) also completed SUCCESS.
- TCE PR #1026: WF-02 [#42105124810](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42105124810) and WF-05 [#42105124578](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42105124578) passed.
- StockDividend PR #32: CI [#42137106072](https://github.com/phanthienquoc/stockdividend/actions/runs/42137106072) passed.
- Media Generation PR #72: CI [#42135150058](https://github.com/phanthienquoc/media-generation/actions/runs/42135150058) passed.
- Authentication PR #87: auth-service CI [#41642031980](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41642031980) passed. This is historical PR evidence, not a new Auth production release run.
- No TCE, StockDividend, Media Generation, or Auth production publisher was dispatched in this checkpoint. App CI success is not production-release authorization.

### Stock/Media retirement: GitOps is removed; K3s workloads remain

- Platform PR #1301 retired Stock/Media GitOps ownership; PRs #1303/#1304 fixed push-scope classification/reconciliation; PR #1305 removed obsolete Stock/Media smoke/helper contracts. Stock PR #32 and Media PR #72 removed app-to-Platform production handoffs.
- The live Pod listing in reconcile #42150629183 at 2026-11-06T02:30:17Z still showed Media backend and frontend 1/1 Running. Stock Admin had two 0/1 ErrImagePull/ImagePullBackOff Pods; the legacy Backend and Frontend remained 1/1; a newer Backend Pod was 0/1 ImagePullBackOff. These are now orphaned from Platform GitOps ownership and were not deleted by reconcile.
- The latest committed read-only inspection snapshot is Platform PR #1308, generated at 2026-11-06T03:09:17Z. It shows only the k3s-debug PVC/PV claim and no PVC/PV claims in stock-prod or media-prod. This is fresh evidence of no target claims, but the protected manual workflow must repeat its same-window preflight immediately before deletion. The snapshot still shows the dedicated Media runner service active; no stop/unregister proof exists.
- The manual-only `decommission-stock-media` workflow has not run. Namespace deletion remains blocked on a fresh same-window object/PVC/PV/StorageClass inventory, backup and external-data ownership review, and independent confirmation that the dedicated Media runner is idle, stopped and unregistered. The protected production Environment and three typed confirmations remain mandatory. Preserve PVs, external databases/object storage, DNS, GHCR packages, app repositories and the shared Platform runner.

### Immutable digest promotion remains outstanding

- TCE production Kustomize still uses legacy paired tag `prod-v0.1.0-e75e338` for web/service; Auth still uses `prod-v1.0.0-ceb2688`. New publishers produce full-source-SHA tags and registry digests, and Platform validates provenance, but no new authorized TCE/Auth release was initiated to replace these references.
- Do not copy a digest from a historical node snapshot or infer it from a tag. Obtain a successful exact publisher run and registry-confirmed digest through the normal app-owned release workflow, then let Platform create the narrow digest-promotion PR. Routine reconcile keeps image changes disabled.
- Auth PR #75/#76 remain gated on authoritative Supabase production integration side-effect and migration-drift evidence. No migration or Auth activation was run.

### Next dependency-safe actions

1. Obtain a fresh read-only `inspect-vps` result and confirm current PVC/PV/StorageClass inventory and dedicated Media runner state.
2. After the service owner confirms backups/external-data retention and the Media runner is independently idle/stopped/unregistered, use only the protected manual namespace-decommission workflow. Do not delete storage or external resources implicitly.
3. Keep TCE/Auth digest promotion manual and provenance-bound; do not dispatch a production publisher without explicit release authorization.
4. Resolve Auth #75/#76 production Supabase/migration gates and verify one real qualifying TCE WF-13 recovery sequence without changing any cron declaration.

No TCE market-scan schedule, production image reference, desired replica count, shared credential, external database, DNS record, K3s namespace or PV was changed in this checkpoint. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.


---

## Workflow inventory runtime update — 2026-11-06 09:33 ICT / 02:33 UTC

### Current five-repository ownership and evidence

| Repository | Current default-branch SHA | Workflow ownership | Latest evidence |
|---|---|---|---|
| Platform Infra | d6f45057f4a7eaba4c81d897aa64d9e5feb67fa1 | Production manifests, shared GHCR pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. | PR #1304 merged; post-merge validations #42150629257/#42150629258/#42150629301 and reconcile #42150629183 passed. |
| TCE Dashboard | 512b69d837e2a65c39867a062529a7fa0eada4cc | App tests/builds/manual immutable publisher; Platform validates provenance/digests and owns production rollout. | WF-06 #42133793538 failed strict public probes with HTTP 503 under the zero-replica state; WF-13 #42133822204 passed read-only. |
| StockDividend | 6fcefa6b3792dab92b6d5c438001633d25f1ca28 | App CI/builds/immutable GHCR publication; no Stock GitOps or Platform publisher receiver remains. | Master CI #42137523269 passed. No production publisher dispatch. |
| Media Generation | 3a8846a4f273eeb20a55b214d5ad80804c2d8d52 | App CI/builds/paired immutable GHCR publication; no Media GitOps or Platform publisher receiver remains. | Master CI #42136991059 passed. No production release dispatch. |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | App CI/manual immutable publisher; Platform verifies provenance and promotes Auth digests. | Master CI #41670642852 passed; PR #75/#76 remain gated. |

### Platform reconcile and rollout evidence

- PR #1304 merged from exact head 29dffd589c800ef3e3a545be128182ace615718a as d6f45057f4a7eaba4c81d897aa64d9e5feb67fa1 after visible exact-head checks #42149835243, #42149835246 and #42149835326 passed.
- Post-merge validations #42150629257, #42150629258 and #42150629301 passed on the new master SHA.
- Reconcile #42150629183 resolved scope all, mode apply and ALLOW_IMAGE_CHANGES=false. GHCR access, Auth runtime Secret provisioning, shared pull credential reconciliation, restart checks and TCE pair validation passed. Preflight detected drift; the image guard found no workload image replacement; manifest apply and post-apply drift verification passed.
- MicroFE, TCE and Auth lanes passed; Keycloak lane skipped. TCE/Auth remained intentionally zero replicas and passed their zero-replica health gates. Recovery controller #42150853420 passed for the source reconcile.
- Optional TCE deployment-start event failed to connect to local 127.0.0.1:18080; continue-on-error prevented this telemetry issue from changing the deployment result.
- The run still observed Stock/Media workloads in K3s. GitOps removal does not prune old namespaced resources; the manual decommission workflow has not run.

### App publisher and payload contracts

- StockDividend deploy.yml keeps app-owned CI/builds, immutable source-SHA publication, ARM64 verification and its explicit manual production hold; no Platform repository_dispatch remains.
- Media wf-03-media-production-deploy.yml keeps paired immutable full-SHA image publication, digest and ARM64 verification; no Platform dispatch remains.
- TCE wf-03-tce-production-deploy.yml is workflow_dispatch-only, validates master/full-source SHA, paired registry digests, ARM64 and tce-release-requested payload provenance.
- Authentication release.yml is workflow_dispatch-only, validates immutable tags/digest/ARM64 and sends auth-image-published with source run/workflow/event/SHA evidence.
- Platform gitops-image-promotion.yml remains the shared digest/provenance receiver; reconcile-vps.yml remains the sole routine production apply authority; inspect-vps.yml remains read-only.

### Known follow-ups

- TCE production Kustomize still uses legacy paired tag prod-v0.1.0-e75e338; Auth still uses legacy tag prod-v1.0.0-ceb2688. Current publisher workflows emit full-source-SHA tags and registry digests, but no new authorized publisher dispatch has pinned these existing manifests to digest. Do not substitute stale containerd cache digests; obtain registry-confirmed provenance before atomic digest promotion.
- Stock/Media namespaces and workloads remain present after GitOps retirement. Fresh PVC/PV/StorageClass inventory, backup/external-data review and independent Media-runner retirement are still required before the protected manual namespace workflow.
- The optional local deployment event bridge at 127.0.0.1:18080 refused the connection during reconcile #42150629183. Diagnose without making it a hard deployment gate unless the event contract is deliberately changed.
- Auth #75/#76 stay gated because Supabase Preview is skipped and production migration side effects remain unresolved.
- Preserve all TCE schedules, especially the market-scan schedule; no schedule declaration was changed.

---

## Workflow inventory runtime update — 2026-11-06 09:15 ICT / 02:15 UTC

### Current workflow ownership and refs

| Repository | Current default-branch SHA | Ownership boundary | Latest evidence |
|---|---|---|---|
| Platform Infra | `e66bdecea35eda2c6740587b87ff69415c4176fa` | Production manifests, shared GHCR pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. | PR #1303 merged; PR #1304 adds the missing reconcile push trigger for resolver changes. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | App tests/builds/manual publisher; Platform validates paired digests and owns production rollout. | WF-06 #42133793538 returned HTTP 503 on four strict public probes under the documented zero-replica state; WF-13 #42133822204 passed read-only. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | App CI/builds/immutable GHCR publication; no Stock GitOps or publisher receiver remains on Platform. | PR #32 merged; latest master CI #42137523269 passed. No publisher dispatch. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | App CI/builds/paired immutable GHCR publication; no Media GitOps or publisher receiver remains on Platform. | PR #72 merged; latest master CI #42136991059 passed. No production release dispatch. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | App CI/manual immutable publisher; Platform verifies source provenance and promotes the Auth digest. | Master CI #41670642852 passed; PR #75 validation passed, Supabase Preview skipped, #75/#76 gated. |

### Publication and dispatch contracts

- **StockDividend:** `.github/workflows/deploy.yml` retains a manual production publication hold, immutable source-SHA tags, registry digest resolution and ARM64 checks. No Platform `repository_dispatch` remains.
- **Media Generation:** `.github/workflows/wf-03-media-production-deploy.yml` retains immutable `prod-v<semver>-<full SHA>` tags, paired frontend/backend digest verification and ARM64 checks. No Platform `repository_dispatch` remains.
- **TCE Dashboard:** `wf-03-tce-production-deploy.yml` is `workflow_dispatch` only for production. It publishes full-source-SHA tags, verifies the web/service digest pair and ARM64 manifests, and validates `tce-release-requested` fields including source run ID, workflow path, event and full source SHA. Platform verifies publisher provenance and tag-to-digest correlation before atomic GitOps promotion.
- **Authentication:** `release.yml` is `workflow_dispatch` only. It verifies immutable source-SHA/semver tags, registry digest and ARM64, then sends `auth-image-published` with app/component, source commit, tag, digest, source run ID, workflow path, event and full source SHA. Platform verifies the source run and digest before promotion.
- **Platform:** `gitops-image-promotion.yml` remains the shared image-promotion receiver. `reconcile-vps.yml` remains the sole routine production apply authority. `inspect-vps.yml` remains read-only. No duplicate app-owned SSH/Compose/kubectl deployment authority was added.

### Stock/Media Platform retirement and decommission guard

- PR #1301 removed Stock/Media manifest trees, production composition entries, reconcile/rollout/health/recovery/GHCR contracts and obsolete dedicated helper files. PR #1296 was closed as superseded.
- PR #1303 fixed the path resolver after master push reconcile #42146800843 failed on the deleted `scripts/bootstrap-media-runner.sh`; the failed run stopped before any cluster mutation. PR #1303's final exact-head `validate-github-actions` #42148684639 and `validate-manifests` #42148684820 passed; merge SHA is `e66bdecea35eda2c6740587b87ff69415c4176fa`.
- The reconcile push filter did not include the resolver file, so the resolver fix itself did not trigger another production reconcile. PR #1304 adds that path, enforces it in the workflow contract validator, and tests the full PR #1301 changed-path fixture. On merge, the existing production workflow will run with scope `all`, apply mode and image changes disabled, under its protected production Environment.
- `decommission-stock-media.yml` remains manual-only with no runs. It requires namespace, backup/external-data and dedicated Media-runner confirmations plus fresh storage preflight. No K3s namespace/PV, DNS, GHCR package, external data or runner registration has been deleted.

### Workflow preservation and schedule safety

- Keep app CI/test/security workflows and purposeful manual/release/scheduled workflows. No workflow was removed solely because it was inactive or historical.
- Preserve strict HTTP 200 health gates. TCE WF-06 HTTP 503 is consistent with operator-requested zero replicas; no replica or health threshold change is authorized here.
- Preserve every TCE schedule, especially the market-scan schedule. No schedule changed.
- The last committed K3s snapshot is stale and lacks fresh PVC/PV/StorageClass inventory; no destructive operation is permitted from that snapshot.

### Current next dependency

Poll PR #1304 exact-head checks and squash-merge only after all required checks pass. Then verify the merge-triggered `reconcile-vps` run before any separate manual K3s namespace decommission. Keep Auth #75/#76 gated on the unresolved Supabase production integration effect.

---

## Workflow inventory runtime update — 2026-11-06 09:10 ICT / 02:10 UTC

### Five-repository workflow ownership

| Repository | Current head | Workflow owner boundary | Latest relevant CI / PR evidence |
|---|---|---|---|
| Platform Infra | `d05f806c636f3e785ffe603efff204767308efa0` | Production manifests, shared GHCR pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. | Retirement PR #1301 merged; post-merge push reconcile #42146800843 exposed a push-scope regression. Fix PR #1303 has passing code-only validation runs #42148457914/#42148457910; docs update requires fresh exact-head checks. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | App tests/builds and manual production publisher; Platform owns paired digest promotion and cluster rollout. | WF-06 #42133793538 failed four strict public probes with HTTP 503 under the documented zero-replica state; WF-13 #42133822204 passed read-only. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | App CI/builds/immutable GHCR publication; Platform no longer owns Stock manifests or publisher receiver. | PR #32 merged; latest master CI #42137523269 passed. No production publisher dispatch or Platform handoff. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | App CI/builds/paired immutable GHCR publication; Platform no longer owns Media manifests or publisher receiver. | PR #72 merged; latest master CI #42136991059 passed. No production release dispatch or Platform handoff. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | App CI and manual immutable publisher; Platform validates source provenance and promotes the Auth digest. | Master CI #41670642852 passed; PR #75 validation passed but Supabase Preview is skipped. #75/#76 remain gated. |

### Publication and dispatch contract audit

- **StockDividend:** `.github/workflows/deploy.yml` remains app-owned and retains a manual publication hold, immutable source-SHA release tags, registry digest resolution and ARM64 verification. The merged workflow contains no Platform repository-dispatch event.
- **Media Generation:** `.github/workflows/wf-03-media-production-deploy.yml` retains immutable `prod-v<semver>-<full SHA>` tags, paired frontend/backend registry digest verification and ARM64 checks. The merged workflow contains no Platform repository-dispatch event.
- **TCE Dashboard:** `wf-03-tce-production-deploy.yml` is `workflow_dispatch` only for production. It publishes full-source-SHA tags, resolves both web/service digests, verifies ARM64 manifests, and constructs/validates `tce-release-requested` with app, release, both digests, source run ID, workflow path, event and full source SHA. Platform validates provenance and tag-to-digest correlation before paired GitOps promotion.
- **Authentication:** `release.yml` is `workflow_dispatch` only. It publishes immutable source-SHA and semver/SHA tags, verifies the registry digest and ARM64 manifest, then sends `auth-image-published` with app/component, source commit, tag, digest, source run ID, workflow path, event and full source SHA. Platform validates the publisher run and digest before changing the Auth Kustomize digest.
- **Platform:** `gitops-image-promotion.yml` remains the only app-image promotion receiver. `reconcile-vps.yml` remains the only routine production apply authority. `inspect-vps.yml` remains read-only. No duplicate app-owned SSH/Compose/kubectl production deployment path was introduced.

### Workflow preservation and retirement status

- Stock/Media-specific GitOps manifests, health/recovery lanes, GHCR namespace setup and obsolete publisher/runner helpers were removed by merged Platform PR #1301. The app repositories and GHCR packages were not deleted.
- `decommission-stock-media.yml` is intentionally retained as a manual-only, protected-Environment workflow. It has no runs; its three typed confirmations and fresh storage preflight are not a substitute for independent backup, external-data and dedicated-runner checks.
- Useful CI/test/security, manual release, observability, inspection, reconciliation, recovery, cleanup and TCE scheduled workflows remain. No workflow was removed solely because it was not recently active.
- TCE WF-06's HTTP 503 result is consistent with the operator-requested zero replicas. Keep the strict health gates and every TCE schedule, especially the market-scan schedule, unchanged.

### Post-merge push-scope regression and repair

- Platform master reconcile #42146800843 failed before any cluster mutation because `scripts/resolve-push-deployment-scope.sh` did not classify the deleted `scripts/bootstrap-media-runner.sh`. Preflight, credential bootstrap, manifest apply and app lanes were skipped.
- PR #1303 adds explicit non-deploying classifications for retired/manual-only helpers and validator-only paths, keeps GHCR pull-access validation cluster-wide, and makes changes to the resolver itself trigger `all`. Regression tests prove helper-only pushes fail closed while the complete retirement path set resolves cluster-wide.
- Code-only exact-head checks passed: `validate-github-actions` #42148457914 and `validate-manifests` #42148457910. The tracker update in PR #1303 changes the head, so revalidate the final PR revision before merge.

### Current next dependency

Poll PR #1303 exact-head checks, then squash-merge only after success. Verify the merge-triggered reconciliation run before doing any live K3s operation. Namespace deletion remains separately gated on a fresh PVC/PV/StorageClass inventory, backup/external-data review and confirmed Media runner retirement. No TCE market-scan schedule change.

---

## Workflow inventory runtime update — 2026-11-06 08:38 ICT / 01:38 UTC

- **Default-branch refs:** Platform Infra `b1a0c185e3f97630aa2bf55945bb5f674200bf97`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `6fcefa6b3792dab92b6d5c438001633d25f1ca28`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1301 ready, #1296/#544/#541/#539 draft; Auth #75 ready/#76 draft; none in TCE, StockDividend or Media.
- **Stock publisher:** PR #32 merged; post-merge StockDividend CI #42137523269 PASS. The app retains ARM64 immutable publication and manual release hold; no new publisher run, Platform dispatch, or production promotion after merge.
- **Media publisher:** PR #72 merged; post-merge Media CI #42136991059 PASS. The app retains paired immutable full-source-SHA GHCR digest verification and no longer sends Platform dispatches; no production release was triggered.
- **Platform decommission PR #1301:** exact head `dce6ae5341ce925177156f5fd9b537c453589323`, 10 commits ahead/0 behind. It removes 19 Stock/Media manifest files and six obsolete app-specific helper files, removes their active reconcile/health/recovery/GHCR/dispatch contracts, and adds a manual-only storage-gated namespace workflow. Exact-head checks #42145176538/#42145176539/#42145176540 are queued; do not merge until all required checks pass on the final head.
- **Decommission guard:** workflow requires `DELETE-STOCK-PROD-AND-MEDIA-PROD`, `BACKUP-AND-EXTERNAL-DATA-REVIEWED`, and `MEDIA-RUNNER-STOPPED-AND-UNREGISTERED`. Preflight inventories all namespaced object names without printing Secret/ConfigMap values, then checks PVCs, PV claims and StorageClasses. Namespace deletion remains unexecuted; PVs, DNS, GHCR packages, external data and app repositories are preserved.
- **Previous branch runs:** #42141922040 and #42142089191 were on older branch commits; they are not current-head checks. Master validation runs #42137791277/#42137885767 passed before this PR.
- **Runtime evidence:** read-only snapshot #42131886966 was generated at 23:46:15Z and is stale for deletion; it omits PVC/PV/StorageClass inventory and last showed the dedicated Media runner active. Current runner state is unverified; no K3s namespace deletion or runner unregister was performed.
- **TCE:** native WF-06 #42133793538 failed four strict public HTTP 200 probes with 503 while TCE/Auth/Keycloak remain operator-scaled to zero; WF-13 fallback #42133822204 passed and remained read-only. TCE market-scan schedule unchanged.
- **Authentication:** PR #75/#76 remain gated; their last validate runs #40446492086/#41329425940 are historical and Supabase Preview is SKIPPED. No migration or release.
- **Ownership:** app repos own tests/builds/immutable GHCR publication; Platform owns remaining manifests/shared pull credentials/provenance/promotion/reconcile/rollout/health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. Preserve useful CI/security/manual/release/scheduled workflows and avoid duplicate SSH/Compose deployment paths.

## Workflow inventory runtime update — 2026-11-06 07:29 ICT / 00:29 UTC

- **Default-branch refs:** Platform Infra `3346be7997d017bd45eb0782331a7dafb9bb571c`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1296 draft plus #544/#541/#539 drafts; Stock #32 at head `c015961ec45ce7b698ea8fde9e2d7e9b5fe3c4f0`; Auth #75 ready/#76 draft; none in TCE or Media.
- **Media publisher:** PR #72 merged as `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`. Exact-head PR/push checks #42135150058/#42135140342 and post-merge push #42136991059 PASS. Media publisher is now GHCR-only: paired immutable full-SHA images, registry digests and ARM64 manifests are verified; no Platform dispatch is sent.
- **Stock publisher:** PR #32 removes the Platform handoff while preserving app-owned CI and ARM64 immutable publication. The first contract run exposed stale assertions; the follow-up fixes are at exact head `c015961ec45ce7b698ea8fde9e2d7e9b5fe3c4f0`. Run #42137106072 is queued/in progress; no merge until its exact-head checks complete successfully.
- **Platform inventory:** PR #1296 remains a plan-only draft at head `7a14b32c86aeb0d281c4ae74b48ba5ad28fc13ae`, exact-head validate-manifests #42131770950 PASS. The receiver workflow, Stock/Media manifest trees, health/recovery branches and shared namespace bootstrap references still exist on Platform master; removal is the next code PR after Stock publisher contract is merged.
- **Runtime evidence:** native inspect #42112599830 PASS; read-only manual inspect #42131886966 PASS with snapshot generated 23:46:15Z. Media backend/frontend 1/1; Stock Admin and new Backend Pods ImagePullBackOff; old Backend and legacy Frontend 1/1. Media runner service active. Snapshot omits PVC/PV/StorageClass inventory and is not authorization for namespace deletion.
- **Platform native schedules:** reconcile #42121826106 FAIL only Stock health; recovery #42121354158 PASS; watchdog #42123445690 PASS. Keep native schedule evidence distinct from dispatch fallbacks.
- **TCE:** WF-06 #42133793538 failed four strict public HTTP 200 probes with 503 while TCE/Auth/Keycloak remain operator-scaled to zero; WF-13 fallback #42133822204 PASS and read-only. No schedule/replica/health-gate changes; TCE market-scan schedule unchanged.
- **Authentication:** #75/#76 remain gated on authoritative Supabase production integration side-effect verification; Preview skipped. No migration, branch or release mutation.
- **Ownership:** app repos own tests/builds/immutable GHCR; Platform owns manifests/shared pull credentials/provenance/promotion/reconcile/rollout/health. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` read-only. Preserve useful CI/security/manual/release/scheduled workflows and avoid duplicate SSH/Compose deployment paths.
- **Next:** finish Stock #32 exact-head checks; then remove Stock/Media Platform receiver and runtime contracts through a dedicated PR; add PVC/PV/storage evidence and explicit approval before any namespace deletion. No production image/manifest/credential/database/replica/host/namespace/DNS/PV/cron mutation; TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 04:56 ICT / 2026-11-05 21:56 UTC

- **Default-branch heads:** Platform Infra 419b83666cae7773b0a1dbc62900f275add05d9d; TCE Dashboard 512b69d837e2a65c39867a062529a7fa0eada4cc; StockDividend 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media Generation e4c7d8990aafc7d837e918c9caf39722d623de7c; Authentication f978a3f378ee22d4630909c2d182275b21ac9e9a.
- **Open PRs:** Platform #544/#541/#539 remain drafts; Auth #75 is ready and #76 draft; no open PRs in TCE, StockDividend or Media.
- **Native inspection recovery:** inspect-vps #42112599830 ran with event=schedule at 04:26:04 ICT and passed. Its snapshot was generated 04:26:12 ICT; inspection PR #1293 exact-head validation passed and the PR was squash-merged as current Platform master 419b83666cae7773b0a1dbc62900f275add05d9d.
- **Reconciliation:** #42112833885 is a workflow_dispatch (not schedule), mode=apply, target_app=stockdividend, allow_image_changes=false. Shared GHCR access and credential bootstrap passed. Auth, Media, MicroFE and TCE lanes passed; Keycloak skipped; Stock lane and final gate failed on the known ARM64 manifest mismatch for Admin/Backend tag 12d63b4.
- **Image-pull restart guard:** the production runner helper classified Stock Admin and Backend errors as permanent no-match-for-platform failures and skipped rollout restart. scripts/tests/restart-blocked-image-pulls.test.sh already covers permanent, transient, mixed and unrelated waiting failures. No additional restart authority or duplicate fix is needed.
- **Recovery:** #42113114275 workflow_dispatch recovery after source #42112833885 passed at 04:29:33 ICT. This is not native schedule evidence.
- **Native schedule status:** inspect-vps #42112599830 PASS; reconcile-vps latest native remains #42068683835 FAIL Stock health; recover-stale-ops latest native remains #42068414686 PASS; watchdog latest native remains #42070623710 FAIL inspection freshness. The newer reconcile/recovery events are dispatches and must not be counted as schedule ticks. Cron declarations remain unchanged.
- **K3s snapshot at 04:26 ICT:** tce-k3s-01 Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB RAM available, restart_required=yes. Media/MicroFE Shell/WS/NATS 1/1; Stock Admin two Pods and new Backend ImagePullBackOff on 12d63b4; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0 by operator request.
- **TCE:** PR #1026 merged; latest post-merge WF-01/WF-02/WF-05/WF-12 checks passed. No post-merge native WF-07 → WF-12 → WF-13 stale-WF-06 recovery sequence yet. WF-13 remains the only WF-06 fallback dispatcher; WF-12 remains read-only.
- **Stock:** publisher #41563856933 verified immutable ARM64 full-SHA images historically, but production release remained disabled and paired promotion skipped. No explicit release authorization/protected publisher provenance; do not promote.
- **Media/Auth:** latest master CI runs #41617592783 and #41670642852 are Nov 3 historical results. Auth PR #75 ready and #76 draft remain blocked because Supabase Preview is SKIPPED and the Deploy-to-production integration effect is unverified.
- **Ownership remains:** app repos own tests/builds/immutable GHCR publication; Platform owns production manifests, shared GHCR pull credentials, provenance validation, paired promotion, GitOps reconciliation, rollout and health. reconcile-vps.yml is the sole production apply authority; inspect-vps.yml is read-only.
- Preserve useful CI/test/security/manual/release/scheduled workflows. No duplicate SSH/Compose/MCP mutation authority. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 03:56 ICT / 2026-11-05 20:56 UTC

- **Default-branch heads:** Platform Infra `086ee573f29b148bdb6ab55e3faa6a3000a5aa56`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Platform PR #1291:** merged as `086ee573f29b148bdb6ab55e3faa6a3000a5aa56`; exact-head #42105809491 and post-merge #42105916492 PASS. This corrects the pre-merge Platform SHA recorded in the 03:42 tracker entry.
- **Open PRs:** Platform #544/#541/#539 remain drafts; their only observed validation checks are from Oct 14. Auth #75 is ready and #76 is draft; both Supabase Preview checks are SKIPPED, so neither is safe to merge based on current evidence. No open PRs in TCE, StockDividend or Media.
- **TCE PR #1026:** merged at 03:39 ICT. Post-merge WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 #42105365586 all PASS. WF-13 #42105390163 correctly SKIPPED for a WF-12 push-smoke event. No qualifying post-merge native WF-07/WF-12 event has exercised the stale-WF-06 recovery path yet.
- **Platform native schedules:** inspect-vps #42049660972 (Nov 5 21:55 ICT, PASS but stale); reconcile-vps #42068683835 (23:51, Stock health failure); recover-stale-ops #42068414686 (23:49, PASS); watchdog #42070623710 (Nov 6 00:02, inspection freshness failure). No newer native `event=schedule` runs appear in the latest 100-run Actions page. Preserve cron declarations.
- **Inspection fallback:** #42099284088 is `workflow_dispatch`, PASS, snapshot generated 03:00:41 ICT; about 56m old at this checkpoint and within the 75m fallback budget, but not native schedule evidence. Snapshot: node Ready/ARM64, disk 56%, ~19 GiB RAM, `restart_required=yes`; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **Stock:** latest publisher #41563856933 (Nov 3) verified immutable ARM64 full-SHA artifacts; release hold false and paired promotion skipped. Production tag `12d63b4` remains ARM64-incompatible. No authorization to enable the production release gate or promote either half independently.
- **Media/Auth:** latest master CI #41617592783/#41670642852 is historical Nov 3. Auth #75/#76 have stale validation and Supabase Preview SKIPPED; no migration or release dispatch.
- **TCE/Auth health:** confirmed ingress routes to operator-requested zero-replica TCE/Auth/Keycloak Deployments explain public 503 responses. Keep shutdown state and strict HTTP 200 gates; do not restore replicas without explicit operator authorization.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR and source-run/tag/digest provenance; Platform owns production manifests, shared pull credentials, provenance/digest validation, promotion, reconciliation, rollout and health. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only. No duplicate SSH/Compose/MCP mutation authority; no production image/manifest/credential/database/replica/host/cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 03:42 ICT / 2026-11-05 20:42 UTC

- **Repository heads:** Platform Infra `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Auth #75 ready/#76 draft; none in TCE, StockDividend or Media.
- **TCE #1026:** merged as `512b69d837e2a65c39867a062529a7fa0eada4cc`. WF-12 now requires a successful native WF-07 source before running the stale-WF-06 verification path; failed WF-07 still sends the existing heartbeat. Exact-head WF-02/WF-05 passed; post-merge WF-12/WF-02/WF-05 passed; WF-01 build was still in progress at 03:42.
- **TCE recovery E2E:** no post-merge native WF-07/WF-12 event yet. Pre-merge #42098855352/#42098897759 are not proof for #1025/#1026. Native WF-06 #42089383865 and WF-12 #42083178274 remain old failures.
- **TCE/Auth 503:** directly explained by ingress routes to TCE frontend/service and Auth Deployment, all explicitly `replicas: 0` under temporary operator shutdown comments; Keycloak is also zero. Keep shutdown and strict HTTP 200 gates until explicit operator authorization.
- **Platform:** PR #1290 merged as `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6`; exact-head #42104850991 and post-merge #42104919461 passed. Native schedule history remains stale; read-only fallback #42099284088 generated 03:00:41 ICT and is ~41m old at this review.
- **Stock:** current production overlay remains tag-pinned to `12d63b4` for Admin/Backend and fails ARM64 manifest compatibility. Publisher #41563856933 verified new immutable ARM64 full-SHA images but release hold was false; no paired promotion authorization.
- **Media/Auth:** latest master CI #41617592783/#41670642852 is historical Nov 3. Auth Preview remains skipped; no migration.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform owns production manifests, shared pull credentials, provenance/digest validation, promotion, reconciliation, rollout and health. No duplicate SSH/Compose/MCP mutation authority; no production image/manifest/credential/database/replica/host/cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 03:34 ICT / 2026-11-05 20:34 UTC

- **Platform PR #1289:** merged as `f5d62e4a4f9abd992458849929a14a85a3250614`; exact-head #42104285775 PASS and post-merge #42104477168 PASS.
- **TCE PR #1025:** merged as `162390fe4811131c11d3f39d264e0722a826dc0f`; exact-head WF-05/WF-02 and post-merge WF-01/WF-05/WF-02 passed. No qualifying post-merge native WF-07/WF-12 event has yet exercised the new WF-13 stale-WF-06 path.
- **Public 503 root cause now confirmed by GitOps source:** TCE ingress routes to `tce-frontend` and `tce-service`, both explicitly `replicas: 0` under a temporary operator shutdown request. Auth ingress routes to `microfe-auth`, whose Deployment is explicitly `replicas: 0`; Keycloak is also `replicas: 0`. These zero-replica states explain the expected strict public 503 responses. Do not restore replicas or weaken HTTP health checks without explicit operator authorization.
- **Stock:** production overlay still uses `newTag: 12d63b4` for both Admin and Backend. Latest publisher #41563856933 verified immutable ARM64 full-SHA images, but the production hold was false and paired promotion was skipped. The old production tag remains architecture-incompatible; no release authorization.
- **Platform native schedules:** latest native inspect #42049660972, reconcile #42068683835, recovery #42068414686 and watchdog #42070623710 remain the latest native schedule events. The 03:00 inspection #42099284088 was workflow_dispatch fallback, not native schedule evidence. Preserve cron declarations.
- **Auth PRs:** #75 remains ready with exact-head `validate` PASS but `Supabase Preview` SKIPPED and commit status pending; #76 remains draft. Do not merge or run migrations on historical/partial checks.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/credentials/provenance/promotion/reconcile/rollout. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 03:27 ICT / 2026-11-05 20:27 UTC

- **Repository heads:** Platform Infra `9d533e503d412e583873a91aefd66263c297fafa`; TCE Dashboard `162390fe4811131c11d3f39d264e0722a826dc0f`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Authentication #75 ready/#76 draft; none in TCE, StockDividend or Media. Auth Preview checks remain SKIPPED; passing checks on these PRs are historical.
- **TCE PR #1025:** merged at 03:22:34 ICT as `162390fe4811131c11d3f39d264e0722a826dc0f`. Exact-head WF-05 #42102448205 and WF-02 #42102448276 passed; post-merge WF-01 #42102796954, WF-05 #42102795916 and WF-02 #42102795382 passed. New contract lets a successful native WF-07 schedule request WF-13 only after WF-12 proves native WF-06 stale. Pre-merge WF-12 #42098855352 failure and WF-13 #42098897759 skip are not E2E evidence for the merged fix.
- **Platform native schedules:** inspect-vps #42049660972 (Nov 5 21:55 ICT, PASS but stale); reconcile-vps #42068683835 (23:51, Stock health failure); recover-stale-ops #42068414686 (23:49, PASS); watchdog #42070623710 (Nov 6 00:02, inspection freshness failure). No later native `event=schedule` run appears through #42099407335 at 03:01 ICT. Preserve cron declarations.
- **Platform latest reconcile:** #42098901197 (workflow_dispatch, 02:58 ICT) failed only Stock health. GHCR preflight, Auth Secret provisioning, shared pull credentials, Media/MicroFE/TCE/Auth lanes passed; Keycloak skipped; manifest apply and image changes skipped (`allow_image_changes=false`).
- **Inspection fallback:** recovery #42099209509 passed and dispatched inspection #42099284088 (workflow_dispatch, PASS). Snapshot generated 03:00:41 ICT; fresh at 03:27 but not native schedule evidence. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB available RAM, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1; TCE frontend/service, microfe-auth and Keycloak 0/0.
- **Stock publisher:** #41563856933 (Nov 3) passed ARM64 runner, three linux/arm64 builds, full-source-SHA tags and registry digest verification. Release hold was false; handoff validation and paired promotion were skipped. Keep production promotion disabled pending explicit authorization and protected publisher provenance.
- **Media/Auth:** Media CI #41617592783 and Auth CI #41670642852 are historical Nov 3 PASS runs. Do not describe them as fresh builds. Auth #75/#76 remain gated on Supabase production side-effect evidence; no migration.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/credentials/provenance/promotion/reconcile/rollout. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` remains read-only. No production image/manifest/database/replica/host/cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 01:58 ICT / 2026-11-05 18:58 UTC

- **Repository heads:** Platform Infra \`ffbfecaa19730a5cef9861c313a2e1597ac05eaf\`; TCE Dashboard \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`; StockDividend \`50ba0dfb67eb3dfaa376db0c752bbef5b0817bec\`; Media Generation \`e4c7d8990aafc7d837e918c9caf39722d623de7c\`; Authentication \`f978a3f378ee22d4630909c2d182275b21ac9e9a\`.
- **Open PRs:** Platform #544/#541/#539 draft; Authentication #75 ready/#76 draft; none in TCE, StockDividend or Media. Exact heads are in the deployment tracker. Auth #75 validate PASS #40446492086 (Oct 27) and #76 validate PASS #41329425940 (Nov 1) are historical; both Supabase Preview checks were SKIPPED.
- **Platform current run:** TCE heartbeat recovery #42089440296 validated the external source and dispatched reconcile #42089469075 with \`ref=master\`, SHA \`ffbfecaa19730a5cef9861c313a2e1597ac05eaf\`, \`mode=apply\`, \`allow_image_changes=false\`, \`target_app=all\`. Reconcile completed FAILURE only on Stock health; GHCR preflight, pull credential bootstrap and Auth Secret provisioning passed; manifest apply/image changes were skipped. Media, MicroFE, TCE and Auth lanes passed; Keycloak skipped.
- **Stock failure:** two Admin Pods and one new Backend Pod on \`12d63b4\` remained ImagePullBackOff with \`no match for platform in manifest\`. Shared GHCR preflight passed, so this is not evidenced as a pull-secret failure. Keep paired promotion closed pending explicit authorization and protected publisher-run provenance.
- **Platform native schedules:** inspect-vps #42049660972 (21:55:03 ICT, PASS but stale); reconcile-vps #42068683835 (23:51:03 ICT, Stock health failure); recover-stale-ops #42068414686 (23:49:29 ICT, PASS); watchdog #42070623710 (00:02:22 ICT, inspection freshness failure). No later native \`event=schedule\` run appears in the latest 100 Platform Actions runs through #42089788857 (02:00:57 ICT). Preserve cron declarations.
- **Inspection fallback:** post-reconcile recovery #42089788857 PASS. Native inspection remained stale, but workflow_dispatch fallback #42083607462 had a fresh 37m activity age and was correctly not duplicated. Snapshot \`debug/vps-latest.md\` generated 18:22:41Z / 01:22:41 ICT; within 75m at review but not native schedule evidence. It recorded K3s node Ready/ARM64, disk 56%, ~19 GiB RAM, restart_required=yes; Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE frontend/service, microfe-auth and Keycloak 0/0.
- **TCE native recovery E2E:** native WF-06 #42089383865 (01:58:27 ICT, schedule) failed all four public HTTP probes. WF-13 #42089421154 validated workflow ID 339198323, exact source run/SHA/event/attempt and dispatched exactly one read-only WF-06 fallback #42089448641 with \`ref=master\`, SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, no inputs. Fallback also failed all four probes with HTTP 503. WF-13 #42089450102 for the subsequent WF-12 workflow_run source was skipped; no duplicate fallback. This is the first post-merge proof of the native WF-06 → WF-13 → exact-SHA fallback contract, not service recovery.
- **TCE/Auth public health:** strict endpoints \`tce.mrcute.space/\`, \`tce.mrcute.space/api/health\`, \`auth.mrcute.space/api/ready\`, and \`auth.mrcute.space/api/health\` returned 503 instead of 200. The older snapshot's zero-replica observations are correlated, not a proven cause. Platform TCE/Auth lane passes do not override public HTTP failures.
- **Media/Auth:** Media CI #41617592783 and Auth CI #41670642852 are historical Nov 3 PASS runs. Media/Auth scoped reconciliation lanes passed in #42089469075; this is not a fresh app build.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR and source-run/tag/digest provenance; Platform owns manifests, shared pull credentials, provenance/digest checks, promotion, reconciliation, rollout and health. \`reconcile-vps.yml\` remains sole apply authority; \`inspect-vps.yml\` read-only. No production image/manifest/database/replica/host/cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 00:56 ICT / 2026-11-05 17:56 UTC

- **Repository heads:** Platform Infra `37caf7ea6ec1c4833e22eb8b6ffaf03186fd0023`; TCE Dashboard `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft); Authentication #75 (ready)/#76 (draft); none in TCE, StockDividend or Media. Current exact heads and check results are recorded in the tracker; all open-PR PASS checks are historical, and Auth Supabase Preview checks are SKIPPED.
- **Platform #1284:** merged as `37caf7ea6ec1c4833e22eb8b6ffaf03186fd0023`; exact-head validate-manifests #42074105857 and post-merge #42074228245 PASS. Documentation-only; no production apply.
- **Platform native schedules:** inspect-vps #42049660972 (21:55:03 ICT, PASS but stale); reconcile-vps #42068683835 (23:51:03 ICT, Stock health failure); recover-stale-ops #42068414686 (23:49:29 ICT, PASS); watchdog #42070623710 (00:02:22 ICT, FAIL inspection freshness). Workflow_run recovery #42070696343 PASS at 00:02:49 ICT but is not native schedule evidence. No newer native inspect-vps run appeared in the latest 100 Actions runs.
- **K3s:** latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch and is about 93m old at this review, outside the 75m fallback budget. Current live health is unverified. Historical snapshot: node Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM; GitOps drift clean; restart_required=yes; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **TCE:** PR #1024 merged as `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; post-merge WF-01 #42053388961, WF-02 #42053388868 and WF-05 #42053388841 PASS. Latest native WF-06 #42019530614 failed four strict public HTTP probes (503); WF-12 #42013061466 failed freshness; no post-merge WF-13 E2E dispatch.
- **Stock:** CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; Platform handoff validation and atomic paired production dispatch SKIPPED. Production tag `12d63b4` remains incompatible with ARM64. No release authorization/protected provenance; promotion remains disabled.
- **Media/Auth:** Media CI #41617592783 PASS (Nov 3). Auth CI #41670642852 PASS (Nov 3), Supabase Preview SKIPPED; PR #75/#76 remain gated by the production integration side-effect check.
- **MCP:** #1268 merged with committed package-lock; #1280 excludes diagnostics-only MCP from recovery bootstrap. No Docker/Kubernetes mutation authority.
- **Safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/credentials/promotion/reconcile/rollout. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only. No production image/manifest/database/replica/host/cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-06 00:18 ICT / 2026-11-05 17:18 UTC

- **Repository heads:** Platform Infra `be13f089e665de5ad23df6209c3a0831a6a5e295`; TCE Dashboard `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Authentication #75 ready/#76 draft; none in TCE, StockDividend or Media.
- **Platform #1283:** merged as `be13f089e665de5ad23df6209c3a0831a6a5e295`; exact-head validate-manifests #42071477343 and post-merge #42071588610 PASS. Documentation-only; no production apply.
- **Platform native schedules:** inspect-vps #42049660972 PASS at 21:55:03 ICT and remains stale; reconcile-vps #42068683835 at 23:51:03 ICT failed only Stock health; recover-stale-ops #42068414686 PASS at 23:49:29 ICT; watchdog #42070623710 at 00:02:22 ICT failed only native inspection freshness. Recovery workflow_run #42070696343 PASS and skipped duplicate inspection because fallback #42063840567 was 38m old. The fallback snapshot is 55m old at this review and is not native schedule evidence.
- **K3s:** snapshot #42063840567 at 23:23:06 ICT; node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB RAM, GitOps drift clean, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **TCE:** PR #1024 merged as `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; exact-head WF-05/WF-02 and post-merge WF-01/WF-02/WF-05 PASS. Native WF-06 #42019530614 returned HTTP 503 on all four public probes; native WF-12 #42013061466 failed freshness; no post-merge WF-13 E2E dispatch. Preserve all TCE cron declarations and the market-scan schedule.
- **Stock:** CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; Platform paired promotion remains disabled because production tag `12d63b4` lacks ARM64 manifest and explicit authorization/provenance is unavailable.
- **Media/Auth:** Media CI #41617592783 PASS and backend/frontend 1/1 in snapshot. Auth CI #41670642852 PASS; Supabase ACTIVE_HEALTHY / FUNCTIONS_DEPLOYED and migrations match 84/84. Auth #75/#76 remain blocked on Deploy-to-production integration side effects.
- **MCP:** #1268 merged with committed package-lock; #1280 excludes diagnostics-only MCP from recovery bootstrap. No Docker/Kubernetes mutation authority.
- **Safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/credentials/promotion/reconcile/rollout/health. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only. No production image/manifest/database/replica/host/cron mutation. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-05 16:57 ICT / 09:57 UTC

- **Repository heads:** Platform Infra 249047cb1da8a5b136c34dd02d5bd4593cf1fab3; TCE Dashboard 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; StockDividend 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media Generation e4c7d8990aafc7d837e918c9caf39722d623de7c; Authentication f978a3f378ee22d4630909c2d182275b21ac9e9a.
- **Open PRs:** Platform #1222/#544/#541/#539 (all draft); Authentication #75 (ready)/#76 (draft); none in TCE, StockDividend or Media. Exact PR heads are unchanged from the 16:01 checkpoint. Their associated PASS runs are historical, not fresh CI.
- **Platform post-merge:** PR #1263 is closed/merged at 249047cb1da8a5b136c34dd02d5bd4593cf1fab3. Post-merge validate-manifests #41999831798 completed PASS at 16:08:26 ICT; all validation steps passed, with optional changed-image validation skipped because this was documentation-only.
- **Latest native Platform schedules:** inspect-vps #41980605875 (13:28:06 ICT, PASS); reconcile-vps #41995809261 (15:36:40 ICT, failed only Stock health); recover-stale-ops #41994805588 (15:29:01 ICT, PASS); watchdog #41997764646 (15:51:58 ICT, FAIL on inspection freshness). No newer native schedule event was observed in the recent Actions history by 16:57 ICT.
- **Inspection fallback:** #41995133938 was workflow_dispatch at 15:31:32 ICT and generated the snapshot at 15:31:43 ICT. It is now about 86 minutes old and outside the 75-minute budget. Recovery workflow_run #41997798431 passed at 15:52:14 ICT but is not native schedule evidence.
- **Schedule diagnostics:** watchdog #41997764646 verified reconcile-vps active, reported latest scheduled inspect queue wait 0m and no deployment lane over the 15m queue budget, then failed because native inspect #41980605875 was 143m old. Do not attribute the gap to runner queue without new evidence. Preserve all cron declarations.
- **K3s snapshot:** at 15:31:43 ICT node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB available RAM, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0. Snapshot is stale at this checkpoint.
- **Stock reconcile:** #41995809261 passed GHCR/pull credentials and Auth runtime Secret provisioning; Stock health failed on Admin/Backend tag 12d63b4 with no matching platform manifest. ALLOW_IMAGE_CHANGES=false; manifest apply and image changes skipped.
- **TCE:** WF-06 #41962074678 failed all four strict public probes with HTTP 503. WF-12 native #41958165099 failed freshness. WF-07 #41982802263 passed; WF-12 workflow_run #41982820872 failed WF-06 freshness but heartbeat HTTP 204 was accepted by Platform #41982836006. Do not treat heartbeat as service health.
- **Stock publication:** #41563856933 verified immutable ARM64 full-SHA Scraper/Admin/Backend digests; production paired promotion and dispatch remain disabled pending explicit authorization and protected Actions:read provenance.
- **Media/Auth:** Media CI #41617592783 and Auth CI #41670642852 passed on current master SHAs. Media runtime 1/1 only in the stale 15:31 snapshot. Auth #75/#76 remain gated by Supabase production side effects and migration provenance.
- Preserve app-owned tests/builds/immutable GHCR, Platform-owned manifests/credentials/promotion/reconcile/rollout, strict health checks, and useful CI/security/backup/manual/release/scheduled workflows. reconcile-vps.yml remains sole production apply authority; inspect-vps.yml remains read-only. No production image, manifest, database, desired replica, host package, reboot or cron change. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-05 16:01 ICT / 09:01 UTC

- **Repository heads:** Platform Infra 6fa3b63a70d7d57b0b46eb7ffdfff286991095b6; TCE Dashboard 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; StockDividend 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media Generation e4c7d8990aafc7d837e918c9caf39722d623de7c; Authentication f978a3f378ee22d4630909c2d182275b21ac9e9a.
- **Open PRs:** Platform #1222/#544/#541/#539 (all draft); Authentication #75 (ready)/#76 (draft); none in TCE, StockDividend or Media. All six current PR heads were re-read. The latest PR-associated runs returned by the API are historical PASS runs (#1222 #41821355040, #544 #38575430454, #541 #38567431761, #539 #38548718033, Auth #75 #40446492086, Auth #76 #41329425940); do not present them as fresh CI.
- **Platform native schedules:** inspect-vps #41980605875 (13:28:06 ICT, PASS but stale); reconcile-vps #41995809261 (15:36:40 ICT, failure only in Stock health); recover-stale-ops #41994805588 (15:29:01 ICT, PASS); reconcile-schedule-watchdog #41997764646 (15:51:58 ICT, FAIL because native inspection is stale). Native schedule delivery is partial, not wholly absent.
- **Inspection fallback:** #41995133938 was workflow_dispatch at 15:31:32 ICT, passed, and generated debug/vps-latest.md at 15:31:43 ICT. It was fresh at review but is not native schedule evidence. Watchdog #41997764646 measured native inspection age 144m and fallback age 19m, avoided duplicate fallback, and confirmed scheduled recovery age 22m / success. Recovery workflow_run #41997798431 passed after the watchdog but is not a native recovery tick.
- **Platform reconciliation:** #41995809261 passed shared GHCR access preflight, Auth runtime Secret provisioning and shared pull credential bootstrap. Auth/TCE/MicroFE/Media lanes passed; Stock failed. Logs show two Admin Pods and the new Backend Pod ImagePullBackOff on 12d63b4 with no matching platform manifest. Existing Backend and Frontend remain 1/1. ALLOW_IMAGE_CHANGES=false; production manifest apply and image changes skipped.
- **K3s snapshot:** generated 15:31:43 ICT; node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, ~19 GiB RAM available, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend failing image pulls; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **TCE:** WF-06 native #41962074678 (10:30:58 ICT) remains latest and failed all four strict public endpoint jobs; TCE web log explicitly shows HTTP 503 vs expected 200. WF-12 native #41958165099 (09:54:09 ICT) failed freshness. WF-07 native #41982802263 (13:47:35 ICT) passed. WF-12 workflow_run #41982820872 failed WF-06 freshness (age 196m) but its authenticated Platform heartbeat returned HTTP 204; receiver #41982836006 accepted it. Do not equate heartbeat success with service health.
- **Stock publisher:** #41563856933 verified immutable ARM64 full-SHA digests: Scraper 6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2; Admin a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e; Backend cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a. Production promotion and atomic dispatch were explicitly skipped pending release authorization and protected Actions:read provenance.
- **Media/Auth:** Media CI #41617592783 PASS; Media backend/frontend 1/1 in current inspection. Auth CI #41670642852 PASS; #75/#76 remain gated on Supabase production side effects and migration provenance. No new app repository master commits or PRs appeared.
- Preserve app-owned build/test/immutable GHCR, Platform-owned manifests/credentials/promotion/reconcile/rollout, strict health checks, backup/security/manual/release/scheduled jobs. reconcile-vps.yml remains the only production apply authority; inspect-vps.yml remains read-only. No production image, manifest, database, desired replica, host package, reboot or cron change. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-02 17:01 ICT / 10:01 UTC

- **Repository heads/open PRs:** Platform `8a83c8cafc041accca2663e29bbde8aaabd4721f`; TCE `a5e8866d2ba28936d57b31ce6a067186c7204369`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open Platform PRs #795/#749/#648/#544/#541/#539; Auth #75/#76; none in TCE, StockDividend or Media. All eight open PR heads have current PR-triggered workflow checks SUCCESS; draft status and documented Auth side-effect gates remain unchanged.
- **Latest Platform reconciliation:** #41424991858 (workflow_dispatch) failed only in StockDividend health. Shared reconcile job passed runner v14, GHCR/pull credential and Auth Secret preflight; GitOps drift clean and apply skipped with `allow_image_changes=false`. Stock lane log: two Admin Pods and one new Backend Pod ImagePullBackOff on tag `12d63b4`, `no match for platform in manifest`; old Backend and unmanaged legacy Frontend remain 1/1. Health gate correctly fails; no image promotion or restart.
- **Recovery:** #41425271774 succeeded, verified source reconciliation #41424991858, found reconciliation age 0m and inspection #41419270996 age 42m, and correctly avoided duplicate dispatches. It is workflow_dispatch, not native schedule delivery.
- **Latest native Platform schedules:** inspection #41407411326 (07:36:38Z, SUCCESS); reconciliation #41407522742 (07:37:40Z, FAILURE only StockDividend); watchdog #41406983213 (07:32:45Z, FAILURE before fresh ops); mirror #41407613563 (07:38:31Z, missing secret); scheduled recovery #41400302676 (06:30:13Z, SUCCESS). No newer native Platform schedule tick observed through 10:01Z. Reconcile cron remains `7,22,37,52 * * * *`; inspection `2,32 * * * *`; watchdog `12,27,42,57 * * * *`; mirror `17 * * * *`. Do not alter them.
- **TCE WF-06/WF-12:** new WF-06 schedule #41424898130 at 09:57:51Z failed all four public endpoint checks with HTTP 503 vs expected 200. WF-12 workflow_run #41424938817 succeeded both WF-06 freshness verification and authenticated Platform heartbeat. Payload source is TCE WF-06 schedule run #41424898130 with matching heartbeat run #41424938817 and full SHA; Platform receiver #41424970499 succeeded. This is one resumed WF-06 scheduled tick and a workflow_run WF-12 forwarder, not a direct WF-12 scheduled tick. Latest direct scheduled WF-12 remains #41419694332 (09:19:29Z); latest WF-07 integration schedule #41397768048 (06:05:28Z). Keep strict HTTP 200 checks while TCE/Auth are intentionally stopped. WF-06/WF-07/WF-12 cron declarations and market-scan schedule remain unchanged.
- **Latest inspection/runtime:** inspection #41419270996 snapshot at 09:16:30Z; node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB RAM available, runner policy v14, GitOps drift clean, restart_required=yes. Reconcile #41424991858 live Pod listing later confirmed Media/MicroFE/NATS 1/1, Stock Admin (2 Pods) and new Backend ImagePullBackOff, old Backend and legacy Frontend 1/1, TCE/Auth/Keycloak 0/0. No reboot or package upgrade.
- **StockDividend publication:** master CI #41397317588 and immutable publisher #41397317600 remain successful; no newer publication observed. Previously verified full-SHA Scraper/Admin/Backend ARM64 digests remain the release inputs. Production release gate stays false/unset. `STOCKDIVIDEND_ACTIONS_READ_TOKEN` presence remains unverified; do not attempt provenance handoff/promotion until the owner configures it and explicitly authorizes release.
- **Mirror:** latest scheduled #41407613563 failed before Git operations due missing/empty `PLATFORM_INFRA_MIRROR_TOKEN`. Preserve hourly/manual mirror; require destination-only Contents:write on `phanthienquoc/locally-uncensored-private`.
- **Media/Auth:** Media CI #41246414186 passed; runtime remains digest-pinned and 1/1. Auth master CI #41033586844 and PR #75/#76 current-head CI passed; retain production Supabase side-effect and migration-drift gates. No database mutation or new Supabase health assertion.
- Preserve CI, tests/builds, security, backup, manual/read-only, release, maintenance, cleanup, mirror and scheduled data workflows. `reconcile-vps.yml` remains sole GitOps apply authority; `inspect-vps.yml` read-only; recovery/watchdog dispatch/observe only; bootstrap remains sole runner-helper installation authority. No direct SSH/Compose deployment authority, production manifest/image mutation, credential mutation, database write, release enablement, desired replica change, schedule change, image deletion or VPS reboot occurred.

## Workflow inventory schedule follow-up — 2026-11-02 16:22 ICT / 09:22 UTC

- TCE WF-12 scheduled run #41419694332 was delivered at 09:19:29Z on master (SHA a5e8866d2ba28936d57b31ce6a067186c7204369). The workflow-enabled check passed.
- WF-12's WF-06 freshness check failed: latest scheduled WF-06 remains #41378060687 (02:30:05Z, age 409m, queue=0m). Keep the public endpoint assertion and schedule freshness check intact.
- WF-12's authenticated Platform heartbeat job succeeded with source and heartbeat run ID 41419694332, source path .github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml, event=schedule, master and full SHA.
- Platform receiver #41419728825 independently verified the source and completed SUCCESS. It did not dispatch duplicate work because latest reconciliation #41418939586 (3m) and inspection #41419270996 (1m) were fresh.
- Count this as one observed native WF-12 schedule tick, not sustained cadence recovery. Platform native reconciliation/inspection schedules and TCE WF-06 remain stale in the latest inspected history.
- No workflow, cron expression, production manifest, desired replica or TCE market-scan schedule changed.

## Workflow inventory update — 2026-11-02 16:20 ICT / 09:20 UTC

- Current master heads: Platform Infra 5a07dc0ede47d47415c8599786d710c49b984489; TCE a5e8866d2ba28936d57b31ce6a067186c7204369; StockDividend 38220ddfef2db7128482547f72b7f06211e9c9bc; Media d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PRs: Platform #795/#749/#648/#544/#541/#539; Authentication #75/#76; none in TCE, StockDividend or Media. Platform #538 is closed as superseded; #1048/#1049/#1050 are merged.
- Auth GitOps validator #1048 is merged and required exact-head/post-merge checks passed. It validates the effective Kustomize render and has one positive/eight negative offline cases. No live cluster or production resources are changed by this validator.
- Tracker/inventory PR #1049 merged; exact-head #41419358101 and post-merge #41419422676 passed.
- Fresh inspection PR #1050 merged as 5a07dc0ede47d47415c8599786d710c49b984489 after exact-head validation #41419373922 passed. Inspection workflow #41419270996 succeeded; snapshot generated 2026-11-02T09:16:30Z, file commit 7056f937b31c900d9bf301b20ed98ac4d345b72d.
- Fresh snapshot: node Ready ARM64, K3s v1.36.3+k3s1, disk 55%, available RAM 19 GiB, runner policy v14. Media backend/frontend, MicroFE Shell/WS and NATS healthy. Stock Admin 0/1; new Stock Backend pod ImagePullBackOff while old replica remains 1/1; legacy frontend 1/1 unmanaged. TCE/Auth/Keycloak intentionally 0/0. restart_required=yes; no reboot.
- Post-merge reconciliation #41418939586: shared preflight passed, no drift, apply skipped; TCE, Media, MicroFE and Auth lanes passed; StockDividend lane failed; Keycloak skipped. Runner v14 skipped restart for permanent no-match-for-platform errors on Stock Admin/Backend. Recovery #41419229756 verified source run and dispatched inspection #41419270996.
- Latest native Platform scheduled events remain inspection #41407411326, reconcile #41407522742, watchdog #41406983213, mirror #41407613563 and recovery #41400302676. Watchdog measured inspection queue delay 0m while event age was 393m. Recovery dispatches are not native cron delivery.
- TCE latest scheduled events remain WF-07 #41397768048 success, WF-06 #41378060687 failure (four public endpoints 503 while TCE/Auth are intentionally stopped), and WF-12 #41374853407 failure due stale WF-06 delivery. TCE heartbeat receiver #41397794672 validated the forwarded WF-07 source.
- StockDividend CI #41397317588 and publisher #41397317600 passed with immutable ARM64 digests. Release gate remains false/unset; no promotion. STOCKDIVIDEND_ACTIONS_READ_TOKEN requires owner configuration (StockDividend Actions:read only).
- Mirror #41407613563 failed because PLATFORM_INFRA_MIRROR_TOKEN is absent; owner action remains destination-only Contents:write on phanthienquoc/locally-uncensored-private.
- Media CI #41246414186 passed. Auth CI #41329425940 passed, but PR #75/#76 remain gated on Supabase production integration and migration-drift/provenance review.
- Preserve useful CI/test/security, manual read-only, release, backup and scheduled workflows. No duplicate SSH/Compose deployment authority introduced. No production manifests, GHCR pull credentials, database objects, release flags, desired replicas or cron expressions changed. TCE market-scan schedule unchanged.

## Workflow inventory update — 2026-11-02 16:17 ICT / 09:17 UTC

- Current master heads: Platform Infra 5402ae607b3917f6586ccfeda72427fb0c127a29; TCE a5e8866d2ba28936d57b31ce6a067186c7204369; StockDividend 38220ddfef2db7128482547f72b7f06211e9c9bc; Media d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PRs: Platform #795/#749/#648/#544/#541/#539; Authentication #75/#76; none in TCE, StockDividend or Media. Platform #538 is closed as superseded by #1048; #1048 is merged.
- Platform #1048 adds scripts/validate-auth-gitops-contract.py and wires it into validate-manifests after Kustomize render. The offline contract validates Auth Ingress -> Service -> Deployment, port 80 -> 4010, immutable image tag, Secret refs, JWT issuer/audience and probes. One positive/eight negative self-test cases passed.
- Exact-head #1048 checks passed: #41418804556, #41418804603, #41418804667. Post-merge #41418913629, #41418913666 and #41418913493 passed. No production resource or release state changed.
- Post-merge push recovery #41418913434 passed and dispatched reconciliation #41418939586 with allow_image_changes=false. Shared reconciliation passed with no drift; apply was skipped. TCE, Media, MicroFE and Auth lanes passed; StockDividend health failed; Keycloak was skipped. The final lane summary was still queued at 09:17Z.
- Runner v14 was verified live in #41418939586. Permanent ARM64 image-pull errors for Stock Admin/Backend were detected and rollout restarts skipped. Current failing tag remains 12d63b4.
- Latest K3s inspection snapshot remains #41407411326 (07:36:46Z); stale against the 75-minute budget. Fresh post-reconciliation inspection required. Node Ready ARM64, K3s v1.36.3+k3s1, disk 55%, available RAM 19 GiB, runner policy v14, restart_required=yes.
- Latest native Platform scheduled events remain inspection #41407411326, reconcile #41407522742, watchdog #41406983213, mirror #41407613563, recovery #41400302676. Watchdog measured inspection queue wait 0m while event age was 393m; no later native scheduled event appeared in the inspected history. Recovery push is not native cron delivery.
- TCE WF-07 scheduled #41397768048 succeeded and WF-12 forwarded a valid Platform heartbeat via #41397785851/#41397794672. WF-06 #41378060687 remains a public-health failure (four endpoints 503 while TCE/Auth are intentionally stopped); WF-12 schedule #41374853407 failed its WF-06 freshness check. No cron expression changed.
- StockDividend publisher #41397317600 and CI #41397317588 passed with immutable linux/arm64 digests: Scraper e637c3f643d863783e98e9184bbdcf60f24665ca94892e698fa8c814c1d572f5; Admin 18a850987ed20bad0c255e56fe14583260cf4b5302a7fdd6128b2c3440e5785d; Backend 5288e7f287a3511c8a67e662f4121d3661e84f52168cb2c22acadd3d3d0e2849. Release gate remains false/unset.
- Owner-only credentials: STOCKDIVIDEND_ACTIONS_READ_TOKEN (StockDividend Actions:read only) and PLATFORM_INFRA_MIRROR_TOKEN (destination Contents:write only). Mirror run #41407613563 confirms the latter is missing.
- Media CI #41246414186 passed. Auth CI #41329425940 passed, but PR #75/#76 remain gated on Supabase production integration and migration-drift/provenance review.
- Preserve CI, security, manual read-only, release and backup workflows. No duplicate SSH/Compose deployment authority introduced. No production manifests, GHCR pull credentials, database objects, release flags, desired replicas or schedules changed. TCE market-scan schedule unchanged.

## Workflow inventory update — 2026-11-02 13:06 ICT / 06:06 UTC

- **Current master heads:** Platform Infra `4a1c1de761bcd1a14b1cae904f5b79414babb1c6`; TCE `a5e8866d2ba28936d57b31ce6a067186c7204369`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- **Open PR inventory:** Platform #795/#749/#648/#544/#541/#539/#538; Authentication #75/#76; none in TCE, StockDividend or Media. StockDividend PR #24 and Platform PR #1040/#1041 are merged.
- **StockDividend release producer:** `.github/workflows/deploy.yml` now sends the exact publisher run ID, workflow path, source event and full source SHA together with the paired Admin/Backend immutable digests. `scripts/validate-production-release-contract.sh` exercises the payload shape without dispatching. The release hold still gates promotion separately from artifact publication.
- **Platform release consumer:** `gitops-image-promotion.yml` validates StockDividend payload fields and calls `scripts/verify-stockdividend-publisher-run.sh` before GHCR reads or GitOps PR creation. The verifier waits for the private StockDividend publisher run to complete and checks repository/head repository, workflow path, event, master branch, full SHA and successful conclusion. Mocked tests cover delayed completion and fail-closed metadata mismatches.
- **Private source credential:** Platform Infra's protected `production` Environment now requires `STOCKDIVIDEND_ACTIONS_READ_TOKEN` for private StockDividend Actions API reads. Configure it with StockDividend-only `Actions: read`; no Contents write, Packages or workflow-dispatch permission. Secret presence is not visible to this audit and must be confirmed by the owner before release enablement. This is separate from `PLATFORM_INFRA_TOKEN` (dispatch) and `GHCR_READ_TOKEN` (package pull/read).
- **Validation:** StockDividend PR #24 exact-head CI #41397120517 passed; post-merge CI #41397317588 passed. Platform PR #1041 final exact-head checks #41397749860/#41397749842 passed; post-merge checks #41397817096/#41397817001 passed. An earlier head had a ShellCheck SC1007 test-assignment warning, corrected before merge.
- **Runtime release status:** Post-merge publisher #41397317600 completed successfully for source SHA `38220ddfef2db7128482547f72b7f06211e9c9bc`; full-SHA tags were verified `linux/arm64` with Scraper `sha256:e637c3f643d863783e98e9184bbdcf60f24665ca94892e698fa8c814c1d572f5`, Admin `sha256:18a850987ed20bad0c255e56fe14583260cf4b5302a7fdd6128b2c3440e5785d`, and Backend `sha256:5288e7f287a3511c8a67e662f4121d3661e84f52168cb2c22acadd3d3d0e2849`. Source-run metadata matched `.github/workflows/deploy.yml`, `push`, `master`, and the exact SHA. The release gate remained false, so no dispatch/promotion occurred; the Platform private-source verifier was not exercised.
- **Recovery correlation:** PR #1038 source-run ID correlation is now runtime-verified: recovery #41397606829 display title includes source reconciliation #41397421456, and its log verifies that exact source run completed. The reconciliation used runner v14, `allow_image_changes=false`, found no drift, skipped manifest apply, suppressed permanent ARM64 image-pull restarts, and failed only the StockDividend health lane.
- **TCE heartbeat:** WF-07 schedule #41397768048 → WF-12 forwarder #41397785851 → Platform receiver #41397794672 validated successfully. WF-12 notification passed; its separate WF-06 freshness check failed because WF-06's latest schedule was stale. Receiver did not dispatch duplicate recovery because reconciliation and inspection remained fresh.
- **Platform schedule freshness:** Latest native reconcile/watchdog/inspection/mirror runs remain #41369624425/#41369864119/#41370072870/#41368359234; no later native Platform cron delivery by 06:06Z. Recovery events do not count as cron. TCE WF-07 scheduled delivery is active (#41397768048); latest WF-06 and direct WF-12 scheduled runs remain #41378060687 and #41374853407. Keep all TCE cron declarations and market-scan cadence unchanged.
- **Mirror blocker:** `PLATFORM_INFRA_MIRROR_TOKEN` remains missing/empty; owner must configure destination-only `Contents: write` for `phanthienquoc/locally-uncensored-private`.
- **Production ownership remains:** app repositories own CI/builds/immutable GHCR publication; Platform Infra owns production manifests/shared pull credentials/GitOps promotion/reconciliation/rollout/health. `reconcile-vps.yml` is the sole apply authority; `inspect-vps.yml` is read-only; `bootstrap-runner.yml` is the only runner-helper installer; `vps-manual-operations.yml` is manual/read-only. TCE WF-06 remains public-only. Preserve useful CI/test/security, backup, release, manual and scheduled workflows; no duplicate SSH/Compose deployment authority.
- **Safety:** no production manifest, image reference, GHCR pull credential, database object, release-enable variable, desired replica or schedule expression changed. No StockDividend promotion, workload restart, image deletion, or VPS reboot.

## Workflow inventory update — 2026-11-02 12:10 ICT / 05:10 UTC

- **Current master heads:** Platform Infra `db672e0f33ea99a4b140df26eead190f232f48d6`; TCE `a5e8866d2ba28936d57b31ce6a067186c7204369`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- **Open PR inventory:** Platform #795/#749/#648/#544/#541/#539/#538; Authentication #75/#76; none in TCE, StockDividend or Media. Platform #1035/#1036/#1037/#1038 are merged.
- **Runner/inspection:** PR #1035 added a read-only `platform-kubectl policy-version` field to `scripts/inspect-vps.sh` and made the inspection workflow require it. Snapshot #41391624912 / PR #1036 records live runner v14 and fresh K3s state. `bootstrap-runner.yml` remains the sole helper installer.
- **StockDividend workload ownership:** only Admin/Backend are Platform-managed. Legacy `stock-frontend` remains present but excluded from Platform health/rollout/restart/rollback gates; it is not deleted or scaled. Runner v14 skips restarts for permanent ARM64 manifest errors. Admin/Backend remain not ready on tag `12d63b4`.
- **GHCR promotion validation:** PR #1037 extended the exact-reference Registry V2 validator to require `linux/arm64` on indexes or single-image config blobs. It is called by the existing promotion workflow before creating a GitOps PR. App repositories still own tests/builds and immutable publication; Platform independently verifies production architecture. Regression tests cover both ARM64 and AMD64 cases. No live promotion was run.
- **Recovery correlation:** PR #1038 adds source-run ID to workflow-dispatch recovery display titles and correlates the notifier by that ID rather than by the recovery run's head SHA. The recovery controller still verifies the source run ID/full SHA. Exact-head and post-merge CI all passed. Runtime source-ID correlation awaits the next actual reconciliation.
- **Reconciliation authority:** `reconcile-vps.yml` remains the sole GitOps apply authority. Latest reconciliation #41391637004 passed v14/shared preflight, found no manifest drift, skipped apply with image changes disabled, and failed only StockDividend Admin/Backend health. Its recovery notifier had a false-negative correlation because master advanced between source and recovery; PR #1038 fixes the race.
- **Inspection authority:** `inspect-vps.yml` remains read-only and records node/OS, runner policy, K3s workloads, imageIDs, failures, GitOps drift and maintenance state. Latest snapshot generated 2026-11-02T05:01:40Z; node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available, restart_required=yes. No reboot or upgrade.
- **TCE:** WF-06 remains public-endpoint-only with no VPS SSH/Docker/Compose inspection. Latest scheduled WF-06 #41378060687 returned HTTP 503 because TCE/Auth are intentionally stopped; WF-12 forwarder #41378080124 and Platform receiver #41378091682 succeeded. No later schedule event was observed. Keep all TCE schedules and the market-scan cadence unchanged.
- **Platform schedules:** latest native scheduled reconcile #41369624425, watchdog #41369864119, inspection #41370072870. No later native schedule event by 05:10Z. Fallback recovery/inspection events do not count as native cron delivery.
- **Mirror:** latest scheduled mirror #41368359234 still fails for missing/empty `PLATFORM_INFRA_MIRROR_TOKEN`. Required scope is destination-only `Contents: write` on `phanthienquoc/locally-uncensored-private`; no credential substitution.
- **StockDividend publication:** CI #41314359022 and publisher #41314359012 passed. Full-source-SHA images were verified linux/arm64 with immutable digests recorded in the deployment tracker. The promotion-enable variable was unset/false, so handoff/dispatch were skipped. No promotion.
- **Media:** master CI #41246414186 passed; runtime backend/frontend 1/1 and digest-pinned. No new publication.
- **Authentication:** PR #75/#76 remain open pending production Supabase integration side-effect and migration-drift review. Auth/Keycloak remain 0/0. No migration or database mutation.
- Preserve all useful CI/build/test/security, backup, release, manual and scheduled workflows. App repos own tests/builds/immutable GHCR publication; Platform owns production manifests/shared pull credentials/GitOps promotion/reconciliation/rollout/health. `reconcile-vps.yml` is the only apply authority; `inspect-vps.yml` is read-only; `bootstrap-runner.yml` is the only runner-helper installer; `vps-manual-operations.yml` is manual/read-only. No duplicate SSH/Compose deployment authority and no schedule change.

## Workflow inventory update — 2026-11-02 11:03 ICT / 04:03 UTC

- **Platform Infra master:** `f43983096cd2b698f01d8d990258e6e7b592a061`. PR #741/#1032/#1033 merged. Platform open PRs: #795/#749/#648/#544/#541/#539/#538; Auth open PRs #75/#76; no open PRs in TCE, StockDividend or Media.
- **Manual read-only operations:** PR #741 merged `.github/workflows/vps-manual-operations.yml`. It is workflow_dispatch-only, master-only, uses the production environment with `contents: read`, a five-minute timeout, host/service read commands and only the existing `platform-kubectl get` allowlist for cluster summaries. It introduces no SSH, Docker/Compose or mutation/deployment authority; preserve it as a narrow manual diagnostic alongside scheduled/read-only `inspect-vps.yml`.
- **Runner policy v14:** bootstrap #41381590010 installed `rollout-status-v14-stockdividend-managed-workloads`. Post-v14 reconciliation #41385997750 verified the exact policy live, logged permanent ARM64 image-pull failures for Stock Admin/Backend and skipped restarts; restart counts remained zero. PR #1032 corrected v13 stale diagnostics and added a regression guard; exact-head and post-merge lint/manifest/Keycloak checks all passed.
- **Reconciliation #41385997750:** `workflow_dispatch`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. Shared GHCR preflight/credential reconciliation succeeded, no manifest drift was found, and apply was correctly skipped. Media/TCE/MicroFE/Auth lanes passed, Keycloak was skipped, StockDividend failed only at Admin/Backend health. This is v14 runtime verification, not a healthy production rollout.
- **Inspection #41386215251:** recovery #41386187542 dispatched the read-only inspector after the reconciliation. Snapshot PR #1033 exact head `6b3eed4f2db6519246c98ad2b2537c17b5706c4e` passed manifest validation #41386278979 and merged as `f43983096cd2b698f01d8d990258e6e7b592a061`. Latest snapshot: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, about 19 GiB available, GitOps drift clean, restart_required=yes; Media/MicroFE/NATS 1/1; Stock Admin and new Backend pods ImagePullBackOff on `12d63b4`; old Backend and legacy Frontend 1/1; TCE/Auth/Keycloak 0/0. No reboot or package upgrade.
- **StockDividend ownership:** only Admin/Backend are Platform-managed; legacy `stock-frontend` remains present but excluded from Platform health/rollout/restart/rollback gates and was not deleted or scaled. Publisher #41314359012 verified linux/arm64 immutable digests for Scraper/Admin/Backend; atomic promotion was skipped because `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=false`. No production image promotion.
- **Media:** master `d8e695d7`, latest CI #41246414186 passed; current production references are paired immutable digests. Runtime lane passed in #41385997750. No new release.
- **TCE:** master `a5e8866d`; WF-06 remains public-endpoint-only (no VPS SSH/Docker/Compose), cron `*/15 * * * *`; WF-12 schedule cron remains `7,22,37,52 * * * *`. Latest schedule-filtered WF-06 #41378060687 returned HTTP 503 for the four endpoints because TCE/Auth are intentionally stopped; its WF-12 forwarder #41378080124 and Platform receiver #41378091682 passed. No scheduled TCE event after the WF-06 cleanup merge; keep all cron declarations and market-scan cadence unchanged.
- **Platform schedules:** latest native scheduled reconciliation #41369624425 (00:54Z), watchdog #41369864119 (00:56Z), inspection #41370072870 (00:59Z). No newer native schedule event by 04:03Z. Workflow-dispatch recovery/inspection runs do not count as cron delivery. Native cadence remains stale.
- **Mirror:** scheduled run #41368359234 failed because `PLATFORM_INFRA_MIRROR_TOKEN` is missing. Required scope remains destination-only `Contents: write` for `phanthienquoc/locally-uncensored-private`; no substitute credential.
- **Authentication:** master `ceb2688d`; PR #75/#76 remain open due the production Supabase integration side-effect gate and migration-drift review. No migration or database mutation. Auth runtime is intentionally 0/0; Keycloak is 0/0.
- Preserve useful CI/build/test/security, backup, release, manual and scheduled workflows. App repos own tests/builds/immutable GHCR publication; Platform owns production manifests/shared pull credentials/GitOps promotion/reconciliation/rollout/health. `reconcile-vps.yml` is the sole GitOps apply authority, `inspect-vps.yml` read-only, `bootstrap-runner.yml` sole runner-helper installer, and `vps-manual-operations.yml` read-only/manual only. No duplicate direct SSH/Compose authority or schedule change.

---

## Workflow inventory update — 2026-11-02 10:13 ICT / 03:13 UTC

- **Platform Infra master:** `acad7c770ea97545abb00bda4ed246f94c073e95`. PR #1028/#1029/#1030 merged with exact-head checks passing. PR #1029 narrowed StockDividend production ownership to Admin/Backend and bumped the approved runner helper contract to v14. PR #1030 fixed push-scope classification for runner bootstrap/recovery-readiness companion paths.
- **Bootstrap authority:** `.github/workflows/bootstrap-runner.yml` remains the only runner-helper installer. Push run #41381590010 succeeded and verified live `rollout-status-v14-stockdividend-managed-workloads` on the VPS. Do not add a second SSH installer.
- **Reconcile authority:** `.github/workflows/reconcile-vps.yml` remains the sole GitOps apply authority and now requires v14 before apply. Push reconciliation #41381590097 failed before preflight/apply on an unclassified companion path; PR #1030 updated the resolver and self-tests. No cluster mutation occurred in that failed run. A post-v14 reconciliation has not yet exercised the new health scope.
- **Inspection authority:** `.github/workflows/inspect-vps.yml` remains read-only. Latest snapshot run #41378301376 was generated before v14 installation; refresh after a later verified reconciliation or scheduled inspection.
- **StockDividend managed workloads:** current app source + production Kustomize + Ingress own only `stock-admin` and `stock-backend`; scraper remains an app-owned scheduled job. Legacy `stock-frontend` has no source/Dockerfile/Kustomize/Service/Ingress ownership and is explicitly excluded from Platform health, rollout, restart and rollback-readiness gates. It is not deleted or scaled. Admin/Backend remain blocked by ARM64-incompatible tag `12d63b4`; production release remains disabled.
- **TCE workflows:** WF-06 is public endpoint smoke only (no VPS SSH/Docker/Compose inspection). Latest scheduled WF-06 #41378060687 returned HTTP 503 for four endpoints because TCE/Auth are intentionally stopped. WF-12 #41378080124 forwarded the source heartbeat; Platform receiver #41378091682 verified it against GitHub Actions API. WF-07 backup #41356061914 and integration #41355068024 remain latest identified scheduled runs. Preserve all TCE cron declarations and market-scan cadence.
- **Platform native schedules:** latest scheduled reconcile #41369624425, watchdog #41369864119, and inspection #41370072870 are still the newest schedule-filtered runs. Later workflow_dispatch/repository_dispatch recovery does not count as native cron delivery. Mirror schedule #41368359234 failed because `PLATFORM_INFRA_MIRROR_TOKEN` is absent.
- **Media Generation:** master `d8e695d7`; latest available CI #41246414186 passed; K3s snapshot shows backend/frontend 1/1. No new release.
- **Authentication:** master `ceb2688d`; open PR #75/#76 remain subject to production Supabase integration side-effect review. No migration or activation.
- **Ownership boundaries:** app repositories own tests/builds/immutable GHCR publication. Platform Infra owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health verification. Preserve CI/test/security, backup, manual/release and scheduled workflows. Do not create duplicate direct SSH/Compose deployment authorities.

---

## Workflow inventory update — 2026-11-02 10:01 ICT / 03:01 UTC

- **Platform Infra:** current master `b5de43fe32ca688dce0f9f062f8743322746301b`; automated read-only inspection PR #1027 merged after exact-head validation #41378367760. Fresh inspection run #41378301376 succeeded and updated `debug/vps-latest.md`. Native scheduled reconciliation/inspection/watchdog have not delivered a new scheduled interval after #41369624425/#41370072870; later repository_dispatch/workflow_dispatch recoveries are fallback, not native cron evidence.
- **Reconcile authority:** `.github/workflows/reconcile-vps.yml` remains the only production GitOps apply authority. Latest TCE heartbeat-triggered receiver #41378091682 validated WF-06 source run #41378060687 and WF-12 forwarder #41378080124 against the TCE Actions API, then dispatched reconciliation #41378106989 with `allow_image_changes=false`. Shared preflight succeeded/no drift; application health failed only for StockDividend.
- **Runner helper:** `bootstrap-runner.yml` remains the sole installer. Live policy v13 was verified during reconciliation #41378106989; permanent ARM64 manifest pull errors for Stock Admin/Backend explicitly skipped rollout restart. Do not add another SSH/helper installation path.
- **Inspection authority:** `.github/workflows/inspect-vps.yml` remains read-only and owns K3s/VPS runtime evidence. PR #1027 is an automated inspection snapshot only; no production manifests changed.
- **TCE app workflows:** WF-06 is now public endpoint smoke only, with no VPS SSH or Docker/Compose inspection. Its latest scheduled run #41378060687 returned HTTP 503 for all four public endpoints because TCE/Auth are intentionally stopped; keep expected HTTP 200 checks strict so the stopped public service remains visible as unhealthy. WF-12 #41378080124 successfully forwarded the scheduled WF-06 heartbeat to Platform; Platform receiver #41378091682 validated it. WF-07 backup #41356061914 and integration #41355068024 remain the latest identified scheduled runs. Preserve all TCE cron declarations and market-scan schedule.
- **StockDividend:** app-owned CI and immutable GHCR publication remain the app repository's responsibility; latest available CI/publisher #41314359022/#41314359012 passed on master `f5c04475`. Production Admin/Backend still reference ARM64-incompatible `12d63b4`; platform health gate must remain failing, and `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=false`. No promotion without explicit authorization.
- **Media Generation:** latest available CI #41246414186 passed on master `d8e695d7`; current K3s inspection shows backend/frontend 1/1 with pinned runtime image IDs. No new Media release.
- **Authentication:** master `ceb2688d`; open PR #75/#76 remain subject to production Supabase integration side-effect review. PR #76 CI #41329425940 passed; no migration or activation. Do not infer current Supabase health from older probes.
- **Mirror workflow:** scheduled run #41368359234 failed because secret `PLATFORM_INFRA_MIRROR_TOKEN` is absent. Required scope: destination-only `Contents: write` for `phanthienquoc/locally-uncensored-private`. Do not substitute GHCR or dispatch credentials.
- Preserve useful CI/build/test/security, backup, manual/release, maintenance and scheduled workflows. Do not create a second direct SSH/Compose deployment authority. Keep app-owned builds/tests/immutable GHCR publication separate from Platform-owned manifests/shared pull credentials/GitOps/rollout/health verification.

---

## Follow-up verification — 2026-11-02 07:00 ICT / 2026-11-02 00:00 UTC

- Platform PR #1020 merged as `b28d1f4e454cec8e521619b4fec33a9b3433a55c`; exact-head validation #41364647902 and post-merge validation #41364681389 passed.
- Cross-repo TCE heartbeat has now been correlated across three successful chains:
  - WF-07 scheduled source #41355068024 → WF-12 workflow_run #41355080288 → Platform repository_dispatch #41355088547 → reconciliation #41355101409.
  - Direct WF-12 schedule #41358488421 → Platform repository_dispatch #41358495488 → reconciliation #41358507981.
  - WF-06 scheduled source #41360343131 → WF-12 workflow_run #41360361422 → Platform repository_dispatch #41360370906 → reconciliation #41360385108.
- Each Platform receiver validation job succeeded after Actions API verification of source/heartbeat run identity, workflow path, event, branch, and full SHA. Each existing reconciliation completed shared operations and inspection recovery; StockDividend was the only failing application lane. These events validate heartbeat and fallback recovery, not a healthy production rollout.
- The heartbeat contract is verified across three source patterns, but continuous native Platform cron delivery is still unproven. Latest native Platform schedule events remain reconciliation #41351121366 and inspection #41351555469. TCE WF-12 scheduled run #41358488421 had a failing WF-06 freshness check while its heartbeat dispatch job succeeded.
- Runner policy v13 was installed by the existing bootstrap run #41360807367. A post-v13 reconciliation exercising permanent image-pull restart suppression is still pending.
- Current Platform Infra master: `b28d1f4e454cec8e521619b4fec33a9b3433a55c`. Other repository heads unchanged: TCE `d011fbb4099f5f9e24068878ac4e035b369e8ace`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs remain Platform #795/#749/#741/#648/#544/#541/#539/#538 and Authentication #75/#76; none in TCE, StockDividend, or Media.
- Preserve the single authority split: app repos own builds/tests/immutable GHCR publication; Platform owns production manifests, shared pull credentials, GitOps/reconciliation/health; TCE heartbeat has no deployment authority. No SSH/Compose authority or TCE cron change.

---

## Runtime verification update — 2026-11-02 06:55 ICT / 2026-11-01 23:55 UTC

- **Runner policy v13 installed:** post-merge existing bootstrap workflow [#41360807367](https://github.com/phanthienquoc/platform-infra/actions/runs/41360807367) completed SUCCESS on master SHA `15c46d1093321a5a5b7570686d9222edfdf564f3`. Its log printed `platform-kubectl policy: rollout-status-v13-permanent-image-pull-restart`; the final runner-service and allowlisted-reconciliation-capability verification step passed. Do not keep the prior "installation pending" status. A post-v13 reconciliation exercising the new permanent-image-pull branch is still pending.
- **TCE cross-repository heartbeat verified end-to-end once:** scheduled WF-06 #41360343131 → WF-12 workflow_run #41360361422 → successful authenticated Platform repository_dispatch #41360370906. TCE's notify job logged the accepted source path, run ID, full SHA, and heartbeat run ID. Platform's receiver fetched both TCE Actions runs and passed exact workflow-path/event/branch/SHA/run-ID validation.
- The Platform receiver dispatched existing reconciliation run [#41360385108](https://github.com/phanthienquoc/platform-infra/actions/runs/41360385108) with `ref=master`, SHA `7b496b4f99737810ad90d2b616d81b58c7f04029`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. Shared preflight and Media/MicroFE/TCE/Auth lanes passed; StockDividend health failed; manifest apply/image-change guard were skipped. This is a successful heartbeat/recovery contract with an expected application-health blocker, not a successful production rollout.
- The heartbeat-triggered reconciliation predates the v13 bootstrap. Verify the next reconciliation and fresh read-only inspection before claiming v13's permanent-pull skip was exercised on production.
- Latest Platform master validation #41360959837 passed on SHA `726c9be6367899ac158ea70841a11c7b7342ff26`. Current master heads: Platform `726c9be6367899ac158ea70841a11c7b7342ff26`; TCE `d011fbb4099f5f9e24068878ac4e035b369e8ace`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs remain Platform #795/#749/#741/#648/#544/#541/#539/#538 and Authentication #75/#76; none in TCE, StockDividend, or Media. Auth #75/#76 validation checks passed; Supabase Preview skipped.
- Native Platform scheduled reconcile/inspection remain stale at #41351121366/#41351555469. TCE WF-06 #41360343131 failed only public endpoint checks (TCE/Auth intentionally stopped) while local healthcheck and heartbeat forwarding succeeded. WF-07 backup #41356061914 and integration #41355068024 succeeded. WF-12 scheduled #41358488421 failed the stale WF-06 freshness check; the later workflow_run #41360361422 successfully forwarded the heartbeat.
- The latest K3s snapshot is still 2026-11-01 22:45:14Z and predates v13 bootstrap. Node Ready/ARM64, disk 55%, about 19 GiB available, GitOps drift clean, restart_required=yes; Media/MicroFE/NATS healthy; Stock Admin and new Backend pods remain ImagePullBackOff on old tag `12d63b4`; old Backend and Frontend replicas remain 1/1.
- Mirror secret `PLATFORM_INFRA_MIRROR_TOKEN` remains missing; destination-only `Contents: write` is required for `phanthienquoc/locally-uncensored-private`.
- Preserve app-owned CI/build/immutable GHCR publication and platform-owned manifests/shared pull credentials/GitOps/reconciliation/health authority. Keep `bootstrap-runner.yml` as the sole runner-helper installer, `reconcile-vps.yml` as the sole GitOps apply authority, and `inspect-vps.yml` read-only. Do not add SSH/Compose deployment paths or change any TCE cron/market-scan schedule.

---

## Workflow inventory review — 2026-11-02 06:02 ICT / 2026-11-01 23:02 UTC

- **Platform Infra PR #1019 merged:** runner policy v13 now skips rollout restarts for permanent image architecture/manifest failures. Exact-head checks: validate-github-actions #41360751760, validate-manifests #41360751736, keycloak-ci #41360751691 — all PASS. Merge commit: `15c46d1093321a5a5b7570686d9222edfdf564f3`.
- **Runner bootstrap is pending runtime verification:** the existing `bootstrap-runner.yml` remains the only installer and is triggered by the helper path. Confirm a post-merge bootstrap run and live `platform-kubectl policy-version` output before declaring v13 installed or allowing reconciliation apply. Reconcile requires exact v13; Auth secret provisioning accepts v13 plus prior compatibility versions. Do not install the helper through a second SSH/Compose authority.
- **Regression contract:** the helper skips restart if any selected container/init-container has a permanent pull message (`no match for platform in manifest`, `manifest unknown`, `manifest not found`). Transient auth/network/rate-limit failures remain retryable after the shared pull-secret reconciliation. Mixed permanent/transient errors are fail-closed. Mocked-kubectl tests cover permanent, transient, mixed, and unrelated waiting states; shellcheck, ops regression tests, workflow contract validation, manifest validation, and Keycloak CI passed on exact PR head.
- **Latest VPS evidence:** snapshot generated 2026-11-01 22:45:14Z by inspection snapshot PR #1018. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, about 19 GiB available, GitOps drift clean, restart_required=yes. Media, MicroFE Shell/WS and NATS 1/1. Stock Admin has two ImagePullBackOff Pods and new Backend one ImagePullBackOff Pod on tag `12d63b4`; old Backend and Frontend replicas remain 1/1. Pull message is permanent ARM64 manifest mismatch. TCE/Auth/Keycloak remain stopped. No reboot/package update.
- **Platform schedule:** last identified native scheduled reconciliation #41351121366 failed only at StockDividend health; inspection #41351555469 and its recovery/watchdog #41351669202/#41351669205 succeeded. The newer inspection snapshot commit #1018 is not independently tied to a schedule event in this review. Multiple consecutive native intervals remain unproven.
- **TCE:** sender/receiver code is merged, but no post-merge scheduled WF-06/WF-07/WF-12 event has been correlated through Platform repository_dispatch and recovery. Last confirmed scheduled run IDs remain WF-06 #41342785812, WF-07 #41311225433, WF-12 #41339371004. Preserve all cron declarations and TCE market-scan schedule.
- **StockDividend:** app CI and immutable ARM64 publisher evidence on `f5c04475` remain valid; no authorized production promotion. Release gate remains false. v13 only prevents pointless restart churn; it does not fix the old image or make the health gate green.
- **Mirror:** `PLATFORM_INFRA_MIRROR_TOKEN` remains missing; destination-only `Contents: write` required for `phanthienquoc/locally-uncensored-private`.
- **Media:** last inspection shows backend/frontend 1/1 with digest-pinned imageIDs; no new Media release was performed.
- **Authentication:** PR #75/#76 remain open pending production integration side-effect review; no migration or activation. No fresh Supabase probe in this review; prior bounded evidence is historical only.

Preserve CI/test/security, backup, manual/release, maintenance, and purposeful scheduled jobs. `reconcile-vps.yml` remains the only GitOps apply authority, `inspect-vps.yml` read-only, and `bootstrap-runner.yml` the only runner-helper installation authority. No direct SSH/Compose deployment authority was added. No production manifest, image reference, secret, DB object, desired replica, or schedule changed. TCE market-scan schedule unchanged. Production remains **NOT HEALTHY/UNVERIFIED**.


## Post-merge verification (2026-11-02 05:00 ICT / 2026-11-01 22:00 UTC)

- Platform Infra PR #1016 merged as `41d6a2b93334d08f20201edf5cfcf9d155c74c00`; exact-head validation #41354811426 and post-merge validation #41354880764 succeeded. Current Platform master is `41d6a2b93334d08f20201edf5cfcf9d155c74c00`.
- Supabase read-only SQL probe at 22:00:13Z passed; bounded 20:55–21:55Z logs: Edge 359, PostgREST 28, HTTP 5xx 0, HTTP 522 0.
- Issue #1015 tracks the confirmed permanent image-pull restart loop; no privileged runner helper change was deployed.
- No post-merge scheduled TCE heartbeat or correlated Platform repository_dispatch is yet verified. Preserve all TCE schedules and market-scan cadence.
- Mirror secret `PLATFORM_INFRA_MIRROR_TOKEN` is still missing; StockDividend release remains held.

## Latest automation review (2026-11-02 04:55 ICT / 2026-11-01 21:55 UTC)

- Default-branch heads: Platform Infra `628201da74d4bdd85dbc4418760f97e5d078cfac`; TCE Dashboard `d011fbb4099f5f9e24068878ac4e035b369e8ace`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; none in TCE Dashboard, StockDividend, or Media Generation.
- Platform native scheduled reconciliation [#41351121366](https://github.com/phanthienquoc/platform-infra/actions/runs/41351121366) failed only in the StockDividend health lane; shared preflight/GHCR/Auth-secret/GitOps-drift and Media/MicroFE/TCE/Auth lanes passed. Scheduled watchdog [#41351292919](https://github.com/phanthienquoc/platform-infra/actions/runs/41351292919) correctly failed at 21:18Z because the then-latest inspection was 244m old. Native inspection [#41351555469](https://github.com/phanthienquoc/platform-infra/actions/runs/41351555469) succeeded at 21:20:58Z; post-inspection recovery [#41351669202](https://github.com/phanthienquoc/platform-infra/actions/runs/41351669202) and watchdog [#41351669205](https://github.com/phanthienquoc/platform-infra/actions/runs/41351669205) succeeded and skipped duplicate dispatches. At 21:55Z reconciliation/inspection freshness was 39m/34m; multiple consecutive healthy cron intervals are not yet proven.
- **New runner issue #1015:** reconciliation #41351121366 restarted Stock Admin and Backend even though their pull messages were permanent `no match for platform in manifest` errors. Fresh inspection #41351555469 showed two blocked Admin pods and a newly created blocked Backend pod while the old Backend remained Running. Add waiting-message-aware skip logic for permanent architecture/manifest failures; preserve transient retry behavior; add mocked-kubectl tests; bump the versioned runner policy and both workflow policy gates. No production helper change was made in this review.
- Latest K3s snapshot [debug/vps-latest.md](https://github.com/phanthienquoc/platform-infra/blob/master/debug/vps-latest.md) generated 21:21:06Z: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, about 19 GiB available, GitOps drift clean, restart_required=yes. Media backend/frontend, MicroFE Shell/WS, and NATS are 1/1 with digest-pinned imageIDs. Stock Admin has two ImagePullBackOff pods on `12d63b4`; new Stock Backend pod is blocked on `12d63b4` while old Backend `23b2878` is 1/1; Frontend `23b2878` is 1/1. TCE/Auth/Keycloak remain stopped as requested.
- TCE scheduled runs remain stale: WF-06 #41342785812 (19:38:53Z, endpoint failure), WF-12 #41339371004 (18:59:02Z, stale WF-06 alert), WF-07 #41311225433 (13:26Z, before sender merge). WF-12 push #41345501969 correctly skipped heartbeat dispatch. No post-merge scheduled source run or authenticated Platform repository_dispatch is verified. Preserve all TCE cron expressions and market-scan schedules.
- StockDividend CI #41314359022 and native ARM64 publisher #41314359012 passed on `f5c04475`; paired immutable Admin/Backend/Scraper digests are recorded in the tracker. `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=false`; no promotion is authorized.
- Media CI #41246414186 passed; latest K3s snapshot shows backend/frontend 1/1 with runtime digest IDs. Auth PR #76 CI #41329425940 passed; PR #75/#76 remain open. Previous Auth migration set comparison was 84/84 but was not re-run.
- Mirror scheduled run #41347028704 failed before Git operations because `PLATFORM_INFRA_MIRROR_TOKEN` is missing. Required scope is destination-only `Contents: write` on `phanthienquoc/locally-uncensored-private`.
- Last Supabase SQL probe (20:22:20Z) passed and bounded 19:22–20:22Z logs had zero 5xx/522, but that evidence is 93m old at this review; obtain a fresh probe before making current health claims.
- Preserve the single deployment authority split: app repos own tests/builds/immutable GHCR publication; Platform Infra owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout/health; TCE has no deployment authority. `reconcile-vps.yml` remains the sole GitOps apply authority, `inspect-vps.yml` remains read-only, and `bootstrap-runner.yml` remains the sole runner-helper installation authority.

## Cross-repository schedule heartbeat contract (2026-11-02 04:05 ICT; source-run metadata validation merged; runtime dispatch pending)

- TCE Dashboard WF-12 remains the scheduled heartbeat producer. It emits `repository_dispatch: tce-schedule-heartbeat` only for its own scheduled run or a `workflow_run` completion whose source event is `schedule` and whose source workflow is WF-06 or WF-07.
- TCE sender PR #1010 remains merged at `d011fbb4099f5f9e24068878ac4e035b369e8ace`. It uses the existing `PLATFORM_INFRA_TOKEN` with Platform repository dispatch access; no new token or TCE GITHUB_TOKEN write permission is introduced.
- Platform receiver PR #1008 remains merged. Hardening PR #1012 merged as `30017a9880469ebf7b5cd0157bfea5870f112892`; exact-head lint/manifest checks and post-merge lint/manifest checks passed.
- Before using a heartbeat for freshness decisions, the receiver fetches the source TCE Actions run and the WF-12 heartbeat run from the public TCE Actions API. It verifies exact workflow path, `event=schedule`, master branch, full head SHA, and allowed run status. Direct WF-12 schedule heartbeats must use the same source/heartbeat run ID and SHA. WF-06/WF-07 source runs must be completed and forwarded by a WF-12 run with `event=workflow_run`.
- The receiver accepts only `phanthienquoc/TCE-dashboard`, the event `tce-schedule-heartbeat`, and allowlisted WF-06/WF-07/WF-12 paths. The payload carries no app, image, release, mode, or target inputs.
- TCE has no SSH, kubectl, Compose, manifest apply, or image-promotion authority. Platform recovery uses only its existing reconciliation workflow with `allow_image_changes=false` or read-only inspection.
- Runtime status remains pending: latest post-merge TCE WF-12 run #41345501969 was a push and correctly skipped heartbeat dispatch. Latest scheduled WF-06 #41342785812, WF-12 #41339371004, and WF-07 #41311225433 all predate the sender merge. Wait for a scheduled event and correlate the source run, WF-12 run, Platform repository_dispatch, and recovery run.
- Preserve the existing TCE WF-06/WF-07/WF-12 cron expressions and all market-scan schedules unchanged.


## Latest automation review (2026-11-02 02:03 ICT / 2026-11-01 19:03 UTC; TCE WF-12 correctly detected stale WF-06 delivery)

This review re-inspected the five repository master refs, open PRs, latest Actions runs/checks, the deployment tracker, the newest TCE watchdog failure log, Platform schedule history, and the latest available K3s snapshot. It found no new code defect to patch safely: the TCE watchdog failure is the intended stale-schedule alert, and the Platform watchdog failure was correctly caused by an inspection that was stale at that run's timestamp. The tracker and inventory are refreshed below; no production mutation or schedule change was made.

### Repository heads and open PRs

- platform-infra: 16c5b28b2850e92724b703daf6435e252bc725dd (PR #1006 docs evidence refresh).
- TCE-dashboard: 8882fc6dca77fc6abaaf45c673f7dfc4c8a400ae.
- stockdividend: f5c04475eb4e67811c66b350d60541b21b8262c7.
- media-generation: d8e695d772ab2dc0da5c15cc428ee78ac6537518.
- phanthienquoc-authentication: ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; no open PRs in TCE Dashboard, StockDividend, or Media Generation.

### Platform Infra latest runs and schedule evidence

- Latest master validation is [#41334595898](https://github.com/phanthienquoc/platform-infra/actions/runs/41334595898), push on master SHA 16c5b28b2850e92724b703daf6435e252bc725dd, SUCCESS. Exact-head PR validation for #1006 is [#41334540658](https://github.com/phanthienquoc/platform-infra/actions/runs/41334540658), SUCCESS. PR #1006 is merged; no newer Platform Actions run was present in the inspected first 100 runs.
- Latest scheduled reconciliation is [#41330228681](https://github.com/phanthienquoc/platform-infra/actions/runs/41330228681), created 2026-11-01 17:11:48Z. Shared repository/GHCR preflight, protected Auth runtime Secret verification, shared pull-credential reconciliation, targeted restart, and cluster verification passed. Media, MicroFE, TCE, and Auth lanes passed; StockDividend failed on the old Admin/Backend image tags with no ARM64 manifest. GitOps drift was clean; manifest apply and image-change guard were skipped. Overall FAILURE is therefore the StockDividend application health gate, not a shared reconciliation failure.
- Latest scheduled inspection is [#41330407550](https://github.com/phanthienquoc/platform-infra/actions/runs/41330407550), created 17:13:57Z and completed SUCCESS; it produced the latest available read-only VPS snapshot at approximately 17:14:04Z.
- Scheduled watchdog [#41330266961](https://github.com/phanthienquoc/platform-infra/actions/runs/41330266961), created 17:12:16Z, failed at Verify scheduled inspection delivery: at that reference time the latest scheduled inspection was still #41301947264 from 11:27:15Z (age 345m, above the 75m budget). The later #41330407550 inspection was created after this watchdog, so this is a valid time-ordered alert, not a false positive.
- Scheduled recovery [#41328484657](https://github.com/phanthienquoc/platform-infra/actions/runs/41328484657) succeeded at 16:51:47Z. Latest post-inspection workflow_run recovery/watchdog runs #41330518351 and #41330518388 both succeeded at 17:15:15Z and correctly skipped duplicate dispatches because reconciliation/inspection were fresh at that time.
- At the current review time (19:03Z), native schedule freshness has again expired: reconcile #41330228681 is about 112m old; inspection #41330407550 about 109m old; scheduled watchdog #41330266961 about 111m old; scheduled recovery #41328484657 about 132m old. Latest mirror schedule #41323952888 (15:59:10Z) predates the secret-name correction. Post-fix push smoke #41325213359 failed before Git operations because PLATFORM_INFRA_MIRROR_TOKEN was not configured. No post-fix scheduled mirror run was observed.
- Preserve reconcile-vps.yml as the sole GitOps apply authority, inspect-vps.yml as read-only, and recovery/watchdog workflows as Actions API dispatch/monitoring only. No second SSH/Compose authority was added.

### TCE Dashboard — watchdog failure is an accurate schedule alert

- Latest WF-12 scheduled run [#41339371004](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41339371004), created 2026-11-01 18:59:02Z, failed in Inspect latest scheduled WF-06 run. Its log reports WF-06 latest scheduled run #41319526719 at 15:06:39Z, age 232m, queue 0m, exceeding the 25m freshness budget. WF-06 workflow state was active. This is a real missing scheduled delivery, not runner queue delay and not a WF-12 implementation regression.
- WF-06 run #41319526719 itself had public HTTP 503 results while TCE/Auth remained intentionally scaled to zero; SSH/container diagnostics passed. Schedule delivery and endpoint health must remain separate signals.
- Latest scheduled WF-07 is #41311225433 at 13:26Z, before PR #1009's merge. No post-merge scheduled WF-07 completion has yet exercised the new WF-07-to-WF-12 heartbeat.
- TCE WF-01 build #41325592312, WF-02 format #41325592287, and WF-05 backend tests #41325592337 all passed on master SHA 8882fc6dca77fc6abaaf45c673f7dfc4c8a400ae.
- Do not weaken WF-12's stale-delivery failure to warning or treat a push/manual run as schedule evidence. Preserve WF-06/WF-07/WF-12 cron and all TCE market-scan scheduling unchanged.

### Latest available K3s snapshot and application state

- Snapshot remains the read-only inspection produced by #41330407550 (2026-11-01 17:14Z); no newer inspection was present in the inspected run history. Node tce-k3s-01 was Ready, ARM64, K3s v1.36.3+k3s1, root disk 54% used, GitOps drift clean. Host still reported restart_required=yes due pending OS package updates; no package upgrade or reboot was performed.
- Media backend/frontend and MicroFE Shell/WS were Ready 1/1; NATS 1/1. Their runtime imageIDs were recorded as digest-pinned in the snapshot.
- Stock Admin remained 0/1 ImagePullBackOff on admin:12d63b4; new Stock Backend pod remained ImagePullBackOff on backend:12d63b4 while the old backend replica remained 1/1; Stock Frontend remained on old user:23b2878, 1/1, updated=0.
- TCE, Auth, and Keycloak remained intentionally 0/0. No desired replicas were changed.

### StockDividend publication and release boundary

- Master CI [#41314359022](https://github.com/phanthienquoc/stockdividend/actions/runs/41314359022) and publisher [#41314359012](https://github.com/phanthienquoc/stockdividend/actions/runs/41314359012) succeeded on source f5c04475eb4e67811c66b350d60541b21b8262c7.
- Verified native ARM64 immutable digests remain: Scraper sha256:2146540a30d972af2d41688b6dc6640353f7552da86f740a092e85c082e7fd4f; Admin sha256:488cd38462ac66b36258cc84296fe0d2d1f9cb029c9cb53c3b93f49dfe19f621; Backend sha256:a3ec6f8c95bfb0184d97228cba25f433d942720aad728fef7716e8f5b6282c94.
- STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=false; no dispatch, manifest promotion, or rollout is authorized. Keep production refs unchanged pending explicit release authorization.
- Weekend scraper #41284033242 remains cancelled after approximately six hours on pre-optimization SHA; cause is not established. Preserve its scheduled/manual workflow and diagnose a future run rather than removing it.

### Media, Authentication, and Supabase evidence

- Media master d8e695d7; latest observed CI [#41246414186](https://github.com/phanthienquoc/media-generation/actions/runs/41246414186) passed. Latest available K3s snapshot shows backend/frontend 1/1. No new Media publication or rollout was observed.
- Authentication master ceb2688d; PR #76 current-head CI [#41329425940](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41329425940) passed; PR #75/#76 remain open. Previously verified Supabase migration source/ledger alignment was 84/84 exact version/name matches, but this was not re-run in this review and does not clear production integration side-effect gates. Auth/Keycloak remain stopped.
- Supabase project gtqovpusfyyvxpeezxlo: last recorded read-only SQL probe was 2026-11-01 16:06:18Z; no fresh SQL/log probe was performed in this review. Do not infer current health from the older bounded observation.

### External dependencies and next actions

1. Configure PLATFORM_INFRA_MIRROR_TOKEN as a Platform Infra Actions secret (or organization secret restricted to Platform Infra), with destination-only Contents: write on phanthienquoc/locally-uncensored-private; then verify a new scheduled mirror run and its workflow_run heartbeat.
2. Continue observing native Platform scheduled reconciliation/inspection and TCE WF-06/WF-07 cadence. Keep watchdog failures fail-closed when delivery is genuinely stale; do not mislabel queue=0 as a schedule recovery.
3. Keep StockDividend promotion disabled until explicit authorization; if authorized later, consume the paired immutable digests and verify all three runtime imageIDs after rollout.
4. Obtain a fresh read-only K3s inspection before making any new runtime claims. Do not reboot/upgrade the VPS without a maintenance window.
5. Keep Auth/Keycloak at zero replicas and preserve all TCE market-scan schedules.

No production manifests, release flags, credentials, database objects, desired replicas, image cleanup, or schedule expressions were changed in this review.

---

# Cross-Repository Workflow Inventory

## Latest workflow inventory review (2026-11-01 16:18 UTC; mirror secret naming corrected; TCE independent heartbeat merged)

### Repository heads and open PRs

- Master heads: Platform Infra `7b294c98eefcb54287dca54944cb0fcae51da71e`; TCE Dashboard `8882fc6dca77fc6abaaf45c673f7dfc4c8a400ae`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; none in TCE, StockDividend, or Media.
- Platform Infra #998 (schedule heartbeat), #999 (fresh inspection snapshot), #1000/#1002 (tracker refreshes), and #1001 (mirror secret-name fix) are merged; TCE Dashboard #1009 (WF-07 independent heartbeat) is merged. No workflow was removed.

### Platform workflow inventory and runtime evidence

- Recovery controller and read-only schedule watchdog now also accept completed scheduled runs from the existing mirror workflow as an independent heartbeat. Exact source path, master branch, and `event=schedule` are required. Manual/push mirror runs are ignored. Cron expressions and deployment authorities are unchanged.
- PR #998 exact-head validation [#41324459254](https://github.com/phanthienquoc/platform-infra/actions/runs/41324459254) and [#41324459291](https://github.com/phanthienquoc/platform-infra/actions/runs/41324459291) passed; post-merge [#41324507161](https://github.com/phanthienquoc/platform-infra/actions/runs/41324507161) and [#41324507168](https://github.com/phanthienquoc/platform-infra/actions/runs/41324507168) passed.
- Recovery push [#41324507322](https://github.com/phanthienquoc/platform-infra/actions/runs/41324507322) verified dispatch of reconciliation #41324521466 on exact master SHA with `mode=apply`, `allow_image_changes=false`, `target_app=all`.
- Reconciliation #41324521466 shared preflight/credential/cluster work passed; no drift so manifest apply skipped; Media/TCE/MicroFE/Auth lanes passed; StockDividend health failed on old non-ARM64 tags.
- Recovery #41324707002 passed the completed-source wait and API reference-clock steps, did not dispatch a duplicate reconciliation, and verified dispatch of read-only inspection #41324734578 because the last inspection was 112m old.
- Inspection #41324734578 succeeded. PR #999 exact-head validation #41324798596 passed; PR merged as `92f85ff`. Fresh snapshot: node Ready/ARM64, disk 54%, runner services active; Media/MicroFE 1/1; Stock Admin/Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend replicas remain; TCE/Auth/Keycloak 0/0.
- Normal scheduled Platform runs remain stale: reconcile #41300948892 (11:13:47Z), inspection #41301947264 (11:27:15Z), watchdog #41301007488 (11:14:36Z). No scheduled recovery-controller run observed.
- Mirror schedule [#41323952888](https://github.com/phanthienquoc/platform-infra/actions/runs/41323952888) was delivered at 15:59:10Z but failed because the workflow referenced invalid hyphenated secret name `Platform-infra-token`. PR #1001 now uses valid `PLATFORM_INFRA_MIRROR_TOKEN`; the secret value still needs to be configured with destination-only `Contents: write`. The mirror-triggered recovery/watchdog path awaits its first post-merge mirror completion.

### Mirror credential correction

- The old `Platform-infra-token` secret name contained hyphens and was invalid under GitHub Actions naming rules. PR #1001 now references `PLATFORM_INFRA_MIRROR_TOKEN` and enforces it in `validate-workflow-contracts.py`.
- The secret value still must be created in Platform Infra's Actions secret scope (or an organization scope limited to Platform Infra), with destination-only `Contents: write` on `phanthienquoc/locally-uncensored-private`. No token value is stored in the repository.

### Application workflow inventory

- TCE Dashboard: WF-06 latest scheduled #41319526719 at 15:06:39Z failed only at public HTTP 503 health endpoints while TCE/Auth remain stopped; SSH diagnostics passed. WF-12 workflow_run follow-up #41319543937 succeeded. Latest scheduled WF-12 #41315132135 at 14:13:39Z reported stale WF-06. WF-07 scheduled #41311225433 at 13:26Z passed. PR #1009 adds WF-07 scheduled completion as an independent read-only WF-12 heartbeat with exact path/event guards; PR checks #41325492972/#41325493160 passed and post-merge WF-12 push smoke #41325592270 correctly warned that WF-06 was 71m old. The first post-merge scheduled WF-07 heartbeat is pending. Preserve all existing schedules and the market-scan cadence.
- StockDividend: CI #41314359022 and ARM64 publisher #41314359012 passed on source `f5c04475`. All three immutable digests remain verified. Production release gate remains false; no digest dispatch or GitOps promotion.
- Media Generation: latest CI #41246414186 passed; fresh K3s snapshot confirms backend/frontend 1/1 with digest-pinned imageIDs.
- Authentication: latest CI #41033586844 and manual release #41040510320 passed on current master. Auth/Keycloak remain stopped; PR #75/#76 remain open pending environment and migration safety evidence.

### External dependencies and operational notes

- Mirror requires `PLATFORM_INFRA_MIRROR_TOKEN` with only target repository `Contents: write`; the previous hyphenated name was invalid under GitHub's secret naming rules. Do not reuse GHCR_READ_TOKEN or app dispatch credentials.
- Supabase project `gtqovpusfyyvxpeezxlo` was `ACTIVE_HEALTHY`; read-only SQL at 16:06:18Z passed. Bounded 15:00–16:06Z logs: 397 edge / 33 PostgREST, zero HTTP 522 mentions and zero statement-timeout mentions.
- VPS reports `restart_required=yes` due pending OS package updates. Do not upgrade/reboot without an approved maintenance window.
- Preserve weekly/manual image cleanup, manual/release workflows, CI/test/security jobs, and all existing deployment authorities. No SSH/Compose authority was added.

## Previous workflow inventory review (2026-11-01 15:08 UTC; recovery-controller fixes merged; TCE WF-06 delivery observed)

### Repository heads and open PRs

- Master heads: platform-infra `f98e65050968810b71027d77a83268284c0df9ea`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; no open PRs in TCE, StockDividend, or Media.
- Platform recovery fixes #995 and #996 are merged. PR #995 uses workflow resource path rather than dynamic `workflow_run.name`; PR #996 anchors recovery freshness after source completion.

### Latest Platform Infra workflow evidence

- PR #995 exact-head validation: [#41319147036](https://github.com/phanthienquoc/platform-infra/actions/runs/41319147036) and [#41319146752](https://github.com/phanthienquoc/platform-infra/actions/runs/41319146752), both SUCCESS; post-merge [#41319189184](https://github.com/phanthienquoc/platform-infra/actions/runs/41319189184) and [#41319189181](https://github.com/phanthienquoc/platform-infra/actions/runs/41319189181), both SUCCESS.
- PR #996 exact-head [#41319502754](https://github.com/phanthienquoc/platform-infra/actions/runs/41319502754) and [#41319502774](https://github.com/phanthienquoc/platform-infra/actions/runs/41319502774), both SUCCESS; post-merge [#41319548298](https://github.com/phanthienquoc/platform-infra/actions/runs/41319548298) and [#41319548285](https://github.com/phanthienquoc/platform-infra/actions/runs/41319548285), both SUCCESS.
- Recovery push [#41319548302](https://github.com/phanthienquoc/platform-infra/actions/runs/41319548302) SUCCESS; it observed recent reconciliation/inspection and correctly did not dispatch duplicates.
- Reconciliation [#41319201561](https://github.com/phanthienquoc/platform-infra/actions/runs/41319201561): shared preflight/credential reconciliation/cluster verification PASS; no drift so manifest apply skipped; Media/TCE/MicroFE/Auth lanes PASS; StockDividend health FAIL; Keycloak skipped. Overall run FAILURE is expected from StockDividend.
- Recovery handoff [#41319362275](https://github.com/phanthienquoc/platform-infra/actions/runs/41319362275) exposed the reference-clock ordering bug; PR #996 fixed it. Runtime proof of the source-run wait branch remains pending.

### TCE Dashboard

- Latest scheduled WF-06 [#41319526719](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41319526719) delivered at 15:06:39Z. SSH diagnostic PASS; four public endpoints returned 503 because TCE/Auth are intentionally stopped.
- WF-12 workflow-run follow-up [#41319543937](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41319543937) SUCCESS; age 0m, queue 0m, schedule delivery fresh.
- WF-07 scheduled [#41311225433](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41311225433) SUCCESS. Preserve WF-06/WF-07/WF-12 and the TCE market-scan schedule unchanged.

### StockDividend

- Master CI [#41314359022](https://github.com/phanthienquoc/stockdividend/actions/runs/41314359022) and publisher [#41314359012](https://github.com/phanthienquoc/stockdividend/actions/runs/41314359012) SUCCESS on `f5c04475eb4e67811c66b350d60541b21b8262c7`.
- Verified ARM64 digests: scraper `sha256:2146540a30d972af2d41688b6dc6640353f7552da86f740a092e85c082e7fd4f`; admin `sha256:488cd38462ac66b36258cc84296fe0d2d1f9cb029c9cb53c3b93f49dfe19f621`; backend `sha256:a3ec6f8c95bfb0184d97228cba25f433d942720aad728fef7716e8f5b6282c94`.
- Production release flag remains false; no handoff or digest dispatch. Current K3s still references old `12d63b4` Admin/Backend images, which lack ARM64 manifests.
- Weekend scraper #41284033242 cancelled after six hours on pre-fix SHA; retain its schedule/manual trigger and checkpointing.

### Media, Authentication, Supabase

- Media master `d8e695d7`; latest Media CI [#41246414186](https://github.com/phanthienquoc/media-generation/actions/runs/41246414186) SUCCESS. Latest reconciliation Media lane PASS; prior fresh K3s inspection [#41315143069](https://github.com/phanthienquoc/platform-infra/actions/runs/41315143069) recorded backend/frontend 1/1.
- Authentication master `ceb2688d`; CI [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844) and release [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) are historical SUCCESS. PR #75/#76 remain open; Auth/Keycloak intentionally stopped.
- Supabase `gtqovpusfyyvxpeezxlo`: SQL probe 14:03:48Z PASS; 13:00–14:04Z log query found 0 HTTP 522, 0 HTTP 5xx, 0 statement timeout matches.

### Workflow ownership and safety

- App repositories own CI, tests/builds, and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, K3s rollout and health verification.
- `reconcile-vps.yml` remains the sole GitOps apply authority; `inspect-vps.yml` remains read-only; `recover-stale-ops.yml` dispatches only these existing authorities.
- Recovery dispatch uses master ref/full SHA and `allow_image_changes=false`; StockDividend production release remains gated by explicit authorization.
- Platform scheduled reconciliation/inspection are still stale (latest scheduled reconcile 11:13:47Z; inspection 11:27:15Z). Push recovery works, but schedule cadence is not yet proven restored.
- Mirror workflow still requires `Platform-infra-token` with destination-only Contents:write.
- Preserve useful CI, test, security, backup, manual, release, and scheduled workflows. No duplicate SSH/Compose authority; no TCE market-scan schedule change.

---

# Cross-Repository Workflow Inventory


## Latest workflow inventory review (2026-11-01 14:16 UTC; recovery bootstrap and StockDividend ARM64 publication)

- Current master heads: platform-infra `ee0e12310a8ec34711d3d7b26feaa4b4664da4eb`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; no TCE/StockDividend/Media PRs. PR #22/#23 (StockDividend), #991/#992 (Platform recovery), and inspection PR #993 are merged.
- StockDividend master CI #41314359022 and publisher #41314359012 succeeded on source SHA `f5c04475eb4e67811c66b350d60541b21b8262c7`. Verified ARM64 registry digests: Scraper `sha256:2146540a30d972af2d41688b6dc6640353f7552da86f740a092e85c082e7fd4f`; Admin `sha256:488cd38462ac66b36258cc84296fe0d2d1f9cb029c9cb53c3b93f49dfe19f621`; Backend `sha256:a3ec6f8c95bfb0184d97228cba25f433d942720aad728fef7716e8f5b6282c94`. Promotion remains disabled; handoff/dispatch skipped.
- StockDividend PR #23 removed duplicate collection/checkpoint lookups and its AST regression test passed in 5/5 CI jobs. Weekend scraper #41284033242 was cancelled after six hours on pre-fix SHA `a6f55ee`; preserve its schedule/manual trigger and MongoDB checkpoint behavior.
- Platform recovery PR #991 added master push bootstrap; push recovery #41314613083 verified reconciliation dispatch #41314625253 with `mode=apply`, `allow_image_changes=false`, `target_app=all`. Shared preflight/credential bootstrap succeeded; Auth runtime Secret was provisioned/verified with values suppressed; GHCR pull credentials reconciled; only blocked StockDividend Admin/Backend deployments restarted. No manifest drift, so `kubectl apply` was skipped. StockDividend health failed on old tag `12d63b4`; MicroFE/Auth/TCE/Media lanes passed; Keycloak skipped.
- Platform recovery PR #992 added post-lane workflow_dispatch handoff with source run ID/full SHA verification. Exact-head lint, manifest, and Keycloak checks passed; post-merge checks passed. Runtime verification of this new post-reconcile handoff remains pending.
- Push recovery #41315123963 verified inspection dispatch #41315143069 after observing reconciliation fresh and inspection stale. Inspection #41315143069 succeeded and PR #993 merged, refreshing `debug/vps-latest.md` at 14:13:55Z. K3s node Ready/ARM64, disk 54%, drift clean; Media/MicroFE 1/1; Stock Admin/Backend still ImagePullBackOff on `12d63b4`; old Backend/Frontend replicas remain Running; TCE/Auth/Keycloak 0 replicas intentionally.
- Platform scheduled reconcile #41300948892 remains latest scheduled run (11:13:47Z, StockDividend health failure); scheduled inspection #41301947264 remains 11:27:15Z. The 14:13 inspection was workflow_dispatch, not schedule recovery. TCE WF-07 #41311225433 succeeded at 13:26Z; WF-06 #41287060151 remains last scheduled run at 09:01:02Z with public 503s while TCE/Auth are intentionally stopped. Preserve all cron and TCE market-scan schedules.
- Supabase project `gtqovpusfyyvxpeezxlo` ACTIVE_HEALTHY; SQL probe 14:03:48Z PASS; corrected 13:00–14:04Z log query: 382 edge, 28 PostgREST, 0 HTTP 522, 0 HTTP 5xx, 0 statement timeout matches. Mirror workflow #41292061857 still lacks `Platform-infra-token` (target repo Contents:write required).
- Media CI #41246414186 and Authentication CI/release #41033586844/#41040510320 are historical; fresh Media runtime health is recorded in inspection #41315143069. Auth PRs #75/#76 remain open pending migration/environment evidence.
- Preserve CI/test/security/backup/manual/release/scheduled jobs. No workflow removal, no production image promotion, no manifest image change, no database mutation, no image deletion, no new SSH/Compose deployment authority. Protected Auth/GHCR runtime credential reconciliation and targeted StockDividend pod restarts were performed by the existing reconcile authority. TCE market-scan schedule unchanged.


## Latest workflow inventory review (2026-11-01 14:05 UTC; StockDividend ARM64 publication complete)

- Current master heads: platform-infra `988f88a30b0fd1039ee78674cfdc7b9735e44dea`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `1559097da834652e2f6dfbd5a8d012a526f0133b`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; StockDividend #23; no TCE or Media PRs.
- StockDividend master CI #41309267914 and publisher #41309267904 succeeded on full source SHA `1559097da834652e2f6dfbd5a8d012a526f0133b`. Verified native ARM64 registry digests: Scraper `sha256:a227b5d235c7518a7d4a7106099ebfe18e59164f922db6a1689f7702c03ad55d`; Admin `sha256:9c55955ec3cb2d6daceaa7419865c10ac552e54c48d42f412179ae48fdafcf58`; Backend `sha256:1ffc7ed921742b4d5004038afd50e7086f3646947ea07e8a07fc2a6fa49acce1`. Promotion gate remained disabled and both handoff/dispatch jobs were skipped. No GitOps promotion occurred.
- Weekend scraper #41284033242 was cancelled at 13:15:44Z after six hours; it used pre-fix SHA `a6f55ee`. Preserve the weekend schedule/manual trigger. MongoDB per-page checkpoints allow subsequent runs to skip pages already recorded; cancellation cause is not established by summary alone.
- StockDividend PR #23 removes duplicate collection initialization and duplicate per-page checkpoint lookup. Exact-head CI #41314185812 was queued at 14:02:41Z; merge remains blocked until every required check passes on the exact PR head.
- Platform master validation #41309372167 succeeded at 13:03:12Z. Latest scheduled reconcile #41300948892 failed at StockDividend health (11:13:47Z); latest scheduled inspection #41301947264 succeeded at 11:27:15Z; watchdog #41301007488 failed at 11:14:36Z. No newer Platform schedule/recovery-controller runtime event observed through 14:05Z. PR #986 workflow_run fallback remains unverified.
- TCE WF-07 schedule #41311225433 succeeded at 13:26Z. WF-06 last scheduled run #41287060151 at 09:01:02Z failed public health while TCE/Auth are intentionally stopped. Scheduled WF-12 #41315132135 at 14:13:39Z correctly failed freshness because WF-06 was 312m old with 0m queue. This is a schedule-delivery gap, not runner queue delay. Preserve WF-06/WF-12 cron and market-scan schedule.
- Media CI #41246414186 and Authentication CI/release #41033586844/#41040510320 are historical successes; no new app runs observed. Keep Auth manual-only and preserve PRs #75/#76 pending migration/environment evidence.
- Latest K3s snapshot #41304636230 is push-triggered at 12:03:24Z: node Ready/ARM64, disk 54%, GitOps drift clean, CRI inventories present; Media/MicroFE 1/1; StockDividend Admin/Backend blocked on old non-ARM64 `12d63b4`; TCE/Auth/Keycloak 0/0 intentionally. Cleanup dry-run #41305323263 passed with no removals. No newer inspection.
- Mirror workflow #41292061857 still lacks `Platform-infra-token`; owner-side setup requires a target-repository-scoped `Contents: write` token. Do not substitute unrelated credentials.
- No workflow was removed; preserve CI, tests, security, backup, manual/release, scheduled scraper, and TCE market-scan jobs. No production manifest, secret, credential, release flag, database object, or desired replica changed.

## Latest workflow inventory review (2026-11-01 13:02 UTC; StockDividend scraper navigation fix merged)

- Current master heads: platform-infra `2ca13b13f8aeb9a6035d928af08eee8259c1681d`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `1559097da834652e2f6dfbd5a8d012a526f0133b`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none in TCE, StockDividend, or Media.
- StockDividend PR #22 merged as `1559097`; exact-head CI #41309092011 passed all five jobs, including the new scraper single-navigation AST contract. Post-merge CI #41309267914 remains in progress. Publisher #41309267904 passed master and release-gate checks, but image build/push is queued and release handoff skipped because production release remains disabled. No new post-merge digest has been verified.
- Weekend scraper #41284033242 remains in progress on pre-fix SHA `a6f55ee`; preserve its weekend schedule/manual trigger. The duplicate-navigation fix affects future runs only; do not claim the active run benefited.
- Platform Infra PR #988 merged as `2ca13b13`; exact-head and post-merge manifest validations #41309196476/#41309250988 passed.
- Platform schedule evidence is unchanged: latest scheduled reconciliation #41300948892 failed at StockDividend health; scheduled inspection #41301947264 and watchdog #41302040071 passed. No newer scheduled run or post-merge recovery-controller execution was observed through 13:02Z. Keep existing cron schedules and verify the next actual event before declaring recovery.
- Latest K3s snapshot #41304636230 remains push-triggered at 12:03:24Z, not scheduled-delivery evidence. Node Ready/ARM64, disk 54%, GitOps drift clean; CRI inventory present; Media/MicroFE 1/1; StockDividend admin/backend blocked on old non-ARM64 `12d63b4`; TCE/Auth/Keycloak 0/0 intentionally.
- Cleanup dry-run #41305323263 succeeded with no image removals. Preserve weekly/manual cleanup, dry-run push/schedule, and fail-closed reference handling.
- TCE master push CI WF-01/WF-02/WF-05/WF-12 passed; latest scheduled WF-06 #41287060151 remains the last observed scheduled healthcheck and returned 503 while TCE/Auth are intentionally stopped. Preserve all TCE cron expressions and market-scan schedule.
- Media CI #41246414186 remains the latest successful master CI; K3s health is from #41304636230. Authentication CI/release #41033586844/#41040510320 are historical; keep Auth manual-only and preserve open PRs #75/#76 pending migration/environment evidence.
- Supabase project status `ACTIVE_HEALTHY`; read-only SQL probe at 14:03:48Z passed. Corrected status-code query 13:00–14:04Z: 382 edge events, 28 PostgREST events, 0 HTTP 522, 0 HTTP 5xx, 0 statement-timeout matches. This is a bounded observation, not a long-term stability claim.
- Mirror workflow #41292061857 still lacks `Platform-infra-token`; owner-side setup requires a target-repository-scoped `Contents: write` token. Do not substitute unrelated credentials.
- Preserve all CI/test/security/backup/manual/release/scheduled jobs. No workflow was removed, no production manifest/credential/release flag/database object/desired replica changed, and no duplicate SSH/Compose authority added.

---

## Latest workflow inventory review (2026-11-01 12:57 UTC; scraper navigation optimization PR opened)

- Current master heads: platform-infra `d551bcfbc761f927607db501fdb373afc564474e`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; StockDividend #22 (CI in progress); no TCE or Media PRs.
- Platform master validation #41305496035 succeeded at 12:14:06Z; no later Platform workflow run was observed through 12:57Z. Latest scheduled reconcile #41300948892 failed at StockDividend health, latest scheduled inspection #41301947264 succeeded at 11:27:15Z, and watchdog #41302040071 succeeded at 11:28:34Z. No post-merge runtime execution of recovery-controller PR #986 was observed; its new scheduled-inspection workflow_run trigger remains unverified.
- Recovery authority boundaries remain unchanged: recovery dispatches only the existing `reconcile-vps.yml` apply path with `allow_image_changes=false`, or the existing read-only `inspect-vps.yml`; no second SSH/Compose authority exists. Cron schedules remain unchanged.
- Latest K3s inspection #41304636230 was push-triggered at 12:03:24Z and succeeded: node Ready/ARM64, disk 54%, GitOps drift clean, CRI image/container inventory present; Media and MicroFE workloads 1/1; StockDividend admin/backend blocked on old non-ARM64 tag `12d63b4`; TCE/Auth/Keycloak 0/0 intentionally. This is not scheduled-delivery evidence.
- Cleanup dry-run #41305323263 passed with no removals (`unused_images=8 retain=10 remove=0 dry_run=true`). Keep weekly/manual cleanup and fail-closed safeguards.
- StockDividend PR #22 removes a duplicate per-page Selenium navigation and adds an AST regression test in CI. Exact head `0f694bf391a41b244c61d7de45b2a791c8e869c0`; CI #41309092011 remains in progress at 12:57Z. Syntax/navigation contract and release-hold jobs passed; backend, admin, and container-build jobs were still running. Do not merge until all required checks pass.
- Weekend scraper run #41284033242 remains active since 07:15:11Z; all setup steps complete and scraper step still running at 12:57Z. The current run uses old master and is not affected by PR #22. Preserve the Saturday/Sunday schedule and manual dispatch; no cancellation issued.
- StockDividend immutable ARM64 publication #41273202844 remains verified, but production release is disabled and no dispatch/promotion occurred. Do not modify production image tags without authorization.
- TCE master WF-01/WF-02/WF-05/WF-12 push runs #41291809038/#41291809188/#41291809106/#41291809063 passed; latest scheduled WF-06 #41287060151 reported 503 because TCE/Auth are intentionally stopped. Preserve TCE market-scan and healthcheck schedules.
- Media CI #41246414186 is the latest successful master CI; runtime health supported by inspection #41304636230. Authentication CI/release runs #41033586844/#41040510320 are historical; keep Auth manual-only and preserve open PRs #75/#76 pending migration/environment evidence.
- Mirror workflow #41292061857 still lacks `Platform-infra-token`; owner-side setup needs a target-repository-scoped `Contents: write` token. Do not substitute unrelated credentials.
- Supabase has no new probe in this review; latest recorded SQL probe passed at 12:07:39Z, while log query failed at backend. No database stability claim is made.
- No workflow was removed; preserve CI, test, security, backup, manual/release, scheduled scraper, and TCE market-scan jobs. No production manifest, secret, credential, release flag, database object, or desired replica changed.

---

## Latest workflow inventory review (2026-11-01 12:12 UTC; safe cleanup dry-run and scheduled-inspection recovery)

- Current heads: platform-infra 86cf196ae7049d226797bddbf1e6dedbd3db945e; TCE Dashboard 49fe5841cce460df2a7be6d8846b34a57b6be152; StockDividend a6f55ee2e511ab5910c825e56803bd82fe9a0f62; Media Generation d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none in TCE, StockDividend, or Media.
- PR #985 narrows cleanup resolution to terminal Pods or ImagePullBackOff/ErrImagePull Pods with empty imageID and no local CRI image. All existing CRI container IDs remain protected. PR checks #41305229622/#41305229705 and post-merge #41305323253/#41305323287 passed. Push dry-run #41305323263 succeeded with unused_images=8, retain=10, remove=0, dry_run=true; no deletion occurred.
- PR #986 extends recover-stale-ops workflow_run triggers to reconcile-vps completions and scheduled inspect-vps completions from master. Push/manual inspection completions do not trigger the fallback. Dispatch remains through reconcile-vps only, with allow_image_changes=false and exact SHA correlation. Exact-head checks #41305336219/#41305336211 and post-merge #41305383714/#41305383799 passed; runtime event verification pending.
- PR #981 switched inspection to the allowlisted platform-crictl wrapper; PR #982 committed a fresh snapshot with CRI image/container inventories; PR #984 refreshed tracker/inventory. Snapshot #41304636230 confirms Media/MicroFE healthy, TCE/Auth/Keycloak 0/0, StockDividend admin/backend blocked on old non-ARM64 tag 12d63b4, node Ready, disk 54%, and GitOps drift clean.
- Platform reconciliation is stale after scheduled run #41300948892 (11:13:47Z). Scheduled inspection #41301947264 (11:27:15Z) and watchdog #41302040071 passed, but no newer scheduled reconciliation or recovery-controller run was observed. Push inspection #41304636230 does not prove schedule delivery. Verify the next scheduled inspection event triggers the new recovery fallback before claiming cadence recovery.
- TCE WF-06 last scheduled run #41287060151 (09:01:02Z) failed HTTP 503 while services are intentionally stopped; WF-12 latest run #41291809063 was push-triggered at 09:08:42Z, with no newer scheduled run observed. Preserve WF-06/WF-12 cron and market-scan schedule.
- StockDividend immutable ARM64 publication #41273202844 remains verified; production promotion stays disabled. Weekend scraper #41284033242 remains active; its 1,000-page queue and duplicate navigation explain potentially long runtime. Preserve scheduled/manual scraper jobs.
- Media CI #41246414186 remains successful and the fresh snapshot shows backend/frontend 1/1. Authentication CI/release #41033586844/#41040510320 are historical successes; Auth/Keycloak remain intentionally stopped.
- Supabase SQL probe passed at 12:07:39Z; unified logs query returned a backend error, so log health is not inferred.
- No workflow removed, no duplicate direct SSH/Compose authority added, and no production manifest/credential/database/release flag/replica changed.

---

## Previous workflow inventory review (2026-11-01 12:07 UTC; restricted CRI inspection and terminal-Pod cleanup contract)

- Current heads: platform-infra `ff14d67a0b17de7a6bac5e0db2938ddbe0b713ec`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none in TCE, StockDividend, or Media.
- PR #981 aligns VPS inspection with the runner's existing restricted `platform-crictl` wrapper. Inspection now requires valid JSON image/container inventories, and avoids unsupported sudo for Docker/disk diagnostics. PR #982 records a fresh snapshot with CRI inventories present. PR #983 narrows the cleanup fail-closed rule: unresolved references from terminal Pods may be ignored only when no local image exists; unresolved Pending/Running/Unknown Pod refs still block cleanup. All three PRs were merged after exact-head validation.
- Validation evidence: #981 PR lint/manifest #41304584095/#41304584154 and post-merge #41304636196/#41304636183 passed; #982 inspection validation #41304694475 passed; #983 PR lint/manifest #41304887010/#41304886843 and post-merge #41304930174/#41304930186 passed.
- Fresh inspection [#41304636230](https://github.com/phanthienquoc/platform-infra/actions/runs/41304636230) completed and snapshot PR #982 merged. It confirms Media/MicroFE ready, TCE/Auth/Keycloak stopped at 0/0, StockDividend admin/backend image pulls blocked on non-ARM64 tag `12d63b4`, node Ready, disk 54%, and GitOps drift clean.
- Cleanup push dry-run [#41304930180](https://github.com/phanthienquoc/platform-infra/actions/runs/41304930180) remains a deliberate failure gate: terminal klipper-helm is ignored, while two active StockDividend Pending refs cause exit 3. `DRY_RUN=true`; no image was deleted. Preserve weekly/manual cleanup and fail-closed behavior.
- Platform scheduled reconciliation remains stale after #41300948892 (11:13:47Z); inspection schedule delivered #41301947264 (11:27:15Z), and its watchdog #41302040071 passed. Push inspection #41304636230 is not scheduled-delivery evidence. No `recover-stale-ops` run observed; continue monitoring before claiming cadence recovery.
- TCE WF-06 last scheduled event #41287060151 (09:01:02Z) failed HTTP 503 while services are intentionally stopped; WF-12 latest run #41291809063 was push-triggered (09:08:42Z), with no newer scheduled run observed. Preserve WF-06/WF-12 and all existing cron expressions; do not alter the market-scan schedule.
- StockDividend ARM64 publication #41273202844 remains verified; production promotion stays disabled. Weekend scraper #41284033242 remains active; preserve its scheduled/manual job.
- Media CI #41246414186 remains successful and the fresh runtime snapshot shows backend/frontend 1/1. Authentication CI/release #41033586844/#41040510320 are historical successes; Auth/Keycloak remain intentionally stopped.
- Supabase SQL probe passed at 12:07:39Z; unified logs query returned a backend error, so log health is not inferred.
- No workflow removed, no duplicate direct SSH/Compose authority added, no production manifest/credential/database/release flag/replica changed.

---

## Previous workflow inventory review (2026-11-01 18:19 ICT; recovery controller event-driven fallback added)

- Current heads: platform-infra `af3c383a3f22191f3eadac61b02fa612e188cf95`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media.
- `recover-stale-ops.yml` preserves its 15-minute schedule and manual dispatch, and now also listens for completed `reconcile-vps` runs from master. It can recover stale inspection delivery after a reconciliation completion without creating a second apply/SSH/Compose authority. Runtime verification of this new trigger is pending.
- PR #978 exact-head lint/manifest checks #41301290971/#41301290921 and post-merge #41301323762/#41301323710 all passed.
- Scheduled reconciliation #41300948892 was delivered and shared reconciliation succeeded; MicroFE/TCE/Auth/Media health passed, StockDividend health failed on old non-ARM64 tag `12d63b4`. No manifest apply/image promotion occurred.
- Watchdog #41301007488 confirmed reconciliation age/queue 0m but failed inspection freshness (last inspection #41264393955 age 539m). Await the next inspection schedule and the new workflow_run recovery dispatch.
- K3s cleanup dry-run #41300876011 remains fail-closed on old StockDividend refs and klipper-helm; no image deletion. Preserve the weekly/manual cleanup workflow and safe push dry-run.
- StockDividend immutable ARM64 publisher #41273202844 passed; promotion disabled. Weekend scraper #41284033242 remains in progress; preserve scheduled/manual workflow while reviewing its long runtime.
- TCE WF-06/WF-12, market-scan schedule, Media/MicroFE runtime contracts, Auth manual-only release, backup/security/test workflows remain unchanged.
- No workflow removed, no duplicate direct SSH/Compose authority added, and no production manifest/credential/database/release flag/replica changed.

## Latest workflow inventory review (2026-11-01 18:15 ICT; one scheduled reconcile observed)

- Current heads: platform-infra `817d3c5c3029a95a47f9aaca8645e802172d7eb4`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media.
- New scheduled reconciliation [#41300948892](https://github.com/phanthienquoc/platform-infra/actions/runs/41300948892) was delivered at 11:13:47Z. Shared reconciliation succeeded; MicroFE, TCE, Auth, and Media lanes passed; Keycloak skipped; StockDividend failed because admin/backend still reference non-ARM64 tag `12d63b4`. No manifest apply or image promotion occurred.
- Scheduled watchdog [#41301007488](https://github.com/phanthienquoc/platform-infra/actions/runs/41301007488) observed reconciliation age/queue 0m, but failed inspection freshness: last inspection #41264393955 age 539m. One fresh reconcile is not sufficient to claim stable cadence.
- No `recover-stale-ops` run observed; the fresh reconciliation was an ordinary scheduled event, not a recovery-controller dispatch. Next inspection slot 11:32Z.
- `vps-image-cleanup.yml` remains a safe push/schedule dry-run plus explicit manual workflow. Latest dry-run #41300876011 correctly failed closed on three unresolved refs and deleted nothing. Keep the cleanup guard.
- StockDividend publisher #41273202844 has verified three ARM64 digests, but production promotion remains disabled. Preserve manual/release gates.
- Weekend scraper #41284033242 remains in progress; preserve its schedule/manual entry and review runtime before adding a timeout.
- TCE WF-06/WF-12, TCE market-scan schedule, Media CI/runtime verification, Auth manual-only release, and all purposeful backup/security/test workflows remain unchanged.
- No workflow removed, no duplicate direct SSH/Compose authority added, and no production manifests/credentials/database/release flags/replicas changed.

## Latest workflow inventory review (2026-11-01 18:13 ICT; cleanup normalization merged)

- Current heads: platform-infra `deaf37cdb3a536e06a78336b8ec710356ab2b4d1`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media.
- `vps-image-cleanup.yml` is retained as a purposeful production operations workflow. It preserves the weekly Sunday cron `30 3 * * 0` and explicit manual dispatch. A path-scoped master-push smoke now runs after cleanup script/test/workflow changes; push and schedule are forced to `DRY_RUN=true`, while only manual dispatch can honor `dry_run=false`.
- `scripts/cleanup-k3s-images.sh` now uses the installed restricted CRI wrapper contract (`ps`, `images`, `rmi <full-sha256>`), reads newline-delimited refs safely, normalizes Docker Hub shorthand to canonical CRI names, and rechecks fresh Pod/container/image inventories immediately before deletion. Any unresolved Pod image reference fails closed.
- Cleanup regression test `scripts/tests/cleanup-k3s-images.test.sh` runs in `validate-github-actions.yml`; it covers GHCR explicit refs, Docker Hub shorthand/canonical names, retention ordering, dry-run non-deletion, and unresolved-ref failure.
- PR #971 (jq rawfile), #972 (safe push dry-run), #973 (restricted CRI wrapper), and #975 (Docker Hub normalization) are merged. Exact-head lint/manifest checks passed for each; post-merge lint/manifest checks at `deaf37c` passed.
- Live push dry-run #41300876011 reached the fail-closed guard after successful prerequisites/CRI inventory. Normalization resolved NATS and most Rancher refs; only StockDividend old admin/backend tags and `rancher/klipper-helm` remained unresolved. Exit 3, no image deletion. Do not mark cleanup healthy until these references are understood.
- `recover-stale-ops.yml` schedule remains unverified; no run observed through 11:12Z after the controller's merge. Reconciliation/inspection schedules remain preserved.
- TCE WF-06 `*/15 * * * *`, WF-12 watchdog, manual checks, and all market-scan schedules remain unchanged. Latest WF-06 #41287060151 failed because TCE/Auth are intentionally stopped; WF-12 push smoke #41291809063 passed.
- StockDividend app CI and immutable publisher #41273202852/#41273202844 passed; all three ARM64 digests verified. Production promotion remains disabled. Weekend scraper #41284033242 remains in progress; preserve the scheduled/manual job while reviewing its long runtime.
- Media CI #41246414186 passed; last full runtime snapshot #41275351280 showed Media/MicroFE 1/1 and matching pinned imageIDs. No fresh full inspection after today's cleanup.
- Supabase SQL probe passed at 11:08:08Z. Auth CI/release evidence remains historical; keep Auth PR #75/#76 open pending environment/migration safety. Preserve manual-only Auth release.
- No workflow removed, no second direct SSH/Compose authority added, no production manifest/credential/database/release flag/replica changed, and no image was deleted.

## Latest workflow inventory review (2026-11-01 18:08 ICT; cleanup workflow safely smoke-tested)

- Current heads: platform-infra `a760e94d8f103e23caec07c095115475664bb627`; TCE Dashboard `49fe5841cce460df2a7be6d8846b34a57b6be152`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media.
- Platform Infra PR #971 fixed jq handling of newline-delimited Pod image refs with `--rawfile`, added a mocked cleanup regression test, and wired it into `validate-github-actions.yml`. Exact-head lint #41300193718 and manifest validation #41300193747 passed.
- Platform Infra PR #972 added a path-scoped master-push dry-run to the existing `vps-image-cleanup` workflow. Push and schedule are forced to `DRY_RUN=true`; only manual `workflow_dispatch` can set false. Weekly Sunday cron `30 3 * * 0`, manual inputs, production environment, runner labels, and concurrency are preserved. Exact-head lint #41300278177 and manifest validation #41300278090 passed.
- Platform Infra PR #973 aligned the cleanup script with the installed `platform-crictl` allowlist: call `ps`, `images`, and `rmi <full-sha256>` without forwarding low-level JSON flags. Exact-head lint #41300385289 and manifest validation #41300385307 passed.
- Post-merge validation at master `a760e94`: workflow lint #41300425015 and manifest validation #41300425064 succeeded.
- Live cleanup dry-run #41300425017 executed on the platform K3s runner with `DRY_RUN=true`. Prerequisites and CRI inventory passed, then the fail-closed reference check refused cleanup because several Pod refs were not resolvable to local CRI image IDs (including StockDividend old admin/backend tags and Docker Hub/Rancher system image refs). Exit 3; no deletion. Investigate CRI tag normalization before changing this safety guard.
- `recover-stale-ops.yml` is a new recovery controller with cron `10,25,40,55 * * * *`, but no run was observed in the latest 100 Actions runs through 11:08Z. Do not claim recovery dispatch occurred. Existing reconciliation/watchdog/inspection schedules remain preserved.
- TCE WF-06 cron `*/15 * * * *`, WF-12 monitoring, manual checks, and all TCE market-scan schedules remain unchanged. Latest WF-06 #41287060151 failed public checks because TCE/Auth are intentionally stopped; WF-12 push smoke #41291809063 passed.
- StockDividend app-owned CI and immutable publisher #41273202852/#41273202844 passed; Scraper/Admin/Backend ARM64 digests verified. Production promotion remains disabled. Weekend scraper #41284033242 remains in progress; preserve the purposeful scheduled/manual workflow.
- Media CI #41246414186 passed; latest full runtime snapshot #41275351280 showed Media and MicroFE workloads 1/1 with matching digest imageIDs. No fresh full inspection after cleanup smoke.
- Supabase SQL probe succeeded at 11:08:08Z. Auth CI/release evidence is historical; keep Auth PR #75/#76 open pending integration target/environment reconciliation. Preserve manual-only Auth release.
- No workflow removed. No duplicate direct SSH/Compose authority added. No production manifest, credential, database, release flag, or K3s desired replica changed.
## Latest workflow inventory review (2026-11-01 13:11 ICT; Auth smoke path correction merged)

- Current review baseline heads: platform-infra `2de34aa036752fd07e1b54479e47099e4e970460`; TCE Dashboard `48a8c86497f55b0454ea20fda0567d27f7b9718b`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media. Platform-infra PRs #955/#956/#957 merged.
- Platform-infra PR #957 aligns manual Auth smoke paths with application routing: `/api/health`, `/api/ready`, and unauthenticated `/auth/me` (401). Regression test added and included in the existing validation workflow. Exact-head checks #41279697716/#41279697827 and post-merge checks #41279747450/#41279747357 all succeeded.
- Platform-infra PR #956 exact-head #41279613899 and post-merge #41279710882 succeeded.
- TCE PR #1005 exact-head and post-merge WF-01/WF-02/WF-05 checks succeeded; scheduled WF-07 #41279469909 succeeded. WF-06 remains unscheduled since #41261234620 at 01:28:29Z despite WF-07 schedule delivery at 06:06:31Z. New four-lane matrix not yet exercised. WF-06 `*/15` schedule unchanged; TCE market-scan schedule untouched.
- Platform-infra reconciliation schedule remains stale: latest reconcile #41260761381 (01:21:35Z) failed; watchdog #41264226448 (02:12:35Z) failed; inspection #41264393955 queue delay 106m46s. Push smoke #41275653339 passed and reported workflow active, but no later scheduled reconcile/watchdog/inspection through 06:10Z.
- Supabase: project `gtqovpusfyyvxpeezxlo` ACTIVE_HEALTHY; SQL probes at 05:59:45Z and 06:10:49Z succeeded; branch FUNCTIONS_DEPLOYED; 84/84 migration-version parity. Auth PR #75 remains unmerged due conflicting production/non-production classification and unavailable authoritative integration target binding; PR #76 remains draft. Auth release manual-only.
- StockDividend publisher #41273202844 succeeded and verified immutable ARM64 images for Scraper/Admin/Backend; promotion false and dispatch skipped. Production still has old image references and failed admin/backend rollout.
- Media/MicroFE snapshot #41275351280 at 05:02:36Z: four workloads 1/1 and runtime imageIDs match pinned digests. TCE/Auth/Keycloak 0/0 by operator request.
- Preserve CI/test/security, backup, manual, release, and scheduled workflows. No workflow removed; no second direct SSH/Compose deployment authority added. Reconcile cron `7,22,37,52 * * * *`; watchdog `12,27,42,57 * * * *`; inspection `2,32 * * * *`.

## Latest workflow inventory review (2026-11-01 13:08 ICT; post-merge TCE and tracker checks verified)

- Current heads: platform-infra `de9099c88a3df05def9ab87ca09b987f90767ed0`; TCE Dashboard `48a8c86497f55b0454ea20fda0567d27f7b9718b`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media.
- Platform-infra PR #955 merged as `de9099c8`; exact-head manifest validation #41279439875 and post-merge manifest validation #41279478266 succeeded.
- TCE PR #1005 merged as `48a8c864`. WF-02/WF-05 exact-head checks #41279268677/#41279268735 passed; post-merge WF-01/WF-02/WF-05 #41279338739/#41279338863/#41279338766 all passed. Scheduled WF-07 integration check #41279469909 passed.
- TCE WF-06 now has four independent public matrix checks: TCE web, TCE API `/api/health`, Auth liveness, Auth readiness. `fail-fast: false`; preserve `workflow_dispatch`, read-only VPS diagnostics, and `*/15 * * * *` cron. No TCE market-scan schedule/workflow changed.
- WF-06 scheduled delivery remains unverified: latest WF-06 run #41261234620 at 01:28:29Z failed public checks (TCE/Auth 503); no later WF-06 scheduled run observed through 06:07Z, although WF-07 schedule fired at 06:06:31Z. The new matrix has not yet been exercised. Workflow enabled-state and workflow-dispatch actions are not exposed by the connected GitHub tool.
- Platform-infra schedule remains stale: reconcile #41260761381 failed 01:21:35Z; watchdog #41264226448 failed 02:12:35Z; inspection #41264393955 queue delay 106m46s. No newer scheduled reconcile/watchdog/inspection event through 06:07Z. Push smoke #41275653339 passed and reported reconcile-vps active.
- StockDividend publisher #41273202844 successfully published and verified Scraper/Admin/Backend immutable ARM64 images; promotion gate false and dispatch skipped. Production rollout remains blocked on old image references.
- Media/MicroFE latest runtime snapshot #41275351280 at 05:02:36Z: all four workloads 1/1 with imageIDs matching pinned digests. StockDividend admin 0/1, backend old replica plus new ImagePullBackOff; TCE/Auth/Keycloak 0/0 by operator request.
- Supabase project `gtqovpusfyyvxpeezxlo` ACTIVE_HEALTHY; SQL probe succeeded 05:59:45Z; branch state FUNCTIONS_DEPLOYED; 84/84 migration-version parity. Auth PR #75 changes docs/tests only and exact-head CI passed; keep unmerged pending production/non-production and GitHub integration target reconciliation. PR #76 remains draft. Auth release stays manual-only.
- Preserve all useful CI/test/security, backup, manual, release, and scheduled workflows. No workflow removed, no second direct SSH/Compose deployment authority added. Reconcile cron `7,22,37,52 * * * *`; watchdog `12,27,42,57 * * * *`; inspection `2,32 * * * *`.

## Latest workflow inventory review (2026-11-01 13:04 ICT; TCE public endpoint matrix merged)

- Current heads: platform-infra `33c19b8a73e0b77071b68b3987f8aef85c709aba`; TCE Dashboard `48a8c86497f55b0454ea20fda0567d27f7b9718b`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76 (draft)/#75; none in TCE, StockDividend, or Media.
- **TCE WF-06 healthcheck:** PR #1005 merged at `48a8c864`. Public endpoint matrix now reports TCE web, TCE API `/api/health`, Auth liveness, and Auth readiness as independent jobs; `fail-fast: false`. Cron remains `*/15 * * * *`; manual dispatch and read-only VPS diagnostics remain. WF-02 and WF-05 exact-head PR checks passed; post-merge WF-02 passed; post-merge WF-01/WF-05 were still running at last observation. No TCE market-scan schedule was modified.
- **TCE endpoint evidence:** latest scheduled WF-06 run #41261234620 (01:28:29Z) returned HTTP 503 for TCE web and both Auth endpoints; SSH/container diagnostics passed. The new TCE API lane has not yet been observed in a scheduled run.
- **Platform Infra workflows:** post-merge lint #41275653303, manifest validation #41275653306, and watchdog push smoke #41275653339 succeeded. The push smoke reported `reconcile-vps` active. Latest scheduled reconcile #41260761381 (01:21:35Z) failed; scheduled watchdog #41264226448 (02:12:35Z) failed; inspection #41264393955 was queued 106m46s before starting. No newer scheduled events observed through 05:58Z; schedule delivery remains unverified.
- **StockDividend publisher:** #41273202844 succeeded for source `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Scraper/Admin/Backend all published and their immutable ARM64 manifests verified. Promotion gate remained false, so handoff and dispatch were skipped. Production still references the old admin/backend tag; no rollout.
- **Media/MicroFE:** latest K3s snapshot #41275351280 (05:02:36Z) reported both Media workloads and both MicroFE workloads 1/1 with runtime imageIDs matching pinned digests.
- **Supabase/Auth safety:** project `gtqovpusfyyvxpeezxlo` ACTIVE_HEALTHY; SQL probe succeeded 05:59:45Z; Supabase reports 84 migration versions and Auth master has 84 matching version filenames; branch state FUNCTIONS_DEPLOYED. Auth PR #75 changes docs/tests only and exact-head CI #40446492086 passed; PR #76 remains draft and exact-head CI #40461047191 passed. Do not merge #75 until conflicting production/non-production classification and the GitHub integration's exact target binding are reconciled. Auth release remains manual-dispatch-only.
- Preserve existing CI, security, backup, manual, release, and scheduled workflows. No workflow was removed. No direct SSH/Compose deployment authority was added. Reconciliation cron remains `7,22,37,52 * * * *`; watchdog remains `12,27,42,57 * * * *`; inspection remains `2,32 * * * *`.


## Latest workflow inventory review (2026-11-01 12:07 ICT; runner queue telemetry added)

- Current heads: platform-infra `7fa8684d016154903a188fd11003d69a00545f80`; TCE Dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none observed in TCE, StockDividend, or Media.
- **Reconcile schedule/watchdog:** reconciliation cron remains `7,22,37,52 * * * *`; watchdog remains `12,27,42,57 * * * *`; inspection remains `2,32 * * * *`. PR #953 adds read-only queue-delay measurement: scheduled/manual/fallback watchdog runs fail if the latest scheduled reconcile waits over 15 minutes for a runner; push smoke emits warnings only; the latest scheduled inspection queue delay is reported as a warning. No cron or permission change.
- Queue evidence: scheduled inspect run #41264393955 waited 106m46s (created 02:15:04Z, started 04:01:50Z). Latest scheduled reconcile #41260761381 remains 01:21:35Z; latest scheduled watchdog #41264226448 remains 02:12:35Z. No newer schedule events observed through 05:07Z. The new watchdog will help distinguish queued-run pressure from missing schedule delivery.
- PR #953 merged as `7fa8684d016154903a188fd11003d69a00545f80`; exact-head lint [#41275616540](https://github.com/phanthienquoc/platform-infra/actions/runs/41275616540) and manifest validation [#41275616418](https://github.com/phanthienquoc/platform-infra/actions/runs/41275616418) passed. Post-merge lint/manifest/watchdog smoke were queued at review time.
- StockDividend publisher #41273202844 published and verified ARM64 full-SHA images: Scraper digest `69bbe0d160a80490fc92c73d77c9a657ffd853a29beb0972a615c10a710f4179`, Admin digest `cdf2e9328b17bcbabc118591d3c179709f51753047d400bb524bc18d2d39053c`, Backend digest `d188e5c4ae0bf4c882a560c0640a96f5497bc9623b863f1fea181dc6b3c974f3`. Promotion gate remained false; handoff/dispatch skipped. The Scraper has a separate weekend/manual GitHub-hosted workflow and no platform-infra workload manifest; preserve it.
- Latest K3s inspection #41275351280: Media and MicroFE are 1/1 with pod imageIDs matching pinned digests; StockDividend Admin and new Backend pods remain ImagePullBackOff on old `12d63b4`; old Backend/Frontend replicas remain on `23b2878`; TCE/Auth/Keycloak are intentionally 0/0.
- Supabase read-only SQL probe passed at 05:06:39Z; Media readiness REST window 05:02–05:07Z had 27 HTTP 200 / 0 HTTP 522; Postgres timeout/reset counts were zero. Continue monitoring; do not bypass readiness.
- Preserve application CI/build/security, StockDividend weekend/manual scraper, backup, inspection, reconciliation, watchdog, and release workflows. No direct SSH/Compose deployment authority added. TCE market-scan schedule unchanged.

## Latest workflow inventory review (2026-11-01 12:02 ICT; StockDividend publication and inspection merge guard evidence refreshed)

- Current heads: platform-infra `68aebdd7a68b6b79571243ae9a278fecc3262c32`; TCE Dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none in TCE Dashboard, StockDividend, or Media Generation. Platform Infra PR #950 is merged as `632b3041b220ed9cd3ffd370f29070699ea25877`; exact-head lint and manifest validation passed. Post-merge lint [#41275351341](https://github.com/phanthienquoc/platform-infra/actions/runs/41275351341), manifest [#41275351188](https://github.com/phanthienquoc/platform-infra/actions/runs/41275351188), and inspection [#41275351280](https://github.com/phanthienquoc/platform-infra/actions/runs/41275351280) all passed; automated snapshot PR #951 merged as `68aebdd7a68b6b79571243ae9a278fecc3262c32` after validation [#41275401751](https://github.com/phanthienquoc/platform-infra/actions/runs/41275401751).
- **StockDividend producer contract:** master push [publisher #41273202844](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202844) successfully built and published Scraper/Admin/Backend on native ARM64 and verified full-source-SHA tags against immutable SHA-256 registry digests. Digests: scraper `69bbe0d160a80490fc92c73d77c9a657ffd853a29beb0972a615c10a710f4179`, admin `cdf2e9328b17bcbabc118591d3c179709f51753047d400bb524bc18d2d39053c`, backend `d188e5c4ae0bf4c882a560c0640a96f5497bc9623b863f1fea181dc6b3c974f3`. The release gate was false; handoff and dispatch were skipped. This is artifact publication only, not production promotion.
- The paired StockDividend GitOps event currently carries Admin/Backend digests, matching the only two application workloads represented in `apps/stockdividend` manifests. The Scraper image is verified/published but no scraper workload manifest exists in the platform-infra tree. Preserve the app repository's separate `Run Scraper (Weekend Only)` schedule (Saturday/Sunday 01:00 UTC) and manual trigger; it runs as a GitHub-hosted data-collection job and is not a second VPS/Compose deploy authority.
- **Platform Infra operations:** PR #950 makes the inspection PR merge API handling idempotent and diagnosable. It captures HTTP status/body, re-reads PR state after rejection, accepts an already-merged result only if its head equals the exact validated SHA, and verifies the merged head/commit after HTTP 200. The previous inspection run #41264393955 waited 106m46s in the self-hosted queue and received HTTP 405 for a head that later changed before PR #940 was merged; exact cause remains unconfirmed. Track runner queue delay separately from schedule-event delivery.
- Reconciliation remains scheduled at minutes 7/22/37/52; watchdog at 12/27/42/57. Latest scheduled reconcile #41260761381 failed; latest scheduled watchdog #41264226448 failed freshness. Latest scheduled inspection #41264393955 was delayed in queue and its PR #940 ultimately merged at head `9c7d5aa959b3d1c4743cd6f00bfade72d2bb4acf`. Cadence is not yet proven stable.
- **Runtime:** latest inspection #41275351280 (snapshot generated 05:02:36Z; earlier digest verification #41271705613) confirms Media frontend/backend 1/1 and imageIDs matching pinned digests; MicroFE Shell/WS 1/1 and imageIDs matching pinned digests. StockDividend admin and new backend pods remain ImagePullBackOff on old non-ARM64 tag `12d63b4`; old backend/frontend replicas remain on `23b2878`. TCE/Auth/Keycloak remain intentionally at zero replicas.
- **Supabase:** read-only SQL probes succeeded at 04:58:12Z and 05:02:04Z; Media readiness REST logs show 0 HTTP 522 in two overlapping 30-minute windows through 05:02Z; Postgres timeout/reset events were zero in 04:32–05:02Z. Monitor further intervals; do not bypass readiness.
- Preserve CI, tests, security, backup, manual/release, maintenance, weekend scraper, and scheduled workflows. No duplicate direct SSH/Compose deployment authority added or removed. TCE market-scan schedule unchanged.

## Post-merge workflow inventory correction (2026-11-01 11:31 ICT)

- Platform Infra PR #948 merged as `ddc44cebcb2430b0da20fcbbdede1a78e7181407`; exact-head and post-merge manifest validation passed. PR #943 was closed as superseded, not merged.
- Current open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none known in TCE Dashboard, StockDividend, or Media Generation.
- StockDividend PR #21 merged. Post-merge CI [#41273202852](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202852) passed; publisher [#41273202844](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202844) is still building the ARM64 Scraper image. Promotion gate is false and Platform Infra handoff is skipped; no promotion dispatch is sent.
- Supabase SQL and Media readiness REST checks have returned successfully through 04:29:41Z; aggregate logs show 182 HTTP 200 and zero HTTP 522 in 04:00–04:30Z, with zero timeout-manager events. Continue observing before declaring stable.
- Latest scheduled reconcile remains #41260761381 (01:21:35Z), watchdog #41264226448 (02:12:35Z), inspection #41264393955 (02:15:04Z). No newer scheduled events were observed through 04:30Z; scheduled cadence is not proven.
- Keep `reconcile-vps.yml` as the sole GitOps apply authority, inspection read-only, watchdog read-only/fail-closed, and preserve CI/test/security/backup/maintenance/manual/release/scheduled jobs. TCE market-scan schedule unchanged.

## Latest workflow inventory review (2026-11-01 11:30 ICT; StockDividend publisher/promotion split and runtime evidence)

- Default-branch heads: platform-infra `29b5123ebcfaf6dddd42175a926914152b29627a`; TCE Dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- StockDividend PR #21 merged `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`. Master push publisher [#41273202844](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202844): master-ref check passed, promotion gate returned false, handoff validation skipped, and ARM64 `build-and-push` was in progress at 04:28Z. Post-merge CI [#41273202852](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202852) was in progress. Confirm final registry digests before any promotion.
- StockDividend publisher now owns native-ARM64 build, full-source-SHA tags, GHCR digest/architecture verification for scraper/admin/backend, and paired admin/backend outputs. `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED` gates only the separate GitOps promotion job. False means master pushes can publish immutable artifacts but cannot send `stockdividend-images-published`; explicit manual dispatch remains fail-closed. `PLATFORM_INFRA_TOKEN` is checked only in the promotion handoff job.
- Platform Infra PR #947 merged `29b5123ebcfaf6dddd42175a926914152b29627a`; image-change guard now recognizes container `image:` fields at all indentation levels and has an offline self-test. Exact-head lint/manifest checks [#41272561991](https://github.com/phanthienquoc/platform-infra/actions/runs/41272561991) / [#41272562071](https://github.com/phanthienquoc/platform-infra/actions/runs/41272562071) passed. Push-auto reconciliation [#41272596749](https://github.com/phanthienquoc/platform-infra/actions/runs/41272596749) passed shared reconciliation and MicroFE/Media/TCE/Auth lanes; StockDividend failed only on the existing `12d63b4` ARM64 ImagePullBackOff.
- Media PR #944 merged `ba1ae5ed0f566daec6b4b2e499a6c6d8d59a9722`, pinning the live frontend/backend digests. Inspection [#41271705613](https://github.com/phanthienquoc/platform-infra/actions/runs/41271705613) verifies Media and MicroFE pod imageIDs match the GitOps digests; Media and MicroFE workloads were Ready in that snapshot.
- Supabase project `gtqovpusfyyvxpeezxlo`: read-only SQL connectivity succeeded at 04:26:24Z; edge logs 04:00–04:26Z show 160 HTTP 200 and 0 HTTP 522 for `video_generation_jobs`; no Postgres timeout-manager events in that window. Treat as recovery sample, not sustained availability proof.
- Schedule offsets from PR #939 remain reconciliation `7,22,37,52`, watchdog `12,27,42,57`, inspection `2,32`. Latest observed scheduled reconcile remains #41260761381 (01:21:35Z, failure), watchdog #41264226448 (02:12:35Z, stale), inspection #41264393955 (02:15:04Z). No later scheduled reconciliation observed through 04:28Z; cadence not proven.
- `reconcile-vps.yml` is still the only production GitOps apply authority. `inspect-vps.yml` remains read-only; watchdog remains read-only and fails closed at 45 minutes. Runner policy v12 is installed; target-scoped restart helper restricts image-pull restarts to selected Deployment selectors. Preserve CI/test/security, backup, maintenance, manual/release, runner bootstrap, and scheduled workflows. No duplicate SSH/Compose deployment authority.
- TCE/Auth/Keycloak remain intentionally zero replicas. Their HTTP/OIDC 503 checks are expected maintenance-state evidence, not healthy service proof. TCE market-scan schedule unchanged.


## Latest workflow inventory review (2026-11-01 10:04 ICT; target-scoped image-pull recovery merged)

- Default-branch heads: platform-infra `055271db7bd37231fe95cbb337992659191895ce`; TCE Dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`; StockDividend `82b7bf6f3d122dec96e870991bac3e25ade64bb5`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open PRs remain platform-infra #795/#749/#741/#648/#544/#541/#539/#538 and Authentication #76/#75; no open PRs observed in TCE Dashboard, StockDividend, or Media Generation.
- **PR #937** merged as `055271db7bd37231fe95cbb337992659191895ce` from exact head `f83e71b480b280ae92ddec79568648ab07d59495`. Exact-head lint [#41267563432](https://github.com/phanthienquoc/platform-infra/actions/runs/41267563432), manifest validation [#41267563436](https://github.com/phanthienquoc/platform-infra/actions/runs/41267563436), and Keycloak CI [#41267563480](https://github.com/phanthienquoc/platform-infra/actions/runs/41267563480) passed. Post-merge lint [#41267595185](https://github.com/phanthienquoc/platform-infra/actions/runs/41267595185), manifest validation [#41267595312](https://github.com/phanthienquoc/platform-infra/actions/runs/41267595312), and Keycloak CI [#41267595223](https://github.com/phanthienquoc/platform-infra/actions/runs/41267595223) passed.
- `reconcile-vps.yml` now passes `TARGET_APP` to `platform-kubectl restart-blocked-image-pulls`. The v12 runner helper maps each app to fixed Deployments, derives the selected pods from that Deployment's selector, and restarts only the Deployment with `ImagePullBackOff` / `ErrImagePull`. The `all` mapping is reserved for all-app/cluster-wide scope. It no longer restarts unrelated StockDividend workloads during a MicroFE promotion or unrelated MicroFE workloads during a StockDividend promotion.
- Runner policy `rollout-status-v12-scoped-image-pull-restart` is required before any production apply. `provision-auth-runtime-secret.yml` accepts v12. The existing `bootstrap-runner.yml` push path for `scripts/bootstrap-runner.sh` installed the policy automatically: [bootstrap #41267595241](https://github.com/phanthienquoc/platform-infra/actions/runs/41267595241) succeeded, confirmed policy v12 on `platform-k3s-01`, re-bootstrapped the Media runner, and passed final runner/reconciliation capability verification. Keep `bootstrap-runner.yml` as the single platform runner-helper installation authority.
- Scheduled reconciliation is still stale: latest observed scheduled reconcile [#41260761381](https://github.com/phanthienquoc/platform-infra/actions/runs/41260761381) at 01:21:35Z failed; watchdog [#41264226448](https://github.com/phanthienquoc/platform-infra/actions/runs/41264226448) at 02:12:35Z failed at 51 minutes; inspection [#41264393955](https://github.com/phanthienquoc/platform-infra/actions/runs/41264393955) at 02:15:04Z succeeded. No scheduled reconcile after v12 installation is yet observed; cadence remains unproven.
- K3s snapshot [`debug/vps-latest.md`](https://github.com/phanthienquoc/platform-infra/blob/055271db7bd37231fe95cbb337992659191895ce/debug/vps-latest.md) at 02:15:17Z: node Ready/ARM64, disk 54%, GitOps drift clean; MicroFE Shell/WS 1/1; StockDividend admin and new backend pod ImagePullBackOff on `12d63b4` without ARM64 manifest; Media backend 0/1 (two pods), frontend 1/1; TCE/Auth/Keycloak 0/0 by intent. CRI image inventory was unavailable because sudo required a password.
- Supabase project remains control-plane `ACTIVE_HEALTHY`, but read-only SQL timed out. Unified logs show 774 HTTP 522 events for Media's `video_generation_jobs` REST probe in 02:00–03:04Z, plus 7 Postgres statement timeouts and 3 client resets. Root cause is not established. Keep Media readiness fail-closed; do not change schema or secrets.
- App repositories continue to own tests/builds and immutable ARM64 GHCR publication. Platform Infra owns shared pull credentials, digest validation/pinning, GitOps promotion/reconciliation, rollout and health. StockDividend remains on release hold; Media has no new paired digest dispatch; no production image publication or application dispatch occurred in this review.
- Preserve CI, tests, security, manual/release, backup, maintenance, runner bootstrap and scheduled workflows. No duplicate direct SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Latest workflow inventory review (2026-11-01; PAT-free promotion and reconcile-triggered watchdog merged)

- Default-branch heads reviewed: platform-infra `81d5a191abeec71945eeb040d8e24a7d9dc9152f`, TCE Dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`, StockDividend `82b7bf6f3d122dec96e870991bac3e25ade64bb5`, Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`, Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Remaining open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none observed in TCE Dashboard, StockDividend or Media Generation.
- **GitOps promotion inventory:** `gitops-image-promotion.yml` now uses workflow-scoped `GITHUB_TOKEN` rather than a separate automation PAT. The MicroFE and shared application promotion jobs alone receive `actions: write`; both explicitly dispatch `validate-manifests.yml` on the exact promotion branch, correlate by exact head SHA/branch/event/creation time, require success, recheck PR state/head/base, and merge with the exact-head guard. GHCR remains a separate read-only credential. PR #927 exact-head checks [#41250669100](https://github.com/phanthienquoc/platform-infra/actions/runs/41250669100) and [#41250669015](https://github.com/phanthienquoc/platform-infra/actions/runs/41250669015) passed; merge commit `e6577e394cd72862ffd3adbccbd5ef68aece5a9b`. Its post-merge manifest check [#41250722586](https://github.com/phanthienquoc/platform-infra/actions/runs/41250722586) passed; post-merge lint [#41250722648](https://github.com/phanthienquoc/platform-infra/actions/runs/41250722648) remained in progress at last query.
- **Schedule watchdog inventory:** `reconcile-schedule-watchdog.yml` retains its */15 cron and 45-minute threshold, and now listens for completed scheduled runs of both `inspect-vps` and `reconcile-vps`. Its event guard ignores non-scheduled workflow_run completions. PR #929 exact-head lint [#41250924240](https://github.com/phanthienquoc/platform-infra/actions/runs/41250924240) and manifest validation [#41250924314](https://github.com/phanthienquoc/platform-infra/actions/runs/41250924314) passed; merge commit `81d5a191abeec71945eeb040d8e24a7d9dc9152f`. Post-merge lint [#41251001565](https://github.com/phanthienquoc/platform-infra/actions/runs/41251001565), manifest validation [#41251001567](https://github.com/phanthienquoc/platform-infra/actions/runs/41251001567), and push-mode API smoke [#41251001532](https://github.com/phanthienquoc/platform-infra/actions/runs/41251001532) passed. Push smoke is diagnostic only; no post-merge scheduled reconciliation has yet exercised the new fallback.
- Scheduled watchdog [#41251234237](https://github.com/phanthienquoc/platform-infra/actions/runs/41251234237) subsequently failed at 23:08Z because the latest scheduled reconcile was 51 minutes old (>45-minute threshold), confirming the cadence gap. The new workflow_run fallback after `reconcile-vps` has not yet been exercised because no later scheduled reconciliation completed.
- **Reconciliation and inspection:** scheduled reconcile [#41247425890](https://github.com/phanthienquoc/platform-infra/actions/runs/41247425890) at 22:16Z failed at MicroFE, Media and StockDividend health lanes after shared reconciliation passed. Scheduled inspection [#41248478496](https://github.com/phanthienquoc/platform-infra/actions/runs/41248478496) at 22:30Z succeeded; exact-head validation [#41248536823](https://github.com/phanthienquoc/platform-infra/actions/runs/41248536823) passed; watchdog fallback [#41248580344](https://github.com/phanthienquoc/platform-infra/actions/runs/41248580344) at 22:31Z passed freshness. No consecutive 15-minute intervals prove stable cadence.
- **Runtime evidence:** the 22:30Z `debug/vps-latest.md` snapshot reports ARM64 K3s node Ready, disk 55%/normal, and GitOps drift clean. MicroFE Shell/WS fail pulls on `0.1.0`/`RELEASE_SHA`; StockDividend admin/backend fail ARM64 manifest selection on `12d63b4`; Media backend is Running but 0/1 ready with `ProgressDeadlineExceeded`. The Media `/ready` route queries Supabase `video_generation_jobs`; exact DB error remains unobserved. TCE and Auth workloads remain scaled to zero.
- **Supabase dependency evidence:** the project management status is `ACTIVE_HEALTHY`, but 56/56 REST calls for `video_generation_jobs` returned HTTP 522 over 22:50–22:55Z, followed by 70 more HTTP 522 responses over 23:00–23:08Z; Postgres logged seven statement timeouts in the preceding hour, and read-only SQL/advisor calls timed out. The Media `/ready` route therefore fails on its Supabase query. Root cause remains unconfirmed; do not bypass readiness or change schema/secrets to hide the data-plane outage.
- **Application CI/release evidence:** TCE healthcheck [#41249248285](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41249248285) failed with expected HTTP 503 while TCE/Auth are stopped; backup/integration [#41245102655](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41245102655), [#41244335183](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41244335183) passed. StockDividend CI [#41237638245](https://github.com/phanthienquoc/stockdividend/actions/runs/41237638245) passed, but publisher [#41237638206](https://github.com/phanthienquoc/stockdividend/actions/runs/41237638206) skipped handoff/build-push under release hold. Media CI [#41246414186](https://github.com/phanthienquoc/media-generation/actions/runs/41246414186) passed with no release dispatch. Auth CI/release [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844), [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) are historical success, not runtime health.
- App repositories continue to own tests/builds, immutable full-SHA GHCR publication, ARM64 verification and dispatch payloads. Platform Infra owns GHCR pull access, atomic digest pinning, GitOps PR validation/merge, reconciliation, rollout and health gates. No duplicate direct SSH/Compose deployment authority was added.
- Preserve useful CI, tests, security, backup, manual, release, maintenance and scheduled workflows. No workflow was removed. The unrelated mirror workflow [#41248213489](https://github.com/phanthienquoc/platform-infra/actions/runs/41248213489) failed but was preserved.
- Application dispatch token presence remains unverified; no values were read or changed. No new image publication, repository dispatch, GitOps promotion or K3s rollout was observed. TCE remains scale-to-zero; Auth/Keycloak remain stopped; market-scan schedule unchanged. Production remains **NOT HEALTHY/UNVERIFIED**.
- Next actions: replay the previously validated MicroFE digest pair once a write-capable dispatch action is available; investigate the Media Supabase readiness query; keep StockDividend release hold until explicit authorization and ARM64 images are verified; observe a scheduled reconciliation to confirm the new watchdog fallback.

## Latest workflow inventory review (2026-11-01 05:00 ICT; Media dispatch verification merged)

- Default-branch heads rechecked: platform-infra `db57cb6b81b7c07afb975cc6e29cd37403062832`, TCE-dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`, StockDividend `82b7bf6f3d122dec96e870991bac3e25ade64bb5`, Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`, Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open PRs: platform-infra #795/#749/#741/#648 and #544/#541/#539/#538; Authentication #76/#75. None observed in TCE-dashboard, StockDividend or Media Generation.
- Media PR [#66](https://github.com/phanthienquoc/media-generation/pull/66) was squash-merged as `d8e695d772ab2dc0da5c15cc428ee78ac6537518` from exact head `5f8016d6679aa84bb16968fc4614e78817da6c43`. It changes only `.github/workflows/wf-03-media-production-deploy.yml` and `scripts/validate-media-release-contract.mjs`, replacing the name-only workflow lookup with an exact `display_title` match for `media-generation / <release-tag>`. Media CI [#41246292632](https://github.com/phanthienquoc/media-generation/actions/runs/41246292632) completed successfully on that exact head. This prevents a concurrent unrelated GitOps run from falsely satisfying the Media dispatch verification; no release was dispatched by this PR.
- Latest recorded scheduled reconciliation is [#41231064067](https://github.com/phanthienquoc/platform-infra/actions/runs/41231064067), at 01:46:51 ICT, conclusion failure. Shared reconciliation passed; MicroFE, StockDividend and Media health lanes failed; Keycloak was skipped. No newer scheduled run was independently verified because the connected run-list wrapper only returns PR-triggered runs. Keep 15-minute schedule status unverified until consecutive schedule/watchdog evidence is available.
- Release contracts: StockDividend and Media publishers emit one paired digest event only after full-SHA publication, registry digest resolution and ARM64 verification; Platform Infra validates paired digest references and updates both production image entries atomically. No actual new image publication, repository dispatch, GitOps promotion or K3s rollout was observed in this pass.
- Known blockers remain missing MicroFE `0.1.0` / `RELEASE_SHA` images, StockDividend `12d63b4` ARM64 incompatibility, previously unready Media backend `prod-v0.3.0-58f80a8`, and unverified protected GitOps/dispatch tokens. StockDividend production release remains disabled pending explicit authorization and prerequisites.
- Preserve useful CI, tests, security, manual, release, backup, maintenance and scheduled workflows. No duplicate SSH/Compose deployment authority was added or removed. TCE remains intentionally scale-to-zero; Auth/Keycloak remain stopped. No production configuration was changed and the TCE market-scan schedule is unchanged.

## Latest workflow inventory review (2026-11-01 03:15 ICT; atomic StockDividend digest handoff merged)

- Re-inspected all five default branches, open PRs, the deployment tracker/inventory, and the latest PR-triggered Actions evidence available in this pass. Observed heads: platform-infra `b3c801ba3c5017e6a7c08ebab033ed8c22d36488`, TCE-dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`, StockDividend `82b7bf6f3d122dec96e870991bac3e25ade64bb5`, Media Generation `12372380849348eb3ed88cb8af3d8e7a6ccc2e23`, Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open PRs remain platform-infra #795/#749/#741/#648 and draft Keycloak PRs #544/#541/#539/#538; Authentication #76/#75. No open PRs are currently observed in TCE-dashboard, StockDividend, or Media Generation.
- **Platform Infra PR #919 merged** as `c38559ed0b85da7fac00b1a2e3537b6f3bfc7a89` from exact head `dfe604e8a06aca220939a9958f08b4e3ddde331f`. Exact-head `validate-manifests` [#41237427173](https://github.com/phanthienquoc/platform-infra/actions/runs/41237427173) and `validate-github-actions` [#41237427238](https://github.com/phanthienquoc/platform-infra/actions/runs/41237427238) both passed.
- **StockDividend PR #20 merged** as `82b7bf6f3d122dec96e870991bac3e25ade64bb5` from exact head `e5f472214bb679ce869967a1d8f4611f03770720`. Exact-head CI [#41237443765](https://github.com/phanthienquoc/stockdividend/actions/runs/41237443765) completed successfully with all five jobs passing: backend test/build, admin production build, scraper syntax, scraper container build, and release-hold contract.
- Both repositories now contain the paired digest handoff contract. The StockDividend publisher captures verified ARM64 backend/admin registry digests and sends one `stockdividend-images-published` event with the full source commit and both digests. Platform Infra validates both exact GHCR digest references and pins both production image entries to digests in one GitOps PR. **End-to-end dispatch and promotion have not yet been verified.**
- PR #20 changed the release-contract script as well as the publisher workflow. The master push may therefore start the StockDividend publisher workflow; the last verified publisher run [#41232557169](https://github.com/phanthienquoc/stockdividend/actions/runs/41232557169) neutral-skipped build/publish while the production release gate was disabled. The post-merge publisher result for commit `82b7bf6` was not available through the current run evidence, so do not claim that the post-merge run skipped or published until its actual job result is inspected. No live release was intentionally dispatched by this automation.
- Latest recorded scheduled reconciliation remains [#41231064067](https://github.com/phanthienquoc/platform-infra/actions/runs/41231064067), created at 01:46:51 ICT on 2026-11-01, with failed MicroFE, StockDividend, and Media health lanes. No newer schedule run was verifiable in this pass; stable 15-minute cadence is not proven. Runtime blockers remain MicroFE missing `0.1.0`/`RELEASE_SHA` tags, StockDividend legacy `12d63b4` ARM64 incompatibility, and unready Media backend `prod-v0.3.0-58f80a8`.
- Protected `PLATFORM_INFRA_AUTOMATION_TOKEN` and StockDividend `PLATFORM_INFRA_TOKEN` remain unresolved/unverified. Do not substitute `GHCR_READ_TOKEN`. Keep StockDividend release disabled until token access and image-readiness prerequisites are confirmed.
- TCE public healthcheck has historical HTTP 503 evidence while TCE remains intentionally scale-to-zero; Auth/Keycloak remain stopped. No credentials, release flags, production manifests, database objects, or K3s workloads were changed. Production remains **NOT HEALTHY/UNVERIFIED**. Do not alter the TCE market-scan schedule.
- Next actions: inspect the post-merge StockDividend publisher run on master and confirm the release gate's actual result; then, only when production release is explicitly authorized and credentials are ready, verify one real paired dispatch, atomic GitOps PR, exact-head checks, K3s rollout, and health gates. Re-check consecutive scheduled reconcile/watchdog events before calling the schedule stable.

## Post-merge workflow inventory evidence (2026-11-01 02:06 ICT; StockDividend ARM64 verification merged)

- **Platform tracker refresh PR [#917](https://github.com/phanthienquoc/platform-infra/pull/917) merged** as `458057caff635da9c45e4ffce00d73d50e20026f` from exact head `831236a06512d85285c2927e28c76593eb45c9cc`. Exact-head `validate` passed in [#41232240907](https://github.com/phanthienquoc/platform-infra/actions/runs/41232240907); post-merge `validate-manifests` passed in [#41232284570](https://github.com/phanthienquoc/platform-infra/actions/runs/41232284570). This was documentation-only.
- **StockDividend PR [#19](https://github.com/phanthienquoc/stockdividend/pull/19) merged** as `28efc5ef7065a71dfa5ebb6bb1304d2b2140a67e` from exact head `42ab2ba95352bac3fa0a8e2dcbcaf3c525f45eee`. Exact-head CI [#41232391200](https://github.com/phanthienquoc/stockdividend/actions/runs/41232391200) passed all five jobs: backend test/build, admin build, scraper syntax, scraper image build, and production release contract.
- StockDividend publisher post-merge [#41232557169](https://github.com/phanthienquoc/stockdividend/actions/runs/41232557169) succeeded, but `Validate Platform Infra release handoff before publishing` and `build-and-push` were skipped because production release remains disabled. No images or GitOps dispatch were produced. Post-merge StockDividend CI [#41232557097](https://github.com/phanthienquoc/stockdividend/actions/runs/41232557097) also passed.
- The StockDividend publisher now verifies each full-source-SHA tag resolves to a registry digest and that the published `scraper`, `admin`, and `backend` image manifests advertise `linux/arm64` before it sends any GitOps dispatch. Contract tests enforce that this verification runs after all image pushes and before dispatch. This prevents a repeat of the current `12d63b4` ARM64 mismatch for future releases; it does not repair the already-published production tag.
- Latest scheduled reconciliation still observed: [#41231064067](https://github.com/phanthienquoc/platform-infra/actions/runs/41231064067), created 01:46:51 ICT, event `schedule`, conclusion `failure` from MicroFE, StockDividend, and Media health lanes. It is one fresh schedule event after the earlier gap, but no later scheduled reconciliation or watchdog run was visible in the latest run history at this review. Schedule cadence is therefore **not yet proven stable**.
- The prior watchdog [#41230260250](https://github.com/phanthienquoc/platform-infra/actions/runs/41230260250) at 01:36 ICT correctly failed because the newest scheduled reconciliation then was 235 minutes old. Its query path worked; the alert was about stale schedule evidence, not an API 404.
- Runtime blockers remain: MicroFE uses missing `0.1.0` / `RELEASE_SHA` tags; Media backend `prod-v0.3.0-58f80a8` is not ready; StockDividend production manifest still points to `12d63b4`, whose admin/backend image manifests do not support the ARM64 node. Protected `PLATFORM_INFRA_AUTOMATION_TOKEN` and StockDividend `PLATFORM_INFRA_TOKEN` are still required before promotion; no recent live handoff demonstrates those prerequisites are configured.
- TCE healthcheck [#41212968442](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41212968442) still failed while integration [#41201516226](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41201516226) passed. Media CI [#41158810606](https://github.com/phanthienquoc/media-generation/actions/runs/41158810606) and Auth CI/release [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844), [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) are successful historical CI evidence, not proof of current runtime health.
- No production manifests, credentials, release flags, or K3s workloads changed. TCE remains intentionally scale-to-zero and Auth/Keycloak remain stopped. **Overall production remains NOT HEALTHY/UNVERIFIED.**
- Next actions: confirm consecutive scheduled reconcile/watchdog events; keep StockDividend release hold in place until tokens are configured; publish full-source-SHA ARM64 images, verify registry digest/platform output and actual dispatch payload, then allow GitOps promotion and verify K3s rollout plus health gates. Do not alter the TCE market-scan schedule.

## Latest workflow inventory review (2026-11-01 02:00 ICT; reconciliation schedule resumed, health gates still failing)

- Re-inspected default-branch heads, open PRs, latest Actions runs, tracker, inventory, and watchdog/reconciliation contracts. Observed heads: platform-infra `4c22f9739cee5a98a7793449188b7841bbecf12f`, TCE-dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`, StockDividend `a1ae52369859d9b72cc823621024bb408d72c168`, Media Generation `12372380849348eb3ed88cb8af3d8e7a6ccc2e23`, Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- **Scheduled reconciliation event delivery has resumed at least once after the observed gap:** [Reconcile VPS #41231064067](https://github.com/phanthienquoc/platform-infra/actions/runs/41231064067) was created at 2026-10-31 18:46:51Z (2026-11-01 01:46:51 ICT), event `schedule`. It completed with `failure`; this is evidence of a fresh scheduled event, not a healthy deployment or proof that cadence is stable.
- The preceding watchdog run [#41230260250](https://github.com/phanthienquoc/platform-infra/actions/runs/41230260250), at 01:36 ICT, correctly failed the 45-minute freshness gate: latest scheduled reconciliation at that time was [#41211251969](https://github.com/phanthienquoc/platform-infra/actions/runs/41211251969), created 21:40 ICT on 2026-10-31, age 235 minutes, conclusion `failure`. The watchdog API request itself reached GitHub and returned history; this was a genuine stale-run alert, not the earlier HTTP 404 defect.
- [Scheduled inspection #41230154807](https://github.com/phanthienquoc/platform-infra/actions/runs/41230154807) succeeded at 01:35 ICT. [Observability reconcile #41231206347](https://github.com/phanthienquoc/platform-infra/actions/runs/41231206347) succeeded at 01:48 ICT. The next scheduled watchdog run after reconciliation #41231064067 had not appeared in the latest run list at review time; confirm it on the next observation and verify multiple consecutive cron intervals before declaring schedule delivery stable.
- Latest reconciliation #41231064067 had a successful shared reconcile but failed final deployment health lanes:
  - MicroFE Shell/WS: `ImagePullBackOff` for missing `microfe-shell:0.1.0` and `microfe-ws:RELEASE_SHA` tags.
  - StockDividend admin/backend: tag `12d63b4` reports `no match for platform in manifest` on the ARM64 K3s node; stock frontend reported desired=1, ready=1, updated=0.
  - Media backend: `prod-v0.3.0-58f80a8` container not ready; deployment reported `ProgressDeadlineExceeded` with image digest `sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d`.
  - TCE and Auth lanes reported success in that workflow, but this does not override the separately observed TCE HTTP 503 healthcheck or prove Auth/SSO is serving traffic. Keycloak lane was skipped.
- Current app workflow evidence is unchanged: TCE healthcheck [#41212968442](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41212968442) failed while integration [#41201516226](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41201516226) passed; StockDividend CI [#41203909024](https://github.com/phanthienquoc/stockdividend/actions/runs/41203909024) passed but publisher [#41203908963](https://github.com/phanthienquoc/stockdividend/actions/runs/41203908963) skipped build/publish under the release hold; Media CI [#41158810606](https://github.com/phanthienquoc/media-generation/actions/runs/41158810606) and Auth CI/release [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844), [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) passed on inspected commits, not runtime evidence.
- Open PRs: platform-infra #795, #749, #741, #648, #544, #541, #539, #538; Authentication #76 and #75. No open PRs observed in TCE-dashboard, StockDividend, or Media Generation. These are existing unrelated/stale workstreams; none was merged by this run.
- Protected GitOps handoff dependencies remain unverified/unresolved: `PLATFORM_INFRA_AUTOMATION_TOKEN` for platform-infra PR creation and `PLATFORM_INFRA_TOKEN` for StockDividend handoff. Do not substitute `GHCR_READ_TOKEN`. No new immutable image publication or GitOps dispatch was observed.
- No credentials, release flags, production manifests, or K3s workloads changed. TCE remains intentionally scale-to-zero; Auth/Keycloak remain stopped. **Overall production remains NOT HEALTHY/UNVERIFIED.**
- Next actions: confirm the next watchdog run sees the fresh scheduled reconciliation and observe consecutive cadence; keep production release holds until the distinct tokens and ARM64-compatible full-source-SHA images are verified; then promote through GitOps and verify K3s rollout plus health gates. Do not alter the TCE market-scan schedule.

## Latest automation review (2026-11-01 01:02 ICT; watchdog API smoke and tracker verified)

- PR [#913](https://github.com/phanthienquoc/platform-infra/pull/913) is merged at `8374728b4c4f07d26d0376869a654d9b4a956563`. Exact-head lint/validation passed on `89ca75d9897650236727e1cead1ec7d138f072c2`; post-merge validation passed in [#41227209930](https://github.com/phanthienquoc/platform-infra/actions/runs/41227209930) and [#41227209850](https://github.com/phanthienquoc/platform-infra/actions/runs/41227209850).
- Tracker/inventory refresh PR [#914](https://github.com/phanthienquoc/platform-infra/pull/914) merged at `4fb254de5819b3683543712f72aedafb7d9ee29f`; exact-head validation [#41227343221](https://github.com/phanthienquoc/platform-infra/actions/runs/41227343221) and post-merge validation [#41227381769](https://github.com/phanthienquoc/platform-infra/actions/runs/41227381769) passed.
- Post-merge read-only API smoke [#41227210009](https://github.com/phanthienquoc/platform-infra/actions/runs/41227210009) succeeded. The log confirms the API query returned the latest scheduled reconciliation [#41211251969](https://github.com/phanthienquoc/platform-infra/actions/runs/41211251969), created at 21:40 ICT on 2026-10-31, age 199 minutes at smoke time, conclusion failure. The API-path blocker is resolved; scheduled-event delivery and runtime health are not.
- No newer scheduled inspection than [#41216706436](https://github.com/phanthienquoc/platform-infra/actions/runs/41216706436) (22:49 ICT, success) and no newer scheduled reconciliation were visible after the watchdog fix. Next action: inspect Actions workflow enablement/event delivery and manually dispatch the read-only watchdog; preserve existing cron cadence.
- Current app evidence: TCE healthcheck [#41212968442](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41212968442) failed while integration [#41201516226](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41201516226) passed; StockDividend CI [#41203909024](https://github.com/phanthienquoc/stockdividend/actions/runs/41203909024) passed but publisher [#41203908963](https://github.com/phanthienquoc/stockdividend/actions/runs/41203908963) skipped image publication under the release hold; Media CI [#41158810606](https://github.com/phanthienquoc/media-generation/actions/runs/41158810606) and Auth CI/release [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844), [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) passed on inspected commits but do not prove runtime health.
- Open PRs after #913 merged: platform-infra #795/#749/#741/#648 and Keycloak #544/#541/#539/#538; Authentication #75/#76; none observed in TCE-dashboard, StockDividend, or Media Generation. No unrelated PR was merged.
- Runtime blockers: missing MicroFE `0.1.0` / `RELEASE_SHA` tags; unready Media backend on `prod-v0.3.0-58f80a8`; StockDividend `12d63b4` images lack ARM64-compatible manifests; protected `PLATFORM_INFRA_AUTOMATION_TOKEN` and StockDividend `PLATFORM_INFRA_TOKEN` still required. TCE and Auth/Keycloak remain stopped as requested.
- No production manifests, credentials, release flags, or K3s workloads changed. Preserve app CI/image publishing, platform-owned GitOps, useful manual/release/security/scheduled workflows, and the TCE market-scan schedule. Production remains **NOT HEALTHY/UNVERIFIED**.

## Latest automation review (2026-10-31 23:59 ICT; watchdog API fix merged)

- Watchdog PR [#911](https://github.com/phanthienquoc/platform-infra/pull/911) is merged as `32d9000ae28bbbd2767f609f016b9c4cda941ae7`; exact-head validation and lint plus post-merge validation/lint all passed. The runtime failure [#41217883661](https://github.com/phanthienquoc/platform-infra/actions/runs/41217883661) was caused by a leading-slash `gh api` endpoint and omitted explicit GET with query fields. The workflow now uses a relative endpoint and `-X GET`; contract tests guard both requirements.
- Post-fix runtime is pending: no watchdog run after merge yet. Latest scheduled reconcile remains [#41211251969](https://github.com/phanthienquoc/platform-infra/actions/runs/41211251969) at 21:40 ICT; shared reconcile passed, but MicroFE, Media, and StockDividend health lanes failed. Confirm the next watchdog can query workflow run history before claiming the monitoring path is healthy.
- Current app evidence: TCE healthcheck [#41212968442](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41212968442) failed while integration check [#41201516226](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41201516226) passed; StockDividend CI [#41203909024](https://github.com/phanthienquoc/stockdividend/actions/runs/41203909024) passed but publisher [#41203908963](https://github.com/phanthienquoc/stockdividend/actions/runs/41203908963) skipped image publication under the production release hold; Media CI [#41158810606](https://github.com/phanthienquoc/media-generation/actions/runs/41158810606) and Auth CI/release [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844), [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) passed on inspected commits but do not establish runtime health.
- Keep credential boundaries distinct: `GHCR_READ_TOKEN` is registry read-only; `PLATFORM_INFRA_AUTOMATION_TOKEN` is for platform-infra GitOps PR/check/merge operations; `PLATFORM_INFRA_TOKEN` is a separate StockDividend/TCE release handoff. Missing secret values cannot be read through the connector and must be configured in protected Environments.
- Preserve app-repo CI and immutable image publishing, platform-infra GitOps reconciliation and health gates, useful security/manual/release/scheduled jobs, and the current TCE market-scan schedule. No production manifests, secrets, release flags, or K3s workloads changed. Production remains **NOT HEALTHY/UNVERIFIED**.

## Latest automation review (2026-10-31 23:02 ICT; PR #909 merged)

- PR [#909](https://github.com/phanthienquoc/platform-infra/pull/909) merged as `ec39d92e551abe123cec42f6b19ab66581f553a8`. Exact-head checks [#41217663279](https://github.com/phanthienquoc/platform-infra/actions/runs/41217663279) and [#41217663215](https://github.com/phanthienquoc/platform-infra/actions/runs/41217663215) passed; post-merge manifest/workflow validation [#41217711178](https://github.com/phanthienquoc/platform-infra/actions/runs/41217711178) and [#41217711107](https://github.com/phanthienquoc/platform-infra/actions/runs/41217711107) passed.
- `reconcile-schedule-watchdog.yml` retains cron/manual entry points and now has a read-only `workflow_run` fallback for completed scheduled `inspect-vps` runs. It does not run for manually triggered inspection. Runtime confirmation is pending until the next scheduled `inspect-vps` completion after merge; no watchdog run is currently visible.
- Scheduled `reconcile-vps.yml` remains stale: latest observed schedule is [#41211251969](https://github.com/phanthienquoc/platform-infra/actions/runs/41211251969) at 21:40 ICT, with shared reconcile success and aggregate health failure. Latest scheduled `inspect-vps` [#41216706436](https://github.com/phanthienquoc/platform-infra/actions/runs/41216706436) passed at 22:49 ICT; snapshot validation [#41216764068](https://github.com/phanthienquoc/platform-infra/actions/runs/41216764068) passed.
- Production image readiness remains blocked: MicroFE uses missing `0.1.0` / `RELEASE_SHA` tags; Media backend is unready on `prod-v0.3.0-58f80a8`; StockDividend `12d63b4` admin/backend images lack ARM64 manifests. StockDividend publisher is correctly held and skipped image publication.
- TCE scheduled healthcheck [#41212968442](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41212968442) failed; integration check [#41201516226](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41201516226) passed. Media CI and Auth CI/release passed on the listed runs, but those results are not production health evidence.
- Keep credential boundaries: `GHCR_READ_TOKEN` is read-only registry auth; `PLATFORM_INFRA_AUTOMATION_TOKEN` grants platform-infra GitOps PR/write/check operations; `PLATFORM_INFRA_TOKEN` is StockDividend/TCE release handoff; `PLATFORM_INFRA_DISPATCH_TOKEN` is Media/Auth handoff. Missing secrets cannot be verified by reading secret values through the connector; they must be configured in protected Environments.
- Preserve CI, security, manual/release and scheduled workflows. No duplicate SSH/Compose authority was added; no credential, release flag, production manifest, or K3s workload changed. Do not alter the TCE market-scan schedule. Overall production remains **NOT HEALTHY/UNVERIFIED**.
## Latest automation review (2026-10-31; after PR #904 merge)

- Platform Infra PR #904 is merged as `fcc1e1204db4d34f5ccd20e73836a6c3fe66d8a7`. Exact-head lint/validation and both post-merge checks passed.
- StockDividend GitOps promotion now accepts only a full 40-character source SHA for StockDividend image tags; short SHA inputs fail closed. Producer dispatch remains same-job and only covers `backend` and `admin`, the components declared in the current production Kustomize overlay.
- App repositories remain release producers; platform-infra remains the sole owner of production manifests, shared pull credentials, GitOps promotion/reconciliation and rollout health gates. Do not enable StockDividend production publishing merely to test the handoff.
- Current blockers: protected `PLATFORM_INFRA_AUTOMATION_TOKEN` for MicroFE/Media; `PLATFORM_INFRA_TOKEN` and explicit release enablement for StockDividend; StockDividend production manifest tags have not been promoted from `12d63b4`. TCE remains intentionally at zero replicas and Auth/Keycloak remain stopped.
- Production is **NOT HEALTHY/UNVERIFIED**. Schedule watchdog runtime and scheduled-event delivery remain unverified. Preserve all useful CI/security/manual/release workflows and the TCE market-scan schedule.

## Post-merge verification (2026-10-31)

- Tracker/inventory PR #901 was squash-merged as `3f1aa97b9086cc2dd77f3002bba883afe37a916d`; post-merge manifest validation [#41204039425](https://github.com/phanthienquoc/platform-infra/actions/runs/41204039425) passed.
- StockDividend master CI [#41203909024](https://github.com/phanthienquoc/stockdividend/actions/runs/41203909024) completed successfully on merge commit `a1ae52369859d9b72cc823621024bb408d72c168`; backend build, scraper container build, scraper syntax, admin production build, and release-hold contract all passed.
- Publisher [#41203908963](https://github.com/phanthienquoc/stockdividend/actions/runs/41203908963) succeeded with the production release hold still disabled. Its handoff validation and `build-and-push` were skipped, so **no images were published and no dispatch was sent**. The new same-job dispatch contract is merged and CI-tested, but live dispatch remains untested until the protected release prerequisites are configured.
- The schedule watchdog still has no observed run in the latest 100 platform-infra workflow runs. Its workflow file includes both `schedule` and `workflow_dispatch`, but no manual or scheduled run evidence exists yet. Next action: manually dispatch the read-only watchdog through GitHub Actions and inspect why scheduled `reconcile-vps.yml` events stopped; do not change the TCE market-scan schedule.
- Production remains **NOT HEALTHY/UNVERIFIED**: TCE public endpoints still return HTTP 503 while TCE is intentionally scaled to zero; Auth/SSO is unavailable; the last scheduled reconciliation failed the Auth, StockDividend, MicroFE, and Media health lanes. MicroFE/Media GitOps promotion still needs `PLATFORM_INFRA_AUTOMATION_TOKEN`; StockDividend release remains disabled and needs `PLATFORM_INFRA_TOKEN` plus compatible ARM64 image references before any live release.

Last reviewed: 2026-10-31, after StockDividend PR #18 merge. `platform-infra/master` is `6fdae4a124d200c0fb9ed5be1963cad136f92de2`; validation #41199921378 passed. StockDividend PR #18 was squash-merged as `a1ae52369859d9b72cc823621024bb408d72c168` after all five checks passed on exact head `128f53aa92cdc57988fc0bf2454865f9de0a800c`. The source publisher run #41203908963 succeeded with production release disabled, so publication and dispatch were skipped; post-merge CI #41203909024 was still in progress at last observation. No `reconcile-schedule-watchdog.yml` run appears in the latest 100 platform-infra workflow runs; latest scheduled reconcile remains #41184627405 (failure). TCE third-party integration check #41201516226 passed, but public healthcheck #41185878137 still fails with HTTP 503. Missing GitOps automation/handoff tokens, StockDividend ARM64 image compatibility, and schedule event delivery remain unresolved. Production remains NOT HEALTHY/UNVERIFIED; do not alter the TCE market-scan schedule.

Last reviewed: 2026-10-31 19:10 ICT. `platform-infra/master` is `d6a468dfc3c92565d525dba3e67ffddf71fa926f`; post-merge validation after PR #899 passed in #41199587478. StockDividend PR #16's neutral skip is verified on master (#41199383757, #41199621253): release disabled, build-and-push skipped, no images published. PR #17's API path change did not fix workflow-run job lookup (#41199646447 still HTTP 404, no dispatch). PR #18 is open at head `128f53aa92cdc57988fc0bf2454865f9de0a800c`, proposing same-job immutable dispatch after successful builds and removing the relay; release-contract test passed, remaining scraper build/checks still in progress. Release remains disabled and `PLATFORM_INFRA_TOKEN` missing. The schedule watchdog still has no observed scheduled run; latest reconcile remains #41184627405. Production remains NOT HEALTHY/UNVERIFIED; no TCE market-scan schedule changes.

Previous review (2026-10-31 19:04 ICT): `platform-infra/master` is `2564489bc54b1d8f95dc3e6f9d749d47837a4c83`; post-merge validation for PR #898 passed in #41199345579. StockDividend PR #16 merged as `969d2456411486b4aeec96e11a116dea76e1c90f`; master publisher #41199383757 now exits successfully with release disabled and skips image publication. Its downstream verifier #41199404999 exposed a leading-slash API path bug (HTTP 404) and correctly did not dispatch. PR #17 fixes the canonical path; contract check passed, other CI jobs are still running. Release flag remains false/unset, `PLATFORM_INFRA_TOKEN` missing, and current ARM64 compatibility blocker remains. The reconcile schedule watchdog has not yet produced an observed scheduled run; latest reconcile remains #41184627405. Production remains NOT HEALTHY/UNVERIFIED; no TCE market-scan schedule changes.

Previous review (2026-10-31 18:58 ICT): `platform-infra/master` is `acb867b0f8a9bfbca858d57044615c2dbebc1614`; PR #897 merged and post-merge manifest/workflow validation passed (#41195608846, #41195608756). The new read-only schedule watchdog has no observed scheduled run yet, and the latest `reconcile-vps.yml` scheduled run remains #41184627405 at 15:26 ICT; event-delivery root cause is unverified. StockDividend PR #16 is open with CI pending: it neutral-skips normal pushes while production publishing is disabled, keeps manual release fail-closed, and checks the actual `build-and-push` job before GitOps dispatch. It has not been merged or published images. MicroFE/Media still require `PLATFORM_INFRA_AUTOMATION_TOKEN`; StockDividend still requires `PLATFORM_INFRA_TOKEN` and compatible ARM64 images. Production remains NOT HEALTHY/UNVERIFIED; no TCE market-scan schedule changes.

Previous review (2026-10-31 17:18 ICT). Runner policy v11 is installed; targeted reconcile #41191877875 passed the Auth/Keycloak zero-replica/no-pod gate, and Supavisor had zero `keycloak_runtime` rows for 10:13:47–10:15:20 UTC. GHCR Registry V2 validation now passes for the checked packages. MicroFE immutable source-SHA images were validated in promotion #41192084543, but GitOps PR creation is blocked by missing `PLATFORM_INFRA_AUTOMATION_TOKEN`; Media promotion is blocked by the same secret. StockDividend's `12d63b4` admin/backend images lack a compatible ARM64 manifest, and its release handoff token is missing while the release flag remains false. The earlier broad reconcile #41191725540 failed the aggregate health gate on StockDividend, MicroFE, and Media. Production remains NOT HEALTHY/UNVERIFIED; no TCE market-scan schedule change.

Last reviewed: 2026-10-31 16:18 ICT. Supabase log query returned 382 recent `keycloak_runtime` auth-error circuit-breaker events in 10 minutes; direct SQL ping and role lookup still time out. Auth remains non-ready, and the exact credential mismatch is not yet proven. No secret or database role was changed.

Last reviewed: 2026-10-31 12:03 ICT. Inventory is based on the workflow files present on each repository's default branch at review time; no workflow definitions were changed by the latest credentials documentation merge.

## Deployment authority contract

- **Application repositories** own application CI, tests, build verification, immutable ARM64 GHCR publication, and dispatching non-secret release metadata.
- **`phanthienquoc/platform-infra`** owns production manifests, shared GHCR pull credentials, package/tag/digest validation, GitOps promotion PRs, cluster reconciliation, rollout/health verification, and deployment notifications.
- A successful app image build or dispatch is not proof of promotion or production health. Production PASS requires current rollout and application-health evidence.
- Never put runtime credentials in dispatch payloads. Payloads carry only app/component identifiers, immutable tags or image digests, and source commit metadata.
- Preserve CI, security, scheduled, manual recovery, backup, cleanup, and bootstrap jobs unless evidence proves a job is obsolete or redundant. Do not remove a workflow based on its filename alone.
- No workflow was removed during this inventory update. The TCE VPS setup and K3s bootstrap workflows remain operational/bootstrap workflows that require a content-level review before any retirement; they must not become a second app-release deployment authority.

## platform-infra — production and platform operations

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/reconcile-vps.yml` | Sole production GitOps reconcile authority; manual plan/apply, GitOps dispatch, path-scoped push, and declared 15-minute schedule. Owns K3s rollout and health gates. | Targeted Keycloak path change [#41191877875](https://github.com/phanthienquoc/platform-infra/actions/runs/41191877875) passed `auth-shutdown`; both Deployments are zero with no matching pods, and Supavisor showed no `keycloak_runtime` rows for 93 seconds. Broad reconcile [#41191725540](https://github.com/phanthienquoc/platform-infra/actions/runs/41191725540) passed GHCR package preflight and reconciled pull credentials but skipped manifest apply due no drift; aggregate health failed on StockDividend, MicroFE, and Media. Latest observed scheduled run remains [#41184627405](https://github.com/phanthienquoc/platform-infra/actions/runs/41184627405) at 15:26 ICT; investigate absent later schedule events without altering the TCE market-scan schedule. Production remains NOT HEALTHY/UNVERIFIED. |
| `.github/workflows/reconcile-schedule-watchdog.yml` | Read-only 15-minute freshness monitor for scheduled `reconcile-vps.yml` runs; fails when the latest scheduled event is older than 45 minutes. It never applies manifests or invokes cluster commands. | Merged by PR #897; post-merge manifest and workflow validation passed. No schedule-triggered run for the watchdog has yet been observed, so runtime behavior/cadence is unverified. Latest scheduled reconcile remains [#41184627405](https://github.com/phanthienquoc/platform-infra/actions/runs/41184627405) at 15:26 ICT; read-only inspection [#41190520868](https://github.com/phanthienquoc/platform-infra/actions/runs/41190520868) ran at 16:53 ICT. Investigate Actions event delivery and manually run once; do not change the TCE market-scan schedule. |
| `.github/workflows/gitops-image-promotion.yml` | Validates release metadata and GHCR access, creates verified GitOps promotion PRs, and dispatches reconciliation only after verified promotion. | PR #919 adds the atomic `stockdividend-images-published` path: it validates both backend/admin SHA-256 references and pins both production image entries by digest in one PR. The matching StockDividend producer is merged in PR #20 and sends one paired payload after ARM64 verification; no end-to-end dispatch has been verified. MicroFE/Media promotion still needs protected `PLATFORM_INFRA_AUTOMATION_TOKEN`; do not substitute `GHCR_READ_TOKEN`. |
| `.github/workflows/validate-manifests.yml` | Manifest/render validation on relevant PRs, master pushes, and explicit workflow dispatch for exact-head inspection validation. | PRs changing only `debug/vps-latest.md` are ignored by the ordinary PR trigger; inspection automation must still dispatch and observe success on the exact head SHA before merge. A regression assertion enforces this contract. |
| `.github/workflows/validate-github-actions.yml` | Workflow syntax/contract validation. | Latest master run passed. |
| `.github/workflows/inspect-vps.yml` | Read-only scheduled VPS/K3s inspection and debug snapshot. | Snapshot [#41178914394](https://github.com/phanthienquoc/platform-infra/actions/runs/41178914394) at 14:01 ICT: node Ready, disk 55%, but Keycloak/Auth/Media backend 0/1; Shell/WS have missing image tags and StockDividend old tags lack ARM64 manifests. The previous workflow immediately merged PR #879 before validation. PR #880 now adds explicit exact-head manifest validation and expected-SHA squash merging; run #41179285331 passed before PR #881 merged. This follow-up avoids the zero-job PR check for debug-only snapshot changes. |
| `.github/workflows/reconcile-observability.yml` | Follow-on observability reconciliation. | Latest observed run passed; this is not a production application-health pass. |
| `.github/workflows/smoke-production.yml` | Production smoke checks. | Preserve; verify current run before relying on it as health evidence. |
| `.github/workflows/keycloak-auth-production-smoke.yml` | Central SSO/Auth production smoke checks. | Preserve; Keycloak/OIDC health is not currently verified. |
| `.github/workflows/keycloak-ci.yml` | Keycloak build/test validation. | CI only. |
| `.github/workflows/provision-keycloak-tce-client.yml` | Controlled Keycloak client provisioning. | Operational, not app image publication. |
| `.github/workflows/verify-keycloak-tce-client.yml` | Keycloak client verification. | Verification-only. |
| `.github/workflows/configure-keycloak-no-email-registration.yml` | Explicit Keycloak realm configuration. | Manual configuration; preserve. |
| `.github/workflows/configure-keycloak-resend-smtp.yml` | Explicit Keycloak SMTP configuration. | Manual configuration; preserve. |
| `.github/workflows/provision-auth-runtime-secret.yml` | Provision Auth runtime secret from protected infrastructure configuration. | Secret values must stay out of logs and repository files. |
| `.github/workflows/runtime-secret-readiness.yml` | Runtime secret presence/readiness validation. | Preserve fail-closed behavior. |
| `.github/workflows/sso-auto-onboarding.yml` | SSO onboarding automation. | Preserve; no evidence to retire. |
| `.github/workflows/staging-dry-run.yml` | Staging dry-run / pre-production validation. | Preserve. |
| `.github/workflows/validate-metrics.yml` | Metrics validation. | Preserve. |
| `.github/workflows/validate-recovery-readiness.yml` | Recovery readiness gate. | Preserve. |
| `.github/workflows/bootstrap-runner.yml` | Self-hosted runner bootstrap/update. | Infrastructure bootstrap; not an app release lane. |
| `.github/workflows/vps-image-cleanup.yml` | VPS image cleanup. | Maintenance job; keep separate from release/reconcile authority. |
| `.github/workflows/mirror-locally-uncensored.yml` | Historical workflow; removed by owner-directed PR #1194. | DETACHED. Do not recreate or restore without explicit owner authorization. |

## TCE-dashboard — application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/wf-01-tce-build-verify.yml` | App build verification. | Latest master run passed. |
| `.github/workflows/wf-01p-tce-web-pr-build.yml` | Pull-request web build. | Preserve PR coverage. |
| `.github/workflows/wf-02-tce-backend-unit-test.yml` | Backend unit tests. | Latest master run passed. |
| `.github/workflows/wf-02-tce-prettier-format.yml` | Formatting validation. | Latest master run passed. |
| `.github/workflows/wf-03-tce-production-deploy.yml` | Explicit manual production image release from master; application-side build/publish and release dispatch, not production cluster reconciliation. | Do not rerun for workflow-only changes. |
| `.github/workflows/wf-04-tce-k3s-cleanup.yml` | K3s cleanup/maintenance. | Preserve; audit before any retirement. |
| `.github/workflows/wf-06-tce-healthcheck.yml` | Scheduled public HTTP health checks. | Latest run [#41185878137](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41185878137) returned HTTP 503 for TCE web and Auth liveness/readiness. TCE 503 is expected while the operator-requested K3s pause remains in force; Auth 503 is an unresolved independent production failure. Preserve the health check rather than masking the failure. |
| `.github/workflows/wf-07-tce-backup.yml` | Backup operation. | Preserve recovery capability. |
| `.github/workflows/wf-07-tce-integration-check.yml` | Integration checks. | Preserve. |
| `.github/workflows/wf-08b-tce-microfe-build-publish.yml` | MicroFE Auth/Shell/WS checks and Shell/WS image publication; dispatches immutable image metadata for central promotion. | Publish run [#41154490073](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41154490073) built/pushed Shell digest sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd and WS digest sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d for source e6940ff911ea63338fb4f66eb903bcdf6c9825a8; GitOps promotion [#41154654986](https://github.com/phanthienquoc/platform-infra/actions/runs/41154654986) is blocked by HTTP 403 from shared GHCR_READ_TOKEN on both packages. Deployed manifests still reference missing placeholder tags. |
| `.github/workflows/wf-09-nginx-readonly-audit.yml` | Read-only Nginx audit. | Audit-only. |
| `.github/workflows/wf-09-tce-vps-safe-setup.yml` | Safe VPS setup/operations. | Keep separate from app release and GitOps promotion. Review content before any change. |
| `.github/workflows/wf-10-tce-k3s-bootstrap.yml` | K3s bootstrap. | Bootstrap-only candidate for ownership review, not deletion by name. |
| `.github/workflows/wf-11-tce-mobile-landscape-viewport.yml` | Mobile landscape viewport regression checks. | Preserve UI regression coverage. |

## stockdividend — application CI, publisher, and scraper

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Application CI. | Latest master CI passed. |
| `.github/workflows/deploy.yml` | Build/publish ARM64 images from master only after release-enable and GitOps handoff gates pass; verifies registry digests/platforms and sends one paired StockDividend digest event after successful publication. | PR #20 merged as `82b7bf6f3d122dec96e870991bac3e25ade64bb5`; exact-head CI [#41237443765](https://github.com/phanthienquoc/stockdividend/actions/runs/41237443765) passed all five jobs. The last verified publisher [#41232557169](https://github.com/phanthienquoc/stockdividend/actions/runs/41232557169) skipped build/push while the release hold was disabled. The post-merge publisher run for #20's merge commit is not yet verified; do not infer that it published or skipped. Existing production admin/backend refs still use `12d63b4`, which lacks a compatible ARM64 manifest. |
| `.github/workflows/run_scraper.yml` | Scraper job, including scheduled/manual operation. | Scheduled run [#41178133076](https://github.com/phanthienquoc/stockdividend/actions/runs/41178133076) is still in progress on the old commit and logs repeatedly report disabled vnstock 5.0.1. PR [#15](https://github.com/phanthienquoc/stockdividend/pull/15) upgraded the dependency to 5.2.1 and merged after the five-job CI suite passed; the next run will pick up the new pin. Do not cancel or remove the scheduled job. |

Confirmed retirement: `.github/workflows/wf-platform-infra-release.yml` was removed by StockDividend PR #18 after the `workflow_run` relay repeatedly failed source-job lookup with HTTP 404. The successful publisher job is now the sole StockDividend release-handoff authority; do not reintroduce the relay.

## media-generation — application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Media app CI. | Latest master CI passed. |
| `.github/workflows/wf-03-media-production-deploy.yml` | Master-only/manual production release, immutable version + full-source-SHA tag publication, then central GitOps promotion request. | Immutable tag prod-v0.3.0-32f3bf56e1f44c65a5d98f35bed0547f398f8e90 exists and exact GHCR manifests validated in [#41158836425](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836425) and [#41158836607](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836607), but promotion is blocked by missing PLATFORM_INFRA_AUTOMATION_TOKEN. The currently deployed backend uses old tag prod-v0.3.0-58f80a8 and remains non-ready; do not equate publication with deployment or health. |

## phanthienquoc-authentication — Auth application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Auth service tests, typecheck, build, and container build. | Latest master CI passed. |
| `.github/workflows/release.yml` | Explicit manual master-only Auth image release; verifies source SHA and version before publishing and dispatching. | Post-merge reconcile [#41187383657](https://github.com/phanthienquoc/platform-infra/actions/runs/41187383657) shows `microfe-auth` desired=1/ready=0 on `prod-v1.0.0-ceb2688`; secret key-presence and TLS checks pass while public Auth health remains HTTP 503. Supabase logs on 2026-10-31 09:08–09:18 UTC show repeated `keycloak_runtime` `auth_error` circuit-breaker events; SQL ping and role lookup via the management connector time out, so role existence/password parity is not verified. Do not reset credentials until secure role/Secret comparison is possible. |
| `.github/workflows/web-ci.yml` | Auth web CI. | Preserve separate web validation. |

## Release contract checks

1. Reject non-master production release attempts.
2. Require successful source tests/build before publication.
3. Use immutable source-SHA tags or verified `sha256:<64 hex>` image digests; never promote mutable aliases such as `latest`.
4. Verify GHCR package access before mutating shared pull credentials or cluster manifests.
5. Require the appropriate protected handoff credential before creating a GitOps PR. `GHCR_READ_TOKEN`, `PLATFORM_INFRA_AUTOMATION_TOKEN`, StockDividend's `PLATFORM_INFRA_TOKEN`, and app release-dispatch tokens are distinct contracts; do not substitute them for one another.
6. Reconcile only through platform-infra, then verify Deployment desired/ready/updated replicas and public liveness/readiness endpoints.
7. A zero-replica maintenance scope passes only when every scoped Deployment has desired=ready=updated=0 and no active pods remain; otherwise fail closed. Keep production health NOT HEALTHY/UNVERIFIED while any required lane fails. Preserve the TCE market-scan schedule continuously.


## Latest workflow inventory review (2026-11-01 06:59 ICT; schedule and Supabase data-plane evidence refreshed)

- Default-branch heads reviewed: platform-infra `2646853eb80e0e83ae186b557a98e8e478ed37b7`, TCE-dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`, StockDividend `82b7bf6f3d122dec96e870991bac3e25ade64bb5`, Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`, Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none observed in TCE-dashboard, StockDividend, or Media Generation.
- **Platform Infra schedule contract:** `reconcile-vps.yml` still declares `*/15 * * * *`; `inspect-vps.yml` declares its hourly :15 and :30 inspections; `reconcile-schedule-watchdog.yml` retains its */15 cron plus schedule-only `workflow_run` fallbacks after both workflows. Latest scheduled reconciliation is [#41247425890](https://github.com/phanthienquoc/platform-infra/actions/runs/41247425890) (22:16:22Z, failure). Latest scheduled inspection [#41253007319](https://github.com/phanthienquoc/platform-infra/actions/runs/41253007319) succeeded at 23:33:10Z. The post-inspection watchdog [#41253097099](https://github.com/phanthienquoc/platform-infra/actions/runs/41253097099) executed but failed freshness at 78 minutes (>45-minute threshold). The separate scheduled watchdog [#41251234237](https://github.com/phanthienquoc/platform-infra/actions/runs/41251234237) also detected stale reconciliation. The after-reconcile fallback remains unexercised since no newer scheduled reconciliation completed; 15-minute cadence is not proven stable.
- **Workflow inventory and authority:** application repositories own tests/builds, immutable full-source-SHA GHCR publication, ARM64 verification, and paired digest dispatch payloads. Platform Infra owns package-read preflight, atomic digest pinning, GitOps PR validation/merge, reconciliation, K3s rollout, and health gates. PR #927's PAT-free promotion contract supersedes older historical notes in this file that describe `PLATFORM_INFRA_AUTOMATION_TOKEN` as required for GitOps PR creation; the active promotion workflow uses scoped `GITHUB_TOKEN`. This does not replace GHCR_READ_TOKEN or app-to-platform dispatch credentials.
- **GHCR / release status:** Media publisher [#41158598649](https://github.com/phanthienquoc/media-generation/actions/runs/41158598649) published immutable frontend/backend digests, but Platform Infra GHCR validation failed HTTP 403 in [#41158836425](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836425) and [#41158836607](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836607); no successful GitOps promotion was established. StockDividend publisher [#41237638206](https://github.com/phanthienquoc/stockdividend/actions/runs/41237638206) skipped handoff validation and build/push under the release hold; no new image/dispatch was produced. Keep the release hold.
- **Supabase dependency:** control-plane project status is `ACTIVE_HEALTHY`, but the read-only SQL probe timed out. Logs for 22:00Z–23:59Z show 1,206 HTTP 522 REST responses on `video_generation_jobs` (last at 23:58:59Z) and seven Postgres statement-timeout events. Root cause remains unconfirmed; preserve Media readiness checks and investigate database/pooler health before changing application behavior.
- **Runtime evidence:** inspection snapshot #930 records K3s node Ready, disk pressure normal at 55%, GitOps drift clean; MicroFE missing image tags, StockDividend ARM64 manifest mismatch, and Media backend 0/1 ready. TCE and Auth/Keycloak remain intentionally at 0/0. Some privileged snapshot commands could not run non-interactively due sudo password requirements.
- Preserve useful CI, tests, security, backup, manual, release, maintenance and scheduled workflows. No duplicate SSH/Compose deployment authority was added or removed. No image publication, repository dispatch, GitOps promotion or production rollout was observed in this review. TCE market-scan schedule unchanged.


## Latest automation review (2026-11-01 07:57 ICT; schedule-state diagnostic and runtime evidence refreshed)

- Re-inspected all five default branches, open PRs, recent workflow runs/checks, and this tracker/inventory. Current heads: platform-infra `af4a480b1d5938e239fcfd7ace4347eb6be24ffa`; TCE Dashboard `8547e1315fea75202f70f14556589e76ab1f65ed`; StockDividend `82b7bf6f3d122dec96e870991bac3e25ade64bb5`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; none returned for TCE Dashboard, StockDividend, or Media Generation. Platform Infra master validation after the previous tracker refresh passed in [#41255106631](https://github.com/phanthienquoc/platform-infra/actions/runs/41255106631).
- **Schedule gap:** latest scheduled `reconcile-vps` in the first 100 recent master workflow runs is [#41247425890](https://github.com/phanthienquoc/platform-infra/actions/runs/41247425890), created 2026-10-31 22:16:22Z and concluded failure. Latest scheduled inspection is [#41253007319](https://github.com/phanthienquoc/platform-infra/actions/runs/41253007319), successful at 23:33:10Z. The after-inspection watchdog [#41253097099](https://github.com/phanthienquoc/platform-infra/actions/runs/41253097099) failed freshness at 78 minutes; scheduled watchdog [#41251234237](https://github.com/phanthienquoc/platform-infra/actions/runs/41251234237) also failed freshness. No newer scheduled reconciliation appears in the inspected first page. The connected GitHub read interface did not allow direct workflow enabled-state metadata; this change adds an explicit runtime check of `actions/workflows/reconcile-vps.yml` and fails with a distinct diagnostic unless its state is `active`. Existing 15-minute reconcile and watchdog cron declarations remain unchanged.
- **Latest reconcile detail:** shared reconcile job in #41247425890 succeeded. GHCR package preflight verified all nine production packages (Auth, Media backend/frontend, MicroFE Shell/WS, StockDividend admin/backend, TCE service/web) at 22:16:35Z; shared `ghcr-pull` Secret was unchanged and credential reconciliation succeeded. This supersedes older HTTP 403 observations as evidence of current package-read access, but does not prove a new digest promotion. MicroFE Shell/WS still fail on missing `0.1.0`/`RELEASE_SHA`; StockDividend admin/backend still lack an ARM64 manifest for `12d63b4`; Media backend remains 0/1 Ready on the old tag. No manifest apply occurred because there was no GitOps drift.
- **Supabase dependency:** project `gtqovpusfyyvxpeezxlo` still reports control-plane `ACTIVE_HEALTHY`. A read-only SQL probe at 2026-11-01 00:57:44Z failed with `Connection terminated due to connection timeout`. Unified logs for 00:00–00:57Z contain 659 edge-log events and 14 Postgres events; 11 Postgres events are `canceling statement due to statement timeout`, and 3 are client resets. Performance advisor also timed out. Root cause remains unconfirmed; do not change schema, roles, credentials, or readiness semantics.
- **Application release evidence:** TCE MicroFE publisher [#41154490073](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41154490073) previously published Shell digest `sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd` and WS digest `sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d` for source `e6940ff911ea63338fb4f66eb903bcdf6c9825a8`; no corresponding successful GitOps promotion or rollout is recorded. StockDividend publisher [#41237638206](https://github.com/phanthienquoc/stockdividend/actions/runs/41237638206) completed at workflow level but skipped handoff validation and build/push under the production release hold. Media has no newer publisher than [#41158598649](https://github.com/phanthienquoc/media-generation/actions/runs/41158598649); its historical GHCR 403 is superseded by the later all-package preflight, but no newer paired digest promotion is verified. Keep StockDividend release hold.
- TCE scheduled healthcheck [#41249248285](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41249248285) remains failed while TCE is intentionally 0/0; backup [#41245102655](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41245102655) and integration [#41244335183](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41244335183) passed. Authentication CI/release evidence [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844) / [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) is historical, not current SSO health proof.
- No production manifests, credentials, release flags, database objects, or K3s workloads changed. No workflow dispatch or repository dispatch was sent because the connected GitHub tool surface is read/write for repository files and PRs but does not expose Actions dispatch. TCE remains scale-to-zero; Auth/Keycloak remain stopped; TCE market-scan schedule unchanged. Production remains **NOT HEALTHY/UNVERIFIED**.
- **Next actions:** verify the new watchdog's workflow-state check on its first scheduled/fallback run; restore Supabase SQL/REST data-plane connectivity; replay only the already-published MicroFE digest pair after exact GHCR digest verification; preserve StockDividend release hold until authorized ARM64 publication; then verify GitOps digest pins, K3s rollout, and application health.


## Latest workflow inventory review (2026-11-01 09:11 ICT; MicroFE digest rollout and push-scope fix pending)

- Re-inspected all five repositories, current default-branch heads, open PRs, and Actions history. Platform Infra master is e01e1b2aee8622e9f0521a1759042671c9dc5d6e; TCE Dashboard 8547e1315fea75202f70f14556589e76ab1f65ed; StockDividend 82b7bf6f3d122dec96e870991bac3e25ade64bb5; Media Generation d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9. Open PRs are platform-infra #934 plus #795/#749/#741/#648/#544/#541/#539/#538, and Authentication #76/#75; no open PRs returned for the other three app repos.
- Reconcile push scope: run [#41263819258](https://github.com/phanthienquoc/platform-infra/actions/runs/41263819258) followed PR #933's MicroFE-only GitOps merge but ran with TARGET_APP=all. The old workflow only selected a special Keycloak scope and otherwise retained all. This caused unrelated StockDividend and Media rollout lanes to run and fail while MicroFE rollout succeeded. PR #934 adds scripts/resolve-push-deployment-scope.sh, maps changed paths to a single app, uses all only for multi-app/cluster-wide changes, preserves the isolated Keycloak shutdown/rollout decision, and rejects unknown paths. It adds self-tests to validate-github-actions.yml; the PR is not merged and checks are pending on the final head.
- MicroFE deployment: PR #933 merged the Shell and WS SHA-256 digests from TCE Dashboard source e6940ff911ea63338fb4f66eb903bcdf6c9825a8. In #41263819258 both deployment rollouts and the MicroFE workload health gate passed. The latest inspection snapshot [#41264393955](https://github.com/phanthienquoc/platform-infra/actions/runs/41264393955) shows the live deployment references pinned to those digests. This is rollout evidence, not a separately captured pod imageID verification.
- Schedule watchdog: the reconcile-vps workflow metadata check returned state=active in [#41264226448](https://github.com/phanthienquoc/platform-infra/actions/runs/41264226448); that scheduled watchdog failed only because the latest scheduled reconcile [#41260761381](https://github.com/phanthienquoc/platform-infra/actions/runs/41260761381) was 51 minutes old. The after-reconcile fallback [#41260888538](https://github.com/phanthienquoc/platform-infra/actions/runs/41260888538) succeeded with age 1 minute. Thus the fallback works, but 15-minute schedule delivery is still not stable/proven. Latest scheduled inspection [#41264393955](https://github.com/phanthienquoc/platform-infra/actions/runs/41264393955) passed; its related workflow_run event [#41264411316](https://github.com/phanthienquoc/platform-infra/actions/runs/41264411316) was skipped by the non-scheduled-source guard, so no after-inspection success is yet evidenced for that inspection.
- Current lane failures: StockDividend still references admin/backend tag 12d63b4; snapshot events show ImagePullBackOff due no matching ARM64 platform manifest. The latest push reconciliation also timed out waiting for old admin/backend replicas and reported the frontend ProgressDeadlineExceeded. Media backend remains 0/1 on prod-v0.3.0-58f80a8 with ProgressDeadlineExceeded; frontend is 1/1. TCE and Auth remain intentionally 0/0; Keycloak 0/0 and public OIDC probes return 503 while stopped.
- TCE scheduled public endpoint check [#41261234620](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41261234620) returned HTTP 503 for TCE web and Auth liveness/readiness, consistent with the current scale-to-zero maintenance state. Backup/integration runs [#41245102655](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41245102655) and [#41244335183](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41244335183) passed. StockDividend release remains disabled; its publisher has not produced a new image/dispatch. Media CI is green but no new paired digest publication/dispatch is verified. Auth CI/release results remain historical only.
- Supabase's last confirmed SQL connectivity probe (00:57:44Z) timed out; no new probe was run in this review. Do not bypass Media readiness or change DB schema/secrets based on this evidence.
- Preserve CI, tests, security, manual, release, backup, maintenance, and scheduled workflows. No duplicate direct SSH/Compose authority added or removed. TCE market-scan schedule unchanged.


## Latest workflow inventory review (2026-11-01 09:20 ICT; path-scoped reconciliation merged)

- Platform Infra master is 351d584aca78c59281d3c9edb8004e869c29effb after PR #934 squash merge. Exact-head PR checks and all three post-merge checks succeeded. Other default-branch heads: TCE Dashboard 8547e1315fea75202f70f14556589e76ab1f65ed; StockDividend 82b7bf6f3d122dec96e870991bac3e25ade64bb5; Media Generation d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PR inventory: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #76/#75; no open PRs observed in TCE Dashboard, StockDividend, or Media Generation.
- Push reconciliation now uses scripts/resolve-push-deployment-scope.sh and a tested path map. Single app changes run only that app's health lane; multi-app and cluster-wide changes run all lanes; Keycloak-only changes preserve the replica-aware shutdown/rollout path; mixed Keycloak and unclassified paths fail closed. The resolver is tested in validate-github-actions.yml. PR #934 exact-head validation and post-merge checks all succeeded. The PR changed workflow/test/docs files only and did not trigger a new production reconcile.
- MicroFE digest references are now applied in production: Shell sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd and WS sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d. Reconcile run #41263819258 and inspection snapshot #41264393955 provide rollout/reference evidence; pod imageIDs were not separately captured.
- StockDividend admin/backend remain on 12d63b4 and ImagePullBackOff due missing ARM64 manifest; rollout also timed out on old replicas. Media backend remains 0/1 on prod-v0.3.0-58f80a8 with ProgressDeadlineExceeded; frontend is 1/1. StockDividend publisher still skips build/push under release hold; no new digest dispatch. Media CI is green but no new paired release dispatch is verified.
- The read-only watchdog now proves reconcile-vps is active. The after-reconcile fallback passed on run #41260888538; the after-inspection fallback ran on #41264498337 and failed freshness at 54 minutes. Scheduled watchdog #41264226448 failed at 51 minutes. Thus fallback triggers are exercised but scheduled reconcile delivery is still stale/unproven.
- Supabase control-plane status is ACTIVE_HEALTHY, but a read-only SQL probe timed out and unified logs recorded 962 HTTP 522 responses for the Media video_generation_jobs REST query during 00:57:44–02:18:00Z. Root cause remains unknown; preserve readiness checks and do not modify schema/secrets to hide it.
- TCE public healthcheck #41261234620 returned HTTP 503 for TCE web and Auth endpoints while TCE/Auth/Keycloak remain intentionally at zero replicas. Backup and integration checks passed. Authentication CI/release checks are historical only.
- Preserve useful CI, security, backup, manual, release, maintenance, and scheduled workflows. No duplicate direct SSH/Compose deployment authority added or removed. TCE market-scan schedule unchanged.


## Latest workflow inventory review (2026-11-01 13:57 ICT; TCE WF-12 monitor pending)

- Verified default-branch heads: platform-infra `0751e3b75d89e7789ece8a9561193e26e8e97df4`; TCE Dashboard `48a8c86497f55b0454ea20fda0567d27f7b9718b`; StockDividend `a6f55ee2e511ab5910c825e56803bd82fe9a0f62`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open PRs: platform-infra #795/#749/#741/#648/#544/#541/#539/#538; TCE #1006; Authentication #75/#76; none in StockDividend or Media Generation.
- Platform Infra latest master manifest validation [#41279841471](https://github.com/phanthienquoc/platform-infra/actions/runs/41279841471) passed on exact current head `0751e3b`. The last master workflow-lint run [#41279747450](https://github.com/phanthienquoc/platform-infra/actions/runs/41279747450) passed on the immediately preceding docs-only commit; the current head only records the Auth smoke correction and does not change workflows.
- **Platform scheduling:** `reconcile-vps.yml` retains cron `7,22,37,52 * * * *`; watchdog retains `12,27,42,57 * * * *`; inspection retains `2,32 * * * *`. Last scheduled reconcile [#41260761381](https://github.com/phanthienquoc/platform-infra/actions/runs/41260761381) failed application health lanes at 01:21:35Z. Last scheduled inspection [#41264393955](https://github.com/phanthienquoc/platform-infra/actions/runs/41264393955) failed the inspection PR merge request with HTTP 405; PR #950 fixed that merge response handling and push inspection [#41275351280](https://github.com/phanthienquoc/platform-infra/actions/runs/41275351280) succeeded, but no scheduled run after that fix has been observed. Scheduled watchdog [#41264226448](https://github.com/phanthienquoc/platform-infra/actions/runs/41264226448) and after-inspection watchdog [#41264498337](https://github.com/phanthienquoc/platform-infra/actions/runs/41264498337) reported stale reconciliation. Schedule recovery is not proven.
- **TCE WF-06 / WF-12:** WF-06 remains at `*/15 * * * *`; last scheduled run [#41261234620](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41261234620) at 01:28:29Z failed its public smoke with HTTP 503 while TCE/Auth were intentionally 0/0. WF-07's six-hour integration run [#41279469909](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41279469909) passed at 06:06:31Z. New TCE PR [#1006](https://github.com/phanthienquoc/TCE-dashboard/pull/1006) adds `.github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml`, a read-only Actions API monitor (actions:read) with a separate offset cron, a 25-minute freshness budget, 15-minute runner queue budget, and a completion fallback after scheduled WF-06. Its contract test is wired through WF-02. Exact-head WF-02 [#41283006267](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283006267) passed; exact-head WF-05 [#41283006289](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283006289) was in progress at the last inspection. Do not merge until WF-05 and the final PR head are verified. No TCE market-scan workflow or schedule was changed.
- **StockDividend app publisher:** master CI [#41273202852](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202852) and publisher [#41273202844](https://github.com/phanthienquoc/stockdividend/actions/runs/41273202844) passed. Publisher job steps confirm native ARM64 build/push and immutable manifest verification for Scraper, Admin and Backend. Exact digests are recorded in the deployment tracker. Platform Infra handoff validation and atomic promotion dispatch were intentionally skipped because `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=false`; the app publisher owns artifacts, but platform-infra still owns GitOps promotion and rollout. Keep the release hold.
- **Media:** master CI [#41246414186](https://github.com/phanthienquoc/media-generation/actions/runs/41246414186) passed. Latest runtime snapshot [#41275351280](https://github.com/phanthienquoc/platform-infra/actions/runs/41275351280) shows Media backend/frontend 1/1 and pod imageIDs matching the pinned digests. No newer Media publisher or paired digest dispatch was observed.
- **MicroFE / StockDividend runtime:** the same 05:02:36Z snapshot confirms MicroFE Shell/WS 1/1 and imageIDs matching pinned digests. StockDividend admin 0/1 ImagePullBackOff and new admin/backend pods fail to pull tag `12d63b4` due no matching ARM64 manifest; old backend/frontend replicas remain Running on `23b2878`. Newly published StockDividend digests are not in production manifests because promotion remains disabled.
- **TCE / Auth runtime:** TCE frontend/service and Auth/Keycloak remain at 0/0 by operator request. Public 503 responses are expected while stopped and are not treated as deployment success. Authentication CI/release evidence [#41033586844](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41033586844) / [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) is historical; no new Auth image promotion or live SSO validation was performed.
- **Supabase:** project `gtqovpusfyyvxpeezxlo` remains `ACTIVE_HEALTHY`; read-only SQL connectivity probe succeeded at 06:57:12Z. Recent log query returned 358 edge and 30 PostgREST events but did not extract a usable status code. Treat as a successful connectivity sample only, not long-term stability proof.
- Authority remains unchanged: app repositories own tests/builds, immutable full-source-SHA GHCR publication, ARM64 verification and paired payload production; platform-infra owns GHCR package-read preflight, shared pull credentials, atomic digest promotion, GitOps reconciliation, K3s rollout and health gates. The active GitOps PR path uses scoped `GITHUB_TOKEN` per PR #927; do not revive the old automation PAT dependency or substitute GHCR_READ_TOKEN for dispatch credentials.
- Preserve useful CI, test, security, backup, manual, release, maintenance and scheduled workflows. Do not add direct SSH/Compose deployment authority. No production manifests, credentials, release flags, database objects or K3s desired replicas changed in this review. TCE market-scan schedule unchanged.


## TCE WF-12 post-merge verification (2026-11-01 14:03 ICT)

- TCE PR #1006 merged at `0abf783801fe5d0791402c26621956277954bce1` after exact-head WF-02 [#41283006267](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283006267) and WF-05 [#41283006289](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283006289) passed on `dbd3cbfec70ef4c8ca74f3675e0365b3882b20d1`.
- First WF-12 push smoke [#41283176612](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176612) succeeded and confirmed the WF-06 workflow is active. It read the latest scheduled WF-06 run [#41261234620](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41261234620), measured age 334 minutes, emitted the expected warning-only stale-schedule diagnostic, and exited successfully because push smoke is non-enforcing. This verifies the monitor's API/read-only path, not WF-06 schedule recovery.
- The next scheduled, manual or schedule-completion WF-12 enforcement run will fail while the latest WF-06 schedule age exceeds 25 minutes. WF-06 remains at `*/15 * * * *`; TCE market-scan schedule is unchanged.
- Post-merge master WF-01 [#41283176495](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176495), WF-02 [#41283176548](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176548), and WF-05 [#41283176531](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176531) were still in progress at this review; record their final conclusions separately when available.


## Cross-repo post-merge status (2026-11-01 14:05 ICT)

- Platform Infra PR #959 merged at `a0c4bac0f4821da3239e0b2727addbc0141017cc`; exact-head manifest validation [#41283220978](https://github.com/phanthienquoc/platform-infra/actions/runs/41283220978) and post-merge manifest validation [#41283255346](https://github.com/phanthienquoc/platform-infra/actions/runs/41283255346) both succeeded.
- TCE PR #1006 merged at `0abf783801fe5d0791402c26621956277954bce1`. Exact-head WF-02 [#41283006267](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283006267) and WF-05 [#41283006289](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283006289) succeeded. Post-merge WF-02 [#41283176548](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176548) and WF-05 [#41283176531](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176531) also succeeded. WF-12 push smoke [#41283176612](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176612) confirmed WF-06 state active and read the latest scheduled run, but reported it 334 minutes stale in warning-only push mode. WF-01 post-merge build [#41283176495](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41283176495) was still building the frontend image at the last check.
- Supabase SQL connectivity succeeded again at 07:03:53Z; this is a second read-only sample after recovery. The latest log summary contained 47 edge and 5 PostgREST events, without a usable status-code breakdown.
- No production manifests, image references, shared pull credentials, application dispatch tokens, release flags, database objects, desired replicas or K3s workloads changed. StockDividend production promotion remains disabled despite all three ARM64 image digests being available. TCE and Auth remain intentionally at zero replicas. The TCE market-scan schedule is unchanged.


## Latest workflow inventory review (2026-11-01 09:07 UTC; clock-safe schedule monitoring)

- TCE Dashboard PR #1007 merged the WF-12 API-clock fix. WF-12 now compares the latest scheduled WF-06 run to the current watchdog run's GitHub Actions API `created_at`, avoiding runner wall-clock skew. Exact-head WF-02 #41287338443 and WF-05 #41287338448 passed; post-merge WF-12 push smoke #41287452389 passed and reported latest WF-06 scheduled run #41287060151 age=5m / queue=0m. WF-06's four public endpoints still returned HTTP 503 because TCE/Auth are intentionally at 0 replicas. Schedule delivery is observed for this single interval; cadence stability is not proven.
- Platform Infra PR #961 merged API-clock-based reconciliation freshness and inspection queue measurement. Exact-head lint #41287343016 and manifest validation #41287342878 passed; post-merge lint #41287395612, manifest validation #41287395593, and read-only watchdog push smoke #41287395596 passed. The watchdog now correctly reports scheduled reconcile #41260761381 age=464m and inspection #41264393955 queue=106m. No production reconciliation was run by this change.
- Preserve TCE WF-06 cron `*/15 * * * *`, WF-12 offset cron `7,22,37,52 * * * *`, Platform reconcile cron `7,22,37,52 * * * *`, Platform watchdog cron `12,27,42,57 * * * *`, and inspection cron `2,32 * * * *`. No TCE market-scan schedule was modified.
- StockDividend weekend scraper workflow #41284033242 remains intentionally scheduled and was still executing its scraper step after dependency/browser setup; do not remove/cancel without a confirmed failure. StockDividend production publisher #41273202844 verified three immutable ARM64 digests, but the GitOps handoff/dispatch remains skipped because production release is disabled.
- Runtime evidence remains from inspection #41275351280 (05:02:36Z): MicroFE and Media healthy with pinned imageIDs; StockDividend old image pull failures persist; TCE/Auth/Keycloak intentionally 0/0. Supabase last successful SQL sample is 07:03:53Z; no new probe in this review.
- Workflow authority remains: app repos own tests/builds/immutable GHCR publication; platform-infra owns package-read preflight, shared pull credentials, atomic GitOps promotion, reconciliation, rollout and health. No duplicate direct SSH/Compose deployment authority introduced. Preserve useful CI/security/backup/manual/release/maintenance/scheduled workflows.


## Latest workflow inventory review (2026-11-01 09:10 UTC; queue diagnostics run after enforcement failures)

- Platform Infra PR #963 merged the read-only inspection queue telemetry change. The diagnostic step now uses `if: always()` and fetches the current watchdog run's Actions API timestamp if the freshness step exited before exporting its reference. Exact-head lint #41287601671 and manifest validation #41287601618 passed; post-merge lint #41287639543 and manifest validation #41287639544 passed; watchdog push smoke #41287639548 passed and emitted the inspection queue diagnostic.
- Watchdog push smoke evidence: scheduled reconcile #41260761381 is 467 minutes old and failed; scheduled inspection #41264393955 waited 106 minutes for a runner. The watchdog now reports both signals independently; scheduled reconciliation and self-hosted queue recovery remain unresolved.
- TCE PR #1007 merged the API-clock reference fix. Post-merge WF-12 push smoke #41287452389 passed, measuring WF-06 run #41287060151 at 5 minutes old with 0-minute queue. WF-06 public checks still return 503 while TCE/Auth are intentionally stopped. WF-01 image build #41287452305 completed SUCCESS at 09:09:35Z; WF-02 and WF-05 passed.
- StockDividend weekend scraper #41284033242 remains in progress at its scraper step; preserve this purposeful scheduled job and await a real conclusion. Its immutable ARM64 image publisher #41273202844 passed for all three images, while production promotion remains disabled.
- Preserve Platform reconcile/watchdog/inspection cron declarations, TCE WF-06/WF-12 cron declarations, and the separate TCE market-scan schedule. No workflow removed or schedule altered. Application/GitOps ownership and read-only monitoring permissions remain unchanged.


## Cross-repo deployment review — 2026-11-01

### Platform Infra operations workflows

- `reconcile-vps.yml`: remains the sole GitOps apply/reconciliation authority. Existing cron declarations are unchanged.
- `reconcile-schedule-watchdog.yml`: read-only Actions API monitor. Reconciliation freshness budget 45m; runner queue budget 15m; inspection freshness budget 75m for the 30m inspection cadence; inspection queue telemetry 15m. Uses the watchdog run's GitHub API `created_at` as the reference clock. For `run_attempt > 1`, queue duration is explicitly not measurable from run-level timestamps; freshness remains tied to the original scheduled `created_at`.
- `inspect-vps.yml`: scheduled read-only inspection. The watchdog now independently checks that the workflow is active and that scheduled inspection events remain fresh.
- Push-triggered watchdog smoke remains warning-only; scheduled/manual/fallback enforcement remains fail-closed. Permissions remain read-only (`actions: read`, `contents: read`).
- PR #965 added inspection schedule freshness; PR #966 made reconciliation and inspection queue telemetry rerun-aware. Both are merged and exact-head/post-merge validations passed.

### TCE Dashboard operations workflows

- WF-06 retains its existing 15-minute schedule and four independent public health endpoints.
- WF-12 remains a read-only monitor with a 25-minute WF-06 freshness budget and 15-minute queue budget; it uses GitHub Actions API timestamps and now treats queue time as not measurable for rerun attempts while preserving original-event freshness.
- PR #1008 merged the rerun-aware queue correction. WF-02/WF-05 exact-head checks and post-merge WF-02/WF-05/WF-12 smoke succeeded.
- No TCE market-scan schedule changes.

### Application publisher and dispatch contract

- StockDividend application repo owns build/test and immutable GHCR publication. Publisher run #41273202844 verified Scraper/Admin/Backend SHA-256 digests and linux/arm64 manifests.
- The publisher constructs one `stockdividend-images-published` event with `app`, full source `commit`, `backend_digest`, and `admin_digest`. Platform Infra consumes the same event, validates the full commit and both SHA-256 digests, and pins the pair atomically in one GitOps promotion.
- Static producer/consumer contract inspection passed. Dispatch was not executed because `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=false`; this hold remains authoritative.
- The weekend scraper is a purposeful data job, not a second deployment authority. It remains scheduled/manual and was still running in #41284033242 at the last observation; do not remove it without a demonstrated failure or redundancy.

### Current operational evidence

- Platform scheduled reconciliation and inspection histories remain stale even though both workflows report `active`. The post-merge watchdog smoke #41291879618 passed in warning-only mode and reported original scheduled-event ages of 468m and 414m respectively. Rerun attempt 2 queue times were correctly marked not measurable.
- Read-only health rerun of #41260761381 attempt 2: MicroFE and Media health gates passed; TCE/Auth were accepted as intentionally scaled to zero; StockDividend failed on old tag `12d63b4` without an ARM64 manifest.
- Supabase SQL probe at 09:09:08Z succeeded; 09:00–09:08Z edge/PostgREST log window had 0 HTTP 522.
- Runtime digest evidence remains available for Media and MicroFE from the prior inspection; a fresh full inspection is still required.

Preserve CI, tests, security, backups, manual release, and purposeful scheduled data jobs. No duplicate direct SSH/Compose deployment authority was added.


## Workflow inventory review — 2026-11-01 17:00 ICT

- **Reconciliation authority:** `.github/workflows/reconcile-vps.yml` remains the sole GitOps apply/reconciliation workflow. It owns shared GHCR pull-credential reconciliation and application rollout/health lanes. The workflow token should not receive package write/read scope; private image reads use the protected `GHCR_READ_TOKEN` only. A dedicated security PR removes unused GITHUB_TOKEN package permissions and adds contract regression coverage.
- **Promotion authority:** `.github/workflows/gitops-image-promotion.yml` remains the sole Platform-owned immutable digest promotion path. Its workflow token is for Actions/Contents/Pull Requests operations; Registry V2 package reads use `GHCR_READ_TOKEN`. No PAT fallback or second SSH/Compose deployment authority is introduced.
- **Schedule/watchdog:** `reconcile-vps.yml` cron remains `7,22,37,52 * * * *`; watchdog remains `12,27,42,57 * * * *`; `inspect-vps.yml` remains `2,32 * * * *`. The latest scheduled reconciliation/inspection histories are stale. Push watchdog smoke is warning-only; scheduled/manual/fallback enforcement remains fail-closed. No schedule expression changed.
- **TCE operations:** WF-06 retains `*/15 * * * *` and its four independent public endpoint checks; WF-12 remains a read-only Actions API monitor. WF-06 latest scheduled run #41287060151 returned HTTP 503 for TCE web/API and Auth liveness/readiness because those services remain intentionally stopped. WF-12 push smoke #41291809063 passed. No TCE market-scan schedule changed.
- **StockDividend:** application publisher #41273202844 and CI #41273202852 passed. All three Scraper/Admin/Backend immutable ARM64 digests remain verified. Production release gate is false; handoff/dispatch skipped. Weekend scraper #41284033242 remains in progress at the scraper step with no completed log artifact; preserve it until a real conclusion is available.
- **Media:** CI #41246414186 passed; latest health-only reconciliation rerun passed Media and MicroFE lanes. No newer full K3s inspection or Media publication was observed.
- **Authentication:** open PR #75/#76 remain blocked by unresolved project/environment binding and migration safety. Auth release remains manual-only; no live SSO health is claimed.
- **Private repository mirror:** `.github/workflows/mirror-locally-uncensored.yml` is a purposeful scheduled/manual mirror, not a deployment authority. Run #41292061857 failed because `secrets['Platform-infra-token']` resolved empty. The exact key and target-repository Contents-write scope are now recorded in `docs/credentials.md` and `docs/credentials-key.md`; secret presence cannot be verified by this connector.
- Preserve useful CI, tests, security, backups, manual/release, maintenance and scheduled data jobs. Do not remove the mirror or weekend scraper without confirmed redundancy/obsolescence. No production manifests, runtime credentials, release flags, database objects, or desired replicas changed. TCE market-scan schedule unchanged.


## Workflow inventory review — 2026-11-01 17:10 ICT

- **PR #968 merged:** `reconcile-vps.yml` no longer grants `packages: write`; `gitops-image-promotion.yml` no longer grants unused `packages: read` to its workflow token. Private registry reads continue exclusively through protected `GHCR_READ_TOKEN`. Regression tests enforce this separation.
- **PR #969 open:** new `recover-stale-ops.yml` is a schedule-delivery recovery controller, not a deployment authority. Cron is `10,25,40,55 * * * *`; it checks latest master workflow activity, dispatches the existing reconciliation in scheduled-safe mode only after 20m staleness, or dispatches read-only inspection after 75m staleness. It skips active runs, serializes dispatches, verifies created workflow_dispatch runs, and uses Actions write/Contents read only. It never runs SSH/kubectl/Compose or applies manifests directly.
- Existing schedule expressions remain unchanged: reconcile `7,22,37,52 * * * *`; watchdog `12,27,42,57 * * * *`; inspection `2,32 * * * *`; TCE WF-06 `*/15 * * * *`; TCE WF-12 `7,22,37,52 * * * *`. The TCE market-scan schedule is untouched.
- Platform scheduled reconciliation/inspection histories remain stale. Mirror schedule #41292061857 ran but failed because `Platform-infra-token` resolved empty; the private-repository mirror remains purposeful and is preserved. Its secret name/scope is now inventoried; secret presence is not readable by the connector.
- StockDividend publisher #41273202844 and CI #41273202852 passed with three immutable ARM64 digests; release remains disabled. Weekend scraper #41284033242 remains in progress at the scraper step without a final conclusion; preserve it pending evidence.
- TCE WF-06 #41287060151 delivered a scheduled run but public endpoints returned 503 while TCE/Auth are intentionally stopped. WF-12 push smoke #41291809063 passed. Media/MicroFE health passed in the last health-only reconciliation rerun; no newer full K3s inspection was available.
- Supabase last recorded read-only SQL probe at 09:09:08Z succeeded; no new probe in this review. Authentication PR #75/#76 remain open due unresolved project/environment binding and migration safety.
- Preserve all useful CI/test/security/backup/manual/release/maintenance/scheduled workflows. No direct SSH/Compose deployment authority was added.


## Workflow inventory review — 2026-11-01 17:12 ICT (schedule recovery merged)

- **GHCR permission boundary:** PR #968 removed unused GITHUB_TOKEN package permissions from `reconcile-vps.yml` and `gitops-image-promotion.yml`. Private package reads use the protected `GHCR_READ_TOKEN` only. Exact-head and post-merge lint/manifest checks passed.
- **Scheduled operations recovery:** PR #969 merged `recover-stale-ops.yml` with cron `10,25,40,55 * * * *`. It is a GitHub workflow dispatcher only: stale reconciliation (>20m activity) dispatches the existing `reconcile-vps.yml` with apply/image-change-disabled/all inputs; stale inspection (>75m) dispatches existing read-only `inspect-vps.yml`. It uses Actions write/Contents read, API timestamps, exact master-SHA dispatch correlation, and active-run suppression. It does not run kubectl/SSH/Compose or apply manifests directly.
- **Runtime evidence pending:** PR #969 merged at 10:11:06Z, after the 10:10 slot. First post-merge recovery slot is 10:25Z; no scheduled recovery run/dispatch observed yet. Native Platform reconcile/watchdog/inspection schedules remain stale; the fallback controller is not yet runtime-verified.
- Existing cron expressions unchanged: reconcile `7,22,37,52 * * * *`; watchdog `12,27,42,57 * * * *`; inspection `2,32 * * * *`; TCE WF-06 `*/15 * * * *`; TCE WF-12 `7,22,37,52 * * * *`. TCE market-scan schedule unchanged.
- Mirror workflow remains purposeful but failed #41292061857 because `Platform-infra-token` resolved empty. Secret scope/configuration must be supplied by the owner; do not substitute GHCR or application handoff tokens.
- StockDividend publication #41273202844 and CI #41273202852 passed; three immutable ARM64 digests are verified but promotion remains disabled. Weekend scraper #41284033242 remains in progress without a final conclusion; preserve it.
- TCE WF-06 #41287060151 produced HTTP 503 on all four public endpoints while TCE/Auth remain intentionally stopped. WF-12 push smoke #41291809063 passed; no newer WF-12 schedule run observed.
- Media CI #41246414186 passed; Media/MicroFE health passed in the last health-only reconciliation rerun; latest full runtime imageID evidence remains inspection #41275351280. Supabase SQL last succeeded at 09:09:08Z; no new probe in this review.
- Authentication PR #75/#76 remain open pending project/environment binding and migration-safety evidence. Preserve useful CI, security, backup, manual/release, maintenance and scheduled data workflows.


## Workflow inventory review — 2026-11-02 00:00 ICT (recovery runtime verified; mirror secret still absent)

### Current repository heads and PRs

- Platform Infra `0d6fd3f6e629daf4b30147f0e34421394d8ab46c`; TCE Dashboard `8882fc6dca77fc6abaaf45c673f7dfc4c8a400ae`; StockDividend `f5c04475eb4e67811c66b350d60541b21b8262c7`; Media Generation `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; none in TCE, StockDividend, or Media.

### Platform operations authority and recovery

- `reconcile-vps.yml` remains the sole GitOps apply/reconciliation authority. It owns shared GHCR pull-credential reconciliation, scoped blocked-image restarts, manifest apply, rollout and health gates.
- `inspect-vps.yml` remains read-only. `recover-stale-ops.yml` is a GitHub Actions dispatcher only; it has no SSH/kubectl/Compose/apply authority. It uses Actions write/Contents read and exact master-SHA correlation.
- Scheduled recovery #41328484657 was delivered and successfully dispatched reconciliation #41328497844 with `mode=apply`, `allow_image_changes=false`, `target_app=all`, exact master SHA `0d6fd3f6e629daf4b30147f0e34421394d8ab46c`.
- Reconciliation #41328497844 passed shared preflight/credential/cluster work and Media/MicroFE/TCE/Auth lanes; StockDividend failed on old Admin/Backend tag `12d63b4` without an ARM64 manifest. No production manifest apply or image promotion occurred.
- The post-reconciliation job dispatched recovery #41328656080. That controller verified source completion and API-clock ordering, then skipped duplicate reconciliation (age 0m) and duplicate inspection (latest inspection age 44m, under 75m). This is runtime evidence for the completed-source handoff.
- The last full inspection remains #41324734578 on prior master SHA `41bc069ba7eb68815800700cf9ae510db5544308`; its snapshot shows node Ready/ARM64, disk 54%, Media/MicroFE/NATS healthy, Stock Admin/Backend ImagePullBackOff, old Stock Frontend/Backend replicas still serving, and TCE/Auth/Keycloak 0/0.
- Native scheduled reconciliation/inspection/watchdog histories remain stale at #41300948892 / #41301947264 / #41301007488 respectively. A workflow_dispatch fallback is not proof that native cron delivery recovered.

### Mirror workflow and credential

- `mirror-locally-uncensored.yml` remains a purposeful scheduled/manual full-ref mirror, not a deployment authority. Its schedule remains `17 * * * *`.
- PR #1001 corrected the invalid hyphenated secret reference to `PLATFORM_INFRA_MIRROR_TOKEN`. Post-fix push run #41325213359 failed at preflight because that secret value is empty; no git mirror operation occurred.
- Required external configuration: target-scoped token with only `Contents: write` on `phanthienquoc/locally-uncensored-private`, stored as Platform Infra repository Actions secret or an organization secret restricted to Platform Infra. Do not substitute GHCR or app handoff tokens.
- The previous scheduled mirror run #41323952888 predates the rename; no post-fix scheduled mirror run has verified the new secret or its independent heartbeat.

### TCE and application workflows

- TCE PR #1009 added the existing scheduled WF-07 completion as a second read-only WF-12 heartbeat. Exact workflow path and `event=schedule` guards prevent manual/push runs from masquerading as schedule evidence. Post-merge WF-12 push smoke #41325592270 passed in warning-only mode but measured WF-06 #41319526719 at 71m old / 0m queue. The first post-merge scheduled WF-07 event remains pending. No TCE market-scan or existing WF-06/WF-07/WF-12 schedule changed.
- StockDividend app repo owns tests/builds and immutable GHCR publication. CI #41314359022 and publisher #41314359012 passed on `f5c04475`; three ARM64 digests are recorded in the deployment tracker. Production release remains disabled; Platform Infra has not received an authorized digest dispatch. Weekend scraper #41284033242 was cancelled after approximately six hours; preserve the workflow and diagnose the next run.
- Media CI #41246414186 passed; the latest inspection found Media backend/frontend healthy 1/1 with digest-pinned runtime images.
- Authentication CI #41033586844 and manual release #41040510320 passed on current master. Auth/Keycloak remain stopped. PR #75/#76 remain open pending the Supabase production integration side-effect review and current-head validation.

### Supabase migration source contract

- Project `gtqovpusfyyvxpeezxlo` reports `ACTIVE_HEALTHY`, PostgreSQL `17.6.1.084`.
- Read-only ledger/source comparison: 84 remote migration rows, 84 local SQL files, 84 exact version/name matches, no remote-only/local-only versions, and no duplicate local prefixes. Latest matching version is `20261028020259_revoke_browser_access_from_tce_data_api`.
- Current source/ledger version-set alignment passes; this does not prove historical deployment errors are cleared or authorize a production migration/deploy. No database writes were performed.

### Preservation rules

- Keep CI/test/security, backup, manual/release, maintenance and purposeful scheduled data workflows.
- Preserve reconciliation as the sole GitOps apply authority, inspection as read-only, and recovery/watchdog as API-only dispatch/monitoring.
- No direct SSH/Compose deployment authority, no production image promotion, and no changes to TCE market-scan scheduling.


## Workflow inventory review — 2026-11-02 00:59 ICT

- **Platform native reconciliation:** scheduled run #41330228681 was delivered on schedule and completed with an overall failure only at the StockDividend health gate (old Admin/Backend tag `12d63b4`, missing ARM64 manifest). Shared reconciliation, GHCR preflight, runtime Secret verification, pull-credential bootstrap, cluster verification, and other application lanes passed. Production manifest apply and image-change guard were skipped. `reconcile-vps.yml` remains the only GitOps apply authority.
- **Platform inspection:** scheduled run #41330407550 succeeded at 17:13:57Z and produced the fresh snapshot at 17:14:04Z. The inspection automation exact-head validated and squash-merged PR #1005, resulting in master SHA `751d0bb5637f8d92776fb8c8ceae116509005fc0`. `inspect-vps.yml` remains read-only with respect to production workloads; its repository snapshot PR is separate from cluster mutation.
- **Recovery/watchdog:** post-inspection recovery #41330518351 and workflow_run watchdog #41330518388 both succeeded. Recovery skipped duplicate dispatches because reconcile/inspection were fresh. Watchdog measured reconcile age 3m / queue 0m (conclusion failure due StockDividend health) and inspection age 1m / queue 0m (success). This is native schedule-delivery evidence, not proof of long-term cadence stability. Recovery remains an Actions API dispatcher only; watchdog remains read-only.
- **TCE:** current master is `8882fc6dca77fc6abaaf45c673f7dfc4c8a400ae`. Latest scheduled WF-06 #41319526719 is 15:06:39Z; WF-07 #41311225433 is 13:26Z on the pre-#1009 SHA; WF-12 #41315132135 is 14:13:39Z. WF-12 push smoke #41325592270 is not schedule evidence. The exact WF-07 workflow path is `.github/workflows/wf-07-tce-integration-check.yml`, and the WF-12 guard/test assert that path correctly. No post-merge scheduled WF-07 heartbeat was observed. Preserve WF-06/WF-07/WF-12 and market-scan cron declarations unchanged.
- **StockDividend:** master `f5c04475`; CI #41314359022 and immutable native ARM64 publisher #41314359012 passed. The three verified Scraper/Admin/Backend digests remain recorded in the deployment tracker. Production release gate remains false; no repository_dispatch or GitOps promotion occurred. Production Admin/Backend still reference non-ARM64 `12d63b4`; frontend/old backend replicas are serving old images. Weekend scraper #41284033242 was cancelled after approximately six hours, with no evidence explaining the cancellation; retain the scheduled/manual job.
- **Media:** master `d8e695d7`; CI #41246414186 passed. Fresh inspection shows Media backend/frontend 1/1 with pinned runtime imageIDs.
- **Authentication:** master `ceb2688d`; PRs #75/#76 remain open. PR #76 current-head CI #41329425940 passed. Previously recorded Supabase migration ledger/source comparison is 84/84 exact version/name matches, but it was not re-run in this review and does not clear the production integration side-effect gate. Auth/Keycloak remain stopped.
- **Mirror:** `mirror-locally-uncensored.yml` remains a purposeful hourly/manual full-ref mirror. It references `PLATFORM_INFRA_MIRROR_TOKEN`; post-fix push smoke #41325213359 failed before Git operations because the secret was empty. No later post-fix scheduled mirror run was observed. Require destination-only Contents:write on `phanthienquoc/locally-uncensored-private`; do not substitute GHCR or app release tokens.
- Preserve useful CI, test, security, backup, manual/release, maintenance, cleanup, and scheduled data workflows. No direct SSH/Compose deployment authority, production image promotion, production manifest change, credential mutation, database write, image deletion, or TCE market-scan schedule change occurred.


## Workflow inventory review — 2026-11-02 08:00 ICT

- **Runner bootstrap and reconciliation:** bootstrap #41360807367 installed `rollout-status-v13-permanent-image-pull-restart`. Scheduled reconciliation #41369624425 passed the live policy-version gate and the helper explicitly skipped restart for permanent Stock Admin/Backend ARM64 manifest errors. This verifies runner v13 behavior on the VPS. The reconciliation's StockDividend health lane still fails; manifest apply and image-change guard were skipped. Preserve `bootstrap-runner.yml` as the only runner-helper installation authority.
- **Inspection and freshness watchdog:** scheduled inspection #41370072870 succeeded, generated `debug/vps-latest.md` at 00:59:35Z, and exact-head validated/squash-merged PR #1023 (merge commit `4ab19043a110f2328609a58066dce52e15c8009c`). Exact-head validation #41370136730 passed. Scheduled watchdog #41369864119 correctly failed before that inspection because the last scheduled inspection was 215m old; post-inspection recovery #41370192192 and watchdog #41370192224 succeeded. Continue distinguishing native schedule delivery from fallback/workflow_run activity.
- **K3s:** node `tce-k3s-01` Ready, ARM64, K3s v1.36.3+k3s1, disk 55%, available memory ~19Gi, `restart_required=yes`. Media and MicroFE/NATS healthy. Stock Admin/Backend new Pods remain 0/1 due permanent `no match for platform in manifest`; restart count 0 confirms v13 suppression. TCE/Auth/Keycloak remain intentionally stopped. No reboot/package upgrade.
- **TCE cross-repo heartbeat:** three real source→WF-12→Platform receiver chains were accepted: WF-07 schedule #41355068024; direct WF-12 schedule #41358488421; WF-06 schedule #41360343131. Platform receiver runs #41355088547, #41358495488, #41360370906 validated source run metadata against GitHub Actions API. Reconciliation runs #41355101409, #41358507981, #41360385108 retained Platform-only apply authority with image changes disabled. WF-06 application health failure (503 while scale-to-zero) is not a heartbeat-delivery failure. Do not change WF-06/WF-07/WF-12 or market-scan cron declarations.
- **StockDividend:** native ARM64 immutable publisher #41314359012 and CI #41314359022 passed; promotion gate remains false. Production Admin/Backend tags remain old and unsupported on ARM64. Keep the health gate; do not promote without explicit authorization. Permanent image-pull restart is now suppressed rather than retried/restarted.
- **Media:** master `d8e695d7`; CI #41246414186 passed; inspected backend/frontend 1/1 with digest-pinned runtime.
- **Authentication:** master `ceb2688d`; PR #75/#76 remain open (PR #75 exact-head CI #40446492086 PASS; PR #76 #41329425940 PASS). Both remain blocked by Supabase integration side-effect review. Keep Auth/Keycloak stopped.
- **Mirror:** scheduled run #41368359234 failed before Git operations because `PLATFORM_INFRA_MIRROR_TOKEN` was empty/missing. Preserve the scheduled/manual mirror workflow; require destination-only Contents:write for `phanthienquoc/locally-uncensored-private`.
- **Open PR inventory:** Platform Infra #795/#749/#741/#648/#544/#541/#539/#538; Authentication #75/#76; no open PRs in TCE Dashboard, StockDividend, or Media Generation.
- Preserve CI, tests, security, backup, manual/release, maintenance, cleanup, and scheduled data workflows. `reconcile-vps.yml` remains the only GitOps apply authority; `inspect-vps.yml` remains read-only; recovery/watchdogs only dispatch/observe. No direct SSH/Compose authority, image promotion, manifest mutation, credential mutation, database write, or market-scan schedule change occurred.


## Workflow inventory review — 2026-11-02 09:02 ICT

- TCE heartbeat: scheduled WF-12 #41374853407 failed only its WF-06 freshness check but successfully sent the independent Platform heartbeat. Platform receiver #41374862392 passed external source-run metadata validation and triggered reconciliation #41374875325. Post-reconciliation recovery #41375036768 succeeded. This is a verified cross-repo fallback chain; it is not evidence that native Platform cron delivery resumed.
- Platform native schedules: latest scheduled reconciliation #41369624425 (00:54:06Z), latest scheduled inspection #41370072870 (00:59:28Z). The later #41374875325 reconciliation was workflow_dispatch. Keep cron expressions unchanged and continue distinguishing schedule from repository_dispatch/workflow_run/workflow_dispatch.
- Platform reconciliation: #41374875325 passed shared preflight, v13 policy gate, GHCR access, runtime Secret, shared pull credentials, scoped helper and cluster verification. MicroFE/TCE/Auth/Media lanes passed; StockDividend alone failed on old Admin/Backend image 12d63b4 without ARM64 manifest. No manifest apply/image promotion.
- Runner v13: #41369624425 logged permanent image-pull restart suppression for Stock Admin and Backend. Inspection #41370072870 showed the same failing pods with restart count 0. Bootstrap remains the only runner-helper installation authority.
- TCE WF-06 PR #1011 removes the informational legacy SSH/Docker/port probe while retaining the 15-minute schedule, manual dispatch and four public endpoint smoke checks. Workflow token permissions are empty. Contract tests now forbid VPS SSH/Docker/legacy port probes in WF-06. Prettier passed; Backend unit tests were still running at review. Do not merge until exact-head required checks pass. WF-12 and its TCE-to-Platform heartbeat contract are unchanged.
- Preserve: WF-06 schedule and public smoke; WF-07 backup/integration; WF-12 watchdog/heartbeat; TCE cleanup, audit, safe-setup and bootstrap jobs; Platform reconcile, read-only inspection, recovery/watchdogs, mirror, security and maintenance workflows. No TCE market-scan schedule changed.
- Application state: StockDividend immutable ARM64 publisher/CI remain successful, but production release remains disabled. Media CI remains successful and last inspected runtime was healthy. Authentication #75/#76 remain open pending production integration side-effect review. Mirror remains blocked by missing PLATFORM_INFRA_MIRROR_TOKEN.

No direct SSH/Compose deployment authority was added. The proposed WF-06 cleanup removes only a redundant informational read-only SSH probe from the application health workflow; Platform Infra retains the sole K3s/VPS inspection path.


### Follow-up — TCE WF-06 boundary PR merged (2026-11-02 09:05 ICT)

- TCE PR #1011 was merged by squash at 2026-11-02 02:05:27Z. Validated head: a2da2271c24794d1d88286c9c11b129205dbb47f; merge commit / new TCE master: a5e8866d2ba28936d57b31ce6a067186c7204369.
- Exact-head Prettier run #41375696971 passed, including the WF-06/WF-12 contract validator. Exact-head Backend unit tests #41375696882 passed, including backend build and unit tests. The merge was performed only after re-fetching the PR and confirming its head was unchanged.
- Post-merge WF-01 build #41375826672, WF-02 #41375826954, and WF-05 #41375826811 were still in progress at this follow-up. No post-merge success is claimed yet.
- WF-06 retains its 15-minute schedule, manual dispatch and four public endpoint checks, but no longer requires VPS_SSH_PRIVATE_KEY or performs legacy Docker/port inspection. Platform Infra remains the read-only VPS/K3s inspection authority. WF-12 and all TCE schedule declarations, including market-scan, are unchanged.


### Follow-up — post-merge validation status (2026-11-02 09:08 ICT)

- Platform PR #1025 merged by squash at 02:06:28Z, merge commit 9c1b4c09844190102c66ca2a62c2423946be5ab8. Exact-head manifest validation #41375873258 passed; post-merge manifest validation #41375916620 also passed.
- TCE PR #1011 remains merged at a5e8866d2ba28936d57b31ce6a067186c7204369. Exact-head Prettier/contract validation #41375696971 and Backend build/unit tests #41375696882 passed. Post-merge WF-02 #41375826954 and WF-05 #41375826811 passed. Post-merge WF-01 Build Verify #41375826672 was still building the frontend image at this review; do not claim full post-merge build completion until it concludes.
- No post-merge scheduled WF-06/WF-07/WF-12 event has yet been observed after TCE master advanced to a5e8866d. The next scheduled event must be checked separately from push-triggered CI.
- Current Platform master at branch creation: 9c1b4c09844190102c66ca2a62c2423946be5ab8. TCE master: a5e8866d2ba28936d57b31ce6a067186c7204369. StockDividend, Media and Authentication heads remain f5c04475, d8e695d7 and ceb2688d respectively.


## Workflow inventory update — 2026-11-02 13:55 ICT / 06:55 UTC

- Current master heads: Platform Infra ba61586003986886e3f6ebf95471080b1be96cf1; TCE a5e8866d2ba28936d57b31ce6a067186c7204369; StockDividend 38220ddfef2db7128482547f72b7f06211e9c9bc; Media d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PR inventory: Platform #795/#749/#648/#544/#541/#539/#538; Authentication #75/#76; no open PRs in TCE, StockDividend or Media.
- Latest Platform schedule events: recovery controller #41400302676 at 06:30Z succeeded and dispatched reconciliation #41400322459 after the prior reconciliation exceeded the 20-minute freshness budget. Reconciliation #41400322459 failed only on StockDividend Admin/Backend health. Latest native schedule events for reconcile/watchdog/inspection/mirror remain #41369624425/#41369864119/#41370072870/#41368359234. Fallback workflow_dispatch and inspection snapshot runs are not native schedule deliveries.
- Latest inspection: #41400552231 generated debug/vps-latest.md at 06:32:37Z and was committed by automated PR #1043 as ba61586003986886e3f6ebf95471080b1be96cf1. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available, runner policy v14 live, GitOps drift clean, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend pods ImagePullBackOff on old tag 12d63b4; old Backend and legacy Frontend 1/1; TCE/Auth/Keycloak 0/0.
- Runner/reconciliation authority: bootstrap-runner.yml remains the only runner-helper installer. reconcile-vps.yml remains the sole GitOps apply authority; latest run #41400322459 verified v14, GHCR pull access and shared credentials, found no drift and skipped manifest apply with allow_image_changes=false. Permanent ARM64 image-pull failures are not restarted; the StockDividend health gate still fails honestly.
- Recovery: #41400522412 correlated the exact source reconciliation #41400322459 and completed successfully. Recovery schedule is active; native reconcile/inspection schedule delivery remains stale.
- TCE: WF-06 remains public-endpoint-only, no SSH/Docker/Compose inspection. Latest scheduled WF-07 #41397768048 passed; latest scheduled WF-06 #41378060687 and direct WF-12 #41374853407 remain stale. Workflow-run forwarder #41397785851 sent the authenticated heartbeat successfully while its independent WF-06 freshness check failed. Platform receiver #41397794672 passed source validation. Keep all TCE schedule expressions and market-scan cadence unchanged.
- StockDividend producer/consumer: producer run #41397317600 verified paired full-SHA immutable linux/arm64 images and digests recorded in the tracker. Platform promotion consumer requires STOCKDIVIDEND_ACTIONS_READ_TOKEN to verify the private publisher run. Secret presence remains unverified; release gate remains false, so no dispatch or promotion. Keep app-owned tests/builds/publication separate from Platform-owned production manifests and rollout.
- Mirror: PLATFORM_INFRA_MIRROR_TOKEN remains missing/empty; destination-only Contents:write for phanthienquoc/locally-uncensored-private is an owner action.
- Media/Auth: Media CI #41246414186 passed and inspected backend/frontend remain 1/1. Auth PR #75/#76 remain open pending production integration side-effect and migration-drift review. No database mutation or current Supabase health claim.
- Preserve CI, build/test/security, backup, manual/read-only, release, maintenance and scheduled workflows. No duplicate direct SSH/Compose deployment authority. No production manifests, credentials, release gate, desired replicas or schedule changes.


## Workflow inventory update — 2026-11-02 15:15 ICT / 08:15 UTC

- **Platform scheduled reconciliation:** #41407522742 (schedule, 07:37:40Z) completed with failure only in the StockDividend health lane. Shared preflight, live runner v14 gate, GHCR pull access, Auth runtime Secret, shared pull credentials, scoped restart helper and cluster verification passed. GitOps drift was clean; manifest apply/image-change guard skipped with `allow_image_changes=false`. The helper logged permanent-error suppression for Admin/Backend tag `12d63b4` (`no match for platform in manifest`), and did not restart them. Health gate correctly failed on Admin and new Backend ImagePullBackOff Pods.
- **Platform inspection:** #41407411326 (schedule, 07:36:38Z) succeeded and produced `debug/vps-latest.md` at 07:36:46Z. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available, runner policy v14 live, GitOps drift clean, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin two Pods and new Backend Pod ImagePullBackOff; old Backend and unmanaged legacy Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **Platform watchdog/recovery:** scheduled watchdog #41406983213 failed at 07:32:45Z because the prior scheduled reconcile #41369624425 was 398m old and inspection #41370072870 was 393m old. After #41407411326/#41407522742, workflow_run watchdog #41407838302 and recovery workflow_dispatch #41407806939 both passed. This confirms the stale alert/recovery path but does not prove subsequent native cron cadence. The current schedule-filtered history shows one new scheduled inspection/reconcile pair; further expected ticks were not present at this review.
- **Platform mirror:** scheduled run #41407613563 failed before clone/push because `MIRROR_TOKEN` was empty; log explicitly reports missing `PLATFORM_INFRA_MIRROR_TOKEN`. Keep the scheduled/manual full-ref mirror workflow. Owner must provide destination-only Contents:write for `phanthienquoc/locally-uncensored-private`.
- **TCE:** latest scheduled WF-07 integration #41397768048 (06:05:28Z) passed. Latest scheduled WF-06 #41378060687 (02:30:05Z) and direct scheduled WF-12 #41374853407 (01:54:04Z) remain stale. WF-12 workflow_run #41397785851 sent heartbeat successfully but its WF-06 freshness job failed; Platform receiver #41397794672 validated the WF-07 source. WF-06 cron remains `*/15 * * * *`; WF-12 remains `7,22,37,52 * * * *`. Keep the four public checks strict while TCE/Auth are intentionally stopped; do not change any schedule, especially market-scan.
- **StockDividend:** master CI #41397317588 and immutable publisher #41397317600 passed. Three paired full-SHA ARM64 digests remain recorded in the tracker. Private publisher provenance consumer still requires protected `STOCKDIVIDEND_ACTIONS_READ_TOKEN`; presence is unverified. Production release gate remains false/unset; no dispatch or promotion.
- **Media:** master CI #41246414186 passed; inspection confirms backend/frontend 1/1 and digest-pinned.
- **Authentication:** master CI #41033586844 and manual release #41040510320 passed. PR #75 head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` CI #40446492086 passed; PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` CI #41329425940 passed and remains draft. Keep both gated on production Supabase integration side effects and migration-drift review.
- **Open PR inventory:** Platform Infra #795/#749/#648/#544/#541/#539/#538; Authentication #75/#76; no open PRs in TCE, StockDividend or Media. Platform PR #541/#538 remain draft; no PR was merged in this run.
- Preserve CI, build/test/security, backup, manual/read-only, release, maintenance, cleanup and scheduled data workflows. `reconcile-vps.yml` remains the sole GitOps apply authority; `inspect-vps.yml` remains read-only; recovery/watchdog remain API dispatch/observation only. Bootstrap remains the only runner-helper installation authority. No direct SSH/Compose deployment authority, production manifest/image change, credential mutation, database write, desired replica change, schedule change, image deletion or VPS reboot occurred. Documentation-only PR #1046 was subsequently squash-merged after exact-head and post-merge validation passed; no application or production PR was merged.


## Follow-up — PR #1046 post-merge evidence (2026-11-02 15:18 ICT / 08:18 UTC)

- Documentation PR #1046 was squash-merged at `9c4f4d1ccac7485b1e656fb23af7081d9d148afa` after exact-head #41411976727 PASS. Post-merge `validate-manifests` #41412028919 passed on the merge SHA. No production manifest or workflow changed.
- Schedule-filtered history was rechecked after merge. Latest Platform native inspection/reconcile/watchdog/mirror remain #41407411326/#41407522742/#41406983213/#41407613563. Latest TCE native WF-07/WF-06/WF-12 remain #41397768048/#41378060687/#41374853407. Do not treat workflow_run or workflow_dispatch recovery as native cron delivery.
- The mirror remains blocked by empty `PLATFORM_INFRA_MIRROR_TOKEN`; StockDividend private provenance remains gated on `STOCKDIVIDEND_ACTIONS_READ_TOKEN` and explicit release authorization. Stock Admin/Backend are still unhealthy on old non-ARM64 tag `12d63b4`; runner v14 continues to suppress permanent-error restarts.
- No application PR was merged, no promotion or production mutation occurred, and no TCE schedule/market-scan cadence changed.


## Workflow inventory update — 2026-11-02 17:59 ICT / 10:59 UTC

- **Repository heads/open PRs:** Platform Infra `4e777cb00dc3290f4a8daf372b1c6619553e5c01`; TCE `a5e8866d2ba28936d57b31ce6a067186c7204369`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`. Open PRs: Platform #795/#749/#648/#544/#541/#539; Auth #75/#76; none in TCE, StockDividend or Media. Platform #544/#541/#539 and Auth #76 are drafts; #538 is closed as superseded. All eight current PR heads have successful PR-triggered workflow runs: Platform #795 #40970075264, #749 #40316261650, #648 #39546799280, #544 #38575430454, #541 #38567431761, #539 #38548718033; Auth #75 #40446492086 and #76 #41329425940. Do not interpret old successful CI as approval for production activation or as proof that draft docs are merge-ready.
- **Platform validation:** master push validation #41425988844 (10:05:51Z, SHA 4e777cb0...) passed all steps, including production render, Auth rendered GitOps contract, Keycloak isolated manifests and network boundaries. Changed-image check was skipped for documentation-only merge.
- **Platform native schedule history:** latest schedule events through 10:59Z are inspection #41407411326 (07:36:38Z, success), reconciliation #41407522742 (07:37:40Z, failure only StockDividend health), watchdog #41406983213 (07:32:45Z, stale delivery), mirror #41407613563 (07:38:31Z, missing token), recovery #41400302676 (06:30:13Z, success). No later native schedule events were returned. Recovery/workflow_dispatch/repository_dispatch/push/workflow_run are not native cron evidence.
- **Platform runtime:** latest reconciliation #41424991858 (workflow_dispatch, 09:58:33Z) passed shared runner v14, GHCR pull and Auth Secret preflight; drift clean, apply skipped with allow_image_changes=false. TCE/Media/MicroFE/Auth lanes passed; Keycloak skipped; StockDividend lane failed on Admin and new Backend ImagePullBackOff with `no match for platform in manifest` for tag `12d63b4`. Runner v14 skips permanent-error restart. Recovery #41425271774 verified the source and avoided duplicate dispatch because inspection/reconciliation were fresh at 10:00Z.
- **TCE schedule:** WF-06 schedule #41424898130 (09:57:51Z) ran but all four public endpoints returned HTTP 503 vs expected 200. Direct scheduled WF-12 #41419694332 (09:19:29Z) had WF-06 freshness failure but heartbeat dispatch succeeded. WF-12 workflow_run #41424938817 (09:58:09Z), triggered by WF-06 completion, passed freshness verification and heartbeat; Platform receiver #41424970499 independently validated source path, schedule event, source/heartbeat IDs and full SHA. Latest scheduled WF-07 integration #41397768048 (06:05:28Z) passed. One WF-06 tick resumed; sustained cadence remains unproven. Keep all TCE cron expressions and market-scan schedule unchanged.
- **K3s:** inspection #41419270996 snapshot at 09:16:30Z: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB memory available, runner policy v14, GitOps drift clean, restart_required=yes. Later Pod listing from #41424991858 confirms Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Backend and unmanaged legacy Frontend 1/1; TCE/Auth/Keycloak 0/0. No reboot.
- **StockDividend:** CI #41397317588 and publisher #41397317600 passed with previously recorded immutable ARM64 Scraper/Admin/Backend digests. Release flag remains false/unset; no dispatch/promotion. `STOCKDIVIDEND_ACTIONS_READ_TOKEN` presence unverified; owner action is StockDividend-only Actions:read in protected Platform production Environment.
- **Mirror:** #41407613563 failed before Git operations because `PLATFORM_INFRA_MIRROR_TOKEN` is empty/missing. Owner action: destination-only Contents:write for `phanthienquoc/locally-uncensored-private`. Preserve the hourly/manual full-ref mirror workflow.
- **Media/Auth:** Media CI #41246414186 passed; backend/frontend 1/1 and digest-pinned. Auth master CI #41033586844 and manual release #41040510320 passed; PR #75/#76 current-head CI passed, but retain production Supabase side-effect and migration provenance/drift gates. No database mutation.
- Preserve useful CI/test/security, build/publish, backup, manual read-only, release, maintenance, cleanup, mirror and scheduled jobs. `reconcile-vps.yml` remains the sole GitOps apply authority; `inspect-vps.yml` read-only; recovery/watchdog observe/dispatch only; runner bootstrap remains sole helper installation authority. No direct SSH/Compose deployment authority added. No production manifest, credential, release gate, desired replica or schedule change.


## Post-merge follow-up — PR #1054 (2026-11-02 18:02 ICT / 11:02 UTC)

- Documentation PR #1054 merged as `d2b78091cf1978cfa4982b2225659881328e4d83` from exact head `43dab98ea5b68dffb99ba6663262c15d97a37d11`. Exact-head validation #41433478071 and post-merge validation #41433569946 both passed.
- Re-queried native schedule events after merge: no newer Platform inspection/reconcile/watchdog/mirror/recovery schedule runs; latest remain #41407411326/#41407522742/#41406983213/#41407613563/#41400302676. TCE latest direct scheduled WF-06/WF-12/WF-07 remain #41424898130/#41419694332/#41397768048. Do not count workflow_run, repository_dispatch or workflow_dispatch as cron delivery.
- WF-06 still runs strict HTTP 200 public checks and currently fails HTTP 503 while TCE/Auth are intentionally scale-to-zero. WF-12 workflow_run #41424938817 forwarded the WF-06 schedule heartbeat successfully and Platform receiver #41424970499 validated it; sustained schedule cadence is not proven.
- No production workflow, manifest, credential, release gate, desired replica, or cron expression changed. TCE market-scan schedule unchanged.


## Workflow inventory review — 2026-11-02 19:03 ICT / 12:03 UTC

- Platform master 4f6b7c9e97915112dc7da2029af862b147c4422b; TCE a5e8866d2ba28936d57b31ce6a067186c7204369; StockDividend 38220ddfef2db7128482547f72b7f06211e9c9bc; Media d8e695d772ab2dc0da5c15cc428ee78ac6537518; Authentication ceb2688d6277b10f1bfe7652223d1d295b7e49d9.
- Open PRs: Platform #795/#749/#648/#544/#541/#539; Auth #75/#76; none in TCE, StockDividend or Media. Drafts: Platform #544/#541/#539 and Auth #76. All eight open PR heads have successful PR-triggered validation runs; see deployment tracker for exact run IDs. PR #1055 merged and Platform master push validation #41433739946 passed.
- Native Platform schedule history remains stale after inspection #41407411326 (07:36:38Z), reconcile #41407522742 (07:37:40Z), watchdog #41406983213 (07:32:45Z), mirror #41407613563 (07:38:31Z), scheduled recovery #41400302676 (06:30:13Z). The 09:58Z reconciliation #41424991858 and recovery #41425271774 were workflow_dispatch, not native cron.
- TCE native history: WF-06 #41424898130 (09:57:51Z, scheduled but public HTTP 503 failures); direct WF-12 #41419694332 (09:19:29Z, stale WF-06 freshness but independent heartbeat success); WF-07 integration #41397768048 (06:05:28Z, success). WF-12 workflow_run #41424938817 and Platform receiver #41424970499 successfully verified/forwarded one WF-06 scheduled source, but are not direct schedule ticks. No sustained cadence proven.
- Current schedule definitions remain staggered: Platform inspect 2,32; reconcile 7,22,37,52; watchdog 12,27,42,57; mirror 17 each hour. TCE WF-06 every 15m; WF-12 minutes 7,22,37,52; WF-07 integration minute 17 every six hours. Do not change any TCE schedule or market-scan cadence.
- Schedule diagnosis: Platform watchdog logs confirmed reconcile and inspection workflows active; TCE WF-12 confirmed WF-06 active. Workflow files are on default branch. Recent cron-changing commits were authored by phanthienquoc. No job was created for missing Platform ticks, so evidence points to schedule event delivery rather than self-hosted runner queue. GitHub documentation permits schedule delays/dropped events under load and notes default-branch/associated-actor requirements; current evidence does not identify a definitive scheduler-side cause. Preserve strict freshness/health checks; no speculative cron change.
- Runner v14 remains live. Latest full K3s snapshot #41419270996 is a workflow_dispatch inspection generated 09:16:30Z; later Pod inventory #41424991858 at 09:59Z confirms Media/MicroFE/NATS 1/1, Stock Admin and new Backend ImagePullBackOff on old tag 12d63b4 (no match for platform in manifest), old Backend and unmanaged legacy Frontend 1/1, TCE/Auth/Keycloak 0/0. No reboot/upgrade.
- StockDividend CI #41397317588 and immutable publisher #41397317600 passed with paired ARM64 digests already recorded in the deployment tracker. Release remains disabled; STOCKDIVIDEND_ACTIONS_READ_TOKEN presence unverified. Mirror #41407613563 failed before clone/push because PLATFORM_INFRA_MIRROR_TOKEN is missing. Owner actions remain separate and least-privileged.
- Media CI #41246414186 passed; last inspected backend/frontend were 1/1 and digest-pinned. Auth master CI #41033586844 and release #41040510320 passed; PR #75/#76 CI passed but remain gated on Supabase production side effects and migration provenance/drift.
- Preserve CI/test/security, build/publish, backup, cleanup, manual/read-only, release, maintenance, mirror, recovery, watchdog and scheduled data workflows. reconcile-vps.yml is the only GitOps apply authority; inspect-vps.yml read-only; recovery/watchdog observe/dispatch only; bootstrap remains sole runner-helper installer. No duplicate direct SSH/Compose authority.
- No production manifest, image reference, GHCR credential, database object, release flag, desired replica, or schedule was changed. TCE market-scan schedule unchanged.


## Post-merge follow-up — PR #1056 (2026-11-02 19:08 ICT / 12:08 UTC)

- PR #1056 merged by squash at b21273aca77193bd804a11b81247d05e10be3a7d from exact validated head 2fd73e4d033bf64b4dfe511384d7c555f74bbf5d.
- Exact-head validate-manifests #41442121813 and post-merge validate-manifests #41442209197 both completed SUCCESS.
- Schedule-run actor metadata for the latest observed Platform and TCE scheduled events is phanthienquoc for both actor and triggering_actor. No evidence of actor deprovisioning was found; scheduler-side delivery remains unresolved.
- Documentation-only change. No production workflow, manifest, image, credential, release flag, database object, desired replica or cron expression changed. TCE market-scan schedule unchanged.


## Workflow inventory follow-up — 2026-11-02 (post-merge repository inspection)

### Repository and PR inventory
- Platform master: `e1275b3fcbd05294df1ce61251f4377e13fccf31`; TCE: `a5e8866d2ba28936d57b31ce6a067186c7204369`; StockDividend: `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media: `d8e695d772ab2dc0da5c15cc428ee78ac6537518`; Authentication: `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Platform #749/#648/#795 merged by squash after exact-head verification; post-merge validation runs #41450146520/#41450175573/#41450197662 all SUCCESS. #749 replaces captured Kubernetes/firewall output with a cautious WireGuard guide; #648 adds repository agent preflight rules; #795 documents the limits of the role smoke test.
- Remaining open PRs: Platform #544/#541/#539 (draft); Auth #75 (open), #76 (draft). Current-head validate checks are SUCCESS; Auth Supabase Preview checks are SKIPPED. TCE, StockDividend and Media have no open PRs.
- Latest Platform master check: validate-manifests #41450197662 on `e1275b3`, SUCCESS.

### Workflow ownership and schedule evidence
- `reconcile-vps.yml` remains the only GitOps apply authority. `inspect-vps.yml` remains read-only and snapshot-producing. Recovery/watchdog workflows only observe, correlate source runs and dispatch the existing authorities. Runner bootstrap remains the sole installer of the `platform-kubectl` helper/policy. No duplicate SSH/Compose deployment authority was introduced.
- Native Platform schedule runs remain inspection #41407411326, reconciliation #41407522742, watchdog #41406983213, mirror #41407613563 and scheduled recovery #41400302676. No newer native schedule run appeared in the latest 100-run history through the post-merge validation. The latest reconciliation's failure is still isolated to StockDividend health; mirror still fails because its token is absent.
- TCE latest native schedule runs remain WF-06 #41424898130, direct WF-12 #41419694332 and WF-07 #41397768048. WF-06 created one scheduled tick but failed four strict public HTTP 200 checks with HTTP 503. WF-12 workflow_run #41424938817 forwarded the WF-06 heartbeat; Platform receiver #41424970499 verified source and heartbeat IDs/SHA. Do not count these event types as direct schedule ticks.
- Official GitHub troubleshooting guidance documents schedule delay/drop under Actions load, default-branch requirements, and associated-actor deprovisioning. Last observed actor is `phanthienquoc`; root cause remains unresolved. Preserve existing cron declarations and strict health assertions; do not alter TCE market-scan schedule.

### Application and production boundaries
- StockDividend app CI/publisher remain successful on master; three immutable ARM64 digests are already recorded in this inventory. Production still references old tag `12d63b4`, causing Admin/new Backend ImagePullBackOff. Release remains disabled pending explicit authorization and owner configuration of `STOCKDIVIDEND_ACTIONS_READ_TOKEN`.
- Mirror requires `PLATFORM_INFRA_MIRROR_TOKEN`, destination-only Contents:write on `phanthienquoc/locally-uncensored-private`; latest schedule #41407613563 failed before Git operations.
- Media last CI #41246414186 passed; last inspected backend/frontend 1/1 and digest-pinned. Auth PR #75/#76 remain blocked by Supabase production side-effect and migration provenance/drift review; no database changes.
- Latest K3s snapshot #41419270996 is generated 09:16:30Z and is stale at this update. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available, runner v14, GitOps drift clean, host restart_required=yes. Last-known workload inventory is unchanged from the deployment tracker; obtain fresh read-only inspection before asserting current health.

### Preservation
Preserve useful CI/test/security, build/publish, backup, cleanup, manual/read-only, release, maintenance, mirror, recovery, watchdog and scheduled data workflows. No production manifest, image reference, GHCR credential, database object, release flag, desired replica or schedule changed. TCE market-scan schedule unchanged.


## Post-merge verification — PR #1058 (2026-11-02)

- PR #1058 merged as `73bfe6e63699352e73007d1e00300efd2dd2eed2` from exact head `60330bc4195ed8093dfda28a21acfebf64bbd422`.
- Exact-head run #41450382752 and post-merge run #41450454704 both completed SUCCESS. All manifest, image, secret, Auth, Keycloak and network-boundary validation steps passed; changed-image validation was correctly skipped for this documentation-only PR.
- The PR changed only the deployment tracker and workflow inventory. No production workflow/manifest/credential/image/replica/schedule was changed.
- Current Platform open PRs: #544/#541/#539. Authentication: #75/#76. No open PRs in TCE, StockDividend or Media. TCE market-scan schedule unchanged.


## Media publisher provenance contract — merged 2026-11-02

- Producer: `phanthienquoc/media-generation/.github/workflows/wf-03-media-production-deploy.yml`.
  - App repository owns frontend/backend build, GHCR publication, immutable digest resolution and ARM64 verification.
  - Paired `media-images-published` payload now contains `app`, `commit`, `release`, `frontend_digest`, `backend_digest`, `source_run_id`, `source_workflow_path`, `source_event`, and `source_head_sha`.
  - Source event is limited to `push` or `workflow_dispatch`; source branch is master; release tag ends in the full 40-character source SHA.
  - Producer PR #67 exact-head CI #41460676531 PASS; merge commit `0d4fc2ac15834c20357fd2420b732e6411fd8930`; post-merge master CI #41460906654 PASS.
- Consumer: `platform-infra/.github/workflows/gitops-image-promotion.yml`.
  - Resolves and validates all four provenance fields before promotion.
  - Runs `scripts/verify-media-publisher-run.sh` before GHCR image validation or GitOps PR creation.
  - Verifier reads the public Media Actions run endpoint without a cross-repository credential and checks exact run ID, repository, head repository, workflow path, event, master branch, full head SHA, completed status and successful conclusion.
  - Regression tests: `scripts/tests/verify-media-publisher-run.test.sh`; executed by `validate-github-actions.yml`.
  - Static workflow contract validation asserts the provenance step precedes GHCR validation and no cross-repo credential is introduced.
  - Platform PR #1060 exact-head #41460750901 (workflow/lint/contracts) and #41460750395 (manifest render/contracts) PASS; merge commit `abe384ba89e09669a3273141d76815d44409cc5c`; post-merge #41460929753/#41460929860 PASS.
- Merge order was producer #67 first, consumer #1060 second. Legacy Media payloads without provenance are rejected by the consumer.
- No new Media Actions token is required while the source repository remains public. If visibility changes to private, fail closed and add a dedicated read-only credential before release.
- No Media release was dispatched by these workflow-only changes; no production image or manifest changed.

## Runtime evidence — reconciliation #41460962292 (2026-11-02 14:20Z)

- Invocation: post-merge recovery `workflow_dispatch`, `target_app=all`, `mode=apply`, `allow_image_changes=false`.
- Shared preflight SUCCESS, runner v14 ready, GHCR access PASS, Auth Secret/pull-credential bootstrap steps PASS, Media digest refs resolved, drift false, manifest apply skipped.
- Node Ready, K3s v1.36.3+k3s1, Ubuntu 22.04.5 ARM64, containerd 2.3.2-k3s2.
- Media, MicroFE and NATS healthy; Auth lane PASS with rollout intentionally skipped; TCE GitOps image pair and scale-to-zero health PASS; Keycloak skipped.
- StockDividend Admin and new Backend remain ImagePullBackOff on old tag 12d63b4 due missing linux/arm64 manifest. Runner v14 skipped restart. StockDividend health lane failed; final gate failed only for StockDividend.
- Read-only inspection #41461378005 completed SUCCESS; inspection PR #1061 exact-head validated by #41461496570 and squash-merged at `08b8b52891e7037e28cc6926648125a85c77db1a`. It is workflow_dispatch recovery evidence, not a native schedule.

## Native schedule evidence at 2026-11-02 14:25Z

- Platform native schedule last observed: inspection #41407411326, reconciliation #41407522742, watchdog #41406983213, mirror #41407613563, recovery #41400302676. No newer schedule event observed.
- TCE native schedule last observed: WF-06 #41424898130, WF-12 #41419694332, WF-07 #41397768048. WF-06 forwarder #41424938817 and Platform receiver #41424970499 are workflow_run/fallback evidence, not cron delivery.
- Do not alter any cron expression, strict HTTP 200 checks or TCE market-scan schedule.

## Current repository and owner-action inventory — 2026-11-02 14:25Z

- Platform Infra master `08b8b52891e7037e28cc6926648125a85c77db1a`; open draft PRs #544/#541/#539.
- TCE Dashboard master `a5e8866d2ba28936d57b31ce6a067186c7204369`; no open PRs.
- StockDividend master `38220ddfef2db7128482547f72b7f06211e9c9bc`; no open PRs.
- Media Generation master `0d4fc2ac15834c20357fd2420b732e6411fd8930`; no open PRs.
- Authentication master `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`; open PRs #75/#76 remain gated on production side effects and migration provenance.
- StockDividend production release remains disabled pending explicit authorization and `STOCKDIVIDEND_ACTIONS_READ_TOKEN`.
- Mirror requires `PLATFORM_INFRA_MIRROR_TOKEN` with destination-only Contents:write.
- Preserve all CI/test/security, backup, cleanup, manual/read-only, release and scheduled workflows. No duplicate SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Read-only VPS inspection contract and latest evidence — 2026-11-02

- `.github/workflows/inspect-vps.yml` remains read-only and writes only `debug/vps-latest.md` through an exact-head inspection PR.
- Recovery-triggered inspection [#41461378005](https://github.com/phanthienquoc/platform-infra/actions/runs/41461378005) SUCCESS; generated at 2026-11-02T14:22:54Z. Inspection PR #1061 exact head `0bf22ec5f13b3e4bd5eada3169300181628f3f6f`, exact manifest validation #41461496570 PASS, squash merge commit `08b8b52891e7037e28cc6926648125a85c77db1a`.
- Node Ready; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Ubuntu 22.04.5 ARM64; Docker 29.1.3; 19 GiB RAM available; disk 55%, pressure normal.
- Platform and Media runner services active/enabled; runner policy v14 installed.
- OS/containerd/Docker updates remain pending and `restart_required=yes`; no maintenance/reboot occurred.
- Media backend/frontend, MicroFE Shell/WS and NATS are healthy with runtime imageIDs recorded. Media backend digest is `sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d`; frontend digest is `sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a`.
- Stock Admin two Pods and new Backend Pod remain ImagePullBackOff on `12d63b4`, no imageID, no restart loop; old Backend `23b2878` and unmanaged legacy Frontend remain Running.
- TCE frontend/service and microfe-auth/Keycloak remain 0/0 intentionally.
- Docker image inventory reported 5.773 GB reclaimable, but disk pressure is normal; no cleanup was run.
- This inspection was a recovery `workflow_dispatch`, not native schedule delivery. No production manifest, image, replica, credential value, database object or cron expression was changed by the inspection.

## Latest Platform state after inspection merge

- Platform master: `08b8b52891e7037e28cc6926648125a85c77db1a`.
- Open Platform PRs: #544/#541/#539 (draft).
- Media PR #67 and Platform PR #1060 are merged; their publisher provenance contract is now active.
- Reconciliation #41460962292 final gate failed only on StockDividend; Auth, MicroFE, Media and TCE lanes passed; Keycloak skipped.
- Native Platform and TCE schedule history remains stale as recorded above. Recovery/inspection dispatches must not be counted as cron ticks.

## TCE publisher provenance contract — merged 2026-11-02

- Producer: `TCE-dashboard/.github/workflows/wf-03-tce-production-deploy.yml`.
  - TCE remains responsible for native ARM64 image builds and GHCR publication.
  - `tce-release-requested` payload now includes `app`, `release`, `source_run_id`, `source_workflow_path`, `source_event`, and `source_head_sha`.
  - Source event is restricted to `workflow_dispatch` from master; full source SHA is attested and the existing 7-character release-tag suffix is checked against it.
  - `scripts/validate-tce-release-contract.sh` runs in WF-01P PR CI, WF-01 master verification and WF-03 before dispatch.
  - PR #1012 exact-head checks #41462785094 (WF-01P), #41462785167 (WF-02) and #41462785008 (WF-05) PASS; merge commit `3c987231ffc1cfafebcb25d2d140e7f499081310`.
- Consumer: `platform-infra/.github/workflows/gitops-image-promotion.yml`.
  - `fanout-tce-release` validates the four source fields and runs `scripts/verify-tce-publisher-run.sh` before either image promotion dispatch.
  - Verifier checks exact run ID, repository, head repository, workflow path, event, master branch, full SHA, completed status and successful conclusion using the public TCE Actions API.
  - Regression tests: `scripts/tests/verify-tce-publisher-run.test.sh`, executed by `validate-github-actions.yml`.
  - Static workflow contract validation ensures provenance verification precedes both image-promotion dispatches and no cross-repository credential is introduced.
  - PR #1063 exact-head #41462823605 (workflow/lint/contracts) and #41462823627 (manifest render/contracts) PASS; merge commit `41c453c0a1b6df2c69de1d9f51c061e2f5266a27`; post-merge #41462989569/#41462989629 PASS.
- Merge order: TCE producer PR #1012 first, Platform consumer PR #1063 second. Legacy `tce-release-requested` payloads without provenance are rejected.
- TCE is public, so no TCE Actions-read PAT is required. Existing TCE `PLATFORM_INFRA_TOKEN` remains only for producer-side Platform dispatch/run correlation. If TCE becomes private, fail closed and configure a dedicated Actions:read credential before release.
- No TCE release was dispatched by these changes. The existing 7-character SHA-derived tag remains; digest-pinned TCE production manifest migration is a separate follow-up.

## TCE provenance post-merge runtime status — 2026-11-02 14:40Z

- TCE post-merge WF-02 #41462961803 PASS; WF-05 #41462961759 PASS.
- WF-01 master build #41462961881 passed `Validate TCE production release contract` and `Verify required repository secrets`; ARM64 frontend image build was still in progress at the time of inventory update.
- Platform post-merge validation #41462989569 and #41462989629 PASS.
- Platform recovery push #41462989681 SUCCESS and explicitly skipped fallback dispatch because reconciliation #41460962292 and inspection #41461378005 were fresh.
- No new native schedule tick observed; do not count post-merge/recovery runs as cron delivery.


## 2026-11-02 15:01 UTC — TCE paired digest release and reconciliation compatibility

### TCE producer: `TCE-dashboard/.github/workflows/wf-03-tce-production-deploy.yml`

- Release labels now end in the full 40-character source commit SHA.
- Buildx registry inspection resolves the web and service manifest digests after push and checks both expose `linux/arm64`.
- `tce-release-requested` carries `web_digest`, `service_digest`, `source_run_id`, `source_workflow_path`, `source_event` and `source_head_sha`.
- Producer acknowledgement matches the exact Platform Image Promotion display title/release, not any recent promotion run.
- WF-01 and WF-01P enforce this contract. Master post-merge WF-01/WF-02/WF-05 all passed on `afad281fa57b2846446a152b6f5cf3c2600ee51d`.

### Platform consumer: `platform-infra/.github/workflows/gitops-image-promotion.yml`

- `promote-tce-digests` handles `tce-release-requested` and verifies full-SHA release metadata and source publisher provenance first.
- GHCR tag resolution must equal each attested digest; the exact digest references are separately checked by `scripts/validate-ghcr-image-reference.sh` for ARM64.
- Web/service are promoted together through `scripts/promote-tce-image-digests.py` in one exact-head PR. The coordinator waits until both digests are on master before dispatching the shared GitOps reconciliation.
- The changed-image contract rejects new TCE tag references. The current legacy tag pair remains renderable until the next authorized digest promotion.
- Concurrency key includes the TCE release label to serialize/reconcile the paired release event.

### Runtime compatibility: TCE release and live-image checks

- `scripts/resolve-tce-gitops-image-refs.py` is the single parser for paired legacy tags or paired SHA-256 digests.
- `scripts/verify-tce-gitops-release.sh` validates both references and rejects mixed modes, malformed/duplicate/missing fields and mismatched legacy tags.
- `scripts/verify-tce-gitops-images.sh` validates the pair and compares live Deployment image references using tag or digest syntax.
- `validate-github-actions.yml` runs resolver self-tests; `validate-workflow-contracts.py` asserts both runtime scripts use the resolver.
- `reconcile-vps.yml` remains the sole production apply authority. No app repository gains SSH, Compose, kubectl apply or production manifest ownership.

### Validation

- TCE producer PR #1013: exact-head WF-01P/WF-02/WF-05 PASS; post-merge WF-01/WF-02/WF-05 PASS.
- Platform consumer PR #1065: exact-head validate-github-actions/validate-manifests/keycloak-ci PASS; post-merge all three PASS.
- Platform runtime compatibility PR #1066: exact-head validate-github-actions/validate-manifests PASS; post-merge both PASS.
- Runtime compatibility changes were code/tests only; no TCE release was published or promoted.


## 2026-11-02 16:03 UTC — current workflow ownership and evidence

### New Platform contract: StockDividend paired digest convergence

Platform PR #1069 merged as `492e0377dccdec09e7fe1daeb0a98b825b10a3e0`.

- `gitops-image-promotion.yml` now waits for the exact backend/admin digest pair to be visible together in the production StockDividend Kustomize overlay on master before dispatching shared reconciliation.
- `scripts/verify-stockdividend-gitops-digests.py` is an offline, dependency-free verifier with positive/negative self-tests.
- `validate-github-actions.yml` runs the self-test; `validate-workflow-contracts.py` checks the readiness gate and step ordering.
- Exact-head PR checks #41477608011/#41477608062 and post-merge checks #41477716689/#41477716663 all PASS. Recovery push #41477716817 SUCCESS.
- The gate is not yet runtime-exercised by a new StockDividend release. It does not enable release, supply credentials or mutate production by itself.

### Repository ownership / latest master state

| Repository | Master SHA | Deployment responsibility | Open PRs |
|---|---|---|---|
| `platform-infra` | `492e0377dccdec09e7fe1daeb0a98b825b10a3e0` | Production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, K3s rollout and health | #544/#541/#539 draft |
| `TCE-dashboard` | `afad281fa57b2846446a152b6f5cf3c2600ee51d` | App CI/tests, WF-03 native ARM64 builds, immutable GHCR digest publication, authenticated release handoff | None |
| `stockdividend` | `38220ddfef2db7128482547f72b7f06211e9c9bc` | App CI, native ARM64 Scraper/Admin/Backend builds, immutable full-SHA tags and paired backend/admin digest handoff | None |
| `media-generation` | `0d4fc2ac15834c20357fd2420b732e6411fd8930` | App CI and paired backend/frontend immutable digest publication with publisher provenance | None |
| `phanthienquoc-authentication` | `ceb2688d6277b10f1bfe7652223d1d295b7e49d9` | Auth CI/tests and controlled auth image publication; production identity/DB lifecycle remains gated | #75 open, #76 draft |

### Workflow inventory — preserve current authority boundaries

- Platform `gitops-image-promotion.yml`: verifies source provenance and exact GHCR manifests; creates scoped manifest PRs; checks exact PR head before squash merge; dispatches reconciliation only after required image references converge.
- Platform `reconcile-vps.yml`: sole production apply authority. App repositories do not gain SSH, Compose, kubectl apply or production-manifest ownership.
- Platform `inspect-vps.yml`: read-only K3s/host snapshot; inspection PRs are exact-head validated before merge.
- Platform `recover-stale-ops.yml`: fallback controller and authenticated TCE heartbeat receiver. Its workflow_dispatch/repository_dispatch/push runs are not native schedule ticks.
- Platform `validate-manifests.yml` and `validate-github-actions.yml`: render/manifest, secret, immutable-image, workflow and regression checks. Both post-merge checks for #1069 passed.
- Platform `mirror-locally-uncensored.yml`: purposeful scheduled mirror; remains blocked only by missing destination token.
- TCE WF-01/WF-02/WF-05: app build, formatting and backend tests. WF-03: native ARM64 production publisher with full-SHA release and paired web/service digests. WF-06: public health assertion (expected HTTP 200). WF-07: independent third-party integration check. WF-12: WF-06 freshness watchdog plus authenticated Platform heartbeat. No cron changes.
- StockDividend `.github/workflows/deploy.yml`: native ARM64 build and immutable full-SHA publication; verifies Admin/Backend ARM64 manifests before dispatching the paired digest event with source-run provenance. Promotion remains release-gated.
- Media `wf-03-media-production-deploy.yml`: app-owned native ARM64 build/publication and paired digest provenance. Platform owns manifest promotion and rollout.
- Auth `auth-service-ci` and `auth-service-release`: app-owned tests/build. Supabase production integration and migration state are separate gates; skipped Preview checks are not counted as PASS.

### Latest workflow evidence

- Platform inspection #41476912329 succeeded (workflow_dispatch) and its exact-head snapshot PR #1068 merged at `94a781d7135db0c732dace628a3eaddd1be7c464`; validation #41477034011 PASS.
- Platform reconciliation #41476348795 failed only on StockDividend Pod health. Runner v14 correctly suppressed restart for permanent `no match for platform in manifest` errors. Recovery #41476822106 and fresh inspection #41476912329 succeeded.
- Platform #1069 exact-head checks #41477608011/#41477608062 and post-merge #41477716689/#41477716663 PASS.
- TCE WF-07 scheduled #41476258191 PASS. WF-12 workflow_run #41476296496 had a stale WF-06 check but successfully dispatched its independent heartbeat; Platform receiver #41476320175 validated the payload.
- StockDividend latest CI #41397317588 and publisher #41397317600 PASS. Media latest CI #41460906654 PASS. Auth #75/#76 validation PASS; Supabase Preview SKIPPED.

### Schedule and runtime status

- Platform native schedule latest: inspection #41407411326 (07:36:38Z), reconciliation #41407522742 (07:37:40Z), watchdog #41406983213 (07:32:45Z), mirror #41407613563 (07:38:31Z), recovery #41400302676 (06:30:13Z). Later dispatch/push/receiver runs are not cron ticks.
- TCE native schedule latest: WF-07 #41476258191 (15:54:51Z) success; WF-06 #41424898130 (09:57:51Z) HTTP 503 health failure; direct WF-12 #41419694332 (09:19:29Z) freshness failure. WF-12 workflow_run #41476296496 (15:55:05Z) failed its WF-06 freshness check at 357 minutes while heartbeat dispatch succeeded.
- Fresh inspection #41476912329 generated 15:58:58Z: node Ready, ARM64, K3s 1.36.3, containerd 2.3.2-k3s2, disk 55%, 19 GiB available memory, runner v14 active. Media/MicroFE/NATS 1/1. Stock Admin two Pods and new Backend Pod fail ARM64 image pull on tag 12d63b4; old Backend and legacy Frontend remain running. TCE/Auth/Keycloak remain 0/0 intentional. Host restart_required=yes; no reboot/upgrade/cleanup.

### Outstanding owner actions

- Configure `STOCKDIVIDEND_ACTIONS_READ_TOKEN` (Actions:read only on StockDividend) in the protected Platform production Environment.
- Configure `PLATFORM_INFRA_MIRROR_TOKEN` (Contents:write only on the destination mirror repository).
- Keep StockDividend release flag false until explicit authorization. No promotion was dispatched.
- Keep Auth production merge/integration gate until Supabase side-effect and migration provenance/drift are resolved.

No production manifest, image reference, shared pull credential, database object, desired replica, cron expression or workflow authority was changed by this inventory update. Preserve TCE market-scan schedules.


## 2026-11-02 16:55 UTC — workflow ownership and latest runtime evidence

### Cross-repository ownership (reconfirmed)
- `phanthienquoc/platform-infra`: sole owner of production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, K3s rollout, workload health, read-only inspection and stale-operations recovery.
- `phanthienquoc/TCE-dashboard`: owns app CI/tests and WF-03 native ARM64 paired web/service GHCR publication with full-SHA provenance. WF-06 remains strict public HTTP 200 health assertion; WF-07 is the independent integration schedule; WF-12 is the freshness watchdog and heartbeat forwarder.
- `phanthienquoc/stockdividend`: owns CI and native ARM64 Scraper/Admin/Backend immutable publication with publisher run provenance. Platform owns paired Admin/Backend GitOps promotion and rollout.
- `phanthienquoc/media-generation`: owns CI and paired frontend/backend immutable GHCR publication with source-run provenance. Platform owns production manifests and rollout.
- `phanthienquoc/phanthienquoc-authentication`: owns Auth CI/tests and controlled image publication. Production identity, Supabase migration and Keycloak lifecycle remain separately gated.

### Platform workflow authority
- `gitops-image-promotion.yml`: validates publisher provenance and immutable GHCR manifests, creates scoped GitOps PRs, verifies exact PR heads, and only dispatches reconciliation after required digest pairs converge on master. StockDividend paired Admin/Backend digest convergence is guarded by `scripts/verify-stockdividend-gitops-digests.py` and regression tests; this gate has not yet been exercised by a new authorized StockDividend release.
- `reconcile-vps.yml`: remains the sole production apply authority. App repositories do not gain SSH, Compose, kubectl apply or production manifest ownership.
- `inspect-vps.yml`: read-only host/K3s snapshot with exact-head validation before inspection PR merge.
- `recover-stale-ops.yml`: scheduled stale-delivery controller, workflow_run fallback and authenticated TCE heartbeat receiver. Only event=schedule counts as its native cron delivery; its dispatches do not count as native reconciliation/inspection ticks.
- `validate-manifests.yml` and `validate-github-actions.yml`: retain rendered-manifest, security, immutable-image, workflow-contract and regression validation.
- `mirror-locally-uncensored.yml`: purposeful scheduled mirror; still blocked by missing destination Contents:write token. Preserve the job.
- Preserve all app CI/test/security, backup, cleanup, manual, release and scheduled workflows. No duplicate SSH/Compose deployment authority is permitted.

### Current run evidence
- Native scheduled recovery [#41482540454](https://github.com/phanthienquoc/platform-infra/actions/runs/41482540454) (16:32:54Z) SUCCESS; both stale reconciliation and inspection recovery steps completed. It dispatched reconciliation because the native reconciliation cadence was stale.
- Fallback reconciliation [#41482572380](https://github.com/phanthienquoc/platform-infra/actions/runs/41482572380) (16:33:06Z, workflow_dispatch) shared job SUCCESS; MicroFE, Media, Auth and TCE lanes SUCCESS; StockDividend health lane FAILURE. No GitOps drift; apply skipped; image changes disabled.
- Recovery [#41482991444](https://github.com/phanthienquoc/platform-infra/actions/runs/41482991444) (16:35:38Z, workflow_dispatch) SUCCESS. It verified the reconciliation age 0m and inspection age 35m at 16:35:50Z, and avoided duplicate dispatch.
- StockDividend health log: Admin Pods and new Backend Pod fail pulling legacy `12d63b4` because the manifest has no ARM64 platform; runner v14 suppresses restart for permanent image-pull errors.
- Latest full K3s inspection [#41476912329](https://github.com/phanthienquoc/platform-infra/actions/runs/41476912329) generated 15:58:58Z; still within the 75-minute freshness budget at 16:55Z. Node Ready, K3s 1.36.3, ARM64, disk 55%, ~19 GiB available RAM; Media/MicroFE/NATS 1/1; Stock Admin/new Backend pull failures; TCE/Auth/Keycloak 0/0 intentional; `restart_required=yes`.
- Latest app CI/publication remains: TCE WF-01 #41466743923, WF-02 #41466743801, WF-05 #41466743773 SUCCESS; StockDividend CI #41397317588 and publisher #41397317600 SUCCESS; Media CI #41460906654 SUCCESS; Auth PR CI #41329425940 SUCCESS. No new application release was dispatched.
- Open PR inventory: Platform #544/#541/#539 (draft); Authentication #75/#76; none in TCE, StockDividend or Media. Platform master is `16719f6251826bb78d0c5efd996cb13ce86eb685`; TCE `afad281fa57b2846446a152b6f5cf3c2600ee51d`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media `0d4fc2ac15834c20357fd2420b732e6411fd8930`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.

### Schedule semantics and blockers
- Native scheduled recovery is alive, but this does not prove native reconcile/inspection cadence: latest native reconcile #41407522742 and inspection #41407411326 remain stale; latest watchdog #41406983213 and mirror #41407613563 remain stale/blocked.
- TCE latest native WF-07 #41476258191 SUCCESS; WF-06 #41424898130 returns HTTP 503 at all strict public endpoints while TCE/Auth are intentionally stopped; direct scheduled WF-12 #41419694332 is stale. Workflow_run forwarding/heartbeats are not cron ticks. Keep every TCE cron and market-scan schedule unchanged.
- Owner-only secrets: `STOCKDIVIDEND_ACTIONS_READ_TOKEN` (StockDividend-only Actions:read) and `PLATFORM_INFRA_MIRROR_TOKEN` (destination-only Contents:write). Do not substitute credentials or write secret values to Git.
- StockDividend production release remains disabled pending explicit authorization. Auth production integration/migration provenance gate remains open. No production manifest, image, database, replica, credential or schedule mutation occurred.


## 2026-11-02 17:58 UTC — downstream runner queue visibility gap

### Current repository heads and open PRs
- Platform Infra master `16719f6251826bb78d0c5efd996cb13ce86eb685`; TCE Dashboard `afad281fa57b2846446a152b6f5cf3c2600ee51d`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media Generation `0d4fc2ac15834c20357fd2420b732e6411fd8930`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open Platform PRs: #1071, #544, #541, #539. Open Auth PRs: #75/#76. No open PRs in TCE, StockDividend or Media.
- Platform PR #1071 exact-head `b22480af63895cb879f9e52dd210a88c9dd677bb` validation #41486648063 SUCCESS before the latest evidence append; rerun is required for the updated head.

### Ownership boundaries remain unchanged
- Platform Infra remains the sole production manifest, shared GHCR pull credential, GitOps promotion/reconciliation, K3s rollout, health and recovery owner.
- App repositories own CI/tests and immutable GHCR publication. They do not gain production SSH, Compose, kubectl apply or manifest ownership.
- Preserve CI/test/security, manual/release, backup/cleanup and purposeful scheduled workflows. Do not remove the mirror workflow while it remains an intentional job blocked only by its destination token.

### New queue evidence
- Native scheduled reconcile [#41491502003](https://github.com/phanthienquoc/platform-infra/actions/runs/41491502003) arrived at 17:28:27Z and its shared reconcile job completed SUCCESS. Auth lane passed; StockDividend lane failed on permanent ARM64 image errors for tag `12d63b4`.
- At 17:58Z, the overall run remained queued because MicroFE job 125435773880, TCE job 125435774162 and Media job 125435774301 were still queued with `runner_id=0` and no runner name since 17:29:10Z. The runner's exact cause is not yet established; do not claim it is offline.
- Watchdog #41491160810 failed because the latest native inspection #41407411326 was 589 minutes old. Existing watchdog reports workflow-level queue timing but misses long-waiting downstream lane jobs. Next implementation: add a read-only job-level queue diagnostic against the latest scheduled reconcile run, using the watchdog's GitHub API reference timestamp and the existing 15-minute queue budget. Fail scheduled/manual enforcement when a targeted lane remains queued without a runner past budget; push smoke should emit warning only. Do not change the schedule or recovery authorities.
- Native reconciliation has one resumed tick; native inspection cadence remains stale. Recovery #41482540454 is native recovery schedule evidence only, not inspection/reconciliation schedule delivery.

### Schedule and runtime
- TCE WF-07 #41476258191 is a recent native schedule SUCCESS. WF-06 #41424898130 remains strict HTTP 503 while TCE/Auth are intentionally stopped; direct WF-12 #41419694332 remains latest scheduled tick with stale freshness. Workflow_run forwarding/receiver is not a native cron tick.
- K3s live pod listing in #41491502003: node Ready; Media/MicroFE/NATS 1/1; Stock Admin two Pods and new Backend Pod ImagePullBackOff; old Backend and legacy Frontend Running. TCE/Auth/Keycloak remain intentionally stopped.
- No new image release, promotion, manifest apply or replica change occurred.

### Owner actions
1. Configure `STOCKDIVIDEND_ACTIONS_READ_TOKEN` with StockDividend-only Actions:read in the protected Platform production Environment.
2. Configure `PLATFORM_INFRA_MIRROR_TOKEN` with destination-only Contents:write on `phanthienquoc/locally-uncensored-private`.
3. Keep StockDividend release disabled until explicit authorization; then exercise publisher provenance, paired ARM64 digest promotion, exact master convergence, reconciliation and live imageID checks.
4. Keep Auth production integration/migration gate until side effects and migration provenance are authoritative.
5. Keep TCE WF-06/WF-07/WF-12 and market-scan cron declarations unchanged.

No production manifest, image, credential, database, replica, release flag, deployment authority or cron expression changed. TCE market-scan schedule unchanged.


## 2026-11-02 18:04 UTC — downstream runner queue SLA and watchdog implementation

### Repository ownership and current heads
- Platform Infra master `4c9429484a5fe2ff1b98222504e0b2ad63dbbece`; TCE Dashboard `afad281fa57b2846446a152b6f5cf3c2600ee51d`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media Generation `0d4fc2ac15834c20357fd2420b732e6411fd8930`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform #1072/#544/#541/#539; Authentication #75/#76; none in TCE, StockDividend or Media. #1071 is merged.
- PR #1072 adds a read-only downstream queue verifier and regression cases; head `2a0c2850612ff2071e0f62ab6d3efeb8a2c2c84f`; validate/lint checks were queued when recorded. It must not be merged until both checks pass at the final head.

### Evidence and queue contract
- Native reconciliation #41491502003 (17:28:27Z) completed at 18:02:05Z. Shared reconcile and Auth succeeded; StockDividend failed its workload health gate on the permanent ARM64-incompatible tag `12d63b4`.
- MicroFE/TCE/Media self-hosted deployment jobs waited 31m41s, 32m03s and 32m21s respectively before runner `platform-k3s-01` (runner id 2) picked them up. They subsequently completed successfully. This is confirmed runner queue delay, not proof of a permanently offline runner.
- Existing watchdog #41491160810 only detected stale inspection age (589m) and did not observe downstream lane assignment delays. PR #1072 extends the watchdog to query the latest scheduled reconcile run's `/jobs` endpoint and detect both queued unassigned jobs and completed jobs whose `started_at - created_at` exceeds the 15-minute budget.
- The verifier uses the watchdog's GitHub API `created_at` as reference clock; scheduled/manual/fallback enforcement fails on a breach, while post-merge push smoke warns only. Rerun attempts are not measured against original timestamps. It has no production write permissions and does not dispatch workflows.
- Preserve the existing 15-minute watchdog cron offset, reconciliation cron, inspection cron, recovery cron and all TCE schedules. TCE market-scan schedule unchanged.

### Runtime and safety
- Recovery #41496719058 and read-only inspection #41496768387 were still in progress at the evidence time; the latter is workflow_dispatch, not native schedule evidence.
- StockDividend release remains disabled pending owner Actions-read credential and explicit authorization. Mirror remains blocked by destination-only token. Auth remains gated on Supabase side-effect and migration review.
- No manifest, image, secret, database, replica, schedule, or deployment authority was changed by the queue-monitoring implementation.


## 2026-11-02 18:06 UTC — fresh inspection evidence and queue-monitoring follow-up

### Latest Platform master and PR state
- Platform Infra master `fc4b951949c12e90bbf5e0e3ba0e1adb6112b080` (automated inspection PR #1073 merged). TCE `afad281fa57b2846446a152b6f5cf3c2600ee51d`; StockDividend `38220ddfef2db7128482547f72b7f06211e9c9bc`; Media `0d4fc2ac15834c20357fd2420b732e6411fd8930`; Authentication `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`.
- Open PRs: Platform #1072/#544/#541/#539; Authentication #75/#76; none in TCE, StockDividend or Media. #1072 is rebased onto current master at head `c10e34d2bb70706716c024988d2f98bb73529b27`; required checks must pass at this exact head before merge.

### Read-only inspection and runner evidence
- Fresh inspection #41496768387 completed SUCCESS and its snapshot PR #1073 merged as `fc4b951`.
- Node `tce-k3s-01` Ready, ARM64, K3s 1.36.3+k3s1, K3s containerd 2.3.2-k3s2, Docker 29.1.3, disk 55%, ~19 GiB available RAM. Host says `restart_required=yes`; containerd.io package 2.4.2-3 is available but not installed.
- Platform and Media runner services were active in the snapshot. This confirms the runner service was present after the previous delay, but does not establish why GitHub assigned the later lanes 31–32 minutes after job creation.
- Media/MicroFE/NATS healthy 1/1 with digest-pinned imageIDs. Stock Admin two Pods and new Backend Pod remain image-pull failures on `12d63b4`; old Backend replica and unmanaged legacy Frontend remain Running. TCE/Auth/Keycloak are intentionally 0/0; OIDC probes return 503 while Keycloak is stopped.

### Recovery and native schedule semantics
- Recovery #41496719058 succeeded, found reconcile activity fresh and inspection activity 121m old, and dispatched read-only inspection #41496768387. This is workflow_dispatch evidence, not native inspection cron.
- Watchdog #41496751519 ran before that inspection completed and failed on 625m native inspection age. The fallback inspection then completed and merged; this ordering explains the failure without claiming the fallback failed.
- Native inspection latest remains #41407411326; native reconcile latest #41491502003; native watchdog latest #41491160810; native recovery latest #41482540454. Only event=schedule counts as native delivery.
- TCE latest native WF-07 #41476258191 SUCCESS; WF-06 #41424898130 HTTP 503; direct WF-12 #41419694332 stale. Preserve strict HTTP 200 and all cron schedules.

### Queue contract
- Reconciliation #41491502003 recorded 31m41s MicroFE, 32m03s TCE and 32m21s Media runner assignment delays; each eventually ran on runner id 2. StockDividend remained the only failed deployment lane.
- PR #1072 adds a read-only job-level queue verifier for both queued/unassigned jobs and completed jobs with `started_at - created_at` beyond 15 minutes. It uses the watchdog GitHub API reference timestamp, fails scheduled/manual/fallback enforcement, and keeps post-merge push smoke warn-only. Regression tests and static workflow assertions are included.
- No direct SSH/Compose authority, production mutation, cron edit, runner restart or credential change was introduced.

### Owner gates
- StockDividend production promotion remains disabled pending Actions:read token and explicit authorization.
- Mirror remains blocked by destination-only Contents:write token.
- Auth production integration/migration review remains gated; no database changes.
- Keep TCE market-scan schedule unchanged.


## 2026-11-02 18:08 UTC — downstream lane queue watchdog merged and exercised

### Workflow contract now on master
- Platform Infra master before this tracker PR: `e1981cb9a89d32c8ea3b212b00a9eef0b6cb1895`.
- PR #1072 merged at exact head `35c336cc7f0ebdcebfce6911764adaf150467597`, merge `e1981cb9a89d32c8ea3b212b00a9eef0b6cb1895`.
- New helper: `scripts/verify-reconcile-lane-queue.py`.
- `reconcile-schedule-watchdog.yml` now queries the latest scheduled reconcile run's `/jobs` API and checks:
  - currently queued/waiting deployment lanes against the watchdog's GitHub API timestamp;
  - historical `started_at - created_at` runner-assignment delay for completed/in-progress lanes;
  - only named `Deploy lane — …` jobs; skipped jobs and reruns with non-comparable original timestamps are excluded.
- Existing 15-minute queue budget is reused. Scheduled/manual/fallback/workflow_run enforcement fails on breach; post-merge push smoke emits warnings only. The job remains read-only, with `actions: read`, `contents: read` and checkout `persist-credentials: false`.
- Offline regression suite covers healthy/short queue, queued over budget, completed delayed start, assigned-but-not-started, unrelated jobs, reruns and push warn-only. `validate-workflow-contracts.py` enforces helper presence, workflow wiring and regression execution.
- No cron expression, production apply authority, recovery authority, manifest, image or credential changed.

### CI and runtime evidence
- Exact-head #1072 checks: validate #41497308517 PASS; lint #41497308596 PASS.
- Post-merge: validate-manifests #41497619290 PASS; validate-github-actions #41497619531 PASS.
- Push watchdog smoke #41497619396 PASS. It detected the actual historical lane delays: MicroFE 31m, TCE 32m, Media 32m. It emitted warnings (not failures) as required for push smoke. It also warned that native inspection was 631m stale.
- Recovery push smoke #41497619299 PASS with no production dispatch.
- Scheduled/manual/workflow_run enforcement has not yet been exercised after merge; the next such event should fail if a lane still exceeds the 15-minute budget.

### Ownership and production status
- Platform remains sole owner of manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, K3s rollout/health and recovery. App repositories continue to own tests/builds and immutable GHCR publication.
- Latest inspection #41496768387 (workflow_dispatch) merged as PR #1073/#commit fc4b951. Node Ready, K3s 1.36.3+k3s1, disk 55%, ~19 GiB available RAM, Platform/Media runner services active. Media/MicroFE/NATS healthy; Stock Admin/new Backend still fail ARM64 image pull on `12d63b4`; old Backend and legacy Frontend remain Running. TCE/Auth/Keycloak are intentionally 0/0.
- Native Platform inspect/reconcile cadence remains stale; recovery dispatches do not count as native schedule ticks. TCE WF-06/WF-12 remain stale/failing; WF-07 last observed native tick passed. Do not alter TCE market-scan schedule.
- StockDividend release remains disabled pending owner token and explicit authorization; mirror token remains missing; Auth production integration/migration gate remains open.


## 2026-11-02 19:04 UTC / 2026-11-03 02:04 ICT — watchdog queue semantics and latest runtime evidence

### Ownership and workflow authority
- Platform Infra remains sole owner of production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, K3s rollout/health, inspection and stale-operations recovery.
- App repositories own CI/tests and immutable GHCR publication. They do not own production SSH, Compose, kubectl apply or production manifest changes.
- `reconcile-vps.yml` remains the sole production apply authority. `inspect-vps.yml` remains read-only. The watchdog and recovery workflows only inspect GitHub Actions history and dispatch the existing authorized workflows under their current policy.
- Preserve all CI/test/security, backup/cleanup, manual/release and purposeful scheduled jobs. No duplicate direct SSH/Compose authority was introduced.

### Queue watchdog follow-up
- The downstream lane queue verifier from PR #1072 is active on master. It measures only named `Deploy lane — …` jobs and enforces a 15m runner-assignment budget.
- Latest workflow_run watchdog #41499180006 exposed a repeat-failure edge: the same completed lane delays from stale reconciliation #41491502003 (31–32m) were re-enforced on later watchdog events even though reconciliation freshness had already failed at 49m (>45m).
- PR #1076 adds a parent-run freshness boundary. Fresh reconciliation runs continue to enforce completed runner-assignment delays; when the parent is stale, completed/already-assigned historical delays are not re-failed, but currently queued/unassigned lanes remain actionable. The reconciliation freshness gate continues to fail the stale schedule.
- PR #1076 exact head: `34786d328f8e136ab2e1c709435df84b3d015783`; validate-manifests #41506862664 SUCCESS; validate-github-actions #41506862858 was in progress at this evidence point. Keep unmerged until both pass on the exact head.

### Schedule event semantics — latest observations
- Native Platform inspection resumed: #41498271871 (event=schedule, SUCCESS, 18:11:59Z).
- Native Platform reconciliation is still stale: #41491502003 (event=schedule, 17:28:27Z, FAILURE due StockDividend).
- Native Platform watchdog schedule latest: #41491160810 (event=schedule, 17:26:13Z, FAILURE due then-stale inspection). #41499180006 is workflow_run, not cron.
- Native Platform recovery schedule latest: #41482540454 (event=schedule, 16:32:54Z, SUCCESS). #41499180093 is workflow_run.
- Native mirror schedule #41499146752 failed because the destination mirror token is empty/missing.
- TCE native schedules: WF-07 #41476258191 SUCCESS; WF-06 #41424898130 strict public HTTP 200 checks FAIL with 503 while intentionally stopped; WF-12 #41419694332 freshness FAIL. WF-12 workflow_run #41476296496 has a successful heartbeat job but failed WF-06 freshness; do not count it as a native schedule.
- Keep every existing cron expression unchanged, especially all TCE market-scan schedules.

### Runtime state and release holds
- Fresh scheduled inspection #41498271871 / snapshot #1075: node Ready, ARM64, K3s 1.36.3+k3s1, disk 55%, ~19 GiB available RAM; Platform/Media runners active; restart_required=yes due pending OS/Docker/containerd updates.
- Media, MicroFE Shell/WS and NATS 1/1 with digest-pinned imageIDs. Stock Admin and new Backend remain ImagePullBackOff on non-ARM64 tag 12d63b4; old Backend replica and unmanaged legacy frontend remain Running. TCE/Auth/Keycloak 0/0 intentionally.
- StockDividend publisher remains successful but production release disabled pending protected Actions-read credential and explicit authorization. Mirror remains blocked by destination-only Contents:write token.
- Auth production integration/migration gate remains open. No database mutation.


## 2026-11-02 19:10 UTC / 2026-11-03 02:10 ICT — stale historical queue guard merged

- PR #1076 merged to Platform master at `778746152bee482fdea24ad9ab88b1cdee03d4ad` from exact head `34786d328f8e136ab2e1c709435df84b3d015783`.
- Required exact-head checks: validate-manifests #41506862664 SUCCESS; validate-github-actions #41506862858 SUCCESS.
- `verify-reconcile-lane-queue.py` now receives parent reconciliation creation time and MAX_AGE_MINUTES. Once the parent scheduled reconciliation is stale (>45m), completed/already-assigned historical queue delays are not re-failed on every later watchdog event; still-queued/unassigned lanes remain enforced at 15m. Fresh reconciliation runs continue enforcing completed assignment delay.
- Regression tests cover both stale completed and stale unassigned cases. Post-merge validate/lint and push smoke runs #41507316295/#41507316523/#41507316907/#41507316109 were queued at this update and remain unverified until completion.
- Runtime exercise of the stale-parent guard awaits the next watchdog invocation. Preserve the existing cron expressions and all TCE market-scan schedules.


## 2026-11-02 19:12 UTC / 2026-11-03 02:12 ICT — fallback reconciliation and lane results

- The post-merge recovery push #41507316109 observed the last native reconciliation stale by 67m and dispatched the sole production apply authority with exact payload: master SHA `778746152bee482fdea24ad9ab88b1cdee03d4ad`, `mode=apply`, `allow_image_changes=false`, `target_app=all`.
- Shared reconcile job succeeded: GHCR access preflight passed; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` Secrets were unchanged; service-account/deployment patches reported no change; runner v14 skipped permanent StockDividend image-pull restarts; no GitOps drift, so production manifest apply was skipped.
- Lane results: MicroFE 15s queue SUCCESS; Media 2s SUCCESS; StockDividend 29s queue FAILURE on three non-ARM64 `12d63b4` Pods; TCE 47s SUCCESS; Auth 64s SUCCESS; Keycloak skipped. All observed runner assignment delays were below the 15m queue budget. The final gate failed only for StockDividend.
- This fallback event is workflow_dispatch, not native schedule delivery. The new stale-parent queue guard has not yet been exercised by a scheduled-source workflow_run. Next native scheduled reconciliation/watchdog cycle remains the runtime verification point.
- #1076 exact-head and post-merge manifest/workflow validations all PASS. PR #1077 documentation head `fe0cf9cb91bda7e318d0c9ae10d138d412fba7fc` had validate-manifests #41507377407 SUCCESS before this additional evidence update; revalidate the final head before merge.
- No app image promotion, manifest apply, Pod restart or DB mutation. TCE market-scan cron unchanged.


## 2026-11-02 19:14 UTC / 2026-11-03 02:14 ICT — final current-state and validation record

- PR #1077 was closed as superseded; PR #1078 carried the tracker/inventory update onto the current master base and merged at `ab281dc47d8389bc0166ec9349a439e3a271c243`.
- PR #1078 exact-head validate-manifests #41507844748 SUCCESS; post-merge validate-manifests #41507991465 SUCCESS.
- Current Platform open PRs: #544/#541/#539 (draft). Authentication open PRs: #75/#76. No open PRs in TCE Dashboard, StockDividend or Media Generation.
- PR #1076 stale-parent queue guard is merged. It suppresses only completed/already-assigned historical lane delays when the parent scheduled reconciliation is itself stale (>45m); currently unassigned lanes remain enforced at 15m. Exact-head validate-manifests #41506862664 and validate-github-actions #41506862858 PASS; post-merge #41507316523 and #41507316295 PASS; push watchdog/recovery smoke #41507316907/#41507316109 PASS.
- Runtime guard exercise still pending a later native scheduled reconciliation and its schedule-source watchdog event. The latest fallback #41507349624 was workflow_dispatch and must not be counted as native schedule evidence.
- Fallback #41507349624 used master SHA `778746152bee482fdea24ad9ab88b1cdee03d4ad`, `mode=apply`, `allow_image_changes=false`, `target_app=all`; shared diff clean and apply skipped. MicroFE/Media/TCE/Auth lanes SUCCESS; StockDividend FAILURE on ARM64 manifest mismatch; Keycloak skipped. Recovery #41507694544 SUCCESS.
- Preserve app-owned CI/build/immutable GHCR publication, Platform-owned manifests/pull credentials/promotion/reconciliation/health, and `reconcile-vps.yml` as sole apply authority. No SSH/Compose duplicate authority or workflow removal.
- Platform/TCE native schedule cadence remains incomplete; mirror token is missing. StockDividend paired release remains gated by Actions-read credential and explicit authorization. Auth production integration/migration gate remains open. TCE market-scan cron unchanged.


## 2026-11-03 02:16 ICT — recovery push trigger narrowed to deployment-relevant changes

- PR #1080 changes only the recovery controller's master-push path filter and its static contract validator, plus tracker/inventory documentation.
- Keep automatic push recovery for production-affecting workflow/app/platform/overlay/script changes. Exclude the recovery controller itself and exact read-only CI/watchdog helpers so a monitoring/validator edit cannot trigger a full production reconciliation.
- Scheduled, manual, workflow_run and authenticated TCE-heartbeat triggers remain unchanged. No cron, release workflow, production manifest or deployment authority is removed.


## 2026-11-03 02:58 ICT — recovery push scope merged and verified

- Platform PR #1080 merged by squash at `dc92d4060a30bef1955fd9738a26c5c79cf80a03`; exact head `73067d7262ef975cf5af9d651a6426236ab256b9`; exact-head `validate-manifests` #41508539722 and `validate-github-actions` #41508539234 both SUCCESS. Post-merge `validate-github-actions` #41514856470 SUCCESS; `validate-manifests` #41514856736 was still in progress at the update time.
- Recovery push now excludes its own workflow file and four read-only helpers from its push trigger while retaining deployment-relevant workflow/app/platform/production-overlay/script changes. Schedule, manual, workflow_run and authenticated TCE repository_dispatch paths are preserved. After #1080 merge, only the two validation workflows were created; no recovery push or production reconciliation was triggered by the read-only scope-hardening change.
- Sole production apply authority remains `.github/workflows/reconcile-vps.yml`; inspection remains read-only. App repos own CI/build/immutable GHCR publication. Platform owns production manifests, shared pull credentials, promotion/reconciliation, rollout and health. No duplicate SSH/Compose deployment authority added.
- Latest Platform native schedule history: inspection #41498271871 SUCCESS; reconciliation #41491502003 FAILURE on StockDividend; watchdog #41491160810 FAILURE; recovery #41482540454 SUCCESS; mirror #41499146752 FAILURE due missing destination token. Manual inspection #41512091554 SUCCESS at 19:40:16Z does not count as cron delivery.
- TCE native WF-12 #41511665345 failed WF-06 freshness (heartbeat job itself SUCCESS); WF-07 #41476258191 SUCCESS; WF-06 #41424898130 failed strict HTTP 200 probes with 503 while services are intentionally stopped. Do not relax health assertions or alter TCE market-scan cron.
- Fresh manual VPS snapshot #1081 generated 2026-11-02 19:40:25Z: node Ready, ARM64, K3s 1.36.3, disk 55%, ~19 GiB available RAM; Media/MicroFE/NATS healthy; Stock Admin and new Backend Pods ImagePullBackOff on `12d63b4` without ARM64 manifest; old Backend and unmanaged legacy frontend 1/1; TCE/Auth/Keycloak 0/0 intentionally.
- Manual reconciliation #41511708072 shared job SUCCESS but StockDividend lane FAILURE. GHCR access passed, Auth runtime Secret provisioned/verified with values suppressed, shared pull Secrets unchanged, v14 skipped permanent image-pull restarts, GitOps diff clean and apply skipped. Other active lanes passed; recovery #41512035335 SUCCESS.
- Current masters: Platform `dc92d406...`; TCE `afad281f...`; StockDividend `38220ddf...`; Media `0d4fc2ac...`; Authentication `ceb2688d...`. Open PRs: Platform #544/#541/#539; Auth #75/#76; none in TCE/StockDividend/Media.
- Owner blockers: `STOCKDIVIDEND_ACTIONS_READ_TOKEN` not verified; `PLATFORM_INFRA_MIRROR_TOKEN` missing. StockDividend release remains disabled and unpromoted. Auth production integration/migration side-effect gate remains open.

## 2026-11-03 03:01 ICT — recovery push excludes read-only inspection changes

- PR #1080 merged at dc92d4060a30bef1955fd9738a26c5c79cf80a03: recovery push no longer self-triggers on its own workflow file and excludes read-only queue/CI validators. Exact-head #41508539722/#41508539234 PASS; post-merge #41514856470/#41514856736 PASS.
- PR #1082 docs refresh merged at df70d70be2069b523bd08d33f91ca328034103e4; exact-head #41515024252 and post-merge #41515242910 PASS.
- PR #1083 merged at c1529192344351a1e773e6d6ec772d373772d46c: remove .github/workflows/inspect-vps.yml from production recovery push positives and exclude scripts/inspect-vps.sh from scripts/**. These are read-only inspection paths; inspect-vps.yml continues its own push/schedule snapshot workflow, and scheduled inspection completion remains a recovery heartbeat. Exact-head #41515191104/#41515191110 PASS. Post-merge #41515316595/#41515316604 were in progress at this record; verify final conclusions.
- The post-merge run list after #1083 contained only manifest/workflow validation runs, with no recovery push or reconcile dispatch from the read-only scope change. This is evidence for this push, not proof of every future path filter case.
- Preserve reconcile-vps.yml as the sole production apply authority. App repos own CI/tests/builds and immutable GHCR publication; Platform owns manifests, shared pull credentials, promotion/reconciliation, rollout and health. No duplicate SSH/Compose authority. Scheduled, manual, workflow_run and authenticated TCE repository_dispatch recovery paths remain intact. No cron changes.
- Current native schedule history: Platform inspect #41498271871 PASS; reconcile #41491502003 FAIL (StockDividend); watchdog #41491160810 FAIL (stale inspection); recovery #41482540454 PASS; mirror #41499146752 FAIL (missing destination token). TCE WF-12 #41511665345 FAIL (WF-06 age 579m; heartbeat PASS), WF-07 #41476258191 PASS, WF-06 #41424898130 FAIL (HTTP 503 while stopped).
- Current master heads: Platform c1529192; TCE afad281f; StockDividend 38220ddf; Media 0d4fc2ac; Auth ceb2688d. Open PRs: Platform #544/#541/#539; Auth #75/#76; none in TCE/StockDividend/Media.
- Latest runtime snapshot #1081: node Ready, K3s 1.36.3, disk 55%, about 19 GiB RAM; Media/MicroFE/NATS healthy; Stock Admin/new Backend ImagePullBackOff on non-ARM64 12d63b4; old Backend and unmanaged frontend 1/1; TCE/Auth/Keycloak 0/0 intentionally.
- StockDividend production release remains disabled/unpromoted pending owner Actions-read token and explicit authorization. Mirror token is missing. Auth production integration/migration side-effect gate remains open.

### PR #1083 final post-merge result
- validate-manifests #41515316595 SUCCESS and validate-github-actions #41515316604 SUCCESS on merge SHA c1529192344351a1e773e6d6ec772d373772d46c.
- No recovery push or production reconciliation was created by the read-only inspection trigger change; only validation workflows ran.

## 2026-11-03 03:10 ICT — Node 24 checkout and workflow-trigger safety

- PR #1085 merged at 4715d7d0e091f67cdbef091b40bf5afe71fe8859; exact head 97bc52c7f9213d571f1b5230c61e8a98ec9b6532. Exact-head validate-manifests #41515782082, validate-github-actions #41515782174, SSO auto-onboarding #41515781776 and keycloak-ci #41515781964 all SUCCESS. Post-merge validate-manifests #41515885218 and validate-github-actions #41515885331 SUCCESS.
- All 17 Platform Infra checkout references now pin actions/checkout v7.0.1 SHA 3d3c42e5aac5ba805825da76410c181273ba90b1 (Node 24). Verified every file on current master contains the new SHA and no old v4 SHA. TCE/StockDividend/Media/Authentication still have v4 references; inspect push/deploy triggers before updating them.
- PR #1085 push triggered Provision TCE OIDC client #41515885560 (failed HTTP 503 at token endpoint before Admin API mutation), read-only Verify #41515885382 (HTTP 503), and vps-image-cleanup #41515885582 (DRY_RUN=true, 8 unused/10 retained/0 removed). Inspection #41515885354 succeeded; SSO auto-onboarding #41515885210 and keycloak-ci #41515885393 succeeded; SSO reconcile job skipped.
- Recovery push #41515885392 dispatched reconciliation #41515916117 because reconcile-vps.yml was in the recovery push filter. That reconciliation verified all nine GHCR packages, provisioned/verified Auth runtime Secret (values suppressed), left shared GHCR pull Secrets unchanged, skipped permanent StockDividend restarts, detected no drift and skipped manifest apply. Auth/TCE/MicroFE/Media lanes passed; StockDividend failed; Keycloak skipped. This workflow-only production dispatch prompted PR #1087.
- PR #1087 merged at 35074857c1b3be1ec6db71045ea30219cdea09fd; exact head 5a9ad12f6adefd5a9178cfbfc2433fd30b1141d5. Exact-head #41516145651/#41516145661 and post-merge #41516319517/#41516319576 all SUCCESS. Recovery push no longer treats reconcile-vps.yml as a push trigger; Keycloak provisioning is manual-only; cleanup workflow self-edit no longer starts cleanup. Manual/scheduled entries remain. The #1087 merge caused only validation runs.
- TCE native WF-06 #41516575222 delivered at 20:09:18Z, but all four strict HTTP 200 probes returned 503 while TCE/Auth are intentionally 0/0. WF-12 workflow_run #41516610495 verified fresh source run (age 0m, queue 0m) and forwarded heartbeat; Platform receiver #41516627460 validated exact source provenance and found reconciliation age 0m/inspection age 3m, so no fallback dispatch. Direct WF-12 schedule #41511665345 still failed freshness before this tick; consecutive cadence remains unproven.
- Latest K3s snapshot #1086: node Ready ARM64/K3s 1.36.3; disk 55%, ~19 GiB RAM. Media/MicroFE/NATS healthy; Stock Admin/new Backend ImagePullBackOff on non-ARM64 12d63b4; old Backend and unmanaged frontend 1/1; microfe-auth/Keycloak/TCE 0/0 intentionally.
- Native Platform schedule history still stale: inspection #41498271871, reconciliation #41491502003, watchdog #41491160810, recovery #41482540454, mirror #41499146752. Manual/dispatch runs do not count as cron delivery.
- Current master heads: Platform 35074857; TCE afad281f; StockDividend 38220ddf; Media 0d4fc2ac; Authentication ceb2688d. Open PRs: Platform #544/#541/#539; Auth #75/#76; none in TCE/StockDividend/Media.
- Owner blockers: StockDividend Actions-read token unverified; mirror Contents-write token missing; explicit StockDividend release authorization absent; Auth Supabase integration/migration side-effect gate remains open. No app release or production image promotion.

## 2026-11-03 03:16 ICT — Node 24 checkout pin standardized across CI workflows

- Verified official actions/checkout v7.0.1 SHA 3d3c42e5aac5ba805825da76410c181273ba90b1; action.yml uses node24.
- Platform Infra #1085 merged 4715d7d0...; 17 workflow refs updated. Exact-head manifest/workflow/SSO/Keycloak checks and post-merge #41515885218/#41515885331 PASS.
- TCE #1014 merged 76a4b9a1...; five CI/test workflows updated; exact-head WF-01P #41517007456, WF-05 #41517007487, WF-11 #41517007413, WF-02 #41517007363 PASS. Post-merge WF-02/WF-05 PASS; WF-01 #41517196734 still in progress.
- StockDividend #25 merged ba16a62e...; CI-only checkout pin; exact-head CI #41517044412 PASS; post-merge CI #41517378004 in progress; no image publisher dispatch.
- Media #68 merged 648e7daa...; CI-only checkout pin; exact-head #41517076554 and post-merge #41517278671 PASS.
- Authentication #83 merged b76a19d8...; ci.yml/web-ci.yml pins; exact-head #41517131273/#41517131277 PASS; post-merge #41517481286/#41517482354 in progress.
- 26 workflow references across five repositories now use the immutable Node24 checkout SHA. Deployment/release workflows in app repos were not changed to avoid unintended publisher/deploy triggers.
- PR #1088 tracker/inventory update merged 33358a2f...; exact-head #41516879912 and post-merge #41517242519 PASS.
- TCE WF-06 native schedule #41516575222 delivered (age/queue 0m) but public endpoints all HTTP503. WF-12 workflow_run #41516610495 and Platform receiver #41516627460 both SUCCESS with exact source provenance. WF-12 direct schedule #41511665345 remains stale; WF-07 #41476258191 PASS. One tick does not prove consecutive cadence; market-scan cron unchanged.
- PR #1085 push side effects were recorded: reconcile #41515916117 (no GitOps drift/apply, Auth runtime Secret provisioned, shared pull Secrets unchanged, Stock lane failure); Provision OIDC client #41515885560 failed HTTP503 before admin mutation; verify #41515885382 HTTP503; cleanup #41515885582 dry-run removed 0; inspection #41515885354 created snapshot #1086. PR #1087 hardening now prevents these workflow-only self-trigger paths.
- Current master heads: Platform 33358a2f; TCE 76a4b9a1; StockDividend ba16a62e; Media 648e7daa; Authentication b76a19d8. Open PRs: Platform #544/#541/#539; Auth #75/#76; none in TCE/StockDividend/Media.
- Remaining owner blockers: StockDividend Actions-read token unverified and release authorization absent; mirror token missing; Auth Supabase integration/migration gate unresolved. Stock Admin/Backend still lack ARM64 manifests for production tag 12d63b4.

## 2026-11-03 03:17 ICT — StockDividend CI Docker actions Node 24 follow-up

- StockDividend CI logs showed Node20 deprecation warning for docker/build-push-action@v6 and docker/setup-buildx-action@v3. Open PR #26 pins CI-only actions to Node24 releases: build-push-action v7.4.0 SHA c3c9e263c25d99ce0380d002d59b67737d91b0dc; setup-buildx-action v4.4.1 SHA f87e5991a6d7451dcb8d9637bfbc97413f497069. push=false remains; production deploy/publisher untouched.
- PR #26 exact-head CI #41517727670 is still in progress; do not merge until all required jobs complete SUCCESS.
- Post-merge CI after the cross-repo checkout pin: TCE WF-01/WF-02/WF-05 all SUCCESS; StockDividend CI SUCCESS with no publisher run; Media CI SUCCESS; Authentication service/web CI SUCCESS. No release workflows were triggered.
- Current open PRs: Platform #544/#541/#539; StockDividend #26; Authentication #75/#76; none in TCE/Media.

### StockDividend Docker action follow-up completed
- PR #26 merged at 60918c2f2c50e5e52d071fe36ba72b1e78a485a2 after exact-head CI #41517727670 SUCCESS. CI-only Buildx actions now use Node24 immutable pins (setup-buildx v4.4.1, build-push v7.4.0); push=false retained. Post-merge CI #41518048674 queued at update time; no publisher run.
- Production StockDividend deploy/publisher workflow remains untouched; no GHCR publication or promotion.


## 2026-11-03 03:58 ICT — release workflow Node24 pins and publisher path guard

- StockDividend PR #27 merged at `fc10f56eadba769fe102da6465bee27c9e14f9a9`; exact-head CI #41524373731 passed all five jobs. Production publisher actions are now immutable Node24 pins (checkout v7.0.1, setup-buildx v4.4.1, login v4.7.0, metadata v6.2.0, build-push v7.4.0).
- PR #27 also changed `scripts/validate-production-release-contract.sh`, which was not in publisher `paths-ignore`; merge triggered Build and Publish Images #41524676740. Its release gate output was `release_enabled=false`; promotion handoff skipped; build-and-push was still running (Scraper step active, Admin/Backend pending). No GitOps dispatch observed. Verify final digest/run conclusion.
- StockDividend PR #28 adds the validator path to `paths-ignore` and asserts it, preventing future contract-only edits from publishing unchanged images. Preserve master source pushes and workflow_dispatch.
- TCE PR #1015 pins manual-only WF-03 checkout/artifact/Docker actions to Node24; stale Buildx v3 assertion was fixed. Exact head `3f04b73deb8b84a99cf45d26bea5a7768b7ee7a5`; WF-01P and WF-02 passed, WF-05 still running.
- Auth PR #84 pins manual-only release checkout/setup-node/Docker actions to Node24; exact head `351c598132cfea05b41a054e673adf8293a63d69`; auth-service-ci running, Supabase Preview skipped. No release dispatch.
- Verified upstream Node24 commits: checkout 3d3c42e5..., setup-node 949feb24..., upload-artifact cf430e03..., download-artifact 9000827c..., login-action 81c6f93d..., metadata-action dc802804..., setup-buildx f87e5991..., build-push c3c9e263....
- Native schedules unchanged: Platform mirror #41499146752 FAIL, inspection #41498271871 PASS, reconciliation #41491502003 FAIL, watchdog #41491160810 FAIL, recovery #41482540454 PASS; TCE WF-06 #41516575222 HTTP503, WF-12 #41511665345 freshness failure, WF-07 #41476258191 PASS. No cron changes.
- K3s snapshot #41515885354: node Ready/K3s 1.36.3; Media/MicroFE/NATS healthy; Stock Admin/new Backend image-pull failure on `12d63b4`; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0 intentional.
- Preserve `reconcile-vps.yml` as sole production apply authority. No DB migration, production manifest change, promotion, shared GHCR credential change or reboot. TCE market-scan schedule unchanged.


### 2026-11-03 03:58 ICT merge follow-up
- TCE PR #1015 merged at `84119b25816d19347f8a0bc6f239914e686ff424`; exact-head WF-01P/WF-02/WF-05 all SUCCESS. Post-merge WF-01/WF-02/WF-05 runs #41524985099/#41524985162/#41524985123 were in progress. WF-03 remains manual-only; no publisher run.
- Auth PR #84 merged at `897bc7b921c7d34a3c19c945cb3d4f1affcdd6c6`; exact-head auth-service-ci #41524582582 SUCCESS, Supabase Preview SKIPPED. Post-merge auth-service-ci #41524996404 queued. Release remains manual-only; no dispatch.
- StockDividend PR #27 merged at `fc10f56eadba769fe102da6465bee27c9e14f9a9`; publisher #41524676740 was triggered because the validator script was not in `paths-ignore`. Gate output false and promotion handoff skipped; build-and-push still running. PR #28 now excludes that helper path and asserts the exclusion.
- Open PRs: Platform #544/#541/#539/#1091; StockDividend #28; Auth #75/#76; TCE/Media none.


### 2026-11-03 03:58 ICT follow-up
- StockDividend PR #28 exact head `9e166bfc85f7363da1eed2baac895d0735754f29`: release-hold contract, Admin build, Backend test/build and Scraper syntax passed; Scraper container build still running. Adds exact validator helper to publisher `paths-ignore`.
- Media PR #69 exact head `729725534471194c9dabd7081cdea191dc01f012`: Node24 pins for WF-03 publisher and CI setup-node; Media CI #41525201157 in progress. Existing Media release path filters exclude workflow and validator changes.
- Platform tracker PR #1091 exact head `97523cebce3136f4ec911917304bb198671122aa`; validate #41525056187 SUCCESS.
- StockDividend publisher #41524676740 remains in progress with promotion gate false and promotion handoff skipped; no Platform dispatch observed.


### 2026-11-03 03:58 ICT final cross-repo correction
- StockDividend #28 merged at `3b68bad71b9c3832c1ee2a6de0ce085d9ac758f9`; exact-head CI all five jobs SUCCESS. Post-merge CI #41525480316 queued; no publisher run was triggered by #28, confirming the validator path exclusion.
- StockDividend #27 merge publisher #41524676740 remains in progress: release_enabled=false, promotion handoff skipped, Scraper/Admin published, Backend build/push active, digest verification pending. No Platform dispatch observed.
- Media #69 closed as superseded after malformed test insertion; corrected PR #70 exact head `3674c4d02e5e073792b00c1b79bb3aa5163bada5`, CI #41525436728 in progress. Existing release path filters exclude workflow/contract-only changes.
- TCE #1015 merged at `84119b25816d19347f8a0bc6f239914e686ff424`; exact-head checks all PASS; post-merge WF-05/WF-02 PASS and WF-01 still running.
- Auth #84 merged at `897bc7b921c7d34a3c19c945cb3d4f1affcdd6c6`; exact-head validation PASS, Preview skipped; post-merge auth-service CI PASS. #75/#76 remain open.
- Open PRs: Platform #544/#541/#539/#1091; Media #70; Auth #75/#76; none in TCE/StockDividend.


### 2026-11-03 03:58 ICT — StockDividend publication outcome
- StockDividend publisher #41524676740 completed SUCCESS on `fc10f56eadba769fe102da6465bee27c9e14f9a9`; release_enabled=false, promotion handoff SKIPPED, atomic promotion job SKIPPED, no Platform repository_dispatch.
- Verified immutable ARM64 publisher digests: scraper `sha256:83c989df5d156d0a70de4a268a0ce35b9313dda7b1d1170da97ccd8058dd2e9b`; admin `sha256:d0d6f037c1d2801018a36921360bfee3852ee7d14e3b33ee2e0fd790dddf6ec1`; backend `sha256:1f8d5a6161da3774578a6f9d2c1e04b4efd624a516e66ab941ebddaa964233a0`. Artifacts are not promoted; production manifest remains unchanged.
- StockDividend #28 merged at `3b68bad71b9c3832c1ee2a6de0ce085d9ac758f9`; all exact-head jobs passed and its merge triggered CI only, not the publisher.
- Media #70 PR CI #41525436728 SUCCESS; separate push CI #41525425598 still running.


### 2026-11-03 03:58 ICT final merge evidence
- Media #70 merged at `763fdcd1463fe4d95c81c93d1e7ae010f2cd0cd3`; exact-head PR and push CI runs #41525436728/#41525425598 SUCCESS; post-merge Media CI #41525798015 queued. No production publisher run after merge due existing path exclusions.
- StockDividend #28 merged at `3b68bad71b9c3832c1ee2a6de0ce085d9ac758f9`; all five exact-head checks and post-merge CI #41525480316 SUCCESS; no publisher run from that merge.
- StockDividend publisher #41524676740 SUCCESS published verified ARM64 digests: scraper 83c989df..., admin d0d6f037..., backend 1f8d5a61.... Promotion gate false; handoff and atomic promotion skipped; no Platform dispatch. Production manifests remain unchanged.
- TCE #1015 merged at `84119b25816d19347f8a0bc6f239914e686ff424`; all exact-head and post-merge WF-01/WF-02/WF-05 checks SUCCESS.
- Auth #84 merged at `897bc7b921c7d34a3c19c945cb3d4f1affcdd6c6`; validate and post-merge auth-service-ci SUCCESS; Supabase Preview SKIPPED.
- Open PRs: Platform #544/#541/#539/#1092; Auth #75/#76; none in TCE/StockDividend/Media.


## 2026-11-03 03:58 ICT — final PR and workflow inventory correction
- Platform PR #1093 merged at `1d16ef3ad47eb0944aa3435619664259d1a62928`; exact-head validation #41525955931 SUCCESS; post-merge validation #41526024719 was in progress.
- Open PRs: Platform #544/#541/#539; Auth #75/#76; none in TCE, StockDividend or Media. Cross-repo docs PRs #1091/#1092 closed as superseded; #1093 merged.
- TCE #1015 and Auth #84 merged with exact-head/post-merge CI success; Media #70 merged with PR/push/post-merge CI success; StockDividend #28 merged with all five checks and post-merge CI success.
- StockDividend publisher #41524676740 SUCCESS published ARM64 immutable artifacts (scraper 83c989df..., admin d0d6f037..., backend 1f8d5a61...). Promotion gate false; handoff and atomic promotion skipped; no Platform dispatch. #28's validator path exclusion prevented a new publisher run.
- Native Platform/TCE schedule history remains as recorded in the tracker; no cron changes. TCE market-scan schedule unchanged.
- Preserve `reconcile-vps.yml` as sole production apply authority; no database migrations, production manifest changes, image promotions, credential mutations or VPS reboot.


## 2026-11-03 03:58 ICT — setup-node runtime migration inventory
- Remaining `actions/setup-node@v4` references were found in TCE WF-01P/WF-02 format/WF-11 mobile/WF-02 backend CI, StockDividend CI and Authentication service/web CI. Dedicated PRs #1016, #29 and #85 replace them with immutable Node24 setup-node v7.1.0 SHA `949feb2413d6458794dcd2491c4babbbce0c15c1`, preserving application Node versions and build/test commands.
- PR #1016 exact head `ee6ca523c434e2d90ab06387f89611c8be88c772`: CI in progress.
- PR #29 exact head `3e0ce3306fcf1f6d8c39c2f3d84a06aa8fb85d63`: CI in progress; only CI workflow path changed, production publisher not triggered.
- PR #85 exact head `0561e3f112e1d78cc7a44af696ab5d2249b94e2c`: service/web CI in progress; Preview skipped.
- Release publishers in TCE #1015, StockDividend #27, Media #70 and Auth #84 now use verified immutable Node24 action releases. TCE/Auth release workflows remain manual-only. Media/Stock publisher path filters prevent CI/contract-only changes from publishing.
- Platform current master `773ae46ba87894fd3f00fc3cf2375375285d0e02`; open PRs #544/#541/#539 plus this tracker PR. TCE #1016; StockDividend #29; Media none; Auth #75/#76/#85.
- Preserve sole production apply authority `reconcile-vps.yml`; no direct SSH/Compose authority. No release dispatch, GitOps promotion, DB migration, cron change or VPS reboot. TCE market-scan schedule unchanged.

## 2026-11-03 04:57 ICT — Node24 CI migration completed

- TCE PR #1016 merged at `2beeedc5a875e0017dbdd0c49e432b3803bbe33d`; exact-head WF-11 #41526244453, WF-02 #41526244889, WF-01P #41526244499 and WF-05 #41526244527 all SUCCESS.
- StockDividend PR #29 merged at `3d67cbb6bacda7d8c46a7f484129091a8fe3af6e`; exact-head CI #41526269593 SUCCESS.
- Authentication PR #85 merged at `bf5ac54a2c48ad4c439d2c1241aca08c4960bc18`; exact-head auth-service-ci #41526295672 and auth-web-ci #41526295607 SUCCESS. Supabase Preview SKIPPED and not counted as production integration evidence.
- Node24 setup-node CI migration is complete for all three remaining application repositories. Publisher workflows across TCE, StockDividend, Media and Auth were previously migrated to immutable Node24 action commits. Application Node versions, package managers, caches, build/test commands and release triggers were preserved.
- Current open PRs: Platform #544/#541/#539 (draft); Authentication #75/#76; none in TCE, StockDividend or Media.
- StockDividend immutable ARM64 artifacts from publisher #41524676740 remain unpromoted: scraper `83c989df...`, admin `d0d6f037...`, backend `1f8d5a61...`. Release gate false; no Platform dispatch; GitOps production image references unchanged.
- Latest available K3s snapshot #41515885354 is stale. It records Stock Admin/new Backend ImagePullBackOff on old tag `12d63b4`, while Media/MicroFE/NATS were healthy and TCE/Auth/Keycloak remained intentionally 0/0.
- Platform native inspection/reconciliation/watchdog/mirror and TCE WF-06/WF-12 schedules remain without proven consecutive cadence recovery. WF-07 and Platform recovery have successful isolated schedule evidence. Do not change any cron expression or TCE market-scan schedule.
- Preserve `reconcile-vps.yml` as the only production apply authority. No direct SSH/Compose deployment authority added. No release dispatch, GitOps promotion, DB migration, secret mutation, replica change or VPS reboot.

## 2026-11-03 05:05 ICT — remaining Node24 workflow pins

- TCE PR #1017 merged at `5d299bea8ba482876ccaa291c68b0ee3f829350c`. Exact-head WF-02 #41533787129, WF-05 #41533787740, WF-08B #41533787314 and WF-11 #41533787316 all SUCCESS. WF-08B release handoff, image publication and dispatch jobs were skipped for the PR event.
- StockDividend PR #30 merged at `efdb0844e868367d29bbeb5393430cd73d6b6f38`. Exact-head CI #41533796010 SUCCESS across all five jobs; scraper image build remained push=false. Weekend schedule `0 1 * * 0,6` unchanged.
- Platform PR #1097 remains open. Exact-head action validation #41533921909 SUCCESS after fixing yamllint comment spacing. Exact-head manifest validation #41533921800 is still running at network-boundary validation; no merge until SUCCESS.
- Current open PRs: Platform #1097/#544/#541/#539; Auth #75/#76; none in TCE, StockDividend or Media. Tracker PR #1096 is open separately.
- Node24 action runtime migration is complete for TCE artifact upload/download, TCE manual safe-setup checkout, StockDividend Python/Go and weekend scraper actions. Platform GitOps image-promotion checkout/login/Buildx pins remain pending #1097.
- No release dispatch, GHCR publication, GitOps promotion, DB migration, credential mutation, replica change, VPS reboot or cron change. Preserve `reconcile-vps.yml` as the sole production apply authority; TCE market-scan schedule unchanged.

## 2026-11-03 05:15 ICT — Node24 action pins merged

- Platform #1097 merged at `60cbeb5ae2d4ea2deb5643503c20f0811a02cdcf`; exact-head workflow and manifest validations #41533921909/#41533921800 SUCCESS after correcting yamllint comment spacing.
- TCE #1017 merged at `5d299bea8ba482876ccaa291c68b0ee3f829350c`; exact-head WF-02/WF-05/WF-08B/WF-11 SUCCESS. MicroFE image publication and Platform dispatch jobs were skipped on PR.
- StockDividend #30 merged at `efdb0844e868367d29bbeb5393430cd73d6b6f38`; exact-head CI #41533796010 SUCCESS across all five jobs. Production publisher ignores `.github/**`; weekend scraper cron remains `0 1 * * 0,6`.
- Verified the immutable upstream action metadata at the pinned commits: checkout, artifact upload/download, Docker login/Buildx, setup-python and setup-go all declare Node24 runtime.
- Current open PRs: Platform #544/#541/#539 (draft); Authentication #75/#76. TCE, StockDividend and Media have no open PRs. Tracker PR #1096 remains open and needs base/mergeability re-check.
- StockDividend production overlay still uses old Admin/Backend tag `12d63b4`; newly published ARM64 digests remain unpromoted. K3s snapshot #41515885354 remains stale. Native schedule cadence is not proven consecutive.
- No production release, GitOps promotion, DB migration, credential mutation, replica change, VPS maintenance or cron change. `reconcile-vps.yml` remains sole production apply authority; TCE market-scan schedule unchanged.

## 2026-11-03 05:25 ICT — post-merge state refresh

- Platform tracker PR #1096 merged at `a362c9a6e4e001b1a1309afd7eeee4ed099c0e13`; docs-only and no PR-triggered workflow run/status contexts surfaced.
- Current master heads: Platform `a362c9a6e4e001b1a1309afd7eeee4ed099c0e13`; TCE `5d299bea8ba482876ccaa291c68b0ee3f829350c`; StockDividend `efdb0844e868367d29bbeb5393430cd73d6b6f38`; Media `763fdcd1463fe4d95c81c93d1e7ae010f2cd0cd3`; Auth `bf5ac54a2c48ad4c439d2c1241aca08c4960bc18`.
- Open PRs: Platform #544/#541/#539 (draft); Auth #75/#76; none in TCE, StockDividend or Media.
- Node24 action migration follow-ups merged: Platform #1097 (manifest/workflow validation PASS), TCE #1017 (WF-02/WF-05/WF-08B/WF-11 PASS), StockDividend #30 (all five CI jobs PASS). Exact immutable action metadata at selected commits declares Node24.
- StockDividend production overlay still references Admin/Backend tag `12d63b4`; new ARM64 digests are unpromoted and release remains disabled. Scraper schedule `0 1 * * 0,6` unchanged.
- K3s evidence remains stale at #41515885354; Stock Admin/new Backend image pull failures persist in last verified snapshot. Native Platform/TCE schedule cadence is not proven consecutive. No cron change.
- No production promotion, DB migration, credential mutation, replica change, VPS maintenance or cron modification. Preserve `reconcile-vps.yml` as sole production apply authority and keep TCE market-scan schedule unchanged.


## 2026-11-03 06:03 ICT — cross-repo current state and Auth web CI follow-up
- Master heads: Platform `f9bbed9d`; TCE `5d299bea`; StockDividend `efdb0844`; Media `763fdcd1`; Auth `bf5ac54a`.
- Open PRs: Platform #544/#541/#539 (draft); Auth #75/#76/#86; none in TCE, StockDividend or Media.
- Auth master web CI #41533191601 failed at `npm ci` with EUSAGE because generated lock omitted optional package `@tailwindcss/oxide-wasm32-wasi`. PR #86 explicitly includes optional dependencies; exact-head auth-web-ci #41542677868 and auth-service-ci #41542677119 were still running. No merge yet.
- Auth #75/#76 validate SUCCESS, but Supabase Preview SKIPPED. #75 remains blocked by production-branch Supabase GitHub integration / unresolved migration provenance; do not merge or migrate.
- TCE master WF-01/WF-02/WF-05, StockDividend master CI and Media master CI are SUCCESS. StockDividend immutable ARM64 publisher #41524676740 produced scraper/admin/backend digests recorded in the readiness tracker; all remain unpromoted because release is disabled and explicit authorization is absent.
- Latest native schedules: Platform inspection #41498271871 SUCCESS, recovery #41482540454 SUCCESS, reconciliation #41491502003 FAILURE (Stock health), watchdog #41491160810 FAILURE/stale, mirror #41499146752 FAILURE (missing token). TCE WF-06 #41516575222 FAILURE (HTTP 503), WF-12 #41511665345 freshness FAILURE, WF-07 #41476258191 SUCCESS. No consecutive cadence recovery established.
- Latest K3s snapshot #41515885354 is stale: node Ready/ARM64, Media/MicroFE/NATS healthy, Stock Admin/new Backend ImagePullBackOff on `12d63b4`, old Backend and unmanaged legacy Frontend 1/1, TCE/Auth/Keycloak 0/0.
- Owner actions: configure `PLATFORM_INFRA_MIRROR_TOKEN` (destination-only Contents:write); verify `STOCKDIVIDEND_ACTIONS_READ_TOKEN` (StockDividend-only Actions:read); provide explicit StockDividend release authorization.
- No production promotion, image-reference/credential/DB/replica/schedule change, migration, restart, image deletion, VPS reboot or maintenance occurred. Preserve `reconcile-vps.yml` as sole apply authority and leave all cron expressions, including TCE market-scan, unchanged.


## 2026-11-03 06:08 ICT — Auth web CI repair merged
- Auth PR #86 merged at `1f39b18d9dd286da9dde32a79c4da269b19d5cfd`. It fixes master auth-web-ci #41533191601, where `npm ci` failed because the ephemeral lock omitted `@tailwindcss/oxide-wasm32-wasi`. Explicit `--include=optional` on lock generation and clean install fixed exact-head auth-web-ci #41542677868; auth-service-ci #41542677119 also passed. Both exact-head PR runs include test/typecheck/lint/build/container validation.
- Post-merge master auth-web-ci #41542942080 and auth-service-ci #41542941957 were still running at container build when inspected; do not claim post-merge completion.
- Platform tracker PR #1099 merged at `ae3971c907c27f166b435c29ea60cee28f225f38`; exact-head validation #41542838607 and post-merge #41542962452 SUCCESS.
- Current open PRs: Platform #544/#541/#539 (draft); Auth #75/#76; none in TCE, StockDividend or Media.
- TCE/StockDividend/Media latest master CI runs remained SUCCESS. StockDividend ARM64 digests remain unpromoted; release disabled.
- Native Platform/TCE schedule cadence and K3s snapshot remain stale as detailed in the readiness tracker. Mirror token and StockDividend Actions-read token remain owner blockers; explicit release authorization absent.
- No production apply, promotion, database migration, credential mutation, desired-replica change, schedule change, image deletion, Pod restart or VPS maintenance. Preserve `reconcile-vps.yml` as sole apply authority; TCE market-scan schedule unchanged.


## 2026-11-03 06:58 ICT — Node24 completion follow-up and current runtime
- Platform master is `1edb289d17afbf62feed3cfd069343941d53025c`; TCE `5d299bea8ba482876ccaa291c68b0ee3f829350c`; StockDividend `efdb0844e868367d29bbeb5393430cd73d6b6f38`; Media `763fdcd1463fe4d95c81c93d1e7ae010f2cd0cd3`; Authentication `1f39b18d9dd286da9dde32a79c4da269b19d5cfd`. Open PRs before this follow-up: Platform #544/#541/#539; Auth #75/#76; none in TCE, StockDividend or Media. Inspection PR #1101 exact-head validated and merged at Platform master `1edb289d`.
- Fresh inspection #41547614220 (workflow_dispatch) completed SUCCESS; snapshot generated 2026-11-02T23:43:46Z. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available, Docker 29.1.3, containerd runtime 2.3.2-k3s2, runner services active/policy v14. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend and unmanaged Frontend 1/1. Maintenance remains pending (`restart_required=yes`).
- Scheduled recovery #41547230804 SUCCESS dispatched reconciliation #41547248939 because the prior reconciliation was 210 minutes old. Shared reconcile and TCE/Media/Auth/MicroFE lanes succeeded; StockDividend failed on missing ARM64 manifest for Admin/Backend tag `12d63b4`; Keycloak skipped. Recovery #41547565460 SUCCESS. No image promotion or manifest apply.
- Native Platform schedules: recovery #41547230804 SUCCESS; mirror #41499146752 missing token; inspection #41498271871 SUCCESS; reconciliation #41491502003 Stock health failure; watchdog #41491160810 stale failure. TCE native schedules: WF-06 #41516575222 HTTP 503 failure, WF-12 #41511665345 freshness failure, WF-07 #41476258191 SUCCESS. No consecutive cadence recovery.
- StockDividend immutable ARM64 digests from publisher #41524676740 remain unpromoted; release disabled. Mirror token missing; StockDividend Actions-read token unverified; explicit release authorization absent. Auth #75/#76 remain gated on production Supabase integration/migration provenance.
- A remaining Node20 deprecation warning identified four `peter-evans/create-pull-request` references in Platform inspection/promotion workflows. Upstream v8.1.1 tag resolves to immutable commit `5f6978faf089d4d20b00c7766989d076bb2fc7f1`; its `action.yml` declares Node24 and retains the outputs used by the workflows. Dedicated branch `chore/platform-create-pull-request-node24-20261103` upgrades all four references and adds static pin-count/legacy-SHA regression assertions. Validation pending.
- Preserve all CI/test/security/release/manual/scheduled jobs and the sole production apply authority `reconcile-vps.yml`. No production promotion, secret/credential/DB/replica/image/cron change, restart, image deletion or VPS maintenance. TCE market-scan schedule unchanged.


## 2026-11-03 07:05 ICT — Platform PR automation Node24 runtime and scheduled reconciliation evidence
- Platform PR #1102 merged at `6640e2a1ea07b8c015c0687c146045de2d1e1832`; exact-head validate-manifests #41549653092 and validate-github-actions #41549653094 PASS; post-merge #41549730733 and #41549730795 PASS. Four `peter-evans/create-pull-request` references now use v8.1.1 immutable Node24 commit `5f6978faf089d4d20b00c7766989d076bb2fc7f1`; static contract enforces 1 inspection + 3 promotion pins and rejects old SHA.
- Runtime exercise: inspect-vps push run #41549730731 SUCCESS executed v8.1.1, created PR #1103, exact-head manifest validation #41549830500 PASS, and auto-squash-merged exact head `41624282a92e606b93f62da74e8caf81549b49b8` to master `63ed484d9ad5e5b491dd171a927709bd957361b2`. Logs show zero Node20/deprecation mentions and zero legacy action SHA references. GitOps promotion path remains CI-validated, not release-exercised.
- Native Platform reconciliation #41549849545 (schedule) shared job SUCCESS, no GitOps drift, production apply skipped, shared GHCR pull Secret unchanged, Auth runtime Secret provisioned/verified, and permanent Stock image-pull restarts skipped. Lanes: MicroFE/Auth/TCE/Media PASS; StockDividend FAIL; Keycloak skipped. Stock Admin x2 and new Backend remain ImagePullBackOff on tag `12d63b4` due missing ARM64 manifest. Recovery #41550174709 SUCCESS and correctly avoided duplicate fallback dispatch because source reconciliation and inspection were fresh.
- Latest inspection #41549730731 is push-triggered (not native schedule), snapshot generated 2026-11-03T00:01:09Z: node Ready/ARM64, K3s 1.36.3, disk 55%, ~19 GiB available; Media/MicroFE/NATS healthy; Stock Admin/new Backend pull failures; old Backend/legacy Frontend 1/1; TCE 0/0; Keycloak 0/0, OIDC probes 503; maintenance pending.
- Native Platform schedule: reconciliation #41549849545 Stock lane failure; watchdog #41549659062 stale inspection failure; recovery #41547230804 SUCCESS; mirror #41499146752 missing token; latest native inspection #41498271871. Push/manual inspections are not counted as schedule ticks. TCE native WF-06 #41516575222 HTTP 503, WF-12 #41511665345 freshness failure, WF-07 #41476258191 SUCCESS; no consecutive cadence recovery.
- Current master heads: Platform `63ed484d`, TCE `5d299bea`, StockDividend `efdb0844`, Media `763fdcd1`, Auth `1f39b18d`. Open PRs: Platform #544/#541/#539 (draft), Auth #75/#76; none in TCE/Stock/Media. Auth #75/#76 validate PASS but Supabase Preview SKIPPED; keep migration/integration side-effect gates.
- StockDividend ARM64 publisher digests remain unpromoted; release false/unset. Mirror token missing, StockDividend Actions-read token unverified, explicit production release authorization absent. Preserve all CI/security/manual/release/scheduled workflows and `reconcile-vps.yml` as sole production apply authority. No DB/image/manifest/replica/schedule change, restart, image deletion or VPS maintenance. TCE market-scan schedule unchanged.


## 2026-11-03 07:07 ICT — post-merge and latest watchdog evidence
- Platform docs PR #1104 merged at `b77a92030f0925dee95ef7600681250b2c6637ed`; post-merge validate-manifests #41550385614 SUCCESS. Docs-only merge did not trigger recovery or production reconciliation.
- Latest native watchdog #41550202827 FAILURE: scheduled reconciliation #41549849545 age 2m, no lane queue over 15m; native inspect-vps remains #41498271871 at 352m (>75m). Push inspection #41549730731 is not counted as native schedule.
- Recovery #41550174709 SUCCESS and skipped duplicate fallback because latest reconciliation/inspection activity was fresh. Native inspection schedule still requires consecutive scheduled ticks; no cron or TCE market-scan schedule changed.


## 2026-11-03 08:01 ICT — recovery source-run audit contract

- TCE WF-07 native schedule #41556575907 was validated by Platform recovery #41556605772 through the authenticated `tce-schedule-heartbeat` repository_dispatch payload (source repository, scheduled event, workflow path, run ID, full SHA, and WF-12 heartbeat ID).
- The fallback dispatched reconciliation #41556624187 only after the latest master reconciliation was 53m old. Payload was `mode=apply`, `allow_image_changes=false`, `target_app=all`; shared preflight passed and no manifest drift meant production manifest apply was skipped. TCE/Auth/MicroFE/Media lanes passed; StockDividend failed on the known old ARM64-incompatible image; Keycloak was skipped.
- Post-reconciliation recovery #41556855046 verified the exact source run and found the latest inspection 58m old (<75m), so no duplicate inspection dispatch was made.
- Audit issue: repository_dispatch run #41556605772 displayed `source none` because the run-name only read `inputs.source_run_id`. The follow-up contract exposes `inputs.source_run_id`, `github.event.client_payload.source_run_id`, and `github.event.workflow_run.id` in the run title and enforces this through `validate-workflow-contracts.py`. Functional trigger/dispatch behavior is unchanged.
- Native inspection schedule remains stale at #41498271871; push inspection #41549730731 is not counted as a native tick. Preserve all existing cron expressions and the TCE market-scan schedule.

## 2026-11-03 09:00 ICT / 02:00 UTC — workflow ownership and readiness follow-up

- **Repository state:** Platform Infra master `1f1186bb6ce0b98bc136b54f23711005e4886bef`; TCE `5d299bea8ba482876ccaa291c68b0ee3f829350c`; StockDividend `efdb0844e868367d29bbeb5393430cd73d6b6f38`; Media `763fdcd1463fe4d95c81c93d1e7ae010f2cd0cd3`; Authentication `1f39b18d9dd286da9dde32a79c4da269b19d5cfd`. Open PRs: Platform #544/#541/#539 (draft), StockDividend #31, Auth #75/#76; no open TCE or Media PRs.
- **StockDividend CI:** PR #31 adds a non-publishing backend image job to `.github/workflows/ci.yml` using Buildx with `load: true`, `push: false`, and an executable/precondition check for `/app/migrate`. Exact-head run #41563638198 was still in progress at 09:00 ICT; release-hold and scraper syntax jobs passed, other build jobs were running. No merge until exact-head checks all succeed.
- **StockDividend publisher ownership:** `.github/workflows/deploy.yml` remains the app-owned immutable ARM64 publisher. A merge changing `backend/**` is expected to publish Scraper/Admin/Backend artifacts from master. The release-enable variable remains false/unset; the Platform repository_dispatch and GitOps promotion jobs must remain skipped. No release was dispatched.
- **Backend runtime contract:** PR #31 changes `backend/Dockerfile` to compile `cmd/migrate` as a static executable and copy it to `/app/migrate`; it removes the previous source-only `migrate_src.go` copy. The CI probe deliberately runs without `MONGO_URI` and expects fail-closed configuration validation, not a database connection. This does not authorize or execute a migration.
- **Platform inspection:** `.github/workflows/inspect-vps.yml` retains its native schedule `2,32 * * * *`, read-only inspection and exact-head inspection PR validation. Latest snapshot is generated 2026-11-03T01:11:21Z in commit #1107; source event was not independently exposed by the current connector query, so classify it as fresh inspection evidence only, not a proven native cron tick.
- **Platform reconciliation/recovery:** `reconcile-vps.yml` remains the sole production apply authority; recovery/watchdog observe and dispatch only. The last documented native schedule history is inspection #41498271871, reconciliation #41549849545, watchdog #41550202827, mirror #41499146752 and recovery #41547230804. Keep dispatch/workflow_run/push runs distinct from native schedule events.
- **TCE schedules:** WF-06/WF-07/WF-12 cron declarations and strict public HTTP 200 assertions remain unchanged. Last documented native runs: WF-06 #41516575222 (HTTP 503 health failure), WF-07 #41556575907 (SUCCESS), WF-12 #41511665345 (freshness failure). Do not count the WF-07 forwarded heartbeat as a direct WF-12 schedule tick. TCE market-scan schedule unchanged.
- **K3s snapshot #1107:** Node Ready/ARM64, K3s 1.36.3+k3s1, Docker 29.1.3, containerd 2.3.2-k3s2, disk 55%, ~19 GiB available RAM, runner services active/policy v14. Media, MicroFE Shell/WS and NATS are 1/1; Stock Admin two Pods and new Backend Pod are ImagePullBackOff on old tag `12d63b4`; old Backend and legacy Frontend are 1/1; TCE/Auth/Keycloak-related workloads remain 0/0. No rollout or maintenance.
- **Owner gates:** mirror token (destination-only Contents:write), StockDividend Actions-read token (presence unverified), explicit StockDividend release authorization, and Auth Supabase integration/migration provenance review remain outstanding.
- Preserve CI/test/security, backup, manual, release and scheduled workflows. No duplicate SSH/Compose deployment authority. No credential, database, production image, manifest, replica, cron or maintenance change. `reconcile-vps.yml` remains sole apply authority.

## 2026-11-03 09:05 ICT / 02:05 UTC — StockDividend migration image contract merged

- StockDividend PR #31 merged at `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. Exact-head CI run #41563638198 completed SUCCESS across all six jobs, including the new backend runtime-image/migration-binary job.
- The new CI job builds a non-publishing amd64 backend image, verifies executable `/app/main` and `/app/migrate`, and verifies that migration exits on missing `MONGO_URI` before any database connection. It does not run a migration.
- The backend Dockerfile now compiles the migration command as a static executable; it no longer copies the Go source file into the runtime image. The master publisher's `backend/**` path should start an app-owned ARM64 publication after merge. No post-merge publisher run/digests were returned by the current connector query, so publication remains unverified.
- The publisher's production release hold remains in place. No Platform repository_dispatch, GitOps PR, manifest promotion, or production migration was observed. Do not infer a release from the successful CI image build.
- Platform runtime README now distinguishes the source/Dockerfile fix and CI evidence from production ARM64 publication, promotion, and separately authorized migration execution.

## 2026-11-03 09:07 ICT / 02:07 UTC — post-merge workflow inventory correction

- Current master heads: Platform Infra `d2051f67f1a82bf06ff940a5aee08c4d4557189b`; TCE `5d299bea8ba482876ccaa291c68b0ee3f829350c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `763fdcd1463fe4d95c81c93d1e7ae010f2cd0cd3`; Authentication `1f39b18d9dd286da9dde32a79c4da269b19d5cfd`.
- Open PR inventory: Platform #544/#541/#539 (draft); Authentication #75/#76; no open TCE, StockDividend or Media PRs. StockDividend #31 and Platform #1108 are merged.
- StockDividend PR #31 exact-head CI #41563638198 SUCCESS: Backend tests/build, Backend runtime image/migration binary, Admin build, Scraper syntax, Scraper image and release-hold contract all passed. The backend image test uses `push: false`, checks `/app/migrate` is executable, and verifies the missing-`MONGO_URI` fail-closed path. It does not execute a migration.
- StockDividend `deploy.yml` remains app-owned immutable ARM64 publisher. The merged `backend/Dockerfile` path should trigger master publication, but no post-merge publisher run/digests were returned by the current master workflow-run query. Keep the production release hold and do not dispatch Platform promotion based on CI alone.
- Platform PR #1108 exact-head validation #41563926388 SUCCESS and merge #d2051f67. Its docs-only changes record the fresh K3s snapshot and distinguish CI image packaging from production ARM64 publication and migration authorization.
- Platform `inspect-vps.yml` schedule remains `2,32 * * * *`; latest inspection artifact #1107 was generated at 01:11:21Z, but the source event was not independently exposed. Keep native-schedule status unverified until an event= schedule run is identified.
- Platform `reconcile-vps.yml` remains the only production apply authority. Recovery/watchdog remain observer/dispatcher. TCE WF-06/WF-07/WF-12 cron and market-scan schedule remain unchanged.
- Runtime: Stock Admin and new Backend Pods remain ImagePullBackOff on old tag `12d63b4`; Media, MicroFE Shell/WS and NATS are 1/1; old Stock Backend and legacy Frontend are 1/1; TCE/Auth/Keycloak workloads remain 0/0 in the last snapshot. GitOps drift clean.
- Outstanding owner gates: mirror destination Contents:write token, StockDividend Actions:read token, explicit StockDividend production release authorization, and Auth Supabase/migration provenance review. Preserve useful CI/test/security/manual/release/scheduled workflows and avoid a second SSH/Compose production authority.


## 2026-11-03 03:03 UTC — latest cross-repo workflow evidence

- **Platform Infra master:** `f4fd705444b92ce28a5498280ffc9e4d6a971db0`; open draft PRs #544/#541/#539. #1110 merged docs-safe production reconcile trigger/scope handling. Exact-head checks #41569698092, #41569698093 and #41569697954 all SUCCESS.
- **TCE Dashboard master:** `5d299bea8ba482876ccaa291c68b0ee3f829350c`; no open PRs. Latest master build/format/backend tests #41533998356/#41533998448/#41533998355 SUCCESS. Native WF-06 #41565175484 FAILURE on strict public health endpoints; WF-07 #41557498266 SUCCESS; WF-12 scheduled #41562429843 FAILURE. WF-12 workflow_run #41565215560 is not a native schedule tick. TCE market-scan schedule unchanged.
- **StockDividend master:** `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no open PRs. CI #41563856934 SUCCESS. App-owned native ARM64 publisher #41563856933 SUCCESS and verified full-SHA tags/digests: scraper `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`, admin `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`, backend `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. All three manifests are `linux/arm64`. Release gate output false; Platform handoff and promotion dispatch skipped. No production promotion.
- **Media Generation master:** `763fdcd1463fe4d95c81c93d1e7ae010f2cd0cd3`; no open PRs. Latest master CI #41525798015 SUCCESS.
- **Authentication master:** `1f39b18d9dd286da9dde32a79c4da269b19d5cfd`; open PR #75 (non-draft) and #76 (draft). Both current-head `validate` SUCCESS; Supabase Preview SKIPPED. Master web CI #41542942080 and service CI #41542941957 SUCCESS. Keep production migration and integration side-effect gates.
- **Production apply ownership:** `reconcile-vps.yml` remains the sole production apply authority. PR #1110 excludes Markdown-only app paths from its push trigger and makes the push-scope resolver ignore app docs before app matching. This prevents a docs-only README update from launching a production lane while preserving manifest-triggered reconciliation.
- **Runtime status:** latest verified snapshot #41558049412 is stale against the 75-minute inspection budget. Stock Admin/new Backend remain ImagePullBackOff on production tag `12d63b4`; the new immutable ARM64 images are published but unpromoted. Media/MicroFE/NATS were healthy in the snapshot; TCE/Auth/Keycloak remain scale-to-zero.
- **Owner gates:** mirror destination Contents:write token missing; StockDividend Actions:read token unverified; explicit StockDividend release authorization absent; Auth Supabase/migration provenance review pending. Preserve CI/test/security, manual/release/scheduled jobs and do not create a competing SSH/Compose production authority.


## 2026-11-03 03:07 UTC — recovery trigger and inspection update

- **Platform Infra master:** `4a2ba7b3e544ef51c538d151cefec594e1dceafa`. Merged #1110 (Markdown-safe reconcile scope), #1111 (StockDividend ARM64 digest evidence), #1112 (Markdown/scope-only recovery exclusions), and automated inspection #1113. Current open drafts #544/#541/#539 remain unmergeable.
- **Recovery push filters:** both `reconcile-vps.yml` and `recover-stale-ops.yml` exclude Markdown-only paths under `apps/**`. Recovery also excludes `scripts/resolve-push-deployment-scope.sh`; the workflow contract validator enforces these boundaries. Docs/routing-only changes must not start production reconciliation.
- **Recent recovery event:** #41569753016 dispatched #41569769227 with `mode=apply`, `allow_image_changes=false`, `target_app=all` after the previous reconciliation exceeded the 20-minute budget. Shared preflight passed, Auth runtime Secret was provisioned/verified, GHCR pull Secrets were unchanged, GitOps drift was clean and manifest apply was skipped. StockDividend lane failed on old tag `12d63b4`; Auth/Media/MicroFE/TCE passed; Keycloak skipped. Post-reconcile recovery #41570003612 dispatched read-only inspection #41570085903.
- **Docs-only recovery observation:** #41570017559 was triggered by README-only PR #1111 and did not dispatch because reconciliation #41569769227 was fresh. PR #1112 now prevents future app Markdown and scope-resolver-only pushes from triggering recovery bootstrap.
- **Latest inspection:** #41570085903 is a successful `workflow_dispatch` fallback; inspection PR #1113 exact-head validated and merged at #bb4fc5. Snapshot generated 03:05:43Z: node Ready/ARM64, K3s 1.36.3+k3s1, Docker 29.1.3, containerd 2.3.2-k3s2, disk 55%, ~19 GiB RAM available, runners active/policy v14. Stock Admin two Pods and new Backend Pod ImagePullBackOff on `12d63b4`; old Backend and legacy Frontend 1/1. Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak remain scale-to-zero; OIDC HTTP 503. Pending host updates/restart required; no maintenance.
- **Native schedules:** Platform latest scheduled inspection #41558049412 SUCCESS but stale; mirror #41560381641 FAILURE (missing token); reconcile #41549849545 FAILURE (StockDividend); watchdog #41549659062 FAILURE (stale inspection); recovery #41547230804 SUCCESS. Manual inspection #41570085903 does not count as schedule recovery. TCE WF-06 #41565175484 FAILURE, WF-07 #41557498266 SUCCESS, WF-12 schedule #41562429843 FAILURE; WF-12 workflow_run #41565215560 is not a native schedule tick.
- **StockDividend immutable publication:** publisher #41563856933 verified ARM64 full-SHA digests for scraper/admin/backend. Release-gate output false, so no runtime event dispatch or promotion. Stock sender payload self-test passed in CI #41563856934; Platform receiver/provenance/digest contract passed in #41570224904. This is static sender/receiver contract evidence, not a runtime handoff.
- **Other repos:** TCE #41533998356/#41533998448/#41533998355 SUCCESS; Stock CI #41563856934 SUCCESS; Media #41525798015 SUCCESS; Auth web/service #41542942080/#41542941957 SUCCESS. Auth #75/#76 validate PASS, Supabase Preview SKIPPED; keep migration/integration gate.
- **Owner gates:** mirror destination Contents:write token missing; StockDividend Actions:read token unverified; explicit StockDividend release authorization absent; Auth Supabase/migration provenance pending. Preserve CI/security/manual/release/scheduled workflows and `reconcile-vps.yml` as sole production apply authority. TCE market-scan schedule unchanged.


## 2026-11-03 03:12 UTC — StockDividend handoff schema validation

- Platform PR #1115 merged at `673f338179f13188ad0cc07e25918be3a9b6131a`. Exact-head #41570623475 (manifest validation) and #41570623524 (workflow contract/lint) SUCCESS; post-merge #41570702258/#41570702263 SUCCESS.
- Platform receiver contract now pins the `stockdividend-images-published` event and each consumed `client_payload` field (app, commit, backend/admin digests, source run ID, source workflow path, source event, source head SHA), plus full-SHA/tag equality, approved publisher workflow/event and digest formats.
- StockDividend sender contract self-test passed in master CI #41563856934. The publisher #41563856933 successfully verified ARM64 full-SHA digests, but the release gate output false; handoff validation and promotion dispatch jobs were skipped. Sender/receiver schema is statically validated; no runtime dispatch or promotion occurred.
- Platform master #673f338 is current. Open PRs remain draft #544/#541/#539 and Auth #75/#76; no open TCE, StockDividend or Media PRs. Production release and migration gates remain closed.


## Scheduled private mirror health and ownership

- Platform Infra workflow mirror-locally-uncensored.yml remains an independent hourly mirror job at 17 * * * *. It mirrors refs/history to phanthienquoc/locally-uncensored-private; it is not a production deployment authority.
- reconcile-schedule-watchdog.yml now checks the mirror workflow state, latest native event=schedule run, 90-minute freshness, and completed success conclusion through read-only GitHub Actions API calls.
- Push-triggered post-merge smoke treats stale/missing/failed historical mirror evidence as warnings; scheduled/manual/fallback watchdog runs fail closed. workflow_dispatch and push runs never satisfy native schedule freshness.
- The mirror job uses only PLATFORM_INFRA_MIRROR_TOKEN. Owner configuration: Platform Infra repository Actions secret (or organization secret scoped only to Platform Infra), destination repository restricted to phanthienquoc/locally-uncensored-private with Contents:write. Do not reuse GHCR or application release-handoff credentials.
- Missing token remains an explicit failure, not a skipped/successful mirror. Latest confirmed native mirror run #41560381641 failed before clone/push because the secret was empty. The schedule remains enabled in YAML; token provisioning is an owner action.


## 2026-11-03 — recovery-controller schedule is now part of the watchdog inventory
- `recover-stale-ops.yml` remains the independent 15-minute recovery controller at `10,25,40,55 * * * *`; it validates source run provenance and dispatches only the existing `reconcile-vps.yml` apply authority or read-only `inspect-vps.yml` fallback.
- `reconcile-schedule-watchdog.yml` now observes the recovery workflow's native `event=schedule` history, active state, 45-minute freshness budget and completed SUCCESS conclusion. It also runs after native scheduled recovery completions.
- Push smoke is warning-only for stale/missing historical recovery evidence; scheduled/manual/fallback watchdog invocations fail closed. Dispatch/workflow_run/push runs do not count as native schedule delivery.
- This adds observability only. It does not add a deployment authority, alter recovery behavior, or change any cron expression.


## 2026-11-03 — exact recovery freshness boundary
- PR #1119 added a read-only native schedule/result check for \`recover-stale-ops.yml\`; exact-head and post-merge validation passed, and the post-merge push smoke executed the new step.
- Follow-up uses elapsed seconds for the 45-minute threshold rather than integer-minute truncation. This prevents a run at 45m35s from being treated as within a 45-minute budget.
- Native schedule history remains distinct from push, workflow_dispatch, repository_dispatch and workflow_run events. No cron expression or production deployment authority changes.


## 2026-11-03 — PR #1120 exact freshness boundary merged
- Platform PR #1120 merged at \`cf24f57a04ce83fd320c6946dbceeb8ded1cf1c7\`; exact-head and post-merge workflow/manifests checks passed.
- The recovery-controller watchdog now compares elapsed seconds against \`MAX_RECOVERY_AGE_MINUTES * 60\`; it no longer relies on integer-minute truncation.
- Post-merge push smoke #41581747151 exercised the check and emitted a warning for native recovery run #41577147958 at 48 minutes old. Push smoke is diagnostic only; scheduled/manual/fallback watchdog runs still fail closed.



## 2026-11-03 12:56 ICT / 05:56 UTC — exact-second watchdog and queue budget follow-up

- Re-read all five master refs, open PRs, latest master workflow runs, and the deployment tracker. Current heads: Platform `93450578`, TCE `5d299bea`, StockDividend `50ba0dfb`, Media `763fdcd1`, Auth `1f39b18d`.
- Platform open PRs #544/#541/#539 remain draft/non-mergeable; #1122 adds exact-second freshness and queue enforcement. Auth #75/#76 remain open behind integration/migration side-effect gates. No open TCE, StockDividend or Media PRs.
- Native schedule history query found no Platform recovery schedule after #41577147958 (04:16:26Z). Latest native inspection #41558049412, reconciliation #41549849545, watchdog #41549659062 and mirror #41560381641 remain stale/failed; mirror failure is missing `PLATFORM_INFRA_MIRROR_TOKEN`. TCE latest native WF-06 #41565175484 and WF-12 #41562429843 failed; WF-07 backup/integration #41557498266/#41556575907 passed. Workflow_run #41565215560 is not a native schedule event.
- Last K3s snapshot #41570085903 was manual, generated 03:05:43Z; now stale. Stock Admin/new Backend remain ImagePullBackOff on `12d63b4`; other last-observed Media/MicroFE/NATS workloads 1/1. No production promotion or restart.
- PR #1122 fixes whole-minute truncation in reconciliation/inspection/mirror/recovery freshness checks, both inline runner-queue checks, and the Python deployment-lane queue verifier. Regression fixtures distinguish exactly 15:00 from 15:01 and cover assigned/unassigned queue paths. The contract validator now rejects legacy whole-minute threshold comparisons.
- Preserve native schedules and all existing CI/security/manual/release/backup jobs. `reconcile-vps.yml` remains the only production apply authority. No cron, image, credential, manifest, database, replica, Pod or host mutation. TCE market-scan schedule unchanged.


## 2026-11-03 12:56 ICT / 05:56 UTC — PR #1122 exact-second watchdog contract merged

- Platform Infra PR [#1122](https://github.com/phanthienquoc/platform-infra/pull/1122) squash-merged at `d402cd9d24333e6a574e6e7aeb698eb0b03c409c` from dedicated branch `fix/ops-exact-seconds-watchdog-budgets-2026-11-03`.
- Exact PR head `4f96c0ba43265b1150b09bcbbeb40d7e137e1fe8` passed `validate-github-actions` [#41587318389](https://github.com/phanthienquoc/platform-infra/actions/runs/41587318389) and `validate-manifests` [#41587318505](https://github.com/phanthienquoc/platform-infra/actions/runs/41587318505). Merge used an exact-head guard.
- Post-merge master validation passed: `validate-github-actions` [#41587385946](https://github.com/phanthienquoc/platform-infra/actions/runs/41587385946), `validate-manifests` [#41587385921](https://github.com/phanthienquoc/platform-infra/actions/runs/41587385921). Read-only watchdog push smoke [#41587385922](https://github.com/phanthienquoc/platform-infra/actions/runs/41587385922) also passed; it executed all schedule freshness checks and warned that inspection/recovery history was stale.
- Freshness budgets for reconciliation (45m), inspection (75m), mirror (90m) and recovery (45m) now compare elapsed seconds. Reconciliation/inspection inline queue checks and the Python deployment-lane queue verifier enforce the 15-minute budget in seconds. Regression fixtures cover exactly 15m and 15m01s for unassigned and assigned lanes; the static workflow validator rejects legacy minute-truncated comparisons.
- This is observability/contract hardening only. No schedule, production manifest, image, credential, database, replica, Pod, host or deployment authority changed. TCE market-scan schedule unchanged.


## 2026-11-03 — inspection completion is part of the deployment evidence contract

- `inspect-vps.yml` native schedule freshness is not sufficient by itself: the latest scheduled run must be completed with conclusion=success before the watchdog reports inspection delivery healthy.
- A recent in-progress inspection is reported as pending, not as completed health evidence. A recent completed failure/cancellation fails scheduled/manual watchdog runs; push-triggered post-merge smoke reports a warning only.
- Recovery checks the latest master inspection run's conclusion as well as its age. A completed non-success run is treated as stale immediately and triggers the existing read-only inspection fallback. In-progress runs continue to suppress duplicate dispatches.
- Manual `workflow_dispatch` inspection can refresh the runtime snapshot but never counts as native event=schedule delivery. No cron expression or production apply authority changes.


## 2026-11-03 15:00 ICT / 08:00 UTC — latest delivery and runtime evidence

- Platform master is `ac205f7c4ae83381509cb436beaaef53d09fec88`; PR #1125 exact-head and post-merge validators passed. Its inspection contract requires latest native scheduled inspection to be completed successfully; manual `workflow_dispatch` refreshes runtime evidence but never satisfies native schedule delivery.
- Platform latest native schedule evidence: reconcile #41591224283 (06:39:06Z, failure at StockDividend health); watchdog #41591762943 (06:44:09Z, failure for stale mirror/inspection/recovery); inspection #41558049412 (01:11:13Z, success); recovery #41577147958 (04:16:26Z, success); mirror #41560381641 (01:32:25Z, failure). No later native recovery or inspection schedule run was present in the queried history. Recovery workflow state was reported active by the watchdog, and the YAML schedule remains `10,25,40,55 * * * *`; cause of missing native schedule delivery remains unverified.
- Non-native recovery events #41591439699 (`workflow_dispatch`) and #41591467278 (`workflow_run`) succeeded; they led to read-only inspection #41591479745 at 06:41:37Z. This snapshot is older than the 75-minute freshness budget at 08:00Z. Do not count these events as native schedule delivery.
- TCE native events: WF-06 #41565175484 failed with four public endpoints returning HTTP 503 (Auth readiness/liveness, TCE web/API); WF-12 #41562429843 failed; WF-07 backup #41557498266 and integration #41556575907 succeeded. WF-12 workflow_run #41565215560 is a distinct non-schedule event. Keep expected HTTP 200 and all existing cron expressions.
- StockDividend publisher #41563856933 and CI #41563856934 passed; full-SHA ARM64 digests were validated, but release gate was false and no handoff/promotion occurred. Production still references old tag `12d63b4` in the last K3s snapshot; paired immutable digest promotion remains authorization-gated.
- Last observed Media, MicroFE and NATS workloads were 1/1; Stock Admin/new Backend were ImagePullBackOff; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0. The inspection snapshot is stale, so these are historical observations only.
- Owner-only credential and authorization actions remain documented in `docs/credentials.md`: configure mirror destination token, verify StockDividend Actions-read token, provide explicit StockDividend release authorization, and complete Auth/Keycloak protected integration prerequisites. Never put secret values in the inventory.
- `reconcile-vps.yml` remains the sole production apply authority. Preserve app-owned CI and immutable publishers, platform-owned GitOps promotion/reconciliation, read-only inspection/watchdogs, backup and intentional manual/release/scheduled workflows. No schedule or TCE market-scan cadence change.


## 2026-11-03 — TCE MicroFE publisher provenance contract

- TCE WF-08B remains the app-owned publisher for MicroFE Shell and WebSocket images. It builds/pushes both images for `linux/arm64`, records full SHA-256 digests, and sends the `microfe-images-published` repository dispatch; Auth is released independently by the Authentication repository.
- The dispatch contract now carries `app`, source repository, numeric source run ID, exact workflow path, source event, full source head SHA, full source commit SHA, release label, and both image digests. The producer validates the payload before dispatch.
- Platform Infra verifies the public TCE Actions run identity (repository, head repository, workflow path, event, master branch, full SHA) and reads its job list. All MicroFE test, release-handoff, and ARM64 build/publish jobs must be completed successfully. While the publisher is waiting for Platform promotion, its dispatch-and-verify job must be in progress; a completed source run is accepted only if dispatch verification also succeeded. This avoids a circular wait while proving that the payload came from the expected app-owned publisher.
- Platform then validates both immutable digests against GHCR, updates only `platform/microfe/kustomization.yaml`, validates/merges the exact-head GitOps PR, and triggers the existing targeted `reconcile-vps.yml` authority. No separate MicroFE reconciliation workflow is permitted.
- The public TCE Actions API is read-only and needs no cross-repository credential on the Platform consumer. TCE's `PLATFORM_INFRA_TOKEN` needs `Contents: write` plus `Actions: read` on Platform Infra because the producer polls promotion/reconciliation runs; StockDividend's separate secret needs only `Contents: write` for its current dispatch flow.
- Historical TCE WF-08B run #41154490073 (2026-10-31) built and published both images successfully, then failed because the Platform promotion workflow revision at that time required an empty `PLATFORM_INFRA_AUTOMATION_TOKEN`. Current `gitops-image-promotion.yml` uses its workflow-scoped `GITHUB_TOKEN` with explicit permissions; the obsolete automation PAT is not required and must not be reintroduced.


## TCE WF-12 exact-second schedule-delivery contract — PR #1019 (in review)

- App-owned `.github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml` remains a read-only observer of WF-06 native schedule delivery and its runner queue. It does not deploy or inspect K3s.
- Follow-up PR [TCE Dashboard #1019](https://github.com/phanthienquoc/TCE-dashboard/pull/1019) replaces whole-minute-truncated comparisons with exact elapsed-second checks: 25-minute schedule freshness and 15-minute runner queue. Its contract validator rejects the legacy comparisons and tests exact 25m/15m boundaries versus one second over.
- Existing WF-06 and WF-12 cron expressions are unchanged. No TCE market-scan schedule is changed. WF-12 keeps Actions read-only and continues to forward only its existing authenticated schedule heartbeat to Platform Infra.
- At inventory update time, exact PR-head WF-05 and WF-02 runs passed; a same-SHA push-triggered WF-05 run was still in progress. Do not mark this follow-up merged until the current head and all relevant checks are re-verified.


## TCE WF-12 exact-second schedule-delivery contract — merged

- TCE Dashboard PR [#1019](https://github.com/phanthienquoc/TCE-dashboard/pull/1019) merged at `53227425841b6283bebad3bc5c93d509bd8a316a` after exact-head WF-05/WF-02 PR and same-SHA push checks passed.
- The app-owned WF-12 read-only watchdog now compares elapsed seconds against the 25-minute WF-06 freshness budget and 15-minute runner queue budget. The contract validator rejects whole-minute comparisons and tests exact 25m/15m boundaries against 25m01s/15m01s.
- No WF-06/WF-12 cron expression changed; no market-scan schedule changed. WF-12 retains Actions read-only and its existing authenticated Platform heartbeat only.
- Post-merge WF-01/WF-02/WF-05 and WF-12 push smoke were queued/in progress at the recorded checkpoint; update the tracker after those runs complete.


## StockDividend and Media source-run job-level provenance — merged

- Platform PR #1133 added exact source-run Jobs API verification to both app publisher receivers.
- StockDividend requires successful master/release gates, native ARM64 build-and-push, all three image build steps, immutable ARM64 manifest verification, release handoff and atomic digest-dispatch jobs. A completed-success workflow run with skipped handoff/dispatch is rejected.
- Media requires successful master gate, release tag resolution, native ARM64 frontend/backend build jobs, architecture/export validation, immutable GHCR digest/ARM64 manifest verification and Platform notification. It uses the public Actions API without a cross-repository token.
- Regression suites exercise missing, skipped and failed jobs/steps; static workflow contract validation enforces the guards. PR #1133 and post-merge validations passed.
- StockDividend latest publisher run #41563856933 had ARM64 build/manifest verification pass but production handoff/dispatch were skipped because the explicit release gate remained closed. No promotion occurred. Media verifier has regression evidence but no new real publisher dispatch in this checkpoint.

## TCE WF-12 exact-second budget — merged

- TCE PR #1019 merged as `53227425841b6283bebad3bc5c93d509bd8a316a`. Exact-second 25m freshness and 15m queue checks plus one-second-over regressions passed. Post-merge WF-01/WF-02/WF-05/WF-12 push smoke all passed.
- Latest WF-12 push smoke #41608676616 still warned that native WF-06 schedule delivery was stale (411m; queue 0m). This is not a native schedule pass. WF-06 and WF-12 cron expressions and all market-scan schedules are unchanged.


## 2026-11-03 17:56 ICT / 10:56 UTC — current cross-repo workflow evidence

### Master refs and latest application validation

| Repository | Master SHA | Latest relevant result |
|---|---|---|
| Platform Infra | `ee779f525021f69c9df9df0c66e01948cede345f` | `validate-github-actions` #41616987207 PASS; `validate-manifests` #41617368068 PASS |
| TCE Dashboard | `53227425841b6283bebad3bc5c93d509bd8a316a` | WF-01 #41608676328, WF-02 #41608676350, WF-05 #41608676512 PASS |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | CI #41563856934 and ARM64 publisher #41563856933 PASS; production handoff/dispatch skipped because release gate=false |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | CI #41617592783 PASS; paired-digest publisher E2E still pending |
| Authentication | `1f39b18d9dd286da9dde32a79c4da269b19d5cfd` | Web #41542942080 and service #41542941957 PASS; migration side-effect gate remains unresolved |

### Native schedule inventory (fallback events do not count)

| Workflow | Latest native event | Result / finding |
|---|---|---|
| Platform mirror | #41611280196, 09:28:17Z | FAIL — `PLATFORM_INFRA_MIRROR_TOKEN` empty |
| Platform inspection | #41603684581, 08:29:41Z | PASS; later #41614707823 was workflow_dispatch only |
| Platform reconciliation | #41591224283, 06:39:06Z | FAIL — StockDividend lane |
| Platform watchdog | #41591762943, 06:44:09Z | FAIL — stale schedule evidence |
| Platform recovery | #41577147958, 04:16:26Z | PASS but stale; later dispatch/workflow_run events are not native |
| TCE WF-06 | #41614307460, 09:50:40Z | FAIL — four public endpoints HTTP 503 |
| TCE WF-12 | #41605106319, 08:41:06Z | FAIL — WF-06 native delivery stale; later workflow_run #41614338174 is not a schedule tick |
| TCE WF-07 integration | #41556575907, 00:58:19Z | PASS |
| TCE WF-07 backup | #41557498266, 01:06:20Z | PASS |
| StockDividend weekend scraper | #41284033242, 2026-11-01 | CANCELLED; not a production publisher |
| Media / Authentication | No scheduled deployment run in queried history | No native schedule evidence |

### Runtime and promotion ownership

- Latest read-only K3s snapshot is `debug/vps-latest.md`, generated 09:53:49Z by inspection #41614707823. It records Node Ready, ARM64, K3s v1.36.3+k3s1, disk 55%, about 19 GiB available RAM, runner policy v14, and pending host restart/updates.
- Media and MicroFE workloads were 1/1 Running. Stock Admin and new Backend remained ImagePullBackOff on `12d63b4`; old Backend and Frontend were Running. TCE frontend/service and Keycloak/Auth were 0/0. GitOps drift was clean.
- Platform reconciliation #41614373680 (workflow_dispatch) completed with StockDividend FAILURE; MicroFE, Auth, TCE and Media lanes succeeded, Keycloak was skipped, and manifest apply was skipped because no drift was detected.
- Media legacy `media-release-requested` tag-only fan-out has been retired by Platform PR #1137; Media PR #71 adds a producer regression test. New production contract is one `media-images-published` event carrying both immutable digests and source-run provenance. A real post-merge publisher dispatch is still required to prove end-to-end handoff.
- StockDividend's explicit release gate remains false. Never promote its paired Admin/Backend digests until protected Actions-read credential verification and production authorization are complete.
- TCE WF-06 remains public-smoke-only with expected HTTP 200; its strict assertion is retained. TCE/Auth are currently scale-to-zero, matching the prior operator direction. Do not reclassify HTTP 503 as healthy or alter their schedule to suppress evidence.
- TCE WF-06 cron remains `*/15 * * * *`; WF-12 remains `7,22,37,52 * * * *`. TCE's app-side `validate-wf-06-healthcheck-contract.sh` explicitly pins both expressions. Market-scan schedules were not changed.
- `reconcile-vps.yml` remains the only production apply authority. App repositories own tests/builds and immutable GHCR publication; Platform Infra owns production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation and rollout/health verification. Preserve purposeful CI, security, backup, manual, release and scheduled workflows.


## 2026-11-03 18:56 ICT / 11:56 UTC — Media publisher provenance regression coverage

- Platform PR [#1140](https://github.com/phanthienquoc/platform-infra/pull/1140), dedicated branch `test/media-provenance-skipped-dispatch-regressions-2026-11-03-1856-ict`, adds negative tests for a skipped Media production-release gate job, a skipped `Notify platform-infra` step, and duplicate required publication jobs.
- The production verifier already rejects any required job not completed-success, any required step without success, and missing/duplicate matching evidence. This change closes a regression-test gap; it does not change runtime acceptance behavior.
- Required validation: `validate-github-actions` and `validate-manifests` on the exact PR head, followed by post-merge validation. Do not claim merged until exact-head checks and merge SHA are confirmed.
- No workflow, publisher, payload, GitOps manifest, credential, release gate, deployment authority or schedule changed. TCE market-scan schedule unchanged.


## 2026-11-03 19:03 ICT / 12:03 UTC — Media provenance regression suite merged and reconciliation rechecked

- Platform PR [#1140](https://github.com/phanthienquoc/platform-infra/pull/1140) merged at `4510198f12d0dc7296252a8cb357d91a02fe26e0`. Exact-head `validate-github-actions` #41632044387 and `validate-manifests` #41632044570 passed; post-merge #41632121961 and #41632121933 passed.
- `scripts/tests/verify-media-publisher-run.test.sh` now explicitly rejects a skipped production release-gate job, a skipped `Notify platform-infra` step, and duplicate required publication jobs. The verifier already failed closed for these outcomes; PR #1140 adds executable regression coverage.
- Push recovery #41632121999 dispatched the sole production authority, reconciliation #41632142164. Shared GHCR preflight passed; `ghcr-pull` remained unchanged; Auth runtime Secret was provisioned/verified with values suppressed. GitOps drift was false and manifest apply skipped.
- Reconciliation's independent lanes: Media, MicroFE, TCE and Auth SUCCESS; Keycloak SKIPPED; StockDividend FAILURE due Admin/Backend `12d63b4` ImagePullBackOff / no ARM64 manifest. Permanent Stock image-pull failures suppressed rollout restart. No image promotion or manifest mutation.
- Native schedule evidence remains stale/failed; dispatch and workflow_run fallbacks are not native schedule ticks. Preserve CI, security, manual, release, backup and scheduled workflows. `reconcile-vps.yml` remains the only production apply authority. TCE market-scan schedule unchanged.


## 2026-11-03 19:04 ICT / 12:04 UTC — latest K3s inspection evidence

- Inspection #41632477654 is a successful \`workflow_dispatch\` fallback, not a native schedule tick. Inspection PR #1142 merged \`debug/vps-latest.md\` at \`343ce495045afd97c94e861da7f3991b22078510\`; post-merge manifest validation #41632633373 passed.
- Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 55%, approximately 19 GiB available RAM, runner policy v14; host restart pending.
- Media and MicroFE workloads 1/1; TCE/Auth/Keycloak 0/0; OIDC 503. Stock Admin and one new Backend Pod still fail on \`12d63b4\` (no ARM64 manifest); an older Backend and Frontend remain running on \`23b2878\`. Do not treat cached prior images as a new release.
- Reconciliation #41632142164: no drift, no manifest apply, shared GHCR pull Secret unchanged, Auth runtime Secret provisioned/verified, Stock permanent pull failures not restarted. Media/MicroFE/TCE/Auth lanes passed; Stock lane failed; Keycloak skipped.
- Keep native schedule evidence separate from fallback dispatches; preserve all existing schedules and workflows. TCE market-scan schedule unchanged.


## 2026-11-03 19:08 ICT / 12:08 UTC — native schedule delivery checkpoint

- Native Platform recovery tick #41633096574 passed. It observed fresh fallback reconciliation #41632142164 and inspection #41632477654 and correctly avoided duplicate dispatches.
- Watchdog #41633130972 failed because native reconcile, mirror and inspection schedules remain stale; the mirror's latest native run #41611280196 failed due missing \`PLATFORM_INFRA_MIRROR_TOKEN\`. Workflow enabled checks passed.
- Native recovery is fresh; native reconcile/inspection/mirror are not. TCE WF-06/WF-12 native runs remain stale/failed. Fallback \`workflow_dispatch\` and \`workflow_run\` events are not schedule proof.
- No schedule definitions changed. Keep strict health assertions, all CI/security/manual/release/backup workflows, and the sole \`reconcile-vps.yml\` production apply authority. TCE market-scan schedule unchanged.


## 2026-11-03 20:15 ICT / 13:15 UTC — Auth immutable digest publisher contract

- **Application owner:** `phanthienquoc/phanthienquoc-authentication` owns Auth service source, tests, Dockerfile, manual-only release publisher, and immutable GHCR image publication.
- **Platform owner:** `phanthienquoc/platform-infra/.github/workflows/gitops-image-promotion.yml` receives `auth-image-published`; it validates full source SHA and public Actions run provenance, confirms the versioned GHCR tag maps to the supplied digest and has linux/arm64, then creates a narrowly scoped GitOps PR that pins the Auth image by digest.
- Platform verifier: `scripts/verify-auth-publisher-run.sh`; digest manifest helper: `scripts/promote-auth-image-digest.py`; registry tag/digest correlation: `scripts/validate-ghcr-image-reference.sh` with `GHCR_EXPECTED_DIGEST`.
- Regression coverage: `scripts/tests/verify-auth-publisher-run.test.sh`, `scripts/tests/validate-ghcr-image-reference.test.sh`, and the Auth digest promotion helper self-test are included in Platform CI.
- Producer implementation is proposed in Auth PR [#87](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/87), still open. Its exact-head Auth CI passed, but Supabase Preview was skipped. Do not merge until the Supabase-on-master side effect gate is explicitly resolved. Do not trigger the manual Auth publisher while this producer PR is unmerged.
- No workflow was removed. Existing CI, security, manual/release and scheduled jobs remain purposeful. `reconcile-vps.yml` is still the sole production apply authority; no direct SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## 2026-11-03 14:06 UTC — Auth verifier hardening, reconciliation and inspection inventory

### Current repository refs

| Repository | Master SHA | Latest app-owned validation / release evidence |
|---|---|---|
| Platform Infra | `0fdded730fb5658e4056fa22df4a6e68f3a2c43a` | #1147 Auth verifier hardening merged; post-merge manifest/workflow checks PASS |
| TCE Dashboard | `53227425841b6283bebad3bc5c93d509bd8a316a` | WF-01 #41608676328, WF-02 #41608676350, WF-05 #41608676512 PASS; WF-06/WF-12 native schedules failed |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; production handoff skipped while release gate=false |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | CI #41617592783 PASS; no post-merge paired-digest production publisher run |
| Authentication | `1f39b18d9dd286da9dde32a79c4da269b19d5cfd` | PR #87 exact-head CI #41642031980 PASS; Supabase Preview skipped and merge side-effect gate unresolved |

### New Platform change

- PR #1147 merged as `8b9e028c8b9d166805c505f91b264fb7a61f5daf`.
- Auth source-run verification now checks five critical `Verify auth service` steps individually: package-lock refresh, `npm ci`, tests, typecheck and build. Each skipped-step case has a negative fixture; static contract validation enforces the checks.
- Exact PR-head runs #41649669578 (`validate-manifests`) and #41649669519 (`validate-github-actions`) passed. Post-merge runs #41649784222 and #41649784381 passed.
- No Auth release, publisher dispatch, GHCR publication, or GitOps image promotion occurred.

### Production authority and lane results

- Recovery push #41649784133 dispatched `reconcile-vps.yml` run #41649818474 with `mode=apply`, `allow_image_changes=false`, `target_app=all`, source master SHA `8b9e028c8b9d166805c505f91b264fb7a61f5daf`.
- Shared reconciliation job passed; GHCR preflight verified Auth, Media backend/frontend, MicroFE Shell/WS, StockDividend Admin/Backend and TCE web/service. Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` remained unchanged.
- GitOps drift clean; manifest apply skipped. Permanent Stock Admin/Backend `12d63b4` image-pull failures were not restarted because the image has no ARM64 manifest.
- Lane outcomes: Stock FAILURE; Media/Auth/MicroFE/TCE SUCCESS; Keycloak SKIPPED. TCE/Auth success corresponds to 0/0 workloads, not active service health.
- Reconciliation failure triggered recovery #41650121040 and read-only inspection #41650172429. Inspection PR #1148 merged at `0fdded730fb5658e4056fa22df4a6e68f3a2c43a`; exact-head manifest check #41650296622 passed.

### Runtime and schedule inventory

- Latest snapshot `debug/vps-latest.md` generated 14:04:59Z: K3s node Ready/ARM64, v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 55%, approximately 19 GiB available RAM. Both self-hosted runners active.
- Host has pending containerd 2.4.2 and Docker 29.9.2 updates; `restart_required: yes`. Maintenance/reboot not performed.
- Media and MicroFE/NATS 1/1. Stock Admin two Pods and new Backend Pod 0/1 ImagePullBackOff; old Backend and Frontend 1/1. TCE/Auth/Keycloak 0/0; public OIDC 503. GitOps drift clean.
- Native Platform schedule latest: recovery #41633096574 PASS (12:07:39Z); mirror #41611280196 FAIL missing `PLATFORM_INFRA_MIRROR_TOKEN` (09:28:17Z); inspection #41603684581 PASS (08:29:41Z); watchdog #41591762943 FAIL (06:44:09Z); reconcile #41591224283 FAIL (06:39:06Z).
- Native TCE schedule latest: WF-06 #41614307460 FAIL (09:50:40Z), WF-12 #41605106319 FAIL (08:41:06Z); WF-07 integration #41556575907 and backup #41557498266 PASS. Workflow_run and workflow_dispatch fallbacks are not schedule evidence.
- No schedule definitions changed. TCE market-scan schedule unchanged.

### Owner gates and authority

- Missing destination-only mirror token; StockDividend Actions-read token verification and explicit paired ARM64 production release authorization; Auth Supabase integration side-effect approval; Media paired-digest publisher E2E; TCE/Auth/Keycloak activation and OIDC/DB/DNS prerequisites; host maintenance window.
- Preserve all CI/test/security workflows and purposeful manual/release/scheduled/backup jobs. `reconcile-vps.yml` is the sole production apply authority; no direct SSH/Compose authority added.


## 2026-11-03 22:01 ICT / 15:01 UTC — native schedule and publisher provenance delta

- Current Platform master: `069be27a063decfc243dced2a42b032c9bc8f77b`; current TCE/Stock/Media/Auth master refs and open PRs are recorded in the deployment tracker checkpoint at the same timestamp.
- Latest scheduled watchdog #41657391305 failed on stale native mirror (#41611280196, 320m), inspection (#41603684581, 379m) and recovery (#41633096574, 161m). Scheduled reconcile #41656213890 was fresh (7m) but its StockDividend health lane failed. workflow_dispatch/workflow_run recovery runs are not native schedule proof.
- Native TCE WF-07 integration #41652078419 passed; WF-06 #41614307460 and WF-12 #41605106319 remain failed/stale. No schedule expression changed; TCE market-scan schedule unchanged.
- StockDividend publisher #41563856933 verified ARM64 immutable artifacts for source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`: scraper `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`, Admin `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`, Backend `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. Production Kustomize still references `12d63b4`, whose Admin/Backend manifests lack ARM64. The latest publisher's production hold was false and handoff/dispatch skipped; owner authorization remains mandatory.
- Auth PR #87 remains open with CI PASS and Supabase Preview SKIPPED; merge side-effect approval remains unresolved. Media CI passes but paired-digest publisher E2E remains pending.
- Preserve the single `reconcile-vps.yml` production apply authority, strict schedule freshness/health checks, and all useful CI/security/manual/release/backup workflows. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-03 23:06 ICT / 16:06 UTC

- **Repository heads:** Platform `fcad6b471f2abf643b8c738a21f9ba502bec1c84`; TCE `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **PR inventory:** Platform #544/#541/#539 remain draft; Auth #75/#76 remain open; Auth #87 is merged; TCE/StockDividend/Media have no open PRs.
- **Auth release producer:** #87 merged at exact head `580ceca91466e998616982059db1befa0bb181eb`. It introduces manual-only master publication with full-SHA tags, provenance/SBOM, tag-to-digest equality, ARM64 verification and `auth-image-published` provenance payload. PR validation passed; post-merge CI #41670642852 was still in progress at checkpoint time. No manual publisher run or dispatch occurred. Supabase Preview was skipped; no migration files were part of the PR.
- **Platform Auth receiver:** merged #1145 verifies the exact source run, required publisher job/steps, full SHA, versioned tag, digest and ARM64 manifest before a digest-only Auth GitOps promotion. Keep Auth production activation and DB migration gates separate from publisher merge.
- **Platform runs:** master manifest validation #41660206785 passed. Native reconciliation #41656213890 failed only StockDividend health; manifest apply skipped because GitOps drift was clean and image changes were disallowed. Native watchdog #41657391305 failed stale mirror/inspection/recovery evidence. Mirror #41611280196 lacks `PLATFORM_INFRA_MIRROR_TOKEN`; inspection #41650172429 is workflow_dispatch; recovery #41656612489 is workflow_run, neither is native schedule evidence.
- **TCE:** WF-07 schedule #41652078419 passed; WF-06 schedule #41614307460 failed four strict HTTP 200 endpoint probes; WF-12 #41652113481 failed WF-06 schedule freshness but authenticated heartbeat dispatch passed. Preserve strict health assertions and every existing cron; TCE market-scan schedule unchanged.
- **StockDividend:** CI #41563856934 and publisher #41563856933 passed; all three native ARM64 image manifests verified. Promotion/handoff remained skipped under the production release hold. Production Admin/Backend tag `12d63b4` remains non-pullable on ARM64; owner authorization and paired digest handoff are required before changing Kustomize.
- **Media:** master CI #41617592783 passed; paired-digest publisher E2E remains pending an authorized release.
- **K3s:** inspection #41650172429 (workflow_dispatch) and reconciliation #41656213890 are the latest evidence. Node Ready/ARM64, v1.36.3+k3s1; disk 55%, ~19 GiB RAM available, runner v14. Stock Admin/new Backend ImagePullBackOff; older Backend, Media and MicroFE pods running; TCE/Auth/Keycloak remain scaled to zero. Host restart required for maintenance; no reboot.
- **Authority and preservation:** `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` read-only; recovery/watchdog dispatch/observe only. Preserve CI/tests/builds/security, backups, manual/release/scheduled workflows. Do not add direct SSH/Compose deploy paths, change schedules, alter production credentials, mutate DB, or restart failed Stock pods to mask image errors.


## Workflow inventory post-merge follow-up — 2026-11-03 23:10 ICT / 16:10 UTC

- Auth PR #87 is merged at `f978a3f378ee22d4630909c2d182275b21ac9e9a`; post-merge `auth-service-ci` #41670642852 completed SUCCESS across lock refresh, install, test, typecheck, build, release-contract checks and container build. No manual release or dispatch occurred.
- Platform Infra tracker/inventory PR #1151 merged as `3a3a67651beb497ac6eed5a9ad8b1f365e246041`; exact-head #41670920201 and post-merge #41671155770 validations passed.
- Read-only Supabase check: project `gtqovpusfyyvxpeezxlo` ACTIVE_HEALTHY; 84 migration versions, latest `20261028020259`, no new version after PR #87. The PR did not change migration files and Supabase Preview was skipped. A targeted 16:00–16:10 UTC log query returned no migration/deploy event, but this does not prove the owner-configured Deploy-to-production integration did not execute. Keep Auth PR #75 and future master merges behind authoritative integration/migration review.
- No database write, migration apply, project setting mutation, release publish, image promotion, replica activation or Supabase branch operation was performed.


## 2026-11-03 23:59 ICT / 16:59 UTC — StockDividend publisher critical-step provenance

- Platform PR #1154 merged at `351bbb5884b3c879a5213022e76decd30e32e70f`. The StockDividend source-run verifier now checks successful completion of the master-ref guard, production release-enable gate, Platform Infra token/access check and atomic digest-dispatch step by exact job/step name. Existing ARM64 runner, Scraper/Admin/Backend build-and-push and immutable manifest checks remain mandatory.
- Four negative fixtures reject skipped critical steps even when the parent job is successful. Static workflow validation requires each verifier assertion and test fixture. Exact-head `validate-github-actions` #41680365526 and `validate-manifests` #41680365295 passed; post-merge checks are not asserted without run evidence.
- Current master refs/open PRs, K3s snapshot, StockDividend release hold, mirror token gate, Auth Supabase side-effect gate, Media E2E status and native schedule evidence are recorded in [the deployment readiness checkpoint](cross-repo-deployment-checkpoints/2026-11-03-2359-ict.md).
- Preserve all CI/test/security/backup/manual/release/scheduled workflows. `reconcile-vps.yml` remains the only production apply authority. Do not add SSH/Compose deployment paths or alter any cron expression; TCE market-scan schedule unchanged.


## Runtime evidence — 2026-11-04 01:04 ICT / 18:04 UTC

- Platform Infra master `716baa7825f7c8b8677b8ea7af8fbd5745c64fa5`; TCE `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- PR inventory: Platform #544/#541/#539 draft; Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. Platform #1157 merged after exact-head validation #41690759467 and #41690759493 passed. Post-merge #41690886530/#41690886564 were still running at checkpoint time.
- Mirror #41687882647 is the latest native schedule and fails because `PLATFORM_INFRA_MIRROR_TOKEN` is empty. The token contract is destination-only `Contents: write` for `phanthienquoc/locally-uncensored-private`; no Actions, Packages, admin or unrelated repository access. Static validator now enforces both workflow binding and credential documentation.
- Platform native schedule evidence: inspection #41674687948 PASS (16:29:16Z), mirror #41687882647 FAIL (17:49:06Z), reconcile #41656213890 FAIL (14:41:42Z), watchdog #41657391305 FAIL (14:48:50Z), recovery #41633096574 PASS (12:07:39Z). Inspection #41687934519 and validation #41688052221 are dispatch runs, not schedule evidence.
- TCE native schedules: WF-06 #41685253743 FAIL (17:32:37Z; all four endpoints HTTP 503 vs 200), WF-12 #41676393032 FAIL (16:39:14Z), WF-07 #41652078419 PASS (14:16:34Z). Preserve strict health checks and cron expressions; TCE market-scan schedule unchanged.
- StockDividend CI #41563856934 and publisher #41563856933 PASS; production paired digest promotion remains disabled pending owner authorization. Admin/Backend production tag `12d63b4` remains non-pullable on ARM64. Media CI #41617592783 PASS; paired-digest E2E pending. Auth CI #41670642852 PASS; no release/promotion, and PR #75 remains behind Supabase integration/migration review.
- Latest VPS snapshot `debug/vps-latest.md` generated 17:49:35Z: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB RAM available, runner services active. Media/MicroFE/NATS healthy; Stock Admin/new Backend ImagePullBackOff; old Backend/Frontend running; TCE/Auth/Keycloak 0/0; public OIDC 503. Host updates/restart pending; no maintenance performed.
- Production image promotion, manifest apply, DB migration, shared pull Secret mutation, replica change, Pod restart and host reboot were not performed. `reconcile-vps.yml` remains the sole production apply authority. No direct SSH/Compose deployment authority added.


## Workflow inventory runtime update — 2026-11-04 02:05 ICT / 19:05 UTC

- **Repository heads:** Platform `38d2aba74cd35c95e85337c8b19c0a8309adb0bf`; TCE `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Auth `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1159 plus draft #544/#541/#539; Auth #75 ready/#76 draft; no open PRs in TCE, StockDividend or Media. Platform PR #1159 exact-head checks #41700394033 (workflow contracts) and #41700393711 (manifest validation) both completed SUCCESS; exact head was squash-merged as `38d2aba74cd35c95e85337c8b19c0a8309adb0bf`.
- **StockDividend receiver:** Platform #1159 adds independent full-SHA tag-to-digest correlation for both Admin and Backend, then separately validates the exact digest reference for linux/arm64. The shared GHCR validator's existing tag mismatch test is reused; the workflow contract now requires tag validation before digest validation. Producer handoff and promotion remain release-gated.
- **Platform post-merge validation:** #41690886530 and #41690886564 SUCCESS; latest tracker manifest validation #41691193224 SUCCESS.
- **Platform native schedules:** mirror #41687882647 FAIL (missing destination-only token); inspection #41674687948 PASS; watchdog #41657391305 FAIL; reconciliation #41656213890 FAIL only StockDividend; recovery #41633096574 PASS. Dispatch inspection #41687934519 is not a native schedule.
- **TCE native schedules:** WF-06 #41685253743 FAIL (four endpoints 503), WF-12 #41676393032 FAIL (freshness), WF-07 #41652078419 PASS. Do not weaken checks or alter cron.
- **StockDividend:** CI #41563856934 PASS; publisher #41563856933 PASS for ARM64 builds but Platform handoff/dispatch SKIPPED under release hold. Production Admin/Backend remain on non-pullable tag `12d63b4`.
- **Media:** CI #41617592783 PASS; paired digest publisher E2E pending. **Auth:** master CI #41670642852 PASS; manual publisher not observed; PR #75/#76 remain gated.
- **K3s:** inspection #41687934519 at 17:49:35Z; node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB RAM available, runner services active. Media/MicroFE/NATS healthy; Stock Admin/new Backend ImagePullBackOff; old Backend/legacy Frontend running; TCE/Auth/Keycloak 0/0; OIDC probes 503. Host maintenance pending.
- **Authority:** app repositories own CI/build/immutable GHCR publication; Platform owns production manifests/shared pull credentials/GitOps promotion/reconciliation/rollout/health. `reconcile-vps.yml` is the sole apply authority. Preserve CI/security/manual/release/scheduled workflows; no direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Post-checkpoint workflow contract update — 2026-11-04 02:05 ICT

- Platform master: `5c9db4d61967b40cc598128cf792b67c884f37d1`.
- PR #1159 merged: StockDividend receiver now verifies each full-SHA Admin/Backend tag maps to the exact payload digest, then separately validates the digest reference for ARM64. Exact-head runs #41700394033 and #41700393711 PASS.
- PR #1160 merged: readiness tracker/workflow inventory refreshed; docs-only manifest validation #41700759192 PASS.
- PR #1161 merged: Media receiver now verifies each `prod-v<semver>-<full-sha>` frontend/backend tag maps to the exact payload digest, then validates the digest reference for ARM64. Exact-head runs #41700938762 and #41700938766 PASS.
- Open PRs: Platform #544/#541/#539 draft; Auth #75 ready/#76 draft; no TCE/StockDividend/Media PRs.
- Publisher status has not changed: StockDividend #41563856933 build/publish PASS but handoff/dispatch SKIPPED under release hold; Media #41617592783 CI PASS but paired-digest publisher E2E pending; Auth #41670642852 CI PASS but manual publisher not run.
- Native schedule and K3s evidence remain those in the 01:04 checkpoint; no newer schedule run listing is available from the connected run-reader surface. Do not infer native cadence from dispatch/recovery events.
- Production ownership remains unchanged: application repos build/test/publish immutable images; Platform owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole apply authority. Preserve useful CI/security/manual/release/scheduled jobs; no SSH/Compose authority; TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-04 03:03 ICT / 20:03 UTC

- **Master heads:** Platform Infra `b58ab998a88a2049fbce2b757f70f4bee26a6f8d`; TCE `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft and #1176 (documentation checkpoint, open); Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. Platform #1166 is merged; intermediate PRs #1164/#1165 were closed as superseded while correcting the test/validator contract and are not open.
- **MicroFE receiver contract:** PR #1166 merged after exact-head lint/manifest checks #41709764057/#41709763643 passed. Platform now checks `microfe-shell:$SOURCE_COMMIT` and `microfe-ws:$SOURCE_COMMIT` against payload `SHELL_DIGEST`/`WS_DIGEST` using `GHCR_EXPECTED_DIGEST`, then separately validates digest references and ARM64. Post-merge checks #41709868434/#41709868502 passed.
- **Post-merge recovery:** #41709868602 succeeded after the Platform push but skipped source reconciliation/inspection recovery steps; no production dispatch occurred.
- **Platform native schedules:** recovery #41703551669 PASS; mirror #41687882647 FAIL because `PLATFORM_INFRA_MIRROR_TOKEN` is absent; inspection #41674687948 PASS; watchdog #41657391305 FAIL; reconciliation #41656213890 FAIL only StockDividend health. Newer reconciliation #41703583116 and inspection #41703987821 are dispatch runs, not native schedule evidence.
- **TCE native schedules:** WF-06 #41685253743 FAIL (four public endpoints HTTP 503); WF-12 #41676393032 FAIL (WF-06 freshness); WF-07 integration #41652078419 PASS. Keep strict HTTP 200 assertions and existing cron declarations.
- **StockDividend:** CI #41563856934 PASS; publisher #41563856933 PASS for native ARM64 build/publish. Production release gate explicitly false; Platform handoff and atomic dispatch SKIPPED. Production Admin/Backend remain on tag `12d63b4`, which fails ARM64 pulls.
- **Media:** CI #41617592783 PASS; paired digest publisher E2E pending. **Auth:** master CI #41670642852 PASS; no manual publisher/dispatch. Auth #75/#76 checks pass, but Supabase Preview is skipped and integration/migration review remains required.
- **K3s inspection:** #41703987821 PASS, snapshot generated 2026-11-03T19:31:16Z. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 55%, ~19 GiB available RAM, runner policy v14. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0. Host restart required for pending updates; no maintenance performed.
- **Authority and safety:** application repositories own tests/builds/immutable GHCR publication; Platform owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains sole apply authority. Preserve CI/test/security/manual/release/scheduled jobs; no SSH/Compose authority. No production promotion, manifest apply, DB migration, shared pull-secret mutation, replica change, Pod restart or host reboot. TCE market-scan schedule unchanged.

## Workflow inventory runtime update — 2026-11-04 04:02 ICT / 2026-11-03 21:02 UTC

- **Platform master:** `e4171bb42a8cfd535b990e44511942da4532a369`. **TCE:** `53227425841b6283bebad3bc5c93d509bd8a316a`. **StockDividend:** `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. **Media:** `e4c7d8990aafc7d837e918c9caf39722d623de7c`. **Authentication:** `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- Platform #1168 merged after exact-head validate #41718044443 and lint #41718044445 both passed; post-merge manifest validation #41718148057 and GitHub Actions validation #41718148134 both passed.
- **GitOps Image Promotion permission boundary:** workflow default is now `contents: read`; non-master guard has no token permissions; TCE coordinator has only `contents: write`; only `promote-microfe-digests`, `promote-tce-digests`, and `promote` retain explicit `actions: write`, `contents: write`, `pull-requests: write`. GHCR access remains on the separate `GHCR_READ_TOKEN`. Static workflow contract validation enforces this boundary.
- Open PRs: Platform #544/#541/#539 remain draft; Authentication #75 ready/#76 draft; no open PRs in TCE, StockDividend or Media.
- Latest native Platform schedules: reconcile #41714763176 (20:40:42Z) failed only StockDividend health; watchdog #41715283880 (20:44:07Z) failed stale Mirror/inspection/recovery freshness; recovery #41703551669 passed; mirror #41687882647 failed due missing `PLATFORM_INFRA_MIRROR_TOKEN`; inspection #41674687948 passed. The newer recovery #41715097490 is workflow_run, not schedule evidence.
- Watchdog log measured mirror age 175m vs 90m, inspection age 254m vs 75m, recovery age 75m vs 45m. Inspection queue wait was 0m and no reconciliation lane exceeded its queue budget; do not classify this as a runner backlog.
- Latest native TCE schedules: WF-06 #41685253743 failed four HTTP 200 endpoint assertions (503 observed); WF-12 #41676393032 failed freshness; WF-07 #41652078419 passed. All cron expressions and the TCE market-scan schedule remain unchanged.
- StockDividend CI/publisher #41563856934/#41563856933 passed, but production release hold remains active and paired handoff/dispatch were skipped. Admin/Backend production tag `12d63b4` remains ARM64-incompatible.
- Media CI #41617592783 passed; paired-digest E2E pending. Auth CI #41670642852 passed; no manual publisher/dispatch. Auth PR #75 remains behind Supabase integration/migration side-effect review; #76 remains draft.
- K3s snapshot #41703987821 (workflow_dispatch, 19:31:16Z) shows node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available RAM, runner policy v14; Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart required. Scheduled reconciliation #41714763176 independently reconfirmed StockDividend health failure and successful Media/MicroFE/TCE lanes.
- Preserve authority split: app repos own tests/builds/immutable GHCR publication; Platform owns production manifests/shared pull credentials/GitOps promotion/reconciliation/rollout/health. `reconcile-vps.yml` remains the only apply authority. No SSH/Compose authority was added. No production state mutation or host maintenance occurred.



## Workflow inventory runtime update — 2026-11-04 05:00 ICT / 2026-11-03 22:00 UTC

- **Repository heads:** Platform Infra `ad0dbab3ea1b03eaddbf36062122d544e3a083f4`; TCE Dashboard `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft); Auth #75 ready/#76 draft; no open PRs in TCE, StockDividend or Media. Platform #1171 is merged; Auth #87 remains merged.
- **Platform Auth receiver contract:** PR #1171 merged at exact head `5c93095a063cf6ca367bc5acca56d50e59280b46` as `ad0dbab3ea1b03eaddbf36062122d544e3a083f4`. The receiver validates the full source SHA, versioned full-SHA release tag suffix, both tag-to-digest mappings, and the digest-only linux/arm64 reference. Static workflow contract validation protects the required checks and ordering. Exact-head `validate-github-actions` #41727710816 and `validate-manifests` #41727710823 passed. No Auth release or dispatch was run.
- **Platform production authority:** `.github/workflows/reconcile-vps.yml` remains the only apply authority. `.github/workflows/inspect-vps.yml` remains read-only. `.github/workflows/recover-stale-ops.yml` and `.github/workflows/reconcile-schedule-watchdog.yml` remain observe/recover-only; neither is a kubectl/SSH/Compose deploy authority. GitOps promotion retains per-job least-privilege permissions; private GHCR reads use the separate `GHCR_READ_TOKEN`.
- **Latest verifiable Platform native schedules:** watchdog #41715283880 FAILURE (stale inspect/recovery/mirror evidence); reconcile #41714763176 FAILURE only StockDividend health; recovery #41703551669 SUCCESS; mirror #41687882647 FAILURE because `PLATFORM_INFRA_MIRROR_TOKEN` is absent; inspection #41674687948 SUCCESS. Read-only inspection PR #1170 generated a newer 21:56:36 UTC snapshot, but its event type is not established and it is not native schedule proof.
- **Latest verifiable TCE native schedules:** WF-06 #41685253743 FAILURE (four HTTP 503 endpoint probes), WF-12 #41676393032 FAILURE (freshness), WF-07 #41652078419 SUCCESS. Keep strict HTTP 200 assertions and all cron expressions unchanged; TCE market-scan schedule unchanged.
- **App ownership remains:** TCE Dashboard, StockDividend, Media Generation and Authentication own application tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, source-run/payload verification, tag-to-digest correlation, GitOps promotion/reconciliation, rollout and health verification.
- **StockDividend:** publisher #41563856933 built/published ARM64 artifacts but release enablement was false; handoff/dispatch skipped. Production Admin/Backend still reference `12d63b4` and fail ARM64 pulls. No release authorization or paired promotion.
- **Media:** CI #41617592783 PASS; paired digest publisher E2E pending. **Auth:** CI #41670642852 PASS; manual publisher E2E not run; PR #75 remains gated by Supabase integration/migration side-effect review and #76 remains draft.
- **Credential/maintenance blockers:** Mirror destination-only token absent; StockDividend protected Actions-read token and explicit release authorization unverified; host restart required for pending OS/containerd/Docker updates. Do not create or substitute credentials, or perform host maintenance without authorization/window.
- Preserve all useful CI/test/security/backup/manual/release/scheduled workflows. No redundant workflow was removed. No direct SSH/Compose authority was added. No production image promotion, manifest apply, DB migration, shared pull-secret mutation, replica change, Pod restart or host reboot occurred.


## Runtime verification update — 2026-11-04 06:00 ICT / 2026-11-03 23:00 UTC

### Repository state and PR inventory
- Platform Infra master is `2e2b3571a8ed76a3b4221df092beeb3719b0c230`; the dedicated safety change is being prepared on `security/reconcile-manual-dispatch-default-plan-20261104-0600-ict`. TCE Dashboard master: `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend: `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation: `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication: `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- Open PRs: Platform #544/#541/#539 (draft); Auth #75 (ready) and #76 (draft); no open PRs in TCE, StockDividend or Media.
- Platform master latest verifiable run is recovery #41731787383 (workflow_dispatch, SUCCESS) after source reconciliation #41731497864. The source reconciliation is workflow_dispatch, completed FAILURE only at the StockDividend health lane. Shared reconciliation succeeded; GHCR pull Secret was unchanged; `ALLOW_IMAGE_CHANGES=false`; no GitOps drift, so manifest apply was skipped. Auth, MicroFE, Media and TCE lanes passed; Keycloak was skipped. Final gate correctly failed because Stock Admin and new Backend remained unready.
- Source reconciliation #41731497864 ran `restart-blocked-image-pulls`; the helper explicitly classified Stock Admin and Backend errors as permanent `no match for platform in manifest` and skipped rollout restart for both. No Stock Pod restart occurred in this run. It is not a native schedule tick.

### Latest native schedule evidence (filtered by event=schedule)
- Platform inspection #41726305748: 2026-11-03 21:56:27Z, SUCCESS. This is the newest native inspection schedule; its snapshot was generated 21:56:36Z.
- Platform watchdog #41715283880: 20:44:07Z, FAILURE due stale native Mirror/inspection/recovery evidence.
- Platform reconciliation #41714763176: 20:40:42Z, FAILURE only at StockDividend workload health.
- Platform recovery #41703551669: 19:28:20Z, SUCCESS.
- Platform mirror #41687882647: 17:49:06Z, FAILURE because `PLATFORM_INFRA_MIRROR_TOKEN` is missing.
- TCE WF-06 #41731424392: 22:30:44Z, FAILURE because TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 instead of required 200.
- TCE WF-12 #41727501039: 22:04:27Z, FAILURE because the latest WF-06 schedule at that time was 271m old (queue wait 0m). A later WF-06 native schedule #41731424392 did arrive at 22:30:44Z; its workflow_run follow-up #41731461425 succeeded, but that follow-up is not a native schedule tick.
- TCE WF-07 #41652078419: 14:16:34Z, SUCCESS. Do not count workflow_run, workflow_dispatch or repository_dispatch as native schedule delivery.

### Fresh K3s/VPS evidence
- Read-only native inspection snapshot `debug/vps-latest.md`, generated 2026-11-03T21:56:36Z: node `tce-k3s-01` Ready/ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 55%, ~19 GiB available RAM. Both Platform and Media runner services are active; runner policy v14. Host `restart_required: yes` because OS/containerd/Docker updates are pending.
- Media backend/frontend, MicroFE Shell/WS and NATS are 1/1. Stock Admin's two Pods and the new Backend Pod remain `ImagePullBackOff` on `12d63b4` with `no match for platform in manifest`; legacy Backend and Frontend remain 1/1. TCE/Auth/Keycloak remain at zero replicas.
- Reconciliation #41731497864 independently reconfirmed the Stock failure at 22:31:57Z; no production image or manifest change was applied.

### Dependency-safe implementation in this PR
- Manual `workflow_dispatch` for `reconcile-vps.yml` now defaults to `mode=plan`, so omitting the input cannot accidentally run a mutating production apply. Operators can still explicitly select `apply`.
- `scripts/validate-workflow-contracts.py` enforces the manual read-only default and verifies that scheduled, master-push and authenticated GitOps `repository_dispatch` events retain their existing automatic apply behavior.
- No cron expression, target scope, production environment, release gate or deployment authority changes. The TCE market-scan schedule is unchanged.
- Exact-head validation is pending PR creation/check completion; do not claim this change merged until checks pass and the exact PR head is verified.

### Blockers and next actions
1. Owner configures `PLATFORM_INFRA_MIRROR_TOKEN` with destination-only `Contents: write` on `phanthienquoc/locally-uncensored-private`; do not substitute GHCR or app-release tokens.
2. Owner verifies `STOCKDIVIDEND_ACTIONS_READ_TOKEN` in the protected production Environment and explicitly authorizes the paired Admin/Backend ARM64 release. Keep the release gate closed until both conditions are satisfied.
3. Keep Auth PR #75 behind authoritative Supabase integration/migration side-effect review; keep #76 draft. Media/Auth publisher E2E remains release-authorized work.
4. Continue observing native schedule events; latest WF-06 did arrive at 22:30Z but still reports endpoint health 503. Preserve strict HTTP 200 assertions.
5. Arrange a maintenance window before OS/containerd/Docker upgrades or reboot.

No production image promotion, GitOps manifest apply, database migration, shared GHCR pull-secret mutation, desired replica change, Stock Pod restart or host reboot occurred in this run. `reconcile-vps.yml` remains the sole production apply authority; no SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Post-merge follow-up — 2026-11-04 06:05 ICT / 2026-11-03 23:05 UTC

- Platform PR [#1173](https://github.com/phanthienquoc/platform-infra/pull/1173) was squash-merged at exact head `2bd04f7c076d1111d8a2eb128defff4887c4f303`, producing master `82676fb9b70865ccd908f0528ee5b790d68a3535`.
- The manual `reconcile-vps.yml` `workflow_dispatch.mode` now defaults to `plan`; an operator must explicitly select `apply` for a manual production apply. The validator enforces the default and preserves automatic apply for schedule, master push and authenticated `gitops-promoted-ready` repository_dispatch events.
- Exact-head PR checks all passed: `validate-manifests` #41736051679, `keycloak-ci` #41736051739 and `validate-github-actions` #41736051742.
- Post-merge master checks all passed: `validate-manifests` #41736157434, `keycloak-ci` #41736157416 and `validate-github-actions` #41736157474.
- The 06:00 ICT deployment checkpoint remains an accurate pre-merge snapshot; this follow-up records the completed merge and post-merge evidence.

### Current production status remains blocked
- Latest Platform reconciliation #41731497864 is a manual `workflow_dispatch` (not a native schedule), with `mode=apply`, `target_app=all`, `ALLOW_IMAGE_CHANGES=false`, shared preflight SUCCESS and no GitOps drift. Manifest apply was skipped. The StockDividend health lane failed on two Admin Pods and one new Backend Pod pulling `12d63b4` with `no match for platform in manifest`; Media, MicroFE, Auth and TCE lanes passed; Keycloak was skipped. The restart helper explicitly skipped the permanent Stock image-pull failures; no Stock Pod restart occurred.
- Recovery #41731787383 succeeded as a workflow_dispatch fallback and confirmed the native inspection activity was fresh. It is not native schedule evidence.
- Latest native Platform inspection #41726305748 (21:56:27Z) succeeded. Latest native reconcile #41714763176 (20:40:42Z) and watchdog #41715283880 (20:44:07Z) failed as recorded in the 06:00 checkpoint; recovery #41703551669 (19:28:20Z) passed; mirror #41687882647 (17:49:06Z) failed because `PLATFORM_INFRA_MIRROR_TOKEN` is absent.
- Latest native TCE WF-06 #41731424392 (22:30:44Z) arrived but failed all four public endpoint checks with HTTP 503. WF-12 native schedule #41727501039 (22:04:27Z) failed freshness at that time; its later workflow_run follow-up #41731461425 succeeded but is not a native schedule tick. WF-07 #41652078419 passed.
- K3s snapshot remains generated at 21:56:36Z: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB RAM available, runner policy v14, host restart required. Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- Open PRs remain Platform #544/#541/#539 (draft) and Auth #75 (ready)/#76 (draft). Auth validation passes but Supabase Preview is skipped; production integration/migration review remains a gate.
- Owner actions remain unchanged: provide destination-only Mirror token, verify Stock protected Actions-read token and authorize paired ARM64 release, complete Auth/Supabase review, and arrange host maintenance window.

No production image promotion, manifest apply, database migration, shared pull-secret mutation, replica change, Pod restart or host reboot occurred. `reconcile-vps.yml` remains the sole production apply authority. No direct SSH/Compose deployment authority or cron change was introduced; TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-04 07:00 ICT / 00:00 UTC

- **Master refs:** Platform Infra `d9d71bab60bb49dbdf68e85b93f1bc71d5b03880`; TCE `53227425841b6283bebad3bc5c93d509bd8a316a`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. Exact-head PR checks are green (#38575430454, #38567431761, #38548718033, #40446492086, #41329425940), but Auth production integration/migration review remains a separate gate.
- **Platform latest runs:** #41738969152 watchdog workflow_run SKIPPED; #41738925054 recovery repository_dispatch SUCCESS; #41738376640 manifest validation workflow_dispatch SUCCESS on automation/vps-inspection (not master); #41738272391 read-only inspection workflow_dispatch SUCCESS; #41737965410 explicit manual apply FAILURE only at StockDividend health.
- **Platform native schedules:** Mirror #41737911916 FAILURE (missing destination-only `PLATFORM_INFRA_MIRROR_TOKEN`); inspection #41726305748 SUCCESS; watchdog #41715283880 FAILURE (stale evidence); reconcile #41714763176 FAILURE (Stock health); recovery #41703551669 SUCCESS. Manual inspection #41738272391 is not a native tick.
- **TCE native schedules:** WF-07 backup #41739787575 SUCCESS; WF-07 integration #41738887996 SUCCESS; WF-06 #41731424392 FAILURE (four public endpoints HTTP 503 vs strict HTTP 200); WF-12 #41727501039 FAILURE (schedule freshness). No cron or market-scan change.
- **StockDividend:** master CI #41563856934 and image publisher #41563856933 PASS, but production release gate false; Platform handoff and digest dispatch SKIPPED. Admin/Backend production tag `12d63b4` is ARM64-incompatible. Owner token/authorization remain missing.
- **Media/Auth:** Media CI #41617592783 PASS; paired release E2E pending. Auth CI #41670642852 PASS; manual publisher/dispatch not observed. PR #75/#76 retain Supabase integration and migration review gates.
- **Latest reconciliation #41737965410:** manual event, explicit `mode=apply`, target all, `ALLOW_IMAGE_CHANGES=false`. Shared preflight and GHCR read-access checks passed. Existing Auth runtime Secret was re-applied from protected inputs (values suppressed); shared GHCR pull Secrets reported unchanged. GitOps drift false, manifest apply skipped. Stock Admin/Backend permanent `no match for platform in manifest` errors caused the only app-lane failure; helper correctly skipped restart. No DB migration, release promotion or scale-up.
- **Latest K3s snapshot:** #41738272391 generated `debug/vps-latest.md` at 23:20Z. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 55%, ~19 GiB available RAM, runner policy v14. Host restart required for pending Ubuntu/containerd/Docker updates. Media/MicroFE/NATS 1/1; Stock Admin two Pods and new Backend ImagePullBackOff on `12d63b4`; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0; OIDC probes HTTP 503.
- **Owner actions:** configure destination-only Mirror token; verify Stock protected Actions-read token and explicitly authorize paired ARM64 release; complete Auth/Supabase review; authorize Media/Auth E2E; arrange host maintenance window.
- **PR #1176:** documentation-only; exact head has no workflow/check/status runs because path filters do not match docs. Branch-protection required-check policy could not be read through the integration, so the PR remains open and unmerged.
- **Authority/safety:** app repos own tests/builds/immutable GHCR publication; Platform owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only apply authority. Preserve useful CI/test/security/manual/release/scheduled jobs. No SSH/Compose authority, production image promotion, manifest apply, DB migration, GHCR pull-secret change, replica change, Pod restart or reboot. Existing Auth runtime Secret was re-applied with values suppressed. TCE market-scan schedule unchanged.


## Workflow inventory PR state — 2026-11-04 07:00 ICT
- Platform PR #1176 contains only the tracker, inventory and two checkpoint documents. Exact-head workflow runs/statuses are empty because docs-only paths do not trigger the existing validation workflows. Branch-protection required-check policy is inaccessible through the current integration; leave the PR open until required-check policy is verified.


## Workflow inventory runtime update — 2026-11-04 08:00 ICT / 01:00 UTC

- **Repository heads:** Platform Infra 1fcfe9b326dc2f14ef90259820c78aa7f83e5718; TCE 53227425841b6283bebad3bc5c93d509bd8a316a; StockDividend 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media e4c7d8990aafc7d837e918c9caf39722d623de7c; Authentication f978a3f378ee22d4630909c2d182275b21ac9e9a.
- **Open PRs:** Platform #1176/#1178 and drafts #544/#541/#539; Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. #1176 exact-head validate passed but base is one commit behind current master; branch protection is not readable through the integration. #1178 current exact-head checks are running.
- **Platform native schedule authority:** reconcile-vps.yml remains the only production apply authority. Native reconcile #41750519522 failed only Stock health; watchdog #41750880073 failed stale Mirror/Inspection/Recovery evidence. Mirror #41737911916 failed because PLATFORM_INFRA_MIRROR_TOKEN is missing; native Inspection #41726305748 and Recovery #41744960810 are stale schedule successes. New manual inspection and recovery dispatch/workflow_run fallbacks are not native schedule evidence.
- **TCE scheduled workflows:** WF-07 Backup #41739787575 and Integration #41738887996 PASS; WF-06 #41731424392 FAIL on four HTTP 503 public endpoints; WF-12 #41727501039 FAIL on freshness. Keep strict HTTP 200 assertions and all cron expressions unchanged; TCE market-scan schedule unchanged.
- **StockDividend app publisher:** CI #41563856934 and publisher #41563856933 PASS. Admin, Backend and Scraper full-SHA tags were verified to resolve to ARM64 digests. release_enabled=false; Platform handoff and atomic digest dispatch SKIPPED. No production promotion.
- **Media and Auth:** master CI #41617592783/#41670642852 PASS. Media paired publisher E2E and Auth manual publisher E2E remain pending; Auth PR #75/#76 remain behind Supabase integration/migration review.
- **K3s:** read-only inspection #41750782322 generated 00:58:57 UTC snapshot. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 55%, ~19 GiB RAM available, runner policy v14. Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff on 12d63b4; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; public OIDC 503. Pending host packages remain; no maintenance.
- **New validator contract:** PR #1178 binds the watchdog schedule cadence to the recovery schedule and requires a three-interval recovery freshness budget. It changes no cron or deployment authority.
- **Owner gates:** Mirror destination-only token; Stock protected Actions-read token plus explicit paired ARM64 release authorization; Auth/Supabase review; Media/Auth E2E authorization; host maintenance window.
- **Safety:** no image promotion, GitOps manifest apply, DB migration, shared GHCR pull-secret mutation, replica change, Pod restart or host reboot. Preserve useful CI/test/security/manual/release/scheduled workflows. No SSH/Compose authority. TCE market-scan schedule unchanged.


## Post-merge workflow inventory follow-up — 2026-11-04 08:10 ICT / 01:10 UTC

- Platform Infra master advanced to 97cf87afc169a68d69f12bdec8dc39c2e338ebae after PR #1178 merged. Exact-head validate-manifests #41751765941 and validate-github-actions #41751765994 passed; post-merge validate-manifests #41751967678 passed; post-merge validate-github-actions #41751967612 passed at 01:08:57 UTC.
- New contract ownership: Platform Infra's cross-workflow validator now enforces that the recovery freshness watchdog runs at least as frequently as the recovery controller and that its freshness budget is exactly three maximum recovery schedule intervals. Current native cadence is 15 minutes for both, with a 45-minute recovery budget. No cron changed.
- PR #1176's exact-head validate-manifests #41751933952 passed, but the branch is two commits behind current master and GitHub reports mergeable=false. Replacement PR #1179 is open from current master on docs/cross-repo-readiness-20261104-0810-ict; old PR #1176 was closed as superseded.
- Native schedule health remains degraded: Platform Mirror missing destination token, Inspection and Recovery schedule evidence stale, Stock deployment health failing on permanent ARM64 manifest mismatch; TCE WF-06 public endpoints remain HTTP 503 and WF-12 freshness remains failed. TCE WF-07 Backup/Integration schedules pass.
- Stock app publisher remains green and has verified full-SHA ARM64 Admin/Backend/Scraper digests, but production release is disabled and Platform dispatch was skipped. Media/Auth CI passes; paired/manual publisher E2E and Auth/Supabase review remain gated.
- Production apply authority remains reconcile-vps.yml only. App repositories own tests/builds/immutable GHCR publication; Platform Infra owns production manifests, shared pull credentials, promotion/reconciliation and rollout/health. Preserve useful CI/test/security/manual/release/scheduled workflows. No SSH/Compose authority; TCE market-scan schedule unchanged.

- Cross-repo TCE schedule heartbeat is verified end-to-end: direct WF-12 schedule #41727501039 dispatched successfully and Platform recovery #41727515701 passed; scheduled WF-07 #41738887996 forwarded through WF-12 workflow_run #41738911293, and Platform recovery #41738925054 passed source repository/path/event/full-SHA/run-ID validation. WF-12's independent WF-06 freshness job still failed because WF-06 delivery was stale; this is not a dispatch or payload-authentication failure.


## Workflow inventory post-merge update — 2026-11-04 08:15 ICT / 01:15 UTC

- **Current master refs:** Platform Infra 12e1bb102a6d76c7094335f0c5c3d2b1ba24ca78; TCE 53227425841b6283bebad3bc5c93d509bd8a316a; StockDividend 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media e4c7d8990aafc7d837e918c9caf39722d623de7c; Authentication f978a3f378ee22d4630909c2d182275b21ac9e9a.
- **PR state:** Platform #1179 merged at exact head 67e1800c76c5e9ecb3198e9d913194f42a10ab99; exact-head validate-manifests #41752587927 and post-merge validate-manifests #41752671604 PASS. Platform #1178's exact-head and both post-merge checks PASS. PR #1176 closed as superseded. Remaining Platform drafts #544/#541/#539; Auth #75 ready/#76 draft.
- **TCE heartbeat:** WF-12 #41727501039 direct schedule and WF-07 #41738887996 -> WF-12 workflow_run #41738911293 both successfully dispatched authenticated heartbeats. Platform recovery #41727515701 and #41738925054 completed successfully; #41738925054 verified source repository/path/event/full SHA and both run IDs. WF-12's independent freshness check still fails because WF-06 is stale.
- **Native schedule health:** Platform reconcile #41750519522 fails only Stock health; watchdog #41750880073 reports stale Mirror/Inspection/Recovery. Mirror #41737911916 is missing PLATFORM_INFRA_MIRROR_TOKEN; native Inspection #41726305748 and Recovery #41744960810 are stale. TCE WF-07 Backup/Integration PASS; WF-06 #41731424392 HTTP 503; WF-12 #41727501039 freshness FAIL.
- **StockDividend publisher:** #41563856933 verified full-SHA ARM64 Admin/Backend/Scraper digests, but release_enabled=false and no Platform handoff/dispatch occurred. Production still has Admin/new Backend ImagePullBackOff on 12d63b4. Media/Auth CI pass; paired/manual E2E remains gated.
- **Authority/safety:** app repositories own tests/builds/immutable GHCR publication; Platform owns production manifests, shared pull credentials, promotion/reconciliation and rollout/health. reconcile-vps.yml remains sole production apply authority. Preserve useful CI/test/security/manual/release/scheduled workflows. No SSH/Compose authority. No production promotion, manifest apply, DB migration, secret mutation, replica change, Pod restart or host reboot. TCE market-scan schedule unchanged.


## Workflow inventory update — 2026-11-04 08:32 ICT / 01:32 UTC

- **Repository heads:** Platform Infra `e3668b0cdac49c4d06c89a32cedba655897cab43`; TCE Dashboard `8e9ed1e1a9428f524e53b733e417a5789b0ec479`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft); Auth #75 ready/#76 draft; no open PRs in TCE, StockDividend or Media. TCE #1020 merged at exact validated head; its post-merge push validations were queued at checkpoint time.
- **TCE app CI contract:** WF-05 now always runs `scripts/validate-wf-06-healthcheck-contract.sh` before backend build/tests. This closes the gap where the helper only ran from WF-02 Prettier when WF-06/WF-12/helper paths changed. Exact-head #41754584520 passed the new step, backend build and tests; WF-02 #41754584422 passed. No cron or market-scan schedule changed.
- **Platform native schedules:** Reconcile #41750519522 failed only Stock workload health; watchdog #41750880073 reported stale Mirror/Inspection/Recovery; Mirror #41737911916 missing `PLATFORM_INFRA_MIRROR_TOKEN`; native Inspection #41726305748 and Recovery #41744960810 are stale schedule successes. Manual fallback events are not native ticks.
- **TCE native schedules:** Backup #41739787575 and Integration #41738887996 PASS; WF-06 #41731424392 FAIL with four HTTP 503 public probes; WF-12 #41727501039 FAIL on WF-06 freshness. WF-12 workflow_run #41738911293 sent a valid Platform heartbeat but failed the 53m-vs-25m WF-06 freshness check; Platform receiver #41738925054 passed payload verification.
- **App publishers:** Stock CI #41563856934 and publisher #41563856933 PASS with verified full-SHA ARM64 Admin/Backend/Scraper digests; `release_enabled=false`, no Platform handoff/dispatch. Media CI #41617592783 and Auth CI #41670642852 PASS; paired/manual publisher E2E remains gated.
- **K3s:** Read-only inspection #41750782322 (workflow_dispatch, not schedule) shows node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB RAM available, runner policy v14. Media/MicroFE/NATS 1/1; Stock Admin (2 Pods) and new Backend ImagePullBackOff on `12d63b4` due `no match for platform in manifest`; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0. Host updates pending; no maintenance.
- **Owner gates:** Mirror destination-only Contents:write token; StockDividend-only Actions:read token plus explicit paired ARM64 release authorization; Auth/Supabase integration/migration review; Media/Auth E2E authorization; host maintenance window.
- **Authority/safety:** App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, digest promotion/reconciliation and rollout/health. `reconcile-vps.yml` remains sole production apply authority. No production promotion, manifest apply, database migration, shared GHCR credential mutation, release enablement, replica change, Pod restart or VPS reboot. No SSH/Compose authority. Preserve useful CI/test/security/manual/release/scheduled workflows. TCE market-scan schedule unchanged.


## Workflow inventory update — 2026-11-04 09:02 ICT / 02:02 UTC

- **Repository heads:** Platform Infra `d6bb3660371ce5dfb972cd93451c3e9cf5420f8a`; TCE Dashboard `a355ce070204cff209df1c9ba38843c972647860`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft, stale bases); Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. TCE #1021 merged at exact validated head; Platform tracker PR #1176 was closed as superseded without merge; Platform #1181 is merged in current master.
- **TCE contract ownership:** PR #1021 removes the duplicate changed-path invocation from WF-02 Prettier. WF-05 remains the single mandatory owner and runs on every push, pull_request and workflow_dispatch without path filters. The validator parses WF-05 and Prettier, asserts the WF-05 step is unconditional, and rejects a duplicate Prettier invocation. Exact-head WF-05 #41757885116 and WF-02 #41757885206 passed. Post-merge WF-02 #41758030952 passed; WF-05 #41758031060 and WF-01 #41758031017 were still running at 02:02 UTC.
- **Platform native schedule:** Reconcile #41750519522 failed only Stock health; watchdog #41750880073 failed Mirror/Inspection/Recovery freshness with queue wait 0m and deployment-lane assignment passing. Mirror #41737911916 failed before Git operations because `PLATFORM_INFRA_MIRROR_TOKEN` is empty. Native Inspection #41726305748 and Recovery #41744960810 are stale schedule successes. Manual inspection #41750782322 is read-only runtime evidence, not a schedule tick.
- **TCE native schedule:** WF-06 #41731424392 failed four public probes with HTTP 503; WF-12 #41727501039 failed WF-06 freshness; WF-07 Backup #41739787575 and Integration #41738887996 passed. WF-12 workflow_run #41738911293 dispatched a valid heartbeat and Platform receiver #41738925054 passed payload verification, but freshness still failed. TCE market-scan schedule unchanged.
- **App publishers:** Stock CI #41563856934 and publisher #41563856933 PASS with verified full-SHA ARM64 Admin/Backend/Scraper digests; `release_enabled=false`, Platform handoff/atomic dispatch SKIPPED. Media CI #41617592783 and Auth CI #41670642852 PASS; paired/manual E2E remains gated.
- **K3s:** Read-only inspection #41750782322 generated a 00:58:57 UTC snapshot. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 55%, ~19 GiB RAM available, runner policy v14. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due `no match for platform in manifest`; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0. Host updates pending; no maintenance.
- **Owner gates:** Mirror destination-only Contents:write token; Stock protected Actions:read token plus explicit paired ARM64 release authorization; Auth/Supabase integration/migration review; Media/Auth E2E authorization; host maintenance window.
- **Authority/safety:** App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, digest promotion/reconciliation and rollout/health. `reconcile-vps.yml` remains sole production apply authority. No production promotion, manifest apply, DB migration, shared GHCR credential mutation, release enablement, replica change, Pod restart or VPS reboot. Auth runtime Secret was re-applied with values suppressed; shared pull Secrets unchanged. No SSH/Compose authority. Preserve useful CI/test/security/manual/release/scheduled workflows. TCE market-scan schedule unchanged.


## Workflow inventory update — 2026-11-04 09:08 ICT / 02:08 UTC

- **Repository heads:** Platform Infra `9d657f0c0ec93c6c89303f0da27ea08327c9705f`; TCE Dashboard `a355ce070204cff209df1c9ba38843c972647860`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft, stale bases); Auth #75 ready/#76 draft; none in TCE, StockDividend or Media. Platform #1182/#1183 and TCE #1021 merged.
- **Recovery authority:** `recover-stale-ops.yml` now subscribes to the schedule freshness watchdog's completed runs, but its new path runs only for a failed native schedule watchdog event on master. Success, push smoke and workflow_run diagnostics do not trigger it. Existing freshness checks still gate dispatch to `reconcile-vps.yml` or read-only `inspect-vps.yml`; no second apply authority.
- **PR #1183 exact-head checks:** validate-github-actions #41758621386 PASS; validate-manifests #41758621288 PASS. An intermediate lint head failed only yamllint line length (141 > 140); converted the workflow source list to block YAML and final exact-head checks passed. Post-merge #41758724456/#41758724485 were in progress at 02:08 UTC.
- **PR #1182:** exact-head #41758220815 and post-merge #41758285427 validate-manifests PASS.
- **TCE #1021:** exact-head WF-05 #41757885116 and WF-02 #41757885206 PASS; post-merge WF-05 #41758031060, WF-01 #41758031017 and WF-02 #41758030952 PASS. WF-05 exclusively owns the mandatory WF-06/WF-12 contract; duplicate conditional invocation removed from Prettier while formatting remains.
- **Platform native schedules:** reconcile #41750519522 failed only Stock health; watchdog #41750880073 failed Mirror/Inspection/Recovery freshness with queue wait 0m and lane assignment passing. Mirror #41737911916 failed before Git operations because `PLATFORM_INFRA_MIRROR_TOKEN` is empty. Native Inspection #41726305748 and Recovery #41744960810 are stale successes; manual inspection #41750782322 is not a schedule tick.
- **TCE native schedules:** WF-06 #41731424392 failed four public probes with HTTP 503; WF-12 #41727501039 failed WF-06 freshness; WF-07 Backup #41739787575 and Integration #41738887996 passed. WF-12 workflow_run #41738911293 dispatched a valid heartbeat and Platform receiver #41738925054 passed payload verification, but freshness remains failed.
- **App publishers:** Stock CI #41563856934 and publisher #41563856933 PASS with verified full-SHA ARM64 Admin/Backend/Scraper digests; `release_enabled=false`, Platform handoff/atomic dispatch SKIPPED. Media CI #41617592783 and Auth CI #41670642852 PASS; paired/manual E2E remains gated.
- **K3s:** read-only inspection #41750782322 generated 00:58:57 UTC snapshot. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 55%, ~19 GiB RAM available, runner policy v14. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due `no match for platform in manifest`; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0. Host updates pending.
- **Owner gates:** Mirror destination-only Contents:write token; Stock protected Actions:read token plus explicit paired ARM64 release authorization; Auth/Supabase integration/migration review; Media/Auth E2E authorization; host maintenance window.
- **Authority/safety:** App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, digest promotion/reconciliation and rollout/health. `reconcile-vps.yml` remains sole production apply authority. No production promotion, manifest apply, DB migration, shared GHCR credential mutation, release enablement, replica change, Pod restart or VPS reboot. Auth runtime Secret re-applied with values suppressed; shared pull Secrets unchanged. No SSH/Compose authority. Preserve useful CI/test/security/manual/release/scheduled workflows. TCE market-scan schedule unchanged.


## Runtime evidence update — 2026-11-04 09:13 ICT / 02:13 UTC

- Latest native Platform Inspection #41758796515 (schedule, 02:08:48 UTC) PASS. Latest native Watchdog remains #41750880073 (schedule, 00:59:41 UTC); #41758946874 is only a workflow_run diagnostic and failed stale Reconcile/Mirror/Recovery freshness with queue wait 0m. Recovery #41758977950 correctly SKIPPED because the source event was workflow_run, not schedule.
- TCE WF-12 #41759196674 (schedule, 02:12:22 UTC) failed WF-06 freshness but its authenticated heartbeat dispatch passed. Payload source path/run/SHA matched WF-12 #41759196674 / `a355ce070204cff209df1c9ba38843c972647860`. Platform receiver #41759211141 validated the payload and completed SUCCESS without duplicate reconciliation. Latest WF-06 schedule #41731424392 age 221m, queue 0m.
- Recovery controller #41758946954 was triggered by native Inspection #41758796515 and dispatched `reconcile-vps.yml` #41758966117 with `mode=apply`, `allow_image_changes=false`, `target_app=all`, exact master SHA `92a3e140f7aed6a94cdad8578effd0b309f1e374`.
- Shared reconciliation passed GHCR preflight, Auth runtime Secret provision/verification, TCE release-pairing and Media digest resolution. GHCR pull Secrets in all four production namespaces were unchanged. Restart helper skipped permanent Stock ARM64 manifest mismatch; no transient image-pull failures were found. Kubernetes diff reported no drift; workload-image guard and manifest apply were skipped.
- Auth/TCE/Media/MicroFE health lanes PASS; Keycloak skipped; Stock health FAIL due Admin two Pods and new Backend ImagePullBackOff on tag `12d63b4` (`no match for platform in manifest`). Overall reconcile #41758966117 FAILURE solely because Stock lane failed. Old Stock Backend/legacy Frontend remain 1/1.
- Post-reconcile recovery #41759189967 SUCCESS with no duplicate dispatch. TCE heartbeat recovery #41759211141 SUCCESS with no duplicate dispatch.
- Platform PR #1183 merged with exact-head lint #41758621386 and validate #41758621288 PASS; post-merge #41758724485 and #41758724456 PASS. New watchdog recovery path's negative gate was exercised; positive native schedule-failure path remains unobserved.
- App ownership and production authority unchanged. No promotion, manifest apply, DB migration, shared pull-secret mutation, release enablement, replica change, Pod restart or VPS reboot. Auth runtime Secret provision/verification step ran with values suppressed; shared GHCR Secrets unchanged. TCE market-scan schedule unchanged.


## Workflow inventory update — 2026-11-04 09:28 ICT / 02:28 UTC

### Current repository heads and PR state
- Platform Infra: `9ab987f8d876ba1f2e1c30f77f2edafa6727b147`; open #544/#541/#539 (draft), #1187 merged.
- TCE Dashboard: `a355ce070204cff209df1c9ba38843c972647860`; no open PRs.
- StockDividend: `50ba0dfb67eb3dfaa376db0c752bbef5f0817bec`; no open PRs.
- Media Generation: `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no open PRs.
- Authentication: `f978a3f378ee22d4630909c2d182275b21ac9e9a`; open #75 (ready) and #76 (draft).

### Workflow ownership and latest evidence
| Repository | Workflow ownership | Latest verified evidence | Readiness |
|---|---|---|---|
| Platform Infra | Production manifests; shared GHCR pull credentials; GitOps promotion/reconciliation; K3s rollout/health; read-only inspection; schedule recovery; mirror | PR #1187 exact-head lint #41760394034 PASS and manifest #41760394024 PASS; post-merge #41760891957/#41760892039 PASS. Native Inspection #41758796515 PASS; native Watchdog #41750880073 FAIL stale; native Reconcile #41750519522 FAIL Stock; Mirror #41737911916 FAIL missing token. | BLOCKED |
| TCE Dashboard | App tests/build/publisher; strict public WF-06 health; WF-07 backup/integration; WF-12 schedule freshness and authenticated heartbeat | Master WF-05 #41758031060, WF-01 #41758031017, WF-02 #41758030952 PASS. Native WF-12 #41759196674 FAIL freshness but heartbeat accepted by Platform #41759211141; WF-06 #41731424392 FAIL four HTTP 503 probes; WF-07 backup #41739787575 and integration #41738887996 PASS. | PUBLIC HEALTH BLOCKED |
| StockDividend | App CI/build; immutable full-SHA GHCR publication and paired digest dispatch | Master CI #41563856934 and publisher #41563856933 PASS; publisher handoff/dispatch SKIPPED while release remains disabled. Production Admin/Backend tag `12d63b4` fails ARM64 pull with no matching platform manifest. | RELEASE BLOCKED |
| Media Generation | App CI/build and immutable GHCR publication; Platform owns deployment and runtime health | Master CI #41617592783 PASS; backend/frontend 1/1 and digest-pinned in latest K3s snapshot. Paired publisher E2E pending. | RUNTIME HEALTHY; E2E PENDING |
| Authentication | Auth service/web CI and immutable release publisher; Platform owns production manifests and runtime Secret | Master auth-service CI #41670642852 PASS; runtime Secret verification passed in reconciliation with values suppressed; Auth remains 0/0. PR #75/#76 await Supabase integration/migration review; manual publisher E2E pending. | ACTIVATION BLOCKED |

### Recovery and schedule contract
- `recover-stale-ops.yml` now selects the newest master reconciliation and inspection by exact workflow `.path`, master branch and `created_at` from the current Actions run page. This allows recent `workflow_dispatch` fallback runs to suppress duplicate dispatches.
- The failure-only native watchdog recovery gate remains intact; successful/diagnostic `workflow_run` events do not trigger production recovery.
- Manual reconciliation defaults to read-only plan; schedule/master-push/authenticated GitOps promotion retain their existing apply behavior. Existing freshness budgets are unchanged.
- TCE WF-05 remains the single unconditional CI owner for the WF-06/WF-12 contract. WF-02 retains formatting only; no duplicate invocation.
- Preserve all purposeful CI/test/security/manual/release/scheduled workflows. No TCE market-scan cron change.

### Production readiness and gates
- K3s `tce-k3s-01`: Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available RAM, runner policy v14. Host maintenance pending (`restart_required=yes`).
- Healthy: Media backend/frontend, MicroFE Shell/WS, NATS. Unhealthy: Stock Admin (2 Pods) and new Backend (ImagePullBackOff, ARM64 manifest mismatch). Existing Stock Backend and legacy Frontend remain 1/1. TCE/Auth/Keycloak 0/0.
- Owner actions: Mirror destination-only Contents:write token; protected Stock Actions:read token plus explicit paired ARM64 release authorization; Auth/Supabase migration review; Media/Auth E2E authorization; host maintenance window.
- App repos remain the only build/publish owners. Platform Infra remains the only production manifest/promotion/reconciliation/health owner. `reconcile-vps.yml` is the sole apply authority; no SSH/Compose deployment authority.
- No image promotion, manifest apply, DB migration, shared pull-secret mutation, release enablement, replica change, Pod restart or VPS reboot in this checkpoint. TCE market-scan schedule unchanged.


## Workflow inventory update — 2026-11-04 09:55 ICT / 02:55 UTC

### Current repository and PR inventory
| Repository | Master SHA | Open PRs | Current readiness |
|---|---|---:|---|
| Platform Infra | `3f591e9aaddb` | #544/#541/#539 (draft) | Promotion/reconciliation owner; Stock and Mirror blocked |
| TCE Dashboard | `a355ce070204` | 0 | App CI PASS; public WF-06 health 503 |
| StockDividend | `50ba0dfb67eb` | 0 | CI/publisher PASS; production release disabled; live Admin/Backend image pull blocked |
| Media Generation | `e4c7d8990aaf` | 0 | CI PASS; runtime backend/frontend 1/1; paired publisher E2E pending |
| Authentication | `f978a3f378ee` | #75 ready / #76 draft | CI PASS; service 0/0; Supabase/migration review gates remain |

Auth PR #75/#76 both have current visible validate checks SUCCESS and Supabase Preview SKIPPED. Do not treat skipped preview as a successful production integration test.

### New Platform paired digest helper
- `scripts/promote-paired-image-digests.py` is now the single implementation for StockDividend backend/admin and Media backend/frontend paired digest rewrites.
- Called from `.github/workflows/gitops-image-promotion.yml` only for `component=release`, after the existing source-run provenance and GHCR tag-to-digest validation.
- `validate-manifests.yml` runs Python compile and helper self-tests. `validate-workflow-contracts.py` statically requires the helper invocation and test wiring.
- PR #1189 exact-head checks #41764217505/#41764217540/#41764217582 all PASS; post-merge checks #41764297891/#41764297953/#41764297783 all PASS. Merge SHA `3f591e9aaddb55f28f7e49438c0d18c92e05208f`.
- The helper is an offline file transformation only. It does not publish images, verify credentials, alter production manifests on master, or trigger a deployment by itself.

### Workflow ownership and schedule evidence
| Repository / workflow | Owner | Latest verified evidence | Status |
|---|---|---|---|
| Platform `reconcile-vps.yml` | Platform Infra | Native #41750519522 FAIL Stock; manual #41762538154 FAIL Stock; shared preflight PASS, drift false, apply skipped | BLOCKED by Stock runtime |
| Platform `inspect-vps.yml` | Platform Infra | Native #41758796515 SUCCESS | Latest observed native inspection |
| Platform `reconcile-schedule-watchdog.yml` | Platform Infra | Native #41750880073 FAILURE | Stale native schedule lanes; queue not established as cause |
| Platform `recover-stale-ops.yml` | Platform Infra | #41762735716 and #41764298072 SUCCESS | Fallbacks avoided when latest master activity was fresh |
| Platform Mirror | Platform Infra | #41737911916 FAILURE | Missing `PLATFORM_INFRA_MIRROR_TOKEN` |
| TCE WF-06 | TCE app | Native #41762490285 FAILURE; four public endpoints HTTP 503 | Schedule delivered; public health blocked |
| TCE WF-12 | TCE app | Native #41759196674 FAILURE; workflow_run #41762512743 SUCCESS | Heartbeat/forwarder works; direct cron freshness remains degraded |
| TCE WF-07 backup/integration | TCE app | #41739787575/#41738887996 SUCCESS | PASS |
| StockDividend CI/publisher | Stock app | #41563856934/#41563856933 SUCCESS | ARM64 publication verified; promotion gate false |
| Media CI | Media app | #41617592783 SUCCESS | Runtime 1/1; E2E pending |
| Auth CI | Auth app | #41670642852 SUCCESS | Runtime stopped; integration/migration review pending |

### Production workload and authority
- K3s node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, runner policy v14. Media backend/frontend, MicroFE Shell/WS and NATS are 1/1. Stock Admin (two Pods) and new Backend are ImagePullBackOff on old tag `12d63b4` due to no matching ARM64 manifest; old Backend and legacy Frontend remain 1/1. TCE/Auth/Keycloak are 0/0.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, publisher provenance/digest validation, GitOps promotion/reconciliation and K3s rollout/health verification.
- `reconcile-vps.yml` remains the sole production apply authority. No duplicate direct SSH/Compose deployment authority. Preserve purposeful CI/test/security/manual/release/scheduled jobs.
- Owner gates: destination-only Mirror Contents:write token; protected Stock Actions:read token plus explicit paired ARM64 release authorization; Auth/Supabase integration/migration review; Media/Auth publisher E2E authorization; host maintenance window.
- No production promotion, manifest apply, DB migration, shared pull-secret mutation, release enablement, replica change, Pod restart or VPS reboot in this checkpoint. TCE market-scan schedule unchanged.


## Cross-repository deployment checkpoint — 2026-11-04 10:58 ICT / 03:58 UTC

### Repository heads and pull requests
- Platform Infra master: `cce9a1755c48f0695ba4ef523fd8a7f43b93fec3` (PR #1194 merged). Follow-up contract cleanup is on branch `fix/retire-locally-uncensored-contracts`.
- TCE Dashboard master: `a355ce070204cff209df1c9ba38843c972647860`; no open PRs.
- StockDividend master: `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no open PRs.
- Media Generation master: `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no open PRs.
- Authentication master: `f978a3f378ee22d4630909c2d182275b21ac9e9a`; open PRs #75 (ready) and #76 (draft).
- Other open Platform Infra PRs: #544, #541 and #539 (all drafts). TCE, StockDividend and Media have no open PRs.

### Detached integration — owner-directed
- PR #1194 merged at 04:00:24 UTC as `cce9a1755c48f0695ba4ef523fd8a7f43b93fec3`; it removes `.github/workflows/mirror-locally-uncensored.yml`. The private destination repository is not deleted.
- The exact-head validation run #41770293998 failed because the workflow-contract validator still required the deleted mirror file; manifest validation #41770294038 passed. The PR was merged before this contract dependency was corrected.
- Follow-up branch `fix/retire-locally-uncensored-contracts` removes the mirror subscriptions from recovery/watchdog, removes mirror freshness monitoring and obsolete credential documentation, and changes workflow-contract validation to fail if the mirror workflow is reintroduced without explicit owner authorization.
- Historical mirror run evidence in this append-only inventory is retained as history, not as an active deployment requirement. Do not restore the mirror workflow, its schedule, or its recovery/watchdog hooks unless the owner explicitly requests it.

### Current workflow ownership
- App repositories remain responsible for tests/builds and immutable GHCR publication: TCE Dashboard, StockDividend, Media Generation and Authentication.
- Platform Infra remains responsible for production manifests, shared GHCR pull credentials, publisher provenance/digest validation, GitOps promotion/reconciliation, K3s rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` is read-only. No direct SSH/Compose deployment authority is introduced.
- Preserve purposeful CI, tests, security, backups, manual/release/maintenance and scheduled jobs. TCE market-scan schedules are unchanged.

### Readiness and owner gates
- Latest recorded checkpoint before this update (09:55 ICT) showed Platform reconciliation blocked by StockDividend Admin/Backend ARM64 image-manifest mismatch; TCE public WF-06 checks returned HTTP 503 while TCE/Auth were scaled to zero; Media runtime was 1/1; Auth remained 0/0 pending Supabase/migration review.
- StockDividend production release remains disabled. Do not promote until the protected Actions-read credential and explicit paired ARM64 release authorization are present.
- Auth PR #75/#76 remain gated on Supabase production integration side effects and migration provenance/drift review. A skipped Supabase Preview is not production integration evidence.
- Media/Auth publisher E2E and VPS maintenance-window gates remain unresolved in the latest recorded runtime checkpoint.
- Latest exact PR check evidence available in this run is #41770293998 (workflow-contract failure described above) and #41770294038 (manifest validation success). The connector does not expose a repository-wide Actions run listing in this session; do not infer newer native schedule or live K3s health results from old checkpoints.

### Safety
- No production manifest/image reference, release-enable flag, shared GHCR credential, database object, replica, pod, or TCE market-scan schedule was changed by this checkpoint.


## Post-merge verification — 2026-11-04 11:02 ICT / 04:02 UTC

- PR #1195 merged by squash as `a704c9dd63c026e327e2d52ae20786bfc3fd7134` after the exact PR head `ea29d3f939fba566b0a5c81ebe590e7e9140b7e1` passed `validate-github-actions` run #41770698592 and `validate-manifests` run #41770698653.
- Post-merge source verification on master: `.github/workflows/mirror-locally-uncensored.yml` returns 404 (absent); `recover-stale-ops.yml` and `reconcile-schedule-watchdog.yml` contain no mirror trigger; active credential inventories contain no mirror credential reference; `validate-workflow-contracts.py` fails if the workflow is recreated without explicit owner authorization.
- PR #1194 is merged as `cce9a1755c48f0695ba4ef523fd8a7f43b93fec3`; PR #1195 is merged as above. The private mirror repository itself was not deleted.
- Exact PR checks are verified. The connected GitHub interface did not return post-merge Actions runs or combined commit statuses for the merge SHA, so no post-merge CI result is claimed.
- No production rollout, image promotion, manifest mutation, credential mutation, database write, K3s restart or TCE market-scan schedule change occurred. The latest live-runtime readiness evidence remains the 09:55 ICT checkpoint until a fresh inspection is available.
- Restoration is prohibited unless the owner explicitly asks for it; do not recreate the workflow, schedule, recovery/watchdog subscriptions, or token documentation.


## Active workflow inventory and readiness — 2026-11-04 12:03 ICT / 05:03 UTC

### Current repository and PR inventory
| Repository | Master SHA | Open PRs | Readiness |
|---|---|---|---|
| Platform Infra | `7e26b75dba3e` | #544/#541/#539 (draft) | Production owner; Stock workload blocked; native schedule evidence stale |
| TCE Dashboard | `a355ce070204` | 0 | CI PASS; strict public WF-06 probes return 503 while TCE/Auth are 0/0 |
| StockDividend | `50ba0dfb67eb` | 0 | CI and immutable ARM64 publication PASS; release handoff/dispatch skipped; production tag `12d63b4` cannot pull on ARM64 |
| Media Generation | `e4c7d8990aaf` | 0 | CI PASS; last inspected runtime 1/1 at 09:08 ICT (stale); paired publisher E2E pending |
| Authentication | `f978a3f378ee` | #75 ready / #76 draft | CI PASS; Auth 0/0; Supabase/migration review and publisher E2E pending |

### Active workflow ownership and evidence
| Repository / workflow | Owner | Latest verified evidence | Status |
|---|---|---|---|
| Platform `reconcile-vps.yml` | Platform Infra | Manual #41762538154: shared preflight PASS, drift false, apply skipped, Stock health FAIL | Sole production apply authority; blocked by Stock |
| Platform `inspect-vps.yml` | Platform Infra | Native #41758796515 SUCCESS at 02:08:48 UTC | Read-only; stale, next safe dispatch is inspection |
| Platform `recover-stale-ops.yml` / `reconcile-schedule-watchdog.yml` | Platform Infra | Native watchdog #41750880073 FAIL stale; push diagnostic #41770766300 PASS but still reports stale native runs | Keep schedules and freshness enforcement; diagnostic is not cron |
| Platform `gitops-image-promotion.yml` | Platform Infra | Stock handoff and paired dispatch skipped by release gate; no production image mutation | Digest/provenance promotion only after authorization |
| Platform `validate-manifests.yml` / `validate-github-actions.yml` | Platform Infra | Current master manifest #41770814934 PASS; post-merge workflow validation #41770766313 PASS | Retain validation checks |
| TCE WF-01/WF-02/WF-05 | TCE app | #41758031017/#41758030952/#41758031060 PASS | App CI owner |
| TCE WF-06 | TCE app | Native #41762490285 FAIL, four HTTP 503 responses vs expected 200 | Keep strict; public health blocked |
| TCE WF-07 Backup/Integration | TCE app | #41739787575/#41738887996 PASS | Preserve backup/integration jobs |
| TCE WF-12 | TCE app | Native #41759196674 freshness FAIL; workflow_run #41762512743 forwarding PASS | Preserve native schedule and authenticated heartbeat |
| StockDividend CI / Build and Publish Images | Stock app | #41563856934/#41563856933 PASS; Scraper/Admin/Backend full-SHA ARM64 digests verified | Release dispatch skipped; owner authorization required |
| Media CI / publisher | Media app | #41617592783 PASS; no paired publisher E2E observed | App owns publication; Platform owns rollout |
| Auth service CI / release handoff | Auth app | #41670642852 PASS including immutable release-contract and manual action pin checks | No manual release dispatch; activation gated |

### Shared production and release gates
- Platform's shared `GHCR_READ_TOKEN`/Kubernetes pull credential contract remains platform-owned. Latest manual reconciliation passed GHCR pull access and shared credential checks; no credential mutation is claimed.
- Stock immutable ARM64 digests are recorded in the deployment tracker. Production still references non-ARM64 tag `12d63b4`; keep release gate closed until `STOCKDIVIDEND_ACTIONS_READ_TOKEN` is verified and paired promotion is explicitly authorized.
- Auth PR #75/#76 remain gated on Supabase integration/migration side effects; Supabase Preview SKIPPED is not production evidence.
- Media/Auth publisher E2E and VPS maintenance window remain pending.
- TCE/Auth/Keycloak 0/0 and public HTTP 503 are not reclassified as healthy. Do not change TCE market-scan schedules.

### Retired workflow
- `.github/workflows/mirror-locally-uncensored.yml` is RETIRED by PR #1194/#1195. No active recovery/watchdog subscription, freshness check or credential documentation remains. The contract validator rejects reintroduction without explicit owner authorization.
- Historical checkpoint files may retain prior mirror-token failure notes as append-only evidence. Do not configure `PLATFORM_INFRA_MIRROR_TOKEN`; do not recreate or auto-add this integration.

### Next actions
1. Trigger/verify a read-only Platform inspection while separately monitoring for native `event=schedule` delivery. Keep all existing cron declarations unchanged.
2. Obtain explicit StockDividend release authorization and protected Actions:read credential; then rerun publisher handoff and promote paired immutable digests through Platform Infra.
3. Complete Auth/Supabase migration and integration review before merging gated Auth PRs or activating Auth.
4. Run Media/Auth publisher E2E only after authorization; schedule host maintenance before reboot/upgrade.

No production apply, promotion, database migration, secret mutation, replica change, Pod restart, VPS reboot or TCE market-scan schedule change occurred in this checkpoint.


## Active workflow inventory — 2026-11-04 13:02 ICT / 06:02 UTC

### Current repository heads and PRs
| Repository | Master SHA | Open PRs | CI / publication evidence |
|---|---|---|---|
| Platform Infra | `be3e61837dfc` | #544/#541/#539 (draft) | Master manifest validation #41777462054 PASS |
| TCE Dashboard | `a355ce070204` | 0 | WF-01 #41758031017, WF-02 #41758030952, WF-05 #41758031060 PASS |
| StockDividend | `50ba0dfb67eb` | 0 | CI #41563856934 and publisher #41563856933 PASS; no later run |
| Media Generation | `e4c7d8990aaf` | 0 | CI #41617592783 PASS; no paired publisher E2E observed |
| Authentication | `f978a3f378ee` | #75 ready / #76 draft | Auth service CI #41670642852 PASS; release not dispatched |

### Active Platform production and schedule workflows
| Workflow | Latest observed event | Latest evidence | Status |
|---|---|---|---|
| `reconcile-vps.yml` | Native schedule | #41750519522 FAILURE; Stock workload health gate | Sole apply authority; keep strict |
| `inspect-vps.yml` | Native schedule | #41758796515 SUCCESS at 09:08 ICT | Read-only; stale at 13:02 ICT |
| `recover-stale-ops.yml` | Native schedule | #41744960810 SUCCESS at 07:11 ICT | No newer native schedule returned |
| `reconcile-schedule-watchdog.yml` | Native schedule | #41750880073 FAILURE at 07:59 ICT; recovery age 48m vs 45m budget | Native schedule freshness degraded |
| `gitops-image-promotion.yml` | Release handoff gated | No paired production promotion | Preserve provenance and digest gate |
| `validate-manifests.yml` | Push | #41777462054 PASS on current master | Active validation |
| `validate-github-actions.yml` | Push | #41770766313 PASS on previous post-merge head | Active validation; no newer run returned |

### App workflow evidence
| Repository / workflow | Latest evidence | Status |
|---|---|---|
| TCE WF-06 | Native #41762490285 FAILURE; four public endpoints HTTP 503 | Keep strict; public health blocked |
| TCE WF-12 | Native #41759196674 FAILURE; freshness | Keep schedule and heartbeat contract |
| TCE WF-07 Backup / Integration | #41739787575 / #41738887996 SUCCESS | Preserve |
| Stock CI / immutable publisher | #41563856934 / #41563856933 SUCCESS | ARM64 digest publication was previously verified; production release still gated |
| Media CI / publisher | #41617592783 SUCCESS; no E2E publisher run observed | Preserve app-side CI/publisher |
| Auth CI / release | #41670642852 SUCCESS; no new release dispatch | Preserve manual release; activation gated |

### Open PR checks and production side-effect gates
- Platform #544/#541/#539 each have a successful exact-head `validate-manifests` run (#38575430454/#38567431761/#38548718033); all remain drafts.
- Auth #75 exact-head CI #40446492086 PASS, but owner-provided Supabase Dashboard evidence in the PR says GitHub integration is connected to the repository root and `Deploy to production=ON` for `master`. Keep open because merge may trigger production database deployment while migration drift is unresolved.
- Auth #76 exact-head CI #41329425940 PASS, remains draft; migration provenance/drift investigation incomplete.
- A successful test-only check does not override external production integration side effects. Do not merge #75/#76 on CI status alone.

### Runtime and ownership
- Last fresh-enough K3s evidence is still inspection #41758796515 at 09:08 ICT; at that time Media/MicroFE/NATS were 1/1 and TCE/Auth/Keycloak 0/0. Last reconciliation #41762538154 at 09:43 ICT confirmed Stock Admin/Backend ImagePullBackOff on tag `12d63b4` due to missing ARM64 manifest. No new live K3s inspection was available by 13:02 ICT.
- Native Platform schedules have no newer `event=schedule` run in the returned Actions history after inspection #41758796515, watchdog #41750880073, reconciliation #41750519522 and recovery #41744960810. Keep all cron expressions intact; do not count manual/push diagnostics as native schedule delivery.
- App repositories own tests/builds and immutable GHCR publishing. Platform Infra owns production manifests, shared pull credentials, provenance/digest validation, GitOps promotion/reconciliation, K3s rollout and health verification.
- `reconcile-vps.yml` is the only production apply authority. `inspect-vps.yml` is read-only. Preserve useful CI/test/security/manual/release/scheduled jobs; do not introduce direct SSH/Compose deployment authority.
- `locally-uncensored-private` remains retired from active workflows by owner direction. The private repository remains untouched; do not restore its mirror workflow, cron, watchdog/recovery hooks or token references without explicit owner authorization.

### Next actions
1. Obtain a fresh read-only inspection and separately verify native schedule delivery; workflow_dispatch could not be invoked by the available automation interface in this run.
2. Resolve Stock's protected Actions:read credential and explicit paired ARM64 release authorization before any digest promotion.
3. Complete Supabase production integration and migration drift review before Auth merge/activation.
4. Keep TCE health strict and market-scan schedules unchanged; arrange maintenance window before host restart/upgrade.


## Cross-repo workflow inventory update — 2026-11-04 13:56 ICT / 06:56 UTC

- Platform master `0b00384174bc`; open draft PRs #544/#541/#539. Latest master manifest validation #41783214164 PASS; latest master workflow validation #41770766313 PASS before the recovery guard change.
- TCE master `a355ce070204`; no open PRs. WF-01/WF-02/WF-05 PASS; WF-07 scheduled integration #41785211971 PASS; WF-12 #41785231592 FAIL because WF-06 schedule run #41762490285 is 221m stale and its four public probes returned HTTP 503. Preserve all TCE schedules, especially market-scan.
- Stock master `50ba0dfb67eb`; no open PRs. CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. Production tag `12d63b4` remains non-ARM64; paired promotion remains gated.
- Media master `e4c7d8990aaf`; no open PRs. CI #41617592783 PASS; latest inspection at 13:26 ICT observed backend/frontend 1/1; paired publisher E2E remains pending authorization.
- Authentication master `f978a3f378ee`; #75 ready and #76 draft. Exact-head Auth CI checks PASS; keep production Supabase/migration and activation gates.
- Platform native schedule watchdog #41787664409 FAIL: reconcile native run #41750519522 age 349m and inspect native run #41758796515 age 276m; both workflows report active. Native recovery schedule #41787641688 PASS and did not need a fallback dispatch because latest all-event master reconcile/inspection activities were 19m/17m old.
- Recovery follow-up #41787700107 was SKIPPED after the failed watchdog. Recovery's job guard incorrectly referenced `github.event.workflow.path`; changed on branch `fix/recovery-workflow-run-source-ids-20261104` to compare verified `github.event.workflow_run.workflow_id` values (reconcile 364209709, inspect 364209707, watchdog 402675709). Contract validator updated to enforce this webhook-payload identity contract and reject the invalid field.
- Latest read-only K3s snapshot #41785522310 (13:26 ICT): node Ready; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on old non-ARM64 tag; old Backend/legacy Frontend 1/1; Auth and Keycloak 0/0; host restart required. No production changes, credential mutation, migration or reboot.
- `locally-uncensored-private` remains retired from active workflow inventory. `reconcile-vps.yml` remains the sole production apply authority. No direct SSH/Compose authority and no TCE market-scan schedule changes.


## Post-merge verification — 2026-11-04 14:03 ICT / 07:03 UTC

- Recovery source-filter fix PR #1199 merged at `a7cd5802dcbc72911db8be6144fa793fd96e737a`.
- Exact PR-head validation: #41789478283 `validate-github-actions` PASS and #41789478238 `validate-manifests` PASS on `64748b34ee61535f5aa40ca1256e4d0211fd46d1).
- Post-merge master validation: #41789565946 `validate-github-actions` PASS and #41789566021 `validate-manifests` PASS on the merge SHA.
- Recovery now identifies source completions using the verified `workflow_run.workflow_id` values (reconcile 364209709, inspection 364209707, watchdog 402675709); contract validation rejects the absent top-level `github.event.workflow.path` reference.
- Runtime confirmation is pending the next native scheduled watchdog/recovery cycle. Do not mark the fallback runtime path repaired solely from static/CI validation.
- No cron or TCE market-scan schedule change; no production manifest/image/credential/database/Pod/host mutation. `reconcile-vps.yml` remains the sole apply authority.


## Cross-repo workflow inventory — 2026-11-04 14:59 ICT / 07:59 UTC

- **Platform Infra** master `ff2d8a9a3add`; open draft PRs #544/#541/#539, each exact-head manifest validation PASS. Latest master `validate-manifests` #41789761594 and `validate-github-actions` #41789565946 PASS. Native reconcile #41792374251 failed only at Stock workload health; native watchdog #41792527398 failed native inspect freshness; latest native recovery schedule #41787641688 passed at 13:45 ICT.
- **TCE Dashboard** master `a355ce070204`; no open PRs. WF-01/WF-02/WF-05 PASS. Native WF-07 #41785211971 PASS. WF-06 #41762490285 FAIL (four public endpoints HTTP 503); latest native WF-12 #41759196674 FAIL (WF-06 schedule freshness). Workflow_run WF-12 #41785231592 forwarded the Platform heartbeat but also failed freshness; do not count it as a native schedule tick. Preserve all schedules and market-scan cadence.
- **StockDividend** master `50ba0dfb67eb`; no open PRs. CI #41563856934 and publisher #41563856933 PASS. Publisher independently verifies immutable full-SHA tags and linux/arm64 digests for Scraper/Admin/Backend (see deployment tracker). Handoff and paired digest dispatch remain SKIPPED by release gate; production tag `12d63b4` still cannot pull on ARM64.
- **Media Generation** master `e4c7d8990aaf`; no open PRs. CI #41617592783 PASS; no paired publisher E2E observed. Last inspected backend/frontend 1/1 at 13:26 ICT, snapshot now stale.
- **Authentication** master `f978a3f378ee`; PR #75 ready / #76 draft, exact-head Auth CI PASS. No release dispatch or production activation; Supabase integration/migration review remains a gate; last inspected desired replicas 0/0.
- Recovery guard runtime: native watchdog failure #41792527398 triggered successful recovery #41792556931 after PR #1199; fallback inspection was correctly skipped because manual inspection #41785522310 was 62m old at recovery time. A later recovery #41792618152 also succeeded; the subsequent workflow_run watchdog failure #41792618193 was not allowed to recurse into recovery (#41792641990 skipped by event guard). Native inspect schedule remains stale; do not claim it was repaired.
- Last K3s snapshot #41785522310 (13:26 ICT): node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, restart required; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend and legacy Frontend 1/1; TCE/Auth/Keycloak 0/0.
- `locally-uncensored-private` remains retired; `reconcile-vps.yml` remains the sole production apply authority. No direct SSH/Compose authority. No production promotion, credential/DB mutation, replica/Pod change, host reboot or TCE market-scan schedule change.


## Checkpoint documentation merge verification — 2026-11-04 15:05 ICT

- PR #1201 merged by squash as `617a1f64ba54abad3683d1d3196784ec23c09f41`.
- Exact-head `validate-manifests` #41796718439 and post-merge master `validate-manifests` #41796804225 both PASS.
- PR touched only the deployment tracker and workflow inventory; the path-filtered GitHub Actions workflow validation was not applicable.
- No newer native Platform or TCE schedule event was observed after the 14:59 ICT checkpoint. The native inspect-vps schedule remains stale; latest K3s snapshot is still the manual inspection #41785522310.


## Cross-repo live readiness inventory — 2026-11-04 16:00 ICT / 09:00 UTC

| Repository | Current master | Open PRs | Latest relevant CI / workflow evidence | Production status |
|---|---|---|---|---|
| Platform Infra | `f4bfdec712a3` | #544/#541/#539 (draft) | #41797011126 manifest validation PASS; native reconcile #41792374251 FAIL at Stock health; watchdog #41792527398 FAIL due missing native inspection schedule event | Sole apply authority; no apply/image change |
| TCE Dashboard | `a355ce070204` | None | WF-01 #41758031017, WF-02 #41758030952, WF-05 #41758031060 PASS; WF-07 #41785211971 PASS; WF-06 #41762490285 FAIL (HTTP 503); WF-12 #41759196674 FAIL (freshness) | TCE/Auth workloads 0/0 in latest K3s snapshot; keep strict health contract |
| StockDividend | `50ba0dfb67eb` | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS | Admin and new Backend Pods ImagePullBackOff on production tag `12d63b4`; release handoff/dispatch gated |
| Media Generation | `e4c7d8990aaf` | None | Media CI #41617592783 PASS | Backend/frontend 1/1 in 16:00 ICT snapshot; no publisher E2E claim |
| Authentication | `f978a3f378ee` | #75 ready / #76 draft | Auth CI #41670642852 PASS; exact-head checks for #75/#76 previously PASS | Auth and Keycloak 0/0; Supabase/migration and activation gates remain closed |

### Platform operational ownership
- `inspect-vps.yml` is read-only. Rerun #41785522310 attempt 2 produced a fresh snapshot at 16:00 ICT; its generated PR #1203 passed exact-head manifest validation #41803947887 but could not merge because it was based on stale SHA `8921555e7cf73a6cb16e95c47cb5bd7c46d458a4` and conflicted with current master. A replacement branch is being prepared from current master.
- `reconcile-vps.yml` is still the only production apply authority. Native reconcile #41792374251 passed shared preflight and non-Stock lanes but failed the Stock health lane; production image apply was skipped.
- Native Platform schedules are stale/missing: latest reconcile #41792374251 (14:27 ICT), watchdog #41792527398 (14:28 ICT), recovery schedule #41787641688 (13:45 ICT); no native scheduled inspect-vps event in the latest 100-run history. Workflow_run recovery is not a substitute for native schedule delivery.
- Last live snapshot is the new 16:00 ICT read-only inspection: node Ready; Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart required with pending package updates.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health.
- Stock release remains disabled until the owner-configured protected Actions:read credential and explicit paired Admin/Backend digest promotion authorization are available.
- Auth #75/#76 remain gated on Supabase integration target/effect and migration drift review. Media/Auth publisher E2E remains pending authorization.
- Preserve useful CI/test/security/manual/release/scheduled workflows. Do not create direct SSH/Compose deployment authority. `locally-uncensored-private` remains retired.
- TCE market-scan schedule and all existing cron declarations remain unchanged.


## Post-merge inspection verification — 2026-11-04 16:00 ICT / 09:04 UTC

- Platform Infra PR #1204 merged as `49e8ea6e60168ce1702303ad7535f49bc4278958`; exact-head validation #41804308471 PASS and post-merge master validation #41804382004 PASS.
- PR #1203 was closed as superseded because its branch was based on old master and GitHub rejected the merge with conflicts. No force merge was attempted.
- Current Platform master includes the fresh read-only `debug/vps-latest.md` snapshot generated at 16:00:13 ICT plus updated cross-repo tracker/inventory.
- Snapshot confirms node Ready, ARM64, K3s v1.36.3+k3s1, disk 55%; Media backend/frontend, MicroFE Shell/WS and NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart required.
- No production rollout, image promotion, credential/database change, Pod/replica mutation, host reboot or cron change occurred. `reconcile-vps.yml` remains the sole apply authority; TCE market-scan schedule unchanged.


## Inspection rebase runtime inventory — 2026-11-04 16:12 ICT / 09:12 UTC

| Repository | Master SHA | Open PRs | Latest CI evidence | Runtime / release gate |
|---|---|---|---|---|
| Platform Infra | `a1c0f1bfa5b7` | #544/#541/#539 (draft) | #41805382982 workflow contracts PASS; #41805383142 manifests PASS; inspect #41805382965 SUCCESS | #1207 fixed native Git auth; #1208 fresh snapshot merged after exact-head validation #41805481821 PASS |
| TCE Dashboard | `a355ce070204` | None | WF-01 #41758031017, WF-02 #41758030952, WF-05 #41758031060 PASS; WF-07 #41785211971 PASS; WF-06 #41762490285 and WF-12 #41759196674 FAIL | TCE/Auth 0/0; strict 503 health remains unhealthy; market-scan schedule untouched |
| StockDividend | `50ba0dfb67eb` | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS | Admin/new Backend ImagePullBackOff on `12d63b4`; release promotion still gated |
| Media Generation | `e4c7d8990aaf` | None | CI #41617592783 PASS | Backend/frontend 1/1 in 16:11 ICT snapshot |
| Authentication | `f978a3f378ee` | #75 ready / #76 draft | CI #41670642852 PASS | Auth/Keycloak 0/0; Supabase/migration activation gates remain closed |

### VPS inspection workflow contract
- The self-hosted runner does not provide `gh`; PR #1207 removed that dependency and uses a per-command Git HTTP extraheader with the workflow token.
- Push run #41805382965 exercised the new rebase step successfully, created PR #1208 from current master, validated its exact head with #41805481821, and squash-merged it. No stale-base conflict occurred.
- The read-only snapshot confirms Node Ready, disk 55%, Media/MicroFE/NATS 1/1, Stock Admin/new Backend ImagePullBackOff, old Stock Backend/Frontend 1/1, TCE/Auth/Keycloak 0/0, and host restart required.
- Native Platform schedule evidence remains stale: reconcile #41792374251 14:27 ICT failed at Stock health; watchdog #41792527398 14:28 ICT failed on missing scheduled inspection; recovery schedule #41787641688 13:45 ICT passed. Workflow_run recovery events are not native schedules.
- Native TCE health schedule evidence remains stale/degraded; preserve strict HTTP 200 assertions and do not weaken health semantics.
- App repositories own CI/build and immutable GHCR publication; Platform Infra owns manifests, pull credentials, promotion/reconciliation, rollout and health.
- Preserve useful CI/test/security/manual/release/scheduled jobs; do not add direct SSH/Compose deployment authority.
- Stock release, Auth activation and Media/Auth publisher E2E remain gated pending explicit authorization/credentials.
- `locally-uncensored-private` remains retired. TCE market-scan schedule and all cron declarations unchanged.


## Workflow inventory checkpoint — 2026-11-04 17:16 ICT / 10:16 UTC

| Repository | CI / publication | Scheduled / operational status | Owner / gate |
|---|---|---|---|
| Platform Infra | PR #1213 exact-head and post-merge validations PASS | Native inspect #41809725184 failed on GitHub remote 500; watchdog #41792527398 stale; reconcile #41792374251 blocked by Stock health; recovery #41787641688 PASS | Sole production apply authority; #1214 snapshot PR awaiting safe validation |
| TCE Dashboard | WF-01/02/05 PASS | WF-06 #41810552435 native schedule FAIL: four endpoints HTTP 503; WF-12 #41810610019 workflow_run PASS; WF-07 #41785211971 native schedule PASS | Keep strict HTTP 200 and all schedules; market-scan unchanged |
| StockDividend | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS | Admin and new Backend Pods ImagePullBackOff on production tag `12d63b4` | App owns build/publish; promotion requires explicit paired-digest release authorization |
| Media Generation | CI #41617592783 PASS | Latest 17:14:55 ICT inspection: backend/frontend 1/1 | App owns build/publish; publisher E2E remains gated |
| Authentication | CI #41670642852 PASS; PR #75/#76 exact-head validate PASS | Auth/Keycloak 0/0; public OIDC HTTP 503 | Supabase integration/migration review before merge/activation |

### Platform inspection workflow contract
- PR #1213 adds bounded exact-head merge retries for transient HTTP 000/500/502/503/504 and passed actionlint, yamllint, ShellCheck, ops regression, workflow-contract and manifest validation.
- PR #1214's snapshot is not treated as merged evidence because its exact-head validation polling hit HTTP 502. The replacement checkpoint carries the 17:14:55 ICT snapshot and adds bounded retry for GitHub API GET calls.
- Inspection remains read-only. GitOps apply remains in `reconcile-vps.yml`; no second SSH/Compose deployment authority is permitted.
- Preserve manual, release, security, CI/test, and scheduled workflows. Do not remove or reschedule useful jobs.
- `locally-uncensored-private` remains detached. TCE market-scan schedule remains unchanged.


## Workflow inventory checkpoint — 2026-11-04 17:23 ICT / 10:23 UTC

| Repository | Latest verified CI / publication | Latest operational evidence | Open PRs / gate |
|---|---|---|---|
| Platform Infra | PR #1215 exact-head and post-merge validation PASS | Push inspection #41813598197 PASS; exact-head snapshot validation #41813734720 PASS; PR #1216 merged. Native schedule remains stale: inspect #41809725184 FAIL, watchdog #41792527398 FAIL, reconcile #41792374251 FAIL, recovery #41787641688 PASS | #544/#541/#539 drafts; no production apply from this checkpoint |
| TCE Dashboard | WF-01 #41758031017, WF-02 #41758030952, WF-05 #41758031060 PASS | WF-06 #41810552435 native schedule FAIL (four HTTP 503); WF-12 #41810610019 workflow_run PASS; WF-07 #41785211971 schedule PASS | No PRs; preserve strict HTTP 200 and all schedules |
| StockDividend | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS | Stock Admin/new Backend Pods ImagePullBackOff on `12d63b4` | No PRs; paired Admin/Backend digest promotion remains gated |
| Media Generation | CI #41617592783 PASS | Latest inspection 17:21:39 ICT: backend/frontend 1/1 | No PRs; publisher E2E remains gated |
| Authentication | CI #41670642852 PASS; PR #75/#76 exact-head validation PASS | Auth/Keycloak 0/0; OIDC HTTP 503 | #75 ready, #76 draft; Supabase/migration gate remains |

### Inspection API reliability contract
- Inspection validation now uses bounded GET retries for HTTP 000/500/502/503/504 across validation-run polling and PR-state verification.
- Retry support is bounded; non-transient 4xx and changed PR heads remain hard failures.
- The new code completed one full push-triggered inspection/validation/squash-merge cycle successfully (#41813598197 / #41813734720 / PR #1216). No actual retry warning was observed in that successful run.
- PR #1214 was closed unmerged as superseded; its snapshot was incorporated in PR #1215. PR #1216 supplies the newer 17:21:39 ICT snapshot.
- Preserve useful CI, tests, security, manual, release and scheduled workflows. Do not add a second deployment authority or alter the TCE market-scan cadence.


## Cross-repo workflow inventory — 2026-11-04 18:05 ICT / 11:05 UTC

- **Platform Infra** master `b2a3bf0c15c1`; PR #1217 merged. Current open drafts #544/#541/#539 each have exact-head `validate` PASS but mergeability false. Post-merge manifest validation #41818356594 PASS. Latest observed native inspect #41809725184 (16:45 ICT) failed in the pre-retry revision while pushing a reused static branch; push inspection #41813598197 (17:21 ICT) succeeded with the newer unique-branch/rebase flow, but is not a schedule event. No newer native schedule events were found by 18:05 ICT. Current master cron declarations remain inspect `2,32`, reconcile `7,22,37,52`, watchdog `12,27,42,57`, recovery `10,25,40,55` (all hourly, UTC). Do not change them to conceal missing schedule delivery.
- **TCE Dashboard** master `a355ce070204`; no open PRs. WF-01/02/05 PASS. WF-06 schedule #41810552435 failed at 16:53 ICT and rerun attempt 2 failed at 18:05 ICT with HTTP 503 on all four public endpoints. WF-12 native #41807645689 failed freshness; workflow_run #41810610019 PASS is not a native schedule tick. WF-07 native #41785211971 PASS. Preserve strict HTTP 200 and all schedules, especially market-scan.
- **StockDividend** master `50ba0dfb67eb`; no open PRs. CI #41563856934 and immutable full-SHA publisher #41563856933 PASS. Master guard, promotion gate and image build/push PASS; handoff and paired-digest dispatch SKIPPED. Production tag `12d63b4` remains non-ARM64; keep paired Admin/Backend promotion gated on protected Actions:read access and explicit authorization.
- **Media Generation** master `e4c7d8990aaf`; no open PRs. CI #41617592783 PASS; latest K3s snapshot at 17:21 ICT observed backend/frontend 1/1. No publisher E2E authorization observed.
- **Authentication** master `f978a3f378ee`; PR #75 ready and #76 draft. Current exact-head validate checks PASS; Supabase Preview checks SKIPPED. Keep #75/#76 gated on production integration effects and migration drift/provenance review; Auth/Keycloak latest snapshot 0/0.
- Latest K3s evidence is read-only snapshot #41813598197, generated 17:21:39 ICT and committed by PR #1216: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart required. No newer inspection could be dispatched in this automation run.
- Platform native schedules have no newer schedule-event evidence after the listed 16:45 inspect / 14:28 watchdog / 14:27 reconcile / 13:45 recovery runs. Successful push and workflow_run events are not substitutes for native schedule ticks. Next action: run read-only `inspect-vps.yml` via workflow_dispatch on master and inspect GitHub Actions workflow enablement/delivery for the scheduled workflows.
- `reconcile-vps.yml` remains the sole production apply authority. App repos own tests/builds and immutable GHCR publication; Platform Infra owns production manifests, shared pull credentials, digest promotion/reconciliation, rollout and health.
- `locally-uncensored-private` remains retired; no direct SSH/Compose deployment authority was added. No production mutation, host reboot, credential/database change, image promotion or TCE market-scan schedule change occurred.


## Cross-repo workflow inventory — 2026-11-04 18:30 ICT / 11:30 UTC

| Repository | Master SHA | Open PRs | Latest CI / publisher evidence | Runtime / release gate |
|---|---|---|---|---|
| Platform Infra | `1bb34fb6cddc` | #1222 draft; #544/#541/#539 drafts | #41821072245 action validation PASS; #41821072276 manifest validation PASS; #1222 #41821355040 manifest validation PASS only | #1221 first-attempt heartbeat guard merged; no post-merge native schedule event. #1222 is not deployable: missing UID/GID forwarding for shell isolation and direct Docker/K8s mutation tools conflict with GitOps authority (review comment #6629554340). |
| TCE Dashboard | `52cecd5584e6` | None | #1022 exact-head WF-02/WF-05 PASS on PR SHA; no current-master combined status | WF-06 #41810552435 native schedule FAIL (four HTTP 503); WF-12 #41807645689 native schedule FAIL; WF-07 #41785211971 PASS. First-attempt heartbeat payload is now present on master; runtime confirmation pending. |
| StockDividend | `50ba0dfb67eb` | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS | Admin/new Backend remain ImagePullBackOff on `12d63b4`; release gate disabled, handoff and paired digest dispatch SKIPPED. |
| Media Generation | `e4c7d8990aaf` | None | CI #41617592783 PASS | Last snapshot observed backend/frontend 1/1 at 17:21 ICT; no new publisher E2E. |
| Authentication | `f978a3f378ee` | #75 ready; #76 draft | CI #41670642852 PASS | Auth/Keycloak 0/0; Supabase/migration and activation gates remain closed; no current-head release publisher run observed. |

### Schedule and runtime evidence
- Platform native schedules: inspect #41809725184 (16:45 ICT) FAIL; reconcile #41792374251 (14:27 ICT) FAIL; watchdog #41792527398 (14:28 ICT) FAIL; recovery #41787641688 (13:45 ICT) PASS. No newer native schedule event observed through 18:30 ICT.
- TCE native schedules: WF-06 #41810552435 (16:53 ICT) FAIL, four public endpoints HTTP 503; WF-12 #41807645689 (16:27 ICT) FAIL; WF-07 #41785211971 (13:23 ICT) PASS. Workflow_run #41818548221 (18:05 ICT) is not a native schedule tick and predates the new first-attempt payload guard.
- The current Platform and TCE master commits both contain first-attempt-only schedule heartbeat protection. No post-merge native schedule cycle has validated the guard yet.
- Latest K3s evidence remains read-only snapshot #41813598197 at 17:21:39 ICT: node Ready, disk 55%; Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart required. Snapshot is stale; no current health claim.
- Preserve all existing cron declarations and the TCE market-scan schedule. Do not treat push, workflow_run, repository_dispatch or rerun attempts as native schedule evidence.

### Publisher and ownership contract
- StockDividend: immutable ARM64 publication PASS; promotion remains disabled and requires the protected Actions:read credential plus explicit paired Admin/Backend digest authorization.
- Media: paired frontend/backend digest publisher and Platform dispatch contract present; no new publisher E2E observed.
- Auth: manual workflow_dispatch release emits full-SHA release tag, immutable digest and source provenance; Platform verifies source run and tag-to-digest correlation. Current-head release execution not observed.
- App repos own tests/builds and immutable GHCR publication. Platform owns production manifests, shared GHCR pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No duplicate SSH/Compose or MCP Docker/Kubectl mutation authority is permitted.
- `locally-uncensored-private` remains retired. No production mutation, image promotion, secret/database change, Pod/replica change or host reboot occurred.


## Cross-repo workflow inventory — 2026-11-04 19:02 ICT / 12:02 UTC

- **Platform Infra** master `7b2eada1d42c`; open PRs #1222 draft and Keycloak drafts #544/#541/#539. Current master manifest validation #41822407438 PASS; action validation #41821072245 belongs to prior master `1bb34fb6`. PR #1222 manifest check #41821355040 PASS only; security/TypeScript checks are not established. Native inspect #41809725184 (16:45 ICT) failed on old workflow revision with GitHub remote HTTP 500 during push to the reused static branch. Current master has a per-run branch and rebase; no newer native schedule event through 19:02 ICT. Native reconcile #41792374251 (14:27 ICT) failed Stock health; watchdog #41792527398 (14:28 ICT) failed freshness; native recovery #41787641688 (13:45 ICT) passed but is stale.
- **TCE Dashboard** master `52cecd5584e6`; no open PRs. Latest native WF-06 #41810552435 (16:53 ICT) failed strict HTTP 200 on all four endpoints with HTTP 503. Native WF-12 #41807645689 (16:27 ICT) failed because its 25-minute WF-06 schedule freshness budget was exceeded; WF-07 #41785211971 (13:23 ICT) passed. Recent WF-02/WF-05 checks #41819221546/#41819221509 are on prior PR head `a1afaf1c`, not the current master SHA. Do not weaken endpoint checks or alter market-scan schedule.
- **StockDividend** master `50ba0dfb67eb`; no open PRs. CI #41563856934 and immutable full-SHA ARM64 publisher #41563856933 PASS. Production still uses Admin/Backend tag `12d63b4` without ARM64 manifest; release gate and paired digest handoff remain disabled pending protected Actions:read access and explicit paired promotion authorization.
- **Media Generation** master `e4c7d8990aaf`; no open PRs. CI #41617592783 PASS. Latest snapshot at 17:21 ICT showed frontend/backend 1/1; no newer runtime snapshot or publisher E2E observed.
- **Authentication** master `f978a3f378ee`; PR #75 ready and #76 draft. Auth CI #41670642852 PASS; Supabase Preview remains skipped. Auth and Keycloak are 0/0 in the latest snapshot; keep merge/activation gated on Supabase integration effects and migration drift/provenance review.
- Latest K3s evidence is `debug/vps-latest.md` generated 17:21:39 ICT: node Ready/ARM64, disk 55%, restart required; Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0. This snapshot is stale; no current-health claim.
- No native schedule events newer than the listed runs were returned at 19:02 ICT. Read-only dispatch of `inspect-vps.yml` via workflow_dispatch is the next operational evidence step, but the available GitHub connector exposes read/write PR/file operations and run inspection, not workflow_dispatch. Do not substitute rerun or workflow_run events.
- PR #1222 must remain draft: missing actual UID/GID forwarding to child shell and direct Docker/Kubectl mutation paths conflict with GitOps-only production authority; reproducible TypeScript/test/YAML/ShellCheck/lockfile validation is also missing.
- `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` is read-only. App repos own tests/builds and immutable publication; Platform owns manifests, pull credentials, digest/provenance checks, promotion, reconciliation and rollout health.
- `locally-uncensored-private` remains retired. No production image promotion, manifest/credential/database mutation, replica/Pod change, host reboot or TCE market-scan schedule change occurred.


## Cross-repo workflow inventory — 2026-11-04 20:04 ICT / 13:04 UTC

| Repository | Current master | Latest verified CI / publisher | Native schedule / runtime | Open PRs / owner gate |
|---|---|---|---|---|
| Platform Infra | `a17b896e45db` | #41826435566 current-head manifest validation PASS; #41821072245 action validation PASS on prior master | Native inspect #41809725184 (16:45 ICT) failed pushing old static branch; current master uses run-specific branch but no new native tick. Reconcile #41792374251 failed Stock health; watchdog #41792527398 stale; recovery schedule #41787641688 last PASS. Latest K3s snapshot 17:21 ICT is stale. | #1222 draft; #544/#541/#539 drafts. Sole production apply authority. |
| TCE Dashboard | `52cecd5584e6` | WF-01 #41758031017 PASS on master; WF-02 #41819221546 and WF-05 #41819221509 PASS on prior PR head | WF-06 #41810552435 native schedule failed all four HTTP 200 checks (503); WF-12 #41807645689 failed freshness; WF-07 #41785211971 PASS. | No PRs; strict health contract and market-scan schedule unchanged. |
| StockDividend | `50ba0dfb67eb` | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; handoff/paired dispatch SKIPPED | Production Admin/new Backend still ImagePullBackOff on `12d63b4`; old Backend/legacy Frontend last observed 1/1. | No PRs; paired digest promotion requires protected Actions:read credential and explicit authorization. |
| Media Generation | `e4c7d8990aaf` | CI #41617592783 PASS; latest observed WF-03 #41158598649 is from Oct 31 | Last K3s snapshot 17:21 ICT observed backend/frontend 1/1; no fresh snapshot/publisher E2E. | No PRs; publisher E2E remains gated. |
| Authentication | `f978a3f378ee` | Service CI #41670642852 PASS on master; web CI #41542942080 is on prior master; PR #75/#76 validate PASS, Supabase Preview SKIPPED | Auth/Keycloak 0/0 in stale 17:21 ICT snapshot; no production activation. | #75 ready, #76 draft; Supabase/migration gate remains closed. |

### Cross-repo deployment contract and blockers

- App repos own test/build and immutable GHCR publication. Stock's current-master publisher completed ARM64 manifest verification for Scraper/Admin/Backend; Platform handoff and paired digest dispatch remain skipped. Never promote Admin or Backend independently.
- Platform owns manifests, shared GHCR pull credentials, source-run/tag/digest provenance checks, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only.
- The latest Stock health log proves the production tag `12d63b4` has no ARM64 manifest for Admin and Backend. Preserve the failure gate until paired immutable digest promotion is authorized and verified.
- TCE WF-06 public endpoints return HTTP 503 while HTTP 200 is required. WF-12's 25-minute freshness check fails separately from endpoint health. Preserve the strict status and all cron expressions.
- Platform's 16:45 native inspection failure was on old master `9f74d23` and old static branch `automation/vps-inspection`; current master has run-specific branches. A fresh native schedule tick is still needed to verify current code.
- PR #1222 remains draft because UID/GID isolation is not wired to the child process and Docker/Kubernetes mutation tools bypass GitOps. Its manifest check alone does not establish TypeScript/security readiness.
- Latest K3s snapshot at 17:21 ICT is stale. Host maintenance remains pending; no reboot/upgrade was performed.
- `locally-uncensored-private` remains retired. Preserve useful CI, tests, security, manual/release/scheduled jobs. Do not create direct SSH/Compose or MCP mutation authority. TCE market-scan schedule and all cron declarations remain unchanged.


## Cross-repo workflow inventory — 2026-11-04 21:04 ICT / 14:04 UTC

- **Platform Infra** master `8540179260f106ac47fc8747445cd9cee18c02ea`; open PRs #1222 draft and #544/#541/#539 drafts. Current-master `validate-manifests` #41835432534 PASS. Latest `validate-github-actions` #41821072245 PASS belongs to prior master `1bb34fb6cddc`, so current-head action validation is not yet established. Native inspection #41809725184 (16:45 ICT) failed on the old static-branch revision; last recorded native reconcile #41792374251 (14:27 ICT) failed Stock health, watchdog #41792527398 (14:28 ICT) failed freshness, and recovery #41787641688 (13:45 ICT) passed but is stale.
- **TCE Dashboard** master `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`; no open PRs. WF-02 #41819221546 and WF-05 #41819221509 PASS on PR SHA `a1afaf1cc04e`, not current master. Latest native WF-06 #41810552435 (16:53 ICT) failed all four public endpoint checks with HTTP 503; WF-12 #41807645689 (16:27 ICT) failed freshness; WF-07 #41785211971 (13:23 ICT) passed. Preserve strict HTTP 200 and all cron declarations, including market-scan.
- **StockDividend** master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no open PRs. CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. Publisher build/manifest checks passed, while the release handoff and paired digest dispatch were SKIPPED. Production Admin/Backend still reference `12d63b4`, which has no ARM64 manifest and remains ImagePullBackOff. Do not promote either image independently.
- **Media Generation** master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no open PRs. CI #41617592783 PASS. Last inspected backend/frontend were 1/1; snapshot is stale and publisher E2E remains gated.
- **Authentication** master `f978a3f378ee22d4630909c2d182275b21ac9e9a`; PR #75 ready and #76 draft. Auth service CI #41670642852 PASS; Supabase Preview SKIPPED. Keep PR #75 gated because the owner-provided Supabase GitHub integration deploys to production on master and exact merge side effects still require authoritative confirmation; keep migration-drift work read-only.
- Latest K3s snapshot remains `debug/vps-latest.md`, generated 17:21:39 ICT: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0; OIDC HTTP 503; host restart required. No current-health claim.
- Added a GitOps-only optional MCP guard on branch `guard/gitops-only-vps-mcp-20261104-2104-ict`: `scripts/validate-vps-control-mcp-contract.py`, manifest validation wiring and a workflow-contract assertion. It rejects Docker/Kubernetes/SSH mutation paths, mutating RBAC and missing shell UID/GID forwarding/configuration. On current master the optional MCP is absent; the open draft #1222 must remain blocked until it meets this contract and supplies build/test/lockfile evidence.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. Recovery/watchdog only inspect and dispatch existing workflows. App repositories own tests/builds and immutable GHCR publication; platform-infra owns manifests, shared pull credentials, provenance checks, paired digest promotion, reconciliation and health verification.
- No production image promotion, manifest apply, credential/database mutation, Pod/replica change or host reboot occurred. `locally-uncensored-private` remains retired. No cron expression or TCE market-scan schedule changed.

Full checkpoint: [2026-11-04 21:04 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-04-2104-ict.md).


## Cross-repo workflow inventory — 2026-11-04 21:18 ICT / 14:18 UTC

- **Platform Infra** master `67029764bb3ece241da364723ca43e8c98383210`. PR #1226 merged the optional VPS MCP GitOps-only/read-only contract; PR #1227 excludes that validator from recovery push triggers; PR #1228 merged a fresh read-only K3s snapshot. Exact-head and post-merge validation for #1226/#1227 passed; #1228 inspection and exact-head manifest validation passed. Open PRs #1222, #544, #541, #539 remain drafts. The new validator rejects Docker/Kubernetes/SSH mutation paths, mutating RBAC and missing shell UID/GID forwarding/configuration if an optional MCP is added.
- **Recovery trigger behavior:** #1226's new `scripts/validate-vps-control-mcp-contract.py` initially matched `scripts/**` and caused recovery #41845398314 to dispatch reconcile #41845426647. Reconcile preflight succeeded, Auth Secret was already complete, GHCR pull Secrets were unchanged, Stock permanent image errors were not restarted, GitOps drift was clean and manifest apply was skipped. Auth/Media/TCE/MicroFE lanes passed; Stock health failed. #1227 adds the explicit path exclusion and regression assertion; its merge did not trigger another push recovery run.
- **Fresh K3s inspection:** #41845846869 (workflow_dispatch) generated `debug/vps-latest.md` at 2026-11-04T14:16:14Z and PR #1228 merged as `67029764bb3ece241da364723ca43e8c98383210`. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, runner policy v14. Media backend/frontend, MicroFE Shell/WS and NATS 1/1 with digest-pinned Media imageIDs. Stock Admin (two Pods) and new Backend remain ImagePullBackOff on non-ARM64 `12d63b4`; old Backend and legacy Frontend 1/1. TCE/Auth/Keycloak 0/0; public OIDC 503; GitOps drift clean; host restart_required=yes with containerd/Docker/Ubuntu updates pending.
- **TCE Dashboard** master `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`; no PRs. Native WF-06 #41810552435 (16:53 ICT) failed four HTTP 200 endpoint checks with 503; WF-12 #41807645689 (16:27 ICT) failed freshness; WF-07 #41785211971 (13:23 ICT) passed. Preserve all cron declarations and the market-scan schedule.
- **StockDividend** master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no PRs. CI #41563856934 and immutable ARM64 publisher #41563856933 passed; release handoff/paired dispatch skipped. Keep production image references unchanged until protected Actions:read access and explicit paired Admin/Backend authorization.
- **Media Generation** master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no PRs. CI #41617592783 passed; fresh inspection confirms backend/frontend 1/1 with pinned digests.
- **Authentication** master `f978a3f378ee22d4630909c2d182275b21ac9e9a`; PR #75 ready and #76 draft. Auth CI #41670642852 passed; Supabase Preview skipped. Keep production integration/migration changes gated.
- **Native schedule status:** Platform inspect #41809725184 (16:45 ICT) failed; reconcile #41792374251 (14:27 ICT) failed Stock health; watchdog #41792527398 (14:28 ICT) failed freshness; recovery #41787641688 (13:45 ICT) passed but is stale. TCE WF-06/WF-12 remain failed and WF-07 passed as above. Workflow_dispatch/workflow_run recovery and inspection do not count as native schedule ticks.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` is read-only. App repositories own tests/builds and immutable GHCR publication; platform-infra owns manifests, shared pull credentials, provenance, promotion, reconciliation and health. `locally-uncensored-private` remains retired. No production image, manifest, credential, database, Pod, replica or host mutation occurred. TCE market-scan schedule unchanged.

Full checkpoint: [2026-11-04 21:18 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-04-2118-ict.md).


---

# Cross-repo workflow inventory checkpoint — 2026-11-04 21:58 ICT / 14:58 UTC

- Platform Infra master `74782e9034e41d613e60e8ef72dcdded6d5aa164`; open PRs #1222, #544, #541, #539 remain drafts. Tracker file `docs/cross-repo-deployment-tracker.md` was found zero bytes and is being restored in this PR.
- Platform validation evidence: current-master manifest validation #41846455387 PASS; latest action validation #41845802140 passed on prior SHA `3671ab1` (no action/workflow files changed by the latest docs commit). PR #1222 has only manifest validation #41821355040 PASS; it remains blocked by missing child-process UID/GID forwarding, direct Docker/Kubernetes mutation paths, and missing reproducible TS/test/YAML/ShellCheck/lockfile coverage.
- Native schedule evidence: recovery schedule #41852388418 SUCCESS at 21:55 ICT. It dispatched reconcile #41852418866 with `ref=master`, source SHA `74782e9034e41d613e60e8ef72dcdded6d5aa164`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. Reconcile preflight succeeded, no manifest drift was found and apply was skipped. Auth/TCE/Media/MicroFE lanes passed; Stock health failed because two Admin Pods and the new Backend Pod cannot pull `12d63b4` (no ARM64 manifest); Keycloak was skipped. Reconciliation is not healthy.
- Watchdog #41852468753 FAILED because the last native scheduled inspection #41809725184 was 310m old and native scheduled reconciliation was 448m old. Post-reconcile recovery #41852743849 SUCCESS; it did not dispatch inspection because the latest all-event inspection #41845846869 was only 40m old. Recovery after watchdog #41852517166 was SKIPPED by the first-attempt/source-event guard; workflow_run/rerun is not native schedule evidence.
- Platform cron declarations remain inspect `2,32 * * * *`, reconcile `7,22,37,52 * * * *`, recovery `10,25,40,55 * * * *`, watchdog `12,27,42,57 * * * *`. Preserve them; only the recovery native schedule has recent evidence in the inspected run window.
- Latest K3s read-only snapshot #41845846869 generated 21:16:14 ICT: node Ready/ARM64, K3s v1.36.3+k3s1, disk 55%, ~19 GiB available; Media/MicroFE/NATS 1/1; Stock Admin/new Backend ImagePullBackOff; old Backend/legacy Frontend 1/1; TCE/Auth/Keycloak 0/0; public OIDC 503; GitOps drift clean; host restart_required=yes. Snapshot is not current enough for a present-health claim.
- TCE master `52cecd5584e6`, no PRs. Latest native WF-06 #41810552435 failed four HTTP 200 endpoint checks (503); WF-12 #41807645689 failed freshness; WF-07 #41785211971 passed. WF-02/WF-05 successes #41819221546/#41819221509 are on prior PR SHA `a1afaf1`, not current master. Preserve all cron declarations and the TCE market-scan schedule.
- StockDividend master `50ba0dfb67eb`, no PRs; CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. Paired release handoff/dispatch skipped; production Admin/Backend still use non-ARM64 `12d63b4`. Require protected Actions:read access and explicit paired digest authorization.
- Media master `e4c7d8990aaf`, no PRs; CI #41617592783 PASS; last runtime snapshot backend/frontend 1/1; no new publisher E2E.
- Authentication master `f978a3f378ee`; PR #75 ready, #76 draft. Master CI #41670642852 PASS. PR #75 head `a8e8a1d` check #40446492086 PASS; PR #76 head `f19cacb` check #41329425940 PASS. Keep both gated by Supabase integration/migration provenance.
- App repos own tests/builds/immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance, paired promotion, GitOps reconciliation, rollout and health. `reconcile-vps.yml` is sole apply authority; `inspect-vps.yml` is read-only. No direct SSH/Compose/MCP mutation authority. `locally-uncensored-private` remains retired. No production mutation or market-scan schedule change.
- Next: restore native Platform schedule delivery, obtain fresh read-only K3s evidence, then pursue Stock paired digest promotion only after authorization; keep Auth and PR #1222 gated.


## Cross-repo workflow inventory checkpoint — 2026-11-04 22:59 ICT / 15:59 UTC

- **Platform Infra master** is `d206e0cc9277ca6b7f707ff3075e13c63ca59961`. Inspection run [#41861306384](https://github.com/phanthienquoc/platform-infra/actions/runs/41861306384) completed successfully via `workflow_dispatch` at 22:46:58 ICT. Snapshot `debug/vps-latest.md` was generated at 22:47:09 ICT and merged by inspection PR [#1231](https://github.com/phanthienquoc/platform-infra/pull/1231). Exact inspection head `150d673d5647737f0aad6e57aa900c012310f032); merge SHA is the current master. Manifest validation #41861440816 passed on the inspection PR head. The dispatch is not native schedule evidence.
- **Platform native schedules:** inspect-vps latest native run [#41809725184](https://github.com/phanthienquoc/platform-infra/actions/runs/41809725184) failed at 16:45 ICT on old SHA `9f74d23`; latest successful inspection #41861306384 is manual dispatch. Native reconcile [#41860865532](https://github.com/phanthienquoc/platform-infra/actions/runs/41860865532) failed at 22:44 ICT only in the StockDividend health lane; Auth, TCE, Media and MicroFE lanes passed. Native watchdog [#41861131656](https://github.com/phanthienquoc/platform-infra/actions/runs/41861131656) failed at 22:45 ICT because inspection delivery and recovery freshness checks failed. Native recovery [#41852388418](https://github.com/phanthienquoc/platform-infra/actions/runs/41852388418) last passed at 21:55 ICT. Later workflow_dispatch/workflow_run recovery runs do not count as schedule delivery.
- **Fresh K3s evidence:** node `tce-k3s-01` Ready, ARM64, K3s `v1.36.3+k3s1`, disk 55%, available memory about 19 GiB, GitOps drift clean. Media backend/frontend, MicroFE Shell/WS and NATS are 1/1. Two Stock Admin Pods and the new Stock Backend Pod are ImagePullBackOff on tag `12d63b4` because the manifest has no ARM64 platform entry; older Stock Backend and Frontend remain 1/1. TCE frontend/service and MicroFE Auth/Keycloak are 0/0. Public OIDC probes return HTTP 503. Host `restart_required=yes`; Ubuntu/Docker/containerd upgrades remain pending. No reboot/upgrade was performed.
- **TCE Dashboard master** remains `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`; no open PRs. Latest native WF-06 #41810552435 (16:53 ICT) failed all four strict HTTP 200 checks with HTTP 503; WF-12 #41807645689 (16:27 ICT) failed freshness; WF-07 #41785211971 (13:23 ICT) passed. WF-02/WF-05 #41819221546/#41819221509 passed on PR head `a1afaf1`, not current master. Preserve all cron expressions and market-scan schedule.
- **StockDividend master** remains `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no open PRs. CI #41563856934 and immutable ARM64 publisher #41563856933 passed. The `build-and-push` job passed, but source handoff validation and paired digest dispatch were skipped. Production remains on the non-ARM64 Admin/Backend tag `12d63b4`; no promotion without protected Actions:read access and explicit paired authorization.
- **Media Generation master** remains `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no open PRs; CI #41617592783 passed. Current inspection confirms both Media workloads 1/1 and digest-pinned.
- **Authentication master** remains `f978a3f378ee22d4630909c2d182275b21ac9e9a`; PR #75 ready and #76 draft. Auth service CI #41670642852 passed; Supabase Preview skipped. Keep both PRs gated by integration target/effects and migration provenance.
- **Open Platform PRs:** #1222 (VPS MCP, draft), #544 (Keycloak activation docs, draft), #541 (Keycloak/Supabase DB preparation, draft), #539 (identity architecture decision, draft). PR #1222 remains blocked by Docker/Kubernetes mutation authority, unproven child UID/GID forwarding and missing reproducible TS/test/YAML/ShellCheck/lockfile evidence.
- **Contract gap found and addressed in this PR:** the restored tracker content did not match the structural contract in `scripts/validate-workflow-contracts.py` (required title, `Last reviewed:`, and the Repository readiness / Current actions / Current runtime blockers sections). The validator now explicitly rejects a missing/zero-byte tracker and requires all five repository identifiers inside the readiness section. The tracker is rewritten to the canonical schema and records this checkpoint.
- App repos own tests/builds/immutable GHCR publication. Platform owns manifests, shared pull credentials, provenance checks, paired digest promotion, reconciliation and rollout/health. `reconcile-vps.yml` remains the sole apply authority; `inspect-vps.yml` is read-only. `locally-uncensored-private` remains retired. No production image, manifest, credential, database, Pod, replica or host mutation occurred. TCE market-scan schedule unchanged.


# Cross-repo workflow inventory checkpoint — 2026-11-05 00:58 ICT / 17:58 UTC

## Repository state

| Repository | Master SHA | Open PRs | Latest verified evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 8d019eab1da2 | #1222, #544, #541, #539 (draft) | Native scheduled inspection #41881867627 PASS; snapshot PR #1235 merged as 8d019eab; exact-head manifest validation #41882047624 PASS. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6 | None | Native WF-06 #41880229621 FAIL (four HTTP 503 probes); native WF-12 #41877745265 FAIL; workflow_run #41880929859 PASS for delivery/heartbeat. |
| phanthienquoc/stockdividend | 50ba0dfb67eb | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS; paired handoff/dispatch SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aaf | None | CI #41617592783 PASS; latest inspection shows backend/frontend 1/1 and digest-pinned. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee | #75 ready, #76 draft | CI #41670642852 PASS; Supabase Preview SKIPPED; migration/integration gates remain. |

## Platform native schedule evidence

- inspect-vps.yml: #41881867627, event=schedule, created 17:55:54Z / 00:55:54 ICT, SUCCESS. All inspection/rebase/PR/exact-head validation steps passed. Snapshot generated 17:56:19Z / 00:56:19 ICT; PR #1235 merged as master SHA 8d019eab1da2c471c1b1014b8d376be88c0ea190. Exact-head manifest validation #41882047624 PASS.
- reconcile-vps.yml: latest native schedule #41860865532 at 15:44:26Z / 22:44:26 ICT, FAIL only in StockDividend health. Later #41881241239 at 17:52:10Z / 00:52:10 ICT is workflow_dispatch and also fails Stock health; do not count it as schedule.
- recover-stale-ops.yml: latest native schedule #41852388418 at 14:55:14Z / 21:55:14 ICT, PASS. Later repository_dispatch #41881214993 and workflow_dispatch #41881585524 succeeded but are not native schedule events.
- reconcile-schedule-watchdog.yml: latest native schedule #41861131656 at 15:45:57Z / 22:45:57 ICT, FAIL due stale inspection/recovery evidence. Workflow_run #41881772345 was skipped because its source was a manual reconciliation. No post-inspection watchdog result observed at checkpoint.

## TCE schedule and heartbeat

- Native WF-06 #41880229621 at 17:45:34Z / 00:45:34 ICT failed all four public endpoint checks (TCE web, TCE API, Auth liveness, Auth readiness): HTTP 503 instead of HTTP 200.
- Native WF-12 #41877745265 at 17:27:45Z / 00:27:45 ICT failed schedule freshness.
- WF-12 workflow_run #41880929859 at 17:50:18Z / 00:50:18 ICT succeeded both WF-06 delivery verification and authenticated heartbeat dispatch.
- Platform receiver/recovery #41881214993 (repository_dispatch) passed external TCE heartbeat payload validation and completed. This is not native Platform schedule delivery.

## K3s snapshot and production health

Snapshot debug/vps-latest.md generated 17:56:19Z / 00:56:19 ICT:
- Node tce-k3s-01: Ready, ARM64, K3s v1.36.3+k3s1; disk 56%; available memory about 19 GiB; GitOps drift clean.
- Media backend/frontend, MicroFE Shell/WS, NATS: 1/1.
- Stock Admin: two Pods 0/1 ImagePullBackOff; new Backend 0/1 ImagePullBackOff; old Backend 1/1; Frontend 1/1.
- Stock image pull error: no match for platform in manifest for Admin/Backend tag 12d63b4.
- TCE frontend/service and MicroFE Auth/Keycloak: 0/0. Do not infer health from zero replicas.
- Host restart_required=yes; Ubuntu/Docker/containerd updates remain pending. No reboot or package upgrade.

## Release and ownership gates

- Stock immutable ARM64 publisher #41563856933 succeeded, but source handoff validation and paired digest promotion dispatch remain SKIPPED. Require protected Actions:read access and explicit paired Admin/Backend authorization. Do not promote either image independently.
- Auth PR #75 is ready and #76 draft; checks passed but Supabase Preview skipped. Do not merge, run migrations, or activate Auth/Keycloak until integration effects and migration provenance are verified.
- Platform PR #1222 remains draft; it still has Docker/Kubernetes mutation paths and unproven shell UID/GID forwarding. Keep it out of production.
- reconcile-vps.yml remains the only production apply authority; inspect-vps.yml is read-only. No duplicate SSH/Compose/MCP mutation authority.
- locally-uncensored-private remains retired.
- No production image, manifest, credential, database, Pod, replica, or host mutation occurred. No cron expression changed; TCE market-scan schedule is unchanged.


# Cross-repo workflow inventory checkpoint — 2026-11-05 02:07 ICT / 19:07 UTC

## Repository state

| Repository | Master SHA | Open PRs | Latest verified evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 2d780e812003 | #1222, #544, #541, #539 (draft) | PR #1236 merged as 2d780e81; exact-head validate-manifests #41883005453 PASS. No post-merge run verified. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6 | None | Native WF-06 #41880229621 FAIL (four HTTP 503 probes); native WF-12 #41877745265 FAIL; workflow_run #41880929859 and Platform receiver #41881214993 passed heartbeat forwarding/payload validation. |
| phanthienquoc/stockdividend | 50ba0dfb67eb | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS; source handoff and paired digest dispatch SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aaf | None | CI #41617592783 PASS; latest snapshot shows backend/frontend 1/1 with digest-pinned imageIDs. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee | #75 ready; #76 draft | Service CI #41670642852 PASS; #75 #40446492086 and #76 #41329425940 PASS; Supabase Preview SKIPPED. |

## Platform PR #1236

- Exact head: e487eb605f172ce15cc404d7c31680f4fc603254.
- Exact-head workflow run #41883005453 (validate-manifests) completed SUCCESS. Job steps include paired image digest promotion tests, Auth digest promotion tests, rendered YAML, secret policy, immutable image policy, isolated Keycloak manifests and network boundary validation.
- PR #1236 was squash-merged with exact-head guard. Merge SHA: 2d780e812003d7190b08283b64bef60fad643eb8.
- Current master commit search confirms 2d780e812003d7190b08283b64bef60fad643eb8 as the latest Platform Infra commit at this checkpoint.
- No post-merge validation run is claimed; current combined status query returned no status contexts.

## Native schedule and TCE heartbeat evidence

- Platform inspect-vps native schedule #41881867627 at 00:55:54 ICT: SUCCESS. It completed read-only inspection, meaningful-change detection, snapshot validation, rebase, inspection PR creation, exact-head validation and squash merge. Snapshot generated at 00:56:19 ICT and was merged by PR #1235 as 8d019eab1da2c471c1b1014b8d376be88c0ea190.
- Platform native reconcile #41860865532 at 22:44:26 ICT: FAIL only at StockDividend health. Manual fallback #41881241239 at 00:52 ICT also failed Stock health but is not a native schedule run.
- Platform native recovery #41852388418 at 21:55:14 ICT: PASS. Repository-dispatch #41881214993 and workflow-dispatch #41881585524 are not native schedule events.
- Platform native watchdog #41861131656 at 22:45:57 ICT: FAIL on stale inspection/recovery evidence. Workflow_run watchdog #41881772345 was skipped because its source was manual reconciliation.
- TCE native WF-06 #41880229621 at 00:45:34 ICT: FAIL, all four public HTTP 200 probes returned 503. Native WF-12 #41877745265 at 00:27:45 ICT: FAIL freshness.
- TCE WF-12 workflow_run #41880929859 at 00:50:18 ICT: PASS for delivery verification and authenticated heartbeat dispatch. Platform receiver #41881214993 validated the payload and completed. These are not native schedule recovery and do not establish endpoint health.
- No newer native schedule run was independently verified in this checkpoint. Keep cron expressions unchanged.

## K3s snapshot and release blockers

Snapshot debug/vps-latest.md generated 00:56:19 ICT:
- Node tce-k3s-01: Ready, ARM64, K3s v1.36.3+k3s1; disk 56%; available memory about 19 GiB; GitOps drift clean.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1.
- Stock Admin: two Pods 0/1 ImagePullBackOff; new Backend 0/1 ImagePullBackOff; old Backend and Frontend 1/1.
- Stock Admin/Backend tag 12d63b4: no matching ARM64 manifest. Paired immutable ARM64 publisher passed, but source handoff and paired promotion dispatch remain skipped.
- TCE frontend/service and MicroFE Auth/Keycloak: 0/0; native WF-06 probes return HTTP 503. Do not infer health from zero replicas.
- Host restart_required=yes; Ubuntu, Docker and containerd upgrades pending. No reboot or package upgrade.

## Remaining gates

- Stock: obtain protected STOCKDIVIDEND_ACTIONS_READ_TOKEN with Actions:read on the private Stock repo and explicit paired Admin/Backend authorization; then use only Platform GitOps promotion.
- TCE: resolve service availability while preserving strict HTTP 200; do not change market-scan schedule.
- Auth: keep #75/#76 gated on Supabase production integration effects and authoritative migration provenance.
- Platform #1222 remains draft: current diff still contains docker_restart and k8s_rollout_restart mutation tools; it has not been shown to satisfy the GitOps-only/UID-GID isolation contract or reproducible build/test/lockfile checks.
- Host maintenance requires an approved maintenance window.
- reconcile-vps.yml remains sole production apply authority; inspect-vps.yml is read-only. App repos own build/test/immutable GHCR publication; Platform owns manifests, shared pull credentials, provenance, paired promotion, reconciliation, rollout and health.
- locally-uncensored-private remains retired. No production image, manifest, credential, database, Pod, replica or host mutation occurred. TCE market-scan schedule unchanged.


# Cross-repo workflow inventory checkpoint — 2026-11-05 02:56 ICT / 19:56 UTC

## Repository state

| Repository | Master SHA | Open PRs | Latest verified evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 53e7acc8f58f | #1222, #544, #541, #539 (draft) | Manual inspect #41900544272 PASS; validation #41900666915 PASS on inspection branch. Current master commit has no check-runs. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6 | None | Native WF-07 #41900042968 PASS; WF-12 workflow_run #41900072829 FAIL delivery verification, heartbeat job PASS; native WF-06 #41880229621 FAIL four HTTP 503 probes. |
| phanthienquoc/stockdividend | 50ba0dfb67eb | None | CI #41563856934 PASS; immutable publisher #41563856933 PASS; source handoff and paired digest dispatch SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aaf | None | CI #41617592783 PASS; latest inspection shows backend/frontend 1/1 with digest-pinned imageIDs. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee | #75 ready; #76 draft | CI #41670642852 PASS; #75/#76 exact-head validate PASS; Supabase Preview skipped. |

## Platform run and inspection evidence

- Latest master commit is inspection PR #1238 merge SHA `53e7acc8f58f519959c22b0a036140604b210995`; it only updates `debug/vps-latest.md`.
- Inspection #41900544272 completed SUCCESS at 02:48:43 ICT with event=workflow_dispatch. All inspection steps passed: inspect, meaningful-change detection, snapshot validation, rebase, PR creation, exact-head validation and squash merge.
- Validation #41900666915 completed SUCCESS on inspection branch `automation/vps-inspection-41900544272-1`, SHA `5284126dc6680f24314466a374e95c32b38b9d62`.
- The latest master commit has zero check-runs. The previous master validation #41894268626 passed on 101a97d5; do not represent it as validation of 53e7acc8.
- Manual reconcile #41900128585 at 02:46:08 ICT failed only in StockDividend health; Auth, TCE, Media and MicroFE lanes passed, Keycloak skipped. This was workflow_dispatch, not native schedule.
- Manual recovery #41900480191 at 02:48:19 ICT succeeded but is not native schedule evidence.

## Native Platform schedule evidence

- inspect-vps.yml: #41881867627, event=schedule, 00:55:54 ICT, SUCCESS. Latest later inspection #41900544272 was manual workflow_dispatch.
- reconcile-vps.yml: #41860865532, event=schedule, 22:44:26 ICT, FAIL only in StockDividend health. Later #41900128585 was manual and also failed Stock health.
- recover-stale-ops.yml: #41852388418, event=schedule, 21:55:14 ICT, PASS. Later #41900480191 was manual.
- reconcile-schedule-watchdog.yml: #41861131656, event=schedule, 22:45:57 ICT, FAIL due stale inspection/recovery evidence. Latest workflow_run #41900169516 skipped; no later native schedule evidence verified.

## TCE schedule and heartbeat

- WF-07 #41900042968, event=schedule, 02:45:37 ICT: SUCCESS; Binance private API check passed and third-party order integration was skipped.
- WF-12 #41900072829, event=workflow_run, 02:45:48 ICT: overall FAIL because WF-06 delivery verification failed; authenticated heartbeat notification job succeeded.
- Native WF-06 #41880229621, 00:45:34 ICT: four public endpoint jobs failed with HTTP 503.
- Native WF-12 #41877745265, 00:27:45 ICT: FAIL on freshness.
- Heartbeat forwarding is not evidence of service health or Platform native schedule recovery.

## K3s snapshot — 2026-11-05 02:48:52 ICT

- Node `tce-k3s-01`: Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56%, available RAM about 19 GiB.
- Media backend/frontend, MicroFE Shell/WS, NATS: 1/1. Media images have digest-pinned imageIDs.
- Stock Admin: two Pods 0/1 ImagePullBackOff; new Backend 0/1 ImagePullBackOff; old Backend and Frontend 1/1.
- Stock Admin/Backend tag `12d63b4`: no matching ARM64 platform manifest; failed Pods have no resolved imageID.
- TCE frontend/service and MicroFE Auth/Keycloak: 0/0. Public OIDC probes return HTTP 503.
- Host `restart_required=yes`; Ubuntu/Docker/containerd updates pending, including Docker 29.9.3 and containerd 2.4.2. No reboot or package upgrade.

## Release gates and ownership

- Stock immutable ARM64 publisher #41563856933 passed, but Platform handoff validation and paired digest dispatch were skipped. Require protected Actions:read access and explicit paired Admin/Backend authorization; promote only through Platform GitOps.
- Auth PR #75 ready and #76 draft. Exact-head validation passed, Supabase Preview skipped. Do not merge/run migrations/activate until integration target and migration provenance are verified.
- Platform PR #1222 remains draft. Current patch includes Docker restart and Kubernetes rollout-restart mutation paths, literal `\\n` sequences in TypeScript/installer content, and a `run()` helper that accepts uid/gid but does not forward them to `execFileAsync`. No reproducible lockfile/build/test/ShellCheck evidence. Do not deploy.
- PRs #544/#541/#539 remain drafts and are not production authorization.
- `reconcile-vps.yml` is sole production apply authority; `inspect-vps.yml` is read-only. App repos own tests/build/immutable GHCR; Platform owns manifests, pull credentials, provenance, paired promotion, reconciliation, rollout and health.
- `locally-uncensored-private` remains retired. No production image, manifest, credential, database, Pod, replica or host mutation occurred. No cron changed; TCE market-scan schedule unchanged.

## Next actions

1. Re-establish native inspect/reconcile/recovery/watchdog delivery; do not count dispatch or workflow_run as schedule evidence.
2. Obtain protected Stock Actions:read access and paired release authorization.
3. Resolve TCE 0/0 / HTTP 503 while preserving strict HTTP 200 assertions.
4. Verify Supabase integration/migration provenance before Auth merge or activation.
5. Obtain maintenance window before host upgrades/reboot.


## Cross-repo workflow inventory checkpoint — 2026-11-05 04:03 ICT / 2026-11-04 21:03 UTC

# Cross-repo workflow inventory checkpoint — 2026-11-05 04:03 ICT / 2026-11-04 21:03 UTC

- **Repository heads/open PRs:** Platform Infra master `fbe997ab3c90799f987d78701fd201fee401c247`; open PRs #1222, #544, #541, #539 (all draft). TCE Dashboard master `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`, no PRs. StockDividend master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`, no PRs. Media Generation master `e4c7d8990aafc7d837e918c9caf39722d623de7c`, no PRs. Authentication master `f978a3f378ee22d4630909c2d182275b21ac9e9a`, PR #75 ready and #76 draft.
- **Platform CI:** current master `validate-manifests` #41902468271 passed on exact SHA `fbe997ab3c90799f987d78701fd201fee401c247` at 03:00 ICT. Latest native schedule events remain inspect #41881867627 (00:55 ICT, PASS), reconcile #41860865532 (22:44 ICT, FAIL Stock lane), watchdog #41861131656 (22:45 ICT, FAIL freshness), recovery #41852388418 (21:55 ICT, PASS). Actions schedule-event history contains no newer native Platform tick through 04:03 ICT. Later manual inspection #41900544272 and manual reconcile #41900128585 are not native schedule evidence.
- **TCE:** native WF-07 #41900042968 at 02:45 ICT PASS (private API check passed; third-party order integration skipped). Native WF-06 #41880229621 at 00:45 ICT failed all four HTTP 200 public probes with 503. Native WF-12 #41877745265 at 00:27 ICT failed WF-06 freshness. WF-12 workflow_run #41900072829 at 02:45 ICT failed delivery verification while authenticated Platform heartbeat notification passed; workflow_run is not a native schedule tick. No newer TCE native schedule event was present through 04:03 ICT. TCE cron and market-scan schedule unchanged.
- **StockDividend publication:** CI #41563856934 and immutable publisher #41563856933 passed on master SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. Publisher logs verified linux/arm64 full-source-SHA images: Scraper `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`; Admin `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`; Backend `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. Crucial correction: the publisher's "Gate production GitOps promotion" job explicitly logs that production promotion is disabled. Source handoff validation and paired digest dispatch were skipped by design; this is not merely an unconfigured Actions:read token. Production remains on Admin/Backend tag `12d63b4`, which has no ARM64 manifest. Do not promote without explicit release authorization.
- **Media:** master CI #41617592783 PASS. Snapshot #41900544272 (manual workflow_dispatch, 02:48 ICT) shows Media backend/frontend 1/1 and digest-pinned; no newer Media publisher run observed.
- **Authentication:** master service CI #41670642852 PASS; Supabase Preview SKIPPED. PR #75 head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` validation #40446492086 PASS; PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` validation #41329425940 PASS. Production integration/migration gate remains closed.
- **K3s snapshot:** `debug/vps-latest.md` from inspection #41900544272 generated 02:48:52 ICT, approximately 74 minutes old at checkpoint. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, about 19 GiB RAM available. Media, MicroFE Shell/WS and NATS 1/1; two Stock Admin Pods and new Backend Pod ImagePullBackOff; old Backend and Frontend 1/1; TCE/Auth/Keycloak 0/0. Host `restart_required=yes`; no reboot or upgrade.
- **MCP PR #1222:** current draft diff still includes Docker restart and Kubernetes Deployment patch/restart, literal backslash-n source/installer defects, and no demonstrated SHELL_UID/GID forwarding to the child process. Build/tests/YAML/ShellCheck/lockfile remain absent. Keep draft; no deployment.
- App repos own tests/builds/immutable GHCR; Platform owns production manifests, shared pull credentials, provenance, paired promotion, GitOps reconciliation, rollout and health. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` read-only. Preserve useful CI/security/manual/release/scheduled workflows. No direct SSH/Compose/MCP mutation authority. `locally-uncensored-private` remains retired.
- No production image/manifest/credential/database/Pod/replica/host mutation or cron change occurred. TCE market-scan schedule unchanged.

Evidence:
- Platform master validation: https://github.com/phanthienquoc/platform-infra/actions/runs/41902468271
- Platform native inspect: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Platform native reconcile: https://github.com/phanthienquoc/platform-infra/actions/runs/41860865532
- Platform native watchdog: https://github.com/phanthienquoc/platform-infra/actions/runs/41861131656
- Platform native recovery: https://github.com/phanthienquoc/platform-infra/actions/runs/41852388418
- K3s inspection: https://github.com/phanthienquoc/platform-infra/actions/runs/41900544272
- TCE WF-07: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE WF-06: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE WF-12: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- TCE heartbeat verification: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900072829
- Stock publisher: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Stock CI: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Media CI: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


## Cross-repo workflow inventory checkpoint — 2026-11-05 05:02 ICT / 2026-11-04 22:02 UTC

# Cross-repo workflow inventory checkpoint — 2026-11-05 05:02 ICT / 2026-11-04 22:02 UTC

- Platform Infra master: 58cb64461beaf70f96fac0a3e4f5559b9efdb0b3; open PRs #1222, #544, #541, #539 (all draft). TCE master 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; Stock master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media master e4c7d8990aafc7d837e918c9caf39722d623de7c; Authentication master f978a3f378ee22d4630909c2d182275b21ac9e9a with PR #75 ready and #76 draft.
- Platform native schedule events: inspect #41881867627 (00:55 ICT PASS, now stale); reconcile #41917440202 (04:35 ICT FAIL in Stock health); recovery #41914511298 (04:16 ICT PASS); watchdog #41918315745 (04:40 ICT FAIL because inspect age was 224 minutes).
- Recovery bug: watchdog-triggered recovery #41918357799 succeeded but queried all inspect-vps events, so it treated manual workflow_dispatch #41914913277 at 04:18 ICT as native schedule activity and skipped fallback. The current branch fix/recovery-native-inspection-evidence-20261105-0502-ict separates event=schedule evidence from workflow_dispatch fallback activity. Manual fallback will never satisfy native schedule freshness; duplicate fallbacks are suppressed.
- TCE: native WF-07 #41900042968 PASS at 02:45 ICT; WF-06 #41880229621 FAIL with four HTTP 503 probes; WF-12 #41877745265 FAIL on freshness; workflow_run #41900072829 FAIL on delivery verification although heartbeat notification passed.
- Stock: CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. Verified Scraper digest sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2, Admin sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e, Backend sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a. Production promotion explicitly disabled; handoff and paired dispatch SKIPPED.
- Media CI #41617592783 PASS; snapshot #1241 backend/frontend 1/1 and digest-pinned.
- Auth CI #41670642852 PASS; PR #75 exact-head #40446492086 PASS; PR #76 exact-head #41329425940 PASS; Supabase Preview SKIPPED.
- K3s snapshot generated 04:19:01 ICT by workflow_dispatch inspection #41914913277 and merged by PR #1241. At 05:02 ICT age about 43 minutes. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, about 19 GiB RAM available. Media, MicroFE Shell/WS and NATS 1/1. Two Stock Admin Pods and new Backend Pod ImagePullBackOff; old Backend/Frontend 1/1. TCE frontend/service and Auth/Keycloak 0/0. Host restart_required=yes.
- MCP PR #1222 remains draft: direct Docker/Kubernetes mutation, malformed literal backslash-n source/installer, missing SHELL_UID/GID forwarding and no reproducible lockfile/build/test/ShellCheck evidence.
- App repos own tests/build/immutable GHCR. Platform owns manifests, shared pull credentials, provenance, paired promotion, reconciliation, rollout and health. reconcile-vps.yml sole apply authority; inspect-vps.yml read-only. No direct SSH/Compose/MCP mutation authority. locally-uncensored-private remains retired.
- No production image/manifest/credential/database/Pod/replica/host mutation or cron change occurred. TCE market-scan schedule unchanged.

Evidence:
- Platform native inspect #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Platform native reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Platform watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- Platform recovery #41918357799: https://github.com/phanthienquoc/platform-infra/actions/runs/41918357799
- Platform native recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- Platform manual inspection #41914913277: https://github.com/phanthienquoc/platform-infra/actions/runs/41914913277
- Snapshot PR #1241: https://github.com/phanthienquoc/platform-infra/pull/1241
- TCE WF-07 #41900042968: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


## Cross-repo workflow inventory checkpoint — 2026-11-05 05:14 ICT / 2026-11-04 22:14 UTC

# Cross-repo workflow inventory checkpoint — 2026-11-05 05:14 ICT / 2026-11-04 22:14 UTC

- Platform Infra master: fe243a7ecc652a720a813f93e669474bb858c848. PR #1242 merged. Exact-head validate-github-actions #41923196096 PASS; exact-head validate-manifests #41923196112 PASS; post-merge validate-github-actions #41923323345 PASS; post-merge validate-manifests #41923323244 PASS. Open Platform PRs remain #1222, #544, #541, #539 (all draft).
- PR #1242 fixes the recovery controller's inspection event classification. Before the fix, watchdog #41918315745 correctly failed because native inspect #41881867627 was 224 minutes old, but recovery #41918357799 queried all inspect events and treated manual workflow_dispatch #41914913277 as recent, skipping the fallback. The merged workflow now queries event=schedule and event=workflow_dispatch separately, suppresses duplicate read-only fallbacks, and explicitly preserves native schedule failure until a native schedule event arrives.
- No post-merge native schedule delivery has yet been observed. PR push validations #41923323345/#41923323244 are not cron evidence. Latest native Platform runs remain inspect #41881867627 (00:55 ICT, PASS but stale), reconcile #41917440202 (04:35 ICT, FAIL Stock health), recovery #41914511298 (04:16 ICT, PASS), watchdog #41918315745 (04:40 ICT, FAIL inspection freshness).
- TCE master 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; no PRs. Native WF-07 #41900042968 PASS at 02:45 ICT. Native WF-06 #41880229621 FAIL with four HTTP 503 probes. Native WF-12 #41877745265 FAIL on freshness; workflow_run #41900072829 also FAIL on delivery verification, although authenticated heartbeat notification passed.
- StockDividend master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; no PRs. CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. Production promotion explicitly disabled by release gate; handoff validation and paired Admin/Backend digest dispatch SKIPPED. Existing production tag 12d63b4 has no ARM64 manifest.
- Media Generation master e4c7d8990aafc7d837e918c9caf39722d623de7c; no PRs. CI #41617592783 PASS; latest snapshot shows backend/frontend 1/1 with digest-pinned images.
- Authentication master f978a3f378ee22d4630909c2d182275b21ac9e9a; PR #75 ready, #76 draft. CI #41670642852 PASS; PR #75 exact-head #40446492086 PASS; PR #76 exact-head #41329425940 PASS. Supabase Preview SKIPPED; migration/production gate remains closed.
- K3s snapshot #1241 generated 04:19:01 ICT by workflow_dispatch inspection #41914913277; about 55 minutes old at this checkpoint. Node tce-k3s-01 Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, about 19 GiB RAM available. Media backend/frontend, MicroFE Shell/WS and NATS 1/1. Two Stock Admin Pods and new Backend Pod ImagePullBackOff; old Backend and Frontend 1/1. TCE frontend/service and Auth/Keycloak 0/0. Host restart_required=yes.
- MCP PR #1222 remains draft: Docker/Kubernetes mutation authority, malformed literal backslash-n source/installer, missing SHELL_UID/GID forwarding and no reproducible build/test/ShellCheck/lockfile evidence.
- App repos own tests/build/immutable GHCR. Platform owns production manifests, shared pull credentials, provenance, paired promotion, reconciliation, rollout and health. reconcile-vps.yml sole apply authority; inspect-vps.yml read-only. No direct SSH/Compose/MCP mutation authority. locally-uncensored-private remains retired.
- No production image/manifest/credential/database/Pod/replica/host mutation or cron change occurred. TCE market-scan schedule unchanged.

Evidence:
- PR #1242: https://github.com/phanthienquoc/platform-infra/pull/1242
- Exact-head validate-github-actions #41923196096: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196096
- Exact-head validate-manifests #41923196112: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196112
- Post-merge validate-github-actions #41923323345: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323345
- Post-merge validate-manifests #41923323244: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323244
- Native inspection #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Native reconciliation #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Native watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- Watchdog-triggered recovery #41918357799: https://github.com/phanthienquoc/platform-infra/actions/runs/41918357799
- Manual inspection fallback #41914913277: https://github.com/phanthienquoc/platform-infra/actions/runs/41914913277
- Snapshot PR #1241: https://github.com/phanthienquoc/platform-infra/pull/1241
- TCE WF-07 #41900042968: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo workflow inventory checkpoint — 2026-11-05 06:01 ICT / 2026-11-04 23:01 UTC

- Platform Infra master: cfdce04a1d78fc2dcc9c1494628ff8791126ca20. Inspection run #41929001497 completed successfully; all inspect job steps passed. It created PR #1244 and merged exact PR head 6d642d020462566b1ad0cc0b8ecf79b30fc6199f as cfdce04. The connected run/job response did not expose the workflow event type; do not count this as native schedule evidence.
- Platform open PRs: #1222, #544, #541, #539 (all draft). Last returned validate-manifests runs: #41821355040, #38575430454, #38567431761, #38548718033 respectively, all successful but historical. #1222 remains blocked by Docker/Kubernetes mutation authority, previously observed literal backslash-n source/installer defects, missing SHELL_UID/GID forwarding and absent reproducible build/test/lockfile evidence.
- TCE Dashboard master: 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; no open PRs. Last verified native WF-07 #41900042968 PASS at 02:45 ICT; WF-06 #41880229621 FAIL with four HTTP 503 endpoints; WF-12 #41877745265 FAIL on freshness. Workflow_run #41900072829 failed delivery verification although its authenticated Platform heartbeat notification passed. No newer run list was exposed in this inspection.
- StockDividend master: 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; no open PRs. CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. The publisher explicitly disables production GitOps promotion; handoff validation and paired Admin/Backend dispatch are SKIPPED. Production tags 12d63b4 for Admin/Backend still have no ARM64 manifest. Do not enable promotion without explicit release authorization and protected STOCKDIVIDEND_ACTIONS_READ_TOKEN.
- Media Generation master: e4c7d8990aafc7d837e918c9caf39722d623de7c; no open PRs. CI #41617592783 PASS. Latest inspection shows backend/frontend 1/1 with digest-pinned imageIDs.
- Authentication master: f978a3f378ee22d4630909c2d182275b21ac9e9a; PR #75 ready (head a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05), PR #76 draft (head f19cacb0bf2b454b3152bd3a501f6f88d0a14a58). Auth CI #41670642852 PASS; last documented exact-head validation refs are #40446492086 and #41329425940. The connected workflow-run lookup returned no run records for current Auth PR heads. Supabase Preview remains SKIPPED; migration branch remains MIGRATIONS_FAILED and production integration target/effect is not verified.
- K3s snapshot debug/vps-latest.md generated 2026-11-04T22:52:28Z (05:52:28 ICT), merged by PR #1244. At 06:01 ICT it is about 9 minutes old. Node tce-k3s-01 Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available memory about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS 1/1. Two Stock Admin Pods and new Stock Backend Pod ImagePullBackOff; old Backend/Frontend 1/1. TCE frontend/service and MicroFE Auth/Keycloak 0/0. Public Keycloak OIDC probes HTTP 503. Host restart_required=yes; Docker 29.1.3 and containerd 2.3.2-k3s2 installed; containerd 2.4.2 and Docker 29.9.3 pending. No reboot/upgrade.
- Native Platform evidence still positively verified: inspect #41881867627 at 00:55 ICT PASS but stale; reconcile #41917440202 at 04:35 ICT FAIL in Stock health; recovery #41914511298 at 04:16 ICT PASS; watchdog #41918315745 at 04:40 ICT FAIL because native inspection freshness exceeded 75 minutes. Inspection #41929001497 is successful but event type is not surfaced; do not count it as native schedule.
- PR #1242 recovery event-classification fix is merged. Exact-head #41923196096/#41923196112 and post-merge #41923323345/#41923323244 all PASS. A post-merge native event=schedule cycle is still required to prove the fix in production.
- Credential contract: GHCR_READ_TOKEN is package read:packages only with GHCR_USERNAME. STOCKDIVIDEND_ACTIONS_READ_TOKEN is protected production Environment Actions:read only. TCE and Stock use separate PLATFORM_INFRA_TOKEN values (TCE Contents:write + Actions:read; Stock Contents:write). Media and Auth use separate PLATFORM_INFRA_DISPATCH_TOKEN values (Media Contents:write + Actions:read; Auth Contents:write). Active GitOps promotion uses workflow-scoped GITHUB_TOKEN; PLATFORM_INFRA_AUTOMATION_TOKEN is obsolete and must not be reintroduced.
- App repos own tests/build/immutable GHCR publication. Platform Infra owns production manifests, shared pull credentials, provenance, paired promotion, reconciliation, rollout and health. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml is read-only. No direct SSH/Compose/MCP mutation authority. locally-uncensored-private remains retired.
- No production image/manifest/credential/database/Pod/replica/host mutation or cron change occurred. TCE market-scan schedule unchanged.

Evidence:
- Inspection run #41929001497: https://github.com/phanthienquoc/platform-infra/actions/runs/41929001497
- Inspection PR #1244: https://github.com/phanthienquoc/platform-infra/pull/1244
- K3s snapshot: https://github.com/phanthienquoc/platform-infra/blob/master/debug/vps-latest.md
- Recovery fix PR #1242: https://github.com/phanthienquoc/platform-infra/pull/1242
- Exact-head validate-github-actions #41923196096: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196096
- Exact-head validate-manifests #41923196112: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196112
- Post-merge validate-github-actions #41923323345: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323345
- Post-merge validate-manifests #41923323244: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323244
- Native inspect #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Native reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Native recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- Native watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- TCE WF-07 #41900042968: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- TCE heartbeat verification #41900072829: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900072829
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo workflow inventory checkpoint — 2026-11-05 07:01 ICT / 2026-11-05 00:01 UTC

- **Repository heads/open PRs:** Platform Infra master 8170761b5d9cc98bfeec291294ef9e1f4c21bac2; open PRs #1222/#544/#541/#539 (all draft). PR #1247 merged after exact-head checks. TCE Dashboard master 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d, no open PRs. StockDividend master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec, no open PRs. Media Generation master e4c7d8990aafc7d837e918c9caf39722d623de7c, no open PRs. Authentication master f978a3f378ee22d4630909c2d182275b21ac9e9a, PR #75 ready and #76 draft.
- **Platform PR #1247:** Branch test/watchdog-native-recovery-event-contract-20261105-0658-ict, exact head 81c4d9250c413171494f51e75111c243ad857d73. Added a validator regression guard requiring the watchdog recovery-history query to filter event=schedule and branch=master, rejecting workflow_run/workflow_dispatch filters. Exact-head lint #41938079392 PASS; exact-head validate #41938079362 PASS. Squash merge SHA 8170761b5d9cc98bfeec291294ef9e1f4c21bac2. Post-merge push validations #41938159895 and #41938159872 were queued at checkpoint.
- **Native Platform inspection:** #41934713847 ran with event=schedule at 2026-11-04T23:33:56Z (06:33:56 ICT), conclusion success. It generated the read-only snapshot at 23:34:04Z and created inspection PR #1246, merged as 3bc0921c4e1e753356c1930a26cd0cf0ab3a9e2d. This confirms inspect-vps native schedule delivery resumed.
- **Native Platform reconciliation:** latest verified native schedule remains #41917440202 at 21:35:01Z (04:35:01 ICT), failed in StockDividend health. Manual reconciliation #41932100148 at 23:14:18Z (06:14:18 ICT) also failed only in StockDividend workload health; its shared reconcile job and Auth/TCE/Media/MicroFE lanes succeeded or skipped safely, and the Stock lane failed on Admin/new Backend ImagePullBackOff. The manual run is not native schedule evidence.
- **Native Platform recovery/watchdog:** latest native recovery remains #41914511298 at 21:16:19Z (04:16:19 ICT), success but stale. Watchdog #41934894419 at 23:35:15Z (06:35:15 ICT), event=workflow_run, failed because the latest native recovery was 138 minutes old, beyond MAX_RECOVERY_AGE_MINUTES=45. Recovery workflow_run #41934894417 at 06:35:15 ICT succeeded after fresh native inspection #41934713847, but is not native schedule evidence and does not clear the recovery cron blocker. Latest native watchdog remains #41918315745 at 21:40:44Z (04:40:44 ICT), failure.
- **Latest Platform K3s snapshot:** debug/vps-latest.md generated 2026-11-04T23:34:04Z (06:34:04 ICT), about 27 minutes old at checkpoint. Node tce-k3s-01 Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, available RAM about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS 1/1. Two Stock Admin Pods and new Stock Backend Pod ImagePullBackOff; old Backend and Frontend 1/1. TCE frontend/service and MicroFE Auth/Keycloak 0/0. Public Keycloak OIDC probes HTTP 503. Host restart_required=yes; Docker 29.1.3 and containerd 2.3.2-k3s2 installed, pending containerd 2.4.2 and Docker 29.9.3; no upgrade/reboot.
- **TCE schedules:** Native WF-07 Backup #41936628258 at 23:48:44Z (06:48:44 ICT) PASS. This is distinct from WF-07 third-party integration check #41900042968 (02:45:37 ICT, PASS). Native WF-06 #41932031987 at 23:13:49Z (06:13:49 ICT) failed all four public probes: TCE API, TCE web, Auth liveness and Auth readiness returned HTTP 503 instead of HTTP 200. Native WF-12 #41928632194 at 22:49:42Z (05:49:42 ICT) failed delivery/freshness; workflow_run #41932063303 at 23:14:02Z (06:14:02 ICT) passed WF-06 delivery verification and authenticated Platform heartbeat forwarding but is not native schedule evidence. TCE cron expressions and market-scan schedule unchanged.
- **StockDividend:** master CI #41563856934 PASS; immutable publisher #41563856933 PASS and verified ARM64 digests remain in tracker. Publisher logs production GitOps promotion disabled; handoff and paired Admin/Backend digest dispatch SKIPPED. Production tags 12d63b4 for Admin/Backend still have no ARM64 manifest. Do not promote without explicit release authorization and protected Actions:read credential.
- **Media:** CI #41617592783 PASS; latest snapshot shows backend/frontend 1/1 with digest-pinned imageIDs.
- **Authentication:** master CI #41670642852 PASS; #75/#76 exact-head validation evidence is historical; Supabase Preview remains SKIPPED, so migration provenance/production integration gate remains closed.
- **MCP PR #1222:** still draft; retains Docker/Kubernetes mutation authority, previously observed malformed newline defects and missing SHELL_UID/GID forwarding; no reproducible build/test/lockfile/ShellCheck evidence. Do not deploy.
- **Ownership/safety:** app repositories own tests/builds/immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, provenance, paired digest promotion, GitOps reconciliation, rollout and health. reconcile-vps.yml remains sole production apply authority; inspect-vps.yml is read-only. No direct SSH/Compose/MCP mutation authority. locally-uncensored-private remains retired.
- **No production mutation:** no production image/manifest/credential/database/Pod/replica/host mutation or cron change occurred. TCE market-scan schedule unchanged.

Evidence:
- PR #1247: https://github.com/phanthienquoc/platform-infra/pull/1247
- PR #1247 exact-head lint #41938079392: https://github.com/phanthienquoc/platform-infra/actions/runs/41938079392
- PR #1247 exact-head validate #41938079362: https://github.com/phanthienquoc/platform-infra/actions/runs/41938079362
- PR #1247 post-merge validate-github-actions #41938159895: https://github.com/phanthienquoc/platform-infra/actions/runs/41938159895
- PR #1247 post-merge validate-manifests #41938159872: https://github.com/phanthienquoc/platform-infra/actions/runs/41938159872
- Native inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Inspection PR #1246: https://github.com/phanthienquoc/platform-infra/pull/1246
- Watchdog failure #41934894419: https://github.com/phanthienquoc/platform-infra/actions/runs/41934894419
- Workflow_run recovery #41934894417: https://github.com/phanthienquoc/platform-infra/actions/runs/41934894417
- Native reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Manual reconcile #41932100148: https://github.com/phanthienquoc/platform-infra/actions/runs/41932100148
- Native TCE WF-06 #41932031987: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987
- Native TCE WF-12 #41928632194: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194
- Native TCE WF-07 Backup #41936628258: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


## Workflow inventory runtime checkpoint — 2026-11-05 07:56 ICT

Repository master refs and open PRs were re-read directly. Platform Infra `420ff3091867b35772472a1ab54efd74d9e5c255` has draft PRs #1222/#544/#541/#539; TCE Dashboard `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`, StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`, and Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c` have no open PRs; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a` has #75 ready and #76 draft.

- Platform latest master validation: #41938463049 push, SUCCESS. Native schedule history: inspect #41934713847 (06:33:56 ICT, SUCCESS); reconcile #41917440202 (04:35:01 ICT, FAILURE in Stock health); recovery #41914511298 (04:16:19 ICT, SUCCESS but stale); watchdog #41918315745 (04:40:44 ICT, FAILURE). No newer Platform event=schedule runs were present at 07:56 ICT. Workflow_run recovery #41934894417 is fallback evidence only.
- TCE latest schedule history: WF-07 Backup #41936628258 (06:48:44 ICT, SUCCESS); WF-06 #41932031987 (06:13:49 ICT, FAILURE, all four HTTP 503); WF-12 #41928632194 (05:49:42 ICT, FAILURE). Workflow_run #41932063303 forwarded heartbeat successfully but is not native schedule evidence. No newer TCE schedule runs were present at 07:56 ICT. TCE market-scan cron unchanged.
- Stock CI #41563856934 and publisher #41563856933 succeeded on 2026-11-03. Publisher's production GitOps gate is disabled; paired digest handoff and dispatch are skipped. Immutable ARM64 digests are published but no production authorization is inferred.
- Media CI #41617592783 and Auth CI #41670642852 succeeded on 2026-11-03. Auth PR #75/#76 validation passed on their exact heads, but Supabase Preview was skipped for both.
- Latest committed K3s snapshot generated 06:34:04 ICT is 82 minutes old. Node was Ready/ARM64, disk 56%, available RAM ~19 GiB. Media/MicroFE/NATS 1/1; Stock Admin two Pods and current Backend 0/1 ImagePullBackOff on tag 12d63b4; previous Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart_required=yes. Treat as stale point-in-time evidence.
- Reconcile #41917440202 shared preflight/GHCR credential operations succeeded with ALLOW_IMAGE_CHANGES=false. Permanent Stock architecture mismatch was correctly classified and rollout restarts skipped; Stock health gate failed.
- Exact-head PR checks inspected: Platform #1222 validate PASS (2026-11-04); #544/#541/#539 validate PASS but historical. Auth #75/#76 validate PASS, Supabase Preview SKIPPED.
- Preserve single apply authority, immutable digest promotion and paired Stock Admin/Backend gate. No production mutation, secret/database changes, host reboot, Pod/replica change or cron edit. No TCE market-scan schedule change.


## Workflow inventory runtime checkpoint — 2026-11-05 09:00 ICT / 02:00 UTC

- Platform Infra master is `76dad0be9a3aab4130dbd25b7c2c00deb8e24d9e`, created by inspection PR #1251 after manual read-only inspection #41949431808. Exact snapshot-head validation #41949516885 passed; PR #1251 merged as the current master commit. Open Platform PRs #1222/#544/#541/#539 remain draft.
- TCE master `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`, no open PRs. Stock master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`, no open PRs. Media master `e4c7d8990aafc7d837e918c9caf39722d623de7c`, no open PRs. Authentication master `f978a3f378ee22d4630909c2d182275b21ac9e9a`, PR #75 ready and #76 draft.
- Native Platform schedule events: inspect #41934713847 (06:33:56 ICT, success but stale); recovery #41949145532 (08:31:53 ICT, success); reconcile #41950932898 (08:47:55 ICT, failure in Stock health only); watchdog #41951133668 (08:49:44 ICT, failure because native inspect was 135 minutes old). The watchdog confirmed inspect-vps/reconcile-vps active and no reconciliation runner queue delay. Do not treat workflow_dispatch fallback as native schedule evidence.
- Recovery fallback #41949160533 was dispatched with `ref=master`, `mode=apply`, `allow_image_changes=false`, `target_app=all`; it did not authorize image changes. Recovery workflow_dispatch #41949390240 then ran read-only inspection #41949431808. PR #1251 merged the generated snapshot. Later recovery workflow_run #41951186498 saw the manual fallback snapshot fresh at 14 minutes but retained the native schedule stale warning.
- Native reconcile #41950932898: shared preflight/reconcile passed; no manifest drift, so manifest apply and rollout restarts were skipped. Auth runtime Secret provision/verification ran; Auth/TCE/MicroFE/Media lanes passed. Stock lane failed because Admin (two Pods) and new Backend (one Pod) still use tag `12d63b4` without an ARM64 manifest; rollout restart skipped. Final lane summary failed correctly.
- TCE native WF-07 Backup #41936628258 (06:48:44 ICT) PASS; WF-06 #41932031987 (06:13:49 ICT) FAIL with four HTTP 503 probes; WF-12 #41928632194 (05:49:42 ICT) FAIL. No later TCE schedule event was in the inspected run list. Workflow_run heartbeat #41932063303 is not native schedule evidence.
- Latest K3s snapshot generated 08:34:36 ICT is about 26 minutes old: node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, RAM available ~19 GiB. Media/MicroFE/NATS 1/1; Stock Admin two Pods and new Backend 0/1 ImagePullBackOff; old Backend/Frontend 1/1; TCE frontend/service and Auth/Keycloak 0/0; OIDC probes HTTP 503; host restart_required=yes.
- Stock publisher #41563856933 and CI #41563856934 remain the latest successful app runs (2026-11-03); promotion is explicitly disabled and paired handoff/dispatch SKIPPED. Media CI #41617592783 and Auth CI #41670642852 remain successful but historical. Auth PR #75/#76 checks are historical; Supabase Preview skipped.
- Preserve app-owned test/build/immutable GHCR publication and Platform-owned manifests/credentials/paired promotion/reconcile/rollout. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` remains read-only. No SSH/Compose/MCP mutation authority added; locally-uncensored-private remains retired.
- No manifest apply, image promotion, migration, Pod/replica change, host reboot or package upgrade was initiated by this documentation checkpoint. The scheduled reconcile did execute Auth runtime Secret provision/verification; do not claim zero production-side operations. TCE market-scan schedule unchanged.
- Exact next actions: verify next native inspect-vps event and investigate GitHub schedule delivery if still absent; retain Stock promotion gate pending explicit release authorization; retain TCE/Auth HTTP 200 and migration gates; keep #1222 draft; wait for VPS maintenance window.
- Evidence: PR #1251 https://github.com/phanthienquoc/platform-infra/pull/1251; manual inspection #41949431808 https://github.com/phanthienquoc/platform-infra/actions/runs/41949431808; exact-head validation #41949516885 https://github.com/phanthienquoc/platform-infra/actions/runs/41949516885; native recovery #41949145532 https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532; native reconcile #41950932898 https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898; native watchdog #41951133668 https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668; TCE WF-07 #41936628258 https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258; TCE WF-06 #41932031987 https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987; TCE WF-12 #41928632194 https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194; Stock publisher #41563856933 https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933; Media CI #41617592783 https://github.com/phanthienquoc/media-generation/actions/runs/41617592783; Auth CI #41670642852 https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852.


## Cross-repo runtime checkpoint — 2026-11-05 10:04 ICT / 03:04 UTC

- Platform master: 8ae797a0bd69be772a590515d73dfce0e45a820e; open PRs #1222/#544/#541/#539 (all draft). Latest manual inspection #41958436222 PASS at 09:56:44 ICT; exact snapshot validation #41958510609 PASS. Current snapshot generated 09:56:52 ICT and committed by inspection PR #1253. It is fresh at this checkpoint, not a native schedule event.
- TCE master: 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; no PR. WF-06 is confirmed active by WF-12 job log, but latest native WF-06 #41932031987 is 220m old at watchdog #41958165099; WF-12 native #41958165099 failed freshness. WF-12 heartbeat dispatch succeeded. Preserve strict HTTP 200 and do not change any cron, especially market-scan.
- StockDividend master: 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; no PR. CI #41563856934 and immutable ARM64 publisher #41563856933 pass. Promotion remains disabled; production tag 12d63b4 has no ARM64 manifest. Reconcile #41958192072 failed only Stock health with explicit no-match-for-platform evidence. No partial Admin/Backend promotion.
- Media master: e4c7d8990aafc7d837e918c9caf39722d623de7c; no PR; CI #41617592783 pass; snapshot backend/frontend 1/1 digest-pinned.
- Authentication master: f978a3f378ee22d4630909c2d182275b21ac9e9a; PR #75 ready and #76 draft. Both latest returned validation checks passed, but Supabase Preview skipped; no migration/activation.
- Native Platform schedule: inspection #41934713847 (23:33:56Z, PASS but stale); reconcile #41950932898 (01:47:55Z, FAIL Stock health); recovery #41949145532 (01:31:53Z, PASS); watchdog #41951133668 (01:49:44Z, FAIL inspection freshness). Manual inspection #41958436222 and manual recovery #41958394974 do not count as native events.
- Latest snapshot: node Ready ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, about 19 GiB RAM available; Media/MicroFE/NATS healthy; Stock Admin/new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart_required=yes.
- Preserve one production apply authority (reconcile-vps.yml), immutable app-owned GHCR publication, Platform-owned GitOps/credentials/rollout, and all useful CI/security/backup/manual/release/scheduled workflows. No production mutation or cron change. TCE market-scan schedule unchanged.


## Cross-repo workflow inventory audit correction — production-side effects of reconcile run #41958192072 (2026-11-05 10:10 ICT)

The prior 10:04 checkpoint incorrectly described the reconcile run as having no credential mutation. The run was a workflow_dispatch with mode=apply, target_app=all and ALLOW_IMAGE_CHANGES=false. Its job-step API records the following successful steps:

- Validate GHCR pull access before mutating cluster credentials.
- Provision Auth runtime Secret from the platform-infra production Environment.
- Bootstrap shared GHCR pull credentials.
- Execute the managed image-pull-blocked workload restart policy.
- Verify cluster after reconciliation.

The shared preflight reported DRIFT=false; Apply production manifests and post-apply drift verification were skipped. Therefore, this run did perform controlled production credential reconciliation (Auth runtime Secret and shared GHCR pull Secret), despite making no production manifest/image-reference change. The Stock lane still failed: Admin and new Backend remained ImagePullBackOff on tag 12d63b4 because the ARM64 manifest is absent. The run did not establish Stock recovery or a healthy overall deployment.

Do not describe this reconcile as zero production-side operations. The evidence does not show a database migration, image digest promotion, manifest apply, desired replica change or host reboot. The workflow-step summary shows the managed restart step completed, but this audit does not infer that every blocked Pod was restarted; the subsequent inspection still shows the Stock Admin/Backend failures.



## Cross-repo workflow inventory runtime checkpoint — 2026-11-05 11:04 ICT / 04:04 UTC

- **Platform Infra:** master `c0d5c5ff18472800f15b352cd950c4c3d959cd1f`; PRs #1222/#544/#541/#539 remain draft. Manual reconcile #41962132547 (10:31 ICT) performed GHCR pull credential and Auth runtime Secret reconciliation, found no manifest drift, skipped manifest apply, skipped restart for permanent Stock architecture failures, and failed the Stock health lane. Manual recovery #41962345391 (10:33 ICT) passed but reused a fresh manual inspection fallback; native inspection remains stale. Latest native schedule runs: inspect #41934713847 PASS (06:33), recovery #41949145532 PASS (08:31), reconcile #41950932898 FAIL Stock health (08:47), watchdog #41951133668 FAIL inspection freshness (08:49). No newer Platform `event=schedule` runs through 11:04 ICT.
- **TCE Dashboard:** master `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`; no PR. Native WF-06 #41962074678 ran at 10:30 ICT and failed all four public HTTP 200 probes with 503. WF-12 workflow_run #41962097006 passed and confirmed WF-06 is active and its scheduled delivery is fresh; this is not a native WF-12 schedule run. Latest native WF-12 remains #41958165099 at 09:54 ICT, failed freshness. WF-07 Backup #41936628258 PASS. Keep market-scan and all cron declarations unchanged.
- **StockDividend:** master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no PR. CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; production Admin/Backend tag `12d63b4` still has no ARM64 manifest. Paired promotion remains disabled and un-dispatched.
- **Media Generation:** master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no PR. CI #41617592783 PASS; latest live reconcile listing shows backend/frontend 1/1 with digest-pinned images.
- **Authentication:** master `f978a3f378ee22d4630909c2d182275b21ac9e9a`; #75 ready, #76 draft. Auth CI #41670642852 PASS; PR-head CI #40446492086/#41329425940 PASS historically. Supabase Preview remains SKIPPED; migration provenance and GitHub deployment binding remain unverified.
- **Latest live K3s evidence:** Platform reconcile #41962132547 at 10:32 ICT: node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff; previous Backend and Frontend 1/1. The committed inspection snapshot from 09:56:52 ICT is 68 minutes old at this checkpoint, close to the 75-minute freshness budget. Host restart_required=yes.
- Preserve app-owned test/build/immutable GHCR and Platform-owned manifests/shared credentials/promotion/reconcile/rollout. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose/MCP mutation authority. No production image promotion, manifest apply, migration, desired replica change, package upgrade or reboot was initiated by this documentation update. The earlier reconcile did perform controlled Auth runtime Secret and shared GHCR credential reconciliation; do not mislabel it as read-only. Preserve all CI/security/backup/manual/release/scheduled workflows. TCE market-scan schedule unchanged.

### Exact evidence
- Platform reconcile #41962132547: https://github.com/phanthienquoc/platform-infra/actions/runs/41962132547
- Platform recovery #41962345391: https://github.com/phanthienquoc/platform-infra/actions/runs/41962345391
- Platform native inspect/reconcile/recovery/watchdog: #41934713847 / #41950932898 / #41949145532 / #41951133668
- TCE WF-06 schedule #41962074678 and WF-12 workflow_run #41962097006
- Stock publisher #41563856933; Media CI #41617592783; Auth CI #41670642852


## Cross-repo workflow inventory runtime checkpoint — 2026-11-05 11:58 ICT / 04:58 UTC

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


# Cross-repo deployment checkpoint — 2026-11-05 13:03 ICT / 06:03 UTC

## Repository heads and open PRs

| Repository | Current master | Open PRs | Latest verified repository evidence |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `837944e2b3e6416f3e8f7a8107e1e2bea2d07fe3` | #1222, #544, #541, #539 (all draft) | PR #1257 merged at 05:03:37Z. Exact-head `validate-manifests` #41971521055 PASS; post-merge #41971589134 PASS. |
| `phanthienquoc/TCE-dashboard` | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Latest previously verified native WF-06 #41962074678 (10:30:58 ICT) failed four public HTTP 200 probes with 503. |
| `phanthienquoc/stockdividend` | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS on Nov 3; paired production promotion remains disabled. |
| `phanthienquoc/media-generation` | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS on Nov 3; last live cluster evidence showed backend/frontend 1/1, but is stale. |
| `phanthienquoc/phanthienquoc-authentication` | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 PASS on Nov 3; Supabase Preview remains SKIPPED and migration/integration gate remains closed. |

### Exact open-PR head checks re-read

- Platform #1222 draft, head `f018e39eda52770539fc10671fba0d04baec8046`: `validate-manifests` #41821355040 PASS (historical). Keep draft: Docker/Kubernetes mutation authority, shell UID/GID isolation and reproducible build/test/lockfile evidence remain unresolved.
- Platform #544 draft, head `c95e7daecb83b65577b54303427fe4ea81adfe06`: #38575430454 PASS (historical).
- Platform #541 draft, head `b8f7c6ba04e3d971336a899b2efd5894662083b3`: #38567431761 PASS (historical).
- Platform #539 draft, head `2dc48b97017ecb08e49682633303a2f1d5e991a1`: #38548718033 PASS (historical).
- Authentication #75 ready, head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`: #40446492086 PASS (historical). Do not merge: the connected Supabase GitHub integration has Deploy to production enabled on `master`; the merge-triggered side effect has not been authoritatively ruled safe.
- Authentication #76 draft, head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`: #41329425940 PASS (historical). Keep draft; migration provenance work is not deployment authorization.

PR #1257 was re-read from the closed-PR list and is confirmed merged. Its exact head is `73c575b22a5bad229edd2ee843f135a39fff9ef5`; exact-head workflow run #41971521055 completed successfully. Post-merge run #41971589134 was inspected job-by-job: the `validate` job and all executed steps passed, including immutable image-change, Auth digest, paired digest, VPS MCP contract, shell syntax, manifest render, Auth GitOps, YAML structure, secret policy, immutable image policy, isolated Keycloak and network-boundary validations.

## Actions run evidence and query limitation

The connected GitHub operations used here can retrieve PR-associated workflow runs for an exact commit, job summaries for a known run ID, and legacy combined commit statuses. They do not expose a repository-wide Actions run listing in this execution. Therefore:

- The PR-head checks above were freshly re-read for the current open PR heads.
- Combined-status lookup returned no status contexts for the five current master SHAs; this is not a passing-check assertion.
- The latest known native schedule and runtime run IDs below are carried forward from the 11:58 ICT tracker checkpoint. This run does **not** claim that no newer workflow runs exist.
- Obtain a fresh repository-wide Actions run list before changing any schedule, declaring recovery, or claiming current production health.

## Last verified native schedule and operational evidence

| Workflow | Latest previously verified native schedule | Result |
|---|---|---|
| Platform `inspect-vps.yml` | #41934713847, 06:33:56 ICT | PASS at run time; now stale. |
| Platform `recover-stale-ops.yml` | #41949145532, 08:31:53 ICT | PASS at run time; now stale. |
| Platform `reconcile-vps.yml` | #41950932898, 08:47:55 ICT | Shared reconciliation passed; Stock health lane failed. |
| Platform `reconcile-schedule-watchdog.yml` | #41951133668, 08:49:44 ICT | FAIL: native inspection freshness exceeded 75 minutes. |
| TCE WF-06 | #41962074678, 10:30:58 ICT | Native schedule delivered; all four public probes returned HTTP 503. |
| TCE WF-12 | #41958165099, 09:54:09 ICT | Native schedule failed freshness. Workflow_run #41962097006 passed after WF-06 but is not native WF-12 schedule evidence. |

At 13:03 ICT the latest known Platform inspection is about 390 minutes old; recovery about 272 minutes; reconciliation about 256 minutes; watchdog about 254 minutes. TCE WF-06 is about 153 minutes old and native WF-12 about 189 minutes old. These ages are based on the last run IDs available in the 11:58 checkpoint, not a fresh Actions list.

## Static deployment-contract review

The current master workflow files were inspected without changing them:

- Platform `inspect-vps.yml` retains cron `2,32 * * * *`, manual dispatch and the master path-scoped push trigger. Its script remains read-only and creates an inspection PR; no production manifest apply is present.
- Platform `reconcile-vps.yml` retains cron `7,22,37,52 * * * *`; manual `workflow_dispatch` defaults to `mode=plan`. It remains the only production apply authority. Schedule/push and authenticated promotion dispatch paths are distinct; image changes remain false except the authenticated `gitops-promoted-ready` promotion event or explicit manual opt-in.
- Platform `gitops-image-promotion.yml` continues to route source events through publisher provenance checks, immutable digest verification and a GitOps PR rather than direct app-repository deployment.
- TCE WF-06/WF-12 remain separate public health and schedule-freshness contracts. Preserve strict HTTP 200 and do not reinterpret workflow_run heartbeat as native cron.
- Stock `deploy.yml` validates the full source SHA tag and ARM64 registry manifest before any paired release handoff. Auth `release.yml` is manual-only and validates immutable SHA/version tags, digest equality, ARM64 and source-run payload provenance.
- Platform `validate-github-actions.yml` and `validate-manifests.yml` retain publisher-provenance, image-change, GitOps and manifest contract tests.

No static evidence justified changing cron declarations, weakening health gates, removing useful release workflows, or introducing a second deployment authority.

## K3s and production readiness

The latest committed `debug/vps-latest.md` snapshot is generated at `2026-11-05T02:56:52Z` / 09:56:52 ICT. It is about 187 minutes old at this checkpoint and is **not current live-health evidence**.

Last snapshot evidence:
- Node `tce-k3s-01` Ready / ARM64; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Disk 56%; available RAM about 19 GiB; `restart_required=yes`.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin Pods and new Backend 0/1 ImagePullBackOff; previous Backend and Frontend 1/1.
- TCE/Auth/Keycloak desired state 0/0; public TCE/Auth/Keycloak probes previously returned HTTP 503.

Last live cluster listing is from manual reconcile #41962132547 at 10:32 ICT and is about 151 minutes old. It confirmed the Stock image-pull failures and Media/MicroFE/NATS 1/1 at that time; it is not a current rollout/health check.

### App release gates

- **StockDividend:** publisher #41563856933 verified immutable ARM64 Scraper/Admin/Backend artifacts for full source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. Production Admin/Backend still reference `12d63b4`, which lacks an ARM64 manifest. Paired handoff/dispatch remain skipped; keep promotion disabled until explicit release authorization and protected Actions:read provenance access are confirmed. Never promote only one of Admin/Backend.
- **Media Generation:** CI #41617592783 passed; last live listing showed backend/frontend 1/1 with digest-pinned images. No fresh publisher-to-GitOps end-to-end release evidence was obtained.
- **Authentication:** CI #41670642852 passed; #75/#76 checks are historical. Supabase Preview remains skipped; integration deployment effect and migration provenance remain unresolved. Do not merge #75, run migrations, or activate Auth/Keycloak based on CI alone.

## Next dependency-safe actions

1. Obtain a fresh repository-wide Actions run listing and read-only K3s inspection; verify native schedule delivery separately from dispatch/workflow_run fallbacks.
2. Keep Stock paired promotion disabled until release authorization and protected Actions:read provenance are confirmed.
3. Investigate TCE/Auth HTTP 503 only with fresh endpoint/runtime evidence; retain HTTP 200 gates and desired replicas 0/0 unless activation is separately authorized.
4. Keep Auth #75/#76 gated on Supabase integration binding and migration provenance.
5. Keep Platform #1222 draft until Docker/Kubernetes mutation authority is removed or reconciled with the sole GitOps authority and shell isolation/build/test evidence is complete.
6. Wait for an approved VPS maintenance window before package upgrades or reboot.

No production manifest apply, image promotion, database migration, desired replica change, Pod restart, host package upgrade, reboot, or cron change was performed by this checkpoint. Earlier reconcile #41962132547 did perform controlled Auth runtime Secret and shared GHCR pull-credential reconciliation; do not describe it as read-only. `reconcile-vps.yml` remains the sole production apply authority. App repositories own tests/builds/immutable GHCR publication; Platform Infra owns manifests, shared credentials, promotion, reconciliation, rollout and health verification. Preserve useful CI/security/backup/manual/release/scheduled workflows and avoid duplicate direct SSH/Compose/MCP mutation authority. The TCE market-scan schedule remains unchanged.

### Evidence

- PR #1257: https://github.com/phanthienquoc/platform-infra/pull/1257
- Exact-head validation #41971521055: https://github.com/phanthienquoc/platform-infra/actions/runs/41971521055
- Post-merge validation #41971589134: https://github.com/phanthienquoc/platform-infra/actions/runs/41971589134
- Native Platform inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Native Platform reconciliation #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native Platform watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Manual Platform reconciliation #41962132547: https://github.com/phanthienquoc/platform-infra/actions/runs/41962132547
- Native TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 workflow_run #41962097006: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962097006
- Native TCE WF-12 #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment checkpoint — 2026-11-05 13:58 ICT / 06:58 UTC

## Repository heads, open PRs and latest Actions evidence

| Repository | Current master | Open PRs | Latest verified evidence |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `499ed173d9e58f04a2a3b42033661e1a8b0302b1` | #1222, #544, #541, #539 (all draft) | Native inspection #41980605875 PASS; snapshot PR #1259 merged at exact validated head; manual reconcile #41980764155 failed only Stock health. |
| `phanthienquoc/TCE-dashboard` | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | WF-07 native schedule #41982802263 PASS; WF-12 workflow_run #41982820872 FAIL because WF-06 schedule is stale; latest WF-06 native #41962074678 failed four HTTP 200 probes with 503. |
| `phanthienquoc/stockdividend` | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS (Nov 3); no newer runs. Production Admin/Backend tags remain incompatible with ARM64. |
| `phanthienquoc/media-generation` | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS (Nov 3); latest K3s snapshot shows backend/frontend 1/1 and digest-pinned. |
| `phanthienquoc/phanthienquoc-authentication` | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS (Nov 3); Supabase integration/migration provenance gate remains closed. |

### Open PR head checks

- Platform #1222 draft, head `f018e39eda52770539fc10671fba0d04baec8046`: #41821355040 PASS (historical); keep draft because Docker/Kubernetes mutation scope, shell UID/GID isolation and reproducible build/test/lockfile evidence remain unresolved.
- Platform #544 draft, head `c95e7daecb83b65577b54303427fe4ea81adfe06`: #38575430454 PASS (historical).
- Platform #541 draft, head `b8f7c6ba04e3d971336a899b2efd5894662083b3`: #38567431761 PASS (historical).
- Platform #539 draft, head `2dc48b97017ecb08e49682633303a2f1d5e991a1`: #38548718033 PASS (historical).
- Authentication #75 ready, head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`: #40446492086 PASS (historical); do not merge until Supabase deployment side effects are resolved.
- Authentication #76 draft, head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`: #41329425940 PASS (historical); migration drift planning is not migration authorization.

PR #1259 inspection snapshot:
- Native schedule run #41980605875 succeeded at 06:28:06Z / 13:28:06 ICT.
- Snapshot generated at 06:28:14Z / 13:28:14 ICT.
- PR #1259 exact head `91bee4bfa3c2faf6433dbdabcea78d094bd64df2` passed exact-head `validate-manifests` #41980684859.
- PR #1259 was squash-merged at 06:29:17Z as master commit `499ed173d9e58f04a2a3b42033661e1a8b0302b1`.
- No separate post-merge validation run for #1259 was verified in this checkpoint.

## Platform native schedule and recovery evidence

| Workflow | Latest native `event=schedule` | Result |
|---|---|---|
| `inspect-vps.yml` | #41980605875, 13:28:06 ICT | PASS; fresh read-only snapshot and exact-head snapshot PR #1259 merged. |
| `reconcile-vps.yml` | #41950932898, 08:47:55 ICT | FAIL in Stock health lane; manual #41980764155 at 13:29:35 ICT also failed Stock health. |
| `recover-stale-ops.yml` | #41949145532, 08:31:53 ICT | PASS at run time, but stale; no newer native scheduled recovery event in the Actions listing. |
| `reconcile-schedule-watchdog.yml` | #41951133668, 08:49:44 ICT | FAIL at run time. Workflow_run watchdog #41980748672 at 13:29:27 ICT also failed because native recovery #41949145532 was 297 minutes old, beyond the 45-minute budget. |

The inspection native schedule has resumed for at least one cycle; do not claim continuous recovery until subsequent native slots are observed. The watchdog run #41982861974 (workflow_run, 13:48 ICT) was skipped and is not native schedule evidence.

TCE WF-07 scheduled run #41982802263 at 13:47:35 ICT sent an authenticated schedule heartbeat. TCE WF-12 run #41982820872 at 13:47:46 ICT:
- Failed its WF-06 freshness check: latest native WF-06 #41962074678 was 196 minutes old versus the 25-minute budget.
- Successfully validated and dispatched the Platform heartbeat (HTTP 204).
- Payload identified source event `schedule`, source workflow `.github/workflows/wf-07-tce-integration-check.yml`, source run #41982802263 attempt 1, TCE master SHA `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`, and heartbeat run #41982820872 attempt 1.

Platform recovery controller #41982836006 (repository_dispatch, 13:47:55 ICT) validated that external heartbeat and completed successfully. It did not dispatch another reconcile because manual reconcile #41980764155 was only 16 minutes old (20-minute fallback budget), and it did not dispatch inspection because native inspection #41980605875 was only 19 minutes old (75-minute budget). This repository_dispatch is fallback coordination, not native recovery schedule evidence. WF-07 integration success is not WF-06 application health.

## TCE schedule and public health

- WF-06 latest native schedule: #41962074678 at 10:30:58 ICT; TCE web, TCE API, Auth liveness and Auth readiness all returned HTTP 503 instead of HTTP 200. No newer WF-06 native schedule appears in the latest Actions listing.
- WF-12 latest native schedule: #41958165099 at 09:54:09 ICT, failed freshness. Latest workflow_run #41982820872 also failed because WF-06 was stale.
- WF-07 integration schedule #41982802263 at 13:47:35 ICT passed Binance Testnet public and private API checks (HTTP 200); the order integration job was skipped by design.
- Keep strict HTTP 200 and the 25-minute WF-06 schedule freshness contract. Do not change any TCE cron declaration or market-scan schedule.

## Fresh K3s snapshot and live runtime state

Snapshot `debug/vps-latest.md` generated at `2026-11-05T06:28:14Z` / 13:28:14 ICT, approximately 30 minutes old at this checkpoint; it is current point-in-time evidence, not continuous health.

- Node `tce-k3s-01`: Ready, ARM64; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Disk 56%; available RAM about 19 GiB; Docker 29.1.3; host `restart_required=yes`.
- Media backend/frontend: 1/1, digest-pinned.
- MicroFE Shell/WS and NATS: 1/1, digest-pinned.
- Keycloak and MicroFE Auth: 0/0.
- TCE namespace has no Pods; TCE frontend/service desired state 0/0.
- Stock Admin has two Pods 0/1 `ImagePullBackOff`; new Stock Backend is 0/1 `ImagePullBackOff`; previous Backend and Frontend remain 1/1.
- Stock Admin image `admin:12d63b4` and new Backend image `backend:12d63b4` have no resolved image digest and containerd reports `no match for platform in manifest`. Existing Backend/Frontend still use older `23b2878` images with resolved digests.

## Reconciliation side effects and release gates

Manual reconciliation #41980764155 ran with `mode=apply`, `target_app=all`, `ALLOW_IMAGE_CHANGES=false`:
- Shared preflight, GHCR pull-access validation, Auth runtime Secret provisioning, shared GHCR pull-credential bootstrap and managed image-pull restart policy all succeeded.
- Auth, MicroFE, TCE and Media lanes succeeded; Keycloak lane was skipped.
- Stock workload health failed for both Admin Pods and the new Backend; final deployment summary correctly failed.
- Production manifest apply, image-change guard and drift-clear verification were skipped. No image promotion or production manifest apply is evidenced.
- This was not a read-only reconcile: Auth runtime Secret and shared GHCR pull credentials were provisioned/verified.

Release gates:
- **StockDividend:** keep paired Admin/Backend promotion disabled until explicit release authorization and protected Actions:read publisher provenance access are confirmed. Never promote one component independently.
- **Media Generation:** CI passed; snapshot confirms both workloads 1/1 and digest-pinned. No new app release was initiated.
- **Authentication:** keep #75/#76 gated on Supabase integration binding and migration provenance; no migration or activation.
- **VPS:** pending package upgrades include containerd 2.4.2 and Docker 29.9.3; host requires restart. Wait for an approved maintenance window.

## Exact next actions

1. Verify the next native Platform slots without changing cron: inspection 14:02 ICT, reconciliation 14:07 ICT, recovery 14:10 ICT, watchdog 14:12 ICT. Keep native schedule evidence separate from dispatch/workflow_run fallback.
2. Keep Stock Admin/Backend paired promotion blocked until explicit release authorization and protected publisher-run read access are available.
3. Investigate WF-06 delivery and the four HTTP 503 endpoints with fresh evidence; preserve HTTP 200 and desired replicas 0/0 unless activation is separately authorized.
4. Resolve Auth Supabase deployment binding and migration provenance before merging #75/#76 or running migrations.
5. Keep Platform MCP PR #1222 draft until mutation authority, shell isolation and reproducible build/test evidence are complete.
6. Wait for an approved VPS maintenance window before package upgrades or reboot.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, manifest apply, database migration, desired replica change, host package upgrade, reboot or cron expression change was performed in this checkpoint. Earlier controlled reconciliation #41980764155 provisioned Auth runtime Secret and shared GHCR credentials. TCE market-scan schedule remains unchanged.

### Evidence

- PR #1259: https://github.com/phanthienquoc/platform-infra/pull/1259
- Native inspection #41980605875: https://github.com/phanthienquoc/platform-infra/actions/runs/41980605875
- Exact-head inspection validation #41980684859: https://github.com/phanthienquoc/platform-infra/actions/runs/41980684859
- Manual reconcile #41980764155: https://github.com/phanthienquoc/platform-infra/actions/runs/41980764155
- Platform watchdog #41980748672: https://github.com/phanthienquoc/platform-infra/actions/runs/41980748672
- TCE WF-07 schedule #41982802263: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41982802263
- TCE WF-12 workflow_run #41982820872: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41982820872
- Platform recovery via repository_dispatch #41982836006: https://github.com/phanthienquoc/platform-infra/actions/runs/41982836006
- Native Platform inspection previous #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Native Platform reconcile #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native Platform watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Native TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- Native TCE WF-12 #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Authentication CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852

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


## Checkpoint — 2026-11-05 17:57 ICT

- Platform master advanced to 3eb956ee8527119699cea8a1e17cafc758e98293 after read-only inspection PR #1265. Inspection fallback #42013436672 and exact-head validation #42013546013 passed; native schedule history remains stale as recorded in the tracker.
- Fresh snapshot generated 17:46:16 ICT: node Ready/ARM64; disk 56%; about 19 GiB RAM available; Media/MicroFE healthy 1/1; Stock Admin and new Backend still ImagePullBackOff on 12d63b4; TCE/Auth/Keycloak 0/0; host restart required.
- TCE WF-12 native #42013061466 failed WF-06 freshness after 432 minutes without a native WF-06 run; Platform heartbeat dispatch returned HTTP 204.
- TCE PR #1023 now isolates Actions:write in new WF-13 workflow_run recovery. WF-12 was restored to actions:read after the existing contract validator rejected the interim write permission. Current head c82afdbd836acff29fd60b0307478f02b8cd0f18; WF-05/WF-02 exact-head checks still pending/in progress. Do not merge yet.
- Stock immutable ARM64 publisher #41563856933 remains PASS, but production promotion stays disabled pending authorization and provenance.
- No production image/manifest/database/replica/host change. TCE market-scan schedule unchanged.


## Checkpoint — 2026-11-05 18:10 ICT

- Platform docs PR #1266 merged as aed8655f98dbc486b5c96525b3fffd2b544a350a; post-merge validate-manifests #42016668480 PASS.
- TCE PR #1023 merged as a7b26b21782e4031364a9559b6eefdc2e654cc1e after exact-head WF-05 #42016023371 and WF-02 #42016023242 PASS. Post-merge WF-05 #42016555379 and WF-02 #42016555285 PASS; WF-01 #42016555183 still in progress.
- WF-12 remains read-only. The isolated WF-13 workflow_run recovery dispatcher has Actions:write, no cron and can dispatch only WF-06 after a failed native WF-12 schedule event on master. Contract validator now parses and asserts this boundary.
- End-to-end WF-13 dispatch not yet observed because native WF-12 schedule history still ends at #42013061466. The HTTP 204 Platform heartbeat is not TCE health evidence.
- Latest K3s snapshot generated 17:46:16 ICT; Stock Admin/new Backend still ImagePullBackOff on 12d63b4; Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0.
- Stock immutable ARM64 publication remains verified, but production paired promotion remains disabled pending authorization/provenance.
- No production mutations, host maintenance or cron changes. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 19:31 ICT / 12:31 UTC

- **Repository heads:** Platform Infra `1d8e7c375a3ed45a9ec52eb1072c94d865b87d7b`; TCE Dashboard `a7b26b21782e4031364a9559b6eefdc2e654cc1e`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1268 (draft), #544/#541/#539 (draft); Authentication #75 (ready), #76 (draft); no open PRs in TCE, StockDividend or Media.
- **Platform PR #1268:** current exact head `0a2769a98e041e738b7553748250d3555e7da3fd`. After adding the required `## Current actions` and `## Current runtime blockers` tracker sections, exact-head `validate-github-actions` #42028865777 PASS, `validate-manifests` #42028865526 PASS and dedicated `Validate TCE VPS Control MCP` #42028865517 PASS. Earlier head `1380e66` failed only at the tracker structural assertion. The generated lockfile artifact #13413128069 was downloaded and inspected; it contains lockfileVersion 3, 94 packages, exact direct dependency versions, registry.npmjs.org HTTPS tarball URLs and integrity metadata. The package-lock is not yet committed, so PR #1268 remains draft.
- **Platform native schedules:** inspect-vps #41980605875 (13:28:06 ICT, PASS); reconcile-vps #41995809261 (15:36:40 ICT, Stock health FAIL); recover-stale-ops #41994805588 (15:29:01 ICT, PASS); reconcile-schedule-watchdog #41997764646 (15:51:58 ICT, FAIL freshness). No newer native schedule runs were found in the inspected Actions history. Latest K3s evidence remains fallback snapshot #42013436672 generated 17:46:16 ICT and is now stale (>75 minutes).
- **TCE schedule/recovery:** WF-06 native #42019530614 at 18:30:38 ICT failed. Latest native WF-12 is #42013061466 at 17:43:23 ICT and failed freshness. WF-12 workflow_run #42019562593 completed successfully after WF-06, but WF-13 #42019590810 was correctly skipped because its source WF-12 event was `workflow_run`, not `schedule`. No qualifying native WF-12 schedule completion has exercised WF-13 end-to-end. Do not modify any TCE cron.
- **StockDividend:** CI #41563856934 and publisher #41563856933 remain PASS. Three immutable ARM64 digests are verified; paired production promotion remains disabled pending explicit release authorization and protected Actions:read provenance.
- **Media Generation:** CI #41617592783 PASS; last snapshot showed backend/frontend 1/1, but runtime evidence is stale.
- **Authentication:** CI #41670642852 PASS; PR #75 ready and #76 draft remain gated on Supabase production binding and migration provenance.
- **Ownership/safety:** App repos continue to own tests/builds/immutable GHCR publication; Platform Infra owns manifests, shared pull credentials, promotion, reconciliation, rollout and health. `reconcile-vps.yml` remains the sole production apply authority. No production image/manifest/database/replica/host/cron change was made; TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 19:43 ICT / 12:43 UTC

- **Platform master:** PR #1269 merged at e07cf243fab7e98238bd8e79197e120870bad3d2. Post-merge validate-manifests #42029574773 completed PASS; manifest render, Auth GitOps contract, secret policy, immutable-image policy, Keycloak isolation, network boundary and VPS MCP GitOps-only contract all passed.
- **Platform PR #1268:** current head 83c0bf4d2639bf9d5dfaa3a75d30ba5454de5c47; exact-head validate-github-actions #42029072787 PASS, validate-manifests #42029072816 PASS, dedicated MCP validation #42029072596 PASS. The earlier workflow-contract failure #42025438305 was fixed by restoring the required tracker headings. PR remains draft because the reviewed lockfile artifact #13413128069 is not yet committed as apps/tce-vps-control-mcp/package-lock.json.
- **Open PRs:** Platform #1268 (draft), #544/#541/#539 (draft); Authentication #75 (ready), #76 (draft); no open PRs in TCE, StockDividend or Media.
- **Platform native schedules:** inspect-vps #41980605875 (13:28:06 ICT, PASS but stale); reconcile-vps #41995809261 (15:36:40 ICT, Stock health FAIL); recover-stale-ops #41994805588 (15:29:01 ICT, PASS but stale); schedule watchdog #41997764646 (15:51:58 ICT, FAIL freshness). No newer native schedule runs were found in the inspected Actions history. Last K3s snapshot #42013436672 was generated 17:46:16 ICT and is beyond the 75-minute inspection freshness budget.
- **TCE:** WF-06 native #42019530614 at 18:30:38 ICT failed all four strict public probes with HTTP 503: https://tce.mrcute.space/, https://tce.mrcute.space/api/health, https://auth.mrcute.space/api/ready, https://auth.mrcute.space/api/health. Latest native WF-12 #42013061466 at 17:43:23 ICT failed WF-06 freshness (latest scheduled WF-06 age 432m at that run). WF-12 workflow_run #42019562593 was not a native schedule; WF-13 #42019590810 correctly skipped because source event was workflow_run, not schedule. No qualifying native WF-13 end-to-end dispatch is evidenced.
- **StockDividend:** CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; Scraper/Admin/Backend SHA-256 digests verified. Production still references incompatible 12d63b4; paired promotion remains disabled pending explicit release authorization and protected publisher-run Actions:read provenance.
- **Media Generation:** CI #41617592783 PASS; last snapshot showed backend/frontend 1/1, but the snapshot is stale and does not prove current health.
- **Authentication:** CI #41670642852 PASS; PR #75 ready and #76 draft remain blocked by unresolved Supabase production integration binding and migration provenance.
- **Safety:** no production manifest/image/database/replica/host/cron mutation. reconcile-vps.yml remains sole production apply authority. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 19:56 ICT / 12:56 UTC

- **Repository heads:** Platform Infra `9c931c51e51ddc4ae3f55e3a4f3c266122d86f55`; TCE Dashboard `a7b26b21782e4031364a9559b6eefdc2e654cc1e`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1268 draft, #544/#541/#539 draft; Authentication #75 ready and #76 draft; none in TCE, StockDividend or Media. Platform #1222 is closed/unmerged, not open.
- **Platform master:** validate-manifests #42030024927 on master `9c931c51e51ddc4ae3f55e3a4f3c266122d86f55` completed PASS.
- **Platform PR #1268:** exact head `81dfa692dc4a0b363314da72cac6700f1d7f514f`; exact-head validate-github-actions #42030355670, validate-manifests #42030355586 and dedicated MCP #42030355637 all PASS. Dedicated job #127254938646 completed lockfile generation, `npm ci`, security tests, typecheck, build, shell syntax and ShellCheck successfully. Artifact #13416365990 ZIP SHA-256 is `243c49c8dacd401f777a666803f05981373a555a40544497a6cdd7119e3a0933`; extracted lockfile SHA-256 is `105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0`. Lockfile v3 has 94 package entries, exact root dependency versions, 93 dependency entries with integrity and HTTPS npm registry tarballs. It remains uncommitted; PR stays draft.
- **Platform native schedules:** explicit `event=schedule` query returned no newer runs than inspect-vps #41980605875 (13:28:06 ICT, PASS but stale), reconcile-vps #41995809261 (15:36:40 ICT, Stock health FAIL), recover-stale-ops #41994805588 (15:29:01 ICT, PASS but stale), and schedule watchdog #41997764646 (15:51:58 ICT, inspection freshness FAIL). No newer native events were returned at 19:56 ICT.
- **K3s:** latest snapshot remains fallback #42013436672, generated 17:46:16 ICT; now about 130 minutes old and stale against the 75-minute budget. Snapshot showed node Ready/ARM64, disk 56%, ~19 GiB RAM, Media/MicroFE/NATS 1/1, Stock Admin/new Backend ImagePullBackOff, previous Backend/Frontend 1/1, TCE/Auth/Keycloak 0/0 and host restart required. Do not claim current health.
- **TCE:** native WF-06 #42019530614 at 18:30:38 ICT failed all four public probes with HTTP 503. Native WF-12 #42013061466 at 17:43:23 ICT failed freshness. WF-12 workflow_run #42019562593 succeeded after WF-06; WF-13 #42019590810 correctly skipped because the source event was `workflow_run`, not `schedule`. No qualifying WF-13 end-to-end dispatch is evidenced. No TCE cron or market-scan schedule changed.
- **StockDividend:** CI #41563856934 and immutable ARM64 publisher #41563856933 PASS; three full-SHA digests remain verified. Production paired promotion remains blocked on explicit authorization and protected publisher Actions:read provenance.
- **Media Generation:** CI #41617592783 PASS; runtime evidence is stale.
- **Authentication:** CI #41670642852 PASS; #75/#76 remain gated on Supabase production deployment binding and migration provenance.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform Infra owns manifests/shared pull credentials/promotion/reconciliation/rollout/health. `reconcile-vps.yml` remains sole production apply authority and `inspect-vps.yml` read-only. No production image, manifest, database, replica, host or cron mutation. TCE market-scan schedule unchanged.


## Deployment authority audit — 2026-11-05 20:59 ICT / 13:59 UTC

- Reviewed current app publisher workflows: TCE wf-03-tce-production-deploy.yml, Stock deploy.yml, Media wf-03-media-production-deploy.yml, Auth release.yml. They build/publish images and send release requests or digest handoffs to Platform Infra; the reviewed paths do not SSH to production, run Compose, or apply Kubernetes manifests.
- Platform gitops-image-promotion.yml owns provenance/digest validation and GitOps manifest promotion. Platform reconcile-vps.yml remains the sole production apply authority. No duplicate direct SSH/Compose or app-owned kubectl apply path was found in the reviewed release workflows.
- Preserve the manual/release triggers: these are deliberate app-owned publishers, not redundant deploy authorities.
- Current master SHAs: Platform 30db773980223132997a3e98c9703c4e2d90c70a; TCE a7b26b21782e4031364a9559b6eefdc2e654cc1e; Stock 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; Media e4c7d8990aafc7d837e918c9caf39722d623de7c; Auth f978a3f378ee22d4630909c2d182275b21ac9e9a.
- Open PRs: Platform #1268/#544/#541/#539; Auth #75/#76; none in TCE, Stock or Media. Platform #1268 is draft because its reviewed lockfile is not committed. Auth #75 exact-head CI #40446492086 passed, but its Supabase master-push side-effect gate remains unresolved.
- Native Platform schedule evidence remains stale; latest K3s snapshot #42013436672 is over the 75-minute freshness budget. TCE WF-13 #42019590810 was skipped for a non-native WF-12 workflow_run event; no native end-to-end recovery is evidenced.
- Do not change any cron declaration, production image, manifest, database, desired replica count, host or deployment authority. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 22:17 ICT / 15:17 UTC

- **Repository heads:** Platform Infra `7b7a287209058f568c9c285092394324c1e50bd2`; TCE Dashboard `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1268/#544/#541/#539; Authentication #75/#76; none in TCE, StockDividend or Media. TCE PR #1024 merged.
- **TCE WF-13 recovery contract:** PR #1024 fixes the invalid top-level `github.event.workflow.path` reference by validating `github.event.workflow_run.workflow_id` (WF-06 339198323; WF-12 403352324). WF-13 listens to failed native schedule completions from both workflows. Failed WF-06 schedule triggers a deduplicated read-only WF-06 fallback; failed WF-12 schedule triggers fallback only when native WF-06 is stale. Exact-head WF-05 #42053173288/WF-02 #42053173277 and post-merge WF-01 #42053388961/WF-02 #42053388868/WF-05 #42053388841 all PASS. No qualifying post-merge native schedule event has exercised the new path yet.
- **TCE native schedule:** latest native WF-06 #42019530614 at 18:30:38 ICT failed all four strict public probes with HTTP 503; latest native WF-12 #42013061466 at 17:43:23 ICT failed freshness. No later native TCE schedule event was returned at this checkpoint. Cron declarations, especially the market-scan schedule, are unchanged.
- **Platform native schedule:** inspect-vps #42049660972 ran natively at 21:55:03 ICT and passed. Recovery controller #42049921179 succeeded from that inspection's workflow_run event; this is not a native recovery cron tick. Native recover-stale-ops remains stale (#41994805588 at 15:29:01 ICT), and watchdog #42049921274 failed native recovery freshness. Native reconcile remains #41995809261; manual reconcile #42049945662 failed only Stock health, and post-reconcile recovery #42050256242 passed.
- **K3s:** snapshot #42049660972 generated 21:55:12 ICT; node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB RAM available, GitOps drift clean, restart_required=yes. Media backend/frontend, MicroFE Shell/WS/NATS 1/1. Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due no matching platform manifest; old Backend/Frontend 1/1 on `23b2878`. TCE/Auth/Keycloak 0/0.
- **Stock release:** CI #41563856934 and immutable publisher #41563856933 PASS with three linux/arm64 digests. Production paired promotion remains disabled pending explicit release authorization and protected publisher Actions:read provenance.
- **Media/Auth:** Media CI #41617592783 PASS and runtime 1/1 in the fresh snapshot. Auth CI #41670642852 PASS; PR #75/#76 remain gated on Supabase production binding and migration provenance.
- **MCP:** Platform PR #1268 remains draft at head 81dfa692dc4a0b363314da72cac6700f1d7f514f; three exact-head checks pass, but reviewed package-lock artifact #13416365990 remains uncommitted.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR publication; Platform owns manifests/shared pull credentials/promotion/reconciliation/rollout/health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` read-only. No duplicate SSH/Compose authority, production image promotion, manifest apply, DB migration, replica change, host reboot or package upgrade. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 23:30 ICT / 16:30 UTC

- **Current master SHAs:** Platform `a239187b7694a02dedb2b7ade6b31e0be139ac44`; TCE `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; Stock `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Auth `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Auth #75 ready/#76 draft; none in TCE, Stock or Media.
- **Platform merged work:** #1268 adds diagnostics-only VPS MCP and committed lockfile; #1276 records fresh inspection snapshot; #1278 prevents MCP-only files from triggering production reconciliation and adds resolver regression coverage. #1278 exact-head checks #42064383310/#42064383238/#42064383170 and post-merge #42064588984/#42064588923/#42064588960 all PASS.
- **Reconcile failure:** #42063703873 triggered on MCP merge due broad `apps/**` push filter and failed closed on `apps/tce-vps-control-mcp/.env.example`. All production mutation steps were skipped. Recovery controller #42063793863 dispatched inspection #42063840567, which passed. This fallback is not native schedule evidence.
- **K3s snapshot:** #42063840567 generated `debug/vps-latest.md` at 23:23:06 ICT. Node Ready/ARM64; disk 56%; ~19 GiB RAM; GitOps drift clean; Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4` due missing ARM64 manifest; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; host restart required.
- **Native Platform schedules:** inspect-vps #42049660972 PASS at 21:55 ICT; reconcile-vps #41995809261 FAIL Stock health; recover-stale-ops #41994805588 PASS but stale; watchdog #41997764646 FAIL freshness. No later native schedule event was returned.
- **TCE native schedules:** WF-06 #42019530614 failed four public probes at 18:30:38 ICT; WF-12 #42013061466 failed freshness at 17:43:23 ICT; WF-13 #42019590810 skipped on non-native workflow_run source. No E2E recovery event yet. WF-01 #42053388961, WF-02 #42053388868 and WF-05 #42053388841 post-merge checks PASS.
- **Stock:** CI #41563856934 and ARM64 publisher #41563856933 PASS; paired promotion blocked on release authorization/provenance.
- **Media:** CI #41617592783 PASS; runtime 1/1 in the fresh fallback snapshot.
- **Auth:** CI #41670642852 PASS; PR #75/#76 remain gated on Supabase binding/migration provenance.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/shared pull credentials/promotion/reconciliation/rollout/health. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` read-only. No production image/manifest/database/replica/host/cron mutation. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 23:44 ICT / 16:44 UTC

- **Repository heads:** Platform Infra `d4705442de747c80ace35d14f7dee209e25fe6ac`; TCE Dashboard `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft); Authentication #75 (ready)/#76 (draft); none in TCE, StockDividend or Media.
- **Platform #1280:** merged as `d4705442de747c80ace35d14f7dee209e25fe6ac`. Exact-head validate-github-actions #42066670909 and validate-manifests #42066667137 PASS; post-merge #42067822505 and #42067839646 PASS. The change excludes diagnostics-only MCP paths from recovery push bootstrap and extends workflow/resolver regression contracts. No cron expression or production apply authority changed.
- **MCP:** PR #1268 was already merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`, including committed package-lock and diagnostics-only permissions. The follow-on #1280 fix closes the separate recovery-controller trigger gap; MCP remains subordinate to GitOps and cannot mutate Docker/Kubernetes.
- **Native Platform schedules:** inspect-vps #42049660972 PASS (21:55:03 ICT); reconcile-vps #41995809261 FAIL (Stock health); recover-stale-ops #41994805588 PASS but stale; watchdog #41997764646 FAIL freshness. No newer `event=schedule` runs returned. Recovery workflow_run and workflow_dispatch fallbacks are not native schedule evidence.
- **K3s snapshot:** #42063840567 generated 23:23:06 ICT by workflow_dispatch. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB RAM, GitOps drift clean, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **TCE:** latest native WF-06 #42019530614 failed all four HTTP 200 probes with 503; WF-12 #42013061466 failed freshness; WF-07 #41982802263 passed. PR #1024 and post-merge WF-01/WF-02/WF-05 checks pass, but no qualifying native WF-13 E2E dispatch is evidenced. No TCE cron changed.
- **StockDividend:** CI #41563856934 and immutable ARM64 publisher #41563856933 PASS. Build/push and ARM64 manifest verification passed; Platform handoff and atomic paired production promotion were SKIPPED. Keep authorization/provenance gate closed.
- **Media:** CI #41617592783 PASS; latest snapshot shows backend/frontend 1/1.
- **Authentication:** CI #41670642852 PASS. PR #75/#76 remain gated on Supabase Deploy to production binding and migration provenance; checks #40446492086/#41329425940 are historical, Preview skipped.
- **Safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/credentials/promotion/reconcile/rollout/health. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only. No production image/manifest/database/replica/host/cron mutation. TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-05 23:53 ICT / 16:53 UTC

- **Repository heads:** Platform Infra `cd5f9001f826a3a25cf992289176df827ac28c77`; TCE Dashboard `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Authentication #75 ready/#76 draft; none in TCE, StockDividend or Media.
- **Platform #1281:** merged as `cd5f9001f826a3a25cf992289176df827ac28c77`; exact-head validate-manifests #42068751747 and post-merge #42068869578 PASS. This was tracker/inventory/checkpoint-only.
- **Native recovery schedule:** #42068414686 PASS at 23:49:29 ICT. It verified fallback dispatch #42068463484 with `ref=master`, SHA `d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`.
- **Native reconciliation:** #42068683835 at 23:51:03 ICT completed FAILURE only on Stock health; shared preflight passed, no manifest drift and apply skipped; TCE/Auth/MicroFE/Media scoped lanes passed. Fallback #42068463484 had the same Stock-only health failure. Recovery #42068810024 PASS and correctly skipped another inspection fallback because snapshot #42063840567 was still fresh.
- **Watchdog:** #42068511916 at 23:50:05 ICT failed on the then-latest native reconcile #41995809261 age 493m and inspect #42049660972 age 115m; it did verify recovery #42068414686 PASS. The later #42068683835 native reconcile started after the watchdog and is new schedule evidence, not a retroactive fix to that run.
- **K3s:** latest snapshot #42063840567 at 23:23:06 ICT by workflow_dispatch; node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB RAM, GitOps drift clean, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **TCE:** native WF-06 #42019530614 HTTP 503, WF-12 #42013061466 freshness FAIL, WF-07 #41982802263 PASS; no post-merge WF-13 E2E dispatch. Do not change cron or market-scan schedule.
- **Stock:** publisher #41563856933 ARM64 build/push and immutable manifest checks PASS; Platform handoff/atomic promotion SKIPPED. No release authorization/provenance; no production promotion.
- **Media/Auth:** Media CI #41617592783 PASS and 1/1 in latest snapshot. Auth CI #41670642852 PASS; #75/#76 remain gated by Supabase production binding/migration provenance.
- **Safety:** no production image/manifest/database/replica/host/cron mutation. `reconcile-vps.yml` sole apply authority, `inspect-vps.yml` read-only, TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-06 00:03 ICT / 2026-11-05 17:03 UTC

- **Repository heads:** Platform Infra `6c2b826175d135b41fcb69f28ca2268391c357c2`; TCE Dashboard `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 draft; Authentication #75 ready/#76 draft; none in TCE, StockDividend or Media.
- **Platform #1282:** merged as `6c2b826175d135b41fcb69f28ca2268391c357c2`; exact-head validate-manifests #42069918051 and post-merge #42070150263 PASS.
- **Native Platform schedule:** recover-stale-ops #42068414686 PASS; reconcile-vps #42068683835 completed with Stock-only health failure; watchdog #42070623710 failed only native inspection freshness (native reconcile age 11m and recovery age 12m passed). Native inspect-vps remains #42049660972 at 21:55:03 ICT, 127m old at watchdog.
- **Inspection fallback:** recovery controller #42070696343 PASS; it did not dispatch a duplicate inspection because workflow_dispatch snapshot #42063840567 was 38m old. Native schedule remains stale.
- **K3s:** snapshot #42063840567 at 23:23:06 ICT by workflow_dispatch; node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, ~19 GiB RAM, GitOps drift clean, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0.
- **TCE:** native WF-06 #42019530614 HTTP 503, WF-12 #42013061466 freshness FAIL, WF-07 #41982802263 PASS; no post-merge WF-13 E2E dispatch. No TCE cron changed.
- **Stock:** publisher #41563856933 ARM64 build/push and immutable manifest checks PASS; Platform handoff/atomic promotion SKIPPED. No release authorization/provenance; no production promotion.
- **Media:** CI #41617592783 PASS; backend/frontend 1/1 in snapshot.
- **Authentication:** Supabase project `gtqovpusfyyvxpeezxlo` ACTIVE_HEALTHY / FUNCTIONS_DEPLOYED; 84 remote migrations exactly match 84 Auth master SQL files, zero mismatch/duplicate. PR #75/#76 are 11 commits behind master; owner-confirmed Deploy to production ON means keep merge blocked pending authoritative integration side-effect confirmation.
- **Safety:** no production image/manifest/database/replica/host/cron mutation. `reconcile-vps.yml` sole apply authority, `inspect-vps.yml` read-only, TCE market-scan schedule unchanged.


## Workflow inventory runtime update — 2026-11-06 06:04 ICT / 2026-11-05 23:04 UTC

- **Live heads / open PRs:** Platform `20af8c89bc2230ff6eb78a58f2066301f75a27a7` (#544/#541/#539 draft); TCE `512b69d837e2a65c39867a062529a7fa0eada4cc` (none); Stock `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` (none); Media `e4c7d8990aafc7d837e918c9caf39722d623de7c` (none); Auth `f978a3f378ee22d4630909c2d182275b21ac9e9a` (#75 ready/#76 draft).
- **Native Platform schedule inventory:** inspect-vps #42112599830 PASS at 21:26:04Z; recover-stale-ops #42121354158 PASS at 22:25:22Z; reconcile-vps #42121826106 FAIL Stock lane at 22:28:47Z; schedule watchdog #42123445690 PASS at 22:40:18Z. The watchdog log reported inspection age 74m, reconcile age 11m, recovery age 14m, inspection/reconcile queue 0m. At checkpoint 23:04Z inspection is 98m old and stale against 75m. Fallback events do not count as native schedule evidence.
- **Reconcile ownership and fail-closed behavior:** #42121826106 had `mode=apply`, `ALLOW_IMAGE_CHANGES=false`; GHCR preflight passed; drift=false; apply skipped. MicroFE/TCE/Auth/Media lanes passed; Stock lane failed due Admin/Backend `12d63b4` lacking ARM64 manifest; permanent image-pull restart guard skipped restart; Keycloak skipped. Keep `reconcile-vps.yml` as sole production apply authority.
- **App publisher inventory:** TCE master build/format/unit tests and push watchdog checks PASS on `512b69d`; no qualifying post-merge native WF-13 E2E. Stock publisher #41563856933 and CI #41563856934 PASS on 2026-11-03, but no newer run and no paired promotion authorization. Media CI #41617592783 PASS on 2026-11-03. Auth service CI #41670642852 PASS on 2026-11-03 and web CI #41542942080 PASS on 2026-11-02. These are historical, not fresh builds.
- **PR checks:** Platform #544/#541/#539 validate PASS on 2026-10-14 (draft/stale); Auth #75 validate PASS but Supabase Preview SKIPPED on 2026-10-27; #76 validate PASS but Supabase Preview SKIPPED on 2026-11-01. Do not merge from those historical checks.
- **Runtime snapshot:** `debug/vps-latest.md` generated 21:26:12Z is stale at checkpoint. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, ~19 GiB available RAM, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/Frontend 1/1.
- **Preserved workflows:** retain app CI, immutable image publishers, security checks, release/manual dispatches, scheduled scraper/scan jobs, inspection, reconciliation, recovery and watchdog. No workflow removal or cron edit.
- **Next:** obtain Stock release authorization/provenance; observe next native inspection/recovery/watchdog; prove TCE post-merge native recovery sequence; resolve Auth Supabase integration side-effect gate; wait for host maintenance approval. TCE market-scan schedule unchanged.


## Runtime inventory update — 2026-11-06 11:01 ICT / 04:01 UTC

- **Repository heads / PR inventory:** Platform Infra `0c322b7104eccc9c05b04e1b7ef4f34c746d167f` (open #1314 docs-only, #544/#541/#539 drafts); TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc` (no PR); StockDividend `6fcefa6b3792dab92b6d5c438001633d25f1ca28` (no PR); Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` (no PR); Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a` (#75 ready, #76 draft).
- **Platform validation:** runner retirement guard PR #1313 merged as `0c322b7104eccc9c05b04e1b7ef4f34c746d167f`. Exact-head #42157150764 (validate-manifests) and #42157150728 (validate-github-actions) PASS; post-merge #42159993013 and #42159993032 PASS. PR #1314 documentation-only mail-service plan validation #42159046171 PASS; it is unrelated to deployment and changes no runtime configuration.
- **Platform production workflow:** Reconcile VPS #42158234979 SUCCESS (workflow_dispatch, `mode=apply`, image changes disabled); shared preflight/credentials and MicroFE/Auth/TCE health lanes PASS; Keycloak skipped. This run predates the #1313 merge and is not native schedule evidence. Latest inspection #42154756357 is workflow_dispatch and produced snapshot at 03:09:17Z. No later native inspection is evidenced in the returned run history.
- **Decommission workflow contract:** `.github/workflows/decommission-stock-media.yml` remains manual-only and protected by production Environment approval, exact typed confirmations, runner retirement guard, fresh storage preflight, fixed namespace allowlist and post-delete verification. PR #1313 hardens `scripts/verify-media-runner-retired.sh` to require systemd inactive plus disabled/masked/not-found and no `Runner.Listener`; GitHub unregistration remains operator-attested. Do not invoke until the dedicated runner is actually retired and storage/external-data/backup ownership is confirmed.
- **TCE Dashboard:** WF-06 #42158243093 failed four public HTTP probes with 503; WF-12 native schedule watchdog #42158209117 failed stale scheduled delivery; WF-13 #42158228852 dispatched a read-only fallback successfully, but the fallback remained unhealthy. Latest returned scheduled WF-06 is #42133793538 (failure); do not count the workflow_dispatch fallback as a native schedule tick. Public 503 aligns with TCE/Auth workloads at 0/0 in the latest K3s snapshot. Keep strict HTTP 200 checks and market-scan schedule unchanged.
- **StockDividend:** master CI #42137523269 PASS. Immutable publisher #41563856933 remains the latest verified publication evidence (2026-11-03); no new digest/provenance or production promotion. K3s snapshot shows two Admin Pods and the newer Backend in ImagePullBackOff due `no match for platform in manifest`; legacy Backend/Frontend are Running. Keep build/publish in Stock; ARM64 multi-platform manifest and digest/provenance must be fixed/verified before Platform promotion.
- **Media Generation:** master CI #42136991059 PASS. K3s snapshot shows backend/frontend 1/1 Running with digest-pinned images. Dedicated Media self-hosted runner is still active and enabled; the new guard is preventive only and does not perform runner retirement.
- **Authentication:** latest listed service CI #41670642852 is historical (2026-11-03); #75/#76 remain gated on authoritative Supabase integration side-effect evidence and fresh exact-head checks. Runtime Auth workload is 0/0 in the latest K3s snapshot; public liveness/readiness returned 503. Do not merge or activate based on historical CI.
- **Ownership and retained workflows:** keep app CI/tests/builds, immutable image publishers, security scans, release/manual dispatches and purposeful scheduled jobs. Keep Platform manifest/credential/provenance/promotion/reconcile/rollout/health workflows. `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only. No direct SSH/Compose deployment authority was introduced or retained as a competing path. TCE market-scan schedule unchanged.


## Immutable publication and dispatch contract audit — 2026-11-06 04:05 UTC

Reviewed the current default-branch workflow files and Platform receivers; this is a source-contract audit, not evidence of a new image publication or deployment.

- **TCE sender:** `TCE-dashboard/.github/workflows/wf-03-tce-production-deploy.yml` (blob `059e686ec445b7c7a796c4ca155168d841588982`) sends `tce-release-requested` with `app`, full-SHA release tag, `web_digest`, `service_digest`, `source_run_id`, `source_workflow_path`, `source_event`, and `source_head_sha`. It validates the serialized payload before dispatch and verifies that Platform scheduled the matching release workflow.
- **TCE receiver:** `platform-infra/.github/workflows/gitops-image-promotion.yml` (blob `d9e371f71fa5352ffc55a1ce728847f3476802b4`) requires the matching app, full-SHA tag, both sha256 digests, source SHA/tag correlation, and successful master publisher run/job/step provenance. It verifies each GHCR tag resolves to the attested digest and includes linux/arm64, validates digest-pinned references, updates the web/service pair atomically in the production overlay, and scopes the PR to that overlay.
- **Auth sender:** `phanthienquoc-authentication/.github/workflows/release.yml` (blob `59122b5ef8fe69b1491973b08c561e77ae225910`) is manual-only and sends `auth-image-published` with app/component, full-SHA commit/tag, digest, source run ID, workflow path, event and source SHA. It rejects non-`workflow_dispatch` publication and verifies the immutable tag/digest and ARM64 manifest before dispatch.
- **Auth receiver:** the Platform promotion workflow validates the exact Auth event target, source SHA/tag, numeric run ID, approved workflow path and manual event; `scripts/verify-auth-publisher-run.sh` (blob `804034e8e4b291b80d076ad1b7d04d183be4576a`) checks the public Actions run identity, master branch, successful application tests/build, ARM64 image publication, digest verification and dispatch step. Platform rechecks full-SHA tag, version tag and digest-reference correlation against GHCR before changing only the Auth image digest manifest.
- **StockDividend:** `.github/workflows/deploy.yml` (blob `6f79abf071fc5279631a32fda63e1bbff6137aae`) gates production publication behind `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`, requires master, publishes full-source-SHA tags and verifies linux/arm64 manifests plus registry digests for Admin/Backend. The reviewed current workflow contains no Platform dispatch; Stock remains app-owned CI/publication only.
- **Media Generation:** `.github/workflows/wf-03-media-production-deploy.yml` (blob `f39c799bf82fd666ade5c50e92d0b94b7151194c`) resolves a full-SHA release tag, verifies exact build artifacts/checksums, publishes the two ARM64 images, resolves immutable registry digests, and explicitly records that Platform deployment is not configured and no repository dispatch is sent.
- **Ownership result:** Platform receiver event types retain TCE, Auth and MicroFE promotion paths; no Stock/Media production handoff was found in the reviewed current app workflows. No competing app-owned SSH/Compose/kubectl apply path was introduced. Preserve app CI, image publishers and manual/release gates.
- **Evidence limitation:** this audit validates sender/receiver source contracts only. It does not establish a fresh TCE/Auth/Stock/Media publisher run, registry digest, provenance attestation, release authorization or production promotion. Latest publisher evidence remains historical as recorded in the deployment tracker; do not promote from this source audit alone.


## Cross-repo deployment checkpoint — 2026-11-06 11:20 ICT / 04:20 UTC

- **Verified default-branch heads:** Platform Infra `5d1ba54b17827f6e423c275f1854fbb7945af50d`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `6fcefa6b3792dab92b6d5c438001633d25f1ca28`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1314 (draft mail-service plan; validate check PASS on head `db152c9a17416d1a7f82165597dfe478321bd055`), #544/#541/#539 (old Keycloak drafts; checks from 2026-10-14, not fresh). Authentication #75 (ready) and #76 (draft); their validate checks pass on old heads, but Supabase Preview is SKIPPED on both and the branches are stale relative to master. No open PRs in TCE, StockDividend or Media Generation. Do not merge unrelated drafts as deployment work.
- **Platform PR/check evidence:** PR #1316 is merged; exact-head validation #42160559268 and post-merge validation #42160625527 PASS. Current open #1314 validation #42161859747 PASS. Latest Platform master validations include #42160625527 PASS. No current failing required check was found on the latest merged deployment-contract change.
- **Native Platform schedule evidence:** latest returned native scheduled reconcile #42152655025 PASS at 02:48:33Z; recovery controller #42152661024 PASS at 02:48:36Z; schedule watchdog #42152865619 PASS at 02:50:36Z. Latest native scheduled inspect #42145981473 PASS at 01:45:56Z. No later native scheduled Platform run appears in the current Actions event-filtered history. The later inspection #42154756357 is workflow_dispatch, not native schedule evidence. At this checkpoint native inspect is about 154m old; native reconcile/watchdog are about 92m/90m old. The last manual reconcile #42158234979 PASS at 03:43:16Z used pre-current master SHA `2b61b197b564f61bc60aa44f574c3435c0dd9bb1`, `mode=apply`, and `ALLOW_IMAGE_CHANGES=false`; it is not a native scheduled run and did not promote images. TCE heartbeat dispatch #42158219469 and recovery #42158367029 completed successfully.
- **Latest K3s snapshot:** inspect workflow_dispatch #42154756357 completed at 03:09:08Z; `debug/vps-latest.md` generated 03:09:17Z (blob `3e21c197b82f1c14d662e68664bbd0ab1594b378`). Snapshot age is about 71m here; use only as a recent-but-not-live observation, not destructive authorization. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, GitOps drift clean. Media backend/frontend 1/1 and digest-pinned. Stock Admin (two Pods) and new Backend are ImagePullBackOff because the deployed `12d63b4` images have no matching ARM64 manifest; legacy Backend/Frontend remain Running. TCE/Auth/Keycloak are 0/0. The snapshot's persistent-storage section showed only the unrelated `k3s-debug` PVC/PV; this is not a same-window pre-delete inventory.
- **TCE Dashboard:** WF-12 native schedule #42158209117 failed because latest scheduled WF-06 #42133793538 was 221m old. WF-13 #42158228852 successfully dispatched read-only fallback WF-06 #42158243093, but the fallback failed all four strict public probes with HTTP 503. The snapshot shows TCE/Auth desired replicas 0/0, consistent with the 503s. Keep HTTP 200 expectations and current desired replicas; do not turn the fallback into native schedule evidence. TCE market-scan schedule remains untouched.
- **StockDividend:** master CI #42137523269 PASS. Latest verified immutable publisher remains #41563856933 (2026-11-03); it is historical and does not prove a fresh digest/provenance or release authorization. No production promotion. Keep Stock app CI/publisher ownership; do not promote while its production retirement is pending and the deployed ARM64 manifest is invalid.
- **Media Generation:** master CI #42136991059 PASS. Backend/frontend remain digest-pinned and 1/1 in the snapshot. Dedicated Media runner remains systemd active/enabled with `Runner.Listener` present. PR #1313's guard is preventive; it does not stop, disable or unregister the runner.
- **Authentication:** latest master service CI #41670642852 PASS but historical (2026-11-03). PR #75 validate PASS / Supabase Preview SKIPPED; PR #76 validate PASS / Supabase Preview SKIPPED. Keep both gated pending fresh exact-head checks and authoritative Supabase integration side-effect evidence. Runtime is 0/0; public health is 503. No activation or release.
- **Decommission gate:** `.github/workflows/decommission-stock-media.yml` has not run. It remains manual-only, protected by production Environment approval, typed namespace/data-retention/runner confirmations, runner-retirement guard and fresh PVC/PV preflight. The current runner state fails the guard. The snapshot is not sufficient to approve deletion. Do not delete namespaces, PVC/PV, external databases/object storage, DNS, GHCR packages, app repos or source code.
- **Ownership and safety:** app repos own tests/builds and immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only routine production apply authority; `inspect-vps.yml` remains read-only. Preserve useful CI/security/manual/release/scheduled workflows and avoid SSH/Compose deployment paths. No image/manifest/secret/replica/host/storage/DNS/database/runner mutation occurred in this checkpoint. TCE market-scan schedule unchanged.

### Next dependency-safe actions

1. Obtain operator confirmation that the dedicated Media runner is idle; stop and disable only `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`, unregister it from the Media repository, and verify no Listener remains. Never touch the shared Platform runner.
2. Obtain a fresh same-window read-only inspection and independent backup/external-data/DNS ownership review. Only then consider the protected manual namespace-decommission workflow.
3. Investigate the missing native Platform scheduled ticks and TCE WF-06 schedule delivery without relaxing freshness thresholds or changing the TCE market-scan schedule.
4. Keep Stock promotion blocked until a new ARM64-capable immutable publication, verified digest/provenance and explicit release authorization exist; keep Auth PRs gated until Supabase side effects are evidenced.


## Runtime inventory update — 2026-11-06 13:58 ICT / 06:58 UTC

### Current branch and PR inventory

| Repository | Default branch SHA | Open PRs | Latest relevant workflow evidence |
|---|---|---|---|
| Platform Infra | `f29465020b25e1b2f5318733b5918e2d3e8a582b` | #1314 draft; #544/#541/#539 drafts | Reconcile #42176253693 SUCCESS; inspect #42176445915 SUCCESS and committed as PR #1324. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 native schedule #42176208184 delivered but HTTP probes failed; WF-12 #42176769424 freshness and heartbeat PASS; WF-13 #42176787185 skipped. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | CI #42167088130 PASS; publisher #41563856933 is the last observed successful publication (Nov 3). |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI #42136991059 PASS (historical); no newer publisher. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | CI #42167100692 PASS; Supabase Preview SKIPPED; no release run. |

### Workflow ownership and publication contract

- **Platform Infra:** sole production apply authority is `.github/workflows/reconcile-vps.yml`. Read-only inspection is `.github/workflows/inspect-vps.yml`. Production reconcile #42176253693 completed SUCCESS on pre-inspection SHA `8d33b984cee5fa5dd8fbd2172a4ddc899d16bb6f`; its shared reconcile, pull access, Auth runtime Secret, MicroFE/Auth/TCE lanes and final gate passed; Keycloak was skipped. No new image promotion was evidenced.
- **TCE Dashboard:** WF-06 keeps cron `*/15 * * * *` and requires HTTP 200 for TCE web/API and Auth liveness/readiness. Native schedule #42176208184 was delivered at 06:43:04Z but all four probes failed HTTP 503. WF-12 #42176769424 verified latest WF-06 schedule freshness successfully after WF-07 #42176751608 and sent the Platform heartbeat successfully. WF-13 #42176787185 was skipped because schedule freshness was no longer stale. Treat schedule delivery and endpoint health as separate signals. Do not change market-scan schedules.
- **StockDividend:** app-owned `deploy.yml` publishes ARM64 scraper/admin/backend images on qualifying master source pushes, tags each with the full source SHA and verifies GHCR digest plus ARM64 manifest. Manual publication requires `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`; no Platform dispatch is sent. Master CI ARM64 builds use `push: false` and are not publication evidence.
- **Media Generation:** app-owned WF-03 validates stable version plus full source SHA, builds native ARM64 images, transfers checksum-verified artifacts, publishes to GHCR, then verifies registry digest and ARM64. It sends no Platform dispatch. No current release run was observed.
- **Authentication:** app-owned release.yml is manual-only. It validates release metadata, builds ARM64 with Buildx provenance/SBOM, verifies SHA/version tags map to one digest, and dispatches `auth_digest`, source run ID, workflow path, event and full source SHA to Platform. No publisher run was observed; CI's ARM64 job is non-publishing.
- Preserve all useful app CI, test, security, manual and release workflows. No duplicate direct SSH/Compose production authority was identified in the inspected release paths.

### Latest K3s state — read-only snapshot #42176445915

Generated 2026-11-06T06:45:26Z; current master snapshot commit `f29465020b25e1b2f5318733b5918e2d3e8a582b`.

- Node Ready, ARM64, K3s v1.36.3+k3s1; disk 56%, ~19 GiB available RAM, restart_required=yes. No reboot/upgrade authorization.
- Media backend/frontend 1/1 Running with digest-pinned images. Media runner service active/enabled and Listener process present; retirement remains blocked.
- Stock namespace Active; Admin (two Pods) and new Backend ImagePullBackOff due missing ARM64 manifest on `12d63b4`; legacy Backend/Frontend 1/1.
- TCE frontend/service and Auth/Keycloak desired 0/0.
- Only PVC/PV listed is `k3s-debug/k3s-debug-logs`; no Stock/Media PVC/PV or VolumeSnapshot references. External backup/data/DNS ownership is not proven.

### Exact open gates

1. No TCE/Auth replica activation without service-owner authorization; keep HTTP 200 probes strict.
2. No Stock manual publisher dispatch without explicit release authorization; no promotion of the invalid `12d63b4` images.
3. No Media runner retirement until operator verifies idle, stopped, disabled and unregistered state.
4. No Stock/Media namespace deletion until fresh same-window preflight and independent backup/external-data/DNS review pass.
5. Auth #75 remains open because the connected Supabase GitHub integration is configured Deploy-to-production ON for master and merge-trigger side effects are unresolved; #76 remains draft.

### Schedule classification

The successful WF-12 run #42176769424 was triggered by a WF-07 `workflow_run`, not a native WF-12 schedule tick. Its internal WF-06 freshness check passed against the latest native WF-06 run #42176208184. WF-13 and Platform watchdog/recovery `workflow_run` events that were skipped are not native scheduled runs. Do not use workflow_dispatch, repository_dispatch or workflow_run as substitutes for native scheduled-run evidence.


## Runtime workflow inventory — 2026-11-06 15:03 ICT / 08:03 UTC

This entry supersedes the 13:58 ICT schedule/readiness classification wherever newer Actions history is available.

### Current workflow ownership and default-branch heads

| Repository | Default-branch SHA | Latest CI evidence | Deployment/publication ownership |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `6687e665f1d62cbe97cff757b63ef7b1b154b4ee` | `validate` PASS #42178567534 | Sole production manifests, shared GHCR pull Secret, digest/provenance receiver, GitOps promotion/reconcile, rollout and health owner. `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only. |
| `phanthienquoc/TCE-dashboard` | `512b69d837e2a65c39867a062529a7fa0eada4cc` | WF-06 schedule #42176208184 failed public HTTP probes; WF-07 schedule #42176751608 passed; WF-12 workflow_run #42176769424 passed freshness at 06:48Z | App CI/tests and TCE release publisher own source build and immutable image request. Platform validates source run, full SHA, digests and ARM64 before promotion. |
| `phanthienquoc/stockdividend` | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | CI #42167088130: 7/7 checks PASS, including build-only ARM64 and release-hold | Stock owns CI and GHCR publication; manual publisher remains gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`. No Platform production dispatch. |
| `phanthienquoc/media-generation` | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | CI #42136991059 PASS (historical) | Media owns build, checksum-verified artifacts, full-SHA tag, GHCR digest and ARM64 verification. No Platform production dispatch. |
| `phanthienquoc/phanthienquoc-authentication` | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | CI #42167100692: validation/build PASS; Supabase Preview SKIPPED | Auth owns manual-only release publisher with Buildx provenance/SBOM and digest handoff. Platform owns digest validation and GitOps promotion. |

### Open PR and check inventory

- Platform Infra: #1314 draft (mail-service documentation, unrelated to deployment; validation passed on old head); #544/#541/#539 remain old Keycloak drafts. No deployment PR is open.
- TCE Dashboard: no open PR.
- StockDividend: no open PR.
- Media Generation: no open PR.
- Authentication: #75 ready (validation passed 2026-10-27, Supabase Preview skipped); #76 draft (validation passed 2026-11-01, Supabase Preview skipped). Both branches have stale base commits. Neither is authorized for merge/release.

### Native schedule delivery evidence (UTC)

| Workflow | Latest native scheduled run | Conclusion | Current interpretation |
|---|---|---|---|
| Platform reconcile-vps | #42152655025, 02:48:33 | SUCCESS | No later native scheduled run observed by 08:03Z. |
| Platform recovery | #42152661024, 02:48:36 | SUCCESS | Later #42176781772 was repository_dispatch, not schedule. |
| Platform schedule watchdog | #42152865619, 02:50:36 | SUCCESS | No later native scheduled watchdog observed. |
| Platform inspect-vps | #42145981473, 01:45:56 | SUCCESS | Latest snapshot refresh #42176445915 was workflow_dispatch, not schedule. |
| TCE WF-06 | #42176208184, 06:43:04 | FAILURE | Four strict public endpoint probes returned HTTP 503; no later native WF-06 schedule by 08:03Z (age ~81m, budget 25m). |
| TCE WF-07 integration | #42176751608, 06:48:12 | SUCCESS | No later native scheduled integration run observed by 08:03Z. |
| TCE WF-12 watchdog | #42158209117, 03:43:01 | FAILURE | #42176769424 at 06:48:22 was a workflow_run after WF-07; it passed freshness at that time but is not a native schedule. |

The relevant YAML schedule declarations remain present: Platform reconcile `7,22,37,52`, inspect `2,32`, schedule watchdog `12,27,42,57`, recovery `10,25,40,55`; TCE WF-06 `*/15` and WF-12 `7,22,37,52`. The observed gap is in native event history, not a proposed cron change. Read-only evidence cannot determine whether the gap is GitHub scheduler delivery delay or a workflow/repository Actions setting. Do not count workflow_run, repository_dispatch or workflow_dispatch as native schedule evidence.

### Runtime snapshot freshness and release gates

- Latest K3s snapshot remains inspect-vps #42176445915, generated 06:45:26Z; age ~78m at this checkpoint. It records Media 1/1 Running, Stock Admin/new Backend ImagePullBackOff due missing ARM64 manifest on `12d63b4`, TCE/Auth/Keycloak 0/0, and the dedicated Media runner active/enabled with `Runner.Listener` present.
- Snapshot lists no Stock/Media PVC/PV or VolumeSnapshot references; external database/object-storage backups and DNS/data-retention ownership are not established.
- Stock CI ARM64 checks use non-publishing builds; latest known publisher #41563856933 is from 2026-11-03. No new digest/provenance or release authorization.
- Media master CI is historical; no newer publisher run.
- Auth master CI includes non-publishing ARM64 build; Supabase Preview skipped; no release publisher/digest.
- TCE health failure (HTTP 503) is consistent with the snapshot's desired 0/0 replicas. Keep HTTP 200 assertions strict and do not activate without owner approval.
- Media runner guard must remain fail-closed until the dedicated runner is idle, stopped, disabled, unregistered and Listener-free. Never retire the shared Platform runner.

Preserve useful app CI/tests/builds, immutable publishers, security checks, purposeful manual/release/scheduled jobs, and Platform reconciliation/recovery/inspection. No duplicate SSH/Compose production apply authority was introduced. No cron, image, manifest, Secret, replica, namespace, storage, DNS, runner or host change occurred. TCE market-scan schedule unchanged.


## Runtime workflow inventory — 2026-11-06 16:03 ICT / 09:03 UTC

- Default branch heads were re-read: Platform Infra `f62f8a8c457cce12a9286efa246f6279129c8bab`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `3aeaf519b7a786d13dcecee763acaca357c47ddd`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `3a8031196f21c4240b617bbd0a623fce2dc56c5e`.
- Open PRs: Platform #1314/#544/#541/#539 (draft); Auth #75 (ready)/#76 (draft); no TCE/Stock/Media PRs. Exact PR-head run retrieval returned successful historical validation/CI runs for these six PRs; all bases are stale and none is approved for merge by this checkpoint.
- The connected GitHub run reader returned no default-branch workflow-run/status records. Its commit-run query is limited to PR-triggered runs; therefore the latest repo-wide schedule/reconcile evidence remains the 15:03 ICT checkpoint and must be treated as stale, not current. Do not infer that no scheduled runs occurred.
- TCE workflow source re-check: WF-06 remains `*/15 * * * *` with strict HTTP 200 probes; WF-12 remains `7,22,37,52 * * * *` and only forwards verified native schedule heartbeats; WF-13 is workflow_run-only read-only fallback and cannot satisfy schedule freshness. Platform reconcile watchdog remains `12,27,42,57 * * * *`. No cron or TCE market-scan schedule change.
- Last known Platform reconcile #42176253693 was manual and successful with image changes disabled; last known inspection #42176445915 generated 06:45:26Z and is ~2h18m old. Last known TCE WF-06 #42176208184 failed four 503 probes; WF-07 #42176751608 passed; WF-12 #42176769424 was workflow_run, not native schedule. No newer event conclusion is claimed.
- Last snapshot still recorded Stock Admin/new Backend ARM64 pull failure on `12d63b4`, Media 1/1, TCE/Auth/Keycloak 0/0, and dedicated Media runner active/enabled with Listener. External backup/data/DNS ownership remains unverified. No fresh publisher/digest/provenance or release authorization was retrieved.
- Ownership remains app-owned CI/build/immutable GHCR publication and Platform-owned production manifests, shared pull credentials, digest/provenance validation, GitOps reconcile, rollout and health. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only. No production mutation; TCE market-scan unchanged.
- Full evidence and next actions: [checkpoint 2026-11-06 16:03 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-06-1603-ict.md).
