# Agentic Copilot for Platform Infra

This directory defines a practical, reviewable operating model for Copilot-assisted infrastructure changes. It is guidance—not an autonomous deployment controller and not authorization to mutate production.

## Components
- `.github/copilot-instructions.md`: repository-wide operating rules and safety invariants.
- `.github/instructions/`: path-scoped Kubernetes, workflow, security, and validation rules.
- `.github/agents/planner.agent.md`: evidence-backed planning only.
- `.github/agents/developer.agent.md`: bounded implementation on a dedicated branch.
- `.github/agents/reviewer.agent.md`: independent review without edits.
- `.github/skills/`: reusable procedures for repository analysis, implementation, validation, and manifest rendering.

## Recommended loop
1. Planner maps the requested change and identifies impact, acceptance criteria, and validation.
2. Developer implements only the bounded scope on a dedicated branch.
3. Validation renders affected manifests and runs available offline checks.
4. Reviewer independently inspects the diff, effective render, permissions, trigger paths, and residual risk.
5. Open a PR with evidence, rollout implications, and rollback notes.
6. Production apply/reconcile remains a separately authorized, auditable operation.

## Safety boundaries
- No production mutation merely because an agent can access GitHub.
- No secret values in source or logs.
- No uncontrolled workflow triggers or arbitrary VPS commands.
- No mutable production image tags outside a documented release contract.
- No automatic database migration, DNS/firewall change, identity cutover, or workload rollout as collateral work.
- No claim of live health based solely on static rendering or CI.

## Compatibility
Custom-agent discovery and skill behavior depend on the Copilot client/version. Validate in the actual supported environment with a low-risk documentation task before relying on role switching in production workflows.
