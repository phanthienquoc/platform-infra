# Production GHCR Pull Credential Contract

## Ownership

- **TCE Dashboard** builds and publishes immutable images to GHCR and requests GitOps promotion.
- **Platform Infra** owns production manifests, Kubernetes pull credentials, and rollout verification.
- Application repositories must not create their own namespace-specific pull-secret names or embed registry credentials in manifests.

## Canonical credential

The `reconcile-vps.yml` production Environment uses:

- Secret `GHCR_READ_TOKEN`: token with `read:packages` permission and access to every private GHCR package deployed to production.
- Variable `GHCR_USERNAME`: optional GHCR account name; defaults to the repository owner.

Because `ghcr-pull` is shared across production namespaces, every non-Keycloak apply validates **all** referenced production GHCR packages before the Secret can be reconciled—even when the requested rollout targets only one app. This prevents a MicroFE-only package check from authorizing a shared credential update while StockDividend or another package is still inaccessible.

The workflow intentionally does **not** fall back to `GITHUB_TOKEN` for Kubernetes pulls. A workflow token that cannot read another repository's private package must fail fast rather than silently creating a Kubernetes secret that returns 401/403. The package preflight obtains a scoped bearer token and probes each package's Registry V2 `tags/list` endpoint. Promotion then uses `scripts/validate-ghcr-image-reference.sh` to request the exact tag or digest from `manifests/<reference>` with a package-scoped bearer token. This avoids relying on Docker's registry-wide `/v2/` login challenge, which can be denied even when scoped package reads succeed.

Never print or commit token values. The workflow passes the credential through stdin to the root-owned, allowlisted `platform-kubectl reconcile-ghcr-pull` command.

## Kubernetes contract

The platform-owned Secret name is `ghcr-pull`. The reconciler applies it to existing production namespaces that host GHCR images:

- `microfe-platform`
- `stock-prod`
- `tce-prod`
- `media-prod`

It attaches `ghcr-pull` to each namespace's `default` ServiceAccount and normalizes any Deployment-level `imagePullSecrets` override for workloads whose container or init-container image uses `ghcr.io/`. This prevents a stale per-app name such as `ghcr-secret` from bypassing the platform credential. Public images in the same namespace remain public; the secret contains credentials only for GHCR.

Namespaces that do not exist yet are skipped and picked up by a later reconciliation after their GitOps namespace manifests are applied.

## Failure handling

For package-scoped GHCR `401`/`403` errors, verify that `GHCR_READ_TOKEN` is present, not expired, has `read:packages`, and belongs to an account with access to each referenced package. For `manifest unknown` or `not found` from the exact manifest probe, verify the exact image name and immutable tag/digest was published before promotion. A denied registry-wide Docker login alone is not treated as proof that package-scoped reads are denied. Do not use repeated pod restarts as a substitute for fixing credentials or invalid image tags.

After changes to `scripts/bootstrap-runner.sh` are merged, the existing `bootstrap-runner.yml` workflow updates the installed allowlisted helper on the VPS. The regular reconciliation then refreshes Kubernetes secrets and workload pull-secret references.
