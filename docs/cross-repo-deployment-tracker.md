# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 00:00 ICT (17:00 UTC)
Platform Infra master at checkpoint: `71bf46709429422def864c1ae5c6948403c562f5`

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | `71bf46709429` | #1222, #544, #541, #539 (all draft) | PR #1232 merged as `71bf4670`; exact-head `lint` #41863805546 and `validate` #41863805484 PASS; post-merge `lint` #41873351411 and `validate` #41873351409 PASS on current master. |
| phanthienquoc/TCE-dashboard | `52cecd5584e6` | None | WF-02 #41819221546 and WF-05 #41819221509 PASS on PR head `a1afaf1c`, not current master. No current-master CI run returned. |
| phanthienquoc/stockdividend | `50ba0dfb67eb` | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Release handoff and paired digest dispatch are SKIPPED. |
| phanthienquoc/media-generation | `e4c7d8990aaf` | None | Media CI #41617592783 PASS. Latest inspection shows backend/frontend 1/1 with digest-pinned imageIDs. |
| phanthienquoc/phanthienquoc-authentication | `f978a3f378ee` | #75 ready; #76 draft | Auth service CI #41670642852 PASS; Supabase Preview SKIPPED. PR #75/#76 remain gated by Supabase integration and migration provenance. |

## Current actions

1. Restore native Platform inspection and reconciliation schedule delivery. Keep watchdog failures visible; workflow_dispatch and workflow_run do not count as native schedule events.
2. Obtain protected Actions:read access and explicit paired Admin/Backend digest authorization before any StockDividend promotion. Promote only through the existing Platform GitOps receiver.
3. Resolve Auth Supabase GitHub integration target/effects and migration provenance before merging #75/#76, running migrations, or activating Auth/Keycloak.
4. Obtain a VPS maintenance window before pending Ubuntu, Docker, and containerd upgrades or reboot.
5. Keep the optional VPS MCP PR #1222 in draft until it removes Docker/Kubernetes mutation authority, proves actual UID/GID isolation, and supplies reproducible build/test/lockfile/security validation.

## Current runtime blockers

- **K3s snapshot:** [read-only inspection #41861306384](https://github.com/phanthienquoc/platform-infra/actions/runs/41861306384) succeeded via `workflow_dispatch` at 22:46:58 ICT; `debug/vps-latest.md` was generated at 22:47:09 ICT and merged by PR #1231. At this 00:00 ICT checkpoint it is about 73 minutes old, close to the 75-minute freshness budget. Node `tce-k3s-01` was Ready, ARM64, K3s `v1.36.3+k3s1`, disk 55%, available memory about 19 GiB; GitOps drift was clean. Treat this as point-in-time evidence, not current health.
- **StockDividend:** latest scheduled reconcile [#41860865532](https://github.com/phanthienquoc/platform-infra/actions/runs/41860865532) failed only in the StockDividend lane. Two Admin Pods and the new Backend Pod are `ImagePullBackOff` on `12d63b4`; containerd reports `no match for platform in manifest`. Old Backend and Frontend were 1/1. Immutable ARM64 publisher #41563856933 succeeded, but the paired handoff and promotion dispatch were skipped. Do not promote either image independently.
- **TCE/Auth:** TCE frontend/service and Auth/Keycloak workloads were 0/0 in the latest inspection. Native WF-06 [#41810552435](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41810552435) failed all four public endpoint jobs; the Auth liveness log confirms HTTP 503 where HTTP 200 is required. WF-12 #41807645689 failed schedule freshness. Preserve strict HTTP 200 checks; do not infer health from a skipped/zero-replica workload.
- **Healthy inspected workloads:** Media backend/frontend, MicroFE Shell/WS, and NATS were 1/1. Media image IDs were digest-pinned. This is only the 22:47 ICT snapshot.
- **Host maintenance:** `restart_required=yes`; Ubuntu, Docker and containerd updates remain pending, including containerd 2.4.2 and Docker 29.9.3 packages. No reboot or upgrade was performed.

## Native schedule evidence

| Workflow | Latest native schedule evidence | Result |
|---|---|---|
| `inspect-vps.yml` (`2,32 * * * *`) | #41809725184 at 16:45 ICT; workflow SHA `9f74d23` | FAIL. Latest successful inspection #41861306384 at 22:46 ICT was `workflow_dispatch`, not schedule. |
| `reconcile-vps.yml` (`7,22,37,52 * * * *`) | #41860865532 at 22:44 ICT | FAIL only at StockDividend workload health; Auth, TCE, Media and MicroFE lanes passed; Keycloak skipped. |
| `recover-stale-ops.yml` (`10,25,40,55 * * * *`) | #41852388418 at 21:55 ICT | PASS. No later native schedule run was returned through 00:00 ICT. |
| `reconcile-schedule-watchdog.yml` (`12,27,42,57 * * * *`) | #41861131656 at 22:45 ICT | FAIL. Its log confirms inspect/recovery workflows were active, but no scheduled inspection was present within 75 minutes (latest native inspect age 360m) and latest native recovery was 50m old. |

The watchdog's failure is a real native schedule-delivery signal, not a health-check false positive. The successful inspection at 22:46 ICT was manually dispatched and does not repair native schedule delivery. The successful recovery #41852388418 was a native schedule run but was already 50 minutes old when watchdog #41861131656 evaluated it. No newer native Platform or TCE schedule events were returned by the Actions API at this checkpoint. Preserve all existing cron declarations, including the TCE market-scan schedule; do not substitute reruns, `workflow_dispatch`, or `workflow_run` events for native schedule evidence.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout, and health verification.
- `reconcile-vps.yml` is the sole production apply authority. `inspect-vps.yml` is read-only.
- Preserve useful CI, tests, security, backup, manual, release, and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, or host reboot occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Platform native reconcile #41860865532: https://github.com/phanthienquoc/platform-infra/actions/runs/41860865532
- Platform native watchdog #41861131656: https://github.com/phanthienquoc/platform-infra/actions/runs/41861131656
- Platform native recovery #41852388418: https://github.com/phanthienquoc/platform-infra/actions/runs/41852388418
- TCE native WF-06 #41810552435: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41810552435
- TCE native WF-12 #41807645689: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41807645689
- TCE native WF-07 #41785211971: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41785211971
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth service CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


## Latest workflow inventory checkpoint

[2026-11-05 00:00 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0000-ict.md) records current repository heads, open PRs, exact-head/post-merge checks, native schedule evidence, latest K3s snapshot age, and the remaining release gates.

- PR #1232 merged as `71bf46709429422def864c1ae5c6948403c562f5`; exact-head checks #41863805546/#41863805484 and post-merge checks #41873351411/#41873351409 all passed.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot, or schedule expression change occurred in this checkpoint.
