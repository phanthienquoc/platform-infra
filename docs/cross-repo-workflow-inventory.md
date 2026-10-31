Last reviewed: 2026-10-31 13:01 ICT. Inventory is based on workflow files present on each repository's default branch at review time; StockDividend's ARM64 publisher correction is in PR [#14](https://github.com/phanthienquoc/stockdividend/pull/14) and is not merged yet.

Last reviewed: 2026-10-31 12:03 ICT. Inventory is based on the workflow files present on each repository's default branch at review time; no workflow definitions were changed by the latest credentials documentation merge.

## Deployment authority contract

- **Application repositories** own application CI, tests, build verification, immutable ARM64 GHCR publication, and dispatching non-secret release metadata.
- **`phanthienquoc/platform-infra`** owns production manifests, shared GHCR pull credentials, package/tag/digest validation, GitOps promotion PRs, cluster reconciliation, rollout/health verification, and deployment notifications.
- A successful app image build or dispatch is not proof of promotion or production health. Production PASS requires current rollout and application-health evidence.
- Never put runtime credentials in dispatch payloads. Payloads carry only app/component identifiers, immutable tags or image digests, and source commit metadata.
- Preserve CI, security, scheduled, manual recovery, backup, cleanup, and bootstrap jobs unless evidence proves a job is obsolete or redundant. Do not remove a workflow based on its filename alone.
- No workflow was removed during this inventory update. The TCE VPS setup and K3s bootstrap workflows remain operational/bootstrap workflows that require a content-level review before any retirement; they must not become a second app-release deployment authority.

## platform-infra — production and platform operations

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/reconcile-vps.yml` | Sole production GitOps reconcile authority; manual plan/apply, GitOps dispatch, path-scoped push, and declared 15-minute schedule. Owns K3s rollout and health gates. | Latest all-app reconcile [#41162916140](https://github.com/phanthienquoc/platform-infra/actions/runs/41162916140) failed real workload health gates; the latest scheduled reconcile remains [#41158397795](https://github.com/phanthienquoc/platform-infra/actions/runs/41158397795) at 09:05 ICT, with no later scheduled reconcile in the current listing. Investigate event delivery/enablement without changing the TCE market-scan schedule. |
| `.github/workflows/gitops-image-promotion.yml` | Validates release metadata and GHCR access, creates GitOps promotion changes, then dispatches reconciliation. | Media promotions are fail-closed because `PLATFORM_INFRA_AUTOMATION_TOKEN` is missing from the protected `production` Environment. |
| `.github/workflows/validate-manifests.yml` | Manifest/render validation. | Latest master run passed. |
| `.github/workflows/validate-github-actions.yml` | Workflow syntax/contract validation. | Latest master run passed. |
| `.github/workflows/inspect-vps.yml` | Read-only scheduled VPS/K3s inspection and debug snapshot. | Latest observed snapshot: 2026-10-31 09:38 ICT; node Ready, disk pressure normal at 55%, several app workloads not ready. |
| `.github/workflows/reconcile-observability.yml` | Follow-on observability reconciliation. | Latest observed run passed; this is not a production application-health pass. |
| `.github/workflows/smoke-production.yml` | Production smoke checks. | Preserve; verify current run before relying on it as health evidence. |
| `.github/workflows/keycloak-auth-production-smoke.yml` | Central SSO/Auth production smoke checks. | Preserve; Keycloak/OIDC health is not currently verified. |
| `.github/workflows/keycloak-ci.yml` | Keycloak build/test validation. | CI only. |
| `.github/workflows/provision-keycloak-tce-client.yml` | Controlled Keycloak client provisioning. | Operational, not app image publication. |
| `.github/workflows/verify-keycloak-tce-client.yml` | Keycloak client verification. | Verification-only. |
| `.github/workflows/configure-keycloak-no-email-registration.yml` | Explicit Keycloak realm configuration. | Manual configuration; preserve. |
| `.github/workflows/configure-keycloak-resend-smtp.yml` | Explicit Keycloak SMTP configuration. | Manual configuration; preserve. |
| `.github/workflows/provision-auth-runtime-secret.yml` | Provision Auth runtime secret from protected infrastructure configuration. | Secret values must stay out of logs and repository files. |
| `.github/workflows/runtime-secret-readiness.yml` | Runtime secret presence/readiness validation. | Preserve fail-closed behavior. |
| `.github/workflows/sso-auto-onboarding.yml` | SSO onboarding automation. | Preserve; no evidence to retire. |
| `.github/workflows/staging-dry-run.yml` | Staging dry-run / pre-production validation. | Preserve. |
| `.github/workflows/validate-metrics.yml` | Metrics validation. | Preserve. |
| `.github/workflows/validate-recovery-readiness.yml` | Recovery readiness gate. | Preserve. |
| `.github/workflows/bootstrap-runner.yml` | Self-hosted runner bootstrap/update. | Infrastructure bootstrap; not an app release lane. |
| `.github/workflows/vps-image-cleanup.yml` | VPS image cleanup. | Maintenance job; keep separate from release/reconcile authority. |
| `.github/workflows/mirror-locally-uncensored.yml` | Scheduled repository mirror. | Recent scheduled runs failed; investigate independently, but do not remove without proving it obsolete. |

## TCE-dashboard — application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/wf-01-tce-build-verify.yml` | App build verification. | Latest master run passed. |
| `.github/workflows/wf-01p-tce-web-pr-build.yml` | Pull-request web build. | Preserve PR coverage. |
| `.github/workflows/wf-02-tce-backend-unit-test.yml` | Backend unit tests. | Latest master run passed. |
| `.github/workflows/wf-02-tce-prettier-format.yml` | Formatting validation. | Latest master run passed. |
| `.github/workflows/wf-03-tce-production-deploy.yml` | Explicit manual production image release from master; application-side build/publish and release dispatch, not production cluster reconciliation. | Do not rerun for workflow-only changes. |
| `.github/workflows/wf-04-tce-k3s-cleanup.yml` | K3s cleanup/maintenance. | Preserve; audit before any retirement. |
| `.github/workflows/wf-06-tce-healthcheck.yml` | Scheduled public HTTP health checks. | Latest observed run [#41160165628](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41160165628) failed because Auth liveness/readiness returned HTTP 503; TCE container checks passed. |
| `.github/workflows/wf-07-tce-backup.yml` | Backup operation. | Preserve recovery capability. |
| `.github/workflows/wf-07-tce-integration-check.yml` | Integration checks. | Preserve. |
| `.github/workflows/wf-08b-tce-microfe-build-publish.yml` | MicroFE Auth/Shell/WS checks and Shell/WS image publication; dispatches immutable image metadata for central promotion. | Latest PR CI passed; deployed Shell/WS replicas remain unhealthy/pending in the latest inspection. |
| `.github/workflows/wf-09-nginx-readonly-audit.yml` | Read-only Nginx audit. | Audit-only. |
| `.github/workflows/wf-09-tce-vps-safe-setup.yml` | Safe VPS setup/operations. | Keep separate from app release and GitOps promotion. Review content before any change. |
| `.github/workflows/wf-10-tce-k3s-bootstrap.yml` | K3s bootstrap. | Bootstrap-only candidate for ownership review, not deletion by name. |
| `.github/workflows/wf-11-tce-mobile-landscape-viewport.yml` | Mobile landscape viewport regression checks. | Preserve UI regression coverage. |

## stockdividend — application CI, publisher, and scraper

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Application CI. | Latest master CI passed. |
| `.github/workflows/deploy.yml` | Build/publish ARM64 images from master after handoff and release-enable gates pass. | Intentionally fail-closed: `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED` remains disabled and `PLATFORM_INFRA_TOKEN` is missing; latest image build was skipped. Source audit found `deploy.yml` used `ubuntu-latest` without explicit platforms for scraper/admin/backend. PR [#14](https://github.com/phanthienquoc/stockdividend/pull/14) adds a native ARM64 runner, explicit `linux/arm64` builds, and full-source-SHA contract assertions; wait for current-head CI before release. |
| `.github/workflows/wf-platform-infra-release.yml` | Sends immutable full-source-SHA promotion dispatches to platform-infra after a successful publisher run. | Latest dispatch was skipped because the publisher was held/failed. |
| `.github/workflows/run_scraper.yml` | Scraper job, including scheduled/manual operation. | Preserve scheduled data collection; unrelated to production image promotion. |

## media-generation — application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Media app CI. | Latest master CI passed. |
| `.github/workflows/wf-03-media-production-deploy.yml` | Master-only/manual production release, immutable version + full-source-SHA tag publication, then central GitOps promotion request. | Immutable release images exist; frontend/backend promotion runs [#41158836425](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836425) and [#41158836607](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836607) passed GHCR validation but stopped at the missing `PLATFORM_INFRA_AUTOMATION_TOKEN` gate. |

## phanthienquoc-authentication — Auth application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Auth service tests, typecheck, build, and container build. | Latest master CI passed. |
| `.github/workflows/release.yml` | Explicit manual master-only Auth image release; verifies source SHA and version before publishing and dispatching. | Last release workflow [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) passed, but public Auth health check [#41160165628](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41160165628) still returned HTTP 503. Do not equate publish success with runtime health. |
| `.github/workflows/web-ci.yml` | Auth web CI. | Preserve separate web validation. |

## Release contract checks

1. Reject non-master production release attempts.
2. Require successful source tests/build before publication.
3. Use immutable source-SHA tags or verified `sha256:<64 hex>` image digests; never promote mutable aliases such as `latest`.
4. Verify GHCR package access before mutating shared pull credentials or cluster manifests.
5. Require the appropriate protected handoff credential before creating a GitOps PR. `GHCR_READ_TOKEN`, `PLATFORM_INFRA_AUTOMATION_TOKEN`, StockDividend's `PLATFORM_INFRA_TOKEN`, and app release-dispatch tokens are distinct contracts; do not substitute them for one another.
6. Reconcile only through platform-infra, then verify Deployment desired/ready/updated replicas and public liveness/readiness endpoints.
7. Keep production health NOT HEALTHY/UNVERIFIED while any required lane fails. Preserve the TCE market-scan schedule continuously.
