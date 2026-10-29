# Platform Infra Copilot Adoption Roadmap

Operating guide: `/home/runner/work/platform-infra/platform-infra/.github/agentic/README.md`

## Phase 1 — Instruction compatibility and low-risk proof
- Merge and inspect the guidance PR.
- Confirm the target Copilot client discovers repository-wide and path-scoped instructions plus Planner/Developer/Validation/Reviewer roles.
- Run a documentation-only task through the full role sequence.
- Verify branch isolation, honest validation reporting, diff review, and PR creation.
- Do not make production changes during the proof.

### Phase 1 measurable exit criteria
- At least one documentation-only PR is completed using all four roles: Planner, Developer, Validation, and Reviewer.
- The Validation evidence in that PR explicitly classifies each attempted or skipped check as **PASS**, **FAIL**, **BLOCKED**, or **NOT RUN**.
- The PR includes command-level evidence for branch isolation (`git status --branch`), full diff inspection, and `git diff --check` execution result (or a documented BLOCKED reason).
- The PR links both this roadmap and the operating guide to confirm the role model and evidence vocabulary in use.

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
