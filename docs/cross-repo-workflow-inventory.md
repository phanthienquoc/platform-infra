## Post-merge receipt — 2026-11-12 15:10 ICT

Platform PR #1678 was squash-merged at 184c75e7ac5491ce386ff8d3a886a2ba4dcc434c. Exact-head validate-manifests #43180530521 completed SUCCESS on 434f9549dd9a1a40a3691be96ecde1be9e842764; all 20 applicable validation steps passed. Post-merge validate-manifests #43180598767 then completed SUCCESS on the exact current master SHA 184c75e7ac5491ce386ff8d3a886a2ba4dcc434c; all 20 applicable steps passed, with changed-image validation correctly skipped for documentation-only changes.

PR #1678 changed only the deployment readiness tracker, workflow inventory and two checkpoint files. No production manifest, workflow definition, credential, runtime configuration, workload, DNS, storage or schedule changed. Current Platform master is 184c75e7ac5491ce386ff8d3a886a2ba4dcc434c; TCE 34f6024f8ccec8fb3ab6688901b3557e058ddfd1, Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61, Media dcd698699c65ba6e73f6b43838975144777131c3 and Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f remain unchanged.

The 15:02 ICT snapshot and 15:07 receipt remain accurate for the unchanged production manifest tree. Current runtime evidence remains the inspection/reconciliation receipts recorded there; no new production mutation occurred. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

## Post-merge receipt — 2026-11-12 15:07 ICT

Platform PR #1677 was squash-merged at f4b03f3153daf4feb5521d0098a9bc81fe56dd1b. Exact-head validate-manifests #43180328807 completed SUCCESS on 80ff0fd7d5475a30a033cba596ace332b19e2a25; all 20 applicable validation steps passed.

PR #1677 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint files. No production manifest, workflow definition, credential, runtime configuration, workload, DNS, storage or schedule changed. The current Platform master is f4b03f3153daf4feb5521d0098a9bc81fe56dd1b; TCE 34f6024f8ccec8fb3ab6688901b3557e058ddfd1, Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61, Media dcd698699c65ba6e73f6b43838975144777131c3 and Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f remain unchanged.

The 15:02 ICT snapshot below is an accurate pre-merge evidence snapshot. PR #1677 was documentation-only, so the referenced current-master reconciliation and K3s evidence remain applicable to the unchanged production manifest tree. No post-merge workflow run on the new merge SHA was present in the queried Actions history at this receipt. Do not represent PR validation as a post-merge runtime check.

No production mutation occurred as part of PR #1677. The referenced reconciliation #43176619995 separately provisioned/verified the Auth runtime Secret (values suppressed); shared ghcr-pull remained unchanged. Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

## Current verified workflow inventory — 2026-11-12 15:02 ICT / 08:02:05 UTC

### Repositories, latest runs and ownership

| Repository | Master SHA | Open PRs | Latest workflow evidence | Deployment ownership |
|---|---|---|---|---|
| Platform Infra | 345f033a37b2ab944614bd688a58bc5c60d01764 | #1314/#544/#541/#539 (owner decisions) | Inspection #43173781408 SUCCESS; PR #1676 exact-head validation #43173998401 PASS and merged; current-master reconciliation #43176619995 SUCCESS; recovery #43176810214 SUCCESS | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health |
| TCE Dashboard | 34f6024f8ccec8fb3ab6688901b3557e058ddfd1 | none | Native WF-06 #43176560763 FAIL (four HTTP 503 probes); WF-12 #43176586474 workflow_run SUCCESS and heartbeat accepted; latest native WF-12 #43154415980 remains stale | App CI/tests/builds, immutable GHCR publication and provenance; no direct production apply |
| StockDividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED (missing protected VNSTOCK_API_KEY); desired tag 12d63b4 lacks ARM64-compatible registry digest evidence | App CI/builds and immutable GHCR publication; Platform owns promotion/retirement |
| Media Generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 PASS; K3s snapshot shows backend/frontend 1/1 with RepoDigests; runner still active | App CI/builds and immutable GHCR publication; Platform owns production apply; Media owner retires its runner |
| Authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (owner decision) | CI #42654579277 PASS; no newer current-master release/promotion evidenced | App CI/security/builds, immutable GHCR, SBOM/provenance and exact Platform dispatch; Platform owns production apply |

### Platform authority and workflow roles

- reconcile-vps.yml remains the sole production GitOps apply authority. Native schedule is 7,22,37,52 * * * *; scheduled events use apply mode and image changes remain disallowed unless exact provenance-verified promotion dispatch authorizes them.
- inspect-vps.yml remains read-only, scheduled at 2,32 * * * *; it may create an inspection PR after exact-head validation and squash merge. PR #1676 is the latest verified example.
- reconcile-schedule-watchdog.yml remains read-only, scheduled at 12,27,42,57 * * * *.
- recover-stale-ops.yml remains a recovery controller, scheduled at 10,25,40,55 * * * *; it may dispatch only existing validated workflows after source/provenance/deduplication/correlation checks and is not a separate apply authority.
- TCE WF-06 remains scheduled every 15 minutes and retains strict HTTP-200 probes. WF-12 runs at minutes 7/22/37/52, verifies WF-06 native delivery and forwards authenticated heartbeat receipts. WF-13 remains workflow_run-only and can dispatch only the read-only WF-06 fallback; fallback is not native schedule evidence.
- TCE WF-03/WF-08B, Stock deploy.yml and Auth release.yml retain app-owned immutable publication responsibilities. Media retains app-owned build/publication; Platform alone promotes verified digests and applies production manifests.
- TCE WF-06 #43176560763 and WF-12 heartbeat #43176586474 demonstrate exact source/attempt/SHA correlation. Platform recovery #43176601065 validated the payload and dispatched current-master reconciliation #43176619995; this proves the cross-repo dispatch path but does not repair native schedule cadence.
- Current native schedule acceptance at 08:02:05Z: all six tracked Platform/TCE lanes exceed age and inter-arrival budgets. WF-06 had one native schedule event after a 25,693s gap and failed all four probes; WF-12's latest run is workflow_run, not schedule. Platform fallback dispatches are not native schedule receipts.
- Current runtime: inspection #43173781408 snapshot age 2,855s vs 4,500s; current-master reconciliation #43176619995 age 1,484s vs 2,700s. Reconciliation no-drift, apply skipped, rollout skipped; Auth runtime Secret provisioned/verified, shared ghcr-pull unchanged; TCE release pairing passed.
- Auth and TCE are explicitly intentional zero-replica maintenance scopes; no live workload health is asserted. Keycloak skipped. MicroFE active-scope health passed.
- Stock desired tag 12d63b4 has no compatible ARM64 manifest/RepoDigest and remains ImagePullBackOff; no promotion. Stock scraper fails closed without protected VNSTOCK_API_KEY.
- Media backend/frontend are 1/1 with RepoDigests, but Media runner and Listener remain active. External backup/retention, authoritative DNS and protected decommission approval are still required.
- Preserve PVC k3s-debug/k3s-debug-logs (Bound, 1Gi, RWO). Stock/Media target namespaces had no PVC/PV/VolumeSnapshot references in the latest inspection; this does not replace external backup/DNS evidence.
- No workflow was confirmed redundant/obsolete. Preserve CI/tests, security, backup, manual, release and scheduled workflows. No duplicate direct SSH/Compose production apply authority.
- TCE market-scan schedule unchanged.

Last reviewed: 2026-11-12 15:02 ICT (2026-11-12 08:02:05 UTC).

## Post-merge receipt — 2026-11-12 14:00 ICT / 07:00:17 UTC

Platform PR #1674 squash-merged at `7ddaf5cd7f5735673c2fb052859fca61da786d0e`. Exact-head validation #43171924642 PASS; post-merge validate-manifests #43172008740 PASS on exact merge SHA (20 successful steps). The PR changed only tracker/inventory/checkpoint documentation; production manifests and workflows were unchanged.

Current Platform master: `7ddaf5cd7f5735673c2fb052859fca61da786d0e`. TCE `34f6024f`, Stock `b1b5e177`, Media `dcd69869`, Authentication `eab85fab`.

At 07:00:17Z all six tracked Platform/TCE native schedule lanes remain over both age and inter-arrival budgets. Ages: reconcile 10,229s; inspection 11,723s; recovery 11,582s; watchdog 11,528s; TCE WF-06 23,498s; TCE WF-12 9,444s. Gaps: 16,665s / 17,233s / 17,135s / 17,077s / 23,393s / 16,987s. No native schedule run superseded the prior evidence. Preserve all cron expressions, especially the TCE market-scan schedule.

Current runtime evidence is stale: reconciliation #43152960974 age 10,229s vs 2,700s; K3s inspection #43150245172 age 11,723s vs 4,500s. Do not infer live cluster health, rollout or drift state from these snapshots.

Branch governance: all five `GET /branches/master` responses show `protected=false`. Rulesets GET returned [] for Platform/TCE/Media/Auth; Stock returned 403 due plan/API restriction. Branch-protection detail GET returned 403 due integration permissions for all five. Administrator must configure and verify PR-only, required checks, no force-push/deletion and squash-only; organization-level policy is not established by these reads.

No production apply, image promotion, rollout, secret/credential change, runner retirement, storage/DNS/database mutation or host restart occurred. Platform Infra remains the sole production apply authority. No workflow was removed.

## Current verified workflow inventory — 2026-11-12 13:56 ICT / 06:56:46 UTC

### Repositories, latest runs and ownership

| Repository | Master SHA | Open PRs | Latest workflow evidence | Deployment ownership |
|---|---|---|---|---|
| Platform Infra | `c1257c38` | #1314/#544/#541/#539 (owner decisions) | validate-manifests #43165632162 PASS; latest native reconcile #43152960974 SUCCESS but stale | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health |
| TCE Dashboard | `34f6024f` | none | WF-12 #43154415980 schedule FAIL; WF-13 #43154436821 SUCCESS; WF-06 fallback #43154458775 FAIL (four HTTP 503); WF-01/02/05 PASS | App CI/tests/builds, immutable GHCR publication and provenance; no direct production apply |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`) | App CI/builds and immutable GHCR publication; Platform owns promotion/retirement |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; no newer current-master publication in latest 100 Actions runs | App CI/builds and immutable GHCR publication; Platform owns production apply; Media owner retires its runner |
| Authentication | `eab85fab` | #76 (owner decision) | CI #42654579277 PASS; no newer current-master release/promotion in latest 100 Actions runs | App CI/security/builds, immutable GHCR, SBOM/provenance and exact Platform dispatch; Platform owns production apply |

### Platform authority and workflow roles

- `reconcile-vps.yml` is the sole production GitOps apply authority. Native schedule is `7,22,37,52 * * * *`; scheduled events use apply mode and image changes remain disallowed unless the exact provenance-verified promotion dispatch authorizes them.
- `inspect-vps.yml` is read-only inspection with a schedule of `2,32 * * * *`; it may create a dedicated inspection PR after validating exact head.
- `reconcile-schedule-watchdog.yml` is read-only, scheduled at `12,27,42,57 * * * *`; it checks workflow enabled state, schedule freshness, queue assignment, native inter-arrival and verified TCE heartbeat receipts.
- `recover-stale-ops.yml` is scheduled at `10,25,40,55 * * * *`; it may dispatch only existing validated inspection/reconciliation workflows after source, provenance, deduplication and exact-run correlation checks. It is not an apply authority.
- TCE WF-06 remains scheduled every 15 minutes and keeps strict HTTP-200 probes. WF-12 runs at minutes 7/22/37/52 and sends authenticated heartbeat receipts to Platform while separately verifying WF-06 native delivery. WF-13 is workflow_run-only and may dispatch only the read-only WF-06 fallback after validated failure/staleness; fallback is not native schedule evidence.
- TCE WF-03/WF-08B, Stock deploy.yml and Auth release.yml retain app-owned immutable publication responsibilities. Platform alone promotes verified digests and applies production manifests. Media CI passes but no newer current-master publication is evidenced.
- Preserve app CI/tests, security scans, provenance/SBOM, backup/integration, manual/release and purposeful scheduled jobs. No workflow was confirmed redundant/obsolete and none was removed.
- No duplicate direct SSH/Compose production deployment authority was introduced.
- Current schedule acceptance: all six tracked Platform/TCE lanes exceed age and inter-arrival budgets at 06:56:46Z. Platform queue assignment checks passed; TCE WF-12 measured 0m queue wait for stale WF-06. Runner congestion is not established; authoritative GitHub scheduler delivery telemetry is still required.
- Runtime evidence: reconciliation #43152960974 is 10,018s old vs 2,700s budget; inspection #43150245172 is 11,512s old vs 4,500s budget. Historical run results are not current rollout/health receipts.
- TCE public endpoints returned HTTP 503 in fallback #43154458775; keep HTTP-200 acceptance strict. TCE/Auth maintenance variable and replica intent require administrator verification.
- Stock desired tag `12d63b4` lacks compatible ARM64 RepoDigest evidence; scraper remains fail-closed without protected API key.
- Media runner/Listener retirement, external backup/retention, authoritative DNS and protected decommission approval remain blockers.
- Five master branches' protection was not re-read in this snapshot; administrator must verify effective rulesets and enforce PR-only, required checks, no force-push/deletion and squash-only.
- TCE market-scan schedule unchanged.

Last reviewed: 2026-11-12 13:03 ICT (2026-11-12 06:03:32 UTC).


## Post-merge receipt — 2026-11-12 13:03:32 ICT / 06:03:32 UTC

Platform PR #1672 was squash-merged at `856c37b3342cdd564aaf6e1e3f2996a51832e55e`. Exact-head validate-manifests #43165357610 completed SUCCESS on `d0971a2cdb82f867a143676110e429aa71b0a78e`; post-merge validate-manifests #43165429654 completed SUCCESS on the exact merge SHA. All 20 applicable validation steps passed.

The PR changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint files. No production manifest, workflow, secret, credential, runtime configuration or schedule changed. Current Platform master is `856c37b3`; TCE `34f6024f`, Stock `b1b5e177`, Media `dcd69869` and Authentication `eab85fab` remain unchanged.

The 12:59 ICT snapshot above remains an accurate pre-merge evidence snapshot. At 06:03:32Z, its native schedule ages have increased by 265s: reconcile 6,824s; inspection 8,318s; recovery 8,177s; watchdog 8,123s; TCE WF-06 20,093s; TCE WF-12 6,039s. Inter-arrival gaps remain 16,665s / 17,233s / 17,135s / 17,077s / 23,393s / 16,987s. Thus all six age budgets and all six gap budgets still fail. K3s snapshot #43150245172 is 8,310s old vs 4,500s budget; reconciliation #43152960974 is 6,824s old vs 2,700s budget. No new native schedule, K3s inspection or current-master reconciliation was observed after the 12:59 snapshot.

No production mutation occurred. Platform Infra remains the sole production apply authority; TCE market-scan schedule remains unchanged.



## Current verified workflow inventory — 2026-11-12 12:59 ICT / 05:59:07 UTC

### Repository refs, open PRs, latest runs and ownership

| Repository | Master SHA | Open PRs | Latest relevant run evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `1e84b2e0` | #1314/#544/#541/#539 (owner decisions) | Current-master validate-manifests #43158871069 PASS. Native reconcile #43152960974 SUCCESS at 04:09:48Z; watchdog #43150601305 FAIL on stale age/inter-arrival; recovery #43150505792 SUCCESS as native schedule but stale. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f` | none | WF-12 #43154415980 native schedule FAIL (WF-06 age 234m; queue 0m); WF-13 #43154436821 SUCCESS; fallback WF-06 #43154458775 FAIL on four HTTP 503s. WF-01/02/05 latest master runs PASS. | App tests/builds, security, immutable GHCR publication and provenance; no direct production apply. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED (missing `VNSTOCK_API_KEY`). | App tests/builds and immutable GHCR publication/provenance; Platform owns production promotion/retirement. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; no new current-master publication evidenced. Last K3s snapshot shows backend/frontend RepoDigests, but snapshot is expired. | App tests/builds and immutable GHCR publication/provenance; Platform owns production apply; Media owner retires its runner. |
| Authentication | `eab85fab` | #76 (owner decision) | CI #42654579277 PASS; no new current-master release evidenced. | App tests/builds, security, immutable GHCR, SBOM/provenance and exact Platform dispatch contract; Platform owns production apply. |

### Platform production authority and current evidence

- `reconcile-vps.yml` remains the sole production GitOps apply authority.
- `inspect-vps.yml` and `reconcile-schedule-watchdog.yml` remain read-only.
- `recover-stale-ops.yml` may dispatch only the existing validated reconciliation/inspection workflows after exact source and freshness checks; it does not apply manifests itself.
- Reconciliation #43152960974 succeeded on parent SHA `9f969fc`: five GHCR package reads passed; Auth runtime Secret verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing passed; drift=false; apply/image replacement/rollout skipped. It is stale at the current reference (6,559s vs 2,700s).
- K3s inspection #43150245172 generated 03:45:02Z and is stale at the current reference (8,045s vs 4,500s). Its workload details remain historical only.

### Native schedule acceptance — 05:59:07Z

| Lane | Latest qualifying native run | Age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #43152960974 | 6,559 | 16,665 | 2,700 |
| Platform inspection | #43150245172 | 8,053 | 17,233 | 4,500 |
| Platform recovery | #43150505792 | 7,912 | 17,135 | 2,700 |
| Platform watchdog | #43150601305 | 7,858 | 17,077 | 2,700 |
| TCE WF-06 | #43127554403 | 19,828 | 23,393 | 1,500 |
| TCE WF-12 | #43154415980 | 5,774 | 16,987 | 1,500 |

All six current-age and inter-arrival budgets fail. Platform queue-assignment checks passed in watchdog #43150601305; TCE WF-12 measured zero queue delay for the stale WF-06 source. Runner saturation is not established. Only original first-attempt `event=schedule` runs on `master` count. Workflow dispatch, workflow_run, repository_dispatch, push and reruns are transport/diagnostic evidence only.

### Workflow preservation and unresolved gates

- Preserve app CI/tests, security scans, immutable publishers, SBOM/provenance, backup/integration workflows, manual/release gates and all purposeful schedules.
- No workflow was confirmed redundant or obsolete; none was removed.
- Keep TCE WF-06 strict HTTP 200. WF-13 warns on unset maintenance mode and dispatches only read-only fallback; administrator must verify `TCE_MAINTENANCE_MODE`.
- Stock desired image `12d63b4` lacks compatible ARM64 RepoDigest evidence; do not promote legacy local image IDs. Scraper remains fail-closed without its protected API secret.
- Media runner and Listener were present in the expired K3s snapshot; do not decommission until owner supplies runner unregister, backup/retention, DNS and protected approval evidence.
- All five default branches were previously observed as `protected=false`; effective inherited organization rulesets remain unverified. Administrator action remains open in issue #1575.
- No duplicate direct SSH/Compose production deployment authority is introduced. Platform Infra remains the only production apply authority.
- TCE market-scan schedule remains unchanged.


## Post-merge receipt — 2026-11-12 11:04 ICT / 2026-11-12 04:04:42 UTC

Platform PR #1668 was squash-merged at `af37d170ea755f1bca4c3f413d6a04b8d2d7210f`. Exact-head validation #43152296355 completed SUCCESS on `2cbe16d1961313a24bc9147e1aba36c9bf7b0555`; post-merge validate-manifests #43152354741 completed SUCCESS on the exact merge SHA. All applicable manifest/contract validation steps passed. The PR changed only the deployment tracker, workflow inventory and two timestamped checkpoint files; no production manifest, workflow, secret, credential or runtime configuration changed.

The 10:59 ICT receipt above remains an accurate timestamped snapshot taken at 03:59:56Z on Platform master `55cacb6d`. Current Platform master is now `af37d170`; TCE `34f6024f`, Stock `b1b5e177`, Media `dcd69869` and Authentication `eab85fab` remain unchanged. Open owner-decision PRs remain Platform #1314/#544/#541/#539 and Authentication #76; PR #1668 is merged.

At 04:04:42Z, no new qualifying native schedule run superseded the 10:59 IDs. Current-age values increased by 286s to: reconcile 16,359s; inspection 1,188s; recovery 1,047s; watchdog 993s; TCE WF-06 12,963s; TCE WF-12 15,896s. Inter-arrival gaps remain 22,471s / 17,233s / 17,135s / 17,077s / 23,393s / 22,441s respectively. Thus 3/6 age budgets and 6/6 gap budgets still fail. Do not change cron or TCE market-scan schedule.

Current-master reconciliation #43150525282 remains successful evidence on the parent manifest tree (age 1,036s vs 2,700s budget); it found no drift, verified five GHCR package reads, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, and skipped manifest apply/image replacement/rollout. K3s snapshot generated 03:45:02Z is 1,180s old vs 4,500s budget. Both remain within freshness budgets at this reference; no new runtime mutation occurred.

All five master branches still report `protected=false`; effective inherited organization rulesets remain unverified. TCE/Auth zero-replica maintenance, Stock ImagePullBackOff, Media runner/Listener active, Stock/Media decommission evidence gaps and host restart approval remain unchanged. No workflow was removed and no production mutation occurred.


## Latest workflow inventory verification — 2026-11-12 10:59 ICT / 2026-11-12 03:59:56 UTC

### Repository refs, open PRs, latest runs and ownership

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `55cacb6d` | #1314/#544/#541/#539 owner decisions | Inspection PR #1667 exact-head validation #43150444565 PASS and merged. Current-master reconciliation #43150525282 SUCCESS; watchdog #43150601305 FAIL on native cadence; recovery #43150855730 SUCCESS (workflow_dispatch). | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f` | none | WF-01 #43132696439, WF-02 #43132696403, WF-05 #43132696349 PASS. Native WF-06 #43127554403 four HTTP 503 failures; WF-12 #43121528127 FAIL. WF-07 backup #43130553977 PASS. | App tests/builds, security, immutable GHCR publication and release provenance; no direct production apply. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED (missing `VNSTOCK_API_KEY`). Desired `12d63b4` has ImagePullBackOff/no compatible ARM64 RepoDigest in latest inspection. | App tests/builds and immutable GHCR publication/provenance; production retirement/promotion remains Platform-owned. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; no current-master publication evidenced. Backend/frontend last inspected 1/1 with RepoDigests; dedicated runner active and Listener present. | App tests/builds and immutable GHCR publication/provenance; runner retirement is owner/operator work. |
| Authentication | `eab85fab` | #76 owner decision | CI #42654579277 PASS; no current-master release evidenced. | App tests/builds, security, immutable GHCR, SBOM/provenance and exact Platform dispatch contract; Platform owns production apply. |

### Current-master Platform reconciliation and runtime evidence

- Reconciliation #43150525282 SUCCESS on exact current master `55cacb6d`, `mode=apply`, `target_app=all`, `allow_image_changes=false`. Five GHCR package reads passed; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing passed; drift=false; manifest apply, image replacement and rollout skipped.
- TCE/Auth lanes report maintenance/zero replicas, not live availability; MicroFE active-scope health passed; Keycloak skipped. No new GHCR publication or digest promotion.
- Full K3s inspection #43150245172 generated `debug/vps-latest.md` at 03:45:02Z and is fresh at the 03:59:56Z reference (894s vs 4,500s). Node Ready/ARM64, disk 57% (~20GiB free), ~19GiB RAM available; host restart required. Media/MicroFE/NATS 1/1. TCE/Auth/Keycloak 0/0 maintenance. Stock Admin has two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod for tag `12d63b4`; legacy Stock Backend/Frontend have no registry RepoDigest evidence.
- Media runner service and Listener remain active. Preserve the Bound debug PVC `k3s-debug/k3s-debug-logs` (1Gi/RWO). Stock/Media deletion remains blocked by external backup/retention, authoritative DNS, runner stop/disable/Listener absence/GitHub unregister and protected production approval.

### Native schedule acceptance — 03:59:56Z

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #43120544165 | 16,073 | 22,471 | 2,700 |
| Platform inspection | #43150245172 | 902 | 17,233 | 4,500 |
| Platform recovery | #43150505792 | 761 | 17,135 | 2,700 |
| Platform watchdog | #43150601305 | 707 | 17,077 | 2,700 |
| TCE WF-06 | #43127554403 | 12,677 | 23,393 | 1,500 |
| TCE WF-12 | #43121528127 | 15,610 | 22,441 | 1,500 |

Three of six age budgets fail and all six inter-arrival budgets fail. Only first-attempt `event=schedule` runs on master count. Workflow_dispatch, workflow_run, repository_dispatch, push and reruns do not count. WF-06 returned HTTP 503 on all four strict endpoints. Preserve all cron expressions and the TCE market-scan schedule.

### Workflow preservation and governance

All five master branch API reads report `protected=false`; effective inherited organization rulesets remain unverified. Administrator action is required for PR-only, required checks, force-push/deletion protection and squash-only. Preserve CI/test/security, build, immutable publisher, provenance/SBOM, backup, integration, manual, release and scheduled workflows. No workflow is confirmed redundant/obsolete. Do not add competing SSH/Compose deployment authority.

Platform Infra remains the only production apply authority. No image publication/promotion, manifest apply, rollout, namespace/storage deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred in this verification.


Last reviewed: 2026-11-12 09:05 ICT (2026-11-12 02:05:00 UTC).




## Post-merge workflow inventory receipt — 2026-11-12 09:05 ICT / 02:05:00 UTC

Platform PR #1663 is merged at `c84b19b6`; exact-head validation #43138768416 and post-merge validation #43138836807 both PASS. The 08:59 checkpoint remains the pre-merge snapshot.

| Repository | Master SHA | Open PRs | Latest relevant evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `c84b19b6` | #1314/#544/#541/#539 | Post-merge validate-manifests #43138836807 PASS. | Production manifests, shared GHCR pull credentials, digest promotion, GitOps, rollout and health. |
| TCE Dashboard | `34f6024f` | none | WF-01 #43132696439, WF-02 #43132696403, WF-05 #43132696349 PASS; native WF-06 #43127554403 and WF-12 #43121528127 FAIL. | Tests/builds, immutable GHCR publication, release provenance. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED (missing `VNSTOCK_API_KEY`). | Tests/builds and immutable GHCR publication. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; no current-master publication evidenced. | Tests/builds and immutable GHCR publication; dedicated runner retirement requires owner/operator. |
| Authentication | `eab85fab` | #76 owner decision | CI #42654579277 PASS; no current-master release evidenced. | Tests/builds, immutable GHCR, SBOM/provenance and Platform dispatch contract. |

All six Platform/TCE native schedule lanes remain outside both current-age and inter-arrival budgets at 02:05:00Z. Manual and fallback events do not satisfy schedule acceptance. Preserve every cron and the TCE market-scan schedule.

Runtime freshness: reconciliation #43127613751 is 5,751s old vs 2,700s; full inspection #43127872524 is 5,619s old vs 4,500s. Both are historical only. No current-master plan/inspection or runtime mutation is evidenced.

App repositories own CI/tests/builds, security and immutable publication/provenance. Platform Infra is the only production manifest, shared pull credential, promotion, GitOps, rollout and health authority. Preserve useful CI/test/security, backup, integration, manual, release and scheduled workflows. No workflow is confirmed obsolete; no duplicate SSH/Compose authority.
Last reviewed: 2026-11-12 09:05 ICT (2026-11-12 02:05:00 UTC).


## Latest workflow inventory verification — 2026-11-12 08:59 ICT / 2026-11-12 01:59:28 UTC

| Repository | Master SHA | Open PRs | Latest workflow evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `85c0d1fe` | #1314/#544/#541/#539 owner decisions | Master validate-manifests #43132927187 SUCCESS. PR #1661/#1662 merged with exact-head and post-merge checks passing. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f` | none | PR #1038 merged. WF-01 #43132696439, WF-02 #43132696403, WF-05 #43132696349 SUCCESS. Native WF-06 #43127554403 FAIL (four HTTP 503); native WF-12 #43121528127 FAIL. WF-13 #43127582309 logged empty maintenance variable before the warning fix merged. | App tests/builds, immutable GHCR publication and release evidence; no VPS SSH/Compose deployment. |
| StockDividend | `b1b5e177` | none | CI #42610360402 SUCCESS. Scheduled scraper #42457182511 FAIL CLOSED due to missing `VNSTOCK_API_KEY`. Desired tag `12d63b4` lacks compatible ARM64 manifest/RepoDigest in last full inspection. | App tests/builds, immutable GHCR publication and provenance; production retirement/promotion remains Platform-owned. |
| Media Generation | `dcd69869` | none | CI #42539512417 SUCCESS; no current-master publication/handoff evidenced. Last full inspection showed backend/frontend 1/1 with digest pins; dedicated runner active with Listener present. | App tests/builds, immutable GHCR publication and provenance; runner retirement is an owner/operator task; no direct production deploy authority. |
| Authentication | `eab85fab` | #76 owner-decision draft | CI #42654579277 SUCCESS; no current-master release/handoff evidenced. | App tests/builds, immutable GHCR publication, SBOM/provenance and exact Platform dispatch payload; Platform owns production apply. |

### Current ownership and runtime evidence

- Platform reconciliation #43127613751 SUCCESS on parent SHA `331120b`: five GHCR package reads passed; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing passed; no drift, so apply/image replacement/rollout skipped. This run is expired and is not current-master authorization.
- Full K3s inspection #43127872524 generated at 00:31:21Z is expired at the 01:59:28Z reference (5,287s vs 4,500s). Its workload/runner state is historical only. Preserve debug PVC `k3s-debug/k3s-debug-logs`.
- Native schedule current-age and inter-arrival budgets fail for all six Platform/TCE lanes. Exact IDs, ages and gaps are recorded in the deployment tracker. Manual, workflow_run, repository_dispatch, push and rerun events do not count as native schedule delivery.
- TCE maintenance flag value is not currently verified. The last WF-13 log showed it empty before PR #1038 added an explicit warning; the PR did not mutate repository variables.
- Stock/Media GitOps ownership retirement is in force, but deletion remains blocked by external backup/retention, authoritative DNS, dedicated Media runner stop/disable/Listener absence/GitHub unregister and protected production approval. Storage-clean in-cluster evidence alone is insufficient.

