# Backup and restore runbook

This runbook covers recovery of the single-node K3s platform and its application data. It does not authorize destructive cleanup or production changes outside the Platform GitOps workflow.

## Recovery principles

- Confirm the backup identifier, timestamp, retention policy and restore target before changing anything.
- Preserve the current state and capture read-only diagnostics before restore.
- Restore data dependencies before application workloads.
- Use the repository as the source of truth for Kubernetes resources.
- Do not print Secret values, database passwords, registry credentials or service-account tokens.

## Kubernetes recovery validation

Before any production apply, run the read-only validation workflows and confirm. The cert-manager controller/CRD bundle is a pinned GitHub Release asset; prepare it before any Kustomize render or diff:

```bash
manifest="$PWD/platform/cert-manager/cert-manager.yaml"
trap 'rm -f "$manifest"' EXIT
bash scripts/prepare-cert-manager-manifest.sh "$manifest"
sudo /usr/local/sbin/platform-kubectl version
sudo /usr/local/sbin/platform-kubectl kustomize environments/prod >/dev/null
sudo /usr/local/sbin/platform-kubectl apply --dry-run=server -k environments/prod >/dev/null
sudo /usr/local/sbin/platform-kubectl diff -k environments/prod
```

Interpret the diff result as:

- `0`: live state matches the repository.
- `1`: drift exists and requires explicit reconciliation.
- `>1`: inspection failed; do not treat the result as approval to apply.

Do not use an emergency rollback or live-only manifest edit as a substitute for restoring the repository source of truth.
