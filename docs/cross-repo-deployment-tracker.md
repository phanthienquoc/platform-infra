# Cross-repo production deployment readiness

Current review: **2026-11-08 06:05 ICT / 2026-11-07 23:05 UTC**

This is the rolling operational summary. Detailed immutable run/PR checkpoints remain under [docs/cross-repo-deployment-checkpoints](cross-repo-deployment-checkpoints/); preserve the archive when refreshing this file.

## Five-repository state

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `4984020757518c515b7be9f7741e489eec055fd1` | #1314/#544/#541/#539 (planning/docs) | PR #1423 merged; post-merge validation #42423484264 PASS. Native watchdog #42423187797 FAIL; recovery #42423100821 PASS; fallback reconcile #42423113109 PASS. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | Native WF-06 #42417660167 FAIL (four public probes HTTP 503); WF-12 #42411262379 FAIL/stale; WF-07 backup #42419031555 and integration #42417842240 PASS. |
| StockDividend | `783ae36f128ba5dffeba8ac1d242602f160ecfd0` | None | CI #42375688209 PASS (7/7); weekend scraper #42349150261 FAIL closed because `VNSTOCK_API_KEY` is missing. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS; no recent immutable publisher run/digest handoff. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft; both migration-gated | CI #42215394539 PASS; no recent release/digest handoff. |

## Latest Platform PR evidence

