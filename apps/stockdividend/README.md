# StockDividend runtime contract

The production GitOps application owns exactly two long-running Deployments:

- **Admin UI**: Next.js application at port 3000, managed by `apps/stockdividend/base/admin.yaml`.
- **Go Backend**: API at port 8080, managed by `apps/stockdividend/base/backend.yaml`.

The scraper is a separately scheduled app-owned job; it is not a long-running production Deployment. The production Ingress routes `mrcute.space`, `www.mrcute.space`, and `admin.mrcute.space` to `stock-admin`, and `api.mrcute.space` to `stock-backend`.

The old `stock-frontend` Deployment/image is legacy cluster residue: there is no matching `user`/frontend source, Dockerfile, Kustomize resource, Service, or production Ingress route in the current app/release contract. It may remain running until a separately authorized cleanup, but it is not owned by the current StockDividend release. Do not include it in rollout, restart, rollback-readiness, or health gates, and do not delete or scale it as part of this contract.

The StockDividend application Dockerfile now compiles `cmd/migrate` into a static `/app/migrate` executable (StockDividend PR #31, master commit `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`). Exact-head CI built a non-publishing amd64 runtime image, verified the executable, and confirmed it exits on missing `MONGO_URI` before any database connection. This is source/CI evidence only: the post-merge ARM64 publisher run and production digest are not yet verified, and the production overlay still references the old Admin/Backend tag `12d63b4`. Do not execute the migration from a production Pod or deployment workflow; any database migration requires a separately reviewed, explicitly authorized operator procedure after the new ARM64 image is published and promoted.
