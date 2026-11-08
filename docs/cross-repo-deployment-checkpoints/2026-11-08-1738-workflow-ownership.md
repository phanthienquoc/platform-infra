# Workflow ownership audit — 2026-11-08 17:38 ICT / 10:38 UTC

Current Platform master at branch creation: 4062cda57dad737534204e369bacbb584f4c91f9. Dedicated branch: docs/workflow-ownership-boundaries-20261108-1738-ict.

## Findings

| Workflow | Trigger/owner | Verified scope | Decision |
|---|---|---|---|
| TCE WF-03 | workflow_dispatch; TCE app repo | ARM64 web/service image publication, digest verification and tce-release-requested dispatch to Platform | Preserve as app publisher; not a direct deploy lane |
| TCE WF-08B | pull_request/push/workflow_dispatch; TCE app repo | ARM64 MicroFE Shell/WS publication and digest-bound Platform handoff | Preserve as app publisher |
| TCE WF-09 | workflow_dispatch; TCE app repo | VPS inspection, isolated directories, source upload only to development/source.tmp; explicit output says existing containers/nginx/ports/domain are not modified | Preserve as manual setup utility; not production deployment |
| TCE WF-10 | workflow_call/workflow_dispatch; TCE app repo | Explicitly staging-only; creates/labels tce-stg and tce-auth staging Secret; no tce-prod or microfe-platform references | Preserve as staging bootstrap; no production authority |
| Stock deploy.yml | master push/workflow_dispatch; Stock app repo | ARM64 immutable GHCR publication using full-SHA and version/full-SHA tags; manual publication is blocked unless STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true; no Platform handoff | Preserve as app publisher; not production deployment |
| Stock run_scraper.yml | weekend schedule/workflow_dispatch; Stock app repo | Weekend ingestion with VNSTOCK_API_KEY fail-closed preflight and preflight_only mode | Preserve as purposeful scheduled/manual job |
| Media WF-03 | master push/workflow_dispatch; Media app repo | ARM64 immutable GHCR publication with digest verification; no Platform handoff while retired | Preserve as app publisher; not active Platform GitOps |
| Auth release.yml | workflow_dispatch; Authentication app repo | App-owned ARM64 image publication, provenance/SBOM and auth-image-published event | Preserve as app publisher |
| Platform reconcile-vps.yml | Platform workflow_dispatch/schedule/recovery | Sole production manifest apply, shared GHCR credentials, runtime Secrets, GitOps reconcile, rollout and health | Sole production apply authority |
| Platform inspect-vps.yml | Platform schedule/push/workflow_dispatch | Read-only K3s/host inspection and snapshot PR | Preserve as read-only |

## Current evidence

- TCE WF-09 source: .github/workflows/wf-09-tce-vps-safe-setup.yml at 960d69ead984df496536cf85827f22eb1b11c359.
- TCE WF-10 source: .github/workflows/wf-10-tce-k3s-bootstrap.yml at 3599f9c30d31f409e6fac02b7589f4b8224dbf85; explicit staging-only comment and tce-stg-only kubectl operations.
- TCE WF-03 source: .github/workflows/wf-03-tce-production-deploy.yml at e933f659d03403b73383a3a46e5e063f52033dff.
- Stock deploy.yml source: d683368a0a45b7f78d119ada1cf226af2640f4b5; master push publisher, manual-publication hold and immutable ARM64 tags.
- Media WF-03 source: da9bdd6940e84bf7a4eb7ddb019c2dc80f4d172e.
- Auth release.yml source: 8233d7645139826cf635c846bbf61f52467a0090.

No workflow was removed. The SSH workflows are retained because their scopes are explicit and distinct from production; they are documented as staging/setup only. No duplicate direct SSH/Compose production authority was introduced. No cron or TCE market-scan schedule changed.
