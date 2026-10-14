# Keycloak production deployment plan

## Architecture decision
- Keycloak external URL: https://sso.mrcute.space
- Existing NestJS Auth API remains https://auth.mrcute.space and is not rerouted.
- Supabase PostgreSQL project `gtqovpusfyyvxpeezxlo`, Supavisor Session Pooler, database `postgres`, isolated schema `keycloak`.
- Keycloak is a separate workload and is targeted explicitly through a dedicated deployment lane. TCE/Media integration is not migrated in this PR.

## Supabase implementation state
- Schema `keycloak` was created and verified empty before workload implementation.
- Login role `keycloak_runtime` was created as `LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`.
- It has database CONNECT and schema USAGE/CREATE on `keycloak`; it has no membership in privileged application roles. Live privilege queries confirmed no SELECT/INSERT/UPDATE/DELETE rights on `public.users`, and no USAGE on `auth`, `storage`, or `extensions`.
- The role **has no password yet**. The operator must set a unique secret through a protected database administration channel and use the identical value for GitHub Environment secret `KEYCLOAK_DB_PASSWORD`. This password must never be sent in chat, written in migration SQL, or committed to Git.
- Keycloak role must not be the `postgres` owner connection. Inspect effective grants/extension PUBLIC access and verify TLS JDBC connectivity before production activation.

## GitHub implementation branch
Merged PR: [#542](https://github.com/phanthienquoc/platform-infra/pull/542), merge commit `fa5a5da56b6d66ffaff095fa887637c25b800265`.

Files added:
- `platform/keycloak/deployment.yaml`: separate Keycloak Deployment and ClusterIP Service, image `quay.io/keycloak/keycloak:26.8.1`, production start mode, pinned hostname, separate DB schema, bounded pool and probes.
- `platform/keycloak/kustomization.yaml`, `ingress.yaml`, `certificate.yaml`: isolated SSO route/certificate for `sso.mrcute.space`.
- `platform/keycloak/README.md`: deployment contract and safety gates.
- `scripts/bootstrap-runner.sh`: v10 allowlist actions for stdin-only Secret provisioning, Secret verification and a Keycloak-only Kustomize apply/rollout/read path. The `Bootstrap self-hosted runner` run `38574201661` completed successfully on the merge commit and installed the updated wrapper.
- `.github/workflows/reconcile-vps.yml`: explicit `target_app=keycloak` deployment lane; skips regular environment apply and skips actions that restart/alter other app workloads.
- `scripts/verify-workload-health.sh`, `scripts/validate-workflow-contracts.py`, `.github/workflows/validate-manifests.yml`: Keycloak health/manifest/workflow contract validation.
- Existing shared ingress still routes `auth.mrcute.space` to `microfe-auth`; new SSO route is a separate resource inside `platform/keycloak`, not included in regular app reconciliation.

## Required GitHub Environment `production` secrets
- `KEYCLOAK_DB_URL` = `jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require`
- `KEYCLOAK_DB_USERNAME` = `keycloak_runtime.gtqovpusfyyvxpeezxlo` (Supavisor username syntax)
- `KEYCLOAK_DB_PASSWORD` = password set on `keycloak_runtime` using a protected database admin channel
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

The earlier screenshot showed secret names only; it did not prove their values or that they are in the `production` Environment. The workflow does not read secret values through the GitHub connector. Never paste passwords in chat.

## Production gates before first activation
1. Set the database role password through a protected path, update the `KEYCLOAK_DB_PASSWORD` Environment secret, and verify the exact Environment scope.
2. Verify effective grants, TLS connectivity from the Kubernetes VPS, database connection headroom, and backups/PITR restore path.
3. Runner bootstrap completed after merge (run `38574201661`); the Keycloak lane still performs a live policy-version check and refuses to continue unless the wrapper reports v10.
4. Verify DNS for `sso.mrcute.space` points to the current Traefik public address.
5. Merge after CI/review, then manually run `reconcile-vps` with `mode=apply` and `target_app=keycloak`. This target applies only `platform/keycloak`, not `environments/prod`.
6. Verify rollout/readiness, TLS and `https://sso.mrcute.space/realms/master/.well-known/openid-configuration`; test restart persistence and rollback before integrating any app clients.

## Post-merge verification
- `validate-manifests` run `38574201727`: success.
- `validate-github-actions` run `38574201892`: success.
- Shared `reconcile-vps` run `38574201455`: success; preflight reported no drift, production manifest apply was skipped, all existing app health lanes passed, and the Keycloak lane was skipped because this was the regular `target_app=all` path.
- Latest VPS inspection artifact (`debug/vps-latest.md`, generated `2026-10-14T13:46:09Z`) contains no Keycloak pod or SSO ingress entry. The live cluster has not been activated for Keycloak.

## Not done yet
- No DB password was set on `keycloak_runtime`.
- No Keycloak Kubernetes Secret was provisioned.
- No Keycloak workload/ingress/certificate has been applied to the live cluster.
- DNS has not been verified.
- No app client, user or session migration has been performed.
