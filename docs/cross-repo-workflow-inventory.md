# Cross-Repository Workflow Inventory

Last reviewed: 2026-11-11 05:55 ICT (2026-11-10 22:55:22 UTC).

This is the compact current workflow inventory. The previous append-only inventory is preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md. Historical timestamped workflow checkpoints remain under docs/cross-repo-workflow-inventory-checkpoints/.

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
| reconcile-vps.yml | Sole production manifest reconciliation/apply authority; image-change bypass only for provenance-verified gitops-promoted-ready dispatch |
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

## Latest verification — 2026-11-11 05:55 ICT / 22:55:22 UTC

- Direct Git ref reads confirm current master SHAs: Platform `89b39427c78510cdcf30326a30737fe9bbe0f4c2`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open owner-decision drafts: Platform #1314, #544, #541, #539; Authentication #76. No open PRs in TCE, Stock or Media. Exact PR heads/check-runs: Platform #1314 `db152c9a` validate PASS; #544 `c95e7dae` PASS; #541 `b8f7c6ba` PASS; #539 `2dc48b97` PASS; Authentication #76 `f19cacb0` validate PASS and Supabase Preview skipped. New Platform PR #1601 is open on dedicated branch `fix/require-provenance-for-image-changes-20261111-0555-ict`; validation is pending on its final docs-updated head.
- Platform PR #1600 is the latest merged readiness checkpoint at master `89b39427`; post-merge validation #42911038235 passed. Latest manual reconciliation #42915749236 succeeded on current master. Recovery #42915997996 succeeded as workflow_dispatch; neither is native schedule evidence.
- Current relevant CI: Platform reconciliation #42915749236 SUCCESS; TCE backend unit tests #42822853137 PASS, manual public health #42915762180 FAIL; Stock CI #42610360402 PASS, scheduled scraper #42457182511 FAIL closed; Media CI #42539512417 PASS; Authentication CI #42654579277 PASS. The old Supabase Preview check on Auth #76 is intentionally skipped.
- Latest native schedule evidence (first-attempt event=schedule, branch=master only): Platform reconcile #42909757881 (21:55:56Z), inspection #42887151366 (19:37:38Z), recovery #42906791198 (21:37:08Z), watchdog #42908417737 (21:47:23Z); TCE WF-06 #42872071366 (18:08:09Z), WF-12 #42915709227 (22:33:49Z). At 22:55:22Z all six inter-arrival gaps exceed their unchanged budgets; five current ages exceed budget. WF-12 age is within budget but its run fails because WF-06 is stale. WF-12 heartbeat dispatch succeeded and Platform receiver #42915725335 accepted it; neither substitutes for a native WF-06 run.
- Native gaps/ages at reference: Platform reconcile 19941s/3566s; inspection 28677s/11864s; recovery 20656s/4694s; watchdog 20852s/4079s; TCE WF-06 27554s/17233s; WF-12 17617s/1293s. Budgets remain 2700/4500/2700/2700/1500/1500s. Cron and market-scan schedules are unchanged.
- Latest full read-only inspection fallback #42907109988 generated `debug/vps-latest.md` at 21:39:20Z and is now 4562s old, just beyond the 4500s budget. A newer workload/node snapshot in reconciliation #42915749236 (22:34:27Z) showed `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; it did not include fresh disk/RAM/restart measurements.
- Reconciliation #42915749236 verified GHCR read access for Auth, MicroFE Shell/WS and TCE web/service packages; Auth runtime Secret was provisioned and verified with values suppressed; shared `ghcr-pull` remained unchanged; managed MicroFE/TCE image-pull helpers found no failures; TCE desired/live images paired at `prod-v0.1.0-e75e338`. GitOps drift=false; production manifest apply, image replacement and rollout were correctly skipped. Auth/TCE are intentional zero-replica maintenance; MicroFE is active/healthy; Keycloak skipped.
- Current workload snapshot: Media backend/frontend and MicroFE Shell/WS/NATS 1/1; TCE/Auth 0/0 maintenance; Stock Admin two pods and desired Backend one pod ImagePullBackOff; legacy Stock Backend/Frontend 1/1. Stock historical tag `12d63b4` still has the known ARM64 manifest mismatch; legacy cached image IDs have no RepoDigest and cannot be promoted.
- TCE manual WF-06 #42915762180 failed all four approved endpoints at HTTP 503 against required HTTP 200. Native WF-12 #42915709227 failed because latest native WF-06 was 265m old at its own reference. Stock scraper #42457182511 failed before dependencies/ingestion because `VNSTOCK_API_KEY` was empty. No Stock production publication or digest handoff occurred.
- Media runner service/listener remains active; remote unregister, backup/retention and authoritative DNS ownership remain unverified. GHCR server-side immutable-tag enforcement remains unverified.
- Last verified branch endpoint reported protected=false for all five master branches; branch-protection detail access and effective inherited rulesets remain unverified. Administrator action remains tracked in issue #1575.
- PR #1601 addresses a source-verified safety gap: the old master workflow_dispatch input could set `ALLOW_IMAGE_CHANGES=true` and bypass the image guard without publisher/promotion provenance. The PR removes the input, restricts authorization to `gitops-promoted-ready` after provenance validation, removes the obsolete recovery/Keycloak input references and adds regression assertions. Current master remains unchanged until the PR passes and merges.
- No workflow was removed; no new image publication, digest promotion, production apply, rollout, scale, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only inventory preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md.
- Timestamped workflow checkpoints: docs/cross-repo-workflow-inventory-checkpoints/.
- Current readiness and runtime blockers: docs/cross-repo-deployment-tracker.md.
