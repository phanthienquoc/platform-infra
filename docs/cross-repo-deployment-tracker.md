# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 05:02 ICT (2026-11-04 22:02 UTC)
Platform Infra master at checkpoint: fe243a7ecc652a720a813f93e669474bb858c848

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | fe243a7ecc652a720a813f93e669474bb858c848 | #1222, #544, #541, #539 (all draft) | PR #1242 merged; exact-head #41923196096/#41923196112 and post-merge #41923323345/#41923323244 all PASS. Current master validation is green on fe243a7. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d | None | Native WF-07 #41900042968 PASS at 02:45 ICT. Native WF-06 #41880229621 FAIL (all four public endpoints HTTP 503). Native WF-12 #41877745265 FAIL (freshness); workflow_run #41900072829 FAIL on delivery verification although authenticated Platform heartbeat notification passed. |
| phanthienquoc/stockdividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Scraper/Admin/Backend full-source-SHA images resolve to linux/arm64 digests. Production GitOps promotion is explicitly disabled by publisher gate; handoff validation and paired digest dispatch are SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None | Media CI #41617592783 PASS. Latest runtime snapshot #1241 shows backend/frontend 1/1 with digest-pinned imageIDs. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft | Auth service CI #41670642852 PASS; Supabase Preview SKIPPED. PR #75 exact head a8e8a1d99e86 validation #40446492086 PASS; PR #76 exact head f19cacb0bf2b validation #41329425940 PASS. Production integration/migration gate remains closed. |

## Current actions

1. PR #1242 merged the inspection recovery event-classification fix. Watchdog #41918315745 correctly failed because native event=schedule inspection #41881867627 was 224 minutes old. Recovery #41918357799 had incorrectly treated manual inspection #41914913277 as native activity. The merged controller now queries native event=schedule and workflow_dispatch fallback runs separately, suppresses duplicate read-only fallbacks, and never treats manual fallback as native schedule evidence. Exact-head validation #41923196096/#41923196112 and post-merge validation #41923323345/#41923323244 all PASS. No native schedule run after the merge has yet been observed.
2. Restore and verify native Platform schedule delivery independently for inspect-vps, reconcile-vps, recover-stale-ops, and reconcile-schedule-watchdog. Do not count workflow_dispatch, workflow_run, repository_dispatch, or reruns as native schedule evidence.
3. Keep StockDividend production promotion disabled. The publisher explicitly logged that promotion is disabled; handoff validation and paired digest dispatch were skipped. Do not enable promotion without explicit release authorization. Preserve atomic Admin/Backend pairing.
4. Resolve TCE service availability while preserving strict HTTP 200 endpoint assertions. Current TCE frontend/service and Auth/Keycloak desired replicas are 0/0 in the latest snapshot; heartbeat forwarding is not service health.
5. Resolve Auth Supabase integration target/effects and migration provenance before merging #75/#76, running migrations, or activating Auth/Keycloak.
6. Obtain a VPS maintenance window before pending Ubuntu, Docker, and containerd upgrades or reboot.
7. Keep optional VPS MCP PR #1222 in draft. Its current head f018e39eda52 still exposes Docker restart and Kubernetes Deployment patch/restart capabilities, contains literal backslash-n source/installer defects, and declares but does not pass SHELL_UID/GID to child-process execution. Build/tests, YAML validation, ShellCheck and committed lockfile remain absent.

## Current runtime blockers

- **K3s snapshot:** Read-only inspection run #41914913277 was a workflow_dispatch fallback at 04:18 ICT; snapshot debug/vps-latest.md was generated at 2026-11-04 21:19:01 UTC (04:19:01 ICT) and merged by inspection PR #1241 as master SHA 58cb64461beaf70f96fac0a3e4f5559b9efdb0b3. At 05:02 ICT it is about 43 minutes old. This is point-in-time evidence, not continuous health. Node tce-k3s-01 was Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, available memory about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Two Stock Admin Pods and the new Stock Backend Pod were ImagePullBackOff; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0.
- **StockDividend:** Production Admin and new Backend still reference tag 12d63b4, which has no ARM64 manifest (no match for platform in manifest). The latest successful publisher #41563856933 verified these immutable linux/arm64 digests for source SHA 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec:
  - Scraper: sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2
  - Admin: sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e
  - Backend: sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a
  The publisher's Gate production GitOps promotion job explicitly enforces the disabled release hold. Handoff validation and paired digest dispatch were SKIPPED. No production promotion is authorized by this evidence.
