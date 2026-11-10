# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 06:08 ICT (2026-11-10 23:08:55 UTC).

This is the compact current readiness view. Historical append-only content is preserved under docs/archive; timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 8b11d6629863b90536066d4e134a089b69dd6182 | #1314, #544, #541, #539 (draft / owner decision); #1603 (push-scope docs isolation, checks pending) | PR #1601 merged at 72ed11ef; PR #1602 inspection checkpoint merged at 8b11d662. Fresh read-only inspection #42920320410 passed at 23:05:16Z; current K3s state and workload evidence recorded below. |
| phanthienquoc/TCE-dashboard | c4602be3b0a7b624bdb9cd41519cfc70a14d92ab | none | Backend tests #42822853137 passed. Manual WF-06 #42915762180 failed all four approved endpoints at HTTP 503 (expected 200); native WF-06 #42872071366 and WF-12 #42915709227 failed. |
| phanthienquoc/stockdividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 passed all seven jobs, including non-publishing ARM64 builds and release-hold contract. Scraper schedule #42457182511 failed closed because VNSTOCK_API_KEY was absent. No production publisher run or digest handoff. |
| phanthienquoc/media-generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 passed. Fresh inspection #42920320410 shows backend/frontend 1/1 and digest-pinned; dedicated runner service/listener remains active. |
| phanthienquoc/phanthienquoc-authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (draft / owner decision) | Auth CI #42654579277 passed; Supabase Preview intentionally skipped. Fresh inspection #42920320410 shows Auth 0/0 maintenance and public OIDC HTTP 503; not live health. |

## Open PRs and exact-head checks

- Platform #1314: head db152c9a; validate PASS; draft mail-service plan remains owner decision.
- Platform #544: head c95e7dae; validate PASS; draft Keycloak activation status remains owner decision.
- Platform #541: head b8f7c6ba; validate PASS; draft Keycloak database change remains owner decision and side-effect gated.
- Platform #539: head 2dc48b97; validate PASS; draft central identity architecture remains owner decision.
- Authentication #76: head f19cacb0; validate PASS; Supabase Preview skipped; migration drift investigation remains owner decision.
- Platform #1603: dedicated push-scope fix branch; validation pending. No open PRs in TCE, Stock or Media. Do not merge owner-decision drafts solely because CI passes.

## Recent Platform changes

