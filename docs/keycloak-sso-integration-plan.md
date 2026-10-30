# Keycloak SSO integration plan — TCE, Media and shared consumers

**Status:** source audit complete; staged implementation required. No application cutover or production credential/config changes are authorized by this plan.
**Date:** 2026-10-26
**Coordinator:** `phanthienquoc/platform-infra`

## Executive finding

Keycloak is not missing from infrastructure. The repository contains a Keycloak workload and a separate `sso.mrcute.space` ingress/deployment lane. Central Auth also has an OIDC resource-server foundation. What is missing is verified end-to-end OIDC client/session integration across application repositories.

Do not equate a running Keycloak pod or a successful discovery endpoint for the `master` realm with a working `mrcute` realm and app SSO.

## Source audit

| Repository | Current state found in source | Decision |
|---|---|---|
| `phanthienquoc/platform-infra` | Keycloak manifests, TLS/ingress and dedicated deployment workflow exist. Docs contain conflicting historical rollout statements, so current live state and the `mrcute` realm must be re-verified. | Own topology, environment references and safe rollout; never commit secret values. |
| `phanthienquoc/phanthienquoc-authentication` | `KeycloakTokenService` uses JWKS and validates issuer, audience, expiry and RS256; guarded `GET /api/oidc/me` extracts roles and persists minimal identity metadata. Legacy password/JWT/refresh/MFA/passkey flows remain. | Reuse this as a foundation; add/verify contract and integration tests before any consumer relies on it. |
| `phanthienquoc/TCE-dashboard` | Login uses shared-auth email/password, MFA and passkey routes. TCE API converts the shared cookie session to an internal JWT. No verified Keycloak browser flow or Keycloak token bridge was found. | Add opt-in non-production OIDC BFF/client integration plus explicit identity mapping; keep legacy mode default. |
| `phanthienquoc/media-generation` | Login proxy forwards to central Auth `/auth/login`; unauthenticated page redirects to the legacy Auth login URL. No verified Keycloak OIDC callback/client found. | Add a distinct Keycloak client and opt-in non-production integration after TCE contract passes. |
| StockDividend / MicroFE shell / WebSocket | Shared-auth references/introspection exist, but this audit did not establish full OIDC compatibility. | Audit each consumer before including it in the SSO completion claim. |

## Target contract

- Identity Provider: Keycloak at `https://sso.mrcute.space`, intended realm `mrcute`.
- Central Auth API: `https://auth.mrcute.space`, retaining existing legacy routes during migration.
- Protocol: OpenID Connect Authorization Code Flow + PKCE S256; validate state and nonce; exact registered callback and logout URIs.
- API tokens: access token only, verified with JWKS signature, exact issuer, explicit audience, expiry and allowed algorithm. Never use ID tokens for API access.
- App identity: define a stable mapping between `(issuer, sub)`, the central Auth identity record and each app's authorization principal. Never assume Keycloak `sub` equals a legacy user UUID; matching email alone is not safe account linking.
- Web session: prefer a server-side BFF/HttpOnly Secure session boundary. Do not place client secrets in frontend variables or persist bearer/refresh tokens in localStorage.
- Roles: deny by default; explicit least-privilege role-to-permission mapping per resource server.
- Compatibility: keep legacy auth enabled until all gates pass and cutover is explicitly reviewed.

## Implementation sequence

### Phase 0 — Baseline and configuration proof
- [ ] Verify DNS/TLS and current Keycloak deployment.
- [ ] Verify `/realms/mrcute/.well-known/openid-configuration` returns 200 and issuer exactly matches configuration.
- [ ] Inspect clients, exact redirect/logout URIs, allowed web origins, audience mapper and role claims without exposing secret values.
- [ ] Reconcile stale/conflicting deployment notes in this repo.

### Phase 1 — Central Auth contract
- [ ] Verify `KeycloakTokenService` negative tests for bad signature, wrong issuer/audience, expiry, malformed tokens and wrong algorithm.
- [ ] Add integration coverage for `GET /api/oidc/me`, role extraction and identity persistence failures.
- [ ] Define identity linking, logout/revocation expectations and the canonical API audience.
- [ ] Do not remove or silently alter existing login, refresh, MFA/recovery or passkey endpoints.

### Phase 2 — TCE (first consumer, non-production)
- [ ] Add opt-in OIDC callback/BFF or explicitly reviewed token flow behind a disabled-by-default feature flag.
- [ ] Bridge authenticated Keycloak identity into TCE API authorization only after mapping is proven; do not trust a decoded token or client-supplied user ID.
- [ ] Add state/nonce/PKCE, CSRF, role-denial, expiry, logout, outage and legacy-regression tests.
- [ ] Keep current legacy login as default until acceptance tests pass.

### Phase 3 — Media (second consumer, non-production)
- [ ] Register a separate client with exact Media callback/logout URIs.
- [ ] Implement the same session and identity contract; keep client secrets server-only.
- [ ] Test SSO with TCE, access denial, logout and legacy mode.

### Phase 4 — Other consumers and production cutover
- [ ] Audit StockDividend, MicroFE shell, WebSocket and any other shared-auth consumers.
- [ ] Verify one-login access to TCE and Media, role mapping, MFA, session expiry, logout and outage behavior.
- [ ] Exercise rollback and promote immutable images using the narrowest deployment lane.
- [ ] Switch production only after explicit cutover approval; no bulk account/session migration or DB mutation as an incidental CI/deploy side effect.

## Definition of done

- Every included app has a registered, least-privilege Keycloak client and verified callback/logout configuration.
- Central Auth and every resource API validate access tokens server-side with exact issuer/audience/signature/expiry checks.
- Identity linking and role mapping are tested and deny-by-default.
- Cross-app SSO and logout/session behavior are proven end-to-end in non-production.
- Legacy paths remain available through a tested rollback window.
- CI is green on the exact reviewed commit; production deployment is separately verified.
