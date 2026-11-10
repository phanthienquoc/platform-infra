# Cross-Repository Workflow Inventory

Last reviewed: 2026-11-11 06:08 ICT (2026-11-10 23:08:55 UTC).

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
| reconcile-vps.yml | Sole production manifest reconciliation/apply authority; image-change bypass only for provenance-verified gitops-promoted-ready dispatch; Keycloak Markdown excluded from push trigger |
| recover-stale-ops.yml | Scheduled and receipt-backed recovery controller; Keycloak operator Markdown excluded from push recovery |
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

## Latest verification — 2026-11-11 06:08 ICT / 23:08:55 UTC

- Current master refs: Platform `8b11d6629863b90536066d4e134a089b69dd6182`; TCE `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- PR #1601 merged at `72ed11ef`, removing manual `allow_image_changes`; exact-head and post-merge validation passed. PR #1602 inspection-only merged at `8b11d662`, carrying read-only inspection #42920320410.
- Push reconciliation #42920184478 was triggered by `platform/keycloak/README.md`, misclassified it as a Keycloak workload change, applied the dedicated Keycloak resource set and executed the allowlisted Auth/Keycloak scale-to-zero command. The run verified no matching pods remained; it did not record pre-scale replica values, so the exact state transition is unknown. This was an unintended side effect of operator documentation. PR #1603 fixes the scope classification and both reconcile/recovery push filters.
- PR #1603 is open on `fix/push-scope-ignore-keycloak-docs-20261111-0610-ict`, based on exact master `8b11d662`. It adds a Keycloak Markdown exclusion, treats resolver-only changes as non-deploying metadata, adds negative scope fixtures, and prevents those changes from forcing cluster-wide apply. Final-head checks are pending.
- Fresh full read-only inspection #42920320410 at 23:05:16Z is 219s old at this reference. Host ARM64 Ubuntu 22.04.5; RAM 19 GiB available; disk 56% used / 20 GiB free; `restart_required=yes`; no restart or package upgrade performed. K3s node Ready, v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Current workload evidence: Media backend/frontend 1/1 and digest-pinned; MicroFE Shell/WS/NATS 1/1; TCE frontend/service 0/0; Auth/Keycloak 0/0; public OIDC discovery for both realms HTTP 503. Stock Admin has two ImagePullBackOff pods and desired Backend one ImagePullBackOff pod on `12d63b4` with `no match for platform in manifest`; legacy Backend/Frontend 1/1 on `23b2878` without RepoDigest evidence.
- Storage preflight reports no Stock/Media PVC or VolumeSnapshot references; the separate `k3s-debug/k3s-debug-logs` PVC remains bound. Media runner service/listener is active/enabled; remote GitHub unregister, backup/retention and DNS ownership remain unverified.
- Inspection reports GitOps drift clean. Reconciliation #42915749236 previously verified five GHCR package reads, Auth runtime Secret with values suppressed, unchanged shared `ghcr-pull`, no managed MicroFE/TCE pull failures and TCE desired/live pairing. It skipped manifest apply, image replacement and rollout.
- Native schedule evidence at 23:08:55Z: Platform reconcile #42909757881 age 4379s/gap 19941s; inspection #42887151366 12677s/28677s; recovery #42906791198 5507s/20656s; watchdog #42908417737 4892s/20852s; TCE WF-06 #42872071366 18046s/27554s; WF-12 #42915709227 2106s/17617s. All six current-age and inter-arrival budgets are exceeded. Cron and TCE market-scan schedule unchanged.
- CI evidence: Platform post-merge #42920184484, #42920184389 and #42920184623 passed; TCE backend tests #42822853137 passed but manual public health #42915762180 failed four HTTP 200 probes with HTTP 503; Stock CI #42610360402 passed but scraper #42457182511 failed closed due missing `VNSTOCK_API_KEY`; Media CI #42539512417 and Auth CI #42654579277 passed.
- GHCR server-side immutable-tag enforcement remains unverified. No new image publication, digest promotion, shared production manifest apply, namespace/PVC/PV deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot occurred. The narrow Auth/Keycloak scale-to-zero command in #42920184478 is the one production-side effect documented above; no other workload rollout was observed. No workflow removed. TCE market-scan schedule unchanged.

## Historical evidence

- Previous full append-only inventory preserved at docs/archive/cross-repo-workflow-inventory-append-only-2026-11-10.md.
- Timestamped workflow checkpoints: docs/cross-repo-workflow-inventory-checkpoints/.
- Current readiness and runtime blockers: docs/cross-repo-deployment-tracker.md.
