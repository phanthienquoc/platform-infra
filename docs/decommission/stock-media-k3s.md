# StockDividend and Media Generation decommission plan

Status: approved scope; execution gated on a fresh production preflight.

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

1. Run the platform's read-only VPS/K3s inspection and record its run ID, timestamp, node health, namespace contents, Deployments, StatefulSets, Jobs/CronJobs, Services, Ingresses, PVCs, PVs, and relevant Secrets.
2. Confirm the exact objects currently present in `stock-prod` and `media-prod`; include legacy StockDividend resources such as `stock-frontend`, which are not in the current GitOps Kustomize set but are still live.
3. Inspect PVC/PV reclaim policies and external storage before namespace deletion. Back up any persistent application data or credentials that must be retained. Do not delete PVs or external databases/storage as an implicit side effect.
4. Confirm with the service owner that the four StockDividend hostnames and `media.mrcute.space` can be retired. DNS records and external provider resources are not owned by Kubernetes namespace deletion.
5. Record the active `media-generation` self-hosted Actions runner service and unregister/stop it separately after confirming no workflow is running on it. Do not remove the shared `platform-infra` runner.

### Phase 2 — remove GitOps ownership

1. Remove `apps/stockdividend` and `apps/media-generation` from `environments/prod/kustomization.yaml`.
2. Remove both application manifest trees from Platform Infra after the removal PR's validation contract is updated.
3. Remove StockDividend/Media deployment lanes, app-specific scope values, image-pair resolution and health checks from `reconcile-vps.yml`.
4. Remove namespace bootstrap entries and app-specific health/restart exceptions from `reconcile-vps.sh`, `bootstrap-runner.sh`, `verify-workload-health.sh`, and recovery readiness checks.
5. Remove obsolete app-specific image promotion/provenance helpers and credentials only after proving no remaining workflow or repository contract references them.
6. Update image-change validation, workflow-contract tests, workflow inventory, README, deployment tracker, and checkpoints. Preserve unrelated CI/security workflows and the single production apply authority (`reconcile-vps.yml`).

### Phase 3 — controlled K3s decommission

1. Use a dedicated, manually invoked, production-environment operation with a typed confirmation string; never trigger namespace deletion from push, schedule, or routine reconciliation.
2. Re-run the read-only preflight in the same maintenance window. Abort if the namespace contents differ from the reviewed inventory, a workload is active unexpectedly, PVC/PV state is unclear, or the node is unhealthy.
3. Delete only the two approved namespaces (`stock-prod` and `media-prod`). Do not delete cluster-wide CRDs, shared secrets, shared ingress controllers, shared storage classes, shared GHCR credentials, cert-manager, or any other namespace.
4. Wait until both namespaces are absent. Verify no StockDividend/Media Pods, Deployments, StatefulSets, Jobs, Services, or Ingresses remain.
5. Verify the platform-owned namespaces and TCE/Auth/MicroFE/Keycloak state are unchanged. Capture a fresh post-decommission inspection.
6. Unregister/stop only the dedicated Media Generation Actions runner after verifying it has no active job. Keep the shared Platform Infra runner online.

## Rollback and safety

- Before namespace deletion, rollback is to stop and retain the namespaces; no workloads are changed.
- Namespace deletion is destructive to namespaced Kubernetes objects. Restore requires the app repositories' source manifests, images, and separately backed-up runtime data/secrets. A Git revert alone does not restore PVC contents or external services.
- Do not delete PVs, external databases, object storage, DNS records, GHCR packages, app repositories, or application source code in this operation.
- Do not touch TCE market-scan schedules or TCE/Auth/MicroFE/Keycloak workloads.
- Keep this change in a dedicated branch and require exact-head validation before squash merge.

## Completion criteria

- Neither application appears in Platform Infra's production Kustomize render, deployment scope, rollout/health/recovery gates, or active workflow inventory.
- Both namespaces are absent from K3s, with the approved post-decommission inspection attached to the tracker.
- The dedicated Media runner is unregistered/stopped; the shared Platform Infra runner remains healthy.
- TCE and all other platform-owned workloads pass their existing health checks.
- The tracker records the PR, exact merge SHA, decommission workflow/run IDs, pre/post inspection evidence, and any DNS/storage follow-up still owned outside Platform Infra.
