# MicroFE platform bootstrap

This layer owns only the platform shell and shared auth edge.

## Public hosts
- app.mrcute.space -> microfe-shell
- auth.mrcute.space -> microfe-auth

TCE, StockDividend, and MediaGeneration stay independently deployable and are integrated after the shared auth host is live on K3s.

## Image build
The manifests expect:
- ghcr.io/phanthienquoc/microfe-shell:0.1.0
- ghcr.io/phanthienquoc/microfe-auth:0.1.0

CI must publish these images before production reconciliation.
