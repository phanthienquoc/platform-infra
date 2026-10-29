# Skill: Platform Infra Validation

## Discover
- Read README and workflow definitions to identify actual repo-supported checks.
- Identify the changed Kustomize entrypoint and all affected overlays.
- Determine whether the check is offline, GitHub-hosted, secret-dependent, or production-mutating.

## Validate
- Run available YAML/workflow/shell lint checks.
- Render the affected Kustomize entrypoint(s).
- Inspect effective images, selectors, Service target ports, ingress rules, Secret references, and policy-sensitive fields.
- For workflow changes, verify triggers/permissions/environment gates as well as syntax.
- Avoid applying manifests, starting migration Jobs, dispatching production workflows, or running mutating host commands as validation.

## Evidence states
- PASS: command executed and succeeded; identify what it proves.
- FAIL: command executed and failed; report the exit/result.
- BLOCKED: required tool, credential, permission, or environment is unavailable.
- NOT RUN: deliberately omitted or outside current scope.

A render validates declared configuration, not live cluster state. CI success validates only the executed checks, not production availability. Do not overstate evidence.
