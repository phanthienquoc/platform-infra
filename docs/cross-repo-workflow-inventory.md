# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 06:58 ICT / 2026-11-07 23:58 UTC**

Rolling inventory only; timestamped run/PR evidence remains under `docs/cross-repo-deployment-checkpoints/`.

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound events; owns manifest/workflow validators, native inspection, reconciliation, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `fe5c0de`; PR #1427 merged. Native inspection #42427239949 PASS but 13,475s inter-arrival. Native reconcile #42423799465 PASS but 12,392s gap and now stale; watchdog #42423187797 FAIL; recovery #42423100821 PASS. |
| TCE Dashboard | CI/tests; manual WF-03 ARM64 publisher with full-SHA/version tags, web/service digest verification and `tce-release-requested`; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. Market-scan schedule remains separately owned and unchanged. | No production SSH/Compose/K3s apply. Platform receives validated digest-bound release events and owns GitOps promotion/apply and production health. | Master `7ab52078`; no open PR. Native WF-06 #42417660167 FAIL; native WF-12 #42427247349 FAIL/stale; manual WF-06 #42427267317 fails four HTTP 503 probes. |
| StockDividend | CI/tests; ARM64 `deploy.yml` publishes full-SHA tags and verifies registry digests; weekend scraper cron has fail-closed `VNSTOCK_API_KEY` preflight. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `783ae36f`; CI #42375688209 7/7 PASS; scraper #42349150261 failed before dependencies/ingestion because `VNSTOCK_API_KEY` is missing. |
| Media Generation | CI/tests; WF-03 builds ARM64, publishes version + full-SHA immutable tags and verifies digests; no Platform dispatch while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS; backend/frontend and dedicated runner remain active in K3s; no recent publisher/digest handoff. |
| Authentication | CI/tests; manual `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags against one digest and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS; PR #75 validate PASS/Supabase Preview skipped, #76 validate PASS/Supabase Preview skipped; both migration/integration gated. |

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest native evidence |
|---|---|---:|---|
| `reconcile-vps.yml` | `7,22,37,52 * * * *` | 45m | #42423799465 PASS; 12,392s gap, latest age 50m41s at review. |
| `inspect-vps.yml` | `2,32 * * * *` | 75m | #42427239949 PASS; 13,475s gap, latest age 5m17s. |
| `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | 45m | #42423187797 FAIL; workflow_run #42427358673 also failed freshness. |
| `recover-stale-ops.yml` | `10,25,40,55 * * * *` | 45m | #42423100821 PASS but age 59m26s; workflow_dispatch #42427458035 is fallback only. |

Native evidence requires original `event=schedule`, master branch, attempt 1, exact workflow path and full source SHA. Manual, push, workflow_run and repository_dispatch are separate evidence classes. Do not lower budgets or count fallbacks as native delivery.

The TCE-triggered Platform recovery #42427253726 validated the external heartbeat and dispatched reconcile-vps #42427264491 with `mode=apply`, `target_app=all`, `allow_image_changes=false`. It ran only through the existing production authority; no GitOps drift was found, so manifest apply and rollout were skipped. Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` was unchanged.

## Cross-repo schedules and release boundaries

- TCE WF-06 remains `*/15 * * * *`; WF-12 remains `7,22,37,52 * * * *`; strict public HTTP 200 expectations remain unchanged. WF-13 is recovery/transport only. TCE market-scan schedule unchanged.
- Stock weekend scraper remains `0 1 * * 0,6` UTC. Missing `VNSTOCK_API_KEY` must be fixed by Stock owner; `preflight_only=true` must pass before ingestion.
- Media/Auth publisher jobs are purposeful manual/release workflows; do not convert them into scheduled production deployment authorities.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, digest/provenance gates, GitOps promotion/reconciliation, rollout and health.

## Latest production evidence

- Native read-only K3s inspection #42427239949 generated `debug/vps-latest.md` at 23:53:12Z and was merged through PR #1427. Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; runtime containerd 2.3.2-k3s2; disk 56% (~20 GiB free), RAM ~19 GiB available.
- Media backend/frontend and MicroFE Shell/WS/NATS Running. TCE/Auth/Keycloak remain intentional 0/0.
- Stock Admin 0/1 with two pods ImagePullBackOff on `12d63b4`; Stock Backend has one old `23b2878` pod Running and a desired `12d63b4` pod ImagePullBackOff; Frontend 1/1 Running. Kubelet reports no ARM64 manifest for `12d63b4`.
- Platform and dedicated Media runner services active/enabled. Stock/Media namespaces remain Active. Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB); no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership unverified.
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable. Host containerd.io 2.2.1 with 2.4.2-3 available; `restart_required=yes`. No cleanup, upgrade or reboot.
- Platform reconciliation passed GHCR read access for Auth/MicroFE/TCE packages, Auth runtime Secret verification/provisioning (values suppressed), and unchanged shared `ghcr-pull`. No GitOps drift; manifest apply/rollout skipped. TCE/Auth lanes confirmed maintenance/zero replicas, not live service health.
- Manual TCE WF-06 #42427267317 failed all four public HTTP 200 probes with HTTP 503. No new immutable publisher run/digest handoff or production image promotion.

## Protected decommission and security

Stock/Media remain retired from active Platform GitOps but legacy namespaces/workloads are still present. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider ownership attestation, dedicated Media runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

A prior short-lived runner registration token appeared in an Actions environment dump. PR #1416 masks it before output and later bootstrap verification showed masked output. Platform owner must still inspect runner registrations and GitHub audit log; registry cleanliness is not certified.

## Authority boundary

- `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only.
- Runner policy `rollout-status-v15-core-workloads` allows image-pull restarts only for core `microfe-platform` and `tce-prod` deployments. Regression test rejects Stock/Media restart or rollout authority.
- No duplicate direct SSH/Compose deployment authority.
- Stock/Media deletion, runner retirement, DNS/database/storage changes and host maintenance remain gated on explicit evidence and owner approval.
- TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0658-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0658-ict.md)
