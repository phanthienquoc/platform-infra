# Auth Central Phase 0/1 Evidence Pack

**Scope:** Documentation-only deliverable for Auth Central Phase 0 read-only audit and Phase 1 architecture/contract readiness. No production, database, secret, traffic, or application behavior changes.

## Current repo/source evidence

- Auth app source of truth: [phanthienquoc-authentication](https://github.com/phanthienquoc/phanthienquoc-authentication)
- GitOps source of truth: [platform-infra](https://github.com/phanthienquoc/platform-infra)
- Consumer repos: [TCE-dashboard](https://github.com/phanthienquoc/TCE-dashboard), [media-generation](https://github.com/phanthienquoc/media-generation)
- Orchestrator issue: [platform-infra#528](https://github.com/phanthienquoc/platform-infra/issues/528)
- Auth service integration issue already exists: [phanthienquoc-authentication#1](https://github.com/phanthienquoc/phanthienquoc-authentication/issues/1)

## Verified in repository source (not live cluster)

| Layer | Declared source state |
|---|---|
| Host route | `auth.mrcute.space` in [Ingress manifest](https://github.com/phanthienquoc/platform-infra/blob/master/platform/microfe/ingress.yaml), host path `/` → Service `microfe-auth:80`, TLS secret reference `auth-mrcute-tls` |
| Runtime | [Deployment](https://github.com/phanthienquoc/platform-infra/blob/master/platform/auth-service/deployment.yaml), container port 4010 and health/readiness probes |
| Auth route prefix | [Central NestJS bootstrap](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/main.ts) applies global `api` but excludes `auth/{*path}`; [controller](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/auth.controller.ts) uses `@Controller('auth')` |
| Media login | [Media proxy](https://github.com/phanthienquoc/media-generation/blob/master/apps/frontend/app/api/auth/login/route.ts) POSTs to `/auth/login` and forwards `Set-Cookie` |
| Media identity check | [Media middleware](https://github.com/phanthienquoc/media-generation/blob/master/apps/backend/src/microfe-session.ts) calls `/auth/me` and forwards Cookie only; central [Auth controller](https://github.com/phanthienquoc/phanthienquoc-authentication/blob/master/src/auth/auth.controller.ts) implements `GET /auth/me` using a Bearer Authorization header |
| TCE route/cookie | [TCE Auth controller](https://github.com/phanthienquoc/TCE-dashboard/blob/master/apps/service/src/auth/auth.controller.ts) has `@Controller('auth')` and sets refresh cookie path `/api/auth`; [TCE docs](https://github.com/phanthienquoc/TCE-dashboard/blob/master/docs/fe-feats) document `/api/auth/*` |

## Contract gaps requiring a decision and tests

1. **Route prefix:** TCE documents `/api/auth/*`; central Auth deliberately exposes `/auth/*`. Trace TCE global prefix and any proxy/rewrite rules before deciding how to converge.
2. **Media /auth/me auth mode:** Media sends Cookie only; central Auth source checks `Authorization: Bearer`. Agree on a server-to-server contract and test it with a non-production user/session. Do not assume a cookie is an access credential.
3. **Refresh cookie path:** central Auth route prefix is `/auth/*`, yet refresh cookie path is `/api/auth`. Browser behavior may not send that cookie to `/auth/refresh`; validate the intended path and origin/domain behavior in non-production before proposing code changes.
4. **JWT:** capture exact algorithm, issuer, audience, claims, TTL and verification behavior from source and compare to both consumers. No real token generation during audit.
5. **Runtime state:** manifest evidence does not prove current Deployment image, readiness, TLS certificate or live route. These remain unverified under the read-only Phase 0 scope.

## Phase 0 registry

- [#529 B-00 reconcile existing work](https://github.com/phanthienquoc/platform-infra/issues/529)
- [#530 A-01 inventory owners and implementations](https://github.com/phanthienquoc/platform-infra/issues/530)
- [#531 A-04 Supabase readiness](https://github.com/phanthienquoc/platform-infra/issues/531)
- [#532 A-07 branch/PR reconciliation](https://github.com/phanthienquoc/platform-infra/issues/532)
- [#533 A-02 hostname and route contract](https://github.com/phanthienquoc/platform-infra/issues/533)
- [#534 A-03 consumer contract matrix](https://github.com/phanthienquoc/platform-infra/issues/534)
- [#535 A-05 ADR from evidence](https://github.com/phanthienquoc/platform-infra/issues/535)
- [#536 A-06 pilot/go-no-go](https://github.com/phanthienquoc/platform-infra/issues/536)

Proposed order: #529 → #530/#532; #530 → #533 → #534; #531 runs independently; #531/#533/#534 → #535; #534/#535 → #536. Validate actual GitHub dependencies/status before execution.

## Phase 1 deliverable requirements

- ADR compares: NestJS remains sole auth service; Keycloak operates as an OIDC provider/broker alongside NestJS; or Keycloak replaces selected auth responsibilities. Do not presuppose replacement.
- Describe identity mapping and existing password-hash compatibility, refresh/session behavior, MFA/passkeys, JWT issuer/audience/claims, cookie/CSRF/CORS, consumer changes, data layout, operations, observability, rollback and alternatives.
- Choose a specific supported Keycloak release and connection mode only after A-04 establishes intended database and compatibility; verify against official documentation and an isolated non-production target.
- Define OIDC acceptance evidence: discovery, authorization-code + PKCE, state/nonce, issuer/audience/signature/expiry checks, logout/session behavior and JWKS rotation.
- Select pilot based on A-03 consumer divergence and rollback simplicity; TCE remains last.
- Require explicit human approval for ADR and pilot before infrastructure rollout or app migration.

## Hard stops

- No PR merge/close or branch deletion without human decision.
- No production DNS, ingress, secrets, environment, traffic, Kubernetes changes or rollout.
- No production credential create/rotate/revoke.
- No schema/role/policy/data mutations in Phase 0.
- No Keycloak deployment, consumer migration or traffic cutover before architecture/pilot approval.
- Keep credentials, real tokens and credential-bearing database URLs out of repository and documentation.

## Remaining work before Phase 0 can be marked complete

- Complete per-branch and per-PR inventory with pagination, base/head, last activity, state, CI evidence and recommendation for both repositories; current search is partial.
- Finish route/prefix trace in TCE and inspect configured proxies without touching live traffic.
- Complete full API table with methods, DTOs, response and error contracts, JWT claims, refresh/logout and cookie attributes.
- Confirm approved Supabase project from authoritative documentation; leave TLS/network/pooler/connection headroom and Keycloak compatibility unknown unless directly observed.
- Add evidence links and update the matching issues; only mark Review when deliverables exist. GitHub Projects v2 membership is unverified because the connected GitHub tool does not expose add-item/field-write actions.
