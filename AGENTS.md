# Coding Agent Instructions

## Mandatory pre-implementation preflight

Before changing code, generating implementation patches, or committing anything, you MUST read the repository's applicable engineering and CI rules first.

1. Read this file and any more-specific `AGENTS.md` files covering the target paths.
2. Inspect the applicable CI workflow(s), package/workspace scripts, formatter/linter configuration, and contribution instructions for the files being changed. Do not assume the tools or commands; derive them from the repository.
3. Identify the exact CI checks that apply to the changed scope (at minimum formatting and linting where configured; also typecheck, tests, and build when required by the applicable CI).
4. Follow the repository's existing conventions. Do not introduce a competing formatter, duplicate CI rules, or unrelated formatting churn.
5. Before committing, format only the task-related files using the repository's configured formatter, then run the matching local checks. Re-run checks after fixing failures.
6. Do not commit while a required formatting/lint check is failing. Never bypass hooks with `--no-verify` or disable CI checks to get a commit through.
7. If a required check cannot run locally, state exactly which check was not run and why; do not claim it passed.
8. If CI fails after the change, inspect the failure, fix the underlying issue, and rerun the relevant checks before committing or updating the PR.

## Git workflow

- Use a dedicated, descriptive branch for each task; do not work directly on `main` or `master`.
- Keep changes scoped to the task and avoid formatting files unrelated to it.
- Squash commits when the repository workflow calls for it.
- Follow repository-specific merge rules; do not merge unless the required CI checks are green and the applicable merge policy allows it.
