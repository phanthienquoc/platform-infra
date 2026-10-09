# MicroFE NestJS rollout contract

MicroFE backend services use NestJS + TypeScript. Do not deploy the Express `server.mjs` Auth implementation.

## Auth runtime
- Keep Auth self-hosted in the existing K3s namespace and retain the externally visible API/cookie contract while the NestJS replacement is developed.
- Reuse the existing Supabase project and `public.users`, `public.refresh_sessions`, MFA and passkey tables.
- Store only credential references in Kubernetes Secret manifests; never commit secret values.
- Do not assume `tce-prod/tce-app-secrets` is the source until the live namespace and required keys are verified without printing values.
- Preserve immutable SHA/digest image promotion.

## Gates before applying production
1. NestJS build, lint, unit and end-to-end tests pass.
2. The implementation uses the existing password format and fully supports enabled MFA/passkeys.
3. Verify `rotate_refresh_token` arguments, return fields, reuse detection and function grants against the live schema.
4. Kustomize validation succeeds and secret keys are verified by names only.
5. Rollout probes pass, all three MicroFE deployments reach desired replicas, and HTTPS health checks pass.

No production schema mutation should occur for this migration without a reviewed migration and explicit evidence it is required.
