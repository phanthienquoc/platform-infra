# Retired workload decommission runbook

**Purpose:** Preserve the guarded, manual retirement procedure for a fixed set of residual Kubernetes workloads and their dedicated runner. This document intentionally avoids duplicating application-specific identifiers; the exact target allowlist remains enforced in the protected workflow, helper scripts and root-owned command wrapper.

**Current state:** GitOps ownership has been removed from the active production composition. Runtime deletion is a separate operation and must not be inferred from that repository change. No live workload, namespace, runner, DNS record, database, storage object or package may be deleted from a documentation-only task.

## Non-negotiable preconditions

1. Start from the current default branch and inspect the exact workflow revision that will execute.
2. Run the read-only plan mode immediately before any proposed deletion. The plan is not an approval and does not authorize mutation.
3. Require same-run namespace inventory and storage preflight covering PVCs, PV claim references, VolumeSnapshots and cluster-scoped snapshot contents.
4. Obtain explicit service-owner confirmation for external database/object-storage backups, retention, restoreability and data ownership. An empty in-cluster PVC list is not proof of external backup.
5. Obtain authoritative DNS/provider ownership evidence and a record-by-record disposition for every ingress hostname.
6. Stop and disable/mask the dedicated retirement runner, prove its Listener process is absent, and verify remote GitHub runner registration is absent using the workflow's scoped read-only audit credential.
7. Require the protected production approval and every exact typed attestation defined by the workflow. Evidence references must be stable and reviewable.

## Execution contract

- The retirement workflow is manual-dispatch only and defaults to read-only plan mode.
- Plan mode must not request destructive approval, stop/unregister a runner, or delete resources.
- Delete mode is a separate protected operation. It must fail closed if any attestation, evidence reference, remote runner audit, local runner check or same-run storage preflight is missing or invalid.
- The helper and root-owned wrapper independently enforce the fixed namespace allowlist, repeat destructive preflight, and verify that shared platform namespaces remain present after deletion.
- Never bypass the wrapper with raw cluster commands or broaden the fixed target allowlist.
- The workflow must never delete application repositories, container packages, DNS records, external databases/object storage, shared credentials, or the shared Platform runner.

## Preservation requirements

- Keep TCE Dashboard, Authentication, Keycloak, MicroFE, cert-manager, observability and the shared Platform runner outside the retirement scope.
- Keep TCE market-scan automation enabled and preserve its existing schedule.
- Do not change GitHub Environment configuration, variables or secret values as part of repository cleanup.
- Do not infer external backup, DNS ownership, remote runner absence or owner approval from a host snapshot.
- If any gate is uncertain, stop before deletion and record the exact missing evidence.

## Completion evidence

The retirement is complete only when a fresh post-operation inspection proves all fixed target namespaces and workloads are absent, the dedicated runner service and Listener are absent, remote GitHub runner registration is absent, external data/backup and DNS owners have signed off, and all protected workflow checks completed successfully. Preserve the evidence without copying credential values or sensitive data into Git.
