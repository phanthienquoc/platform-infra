# Cross-Repository Workflow Inventory

Last reviewed: 2026-11-11 02:56 ICT (2026-11-10 19:56:40 UTC).

This is the compact current workflow inventory. The previous append-only inventory is preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md. Historical timestamped workflow checkpoints remain under docs/cross-repo-workflow-inventory-checkpoints/.

## Ownership and production authority

| Repository | Owns | Must not own |
|---|---|---|
| TCE-dashboard | App CI, tests, build verification, immutable TCE/MicroFE GHCR publication, public app health probes and app-specific backup/integration checks | Production manifests, shared pull credentials, production GitOps apply, K3s rollout or direct SSH/Compose deployment |
| StockDividend | App CI, tests, native ARM64 immutable image publication, scraper and safe credential preflight | Platform manifests, shared GHCR credentials, direct Kubernetes/SSH/Compose production deployment |
| Media Generation | App CI, tests and immutable image publication | Platform manifests, shared pull credentials, direct production deployment |
| phanthienquoc-authentication | Auth CI, tests, release/provenance and immutable app publication | Shared pull credentials, production manifests, direct production apply |
| platform-infra | Production manifests, shared GHCR pull credentials, source-run/provenance verification, digest promotion, GitOps reconciliation, rollout, runtime inspection and health verification | App source tests/builds or app-owned image publication |

Platform reconcile-vps.yml is the single production apply authority. Platform inspect-vps.yml is read-only. Do not add competing SSH/Compose deployment authorities in app repositories.

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
| reconcile-vps.yml | Sole production manifest reconciliation/apply authority |
| recover-stale-ops.yml | Scheduled and receipt-backed recovery controller |
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
4. Platform validates digest references, reconciles production manifests and verifies rollout/health only with fresh runtime evidence.
5. Shared ghcr-pull credentials are Platform-owned; app workflows must not rotate or mutate them.
6. Repository-level pre-push tag-absence guards and digest checks do not prove GHCR server-side immutable-tag policy. Registry-side enforcement remains unverified.

## Preservation decisions

- Keep all CI, test, security, formatting, release, backup, integration, manual and scheduled workflows listed above.
- No workflow is confirmed redundant or obsolete in this review.
- Do not merge owner-decision drafts or trigger a production publisher merely to make the inventory appear complete.
- Do not add duplicate direct SSH/Compose deployment authorities.
- Do not change the TCE market-scan schedule.

## Latest verification — 2026-11-11 02:56 ICT / 19:56:40 UTC

- Direct Git ref reads confirm current master SHAs: Platform \`67732ddee261bd70a42f96735462761353e01fb4\`; TCE \`c4602be3b0a7b624bdb9cd41519cfc70a14d92ab\`; Stock \`b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61\`; Media \`dcd698699c65ba6e73f6b43838975144777131c3\`; Authentication \`eab85fab32d7c9baef750c1fedbb93deb8c1333f\`.
- Open owner-decision drafts: Platform #1314, #544, #541, #539; Authentication #76. No open PRs in TCE, Stock or Media. Platform inspection PR #1596 is merged as current master \`67732ddee261bd70a42f96735462761353e01fb4\`; exact-head manifest validation #42887430642 passed. No post-merge manifest validation on that SHA was observed in latest Actions history.
- Latest Platform read-only inspection #42887151366 succeeded as native \`schedule\` at 19:37:38Z and generated \`debug/vps-latest.md\` at 19:37:48Z. At 19:56:40Z the snapshot is 1132s old, within the 4500s budget. It reports ARM64 node Ready, K3s v1.36.3+k3s1, disk 56% (~20 GiB free), RAM ~19 GiB, \`restart_required: yes\`; Media and MicroFE core workloads 1/1; TCE/Auth/Keycloak 0/0 maintenance; Stock Admin and a new desired Backend pod fail image pull on \`12d63b4\`; legacy Backend/Frontend remain 1/1 on \`23b2878\`. Stock cached \`23b2878\` images have no RepoDigest. Keycloak/OIDC probes return HTTP 503; Media runner service/listener is active.
- Latest Platform reconciliation #42887561360 succeeded at 19:40:11Z via \`workflow_dispatch\`, not native schedule. Auth runtime Secret keys were verified with values suppressed; shared \`ghcr-pull\` Secrets remained unchanged; TCE release pairing passed with desired/live \`prod-v0.1.0-e75e338\`; GitOps drift=false; manifest apply and rollout skipped. MicroFE active health passed; TCE/Auth were explicitly maintenance; Keycloak skipped.
- Latest TCE WF-06 manual run #42888337472 failed all four approved endpoints at HTTP 503 against required HTTP 200. Latest native WF-06 #42872071366 and WF-12 #42867304730 remain failures/stale. Native TCE WF-07 integration run #42888228034 succeeded at 19:44:10Z; it is not a substitute for WF-06/WF-12.
- At 19:56:40Z five of six native deployment-lane current ages exceed their unchanged budgets; Platform inspection alone is within age budget. All six inter-arrival gaps exceed budget. Exact run IDs, age and gap values are in \`docs/cross-repo-deployment-tracker.md\`. Cron and freshness budgets remain unchanged.
- Latest app CI evidence remains Platform post-merge #42881164425 PASS on previous master SHA \`b629d406\`; TCE WF-02/WF-05 previously passed but latest health probes fail; Stock CI #42610360402 PASS; Media CI #42539512417 PASS; Authentication CI #42654579277 PASS. Current master CI evidence must be interpreted by head SHA, not merely latest run conclusion.
- Branch endpoint reports \`protected=false\` for all five master branches. Branch-protection detail GET returns 403; repository rulesets GET returns \`[]\` for Platform, TCE, Media and Authentication; Stock rulesets GET returns 403 due plan limitation. Effective inherited organization rulesets are not independently verified; administrator action remains open in issue #1575.
- Stock scraper #42457182511 remains fail-closed because \`VNSTOCK_API_KEY\` is absent. Stock ARM64 publisher contract is present, but no production publication or digest handoff occurred. GHCR server-side immutable-tag enforcement remains unverified.
- No workflow was removed; no new image publication, digest promotion, production apply, rollout, scale, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only inventory preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md.
- Timestamped workflow checkpoints: docs/cross-repo-workflow-inventory-checkpoints/.
- Current readiness and runtime blockers: docs/cross-repo-deployment-tracker.md.
