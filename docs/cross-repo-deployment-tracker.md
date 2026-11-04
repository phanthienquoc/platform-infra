# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 02:56 ICT (19:56 UTC)
Platform Infra master at checkpoint: 53e7acc8f58f519959c22b0a036140604b210995

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | 53e7acc8f58f | #1222, #544, #541, #539 (all draft) | Latest master commit is inspection snapshot PR #1238 (merge SHA 53e7acc8). Manual inspection #41900544272 PASS; validation #41900666915 PASS on the inspection branch. Current master SHA has zero check-runs; latest prior master validation #41894268626 PASS was on 101a97d5, not this SHA. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6 | None | WF-07 native schedule #41900042968 PASS (private API check PASS; third-party order integration SKIPPED). WF-12 workflow_run #41900072829 FAIL on WF-06 delivery verification; heartbeat notification job PASS. Native WF-06 #41880229621 failed all four HTTP 200 probes with HTTP 503; native WF-12 #41877745265 failed freshness. |
| phanthienquoc/stockdividend | 50ba0dfb67eb | None | CI #41563856934 PASS; immutable publisher #41563856933 PASS. Build-and-push PASS, but Platform handoff validation and paired digest dispatch were SKIPPED. Current master check-run API shows 11 successful build/CI checks plus the two skipped release-handoff jobs. |
| phanthienquoc/media-generation | e4c7d8990aaf | None | Media CI #41617592783 PASS (latest master check-run). Runtime snapshot #41900544272 shows backend/frontend 1/1 with digest-pinned imageIDs; this is point-in-time inspection, not continuous health. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee | #75 ready; #76 draft | Auth service CI #41670642852 PASS; Supabase Preview SKIPPED. PR #75 exact head a8e8a1d9: validate #40446492086 PASS, Preview SKIPPED. PR #76 exact head f19cacb0: validate #41329425940 PASS, Preview SKIPPED. Production integration/migration gate remains closed. |

## Current actions

1. Continue validating native Platform schedule delivery. The latest verified native inspect remains #41881867627 at 00:55:54 ICT. Newer inspection #41900544272 at 02:48:43 ICT was workflow_dispatch, not schedule. Do not count manual dispatch, workflow_run, repository_dispatch, or reruns as native schedule evidence.
2. Obtain protected STOCKDIVIDEND_ACTIONS_READ_TOKEN access and explicit paired Admin/Backend digest authorization before StockDividend promotion. Promote only through the existing Platform GitOps receiver.
3. Resolve TCE service availability while preserving strict HTTP 200 health assertions. Do not infer health from zero-replica workloads or successful heartbeat forwarding.
4. Resolve Auth Supabase GitHub integration target/effects and migration provenance before merging #75/#76, running migrations, or activating Auth/Keycloak.
5. Obtain a VPS maintenance window before pending Ubuntu, Docker, and containerd upgrades or reboot.
6. Keep optional VPS MCP PR #1222 in draft until Docker/Kubernetes mutation paths are removed, real UID/GID isolation is demonstrated, literal escape sequences in source/installer are corrected, and reproducible build/test/lockfile/security validation is supplied.

## Current runtime blockers

