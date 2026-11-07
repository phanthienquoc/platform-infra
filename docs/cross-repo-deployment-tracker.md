# Cross-repo production deployment readiness

Current review: **2026-11-08 06:11 ICT / 2026-11-07 23:11 UTC**

This is the rolling operational summary. Detailed immutable run/PR checkpoints remain under [docs/cross-repo-deployment-checkpoints](cross-repo-deployment-checkpoints/); preserve the archive.

## Five-repository state

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `769c558f2ded93979f6857ba35d5954404d25949` | #1314/#544/#541/#539 (planning/docs) | PR #1424/#1425 merged. Native reconcile #42423799465 PASS; watchdog #42423187797 FAIL; recovery #42423100821 PASS. Fresh inspection #42423938208 PASS. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-06 #42417660167 FAIL (four HTTP 503 probes); WF-12 #42411262379 FAIL/stale; WF-07 backup #42419031555 and integration #42417842240 PASS. |
| StockDividend | `783ae36f128ba5dffeba8ac1d242602f160ecfd0` | None | CI #42375688209 PASS (7/7); scraper #42349150261 FAIL closed because `VNSTOCK_API_KEY` is missing. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS; no recent immutable publisher run/digest handoff. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft; both migration-gated | CI #42215394539 PASS; no recent release/digest handoff. |

## Platform PRs merged

