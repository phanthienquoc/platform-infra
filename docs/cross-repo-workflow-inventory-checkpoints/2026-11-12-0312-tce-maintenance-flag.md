# TCE Maintenance Flag / Workflow Inventory — 2026-11-12 03:12 ICT

- WF-13 #43088861304 environment log shows `TCE_MAINTENANCE_MODE` empty.
- Current master workflow maps empty to `enabled=false`; the fallback job proceeded and dispatched WF-06 manual run #43088897948.
- WF-06 manual fallback #43088897948 returned HTTP 503 on all four public endpoints.
- The repository variable's present value after that run cannot be read by the current integration. No variable was changed.
- Admin action: set true only if the 0/0 maintenance window is approved; otherwise restore replicas. Strict WF-06 HTTP-200 and WF-12 schedule checks remain.
- Native schedule freshness at 20:11:03Z: all six age and inter-arrival budgets fail; WF-07 is integration-only and WF-13 is workflow_run.
- Current Platform master at checkpoint start: `99509adbffb3888ac5bee59042c28292e5010919`. Post-merge validation #43094091607 PASS for PR #1652.
- No production manifest, runtime, credential, image or schedule mutation. Platform remains sole production apply authority; TCE market-scan schedule unchanged.


# Stock/Media Decommission Workflow Inventory — 2026-11-12 03:12 ICT

- Production manifest ownership for Stock/Media is retired; app CI/test/security/immutable publishers remain.
- The approved remaining operation is protected K3s namespace deletion of only `stock-prod` and `media-prod`.
- Manual workflow `decommission-stock-media.yml` defaults to read-only plan; delete mode is gated by production Environment approval, exact typed confirmations, HTTPS backup/DNS evidence, same-run storage preflight, Media service inactive + disabled/masked or absent, no Listener and remote runner absence verified with read-only audit token.
- Latest full snapshot #43089176130: no PVC/PV claims or VolumeSnapshot refs in target namespaces, but Services/Ingresses/Deployments/ReplicaSets/Secrets remain. Media runner is active/enabled with Listener present. Stock desired pods still ImagePullBackOff on incompatible ARM64 manifest. Keycloak OIDC probes 503, outside scope.
- No decommission workflow was dispatched and no resources/runners were deleted. Keep application repositories and useful workflows intact; no duplicate SSH/Compose authority; TCE market-scan schedule unchanged.
