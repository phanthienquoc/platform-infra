# StockDividend and Media Generation decommission plan

Status: GitOps ownership retirement and the guarded manual decommission workflow are merged. The approved K3s decommission scope remains in force; namespace/workload deletion and Media runner retirement have not been executed. The last full snapshot is now expired; deletion remains blocked pending fresh same-run evidence, external backup/retention and DNS proof, and verified runner retirement.

## Current gate status — 2026-11-12 04:02 ICT / 2026-11-11 21:02:52 UTC

The last full inspection #43089176130 was generated at 19:39:15Z. Its age at this reference is 5,017s, beyond the 4,500s freshness budget by 517s. It is now historical evidence only; this checkpoint does not assert that the previously observed workload or runner state is still current.

The last-known snapshot showed:
- `media-prod` backend/frontend 1/1 with registry RepoDigests; the dedicated Media runner service active/enabled and `Runner.Listener` present.
- `stock-prod` with two desired Admin pods and one desired Backend pod in ImagePullBackOff for tag `12d63b4`, error `no match for platform in manifest`; legacy Backend/Frontend 1/1.
- No PVC/PV claims or VolumeSnapshot references in the two target namespaces. Preserve the separate `k3s-debug/k3s-debug-logs` PVC (1Gi, Bound, RWO).
- Target namespaces still contained Deployments, ReplicaSets, Services, Ingresses and namespaced Secrets; namespace deletion would remove these resources.
- External backup/retention, authoritative DNS ownership and GitHub-side runner unregister remained unverified.

No newer full inspection or protected `decommission-stock-media.yml` plan run is evidenced in this pass. The connector does not expose workflow dispatch. Do not infer that the Media runner has since been retired or that DNS/backup gates are satisfied. No stop/unregister/delete operation was executed. The protected delete workflow must repeat the storage preflight in the same run and verify local service/Listener plus remote GitHub registration before deleting only `stock-prod` and `media-prod`.


## Previous inspection snapshot — 2026-11-12 03:12 ICT

### Latest full read-only inspection — 2026-11-12 03:12 ICT / 2026-11-11 20:11:03 UTC

Source: [inspect-vps #43089176130](https://github.com/phanthienquoc/platform-infra/actions/runs/43089176130), snapshot `debug/vps-latest.md`, exact-head validated by #43089441872 and merged through inspection PR [#1649](https://github.com/phanthienquoc/platform-infra/pull/1649) at `3e6d3f48`. Subsequent PRs #1650–#1652 changed documentation only; the active production manifest tree is unchanged. Snapshot generated at `2026-11-11T19:39:15Z`; at the 20:11:03Z reference its age is 1,908s within the 4,500s budget, with 2,592s remaining.

### Host and capacity

- Node `tce-k3s-01`: Ready/ARM64; Ubuntu 22.04.5; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`; kernel `6.8.0-1049-oracle`.
- Disk 56% (~20GiB free); RAM ~19GiB available. Host restart required with kernel/containerd/Docker/OS updates pending. No reboot or package upgrade.
- Docker image store 9.195GB with 5.773GB reclaimable; no cleanup.

### Workload, storage and runner state

- `media-prod`: backend/frontend 1/1 Running, pinned to RepoDigests `sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d` and `sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a`.
- `stock-prod`: two desired Admin pods and one desired Backend pod ImagePullBackOff for tag `12d63b4`; exact error `no match for platform in manifest: not found`. Legacy Backend/Frontend remain 1/1 but their cached image IDs are not registry RepoDigest evidence.
- Only PVC/PV claim is `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO). No PVC/PV claim or VolumeSnapshot reference exists in either target namespace. This is in-cluster storage evidence only; it does not prove external database/object-storage backup or retention.
- Target namespaces still contain namespaced Deployments, ReplicaSets, Services, Ingresses and Secrets. Namespace deletion removes those objects; inspect names only and never print Secret/ConfigMap values.
- Dedicated Media runner service is active/enabled and `Runner.Listener` is present. Host inspection cannot establish GitHub-side registration. Do not stop the shared Platform runner.
- Ingress snapshot lists `media.mrcute.space` and Stock hosts `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space` plus one additional host. The existing plan lists `api.mrcute.space`; re-confirm the exact host/TLS list in the same-run plan and authoritative DNS/provider records.

### Health outside the decommission scope