- **TCE/Auth/Keycloak:** TCE frontend/service and MicroFE Auth/Keycloak are 0/0 in snapshot #1241. Native WF-06 #41880229621 failed all four strict public endpoint checks (TCE web, TCE API, Auth liveness, Auth readiness returned HTTP 503). Native WF-12 #41877745265 failed freshness; later workflow_run #41900072829 failed WF-06 delivery verification while the authenticated Platform heartbeat notification job succeeded.
- **Media/MicroFE:** Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 in snapshot #1241; Media imageIDs are digest-pinned. No newer Media CI/publisher run was observed after #41617592783.
- **Host maintenance:** restart_required: yes; Ubuntu upgrades remain pending, including containerd 2.4.2 and Docker 29.9.3 (installed versions: containerd 2.3.2-k3s2, Docker 29.1.3). No reboot or package upgrade was performed.

## Native schedule evidence

| Workflow | Cron (unchanged) | Latest verified native schedule evidence | Result |
|---|---|---|---|
| inspect-vps.yml | 2,32 * * * * | #41881867627 at 00:55:54 ICT | PASS, but stale. Later inspection #41914913277 at 04:18 ICT was workflow_dispatch and does not satisfy native schedule freshness. |
| reconcile-vps.yml | 7,22,37,52 * * * * | #41917440202 at 04:35:01 ICT | FAIL in StockDividend health lane. |
| recover-stale-ops.yml | 10,25,40,55 * * * * | #41914511298 at 04:16:19 ICT | PASS. Later #41918357799 at 04:41 ICT was workflow_run, not native schedule evidence. |
| reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | #41918315745 at 04:40:44 ICT | FAIL: no native inspect-vps run within the 75-minute budget. The failed step explicitly reported latest native inspect #41881867627 age 224 minutes. |

The recovery run #41918357799 succeeded but did not dispatch a fallback because it treated recent workflow_dispatch inspection #41914913277 as if it were native schedule activity. PR #1242 fixes this event-classification defect. The post-merge push validations are not native schedule evidence; a later event=schedule recovery/inspection cycle is still required to verify the behavior in production. A successful manual fallback refreshes the snapshot but must not turn the native schedule watchdog green.

TCE native schedule evidence:
- WF-07 #41900042968 at 02:45:37 ICT: SUCCESS; Binance private API check passed; third-party order integration skipped.
- WF-06 #41880229621 at 00:45:34 ICT: FAIL; all four public endpoint probes returned HTTP 503 instead of HTTP 200.
- WF-12 #41877745265 at 00:27:45 ICT: FAIL on freshness.
- WF-12 workflow_run #41900072829 at 02:45:48 ICT: overall FAIL because WF-06 delivery verification failed; authenticated Platform heartbeat notification job succeeded. It is not a native schedule event.
- No newer native TCE schedule event was present in the latest 20-run history through 05:02 ICT. Preserve all cron expressions, especially the TCE market-scan schedule.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout, and health verification.
- reconcile-vps.yml is the sole production apply authority. inspect-vps.yml is read-only.
- Preserve useful CI, tests, security, backup, manual, release, and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot, or schedule expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Recovery event-classification fix PR #1242: https://github.com/phanthienquoc/platform-infra/pull/1242
- PR #1242 exact-head validate-github-actions #41923196096: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196096
- PR #1242 exact-head validate-manifests #41923196112: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196112
- PR #1242 post-merge validate-github-actions #41923323345: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323345
- PR #1242 post-merge validate-manifests #41923323244: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323244
- Platform latest native reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Platform native watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- Platform watchdog-triggered recovery #41918357799: https://github.com/phanthienquoc/platform-infra/actions/runs/41918357799
- Platform latest native recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- Platform latest native inspection #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- Platform manual inspection fallback #41914913277: https://github.com/phanthienquoc/platform-infra/actions/runs/41914913277
- Platform inspection snapshot PR #1241: https://github.com/phanthienquoc/platform-infra/pull/1241
- TCE native WF-07 #41900042968: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE native WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE native WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- TCE heartbeat/delivery verification #41900072829: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900072829
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth service CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75 exact-head validation #40446492086: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/40446492086
- Auth PR #76 exact-head validation #41329425940: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41329425940
- Platform MCP PR #1222: https://github.com/phanthienquoc/platform-infra/pull/1222

## Latest workflow inventory checkpoint

[2026-11-05 05:14 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0514-ict.md) records the current five-repository heads/open PRs, PR #1242 merge evidence, native schedule evidence, Stock promotion hold, current K3s snapshot, and remaining runtime blockers.
