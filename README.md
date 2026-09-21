# Platform Infra

Kubernetes infrastructure skeleton for the K3s platform serving `stock-prod` and `tce-prod`.

## Architecture

- `tce-dashboard` and `stockdividend` build container images and publish them to GHCR.
- This repository bootstraps and configures the K3s cluster.
- Cluster foundations include Traefik, cert-manager, metrics, storage, and baseline network policies.
- Application workloads run in separate namespaces:
  - `stock-prod`: frontend, backend, scraper, migration job
  - `tce-prod`: frontend, service, workers, migration job
- Workloads may connect to external databases/APIs, Supabase, and MongoDB.

## Repository layout

```text
kubernetes/
  core/                 Cluster foundations
  apps/                 Application workload skeletons
  values/               Non-secret configuration examples
scripts/                Safe validation and apply helpers
.github/workflows/      Manifest validation
```

## Prerequisites

- `kubectl` configured for the target K3s cluster
- Optional: `kubeconform` for schema validation
- Optional: Helm for installing upstream components

## Bootstrap

Review every placeholder and secret reference before applying anything:

```bash
./scripts/validate.sh
./scripts/kubectl-apply.sh
```

The apply script is intentionally limited to this repository's manifests. It does not install K3s or third-party Helm charts automatically.

## Images

Replace the placeholder image references in the app manifests with immutable GHCR tags or digests, for example:

```text
ghcr.io/<OWNER>/stockdividend:<TAG>
ghcr.io/<OWNER>/tce-dashboard:<TAG>
```

Use `imagePullSecrets` only if the GHCR packages are private. Never commit credentials.

## Secrets and external services

Create secrets out-of-band, for example with an approved secret manager or `kubectl create secret`. The checked-in `kubernetes/values/secret.example.yaml` contains placeholders only.

Typical integrations include external DBs/APIs, Supabase, and MongoDB. Keep connection strings and tokens outside Git.

## Production TODOs

- Replace example domains and email addresses.
- Install and pin approved versions of Traefik, cert-manager, metrics-server, and storage.
- Select the production storage implementation and backup policy.
- Add DNS, TLS issuers, image pull credentials, resource limits, probes, and PodDisruptionBudgets.
- Review NetworkPolicies against actual service-to-service traffic.
- Configure GitHub Actions deployment with environment protection and least-privilege credentials.