### Workflow preservation and validation policy

App repositories own tests/builds, security workflows, immutable GHCR publication, source metadata, SBOM/provenance and release contracts. Platform Infra alone owns production manifests, shared pull credentials, image digest promotion, GitOps plan/apply, rollout and health verification. Preserve useful CI/test/security, backup, integration, manual, release and scheduled workflows. No workflow is confirmed redundant/obsolete. Do not add a competing SSH/Compose deployment authority.

Only first-attempt `event=schedule` runs on master count toward native cadence. Preserve all cron expressions and the TCE market-scan schedule. Do not weaken strict HTTP-200 health checks to hide intentional zero-replica maintenance.

Last reviewed: 2026-11-12 08:59 ICT (2026-11-12 01:59:28 UTC).


## Latest workflow inventory verification — 2026-11-12 06:14 ICT / 2026-11-11 23:14:06 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | 3ad8cc30535af6c627175b22070ee2ca3799d100 | #1658 current readiness refresh; #1314/#544/#541/#539 owner decisions | PR #1657 merged; exact-head validate-github-actions #43118015009 PASS and validate-manifests #43118014978 PASS; post-merge #43118124205 and #43118124229 PASS. Reconcile #43116379969 SUCCESS on parent SHA c0f309, no drift/no manifest apply. | Sole production manifests, shared GHCR pull credentials, provenance/digest promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | 5b425bdeab457e943bcecf1831836fc698e24394 | none | Native WF-06 #43073311537 FAIL; native WF-12 #43068077606 FAIL; manual WF-06 #43088897948 four 503s; WF-13 #43088861304 empty maintenance variable; WF-07 #43088811861 PASS. | Own tests/builds, immutable GHCR publishers, provenance and strict public health probes. No direct production apply. |
| StockDividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing VNSTOCK_API_KEY; desired tag 12d63b4 has no compatible platform manifest/RepoDigest. | Own tests/builds and immutable ARM64 publication only if retirement is reversed. |
| Media Generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 PASS; backend/frontend 1/1 with RepoDigests; dedicated runner service and Listener active. | Own tests/builds/immutable publication. Runner retirement needs stop/disable, Listener absence, GitHub unregister, backup/retention and DNS evidence. |
| Authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 owner-decision draft | CI #42654579277 PASS; Auth 0/0 maintenance; Platform verified runtime Secret with values suppressed. | Own Auth tests/builds/security/release provenance; Platform provisions runtime Secret and applies production state. |

### Recovery controller change merged

PR #1657 merged as 3ad8cc30535af6c627175b22070ee2ca3799d100. The recovery controller now retries only transient HTTP 500/502/503/504 during both reconciliation and inspection workflow-dispatch correlation GETs. Permanent 4xx/auth and malformed JSON remain fail-closed. Exact-head and post-merge action/manifest validation passed. The fix does not change cron, TCE market-scan schedule, dispatch scope or production authority.

### Native schedule and runtime evidence

At 23:14:06Z, all six native inter-arrival budgets fail; three current-age budgets fail. Platform inspection/recovery/watchdog current-age are within budget, but inter-arrival gaps remain above limits. Queue diagnostic reported no scheduled deployment lane above 15 minutes. TCE WF-06/WF-12 native runs remain stale; workflow_run/manual receipts are not native schedule evidence.

Fresh K3s inspection #43116036275 is 985s old (4,500s budget). Node Ready/ARM64, disk 56% (~20GiB free), ~19GiB RAM available; host restart required. Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend have ImagePullBackOff on 12d63b4. Preserve the Bound debug PVC. Media runner remains active; decommission gates are not met.

Preserve all useful CI/test/security/build/immutable-publisher/provenance/release/backup/integration/manual/scheduled workflows. No workflow was removed. Platform Infra remains the only production apply authority; no competing SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-11 22:02:56 UTC / 2026-11-12 05:02:56 ICT

This verification supersedes the prior 04:02 ICT compact inventory snapshot. Current master refs were read directly from GitHub refs; latest master-branch Actions runs and open PRs were inspected across all five repositories.

### Repository refs, PRs and workflow ownership

| Repository | Master SHA | Open PRs | App-owned workflows | Platform-owned workflows |
|---|---|---|---|---|
| Platform Infra | `f2ad42a5` | #1314/#544/#541/#539 (owner decisions) | Manifest validation, read-only inspection and repository automation | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s inspection, rollout and health verification |
| TCE Dashboard | `5b425bde` | none | Tests/builds, immutable GHCR publishers, strict WF-06 HTTP-200 probes, WF-12 native schedule watchdog, WF-13 maintenance-aware recovery, integration and backup | No direct production apply; authenticated release handoffs to Platform |
| StockDividend | `b1b5e177` | none | Tests/builds, native ARM64 immutable publisher, fail-closed scraper | No active production manifests; approved K3s decommission remains gated by fresh preflight and owner evidence |
| Media Generation | `dcd69869` | none | Tests/builds, immutable GHCR publisher and release workflow | No active production manifests; residual K3s workloads/runner require backup, DNS and local/remote runner retirement evidence |
| Authentication | `eab85fab` | #76 (owner-decision draft) | Auth CI/security, ARM64 immutable release publisher, provenance/SBOM and auth-image-published handoff | No direct production apply; Platform validates dispatch and owns GitOps promotion/reconcile |

### Latest workflow evidence

| Repository / workflow | Run | Event / result | Notes |
|---|---:|---|---|
| Platform validate-manifests | #43108386625 | push / IN_PROGRESS | Current master after PR #1653 merge; network-boundary validation step in progress at 22:02:56Z. |
| Platform PR #1653 validate-manifests | #43100250244 | pull_request / SUCCESS | Exact head `dae50fe614dcdf6432de1b1c616f3034a1146f6c`; 20/20 steps PASS. |
| Platform inspect-vps | #43089176130 | workflow_dispatch / SUCCESS | Full snapshot generated 19:39:15Z; expired at current reference. |
| Platform reconcile-vps | #43088879697 | workflow_dispatch / SUCCESS | Parent `9093831c`, apply/all/image changes false; 5 GHCR reads PASS, Auth Secret verified, shared pull Secret unchanged, no drift, apply/image replacement/rollout skipped; expired. |
| TCE WF-06 / WF-12 / WF-13 | #43088897948 / #43088836266 / #43088861304 | manual FAIL / workflow_run FAIL / workflow_run SUCCESS | WF-06 four 503s; WF-13 logged empty maintenance flag; none resets native schedule age. |
| TCE WF-07 | #43088811861 | schedule / SUCCESS | Third-party integration only. |
| Stock CI / scraper | #42610360402 / #42457182511 | push / SUCCESS; schedule / FAILURE | Scraper fail-closed on missing `VNSTOCK_API_KEY`. |
| Media CI | #42539512417 | push / SUCCESS | No current-master publication evidence. |
| Authentication CI | #42654579277 | push / SUCCESS | No current-master release evidence. |

### Native schedule and ownership acceptance

Only first-attempt `event=schedule` runs on master count toward cadence. Latest age/gap values at 22:02:56Z are recorded in the deployment tracker: all six age budgets and all six inter-arrival budgets fail. Do not count manual, push, pull_request, workflow_run, repository_dispatch or reruns as native delivery. Keep all cron expressions and TCE market-scan schedule unchanged.

App repositories own tests/builds, security workflows, immutable GHCR publication, provenance and source metadata. Platform Infra alone owns production manifests, shared pull credentials, digest/provenance validation, GitOps plan/apply, K3s rollout and health verification. Keep CI/test/security, backup, integration, manual, release and scheduled workflows; none is proven redundant/obsolete. Do not add competing SSH/Compose deployment authority.

Stock/Media GitOps ownership retirement is merged and decommission scope approved, but namespace deletion is still gated by fresh same-run storage preflight, backup/retention, authoritative DNS, local runner stop/disable/Listener absence, GitHub-side runner unregister and protected production approval. Preserve the separate debug PVC and all TCE/Auth/MicroFE/Keycloak resources.

PR #1653 is merged by squash after exact-head validation #43100250244 passed 20/20 steps. Current master validation #43108386625 is still in progress. Current-master GitOps plan and fresh K3s inspection are not evidenced. Workflow dispatch is not available through the current connector.

Last reviewed: 2026-11-12 04:02 ICT (2026-11-11 21:02:52 UTC).

This is the compact current workflow inventory; the 04:02 ICT verification above supersedes the prior 03:12 ICT snapshot. Historical append-only inventory is preserved at `docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md`; timestamped checkpoints remain under `docs/cross-repo-workflow-inventory-checkpoints/`. This review used read-only GitHub Actions REST run listings (first page per repository/query). Workflow dispatch is not exposed by the current connector. PR #1650 merged at `31b1245c`; PR #1651 merged at `7ff2da75`; PR #1652 merged at `99509adb`; current docs PR #1653 is open with latest exact-head validation #43095125265 queued.

## Latest workflow inventory verification — 2026-11-12 04:02 ICT / 2026-11-11 21:02:52 UTC

### Repository refs, open PRs and latest workflow evidence

| Repository | Master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `99509adb` | #1653 (documentation PR), #1314/#544/#541/#539 (owner decisions) | Master `validate-manifests` #43094091607 PASS. PR #1653 head `fb06a347`; exact-head #43095467009 queued since 20:20:41Z with no jobs. Older validations on previous PR commits do not satisfy exact-head merge requirements. |
| TCE Dashboard | `5b425bde` | none | Native WF-06 #43073311537 FAIL; native WF-12 #43068077606 FAIL; manual WF-06 #43088897948 returns four HTTP 503; WF-13 #43088861304 workflow_run success but maintenance variable logged empty; WF-07 #43088811861 schedule success is integration-only. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED (missing `VNSTOCK_API_KEY`); latest successful Build and Publish Images #41563856933 is 2026-11-03 and not a current-master publication. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; latest successful WF-03 publication #41158598649 is 2026-10-31 and not a current-master publication. |
| Authentication | `eab85fab` | #76 owner-decision draft | CI #42654579277 PASS; latest successful auth release #41040510320 is 2026-10-30 and not a current-master release. |

### Native schedule inventory — reference 21:02:52Z

| Lane | Latest qualifying native run | Previous | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile-vps.yml | #43066718643 | #42993779924 | 13,520 | 28,867 | 2,700 |
| Platform inspect-vps.yml | #43054529460 | #42981286761 | 17,947 | 30,159 | 4,500 |
| Platform recover-stale-ops.yml | #43058316157 | #42986496462 | 16,597 | 29,036 | 2,700 |
| Platform reconcile-schedule-watchdog | #43058640134 | #42986833403 | 16,476 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 11,046 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 13,027 | 28,287 | 1,500 |

All six native cadence lanes exceed both current-age and inter-arrival budgets. Count only first-attempt `event=schedule` runs on master. Manual, push, pull_request, workflow_run, repository_dispatch and rerun attempts are excluded. Keep existing TCE WF-06/WF-12/WF-13 contracts and all cron expressions; no market-scan schedule change.

### Runtime freshness, ownership and preservation

- Full K3s inspection #43089176130 (generated 19:39:15Z) is expired at this reference: age 5,017s vs 4,500s budget. Reconciliation #43088879697 (19:37:08Z, parent SHA `9093831c`) is expired: age 5,144s vs 2,700s budget. Both are historical evidence only.
- Historical reconciliation verified five GHCR package reads and Auth runtime Secret, left shared `ghcr-pull` unchanged, found no drift, and skipped apply/image replacement/rollout. No current-master plan or rollout is evidenced.
- Last-known Stock desired images fail ARM64 manifest resolution; Media workloads were 1/1 and the dedicated Media runner active/enabled with Listener present. Because the full snapshot is expired, do not assert these as current without a fresh inspection.
- Stock/Media GitOps ownership retirement and the guarded manual decommission workflow remain in force. The delete gate requires fresh same-run storage preflight, external backup/retention and authoritative DNS evidence, local runner service inactive/disabled, Listener absent, GitHub-side runner registration absent, exact attestations and protected production Environment approval. Do not delete shared Platform runner or the separate `k3s-debug` PVC.
- App repositories retain ownership of tests/builds, immutable GHCR publication and provenance. Platform Infra alone owns production manifests, shared pull credentials, digest promotion, GitOps plan/apply, rollout and health verification.
- Preserve CI, tests, security, backup, integration, manual, release and scheduled workflows. No workflow is confirmed redundant/obsolete. No duplicate direct SSH/Compose deployment authority.

### Current PR and merge gate

