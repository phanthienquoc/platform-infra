# Auth Central Phase 0/1 Evidence Pack

**Scope:** Documentation-only deliverable for Auth Central Phase 0 read-only audit and Phase 1 architecture/contract readiness. No production, database, secret, traffic, or application behavior changes.

## Current repo/source evidence

- Auth app source of truth: [phanthienquoc-authentication](https://github.com/phanthienquoc/phanthienquoc-authentication)
- GitOps source of truth: [platform-infra](https://github.com/phanthienquoc/platform-infra)
- Consumer repos: [TCE-dashboard](https://github.com/phanthienquoc/TCE-dashboard), [media-generation](https://github.com/phanthienquoc/media-generation)
- Orchestrator issue: [platform-infra#528](https://github.com/phanthienquoc/platform-infra/issues/528)
- Auth service integration issue already exists: [phanthienquoc-authentication#1](https://github.com/phanthienquoc/phanthienquoc-authentication/issues/1)

## Verified repository source (not live cluster)

| Layer | Declared source state |
|---|---|
| Host route | `auth.mrcute.space` in [Ingress manifest](https://github.com/phanthienquoc/platform-infra/blob/master/platform/microfe/ingress.yaml), host path `/` → Service `microfe-auth:80`, TLS secret reference `auth-mrcute-tls` |
| Runtime | [Deployment](https://github.com/phanthienquoc/platform-infra/blob/master/platform/auth-service/deployment.yaml), container port 4010 and health/readiness probes |
| Auth route prefix | [Central NestJS bootstrap](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/main.ts) applies global `api` but excludes `auth/{*path}`; [controller](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/auth.controller.ts) uses `@Controller('auth')` |
| Media login | [Media proxy](https://github.com/phanthienquoc/media-generation/blob/master/apps/frontend/app/api/auth/login/route.ts) POSTs to `/auth/login` and forwards `Set-Cookie` |
| Media identity check | [Media middleware](https://github.com/phanthienquoc/media-generation/blob/master/apps/backend/src/microfe-session.ts) calls `/auth/me` and forwards Cookie only; central [Auth controller](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/auth.controller.ts) implements `GET /auth/me` using a Bearer Authorization header |
| TCE route/cookie | [TCE Auth controller](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/auth/auth.controller.ts) has `@Controller('auth')` and sets refresh cookie path `/api/auth`; [TCE bootstrap](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/main.ts) sets global prefix `api`; [TCE docs](https://github.com/phanthienquoc/TCE-dashboard/blob/master/docs/fe-feats) describe `/api/auth/*` |
| JWT issuance | [TCE JWT service](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/auth/jwt.service.ts) signs HS256 with `sub`, `role`, `typ`, `iat`, `exp`, `jti`; inspected source does not emit `iss`/`aud`. [Central Auth JWT service](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/jwt.service.ts) emits and verifies `iss` and `aud`. This is a token-compatibility gate. |
| Persistence owner | Auth repo README says persistence uses `@supabase/supabase-js` service-role client and RPCs for selected atomic operations. Runtime secret values are owned through protected platform-infra `production` environment / Kubernetes Secret; do not move or expose them. |

## Contract gaps requiring decision and tests

1. **Route prefix:** TCE bootstrap sets global `/api` and TCE docs describe `/api/auth/*`; central Auth excludes `auth/*` from that prefix and intends external `/auth/*`. Media proxies call `/auth/login`. Decide an explicit compatibility contract rather than silently rewriting paths.
2. **Media /auth/me auth mode:** Media backend sends Cookie only; central Auth `GET /auth/me` requires `Authorization: Bearer`. TCE `platform-session.middleware.ts` also sends Cookie only to central `/auth/me`, then creates an internal TCE Bearer token. The central endpoint as inspected will not accept the cookie-only request unless another mechanism exists outside inspected source. Agree the server-to-server session contract and test it in non-production; do not infer a refresh cookie is an access credential.
3. **Refresh cookie path:** central Auth routes are intended at `/auth/*`, yet refresh cookie path is `/api/auth`; browser path matching may prevent cookie delivery to `/auth/refresh`. Validate intended path, domain and SameSite behavior in non-production before code changes.
4. **JWT compatibility:** TCE inspected JWT source issues HS256 tokens without `iss`/`aud`; central Auth emits/verifies `iss`/`aud`. Compare every consumer's actual token validation before changing either side. Do not generate or paste real tokens into audit artifacts.
5. **MFA/passkey routes:** complete method/path/DTO/response/status/error matrix including signup/login, refresh/replay, logout, MFA login/setup/enable/disable/recovery, and WebAuthn options/verification.
6. **Runtime state:** manifests do not prove current Deployment image, pod readiness, TLS certificate, routing behavior or secret readiness. These remain unknown because Phase 0 is source-audit only.

Evidence:
- [Central bootstrap](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/main.ts)
- [Central Auth controller](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/auth.controller.ts)
- [Central JWT service](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/jwt.service.ts)
- [TCE service bootstrap](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/main.ts)
- [TCE Auth controller](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/auth/auth.controller.ts)
- [TCE JWT service](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/auth/jwt.service.ts)
- [TCE platform-session middleware](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/platform-session.middleware.ts)
- [Media login proxy](https://github.com/phanthienquoc/media-generation/blob/master/apps/frontend/app/api/auth/login/route.ts)
- [Media session middleware](https://github.com/phanthienquoc/media-generation/blob/master/apps/backend/src/microfe-session.ts)

## Existing work reconciliation (partial evidence)

### Central Auth repository
- [Issue #1](https://github.com/phanthienquoc/phanthienquoc-authentication/issues/1) already tracks service completion and end-to-end compatibility; no duplicate implementation issue required.
- PRs [#3](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/3), [#4](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/4), [#5](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/5), [#6](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/6), [#7](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/7), [#8](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/8) and [#9](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/9) were observed merged in connected API results, covering persistence, release image/tag, dispatch handoff and secret ownership docs.
- Auth repo branch search returned `master` and `chore/auth-release-infra-owned-secrets`, `feat/auth-gitops-handoff`, `feat/auth-owned-runtime-secret-provisioning`, `feat/auth-service-cicd`, `feat/auth-service-gitops-deploy`, `feat/nestjs-auth-service`, `fix/release-version-sha-tags`, `refactor/auth-secret-ownership`. These feature branches are not equivalent to open PRs; compare branch SHAs and PR status, not names alone.

### platform-infra
- [PR #505](https://github.com/phanthienquoc/platform-infra/pull/505), [#508](https://github.com/phanthienquoc/platform-infra/pull/508), and [#512](https://github.com/phanthienquoc/platform-infra/pull/512) were observed merged, covering canonical image path, versioned image tag convention and reconciliation scope.
- [PR #510](https://github.com/phanthienquoc/platform-infra/pull/510) was observed open and touches Auth image pin; do not assume it merged.
- Current manifest consistency needs targeted validation: `platform/auth-service/deployment.yaml` declares full SHA `8138295b27f8754d96255d292e3ec630270abfe9`, while `platform/auth-service/kustomization.yaml` specifies `prod-v1.0.0-b65396d`. These source files appear to declare conflicting image identities unless Kustomize rewrite behavior resolves differently; render manifests in CI to establish effective image before production claims.
- PRs [#151](https://github.com/phanthienquoc/platform-infra/pull/151), [#152](https://github.com/phanthienquoc/platform-infra/pull/152), [#153](https://github.com/phanthienquoc/platform-infra/pull/153), [#154](https://github.com/phanthienquoc/platform-infra/pull/154), [#155](https://github.com/phanthienquoc/platform-infra/pull/155), [#156](https://github.com/phanthienquoc/platform-infra/pull/156) were checked individually and remain open. They are bot-created TCE web/service promotions with distinct immutable tags, updated on 2026-09-24; compare each with current release/manifests before recommendation. No batch-close recommendation is made.
- Branch searches are paginated but do not return PR association or SHA in the search result. The first pages show a large `platform-infra` inventory (including auth `feat/*`, `fix/*`, `refactor/*` branches) and nine Auth repo branches; this is not sufficient to mark every branch/PR reconciled. Match branch heads with PR refs/commit history to complete B-00.

## Sprint 0 issue registry already created

- [#528 — Sprint 0 preflight / orchestration](https://github.com/phanthienquoc/platform-infra/issues/528)
- [#529 — B-00 reconcile existing Auth work](https://github.com/phanthienquoc/platform-infra/issues/529)
- [#530 — A-01 inventory implementations and ownership](https://github.com/phanthienquoc/platform-infra/issues/530)
- [#531 — A-04 Supabase readiness](https://github.com/phanthienquoc/platform-infra/issues/531)
- [#532 — A-07 branch/PR reconciliation](https://github.com/phanthienquoc/platform-infra/issues/532)
- [#533 — A-02 hostname and route-prefix validation](https://github.com/phanthienquoc/platform-infra/issues/533)
- [#534 — A-03 TCE/Media contract matrix](https://github.com/phanthienquoc/platform-infra/issues/534)
- [#535 — A-05 ADR from evidence](https://github.com/phanthienquoc/platform-infra/issues/535)
- [#536 — A-06 pilot and go/no-go recommendation](https://github.com/phanthienquoc/platform-infra/issues/536)

Dependency proposal: #529 → #530/#532; #530 → #533 → #534; #531 runs independently; #531/#533/#534 → #535; #534/#535 → #536. Resolve actual issue status/relationships before executing each goal. The connected GitHub tool cannot currently add items/fields to GitHub Projects v2, so membership in [Project #2](https://github.com/users/phanthienquoc/projects/2) remains unverified.

## Supabase and database gate

The existing Notion audit records project metadata as PostgreSQL `17.6.1.084` in `ap-southeast-1`, status `ACTIVE_HEALTHY`; it is not yet proven to be the approved Keycloak target. TLS/network mode, pooler type, connection limits/headroom and compatibility with a selected Keycloak release remain unknown. Existing advisors reported informational RLS-without-policy and unindexed-FK findings. These are not automatic instructions to change schemas. Do not execute DDL/DML or alter roles, policies, credentials or data during Phase 0.

## Phase 0 acceptance checklist

- [ ] Complete B-00 classification across both repositories; include search scope, pagination, branch heads, PR base/head, activity, status checks and recommendation.
- [ ] Complete A-01 owner/implementation inventory with commit-pinned references.
- [ ] Complete A-02 route/prefix/cookie-path trace from source and manifests; do not contact live endpoint as part of read-only audit.
- [ ] Complete A-03 full methods/paths/DTOs/responses/errors/JWT/cookie matrix and add non-production test proposals for each mismatch.
- [ ] Complete A-04 intended Supabase project confirmation and read-only connection/security compatibility report against one explicitly selected Keycloak candidate.
- [ ] Publish results in Notion hub and update matching issues with evidence.
- [ ] Keep all production/database/security mutations out of Phase 0.

## Phase 1: design and implementation contract

Phase 1 must not start Keycloak infrastructure until audit evidence is reviewed. Required deliverables:
1. ADR explicitly compares (a) current NestJS Auth as sole identity/auth service, (b) Keycloak as an OIDC provider/broker alongside NestJS, and (c) replacing selected NestJS responsibilities with Keycloak. Include ownership, identity mapping, existing password hashes, sessions/refresh, MFA/passkeys, JWT claims/issuer/audience, cookie/CSRF/CORS, client integration, data layout, operations, observability, rollback and alternatives.
2. Choose a specific supported Keycloak version and evidence-backed database connection mode only after A-04; verify official requirements and test against an isolated non-production target. Do not assume the currently visible Supabase project is approved.
3. Define OIDC proof requirements: discovery document, authorization-code + PKCE, state/nonce validation, issuer/audience/signature/expiry checks, logout/session behavior and JWKS rotation.
4. Define the pilot using A-03 contract evidence and rollback simplicity. TCE remains last; no application migration or traffic cutover before human approval.
5. Record open questions and explicit human decisions; only move deliverables to Review when artifact/evidence exists. Human marks Done.

## Security hard stops

- No autonomous merge/close of PRs or branch deletion.
- No production DNS, ingress, traffic, secret, env or Kubernetes changes.
- No production credential creation/rotation/revocation.
- No database schema/role/policy/data mutations in Phase 0.
- No Keycloak rollout, application migration or traffic cutover until ADR and pilot are approved.
- Never write actual credentials, tokens, database URLs with credentials or sensitive user data to GitHub/Notion.
