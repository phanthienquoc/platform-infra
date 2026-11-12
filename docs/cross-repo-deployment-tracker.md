## Post-merge receipt — 2026-11-12 15:10 ICT

Platform PR #1678 was squash-merged at 184c75e7ac5491ce386ff8d3a886a2ba4dcc434c. Exact-head validate-manifests #43180530521 completed SUCCESS on 434f9549dd9a1a40a3691be96ecde1be9e842764; all 20 applicable validation steps passed. Post-merge validate-manifests #43180598767 then completed SUCCESS on the exact current master SHA 184c75e7ac5491ce386ff8d3a886a2ba4dcc434c; all 20 applicable steps passed, with changed-image validation correctly skipped for documentation-only changes.

PR #1678 changed only the deployment readiness tracker, workflow inventory and two checkpoint files. No production manifest, workflow definition, credential, runtime configuration, workload, DNS, storage or schedule changed. Current Platform master is 184c75e7ac5491ce386ff8d3a886a2ba4dcc434c; TCE 34f6024f8ccec8fb3ab6688901b3557e058ddfd1, Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61, Media dcd698699c65ba6e73f6b43838975144777131c3 and Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f remain unchanged.

The 15:02 ICT snapshot and 15:07 receipt remain accurate for the unchanged production manifest tree. Current runtime evidence remains the inspection/reconciliation receipts recorded there; no new production mutation occurred. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

## Post-merge receipt — 2026-11-12 15:07 ICT

Platform PR #1677 was squash-merged at f4b03f3153daf4feb5521d0098a9bc81fe56dd1b. Exact-head validate-manifests #43180328807 completed SUCCESS on 80ff0fd7d5475a30a033cba596ace332b19e2a25; all 20 applicable validation steps passed.

PR #1677 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint files. No production manifest, workflow definition, credential, runtime configuration, workload, DNS, storage or schedule changed. The current Platform master is f4b03f3153daf4feb5521d0098a9bc81fe56dd1b; TCE 34f6024f8ccec8fb3ab6688901b3557e058ddfd1, Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61, Media dcd698699c65ba6e73f6b43838975144777131c3 and Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f remain unchanged.

The 15:02 ICT snapshot below is an accurate pre-merge evidence snapshot. PR #1677 was documentation-only, so the referenced current-master reconciliation and K3s evidence remain applicable to the unchanged production manifest tree. No post-merge workflow run on the new merge SHA was present in the queried Actions history at this receipt. Do not represent PR validation as a post-merge runtime check.

No production mutation occurred as part of PR #1677. The referenced reconciliation #43176619995 separately provisioned/verified the Auth runtime Secret (values suppressed); shared ghcr-pull remained unchanged. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

## Current verified snapshot — 2026-11-12 15:02 ICT / 08:02:05 UTC

This refresh independently re-read all five master refs, open PRs, latest Actions runs, workflow-specific native schedule histories, the deployment tracker and workflow inventory, inspection PR #1676, current-master reconciliation #43176619995, and the TCE-to-Platform heartbeat correlation. Only first-attempt event=schedule runs on master count as native schedule delivery; workflow_dispatch, workflow_run and repository_dispatch are recorded separately.

### Repository refs, open PRs and latest workflow evidence

| Repository | Verified master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | 345f033a37b2ab944614bd688a58bc5c60d01764 | #1314/#544/#541/#539 (owner-decision drafts) | Inspection #43173781408 SUCCESS; its PR #1676 exact-head validation #43173998401 PASS and squash merge produced this master. Current-master reconciliation #43176619995 SUCCESS via workflow_dispatch; recovery #43176810214 SUCCESS. Latest native reconcile remains #43152960974 and is stale. |
| TCE Dashboard | 34f6024f8ccec8fb3ab6688901b3557e058ddfd1 | none | Native WF-06 #43176560763 at 07:36:52Z FAIL (four public probes HTTP 503). WF-12 #43176586474 is workflow_run, not native schedule; its schedule-verification and authenticated heartbeat jobs PASS. WF-13 #43176586309 SUCCESS. Latest native WF-12 remains #43154415980 and is stale. |
| StockDividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 PASS. Weekend scraper #42457182511 FAIL CLOSED because protected VNSTOCK_API_KEY is missing. No new current-master publication or promotion. |
| Media Generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 PASS. No newer current-master publication or Platform promotion evidenced. |
| Authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (owner-decision draft) | CI #42654579277 PASS. No newer current-master release or promotion evidenced. |

Platform PRs #1314/#544/#541/#539 and Authentication PR #76 remain owner-decision items. None was changed or merged in this refresh. TCE, Stock and Media have no open PRs.

### Native schedule evidence — reference 08:02:05Z

| Lane | Latest qualifying native run | Age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #43152960974 | 13,937 | 16,665 | 2,700 |
| Platform inspection | #43150245172 | 15,431 | 17,233 | 4,500 |
| Platform recovery | #43150505792 | 15,290 | 17,135 | 2,700 |
| Platform watchdog | #43150601305 | 15,236 | 17,077 | 2,700 |
| TCE WF-06 | #43176560763 | 1,513 | 25,693 | 1,500 |
| TCE WF-12 | #43154415980 | 13,152 | 16,987 | 1,500 |

All six current-age budgets and all six inter-arrival budgets fail at this reference. TCE WF-06 has resumed one native event after a 25,693s (7h 8m 13s) gap, but that run failed its health probes and was already 13s beyond the 1,500s age budget at the reference. TCE WF-12 #43176586474 is a workflow_run triggered by WF-06; it is not a native schedule run and does not reset WF-12 cadence.

Platform recovery dispatches succeeded, but they do not reset Platform native schedule cadence. No authoritative GitHub scheduler enqueue/delivery telemetry was available to distinguish delayed from dropped events. Platform watchdog/queue checks and TCE's measured 0m queue wait do not establish runner congestion. Keep all existing cron expressions and budgets; do not add a duplicate scheduler or alter the TCE market-scan schedule.

### Verified cross-repo heartbeat and GitOps reconciliation

TCE WF-06 #43176560763 ran with event=schedule, attempt 1 and master SHA 34f6024f8ccec8fb3ab6688901b3557e058ddfd1. It failed all four strict public probes:
- TCE web: HTTP 503 (expected 200).
- TCE API: HTTP 503 (expected 200).
- Auth liveness: HTTP 503 (expected 200).
- Auth readiness: HTTP 503 (expected 200).

TCE WF-12 #43176586474 verified the WF-06 workflow was enabled, inspected the scheduled source run, and dispatched the authenticated heartbeat. Platform recovery #43176601065 validated the exact source repository, event, workflow path, source run ID/attempt/SHA and heartbeat run ID/attempt/SHA; it confirmed the watchdog was active and successfully dispatched the existing GitOps authority. The exact correlated dispatch was ref=master, SHA 345f033a37b2ab944614bd688a58bc5c60d01764, mode=apply, target_app=all. This is verified dispatch-payload/correlation evidence, not a native Platform schedule delivery.

Current-master reconciliation #43176619995 completed SUCCESS at 07:37:21Z on SHA 345f033a37b2ab944614bd688a58bc5c60d01764. At 08:02:05Z its age was 1,484s, within the 2,700s runtime freshness budget. Inputs were mode=apply, target_app=all, allow_image_changes=false. Results:
- GHCR read-access preflight passed for all five currently referenced packages.
- Auth runtime Secret was provisioned and verified in microfe-platform; all required keys were present and values were suppressed.
- Shared ghcr-pull Secret was unchanged; deployment patches for microfe-auth and TCE frontend/service reported no change.
- TCE release pairing passed; desired and live frontend/service tags matched prod-v0.1.0-e75e338.
- GitOps drift=false; manifest apply, image replacement and rollout were skipped.
- Blocked-image-pull inspection found no failures for MicroFE Auth/Shell/WS or TCE service/frontend. Stock workloads are not part of that restart allowlist and remain blocked separately.
- MicroFE active-scope health passed. Auth service and TCE dashboard were explicitly identified as intentional zero-replica maintenance scopes; no live workload health is asserted. Keycloak was skipped.
- Post-reconcile node/pod inventory completed successfully. No image publication or digest promotion occurred.

Recovery #43176810214 completed SUCCESS after reconciliation. It found the current reconciliation recent and avoided a duplicate dispatch; it also found read-only inspection fallback #43173781408 fresh and avoided a duplicate inspection dispatch. The controller explicitly retained the native-schedule stale warning.

### K3s and host evidence

Read-only inspection #43173781408 completed SUCCESS at 07:14:22Z. It created PR #1676 from branch automation/vps-inspection-43173781408-1; exact head 4d183921c49b2ad1b49ecf08a498b46734004c2e passed validate-manifests #43173998401 and was squash-merged at 07:16:31Z to merge SHA 345f033a37b2ab944614bd688a58bc5c60d01764. Snapshot debug/vps-latest.md was generated at 07:14:30Z; age at this reference was 2,855s, within the 4,500s inspection budget. The reconciliation run independently captured cluster state at 07:37:43Z.

- Node tce-k3s-01 was Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Root disk 57% used with about 20GiB free; available RAM about 19GiB; restart_required=yes.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running. Media backend/frontend had RepoDigests sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d and sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a.
- TCE frontend/service, MicroFE Auth and Keycloak were 0/0 maintenance. Do not infer live availability.
- Stock Admin had two failed pods on desired tag 12d63b4; desired Stock Backend had one ImagePullBackOff pod while a legacy backend pod remained 1/1; legacy frontend remained 1/1. The desired admin/backend tag failed with no match for platform in manifest and had no usable RepoDigest. Do not promote local image IDs or legacy tags.
- Media runner service was active/enabled and Runner.Listener was present; Platform runner service/Listener was also active.
- Stock and Media namespaces had no PVC/PV claims or VolumeSnapshot references in the inspection preflight. Preserve PVC k3s-debug/k3s-debug-logs (Bound, 1Gi, RWO).
- Host package/kernel/containerd/Docker updates remain pending. No host restart or Docker cleanup was performed.

### Ownership, blockers and exact next actions

- App repositories own tests/builds, immutable GHCR publication, SBOM/provenance and exact dispatch payloads. Platform Infra remains the sole owner of production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, K3s rollout and health verification.
- TCE/Auth remain intentional zero-replica maintenance scopes in the current cluster inventory. TCE administrator must verify TCE_MAINTENANCE_MODE and approved replica intent; retain strict HTTP-200 probes. Do not scale workloads without approval.
- Stock desired ARM64 image provenance remains unresolved; Stock owner must supply a compatible immutable digest or approve retirement. If scraper remains required, configure VNSTOCK_API_KEY only as a protected Actions secret.
- Media runner retirement remains blocked by owner-backed stop/disable, Listener absence, GitHub-side unregister, external backup/retention, authoritative DNS and protected production approval.
- Effective organization rulesets/branch protection remain an administrator task; prior repository-level reads showed all five master branches unprotected, while branch-protection detail endpoints were denied to the integration. Verify PR-only, required checks, no force-push/deletion and squash-only.
- No workflow was proven redundant/obsolete; preserve CI, tests, security, backup, manual, release and scheduled jobs. No duplicate direct SSH/Compose production authority was introduced.
- Exact next actions: obtain fresh inspection/current-master plan as cadence allows; escalate authoritative GitHub schedule-delivery telemetry; have TCE admin verify maintenance/replica intent; have Stock owner resolve ARM64 image provenance and protected scraper secret; have Media owner complete runner/backup/DNS gates; have GitHub admin enforce branch governance; obtain explicit approval before host restart.

No production manifest apply, image promotion, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. The only production-side secret action in reconciliation #43176619995 was provisioning/verifying the Auth runtime Secret; shared ghcr-pull remained unchanged. TCE market-scan schedule and all checked-in cron expressions remain unchanged.

Last reviewed: 2026-11-12 15:02 ICT (2026-11-12 08:02:05 UTC).

## Post-merge receipt — 2026-11-12 14:00 ICT / 07:00:17 UTC

Platform PR #1674 was squash-merged at `7ddaf5cd7f5735673c2fb052859fca61da786d0e`. Exact-head `validate-manifests` #43171924642 completed SUCCESS on `3a2db3628270e4bf1bbb701d608e1ed007a12ead`; post-merge `validate-manifests` #43172008740 completed SUCCESS on the exact merge SHA with 20 successful validation steps and no failures.

PR #1674 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint files. No production manifest, workflow, secret, credential, runtime configuration, schedule or workload changed. Current Platform master is `7ddaf5cd7f5735673c2fb052859fca61da786d0e`; TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3` and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f` remain unchanged.

The 13:56 ICT snapshot remains an accurate pre-merge evidence snapshot. At 07:00:17Z, no new qualifying native schedule run superseded the 13:56 IDs. Current ages increased by 211s: reconcile 10,229s; inspection 11,723s; recovery 11,582s; watchdog 11,528s; TCE WF-06 23,498s; TCE WF-12 9,444s. Inter-arrival gaps remain 16,665s / 17,233s / 17,135s / 17,077s / 23,393s / 16,987s. All six current-age and all six inter-arrival budgets still fail. TCE market-scan schedule and all checked-in cron expressions remain unchanged.

Reconciliation #43152960974 is 10,229s old vs 2,700s budget. K3s inspection #43150245172 is 11,723s old vs 4,500s budget. Both are stale; historical no-drift and workload details are not current runtime receipts. No new current-master plan, inspection, rollout or health verification was observed.

Fresh branch governance reads: `GET /branches/master` returned `protected=false` on all five repositories. Repository rulesets returned empty lists for Platform, TCE, Media and Authentication; Stock rulesets GET returned HTTP 403 because the private repository plan does not expose that endpoint. Branch-protection detail GET returned HTTP 403 `Resource not accessible by integration` on all five, so detailed required-check/review configuration remains unreadable. Do not infer organization-level policy from these repository-level reads.

No production mutation occurred. Platform Infra remains the sole production apply authority. TCE market-scan schedule remains unchanged.

## Current verified snapshot — 2026-11-12 13:56 ICT / 06:56:46 UTC

This refresh independently re-reads all five master refs, open PRs, latest Actions runs, current tracker/inventory, Platform/TCE schedule workflow definitions, and selected failure logs. Runtime evidence is age-gated; no current K3s state is inferred from expired inspection data.

### Repository refs, open PRs, latest workflows

| Repository | Verified master SHA | Open PRs | Latest relevant workflow evidence |
|---|---|---|---|
| Platform Infra | `c1257c3801bb079467e3442ee768b684214645c6` | #1314/#544/#541/#539 (owner-decision drafts) | Current-master validate-manifests #43165632162 PASS on exact SHA. Latest native reconciliation #43152960974 SUCCESS at 04:09:48Z, but stale. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-12 native schedule #43154415980 FAIL at 04:22:53Z; WF-13 #43154436821 SUCCESS; read-only WF-06 fallback #43154458775 FAIL with four HTTP 503 responses. WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 PASS. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS. Weekend scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. No newer current-master publication or Platform promotion appears in the latest 100 Actions runs. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | CI #42654579277 PASS. No newer current-master release/promotion appears in the latest 100 Actions runs. |

The five default branches are `master`. Platform PRs #1314/#544/#541/#539 and Authentication PR #76 remain owner-decision drafts; none was modified or merged. TCE, Stock and Media have no open PRs.

Platform PR #1673 post-merge validation #43165632162 completed SUCCESS on exact current master `c1257c3801bb079467e3442ee768b684214645c6`. The latest Platform changes in this range are documentation/checkpoint-only; no production manifest, workflow definition, secret, credential, runtime configuration or schedule was changed.

### Native schedule evidence — reference 06:56:46Z

Only first-attempt `event=schedule` runs on `master` count. Manual dispatch, workflow_run, repository_dispatch, push and reruns do not reset native cadence.

| Lane | Latest qualifying native run | Created (UTC) | Age (s) | Previous inter-arrival gap (s) | Budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile-vps.yml | #43152960974 | 04:09:48 | 10,018 | 16,665 | 2,700 |
| Platform inspect-vps.yml | #43150245172 | 03:44:54 | 11,512 | 17,233 | 4,500 |
| Platform recover-stale-ops.yml | #43150505792 | 03:47:15 | 11,371 | 17,135 | 2,700 |
| Platform reconcile-schedule-watchdog.yml | #43150601305 | 03:48:09 | 11,317 | 17,077 | 2,700 |
| TCE WF-06 | #43127554403 | 00:28:39 | 23,287 | 23,393 | 1,500 |
| TCE WF-12 | #43154415980 | 04:22:53 | 9,233 | 16,987 | 1,500 |

All six current-age budgets and all six inter-arrival budgets fail at this reference.

Checked-in cron expressions remain:
- Platform reconcile: `7,22,37,52 * * * *`.
- Platform inspection: `2,32 * * * *`.
- Platform watchdog: `12,27,42,57 * * * *`.
- Platform recovery: `10,25,40,55 * * * *`.
- TCE WF-06: `*/15 * * * *`.
- TCE WF-12: `7,22,37,52 * * * *`.

Platform watchdog #43150601305's queue-assignment checks passed while native schedule freshness/inter-arrival checks failed. TCE WF-12 #43154415980 measured 0m queue wait for its stale WF-06 source. This does not establish runner congestion. No authoritative GitHub scheduler enqueue/delivery/support telemetry was available to distinguish delayed from dropped events. Keep the existing cron expressions and freshness budgets; do not introduce a duplicate scheduler or change the TCE market-scan schedule.

TCE WF-12's heartbeat dispatch to Platform succeeded, but its separate schedule-verification job failed because WF-06 was 234 minutes old at the watchdog's own API timestamp. WF-13 then dispatched read-only fallback #43154458775. Job logs confirm:
- `https://tce.mrcute.space/`: HTTP 503, expected 200.
- `https://tce.mrcute.space/api/health`: HTTP 503, expected 200.
- `https://auth.mrcute.space/api/health`: HTTP 503, expected 200.
- `https://auth.mrcute.space/api/ready`: HTTP 503, expected 200.

WF-06 still has strict HTTP-200 checks. These failures indicate endpoint unavailability, not a schedule delivery pass. WF-13's explicit maintenance handling does not make health green.

### GitOps and K3s evidence freshness

Latest successful native reconciliation #43152960974 completed at 04:09:48Z on parent Platform SHA `9f969fcfe0a8b31c5b612e218ea9f5a86e629059`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`. At 06:56:46Z it is 10,018s old, beyond the 2,700s freshness budget.

Historical reconciliation results:
- Five GHCR package read preflights passed (Auth service, MicroFE Shell/WS, TCE service/web).
- Auth runtime Secret was provisioned/verified; secret values were suppressed.
- Shared `ghcr-pull` was unchanged.
- TCE release pairing passed.
- GitOps drift was false; manifest apply, image replacement and workload rollout were skipped.
- MicroFE active-scope health passed. TCE/Auth were in maintenance/zero-replica state, not live application availability. Keycloak was skipped.
- No new GHCR publication or digest promotion was evidenced.

Full K3s inspection #43150245172 was created at 03:44:54Z (snapshot file timestamp 03:45:02Z). At 06:56:46Z it is 11,512s old, beyond the 4,500s freshness budget. All workload information from it is historical only:
- Node `tce-k3s-01`: last observed Ready, ARM64; Ubuntu 22.04.5; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Root disk last observed 57% used (~20GiB free); available RAM ~19GiB; host `restart_required=yes`.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running.
- TCE frontend/service, MicroFE Auth and Keycloak were 0/0 maintenance; do not infer live availability.
- Stock Admin had two ImagePullBackOff pods on desired tag `12d63b4`; desired Stock Backend had one ImagePullBackOff pod. The desired tag lacked compatible ARM64 manifest/RepoDigest evidence. Do not promote local image IDs or legacy tags.
- Media runner service was active/enabled and `Runner.Listener` was present.
- Preserve PVC `k3s-debug/k3s-debug-logs` (Bound, 1Gi, RWO).
- Docker cleanup was not performed; prior reclaimable-space estimate is stale and must not be acted upon.

No fresh same-run K3s inspection, current-master reconciliation plan, rollout or health receipt was available at this reference. No production mutation occurred.

### Ownership, blockers and next actions

- App repositories own tests/builds, immutable GHCR publication, SBOM/provenance and exact dispatch payloads. Platform Infra alone owns production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, K3s rollout and health.
- TCE's WF-13 warns when `TCE_MAINTENANCE_MODE` is unset and retains strict WF-06 HTTP-200 probes. The current Actions variable value is not readable through this connection. TCE administrator must verify it and either explicitly enable approved zero-replica maintenance or restore replicas under an approved change.
- Stock scraper remains fail-closed without protected `VNSTOCK_API_KEY`; do not bypass preflight or place secrets in Git/logs. Stock desired ARM64 image provenance remains unresolved.
- Media runner retirement remains blocked by missing owner-backed stop/disable, Listener absence, GitHub-side unregister, external backup/retention, authoritative DNS and protected approval evidence.
- All five master branches were previously observed as unprotected; this run did not re-read branch-protection endpoints. GitHub administrator must verify effective organization rulesets and enforce PR-only, required checks, block force-push/deletion and squash-only.
- No workflow was proven redundant/obsolete; preserve useful CI, security, backup, manual, release and scheduled workflows.
- Do not add duplicate direct SSH/Compose production deployment authority.
- TCE market-scan schedule is unchanged.

Exact next actions: (1) Platform operator obtains fresh read-only `inspect-vps.yml` and current-master `reconcile-vps.yml` `mode=plan`; (2) GitHub administrator obtains authoritative schedule enqueue/delivery telemetry; (3) TCE administrator verifies maintenance variable and approved replica intent; (4) Stock owner supplies ARM64-compatible immutable digest or retirement decision and protected scraper secret if the scraper remains required; (5) Media owner completes runner/backup/DNS evidence before protected decommission; (6) GitHub administrator enforces branch governance.

Last reviewed: 2026-11-12 13:03 ICT (2026-11-12 06:03:32 UTC).


## Post-merge receipt — 2026-11-12 13:03:32 ICT / 06:03:32 UTC

Platform PR #1672 was squash-merged at `856c37b3342cdd564aaf6e1e3f2996a51832e55e`. Exact-head validate-manifests #43165357610 completed SUCCESS on `d0971a2cdb82f867a143676110e429aa71b0a78e`; post-merge validate-manifests #43165429654 completed SUCCESS on the exact merge SHA. All 20 applicable validation steps passed.

The PR changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint files. No production manifest, workflow, secret, credential, runtime configuration or schedule changed. Current Platform master is `856c37b3`; TCE `34f6024f`, Stock `b1b5e177`, Media `dcd69869` and Authentication `eab85fab` remain unchanged.

The 12:59 ICT snapshot above remains an accurate pre-merge evidence snapshot. At 06:03:32Z, its native schedule ages have increased by 265s: reconcile 6,824s; inspection 8,318s; recovery 8,177s; watchdog 8,123s; TCE WF-06 20,093s; TCE WF-12 6,039s. Inter-arrival gaps remain 16,665s / 17,233s / 17,135s / 17,077s / 23,393s / 16,987s. Thus all six age budgets and all six gap budgets still fail. K3s snapshot #43150245172 is 8,310s old vs 4,500s budget; reconciliation #43152960974 is 6,824s old vs 2,700s budget. No new native schedule, K3s inspection or current-master reconciliation was observed after the 12:59 snapshot.

No production mutation occurred. Platform Infra remains the sole production apply authority; TCE market-scan schedule remains unchanged.



## Current verified snapshot — 2026-11-12 12:59 ICT / 05:59:07 UTC

This refresh re-reads all five master refs, open PRs, first-page latest Actions runs, native schedule histories, the current tracker/inventory, the committed K3s inspection and selected failing job logs. Runtime evidence is explicitly age-gated; no current K3s state is inferred from an expired snapshot.

### Repository refs, open PRs and latest workflow evidence

| Repository | Verified master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `1e84b2e0919097c860dcb1e01ff98ea15a72b37b` | #1314/#544/#541/#539 (owner-decision drafts) | Current-master validate-manifests #43158871069 PASS. Latest native reconciliation #43152960974 SUCCESS at 04:09:48Z; no later native reconcile in the queried schedule history. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-12 native #43154415980 FAIL at 04:22:53Z because WF-06 was 234 minutes old; WF-13 #43154436821 SUCCESS; read-only WF-06 fallback #43154458775 FAIL, all four endpoints HTTP 503. WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 PASS. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS. Weekend scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. No current-master immutable publication or Platform promotion is evidenced by the latest run history. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | CI #42654579277 PASS. No current-master release/promotion is evidenced by the latest run history. |

The five default branches are `master`. Platform PRs #1314/#544/#541/#539 and Authentication #76 remain owner-decision drafts; none was changed or merged in this run. TCE, Stock and Media have no open PRs.

Platform master #1669 post-merge validation #43158871069 completed SUCCESS on exact current master `1e84b2e0`. The compare from parent `9f969fcfe0a8b31c5b612e218ea9f5a86e629059` to current master contains only documentation/checkpoint/decommission-runbook files; no production manifests, workflow definitions, secrets, credentials or runtime configuration changed.

### Latest native schedule evidence — reference 05:59:07Z

Only original first-attempt `event=schedule` runs on `master` count. Dispatch, workflow_run, push and rerun attempts do not reset native cadence.

| Lane | Latest native run | Created (UTC) | Age (s) | Previous inter-arrival gap (s) | Budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile-vps.yml | #43152960974 | 04:09:48 | 6,559 | 16,665 | 2,700 |
| Platform inspect-vps.yml | #43150245172 | 03:44:54 | 8,053 | 17,233 | 4,500 |
| Platform recover-stale-ops.yml | #43150505792 | 03:47:15 | 7,912 | 17,135 | 2,700 |
| Platform reconcile-schedule-watchdog.yml | #43150601305 | 03:48:09 | 7,858 | 17,077 | 2,700 |
| TCE WF-06 | #43127554403 | 00:28:39 | 19,828 | 23,393 | 1,500 |
| TCE WF-12 | #43154415980 | 04:22:53 | 5,774 | 16,987 | 1,500 |

All six current-age budgets and all six inter-arrival budgets fail. The TCE WF-12 job log reports the latest native WF-06 run age as 14,054s (234m) at its own API timestamp and measured runner queue wait as 0m. Platform watchdog #43150601305 reports its queue-assignment checks succeeded while native inter-arrival checks failed. These observations do not establish runner congestion as the cause.

TCE WF-12 #43154415980's authenticated Platform heartbeat job succeeded, but its separate schedule-verification job failed because WF-06 was stale. WF-13 #43154436821 then dispatched the existing read-only fallback #43154458775; all four strict public endpoints returned HTTP 503 (TCE web, TCE API, Auth liveness, Auth readiness). This fallback is not native schedule evidence and does not make service health green.

WF-06 was confirmed `active` by the WF-12 workflow-enabled step; Platform `reconcile-vps.yml` was confirmed active by the Platform watchdog. Other workflow enabled states were not freshly verified in this run. No authoritative GitHub scheduler-delivery/support telemetry was available to distinguish delayed from dropped enqueue events.

Preserve the checked-in cron expressions and existing freshness budgets. Do not alter TCE market-scan schedule, weaken HTTP-200 probes, add duplicate scheduled deployment authorities, or count fallback events as native delivery.

### GitOps reconciliation and K3s freshness

Reconciliation #43152960974 completed SUCCESS at 04:09:48Z on parent Platform SHA `9f969fcfe0a8b31c5b612e218ea9f5a86e629059`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`. At 05:59:07Z its age is 6,559s, beyond the 2,700s freshness budget.

- GHCR read preflight passed for all five managed packages (Auth service, MicroFE Shell/WS, TCE service/web).
- Auth runtime Secret was provisioned/verified; secret values were suppressed.
- Shared `ghcr-pull` remained unchanged.
- TCE release pairing passed.
- GitOps drift was false; manifest apply, image replacement and workload rollout were skipped.
- TCE/Auth were reported in maintenance/zero-replica state, not live application availability. MicroFE active-scope health passed; Keycloak was skipped.
- No new GHCR publication or digest promotion occurred.

The only commits after that reconciliation's parent and before current master are documentation/checkpoint/decommission-runbook changes, verified by compare API. The old no-drift result therefore describes the same manifest tree, but is not a fresh current-time runtime receipt.

Full inspection #43150245172 generated `debug/vps-latest.md` at 03:45:02Z. At 05:59:07Z it is 8,045s old, beyond the 4,500s inspection budget. Treat every workload detail below as historical only:

- Node `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Root disk 57% used, approximately 20GiB free; available RAM approximately 19GiB.
- Host `restart_required=yes`; kernel, containerd, Docker and OS updates pending. No upgrade/reboot occurred.
- Media backend/frontend and MicroFE Shell/WS/NATS: 1/1 Running. Media backend/frontend RepoDigests were recorded as `sha256:93ddb944…` and `sha256:095c72ed…`.
- TCE frontend/service, MicroFE Auth and Keycloak: 0/0 maintenance; do not infer live availability.
- Stock Admin: two Pods ImagePullBackOff on desired tag `12d63b4`; desired Backend: one Pod ImagePullBackOff. Legacy Backend/Frontend were Running but their imageIDs did not provide registry RepoDigest provenance. Do not promote local IDs or legacy tags.
- Platform and Media runner services were active/enabled; Media `Runner.Listener` was present.
- Preserve PVC `k3s-debug/k3s-debug-logs` (Bound, 1Gi/RWO).
- Docker reported 20 images / 9.195GB, 5.773GB reclaimable. No cleanup occurred.

Stock/Media decommission remains blocked by external backup/retention evidence, authoritative DNS ownership, Media runner stop/disable, Listener absence, GitHub-side runner unregister, fresh same-run storage preflight and protected production approval. In-cluster storage inventory is not external backup evidence.

### Safety and next actions

No production manifest apply, image publication/promotion, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation, Docker cleanup, host reboot/upgrade or workflow removal occurred. Platform Infra remains the sole production apply authority.

1. Platform operator: obtain fresh read-only `inspect-vps.yml` evidence and current-master `reconcile-vps.yml` `mode=plan` on `1e84b2e0`; do not use stale receipts as authorization.
2. GitHub repository/org administrator: inspect Actions policy and obtain authoritative schedule enqueue/delivery telemetry for the affected repositories/time windows; escalate persistent gaps to GitHub Support. Do not change cron or freshness budgets.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE`; set true only for approved zero-replica maintenance, otherwise restore services under the approved rollback plan. Preserve strict HTTP-200 health checks.
4. Stock owner: provide an ARM64-compatible immutable image digest/provenance if restoring Stock; configure `VNSTOCK_API_KEY` only through protected Actions settings if the scraper remains required.
5. Media owner: stop/disable/unregister the dedicated runner and provide backup/retention and authoritative DNS evidence before protected decommission.
6. GitHub administrator: verify effective inherited rulesets and enforce PR-only, required checks, force-push/deletion protection and squash-only on all five default branches.
7. Platform operator: obtain explicit approval before host package/kernel/containerd/Docker upgrades or reboot.


## Post-merge receipt — 2026-11-12 11:04 ICT / 2026-11-12 04:04:42 UTC

Platform PR #1668 was squash-merged at `af37d170ea755f1bca4c3f413d6a04b8d2d7210f`. Exact-head validation #43152296355 completed SUCCESS on `2cbe16d1961313a24bc9147e1aba36c9bf7b0555`; post-merge validate-manifests #43152354741 completed SUCCESS on the exact merge SHA. All applicable manifest/contract validation steps passed. The PR changed only the deployment tracker, workflow inventory and two timestamped checkpoint files; no production manifest, workflow, secret, credential or runtime configuration changed.

The 10:59 ICT receipt above remains an accurate timestamped snapshot taken at 03:59:56Z on Platform master `55cacb6d`. Current Platform master is now `af37d170`; TCE `34f6024f`, Stock `b1b5e177`, Media `dcd69869` and Authentication `eab85fab` remain unchanged. Open owner-decision PRs remain Platform #1314/#544/#541/#539 and Authentication #76; PR #1668 is merged.

At 04:04:42Z, no new qualifying native schedule run superseded the 10:59 IDs. Current-age values increased by 286s to: reconcile 16,359s; inspection 1,188s; recovery 1,047s; watchdog 993s; TCE WF-06 12,963s; TCE WF-12 15,896s. Inter-arrival gaps remain 22,471s / 17,233s / 17,135s / 17,077s / 23,393s / 22,441s respectively. Thus 3/6 age budgets and 6/6 gap budgets still fail. Do not change cron or TCE market-scan schedule.

Current-master reconciliation #43150525282 remains successful evidence on the parent manifest tree (age 1,036s vs 2,700s budget); it found no drift, verified five GHCR package reads, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, and skipped manifest apply/image replacement/rollout. K3s snapshot generated 03:45:02Z is 1,180s old vs 4,500s budget. Both remain within freshness budgets at this reference; no new runtime mutation occurred.

All five master branches still report `protected=false`; effective inherited organization rulesets remain unverified. TCE/Auth zero-replica maintenance, Stock ImagePullBackOff, Media runner/Listener active, Stock/Media decommission evidence gaps and host restart approval remain unchanged. No workflow was removed and no production mutation occurred.


## Latest verification — 2026-11-12 10:59 ICT / 2026-11-12 03:59:56 UTC

This refresh supersedes the 09:05 ICT repository/runtime snapshot. It uses direct GitHub REST reads of all five master refs, open PRs, first-page latest Actions runs, native schedule histories, Platform master check runs, the committed K3s inspection, and selected job logs. Only first-attempt `event=schedule` runs on `master` count toward native cadence.

### Verified repository refs, open PRs and latest evidence

| Repository | Verified master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `55cacb6d2f0f347df896b7811ab5183399b1c0e5` | #1314/#544/#541/#539 (owner-decision drafts) | Inspection PR #1667 merged at `55cacb6d`; exact-head validate-manifests #43150444565 PASS. Current-master reconciliation #43150525282 SUCCESS. Native watchdog #43150601305 FAIL on stale native cadence. Recovery #43150855730 SUCCESS as workflow_dispatch. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 PASS. Native WF-06 #43127554403 FAIL (all four strict endpoints returned HTTP 503); native WF-12 #43121528127 FAIL. WF-07 backup #43130553977 SUCCESS. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS. Scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. Desired tag `12d63b4` remains without compatible ARM64 RepoDigest evidence in the latest K3s snapshot. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS; no current-master immutable publication/handoff evidenced. Latest K3s snapshot shows backend/frontend 1/1 with registry RepoDigests. Dedicated runner remains active. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | CI #42654579277 PASS; no current-master release evidenced. Auth remains zero-replica maintenance in the latest K3s snapshot. |

Platform PR #1667 was generated by scheduled inspection #43150245172, validated on exact PR head `907e2e45fd0153d5c277b07c55f919bad0a06cba` by #43150444565, and squash-merged at `55cacb6d2f0f347df896b7811ab5183399b1c0e5`. The committed `debug/vps-latest.md` is generated at 03:45:02Z. No production manifest changed in that inspection PR.

### Current-master GitOps reconciliation

Reconciliation #43150525282 completed SUCCESS at 03:47:26Z on exact current Platform master SHA `55cacb6d2f0f347df896b7811ab5183399b1c0e5`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`. At the 03:59:56Z reference its age is 750s, within the 2,700s reconciliation freshness budget.

- GHCR pull-access preflight passed for all five managed packages: Auth service, MicroFE Shell/WS, and TCE service/web.
- Auth runtime Secret was provisioned and verified; secret values were suppressed.
- Shared `ghcr-pull` Secrets were unchanged.
- TCE release pairing passed for `prod-v0.1.0-e75e338`.
- Blocked-image-pull restart check found no failures in the managed MicroFE Auth/Shell/WS and TCE service/frontend workloads.
- GitOps drift was false. Production manifest apply, image replacement and workload rollout were skipped.
- TCE and Auth deployment lanes reported maintenance/zero-replica health; this is not live application availability. MicroFE active-scope health passed. Keycloak lane was skipped.
- No new GHCR publication or digest promotion occurred.

This is current-master apply-mode evidence, not merely a plan. It does not repair the separately retired Stock/Media workloads.

### Fresh K3s snapshot — historical state is now within inspection freshness

Full inspection #43150245172 completed SUCCESS as a native scheduled run on parent SHA `964c0b7d`; its exact inspection PR was merged as #1667. Snapshot generated at 03:45:02Z is 894s old at the 03:59:56Z reference, within the 4,500s budget.

