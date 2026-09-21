# Platform Infra

K3s platform infrastructure for TCE Dashboard and StockDividend.

Kubernetes resources live here. Application repositories own source, Dockerfiles, tests and image builds. Production images are immutable Git-SHA tags. Secrets are runtime-only. Migrations are explicit Jobs.

Production entrypoint: environments/prod.

Static verification: kubectl kustomize environments/prod and kubectl apply --dry-run=client against the rendered output.
