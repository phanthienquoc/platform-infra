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
4. The workflow runs `scripts/decommission-stock-media-namespaces.sh plan` and then `delete`. Both passes enumerate all namespaced API object names (without printing Secret/ConfigMap values), cluster-scoped VolumeSnapshotContent references, common workload status, PVCs, PV claim references and StorageClasses. The root-owned `platform-kubectl decommission-stock-media` command repeats the PVC/PV checks, accepts only the two fixed namespaces, deletes only those namespaces, and verifies `tce-prod` and `microfe-platform` remain.
5. The operation aborts if either target namespace is missing, any PVC exists, any PV claim or VolumeSnapshot/VolumeSnapshotContent reference still points to either namespace, any typed confirmation is wrong, or the installed runner policy is not v15. Review the fresh inventory and resolve storage before retrying; never delete PVs as a workaround.
6. Capture a fresh post-decommission `inspect-vps.yml` run and verify the two namespaces are absent and TCE/Auth/MicroFE/Keycloak remain unchanged.

## Current execution state

- The manual decommission workflow is intentionally not triggered by this PR or by routine reconciliation.
- No live K3s namespace deletion, PVC/PV deletion, DNS change, GHCR package deletion, external database change, or runner unregister has been performed by this implementation.
- The latest committed read-only snapshot is Platform PR #1308 (2026-11-06T03:09:17Z). It confirms no target-namespace PVC/PV claims, but the manual workflow must repeat its same-window preflight. It also confirms the dedicated Media runner remains active. The workflow must be run only after accepted backup/external-data review and independent runner stop/unregister evidence.

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
