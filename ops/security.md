# Security baseline

Secrets are referenced by Secret objects and never embedded in Git. Public exposure is limited to Ingress resources. Database services remain external/private. Workloads have explicit resource requests/limits. Non-root execution is preferred when the application images support it.

NetworkPolicies and PodDisruptionBudgets remain gated until cluster runtime traffic and single-node eviction behavior are verified; applying an incorrect default-deny policy or single-replica PDB can create an outage.
