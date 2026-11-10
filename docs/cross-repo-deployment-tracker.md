# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-10 21:59 ICT (2026-11-10 14:59:54 UTC)

This is the compact current readiness view. Historical append-only content from the previous rolling tracker is preserved at docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md. Timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints/.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | be48a9daf6101d79e30b4c71c1871bb7333a371e | #1314, #544, #541, #539 (all drafts / owner decisions) | validate-manifests #42831204727 SUCCESS on this exact master SHA; all validation steps completed successfully |
| phanthienquoc/TCE-dashboard | c4602be3b0a7b624bdb9cd41519cfc70a14d92ab | none | WF-02 #42822853121 and WF-05 #42822853137 PASS on current master; WF-06 #42799497774 FAIL (four public endpoints HTTP 503); WF-12 #42795292155 FAIL |
| phanthienquoc/stockdividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | StockDividend CI #42610360402 PASS on current master; scraper #42457182511 failed closed because VNSTOCK_API_KEY was missing |
| phanthienquoc/media-generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | Media CI #42539512417 PASS on current master; production promotion remains owner/token gated |
| phanthienquoc/phanthienquoc-authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (draft / owner decision) | auth-service-ci #42654579277 PASS on current master |

Platform PR #1584 was merged as be48a9daf6101d79e30b4c71c1871bb7333a371e. Exact-head validation #42831036600 PASS. Post-merge validation #42831204727 PASS; the validate job completed all contract, shell, manifest-rendering, secret-policy, Keycloak-isolation and network-boundary steps. TCE PR #1036 remains merged as c4602be3b0a7b624bdb9cd41519cfc70a14d92ab; its regression contract requires exactly four approved public health endpoints with expected HTTP 200. WF-01's latest successful master run remains on the parent SHA, so do not describe it as a current-head check.

Open draft PRs remain unchanged: Platform #1314 (mail plan), #544 (Keycloak activation status), #541 (Keycloak database plan), #539 (central identity decision), and Authentication #76 (migration drift investigation). They have no legacy commit-status contexts and remain draft/owner-decision items. Do not merge them without the relevant owner decision and side-effect review.

## Native schedule freshness

Reference time: 2026-11-10 14:59:54 UTC. Only first-attempt event=schedule runs on master count. Manual, push, workflow_run and repository_dispatch events are excluded.

