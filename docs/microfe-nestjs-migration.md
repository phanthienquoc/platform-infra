# MicroFE NestJS rollout contract

MicroFE Auth must be a standalone NestJS + TypeScript service. **No Supabase SDK, Data API, Supabase Auth, RPC-based auth logic, or Supabase service-role key in the auth runtime.**

## Auth runtime
- NestJS owns authentication/authorization business logic: password verification, MFA/recovery policy, session lifecycle, refresh rotation/reuse detection, CSRF, passkey challenge and credential-counter logic, role checks.
- PostgreSQL is the data store. Connect using the standard `pg` driver with `DATABASE_URL` and bounded `DB_POOL_MAX`; use parameterized SQL and transactions for atomic operations.
- Reuse the existing `public.users`, `public.refresh_sessions`, `public.mfa_recovery_codes`, `public.auth_passkey_challenges`, and `public.auth_passkey_credentials` tables. Preserve API paths, cookie names/domain and existing password hash compatibility.
- Do not create duplicate user/session tables. The Auth branch includes the narrowly scoped migration `microfe/auth/migrations/0001_allow_mfa_challenges.sql` to allow the `mfa` purpose on the shared challenge table; review and apply it through the normal database migration process before deploying.
- Store only secret references in Kubernetes manifests; never print or commit secret values. The runtime Secret must provide `DATABASE_URL`, `JWT_SECRET`, and `MFA_ENCRYPTION_KEY` (plus passkey RP/origin config as non-secret values).
- Never copy Supabase service-role credentials into this service. Confirm existing DB URL secret source and network/SSL connectivity using key names only, without exposing credentials.
- Preserve immutable SHA/digest image promotion.

## Gates before applying production
1. NestJS build, lint, unit and end-to-end tests pass.
2. Review and apply `microfe/auth/migrations/0001_allow_mfa_challenges.sql` to the existing database before deploying MFA challenge persistence.
3. Confirm existing password hash formats and passkey schema compatibility.
4. Test refresh rotation/reuse, recovery-code single use, MFA challenge single use and passkey challenge single use under concurrent requests.
4. Confirm Kubernetes secret source has `DATABASE_URL`, `JWT_SECRET` and `MFA_ENCRYPTION_KEY`; do not display values.
6. Kustomize validation succeeds and immutable image digest is available.
7. Rollout probes pass and HTTPS health checks return expected results.

No production deploy or schema mutation before all gates pass.
