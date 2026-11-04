# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 00:58 ICT (17:58 UTC)
Platform Infra master at checkpoint: 8d019eab1da2c471c1b1014b8d376be88c0ea190

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | 8d019eab1da2 | #1222, #544, #541, #539 (all draft) | Native scheduled inspection #41881867627 PASS; snapshot PR #1235 merged as 8d019eab; exact-head manifest validation #41882047624 PASS. Current master has no complete new CI suite; only a skipped recovery check is attached to the latest commit. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6 | None | Native WF-06 #41880229621 failed all four public HTTP 200 probes (HTTP 503). Native WF-12 #41877745265 failed freshness. Workflow-run WF-12 #41880929859 successfully verified delivery and forwarded the heartbeat; it is not native schedule evidence. |
| phanthienquoc/stockdividend | 50ba0dfb67eb | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Build/push passed, but source handoff and paired digest promotion dispatch were SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aaf | None | Media CI #41617592783 PASS. Latest read-only inspection shows backend/frontend 1/1 with digest-pinned imageIDs. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee | #75 ready; #76 draft | Auth service CI #41670642852 PASS; Supabase Preview SKIPPED. PR #75/#76 checks pass, but production Supabase integration and migration provenance remain gated. |

## Current actions

1. Keep validating native schedule recovery. A genuine native inspect-vps schedule run #41881867627 succeeded at 00:55:54 ICT and produced the fresh snapshot below. This is one successful tick, not proof of sustained recovery. Native reconcile, recovery and watchdog remain stale; continue separating schedule from workflow_dispatch, workflow_run, and repository_dispatch.
2. Obtain protected Actions:read access and explicit paired Admin/Backend digest authorization before any StockDividend promotion. Promote only through the existing Platform GitOps receiver.
3. Resolve TCE service availability and preserve strict HTTP 200 health assertions. Do not infer service health from zero-replica workloads or successful heartbeat forwarding.
4. Resolve Auth Supabase GitHub integration target/effects and migration provenance before merging #75/#76, running migrations, or activating Auth/Keycloak.
5. Obtain a VPS maintenance window before pending Ubuntu, Docker, and containerd upgrades or reboot.
6. Keep optional VPS MCP PR #1222 in draft until it removes Docker/Kubernetes mutation authority, proves actual UID/GID isolation, and supplies reproducible build/test/lockfile/security validation.

## Current runtime blockers

- **K3s snapshot:** Native scheduled inspection #41881867627 succeeded at 17:55:54 UTC (00:55:54 ICT). Snapshot debug/vps-latest.md was generated at 17:56:19 UTC (00:56:19 ICT) and merged by PR #1235 as master commit 8d019eab1da2c471c1b1014b8d376be88c0ea190. Exact-head manifest validation #41882047624 passed. Node tce-k3s-01 was Ready, ARM64, K3s v1.36.3+k3s1, disk 56%, available memory about 19 GiB; GitOps drift clean. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Stock Admin was 0/1 (two Pods ImagePullBackOff); new Stock Backend was 0/1; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0. Treat this as point-in-time evidence, not current health.
- **StockDividend:** Admin tag 12d63b4 (two Pods) and new Backend tag 12d63b4 still fail with "no match for platform in manifest" on ARM64. Old Backend remains 1/1 and Frontend 1/1. Latest manual/fallback reconciliation #41881241239 failed only in the Stock health lane; the earlier native scheduled reconcile #41860865532 also failed Stock health. Immutable ARM64 publisher #41563856933 succeeded, but handoff and paired promotion dispatch remain skipped. Do not promote either image independently.
- **TCE/Auth:** Latest native WF-06 #41880229621 failed all four public endpoint jobs (TCE web, TCE API, Auth liveness, Auth readiness) because HTTP 503 was returned instead of HTTP 200. TCE frontend/service and Auth/Keycloak are 0/0 in the latest K3s snapshot. Preserve strict HTTP 200 checks; heartbeat forwarding is not service health.
- **Healthy inspected workloads:** Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 with digest-pinned Media imageIDs. This is only the 00:56 ICT snapshot.
- **Host maintenance:** restart_required=yes; Ubuntu, Docker and containerd updates remain pending, including containerd 2.4.2 and Docker 29.9.3 packages. No reboot or upgrade was performed.

