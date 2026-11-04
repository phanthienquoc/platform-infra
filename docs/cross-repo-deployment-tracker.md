# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 02:07 ICT (19:07 UTC)
Platform Infra master at checkpoint: 2d780e812003d7190b08283b64bef60fad643eb8

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | 2d780e812003 | #1222, #544, #541, #539 (all draft) | PR #1236 merged as 2d780e81; exact-head validate-manifests #41883005453 PASS. No post-merge validation run or complete current-master CI suite has been verified. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6 | None | Native WF-06 #41880229621 failed all four HTTP 200 probes (HTTP 503); native WF-12 #41877745265 failed freshness. WF-12 workflow_run #41880929859 and Platform receiver #41881214993 passed heartbeat forwarding/payload validation, not native schedule health. |
| phanthienquoc/stockdividend | 50ba0dfb67eb | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Source handoff and paired digest promotion dispatch remain SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aaf | None | Media CI #41617592783 PASS. Latest inspected snapshot shows backend/frontend 1/1 with digest-pinned imageIDs; snapshot is aging and not current health. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee | #75 ready; #76 draft | Auth service CI #41670642852 PASS; PR #75 #40446492086 and #76 #41329425940 passed on their exact heads. Supabase Preview SKIPPED; production integration/migration gate remains closed. |

## Current actions

1. Continue validating native Platform schedule delivery. Native scheduled inspect #41881867627 succeeded at 00:55:54 ICT and produced the snapshot below; this is one successful tick, not proof of sustained recovery. Do not treat manual dispatch, workflow_run, repository_dispatch, or reruns as native schedule evidence.
2. Obtain protected STOCKDIVIDEND_ACTIONS_READ_TOKEN access and explicit paired Admin/Backend digest authorization before StockDividend promotion. Promote only through the existing Platform GitOps receiver.
3. Resolve TCE service availability while preserving strict HTTP 200 health assertions. Do not infer health from zero-replica workloads or successful heartbeat forwarding.
4. Resolve Auth Supabase GitHub integration target/effects and migration provenance before merging #75/#76, running migrations, or activating Auth/Keycloak.
5. Obtain a VPS maintenance window before pending Ubuntu, Docker, and containerd upgrades or reboot.
6. Keep optional VPS MCP PR #1222 in draft until Docker/Kubernetes mutation paths are removed, real UID/GID isolation is demonstrated, and reproducible build/test/lockfile/security validation is supplied.

## Current runtime blockers

- **K3s snapshot:** Native scheduled inspection #41881867627 succeeded at 17:55:54 UTC (00:55:54 ICT); debug/vps-latest.md was generated at 17:56:19 UTC (00:56:19 ICT) and merged by PR #1235 as 8d019eab1da2c471c1b1014b8d376be88c0ea190. At 02:07 ICT this evidence is about 71 minutes old and close to the 75-minute freshness budget. Node tce-k3s-01 was Ready, ARM64, K3s v1.36.3+k3s1, disk 56%, available memory about 19 GiB; GitOps drift was clean. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Two Stock Admin Pods and the new Stock Backend Pod were ImagePullBackOff; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0. This is point-in-time evidence, not current health.
- **StockDividend:** Admin and new Backend still use tag 12d63b4, which has no matching ARM64 manifest (no match for platform in manifest). Old Backend and Frontend were 1/1 in the snapshot. Immutable ARM64 publication passed, but source handoff and paired promotion dispatch were skipped. Do not promote either image independently.
- **TCE/Auth:** Native WF-06 #41880229621 failed all four public endpoint checks (TCE web, TCE API, Auth liveness, Auth readiness) with HTTP 503 instead of HTTP 200. TCE and Auth/Keycloak workloads were 0/0 in the latest snapshot. Heartbeat forwarding success does not establish service health.
- **Host maintenance:** restart_required=yes; Ubuntu, Docker and containerd updates remain pending, including containerd 2.4.2 and Docker 29.9.3. No reboot or package upgrade was performed.

## Native schedule evidence

| Workflow | Cron (unchanged) | Latest verified native schedule evidence | Result |
|---|---|---|---|
| inspect-vps.yml | 2,32 * * * * | #41881867627 at 00:55:54 ICT | PASS. Genuine event=schedule; inspection PR #1235 merged after exact-head manifest validation #41882047624. One success only; sustained recovery not established. |
| reconcile-vps.yml | 7,22,37,52 * * * * | #41860865532 at 22:44:26 ICT | FAIL in StockDividend health. Later #41881241239 at 00:52 ICT was workflow_dispatch and also failed Stock health; it is not a native schedule tick. |
| recover-stale-ops.yml | 10,25,40,55 * * * * | #41852388418 at 21:55:14 ICT | PASS. Later #41881214993 (repository_dispatch) and #41881585524 (workflow_dispatch) are not native schedule events. |
| reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | #41861131656 at 22:45:57 ICT | FAIL on stale inspection/recovery evidence. Workflow_run watchdog #41881772345 was skipped because its source was a manual reconciliation; no later native watchdog result has been verified in this checkpoint. |

TCE native schedule evidence:
- WF-06 #41880229621 at 00:45:34 ICT: FAIL, all four public probes returned HTTP 503.
- WF-12 #41877745265 at 00:27:45 ICT: FAIL on freshness.
- WF-12 workflow_run #41880929859 at 00:50:18 ICT: PASS for delivery verification and authenticated heartbeat dispatch.
- Platform receiver #41881214993 (repository_dispatch): PASS for external heartbeat payload validation. Neither run is native Platform schedule evidence or proof of TCE endpoint health.

No newer native schedule run was independently verified for this checkpoint. Preserve all existing cron expressions, especially the TCE market-scan schedule. Do not substitute reruns, manual dispatches, workflow_run, or repository_dispatch for native schedule evidence.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout, and health verification.
- reconcile-vps.yml is the sole production apply authority. inspect-vps.yml is read-only.
- Preserve useful CI, tests, security, backup, manual, release, and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- PR #1236 was merged at exact head e487eb605f172ce15cc404d7c31680f4fc603254 as 2d780e812003d7190b08283b64bef60fad643eb8; its exact-head validate-manifests run #41883005453 passed. No post-merge validation evidence is claimed.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot, or schedule expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Platform native inspection #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Platform inspection snapshot validation #41882047624: https://github.com/phanthienquoc/platform-infra/actions/runs/41882047624
- Platform PR #1236 exact-head validation #41883005453: https://github.com/phanthienquoc/platform-infra/actions/runs/41883005453
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

[2026-11-05 02:07 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0207-ict.md) records the #1236 merge, exact-head validation, current five-repository heads/open PRs, latest independently verified runtime evidence, and remaining release/schedule gates.
