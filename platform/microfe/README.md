# MicroFE platform bootstrap

This layer owns the platform shell and shared WebSocket gateway. The canonical Auth service is managed independently by `platform/auth-service`.

## Public hosts
- app.mrcute.space -> microfe-shell
- auth.mrcute.space -> microfe-auth

TCE, StockDividend, and Media Generation remain independently deployable.

## Immutable image promotion

- `platform/microfe/kustomization.yaml` pins the Shell and WebSocket gateway to SHA-256 image digests.
- TCE-dashboard CI owns building, testing, and publishing these images from a full source commit SHA.
- Platform Infra owns GHCR digest verification, atomic GitOps promotion, reconciliation, and rollout health checks.
- Do not restore placeholder tags such as `0.1.0` or `RELEASE_SHA` in production manifests.
- The current pair was published from source commit `e6940ff911ea63338fb4f66eb903bcdf6c9825a8`; the application head subsequently advanced by one workflow-only commit.

A successful image publication or manifest validation is not proof of production health. Require the targeted K3s rollout and application health gate after promotion.
