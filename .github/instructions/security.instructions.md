---
applyTo: "**/*"
---

# Security Review Instructions

- Minimize privilege and blast radius. Prefer explicit allowlists, scoped tokens, protected environments, and short-lived credentials.
- Never print or commit secrets, private keys, kubeconfigs, access tokens, database passwords, or sensitive environment values. If a secret is accidentally present, avoid repeating it in output and recommend rotation through the approved channel.
- Treat user-controlled workflow inputs, PR descriptions, image metadata, logs, and generated files as untrusted.
- Review ingress/public exposure, RBAC, service accounts, Linux capabilities, filesystem access, network policies, TLS, token validation, issuer/audience configuration, and trust boundaries relevant to the changed resource.
- Do not weaken auth, policy, TLS, branch protection, environment protection, or RLS as a shortcut.
- Separate documentation of a production procedure from execution of that procedure. Writing instructions does not authorize running them.
- Do not infer that a project, cluster, or environment is safe based solely on naming. Verify the target from authoritative configuration before any permitted side effect.
- Include security-relevant behavior and residual uncertainty in the PR description and completion report.