- Keycloak remains 0/0 and both public OIDC discovery probes returned HTTP 503.
- TCE/Auth/MicroFE/Keycloak are outside this operation. Preserve them and the TCE market-scan schedule.

### Protected execution gates

- `.github/workflows/decommission-stock-media.yml` is `workflow_dispatch` only; `mode=plan` is the default and read-only.
- Delete mode requires the protected `production` Environment, exact confirmations `DELETE-STOCK-PROD-AND-MEDIA-PROD`, `BACKUP-AND-EXTERNAL-DATA-REVIEWED`, `AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED`, `MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED`, and stable HTTPS backup/DNS evidence references.
- Before deleting it verifies the Media systemd service is inactive and disabled/masked or absent, no Listener process remains, and the GitHub Media repository runner list has no `media-generation-k3s-01` entry using read-only `MEDIA_RUNNER_AUDIT_TOKEN`; it repeats storage preflight in the same run and deletes only `stock-prod` and `media-prod`.
- Current snapshot shows the local Media runner gate is not satisfied. Remote registration, audit-token availability, external backup/retention, authoritative DNS ownership and production Environment approval remain unverified. No plan/delete workflow run was invoked in this automation because the current GitHub connector has no workflow-dispatch action.

---

## Historical full read-only inspection — 2026-11-10 05:14 ICT / 2026-11-09 22:12:13 UTC

Source: [inspect-vps #42709680634](https://github.com/phanthienquoc/platform-infra/actions/runs/42709680634), snapshot `debug/vps-latest.md`, exact-head validated by #42709965064 and squash-merged through inspection PR [#1550](https://github.com/phanthienquoc/platform-infra/pull/1550) at master `051f7b8325c6a79e4b3a91a97f57b61169721f0c`. This was the latest full snapshot at its original checkpoint and is superseded by the 2026-11-12 inspection above.

### Host and capacity

- `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`; kernel `6.8.0-1049-oracle`.
- RAM 23 GiB total, 19 GiB available. Root disk 45 GiB total, 25 GiB used, 20 GiB free (56%, normal pressure).
- Uptime 192 days, 8 hours. `restart_required=yes`; pending updates include containerd/Docker. No reboot or package upgrade.
- Docker image store 9.195 GB, 5.773 GB reclaimable; build cache 519.4 MB, 154.4 MB reclaimable. No cleanup.

### Workload and image state

- Media backend/frontend 1/1 Running, digest-pinned.
- MicroFE Shell/WS/NATS 1/1 Running.
- Auth and Keycloak 0/0; TCE frontend/service 0/0.
- Stock Admin desired 0/1 with two pods ImagePullBackOff; desired Backend has one legacy Running pod and one new ImagePullBackOff pod; Frontend 1/1 Running.
- Stock desired tag `12d63b4` fails with `no match for platform in manifest` on ARM64. Do not interpret this as shared GHCR credential failure.

### Storage and runners

- Only PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB, Bound); no Stock/Media VolumeSnapshot references. Preflight reports `storage-clean`.
- Stock/Media namespaces remain Active with Services/Ingresses. Storage-clean does not establish external backup/retention or DNS ownership.
- Platform runner service active/enabled. Dedicated Media runner service active/enabled and `Runner.Listener` present. Host inspection cannot establish GitHub-side registration; remote unregister remains unverified.

### Health and drift

- GitOps drift status clean.
- Public OIDC probes for `sso.mrcute.space` master and mrcute discovery both returned HTTP 503; Keycloak remains 0/0 and condition wait timed out.
- TCE frontend/service remain 0/0; no live TCE health assertion. Latest known strict WF-06 probes returned 503.
- No protected namespace/runner deletion, workload scaling, storage cleanup, DNS/database change or host maintenance.

## Latest live workload readout — 2026-11-10 05:10 ICT / 2026-11-09 22:10:30 UTC

