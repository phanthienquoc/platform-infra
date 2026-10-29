# Platform Infra Copilot Adoption Roadmap

## Phase 1 — Instruction compatibility and low-risk proof
- Merge and inspect the guidance PR.
- Confirm the target Copilot client discovers repository-wide and path-scoped instructions plus Planner/Developer/Reviewer agents.
- Run a documentation-only task through the full role sequence.
- Verify branch isolation, honest validation reporting, diff review, and PR creation.
- Do not make production changes during the proof.

## Phase 2 — Safe PR assistance
- Use Planner -> Developer -> Validation -> Reviewer on manifest, documentation, and offline-validator changes.
- Require render evidence for Kustomize-affecting PRs.
- Require complete trigger/permission review for workflow changes.
- Track recurring failure modes and refine instructions.

## Phase 3 — Controlled automation in CI
- Add automation only where deterministic checks and least-privilege permissions are clear.
- Keep untrusted pull requests isolated from secrets.
- Use immutable artifacts, explicit environments, bounded timeouts, and auditable evidence.
- Keep CI unable to perform unintended deployment side effects.

## Phase 4 — Controlled delivery
- Treat release/promotion/reconciliation as separate, protected steps.
- Preserve existing production environment approvals and explicit deployment targets.
- Require independent review and verified rollback for high-impact changes.
- Monitor actual deployment evidence separately from merge/CI results.

## Exit criteria
Each phase requires evidence from the actual GitHub/Copilot environment. Repository documentation alone does not prove agent discovery, execution, or live-system health.
