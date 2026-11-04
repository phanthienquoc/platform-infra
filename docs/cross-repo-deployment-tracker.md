# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 04:03 ICT (2026-11-04 21:03 UTC)
Platform Infra master at checkpoint: fbe997ab3c90799f987d78701fd201fee401c247

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | `fbe997ab3c90` | #1222, #544, #541, #539 (all draft) | Master `validate-manifests` #41902468271 PASS on this exact SHA at 03:00 ICT. No newer native scheduled run is present in the inspected Actions history. |
| phanthienquoc/TCE-dashboard | `52cecd5584e6` | None | Native WF-07 #41900042968 PASS at 02:45 ICT. Native WF-06 #41880229621 FAIL (four public endpoints HTTP 503); native WF-12 #41877745265 FAIL (WF-06 freshness). WF-12 workflow_run #41900072829 also FAIL on delivery verification, although its Platform heartbeat notification job PASS. |
| phanthienquoc/stockdividend | `50ba0dfb67eb` | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Scraper/Admin/Backend full-source-SHA tags resolve to ARM64 digests. Production GitOps promotion is explicitly disabled by the publisher gate; handoff validation and paired dispatch are SKIPPED. |
| phanthienquoc/media-generation | `e4c7d8990aaf` | None | Media CI #41617592783 PASS. Latest inspected runtime snapshot #41900544272 showed backend/frontend 1/1 with digest-pinned imageIDs; snapshot is now about 74 minutes old. |
| phanthienquoc/phanthienquoc-authentication | `f978a3f378ee` | #75 ready; #76 draft | Auth service CI #41670642852 PASS; Supabase Preview SKIPPED. PR #75 exact head `a8e8a1d99e86` validation #40446492086 PASS; PR #76 exact head `f19cacb0bf2b` validation #41329425940 PASS. Production integration/migration gate remains closed. |

## Current actions

1. Restore and verify native Platform schedule delivery independently for inspect-vps, reconcile-vps, recover-stale-ops, and reconcile-schedule-watchdog. Latest verified native inspection is #41881867627 at 00:55 ICT; the latest native reconcile/watchdog/recovery remain #41860865532, #41861131656, and #41852388418. Do not count workflow_dispatch, workflow_run, repository_dispatch, or reruns as native schedule evidence.
2. Keep StockDividend production promotion disabled. The latest publisher's Gate production GitOps promotion job explicitly logged that promotion is disabled; therefore release handoff validation and paired digest dispatch were skipped. Do not describe this as only a missing Actions:read token and do not enable promotion without explicit release authorization. Preserve the paired Admin/Backend release contract.
3. Resolve TCE service availability while preserving strict HTTP 200 endpoint assertions. Current K3s desired replicas are 0/0 for TCE and Auth; successful heartbeat forwarding is not service health.
4. Resolve Auth Supabase integration target/effects and migration provenance before merging #75/#76, running migrations, or activating Auth/Keycloak.
5. Obtain a VPS maintenance window before pending Ubuntu, Docker, and containerd upgrades or reboot.
6. Keep optional VPS MCP PR #1222 in draft. Its current diff still exposes Docker restart and Kubernetes Deployment patch/restart capabilities, contains literal backslash-n sequences in TypeScript/installer source, and declares but does not pass SHELL_UID/GID into child-process execution. Local build/tests, YAML validation, ShellCheck, and a committed lockfile are absent.

## Current runtime blockers

- **K3s snapshot:** Read-only inspection #41900544272 completed at 02:48:43 ICT; `debug/vps-latest.md` was generated at 02:48:52 ICT and merged by inspection PR #1238 as `53e7acc8f58f519959c22b0a036140604b210995`. At 04:03 ICT this snapshot is about 74 minutes old and is near the 75-minute freshness budget. Node `tce-k3s-01` was Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, available memory about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Two Stock Admin Pods and the new Stock Backend Pod were ImagePullBackOff; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0. This is point-in-time evidence, not continuous health.
- **StockDividend:** Production Admin and new Backend still reference tag `12d63b4`, which has no ARM64 manifest (`no match for platform in manifest`). The latest successful publisher run #41563856933 verified these immutable linux/arm64 digests for source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`:
  - Scraper: `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`
  - Admin: `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`
  - Backend: `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`
  The publisher's `Gate production GitOps promotion` job succeeded by enforcing the disabled release hold and logged: production promotion is disabled; continue immutable publication without a dispatch. Consequently `Validate Platform Infra release handoff before promotion` and `Dispatch atomic StockDividend digest promotion` were SKIPPED. No production promotion is authorized by this evidence.
