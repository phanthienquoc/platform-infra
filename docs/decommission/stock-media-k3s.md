

## Latest runtime evidence — 2026-11-07 13:01 ICT / 06:01 UTC

This section supersedes the prior Nov 6 snapshot. Source: read-only inspection run [#42345149215](https://github.com/phanthienquoc/platform-infra/actions/runs/42345149215), generated at `2026-11-07T06:01:30Z`, committed by inspection PR [#1380](https://github.com/phanthienquoc/platform-infra/pull/1380) as `958e33281b5121144848676d217a6199d92067f4`. Exact-head manifest validation #42345235423 passed before merge. The PR changed only `debug/vps-latest.md`; no production manifest or workload was changed.

- Node `tce-k3s-01` remains Ready, ARM64, K3s `v1.36.3+k3s1`, containerd runtime `2.3.2-k3s2`. Disk is 56% used with about 20 GiB free; available RAM is about 19 GiB.
- Docker is 29.1.3. Containerd package 2.2.1 is upgradable to 2.4.2; Docker CE/CLI and buildx/compose packages also have updates available. `restart_required=yes`; do not upgrade/reboot without a separate maintenance window.
- The dedicated Media runner service `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service` is active and enabled, and `/opt/media-actions-runner/bin/Runner.Listener` is present. The shared Platform runner is also active and must remain untouched.
- Both target namespaces remain Active. `media-prod` backend and frontend are each 1/1 Running. `stock-prod` has two Admin Pods and the newer Backend Pod in ImagePullBackOff on tag `12d63b4` because GHCR reports no matching `linux/arm64` manifest; the older Backend and Frontend remain Running.
- The only PVC/PV claim in the fresh snapshot is `k3s-debug/k3s-debug-logs`. No Stock/Media PVC, PV claim, VolumeSnapshot or VolumeSnapshotContent reference is listed. This is in-cluster evidence only and does not prove external database/object-storage backup, retention or ownership.
- The Media Ingress still publishes `media.mrcute.space`; Stock Ingresses remain in `stock-prod` for the retired Stock host set. The plan's host inventory includes `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space` and `api.mrcute.space`. Reconcile these against authoritative DNS/provider records before any deletion; the cluster snapshot does not prove DNS ownership.

The protected `decommission-stock-media.yml` workflow was not dispatched. Its read-only `mode=plan` must still be run on the self-hosted Platform runner immediately before deletion. The delete path remains blocked because the dedicated Media runner is active/enabled and external backup/retention plus authoritative DNS ownership are not independently confirmed. No namespace, PVC/PV, runner, DNS record, external database, object-storage resource, GHCR package or application repository was deleted.

The production Kustomize root and validator already exclude/reject Stock/Media manifests; this is GitOps ownership retirement, not live-cluster decommission completion. Do not infer completion from the absence of PVCs. Preserve `tce-prod`, `microfe-platform`, TCE/Auth/MicroFE/Keycloak, the shared Platform runner and the TCE market-scan schedule.
# StockDividend and Media Generation decommission plan

Status: Stock/Media GitOps ownership retirement and the guarded manual decommission workflow are merged (Platform PRs #1301, #1303, #1304, #1305 and #1310; Stock PR #32; Media PR #72). The K3s namespaces/workloads and dedicated Media runner cleanup have **not** been executed.

## Objective

Remove StockDividend and Media Generation from Platform Infra's production GitOps ownership and remove their Kubernetes workloads from the K3s cluster. Keep TCE Dashboard, Authentication, MicroFE, Keycloak, cert-manager, observability, and the platform inspection/reconciliation controllers intact.

Target namespaces:
- `stock-prod`
- `media-prod`

Target public routes:
- StockDividend: `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space`, `api.mrcute.space`
- Media Generation: `media.mrcute.space`

## Historical evidence before GitOps retirement

The latest committed VPS snapshot currently available in the repository was generated at **2026-11-05T21:26:12Z**. It is historical evidence, not a live preflight.

It showed:
- `media-prod`: backend and frontend each 1/1 Running; an app-specific GitHub Actions runner service was also active on the VPS.
- `stock-prod`: Admin Pods in ImagePullBackOff; Backend 1/1 Running; legacy `stock-frontend` 1/1 Running.
- Stock and Media Services and Ingress objects existed in their respective namespaces.

Because the snapshot is stale, do not use it as authorization to delete current resources. Obtain a new read-only K3s inspection immediately before the decommission operation.

## Current runtime evidence — 2026-11-06 10:18 ICT / 03:18 UTC

- GitOps ownership is retired on Platform master. Stock PR #32 and Media PR #72 removed app-to-Platform production handoffs. Routine Platform reconcile no longer manages or health-gates these namespaces.
- Platform inspection-only PR #1308 committed a fresh read-only snapshot generated at 2026-11-06T03:09:17Z. It confirms both `stock-prod` and `media-prod` namespaces remain Active, with their Services and Ingresses still present.
- Media backend and frontend are each 1/1 Running. Stock Admin has two 0/1 ImagePullBackOff Pods; the newer Backend is 0/1 ImagePullBackOff; the older Backend and legacy Frontend remain 1/1. The newer Stock images fail with `no match for platform in manifest`; this is not evidence of a GHCR pull-secret failure.
- Fresh storage inventory shows only the `k3s-debug/k3s-debug-logs` PVC/PV claim; neither target namespace has a PVC or PV claim. The protected manual workflow must repeat its same-window preflight immediately before deletion.
- The dedicated Media Actions runner remains active and enabled: `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`. Platform runner policy v15 is installed, but that does not retire the Media runner.
- Platform PR #1310 adds a hard pre-delete host guard requiring the dedicated Media systemd service to be inactive and no Media `Runner.Listener` process to remain. Follow-up PR #1313 strengthens this by also requiring the unit to be disabled/masked or absent, preventing it from auto-starting after a reboot. Because the latest snapshot shows the service active and enabled, the manual workflow must fail closed before storage preflight/deletion. GitHub unregistration remains a typed operator attestation.
- Namespace deletion and runner unregister have not been executed. Backup/external-data ownership is not independently confirmed. Do not delete PVs, external data, DNS, GHCR packages, app repositories or the shared Platform runner.

## Execution sequence

### Phase 1 — preflight and preservation

1. Run the platform's read-only VPS/K3s inspection and record its run ID, timestamp, node health, all namespaced API object names, Deployments, StatefulSets, Jobs/CronJobs, Services, Ingresses, PVCs, PVs, StorageClasses, and Secret names. Never print Secret or ConfigMap values.
2. Confirm the exact objects currently present in `stock-prod` and `media-prod`; include legacy StockDividend resources such as `stock-frontend`, which are not in the current GitOps Kustomize set but are still live.
3. Inspect PVC/PV reclaim policies and external storage before namespace deletion. Back up any persistent application data or credentials that must be retained. Do not delete PVs or external databases/storage as an implicit side effect.
4. Confirm with the service owner that the four StockDividend hostnames and `media.mrcute.space` can be retired. DNS records and external provider resources are not owned by Kubernetes namespace deletion.
5. Record the active `media-generation` self-hosted Actions runner service and confirm no workflow is running on it. Then stop and disable the exact unit (`systemctl disable --now actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`), unregister it from the Media repository, and verify the unit is disabled/masked or absent and no `Runner.Listener` process remains. The last snapshot named user `media-runner` and directory `/opt/media-actions-runner`; re-verify before acting. Do not remove the shared `platform-infra` runner.

### Phase 2 — remove GitOps ownership

Merged Platform PR #1301 removed both application manifest trees from the production Kustomize root and deletes their manifest directories. It removes their reconcile/health/recovery/GHCR scopes, dispatch receivers, dedicated-runner bootstrap helper, and app-specific publisher/provenance helpers. It also removes the retired Media origin and JWT audience from the shared Auth service configuration while retaining the TCE audience. StockDividend and Media Generation application repositories remain intact as source/image-publisher repositories; their workflows no longer send Platform production dispatches. The shared `reconcile-vps.yml` remains the only routine production apply authority. The PR adds a manual-only namespace decommission workflow and an all-namespaced-resource inventory; it does not execute that workflow.

### Phase 3 — controlled K3s decommission

1. With GitOps retirement merged and runner policy v15 verified by reconcile #42150629183, verify the dedicated Media runner is idle in the Media repository Actions runner settings. Stop and disable its exact systemd unit (`systemctl disable --now actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`), unregister it with a short-lived removal token from the Media repository, uninstall only that runner service, and verify the runner is absent from GitHub. Remove its sudoers entry and local runner directory only after any required logs/artifacts are retained. Never stop or unregister the shared Platform Infra runner.
2. Invoke `.github/workflows/decommission-stock-media.yml` manually from `master` in the protected `production` Environment.
3. Type all three exact confirmations: `DELETE-STOCK-PROD-AND-MEDIA-PROD`, `BACKUP-AND-EXTERNAL-DATA-REVIEWED`, and `MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED`. The backup and runner values are operator attestations; the workflow does not infer those external facts.
4. The workflow runs `scripts/decommission-stock-media-namespaces.sh plan` and then `delete`. Both passes enumerate all namespaced API object names (without printing Secret/ConfigMap values), cluster-scoped VolumeSnapshotContent references, common workload status, PVCs, PV claim references and StorageClasses. The plan also prints each target namespace's Ingress rule hosts, TLS hostnames, TLS Secret names and published ingress addresses (names/metadata only) so the operator can reconcile them with authoritative DNS/provider records. This inventory does not prove DNS ownership or external data retention. The root-owned `platform-kubectl decommission-stock-media` command repeats the PVC/PV/VolumeSnapshot checks, accepts only the two fixed namespaces, deletes only those namespaces, and verifies `tce-prod` and `microfe-platform` remain.
5. The operation aborts if either target namespace is missing, any PVC exists, any PV claim or VolumeSnapshot/VolumeSnapshotContent reference still points to either namespace, any typed confirmation is wrong, or the installed runner policy is not v15. Review the fresh inventory and resolve storage before retrying; never delete PVs as a workaround.
6. Capture a fresh post-decommission `inspect-vps.yml` run and verify the two namespaces are absent and TCE/Auth/MicroFE/Keycloak remain unchanged.

## Current execution state

- The manual decommission workflow is intentionally not triggered by this PR or by routine reconciliation.
- No live K3s namespace deletion, PVC/PV deletion, DNS change, GHCR package deletion, external database change, or runner unregister has been performed by this implementation.
- The latest committed read-only snapshot is inspection PR #1324 / run #42176445915 (2026-11-06T06:45:26Z). It confirms no target-namespace PVC/PV claims or VolumeSnapshot references, but the manual workflow must repeat its same-window preflight. It also confirms the dedicated Media runner remains active and enabled. The workflow must be run only after accepted backup/external-data/DNS review and independent runner stop/unregister evidence.

## Rollback and safety

- Before namespace deletion, rollback is to stop and retain the namespaces; no workloads are changed.
- Namespace deletion is destructive to namespaced Kubernetes objects. Restore requires the app repositories' source manifests, images, and separately backed-up runtime data/secrets. A Git revert alone does not restore PVC contents or external services.
- Do not delete PVs, external databases, object storage, DNS records, GHCR packages, app repositories, or application source code in this operation.
- Do not touch TCE market-scan schedules or TCE/Auth/MicroFE/Keycloak workloads.
- Keep this change in a dedicated branch and require exact-head validation before squash merge.

## Completion criteria

- Neither application appears in Platform Infra's production Kustomize render, deployment scope, rollout/health/recovery gates, or active production dispatch contract.
- Both namespaces are absent from K3s, with the approved post-decommission inspection attached to the tracker.
- The dedicated Media runner is unregistered/stopped; the shared Platform Infra runner remains healthy.
- TCE and all other platform-owned workloads pass their existing health checks.
- The tracker records the PR, exact merge SHA, decommission workflow/run IDs, pre/post inspection evidence, and any DNS/storage follow-up still owned outside Platform Infra.


## Latest runtime evidence — 2026-11-06 13:58 ICT / 06:45 UTC

This section supersedes the 10:18 ICT runtime snapshot above. Source: read-only `inspect-vps` run [#42176445915](https://github.com/phanthienquoc/platform-infra/actions/runs/42176445915), generated at `2026-11-06T06:45:26Z`, committed by inspection PR #1324 as `f29465020b25e1b2f5318733b5918e2d3e8a582b`.

- K3s node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`; disk usage is 56%, available RAM about 19 GiB, and the host reports `restart_required=yes`. No reboot or package upgrade is authorized by this decommission plan.
- Both target namespaces remain Active. `media-prod` backend/frontend are 1/1 Running with digest-pinned images. `stock-prod` remains Active: two Admin Pods and the newer Backend Pod are ImagePullBackOff because image tag `12d63b4` has no matching ARM64 manifest; the legacy Backend and Frontend are 1/1 Running.
- Storage inventory lists only `k3s-debug/k3s-debug-logs`. No Stock/Media PVC/PV claim or VolumeSnapshot/VolumeSnapshotContent reference is listed. This is in-cluster evidence only; it does not prove external database/object-storage backup, data ownership, DNS ownership or retention approval.
- The dedicated Media runner is still unsafe to retire automatically: `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service` is active and enabled, and `/opt/media-actions-runner/bin/Runner.Listener` remains. The shared Platform runner is also active and must remain untouched.
- TCE frontend/service and Auth/Keycloak remain desired at 0/0. Their state is outside this decommission; do not scale them or alter the TCE market-scan schedule.
- Production reconcile [#42176253693](https://github.com/phanthienquoc/platform-infra/actions/runs/42176253693) completed SUCCESS before the inspection, with Platform-owned MicroFE/Auth/TCE lanes passing and Keycloak skipped. It did not delete or manage Stock/Media namespaces.

The manual decommission workflow remains blocked by the active/enabled Media runner and the absence of independent backup/external-data/DNS ownership approval. Do not run it based on this snapshot alone.


## Workflow mode hardening — 2026-11-07

The manual `decommission-stock-media` workflow now separates inspection from deletion:

- `mode=plan` is the default. It runs the fresh read-only storage inventory and reports the dedicated Media runner service/enabled/Listener state. It does not require destructive attestations, request the production environment, or call the delete command.
- `mode=delete` remains a separate protected production operation. It requires all three exact operator confirmations, verifies the dedicated Media runner is stopped/disabled and has no Listener, repeats the storage preflight in the same run, and only then deletes the two fixed namespaces.
- The workflow remains `workflow_dispatch` only. No schedule, push, repository-dispatch or automatic decommission path is added.
- Plan mode does not infer GitHub runner registration or external backup/DNS ownership; those remain operator checks. It prints in-cluster Ingress host/TLS references for DNS reconciliation, but does not query or mutate authoritative DNS. It does not stop or unregister any runner.


## Latest runtime evidence — 2026-11-07 15:39 ICT / 08:39 UTC

This section supersedes the 13:01 ICT / 06:01 UTC snapshot above. Source: read-only inspection [#42356397506](https://github.com/phanthienquoc/platform-infra/actions/runs/42356397506), generated at `2026-11-07T08:39:29Z`, committed by inspection PR #1387 as master `067b3a2a85bf9b2590829e16c6dc57adf87a4cc8`. The inspection run completed successfully; no workload or production manifest was changed.

- Node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`, containerd runtime `2.3.2-k3s2`. Host Ubuntu 22.04.5; disk 56% used (~20 GiB free); available RAM ~19 GiB.
- Docker 29.1.3: 20 images, 11 active, 9.195 GB; 5.773 GB reclaimable. Build cache: 31 entries / 519.4 MB.
- `restart_required=yes`. containerd 2.2.1→2.4.2, Docker CE/CLI 29.1.3→29.9.3 and other OS package updates are available. Upgrade/reboot requires a separate maintenance window.
- The dedicated Media runner service remains active and enabled; `/opt/media-actions-runner/bin/Runner.Listener` is present. The shared Platform runner and Listener are also active and must remain untouched.
- `media-prod`: backend and frontend each 1/1 Running.
- `stock-prod`: two Admin Pods and the newer Backend Pod are ImagePullBackOff on tag `12d63b4` because GHCR has no matching `linux/arm64` manifest. Older Backend and Frontend remain Running.
- `microfe-platform`: Shell, WS and NATS 1/1 Running; Keycloak and microfe-auth 0/0. `tce-prod` frontend/service are 0/0 maintenance.
- Only PVC/PV claim listed is `k3s-debug/k3s-debug-logs`; no Stock/Media VolumeSnapshot or VolumeSnapshotContent references. This is in-cluster evidence only; external database/object-storage backups, retention and ownership remain unverified.
- Media Ingress still publishes `media.mrcute.space`; Stock Ingresses still publish the four Stock hostnames. Authoritative DNS/provider ownership must be confirmed before decommission.

The protected decommission workflow was not dispatched. The delete gate remains blocked by the active/enabled Media runner and missing external backup/retention and DNS-owner confirmation. No namespace, workload, PVC/PV, runner, DNS record, external database/storage, GHCR package or app repository was deleted.


## Remote GitHub runner registration verification — merged PR #1458 (2026-11-08)

The delete-mode guard is strengthened to verify the repository-level GitHub runner list, not merely accept a typed operator attestation:

- Before namespace deletion, the Platform workflow runs `scripts/verify-media-runner-retired.sh` after checking the local systemd unit and `Runner.Listener` process.
- The script requires `MEDIA_RUNNER_AUDIT_TOKEN` and queries only `GET /repos/phanthienquoc/media-generation/actions/runners`. It fails closed on a missing token, HTTP/API error, malformed response, or any registered runner named `media-generation-k3s-01`.
- Configure `MEDIA_RUNNER_AUDIT_TOKEN` as a Platform Infra Actions secret using a fine-grained GitHub token or GitHub App installation token with **Administration: read** on `phanthienquoc/media-generation` only. The token is read-only for this verification; it must not be granted runner deletion/write permission. The value is passed to curl through stdin configuration and is never printed.
- The owner/operator must still stop and disable the exact Media runner service and unregister it from the Media repository using GitHub's supported removal flow. This workflow verifies absence; it does not stop, unregister, or delete any runner.
- If the secret is not provisioned or the API cannot be read, the protected namespace delete path is blocked. Plan mode remains read-only and does not require this secret.

Merged implementation evidence: PR #1458 merged at `098cf54de9e2223bc97db57cca6fbee8334fc80c`. Exact-head `validate-github-actions` #42474849755 and `validate-manifests` #42474849751 passed; post-merge #42474925147 and #42474925187 passed. The PR changed only the protected verification gate and documentation/tests; no runner or namespace was changed.


## Latest read-only runtime evidence — 2026-11-08 18:17 ICT / 11:17 UTC

Source: inspection fallback [#42475079478](https://github.com/phanthienquoc/platform-infra/actions/runs/42475079478), generated at `2026-11-08T11:17:34Z`, committed by inspection PR [#1459](https://github.com/phanthienquoc/platform-infra/pull/1459) at `ef7a1a15b94acdaf7c46cbecb4aa2391cb90b0f8`. Exact-head manifest validation #42475211696 passed. PR #1459 changed only `debug/vps-latest.md`.

- Node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`; disk 56% used (~21 GiB free), available RAM ~19 GiB.
- `media-prod`: backend/frontend each 1/1 Running. `microfe-platform`: Shell/WS/NATS each 1/1 Running; Auth/Keycloak 0/0. `tce-prod`: frontend/service 0/0.
- `stock-prod`: two Admin Pods and the newer Backend Pod remain ImagePullBackOff on tag `12d63b4`; kubelet says no matching `linux/arm64` manifest. Older Backend and Frontend remain 1/1.
- In-cluster storage inventory shows no Stock/Media PVC/PV claim or VolumeSnapshot/VolumeSnapshotContent references. This does not prove external database/object-storage backup or retention.
- Dedicated Media runner service remains active and enabled, with `Runner.Listener` present. The shared Platform runner is active and must remain untouched. Media Ingress still publishes `media.mrcute.space`; Stock Ingresses still publish the four retired Stock hostnames.
- OIDC probes to `sso.mrcute.space` returned HTTP 503 while Keycloak/Auth remain 0/0. This is not live service health.
- PR #1458's remote registration check requires `MEDIA_RUNNER_AUDIT_TOKEN` with repository Administration:read on Media. Secret existence has not been independently verified; no delete-mode workflow was run. External backup/retention and authoritative DNS-owner approvals remain outstanding.

No namespace, PVC/PV, runner, DNS, external database/storage, GHCR package or app repository was deleted.


## Latest read-only runtime evidence — 2026-11-09 02:00 ICT / 19:00 UTC

Source: native inspection [#42510125328](https://github.com/phanthienquoc/platform-infra/actions/runs/42510125328), generated at `2026-11-08T18:27:55Z`, merged by inspection PR [#1477](https://github.com/phanthienquoc/platform-infra/pull/1477) at `e412faffc669a766176adccec7207c5cc02306f5`. Exact-head manifest validation [#42510263923](https://github.com/phanthienquoc/platform-infra/actions/runs/42510263923) passed before merge. The PR changed only the inspection snapshot.

- Both `stock-prod` and `media-prod` remain Active. Media backend/frontend are 1/1 Running. Stock Admin×2 and the newer Backend remain ImagePullBackOff on `12d63b4` due to the missing ARM64 manifest; the legacy Backend and Frontend remain Running.
- The inspection ran the protected workflow's read-only plan script. It confirmed `tce-prod` and `microfe-platform` are present, and reported `storage-clean`: no PVC, PV claim, VolumeSnapshot or VolumeSnapshotContent references for either target namespace. This is same-snapshot in-cluster evidence, not proof of external database/object-storage backups or retention.
- Stock Ingresses still publish `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space`, and `api.mrcute.space`. Media Ingress still publishes `media.mrcute.space`. The inspection explicitly states DNS ownership is not inferred.
- Dedicated Media runner service remains active/enabled and `/opt/media-actions-runner/bin/Runner.Listener` is present. The host snapshot cannot prove whether GitHub still lists the runner; the delete guard requires the read-only `MEDIA_RUNNER_AUDIT_TOKEN` check against the Media repository.
- The protected `decommission-stock-media.yml` delete mode was not dispatched. It remains blocked until the Media runner is idle, stopped, disabled and unregistered; `MEDIA_RUNNER_AUDIT_TOKEN` is available and verifies absence; external backup/retention and authoritative DNS/provider ownership are reviewed; exact typed confirmations are supplied; and the protected production Environment approves the operation.

No namespace, workload, PVC/PV, runner, DNS record, external database/storage, GHCR package or application repository was deleted. Preserve the shared Platform runner, TCE/Auth/MicroFE/Keycloak and TCE market-scan schedule.


## Delete-gate attestation propagation — 2026-11-09 14:00 ICT

A review of the destructive path found that the workflow validated the fourth operator attestation `MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED` and separately queried GitHub's Media runner API, but the final namespace-delete script and root-owned `platform-kubectl` wrapper consumed only the namespace, backup/external-data and DNS confirmations. A direct invocation of those lower layers could therefore omit the runner-retirement attestation.

The contract is now propagated and checked independently at every layer:

1. The protected workflow validates the exact runner-retirement input and performs the existing local systemd/Listener plus read-only remote GitHub runner absence checks.
2. The final delete step passes the same attestation to `decommission-stock-media-namespaces.sh`.
3. The script rejects a missing or mismatched runner-retirement attestation before running its destructive preflight.
4. The root-owned wrapper reads and validates all four newline-delimited confirmations before it can delete either namespace.
5. Shell regression tests cover missing and incorrect runner attestations as well as the existing PVC/PV/VolumeSnapshot guards.

This is defense in depth for the operator attestation. It does not replace the workflow's remote GitHub runner API check, and it does not unregister or stop a runner. Delete mode remains blocked until the operator independently stops/disables/unregisters the dedicated Media runner, the read-only API audit confirms it is absent, external backup/retention and authoritative DNS ownership are reviewed, and the protected production Environment authorizes the operation.

## Fresh read-only K3s evidence — 2026-11-09 13:16 ICT / 06:16 UTC

Source: inspection snapshot committed by [PR #1506](https://github.com/phanthienquoc/platform-infra/pull/1506), master commit `1a9c9b9b1c3cb550f9904f65a50ed87df0c157cb`. Snapshot generated at `2026-11-09T06:16:06Z`; it is fresh for this checkpoint but is not a deployment authorization.

- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; 4 CPUs, ~19 GiB available RAM, disk 56% (~21 GiB free), uptime 191 days 16 hours. Host still reports `restart_required=yes`; package upgrades are available, but no maintenance was performed.
- Media backend/frontend: 1/1 Running with RepoDigest evidence. MicroFE Shell/WS/NATS: 1/1 Running with RepoDigest evidence. TCE frontend/service, Auth and Keycloak remain intentional 0/0.
- Stock Admin remains 0/1 with two ImagePullBackOff pods on `12d63b4`; the newer Stock Backend pod also ImagePullBackOff due to no matching platform manifest. A legacy Backend and Frontend remain 1/1 on `23b2878`, but their local cached images have no RepoDigest and are not promotion evidence.
- In-cluster preflight still reports no Stock/Media PVC/PV claims or VolumeSnapshot references. The namespace inventory includes names of namespace-scoped credentials/TLS Secrets and many workload/ReplicaSet objects; values are suppressed. Namespace deletion would remove those namespaced objects, so external backup, credential rotation/retention and service-owner sign-off remain required.
- Stock Ingresses still publish `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space` and `api.mrcute.space`; Media still publishes `media.mrcute.space`. Authoritative DNS/provider ownership is not inferred by inspection.
- The dedicated Media runner remains active/enabled with `Runner.Listener` present; the shared Platform runner is also active and must be preserved. Remote Media runner registration still requires the read-only audit token.
- Public OIDC probes for both master and mrcute realms returned HTTP 503 while Keycloak remains 0/0. This is not live SSO health.
- GHCR digest coverage remains warning because the cached Stock legacy Backend/User images lack RepoDigest; local image IDs are not registry proof.

No Stock/Media namespace, workload, PVC/PV, runner, DNS record, external database/storage, GHCR package or app repository was deleted. No image was published/promoted, no manifest was applied, no workload was scaled, and no host package/reboot maintenance was performed.
