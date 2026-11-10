# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 00:11 ICT (2026-11-10 17:11:58 UTC)

This is the compact current readiness view. Historical append-only content from the previous rolling tracker is preserved at docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md. Timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints/.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | bfd0ea66ee005bd47b4dbcc85ced6428d78d9f44 | #1314, #544, #541, #539 (all drafts / owner decisions) | PR #1588 merged; exact-head validate-github-actions #42862175393 and validate-manifests #42862174503 PASS on head 3faf1a73; post-merge push checks not observable via PR-only run reader |
| phanthienquoc/TCE-dashboard | c4602be3b0a7b624bdb9cd41519cfc70a14d92ab | none | WF-02 #42822853121 and WF-05 #42822853137 PASS on current master; WF-06 #42799497774 FAIL (four public endpoints HTTP 503); WF-12 #42795292155 FAIL |
| phanthienquoc/stockdividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | StockDividend CI #42610360402 PASS on current master; scraper #42457182511 failed closed because VNSTOCK_API_KEY was missing |
| phanthienquoc/media-generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | Media CI #42539512417 PASS on current master; production promotion remains owner/token gated |
| phanthienquoc/phanthienquoc-authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (draft / owner decision) | auth-service-ci #42654579277 PASS on current master |

Platform PR #1584 was merged as be48a9daf6101d79e30b4c71c1871bb7333a371e; its exact-head and post-merge validation passed. The latest Platform master commit is inspection-only PR #1586, merged as f8743521ffb578c46abdc95dc56fc8bed028f114. Inspection #42849443955 succeeded from parent master 801a6821 and created the snapshot; exact inspection-head validation #42849732813 passed on PR head 19ba9510 before squash merge. No production manifest was changed by #1586, and no post-merge validate-manifests run on f8743521 was observed. TCE PR #1036 remains merged as c4602be3b0a7b624bdb9cd41519cfc70a14d92ab; its regression contract requires exactly four approved public health endpoints with expected HTTP 200. WF-01's latest successful master run remains on the parent SHA, so do not describe it as a current-head check.

Open draft PRs remain unchanged: Platform #1314 (mail plan), #544 (Keycloak activation status), #541 (Keycloak database plan), #539 (central identity decision), and Authentication #76 (migration drift investigation). They have no legacy commit-status contexts and remain draft/owner-decision items. Do not merge them without the relevant owner decision and side-effect review.

## Native schedule freshness

Reference time: 2026-11-10 17:11:58 UTC. Only first-attempt event=schedule runs on master count. The connected workflow-run reader exposes PR-triggered runs only; ages below are for the last-confirmed native events from the 15:57:57Z inventory and cannot prove that no later event occurred. Manual, push, workflow_run and repository_dispatch events are excluded.