- **TCE/Auth/Keycloak:** TCE frontend/service and MicroFE Auth/Keycloak are 0/0 in the latest snapshot. Native WF-06 #41880229621 failed all four strict public endpoint checks (TCE web, TCE API, Auth liveness, Auth readiness returned HTTP 503). Native WF-12 #41877745265 failed freshness; later workflow_run #41900072829 failed WF-06 delivery verification while the authenticated heartbeat notification job succeeded. Heartbeat delivery is not service health.
- **Media/MicroFE:** Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 in the snapshot; Media imageIDs are digest-pinned. No newer Media CI/publisher run was observed after #41617592783.
- **Host maintenance:** `restart_required: yes`; Ubuntu upgrades remain pending, including containerd 2.4.2 and Docker 29.9.3 (installed versions: containerd 2.3.2-k3s2, Docker 29.1.3). No reboot or package upgrade was performed.

## Native schedule evidence

| Workflow | Cron (unchanged) | Latest verified native schedule evidence | Result |
|---|---|---|---|
| inspect-vps.yml | `2,32 * * * *` | #41881867627 at 00:55:54 ICT | PASS. Genuine `event=schedule`; inspection PR #1235 merged after exact-head manifest validation #41882047624. Later #41900544272 at 02:48:43 was workflow_dispatch, not a native tick. No newer native inspect run appears in the current schedule-event history. |
| reconcile-vps.yml | `7,22,37,52 * * * *` | #41860865532 at 22:44:26 ICT | FAIL in StockDividend health lane. Later #41900128585 at 02:46:08 was workflow_dispatch and also failed Stock health; it is not native schedule evidence. No newer native reconcile run appears in the current schedule-event history. |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | #41852388418 at 21:55:14 ICT | PASS. Later #41900480191 at 02:48:19 was workflow_dispatch, not native schedule evidence. No newer native recovery run appears in the current schedule-event history. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | #41861131656 at 22:45:57 ICT | FAIL on stale inspection/recovery evidence. No newer native watchdog run appears in the current schedule-event history. |

TCE native schedule evidence:
- WF-07 #41900042968 at 02:45:37 ICT: SUCCESS. Binance private API check passed; third-party order integration was skipped.
- WF-06 #41880229621 at 00:45:34 ICT: FAIL, all four public endpoint probes returned HTTP 503 instead of HTTP 200.
- WF-12 #41877745265 at 00:27:45 ICT: FAIL on freshness.
- WF-12 workflow_run #41900072829 at 02:45:48 ICT: overall FAIL because WF-06 schedule delivery verification failed; authenticated Platform heartbeat notification job succeeded. It is not a native schedule event.
- No newer native Platform or TCE schedule event was independently verified through 04:03 ICT. Preserve all existing cron expressions, especially the TCE market-scan schedule. Do not substitute reruns, manual dispatches, workflow_run, or repository_dispatch for native schedule evidence.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout, and health verification.
- `reconcile-vps.yml` is the sole production apply authority. `inspect-vps.yml` is read-only.
- Preserve useful CI, tests, security, backup, manual, release, and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot, or schedule expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Platform master validation #41902468271: https://github.com/phanthienquoc/platform-infra/actions/runs/41902468271
- Platform inspection #41900544272 (workflow_dispatch): https://github.com/phanthienquoc/platform-infra/actions/runs/41900544272
- Platform inspection validation #41900666915: https://github.com/phanthienquoc/platform-infra/actions/runs/41900666915
- Platform inspection snapshot PR #1238: https://github.com/phanthienquoc/platform-infra/pull/1238
- Platform native inspection #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Platform native reconcile #41860865532: https://github.com/phanthienquoc/platform-infra/actions/runs/41860865532
- Platform manual fallback reconcile #41900128585: https://github.com/phanthienquoc/platform-infra/actions/runs/41900128585
- Platform native watchdog #41861131656: https://github.com/phanthienquoc/platform-infra/actions/runs/41861131656
- Platform native recovery #41852388418: https://github.com/phanthienquoc/platform-infra/actions/runs/41852388418
- TCE native WF-07 #41900042968: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE WF-12 heartbeat/delivery verification #41900072829: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900072829
- TCE native WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE native WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth service CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75 exact-head validation #40446492086: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/40446492086
- Auth PR #76 exact-head validation #41329425940: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41329425940

## Latest workflow inventory checkpoint

[2026-11-05 04:03 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0403-ict.md) records current five-repository heads/open PRs, exact schedule-event evidence, Stock immutable digests and explicit disabled promotion gate, K3s snapshot age, and remaining release gates.
