# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 22:03 ICT (2026-11-11 15:03:23 UTC).

This is the compact current readiness view. Historical append-only content is preserved under `docs/archive`; timestamped checkpoints remain under `docs/cross-repo-deployment-checkpoints`.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | `1fdc57a8dc098fa5fdc1749f0e11ff0714209e42` | #1314, #544, #541, #539 (draft / owner decision) | PR #1641 merged at `1fdc57a8`; exact-head validation #43035377158 PASS. Current-master `validate-manifests` #43044426610 is IN_PROGRESS; runtime inspection/reconciliation evidence remains stale. |
| phanthienquoc/TCE-dashboard | `5b425bdeab457e943bcecf1831836fc698e24394` | none | WF-01 #43008514423, WF-02 #43008514481, WF-05 #43008514459 PASS. Latest qualifying first-attempt native WF-06 #42949191917 FAIL and WF-12 #42996293386 FAIL. WF-06 attempt 2 #43003016447 is excluded from native cadence; WF-12 #43019107548 and WF-13 #43019140175 are workflow_run/SKIPPED. `TCE_MAINTENANCE_MODE` remains unverified. |
| phanthienquoc/stockdividend | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS; scheduled scraper #42457182511 FAIL CLOSED on empty `VNSTOCK_API_KEY`. Last full snapshot showed desired Admin/Backend ImagePullBackOff and legacy Backend/Frontend 1/1; runtime snapshot is stale. No publication/promotion while retirement scope remains unresolved. |
| phanthienquoc/media-generation | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS. Last full snapshot #42994074939 showed backend/frontend 1/1 with registry digest references and runner service/listener active. Snapshot is stale; remote unregister, backup/retention and DNS ownership remain unverified. |
| phanthienquoc/phanthienquoc-authentication | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft / owner decision) | CI #42654579277 PASS. Auth runtime Secret was verified in historical reconciliation #43003088695 on pre-current Platform SHA with values suppressed. Auth remains 0/0 maintenance in the last snapshot; this is not live health. |

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
