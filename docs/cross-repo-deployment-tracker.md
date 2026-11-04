# Cross-Repository Production Deployment Tracker

Last reviewed: 2026-11-05 06:01 ICT (2026-11-04 23:01 UTC)
Platform Infra master at checkpoint: cfdce04a1d78fc2dcc9c1494628ff8791126ca20

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | cfdce04a1d78fc2dcc9c1494628ff8791126ca20 | #1222, #544, #541, #539 (all draft) | Inspection run #41929001497 completed successfully; inspection PR #1244 merged at exact validated head 6d642d020462566b1ad0cc0b8ecf79b30fc6199f as cfdce04. This is an inspection workflow success, not a current master CI result. The connected run metadata did not expose its event type, so it is not counted as native schedule evidence. |
| phanthienquoc/TCE-dashboard | 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d | None | Last verified native WF-07 #41900042968 PASS at 02:45 ICT. WF-06 #41880229621 FAIL (four public endpoints HTTP 503); WF-12 #41877745265 FAIL (freshness); workflow_run #41900072829 FAIL (delivery verification) although its authenticated Platform heartbeat notification passed. No newer run list was exposed in this inspection. |
| phanthienquoc/stockdividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None | CI #41563856934 PASS; immutable ARM64 publisher #41563856933 PASS. Scraper/Admin/Backend full-source-SHA images have verified linux/arm64 digests. Production GitOps promotion remains explicitly disabled by the publisher release gate; handoff validation and paired digest dispatch are SKIPPED. |
| phanthienquoc/media-generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None | Media CI #41617592783 PASS. Latest inspected runtime has backend/frontend 1/1 with digest-pinned imageIDs. No newer Media CI/publisher run was surfaced. |
| phanthienquoc/phanthienquoc-authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft | Auth service CI #41670642852 PASS. Last documented PR #75 validation #40446492086 and PR #76 validation #41329425940 are historical evidence; current Auth PR head runs were not returned by the connected workflow-run lookup. Supabase Preview remains SKIPPED; migration/production gate remains closed. |

Current Platform Infra PR heads and last returned validation runs:
- #1222 draft, head f018e39eda52770539fc10671fba0d04baec8046; validate-manifests #41821355040 PASS. The PR remains unsafe for deployment: it still proposes Docker/Kubernetes mutation tools, the previously reviewed source/installer newline defects and missing SHELL_UID/GID forwarding remain unresolved, and reproducible build/tests/lockfile evidence is absent.
- #544 draft, head c95e7daecb83b65577b54303427fe4ea81adfe06; validate-manifests #38575430454 PASS.
- #541 draft, head b8f7c6ba04e3d971336a899b2efd5894662083b3; validate-manifests #38567431761 PASS.
- #539 draft, head 2dc48b97017ecb08e49682633303a2f1d5e991a1; validate-manifests #38548718033 PASS.
- These are the last PR-associated runs returned for the exact heads, not new post-merge or production-health evidence. Combined-status lookup returned no status contexts for the current master heads.

## Current actions

1. PR #1242 merged the recovery event-classification fix. The previous watchdog correctly failed because native inspection #41881867627 was stale, while recovery #41918357799 incorrectly treated manual inspection #41914913277 as native activity. The merged controller now separates event=schedule evidence from workflow_dispatch fallback activity, suppresses duplicate read-only fallbacks, and never lets manual fallback satisfy native schedule freshness. Exact-head #41923196096/#41923196112 and post-merge #41923323345/#41923323244 all PASS.
2. The latest inspected snapshot was produced by run #41929001497. Its inspect job and all listed steps completed successfully; it created inspection PR #1244 and merged exact head 6d642d020462566b1ad0cc0b8ecf79b30fc6199f as cfdce04. The workflow run event type was not present in the connected run/job response. Do not classify it as native schedule evidence without a verified event=schedule field.
3. Keep verifying native Platform schedule delivery independently for inspect-vps, reconcile-vps, recover-stale-ops and reconcile-schedule-watchdog. Do not count workflow_dispatch, workflow_run, repository_dispatch or reruns as native schedule evidence. The recovery fix is not considered production-verified until a post-merge native schedule cycle is directly confirmed.
4. Keep StockDividend production promotion disabled. The app publisher explicitly logs that promotion is disabled; handoff validation and paired digest dispatch were skipped. Do not enable promotion without explicit release authorization and protected Actions:read access. Preserve atomic Admin/Backend pairing.
5. Resolve TCE service availability while preserving strict HTTP 200 endpoint assertions. Current inspected TCE frontend/service and Auth/Keycloak desired replicas are 0/0; heartbeat forwarding is not service health.
6. Resolve Auth Supabase integration target/effects and migration provenance before merging #75/#76, running migrations or activating Auth/Keycloak.
7. Obtain a VPS maintenance window before pending Ubuntu, Docker and containerd upgrades or reboot.
8. Keep optional VPS MCP PR #1222 in draft until its mutation paths are removed or brought under the single GitOps authority, shell UID/GID isolation is actually enforced, and reproducible build/test/lockfile checks pass.

