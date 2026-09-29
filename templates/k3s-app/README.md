# K3s application template

Reusable template for adding a new application to platform-infra and deploying it through the existing GitOps/VPS workflow.

Copy `base/` and `overlays/prod/` into `apps/<app-name>/`, replace placeholders, then add the prod overlay to `environments/prod/kustomization.yaml`.

Application repositories build immutable GHCR images tagged with Git SHA. platform-infra owns runtime manifests and production image promotion. Follow the TCE-dashboard pattern: CI verifies/builds the image, GitOps promotion updates the prod overlay, and reconcile-vps applies production Kustomize on the VPS.

Do not put provider credentials in this repository.