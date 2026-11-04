# Cross-Repo Production Deployment Readiness

**Snapshot:** 2026-11-04 21:58 ICT (14:58 UTC)  
**Platform Infra master:** `74782e9034e41d613e60e8ef72dcdded6d5aa164`

## Current repository state

| Repository | Master SHA | Open PRs | Latest verified master CI / publication |
|---|---|---|---|
| [platform-infra](https://github.com/phanthienquoc/platform-infra) | `74782e9034e4` | #1222 draft; #544/#541/#539 drafts | Manifest validation #41846455387 PASS. Latest action validation #41845802140 is on prior SHA `3671ab1`, not this docs-only head. |
| [TCE-dashboard](https://github.com/phanthienquoc/TCE-dashboard) | `52cecd5584e6` | None | WF-02 #41819221546 and WF-05 #41819221509 PASS on PR SHA `a1afaf1`, not current master. No current-master run returned. |
| [stockdividend](https://github.com/phanthienquoc/stockdividend) | `50ba0dfb67eb` | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. |
| [media-generation](https://github.com/phanthienquoc/media-generation) | `e4c7d8990aaf` | None | Media CI #41617592783 PASS. |
| [phanthienquoc-authentication](https://github.com/phanthienquoc/phanthienquoc-authentication) | `f978a3f378ee` | #75 ready; #76 draft | Auth service CI #41670642852 PASS. |

## Latest Platform schedule and recovery evidence

The current workflow declarations remain:

| Workflow | Cron (UTC) | Latest relevant evidence |
|---|---|---|
| `inspect-vps.yml` | `2,32 * * * *` | Last native scheduled inspection #41809725184 failed; latest successful inspection #41845846869 was workflow_dispatch, not schedule. |
| `reconcile-vps.yml` | `7,22,37,52 * * * *` | Native scheduled reconciliation is stale. Watchdog measured the latest native schedule run at 448 minutes old. |
| `recover-stale-ops.yml` | `10,25,40,55 * * * *` | Native schedule #41852388418 succeeded at 21:55 ICT and dispatched fallback reconciliation. |
| `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | Watchdog #41852468753 failed after the recovery schedule because native reconcile/inspection delivery remained stale. |

Evidence chain:
- [Recovery schedule #41852388418](https://github.com/phanthienquoc/platform-infra/actions/runs/41852388418): native `schedule`, SUCCESS.
- [Fallback reconcile #41852418866](https://github.com/phanthienquoc/platform-infra/actions/runs/41852418866): `workflow_dispatch`, ref `master`, source SHA `74782e9034e41d613e60e8ef72dcdded6d5aa164`, `mode=apply`, `allow_image_changes=false`, `target_app=all`; overall FAILURE only at the StockDividend health lane.
- [Watchdog #41852468753](https://github.com/phanthienquoc/platform-infra/actions/runs/41852468753): FAILURE; latest native inspection #41809725184 was 310 minutes old, and latest native reconciliation was 448 minutes old.
- [Post-reconcile recovery #41852743849](https://github.com/phanthienquoc/platform-infra/actions/runs/41852743849): SUCCESS; inspection fallback was not dispatched because the latest inspection run was still within the 75-minute all-event fallback threshold.
- [Recovery after watchdog #41852517166](https://github.com/phanthienquoc/platform-infra/actions/runs/41852517166): SKIPPED by the first-attempt/source-event guard; the watchdog run itself was a `workflow_run`, not native schedule evidence.

Do not count workflow_dispatch, workflow_run, push or rerun as native schedule delivery. The recovery fallback is functioning, but it does not repair the missing native reconcile/inspection schedule evidence. Preserve all cron declarations.

## K3s and production evidence

Latest read-only snapshot: [inspection #41845846869](https://github.com/phanthienquoc/platform-infra/actions/runs/41845846869), generated 2026-11-04 21:16:14 ICT.

- Node `tce-k3s-01`: Ready, ARM64; K3s `v1.36.3+k3s1`; disk 55%; available memory approximately 19 GiB.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1.
- Stock Admin: two Pods `ImagePullBackOff`; new Stock Backend: `ImagePullBackOff`; old Backend and legacy Frontend: 1/1.
- TCE frontend/service, MicroFE Auth and Keycloak: 0/0 (intentionally stopped in the inspected state).
- Public OIDC probes: HTTP 503.
- GitOps drift: clean.
- Host reports `restart_required=yes`; OS/Docker/containerd maintenance remains pending. No reboot or upgrade performed.

The later reconciliation #41852418866 independently reconfirmed the Stock pull errors:
`admin:12d63b4` and `backend:12d63b4` have no matching ARM64 manifest. Shared preflight succeeded, no manifest drift was found, production apply was correctly skipped, and `allow_image_changes=false`. Auth, TCE, Media and MicroFE lanes passed; Stock health failed; Keycloak was skipped.

## Application release gates

### StockDividend
- App CI and immutable ARM64 publisher passed on master SHA `50ba0dfb67eb`.
- Publisher #41563856933 verified ARM64 publication for Scraper, Admin and Backend; release handoff and paired-digest dispatch remain skipped.
- Production Admin/Backend still reference `12d63b4`, which is not ARM64-compatible.
- Do not promote either image alone. Require protected Actions:read access, validated source-run/tag/digest provenance, and explicit authorization for the paired Admin/Backend promotion.

### TCE Dashboard
- Latest native WF-06 #41810552435 failed all four strict public HTTP 200 checks with HTTP 503.
- Latest native WF-12 #41807645689 failed schedule freshness; WF-07 #41785211971 passed.
- Recent WF-02/WF-05 success is on a prior PR head, not current master.
- Preserve strict health checks and every existing cron, especially the TCE market-scan schedule.

### Media Generation
- Master CI #41617592783 passed.
- Last inspected backend/frontend were 1/1 and digest-pinned.
- No newer publisher E2E or runtime snapshot observed.

### Authentication
- Master service CI #41670642852 passed.
- PR #75 head `a8e8a1d99e86`: Auth service CI #40446492086 passed; keep open because the Supabase GitHub integration may deploy pending migrations on master and the actual integration target/effect is not authoritatively confirmed.
- PR #76 head `f19cacb0bf2b`: Auth service CI #41329425940 passed; remains draft and documentation-only.
- Supabase Preview is skipped. Do not merge, run migrations, or activate Auth/Keycloak until the production integration and migration provenance gates are resolved.

## Ownership and safety contract

- App repositories own tests, builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source provenance and digest verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` is the sole production apply authority. `inspect-vps.yml` is read-only.
- Preserve CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- No second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- PR #1222 remains draft: its current diff still has unresolved shell UID/GID forwarding, Docker/Kubernetes mutation paths outside GitOps, and missing reproducible TypeScript/test/YAML/ShellCheck/lockfile evidence.
- `locally-uncensored-private` remains retired; do not recreate a mirror workflow or credential.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot or TCE market-scan schedule change occurred in this run.

## Next dependency-safe actions

1. Restore native Platform reconcile and inspection schedule delivery; keep watchdog failures visible until native schedule events return.
2. Resolve Stock protected Actions:read access and explicit paired Admin/Backend digest authorization, then promote only through the existing Platform GitOps workflow.
3. Refresh the read-only K3s inspection after the next recovery/reconciliation cycle.
4. Resolve Auth Supabase integration side effects and migration provenance before PR #75/#76 merge or activation.
5. Obtain a maintenance window before host package upgrades/reboot.