## Current runtime blockers

- **K3s snapshot:** Read-only inspection snapshot in debug/vps-latest.md was generated at 2026-11-04T22:52:28Z (2026-11-05 05:52:28 ICT) and merged by inspection PR #1244 as master SHA cfdce04a1d78fc2dcc9c1494628ff8791126ca20. At 06:01 ICT it is about 9 minutes old. This is point-in-time evidence, not continuous health. Node tce-k3s-01 was Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, available memory about 19 GiB. Media backend/frontend, MicroFE Shell/WS and NATS were 1/1. Two Stock Admin Pods and the new Stock Backend Pod were ImagePullBackOff; old Backend and Frontend were 1/1. TCE frontend/service and MicroFE Auth/Keycloak were 0/0. Public Keycloak OIDC probes returned HTTP 503. No claim of current continuous cluster health is made.
- **StockDividend:** Production Admin and new Backend still reference tag 12d63b4, which has no ARM64 manifest (containerd reports no match for platform in manifest). The successful publisher #41563856933 verified these immutable linux/arm64 digests for source SHA 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec:
  - Scraper: sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2
  - Admin: sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e
  - Backend: sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a
  The publisher release gate explicitly disables production GitOps promotion. Handoff validation and paired digest dispatch are SKIPPED. No production promotion is authorized by this evidence.
- **TCE/Auth/Keycloak:** TCE frontend/service and MicroFE Auth/Keycloak are 0/0 in the 05:52 ICT snapshot. The last verified native WF-06 #41880229621 failed all four strict public endpoint probes (TCE web, TCE API, Auth liveness and Auth readiness returned HTTP 503). Native WF-12 #41877745265 failed freshness; workflow_run #41900072829 failed WF-06 delivery verification although authenticated Platform heartbeat notification succeeded.
- **Media/MicroFE:** Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 in the 05:52 ICT snapshot. Media imageIDs are digest-pinned. No newer Media CI/publisher run was surfaced.
- **Host maintenance:** restart_required: yes. The host is Ubuntu 22.04.5 ARM64 with Docker 29.1.3 and K3s containerd 2.3.2-k3s2. Pending package upgrades include containerd 2.4.2 and Docker 29.9.3. No reboot or package upgrade was performed.

## Native schedule evidence

| Workflow | Cron (unchanged) | Latest positively verified native schedule evidence | Result |
|---|---|---|---|
| inspect-vps.yml | 2,32 * * * * | #41881867627 at 00:55:54 ICT | PASS, but stale. Inspection #41929001497 succeeded and refreshed the snapshot, but its event type was not exposed in the connected run response and is not counted as native schedule evidence. |
| reconcile-vps.yml | 7,22,37,52 * * * * | #41917440202 at 04:35:01 ICT | FAIL in StockDividend health lane. |
| recover-stale-ops.yml | 10,25,40,55 * * * * | #41914511298 at 04:16:19 ICT | PASS. |
| reconcile-schedule-watchdog.yml | 12,27,42,57 * * * * | #41918315745 at 04:40:44 ICT | FAIL: no native inspect-vps run within the 75-minute budget; it reported native inspect #41881867627 age 224 minutes. |

The recovery event-classification fix is merged, but no post-merge native schedule run with a verified event=schedule field has been recorded in this checkpoint. The latest successful inspection run #41929001497 is not used to infer the event type. A successful manual fallback refreshes the snapshot but must not turn the native schedule watchdog green.