PR [#1423](https://github.com/phanthienquoc/platform-infra/pull/1423) was squash-merged from exact head `fcfa48384212073ef0322718879bfe49e6896979`, producing master `4984020757518c515b7be9f7741e489eec055fd1`. Its exact-head validation #42418587698 passed; post-merge master validation [#42423484264](https://github.com/phanthienquoc/platform-infra/actions/runs/42423484264) passed. It records PR #1422 evidence and updates the rolling tracker/inventory only. No production workflow, schedule, manifest, secret, image, workload or host change was made.

## Native schedule delivery — original event=schedule only

| Platform workflow | Latest native run | Result | Age at review | Inter-arrival gap | Budget |
|---|---|---|---:|---:|---:|
| reconcile-vps.yml | #42407410735, 19:41:08Z | PASS | 3h24m45s | 14,624s | 45m |
| inspect-vps.yml | #42409592778, 20:08:29Z | PASS | 2h57m24s | 16,311s | 75m |
| reconcile-schedule-watchdog.yml | #42423187797, 23:00:06Z | FAIL | 5m47s | 12,563s | 45m |
| recover-stale-ops.yml | #42423100821, 22:58:55Z | PASS | 6m58s | 12,553s | 45m |

The watchdog [#42423187797](https://github.com/phanthienquoc/platform-infra/actions/runs/42423187797) failed closed on stale native reconciliation/inspection and inter-arrival gaps. The recovery controller's native run [#42423100821](https://github.com/phanthienquoc/platform-infra/actions/runs/42423100821) succeeded and dispatched the existing reconcile authority as a fallback. That fallback is not native schedule evidence. Do not lower freshness budgets or count workflow_dispatch/workflow_run/repository_dispatch as native cron delivery.

TCE schedule evidence:
- Native WF-06 [#42417660167](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42417660167) at 21:49:14Z failed all four strict HTTP 200 probes (TCE web/API and Auth liveness/readiness returned HTTP 503). Its inter-arrival gap from #42399835467 was 13,197s (3h39m57s), above the 1,500s/25m budget; age at review is 1h16m39s.
- Native WF-12 [#42411262379](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42411262379) at 20:29:03Z failed the WF-06 freshness check. Its inter-arrival gap from #42392155494 was 13,949s (3h52m29s), above the 1,500s budget; age at review is 2h36m50s.
- Native WF-07 integration #42417842240 and backup #42419031555 passed. Workflow_run heartbeats are transport evidence only, not native schedule evidence.
- Keep WF-06/WF-12 schedules and strict HTTP 200 checks unchanged. TCE market-scan schedule unchanged.

Stock weekend scraper cron remains `0 1 * * 0,6` UTC. The latest native run failed before dependency installation or ingestion because the repository secret is missing. The next Sunday run is expected at 01:00Z / 08:00 ICT; Stock owner must add `VNSTOCK_API_KEY` and run `preflight_only=true` first. Do not ingest before authenticated non-guest entitlement passes.

## Latest K3s runtime evidence

Latest full read-only inspection [#42417844482](https://github.com/phanthienquoc/platform-infra/actions/runs/42417844482) generated `debug/vps-latest.md` at 21:51:41Z. A newer runtime pod snapshot was captured by reconciliation #42423113109 at 22:59:28Z; this is not a replacement for the full inspection.

- Node `tce-k3s-01`: Ready, ARM64, Ubuntu 22.04.5; K3s v1.36.3+k3s1; K3s containerd 2.3.2-k3s2.
- Last full inspection: disk 56% used (~20 GiB free), available RAM ~19 GiB.
- Runtime snapshot: Media backend/frontend and MicroFE Shell/WS/NATS Running.
- Stock Admin (two pods) and newer Stock Backend remain ImagePullBackOff; the last full inspection attributes tag `12d63b4` to a missing ARM64 platform manifest. Older Stock Backend and Stock Frontend remain Running.
- TCE frontend/service, Auth and Keycloak remain intentional 0/0 maintenance. No live workload health is asserted for these lanes.
- Platform and dedicated Media runner services remain active/enabled. Stock/Media namespaces remain Active.
- External backup/retention and authoritative DNS/provider ownership are not verified. No Stock/Media VolumeSnapshot references were reported; this does not prove external backup completeness.
- Docker 29.1.3 and host containerd.io 2.2.1 have newer packages available; `restart_required=yes`. No upgrade, cleanup or reboot occurred.

## Latest reconciliation and immutable release contracts

Reconciliation [#42423113109](https://github.com/phanthienquoc/platform-infra/actions/runs/42423113109) completed successfully in fallback `workflow_dispatch` apply mode with `ALLOW_IMAGE_CHANGES=false`:
- GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE web/service.
- Auth runtime Secret provision/verification passed with values suppressed; shared `ghcr-pull` remained unchanged.
- TCE release pairing passed.
- GitOps preflight found no manifest drift; manifest apply and rollout were correctly skipped.
- Auth and TCE lanes passed only by confirming intentional zero-replica maintenance; this is not live service recovery.

Static cross-repo contract review:
- TCE WF-03 is manual-only, builds ARM64 images, uses a version + full-source-SHA release tag, verifies web/service registry digests and sends `tce-release-requested` with app/release/digests/source run/path/event/full SHA. Platform's receiver consumes and validates those fields.
- Auth `release.yml` is manual-only, builds ARM64 with provenance/SBOM, verifies SHA/version tags resolve to the same digest, and sends `auth-image-published` with source run/path/event/full SHA. Platform's receiver consumes and validates the digest-bound payload.
- Stock `deploy.yml` verifies ARM64 full-SHA image tags/digests; Stock is retired from active Platform GitOps and has no production handoff in this state.
- Media WF-03 verifies immutable full-SHA release tags, ARM64 manifests and digests; its release summary explicitly states no Platform deployment handoff is configured because Media is retired from active Platform GitOps.
- No new publisher run, digest/provenance handoff or production image promotion was observed. Static contract review is not evidence of a fresh publication.

## Ownership, blockers and exact next actions

1. **Platform owner:** inspect runner registrations and GitHub audit log for unexpected registrations during the earlier short-lived runner registration-token validity window. PR #1416 masks the token before output and later bootstrap verification showed masked output, but registry cleanliness is not certified by the current connector.
2. **GitHub Actions administrator:** investigate missed Platform native schedule delivery; require another original native cycle and in-budget inter-arrival for each workflow. Keep the watchdog fail-closed and do not change cadence/budgets to hide stale delivery.
3. **TCE/service owner:** restore WF-06/WF-12 native cadence and investigate the four HTTP 503 endpoints. Obtain explicit service-owner approval before any replica change.
4. **Stock owner:** add `VNSTOCK_API_KEY`, run safe `preflight_only=true`, confirm authenticated non-guest entitlement; no ingestion before that gate.
5. **Auth/Supabase owner:** resolve migration provenance and connected GitHub integration side effects before PR #75/#76 are retargeted or merged.
6. **Stock/Media owners:** provide external backup/retention and authoritative DNS/provider evidence. Retire the dedicated Media runner (idle, stopped, disabled and unregistered) before any namespace deletion.
7. **Platform operator:** obtain a fresh read-only K3s inspection before subsequent decommission/maintenance decisions. Docker/containerd upgrade/reboot requires a separate maintenance window.

Stock/Media decommission remains manual-only. Delete requires production Environment approval, exact namespace confirmation, backup/external-data review, authoritative DNS/provider attestation, Media runner retirement proof and fresh PVC/PV/VolumeSnapshot preflight. Current evidence does not satisfy those gates.

No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, new secret write, DNS/database/storage mutation or host maintenance occurred in this review. Auth runtime Secret provisioning/verification in #42423113109 was performed by the existing authorized reconciliation workflow; values were suppressed. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

Detailed evidence: [2026-11-08-0605-ict.md](cross-repo-deployment-checkpoints/2026-11-08-0605-ict.md)