| Lane | Last-confirmed native run | Result / created UTC | Age of last-confirmed run (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile | #42778829676 | success / 07:56:31 | 33327 | 25539 | 2700 |
| Platform inspection | #42809278936 | success / 11:39:41 | 19937 | 29694 | 4500 |
| Platform recovery | #42848981485 | success / 15:52:52 | 4746 | 29378 | 2700 |
| Platform watchdog | #42777386082 | failure / 07:44:22 | 34056 | 25992 | 2700 |
| TCE WF-06 | #42799497774 | failure / 10:28:55 | 24183 | 27892 | 1500 |
| TCE WF-12 | #42795292155 | failure / 09:59:25 | 25953 | 27790 | 1500 |

All six inter-arrival gaps in the last-confirmed inventory exceed their unchanged budgets. At 17:11:58Z, all six last-confirmed event ages also exceed their budgets; Platform recovery's last-confirmed run #42848981485 is 4746s old and its 29378s inter-arrival gap exceeds the 2700s budget. These are last-confirmed ages, not proof that no later native event exists. Inspection #42849443955 is workflow_dispatch and does not refresh the inspection schedule lane; watchdog observer #42849104532 is workflow_run and does not count. The connected run reader cannot query later non-PR schedule events. Configured schedules remain unchanged: Platform reconcile 7,22,37,52; inspection 2,32; recovery 10,25,40,55; watchdog 12,27,42,57; TCE WF-06 every 15 minutes; TCE WF-12 at 7,22,37,52. Do not change any cron, freshness budget, strict health threshold or TCE market-scan schedule.

## Current actions

1. Issue #1497 — GitHub administrator must provide enqueue, delivery and Actions service telemetry for the six affected schedule workflows. Native recovery run #42848981485 succeeded at 15:52:52Z, but its 29378s inter-arrival gap still fails; the other five native lanes remain stale. Repository run history cannot establish whether GitHub delayed, dropped or failed to enqueue events. Require consecutive native runs within the existing budgets before closing.
2. Issue #1575 — administrator must verify effective inherited rulesets and required-check enforcement. Branch API metadata currently reports protected=false for all five master branches; rulesets reads previously returned HTTP 403, so inherited coverage remains unknown. Do not infer that no organization ruleset exists.
3. Issue #872 — TCE/Auth owners must diagnose and recover runtime health with approved immutable digests, rollback references and no unintended database migration. Keep HTTP 200 as the only healthy public response. TCE/Auth/Keycloak zero replicas are maintenance, not healthy service.
4. Stock issue #42 — Stock owner must provision VNSTOCK_API_KEY through repository/organization secrets and run the scraper with preflight_only=true before any ingestion. Never put the key in Git, logs, artifacts or chat.
5. Stock issue #43 — owner must approve the current source release and enable the manual production gate only for an approved run. Publish scraper/admin/backend linux/arm64 images using the existing immutable full-SHA and version+SHA contract, verify per-component digest equality, then hand admin/backend digests to Platform. Never overwrite historical tag 12d63b4.
6. Media production promotion remains blocked pending an authorized PLATFORM_INFRA_AUTOMATION_TOKEN and owner approval. Media runner retirement additionally requires remote unregister, backup/retention and DNS ownership evidence.
7. Platform operator has a fresh read-only K3s inspection #42849443955 generated at 15:55:38Z; use it only while within the 4500s evidence budget, and separately approve host maintenance/restart. TCE owner must verify the SSH host fingerprint before any SSH-based maintenance.
8. Preserve the current production ownership boundary: app repositories own tests/builds and immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health verification.

## Current runtime blockers

- Latest completed full read-only K3s inspection remains #42849443955, generated at 15:55:38 UTC. At 17:11:58Z it is 4580 seconds old, beyond the 4500-second inspection freshness budget. Rerun attempt 2 passed the host inspection and output validation but failed during the local remote-tracking ref update; PR #1588 merged the fix. A post-merge push-triggered inspection is not yet confirmed, so all K3s details below are last-known only.
- Latest reconciliation #42849053816 completed at 15:55:16 UTC; at 17:11:58Z it is 4602 seconds old, beyond the 2700-second evidence budget. Its logs verify GHCR read access to Auth, MicroFE Shell/WS and TCE web/service packages; Auth runtime Secret provision/verification with values suppressed; shared ghcr-pull unchanged; DRIFT=false; production apply, image replacement and rollout skipped. TCE and Auth lanes explicitly reported intentional zero-replica maintenance with no live health asserted; active MicroFE Shell/WS health passed. This is last-known evidence, not current runtime health.
- Last-known K3s inventory at 15:55:38Z: ARM64 node Ready; disk 56% with about 20 GiB free and RAM available about 19 GiB; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; TCE frontend/service, Auth and Keycloak 0/0 maintenance; Stock Admin 0/1 (two pods ImagePullBackOff/ErrImagePull) and desired Backend 0/1 on historical ARM64-incompatible tag 12d63b4, while the existing Backend and Frontend pods remain 1/1; both public OIDC discovery probes return HTTP 503; Media and Platform runner services/listeners are active; host reports restart_required=yes. This stale snapshot does not authorize rollout, restart, deletion or retirement.
- TCE WF-06 #42799497774 logs show TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 while expected_status remained 200; the last-known inspection #42849443955 independently confirmed both public OIDC discovery probes returned HTTP 503. The strict HTTP 200 contract is correct; TCE/Auth/Keycloak remain 0/0 maintenance and runtime recovery is outstanding.
- Stock scraper remains fail-closed on missing VNSTOCK_API_KEY. The historical Stock ARM64 pull failure is not evidence that the shared GHCR credential is invalid.
- GHCR tag absence guards, SHA tags and digest equality do not prove registry-side immutable-tag enforcement. Registry-side policy remains unverified.

## Current deployment authority and safety

- Platform PR #1587 merged as `ec8b91f1fb9c66740562d50cc73c4b68c6cb8422`; PR #1588 merged as `bfd0ea66ee005bd47b4dbcc85ced6428d78d9f44`. Exact-head validation for #1588 passed in both `validate-github-actions` #42862175393 and `validate-manifests` #42862174503. Post-merge push workflow results are not exposed by the connected PR-only run reader.

- App repositories own CI/tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health.
- reconcile-vps.yml remains the sole production apply authority. inspect-vps.yml remains read-only.
- Preserve purposeful CI, test, security, manual, release, backup and scheduled workflows. No workflow has been confirmed redundant/obsolete.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, runner retirement, shared credential rotation, DNS/database/storage mutation or host maintenance occurred in this checkpoint.
- Latest reconciliation #42849053816 provisioned/verified the Auth runtime Secret with values suppressed; shared ghcr-pull was unchanged. No production manifest drift was detected, so apply and rollout were correctly skipped.
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
