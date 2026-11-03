# MicroFE deployment contract

## Repository ownership

- `platform-infra` owns Kubernetes manifests, Kustomize overlays, deployment/reconciliation workflows, immutable image promotion, and rollout/health verification only.
- Application implementation belongs in its application repository: source code, package manifests, Dockerfiles, unit/integration tests, and application-owned database migrations must not live in `platform-infra`.
- The Auth application repository is `phanthienquoc/phanthienquoc-authentication`. It exclusively owns Auth source, tests, Dockerfile, application dependencies, and database migrations. Its CI validates the service; its manual release workflow publishes `ghcr.io/phanthienquoc/auth-service/auth` with a full source-SHA tag, BuildKit provenance/SBOM, and an ARM64 registry digest.
- TCE Dashboard, Media Generation, and MRCute are Auth clients. They must integrate with the shared Auth API; they must not copy authentication business logic or create parallel user/session stores.
- Auth release handoff contract: repository dispatch `auth-image-published` to `phanthienquoc/platform-infra` with `app=auth-service`, `component=auth`, full source `commit`, full-SHA versioned `tag`, `auth_digest=sha256:<64 hex>`, numeric `source_run_id`, `source_workflow_path=.github/workflows/release.yml`, `source_event=workflow_dispatch`, and full `source_head_sha`. Platform verifies the exact public Actions run/jobs, proves the tag resolves to the supplied ARM64 digest, and pins that digest in GitOps.
- The Auth repository needs a repository-scoped token secret such as `PLATFORM_INFRA_DISPATCH_TOKEN` with permission to dispatch repository events to `platform-infra`. Never use the Supabase service-role key for this purpose.
- `platform-infra` promotes only `platform/auth-service/kustomization.yaml` for this event, opens a narrowly scoped promotion PR, and reconciles the Auth workload after the image reference is merged. It must not rebuild or host Auth application code.
- Keep deployment manifests such as `platform/auth-service/deployment.yaml`, `platform/microfe/**/deployment.yaml`, certificates, ingress, namespace, and Kustomize configuration in this repository. Do not add Auth source files, package manifests, Dockerfiles, application tests, or app-owned migrations here.

## Auth runtime contract

- NestJS owns authentication/authorization business logic: password verification, MFA/recovery policy, session lifecycle, refresh rotation/reuse detection, CSRF, passkey challenge and credential-counter logic, and role checks.
- Auth uses the existing Supabase project server-side through `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`; keep the service-role key backend-only and never expose it to browser/client code.
- The Kubernetes Secret `microfe-auth-secrets` provides runtime credentials: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `JWT_SECRET`, and `MFA_ENCRYPTION_KEY`. Non-secret Auth configuration belongs in `microfe-auth-config`.
- `platform-infra` deploys the workload; it does not need Supabase credentials in GitHub Actions just to apply manifests or roll out an image. Add pipeline credentials only if a specific pipeline step actually performs a Supabase migration or integration test.
- Store only Secret references in manifests. Never commit, print, or include secret values in workflow logs.
- Preserve existing tables and API/cookie compatibility; do not create duplicate user/session tables. Keep database/RPC changes in the owning application/database migration source and apply them through the approved migration process.
- Preserve immutable SHA/digest image promotion.

## Gates before production rollout

1. The Auth repository's build, lint, unit, and end-to-end tests pass.
2. Required Supabase RPCs/schema are applied and verified by the owning migration process.
3. Confirm password hash, session, MFA recovery, challenge, and passkey compatibility.
4. Test refresh rotation/reuse, recovery-code single use, MFA challenge single use, and passkey challenge/counter behavior under concurrent requests.
5. Confirm Kubernetes runtime Secret keys exist by key name only; never display values.
6. Kustomize validation succeeds and an immutable image digest is available.
7. Rollout probes and HTTPS health checks pass.

No production rollout before the relevant gates pass.
