# StockDividend runtime contract

The production GitOps application owns exactly two long-running Deployments:

- **Admin UI**: Next.js application at port 3000, managed by `apps/stockdividend/base/admin.yaml`.
- **Go Backend**: API at port 8080, managed by `apps/stockdividend/base/backend.yaml`.

The scraper is a separately scheduled app-owned job; it is not a long-running production Deployment. The production Ingress routes `mrcute.space`, `www.mrcute.space`, and `admin.mrcute.space` to `stock-admin`, and `api.mrcute.space` to `stock-backend`.

The old `stock-frontend` Deployment/image is legacy cluster residue: there is no matching `user`/frontend source, Dockerfile, Kustomize resource, Service, or production Ingress route in the current app/release contract. It may remain running until a separately authorized cleanup, but it is not owned by the current StockDividend release. Do not include it in rollout, restart, rollback-readiness, or health gates, and do not delete or scale it as part of this contract.

The current backend image does not compile the migration source into an executable binary; migration execution remains blocked until the application image is corrected.