## Native schedule evidence

| Workflow | Latest native schedule evidence | Result |
|---|---|---|
| inspect-vps.yml (2,32 * * * *) | #41881867627 at 00:55:54 ICT | PASS. This is a genuine event=schedule run; it created inspection PR #1235, exact-head manifest validation passed, and the snapshot merged as 8d019eab. Require subsequent scheduled ticks before declaring sustained recovery. |
| reconcile-vps.yml (7,22,37,52 * * * *) | #41860865532 at 22:44:26 ICT | FAIL only in StockDividend workload health. Later #41881241239 at 00:52 ICT was workflow_dispatch, not schedule, and also failed Stock health. No newer native reconcile schedule was observed through 00:58 ICT. |
| recover-stale-ops.yml (10,25,40,55 * * * *) | #41852388418 at 21:55:14 ICT | PASS. Later #41881214993 (repository_dispatch) and #41881585524 (workflow_dispatch) succeeded but are not native schedule evidence. |
| reconcile-schedule-watchdog.yml (12,27,42,57 * * * *) | #41861131656 at 22:45:57 ICT | FAIL on stale inspection/recovery evidence. Workflow-run watchdog #41881772345 at 00:55 ICT was SKIPPED because its source was a manual reconciliation; no post-inspection scheduled watchdog result was observed yet. |

The inspection schedule has produced one real success after a long gap. Do not describe all Platform schedules as recovered: native reconcile, recovery and watchdog remain stale. The inspection run used the pre-inspection master SHA 2140b9714b7a, then rebased and merged its snapshot as PR #1235. The fallback reconciliation at 00:52 ICT was a manual dispatch and failed the Stock health gate.

TCE schedule evidence:
- Native WF-06 #41880229621 at 00:45:34 ICT: FAIL, four HTTP 503 endpoint checks.
- Native WF-12 #41877745265 at 00:27:45 ICT: FAIL.
- WF-12 workflow-run #41880929859 at 00:50:18 ICT: SUCCESS; its delivery verification and authenticated heartbeat dispatch passed. Platform receiver/recovery #41881214993 validated the external TCE heartbeat payload and completed successfully. These are workflow_run/repository_dispatch events, not native WF-12 or Platform schedule events.

Preserve all existing cron declarations, including the TCE market-scan schedule. Do not substitute reruns, manual dispatches, workflow-run events, or repository dispatches for native schedule evidence.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout, and health verification.
- reconcile-vps.yml is the sole production apply authority. inspect-vps.yml is read-only.
- Preserve useful CI, tests, security, backup, manual, release, and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot, or schedule expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Platform native inspection #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Platform native reconcile #41860865532: https://github.com/phanthienquoc/platform-infra/actions/runs/41860865532
- Platform fallback reconcile #41881241239: https://github.com/phanthienquoc/platform-infra/actions/runs/41881241239
- Platform native watchdog #41861131656: https://github.com/phanthienquoc/platform-infra/actions/runs/41861131656
- Platform native recovery #41852388418: https://github.com/phanthienquoc/platform-infra/actions/runs/41852388418
- TCE native WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE native WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- TCE heartbeat forwarder #41880929859: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880929859
- Platform TCE heartbeat receiver #41881214993: https://github.com/phanthienquoc/platform-infra/actions/runs/41881214993
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth service CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852

## Latest workflow inventory checkpoint

[2026-11-05 00:58 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0058-ict.md) records repository heads, open PRs, latest CI/publication checks, the first resumed native inspection schedule tick, current K3s snapshot, TCE heartbeat evidence, and remaining release gates.
