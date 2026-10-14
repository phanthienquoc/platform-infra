# MicroFE deployment contract

## Repository ownership

- `platform-infra` owns Kubernetes manifests, Kustomize overlays, deployment/reconciliation workflows, immutable image promotion, and rollout/health verification only.
- Application implementation belongs in its application repository: source code, package manifests, Dockerfiles, unit/integration tests, and application-owned database migrations must not live in `platform-infra`.
- The Auth application repository is `phanthienquoc/phanthienquoc-authentication`. Its CI builds and publishes the Auth image; `platform-infra` consumes the published immutable image reference and deploys it.
- Keep deployment manifests such as `platform/auth-service/deployment.yaml`, `platform/microfe/**/deployment.yaml`, certificates, ingress, namespace, and Kustomize configuration in this repository.

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
