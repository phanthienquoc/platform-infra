# StockDividend and Media Generation decommission

Status: GitOps retirement is being implemented in a dedicated PR. Namespace deletion is a separate, manually dispatched production operation and has **not** been executed.

## Objective and scope

Remove StockDividend and Media Generation from Platform Infra's production GitOps ownership, then remove only their Kubernetes namespaces from the K3s cluster:

- `stock-prod`
- `media-prod`

Public routes currently associated with the namespaces:
- StockDividend: `mrcute.space`, `www.mrcute.space`, `admin.mrcute.space`, `api.mrcute.space`
- Media Generation: `media.mrcute.space`

The decommission workflow does not change DNS, external databases, object storage, GHCR packages, application source repositories, or the dedicated Media Actions runner. Those are separate ownership/cleanup decisions.

## App publisher handoff retirement

- Media Generation PR [#72](https://github.com/phanthienquoc/media-generation/pull/72) merged by squash at `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`. Its app workflow remains responsible for CI, immutable GHCR publication and ARM64 digest verification; it no longer dispatches Platform.
- StockDividend PR [#32](https://github.com/phanthienquoc/stockdividend/pull/32) merged by squash at `6fcefa6b3792dab92b6d5c438001633d25f1ca28`. Its app workflow retains CI and immutable ARM64 publication with a manual release hold; it no longer dispatches Platform.
- Platform's receiver/manifests/rollout lanes are removed separately in the active decommission PR. The shared pull-secret reconciler temporarily retains the two existing namespaces until deletion, so already-running Pods are not deprived of pull credentials during the transition.

## Latest read-only K3s evidence

The latest committed read-only inspection completed successfully in Platform workflow [#42137791156](https://github.com/phanthienquoc/platform-infra/actions/runs/42137791156). Snapshot timestamp: **2026-11-06T00:34:27Z**.

Observed workloads:
- `media-prod`: backend and frontend each 1/1 Running.
- `stock-prod`: Admin Pods 0/1 ImagePullBackOff; Backend had one old 1/1 Pod and one ImagePullBackOff Pod; legacy `stock-frontend` remained 1/1.
- Dedicated Media Actions runner service was active on the VPS at snapshot time. The snapshot does not prove the runner is idle; leave it running until a separate GitHub runner/job check.

Persistent storage inventory:
- The only observed PVC was `k3s-debug/k3s-debug-logs` (1 GiB, Bound, `local-path`).
- Its PV claim reference was `k3s-debug/k3s-debug-logs`, reclaim policy `Delete`.
- No PVC in `stock-prod` or `media-prod`, and no PV claim reference to either target namespace.

This snapshot is evidence for planning, not a substitute for the live preflight in the manual decommission workflow. The runner repeats PVC/PV checks immediately before deleting anything and aborts if any claim exists or ownership cannot be verified.

## Controlled execution

### Phase 1 — remove Platform GitOps ownership

1. Remove both app trees from the production Kustomize root.
2. Remove the Stock/Media repository-dispatch receiver branches, app-specific digest promotion helpers, deployment lanes, image scope, health/recovery checks and certificate manifest.
3. Preserve TCE Dashboard, Authentication, MicroFE, Keycloak, cert-manager controllers, observability, and the shared production reconcile authority.
4. Keep shared GHCR pull-secret refresh for the residual namespaces until deletion; remove those temporary namespace entries only after successful deletion.
5. Validate the exact PR head and squash-merge only after required checks pass.

### Phase 2 — delete only the two namespaces

Use GitHub Actions workflow **Decommission StockDividend and Media K3s namespaces** from `master`, under the existing `production` Environment.

The workflow is `workflow_dispatch` only. It requires all of the following exact typed acknowledgements:
- `DECOMMISSION stock-prod media-prod`
- `I UNDERSTAND THE OPERATION ABORTS ON ANY PVC OR PV CLAIM`
- `EXTERNAL DATA STORES AND DNS WILL BE LEFT IN PLACE`
- `MEDIA RUNNER WILL REMAIN ACTIVE FOR SEPARATE CLEANUP`

The root-owned `platform-kubectl decommission-stock-media` action:
1. Verifies the Stock namespace ownership label and a Media-owned Deployment.
2. Prints a read-only inventory of Deployments, Pods, Services, Ingresses, Jobs and CronJobs.
3. Aborts if either namespace has any PVC or any PV claim reference.
4. Deletes only `stock-prod` and `media-prod`, waits for completion, and verifies both are absent.
5. Verifies `tce-prod` and `microfe-platform` still exist.
6. Never deletes PVCs/PVs, shared controllers, external data, DNS, GHCR packages, or the dedicated Media runner.

If any preflight is unclear, the action fails closed and does not delete either namespace. Do not work around a failed storage/ownership check by manually deleting resources.

### Phase 3 — separate runner and external cleanup

1. Confirm the dedicated Media Actions runner has no active job; then unregister/stop only that runner. Keep the shared Platform Infra runner online.
2. Coordinate DNS and certificate follow-up outside the namespace-deletion workflow. DNS records are not changed automatically.
3. Keep external databases and object storage unless separately backed up and explicitly authorized for retirement.
4. Capture a fresh post-decommission read-only inspection and update the tracker.

## Safety boundaries

- No namespace deletion has been executed by this PR.
- Do not delete PVs, external databases, object storage, DNS records, GHCR packages, app repositories, or source code.
- Do not reboot/upgrade the K3s node.
- Do not change TCE/Auth/MicroFE/Keycloak state or any TCE market-scan schedule.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
