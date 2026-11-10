# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-11 00:18 ICT (2026-11-10 17:18:32 UTC)

This is the compact current readiness view. Historical append-only content from the previous rolling tracker is preserved at docs/archive/cross-repo-deployment-tracker-append-only-2026-11-10.md. Timestamped checkpoints remain under docs/cross-repo-deployment-checkpoints/.

## Repository readiness

| Repository | Current master SHA | Open PRs | Latest verified CI / operational evidence |
|---|---|---|---|
| phanthienquoc/platform-infra | 61bbb9c0927ba43902f59344c38b289d493934b3 | #1590 (documentation checkpoint), #1314, #544, #541, #539 | PR #1589 inspection-only auto-merged; workflow #42862329716 passed inspection, output validation, latest-master rebase, PR creation and exact-head validation |
| phanthienquoc/TCE-dashboard | c4602be3b0a7b624bdb9cd41519cfc70a14d92ab | none | WF-02 #42822853121 and WF-05 #42822853137 PASS; WF-06 #42799497774 FAIL (four public endpoints HTTP 503); WF-12 #42795292155 FAIL/stale |
| phanthienquoc/stockdividend | b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61 | none | CI #42610360402 PASS; scraper #42457182511 failed closed because VNSTOCK_API_KEY was missing |
| phanthienquoc/media-generation | dcd698699c65ba6e73f6b43838975144777131c3 | none | CI #42539512417 PASS; production promotion remains owner/token gated |
| phanthienquoc/phanthienquoc-authentication | eab85fab32d7c9baef750c1fedbb93deb8c1333f | #76 (draft / owner decision) | auth-service-ci #42654579277 PASS; migration side-effect review remains |

Platform PR #1587 merged as ec8b91f1fb9c66740562d50cc73c4b68c6cb8422 after exact-head manifest validation #42850835140 passed. PR #1588 merged as bfd0ea66ee005bd47b4dbcc85ced6428d78d9f44 after exact-head validate-github-actions #42862175393 and validate-manifests #42862174503 passed on head 3faf1a73. PR #1588 fixed the read-only inspection rebase by force-updating only the runner-local refs/remotes/origin/master ref; it also pins actionlint v1.7.12 to the official Linux release and verifies the checksums manifest and archive before execution. The merged change triggered inspection workflow #42862329716. Inspection PR #1589, branch automation/vps-inspection-42862329716-1, passed all steps including latest-master rebase and exact-head validation, then squash-merged as 61bbb9c0927ba43902f59344c38b289d493934b3. Snapshot debug/vps-latest.md was generated at 17:11:28Z. No production manifests or workloads changed.

Open owner-decision drafts remain: Platform #1314 (mail plan), #544 (Keycloak activation status), #541 (Keycloak database plan), #539 (central identity decision), and Authentication #76 (migration drift investigation). Platform #1590 is this documentation-only checkpoint PR. Do not merge owner-decision drafts without the relevant owner decision and side-effect review.

## Native schedule freshness

Reference time: 2026-11-10 17:18:32 UTC. Only first-attempt event=schedule runs on master count. The connected workflow-run reader exposes PR-triggered runs only; ages below are the ages of last-confirmed native events from the 15:57:57Z inventory, not proof that no later event occurred. Manual, push, workflow_run and repository_dispatch events are excluded.

| Lane | Last-confirmed native run | Result / created UTC | Age of last-confirmed run (s) | Inter-arrival gap (s) | Existing budget (s) |
|---|---:|---|---:|---:|---:|
| Platform reconcile | #42778829676 | success / 07:56:31 | 33721 | 25539 | 2700 |
| Platform inspection | #42809278936 | success / 11:39:41 | 20331 | 29694 | 4500 |
| Platform recovery | #42848981485 | success / 15:52:52 | 5140 | 29378 | 2700 |
| Platform watchdog | #42777386082 | failure / 07:44:22 | 34450 | 25992 | 2700 |
| TCE WF-06 | #42799497774 | failure / 10:28:55 | 24577 | 27892 | 1500 |
| TCE WF-12 | #42795292155 | failure / 09:59:25 | 26347 | 27790 | 1500 |

All six inter-arrival gaps in the last-confirmed inventory exceed their unchanged budgets. At 17:18:32Z all six last-confirmed event ages also exceed their budgets; Platform recovery's last-confirmed run #42848981485 is 5140s old and its 29378s inter-arrival gap exceeds the 2700s budget. These are last-confirmed ages, not proof that no later native event exists. Inspection #42862329716 is push-triggered and does not refresh the inspection schedule lane; manual workflow_dispatch and workflow_run events do not count. The connected run reader cannot query later non-PR schedule events. Configured schedules remain unchanged: Platform reconcile 7,22,37,52; inspection 2,32; recovery 10,25,40,55; watchdog 12,27,42,57; TCE WF-06 every 15 minutes; TCE WF-12 at 7,22,37,52. Do not change cron, freshness budgets, strict health thresholds or TCE market-scan scheduling.

## Current actions

