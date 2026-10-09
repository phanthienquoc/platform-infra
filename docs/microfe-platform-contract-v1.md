# MicroFE Platform Contract v1

## Public boundaries
- Shell: app.mrcute.space
- Auth: auth.mrcute.space
- API: api.mrcute.space
- WebSocket: ws.mrcute.space

## Auth
- Self-hosted authentication.
- Browser uses an HttpOnly session boundary.
- Supabase Auth is not used; the self-hosted Auth service uses the existing Supabase Data API and canonical `public.users` / `public.refresh_sessions` tables.
- The browser never receives `SUPABASE_SERVICE_ROLE_KEY`; production injects it only into the Auth server from the existing TCE runtime secret.
- Auth owns identity, sessions, rotation, revocation, RBAC, logout, CSRF, rate limits, audit events, and request IDs.
- Browser API: GET /auth/me, POST /auth/login, POST /auth/refresh, POST /auth/logout, POST /auth/logout-all.
- Auth errors use stable code/message/requestId fields.
- Authentication material is never exposed through browser storage or URLs.

## WebSocket
- Prefer one browser connection.
- Use the existing browser session boundary.
- Do not authenticate through URL parameters.
- Support heartbeat, exponential reconnect with jitter, subscription recovery, duplicate suppression, ordering checks, and session-expiry handling.
- REST/BFF is authoritative; WebSocket is delivery.
- Subscription access is checked for the authenticated principal.
- Event envelope: id, channel, event, timestamp, sequence, data.
- Sequence gaps require REST/BFF resync.
- Session revocation closes the connection and requires re-authentication.

## MicroFE boundary
- TCE-dashboard, StockDividend, and Media Generation keep domain state and business logic independent.
- Shared browser surface is limited to platform authentication and realtime contracts.
- Supabase remains data-plane only; Supabase Realtime is not used.

## Production ownership
- platform-infra remains the Kubernetes source of truth.
- Existing GitOps promotion and VPS reconciliation remain unchanged.
- Scheduled reconciliation must not change production image tags unless explicitly authorized.