- [PR #1424](https://github.com/phanthienquoc/platform-infra/pull/1424): exact head `dd89cd8ba147a7d5bb13e80328491453475613b7`, squash merge `8e64f0710c857c53284be6e2ad3e675307d8ceef`. Exact-head #42423773316 PASS; post-merge #42423822311 PASS. Updated tracker/inventory/checkpoint.
- [PR #1425](https://github.com/phanthienquoc/platform-infra/pull/1425): automated read-only inspection, exact head `e6a60d54347963378a34f0c78a481b30f3935403`, squash merge `769c558f2ded93979f6857ba35d5954404d25949`. Inspection #42423938208 PASS; exact-head validation step PASS; validation #42424034112 PASS. Changed `debug/vps-latest.md` only.

Neither PR changed production workflows, schedules, manifests, secrets, images, workloads or host state.

## Native schedule delivery — original event=schedule only

| Platform workflow | Latest native run | Result | Age at review | Inter-arrival gap | Budget |
|---|---|---|---:|---:|---:|
| reconcile-vps.yml | #42423799465, 23:07:40Z | PASS | 3m47s | 12,392s | 45m |
| inspect-vps.yml | #42409592778, 20:08:29Z | PASS | 3h02m58s | 16,311s | 75m |
| reconcile-schedule-watchdog.yml | #42423187797, 23:00:06Z | FAIL | 11m21s | 12,563s | 45m |
| recover-stale-ops.yml | #42423100821, 22:58:55Z | PASS | 12m32s | 12,553s | 45m |

Native reconcile #42423799465 succeeded, but its gap from #42407410735 was 12,392s (3h26m32s), still above the 2,700s budget. One fresh event does not restore cadence; the next original native cycle must arrive within budget. Native watchdog remains fail-closed. Workflow_run watchdog #42423924180 also failed on stale inter-arrival evidence and is not native evidence.

Native recovery #42423100821 succeeded. Recovery workflow_dispatch #42423906835 then completed successfully and dispatched read-only inspection #42423938208. That inspection is a manual fallback, not a native schedule event.

TCE schedule evidence:
- Native WF-06 [#42417660167](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42417660167) at 21:49:14Z failed all four strict HTTP 200 probes (TCE web/API and Auth liveness/readiness returned HTTP 503). Gap from #42399835467 was 13,197s (3h39m57s), above the 1,500s/25m budget; age at review 1h22m13s.
- Native WF-12 #42411262379 at 20:29:03Z failed WF-06 freshness. Gap from #42392155494 was 13,949s (3h52m29s), above its 1,500s budget; age at review 2h42m24s.
- Native WF-07 integration #42417842240 and backup #42419031555 passed. workflow_run heartbeat is transport evidence only.
- Keep WF-06/WF-12 schedules and strict HTTP 200 checks unchanged. TCE market-scan schedule unchanged.

Stock scraper cron remains `0 1 * * 0,6` UTC. Latest native run failed before dependencies/ingestion because the secret is missing. Next Sunday run expected 01:00Z / 08:00 ICT; Stock owner must add `VNSTOCK_API_KEY` and run `preflight_only=true` first. No ingestion before authenticated non-guest entitlement passes.

## Latest K3s snapshot

Read-only inspection [#42423938208](https://github.com/phanthienquoc/platform-infra/actions/runs/42423938208) succeeded and generated `debug/vps-latest.md` at 23:09:36Z. PR #1425 carried that snapshot to master.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- RAM 23 GiB total / ~19 GiB available. Disk 45 GiB total / 26 GiB used / 20 GiB available (56%, pressure normal).
- Docker 29.1.3; 20 images / 9.195 GB, ~5.773 GB reclaimable; 12 containers active. No cleanup performed.
- Host updates include Docker 29.9.3 and containerd.io 2.4.2-3; installed containerd.io 2.2.1-1. `restart_required=yes`. No upgrade/reboot.
- Platform runner and dedicated Media runner services are active/enabled; runner policy `rollout-status-v15-core-workloads`.
- Media backend/frontend and MicroFE Shell/WS/NATS Running.
- Stock Admin (two pods) and newer Stock Backend remain ImagePullBackOff on `12d63b4`; kubelet reports no ARM64 manifest. Older Stock Backend and Frontend remain Running.
- TCE frontend/service, Auth service and Keycloak remain intentional 0/0 maintenance.
- Only reported PVC/PV is `k3s-debug/k3s-debug-logs` (1 GiB, Bound); no Stock/Media VolumeSnapshot references. This does not prove external backup/retention completeness.
- `stock-prod` and `media-prod` remain Active. Ingress host inventory includes Stock, Media, TCE, SSO and MicroFE names; authoritative DNS/provider ownership is not verified.

## Latest scheduled reconciliation and health lanes

Scheduled reconciliation [#42423799465](https://github.com/phanthienquoc/platform-infra/actions/runs/42423799465) completed successfully at 23:09:15Z on pre-PR-#1424 SHA `4984020757518c515b7be9f7741e489eec055fd1` (later changes were documentation/inspection only):
- GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE web/service.
- Auth runtime Secret provision/verification passed with values suppressed; shared `ghcr-pull` remained unchanged.
- TCE release pairing passed.
- GitOps preflight found no drift; manifest apply, image guard, rollout and drift recheck were skipped correctly.
- TCE lane passed image pairing and confirmed intentional zero replicas; no live health asserted.
- MicroFE active health passed; rollout skipped.
- Auth Secret, HTTPS and maintenance-state checks passed; Auth remains intentional zero replicas.
- Keycloak lane skipped; final deployment gate passed.

This is successful native reconciliation/preflight and health verification, not a new image promotion, production rollout or TCE/Auth restoration.

## Immutable release and dispatch contract review

- TCE WF-03 is manual-only; it builds ARM64, tags with version + full source SHA, verifies web/service digests and sends `tce-release-requested` with app/release/digests/source run/path/event/full SHA. Platform receiver consumes and validates these fields.
- Auth `release.yml` is manual-only; it builds ARM64 with provenance/SBOM, verifies SHA/version tags against one digest and sends `auth-image-published` with source run/path/event/full SHA. Platform receiver consumes and validates the digest-bound payload.
- Stock `deploy.yml` verifies ARM64 full-SHA tags/digests; Stock is retired from active Platform GitOps and has no production handoff in this state.
- Media WF-03 verifies immutable full-SHA ARM64 tags/digests and explicitly sends no Platform dispatch because Media is retired from active Platform GitOps.
- No new publisher run, digest/provenance handoff or production image promotion was observed. Static workflow review is not evidence of fresh publication.

## Ownership, blockers and exact next actions

1. **Platform owner:** audit runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived runner registration-token validity window. PR #1416 masks the token before output and later bootstrap verification showed masked output, but registry cleanliness is not certified.
2. **GitHub Actions administrator:** investigate missed Platform native schedule delivery; require the next original native cycle and in-budget inter-arrival for each workflow. Do not lower freshness budgets or count fallback/manual events.
3. **TCE/service owner:** restore WF-06/WF-12 native cadence and investigate the four HTTP 503 endpoints. Obtain explicit approval before any replica change.
4. **Stock owner:** add `VNSTOCK_API_KEY`, run safe `preflight_only=true`, confirm authenticated non-guest entitlement; no ingestion before that gate.
5. **Auth/Supabase owner:** resolve migration provenance and connected GitHub integration side effects before PR #75/#76 are retargeted or merged.
6. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence. Retire the dedicated Media runner (idle, stopped, disabled and unregistered) before namespace deletion.
7. **Platform operator:** use the new read-only snapshot for planning only. Docker/containerd upgrade/reboot requires a separate maintenance window; no image cleanup without a retention/rollback plan.

Stock/Media decommission remains manual-only. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, new secret write, DNS/database/storage mutation or host maintenance occurred. Auth runtime Secret provisioning/verification in #42423799465 was performed by the existing authorized reconciliation workflow; values were suppressed. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0611-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0611-ict.md)