- Node `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Root disk 57% used, about 20GiB free; available RAM about 19GiB.
- Host reports `restart_required=yes`; kernel, containerd, Docker and OS package updates are pending. No upgrade/reboot was performed.
- Media backend/frontend: 1/1 Running with RepoDigests `sha256:93ddb944…` and `sha256:095c72ed…`.
- MicroFE Shell/WS and NATS: 1/1 Running with RepoDigest evidence.
- TCE frontend/service, MicroFE Auth and Keycloak: 0/0 maintenance; no live health is asserted.
- Stock Admin: two pods ImagePullBackOff on desired tag `12d63b4`; Stock desired Backend: one pod ImagePullBackOff. A legacy Backend and Frontend pod are Running but have no registry RepoDigest evidence; do not use local image IDs or legacy tags for promotion.
- Platform and Media self-hosted runner services are active/enabled; Media `Runner.Listener` is present.
- The only listed PVC is `k3s-debug/k3s-debug-logs`, Bound, 1Gi/RWO. Preserve it.
- Docker reports 20 images / 9.195GB, 5.773GB reclaimable. No cleanup occurred.

Stock/Media decommission remains blocked by external backup/retention, authoritative DNS, Media runner stop/disable/Listener absence/GitHub-side unregister, and protected production approval. In-cluster storage inventory alone is not external backup evidence.

### Native schedule freshness — reference 03:59:56Z

| Lane | Latest qualifying native run | Age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile-vps.yml | #43120544165 | 16,073 | 22,471 | 2,700 |
| Platform inspect-vps.yml | #43150245172 | 902 | 17,233 | 4,500 |
| Platform recover-stale-ops.yml | #43150505792 | 761 | 17,135 | 2,700 |
| Platform reconcile-schedule-watchdog.yml | #43150601305 | 707 | 17,077 | 2,700 |
| TCE WF-06 | #43127554403 | 12,677 | 23,393 | 1,500 |
| TCE WF-12 | #43121528127 | 15,610 | 22,441 | 1,500 |

Current-age budgets fail for 3/6 lanes (Platform reconciliation, TCE WF-06 and WF-12); inter-arrival budgets fail for 6/6. The current-master workflow_dispatch reconciliation #43150525282 and recovery workflow_dispatch #43150855730 do not reset native schedule age/gaps. Watchdog #43150601305 failed on stale native reconciliation and inter-arrival gaps. TCE WF-06 logs confirm HTTP 503 for TCE web, TCE API, Auth liveness and Auth readiness; WF-12 confirms the WF-06 schedule is stale while its authenticated Platform heartbeat job succeeded. A successful heartbeat/manual recovery is not native WF-06 delivery.

Platform cron expressions remain unchanged: reconcile `7,22,37,52`, inspection `2,32`, recovery `10,25,40,55`, watchdog `12,27,42,57`. TCE WF-06 remains `*/15`; WF-12 remains `7,22,37,52`. Do not alter the TCE market-scan schedule or weaken strict HTTP-200 probes. No authoritative evidence establishes runner congestion as the cause; administrator-side scheduler enqueue/delivery telemetry is still required.

### Governance, preservation and next actions

All five `master` branch API reads report `protected=false`. Repository metadata still permits squash, merge commit and rebase. Effective inherited organization rulesets are not verified. GitHub administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.

1. GitHub administrator: provide authoritative schedule enqueue/delivery telemetry; preserve existing cron expressions.
2. TCE administrator: verify `TCE_MAINTENANCE_MODE`; set true only for an approved zero-replica maintenance window, otherwise restore replicas. Keep strict HTTP-200 probes.
3. Stock owner: provide a compatible immutable ARM64 image digest or complete approved retirement; configure `VNSTOCK_API_KEY` only through protected Actions settings if scraper operation is retained.
4. Media owner/operator: stop/disable/unregister the dedicated runner and prove Listener absence, GitHub-side unregister, backup/retention and DNS before protected decommission.
5. Platform operator: obtain explicit approval before host upgrades/reboot; preserve the debug PVC.
6. Continue fresh read-only inspection and reconciliation evidence before any further production mutation.

No workflow was removed. No new image was published/promoted; no manifest drift/apply or workload rollout occurred; no namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. App repositories retain tests/builds/security/immutable publication/provenance ownership; Platform Infra remains the sole production manifest, shared pull credential, promotion, GitOps, rollout and health authority. No competing SSH/Compose authority was added.


Last reviewed: 2026-11-12 09:05 ICT (2026-11-12 02:05:00 UTC).




## Post-merge readiness verification — 2026-11-12 09:05 ICT / 2026-11-12 02:05:00 UTC

This receipt supersedes the 08:59 ICT snapshot for repository refs and Platform validation. PR #1663 was squash-merged at `c84b19b6fd0618cda70034e9cb7c65992ea0bfbb`; exact-head validation #43138768416 passed on `b52a68e2afb00b5d4bf881326761c9593b90fd29`, and post-merge validation #43138836807 passed on the exact merge SHA. The 08:59 checkpoint remains an accurate timestamped pre-merge snapshot; no production manifests or runtime state changed in PR #1663.

### Verified repository refs and open PRs

| Repository | Master SHA | Open PRs | Latest relevant checks |
|---|---|---|---|
| Platform Infra | `c84b19b6fd0618cda70034e9cb7c65992ea0bfbb` | #1314/#544/#541/#539 owner decisions | Post-merge validate-manifests #43138836807 SUCCESS. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-01 #43132696439, WF-02 #43132696403, WF-05 #43132696349 SUCCESS. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing `VNSTOCK_API_KEY`). |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; no current-master publication evidenced. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner-decision draft | CI #42654579277 SUCCESS; no current-master release evidenced. |

All five branch metadata reads still report `protected=false`. Effective inherited organization rulesets remain unverified. GitHub administrator enforcement is still required.

### Native schedule freshness — reference 02:05:00Z

Only first-attempt `event=schedule` runs on master count. Ages are recalculated from the same latest qualifying run timestamps; inter-arrival gaps are unchanged.

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #43120544165 | 9,177 | 22,471 | 2,700 |
| Platform inspection | #43116036275 | 11,239 | 24,826 | 4,500 |
| Platform recovery | #43116568507 | 11,000 | 23,725 | 2,700 |
| Platform watchdog | #43116818114 | 10,888 | 23,716 | 2,700 |
| TCE WF-06 | #43127554403 | 5,781 | 23,393 | 1,500 |
| TCE WF-12 | #43121528127 | 8,714 | 22,441 | 1,500 |

All 6/6 age and 6/6 inter-arrival budgets fail. WF-06 #43127554403 returned HTTP 503 on all four strict probes. WF-12 #43121528127 found the prior native WF-06 source 20,460s old at its own reference and measured 0m queue wait. Runner congestion is not established. Do not count manual, workflow_run, repository_dispatch, push or rerun events as native delivery. Preserve all cron expressions and the TCE market-scan schedule.

### Runtime evidence remains expired

- Reconciliation #43127613751: SUCCESS on parent SHA `331120b`, workflow_dispatch at 00:29:09Z, age 5,751s vs 2,700s budget (expired by 3,051s). Five GHCR package reads passed; Auth runtime Secret verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing passed; drift=false; apply/image replacement/rollout skipped.
- Full inspection #43127872524: SUCCESS on parent SHA `331120b`, generated 00:31:21Z, age 5,619s vs 4,500s budget (expired by 1,119s). Last-known node/workload/image/runner/storage details remain historical only.
- Compare `331120b` to current master includes only inspection/documentation/checkpoint changes; no production manifest path changed. This does not replace a current-master `mode=plan` or fresh full inspection.
- Stock/Media decommission remains blocked by external backup/retention, authoritative DNS, Media runner stop/disable/Listener absence/GitHub unregister and protected production approval. Preserve the debug PVC.

### Next actions and safety

1. Platform operator: fresh read-only inspection and current-master `reconcile-vps.yml` `mode=plan` on `c84b19b6`. Workflow dispatch is not available through the current connector.
2. GitHub administrator: provide authoritative schedule enqueue/delivery telemetry and enforce PR-only/required checks/force-push and deletion protection/squash-only.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE`; PR #1038 adds an unset warning but does not change the repository variable. Keep strict HTTP-200 probes.
4. Stock owner: keep desired image promotion blocked until a compatible immutable ARM64 digest exists or approved retirement completes; scraper remains fail-closed until the secret is configured through protected settings.
5. Media owner: complete runner retirement, backup/retention and DNS evidence before protected decommission.
6. Platform operator: obtain explicit maintenance approval before host package/kernel/containerd/Docker upgrades or reboot.

No new GHCR publication, digest promotion, current-master plan/apply, manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow was removed or direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-12 08:59 ICT / 2026-11-12 01:59:28 UTC

This refresh uses direct GitHub REST reads of all five master refs, open PRs, the first page of Actions runs, selected job logs, the current tracker/inventory and the committed full K3s snapshot. Native cadence counts only first-attempt `event=schedule` runs on `master`; manual, push, pull_request, workflow_run, repository_dispatch and reruns are excluded.

### Repository readiness

| Repository | Verified master SHA | Open PRs | Latest relevant checks |
|---|---|---|---|
| phanthienquoc/platform-infra | `85c0d1fe1a61af3bdd4e1e2b1441e74cdb08d8c3` | #1314/#544/#541/#539 owner-decision drafts | Current-master validate-manifests #43132927187 SUCCESS. PR #1661/#1662 merged; exact-head and post-merge validations passed. |
| phanthienquoc/TCE-dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | TCE PR #1038 merged. Current-master WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 SUCCESS. Latest native WF-06 #43127554403 FAIL (four HTTP 503); latest native WF-12 #43121528127 FAIL. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Current-master CI #42610360402 SUCCESS. Scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. Desired Admin/Backend tag `12d63b4` still has no compatible ARM64 manifest/RepoDigest in the last full inspection. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Current-master CI #42539512417 SUCCESS; no current-master immutable publication/handoff is evidenced. Last full inspection showed backend/frontend 1/1 with RepoDigests and dedicated runner active. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner-decision draft | Current-master CI #42654579277 SUCCESS; no current-master release/handoff is evidenced. Auth remains 0/0 maintenance in the last full inspection. |

### TCE maintenance warning change

- TCE PR #1038 was squash-merged at `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`. It makes an unset `TCE_MAINTENANCE_MODE` explicit with a warning while preserving read-only fallback behavior and strict WF-06 HTTP-200/WF-12 schedule checks.
- Current-master WF-01/WF-02/WF-05 checks passed. The Actions variable itself was not changed by the PR.
- WF-13 #43127582309 ran before the merge on TCE SHA `5b425bde`; its log showed an empty `TCE_MAINTENANCE_MODE` and dispatched read-only WF-06 fallback #43127603475. The current repository variable value has not been read or re-proven after the merge. TCE administrator must verify it and set `true` only for an approved zero-replica maintenance window; otherwise restore service replicas. Do not weaken HTTP-200 probes.

### GitOps and runtime freshness

- Reconciliation #43127613751 completed SUCCESS as `workflow_dispatch` on parent SHA `331120b33ed7b090620dec373b20aab463d78cc8` at 00:29:09Z. It used `mode=apply`, `target_app=all`, `allow_image_changes=false`. Five GHCR package read checks passed; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` was unchanged; TCE release pairing passed. GitOps drift was false, so manifest apply, image replacement and workload rollout were skipped.
- At the 01:59:28Z reference, that reconciliation is 5,419s old versus a 2,700s freshness budget (expired by 2,719s). It is historical evidence only and does not authorize current production action.
- Compare `331120b` to current master `85c0d1fe` shows only the inspection snapshot and documentation/checkpoint changes; no production manifest path changed. This does not replace a current-master `mode=plan`.
- Full inspection #43127872524 completed SUCCESS as `workflow_dispatch` on the same parent SHA and generated `debug/vps-latest.md` at 00:31:21Z. At 01:59:28Z its age is 5,287s against a 4,500s budget (expired by 787s). It is historical only; no fresh full inspection is evidenced.

### Last-known K3s state — historical, not current

- Node `tce-k3s-01`: Ready/ARM64; Ubuntu 22.04.5; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`; disk 56% with about 20GiB free; available RAM about 19GiB; host `restart_required=yes`.
- Media backend/frontend: 1/1 Running with RepoDigests `sha256:93ddb944…` and `sha256:095c72ed…`. MicroFE Shell/WS and NATS: 1/1 with RepoDigest evidence.
- TCE frontend/service, MicroFE Auth and Keycloak: 0/0 maintenance; public OIDC probes returned 503. Do not assert live service health.
- Stock Admin has two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod for tag `12d63b4`; K3s reported `no match for platform in manifest`. Legacy Stock Backend/Frontend were running but had no registry RepoDigest evidence. Do not promote local image IDs or legacy tags.
- Dedicated Media runner service was active/enabled and `Runner.Listener` was present. GitHub-side runner unregister remains unverified. Target Stock/Media namespaces had no PVC/PV claims or VolumeSnapshot references in that snapshot; this does not prove external backup/retention or DNS ownership.
- Preserve `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO). No Docker cleanup, host reboot, runner stop/unregister, namespace deletion or storage mutation occurred.

### Native schedule freshness — reference 01:59:28Z

Only first-attempt scheduled runs on master count. Latest run age and inter-arrival gaps were recalculated from GitHub run timestamps:

| Lane | Latest qualifying native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile-vps.yml | #43120544165 | 8,845 | 22,471 | 2,700 |
| Platform inspect-vps.yml | #43116036275 | 10,907 | 24,826 | 4,500 |
| Platform recover-stale-ops.yml | #43116568507 | 10,668 | 23,725 | 2,700 |
| Platform schedule watchdog | #43116818114 | 10,556 | 23,716 | 2,700 |
| TCE WF-06 | #43127554403 | 5,449 | 23,393 | 1,500 |
| TCE WF-12 | #43121528127 | 8,382 | 22,441 | 1,500 |

All 6/6 current-age budgets and 6/6 inter-arrival budgets fail. WF-06 #43127554403 executed natively but failed all four strict public probes (TCE web/API and Auth liveness/readiness returned HTTP 503). WF-12 #43121528127 failed because the latest native WF-06 was 20,460s old at its 23:39:46Z reference; its log measured 0m queue wait for that source run, so runner congestion is not established. WF-13 workflow_run and read-only WF-06 fallback runs do not satisfy native schedule freshness. Preserve all cron expressions, especially the TCE market-scan schedule.

### Governance and next actions

- Direct branch metadata reads report `protected=false` for all five master branches. Effective inherited organization rulesets cannot be inferred from the available reads; GitHub administrator must verify/enforce PR-only, required checks, force-push/deletion protection and squash-only.
- Platform operator: obtain fresh read-only `inspect-vps.yml` and current-master `reconcile-vps.yml` `mode=plan` on `85c0d1fe`. The connector has no workflow-dispatch action, so neither was run in this pass.
- GitHub administrator: provide authoritative schedule enqueue/delivery telemetry and repair native delivery without changing cron or freshness budgets.
- TCE administrator: verify `TCE_MAINTENANCE_MODE`; retain strict WF-06/WF-12 checks.
- Stock owner: keep desired image promotion blocked until a compatible immutable ARM64 digest exists or approved retirement completes; scraper remains fail-closed until `VNSTOCK_API_KEY` is configured.
- Media owner: stop/disable/unregister the dedicated runner and provide external backup/retention and authoritative DNS evidence before protected decommission.
- Platform operator: obtain explicit maintenance approval before OS/kernel/containerd/Docker upgrades or reboot.

No new GHCR publication, digest promotion, current-master GitOps plan/apply, manifest change, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. No workflow was removed and no direct SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 23:14:06 UTC / 2026-11-12 06:14:06 ICT

This refresh supersedes the 06:10 ICT follow-up. Direct reads verified all five master refs/open PRs, current Platform Actions runs/checks, the merged recovery retry fix, and the latest K3s/GitOps evidence. Native cadence counts only first-attempt event=schedule runs on master.

## Repository readiness

| Repository | Master SHA | Open PRs | Current relevant evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 3ad8cc30535af6c627175b22070ee2ca3799d100 | #1658 current readiness refresh; #1314/#544/#541/#539 owner-decision drafts | PR #1657 merged; exact-head validate-github-actions #43118015009 PASS and validate-manifests #43118014978 PASS. Post-merge #43118124205 and #43118124229 both PASS. |
| phanthienquoc/TCE-dashboard | 5b425bdeab457e943bcecf1831836fc698e24394 | none | Native WF-06 #43073311537 FAIL; native WF-12 #43068077606 FAIL. Manual WF-06 #43088897948 FAIL (four HTTP 503 probes). WF-13 #43088861304 logged empty TCE_MAINTENANCE_MODE. WF-07 integration #43088811861 PASS. |
| phanthienquoc/stockdividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED because VNSTOCK_API_KEY is missing. Desired Admin/Backend image tag 12d63b4 has no compatible platform manifest/RepoDigest. |
| phanthienquoc/media-generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 PASS. Fresh K3s snapshot shows Media backend/frontend 1/1 with RepoDigests. Dedicated Media runner remains active/enabled; no current-master publication is evidenced. |
| phanthienquoc/phanthienquoc-authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 owner-decision draft | CI #42654579277 PASS. Auth remains intentional 0/0 maintenance; no current-master release/handoff is evidenced. |

### PR #1657 — recovery correlation retry fix

- PR #1657 was squash-merged at 23:13:14Z; exact head b4ac08479cee2f54bfd4b86717b8bd9b0967a339; merge/current master 3ad8cc30535af6c627175b22070ee2ca3799d100.
- Exact-head validate-github-actions #43118015009 PASS (actionlint, yamllint, shellcheck, ops regression tests, immutable image-change tests and workflow-contract checks). Exact-head validate-manifests #43118014978 PASS.
- Post-merge validate-github-actions #43118124205 PASS and validate-manifests #43118124229 PASS on current master.
- Root cause: recovery run #43116633087 dispatched reconciliation successfully but then failed when the GitHub Actions run-history correlation GET returned HTTP 502. The old set -e path aborted before the outer six-attempt loop could retry.
- The merged recovery controller now retries only HTTP 500/502/503/504 during both reconciliation and read-only inspection dispatch-correlation GETs, with bounded 5-second-per-attempt backoff. Permanent 4xx/auth errors and malformed JSON remain fail-closed. Cron, dispatch mode/scope and production ownership are unchanged.

### GitOps and K3s evidence

- Native inspection #43116036275 completed SUCCESS and generated debug/vps-latest.md at 22:57:49Z. At this 23:14:06Z reference the snapshot age is 985s, within the 4,500s budget.
- Reconciliation #43116379969 completed SUCCESS on parent master SHA c0f309, triggered by the recovery controller with mode=apply, target_app=all, allow_image_changes=false. Docs-only PR #1656 and workflow/validator PR #1657 advanced master to 3ad8cc without changing production manifests. No exact-3ad8cc reconciliation is evidenced.
- GHCR read preflight passed five managed packages. Auth runtime Secret was provisioned/verified with values suppressed. Shared ghcr-pull was unchanged. TCE release pairing passed for prod-v0.1.0-e75e338. GitOps drift=false; manifest apply, image replacement and workload rollout were skipped. Auth and TCE lanes reported maintenance (zero replicas; no live health asserted); MicroFE active-scope health passed; Keycloak was skipped.
- K3s node tce-k3s-01 is Ready/ARM64; Ubuntu 22.04.5; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2. RAM about 19Gi available; root disk 56% used with about 20GiB free. Host restart remains required for pending OS/kernel/containerd/Docker updates; no reboot/upgrade occurred.
- Media backend/frontend, MicroFE Shell/WS and NATS are 1/1. TCE frontend/service, MicroFE Auth and Keycloak are 0/0 maintenance; OIDC probes returned 503. Stock Admin has two ImagePullBackOff pods; desired Backend has one ImagePullBackOff pod while an older pod remains Running. Desired Stock tag 12d63b4 has no matching platform manifest/RepoDigest. Legacy Stock tag 23b2878 is cached/running but has no RepoDigest and is not promotion evidence.
- PVC k3s-debug/k3s-debug-logs remains Bound (1Gi/RWO/local-path). Stock/Media storage preflight found no PVC/PV or VolumeSnapshot references, but decommission remains blocked by backup/retention, authoritative DNS, Media runner stop/disable/unregister and protected production approval. Media runner service and Runner.Listener remain active. Docker cleanup was not performed.

### Native schedule freshness — reference 23:14:06Z

| Lane | Latest qualifying native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #43066718643 | #42993779924 | 21,394 | 28,867 | 2,700 |
| Platform inspection | #43116036275 | #43054529460 | 985 | 24,836 | 4,500 |
| Platform recovery | #43116568507 | #43058316157 | 746 | 23,725 | 2,700 |
| Platform watchdog | #43116818114 | #43058640134 | 634 | 23,716 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 18,920 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 20,901 | 28,287 | 1,500 |

All 6/6 inter-arrival budgets fail; 3/6 current-age budgets fail (Platform reconcile, TCE WF-06 and TCE WF-12). Inspection, recovery and watchdog current-age are within budget, but their inter-arrival gaps still fail. Watchdog #43116818114 failed on native gaps. It verified three WF-06 and four WF-12 heartbeat receipts and reported no scheduled deployment lane over the 15-minute queue budget; runner congestion is not established. Recovery #43116883745 is a workflow_run success, not native schedule delivery. Preserve all cron expressions and the TCE market-scan schedule.

## Current actions

1. Platform operator: run a fresh read-only inspection and a current-master reconcile-vps mode=plan on 3ad8cc; the last successful reconciliation #43116379969 ran on parent SHA c0f309, and no exact-current-master reconciliation is evidenced.
2. GitHub administrator: repair native schedule delivery/telemetry and enforce PR-only, required checks, force-push/deletion protection and squash-only.
3. TCE administrator: verify TCE_MAINTENANCE_MODE according to the approved zero-replica maintenance state; keep strict HTTP-200 probes.
4. Media owner/operator: stop/disable/unregister the dedicated runner and provide backup/retention and authoritative DNS evidence before protected decommission.
5. Stock owner: keep desired image promotion blocked until a compatible immutable ARM64 digest exists or the approved retirement path completes.
6. Platform operator: obtain approval before host package upgrades/reboot; preserve k3s-debug/k3s-debug-logs.

## Current runtime blockers

- TCE administrator must verify TCE_MAINTENANCE_MODE. WF-13 #43088861304 logged it empty (mapped to disabled); strict WF-06 HTTP-200 probes returned four 503s. Do not weaken WF-06/WF-12.
- Stock desired image remains unpromotable until a compatible immutable ARM64 digest exists or the approved retirement path completes. Scraper remains fail-closed on missing VNSTOCK_API_KEY.
- Media runner retirement, backup/retention, authoritative DNS and protected production approval remain outstanding. Preserve the debug PVC.
- Host restart/upgrade requires platform approval. No reboot, Docker cleanup or namespace deletion.
- Branch-protection detail GET returned 403 for all five repositories; effective inherited organization rulesets remain unverified. GitHub administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.
- No new GHCR publication, digest promotion, manifest apply, image replacement or workload rollout occurred. Auth runtime Secret provision/verification did occur; shared ghcr-pull remained unchanged. No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow was removed or direct SSH/Compose authority added.


## Latest verification — 2026-11-11 22:02:56 UTC / 2026-11-12 05:02:56 ICT

This post-merge refresh supersedes the prior 04:02 ICT compact snapshot. Repository refs and Actions runs were read directly from GitHub REST. Only first-attempt `event=schedule` runs on `master` count toward native cadence; manual, push, pull_request, workflow_run, repository_dispatch and reruns are excluded.

### Direct master refs and open PRs

| Repository | Verified master SHA | Open PRs | Latest relevant workflow evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `f2ad42a5a9437c35aad11f3a5eeab644902f6241` | #1314/#544/#541/#539 owner-decision drafts | PR #1653 merged by squash at 22:02:53Z; exact-head validation #43100250244 on `dae50fe614dcdf6432de1b1c616f3034a1146f6c` PASS (20/20 validation steps). New master validation #43108386625 on `f2ad42a5` is in progress; network-boundary step was still running at inspection. |
| phanthienquoc/TCE-dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | none | Latest WF-06 manual #43088897948 FAIL (4 strict HTTP-200 probes returned 503); latest native WF-06 #43073311537 FAIL; latest native WF-12 #43068077606 FAIL; WF-13 #43088861304 workflow_run SUCCESS but logged empty `TCE_MAINTENANCE_MODE`; WF-07 integration schedule #43088811861 PASS (not health/schedule-watchdog evidence). |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Stock CI #42610360402 PASS. Scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. No current-master image publication/promotion is evidenced in the inspected Actions run window. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Media CI #42539512417 PASS. Latest inspected successful production publication #41158598649 is older than current master; no current-master publication or Platform handoff is evidenced. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner-decision draft | Auth CI #42654579277 PASS. Latest inspected release #41040510320 is older than current master; no current-master release/handoff is evidenced. |

PR #1653 ([TCE maintenance and Stock/Media decommission gates](https://github.com/phanthienquoc/platform-infra/pull/1653)) is now merged. It changed documentation only; no Actions variable, secret, manifest, image, workload, namespace, runner, DNS, database, storage or host state was mutated. Its exact-head validation #43100250244 completed successfully with all 20 validation steps PASS. Merge SHA is the current master `f2ad42a5a9437c35aad11f3a5eeab644902f6241`.

### Latest master workflow checks

| Repository / workflow | Run | Event / state | Interpretation |
|---|---:|---|---|
| Platform validate-manifests | #43108386625 | push / in_progress | Current-master post-merge validation; validation job running, network-boundary step in progress at inspection. |
| Platform validate-manifests | #43094091607 | push / SUCCESS | Previous master `99509adb`, superseded by PR #1653 merge. |
| Platform inspect-vps | #43089176130 | workflow_dispatch / SUCCESS | Full snapshot generated 19:39:15Z on older SHA `9093831c`; now expired. |
| Platform reconcile-vps | #43088879697 | workflow_dispatch / SUCCESS | Parent `9093831c`, `mode=apply`, target=all, image changes=false; 5 GHCR reads PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; drift=false; apply/image replacement/rollout skipped. Historical only, expired and not current-master authorization. |
| TCE WF-06 | #43088897948 | workflow_dispatch / FAILURE | Four public HTTP-200 probes returned 503. |
| TCE WF-13 | #43088861304 | workflow_run / SUCCESS | Log showed empty `TCE_MAINTENANCE_MODE`, which maps to disabled; does not prove the current repository variable value. |
| TCE WF-12 | #43088836266 | workflow_run / FAILURE | Stale native WF-06 source; not a native schedule run. |
| TCE WF-07 integration | #43088811861 | schedule / SUCCESS | Integration-only lane. |
| Stock CI / scraper | #42610360402 / #42457182511 | push / SUCCESS; schedule / FAILURE | Scraper remains fail-closed on missing API key. |
| Media CI | #42539512417 | push / SUCCESS | Tests/build passed; no current-master publication evidence. |
| Authentication CI | #42654579277 | push / SUCCESS | CI passed; no current-master release evidence. |

### Native schedule freshness — reference 22:02:56Z

| Lane | Latest qualifying native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile-vps.yml | #43066718643 | #42993779924 | 17,124 | 28,867 | 2,700 |
| Platform inspect-vps.yml | #43054529460 | #42981286761 | 21,551 | 30,159 | 4,500 |
| Platform recover-stale-ops.yml | #43058316157 | #42986496462 | 20,201 | 29,036 | 2,700 |
| Platform schedule watchdog | #43058640134 | #42986833403 | 20,080 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 14,650 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 16,631 | 28,287 | 1,500 |

All 6/6 current-age and 6/6 inter-arrival budgets fail. Queue telemetry in the last inspected WF-12 sample was zero minutes, so the available evidence does not establish runner congestion. WF-07, WF-13 workflow_run receipts, manual WF-06 runs and reruns do not substitute for native first-attempt schedule delivery. Preserve every cron expression and the TCE market-scan schedule.

### Runtime freshness and production authority

- Full K3s inspection #43089176130 generated `debug/vps-latest.md` at 19:39:15Z. At 22:02:56Z its age is 8,621s against a 4,500s budget; expired by 4,121s. It is historical only.
- Reconciliation #43088879697 ran at 19:37:08Z on parent SHA `9093831c`. At 22:02:56Z its age is 8,748s against a 2,700s budget; expired by 6,048s. It is historical only and does not authorize current-master apply.
- Last-known workloads: Media backend/frontend and MicroFE Shell/WS/NATS were 1/1; TCE/Auth/Keycloak were 0/0 maintenance; Stock desired Admin (two pods) and Backend (one pod) were ImagePullBackOff on `12d63b4`. Stock legacy workloads were running but did not provide compatible desired-release digest evidence. Do not assert these as current without a fresh inspection.
- Historical reconciliation verified five GHCR package reads and Auth runtime Secret, left shared `ghcr-pull` unchanged, found no drift, and skipped apply/image replacement/rollout.
- PR #1653 confirms the Stock/Media decommission scope is approved and GitOps ownership retirement is already merged. Namespace deletion remains blocked pending fresh same-run storage preflight, external backup/retention evidence, authoritative DNS/host/TLS review, local Media runner service stopped/disabled with no Listener, and GitHub-side runner registration absence. Preserve `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO) and all TCE/Auth/MicroFE/Keycloak resources.
- WF-13 #43088861304 logged `TCE_MAINTENANCE_MODE` empty; that run resolved maintenance as disabled and dispatched a read-only WF-06 fallback. Current repository variable value remains inaccessible. TCE administrator must verify it; set true only for an approved zero-replica maintenance window, otherwise restore service replicas. Keep strict HTTP-200 probes.
- GitHub repository metadata still permits squash, merge commit and rebase. Repo rulesets GET returned `[]` on Platform, TCE, Media and Auth; Stock rulesets GET returned 403. Branch-protection detail GET returned 403. Effective inherited organization rulesets and actual protection cannot be inferred from these reads; administrator verification/enforcement remains required.

### Exact next actions

1. Platform operator: obtain fresh read-only `inspect-vps.yml` and run `reconcile-vps.yml` on current master `f2ad42a5` with `mode=plan`; do not use expired parent-SHA evidence.
2. Platform CI: verify current-master validation #43108386625 completes successfully; exact PR #1653 validation #43100250244 already passed.
3. GitHub administrator: provide native schedule enqueue/delivery telemetry and enforce PR-only, required checks, force-push/deletion protection and squash-only across all five repositories.
4. TCE administrator: verify `TCE_MAINTENANCE_MODE`; do not weaken HTTP-200 or native schedule checks.
5. Media operator/decommission owner: provide backup/retention and authoritative DNS evidence; stop/disable runner, verify local Listener absence and GitHub-side registration removal; then run the protected same-run plan before any delete.
6. Stock owner: keep desired image publication/promotion blocked until a compatible ARM64 immutable digest exists or the approved decommission path is completed.
7. Preserve app-owned tests/builds/security and immutable publishers; Platform remains sole production manifest, shared pull credential, digest promotion, GitOps, rollout and health authority.

No workflow dispatch, new GHCR publication, digest promotion, current-master GitOps plan/apply, workload rollout, namespace/PVC/PV deletion, runner stop/unregister, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. The current GitHub connector exposes read/write repository and PR operations but no Actions workflow-dispatch action. No direct SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.

---

Last reviewed: 2026-11-12 04:02 ICT (2026-11-11 21:02:52 UTC).

This is the compact current readiness view; the 04:02 ICT verification above supersedes the prior 03:12 ICT compact snapshot. Historical append-only content is preserved below and under `docs/archive`; timestamped checkpoints remain under `docs/cross-repo-deployment-checkpoints`. GitHub Actions run listing was retrieved through read-only Actions REST GET (first page per repository/query). PR #1651 merged at 20:09:00Z; exact-head #43093685819 and post-merge master validation #43093772516 completed SUCCESS.

## Latest verification — 2026-11-12 04:02 ICT / 2026-11-11 21:02:52 UTC

This refresh uses direct master refs, first-page Actions REST run listings, PR metadata and exact-head run/job inspection. Native cadence counts only first-attempt `event=schedule` runs on master. Manual, push, pull_request, workflow_run, repository_dispatch and reruns are not substitutes.

### Direct repository refs and open PRs

| Repository | Verified master SHA | Open PRs | Latest verified app CI / deployment evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `99509adbffb3888ac5bee59042c28292e5010919` | #1653 plus #1314/#544/#541/#539 owner-decision drafts | Master validation #43094091607 PASS. PR #1653 exact head `fb06a347831c5c814f3232a6c56b6694b6c73afc`, base `99509adb`, remains open/mergeable. Exact-head validation #43095467009 has been queued since 20:20:41Z; latest GET shows status=queued and its jobs collection is empty. Earlier queued validations are for superseded commits; older completed successes are not exact-head evidence. |
| phanthienquoc/TCE-dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | none | WF-06 manual #43088897948 FAIL (four HTTP 503); latest native WF-06 #43073311537 FAIL; latest native WF-12 #43068077606 FAIL; WF-12 workflow_run #43088836266 FAIL; WF-13 workflow_run #43088861304 SUCCESS but its log showed `TCE_MAINTENANCE_MODE` empty; WF-07 integration schedule #43088811861 PASS (not WF-06/WF-12 health). |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS. Scraper schedule #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. Latest successful image publication in the retrieved run window is #41563856933 (2026-11-03, older source SHA); no current-master publication or promotion is evidenced. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. Latest successful WF-03 publication in the retrieved run window is #41158598649 (2026-10-31, older source SHA); no current-master publication or Platform handoff is evidenced. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner-decision draft | CI #42654579277 PASS. Latest successful release #41040510320 (2026-10-30, older source SHA); no current-master release/handoff is evidenced. |

### Current native schedule freshness — reference 21:02:52Z

| Lane | Latest qualifying native run | Previous | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile-vps.yml | #43066718643 | #42993779924 | 13,520 | 28,867 | 2,700 |
| Platform inspect-vps.yml | #43054529460 | #42981286761 | 17,947 | 30,159 | 4,500 |
| Platform recover-stale-ops.yml | #43058316157 | #42986496462 | 16,597 | 29,036 | 2,700 |
| Platform reconcile-schedule-watchdog | #43058640134 | #42986833403 | 16,476 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 11,046 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 13,027 | 28,287 | 1,500 |

All 6/6 current-age budgets and 6/6 inter-arrival budgets fail. TCE WF-06 and WF-12 latest qualifying native runs are both failures. WF-07 integration success, WF-13 workflow_run success, manual WF-06 runs and rerun attempts do not reset native schedule age. Preserve all cron expressions and the TCE market-scan schedule.

### Runtime evidence freshness and interpretation

- Latest full K3s inspection #43089176130 generated its snapshot at 19:39:15Z. At 21:02:52Z age=5,017s, exceeding the 4,500s budget by 517s. It is historical only; no current workload-health or decommission decision may rely on it.
- Last successful reconciliation #43088879697 ran at 19:37:08Z on parent SHA `9093831c`, `mode=apply`, target=all, image changes=false. At 21:02:52Z age=5,144s, exceeding the 2,700s budget by 2,444s. Historical results: five GHCR package reads PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; drift=false; manifest apply/image replacement/rollout skipped. It is not current-master authorization.
- Last-known K3s state from #43089176130: Media backend/frontend 1/1; MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock desired Admin (two pods) and Backend (one pod) ImagePullBackOff on `12d63b4`; separate `k3s-debug/k3s-debug-logs` PVC 1Gi Bound/RWO. Media runner service was active/enabled with Listener present. Because the snapshot is expired, all of these are last-known observations, not current assertions.
- Stock/Media decommission scope is approved and GitOps ownership retirement is merged. K3s namespace deletion remains blocked by missing fresh same-run preflight, external backup/retention evidence, authoritative DNS evidence and proof that the dedicated Media runner is stopped/disabled/unregistered. Preserve the separate debug PVC and all TCE/Auth/MicroFE/Keycloak resources.
- WF-13 #43088861304 logged an empty `TCE_MAINTENANCE_MODE`; the workflow maps empty to `enabled=false`. The current repository variable value is not readable through this integration. Do not infer the current setting from that historical run.
- The latest PR #1653 exact-head validation #43095467009 is queued (created 20:20:41Z; ~42 minutes old at this reference) with no jobs assigned/returned. Seven recent validation attempts for successive PR commits are queued; older successful validations target superseded heads. This establishes an Actions queue delay, not its root cause.

### Exact next actions and safety

1. Platform operator: obtain a fresh read-only `inspect-vps.yml` run; the previous full snapshot is expired.
2. Platform operator: dispatch `reconcile-vps.yml` on current master `99509adb` with `mode=plan`; do not apply based on the expired parent-SHA reconciliation.
3. Platform CI/GitHub administrator: investigate why exact-head `validate-manifests` #43095467009 remains queued with no job; do not merge PR #1653 until an exact-head run completes successfully.
4. TCE administrator: verify the current repository variable; set `TCE_MAINTENANCE_MODE=true` only for an approved zero-replica maintenance window, otherwise restore service replicas. Keep strict HTTP-200 probes.
5. Media operator/decommission owner: provide external backup/retention and authoritative DNS evidence; stop/disable the dedicated runner and verify both local Listener absence and GitHub-side registration removal; then run the protected same-run `mode=plan` before any delete.
6. GitHub administrator: enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only across all five repositories.

No workflow dispatch, new GHCR publication, digest promotion, production apply, workload rollout, namespace/PVC/PV deletion, runner stop/unregister, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred in this refresh. The current GitHub connector exposes read operations but no workflow-dispatch action. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.


## Previous compact snapshot — 2026-11-12 03:12 ICT

### Repository readiness — direct master refs verified at 20:11:03 UTC

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `99509adbffb3888ac5bee59042c28292e5010919` | #1314/#544/#541/#539 (owner-decision drafts), #1653 (docs validation) | Inspection PR #1649 merged at `3e6d3f48`; readiness PR #1650 merged at parent `31b1245c`; post-merge sync PR #1651 merged at this SHA after exact-head validation #43093685819 PASS and post-merge master validation #43093772516 PASS. PR #1651 added direct branch-protection/ruleset evidence and source-level publisher audit; no production manifests changed. Reconciliation #43088879697 SUCCESS on parent `9093831c`, `mode=apply`, target=all, image changes=false: 5 GHCR package read preflight PASS; Auth runtime Secret provisioned/verified (values suppressed); shared `ghcr-pull` unchanged; blocked-image-pull checks clear for MicroFE/TCE; TCE release pairing PASS; GitOps drift=false; manifest apply/image replacement/rollout skipped. PR #1649 changed only `debug/vps-latest.md`, so production manifests are unchanged since reconciliation. |
| phanthienquoc/TCE-dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | none | Latest manual WF-06 #43088897948 FAIL: all four strict public HTTP-200 probes returned 503. Latest native WF-06 schedule #43073311537 FAIL; native WF-12 #43068077606 FAIL. Latest WF-12 workflow_run #43088836266 FAIL on stale WF-06 delivery; WF-13 fallback #43088861304 SUCCESS is workflow_run, not native schedule evidence. WF-07 integration schedule #43088811861 PASS. WF-13 #43088861304 job log shows `TCE_MAINTENANCE_MODE` resolved empty; current master maps empty to `enabled=false`, so maintenance suppression was not enabled in that run. It dispatched read-only fallback #43088897948; current repository variable value after that run remains inaccessible to this integration. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Current full K3s snapshot shows two desired Admin pods and one desired Backend pod in ImagePullBackOff for tag `12d63b4`, with no registry RepoDigest/compatible ARM64 descriptor; legacy Backend/Frontend are running old `23b2878` but have no registry RepoDigest. Stock/Media GitOps ownership retirement is merged and the approved scope is decommission, not restoration. Keep Stock publication/promotion blocked; K3s deletion is gated by external backup/retention and DNS evidence, Media runner stop/disable/unregister plus read-only audit, a fresh same-run plan and protected production approval. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. Current K3s snapshot shows residual backend/frontend pods 1/1 with RepoDigests `sha256:93ddb944…` / `sha256:095c72ed…`; Media runner service/listener remains active. Active Platform manifest tree has no retired Stock/Media references, but residual cluster workloads and runner remain; backup/retention, authoritative DNS and remote runner unregister are unverified. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | CI #42654579277 PASS. Auth runtime Secret was provisioned/verified by reconciliation #43088879697 with values suppressed. Auth deployment is intentional 0/0 maintenance; HTTPS/TLS verification PASS, but no live Auth workload health is asserted. |

## Current runtime and native-schedule evidence — reference 2026-11-11 20:11:03 UTC

Only first-attempt `event=schedule` runs on `master` count for native cadence. Manual, push, pull_request, workflow_run, repository_dispatch and rerun attempts do not substitute.

