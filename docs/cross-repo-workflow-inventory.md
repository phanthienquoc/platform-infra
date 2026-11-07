# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 06:05 ICT / 2026-11-07 23:05 UTC**

This is the rolling workflow/ownership inventory. Timestamped run and PR evidence remains under `docs/cross-repo-deployment-checkpoints/`.

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives TCE/Auth digest-bound release events; owns CI/manifest validators, scheduled inspection, watchdog and recovery. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `49840207`; PR #1423 merged; post-merge validation #42423484264 PASS. Native watchdog #42423187797 FAIL; native recovery #42423100821 PASS; fallback reconcile #42423113109 PASS with no drift/apply skipped. |
| TCE Dashboard | CI/tests; manual-only WF-03 ARM64 production publisher with full-SHA release tag, web/service digest verification and `tce-release-requested` payload; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery. | No production SSH/Compose/K3s apply. Platform receives digest-bound event, owns GitOps promotion/apply and production health. | Master `7ab52078`; native WF-06 #42417660167 failed four HTTP 503 probes; native WF-12 #42411262379 stale/failing; WF-07 backup/integration passed. |
| StockDividend | CI/tests; ARM64 `deploy.yml` publishes full-SHA tags and verifies registry digests; weekend scraper has fail-closed `VNSTOCK_API_KEY` preflight. | Stock is retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No active production handoff. | Master `783ae36f`; CI #42375688209 7/7 PASS; scraper #42349150261 failed before dependencies/ingestion because `VNSTOCK_API_KEY` is missing. |
| Media Generation | CI/tests; WF-03 builds ARM64, publishes version + full-SHA immutable tags and verifies digests. Its release summary explicitly sends no Platform dispatch. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. | Master `54f3a76a`; CI #42239703151 PASS; no recent publisher/digest handoff; backend/frontend and dedicated runner remain active. |
| Authentication | CI/tests; manual-only `release.yml` builds ARM64 with provenance/SBOM, verifies SHA/version tags against the same digest and sends `auth-image-published`. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `3b60ff46`; CI #42215394539 PASS; PR #75/#76 remain Supabase migration/integration-gated; no recent release handoff. |

## Evidence and acceptance rules

- Native schedule evidence requires original `event=schedule`, master branch, attempt 1, exact workflow path and full source SHA. Manual, push, workflow_run and repository_dispatch events are separate evidence classes.
- Platform cron remains: reconcile `7,22,37,52 * * * *`; inspection `2,32 * * * *`; watchdog `12,27,42,57 * * * *`; recovery `10,25,40,55 * * * *`. Freshness budgets remain 45/75/45/45 minutes. Latest native inter-arrival gaps exceed those budgets; watchdog remains fail-closed.
- TCE WF-06 remains `*/15 * * * *`, WF-12 remains `7,22,37,52 * * * *), and strict public HTTP 200 expectations remain unchanged. TCE market-scan schedule is untouched.
- Stock weekend scraper remains `0 1 * * 0,6` UTC. Missing `VNSTOCK_API_KEY` must be fixed by Stock owner; `preflight_only=true` must pass before ingestion.
- Media/Auth do not require native scheduled publisher jobs. Preserve purposeful manual/release workflows and useful CI/test/security workflows.
- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, digest/provenance gates, GitOps promotion/reconciliation, rollout and health.
- `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` is read-only. No duplicate direct SSH/Compose deployment authority.

## Current production evidence

- Latest full read-only K3s inspection #42417844482 (21:51:41Z): node Ready/ARM64, K3s v1.36.3+k3s1, K3s runtime containerd 2.3.2-k3s2, disk 56% (~20 GiB free), RAM ~19 GiB available.
- Reconcile #42423113109 (22:59:05Z) captured a newer pod snapshot at 22:59:28Z: Media backend/frontend and MicroFE Shell/WS/NATS Running; Stock Admin x2 and newer Backend ImagePullBackOff; older Stock Backend/Frontend Running. TCE/Auth/Keycloak remain intentional 0/0.
- Reconcile #42423113109 passed GHCR read access and Auth runtime Secret provision/verification (values suppressed), left shared `ghcr-pull` unchanged, found no manifest drift and skipped apply/rollout. `ALLOW_IMAGE_CHANGES=false`.
- No new publisher run/digest handoff or production image promotion was observed. TCE WF-06 still fails four public HTTP 200 probes with HTTP 503.

## Protected decommission status

Stock/Media remain retired from active Platform GitOps but legacy namespaces/workloads are still present. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider ownership attestation, dedicated Media runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight. Current runner is active; backup/retention and DNS ownership are not verified. No deletion or runner retirement occurred.

## Security follow-up

A prior short-lived runner registration token appeared in an Actions environment dump. PR #1416 masks the token before `GITHUB_OUTPUT`, and later bootstrap verification showed masked output. Platform owner must still inspect runner registrations and audit log; the current connector cannot certify registry cleanliness.

Detailed evidence: [2026-11-08-0605-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0605-ict.md)
