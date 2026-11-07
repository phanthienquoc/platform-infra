# Cross-repo workflow inventory and deployment ownership

Current review: **2026-11-08 04:55 ICT / 2026-11-07 21:55 UTC**

This is the rolling inventory. Timestamped detailed evidence is retained under docs/cross-repo-deployment-checkpoints/.

| Repository | App-owned workflows | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds; receives app release events | Sole production manifests, shared GHCR pull credentials, runtime Secrets, digest/provenance validation, GitOps promotion/reconciliation, rollout/health, read-only inspection and protected Stock/Media decommission | Master c6ca9f; inspection PR #1421 merged; latest manual reconcile #42417693554 passed with no drift/apply skipped; native schedule runs remain stale. |
| TCE Dashboard | CI/tests; WF-03 publisher; WF-06 public health; WF-07 backup/integration; WF-08B MicroFE publisher; WF-12 watchdog; WF-13 recovery | No production SSH/Compose/K3s apply; Platform receives digest-bound events and owns production apply/reconciliation | Master 7ab52078; native WF-06 #42417660167 failed four HTTP 503 probes; native WF-12 #42411262379 stale/failing; workflow_run heartbeat is not native evidence. |
| StockDividend | CI/tests; ARM64 immutable image publisher; weekend scraper with safe credential preflight | Retired from active Platform GitOps; legacy workloads await protected decommission | Master 783ae36; CI 7/7; scraper #42349150261 failed closed because VNSTOCK_API_KEY is missing. |
| Media Generation | CI/tests; immutable ARM64 publisher with full-SHA release tag and digest verification | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission | Master 54f3a76; CI PASS; backend/frontend and dedicated runner remain active in latest inspection. |
| Authentication | CI/tests; manual-only immutable ARM64 release publisher with full-SHA/versioned tags, provenance/SBOM and digest handoff | Platform owns runtime manifests/Secrets and digest-pinned GitOps apply | Master 3b60ff4; CI PASS; PR #75/#76 remain Supabase migration-gated. |

## Evidence and acceptance rules

- Native schedule evidence requires original event=schedule, master branch, attempt 1, exact workflow path and full source SHA. Manual, push, workflow_run and repository_dispatch events are separate evidence classes.
- Platform reconcile cadence remains 7,22,37,52 * * * *; inspection/watchdog/recovery cron and freshness budgets remain unchanged. Current native gaps exceed the configured 45/75/45/45-minute budgets; watchdog remains fail-closed.
- TCE WF-06 remains */15 * * * * and strict public HTTP 200 checks remain unchanged. Its latest native run is recent but failed four endpoints with HTTP 503 after a long inter-arrival gap. WF-12 native delivery remains stale; workflow_run heartbeat proves transport only.
- Stock weekend scraper remains 0 1 * * 0,6 UTC. Missing VNSTOCK_API_KEY must be fixed by Stock owner; preflight_only=true must pass before ingestion.
- Media/Auth do not require native scheduled publisher jobs. Preserve purposeful manual/release workflows and useful CI/test/security workflows.
- App repositories own tests/builds and immutable GHCR publishing. Platform alone owns production manifests, shared pull credentials, digest/provenance gates, GitOps promotion/reconciliation, rollout and health.
- reconcile-vps.yml is the only production apply authority; inspect-vps.yml is read-only. Do not add direct SSH/Compose deployment authority.

## Current production evidence

- Latest read-only K3s inspection #42417844482 (21:51:41Z): node Ready/ARM64, K3s v1.36.3+k3s1, runtime containerd 2.3.2-k3s2, disk 56% (~20GiB free), RAM ~19GiB available. Media/MicroFE Running; Stock Admin x2 and newer Backend ImagePullBackOff on 12d63b4 without ARM64 manifest; older Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0; OIDC 503. Media runner active. External backup/retention and DNS ownership unverified.
- Manual reconciliation #42417693554 passed GHCR read access and Auth runtime Secret verification/provisioning (values suppressed), left shared ghcr-pull unchanged, found no manifest drift and skipped manifest apply/rollout. Stock ImagePullBackOff persists outside active Platform GitOps.
- No new publisher run/digest handoff or production image promotion was observed.

## Protected decommission status

Stock/Media remain retired from active Platform GitOps but legacy namespaces/workloads are still present. The read-only plan mode reports namespace/storage/Ingress/runner state. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider ownership attestation, dedicated Media runner idle/stopped/disabled/unregistered proof and fresh PVC/PV/VolumeSnapshot preflight. Current runner is active; backup/retention and DNS ownership are not verified. No deletion or runner retirement occurred.

## Security follow-up

A prior short-lived runner registration token appeared in an Actions environment dump. PR #1416 masks the token before GITHUB_OUTPUT and later bootstrap verification showed the masked value. Platform owner must still inspect runner registrations and audit log; the connector cannot certify registry cleanliness.

Detailed evidence: docs/cross-repo-deployment-checkpoints/2026-11-08-0455-ict.md


---

## PR #1422 merge record — 2026-11-08 05:00 ICT

Rolling inventory compaction merged at `c6ca9f92d35b69f99e0ff1308c3ac097e2cffa5b`. PR #1422 exact-head validation #42418449005 and post-merge validation #42418489331 passed. Historical detailed evidence remains archived in 50 timestamped checkpoint files; the inventory is now a concise current ownership/evidence view. No workflow, cron, production manifest, publisher, dispatch or deployment authority changed. TCE market-scan schedule unchanged.
