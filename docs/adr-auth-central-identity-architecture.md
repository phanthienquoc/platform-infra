# ADR: Central Identity Architecture

**Status:** Draft — decision pending evidence and explicit owner review  
**Date:** 2026-10-14  
**Decision owners:** Platform/Auth maintainers  
**Related issues:** [#528](https://github.com/phanthienquoc/platform-infra/issues/528), [#530](https://github.com/phanthienquoc/platform-infra/issues/530), [#531](https://github.com/phanthienquoc/platform-infra/issues/531), [#533](https://github.com/phanthienquoc/platform-infra/issues/533), [#534](https://github.com/phanthienquoc/platform-infra/issues/534), [#535](https://github.com/phanthienquoc/platform-infra/issues/535)

## Context and source-backed current state

- `phanthienquoc-authentication` owns NestJS auth application code, tests, Docker and migrations. `platform-infra` owns GitOps manifests, image promotion and deployment reconciliation.
- Repository manifests declare `auth.mrcute.space` → Ingress `microfe-public` → Service `microfe-auth:80` → Deployment `microfe-auth`, container port 4010. This is repository state, not proof of live runtime.
- Central Auth uses a global `/api` prefix but excludes `auth/{*path}`, intending auth routes under `/auth/*` and health/readiness under `/api/*`.
- Central Auth access JWTs use HS256 with configured `iss` and `aud`; access token is returned in JSON. The refresh token is a separate HttpOnly cookie named `tce_refresh_token`.
- Current refresh cookie settings include `HttpOnly`, `SameSite=Lax`, `Secure` outside development and `Path=/api/auth`.
- TCE docs/controllers describe `/api/auth/*`; central Auth intends `/auth/*`.
- Media backend and TCE platform middleware forward Cookie to central `/auth/me`, while central `GET /auth/me` currently requires an Authorization Bearer access token. Source contract is inconsistent and must be resolved by an explicit design + non-production integration tests.
- The currently connected Supabase project metadata is PostgreSQL 17.6.1.084 in `ap-southeast-1`, but approval as a Keycloak target, network/TLS/pooler mode, plan limits and available connection headroom are not proven.
- Auth CI and GitOps release work exists and must be reused; do not duplicate existing release pipelines or runtime secret ownership.

## Decision criteria

Any selected option must document:
1. Authentication/authorization responsibility and ownership.
2. Compatibility with existing accounts, password hashes, user identifiers and role claims.
3. Access-token issuer, audience, algorithm, expiry, key distribution/rotation and validation by every consumer.
4. Browser session, refresh-token rotation/reuse detection, logout/revocation, cookie scope, CSRF and CORS.
5. MFA/TOTP, recovery codes and WebAuthn/passkey behavior and parity.
6. Service-to-service identity/session contract for Media and TCE.
7. Data model, persistence, database compatibility, connection capacity, backup/restore and operational ownership.
8. Migration sequencing, rollback, observability, incident recovery and user impact.

## Options

### Option A — Keep NestJS Auth as the sole central auth service

NestJS continues to own password verification, sessions/refresh, JWT issue/validation, MFA/recovery and passkeys. Consumers converge on a documented API contract and add integration coverage.

**Benefits:** minimizes new identity-provider infrastructure and preserves existing service responsibilities and migration path.  
**Costs/risks:** custom authentication/session lifecycle remains the platform's responsibility; standards-based OIDC provider features would need to be implemented or delegated separately.

### Option B — Operate Keycloak alongside NestJS as an OIDC provider/broker

Keycloak becomes the OIDC/OAuth identity provider for browser/client authentication; NestJS remains as a domain/auth adapter only where its existing business rules, legacy password validation, session semantics or internal APIs are still needed. Exact division of ownership must be explicit.

**Benefits:** standards-based OIDC discovery and protocol handling can be delegated to a dedicated IdP while app-specific behavior can be migrated incrementally.  
**Costs/risks:** introduces another security-critical service and identity lifecycle; user/password/session/MFA/passkey mapping and duplicate authentication paths require a carefully tested contract.

### Option C — Replace selected NestJS authentication responsibilities with Keycloak

Keycloak becomes the primary user identity and login system; NestJS transitions to a narrower profile/authorization/domain boundary or is retired only after all consumers and dependencies are accounted for.

**Benefits:** reduces custom authentication functionality if feature parity and all consumers are proven.  
**Costs/risks:** highest migration risk due existing user identifiers, scrypt password hash compatibility, refresh/session behavior, MFA/recovery/passkeys, JWT claims and app authorization assumptions. No replacement is justified without evidence and rollback proof.

## Provisional recommendation

**No option is approved yet.** Do not deploy Keycloak or switch production traffic until Phase 0 evidence is complete, the ADR is reviewed, and a pilot/rollback plan is approved.

A lower-risk starting posture is to stabilize and test the existing NestJS service contract first, then decide whether Keycloak adds enough value to justify a separate OIDC boundary. This is a sequencing recommendation, not a final architecture selection.

## Required unresolved questions

- Which Supabase project is explicitly approved for a Keycloak database, if any? Can the exact candidate Keycloak release connect using a supported PostgreSQL mode within network/TLS and connection-budget constraints?
- Should Keycloak be a separate OIDC provider/broker, or is the intention to replace NestJS login/session functionality?
- What is the canonical external auth route: `/auth/*`, `/api/auth/*`, or a tested compatibility layer? No route equivalence is assumed.
- Should `/auth/me` require Bearer access tokens, or should a separate, explicitly named server-side session-introspection endpoint be designed? A refresh token must not silently become an access credential.
- What cookie path/domain is required by all app origins and paths? Browser and server-side forwarding must be tested without exposing tokens.
- What exact JWT claims/issuer/audience are required by TCE, Media and any other consumers? How is a transition from legacy TCE-issued HS256 tokens managed without a sudden issuer/key mismatch?
- Can the legacy scrypt `salt:hex` password hashes be validated or migrated safely? What is the user-ID mapping if IdP `sub` values differ from existing Supabase IDs?
- Are MFA/TOTP, one-time recovery codes and WebAuthn/passkeys required on day one, and what is the verified parity/migration path?
- Which app is the safest pilot based on the completed consumer contract matrix and rollback simplicity?

## Required follow-up artifacts before approval

- [ ] Complete branch/PR reconciliation in #529/#532; human approval for any merge/close action.
- [ ] Complete source/deployment ownership inventory in #530.
- [ ] Complete route/prefix evidence in #533.
- [ ] Complete per-consumer contract matrix and mismatch tests in #534.
- [ ] Complete read-only database/Keycloak compatibility report in #531.
- [ ] Update this ADR with answers, chosen option, consequences, accountable owners and rollback.
- [ ] Pilot proposal in #536 includes baseline, observable success/failure thresholds agreed by a human, migration steps and rollback triggers.
- [ ] Obtain human ADR + pilot approval before infrastructure deployment or consumer migration.

## Rollout and safety

- No production deployment, DNS/ingress/traffic/secret/env change in this ADR task.
- No database DDL/DML, roles, policies, credentials or data mutation as part of audit/design.
- No automatic branch deletion, PR merge or PR closure.
- Required security/data-integrity checks block the affected release; independent safe work may continue.
- TCE migration is last, after the pilot and other app migrations are verified.
