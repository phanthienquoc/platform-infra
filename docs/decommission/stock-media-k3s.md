# StockDividend and Media Generation decommission plan

Status: GitOps removal and guarded decommission workflow are implemented on a dedicated PR branch; namespace deletion and dedicated-runner cleanup have **not** been executed.

## Objective

Remove StockDividend and Media Generation from Platform Infra's production GitOps ownership and remove their Kubernetes workloads from the K3s cluster. Keep TCE Dashboard, Authentication, MicroFE, Keycloak, cert-manager, observability, and the platform inspection/reconciliation controllers intact.

Target namespaces:
- `stock-prod`
- `media-prod`

Target public routes:
- StockDividend: `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space`, `api.mrcute.space`
- Media Generation: `media.mrcute.space`

## Evidence available before this change

The latest committed VPS snapshot currently available in the repository was generated at **2026-11-05T21:26:12Z**. It is historical evidence, not a live preflight.

It showed:
- `media-prod`: backend and frontend each 1/1 Running; an app-specific GitHub Actions runner service was also active on the VPS.
- `stock-prod`: Admin Pods in ImagePullBackOff; Backend 1/1 Running; legacy `stock-frontend` 1/1 Running.
- Stock and Media Services and Ingress objects existed in their respective namespaces.

Because the snapshot is stale, do not use it as authorization to delete current resources. Obtain a new read-only K3s inspection immediately before the decommission operation.

## Execution sequence

### Phase 1 — preflight and preservation

1. Run the platform's read-only VPS/K3s inspection and record its run ID, timestamp, node health, all namespaced API object names, Deployments, StatefulSets, Jobs/CronJobs, Services, Ingresses, PVCs, PVs, StorageClasses, and Secret names. Never print Secret or ConfigMap values.
2. Confirm the exact objects currently present in `stock-prod` and `media-prod`; include legacy StockDividend resources such as `stock-frontend`, which are not in the current GitOps Kustomize set but are still live.
3. Inspect PVC/PV reclaim policies and external storage before namespace deletion. Back up any persistent application data or credentials that must be retained. Do not delete PVs or external databases/storage as an implicit side effect.
4. Confirm with the service owner that the four StockDividend hostnames and `media.mrcute.space` can be retired. DNS records and external provider resources are not owned by Kubernetes namespace deletion.
5. Record the active `media-generation` self-hosted Actions runner service and unregister/stop it separately after confirming no workflow is running on it. The last snapshot named systemd unit `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`, user `media-runner`, and directory `/opt/media-actions-runner`; re-verify all three before acting. Do not remove the shared `platform-infra` runner.

### Phase 2 — remove GitOps ownership

The implementation branch removes both application manifest trees from the production Kustomize root and deletes their manifest directories. It removes their reconcile/health/recovery/GHCR scopes, dispatch receivers, dedicated-runner bootstrap helper, and app-specific publisher/provenance helpers. It also removes the retired Media origin and JWT audience from the shared Auth service configuration while retaining the TCE audience. StockDividend and Media Generation application repositories remain intact as source/image-publisher repositories; their workflows no longer send Platform production dispatches. The shared `reconcile-vps.yml` remains the only routine production apply authority. The PR adds a manual-only namespace decommission workflow and an all-namespaced-resource inventory; it does not execute that workflow.

### Phase 3 — controlled K3s decommission

1. After the GitOps-removal PR is merged and runner bootstrap policy v15 is installed, verify the dedicated Media runner is idle in the Media repository Actions runner settings. Stop its exact systemd service, unregister it with a short-lived removal token from the Media repository, uninstall only that runner service, and verify the runner is absent from GitHub. Remove its sudoers entry and local runner directory only after any required logs/artifacts are retained. Never stop or unregister the shared Platform Infra runner.
2. Invoke `.github/workflows/decommission-stock-media.yml` manually from `master` in the protected `production` Environment.
3. Type all three exact confirmations: `DELETE-STOCK-PROD-AND-MEDIA-PROD`, `BACKUP-AND-EXTERNAL-DATA-REVIEWED`, and `MEDIA-RUNNER-STOPPED-AND-UNREGISTERED`. The backup and runner values are operator attestations; the workflow does not infer those external facts.
4. The workflow runs `scripts/decommission-stock-media-namespaces.sh plan` and then `delete`. Both passes enumerate all namespaced API object names (without printing Secret/ConfigMap values), common workload status, PVCs, PV claim references and StorageClasses. The root-owned `platform-kubectl decommission-stock-media` command repeats the PVC/PV checks, accepts only the two fixed namespaces, deletes only those namespaces, and verifies `tce-prod` and `microfe-platform` remain.
5. The operation aborts if either target namespace is missing, any PVC exists, any PV claim still references either namespace, any typed confirmation is wrong, or the installed runner policy is not v15. Review the fresh inventory and resolve storage before retrying; never delete PVs as a workaround.
6. Capture a fresh post-decommission `inspect-vps.yml` run and verify the two namespaces are absent and TCE/Auth/MicroFE/Keycloak remain unchanged.

## Current execution state

- The manual decommission workflow is intentionally not triggered by this PR or by routine reconciliation.
- No live K3s namespace deletion, PVC/PV deletion, DNS change, GHCR package deletion, external database change, or runner unregister has been performed by this implementation.
- The latest committed VPS snapshot is stale and does not provide the required same-window storage preflight. The dedicated Media runner was last observed active in that snapshot; its current state is unverified. The manual workflow must be run only after the runner is independently stopped/unregistered and the current inventory/data-retention review is accepted.

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