1. Issue #1497 — GitHub administrator must provide authoritative enqueue, delivery and Actions service telemetry for the six affected schedule workflows. Last-confirmed native recovery #42848981485 succeeded at 15:52:52Z, but its 29378s inter-arrival gap still fails. Require consecutive native runs within existing budgets before closing.
2. Issue #1575 — administrator must verify effective inherited rulesets and required-check enforcement. Branch API metadata previously reported protected=false for all five master branches; rulesets reads returned HTTP 403, so inherited coverage remains unknown. Do not infer that no organization ruleset exists.
3. Issue #872 — TCE/Auth owners must diagnose and recover runtime health with approved immutable digests, rollback references and no unintended database migration. Keep HTTP 200 as the only healthy public response. TCE/Auth/Keycloak zero replicas are maintenance, not healthy service.
4. Stock issue #42 — Stock owner must provision VNSTOCK_API_KEY through repository/organization secrets and run scraper with preflight_only=true before ingestion. Never put the key in Git, logs, artifacts or chat.
5. Stock issue #43 — owner must approve the current source release and native ARM64 immutable scraper/admin/backend publication. Verify per-component digest equality, then hand admin/backend digests to Platform. Never overwrite historical tag 12d63b4.
6. Media production promotion remains blocked pending authorized PLATFORM_INFRA_AUTOMATION_TOKEN and owner approval. Media runner retirement additionally requires remote unregister, backup/retention and DNS ownership evidence.
7. Platform operator has fresh read-only K3s inspection #42862329716; snapshot generated at 17:11:28Z and is 424s old at the 17:18:32Z reference, within the 4500s budget. Host maintenance/restart still requires separate approval. TCE owner must verify SSH host fingerprint before SSH maintenance.
8. PR #1588 merged as bfd0ea66; exact-head workflow validation #42862175393 and manifest validation #42862174503 passed. It fixes the persistent runner's local remote-tracking ref and pins actionlint v1.7.12 with checksum verification.
9. PR #1589 inspection-only auto-merged as 61bbb9c0 after workflow #42862329716 passed inspection, output validation, latest-master rebase, PR creation and exact-head validation. No production manifests or workloads changed.
10. Decommission preflight: active production manifest tree contains no StockDividend/Media namespace or image refs; no Stock/Media VolumeSnapshot refs or PVCs were found (only k3s-debug PVC exists); preserved tce-prod and microfe-platform remain. Media runner service/listener is still active, GitHub runner registration is not inferred by host inspection, and DNS ownership is not inferred. Keep decommission blocked until owner supplies remote unregister, backup/retention and DNS evidence.

## Current runtime blockers

- Latest full read-only K3s inspection is workflow #42862329716; snapshot generated at 17:11:28Z. At 17:18:32Z it is 424 seconds old, within the 4500-second inspection freshness budget. PR #1589 was exact-head validated and squash-merged as 61bbb9c0. This is read-only evidence and does not authorize production changes.
- Fresh K3s inventory at 17:11:28Z: ARM64 node Ready; disk 56% with about 20 GiB free and RAM available about 19 GiB; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; TCE frontend/service, Auth and Keycloak 0/0 maintenance; Stock Admin 0/1 (two ImagePullBackOff pods) and desired Backend 0/1 on historical tag 12d63b4, while existing Backend and Frontend remain 1/1; both public OIDC discovery probes return HTTP 503; Keycloak diagnostic timed out while deployment is 0/0; Media runner service/listener remains active; host reports restart_required=yes; GitOps drift is clean. No Stock/Media VolumeSnapshot refs or PVCs were found; only k3s-debug PVC is present. Protected decommission preflight found no active Stock/Media references in the Platform production manifest tree and confirmed preserved tce-prod and microfe-platform namespaces. This snapshot does not authorize rollout, restart, deletion or retirement.
- Latest reconciliation #42849053816 completed at 15:55:16 UTC; at 17:18:32Z it is 4996 seconds old, beyond the 2700-second evidence budget. Its logs verify GHCR read access to Auth, MicroFE Shell/WS and TCE web/service packages; Auth runtime Secret provision/verification with values suppressed; shared ghcr-pull unchanged; DRIFT=false; production apply, image replacement and rollout skipped. This is last-known evidence, not current runtime health.
- Stock GHCR digest coverage remains warning: cached backend/user tags 23b2878 lack RepoDigest; local image IDs are not registry digests or publication evidence. Stock Admin and desired Backend still fail with no match for platform in manifest on tag 12d63b4.
- TCE WF-06 #42799497774 logs show TCE web, TCE API, Auth liveness and Auth readiness each returned HTTP 503 while expected_status remained 200; fresh inspection #42862329716 independently confirms both public OIDC discovery probes return HTTP 503 and Keycloak remains 0/0 with a timed-out diagnostic. The strict HTTP 200 contract is correct; TCE/Auth/Keycloak runtime recovery is outstanding.
- GHCR tag absence guards, SHA tags and digest equality do not prove registry-side immutable-tag enforcement. Registry-side policy remains unverified.

## Current deployment authority and safety

- App repositories own CI/tests/builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout and post-rollout health verification.
- reconcile-vps.yml remains the sole production apply authority. inspect-vps.yml remains read-only.
- Preserve purposeful CI, test, security, manual, release, backup and scheduled workflows. No workflow has been confirmed redundant/obsolete.
- No new GHCR publication, digest promotion, production manifest apply, workload rollout/scaling, namespace/PVC/PV deletion, runner retirement, shared credential rotation, DNS/database/storage mutation or host maintenance occurred in this checkpoint.
- Latest reconciliation #42849053816 provisioned/verified Auth runtime Secret with values suppressed; shared ghcr-pull was unchanged. No production manifest drift was detected at that time, so apply and rollout were correctly skipped.
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
