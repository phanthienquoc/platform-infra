# Skill: Rendered Manifest Validation

1. Determine the exact Kustomize entrypoint from README and the changed overlay.
2. The production entrypoint includes the pinned cert-manager release asset at `platform/cert-manager/cert-manager.yaml`. From the repository root, run `bash scripts/prepare-cert-manager-manifest.sh "$PWD/platform/cert-manager/cert-manager.yaml"` before rendering. The helper verifies the pinned release SHA-256; remove the generated file after validation.
3. Render with the repository's documented command (currently `kubectl kustomize environments/prod`).
4. Review rendered output and check whether transformations alter image references, names, selectors, namespaces, or resource wiring.
5. If a documented client-side dry-run is available, only use it against rendered output and do not confuse it with a server-side/live-cluster validation.
6. Confirm workload -> Service -> Ingress mappings, ports, probes, required Secret references, and immutable image tags where relevant.
7. Compare the render to the intended change and inspect unrelated resource drift.
8. Record the exact command and result. If the environment lacks kubectl or another required validator, report BLOCKED rather than guessing.