TCE native schedule evidence:
- WF-07 #41900042968 at 02:45:37 ICT: SUCCESS; Binance private API check passed; third-party order integration skipped.
- WF-06 #41880229621 at 00:45:34 ICT: FAIL; all four public endpoint probes returned HTTP 503 instead of HTTP 200.
- WF-12 #41877745265 at 00:27:45 ICT: FAIL on freshness.
- WF-12 workflow_run #41900072829 at 02:45:48 ICT: overall FAIL because WF-06 delivery verification failed; authenticated Platform heartbeat notification job succeeded. It is not a native schedule event.
- The connected run lookup did not expose a newer TCE run list in this inspection. Preserve all cron expressions, especially the TCE market-scan schedule.

## Credential and dispatch contract

- GHCR pull access is separate from GitOps/repository dispatch. GHCR_READ_TOKEN is package-scoped read:packages access paired with GHCR_USERNAME and package access to every production image.
- STOCKDIVIDEND_ACTIONS_READ_TOKEN is only for Platform Infra to read private StockDividend publisher run metadata. Store it in the protected production Environment with Actions:read only; do not grant Contents write, Packages or workflow-dispatch.
- TCE and Stock use separate per-repository PLATFORM_INFRA_TOKEN values. TCE requires Contents:write and Actions:read on Platform Infra because WF-08B correlates Platform runs and WF-12 sends schedule heartbeats. Stock requires Contents:write for repository dispatch; neither requires Packages or workflow-dispatch.
- Media and Authentication use separate per-repository PLATFORM_INFRA_DISPATCH_TOKEN values. Media requires Contents:write and Actions:read for dispatch correlation; Authentication requires Contents:write.
- Active Platform promotion uses workflow-scoped GITHUB_TOKEN for GitOps PR/validation/merge permissions and GHCR_READ_TOKEN for registry reads. PLATFORM_INFRA_AUTOMATION_TOKEN is obsolete and must not be reintroduced.
- Never store secret values, PATs, passwords, environment files or token fragments in Git or logs.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication, and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- reconcile-vps.yml is the sole production apply authority. inspect-vps.yml is read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- No production image promotion, manifest/credential/database mutation, Pod/replica change, host reboot or cron expression change occurred in this checkpoint. TCE market-scan schedule is unchanged.

## Current runtime and release references

- Recovery event-classification fix PR #1242: https://github.com/phanthienquoc/platform-infra/pull/1242
- PR #1242 exact-head validate-github-actions #41923196096: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196096
- PR #1242 exact-head validate-manifests #41923196112: https://github.com/phanthienquoc/platform-infra/actions/runs/41923196112
- PR #1242 post-merge validate-github-actions #41923323345: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323345
- PR #1242 post-merge validate-manifests #41923323244: https://github.com/phanthienquoc/platform-infra/actions/runs/41923323244
- Latest inspection run #41929001497: https://github.com/phanthienquoc/platform-infra/actions/runs/41929001497
- Inspection snapshot PR #1244: https://github.com/phanthienquoc/platform-infra/pull/1244
- Latest K3s snapshot: https://github.com/phanthienquoc/platform-infra/blob/master/debug/vps-latest.md
- Platform latest positively verified native reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Platform native watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- Platform watchdog-triggered recovery #41918357799: https://github.com/phanthienquoc/platform-infra/actions/runs/41918357799
- Platform latest positively verified native recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- Platform latest positively verified native inspection #41881867627: https://github.com/phanthienquoc/platform-infra/actions/runs/41881867627
- TCE native WF-07 #41900042968: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900042968
- TCE native WF-06 #41880229621: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41880229621
- TCE native WF-12 #41877745265: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41877745265
- TCE heartbeat/delivery verification #41900072829: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41900072829
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75: https://github.com/phanthienquoc/phanthienquoc-authentication/pull/75
- Auth PR #76: https://github.com/phanthienquoc/phanthienquoc-authentication/pull/76
- Platform MCP PR #1222: https://github.com/phanthienquoc/platform-infra/pull/1222

## Latest workflow inventory checkpoint

[2026-11-05 06:01 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-05-0601-ict.md) records the current five-repository heads/open PRs, inspection PR #1244, current K3s snapshot, native-schedule evidence limitations, credential scopes and remaining production gates.
