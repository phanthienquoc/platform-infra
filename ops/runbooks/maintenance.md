# Production maintenance runbook

This runbook is the safe operational boundary for the single-node K3s production cluster. Prefer GitOps changes through `master`; use direct Kubernetes commands only for explicitly documented, reversible incident actions.

## Safety rules

- Inspect first: node health, namespaces, workloads, events, GitOps drift, and rollout state.
- Do not read or print Secret values.
- Do not mutate workloads until the affected application and target resource are explicitly identified.
- Do not use `kubectl apply` from an operator shell for normal releases; use `reconcile-vps` through the repository.
- Never reintroduce the removed scraper workload.
- Because the cluster is single-node, do not claim high availability or use disruption settings that assume another node exists.

## Standard inspection

Run the repository inspection workflow/script first and capture the resulting evidence. The expected checks are equivalent to:

```bash
sudo /usr/local/sbin/platform-kubectl get nodes -o wide
sudo /usr/local/sbin/platform-kubectl get pods -A -o wide
sudo /usr/local/sbin/platform-kubectl get deployments -A
sudo /usr/local/sbin/platform-kubectl get events -A --sort-by=.lastTimestamp
sudo /usr/local/sbin/platform-kubectl diff -k environments/prod
```

Interpret `diff` exit code `0` as clean, `1` as drift, and `>1` as an inspection error. Do not treat a diff error as permission to apply.

## Rollout / restart

Normal rollout is performed by `reconcile-vps` after the GitOps change has passed validation. For an incident affecting a specific deployment, inspect first:

```bash
sudo /usr/local/sbin/platform-kubectl rollout status deployment/<name> -n <namespace> --timeout=180s
sudo /usr/local/sbin/platform-kubectl rollout history deployment/<name> -n <namespace>
```

A manual restart is an incident action, not a release mechanism. If it is required, target only the named deployment and record the reason and resulting rollout status:

```bash
sudo /usr/local/sbin/platform-kubectl rollout restart deployment/<name> -n <namespace>
sudo /usr/local/sbin/platform-kubectl rollout status deployment/<name> -n <namespace> --timeout=180s
```

Do not restart all namespaces or all deployments as a troubleshooting shortcut.

## Rollback

Before rollback, capture the current revision and rollout history. Roll back only the affected deployment:

```bash
sudo /usr/local/sbin/platform-kubectl rollout history deployment/<name> -n <namespace>
sudo /usr/local/sbin/platform-kubectl rollout undo deployment/<name> -n <namespace>
sudo /usr/local/sbin/platform-kubectl rollout status deployment/<name> -n <namespace> --timeout=180s
```

A rollback is temporary runtime recovery. The repository must subsequently be reconciled to the intended state; do not leave an undocumented live-only image or manifest override.

## Cleanup

Prefer Kubernetes-native TTL cleanup for completed Jobs. Before deleting anything manually, inspect the exact resource and confirm it is not an active migration or required workload:

```bash
sudo /usr/local/sbin/platform-kubectl get jobs -A
sudo /usr/local/sbin/platform-kubectl get pods -A
```

Never use broad deletion patterns such as `delete pods --all`, namespace-wide workload deletion, or unbounded image pruning during an incident.

## Incident evidence

Capture non-secret diagnostics before making a change:

```bash
sudo /usr/local/sbin/platform-kubectl get nodes -o wide
sudo /usr/local/sbin/platform-kubectl get pods -A -o wide
sudo /usr/local/sbin/platform-kubectl get deployments -A
sudo /usr/local/sbin/platform-kubectl get events -A --sort-by=.lastTimestamp
```

Do not include Secret data, service-account tokens, registry credentials, or private configuration values in tickets, PRs, Telegram messages, or committed inspection artifacts.

## Disk pressure

The VPS inspection reports root filesystem pressure. Treat `>=80%` as warning and `>=90%` as critical. Prefer identifying large, disposable artifacts before cleanup. Do not delete Kubernetes state, application data, or Docker volumes without an explicit backup/recovery plan.

## Recovery boundary

The repository is the source of truth for declarative platform state. After any emergency runtime action:

1. record what changed;
2. verify rollout health;
3. run the GitOps diff;
4. reconcile through the repository once the intended state is confirmed; and
5. record the final state and any remaining drift.

This runbook intentionally does not define database backup credentials, secret values, or application-specific migration commands until their production contracts are verified.