| Lane | Latest native run | Result / created UTC | Current age (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile | #42778829676 | success / 07:56:31 | 25403 | 25539 | 2700 |
| Platform inspection | #42809278936 | success / 11:39:41 | 12013 | 29694 | 4500 |
| Platform recovery | #42777251549 | success / 07:43:14 | 26200 | 26068 | 2700 |
| Platform watchdog | #42777386082 | failure / 07:44:22 | 26132 | 25992 | 2700 |
| TCE WF-06 | #42799497774 | failure / 10:28:55 | 16259 | 27892 | 1500 |
| TCE WF-12 | #42795292155 | failure / 09:59:25 | 18029 | 27790 | 1500 |

All six current ages and inter-arrival gaps exceed their unchanged budgets. No newer native schedule run appeared in the current Actions API query. Configured schedules remain unchanged: Platform reconcile 7,22,37,52; inspection 2,32; recovery 10,25,40,55; watchdog 12,27,42,57; TCE WF-06 every 15 minutes; TCE WF-12 at 7,22,37,52. Do not change any cron, freshness budget, strict health threshold or TCE market-scan schedule.

## Current actions

1. Issue #1497 — GitHub administrator must provide enqueue, delivery and Actions service telemetry for the six affected schedule workflows. Repository run history cannot establish whether GitHub delayed, dropped or failed to enqueue events. Require consecutive native runs within the existing budgets before closing.
2. Issue #1575 — administrator must verify effective inherited rulesets and required-check enforcement. Branch API metadata currently reports protected=false for all five master branches; rulesets reads previously returned HTTP 403, so inherited coverage remains unknown. Do not infer that no organization ruleset exists.
3. Issue #872 — TCE/Auth owners must diagnose and recover runtime health with approved immutable digests, rollback references and no unintended database migration. Keep HTTP 200 as the only healthy public response. TCE/Auth/Keycloak zero replicas are maintenance, not healthy service.
4. Stock issue #42 — Stock owner must provision VNSTOCK_API_KEY through repository/organization secrets and run the scraper with preflight_only=true before any ingestion. Never put the key in Git, logs, artifacts or chat.
5. Stock issue #43 — owner must approve the current source release and enable the manual production gate only for an approved run. Publish scraper/admin/backend linux/arm64 images using the existing immutable full-SHA and version+SHA contract, verify per-component digest equality, then hand admin/backend digests to Platform. Never overwrite historical tag 12d63b4.
6. Media production promotion remains blocked pending an authorized PLATFORM_INFRA_AUTOMATION_TOKEN and owner approval. Media runner retirement additionally requires remote unregister, backup/retention and DNS ownership evidence.
7. Platform operator must obtain a fresh read-only K3s inspection before any runtime decision and separately approve host maintenance/restart. TCE owner must verify the SSH host fingerprint before any SSH-based maintenance.
8. Preserve the current production ownership boundary: app repositories own tests/builds and immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health verification.

## Current runtime blockers

- Latest full read-only K3s inspection is #42809278936; its snapshot was generated at 11:39:49 UTC. At the 14:59:54 UTC reference it is 12005 seconds old, beyond the 4500-second inspection freshness budget. Treat every workload value below as last-known only, not live health.
- Latest reconciliation #42809629336 completed at 11:42:17 UTC and is 11857 seconds old, beyond the 2700-second reconciliation evidence budget. It reported GHCR read preflight success, Auth runtime Secret provision/verification with values suppressed, shared ghcr-pull unchanged, DRIFT=false and correctly skipped production apply/image replacement/rollout. This does not prove current cluster health.
- Last-known K3s inventory: ARM64 node Ready; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and desired Backend ImagePullBackOff on historical ARM64-incompatible tag 12d63b4; public OIDC last observed HTTP 503; Media runner service/listener active; host restart required. These observations are stale and must not authorize rollout, restart, deletion or retirement.
- TCE WF-06 #42799497774 logs independently show TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 while expected_status remained 200. The strict contract is correct; runtime recovery is still outstanding.
- Stock scraper remains fail-closed on missing VNSTOCK_API_KEY. The historical Stock ARM64 pull failure is not evidence that the shared GHCR credential is invalid.
- GHCR tag absence guards, SHA tags and digest equality do not prove registry-side immutable-tag enforcement. Registry-side policy remains unverified.

## Current deployment authority and safety

- App repositories own CI/tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health.
- reconcile-vps.yml remains the sole production apply authority. inspect-vps.yml remains read-only.
- Preserve purposeful CI, test, security, manual, release, backup and scheduled workflows. No workflow has been confirmed redundant/obsolete.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, runner retirement, shared credential rotation, DNS/database/storage mutation or host maintenance occurred in this checkpoint.
- The last approved reconciliation provisioned/verified the Auth runtime Secret with values suppressed; shared ghcr-pull was unchanged.
- TCE market-scan schedule unchanged.

## Historical evidence

- Previous full rolling tracker preserved at docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md.
- Timestamped deployment checkpoints: docs/cross-repo-deployment-checkpoints/.
- Workflow ownership and file inventory: docs/cross-repo-workflow-inventory.md.
- Schedule investigation: https://github.com/phanthienquoc/platform-infra/issues/1497
- TCE/Auth recovery: https://github.com/phanthienquoc/platform-infra/issues/872
- Branch governance: https://github.com/phanthienquoc/platform-infra/issues/1575
- Stock scraper credential: https://github.com/phanthienquoc/stockdividend/issues/42
- Stock ARM64 release: https://github.com/phanthienquoc/stockdividend/issues/43