PR [#1653](https://github.com/phanthienquoc/platform-infra/pull/1653) remains open/mergeable on exact head `fb06a347831c5c814f3232a6c56b6694b6c73afc`. Latest exact-head validation #43095467009 is queued and has no jobs. Do not merge until that exact head receives a completed successful validation and the PR head is re-read immediately before squash merge.


## Previous inventory snapshot — 2026-11-12 03:12 ICT

### Repository refs, PRs and workflow ownership

| Repository | Master SHA | Open PRs | App-owned workflows | Platform-owned workflows |
|---|---|---|---|---|
| Platform Infra | `99509adb` | #1314/#544/#541/#539 (owner decisions), #1653 (docs) | Validation, inspection and repository automation only | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s inspection, rollout and health verification |
| TCE Dashboard | `5b425bde` | None | Tests/builds, immutable GHCR publishers, strict WF-06 HTTP-200 probes, WF-12 schedule watchdog, WF-13 maintenance-aware fallback, integration and backup | No direct production apply; authenticated release handoffs to Platform |
| StockDividend | `b1b5e177` | None | Tests/builds, native ARM64 immutable publisher, fail-closed scraper | No active production manifests; approved decommission scope remains, with residual `stock-prod` resources gated by backup/DNS evidence and protected namespace deletion |
| Media Generation | `dcd69869` | None | Tests/builds, immutable GHCR publisher and release workflow | No active production manifests; residual Media pods 1/1 and runner active. Decommission requires backup/retention, DNS ownership and remote runner unregister evidence |
| Authentication | `eab85fab` | #76 (owner decision) | Auth CI/security, ARM64 immutable release publisher, provenance/SBOM and auth-image-published handoff | No direct production apply; Platform validates dispatch and owns GitOps promotion/reconcile |

## Latest directly inspected workflow evidence

| Repository / workflow | Run | Event / result | Notes |
|---|---:|---|---|
| Platform validate-manifests | pending | queued | PR #1653 final exact-head validation; do not merge until completed PASS. |
| Platform validate-manifests | #43094091607 | push / SUCCESS | PR #1652 post-merge validation on master `99509adb`; all required validation steps PASS. |
| Platform validate-manifests | #43093772516 | push / SUCCESS | PR #1651 post-merge validation on master `7ff2da75`; all required validation steps PASS. |
| Platform validate-manifests | #43093109452 | push / SUCCESS | PR #1650 post-merge validation on master `31b1245c`; all required validation steps PASS. |
| Platform inspect-vps | #43089176130 | workflow_dispatch / SUCCESS | Fresh snapshot generated 19:39:15Z; inspection PR #1649 merged at `3e6d3f48`. |
| Platform validate-manifests | #43089441872 | workflow_dispatch / SUCCESS | Exact inspection PR head validation, 20/20 steps PASS; not a separate post-merge master run. |
| Platform reconcile-vps | #43088879697 | workflow_dispatch / SUCCESS | Parent `9093831c`, mode=apply, image changes false; five GHCR package preflight PASS; Auth Secret verified; shared `ghcr-pull` unchanged; no drift; apply/image replacement/rollout skipped. |
| Platform recover-stale-ops | #43089116141 | workflow_dispatch / SUCCESS | Manual recovery; not native schedule delivery. |
| Platform native reconcile / inspect / recovery / watchdog | #43066718643 / #43054529460 / #43058316157 / #43058640134 | schedule / SUCCESS / SUCCESS / SUCCESS / FAILURE | Latest qualifying native first-attempt runs; all outside their current freshness budgets. |
| TCE WF-06 | #43088897948 | workflow_dispatch / FAILURE | Four public endpoints returned 503 instead of 200. |
| TCE WF-12 | #43088836266 | workflow_run / FAILURE | Native WF-06 schedule freshness failed; heartbeat dispatch succeeded. |
| TCE WF-13 | #43088861304 | workflow_run / SUCCESS | Job log shows `TCE_MAINTENANCE_MODE` empty; code maps empty to `enabled=false`, then dispatched fallback #43088897948. Not native schedule evidence. |
| TCE WF-07 integration | #43088811861 | schedule / SUCCESS | Integration check only; not WF-06/WF-12 health evidence. |
| Stock CI / scraper | #42610360402 / #42457182511 | push / SUCCESS; schedule / FAILURE | Scraper fails closed on missing `VNSTOCK_API_KEY`. |
| Media CI | #42539512417 | push / SUCCESS | Application tests/build passed; no new image publication. |
| Authentication CI | #42654579277 | push / SUCCESS | Validation and ARM64 image build passed. |

## Native schedule inventory and acceptance

Only first-attempt `event=schedule` runs on `master` count. Manual, push, pull_request, workflow_run, repository_dispatch and reruns are not native schedule substitutes.

| Lane | Latest native run | Previous native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile-vps.yml | #43066718643 | #42993779924 | 10,411 | 28,867 | 2,700 |
| Platform inspect-vps.yml | #43054529460 | #42981286761 | 14,104 | 30,159 | 4,500 |
| Platform recover-stale-ops.yml | #43058316157 | #42986496462 | 13,488 | 29,036 | 2,700 |
| Platform reconcile-schedule-watchdog | #43058640134 | #42986833403 | 13,367 | 29,006 | 2,700 |
| TCE WF-06 | #43073311537 | #42949191917 | 7,937 | 54,245 | 1,500 |
| TCE WF-12 | #43068077606 | #42996293386 | 9,918 | 28,287 | 1,500 |

All six current-age and all six inter-arrival budgets fail at 19:58:49Z. WF-06 manual #43088897948 does not count as schedule delivery. WF-12's latest log reports WF-06 source #43073311537 at 98m age and queue=0m; the observed failure is stale schedule delivery, not proven runner congestion. Preserve all cron expressions and TCE market-scan schedule.

## Source-level immutable publisher and dispatch contract audit — 2026-11-11

- TCE `.github/workflows/wf-03-tce-production-deploy.yml`: manual release dispatch, full 40-character source SHA, refuse existing immutable tags, inspect registry manifests for `linux/arm64`, require valid SHA-256 web/service digests, validate exact repository-dispatch schema and wait for the Platform handoff run.
- TCE `.github/workflows/wf-08b-tce-microfe-build-publish.yml`: `packages: write` is job-scoped to publisher jobs; Shell/WS builds target `linux/arm64` with provenance/SBOM; digests are validated; exact payload schema is checked before dispatch and the Platform promotion run is verified.
- Stock `.github/workflows/deploy.yml`: manual production image publication is explicitly disabled; master-push artifact publication uses job-scoped package write, refuses tag overwrite, builds backend/admin/frontend for `linux/arm64`, verifies full-SHA and version+SHA tags resolve to the same valid registry digest. No Platform handoff is sent, consistent with the approved decommission scope and absence of active Stock production manifests.
- Media `.github/workflows/wf-03-media-production-deploy.yml`: full source SHA, immutable-tag preflight, ARM64 manifest and digest verification; explicitly no Platform deployment/dispatch is configured.
- Authentication `.github/workflows/release.yml`: manual release from master only, immutable full-SHA tags, ARM64 build with provenance/SBOM, digest equality across tags, exact Auth dispatch schema and required Platform dispatch token.
- Platform exact-head and post-merge validation for PR #1650 (#43092982966 and #43093109452) passed immutable image-change and exact Auth/TCE dispatch-payload contract tests. No image was published or promoted during this audit.

## Deployment contract and preservation rules

- App repositories own application code, dependencies, tests/builds, Dockerfiles, immutable GHCR publication and source provenance. Use full source SHA tags and verify registry digest/ARM64 descriptors before handoff.
- Platform Infra alone owns production Kustomize manifests, shared GHCR pull credentials, authenticated dispatch validation, provenance/digest promotion, GitOps plan/apply, rollout and live health.
- `reconcile-vps.yml` manual dispatch defaults to `mode=plan`; explicit manual apply and existing schedule/push/authenticated promotion events retain their documented behavior. `inspect-vps.yml` remains read-only.
- Keep Stock/Media out of active Platform production manifests while preserving app CI/publish workflows. The decommission scope is approved; delete only through the protected manual workflow after same-run storage preflight, external backup/retention and authoritative DNS evidence, Media runner stop/disable/unregister plus read-only GitHub runner audit, and production Environment approval. Do not confuse cached/local image IDs with registry RepoDigests.
- Preserve useful CI, test, security, backup, integration, release, manual and scheduled workflows. No workflow is confirmed redundant/obsolete in this checkpoint.
- No duplicate direct SSH/Compose deployment authority. No change to TCE market-scan schedule.

## Stock/Media decommission workflow

- Workflow: `.github/workflows/decommission-stock-media.yml`; `workflow_dispatch` only; default `mode=plan`.
- Plan mode verifies Platform runner policy v15, reports the dedicated Media systemd unit/enablement/Listener state, and runs the read-only namespace/storage/Ingress inventory. It does not stop or unregister a runner or delete resources.
- Delete mode uses the protected `production` Environment and requires exact confirmations `DELETE-STOCK-PROD-AND-MEDIA-PROD`, `BACKUP-AND-EXTERNAL-DATA-REVIEWED`, `AUTHORITATIVE-DNS-OWNERSHIP-REVIEWED`, and `MEDIA-RUNNER-DISABLED-STOPPED-AND-UNREGISTERED`, plus stable HTTPS backup/DNS evidence references.
- Before deleting, it verifies the Media service is inactive and disabled/masked or absent, no Listener process exists, and the GitHub Media repository runner list has no `media-generation-k3s-01` entry via read-only `MEDIA_RUNNER_AUDIT_TOKEN`; it repeats the storage preflight in the same run and deletes only `stock-prod` and `media-prod`.
- Current inspection #43089176130 shows target namespaces storage-clean but the Media runner service is active/enabled and Listener present. No delete run is authorized by the current evidence or executed. Preserve the shared Platform runner, TCE/Auth/MicroFE/Keycloak and all app CI/publisher workflows.

## Governance evidence

- Direct `GET /branches/master` returned `protected=false` for all five repositories. Branch-protection detail GET returned HTTP 403 for all five. `GET /rulesets?includes_parents=true` returned an empty array for Platform Infra, TCE Dashboard, Media Generation and Authentication; StockDividend returned HTTP 403 because GitHub rulesets require Pro or a public repository, so its inherited rulesets remain unverified. Repository metadata allows squash, merge commit and rebase on all five. This confirms all five master branches are unprotected at the branch API level; the administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.

## Current safety state

- No new app image publication or digest promotion.
- No new GitOps dispatch/plan/apply on current master; latest successful apply-mode reconciliation was on parent `9093831c` before the inspection-only PR #1649 changed only `debug/vps-latest.md`.
- No manifest apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot.
- Historical reconciliation provisioned/verified Auth runtime Secret with values suppressed; shared `ghcr-pull` was unchanged.
- Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.

## Historical verification — 2026-11-11 15:09 ICT / 08:09:56 UTC

- Direct master refs: Platform `48c9cf344c40fb76b1c720149d67bbced29e9255`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Authentication #76, all draft/owner decisions; none in TCE/Stock/Media. Last exact-head validation runs remain PASS for the unchanged heads; Auth Supabase Preview is skipped.
- Platform native inspection #42981286761 succeeded and generated inspection PR #1620, merged at current master #48c9cf34. Manual reconciliation #42981589486 succeeded: GHCR read preflight passed for five managed packages; Auth runtime Secret provision/verification passed with values suppressed; shared `ghcr-pull` unchanged; TCE desired/live release pairing passed; drift=false; manifest apply and image replacement skipped. TCE/Auth zero replicas are intentional maintenance, not healthy. Recovery #42981775331 succeeded without duplicate fallback dispatch. Watchdog #42981569803 failed on stale native cadence; no scheduled runner queue exceeded 15 minutes in its sample.
- TCE native WF-06 #42949191917 and WF-12 #42944415193 remain failed/stale. Manual WF-06 #42972014911 confirms four strict endpoints returned 503 instead of 200. WF-07 integration schedule #42971954835 passed but does not replace health lanes. Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Native cadence reference 08:09:56Z: Platform reconcile #42942147668 age 22,596s/gap 14,244s; inspection #42981286761 age 1,730s/gap 25,617s; recovery #42939222343 age 24,079s/gap 13,889s; watchdog #42940581820 age 23,403s/gap 13,950s; TCE WF-06 #42949191917 age 18,915s/gap 12,853s; TCE WF-12 #42944415193 age 21,441s/gap 13,126s. All six inter-arrival budgets fail; five of six current-age budgets fail. Keep all cron expressions and the TCE market-scan schedule unchanged.
- Fresh read-only K3s snapshot #42981286761 generated at 07:41:14Z and is 1,722s old at reference (within 4,500s). Node Ready/ARM64; K3s v1.36.3+k3s1; disk 56% / ~20 GiB free; ~19 GiB RAM available; host restart required. Media and MicroFE core pods 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1. Media runner service/listener active; retirement evidence incomplete.
- No new app image publication or digest promotion. No GitOps drift, manifest apply, image replacement or workload rollout in reconciliation #42981589486. Shared pull Secret unchanged; Auth runtime Secret provision/verification succeeded. No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot.
- Preserve CI/test/security, app-owned immutable publishers, release, backup, integration, manual and scheduled workflows. No workflow confirmed obsolete. No direct SSH/Compose authority. Platform remains the only production apply authority.

## Post-merge verification — 2026-11-11 15:18 ICT

- Platform master advanced documentation-only to `9c2e4e0efb54aad29bcdb82afeaf06c187c60499` through PR #1621.
- Exact-head validation #42985848211 and post-merge master validation #42985958377 both PASS.
- Only `validate-manifests` ran after the docs-only merge; no production reconcile/recovery push run was triggered.
- The 15:09 ICT workflow checkpoint remains the latest operational snapshot; this addendum updates only the Platform master SHA and merge receipt.
- Workflow ownership and production authority boundaries are unchanged; no workflow was removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.

## Post-merge verification — 2026-11-11 15:20 ICT

- Platform master advanced documentation-only to `8f95ddd8729eae6fee662e3a395f083be4fc21b0` through PR #1622.
- Exact-head validation #42986144723 and post-merge master validation #42986252700 both PASS.
- Only `validate-manifests` ran after the docs-only merge; no production reconcile/recovery push was triggered.
- The 15:09 ICT operational checkpoint remains the latest runtime/schedule evidence.
- Workflow ownership and production authority boundaries are unchanged; no workflow was removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.

## Historical verification — 2026-11-11 15:25 ICT / 08:25:10 UTC

- Platform master: `c811ed79f22505c074eaa9b08b0e8a61e59db08a`; TCE: `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media: `dcd698699c65ba6e73f6b43838975144777131c3`; Auth: `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform PR #1623 exact-head #42986594992 and post-merge #42986698420 PASS. Current open owner-decision PRs: Platform #1314/#544/#541/#539 and Auth #76; no TCE/Stock/Media PRs.
- Platform native inspection #42981286761 PASS; native recovery #42986496462 PASS; native watchdog #42986833403 FAIL on stale cadence. Manual reconciliation #42986517013 PASS: GHCR preflight, Auth Secret verification, shared pull Secret unchanged, no drift, no manifest apply/image replacement. Recovery #42986712253 PASS with no duplicate fallback dispatch.
- TCE native WF-06 #42949191917 and WF-12 #42944415193 remain stale/failed; manual WF-06 #42972014911 returned HTTP 503 on all four strict probes. TCE/Auth are intentional 0/0 maintenance. Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Native schedule reference 08:25:10Z: reconcile #42942147668 age 23,510s/gap 14,244s; inspection #42981286761 age 2,644s/gap 25,617s; recovery #42986496462 age 171s/gap 24,822s; watchdog #42986833403 age 20s/gap 24,297s; TCE WF-06 #42949191917 age 19,829s/gap 12,853s; TCE WF-12 #42944415193 age 22,355s/gap 13,126s. All six inter-arrival gaps fail; three current-age budgets fail. Preserve cron and TCE market-scan schedule.
- Fresh K3s snapshot #42981286761 age 2,636s / 4,500s. Node Ready/ARM64; disk 56% / ~20 GiB free; ~19 GiB RAM; restart required. Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1. Media runner active; retirement evidence incomplete.
- App repos retain CI/build/immutable publication ownership; Platform remains sole production apply authority. No image publication, digest promotion, manifest apply, workload rollout, destructive retirement, credential rotation, host reboot or DNS/database/storage mutation. Auth runtime Secret provision/verification succeeded; shared `ghcr-pull` unchanged. No workflow removed or SSH/Compose authority added.

## Ownership and production authority

| Repository | Owns | Must not own |
|---|---|---|
| TCE-dashboard | App CI, tests, build verification, immutable TCE/MicroFE GHCR publication, public app health probes and app-specific backup/integration checks | Production manifests, shared pull credentials, production GitOps apply, K3s rollout or direct SSH/Compose deployment |
| StockDividend | App CI, tests, native ARM64 immutable image publication, scraper and safe credential preflight | Platform manifests, shared GHCR credentials, direct Kubernetes/SSH/Compose production deployment |
| Media Generation | App CI, tests and immutable image publication | Platform manifests, shared pull credentials, direct production deployment |
| phanthienquoc-authentication | Auth CI, tests, release/provenance and immutable app publication | Shared pull credentials, production manifests, direct production apply |
| platform-infra | Production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout, runtime inspection and health verification | App source tests/builds or app-owned image publication |

Platform reconcile-vps.yml is the single production apply authority. Platform inspect-vps.yml is read-only. Manual reconcile dispatch has no image-change override; only the provenance-verified gitops-promoted-ready repository_dispatch may bypass the image guard after the originating promotion run and required jobs are verified. Do not add competing SSH/Compose deployment authorities in app repositories.

## Platform Infra workflow files on master

| Workflow file | Responsibility / preservation |
|---|---|
| bootstrap-runner.yml | Allowlisted self-hosted runner bootstrap and scoped operational policy |
| configure-keycloak-no-email-registration.yml | Keycloak configuration utility |
| configure-keycloak-resend-smtp.yml | Transactional email configuration utility |
| decommission-stock-media.yml | Guarded decommission workflow; retain approval and evidence gates |
| gitops-image-promotion.yml | Verify app source-run provenance and promote approved immutable digests |
| inspect-vps.yml | Read-only K3s/VPS inspection; never production apply |
| keycloak-auth-production-smoke.yml | Keycloak/Auth production smoke utility |
| keycloak-ci.yml | Keycloak CI |
| provision-auth-runtime-secret.yml | Scoped Auth runtime Secret provisioning and verification |
| provision-keycloak-tce-client.yml | Keycloak TCE client provisioning |
| reconcile-observability.yml | Observability reconciliation |
| reconcile-schedule-watchdog.yml | Read-only native schedule freshness watchdog |
| reconcile-vps.yml | Sole production manifest reconciliation/apply authority; image-change bypass only for provenance-verified gitops-promoted-ready dispatch; recursive Keycloak Markdown excluded from push trigger; resolver-only edits do not auto-apply |
| recover-stale-ops.yml | Scheduled and receipt-backed recovery controller; recursive Keycloak operator Markdown excluded from push recovery |
| runtime-secret-readiness.yml | Runtime Secret readiness validation |
| smoke-production.yml | Production smoke checks |
| sso-auto-onboarding.yml | SSO onboarding utility |
| staging-dry-run.yml | Staging dry-run |
| validate-github-actions.yml | Workflow, payload and contract validation |
| validate-manifests.yml | Production manifest and deployment contract validation |
| validate-metrics.yml | Metrics validation |
| validate-recovery-readiness.yml | Recovery readiness contract |
| validate-tce-vps-control-mcp.yml | TCE VPS control MCP contract |
| verify-keycloak-tce-client.yml | Keycloak client verification |
| vps-image-cleanup.yml | Guarded image cleanup utility |
| vps-manual-operations.yml | Allowlisted manual operations |

## TCE Dashboard workflow files on master

| Workflow file | Responsibility / preservation |
|---|---|
| wf-01-tce-build-verify.yml | TCE build verification |
| wf-01p-tce-web-pr-build.yml | PR-scoped web build |
| wf-02-tce-backend-unit-test.yml | Backend unit tests |
| wf-02-tce-prettier-format.yml | Formatting validation |
| wf-03-tce-production-deploy.yml | App-owned, gated immutable production publisher |
| wf-06-tce-healthcheck.yml | Strict public HTTP 200 health checks; preserve the four approved endpoints |
| wf-07-tce-backup.yml | Scheduled backup; preserve |
| wf-07-tce-integration-check.yml | Scheduled integration check |
| wf-08b-tce-microfe-build-publish.yml | App-owned MicroFE image build/publication |
| wf-09-nginx-readonly-audit.yml | Read-only Nginx audit utility |
| wf-09-tce-vps-safe-setup.yml | Manual safe setup utility; not production apply authority |
| wf-10-tce-k3s-bootstrap.yml | Staging/bootstrap utility; keep separately gated |
| wf-11-tce-mobile-landscape-viewport.yml | UI/viewport validation |
| wf-12-tce-healthcheck-schedule-watchdog.yml | Native schedule freshness watchdog and heartbeat |
| wf-13-tce-healthcheck-recovery.yml | Healthcheck recovery utility |

## StockDividend workflow files on master

- `ci.yml` — app CI/tests, including non-publishing native ARM64 builds for scraper/admin/backend.
- `deploy.yml` — app-owned, gated native ARM64 immutable image publisher. Code review confirms the workflow requires a native `ubuntu-24.04-arm` runner, publishes scraper/admin/backend with full-source-SHA and `prod-v<semver>-<sha>` tags, verifies `linux/arm64` descriptors and digest equality for both tags, and refuses existing immutable tags. Manual publication requires `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`. The workflow does not dispatch to Platform; approved digests are handed off separately. No publication was run in this checkpoint.
- `run_scraper.yml` — weekend scraper with fail-closed `VNSTOCK_API_KEY` preflight and side-effect-free `preflight_only=true` path.

## Media Generation workflow files on master

- ci.yml — app CI/tests.
- wf-03-media-production-deploy.yml — app-owned immutable image publication and Platform promotion handoff; production promotion remains token/owner gated.

## Authentication workflow files on master

- ci.yml — service CI/tests.
- release.yml — app-owned release and immutable publication/provenance.
- web-ci.yml — web CI/tests.

## Native schedule contracts

Only first-attempt event=schedule runs on master count for cadence acceptance. Push, pull_request, workflow_run, workflow_dispatch and repository_dispatch are not native schedule substitutes.

| Workflow | Current cron | Existing age/gap budget |
|---|---|---:|
| Platform reconcile-vps.yml | 7,22,37,52 * * * * | 2700s |
| Platform inspect-vps.yml | 2,32 * * * * | 4500s |
| Platform recover-stale-ops.yml | 10,25,40,55 * * * * | 2700s |
| Platform reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | 2700s |
| TCE wf-06-tce-healthcheck.yml | */15 * * * * | 1500s |
| TCE wf-12-tce-healthcheck-schedule-watchdog.yml | 7,22,37,52 * * * * | 1500s |

Current native evidence and exact age/gap values are in docs/cross-repo-deployment-tracker.md. Do not change cron, freshness budgets or TCE market-scan scheduling to hide delivery gaps.

## Publication and GitOps contract

1. App repository builds/tests and publishes immutable full-source-SHA plus version/source-SHA tags.
2. Publisher verifies architecture descriptors and registry-resolved digest equality before dispatch.
3. Platform verifies source workflow path, source SHA, run ID, attempt, release tag and image digests; it does not trust mutable tags or caller-supplied payloads alone.
4. Only the `gitops-promoted-ready` repository_dispatch may authorize workload image replacement, and only after Platform validates the originating promotion run, required job results, release identity, source commit and digest-pinned image references. Manual `reconcile-vps.yml` dispatch exposes no image-change override.
5. Manual, scheduled and push-triggered reconciliation remain subject to `guard-reconcile-images.sh`; non-image manifest changes can still be applied through the single Platform apply authority.
6. Platform validates digest references, reconciles production manifests and verifies rollout/health only with fresh runtime evidence.
7. Shared `ghcr-pull` credentials are Platform-owned; app workflows must not rotate or mutate them.
8. Repository-level pre-push tag-absence guards and digest checks do not prove GHCR server-side immutable-tag policy. Registry-side enforcement remains unverified.

## Preservation decisions

- Keep all CI, test, security, formatting, release, backup, integration, manual and scheduled workflows listed above.
- No workflow is confirmed redundant or obsolete in this review.
- Do not merge owner-decision drafts or trigger a production publisher merely to make the inventory appear complete.
- Do not add duplicate direct SSH/Compose deployment authorities.
- Do not change the TCE market-scan schedule.

## Historical verification — 2026-11-11 07:02 ICT / 00:02:43 UTC

- Master refs at the 00:02:43Z snapshot, read directly from Git refs: Platform `ad54469d6cf0d2c3362d6105f50fa9131dadf8a5`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. All remain drafts/owner decisions. Exact-head `validate` checks pass on all five; Authentication Supabase Preview is skipped. No open PRs in TCE, Stock or Media.
- PR #1601 merged at `72ed11ef`, removing manual `allow_image_changes`. PR #1602 merged at `8b11d662`, adding read-only inspection evidence. PR #1603 merged at `98bc3d8c`, excluding Keycloak Markdown from reconcile/recovery push scope and making resolver-only edits fail closed. PR #1604 merged at `ad54469d`, refreshing readiness docs. Exact-head and post-merge checks for #1603 and #1604 passed; latest post-merge manifest validation is #42921972012 PASS.
- Historical push run #42920184478 (event=push, created 23:04:13Z, completed 23:04:57Z) misclassified `platform/keycloak/README.md`, applied the Keycloak resource set and executed the narrow Auth/Keycloak scale-to-zero action. No pre-scale replica snapshot exists, so the exact state transition is unknown. PR #1603 added path exclusions and resolver-only fail-closed regression coverage. No reconcile/recovery push run was created by the #1603/#1604 merges.
- Latest Platform recovery receipt #42922588369 (event=repository_dispatch, 23:20:48Z) verified TCE WF-06 heartbeat #42922537816. Reconcile fallback was skipped because the last reconcile activity #42920184478 was 15 minutes old at recovery time. The recovery controller found the existing read-only inspection fallback #42920320410 still fresh (age 13 minutes at that run), so no additional inspection was dispatched. This is not a native schedule delivery or a new reconciliation.
- Current native schedule evidence at 00:02:43Z (only first-attempt event=schedule on master counts): Platform reconcile #42909757881 age 7607s / gap 19941s; inspection #42887151366 age 15905s / gap 28677s; recovery #42906791198 age 8735s / gap 20656s; watchdog #42908417737 age 8120s / gap 20852s; TCE WF-06 #42922537816 age 2535s / gap 18739s; TCE WF-12 #42915709227 age 5334s / gap 17617s. All six age and gap budgets fail. TCE WF-06 failed strict HTTP 200 checks; WF-12 failed freshness. Separate TCE WF-07 backup #42924677977 succeeded at 23:35:49Z but does not replace either health lane.
- Current cron expressions were re-read from the actual workflow files: Platform reconcile `7,22,37,52 * * * *`; inspection `2,32 * * * *`; recovery `10,25,40,55 * * * *`; watchdog `12,27,42,57 * * * *`; TCE WF-06 `*/15 * * * *`; TCE WF-12 `7,22,37,52 * * * *`. Keycloak recursive Markdown exclusions remain in reconcile/recovery push filters. No cron or market-scan schedule changed.
- Fresh read-only inspection #42920320410 generated `debug/vps-latest.md` at 23:05:16Z; age 3447s at this reference, within the 4500s budget. Host ARM64 Ubuntu 22.04.5, uptime 193 days, 19 GiB RAM available, root disk 56% used / 20 GiB free, `restart_required=yes`; K3s node Ready, v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Workloads in that snapshot: Media backend/frontend 1/1 with registry-resolved digest evidence; MicroFE Shell/WS/NATS 1/1; TCE frontend/service 0/0; Auth/Keycloak 0/0; OIDC discovery HTTP 503. Stock Admin has two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod on `12d63b4` (no ARM64 platform match); legacy Backend/Frontend 1/1 on `23b2878`, but no RepoDigest evidence for promotion.
- Storage preflight reports no Stock/Media PVC or VolumeSnapshot references; `k3s-debug/k3s-debug-logs` remains bound. Media runner service/listener active/enabled; remote runner unregister, backup/retention and authoritative DNS ownership remain unverified.
- Latest reconcile run #42920184478 is now 3466s old; manual reconciliation #42915749236 is 5318s old. Prior manual reconciliation verified GHCR read access, Auth runtime Secret (values suppressed), unchanged shared `ghcr-pull`, clean GitOps drift and skipped apply/image replacement/rollout. Recovery #42922588369 is a repository_dispatch receipt, not a native scheduled reconciliation.
- TCE native WF-06 #42922537816 failed all four public endpoint jobs; Auth readiness log observed HTTP 503 versus required HTTP 200. WF-12 #42915709227 failed because native WF-06 evidence is stale. TCE backend tests previously passed. Stock CI #42610360402 passed; scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was absent. Media CI #42539512417 and Auth CI #42654579277 passed.
- Branch-protection detail GET returned 403 for all five repositories. Rulesets GET returned `[]` for four public repositories; private Stock rulesets GET returned 403 with a plan limitation. Effective inherited rulesets remain unverified; administrator confirmation is required.
- GHCR server-side immutable-tag enforcement remains unverified. Pre-push tag-absence guards and digest equality do not prove registry-side enforcement.
- No new image publication, digest promotion, production apply, rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred in this checkpoint.
- Preserve all useful CI/test/security, formatting, release, backup, integration, manual and scheduled workflows. No workflow is confirmed redundant or obsolete. Do not add direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Retired Stock/Media GitOps and K3s status — 2026-11-11 07:56 ICT

- StockDividend and Media Generation remain application repositories for CI/tests and their own gated image publishers, but their production manifest trees and image/namespace references have been removed from the active Platform GitOps scope. The current tree has no `apps/stockdividend` or `apps/media-generation` manifest tree; `scripts/verify-retired-production-manifests.sh` fails if those trees or Stock/Media references reappear under `environments/prod`, `platform` or `apps`.
- Keep `.github/workflows/decommission-stock-media.yml` and its helper/test scripts. This is the sole guarded namespace retirement path, not an application deployment workflow. Its plan mode is read-only. Delete mode requires the production environment, exact typed confirmations, stable HTTPS backup and DNS evidence references, local Media runner stopped/disabled with no listener, authoritative GitHub runner registration absence verified using the scoped audit token, and a fresh namespace/PV/PVC/VolumeSnapshot preflight.
- Inspection #42932368784 generated the latest read-only snapshot at 00:34:17Z. The embedded Stock/Media storage preflight returned `storage-clean`: no PVC, PV claim or VolumeSnapshot/VolumeSnapshotContent references in `stock-prod` or `media-prod`. Both namespaces remain Active and workloads remain present. The separate `k3s-debug/k3s-debug-logs` PVC is Bound and must be preserved.
- The Media runner service is active/enabled and its listener process is present. GitHub runner registration is not inferred from host inspection. External DB/object-storage backup/retention and authoritative DNS/provider ownership are still unverified. The explicit decommission workflow plan mode has not been dispatched; the inspection ran the underlying read-only namespace/storage preflight.
- No delete-mode execution, namespace/PVC/PV deletion, runner stop/disable/unregister, external-data mutation, DNS change, credential rotation or host restart occurred. Do not publish/promote Stock or Media production images while the approved retirement is pending.
- Preserve TCE/Auth workloads and TCE market-scan schedule. The decommission workflow must remain narrowly scoped to `stock-prod` and `media-prod`.

## Historical verification — 2026-11-11 07:56 ICT / 00:56:58 UTC

- Direct Git refs: Platform `0faec01a5ad0f7c7349a1dd9d22750e80d32756f`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. Exact-head validation runs #42161859747, #38575430454, #38567431761, #38548718033 and #41329425940 all completed successfully. All remain drafts/owner decisions. No open PRs in TCE, Stock or Media.
- Platform PR #1607 was generated by native scheduled inspection #42932368784 and squash-merged at `0faec01a`; only `debug/vps-latest.md` changed. Exact-head validation was part of the inspection workflow; no post-merge manifest validation was triggered because deployment files did not change.
- Manual reconcile #42932691349 succeeded with GHCR read preflight, Auth runtime Secret verified (values suppressed), shared `ghcr-pull` unchanged, managed MicroFE/TCE pull checks clean, TCE release pairing passed and GitOps drift=false. Manifest apply, image replacement and rollout were skipped. Stock ImagePullBackOff pods remained; Stock is outside the managed pull helper and is in the approved retirement scope.
- Recovery #42932880278 succeeded as workflow_dispatch for source reconcile #42932691349. It verified the source completion and found the reconciliation and native inspection recent; no fallback reconcile or inspection was dispatched. This is not native schedule delivery.
- Latest native schedule metrics at 00:56:58Z: Platform reconcile #42909757881 age 10862s/gap 19941s; inspection #42932368784 age 1369s/gap 17791s; recovery #42906791198 age 11990s/gap 20656s; watchdog #42908417737 age 11375s/gap 20852s; TCE WF-06 #42922537816 age 5790s/gap 18739s; TCE WF-12 #42915709227 age 8589s/gap 17617s. All six inter-arrival gaps fail; five current-age budgets fail. Manual and workflow_run fallbacks are not counted.
- Current inspection: K3s node Ready (ARM64, v1.36.3+k3s1, containerd 2.3.2-k3s2), disk 56% / 20 GiB free, RAM 19 GiB available, restart required. Media and MicroFE core pods 1/1; TCE/Auth/Keycloak 0/0 maintenance; public OIDC both realms HTTP 503. Stock Admin (two pods) and desired Backend (one pod) ImagePullBackOff on `12d63b4` due no ARM64 platform match; legacy Backend/Frontend remain running but cached tags have no RepoDigest.
- TCE native WF-06 #42922537816 failed all four strict HTTP 200 endpoint checks; WF-12 #42915709227 failed freshness. Stock CI #42610360402 passed; scraper #42457182511 failed closed due missing `VNSTOCK_API_KEY`. Media CI #42539512417 and Auth CI #42654579277 passed.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred.
- Preserve all CI/test/security, formatting, release, backup, integration, manual and scheduled workflows. No workflow is confirmed redundant or obsolete. Do not add direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Historical verification — 2026-11-11 08:05 ICT / 01:05:25 UTC

- Direct master refs: Platform 010558ada7c36738a287ed38ae107d260f63ebf9; TCE c4602be3b0a7b624bdb9cd41519cfc70a14d92ab; Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61; Media dcd698699c65ba6e73f6b43838975144777131c3; Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f.
- PR #1608 refreshed the deployment tracker/inventory and Stock/Media retirement evidence, merging at Platform master 010558ada7c36738a287ed38ae107d260f63ebf9. Latest Platform master run #42935987763 (validate-manifests, push) completed SUCCESS at 01:02:54Z. No production reconcile/recovery push run followed the docs-only merge.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. Exact-head checks: #1314 #42161859747 PASS; #544 #38575430454 PASS; #541 #38567431761 PASS; #539 #38548718033 PASS; Auth #76 #41329425940 validate PASS, Supabase Preview skipped. All remain drafts/owner decisions. No open PRs in TCE, Stock or Media.
- Latest workflow evidence: TCE native WF-06 #42922537816 and manual WF-06 #42922596353 both failed all four public endpoint checks (503 vs 200); native WF-12 #42915709227 failed freshness; WF-07 backup #42924677977 succeeded but is not a health substitute. Stock CI #42610360402 passed; scraper #42457182511 failed closed on absent VNSTOCK_API_KEY. Media CI #42539512417 and Auth CI #42654579277 passed.
- Native schedule reference: 01:05:25Z. Platform reconcile #42909757881 age 11369s/gap 19941s; inspection #42932368784 age 1876s/gap 17791s; recovery #42906791198 age 12497s/gap 20656s; watchdog #42908417737 age 11882s/gap 20852s; TCE WF-06 #42922537816 age 6297s/gap 18739s; TCE WF-12 #42915709227 age 9096s/gap 17617s. All six inter-arrival gaps fail; five current-age budgets fail. Only first-attempt event=schedule on master counts. Manual and workflow_run fallbacks do not substitute.
- Cron expressions remain unchanged: Platform reconcile 7,22,37,52 * * * *; inspection 2,32 * * * *; recovery 10,25,40,55 * * * *; watchdog 12,27,42,57 * * * *; TCE WF-06 */15 * * * *; TCE WF-12 7,22,37,52 * * * *. TCE market-scan schedule unchanged.
- Freshest full K3s inspection #42932368784 generated debug/vps-latest.md at 00:34:17Z, age 1,868s at this reference and still within the 4,500s budget. Node Ready (ARM64, K3s v1.36.3+k3s1), disk 56% / ~20 GiB free, ~19 GiB RAM available, host restart required. Media backend/frontend and MicroFE core 1/1; TCE/Auth/Keycloak 0/0 maintenance; OIDC discovery 503; Stock Admin (two pods) and desired Backend ImagePullBackOff on 12d63b4 due missing ARM64 platform descriptor. No reboot or workload mutation.
- Stock/Media production manifests remain retired from active Platform GitOps. Both namespaces/workloads remain present pending the guarded decommission. Storage preflight from inspection found no target PVC/PV/VolumeSnapshot references; preserve the separate Bound k3s-debug/k3s-debug-logs PVC. Dedicated Media runner service/listener remains active/enabled; remote unregister, external backup/retention and authoritative DNS ownership remain unverified. Delete mode remains blocked.
- GHCR read access and Auth runtime Secret were verified by manual reconciliation #42932691349; shared ghcr-pull unchanged; GitOps drift clean; apply/image replacement/rollout skipped. Recovery receipt #42932880278 reused fresh existing inspection and did not dispatch a new inspection or reconciliation.
- No new image publication, digest promotion, production apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation or host restart occurred in this checkpoint. Preserve CI/test/security/release/backup/integration/manual/scheduled workflows; no workflow confirmed obsolete; no duplicate SSH/Compose authority.


## Historical verification — 2026-11-11 09:02 ICT / 02:02:00 UTC

- Direct master refs: Platform `fbb479fc7e6415eeec8ef34fdaccf039f5477e17`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314, #544, #541, #539; Authentication #76. No open PRs in TCE, Stock or Media. All listed PRs remain drafts/owner decisions; exact-head `validate` checks pass; Auth Supabase Preview is skipped.
- Platform PR #1610 is the latest inspection-only merge at `fbb479fc`. Source inspection #42942360712 and exact-head validation #42942563353 passed. It only updated `debug/vps-latest.md`; no post-merge master validation run was observed for this debug-only change.
- Latest app CI evidence: TCE backend CI previously passed, but native WF-06 #42922537816 failed four strict public HTTP 200 probes with 503 and WF-12 #42915709227 failed freshness. Stock CI #42610360402 passed; scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is empty. Media CI #42539512417 and Auth CI #42654579277 passed. No new Stock/Media/Auth image publication was run.
- Native cadence at 02:02:00Z: Platform reconcile #42942147668 age 520s / gap 14,244s; inspection #42932368784 age 5,271s / gap 17,791s; recovery #42939222343 age 2,003s / gap 13,889s; watchdog #42940581820 age 1,327s / gap 13,950s; TCE WF-06 #42922537816 age 9,692s / gap 18,739s; TCE WF-12 #42915709227 age 12,491s / gap 17,617s. All six inter-arrival gaps fail. Current age passes only for three Platform lanes. Manual inspection #42942360712 generated a fresh snapshot at 01:55:21Z but does not count as native schedule delivery.
- Watchdog logs show no sampled scheduled deployment lane above the 15-minute runner queue budget, while inter-arrival gaps remain 3.8–5.2 hours. Scheduler enqueue/delivery telemetry is not available through the repository workflow; GitHub administrator investigation remains a blocker.
- Fresh K3s snapshot: node Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; disk 56% / ~20 GiB free; ~19 GiB RAM available; restart required. Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1. Public OIDC discovery both realms HTTP 503.
- Stock/Media remain outside active Platform GitOps manifest scope but their namespaces/workloads remain pending the guarded retirement workflow. Storage preflight reports no target PVC/PV/VolumeSnapshot references; preserve Bound `k3s-debug/k3s-debug-logs`. Media runner service/listener remains active/enabled; remote unregister, external backup/retention and DNS ownership are not verified.
- Native reconciliation #42942147668 verified GHCR read access for five managed packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, observed TCE release pairing and clean GitOps drift, and skipped manifest apply/rollout. MicroFE health passed; TCE/Auth remain intentional zero-replica maintenance; Keycloak skipped.
- Do not alter cron, freshness budgets, TCE market-scan schedule or deployment ownership. Preserve CI/test/security/release/backup/integration/manual/scheduled workflows. No workflow is confirmed redundant or obsolete; no duplicate SSH/Compose authority was introduced.


## Historical verification — 2026-11-11 10:01 ICT / 03:01:03 UTC

- Direct master refs: Platform `1accff7fd7cc1ae733513dfa7eb6067a660f030a`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 and Authentication #76; no open PRs in TCE, Stock or Media. All remain draft/owner-decision. No workflow file was added or removed in this checkpoint.
- Platform manual reconciliation #42949244537 (workflow_dispatch, mode=apply, target=all, image changes disabled) succeeded with clean drift. GHCR preflight and Auth runtime Secret verification passed; shared `ghcr-pull` was unchanged. TCE desired/live image pairing matched `prod-v0.1.0-e75e338`. MicroFE was healthy; TCE/Auth were explicit zero-replica maintenance; Keycloak was skipped. Apply and rollout were skipped.
- Recovery receipt #42949413722 verified reconciliation #42949244537 and found native inspection #42932368784 stale. It reused the fresh manual inspection fallback #42942360712 (age 59m at 02:57Z) and did not dispatch a duplicate inspection. The fallback is 3,942s old at the 03:01:03Z reference and has only 558s remaining within the 4,500s limit. Fallback receipts do not satisfy native schedule cadence.
- Native schedule reference 03:01:03Z: Platform reconcile #42942147668 age 4,063s / gap 14,244s; inspection #42932368784 age 8,814s / gap 17,791s; recovery #42939222343 age 5,546s / gap 13,889s; watchdog #42940581820 age 4,870s / gap 13,950s; TCE WF-06 #42949191917 age 382s / gap 12,853s; TCE WF-12 #42944415193 age 2,908s / gap 13,126s. All six gaps fail; only TCE WF-06 current age passes. Watchdog runner-queue sample was below 15 minutes but does not provide scheduler enqueue/delivery telemetry.
- TCE native WF-06 #42949191917 and manual WF-06 #42949231253 failed strict HTTP 200 checks: TCE web, TCE API, Auth liveness and Auth readiness returned 503. WF-12 #42944415193 failed freshness. Preserve the strict health contract.
- Last-known K3s fallback #42942360712: node Ready/ARM64; disk 56% / ~20 GiB free; ~19 GiB RAM available; restart required. Media and MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1. Media runner remains active; retirement evidence incomplete. Snapshot expires at approximately 03:10:21Z if no newer inspection arrives.
- Keep the existing app-owned publisher workflows and Platform's single production apply authority. No app-owned direct SSH/Compose deploy authority was added. No workflow was confirmed redundant/obsolete. Do not change cron, freshness budgets or TCE market-scan schedule.


## Historical verification — 2026-11-11 10:55 ICT / 03:55:46 UTC

- Direct master refs: Platform `9848cdeb97a29ff3833378013f4932e6558cb933`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314/#544/#541/#539; Authentication #76; none in TCE/Stock/Media. Heads unchanged from the exact-head validation evidence recorded in the deployment tracker. All remain drafts/owner decisions.
- Latest workflow evidence: Platform master push validation #42950290166 PASS; TCE native WF-06 #42949191917 and manual #42949231253 failed four strict 503 probes; native WF-12 #42944415193 failed freshness; Stock CI #42610360402 PASS and scraper #42457182511 failed closed; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes have stale current-age and inter-arrival evidence at 03:55:46Z. Exact run IDs, ages, gaps and budgets are recorded in the deployment tracker. Do not count manual/workflow_run/repository_dispatch fallback receipts as native schedule delivery.
- Latest K3s snapshot #42942360712 is 7,225s old and exceeds the 4,500s freshness budget. Latest manual reconciliation #42949244537 is 3,636s old and exceeds its 2,700s budget. Prior GHCR/Secret/drift results are historical; no current rollout authorization is inferred.
- Preserve application-owned build/publish and Platform-only production apply boundaries. Stock/Media remain in guarded retirement scope; no republish, delete, runner retirement, credential rotation, host restart or DNS/database/storage mutation occurred. Preserve all useful workflows; none was confirmed redundant/obsolete. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Historical verification — 2026-11-11 12:04 ICT / 05:04:56 UTC

- Direct master refs: Platform Infra `bfa50827eacdb6675f718593c0b38cf693a38b01`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Current open PRs: Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. All remain drafts/owner decisions. Exact-head checks on those PRs are successful; Auth Supabase Preview is skipped. Do not merge owner-decision work without approval.
- Latest master CI: Platform validation #42956212725 PASS; TCE native WF-06 #42949191917 and manual #42949231253 fail all four strict public probes (HTTP 503 vs 200); WF-12 native #42944415193 fails freshness; Stock CI #42610360402 PASS and scraper #42457182511 fails closed on empty `VNSTOCK_API_KEY`; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes at 05:04:56Z: reconcile #42942147668 age 11,496s/gap 14,244s; inspection #42932368784 age 16,247s/gap 17,791s; recovery #42939222343 age 12,979s/gap 13,889s; watchdog #42940581820 age 12,303s/gap 13,950s; TCE WF-06 #42949191917 age 7,815s/gap 12,853s; TCE WF-12 #42944415193 age 10,341s/gap 13,126s. Every current-age and inter-arrival check exceeds its budget. Fallback receipts do not count.
- Latest K3s inspection #42942360712 is 11,375s old against 4,500s. Last manual reconciliation #42949244537 is 7,786s old against 2,700s. Both are stale; prior GHCR/Secret/drift results are historical and do not authorize rollout.
- Direct branch reads report `protected=false` for all five master branches. Repository metadata allows squash, merge commits and rebase on all five; administrator must confirm effective inherited rulesets and enforce squash-only/PR-only policy.
- App repositories retain ownership of CI/builds and immutable image publication. Platform remains the sole production apply authority. No new publication, promotion, apply, rollout, retirement, credential/DNS/database/storage mutation or host restart occurred. Preserve useful workflows; none was confirmed redundant/obsolete. No direct SSH/Compose authority added. TCE market-scan schedule unchanged.


## Post-checkpoint merge verification — 2026-11-11 12:08 ICT

- Platform master advanced documentation-only from `bfa50827...` to `0191e968d11a3b9096ddd24d46fa8daeb03fec3a` through PR #1614.
- Exact-head validation #42963714334 and post-merge validation #42963772141 both PASS.
- No production reconcile/recovery push run was triggered by the documentation-only merge. Workflow ownership and production authority boundaries are unchanged.


## Latest verification delta — 2026-11-11 12:58 ICT / 05:58:04 UTC

This checkpoint supersedes the 12:08 ICT compact readiness values above. It is based on direct Git refs, current open-PR metadata, first-page Actions run history (up to 100 runs per repository), exact-head workflow evidence for open PRs, and decoded job logs. Runtime evidence is explicitly freshness-bounded.

### Direct repository state and open PRs

- Direct `refs/heads/master` reads: Platform Infra `b88399f0b593f3e336db4d28b38d364c99215ce3`; TCE Dashboard `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; StockDividend `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media Generation `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform open PRs: #1314 head `db152c9a17416d1a7f82165597dfe478321bd055`; #544 `c95e7daecb83b65577b54303427fe4ea81adfe06`; #541 `b8f7c6ba04e3d971336a899b2efd5894662083b3`; #539 `2dc48b97017ecb08e49682633303a2f1d5e991a1`. Authentication open PR #76 head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`. No open PRs in TCE, Stock or Media.
- Exact-head validations for those five PRs remain successful: #1314 run #42161859747; #544 #38575430454; #541 #38567431761; #539 #38548718033; Auth #76 #41329425940. Auth Supabase Preview is skipped. All five remain drafts/owner decisions; do not merge Keycloak/database/identity/migration decisions without owner approval.
- Platform PR #1614 merged at `0191e968d11a3b9096ddd24d46fa8daeb03fec3a`; PR #1615 merged at current master `b88399f0b593f3e336db4d28b38d364c99215ce3`. Their exact-head and post-merge validation runs passed.
- Latest Platform master run is [#42963960326](https://github.com/phanthienquoc/platform-infra/actions/runs/42963960326), `validate-manifests`, push on current master SHA, SUCCESS at 05:10:33Z. No later Platform run appears in the queried 100-run page.
- Latest app evidence in queried run history: TCE manual WF-06 #42949231253 failed; native WF-06 #42949191917 failed; native WF-12 #42944415193 failed. Stock CI #42610360402 passed; scraper schedule #42457182511 failed closed. Media CI #42539512417 passed. Authentication CI #42654579277 passed. These app runs are older than this checkpoint; no new image publication/digest handoff was observed.

### Native schedule freshness

Reference: 2026-11-11 05:58:04 UTC. Only first-attempt `event=schedule` runs on `master` count. Manual, push, workflow_run and repository_dispatch receipts do not substitute.

| Lane | Latest native run | Previous native run | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---:|---:|---:|
| Platform reconcile | #42942147668 | #42909757881 | 14684 | 14244 | 2700 |
| Platform inspection | #42932368784 | #42887151366 | 19435 | 17791 | 4500 |
| Platform recovery | #42939222343 | #42906791198 | 16167 | 13889 | 2700 |
| Platform watchdog | #42940581820 | #42908417737 | 15491 | 13950 | 2700 |
| TCE WF-06 | #42949191917 | #42922537816 | 11003 | 12853 | 1500 |
| TCE WF-12 | #42944415193 | #42915709227 | 13529 | 13126 | 1500 |

All six current-age and all six inter-arrival checks exceed their budgets. The latest Platform native reconcile/recovery/watchdog runs use pre-current-master SHA `b5fceb3e...`; native inspection uses `d89bcf7e...`. No native scheduled run has validated current Platform master `b88399f0...`. TCE schedule runs use current TCE master but fail health/freshness. Preserve all cron expressions, budgets and the TCE market-scan schedule.

### TCE endpoint evidence

- Manual WF-06 [#42949231253](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42949231253) contains four independent failed endpoint jobs. Decoded logs show TCE web `https://tce.mrcute.space/` = HTTP 503; TCE API `/api/health` = 503; Auth liveness `/api/health` = 503; Auth readiness `/api/ready` = 503. All expected HTTP 200. Curl completed with retries; this is an upstream health failure, not runner initialization. The response body was not surfaced, so root cause remains unproven. Keep strict HTTP 200 contracts; do not scale or promote without owner-approved immutable digest, rollback reference and recovery approval.

### Stock and Media

- Stock CI #42610360402 passed. Scraper schedule #42457182511 failed closed because `VNSTOCK_API_KEY` was empty; the credential gate stopped before dependency installation/ingestion. Do not place the key in Git/logs/chat. Stock remains in the approved retirement scope; do not publish/promote replacement images while that scope remains active without an owner decision.
- Media CI #42539512417 passed. Media remains in guarded retirement scope. Remote runner unregister, external DB/object-storage backup/retention and authoritative DNS/provider ownership are not verified.
- Preserve the Bound `k3s-debug/k3s-debug-logs` PVC. No namespace/PVC/PV deletion or runner retirement is authorized by this checkpoint.

### K3s and GitOps — stale evidence only

- Latest read-only inspection fallback [#42942360712](https://github.com/phanthienquoc/platform-infra/actions/runs/42942360712) is `workflow_dispatch`, created 01:55:12Z (age 14572s at reference); its embedded snapshot was generated 01:55:21Z (age 14563s), far beyond the 4500s inspection budget. Latest native inspection #42932368784 is 19435s old.
- Latest native reconciliation [#42942147668](https://github.com/phanthienquoc/platform-infra/actions/runs/42942147668) is 14684s old; last manual reconciliation #42949244537 is 10974s old, beyond the 2700s budget. Recovery receipt #42949413722 is 10881s old. These are historical, not current rollout authorization.
- Native reconciliation job logs show `mode=apply`, `target_app=all`, `allow_image_changes=false`; shared `ghcr-pull` was unchanged, managed MicroFE/TCE image-pull checks reported no failures, TCE release pairing matched `prod-v0.1.0-e75e338`, and GitOps drift was false. The idempotent manifest/credential reconciliation returned `patched (no change)` / `unchanged`; the subsequent drift gate skipped any further manifest apply. No image replacement or workload rollout is evidenced. Deployment lane summary explicitly classified Auth as intentional zero-replica maintenance, MicroFE as healthy, TCE as maintenance, and Keycloak as skipped. Stock remains outside the managed GHCR pull helper/active GitOps scope.
- Last-known inspection: ARM64 node `tce-k3s-01` Ready, K3s v1.36.3+k3s1, Ubuntu 22.04.5, disk 56% / about 20 GiB free, RAM about 19 GiB available, host restart required. Media/MicroFE were 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin (two pods) and desired Backend ImagePullBackOff on `12d63b4` due no ARM64 platform descriptor; legacy Stock Backend/Frontend 1/1 without RepoDigest promotion evidence. Do not present this as live health.
- No fresh K3s snapshot or reconciliation was obtained in this run. Platform operator must run `inspect-vps.yml` read-only before any deployment decision. This does not authorize reboot, rollout or deletion.

### Branch governance and merge methods

- Direct `GET /branches/master` reports `protected=false` for all five repositories at this checkpoint.
- Repository metadata reports `allow_squash_merge=true`, `allow_merge_commit=true`, and `allow_rebase_merge=true` for all five repositories. Squash is available but merge-commit and rebase remain enabled, contrary to the intended squash-only standard.
- Branch-protection detail GET returns HTTP 403 for all five through the current integration. Effective inherited organization ruleset enforcement is therefore not positively established by this run.
- GitHub administrator must configure/confirm PR-only updates, required CI/deployment-contract checks, block force-push and deletion, disable merge-commit/rebase, and verify effective organization ruleset coverage. Continue dedicated branches, exact-head checks and expected-head squash merges until confirmed.

### Exact next actions and safety

1. Platform operator: run a fresh read-only `inspect-vps.yml`; do not reboot/upgrade the host or mutate production using stale receipts.
2. GitHub administrator: provide scheduler enqueue/delivery/Actions service telemetry for six lanes and enforce/confirm master protection plus squash-only merge settings.
3. TCE/Auth owners: diagnose four HTTP 503 endpoints and provide approved immutable release digest, rollback reference and explicit recovery approval.
4. Stock owner: decide whether scraper remains in service or stays in retirement scope; if retained, provision `VNSTOCK_API_KEY` only via Actions Secrets and run safe `preflight_only=true`.
5. Media/Platform owners: complete external backup/retention, DNS ownership and remote runner stop/disable/unregister evidence before guarded deletion.
6. Registry administrator: verify GHCR server-side immutable-tag enforcement.

No new GHCR publication, digest promotion, effective production manifest change, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/object-storage mutation or host reboot occurred in this checkpoint. Preserve all useful CI/test/security, release, backup, integration, manual and scheduled workflows; none is confirmed redundant/obsolete. Do not add direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 13:03 ICT

- PR #1616 squash merge SHA: `14e79f1c90f8390636f13a06a899c0de0ab85bd0`.
- Exact-head validation #42969674108 PASS; post-merge master validation #42969724857 PASS.
- Only `validate-manifests` ran after the docs-only merge. No production reconcile/recovery push run was triggered.
- App repositories remain CI/build/immutable-publication owners; Platform remains the only production apply authority.
- No workflow was removed; no SSH/Compose deployment authority added; TCE market-scan schedule unchanged.


## Latest operational evidence — 2026-11-11 14:03 ICT / 07:03:57 UTC

### Current repository refs and open PRs

- Platform Infra master `e6d6213ea5441622a314d1ccacfc3d5fe358fe40`; open PRs #1314/#544/#541/#539, all drafts/owner decisions. Exact-head `validate` checks PASS.
- TCE Dashboard master `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; no open PRs. WF-06 manual #42972014911 failed four strict HTTP 200 probes; native WF-06 #42949191917 and native WF-12 #42944415193 remain stale. WF-07 schedule #42971954835 succeeded but is not a health-lane substitute.
- StockDividend master `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; no open PRs. CI #42610360402 passed; scraper #42457182511 failed closed because `VNSTOCK_API_KEY` was empty. Stock remains guarded retirement scope.
- Media Generation master `dcd698699c65ba6e73f6b43838975144777131c3`; no open PRs. CI #42539512417 passed; K3s backend/frontend are 1/1 and digest-pinned; dedicated runner service remains active/enabled.
- Authentication master `eab85fab32d7c9baef750c1fedbb93deb8c1333f`; open PR #76 is a draft migration-drift plan. Exact-head validate PASS and Supabase Preview skipped. Auth runtime remains intentional 0/0 maintenance.

### Current runtime/credential evidence

- Inspection #42972248777 is a read-only workflow_dispatch fallback generated 06:25:00Z; age 2,337s at reference, within the 4,500s budget. Node Ready/ARM64, K3s v1.36.3+k3s1, disk 56% / ~20 GiB free, ~19 GiB RAM available, host restart required. Preserve the Bound debug PVC.
- Media and MicroFE core workloads 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1 without RepoDigest. Target Stock/Media namespaces have no PVC/PV claim or VolumeSnapshot references in read-only preflight; Media remote runner unregister, external backup/retention and DNS ownership remain unverified.
- Reconciliation #42972016233 age 2,464s at reference, within 2,700s budget. GHCR read preflight passed for five managed packages; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged. No managed image-pull failures; clean diff/drift; manifest apply, image replacement and rollout skipped. MicroFE healthy; TCE/Auth maintenance; Keycloak skipped.
- TCE/Auth/OIDC HTTP 503 results are consistent with zero-replica maintenance. Preserve strict HTTP 200 probes; never mark zero-replica maintenance as live healthy.

### Native schedule state

At 07:03:57Z, all six configured health/reconciliation lanes exceed current-age and inter-arrival budgets. Latest native runs: Platform reconcile #42942147668, inspection #42932368784, recovery #42939222343, watchdog #42940581820; TCE WF-06 #42949191917 and WF-12 #42944415193. Exact ages, gaps and budgets are in the deployment tracker. Do not count manual/workflow_run/repository_dispatch fallbacks as native delivery. Preserve all cron expressions and the TCE market-scan schedule.

### Workflow preservation and authority

No workflow was added or removed in this checkpoint. Keep CI, tests, security, app-owned immutable publication, release, backup, integration, manual and scheduled workflows. App repositories remain responsible for tests/builds and immutable GHCR publication; Platform remains the sole production manifest, shared credential, GitOps promotion/reconciliation, rollout and health authority. No duplicate direct SSH/Compose authority is permitted.


## Historical verification — 2026-11-11 15:35 ICT / 08:35:19 UTC

- Platform master `cfeb5dbf74a625f443d44141bd4c719f47ec60a3`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1624 squash-merged at `cfeb5dbf...`; exact-head #42987271290 PASS and post-merge master #42988178995 PASS. Post-merge run contains `validate-manifests` only; no production reconcile/recovery push was triggered.
- Open owner-decision PRs remain Platform #1314/#544/#541/#539 and Authentication #76; none in TCE/Stock/Media. Exact-head `validate` checks pass; Auth Supabase Preview skipped. Do not merge without owner approval.
- Platform native lanes: reconcile #42942147668, inspection #42981286761, recovery #42986496462, watchdog #42986833403. TCE health lanes: WF-06 #42949191917 and WF-12 #42944415193. All six inter-arrival budgets fail; three current-age budgets fail. Manual and workflow_run fallbacks do not count as native delivery.
- Freshness-bounded runtime evidence: inspection #42981286761 age 3245s / 4500s; manual reconciliation #42986517013 age 771s / 2700s; recovery #42986712253 age 683s / 2700s. Node Ready/ARM64; Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1 without RepoDigest. Preserve the Bound debug PVC.
- Reconciliation #42986517013: GHCR read preflight PASS, Auth runtime Secret verified with values suppressed, shared `ghcr-pull` unchanged, TCE image pairing PASS, drift=false, apply/image replacement/rollout skipped. Recovery #42986712253 avoided duplicate fallback dispatch.
- TCE manual WF-06 #42972014911 returned HTTP 503 on all four strict public probes while K3s reports TCE/Auth/Keycloak 0/0 maintenance. Keep HTTP 200 health contract; maintenance is not healthy.
- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Media CI #42539512417 PASS; digest-pinned workloads running and runner still active. Auth CI #42654579277 PASS; Auth remains maintenance.
- Preserve app-owned tests/builds/immutable publishers and Platform-only production apply. No workflow removed, no direct SSH/Compose authority, no production mutation, no credential/DNS/database/storage change, no reboot. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 15:40 ICT / 08:40:35 UTC

- Platform master `8419328596b1a96340dd48fd439d08c77f04da38`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Auth `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1625 exact-head #42988772690 PASS and post-merge master #42988867666 PASS. Only `validate-manifests` ran after merge; no production reconciliation/recovery push was triggered.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 and Auth #76; none in TCE/Stock/Media. Exact-head `validate` checks pass; Auth Supabase Preview skipped.
- Six native schedule lanes: Platform reconcile #42942147668, inspection #42981286761, recovery #42986496462, watchdog #42986833403; TCE WF-06 #42949191917 and WF-12 #42944415193. All six inter-arrival gaps fail; three current-age budgets fail. Do not count manual or workflow_run fallbacks as native delivery.
- K3s inspection #42981286761 age 3561s / 4500s; manual reconciliation #42986517013 age 1087s / 2700s; recovery #42986712253 age 999s / 2700s. Node Ready/ARM64; Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; legacy Stock Backend/Frontend 1/1 without RepoDigest. Preserve the Bound debug PVC.
- Reconciliation: GHCR preflight PASS, Auth runtime Secret verified, shared `ghcr-pull` unchanged, TCE pairing PASS, drift=false, apply/image replacement/rollout skipped. Recovery avoided duplicate fallback dispatch.
- TCE strict HTTP 200 probes still returned 503 in the last manual WF-06 run while K3s shows zero replicas. Preserve strict health contract; maintenance is not healthy.
- Stock CI PASS; scraper fails closed on empty `VNSTOCK_API_KEY`. Media CI PASS; digest-pinned workloads running; runner still active. Auth CI PASS; Auth remains maintenance.
- Preserve app-owned tests/builds/immutable GHCR publication and Platform-only production apply. No workflow removed, no SSH/Compose authority, no production mutation, no credential/DNS/database/storage changes, no host reboot. TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-11 15:55 ICT / 08:55:27 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest relevant workflow evidence | Ownership / preserved lanes |
|---|---|---|---|
| Platform Infra | `4cb217722b77c190886cb2ce1c28fe26802bce19` | `validate-manifests` #42989295172 PASS on current master; native reconcile #42942147668, inspection #42981286761, recovery #42986496462, watchdog #42986833403. | Sole production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health authority. Preserve native schedules, manual reconciliation, recovery, watchdog, inspection, CI/contract validation, backup/cleanup and purposeful dispatch jobs. |
| TCE Dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | Native WF-06 #42949191917 FAIL; native WF-12 #42944415193 FAIL; latest manual WF-06 #42972014911 FAIL; WF-07 integration #42971954835 PASS; WF-07 backup #42924677977 PASS. | Owns application tests/builds and immutable image publication. Preserve WF-06 strict HTTP 200 probes, WF-12 freshness watchdog, WF-13 recovery, WF-07 integration and backup. Do not count integration/backup as health-lane substitutes. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; weekend scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty. | Owns app tests/builds/publication if service retention is approved. Keep scraper fail-closed; no secret in Git/logs/chat; no image publication while approved retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last K3s snapshot #42981286761 showed backend/frontend 1/1 with registry digest references and runner service/listener active. | Owns tests/builds/immutable publication. Preserve CI/release workflows. Runner retirement remains gated on remote unregister, backup/retention and DNS ownership. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; last reconciliation #42986517013 verified runtime Secret with values suppressed; Auth remains 0/0 maintenance. | Owns Auth tests/builds/immutable publication. Preserve CI, security and release contracts. Zero replicas and OIDC 503 are not live health. |

### Open PR and governance inventory

- Platform open drafts: #1314, #544, #541, #539. Authentication open draft: #76. No open PRs in TCE, Stock or Media.
- Exact-head checks: Platform drafts each `validate=success`; Auth #76 `validate=success`, Supabase Preview skipped. Keep all owner-decision drafts unmerged.
- All five master branches report `protected=false` and no required status checks; all five repository metadata records allow squash, merge commits and rebase. Effective inherited rulesets remain unverified. Administrator action is required; no repository setting was changed.
- No workflow was removed or added. No direct SSH/Compose deployment authority was introduced. TCE market-scan schedule and all existing cron expressions are unchanged.


## Post-merge workflow inventory receipt — 2026-11-11 16:00 ICT

- Platform master now `37a5624a325c570df0fc689b4f6ecde5f9bae89e` after docs-only PR #1627.
- Exact-head validation #42991422461 PASS; post-merge `validate-manifests` #42991499455 PASS.
- No reconcile/recovery push was triggered. Production apply authority remains Platform only; app repositories retain tests/builds/immutable GHCR publication ownership.
- Last K3s snapshot #42981286761 is expired; last successful reconciliation #42986517013 is within its age budget but ran on older SHA `8f95ddd872...`. Neither authorizes a new rollout against current master.
- Preserve CI/test/security, app publication, release, backup, integration, manual and scheduled jobs. No workflow removal/addition, no SSH/Compose authority, and no TCE market-scan schedule change.


## Latest workflow inventory verification — 2026-11-11 16:58 ICT / 09:58:55 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `e6b7156d191ff3ae9bcb8ff66f1b2a5259de331e` | Native reconcile #42993779924 SUCCESS (pre-merge SHA `c557b3f`); read-only inspection #42994074939 SUCCESS via workflow_dispatch and PR #1629 squash-merged; exact-head validation #42994322789 PASS; recovery #42996312662 SUCCESS; watchdog workflow_run #42996353169 SKIPPED. | Sole production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and health authority. Preserve native schedules, manual reconciliation, recovery, watchdog, inspection, CI/contract validation, backup/cleanup and purposeful dispatch jobs. |
| TCE Dashboard | `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab` | Native WF-06 #42949191917 stale/failed; native WF-12 #42996293386 failed because WF-06 age was 399m; manual WF-06 #42996339882 failed four strict HTTP 200 probes (503); WF-13 #42996315416 recovery success. | Owns app tests/builds, immutable TCE/MicroFE GHCR publication, strict public health probes, backup and integration checks. Preserve WF-06/WF-12/WF-13, WF-07 backup/integration and release-gated publishers. Do not count fallback/integration/backup as native health delivery. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. K3s desired Stock Admin/Backend pods ImagePullBackOff; legacy Backend/Frontend 1/1. | Owns app tests/builds and native ARM64 immutable publication only if service retention is approved. Preserve fail-closed scraper and gated publisher; no secret in Git/logs/chat and no publication while retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; K3s backend/frontend 1/1 with registry digest references; dedicated Media runner service/listener active/enabled. | Owns tests/builds/immutable publication. Preserve CI/release workflows. Runner retirement remains gated on remote unregister, backup/retention and DNS ownership. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth remains 0/0 maintenance; runtime Secret provision/verification succeeded in #42993779924 with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release contracts. Zero replicas and OIDC/health 503 are not live health. |

### Open PR and governance inventory

- Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76; no open PRs in TCE, Stock or Media. Exact-head `validate` checks remain PASS on the unchanged heads; Auth Supabase Preview is skipped. Keep these drafts unmerged pending their stated owner decisions.
- All five direct `branches/master` API responses report `protected=false`, `protection.enabled=false`, and no required status checks (`enforcement_level=off`, empty contexts/checks). Repository settings allow squash, merge commits and rebase. Effective inherited organization ruleset evaluation remains a separate administrator task.
- No workflow was added or removed. Preserve app CI/tests/security, immutable publishers, backup, integration, manual/release and scheduled jobs. No direct SSH/Compose deployment authority. TCE market-scan schedule and all existing cron expressions remain unchanged.

### Freshness and production authority

- Six native cadence lanes all exceed inter-arrival budgets. Current-age budgets fail for Platform inspection/recovery/watchdog and TCE WF-06; Platform reconciliation and TCE WF-12 are still within current-age budgets at the 09:58:55Z reference. Do not count workflow_dispatch, workflow_run or repository_dispatch as native schedule delivery.
- Read-only K3s snapshot #42994074939 is 2,415s old / 4,500s budget. Native reconciliation #42993779924 is 2,550s old / 2,700s budget but ran on pre-merge SHA `c557b3f`, not current master `e6b7156d`. It found no drift and skipped apply/image replacement/rollout; Auth runtime Secret provision/verification succeeded, shared `ghcr-pull` remained unchanged.
- No new app image publication or digest promotion. No current-master production apply or workload rollout. Keep Platform `reconcile-vps.yml` as the single production apply authority; `inspect-vps.yml` remains read-only. No SSH/Compose authority in app repos.

## Post-merge workflow inventory receipt — 2026-11-11 16:58 ICT

- Platform master advanced documentation-only through PR #1630 to `1bd6ea38fcc4591da16422868ac03124704ea293`.
- Exact-head validation #43000595633 PASS; post-merge master validation #43000748526 PASS.
- Post-merge run contains `validate-manifests` only; no production reconcile/recovery push was triggered.
- The 16:58 operational snapshot remains the latest runtime/schedule evidence; this receipt updates only the Platform master SHA and validation provenance.
- Workflow ownership and production authority boundaries are unchanged. No workflow was added/removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.

## Latest verification — 2026-11-11 18:01 ICT / 11:01:52 UTC

### Current refs and workflow ownership

| Repository | Current master | Latest evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `ff401dadb1cac5b0647c1a4187fe171b2cfbc937` | Current-master manual reconcile #43003088695 SUCCESS; recovery #43003328970 SUCCESS; current-master manifest validation #43001011228 PASS. Native schedule lanes remain stale. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps reconciliation, rollout and health authority. Preserve native schedules, read-only inspection, manual plan/apply, recovery, watchdog, validation, backup and guarded operations. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | PR #1037 merged; exact-head WF-01P #43008284677, WF-02 #43008284672, WF-05 #43008284792, WF-08B #43008284695 PASS. Post-merge WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 queued/in progress. Native WF-06 #43003016447 failed four HTTP 200 probes with 503. | Owns tests/builds/immutable GHCR publication, strict public health probes, integration/backup and maintenance-aware recovery. WF-13 honors `TCE_MAINTENANCE_MODE=true` only to suppress redundant read-only fallback; WF-06/12 remain strict and scheduled. WF-01P runs the health-recovery contract validator. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Desired Stock Admin/Backend ImagePullBackOff; legacy Backend/Frontend 1/1. | Owns app tests/builds/native ARM64 immutable publication only if owner approves retention. Keep scraper fail-closed; no secret in Git/logs/chat and no image publication while retirement remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last partial K3s inventory showed backend/frontend 1/1 and runner active. Full inspection is stale. | Owns tests/builds/immutable publication. Preserve CI/release. Runner retirement remains gated on remote unregister, backup/retention and DNS ownership. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth is intentional 0/0 maintenance; runtime Secret provision/verification succeeded in #43003088695 with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release. Zero replicas and OIDC/health 503 are not live health. |

### Open PRs and branch governance

- Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. Exact-head validation runs remain PASS: #42161859747, #38575430454, #38567431761, #38548718033 and Auth #41329425940 (Supabase Preview skipped). TCE #1037 is merged; no open PRs remain in Stock or Media.
- Direct `branches/master` API responses still report `protected=false`, `protection.enabled=false`, and required status checks enforcement off/empty on all five repositories. Repository settings permit squash, merge commit and rebase. Administrator must enforce PR-only, required checks, force-push/deletion protection and squash-only.
- No workflow was removed or added in this checkpoint. App repositories own tests/builds/immutable publication; Platform remains sole production apply authority. No direct SSH/Compose authority. TCE market-scan schedule unchanged.

### TCE maintenance-aware recovery contract

- TCE PR #1037 merged at `5b425bdeab457e943bcecf1831836fc698e24394`. WF-13 now reads the repository Actions variable `TCE_MAINTENANCE_MODE`; `true` suppresses only the redundant read-only WF-06 fallback. It does not change WF-06 expected HTTP 200 status, WF-12 schedule monitoring or cron expressions.
- `scripts/validate-tce-health-recovery-contract.sh` is run by WF-01P and checks workflow YAML, both maintenance guards, four HTTP 200 endpoints and unchanged WF-06/WF-12 schedules. Exact-head PR validation passed.
- Repository variable value was not changed or verified. An authorized TCE repository administrator must set `TCE_MAINTENANCE_MODE=true` while zero-replica maintenance is intentional; unset/set false after reactivation.

### Runtime and schedule evidence

- Current-master reconciliation #43003088695 passed GHCR read preflight for five packages, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, verified TCE pairing `prod-v0.1.0-e75e338`, found drift=false and skipped manifest apply/image replacement/rollout. Its post-check pod inventory showed Media/MicroFE 1/1, TCE/Auth/Keycloak 0/0 maintenance, Stock Admin/desired Backend ImagePullBackOff and legacy Stock Backend/Frontend 1/1.
- Last full read-only inspection #42994074939 is older than the 4,500s budget. Partial node/pod output from #43003088695 is not a substitute for full disk/RAM/storage/runner inventory. Obtain a fresh inspect before any production decision.
- All six native schedule lanes exceed both current-age and inter-arrival budgets at 11:01:52Z. Do not count manual/workflow_run/repository_dispatch as native delivery. Keep every cron expression and TCE market-scan schedule unchanged.


## Post-merge workflow inventory receipt — 2026-11-11 18:05 ICT

- Platform master advanced documentation-only through PR #1632 to `c49bb0f1f1df71f403c64cc17fada8d4ab99bc31`.
- Exact-head `validate-manifests` #43008866804 PASS; post-merge master `validate-manifests` #43008949806 PASS.
- Only `validate-manifests` ran after the Platform docs-only merge; no production reconciliation/recovery push was triggered.
- TCE master `5b425bdeab457e943bcecf1831836fc698e24394`: post-merge WF-01 #43008514423, WF-05 #43008514459 and WF-02 #43008514481 all PASS after PR #1037. No GHCR publication was triggered.
- The 18:01 ICT operational/schedule snapshot remains the latest runtime evidence; this receipt updates only current refs and validation provenance.
- Workflow ownership and production authority boundaries are unchanged. No workflow removed, no SSH/Compose authority added, and TCE market-scan schedule unchanged.


## Fresh K3s inspection inventory — 2026-11-11 18:09 ICT

- Inspection #42994074939 attempt 2 SUCCESS; snapshot generated 11:06:54Z and was 152s old at the 11:09:26Z reference. Inspection-only PR #1634 auto-squash-merged after exact-head validation #43009458775 PASS; current Platform master `388f96b7f7b0c97f461691b5862aff83b7d0b4f2`.
- Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Ubuntu 22.04.5; RAM 23Gi total/19Gi available; disk 45G/56% used/20G available; pressure normal. Host restart required; kernel/containerd/Docker updates pending. Do not reboot or clean images without approval.
- Platform and Media runner services active/enabled. Docker has 5.773GB reclaimable image data; no cleanup performed. Preserve `k3s-debug/k3s-debug-logs` PVC/PV (Bound, 1Gi, RWO, local-path).
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running with registry digests. TCE/Auth/Keycloak are 0/0 maintenance, not healthy. Stock Admin (2) and desired Backend (1) remain ImagePullBackOff on tag `12d63b4` with no registry digest; legacy Backend/Frontend 1/1 have only local image IDs and are not promotion evidence.
- All six native schedule current-age/inter-arrival budgets fail. Manual inspection rerun is not native schedule evidence. TCE market-scan schedule unchanged.
- Platform #1632/#1633 validations and post-merge validations PASS; inspection PR #1634 exact-head validation PASS. TCE #1037 exact-head and post-merge checks PASS. No workflow removed, no SSH/Compose authority, Platform remains sole production apply authority.


## Latest workflow inventory verification — 2026-11-11 19:01 ICT / 12:01:39 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest workflow evidence | Ownership / preserved lanes |
|---|---|---|---|
| Platform Infra | `8da047c223a2c10b5e0dd6a08aa8770fbc7f92c1` | `validate-manifests` #43009993417 PASS. Native reconcile #42993779924 (schedule/success), inspection #42981286761 (schedule/success), recovery #42986496462 (schedule/success), watchdog #42986833403 (schedule/failure). | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and health verification. Preserve reconcile, read-only inspection, recovery, watchdog, manifest/contract validation, backup and guarded maintenance workflows. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | Master WF-01 #43008514423 PASS, WF-05 #43008514459 PASS, WF-02 #43008514481 PASS. Native WF-06 #43003016447 FAIL (four HTTP 503 probes); native WF-12 #42996293386 FAIL (WF-06 source stale, queue 0m). | Owns app tests/builds/immutable GHCR publication, strict public health probes, integration/backup and maintenance-aware recovery. Preserve WF-06 HTTP 200, WF-12 schedule watchdog, WF-13 maintenance-aware fallback, WF-07 integration/backup and release publishers. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scheduled scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` was empty. | Owns app tests/builds/native ARM64 immutable publication only if retention is approved. Preserve fail-closed scraper and gated publisher; no secret in Git/logs/chat and no publication while retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last full K3s snapshot shows backend/frontend 1/1 with registry digest references; runner service/listener active. | Owns tests/builds/immutable publication. Preserve CI/release. Runner retirement requires remote unregister, backup/retention and DNS ownership evidence. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth remains 0/0 maintenance; Auth runtime Secret was provisioned/verified in historical reconciliation #43003088695 with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release. Zero replicas and OIDC/health 503 are not live health. |

### Open PRs and checks

- Platform open owner-decision drafts: #1314, #544, #541 and #539; TCE/Stock/Media have no open PRs; Authentication draft #76 remains open.
- Exact-head PR validation evidence: Platform #1314 #42161859747 PASS, #544 #38575430454 PASS, #541 #38567431761 PASS, #539 #38548718033 PASS; Auth #76 #41329425940 PASS (Supabase Preview skipped by design). Keep these drafts unmerged pending their documented owner decisions.
- Current master refs were read directly from `refs/heads/master`. Direct branch-protection GET returned 403 for all five repositories; repository metadata allows squash, merge commit and rebase. Do not claim effective inherited rulesets are absent; administrator verification is required.

### Schedule and runtime evidence

- At 12:01:39Z, all six native schedule lanes exceed both current-age and inter-arrival budgets. Latest run IDs/gaps: Platform reconcile #42993779924 / 26,585s; inspection #42981286761 / 25,617s; recovery #42986496462 / 24,822s; watchdog #42986833403 / 24,297s; TCE WF-06 #43003016447 / 26,842s; WF-12 #42996293386 / 26,503s. Do not count manual, push, `workflow_run` or `repository_dispatch` as native delivery.
- Watchdog logs confirm the four Platform schedule inter-arrival failures. WF-12 logs report WF-06 source #42949191917 age 399m and queue 0m. WF-06 logs confirm all four public endpoints returned 503 rather than the required 200.
- K3s snapshot #42994074939 was generated 11:06:54Z; age 3,285s / 4,500s budget at reference, expires 12:21:54Z. Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock desired Admin/Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1 without registry RepoDigest. Preserve the Bound debug PVC.
- Reconciliation #43003088695 succeeded on old SHA `ff401dad`, not current master `8da047c2`; it found no drift, verified GHCR read access and Auth runtime Secret, left shared `ghcr-pull` unchanged, and skipped apply/image replacement/rollout. It is older than the 20-minute recovery freshness window. Run current-master `reconcile-vps.yml` in `mode=plan` before any deployment decision.
- TCE `TCE_MAINTENANCE_MODE` Actions variable could not be read through the current connector; its value remains unverified. Keep WF-06 strict and WF-12 active. Do not change the TCE market-scan schedule.

### Authority and safety

- App repositories retain tests/builds and immutable GHCR publication. Platform Infra remains the only production manifest/credential/GitOps apply, rollout and health authority.
- No workflow removed or added, no direct SSH/Compose authority, no new image publication or digest promotion, no current-master production apply, no workload rollout, no namespace/PVC/PV deletion, no runner retirement, no credential rotation, no DNS/database/storage mutation and no host reboot.


## Post-merge workflow inventory receipt — 2026-11-11 19:09 ICT / 12:09:43 UTC

- Platform master is `815f87e14832d35970f3e43b8e9c309301b0fc81` after docs-only PR #1636 and corrective PR #1637. Exact-head validations #43017483631 and #43017776105 PASS; post-merge `validate-manifests` runs #43017580624 and #43017854916 PASS. Only manifest validation ran after both merges; no production reconcile/recovery push was triggered.
- PR #1637 corrected the three interval pairs by exact run timestamps: Platform reconcile #42942147668 → #42993779924 = 26,585s; TCE WF-06 #42949191917 → #43003016447 = 26,842s; TCE WF-12 #42944415193 → #42996293386 = 26,503s. The other Platform gaps remain inspection 25,617s, recovery 24,822s and watchdog 24,297s.
- No new native schedule run appeared by 12:09:43Z. All six current-age budgets and all six inter-arrival budgets remain failed. Do not count manual, push, `workflow_run` or `repository_dispatch` as native schedule delivery.
- K3s snapshot #42994074939 is 3,769s old / 4,500s budget at the reference, with 731s remaining. Platform operator must refresh read-only inspection before 12:21:54Z. Last reconciliation #43003088695 is 6,429s old and is on pre-current SHA `ff401dad`; run current-master `mode=plan` before any apply decision.
- Ownership boundaries unchanged: app repositories own tests/builds/immutable GHCR publication; Platform Infra alone owns production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health verification. No workflow removed/added, no SSH/Compose authority, no production mutation, and TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-11 19:59 ICT / 12:59:10 UTC

### Repository workflow and ownership snapshot

| Repository | Current master | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `47052106687e95a151da731f8fd28cddd872fbe6` | Current-master manifest validation #43018649706 PASS. No current-master reconcile or fresh inspection. Last full inspection #42994074939 attempt 2 is stale; last reconciliation #43003088695 succeeded on old SHA `ff401dad` and skipped apply/image replacement/rollout. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and health verification. Preserve native schedules, manual reconciliation, read-only inspection, recovery, watchdog, CI/contract validation, backup and guarded maintenance workflows. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | WF-01/02/05 master runs PASS. Native WF-06 #42949191917 and WF-12 #42996293386 FAIL/stale; WF-06 rerun attempt 2 #43003016447 excluded from native first-attempt cadence. Manual WF-06 #43003071073 returns four HTTP 503s. WF-12 #43019107548 and WF-13 #43019140175 workflow_run receipts SKIPPED. | Owns tests/builds/immutable TCE and MicroFE GHCR publication, strict public health probes, integration/backup and maintenance-aware recovery. Preserve WF-06 HTTP 200, WF-12 native schedule monitoring, WF-13 maintenance-aware fallback, integration/backup and release publishers. Do not count reruns/fallback/workflow_run as native schedule delivery. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Last K3s snapshot shows desired Admin/Backend ImagePullBackOff; legacy Backend/Frontend 1/1. | Owns app tests/builds/native ARM64 immutable publication only if retention is approved. Preserve fail-closed scraper and gated publisher; no secret in Git/logs/chat and no publication while retirement scope remains active. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS; last full snapshot shows backend/frontend 1/1 with registry RepoDigests; dedicated runner service/listener active/enabled. | Owns tests/builds/immutable publication. Preserve CI/release workflows. Runner retirement requires remote unregister, backup/retention and DNS ownership evidence. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth 0/0 maintenance. Runtime Secret was verified by historical reconciliation #43003088695 on old Platform SHA with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release. Zero replicas and OIDC/health 503 are not live health. |

### Open PR and check inventory

- Platform owner-decision drafts: #1314/#544/#541/#539; Auth draft #76; no open PRs in TCE/Stock/Media. Current check-run API reads show the unchanged PR heads' `validate` checks PASS: Platform #1314 #42161859747, #544 #38575430454, #541 #38567431761, #539 #38548718033; Auth #76 #41329425940 PASS with Supabase Preview SKIPPED. Keep all owner-decision drafts unmerged.
- Direct branch API: all five master branches report `protected=false`, protection disabled and no required status-check enforcement. Repository metadata permits squash, merge commit and rebase. Effective organization ruleset inheritance is unverified; GitHub administrator must confirm and enforce squash-only/required checks.

### Native schedule evidence at 12:59:10 UTC

Only first-attempt `event=schedule` runs on `master` count. Platform reconcile #42993779924 age 13,365s/gap 26,585s; inspection #42981286761 age 19,084s/gap 25,617s; recovery #42986496462 age 16,611s/gap 24,822s; watchdog #42986833403 age 16,460s/gap 24,297s; TCE WF-06 #42949191917 age 36,269s/gap 12,853s; TCE WF-12 #42996293386 age 12,292s/gap 26,503s. All current-age and inter-arrival budgets fail. WF-06 #43003016447 is attempt 2 and not counted; WF-12 #43019107548 is workflow_run/SKIPPED. Preserve all cron expressions and TCE market-scan schedule.

### Runtime freshness and safety

- Full K3s snapshot #42994074939 attempt 2 generated 11:06:54Z; age 6,736s / 4,500s budget, expired. Last reconciliation #43003088695 age 9,396s / 2,700s, old Platform SHA `ff401dad`; drift=false and no apply/image replacement/rollout. No current-master production authorization.
- Last-known node/resources/workloads are historical only. Preserve `k3s-debug/k3s-debug-logs`; Stock desired pods ImagePullBackOff and legacy images have no RepoDigest; Media/MicroFE digest references are valid in the snapshot. Do not reboot, cleanup images, scale maintenance workloads, promote Stock, delete namespace/storage or unregister runner from stale evidence.
- App repos retain tests/builds and immutable publication. Platform Infra alone owns production manifests, shared GHCR credentials, GitOps promotion/reconciliation, rollout and health. No direct SSH/Compose authority. No workflow added/removed in this checkpoint.


## Post-merge workflow inventory receipt — 2026-11-11 20:05 ICT / 13:05:10 UTC

- Platform master advanced documentation-only through PR #1639 to `11aab7a9241621dcd09cb580b2760f76f198edd0`.
- Exact-head `validate-manifests` #43025767904 PASS; post-merge master `validate-manifests` #43025893643 PASS on the exact merge SHA.
- The post-merge run contained validation only. No production reconciliation/recovery push was triggered.
- The 19:59 ICT operational/schedule snapshot remains the latest runtime evidence. This receipt changes only master SHA/validation provenance.
- Workflow ownership and authority boundaries are unchanged. No workflow added/removed, no SSH/Compose authority, no production mutation, and TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-11 21:03 ICT / 14:03:27 UTC

### Repository refs, PRs and workflow status

| Repository | Current master | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `be9a5fba7feb057a6f4ee94f90836804baeb2b66` | Master `validate-manifests` #43026129602 PASS. No current-master inspection or reconciliation. Native schedule lanes remain stale. | Sole production manifests, shared GHCR pull credentials, provenance/digest promotion, GitOps plan/apply, rollout and runtime health. Preserve inspection, reconciliation, recovery, watchdog, validation, backup and guarded maintenance. |
| TCE Dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | WF-01/02/05 master runs PASS. Native WF-06 #42949191917 and WF-12 #42996293386 fail/stale. WF-06 attempt 2 #43003016447 is excluded from first-attempt cadence. WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED. | Owns app tests/builds/immutable GHCR publication and strict HTTP 200 health probes. Preserve WF-06, WF-12 native monitoring, WF-13 maintenance-aware fallback, integration/backup and release workflows. Maintenance variable remains unverified. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Desired Admin/Backend last seen ImagePullBackOff. | Owns tests/builds/native ARM64 immutable publication only if owner reverses retirement. Preserve fail-closed scraper and gated publisher; no secrets in Git/logs/chat. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | CI #42539512417 PASS. Last full inspection showed backend/frontend 1/1 with registry RepoDigests and runner active/enabled; evidence is stale. | Owns tests/builds/immutable publication. Preserve CI/release. Runner retirement requires remote unregister, backup/retention and authoritative DNS evidence. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | CI #42654579277 PASS; Auth remains 0/0 maintenance in last full snapshot. Historical runtime Secret provision/verification succeeded with values suppressed. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release; zero replicas and OIDC/health 503 are not live health. |

- Open drafts: Platform #1314/#544/#541/#539 and Auth #76; no open PRs in TCE/Stock/Media. Exact-head validation receipts remain PASS on unchanged heads, but are historical and do not resolve owner decisions.
- Direct branch-protection GET returned 403 for all five repositories. Repo-level rulesets GET returned [] for public Platform/TCE/Media/Auth and 403 for private Stock. Effective organization ruleset inheritance remains unverified. Repository metadata permits squash, merge commit and rebase; administrator must enforce the intended governance.
- At 14:03:27Z all six native schedule current-age and inter-arrival budgets fail. Latest run IDs/gaps: Platform reconcile #42993779924 / 26,585s; inspection #42981286761 / 25,617s; recovery #42986496462 / 24,822s; watchdog #42986833403 / 24,297s; TCE WF-06 #42949191917 / 12,853s; WF-12 #42996293386 / 26,503s. WF-06 #43003016447 is attempt 2; WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED. None substitutes for native first-attempt delivery.
- Full K3s inspection #42994074939 attempt 2 snapshot is approximately 10,593s old / 4,500s budget. Last reconciliation #43003088695 is 13,253s old / 2,700s budget and ran on pre-current SHA `ff401dad`. Neither authorizes a deployment. Obtain fresh read-only inspection and current-master `mode=plan` reconciliation before any production decision.
- No new GHCR publication/digest promotion, current-master apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot. Preserve useful workflows; none is confirmed obsolete. Platform Infra remains sole production apply authority; no SSH/Compose authority. TCE market-scan schedule unchanged.


## Post-merge verification — 2026-11-11 22:03 ICT

- Platform Infra PR #1641 was squash-merged after exact-head validation #43035377158 passed all contract steps. Merge SHA/current master: `1fdc57a8dc098fa5fdc1749f0e11ff0714209e42`.
- Current-master `validate-manifests` #43044426610 was IN_PROGRESS at 15:03:23 UTC. Initial guard, immutable image-change, Auth digest promotion and TCE/Auth dispatch payload steps passed; offline dependency installation and subsequent checks had not yet completed.
- Direct master refs: Platform `1fdc57a8`; TCE `5b425bde`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision drafts remain Platform #1314/#544/#541/#539 and Auth #76.
- No workflow inventory additions/removals. Preserve all CI, test, security, build, immutable publisher, release, backup, integration, manual and scheduled workflows. No duplicate SSH/Compose production authority.
- Native schedule reference 15:03:23 UTC: Platform reconcile #42993779924 age 20,798s/gap 26,585s; inspection #42981286761 age 26,517s/gap 25,617s; recovery #42986496462 age 24,044s/gap 24,822s; watchdog #42986833403 age 23,893s/gap 24,297s; TCE WF-06 #42949191917 age 43,702s/gap 12,853s; TCE WF-12 #42996293386 age 19,725s/gap 26,503s. All age and gap budgets fail. Manual, rerun attempt 2 and workflow_run receipts do not substitute.
- Latest full K3s snapshot #42994074939 and reconciliation #43003088695 are expired. Do not use them for current health or rollout authorization. No current-master inspection/plan is present.
- Branch-protection GET remains HTTP 403 on all five repositories; repo-level rulesets are [] for public repositories and inaccessible for private Stock. Merge commit and rebase remain enabled in repository metadata. Administrator action remains required.
- No production mutation, image publication/promotion, credential rotation, destructive cleanup, host reboot or workflow removal. TCE market-scan schedule unchanged.


## Latest verification — 2026-11-11 23:09 ICT / 16:09:29 UTC

- Platform Infra master is `4cb817cba48119b04a38ba3ca1beefa579381571`. PR #1642 merged at `746596aa`; post-merge `validate-manifests` #43054650479 PASS on that parent SHA. PR #1643 merged at `4cb817c` after exact-head validation #43054831431 PASS; native inspection run #43054529460 completed SUCCESS and generated `debug/vps-latest.md` at 16:03:55Z. No post-merge manifest validation on SHA `4cb817c` is present in the run listing.
- App master refs: TCE `5b425bde`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision drafts: Platform #1314/#544/#541/#539; Authentication #76. None in TCE/Stock/Media.
- TCE WF-01 #43008514423, WF-02 #43008514481 and WF-05 #43008514459 PASS. Native WF-06 #42949191917 and WF-12 #42996293386 FAIL; WF-06 attempt 2 #43003016447 is excluded from first-attempt cadence; WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED. Four strict HTTP-200 probes returned 503 in manual diagnostic #43003071073. Keep `TCE_MAINTENANCE_MODE` unverified until an administrator reads the Actions variable.
- Stock CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Fresh K3s inspection shows desired Admin and Backend ImagePullBackOff due to missing ARM64-compatible image descriptors; legacy pods running do not provide registry RepoDigest evidence.
- Media CI #42539512417 PASS. Fresh snapshot shows backend/frontend 1/1 with registry RepoDigests; Media runner service/listener active and enabled. Remote unregister, backup/retention and DNS ownership remain unverified.
- Auth CI #42654579277 PASS. Fresh snapshot shows MicroFE Auth/Keycloak 0/0 and public OIDC 503. Historical Auth runtime Secret verification occurred on old Platform SHA `ff401dad` with values suppressed; no current-master reconciliation evidence.
- Native schedule reference 16:07:41Z: reconcile #42993779924 age 24,676s/gap 26,585s; inspection #43054529460 age 236s/gap 30,159s; recovery #42986496462 age 27,922s/gap 24,822s; watchdog #42986833403 age 27,771s/gap 24,297s; TCE WF-06 #42949191917 age 47,580s/gap 12,853s; WF-12 #42996293386 age 23,603s/gap 26,503s. All six inter-arrival budgets fail; five current-age budgets fail. No cron or TCE market-scan schedule change.
- Current snapshot: node Ready/ARM64; disk 56% (~20GiB free), ~19GiB RAM available, restart required; Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff. Preserve Bound PVC `k3s-debug/k3s-debug-logs`; do not cleanup/reboot.
- Preserve all app CI/test/security/build/immutable-publisher/release/backup/integration/manual/scheduled workflows. No workflow is confirmed obsolete or removed. No duplicate SSH/Compose production authority. Platform Infra remains the sole production apply authority.
- No current-master GitOps `mode=plan`/apply, image promotion, manifest apply or workload rollout is evidenced. No credential rotation, destructive cleanup, runner retirement, DNS/database/storage change or host reboot.

 
## Latest verification — 2026-11-12 00:06 ICT / 17:06:33 UTC

- Direct master refs: Platform Infra `e6163feea2dabaeaa9abbdc8192b1da74ea0cbb1`; TCE `5b425bdeab457e943bcecf1831836fc698e24394`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Platform PR #1644 merged at `e6163fe`; exact-head validation #43055819417 PASS and post-merge master validation #43064658676 PASS. Open owner-decision drafts: Platform #1314/#544/#541/#539 and Auth #76; none in TCE/Stock/Media.
- Preserve all app CI/test/security/build/immutable-publisher/release/backup/integration/manual/scheduled workflows. No workflow additions/removals are justified by current evidence.
- Platform manual reconciliation #43055528687 SUCCESS on parent SHA `4cb817c`, not current master. GHCR read preflight passed five packages; Auth runtime Secret provision/verification passed with values suppressed; shared `ghcr-pull` unchanged; no drift; manifest/image apply and rollout skipped. TCE/Auth remain intentional 0/0 maintenance; MicroFE active health passed. This run is beyond the 2,700s freshness budget at reference.
- Fresh K3s inspection #43054529460 generated 16:03:55Z and is within its 4,500s budget by 742s at reference. Media/MicroFE/NATS 1/1 with registry digests; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff. Preserve Bound `k3s-debug/k3s-debug-logs`; no cleanup/reboot.
- Native schedule reference 17:06:33Z: Platform reconcile #42993779924 age 28,208s/gap 26,585s; inspection #43054529460 age 3,768s/gap 30,159s; recovery #43058316157 age 2,418s/gap 29,036s; watchdog #43058640134 age 2,297s/gap 29,006s; TCE WF-06 #42949191917 age 51,112s/gap 12,853s; WF-12 #42996293386 age 27,135s/gap 26,503s. All six inter-arrival budgets fail; current-age fails for reconcile and both TCE health lanes. Watchdog failed on missing scheduled reconciliation and inter-arrival gaps; queue sample found no lane over the 15-minute queue budget. Recovery #43058737375 succeeded without duplicate dispatch because the prior manual reconciliation and native inspection were still recent at its reference.
- Branch governance remains unverified/enforced: all five master branch API records report `protected=false` and required-check enforcement off; repository metadata permits merge commit and rebase as well as squash. Effective inherited organization rulesets need administrator verification.
- Ownership remains unchanged: app repositories own tests/builds and immutable GHCR publication; Platform Infra alone owns production manifests, shared pull credentials, provenance/digest promotion, GitOps plan/apply, rollout and runtime verification.
- No new GHCR publication/promotion, current-master GitOps plan/apply, manifest change, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow is confirmed redundant/obsolete. No duplicate SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-12 01:00 ICT / 18:00:25 UTC

### Repository refs and workflow evidence

| Repository | Current master | Latest relevant evidence | Ownership / preservation |
|---|---|---|---|
| Platform Infra | `fc9318db` | Inspection PR #1646 merged; inspection #43067027719 SUCCESS. Current-master manual reconcile #43073396454 SUCCESS (no drift; manifest/image apply and rollout skipped). Latest native scheduled reconcile #43066718643 SUCCESS on parent SHA `ee5485b`. | Sole production manifests, shared GHCR pull credentials, provenance/digest promotion, GitOps plan/apply, rollout and runtime verification. Preserve native schedules, manual reconciliation, read-only inspection, recovery, watchdog, validation, backup and guarded maintenance. |
| TCE Dashboard | `5b425bde` | Native WF-06 #43073311537 FAIL on four HTTP-200 probes (503); native WF-12 #43068077606 FAIL. WF-12 workflow_run #43073350823 SUCCESS is not native delivery; WF-13 #43073377037 SKIPPED. | Owns tests/builds/immutable GHCR publication and strict public HTTP-200 health probes. Preserve WF-06, WF-12 native monitoring, WF-13 maintenance-aware fallback, integration/backup and release workflows. TCE/Auth remain 0/0 maintenance; do not weaken probes. |
| StockDividend | `b1b5e177` | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Desired Admin/Backend `12d63b4` ImagePullBackOff; legacy Backend/Frontend `23b2878` are 1/1 with registry RepoDigests, but are not evidence for desired image repair. | Owns app tests/builds/native ARM64 immutable publication only if owner reverses retirement. Preserve fail-closed scraper and gated publisher; no secret in Git/logs/chat. |
| Media Generation | `dcd69869` | CI #42539512417 PASS. Latest inspection snapshot shows backend/frontend 1/1 with registry RepoDigests; dedicated runner active/enabled. | Owns tests/builds/immutable publication. Preserve CI/release. Runner retirement requires remote unregister, backup/retention and DNS ownership evidence. |
| Authentication | `eab85fab` | CI #42654579277 PASS; Auth remains 0/0 maintenance. Current-master reconciliation provisioned/verified runtime Secret with values suppressed; HTTPS/TLS probe passed, but no live Auth workload health is asserted. | Owns Auth tests/builds/release provenance/immutable publication. Preserve CI/security/release; zero replicas and OIDC 503 are not live health. |

### Open PRs and branch governance

- Open owner-decision drafts: Platform #1314/#544/#541/#539; Auth #76. No open PRs in TCE/Stock/Media. PR #1646 (automated read-only VPS inspection snapshot) is merged at `fc9318db`.
- Repository metadata permits squash, merge commit and rebase across all five repositories. Effective inherited organization rulesets/branch protection are not established by these reads; administrator must enforce PR-only, required CI/deployment checks, force-push/deletion protection and squash-only.

### GitOps, image and runtime evidence

- Current-master manual reconciliation #43073396454: GHCR read preflight passed five packages; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; no blocked image-pull failures in MicroFE Auth/Shell/WS or TCE service/frontend; TCE release pairing `prod-v0.1.0-e75e338` passed; drift=false; manifest apply/image replacement/rollout skipped. TCE/Auth intentionally zero-replica maintenance; MicroFE active-scope health passed; Keycloak skipped.
- Latest K3s snapshot #43067027719 generated 17:19:36Z; at 18:00:25Z age 2,449s / 4,500s budget. Node Ready/ARM64, disk 56% (~20GiB free), ~19GiB RAM available, host restart required. Media/MicroFE/NATS 1/1. TCE/Auth/Keycloak 0/0; public OIDC 503. Stock desired Admin (2 pods) and Backend (1 pod) ImagePullBackOff due to missing platform-compatible manifest for tag `12d63b4`. Legacy Stock Backend/Frontend are 1/1 with old `23b2878` registry digests, not promotion evidence for desired release. Preserve PVC `k3s-debug/k3s-debug-logs`; no cleanup/reboot.
- Native schedule reference 18:00:25Z: Platform reconcile #43066718643 age 2,573s/gap 28,867s; inspection #43054529460 age 7,000s/gap 30,151s; recovery #43058316157 age 5,650s/gap 29,036s; watchdog #43058640134 age 5,529s/gap 29,006s; TCE WF-06 #43073311537 age 99s/gap 54,245s; WF-12 #43068077606 age 2,080s/gap 28,287s. All six inter-arrival budgets fail; four current-age budgets fail. Do not count manual fallback, workflow_run, repository_dispatch or rerun attempts as native schedule delivery. TCE market-scan schedule unchanged.

### Safety boundary

- No new GHCR publication/digest promotion, production manifest apply, image replacement or workload rollout. Auth runtime Secret provisioning/verification occurred; shared `ghcr-pull` remained unchanged.
- No namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow added/removed; no duplicate SSH/Compose authority. Platform Infra remains the sole production apply authority.


## Recovery API correlation resilience — 2026-11-12 06:05 ICT

PR #1657 adds bounded retry/backoff for transient GitHub HTTP 5xx responses during both recovery-controller dispatch-correlation GETs (reconcile-vps and inspect-vps). Permanent 4xx/auth failures and malformed JSON remain fail-closed. The static workflow-contract validator now asserts both paths retain this behavior. No schedule expression or deployment authority changes.

## Latest follow-up — 2026-11-12 06:10 ICT

- Current Platform master is 9d84aa020c5aacd28c56ef68d5a81a0a9acccfe2; PR #1656 was docs-only and its post-merge validate-manifests run #43117100616 passed. Reconciliation #43116379969 ran on parent SHA c0f309; the production manifest tree was unchanged by PR #1656, but do not label that run exact-current-master evidence.
- Watchdog #43116818114 (native schedule, 23:03:32Z) failed on native inter-arrival gaps. It verified 3 WF-06 and 4 WF-12 heartbeat receipts and reported no scheduled deployment lane exceeding the 15-minute queue budget. Recovery #43116883745 was a workflow_run success, not native schedule evidence.
- PR #1657 fixes transient HTTP 5xx during both recovery dispatch-correlation GETs. Previous head b94f850 passed validate-manifests #43117701360 but failed validate-github-actions #43117701372 because the tracker lacked the required Current runtime blockers section; the section is restored on the current branch head and exact-head checks must rerun before squash merge.


## Latest inventory verification — 2026-11-12 07:02 ICT / 00:02:34 UTC

### Repository ownership and current workflow evidence

- Platform Infra master `d0b79f0`; open owner-decision PRs #1314/#544/#541/#539. Sole production authority: shared GHCR pull credentials, production manifests, GitOps plan/apply, digest/provenance promotion, rollout and runtime verification.
- TCE Dashboard master `5b425bde`; no open PR. App-owned tests/builds and immutable GHCR publishers remain in place. Latest native WF-12 #43121528127 failed because the latest native WF-06 schedule #43073311537 was 341 minutes old. WF-13 #43121552311 completed as workflow_run recovery, but its log shows `TCE_MAINTENANCE_MODE` empty and fallback suppression disabled; read-only WF-06 fallback #43121575816 then failed all four strict HTTP-200 probes with HTTP 503. Do not weaken probes or alter market-scan cron.
- StockDividend master `b1b5e177`; no open PR. CI #42610360402 passed. Scheduled scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`. Desired K3s tag `12d63b4` has no ARM64-compatible manifest/RepoDigest; no promotion.
- Media Generation master `dcd69869`; no open PR. CI #42539512417 passed. K3s backend/frontend were 1/1 with immutable registry RepoDigests, but the Media self-hosted runner service and Listener remain active. No namespace deletion until runner unregister, backup/retention, DNS and protected approval gates pass.
- Authentication master `eab85fab`; open owner-decision PR #76. CI #42654579277 passed. Auth runtime Secret was provisioned/verified by Platform reconciliation with values suppressed; MicroFE Auth/Keycloak remained 0/0 maintenance in the K3s snapshot.

### Latest Platform authority evidence

- Native scheduled reconciliation #43120544165 succeeded on current Platform master `d0b79f0`, mode=apply / target=all / allow_image_changes=false. GHCR read preflight passed five packages; Auth runtime Secret was provisioned/verified; shared `ghcr-pull` unchanged; TCE release pairing passed; drift=false; manifest apply, image replacement and rollout skipped.
- Recovery repository_dispatch #43121541699 succeeded after the TCE WF-12 heartbeat and used the retry-capable recovery controller. It did not replace native schedule delivery and did not dispatch a new inspection because #43116036275 was still within the 75-minute inspection threshold at that time.
- Latest K3s snapshot #43116036275 generated 22:57:49Z; age 3,885s at reference, within 4,500s budget by 615s. Media/MicroFE/NATS 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff; host restart required; Media runner Listener present; preserve debug PVC.

### Native schedule and governance

At 00:02:34Z, all six inter-arrival gaps failed. Current-age failures: Platform recovery, Platform watchdog and TCE WF-06. Latest native runs: Platform reconcile #43120544165, inspection #43116036275, recovery #43116568507, watchdog #43116818114; TCE WF-06 #43073311537 and WF-12 #43121528127. Do not count workflow_run/repository_dispatch/manual fallback or rerun attempt 2 as native schedule delivery. Keep all cron expressions and TCE market-scan schedule unchanged.

Direct branch API returned `protected=false` on all five master branches. Preserve all useful CI, tests, security, builds, immutable publishers, release, backup, integration, manual and scheduled workflows. No workflow removal is justified. No direct SSH/Compose production authority. No new image publication/promotion, production manifest change, rollout, destructive cleanup, runner retirement, credential rotation, host reboot or DNS/database/storage mutation occurred in this checkpoint.


## Latest workflow inventory verification — 2026-11-12 08:07 ICT / 2026-11-12 01:07:20 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `deadaa4f` | #1314/#544/#541/#539 owner decisions | Manual reconcile #43127613751 SUCCESS (no drift/app/rollout); recovery #43127821037 SUCCESS; inspection #43127872524 SUCCESS; exact-head manifest validation #43128079244 PASS. Latest native reconcile #43120544165, inspection #43116036275, recovery #43116568507 and watchdog #43116818114 are stale. | Sole production manifests, shared GHCR pull credentials, GitOps plan/apply, digest/provenance promotion, rollout and runtime verification. |
| TCE Dashboard | `5b425bde` | #1038 (checks queued) | Native WF-06 #43127554403 FAIL (four HTTP 503); native WF-12 #43121528127 FAIL (stale WF-06); WF-13 #43127582309 SUCCESS but maintenance variable empty; fallback #43127603475 FAIL (four HTTP 503); WF-07 backup #43130553977 SUCCESS. | Owns app tests/builds, immutable GHCR publication, provenance and strict HTTP-200 health probes. No direct production apply. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Desired Admin/Backend `12d63b4` has no compatible platform manifest or RepoDigest. Legacy cached tags `23b2878` have no RepoDigest in the latest CRI inventory. | Owns tests/builds and immutable ARM64 publication only if retirement is reversed. Preserve fail-closed scraper and gated publisher. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; backend/frontend 1/1 with RepoDigests. Dedicated runner service active and Listener present; GitHub unregister, backup/retention and DNS evidence outstanding. | Owns tests/builds/immutable publication. Preserve CI/release; runner retirement and namespace deletion remain gated. |
| Authentication | `eab85fab` | #76 owner decision | CI #42654579277 PASS. Auth runtime Secret provisioned/verified by Platform; Auth/Keycloak 0/0 maintenance, no live workload health asserted. | Owns Auth tests/builds/release provenance/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Native schedule inventory

- At 01:07:20Z all six monitored native schedule lanes exceed both current-age and inter-arrival budgets. Manual dispatch, workflow_run, repository_dispatch, fallback and rerun attempts are not native schedule delivery.
- TCE WF-07 backup #43130553977 is a separate scheduled job and succeeded; it does not replace WF-06 or WF-12.
- Preserve all existing cron expressions, especially the TCE market-scan schedule. No schedule was changed.

### Cross-repo publication and deployment authority

- TCE, Stock, Media and Auth remain app-owned for tests/builds and immutable GHCR publication. Platform remains the sole production apply authority for manifests, shared `ghcr-pull`, GitOps promotion/reconciliation, rollout and health.
- Latest inspection shows Media and MicroFE running images with immutable registry RepoDigests. Stock desired tag `12d63b4` has no compatible manifest/RepoDigest; cached `23b2878` local image IDs are not registry provenance.
- No new image was published or promoted. No production manifest apply, image replacement or workload rollout occurred in the current evidence window.
- Preserve CI, tests, security, manual release, backup, integration and scheduled workflows. No workflow is proven redundant/obsolete; none removed. No direct SSH/Compose production authority.

### Governance and blockers

- Direct master branch GET returned `protected=false` across all five repositories. Effective inherited organization rulesets remain unverified. Admin action: PR-only, required checks, block force-push/deletion and squash-only.
- TCE PR #1038 adds an explicit warning for an unset maintenance variable without weakening health checks or changing schedule behavior. Exact-head WF-01P/WF-02/WF-05 runs are queued/in progress; do not merge until they pass.
- Stock/Media decommission remains blocked by active Media runner/Listener, unverified GitHub-side unregister, external backup/retention, authoritative DNS and protected production approval. Preserve `k3s-debug/k3s-debug-logs`.
- Host reports restart required; no reboot or package upgrade without platform approval.

## Follow-up — 2026-11-12 08:09 ICT / 2026-11-12 01:09:34 UTC

- Platform PR #1661 exact head `9ed3b122aa0c45b91a8380ab7a503d40dd363435`: validate-manifests #43132479380 PASS; PR remains open pending review of exact-head state.
- TCE PR #1038 current exact head `e718d728d531ac1c492e34a337e3fe308980a767`. Prior WF-01P #43132263903 failed on old head `8a81933f` because of an incorrect validator grep literal; corrected on new head. New WF-01P #43132521680, WF-02 #43132521802, WF-05 #43132521704 and WF-08B #43132521695 are in progress; no merge authorization yet.
- WF-08B on prior head ran only tests/payload checks; GHCR publication and production dispatch jobs were skipped on the pull_request event.
- The TCE maintenance change remains observability-only: empty variable still follows non-maintenance read-only fallback; strict HTTP 200 probes and all schedules remain unchanged.

## Latest workflow inventory verification — 2026-11-12 08:11 ICT / 2026-11-12 01:11:13 UTC

| Repository | Master SHA | Open PRs | Latest relevant runs | Ownership |
|---|---|---|---|---|
| Platform Infra | `166363e7` | #1314/#544/#541/#539 | PR #1661 merged; exact-head validate-manifests #43132612104 PASS; post-merge #43132719192 in progress. Manual reconcile #43127613751 SUCCESS/no drift/no apply; recovery #43127821037 SUCCESS; inspection fallback #43127872524 SUCCESS. Native schedule lanes remain stale. | Sole production manifests, shared GHCR pull credentials, GitOps plan/apply, digest promotion, rollout and health verification. |
| TCE Dashboard | `34f6024f` | none; PR #1038 merged | Exact-head WF-01P #43132521680, WF-02 #43132521802, WF-05 #43132521704 and WF-08B #43132521695 PASS. Post-merge WF-01 #43132696439, WF-02 #43132696403 and WF-05 #43132696349 in progress. Prior WF-06 #43127603475 four HTTP 503s; WF-13 #43127582309 empty variable. | Own tests/builds, immutable GHCR publication, provenance and strict HTTP-200 health. No direct production apply. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`; desired tag `12d63b4` lacks compatible manifest/RepoDigest. | Own tests/builds and immutable ARM64 publication only if retirement is reversed. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS; backend/frontend 1/1 with RepoDigests; runner service/Listener active. | Own tests/builds/immutable publication. Runner retirement requires unregister, backup/retention and DNS evidence. |
| Authentication | `eab85fab` | #76 owner decision | CI #42654579277 PASS; Auth runtime Secret provisioned/verified by Platform; Auth/Keycloak 0/0 maintenance. | Own Auth tests/builds/release provenance; Platform owns runtime Secret and production reconciliation. |

### Ownership and safety

- App repositories own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared GHCR pull credentials, GitOps promotion/reconciliation, rollout and health verification.
- No new image publication, digest promotion, manifest apply, image replacement or workload rollout in this verification window. No workflow removal is justified. Preserve CI/test/security/manual/release/backup/integration/scheduled jobs.
- TCE PR #1038 changes only unset-maintenance observability; empty remains non-maintenance, read-only fallback continues, strict health and cron remain unchanged. Variable was not modified.
- All six monitored native schedule lanes fail age and inter-arrival budgets. TCE WF-07 backup is not a substitute for WF-06/WF-12. TCE market-scan schedule unchanged.
- All five master branch APIs return `protected=false`; effective inherited org rulesets remain unverified. No branch policy changed.
- Stock/Media decommission remains blocked by active Media runner/Listener, unverified GitHub-side unregister, external backup/retention, authoritative DNS and protected approval. Preserve the debug PVC.
- Host restart remains required but was not performed.

## Latest workflow inventory verification — 2026-11-12 10:02 ICT / 03:02:38 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflows | Ownership / preservation |
|---|---|---|---|---|
| Platform Infra | `a2f7a49c` | #1314/#544/#541/#539 owner-decision | Master validation #43139122792 PASS. Native reconcile #43120544165 SUCCESS but stale; inspection #43116036275 SUCCESS but stale; recovery #43116568507 SUCCESS but stale; watchdog #43116818114 FAIL on freshness/inter-arrival. Manual reconcile #43127613751 SUCCESS/no drift/no apply but stale. | Sole production manifests, shared GHCR pull credentials, provenance/digest promotion, GitOps plan/apply, rollout and runtime verification. Preserve native schedules, manual plan/apply, read-only inspection, recovery, watchdog, backup, validation and guarded maintenance. |
| TCE Dashboard | `34f6024f` | none; PR #1038 merged | Master WF-01 #43132696439, WF-02 #43132696403, WF-05 #43132696349 PASS. Native WF-06 #43127554403 FAIL: four HTTP 503. Native WF-12 #43121528127 FAIL: WF-06 source 341m old, queue 0m. WF-13 #43127582309 last observed maintenance variable empty; merged PR #1038 adds an unset warning. WF-07 backup #43130553977 SUCCESS, TCE-only. | Owns app tests/builds, immutable GHCR publication, release provenance and strict HTTP-200 health probes. WF-03 manual release publisher dispatches Platform; WF-07 backup SSH is backup-only. Preserve WF-06/WF-12/WF-13, backup, integration, release and market-scan jobs. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS. Scheduled scraper #42457182511 FAIL CLOSED at missing `VNSTOCK_API_KEY` before dependency install or scrape. Desired K3s tag `12d63b4` has no compatible ARM64 manifest/RepoDigest in last snapshot; cached legacy IDs are not registry provenance. | Owns tests/builds and immutable ARM64 publication if retirement is reversed. Preserve fail-closed scraper and gated manual publisher. No Platform apply authority. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS. Last K3s snapshot showed backend/frontend 1/1 with registry RepoDigests; dedicated runner service and Listener active. | Owns tests/builds/immutable GHCR publication. WF-03 does not send Platform dispatch and does not apply workloads. Preserve CI/release; runner retirement requires remote unregister, backup/retention and DNS evidence. |
| Authentication | `eab85fab` | #76 owner-decision | auth-service-ci #42654579277 PASS. Auth runtime Secret provisioned/verified in last successful Platform reconciliation; Auth/Keycloak were 0/0 maintenance, no live workload health asserted. | Owns Auth tests/builds/release provenance/SBOM/immutable publication and exact Platform dispatch request. Platform owns runtime Secret and production reconciliation. |

### Native schedule acceptance at 03:02:38Z

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) | Acceptance |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43120544165 | 12,635 | 22,471 | 2,700 | FAIL |
| Platform inspection | #43116036275 | 14,697 | 24,826 | 4,500 | FAIL |
| Platform recovery | #43116568507 | 14,458 | 23,725 | 2,700 | FAIL |
| Platform watchdog | #43116818114 | 14,346 | 23,716 | 2,700 | FAIL |
| TCE WF-06 | #43127554403 | 9,239 | 23,393 | 1,500 | FAIL |
| TCE WF-12 | #43121528127 | 12,172 | 22,441 | 1,500 | FAIL |

All six current-age and inter-arrival budgets fail. TCE WF-07 backup #43130553977 is a separate scheduled workflow and cannot satisfy WF-06/WF-12 delivery. Watchdog diagnostics did not establish runner queue congestion. Keep all cron expressions unchanged, especially the TCE market-scan schedule.

### Cross-repo publisher / authority audit

- TCE WF-03: manual-only release; immutable-tag absence check; ARM64 digest verification; exact release-request payload; Platform repository dispatch. No direct VPS/Compose apply.
- Stock deploy.yml: manual immutable GHCR publisher with ARM64 digest verification; no Platform production apply. Scraper fail-closed credential preflight preserved.
- Media WF-03: immutable ARM64 GHCR publisher; explicitly no Platform dispatch configured; no production apply.
- Auth release.yml: manual master release with provenance/SBOM, immutable digest verification and exact Platform dispatch.
- TCE WF-07 SSH is limited to TCE backup archive; not a second deployment authority.
- Preserve all CI/test/security/build/publish/manual/release/backup/integration/scheduled workflows. No workflow is confirmed obsolete or removed. No duplicate direct SSH/Compose production apply authority.

### Runtime and governance

- Last K3s snapshot #43127872524 was generated 00:31:21Z and is stale at the current reference. It showed node Ready/ARM64, disk 56%, ~19GiB RAM available, restart required, Media/MicroFE 1/1, TCE/Auth/Keycloak 0/0, Stock desired Admin/Backend ImagePullBackOff, Media runner active/Listener present, and the debug PVC Bound (1Gi, RWO).
- Last reconciliation #43127613751 was a manual apply-mode no-drift check on parent SHA `331120b`; five GHCR reads PASS, Auth runtime Secret verified, shared `ghcr-pull` unchanged, no manifest/image apply or rollout. It is stale and not exact-current-master plan evidence.
- Rulesets GET returned `[]` for Platform/TCE/Media/Auth and 403 for Stock; branch-protection detail GET returned 403 for all five. Inherited org rulesets and required-check enforcement remain unverified. Repository metadata allows squash, merge commit and rebase.
- No new image publication/promotion, current-master GitOps plan/apply, production mutation, rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. TCE market-scan schedule unchanged.


## Post-merge receipt — 2026-11-12 10:10 ICT

- Platform PR #1665 merged by squash: `26eaa72393f9578a8ca3742f669b74f9cf1060f3` -> `7db202b643e08b6c9fd8b643758731fabba17bca`.
- Exact-head validation #43146309032 PASS; post-merge validation #43146400383 PASS on the exact master merge SHA.
- The change is documentation-only; no production manifest, workflow, image, secret, schedule or runtime state changed.
- Current Platform open PRs remain #1314/#544/#541/#539 (owner-decision drafts). Platform Infra remains the only production apply authority. TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-12 11:56 ICT / 04:56:38 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership and preservation |
|---|---|---|---|---|
| Platform Infra | `9f969fcfe0a8b31c5b612e218ea9f5a86e629059` | #1314/#544/#541/#539 owner decisions | Native reconcile #43152960974 SUCCESS on current master; native inspection #43150245172 SUCCESS; native recovery #43150505792 SUCCESS; native watchdog #43150601305 FAIL. Latest recovery #43154428142 is repository_dispatch SUCCESS, not native schedule. | Sole production manifests, shared GHCR pull credentials, GitOps plan/apply, immutable digest/provenance promotion, rollout and runtime verification. Preserve reconcile, inspect, recovery, watchdog, backup, validation and guarded manual jobs. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Native WF-12 #43154415980 FAIL: latest native WF-06 #43127554403 age 234m, queue 0m. WF-13 #43154436821 dispatched read-only fallback #43154458775; fallback failed four HTTP-200 probes with HTTP 503. | Owns tests/builds, immutable GHCR publication, provenance and strict HTTP-200 health. Preserve WF-06/WF-12/WF-13, manual release, backup, integration and market-scan jobs. No direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS; scraper #42457182511 FAIL CLOSED on missing `VNSTOCK_API_KEY`. Desired Admin/Backend tag `12d63b4` has no compatible ARM64 manifest/RepoDigest. Legacy `23b2878` running pods are not accepted as promotion provenance without registry-qualified RepoDigest. | Owns tests/builds and immutable ARM64 publication only if retirement is reversed. Preserve fail-closed scraper and gated manual publisher. No Platform apply authority. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS; last K3s snapshot backend/frontend 1/1 with RepoDigests; dedicated runner service active and Listener present. | Owns tests/builds/immutable publication. WF-03 does not dispatch Platform or apply production workloads. Runner retirement requires remote unregister, external backup/retention and DNS evidence. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner decision | CI #42654579277 PASS; Auth runtime Secret verified by Platform reconciliation; Auth/Keycloak 0/0 maintenance, no live workload health asserted. | Owns Auth tests/builds/release provenance/SBOM/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Native schedule acceptance

At 04:56:38Z all six monitored inter-arrival budgets fail; five of six current-age budgets fail. Latest native runs and exact measurements are recorded in the deployment tracker. The only lane still inside current-age budget is Platform inspection #43150245172 (4,304s against 4,500s), with 196s remaining at the reference time. TCE WF-07 backup/integration, workflow_run recovery, repository_dispatch recovery and manual fallbacks do not satisfy WF-06/WF-12 or Platform native schedule acceptance.

Current schedule definitions were read from master and left unchanged:
- Platform reconcile: `7,22,37,52 * * * *`
- Platform inspection: `2,32 * * * *`
- Platform recovery: `10,25,40,55 * * * *`
- Platform watchdog: `12,27,42,57 * * * *`
- TCE WF-06: `*/15 * * * *`
- TCE WF-12: `7,22,37,52 * * * *`

**TCE market-scan schedule unchanged.**

### Publisher and deployment-authority audit

- TCE WF-03 remains the manual immutable ARM64 release publisher and exact Platform release-request dispatcher; it does not perform direct VPS/Compose apply.
- Stock deploy remains the gated manual immutable ARM64 GHCR publisher; it does not own Platform apply. Scraper fail-closed secret preflight remains.
- Media WF-03 remains the immutable ARM64 publisher with no Platform dispatch or production apply.
- Auth release remains the manual master publisher with provenance/SBOM, immutable digest verification and exact Platform dispatch.
- TCE WF-07 SSH is backup-only, not a competing production apply authority.
- Preserve CI/test/security/build/publish/manual/release/backup/integration/scheduled workflows. No workflow is confirmed redundant/obsolete; none removed. No duplicate direct SSH/Compose production apply authority.

### Runtime and governance

- Current-master native reconciliation #43152960974 completed preflight and health checks, found drift=false and skipped manifest apply, image replacement and rollout. Auth/TCE zero-replica maintenance is not live health. Five GHCR package reads passed; Auth Secret verified; shared `ghcr-pull` unchanged.
- K3s snapshot #43150245172 / `debug/vps-latest.md` generated 03:45:02Z; at 04:56:38Z age 4,296s against 4,500s budget. Node Ready/ARM64, disk 57%, ~20GiB free, ~19GiB RAM available, restart required. Media/MicroFE active; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff; Media runner Listener present; preserve debug PVC.
- All five master branch APIs report `protected=false` and required-check enforcement off. Rulesets GET is empty for Platform/TCE/Media/Auth and 403 for Stock. Effective inherited org rulesets remain unverified; all repositories still allow squash, merge commit and rebase.
- No new image publication/promotion, manifest apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. No workflow removal. Platform Infra remains sole production apply authority.


## Post-merge receipt — 2026-11-12 12:02 ICT

- Platform PR #1670 merged by squash: exact head `145745ea3f00cadbed3b323ff92741ca0195cffc` -> master `3dd57285c86502df58128c2b392fd4bf620396f4`.
- Exact-head validation #43158559048 PASS; post-merge validation #43158638646 PASS on exact merge SHA.
- The change is documentation-only. No production manifests, workflow definitions, images, credentials, Actions variables, schedules or runtime resources changed.
- Current Platform open PRs remain #1314/#544/#541/#539 (owner-decision); Authentication #76 remains an owner-decision draft.
- Platform Infra remains the sole production apply authority. Preserve all app-owned tests/builds/immutable publishers and all useful manual/release/backup/integration/scheduled workflows. TCE market-scan schedule unchanged.


## Latest workflow inventory verification — 2026-11-12 15:59 ICT / 08:59:30 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|---|
| Platform Infra | `c6b71a37` | #1314/#544/#541/#539 drafts | Master validate-manifests #43180879007 PASS. Reconciliation #43176619995 SUCCESS via workflow_dispatch on parent `345f033a`, no drift/apply/rollout, but stale. Inspection #43173781408 SUCCESS on parent `826b9427`, but stale. Native reconcile/inspect/recovery/watchdog latest #43152960974/#43150245172/#43150505792/#43150601305. | Sole production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, rollout and runtime verification. Preserve reconcile, inspection, recovery, watchdog, backup, validation and guarded manual jobs. |
| TCE Dashboard | `34f6024f` | none | WF-06 native schedule #43176560763 FAILURE at 07:36:52Z; four strict probes HTTP 503. WF-12 #43176586474 and WF-13 #43176586309 SUCCESS via workflow_run; WF-13 #43176605608 SKIPPED. Latest native WF-12 #43154415980 is stale. WF-01/02/05 build/test checks PASS. | Owns tests/builds, immutable GHCR publication, provenance and strict health checks. Preserve WF-06/WF-12/WF-13, manual release, backup, integration and market-scan workflows. No direct production apply. |
| StockDividend | `b1b5e177` | none | CI #42610360402 PASS. Scraper #42457182511 FAIL CLOSED because `VNSTOCK_API_KEY` is missing. No new immutable publication/promotion. | Owns tests/builds and immutable ARM64 publication only if operation is authorized. Preserve fail-closed scraper and gated manual publisher. No Platform apply authority. |
| Media Generation | `dcd69869` | none | CI #42539512417 PASS. No newer publication/promotion; last inspection showed backend/frontend 1/1 with RepoDigests but is stale. Dedicated runner Listener was present in last inspection. | Owns tests/builds/immutable publication. No Platform dispatch or production apply in current publisher contract. Preserve CI/release while runner retirement is gated. |
| Authentication | `eab85fab` | #76 draft | CI #42654579277 PASS. No newer current-master release/promotion. Auth runtime Secret was provisioned/verified in the last successful Platform reconciliation; Auth/Keycloak were 0/0 maintenance in historical runtime evidence. | Owns Auth tests/builds/release provenance/SBOM/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Native schedule acceptance at 08:59:30Z

| Lane | Latest native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43152960974 | 17,382 | 16,665 | 2,700 | FAIL |
| Platform inspection | #43150245172 | 18,876 | 17,233 | 4,500 | FAIL |
| Platform recovery | #43150505792 | 18,735 | 17,135 | 2,700 | FAIL |
| Platform watchdog | #43150601305 | 18,681 | 17,077 | 2,700 | FAIL |
| TCE WF-06 | #43176560763 | 4,958 | 25,693 | 1,500 | FAIL |
| TCE WF-12 | #43154415980 | 16,597 | 16,987 | 1,500 | FAIL |

Only first-attempt `event=schedule` runs on `master` count. TCE WF-12 #43176586474 is a workflow_run heartbeat/verification and does not reset native WF-12 cadence. TCE WF-06 #43176560763 is a native schedule run, but it failed the four public health probes (HTTP 503). Platform watchdog #43150601305 recorded the inter-arrival gaps above and failed Platform native schedule acceptance. No authoritative scheduler enqueue/delivery telemetry was available; runner congestion is not established.

### Runtime freshness and ownership

- Reconciliation #43176619995: age 4,929s against 2,700s budget; expired. Five GHCR reads passed, Auth runtime Secret verified (values suppressed), shared `ghcr-pull` unchanged, TCE release pairing PASS, drift=false, apply/image replacement/rollout skipped. Run is on parent SHA `345f033a`, not current master.
- K3s inspection #43173781408 / `debug/vps-latest.md`: generated 07:14:30Z, age 6,308s against 4,500s budget; expired. Last snapshot: ARM64 node Ready, disk 57%, ~20GiB free, ~19GiB RAM available, restart required, Media runner Listener present, debug PVC Bound (1Gi/RWO).
- Last-known workload state: Media/MicroFE active; TCE/Auth/Keycloak 0/0 maintenance; Stock desired Admin/Backend ImagePullBackOff on `12d63b4`. Do not assert current health from this expired snapshot.
- App repositories own tests/builds/immutable GHCR publication; Platform Infra alone owns production manifests, shared pull credentials, digest promotion, GitOps, rollout and health.
- Preserve all useful CI/test/security/build/publisher/manual/release/backup/integration/scheduled workflows. No workflow is confirmed obsolete; none removed. No direct SSH/Compose production apply authority. No image publication/promotion, manifest apply, rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred.
- Repository metadata allows squash, merge commit and rebase; effective inherited organization rulesets/branch protection remain unverified. Open owner-decision PRs remain drafts and are not merged.

**TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 16:04 ICT / 09:04:35 UTC

- Platform PR #1680 was squash-merged from exact head `d61d9791f6ed8f4415a3ab59dd3243c7453160ca` to master `470cf1f6be68d1f68e61611792a39787003c2a1b`.
- Exact-head `validate-manifests` run [#43188151487](https://github.com/phanthienquoc/platform-infra/actions/runs/43188151487) completed SUCCESS on the exact PR head. All applicable contract, manifest-render, shell, secret, immutable-image, Keycloak-isolation and network checks passed; changed-image-reference validation was skipped because the PR is documentation-only.
- Post-merge `validate-manifests` run [#43188233039](https://github.com/phanthienquoc/platform-infra/actions/runs/43188233039) completed SUCCESS on exact merge SHA `470cf1f6be68d1f68e61611792a39787003c2a1b`. Direct `refs/heads/master` verification matched this SHA; PR #1680 is merged.
- PR #1680 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint documents. No production manifest, workflow definition, image reference, credential, Actions variable, runtime configuration, workload, DNS, database, storage or schedule changed.
- The 15:59 ICT snapshot remains an accurate evidence snapshot. Latest K3s inspection #43173781408 and reconciliation #43176619995 remain beyond their freshness budgets; this documentation merge does not refresh runtime evidence. Native schedule delivery remains degraded, and TCE WF-06 last returned four HTTP 503 probes.
- Current Platform master is `470cf1f6be68d1f68e61611792a39787003c2a1b`. TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3` and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f` remain unchanged.
- Open Platform owner-decision drafts remain #1314/#544/#541/#539; Authentication draft #76 remains open. No owner-decision PR was merged.
- No new GHCR publication/promotion, production apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**


## Latest workflow inventory verification — 2026-11-12 17:04 ICT / 10:04:47 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|---|
| Platform Infra | `466b848d9743843b48062fa53b2c9bd070fe2b09` | #1314/#544/#541/#539 drafts | Master `validate-manifests` #43188500016 PASS. Native reconcile #43152960974, inspect #43150245172, recovery #43150505792 and watchdog #43150601305 are all beyond their age/inter-arrival budgets. Latest reconciliation #43176619995 is a successful workflow_dispatch on parent `345f033a`, expired; latest inspection #43173781408 is a successful workflow_dispatch on parent `826b9427`, expired. | Sole production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, rollout and runtime verification. Preserve reconcile, inspection, recovery, watchdog, backup, validation and guarded manual jobs. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Native WF-06 #43176560763 FAILURE: four strict public probes HTTP 503. Native WF-12 #43154415980 FAILURE/stale. WF-12 #43176586474 and WF-13 #43176586309 SUCCESS via workflow_run only; they do not count as native schedule. WF-01/02/05 build/test checks PASS. | Owns tests/builds, immutable GHCR publication, provenance and strict HTTP-200 probes. Preserve WF-06/WF-12/WF-13, manual release, backup, integration and market-scan jobs. No direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS with seven successful check runs. Scraper #42457182511 FAIL CLOSED because protected `VNSTOCK_API_KEY` is absent; no newer publication/promotion evidence. | Owns tests/builds and immutable ARM64 publication only if operation is authorized. Preserve fail-closed scraper and gated manual publisher. No Platform apply authority. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. No newer current-master publication/promotion evidence. Last K3s snapshot showed backend/frontend 1/1 with registry RepoDigests but is expired; dedicated runner Listener was present. | Owns tests/builds/immutable publication. No Platform dispatch or production apply in current publisher contract. Preserve CI/release while runner retirement is gated. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 draft | CI #42654579277 PASS; build and validate checks PASS, Supabase Preview SKIPPED. No newer current-master release/promotion evidence. | Owns Auth tests/builds/release provenance/SBOM/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Native schedule delivery — reference 10:04:47Z

| Lane | Latest native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43152960974 | 21,299 | 16,665 | 2,700 | FAIL |
| Platform inspection | #43150245172 | 22,793 | 17,233 | 4,500 | FAIL |
| Platform recovery | #43150505792 | 22,652 | 17,135 | 2,700 | FAIL |
| Platform watchdog | #43150601305 | 22,598 | 17,077 | 2,700 | FAIL |
| TCE WF-06 | #43176560763 | 8,875 | 25,693 | 1,500 | FAIL |
| TCE WF-12 | #43154415980 | 20,514 | 16,987 | 1,500 | FAIL |

Only first-attempt `event=schedule` runs on `master` count. TCE WF-12 #43176586474 and WF-13 #43176586309 are workflow_run events and do not satisfy native cadence. WF-06 #43176560763 is a native schedule event but failed all four HTTP-200 probes with HTTP 503. The available integration does not expose authoritative scheduler enqueue/delivery telemetry; runner congestion is not established. Preserve existing cron expressions and budgets; **TCE market-scan schedule unchanged**.

### Current checks, runtime freshness and governance

- Platform master #43188500016: `validate` SUCCESS; failure-report job SKIPPED. All five master branch APIs report `protected=false` and required status-check enforcement `off`; inherited organization rulesets remain unverified.
- Latest successful Platform reconciliation #43176619995: workflow_dispatch on parent `345f033a`; five GHCR reads PASS, Auth runtime Secret verified with values suppressed, shared `ghcr-pull` unchanged, TCE release pairing PASS, drift=false, apply/image replacement/rollout skipped. Expired at this reference.
- Latest K3s inspection #43173781408: workflow_dispatch on parent `826b9427`; generated 07:14:22Z and expired at this reference. Last snapshot recorded node Ready/ARM64, disk 57%, ~20GiB free, ~19GiB RAM available, restart required, Media/MicroFE active, TCE/Auth/Keycloak 0/0, Stock desired Admin/Backend ImagePullBackOff, Media runner Listener present, and debug PVC Bound (1Gi/RWO). Historical only.
- App repositories retain tests/builds/immutable GHCR publication. Platform Infra alone owns production manifests, shared pull credentials, digest promotion, GitOps, rollout and health.
- Preserve all useful CI/test/security/build/publisher/manual/release/backup/integration/scheduled workflows. No workflow is confirmed obsolete; none removed. No direct SSH/Compose production apply authority. No image publication/promotion, manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred.
- Open owner-decision drafts remain unmerged. TCE market-scan schedule unchanged.


## Post-merge receipt — 2026-11-12 17:09 ICT

- PR #1682 merged by squash: exact head `51b85670f38afc02e1271778a000d0e7bb41d7a2` -> master `ff914b1f352eeb571e669e997c93bd6bfe342800`.
- Exact-head validation #43197648043 PASS (21 steps); post-merge validation #43197786121 PASS on the exact merge SHA.
- Documentation/checkpoint-only change. No production manifests, workflow definitions, images, credentials, runtime configuration or schedules changed.
- The 17:04 snapshot records repository/Actions evidence only. K3s inspection and GitOps reconciliation remain expired; native schedule delivery remains degraded.
- App repositories continue to own tests/builds/immutable GHCR publication. Platform Infra remains sole production apply authority. No workflow removed and no duplicate SSH/Compose production apply introduced. **TCE market-scan schedule unchanged.**


## Latest workflow inventory verification — 2026-11-12 18:02 ICT / 11:02:40Z

| Repository | Master SHA | Open PRs | Latest relevant workflow evidence | Ownership / preservation |
|---|---|---|---|---|
| Platform Infra | `24bdbd8d1ec120d0c460e41f50b61eb4e4974ba2` | #1314/#544/#541/#539 drafts | Master validate-manifests #43198032757 SUCCESS. Latest native reconcile #43152960974, inspection #43150245172, recovery #43150505792, watchdog #43150601305; all age/inter-arrival budgets fail. Last successful reconciliation #43176619995 is workflow_dispatch on parent `345f033a`, expired. Last inspection #43173781408 is workflow_dispatch on parent `826b9427`, expired. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, rollout and runtime verification. Preserve reconcile, inspection, recovery, watchdog, backup, validation and guarded manual jobs. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Native WF-06 #43176560763 FAILURE; all four public probes HTTP 503. Native WF-12 #43154415980 FAILURE/stale. WF-12 #43176586474 and WF-13 #43176586309 SUCCESS are workflow_run events, not native schedules. WF-07 #43173471263 scheduled integration check SUCCESS. | Owns tests/builds, immutable GHCR publication, provenance and strict HTTP-200 health. Preserve WF-06/WF-12/WF-13, manual release, backup, integration and market-scan workflows. No direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS. Scraper #42457182511 FAIL CLOSED on missing protected `VNSTOCK_API_KEY`; no newer publication/promotion evidence. | Owns tests/builds and immutable ARM64 publication only if operation is authorized. Preserve fail-closed scraper and gated manual publisher. No Platform apply authority. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS. No newer publication/promotion evidence. Last K3s snapshot showed backend/frontend 1/1 with RepoDigests but is expired; dedicated runner Listener was present in that historical snapshot. | Owns tests/builds/immutable publication. No Platform dispatch or production apply in current publisher contract. Preserve CI/release while runner retirement is gated. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 draft | CI #42654579277 SUCCESS; no newer current-master release/promotion evidence. | Owns Auth tests/builds/release provenance/SBOM/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Native schedule acceptance — reference 11:02:40Z

| Lane | Latest native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43152960974 | 24,772 | 16,665 | 2,700 | FAIL |
| Platform inspection | #43150245172 | 26,266 | 17,233 | 4,500 | FAIL |
| Platform recovery | #43150505792 | 26,125 | 17,135 | 2,700 | FAIL |
| Platform watchdog | #43150601305 | 26,071 | 17,077 | 2,700 | FAIL |
| TCE WF-06 | #43176560763 | 12,348 | 25,693 | 1,500 | FAIL |
| TCE WF-12 | #43154415980 | 23,987 | 16,987 | 1,500 | FAIL |

Only first-attempt `event=schedule` runs on `master` count. Workflow_run, repository_dispatch, workflow_dispatch, recovery and backup runs do not reset native cadence. TCE WF-06's latest native run completed but failed all four strict HTTP-200 probes. The integration does not expose authoritative scheduler enqueue/delivery telemetry; runner congestion is not established. Existing cron expressions and freshness budgets remain unchanged. **TCE market-scan schedule unchanged.**

### Governance and runtime freshness

- All five direct master branch API reads report `protected=false`; required status-check enforcement is `off`. Effective inherited organization rulesets remain unverified.
- Last successful reconciliation #43176619995: five GHCR package reads PASS, Auth runtime Secret verified with values suppressed, shared `ghcr-pull` unchanged, TCE release pairing PASS, drift=false, apply/image replacement/rollout skipped; expired and not current-master.
- Last K3s inspection #43173781408: historical ARM64 node Ready, disk 57%, ~20GiB free, ~19GiB RAM available, restart required; Media/MicroFE active; TCE/Auth/Keycloak 0/0 maintenance; Stock desired Admin/Backend ImagePullBackOff; Media runner Listener present; debug PVC Bound (1Gi/RWO). Snapshot expired; do not assert current health.
- Preserve all useful CI/test/security/build/publisher/manual/release/backup/integration/scheduled workflows. No workflow is confirmed obsolete; none removed. No direct SSH/Compose production apply authority.
- No new image publication/promotion, current-master plan/apply, image replacement, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred.

**Next owner actions:** Platform operator obtains fresh inspection and current-master plan; GitHub administrator investigates native schedule delivery and branch protection; TCE administrator confirms maintenance intent; Stock owner supplies protected scraper secret only if operation remains authorized and ARM64 digest evidence before promotion; Media owner proves runner unregister, backup/retention and DNS before decommission. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 18:08 ICT

- Platform PR #1684 exact head `51f0fca330717d6e5daf174cfa1ac4d199c146bd` was validated by #43206108133 (SUCCESS) and squash-merged to master `5608c452591e81aec0e1a09a71d9a8bb5a0627a1`.
- Post-merge validation #43206219386 completed SUCCESS on the exact merge SHA; direct master ref matched and PR #1684 is merged.
- Documentation/checkpoint-only change. No workflow, manifest, image, credential, Actions variable, runtime configuration or schedule changed.
- Current Platform master: `5608c452591e81aec0e1a09a71d9a8bb5a0627a1`. Other four application master refs remain unchanged. Owner-decision PRs remain open.
- Native schedule gaps, TCE HTTP 503 probes, Stock scraper missing-secret fail-closed and expired K3s/reconciliation evidence remain unresolved. This receipt does not refresh runtime evidence.
- No workflow removed; no duplicate SSH/Compose apply authority; no production mutation. **TCE market-scan schedule unchanged.**


## Latest workflow inventory verification — 2026-11-12 19:06 ICT / 12:06:46 UTC

| Repository | Master SHA | Open PRs | Latest run/check evidence | Workflow ownership and preservation |
|---|---|---|---|---|
| Platform Infra | `b6b6951f0a718bcee7fdf6f95e5d35858c0055f8` | #1314/#544/#541/#539 drafts | Native reconcile #43152960974 and inspection #43150245172 are stale; native recovery #43213480231 SUCCESS but gap 29,367s; native watchdog #43214581449 FAILURE with gap 29,769s. Fresh reconcile #43213499525 SUCCESS on parent `6f792622`; fresh inspection #43213776807 SUCCESS and PR #1686 merged after exact-head validation #43214035228. | Sole production manifests, shared GHCR pull credentials, digest promotion, GitOps, rollout and runtime verification. Preserve reconcile, inspection, recovery, watchdog, backup, validation, guarded manual and decommission workflows. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-06 native #43176560763 FAIL; four probes HTTP 503. WF-12 native #43154415980 stale/FAIL. WF-12 #43176586474 and WF-13 #43176586309 are workflow_run SUCCESS only. WF-07 integration schedule #43173471263 SUCCESS. | Owns tests/builds, immutable GHCR publication, provenance and strict HTTP-200 probes. Preserve WF-06/WF-12/WF-13, manual release, backup, integration and market-scan workflows. No production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS. Scraper #42457182511 FAIL CLOSED on missing protected `VNSTOCK_API_KEY`; no new publication/promotion evidence. | Owns tests/builds and immutable ARM64 publication only if authorized. Preserve fail-closed scraper and gated manual publisher. No Platform apply. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS. Fresh K3s inspection shows backend/frontend 1/1 with immutable registry RepoDigests; dedicated runner Listener still present. | Owns tests/builds/immutable publication. No Platform dispatch or production apply in current contract. Preserve CI/release while runner retirement is gated. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 draft | CI #42654579277 SUCCESS; no new current-master release/promotion. Auth/Keycloak 0/0 maintenance in fresh K3s snapshot; public OIDC 503. | Owns Auth tests/builds/release provenance/SBOM/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Workflow schedule definitions re-read from current master

| Workflow | Cron | Native acceptance budget |
|---|---|---:|
| Platform `reconcile-vps.yml` | `7,22,37,52 * * * *` | 2,700s |
| Platform `inspect-vps.yml` | `2,32 * * * *` | 4,500s |
| Platform `recover-stale-ops.yml` | `10,25,40,55 * * * *` | 2,700s |
| Platform `reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | 2,700s |
| TCE `wf-06-tce-healthcheck.yml` | `*/15 * * * *` | 1,500s |
| TCE `wf-12-tce-healthcheck-schedule-watchdog.yml` | `7,22,37,52 * * * *` | 1,500s |

Do not count workflow_run/workflow_dispatch/repository_dispatch as native schedule delivery. All six inter-arrival gaps exceed budget at the 12:06:46Z reference; only recovery and watchdog latest-run ages are currently within budget. Existing schedules are unchanged; **TCE market-scan schedule unchanged**.

### Preservation and safety

- TCE publisher, MicroFE publisher, Stock publisher, Media publisher and Auth release remain application-owned build/publication contracts; Platform receives only validated exact payloads/digests and owns production reconciliation.
- Keep fail-closed Stock scraper credential preflight; do not bypass missing `VNSTOCK_API_KEY`. Keep TCE four strict HTTP-200 probes; do not convert HTTP 503 to success or infer health from zero replicas.
- Preserve Media CI/release while its runner retirement is gated. Listener remains present; no GitHub-side unregister evidence. No workflow is confirmed redundant/obsolete; none removed.
- All five direct master branch reads report `protected=false`; effective inherited organization rulesets remain unverified. Enforce PR-only, required checks, no force-push/deletion, squash-only through GitHub administrator.
- No GHCR publication/promotion, production apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot. Auth runtime Secret was provisioned/verified by reconciliation #43213499525 with values suppressed; shared `ghcr-pull` was unchanged.

**TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 19:09 ICT / 12:09:47 UTC

- PR #1687 exact head `245811d308501ae95e6f13e5ba9553294b06ff5e` passed validate-manifests #43215253958; squash merge SHA is `f1985e354598ff074fed43267a06ac58ed8a4727`.
- Post-merge validation #43215329716 completed SUCCESS on exact current master; direct master ref matched. Documentation/checkpoint-only change; no production workflow, manifest, image, credential or schedule changed.
- Current master refs: Platform `f1985e354598ff074fed43267a06ac58ed8a4727`; TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Auth `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Native schedule gaps, TCE HTTP 503, Stock missing-secret fail-closed, Media runner retirement and branch governance remain unresolved. Runtime evidence from inspection #43213776807 and reconciliation #43213499525 is fresh at the 19:06 reference; this documentation merge does not refresh runtime evidence.
- No workflow removed, no duplicate SSH/Compose production apply authority, and no production mutation. **TCE market-scan schedule unchanged.**


## Latest verified workflow inventory — 2026-11-12 20:02 ICT / 13:02:20Z

| Repository | Master SHA | Open PRs | Latest workflow/check evidence | Ownership and preservation |
|---|---|---|---|---|
| Platform Infra | `d37c1209d84c2bab96a1ea4582fc380f47b9131e` | #1314/#544/#541/#539 owner-decision drafts | Native reconcile #43222790763 SUCCESS on current master; native inspection #43218736508 SUCCESS and PR #1689 merged; recovery dispatch #43223002456 SUCCESS; latest watchdog workflow_run #43223039574 FAILURE because native schedule gaps remain outside budgets. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps, K3s rollout and health verification. Preserve reconcile, inspection, recovery, watchdog, backup, validation, guarded manual and decommission workflows. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-06 native #43176560763 FAIL: four public endpoints HTTP 503. WF-12 #43176586474 and WF-13 #43176586309 SUCCESS are workflow_run events only. WF-07 scheduled integration #43173471263 SUCCESS. WF-01/02/05 CI/build checks PASS. | Owns tests/builds, immutable GHCR publication, provenance and strict HTTP-200 probes. Preserve WF-06/WF-12/WF-13, market-scan, manual release, backup and integration jobs. No direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS (7 checks). Scraper #42457182511 FAIL CLOSED because protected `VNSTOCK_API_KEY` is missing. K3s snapshot shows desired tag `12d63b4` without ARM64-compatible RepoDigest. | Owns app tests/builds and immutable ARM64 publication only if operation is authorized. Preserve fail-closed scraper and gated publisher. Platform owns promotion/retirement; no direct apply. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. Latest inspection records backend/frontend 1/1 with immutable RepoDigests; dedicated runner Listener remains present. | Owns app tests/builds/immutable publication. No Platform dispatch or production apply in current publisher contract. Preserve CI/release while runner retirement is gated. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 owner-decision draft | CI #42654579277 PASS; ARM64 build and validate PASS, Supabase Preview SKIPPED. No newer current-master release/promotion evidenced. | Owns Auth tests/builds/release provenance/SBOM/immutable publication. Platform owns runtime Secret and production reconciliation. |

### Native schedule freshness — reference 13:02:20Z

| Lane | Latest native run | Age (s) | Inter-arrival gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43222790763 | 251 | 31,701 | 2,700 | Age PASS / gap FAIL |
| Platform inspection | #43218736508 | 1,825 | 31,621 | 4,500 | Age PASS / gap FAIL |
| Platform recovery | #43213480231 | 3,938 | 29,367 | 2,700 | Age FAIL / gap FAIL |
| Platform watchdog | #43214581449 | 3,482 | 29,769 | 2,700 | Age FAIL / gap FAIL |
| TCE WF-06 | #43176560763 | 19,528 | 25,693 | 1,500 | Age FAIL / gap FAIL |
| TCE WF-12 | #43154415980 | 31,167 | 16,987 | 1,500 | Age FAIL / gap FAIL |

Only first-attempt `event=schedule` runs on master count. Workflow_run and workflow_dispatch recovery are separate evidence. Two Platform lanes currently meet age budgets, but all six inter-arrival gaps still fail. No authoritative scheduler enqueue/delivery telemetry is exposed; runner congestion is not established. Keep all existing cron expressions/budgets and **TCE market-scan schedule unchanged**.

### Current-master reconciliation and runtime evidence

- [Reconciliation #43222790763](https://github.com/phanthienquoc/platform-infra/actions/runs/43222790763) SUCCESS on exact current master, event=schedule, attempt 1, mode=apply, target=all. GHCR read preflight passed for five packages; Auth runtime Secret was provisioned/verified with values suppressed; shared `ghcr-pull` remained unchanged; no image-pull failures were found for MicroFE Auth/Shell/WS or TCE service/frontend; TCE release tag `prod-v0.1.0-e75e338` matched desired/live references; drift=false; manifest apply/image replacement/rollout skipped.
- MicroFE active health passed. TCE and Auth were classified as intentional zero-replica maintenance, so no live workload health is asserted. Keycloak was skipped.
- [K3s inspection #43218736508](https://github.com/phanthienquoc/platform-infra/actions/runs/43218736508) SUCCESS; snapshot generated 12:32:04Z and was within the 4,500s freshness budget at 13:02:20Z. Node Ready/ARM64; disk 57% with ~20GiB free; ~19GiB RAM available; host restart required. Media/MicroFE active; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff; Media runner Listener present; debug PVC Bound (1Gi/RWO). Both public OIDC probes returned HTTP 503 and Keycloak diagnostics timed out.
- Stock tag `12d63b4` has no ARM64-compatible RepoDigest; do not promote. Active Platform manifest tree contains no retired StockDividend/Media references. External backup/retention and authoritative DNS remain outstanding for decommission.
- All five direct master branch API reads report `protected=false`; effective inherited organization rulesets remain unverified. GitHub administrator must enforce PR-only, required checks, no force-push/deletion and squash-only.
- Preserve all useful CI/test/security/build/publisher/manual/release/backup/integration/scheduled workflows. No workflow is confirmed obsolete; none removed. No duplicate SSH/Compose production apply authority. No new image publication/promotion, manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot occurred. Auth runtime Secret provision/verification is explicitly recorded; shared `ghcr-pull` was unchanged.

**TCE market-scan schedule unchanged.**

## Post-merge receipt — 2026-11-12 20:11 ICT

- PR #1690 exact-head validation #43224655375 PASS (20 validation steps); squash merge SHA `ea90c0a786e2092be3963c0de0d0319a95faf4c9`.
- Post-merge validation #43224865472 SUCCESS on exact merge SHA; direct master ref matched.
- Documentation/checkpoint-only change; no workflow, manifest, image, credential, runtime setting or schedule changed.
- Follow-up TCE native WF-12 #43224725401 FAIL: heartbeat succeeded but WF-06 schedule age was 333m against 25m; queue wait 0m. Platform recovery #43224740384 SUCCESS via repository_dispatch after validating the TCE payload and confirming recent reconciliation/fresh inspection. These recovery events do not reset native cadence.
- Current Platform master `ea90c0a786e2092be3963c0de0d0319a95faf4c9`; TCE, Stock, Media and Auth master refs remain unchanged.
- Native schedule gaps, TCE HTTP 503/maintenance, Stock ARM64 image/secret gate, Media runner retirement and branch protection remain unresolved. No workflow removed and no production mutation. **TCE market-scan schedule unchanged.**

## Latest verified workflow inventory — 2026-11-12 21:01 ICT / 14:01:40 UTC

# Cross-repo workflow inventory checkpoint — 2026-11-12 21:01 ICT

Reference: 2026-11-12 14:01:40 UTC. Platform master at inspection: `8d0d8148c1c6febbb25b4313d3d464b7a6c72059`.

## Repository inventory

| Repository | Master SHA | Open PRs | Latest workflow evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `8d0d8148c1c6febbb25b4313d3d464b7a6c72059` | #1314/#544/#541/#539 drafts | Master validate #43225264383 SUCCESS; native reconcile #43222790763 SUCCESS, inspection #43218736508 SUCCESS, recovery #43213480231 SUCCESS, watchdog #43214581449 FAILURE | Sole production manifests, shared GHCR pull credentials, digest promotion, GitOps, rollout and health |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-06 #43176560763 native FAILURE; WF-12 #43224725401 native FAILURE; WF-13 #43224758080 workflow_run SUCCESS; fallback #43224789391 four HTTP 503 failures | App CI/tests/builds, immutable GHCR and provenance; no direct production apply |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`) | App CI/builds/immutable ARM64 publication only when authorized; Platform promotion/retirement |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; last inspection showed backend/frontend 1/1 with RepoDigests; runner Listener present | App CI/builds/immutable publication; Platform production apply; Media owner runner retirement |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 draft | CI #42654579277 SUCCESS; no newer current-master release/promotion evidenced | Auth CI/security/build/SBOM/provenance/immutable publication; Platform runtime Secret and production apply |

## Preserved workflow authorities

- Platform `reconcile-vps.yml`: sole production GitOps apply authority; scheduled `7,22,37,52 * * * *`. Image replacement remains gated by exact provenance-verified promotion dispatch.
- Platform `inspect-vps.yml`: read-only, scheduled `2,32 * * * *`; generated inspection changes go through exact-head validated PRs.
- Platform `recover-stale-ops.yml`: recovery controller, scheduled `10,25,40,55 * * * *`; validates provenance/deduplication and dispatches existing workflows only. Not a second apply authority.
- Platform `reconcile-schedule-watchdog.yml`: read-only watchdog, scheduled `12,27,42,57 * * * *`.
- TCE WF-06: strict public HTTP-200 checks, scheduled `*/15 * * * *`.
- TCE WF-12: native schedule `7,22,37,52 * * * *`, verifies WF-06 native cadence and forwards authenticated heartbeat receipts.
- TCE WF-13: workflow_run-only recovery; its fallback is not native schedule evidence.
- Preserve TCE manual/release, backup, integration and market-scan workflows; preserve app CI/test/security/publisher workflows across all repositories.

## Native schedule freshness — 14:01:40 UTC

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) |
|---|---:|---:|---:|---:|
| Platform reconcile | #43222790763 | 3,811 | 31,701 | 2,700 |
| Platform inspection | #43218736508 | 5,385 | 31,621 | 4,500 |
| Platform recovery | #43213480231 | 7,498 | 29,367 | 2,700 |
| Platform watchdog | #43214581449 | 7,042 | 29,769 | 2,700 |
| TCE WF-06 | #43176560763 | 23,088 | 25,693 | 1,500 |
| TCE WF-12 | #43224725401 | 3,085 | 31,642 | 1,500 |

All six age and inter-arrival budgets fail. Workflow_run/workflow_dispatch/repository_dispatch are excluded from native cadence. Authoritative GitHub scheduler enqueue/delivery telemetry is unavailable; runner congestion is not established. Existing schedules and budgets remain unchanged. **TCE market-scan schedule unchanged.**

## Runtime evidence

- Reconciliation #43222790763 SUCCESS on parent `d37c1209`: five GHCR reads PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing PASS; drift=false; apply/image replacement/rollout skipped. Evidence age 3,811s > 2,700s budget.
- Inspection #43218736508 SUCCESS, snapshot 12:32:04Z; age 5,376s > 4,500s budget. Last-known ARM64 node Ready, disk 57%, ~20GiB free, ~19GiB available RAM, host restart required. Media/MicroFE active; TCE/Auth/Keycloak 0/0 maintenance; Stock desired workloads ImagePullBackOff; Media runner Listener present; debug PVC Bound 1Gi/RWO. Do not assert current health.
- TCE fallback #43224789391 failed all four endpoints: TCE web/API and Auth liveness/readiness each returned HTTP 503 instead of 200. Keep probes strict.
- No new GHCR publication/promotion, production apply, workload rollout, runner retirement, credential rotation, storage/DNS/database mutation, Docker cleanup or host restart occurred.

## Governance and next actions

- Prior direct master branch API reads: all five `protected=false`; effective inherited organization rulesets unverified. GitHub administrator must enforce PR-only, required checks, no force-push/deletion and squash-only.
- TCE administrator verifies `TCE_MAINTENANCE_MODE` and replica intent.
- Stock owner provides ARM64 immutable digest/provenance and protected scraper secret only if reactivation is authorized.
- Media owner completes runner stop/disable/unregister plus Listener, backup/retention and DNS evidence before decommission.
- Platform operator obtains fresh inspection and current-master `mode=plan`; separate approval required for host restart.

No workflow is confirmed obsolete; none removed. No duplicate direct SSH/Compose apply authority. Platform Infra remains sole production apply authority. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 21:04 ICT / 14:05:33 UTC

- Platform PR #1692 exact head `8daedcfb574b430469100558b49adc9f17cf9249` passed validate-manifests [#43233496023](https://github.com/phanthienquoc/platform-infra/actions/runs/43233496023); validation job SUCCESS and failure-report job correctly SKIPPED.
- PR #1692 was squash-merged to `349936d14ff01c2b751d9a85d3dc7515467aff04`. Direct `refs/heads/master` verification matched the merge SHA.
- Post-merge validate-manifests [#43233624749](https://github.com/phanthienquoc/platform-infra/actions/runs/43233624749) completed SUCCESS on the exact merge SHA; validation job SUCCESS and failure-report job correctly SKIPPED.
- PR #1692 changed only the deployment readiness tracker, workflow inventory and two timestamped checkpoint files. No production manifest, workflow definition, image reference, credential, Actions variable, runtime configuration, workload, DNS, database, storage or schedule changed.
- Fresh 21:01 ICT evidence was added to [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497) (comment 6825808556) and [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872) (comment 6825809535).
- Current Platform master is `349936d14ff01c2b751d9a85d3dc7515467aff04`; TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3` and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f` remain unchanged.
- Native schedule cadence, TCE HTTP 503 probes, Stock missing-secret fail-closed and ARM64 image gate, Media runner retirement, branch governance and stale runtime evidence remain unresolved. No workflow was removed, no duplicate SSH/Compose apply authority was introduced and no production mutation occurred. **TCE market-scan schedule unchanged.**



## Latest verified workflow inventory — 2026-11-12 22:01 ICT / 15:01:51 UTC

| Repository | Master SHA | Open PRs | Latest run evidence | Workflow ownership/preservation |
|---|---|---|---|---|
| Platform Infra | `8a1f593de194b3ce0a6efc16c5fd3abd1f24b325` | #1314/#544/#541/#539 drafts | Validate-manifests #43234002015 SUCCESS; native reconcile #43222790763 SUCCESS; inspection #43218736508 SUCCESS; recovery #43213480231 SUCCESS; watchdog #43214581449 FAILURE. | Sole production manifest, shared GHCR pull credential, digest promotion, GitOps plan/apply, rollout and health authority. Preserve reconcile, inspect, recovery, watchdog, backup, validation, guarded manual and decommission workflows. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-12 native #43224725401 FAILURE; WF-06 native #43176560763 FAILURE; WF-13 #43224758080 workflow_run SUCCESS; manual fallback #43224789391 FAILURE (four HTTP 503 probes). | App tests/builds, immutable GHCR and provenance; strict public HTTP-200 probes. Preserve WF-06/WF-12/WF-13, WF-07, manual/release, backup, integration and market-scan workflows. No direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`). | App CI/builds and immutable ARM64 publication only if authorized; preserve fail-closed scraper and gated publisher. Platform owns promotion/retirement. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; last K3s snapshot recorded backend/frontend 1/1 with RepoDigests; runner Listener present. Snapshot is expired. | App CI/builds/immutable publication. No Platform dispatch or production apply in current contract. Preserve CI/release while runner retirement is gated. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 draft | CI #42654579277 SUCCESS; no newer current-master release/promotion evidence. | Auth CI/security/tests/build/SBOM/provenance/immutable publication; Platform owns runtime Secret and production reconciliation. |

### Native schedule definitions and current acceptance

| Workflow | Cron (unchanged) | Latest native run | Age (s) | Gap (s) | Budget (s) | Result |
|---|---|---:|---:|---:|---:|---|
| Platform reconcile | `7,22,37,52 * * * *` | #43222790763 | 7,422 | 31,701 | 2,700 | FAIL / FAIL |
| Platform inspection | `2,32 * * * *` | #43218736508 | 8,996 | 31,621 | 4,500 | FAIL / FAIL |
| Platform recovery | `10,25,40,55 * * * *` | #43213480231 | 11,109 | 29,367 | 2,700 | FAIL / FAIL |
| Platform watchdog | `12,27,42,57 * * * *` | #43214581449 | 10,653 | 29,769 | 2,700 | FAIL / FAIL |
| TCE WF-06 | `*/15 * * * *` | #43176560763 | 26,699 | 25,693 | 1,500 | FAIL / FAIL |
| TCE WF-12 | `7,22,37,52 * * * *` | #43224725401 | 6,696 | 31,642 | 1,500 | FAIL / FAIL |

Only first-attempt native `event=schedule` runs on `master` count. workflow_run/workflow_dispatch/repository_dispatch do not satisfy cadence. No authoritative scheduler enqueue/delivery telemetry is available; 0m queue observations do not prove runner congestion. Existing cron expressions and budgets remain unchanged; **TCE market-scan schedule unchanged**.

### Runtime and safety evidence

- Reconciliation #43222790763 SUCCESS on parent `d37c1209`: five GHCR package reads PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing PASS; drift=false; manifest apply/image replacement/rollout skipped. Age 7,422s exceeds 2,700s budget.
- Compare `d37c1209...8a1f593d` shows only four docs/checkpoint commits; no production manifest or workflow file changed since the last reconciliation. Current runtime is still unverified because reconciliation and inspection receipts are expired.
- Inspection #43218736508 snapshot generated 12:32:04Z; age ~8,987s exceeds 4,500s. Last-known ARM64 node Ready, disk 57%, ~20GiB free, ~19GiB RAM available; host restart required; Media/MicroFE active; TCE/Auth/Keycloak 0/0 maintenance; Stock desired workloads ImagePullBackOff; Media runner Listener present; debug PVC Bound (1Gi/RWO). Do not assert current health.
- TCE fallback #43224789391 returned HTTP 503 on TCE web/API and Auth liveness/readiness; strict HTTP-200 acceptance retained.
- All five master branch API reads report `protected=false` and required status checks off; inherited org rulesets remain unverified. GitHub administrator action required.
- Preserve all useful app CI/test/security/publisher/manual/release/backup/integration/scheduled workflows. No workflow confirmed obsolete; none removed. No duplicate SSH/Compose apply authority. No GHCR publication/promotion, manifest apply, workload rollout, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup or host reboot in this checkpoint.

### Exact next actions

1. Platform operator: fresh read-only inspection and current-master `mode=plan` on `8a1f593d`; separate approval before host restart or apply.
2. GitHub administrator: obtain authoritative schedule enqueue/delivery telemetry; enforce branch protection, required checks, no force-push/deletion and squash-only.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE` and approved replica intent; keep HTTP-200 probes strict.
4. Stock owner: ARM64 immutable digest/provenance and protected scraper secret only if reactivation is approved.
5. Media owner: stop/disable/unregister runner; prove Listener absence, GitHub unregister, backup/retention and DNS before decommission.

Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 22:06 ICT / 15:06:35 UTC

- PR #1694 `docs/cross-repo-readiness-20261112-2201-ict` was opened against Platform master `8a1f593de194b3ce0a6efc16c5fd3abd1f24b325` and validated on exact head `902aad999c1c996d74f70ad5ada89dd0df57369f`.
- Exact-head `validate-manifests` [#43244058093](https://github.com/phanthienquoc/platform-infra/actions/runs/43244058093) completed SUCCESS; validation job passed and failure-report job was correctly SKIPPED.
- PR #1694 was squash-merged with expected head SHA `902aad999c1c996d74f70ad5ada89dd0df57369f`; merge commit is `0594c8b2cdf001a7d62e711f43e75c56f74da939`. Direct `refs/heads/master` read matched this merge SHA, and PR API confirms merged=true.
- Post-merge `validate-manifests` [#43244174321](https://github.com/phanthienquoc/platform-infra/actions/runs/43244174321) completed SUCCESS on exact current master; failure-report job was correctly SKIPPED.
- PR #1694 changed only `docs/cross-repo-deployment-tracker.md`, `docs/cross-repo-workflow-inventory.md` and two timestamped checkpoint files. No production manifest, workflow definition, image reference, credential, Actions variable, runtime setting, workload, DNS, database, storage or schedule changed.
- Current Platform master: `0594c8b2cdf001a7d62e711f43e75c56f74da939`. App master refs remain TCE `34f6024f8ccec8fb3ab6688901b3557e058ddfd1`, Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, Media `dcd698699c65ba6e73f6b43838975144777131c3` and Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Native schedule gaps, TCE HTTP 503/maintenance, Stock missing-secret fail-closed and ARM64 image gate, Media runner retirement, branch governance and stale runtime evidence remain unresolved. No workflow was removed, no duplicate SSH/Compose production apply authority was introduced, and no production mutation occurred in PR #1694. **TCE market-scan schedule unchanged.**


## Latest verified workflow inventory — 2026-11-12 22:56 ICT / 15:56:36 UTC

| Repository | Master SHA | Open PRs | Latest relevant run evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `a58658292ac87e7c4fc72fc9dbb78fda4e73765c` | #1314/#544/#541/#539 (owner decisions) | Current-master push validation #43244549789 SUCCESS on exact SHA (20 applicable validation steps). Native reconcile #43222790763 SUCCESS but stale; inspection #43218736508 SUCCESS but stale; recovery #43213480231 SUCCESS but stale; watchdog #43214581449 FAILURE. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-12 native #43224725401 FAILURE; WF-06 native #43176560763 FAILURE; WF-13 #43224758080 workflow_run SUCCESS; WF-06 fallback #43224789391 FAILURE (four HTTP 503 probes). | App tests/builds, immutable GHCR publication/provenance; no direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`). | App CI/builds and immutable ARM64 publication; Platform promotion/retirement. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; last K3s snapshot recorded backend/frontend 1/1 with RepoDigests and runner Listener present, but snapshot expired. | App CI/builds/immutable publication; Platform production apply; Media owner runner retirement. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner decision) | CI #42654579277 SUCCESS; no newer current-master release/promotion evidence. | Auth CI/security/tests/SBOM/provenance/immutable publication; Platform runtime Secret and production apply. |

### Preserved workflow authorities and schedules

- Platform `reconcile-vps.yml`: sole production GitOps apply authority; schedule `7,22,37,52 * * * *`.
- Platform `inspect-vps.yml`: read-only inspection; schedule `2,32 * * * *`.
- Platform `recover-stale-ops.yml`: recovery controller; schedule `10,25,40,55 * * * *`; dispatches only existing validated workflows and is not a second apply authority.
- Platform `reconcile-schedule-watchdog.yml`: read-only watchdog; schedule `12,27,42,57 * * * *`.
- TCE WF-06: strict public HTTP-200 probes; schedule `*/15 * * * *`.
- TCE WF-12: native schedule `7,22,37,52 * * * *`; verifies WF-06 native delivery and forwards authenticated heartbeat receipts.
- TCE WF-13: workflow_run-only read-only fallback; not native schedule evidence.
- Preserve TCE manual/release, backup, integration and market-scan workflows; preserve app CI/test/security/publisher workflows across all repositories.

### Native schedule acceptance — 15:56:36 UTC

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43222790763 | 10,707 | 31,701 | 2,700 | FAIL / FAIL |
| Platform inspection | #43218736508 | 12,281 | 31,621 | 4,500 | FAIL / FAIL |
| Platform recovery | #43213480231 | 14,394 | 29,367 | 2,700 | FAIL / FAIL |
| Platform watchdog | #43214581449 | 13,938 | 29,769 | 2,700 | FAIL / FAIL |
| TCE WF-06 | #43176560763 | 29,984 | 25,693 | 1,500 | FAIL / FAIL |
| TCE WF-12 | #43224725401 | 9,981 | 31,642 | 1,500 | FAIL / FAIL |

Only first-attempt event=schedule on master counts. Push, workflow_run, workflow_dispatch and repository_dispatch do not satisfy native cadence. Authoritative GitHub scheduler enqueue/delivery telemetry is unavailable; queue wait observations do not prove runner congestion. All current workflow cron definitions were read and left unchanged. **TCE market-scan schedule unchanged.**

### Runtime, failure and governance evidence

- Reconciliation #43222790763 SUCCESS on parent `d37c1209`: five GHCR reads PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing PASS; drift=false; apply/image replacement/rollout skipped. Age 10,707s > 2,700s.
- Compare `d37c1209...a5865829` shows six commits limited to tracker/inventory/checkpoint documentation; no production manifest or workflow file changed. This is not a current runtime receipt.
- Inspection #43218736508 snapshot 12:32:04Z; age 12,272s > 4,500s. Last-known node Ready/ARM64, disk 57%, ~20GiB free, ~19GiB available RAM, host restart required; Media/MicroFE active; TCE/Auth/Keycloak 0/0 maintenance; Stock desired workloads ImagePullBackOff; Media runner Listener present; debug PVC Bound 1Gi/RWO. Do not assert current health.
- TCE fallback #43224789391 failed four independent endpoints: TCE web/API and Auth liveness/readiness each returned HTTP 503 instead of 200. Keep strict probes.
- Stock scraper #42457182511 failed closed at missing protected `VNSTOCK_API_KEY` before dependency installation or scraper execution.
- All five direct master branch reads report `protected=false`. Rulesets are empty for Platform/TCE/Media/Auth; Stock rulesets endpoint returns 403 due plan/API restriction. Detailed branch-protection reads are blocked by integration 403; inherited org policy is unverified.
- Preserve all useful CI/test/security/publisher/manual/release/backup/integration/scheduled workflows. No workflow confirmed obsolete; none removed. No duplicate direct SSH/Compose production apply authority.
- No new GHCR publication/promotion, production apply, rollout, runner retirement, credential rotation, storage/DNS/database mutation, Docker cleanup or host reboot occurred in this checkpoint.

### Exact next actions

1. Platform operator: fresh read-only K3s inspection and current-master `mode=plan` on `a5865829`; separate approval before apply or host restart.
2. GitHub administrator: authoritative schedule enqueue/delivery telemetry for six workflow IDs; enforce PR-only, required checks, no force-push/deletion and squash-only.
3. TCE administrator: verify `TCE_MAINTENANCE_MODE` and approved replica intent; preserve HTTP-200 probes.
4. Stock owner: ARM64 immutable digest/provenance and protected scraper secret only if reactivation is approved.
5. Media owner: stop/disable/unregister runner; prove Listener absence, GitHub unregister, backup/retention and DNS before decommission.

Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 23:02 ICT / 16:02:35 UTC

Platform PR #1696 was squash-merged at `fc0800db36738013298dee2b49fa2c7421916966`. Exact-head validate-manifests #43254212165 completed SUCCESS on `d65caa9a82697f579f9df63d1c6b8601d01a24a1` (21 steps); post-merge validate-manifests #43254324762 completed SUCCESS on the exact merge SHA (20 applicable steps). The failure-report job was correctly skipped in both runs.

PR #1696 changed only the deployment tracker, workflow inventory and two 22:56 ICT checkpoint files. Compare `a5865829...fc0800db` confirms no production manifest or workflow file changed. Current Platform master is `fc0800db36738013298dee2b49fa2c7421916966`; TCE `34f6024f`, Stock `b1b5e177`, Media `dcd69869`, Authentication `eab85fab`.

This receipt does not refresh runtime health: the last reconciliation and K3s inspection remain expired. No image publication/promotion, manifest apply, workload rollout, credential change, runner retirement, DNS/database/storage mutation, Docker cleanup or host restart occurred. **Platform Infra remains the sole production apply authority. TCE market-scan schedule unchanged.**


## Latest verified inventory — 2026-11-12 23:59 ICT / 16:59:26 UTC

| Repository | Master SHA | Open PRs | Latest relevant evidence | Workflow ownership |
|---|---|---|---|---|
| Platform Infra | `8979b4829d4468cac779b9cee16447cf0a5088f2` | #1314/#544/#541/#539 (owner decisions) | Inspection #43257414853 workflow_dispatch SUCCESS; reconciliation #43257038616 workflow_dispatch SUCCESS; recovery #43257327411 workflow_dispatch SUCCESS; latest native watchdog #43214581449 FAILURE. Inspection PR #1698 merged as current master; changed only debug snapshot. | Sole production manifests, shared GHCR credentials, digest promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Native WF-06 #43256916802 FAILURE (four HTTP 503 probes); WF-12 #43256963936 workflow_run SUCCESS; WF-13 #43256963860 workflow_run SUCCESS; manual WF-06 #43257006805 FAILURE. | App tests/builds, immutable GHCR publication/provenance; strict HTTP-200 checks; no production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`); K3s desired tag `12d63b4` has no ARM64-compatible manifest. | App CI/builds/immutable ARM64 publication; Platform promotion and retirement. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; backend/frontend 1/1 with immutable RepoDigests in inspection #43257414853; Media runner Listener present. | App CI/builds/immutable publication; Platform production apply; Media owner runner retirement. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner decision) | CI #42654579277 SUCCESS; Auth runtime Secret provisioned/verified in reconciliation #43257038616, values suppressed; live Auth remains zero-replica maintenance. | Auth tests/security/build/SBOM/provenance/immutable publication; Platform runtime Secret and production apply. |

### Native schedules — 16:59:26 UTC

| Lane | Latest native run | Age (s) | Gap (s) | Budget (s) | Result |
|---|---:|---:|---:|---:|---|
| Platform reconcile | #43222790763 | 14,477 | 31,701 | 2,700 | FAIL / FAIL |
| Platform inspection | #43218736508 | 16,051 | 31,621 | 4,500 | FAIL / FAIL |
| Platform recovery | #43213480231 | 18,164 | 29,367 | 2,700 | FAIL / FAIL |
| Platform watchdog | #43214581449 | 17,708 | 29,769 | 2,700 | FAIL / FAIL |
| TCE WF-06 | #43256916802 | 2,557 | 31,197 | 1,500 | FAIL / FAIL |
| TCE WF-12 | #43224725401 | 13,751 | 31,642 | 1,500 | FAIL / FAIL |

Only first-attempt `event=schedule` on master counts. workflow_run/workflow_dispatch/repository_dispatch/push are separate evidence. No authoritative scheduler enqueue/delivery telemetry is exposed; queue observations do not prove runner congestion. All cron definitions and budgets remain unchanged. **TCE market-scan schedule unchanged.**

### Runtime receipt

- Reconciliation #43257038616 SUCCESS at 16:17:28Z, event=workflow_dispatch, source SHA `e4e9a2c`, mode=apply, target=all, allow_image_changes=false. GHCR 5/5 package reads PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing PASS; drift=false; manifest apply/image replacement/rollout skipped.
- Health lanes: Auth maintenance (zero replicas; no live health asserted); MicroFE healthy (active scopes verified); TCE maintenance (zero replicas; no live health asserted); Keycloak skipped. Recovery #43257327411 SUCCESS.
- Inspection #43257414853 SUCCESS; `debug/vps-latest.md` generated 16:19:43Z, fresh within 4,500s. Node Ready/ARM64, disk 57%, ~20GiB free, ~19GiB RAM available. Media and MicroFE active workloads Running; TCE/Auth/Keycloak maintenance; Stock Admin and desired Backend ImagePullBackOff; Media runner Listener present; debug PVC Bound 1Gi/RWO; OIDC probes HTTP 503.
- Current master differs from reconciliation checkout only by `debug/vps-latest.md`; production manifest/workflow tree unchanged. No current-master mode=plan run or post-merge check-run was returned for inspection merge SHA.
- No GHCR publication/promotion, manifest apply, workload rollout, runner retirement, credential rotation, DNS/database/storage mutation, Docker cleanup, host reboot or namespace/PVC/PV deletion.

### Preservation and next actions

- Preserve Platform reconcile, read-only inspection, recovery, watchdog, validation, backup, guarded manual and decommission workflows.
- Preserve TCE WF-06/WF-12/WF-13, WF-07, manual/release, backup, integration and market-scan workflows.
- Preserve app CI/test/security/build/publisher workflows across Stock, Media and Authentication. No workflow confirmed obsolete; none removed. No duplicate direct SSH/Compose authority.
- Platform operator: current-master `mode=plan` and fresh inspection before any separate apply.
- GitHub administrator: authoritative scheduler delivery telemetry and branch protection.
- TCE administrator: maintenance variable and replica intent.
- Stock owner: ARM64 immutable digest/provenance and protected scraper secret only if reactivation is approved.
- Media owner: runner retirement, Listener absence, GitHub unregister, backup/retention and DNS evidence.

Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**


## Post-merge receipt — 2026-11-12 23:59 ICT / 17:05:40Z

- PR #1699 exact head `8ff5c0d69c4e0e4fa2c2abfc044e794c524284e1` passed [validate-manifests #43265536725](https://github.com/phanthienquoc/platform-infra/actions/runs/43265536725); 20 applicable steps passed, changed-image validation skipped for docs-only changes, failure-report skipped.
- PR #1699 squash merge: `5ad78ef37c8b82f7f268d87b3d40c4a4401bd8e1`; direct master ref and PR API confirmed merged.
- Post-merge [validate-manifests #43265741937](https://github.com/phanthienquoc/platform-infra/actions/runs/43265741937) passed on the exact merge SHA; 20 applicable steps passed.
- Changed files were tracker, workflow inventory and two 23:59 ICT checkpoint files only. No production manifest/workflow, image, secret, runtime, workload, DNS, database, storage or schedule changed.
- Current Platform master: `5ad78ef37c8b82f7f268d87b3d40c4a4401bd8e1`; app master refs unchanged. No GHCR publication/promotion, manifest apply, workload rollout, runner retirement, credential rotation, host reboot or resource deletion. **TCE market-scan schedule unchanged.**


## Latest verified inventory — 2026-11-13 00:57 ICT / 17:57:45 UTC

| Repository | Master SHA | Open PRs | Latest relevant run evidence | Ownership |
|---|---|---|---|---|
| Platform Infra | `ce810a563091da4583cf10b0de4adf302699b5c4` | #1314/#544/#541/#539 (owner decisions) | Current-master `validate-manifests` #43266087926 SUCCESS. Native reconcile #43222790763, inspection #43218736508 and recovery #43213480231 SUCCESS but stale; watchdog #43214581449 FAILURE. Last dispatch inspection #43257414853 and reconciliation #43257038616 SUCCESS but expired. | Sole production manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-06 native #43256916802 FAILURE; manual fallback #43257006805 FAILURE (four HTTP 503 probes); WF-12 #43256963936 and WF-13 #43256963860 SUCCESS via workflow_run; native WF-12 #43224725401 FAILURE. | App tests/builds, immutable GHCR publication/provenance; strict HTTP-200 checks; no direct production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`). | App CI/builds and immutable ARM64 publication; Platform promotion/retirement. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; last K3s inspection shows backend/frontend 1/1 with RepoDigests, but inspection is expired; runner Listener was present. | App CI/builds/immutable publication; Platform production apply; Media owner runner retirement. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner decision) | CI #42654579277 SUCCESS; Auth runtime Secret was provisioned/verified in historical reconciliation #43257038616, values suppressed; live Auth remained zero-replica maintenance. | Auth CI/security/tests/SBOM/provenance/immutable publication; Platform runtime Secret and production apply. |

### Preserved workflow authorities and schedules

- Platform `reconcile-vps.yml`: sole production GitOps apply authority; native schedule `7,22,37,52 * * * *`.
- Platform `inspect-vps.yml`: read-only inspection; schedule `2,32 * * * *`.
- Platform `recover-stale-ops.yml`: recovery controller; schedule `10,25,40,55 * * * *`; dispatches only existing validated workflows and is not a second apply authority.
- Platform `reconcile-schedule-watchdog.yml`: read-only watchdog; schedule `12,27,42,57 * * * *`.
- TCE WF-06: strict public HTTP-200 probes; schedule `*/15 * * * *`.
- TCE WF-12: native schedule `7,22,37,52 * * * *`; verifies WF-06 native delivery and forwards authenticated heartbeat receipts.
- TCE WF-13: workflow_run-only read-only fallback; not native schedule evidence.
- Preserve TCE market-scan, manual/release, backup and integration workflows; preserve app CI/test/security/publisher workflows across all repositories.
- All six native schedule lanes exceed both age and inter-arrival budgets at 17:57:45Z. Do not count workflow_run/workflow_dispatch/repository_dispatch/push as native schedule receipts. Authoritative scheduler enqueue/delivery telemetry remains unavailable.
- Last reconciliation #43257038616 is 6,017s old vs 2,700s budget; last inspection #43257414853 is 5,891s old vs 4,500s budget. Historical no-drift/health details are not current runtime receipts.
- TCE WF-06 and manual fallback each failed four independent HTTP-200 probes with HTTP 503. Stock scraper remains fail-closed because protected `VNSTOCK_API_KEY` is absent. Stock desired ARM64 digest/provenance is unresolved.
- All five direct master branch reads returned `protected=false`; effective inherited organization rulesets remain unverified.
- No workflow was confirmed redundant/obsolete; none removed. No duplicate direct SSH/Compose production apply authority.
- **TCE market-scan schedule unchanged.**

Last reviewed: 2026-11-13 00:57 ICT (2026-11-12 17:57:45 UTC).


## Post-merge receipt — 2026-11-13 00:57 ICT / 18:05:04Z

- PR #1701 readiness snapshot exact head `2ac7b0984f4c5f40709694061024b0db211f246f` passed [validate-manifests #43275887422](https://github.com/phanthienquoc/platform-infra/actions/runs/43275887422); failure-report skipped.
- PR #1701 squash merge: `aa77cb8386215a5e898415e111eb07b304dcde7e`; direct master ref and PR API confirmed the merge.
- Post-merge [validate-manifests #43276121039](https://github.com/phanthienquoc/platform-infra/actions/runs/43276121039) passed on the exact merge SHA.
- Changed files were tracker, workflow inventory and two 00:57 ICT checkpoint files only. No production manifest/workflow, image, secret, runtime, workload, DNS, database, storage or schedule changed.
- This post-merge validation does not refresh K3s inspection or GitOps reconciliation freshness. The latest receipts remain expired as recorded in the 00:57 snapshot.
- Current Platform master: `aa77cb8386215a5e898415e111eb07b304dcde7e`; app master refs unchanged. No GHCR publication/promotion, manifest apply, rollout, runner retirement, credential rotation, host restart or resource deletion occurred.

Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**


## Latest verified workflow inventory — 2026-11-13 01:56 ICT / 18:56:35 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow runs | Ownership |
|---|---|---|---|---|
| Platform Infra | `fbd34290fbe65f5038dafd268aeae3131590a6d1` | #1314/#544/#541/#539 (owner decisions) | Current-master validate-manifests #43276541752 SUCCESS; PR #1701/#1702 validation and post-merge checks SUCCESS. | Sole production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | WF-06 native #43256916802 FAILURE; fallback #43257006805 FAILURE (four HTTP 503 probes); WF-12 #43256963936 and WF-13 #43256963860 workflow_run SUCCESS; native WF-12 #43224725401 FAILURE. | App tests/builds and immutable GHCR publication/provenance; strict public HTTP-200 probes; no production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`). | App CI/builds and immutable ARM64 publication; Platform promotion/retirement. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; latest inspection #43257414853 is expired; runner Listener was present in that historical snapshot. | App CI/builds/immutable publication; Platform production apply; Media owner runner retirement. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner decision) | CI #42654579277 SUCCESS; Auth runtime Secret provision/verification exists only in expired reconciliation #43257038616. | Auth CI/security/tests/SBOM/provenance/immutable publication; Platform runtime Secret and production apply. |

### Preserved workflow authorities and schedules

- Platform `reconcile-vps.yml`: sole production GitOps apply authority; native schedule `7,22,37,52 * * * *`.
- Platform `inspect-vps.yml`: read-only inspection; schedule `2,32 * * * *`.
- Platform `recover-stale-ops.yml`: recovery controller; schedule `10,25,40,55 * * * *`; may dispatch only existing validated workflows and is not a second apply authority.
- Platform `reconcile-schedule-watchdog.yml`: read-only watchdog; schedule `12,27,42,57 * * * *`.
- TCE WF-06: strict public HTTP-200 probes; schedule `*/15 * * * *`.
- TCE WF-12: native schedule `7,22,37,52 * * * *`; verifies WF-06 native delivery and forwards authenticated heartbeat receipts.
- TCE WF-13: workflow_run-only read-only fallback; not native schedule evidence.
- Preserve TCE market-scan, manual/release, backup and integration workflows; preserve app CI/test/security/publisher workflows across all repositories.
- All six native lanes exceed age and inter-arrival budgets at 18:56:35Z. Only first-attempt `event=schedule` on master counts. Authoritative scheduler enqueue/delivery telemetry remains unavailable; do not infer runner congestion.
- Latest reconciliation #43257038616 is 9,547s old vs 2,700s budget; latest inspection #43257414853 is 9,412s old vs 4,500s budget. Historical no-drift and workload details are not current runtime receipts.
- TCE four-endpoint HTTP 503 failure and Stock missing-secret fail-closed behavior remain unresolved. Stock desired ARM64 immutable digest/provenance is not verified.
- Previous direct branch checks found all five master branches `protected=false`; effective inherited organization rulesets remain unverified.
- No workflow confirmed obsolete; none removed. No duplicate direct SSH/Compose production apply authority. No new publication, promotion, apply, rollout, runner retirement, credential rotation, infrastructure mutation or host restart occurred.
- **TCE market-scan schedule unchanged.**

Last reviewed: 2026-11-13 01:56 ICT (2026-11-12 18:56:35 UTC).


## Post-merge receipt — 2026-11-13 01:56 ICT

- Platform PR #1703 exact-head `validate-manifests` [#43285569883](https://github.com/phanthienquoc/platform-infra/actions/runs/43285569883) completed SUCCESS on `f3ed74e9b79c4418df23752df21b2935f3093be2`.
- PR #1703 squash merge SHA: `0c0dd217208c783972a4b5153eac2dc62247d3ad`; direct master ref and PR API confirmed exact merge.
- Post-merge `validate-manifests` [#43285684313](https://github.com/phanthienquoc/platform-infra/actions/runs/43285684313) completed SUCCESS on the exact merge SHA.
- Documentation-only change: tracker, workflow inventory and two timestamped checkpoints. No workflow, production manifest, image, credential, runtime, DNS, database, storage or schedule changed.
- Runtime freshness remains expired as of the 01:56 ICT snapshot. No publication/promotion, production apply, rollout, runner retirement, credential rotation, cleanup, host restart or resource deletion occurred.
- **TCE market-scan schedule unchanged.**


## Latest verified workflow inventory — 2026-11-13 02:56 ICT / 19:56:07 UTC

| Repository | Master SHA | Open PRs | Latest relevant workflow runs | Ownership |
|---|---|---|---|---|
| Platform Infra | `3406c0372fb2f87504d805aaed853cb50e5a5555` | #1314/#544/#541/#539 (owner decisions) | Inspection #43294800951 SUCCESS; reconciliation #43294483085 SUCCESS; watchdog #43294595071 FAILURE; recovery schedule #43294456060 SUCCESS; PR #1705 exact-head validation #43295107587 SUCCESS and PR merged. | Sole production manifests, shared GHCR pull credentials, digest promotion, GitOps plan/apply, K3s rollout and health. |
| TCE Dashboard | `34f6024f8ccec8fb3ab6688901b3557e058ddfd1` | none | Native WF-06 #43256916802 FAILURE; fallback #43295147862 FAILURE (four HTTP 503 probes); WF-12 #43295079422 workflow_run FAILURE; WF-13 #43295110348 workflow_run SUCCESS; WF-07 #43295047279 scheduled integration SUCCESS. | App tests/builds, immutable GHCR publication/provenance; strict HTTP-200 checks; no production apply. |
| StockDividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 SUCCESS; scraper #42457182511 FAIL CLOSED (missing protected `VNSTOCK_API_KEY`). | App CI/builds/immutable ARM64 publication; Platform approval-gated decommission only; no Stock production manifests in Platform. |
| Media Generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 SUCCESS; latest inspection #43294800951 shows backend/frontend 1/1 with RepoDigests; runner Listener present. | App CI/builds/immutable publication; Platform approval-gated runner/cluster retirement; no Media production manifests in Platform. |
| Authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (owner decision) | CI #42654579277 SUCCESS; Auth runtime Secret provisioned/verified in reconciliation #43294483085, values suppressed; live Auth remains zero-replica maintenance. | Auth tests/security/build/SBOM/provenance/immutable publication; Platform runtime Secret and production apply. |

### Preserved production workflow authorities

- Platform `reconcile-vps.yml`: sole production GitOps apply authority; native schedule `7,22,37,52 * * * *`.
- Platform `inspect-vps.yml`: read-only K3s inspection; schedule `2,32 * * * *`; inspection snapshots are merged through a dedicated automation PR after exact-head validation.
- Platform `recover-stale-ops.yml`: recovery controller; schedule `10,25,40,55 * * * *`; dispatches only existing validated workflows and does not own a second apply path.
- Platform `reconcile-schedule-watchdog.yml`: read-only watchdog; schedule `12,27,42,57 * * * *`.
- Platform `validate-manifests.yml`: pull-request and master validation; exact image-change contract, Auth/TCE dispatch payload tests, retired Stock/Media manifest guard, YAML/secret/image/network and rendered manifest checks.
- TCE WF-06: strict public HTTP-200 probes; schedule `*/15 * * * *`.
- TCE WF-12: native schedule `7,22,37,52 * * * *`; verifies WF-06 native delivery and sends authenticated heartbeat receipts.
- TCE WF-13: workflow_run-only read-only recovery; not native schedule evidence.
- TCE WF-07 integration and backup, manual/release, market-scan jobs remain preserved.
- Stock, Media and Authentication retain app CI/test/security/build/publisher/provenance workflows. No workflow is confirmed obsolete; none removed.

### Schedule and runtime observations

- At 19:56:07Z, six native lanes all fail inter-arrival budgets. Platform recovery/watchdog ages are fresh (268s/218s) but gaps remain 28,497s/28,091s; Platform reconcile/inspection and TCE WF-06/WF-12 remain stale. Only first-attempt `event=schedule` on master counts.
- No authoritative scheduler enqueue/delivery telemetry is exposed. Do not infer runner congestion or change cron/freshness budgets. **TCE market-scan schedule unchanged.**
- Reconciliation #43294483085 SUCCESS on source SHA `23f8aef9`, mode=apply, target=all, image changes disabled. Auth runtime Secret provisioned/verified (values suppressed); shared `ghcr-pull` unchanged; TCE release pairing passed; drift=false; manifest apply/image replacement/workload rollout skipped. TCE/Auth zero-replica maintenance; MicroFE active health passed; Keycloak skipped.
- Inspection #43294800951 generated `debug/vps-latest.md` at 19:53:51Z, fresh at the 19:56:07Z checkpoint. Node Ready/ARM64, disk 57%, ~20GiB free, ~19GiB RAM available, restart required. Media and MicroFE active workloads Running; TCE/Auth/Keycloak maintenance; Stock desired Admin/Backend ImagePullBackOff because tag `12d63b4` has no matching platform manifest; OIDC probes HTTP 503; Media runner Listener present; debug PVC Bound 1Gi/RWO.
- Current Platform master differs from reconciliation source only by `debug/vps-latest.md`; production manifest/workflow tree unchanged. No current-master mode=plan run was observed.
- TCE manual WF-06 #43295147862 failed four independent HTTP-200 probes (all HTTP 503). WF-12 #43295079422 workflow_run failed stale WF-06 verification; heartbeat dispatch succeeded; WF-13 #43295110348 succeeded. Stock scraper remains fail-closed on missing protected key.
- All five direct master branch reads report `protected=false`; inherited organization rulesets remain unverified.

### Current open decisions and next owners

1. Platform operator: fresh current-master `mode=plan`; separate approval for apply or host restart.
2. GitHub administrator: authoritative schedule enqueue/delivery telemetry and branch protection.
3. TCE administrator: maintenance variable and replica intent; strict HTTP-200 probes remain.
4. Stock owner: ARM64 immutable digest/provenance and protected scraper secret only if reactivation is approved.
5. Media owner: runner stop/disable/unregister, Listener absence, GitHub unregister, backup/retention and DNS evidence.

Platform Infra remains the sole production apply authority. **TCE market-scan schedule unchanged.**
