# Platform schedule and cleanup checkpoint — 2026-11-08 17:40 ICT / 10:40 UTC

Current Platform master at branch creation: c473432c54b4a4a4fad5d7751a867738e1e2e300. Dedicated branch: docs/platform-schedule-evidence-20261108-1740-ict.

## Weekly image cleanup

- Workflow: .github/workflows/vps-image-cleanup.yml
- Native cron: Sunday 03:30 UTC (30 3 * * 0).
- Latest scheduled run: [#42472343489](https://github.com/phanthienquoc/platform-infra/actions/runs/42472343489), created 2026-11-08T10:39:26Z; approximately 7h09 after the scheduled time.
- Result: PASS. DRY_RUN=true, KEEP_UNUSED_IMAGES=10, unused_images=8, remove=0. No images were removed.
- The workflow expression forces dry-run for every non-workflow_dispatch event. The script protects all Pod references and CRI containers (including terminated containers), excludes pinned images, fails closed on unresolved non-terminal Pod references, and rechecks current Pods/containers immediately before each deletion. The destructive manual path was not invoked.
- Preserve this purposeful weekly maintenance workflow; it is not a deployment cadence gate and is not a production deployment authority.

## Platform deployment state

- Current master at review: c473432c54b4a4a4fad5d7751a867738e1e2e300. PR #1455 and #1456 merged. Post-merge manifest validation #42472161449 and #42472328823 PASS.
- Recovery-dispatched reconcile #42471718647 SUCCESS; recovery controller #42471978667 SUCCESS. GHCR access and Auth runtime Secret checks passed; shared ghcr-pull unchanged; no active Auth/MicroFE/TCE image-pull failures; GitOps drift false; production apply skipped; MicroFE/TCE/Auth lanes and final gate passed.
- Fresh K3s inspection #42471706668 generated snapshot at 10:30:37Z; exact-head inspection PR #1454 passed #42471833649 and merged. Stock/Media storage preflight passed with no PVC/PV claims or VolumeSnapshot references; Media runner remains active/enabled/listening; backup/DNS evidence remains missing.

## Native schedule acceptance

No newer native Platform/TCE/Stock schedule events were returned through 10:38Z.

| Workflow | Latest native run | Result | Age at 10:40Z | Budget |
|---|---|---|---:|---:|
| Platform reconcile | #42467231073, 09:27:03Z | FAIL (pre-fix cert-manager render) | ~73m | 45m |
| Platform inspection | #42452273701, 05:49:40Z | PASS | ~290m | 75m |
| Platform watchdog | #42467080859, 09:24:53Z | FAIL | ~75m | 45m |
| Platform recovery | #42466737776, 09:20:06Z | PASS | ~80m | 45m |
| TCE WF-06 | #42458256899, 07:18:37Z | FAIL, four HTTP 503 probes | ~201m | 25m |
| TCE WF-12 | #42452308083, 05:50:11Z | FAIL freshness | ~290m | 25m |
| Stock scraper | #42457182511, 07:03:12Z | FAIL closed, missing VNSTOCK_API_KEY | ~217m | weekly |

The cleanup run is separate: it is a weekly dry-run, not part of strict deployment cadence acceptance. Native schedule delays remain an administrator-level issue; cron and freshness budgets were not changed.

## Other blockers

- Stock Admin (two pods) and desired Backend on 12d63b4 remain ARM64 ImagePullBackOff; older Backend/Frontend are 1/1 Running. Stock owner must provision VNSTOCK_API_KEY and run preflight_only=true before scraper ingestion.
- TCE/Auth/Keycloak remain intentional 0/0; public OIDC and four TCE/Auth endpoint probes returned HTTP 503. No replica scaling without service-owner approval.
- Media backend/frontend 1/1; dedicated runner active. External backup/retention, DNS ownership and runner unregistration remain decommission gates.
- Auth PR #75/#76 remain open; Supabase merge-triggered migration side effects are not authoritatively cleared.

No GHCR publication/promotion, production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.