- **K3s snapshot:** Read-only inspection #41900544272 completed at 02:48:43 ICT; snapshot `debug/vps-latest.md` generated 02:48:52 ICT and was merged by PR #1238 as 53e7acc8f58f519959c22b0a036140604b210995. At 02:56 ICT this snapshot is about 7 minutes old. Node `tce-k3s-01` was Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, available memory about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Two Stock Admin Pods and the new Stock Backend Pod were ImagePullBackOff; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0. This is point-in-time evidence, not continuous health.
- **StockDividend:** Admin and new Backend still use tag `12d63b4`, which has no matching ARM64 manifest (`no match for platform in manifest`). Two Admin Pods and one new Backend Pod have no resolved imageID. Old Backend tag `23b2878` and Frontend tag `23b2878` are running with resolved imageIDs. Immutable ARM64 publication passed, but source handoff and paired promotion dispatch were skipped. Do not promote either image independently.
- **TCE/Auth/Keycloak:** TCE frontend/service and MicroFE Auth/Keycloak are 0/0 in the latest snapshot. Public Keycloak OIDC probes return HTTP 503. Native TCE WF-06 #41880229621 failed all four strict public endpoint checks (TCE web, TCE API, Auth liveness, Auth readiness). WF-12 #41900072829 at 02:45:48 ICT failed its WF-06 delivery verification, while its authenticated heartbeat notification job succeeded. Heartbeat delivery is not service health.
- **Media/MicroFE:** Media backend/frontend, MicroFE Shell/WS and NATS are 1/1 in the snapshot; imageIDs are digest-pinned for Media. No newer Media CI or publisher run was observed after #41617592783.
- **Host maintenance:** `restart_required: yes`; Ubuntu upgrades remain pending, including containerd 2.4.2 and Docker 29.9.3 (installed versions: containerd 2.3.2-k3s2, Docker 29.1.3). No reboot or package upgrade was performed.

## Native schedule evidence

| Workflow | Cron (unchanged) | Latest verified native schedule evidence | Result |
|---|---|---|---|
| inspect-vps.yml | 2,32 * * * * | #41881867627 at 00:55:54 ICT | PASS. Genuine event=schedule; inspection PR #1235 merged after exact-head manifest validation #41882047624. Newer #41900544272 at 02:48:43 was workflow_dispatch and is not a native tick. |
| reconcile-vps.yml | 7,22,37,52 * * * * | #41860865532 at 22:44:26 ICT | FAIL in StockDividend health. Later #41900128585 at 02:46:08 was workflow_dispatch and also failed Stock health; it is not a native schedule tick. |
| recover-stale-ops.yml | 10,25,40,55 * * * * | #41852388418 at 21:55:14 ICT | PASS. Later #41900480191 at 02:48:19 was workflow_dispatch, not native schedule evidence. |
| reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | #41861131656 at 22:45:57 ICT | FAIL on stale inspection/recovery evidence. Latest workflow_run watchdog #41900169516 was skipped; no later native watchdog result has been verified. |

TCE native schedule evidence:
- WF-07 #41900042968 at 02:45:37 ICT: SUCCESS. Binance private API check passed; third-party order integration was skipped.
- WF-06 #41880229621 at 00:45:34 ICT: FAIL, all four public endpoint probes returned HTTP 503 instead of HTTP 200.
- WF-12 #41877745265 at 00:27:45 ICT: FAIL on freshness.
- WF-12 workflow_run #41900072829 at 02:45:48 ICT: overall FAIL because WF-06 schedule delivery verification failed; authenticated Platform heartbeat notification job succeeded. It is not a native schedule event.
- No newer native Platform inspect/reconcile/recovery/watchdog run was independently verified at this checkpoint. Preserve all existing cron expressions, especially the TCE market-scan schedule. Do not substitute reruns, manual dispatches, workflow_run, or repository_dispatch for native schedule evidence.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout, and health verification.
- reconcile-vps.yml is the sole production apply authority. inspect-vps.yml is read-only.
- Preserve useful CI, tests, security, backup, manual, release, and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- PR #1238 was merged as 53e7acc8f58f519959c22b0a036140604b210995; inspection #41900544272 was a workflow_dispatch and its exact inspection branch validation #41900666915 passed. This does not establish native schedule recovery.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot, or schedule expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

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
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth service CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75 exact-head validation #40446492086: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/40446492086
- Auth PR #76 exact-head validation #41329425940: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41329425940

## Latest workflow inventory checkpoint

[2026-11-05 02:56 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0256-ict.md) records the #1238 inspection snapshot, current five-repository heads/open PRs, exact workflow event types, current K3s evidence, and remaining release/schedule gates.
