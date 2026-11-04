# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-04 22:59 ICT (15:59 UTC)  
Platform Infra master: `d206e0cc9277ca6b7f707ff3075e13c63ca59961`

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | `d206e0cc9277` | #1222, #544, #541, #539 (all draft) | Read-only inspection #41861306384 PASS; inspection PR #1231 merged as this SHA. Manifest validation #41861440816 PASS on inspection PR head `150d673d`. No current-master workflow-contract validation after the inspection merge; this tracker/validator PR will trigger it. |
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

- **K3s snapshot:** [inspection #41861306384](https://github.com/phanthienquoc/platform-infra/actions/runs/41861306384) succeeded via workflow_dispatch at 22:46:58 ICT; snapshot generated 22:47:09 ICT and merged through [PR #1231](https://github.com/phanthienquoc/platform-infra/pull/1231) as master SHA `d206e0cc9277`. Node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`, disk 55%, available memory about 19 GiB. GitOps drift is clean.
- **StockDividend:** two Admin Pods and the new Backend Pod are `ImagePullBackOff` on `12d63b4`; GHCR reports no matching ARM64 manifest. The older Backend and Frontend remain 1/1. Do not promote either Admin or Backend independently.
- **TCE/Auth:** TCE frontend/service and MicroFE Auth/Keycloak are 0/0 in this snapshot. Public OIDC probes return HTTP 503. WF-06's strict four-endpoint HTTP 200 check failed with HTTP 503; WF-12 schedule freshness also failed. Preserve the strict health gate.
- **Healthy inspected workloads:** Media backend/frontend, MicroFE Shell/WS, and NATS are 1/1. This is point-in-time evidence, not a continuing health guarantee.
- **Host maintenance:** `restart_required=yes`; Ubuntu, Docker and containerd updates are pending. No reboot or upgrade was performed.

## Native schedule evidence

| Workflow | Latest native schedule evidence | Result |
|---|---|---|
| `inspect-vps.yml` (`2,32 * * * *`) | #41809725184 at 16:45 ICT; old workflow SHA `9f74d23` | FAIL. Latest successful inspection #41861306384 at 22:46 ICT was `workflow_dispatch`, not schedule. |
| `reconcile-vps.yml` (`7,22,37,52 * * * *`) | #41860865532 at 22:44 ICT | FAIL only at StockDividend workload health; Auth, TCE, Media and MicroFE lanes passed. |
| `recover-stale-ops.yml` (`10,25,40,55 * * * *`) | #41852388418 at 21:55 ICT | PASS. Later dispatch/workflow_run executions are not native schedule evidence. |
| `reconcile-schedule-watchdog.yml` (`12,27,42,57 * * * *`) | #41861131656 at 22:45 ICT | FAIL: scheduled inspection delivery and recovery-controller freshness checks failed. |

The native watchdog's failures are real schedule-delivery signals. The manual inspection at 22:46 ICT refreshed the snapshot but does not repair native schedule delivery. Preserve all existing cron declarations, including the TCE market-scan schedule.

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
