## Current review — 2026-11-06 10:21 ICT (2026-11-06 03:21 UTC)

Incremental cross-repository update after Platform PR #1311. This checkpoint records the latest exact heads, workflow outcomes and the current fail-closed Stock/Media retirement gate. It does not authorize a production release or destructive cluster action.

### Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Current state |
|---|---|---|---|
| Platform Infra | `40db4f6378d7f9cf21d830100fe0548e2197cc65` | #544/#541/#539 (draft) | PR #1310 runner guard and PR #1311 readiness documentation merged. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | App CI/workflow state unchanged; no production publisher dispatched. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | CI passed; immutable publisher remains separate and no new release was requested. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI passed; no production release or Platform handoff remains. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready / #76 draft | CI head is historical; Supabase integration/migration gates remain unresolved. |

### Latest workflow evidence

- Platform master validation [#42156021306](https://github.com/phanthienquoc/platform-infra/actions/runs/42156021306) completed SUCCESS on exact head `40db4f6378d7f9cf21d830100fe0548e2197cc65`. The run validated manifest rendering, immutable image policy, Auth digest contract, shell scripts and secret/network boundaries.
- The latest production reconcile [#42155789344](https://github.com/phanthienquoc/platform-infra/actions/runs/42155789344) completed SUCCESS on `a75980906ddec00c84dc64112fa87835906a6569`: MicroFE, Auth and TCE lanes passed; Keycloak was skipped; final gate and inspection-recovery trigger passed. This is evidence for that run/head, not a fresh rollout after the later docs-only PR #1311.
- TCE native WF-06 [#42133793538](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133793538) failed all four public probes with HTTP 503 (TCE web/API and Auth liveness/readiness). WF-12 [#42133822319](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133822319) passed and WF-13 [#42133822204](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133822204) completed its read-only fallback successfully; subsequent WF-13 [#42133843652](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133843652) was skipped for a successful watchdog source. This is healthcheck evidence, not a production rollout. TCE market-scan schedule and all cron declarations remain untouched.
- StockDividend CI [#42137523269](https://github.com/phanthienquoc/stockdividend/actions/runs/42137523269) and Media CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) passed. Authentication CI [#41670642852](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852) passed on 2026-11-03; no newer Auth publisher run was observed.
- No new TCE, StockDividend, Media or Auth production publisher was dispatched. App CI success is not release authorization. TCE/Auth GitOps still use legacy tags; digest promotion requires a new exact publisher run, registry-confirmed digest/provenance and the normal Platform promotion path. Routine reconcile keeps image changes disabled.

### Stock/Media K3s decommission gate

- The latest committed read-only snapshot [inspect-vps #42154756357](https://github.com/phanthienquoc/platform-infra/actions/runs/42154756357) was generated at 2026-11-06T03:09:17Z. It shows the dedicated Media runner systemd service active and a Media `Runner.Listener` process; Media backend/frontend remain 1/1 Running. Stock Admin and the newer Backend remain ImagePullBackOff; the older Backend and Frontend remain 1/1. The snapshot reports no PVC/PV claims in `stock-prod` or `media-prod`, but the manual workflow must repeat the storage preflight in the same maintenance window.
- Platform PR [#1310](https://github.com/phanthienquoc/platform-infra/pull/1310) added a fail-closed check requiring the dedicated Media service to be inactive and its Listener process absent. The protected workflow also requires typed backup/external-data and runner-retirement attestations. It does not stop or unregister the runner.
- The manual `decommission-stock-media` workflow has not run. With the observed runner state, it must abort before namespace deletion. The service owner must first confirm no active job, stop the dedicated Media runner and unregister it from the Media repository. Do not stop the shared Platform runner.
- Do not delete PVs, external databases/object storage, DNS, GHCR packages, application repositories or source code. Do not change TCE/Auth desired replicas, production images, Keycloak or TCE market-scan schedules.

### Next dependency-safe actions

1. Obtain a new read-only VPS inspection after the Media runner is safely retired; repeat namespaced-object, PVC/PV and StorageClass preflight immediately before any deletion.
2. Require the service owner’s backup/external-data review and GitHub runner-unregistration confirmation before using the protected manual workflow.
3. Keep TCE/Auth digest promotion gated on an authorized, successful exact-source publisher run and registry digest verification; do not infer or reuse a historical digest.
4. Investigate the TCE/Auth public HTTP 503 health probes against the intentionally zero-replica state without changing any market-scan cron declaration.

`reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No K3s namespace, PV, DNS, external database, production image, desired replica count or schedule was changed in this checkpoint.

---

Last reviewed: 2026-11-06 10:18 ICT (2026-11-06 03:18 UTC)

## Current review — 2026-11-06 10:18 ICT (2026-11-06 03:18 UTC)

Incremental update to the 10:10 checkpoint below. Platform master is now `a75980906ddec00c84dc64112fa87835906a6569` after PR #1310; the four app-repository heads and their open-PR state are unchanged.

- Platform PR [#1310](https://github.com/phanthienquoc/platform-infra/pull/1310) adds a fail-closed guard to the manual Stock/Media namespace workflow. Before storage preflight or deletion it checks that the exact dedicated Media systemd service is inactive and that no `/opt/media-actions-runner/bin/Runner.Listener` process remains. GitHub runner unregistration remains a required operator attestation; the guard does not claim to verify the GitHub registration.
- Exact PR head `b32b75e4923d9f59ec8a8cc823828e7f5c2c6ba2` passed `validate-github-actions` [#42155669711](https://github.com/phanthienquoc/platform-infra/actions/runs/42155669711) and `validate-manifests` [#42155669700](https://github.com/phanthienquoc/platform-infra/actions/runs/42155669700); PR #1310 was squash-merged as `a75980906ddec00c84dc64112fa87835906a6569`.
- The latest read-only inspection snapshot #1308 (2026-11-06T03:09:17Z) still shows the Media runner service active. Therefore, the new guard would currently stop the manual decommission workflow before namespace deletion. It does not stop or unregister the runner.
- The same snapshot shows only the `k3s-debug` PVC/PV claim and no target-namespace PVC/PV claims. The workflow will still repeat its same-window storage preflight; backup/external-data review and runner retirement remain mandatory.
- Stock/Media namespaces, Services, Ingresses and workloads remain in K3s. Media backend/frontend are 1/1; Stock Admin and the newer Backend remain ImagePullBackOff because their ARM64 image manifests are unavailable; older Stock Backend and legacy Frontend remain 1/1. No workload or namespace was deleted.
- TCE and Auth still use legacy production tags in GitOps. No new publisher release or digest promotion was initiated. TCE schedule and all cron declarations remain unchanged.

Next action: the service owner must review backups/external-data ownership, stop the dedicated Media runner when idle, unregister it from the Media repository, and then use the protected manual workflow with its exact typed confirmations. Do not remove the shared Platform runner or delete PV/external data/DNS/GHCR packages.

---


## Current review — 2026-11-06 10:10 ICT (2026-11-06 03:10 UTC)

This checkpoint follows the successful merge of Platform PR #1307. It records current repository heads, exact-head validation, the remaining digest-promotion and K3s decommission gates, and the latest live cluster evidence retrieved in this pass.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `221d928575a9d9999827fcce5625f2cc06c9f9c6` | #544/#541/#539 drafts | PR #1307 merged; TCE source publisher job/step provenance is now enforced. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; WF-02 and WF-05 checks passed. No production release dispatched. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 removed the retired Platform handoff; CI passed. Publisher remains build/publish-only. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 removed the retired Platform handoff; CI passed. Publisher remains build/publish-only. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | PR #87 established digest/provenance handoff; #75/#76 remain gated on Supabase integration and migration review. |

### Exact workflow and merge evidence

- Platform PR [#1307](https://github.com/phanthienquoc/platform-infra/pull/1307) strengthened `verify-tce-publisher-run.sh`: a successful top-level TCE Actions run is no longer sufficient. The verifier now requires the exact release dependency jobs, native ARM64 frontend/backend build and artifact-integrity steps, GHCR publication, registry digest/ARM64 verification, and Platform dispatch correlation to be completed-success.
- Exact PR head `248802e05fa397b37d573749bf75be8bc57e2e45` passed `validate-github-actions` [#42154577734](https://github.com/phanthienquoc/platform-infra/actions/runs/42154577734) and `validate-manifests` [#42154577576](https://github.com/phanthienquoc/platform-infra/actions/runs/42154577576). PR #1307 was squash-merged as `67e8d8746934ec40b60b0fe0f62c5e4b3bcccfc2`.
- Platform inspection-only PR [#1308](https://github.com/phanthienquoc/platform-infra/pull/1308) refreshed the read-only K3s/storage snapshot at 2026-11-06T03:09:17Z; no production manifests were changed. Platform production reconcile [#42150629183](https://github.com/phanthienquoc/platform-infra/actions/runs/42150629183) completed SUCCESS: policy v15 verified, scope `all`, mode `apply`, `ALLOW_IMAGE_CHANGES=false`; MicroFE, TCE and Auth lanes passed, Keycloak lane skipped, and post-apply GitOps drift was clean. Recovery controller [#42150853420](https://github.com/phanthienquoc/platform-infra/actions/runs/42150853420) also completed SUCCESS.
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


## Current review — 2026-11-06 09:33 ICT (2026-11-06 02:33 UTC)

This review follows the merge of Platform PR #1304 and the successful post-merge production reconciliation. It records verified CI, GitOps, credential and rollout evidence separately from the still-unfinished Stock/Media namespace decommission and image-digest migration work.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | d6f45057f4a7eaba4c81d897aa64d9e5feb67fa1 | #544/#541/#539 draft | PR #1304 merged; post-merge validations and reconcile passed. |
| TCE Dashboard | 512b69d837e2a65c39867a062529a7fa0eada4cc | None | CI/workflow state unchanged; strict public WF-06 still reports the documented zero-replica HTTP 503 condition. |
| StockDividend | 6fcefa6b3792dab92b6d5c438001633d25f1ca28 | None | Latest master CI #42137523269 passed; production publisher/release was not triggered. |
| Media Generation | 3a8846a4f273eeb20a55b214d5ad80804c2d8d52 | None | Latest master CI #42136991059 passed; production publisher/release was not triggered. |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft | Master CI #41670642852 passed; #75/#76 remain gated on Supabase integration side effects. |

### Platform PR #1304 and production reconciliation

- PR #1304 added scripts/resolve-push-deployment-scope.sh to the push paths for the sole production reconcile workflow, enforced that trigger in validate-workflow-contracts.py, and added a full changed-path regression fixture from the Stock/Media retirement.
- Exact PR head 29dffd589c800ef3e3a545be128182ace615718a passed all three visible checks: validate-github-actions #42149835243, keycloak-ci #42149835246 and validate-manifests #42149835326. GitHub accepted the squash merge with expected head SHA; merge commit is d6f45057f4a7eaba4c81d897aa64d9e5feb67fa1.
- Post-merge master checks on that exact commit passed: validate-github-actions #42150629257, keycloak-ci #42150629258 and validate-manifests #42150629301.
- Reconcile run #42150629183 completed SUCCESS on the merge commit. The push resolver produced scope all; mode was apply and ALLOW_IMAGE_CHANGES=false. GHCR pull-access validation, Auth runtime Secret provisioning, shared GHCR pull-credential reconciliation, blocked-image-pull restart checks and TCE release-pair validation passed.
- Preflight found Kubernetes drift. The image-change guard passed and reported no existing workload image replacement; production manifests applied successfully and post-apply GitOps drift verification was clean.
- MicroFE, TCE and Auth deployment lanes passed. Keycloak lane was skipped by the current all-scope contract. TCE and Auth health checks explicitly accepted their intentional zero-replica state; no replicas were restored. MicroFE Shell/WS rollout and health passed.
- Recovery controller #42150853420 completed SUCCESS for source reconciliation #42150629183.
- Non-blocking telemetry issue: "Publish TCE deployment started event" could not connect to 127.0.0.1:18080 (curl exit 7). The step is continue-on-error, so this did not invalidate the reconcile or rollout gates. Verify whether the local event bridge is expected to be running before relying on this notification.
- The reconcile's cluster listing still showed Media workloads running and Stock workloads present (including Stock Admin ImagePullBackOff and older Backend/Frontend pods). The GitOps retirement does not prune those resources; namespace deletion has not run.

### Cross-repository publication and dispatch boundary

- StockDividend master CI #42137523269 passed all six jobs, including backend test/build, admin build, scraper build/syntax and production release-hold contract. No production publication or Platform dispatch was triggered.
- Media Generation master CI #42136991059 passed its application test/build job. No production release was triggered and no Platform dispatch receiver remains.
- TCE WF-03 remains manual-only and validates the full source SHA, paired web/service registry digests, ARM64 manifests and the source run/workflow/event/SHA payload before dispatch. No TCE production publisher run was initiated.
- Authentication release.yml remains manual-only and sends source run ID, workflow path, event, full source SHA and registry digest. Platform validates publisher provenance before promotion. No Auth release was initiated.
- Platform remains the owner of production manifests, shared GHCR pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health. App repositories retain tests/builds/immutable GHCR publication. No duplicate SSH/Compose/app-owned Kubernetes deployment authority was added.

### Outstanding GitOps digest pinning gap

- The current TCE production Kustomize file still contains the legacy paired tag prod-v0.1.0-e75e338 (7-character source prefix), rather than registry digest references. The live TCE verification in reconcile #42150629183 confirmed desired/live tag pairing, not registry digest pinning.
- The current Auth Kustomize file likewise still uses legacy tag prod-v1.0.0-ceb2688. The new TCE/Auth publisher contracts produce full-source-SHA tags and registry digests, and Platform has digest-promotion helpers, but no new authorized publisher dispatch has converted these existing manifest references.
- Do not invent or reuse a cached digest as current registry evidence. Next safe action is to obtain registry-confirmed digests tied to successful publisher provenance, then create atomic TCE web/service and Auth digest-promotion PRs. Keep image changes disabled in routine reconciliation.

### TCE, Auth and decommission safety

- TCE native WF-06 #42133793538 failed four strict public HTTP 200 probes with HTTP 503 while TCE/Auth/Keycloak were intentionally at zero replicas. WF-13 fallback #42133822204 passed read-only. Do not weaken health gates, restore replicas or change any TCE schedule.
- Auth PR #75 validation evidence is historical; Supabase Preview is skipped and the connected production integration's merge-triggered migration effect is not authoritatively verified. Do not merge #75/#76, run migrations or publish an Auth release on current evidence.
- The latest committed read-only inspection remains run #42145981473, snapshot generated 2026-11-06T01:46:04Z. It is stale for destructive action and showed the dedicated Media runner service active. It showed only the k3s-debug PVC/PV claim, but that historical observation is not a same-window storage preflight.
- The manual-only decommission-stock-media workflow has no execution run. No Stock/Media namespace, PVC/PV, DNS, GHCR package, external database/object storage or runner registration was deleted. Before namespace deletion, obtain fresh storage inventory, confirm backups/external-data ownership and independently verify the dedicated Media runner is idle, stopped and unregistered. Do not remove the shared Platform runner.
- reconcile-vps.yml remains the sole routine production apply authority; inspect-vps.yml remains read-only. TCE market-scan schedule and all other TCE schedules are unchanged.

### Next actions

1. Obtain fresh read-only K3s/PVC/PV/StorageClass and runner evidence; only then consider the protected manual Stock/Media namespace workflow with its exact typed confirmations.
2. Obtain registry-confirmed full-SHA digest evidence for the currently deployed TCE and Auth images; promote the paired TCE digests and Auth digest atomically through Platform PRs.
3. Diagnose the optional local deployment-event bridge at 127.0.0.1:18080 without weakening rollout/health gates.
4. Keep Stock/Media production publication closed unless explicitly authorized; keep Auth #75/#76 gated on the Supabase production integration effect.
5. Preserve every TCE schedule, especially the market-scan schedule.

---

Last reviewed: 2026-11-06 09:15 ICT (2026-11-06 02:15 UTC)

## Current review — 2026-11-06 09:15 ICT (2026-11-06 02:15 UTC)

This review follows the successful merge of PR #1303 and closes the remaining trigger gap that prevented a new production reconciliation attempt.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `e66bdecea35eda2c6740587b87ff69415c4176fa` | #1304 open; #544/#541/#539 draft | #1301 and #1303 merged; #1296 closed as superseded. #1304 adds the resolver to the sole production reconcile push filter. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Strict public health probes still return 503 while TCE/Auth/Keycloak remain operator-scaled to zero. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 merged; latest master CI #42137523269 passed. Production publication remains untriggered. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged; latest master CI #42136991059 passed. Production publication remains untriggered. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 passed. PR #75 validation passed, but Supabase Preview is skipped and the production integration side-effect gate remains unresolved. |

### Platform retirement, push-scope fix and remaining trigger gap

- Platform PR #1301 was squash-merged as `d05f806c636f3e785ffe603efff204767308efa0`; its exact-head manifest, GitHub Actions and Keycloak checks passed. PR #1296 was closed as superseded. The merge removed Stock/Media GitOps ownership but did not delete namespaces or persistent/external data.
- Post-merge reconcile #42146800843 failed before preflight or any cluster mutation because the push-scope resolver rejected deleted `scripts/bootstrap-media-runner.sh`. The failed run skipped GHCR credential bootstrap, manifest apply, rollout and app lanes.
- PR #1303 fixed the resolver classifications and regression tests, refreshed this tracker/inventory, and was squash-merged at `e66bdecea35eda2c6740587b87ff69415c4176fa`. Exact final-head checks passed: `validate-github-actions` #42148684639 and `validate-manifests` #42148684820.
- A follow-up inspection of `reconcile-vps.yml` showed its push path filter did not include `scripts/resolve-push-deployment-scope.sh`; therefore merging #1303 alone did not create another reconcile run. No new production reconcile was dispatched or applied after #1303.
- PR [#1304](https://github.com/phanthienquoc/platform-infra/pull/1304) adds the resolver to the push filter, makes `validate-workflow-contracts.py` enforce that trigger, and adds a full changed-path fixture from PR #1301. Its merge is intentionally expected to trigger the existing `reconcile-vps` workflow with scope `all`, mode `apply`, and `allow_image_changes=false`, subject to the protected production Environment approval and strict health gates. Its exact-head checks are pending; do not merge until they pass.

### App-owned publication and dispatch boundaries

- StockDividend `deploy.yml` retains app-owned CI/build/publication, immutable full-source-SHA image tags, registry digest resolution, ARM64 checks and the explicit manual publication hold. It contains no Platform repository-dispatch handoff.
- Media Generation `wf-03-media-production-deploy.yml` retains immutable full-source-SHA tags and paired registry digest/ARM64 verification. It contains no Platform repository-dispatch handoff.
- TCE WF-03 remains manual-only for production, verifies the full-source-SHA web/service digest pair and ARM64 manifests, and validates `tce-release-requested` source provenance before Platform promotion.
- Authentication `release.yml` remains manual-only and sends the Auth digest with source run ID, workflow path, event and full source SHA. Platform validates that provenance and the registry digest before updating Auth GitOps. No TCE/Auth release workflow was dispatched.

### TCE, Authentication and runtime safety

- TCE native WF-06 #42133793538 failed all four strict public HTTP 200 probes with HTTP 503 while TCE/Auth/Keycloak remain operator-scaled to zero. WF-13 fallback #42133822204 passed read-only. Do not weaken health gates, restore replicas or change any TCE schedule; the market-scan schedule is unchanged.
- Auth PR #75 remains gated because Supabase Preview is `SKIPPED` and the connected production integration's merge-triggered migration effect is not authoritatively verified. Do not merge #75/#76, run migrations or dispatch an Auth release on current evidence.
- `decommission-stock-media.yml` is manual-only and has no execution runs. Its protected production Environment, three exact confirmations and fresh storage preflight do not replace independent backup/external-data and dedicated-runner checks. The last committed VPS snapshot is stale and lacks fresh PVC/PV/StorageClass inventory.
- `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority, K3s namespace/PV/DNS/GHCR/external-data mutation, credential rotation, image promotion or schedule change occurred.

### Next actions

1. Poll PR #1304's exact current head; squash-merge only after all required checks pass.
2. Verify the merge-triggered `reconcile-vps` push run reaches fresh preflight, resolves scope `all`, and reports rollout/health truthfully. Keep image changes disabled.
3. Obtain fresh read-only K3s/PVC/PV/StorageClass evidence, confirm backups/external-data ownership and independently retire the dedicated Media runner before considering manual namespace deletion.
4. Keep Stock production publication closed without explicit release authorization and Auth #75/#76 gated on the Supabase integration side-effect question.
5. Preserve all TCE schedules, especially the market-scan schedule.

---

Last reviewed: 2026-11-06 09:10 ICT (2026-11-06 02:10 UTC)

## Current review — 2026-11-06 09:10 ICT (2026-11-06 02:10 UTC)

This review follows the StockDividend/Media GitOps retirement merge, inspects the five repository heads and active PRs, and records the first post-merge reconciliation regression plus its dedicated fix.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `d05f806c636f3e785ffe603efff204767308efa0` | #1303 open; #544/#541/#539 draft | #1301 merged; #1296 closed as superseded. #1303 fixes the post-merge push-scope regression. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Strict public health probes still return 503 while TCE/Auth/Keycloak remain operator-scaled to zero. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 merged; latest master CI #42137523269 passed. No production publisher run or release promotion was triggered. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged; latest master CI #42136991059 passed. No production publisher run or release promotion was triggered. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 passed. PR #75 validation passed, but Supabase Preview is skipped and the production integration side-effect gate remains unresolved. |

### Platform retirement merge and reconciliation regression

- Platform PR [#1301](https://github.com/phanthienquoc/platform-infra/pull/1301) was squash-merged as `d05f806c636f3e785ffe603efff204767308efa0` from exact head `1e2f1d75009e5f79ef856b52f2b3ea7cc5cee545`. Exact-head `validate-github-actions` #42146647078, `validate-manifests` #42146647030 and `keycloak-ci` #42146647019 passed. Superseded plan-only PR #1296 was closed.
- The merge removed the StockDividend/Media manifest trees and their Platform reconcile, health, recovery, GHCR and publisher contracts. It added the manually invoked `decommission-stock-media` workflow. It did not delete K3s namespaces, PVs, DNS, GHCR packages, external data or runner registrations.
- Post-merge push reconciliation #42146800843 failed at `Resolve push deployment scope` because the resolver did not classify the deleted `scripts/bootstrap-media-runner.sh`. The job stopped before preflight, credential bootstrap, manifest apply, rollout or application lanes; no cluster mutation occurred. The accompanying Platform manifest validation #42146800900, GitHub Actions validation #42146800878, Keycloak CI #42146800876 and runner bootstrap #42146800844 passed.
- PR [#1303](https://github.com/phanthienquoc/platform-infra/pull/1303) updates the resolver and its regression tests. It treats retired/manual-only helper and validator-only paths as non-deploying, keeps the shared GHCR pull-access validator and production manifest/health paths cluster-wide, and makes a change to the resolver itself resolve to `all` so the merge can trigger a safe reconciliation attempt.
- The resolver's code-only revision passed exact-head `validate-github-actions` #42148457914 and `validate-manifests` #42148457910. The tracker/inventory update is included in the same PR, so checks must be re-read on the final updated head before merge.

### App-owned publication and dispatch boundaries

- StockDividend `deploy.yml` retains app-owned CI/build/publication, immutable full-source-SHA image tags, registry digest resolution and ARM64 checks, plus the explicit manual publication hold. The merged workflow no longer contains a Platform repository-dispatch handoff.
- Media Generation `wf-03-media-production-deploy.yml` retains app-owned image publication with full-source-SHA tags and paired registry digest/ARM64 verification. The merged workflow no longer dispatches Platform.
- TCE WF-03 remains manual-only for production release, uses full-source-SHA tags, verifies the web/service digest pair and ARM64 manifests, and validates the `tce-release-requested` payload before dispatching Platform. Platform's receiver validates source run/workflow/event/SHA, digest formats and tag-to-digest correlation before creating an atomic promotion PR.
- Authentication `release.yml` remains manual-only and sends the Auth digest with source run ID, workflow path, event and full source SHA. Platform validates that provenance and the digest before updating the Auth GitOps reference. No TCE/Auth release workflow was dispatched in this review.

### TCE, Authentication and runtime safety

- TCE native WF-06 #42133793538 failed all four strict public HTTP 200 probes with HTTP 503 (Auth liveness/readiness and TCE API/web). This matches the operator-requested zero-replica state. WF-13 fallback #42133822204 passed as a read-only recovery path. Do not weaken HTTP 200 gates, restore replicas, or change any TCE schedule; the market-scan schedule is unchanged.
- Auth PR #75 remains gated: its validation check passed, but Supabase Preview is `SKIPPED` and the connected production integration's merge-triggered migration effect is not authoritatively verified. Do not merge #75/#76, run migrations or dispatch an Auth release on current evidence.
- `decommission-stock-media.yml` is manual-only, requires the protected production Environment and three exact confirmations, and has no execution runs. The last committed VPS snapshot is stale and lacks fresh PVC/PV/StorageClass inventory. The dedicated Media runner's current state is unverified. Do not dispatch namespace deletion until a same-window inventory, backup/external-data review and idle/stopped/unregistered runner confirmation are complete.
- `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority was added. No K3s, credential, image, DNS, PV, database, object-storage or schedule mutation was performed.

### Next actions

1. Poll PR #1303's exact current head after the tracker update; squash-merge only if all required checks pass on that head.
2. Verify the merge-triggered push reconciliation now resolves to `all`; inspect its preflight and lane results. Keep the zero-replica health failures explicit rather than weakening health gates.
3. Obtain a fresh read-only K3s/storage inventory, confirm backups/external-data ownership and independently retire the dedicated Media runner before considering the manual namespace workflow.
4. Keep Stock production publication/promotion closed without explicit release authorization; keep Auth #75/#76 gated on the Supabase integration side-effect question.
5. Preserve all TCE schedules, especially the market-scan schedule.

---

Last reviewed: 2026-11-06 08:38 ICT (2026-11-06 01:38 UTC)

## Current review — 2026-11-06 08:38 ICT (2026-11-06 01:38 UTC)

This review re-read all five default-branch refs, open PRs, latest Actions run pages and exact-head checks, then inspected the active Platform decommission branch and its validation contracts. It distinguishes app publisher CI from an authorized production image release and branch-only GitOps changes from the current master runtime.

### Repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `b1a0c185e3f97630aa2bf55945bb5f674200bf97` | #1301 ready; #1296/#544/#541/#539 draft | #1301 proposes the complete Stock/Media GitOps retirement at head `dce6ae5341ce925177156f5fd9b537c453589323`; exact-head validation is queued. Master remains unchanged. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Native WF-06 #42133793538 returned HTTP 503 on four strict public probes while TCE/Auth/Keycloak remain operator-scaled to zero; WF-13 fallback #42133822204 passed and remained read-only. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 merged; post-merge CI #42137523269 PASS. No new production publisher run or Platform dispatch after merge; release hold remains closed. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged; post-merge CI #42136991059 PASS. The app publisher no longer dispatches Platform; no production release was triggered. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Latest PR validation runs #40446492086/#41329425940 are historical; Supabase Preview remains SKIPPED and the production integration side-effect gate is unresolved. |

### App-owned publisher boundary

- Stock PR [#32](https://github.com/phanthienquoc/stockdividend/pull/32) merged after exact-head review. Post-merge StockDividend CI #42137523269 passed. The app repo retains its own CI, ARM64 immutable image build and manual publication hold; no new publisher run or production tag/digest promotion was initiated.
- Media PR [#72](https://github.com/phanthienquoc/media-generation/pull/72) merged. Post-merge Media CI #42136991059 passed. The app repo retains paired immutable full-source-SHA GHCR publication/digest verification and no longer sends a Platform dispatch. No production release workflow was manually dispatched.
- App repos continue to own tests/builds/immutable GHCR publication. Platform owns only remaining production manifests, shared pull credentials, digest/provenance checks, GitOps promotion/reconciliation, rollout and health.

### Platform implementation PR #1301

- PR [#1301](https://github.com/phanthienquoc/platform-infra/pull/1301) is open at exact head `dce6ae5341ce925177156f5fd9b537c453589323`, 10 commits ahead of master and 0 behind.
- The branch removes all 19 files under `apps/stockdividend` and `apps/media-generation`, excludes both from production composition, removes their reconcile/health/recovery/GHCR and dispatch contracts, and deletes six obsolete app-specific runner/publisher helper files. It preserves app repositories, GHCR packages, TCE, Auth, MicroFE, Keycloak, cert-manager and the shared Platform runner.
- It adds a manual-only namespace workflow guarded by the protected production Environment and three typed confirmations. The live preflight enumerates all namespaced API object names without printing Secret/ConfigMap values, lists common workload status, checks PVC/PV claims and StorageClasses, and the root-owned wrapper can delete only `stock-prod` and `media-prod`.
- The first PR check set is queued: Validate Keycloak manifests/boundaries #42145176538, validate-manifests #42145176539, and validate-github-actions #42145176540. Do not merge until all required checks pass against the final exact head.
- Two earlier branch push runs (#42141922040 and #42142089191) belong to older commits, not the current PR head. They are not evidence of current-head validation.
- The plan-only PR #1296 is superseded by implementation PR #1301 and should be closed once the implementation PR is accepted.

### Runtime and schedule safety

- The latest committed read-only VPS snapshot is #42131886966, generated at 2026-11-05T23:46:15Z. It is stale for a destructive operation and does not include PVC/PV/StorageClass inventory. The dedicated Media runner was present in that snapshot; its current state is unverified.
- No K3s namespace, PV, DNS record, GHCR package, external database/object storage, host, or runner registration was changed. Namespace deletion remains a separate manual action after fresh same-window inspection, backup/external-data review, and independently verified Media-runner stop/unregister.
- TCE WF-06 HTTP 503 is consistent with the operator-requested zero-replica state. Keep strict HTTP 200 gates and all schedules, especially the TCE market-scan schedule, unchanged.
- `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority was added.

### Next actions

1. Poll #1301 exact-head checks; fix any failing contract and revalidate the updated head.
2. Squash-merge only after all required checks pass against the current PR head; close superseded draft PR #1296.
3. After merge, independently stop/unregister the dedicated Media runner, then use the manual namespace workflow only with a fresh live inventory and approved backup/external-data review.
4. Capture a fresh post-decommission inspection and verify TCE/Auth/MicroFE/Keycloak remain unchanged.
5. Keep Stock production publication/promotion closed without explicit release authorization; keep Auth #75/#76 gated on the unresolved Supabase integration effect.

## Current review — 2026-11-06 07:29 ICT (2026-11-06 00:29 UTC)

This review supersedes the 04:56 tracker entry and the 06:04 workflow-inventory checkpoint. It records the current five-repository state, the Media publisher-only merge, the Stock CI repair in progress, and the decommission safety boundary.

### Repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `3346be7997d017bd45eb0782331a7dafb9bb571c` | #1296 (draft), #544/#541/#539 (draft) | #1296 is a plan-only decommission runbook; exact-head `validate-manifests` #42131770950 PASS. No production or K3s resources changed. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 public checks fail on intentional HTTP 503 while TCE/Auth are operator-scaled to zero; WF-13 read-only fallback succeeded. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | #32 | Retired Platform dispatch removal is in review at exact head `c015961ec45ce7b698ea8fde9e2d7e9b5fe3c4f0`; latest CI #42137106072 is queued/in progress. Do not merge yet. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged by squash; app publisher now builds, publishes and verifies immutable paired GHCR digests without dispatching Platform. Post-merge CI #42136991059 PASS. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Keep both gated: production Supabase integration side effect is still not authoritatively verified; Preview remains skipped. |

### App publisher contract changes

- Media PR [#72](https://github.com/phanthienquoc/media-generation/pull/72) merged at exact head `9e66bd6bdef065f5ca427cfd5e69b30b59c3cbab`; squash merge `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`. Exact-head PR/push CI #42135150058/#42135140342 both passed; post-merge push CI #42136991059 passed. The workflow retains immutable full-source-SHA tags, registry digest resolution and ARM64 verification, and no longer sends a Platform repository_dispatch.
- Stock PR [#32](https://github.com/phanthienquoc/stockdividend/pull/32) removes the Platform token check and atomic promotion dispatch while retaining app CI, the manual publication hold, native ARM64 image builds and immutable registry verification. The first contract run failed on stale assertions; the follow-up branch changes restored the validator self-path in `deploy.yml` path exclusions, renamed the CI step, corrected the exact manual-hold assertion and escaped literal GitHub expression markers in the shell test. Latest exact-head run #42137106072 is not complete; merge remains blocked until all exact-head checks pass.
- Do not enable `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`, promote either half of the Stock Admin/Backend pair, or change production image references without explicit release authorization and protected publisher provenance.

### Platform schedule and K3s evidence

- Latest native Platform inspect schedule: #42112599830 PASS at 2026-11-05 21:26:04Z. Latest read-only manual inspection: #42131886966 PASS, generated snapshot at 2026-11-05 23:46:15Z; this is not native schedule evidence.
- Latest native reconcile schedule #42121826106 failed only at the Stock health gate; native recovery #42121354158 passed; native schedule watchdog #42123445690 passed. Do not count workflow_dispatch/workflow_run fallbacks as cron ticks.
- Snapshot-time node: ARM64, 19 GiB available RAM, disk 56%, K3s service active. Media backend/frontend were 1/1 Running. Stock Admin had two ImagePullBackOff Pods, Stock Backend had one old 1/1 Pod plus one ImagePullBackOff Pod, and legacy Stock Frontend remained 1/1. Both namespaces, Services and Ingresses remained present.
- The snapshot shows the dedicated Media Actions runner service active. It does not contain PVC/PV or StorageClass inventory, so it is insufficient for namespace deletion or storage-retention decisions. No namespace deletion, runner unregister/stop, DNS change, PV deletion, or external storage/database mutation was performed.
- The snapshot is about 43 minutes old at this review and is not a live guarantee.

### TCE health and schedule guard

- TCE WF-06 #42133793538 (native schedule) failed all four strict public probes: Auth liveness/readiness and TCE API/web returned HTTP 503 instead of 200.
- This matches the documented operator-requested zero-replica state for TCE/Auth/Keycloak. WF-13 fallback #42133822204 completed successfully and remains read-only; no replica, ingress, health threshold or cron was changed.
- Preserve every TCE schedule, especially the market-scan schedule. Do not restore TCE/Auth/Keycloak replicas or weaken HTTP 200 gates without explicit operator authorization.

### Deployment authority and next safe work

- Ownership remains: app repositories own tests/builds and immutable GHCR publication; Platform Infra owns production manifests, shared GHCR pull credentials, publisher provenance/digest validation, GitOps promotion/reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No app workflow is allowed to add a competing SSH/Compose/kubectl production path.
- Next: complete and merge Stock PR #32 only after exact-head CI passes; then remove Stock/Media receiver, manifest, health and recovery contracts from Platform in a dedicated PR. Before deleting `stock-prod` or `media-prod`, extend/read a fresh inspection that inventories PVCs/PVs/storage classes, verify backups and DNS ownership, and confirm the dedicated Media runner is idle. Keep deletion a separate manually approved operation.
- No production image, manifest, credential, database, replica, host, namespace, DNS, PV, or cron mutation was made. TCE market-scan schedule unchanged.

## Current review — 2026-11-06 04:56 ICT (2026-11-05 21:56 UTC)

This review supersedes the 03:56 ICT entry. It re-reads all five default-branch refs, open PRs, latest Actions run pages, the latest native Platform inspection, the resulting K3s snapshot, the latest reconciliation lane results and the current TCE native-event history. It distinguishes native schedule runs from workflow_dispatch/workflow_run recovery.

### Repository refs, open PRs and latest workflow evidence

| Repository | Current default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | 419b83666cae7773b0a1dbc62900f275add05d9d | #544/#541/#539 (draft) | Native inspect-vps #42112599830 PASS at 04:26 ICT; inspection PR #1293 merged as current master. Reconcile dispatch #42112833885 failed only at Stock health. Recovery dispatch #42113114275 PASS. |
| TCE Dashboard | 512b69d837e2a65c39867a062529a7fa0eada4cc | None | PR #1026 merged. Latest master push checks WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 #42105365586 PASS. No eligible post-merge native WF-07/WF-12 sequence yet. |
| StockDividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None | Latest master CI #41563856934 and immutable publisher #41563856933 PASS on Nov 3; no newer app build or release publication. |
| Media Generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None | Latest master CI #41617592783 PASS on Nov 3; historical, not fresh validation. |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 (ready), #76 (draft) | Latest master Auth CI #41670642852 PASS on Nov 3; historical, not fresh validation. Supabase Preview remains SKIPPED on the open PRs. |

### Platform native inspection restored; PR #1293

- Native scheduled inspection #42112599830 ran at 04:26:04 ICT with event=schedule and concluded success.
- Its inspection job passed: Inspect VPS, detect meaningful changes, validate output, rebase snapshot, create inspection PR and validate the exact inspection PR head before squash merge.
- Automated inspection PR #1293 merged at 04:27:15 ICT. Its exact head was 375cefa0a9e08828df2052a60373b1ecf5ff5aa2 and the squash merge/current master SHA is 419b83666cae7773b0a1dbc62900f275add05d9d.
- The current debug/vps-latest.md snapshot was generated at 04:26:12 ICT. At this 04:56 review it is about 30 minutes old. This is genuine native-schedule inspection evidence, unlike the earlier workflow_dispatch snapshots.

### Latest reconciliation and StockDividend failure

- Reconcile #42112833885 was a workflow_dispatch run at 04:27:38 ICT, not a native schedule tick. It used mode=apply, target_app=stockdividend and allow_image_changes=false.
- Shared GHCR pull-access validation, GHCR credential bootstrap and the scoped image-pull recovery step succeeded. The Auth, Media, MicroFE and TCE lanes passed; Keycloak was skipped. The final gate correctly failed only because the StockDividend lane was unhealthy.
- The exact Stock lane log reports two Stock Admin Pods and one new Stock Backend Pod using ghcr.io/phanthienquoc/stockdividend/{admin,backend}:12d63b4 with ImagePullBackOff and no match for platform in manifest. The deployment stock-admin remained desired=1/ready=0/updated=1.
- The runner helper explicitly classified both errors as permanent architecture/manifest failures and logged that it was skipping rollout restart; no replacement rollout was triggered for those bad references. The regression test scripts/tests/restart-blocked-image-pulls.test.sh covers permanent failures, transient credential/network failures, mixed failures and unrelated CrashLoopBackOff. Do not add a redundant restart or bypass this guard.
- Preflight found no manifest drift, so image-change guard and production manifest apply were skipped. No production image reference was changed. The failure is not a GHCR pull-secret issue: shared access preflight and credential bootstrap passed.
- Recovery controller #42113114275 completed successfully at 04:29:33 ICT after the failed reconciliation. It is workflow_dispatch recovery evidence, not a native recovery schedule tick.

### Native Platform schedule matrix

| Workflow | Latest native event=schedule | Result | Latest non-native evidence |
|---|---|---|---|
| inspect-vps | #42112599830 — 04:26:04 ICT | PASS | Inspection PR #1293 merged; snapshot 04:26:12 ICT. |
| reconcile-vps | #42068683835 — Nov 5 23:51:03 ICT | FAIL at Stock health | #42112833885 workflow_dispatch failed at Stock health. |
| recover-stale-ops | #42068414686 — Nov 5 23:49:29 ICT | PASS | #42113114275 workflow_dispatch PASS after #42112833885. |
| reconcile-schedule-watchdog | #42070623710 — Nov 6 00:02:22 ICT | FAIL, inspection freshness | #42112872580 workflow_run SKIPPED. |

- The native inspection schedule has produced a new successful run. Do not continue describing inspect-vps as wholly stale.
- Native reconcile, native recovery and native watchdog schedule evidence remain old. Keep their native freshness separate from the newer manual/event-driven runs.
- Preserve all existing cron declarations. No schedule was edited.

### K3s snapshot at 04:26 ICT

Source: debug/vps-latest.md generated by native inspect-vps #42112599830.

- Node tce-k3s-01: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3.
- Disk 56%; available RAM about 19 GiB; restart_required=yes. No maintenance authorization was present, so no host restart or package upgrade.
- Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 Running.
- Stock Admin had two ImagePullBackOff Pods on tag 12d63b4; the new Backend Pod was ImagePullBackOff on the same tag. The old Backend and Frontend remained 1/1.
- TCE frontend/service, microfe-auth and Keycloak were 0/0, matching the documented operator-requested shutdown. Their public HTTP 503 state is expected while that shutdown remains in force; do not restore replicas or weaken strict HTTP 200 health gates without fresh operator authorization.
- Snapshot is native inspection evidence at 04:26:12 ICT, not a live guarantee after that timestamp.

### TCE recovery status

- TCE master remains 512b69d837e2a65c39867a062529a7fa0eada4cc; PR #1026 is merged and post-merge WF-01/WF-02/WF-05/WF-12 checks passed.
- Latest native WF-07 is #42098832858 (Nov 5 02:57:39 ICT), before PR #1026 merged. Latest native WF-06 is #42089383865 (01:58:27 ICT, failure); latest native WF-12 is #42083178274 (01:19:51 ICT, failure).
- No post-merge native WF-07 success → WF-12 stale-WF-06 detection → WF-13 → exactly one WF-06 fallback sequence has yet exercised the new source-conclusion guard.
- WF-13 remains the only WF-06 fallback dispatcher. WF-12 is read-only. No TCE market-scan schedule or health gate was changed.

### App repository release and CI gates

- Stock publisher #41563856933 previously verified immutable full-source-SHA ARM64 artifacts for Scraper/Admin/Backend, but it is historical and its production promotion gate was disabled. Production Admin/Backend still reference tag 12d63b4, which is not ARM64-compatible. Do not set STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED or paired-promote without explicit release authorization and protected publisher-run provenance.
- Media master CI #41617592783 and Auth master CI #41670642852 are Nov 3 historical results, not fresh builds.
- Auth PR #75 remains ready at head a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05; PR #76 remains draft at head f19cacb0bf2b454b3152bd3a501f6f88d0a14a58. Supabase Preview is SKIPPED and the Deploy-to-production integration target/effect is not authoritatively verified. Do not merge either PR, dispatch a release, or run migrations on that evidence.
- Platform PR #544 (draft head c95e7daecb83b65577b54303427fe4ea81adfe06), #541 (draft head b8f7c6ba04e3d971336a899b2efd5894662083b3) and #539 (draft head 2dc48b97017ecb08e49682633303a2f1d5e991a1) remain open. Their observed checks are stale; do not merge drafts.

### Next actions and safety

1. Keep monitoring native inspect-vps after its successful #42112599830 schedule run; independently track native reconcile/recovery/watchdog freshness and investigate only if subsequent scheduled ticks are missed.
2. Keep Stock paired promotion blocked until explicit release authorization and protected publisher provenance; do not mutate the incompatible production tag.
3. Verify the first eligible post-merge native TCE WF-07 → WF-12 → WF-13 sequence and exactly one fallback with exact SHA/source correlation.
4. Keep Authentication PRs/migrations and Keycloak activation gated on authoritative Supabase integration and credential/DB evidence.
5. Keep TCE/Auth/Keycloak zero replicas until explicit operator reactivation authorization; retain strict public HTTP 200 gates.
6. Preserve app-owned tests/builds/immutable GHCR and Platform-owned manifests/credentials/provenance/promotion/reconciliation/rollout. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
7. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.

## Current review — 2026-11-06 03:56 ICT (2026-11-05 20:56 UTC)

This review reconciles the 03:42 checkpoint with the merged Platform PR #1291, completed TCE post-merge build, current open-PR heads/checks, latest Actions run pages, and the latest read-only VPS snapshot. It does not infer new production health from stale runtime evidence.

### Repository refs, open PRs and latest workflow evidence

| Repository | Current default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `086ee573f29b148bdb6ab55e3faa6a3000a5aa56` | #544/#541/#539 (draft) | PR #1291 merged at 03:42:45 ICT; post-merge validate-manifests #42105916492 PASS. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; post-merge WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 #42105365586 all PASS. WF-13 #42105390163 correctly SKIPPED for a WF-12 push-smoke source. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | Latest master CI #41563856934 and publisher #41563856933 PASS on Nov 3; no newer app build. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | Latest master CI #41617592783 PASS on Nov 3; historical, not fresh validation. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Latest master Auth CI #41670642852 PASS on Nov 3; historical, not fresh validation. |

### PR #1291 and current Platform master

- Platform PR [#1291](https://github.com/phanthienquoc/platform-infra/pull/1291) is closed/merged; its exact head was `9ae3f8da82d5bd13cf0f30d113fc632db43c0132`, and its squash merge commit is `086ee573f29b148bdb6ab55e3faa6a3000a5aa56`.
- Exact-head validation #42105809491 and post-merge master validation #42105916492 both PASS. The current master ref was independently read from GitHub's branch endpoint and matches the merge SHA.
- The previous 03:42 tracker entry listed the pre-merge Platform SHA `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6`; this entry supersedes it.
- Platform open PRs remain unchanged: #544 draft head `c95e7daecb83b65577b54303427fe4ea81adfe06`, #541 draft head `b8f7c6ba04e3d971336a899b2efd5894662083b3`, #539 draft head `2dc48b97017ecb08e49682633303a2f1d5e991a1`. Their only observed validate checks passed on Oct 14; these are stale checks and do not justify merging the drafts.

### Authentication PR gates

- PR #75 is open/ready at head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; validate passed Oct 27, while Supabase Preview is SKIPPED.
- PR #76 is open/draft at head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; validate passed Nov 1, while Supabase Preview is SKIPPED.
- The PR #75 description still records Deploy-to-production integration as ON and says the actual integration target/effect is not authoritatively verified. Do not merge either PR, dispatch release workflows, or run migrations until that external side effect is resolved.

### TCE post-merge verification and remaining native-event gap

- PR #1026 is present on current master `512b69d837e2a65c39867a062529a7fa0eada4cc`. Its source-conclusion guard is covered by successful post-merge WF-01/WF-02/WF-05/WF-12 checks.
- WF-13 #42105390163 was skipped because its source was the WF-12 push smoke #42105365586, not an eligible native schedule event. This is expected and is not a recovery failure.
- Latest native WF-07 remains #42098832858 (02:57:39 ICT), before PR #1026 merged. Latest native WF-06 remains #42089383865 (01:58:27 ICT, failure); latest native WF-12 remains #42083178274 (01:19:51 ICT, failure). No post-merge native WF-07 → WF-12 → WF-13 sequence has yet validated the new guard.
- Keep the confirmed operator-requested TCE/Auth/Keycloak zero-replica state and strict HTTP 200 health gates. No replica, ingress or market-scan schedule changes.

### Platform native schedules and fallback freshness

| Platform workflow | Latest native `event=schedule` run | Result |
|---|---|---|
| inspect-vps | #42049660972 — Nov 5 21:55:03 ICT | PASS, stale |
| reconcile-vps | #42068683835 — Nov 5 23:51:03 ICT | FAIL at Stock health gate |
| recover-stale-ops | #42068414686 — Nov 5 23:49:29 ICT | PASS |
| reconcile-schedule-watchdog | #42070623710 — Nov 6 00:02:22 ICT | FAIL, inspection freshness |

- The latest 100-run Actions page contains no later native `event=schedule` run for these Platform workflows. The current `inspect-vps.yml` still declares cron `2,32 * * * *`, uses the self-hosted ARM64 Platform/K3s/VPS runner, and is not to be conflated with manual fallback.
- The latest read-only inspection remains #42099284088, `workflow_dispatch`, generated at 03:00:41 ICT. At 03:56 it is about 56 minutes old and within the 75-minute fallback budget, but it is not native schedule evidence.
- Snapshot-time state: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB available RAM; `restart_required=yes`. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend (one Pod) ImagePullBackOff; old Stock Backend/Frontend 1/1; TCE frontend/service, microfe-auth and Keycloak 0/0.
- The snapshot is read-only evidence at its generation time, not a live inspection at 03:56. Do not restart the host or update packages without an approved maintenance window.

### Stock release and architecture gate

- Publisher #41563856933 verified immutable full-source-SHA ARM64 artifacts for Scraper/Admin/Backend. The release hold remained false; production handoff and paired promotion were skipped.
- Production Admin/Backend still reference tag `12d63b4`, which is incompatible with the ARM64 K3s node (`no match for platform in manifest`). Shared GHCR preflight/credential bootstrap had passed in the prior reconcile evidence, so do not misclassify this as a pull-secret failure.
- Do not set `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`, promote a single member of the Admin/Backend pair, or mutate production image references without explicit release authorization and protected publisher-run provenance.

### Next actions and safety

1. Keep native Platform schedule freshness distinct from workflow_dispatch fallback freshness; investigate delivery without changing any cron declaration or adding a competing apply authority.
2. Verify the first eligible post-merge native TCE WF-07 → WF-12 → WF-13 sequence exactly once; keep WF-13 as the only WF-06 fallback dispatcher.
3. Keep Stock paired promotion blocked until explicit release authorization and protected publisher provenance are verified.
4. Keep Auth PRs/migrations and Keycloak activation gated on authoritative Supabase integration and credential/DB evidence.
5. Keep TCE/Auth/Keycloak zero replicas until explicit operator reactivation authorization; retain strict public HTTP 200 gates.
6. Preserve app-owned tests/builds/immutable GHCR and Platform-owned manifests/credentials/provenance/promotion/reconciliation/rollout. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
7. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.

# Cross-Repository Production Deployment Tracker

## Current review — 2026-11-06 03:42 ICT (2026-11-05 20:42 UTC)

This review adds the TCE WF-12 source-filter hardening merged after the 03:34 review. It also preserves the direct GitOps explanation for the TCE/Auth 503 state.

### Repository refs and PRs

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6` | #544/#541/#539 (draft) | PR #1290 merged; exact-head #42104850991 and post-merge #42104919461 PASS. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; exact-head WF-02/WF-05 and post-merge WF-12/WF-02/WF-05 passed; post-merge WF-01 build is still running at this review. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | Publisher #41563856933 verified immutable ARM64 full-SHA artifacts; production hold false and paired promotion skipped. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | Latest CI #41617592783 is historical (Nov 3). |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Latest master CI #41670642852 is historical (Nov 3); PR #75 Supabase Preview is SKIPPED and commit status pending. |

### TCE PR #1026 — WF-07 source conclusion guard

- PR [#1026](https://github.com/phanthienquoc/TCE-dashboard/pull/1026) merged at 03:39:08 ICT as `512b69d837e2a65c39867a062529a7fa0eada4cc`.
- The WF-12 `verify` job now accepts a `workflow_run` source from WF-06 as before, but accepts WF-07 only when that native scheduled WF-07 run concluded `success`. A failed WF-07 still emits the existing Platform heartbeat; it cannot independently cause the stale-WF-06 watchdog path to fail and trigger WF-13.
- WF-06 native failures remain independently handled by WF-13. WF-12 remains read-only and WF-13 remains the only WF-06 fallback dispatcher. No cron or market-scan schedule changed.
- Exact-head checks on `d3025bcdf63e90eff24c36b10ce6d03133f69f50`: WF-02 PR #42105124810 PASS; WF-05 PR #42105124578 PASS; push WF-02 #42105113543 PASS and push WF-05 #42105113596 PASS.
- Post-merge checks on `512b69d837e2a65c39867a062529a7fa0eada4cc`: WF-12 push smoke #42105365586 PASS; WF-02 #42105365483 PASS; WF-05 #42105365567 PASS. WF-01 build/verify #42105365294 was still in progress at 03:42 ICT after the frontend image build passed and backend image build began; do not call the full post-merge build green until it completes.
- No post-merge native WF-07/WF-12 schedule event has yet exercised the new source-conclusion guard. Latest native WF-07 #42098832858 (02:57:39 ICT), WF-12 workflow_run #42098855352 (02:57:48 ICT), and WF-13 #42098897759 (02:58:04 ICT) all predate PR #1025 and #1026 merges. Latest native WF-06 #42089383865 (01:58:27 ICT) and native WF-12 #42083178274 (01:19:51 ICT) remain old failures.

### Confirmed TCE/Auth public 503 state

- TCE ingress routes `tce.mrcute.space/` to `tce-frontend` and `/api` to `tce-service`; both backing Deployments explicitly set `replicas: 0` under a temporary operator shutdown request.
- Auth ingress routes `auth.mrcute.space` to `microfe-auth`; its Deployment explicitly sets `replicas: 0` under the same operator shutdown intent. Keycloak also explicitly sets `replicas: 0`.
- These source manifests and ingress mappings explain the public 503 probes. The healthcheck is correctly reporting intentional unavailability, not a new image or credential regression. Do not restore replicas, alter ingress or weaken HTTP 200 gates without explicit operator authorization.

### Platform runtime and native schedule evidence

- Platform PR #1290 merged as `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6`; exact-head #42104850991 and post-merge #42104919461 passed.
- Latest native Platform schedules remain inspect-vps #42049660972 (Nov 5 21:55 ICT), reconcile-vps #42068683835 (23:51, Stock health failure), recover-stale-ops #42068414686 (23:49, PASS), and watchdog #42070623710 (Nov 6 00:02, inspection freshness failure). No newer native `event=schedule` run appeared through the latest run page after #42104919461.
- Recovery #42099209509 dispatched read-only inspect #42099284088, which passed and generated `debug/vps-latest.md` at 03:00:41 ICT. At 03:42 it is about 41 minutes old and remains within the 75-minute fallback budget; it is workflow_dispatch evidence, not native schedule evidence.
- Snapshot-time runtime remains: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB available RAM; `restart_required=yes`. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE frontend/service, microfe-auth and Keycloak 0/0.
- Stock production overlay still uses `newTag: 12d63b4` for Admin and Backend. Publisher #41563856933 verified ARM64 full-SHA artifacts, but the production hold was false and paired promotion was skipped. Platform's `validate-ghcr-image-reference.sh` independently verifies ARM64 manifests/configs before accepting a promotion. Keep the old tag blocked; do not promote without explicit release authorization and protected publisher provenance.

### Next actions and safety

1. Wait for TCE post-merge WF-01 #42105365294 to finish; then verify the next post-merge native WF-07 → WF-12 → WF-13 sequence exactly once.
2. Keep TCE/Auth/Keycloak at their explicitly requested zero-replica state until a new operator authorization resolves the Supabase/Keycloak issue.
3. Keep Stock paired promotion disabled until explicit release authorization and protected publisher provenance are verified.
4. Keep native schedule freshness separate from workflow_dispatch fallback freshness; preserve every cron declaration.
5. Keep Auth migrations and Keycloak activation gated; wait for an approved VPS maintenance window before host/package changes.
6. Preserve app-owned tests/builds/immutable GHCR and Platform-owned manifests/credentials/provenance/promotion/reconciliation/rollout. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
7. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.


## Runtime diagnosis update — 2026-11-06 03:34 ICT (2026-11-05 20:34 UTC)

This update supersedes the earlier statement that TCE/Auth public HTTP 503 responses were only correlated with zero-replica observations. Current GitOps source manifests and their ingress routes now prove the expected upstream-unavailable state.

### Public 503 root cause — intentional operator shutdown

- TCE ingress `apps/tce-dashboard/overlays/prod/ingress.yaml` routes `tce.mrcute.space/` to Service `tce-frontend:80` and `/api` to `tce-service:8210`.
- Both backing Deployments explicitly declare `replicas: 0` in `apps/tce-dashboard/base/frontend.yaml` and `apps/tce-dashboard/base/service.yaml`, with comments recording the temporary operator request to scale TCE down until re-enabled.
- Auth ingress `platform/microfe/ingress.yaml` routes `auth.mrcute.space/` to Service `microfe-auth:80`.
- The backing `platform/auth-service/deployment.yaml` explicitly declares `replicas: 0` and records the temporary operator request to stop Auth API and Keycloak until the Supabase/Keycloak connection issue is resolved.
- `platform/keycloak/deployment.yaml` also explicitly declares `replicas: 0` under the same operator shutdown intent.
- These routes plus zero desired replicas explain the strict public 503 probes for TCE web/API and Auth readiness/liveness. The healthcheck is correctly reporting intentional unavailability; it is not evidence of a new image-pull or deployment regression.
- Do not restore replicas, alter ingress, or weaken HTTP 200 gates without a new explicit operator authorization. The existing shutdown state is intentional and must remain GitOps-managed.

### PR #1289 completion

- PR #1289 merged by squash as `f5d62e4a4f9abd992458849929a14a85a3250614`.
- Exact-head validation #42104285775 PASS on `5a570ae15ded480b2c391941db9bc71eeb8d4cb5`.
- Post-merge validation #42104477168 PASS on the merge SHA. Manifest rendering, digest-promotion helpers, MCP GitOps-only contract, shell checks, Auth GitOps, YAML structure, secret policy, immutable image policy, Keycloak isolation and network boundaries passed. Changed-image validation was skipped because PR #1289 was documentation-only.

### Updated next actions

1. Keep TCE/Auth/Keycloak at their operator-requested zero-replica state until the operator resolves the Supabase/Keycloak issue and explicitly authorizes reactivation.
2. Continue verifying the new TCE PR #1025 stale-WF-06 recovery path on a post-merge native WF-07/WF-12 event; do not count pre-merge runs as E2E evidence.
3. Keep Stock Admin/Backend paired promotion blocked until explicit release authorization and protected publisher provenance; current tag `12d63b4` remains ARM64-incompatible.
4. Preserve native schedule freshness separately from workflow_dispatch fallback freshness; do not change cron declarations.
5. Keep Authentication migrations and Keycloak activation gated; wait for an approved VPS maintenance window before host/package changes.


## Current review — 2026-11-06 03:27 ICT (2026-11-05 20:27 UTC)

This review re-read all five default-branch commits, open PRs, latest Actions runs, Platform native schedule history, the latest reconciliation and lane summaries, the current read-only VPS snapshot, Stock's publisher contract/run, and TCE's newly merged recovery change. It supersedes the 01:58 review below.

### Repository refs, open PRs and CI evidence

| Repository | Current default-branch SHA | Open PRs | Latest evidence |
|---|---|---|---|
| Platform Infra | `9d533e503d412e583873a91aefd66263c297fafa` | #544/#541/#539 (draft) | Inspection-state PR #1288 merged at 03:01:43 ICT; exact inspection branch validation #42099407335 PASS. Latest master read-only inspection #42099284088 PASS. |
| TCE Dashboard | `162390fe4811131c11d3f39d264e0722a826dc0f` | None | PR #1025 merged at 03:22:34 ICT; exact-head WF-05 #42102448205 and WF-02 #42102448276 PASS; post-merge WF-01 #42102796954, WF-05 #42102795916 and WF-02 #42102795382 PASS. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and publisher #41563856933 PASS (Nov 3); publisher verified all three immutable full-SHA ARM64 image manifests, while production promotion was held/skipped. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | Latest master CI #41617592783 PASS (Nov 3); no newer app build in the latest run page. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Latest master CI #41670642852 PASS (Nov 3); no newer master build. Supabase Preview checks on the open PRs remain SKIPPED. |

Open PR heads were re-read:
- Platform #544: `c95e7daecb83b65577b54303427fe4ea81adfe06` (draft); #541: `b8f7c6ba04e3d971336a899b2efd5894662083b3` (draft); #539: `2dc48b97017ecb08e49682633303a2f1d5e991a1` (draft).
- Authentication #75: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` (ready); #76: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` (draft). Their passing checks are historical and Supabase Preview is skipped; do not merge or run migrations on that evidence.
- No open PRs in TCE Dashboard, StockDividend or Media Generation. Do not treat Nov 3 app CI as fresh validation.

### TCE PR #1025 — new stale-WF-06 recovery path

- PR [#1025](https://github.com/phanthienquoc/TCE-dashboard/pull/1025) merged as `162390fe4811131c11d3f39d264e0722a826dc0f` at 03:22:34 ICT.
- It closes the gap where a successful native WF-07 schedule causes WF-12 to detect a stale native WF-06 schedule, but WF-13 previously ignored the resulting workflow_run event.
- WF-12 remains read-only. It requests WF-13 only after a successful native WF-07 schedule leads to a failed stale-WF-06 verification; the request is correlated to the exact WF-12 run and its failed job/step evidence. WF-13 remains the only WF-06 fallback dispatcher.
- Exact-head WF-05/WF-02 checks and all three post-merge master checks passed.
- Important ordering: WF-07 #42098832858 (02:57:39 ICT), WF-12 workflow_run #42098855352 (02:57:48 ICT, failure), and WF-13 #42098897759 (02:58:04 ICT, skipped) all ran before PR #1025 merged. They do not exercise the new code. No qualifying post-merge native WF-07/WF-12 event has yet proved the new path end-to-end.
- Latest native TCE evidence remains WF-06 #42089383865 (01:58:27 ICT, failure) and WF-12 #42083178274 (01:19:51 ICT, failure). The earlier WF-06 fallback #42089448641 also failed all four strict public probes with HTTP 503. Keep HTTP 200 gates and every TCE cron declaration unchanged.

### Platform native schedule evidence — separate native schedules from fallbacks

| Platform workflow | Latest native `event=schedule` run | Result |
|---|---|---|
| inspect-vps | #42049660972 — Nov 5 21:55:03 ICT | PASS, stale |
| reconcile-vps | #42068683835 — Nov 5 23:51:03 ICT | FAIL at Stock health gate |
| recover-stale-ops | #42068414686 — Nov 5 23:49:29 ICT | PASS |
| reconcile-schedule-watchdog | #42070623710 — Nov 6 00:02:22 ICT | FAIL, inspection freshness |

The latest 100 Platform Actions runs through #42099407335 (03:01:17 ICT) contain no later native `event=schedule` run. Do not attribute the missing native inspect event to runner queue without new evidence. The workflow's existing cron remains `2,32 * * * *`; the recovery controller still distinguishes native schedule freshness from workflow_dispatch fallback freshness. Preserve all cron declarations.

### Latest reconciliation and current read-only K3s snapshot

- Reconcile #42098901197 (workflow_dispatch, 02:58:05 ICT; source Platform SHA `fff1767db7e8e3d14b78ed84a5f7e03bef9341cd`) failed only in the StockDividend lane. Shared GHCR preflight, Auth runtime Secret provisioning and pull-credential bootstrap passed. Media, MicroFE, TCE and Auth lanes passed; Keycloak was skipped. Production manifest apply and image changes were skipped with `allow_image_changes=false`.
- Stock failure was isolated to Admin (two Pods) and the new Backend Pod on image tag `12d63b4`; containerd reports `no match for platform in manifest`. The failure is architecture compatibility, not evidence of a shared pull-secret problem. Existing Stock Backend and Frontend remained 1/1 in this snapshot.
- Recovery #42099209509 passed and dispatched read-only inspection #42099284088, which passed. Snapshot `debug/vps-latest.md` was generated 03:00:41 ICT. At this review it is about 27 minutes old and within the 75-minute fallback budget, but it is a workflow_dispatch snapshot, not native schedule evidence.
- Snapshot-time host/runtime: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB available RAM; `restart_required=yes`.
- Snapshot-time workloads: Media backend/frontend 1/1; MicroFE Shell/WS and NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff; old Backend and Frontend 1/1; TCE frontend/service 0/0; microfe-auth and Keycloak 0/0. These are observations from the 03:00 snapshot, not a claim about later live state.

### Stock immutable publisher and paired promotion gate

- Current Stock publisher workflow uses an ARM64 runner, builds Scraper/Admin/Backend for `linux/arm64`, tags each image with the full source SHA, and verifies each registry manifest/digest before any promotion handoff.
- Publisher #41563856933 passed the ARM64 runner check, all three builds, and immutable ARM64 registry verification. Its production-release hold returned `release_enabled=false`; handoff validation and atomic paired promotion were skipped.
- The current production tag `12d63b4` remains architecture-incompatible. Do not repoint production to a new digest or promote Admin/Backend separately. The exact next gate is explicit release authorization (`STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`) plus protected publisher-run provenance/Actions:read verification and the existing paired digest contract. Do not enable the release variable or dispatch promotion without authorization.

### Authentication, Media and Keycloak gates

- Media's latest CI is historical (Nov 3); its 1/1 workload status is only from the 03:00 snapshot.
- Authentication's latest master CI is historical (Nov 3). PR #75/#76 remain gated because Supabase Preview is skipped and the production integration side-effect binding is not authoritatively verified. Do not merge or run migrations.
- Keycloak remains 0/0 in the current snapshot. Platform PR #544/#541/#539 are still drafts; the Keycloak runtime DB credential and SSO ingress prerequisites are not proven. Do not activate the lane.

### Next dependency-safe actions

1. Wait for the next native WF-07 schedule after PR #1025 merge; verify native WF-07 → read-only WF-12 stale-WF-06 evidence → exactly one WF-13 → one read-only WF-06 fallback, with source run/attempt/SHA correlation. Do not count pre-merge #42098855352/#42098897759 as proof.
2. Keep strict TCE/Auth HTTP 200 health gates. Investigate ingress/service/endpoints using fresh runtime evidence; the 0/0 snapshot and 503 probes are correlated, not a proven root cause.
3. Keep Stock paired promotion closed until explicit authorization and protected publisher provenance are both verified.
4. Continue distinguishing native Platform schedule freshness from the fresh workflow_dispatch inspection fallback; preserve cron declarations and do not dispatch duplicate inspection while the fallback remains within 75 minutes.
5. Keep Authentication migrations and Keycloak activation gated on authoritative credentials/integration evidence.
6. Wait for an approved VPS maintenance window before host restart or Docker/containerd package changes.

### Safety invariants

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, provenance/digest verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred in this review.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows.
- TCE market-scan schedule unchanged.


Last reviewed: 2026-11-06 08:38 ICT (2026-11-06 01:38 UTC)
Platform Infra master at checkpoint: b1a0c185e3f97630aa2bf55945bb5f674200bf97
Latest checkpoint: docs/cross-repo-workflow-inventory-checkpoints/2026-11-06-0838-ict.md

## Current review — 2026-11-06 01:58 ICT (2026-11-05 18:58 UTC)

This review re-read all five default-branch refs, open PRs, recent Actions runs, current open-PR heads, Platform native schedule history, the active reconciliation and its lane logs, TCE native WF-06/WF-13/fallback runs, and the current runtime snapshot. It supersedes the 00:56 review below.

### Current repository refs and open PRs

| Repository | Default branch SHA | Open PRs | Latest evidence in this review |
|---|---|---|---|
| Platform Infra | \`ffbfecaa19730a5cef9861c313a2e1597ac05eaf\` | #544/#541/#539 (draft) | Inspection snapshot PR #1286 is on master; reconciliation #42089469075 failed only Stock health; post-reconcile recovery #42089788857 passed. |
| TCE Dashboard | \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\` | None | Native WF-06 #42089383865 failed; WF-13 #42089421154 successfully dispatched exactly one fallback #42089448641, which also failed the four strict public probes. |
| StockDividend | \`50ba0dfb67eb3dfaa376db0c752bbef5b0817bec\` | None | CI #41563856934 and immutable ARM64 publisher #41563856933 passed on Nov 3; current production Admin/Backend image references remain incompatible with ARM64. |
| Media Generation | \`e4c7d8990aafc7d837e918c9caf39722d623de7c\` | None | CI #41617592783 passed on Nov 3; Media lane passed in reconciliation #42089469075. |
| Authentication | \`f978a3f378ee22d4630909c2d182275b21ac9e9a\` | #75 (ready), #76 (draft) | CI #41670642852 passed on Nov 3; Auth lane passed in #42089469075. |

Open PR heads were re-read:
- Platform #544: \`c95e7daecb83b65577b54303427fe4ea81adfe06\` (draft).
- Platform #541: \`b8f7c6ba04e3d971336a899b2efd5894662083b3\` (draft).
- Platform #539: \`2dc48b97017ecb08e49682633303a2f1d5e991a1\` (draft).
- Authentication #75: \`a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05\` (ready); latest exact-head checks remain historical: validate PASS #40446492086 (Oct 27), Supabase Preview SKIPPED.
- Authentication #76: \`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58\` (draft); validate PASS #41329425940 (Nov 1), Supabase Preview SKIPPED.
- No open PRs in TCE Dashboard, StockDividend or Media Generation. Do not describe historical PASS checks as fresh validation.

### Native schedule evidence — event types remain distinct

| Platform workflow | Latest native \`event=schedule\` run | Result |
|---|---|---|
| inspect-vps | #42049660972 — 2026-11-05 21:55:03 ICT | PASS, stale |
| reconcile-vps | #42068683835 — 2026-11-05 23:51:03 ICT | FAIL only Stock health |
| recover-stale-ops | #42068414686 — 2026-11-05 23:49:29 ICT | PASS |
| reconcile-schedule-watchdog | #42070623710 — 2026-11-06 00:02:22 ICT | FAIL inspection freshness |

The latest 100 Platform Actions runs through #42089788857 (19:00:57Z / 02:00:57 ICT) contain no native schedule run after watchdog #42070623710. Native inspection #42049660972 is 246 minutes old at the recovery API reference clock; the latest native watchdog is also stale. This is not evidence of runner queue congestion. The inspection workflow is active, and the recovery controller separately measures native schedule freshness versus workflow_dispatch fallback freshness. Preserve all existing cron declarations.

### TCE WF-13 native recovery — first post-merge end-to-end proof

- Native WF-06 schedule #42089383865 started 2026-11-06 01:58:27 ICT, on master SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, and failed all four public endpoint probes.
- WF-13 #42089421154 started at 01:58:42 ICT and completed PASS. Its source validation confirmed workflow ID \`339198323\`, path \`.github/workflows/wf-06-tce-healthcheck.yml\`, source run #42089383865, event \`schedule\`, attempt 1, master branch and exact source SHA.
- WF-13 dispatched read-only WF-06 with \`ref=master\`, exact SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, and no inputs. The job correlated the dispatch to fallback #42089448641. No deployment or mutation authority is involved.
- Fallback #42089448641 completed FAILURE: TCE web, TCE API, Auth readiness and Auth liveness all remained HTTP 503 (expected 200).
- WF-13 run #42089450102 for the subsequent WF-12 \`workflow_run\` source #42089421216 was SKIPPED; it is not a second native schedule failure and no second fallback was dispatched.
- This proves one qualifying native WF-06 failure → one WF-13 dispatch → one exact-master WF-06 fallback. It does not prove service recovery; all four endpoint probes still fail. Keep strict HTTP 200 checks and all TCE cron declarations unchanged.

### Platform heartbeat, reconciliation and release gates

- Platform recovery #42089440296 validated the TCE repository, source workflow path, source run #42089383865, event \`schedule\`, attempt 1, source SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, and WF-12 heartbeat run #42089421216.
- It dispatched the existing Platform GitOps authority with exact payload: \`ref=master\`, SHA \`ffbfecaa19730a5cef9861c313a2e1597ac05eaf\`, \`mode=apply\`, \`allow_image_changes=false\`, \`target_app=all\`.
- Reconciliation #42089469075 completed FAILURE only at the final lane gate. Shared GHCR preflight, Auth runtime Secret provisioning and GHCR credential bootstrap passed. Production manifest apply and image changes were SKIPPED; \`ALLOW_IMAGE_CHANGES=false\`.
- Media, MicroFE, TCE and Auth lanes passed their scoped checks; Keycloak lane was skipped. StockDividend lane failed: two Admin Pods and one new Backend Pod were in ImagePullBackOff on tag \`12d63b4\`, with containerd reporting \`no match for platform in manifest\`. The failure is architecture compatibility, not a shared GHCR credential failure. No half-pair promotion was attempted.
- Post-reconcile recovery #42089788857 completed PASS. It confirmed native inspection remained stale, but the last read-only workflow_dispatch snapshot #42083607462 was fresh (37 minutes old at the recovery API reference clock), so it correctly avoided a duplicate inspection dispatch. This fallback is not native schedule evidence.
- Snapshot \`debug/vps-latest.md\` was generated 2026-11-05 18:22:41Z (2026-11-06 01:22:41 ICT). At this review it is still within the 75-minute fallback budget, but it is not a new live inspection. It recorded node \`tce-k3s-01\` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, about 19 GiB available RAM, and \`restart_required=yes\`. Media/MicroFE/NATS were 1/1; Stock Admin and new Backend were ImagePullBackOff; old Backend and Frontend were 1/1; TCE frontend/service, microfe-auth and Keycloak were 0/0. Treat these as snapshot-time observations only.
- The TCE/Auth public 503 probes and the snapshot's zero-replica workloads are correlated observations, not a proven causal diagnosis. Platform TCE/Auth lane success is a scoped GitOps/runtime check and does not override the independent public HTTP healthcheck failures.
- Stock paired Admin/Backend promotion remains closed until explicit release authorization and protected publisher-run Actions:read provenance are verified. Existing Stock publisher #41563856933 proved ARM64 image builds/digests, but it does not authorize production promotion.
- Authentication #75/#76 remain gated: exact-head checks are historical and Supabase Preview was SKIPPED. The connected integration's Deploy-to-production binding/effect is not authoritatively exposed. Do not merge or run migrations.
- VPS host restart and Docker/containerd maintenance remain pending an approved maintenance window.

### Next dependency-safe actions

1. Keep the existing inspection fallback policy: do not dispatch another read-only inspect while #42083607462 remains within the 75-minute fallback budget; let the recovery controller request one when it becomes stale. Continue reporting native schedule freshness separately.
2. Investigate Platform native schedule delivery without changing cron declarations or adding a second deployment authority.
3. Keep Stock Admin/Backend paired promotion disabled until release authorization and protected publisher provenance are available.
4. Investigate why all four TCE/Auth public probes return HTTP 503; do not weaken the strict health gate or infer root cause from the older snapshot.
5. Keep Auth #75/#76 and Supabase migrations gated on authoritative integration side-effect evidence.
6. Wait for an approved VPS maintenance window before host restart or package upgrade.

### Safety invariants

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- \`reconcile-vps.yml\` remains the sole production apply authority; \`inspect-vps.yml\` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred in this review.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows.
- TCE market-scan schedule unchanged.

## Previous review — 2026-11-06 00:56 ICT (2026-11-05 17:56 UTC)

This review re-read all five default-branch refs, open PRs, latest Actions runs, exact master check-runs, open-PR head check-runs, native schedule history and the current tracker. It supersedes the 00:18 runtime snapshot below.

### Current repository refs and checks

| Repository | Master SHA | Latest master CI / publication evidence |
|---|---|---|
| Platform Infra | `37caf7ea6ec1c4833e22eb8b6ffaf03186fd0023` | PR #1284 merged; exact-head #42074105857 PASS and post-merge validate-manifests #42074228245 PASS (00:23:58 ICT). |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | WF-01 #42053388961 PASS; WF-02 #42053388868 formatting check PASS (auto-format commit step skipped); WF-05 #42053388841 PASS (22:17–22:20 ICT). |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | CI #41563856934 PASS; publisher #41563856933 built/pushed immutable images, but Platform handoff validation and atomic paired promotion were SKIPPED (Nov 3). |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | CI #41617592783 PASS (Nov 3); no newer master run. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | CI #41670642852 PASS; Supabase Preview check SKIPPED (Nov 3). |

### Current open PRs and exact-head checks

- Platform #544 draft, head `c95e7daecb83b65577b54303427fe4ea81adfe06`; validate PASS #38575430454 (Oct 14, historical).
- Platform #541 draft, head `b8f7c6ba04e3d971336a899b2efd5894662083b3`; validate PASS #38567431761 (Oct 14, historical).
- Platform #539 draft, head `2dc48b97017ecb08e49682633303a2f1d5e991a1`; validate PASS #38548718033 (Oct 14, historical).
- Authentication #75 ready, head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; validate PASS #40446492086 (Oct 27), Supabase Preview SKIPPED.
- Authentication #76 draft, head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; validate PASS #41329425940 (Nov 1), Supabase Preview SKIPPED.
- No open PRs in TCE Dashboard, StockDividend or Media Generation. All open-PR PASS checks above are historical; none is fresh validation against a new head.

### Native schedule evidence — keep event types distinct

| Workflow | Latest native `event=schedule` run | Result |
|---|---|---|
| Platform inspect-vps | #42049660972 — 2026-11-05 21:55:03 ICT | PASS, stale |
| Platform reconcile-vps | #42068683835 — 2026-11-05 23:51:03 ICT | FAIL only Stock health |
| Platform recover-stale-ops | #42068414686 — 2026-11-05 23:49:29 ICT | PASS |
| Platform schedule watchdog | #42070623710 — 2026-11-06 00:02:22 ICT | FAIL inspection freshness |
| TCE WF-06 | #42019530614 — 2026-11-05 18:30:38 ICT | FAIL; four strict public probes returned HTTP 503 |
| TCE WF-12 | #42013061466 — 2026-11-05 17:43:23 ICT | FAIL freshness |
| TCE WF-07 | #41982802263 — 2026-11-05 13:47:35 ICT | PASS |

The latest 100 Platform Actions runs contain no newer `event=schedule` inspect-vps run than #42049660972. The watchdog #42070623710 independently passed reconcile freshness (11m) and recovery freshness (12m) but failed inspection freshness (127m). Workflow_run recovery #42070696343 passed at 00:02:49 ICT; it is not a native recovery tick and skipped duplicate inspection because fallback #42063840567 was still fresh at that time. Do not attribute the missing inspect event to runner queue: the previous watchdog evidence reported queue_wait=0m.

### Runtime evidence and release gates

- Latest read-only K3s snapshot remains #42063840567, generated 2026-11-05 23:23:06 ICT by `workflow_dispatch`. At 00:56 ICT it is approximately 93 minutes old, outside the 75-minute fallback freshness budget. No newer inspect-vps snapshot was found in the latest workflow-run view; current live cluster health is therefore unverified.
- At that snapshot, node `tce-k3s-01` was Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB RAM available; GitOps drift clean; host `restart_required=yes`. Media/MicroFE/NATS were 1/1. Stock Admin and new Backend were ImagePullBackOff on `12d63b4`; previous Backend/Frontend were 1/1. TCE/Auth/Keycloak were 0/0. This is historical snapshot evidence only.
- Stock publisher #41563856933 verified immutable linux/arm64 builds and digests, but the handoff validation and atomic paired production dispatch were SKIPPED. Keep Admin/Backend promotion disabled until explicit release authorization and protected publisher-run Actions:read provenance are available.
- TCE PR #1024 recovery contract is merged and its post-merge WF-01/WF-02/WF-05 checks passed. No qualifying post-merge native WF-06/WF-12 failure has exercised WF-13 end-to-end; no fallback dispatch is claimed.
- Authentication #75/#76 remain gated: validate checks are historical, Supabase Preview was SKIPPED, and the Deploy-to-production integration binding/effect is not exposed by the authorized API. Do not merge or run migrations.
- VPS host restart and Docker/containerd maintenance remain pending an approved maintenance window.

### Next dependency-safe actions

1. Let the existing recovery controller obtain a fresh read-only inspect fallback when its native schedule next runs; do not dispatch a duplicate while a run is active or a fallback is fresh. Native schedule freshness must remain separate from workflow_dispatch freshness.
2. Continue monitoring the next native Platform watchdog and recovery ticks; preserve all existing cron declarations.
3. Keep Stock paired promotion closed until release authorization and protected publisher provenance are verified.
4. Verify one qualifying native TCE failure triggers exactly one WF-13 → WF-06 fallback with full source run/SHA correlation.
5. Keep Auth PRs and migrations gated on the Supabase production integration side-effect check.
6. Wait for an approved VPS maintenance window before host restart or package upgrade.

### Safety invariants

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred in this review.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows.
- TCE market-scan schedule unchanged.

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | `b1a0c185e3f9` | #1301 ready; #1296/#544/#541/#539 draft | PR #1301 exact head `dce6ae5341ce` has checks #42145176538/#42145176539/#42145176540 queued; no decommission merge or K3s mutation yet. |
| phanthienquoc/TCE-dashboard | `512b69d837e2` | None | Native WF-06 #42133793538 failed four strict HTTP 200 probes with 503 under the operator zero-replica state; WF-13 fallback #42133822204 PASS/read-only. TCE market-scan schedule unchanged. |
| phanthienquoc/stockdividend | `6fcefa6b3792` | None | PR #32 merged; post-merge CI #42137523269 PASS. No new publisher run or production release after merge; manual hold remains closed. |
| phanthienquoc/media-generation | `3a8846a4f273` | None | PR #72 merged; post-merge CI #42136991059 PASS. No Platform dispatch or production release after merge. |
| phanthienquoc/phanthienquoc-authentication | `f978a3f378ee` | #75 ready; #76 draft | Auth CI #41670642852 PASS (historical); PR checks #40446492086/#41329425940 are historical and Supabase Preview is SKIPPED. Production integration side-effect gate unresolved. |

## Current runtime blockers

- **Stock/Media retirement:** Platform PR #1301 is branch-only; master still owns the prior runtime until the PR is merged and the manual decommission is separately authorized. The latest committed snapshot #42131886966 is stale and omits PVC/PV/StorageClass data. No namespace or runner deletion has occurred.

- **Platform schedule delivery:** Native inspect-vps #42049660972 succeeded at 21:55:03 ICT and remains the latest native inspection; no newer `event=schedule` inspect run appears in the latest 100 Actions runs through 00:18 ICT. Native reconcile #42068683835 at 23:51:03 ICT failed only Stock health. Native recovery #42068414686 at 23:49:29 ICT passed. Watchdog #42070623710 at 00:02:22 ICT failed only inspection freshness: reconcile age 11m and recovery age 12m passed, while native inspection age was 127m. Recovery workflow_run #42070696343 passed but skipped a duplicate inspection because fallback snapshot #42063840567 was 38m old then. The fallback snapshot is about 55m old at 00:18 ICT (within the 75m fallback budget) but is not native schedule evidence.

- **K3s / Stock runtime:** Latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by `workflow_dispatch`. Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB RAM available; GitOps drift clean; host `restart_required=yes`. Media backend/frontend, MicroFE Shell/WS and NATS are 1/1. Stock Admin (two Pods) and new Backend remain ImagePullBackOff on `12d63b4` because the manifest has no matching platform; previous Backend and Frontend remain 1/1 on `23b2878`. TCE/Auth/Keycloak remain 0/0. No host reboot or package upgrade.

- **TCE health/schedule:** Latest native WF-06 #42019530614 (18:30:38 ICT) failed all four strict public probes with HTTP 503. Latest native WF-12 #42013061466 (17:43:23 ICT) failed freshness; WF-07 #41982802263 passed. PR #1024 merged the WF-13 fix: it validates native schedule source via workflow IDs 339198323 (WF-06) and 403352324 (WF-12), deduplicates, and dispatches only the read-only WF-06 fallback. No qualifying post-merge native event has exercised this path. Keep strict HTTP 200 checks and all TCE cron declarations unchanged.

- **Authentication:** Supabase project `gtqovpusfyyvxpeezxlo` reports ACTIVE_HEALTHY / PostgreSQL 17.6.1.084 and FUNCTIONS_DEPLOYED. The remote migration ledger matches all 84 local migration files exactly. PR #75/#76 remain 11 commits behind master; #75 is ready and #76 draft. The owner-provided integration setting still shows Deploy to production ON for Auth master, but the binding/effect is not exposed by the authorized API. Keep both PRs open; do not merge or run migrations.

- **VPS maintenance:** Latest inspection reports host restart required and pending Docker/containerd maintenance. No approved maintenance window is evidenced; do not reboot or upgrade packages.

- **VPS Control MCP:** PR #1268 is merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`; `apps/tce-vps-control-mcp/package-lock.json` is committed (lockfile v3; 94 package entries). PR #1280 is merged as `d4705442de747c80ace35d14f7dee209e25fe6ac` and excludes MCP-only paths from recovery bootstrap. The MCP remains diagnostics-only with no Docker/Kubernetes mutation authority.

- **Stock release authorization:** Immutable ARM64 publisher #41563856933 verified Scraper/Admin/Backend digests, but paired production promotion remains disabled until explicit release authorization and protected publisher-run Actions:read provenance are available.

- **Superseded MCP proposal:** Platform PR #1222 is closed and not merged; it is not an open PR or production authority. The diagnostics-only replacement is #1268.

## Current operational status

- **Platform master:** `37caf7ea6ec1c4833e22eb8b6ffaf03186fd0023`. PR #1284 merged; exact-head validate-manifests #42074105857 and post-merge #42074228245 PASS. PR #1283/#1282/#1281/#1280 and diagnostics-only MCP #1268 are also merged. The latest documentation-only merge did not trigger production apply.
- **Platform native schedules:** inspect-vps #42049660972 (21:55:03 ICT, PASS but stale); reconcile-vps #42068683835 (23:51:03 ICT, Stock health failure); recover-stale-ops #42068414686 (23:49:29 ICT, PASS); watchdog #42070623710 (00:02:22 ICT, FAIL only native inspection freshness). Workflow_run recovery #42070696343 passed and skipped another inspection fallback because #42063840567 was still fresh. Native inspection and fallback freshness remain separate.
- **Fallback and native reconciliation:** Recovery schedule #42068414686 verified fallback reconcile #42068463484 with exact payload `ref=master`, SHA `d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. Fallback #42068463484 and native #42068683835 passed shared preflight, GHCR access and credential bootstrap; GitOps drift was false and production apply/image changes were skipped. TCE/Auth/MicroFE/Media lanes passed; Stock health failed.
- **K3s:** Latest snapshot #42063840567 generated at 23:23:06 ICT by workflow_dispatch; about 55m old at this checkpoint. Node Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM; GitOps drift clean; restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1 on `23b2878`; TCE/Auth/Keycloak 0/0. No reboot or host package upgrade.
- **TCE:** master `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; PR #1024 recovery fix merged and post-merge WF-01 #42053388961/WF-02 #42053388868/WF-05 #42053388841 PASS. Latest native WF-06 #42019530614 returned HTTP 503 on all four public endpoints; WF-12 #42013061466 failed freshness; WF-07 #41982802263 PASS. No post-merge native WF-13 E2E dispatch. No TCE schedule changed.
- **StockDividend:** master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; CI #41563856934 and immutable publisher #41563856933 PASS. Publisher built/verified ARM64 manifests for Scraper/Admin/Backend, but Platform handoff validation and atomic paired production promotion were SKIPPED. Production tag `12d63b4` still lacks matching ARM64 manifests; no paired promotion without authorization/provenance.
- **Media Generation:** master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; CI #41617592783 PASS; backend/frontend 1/1 in the 23:23 snapshot.
- **Authentication:** master `f978a3f378ee22d4630909c2d182275b21ac9e9a`; CI #41670642852 PASS. Supabase project ACTIVE_HEALTHY / FUNCTIONS_DEPLOYED; migration set matches 84/84. PR #75/#76 remain open and 11 commits behind master; PR #75 Deploy-to-production side-effect gate remains unresolved.

## Current PR heads and validation

- Platform #1283 merged as `be13f089e665de5ad23df6209c3a0831a6a5e295`; exact-head validate-manifests #42071477343 PASS and post-merge #42071588610 PASS. It updated tracker/inventory/checkpoint only.
- Platform #1282 merged as `6c2b826175d135b41fcb69f28ca2268391c357c2`; exact-head #42069918051 and post-merge #42070150263 PASS.
- Platform #1281 merged as `cd5f9001f826a3a25cf992289176df827ac28c77`; exact-head #42068751747 and post-merge #42068869578 PASS.
- Platform #1280 merged as `d4705442de747c80ace35d14f7dee209e25fe6ac`; exact-head validate-github-actions #42066670909 and validate-manifests #42066667137 PASS; post-merge #42067822505/#42067839646 PASS.
- Platform #1268 merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`; diagnostics-only MCP lockfile committed, no Docker/Kubernetes mutation capability. Platform #544/#541/#539 remain old draft proposals and are not deployment approvals.
- TCE #1024 merged as `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; exact-head WF-05 #42053173288/WF-02 #42053173277 and post-merge WF-01 #42053388961/WF-02 #42053388868/WF-05 #42053388841 passed. No post-merge native WF-13 E2E is evidenced.
- Authentication #75 is ready at `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` (28 ahead/11 behind master); #76 remains draft at `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` (3 ahead/11 behind). Their latest `validate` checks #40446492086/#41329425940 are historical; Supabase Preview was skipped. Keep both gated on integration side effects and refresh branches conflict-safely before any future merge.
- Current open PRs: Platform #544/#541/#539 (all draft); Authentication #75 (ready)/#76 (draft); no open PRs in TCE, StockDividend or Media Generation.
- StockDividend and Media Generation have no fresh master CI since Nov 3; current runs remain #41563856934/#41563856933 and #41617592783 respectively. Treat them as historical checks, not fresh CI.

## Current actions

1. Poll Platform PR #1301 exact-head checks #42145176538, #42145176539 and #42145176540; fix failures and revalidate the updated head before any merge.
2. Squash-merge #1301 only when all required checks pass on the current head; close the superseded plan-only PR #1296 after the implementation PR is accepted.
3. Before namespace deletion, obtain a fresh same-window inventory of all namespaced resources, PVCs, PVs and StorageClasses; verify backups/external data and independently stop/unregister the dedicated Media runner.
4. After the guarded manual decommission, capture a fresh read-only inspection and verify TCE/Auth/MicroFE/Keycloak remain unchanged.
5. Keep Stock production publication and paired promotion disabled until explicit release authorization and protected publisher provenance are available.
6. Keep Authentication #75/#76 gated on authoritative Supabase production integration side-effect evidence; do not merge or run migrations.
7. Observe TCE WF-06/WF-13 recovery while preserving strict HTTP 200 checks and every TCE schedule, especially the market-scan schedule.
8. Wait for an approved VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

## Ownership and safety invariants

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
- WF-12 remains read-only; isolated WF-13 may only dispatch the public HTTP-only WF-06 healthcheck.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- No production image promotion, production manifest apply, database migration, desired replica change, host package upgrade, reboot or cron declaration change occurred in this checkpoint.
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


# Cross-repo deployment checkpoint — 2026-11-05 19:56 ICT / 12:56 UTC

## Repository heads and open PRs

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | 9c931c51e51ddc4ae3f55e3a4f3c266122d86f55 | #1268 draft; #544/#541/#539 draft |
| TCE Dashboard | a7b26b21782e4031364a9559b6eefdc2e654cc1e | None |
| StockDividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None |
| Media Generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft |

Platform PR #1222 is closed and not merged. It is not an active open PR. The diagnostics-only proposal currently under review is PR #1268.

## Platform Infra

- Master commit `9c931c51e51ddc4ae3f55e3a4f3c266122d86f55`; master validate-manifests #42030024927 completed PASS.
- PR #1268 exact head `81dfa692dc4a0b363314da72cac6700f1d7f514f`, branch `security/vps-mcp-readonly-boundary-20261105-1855-ict`.
- Exact-head validate-github-actions #42030355670, validate-manifests #42030355586 and dedicated MCP validation #42030355637 all completed PASS.
- Dedicated MCP job #127254938646 ran: generate lockfile, install exact lockfile dependencies with `npm ci`, security contract tests, typecheck, build, shell syntax and ShellCheck; every step passed.
- Artifact #13416365990 was downloaded. Artifact ZIP SHA-256: `243c49c8dacd401f777a666803f05981373a555a40544497a6cdd7119e3a0933`. Extracted package-lock SHA-256: `105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0`.
- Lockfile validation: lockfileVersion 3; 94 package entries including root; exact root dependencies and devDependencies match package.json; all 93 dependency entries have integrity hashes; all resolved tarballs use HTTPS registry.npmjs.org. The lockfile is still not committed on the PR branch, so PR #1268 remains draft.
- No production deployment or host mutation was attempted.

## Native schedule evidence and K3s

An explicit Actions API query filtered to `event=schedule` returned the following latest Platform runs:

| Workflow | Run | Local time | Result |
|---|---:|---:|---|
| inspect-vps | #41980605875 | 13:28:06 | PASS, stale |
| reconcile-vps | #41995809261 | 15:36:40 | FAIL, Stock health |
| recover-stale-ops | #41994805588 | 15:29:01 | PASS, stale |
| schedule watchdog | #41997764646 | 15:51:58 | FAIL, inspection freshness |

No newer native Platform schedule events were returned at 19:56 ICT. Manual recovery/inspection runs remain distinct from native schedule evidence.

Latest K3s snapshot is fallback #42013436672, generated at 17:46:16 ICT. It is about 130 minutes old and exceeds the 75-minute freshness budget. At snapshot time: node Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB RAM available; host restart_required=yes. Media/MicroFE/NATS 1/1. Stock Admin and new Backend ImagePullBackOff on 12d63b4; previous Backend/Frontend 1/1. TCE/Auth/Keycloak 0/0. This is historical evidence, not current health.

## TCE schedule and public health

- Latest native WF-06 #42019530614 at 18:30:38 ICT failed all four strict public probes with HTTP 503: TCE web, TCE API, Auth readiness and Auth liveness.
- Latest native WF-12 #42013061466 at 17:43:23 ICT failed freshness.
- WF-12 workflow_run #42019562593 completed successfully after WF-06, but WF-13 #42019590810 was correctly skipped because its source event was `workflow_run`, not `schedule`.
- No qualifying native WF-12 event has exercised WF-13 end-to-end. Keep HTTP 200 and 25-minute freshness gates. No cron declaration or market-scan schedule changed.

## Stock, Media and Authentication

- Stock CI #41563856934 and publisher #41563856933 passed on master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. Publisher verified immutable linux/arm64 full-source-SHA digests: Scraper `6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`, Admin `a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`, Backend `cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. Production paired promotion remains disabled pending authorization and protected publisher provenance.
- Media CI #41617592783 passed on master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; runtime 1/1 evidence is only from the stale 17:46 snapshot.
- Authentication CI #41670642852 passed on master `f978a3f378ee22d4630909c2d182275b21ac9e9a`. PR #75/#76 remain gated by Supabase production binding and migration provenance.

## Exact next actions

1. Commit the reviewed lockfile to PR #1268's dedicated branch and rerun exact-head checks; keep draft until complete.
2. Obtain a fresh read-only K3s snapshot through the existing inspection authority when authorized Actions dispatch access is available.
3. Observe a qualifying native WF-12 schedule failure and verify one correlated WF-13 to WF-06 fallback dispatch.
4. Keep Stock paired promotion, Auth migration and TCE/Auth replica activation blocked pending their separate authorizations.
5. Investigate the four TCE HTTP 503 probes without weakening gates.
6. Wait for approved VPS maintenance before reboot or package upgrades.

## Safety invariants

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, manifest apply, database migration, desired replica change, host package upgrade, reboot or cron expression change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

## Evidence

- Platform master validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030024927
- PR #1268: https://github.com/phanthienquoc/platform-infra/pull/1268
- PR #1268 GitHub Actions validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030355670
- PR #1268 manifest validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030355586
- PR #1268 MCP validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030355637
- TCE WF-06: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019530614
- TCE WF-12 native: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42013061466
- TCE WF-13 skipped: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019590810
- Stock CI: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock immutable publisher: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Authentication CI: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment checkpoint — 2026-11-05 20:59 ICT / 13:59 UTC

## Repository heads and open PRs

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | 30db773980223132997a3e98c9703c4e2d90c70a | #1268 draft; #544/#541/#539 draft |
| TCE Dashboard | a7b26b21782e4031364a9559b6eefdc2e654cc1e | None |
| StockDividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None |
| Media Generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft |

PR state was read from the current GitHub open-PR collections. Platform #1222 remains closed/unmerged and is not counted as open.

## Latest workflow and exact-head evidence

- Platform master validate-manifests #42032333095 completed successfully on master 30db773980223132997a3e98c9703c4e2d90c70a.
- Platform PR #1268 current head is 81dfa692dc4a0b363314da72cac6700f1d7f514f. Exact-head validate-github-actions #42030355670, validate-manifests #42030355586 and dedicated MCP validation #42030355637 all passed. The reviewed lockfile artifact #13416365990 remains absent from the PR branch; the PR stays draft.
- TCE latest native WF-06 schedule #42019530614 (18:30:38 ICT) failed all four public HTTP 200 probes. Latest native WF-12 schedule #42013061466 (17:43:23 ICT) failed freshness. WF-12 workflow_run #42019562593 completed successfully after WF-06; WF-13 #42019590810 was correctly skipped because its source event was workflow_run, not schedule. No qualifying WF-13 native-schedule recovery dispatch is evidenced.
- StockDividend CI #41563856934 and immutable publisher #41563856933 passed on master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec.
- Media CI #41617592783 passed on master e4c7d8990aafc7d837e918c9caf39722d623de7c; runtime evidence remains stale.
- Authentication CI #41670642852 passed on master f978a3f378ee22d4630909c2d182275b21ac9e9a. Auth PR #75 exact-head run #40446492086 passed on head a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05; this does not clear its external Supabase deployment side-effect gate.

## Deployment authority audit

Reviewed the active application publisher/release workflows and Platform promotion/apply workflows:

| Repository | Workflow | Responsibility | Direct production mutation |
|---|---|---|---|
| TCE Dashboard | wf-03-tce-production-deploy.yml | Manual build, immutable image publication, release request to Platform Infra | None found in this publisher path |
| StockDividend | deploy.yml | Master publication and optional manual release request; production promotion explicitly disabled | None found in this publisher path |
| Media Generation | wf-03-media-production-deploy.yml | Manual build, immutable image publication, release request to Platform Infra | None found in this publisher path |
| Authentication | release.yml | Manual immutable image publication and digest handoff to Platform Infra | None found in this publisher path |
| Platform Infra | gitops-image-promotion.yml | Verify source provenance/digests, update digest-pinned GitOps manifests and await master convergence | GitOps promotion only |
| Platform Infra | reconcile-vps.yml | Apply production manifests, reconcile credentials, verify rollout and health | Sole production apply authority |

No second direct SSH/Compose or application-owned kubectl apply authority was found in the reviewed publisher paths. Keep manual/release workflows: they are purposeful app-owned publishers, not duplicate deployers.

## Native schedules and runtime freshness

The explicit Platform Actions query filtered to event=schedule still returns these latest runs:

| Workflow | Latest native run | Result |
|---|---|---|
| inspect-vps | #41980605875 — 13:28:06 ICT | PASS, stale |
| reconcile-vps | #41995809261 — 15:36:40 ICT | FAIL, Stock health |
| recover-stale-ops | #41994805588 — 15:29:01 ICT | PASS, stale |
| schedule watchdog | #41997764646 — 15:51:58 ICT | FAIL, inspection freshness |

No later native Platform schedule runs were returned at this checkpoint. Do not count workflow_dispatch or workflow_run fallbacks as native schedule evidence.

Latest K3s evidence remains fallback snapshot #42013436672 generated at 17:46:16 ICT, now more than three hours old and beyond the 75-minute freshness budget. Historical snapshot: node Ready/ARM64, disk 56%, about 19 GiB available RAM, Media/MicroFE/NATS 1/1, Stock Admin and new Backend ImagePullBackOff on 12d63b4, previous Backend/Frontend 1/1, TCE/Auth/Keycloak 0/0, host restart required. This is not current health evidence.

## Release and safety gates

- Stock publisher #41563856933 verified immutable linux/arm64 full-source-SHA digests: Scraper sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2, Admin sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e, Backend sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a. Production paired promotion remains disabled pending explicit authorization and protected publisher-run Actions:read provenance.
- Auth PR #75 remains open even though its exact-head CI passed. Owner-provided Supabase evidence says GitHub integration Deploy to production is ON for master; the 2026-11-02 read-only ledger check found 84 local/remote migration versions matching, but the historical failed deployment state and exact merge-triggered side effect remain unresolved. Do not merge or dispatch release workflows.
- Platform MCP PR #1268 remains draft. Lockfile artifact ZIP SHA-256 243c49c8dacd401f777a666803f05981373a555a40544497a6cdd7119e3a0933; extracted lockfile SHA-256 105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0; lockfile v3, 94 package entries, 93 dependency entries with integrity and HTTPS npm registry URLs. It is verified but not committed.
- No production image promotion, manifest apply, database migration, desired replica change, host maintenance, reboot or cron expression change occurred.
- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
- TCE market-scan schedule remains unchanged.

## Exact next actions

1. Commit the reviewed MCP lockfile to PR #1268's dedicated branch and rerun all exact-head checks; keep draft until then.
2. Obtain a fresh read-only K3s inspection through the existing Platform inspection authority when dispatch access is available.
3. Observe a qualifying native WF-12 schedule failure and verify exactly one correlated WF-13 → WF-06 fallback dispatch.
4. Keep Stock paired promotion, Auth migration/release, and TCE/Auth replica activation blocked until their separate provenance/authorization gates are satisfied.
5. Investigate TCE's four HTTP 503 probes without weakening strict HTTP 200 or freshness gates.
6. Wait for an approved VPS maintenance window before reboot or package upgrades.

## Evidence

- Platform master validation #42032333095: https://github.com/phanthienquoc/platform-infra/actions/runs/42032333095
- Platform PR #1268: https://github.com/phanthienquoc/platform-infra/pull/1268
- Platform PR #1268 exact-head checks: #42030355670, #42030355586, #42030355637
- TCE WF-06 #42019530614: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019530614
- TCE WF-12 native #42013061466: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42013061466
- TCE WF-12 workflow_run #42019562593: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019562593
- TCE WF-13 skipped #42019590810: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019590810
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth master CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75 exact-head CI #40446492086: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/40446492086


# Cross-repo deployment checkpoint — 2026-11-05 23:30 ICT / 16:30 UTC

## Repository heads and open PRs

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `a239187b7694a02dedb2b7ade6b31e0be139ac44` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra changes merged

- PR #1268 merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`. It adds the optional diagnostics-only VPS MCP with committed lockfile and read-only GitOps-subordinate permissions. Exact-head checks #42063067665, #42063067491 and #42063067460 passed; post-merge checks #42063703576, #42063703585 and #42063703609 passed.
- PR #1276 merged as `22a8d4f0807f41f26ed1cba6ebcd96e3afc662fa` after inspection #42063840567. This records a fresh read-only snapshot generated at 23:23:06 ICT.
- PR #1278 merged as `a239187b7694a02dedb2b7ade6b31e0be139ac44`. It excludes `apps/tce-vps-control-mcp/**` from `reconcile-vps.yml` push paths and explicitly treats MCP paths as non-production in the push-scope resolver. Exact-head checks #42064383310, #42064383238 and #42064383170 passed; post-merge checks #42064588984, #42064588923 and #42064588960 passed on current master.
- PRs #1275 and #1277 were closed unmerged after their branches became stale/diverged from master; their evidence is superseded by this checkpoint and the merged #1278 fix.

## Reconcile failure and recovery evidence

- The MCP merge initially triggered `Reconcile VPS — push-auto` run #42063703873 because the old path filter included all `apps/**`.
- The run failed closed at `Resolve push deployment scope` with: `Unclassified production-trigger path 'apps/tce-vps-control-mcp/.env.example'; refusing broad push reconciliation.`
- All credential bootstrap, restart, Auth secret provisioning, manifest apply and rollout steps were skipped. No production mutation occurred.
- Recovery controller #42063793863 completed successfully and dispatched read-only inspection #42063840567 (`workflow_dispatch`), which passed. This is a manual/fallback inspection, not a native schedule tick.
- After #1278 merged, master validation #42064588984/#42064588923/#42064588960 all passed. No `reconcile-vps.yml` run was triggered by the #1278 merge itself; the workflow and resolver path filters now keep the diagnostics-only MCP out of production deployment scope.
- The resolver still rejects unclassified paths and now tests both MCP-only (no production scope) and mixed TCE+MCP (TCE-only scope) changes.

## Current K3s evidence

Latest snapshot in `debug/vps-latest.md` was generated at 23:23:06 ICT by inspection #42063840567 (workflow_dispatch), not by a native schedule.

- K3s node `tce-k3s-01`: Ready / ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3.
- Disk 56%; about 19 GiB RAM available; GitOps drift status clean.
- Media backend/frontend, MicroFE Shell/WS and NATS are 1/1 Running.
- Stock Admin (two Pods) and new Stock Backend remain ImagePullBackOff on `12d63b4` with `no match for platform in manifest`; old Backend and Frontend remain 1/1 on `23b2878`.
- TCE frontend/service and Auth/Keycloak remain 0/0. Do not activate them without separate approval.
- Host reports `restart_required=yes`. No host restart or package upgrade was performed.

This snapshot is fresh operational evidence, but it does not replace native schedule evidence.

## Native schedule history

Latest native Platform schedule runs remain:
- inspect-vps #42049660972 — PASS at 21:55:03 ICT (older than the 23:23 fallback snapshot).
- reconcile-vps #41995809261 — FAIL (Stock health).
- recover-stale-ops #41994805588 — PASS but stale.
- schedule watchdog #41997764646 — FAIL freshness.

Latest native TCE schedule runs remain:
- WF-06 #42019530614 — FAIL at 18:30:38 ICT, four public HTTP 200 probes failed.
- WF-12 #42013061466 — FAIL freshness at 17:43:23 ICT.
- WF-13 #42019590810 was skipped because its source was a non-native `workflow_run` event. No post-merge native WF-13 → WF-06 E2E recovery has been evidenced.
- TCE post-merge WF-01 #42053388961, WF-02 #42053388868 and WF-05 #42053388841 all passed.

Do not count workflow_dispatch/workflow_run fallback as native schedule delivery.

## Application release state

- **TCE:** master `c5415f8ac0aa`; build/format/unit tests pass. Public health still fails while TCE workloads are 0/0. Keep strict HTTP 200 gates; do not activate workloads or alter any TCE cron.
- **StockDividend:** master `50ba0dfb67eb`; CI #41563856934 and immutable ARM64 publisher #41563856933 pass. Three component digests remain verified, but paired production promotion is blocked on explicit release authorization and protected publisher provenance. Production tag `12d63b4` has no matching ARM64 manifest.
- **Media:** master `e4c7d8990aaf`; CI #41617592783 passes; backend/frontend 1/1 in the latest snapshot.
- **Authentication:** master `f978a3f378ee`; CI #41670642852 passes. PR #75/#76 remain gated on Supabase production binding and migration provenance.

## MCP lockfile and authority

- PR #1268 committed `apps/tce-vps-control-mcp/package-lock.json` (blob `e768247f2394a203c917edd81d39343ee55a896d`), lockfile v3, 94 entries including root, 93 dependencies with integrity and HTTPS npm registry URLs. SHA-256: `105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0`.
- Dedicated validation uses `npm ci` against the committed lockfile, Node 22, security tests, typecheck, build and ShellCheck. Workflow permissions are read-only and checkout credentials are disabled.
- MCP only exposes diagnostics; no Docker restart, Kubernetes mutation, SSH or Compose deployment authority. `reconcile-vps.yml` remains the sole production apply authority.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health.
- No production image promotion, manifest apply, database migration, desired replica change, host reboot/package upgrade or cron expression change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

## Exact next actions

1. Observe the next native Platform schedule tick; do not substitute the 23:23 workflow_dispatch inspection.
2. Repair native recovery/watchdog delivery while preserving the existing schedule expressions.
3. Observe a qualifying native TCE WF-06/WF-12 failure and verify exactly one correlated WF-13 → WF-06 fallback.
4. Keep Stock paired promotion blocked until explicit release authorization and protected publisher provenance are available.
5. Keep Auth PR #75/#76 gated until Supabase deployment side effects and migration provenance are resolved.
6. Wait for an approved maintenance window before host restart or package upgrades.


# Cross-repo deployment checkpoint — 2026-11-05 23:44 ICT / 16:44 UTC

## Repository heads and open PRs

All five default-branch refs, open PRs, latest Actions runs/checks, native schedule history and the deployment tracker were re-read.

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `d4705442de747c80ace35d14f7dee209e25fe6ac` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra — PR #1280 merged

PR [#1280](https://github.com/phanthienquoc/platform-infra/pull/1280) was merged with squash after re-reading the exact PR head `7618eb7f243ad7e67b667c0d11fa06a09044024a`, confirming the PR was open/non-draft/mergeable, confirming it was 2 commits ahead and 0 behind current master, and verifying both exact-head checks passed.

- Merge SHA: `d4705442de747c80ace35d14f7dee209e25fe6ac`.
- Exact-head validate-github-actions [#42066670909](https://github.com/phanthienquoc/platform-infra/actions/runs/42066670909): PASS.
- Exact-head validate-manifests [#42066667137](https://github.com/phanthienquoc/platform-infra/actions/runs/42066667137): PASS.
- Post-merge validate-github-actions [#42067822505](https://github.com/phanthienquoc/platform-infra/actions/runs/42067822505): PASS.
- Post-merge validate-manifests [#42067839646](https://github.com/phanthienquoc/platform-infra/actions/runs/42067839646): PASS.

The change excludes `apps/tce-vps-control-mcp/**` from the recovery controller's production bootstrap push paths and extends `validate-workflow-contracts.py` to enforce the exclusion in both recovery and reconciliation filters. Resolver regression assertions cover MCP-only changes as no production scope and mixed TCE+MCP changes as TCE-only scope. The existing `reconcile-vps.yml` remains the only production apply authority. No schedule expression changed, and the TCE market-scan schedule is untouched.

## Post-merge and runtime evidence

- Latest Platform master validation runs on merge SHA d470544: #42067822505 and #42067839646 both PASS. No reconcile-vps or production mutation run was triggered by this docs-independent recovery-filter fix.
- Platform #1268 had already merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`; its diagnostics-only MCP package-lock is committed. #1280 closes the follow-on recovery push-filter gap discovered when the MCP-only merge triggered recovery bootstrap.
- Latest native Platform schedules returned by explicit `event=schedule` query: inspect-vps #42049660972 PASS at 21:55:03 ICT; reconcile-vps #41995809261 FAIL at 15:36:40 ICT on Stock health; recover-stale-ops #41994805588 PASS at 15:29:01 ICT but stale; watchdog #41997764646 FAIL at 15:51:58 ICT on freshness. No newer native schedule events were returned.
- Latest native TCE schedules: WF-06 #42019530614 FAIL at 18:30:38 ICT (four public HTTP 503 probes); WF-12 #42013061466 FAIL at 17:43:23 ICT; WF-07 #41982802263 PASS at 13:47:35 ICT. No later native schedule events were returned. WF-13's post-merge E2E dispatch remains unproven.
- Latest read-only K3s snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch, not native schedule. Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM available; GitOps drift clean; host restart_required=yes. Media backend/frontend, MicroFE Shell/WS and NATS 1/1. Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due no matching platform manifest; old Backend/Frontend 1/1 on `23b2878`. TCE/Auth/Keycloak 0/0.
- Stock publisher #41563856933 on master built/pushed Scraper, Admin and Backend on a native ARM64 runner and verified immutable manifests successfully. Its explicit production promotion gate passed only as a guard; Platform handoff validation and atomic paired digest dispatch were SKIPPED. No release authorization/protected provenance handoff is evidenced, so do not promote.
- Media CI #41617592783 PASS; the 23:23 snapshot showed backend/frontend 1/1. Authentication master CI #41670642852 PASS. PR #75 current head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` has historical validate PASS #40446492086 (2026-10-27) and Supabase Preview SKIPPED; PR body still reports Deploy to production ON and unresolved merge-triggered migration effects. PR #76 remains draft with historical validate #41329425940 PASS and Preview SKIPPED.
- TCE master `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; PR #1024 recovery fix and WF-01/WF-02/WF-05 post-merge checks remain PASS. No qualifying post-merge native schedule event has exercised WF-13.

## Next dependency-safe actions

1. Continue observing native Platform schedule delivery; use the existing read-only inspection path for a fresh K3s snapshot, and keep schedule/manual/fallback evidence distinct.
2. Verify one qualifying native TCE WF-06/WF-12 failure causes exactly one WF-13 → WF-06 fallback with full source run and SHA correlation.
3. Keep Stock paired Admin/Backend promotion disabled until explicit release authorization and protected publisher-run Actions:read provenance are verified.
4. Keep Auth #75/#76 gated until the actual Supabase production integration binding and migration side effects are authoritatively verified.
5. Wait for an approved VPS maintenance window before host restart or Docker/containerd/Ubuntu upgrades.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred.
- Useful CI/security/backup/manual/release/scheduled workflows remain preserved.
- TCE market-scan schedule unchanged.


# Cross-repo deployment checkpoint — 2026-11-05 23:53 ICT / 16:53 UTC

## Repository heads and PRs

All five default-branch refs, open PRs, latest Actions runs/checks, deployment tracker and native schedule history were re-read.

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `cd5f9001f826a3a25cf992289176df827ac28c77` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra PR #1281 merged

- PR [#1281](https://github.com/phanthienquoc/platform-infra/pull/1281) merged with squash as `cd5f9001f826a3a25cf992289176df827ac28c77`.
- Exact-head validate-manifests [#42068751747](https://github.com/phanthienquoc/platform-infra/actions/runs/42068751747) PASS.
- Post-merge validate-manifests [#42068869578](https://github.com/phanthienquoc/platform-infra/actions/runs/42068869578) PASS.
- The merge updated only the deployment tracker, workflow inventory and checkpoint. No production manifest or runtime resource changed.

## New native schedule and dispatch evidence

- Native recover-stale-ops [#42068414686](https://github.com/phanthienquoc/platform-infra/actions/runs/42068414686) completed PASS at 23:49:29 ICT.
- Its job log proves it detected master reconciliation #42063703873 at age 27m and dispatched the existing `reconcile-vps.yml` authority with exact payload: `ref=master`, `sha=d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. It correlated fallback run [#42068463484](https://github.com/phanthienquoc/platform-infra/actions/runs/42068463484). This is a workflow_dispatch fallback initiated by a native recovery tick, not a native reconciliation tick.
- Fallback reconcile #42068463484 passed shared preflight, GHCR access and credential bootstrap; GitOps drift was false, so production manifest apply and image changes were skipped. TCE, Auth, MicroFE and Media lanes passed; Stock health failed on two Admin Pods and the new Backend Pod in ImagePullBackOff.
- Native scheduled reconcile [#42068683835](https://github.com/phanthienquoc/platform-infra/actions/runs/42068683835) started at 23:51:03 ICT and completed FAILURE only because the StockDividend lane failed. Shared reconciliation/preflight passed, drift was false and production apply was skipped. TCE/Auth/MicroFE/Media lanes passed their scoped checks.
- Watchdog [#42068511916](https://github.com/phanthienquoc/platform-infra/actions/runs/42068511916) ran at 23:50:05 ICT after the native recovery tick but before #42068683835 started. It failed because the latest native reconcile then was #41995809261 at age 493m and latest native inspect #42049660972 at age 115m. It did verify recovery #42068414686 PASS. The later #42068683835 run post-dates the watchdog and cannot retroactively make that watchdog green.
- Recovery controller [#42068810024](https://github.com/phanthienquoc/platform-infra/actions/runs/42068810024) completed PASS after fallback reconcile #42068463484 and correctly skipped another inspection dispatch because the latest read-only snapshot was still within the 75-minute freshness budget.

## K3s and application state

Latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch, not native schedule. It is about 30 minutes old at this checkpoint.

- Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM available; GitOps drift clean; restart_required=yes.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` because the registry manifest has no matching platform; old Backend and Frontend 1/1 on `23b2878`.
- TCE/Auth/Keycloak remain 0/0. The successful TCE/Auth reconciliation-lane checks are not evidence that the four public WF-06 HTTP endpoints are healthy.
- Latest native TCE WF-06 remains #42019530614 (HTTP 503 on all four probes); latest native WF-12 remains #42013061466 (freshness failure); WF-07 #41982802263 passed. No post-merge WF-13 native E2E dispatch is evidenced.
- Stock immutable publisher #41563856933 passed ARM64 build/push and manifest verification for Scraper/Admin/Backend, but Platform handoff and atomic paired production promotion were SKIPPED. No explicit release authorization or protected publisher Actions:read provenance is available; do not promote.
- Media CI #41617592783 PASS; snapshot showed backend/frontend 1/1. Auth CI #41670642852 PASS; PR #75/#76 remain gated on Supabase Deploy to production binding and migration provenance.

## Next actions

1. Observe the next native inspect-vps tick; current recovery schedule is delivering, but native inspection remains stale.
2. Check the next watchdog after #42068683835; reconcile freshness should now be based on the new native schedule, but inspect freshness remains unresolved.
3. Keep Stock paired Admin/Backend promotion closed until explicit authorization and protected publisher provenance.
4. Verify a qualifying native TCE failure triggers exactly one WF-13 → WF-06 fallback with full source run/SHA correlation.
5. Keep Auth PRs and migrations blocked until Supabase integration side effects are authoritatively known.
6. Wait for an approved host maintenance window.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns manifests, shared GHCR pull credentials, provenance/digest checks, paired promotion, reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No production image/manifest/database/replica/host/cron mutation occurred. No reboot or package upgrade.
- No duplicate SSH/Compose/MCP mutation authority.
- TCE market-scan schedule unchanged.


# Cross-repo deployment checkpoint — 2026-11-06 00:03 ICT / 2026-11-05 17:03 UTC

## Repository heads and PRs

All five default-branch refs, open PRs, latest Actions runs/checks, deployment tracker, explicit native schedule history and read-only Supabase migration state were re-read.

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `6c2b826175d135b41fcb69f28ca2268391c357c2` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra PR #1282 merged

- PR [#1282](https://github.com/phanthienquoc/platform-infra/pull/1282) merged with squash as `6c2b826175d135b41fcb69f28ca2268391c357c2`.
- Exact-head validate-manifests [#42069918051](https://github.com/phanthienquoc/platform-infra/actions/runs/42069918051) PASS.
- Post-merge validate-manifests [#42070150263](https://github.com/phanthienquoc/platform-infra/actions/runs/42070150263) PASS.
- The PR changed only tracker/inventory/checkpoint documentation. No production manifest or runtime resource changed.

## Native schedule evidence after PR #1282

- Native recover-stale-ops #42068414686 PASS at 23:49:29 ICT. It dispatched fallback reconcile #42068463484 with exact payload `ref=master`, SHA `d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`.
- Native reconcile #42068683835 at 23:51:03 ICT completed FAILURE only on Stock health. Shared preflight passed, drift was false, production apply/image changes were skipped; TCE/Auth/MicroFE/Media lanes passed their scoped checks.
- Native watchdog [#42070623710](https://github.com/phanthienquoc/platform-infra/actions/runs/42070623710) ran at 00:02:22 ICT and failed only native inspect freshness. It passed native reconcile #42068683835 at age 11m (freshness pass despite Stock health conclusion=FAIL) and native recovery #42068414686 at age 12m (PASS). It failed because native inspect-vps #42049660972 at 21:55:03 ICT was 127m old.
- Recovery controller [#42070696343](https://github.com/phanthienquoc/platform-infra/actions/runs/42070696343) completed PASS after the watchdog. It confirmed the latest workflow_dispatch inspection fallback #42063840567 was 38m old and correctly avoided a duplicate read-only inspection. This fallback does not satisfy native schedule freshness.
- Latest native inspect-vps remains #42049660972 at 21:55:03 ICT; no later `event=schedule` inspect run was returned. The workflow is active (watchdog passed its enabled-state check); event delivery is still missing, not a runner queue failure.

## K3s and app runtime

Latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch, not native schedule. It is about 40m old at this checkpoint and within the 75-minute fallback freshness budget.

- Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM available; GitOps drift clean; restart_required=yes.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due no matching platform manifest; old Backend/Frontend 1/1 on `23b2878`.
- TCE/Auth/Keycloak remain 0/0. The TCE/Auth reconciliation lane success is not evidence that the public WF-06 HTTP endpoints are healthy.
- Latest native TCE WF-06 #42019530614 failed all four public HTTP probes with 503; latest native WF-12 #42013061466 failed freshness; WF-07 #41982802263 passed. No post-merge WF-13 native E2E dispatch is evidenced.
- Stock immutable publisher #41563856933 passed ARM64 build/push and manifest verification for Scraper/Admin/Backend, but Platform handoff and atomic paired production promotion were SKIPPED. No explicit release authorization or protected publisher Actions:read provenance is available; do not promote.
- Media CI #41617592783 PASS; snapshot showed backend/frontend 1/1. Auth CI #41670642852 PASS.

## Authentication — fresh read-only migration verification

Using the connected Supabase read-only API and GitHub recursive Git tree for Authentication master:

- Project `gtqovpusfyyvxpeezxlo`: `ACTIVE_HEALTHY`, PostgreSQL 17.6.1.084, ap-southeast-1.
- Its only listed default branch `main` / Git `master` reports `FUNCTIONS_DEPLOYED` (not the earlier historical `MIGRATIONS_FAILED` status).
- Authentication master `f978a3f378ee22d4630909c2d182275b21ac9e9a` has 84 SQL migration files; remote ledger has 84 rows; exact version/name set match 84/84, zero local-only, zero remote-only, zero duplicate prefixes.
- PR #75 changes exactly five files: three Markdown planning/task files and two tests. No `supabase/**`, runtime or workflow files. PR #75 is 28 commits ahead/11 behind master; #76 is 3 ahead/11 behind.
- Owner-provided GitHub Integration screenshot still reports Deploy to production ON for Auth repository `master`; the connected integration target/effect is not exposed by the authorized Supabase API. Keep #75/#76 open; do not merge until this external side-effect gate is authoritatively cleared. A fresh read-only evidence comment was added to PR #75 (#6664113606). No Supabase writes or migration actions occurred.

## Next actions

1. Observe the next native inspect-vps tick; keep workflow_dispatch fallback freshness separate from native schedule evidence.
2. Re-check the next watchdog; it should continue to pass reconcile/recovery freshness while failing inspection until a native inspect run arrives.
3. Keep Stock paired Admin/Backend promotion closed until explicit authorization and protected publisher provenance.
4. Verify a qualifying native TCE failure triggers exactly one WF-13 → WF-06 fallback with source-run/SHA correlation.
5. Keep Auth PRs gated on Supabase integration side effects; exact migration set alignment is now verified, but PRs are stale by 11 commits and require conflict-aware refresh before any future merge.
6. Wait for an approved host maintenance window.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns manifests, shared GHCR pull credentials, provenance/digest checks, paired promotion, reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No production image/manifest/database/replica/host/cron mutation occurred. No reboot or package upgrade.
- No duplicate SSH/Compose/MCP mutation authority.
- TCE market-scan schedule unchanged.


## Cross-repo deployment checkpoint — 2026-11-06 06:04 ICT / 2026-11-05 23:04 UTC

- **Live repository heads:** Platform Infra `20af8c89bc2230ff6eb78a58f2066301f75a27a7`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft); Auth #75 (ready)/#76 (draft); none in TCE, StockDividend or Media. Platform checks are historical (2026-10-14). Auth validate checks passed but Supabase Preview was SKIPPED; no PR merge.
- **Platform native schedules:** inspect-vps #42112599830 PASS at 21:26:04Z; recover-stale-ops #42121354158 PASS at 22:25:22Z; reconcile-vps #42121826106 FAIL at 22:28:47Z only on Stock health; watchdog #42123445690 PASS at 22:40:18Z. Watchdog measured inspect age 74m, reconcile age 11m and recovery age 14m, with 0m queue for inspection/reconcile. At 23:04Z the inspect snapshot is ~98m old (>75m freshness budget); no later native inspect/watchdog run is evidenced. Reconcile workflow_run/workflow_dispatch recovery follow-ups are not native ticks.
- **K3s snapshot:** `debug/vps-latest.md` generated 21:26:12Z; stale at this checkpoint. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, ~19 GiB RAM available, runner services active, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff; old Backend/Frontend 1/1. No live-health claim.
- **Stock:** production overlay still pins Admin/Backend to `12d63b4`. Reconcile #42121826106 used `ALLOW_IMAGE_CHANGES=false`; GHCR pull preflight passed, drift=false, apply skipped. ARM64 pull failed with `no match for platform in manifest`; permanent-failure restart guard skipped restart. Latest publisher #41563856933 and CI #41563856934 PASS on 2026-11-03; no newer publication. Paired promotion remains blocked on explicit authorization/protected provenance.
- **TCE:** current-master WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 push smoke #42105365586 PASS. WF-13 #42105390163 SKIPPED for push-smoke source. Latest native WF-07 #42098832858 PASS, WF-06 #42089383865 FAIL, WF-12 #42083178274 FAIL; all predate current master SHA. No post-merge native recovery E2E yet.
- **Media/Auth:** Media CI #41617592783 PASS (2026-11-03). Auth service CI #41670642852 PASS (2026-11-03), web CI #41542942080 PASS (2026-11-02); no newer master builds. Auth #75/#76 remain gated on Supabase Preview/deployment integration side-effect evidence.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/shared pull credentials/provenance/promotion/reconciliation/rollout/health. `reconcile-vps.yml` sole production apply authority; `inspect-vps.yml` read-only. No production image/manifest/database/secret/replica/host/cron changes; no duplicate SSH/Compose/MCP authority; TCE market-scan schedule unchanged.