Source: successful recovery-triggered [reconcile-vps run #42709362025](https://github.com/phanthienquoc/platform-infra/actions/runs/42709362025). This is a fresh node/pod readout during controlled reconciliation, not a replacement for the full disk/RAM/runner/storage inspection.

- Node `tce-k3s-01` was Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`.
- `media-prod`: backend/frontend each 1/1 Running.
- `microfe-platform`: Shell/WS/NATS each 1/1 Running.
- `stock-prod`: two Admin pods and desired Backend pod remain ImagePullBackOff; legacy Backend/Frontend remain 1/1 Running.
- TCE frontend/service and Auth/Keycloak remain intentional 0/0. This reconciliation did not assert public HTTP 200 for those services.
- GHCR read-access preflight passed for all managed Auth/MicroFE/TCE images; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; no image-pull failures for managed MicroFE/Auth/TCE targets. TCE release pairing `prod-v0.1.0-e75e338` passed.
- GitOps drift=false, `ALLOW_IMAGE_CHANGES=false`, and production manifest apply skipped. Reconciliation and post-reconcile cluster verification passed.
- This readout contains no disk/RAM or `restart_required` measurement. The latest full hardware/storage/runner inspection remains #42694932077 at 20:38:49Z and is now older than the 75-minute freshness budget. Obtain a fresh full read-only inspection before any runtime mutation or decommission operation.
- Stock/Media namespaces remain present. Media runner service/listener, remote unregister, external backup/retention and authoritative DNS ownership remain unverified. The protected delete workflow remains blocked.

## Latest runtime evidence — 2026-11-10 04:03 ICT / 2026-11-09 21:03:15 UTC

This section supersedes the older runtime snapshots below. Source: read-only inspection [#42694932077](https://github.com/phanthienquoc/platform-infra/actions/runs/42694932077), generated at `2026-11-09T20:38:49Z`, committed by inspection PR [#1546](https://github.com/phanthienquoc/platform-infra/pull/1546) at master `827d8d442cf7de344be04a246e56ee2ee3148657`. Snapshot age at this checkpoint was 24m26s (within the 75-minute inspection budget). The PR changed only the inspection snapshot; no production manifest was changed.

- Node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`, Ubuntu 22.04.5. Disk is 56% used (~20 GiB free), available RAM ~19 GiB, uptime 192 days.
- `restart_required=yes`; Ubuntu, containerd and Docker updates are pending. No reboot or upgrade was performed.
- `media-prod`: backend and frontend are 1/1 Running with digest-pinned imageIDs. The dedicated Media runner systemd service is active/enabled and `/opt/media-actions-runner/bin/Runner.Listener` remains present.
- `stock-prod`: two Admin pods and the desired Backend pod are ImagePullBackOff on historical tag `12d63b4`, with GHCR reporting no matching linux/arm64 manifest. The older Backend and Frontend remain 1/1 Running. This is an image-platform failure, not evidence that the shared pull Secret is invalid.
- `microfe-platform`: Shell, WS and NATS are 1/1 Running. TCE frontend/service and Auth/Keycloak remain intentional 0/0; public HTTP 200 health was not established.
- The only PVC/PV claim listed is `k3s-debug/k3s-debug-logs`. No Stock/Media VolumeSnapshot or VolumeSnapshotContent references were found. Both target namespaces remain Active with namespaced resources, Services and Ingresses. Absence of in-cluster PVCs/snapshots does not prove external database/object-storage backup or retention.
- The protected decommission preflight confirms no retired Stock/Media references in the active production manifest tree, but the dedicated Media runner has not been retired, remote GitHub unregister is unverified, and external backup/retention plus authoritative DNS ownership are not independently confirmed. The delete workflow remains blocked. Do not infer delete authorization from storage-clean output.
- Docker image store is ~9.195 GB with ~5.773 GB reclaimable; no cleanup was performed. No host maintenance was performed.

The protected manual workflow remains `workflow_dispatch` only. Preserve `tce-prod`, `microfe-platform`, the shared Platform runner, strict HTTP 200 health assertions and the TCE market-scan schedule.


---



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

## Historical execution state — 2026-11-12 03:12 ICT / 20:11:03 UTC

- GitOps ownership retirement is merged and the controlled decommission scope is approved. K3s namespace/workload deletion and Media runner retirement have not been executed.
- Latest full read-only inspection: [#43089176130](https://github.com/phanthienquoc/platform-infra/actions/runs/43089176130), generated 2026-11-11T19:39:15Z and committed by inspection PR [#1649](https://github.com/phanthienquoc/platform-infra/pull/1649). At 20:11:03Z age=1,908s within the 4,500s budget (2,592s remaining). Node `tce-k3s-01` Ready/ARM64; Ubuntu 22.04.5; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56% (~20GiB free); RAM ~19GiB available. Host reports restart required with updates pending; no reboot.
- `media-prod`: backend/frontend 1/1 Running with registry RepoDigests `93ddb944…` and `095c72ed…`. The dedicated Media runner systemd service is active/enabled and `Runner.Listener` is present; GitHub-side registration cannot be inferred by host inspection.
- `stock-prod`: two Admin pods and one desired Backend pod are ImagePullBackOff for `12d63b4`, exact error `no match for platform in manifest: not found`. Legacy Backend/Frontend are 1/1, but cached/local IDs are not registry RepoDigest evidence.
- Read-only storage preflight reports no PVC/PV claims or VolumeSnapshot references in `stock-prod` or `media-prod`. The only PVC/PV claim is the separate `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO); preserve it. Target namespaces still contain Deployments, ReplicaSets, Services, Ingresses and namespaced Secrets, all of which namespace deletion removes.
- Current Ingress snapshot shows `media.mrcute.space` and Stock host entries `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space` plus one additional host. The existing plan lists `api.mrcute.space`; the same-run plan must print and confirm the exact current host/TLS list against authoritative DNS/provider records. Host inspection does not prove DNS ownership.
- Public Keycloak OIDC probes for both master and mrcute realms returned HTTP 503 while Keycloak is 0/0. TCE/Auth/Keycloak/MicroFE are outside this decommission and must remain untouched.
- The protected `decommission-stock-media.yml` workflow remains `workflow_dispatch` only, default `mode=plan`. Delete mode requires the production Environment, exact typed attestations, stable HTTPS backup/DNS evidence references, a fresh same-run storage preflight, local Media service inactive and disabled/masked or absent, no Listener process, and remote GitHub runner absence verified by read-only `MEDIA_RUNNER_AUDIT_TOKEN`. The current snapshot proves the local runner gate is not satisfied. Secret availability and GitHub runner registration remain unverified.
- The current integration has no workflow-dispatch action, so this run did not invoke the plan/delete workflow. The snapshot's storage-clean preflight is useful but does not replace the workflow's same-run plan immediately before deletion.
- No namespace/workload, PVC/PV, runner, DNS record, external database/storage, GHCR package or application repository was deleted. No runner was stopped/unregistered. External backup/retention and authoritative DNS ownership evidence remain outstanding.

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


## Latest read-only K3s inspection — 2026-11-09 14:10 ICT / 07:10 UTC

Source: `debug/vps-latest.md` generated at `2026-11-09T07:10:37Z`, committed by inspection PR [#1508](https://github.com/phanthienquoc/platform-infra/pull/1508) as master `1433711b25926d528f16df4f727a8e0929ea354c`.

- Node `tce-k3s-01` is Ready/ARM64 on K3s `v1.36.3+k3s1` and containerd `2.3.2-k3s2`; disk 56% (~21 GiB free), available RAM ~19 GiB, uptime 191d17h. Host reports `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry RepoDigest evidence.
- Stock Admin has two ImagePullBackOff pods on `12d63b4`; desired Backend pod also ImagePullBackOff because GHCR reports no matching platform manifest. Legacy Backend and Frontend remain 1/1 on `23b2878`, but those cached images lack RepoDigest.
- TCE frontend/service, Auth and Keycloak remain 0/0. Both public OIDC realm probes returned HTTP 503.
- No Stock/Media PVC/PV claims or VolumeSnapshot references were found. Both namespaces remain Active and contain namespaced Secrets (`ghcr-pull`, `ghcr-secret`, TLS and app Secrets), Services, Ingresses, Deployments and many ReplicaSets. Namespace deletion would remove these namespaced objects; external backup/retention and credential ownership/rotation review are still required.
- Stock Ingresses still expose `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space` and `api.mrcute.space`; Media exposes `media.mrcute.space`. DNS/provider ownership is not inferred.
- Dedicated Media runner service is active/enabled and Listener present; shared Platform runner remains active and must be preserved. Remote Media registration still requires the read-only API audit.
- GHCR digest coverage warning is limited to the legacy cached Stock Backend/User images. No local image ID is accepted as registry promotion evidence.

No namespace, workload, PVC/PV, runner, DNS record, external database/storage, GHCR package or application repository was deleted. No manifest apply, image promotion, workload scaling, cleanup or host maintenance occurred.
