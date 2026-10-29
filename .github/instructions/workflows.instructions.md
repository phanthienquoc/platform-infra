---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml"
---

# GitHub Actions Instructions

- Read the complete workflow and related reusable workflows/scripts before making changes.
- Review triggers, workflow/job permissions, checkout refs, action pinning, environments, concurrency, inputs, secrets, shell quoting, timeouts, and cancellation behavior.
- Use least privilege. Set explicit permissions; do not grant `write-all` or broad token permissions without a verified need.
- Never expose protected secrets to fork/untrusted pull request code. Do not interpolate untrusted input directly into shell scripts.
- Separate validation, artifact publication, promotion, and production reconciliation. Make deployment-capable jobs gated, explicit, and auditable.
- Preserve immutable image tags and release promotion contracts. Do not silently introduce mutable tags, automatic tag promotion, or deployment on arbitrary branch pushes.
- Keep VPS commands allowlisted, bounded by timeouts, and scoped to the requested operation. Never add arbitrary shell, credential printing, filesystem cleanup, restarts, or apply behavior to a read-only inspection workflow.
- Do not add or change `schedule`, `repository_dispatch`, `workflow_dispatch` defaults, or production environment targets as collateral work.
- Validate workflow syntax/lint using tools already declared by the repository. Report unavailable checks honestly.
