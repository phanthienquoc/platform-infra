# Platform Infra

K3s platform infrastructure for TCE Dashboard, Authentication, MicroFE and shared services.

StockDividend and Media Generation have been retired from this Platform K3s footprint. Their application repositories and GHCR packages remain independently owned and are not managed here.

Kubernetes resources live here. Application repositories own source, Dockerfiles, tests and image builds. Production images are immutable Git-SHA tags. Secrets are runtime-only. Migrations are explicit Jobs.

Production entrypoint: environments/prod.

The cert-manager controller/CRD bundle is a pinned GitHub Release asset, not a Kustomize Git base. Before rendering the production entrypoint locally, prepare the checksum-verified asset and remove it afterward:

```bash
manifest="$PWD/platform/cert-manager/cert-manager.yaml"
trap 'rm -f "$manifest"' EXIT
bash scripts/prepare-cert-manager-manifest.sh "$manifest"
kubectl kustomize environments/prod
```

The preparation script pins cert-manager v1.21.1 and its release-asset SHA-256. The production reconciliation workflow uses the same helper and remains the only production apply authority.
