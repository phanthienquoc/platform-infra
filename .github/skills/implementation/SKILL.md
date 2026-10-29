# Skill: Safe Platform Infra Implementation

1. Convert the request into acceptance criteria, non-goals, and an impact classification.
2. Inspect current repository patterns, ownership boundaries, and working status.
3. Create a dedicated branch from the latest appropriate base; do not edit `master`.
4. Implement only the necessary declarative change using existing Kustomize/workflow patterns.
5. Keep production image tags immutable and preserve required runtime Secret references.
6. For workflows, inspect every trigger, permission, environment, secret, shell input, timeout, and downstream side effect.
7. Update docs and offline tests/validators when useful; avoid unrelated cleanup.
8. Render the affected overlay and review effective resources, not only source YAML.
9. Review the full diff for scope creep, security regressions, environment-target mistakes, and rollback limitations.
10. Open a PR with summary, validation evidence, production risk, and recovery plan.

Never perform unapproved production changes as part of implementation. If the requested change inherently mutates production, verify the exact target and authorization before that operation, and separate it from preparatory code/config changes.
