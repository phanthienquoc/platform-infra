# Production

This is the production Kustomize entrypoint. CI validates it but does not contain cluster credentials.

The cert-manager controller/CRD bundle is a pinned GitHub Release asset and is generated locally before rendering. From the repository root:

```bash
manifest="$PWD/platform/cert-manager/cert-manager.yaml"
trap 'rm -f "$manifest"' EXIT
bash scripts/prepare-cert-manager-manifest.sh "$manifest"
kubectl kustomize environments/prod
```

The helper verifies the upstream release asset SHA-256. Normal production diff/apply must run through `reconcile-vps.yml`; do not use an operator shell for routine releases.
