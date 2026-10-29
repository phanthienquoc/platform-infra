# Skill: Rendered Manifest Validation

1. Determine the exact Kustomize entrypoint from README and the changed overlay.
2. Render with the repository's documented command (currently the README identifies `kubectl kustomize environments/prod`).
3. Review rendered output and check whether transformations alter image references, names, selectors, namespaces, or resource wiring.
4. If a documented client-side dry-run is available, only use it against rendered output and do not confuse it with a server-side/live-cluster validation.
5. Confirm workload -> Service -> Ingress mappings, ports, probes, required Secret references, and immutable image tags where relevant.
6. Compare the render to the intended change and inspect unrelated resource drift.
7. Record the exact command and result. If the environment lacks kubectl or another required validator, report BLOCKED rather than guessing.