- Direct Git ref reads confirm current master SHAs: Platform `8b11d6629863b90536066d4e134a089b69dd6182`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1601 merged as `72ed11efd7af00f45e5cf047f9919525f56aed25`. Exact-head checks #42920076768 (lint), #42920076924 (manifest validation) and #42920077652 (Keycloak CI) passed; post-merge #42920184484, #42920184389 and #42920184623 passed.
- PR #1602 merged as `8b11d6629863b90536066d4e134a089b69dd6182`; it updates only `debug/vps-latest.md` from read-only inspection #42920320410.
- Push reconciliation [#42920184478](https://github.com/phanthienquoc/platform-infra/actions/runs/42920184478) succeeded but exposed an unintended path-classification side effect: `platform/keycloak/README.md` was classified as a Keycloak workload change, selected `auth-shutdown`, applied `platform/keycloak`, and executed `kubectl scale deployment/microfe-auth deployment/keycloak --replicas=0`. It verified no matching pods remained. Prior inspection reported Auth/Keycloak 0/0, but this run did not capture a pre-scale replica snapshot; do not infer the exact state transition. Recovery workflow #42920264478 then dispatched the read-only inspection #42920320410.
- New PR [#1603](https://github.com/phanthienquoc/platform-infra/pull/1603) excludes Keycloak Markdown from reconcile/recovery push triggers, classifies it as documentation, and makes resolver-only edits fail closed instead of forcing cluster-wide reconciliation. Validation is pending on the final head.
- Current master is unchanged by PR #1603; its base is exact `8b11d662`. The latest full inspection at 23:05:16Z is fresh and records current host, K3s, pod, image, storage and runner evidence.

## Native schedule freshness

Reference time: 2026-11-10 23:08:55 UTC (2026-11-11 06:08:55 ICT). Only first-attempt `event=schedule` runs on master count.

| Lane | Latest native run | Previous native run | Result / created UTC | Current age (s) | Inter-arrival gap (s) | Budget (s) |
|---|---:|---:|---|---:|---:|---:|
| Platform reconcile | #42909757881 | #42854065227 | success / 21:55:56 | 4379 | 19941 | 2700 |
| Platform inspection | #42887151366 | #42809278936 | success / 19:37:38 | 12677 | 28677 | 4500 |
| Platform recovery | #42906791198 | #42848981485 | success / 21:37:08 | 5507 | 20656 | 2700 |
| Platform watchdog | #42908417737 | #42850178931 | failure / 21:47:23 | 4892 | 20852 | 2700 |
| TCE WF-06 | #42872071366 | #42799497774 | failure / 18:08:09 | 18046 | 27554 | 1500 |
| TCE WF-12 | #42915709227 | #42867304730 | failure / 22:33:49 | 2106 | 17617 | 1500 |

All six current-age budgets and all six inter-arrival budgets are exceeded. WF-12 failed because its native WF-06 source is stale; its heartbeat/recovery events do not substitute for native WF-06 delivery. No new native scheduled run was found in the current run-list scan.

Do not change cron, freshness budgets, strict HTTP 200 health thresholds or TCE market-scan scheduling to hide delivery gaps.

## Current runtime blockers

- Fresh full read-only inspection [#42920320410](https://github.com/phanthienquoc/platform-infra/actions/runs/42920320410) generated `debug/vps-latest.md` at 23:05:16Z; age 219s at the 23:08:55Z reference, within the 4500s budget.
- Host: ARM64 Ubuntu 22.04.5, uptime 193 days, RAM 23 GiB total / 19 GiB available, root disk 45 GiB with 20 GiB free (56% used), `restart_required=yes`. Updates include kernel, containerd and Docker; no restart or package upgrade was performed.
- K3s node `tce-k3s-01` Ready, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2. Full snapshot includes current workloads and image IDs/digests.
- Media backend/frontend 1/1 and digest-pinned; MicroFE Shell/WS/NATS 1/1. TCE frontend/service 0/0; Auth and Keycloak 0/0. Public OIDC discovery for both `master` and `mrcute` realms returns HTTP 503.
- Stock Admin has two 0/1 ImagePullBackOff pods; desired Backend has one 0/1 ImagePullBackOff pod on historical `12d63b4`, with kubelet error `no match for platform in manifest`. Legacy Backend and Frontend remain 1/1 on `23b2878`; their local image IDs are not a substitute for a publisher registry digest.
- Inspection confirms Media runner service/listener active and enabled. GitHub runner registration is not inferred by host inspection. Remote unregister, backup/retention and authoritative DNS ownership remain unverified.
- Storage preflight is `storage-clean`: no Stock/Media PVCs or VolumeSnapshot references; the separate `k3s-debug/k3s-debug-logs` PVC remains bound. This does not authorize namespace or workload deletion.
- Inspection reports GitOps drift clean. GHCR image refs for Media and MicroFE are digest-pinned; Stock Admin/desired Backend remain unpullable. Server-side GHCR immutable-tag enforcement remains unverified.
- Reconciliation #42915749236 (22:34:27Z) previously verified GHCR read access for five packages, Auth runtime Secret with values suppressed, shared `ghcr-pull` unchanged, and TCE desired/live pairing; no manifest apply or image replacement was needed. This is older than the latest inspection.

## Current actions

1. [Issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497): GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for all six schedule workflows. At 23:08:55Z all six current-age and inter-arrival gaps exceed budget; WF-12 failed because WF-06 is stale.
2. [Issue #872](https://github.com/phanthienquoc/platform-infra/issues/872): TCE/Auth owners must diagnose HTTP 503 and provide approved immutable release digests, rollback references and explicit recovery approval. Platform operator must continue read-only inspection and obtain separate host maintenance approval before restart/upgrade.
3. [Issue #1575](https://github.com/phanthienquoc/platform-infra/issues/1575): Last verified branch metadata reported protected=false for all five master branches; branch-protection detail GET returned 403 and effective inherited rulesets remain unverified. GitHub administrator must confirm PR-only, required checks, force-push and deletion protections.
4. [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42): Stock owner must provision VNSTOCK_API_KEY through repository/organization secrets and run preflight_only=true before ingestion. Never place the key in Git, logs, artifacts or chat.
5. [Stock issue #43](https://github.com/phanthienquoc/stockdividend/issues/43): Stock owner must approve a source release and explicitly enable the manual publisher gate. Native ARM64 publisher and non-publishing CI builds exist, but no production publication or digest handoff exists. Never overwrite historical tags.
6. Media promotion remains blocked pending an authorized PLATFORM_INFRA_AUTOMATION_TOKEN and owner approval. Runner retirement additionally requires remote unregister evidence, backup/retention and DNS ownership evidence.
7. Registry administrator must verify GHCR server-side immutable-tag policy. TCE owner must verify SSH host fingerprint before any SSH-based maintenance.

## Current deployment authority and safety

- App repositories own application tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- `reconcile-vps.yml` remains the single production apply authority; `inspect-vps.yml` remains read-only.
- PR #1601 is merged at `72ed11ef`; manual `allow_image_changes` input is removed. Only the provenance-verified `gitops-promoted-ready` repository dispatch can bypass the workload image guard. PR #1603 is pending to keep Keycloak Markdown and resolver-only edits out of production push scope.
- Push reconcile #42920184478 did execute the narrow Auth/Keycloak scale-to-zero command after misclassifying a Keycloak README change; the run verified no matching pods remained. No shared production manifest apply, image replacement, new GHCR publication, digest promotion, namespace/PVC/PV deletion, Media runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. PR #1603 prevents this docs-only path from selecting a workload.
- Preserve useful CI/test/security workflows and purposeful manual/release/scheduled jobs. No workflow was removed or confirmed redundant/obsolete.
- TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only tracker preserved at docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md.
- Previous full append-only workflow inventory preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md.
- Timestamped deployment checkpoints: docs/cross-repo-deployment-checkpoints/.
- Workflow ownership and file inventory: docs/cross-repo-workflow-inventory.md.
- Schedule investigation: https://github.com/phanthienquoc/platform-infra/issues/1497
- TCE/Auth recovery: https://github.com/phanthienquoc/platform-infra/issues/872
- Branch governance: https://github.com/phanthienquoc/platform-infra/issues/1575
- Stock scraper credential: https://github.com/phanthienquoc/stockdividend/issues/42
- Stock ARM64 release: https://github.com/phanthienquoc/stockdividend/issues/43
