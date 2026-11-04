# Cross-repository production deployment readiness

**Updated:** 2026-11-04 21:04 ICT / 14:04 UTC  
**Scope:** `phanthienquoc/platform-infra`, `TCE-dashboard`, `stockdividend`, `media-generation`, `phanthienquoc-authentication`.

This is the current operator-facing readiness summary. Historical evidence and per-workflow details are retained in [the workflow inventory](cross-repo-workflow-inventory.md) and [the timestamped checkpoint](cross-repo-workflow-inventory-checkpoints/2026-11-04-2104-ict.md).

## Ownership and deployment authority

- **Application repositories** own tests, builds, source provenance and immutable GHCR publication.
- **platform-infra** owns production manifests, shared GHCR pull credentials, source-run/tag/digest verification, GitOps promotion, reconciliation, rollout and health verification.
- `.github/workflows/reconcile-vps.yml` is the sole production apply authority. `inspect-vps.yml` is read-only. Recovery and watchdog workflows may inspect and dispatch those existing workflows; they must not apply resources themselves.
- Do not add direct SSH, Docker Compose, Docker restart, or Kubernetes rollout mutation paths outside GitOps.
- Preserve CI, tests, security, backup, manual, release and scheduled jobs. Do not change the TCE market-scan schedule.
- `locally-uncensored-private` remains retired from active platform workflows. Do not restore its mirror or credentials without an explicit owner request.

## Repository readiness

| Repository | Current master | Open PRs | Latest verified CI / publication | Readiness |
|---|---|---|---|---|
| [platform-infra](https://github.com/phanthienquoc/platform-infra) | `8540179260f1` | #1222 draft; #544/#541/#539 drafts | [#41835432534](https://github.com/phanthienquoc/platform-infra/actions/runs/41835432534) `validate-manifests` PASS on current master. [#41821072245](https://github.com/phanthienquoc/platform-infra/actions/runs/41821072245) action validation PASS on prior master `1bb34fb6cddc`, not current head. | Documentation validation is green; current native schedule freshness and production runtime are not green. |
| [TCE-dashboard](https://github.com/phanthienquoc/TCE-dashboard) | `52cecd5584e6` | None | [#41819221546](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41819221546) WF-02 and [#41819221509](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41819221509) WF-05 PASS on PR SHA `a1afaf1cc04e`, not current master. Latest master runs #41819056100/#41819056017 were on `a355ce070204`. | Current-head checks not established; WF-06 public health and WF-12 schedule freshness remain failed. |
| [stockdividend](https://github.com/phanthienquoc/stockdividend) | `50ba0dfb67eb` | None | [#41563856934](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934) CI PASS; [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933) immutable publisher and ARM64 manifest verification PASS. | Release handoff and paired-digest dispatch SKIPPED; production Admin/Backend remain on a tag without ARM64 manifest. |
| [media-generation](https://github.com/phanthienquoc/media-generation) | `e4c7d8990aaf` | None | [#41617592783](https://github.com/phanthienquoc/media-generation/actions/runs/41617592783) Media CI PASS. | Last inspected backend/frontend were 1/1; runtime snapshot is stale and publisher E2E remains gated. |
| [phanthienquoc-authentication](https://github.com/phanthienquoc/phanthienquoc-authentication) | `f978a3f378ee` | #75 ready; #76 draft | [#41670642852](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852) auth-service-ci PASS; Supabase Preview SKIPPED. Web CI #41542942080 is on prior master. | Production activation/merge side-effect review remains gated; no migration or release is authorized by this checkpoint. |

### Open PR gates

- **Platform #1222:** keep draft. It exposes `docker_restart` and `k8s_rollout_restart`, grants Kubernetes `patch`, and its shell child does not receive the declared UID/GID. The installer also does not persist `SHELL_UID`/`SHELL_GID`. Manifest validation alone is not sufficient.
- **Platform #544/#541/#539:** draft Keycloak database/activation/architecture documentation. Required production DB password, endpoint/DNS and architecture decisions remain owner-controlled.
- **Authentication #75:** do not merge solely because application CI passes. The owner-provided Supabase integration is configured to deploy production on `master`; the exact master-push side effect still needs authoritative confirmation.
- **Authentication #76:** migration-drift investigation plan only; do not reset, rewrite or replay migration history.

## Latest read-only K3s evidence

Source: [`debug/vps-latest.md`](../debug/vps-latest.md), generated **2026-11-04 17:21:39 ICT** (10:21:39 UTC). This is the latest available snapshot, not a live health claim.

- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`; root disk 55%, normal pressure.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1 in the snapshot.
- Stock Admin: two Pods `ImagePullBackOff`; new Stock Backend: `ImagePullBackOff`; old Backend and legacy Frontend: 1/1.
- TCE frontend/service and MicroFE Auth/Keycloak: 0/0.
- Public OIDC probes returned HTTP 503.
- Host reports `restart_required: yes`; Ubuntu, Docker and containerd updates are pending. No reboot or package upgrade was performed.

## Native schedule evidence

Native schedule events are distinguished from `workflow_dispatch`, push, `workflow_run`, repository_dispatch and reruns.

- **Platform:** latest native inspection visible in the current Actions history is [#41809725184](https://github.com/phanthienquoc/platform-infra/actions/runs/41809725184), 2026-11-04 16:45 ICT, failed on the older static-branch inspection revision. Previously recorded native reconcile #41792374251 (14:27 ICT) failed at Stock health; watchdog #41792527398 (14:28 ICT) failed on freshness; recovery #41787641688 (13:45 ICT) passed but is stale. No newer native ticks were returned in the current Actions history page.
- **TCE:** [WF-06 #41810552435](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41810552435), 16:53 ICT, failed all four public endpoint checks with HTTP 503 instead of 200. [WF-12 #41807645689](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41807645689), 16:27 ICT, failed schedule freshness. [WF-07 #41785211971](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41785211971), 13:23 ICT, passed.
- No successful push or workflow_run fallback is counted as native cron recovery. Do not weaken strict HTTP 200 or freshness assertions to conceal stopped services or missing schedule delivery.

## Current implementation and next actions

1. A new validation contract is being added on branch `guard/gitops-only-vps-mcp-20261104-2104-ict`. It self-tests that an optional VPS MCP is read-only, has no Docker/Kubernetes/SSH mutation path, forwards child UID/GID and persists the dedicated shell identity. The MCP is absent from master, so the master-side contract is non-mutating; the current draft #1222 should fail this guard until corrected.
2. Obtain a fresh read-only K3s inspection from current master. The available GitHub connection supports run inspection but not `workflow_dispatch`; do not substitute a rerun or old snapshot.
3. Restore native Platform/TCE schedule evidence without changing cron expressions. Verify workflow enablement/delivery through an authorized GitHub Actions control surface.
4. Keep Stock release disabled until the protected Actions:read credential is configured and the owner authorizes one paired Admin/Backend digest promotion. Never promote only one half of the pair.
5. Keep Auth/Supabase migration and production side effects gated; arrange a host maintenance window before package upgrades or reboot.

**No production manifest, image reference, shared GHCR credential, database, Pod, replica or host was changed in this checkpoint.**