| Lane | Latest qualifying native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #43066718643 | #42993779924 | 10,411 | 28,867 | 2,700 |
| Platform inspection | #43054529460 | #42981286761 | 14,838 | 30,159 | 4,500 |
| Platform recovery | #43058316157 | #42986496462 | 13,488 | 29,036 | 2,700 |
| Platform watchdog | #43058640134 | #42986833403 | 13,367 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 7,937 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 9,918 | 28,287 | 1,500 |

All six current-age budgets and all six inter-arrival budgets fail at this reference. WF-06 #43073311537 is the latest qualifying native schedule run; later WF-06 #43088897948 is manual and does not reset schedule age. WF-12 #43068077606 is the latest qualifying native schedule run; #43088836266 is workflow_run. The latest WF-12 log measured latest scheduled WF-06 #43073311537 at 5,886s (98m) old at its 19:36:52Z reference and reported queue=0m, so the sample does not indicate runner congestion. Keep all cron expressions and the TCE market-scan schedule unchanged.

## Latest directly inspected workflow evidence

| Repository / workflow | Run | Event / result | Notes |
|---|---:|---|---|
| Platform inspect-vps | #43089176130 | workflow_dispatch / SUCCESS | Generated full snapshot at 2026-11-11T19:39:15Z; merged inspection-only PR #1649. |
| Platform validate-manifests | #43089441872 | workflow_dispatch / SUCCESS | Exact inspection PR head validation; all 20 validation steps PASS. Not a separate post-merge master run. |
| Platform reconcile-vps | #43088879697 | workflow_dispatch / SUCCESS | Parent SHA `9093831c`, mode=apply, target=all, image changes=false; five-package GHCR preflight PASS; Auth Secret verified; shared pull Secret unchanged; no manifest drift; apply/image replacement/rollout skipped. |
| Platform recover-stale-ops | #43089116141 | workflow_dispatch / SUCCESS | Manual recovery controller completed after reconciliation/inspection; not native schedule delivery. |
| Platform recovery/watchdog workflow_run | #43088925705 / #43088917353 | SKIPPED | Not native schedule evidence. |
| Platform native reconcile/watchdog | #43066718643 / #43058640134 | schedule / SUCCESS / FAILURE | Latest qualifying native runs; both outside freshness budgets. |
| TCE WF-06 | #43088897948 | workflow_dispatch / FAILURE | Four public endpoints returned HTTP 503 instead of 200. |
| TCE WF-12 | #43088836266 | workflow_run / FAILURE | Native WF-06 schedule delivery stale; heartbeat notification succeeded. |
| TCE WF-13 | #43088861304 | workflow_run / SUCCESS | Job log shows `TCE_MAINTENANCE_MODE` empty; current code maps empty to `enabled=false`, then dispatched read-only WF-06 fallback #43088897948. Not native schedule evidence. |
| TCE WF-07 integration | #43088811861 | schedule / SUCCESS | Integration schedule only; does not replace WF-06/WF-12 health lanes. |
| Stock CI / scraper | #42610360402 / #42457182511 | push / SUCCESS; schedule / FAILURE | Scraper remains fail-closed on missing `VNSTOCK_API_KEY`. |
| Media CI | #42539512417 | push / SUCCESS | App test/build passed; no new image publication. |
| Authentication CI | #42654579277 | push / SUCCESS | Validation and ARM64 build passed. |

### K3s / GitOps evidence

- Full read-only inspection #43089176130 generated `debug/vps-latest.md` at 2026-11-11T19:39:15Z. At the 20:11:03Z reference its age is 1,908s, within the 4,500s freshness budget with 2,592s remaining (expected expiry 20:54:15Z). It is a full current snapshot at this reference.
- Node `tce-k3s-01` was Ready/ARM64; Ubuntu 22.04.5; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; kernel 6.8.0-1049-oracle; disk 56% (~20GiB free); RAM ~19GiB available. Host reports restart required with kernel/containerd/Docker/OS updates pending. No reboot/upgrade.
- Last-known workload state: Media backend/frontend 1/1; MicroFE Shell/WS/NATS 1/1; TCE frontend/service, Auth and Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend (one pod) ImagePullBackOff for `12d63b4`; legacy Stock Backend/Frontend 1/1.
- Stock desired image failure is `no match for platform in manifest`; desired pods have no RepoDigest. Legacy Stock `23b2878` images have local image IDs but no registry RepoDigest, so they are not promotion evidence.
- Media backend/frontend RepoDigests: `sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d` and `sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a`. MicroFE Shell/WS and NATS also have registry RepoDigests in the snapshot. Auth and TCE images are cached, but their deployments are zero replicas; cached digests do not mean live workloads.
- Keycloak deployment is 0/0; both public OIDC discovery probes (`sso.mrcute.space/realms/master` and `/realms/mrcute`) returned HTTP 503. Auth host TLS verification passed separately, but Auth remains 0/0 maintenance and no live Auth health is asserted.
- Residual cluster resources remain in `stock-prod` and `media-prod` even though the active Platform production manifest tree has no retired Stock/Media namespace/image references. Media pods are still 1/1 and the Media runner service/listener is active; Stock desired pods still fail image pull. No namespace/PVC/PV or runner deletion was performed.
- Read-only Stock/Media decommission preflight reports no PVCs, PV claims or VolumeSnapshot references in `stock-prod`/`media-prod`; this is storage evidence only and does not authorize namespace/workload deletion. Preserve PVC `k3s-debug/k3s-debug-logs` (1Gi, RWO, local-path). Docker image data 9.195GB with 5.773GB reclaimable; no cleanup. Media runner service/listener is active/enabled/present; host inspection cannot infer GitHub runner registration. External backup/retention, authoritative DNS and remote runner unregister remain unverified.
- Reconciliation #43088879697 completed SUCCESS on parent SHA `9093831c`, mode=apply, target=all, image changes=false. GHCR read preflight passed five packages; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; `restart-blocked-image-pulls` found no failures in MicroFE/TCE scopes; TCE release pairing passed; GitOps drift=false; manifest apply, image replacement and workload rollout skipped. Auth HTTPS/TLS passed but Auth was 0/0 maintenance; TCE was 0/0 maintenance; MicroFE active-scope health passed; Keycloak lane skipped.
- PR #1649 changed only `debug/vps-latest.md` (one file; no production manifests), moving master from `9093831c` to `3e6d3f48`. Therefore the production manifest tree was unchanged after the successful reconciliation. No separate current-master `mode=plan` run exists; the GitHub connector can read/list Actions runs but does not expose a workflow-dispatch action.
- The manual reconciliation is 2,035s old at the reference, within the 2,700s reconciliation freshness budget with 665s remaining (expected expiry 20:22:08Z). No new apply is authorized by stale evidence after expiry; obtain a new read-only inspection and current-master plan before further production action.

### Stock/Media decommission execution state

- The approved objective is to remove StockDividend and Media Generation from Platform production ownership and delete only `stock-prod` and `media-prod` from K3s. GitOps ownership retirement is already merged; application repositories and their CI/test/security/immutable-publisher workflows remain intact.
- Protected `.github/workflows/decommission-stock-media.yml` is manual-only; `mode=plan` is the default and read-only. Delete mode requires the protected `production` Environment, exact namespace/backup/DNS/runner attestations, stable HTTPS backup and DNS evidence references, a same-run storage preflight, local Media service inactive and disabled/masked or absent, no `Runner.Listener`, and a read-only GitHub runner-list audit using `MEDIA_RUNNER_AUDIT_TOKEN`.
- Current full inspection #43089176130 reports no PVC/PV claims or VolumeSnapshot references in the two target namespaces, but they still contain Deployments, ReplicaSets, Services, Ingresses and namespaced Secrets. Preserve the separate `k3s-debug/k3s-debug-logs` PVC. Storage-clean is not external backup or deletion approval.
- The dedicated Media runner remains active/enabled with Listener present; remote registration is not inferred by host inspection. Therefore the delete gate is currently unsatisfied. External backup/retention, authoritative DNS ownership, audit-token availability and protected Environment approval remain outstanding. No plan/delete workflow run was invoked in this review because the current connector has no workflow-dispatch action.
- See [the controlled decommission plan](decommission/stock-media-k3s.md). Never stop the shared Platform runner or alter TCE/Auth/MicroFE/Keycloak or the TCE market-scan schedule.

### Governance and exact next actions

- Open owner-decision drafts: Platform #1314/#544/#541/#539 and Auth #76. Current docs PR #1653 is open; its final exact-head validation is queued. Merge only after a completed PASS on the current PR head. No open PRs in TCE/Stock/Media. Exact-head checks remain PASS: Platform #1314 #42161859747, #544 #38575430454, #541 #38567431761, #539 #38548718033; Auth #76 #41329425940 PASS with Supabase Preview skipped. Do not merge owner decisions solely because historical checks passed.
- Direct `GET /branches/master` returned `protected=false` for all five repositories. Branch-protection detail GET returned HTTP 403 for all five. `GET /rulesets?includes_parents=true` returned an empty array for Platform Infra, TCE Dashboard, Media Generation and Authentication; StockDividend returned HTTP 403 because GitHub rulesets require Pro or a public repository, so its inherited rulesets remain unverified. Repository metadata allows squash, merge commit and rebase on all five. This confirms all five master branches are unprotected at the branch API level; the administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.
- Platform operator: obtain a fresh read-only inspection before 20:54:15Z and run current-master `reconcile-vps.yml` with `mode=plan` on `3e6d3f48` before any apply decision. No workflow dispatch was fabricated.
- GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry; WF-12's latest sample reported queue=0m, so runner congestion is not established.
- TCE administrator: WF-13 #43088861304 logged `TCE_MAINTENANCE_MODE` empty; current workflow code maps empty to `enabled=false` and dispatched fallback #43088897948. Set the repository variable to true only if the zero-replica maintenance window is approved; otherwise restore service replicas and keep strict HTTP-200 probes. The current setting after that run is not readable through this integration.
- TCE/Auth owners: decide maintenance vs reactivation and provide immutable release digests, rollback references and explicit recovery approval before Platform applies.
- Stock/Media decommission: approved scope is documented in `docs/decommission/stock-media-k3s.md`. The current snapshot proves the Media runner is active/enabled with Listener present, so delete mode is blocked. Run the protected workflow in `mode=plan`, provide external backup/retention and authoritative DNS evidence, stop/disable/unregister the dedicated Media runner and verify absence with `MEDIA_RUNNER_AUDIT_TOKEN`, then use delete mode only with exact attestations and production Environment approval. Preserve app repositories and their CI/publisher workflows.
- Media owner: complete external backup/retention, authoritative DNS ownership and remote runner stop/disable/unregister evidence before decommission.
- Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new app image publication/digest promotion, new GitOps plan/apply, manifest apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred in this checkpoint. Historical reconciliation #43088879697 did provision/verify the Auth runtime Secret; shared `ghcr-pull` was unchanged. Preserve useful CI/test/security, immutable publishers, release, backup, integration, manual and scheduled workflows; none is confirmed obsolete. No direct SSH/Compose authority. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

## Historical verification — 2026-11-11 15:09 ICT / 08:09:56 UTC

This is the current compact snapshot. Only first-attempt `event=schedule` runs on `master` count for native cadence. Manual, push, workflow_run and repository_dispatch receipts do not substitute.

### Direct repository state and open PRs

- Direct `refs/heads/master`: Platform Infra `48c9cf344c40fb76b1c720149d67bbced29e9255`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314 head `db152c9a17416d1a7f82165597dfe478321bd055`, #544 `c95e7daecb83b65577b54303427fe4ea81adfe06`, #541 `b8f7c6ba04e3d971336a899b2efd5894662083b3`, #539 `2dc48b97017ecb08e49682633303a2f1d5e991a1`; Authentication #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`. No open PRs in TCE, Stock or Media. All five open PRs remain drafts/owner decisions.
- Last exact-head checks still attached to unchanged PR heads: Platform #1314 #42161859747 PASS; #544 #38575430454 PASS; #541 #38567431761 PASS; #539 #38548718033 PASS; Auth #76 #41329425940 PASS (Supabase Preview skipped). Do not merge owner-decision work solely because checks pass.

### Latest workflow evidence

