Last reviewed: 2026-10-31 17:01 ICT. Auth shutdown is not yet verified: merged PR #891 changed the Auth manifest, but reconcile #41190669294 applied the shared environment overlay without applying the separate Keycloak Kustomize path; its snapshot still showed a Keycloak pod Running 0/1. PR #892 is being hardened so the manual `auth-shutdown` target uses an exact runner allowlist, skips shared GHCR mutation/restarts, and fails until both workloads have zero desired/ready/updated replicas and no matching pods remain. No TCE market-scan schedule change. Production remains NOT HEALTHY/UNVERIFIED.

Last reviewed: 2026-10-31 16:18 ICT. Supabase log query returned 382 recent `keycloak_runtime` auth-error circuit-breaker events in 10 minutes; direct SQL ping and role lookup still time out. Auth remains non-ready, and the exact credential mismatch is not yet proven. No secret or database role was changed.

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
| `.github/workflows/reconcile-vps.yml` | Sole production GitOps reconcile authority; manual plan/apply, GitOps dispatch, path-scoped push, and declared 15-minute schedule. Owns K3s rollout and health gates. | Post-merge run [#41187383657](https://github.com/phanthienquoc/platform-infra/actions/runs/41187383657) passed the TCE paused-state lane but failed Auth, StockDividend, MicroFE and Media health gates. New health diagnostics identify MicroFE tags 0.1.0/RELEASE_SHA as not found and StockDividend tag 12d63b4 as lacking an ARM64 manifest. Latest observed scheduled run remains [#41184627405](https://github.com/phanthienquoc/platform-infra/actions/runs/41184627405) at 15:26 ICT; investigate absent later schedule events without altering the TCE market-scan schedule. Production remains NOT HEALTHY/UNVERIFIED. |
| `.github/workflows/gitops-image-promotion.yml` | Validates release metadata and GHCR access, creates GitOps promotion changes, then dispatches reconciliation. | Media exact manifests validated, but promotion fails before PR creation because PLATFORM_INFRA_AUTOMATION_TOKEN is empty. MicroFE promotion [#41154654986](https://github.com/phanthienquoc/platform-infra/actions/runs/41154654986) additionally fails GHCR preflight with HTTP 403 for microfe-shell and microfe-ws; after package access is corrected, the protected automation token is still required. Keep fail-closed behavior. |
| `.github/workflows/validate-manifests.yml` | Manifest/render validation on relevant PRs, master pushes, and explicit workflow dispatch for exact-head inspection validation. | PRs changing only `debug/vps-latest.md` are ignored by the ordinary PR trigger; inspection automation must still dispatch and observe success on the exact head SHA before merge. A regression assertion enforces this contract. |
| `.github/workflows/validate-github-actions.yml` | Workflow syntax/contract validation. | Latest master run passed. |
| `.github/workflows/inspect-vps.yml` | Read-only scheduled VPS/K3s inspection and debug snapshot. | Snapshot [#41178914394](https://github.com/phanthienquoc/platform-infra/actions/runs/41178914394) at 14:01 ICT: node Ready, disk 55%, but Keycloak/Auth/Media backend 0/1; Shell/WS have missing image tags and StockDividend old tags lack ARM64 manifests. The previous workflow immediately merged PR #879 before validation. PR #880 now adds explicit exact-head manifest validation and expected-SHA squash merging; run #41179285331 passed before PR #881 merged. This follow-up avoids the zero-job PR check for debug-only snapshot changes. |
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
| `.github/workflows/wf-06-tce-healthcheck.yml` | Scheduled public HTTP health checks. | Latest run [#41185878137](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41185878137) returned HTTP 503 for TCE web and Auth liveness/readiness. TCE 503 is expected while the operator-requested K3s pause remains in force; Auth 503 is an unresolved independent production failure. Preserve the health check rather than masking the failure. |
| `.github/workflows/wf-07-tce-backup.yml` | Backup operation. | Preserve recovery capability. |
| `.github/workflows/wf-07-tce-integration-check.yml` | Integration checks. | Preserve. |
| `.github/workflows/wf-08b-tce-microfe-build-publish.yml` | MicroFE Auth/Shell/WS checks and Shell/WS image publication; dispatches immutable image metadata for central promotion. | Publish run [#41154490073](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41154490073) built/pushed Shell digest sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd and WS digest sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d for source e6940ff911ea63338fb4f66eb903bcdf6c9825a8; GitOps promotion [#41154654986](https://github.com/phanthienquoc/platform-infra/actions/runs/41154654986) is blocked by HTTP 403 from shared GHCR_READ_TOKEN on both packages. Deployed manifests still reference missing placeholder tags. |
| `.github/workflows/wf-09-nginx-readonly-audit.yml` | Read-only Nginx audit. | Audit-only. |
| `.github/workflows/wf-09-tce-vps-safe-setup.yml` | Safe VPS setup/operations. | Keep separate from app release and GitOps promotion. Review content before any change. |
| `.github/workflows/wf-10-tce-k3s-bootstrap.yml` | K3s bootstrap. | Bootstrap-only candidate for ownership review, not deletion by name. |
| `.github/workflows/wf-11-tce-mobile-landscape-viewport.yml` | Mobile landscape viewport regression checks. | Preserve UI regression coverage. |

## stockdividend — application CI, publisher, and scraper

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Application CI. | Latest master CI passed. |
| `.github/workflows/deploy.yml` | Build/publish ARM64 images from master after handoff and release-enable gates pass. | K3s diagnostics in [#41187383657](https://github.com/phanthienquoc/platform-infra/actions/runs/41187383657) confirm admin:12d63b4 and backend:12d63b4 have no matching ARM64 manifest. Publisher remains fail-closed: STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED is false and PLATFORM_INFRA_TOKEN is missing. PR #14 fixed the publisher to use native ARM64 and full-SHA tags; configure handoff first, then publish and verify new images before promotion. |
| `.github/workflows/wf-platform-infra-release.yml` | Sends immutable full-source-SHA promotion dispatches to platform-infra after a successful publisher run. | Latest dispatch was skipped because the publisher was held/failed. |
| `.github/workflows/run_scraper.yml` | Scraper job, including scheduled/manual operation. | Scheduled run [#41178133076](https://github.com/phanthienquoc/stockdividend/actions/runs/41178133076) is still in progress on the old commit and logs repeatedly report disabled vnstock 5.0.1. PR [#15](https://github.com/phanthienquoc/stockdividend/pull/15) upgraded the dependency to 5.2.1 and merged after the five-job CI suite passed; the next run will pick up the new pin. Do not cancel or remove the scheduled job. |

## media-generation — application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Media app CI. | Latest master CI passed. |
| `.github/workflows/wf-03-media-production-deploy.yml` | Master-only/manual production release, immutable version + full-source-SHA tag publication, then central GitOps promotion request. | Immutable tag prod-v0.3.0-32f3bf56e1f44c65a5d98f35bed0547f398f8e90 exists and exact GHCR manifests validated in [#41158836425](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836425) and [#41158836607](https://github.com/phanthienquoc/platform-infra/actions/runs/41158836607), but promotion is blocked by missing PLATFORM_INFRA_AUTOMATION_TOKEN. The currently deployed backend uses old tag prod-v0.3.0-58f80a8 and remains non-ready; do not equate publication with deployment or health. |

## phanthienquoc-authentication — Auth application CI and release producer

| Workflow file | Role / contract | Current note |
|---|---|---|
| `.github/workflows/ci.yml` | Auth service tests, typecheck, build, and container build. | Latest master CI passed. |
| `.github/workflows/release.yml` | Explicit manual master-only Auth image release; verifies source SHA and version before publishing and dispatching. | Post-merge reconcile [#41187383657](https://github.com/phanthienquoc/platform-infra/actions/runs/41187383657) shows `microfe-auth` desired=1/ready=0 on `prod-v1.0.0-ceb2688`; secret key-presence and TLS checks pass while public Auth health remains HTTP 503. Supabase logs on 2026-10-31 09:08–09:18 UTC show repeated `keycloak_runtime` `auth_error` circuit-breaker events; SQL ping and role lookup via the management connector time out, so role existence/password parity is not verified. Do not reset credentials until secure role/Secret comparison is possible. |
| `.github/workflows/web-ci.yml` | Auth web CI. | Preserve separate web validation. |

## Release contract checks

1. Reject non-master production release attempts.
2. Require successful source tests/build before publication.
3. Use immutable source-SHA tags or verified `sha256:<64 hex>` image digests; never promote mutable aliases such as `latest`.
4. Verify GHCR package access before mutating shared pull credentials or cluster manifests.
5. Require the appropriate protected handoff credential before creating a GitOps PR. `GHCR_READ_TOKEN`, `PLATFORM_INFRA_AUTOMATION_TOKEN`, StockDividend's `PLATFORM_INFRA_TOKEN`, and app release-dispatch tokens are distinct contracts; do not substitute them for one another.
6. Reconcile only through platform-infra, then verify Deployment desired/ready/updated replicas and public liveness/readiness endpoints.
7. A zero-replica maintenance scope passes only when every scoped Deployment has desired=ready=updated=0 and no active pods remain; otherwise fail closed. Keep production health NOT HEALTHY/UNVERIFIED while any required lane fails. Preserve the TCE market-scan schedule continuously.
