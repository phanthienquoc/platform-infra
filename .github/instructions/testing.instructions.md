---
applyTo: "**/*"
---

# Validation Instructions

- Discover supported commands from README, scripts, workflow definitions, and package/config files before execution.
- Prefer offline and deterministic validation. Do not require production credentials for ordinary checks.
- Validate changed YAML syntax, shell scripts, workflow structure, and rendered Kustomize output as applicable.
- For transformed fields such as images and names, inspect the effective rendered resource rather than relying on source fragments.
- For a workflow change, inspect every trigger and permission path; a syntax pass does not prove operational safety.
- For scripts, check shell syntax and failure/timeout paths. Do not execute scripts that mutate infrastructure simply to test them.
- Never run `kubectl apply`, database migration Jobs, production reconciliation, credential rotation, DNS/firewall updates, or service restarts unless explicitly authorized for that operation and the target is independently verified.
- Report each check as PASS, FAIL, BLOCKED, or NOT RUN, with command and concise evidence. Never state that CI/runtime/deployment succeeded without corresponding evidence.
