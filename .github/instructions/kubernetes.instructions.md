---
applyTo: "**/*.yaml"
---

# Kubernetes Manifest Instructions

- Read the owning Kustomize `kustomization.yaml`, bases, overlays, and relevant service/network contracts before changing a resource.
- Treat `environments/prod` as production-impacting. Prefer shared-base changes only when all overlays should inherit them; otherwise patch the narrowest correct overlay.
- Preserve namespace, workload selectors, label consistency, Service target ports, Ingress routing, health probes, rollout strategy, resource requests/limits, security contexts, and existing Secret references.
- Do not inline credentials or add literal Kubernetes Secret data. Use existing runtime Secret references and approved external secret patterns.
- Prefer immutable image references aligned with the documented Git-SHA promotion flow. Validate the *rendered* image after Kustomize transformations.
- Do not introduce privileged containers, host networking, hostPath mounts, broad RBAC, public ingress, or broad NetworkPolicy exceptions without explicit scope and security justification.
- Avoid unnecessary destructive fields or resource replacement. Call out downtime, rollout, PVC/data-loss, selector immutability, and rollback risks.
- Render the complete affected overlay and inspect output. Source YAML validity alone is insufficient.
- Do not apply manifests to a live cluster as a routine validation step. Use offline rendering and client-side dry-run only when the repository's documented command and environment support it.
