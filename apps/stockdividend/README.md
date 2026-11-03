# StockDividend runtime contract

The production GitOps application owns exactly two long-running Deployments:

- **Admin UI**: Next.js application at port 3000, managed by `apps/stockdividend/base/admin.yaml`.
- **Go Backend**: API at port 8080, managed by `apps/stockdividend/base/backend.yaml`.

The scraper is a separately scheduled app-owned job; it is not a long-running production Deployment. The production Ingress routes `mrcute.space`, `www.mrcute.space`, and `admin.mrcute.space` to `stock-admin`, and `api.mrcute.space` to `stock-backend`.

The old `stock-frontend` Deployment/image is legacy cluster residue: there is no matching `user`/frontend source, Dockerfile, Kustomize resource, Service, or production Ingress route in the current app/release contract. It may remain running until a separately authorized cleanup, but it is not owned by the current StockDividend release. Do not include it in rollout, restart, rollback-readiness, or health gates, and do not delete or scale it as part of this contract.

The StockDividend application Dockerfile now compiles `cmd/migrate` into a static `/app/migrate` executable (StockDividend PR #31, master commit `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`). Exact-head CI built a non-publishing amd64 runtime image, verified the executable, and confirmed it exits on missing `MONGO_URI` before any database connection.

The post-merge master publisher [run #41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933) then completed on the native ARM64 runner for source commit `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. It verified the full-source-SHA tag resolves to a registry digest with `linux/arm64` support for all three components:

| Component | Verified registry digest |
|---|---|
| Scraper | `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2` |
| Admin | `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e` |
| Backend | `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a` |

This proves app-owned immutable ARM64 publication, not production promotion. The publisher's release-gate output was `false`; the Platform handoff validation and atomic promotion-dispatch jobs were skipped. The production overlay still references Admin/Backend tag `12d63b4`, and the later Platform StockDividend health lane #41563976954 confirmed those Pods cannot pull that old tag because its manifest lacks ARM64. Keep the release hold until explicit production authorization and the required owner credentials are available; do not change the overlay or dispatch promotion automatically.

Do not execute the migration from a production Pod or deployment workflow. Any database migration requires a separately reviewed, explicitly authorized operator procedure after the image is published and promoted.
