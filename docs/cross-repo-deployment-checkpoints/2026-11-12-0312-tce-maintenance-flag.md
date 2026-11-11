# TCE Maintenance Flag Evidence — 2026-11-12 03:12 ICT

Reference: 2026-11-11T20:11:03Z. Platform master at checkpoint start: `99509adbffb3888ac5bee59042c28292e5010919`.

## New finding from WF-13 logs

- TCE WF-13 run #43088861304 completed SUCCESS on a `workflow_run` event sourced from failed WF-12 #43088836266.
- Job #130760312074 is named “Dispatch read-only WF-06 fallback for a verified stale schedule”.
- Its log records the environment line `TCE_MAINTENANCE_MODE:` with an empty value.
- Current master `.github/workflows/wf-13-tce-healthcheck-recovery.yml` maps `""|false|0|no` to `enabled=false`; only `true|1|yes` enables maintenance suppression.
- Therefore maintenance suppression was **not enabled in that WF-13 run**. The job continued source validation and dispatched manual/read-only WF-06 fallback #43088897948 on exact TCE master SHA `5b425bdeab457e943bcecf1831836fc698e24394`.
- Fallback #43088897948 then returned HTTP 503 for TCE web, TCE API, Auth liveness and Auth readiness (expected 200).
- The current repository variable value after that run is not readable through this integration. No Actions variable was changed.

TCE administrator must set `TCE_MAINTENANCE_MODE=true` only if the 0/0 maintenance window is approved; otherwise restore service replicas and keep the variable false. WF-06 HTTP-200 and WF-12 native schedule checks remain strict.

## Current schedule evidence — 20:11:03Z

| Lane | Latest native | Previous | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #43066718643 | #42993779924 | 10,411 | 28,867 | 2,700 |
| Platform inspection | #43054529460 | #42981286761 | 14,838 | 30,159 | 4,500 |
| Platform recovery | #43058316157 | #42986496462 | 13,488 | 29,036 | 2,700 |
| Platform watchdog | #43058640134 | #42986833403 | 13,367 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 7,937 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 9,918 | 28,287 | 1,500 |

All six current-age and all six inter-arrival budgets fail. WF-07 #43088811861 is integration-only. WF-13 #43088861304 is workflow_run and does not satisfy native cadence.

## Platform / K3s evidence

- Latest successful reconciliation #43088879697 (19:37:08Z) ran `mode=apply`, target=all, image changes=false on parent SHA `9093831c`. At 20:11:03Z age=2,035s, with 665s remaining in the 2,700s budget. It verified five GHCR packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, found no blocked image pulls in MicroFE/TCE scopes, confirmed TCE release pairing, and reported drift=false; manifest apply/image replacement/rollout skipped.
- Full inspection #43089176130 snapshot generated 19:39:15Z. At 20:11:03Z age=1,908s, with 2,592s remaining in the 4,500s budget.
- K3s last-known: node Ready/ARM64; Media backend/frontend 1/1; MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin two pods and desired Backend one pod ImagePullBackOff for `12d63b4`; Keycloak OIDC probes 503; preserve the separate `k3s-debug` PVC. Host restart required; no reboot.
- Current master advanced to `99509adb` via docs-only PR #1652; no production manifest changes.

## Exact next actions

1. Platform operator: current-master `reconcile-vps.yml` `mode=plan` on `99509adb` before the last reconciliation freshness expires at 20:22:08Z; obtain fresh inspection before 20:54:15Z.
2. TCE administrator: verify the current repository variable setting and set it to true only if the maintenance window is approved; otherwise restore service replicas. Do not relax strict health probes.
3. GitHub administrator: scheduler enqueue/delivery telemetry and master protection/squash-only remediation.
4. Stock owner: retirement/restoration decision; if restored, publish a compatible ARM64 immutable digest.
5. Media owner: backup/retention, DNS and remote runner unregister evidence.

No current-master workflow dispatch, new image publication/promotion, manifest apply, rollout, deletion, credential rotation, DNS/database/storage mutation, cleanup or reboot occurred. Platform Infra remains the only production apply authority. TCE market-scan schedule unchanged.
