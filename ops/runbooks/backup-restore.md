# Production backup and restore runbook

This runbook defines the safe boundary for FEAT-62. It documents what must be backed up and how recovery is coordinated without inventing unverified production backup commands or exposing credentials.

## Safety rules

- Treat `platform-infra` as the declarative source of truth for Kubernetes resources.
- Never commit database credentials, object-storage credentials, registry credentials, Kubernetes Secret values, or service-account tokens.
- Do not claim a backup is restorable until a restore has been exercised against an isolated target.
- Do not delete or overwrite an existing backup as part of a recovery test.
- Because production is a single-node K3s cluster, Kubernetes-state recovery and application-data recovery are separate concerns.
- Never reintroduce the removed scraper workload as part of recovery.

## Backup scope

### Kubernetes / platform state

The Git repository is the primary backup of declarative Kubernetes state. A recovery package should also preserve non-secret runtime metadata needed to diagnose the cluster:

- K3s version and node inventory
- namespaces and workload inventory
- ingress and certificate metadata
- persistent-volume / storage metadata
- rollout history and recent cluster events
- Git commit used as the intended production state

Do not export Secret values. Preserve only Secret names, namespaces, and references required to restore the external secret contract.

### Application data

Application data must be backed up using the authoritative provider-owned mechanism for each external dependency. The exact command, retention policy, encryption key, and restore endpoint must be verified against the application's production contract before automation is added here.

The current repository intentionally does not invent MongoDB Atlas, Supabase, or other provider credentials/commands. Those dependencies remain external to Kubernetes and must be restored through their provider-supported procedures.

## Recovery order

1. Identify the last known-good `platform-infra` commit and immutable application image tags.
2. Confirm the target K3s version and node prerequisites.
3. Restore external application data into an isolated or explicitly approved target first.
4. Restore the platform from the repository with server-side dry-run validation before apply.
5. Restore namespace/platform resources and then application workloads through the normal GitOps reconciliation path.
6. Run rollout and smoke validation.
7. Verify application connectivity to restored data dependencies.
8. Record the recovered Git commit, image tags, data backup identifiers, and remaining drift.

## Kubernetes recovery validation

Before any production apply, run the read-only validation workflows and confirm:

```bash
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

## Data restore validation

A data restore is considered verified only when all of the following are recorded without exposing sensitive values:

- backup identifier / timestamp
- source environment
- target environment or isolated restore target
- provider restore operation result
- application connectivity check
- expected record/document sanity checks
- recovery timestamp and operator

For destructive or point-in-time recovery, require an explicit recovery window and preserve the original backup before any overwrite operation.

## Recovery evidence

Capture only non-secret evidence:

- Git commit SHA
- image tags
- Kubernetes resource health
- backup identifiers and timestamps
- restore operation status
- smoke-test results
- final GitOps drift result

Never place secret values, tokens, connection strings, private keys, or full credential-bearing configuration in PRs, logs, Telegram notifications, or committed artifacts.

## Current implementation boundary

This runbook is intentionally a recovery **procedure and contract**, not an unverified backup automation. Provider-specific backup jobs and credentials should be added only after the external data dependency contracts are confirmed. This keeps recovery reversible and avoids creating a false claim of backup coverage.