- Platform native inspection [#42981286761](https://github.com/phanthienquoc/platform-infra/actions/runs/42981286761) completed SUCCESS on master SHA `4b22409c...`; it created inspection PR #1620, whose exact-head validation step passed and whose squash merge produced current master `48c9cf34...`. The inspection-only branch validation #42981497429 passed; it is not a separate post-merge master validation.
- Platform manual reconciliation [#42981589486](https://github.com/phanthienquoc/platform-infra/actions/runs/42981589486) completed SUCCESS at 07:43:36Z on current master, `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE service/web. Auth runtime Secret provision/verification succeeded with values suppressed; shared `ghcr-pull` was unchanged. TCE release pairing passed for `prod-v0.1.0-e75e338`; desired/live images matched. GitOps drift=false, manifest apply skipped, image replacement skipped. TCE/Auth were explicitly classified as intentional zero-replica maintenance; no live workload health was asserted. Media and MicroFE core workloads were healthy; Stock Admin/desired Backend still had ImagePullBackOff pods.
- Platform recovery [#42981775331](https://github.com/phanthienquoc/platform-infra/actions/runs/42981775331) completed SUCCESS as workflow_dispatch. Logs confirmed the reconciliation was recent and native inspection #42981286761 was fresh; no duplicate reconciliation or inspection fallback was dispatched. This does not satisfy native cadence.
- Platform schedule watchdog #42981569803 failed because native reconcile/recovery/watchdog and inter-arrival evidence were stale. Its runner-queue sample found no scheduled lane over the 15-minute queue budget; GitHub scheduler enqueue/delivery timestamps remain unavailable.
- TCE native WF-06 #42949191917 and WF-12 #42944415193 failed/stale. Manual WF-06 #42972014911 failed all four strict HTTP 200 probes (TCE web, TCE API, Auth liveness, Auth readiness returned 503). TCE/Auth 0/0 maintenance is consistent with these 503s; do not relax the health contract or call maintenance healthy. WF-07 integration schedule #42971954835 passed but is not a health-lane substitute.
- Stock CI #42610360402 passed; scraper schedule #42457182511 failed closed because `VNSTOCK_API_KEY` was empty. Do not put secrets in Git/logs/chat or publish Stock images while retirement scope remains approved. Media CI #42539512417 passed. Authentication CI #42654579277 passed.

### Native schedule freshness

Reference: 2026-11-11 08:09:56 UTC. Age is measured from each latest run's `created_at`; inter-arrival is between the latest and previous native runs of the same workflow.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 22596 | 14244 | 2700 |
| Platform inspection | #42981286761 | #42932368784 | 1730 | 25617 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 24079 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 23403 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 18915 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 21441 | 13126 | 1500 |

All six inter-arrival gaps exceed budget. Five of six current-age checks fail; only Platform inspection current age passes. Platform native reconcile/recovery/watchdog and both TCE health lanes remain stale. The latest inspection run is fresh but its 25,617s inter-arrival gap still fails. Do not change cron, freshness budgets or the TCE market-scan schedule.

### K3s inspection and GitOps runtime

- Fresh read-only inspection [#42981286761](https://github.com/phanthienquoc/platform-infra/actions/runs/42981286761) generated `debug/vps-latest.md` at 07:41:14Z. At reference it is 1,722s old, within the 4,500s budget (2,778s remaining). Node `tce-k3s-01` Ready, ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% / about 20 GiB free; about 19 GiB RAM available. Host reports `restart_required=yes` and package/kernel updates pending. Do not reboot or upgrade without a maintenance window.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running. TCE/Auth/Keycloak remain 0/0 maintenance. Stock Admin has two ImagePullBackOff pods; desired Stock Backend has one ImagePullBackOff pod; legacy Backend and Frontend are 1/1. Historical Stock tag `12d63b4` still lacks a compatible ARM64 descriptor; do not substitute local image IDs for registry RepoDigest.
- Pod image evidence includes registry digests for Media backend/frontend and MicroFE Shell/WS. Stock failed-pull pods have no resolved RepoDigest; legacy Stock pods have local image IDs only and are not promotion evidence. Media runner service/listener is active/enabled; remote unregister, external backup/retention and authoritative DNS ownership remain unverified.
- Reconciliation #42981589486 is 1,580s old at reference, within its 2,700s freshness budget. It verified GHCR read access and Auth Secret, found no GitOps drift, and skipped manifest apply/image replacement. Shared `ghcr-pull` remained unchanged. No workload rollout was required by the no-drift result. Treat TCE/Auth maintenance as not healthy.

### Branch governance and next actions

- Last direct governance evidence (12:58 ICT) reported `protected=false` on all five master branches and repository metadata allowed squash, merge commits and rebase. No administrator remediation is evidenced in this run; inherited ruleset enforcement remains unverified because branch-protection detail reads are denied by the integration.
- GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry; enforce PR-only, required checks, force-push/deletion protection and squash-only merge on all five repositories.
- Platform operator: keep the fresh inspection within budget; obtain a new read-only inspection before it expires if no native inspection arrives. No reboot/upgrade without approval.
- TCE/Auth owners: decide whether to reactivate maintenance scopes; if approved, provide immutable release digests, rollback references and explicit recovery approval before Platform applies.
- Stock owner: confirm continued retirement vs service restoration. If retirement remains, do not publish/restore Stock; complete backup/retention and DNS evidence. If service is restored by owner decision, provision `VNSTOCK_API_KEY` only through Actions Secrets and use safe preflight first.
- Media owner: complete external backup/retention, DNS ownership and remote runner stop/disable/unregister evidence before namespace deletion.
- Registry administrator: verify GHCR server-side immutable-tag enforcement.

No image publication, digest promotion, manifest change, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint. Auth runtime Secret provisioning/verification ran successfully; shared `ghcr-pull` was unchanged. Preserve useful workflows; none is confirmed redundant/obsolete. No direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 15:18 ICT / 08:18 UTC

- PR #1621 was squash-merged at `9c2e4e0efb54aad29bcdb82afeaf06c187c60499`; direct `refs/heads/master` reads match this SHA.
- Exact-head `validate-manifests` #42985848211 PASS on PR head `d8066977e9c9af2826d57e254dea04225b050718`.
- Post-merge `validate-manifests` #42985958377 PASS on master SHA `9c2e4e0e...`; retired Stock/Media guard, immutable image-change contract, Auth digest promotion, TCE/Auth dispatch payload, manifest rendering, Secret policy, Keycloak isolation and network boundaries passed. Changed-image reference validation was skipped because this was documentation-only.
- The post-merge run list contains only `validate-manifests`; no `reconcile-vps.yml` or `recover-stale-ops.yml` push run was triggered by this documentation-only merge.
- The 15:09 ICT operational checkpoint preserves Platform master `48c9cf34...` and its runtime/schedule reference time. This addendum advances the compact current master SHA only; it does not refresh runtime or schedule evidence.
- No production manifest, image, Secret, workload, DNS, database, storage, namespace or runner was changed by PR #1621. TCE market-scan schedule unchanged.

## Latest verification — 2026-11-11 15:25 ICT / 08:25:10 UTC

This snapshot supersedes the 15:09 operational snapshot for native schedule and Platform runtime evidence. Only first-attempt `event=schedule` runs on `master` count for cadence; manual/workflow_run/repository_dispatch receipts do not substitute.

### Direct refs, open PRs and checks

- Direct master refs: Platform Infra `c811ed79f22505c074eaa9b08b0e8a61e59db08a`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. All are drafts/owner decisions. Last exact-head checks on unchanged heads remain PASS: Platform #1314 #42161859747, #544 #38575430454, #541 #38567431761, #539 #38548718033; Auth #76 #41329425940 PASS (Supabase Preview skipped).
- PR #1623 squash-merged at current master `c811ed79...`; exact-head validation #42986594992 PASS and post-merge master validation #42986698420 PASS. Only `validate-manifests` ran after the docs-only merge; no production reconcile/recovery push was triggered by PR #1623.

### Latest Platform workflow evidence

- Native inspection #42981286761 SUCCESS; it generated inspection PR #1620, merged to `48c9cf34...`. `debug/vps-latest.md` was generated 07:41:14Z.
- Native recovery #42986496462 SUCCESS at 08:22:19Z on pre-docs master `8f95ddd8...`; its inter-arrival gap remains 24,822s (over 2,700s).
- Native watchdog #42986833403 FAILED at 08:24:50Z on current master `c811ed79...`. Logs confirm scheduled inspection #42981286761 and recovery #42986496462 completed; the runner queue sample found no scheduled deployment lane over 15 minutes. The watchdog failed on stale scheduled reconciliation and native inter-arrival gaps, not a demonstrated runner-queue delay.
- Manual reconciliation #42986517013 SUCCESS at 08:22:28Z on pre-docs master `8f95ddd8...`, `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE service/web. Auth runtime Secret provision/verification passed with values suppressed; shared `ghcr-pull` was unchanged. TCE release pairing passed for `prod-v0.1.0-e75e338`; desired/live images matched. GitOps drift=false; manifest apply and image replacement skipped. The managed image-pull restart helper found no failures for MicroFE/Auth/TCE; no managed workload restart was triggered. TCE/Auth were explicitly classified as zero-replica maintenance; no live health asserted. Media/MicroFE core workloads healthy; Stock Admin/desired Backend still ImagePullBackOff.
- Recovery #42986712253 SUCCESS at 08:23:56Z on current master `c811ed79...`. It verified reconciliation #42986517013 was recent and native inspection #42981286761 was fresh; no duplicate reconciliation or inspection fallback dispatch was issued.

### Latest app workflow evidence

- TCE native WF-06 #42949191917 and WF-12 #42944415193 remain failed/stale. Manual WF-06 #42972014911 showed all four strict HTTP 200 probes (TCE web, TCE API, Auth liveness, Auth readiness) returning 503. Current K3s state still classifies TCE/Auth as 0/0 maintenance; preserve strict health contract and do not call maintenance healthy. WF-07 integration schedule #42971954835 passed but is not a health-lane substitute.
- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Stock remains in approved retirement scope; do not publish/restore without owner reversal.
- Media CI #42539512417 PASS; backend/frontend 1/1 with registry-resolved digest references; dedicated runner remains active/enabled.
- Authentication CI #42654579277 PASS; Auth remains 0/0 maintenance; runtime Secret verified by #42986517013.

### Native schedule freshness

Reference: 2026-11-11 08:25:10 UTC. Age is measured from latest run `created_at`; gap is between the latest and previous native runs of the same workflow.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 23510 | 14244 | 2700 |
| Platform inspection | #42981286761 | #42932368784 | 2644 | 25617 | 4500 |
| Platform recovery | #42986496462 | #42939222343 | 171 | 24822 | 2700 |
| Platform watchdog | #42986833403 | #42940581820 | 20 | 24297 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 19829 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 22355 | 13126 | 1500 |

All six inter-arrival gaps fail. Three of six current-age budgets fail (Platform reconcile and both TCE health lanes); inspection, recovery and watchdog current ages are within budget. The successful recovery/watchdog receipts do not cure their inter-arrival gaps. Keep all cron expressions, freshness budgets and TCE market-scan schedule unchanged.

### K3s inspection and freshness

- Latest read-only inspection #42981286761 generated `debug/vps-latest.md` at 07:41:14Z; age 2,636s at reference, within the 4,500s budget (1,864s remaining). Node `tce-k3s-01` Ready/ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% / ~20 GiB free; ~19 GiB RAM available. Host `restart_required=yes` and kernel/package updates pending; no reboot/upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1 Running. TCE/Auth/Keycloak 0/0 maintenance. Stock Admin has two ImagePullBackOff pods; desired Stock Backend has one ImagePullBackOff pod; legacy Backend/Frontend 1/1. Historical Stock tag `12d63b4` still lacks compatible ARM64 descriptor; local image IDs are not RepoDigest evidence.
- Media runner service/listener active/enabled. Remote unregister, external backup/retention and authoritative DNS ownership remain unverified. Preserve bound `k3s-debug/k3s-debug-logs` PVC.

### Governance, next actions and safety

- Last direct governance evidence (12:58 ICT) reported `protected=false` for all five master branches and repository metadata allowed squash, merge commits and rebase. No administrator remediation is evidenced; inherited ruleset enforcement remains unverified.
- GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry; enforce PR-only, required checks, force-push/deletion protection and squash-only merge.
- Platform operator: refresh read-only inspection before its 4,500s budget expires; do not reboot/upgrade without a maintenance window.
- TCE/Auth owners: keep maintenance until explicit reactivation approval, immutable release digests and rollback references are provided.
- Stock owner: confirm retirement vs restoration; no publication while retirement remains approved. If restored, provision `VNSTOCK_API_KEY` through Actions Secrets and run safe preflight.
- Media owner: complete backup/retention, DNS ownership and remote runner stop/disable/unregister evidence.
- Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new image publication, digest promotion, manifest apply, image replacement, managed workload restart/rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. Auth runtime Secret provision/verification succeeded; shared `ghcr-pull` was unchanged. Preserve useful workflows; none is confirmed redundant/obsolete. No direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Historical verification — 2026-11-11 12:58 ICT / 05:58:04 UTC

Direct refs: Platform `b88399f0b593f3e336db4d28b38d364c99215ce3`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Auth `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.

Open PRs: Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. All remain drafts/owner decisions. Exact-head validations remain PASS; Auth Supabase Preview skipped.

Latest workflow evidence: Platform #42963960326 (master `b88399f0...`) validate-manifests PASS. TCE manual WF-06 #42949231253 and native WF-06 #42949191917 failed four strict HTTP 200 probes (all 503); WF-12 #42944415193 failed. Stock CI #42610360402 PASS; scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`. Media CI #42539512417 PASS. Auth CI #42654579277 PASS.

| Native lane | Latest run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | 14684 | 14244 | 2700 |
| Platform inspection | #42932368784 | 19435 | 17791 | 4500 |
| Platform recovery | #42939222343 | 16167 | 13889 | 2700 |
| Platform watchdog | #42940581820 | 15491 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | 11003 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | 13529 | 13126 | 1500 |

All six current-age and inter-arrival checks fail. Latest Platform schedule runs predate current Platform master. Do not count manual/workflow_run fallback receipts or alter cron/freshness budgets/TCE market-scan schedule.

K3s: latest read-only fallback #42942360712 is workflow_dispatch, created 01:55:12Z; embedded snapshot generated 01:55:21Z and is 14563s old, beyond 4500s. Native inspection #42932368784 is 19435s old. Native reconciliation #42942147668 is 14684s old; manual reconciliation #42949244537 is 10974s old. All are stale. Last-known node was Ready ARM64, K3s v1.36.3+k3s1, disk 56% / ~20 GiB free, ~19 GiB RAM; host restart required. Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`. Do not treat this as live health.

Native reconciliation #42942147668 used `mode=apply`, `target_app=all`, image changes disabled. Shared `ghcr-pull` unchanged; managed MicroFE/TCE image-pull checks clean; TCE release pairing `prod-v0.1.0-e75e338`; GitOps drift=false. Manifest/credential patches returned no change; no image replacement or workload rollout evidenced. Final gate: MicroFE healthy, TCE/Auth maintenance, Keycloak skipped.

TCE WF-06 #42949231253 decoded logs confirm TCE web, TCE API, Auth liveness and Auth readiness all HTTP 503 vs expected 200. Root cause not established because upstream response body was not surfaced. Stock scraper failure is fail-closed on empty `VNSTOCK_API_KEY`; do not put secrets in Git/logs/chat.

Branch governance: direct `GET /branches/master` reports `protected=false` for all five repositories. Metadata for all five reports squash=true, merge_commit=true and rebase=true. Branch-protection detail GET returns HTTP 403 through this integration, so inherited org ruleset enforcement is not positively established. Administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.

Next actions: Platform operator obtains fresh read-only `inspect-vps.yml`; GitHub administrator supplies scheduler enqueue/delivery telemetry and configures branch/ruleset/merge settings; TCE/Auth owners diagnose 503 and supply approved immutable digest plus rollback reference; Stock owner decides retain vs retire and, only if retained, provisions `VNSTOCK_API_KEY` via Actions Secrets and runs safe preflight; Media owner supplies backup/retention, DNS and remote runner unregister evidence; registry administrator verifies server-side GHCR immutable-tag policy.

No new image publication, digest promotion, effective production manifest change, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint. Preserve all useful workflows; none is confirmed obsolete. No direct SSH/Compose authority. TCE market-scan schedule unchanged.




## Post-merge verification — 2026-11-11 13:03 ICT / 06:03:28 UTC

- PR #1616 was squash-merged at `14e79f1c90f8390636f13a06a899c0de0ab85bd0`; direct `refs/heads/master` reads match the merge SHA.
- Exact-head validation #42969674108 PASS for head `a6a015607dfeea1da64b012be53ddc9e71068d63`.
- Post-merge `validate-manifests` #42969724857 PASS on master SHA `14e79f1c...`; failure-report job skipped by design.
- The post-merge run list contains only `validate-manifests`; no `reconcile-vps.yml` or `recover-stale-ops.yml` push run was triggered by this documentation-only merge.
- The 12:58 ICT checkpoint preserves pre-merge Platform SHA `b88399f0...` as a timestamped snapshot; this addendum advances the compact current SHA only.
- No production manifest, image, Secret, workflow, workload, DNS, database or cluster resource was changed. TCE market-scan schedule unchanged.

## Open PRs and exact-head checks

- Platform #1314: head `db152c9a17416d1a7f82165597dfe478321bd055`; validation run #42161859747 PASS; draft managed-mail plan remains owner decision.
- Platform #544: head `c95e7daecb83b65577b54303427fe4ea81adfe06`; validation run #38575430454 PASS; Keycloak activation remains secret/DNS/owner gated.
- Platform #541: head `b8f7c6ba04e3d971336a899b2efd5894662083b3`; validation run #38567431761 PASS; Keycloak database plan remains owner decision; no DB mutation.
- Platform #539: head `2dc48b97017ecb08e49682633303a2f1d5e991a1`; validation run #38548718033 PASS; identity architecture remains an unapproved draft.
- Authentication #76: head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; CI run #41329425940 PASS; Supabase Preview remains skipped; migration drift plan remains owner decision.
- No open PRs in TCE, Stock or Media. All listed PRs remain drafts; do not merge owner-decision work solely because checks pass.

## Recent Platform changes and reconciliation evidence

- Direct Git ref reads at 01:05:25Z confirm current master SHAs: Platform `010558ada7c36738a287ed38ae107d260f63ebf9`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1607 was generated by native scheduled inspection #42932368784 and squash-merged at `0faec01a5ad0f7c7349a1dd9d22750e80d32756f`. It changed only `debug/vps-latest.md`; exact-head inspection validation passed. PR #1608 then refreshed readiness and Stock/Media retirement evidence, merging at `010558ada7c36738a287ed38ae107d260f63ebf9`. Its master push run #42935987763 (validate-manifests) completed SUCCESS at 01:02:54Z. No production reconcile/recovery push run was created by the docs-only PR.
- Fresh read-only inspection #42932368784 completed at 00:36:22Z; `debug/vps-latest.md` was generated at 00:34:17Z. At the 01:05:25Z reference the snapshot age is 1,868s, within the 4,500s inspection budget (2,632s remaining). No new inspection dispatch is required yet; obtain another read-only snapshot before 01:49:17Z if no native inspection arrives.
- Manual reconciliation [#42932691349](https://github.com/phanthienquoc/platform-infra/actions/runs/42932691349) ran at 00:36:34Z with `mode=apply`, `target_app=all`, and image changes disabled. GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE service/web. Auth runtime Secret was provisioned and verified with values suppressed. Shared `ghcr-pull` remained unchanged. Managed MicroFE/TCE image-pull checks found no failures; TCE desired/live release pairing passed. Kubernetes diff was clean, so manifest apply, image replacement and rollout were correctly skipped. This is a workflow_dispatch run, not native schedule delivery.
- Reconciliation's final cluster listing still showed two Stock Admin pods and one desired Stock Backend pod in ImagePullBackOff. The managed pull helper covers MicroFE/TCE, not the retired Stock namespace. Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. TCE/Auth/Keycloak remained 0/0 maintenance; the inspection's public OIDC probes returned 503.
- Recovery [#42932880278](https://github.com/phanthienquoc/platform-infra/actions/runs/42932880278) completed successfully as workflow_dispatch for source reconciliation #42932691349. Logs verified the source run had completed, found the reconciliation recent and native inspection #42932368784 fresh, and therefore dispatched neither a duplicate reconciliation nor inspection. This receipt does not count as a native schedule run.
- Schedule watchdog run #42932671708 (workflow_run) failed on stale native reconcile/recovery evidence and inter-arrival gaps; the separate recovery workflow_run #42932671734 succeeded. Neither changes native schedule freshness.
- Prior Platform changes remain: PR #1601 removed manual image-change bypass; PR #1603 excluded recursive Keycloak Markdown from reconcile/recovery push triggers and made resolver-only changes fail closed; PR #1605 refreshed readiness; PR #1606 corrected recovery receipt wording. The earlier Keycloak README push side effect #42920184478 remains recorded as historical; pre-scale replica state was not captured.

## Native schedule freshness

Reference time: 2026-11-11 01:05:25 UTC (08:05:25 ICT). Only first-attempt event=schedule runs on master count for cadence acceptance. Inter-arrival is measured from the previous native run of the same workflow.

| Lane | Latest native run | Previous native run | Latest created UTC | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42909757881 | #42854065227 | 2026-11-10 21:55:56 | 11369 | 19941 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 2026-11-11 00:34:09 | 1876 | 17791 | 4500 |
| Platform recovery | #42906791198 | #42848981485 | 2026-11-10 21:37:08 | 12497 | 20656 | 2700 |
| Platform watchdog | #42908417737 | #42850178931 | 2026-11-10 21:47:23 | 11882 | 20852 | 2700 |
| TCE WF-06 | #42922537816 | #42872071366 | 2026-11-10 23:20:28 | 6297 | 18739 | 1500 |
| TCE WF-12 | #42915709227 | #42867304730 | 2026-11-10 22:33:49 | 9096 | 17617 | 1500 |

All six inter-arrival gaps exceed budget. Five of six current-age checks exceed budget; only Platform inspection current age is within the 4,500s budget. Its inter-arrival gap still fails. TCE WF-06 native run #42922537816 and manual run #42922596353 both failed all four strict HTTP 200 endpoint checks (HTTP 503); WF-12 #42915709227 failed freshness. TCE WF-07 backup #42924677977 succeeded but is not a substitute for either health lane. Heartbeats, workflow_run recovery and workflow_dispatch/repository_dispatch fallbacks never substitute for native schedule delivery.

The six cron expressions remain unchanged: Platform reconcile 7,22,37,52 * * * *; inspection 2,32 * * * *; recovery 10,25,40,55 * * * *; watchdog 12,27,42,57 * * * *; TCE WF-06 */15 * * * *; TCE WF-12 7,22,37,52 * * * *. Do not change cron, freshness budgets or TCE market-scan scheduling to hide delivery gaps.

## Current K3s runtime and decommission evidence

- Latest full read-only inspection [#42932368784](https://github.com/phanthienquoc/platform-infra/actions/runs/42932368784) generated `debug/vps-latest.md` at 00:34:17Z; age 1,868s at the 01:05:25Z reference (within the 4,500s budget). Host is ARM64 Ubuntu 22.04.5, uptime about 193 days 10h24m, 23 GiB RAM / 19 GiB available, root disk 45 GiB / 20 GiB free (56% used), `restart_required=yes`. K3s node `tce-k3s-01` Ready, v1.36.3+k3s1, containerd 2.3.2-k3s2. No host restart or package upgrade was performed.
- Media backend/frontend 1/1 with registry-resolved digest references. MicroFE Shell/WS/NATS 1/1. TCE frontend/service 0/0; Auth and Keycloak 0/0. Public OIDC discovery for both `master` and `mrcute` realms returned HTTP 503.
- Stock Admin has two 0/1 ImagePullBackOff pods and desired Backend one 0/1 ImagePullBackOff pod on historical tag `12d63b4`; kubelet reports `no match for platform in manifest`. Legacy Stock Backend/Frontend are 1/1 on `23b2878`, but cached GHCR tags lack RepoDigest evidence and are not promotion evidence.
- The repository's retired-manifest guard requires `apps/stockdividend` and `apps/media-generation` trees to be absent and rejects Stock/Media namespace or GHCR image references under `environments/prod`, `platform` and `apps`. The current repository tree has no retired Stock/Media manifest trees; PR #1606's post-merge validation #42929239138 passed. Stock/Media are therefore removed from the active Platform GitOps manifest scope, but their Kubernetes namespaces/workloads remain pending the separately gated decommission.
- Fresh inspection ran `scripts/decommission-stock-media-namespaces.sh plan`: `storage-clean`; no PVC, PV claim or VolumeSnapshot/VolumeSnapshotContent references in `stock-prod` or `media-prod`. Both namespaces remain Active. The separate `k3s-debug/k3s-debug-logs` PVC remains Bound and is outside the two target namespaces; it must be preserved.
- Media runner service/listener remains active, enabled and present. The host inspection cannot infer GitHub runner registration. Remote unregister, backup/retention for application and external DB/object-storage data, and authoritative DNS/provider ownership for every retired Ingress hostname remain unverified. The explicit `decommission-stock-media.yml` workflow plan mode has not been dispatched in this run; inspection executed its underlying read-only namespace/storage preflight.
- The delete workflow remains fail-closed: master ref; `production` environment; exact typed confirmations for namespace deletion, backup/external-data review, DNS ownership and Media runner retirement; HTTPS backup and DNS evidence references; local service stopped/disabled, listener absent and GitHub runner registration absent via scoped audit token; fresh storage preflight; then deletion of only `stock-prod` and `media-prod`. No delete-mode execution occurred.
- GitOps drift was clean. Shared GHCR credentials were unchanged. No namespace/PVC/PV deletion, runner stop/disable/unregister, DNS/database/object-storage mutation, credential rotation, host reboot or package upgrade occurred.
- `k3s-debug/k3s-debug-logs` is a separate bound PVC; do not delete it as part of Stock/Media retirement.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497): GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for all six schedule workflows. At 01:05:25Z all six inter-arrival gaps exceed budget; five current-age checks also fail.
2. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872): TCE/Auth owners must diagnose HTTP 503 and provide approved immutable release digests, rollback references and explicit recovery approval. Platform operator must obtain a maintenance window before host restart/upgrade.
3. Stock/Media decommission (user-approved scope): Platform operator/owners must complete external backup/retention and DB/object-storage ownership review, authoritative DNS/provider export for every retired Ingress host, and dedicated Media runner stop/disable/unregister. Then run `decommission-stock-media.yml` in `plan` mode and review output. Only after evidence and the production environment approval may an authorized operator use the exact delete confirmations. Do not delete the bound `k3s-debug` PVC.
4. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575): GitHub administrator must confirm effective PR-only, required-check, force-push and branch-deletion rulesets; current connector cannot verify inherited ruleset enforcement.
5. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42): `VNSTOCK_API_KEY` remains absent and scraper fails closed. This is not a reason to publish or revive Stock production while Stock is in the approved retirement scope.
6. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43): ARM64 publisher exists but no production publication/digest handoff; do not trigger it while Stock production is being retired.
7. Registry administrator must verify GHCR server-side immutable-tag policy. TCE owner must verify SSH host fingerprint before any SSH-based maintenance.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the single production apply authority; `inspect-vps.yml` remains read-only. Manual reconcile dispatch has no image-change override; only provenance-verified `gitops-promoted-ready` repository_dispatch may bypass the image guard.
- `decommission-stock-media.yml` is a separate, explicitly gated namespace retirement workflow; it is not a second deployment authority. It can delete only the two retired namespaces after exact confirmations, evidence, remote runner verification and a fresh storage preflight.
- Preserve useful CI/test/security workflows and purposeful manual/release/scheduled jobs. No workflow was removed or confirmed redundant/obsolete. Do not add direct SSH/Compose deployment authority.
- TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only tracker: `docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md`.
- Previous full append-only workflow inventory: `docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md`.
- Timestamped checkpoints: `docs/cross-repo-deployment-checkpoints/`.
- Workflow ownership and file inventory: `docs/cross-repo-workflow-inventory.md`.
- Schedule investigation: https://github.com/phanthienquoc/platform-infra/issues/1497
- TCE/Auth recovery: https://github.com/phanthienquoc/platform-infra/issues/872
- Branch governance: https://github.com/phanthienquoc/platform-infra/issues/1575
- Stock scraper credential: https://github.com/phanthienquoc/stockdividend/issues/42
- Stock ARM64 release: https://github.com/phanthienquoc/stockdividend/issues/43


## Historical verification — 2026-11-11 09:02 ICT / 02:02:00 UTC

- Direct master refs at this checkpoint: Platform Infra `fbb479fc7e6415eeec8ef34fdaccf039f5477e17`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Current open PRs from GitHub REST: Platform #1314 (`db152c9a`), #544 (`c95e7dae`), #541 (`b8f7c6ba`), #539 (`2dc48b97`); Authentication #76 (`f19cacb0`). All are drafts/owner-decision work. No open PRs in TCE, Stock or Media. Exact-head check-runs: Platform #1314/#544/#541/#539 each have `validate=success`; Auth #76 has `validate=success` and Supabase Preview `skipped`. Do not merge the Keycloak/database/identity or Auth migration-drift decisions without owner approval.
- Platform PR #1610 was generated from read-only inspection run #42942360712 (`workflow_dispatch`, completed success) and squash-merged at `fbb479fc7e6415eeec8ef34fdaccf039f5477e17`. It changed only `debug/vps-latest.md`. Exact-head `validate-manifests` run #42942563353 completed success on the inspection branch before merge. No separate post-merge master validation run was returned for the debug-only merge; do not represent the branch check as a post-merge check.
- Latest Platform run evidence: native scheduled reconcile #42942147668 at 01:53:20Z succeeded; native scheduled watchdog #42940581820 at 01:39:53Z failed on schedule freshness/inter-arrival acceptance; native scheduled recovery #42939222343 at 01:28:37Z succeeded; native scheduled inspection remains #42932368784 at 00:34:09Z. A newer manual inspection #42942360712 generated the fresh snapshot at 01:55:21Z but does not replace native inspection cadence. Exact-head inspection validation #42942563353 succeeded.
- Latest TCE native evidence: WF-06 #42922537816 at 23:20:28Z failed all four public endpoints (TCE web, TCE API, Auth liveness, Auth readiness: HTTP 503 vs required 200); WF-12 #42915709227 at 22:33:49Z failed freshness. WF-07 backup #42924677977 at 23:35:49Z succeeded but is not health or schedule-cadence evidence for WF-06/WF-12. Stock latest master CI #42610360402 passed; scheduled scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was empty. Media master CI #42539512417 passed. Authentication master CI #42654579277 passed.
- Native schedule reference: 2026-11-11 02:02:00Z. Only first-attempt `event=schedule` runs on `master` count. Platform reconcile #42942147668 / previous #42909757881: age 520s, gap 14,244s, budget 2,700s. Platform inspection #42932368784 / previous #42887151366: age 5,271s, gap 17,791s, budget 4,500s. Platform recovery #42939222343 / previous #42906791198: age 2,003s, gap 13,889s, budget 2,700s. Platform watchdog #42940581820 / previous #42908417737: age 1,327s, gap 13,950s, budget 2,700s. TCE WF-06 #42922537816 / previous #42872071366: age 9,692s, gap 18,739s, budget 1,500s. TCE WF-12 #42915709227 / previous #42867304730: age 12,491s, gap 17,617s, budget 1,500s. All six inter-arrival gaps fail; current-age checks pass only for Platform reconcile, recovery and watchdog. Manual inspection #42942360712 is fresh but not native schedule evidence. Do not change cron, freshness budgets or TCE market-scan schedule.
- Watchdog #42940581820 logs confirm the four Platform inter-arrival gaps (19,941s, 17,791s, 13,889s, 13,950s at its 01:39:53Z reference) and TCE WF-06/WF-12 gaps (18,739s and 17,617s). Its runner queue diagnostic reported no scheduled deployment lane above the 15-minute queue budget for the sampled reconciliation. This does not expose GitHub scheduler enqueue/delivery telemetry and does not explain the long gaps; GitHub administrator evidence remains required.
- Latest manual K3s inspection #42942360712 completed successfully; `debug/vps-latest.md` was generated at 01:55:21Z (age 399s at this checkpoint, within the 4,500s manual snapshot freshness budget). Node `tce-k3s-01` Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Ubuntu 22.04.5; uptime 193d 11h45m; 23 GiB RAM with 19 GiB available; root disk 45 GiB, 56% used / about 20 GiB free; `restart_required=yes`. Kernel/containerd/Docker and OS package updates are available; no upgrade/reboot was performed.
- Current inspected workload state: Media backend/frontend 1/1 with registry-resolved digest references; MicroFE Shell/WS/NATS 1/1; TCE frontend/service 0/0 maintenance; Auth and Keycloak 0/0 maintenance; Stock Admin two pods 0/1 ImagePullBackOff and desired Backend one pod 0/1 ImagePullBackOff on `12d63b4`; legacy Stock Backend and Frontend 1/1. Stock Admin/Backend image IDs are empty because pull failed; do not use local image IDs as registry digests. Kubelet's historical failure is `no match for platform in manifest`. Public OIDC discovery for both Keycloak realms returned HTTP 503.
- Inspection reports GitOps drift clean. Media runner service/listener remains active and enabled; GitHub runner registration is not inferred from host state. Stock/Media namespaces remain Active even though their production manifest trees/references are retired from active Platform GitOps. The read-only decommission preflight found no PVC/PV/VolumeSnapshot references in `stock-prod` or `media-prod`; preserve the separate Bound `k3s-debug/k3s-debug-logs` PVC. External DB/object-storage backup/retention, authoritative DNS/provider ownership and remote Media runner unregister remain unverified. Delete-mode retirement remains blocked.
- Native scheduled reconciliation #42942147668 at 01:53:20Z succeeded. Job logs verified GHCR read access for Auth, MicroFE Shell/WS and TCE service/web; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` was unchanged. Core/TCE deployments were patched with no changes, TCE desired/live release pairing matched `prod-v0.1.0-e75e338`, GitOps drift was false, and apply/rollout were skipped. Final gate classified MicroFE healthy, TCE/Auth as intentional zero-replica maintenance (no live health asserted), Keycloak skipped. Stock ImagePullBackOff pods remained outside the managed MicroFE/TCE pull helper.
- Current blockers/actions: (1) GitHub administrator: provide authoritative scheduler enqueue/delivery/service telemetry and effective branch ruleset confirmation; (2) TCE/Auth owners: diagnose HTTP 503, supply approved immutable release digest, rollback reference and recovery approval; (3) Stock owner: provision `VNSTOCK_API_KEY` only if the owner still intends to operate the scraper; Stock remains in the approved retirement scope and must not be republished/promoted pending retirement decision; (4) Media/Platform owners: complete external backup/retention, DNS ownership and remote runner unregister evidence before guarded decommission; (5) Platform operator: obtain a separate maintenance window before host restart/upgrade; (6) registry administrator: verify server-side GHCR immutable-tag enforcement.
- No new application image publication, digest promotion, Stock/Media delete-mode execution, namespace/PVC/PV deletion, Media runner retirement, GHCR credential rotation, DNS/database/object-storage mutation or host reboot occurred. Auth runtime Secret provisioning/verification and read-only inspection/reconciliation checks are recorded above. Preserve all CI/test/security, release, backup, integration, manual and scheduled workflows; no workflow was confirmed redundant/obsolete. No direct SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Latest run evidence — 2026-11-11 10:01 ICT / 03:01:03 UTC

This section supersedes earlier timestamped readiness values above while preserving their historical evidence.

### Current repository and PR state

- Direct master refs: Platform `1accff7fd7cc1ae733513dfa7eb6067a660f030a`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314, #544, #541, #539 and Authentication #76; no open PRs in TCE, Stock or Media. All remain draft/owner decision. Existing exact-head validation references are listed above; Auth Supabase Preview is intentionally skipped. No owner-decision PR was merged.
- Platform master now includes the previously recorded PR #1607/#1608 updates. No application repository master changed in this checkpoint.

### Latest reconciliation and recovery receipts

- Manual Platform reconciliation [#42949244537](https://github.com/phanthienquoc/platform-infra/actions/runs/42949244537) ran at 02:55:10Z on master SHA `1accff7fd7cc1ae733513dfa7eb6067a660f030a`, with `mode=apply`, `target_app=all`, and image changes disabled. Shared preflight succeeded; GitOps drift was false; manifest apply and rollout were skipped.
- Job logs verified TCE desired/live image pairing at `prod-v0.1.0-e75e338`. TCE and Auth were classified as intentional zero-replica maintenance; no live workload health was asserted for either. MicroFE health was verified healthy. Keycloak lane was skipped. Auth runtime Secret contained required keys; values were suppressed. Shared `ghcr-pull` was unchanged.
- The TCE lane confirmed the desired and live frontend/service image references matched. It did not restore TCE replicas or resolve the public HTTP 503 responses.
- Reconciliation's post-run inspection-recovery job dispatched [recovery receipt #42949413722](https://github.com/phanthienquoc/platform-infra/actions/runs/42949413722) at 02:56:43Z. The receipt succeeded and verified source reconciliation #42949244537. It found native inspection #42932368784 stale (142m at 02:57Z) but manual read-only fallback #42942360712 fresh (59m at 02:57Z), so it correctly dispatched no duplicate inspection. This is workflow_dispatch recovery, not native schedule delivery.
- Manual fallback inspection #42942360712 generated `debug/vps-latest.md` at 01:55:21Z. At the 03:01:03Z reference its age is 3,942s (65m42s), within the 4,500s budget by only 558s (9m18s). It is not live evidence beyond that freshness window. Obtain a new read-only inspection before 03:10:21Z if no newer inspection completes.

### Current native schedule freshness

Reference: 2026-11-11 03:01:03 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run and repository_dispatch runs are not substitutes.

| Lane | Latest native run | Previous native run | Latest created UTC | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 2026-11-11 01:53:20 | 4063 | 14244 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 2026-11-11 00:34:09 | 8814 | 17791 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 2026-11-11 01:28:37 | 5546 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 2026-11-11 01:39:53 | 4870 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 2026-11-11 02:54:41 | 382 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 2026-11-11 02:12:35 | 2908 | 13126 | 1500 |

All six inter-arrival gaps exceed budget. Five of six current-age checks exceed budget; only TCE WF-06 current age is within its 1,500s budget. Platform watchdog #42940581820 failed freshness checks. Its sampled runner-queue diagnostic found no scheduled deployment lane above the 15-minute queue budget, but did not expose scheduler enqueue/delivery timestamps and does not explain the long inter-arrival gaps. GitHub administrator telemetry remains required.

### TCE public health

- Native WF-06 [#42949191917](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42949191917) failed at 02:54:41Z. A subsequent manual WF-06 [#42949231253](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42949231253) also failed.
- The four strict endpoints remain HTTP 503 instead of required HTTP 200: TCE web, TCE API, Auth liveness and Auth readiness. The TCE workflow logs confirm the web probe returned 503; the run's four endpoint jobs all concluded failure.
- Native WF-12 [#42944415193](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42944415193) failed freshness. WF-13/workflow_run recovery receipts do not count as native WF-06/WF-12 cadence.
- Do not lower expected status, weaken probes, or scale TCE/Auth from zero without owner-approved immutable release digests, rollback references and a recovery plan.

### Latest K3s snapshot — last-known, freshness-limited

- Manual inspection #42942360712 reports node `tce-k3s-01` Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Ubuntu 22.04.5; root disk 56% used / about 20 GiB free; about 19 GiB RAM available; `restart_required=yes`. Kernel/containerd/Docker and OS updates are available; no reboot or upgrade was performed.
- Media backend/frontend 1/1 and MicroFE Shell/WS/NATS 1/1. TCE frontend/service, Auth and Keycloak remain 0/0 maintenance. Stock Admin has two 0/1 ImagePullBackOff pods and desired Backend one 0/1 ImagePullBackOff pod on historical tag `12d63b4`; kubelet reports `no match for platform in manifest`. Legacy Stock Backend/Frontend remain 1/1 on `23b2878`, but no registry RepoDigest evidence was established for promotion.
- Media runner service/listener remains active/enabled. Remote GitHub runner unregister, external DB/object-storage backup and retention, and authoritative DNS/provider ownership remain unverified. Stock/Media namespaces remain Active despite being removed from active Platform GitOps manifest scope.
- The read-only retirement preflight found no PVC/PV/VolumeSnapshot references in `stock-prod` or `media-prod`; preserve the separate Bound `k3s-debug/k3s-debug-logs` PVC. Delete-mode retirement remains blocked.

### Exact next actions and safety

1. Platform operator: obtain a fresh read-only `inspect-vps.yml` snapshot before the manual fallback #42942360712 exceeds 4,500s; no restart or package upgrade without a separate maintenance window.
2. GitHub administrator: provide authoritative scheduler enqueue, delivery and Actions service telemetry for the six lanes; verify effective PR-only/required-check/force-push/deletion rulesets for all five repositories.
3. TCE/Auth owners: diagnose the four HTTP 503 endpoints and supply approved immutable release digests, rollback references and explicit recovery approval.
4. Stock/Media owners: complete external backup/retention, DNS ownership and remote Media runner stop/disable/unregister evidence before the guarded namespace decommission. Stock remains in the approved retirement scope; do not publish/promote Stock images as a workaround.
5. Registry administrator: verify GHCR server-side immutable-tag enforcement. TCE owner: verify SSH host fingerprint before any SSH-based maintenance.

No GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/object-storage mutation, host reboot or workflow removal occurred in this checkpoint. Shared `ghcr-pull` remained unchanged. Preserve all useful CI/test/security, release, backup, integration, manual and scheduled workflows. No duplicate direct SSH/Compose deployment authority was added. TCE market-scan schedule and all six cron expressions/budgets remain unchanged.


## Historical verification — 2026-11-11 10:55 ICT / 03:55:46 UTC

This checkpoint supersedes the 10:01 ICT compact readiness values above. It is a read-only evidence refresh plus documentation update; no production mutation was authorized or performed.

### Direct repository state and open PRs

- Direct master refs at this checkpoint: Platform Infra `9848cdeb97a29ff3833378013f4932e6558cb933`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314 (head `db152c9a17416d1a7f82165597dfe478321bd055`), #544 (`c95e7daecb83b65577b54303427fe4ea81adfe06`), #541 (`b8f7c6ba04e3d971336a899b2efd5894662083b3`), #539 (`2dc48b97017ecb08e49682633303a2f1d5e991a1`), and Authentication #76 (`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`). All remain drafts/owner decisions. No open PRs in TCE, Stock or Media. No head changes were observed; previously recorded exact-head validation remains PASS, with Auth Supabase Preview intentionally skipped.
- Latest Platform master run is post-merge `validate-manifests` #42950290166 (push, master SHA `9848cdeb...`), completed SUCCESS at 03:04:36Z. Exact-head PR validation #42950213555 also succeeded. The latest 10-run listing contained no later production reconcile/recovery push.
- Latest TCE native WF-06 #42949191917 (schedule, 02:54:41Z) failed; manual WF-06 #42949231253 (02:55:03Z) also failed. Native WF-12 #42944415193 (02:12:35Z) failed freshness. All four strict public probes remain HTTP 503 versus required 200.
- Latest app-repository master CI evidence remains Stock #42610360402 PASS (2026-11-09), Media #42539512417 PASS (2026-11-09), and Authentication #42654579277 PASS (2026-11-09). Stock scraper #42457182511 remains failed closed because `VNSTOCK_API_KEY` was absent. No new application build or image publication was observed.

### Native schedule freshness

Reference: 2026-11-11 03:55:46 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run and repository_dispatch receipts do not replace native schedule delivery.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 7346 | 14244 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 12097 | 17791 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 8829 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 8153 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 3665 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 6191 | 13126 | 1500 |

All six current-age checks and all six inter-arrival gaps exceed their budgets. No newer native schedule run appeared in the current Actions API query. Do not change cron expressions, freshness budgets or the TCE market-scan schedule. GitHub administrator enqueue/delivery/service telemetry remains unavailable and is still required to locate the delivery gap.

### Runtime evidence freshness and deployment authority

- Last full read-only K3s inspection is #42942360712, whose embedded snapshot was generated at 01:55:21Z. At 03:55:46Z its age is 7,225s, beyond the 4,500s budget by 2,725s. It is stale and must not be used to authorize rollout, deletion, restart or health claims. No fresh inspection run appeared in the latest Platform Actions listing.
- Last manual reconciliation #42949244537 was created at 02:55:10Z; age 3,636s, beyond its 2,700s freshness budget. Native reconciliation #42942147668 is 7,346s old. Recovery receipt #42949413722 is 3,543s old. Their prior results (GHCR read preflight PASS, Auth runtime Secret verified with values suppressed, shared `ghcr-pull` unchanged, drift=false, apply/rollout skipped) are historical evidence only, not current production health.
- Last-known K3s state from the stale inspection: node Ready/ARM64; K3s v1.36.3+k3s1; disk 56% / about 20 GiB free; about 19 GiB RAM available; host restart required. Media and MicroFE core workloads were 1/1; TCE/Auth/Keycloak were 0/0 maintenance; Stock Admin and desired Backend were ImagePullBackOff on `12d63b4` because the image manifest had no matching platform. Stock legacy Backend/Frontend were 1/1 but no registry RepoDigest evidence was available for promotion.
- Media runner service/listener was active/enabled. Remote GitHub runner unregister, external DB/object-storage backup/retention and authoritative DNS/provider ownership remain unverified. Stock/Media namespaces remain present pending the guarded retirement workflow. The separate Bound `k3s-debug/k3s-debug-logs` PVC must be preserved.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred. Platform remains the sole production apply authority; app repositories remain responsible for tests/builds and immutable publication.

### Exact next actions

1. Platform operator: obtain a fresh read-only `inspect-vps.yml` snapshot before any deployment decision; current inspection and reconciliation evidence are stale. No reboot/package upgrade without a separately approved maintenance window.
2. GitHub administrator: provide scheduler enqueue, delivery and Actions service telemetry for all six lanes; verify effective PR-only/required-check/force-push/deletion rulesets for all five repositories.
3. TCE/Auth owners: diagnose four HTTP 503 endpoints and provide approved immutable release digests, rollback references and explicit recovery approval. Preserve strict HTTP 200 probes.
4. Stock/Media owners: complete external backup/retention, DNS ownership and remote Media runner stop/disable/unregister evidence before the guarded namespace decommission. Stock remains in the retirement scope; do not publish/promote Stock images as a workaround.
5. Registry administrator: verify GHCR server-side immutable-tag enforcement. TCE owner: verify SSH host fingerprint before any SSH maintenance.

No workflow was removed; none was confirmed redundant/obsolete. Preserve CI/test/security, release, backup, integration, manual and scheduled workflows. No duplicate SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Historical verification — 2026-11-11 12:04 ICT / 05:04:56 UTC

This checkpoint supersedes the 10:55 ICT readiness values above. It is a read-only evidence refresh plus tracker/inventory documentation; no production mutation was authorized or performed.

### Direct repository state and open PRs

- Direct master refs: Platform Infra `bfa50827eacdb6675f718593c0b38cf693a38b01`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314 (head `db152c9a17416d1a7f82165597dfe478321bd055`), #544 (`c95e7daecb83b65577b54303427fe4ea81adfe06`), #541 (`b8f7c6ba04e3d971336a899b2efd5894662083b3`), #539 (`2dc48b97017ecb08e49682633303a2f1d5e991a1`), and Authentication #76 (`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`). No open PRs in TCE, Stock or Media. All five listed PRs remain drafts/owner decisions.
- Exact-head checks: Platform #1314/#544/#541/#539 each `validate=success`; Authentication #76 `validate=success`, Supabase Preview `skipped`. No owner approval was observed; do not merge Keycloak/database/identity or Auth migration-drift decisions solely because checks pass.
- Latest Platform master workflow is [validate-manifests #42956212725](https://github.com/phanthienquoc/platform-infra/actions/runs/42956212725), push on master SHA `bfa50827...`, SUCCESS at 03:58:50Z. Its jobs passed retired-manifest guard, immutable image contract, Auth digest promotion, TCE/Auth dispatch payload, shell, cert-manager, production rendering, Auth GitOps, secret, immutable-image, Keycloak isolation and network-boundary checks.
- Latest TCE manual WF-06 [#42949231253](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42949231253) failed at 02:55:03Z; native WF-06 [#42949191917](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42949191917) failed at 02:54:41Z; native WF-12 [#42944415193](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42944415193) failed at 02:12:35Z. Workflow_run heartbeat receipt #42949213916 succeeded but is not a native WF-12 schedule run.
- Stock CI [#42610360402](https://github.com/phanthienquoc/stockdividend/actions/runs/42610360402) PASS; scraper schedule [#42457182511](https://github.com/phanthienquoc/stockdividend/actions/runs/42457182511) FAIL CLOSED because repository secret `VNSTOCK_API_KEY` is empty. The credential gate exits before dependency installation and ingestion; no secret value should be placed in Git, logs, artifacts or chat.
- Media CI [#42539512417](https://github.com/phanthienquoc/media-generation/actions/runs/42539512417) PASS. Authentication CI [#42654579277](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42654579277) PASS. No newer application publication or digest handoff was observed.

### Native schedule freshness

Reference: 2026-11-11 05:04:56 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run, repository_dispatch and fallback receipts do not substitute for native schedule delivery.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 11496 | 14244 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 16247 | 17791 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 12979 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 12303 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 7815 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 10341 | 13126 | 1500 |

All six current-age checks and all six inter-arrival gaps exceed their configured budgets. No newer first-attempt native schedule run appeared in the queried Actions history. The latest Platform schedule runs predate current master SHA `bfa50827...`; no native reconciliation/inspection/recovery/watchdog run has validated the current master since PR #1613. Do not alter cron expressions, freshness budgets or the TCE market-scan schedule.

### TCE health and Stock credential evidence

- TCE manual WF-06 #42949231253 has four independent failed jobs. Their decoded logs show: `https://tce.mrcute.space/` returned HTTP 503 (expected 200); `https://tce.mrcute.space/api/health` returned 503; `https://auth.mrcute.space/api/health` returned 503; and `https://auth.mrcute.space/api/ready` returned 503. The curl steps completed and reported the actual status; this is not a runner setup failure. The upstream response body was not surfaced in the job summary, so root cause is not established. Preserve strict HTTP 200 probes; no scale-up or release promotion without owner-approved immutable digest, rollback reference and recovery approval.
- Stock scraper #42457182511 job #128658604760 failed at `Require VNStock API key before installing dependencies`: `VNSTOCK_API_KEY` was empty. Python setup, dependencies, entitlement verification and ingestion were all skipped. This is a fail-closed credential gate, not a deployment-contract defect. Stock remains in the approved retirement scope; do not provision or publish a replacement merely to make this historical job green without an owner decision.

### K3s and GitOps — historical evidence only

- Last full read-only K3s inspection remains #42942360712; its embedded snapshot was generated at 01:55:21Z. At 05:04:56Z it is 11375s old, exceeding the 4500s budget by 6875s. No newer inspection run is present in the current Actions history. It cannot authorize rollout, deletion, restart or a current health claim.
- Last manual reconciliation #42949244537 was created at 02:55:10Z (age 7786s, beyond 2700s); latest native reconciliation #42942147668 is 11496s old. Recovery receipt #42949413722 is 7693s old. Their prior GHCR read preflight, Auth runtime Secret verification, unchanged shared `ghcr-pull`, clean drift and skipped apply/rollout are historical only.
- Last-known inspection state: ARM64 node `tce-k3s-01` Ready, K3s v1.36.3+k3s1, Ubuntu 22.04.5, disk 56% / about 20 GiB free, about 19 GiB RAM available, `restart_required=yes`. Media/MicroFE were 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend (one pod) ImagePullBackOff on historical tag `12d63b4`, kubelet reported `no match for platform in manifest`; legacy Stock Backend/Frontend were 1/1 but lacked RepoDigest evidence for promotion.
- Media runner service/listener was last observed active/enabled. Remote GitHub runner unregister, external DB/object-storage backup/retention and authoritative DNS/provider ownership remain unverified. Stock/Media namespaces remain pending the guarded decommission. The separate Bound `k3s-debug/k3s-debug-logs` PVC must be preserved.
- No fresh K3s snapshot or current reconciliation was obtained in this run. A Platform operator must run `inspect-vps.yml` in read-only mode before any deployment decision; a fresh inspection is a prerequisite, not approval for reboot or rollout.

### Branch governance and merge settings

- Direct `GET /branches/master` reports `protected=false` on all five repositories at this checkpoint.
- Repository metadata reports `allow_squash_merge=true`, but also `allow_merge_commit=true` and `allow_rebase_merge=true` on all five repositories. Thus squash is available but merge/rebase methods are not disabled at repository level.
- Branch-protection detail reads previously returned HTTP 403 for all five; rulesets reads returned an empty list for the four public repositories, while private Stock rulesets were inaccessible due plan/permission limits. Effective inherited organization enforcement is not positively established.
- GitHub administrator must configure/confirm PR-only updates, required CI/contract checks, block force-push, block branch deletion, squash-only merge settings and effective organization ruleset coverage. Until verified, continue dedicated branches, exact-head checks and expected-head squash merges.

### Exact next actions and safety

1. Platform operator: obtain a fresh read-only `inspect-vps.yml` snapshot. Do not reboot/upgrade the host or mutate production based on stale inspection/reconciliation receipts.
2. GitHub administrator: provide enqueue/delivery/Actions service telemetry for all six schedule lanes; configure/confirm effective master protections and disable merge-commit/rebase methods if squash-only is the policy.
3. TCE/Auth owners: diagnose the four HTTP 503 endpoints and provide approved immutable release digests, rollback references and explicit recovery approval. Preserve HTTP 200 health contracts.
4. Stock owner: decide whether the scraper remains in service or stays in retirement scope. If still needed, provision `VNSTOCK_API_KEY` through repository Actions Secrets and run `preflight_only=true`; never paste the key into source/logs/chat. Do not publish/promote Stock images while retirement scope remains active.
5. Media/Platform owners: complete external backup/retention, DNS ownership and remote runner stop/disable/unregister evidence before guarded namespace deletion.
6. Registry administrator: verify GHCR server-side immutable-tag enforcement. TCE owner: verify SSH host fingerprint before any SSH maintenance.

No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/object-storage mutation, host reboot/package upgrade or workflow removal occurred. Preserve all useful CI/test/security, release, backup, integration, manual and scheduled workflows. No duplicate SSH/Compose deployment authority was added. TCE market-scan schedule and all six cron expressions/budgets remain unchanged.


## Post-checkpoint merge verification — 2026-11-11 12:08 ICT / 05:08:18 UTC

- Documentation PR #1614 was squash-merged at `0191e968d11a3b9096ddd24d46fa8daeb03fec3a`; direct `refs/heads/master` read matches this SHA.
- Exact-head validation #42963714334 PASS; post-merge `validate-manifests` #42963772141 PASS.
- The 12:04 ICT readiness section and checkpoint preserve the pre-merge master SHA `bfa50827...` as a timestamped snapshot. This addendum advances only the compact current master reference.
- The post-merge Actions run list for SHA `0191e968...` contains only `validate-manifests`; no `reconcile-vps.yml` or `recover-stale-ops.yml` push run was triggered by the docs-only merge.


## Historical verification — 2026-11-11 14:03 ICT / 07:03:57 UTC

This checkpoint supersedes the 13:03 ICT compact readiness values. Evidence is from direct master refs, open PR metadata, exact-head check-runs, first-page Actions history (up to 100 schedule runs per workflow), decoded job logs and the current read-only VPS snapshot. Runtime freshness is bounded and stated explicitly.

### Direct repository state and open PRs

- Direct `refs/heads/master`: Platform Infra `e6d6213ea5441622a314d1ccacfc3d5fe358fe40`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314 (head `db152c9a17416d1a7f82165597dfe478321bd055`), #544 (`c95e7daecb83b65577b54303427fe4ea81adfe06`), #541 (`b8f7c6ba04e3d971336a899b2efd5894662083b3`), #539 (`2dc48b97017ecb08e49682633303a2f1d5e991a1`); Authentication #76 (`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`). No open PRs in TCE, Stock or Media. All listed PRs remain drafts/owner decisions.
- Exact-head checks: Platform #1314/#544/#541/#539 each `validate=success`; Authentication #76 `validate=success`, Supabase Preview `skipped`. Do not merge owner-decision PRs solely because checks pass.
- Platform inspection PR #1618 was created from dedicated branch `automation/vps-inspection-42972248777-1`, exact head `e2d57a1e91b442720067a9b3e9591abdabbe8971`, validated by #42972457127 PASS, then squash-merged at `e6d6213ea5441622a314d1ccacfc3d5fe358fe40`. It changed only `debug/vps-latest.md`. No separate post-merge validation run for `e6d6213ea5441622a314d1ccacfc3d5fe358fe40` appears in the current Actions listing; the exact PR head validation passed. Latest earlier master push validation #42969932926 was on parent SHA `558afd0026d6d0b8341cd93cc83822a1bbd8ae49`.
- Latest relevant CI: Platform inspection validation #42972457127 PASS; TCE WF-06 manual #42972014911 FAIL and WF-12 workflow_run #42971976274 FAIL; Stock CI #42610360402 PASS and scraper #42457182511 FAIL CLOSED; Media CI #42539512417 PASS; Auth CI #42654579277 PASS. No new application image publication or digest handoff was observed.

### Native schedule freshness

Reference: 2026-11-11 07:03:57 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run, repository_dispatch and fallback receipts do not substitute.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 18637 | 14244 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 23388 | 17791 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 20120 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 19444 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 14956 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 17482 | 13126 | 1500 |

All six current-age checks and all six inter-arrival gaps exceed their budgets. Latest Platform native reconcile/recovery/watchdog runs use pre-current-master SHA `b5fceb3e...`; native inspection uses `d89bcf7e...`. No native scheduled Platform lane has validated current master `e6d6213ea5441622a314d1ccacfc3d5fe358fe40`. TCE WF-07 #42971954835 succeeded as a native schedule at 06:22:22Z, but it is a third-party integration check and does not replace WF-06/WF-12. Preserve every cron expression and freshness budget, including the TCE market-scan schedule.

### Fresh K3s inspection and decommission evidence

- Read-only inspection [#42972248777](https://github.com/phanthienquoc/platform-infra/actions/runs/42972248777) generated `debug/vps-latest.md` at 2026-11-11 06:25:00Z. At the 07:03:57Z reference its age is 2,337s, within the 4,500s budget (2,163s remaining). The recovery controller [#42972199624](https://github.com/phanthienquoc/platform-infra/actions/runs/42972199624) verified reconciliation #42972016233 was recent, found native inspection stale and dispatched this read-only inspection fallback. The fallback does not satisfy native schedule freshness.
- Host: ARM64 Ubuntu 22.04.5; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; node `tce-k3s-01` Ready; disk 56% / about 20 GiB free; RAM about 19 GiB available; uptime about 193 days 16h15m at snapshot time. `restart_required=yes`; kernel, containerd, Docker and OS packages have updates pending. No reboot or package upgrade was performed.
- Workloads: Media backend/frontend 1/1; MicroFE Shell/WS/NATS 1/1; TCE frontend/service 0/0 maintenance; Auth `microfe-auth` 0/0 maintenance; Keycloak 0/0 maintenance. Stock Admin has two ImagePullBackOff pods and desired Stock Backend one ImagePullBackOff pod on tag `12d63b4`, with kubelet reporting `no match for platform in manifest`. Legacy Stock Backend/Frontend are 1/1 on `23b2878`, but their cached images have no RepoDigest; local image IDs are not registry promotion evidence.
- Digest-pinned runtime evidence exists for Media backend `sha256:93ddb944...`, Media frontend `sha256:095c72ed...`, MicroFE Shell `sha256:ae64acc0...` and MicroFE WS `sha256:416bc16a...`. TCE/Auth remain 0/0 and are not healthy merely because their deploy-lane maintenance contract passes.
- GitOps drift: clean. Target Stock/Media namespaces have no PVC/PV claim or VolumeSnapshot references in the read-only decommission preflight. Preserve the separate Bound PVC `k3s-debug/k3s-debug-logs` (1 GiB). Media runner service/listener is active and enabled; remote GitHub runner unregister is not inferred by host inspection and remains unverified. External backup/retention and authoritative DNS/provider ownership remain outstanding.

### Reconciliation, credentials and health interpretation

- Manual reconciliation [#42972016233](https://github.com/phanthienquoc/platform-infra/actions/runs/42972016233) ran on parent master SHA `558afd0026d6d0b8341cd93cc83822a1bbd8ae49` at 06:22:53Z with `mode=apply`, `target_app=all`, `allow_image_changes=false`. At the reference time its age is 2,464s, within the 2,700s reconciliation budget by 236s.
- GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE service/web. Auth runtime Secret was provisioned and verified with values suppressed. Shared `ghcr-pull` reconciliation returned unchanged. The blocked-image-pull restart helper found no image-pull failures in managed Auth/MicroFE/TCE workloads; it did not restart those workloads. Preflight diff was clean, GitOps drift=false, manifest apply skipped, image replacement skipped and rollout skipped. Deployment lane summary: MicroFE healthy; Auth and TCE intentional zero-replica maintenance with no live health asserted; Keycloak skipped.
- TCE WF-06 manual [#42972014911](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42972014911) has four independent public probes returning HTTP 503 vs expected HTTP 200: TCE web, TCE API, Auth liveness and Auth readiness. The fresh K3s snapshot shows the corresponding TCE/Auth workloads intentionally at 0/0; Keycloak is also 0/0 and both public OIDC realm discovery probes return 503. These 503s are consistent with the approved zero-replica maintenance state, not evidence that the HTTP 200 contract should be weakened. Preserve strict probes; do not scale up without owner-approved immutable release digests, rollback references and explicit recovery approval.
- TCE WF-12 workflow_run #42971976274 failed because native WF-06 delivery/health evidence was stale/failed. Native WF-06 #42949191917 and native WF-12 #42944415193 remain the latest schedule runs and are stale. No native schedule recovery is claimed.

### Branch governance and merge settings

- Direct `GET /branches/master` reports `protected=false` on all five repositories at this checkpoint.
- Repository metadata reports `allow_squash_merge=true`, `allow_merge_commit=true`, and `allow_rebase_merge=true` on all five repositories. Squash is available but merge-commit and rebase are still enabled, contrary to the intended squash-only standard.
- Effective inherited organization ruleset enforcement is not positively established through the current integration. GitHub administrator must enforce/confirm PR-only updates, required CI/deployment-contract checks, force-push and deletion protection, disable merge-commit/rebase, and verify effective organization ruleset coverage.
- Continue dedicated branches, exact-head checks and expected-head squash merges. Do not work directly on master.

### Exact next actions and safety

1. Platform operator: refresh read-only inspection before the 4,500s snapshot budget expires (approximately 07:40:00Z if no newer inspection arrives). Do not reboot or upgrade the host; obtain a separately approved maintenance window.
2. GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry for all six lanes; configure/confirm effective master protection and squash-only merge settings across all five repositories.
3. TCE/Auth owners: keep 0/0 maintenance explicit until an approved recovery decision; supply immutable release digests, rollback references and explicit approval before Platform changes replicas or images.
4. Stock owner: decide whether Stock remains in service or stays in retirement scope. Do not publish/promote replacement images while retirement remains active. If retained, provision `VNSTOCK_API_KEY` only through Actions Secrets and run safe `preflight_only=true`.
5. Media/Platform owners: complete external backup/retention, DNS ownership and remote runner stop/disable/unregister evidence before guarded namespace deletion.
6. Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new GHCR publication or digest promotion occurred. The reconciliation did provision/verify the Auth runtime Secret and confirm shared `ghcr-pull` unchanged; no manifest apply, image replacement or workload rollout occurred. No namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/object-storage mutation, host reboot/package upgrade or workflow removal occurred in this run. Preserve all useful CI/test/security, release, backup, integration, manual and scheduled workflows; none is confirmed redundant/obsolete. No duplicate SSH/Compose deployment authority was added. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 15:20 ICT / 08:20:47 UTC

- PR #1622 was squash-merged at `8f95ddd8729eae6fee662e3a395f083be4fc21b0`; direct `refs/heads/master` reads match this SHA.
- Exact-head `validate-manifests` #42986144723 PASS on PR head `88f22bb11a927e87af676d274b921cc9118b9805`.
- Post-merge `validate-manifests` #42986252700 PASS on master SHA `8f95ddd8...`; retired Stock/Media guard, immutable image-change contract, Auth digest promotion, TCE/Auth dispatch payload, manifest rendering, Secret policy, Keycloak isolation and network boundaries passed. Changed-image reference validation was skipped because this was documentation-only.
- The post-merge run list contains only `validate-manifests`; no `reconcile-vps.yml` or `recover-stale-ops.yml` push run was triggered by this documentation-only merge.
- The 15:09 ICT operational checkpoint remains the latest runtime/schedule snapshot. This addendum advances the compact current Platform SHA only; it does not refresh K3s or native schedule evidence.
- No production manifest, image, Secret, workload, DNS, database, storage, namespace or runner was changed by PR #1622. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 15:35 ICT / 08:35:19 UTC

### Merge and exact-head evidence

- PR #1624 [docs(deploy): refresh cross-repo readiness at 15:25 ICT](https://github.com/phanthienquoc/platform-infra/pull/1624) was squash-merged at `cfeb5dbf74a625f443d44141bd4c719f47ec60a3`; direct `refs/heads/master` matches this SHA.
- Exact PR head `7a96c7deeae23245a208a94bab66139869269614` passed run #42987271290. The exact-head check-runs show `validate=success`; the failure reporter was skipped by design. All 19 manifest/deployment-contract validation steps completed successfully.
- Post-merge master validation #42988178995 completed SUCCESS on `cfeb5dbf...`. It ran `validate-manifests` only. No production reconcile/recovery push run was triggered by the docs-only merge.
- PR #1624 changed only the tracker, workflow inventory and two timestamped checkpoints. No production workflow, manifest or app source changed.

### Direct repository state and open PRs

- Master refs: Platform Infra `cfeb5dbf74a625f443d44141bd4c719f47ec60a3`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Current open PRs: Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. All remain drafts/owner decisions. Exact-head `validate` checks are PASS on the current heads; Auth Supabase Preview is skipped. Do not merge these owner-decision PRs without approval.
- App CI evidence remains historical but last-known successful: TCE has no app code PR; Stock CI #42610360402 PASS; Media CI #42539512417 PASS; Authentication CI #42654579277 PASS. Stock scraper #42457182511 remains FAIL CLOSED because `VNSTOCK_API_KEY` is empty.

### Native schedule freshness

Reference: 2026-11-11 08:35:19 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run and repository_dispatch receipts do not substitute.

| Lane | Latest native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | 24119 | 14244 | 2700 |
| Platform inspection | #42981286761 | 3253 | 25617 | 4500 |
| Platform recovery | #42986496462 | 780 | 24822 | 2700 |
| Platform watchdog | #42986833403 | 629 | 24297 | 2700 |
| TCE WF-06 | #42949191917 | 20438 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | 22964 | 13126 | 1500 |

All six inter-arrival budgets fail. Three current-age budgets fail (Platform reconciliation and both TCE health lanes); Platform inspection, recovery and watchdog current-age budgets pass. Watchdog #42986833403 failed on the native inter-arrival gates and stale TCE WF-06 observation; runner-queue diagnostics did not establish a queue delay over 15 minutes. Scheduler enqueue/delivery telemetry is still required from GitHub administration. Preserve every cron expression, freshness budget and the TCE market-scan schedule.

### K3s, GitOps and application health — freshness-bounded

- Read-only inspection #42981286761 generated `debug/vps-latest.md` at 07:41:14Z; age 3245s at this reference, within the 4500s budget by 1255s. Node `tce-k3s-01` Ready/ARM64; Ubuntu 22.04.5; K3s v1.36.3+k3s1; disk 56% / ~20 GiB free; RAM ~19 GiB available; `restart_required=yes`. No reboot or package upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry RepoDigest references. TCE frontend/service, Auth and Keycloak are 0/0 intentional maintenance; they are not healthy/live. Stock Admin (two pods) and desired Stock Backend remain ImagePullBackOff on tag `12d63b4` with `no match for platform in manifest`. Legacy Stock Backend/Frontend are 1/1 on `23b2878`, but cached images have no RepoDigest; local image IDs are not promotion evidence.
- Preserve Bound PVC `k3s-debug/k3s-debug-logs`. Media runner service/listener remains active/enabled; remote GitHub runner unregister, external DB/object-storage backup/retention and authoritative DNS ownership remain unverified.
- Manual reconciliation #42986517013 SUCCESS at 08:22:28Z; age 771s within the 2700s budget. GHCR read preflight passed for managed Auth/MicroFE/TCE packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` unchanged. TCE desired/live image pairing passed; drift=false; manifest apply, image replacement and workload rollout skipped. MicroFE healthy; TCE/Auth maintenance; Keycloak skipped.
- Recovery #42986712253 SUCCESS at 08:23:56Z; age 683s within the 2700s budget. It verified fresh reconciliation and inspection evidence and did not dispatch duplicate fallbacks. These receipts are not native schedule cadence.
- TCE manual WF-06 #42972014911 returned HTTP 503 on TCE web/API and Auth liveness/readiness; the inspection shows TCE/Auth/Keycloak at 0/0. Preserve strict HTTP 200 checks and do not classify maintenance as healthy. No owner-approved recovery digest, rollback reference or activation approval is available.

### Governance, next actions and safety

- Current repository metadata still allows merge commits and rebase alongside squash. Last direct branch governance evidence reports `protected=false` on all five master branches; effective inherited organization rulesets remain unverified. GitHub administrator must enforce PR-only, required CI/deployment-contract checks, force-push/deletion protection and squash-only merge.
- Platform operator: refresh read-only K3s inspection before the 4500s budget expires; do not reboot/upgrade without an approved maintenance window.
- GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry for all six lanes and confirm effective branch rulesets.
- TCE/Auth owners: keep maintenance until explicit recovery approval, immutable release digests and rollback references are provided.
- Stock owner: confirm retirement versus restoration; do not publish while retirement remains approved. If restored, provision `VNSTOCK_API_KEY` only through Actions Secrets and run safe preflight.
- Media owner: complete backup/retention, DNS ownership and remote runner stop/disable/unregister evidence.
- Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new GHCR publication, digest promotion, production manifest apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this post-merge verification. Preserve useful CI/test/security, release, backup, integration, manual and scheduled workflows; none is confirmed redundant/obsolete. App repositories remain responsible for tests/builds and immutable GHCR publication; Platform remains the sole production manifest, shared credential, GitOps promotion/reconciliation, rollout and health authority. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 15:40 ICT / 08:40:35 UTC

- PR #1625 [post-merge readiness SHA synchronization](https://github.com/phanthienquoc/platform-infra/pull/1625) was squash-merged at `8419328596b1a96340dd48fd439d08c77f04da38`; direct master ref matches this SHA.
- Exact-head validation #42988772690 PASS on `2f5ad7b553b8ea6ebc86be2a9a70ad2692e4659f`; all 19 validation steps passed. Post-merge master validation #42988867666 PASS.
- Post-merge run history contains only `validate-manifests`; no production reconcile/recovery push run was triggered by PR #1625. PR #1625 changed only the tracker, workflow inventory and two post-merge checkpoints.
- Direct refs remain Platform `8419328596b1a96340dd48fd439d08c77f04da38`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Auth `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Auth #76; none in TCE/Stock/Media. All remain drafts/owner decisions. Exact-head validation passes on the current heads; Auth Supabase Preview is skipped. No owner-decision PR was merged.

### Native schedule freshness

Reference: 2026-11-11 08:40:35 UTC. Only first-attempt `event=schedule` runs on `master` count.

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | 24435 | 14244 | 2700 |
| Platform inspection | #42981286761 | 3569 | 25617 | 4500 |
| Platform recovery | #42986496462 | 1096 | 24822 | 2700 |
| Platform watchdog | #42986833403 | 945 | 24297 | 2700 |
| TCE WF-06 | #42949191917 | 20754 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | 23280 | 13126 | 1500 |

All six inter-arrival budgets fail; three current-age budgets fail (Platform reconciliation and both TCE health lanes). Inspection, recovery and watchdog current-age budgets pass. The watchdog's runner queue sample did not establish a delay above 15 minutes; GitHub scheduler enqueue/delivery telemetry is still required. Preserve all cron expressions and the TCE market-scan schedule.

### K3s and GitOps freshness

- Read-only inspection #42981286761 generated `debug/vps-latest.md` at 07:41:14Z; age 3561s at reference, within the 4500s budget by 939s. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 56% / ~20 GiB free, ~19 GiB RAM available, host restart required. No reboot/upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1 Running with RepoDigest references. TCE/Auth/Keycloak 0/0 intentional maintenance; not live healthy. Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4` due no compatible ARM64 manifest descriptor. Legacy Stock Backend/Frontend 1/1 on `23b2878`, but no RepoDigest promotion evidence.
- Preserve Bound `k3s-debug/k3s-debug-logs` PVC. Media runner remains active/enabled; remote unregister, external backup/retention and authoritative DNS ownership remain unverified.
- Manual reconciliation #42986517013 SUCCESS at 08:22:28Z; age 1087s within 2700s. GHCR read preflight passed; Auth runtime Secret verified with values suppressed; shared `ghcr-pull` unchanged; TCE desired/live pairing passed; drift=false; manifest apply, image replacement and workload rollout skipped. MicroFE healthy; TCE/Auth maintenance; Keycloak skipped.
- Recovery #42986712253 SUCCESS at 08:23:56Z; age 999s within 2700s; no duplicate fallback dispatch. These manual/workflow_dispatch receipts do not satisfy native cadence.
- TCE manual WF-06 #42972014911 returned HTTP 503 on all four strict probes; inspection shows TCE/Auth/Keycloak 0/0. Preserve HTTP 200 checks and do not classify maintenance as healthy.

### App state and governance

- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Stock remains approved retirement scope; do not publish/promote without owner reversal.
- Media CI #42539512417 PASS; backend/frontend digest-pinned and running; runner retirement evidence incomplete.
- Auth CI #42654579277 PASS; Auth remains 0/0 maintenance.
- Open PR exact-head checks: Platform #1314/#544/#541/#539 `validate=success`; Auth #76 `validate=success`, Supabase Preview skipped.
- Last direct branch governance evidence remains `protected=false` on all five master branches; repository metadata allows merge commit and rebase alongside squash. Effective inherited rulesets remain unverified. Administrator action is still required for PR-only, required checks, force-push/deletion protection and squash-only.

No new image publication, digest promotion, production apply, workload rollout, namespace/storage deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. No workflow was removed. App repositories retain build/publish ownership; Platform remains the sole production apply authority. No direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest verification delta — 2026-11-11 15:55 ICT / 08:55:27 UTC

This checkpoint is based on direct Git refs, current open-PR metadata and exact-head check-runs, the first 100 native schedule events for Platform/TCE, the latest 100 Platform master Actions runs, and decoded logs for reconciliation #42986517013. Runtime evidence is freshness-bounded and must not be treated as current after its stated expiry.

### Direct repository state and open PRs

- Direct `refs/heads/master`: Platform Infra `4cb217722b77c190886cb2ce1c28fe26802bce19`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314 head `db152c9a17416d1a7f82165597dfe478321bd055`, #544 `c95e7daecb83b65577b54303427fe4ea81adfe06`, #541 `b8f7c6ba04e3d971336a899b2efd5894662083b3`, #539 `2dc48b97017ecb08e49682633303a2f1d5e991a1`; Authentication #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`. No open PRs in TCE, Stock or Media. All five remain drafts / owner decisions.
- Exact current-head check-runs: Platform #1314/#544/#541/#539 each have `validate=success`; Auth #76 has `validate=success` and `Supabase Preview=skipped`. These checks do not authorize merging owner-decision drafts.
- Platform latest master run [#42989295172](https://github.com/phanthienquoc/platform-infra/actions/runs/42989295172) is `validate-manifests`, push, SUCCESS on current master `4cb21772...` at 08:43:31Z. Its post-merge validation does not constitute a production reconcile or K3s inspection.
- Latest app evidence in the current first-page master run history: TCE manual WF-06 #42972014911 failed; latest native WF-06 #42949191917 and native WF-12 #42944415193 failed. WF-07 integration #42971954835 succeeded but is not a health-lane substitute. Stock CI #42610360402 passed; scraper #42457182511 failed closed. Media CI #42539512417 passed. Auth CI #42654579277 passed. No newer app build/publication or immutable digest handoff was observed.

### Native schedule freshness

Reference: 2026-11-11 08:55:27 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run, repository_dispatch and rerun attempts do not substitute.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 25327 | 14244 | 2700 |
| Platform inspection | #42981286761 | #42932368784 | 4461 | 25617 | 4500 |
| Platform recovery | #42986496462 | #42939222343 | 1988 | 24822 | 2700 |
| Platform watchdog | #42986833403 | #42940581820 | 1837 | 24297 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 21646 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 24172 | 13126 | 1500 |

All six inter-arrival gaps exceed budget. Three of six current-age checks fail (Platform reconcile and TCE WF-06/WF-12); Platform inspection is only 39 seconds inside its run-age budget, while recovery and watchdog are currently inside their age budgets. No newer native event appears in the queried 100-run filtered histories. The latest Platform native inspection/reconcile/recovery/watchdog runs use pre-current-master SHAs; only Platform's docs validation run #42989295172 is on current master. TCE native health events use current TCE master but fail.

### K3s inspection — immediate expiry boundary

- Latest native read-only inspection [#42981286761](https://github.com/phanthienquoc/platform-infra/actions/runs/42981286761) was created at 07:41:06Z on Platform SHA `4b22409cd0...`; embedded snapshot `debug/vps-latest.md` was generated at 07:41:14Z. At this reference the snapshot age is 4,453s against a 4,500s budget, leaving only 47 seconds. It expires at approximately 08:56:14Z. This is not a durable rollout authorization and was generated before current master `4cb21772...`.
- Last-known read-only state: ARM64 node `tce-k3s-01` Ready; K3s v1.36.3+k3s1; disk 56% / ~20 GiB free; ~19 GiB RAM available; host restart required. Media backend/frontend and MicroFE Shell/WS/NATS 1/1. TCE/Auth/Keycloak 0/0 maintenance. Stock Admin (two pods) and desired Backend (one pod) ImagePullBackOff; legacy Stock Backend/Frontend 1/1.
- Stock desired image tag `12d63b4` lacks a compatible ARM64 manifest descriptor (`no match for platform in manifest`). Legacy Stock local image IDs are not registry RepoDigest evidence. Do not promote them.
- Media runner service/listener remains active/enabled. Remote GitHub runner unregister, external DB/object-storage backup/retention and authoritative DNS/provider ownership remain unverified. Preserve Bound PVC `k3s-debug/k3s-debug-logs`; no namespace/PVC/PV deletion is authorized.

### Latest reconciliation — historical commit, no rollout

- Latest visible successful manual reconciliation [#42986517013](https://github.com/phanthienquoc/platform-infra/actions/runs/42986517013) was created at 08:22:28Z on older Platform SHA `8f95ddd872...`, not current master `4cb21772...`. At reference it is 1,979s old against a 2,700s budget (721s remaining).
- Decoded reconcile job logs show `mode=apply`, `target_app=all`, `allow_image_changes=false`. Runner policy v15 became ready after its bounded wait. GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE service/web. Auth runtime Secret was provisioned and verified with values suppressed. Shared `ghcr-pull` was unchanged. Managed MicroFE/TCE image-pull checks reported no failures; Stock Admin/desired Backend ImagePullBackOff remained visible outside the managed GHCR helper.
- GitOps drift was false; manifest apply and drift verification were skipped by the no-drift gate; no image replacement or workload rollout occurred. MicroFE was reported healthy; TCE/Auth were intentional 0/0 maintenance; Keycloak was skipped. This run is not current-master reconciliation evidence and must not be used to authorize a new rollout.
- Recovery receipt #42986712253 (workflow_dispatch) and watchdog #42986833403 (schedule) are still inside their 2,700s age budgets at this reference, but do not repair native inter-arrival gaps.

### Branch governance

- Direct `GET /branches/master` reports `protected=false` and no required status checks for all five repositories.
- Repository metadata for all five reports `allow_squash_merge=true`, `allow_merge_commit=true`, `allow_rebase_merge=true`; this is not squash-only.
- Effective inherited organization ruleset enforcement remains unverified. The current integration does not expose repository administration writes. GitHub administrator must enforce PR-only, required CI/deployment-contract checks, force-push and deletion protection, disable merge-commit/rebase, and verify inherited coverage.
- Continue dedicated descriptive branches, exact-head checks and expected-head squash merges. Do not merge the five owner-decision drafts.

### Exact next actions and safety

1. Platform operator: run a fresh read-only `inspect-vps.yml` immediately; the embedded snapshot reaches its 4,500s expiry at 08:56:14Z. The available GitHub connection in this run has read and PR/file-write operations but no workflow-dispatch action, so this automation did not dispatch inspection. Do not use the expiring snapshot for rollout.
2. Platform operator: run a fresh read-only reconciliation against current master `4cb21772...` before any deployment decision; the last successful reconciliation ran on older SHA `8f95ddd872...`.
3. GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry and enforce/confirm master protection plus squash-only settings.
4. TCE/Auth owners: diagnose four strict HTTP 200 endpoints returning 503 while workloads are 0/0 maintenance; provide owner-approved immutable release digest, rollback reference and explicit recovery approval.
5. Stock owner: decide whether Stock remains retired; if retained, provision `VNSTOCK_API_KEY` only through protected Actions Secrets and run safe `preflight_only=true`. Do not publish/promote while retirement scope remains active.
6. Media/Platform owners: complete external backup/retention, DNS ownership and remote runner stop/disable/unregister evidence before guarded deletion.
7. Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new GHCR publication, digest promotion, current-master production apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred. Preserve useful CI/test/security, release, backup, integration, manual and scheduled workflows; none is confirmed redundant/obsolete. App repositories retain tests/builds/immutable publication ownership; Platform remains the sole production manifest, shared credential, GitOps promotion/reconciliation, rollout and health authority. No direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 16:00 ICT / 09:00:35 UTC

- PR #1627 squash-merged at `37a5624a325c570df0fc689b4f6ecde5f9bae89e`; exact-head validation [#42991422461](https://github.com/phanthienquoc/platform-infra/actions/runs/42991422461) PASS and post-merge current-master validation [#42991499455](https://github.com/phanthienquoc/platform-infra/actions/runs/42991499455) PASS.
- Master ref was read after merge and matched `37a5624a...`. Post-merge workflow ran `validate-manifests` only; no production reconciliation or recovery push run was triggered by this documentation-only merge.
- PR #1627 changed only the tracker, workflow inventory and two timestamped checkpoints. No manifests, app code, workflows, secrets or production resources changed.
- The embedded K3s inspection snapshot #42981286761 generated 07:41:14Z is now 4,761s old at this reference, exceeding the 4,500s budget by 261s. It is expired; no fresh inspection was obtained.
- Latest successful manual reconciliation #42986517013 is 2,287s old against 2,700s (413s remaining) but ran on older Platform SHA `8f95ddd872...`, not current master `37a5624a...`. It reported drift=false and skipped apply/image replacement/rollout; do not treat it as current-master reconciliation evidence.
- Six native schedule inter-arrival gaps remain outside budget. Current-age checks now also fail for inspection, in addition to Platform reconcile and TCE WF-06/WF-12. Recovery and watchdog remain within current-age budgets.
- No production dispatch, GHCR publication, digest promotion, apply, rollout, deletion, credential/DNS/database/storage mutation or host restart occurred. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 16:58 ICT / 09:58:55 UTC

### Direct repository refs, open PRs and checks

- Direct `refs/heads/master`: Platform Infra `e6b7156d191ff3ae9bcb8ff66f1b2a5259de331e`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open drafts/owner decisions: Platform #1314 (head `db152c9a`, validate PASS), #544 (`c95e7dae`, validate PASS; currently mergeable=false), #541 (`b8f7c6ba`, validate PASS), #539 (`2dc48b97`, validate PASS); Authentication #76 (`f19cacb0`, validate PASS; Supabase Preview skipped). No open PRs in TCE, Stock or Media. Keep all owner-decision PRs unmerged.
- Platform inspection PR #1629 was squash-merged at `e6b7156d191ff3ae9bcb8ff66f1b2a5259de331e`; exact-head `validate-manifests` #42994322789 passed on branch `automation/vps-inspection-42994074939-1`, head `dc7f043a`. Current-master check-run history contains recovery #42996312662 SUCCESS plus watchdog/recovery workflow_run jobs SKIPPED; no post-merge `validate-manifests` run is present for `e6b7156d`. Do not report a post-merge validation that was not observed.
- All five direct `branches/master` API responses report `protected=false`, `protection.enabled=false`, `required_status_checks.enforcement_level=off`, and no required contexts/checks. Repository metadata still allows squash, merge commits and rebase. This is direct branch-protection evidence; inherited organization ruleset evaluation remains a separate admin check.

### Latest workflow evidence

- Platform native reconciliation [#42993779924](https://github.com/phanthienquoc/platform-infra/actions/runs/42993779924) SUCCESS at 09:16:25Z on pre-merge SHA `c557b3f3405b8276c5930d3ffab93690b04694d4`. GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE service/web. Auth runtime Secret was provisioned and verified with values suppressed; shared `ghcr-pull` was unchanged. TCE desired/live pairing passed for `prod-v0.1.0-e75e338`; GitOps drift=false, manifest apply skipped, image replacement skipped and no managed workload restart was required. Stock Admin and desired Backend still had ImagePullBackOff pods.
- Read-only inspection [#42994074939](https://github.com/phanthienquoc/platform-infra/actions/runs/42994074939) SUCCESS at 09:18:31Z (snapshot `debug/vps-latest.md` generated 09:18:40Z). It created PR #1629; exact-head validation passed and the inspection automation squash-merged it to current master `e6b7156d`. This is workflow_dispatch fallback evidence, not a native scheduled inspection.
- Recovery [#42996312662](https://github.com/phanthienquoc/platform-infra/actions/runs/42996312662) SUCCESS on current master after TCE WF-12 #42996293386. Logs say reconciliation #42993779924 was recent enough (age 16m at recovery reference), so no reconciliation fallback was dispatched. Native inspection #42981286761 was stale, but read-only fallback #42994074939 was fresh (age 13m at recovery reference), so no duplicate inspection fallback was dispatched. Native schedule remains stale.
- Platform watchdog workflow_run #42996353169 and its recovery workflow_run #42996363913 were SKIPPED; neither counts as native schedule delivery.
- TCE native WF-12 [#42996293386](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42996293386) FAILED because latest native WF-06 #42949191917 was 23,977s old (399m) at watchdog reference; measured runner queue was 0m. TCE manual WF-06 [#42996339882](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42996339882) returned HTTP 503 for all four strict endpoints: TCE web, TCE API, Auth liveness and Auth readiness. WF-13 recovery #42996315416 succeeded as a fallback, not native schedule evidence.
- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty. Media CI #42539512417 PASS. Authentication CI #42654579277 PASS. No new app image publication or immutable digest promotion was observed.

### Native schedule freshness

Only first-attempt `event=schedule` runs on `master` count. Reference is 2026-11-11 09:58:55 UTC; age is from `created_at`; inter-arrival is latest minus previous native run.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | #42942147668 | 2,550 | 26,585 | 2,700 |
| Platform inspection | #42981286761 | #42932368784 | 8,269 | 25,617 | 4,500 |
| Platform recovery | #42986496462 | #42939222343 | 5,796 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | #42940581820 | 5,645 | 24,297 | 2,700 |
| TCE WF-06 | #42949191917 | #42922537816 | 25,454 | 12,853 | 1,500 |
| TCE WF-12 | #42996293386 | #42971976274 | 1,477 | 11,506 | 1,500 |

All six inter-arrival budgets fail. Four of six current-age budgets fail; Platform reconciliation and TCE WF-12 remain within current-age budget at this reference, with 150s and 23s remaining respectively. WF-12's own schedule age being fresh does not make its failed WF-06 freshness check healthy. Do not count manual, workflow_run or repository_dispatch receipts as native schedule delivery. Preserve all cron expressions and TCE market-scan scheduling.

### K3s inspection and GitOps runtime

- Fresh read-only fallback inspection #42994074939 generated `debug/vps-latest.md` at 09:18:40Z; age 2,415s at reference, within 4,500s budget (2,085s remaining). Node `tce-k3s-01` Ready/ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% / about 20 GiB free; about 19 GiB RAM available. Host `restart_required=yes`; package/kernel/Docker updates pending. Do not reboot or upgrade without a maintenance window.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry digest references for Media and MicroFE images. Media and Platform self-hosted runner services/listeners are active/enabled. TCE frontend/service, Auth and Keycloak remain 0/0 maintenance.
- Stock Admin has two ImagePullBackOff pods; desired Stock Backend has one ImagePullBackOff pod, while the legacy Stock Backend remains 1/1 and Stock Frontend remains 1/1. The failing desired images use historical tag `12d63b4` with no RepoDigest. Legacy Stock `23b2878` image IDs are local `sha256:` IDs, not registry RepoDigest promotion evidence. Preserve the existing healthy legacy replicas while owner retirement/restore decision remains unresolved.
- PVC `k3s-debug/k3s-debug-logs` remains Bound (1Gi); preserve it. Docker reports 20 images / 9.195GB, 5.773GB reclaimable; `/var/log` about 1.8GB and journal about 1.5GB. This is diagnostic only; no cleanup was run.
- Reconciliation #42993779924 ran on older SHA `c557b3f`, not current master `e6b7156d`. It verified GHCR access for five managed packages, Auth runtime Secret, shared `ghcr-pull` unchanged, TCE release pairing and no GitOps drift; apply/image replacement/rollout were skipped. Do not use this older-SHA receipt as authorization to apply current master.

### Governance, ownership and next actions

- Branch protection remains absent in direct API evidence on all five master branches; no required checks are configured and merge commit/rebase remain enabled. GitHub administrator must enforce PR-only, actual CI/contract checks, force-push/deletion protection and squash-only merge, then verify effective inherited rulesets.
- GitHub administrator: provide scheduler enqueue/delivery and Actions service telemetry for the six lanes; runner queue evidence does not establish scheduler delivery cause.
- Platform operator: obtain a new read-only inspection before fallback #42994074939 exceeds its 4,500s freshness budget (approximately 10:33:40Z / 17:33:40 ICT), and run read-only reconciliation on current master `e6b7156d` before any deployment decision. Do not reboot/upgrade without approval.
- TCE/Auth owners: decide whether to reactivate maintenance; if approved, provide immutable release digests, rollback references and explicit recovery approval. Keep strict HTTP 200 health probes.
- Stock owner: confirm continued retirement vs service restoration. If retained, provision `VNSTOCK_API_KEY` only via protected Actions Secrets and run safe `preflight_only=true`; do not publish while retirement scope remains active.
- Media owner: complete external backup/retention, authoritative DNS ownership and remote runner stop/disable/unregister evidence before namespace deletion.
- Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new GHCR publication, digest promotion, current-master manifest apply, workload rollout, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred in this checkpoint. Auth runtime Secret provisioning/verification did run in native reconciliation #42993779924; values were suppressed and shared `ghcr-pull` was unchanged. Preserve useful CI/test/security, release, backup, integration, manual and scheduled workflows; none is confirmed obsolete. App repositories own tests/builds/immutable publication; Platform remains sole production apply authority. No direct SSH/Compose authority. TCE market-scan schedule unchanged.

## Post-merge verification — 2026-11-11 16:58 ICT / 10:06:28 UTC

- PR #1630 was squash-merged at `1bd6ea38fcc4591da16422868ac03124704ea293`; direct `refs/heads/master` read matched the merge SHA.
- Exact-head `validate-manifests` #43000595633 PASS on PR head `679ea218d644664c0bb51c042179c06bfda62678`.
- Post-merge current-master `validate-manifests` [#43000748526](https://github.com/phanthienquoc/platform-infra/actions/runs/43000748526) PASS on `1bd6ea38...`. Retired Stock/Media guard, immutable image-change contract, Auth digest promotion, TCE/Auth dispatch payload, shell validation, cert-manager bootstrap, manifest rendering, Auth GitOps, YAML, Secret policy, immutable image policy, Keycloak isolation and network boundaries passed. Changed-image validation skipped because this PR was documentation-only.
- Post-merge run list contains `validate-manifests` only; no production reconciliation or recovery push was triggered by this documentation-only merge.
- This addendum advances the compact Platform master SHA only. The 09:58:55Z operational/schedule reference and K3s snapshot freshness remain unchanged; do not treat the SHA sync as new runtime evidence.
- No manifests, app code, workflows, secrets, GHCR publication, digest promotion, production apply, rollout, deletion, host reboot or DNS/database/storage mutation occurred. TCE market-scan schedule unchanged.

## Latest verification — 2026-11-11 18:01 ICT / 11:01:52 UTC

### Direct repository refs, open PRs and exact-head checks

- Platform Infra master: `ff401dadb1cac5b0647c1a4187fe171b2cfbc937`; TCE Dashboard master after PR #1037: `5b425bdeab457e943bcecf1831836fc698e24394`; StockDividend: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication: `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- TCE PR [#1037](https://github.com/phanthienquoc/TCE-dashboard/pull/1037) was squash-merged at `5b425bdeab457e943bcecf1831836fc698e24394`. Exact head `4abbcab17e4cc6257ab0e00ff7216eba5ce37fdd`; WF-01P #43008284677, WF-02 #43008284672, WF-05 #43008284792 and WF-08B #43008284695 all PASS. WF-01P logs confirm the new contract script parsed WF-13/WF-06/WF-12/WF-01P YAML, preserved all four HTTP 200 endpoint expectations and both schedule expressions, and passed the TCE release contract plus frontend build. Post-merge master WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 were queued/in progress at this reference; do not claim post-merge completion yet.
- Remaining open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. Their exact-head validation runs remain PASS: Platform #42161859747, #38575430454, #38567431761 and #38548718033; Auth #41329425940 PASS with Supabase Preview skipped. No open PRs remain in TCE, Stock or Media after #1037 merged.
- Direct `branches/master` API responses still show `protected=false`, `protection.enabled=false`, and required status checks enforcement off/empty on all five repositories. Repository metadata allows squash, merge commit and rebase. Administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only; no settings change was made.

### Current Platform reconciliation, credentials and runtime evidence

- Manual reconciliation [#43003088695](https://github.com/phanthienquoc/platform-infra/actions/runs/43003088695) ran on current Platform master `ff401dad` with `mode=apply`, `target_app=all`, `allow_image_changes=false`. It completed successfully at 10:24:29Z. GHCR read preflight passed for five packages: Auth service, MicroFE Shell, MicroFE WS, TCE service and TCE web.
- Auth runtime Secret was provisioned in `microfe-platform` and verified to contain required keys; values were suppressed. Shared `ghcr-pull` returned unchanged in both managed GHCR namespaces. The scoped image-pull restart check found no failures for the five managed MicroFE/TCE workloads.
- TCE GitOps release pairing passed for `prod-v0.1.0-e75e338`. Read-only Kubernetes diff reported no drift. Manifest apply, image replacement and workload rollout were skipped. The run therefore did not change production manifests or workloads, although Auth runtime Secret provisioning was a real cluster credential operation.
- Post-reconciliation node/pod inventory at 10:22:57Z showed node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1; Media backend/frontend 1/1; MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak intentional zero-replica maintenance; Stock Admin two ImagePullBackOff pods and desired Stock Backend one ImagePullBackOff pod, while legacy Stock Backend/Frontend remained 1/1.
- Stock desired admin image `ghcr.io/phanthienquoc/stockdividend/admin:12d63b4` still has no compatible platform descriptor. Do not promote local image IDs or cached tags as registry RepoDigest evidence. Stock scraper #42457182511 remains FAIL CLOSED on empty `VNSTOCK_API_KEY`; Stock CI #42610360402 PASS. Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Recovery [#43003328970](https://github.com/phanthienquoc/platform-infra/actions/runs/43003328970) completed SUCCESS. At its 10:24Z reference it correctly treated reconciliation #43003088695 as recent and read-only inspection fallback #42994074939 as fresh (age about 63m), so it dispatched no duplicate reconciliation or inspection. At 11:01:52Z, that reconciliation is now beyond the 20-minute recovery freshness window and inspection fallback #42994074939 is beyond the 75-minute inspection budget. The last full inspection is stale. The partial node/pod list from reconciliation is not a substitute for full disk/RAM/storage/runner inspection.

### TCE maintenance-aware recovery contract

- TCE native WF-06 [#43003016447](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/43003016447) failed all four strict public probes: TCE web, TCE API, Auth liveness and Auth readiness returned HTTP 503 instead of 200. TCE/Auth zero replicas are intentional maintenance; they are not live healthy.
- WF-12 run #43003045329 was a `workflow_run` delivery watchdog with zero measured queue wait, not a native schedule run. WF-13 recovery #43003045466 dispatched manual fallback WF-06 #43003071073, which reproduced the same four HTTP 503 responses.
- Merged TCE PR #1037 adds an explicit `TCE_MAINTENANCE_MODE` Actions-variable gate to WF-13. When set to `true`, it suppresses only the redundant read-only WF-06 fallback; strict WF-06 HTTP 200 probes and WF-12 native schedule monitoring remain unchanged. If unset/false, existing recovery behavior is preserved. The variable value was not changed or verified by this run; an authorized TCE repository administrator must set `TCE_MAINTENANCE_MODE=true` during the intentional zero-replica maintenance window, and unset/set false when services are reactivated.
- WF-01P now runs `scripts/validate-tce-health-recovery-contract.sh`; its PASS evidence covers YAML syntax, both maintenance guards, all four HTTP 200 expectations and unchanged WF-06/WF-12 cron expressions. No schedule or TCE market-scan schedule changed.

### Native schedule freshness

Reference: 2026-11-11 11:01:52 UTC. Only first-attempt `event=schedule` runs on `master` count. Current age is measured from `created_at`; inter-arrival is the latest minus previous native run.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | #42942147668 | 6,327 | 26,585 | 2,700 |
| Platform inspection | #42981286761 | #42932368784 | 12,046 | 25,617 | 4,500 |
| Platform recovery | #42986496462 | #42939222343 | 9,573 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | #42940581820 | 9,422 | 24,297 | 2,700 |
| TCE WF-06 | #43003016447 | #42949191917 | 2,389 | 26,842 | 1,500 |
| TCE WF-12 | #42996293386 | #42944415193 | 5,254 | 26,503 | 1,500 |

All six current-age budgets and all six inter-arrival budgets fail. TCE WF-06's latest native run did execute on schedule but failed public health; the WF-12 workflow_run receipt is not native schedule evidence. Do not count manual/workflow_run/repository_dispatch fallbacks as native delivery. No scheduler enqueue/delivery telemetry is available to attribute the gaps to GitHub scheduler delivery vs other causes. Preserve all cron expressions and the TCE market-scan schedule.

### Exact next actions and safety

1. Platform operator: run a fresh read-only `inspect-vps.yml` now; the last full fallback snapshot #42994074939 has exceeded 4,500s. Do not reboot/upgrade the host.
2. Platform operator: run `reconcile-vps.yml` on current master `ff401dad` in `mode=plan` before any new deployment decision; last successful current-master reconciliation #43003088695 is beyond the 20-minute recovery freshness window.
3. TCE repository administrator: set `TCE_MAINTENANCE_MODE=true` for the intentional zero-replica maintenance period; keep WF-06 strict and WF-12 active.
4. GitHub administrator: provide enqueue/delivery/Actions service telemetry and enforce master protection plus squash-only merge across all five repositories.
5. TCE/Auth owners: provide approved immutable release digests, rollback references and explicit recovery approval before reactivation.
6. Stock owner: confirm continued retirement vs restoration; if restored, provision `VNSTOCK_API_KEY` only via protected Actions Secrets and run safe preflight first.
7. Media owner: complete external backup/retention, authoritative DNS ownership and remote runner stop/disable/unregister evidence before deletion.

No new GHCR publication or digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, shared GHCR credential rotation, DNS/database/object-storage mutation or host reboot occurred. Auth runtime Secret provisioning/verification did occur in #43003088695; values were suppressed and shared `ghcr-pull` was unchanged. No workflow was removed or duplicate SSH/Compose authority added. Platform remains the sole production apply authority. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 18:05 ICT / 11:05:31 UTC

- PR #1632 was squash-merged at `c49bb0f1f1df71f403c64cc17fada8d4ab99bc31`; direct `refs/heads/master` read matches the merge SHA.
- Exact-head `validate-manifests` [#43008866804](https://github.com/phanthienquoc/platform-infra/actions/runs/43008866804) PASS on PR head `bd0cbf654ce7d78f33af4b562898020f6fb5dcb5`; post-merge current-master `validate-manifests` [#43008949806](https://github.com/phanthienquoc/platform-infra/actions/runs/43008949806) PASS on `c49bb0f1...`.
- The post-merge Platform run list contains `validate-manifests` only; no `reconcile-vps.yml` or `recover-stale-ops.yml` push run was triggered by this documentation-only merge.
- TCE PR #1037 was squash-merged at `5b425bdeab457e943bcecf1831836fc698e24394`. Post-merge master WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 all PASS. No GHCR publication occurred; the PR changed only health-recovery workflow behavior and its contract validation.
- This receipt advances the compact Platform master SHA and records TCE post-merge CI completion only. The 18:01 ICT / 11:01:52Z runtime and native-schedule snapshot remains the latest operational reference; this SHA sync does not refresh K3s or scheduler evidence.
- No production manifest, image, digest, Secret, workload, DNS, database, storage, namespace, runner or host state was changed by PR #1632. TCE market-scan schedule unchanged.


## Fresh K3s inspection — 2026-11-11 18:09 ICT / 11:09:26 UTC

- Read-only inspection [#42994074939 attempt 2](https://github.com/phanthienquoc/platform-infra/actions/runs/42994074939) completed SUCCESS; snapshot `debug/vps-latest.md` generated at 11:06:54Z (152s old at reference, within 4,500s budget). Inspection-only PR #1634 auto-squash-merged after exact-head validation #43009458775 PASS. Current Platform master: `388f96b7f7b0c97f461691b5862aff83b7d0b4f2`.

### Host/K3s

| Signal | Fresh evidence |
|---|---|
| Node | `tce-k3s-01` Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2 |
| OS/kernel | Ubuntu 22.04.5 LTS; 6.8.0-1049-oracle |
| Memory | 23Gi total, 19Gi available, 3.6Gi used |
| Disk | 45G total, 26G used, 20G available, 56%; pressure normal |
| Uptime | 193 days, 20:57 |
| Docker | 29.1.3; 20 images/9.195GB, 11 active, 5.773GB reclaimable; 12 containers; 5 volumes/66.2MB; 519.4MB build cache |
| Runners | Platform and Media runner services active/enabled; `rollout-status-v15-core-workloads` policy |
| Maintenance | `restart_required: yes`; kernel/containerd/Docker/OS updates pending |

Do not reboot/upgrade without an approved maintenance window. Do not clean reclaimable Docker/containerd data; verify retention and consumers first. Largest disk consumers: `/var/log` 1.8G (journal 1.5G), `/var/lib/rancher/k3s` 236M.

### Workload and digest inventory

| Workload | READY | Image evidence | State |
|---|---:|---|---|
| Media backend | 1/1 | `prod-v0.3.0-58f80a8@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d` | Running |
| Media frontend | 1/1 | `prod-v0.3.0-58f80a8@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a` | Running |
| MicroFE Shell | 1/1 | `microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd` | Running |
| MicroFE WS | 1/1 | `microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d` | Running |
| MicroFE NATS | 1/1 | `nats@sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6` | Running |
| TCE frontend/service | 0/0 | — | Intentional maintenance; not healthy |
| Auth / Keycloak | 0/0 | — | Intentional maintenance; not healthy |
| Stock Admin (2) | 0/1 each | `admin:12d63b4`, no imageID digest | ImagePullBackOff |
| Stock desired Backend | 0/1 | `backend:12d63b4`, no imageID digest | ImagePullBackOff |
| Stock legacy Backend | 1/1 | `backend:23b2878`, local imageID only | Running; not promotion evidence |
| Stock legacy Frontend | 1/1 | `user:23b2878`, local imageID only | Running; not promotion evidence |

Stock desired images still lack compatible registry descriptors. Local SHA image IDs are not GHCR RepoDigest values. Preserve `k3s-debug/k3s-debug-logs` PVC/PV (Bound, 1Gi, RWO, local-path).

### Cross-repo refs, PRs and CI

- Platform `388f96b7f7b0c97f461691b5862aff83b7d0b4f2`; TCE `5b425bdeab457e943bcecf1831836fc698e24394`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Auth `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open owner-decision drafts: Platform #1314/#544/#541/#539 and Auth #76. TCE #1037 and Platform docs #1632/#1633 plus inspection #1634 are merged; no Stock/Media PRs.
- Platform #1632 exact-head #43008866804 and post-merge #43008949806 PASS; #1633 exact-head #43009127491 and post-merge #43009271130 PASS; inspection #1634 exact-head #43009458775 PASS (debug snapshot only).
- TCE #1037 exact-head WF-01P #43008284677, WF-02 #43008284672, WF-05 #43008284792, WF-08B #43008284695 PASS; post-merge WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 PASS. Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- All five master branches remain `protected=false`, required checks enforcement off/empty; merge commit and rebase still allowed. GitHub administrator action required.

### Native schedule — 11:09:26 UTC

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | 6,781 | 26,585 | 2,700 |
| Platform inspection | #42981286761 | 12,500 | 25,617 | 4,500 |
| Platform recovery | #42986496462 | 10,027 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | 9,876 | 24,297 | 2,700 |
| TCE WF-06 | #43003016447 | 2,843 | 26,842 | 1,500 |
| TCE WF-12 | #42996293386 | 5,708 | 26,503 | 1,500 |

All six current-age and inter-arrival budgets fail. Manual inspection rerun is not native schedule evidence. TCE WF-06 executed on schedule but failed four strict HTTP 200 probes with 503; WF-12 workflow_run #43003045329 is not a native schedule run. No cron or TCE market-scan schedule changed.

### Exact next actions and safety

1. Platform operator: run current-master `reconcile-vps.yml` in `mode=plan` before any apply decision. Last current-master reconciliation #43003088695 ran on prior master `ff401dad` and is beyond the 20-minute recovery freshness window.
2. Platform operator: obtain maintenance approval before host restart/upgrade; no reboot or image cleanup.
3. TCE administrator: set `TCE_MAINTENANCE_MODE=true` during intentional zero-replica maintenance; unset/set false on reactivation. Variable value was not changed or verified.
4. GitHub administrator: provide scheduler enqueue/delivery telemetry and enforce PR-only, required checks, force-push/deletion protection and squash-only across all five repositories.
5. TCE/Auth owners: provide immutable release digests, rollback references and explicit reactivation approval.
6. Stock owner: decide retirement vs restoration; if restoring, provision `VNSTOCK_API_KEY` only through protected Actions Secrets and run safe preflight first.
7. Media owner: complete external backup/retention, DNS ownership and remote runner unregister before retirement/deletion.

No GHCR publication, digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, shared GHCR credential rotation, DNS/database/object-storage mutation or host reboot. Auth runtime Secret provisioning/verification occurred earlier in #43003088695 with values suppressed; shared `ghcr-pull` was unchanged. Platform remains sole production apply authority; no direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 19:01 ICT / 12:01:39 UTC

### Repository refs, open PRs and latest workflow evidence

| Repository | Current master | Open PRs | Latest relevant workflow evidence |
|---|---|---|---|
| Platform Infra | `8da047c223a2c10b5e0dd6a08aa8770fbc7f92c1` | #1314, #544, #541, #539 (all drafts/owner decisions) | Current-master `validate-manifests` #43009993417 PASS. Latest native reconcile #42993779924, inspection #42981286761, recovery #42986496462 and watchdog #42986833403. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | None | Master WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 PASS. Native WF-06 #43003016447 FAIL; WF-12 #42996293386 FAIL. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | None | CI #42610360402 PASS; weekend scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | None | CI #42539512417 PASS. Last full K3s snapshot shows digest-pinned backend/frontend 1/1; runner remains active. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft/owner decision) | CI #42654579277 PASS; Auth remains intentional 0/0 maintenance. |

Open Platform PR exact-head validations remain PASS: #1314 run #42161859747, #544 #38575430454, #541 #38567431761 and #539 #38548718033. Authentication PR #76 run #41329425940 PASS; Supabase Preview remains skipped by design. Keep all five owner-decision drafts unmerged.

### Native schedule freshness — reference 12:01:39 UTC

| Lane | Latest native run | Latest created_at (UTC) | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile | #42993779924 | 09:16:25 | 9,914 | 26,585 | 2,700 |
| Platform inspection | #42981286761 | 07:41:06 | 15,633 | 25,617 | 4,500 |
| Platform recovery | #42986496462 | 08:22:19 | 13,160 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | 08:24:50 | 13,009 | 24,297 | 2,700 |
| TCE WF-06 | #43003016447 | 10:22:03 | 5,976 | 26,842 | 1,500 |
| TCE WF-12 | #42996293386 | 09:34:18 | 8,841 | 26,503 | 1,500 |

All six current-age and inter-arrival budgets fail. These are native `event=schedule` runs; manual, push, `workflow_run` and `repository_dispatch` are not substitutes. The Platform watchdog log #42986833403 independently reports the four Platform inter-arrival failures. TCE WF-12 log #42996293386 reports its latest WF-06 source #42949191917 was 399 minutes old while measured runner queue was 0 minutes; this supports a delivery/freshness gap rather than runner queue congestion. No GitHub scheduler enqueue/delivery telemetry is available to attribute the root cause.

TCE WF-06 #43003016447 logs confirm all four strict public probes returned HTTP 503 (TCE web, TCE API, Auth liveness and Auth readiness; expected 200). Keep the strict HTTP 200 contract. The TCE maintenance-aware WF-13 contract from PR #1037 is merged, but the repository variable `TCE_MAINTENANCE_MODE` could not be read through the available connection and its value remains unverified. Do not infer it is set.

### K3s inspection and GitOps evidence

- Full read-only snapshot #42994074939, `debug/vps-latest.md` generated 2026-11-11T11:06:54Z. At 12:01:39Z it is 3,285s old against a 4,500s freshness budget (1,215s remaining; expires at 12:21:54Z). This was a `workflow_dispatch` inspection, not native schedule delivery.
- Node `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2. Memory 23Gi total / 19Gi available; disk 45G total / 26G used / 20G available (56%, pressure normal). Host restart and OS/kernel/containerd/Docker updates are pending; no reboot or upgrade without an approved maintenance window.
- Platform and Media runner services are active/enabled. Docker inventory: 20 images / 9.195GB, 5.773GB reclaimable, 12 containers, 5 volumes and 519.4MB build cache. No cleanup performed.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry digest references. TCE frontend/service, Auth and Keycloak are 0/0 maintenance, not healthy. Stock Admin (2 pods) and desired Backend (1 pod) remain ImagePullBackOff on `12d63b4` without registry RepoDigest. Legacy Stock Backend/Frontend are 1/1 but only have local image IDs, not promotion evidence.
- Preserve Bound PVC `k3s-debug/k3s-debug-logs` (1Gi, RWO, local-path). Media runner remote unregister, external backup/retention and authoritative DNS ownership remain unverified.

Latest successful full reconciliation #43003088695 was a `workflow_dispatch` on older Platform SHA `ff401dad`, not current master `8da047c2`; at 12:01:39Z it was 5,945s old, beyond the 20-minute recovery freshness window. It verified five GHCR packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, found drift=false and skipped apply/image replacement/rollout. It does not authorize a current-master rollout. Current `.github/workflows/reconcile-vps.yml` manual default is `mode=plan`; run a current-master plan before any apply decision.

### Governance and exact next actions

- Repository metadata still allows squash, merge commit and rebase. Direct branch-protection GET returned HTTP 403 (Resource not accessible by integration) on all five repositories; effective inherited rulesets therefore cannot be independently confirmed by this connection. GitHub administrator must verify/enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.
- Platform operator: run fresh read-only `inspect-vps.yml` before snapshot #42994074939 expires at 12:21:54Z, then run `reconcile-vps.yml` on current master `8da047c2` in `mode=plan`. No workflow dispatch was issued in this run.
- GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry and enforce master governance.
- TCE administrator: verify/set `TCE_MAINTENANCE_MODE=true` only while zero-replica maintenance is intentional; unset it before reactivation. Keep WF-06 strict and WF-12 scheduled.
- TCE/Auth owners: provide approved immutable release digests, rollback references and explicit recovery approval before reactivation.
- Stock owner: decide retirement vs restoration; if restored, provision `VNSTOCK_API_KEY` only through protected Actions Secrets and run safe preflight.
- Media owner: complete external backup/retention, authoritative DNS ownership and remote runner unregister before retirement/deletion.

No new GHCR publication or digest promotion, current-master production apply, workload rollout, namespace/PVC/PV deletion, runner retirement, shared GHCR credential rotation, DNS/database/object-storage mutation or host reboot occurred. No workflow was added/removed, no direct SSH/Compose authority was introduced, and the TCE market-scan schedule is unchanged. Platform remains the sole production apply authority.


## Post-merge verification — 2026-11-11 19:09 ICT / 12:09:43 UTC

- PR #1636 (19:01 readiness refresh) squash-merged at `f866e33131557bede21c15df588c764a28199907`. Exact-head `validate-manifests` #43017483631 PASS; post-merge master `validate-manifests` #43017580624 PASS.
- PR #1637 (schedule-gap correction) squash-merged at `815f87e14832d35970f3e43b8e9c309301b0fc81`. Exact-head `validate-manifests` #43017776105 PASS; post-merge master `validate-manifests` #43017854916 PASS.
- Direct `refs/heads/master` read matches final merge SHA `815f87e14832d35970f3e43b8e9c309301b0fc81`. Both post-merge runs contain `validate-manifests` only; no `reconcile-vps.yml` or `recover-stale-ops.yml` push run was triggered by these docs-only merges.
- PR #1637 corrected the 19:01 schedule table to use the interval ending at each latest native run: Platform reconcile 26,585s; TCE WF-06 26,842s; TCE WF-12 26,503s. Platform inspection 25,617s, recovery 24,822s and watchdog 24,297s remain unchanged. All six inter-arrival budgets still fail.
- No new native schedule runs appeared in the Actions run list by 12:09:43Z. Current ages are: Platform reconcile 10,398s; inspection 16,117s; recovery 13,644s; watchdog 13,493s; TCE WF-06 6,460s; WF-12 9,325s. All six current-age budgets fail.
- K3s snapshot #42994074939 generated 11:06:54Z is 3,769s old / 4,500s budget at 12:09:43Z; 731s remain, with expiry at 12:21:54Z. Last reconciliation #43003088695 is 6,429s old and ran on pre-current master `ff401dad`, not `815f87e`; it cannot authorize current-master rollout.
- This receipt advances only documentation provenance/current master SHA. No runtime, image, credential, manifest, workflow schedule or production resource changed. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 19:59 ICT / 12:59:10 UTC

### Direct repository refs and open PRs

- Direct `refs/heads/master`: Platform Infra `47052106687e95a151da731f8fd28cddd872fbe6`; TCE Dashboard `5b425bdeab457e943bcecf1831836fc698e24394`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314 (head `db152c9a`), #544 (`c95e7dae`), #541 (`b8f7c6ba`), #539 (`2dc48b97`); Authentication #76 (head `f19cacb0`). All are drafts/owner decisions. TCE, Stock and Media have no open PRs.
- Current exact-head check-runs: Platform #1314 `validate` #42161859747 PASS; #544 #38575430454 PASS; #541 #38567431761 PASS; #539 #38548718033 PASS. Auth #76 `validate` #41329425940 PASS; Supabase Preview is SKIPPED by design. These checks are historical but remain attached to unchanged PR heads.
- Platform current-master `validate-manifests` #43018649706 PASS on `47052106687e95a151da731f8fd28cddd872fbe6`. No newer Platform workflow run appeared in the latest 30-run query; no current-master inspection or reconciliation is evidenced.

### Latest app workflow evidence

- TCE master `5b425bdeab457e943bcecf1831836fc698e24394`: WF-01 #43008514423, WF-02 #43008514481 and WF-05 #43008514459 PASS. Latest WF-12 workflow_run #43019107548 and WF-13 workflow_run #43019140175 are SKIPPED, not native schedule deliveries. Last first-attempt native WF-06 schedule run is #42949191917 (FAIL); #43003016447 is a schedule event but attempt 2 and is excluded from first-attempt cadence. Latest first-attempt native WF-12 schedule run is #42996293386 (FAIL). Manual WF-06 #43003071073 failed all four strict HTTP 200 probes: TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503. The current value of repository variable `TCE_MAINTENANCE_MODE` is not readable through this connection and remains unverified.
- Stock CI #42610360402 PASS. Scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty; do not bypass the credential gate or place secrets in Git/logs/chat.
- Media CI #42539512417 PASS. The last full K3s snapshot shows Media backend/frontend 1/1 with registry-resolved RepoDigests. Media runner service/listener is active/enabled; GitHub-side unregister, external backup/retention and authoritative DNS ownership are not verified.
- Authentication CI #42654579277 PASS. Auth remains 0/0 maintenance in the last full snapshot; historical Auth runtime Secret provision/verification succeeded in reconciliation #43003088695 with values suppressed. This is not current-master or current-freshness evidence.

### Native schedule freshness

Reference: 2026-11-11 12:59:10 UTC. Only first-attempt `event=schedule` runs on `master` count. Workflow_dispatch, rerun attempts, workflow_run, push and repository_dispatch do not substitute.

| Lane | Latest qualifying native run | Current age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #42993779924 | 13,365 | 26,585 | 2,700 | FAIL |
| Platform inspection | #42981286761 | 19,084 | 25,617 | 4,500 | FAIL |
| Platform recovery | #42986496462 | 16,611 | 24,822 | 2,700 | FAIL |
| Platform watchdog | #42986833403 | 16,460 | 24,297 | 2,700 | FAIL |
| TCE WF-06 | #42949191917 | 36,269 | 12,853 | 1,500 | FAIL |
| TCE WF-12 | #42996293386 | 12,292 | 26,503 | 1,500 | FAIL |

All six current-age and all six inter-arrival budgets fail. WF-06 #43003016447 has `event=schedule` but `run_attempt=2`; it is not a qualifying first-attempt native delivery. WF-12 #43019107548 is `workflow_run` and SKIPPED. Do not count these as schedule freshness. Preserve every cron expression and the TCE market-scan schedule.

### K3s inspection and reconciliation freshness

- Latest full snapshot: inspection #42994074939, attempt 2, generated `2026-11-11T11:06:54Z`. At reference it is 6,736s old against a 4,500s budget (expired by 2,236s). It is a workflow_dispatch rerun, not native schedule evidence. No fresh full inspection is available for a current runtime decision.
- Last reconciliation #43003088695 was created 10:22:34Z, 9,396s old against a 2,700s budget; it ran on pre-current Platform SHA `ff401dadb1cac5b0647c1a4187fe171b2cfbc937`, not current master `47052106687e95a151da731f8fd28cddd872fbe6`. It reported GHCR read preflight PASS for five packages, Auth runtime Secret provision/verification with values suppressed, shared `ghcr-pull` unchanged, TCE release pairing PASS, GitOps drift=false and manifest apply/image replacement/rollout skipped. It is historical evidence only, not current-master authorization.
- Last-known K3s node `tce-k3s-01` was Ready/ARM64, Ubuntu 22.04.5, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% / about 20 GiB free, RAM about 19 GiB available, host restart required and package/kernel updates pending. This snapshot is stale; do not treat these as live values.
- Last-known workloads: Media backend/frontend and MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin two pods and desired Backend one pod ImagePullBackOff on tag `12d63b4`; legacy Stock Backend/Frontend 1/1. Media/MicroFE have registry RepoDigest evidence. Failed Stock desired pods have no RepoDigest; legacy Stock image IDs are local IDs, not promotion evidence.
- Preserve PVC `k3s-debug/k3s-debug-logs` (Bound, 1Gi, RWO, local-path). Do not cleanup Docker images, reboot host, delete namespaces/PVC/PV, or retire runners from stale evidence. Media and Platform runner services were active/enabled in the snapshot; remote unregister and external backup/retention/DNS ownership remain unverified.

### Branch governance and production authority

- Direct `branches/master` responses report `protected=false`, `protection.enabled=false`, and required status checks enforcement off/empty for all five repositories. Repository metadata allows squash, merge commits and rebase. Effective inherited organization ruleset enforcement is not confirmed; administrator action is required.
- GitHub administrator: enforce PR-only updates, required CI/deployment-contract checks, force-push/deletion protection and squash-only merge; provide scheduler enqueue/delivery/Actions service telemetry.
- Platform operator: obtain a fresh read-only `inspect-vps.yml` run and a current-master `reconcile-vps.yml` `mode=plan` run before any production decision. The available GitHub connection in this run exposes read and PR operations but no workflow-dispatch action; no dispatch was fabricated.
- TCE/Auth owners: decide whether to keep maintenance or reactivate; if reactivating, provide immutable release digests, rollback references and explicit approval. TCE administrator must verify/set `TCE_MAINTENANCE_MODE` through repository settings; this connection cannot read the variable.
- Stock owner: confirm retirement vs restoration. If restoration is approved, provision `VNSTOCK_API_KEY` only through protected Actions Secrets and run preflight before any image publication.
- Media owner: complete external backup/retention, authoritative DNS and GitHub runner unregister evidence before decommissioning.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra remains the sole production manifest, shared pull-credential, digest promotion, GitOps apply, rollout and health authority. No direct SSH/Compose authority.

No new image publication, digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint. No workflow was added or removed. TCE market-scan schedule unchanged.


## Post-merge receipt — 2026-11-11 20:05 ICT / 13:05:10 UTC

- PR #1639 was squash-merged from exact head `cd1ef6a43984922d567b65d862ad0956c5ac040f` to master at `11aab7a9241621dcd09cb580b2760f76f198edd0`.
- Exact-head `validate-manifests` #43025767904 PASS. Post-merge master `validate-manifests` #43025893643 PASS on the exact merge SHA.
- Post-merge workflow run contains `validate` PASS and `report-validation-failure` SKIPPED. Only manifest validation ran; no production reconcile/recovery push was triggered by this docs-only merge.
- The 19:59 ICT checkpoint remains the latest runtime and schedule evidence. This receipt advances documentation/master provenance only; it does not refresh K3s inspection, GitOps reconciliation, schedule cadence or public health.
- No production manifest, image, Secret, workload, DNS, database, storage, namespace, runner or host state changed. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 21:03 ICT / 14:03:27 UTC

### Direct repository refs, open PRs and latest checks

- Direct `refs/heads/master`: Platform Infra `be9a5fba7feb057a6f4ee94f90836804baeb2b66`; TCE Dashboard `5b425bdeab457e943bcecf1831836fc698e24394`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open owner-decision drafts: Platform #1314 (head `db152c9a17416d1a7f82165597dfe478321bd055`), #544 (`c95e7daecb83b65577b54303427fe4ea81adfe06`), #541 (`b8f7c6ba04e3d971336a899b2efd5894662083b3`), #539 (`2dc48b97017ecb08e49682633303a2f1d5e991a1`); Authentication #76 (`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`). TCE, Stock and Media have no open PRs. Keep all five drafts unmerged pending their documented owner decisions.
- Exact-head validation runs on unchanged PR heads remain PASS: Platform #1314 #42161859747; #544 #38575430454; #541 #38567431761; #539 #38548718033; Auth #76 #41329425940 (Supabase Preview SKIPPED by design). These are historical check receipts, not new checks on this run.
- Platform current-master `validate-manifests` #43026129602 PASS on `be9a5fba7feb057a6f4ee94f90836804baeb2b66`. TCE latest master WF-01 #43008514423, WF-02 #43008514481 and WF-05 #43008514459 PASS; latest WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED. Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty. Media CI #42539512417 PASS. Auth CI #42654579277 PASS.
- TCE native health evidence: first-attempt scheduled WF-06 #42949191917 failed; schedule-event attempt 2 #43003016447 also failed but is excluded from first-attempt cadence. Latest qualifying native WF-12 is #42996293386 (failure). WF-12 #43019107548 was a workflow_run/SKIPPED receipt, and WF-13 #43019140175 was skipped because its source workflow_run was skipped; neither proves the maintenance variable was read. The current Actions variable `TCE_MAINTENANCE_MODE` remains unverified. Manual WF-06 #43003071073 returned HTTP 503 from all four strict endpoints; do not relax expected HTTP 200 or count maintenance as healthy.

### Native schedule freshness

Reference: 2026-11-11 14:03:27 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run, repository_dispatch and rerun attempts do not substitute.

| Lane | Latest qualifying native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | #42942147668 | 17,222 | 26,585 | 2,700 |
| Platform inspection | #42981286761 | #42932368784 | 22,941 | 25,617 | 4,500 |
| Platform recovery | #42986496462 | #42939222343 | 20,468 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | #42940581820 | 20,317 | 24,297 | 2,700 |
| TCE WF-06 | #42949191917 | #42922537816 | 40,126 | 12,853 | 1,500 |
| TCE WF-12 | #42996293386 | #42944415193 | 16,149 | 26,503 | 1,500 |

All six current-age and all six inter-arrival budgets fail. Latest native runs are on master; newer workflow_run/manual/rerun receipts are excluded. No cron expression or TCE market-scan schedule was changed.

### K3s inspection and GitOps reconciliation freshness

- Latest full read-only inspection #42994074939 succeeded on attempt 2. GitHub reports the rerun started at `2026-11-11T11:06:45Z`; snapshot generation is approximately `11:06:54Z`. At the reference, snapshot age is 10,593s against a 4,500s budget (expired by 6,093s). It ran on pre-current Platform SHA `c557b3f3...`, not current master `be9a5fba...`.
- Historical inspection state only: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; Ubuntu 22.04.5; disk 56% / about 20 GiB free; RAM about 19 GiB available; host restart required and package/kernel/containerd/Docker updates pending. Media backend/frontend and MicroFE Shell/WS/NATS were 1/1; TCE/Auth/Keycloak were 0/0 maintenance; Stock Admin (two pods) and desired Backend (one pod) were ImagePullBackOff; legacy Stock Backend/Frontend were 1/1. Media runner service/listener was active/enabled. Preserve PVC `k3s-debug/k3s-debug-logs` (Bound, 1Gi, RWO, local-path). These values are stale and must not be treated as current runtime health.
- Last full reconciliation #43003088695 completed successfully at `2026-11-11T10:24:29Z`, created at `10:22:34Z`, on old Platform SHA `ff401dad...`. At reference it is 13,253s old against the 2,700s recovery freshness budget (expired by 10,553s). It passed GHCR read preflight for five packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, passed TCE release pairing, found drift=false and skipped manifest apply/image replacement/rollout. It is historical evidence only and cannot authorize current-master deployment.
- No current-master `inspect-vps.yml` or `reconcile-vps.yml` plan run is present in the latest Actions history. This run's GitHub connector exposes repository reads and PR/file operations but no workflow-dispatch action; no inspection or reconciliation dispatch was fabricated.

### Branch governance and authority

- `get_repo` metadata for all five repositories confirms squash, merge commit and rebase are enabled. Direct `branches/master/protection` GET returns HTTP 403 for all five; repo-level rulesets GET returns `[]` for the four public repositories and HTTP 403 for private StockDividend. Organization-level inherited ruleset coverage cannot be verified through this connection. Do not claim that inherited rulesets are absent; GitHub administrator must verify/enforce PR-only, required checks, force-push/deletion protection and squash-only.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra remains the sole production manifest, shared GHCR pull credential, digest/provenance promotion, GitOps plan/apply, rollout and runtime health authority. Preserve CI, security, release, backup, integration, native schedule, manual plan/apply and guarded operations. No workflow is confirmed redundant/obsolete; no direct SSH/Compose authority.
- No new GHCR publication or digest promotion, current-master production apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 22:03 ICT / 15:03:23 UTC

### PR #1641 and current master

- PR #1641 [cross-repo readiness at 21:03 ICT](https://github.com/phanthienquoc/platform-infra/pull/1641) was squash-merged after re-reading its exact head `f2e303413f6bee4feb3e7622ff87717d238e17bf` and verifying the complete `validate` job in run #43035377158 PASS. All contract steps passed, including retired Stock/Media manifest guard, immutable image-change contract, Auth digest promotion, TCE/Auth dispatch payload, offline dependency installation, shell checks, manifest rendering, Auth GitOps, YAML/secret/immutable-image/Keycloak/network validation. `report-validation-failure` was SKIPPED as expected.
- Merge SHA and direct `refs/heads/master`: `1fdc57a8dc098fa5fdc1749f0e11ff0714209e42`.
- Current-master `validate-manifests` run #43044426610 was queued at 15:03:03Z and is IN_PROGRESS at this checkpoint. Initial steps passed; offline dependency installation and subsequent rendering/security checks were still running. Do not record post-merge validation PASS until this run completes.
- Open PRs after #1641 merge: Platform #1314/#544/#541/#539 (draft/owner decision); Authentication #76 (draft/owner decision); none in TCE, Stock or Media. Exact-head checks on owner-decision drafts are historical and do not authorize merging.

### Direct master refs across all five repositories

- Platform Infra: `1fdc57a8dc098fa5fdc1749f0e11ff0714209e42`.
- TCE Dashboard: `5b425bdeab457e943bcecf1831836fc698e24394`.
- StockDividend: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`.
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`.
- Authentication: `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.

### Native schedule evidence

Only first-attempt `event=schedule` runs on `master` count. Reference: 2026-11-11 15:03:23 UTC.

| Lane | Latest native run | Age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | 20,798 | 26,585 | 2,700 |
| Platform inspection | #42981286761 | 26,517 | 25,617 | 4,500 |
| Platform recovery | #42986496462 | 24,044 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | 23,893 | 24,297 | 2,700 |
| TCE WF-06 | #42949191917 | 43,702 | 12,853 | 1,500 |
| TCE WF-12 | #42996293386 | 19,725 | 26,503 | 1,500 |

All six age budgets and all six inter-arrival budgets fail. TCE WF-06 attempt 2 #43003016447 is excluded from native first-attempt cadence; WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED and do not substitute. No cron, freshness budget or TCE market-scan schedule changed.

### Runtime evidence freshness

- Latest full inspection #42994074939 attempt 2 produced snapshot at 11:06:54Z; age 14,189s against 4,500s budget. It is expired. Last-known state remains historical only: node Ready/ARM64, disk 56% (~20GiB free), ~19GiB RAM available; host restart required; Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock desired Admin/Backend ImagePullBackOff; Media runner active/enabled; preserve Bound PVC `k3s-debug/k3s-debug-logs` (1Gi, RWO, local-path).
- Latest full reconciliation #43003088695 completed at 10:24:29Z on old Platform SHA `ff401dad...`; age 16,734s against 2,700s budget. Historical GHCR preflight passed for five packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing passed; drift=false; manifest apply, image replacement and rollout skipped. It cannot authorize current master.
- No current-master inspection or GitOps plan/apply is evidenced. The current connection has no workflow-dispatch action; no run was fabricated.

### Governance and safety

- All five repo metadata records allow squash, merge commit and rebase. Branch-protection GET returned HTTP 403 for all five; repo-level rulesets returned [] for public Platform/TCE/Media/Auth and HTTP 403 for private Stock. Effective organization-level inherited rulesets remain unverified. Administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot. No workflow was removed or added; no SSH/Compose authority introduced.
- TCE market-scan schedule unchanged. Platform Infra remains the sole production apply authority.

### Exact next actions

1. Wait for current-master validation #43044426610 to complete; record the actual final conclusion and inspect failed job logs if any.
2. Platform operator: run fresh read-only `inspect-vps.yml`, then run `reconcile-vps.yml` on current master `1fdc57a8` with `mode=plan`; do not apply before reviewing current evidence and approval.
3. GitHub administrator: provide scheduler enqueue/delivery/Actions-service telemetry and enforce master protection/squash-only.
4. TCE administrator: verify `TCE_MAINTENANCE_MODE` in repository Actions variables; do not infer it from skipped WF-13.
5. TCE/Auth owners: provide immutable release digests, rollback references and explicit recovery approval before reactivation.
6. Stock owner: decide retirement versus restoration; keep scraper fail-closed and do not publish images pending owner decision.
7. Media owner: complete remote runner unregister, backup/retention and authoritative DNS evidence before retirement.


## Latest verification — 2026-11-11 23:09 ICT / 16:09:29 UTC

### Direct refs, open PRs and validations

- Platform Infra master: `4cb817cba48119b04a38ba3ca1beefa579381571`. PR #1642 [post-merge readiness sync](https://github.com/phanthienquoc/platform-infra/pull/1642) squash-merged at `746596aa9cfd9425cf4cd7d9bc4217938b9c1a39`; current-master validation #43054650479 completed PASS on that SHA. PR #1643 [fresh VPS inspection](https://github.com/phanthienquoc/platform-infra/pull/1643) exact-head validation #43054831431 completed PASS on head `f2de932c29aaacaa18b23bffa621205b4f293189`, then squash-merged at `4cb817cba48119b04a38ba3ca1beefa579381571` (merged 16:09:20Z). Native inspection run #43054529460 completed SUCCESS.
- No post-merge `validate-manifests` run on SHA `4cb817c` is present in the latest run listing. #43054650479 is a PASS on parent SHA `746596aa`; #43054831431 is exact-head PASS for the inspection PR. Do not conflate either with a current-master manifest validation on `4cb817c`.
- Direct master refs: Platform `4cb817cba48119b04a38ba3ca1beefa579381571`; TCE `5b425bdeab457e943bcecf1831836fc698e24394`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314/#544/#541/#539 (draft/owner decision); Authentication #76 (draft/owner decision); none in TCE/Stock/Media. Do not merge owner-decision drafts without owner approval.

### Native schedule evidence

Reference: 2026-11-11 16:07:41 UTC. Only first-attempt `event=schedule` runs on `master` count.

| Lane | Latest qualifying run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | 24,676 | 26,585 | 2,700 |
| Platform inspection | #43054529460 | 236 | 30,159 | 4,500 |
| Platform recovery | #42986496462 | 27,922 | 24,822 | 2,700 |
| Platform watchdog | #42986833403 | 27,771 | 24,297 | 2,700 |
| TCE WF-06 | #42949191917 | 47,580 | 12,853 | 1,500 |
| TCE WF-12 | #42996293386 | 23,603 | 26,503 | 1,500 |

All six inter-arrival gaps fail; five of six current-age budgets fail. New inspection run #43054529460 is a qualifying native schedule event and brings the inspection current-age within budget, but its 30,159s inter-arrival gap remains out of budget. The expected Platform reconcile event at minute 07 had not appeared in the schedule listing at 16:07:41Z. WF-06 attempt 2 #43003016447, WF-12 workflow_run/SKIPPED #43019107548 and WF-13 workflow_run/SKIPPED #43019140175 are excluded. Preserve all cron expressions and TCE market-scan schedule.

### Fresh K3s inspection — snapshot generated 2026-11-11T16:03:55Z

- Node `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5 LTS; kernel `6.8.0-1049-oracle`; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`; Docker `29.1.3`.
- Resources: 23Gi RAM, ~19Gi available; root disk 45Gi, 26Gi used, 20Gi available (56%); disk pressure normal. Host uptime 194d 1h54m; `restart_required: yes`; package updates include containerd, Docker and Ubuntu components. No reboot or upgrade.
- Docker inventory: 20 images / 9.195GB, 5.773GB reclaimable; 12 active containers, 5 volumes, 519.4MB build cache. No cleanup.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running. Registry RepoDigests: Media backend `sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d`; Media frontend `sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a`; MicroFE Shell `sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd`; MicroFE WS `sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d`; NATS `sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6`.
- TCE frontend/service, MicroFE Auth and Keycloak remain 0/0. Public OIDC probes return HTTP 503. Do not call maintenance workloads healthy.
- Stock Admin deployment is 0/1 with two pods ImagePullBackOff; desired Stock Backend has one ImagePullBackOff pod. Desired `admin:12d63b4` and `backend:12d63b4` report `no match for platform in manifest` and have no RepoDigest. Legacy Backend/Frontend remain 1/1, but only local image IDs are present; they are not registry digest evidence.
- PVC `k3s-debug/k3s-debug-logs` remains Bound (1Gi, RWO, local-path). Stock/Media preflight reports no PVC/PV claims or VolumeSnapshot references in those namespaces; external backup/retention and authoritative DNS ownership remain unverified.
- Platform and Media runner services/listeners are active/enabled. Remote GitHub runner registration/unregistration is not proven by host inspection.

### GitOps, credentials and authority

- Historical full reconciliation #43003088695 ran on old Platform SHA `ff401dad`; its GHCR read preflight passed five packages, Auth runtime Secret was provisioned/verified with values suppressed, shared `ghcr-pull` was unchanged, TCE release pairing passed, drift=false, and apply/image replacement/rollout were skipped. It is expired and cannot authorize current master.
- No current-master `reconcile-vps.yml` `mode=plan` or apply is evidenced. The current GitHub connector has no workflow-dispatch action; no dispatch/run was fabricated.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and runtime health verification.
- All five repository metadata records still allow squash, merge commit and rebase. Branch-protection GET returned HTTP 403; effective inherited organization rulesets remain unverified. Administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.
- No new GHCR publication or digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow was removed or added; no SSH/Compose authority. TCE market-scan schedule unchanged.

### Exact next actions

1. Platform operator: run current-master `reconcile-vps.yml` in `mode=plan` on `4cb817c`; review output before any apply. Obtain a post-merge manifest validation on `4cb817c` if the workflow path policy did not trigger one.
2. GitHub administrator: provide scheduler enqueue/delivery telemetry; enforce PR-only, required checks, force-push/deletion protection and squash-only across all five repositories.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE` in repository Actions variables; do not infer it from WF-13 SKIPPED.
4. TCE/Auth owners: provide immutable release digests, rollback references and explicit recovery approval before reactivation.
5. Stock owner: decide retirement versus restoration; keep scraper fail-closed on missing `VNSTOCK_API_KEY` and do not publish/promote while decision is unresolved.
6. Media owner: verify remote runner unregister, backup/retention and authoritative DNS before retirement.
7. Platform operator: obtain maintenance approval before host restart/package upgrades; preserve PVC `k3s-debug/k3s-debug-logs`.


## Latest verification — 2026-11-12 00:06 ICT / 17:06:33 UTC

### Direct refs, PRs and validation

- Direct `refs/heads/master`: Platform Infra `e6163feea2dabaeaa9abbdc8192b1da74ea0cbb1`; TCE Dashboard `5b425bdeab457e943bcecf1831836fc698e24394`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform PR #1644 was squash-merged at `e6163feea2dabaeaa9abbdc8192b1da74ea0cbb1`. Exact-head `validate-manifests` #43055819417 PASS; post-merge #43064658676 PASS on current master. Changed-image validation was skipped because the PR was documentation-only.
- Open owner-decision drafts remain Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE/Stock/Media. Do not merge owner-decision work without the relevant owner decision.
- Latest Platform master branch API still reports `protected=false` and required status-check enforcement off. Repository metadata allows squash, merge commit and rebase on all five repositories; effective inherited organization rulesets remain unverified.

### Latest workflow and GitOps evidence

- Manual reconciliation [#43055528687](https://github.com/phanthienquoc/platform-infra/actions/runs/43055528687) completed SUCCESS at 16:09:44Z on parent Platform SHA `4cb817c`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`. Runner policy v15 was ready. GHCR read preflight passed for five managed packages (Auth, MicroFE Shell/WS, TCE service/web). Auth runtime Secret was provisioned and verified with values suppressed. Shared `ghcr-pull` remained unchanged; service-account/deployment patches reported no change. TCE GitOps image verification passed. TCE/Auth were explicitly treated as intentional zero-replica maintenance; no live workload health was asserted. Auth TLS verification passed; MicroFE health passed for one active scope.
- The reconciliation found no manifest drift. Production manifest apply, image replacement and rollout steps were skipped. The run is 3,409s old at reference, beyond the 2,700s reconciliation freshness budget, and ran on `4cb817c`, not current master `e6163fe`. It does not authorize a current-master deployment.
- Recovery [#43058737375](https://github.com/phanthienquoc/platform-infra/actions/runs/43058737375) completed SUCCESS as `workflow_run`. At its 16:28:56Z reference, it correctly avoided duplicate reconciliation because manual run #43055528687 had activity age 17m (<20m fallback threshold), and avoided inspection fallback because native inspection #43054529460 was fresh. This recovery receipt is not a native schedule delivery.
- Schedule watchdog [#43058640134](https://github.com/phanthienquoc/platform-infra/actions/runs/43058640134) failed: no native scheduled `reconcile-vps` run existed within 45m; native inter-arrival checks also failed. Its queue sample found no scheduled deployment lane over the 15m runner queue budget. This supports a GitHub schedule-delivery gap, not a demonstrated runner congestion issue.
- TCE WF-01 #43008514423, WF-02 #43008514481 and WF-05 #43008514459 PASS. Native WF-06 #42949191917 and WF-12 #42996293386 remain failed/stale. WF-06 attempt 2 #43003016447 is excluded from native first-attempt cadence; WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED. Manual diagnostic #43003071073 confirmed all four strict HTTP-200 probes returned 503.
- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Media CI #42539512417 PASS. Auth CI #42654579277 PASS.

### Native schedule freshness

Reference: 2026-11-11 17:06:33 UTC. Only first-attempt `event=schedule` runs on `master` count. Age is from the latest run's `created_at`; gap is between the latest and previous qualifying schedule runs.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42993779924 | #42942147668 | 28,208 | 26,585 | 2,700 |
| Platform inspection | #43054529460 | #42981286761 | 3,768 | 30,159 | 4,500 |
| Platform recovery | #43058316157 | #42986496462 | 2,418 | 29,036 | 2,700 |
| Platform watchdog | #43058640134 | #42986833403 | 2,297 | 29,006 | 2,700 |
| TCE WF-06 | #42949191917 | #42922537816 | 51,112 | 12,853 | 1,500 |
| TCE WF-12 | #42996293386 | #42944415193 | 27,135 | 26,503 | 1,500 |

All six inter-arrival gaps fail. Three current-age budgets fail: Platform reconcile and both TCE health lanes. Inspection, recovery and watchdog current ages are within budget. Do not count manual, push, workflow_run, repository_dispatch or rerun attempt 2 as native schedule delivery. Keep all cron expressions and the TCE market-scan schedule unchanged.

### Fresh K3s snapshot — generated 2026-11-11T16:03:55Z

- Snapshot [inspection #43054529460](https://github.com/phanthienquoc/platform-infra/actions/runs/43054529460) is 3,758s old at reference, within its 4,500s budget by 742s. This freshness is time-limited; obtain another read-only inspection before expiry if no new native inspection arrives.
- ARM64 Ubuntu 22.04.5 LTS; kernel 6.8.0-1049-oracle; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3. Snapshot resources: 23Gi RAM / ~19Gi available; 45Gi root disk / 26Gi used / 20Gi free (56%); disk pressure normal. Host reported `restart_required: yes` with kernel, containerd, Docker and OS package updates pending. No reboot or upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running. Registry RepoDigests: Media backend `sha256:93ddb944…`, frontend `sha256:095c72ed…`; MicroFE Shell `sha256:ae64acc0…`, WS `sha256:416bc16a…`; NATS `sha256:b270f5e2…`.
- TCE frontend/service, MicroFE Auth and Keycloak remain 0/0. Public OIDC probes return HTTP 503; do not call maintenance workloads healthy.
- Stock Admin has two ImagePullBackOff pods and desired Backend has one ImagePullBackOff pod. Tags `12d63b4` have no RepoDigest and fail with `no match for platform in manifest`. Legacy Backend/Frontend are 1/1 but only local image IDs are present; they are not registry digest evidence.
- PVC `k3s-debug/k3s-debug-logs` remains Bound (1Gi, RWO, local-path). Platform and Media runner services/listeners are active/enabled; remote GitHub runner unregister is not proven. Docker has 20 images / 9.195GB, 5.773GB reclaimable; no cleanup performed. External backup/retention and authoritative DNS ownership remain unverified.

### Exact next actions and safety

1. Platform operator: run a fresh read-only inspection before the 4,500s snapshot budget expires; then run current-master `reconcile-vps.yml` with `mode=plan` on `e6163fe`. Review plan output before any apply.
2. GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry; enforce PR-only, required checks, force-push/deletion protection and squash-only across all five repositories.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE` in repository Actions variables; do not infer it from WF-13 SKIPPED or weaken strict HTTP-200 probes.
4. TCE/Auth owners: provide immutable release digests, rollback references and explicit recovery approval before reactivation.
5. Stock owner: decide retirement versus restoration; keep scraper fail-closed on missing `VNSTOCK_API_KEY` and do not publish/promote while the decision is unresolved.
6. Media owner: verify remote runner unregister, external backup/retention and authoritative DNS before retirement.
7. Platform operator: obtain maintenance approval before host restart/package upgrades; preserve PVC `k3s-debug/k3s-debug-logs`.

No new GHCR publication/digest promotion, production manifest apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred in this checkpoint. Auth runtime Secret provisioning/verification did occur in the historical reconciliation above; shared `ghcr-pull` was unchanged. Preserve useful workflows; none is confirmed obsolete/removed. No direct SSH/Compose authority. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-12 01:00 ICT / 2026-11-11 18:00:25 UTC

### Direct repository refs, PRs and latest workflow evidence

- Direct master refs: Platform Infra `fc9318db48164a4b37a8003cf0fc201cb5e06e4f`; TCE Dashboard `5b425bdeab457e943bcecf1831836fc698e24394`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform inspection snapshot PR #1646 was squash-merged at `fc9318db48164a4b37a8003cf0fc201cb5e06e4f`; head `91cf3345a518e5911bfe41eea72ecd156ff33eba`, inspection #43067027719 SUCCESS, validation #43067326077 PASS on the PR head. The merged snapshot is `debug/vps-latest.md`, generated 2026-11-11T17:19:36Z.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE/Stock/Media. Keep owner decisions unmerged.
- Latest relevant runs: Platform current-master manual reconciliation #43073396454 SUCCESS; recovery #43073697990 SUCCESS. Latest native scheduled Platform reconciliation #43066718643 SUCCESS on parent SHA `ee5485b`. TCE native WF-06 #43073311537 FAIL (all four endpoint jobs fail); native WF-12 #43068077606 FAIL; WF-12 workflow_run #43073350823 SUCCESS is not native schedule delivery; WF-13 workflow_run #43073377037 SKIPPED. Stock CI #42610360402 PASS and scheduled scraper #42457182511 FAIL CLOSED. Media CI #42539512417 PASS. Auth CI #42654579277 PASS.
- Repository metadata continues to allow squash, merge commits and rebase on all five repositories. Effective inherited organization rulesets/branch-protection enforcement are not established by these metadata reads; GitHub administrator action remains required.

### Current-master GitOps reconciliation — run #43073396454

- Manual `workflow_dispatch` on current Platform master `fc9318db`; inputs: `mode=apply`, `target_app=all`, `allow_image_changes=false`. Overall run and all deployment lane gates completed SUCCESS.
- GHCR read preflight passed for five managed packages: Auth service, MicroFE Shell/WS and TCE service/web.
- Auth runtime Secret was provisioned and verified; values were suppressed. Shared `ghcr-pull` Secret remained unchanged. ServiceAccount/Deployment patches reported no change.
- Blocked-image-pull check found no image-pull failures in MicroFE Auth/Shell/WS or TCE service/frontend; no workload restart was needed for those scopes.
- TCE release pairing passed for `prod-v0.1.0-e75e338`. GitOps diff reported no drift. Manifest apply, image replacement and rollout were skipped. Auth and TCE lanes were explicitly classified as intentional zero-replica maintenance; no live app health was asserted. Auth HTTPS/TLS check passed, MicroFE active-scope health passed, Keycloak lane skipped.
- This run is current-master evidence, but it is a manual dispatch, not a native schedule delivery. The apply-mode run performed Auth Secret provisioning and GHCR credential reconciliation (shared pull Secret unchanged); it did not apply production manifests or roll workloads.

### Fresh K3s snapshot — inspection #43067027719

- Snapshot generated 2026-11-11T17:19:36Z; at 18:00:25Z its age is 2,449s, within the 4,500s budget by 2,051s. This is a workflow_dispatch fallback merged by PR #1646, not native schedule delivery.
- Node `tce-k3s-01` Ready, ARM64; Ubuntu 22.04.5 LTS, kernel 6.8.0-1049-oracle, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3. RAM 23Gi total / ~19Gi available; root disk 45Gi / 26Gi used / 20Gi free (56%), disk pressure normal. Host reports `restart_required: yes` with kernel/containerd/Docker/OS updates pending. No reboot or package upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running. Registry RepoDigests: Media backend `sha256:93ddb944…`, frontend `sha256:095c72ed…`; MicroFE Shell `sha256:ae64acc0…`, WS `sha256:416bc16a…`; NATS `sha256:b270f5e2…`.
- TCE frontend/service, MicroFE Auth and Keycloak remain 0/0. Public OIDC probes return HTTP 503; maintenance workloads are not healthy/live and must not be represented as such.
- Stock Admin has two ImagePullBackOff pods and desired Backend has one ImagePullBackOff pod; tags `12d63b4` report `no match for platform in manifest` and have no RepoDigest. Legacy Stock Backend/Frontend are 1/1 and do have registry RepoDigests for old tag `23b2878` (backend `sha256:bcf5f7b1…`, frontend `sha256:bca44dd3…`); these old digests do not validate or replace the failed desired `12d63b4` images.
- PVC `k3s-debug/k3s-debug-logs` remains Bound (1Gi, RWO, local-path). Media and Platform runner services/listeners are active/enabled; remote runner unregister remains unproven. Docker inventory: 20 images / 9.195GB, 5.773GB reclaimable; no cleanup. External backup/retention and authoritative DNS ownership remain unverified.

### Native schedule evidence at 18:00:25 UTC

Only first-attempt `event=schedule` runs on `master` count. Current age is measured from latest `created_at`; inter-arrival is latest minus previous qualifying native schedule run.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #43066718643 | #42993779924 | 2,573 | 28,867 | 2,700 |
| Platform inspection | #43054529460 | #42981286761 | 7,000 | 30,151 | 4,500 |
| Platform recovery | #43058316157 | #42986496462 | 5,650 | 29,036 | 2,700 |
| Platform watchdog | #43058640134 | #42986833403 | 5,529 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 99 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 2,080 | 28,287 | 1,500 |

All six inter-arrival budgets fail. Four current-age budgets fail: Platform inspection, recovery, watchdog and TCE WF-12. Platform reconciliation is within age budget by 127s; TCE WF-06 is within age budget. Current-master manual reconciliation #43073396454 and manual inspection fallback #43067027719 do not count as native schedule delivery. TCE WF-06 #43073311537 failed all four strict HTTP-200 endpoint jobs (TCE web/API and Auth liveness/readiness); this is consistent with the zero-replica maintenance snapshot, not a reason to weaken health probes. Preserve every cron expression and the TCE market-scan schedule.

### Safety and ownership

- App repositories own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and runtime verification.
- No new app image publication or digest promotion. No production manifest apply, image replacement or workload rollout in #43073396454 because GitOps drift was false. Auth runtime Secret provisioning/verification occurred; shared `ghcr-pull` was unchanged.
- No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow is confirmed obsolete/removed. No duplicate SSH/Compose authority.
- Exact next actions: obtain a fresh read-only K3s inspection before the 4,500s budget expires; continue native scheduler telemetry; GitHub administrator to enforce PR-only/required checks/force-push and deletion protection/squash-only; TCE administrator to verify `TCE_MAINTENANCE_MODE`; TCE/Auth owners to supply release digest/rollback approval; Stock owner to decide retirement/restoration; Media owner to verify remote runner unregister, backup/retention and DNS; Platform operator to obtain maintenance approval before host upgrades/restart.


## Recovery controller follow-up — 2026-11-12 06:05 ICT

- PR #1657 adds bounded retry for transient GitHub HTTP 500/502/503/504 during the recovery controller's reconciliation and inspection workflow-dispatch correlation GETs. The previous run #43116633087 failed because GitHub returned HTTP 502 during reconciliation-run correlation after the dispatch itself had succeeded. The change keeps non-5xx/auth failures fail-closed and adds static contract assertions.
- This is a workflow/validator change only; it does not change cron, dispatch mode, deployment scope, manifest ownership, or production state. Exact-head validation is required before merge.

## Current runtime blockers

- Native schedule delivery: at the 23:02:43Z reference, all six inter-arrival budgets failed and four current-age budgets failed. The later native watchdog #43116818114 (23:03:32Z) also failed on inter-arrival gaps. Its queue diagnostic reported no scheduled deployment lane above the 15-minute queue budget; runner congestion is not established. Recovery #43116883745 is a workflow_run receipt, not native schedule delivery.
- Recovery API transient: #43116633087 failed after HTTP 502 during the reconciliation dispatch-correlation GET. PR #1657 adds bounded retry/backoff for HTTP 500/502/503/504 in both recovery correlation paths; non-5xx/auth and malformed JSON remain fail-closed. On prior head b94f850, validate-manifests #43117701360 passed, but validate-github-actions #43117701372 failed because the tracker lacked the required Current runtime blockers heading. That section is restored on the current branch head; exact-head checks must rerun before merge. Earlier yamllint line-length errors on head 75dbc were also fixed.
- TCE maintenance: WF-13 #43088861304 logged empty TCE_MAINTENANCE_MODE, which mapped to disabled; WF-06 strict HTTP-200 probes returned four 503s. TCE administrator must verify/set the variable according to the approved zero-replica maintenance state. Do not weaken WF-06/WF-12 or alter market-scan cron.
- Stock: desired Admin/Backend tag 12d63b4 lacks a compatible platform manifest/RepoDigest; the scraper remains fail-closed on missing VNSTOCK_API_KEY. No image promotion is allowed.
- Media decommission: Media runner service/Listener is active. Stop/disable/unregister, external backup/retention, authoritative DNS and protected production approval are still required before namespace deletion. Preserve k3s-debug/k3s-debug-logs.
- Host maintenance: K3s host reports restart required with pending OS/kernel/containerd/Docker updates. No reboot or cleanup without platform approval.
- Governance: branch-protection detail GET returned 403 for all five repositories; effective inherited organization rulesets remain unverified. GitHub administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.


## Latest verification — 2026-11-12 07:02 ICT / 2026-11-12 00:02:34 UTC

### Repository refs, open PRs and latest workflow runs

Direct `master` refs at this checkpoint:

- Platform Infra: `d0b79f0fb22aa4b6c1eae537785a5adf5f4cbb1e`.
- TCE Dashboard: `5b425bdeab457e943bcecf1831836fc698e24394`.
- StockDividend: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`.
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`.
- Authentication: `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.

Open PRs: Platform #1314/#544/#541/#539 (owner-decision drafts); Authentication #76 (owner-decision draft); none in TCE, Stock or Media. No owner-decision PR was merged.

Latest directly inspected workflow evidence:

- Platform native scheduled reconciliation #43120544165: SUCCESS on current master `d0b79f0`, event=schedule, created 23:32:03Z. Native inspection #43116036275: SUCCESS on prior manifest-equivalent master `51729f13`, created 22:57:41Z; snapshot generated 22:57:49Z. Native recovery #43116568507: SUCCESS; native watchdog #43116818114: FAILURE on native inter-arrival gaps. Recovery receipt #43121541699: SUCCESS via repository_dispatch from TCE WF-12; it is not native schedule delivery.
- TCE native WF-12 #43121528127: FAILURE at 23:39:46Z. WF-13 #43121552311: SUCCESS as workflow_run recovery, not a native schedule. Its log shows `TCE_MAINTENANCE_MODE` was empty in that run, mapped to `enabled=false`, and the read-only WF-06 fallback was dispatched. Fallback #43121575816: FAILURE; all four strict public endpoint probes returned HTTP 503. Latest native WF-06 schedule remains #43073311537 (FAILURE, 17:58:46Z); WF-12 reports its age as 341 minutes. The variable value after that run is not available from this read-only integration; do not claim it remains unchanged.
- Stock CI #42610360402: SUCCESS; scraper #42457182511: FAILURE/FAIL-CLOSED due to missing `VNSTOCK_API_KEY`. Media CI #42539512417: SUCCESS. Authentication CI #42654579277: SUCCESS. These are latest visible runs from the current Actions run listings; no new immutable image publication is evidenced on app master refs.

### Current-master GitOps reconciliation — #43120544165

- Native scheduled run on current Platform master `d0b79f0`; inputs recorded in job log: `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- GHCR read preflight passed for five packages: Auth service, MicroFE Shell/WS and TCE service/web.
- Auth runtime Secret was provisioned and verified; secret values were suppressed. Shared `ghcr-pull` was reconciled and reported unchanged. ServiceAccount/Deployment patches reported no change.
- Blocked-image-pull checks found no failures for MicroFE Auth/Shell/WS and TCE service/frontend. TCE release pairing passed for `prod-v0.1.0-e75e338`.
- GitOps drift was false. Production manifest apply, image replacement and rollout were skipped. This is a successful reconciliation/preflight, not evidence of a new production rollout or app image promotion.
- The later recovery run #43121541699 used the merged retry-capable recovery controller on master and completed successfully. It considered the native inspection #43116036275 fresh (42 minutes old at 23:40Z) and did not dispatch a duplicate inspection. This proves the recovery path completed, not that a transient HTTP 5xx retry branch was exercised.

### K3s snapshot — #43116036275 / debug/vps-latest.md

- Snapshot generated `2026-11-11T22:57:49Z`; age at reference is 3,885s, within the 4,500s budget by 615s. Obtain a fresh read-only inspection before expiry.
- Node `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5 LTS; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3. RAM ~19GiB available; root disk 45GiB total / 26GiB used / 20GiB free (56%). Host reports `restart_required: yes` with kernel, containerd, Docker and OS updates pending. No reboot or package upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running with registry RepoDigests. TCE frontend/service, MicroFE Auth and Keycloak were 0/0; do not represent these maintenance workloads as live/healthy.
- Stock Admin had two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod. Desired tag `12d63b4` failed with `no match for platform in manifest` and had no RepoDigest. Legacy Backend/Frontend were 1/1 with old `23b2878` registry digests; these do not validate or replace the desired image.
- Stock/Media storage preflight found no PVC/PV claims or VolumeSnapshot references in the target namespaces. Preserve separate PVC `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO).
- Media runner service was active/enabled and `Runner.Listener` was present. GitHub-side runner unregister remains unverified. Docker inventory was 20 images / 9.195GB, 5.773GB reclaimable; no cleanup. External backup/retention and authoritative DNS evidence remain unverified.

### Native schedule evidence at 00:02:34Z

Only first-attempt `event=schedule` runs on `master` count. Current age uses latest native run `created_at`; gap uses latest minus previous qualifying native run. Budgets are current-age / inter-arrival.

| Lane | Latest native run | Current age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43120544165 | 1,831 | 22,471 | 2,700 / 2,700 | age PASS, gap FAIL |
| Platform inspection | #43116036275 | 3,893 | 24,826 | 4,500 / 4,500 | age PASS, gap FAIL |
| Platform recovery | #43116568507 | 3,654 | 23,725 | 2,700 / 2,700 | age FAIL, gap FAIL |
| Platform watchdog | #43116818114 | 3,542 | 23,716 | 2,700 / 2,700 | age FAIL, gap FAIL |
| TCE WF-06 | #43073311537 | 21,828 | 54,245 | 1,500 / 1,500 | age FAIL, gap FAIL |
| TCE WF-12 | #43121528127 | 1,368 | 22,441 | 1,500 / 1,500 | age PASS, gap FAIL |

All six inter-arrival budgets fail; three current-age budgets fail (Platform recovery, Platform watchdog and TCE WF-06). The latest WF-12 native run itself is within its 25-minute age threshold but fails because the latest native WF-06 schedule is stale. The WF-13 workflow_run and Platform repository_dispatch receipts do not substitute for native schedule delivery. The Platform watchdog queue diagnostic did not establish runner congestion; the observed failure is native schedule cadence. Preserve all cron expressions and the TCE market-scan schedule.

### Governance and exact next actions

- Direct GitHub branch API returned `protected=false` for all five `master` branches. Repository metadata still permits merge commits and rebase in addition to squash. Effective inherited organization rulesets are not established by these reads. GitHub administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.
- TCE administrator: verify the Actions variable `TCE_MAINTENANCE_MODE`; the 23:40Z WF-13 log showed it empty. If zero-replica maintenance is still approved, explicitly set true; otherwise restore replicas and keep it false. Do not weaken strict HTTP-200 checks or schedule monitoring.
- Platform operator: obtain a fresh read-only inspection before the 4,500s snapshot budget expires, then run current-master `reconcile-vps.yml` in `mode=plan` on `d0b79f0` and review the plan before any apply.
- Stock owner: resolve ARM64-compatible immutable publication or confirm retirement; do not promote tag `12d63b4` without registry digest/provenance.
- Media owner: stop/disable/unregister the runner and prove both local Listener absence and GitHub-side unregister; provide external backup/retention and authoritative DNS evidence before protected namespace deletion.
- Platform operator: obtain maintenance approval before host package upgrades/restart. Preserve `k3s-debug/k3s-debug-logs`.

No new GHCR publication/digest promotion, production manifest change, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. Auth runtime Secret provisioning/verification and GHCR credential reconciliation did occur in #43120544165; shared `ghcr-pull` remained unchanged. No workflow is confirmed obsolete or removed. No duplicate direct SSH/Compose deployment authority. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-12 08:07 ICT / 2026-11-12 01:07:20 UTC

### Repository refs, open PRs and directly listed Actions runs

GitHub branch and Actions run collections were read directly for all five repositories. The Actions listing used the first 100 runs per repository and was filtered to `master`, first-attempt native `event=schedule` runs, and current PR-head runs. Do not infer that a run not present in this first page does not exist.

| Repository | `master` SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `deadaa4f7b30a47a997550b491928027d5a15737` | #1314/#544/#541/#539 (owner-decision drafts) | PR #1660 merged; inspection #43127872524 SUCCESS (workflow_dispatch), exact-head manifest validation #43128079244 PASS. Manual reconciliation #43127613751 SUCCESS; native reconcile #43120544165 is still the latest listed native schedule. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | #1038 (maintenance-mode unset warning; checks queued) | Native WF-06 #43127554403 FAILURE; native WF-12 #43121528127 FAILURE; WF-13 #43127582309 SUCCESS but `TCE_MAINTENANCE_MODE` was empty; fallback #43127603475 FAILURE with four HTTP 503 probes; WF-07 backup #43130553977 SUCCESS. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Desired Admin/Backend tag `12d63b4` remains without an ARM64-compatible manifest/RepoDigest. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS. Latest inspection shows backend/frontend 1/1 with immutable registry RepoDigests; dedicated runner service and `Runner.Listener` remain active. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | CI #42654579277 SUCCESS. Auth and Keycloak remain 0/0 maintenance; no live Auth/Keycloak health is claimed. |

Platform PR #1660 was merged from exact head `0bd88bcae019ed6d97c0305bdba5d75bce68e0b6` to `deadaa4f7b30a47a997550b491928027d5a15737`. Its inspection job #43127872524 completed SUCCESS; exact-head manifest validation #43128079244 completed SUCCESS. No separate post-merge validation run on merge SHA `deadaa4f` was observed in the current Actions listing.

TCE PR #1038 is open on exact head `e718d728d531ac1c492e34a337e3fe308980a767`. WF-01P #43132521680, WF-02 PR #43132521802, WF-05 PR #43132521704 and WF-08B PR #43132521695 are in progress on the current exact head. Previous WF-01P #43132263903 failed on the prior head due to an incorrect grep literal; corrected on current head. Push WF-02 #43132514345 and WF-05 #43132514285 are also in progress. Earlier intermediate-head runs were cancelled after the second commit. Do not merge until current exact-head applicable checks complete successfully.

### Platform reconciliation and recovery evidence

- Manual `Reconcile VPS — all / apply` #43127613751 ran on parent SHA `331120b33ed7b090620dec373b20aab463d78cc8` at 00:29:09Z and completed SUCCESS at 00:31:00Z. Inputs: `mode=apply`, `target_app=all`, `allow_image_changes=false`.
- GHCR read preflight passed five packages: Auth service, MicroFE Shell/WS and TCE service/web. Auth runtime Secret was provisioned and verified with values suppressed. `secret/ghcr-pull unchanged` was emitted for both namespace reconciliation outputs.
- Blocked-image-pull checks found no failures for MicroFE Auth/Shell/WS or TCE service/frontend. TCE release pairing passed. GitOps drift was `false`; manifest apply, image replacement and rollout were skipped. Keycloak deployment lane was skipped. This is successful reconciliation/preflight, not a new rollout.
- Recovery workflow_dispatch #43127821037 completed SUCCESS after #43127613751. It reported the native inspection stale and dispatched read-only inspection fallback #43127872524. Neither workflow_dispatch receipt counts as native schedule delivery.
- Current `master` is now `deadaa4f`; PR #1660 changed only `debug/vps-latest.md`, so the production manifest tree is unchanged from the reconciliation parent SHA. No exact-current-master `mode=plan` has been run.

### Fresh K3s inspection — #43127872524

- Snapshot generated `2026-11-12T00:31:21Z`; at reference 01:07:20Z age is 2,159s / 4,500s budget, with 2,341s remaining. Expected expiry: `2026-11-12T01:46:21Z` unless a newer inspection supersedes it. This is a workflow_dispatch fallback, not native schedule evidence.
- Node `tce-k3s-01`: Ready, ARM64; Ubuntu 22.04.5 LTS; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3. Root disk 45GiB total / 26GiB used / 20GiB free (56%); ~19GiB RAM available. Host reports `restart_required: yes` with pending OS/kernel/containerd/Docker updates. No reboot or package upgrade.
- Media backend/frontend and MicroFE Shell/WS/NATS were 1/1 Running with registry RepoDigests. Media backend digest `sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d`; frontend `sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a`; MicroFE Shell `sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd`; WS `sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d`; NATS `sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6`.
- TCE frontend/service, MicroFE Auth and Keycloak were 0/0; do not represent these maintenance workloads as live/healthy. Stock Admin had two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod. Desired tag `12d63b4` failed with `no match for platform in manifest` and has no RepoDigest.
- Correction to prior Stock evidence: in this latest snapshot the CRI image inventory has an empty RepoDigest field for both cached legacy Stock tags `backend:23b2878` and `user:23b2878`; only local image IDs are shown. They are not registry provenance or promotion evidence.
- Stock/Media target namespace storage preflight found no PVC/PV claims or VolumeSnapshot references. Preserve separate PVC `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO).
- Media runner service was active/enabled and `Runner.Listener` was present. GitHub-side runner unregister remains unverified. Docker inventory was 20 images / 9.195GB, 5.773GB reclaimable; no cleanup. External backup/retention and authoritative DNS evidence remain unverified.

### TCE maintenance and health

- WF-13 #43127582309 log at 00:28:57Z showed `TCE_MAINTENANCE_MODE` empty. The current workflow maps empty to `enabled=false`, so the read-only WF-06 fallback was dispatched. This does not assert maintenance is healthy.
- Fallback WF-06 #43127603475 failed all four strict probes: TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 (expected 200). Native WF-06 #43127554403 also failed all four probes. Keep strict HTTP 200 behavior.
- New TCE PR #1038 separates the empty case from explicit false and adds a warning while preserving the current behavior: empty remains non-maintenance and still runs the read-only fallback; only an approved explicit true suppresses it. No repository variable was changed by this automation.
- TCE WF-07 backup #43130553977 succeeded at 00:53:07Z and created a TCE archive under `/home/ubuntu/tce/backups` with 7-day retention. This is TCE backup evidence only; it does not satisfy Stock/Media external backup or retention gates.

### Native schedule freshness at reference 01:07:20Z

Only first-attempt `event=schedule` runs on `master` count. Age uses the latest qualifying run's `created_at`; inter-arrival uses the latest and previous qualifying native run. Budgets remain unchanged.

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43120544165 | 5,717 | 22,471 | 2,700 / 2,700 | age FAIL, gap FAIL |
| Platform inspection | #43116036275 | 7,779 | 24,826 | 4,500 / 4,500 | age FAIL, gap FAIL |
| Platform recovery | #43116568507 | 7,540 | 23,725 | 2,700 / 2,700 | age FAIL, gap FAIL |
| Platform watchdog | #43116818114 | 7,428 | 23,716 | 2,700 / 2,700 | age FAIL, gap FAIL |
| TCE WF-06 | #43127554403 | 2,321 | 23,393 | 1,500 / 1,500 | age FAIL, gap FAIL |
| TCE WF-12 | #43121528127 | 5,254 | 22,441 | 1,500 / 1,500 | age FAIL, gap FAIL |

All six current-age and all six inter-arrival budgets fail. TCE WF-07 backup #43130553977 succeeded as a separate scheduled workflow and is not a substitute for WF-06/WF-12. Manual workflow_dispatch, workflow_run, repository_dispatch and rerun attempts do not satisfy native schedule acceptance. Available watchdog diagnostics did not establish runner congestion. Preserve all cron expressions and the TCE market-scan schedule.

### Governance and safety

- Direct GET of `branches/master` returned `protected=false` for all five repositories. Repository metadata allows squash, merge commit and rebase. This does not establish whether inherited organization rulesets exist; effective policy remains unverified. Administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.
- No new GHCR publication/digest promotion, production manifest change, image replacement or workload rollout. Auth runtime Secret provisioning/verification and GHCR credential reconciliation did occur in #43127613751; shared `ghcr-pull` remained unchanged.
- No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow is confirmed obsolete or removed. No duplicate direct SSH/Compose authority. Platform Infra remains the sole production apply authority.
- TCE market-scan schedule unchanged.

### Exact next actions

1. Platform operator: obtain a fresh read-only inspection before `2026-11-12T01:46:21Z`; do not use a fallback as native schedule acceptance.
2. Platform operator: run current-master `reconcile-vps.yml` in `mode=plan` on `deadaa4f` and review the plan before any apply. The last reconciliation is within its 45-minute budget but expires at approximately `01:16:00Z`.
3. TCE administrator: set `TCE_MAINTENANCE_MODE=true` only if zero-replica maintenance remains explicitly approved; otherwise set false and restore replicas. Keep strict HTTP 200 probes.
4. TCE PR #1038: wait for WF-01P/WF-02/WF-05 exact-head checks; do not merge while queued/in progress.
5. GitHub administrator: resolve native schedule delivery and branch governance using authoritative GitHub delivery/organization ruleset access.
6. Media owner: stop/disable/unregister the runner and prove local Listener absence plus GitHub-side unregister; provide external backup/retention and authoritative DNS evidence before protected namespace deletion.
7. Stock owner: resolve retirement or supply a platform-compatible immutable release with registry digest/provenance; do not promote `12d63b4` or cached legacy image IDs.
8. Platform operator: obtain separate maintenance approval before host package upgrades/restart.

## Follow-up — 2026-11-12 08:09 ICT / 2026-11-12 01:09:34 UTC

- Platform PR #1661 exact head `9ed3b122aa0c45b91a8380ab7a503d40dd363435` passed validate-manifests #43132479380; current PR metadata still reports open and mergeable. No production files changed.
- TCE PR #1038 advanced from `8a81933f6afee302ef84f844c4a5d204600182f9` to exact head `e718d728d531ac1c492e34a337e3fe308980a767`. The previous WF-01P #43132263903 failed on the prior head because the static validator searched for the wrong literal spacing around the empty case; the assertion was corrected to match the exact `"")` case. Do not treat that prior failure as validation of the new head.
- New exact-head PR runs are in progress: WF-01P #43132521680, WF-02 #43132521802, WF-05 #43132521704 and WF-08B #43132521695. Push runs WF-02 #43132514345 and WF-05 #43132514285 are also in progress. No check on the new head has completed at this follow-up.
- WF-08B PR run #43132263833 on the prior head executed only WebSocket/Auth tests and payload validation; image publication and production dispatch jobs were skipped. The new-head WF-08B run remains in progress.
- No variable, secret, cron, market-scan schedule, production release or deployment was changed.

## Latest verification — 2026-11-12 08:11 ICT / 2026-11-12 01:11:13 UTC

### Master refs and open PRs

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | `166363e7c47450d62e002ef6c2950ed824421caa` | #1314/#544/#541/#539 (owner-decision drafts) |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none; PR #1038 merged |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner-decision draft |

Platform PR #1661 was squash-merged from exact head `ea3728fa225f927c26f1448f6eefda492fcfa05f` to master `166363e7`. Exact-head validate-manifests #43132612104 PASS. Post-merge validate-manifests #43132719192 is still in progress; do not claim post-merge PASS yet.

TCE PR #1038 was squash-merged from exact head `e718d728d531ac1c492e34a337e3fe308980a767` to master `34f6024f`. Exact-head checks all PASS: WF-01P #43132521680, WF-02 #43132521802, WF-05 #43132521704, WF-08B #43132521695. On the PR event, WF-08B test jobs passed while GHCR publication and production dispatch jobs were skipped. Post-merge master runs WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 are still in progress. No production release or image publication was triggered.

### Platform GitOps and runtime

- Manual reconciliation #43127613751 completed SUCCESS at 00:31:00Z on parent SHA `331120b`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR read preflight passed five packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` remained unchanged; TCE release pairing passed; no blocked pulls were found in MicroFE Auth/Shell/WS or TCE service/frontend. GitOps drift=false; manifest apply, image replacement and rollout were skipped. This is reconciliation/preflight evidence, not a new rollout.
- At 01:11:13Z, reconciliation completion age was 2,413s against a 2,700s budget (287s remaining; expected expiry 01:16:00Z). It ran on parent `331120b`; subsequent Platform PRs #1660/#1661 changed only inspection/documentation files, not production manifests. No exact-current-master `mode=plan` is evidenced.
- Recovery #43127821037 SUCCESS and read-only inspection fallback #43127872524 SUCCESS. Inspection snapshot generated 00:31:21Z; age 2,392s against a 4,500s budget (2,108s remaining; expected expiry 01:46:21Z). This is workflow_dispatch fallback, not native schedule acceptance.
- Latest snapshot: K3s node Ready/ARM64, disk 56% (~20GiB free), ~19GiB RAM available, host `restart_required: yes`. Media backend/frontend and MicroFE Shell/WS/NATS 1/1 with RepoDigests. TCE/Auth/Keycloak 0/0 maintenance. Stock Admin two pods and desired Backend one pod ImagePullBackOff on `12d63b4`, no compatible manifest/RepoDigest. Cached legacy Stock `23b2878` tags have blank RepoDigest fields; local image IDs are not registry provenance.
- Media runner service active/enabled and `Runner.Listener` present. Stock/Media namespace storage preflight had no PVC/PV claims or VolumeSnapshot references; preserve `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO). External backup/retention, authoritative DNS and GitHub-side runner unregister remain unverified. No decommission.

### TCE maintenance and health

- TCE PR #1038 adds a warning when `TCE_MAINTENANCE_MODE` is empty while retaining existing safe behavior: empty remains non-maintenance and the read-only WF-06 fallback continues; only explicit true suppresses that fallback. It does not make health green.
- Last observed WF-13 #43127582309 logged an empty variable and dispatched fallback. WF-06 fallback #43127603475 returned HTTP 503 for TCE web, TCE API, Auth liveness and Auth readiness. The new warning code has merged, but the variable was not changed and no post-merge WF-13/health run is yet evidenced.
- TCE WF-07 backup #43130553977 succeeded under `/home/ubuntu/tce/backups` with 7-day retention. This is TCE-only backup evidence, not Stock/Media backup evidence.

### Native schedule freshness at 01:11:13Z

Only first-attempt `event=schedule` runs on master count; manual/workflow_run/repository_dispatch/fallback events do not satisfy native delivery.

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #43120544165 | 5,950 | 22,471 | 2,700 |
| Platform inspection | #43116036275 | 8,012 | 24,826 | 4,500 |
| Platform recovery | #43116568507 | 7,773 | 23,725 | 2,700 |
| Platform watchdog | #43116818114 | 7,661 | 23,716 | 2,700 |
| TCE WF-06 | #43127554403 | 2,554 | 23,393 | 1,500 |
| TCE WF-12 | #43121528127 | 5,487 | 22,441 | 1,500 |

All six current-age and all six inter-arrival budgets fail. TCE WF-07 backup #43130553977 succeeded but is not WF-06/WF-12 schedule evidence. No cron expression or TCE market-scan schedule changed.

### Governance and safety

- Direct master branch API continues to return `protected=false` for all five repositories. Effective inherited organization rulesets remain unverified. Administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.
- No new GHCR publication/digest promotion, production manifest change, image replacement or workload rollout. Auth Secret provisioning and GHCR credential reconciliation occurred in #43127613751; shared `ghcr-pull` was unchanged.
- No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow was removed. Platform Infra remains the sole production apply authority.
- TCE market-scan schedule unchanged.

### Exact next actions

1. Platform operator: run a fresh current-master `reconcile-vps.yml` in `mode=plan` before the last reconciliation expires at approximately 01:16:00Z; review output before any apply.
2. Platform operator: obtain fresh read-only K3s inspection before approximately 01:46:21Z; do not count workflow_dispatch fallback as native schedule success.
3. TCE administrator: set `TCE_MAINTENANCE_MODE=true` only if zero-replica maintenance remains approved; otherwise set false and restore replicas. No Actions-variable write capability was available in this run.
4. GitHub administrator: resolve native schedule delivery and enforce branch protection/squash-only.
5. Media owner: stop/disable/unregister runner and prove local Listener absence plus GitHub-side unregister; supply external backup/retention and DNS evidence before deletion.
6. Stock owner: do not promote `12d63b4` or cached legacy IDs; provide a platform-compatible immutable release with registry digest if retirement is reversed.
7. Platform operator: obtain separate approval before host upgrades/restart.

## Latest cross-repo verification — 2026-11-12 10:02 ICT / 03:02:38 UTC

### Repository refs, open PRs and latest master workflow evidence

| Repository | Current master | Open PRs | Latest master workflow evidence |
|---|---|---|---|
| Platform Infra | `a2f7a49c8d1f26db0ace9828c2b2de72c90a3467` | #1314, #544, #541, #539 (owner-decision drafts) | `validate-manifests` #43139122792 SUCCESS on exact master SHA at 02:06:54Z. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 SUCCESS on master at 01:11:02Z. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | StockDividend CI #42610360402 SUCCESS on master; scheduled scraper #42457182511 FAILED CLOSED at credential preflight. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Media CI #42539512417 SUCCESS on master. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | auth-service-ci #42654579277 SUCCESS on master. |

PR #1663 and #1664 are merged. PR #1664 post-merge validation #43139122792 passed on current Platform master. TCE PR #1038 is merged; its exact-head WF-01P/WF-02/WF-05/WF-08B checks passed, and post-merge master WF-01/WF-02/WF-05 runs passed. No new app release or GHCR publication was observed in this verification window.

The current-master combined-status endpoint returned no legacy status contexts for all five commits; the workflow-run evidence above is the available CI record. Latest run collections were queried directly from each repository's Actions API (first page, up to 100 runs).

### Native schedule delivery — reference 03:02:38Z

Only first-attempt `event=schedule` runs on `master` count. Manual dispatches, `workflow_run`, `repository_dispatch`, fallback runs and reruns do not satisfy native schedule delivery.

| Lane | Latest native run | Created (UTC) | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---|---:|---:|---:|---|
| Platform reconcile | #43120544165 | 2026-11-11 23:32:03 | 12,635 | 22,471 | 2,700 | age FAIL / gap FAIL |
| Platform inspection | #43116036275 | 2026-11-11 22:57:41 | 14,697 | 24,826 | 4,500 | age FAIL / gap FAIL |
| Platform recovery | #43116568507 | 2026-11-11 23:01:40 | 14,458 | 23,725 | 2,700 | age FAIL / gap FAIL |
| Platform watchdog | #43116818114 | 2026-11-11 23:03:32 | 14,346 | 23,716 | 2,700 | age FAIL / gap FAIL |
| TCE WF-06 | #43127554403 | 2026-11-12 00:28:39 | 9,239 | 23,393 | 1,500 | age FAIL / gap FAIL |
| TCE WF-12 | #43121528127 | 2026-11-11 23:39:46 | 12,172 | 22,441 | 1,500 | age FAIL / gap FAIL |

All six age budgets and all six inter-arrival budgets fail. TCE WF-07 backup #43130553977 succeeded at 00:53:07Z but is a separate backup workflow, not WF-06/WF-12 schedule evidence. Platform watchdog #43116818114 verified the reconcile workflow was active and its queue sample did not establish a lane waiting over the 15-minute queue budget. TCE WF-12 #43121528127 verified WF-06 was enabled, found the latest native WF-06 run #43073311537 to be 341 minutes old, and measured queue wait as 0 minutes for that source run. The evidence supports a schedule-delivery gap, not a proven runner-congestion cause.

Current cron definitions were read from master and left unchanged: Platform reconcile `7,22,37,52 * * * *`, inspection `2,32 * * * *`, recovery `10,25,40,55 * * * *`, watchdog `12,27,42,57 * * * *`; TCE WF-06 `*/15 * * * *`, WF-12 `7,22,37,52 * * * *`. **TCE market-scan schedule unchanged.**

### GitOps and K3s runtime evidence

- Latest successful native Platform reconciliation #43120544165 ran on parent SHA `d0b79f0f`, mode=apply / target=all / allow_image_changes=false. It passed five GHCR package-read checks, verified Auth runtime Secret provisioning with values suppressed, left shared `ghcr-pull` unchanged, passed TCE release pairing `prod-v0.1.0-e75e338`, found drift=false, and skipped manifest apply, image replacement and workload rollout.
- Later manual reconciliation #43127613751 succeeded on parent SHA `331120b` with the same five-package GHCR preflight, Auth Secret verification, unchanged shared pull credential, TCE pairing PASS, drift=false and no apply/rollout. At 03:02:38Z it is 9,098s old, beyond the 2,700s reconciliation freshness budget. Neither run is exact-current-master `mode=plan` evidence for `a2f7a49c`.
- Latest full K3s snapshot remains `debug/vps-latest.md`, blob `bde5bc7fc23aafc2659fa8cd919ce96cb4545c35`, generated 00:31:21Z by inspection #43127872524. At 03:02:38Z it is 9,077s old, beyond the 4,500s budget. No fresh inspection/plan was available in this run.
- Historical snapshot: K3s node Ready/ARM64; disk 56% (~20GiB free); ~19GiB RAM available; host restart required. Media backend/frontend and MicroFE Shell/WS/NATS were 1/1. TCE/Auth/Keycloak were 0/0 maintenance. Stock Admin (two pods) and desired Backend (one pod) were ImagePullBackOff on tag `12d63b4`; no compatible manifest/RepoDigest was present. Stock legacy Backend/Frontend were 1/1 but had no registry RepoDigest in the snapshot; local image IDs are not promotion evidence.
- Media runner service was active/enabled and `Runner.Listener` was present. The Platform runner was also active. Docker showed 20 images / 9.195GB with 5.773GB reclaimable; no cleanup was performed. Host kernel/containerd/Docker/OS updates were pending and restart was required; no reboot was performed.
- PVC `k3s-debug/k3s-debug-logs` remains Bound, 1Gi, RWO and must be preserved. Stock/Media namespace storage inventory showed no PVC/PV claims or VolumeSnapshot references, but external backup/retention, authoritative DNS and GitHub-side Media runner unregister evidence remain outstanding. No namespace deletion/decommission occurred.

### App-owned publication and deployment authority audit

- TCE WF-03 is a manual production release publisher: it refuses existing immutable tags, verifies ARM64 registry digests, validates an exact release-request payload, and dispatches Platform Infra. It does not perform direct VPS/Compose apply.
- Stock `deploy.yml` is a manual GHCR publisher with immutable-tag and ARM64 digest checks; it does not own Platform production apply. The scheduled scraper #42457182511 stopped at `Require VNStock API key before installing dependencies` because `VNSTOCK_API_KEY` was missing; Python setup, dependency install and scraping were skipped. Fail-closed behavior is preserved.
- Media WF-03 publishes immutable ARM64 images and explicitly records that no Platform dispatch is configured; it does not apply production workloads.
- Auth `release.yml` is a manual master publisher with provenance/SBOM, immutable digest verification and exact Platform dispatch payload.
- TCE WF-07 uses SSH only for its purposeful TCE backup archive; it is not a competing deployment authority. No duplicate direct SSH/Compose production apply authority was found in the inspected publisher workflows.
- Ownership remains: app repos own tests/builds and immutable GHCR publication; Platform Infra alone owns production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and runtime verification. Preserve CI/test/security/manual/release/backup/integration/scheduled workflows. No workflow is confirmed redundant/obsolete.

### TCE maintenance and health

- TCE WF-06 #43127554403 failed all four public endpoint checks with HTTP 503: TCE web, TCE API, Auth liveness and Auth readiness. The probes correctly require HTTP 200 and were not weakened.
- TCE WF-12 #43121528127 failed its schedule-delivery check because native WF-06 was 341 minutes old; its heartbeat dispatch to Platform succeeded.
- WF-13 #43127582309 last logged an empty `TCE_MAINTENANCE_MODE` and treated it as non-maintenance. TCE PR #1038 has since merged a warning for the unset variable while preserving read-only fallback and strict health checks. The Actions variable itself was not changed or readable through this integration; its current value is unverified.
- TCE WF-07 backup #43130553977 succeeded with 7-day retention under `/home/ubuntu/tce/backups`. This is TCE-only backup evidence and does not satisfy Stock/Media external backup requirements.

### Governance and safety

- Repository metadata permits squash, merge commit and rebase on all five repositories. Repository rulesets GET returned an empty list for Platform, TCE, Media and Authentication; Stock rulesets GET returned 403. Branch-protection detail GET returned 403 for all five repositories. Effective inherited organization rulesets and current required-check enforcement therefore remain unverified; administrator access is required to enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.
- No new GHCR publication/digest promotion, current-master GitOps plan/apply, production manifest mutation, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred.
- No workflow was removed. No duplicate direct SSH/Compose production authority was introduced. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

### Exact next actions

1. Platform operator: obtain fresh read-only `inspect-vps.yml` and run current-master `reconcile-vps.yml` with `mode=plan` on `a2f7a49c`; review plan before any apply. The available GitHub connector in this run is read-only for workflow dispatch, so these runs were not triggered.
2. GitHub administrator: investigate native scheduled-event delivery using organization/repository Actions delivery telemetry; available evidence shows workflows active and no measured queue congestion, but does not identify why native events stopped.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE`; set true only for explicitly approved zero-replica maintenance, otherwise restore replicas and keep false. Preserve HTTP-200 probes.
4. GitHub administrator: verify inherited rulesets and enforce PR-only / required checks / squash-only.
5. Media owner: stop/disable/unregister the runner and prove local Listener absence plus GitHub-side unregister; provide external backup/retention and authoritative DNS evidence before protected namespace deletion.
6. Stock owner: do not promote `12d63b4` or cached legacy image IDs; provide a platform-compatible immutable registry digest/provenance if retirement is reversed. Provide `VNSTOCK_API_KEY` through protected Actions secret storage only if scraper operation is authorized.
7. Platform operator: obtain separate maintenance approval before host package upgrades or restart.


## Post-merge synchronization — 2026-11-12 10:10 ICT / 03:10:32 UTC

- Platform PR #1665 (docs-only readiness refresh) was squash-merged from exact head `26eaa72393f9578a8ca3742f669b74f9cf1060f3` to master `7db202b643e08b6c9fd8b643758731fabba17bca`.
- Exact-head `validate-manifests` run #43146309032 completed SUCCESS with all 20 applicable validation steps passing.
- Post-merge `validate-manifests` run #43146400383 completed SUCCESS on exact merge SHA `7db202b643e08b6c9fd8b643758731fabba17bca` (21/21 job steps completed; validation PASS).
- Direct `refs/heads/master` verification matched the merge SHA. PR #1665 is merged.
- Open Platform owner-decision drafts remain #1314/#544/#541/#539. No application or production workflow PR was added.
- PR #1665 changed only the deployment tracker, workflow inventory and two documentation checkpoints. Production manifests, workflows, secrets, Actions variables, image references and schedules are unchanged. No production apply, image promotion or workload rollout occurred.
- Current Platform master is now `7db202b643e08b6c9fd8b643758731fabba17bca`. The runtime and scheduler blockers recorded in the 10:02 checkpoint are unchanged; no fresh K3s inspection or current-master GitOps plan was available after the merge.
- TCE market-scan schedule unchanged.


## Latest cross-repo verification — 2026-11-12 11:56 ICT / 04:56:38 UTC

### Repository state and open pull requests

| Repository | Current master | Open PRs | Latest relevant CI / runtime evidence |
|---|---|---|---|
| Platform Infra | `9f969fcfe0a8b31c5b612e218ea9f5a86e629059` | #1314, #544, #541, #539 (owner-decision drafts) | Native reconcile #43152960974 SUCCESS on current master; watchdog #43153156539 FAILED native inter-arrival acceptance; recovery #43154428142 SUCCESS via repository_dispatch; latest native inspection #43150245172 SUCCESS. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Native WF-12 #43154415980 FAILED because latest native WF-06 #43127554403 was 234m old; read-only fallback #43154458775 FAILED all four strict public HTTP-200 probes with HTTP 503. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Desired K3s tag `12d63b4` has no compatible platform manifest. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS; last K3s snapshot has backend/frontend 1/1 with registry RepoDigests; dedicated runner service and Listener remain active. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner-decision draft) | CI #42654579277 PASS; Platform reconciliation verified Auth runtime Secret with values suppressed; Auth/Keycloak remain intentional zero-replica maintenance, so no live workload health is asserted. |

Open Platform PRs #1314/#544/#541/#539 and Authentication PR #76 remain owner decisions. No Keycloak, database, identity architecture or migration PR was merged or modified.

### Latest exact workflow evidence

- Platform native scheduled reconciliation [#43152960974](https://github.com/phanthienquoc/platform-infra/actions/runs/43152960974) ran at 2026-11-12T04:09:48Z on exact current master `9f969fc`, with `mode=apply`, `target_app=all`, `allow_image_changes=false`. Five GHCR package-read preflights passed; Auth runtime Secret was verified with values suppressed; shared `ghcr-pull` was unchanged; TCE release pairing passed; GitOps drift was false; manifest apply, image replacement and rollout were skipped. The image-pull restart checks found no failures in the MicroFE/TCE scopes. Auth and TCE lanes explicitly reported intentional zero-replica maintenance; MicroFE active-scope health passed; Keycloak was skipped.
- Platform recovery [#43154428142](https://github.com/phanthienquoc/platform-infra/actions/runs/43154428142) succeeded as `repository_dispatch` after the TCE heartbeat. Its log found native inspection #43150245172 only 38m old at that reference, within the 75m inspection budget, so it correctly avoided a duplicate inspection fallback. This recovery event is not native schedule evidence.
- Platform watchdog [#43153156539](https://github.com/phanthienquoc/platform-infra/actions/runs/43153156539) failed its native inter-arrival checks. Its log reported gaps of 16,665s (reconcile), 17,233s (inspection), 17,135s (recovery) and 17,077s (watchdog), each above its respective budget. The diagnostic `workflow_run` event skipped TCE schedule collection; it did not assert TCE cadence.
- TCE native WF-12 [#43154415980](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/43154415980) ran at 04:22:53Z. Its heartbeat dispatch to Platform succeeded, but schedule delivery verification failed: latest native WF-06 #43127554403 was created at 00:28:39Z, age 234m, with measured queue wait 0m. This is a missed native WF-06 delivery, not evidence of runner queue congestion.
- TCE WF-13 [#43154436821](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/43154436821) succeeded by dispatching a read-only fallback. It logged exact ref `master`, SHA `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, source run #43154415980 and no workflow inputs. The fallback correlated to [WF-06 #43154458775](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/43154458775), which failed all four strict public probes: TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 (expected 200). A workflow_dispatch fallback does not satisfy native schedule freshness.
- The last observed empty `TCE_MAINTENANCE_MODE` remains from WF-13 #43127582309; the current Actions variable value is not exposed by this integration. TCE PR #1038's merged change adds an unset warning without changing fallback behavior or weakening HTTP-200 probes.

### Native schedule acceptance at 04:56:38Z

| Lane | Latest native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43152960974 | 2,810 | 16,665 | 2,700 | age FAIL / gap FAIL |
| Platform inspection | #43150245172 | 4,304 | 17,233 | 4,500 | age PASS / gap FAIL |
| Platform recovery | #43150505792 | 4,163 | 17,135 | 2,700 | age FAIL / gap FAIL |
| Platform watchdog | #43150601305 | 4,109 | 17,077 | 2,700 | age FAIL / gap FAIL |
| TCE WF-06 | #43127554403 | 16,079 | 23,393 | 1,500 | age FAIL / gap FAIL |
| TCE WF-12 | #43154415980 | 2,025 | 16,987 | 1,500 | age FAIL / gap FAIL |

All six inter-arrival budgets fail; five of six current-age budgets fail. Platform inspection #43150245172 remains within its 4,500s age budget by only 196s at this reference. It will expire at approximately 05:00:02Z (12:00:02 ICT) if no newer inspection completes. Platform reconciliation #43152960974 is already 110s beyond its 2,700s freshness budget. Do not count `workflow_run`, `repository_dispatch`, manual fallback or rerun attempts as native schedule delivery.

Current cron definitions were read from master and left unchanged: Platform reconcile `7,22,37,52 * * * *`, inspection `2,32 * * * *`, recovery `10,25,40,55 * * * *`, watchdog `12,27,42,57 * * * *`; TCE WF-06 `*/15 * * * *`, WF-12 `7,22,37,52 * * * *`. **TCE market-scan schedule unchanged.**

### GitOps, K3s and decommission evidence

- Current-master reconciliation #43152960974 is successful but is an apply-mode reconciliation with no drift, not a fresh `mode=plan` receipt. Its freshness age is 2,810s against a 2,700s budget at this checkpoint. No production manifest apply, image replacement or workload rollout occurred.
- Latest full inspection [#43150245172](https://github.com/phanthienquoc/platform-infra/actions/runs/43150245172) generated `debug/vps-latest.md` at 03:45:02Z. At 04:56:38Z it is 4,296s old, within the 4,500s budget by 204s. Node `tce-k3s-01` is Ready/ARM64 on K3s `v1.36.3+k3s1` and containerd `2.3.2-k3s2`; disk 57% (~20GiB free), available RAM ~19GiB, uptime ~194d13h, and `restart_required=yes`.
- Snapshot workload state: Media backend/frontend 1/1 Running with registry RepoDigests; MicroFE Shell/WS/NATS 1/1 Running; TCE frontend/service, Auth and Keycloak 0/0 intentional maintenance; Stock Admin two pods and desired Backend one pod are ImagePullBackOff on `12d63b4` with `no match for platform in manifest`. Legacy Stock Backend/Frontend remain 1/1 on `23b2878`, but the snapshot does not provide registry-qualified RepoDigest evidence for those legacy tags; local image IDs are not promotion provenance.
- Media runner service remains active/enabled and `Runner.Listener` is present. Platform runner is also active and must be preserved. Target Stock/Media namespaces passed the same-run storage preflight with no PVC/PV claims or VolumeSnapshot references. Preserve the separate `k3s-debug/k3s-debug-logs` PVC (1Gi, Bound, RWO). External backup/retention and authoritative DNS ownership remain unverified; DNS ownership is not inferred from Ingress hosts.
- Public OIDC realm probes returned HTTP 503. This is consistent with Keycloak being 0/0 maintenance; no live SSO health is claimed.
- Docker inventory showed 20 images / 9.195GB, 5.773GB reclaimable. No Docker cleanup or host reboot was performed.

### Governance, ownership and safety

- Direct branch API now confirms `protected=false` and required status-check enforcement `off` on all five master branches. Repository rulesets GET returned `[]` for Platform, TCE, Media and Authentication; Stock rulesets GET returned 403. Repository metadata still allows squash, merge commit and rebase on all five. Effective inherited organization rulesets remain unverified.
- App repositories own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health verification.
- No new GHCR publication or digest promotion; no production manifest apply, image replacement or workload rollout; no namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot.
- Preserve useful CI, test, security, build, publisher, release, backup, integration, manual and scheduled workflows. No workflow is proven redundant/obsolete and none was removed. No duplicate direct SSH/Compose production apply authority.

### Exact next actions

1. Platform operator: run fresh read-only `inspect-vps.yml` immediately (the current snapshot is due to expire at 05:00:02Z) and run current-master `reconcile-vps.yml` with `mode=plan` on `9f969fcfe0a8b31c5b612e218ea9f5a86e629059`; review the plan before any apply.
2. GitHub administrator: inspect authoritative repository/organization Actions schedule enqueue/delivery telemetry for the six missing native events. Existing evidence shows workflows active and measured queue waits of 0m / no lane above 15m, but does not identify why native schedule events stopped.
3. TCE administrator: verify the current `TCE_MAINTENANCE_MODE` value. Set true only for explicitly approved zero-replica maintenance; otherwise restore replicas and keep false. Preserve all four HTTP-200 probes.
4. GitHub administrator: enforce PR-only, required checks, block force-push/deletion and squash-only; verify inherited organization rulesets.
5. Media owner: stop/disable/unregister the dedicated runner and prove local Listener absence plus GitHub-side unregister; provide external backup/retention and authoritative DNS evidence before protected namespace deletion.
6. Stock owner: do not promote `12d63b4` or local image IDs; provide an ARM64-compatible immutable registry digest/provenance if Stock retirement is reversed. Provide `VNSTOCK_API_KEY` only through protected Actions secret storage if scraper operation is authorized.
7. Platform operator: obtain separate approval before host package/kernel/containerd/Docker upgrades or restart.

The GitHub connection used for this run is read-only for workflow dispatch and does not expose Actions variable/secret management. No fresh inspection/plan dispatch or maintenance-variable mutation was attempted from this run.


## Post-merge receipt — 2026-11-12 12:02 ICT / 05:02:05 UTC

- Platform PR #1670 (11:56 readiness/decommission evidence refresh) was squash-merged from exact head `145745ea3f00cadbed3b323ff92741ca0195cffc` to master `3dd57285c86502df58128c2b392fd4bf620396f4`.
- Exact-head `validate-manifests` run [#43158559048](https://github.com/phanthienquoc/platform-infra/actions/runs/43158559048) completed SUCCESS on the exact PR head. Contract, manifest render, shell, secret, immutable image, Keycloak isolation and network checks passed; changed-image-reference validation was skipped because the PR is documentation-only.
- Post-merge `validate-manifests` run [#43158638646](https://github.com/phanthienquoc/platform-infra/actions/runs/43158638646) completed SUCCESS on exact merge SHA `3dd57285c86502df58128c2b392fd4bf620396f4`.
- Direct `refs/heads/master` verification matched the merge SHA. PR #1670 is merged.
- PR #1670 changed only deployment tracker, workflow inventory, decommission runbook and two checkpoint documents. No production manifests, workflow definitions, image references, secrets, Actions variables, cron expressions or runtime resources changed.
- Current Platform master is `3dd57285c86502df58128c2b392fd4bf620396f4`. Open Platform owner-decision drafts remain #1314/#544/#541/#539; Authentication owner-decision draft #76 remains open.
- The 11:56 runtime snapshot remains historical evidence: current-master GitOps `mode=plan` and fresh K3s inspection still require an operator dispatch. Native schedule gaps, TCE HTTP 503, Stock ARM64 image-pull failure and Media runner/decommission gates are unchanged by this docs-only merge.
- TCE market-scan schedule unchanged.


## Current verified snapshot — 2026-11-12 15:59 ICT / 08:59:30 UTC

This refresh re-read all five default-branch refs, open PRs and their current head checks, the latest 100 Actions runs per repository, master check-runs, the current deployment tracker/workflow inventory, the latest available TCE health logs, Platform reconciliation/inspection receipts and native schedule histories. Only first-attempt `event=schedule` runs on `master` count as native schedule delivery. `workflow_run`, `workflow_dispatch`, `repository_dispatch`, push and rerun events are reported separately.

### Repository refs, open PRs and latest Actions evidence

| Repository | Verified master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `c6b71a37267db6c18279e07c2ed4ed4586254ccb` | #1314/#544/#541/#539 (all drafts / owner decisions) | Latest master validation #43180879007 SUCCESS on this exact SHA. Latest reconciliation #43176619995 SUCCESS on parent SHA `345f033a` via workflow_dispatch; latest inspection #43173781408 SUCCESS on `826b9427`; both runtime receipts are stale. Latest native reconcile #43152960974, inspect #43150245172, recovery #43150505792 and watchdog #43150601305. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Latest workflow_run WF-13 #43176605608 SKIPPED; WF-12 #43176586474 SUCCESS and WF-13 #43176586309 SUCCESS are workflow_run events, not native schedule. Latest native WF-06 #43176560763 FAILURE; all four public probes returned HTTP 503. Latest native WF-12 #43154415980 remains stale. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Master CI #42610360402 SUCCESS. Latest scraper schedule #42457182511 FAIL CLOSED because protected `VNSTOCK_API_KEY` is missing. No newer publication/promotion evidence. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Master CI #42539512417 SUCCESS. No newer current-master publication or Platform promotion evidence. Last K3s inspection showed Media backend/frontend 1/1 with registry RepoDigests; that inspection is now stale. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft / owner decision) | Master CI #42654579277 SUCCESS. No newer current-master release/promotion evidence. |

Platform PRs #1314, #544, #541 and #539 remain draft owner decisions; their latest head validation checks are successful but old. Authentication PR #76 remains a draft; its validation is successful and Supabase Preview is skipped. Do not merge any of these without the respective human decision. TCE, Stock and Media have no open PRs.

### Current master checks

- Platform: `validate-manifests` #43180879007 PASS on `c6b71a37`.
- TCE: WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 PASS. WF-06 #43176560763 fails public HTTP-200 probes; WF-12 #43176586474 and WF-13 #43176586309 are workflow_run successes, not native cadence evidence.
- Stock: CI #42610360402 PASS; scraper #42457182511 fails closed before dependency installation/scraping because `VNSTOCK_API_KEY` is absent.
- Media: CI #42539512417 PASS.
- Authentication: CI #42654579277 PASS.

### Native schedule acceptance — reference 08:59:30Z

| Lane | Latest qualifying native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43152960974 | 17,382 | 16,665 | 2,700 | FAIL |
| Platform inspection | #43150245172 | 18,876 | 17,233 | 4,500 | FAIL |
| Platform recovery | #43150505792 | 18,735 | 17,135 | 2,700 | FAIL |
| Platform watchdog | #43150601305 | 18,681 | 17,077 | 2,700 | FAIL |
| TCE WF-06 | #43176560763 | 4,958 | 25,693 | 1,500 | FAIL |
| TCE WF-12 | #43154415980 | 16,597 | 16,987 | 1,500 | FAIL |

All six current-age and inter-arrival budgets fail. Platform watchdog #43150601305 logs the same excessive inter-arrival gaps and does not establish runner congestion. TCE WF-12 #43176586474 verified the WF-06 source run at age 0m / queue 0m at 07:37:10Z and dispatched the authenticated heartbeat, but it was triggered by `workflow_run`, not by WF-12's native schedule. Do not count it as native schedule delivery. WF-06 #43176560763 itself ran natively at 07:36:52Z but failed all four strict public probes with HTTP 503.

No authoritative GitHub scheduler enqueue/delivery telemetry is exposed by the current integration, so delayed versus dropped scheduled events cannot be distinguished. Do not infer runner congestion from 0m measured queue wait. Keep every existing cron expression and freshness budget unchanged, especially the TCE market-scan schedule. Do not add a duplicate scheduler.

### GitOps, K3s and runtime freshness

- Latest successful reconciliation [#43176619995](https://github.com/phanthienquoc/platform-infra/actions/runs/43176619995) was a workflow_dispatch apply-mode run on parent SHA `345f033a`, not current master. At this reference its age is 4,929s against the 2,700s budget (expired). GHCR read preflight passed for five packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` was unchanged; TCE release pairing passed; drift=false; manifest apply, image replacement and workload rollout were skipped. Current master has only documentation/checkpoint commits after that parent, but this historical receipt is not a fresh current-master plan.
- Latest inspection [#43173781408](https://github.com/phanthienquoc/platform-infra/actions/runs/43173781408) generated `debug/vps-latest.md` at 07:14:30Z on parent SHA `826b9427`. Age is 6,308s against the 4,500s budget (expired). Snapshot recorded ARM64 Ubuntu 22.04.5, K3s node Ready, disk 57% (~20GiB free), ~19GiB RAM available, host restart required, and a live Media `Runner.Listener`.
- Last-known workloads from the inspection/reconciliation window: Media backend/frontend 1/1; MicroFE Shell/WS/NATS 1/1; TCE frontend/service and Auth/Keycloak 0/0 maintenance; Stock Admin two pods and desired Backend one pod in ImagePullBackOff on tag `12d63b4`. These are historical states, not current health assertions.
- The debug PVC `k3s-debug/k3s-debug-logs` remains a protected 1Gi Bound RWO claim. No namespace/PVC/PV deletion, runner retirement, Docker cleanup or host reboot occurred.

### Publisher ownership and safety

- App repositories retain ownership of tests/builds and immutable GHCR publication. Platform Infra remains the sole owner of production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, rollout and health verification.
- TCE WF-03/WF-08B and Auth release retain immutable digest/provenance and exact Platform dispatch contracts. Stock remains a gated immutable publisher with fail-closed scraper credentials. Media publisher has no Platform dispatch and remains in retirement scope.
- No new GHCR publication or digest promotion; no production manifest apply, image replacement or workload rollout in this refresh. No direct SSH/Compose production apply authority was introduced. Preserve CI/test/security/manual/release/backup/integration/scheduled workflows; no workflow was proven obsolete or removed.
- Current repository metadata still allows squash, merge commit and rebase; effective inherited organization rulesets/branch protection are not confirmed by this read. Keep owner-decision PRs open.

### Exact next actions

1. Platform operator: run a fresh read-only inspection and current-master `reconcile-vps.yml` with `mode=plan` on `c6b71a37267db6c18279e07c2ed4ed4586254ccb`; review the plan before any apply.
2. GitHub administrator: obtain authoritative Actions schedule enqueue/delivery telemetry for the six monitored lanes; preserve existing cron definitions and budgets.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE` and confirm whether zero-replica maintenance remains approved. If not, restore replicas through an approved change; keep all four HTTP-200 probes strict.
4. Stock owner: supply `VNSTOCK_API_KEY` through protected Actions secret storage only if scraper operation is authorized; do not bypass fail-closed behavior. Do not promote `12d63b4` or local image IDs without ARM64-compatible immutable registry digest/provenance.
5. Media owner: stop/disable/unregister the dedicated runner and prove Listener absence plus GitHub-side unregister; provide external backup/retention and authoritative DNS evidence before protected decommission.
6. GitHub administrator: enforce PR-only, required checks, block force-push/deletion and squash-only; verify inherited organization rulesets.
7. Platform operator: obtain separate approval before host package/kernel/containerd/Docker upgrades or restart.

The available GitHub integration supports repository/Actions reads, branch/PR creation and PR merge, but does not expose workflow dispatch or Actions variable/secret management. No fresh inspection/plan dispatch or maintenance-variable mutation was attempted. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 16:04 ICT / 09:04:35 UTC

- Platform PR #1680 was squash-merged from exact head `d61d9791f6ed8f4415a3ab59dd3243c7453160ca` to master `470cf1f6be68d1f68e61611792a39787003c2a1b`.
- Exact-head `validate-manifests` run [#43188151487](https://github.com/phanthienquoc/platform-infra/actions/runs/43188151487) completed SUCCESS on the exact PR head. All applicable contract, manifest-render, shell, secret, immutable-image, Keycloak-isolation and network checks passed; changed-image-reference validation was skipped because the PR is documentation-only.
- Post-merge `validate-manifests` run [#43188233039](https://github.com/phanthienquoc/platform-infra/actions/runs/43188233039) completed SUCCESS on exact merge SHA `470cf1f6be68d1f68e61611792a39787003c2a1b`. Direct `refs/heads/master` verification matched this SHA; PR #1680 is merged.
- PR #1680 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint documents. No production manifest, workflow definition, image reference, credential, Actions variable, runtime configuration, workload, DNS, database, storage or schedule changed.
- The 15:59 ICT snapshot remains an accurate evidence snapshot. Latest K3s inspection #43173781408 and reconciliation #43176619995 remain beyond their freshness budgets; this documentation merge does not refresh runtime evidence. Native schedule delivery remains degraded, and TCE WF-06 last returned four HTTP 503 probes.
- Current Platform master is `470cf1f6be68d1f68e61611792a39787003c2a1b`. TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3` and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f` remain unchanged.
- Open Platform owner-decision drafts remain #1314/#544/#541/#539; Authentication draft #76 remains open. No owner-decision PR was merged.
- No new GHCR publication/promotion, production apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**


## Latest cross-repo evidence — 2026-11-12 17:04 ICT / 10:04:47 UTC

This is a repository/Actions evidence refresh. It does not imply a fresh K3s inspection or GitOps plan; the last runtime receipts listed below are expired. All ages are calculated against the GitHub Actions API reference time above. Only first-attempt `event=schedule` runs on `master` count as native schedule delivery.

### Repository refs, open PRs and current-master checks

| Repository | Verified master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `466b848d9743843b48062fa53b2c9bd070fe2b09` | #1314/#544/#541/#539 (draft owner decisions) | `validate-manifests` #43188500016 SUCCESS on this exact SHA; check-run `validate` SUCCESS, `report-validation-failure` SKIPPED. Latest native reconcile #43152960974; inspection #43150245172; recovery #43150505792; watchdog #43150601305. Latest successful reconciliation #43176619995 was workflow_dispatch on parent SHA `345f033a`, now expired. Latest inspection #43173781408 was workflow_dispatch on parent `826b9427`, now expired. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-06 native schedule #43176560763 FAILURE; four independent public probes returned HTTP 503. WF-12 latest native schedule #43154415980 FAILURE. WF-12 #43176586474 and WF-13 #43176586309 SUCCESS are workflow_run events, not native schedule delivery. Master CI/build checks #43132696439/#43132696349 PASS. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | Master CI #42610360402 SUCCESS; its seven check runs all completed successfully. Latest scraper schedule #42457182511 FAIL CLOSED on missing protected `VNSTOCK_API_KEY`; no newer publication/promotion evidence. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | Master CI #42539512417 SUCCESS; no newer publication or Platform promotion evidence. Last K3s evidence for Media backend/frontend is stale. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft owner decision) | Master CI #42654579277 SUCCESS; build and validate checks PASS, Supabase Preview SKIPPED. No newer release/promotion evidence. |

All five direct master-branch reads report `protected=false`; required status-check enforcement is `off`. This is direct branch API evidence, not an inference from repository metadata. Effective inherited organization rulesets remain unverified. Do not merge owner-decision drafts.

### Native schedule acceptance — reference 10:04:47Z

| Lane | Latest qualifying native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43152960974 | 21,299 | 16,665 | 2,700 | FAIL |
| Platform inspection | #43150245172 | 22,793 | 17,233 | 4,500 | FAIL |
| Platform recovery | #43150505792 | 22,652 | 17,135 | 2,700 | FAIL |
| Platform watchdog | #43150601305 | 22,598 | 17,077 | 2,700 | FAIL |
| TCE WF-06 | #43176560763 | 8,875 | 25,693 | 1,500 | FAIL |
| TCE WF-12 | #43154415980 | 20,514 | 16,987 | 1,500 | FAIL |

All six age budgets and all six inter-arrival budgets fail. The latest TCE WF-12 success #43176586474 is a `workflow_run` heartbeat, not a native schedule. WF-13 #43176586309 is also `workflow_run`; neither resets native cadence. TCE WF-07 scheduled integration/backup runs do not satisfy WF-06/WF-12 acceptance.

TCE WF-06 #43176560763 ran natively at 07:36:52Z. Its four jobs independently returned HTTP 503: TCE web, TCE API, Auth liveness and Auth readiness. The logs show the expected status is HTTP 200 and the actual status was HTTP 503. Keep the strict probes; do not convert 503 to healthy or infer maintenance state from historical configuration.

The available GitHub integration exposes workflow-run/job history but no authoritative scheduler enqueue/delivery telemetry. Queue checks in WF-12 measured 0 minutes for its inspected source run; this does not prove that scheduled events were delivered on time and does not establish runner congestion. Do not add a second scheduler, change cron expressions or relax freshness budgets. **TCE market-scan schedule unchanged.**

### GitOps, K3s and runtime freshness

- Last successful reconciliation [#43176619995](https://github.com/phanthienquoc/platform-infra/actions/runs/43176619995) was created 07:37:21Z as `workflow_dispatch` on parent SHA `345f033a37b2ab944614bd688a58bc5c60d01764`. It completed SUCCESS at 07:39:09Z. Five GHCR package reads passed; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` was unchanged; TCE release pairing passed; drift=false; manifest apply, image replacement and workload rollout were skipped. At 10:04:47Z its age is 8,846s against the 2,700s budget: EXPIRED. It is not a current-master plan receipt.
- Last inspection [#43173781408](https://github.com/phanthienquoc/platform-infra/actions/runs/43173781408) was created 07:14:22Z on parent SHA `826b94276a1f2253240d560ea663bb39cb420b65`, completed 07:16:39Z. At 10:04:47Z its age is 10,225s against the 4,500s budget: EXPIRED. Do not assert current K3s health from this snapshot.
- Last-known snapshot: ARM64 K3s node Ready, disk 57% (~20GiB free), ~19GiB RAM available, host restart required; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend in ImagePullBackOff on tag `12d63b4`; Media runner service active and `Runner.Listener` present. These are historical states only.
- Stock desired image tag `12d63b4` still lacks compatible ARM64 manifest/RepoDigest evidence. Do not promote local image IDs or legacy tags.
- Preserve debug PVC `k3s-debug/k3s-debug-logs` (1Gi, Bound, RWO). No namespace/PVC/PV deletion, runner retirement, Docker cleanup or host reboot is authorized by this snapshot.

### Ownership, publication and safety

- App repositories own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and runtime health verification.
- TCE WF-03/WF-08B and Auth release retain immutable digest/provenance and exact Platform dispatch contracts. Stock remains a gated immutable publisher with fail-closed scraper credentials. Media publisher remains without Platform dispatch or production apply while decommission is unresolved.
- No new GHCR publication/promotion, current-master GitOps plan/apply, production manifest mutation, image replacement or workload rollout occurred in this evidence refresh. No direct SSH/Compose production apply authority was introduced. Preserve useful CI/test/security/manual/release/backup/integration/scheduled workflows; no workflow is confirmed obsolete or removed.
- No credential rotation, DNS/database/storage mutation, runner retirement, namespace/PVC/PV deletion, Docker cleanup or host reboot occurred.

### Exact next actions

1. Platform operator: obtain a fresh read-only K3s inspection and run current-master `reconcile-vps.yml` with `mode=plan` on `466b848d9743843b48062fa53b2c9bd070fe2b09`; review the plan before any apply.
2. GitHub administrator: obtain authoritative Actions scheduler enqueue/delivery telemetry for the six monitored lanes; preserve all existing cron expressions and budgets.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE` and explicitly confirm approved zero-replica maintenance or restore replicas through an approved change; keep all four HTTP-200 probes strict.
4. Stock owner: provide `VNSTOCK_API_KEY` only through protected Actions secret storage if scraper operation remains authorized. Do not bypass fail-closed behavior or promote `12d63b4` without ARM64-compatible immutable digest/provenance.
5. Media owner: stop/disable/unregister the dedicated runner and prove Listener absence plus GitHub-side unregister; provide external backup/retention and authoritative DNS evidence before protected decommission.
6. GitHub administrator: enforce PR-only, required checks, block force-push/deletion and squash-only; verify inherited organization rulesets.
7. Platform operator: obtain separate approval before host package/kernel/containerd/Docker upgrades or restart.

The current GitHub integration supports repository/Actions reads, branch/PR creation and PR merge, but does not expose workflow dispatch or Actions variable/secret management. No fresh inspection/plan dispatch or maintenance-variable mutation was attempted. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 17:09 ICT / 10:09:11Z

- Platform PR #1682 was squash-merged from exact head `51b85670f38afc02e1271778a000d0e7bb41d7a2` to master `ff914b1f352eeb571e669e997c93bd6bfe342800`.
- Exact-head validation #43197648043 completed SUCCESS on the exact PR head; all 21 validation steps passed, with the failure-report job correctly skipped.
- Post-merge `validate-manifests` #43197786121 completed SUCCESS on the exact merge SHA `ff914b1f352eeb571e669e997c93bd6bfe342800`. Direct `refs/heads/master` verification matched the merge SHA. All applicable contract, shell, manifest-render, secret, immutable-image, Keycloak-isolation and network checks passed; changed-image-reference validation was skipped because the PR is documentation-only.
- PR #1682 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint documents. No production manifest, workflow definition, image reference, credential, Actions variable, runtime resource, DNS, database, storage or schedule changed.
- The 17:04 ICT evidence snapshot remains historical and accurate for its reference time. Native schedule gaps remain unresolved; latest K3s inspection #43173781408 and reconciliation #43176619995 are expired and are not current-master runtime evidence. No fresh K3s inspection or current-master GitOps plan was available through this integration.
- Current Platform master is `ff914b1f352eeb571e669e997c93bd6bfe342800`. TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3` and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f` remain unchanged.
- Open Platform owner-decision drafts remain #1314/#544/#541/#539; Authentication draft #76 remains open. No owner-decision PR was merged.
- No GHCR publication/promotion, GitOps apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**
