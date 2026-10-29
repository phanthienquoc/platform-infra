# Skill: Platform Infra Repository Analysis

Use this skill before planning non-trivial changes to the GitOps repository.

## Procedure
1. Read root README, `.github/copilot-instructions.md`, `AGENTS.md` if present, and path-specific guidance.
2. Identify production entrypoints and trace Kustomize roots to bases, overlays, patches, and transformers.
3. For a workload, trace Deployment/StatefulSet/CronJob -> Service -> Ingress/NetworkPolicy/PVC/ConfigMap/Secret references as relevant.
4. For workflows, trace event triggers -> inputs -> permissions -> environments/secrets -> scripts/reusable workflows -> deployment/reconciliation effect.
5. Locate application-repository ownership and identify where source, image build, immutable tag, promotion, and runtime config each live.
6. Read related system design, operations, security, migration, and rollback docs plus recent relevant PRs.
7. Find actual validation commands in scripts and CI.
8. Record evidence using paths and symbols. Mark missing/ambiguous evidence explicitly; do not infer live state from repository declarations.

## Output
Produce a concise dependency map, current behavior, affected consumers, production impact, validation options, and rollback considerations.
