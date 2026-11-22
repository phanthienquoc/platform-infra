# Operations

Sequence: render -> validate -> diff -> explicit migration if required -> shared platform services (Authentication, MicroFE, Keycloak, cert-manager) -> TCE rollout -> health verification -> read-only smoke -> record revisions.


Rollback is performed by reverting the Git image/config revision and reconciling. Avoid hot-editing live resources as the normal operating model.
