# Cross-repo deployment checkpoint — 2026-11-06 18:27 ICT / 11:27 UTC

This checkpoint follows a fresh audit of default-branch heads, all open PRs, current Actions run history, exact PR-head checks, and the latest committed read-only K3s snapshot. Evidence only: no publisher, production promotion, replica activation, runner retirement, namespace deletion, reboot, or external-data deletion was authorized.

## Repository heads, open PRs, and current CI

| Repository | Default branch SHA | Open PRs | Latest relevant workflow evidence |
|---|---|---|---|
| Platform Infra | `0b0832d8c52a4751d518d137877997ff4d586c29` | #1314, #544, #541, #539 (all drafts) | Current-head manifest validation [#42210042886](https://github.com/phanthienquoc/platform-infra/actions/runs/42210042886) PASS. Latest Actions lint [#42209733500](https://github.com/phanthienquoc/platform-infra/actions/runs/42209733500) PASS on preceding code-identical merge head `c19d8e2d6e09fbe9e4eef923b420d512a246d961`; current HEAD change after it is documentation-only. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 native schedule [#42176208184](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176208184) FAIL (four HTTP 503 probes); WF-07 native schedule [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608) PASS; WF-12 native schedule [#42158209117](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158209117) FAIL. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) PASS, all 7 jobs including non-publishing ARM64 build. Last publisher [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933) is from Nov 3. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) PASS; no newer publisher run observed. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready, #76 draft | CI [#42167100692](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42167100692) PASS, including non-publishing ARM64 build. No new release publisher. |

### Open PR check freshness

- Platform #1314: exact head `db152c9a...`, validation PASS on Nov 6 04:20Z; draft and unrelated to deployment.
- Platform #544/#541/#539: exact-head validation PASS on Oct 14; all drafts and stale.
- Authentication #75: exact head `a8e8a1d9...`, validation PASS on Oct 27; Supabase Preview SKIPPED.
- Authentication #76: exact head `f19cacb0...`, validation PASS on Nov 1; Supabase Preview SKIPPED.
- These are historical checks, not current merge authorization. No open deployment PR exists.

## Platform promotion receiver hardening

[PR #1336](https://github.com/phanthienquoc/platform-infra/pull/1336) merged at 11:22:08Z as `c19d8e2d6e09fbe9e4eef923b420d512a246d961`. Exact-head validation [#42209633143](https://github.com/phanthienquoc/platform-infra/actions/runs/42209633143) and [#42209633160](https://github.com/phanthienquoc/platform-infra/actions/runs/42209633160) passed; post-merge [#42209733392](https://github.com/phanthienquoc/platform-infra/actions/runs/42209733392) and [#42209733500](https://github.com/phanthienquoc/platform-infra/actions/runs/42209733500) passed.

The generic legacy `image-published` repository-dispatch event was removed. The receiver now accepts the dedicated TCE, Auth and MicroFE event types; Auth requires the provenance-bound `auth-image-published` payload. Stock and Media remain app-owned publishers with no Platform production dispatch. No image was published or promoted by this hardening.

## Native schedule evidence — event type verified

- Platform native reconcile: [#42199267592](https://github.com/phanthienquoc/platform-infra/actions/runs/42199267592), `schedule`, SUCCESS at 10:00:15Z.
- Platform native recovery: [#42199274660](https://github.com/phanthienquoc/platform-infra/actions/runs/42199274660), `schedule`, SUCCESS at 10:00:18Z.
- Platform native freshness watchdog: [#42201400071](https://github.com/phanthienquoc/platform-infra/actions/runs/42201400071), `schedule`, SUCCESS at 10:16:28Z.
- Platform native inspect: [#42193617816](https://github.com/phanthienquoc/platform-infra/actions/runs/42193617816), `schedule`, SUCCESS at 09:15:08Z. A newer manual read-only inspect [#42208147735](https://github.com/phanthienquoc/platform-infra/actions/runs/42208147735) generated the snapshot at 11:09:51Z; it is not native schedule evidence. Manual reconcile [#42207918291](https://github.com/phanthienquoc/platform-infra/actions/runs/42207918291) is also fallback evidence, not native schedule proof.
- TCE native WF-06 latest: #42176208184 at 06:43:04Z, FAILURE. TCE native WF-07 latest: #42176751608 at 06:48:12Z, SUCCESS. TCE native WF-12 latest: #42158209117 at 03:43:01Z, FAILURE.
- WF-12 #42176769424 and WF-13 #42176787185 were `workflow_run` events, not native schedules. Do not count workflow_run, workflow_dispatch or repository_dispatch as cron delivery.
- The TCE native schedule history is stale by this checkpoint. WF-06 probes continue to require HTTP 200 and returned 503 for TCE web, TCE API, Auth liveness and Auth readiness. The Platform advisory observer run [#42208198166](https://github.com/phanthienquoc/platform-infra/actions/runs/42208198166) reported WF-06 age 16,022 seconds against a 1,500-second budget; it is warning-only and cannot trigger production recovery.
- Existing cron declarations remain unchanged. Do not alter the TCE market-scan schedule. The available read-only evidence does not identify whether the remaining native event gap is GitHub scheduler delivery or an Actions policy/configuration issue.

## Latest read-only K3s snapshot

Source: [inspect-vps #42208147735](https://github.com/phanthienquoc/platform-infra/actions/runs/42208147735), generated 2026-11-06 11:09:51Z (about 18 minutes old at this checkpoint).

- Node is ARM64; K3s v1.36.3+k3s1; disk 56%, about 19 GiB available RAM; `restart_required=yes`. Do not reboot without separate approval.
- GitOps drift is clean.
- Media backend/frontend are 1/1 Running and digest-pinned.
- Stock Admin has two Pods in ImagePullBackOff; the newer Stock Backend Pod is also ImagePullBackOff. The failing `12d63b4` Admin/Backend tags have no matching ARM64 manifest. The legacy Backend and Frontend on `23b2878` remain running. This is an image-platform mismatch, not evidence of invalid pull credentials.
- TCE frontend/service and Auth/Keycloak remain desired 0/0. Public OIDC probes return HTTP 503, consistent with the maintenance state.
- Only PVC/PV listed is unrelated `k3s-debug/k3s-debug-logs`; no Stock/Media PVC/PV or VolumeSnapshot references were found. External database/object-storage backups, retention approval and DNS ownership remain unverified.
- Dedicated Media runner service remains active and enabled; `Runner.Listener` remains present. Shared Platform runner is also active. Do not stop/unregister the shared runner or retire Media without operator confirmation of idle state and explicit stop/disable/unregister.

## Immutable publication and ownership

- **TCE:** WF-03 app-owned full-source-SHA publisher checks ARM64/digest and sends `tce-release-requested` with web/service digests, source run ID, workflow path, event and source SHA. Platform validates provenance/digest and owns promotion. No new publisher run observed.
- **StockDividend:** `deploy.yml` is publisher-only, with full-SHA tag, immutable digest and ARM64 verification; no Platform dispatch. Latest publisher #41563856933 is historical. Current CI ARM64 job is build-only. No release authorization or new digest/provenance; do not promote `12d63b4`.
- **Media:** WF-03 is publisher-only, with ARM64 build, checksum-verified artifacts, full-SHA tag and digest verification; no Platform dispatch. No new publisher run observed.
- **Authentication:** manual-only `release.yml` sends `auth-image-published` with `auth_digest`, source run ID, workflow path, event and full source SHA; Platform verifies exact source-run provenance, tag/digest mapping and ARM64. No new publisher run has exercised this current contract.
- App repositories own tests/builds and immutable GHCR publication. Platform owns production manifests, shared pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only.

## Next dependency-safe actions

1. Keep observing native Platform and TCE schedules independently; do not treat fallback dispatches as native delivery. Inspect Actions settings through an authorized admin surface if the native schedule gap persists; the read-only GitHub connector did not expose the Actions permissions endpoint.
2. Keep TCE/Auth at desired 0/0 and HTTP 200 assertions strict until service owners authorize activation.
3. Obtain explicit Stock release authorization before manual publication; then require full-source-SHA, GHCR digest, provenance and linux/arm64 manifest before separate Platform promotion.
4. Operator must confirm the dedicated Media runner is idle, then stop/disable/unregister it and verify no Listener remains. Never touch the shared Platform runner.
5. Require same-window storage preflight plus independent external database/object-storage backup, retention and DNS ownership review before protected Stock/Media namespace decommission.

**No production workload, replica, image, manifest, credential, namespace, PVC/PV, external data, DNS, runner or host was mutated in this checkpoint.** TCE market-scan schedule unchanged.


---

## Current review — 2026-11-06 18:22 ICT (2026-11-06 11:22 UTC)

This checkpoint adds the immutable-publication and dispatch-payload audit after the Auth promotion hardening. It is evidence-only: no publisher was triggered and no production image was promoted.

### Current repositories and open PRs

| Repository | Default-branch SHA | Open PRs | Current state |
|---|---|---|---|
| Platform Infra | `c19d8e2d6e09fbe9e4eef923b420d512a246d961` | #1314, #544, #541, #539 (draft) | PR #1336 merged; post-merge validations pass. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 native schedule stale; public probes still fail HTTP 503. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | Publisher-only; no Platform dispatch in current `deploy.yml`. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | Publisher-only; no Platform dispatch in current WF-03. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | Manual release sends the provenance-bound Auth event; no new publisher run. |

Open PR checks remain old: Platform #1314 has a historical validation PASS from 04:20Z; #544/#541/#539 have Oct 14 checks. Auth #75 validation is from Oct 27 and #76 from Nov 1; both Supabase Preview checks are SKIPPED. None is treated as newly merge-ready.

### Auth promotion receiver hardening — merged

[PR #1336](https://github.com/phanthienquoc/platform-infra/pull/1336) removed the generic `image-published` repository-dispatch event from `.github/workflows/gitops-image-promotion.yml`. Final exact head `f320eee277fc690da3ce8f39ee5e60ffe5c252bb` passed [validate-manifests #42209633143](https://github.com/phanthienquoc/platform-infra/actions/runs/42209633143) and [validate-github-actions #42209633160](https://github.com/phanthienquoc/platform-infra/actions/runs/42209633160), then squash-merged as `c19d8e2d6e09fbe9e4eef923b420d512a246d961`. Post-merge [#42209733392](https://github.com/phanthienquoc/platform-infra/actions/runs/42209733392) and [#42209733500](https://github.com/phanthienquoc/platform-infra/actions/runs/42209733500) both passed.

The receiver now accepts only:
- `tce-release-requested` for the TCE publisher lane;
- `auth-image-published` for provenance-bound Auth promotion;
- `microfe-images-published` for the MicroFE lane.

The Auth promotion job is limited to a manual `workflow_dispatch` on master or `repository_dispatch: auth-image-published`. The resolver rejects any other repository-dispatch action. Manual promotion remains available on master and still requires a full source commit and immutable digest.

Organization code search found no current `event_type="image-published"` producer in the in-scope repositories; the only current occurrence was the Auth negative regression assertion. The legacy event had allowed an older tag-only Auth payload to reach the generic receiver without source-run provenance. Removing it is a fail-closed contract change, not a workflow deletion.

### Immutable GHCR publication and payload audit

| App | Current producer contract | Latest historical publisher evidence | Current handoff |
|---|---|---|---|
| TCE | WF-03 publishes full-SHA release images, checks ARM64 and digest, then sends `tce-release-requested` with web/service digests and source run/workflow/event/head SHA. Platform receiver verifies source-run provenance and registry digest. | No new publisher run observed after current contract. | Validated by current source contract; no new promotion. |
| StockDividend | Current `deploy.yml` is publisher-only; full-SHA tag, immutable digest and ARM64 verification. No Platform dispatch or direct SSH/Compose deploy. | [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933), source `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`, verified ARM64 digests: scraper `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`; admin `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`; backend `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. | No Platform promotion. These historical digests do not repair deployed tag `12d63b4`, which still lacks ARM64. |
| Media | Current WF-03 is publisher-only; ARM64, checksum, full-SHA tag and registry digest checks. No Platform dispatch in current workflow. | [#41158598649](https://github.com/phanthienquoc/media-generation/actions/runs/41158598649), source `32f3bf56e1f44c65a5d98f35bed0547f398f8e90`, historical frontend digest `sha256:b55f3cf6dd29503f43731f5b1c519233a223baa32010f038c72c36cb900bc625`, backend digest `sha256:d66de088c4badd604a114315a18dc259a76e8963d4ffce8a4cc2b382ea0e645d`. Its historical Platform pairing run [#41158826992](https://github.com/phanthienquoc/platform-infra/actions/runs/41158826992) failed at “Wait for paired GitOps release”. | Current Media publisher no longer dispatches; Platform has no Media promotion lane. Historical digests are not a current release authorization. |
| Authentication | Current manual-only `release.yml` sends `auth-image-published` with `auth_digest`, source run ID, workflow path, event and full source head SHA. Platform verifies the exact publisher run, workflow path, event, source SHA, digest/tag mapping and ARM64 before promotion. | [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320), source `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`, digest `sha256:15bd51d68155a3b0cbc732e3baa148fc123aafb11b4290e6f66aa252969cdfc7`. This historical run used legacy `image-published` with only app/component/tag; it is not evidence for the current payload contract. | Current source and receiver contracts are aligned; no new manual publisher run has exercised them yet. |

The current Stock and Media workflows retain app-owned publication but do not send Platform dispatches. Their old Platform handoff paths remain retired; do not reintroduce them without an explicit scope decision. The current Platform GitOps promotion workflow has no Stock/Media lane.

### Current workflow and runtime status

- Platform post-merge validations #42209733392 and #42209733500 passed. The last native reconcile remains #42199267592 at 10:00:15Z; recovery #42199274660 at 10:00:18Z; watchdog #42201400071 at 10:16:28Z; inspect #42193617816 at 09:15:08Z. Later reconcile #42207918291 and inspect #42208147735 are workflow_dispatch fallbacks, not native schedule proof.
- The advisory TCE observer in watchdog push run [#42208198166](https://github.com/phanthienquoc/platform-infra/actions/runs/42208198166) reported WF-06 run #42176208184 age 16,022s against a 1,500s budget. The step is warning-only and cannot trigger production recovery.
- TCE WF-06 native #42176208184 (06:43:04Z) failed HTTP 503; WF-07 #42176751608 (06:48:12Z) passed; WF-12 native #42158209117 (03:43:01Z) failed. WF-12 #42176769424 (06:48:22Z) is workflow_run, not schedule.
- Stock CI #42167088130 passed; Media CI #42136991059 passed; Auth CI #42167100692 passed. These CI runs do not constitute new GHCR publication or promotion.

### Latest read-only K3s evidence

Snapshot [debug/vps-latest.md](../debug/vps-latest.md) was generated at 11:09:51Z by inspect-vps #42208147735:
- Node Ready/ARM64, K3s v1.36.3+k3s1; disk 56%, ~19 GiB available RAM, `restart_required=yes`; GitOps drift clean.
- Media backend/frontend 1/1 Running and digest-pinned; MicroFE Shell/WS/NATS 1/1.
- Stock Admin and new Backend remain ImagePullBackOff due missing ARM64 manifest for deployed tag `12d63b4`; older Backend/Frontend 1/1 on `23b2878`.
- TCE/Auth/Keycloak desired 0/0; public OIDC probes 503.
- Only PVC/PV is `k3s-debug/k3s-debug-logs`; no Stock/Media PVC/PV or VolumeSnapshot references. External database/object-storage backups and DNS ownership remain unverified.
- Media runner remains active/enabled with Listener present; shared Platform runner is also active. No runner retirement or reboot is authorized.

### Next actions

1. Observe native Platform and TCE schedule delivery independently; dispatch fallbacks do not count as schedule proof.
2. Do not publish or promote Stock/Auth without explicit release authorization and a current full-SHA/digest/provenance run.
3. Keep Media runner retirement blocked until operator confirms idle, stop/disable/unregister and no Listener remains; do not touch the shared Platform runner.
4. Require same-window storage, external backup, object-storage and DNS ownership review before any Stock/Media decommission.
5. Keep TCE/Auth at 0/0 until service-owner approval; retain strict HTTP 200 checks and leave the TCE market-scan schedule unchanged.

**Authority boundary:** app repositories own CI/builds and immutable GHCR publication. Platform Infra owns production manifests, shared pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only.

---

## Current review — 2026-11-06 18:10 ICT (2026-11-06 11:10 UTC)

This checkpoint covers the five production repositories, current PR/check state, native schedule evidence, the new cross-repo TCE schedule observer, and a fresh read-only K3s snapshot. It records evidence only; it does not authorize image publication, replica activation, runner retirement, namespace deletion, reboot, or external-data deletion.

### Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `50aed8dc59e596765279e3504633df11aa5f84d5` | #1314, #544, #541, #539 (all draft) | PRs #1332, #1333 and inspection PR #1334 merged. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 native schedule is stale; strict public health probes fail HTTP 503. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | ARM64 CI is build-only; no new authorized GHCR publication. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI evidence passes but is older; workloads remain active pending approved retirement. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | ARM64 CI is build-only; release remains manual and Supabase-gated. |

Open PR check evidence is old and must not be treated as current merge approval: Platform #1314 validation passed at 04:20Z; #544/#541/#539 checks date from Oct 14. Auth #75 validation passed Oct 27 and #76 validation passed Nov 1; both Supabase Preview checks were SKIPPED. No PR is open in TCE, StockDividend or Media.

### Platform implementation and validation

- PR [#1332](https://github.com/phanthienquoc/platform-infra/pull/1332) added a read-only observer for TCE WF-06 native schedule delivery and regression fixtures. Final exact head `f9f5cc12675efb2af60f5f2aeaed80258a0202c6` passed [validate-github-actions #42207795654](https://github.com/phanthienquoc/platform-infra/actions/runs/42207795654) and [validate-manifests #42207795972](https://github.com/phanthienquoc/platform-infra/actions/runs/42207795972); squash-merged as `e605cb50c48f7a0d1fd9ec1db4ac6ea80aa2cf06`.
- The first post-merge push smoke [#42207900645](https://github.com/phanthienquoc/platform-infra/actions/runs/42207900645) exposed a shell URL-construction error. The new helper also matched the recovery controller's broad `scripts/**` push filter and triggered fallback reconcile [#42207918291](https://github.com/phanthienquoc/platform-infra/actions/runs/42207918291). That run completed SUCCESS with `ALLOW_IMAGE_CHANGES=false`; preflight passed, image-change guard was skipped, `Apply production manifests` was SKIPPED, and post-reconcile verification passed. It validated GHCR pull access and Auth runtime Secret provisioning; it did not publish or promote an image.
- PR [#1333](https://github.com/phanthienquoc/platform-infra/pull/1333) fixed URL construction and explicitly excluded the read-only helper from the recovery controller's deployment-relevant push filter. Final exact head `b8157c10048c71dc7afc19f910562ae89aaf0411` passed [validate-github-actions #42208114604](https://github.com/phanthienquoc/platform-infra/actions/runs/42208114604) and [validate-manifests #42208114607](https://github.com/phanthienquoc/platform-infra/actions/runs/42208114607); squash-merged as `6f5d32988e0cd6ece0fec77d36c1118428d390c3`. Post-merge [#42208198270](https://github.com/phanthienquoc/platform-infra/actions/runs/42208198270) and [#42208198279](https://github.com/phanthienquoc/platform-infra/actions/runs/42208198279) both passed. No recovery-controller push run was created by this follow-up merge, confirming the helper exclusion.
- The post-merge watchdog push smoke [#42208198166](https://github.com/phanthienquoc/platform-infra/actions/runs/42208198166) completed SUCCESS. Its new advisory step warned that native TCE WF-06 run #42176208184 was 16,022 seconds old against a 1,500-second budget. This push run is not native schedule evidence.
- Read-only inspection [#42208147735](https://github.com/phanthienquoc/platform-infra/actions/runs/42208147735) completed SUCCESS and generated the snapshot at 11:09:51Z. Inspection PR [#1334](https://github.com/phanthienquoc/platform-infra/pull/1334) passed exact-head validation and squash-merged as `50aed8dc59e596765279e3504633df11aa5f84d5`.

### Native schedule delivery — do not count fallbacks

| Platform workflow | Latest native schedule run | Age at 11:10:57Z | Budget | Result |
|---|---|---:|---:|---|
| Reconcile VPS | [#42199267592](https://github.com/phanthienquoc/platform-infra/actions/runs/42199267592), 10:00:15Z | ~71m | 45m | SUCCESS but stale |
| Recovery controller | [#42199274660](https://github.com/phanthienquoc/platform-infra/actions/runs/42199274660), 10:00:18Z | ~71m | 45m | SUCCESS but stale |
| Schedule watchdog | [#42201400071](https://github.com/phanthienquoc/platform-infra/actions/runs/42201400071), 10:16:28Z | ~54m | 45m | SUCCESS but stale |
| VPS inspection | [#42193617816](https://github.com/phanthienquoc/platform-infra/actions/runs/42193617816), 09:15:08Z | ~116m | 75m | SUCCESS but stale |

The later reconcile #42207918291 and inspection #42208147735 are `workflow_dispatch` fallbacks, not native schedule events. The push watchdog #42208198166 is a diagnostic smoke run, also not a native schedule. Native Platform schedule delivery therefore remains stale despite successful manual recovery.

| TCE workflow | Latest native schedule run | Result |
|---|---|---|
| WF-06 healthcheck | [#42176208184](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176208184), 06:43:04Z | FAILURE; public probes returned HTTP 503 |
| WF-07 integration | [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608), 06:48:12Z | SUCCESS |
| WF-12 schedule watchdog | [#42158209117](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158209117), 03:43:01Z | FAILURE; native WF-06 freshness stale |
| WF-13 recovery | [#42176787185](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176787185) | SKIPPED by its recovery guard |

WF-12 [#42176769424](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176769424) at 06:48:22Z is a `workflow_run` after WF-07, not a native schedule. The new Platform observer independently queries only the public WF-06 `event=schedule` history and warns on stale delivery; it does not treat dispatch/fallback runs as schedule proof.

The GitHub Status API last reported “All Systems Operational” at 07:53:04Z, but this is an earlier component snapshot and does not prove that repository schedule events are being delivered at 11:10Z: [status API](https://www.githubstatus.com/api/v2/status.json). No causal link between the status history and these missing runs is established.

### Fresh read-only K3s snapshot

Snapshot: [debug/vps-latest.md](../debug/vps-latest.md), generated 2026-11-06 11:09:51Z by inspect-vps #42208147735.

- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk 56%, ~19 GiB available RAM, `restart_required=yes`. No reboot or package upgrade is authorized.
- GitOps drift: clean.
- Media backend/frontend: 1/1 Running, pinned to registry digests.
- MicroFE Shell/WS/NATS: 1/1 Running; Shell/WS are digest-pinned.
- Stock Admin: 0/1 with two Pods in ImagePullBackOff. New Backend Pod using `12d63b4` is ImagePullBackOff. Kubelet reports `no match for platform in manifest`; this is an ARM64 manifest gap, not evidence of bad GHCR credentials. Older Backend and Frontend remain 1/1 on `23b2878`.
- TCE frontend/service, Auth and Keycloak are desired 0/0. Public OIDC probes return HTTP 503. Keep strict HTTP 200 health assertions; do not activate replicas without owner approval.
- Only PVC/PV listed is `k3s-debug/k3s-debug-logs` (1 GiB, local-path, PV reclaim policy Delete). No Stock/Media PVC/PV or VolumeSnapshot/VolumeSnapshotContent references were found. This does not establish that external databases, object storage, backups, DNS or third-party data are disposable.
- Dedicated Media runner service is active and enabled; `/opt/media-actions-runner/bin/Runner.Listener` remains. The shared Platform runner is also active. Do not stop or unregister either without the exact operator-approved maintenance procedure.

### App CI and immutable publication status

- StockDividend master CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) passed ARM64 build-only checks. No new GHCR publisher run, full-SHA digest, provenance or release authorization was observed.
- Media Generation CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) passed but is older; no new publisher run was observed. Running workloads remain digest-pinned.
- Authentication CI [#42167100692](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42167100692) passed ARM64 build-only checks; no new manual release/publisher or digest/provenance was observed. PR #75/#76 retain skipped Supabase Preview checks.
- No new publisher evidence exists to authorize promotion in Stock, Media, TCE or Authentication. Routine reconciliation keeps image changes disabled.

### Dependency-safe next actions

1. Observe the next native Platform schedule ticks and TCE WF-06 delivery separately. Use existing Platform fallback only for stale Platform operations; do not count dispatch as schedule proof.
2. Keep TCE/Auth at 0/0 until the service owner authorizes activation; retain strict HTTP 200 probes and do not alter the TCE market-scan schedule.
3. Obtain operator confirmation that the dedicated Media runner is idle; only then stop, disable and unregister that runner and verify no Listener remains. Do not touch the shared Platform runner.
4. Require a fresh same-window storage preflight plus external database/object-storage backup and DNS ownership review before protected Stock/Media namespace decommission.
5. Stock/Auth publication and promotion remain blocked until an authorized publisher run proves full source SHA, GHCR digest, ARM64 manifest and provenance.

**Ownership:** app repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.

---

## Current review — 2026-11-06 13:03 ICT (2026-11-06 06:03 UTC)

This checkpoint revalidates all five default branches, open PRs, recent Actions runs, the TCE schedule/health failures, and the latest committed read-only K3s snapshot. It records observed state only; it does not authorize image publication, replica changes, runner retirement, or namespace deletion.

### Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `fb5c28f99148e6d4af8c43ffa2685c24e76635e5` | #1314 draft; #544/#541/#539 drafts | PRs #1320, #1321 and #1322 are merged; current master validation passes. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Strict public probes remain HTTP 503; WF-06 native schedule delivery is stale. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | Master CI passes ARM64 build-only checks for Admin, Backend and Scraper; no authorized GHCR publication observed. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | Latest master CI passes (historical run); no new publisher. Workloads remain active pending approved retirement. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | Master CI passes ARM64 build-only; release remains manual-only. |

### Platform Infra state

- PR #1322 updated the tracker/inventory after #1320 storage inventory and #1321 read-only inspection. Current master is `fb5c28f99148e6d4af8c43ffa2685c24e76635e5`.
- Latest master validation [#42168557657](https://github.com/phanthienquoc/platform-infra/actions/runs/42168557657) completed SUCCESS on this exact SHA. PR #1322 exact-head validation [#42168470421](https://github.com/phanthienquoc/platform-infra/actions/runs/42168470421) also passed before merge.
- Latest production reconcile in current run history remains [#42167232258](https://github.com/phanthienquoc/platform-infra/actions/runs/42167232258), SUCCESS at 05:14:26Z on an earlier commit, with `ALLOW_IMAGE_CHANGES=false`. Later PRs changed inspection/docs rather than production image or workload manifests; no new apply was required by this checkpoint.
- Unrelated open drafts: Platform #1314 mail-service plan and #544/#541/#539 Keycloak documentation. Authentication #75/#76 remain open. No PR is open in TCE, StockDividend or Media.

### TCE health and schedule delivery — exact failure diagnosis

- WF-06 workflow file remains active and its schedule declaration is unchanged at `*/15 * * * *`. The public health contract still expects HTTP 200 for all four endpoints.
- Latest observed native scheduled WF-06 run is [#42133793538](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133793538), created 2026-11-06 00:01:48Z, conclusion FAILURE.
- WF-06 [#42158243093](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158243093) at 03:43:21Z is a `workflow_dispatch` fallback, not a native schedule. Its four independent jobs all returned HTTP 503 (expected 200): TCE web, TCE API `/api/health`, Auth liveness `/api/health`, and Auth readiness `/api/ready`.
- WF-12 [#42158209117](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158209117) ran on its own native schedule at 03:43:01Z. It confirmed WF-06 is active, then detected that the latest native scheduled WF-06 run was 221 minutes old (budget 25 minutes). Its authenticated Platform heartbeat dispatch succeeded; the schedule-freshness job correctly failed.
- WF-13 [#42158228852](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42158228852) completed the read-only fallback dispatch. A fallback dispatch is explicitly not native schedule evidence and did not restore HTTP 200 health.
- The committed K3s snapshot still reports TCE frontend/service and Auth/Keycloak desired at 0/0. The 503s are therefore consistent with the recorded inactive runtime state; do not weaken the 200 assertions or turn a dispatch fallback into a green native schedule.
- This is a GitHub scheduled-event delivery gap plus intentionally inactive public services, not evidence that the app CI/build is failing. Do not change any TCE market-scan schedule or cron declaration.

### Other app CI and release evidence

- StockDividend master CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) SUCCESS, including ARM64 build-only checks for Admin, Backend and Scraper. These jobs use non-publishing CI and do not prove a GHCR release, digest, provenance or production authorization. The deployed Stock Admin/new Backend image issue remains unresolved; no promotion of tag `12d63b4`.
- Media Generation master CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) SUCCESS but is historical. No new release/publisher run or Platform handoff was observed.
- Authentication master CI [#42167100692](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42167100692) SUCCESS, including ARM64 build-only validation. No new publisher run, registry digest/provenance or promotion was observed. Keep PR #75/#76 gated by authoritative Supabase production integration side-effect/migration evidence.

### Latest committed K3s/storage evidence

- Latest read-only inspection remains [#42168105492](https://github.com/phanthienquoc/platform-infra/actions/runs/42168105492), snapshot generated 2026-11-06 05:23:12Z. No newer inspect-vps run was present in the inspected Platform Actions history.
- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk 56%, about 19 GiB available RAM, `restart_required=yes`. No reboot/upgrade is authorized.
- GitOps drift clean. Media backend/frontend remain 1/1 Running. Stock Admin (two Pods) and newer Backend remain ImagePullBackOff; legacy Backend/Frontend remain 1/1.
- Only `k3s-debug/k3s-debug-logs` PVC/PV appears in the snapshot; no Stock/Media PVC/PV claims or VolumeSnapshot/VolumeSnapshotContent references were listed. This does not prove external database/object-storage backups or DNS/data ownership.
- Dedicated Media runner is still active and enabled with `/opt/media-actions-runner/bin/Runner.Listener` present. Decommission guard must continue to block. Do not touch the shared Platform runner.

### Dependency-safe next actions

1. Investigate missing native WF-06 schedule events through GitHub Actions scheduling/operational support; retain the existing 15-minute healthcheck cadence and strict HTTP 200 probes. WF-13 fallback is recovery-only, not schedule proof.
2. Keep TCE/Auth services at their declared 0/0 until the service owner authorizes activation; do not change TCE market-scan schedule.
3. Operator verifies the dedicated Media runner is idle, then stops/disables/unregisters only that runner and confirms no Listener remains. No automation may attest this on the operator's behalf.
4. Repeat read-only K3s/storage preflight in the same maintenance window and obtain backup/external-data/DNS ownership review before considering the protected namespace-decommission workflow.
5. Keep Stock/Auth promotion blocked until an authorized publisher run proves exact full-source SHA, GHCR digest, ARM64 manifest and provenance; routine reconcile keeps image changes disabled.

**Ownership and safety:** app repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No production image, desired replica, namespace, PVC/PV, DNS, external database, runner, host or TCE market-scan schedule was changed by this checkpoint.

---

## Current review — 2026-11-06 12:26 ICT (2026-11-06 05:26 UTC)

This checkpoint follows Platform PRs #1320 and #1321. Both changes are merged; the second merge produced a fresh read-only VPS/K3s snapshot. This update records current evidence only and does not authorize release, runner retirement, namespace deletion, or any other production mutation.

### Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Current state |
|---|---|---|---|
| Platform Infra | `70dc56818596dd329e0eb055394d2bfde125b8ac` | #1314 draft, #544/#541/#539 drafts | PR #1320 storage snapshot references and PR #1321 fresh inspection snapshot merged. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Public health remains HTTP 503; no production publisher. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | Master CI now includes and passes native ARM64 builds for Admin, Backend and Scraper; no production publication. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | Existing CI evidence passes; runtime remains active pending approved retirement. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready, #76 draft | Master CI now includes and passes a native ARM64 image build; release remains manual-only and gated. |

### Platform PRs and validation

- PR #1320 — [Expose VolumeSnapshot references in read-only VPS inspection](https://github.com/phanthienquoc/platform-infra/pull/1320) — merged as `7943360e08e12d882c762484f95570682a1ef041`. Exact-head checks passed: `validate-manifests` #42167697233 and `validate-github-actions` #42167697100.
- PR #1321 — [Refresh VPS inspection state](https://github.com/phanthienquoc/platform-infra/pull/1321) — merged as `70dc56818596dd329e0eb055394d2bfde125b8ac`. Inspection #42168105492 completed SUCCESS; exact inspection PR head `5a9d73c866f7c41f00c05015e41753c1cebce6d8` passed validation #42168230639. Post-merge manifest validation #42168105545 and GitHub Actions validation #42168105411 both passed.
- The inspection workflow remained read-only. No reconcile, image promotion, namespace deletion, PVC/PV deletion, runner mutation, DNS, database, or host operation was performed by these PRs.
- Current unrelated Platform drafts: #1314 mail-service plan and Keycloak docs #544/#541/#539. They are not deployment blockers and are not merged as part of this work.

### Latest production workflow evidence

- Latest production reconcile in the returned history: [#42167232258](https://github.com/phanthienquoc/platform-infra/actions/runs/42167232258), completed SUCCESS at 2026-11-06 05:14:26 UTC on pre-inspection master SHA `2ec1d0f96ccbf679de1b156c3a40acd3221698f0`, with image changes disabled. This is not a reconcile after PR #1320/#1321; those PRs changed inspection/validation only.
- Post-merge validation: #42168105411 and #42168105545 SUCCESS on `7943360e08e12d882c762484f95570682a1ef041`; exact snapshot PR validation #42168230639 SUCCESS on `5a9d73c866f7c41f00c05015e41753c1cebce6d8`.
- Workflow-run recovery/watchdog events #42168288577, #42168288702, #42168296862 and #42168300708 were SKIPPED by their event guards; they are not native scheduled ticks. Do not count workflow_dispatch or workflow_run recovery as native schedule evidence.

### Fresh K3s snapshot — inspect-vps #42168105492

Snapshot `debug/vps-latest.md` generated at `2026-11-06T05:23:12Z` (blob `67782b5c4ba9609b0a69fc942a248bf92ae8310e`).

- Node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; disk use 56%, memory available ~19 GiB, `restart_required=yes`. No reboot/upgrade is authorized by this checkpoint.
- GitOps drift: clean.
- `media-prod`: namespace Active; backend and frontend both 1/1 Running, with digest-pinned images. Ingress `media.mrcute.space` remains present.
- `stock-prod`: namespace Active; Admin Deployment 0/1 with two Pods in ImagePullBackOff; new Backend Pod using tag `12d63b4` is ImagePullBackOff because its manifest has no matching ARM64 platform; older Backend and Frontend remain 1/1 Running.
- Persistent storage: the only listed PVC/PV is `k3s-debug/k3s-debug-logs`; no Stock/Media PVC/PV appears in this snapshot. New read-only inventory reports `stock-prod: none` and `media-prod: none` for VolumeSnapshot/VolumeSnapshotContent references. This is useful in-cluster evidence, not proof that external databases, object storage, DNS, backups, or third-party data are disposable.
- Dedicated Media runner remains **active and enabled**; `/opt/media-actions-runner/bin/Runner.Listener` is still present. The Platform runner is also active and must not be touched. The retirement guard correctly blocks decommission.
- `tce-prod` frontend/service and Auth/Keycloak workloads are desired 0/0 in this snapshot; public OIDC probes return 503. Keep strict HTTP 200 health checks; do not activate replicas or change the TCE market-scan schedule.

### Cross-repo CI and publication status

- **TCE Dashboard:** WF-06 #42158243093 failed all four public probes (TCE web/API and Auth liveness/readiness, HTTP 503). WF-12 #42158209117 failed the native schedule-freshness check; its Platform heartbeat dispatch succeeded. WF-13 #42158228852 dispatched a read-only fallback, but the fallback healthcheck also failed. Preserve strict HTTP 200 checks and investigate scheduled delivery separately from application availability.
- **StockDividend:** master CI #42167088130 SUCCESS, including native ARM64 build-only checks for all three production Dockerfiles. The exploratory branch CI #42166117405 is superseded by the same contract now present and passing on master. No new GHCR publication, registry digest/provenance, release authorization, or Platform promotion was observed. Do not promote the deployed `12d63b4` images.
- **Media Generation:** master CI #42136991059 SUCCESS (historical). No new release/publisher run. Runtime remains 1/1; the dedicated runner gate is independent of workload readiness.
- **Authentication:** master CI #42167100692 SUCCESS, including native ARM64 build and local architecture verification. The exploratory branch run #42166445643 is superseded by the master contract. The release workflow remains `workflow_dispatch` only; no publisher run, new digest/provenance, or promotion was observed. PR #75/#76 remain gated by the production Supabase integration side-effect review and stale exact-head checks.
- Source-contract/CI success is not GHCR publication or release authorization. App repositories own tests/builds and immutable publication; Platform owns manifests, shared pull credentials, provenance/digest validation, promotion, reconcile, rollout and health.

### Stock/Media decommission gate

- The fresh snapshot shows no Stock/Media PVC/PV and no VolumeSnapshot references, but it does not satisfy external-data/backup ownership review.
- The dedicated Media runner is still active/enabled with a Listener process. Do not supply the runner-retirement confirmation or invoke `.github/workflows/decommission-stock-media.yml`.
- Required next steps remain: operator verifies no active Media job; stop and disable only the dedicated Media runner service; unregister that runner from the Media repository; verify no Listener remains; independently review backups/external data/DNS ownership; take another same-window read-only inspection; then consider the protected manual decommission workflow with production Environment approval and exact typed confirmations.
- Never delete app repositories, source code, GHCR packages, external databases/object storage, DNS, or the shared Platform runner as part of namespace retirement.

### Next dependency-safe actions

1. Complete dedicated Media runner retirement through an authorized operator; current live snapshot fails the guard.
2. Re-run read-only inspection after runner retirement and repeat storage/external-data/backup/DNS review in the same maintenance window.
3. Only then consider manual deletion of exactly `stock-prod` and `media-prod`; do not delete persistent or external data.
4. Investigate TCE WF-06 native schedule delivery and 503 health separately; do not relax thresholds or touch market-scan cron.
5. Keep Stock release blocked until a new authorized publisher run proves full-SHA tags, GHCR digest and ARM64 manifest; keep Auth publication manual-only and PR #75/#76 gated pending authoritative Supabase side-effect evidence.

**Safety:** `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No TCE market-scan schedule change.


## Current review — 2026-11-06 10:21 ICT (2026-11-06 03:21 UTC)

Incremental cross-repository update after Platform PR #1311. This checkpoint records the latest exact heads, workflow outcomes and the current fail-closed Stock/Media retirement gate. It does not authorize a production release or destructive cluster action.

### Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Current state |
|---|---|---|---|
| Platform Infra | `40db4f6378d7f9cf21d830100fe0548e2197cc65` | #544/#541/#539 (draft) | PR #1310 runner guard and PR #1311 readiness documentation merged. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | App CI/workflow state unchanged; no production publisher dispatched. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | CI passed; immutable publisher remains separate and no new release was requested. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI passed; no production release or Platform handoff remains. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready / #76 draft | CI head is historical; Supabase integration/migration gates remain unresolved. |

### Latest workflow evidence

- Platform master validation [#42156021306](https://github.com/phanthienquoc/platform-infra/actions/runs/42156021306) completed SUCCESS on exact head `40db4f6378d7f9cf21d830100fe0548e2197cc65`. The run validated manifest rendering, immutable image policy, Auth digest contract, shell scripts and secret/network boundaries.
- The latest production reconcile [#42155789344](https://github.com/phanthienquoc/platform-infra/actions/runs/42155789344) completed SUCCESS on `a75980906ddec00c84dc64112fa87835906a6569`: MicroFE, Auth and TCE lanes passed; Keycloak was skipped; final gate and inspection-recovery trigger passed. This is evidence for that run/head, not a fresh rollout after the later docs-only PR #1311.
- TCE native WF-06 [#42133793538](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133793538) failed all four public probes with HTTP 503 (TCE web/API and Auth liveness/readiness). WF-12 [#42133822319](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133822319) passed and WF-13 [#42133822204](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133822204) completed its read-only fallback successfully; subsequent WF-13 [#42133843652](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42133843652) was skipped for a successful watchdog source. This is healthcheck evidence, not a production rollout. TCE market-scan schedule and all cron declarations remain untouched.
- StockDividend CI [#42137523269](https://github.com/phanthienquoc/stockdividend/actions/runs/42137523269) and Media CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) passed. Authentication CI [#41670642852](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852) passed on 2026-11-03; no newer Auth publisher run was observed.
- No new TCE, StockDividend, Media or Auth production publisher was dispatched. App CI success is not release authorization. TCE/Auth GitOps still use legacy tags; digest promotion requires a new exact publisher run, registry-confirmed digest/provenance and the normal Platform promotion path. Routine reconcile keeps image changes disabled.

### Stock/Media K3s decommission gate

- The latest committed read-only snapshot [inspect-vps #42154756357](https://github.com/phanthienquoc/platform-infra/actions/runs/42154756357) was generated at 2026-11-06T03:09:17Z. It shows the dedicated Media runner systemd service active and a Media `Runner.Listener` process; Media backend/frontend remain 1/1 Running. Stock Admin and the newer Backend remain ImagePullBackOff; the older Backend and Frontend remain 1/1. The snapshot reports no PVC/PV claims in `stock-prod` or `media-prod`, but the manual workflow must repeat the storage preflight in the same maintenance window.
- Platform PR [#1310](https://github.com/phanthienquoc/platform-infra/pull/1310) added a fail-closed check requiring the dedicated Media service to be inactive and its Listener process absent. The protected workflow also requires typed backup/external-data and runner-retirement attestations. It does not stop or unregister the runner.
- The manual `decommission-stock-media` workflow has not run. With the observed runner state, it must abort before namespace deletion. The service owner must first confirm no active job, stop the dedicated Media runner and unregister it from the Media repository. Do not stop the shared Platform runner.
- Do not delete PVs, external databases/object storage, DNS, GHCR packages, application repositories or source code. Do not change TCE/Auth desired replicas, production images, Keycloak or TCE market-scan schedules.

### Next dependency-safe actions

1. Obtain a new read-only VPS inspection after the Media runner is safely retired; repeat namespaced-object, PVC/PV and StorageClass preflight immediately before any deletion.
2. Require the service owner’s backup/external-data review and GitHub runner-unregistration confirmation before using the protected manual workflow.
3. Keep TCE/Auth digest promotion gated on an authorized, successful exact-source publisher run and registry digest verification; do not infer or reuse a historical digest.
4. Investigate the TCE/Auth public HTTP 503 health probes against the intentionally zero-replica state without changing any market-scan cron declaration.

`reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No K3s namespace, PV, DNS, external database, production image, desired replica count or schedule was changed in this checkpoint.

---

Last reviewed: 2026-11-06 10:18 ICT (2026-11-06 03:18 UTC)

## Current review — 2026-11-06 10:18 ICT (2026-11-06 03:18 UTC)

Incremental update to the 10:10 checkpoint below. Platform master is now `a75980906ddec00c84dc64112fa87835906a6569` after PR #1310; the four app-repository heads and their open-PR state are unchanged.

- Platform PR [#1310](https://github.com/phanthienquoc/platform-infra/pull/1310) adds a fail-closed guard to the manual Stock/Media namespace workflow. Before storage preflight or deletion it checks that the exact dedicated Media systemd service is inactive and that no `/opt/media-actions-runner/bin/Runner.Listener` process remains. GitHub runner unregistration remains a required operator attestation; the guard does not claim to verify the GitHub registration.
- Exact PR head `b32b75e4923d9f59ec8a8cc823828e7f5c2c6ba2` passed `validate-github-actions` [#42155669711](https://github.com/phanthienquoc/platform-infra/actions/runs/42155669711) and `validate-manifests` [#42155669700](https://github.com/phanthienquoc/platform-infra/actions/runs/42155669700); PR #1310 was squash-merged as `a75980906ddec00c84dc64112fa87835906a6569`.
- The latest read-only inspection snapshot #1308 (2026-11-06T03:09:17Z) still shows the Media runner service active. Therefore, the new guard would currently stop the manual decommission workflow before namespace deletion. It does not stop or unregister the runner.
- The same snapshot shows only the `k3s-debug` PVC/PV claim and no target-namespace PVC/PV claims. The workflow will still repeat its same-window storage preflight; backup/external-data review and runner retirement remain mandatory.
- Stock/Media namespaces, Services, Ingresses and workloads remain in K3s. Media backend/frontend are 1/1; Stock Admin and the newer Backend remain ImagePullBackOff because their ARM64 image manifests are unavailable; older Stock Backend and legacy Frontend remain 1/1. No workload or namespace was deleted.
- TCE and Auth still use legacy production tags in GitOps. No new publisher release or digest promotion was initiated. TCE schedule and all cron declarations remain unchanged.

Next action: the service owner must review backups/external-data ownership, stop the dedicated Media runner when idle, unregister it from the Media repository, and then use the protected manual workflow with its exact typed confirmations. Do not remove the shared Platform runner or delete PV/external data/DNS/GHCR packages.

---


## Current review — 2026-11-06 10:10 ICT (2026-11-06 03:10 UTC)

This checkpoint follows the successful merge of Platform PR #1307. It records current repository heads, exact-head validation, the remaining digest-promotion and K3s decommission gates, and the latest live cluster evidence retrieved in this pass.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `221d928575a9d9999827fcce5625f2cc06c9f9c6` | #544/#541/#539 drafts | PR #1307 merged; TCE source publisher job/step provenance is now enforced. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; WF-02 and WF-05 checks passed. No production release dispatched. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 removed the retired Platform handoff; CI passed. Publisher remains build/publish-only. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 removed the retired Platform handoff; CI passed. Publisher remains build/publish-only. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | PR #87 established digest/provenance handoff; #75/#76 remain gated on Supabase integration and migration review. |

### Exact workflow and merge evidence

- Platform PR [#1307](https://github.com/phanthienquoc/platform-infra/pull/1307) strengthened `verify-tce-publisher-run.sh`: a successful top-level TCE Actions run is no longer sufficient. The verifier now requires the exact release dependency jobs, native ARM64 frontend/backend build and artifact-integrity steps, GHCR publication, registry digest/ARM64 verification, and Platform dispatch correlation to be completed-success.
- Exact PR head `248802e05fa397b37d573749bf75be8bc57e2e45` passed `validate-github-actions` [#42154577734](https://github.com/phanthienquoc/platform-infra/actions/runs/42154577734) and `validate-manifests` [#42154577576](https://github.com/phanthienquoc/platform-infra/actions/runs/42154577576). PR #1307 was squash-merged as `67e8d8746934ec40b60b0fe0f62c5e4b3bcccfc2`.
- Platform inspection-only PR [#1308](https://github.com/phanthienquoc/platform-infra/pull/1308) refreshed the read-only K3s/storage snapshot at 2026-11-06T03:09:17Z; no production manifests were changed. Platform production reconcile [#42150629183](https://github.com/phanthienquoc/platform-infra/actions/runs/42150629183) completed SUCCESS: policy v15 verified, scope `all`, mode `apply`, `ALLOW_IMAGE_CHANGES=false`; MicroFE, TCE and Auth lanes passed, Keycloak lane skipped, and post-apply GitOps drift was clean. Recovery controller [#42150853420](https://github.com/phanthienquoc/platform-infra/actions/runs/42150853420) also completed SUCCESS.
- TCE PR #1026: WF-02 [#42105124810](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42105124810) and WF-05 [#42105124578](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42105124578) passed.
- StockDividend PR #32: CI [#42137106072](https://github.com/phanthienquoc/stockdividend/actions/runs/42137106072) passed.
- Media Generation PR #72: CI [#42135150058](https://github.com/phanthienquoc/media-generation/actions/runs/42135150058) passed.
- Authentication PR #87: auth-service CI [#41642031980](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41642031980) passed. This is historical PR evidence, not a new Auth production release run.
- No TCE, StockDividend, Media Generation, or Auth production publisher was dispatched in this checkpoint. App CI success is not production-release authorization.

### Stock/Media retirement: GitOps is removed; K3s workloads remain

- Platform PR #1301 retired Stock/Media GitOps ownership; PRs #1303/#1304 fixed push-scope classification/reconciliation; PR #1305 removed obsolete Stock/Media smoke/helper contracts. Stock PR #32 and Media PR #72 removed app-to-Platform production handoffs.
- The live Pod listing in reconcile #42150629183 at 2026-11-06T02:30:17Z still showed Media backend and frontend 1/1 Running. Stock Admin had two 0/1 ErrImagePull/ImagePullBackOff Pods; the legacy Backend and Frontend remained 1/1; a newer Backend Pod was 0/1 ImagePullBackOff. These are now orphaned from Platform GitOps ownership and were not deleted by reconcile.
- The latest committed read-only inspection snapshot is Platform PR #1308, generated at 2026-11-06T03:09:17Z. It shows only the k3s-debug PVC/PV claim and no PVC/PV claims in stock-prod or media-prod. This is fresh evidence of no target claims, but the protected manual workflow must repeat its same-window preflight immediately before deletion. The snapshot still shows the dedicated Media runner service active; no stop/unregister proof exists.
- The manual-only `decommission-stock-media` workflow has not run. Namespace deletion remains blocked on a fresh same-window object/PVC/PV/StorageClass inventory, backup and external-data ownership review, and independent confirmation that the dedicated Media runner is idle, stopped and unregistered. The protected production Environment and three typed confirmations remain mandatory. Preserve PVs, external databases/object storage, DNS, GHCR packages, app repositories and the shared Platform runner.

### Immutable digest promotion remains outstanding

- TCE production Kustomize still uses legacy paired tag `prod-v0.1.0-e75e338` for web/service; Auth still uses `prod-v1.0.0-ceb2688`. New publishers produce full-source-SHA tags and registry digests, and Platform validates provenance, but no new authorized TCE/Auth release was initiated to replace these references.
- Do not copy a digest from a historical node snapshot or infer it from a tag. Obtain a successful exact publisher run and registry-confirmed digest through the normal app-owned release workflow, then let Platform create the narrow digest-promotion PR. Routine reconcile keeps image changes disabled.
- Auth PR #75/#76 remain gated on authoritative Supabase production integration side-effect and migration-drift evidence. No migration or Auth activation was run.

### Next dependency-safe actions

1. Obtain a fresh read-only `inspect-vps` result and confirm current PVC/PV/StorageClass inventory and dedicated Media runner state.
2. After the service owner confirms backups/external-data retention and the Media runner is independently idle/stopped/unregistered, use only the protected manual namespace-decommission workflow. Do not delete storage or external resources implicitly.
3. Keep TCE/Auth digest promotion manual and provenance-bound; do not dispatch a production publisher without explicit release authorization.
4. Resolve Auth #75/#76 production Supabase/migration gates and verify one real qualifying TCE WF-13 recovery sequence without changing any cron declaration.

No TCE market-scan schedule, production image reference, desired replica count, shared credential, external database, DNS record, K3s namespace or PV was changed in this checkpoint. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.


---


## Current review — 2026-11-06 09:33 ICT (2026-11-06 02:33 UTC)

This review follows the merge of Platform PR #1304 and the successful post-merge production reconciliation. It records verified CI, GitOps, credential and rollout evidence separately from the still-unfinished Stock/Media namespace decommission and image-digest migration work.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | d6f45057f4a7eaba4c81d897aa64d9e5feb67fa1 | #544/#541/#539 draft | PR #1304 merged; post-merge validations and reconcile passed. |
| TCE Dashboard | 512b69d837e2a65c39867a062529a7fa0eada4cc | None | CI/workflow state unchanged; strict public WF-06 still reports the documented zero-replica HTTP 503 condition. |
| StockDividend | 6fcefa6b3792dab92b6d5c438001633d25f1ca28 | None | Latest master CI #42137523269 passed; production publisher/release was not triggered. |
| Media Generation | 3a8846a4f273eeb20a55b214d5ad80804c2d8d52 | None | Latest master CI #42136991059 passed; production publisher/release was not triggered. |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft | Master CI #41670642852 passed; #75/#76 remain gated on Supabase integration side effects. |

### Platform PR #1304 and production reconciliation

- PR #1304 added scripts/resolve-push-deployment-scope.sh to the push paths for the sole production reconcile workflow, enforced that trigger in validate-workflow-contracts.py, and added a full changed-path regression fixture from the Stock/Media retirement.
- Exact PR head 29dffd589c800ef3e3a545be128182ace615718a passed all three visible checks: validate-github-actions #42149835243, keycloak-ci #42149835246 and validate-manifests #42149835326. GitHub accepted the squash merge with expected head SHA; merge commit is d6f45057f4a7eaba4c81d897aa64d9e5feb67fa1.
- Post-merge master checks on that exact commit passed: validate-github-actions #42150629257, keycloak-ci #42150629258 and validate-manifests #42150629301.
- Reconcile run #42150629183 completed SUCCESS on the merge commit. The push resolver produced scope all; mode was apply and ALLOW_IMAGE_CHANGES=false. GHCR pull-access validation, Auth runtime Secret provisioning, shared GHCR pull-credential reconciliation, blocked-image-pull restart checks and TCE release-pair validation passed.
- Preflight found Kubernetes drift. The image-change guard passed and reported no existing workload image replacement; production manifests applied successfully and post-apply GitOps drift verification was clean.
- MicroFE, TCE and Auth deployment lanes passed. Keycloak lane was skipped by the current all-scope contract. TCE and Auth health checks explicitly accepted their intentional zero-replica state; no replicas were restored. MicroFE Shell/WS rollout and health passed.
- Recovery controller #42150853420 completed SUCCESS for source reconciliation #42150629183.
- Non-blocking telemetry issue: "Publish TCE deployment started event" could not connect to 127.0.0.1:18080 (curl exit 7). The step is continue-on-error, so this did not invalidate the reconcile or rollout gates. Verify whether the local event bridge is expected to be running before relying on this notification.
- The reconcile's cluster listing still showed Media workloads running and Stock workloads present (including Stock Admin ImagePullBackOff and older Backend/Frontend pods). The GitOps retirement does not prune those resources; namespace deletion has not run.

### Cross-repository publication and dispatch boundary

- StockDividend master CI #42137523269 passed all six jobs, including backend test/build, admin build, scraper build/syntax and production release-hold contract. No production publication or Platform dispatch was triggered.
- Media Generation master CI #42136991059 passed its application test/build job. No production release was triggered and no Platform dispatch receiver remains.
- TCE WF-03 remains manual-only and validates the full source SHA, paired web/service registry digests, ARM64 manifests and the source run/workflow/event/SHA payload before dispatch. No TCE production publisher run was initiated.
- Authentication release.yml remains manual-only and sends source run ID, workflow path, event, full source SHA and registry digest. Platform validates publisher provenance before promotion. No Auth release was initiated.
- Platform remains the owner of production manifests, shared GHCR pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health. App repositories retain tests/builds/immutable GHCR publication. No duplicate SSH/Compose/app-owned Kubernetes deployment authority was added.

### Outstanding GitOps digest pinning gap

- The current TCE production Kustomize file still contains the legacy paired tag prod-v0.1.0-e75e338 (7-character source prefix), rather than registry digest references. The live TCE verification in reconcile #42150629183 confirmed desired/live tag pairing, not registry digest pinning.
- The current Auth Kustomize file likewise still uses legacy tag prod-v1.0.0-ceb2688. The new TCE/Auth publisher contracts produce full-source-SHA tags and registry digests, and Platform has digest-promotion helpers, but no new authorized publisher dispatch has converted these existing manifest references.
- Do not invent or reuse a cached digest as current registry evidence. Next safe action is to obtain registry-confirmed digests tied to successful publisher provenance, then create atomic TCE web/service and Auth digest-promotion PRs. Keep image changes disabled in routine reconciliation.

### TCE, Auth and decommission safety

- TCE native WF-06 #42133793538 failed four strict public HTTP 200 probes with HTTP 503 while TCE/Auth/Keycloak were intentionally at zero replicas. WF-13 fallback #42133822204 passed read-only. Do not weaken health gates, restore replicas or change any TCE schedule.
- Auth PR #75 validation evidence is historical; Supabase Preview is skipped and the connected production integration's merge-triggered migration effect is not authoritatively verified. Do not merge #75/#76, run migrations or publish an Auth release on current evidence.
- The latest committed read-only inspection remains run #42145981473, snapshot generated 2026-11-06T01:46:04Z. It is stale for destructive action and showed the dedicated Media runner service active. It showed only the k3s-debug PVC/PV claim, but that historical observation is not a same-window storage preflight.
- The manual-only decommission-stock-media workflow has no execution run. No Stock/Media namespace, PVC/PV, DNS, GHCR package, external database/object storage or runner registration was deleted. Before namespace deletion, obtain fresh storage inventory, confirm backups/external-data ownership and independently verify the dedicated Media runner is idle, stopped and unregistered. Do not remove the shared Platform runner.
- reconcile-vps.yml remains the sole routine production apply authority; inspect-vps.yml remains read-only. TCE market-scan schedule and all other TCE schedules are unchanged.

### Next actions

1. Obtain fresh read-only K3s/PVC/PV/StorageClass and runner evidence; only then consider the protected manual Stock/Media namespace workflow with its exact typed confirmations.
2. Obtain registry-confirmed full-SHA digest evidence for the currently deployed TCE and Auth images; promote the paired TCE digests and Auth digest atomically through Platform PRs.
3. Diagnose the optional local deployment-event bridge at 127.0.0.1:18080 without weakening rollout/health gates.
4. Keep Stock/Media production publication closed unless explicitly authorized; keep Auth #75/#76 gated on the Supabase production integration effect.
5. Preserve every TCE schedule, especially the market-scan schedule.

---

Last reviewed: 2026-11-06 09:15 ICT (2026-11-06 02:15 UTC)

## Current review — 2026-11-06 09:15 ICT (2026-11-06 02:15 UTC)

This review follows the successful merge of PR #1303 and closes the remaining trigger gap that prevented a new production reconciliation attempt.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `e66bdecea35eda2c6740587b87ff69415c4176fa` | #1304 open; #544/#541/#539 draft | #1301 and #1303 merged; #1296 closed as superseded. #1304 adds the resolver to the sole production reconcile push filter. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Strict public health probes still return 503 while TCE/Auth/Keycloak remain operator-scaled to zero. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 merged; latest master CI #42137523269 passed. Production publication remains untriggered. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged; latest master CI #42136991059 passed. Production publication remains untriggered. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 passed. PR #75 validation passed, but Supabase Preview is skipped and the production integration side-effect gate remains unresolved. |

### Platform retirement, push-scope fix and remaining trigger gap

- Platform PR #1301 was squash-merged as `d05f806c636f3e785ffe603efff204767308efa0`; its exact-head manifest, GitHub Actions and Keycloak checks passed. PR #1296 was closed as superseded. The merge removed Stock/Media GitOps ownership but did not delete namespaces or persistent/external data.
- Post-merge reconcile #42146800843 failed before preflight or any cluster mutation because the push-scope resolver rejected deleted `scripts/bootstrap-media-runner.sh`. The failed run skipped GHCR credential bootstrap, manifest apply, rollout and app lanes.
- PR #1303 fixed the resolver classifications and regression tests, refreshed this tracker/inventory, and was squash-merged at `e66bdecea35eda2c6740587b87ff69415c4176fa`. Exact final-head checks passed: `validate-github-actions` #42148684639 and `validate-manifests` #42148684820.
- A follow-up inspection of `reconcile-vps.yml` showed its push path filter did not include `scripts/resolve-push-deployment-scope.sh`; therefore merging #1303 alone did not create another reconcile run. No new production reconcile was dispatched or applied after #1303.
- PR [#1304](https://github.com/phanthienquoc/platform-infra/pull/1304) adds the resolver to the push filter, makes `validate-workflow-contracts.py` enforce that trigger, and adds a full changed-path fixture from PR #1301. Its merge is intentionally expected to trigger the existing `reconcile-vps` workflow with scope `all`, mode `apply`, and `allow_image_changes=false`, subject to the protected production Environment approval and strict health gates. Its exact-head checks are pending; do not merge until they pass.

### App-owned publication and dispatch boundaries

- StockDividend `deploy.yml` retains app-owned CI/build/publication, immutable full-source-SHA image tags, registry digest resolution, ARM64 checks and the explicit manual publication hold. It contains no Platform repository-dispatch handoff.
- Media Generation `wf-03-media-production-deploy.yml` retains immutable full-source-SHA tags and paired registry digest/ARM64 verification. It contains no Platform repository-dispatch handoff.
- TCE WF-03 remains manual-only for production, verifies the full-source-SHA web/service digest pair and ARM64 manifests, and validates `tce-release-requested` source provenance before Platform promotion.
- Authentication `release.yml` remains manual-only and sends the Auth digest with source run ID, workflow path, event and full source SHA. Platform validates that provenance and the registry digest before updating Auth GitOps. No TCE/Auth release workflow was dispatched.

### TCE, Authentication and runtime safety

- TCE native WF-06 #42133793538 failed all four strict public HTTP 200 probes with HTTP 503 while TCE/Auth/Keycloak remain operator-scaled to zero. WF-13 fallback #42133822204 passed read-only. Do not weaken health gates, restore replicas or change any TCE schedule; the market-scan schedule is unchanged.
- Auth PR #75 remains gated because Supabase Preview is `SKIPPED` and the connected production integration's merge-triggered migration effect is not authoritatively verified. Do not merge #75/#76, run migrations or dispatch an Auth release on current evidence.
- `decommission-stock-media.yml` is manual-only and has no execution runs. Its protected production Environment, three exact confirmations and fresh storage preflight do not replace independent backup/external-data and dedicated-runner checks. The last committed VPS snapshot is stale and lacks fresh PVC/PV/StorageClass inventory.
- `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority, K3s namespace/PV/DNS/GHCR/external-data mutation, credential rotation, image promotion or schedule change occurred.

### Next actions

1. Poll PR #1304's exact current head; squash-merge only after all required checks pass.
2. Verify the merge-triggered `reconcile-vps` push run reaches fresh preflight, resolves scope `all`, and reports rollout/health truthfully. Keep image changes disabled.
3. Obtain fresh read-only K3s/PVC/PV/StorageClass evidence, confirm backups/external-data ownership and independently retire the dedicated Media runner before considering manual namespace deletion.
4. Keep Stock production publication closed without explicit release authorization and Auth #75/#76 gated on the Supabase integration side-effect question.
5. Preserve all TCE schedules, especially the market-scan schedule.

---

Last reviewed: 2026-11-06 09:10 ICT (2026-11-06 02:10 UTC)

## Current review — 2026-11-06 09:10 ICT (2026-11-06 02:10 UTC)

This review follows the StockDividend/Media GitOps retirement merge, inspects the five repository heads and active PRs, and records the first post-merge reconciliation regression plus its dedicated fix.

### Current repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `d05f806c636f3e785ffe603efff204767308efa0` | #1303 open; #544/#541/#539 draft | #1301 merged; #1296 closed as superseded. #1303 fixes the post-merge push-scope regression. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Strict public health probes still return 503 while TCE/Auth/Keycloak remain operator-scaled to zero. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 merged; latest master CI #42137523269 passed. No production publisher run or release promotion was triggered. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged; latest master CI #42136991059 passed. No production publisher run or release promotion was triggered. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 passed. PR #75 validation passed, but Supabase Preview is skipped and the production integration side-effect gate remains unresolved. |

### Platform retirement merge and reconciliation regression

- Platform PR [#1301](https://github.com/phanthienquoc/platform-infra/pull/1301) was squash-merged as `d05f806c636f3e785ffe603efff204767308efa0` from exact head `1e2f1d75009e5f79ef856b52f2b3ea7cc5cee545`. Exact-head `validate-github-actions` #42146647078, `validate-manifests` #42146647030 and `keycloak-ci` #42146647019 passed. Superseded plan-only PR #1296 was closed.
- The merge removed the StockDividend/Media manifest trees and their Platform reconcile, health, recovery, GHCR and publisher contracts. It added the manually invoked `decommission-stock-media` workflow. It did not delete K3s namespaces, PVs, DNS, GHCR packages, external data or runner registrations.
- Post-merge push reconciliation #42146800843 failed at `Resolve push deployment scope` because the resolver did not classify the deleted `scripts/bootstrap-media-runner.sh`. The job stopped before preflight, credential bootstrap, manifest apply, rollout or application lanes; no cluster mutation occurred. The accompanying Platform manifest validation #42146800900, GitHub Actions validation #42146800878, Keycloak CI #42146800876 and runner bootstrap #42146800844 passed.
- PR [#1303](https://github.com/phanthienquoc/platform-infra/pull/1303) updates the resolver and its regression tests. It treats retired/manual-only helper and validator-only paths as non-deploying, keeps the shared GHCR pull-access validator and production manifest/health paths cluster-wide, and makes a change to the resolver itself resolve to `all` so the merge can trigger a safe reconciliation attempt.
- The resolver's code-only revision passed exact-head `validate-github-actions` #42148457914 and `validate-manifests` #42148457910. The tracker/inventory update is included in the same PR, so checks must be re-read on the final updated head before merge.

### App-owned publication and dispatch boundaries

- StockDividend `deploy.yml` retains app-owned CI/build/publication, immutable full-source-SHA image tags, registry digest resolution and ARM64 checks, plus the explicit manual publication hold. The merged workflow no longer contains a Platform repository-dispatch handoff.
- Media Generation `wf-03-media-production-deploy.yml` retains app-owned image publication with full-source-SHA tags and paired registry digest/ARM64 verification. The merged workflow no longer dispatches Platform.
- TCE WF-03 remains manual-only for production release, uses full-source-SHA tags, verifies the web/service digest pair and ARM64 manifests, and validates the `tce-release-requested` payload before dispatching Platform. Platform's receiver validates source run/workflow/event/SHA, digest formats and tag-to-digest correlation before creating an atomic promotion PR.
- Authentication `release.yml` remains manual-only and sends the Auth digest with source run ID, workflow path, event and full source SHA. Platform validates that provenance and the digest before updating the Auth GitOps reference. No TCE/Auth release workflow was dispatched in this review.

### TCE, Authentication and runtime safety

- TCE native WF-06 #42133793538 failed all four strict public HTTP 200 probes with HTTP 503 (Auth liveness/readiness and TCE API/web). This matches the operator-requested zero-replica state. WF-13 fallback #42133822204 passed as a read-only recovery path. Do not weaken HTTP 200 gates, restore replicas, or change any TCE schedule; the market-scan schedule is unchanged.
- Auth PR #75 remains gated: its validation check passed, but Supabase Preview is `SKIPPED` and the connected production integration's merge-triggered migration effect is not authoritatively verified. Do not merge #75/#76, run migrations or dispatch an Auth release on current evidence.
- `decommission-stock-media.yml` is manual-only, requires the protected production Environment and three exact confirmations, and has no execution runs. The last committed VPS snapshot is stale and lacks fresh PVC/PV/StorageClass inventory. The dedicated Media runner's current state is unverified. Do not dispatch namespace deletion until a same-window inventory, backup/external-data review and idle/stopped/unregistered runner confirmation are complete.
- `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority was added. No K3s, credential, image, DNS, PV, database, object-storage or schedule mutation was performed.

### Next actions

1. Poll PR #1303's exact current head after the tracker update; squash-merge only if all required checks pass on that head.
2. Verify the merge-triggered push reconciliation now resolves to `all`; inspect its preflight and lane results. Keep the zero-replica health failures explicit rather than weakening health gates.
3. Obtain a fresh read-only K3s/storage inventory, confirm backups/external-data ownership and independently retire the dedicated Media runner before considering the manual namespace workflow.
4. Keep Stock production publication/promotion closed without explicit release authorization; keep Auth #75/#76 gated on the Supabase integration side-effect question.
5. Preserve all TCE schedules, especially the market-scan schedule.

---

Last reviewed: 2026-11-06 08:38 ICT (2026-11-06 01:38 UTC)

## Current review — 2026-11-06 08:38 ICT (2026-11-06 01:38 UTC)

This review re-read all five default-branch refs, open PRs, latest Actions run pages and exact-head checks, then inspected the active Platform decommission branch and its validation contracts. It distinguishes app publisher CI from an authorized production image release and branch-only GitOps changes from the current master runtime.

### Repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `b1a0c185e3f97630aa2bf55945bb5f674200bf97` | #1301 ready; #1296/#544/#541/#539 draft | #1301 proposes the complete Stock/Media GitOps retirement at head `dce6ae5341ce925177156f5fd9b537c453589323`; exact-head validation is queued. Master remains unchanged. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Native WF-06 #42133793538 returned HTTP 503 on four strict public probes while TCE/Auth/Keycloak remain operator-scaled to zero; WF-13 fallback #42133822204 passed and remained read-only. |
| StockDividend | `6fcefa6b3792dab92b6d5c438001633d25f1ca28` | None | PR #32 merged; post-merge CI #42137523269 PASS. No new production publisher run or Platform dispatch after merge; release hold remains closed. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged; post-merge CI #42136991059 PASS. The app publisher no longer dispatches Platform; no production release was triggered. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Latest PR validation runs #40446492086/#41329425940 are historical; Supabase Preview remains SKIPPED and the production integration side-effect gate is unresolved. |

### App-owned publisher boundary

- Stock PR [#32](https://github.com/phanthienquoc/stockdividend/pull/32) merged after exact-head review. Post-merge StockDividend CI #42137523269 passed. The app repo retains its own CI, ARM64 immutable image build and manual publication hold; no new publisher run or production tag/digest promotion was initiated.
- Media PR [#72](https://github.com/phanthienquoc/media-generation/pull/72) merged. Post-merge Media CI #42136991059 passed. The app repo retains paired immutable full-source-SHA GHCR publication/digest verification and no longer sends a Platform dispatch. No production release workflow was manually dispatched.
- App repos continue to own tests/builds/immutable GHCR publication. Platform owns only remaining production manifests, shared pull credentials, digest/provenance checks, GitOps promotion/reconciliation, rollout and health.

### Platform implementation PR #1301

- PR [#1301](https://github.com/phanthienquoc/platform-infra/pull/1301) is open at exact head `dce6ae5341ce925177156f5fd9b537c453589323`, 10 commits ahead of master and 0 behind.
- The branch removes all 19 files under `apps/stockdividend` and `apps/media-generation`, excludes both from production composition, removes their reconcile/health/recovery/GHCR and dispatch contracts, and deletes six obsolete app-specific runner/publisher helper files. It preserves app repositories, GHCR packages, TCE, Auth, MicroFE, Keycloak, cert-manager and the shared Platform runner.
- It adds a manual-only namespace workflow guarded by the protected production Environment and three typed confirmations. The live preflight enumerates all namespaced API object names without printing Secret/ConfigMap values, lists common workload status, checks PVC/PV claims and StorageClasses, and the root-owned wrapper can delete only `stock-prod` and `media-prod`.
- The first PR check set is queued: Validate Keycloak manifests/boundaries #42145176538, validate-manifests #42145176539, and validate-github-actions #42145176540. Do not merge until all required checks pass against the final exact head.
- Two earlier branch push runs (#42141922040 and #42142089191) belong to older commits, not the current PR head. They are not evidence of current-head validation.
- The plan-only PR #1296 is superseded by implementation PR #1301 and should be closed once the implementation PR is accepted.

### Runtime and schedule safety

- The latest committed read-only VPS snapshot is #42131886966, generated at 2026-11-05T23:46:15Z. It is stale for a destructive operation and does not include PVC/PV/StorageClass inventory. The dedicated Media runner was present in that snapshot; its current state is unverified.
- No K3s namespace, PV, DNS record, GHCR package, external database/object storage, host, or runner registration was changed. Namespace deletion remains a separate manual action after fresh same-window inspection, backup/external-data review, and independently verified Media-runner stop/unregister.
- TCE WF-06 HTTP 503 is consistent with the operator-requested zero-replica state. Keep strict HTTP 200 gates and all schedules, especially the TCE market-scan schedule, unchanged.
- `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority was added.

### Next actions

1. Poll #1301 exact-head checks; fix any failing contract and revalidate the updated head.
2. Squash-merge only after all required checks pass against the current PR head; close superseded draft PR #1296.
3. After merge, independently stop/unregister the dedicated Media runner, then use the manual namespace workflow only with a fresh live inventory and approved backup/external-data review.
4. Capture a fresh post-decommission inspection and verify TCE/Auth/MicroFE/Keycloak remain unchanged.
5. Keep Stock production publication/promotion closed without explicit release authorization; keep Auth #75/#76 gated on the unresolved Supabase integration effect.

## Current review — 2026-11-06 07:29 ICT (2026-11-06 00:29 UTC)

This review supersedes the 04:56 tracker entry and the 06:04 workflow-inventory checkpoint. It records the current five-repository state, the Media publisher-only merge, the Stock CI repair in progress, and the decommission safety boundary.

### Repository refs and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `3346be7997d017bd45eb0782331a7dafb9bb571c` | #1296 (draft), #544/#541/#539 (draft) | #1296 is a plan-only decommission runbook; exact-head `validate-manifests` #42131770950 PASS. No production or K3s resources changed. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 public checks fail on intentional HTTP 503 while TCE/Auth are operator-scaled to zero; WF-13 read-only fallback succeeded. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | #32 | Retired Platform dispatch removal is in review at exact head `c015961ec45ce7b698ea8fde9e2d7e9b5fe3c4f0`; latest CI #42137106072 is queued/in progress. Do not merge yet. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | PR #72 merged by squash; app publisher now builds, publishes and verifies immutable paired GHCR digests without dispatching Platform. Post-merge CI #42136991059 PASS. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Keep both gated: production Supabase integration side effect is still not authoritatively verified; Preview remains skipped. |

### App publisher contract changes

- Media PR [#72](https://github.com/phanthienquoc/media-generation/pull/72) merged at exact head `9e66bd6bdef065f5ca427cfd5e69b30b59c3cbab`; squash merge `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`. Exact-head PR/push CI #42135150058/#42135140342 both passed; post-merge push CI #42136991059 passed. The workflow retains immutable full-source-SHA tags, registry digest resolution and ARM64 verification, and no longer sends a Platform repository_dispatch.
- Stock PR [#32](https://github.com/phanthienquoc/stockdividend/pull/32) removes the Platform token check and atomic promotion dispatch while retaining app CI, the manual publication hold, native ARM64 image builds and immutable registry verification. The first contract run failed on stale assertions; the follow-up branch changes restored the validator self-path in `deploy.yml` path exclusions, renamed the CI step, corrected the exact manual-hold assertion and escaped literal GitHub expression markers in the shell test. Latest exact-head run #42137106072 is not complete; merge remains blocked until all exact-head checks pass.
- Do not enable `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`, promote either half of the Stock Admin/Backend pair, or change production image references without explicit release authorization and protected publisher provenance.

### Platform schedule and K3s evidence

- Latest native Platform inspect schedule: #42112599830 PASS at 2026-11-05 21:26:04Z. Latest read-only manual inspection: #42131886966 PASS, generated snapshot at 2026-11-05 23:46:15Z; this is not native schedule evidence.
- Latest native reconcile schedule #42121826106 failed only at the Stock health gate; native recovery #42121354158 passed; native schedule watchdog #42123445690 passed. Do not count workflow_dispatch/workflow_run fallbacks as cron ticks.
- Snapshot-time node: ARM64, 19 GiB available RAM, disk 56%, K3s service active. Media backend/frontend were 1/1 Running. Stock Admin had two ImagePullBackOff Pods, Stock Backend had one old 1/1 Pod plus one ImagePullBackOff Pod, and legacy Stock Frontend remained 1/1. Both namespaces, Services and Ingresses remained present.
- The snapshot shows the dedicated Media Actions runner service active. It does not contain PVC/PV or StorageClass inventory, so it is insufficient for namespace deletion or storage-retention decisions. No namespace deletion, runner unregister/stop, DNS change, PV deletion, or external storage/database mutation was performed.
- The snapshot is about 43 minutes old at this review and is not a live guarantee.

### TCE health and schedule guard

- TCE WF-06 #42133793538 (native schedule) failed all four strict public probes: Auth liveness/readiness and TCE API/web returned HTTP 503 instead of 200.
- This matches the documented operator-requested zero-replica state for TCE/Auth/Keycloak. WF-13 fallback #42133822204 completed successfully and remains read-only; no replica, ingress, health threshold or cron was changed.
- Preserve every TCE schedule, especially the market-scan schedule. Do not restore TCE/Auth/Keycloak replicas or weaken HTTP 200 gates without explicit operator authorization.

### Deployment authority and next safe work

- Ownership remains: app repositories own tests/builds and immutable GHCR publication; Platform Infra owns production manifests, shared GHCR pull credentials, publisher provenance/digest validation, GitOps promotion/reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No app workflow is allowed to add a competing SSH/Compose/kubectl production path.
- Next: complete and merge Stock PR #32 only after exact-head CI passes; then remove Stock/Media receiver, manifest, health and recovery contracts from Platform in a dedicated PR. Before deleting `stock-prod` or `media-prod`, extend/read a fresh inspection that inventories PVCs/PVs/storage classes, verify backups and DNS ownership, and confirm the dedicated Media runner is idle. Keep deletion a separate manually approved operation.
- No production image, manifest, credential, database, replica, host, namespace, DNS, PV, or cron mutation was made. TCE market-scan schedule unchanged.

## Current review — 2026-11-06 04:56 ICT (2026-11-05 21:56 UTC)

This review supersedes the 03:56 ICT entry. It re-reads all five default-branch refs, open PRs, latest Actions run pages, the latest native Platform inspection, the resulting K3s snapshot, the latest reconciliation lane results and the current TCE native-event history. It distinguishes native schedule runs from workflow_dispatch/workflow_run recovery.

### Repository refs, open PRs and latest workflow evidence

| Repository | Current default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | 419b83666cae7773b0a1dbc62900f275add05d9d | #544/#541/#539 (draft) | Native inspect-vps #42112599830 PASS at 04:26 ICT; inspection PR #1293 merged as current master. Reconcile dispatch #42112833885 failed only at Stock health. Recovery dispatch #42113114275 PASS. |
| TCE Dashboard | 512b69d837e2a65c39867a062529a7fa0eada4cc | None | PR #1026 merged. Latest master push checks WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 #42105365586 PASS. No eligible post-merge native WF-07/WF-12 sequence yet. |
| StockDividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None | Latest master CI #41563856934 and immutable publisher #41563856933 PASS on Nov 3; no newer app build or release publication. |
| Media Generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None | Latest master CI #41617592783 PASS on Nov 3; historical, not fresh validation. |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 (ready), #76 (draft) | Latest master Auth CI #41670642852 PASS on Nov 3; historical, not fresh validation. Supabase Preview remains SKIPPED on the open PRs. |

### Platform native inspection restored; PR #1293

- Native scheduled inspection #42112599830 ran at 04:26:04 ICT with event=schedule and concluded success.
- Its inspection job passed: Inspect VPS, detect meaningful changes, validate output, rebase snapshot, create inspection PR and validate the exact inspection PR head before squash merge.
- Automated inspection PR #1293 merged at 04:27:15 ICT. Its exact head was 375cefa0a9e08828df2052a60373b1ecf5ff5aa2 and the squash merge/current master SHA is 419b83666cae7773b0a1dbc62900f275add05d9d.
- The current debug/vps-latest.md snapshot was generated at 04:26:12 ICT. At this 04:56 review it is about 30 minutes old. This is genuine native-schedule inspection evidence, unlike the earlier workflow_dispatch snapshots.

### Latest reconciliation and StockDividend failure

- Reconcile #42112833885 was a workflow_dispatch run at 04:27:38 ICT, not a native schedule tick. It used mode=apply, target_app=stockdividend and allow_image_changes=false.
- Shared GHCR pull-access validation, GHCR credential bootstrap and the scoped image-pull recovery step succeeded. The Auth, Media, MicroFE and TCE lanes passed; Keycloak was skipped. The final gate correctly failed only because the StockDividend lane was unhealthy.
- The exact Stock lane log reports two Stock Admin Pods and one new Stock Backend Pod using ghcr.io/phanthienquoc/stockdividend/{admin,backend}:12d63b4 with ImagePullBackOff and no match for platform in manifest. The deployment stock-admin remained desired=1/ready=0/updated=1.
- The runner helper explicitly classified both errors as permanent architecture/manifest failures and logged that it was skipping rollout restart; no replacement rollout was triggered for those bad references. The regression test scripts/tests/restart-blocked-image-pulls.test.sh covers permanent failures, transient credential/network failures, mixed failures and unrelated CrashLoopBackOff. Do not add a redundant restart or bypass this guard.
- Preflight found no manifest drift, so image-change guard and production manifest apply were skipped. No production image reference was changed. The failure is not a GHCR pull-secret issue: shared access preflight and credential bootstrap passed.
- Recovery controller #42113114275 completed successfully at 04:29:33 ICT after the failed reconciliation. It is workflow_dispatch recovery evidence, not a native recovery schedule tick.

### Native Platform schedule matrix

| Workflow | Latest native event=schedule | Result | Latest non-native evidence |
|---|---|---|---|
| inspect-vps | #42112599830 — 04:26:04 ICT | PASS | Inspection PR #1293 merged; snapshot 04:26:12 ICT. |
| reconcile-vps | #42068683835 — Nov 5 23:51:03 ICT | FAIL at Stock health | #42112833885 workflow_dispatch failed at Stock health. |
| recover-stale-ops | #42068414686 — Nov 5 23:49:29 ICT | PASS | #42113114275 workflow_dispatch PASS after #42112833885. |
| reconcile-schedule-watchdog | #42070623710 — Nov 6 00:02:22 ICT | FAIL, inspection freshness | #42112872580 workflow_run SKIPPED. |

- The native inspection schedule has produced a new successful run. Do not continue describing inspect-vps as wholly stale.
- Native reconcile, native recovery and native watchdog schedule evidence remain old. Keep their native freshness separate from the newer manual/event-driven runs.
- Preserve all existing cron declarations. No schedule was edited.

### K3s snapshot at 04:26 ICT

Source: debug/vps-latest.md generated by native inspect-vps #42112599830.

- Node tce-k3s-01: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3.
- Disk 56%; available RAM about 19 GiB; restart_required=yes. No maintenance authorization was present, so no host restart or package upgrade.
- Media backend/frontend, MicroFE Shell/WS and NATS were 1/1 Running.
- Stock Admin had two ImagePullBackOff Pods on tag 12d63b4; the new Backend Pod was ImagePullBackOff on the same tag. The old Backend and Frontend remained 1/1.
- TCE frontend/service, microfe-auth and Keycloak were 0/0, matching the documented operator-requested shutdown. Their public HTTP 503 state is expected while that shutdown remains in force; do not restore replicas or weaken strict HTTP 200 health gates without fresh operator authorization.
- Snapshot is native inspection evidence at 04:26:12 ICT, not a live guarantee after that timestamp.

### TCE recovery status

- TCE master remains 512b69d837e2a65c39867a062529a7fa0eada4cc; PR #1026 is merged and post-merge WF-01/WF-02/WF-05/WF-12 checks passed.
- Latest native WF-07 is #42098832858 (Nov 5 02:57:39 ICT), before PR #1026 merged. Latest native WF-06 is #42089383865 (01:58:27 ICT, failure); latest native WF-12 is #42083178274 (01:19:51 ICT, failure).
- No post-merge native WF-07 success → WF-12 stale-WF-06 detection → WF-13 → exactly one WF-06 fallback sequence has yet exercised the new source-conclusion guard.
- WF-13 remains the only WF-06 fallback dispatcher. WF-12 is read-only. No TCE market-scan schedule or health gate was changed.

### App repository release and CI gates

- Stock publisher #41563856933 previously verified immutable full-source-SHA ARM64 artifacts for Scraper/Admin/Backend, but it is historical and its production promotion gate was disabled. Production Admin/Backend still reference tag 12d63b4, which is not ARM64-compatible. Do not set STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED or paired-promote without explicit release authorization and protected publisher-run provenance.
- Media master CI #41617592783 and Auth master CI #41670642852 are Nov 3 historical results, not fresh builds.
- Auth PR #75 remains ready at head a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05; PR #76 remains draft at head f19cacb0bf2b454b3152bd3a501f6f88d0a14a58. Supabase Preview is SKIPPED and the Deploy-to-production integration target/effect is not authoritatively verified. Do not merge either PR, dispatch a release, or run migrations on that evidence.
- Platform PR #544 (draft head c95e7daecb83b65577b54303427fe4ea81adfe06), #541 (draft head b8f7c6ba04e3d971336a899b2efd5894662083b3) and #539 (draft head 2dc48b97017ecb08e49682633303a2f1d5e991a1) remain open. Their observed checks are stale; do not merge drafts.

### Next actions and safety

1. Keep monitoring native inspect-vps after its successful #42112599830 schedule run; independently track native reconcile/recovery/watchdog freshness and investigate only if subsequent scheduled ticks are missed.
2. Keep Stock paired promotion blocked until explicit release authorization and protected publisher provenance; do not mutate the incompatible production tag.
3. Verify the first eligible post-merge native TCE WF-07 → WF-12 → WF-13 sequence and exactly one fallback with exact SHA/source correlation.
4. Keep Authentication PRs/migrations and Keycloak activation gated on authoritative Supabase integration and credential/DB evidence.
5. Keep TCE/Auth/Keycloak zero replicas until explicit operator reactivation authorization; retain strict public HTTP 200 gates.
6. Preserve app-owned tests/builds/immutable GHCR and Platform-owned manifests/credentials/provenance/promotion/reconciliation/rollout. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
7. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.

## Current review — 2026-11-06 03:56 ICT (2026-11-05 20:56 UTC)

This review reconciles the 03:42 checkpoint with the merged Platform PR #1291, completed TCE post-merge build, current open-PR heads/checks, latest Actions run pages, and the latest read-only VPS snapshot. It does not infer new production health from stale runtime evidence.

### Repository refs, open PRs and latest workflow evidence

| Repository | Current default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `086ee573f29b148bdb6ab55e3faa6a3000a5aa56` | #544/#541/#539 (draft) | PR #1291 merged at 03:42:45 ICT; post-merge validate-manifests #42105916492 PASS. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; post-merge WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 #42105365586 all PASS. WF-13 #42105390163 correctly SKIPPED for a WF-12 push-smoke source. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | Latest master CI #41563856934 and publisher #41563856933 PASS on Nov 3; no newer app build. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | Latest master CI #41617592783 PASS on Nov 3; historical, not fresh validation. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Latest master Auth CI #41670642852 PASS on Nov 3; historical, not fresh validation. |

### PR #1291 and current Platform master

- Platform PR [#1291](https://github.com/phanthienquoc/platform-infra/pull/1291) is closed/merged; its exact head was `9ae3f8da82d5bd13cf0f30d113fc632db43c0132`, and its squash merge commit is `086ee573f29b148bdb6ab55e3faa6a3000a5aa56`.
- Exact-head validation #42105809491 and post-merge master validation #42105916492 both PASS. The current master ref was independently read from GitHub's branch endpoint and matches the merge SHA.
- The previous 03:42 tracker entry listed the pre-merge Platform SHA `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6`; this entry supersedes it.
- Platform open PRs remain unchanged: #544 draft head `c95e7daecb83b65577b54303427fe4ea81adfe06`, #541 draft head `b8f7c6ba04e3d971336a899b2efd5894662083b3`, #539 draft head `2dc48b97017ecb08e49682633303a2f1d5e991a1`. Their only observed validate checks passed on Oct 14; these are stale checks and do not justify merging the drafts.

### Authentication PR gates

- PR #75 is open/ready at head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; validate passed Oct 27, while Supabase Preview is SKIPPED.
- PR #76 is open/draft at head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; validate passed Nov 1, while Supabase Preview is SKIPPED.
- The PR #75 description still records Deploy-to-production integration as ON and says the actual integration target/effect is not authoritatively verified. Do not merge either PR, dispatch release workflows, or run migrations until that external side effect is resolved.

### TCE post-merge verification and remaining native-event gap

- PR #1026 is present on current master `512b69d837e2a65c39867a062529a7fa0eada4cc`. Its source-conclusion guard is covered by successful post-merge WF-01/WF-02/WF-05/WF-12 checks.
- WF-13 #42105390163 was skipped because its source was the WF-12 push smoke #42105365586, not an eligible native schedule event. This is expected and is not a recovery failure.
- Latest native WF-07 remains #42098832858 (02:57:39 ICT), before PR #1026 merged. Latest native WF-06 remains #42089383865 (01:58:27 ICT, failure); latest native WF-12 remains #42083178274 (01:19:51 ICT, failure). No post-merge native WF-07 → WF-12 → WF-13 sequence has yet validated the new guard.
- Keep the confirmed operator-requested TCE/Auth/Keycloak zero-replica state and strict HTTP 200 health gates. No replica, ingress or market-scan schedule changes.

### Platform native schedules and fallback freshness

| Platform workflow | Latest native `event=schedule` run | Result |
|---|---|---|
| inspect-vps | #42049660972 — Nov 5 21:55:03 ICT | PASS, stale |
| reconcile-vps | #42068683835 — Nov 5 23:51:03 ICT | FAIL at Stock health gate |
| recover-stale-ops | #42068414686 — Nov 5 23:49:29 ICT | PASS |
| reconcile-schedule-watchdog | #42070623710 — Nov 6 00:02:22 ICT | FAIL, inspection freshness |

- The latest 100-run Actions page contains no later native `event=schedule` run for these Platform workflows. The current `inspect-vps.yml` still declares cron `2,32 * * * *`, uses the self-hosted ARM64 Platform/K3s/VPS runner, and is not to be conflated with manual fallback.
- The latest read-only inspection remains #42099284088, `workflow_dispatch`, generated at 03:00:41 ICT. At 03:56 it is about 56 minutes old and within the 75-minute fallback budget, but it is not native schedule evidence.
- Snapshot-time state: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB available RAM; `restart_required=yes`. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend (one Pod) ImagePullBackOff; old Stock Backend/Frontend 1/1; TCE frontend/service, microfe-auth and Keycloak 0/0.
- The snapshot is read-only evidence at its generation time, not a live inspection at 03:56. Do not restart the host or update packages without an approved maintenance window.

### Stock release and architecture gate

- Publisher #41563856933 verified immutable full-source-SHA ARM64 artifacts for Scraper/Admin/Backend. The release hold remained false; production handoff and paired promotion were skipped.
- Production Admin/Backend still reference tag `12d63b4`, which is incompatible with the ARM64 K3s node (`no match for platform in manifest`). Shared GHCR preflight/credential bootstrap had passed in the prior reconcile evidence, so do not misclassify this as a pull-secret failure.
- Do not set `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`, promote a single member of the Admin/Backend pair, or mutate production image references without explicit release authorization and protected publisher-run provenance.

### Next actions and safety

1. Keep native Platform schedule freshness distinct from workflow_dispatch fallback freshness; investigate delivery without changing any cron declaration or adding a competing apply authority.
2. Verify the first eligible post-merge native TCE WF-07 → WF-12 → WF-13 sequence exactly once; keep WF-13 as the only WF-06 fallback dispatcher.
3. Keep Stock paired promotion blocked until explicit release authorization and protected publisher provenance are verified.
4. Keep Auth PRs/migrations and Keycloak activation gated on authoritative Supabase integration and credential/DB evidence.
5. Keep TCE/Auth/Keycloak zero replicas until explicit operator reactivation authorization; retain strict public HTTP 200 gates.
6. Preserve app-owned tests/builds/immutable GHCR and Platform-owned manifests/credentials/provenance/promotion/reconciliation/rollout. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
7. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.

# Cross-Repository Production Deployment Tracker

## Current review — 2026-11-06 03:42 ICT (2026-11-05 20:42 UTC)

This review adds the TCE WF-12 source-filter hardening merged after the 03:34 review. It also preserves the direct GitOps explanation for the TCE/Auth 503 state.

### Repository refs and PRs

| Repository | Default-branch SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6` | #544/#541/#539 (draft) | PR #1290 merged; exact-head #42104850991 and post-merge #42104919461 PASS. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | PR #1026 merged; exact-head WF-02/WF-05 and post-merge WF-12/WF-02/WF-05 passed; post-merge WF-01 build is still running at this review. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | Publisher #41563856933 verified immutable ARM64 full-SHA artifacts; production hold false and paired promotion skipped. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | Latest CI #41617592783 is historical (Nov 3). |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Latest master CI #41670642852 is historical (Nov 3); PR #75 Supabase Preview is SKIPPED and commit status pending. |

### TCE PR #1026 — WF-07 source conclusion guard

- PR [#1026](https://github.com/phanthienquoc/TCE-dashboard/pull/1026) merged at 03:39:08 ICT as `512b69d837e2a65c39867a062529a7fa0eada4cc`.
- The WF-12 `verify` job now accepts a `workflow_run` source from WF-06 as before, but accepts WF-07 only when that native scheduled WF-07 run concluded `success`. A failed WF-07 still emits the existing Platform heartbeat; it cannot independently cause the stale-WF-06 watchdog path to fail and trigger WF-13.
- WF-06 native failures remain independently handled by WF-13. WF-12 remains read-only and WF-13 remains the only WF-06 fallback dispatcher. No cron or market-scan schedule changed.
- Exact-head checks on `d3025bcdf63e90eff24c36b10ce6d03133f69f50`: WF-02 PR #42105124810 PASS; WF-05 PR #42105124578 PASS; push WF-02 #42105113543 PASS and push WF-05 #42105113596 PASS.
- Post-merge checks on `512b69d837e2a65c39867a062529a7fa0eada4cc`: WF-12 push smoke #42105365586 PASS; WF-02 #42105365483 PASS; WF-05 #42105365567 PASS. WF-01 build/verify #42105365294 was still in progress at 03:42 ICT after the frontend image build passed and backend image build began; do not call the full post-merge build green until it completes.
- No post-merge native WF-07/WF-12 schedule event has yet exercised the new source-conclusion guard. Latest native WF-07 #42098832858 (02:57:39 ICT), WF-12 workflow_run #42098855352 (02:57:48 ICT), and WF-13 #42098897759 (02:58:04 ICT) all predate PR #1025 and #1026 merges. Latest native WF-06 #42089383865 (01:58:27 ICT) and native WF-12 #42083178274 (01:19:51 ICT) remain old failures.

### Confirmed TCE/Auth public 503 state

- TCE ingress routes `tce.mrcute.space/` to `tce-frontend` and `/api` to `tce-service`; both backing Deployments explicitly set `replicas: 0` under a temporary operator shutdown request.
- Auth ingress routes `auth.mrcute.space` to `microfe-auth`; its Deployment explicitly sets `replicas: 0` under the same operator shutdown intent. Keycloak also explicitly sets `replicas: 0`.
- These source manifests and ingress mappings explain the public 503 probes. The healthcheck is correctly reporting intentional unavailability, not a new image or credential regression. Do not restore replicas, alter ingress or weaken HTTP 200 gates without explicit operator authorization.

### Platform runtime and native schedule evidence

- Platform PR #1290 merged as `04fab34ea9e1a8d2803881b4587e8f15b89e4cd6`; exact-head #42104850991 and post-merge #42104919461 passed.
- Latest native Platform schedules remain inspect-vps #42049660972 (Nov 5 21:55 ICT), reconcile-vps #42068683835 (23:51, Stock health failure), recover-stale-ops #42068414686 (23:49, PASS), and watchdog #42070623710 (Nov 6 00:02, inspection freshness failure). No newer native `event=schedule` run appeared through the latest run page after #42104919461.
- Recovery #42099209509 dispatched read-only inspect #42099284088, which passed and generated `debug/vps-latest.md` at 03:00:41 ICT. At 03:42 it is about 41 minutes old and remains within the 75-minute fallback budget; it is workflow_dispatch evidence, not native schedule evidence.
- Snapshot-time runtime remains: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB available RAM; `restart_required=yes`. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff; old Backend/Frontend 1/1; TCE frontend/service, microfe-auth and Keycloak 0/0.
- Stock production overlay still uses `newTag: 12d63b4` for Admin and Backend. Publisher #41563856933 verified ARM64 full-SHA artifacts, but the production hold was false and paired promotion was skipped. Platform's `validate-ghcr-image-reference.sh` independently verifies ARM64 manifests/configs before accepting a promotion. Keep the old tag blocked; do not promote without explicit release authorization and protected publisher provenance.

### Next actions and safety

1. Wait for TCE post-merge WF-01 #42105365294 to finish; then verify the next post-merge native WF-07 → WF-12 → WF-13 sequence exactly once.
2. Keep TCE/Auth/Keycloak at their explicitly requested zero-replica state until a new operator authorization resolves the Supabase/Keycloak issue.
3. Keep Stock paired promotion disabled until explicit release authorization and protected publisher provenance are verified.
4. Keep native schedule freshness separate from workflow_dispatch fallback freshness; preserve every cron declaration.
5. Keep Auth migrations and Keycloak activation gated; wait for an approved VPS maintenance window before host/package changes.
6. Preserve app-owned tests/builds/immutable GHCR and Platform-owned manifests/credentials/provenance/promotion/reconciliation/rollout. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
7. No production image, manifest, credential, database, replica, host or cron mutation. TCE market-scan schedule unchanged.


## Runtime diagnosis update — 2026-11-06 03:34 ICT (2026-11-05 20:34 UTC)

This update supersedes the earlier statement that TCE/Auth public HTTP 503 responses were only correlated with zero-replica observations. Current GitOps source manifests and their ingress routes now prove the expected upstream-unavailable state.

### Public 503 root cause — intentional operator shutdown

- TCE ingress `apps/tce-dashboard/overlays/prod/ingress.yaml` routes `tce.mrcute.space/` to Service `tce-frontend:80` and `/api` to `tce-service:8210`.
- Both backing Deployments explicitly declare `replicas: 0` in `apps/tce-dashboard/base/frontend.yaml` and `apps/tce-dashboard/base/service.yaml`, with comments recording the temporary operator request to scale TCE down until re-enabled.
- Auth ingress `platform/microfe/ingress.yaml` routes `auth.mrcute.space/` to Service `microfe-auth:80`.
- The backing `platform/auth-service/deployment.yaml` explicitly declares `replicas: 0` and records the temporary operator request to stop Auth API and Keycloak until the Supabase/Keycloak connection issue is resolved.
- `platform/keycloak/deployment.yaml` also explicitly declares `replicas: 0` under the same operator shutdown intent.
- These routes plus zero desired replicas explain the strict public 503 probes for TCE web/API and Auth readiness/liveness. The healthcheck is correctly reporting intentional unavailability; it is not evidence of a new image-pull or deployment regression.
- Do not restore replicas, alter ingress, or weaken HTTP 200 gates without a new explicit operator authorization. The existing shutdown state is intentional and must remain GitOps-managed.

### PR #1289 completion

- PR #1289 merged by squash as `f5d62e4a4f9abd992458849929a14a85a3250614`.
- Exact-head validation #42104285775 PASS on `5a570ae15ded480b2c391941db9bc71eeb8d4cb5`.
- Post-merge validation #42104477168 PASS on the merge SHA. Manifest rendering, digest-promotion helpers, MCP GitOps-only contract, shell checks, Auth GitOps, YAML structure, secret policy, immutable image policy, Keycloak isolation and network boundaries passed. Changed-image validation was skipped because PR #1289 was documentation-only.

### Updated next actions

1. Keep TCE/Auth/Keycloak at their operator-requested zero-replica state until the operator resolves the Supabase/Keycloak issue and explicitly authorizes reactivation.
2. Continue verifying the new TCE PR #1025 stale-WF-06 recovery path on a post-merge native WF-07/WF-12 event; do not count pre-merge runs as E2E evidence.
3. Keep Stock Admin/Backend paired promotion blocked until explicit release authorization and protected publisher provenance; current tag `12d63b4` remains ARM64-incompatible.
4. Preserve native schedule freshness separately from workflow_dispatch fallback freshness; do not change cron declarations.
5. Keep Authentication migrations and Keycloak activation gated; wait for an approved VPS maintenance window before host/package changes.


## Current review — 2026-11-06 03:27 ICT (2026-11-05 20:27 UTC)

This review re-read all five default-branch commits, open PRs, latest Actions runs, Platform native schedule history, the latest reconciliation and lane summaries, the current read-only VPS snapshot, Stock's publisher contract/run, and TCE's newly merged recovery change. It supersedes the 01:58 review below.

### Repository refs, open PRs and CI evidence

| Repository | Current default-branch SHA | Open PRs | Latest evidence |
|---|---|---|---|
| Platform Infra | `9d533e503d412e583873a91aefd66263c297fafa` | #544/#541/#539 (draft) | Inspection-state PR #1288 merged at 03:01:43 ICT; exact inspection branch validation #42099407335 PASS. Latest master read-only inspection #42099284088 PASS. |
| TCE Dashboard | `162390fe4811131c11d3f39d264e0722a826dc0f` | None | PR #1025 merged at 03:22:34 ICT; exact-head WF-05 #42102448205 and WF-02 #42102448276 PASS; post-merge WF-01 #42102796954, WF-05 #42102795916 and WF-02 #42102795382 PASS. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and publisher #41563856933 PASS (Nov 3); publisher verified all three immutable full-SHA ARM64 image manifests, while production promotion was held/skipped. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | Latest master CI #41617592783 PASS (Nov 3); no newer app build in the latest run page. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 (ready), #76 (draft) | Latest master CI #41670642852 PASS (Nov 3); no newer master build. Supabase Preview checks on the open PRs remain SKIPPED. |

Open PR heads were re-read:
- Platform #544: `c95e7daecb83b65577b54303427fe4ea81adfe06` (draft); #541: `b8f7c6ba04e3d971336a899b2efd5894662083b3` (draft); #539: `2dc48b97017ecb08e49682633303a2f1d5e991a1` (draft).
- Authentication #75: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` (ready); #76: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` (draft). Their passing checks are historical and Supabase Preview is skipped; do not merge or run migrations on that evidence.
- No open PRs in TCE Dashboard, StockDividend or Media Generation. Do not treat Nov 3 app CI as fresh validation.

### TCE PR #1025 — new stale-WF-06 recovery path

- PR [#1025](https://github.com/phanthienquoc/TCE-dashboard/pull/1025) merged as `162390fe4811131c11d3f39d264e0722a826dc0f` at 03:22:34 ICT.
- It closes the gap where a successful native WF-07 schedule causes WF-12 to detect a stale native WF-06 schedule, but WF-13 previously ignored the resulting workflow_run event.
- WF-12 remains read-only. It requests WF-13 only after a successful native WF-07 schedule leads to a failed stale-WF-06 verification; the request is correlated to the exact WF-12 run and its failed job/step evidence. WF-13 remains the only WF-06 fallback dispatcher.
- Exact-head WF-05/WF-02 checks and all three post-merge master checks passed.
- Important ordering: WF-07 #42098832858 (02:57:39 ICT), WF-12 workflow_run #42098855352 (02:57:48 ICT, failure), and WF-13 #42098897759 (02:58:04 ICT, skipped) all ran before PR #1025 merged. They do not exercise the new code. No qualifying post-merge native WF-07/WF-12 event has yet proved the new path end-to-end.
- Latest native TCE evidence remains WF-06 #42089383865 (01:58:27 ICT, failure) and WF-12 #42083178274 (01:19:51 ICT, failure). The earlier WF-06 fallback #42089448641 also failed all four strict public probes with HTTP 503. Keep HTTP 200 gates and every TCE cron declaration unchanged.

### Platform native schedule evidence — separate native schedules from fallbacks

| Platform workflow | Latest native `event=schedule` run | Result |
|---|---|---|
| inspect-vps | #42049660972 — Nov 5 21:55:03 ICT | PASS, stale |
| reconcile-vps | #42068683835 — Nov 5 23:51:03 ICT | FAIL at Stock health gate |
| recover-stale-ops | #42068414686 — Nov 5 23:49:29 ICT | PASS |
| reconcile-schedule-watchdog | #42070623710 — Nov 6 00:02:22 ICT | FAIL, inspection freshness |

The latest 100 Platform Actions runs through #42099407335 (03:01:17 ICT) contain no later native `event=schedule` run. Do not attribute the missing native inspect event to runner queue without new evidence. The workflow's existing cron remains `2,32 * * * *`; the recovery controller still distinguishes native schedule freshness from workflow_dispatch fallback freshness. Preserve all cron declarations.

### Latest reconciliation and current read-only K3s snapshot

- Reconcile #42098901197 (workflow_dispatch, 02:58:05 ICT; source Platform SHA `fff1767db7e8e3d14b78ed84a5f7e03bef9341cd`) failed only in the StockDividend lane. Shared GHCR preflight, Auth runtime Secret provisioning and pull-credential bootstrap passed. Media, MicroFE, TCE and Auth lanes passed; Keycloak was skipped. Production manifest apply and image changes were skipped with `allow_image_changes=false`.
- Stock failure was isolated to Admin (two Pods) and the new Backend Pod on image tag `12d63b4`; containerd reports `no match for platform in manifest`. The failure is architecture compatibility, not evidence of a shared pull-secret problem. Existing Stock Backend and Frontend remained 1/1 in this snapshot.
- Recovery #42099209509 passed and dispatched read-only inspection #42099284088, which passed. Snapshot `debug/vps-latest.md` was generated 03:00:41 ICT. At this review it is about 27 minutes old and within the 75-minute fallback budget, but it is a workflow_dispatch snapshot, not native schedule evidence.
- Snapshot-time host/runtime: node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB available RAM; `restart_required=yes`.
- Snapshot-time workloads: Media backend/frontend 1/1; MicroFE Shell/WS and NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff; old Backend and Frontend 1/1; TCE frontend/service 0/0; microfe-auth and Keycloak 0/0. These are observations from the 03:00 snapshot, not a claim about later live state.

### Stock immutable publisher and paired promotion gate

- Current Stock publisher workflow uses an ARM64 runner, builds Scraper/Admin/Backend for `linux/arm64`, tags each image with the full source SHA, and verifies each registry manifest/digest before any promotion handoff.
- Publisher #41563856933 passed the ARM64 runner check, all three builds, and immutable ARM64 registry verification. Its production-release hold returned `release_enabled=false`; handoff validation and atomic paired promotion were skipped.
- The current production tag `12d63b4` remains architecture-incompatible. Do not repoint production to a new digest or promote Admin/Backend separately. The exact next gate is explicit release authorization (`STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`) plus protected publisher-run provenance/Actions:read verification and the existing paired digest contract. Do not enable the release variable or dispatch promotion without authorization.

### Authentication, Media and Keycloak gates

- Media's latest CI is historical (Nov 3); its 1/1 workload status is only from the 03:00 snapshot.
- Authentication's latest master CI is historical (Nov 3). PR #75/#76 remain gated because Supabase Preview is skipped and the production integration side-effect binding is not authoritatively verified. Do not merge or run migrations.
- Keycloak remains 0/0 in the current snapshot. Platform PR #544/#541/#539 are still drafts; the Keycloak runtime DB credential and SSO ingress prerequisites are not proven. Do not activate the lane.

### Next dependency-safe actions

1. Wait for the next native WF-07 schedule after PR #1025 merge; verify native WF-07 → read-only WF-12 stale-WF-06 evidence → exactly one WF-13 → one read-only WF-06 fallback, with source run/attempt/SHA correlation. Do not count pre-merge #42098855352/#42098897759 as proof.
2. Keep strict TCE/Auth HTTP 200 health gates. Investigate ingress/service/endpoints using fresh runtime evidence; the 0/0 snapshot and 503 probes are correlated, not a proven root cause.
3. Keep Stock paired promotion closed until explicit authorization and protected publisher provenance are both verified.
4. Continue distinguishing native Platform schedule freshness from the fresh workflow_dispatch inspection fallback; preserve cron declarations and do not dispatch duplicate inspection while the fallback remains within 75 minutes.
5. Keep Authentication migrations and Keycloak activation gated on authoritative credentials/integration evidence.
6. Wait for an approved VPS maintenance window before host restart or Docker/containerd package changes.

### Safety invariants

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, provenance/digest verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred in this review.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows.
- TCE market-scan schedule unchanged.


Last reviewed: 2026-11-06 08:38 ICT (2026-11-06 01:38 UTC)
Platform Infra master at checkpoint: b1a0c185e3f97630aa2bf55945bb5f674200bf97
Latest checkpoint: docs/cross-repo-workflow-inventory-checkpoints/2026-11-06-0838-ict.md

## Current review — 2026-11-06 01:58 ICT (2026-11-05 18:58 UTC)

This review re-read all five default-branch refs, open PRs, recent Actions runs, current open-PR heads, Platform native schedule history, the active reconciliation and its lane logs, TCE native WF-06/WF-13/fallback runs, and the current runtime snapshot. It supersedes the 00:56 review below.

### Current repository refs and open PRs

| Repository | Default branch SHA | Open PRs | Latest evidence in this review |
|---|---|---|---|
| Platform Infra | \`ffbfecaa19730a5cef9861c313a2e1597ac05eaf\` | #544/#541/#539 (draft) | Inspection snapshot PR #1286 is on master; reconciliation #42089469075 failed only Stock health; post-reconcile recovery #42089788857 passed. |
| TCE Dashboard | \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\` | None | Native WF-06 #42089383865 failed; WF-13 #42089421154 successfully dispatched exactly one fallback #42089448641, which also failed the four strict public probes. |
| StockDividend | \`50ba0dfb67eb3dfaa376db0c752bbef5b0817bec\` | None | CI #41563856934 and immutable ARM64 publisher #41563856933 passed on Nov 3; current production Admin/Backend image references remain incompatible with ARM64. |
| Media Generation | \`e4c7d8990aafc7d837e918c9caf39722d623de7c\` | None | CI #41617592783 passed on Nov 3; Media lane passed in reconciliation #42089469075. |
| Authentication | \`f978a3f378ee22d4630909c2d182275b21ac9e9a\` | #75 (ready), #76 (draft) | CI #41670642852 passed on Nov 3; Auth lane passed in #42089469075. |

Open PR heads were re-read:
- Platform #544: \`c95e7daecb83b65577b54303427fe4ea81adfe06\` (draft).
- Platform #541: \`b8f7c6ba04e3d971336a899b2efd5894662083b3\` (draft).
- Platform #539: \`2dc48b97017ecb08e49682633303a2f1d5e991a1\` (draft).
- Authentication #75: \`a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05\` (ready); latest exact-head checks remain historical: validate PASS #40446492086 (Oct 27), Supabase Preview SKIPPED.
- Authentication #76: \`f19cacb0bf2b454b3152bd3a501f6f88d0a14a58\` (draft); validate PASS #41329425940 (Nov 1), Supabase Preview SKIPPED.
- No open PRs in TCE Dashboard, StockDividend or Media Generation. Do not describe historical PASS checks as fresh validation.

### Native schedule evidence — event types remain distinct

| Platform workflow | Latest native \`event=schedule\` run | Result |
|---|---|---|
| inspect-vps | #42049660972 — 2026-11-05 21:55:03 ICT | PASS, stale |
| reconcile-vps | #42068683835 — 2026-11-05 23:51:03 ICT | FAIL only Stock health |
| recover-stale-ops | #42068414686 — 2026-11-05 23:49:29 ICT | PASS |
| reconcile-schedule-watchdog | #42070623710 — 2026-11-06 00:02:22 ICT | FAIL inspection freshness |

The latest 100 Platform Actions runs through #42089788857 (19:00:57Z / 02:00:57 ICT) contain no native schedule run after watchdog #42070623710. Native inspection #42049660972 is 246 minutes old at the recovery API reference clock; the latest native watchdog is also stale. This is not evidence of runner queue congestion. The inspection workflow is active, and the recovery controller separately measures native schedule freshness versus workflow_dispatch fallback freshness. Preserve all existing cron declarations.

### TCE WF-13 native recovery — first post-merge end-to-end proof

- Native WF-06 schedule #42089383865 started 2026-11-06 01:58:27 ICT, on master SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, and failed all four public endpoint probes.
- WF-13 #42089421154 started at 01:58:42 ICT and completed PASS. Its source validation confirmed workflow ID \`339198323\`, path \`.github/workflows/wf-06-tce-healthcheck.yml\`, source run #42089383865, event \`schedule\`, attempt 1, master branch and exact source SHA.
- WF-13 dispatched read-only WF-06 with \`ref=master\`, exact SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, and no inputs. The job correlated the dispatch to fallback #42089448641. No deployment or mutation authority is involved.
- Fallback #42089448641 completed FAILURE: TCE web, TCE API, Auth readiness and Auth liveness all remained HTTP 503 (expected 200).
- WF-13 run #42089450102 for the subsequent WF-12 \`workflow_run\` source #42089421216 was SKIPPED; it is not a second native schedule failure and no second fallback was dispatched.
- This proves one qualifying native WF-06 failure → one WF-13 dispatch → one exact-master WF-06 fallback. It does not prove service recovery; all four endpoint probes still fail. Keep strict HTTP 200 checks and all TCE cron declarations unchanged.

### Platform heartbeat, reconciliation and release gates

- Platform recovery #42089440296 validated the TCE repository, source workflow path, source run #42089383865, event \`schedule\`, attempt 1, source SHA \`c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c\`, and WF-12 heartbeat run #42089421216.
- It dispatched the existing Platform GitOps authority with exact payload: \`ref=master\`, SHA \`ffbfecaa19730a5cef9861c313a2e1597ac05eaf\`, \`mode=apply\`, \`allow_image_changes=false\`, \`target_app=all\`.
- Reconciliation #42089469075 completed FAILURE only at the final lane gate. Shared GHCR preflight, Auth runtime Secret provisioning and GHCR credential bootstrap passed. Production manifest apply and image changes were SKIPPED; \`ALLOW_IMAGE_CHANGES=false\`.
- Media, MicroFE, TCE and Auth lanes passed their scoped checks; Keycloak lane was skipped. StockDividend lane failed: two Admin Pods and one new Backend Pod were in ImagePullBackOff on tag \`12d63b4\`, with containerd reporting \`no match for platform in manifest\`. The failure is architecture compatibility, not a shared GHCR credential failure. No half-pair promotion was attempted.
- Post-reconcile recovery #42089788857 completed PASS. It confirmed native inspection remained stale, but the last read-only workflow_dispatch snapshot #42083607462 was fresh (37 minutes old at the recovery API reference clock), so it correctly avoided a duplicate inspection dispatch. This fallback is not native schedule evidence.
- Snapshot \`debug/vps-latest.md\` was generated 2026-11-05 18:22:41Z (2026-11-06 01:22:41 ICT). At this review it is still within the 75-minute fallback budget, but it is not a new live inspection. It recorded node \`tce-k3s-01\` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, about 19 GiB available RAM, and \`restart_required=yes\`. Media/MicroFE/NATS were 1/1; Stock Admin and new Backend were ImagePullBackOff; old Backend and Frontend were 1/1; TCE frontend/service, microfe-auth and Keycloak were 0/0. Treat these as snapshot-time observations only.
- The TCE/Auth public 503 probes and the snapshot's zero-replica workloads are correlated observations, not a proven causal diagnosis. Platform TCE/Auth lane success is a scoped GitOps/runtime check and does not override the independent public HTTP healthcheck failures.
- Stock paired Admin/Backend promotion remains closed until explicit release authorization and protected publisher-run Actions:read provenance are verified. Existing Stock publisher #41563856933 proved ARM64 image builds/digests, but it does not authorize production promotion.
- Authentication #75/#76 remain gated: exact-head checks are historical and Supabase Preview was SKIPPED. The connected integration's Deploy-to-production binding/effect is not authoritatively exposed. Do not merge or run migrations.
- VPS host restart and Docker/containerd maintenance remain pending an approved maintenance window.

### Next dependency-safe actions

1. Keep the existing inspection fallback policy: do not dispatch another read-only inspect while #42083607462 remains within the 75-minute fallback budget; let the recovery controller request one when it becomes stale. Continue reporting native schedule freshness separately.
2. Investigate Platform native schedule delivery without changing cron declarations or adding a second deployment authority.
3. Keep Stock Admin/Backend paired promotion disabled until release authorization and protected publisher provenance are available.
4. Investigate why all four TCE/Auth public probes return HTTP 503; do not weaken the strict health gate or infer root cause from the older snapshot.
5. Keep Auth #75/#76 and Supabase migrations gated on authoritative integration side-effect evidence.
6. Wait for an approved VPS maintenance window before host restart or package upgrade.

### Safety invariants

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- \`reconcile-vps.yml\` remains the sole production apply authority; \`inspect-vps.yml\` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred in this review.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows.
- TCE market-scan schedule unchanged.

## Previous review — 2026-11-06 00:56 ICT (2026-11-05 17:56 UTC)

This review re-read all five default-branch refs, open PRs, latest Actions runs, exact master check-runs, open-PR head check-runs, native schedule history and the current tracker. It supersedes the 00:18 runtime snapshot below.

### Current repository refs and checks

| Repository | Master SHA | Latest master CI / publication evidence |
|---|---|---|
| Platform Infra | `37caf7ea6ec1c4833e22eb8b6ffaf03186fd0023` | PR #1284 merged; exact-head #42074105857 PASS and post-merge validate-manifests #42074228245 PASS (00:23:58 ICT). |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | WF-01 #42053388961 PASS; WF-02 #42053388868 formatting check PASS (auto-format commit step skipped); WF-05 #42053388841 PASS (22:17–22:20 ICT). |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | CI #41563856934 PASS; publisher #41563856933 built/pushed immutable images, but Platform handoff validation and atomic paired promotion were SKIPPED (Nov 3). |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | CI #41617592783 PASS (Nov 3); no newer master run. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | CI #41670642852 PASS; Supabase Preview check SKIPPED (Nov 3). |

### Current open PRs and exact-head checks

- Platform #544 draft, head `c95e7daecb83b65577b54303427fe4ea81adfe06`; validate PASS #38575430454 (Oct 14, historical).
- Platform #541 draft, head `b8f7c6ba04e3d971336a899b2efd5894662083b3`; validate PASS #38567431761 (Oct 14, historical).
- Platform #539 draft, head `2dc48b97017ecb08e49682633303a2f1d5e991a1`; validate PASS #38548718033 (Oct 14, historical).
- Authentication #75 ready, head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; validate PASS #40446492086 (Oct 27), Supabase Preview SKIPPED.
- Authentication #76 draft, head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; validate PASS #41329425940 (Nov 1), Supabase Preview SKIPPED.
- No open PRs in TCE Dashboard, StockDividend or Media Generation. All open-PR PASS checks above are historical; none is fresh validation against a new head.

### Native schedule evidence — keep event types distinct

| Workflow | Latest native `event=schedule` run | Result |
|---|---|---|
| Platform inspect-vps | #42049660972 — 2026-11-05 21:55:03 ICT | PASS, stale |
| Platform reconcile-vps | #42068683835 — 2026-11-05 23:51:03 ICT | FAIL only Stock health |
| Platform recover-stale-ops | #42068414686 — 2026-11-05 23:49:29 ICT | PASS |
| Platform schedule watchdog | #42070623710 — 2026-11-06 00:02:22 ICT | FAIL inspection freshness |
| TCE WF-06 | #42019530614 — 2026-11-05 18:30:38 ICT | FAIL; four strict public probes returned HTTP 503 |
| TCE WF-12 | #42013061466 — 2026-11-05 17:43:23 ICT | FAIL freshness |
| TCE WF-07 | #41982802263 — 2026-11-05 13:47:35 ICT | PASS |

The latest 100 Platform Actions runs contain no newer `event=schedule` inspect-vps run than #42049660972. The watchdog #42070623710 independently passed reconcile freshness (11m) and recovery freshness (12m) but failed inspection freshness (127m). Workflow_run recovery #42070696343 passed at 00:02:49 ICT; it is not a native recovery tick and skipped duplicate inspection because fallback #42063840567 was still fresh at that time. Do not attribute the missing inspect event to runner queue: the previous watchdog evidence reported queue_wait=0m.

### Runtime evidence and release gates

- Latest read-only K3s snapshot remains #42063840567, generated 2026-11-05 23:23:06 ICT by `workflow_dispatch`. At 00:56 ICT it is approximately 93 minutes old, outside the 75-minute fallback freshness budget. No newer inspect-vps snapshot was found in the latest workflow-run view; current live cluster health is therefore unverified.
- At that snapshot, node `tce-k3s-01` was Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB RAM available; GitOps drift clean; host `restart_required=yes`. Media/MicroFE/NATS were 1/1. Stock Admin and new Backend were ImagePullBackOff on `12d63b4`; previous Backend/Frontend were 1/1. TCE/Auth/Keycloak were 0/0. This is historical snapshot evidence only.
- Stock publisher #41563856933 verified immutable linux/arm64 builds and digests, but the handoff validation and atomic paired production dispatch were SKIPPED. Keep Admin/Backend promotion disabled until explicit release authorization and protected publisher-run Actions:read provenance are available.
- TCE PR #1024 recovery contract is merged and its post-merge WF-01/WF-02/WF-05 checks passed. No qualifying post-merge native WF-06/WF-12 failure has exercised WF-13 end-to-end; no fallback dispatch is claimed.
- Authentication #75/#76 remain gated: validate checks are historical, Supabase Preview was SKIPPED, and the Deploy-to-production integration binding/effect is not exposed by the authorized API. Do not merge or run migrations.
- VPS host restart and Docker/containerd maintenance remain pending an approved maintenance window.

### Next dependency-safe actions

1. Let the existing recovery controller obtain a fresh read-only inspect fallback when its native schedule next runs; do not dispatch a duplicate while a run is active or a fallback is fresh. Native schedule freshness must remain separate from workflow_dispatch freshness.
2. Continue monitoring the next native Platform watchdog and recovery ticks; preserve all existing cron declarations.
3. Keep Stock paired promotion closed until release authorization and protected publisher provenance are verified.
4. Verify one qualifying native TCE failure triggers exactly one WF-13 → WF-06 fallback with full source run/SHA correlation.
5. Keep Auth PRs and migrations gated on the Supabase production integration side-effect check.
6. Wait for an approved VPS maintenance window before host restart or package upgrade.

### Safety invariants

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred in this review.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows.
- TCE market-scan schedule unchanged.

## Repository readiness

| Repository | Master SHA | Open PRs | Latest verified CI / publication |
|---|---|---|---|
| phanthienquoc/platform-infra | `b1a0c185e3f9` | #1301 ready; #1296/#544/#541/#539 draft | PR #1301 exact head `dce6ae5341ce` has checks #42145176538/#42145176539/#42145176540 queued; no decommission merge or K3s mutation yet. |
| phanthienquoc/TCE-dashboard | `512b69d837e2` | None | Native WF-06 #42133793538 failed four strict HTTP 200 probes with 503 under the operator zero-replica state; WF-13 fallback #42133822204 PASS/read-only. TCE market-scan schedule unchanged. |
| phanthienquoc/stockdividend | `6fcefa6b3792` | None | PR #32 merged; post-merge CI #42137523269 PASS. No new publisher run or production release after merge; manual hold remains closed. |
| phanthienquoc/media-generation | `3a8846a4f273` | None | PR #72 merged; post-merge CI #42136991059 PASS. No Platform dispatch or production release after merge. |
| phanthienquoc/phanthienquoc-authentication | `f978a3f378ee` | #75 ready; #76 draft | Auth CI #41670642852 PASS (historical); PR checks #40446492086/#41329425940 are historical and Supabase Preview is SKIPPED. Production integration side-effect gate unresolved. |

## Current runtime blockers

- **Stock/Media retirement:** Platform PR #1301 is branch-only; master still owns the prior runtime until the PR is merged and the manual decommission is separately authorized. The latest committed snapshot #42131886966 is stale and omits PVC/PV/StorageClass data. No namespace or runner deletion has occurred.

- **Platform schedule delivery:** Native inspect-vps #42049660972 succeeded at 21:55:03 ICT and remains the latest native inspection; no newer `event=schedule` inspect run appears in the latest 100 Actions runs through 00:18 ICT. Native reconcile #42068683835 at 23:51:03 ICT failed only Stock health. Native recovery #42068414686 at 23:49:29 ICT passed. Watchdog #42070623710 at 00:02:22 ICT failed only inspection freshness: reconcile age 11m and recovery age 12m passed, while native inspection age was 127m. Recovery workflow_run #42070696343 passed but skipped a duplicate inspection because fallback snapshot #42063840567 was 38m old then. The fallback snapshot is about 55m old at 00:18 ICT (within the 75m fallback budget) but is not native schedule evidence.

- **K3s / Stock runtime:** Latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by `workflow_dispatch`. Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB RAM available; GitOps drift clean; host `restart_required=yes`. Media backend/frontend, MicroFE Shell/WS and NATS are 1/1. Stock Admin (two Pods) and new Backend remain ImagePullBackOff on `12d63b4` because the manifest has no matching platform; previous Backend and Frontend remain 1/1 on `23b2878`. TCE/Auth/Keycloak remain 0/0. No host reboot or package upgrade.

- **TCE health/schedule:** Latest native WF-06 #42019530614 (18:30:38 ICT) failed all four strict public probes with HTTP 503. Latest native WF-12 #42013061466 (17:43:23 ICT) failed freshness; WF-07 #41982802263 passed. PR #1024 merged the WF-13 fix: it validates native schedule source via workflow IDs 339198323 (WF-06) and 403352324 (WF-12), deduplicates, and dispatches only the read-only WF-06 fallback. No qualifying post-merge native event has exercised this path. Keep strict HTTP 200 checks and all TCE cron declarations unchanged.

- **Authentication:** Supabase project `gtqovpusfyyvxpeezxlo` reports ACTIVE_HEALTHY / PostgreSQL 17.6.1.084 and FUNCTIONS_DEPLOYED. The remote migration ledger matches all 84 local migration files exactly. PR #75/#76 remain 11 commits behind master; #75 is ready and #76 draft. The owner-provided integration setting still shows Deploy to production ON for Auth master, but the binding/effect is not exposed by the authorized API. Keep both PRs open; do not merge or run migrations.

- **VPS maintenance:** Latest inspection reports host restart required and pending Docker/containerd maintenance. No approved maintenance window is evidenced; do not reboot or upgrade packages.

- **VPS Control MCP:** PR #1268 is merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`; `apps/tce-vps-control-mcp/package-lock.json` is committed (lockfile v3; 94 package entries). PR #1280 is merged as `d4705442de747c80ace35d14f7dee209e25fe6ac` and excludes MCP-only paths from recovery bootstrap. The MCP remains diagnostics-only with no Docker/Kubernetes mutation authority.

- **Stock release authorization:** Immutable ARM64 publisher #41563856933 verified Scraper/Admin/Backend digests, but paired production promotion remains disabled until explicit release authorization and protected publisher-run Actions:read provenance are available.

- **Superseded MCP proposal:** Platform PR #1222 is closed and not merged; it is not an open PR or production authority. The diagnostics-only replacement is #1268.

## Current operational status

- **Platform master:** `37caf7ea6ec1c4833e22eb8b6ffaf03186fd0023`. PR #1284 merged; exact-head validate-manifests #42074105857 and post-merge #42074228245 PASS. PR #1283/#1282/#1281/#1280 and diagnostics-only MCP #1268 are also merged. The latest documentation-only merge did not trigger production apply.
- **Platform native schedules:** inspect-vps #42049660972 (21:55:03 ICT, PASS but stale); reconcile-vps #42068683835 (23:51:03 ICT, Stock health failure); recover-stale-ops #42068414686 (23:49:29 ICT, PASS); watchdog #42070623710 (00:02:22 ICT, FAIL only native inspection freshness). Workflow_run recovery #42070696343 passed and skipped another inspection fallback because #42063840567 was still fresh. Native inspection and fallback freshness remain separate.
- **Fallback and native reconciliation:** Recovery schedule #42068414686 verified fallback reconcile #42068463484 with exact payload `ref=master`, SHA `d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. Fallback #42068463484 and native #42068683835 passed shared preflight, GHCR access and credential bootstrap; GitOps drift was false and production apply/image changes were skipped. TCE/Auth/MicroFE/Media lanes passed; Stock health failed.
- **K3s:** Latest snapshot #42063840567 generated at 23:23:06 ICT by workflow_dispatch; about 55m old at this checkpoint. Node Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM; GitOps drift clean; restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin and new Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1 on `23b2878`; TCE/Auth/Keycloak 0/0. No reboot or host package upgrade.
- **TCE:** master `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; PR #1024 recovery fix merged and post-merge WF-01 #42053388961/WF-02 #42053388868/WF-05 #42053388841 PASS. Latest native WF-06 #42019530614 returned HTTP 503 on all four public endpoints; WF-12 #42013061466 failed freshness; WF-07 #41982802263 PASS. No post-merge native WF-13 E2E dispatch. No TCE schedule changed.
- **StockDividend:** master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; CI #41563856934 and immutable publisher #41563856933 PASS. Publisher built/verified ARM64 manifests for Scraper/Admin/Backend, but Platform handoff validation and atomic paired production promotion were SKIPPED. Production tag `12d63b4` still lacks matching ARM64 manifests; no paired promotion without authorization/provenance.
- **Media Generation:** master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; CI #41617592783 PASS; backend/frontend 1/1 in the 23:23 snapshot.
- **Authentication:** master `f978a3f378ee22d4630909c2d182275b21ac9e9a`; CI #41670642852 PASS. Supabase project ACTIVE_HEALTHY / FUNCTIONS_DEPLOYED; migration set matches 84/84. PR #75/#76 remain open and 11 commits behind master; PR #75 Deploy-to-production side-effect gate remains unresolved.

## Current PR heads and validation

- Platform #1283 merged as `be13f089e665de5ad23df6209c3a0831a6a5e295`; exact-head validate-manifests #42071477343 PASS and post-merge #42071588610 PASS. It updated tracker/inventory/checkpoint only.
- Platform #1282 merged as `6c2b826175d135b41fcb69f28ca2268391c357c2`; exact-head #42069918051 and post-merge #42070150263 PASS.
- Platform #1281 merged as `cd5f9001f826a3a25cf992289176df827ac28c77`; exact-head #42068751747 and post-merge #42068869578 PASS.
- Platform #1280 merged as `d4705442de747c80ace35d14f7dee209e25fe6ac`; exact-head validate-github-actions #42066670909 and validate-manifests #42066667137 PASS; post-merge #42067822505/#42067839646 PASS.
- Platform #1268 merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`; diagnostics-only MCP lockfile committed, no Docker/Kubernetes mutation capability. Platform #544/#541/#539 remain old draft proposals and are not deployment approvals.
- TCE #1024 merged as `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; exact-head WF-05 #42053173288/WF-02 #42053173277 and post-merge WF-01 #42053388961/WF-02 #42053388868/WF-05 #42053388841 passed. No post-merge native WF-13 E2E is evidenced.
- Authentication #75 is ready at `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` (28 ahead/11 behind master); #76 remains draft at `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58` (3 ahead/11 behind). Their latest `validate` checks #40446492086/#41329425940 are historical; Supabase Preview was skipped. Keep both gated on integration side effects and refresh branches conflict-safely before any future merge.
- Current open PRs: Platform #544/#541/#539 (all draft); Authentication #75 (ready)/#76 (draft); no open PRs in TCE, StockDividend or Media Generation.
- StockDividend and Media Generation have no fresh master CI since Nov 3; current runs remain #41563856934/#41563856933 and #41617592783 respectively. Treat them as historical checks, not fresh CI.

## Current actions

1. Poll Platform PR #1301 exact-head checks #42145176538, #42145176539 and #42145176540; fix failures and revalidate the updated head before any merge.
2. Squash-merge #1301 only when all required checks pass on the current head; close the superseded plan-only PR #1296 after the implementation PR is accepted.
3. Before namespace deletion, obtain a fresh same-window inventory of all namespaced resources, PVCs, PVs and StorageClasses; verify backups/external data and independently stop/unregister the dedicated Media runner.
4. After the guarded manual decommission, capture a fresh read-only inspection and verify TCE/Auth/MicroFE/Keycloak remain unchanged.
5. Keep Stock production publication and paired promotion disabled until explicit release authorization and protected publisher provenance are available.
6. Keep Authentication #75/#76 gated on authoritative Supabase production integration side-effect evidence; do not merge or run migrations.
7. Observe TCE WF-06/WF-13 recovery while preserving strict HTTP 200 checks and every TCE schedule, especially the market-scan schedule.
8. Wait for an approved VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

## Ownership and safety invariants

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
- WF-12 remains read-only; isolated WF-13 may only dispatch the public HTTP-only WF-06 healthcheck.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- locally-uncensored-private remains retired.
- No production image promotion, production manifest apply, database migration, desired replica change, host package upgrade, reboot or cron declaration change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

## Checkpoint update — 2026-11-05 07:56 ICT (00:56 UTC)

This update supersedes older status rows above where timestamps differ. Repository refs, open PRs, latest Actions runs, exact-head check-runs, native schedule event history and the current tracker were inspected directly.

### Repository heads, PRs and checks

| Repository | Current master | Open PRs | Latest verified run/check evidence |
|---|---|---|---|
| Platform Infra | `420ff3091867b35772472a1ab54efd74d9e5c255` | #1222, #544, #541, #539 (all draft) | Master `validate-manifests` #41938463049 PASS (push, 07:03:36 ICT). PR #1222 exact-head validate PASS; #544/#541/#539 checks PASS but historical. |
| TCE Dashboard | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Latest schedule WF-07 Backup #41936628258 PASS (06:48:44 ICT); WF-06 #41932031987 FAIL; WF-12 #41928632194 FAIL. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 PASS and immutable publisher #41563856933 PASS (2026-11-03); promotion gate disabled and paired dispatch SKIPPED. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS (2026-11-03); last inspected backend/frontend 1/1, digest-pinned. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS (2026-11-03). #75/#76 validate PASS; both Supabase Preview checks SKIPPED. |

Open PR exact heads:
- Platform #1222 `f018e39eda52770539fc10671fba0d04baec8046`; validate PASS at 2026-11-04T11:30:16Z. Still unsafe: proposed Docker/Kubernetes mutation tools, malformed newline defects, missing SHELL_UID/GID forwarding and no reproducible lockfile/build/test/ShellCheck evidence.
- Platform #544 `c95e7daecb83b65577b54303427fe4ea81adfe06`; validate PASS at 2026-10-14T13:52:17Z; draft.
- Platform #541 `b8f7c6ba04e3d971336a899b2efd5894662083b3`; validate PASS at 2026-10-14T12:54:46Z; draft.
- Platform #539 `2dc48b97017ecb08e49682633303a2f1d5e991a1`; validate PASS at 2026-10-14T10:19:24Z; draft.
- Auth #75 `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; validate PASS at 2026-10-27T03:52:49Z, Supabase Preview SKIPPED.
- Auth #76 `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; validate PASS at 2026-11-01T17:04:06Z, Supabase Preview SKIPPED.

### Native schedule delivery

Filtered Actions history by `event=schedule`; fallback events and reruns are not counted.

| Platform workflow | Latest native schedule run | Result |
|---|---|---|
| inspect-vps | #41934713847, 06:33:56 ICT | PASS; latest native inspection |
| reconcile-vps | #41917440202, 04:35:01 ICT | FAIL; StockDividend health lane |
| recover-stale-ops | #41914511298, 04:16:19 ICT | PASS but stale |
| reconcile-schedule-watchdog | #41918315745, 04:40:44 ICT | FAIL; inspection freshness |

No newer Platform `event=schedule` run was present in Actions history by 07:56 ICT. The latest Platform master push validation #41938463049 is not schedule evidence. Workflow_run recovery #41934894417 succeeded at 06:35:15 ICT, but it is not a native recovery tick. The latest workflow_run watchdog #41934894419 failed recovery freshness.

TCE schedule history:
- WF-07 Backup #41936628258, 06:48:44 ICT: PASS.
- WF-06 #41932031987, 06:13:49 ICT: FAIL; all four strict public checks returned HTTP 503 (TCE web, TCE API, Auth liveness, Auth readiness).
- WF-12 #41928632194, 05:49:42 ICT: FAIL at scheduled WF-06 delivery inspection.
- WF-12 workflow_run #41932063303, 06:14:02 ICT: heartbeat forwarding PASS, but not a native WF-12 schedule event.
- No newer TCE `event=schedule` run was present by 07:56 ICT. Keep strict HTTP 200 and all TCE cron declarations, especially the market-scan schedule, unchanged.

### K3s evidence and age

The latest committed read-only snapshot `debug/vps-latest.md` was generated at 2026-11-04T23:34:04Z (06:34:04 ICT), about 82 minutes old at this checkpoint. It is therefore outside the 75-minute inspection freshness budget and must not be represented as current live health.

At snapshot time:
- Node `tce-k3s-01`: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available RAM about 19 GiB.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1.
- Stock Admin: two Pods 0/1 ImagePullBackOff on `admin:12d63b4`; current Backend replica 0/1 ImagePullBackOff on `backend:12d63b4`; previous Backend and Frontend 1/1 on `23b2878`.
- TCE frontend/service and MicroFE Auth/Keycloak: 0/0. Public Keycloak OIDC probes returned HTTP 503.
- Host `restart_required=yes`; no reboot or package upgrade was performed.

Reconcile #41917440202 confirms shared GHCR credential preflight and GitOps patch operations succeeded without image changes (`ALLOW_IMAGE_CHANGES=false`). The runner helper explicitly classified Stock Admin/Backend `no match for platform in manifest` as permanent and skipped rollout restarts. The Stock health lane correctly failed; no retry churn or false-green status was introduced.

### Release gates and next actions

- StockDividend publisher #41563856933 verified immutable linux/arm64 artifacts, but its production promotion gate is explicitly disabled. Platform handoff validation and atomic Admin/Backend digest dispatch were SKIPPED. Keep promotion disabled until release authorization and protected Actions:read access are verified; do not promote one image independently.
- TCE/Auth remain intentionally 0/0 in the last snapshot. Do not activate workloads or weaken HTTP 200 checks without explicit deployment authorization.
- Auth PRs remain gated because Supabase Preview is SKIPPED and the connected integration target/migration side effect is not authoritatively verified. Do not merge #75/#76 or run migrations on this evidence.
- Keep #1222 draft; it is not a safe alternate deployment authority.
- Next concrete action: verify the enabled state and event delivery for the four Platform scheduled workflows and TCE WF-06/WF-12, then obtain a fresh read-only K3s inspection. Continue Stock paired-release work only after release authorization is available.
- No production manifest, image, credential, database, Pod, replica, host or cron mutation occurred in this checkpoint. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. `locally-uncensored-private` remains retired. TCE market-scan schedule unchanged.

Evidence:
- Platform master validation #41938463049: https://github.com/phanthienquoc/platform-infra/actions/runs/41938463049
- Native Platform inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform reconcile #41917440202: https://github.com/phanthienquoc/platform-infra/actions/runs/41917440202
- Native Platform recovery #41914511298: https://github.com/phanthienquoc/platform-infra/actions/runs/41914511298
- Native Platform watchdog #41918315745: https://github.com/phanthienquoc/platform-infra/actions/runs/41918315745
- TCE WF-06 #41932031987: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987
- TCE WF-12 #41928632194: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194
- TCE WF-07 Backup #41936628258: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment readiness checkpoint — 2026-11-05 09:00 ICT / 02:00 UTC

## Repository state and pull requests

All five default-branch refs, open PRs, latest Actions runs and the current deployment tracker were re-read for this checkpoint.

| Repository | Master SHA | Open PRs | Latest verified CI / run evidence |
|---|---|---|---|
| Platform Infra | `76dad0be9a3aab4130dbd25b7c2c00deb8e24d9e` | #1222, #544, #541, #539 (all draft) | Inspection snapshot PR #1251 exact-head validation #41949516885 PASS; PR #1251 merged. Native recovery #41949145532 PASS; native reconcile #41950932898 FAIL only in Stock health; native watchdog #41951133668 FAIL because native inspection is stale. |
| TCE Dashboard | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Latest native schedule WF-07 Backup #41936628258 PASS at 06:48:44 ICT. WF-06 #41932031987 FAIL at 06:13:49 ICT; WF-12 #41928632194 FAIL at 05:49:42 ICT. No newer TCE schedule run in the inspected Actions history. |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and immutable ARM64 publisher #41563856933 PASS on 2026-11-03. Production promotion remains explicitly disabled; paired handoff/dispatch SKIPPED. |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS on 2026-11-03. Latest snapshot shows backend/frontend 1/1 and digest-pinned. |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS on 2026-11-03. Exact-head PR checks #40446492086/#41329425940 PASS but historical; Supabase Preview remains SKIPPED. |

Open PR exact heads remain unchanged:
- Platform #1222: `f018e39eda52770539fc10671fba0d04baec8046`; last PR validation #41821355040 PASS (historical). Still draft and unsafe: proposed Docker/Kubernetes mutation tools, unresolved shell/newline and UID/GID isolation issues, and no reproducible lockfile/build/test/ShellCheck evidence.
- Platform #544: `c95e7daecb83b65577b54303427fe4ea81adfe06`; #38575430454 PASS (historical, draft).
- Platform #541: `b8f7c6ba04e3d971336a899b2efd5894662083b3`; #38567431761 PASS (historical, draft).
- Platform #539: `2dc48b97017ecb08e49682633303a2f1d5e991a1`; #38548718033 PASS (historical, draft).
- Auth #75: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; #40446492086 PASS (historical, ready).
- Auth #76: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; #41329425940 PASS (historical, draft).

## Platform native schedule evidence

Native schedule events are separated from workflow_dispatch, workflow_run and repository_dispatch. A fallback can refresh a snapshot or run reconciliation, but it cannot satisfy native schedule freshness.

| Workflow | Latest native schedule | Result at 09:00 ICT |
|---|---|---|
| inspect-vps | #41934713847 at 06:33:56 ICT | PASS but stale; no later event=schedule observed |
| recover-stale-ops | #41949145532 at 08:31:53 ICT | PASS |
| reconcile-vps | #41950932898 at 08:47:55 ICT | FAIL in StockDividend health lane |
| reconcile-schedule-watchdog | #41951133668 at 08:49:44 ICT | FAIL because latest native inspect run was 135 minutes old |

Details:
- The scheduled recovery controller #41949145532 successfully detected stale reconciliation and dispatched the existing GitOps authority as workflow_dispatch #41949160533. Payload evidence in its log: `ref=master`, source SHA `bba0cf2e8dafaf312fea45b8c8a9c93d22aa5ec0`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. The fallback is not native schedule evidence.
- Reconcile #41950932898 had no runner queue delay. Shared preflight and reconciliation job succeeded; no manifest drift was detected, so manifest apply and rollout restarts were skipped. Auth runtime Secret provision/verification completed; Auth, TCE, MicroFE and Media health lanes succeeded. Stock health failed on Admin and new Backend ImagePullBackOff. The final lane summary correctly failed.
- The Stock lane log identifies `ghcr.io/phanthienquoc/stockdividend/admin:12d63b4` (two Pods) and `backend:12d63b4` (one Pod) with `no match for platform in manifest`. `ALLOW_IMAGE_CHANGES=false`; no image was promoted and rollout restart was skipped.
- Watchdog #41951133668 verified `inspect-vps` and `reconcile-vps` are active and found no scheduled reconciliation runner queue delay. It accepted native recovery #41949145532 (17 minutes old at watchdog time) but failed native inspection freshness: latest native inspect #41934713847 was 135 minutes old, beyond the 75-minute budget.
- The manual read-only inspection #41949431808 ran at 08:34:27 ICT and generated snapshot at 08:34:36 ICT. Recovery workflow_dispatch #41949390240 completed the fallback path. Inspection PR #1251 merged exact head `e063193f1bdb8383a06ee9af891450753793f313` as master commit `76dad0be9a3aab4130dbd25b7c2c00deb8e24d9e`. This fresh fallback snapshot does not clear the native inspect schedule blocker.
- Recovery workflow_run #41951186498 succeeded and explicitly observed the fresh workflow_dispatch inspection fallback #41949431808 (14 minutes old at its reference time); it did not conflate that fallback with native schedule evidence. Watchdog workflow_run #41951186419 also failed native inspection freshness.

## Latest K3s snapshot

`debug/vps-latest.md` was generated at 2026-11-05T01:34:36Z (08:34:36 ICT), about 26 minutes old at this checkpoint; it is within the 75-minute snapshot freshness budget but is still point-in-time evidence.

- Node `tce-k3s-01`: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available RAM about 19 GiB.
- Media backend/frontend: 1/1. MicroFE Shell/WS and NATS: 1/1.
- Stock Admin: two Pods 0/1 ImagePullBackOff on tag `12d63b4`; new Backend Pod 0/1 ImagePullBackOff on `12d63b4`; previous Backend and Frontend 1/1.
- TCE frontend/service: 0/0. MicroFE Auth and Keycloak: 0/0. Public Keycloak OIDC discovery probes returned HTTP 503.
- Host `restart_required=yes`; Docker/containerd and Ubuntu package upgrades remain pending. No reboot or upgrade was performed.

## TCE, Stock, Media and Auth gates

- TCE WF-06 #41932031987 failed four strict public probes (TCE API, TCE web, Auth liveness and Auth readiness) with HTTP 503 instead of HTTP 200. WF-12 native #41928632194 failed; workflow_run #41932063303 passed heartbeat forwarding only. WF-07 Backup #41936628258 passed. No newer TCE schedule event was present by this checkpoint. Preserve all TCE cron declarations, especially the market-scan schedule; do not weaken HTTP 200.
- Stock publisher #41563856933 published immutable linux/arm64 artifacts for source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`: Scraper `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`; Admin `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`; Backend `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. Publisher gate explicitly disables production promotion; handoff validation and paired Admin/Backend dispatch are SKIPPED. No release authorization is inferred.
- Media CI #41617592783 PASS; snapshot shows both production workloads 1/1 with digest-pinned imageIDs.
- Auth CI #41670642852 PASS. PR #75/#76 checks are historical and Supabase Preview remains SKIPPED; migration provenance and production integration target/effects are unverified. Do not merge on these checks or run migrations.

## Next dependency-safe actions

1. Confirm the next native `inspect-vps` scheduled event. If still absent, investigate GitHub Actions schedule delivery and workflow enabled state; do not count manual fallback as native evidence or change cron without a diagnosed cause.
2. Keep the Stock paired promotion gate closed until explicit release authorization and protected `STOCKDIVIDEND_ACTIONS_READ_TOKEN` access are confirmed. Then promote both Admin and Backend digests atomically through Platform GitOps.
3. Keep TCE/Auth health gates strict and workloads at their last declared 0/0 until activation is explicitly authorized; investigate 503 without manufacturing a green result.
4. Verify Auth Supabase deployment binding and migration provenance before merging #75/#76 or running migrations.
5. Keep #1222 draft until Docker/Kubernetes mutation authority is removed or brought under the single GitOps authority, UID/GID isolation is enforced, and reproducible build/test/lockfile/ShellCheck evidence exists.
6. Wait for a maintenance window before host upgrades or reboot.

## Ownership and safety

- App repositories own tests, builds and immutable GHCR publication.
- Platform Infra owns production manifests, shared GHCR pull credentials, provenance, paired digest promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No direct SSH/Compose/MCP mutation authority was added. `locally-uncensored-private` remains retired.
- The scheduled reconcile executed its Auth runtime Secret provision/verification step, but no manifest drift was found and production manifest apply was skipped. Do not represent this checkpoint as having made zero production-side operations.
- No production image promotion, manifest apply, database migration, Pod/replica change, host reboot or package upgrade was initiated by this documentation update. TCE market-scan schedule unchanged.

## Evidence

- Inspection snapshot PR #1251: https://github.com/phanthienquoc/platform-infra/pull/1251
- Manual read-only inspection #41949431808: https://github.com/phanthienquoc/platform-infra/actions/runs/41949431808
- Inspection exact-head validation #41949516885: https://github.com/phanthienquoc/platform-infra/actions/runs/41949516885
- Native recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Recovery reconciliation fallback #41949160533: https://github.com/phanthienquoc/platform-infra/actions/runs/41949160533
- Native reconciliation #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Watchdog workflow_run #41951186419: https://github.com/phanthienquoc/platform-infra/actions/runs/41951186419
- Recovery workflow_run #41951186498: https://github.com/phanthienquoc/platform-infra/actions/runs/41951186498
- Native TCE WF-07 Backup #41936628258: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41936628258
- Native TCE WF-06 #41932031987: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932031987
- Native TCE WF-12 #41928632194: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41928632194
- TCE workflow_run heartbeat forwarding #41932063303: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41932063303
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


## Live checkpoint — 2026-11-05 10:04 ICT / 03:04 UTC

### Exact repository and workflow evidence

- Platform Infra master is 8ae797a0bd69be772a590515d73dfce0e45a820e (commit #1253, generated by inspection automation at 02:57:53Z). Latest read-only inspection #41958436222 ran by workflow_dispatch at 02:56:44Z and succeeded; validation #41958510609 completed successfully at 02:57:28Z. These are not native schedule events.
- Platform Infra open PRs: #1222, #544, #541, #539; all remain draft. PR #1222 head f018e39eda52770539fc10671fba0d04baec8046; its only returned check validate #41821355040 is historical PASS, but its Docker/Kubernetes mutation scope, shell isolation and reproducible build/test gaps remain release blockers.
- TCE master 52cecd5584e6c0a3daf0e2bcff6c89ca064e203d; no open PRs. WF-12 native #41958165099 ran at 02:54:09Z and failed freshness. Its log verifies WF-06 is active, but latest WF-06 scheduled run #41932031987 is 23:13:49Z (220 minutes old at watchdog time). WF-06 source cron remains */15 * * * *; latest known public smoke failed four strict HTTP 200 checks with HTTP 503. WF-12 heartbeat forwarding succeeded; that does not make the schedule check pass.
- StockDividend master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; no open PRs. CI #41563856934 and publisher #41563856933 succeeded. Production paired promotion remains disabled; current Admin and Backend tag 12d63b4 has no ARM64 manifest. No image or manifest change is authorized.
- Media master e4c7d8990aafc7d837e918c9caf39722d623de7c; no open PRs. CI #41617592783 succeeded; snapshot imageIDs are digest-pinned.
- Authentication master f978a3f378ee22d4630909c2d182275b21ac9e9a; PR #75 is ready, #76 draft. Their latest returned validate checks passed, but Supabase Preview checks were SKIPPED. No migration or production activation is authorized.

### Native schedule delivery (only event=schedule counts)

| Workflow | Latest verified native run | Result and interpretation |
|---|---|---|
| Platform inspect-vps | #41934713847 at 2026-11-04 23:33:56Z | PASS, but stale. Manual inspection #41958436222 at 02:56:44Z succeeded and produced the current snapshot; it is not native schedule evidence. |
| Platform reconcile-vps | #41950932898 at 2026-11-05 01:47:55Z | FAIL only in Stock health. Manual reconcile #41958192072 at 02:54:23Z also failed Stock health; the health log confirms no match for platform in manifest for Admin/Backend tag 12d63b4. |
| Platform recover-stale-ops | #41949145532 at 2026-11-05 01:31:53Z | PASS. Manual recovery #41958394974 at 02:56:20Z succeeded after the manual reconcile failure; it is not native schedule evidence. |
| Platform reconcile-schedule-watchdog | #41951133668 at 2026-11-05 01:49:44Z | FAIL: native inspection freshness exceeded 75 minutes. Its recovery freshness step passed against #41949145532. |
| TCE WF-06 | #41932031987 at 2026-11-04 23:13:49Z | FAIL on public endpoint HTTP 503; at WF-12 run #41958165099 it was 220m old, beyond the 25m schedule freshness budget. Workflow-enabled check passed (state=active). |
| TCE WF-12 | #41958165099 at 2026-11-05 02:54:09Z | FAIL on stale WF-06 schedule delivery. Authenticated heartbeat dispatch succeeded but is not a substitute for WF-06 native delivery. |
| TCE WF-07 Backup | #41936628258 at 2026-11-04 23:48:44Z | PASS; separate from WF-07 third-party integration and from WF-06 service health. |

### Latest K3s snapshot

- debug/vps-latest.md generated at 2026-11-05T02:56:52Z (09:56:52 ICT) by manual inspection #41958436222; PR #1253 committed it at Platform master 8ae797a0bd69be772a590515d73dfce0e45a820e. At this checkpoint the snapshot is about 8 minutes old, inside the 75-minute freshness budget.
- Node tce-k3s-01: Ready, ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56%; available memory about 19 GiB.
- Media backend/frontend, MicroFE Shell/WS and NATS are 1/1 and digest-pinned. Stock Admin (two Pods) and new Backend remain ImagePullBackOff on 12d63b4; old Backend and Frontend are 1/1. TCE/Auth/Keycloak desired replicas remain 0/0. Public Keycloak OIDC remains HTTP 503.
- Host restart_required=yes; Docker/containerd/Ubuntu upgrades remain pending. No reboot or package upgrade.

### Safety and next actions

1. Confirm native schedule event delivery for inspect, reconcile, recovery, watchdog and TCE WF-06/WF-12 independently; do not count manual, workflow_run or repository_dispatch events.
2. Keep Stock promotion disabled until explicit release authorization and protected StockDividend Actions:read provenance access are confirmed; preserve atomic Admin/Backend digest pairing.
3. Keep strict HTTP 200 gates and TCE/Auth 0/0 desired state unchanged until a separately authorized service activation.
4. Keep Auth Supabase migration provenance/target review as a pre-merge gate.
5. Obtain a maintenance window before host package upgrades/reboot.

No production image, manifest, credential, database, Pod, replica or host mutation was performed. reconcile-vps.yml remains the sole production apply authority; app repos own build/test/immutable GHCR; Platform Infra owns GitOps, pull credentials, promotion and rollout. Preserve useful CI, security, backup, manual and scheduled workflows. No cron expression was changed; the TCE market-scan schedule is unchanged.


## Audit correction — production-side effects of reconcile run #41958192072 (2026-11-05 10:10 ICT)

The prior 10:04 checkpoint incorrectly described the reconcile run as having no credential mutation. The run was a workflow_dispatch with mode=apply, target_app=all and ALLOW_IMAGE_CHANGES=false. Its job-step API records the following successful steps:

- Validate GHCR pull access before mutating cluster credentials.
- Provision Auth runtime Secret from the platform-infra production Environment.
- Bootstrap shared GHCR pull credentials.
- Execute the managed image-pull-blocked workload restart policy.
- Verify cluster after reconciliation.

The shared preflight reported DRIFT=false; Apply production manifests and post-apply drift verification were skipped. Therefore, this run did perform controlled production credential reconciliation (Auth runtime Secret and shared GHCR pull Secret), despite making no production manifest/image-reference change. The Stock lane still failed: Admin and new Backend remained ImagePullBackOff on tag 12d63b4 because the ARM64 manifest is absent. The run did not establish Stock recovery or a healthy overall deployment.

Do not describe this reconcile as zero production-side operations. The evidence does not show a database migration, image digest promotion, manifest apply, desired replica change or host reboot. The workflow-step summary shows the managed restart step completed, but this audit does not infer that every blocked Pod was restarted; the subsequent inspection still shows the Stock Admin/Backend failures.



## Live checkpoint — 2026-11-05 11:04 ICT / 04:04 UTC

### Repository and PR state

- Platform Infra master: `c0d5c5ff18472800f15b352cd950c4c3d959cd1f`. Open PRs #1222, #544, #541 and #539 remain draft. Exact PR-head workflow runs returned: #1222 validate-manifests #41821355040 PASS; #544 #38575430454 PASS; #541 #38567431761 PASS; #539 #38548718033 PASS. These are historical checks. #1222 remains blocked by Docker/Kubernetes mutation scope, shell UID/GID isolation, newline defects and missing reproducible build/test/lockfile/ShellCheck evidence.
- TCE Dashboard master: `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`; no open PRs.
- StockDividend master: `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; no open PRs.
- Media Generation master: `e4c7d8990aafc7d837e918c9caf39722d623de7c`; no open PRs.
- Authentication master: `f978a3f378ee22d4630909c2d182275b21ac9e9a`; PR #75 ready and #76 draft. Their exact-head Auth CI runs #40446492086 and #41329425940 passed historically. Supabase Preview remains SKIPPED; #75 remains blocked by unknown Supabase deployment binding/migration side effect, and #76 remains draft.

### Latest Platform workflow and native schedule evidence

- Manual reconcile #41962132547 ran at 2026-11-05 03:31:30Z (10:31:30 ICT), event=workflow_dispatch, ref=master, mode=apply, target_app=all, ALLOW_IMAGE_CHANGES=false. Shared reconciliation and preflight succeeded; no GitOps manifest drift was found, so production manifest apply and post-apply drift verification were skipped.
- The same reconcile completed controlled production credential work: GHCR pull access validation, Auth runtime Secret provisioning/verification, shared GHCR pull credential bootstrap and the managed image-pull restart policy. The restart policy explicitly skipped Stock Admin and Backend because their errors are permanent `no match for platform in manifest`; no rollout restart was performed for those two workloads. No image digest promotion, manifest apply, database migration, replica change or host reboot is evidenced.
- Stock health lane and final deployment gate failed correctly. Media, MicroFE, TCE internal workload and Auth lanes passed their configured checks; Keycloak lane was skipped.
- Manual recovery #41962345391 at 10:33 ICT succeeded. It found the prior manual inspection fallback #41958436222 still fresh (about 35 minutes old), avoided a duplicate inspection dispatch, and explicitly retained the native inspection schedule as stale. This is workflow_dispatch, not native schedule evidence.
- Latest native Platform schedule events remain: inspect-vps #41934713847 (06:33:56 ICT, success but stale); reconcile-vps #41950932898 (08:47:55 ICT, failure in Stock health); recovery #41949145532 (08:31:53 ICT, success); watchdog #41951133668 (08:49:44 ICT, failure on native inspection freshness). No later `event=schedule` run was returned through 11:04 ICT. Workflow_dispatch, workflow_run and repository_dispatch fallbacks do not satisfy native cadence.
- Reconcile #41962132547's live cluster listing at 10:32 ICT: node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Media backend/frontend, MicroFE Shell/WS and NATS 1/1; two Stock Admin Pods and the new Stock Backend Pod ImagePullBackOff; previous Stock Backend and Stock Frontend 1/1. No TCE/Auth Pods appeared in the live Pod listing; the latest committed inspection still records their desired workloads at 0/0.
- The latest committed read-only snapshot remains #41958436222 at 09:56:52 ICT. It is about 68 minutes old at this checkpoint and approaching the 75-minute freshness budget. Host restart_required=yes; no package upgrade or reboot.

### TCE schedule and endpoint evidence

- Native WF-06 #41962074678 ran at 10:30:58 ICT (event=schedule) and failed all four strict public HTTP 200 probes: TCE API `https://tce.mrcute.space/api/health`, TCE web `https://tce.mrcute.space/`, Auth liveness `https://auth.mrcute.space/api/health`, and Auth readiness `https://auth.mrcute.space/api/ready` each returned HTTP 503.
- WF-12 workflow_run #41962097006 ran at 10:31:50 ICT and passed its schedule-delivery check. Its job log confirms WF-06 is active and a recent scheduled WF-06 run exists. This establishes that WF-06 native schedule delivery resumed at 10:30; it does not establish endpoint health or a native WF-12 schedule event.
- Latest native WF-12 scheduled run remains #41958165099 at 09:54:09 ICT (failure on then-stale WF-06 delivery). WF-07 Backup #41936628258 at 06:48:44 ICT remains PASS.
- Preserve strict HTTP 200 and do not change TCE cron declarations or market-scan schedule.

### App publication and release gates

- Stock CI #41563856934 and immutable ARM64 publisher #41563856933 remain the latest successful Stock runs (2026-11-03). Publisher produced full-source-SHA-tagged Scraper/Admin/Backend ARM64 artifacts and registry digests; production paired Admin/Backend promotion remains explicitly disabled and handoff/dispatch remain SKIPPED. Production tags `12d63b4` still lack an ARM64 manifest. No release authorization is inferred.
- Media CI #41617592783 PASS (2026-11-03); live reconcile listing confirms both production workloads 1/1 with digest-pinned images.
- Auth CI #41670642852 PASS (2026-11-03); no Supabase Preview evidence or migration authorization.

### Next dependency-safe actions

1. Obtain a fresh read-only inspection before the 75-minute freshness budget expires, while separately continuing to require a new native `event=schedule` inspection run. Do not count the manual fallback as native delivery.
2. Investigate Platform scheduled-event delivery after 08:49 ICT. Prior watchdog logs confirmed inspect-vps and reconcile-vps were active and no runner queue delay was detected; no evidence justifies changing cron expressions.
3. Keep Stock paired promotion disabled until explicit release authorization and protected StockDividend Actions:read provenance access are confirmed. Promote Admin and Backend only as one atomic digest-pinned release.
4. Keep TCE/Auth public HTTP 200 gates strict and desired replicas at 0/0 until separately authorized activation. WF-06 schedule delivery is fresh again; public endpoints remain unhealthy.
5. Keep Auth #75/#76 behind Supabase binding and migration-provenance review. Keep Platform #1222 draft until the mutation boundary and reproducible security/build checks are resolved.
6. Wait for a VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

### Evidence

- Platform master: https://github.com/phanthienquoc/platform-infra/commit/c0d5c5ff18472800f15b352cd950c4c3d959cd1f
- Manual reconcile #41962132547: https://github.com/phanthienquoc/platform-infra/actions/runs/41962132547
- Manual recovery #41962345391: https://github.com/phanthienquoc/platform-infra/actions/runs/41962345391
- Native Platform inspection #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform reconcile #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native Platform recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Native Platform watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Native TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 workflow_run #41962097006: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962097006
- Native TCE WF-12 #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852

No cron expression, production manifest, image reference, database, desired replica, host package or reboot setting was changed by this checkpoint. TCE market-scan schedule remains unchanged.


# Cross-repo deployment checkpoint — 2026-11-05 11:58 ICT / 04:58 UTC

## Repository state and PRs

| Repository | Current master | Open PRs | Latest relevant Actions evidence |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `afb49ba5dcc95f273b940463fe4cdd8d92001bd2` | #1222, #544, #541, #539 (all draft) | PR #1256 merged; exact-head validation #41965908624 PASS; post-merge `validate-manifests` #41965978011 PASS. |
| `phanthienquoc/TCE-dashboard` | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | Native WF-06 #41962074678 (10:30:58 ICT) delivered but failed all four public HTTP 200 probes with 503. WF-12 workflow_run #41962097006 PASS; latest native WF-12 #41958165099 (09:54 ICT) failed freshness. |
| `phanthienquoc/stockdividend` | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and immutable publisher #41563856933 PASS (Nov 3); paired production promotion remains disabled and un-dispatched. |
| `phanthienquoc/media-generation` | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS (Nov 3); last live reconcile listing #41962132547 showed backend/frontend 1/1. |
| `phanthienquoc/phanthienquoc-authentication` | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | Master CI #41670642852 PASS (Nov 3); PR #75/#76 CI passed historically; Supabase Preview remains SKIPPED. |

Platform open PR heads were re-read:
- #1222 draft: `f018e39eda52770539fc10671fba0d04baec8046`; exact-head validation #41821355040 PASS (historical). Keep blocked on mutation authority, shell UID/GID enforcement, newline defects and reproducible lockfile/build/test/ShellCheck evidence.
- #544 draft: `c95e7daecb83b65577b54303427fe4ea81adfe06`; #38575430454 PASS (historical).
- #541 draft: `b8f7c6ba04e3d971336a899b2efd5894662083b3`; #38567431761 PASS (historical).
- #539 draft: `2dc48b97017ecb08e49682633303a2f1d5e991a1`; #38548718033 PASS (historical).
- Authentication #75 ready: `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`; #40446492086 PASS (historical).
- Authentication #76 draft: `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`; #41329425940 PASS (historical).

## Platform Infra schedule and deployment evidence

The latest native `event=schedule` runs returned by GitHub Actions are unchanged from the 11:04 checkpoint:

| Workflow | Latest native scheduled run | Result at run time |
|---|---|---|
| `inspect-vps.yml` | #41934713847, 06:33:56 ICT | PASS; now stale |
| `recover-stale-ops.yml` | #41949145532, 08:31:53 ICT | PASS |
| `reconcile-vps.yml` | #41950932898, 08:47:55 ICT | Shared reconcile passed; Stock health lane failed |
| `reconcile-schedule-watchdog.yml` | #41951133668, 08:49:44 ICT | FAIL: no native inspection run within 75 minutes |

At 11:58 ICT these native events are approximately 325m, 206m, 190m and 188m old respectively. No newer Platform `event=schedule` run was returned. The watchdog's inspection-delivery step failed on inspection freshness; the step checks workflow state before freshness, so the failure was not reported as a disabled `inspect-vps` workflow. Do not infer why GitHub stopped delivering the scheduled event.

Latest Platform master validation after PR #1256:
- Exact-head #41965908624: PASS.
- PR #1256 merged as `afb49ba5dcc95f273b940463fe4cdd8d92001bd2`.
- Post-merge `validate-manifests` #41965978011: PASS.
- PR #1256: https://github.com/phanthienquoc/platform-infra/pull/1256

Latest operational reconcile evidence remains manual dispatch #41962132547 (10:31 ICT), not a native schedule. Its shared preflight, GHCR access validation, Auth runtime Secret provisioning, shared GHCR pull credential bootstrap and managed restart-policy steps succeeded. GitOps drift was false, so production manifest apply was skipped. Stock Admin and new Backend were classified as permanent architecture mismatches and were not restarted; Stock health and final deployment gate failed. Manual recovery #41962345391 (10:33 ICT) passed but did not constitute native cron evidence.

## TCE schedule and health

- WF-06 native schedule #41962074678 at 10:30:58 ICT is the latest scheduled run. Its four public probes all returned HTTP 503: TCE web, TCE API, Auth liveness and Auth readiness.
- WF-12 workflow_run #41962097006 passed after WF-06, but it is a workflow_run event, not native WF-12 cron evidence.
- Latest native WF-12 remains #41958165099 at 09:54:09 ICT, failed because WF-06 schedule delivery was stale at that time.
- WF-07 Backup #41936628258 at 06:48:44 ICT remains the latest returned successful native backup run.
- At 11:58 ICT WF-06's last native run is about 87 minutes old and WF-12's last native run about 124 minutes old. Keep strict HTTP 200 and schedule-freshness checks. Do not change any TCE cron declaration or the market-scan schedule.

## K3s and app release gates

The committed `debug/vps-latest.md` snapshot was generated at 2026-11-05T02:56:52Z (09:56:52 ICT), so it is about 122 minutes old at this checkpoint and is not current live-health evidence. It records:
- Node `tce-k3s-01` Ready / ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2.
- Disk 56%; available RAM about 19 GiB; `restart_required=yes`.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin (two Pods) and new Backend 0/1 ImagePullBackOff; old Backend and Frontend 1/1.
- TCE/Auth/Keycloak desired state 0/0; public Keycloak endpoints HTTP 503.

The last live cluster listing in reconcile #41962132547 at 10:32 ICT corroborated the Stock ImagePullBackOff and Media/MicroFE/NATS 1/1 states, but is now about 86 minutes old. No fresh K3s inspection was available in the current Actions history.

- **StockDividend:** successful publisher #41563856933 verified immutable ARM64 artifacts for Scraper/Admin/Backend, but production Admin/Backend still reference tag `12d63b4` without an ARM64 manifest. Production paired handoff/dispatch are SKIPPED. Keep promotion disabled until explicit release authorization and protected Actions:read provenance access are confirmed; never promote only one of Admin/Backend.
- **Media Generation:** latest CI #41617592783 PASS; last live reconcile showed backend/frontend 1/1 with digest-pinned images.
- **Authentication:** latest master CI #41670642852 PASS; #75/#76 remain gated on Supabase deployment binding and migration provenance. No Preview or migration authorization is evidenced.

## Exact next actions

1. Obtain a fresh read-only K3s inspection and separately restore/verify native `inspect-vps` schedule delivery. The current connected GitHub operations expose read/search and PR writes but no workflow-dispatch action; no manual inspection dispatch was initiated in this run.
2. Investigate GitHub scheduled-event delivery for Platform inspect/reconcile/recovery/watchdog and TCE WF-06/WF-12. Preserve cron expressions; do not count manual, workflow_run or repository_dispatch as native schedule evidence.
3. Keep Stock Admin/Backend promotion disabled until explicit authorization and paired immutable digest provenance are available.
4. Keep TCE/Auth public HTTP 200 gates strict and desired replicas 0/0 until separately authorized activation.
5. Keep Auth #75/#76 behind Supabase binding and migration-provenance review; keep Platform #1222 draft.
6. Wait for an approved VPS maintenance window before package upgrades or reboot.

No production manifest/image promotion, database migration, desired replica change, host package upgrade, reboot or cron change was performed by this documentation checkpoint. The earlier reconcile #41962132547 did perform controlled Auth runtime Secret and shared GHCR credential reconciliation; it must not be described as read-only. `reconcile-vps.yml` remains the sole production apply authority; app repositories own tests/builds/immutable GHCR; Platform Infra owns manifests, shared pull credentials, promotion, reconciliation, rollout and health verification. Preserve useful CI/security/backup/manual/release/scheduled workflows and do not introduce direct SSH/Compose/MCP mutation authority. The TCE market-scan schedule remains unchanged.

### Evidence

- PR #1256: https://github.com/phanthienquoc/platform-infra/pull/1256
- Exact-head validation #41965908624: https://github.com/phanthienquoc/platform-infra/actions/runs/41965908624
- Post-merge validation #41965978011: https://github.com/phanthienquoc/platform-infra/actions/runs/41965978011
- Native Platform inspect #41934713847: https://github.com/phanthienquoc/platform-infra/actions/runs/41934713847
- Native Platform recovery #41949145532: https://github.com/phanthienquoc/platform-infra/actions/runs/41949145532
- Native Platform reconcile #41950932898: https://github.com/phanthienquoc/platform-infra/actions/runs/41950932898
- Native Platform watchdog #41951133668: https://github.com/phanthienquoc/platform-infra/actions/runs/41951133668
- Manual Platform reconcile #41962132547: https://github.com/phanthienquoc/platform-infra/actions/runs/41962132547
- Manual Platform recovery #41962345391: https://github.com/phanthienquoc/platform-infra/actions/runs/41962345391
- Native TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 workflow_run #41962097006: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962097006
- Native TCE WF-12 #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment checkpoint — 2026-11-05 15:01 ICT / 08:01 UTC

## Repository heads, open PRs and latest Actions evidence

| Repository | Current master | Open PRs | Latest verified evidence |
|---|---|---|---|
| `phanthienquoc/platform-infra` | `543dc4c4cca08ae7261f9d53aabaf5df6d39bb3a` | #1222, #544, #541, #539 (all draft) | Post-merge `validate-manifests` #41984819070 PASS after PR #1260; latest native inspection #41980605875 PASS at 13:28 but now stale; manual reconcile #41980764155 failed Stock health. |
| `phanthienquoc/TCE-dashboard` | `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d` | None | WF-07 native schedule #41982802263 PASS; WF-12 workflow_run #41982820872 failed WF-06 freshness but heartbeat dispatch returned HTTP 204; latest WF-06 native #41962074678 failed all four public HTTP 200 probes with 503. |
| `phanthienquoc/stockdividend` | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None | CI #41563856934 and publisher #41563856933 PASS; publisher log verifies Scraper/Admin/Backend linux/arm64 digests. Production promotion gate and paired dispatch were explicitly skipped. |
| `phanthienquoc/media-generation` | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None | CI #41617592783 PASS; latest K3s snapshot at 13:28 shows backend/frontend 1/1 and digest-pinned, but snapshot is stale at this checkpoint. |
| `phanthienquoc/phanthienquoc-authentication` | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft | CI #41670642852 PASS; Supabase GitHub integration is owner-reported as deploy-to-production ON and migration state remains unresolved, so #75/#76 remain gated. |

### Open PR heads and latest exact-head checks

- Platform #1222 draft, head `f018e39eda52770539fc10671fba0d04baec8046`: #41821355040 PASS (historical); keep draft because Docker/Kubernetes mutation scope, shell UID/GID isolation and reproducible build/test/lockfile/ShellCheck evidence remain unresolved.
- Platform #544 draft, head `c95e7daecb83b65577b54303427fe4ea81adfe06`: #38575430454 PASS (historical).
- Platform #541 draft, head `b8f7c6ba04e3d971336a899b2efd5894662083b3`: #38567431761 PASS (historical).
- Platform #539 draft, head `2dc48b97017ecb08e49682633303a2f1d5e991a1`: #38548718033 PASS (historical).
- Authentication #75 ready, head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05`: #40446492086 PASS (historical); no merge because the connected Supabase GitHub integration is configured to deploy to production and the migration state/binding is not reconciled.
- Authentication #76 draft, head `f19cacb0bf2b454b3152bd3a501f6f88d0a14a58`: #41329425940 PASS (historical); planning is not migration authorization.

## Platform native schedule and recovery evidence

Filtered Actions history by `event=schedule`; workflow_dispatch, workflow_run and repository_dispatch events are not counted as native cron delivery.

| Workflow | Latest native schedule | Result |
|---|---|---|
| `inspect-vps.yml` | #41980605875, 13:28:06 ICT | PASS; generated snapshot at 13:28:14 ICT. At 15:01 it is about 93 minutes old, beyond the 75-minute freshness budget. |
| `reconcile-vps.yml` | #41950932898, 08:47:55 ICT | FAIL in Stock health; about 373 minutes old. |
| `recover-stale-ops.yml` | #41949145532, 08:31:53 ICT | PASS at run time; about 389 minutes old, beyond the 45-minute budget. |
| `reconcile-schedule-watchdog.yml` | #41951133668, 08:49:44 ICT | FAIL at run time; about 371 minutes old. |

The later workflow_run watchdog #41980748672 at 13:29:27 ICT confirms:
- `reconcile-vps` workflow enabled check PASS.
- Native reconciliation #41950932898 was 281 minutes old at watchdog reference time; the watchdog correctly failed the 45-minute freshness gate.
- Native inspection #41980605875 was 1 minute old and its runner queue wait was 0 minutes.
- Native recovery #41949145532 was 297 minutes old and failed the 45-minute freshness gate.
- No reconciliation deployment-lane queue exceeded the 15-minute budget.

This evidence points to missing/stale scheduled event delivery, not a disabled reconcile workflow or a self-hosted runner queue delay. Do not change cron expressions to hide the gap.

## TCE schedule and public health

- WF-06 latest native schedule #41962074678 at 10:30:58 ICT; all four endpoints failed strict HTTP 200 checks with HTTP 503: TCE web, TCE API, Auth liveness and Auth readiness.
- WF-12 latest native schedule #41958165099 at 09:54:09 ICT; it failed WF-06 freshness.
- WF-07 native schedule #41982802263 at 13:47:35 ICT passed Binance Testnet public/private checks; order integration was skipped by design.
- WF-12 workflow_run #41982820872 at 13:47:46 ICT failed because the latest native WF-06 was 196 minutes old against a 25-minute budget. Its independent Platform heartbeat job succeeded with HTTP 204 and carried source workflow path `.github/workflows/wf-07-tce-integration-check.yml`, source run #41982802263 attempt 1, TCE master SHA `52cecd5584e6c0a3daf0e2bcff6c89ca064e203d`, and heartbeat run #41982820872 attempt 1.
- Platform recovery #41982836006 (repository_dispatch) accepted that heartbeat and succeeded. It is fallback coordination, not native Platform recovery schedule evidence.
- Keep strict HTTP 200 and the existing 25-minute freshness gate. Do not change any TCE cron declaration or the market-scan schedule.

## K3s snapshot and operational reconciliation

Snapshot `debug/vps-latest.md` generated at `2026-11-05T06:28:14Z` / 13:28:14 ICT; approximately 93 minutes old at this checkpoint and therefore stale for the 75-minute inspection budget.

At snapshot time:
- Node `tce-k3s-01`: Ready / ARM64; K3s `v1.36.3+k3s1`; containerd `2.3.2-k3s2`.
- Disk 56%; available RAM about 19 GiB; Docker 29.1.3; host `restart_required=yes`.
- Media backend/frontend, MicroFE Shell/WS and NATS: 1/1 with digest-pinned images.
- Stock Admin: two Pods 0/1 ImagePullBackOff on `admin:12d63b4`; new Backend Pod 0/1 ImagePullBackOff on `backend:12d63b4`; previous Backend and Frontend remain 1/1 on older `23b2878` images.
- The failed Stock images have no resolved digest; containerd reports `no match for platform in manifest`.
- TCE frontend/service and MicroFE Auth/Keycloak remain desired 0/0. Public OIDC probes returned HTTP 503.

Manual reconcile #41980764155 (13:29:35 ICT) used `mode=apply`, `target_app=all`, `ALLOW_IMAGE_CHANGES=false`:
- GHCR access preflight, Auth runtime Secret provisioning, shared GHCR pull credential bootstrap and managed image-pull restart policy succeeded.
- Media, MicroFE, TCE and Auth lanes passed; Keycloak lane was skipped.
- Stock health failed; final deployment gate failed.
- Production manifest apply and image changes were skipped; no image promotion or manifest apply is evidenced.
- This was controlled credential reconciliation, not a read-only run.

## Immutable Stock publication evidence

Stock publisher #41563856933 (master SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`) completed successfully on a native ARM64 runner. The publisher log explicitly verified the full-source-SHA tags with linux/arm64 support and immutable registry digests:

| Component | Immutable tag | Verified digest |
|---|---|---|
| Scraper | `sha-50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | `sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2` |
| Admin | `sha-50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | `sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e` |
| Backend | `sha-50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | `sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a` |

The same run explicitly reported production GitOps promotion disabled; the Platform handoff validation and atomic digest dispatch jobs were skipped. Therefore the current production `12d63b4` mismatch is a stale/unpromoted production reference, not evidence that the new publisher failed. Keep paired Admin/Backend promotion disabled until explicit release authorization and protected source-run Actions:read provenance are available.

## Exact next actions

1. Obtain a fresh read-only K3s inspection; the 13:28 snapshot is now stale. Verify the next native Platform schedule slots (inspection 15:02, reconcile 15:07, recovery 15:10, watchdog 15:12 ICT) without changing cron expressions. If native delivery is still absent, use only the existing recovery/inspection fallback authority when its policy allows; never count fallback as native schedule evidence.
2. Keep Stock paired Admin/Backend promotion disabled until explicit production release authorization and protected publisher-run Actions:read access are confirmed. The current full-SHA ARM64 digests are available but are not promotion authorization.
3. Keep TCE/Auth desired replicas 0/0 and strict HTTP 200 gates; investigate the missing WF-06 native delivery and 503 endpoints without activating workloads.
4. Keep Auth #75/#76 gated until Supabase production integration side effects and migration provenance are authoritatively reconciled.
5. Keep Platform MCP PR #1222 draft until mutation authority, shell UID/GID isolation and reproducible build/test/security evidence are complete.
6. Wait for an approved VPS maintenance window before Docker/containerd/Ubuntu package upgrades or reboot.

## Ownership and safety contract

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, production manifest apply, database migration, desired replica change, host package upgrade, reboot or cron expression change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

### Evidence

- Platform master/post-merge validation #41984819070: https://github.com/phanthienquoc/platform-infra/actions/runs/41984819070
- PR #1260: https://github.com/phanthienquoc/platform-infra/pull/1260
- Native Platform inspection #41980605875: https://github.com/phanthienquoc/platform-infra/actions/runs/41980605875
- Platform watchdog workflow_run #41980748672: https://github.com/phanthienquoc/platform-infra/actions/runs/41980748672
- Manual Platform reconcile #41980764155: https://github.com/phanthienquoc/platform-infra/actions/runs/41980764155
- TCE WF-06 #41962074678: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41962074678
- TCE WF-12 native #41958165099: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41958165099
- TCE WF-07 #41982802263: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41982802263
- TCE WF-12 workflow_run #41982820872: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/41982820872
- Platform heartbeat recovery #41982836006: https://github.com/phanthienquoc/platform-infra/actions/runs/41982836006
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock immutable publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Authentication CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment checkpoint — 2026-11-05 19:56 ICT / 12:56 UTC

## Repository heads and open PRs

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | 9c931c51e51ddc4ae3f55e3a4f3c266122d86f55 | #1268 draft; #544/#541/#539 draft |
| TCE Dashboard | a7b26b21782e4031364a9559b6eefdc2e654cc1e | None |
| StockDividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None |
| Media Generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft |

Platform PR #1222 is closed and not merged. It is not an active open PR. The diagnostics-only proposal currently under review is PR #1268.

## Platform Infra

- Master commit `9c931c51e51ddc4ae3f55e3a4f3c266122d86f55`; master validate-manifests #42030024927 completed PASS.
- PR #1268 exact head `81dfa692dc4a0b363314da72cac6700f1d7f514f`, branch `security/vps-mcp-readonly-boundary-20261105-1855-ict`.
- Exact-head validate-github-actions #42030355670, validate-manifests #42030355586 and dedicated MCP validation #42030355637 all completed PASS.
- Dedicated MCP job #127254938646 ran: generate lockfile, install exact lockfile dependencies with `npm ci`, security contract tests, typecheck, build, shell syntax and ShellCheck; every step passed.
- Artifact #13416365990 was downloaded. Artifact ZIP SHA-256: `243c49c8dacd401f777a666803f05981373a555a40544497a6cdd7119e3a0933`. Extracted package-lock SHA-256: `105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0`.
- Lockfile validation: lockfileVersion 3; 94 package entries including root; exact root dependencies and devDependencies match package.json; all 93 dependency entries have integrity hashes; all resolved tarballs use HTTPS registry.npmjs.org. The lockfile is still not committed on the PR branch, so PR #1268 remains draft.
- No production deployment or host mutation was attempted.

## Native schedule evidence and K3s

An explicit Actions API query filtered to `event=schedule` returned the following latest Platform runs:

| Workflow | Run | Local time | Result |
|---|---:|---:|---|
| inspect-vps | #41980605875 | 13:28:06 | PASS, stale |
| reconcile-vps | #41995809261 | 15:36:40 | FAIL, Stock health |
| recover-stale-ops | #41994805588 | 15:29:01 | PASS, stale |
| schedule watchdog | #41997764646 | 15:51:58 | FAIL, inspection freshness |

No newer native Platform schedule events were returned at 19:56 ICT. Manual recovery/inspection runs remain distinct from native schedule evidence.

Latest K3s snapshot is fallback #42013436672, generated at 17:46:16 ICT. It is about 130 minutes old and exceeds the 75-minute freshness budget. At snapshot time: node Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; about 19 GiB RAM available; host restart_required=yes. Media/MicroFE/NATS 1/1. Stock Admin and new Backend ImagePullBackOff on 12d63b4; previous Backend/Frontend 1/1. TCE/Auth/Keycloak 0/0. This is historical evidence, not current health.

## TCE schedule and public health

- Latest native WF-06 #42019530614 at 18:30:38 ICT failed all four strict public probes with HTTP 503: TCE web, TCE API, Auth readiness and Auth liveness.
- Latest native WF-12 #42013061466 at 17:43:23 ICT failed freshness.
- WF-12 workflow_run #42019562593 completed successfully after WF-06, but WF-13 #42019590810 was correctly skipped because its source event was `workflow_run`, not `schedule`.
- No qualifying native WF-12 event has exercised WF-13 end-to-end. Keep HTTP 200 and 25-minute freshness gates. No cron declaration or market-scan schedule changed.

## Stock, Media and Authentication

- Stock CI #41563856934 and publisher #41563856933 passed on master `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`. Publisher verified immutable linux/arm64 full-source-SHA digests: Scraper `6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2`, Admin `a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e`, Backend `cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a`. Production paired promotion remains disabled pending authorization and protected publisher provenance.
- Media CI #41617592783 passed on master `e4c7d8990aafc7d837e918c9caf39722d623de7c`; runtime 1/1 evidence is only from the stale 17:46 snapshot.
- Authentication CI #41670642852 passed on master `f978a3f378ee22d4630909c2d182275b21ac9e9a`. PR #75/#76 remain gated by Supabase production binding and migration provenance.

## Exact next actions

1. Commit the reviewed lockfile to PR #1268's dedicated branch and rerun exact-head checks; keep draft until complete.
2. Obtain a fresh read-only K3s snapshot through the existing inspection authority when authorized Actions dispatch access is available.
3. Observe a qualifying native WF-12 schedule failure and verify one correlated WF-13 to WF-06 fallback dispatch.
4. Keep Stock paired promotion, Auth migration and TCE/Auth replica activation blocked pending their separate authorizations.
5. Investigate the four TCE HTTP 503 probes without weakening gates.
6. Wait for approved VPS maintenance before reboot or package upgrades.

## Safety invariants

- App repositories own tests, builds, immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve useful CI, tests, security, backup, manual, release and scheduled workflows unless redundancy/obsolescence is proven.
- Do not create a second direct SSH/Compose or MCP Docker/Kubernetes mutation authority.
- `locally-uncensored-private` remains retired.
- No production image promotion, manifest apply, database migration, desired replica change, host package upgrade, reboot or cron expression change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

## Evidence

- Platform master validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030024927
- PR #1268: https://github.com/phanthienquoc/platform-infra/pull/1268
- PR #1268 GitHub Actions validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030355670
- PR #1268 manifest validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030355586
- PR #1268 MCP validation: https://github.com/phanthienquoc/platform-infra/actions/runs/42030355637
- TCE WF-06: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019530614
- TCE WF-12 native: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42013061466
- TCE WF-13 skipped: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019590810
- Stock CI: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock immutable publisher: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Authentication CI: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852


# Cross-repo deployment checkpoint — 2026-11-05 20:59 ICT / 13:59 UTC

## Repository heads and open PRs

| Repository | Master SHA | Open PRs |
|---|---|---|
| Platform Infra | 30db773980223132997a3e98c9703c4e2d90c70a | #1268 draft; #544/#541/#539 draft |
| TCE Dashboard | a7b26b21782e4031364a9559b6eefdc2e654cc1e | None |
| StockDividend | 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec | None |
| Media Generation | e4c7d8990aafc7d837e918c9caf39722d623de7c | None |
| Authentication | f978a3f378ee22d4630909c2d182275b21ac9e9a | #75 ready; #76 draft |

PR state was read from the current GitHub open-PR collections. Platform #1222 remains closed/unmerged and is not counted as open.

## Latest workflow and exact-head evidence

- Platform master validate-manifests #42032333095 completed successfully on master 30db773980223132997a3e98c9703c4e2d90c70a.
- Platform PR #1268 current head is 81dfa692dc4a0b363314da72cac6700f1d7f514f. Exact-head validate-github-actions #42030355670, validate-manifests #42030355586 and dedicated MCP validation #42030355637 all passed. The reviewed lockfile artifact #13416365990 remains absent from the PR branch; the PR stays draft.
- TCE latest native WF-06 schedule #42019530614 (18:30:38 ICT) failed all four public HTTP 200 probes. Latest native WF-12 schedule #42013061466 (17:43:23 ICT) failed freshness. WF-12 workflow_run #42019562593 completed successfully after WF-06; WF-13 #42019590810 was correctly skipped because its source event was workflow_run, not schedule. No qualifying WF-13 native-schedule recovery dispatch is evidenced.
- StockDividend CI #41563856934 and immutable publisher #41563856933 passed on master 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec.
- Media CI #41617592783 passed on master e4c7d8990aafc7d837e918c9caf39722d623de7c; runtime evidence remains stale.
- Authentication CI #41670642852 passed on master f978a3f378ee22d4630909c2d182275b21ac9e9a. Auth PR #75 exact-head run #40446492086 passed on head a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05; this does not clear its external Supabase deployment side-effect gate.

## Deployment authority audit

Reviewed the active application publisher/release workflows and Platform promotion/apply workflows:

| Repository | Workflow | Responsibility | Direct production mutation |
|---|---|---|---|
| TCE Dashboard | wf-03-tce-production-deploy.yml | Manual build, immutable image publication, release request to Platform Infra | None found in this publisher path |
| StockDividend | deploy.yml | Master publication and optional manual release request; production promotion explicitly disabled | None found in this publisher path |
| Media Generation | wf-03-media-production-deploy.yml | Manual build, immutable image publication, release request to Platform Infra | None found in this publisher path |
| Authentication | release.yml | Manual immutable image publication and digest handoff to Platform Infra | None found in this publisher path |
| Platform Infra | gitops-image-promotion.yml | Verify source provenance/digests, update digest-pinned GitOps manifests and await master convergence | GitOps promotion only |
| Platform Infra | reconcile-vps.yml | Apply production manifests, reconcile credentials, verify rollout and health | Sole production apply authority |

No second direct SSH/Compose or application-owned kubectl apply authority was found in the reviewed publisher paths. Keep manual/release workflows: they are purposeful app-owned publishers, not duplicate deployers.

## Native schedules and runtime freshness

The explicit Platform Actions query filtered to event=schedule still returns these latest runs:

| Workflow | Latest native run | Result |
|---|---|---|
| inspect-vps | #41980605875 — 13:28:06 ICT | PASS, stale |
| reconcile-vps | #41995809261 — 15:36:40 ICT | FAIL, Stock health |
| recover-stale-ops | #41994805588 — 15:29:01 ICT | PASS, stale |
| schedule watchdog | #41997764646 — 15:51:58 ICT | FAIL, inspection freshness |

No later native Platform schedule runs were returned at this checkpoint. Do not count workflow_dispatch or workflow_run fallbacks as native schedule evidence.

Latest K3s evidence remains fallback snapshot #42013436672 generated at 17:46:16 ICT, now more than three hours old and beyond the 75-minute freshness budget. Historical snapshot: node Ready/ARM64, disk 56%, about 19 GiB available RAM, Media/MicroFE/NATS 1/1, Stock Admin and new Backend ImagePullBackOff on 12d63b4, previous Backend/Frontend 1/1, TCE/Auth/Keycloak 0/0, host restart required. This is not current health evidence.

## Release and safety gates

- Stock publisher #41563856933 verified immutable linux/arm64 full-source-SHA digests: Scraper sha256:6b3ee2676268baf8ae2e77f68df3b730d797ea6192541710720d04585e99f8a2, Admin sha256:a5c2dbb1a0b6c417891e18256fd4c00a6e14e53a4c34939c12fc1e43c7f3339e, Backend sha256:cb0135fc57bc8a2514288105ab35cc59f4cb922555f028dbf97f44c077b76a9a. Production paired promotion remains disabled pending explicit authorization and protected publisher-run Actions:read provenance.
- Auth PR #75 remains open even though its exact-head CI passed. Owner-provided Supabase evidence says GitHub integration Deploy to production is ON for master; the 2026-11-02 read-only ledger check found 84 local/remote migration versions matching, but the historical failed deployment state and exact merge-triggered side effect remain unresolved. Do not merge or dispatch release workflows.
- Platform MCP PR #1268 remains draft. Lockfile artifact ZIP SHA-256 243c49c8dacd401f777a666803f05981373a555a40544497a6cdd7119e3a0933; extracted lockfile SHA-256 105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0; lockfile v3, 94 package entries, 93 dependency entries with integrity and HTTPS npm registry URLs. It is verified but not committed.
- No production image promotion, manifest apply, database migration, desired replica change, host maintenance, reboot or cron expression change occurred.
- reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only.
- TCE market-scan schedule remains unchanged.

## Exact next actions

1. Commit the reviewed MCP lockfile to PR #1268's dedicated branch and rerun all exact-head checks; keep draft until then.
2. Obtain a fresh read-only K3s inspection through the existing Platform inspection authority when dispatch access is available.
3. Observe a qualifying native WF-12 schedule failure and verify exactly one correlated WF-13 → WF-06 fallback dispatch.
4. Keep Stock paired promotion, Auth migration/release, and TCE/Auth replica activation blocked until their separate provenance/authorization gates are satisfied.
5. Investigate TCE's four HTTP 503 probes without weakening strict HTTP 200 or freshness gates.
6. Wait for an approved VPS maintenance window before reboot or package upgrades.

## Evidence

- Platform master validation #42032333095: https://github.com/phanthienquoc/platform-infra/actions/runs/42032333095
- Platform PR #1268: https://github.com/phanthienquoc/platform-infra/pull/1268
- Platform PR #1268 exact-head checks: #42030355670, #42030355586, #42030355637
- TCE WF-06 #42019530614: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019530614
- TCE WF-12 native #42013061466: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42013061466
- TCE WF-12 workflow_run #42019562593: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019562593
- TCE WF-13 skipped #42019590810: https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42019590810
- Stock CI #41563856934: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856934
- Stock publisher #41563856933: https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933
- Media CI #41617592783: https://github.com/phanthienquoc/media-generation/actions/runs/41617592783
- Auth master CI #41670642852: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41670642852
- Auth PR #75 exact-head CI #40446492086: https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/40446492086


# Cross-repo deployment checkpoint — 2026-11-05 23:30 ICT / 16:30 UTC

## Repository heads and open PRs

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `a239187b7694a02dedb2b7ade6b31e0be139ac44` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra changes merged

- PR #1268 merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`. It adds the optional diagnostics-only VPS MCP with committed lockfile and read-only GitOps-subordinate permissions. Exact-head checks #42063067665, #42063067491 and #42063067460 passed; post-merge checks #42063703576, #42063703585 and #42063703609 passed.
- PR #1276 merged as `22a8d4f0807f41f26ed1cba6ebcd96e3afc662fa` after inspection #42063840567. This records a fresh read-only snapshot generated at 23:23:06 ICT.
- PR #1278 merged as `a239187b7694a02dedb2b7ade6b31e0be139ac44`. It excludes `apps/tce-vps-control-mcp/**` from `reconcile-vps.yml` push paths and explicitly treats MCP paths as non-production in the push-scope resolver. Exact-head checks #42064383310, #42064383238 and #42064383170 passed; post-merge checks #42064588984, #42064588923 and #42064588960 passed on current master.
- PRs #1275 and #1277 were closed unmerged after their branches became stale/diverged from master; their evidence is superseded by this checkpoint and the merged #1278 fix.

## Reconcile failure and recovery evidence

- The MCP merge initially triggered `Reconcile VPS — push-auto` run #42063703873 because the old path filter included all `apps/**`.
- The run failed closed at `Resolve push deployment scope` with: `Unclassified production-trigger path 'apps/tce-vps-control-mcp/.env.example'; refusing broad push reconciliation.`
- All credential bootstrap, restart, Auth secret provisioning, manifest apply and rollout steps were skipped. No production mutation occurred.
- Recovery controller #42063793863 completed successfully and dispatched read-only inspection #42063840567 (`workflow_dispatch`), which passed. This is a manual/fallback inspection, not a native schedule tick.
- After #1278 merged, master validation #42064588984/#42064588923/#42064588960 all passed. No `reconcile-vps.yml` run was triggered by the #1278 merge itself; the workflow and resolver path filters now keep the diagnostics-only MCP out of production deployment scope.
- The resolver still rejects unclassified paths and now tests both MCP-only (no production scope) and mixed TCE+MCP (TCE-only scope) changes.

## Current K3s evidence

Latest snapshot in `debug/vps-latest.md` was generated at 23:23:06 ICT by inspection #42063840567 (workflow_dispatch), not by a native schedule.

- K3s node `tce-k3s-01`: Ready / ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3.
- Disk 56%; about 19 GiB RAM available; GitOps drift status clean.
- Media backend/frontend, MicroFE Shell/WS and NATS are 1/1 Running.
- Stock Admin (two Pods) and new Stock Backend remain ImagePullBackOff on `12d63b4` with `no match for platform in manifest`; old Backend and Frontend remain 1/1 on `23b2878`.
- TCE frontend/service and Auth/Keycloak remain 0/0. Do not activate them without separate approval.
- Host reports `restart_required=yes`. No host restart or package upgrade was performed.

This snapshot is fresh operational evidence, but it does not replace native schedule evidence.

## Native schedule history

Latest native Platform schedule runs remain:
- inspect-vps #42049660972 — PASS at 21:55:03 ICT (older than the 23:23 fallback snapshot).
- reconcile-vps #41995809261 — FAIL (Stock health).
- recover-stale-ops #41994805588 — PASS but stale.
- schedule watchdog #41997764646 — FAIL freshness.

Latest native TCE schedule runs remain:
- WF-06 #42019530614 — FAIL at 18:30:38 ICT, four public HTTP 200 probes failed.
- WF-12 #42013061466 — FAIL freshness at 17:43:23 ICT.
- WF-13 #42019590810 was skipped because its source was a non-native `workflow_run` event. No post-merge native WF-13 → WF-06 E2E recovery has been evidenced.
- TCE post-merge WF-01 #42053388961, WF-02 #42053388868 and WF-05 #42053388841 all passed.

Do not count workflow_dispatch/workflow_run fallback as native schedule delivery.

## Application release state

- **TCE:** master `c5415f8ac0aa`; build/format/unit tests pass. Public health still fails while TCE workloads are 0/0. Keep strict HTTP 200 gates; do not activate workloads or alter any TCE cron.
- **StockDividend:** master `50ba0dfb67eb`; CI #41563856934 and immutable ARM64 publisher #41563856933 pass. Three component digests remain verified, but paired production promotion is blocked on explicit release authorization and protected publisher provenance. Production tag `12d63b4` has no matching ARM64 manifest.
- **Media:** master `e4c7d8990aaf`; CI #41617592783 passes; backend/frontend 1/1 in the latest snapshot.
- **Authentication:** master `f978a3f378ee`; CI #41670642852 passes. PR #75/#76 remain gated on Supabase production binding and migration provenance.

## MCP lockfile and authority

- PR #1268 committed `apps/tce-vps-control-mcp/package-lock.json` (blob `e768247f2394a203c917edd81d39343ee55a896d`), lockfile v3, 94 entries including root, 93 dependencies with integrity and HTTPS npm registry URLs. SHA-256: `105eb616f8319e0c1d3234429434d35828c750f29a595395aace0f03e6b6e2c0`.
- Dedicated validation uses `npm ci` against the committed lockfile, Node 22, security tests, typecheck, build and ShellCheck. Workflow permissions are read-only and checkout credentials are disabled.
- MCP only exposes diagnostics; no Docker restart, Kubernetes mutation, SSH or Compose deployment authority. `reconcile-vps.yml` remains the sole production apply authority.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health.
- No production image promotion, manifest apply, database migration, desired replica change, host reboot/package upgrade or cron expression change occurred in this checkpoint.
- TCE market-scan schedule remains unchanged.

## Exact next actions

1. Observe the next native Platform schedule tick; do not substitute the 23:23 workflow_dispatch inspection.
2. Repair native recovery/watchdog delivery while preserving the existing schedule expressions.
3. Observe a qualifying native TCE WF-06/WF-12 failure and verify exactly one correlated WF-13 → WF-06 fallback.
4. Keep Stock paired promotion blocked until explicit release authorization and protected publisher provenance are available.
5. Keep Auth PR #75/#76 gated until Supabase deployment side effects and migration provenance are resolved.
6. Wait for an approved maintenance window before host restart or package upgrades.


# Cross-repo deployment checkpoint — 2026-11-05 23:44 ICT / 16:44 UTC

## Repository heads and open PRs

All five default-branch refs, open PRs, latest Actions runs/checks, native schedule history and the deployment tracker were re-read.

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `d4705442de747c80ace35d14f7dee209e25fe6ac` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra — PR #1280 merged

PR [#1280](https://github.com/phanthienquoc/platform-infra/pull/1280) was merged with squash after re-reading the exact PR head `7618eb7f243ad7e67b667c0d11fa06a09044024a`, confirming the PR was open/non-draft/mergeable, confirming it was 2 commits ahead and 0 behind current master, and verifying both exact-head checks passed.

- Merge SHA: `d4705442de747c80ace35d14f7dee209e25fe6ac`.
- Exact-head validate-github-actions [#42066670909](https://github.com/phanthienquoc/platform-infra/actions/runs/42066670909): PASS.
- Exact-head validate-manifests [#42066667137](https://github.com/phanthienquoc/platform-infra/actions/runs/42066667137): PASS.
- Post-merge validate-github-actions [#42067822505](https://github.com/phanthienquoc/platform-infra/actions/runs/42067822505): PASS.
- Post-merge validate-manifests [#42067839646](https://github.com/phanthienquoc/platform-infra/actions/runs/42067839646): PASS.

The change excludes `apps/tce-vps-control-mcp/**` from the recovery controller's production bootstrap push paths and extends `validate-workflow-contracts.py` to enforce the exclusion in both recovery and reconciliation filters. Resolver regression assertions cover MCP-only changes as no production scope and mixed TCE+MCP changes as TCE-only scope. The existing `reconcile-vps.yml` remains the only production apply authority. No schedule expression changed, and the TCE market-scan schedule is untouched.

## Post-merge and runtime evidence

- Latest Platform master validation runs on merge SHA d470544: #42067822505 and #42067839646 both PASS. No reconcile-vps or production mutation run was triggered by this docs-independent recovery-filter fix.
- Platform #1268 had already merged as `29e26d829d4f02d44be2747a411a8c68d4ff48db`; its diagnostics-only MCP package-lock is committed. #1280 closes the follow-on recovery push-filter gap discovered when the MCP-only merge triggered recovery bootstrap.
- Latest native Platform schedules returned by explicit `event=schedule` query: inspect-vps #42049660972 PASS at 21:55:03 ICT; reconcile-vps #41995809261 FAIL at 15:36:40 ICT on Stock health; recover-stale-ops #41994805588 PASS at 15:29:01 ICT but stale; watchdog #41997764646 FAIL at 15:51:58 ICT on freshness. No newer native schedule events were returned.
- Latest native TCE schedules: WF-06 #42019530614 FAIL at 18:30:38 ICT (four public HTTP 503 probes); WF-12 #42013061466 FAIL at 17:43:23 ICT; WF-07 #41982802263 PASS at 13:47:35 ICT. No later native schedule events were returned. WF-13's post-merge E2E dispatch remains unproven.
- Latest read-only K3s snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch, not native schedule. Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM available; GitOps drift clean; host restart_required=yes. Media backend/frontend, MicroFE Shell/WS and NATS 1/1. Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due no matching platform manifest; old Backend/Frontend 1/1 on `23b2878`. TCE/Auth/Keycloak 0/0.
- Stock publisher #41563856933 on master built/pushed Scraper, Admin and Backend on a native ARM64 runner and verified immutable manifests successfully. Its explicit production promotion gate passed only as a guard; Platform handoff validation and atomic paired digest dispatch were SKIPPED. No release authorization/protected provenance handoff is evidenced, so do not promote.
- Media CI #41617592783 PASS; the 23:23 snapshot showed backend/frontend 1/1. Authentication master CI #41670642852 PASS. PR #75 current head `a8e8a1d99e86a679b8d2ea7c7e7fa91302ffcc05` has historical validate PASS #40446492086 (2026-10-27) and Supabase Preview SKIPPED; PR body still reports Deploy to production ON and unresolved merge-triggered migration effects. PR #76 remains draft with historical validate #41329425940 PASS and Preview SKIPPED.
- TCE master `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c`; PR #1024 recovery fix and WF-01/WF-02/WF-05 post-merge checks remain PASS. No qualifying post-merge native schedule event has exercised WF-13.

## Next dependency-safe actions

1. Continue observing native Platform schedule delivery; use the existing read-only inspection path for a fresh K3s snapshot, and keep schedule/manual/fallback evidence distinct.
2. Verify one qualifying native TCE WF-06/WF-12 failure causes exactly one WF-13 → WF-06 fallback with full source run and SHA correlation.
3. Keep Stock paired Admin/Backend promotion disabled until explicit release authorization and protected publisher-run Actions:read provenance are verified.
4. Keep Auth #75/#76 gated until the actual Supabase production integration binding and migration side effects are authoritatively verified.
5. Wait for an approved VPS maintenance window before host restart or Docker/containerd/Ubuntu upgrades.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, paired promotion, GitOps reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No duplicate SSH/Compose/MCP Docker/Kubernetes mutation authority was added.
- No production image, manifest, database, desired replica, host package, reboot or cron mutation occurred.
- Useful CI/security/backup/manual/release/scheduled workflows remain preserved.
- TCE market-scan schedule unchanged.


# Cross-repo deployment checkpoint — 2026-11-05 23:53 ICT / 16:53 UTC

## Repository heads and PRs

All five default-branch refs, open PRs, latest Actions runs/checks, deployment tracker and native schedule history were re-read.

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `cd5f9001f826a3a25cf992289176df827ac28c77` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra PR #1281 merged

- PR [#1281](https://github.com/phanthienquoc/platform-infra/pull/1281) merged with squash as `cd5f9001f826a3a25cf992289176df827ac28c77`.
- Exact-head validate-manifests [#42068751747](https://github.com/phanthienquoc/platform-infra/actions/runs/42068751747) PASS.
- Post-merge validate-manifests [#42068869578](https://github.com/phanthienquoc/platform-infra/actions/runs/42068869578) PASS.
- The merge updated only the deployment tracker, workflow inventory and checkpoint. No production manifest or runtime resource changed.

## New native schedule and dispatch evidence

- Native recover-stale-ops [#42068414686](https://github.com/phanthienquoc/platform-infra/actions/runs/42068414686) completed PASS at 23:49:29 ICT.
- Its job log proves it detected master reconciliation #42063703873 at age 27m and dispatched the existing `reconcile-vps.yml` authority with exact payload: `ref=master`, `sha=d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. It correlated fallback run [#42068463484](https://github.com/phanthienquoc/platform-infra/actions/runs/42068463484). This is a workflow_dispatch fallback initiated by a native recovery tick, not a native reconciliation tick.
- Fallback reconcile #42068463484 passed shared preflight, GHCR access and credential bootstrap; GitOps drift was false, so production manifest apply and image changes were skipped. TCE, Auth, MicroFE and Media lanes passed; Stock health failed on two Admin Pods and the new Backend Pod in ImagePullBackOff.
- Native scheduled reconcile [#42068683835](https://github.com/phanthienquoc/platform-infra/actions/runs/42068683835) started at 23:51:03 ICT and completed FAILURE only because the StockDividend lane failed. Shared reconciliation/preflight passed, drift was false and production apply was skipped. TCE/Auth/MicroFE/Media lanes passed their scoped checks.
- Watchdog [#42068511916](https://github.com/phanthienquoc/platform-infra/actions/runs/42068511916) ran at 23:50:05 ICT after the native recovery tick but before #42068683835 started. It failed because the latest native reconcile then was #41995809261 at age 493m and latest native inspect #42049660972 at age 115m. It did verify recovery #42068414686 PASS. The later #42068683835 run post-dates the watchdog and cannot retroactively make that watchdog green.
- Recovery controller [#42068810024](https://github.com/phanthienquoc/platform-infra/actions/runs/42068810024) completed PASS after fallback reconcile #42068463484 and correctly skipped another inspection dispatch because the latest read-only snapshot was still within the 75-minute freshness budget.

## K3s and application state

Latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch, not native schedule. It is about 30 minutes old at this checkpoint.

- Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM available; GitOps drift clean; restart_required=yes.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` because the registry manifest has no matching platform; old Backend and Frontend 1/1 on `23b2878`.
- TCE/Auth/Keycloak remain 0/0. The successful TCE/Auth reconciliation-lane checks are not evidence that the four public WF-06 HTTP endpoints are healthy.
- Latest native TCE WF-06 remains #42019530614 (HTTP 503 on all four probes); latest native WF-12 remains #42013061466 (freshness failure); WF-07 #41982802263 passed. No post-merge WF-13 native E2E dispatch is evidenced.
- Stock immutable publisher #41563856933 passed ARM64 build/push and manifest verification for Scraper/Admin/Backend, but Platform handoff and atomic paired production promotion were SKIPPED. No explicit release authorization or protected publisher Actions:read provenance is available; do not promote.
- Media CI #41617592783 PASS; snapshot showed backend/frontend 1/1. Auth CI #41670642852 PASS; PR #75/#76 remain gated on Supabase Deploy to production binding and migration provenance.

## Next actions

1. Observe the next native inspect-vps tick; current recovery schedule is delivering, but native inspection remains stale.
2. Check the next watchdog after #42068683835; reconcile freshness should now be based on the new native schedule, but inspect freshness remains unresolved.
3. Keep Stock paired Admin/Backend promotion closed until explicit authorization and protected publisher provenance.
4. Verify a qualifying native TCE failure triggers exactly one WF-13 → WF-06 fallback with full source run/SHA correlation.
5. Keep Auth PRs and migrations blocked until Supabase integration side effects are authoritatively known.
6. Wait for an approved host maintenance window.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns manifests, shared GHCR pull credentials, provenance/digest checks, paired promotion, reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No production image/manifest/database/replica/host/cron mutation occurred. No reboot or package upgrade.
- No duplicate SSH/Compose/MCP mutation authority.
- TCE market-scan schedule unchanged.


# Cross-repo deployment checkpoint — 2026-11-06 00:03 ICT / 2026-11-05 17:03 UTC

## Repository heads and PRs

All five default-branch refs, open PRs, latest Actions runs/checks, deployment tracker, explicit native schedule history and read-only Supabase migration state were re-read.

| Repository | Default branch SHA | Open PRs |
|---|---|---|
| Platform Infra | `6c2b826175d135b41fcb69f28ca2268391c357c2` | #544/#541/#539 draft |
| TCE Dashboard | `c5415f8ac0aa1ffa0b17c18d1b05952c68f9f65c` | None |
| StockDividend | `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec` | None |
| Media Generation | `e4c7d8990aafc7d837e918c9caf39722d623de7c` | None |
| Authentication | `f978a3f378ee22d4630909c2d182275b21ac9e9a` | #75 ready; #76 draft |

## Platform Infra PR #1282 merged

- PR [#1282](https://github.com/phanthienquoc/platform-infra/pull/1282) merged with squash as `6c2b826175d135b41fcb69f28ca2268391c357c2`.
- Exact-head validate-manifests [#42069918051](https://github.com/phanthienquoc/platform-infra/actions/runs/42069918051) PASS.
- Post-merge validate-manifests [#42070150263](https://github.com/phanthienquoc/platform-infra/actions/runs/42070150263) PASS.
- The PR changed only tracker/inventory/checkpoint documentation. No production manifest or runtime resource changed.

## Native schedule evidence after PR #1282

- Native recover-stale-ops #42068414686 PASS at 23:49:29 ICT. It dispatched fallback reconcile #42068463484 with exact payload `ref=master`, SHA `d4705442de747c80ace35d14f7dee209e25fe6ac`, `mode=apply`, `allow_image_changes=false`, `target_app=all`.
- Native reconcile #42068683835 at 23:51:03 ICT completed FAILURE only on Stock health. Shared preflight passed, drift was false, production apply/image changes were skipped; TCE/Auth/MicroFE/Media lanes passed their scoped checks.
- Native watchdog [#42070623710](https://github.com/phanthienquoc/platform-infra/actions/runs/42070623710) ran at 00:02:22 ICT and failed only native inspect freshness. It passed native reconcile #42068683835 at age 11m (freshness pass despite Stock health conclusion=FAIL) and native recovery #42068414686 at age 12m (PASS). It failed because native inspect-vps #42049660972 at 21:55:03 ICT was 127m old.
- Recovery controller [#42070696343](https://github.com/phanthienquoc/platform-infra/actions/runs/42070696343) completed PASS after the watchdog. It confirmed the latest workflow_dispatch inspection fallback #42063840567 was 38m old and correctly avoided a duplicate read-only inspection. This fallback does not satisfy native schedule freshness.
- Latest native inspect-vps remains #42049660972 at 21:55:03 ICT; no later `event=schedule` inspect run was returned. The workflow is active (watchdog passed its enabled-state check); event delivery is still missing, not a runner queue failure.

## K3s and app runtime

Latest read-only snapshot #42063840567 was generated at 23:23:06 ICT by workflow_dispatch, not native schedule. It is about 40m old at this checkpoint and within the 75-minute fallback freshness budget.

- Node `tce-k3s-01` Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; Docker 29.1.3; disk 56%; ~19 GiB RAM available; GitOps drift clean; restart_required=yes.
- Media backend/frontend, MicroFE Shell/WS and NATS 1/1.
- Stock Admin (two Pods) and new Backend ImagePullBackOff on `12d63b4` due no matching platform manifest; old Backend/Frontend 1/1 on `23b2878`.
- TCE/Auth/Keycloak remain 0/0. The TCE/Auth reconciliation lane success is not evidence that the public WF-06 HTTP endpoints are healthy.
- Latest native TCE WF-06 #42019530614 failed all four public HTTP probes with 503; latest native WF-12 #42013061466 failed freshness; WF-07 #41982802263 passed. No post-merge WF-13 native E2E dispatch is evidenced.
- Stock immutable publisher #41563856933 passed ARM64 build/push and manifest verification for Scraper/Admin/Backend, but Platform handoff and atomic paired production promotion were SKIPPED. No explicit release authorization or protected publisher Actions:read provenance is available; do not promote.
- Media CI #41617592783 PASS; snapshot showed backend/frontend 1/1. Auth CI #41670642852 PASS.

## Authentication — fresh read-only migration verification

Using the connected Supabase read-only API and GitHub recursive Git tree for Authentication master:

- Project `gtqovpusfyyvxpeezxlo`: `ACTIVE_HEALTHY`, PostgreSQL 17.6.1.084, ap-southeast-1.
- Its only listed default branch `main` / Git `master` reports `FUNCTIONS_DEPLOYED` (not the earlier historical `MIGRATIONS_FAILED` status).
- Authentication master `f978a3f378ee22d4630909c2d182275b21ac9e9a` has 84 SQL migration files; remote ledger has 84 rows; exact version/name set match 84/84, zero local-only, zero remote-only, zero duplicate prefixes.
- PR #75 changes exactly five files: three Markdown planning/task files and two tests. No `supabase/**`, runtime or workflow files. PR #75 is 28 commits ahead/11 behind master; #76 is 3 ahead/11 behind.
- Owner-provided GitHub Integration screenshot still reports Deploy to production ON for Auth repository `master`; the connected integration target/effect is not exposed by the authorized Supabase API. Keep #75/#76 open; do not merge until this external side-effect gate is authoritatively cleared. A fresh read-only evidence comment was added to PR #75 (#6664113606). No Supabase writes or migration actions occurred.

## Next actions

1. Observe the next native inspect-vps tick; keep workflow_dispatch fallback freshness separate from native schedule evidence.
2. Re-check the next watchdog; it should continue to pass reconcile/recovery freshness while failing inspection until a native inspect run arrives.
3. Keep Stock paired Admin/Backend promotion closed until explicit authorization and protected publisher provenance.
4. Verify a qualifying native TCE failure triggers exactly one WF-13 → WF-06 fallback with source-run/SHA correlation.
5. Keep Auth PRs gated on Supabase integration side effects; exact migration set alignment is now verified, but PRs are stale by 11 commits and require conflict-aware refresh before any future merge.
6. Wait for an approved host maintenance window.

## Safety

- App repos own tests/builds/immutable GHCR publication and source-run/tag/digest provenance.
- Platform Infra owns manifests, shared GHCR pull credentials, provenance/digest checks, paired promotion, reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- No production image/manifest/database/replica/host/cron mutation occurred. No reboot or package upgrade.
- No duplicate SSH/Compose/MCP mutation authority.
- TCE market-scan schedule unchanged.


## Cross-repo deployment checkpoint — 2026-11-06 06:04 ICT / 2026-11-05 23:04 UTC

- **Live repository heads:** Platform Infra `20af8c89bc2230ff6eb78a58f2066301f75a27a7`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; Media Generation `e4c7d8990aafc7d837e918c9caf39722d623de7c`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #544/#541/#539 (draft); Auth #75 (ready)/#76 (draft); none in TCE, StockDividend or Media. Platform checks are historical (2026-10-14). Auth validate checks passed but Supabase Preview was SKIPPED; no PR merge.
- **Platform native schedules:** inspect-vps #42112599830 PASS at 21:26:04Z; recover-stale-ops #42121354158 PASS at 22:25:22Z; reconcile-vps #42121826106 FAIL at 22:28:47Z only on Stock health; watchdog #42123445690 PASS at 22:40:18Z. Watchdog measured inspect age 74m, reconcile age 11m and recovery age 14m, with 0m queue for inspection/reconcile. At 23:04Z the inspect snapshot is ~98m old (>75m freshness budget); no later native inspect/watchdog run is evidenced. Reconcile workflow_run/workflow_dispatch recovery follow-ups are not native ticks.
- **K3s snapshot:** `debug/vps-latest.md` generated 21:26:12Z; stale at this checkpoint. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, disk 56%, ~19 GiB RAM available, runner services active, restart_required=yes. Media/MicroFE/NATS 1/1; Stock Admin (two Pods) and new Backend ImagePullBackOff; old Backend/Frontend 1/1. No live-health claim.
- **Stock:** production overlay still pins Admin/Backend to `12d63b4`. Reconcile #42121826106 used `ALLOW_IMAGE_CHANGES=false`; GHCR pull preflight passed, drift=false, apply skipped. ARM64 pull failed with `no match for platform in manifest`; permanent-failure restart guard skipped restart. Latest publisher #41563856933 and CI #41563856934 PASS on 2026-11-03; no newer publication. Paired promotion remains blocked on explicit authorization/protected provenance.
- **TCE:** current-master WF-01 #42105365294, WF-02 #42105365483, WF-05 #42105365567 and WF-12 push smoke #42105365586 PASS. WF-13 #42105390163 SKIPPED for push-smoke source. Latest native WF-07 #42098832858 PASS, WF-06 #42089383865 FAIL, WF-12 #42083178274 FAIL; all predate current master SHA. No post-merge native recovery E2E yet.
- **Media/Auth:** Media CI #41617592783 PASS (2026-11-03). Auth service CI #41670642852 PASS (2026-11-03), web CI #41542942080 PASS (2026-11-02); no newer master builds. Auth #75/#76 remain gated on Supabase Preview/deployment integration side-effect evidence.
- **Ownership/safety:** app repos own tests/builds/immutable GHCR; Platform owns manifests/shared pull credentials/provenance/promotion/reconciliation/rollout/health. `reconcile-vps.yml` sole production apply authority; `inspect-vps.yml` read-only. No production image/manifest/database/secret/replica/host/cron changes; no duplicate SSH/Compose/MCP authority; TCE market-scan schedule unchanged.


## Cross-repo deployment checkpoint — 2026-11-06 11:01 ICT / 04:01 UTC

- **Current default-branch heads:** Platform Infra `0c322b7104eccc9c05b04e1b7ef4f34c746d167f`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `6fcefa6b3792dab92b6d5c438001633d25f1ca28`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1314 (documentation-only mail-service plan), plus older draft #544/#541/#539; Authentication #75 (ready) and #76 (draft); none in TCE, StockDividend or Media. Platform #1313 is merged. Do not merge Auth PRs while the external Supabase integration side-effect gate remains unresolved.
- **Platform runner-retirement guard:** PR #1313 `fix(decommission): require Media runner unit disabled` merged by squash as `0c322b7104eccc9c05b04e1b7ef4f34c746d167f`. Exact-head checks `validate-manifests` #42157150764 and `validate-github-actions` #42157150728 both PASS on `e2b713cd8ab14aa7b8c04c0cc277fb84f4961245`. Post-merge checks #42159993013 and #42159993032 both PASS on the merge head. The pre-delete host guard now requires the dedicated Media runner service to be inactive AND disabled/masked/not-found, no `Runner.Listener` process, and a typed operator attestation of GitHub unregistration. The guard does not stop or unregister the runner itself.
- **Latest production reconcile evidence:** #42158234979 completed SUCCESS at 03:43:16Z with `mode=apply`, `ALLOW_IMAGE_CHANGES=false`. Shared GHCR access, Auth runtime Secret, pull credentials, preflight, post-apply drift check, MicroFE, Auth and TCE lanes passed; Keycloak lane was skipped. This is a workflow_dispatch run on pre-#1313 SHA `2b61b197b564f61bc60aa44f574c3435c0dd9bb1`, not a native schedule tick. No image promotion occurred.
- **Latest read-only K3s evidence:** inspect-vps #42154756357 completed at 03:09:08Z; `debug/vps-latest.md` was generated at 03:09:17Z (snapshot SHA `3e21c197b82f1c14d662e68664bbd0ab1594b378`). At this checkpoint it is 52 minutes old, within the 75-minute freshness budget, but is not a live query. Node `tce-k3s-01` is Ready on K3s v1.36.3+k3s1 / ARM64; GitOps drift is clean. Media backend/frontend are 1/1 Running and pinned to immutable digests. Stock Admin has two 0/1 ImagePullBackOff Pods and the newer Backend is 0/1 ImagePullBackOff because GHCR reports `no match for platform in manifest`; the legacy Backend and Frontend remain 1/1 Running. This is an ARM64 image-manifest issue, not evidence of a pull-secret failure. MicroFE Shell/WS/NATS are 1/1; TCE frontend/service, Auth and Keycloak are 0/0. The dedicated Media runner systemd unit is still active and enabled, with a `Runner.Listener` process. The snapshot does not independently establish external-data ownership or a complete storage backup decision.
- **TCE public health/recovery:** current-master WF-06 fallback #42158243093 failed all four strict public probes: `https://auth.mrcute.space/api/health`, `https://auth.mrcute.space/api/ready`, `https://tce.mrcute.space/api/health`, and `https://tce.mrcute.space/` all returned HTTP 503 (expected 200). The same snapshot reports TCE/Auth desired replicas 0/0, so this is consistent with the current disabled workload state; do not weaken probes or enable workloads to make CI green. Native WF-12 schedule watchdog #42158209117 failed because the scheduled WF-06 delivery was stale. WF-13 #42158228852 successfully dispatched the read-only fallback, but that fallback did not restore public health. Latest scheduled WF-06 in the returned run history is #42133793538 (00:01:48Z, failure); the later WF-06 #42158243093 is workflow_dispatch, not native schedule evidence. TCE market-scan cron is unchanged.
- **App CI / publication freshness:** StockDividend CI #42137523269 PASS on master; the latest immutable publisher evidence remains #41563856933 (2026-11-03), so no fresh ARM64 digest publication or paired production promotion is established. Media CI #42136991059 PASS on master; deployed Media backend/frontend remain digest-pinned and 1/1 in the snapshot. Authentication CI #41670642852 is historical (2026-11-03). TCE master remains `512b69d`; its public endpoint checks fail as described above. No new app image was published or promoted in this checkpoint.
- **Next dependency-safe actions:** (1) verify the dedicated Media runner is idle; stop and disable only its exact service, unregister it from the Media repository, then prove inactive/disabled and no Listener process; never touch the shared Platform runner. (2) Obtain a fresh same-window read-only K3s/storage inventory and independent backup/external-data/DNS owner confirmation. (3) Only then consider the protected manual decommission workflow with production Environment approval and exact typed confirmations; no namespace deletion is authorized by this checkpoint. (4) Fix Stock's ARM64 image manifest in the app-owned publisher, validate immutable digest/provenance, and require explicit release authorization before Platform promotion. (5) Keep TCE/Auth at 0/0 until the owner authorizes activation; investigate the external 503s without changing desired replicas or schedule.
- **Authority/safety:** app repositories own tests, builds and immutable GHCR publication; Platform Infra owns production manifests, shared pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole routine production apply authority; `inspect-vps.yml` remains read-only. Preserve useful CI/security/manual/release/scheduled jobs; no duplicate SSH/Compose authority. No K3s namespace, PVC/PV, database, DNS, GHCR package, host, replica or cron mutation. TCE market-scan schedule unchanged.


## Cross-repo deployment checkpoint — 2026-11-06 11:20 ICT / 04:20 UTC

- **Verified default-branch heads:** Platform Infra `5d1ba54b17827f6e423c275f1854fbb7945af50d`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `6fcefa6b3792dab92b6d5c438001633d25f1ca28`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `f978a3f378ee22d4630909c2d182275b21ac9e9a`.
- **Open PRs:** Platform #1314 (draft mail-service plan; validate check PASS on head `db152c9a17416d1a7f82165597dfe478321bd055`), #544/#541/#539 (old Keycloak drafts; checks from 2026-10-14, not fresh). Authentication #75 (ready) and #76 (draft); their validate checks pass on old heads, but Supabase Preview is SKIPPED on both and the branches are stale relative to master. No open PRs in TCE, StockDividend or Media Generation. Do not merge unrelated drafts as deployment work.
- **Platform PR/check evidence:** PR #1316 is merged; exact-head validation #42160559268 and post-merge validation #42160625527 PASS. Current open #1314 validation #42161859747 PASS. Latest Platform master validations include #42160625527 PASS. No current failing required check was found on the latest merged deployment-contract change.
- **Native Platform schedule evidence:** latest returned native scheduled reconcile #42152655025 PASS at 02:48:33Z; recovery controller #42152661024 PASS at 02:48:36Z; schedule watchdog #42152865619 PASS at 02:50:36Z. Latest native scheduled inspect #42145981473 PASS at 01:45:56Z. No later native scheduled Platform run appears in the current Actions event-filtered history. The later inspection #42154756357 is workflow_dispatch, not native schedule evidence. At this checkpoint native inspect is about 154m old; native reconcile/watchdog are about 92m/90m old. The last manual reconcile #42158234979 PASS at 03:43:16Z used pre-current master SHA `2b61b197b564f61bc60aa44f574c3435c0dd9bb1`, `mode=apply`, and `ALLOW_IMAGE_CHANGES=false`; it is not a native scheduled run and did not promote images. TCE heartbeat dispatch #42158219469 and recovery #42158367029 completed successfully.
- **Latest K3s snapshot:** inspect workflow_dispatch #42154756357 completed at 03:09:08Z; `debug/vps-latest.md` generated 03:09:17Z (blob `3e21c197b82f1c14d662e68664bbd0ab1594b378`). Snapshot age is about 71m here; use only as a recent-but-not-live observation, not destructive authorization. Node Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2, Docker 29.1.3, disk 56%, GitOps drift clean. Media backend/frontend 1/1 and digest-pinned. Stock Admin (two Pods) and new Backend are ImagePullBackOff because the deployed `12d63b4` images have no matching ARM64 manifest; legacy Backend/Frontend remain Running. TCE/Auth/Keycloak are 0/0. The snapshot's persistent-storage section showed only the unrelated `k3s-debug` PVC/PV; this is not a same-window pre-delete inventory.
- **TCE Dashboard:** WF-12 native schedule #42158209117 failed because latest scheduled WF-06 #42133793538 was 221m old. WF-13 #42158228852 successfully dispatched read-only fallback WF-06 #42158243093, but the fallback failed all four strict public probes with HTTP 503. The snapshot shows TCE/Auth desired replicas 0/0, consistent with the 503s. Keep HTTP 200 expectations and current desired replicas; do not turn the fallback into native schedule evidence. TCE market-scan schedule remains untouched.
- **StockDividend:** master CI #42137523269 PASS. Latest verified immutable publisher remains #41563856933 (2026-11-03); it is historical and does not prove a fresh digest/provenance or release authorization. No production promotion. Keep Stock app CI/publisher ownership; do not promote while its production retirement is pending and the deployed ARM64 manifest is invalid.
- **Media Generation:** master CI #42136991059 PASS. Backend/frontend remain digest-pinned and 1/1 in the snapshot. Dedicated Media runner remains systemd active/enabled with `Runner.Listener` present. PR #1313's guard is preventive; it does not stop, disable or unregister the runner.
- **Authentication:** latest master service CI #41670642852 PASS but historical (2026-11-03). PR #75 validate PASS / Supabase Preview SKIPPED; PR #76 validate PASS / Supabase Preview SKIPPED. Keep both gated pending fresh exact-head checks and authoritative Supabase integration side-effect evidence. Runtime is 0/0; public health is 503. No activation or release.
- **Decommission gate:** `.github/workflows/decommission-stock-media.yml` has not run. It remains manual-only, protected by production Environment approval, typed namespace/data-retention/runner confirmations, runner-retirement guard and fresh PVC/PV preflight. The current runner state fails the guard. The snapshot is not sufficient to approve deletion. Do not delete namespaces, PVC/PV, external databases/object storage, DNS, GHCR packages, app repos or source code.
- **Ownership and safety:** app repos own tests/builds and immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only routine production apply authority; `inspect-vps.yml` remains read-only. Preserve useful CI/security/manual/release/scheduled workflows and avoid SSH/Compose deployment paths. No image/manifest/secret/replica/host/storage/DNS/database/runner mutation occurred in this checkpoint. TCE market-scan schedule unchanged.

### Next dependency-safe actions

1. Obtain operator confirmation that the dedicated Media runner is idle; stop and disable only `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`, unregister it from the Media repository, and verify no Listener remains. Never touch the shared Platform runner.
2. Obtain a fresh same-window read-only inspection and independent backup/external-data/DNS ownership review. Only then consider the protected manual namespace-decommission workflow.
3. Investigate the missing native Platform scheduled ticks and TCE WF-06 schedule delivery without relaxing freshness thresholds or changing the TCE market-scan schedule.
4. Keep Stock promotion blocked until a new ARM64-capable immutable publication, verified digest/provenance and explicit release authorization exist; keep Auth PRs gated until Supabase side effects are evidenced.


## Current review — 2026-11-06 13:58 ICT (2026-11-06 06:58 UTC)

This checkpoint supersedes the 13:03 ICT runtime summary where newer evidence exists. It rechecks all five default-branch heads, open PRs, latest workflow/check outcomes, current release contracts, and the latest read-only VPS inspection. It records observed state only; it does not authorize release, replica changes, runner retirement, or namespace deletion.

### Default branches and open PRs

| Repository | Default-branch SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `f29465020b25e1b2f5318733b5918e2d3e8a582b` | #1314 draft; #544/#541/#539 drafts | Automated inspection PR #1324 merged; current head is the resulting inspection snapshot commit. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Native WF-06 schedule delivery is fresh again in the latest check; public endpoints still return HTTP 503. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | Master CI and native ARM64 build-only contract pass; no new publisher run. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | Master CI passes but is historical; no new publisher run. Runtime and dedicated runner remain active. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | CI passes; #75 remains blocked by the connected Supabase master-push deployment side-effect gate. |

### Platform Infra — latest reconcile and inspection

- Latest production reconcile: [#42176253693](https://github.com/phanthienquoc/platform-infra/actions/runs/42176253693), workflow_dispatch, created 2026-11-06 06:43:31Z on pre-inspection SHA `8d33b984cee5fa5dd8fbd2172a4ddc899d16bb6f`, completed SUCCESS. Shared reconcile, GHCR pull-access validation, Auth runtime Secret, shared pull credentials, MicroFE, Auth and TCE lanes, and final deployment gate passed; Keycloak lane was skipped. No new image promotion is evidenced by this run.
- Latest read-only inspection: [#42176445915](https://github.com/phanthienquoc/platform-infra/actions/runs/42176445915), created 06:45:17Z; snapshot generated 06:45:26Z. Its exact-head validation and squash merge completed, producing current master commit `f29465020b25e1b2f5318733b5918e2d3e8a582b` (inspection PR #1324).
- Recovery dispatch [#42176781772](https://github.com/phanthienquoc/platform-infra/actions/runs/42176781772) completed SUCCESS after the TCE integration-check event. The later `workflow_run` watchdog/recovery events #42176809771/#42176816321 were SKIPPED by event guards; do not count them as native scheduled reconcile ticks.
- No production manifests changed in the inspection snapshot. A new production apply is not required by this docs/inspection-only checkpoint.

### TCE — schedule freshness recovered; endpoint health still fails

- Native scheduled WF-06 run [#42176208184](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176208184) was delivered at 06:43:04Z (event=`schedule`) and failed all four public endpoint checks: TCE web, TCE API, Auth liveness and Auth readiness, each expected HTTP 200 but returned HTTP 503. Manual run #42176245458 also failed the same four checks.
- WF-07 native schedule [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608) completed SUCCESS at 06:48:12Z; its Binance private API check passed and the optional Testnet order integration job was skipped.
- WF-12 [#42176769424](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176769424), triggered by the successful WF-07 `workflow_run`, completed SUCCESS. Both "Verify WF-06 schedule delivery" and the authenticated Platform heartbeat dispatch passed. WF-13 [#42176787185](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176787185) was skipped because its stale-schedule recovery condition was not met.
- This supersedes the earlier "native WF-06 delivery is stale" diagnosis for this checkpoint: the latest native WF-06 schedule event was delivered and WF-12 verified freshness. It does **not** prove uninterrupted future schedule delivery.
- Endpoint health remains a separate failure. The latest K3s snapshot has `tce-prod/tce-frontend` and `tce-prod/tce-service` desired at 0/0; Auth/Keycloak are also 0/0. Keep strict HTTP 200 probes and the existing WF-06 cadence. Do not activate replicas without owner authorization and do not change any TCE market-scan schedule.

### Latest read-only K3s/storage evidence

Snapshot `debug/vps-latest.md`, generated 2026-11-06T06:45:26Z by inspect-vps #42176445915:

- Node `tce-k3s-01` is Ready, ARM64, K3s `v1.36.3+k3s1`; root filesystem 56% used, ~19 GiB available RAM, and `restart_required=yes`. No reboot or upgrade is authorized.
- GitOps drift is clean. Platform runner and dedicated Media runner are both active. The Media unit is enabled and `/opt/media-actions-runner/bin/Runner.Listener` remains present; the decommission guard must continue to block.
- `media-prod`: backend and frontend each 1/1 Running, digest-pinned to `prod-v0.3.0-58f80a8`; `media.mrcute.space` remains in service.
- `stock-prod`: namespace remains Active. Two Stock Admin Pods and one newer Backend Pod are ImagePullBackOff because tags `12d63b4` have no matching ARM64 manifest. Legacy Backend and Frontend remain 1/1 Running. This is an image-platform mismatch, not evidence of bad GHCR pull credentials.
- Persistent storage inventory lists only `k3s-debug/k3s-debug-logs`; Stock/Media have no listed PVC/PV claims and no VolumeSnapshot/VolumeSnapshotContent references. This does not prove external database/object-storage backup, DNS ownership, or data-retention approval.
- TCE frontend/service and Auth/Keycloak are desired 0/0. Do not scale them up as a healthcheck workaround.

### App-owned build and release contracts

- **StockDividend:** master CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) SUCCESS, including non-publishing native ARM64 builds for Admin, Backend and Scraper plus the release-hold contract. The latest observed publisher is older run [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933) (2026-11-03); no newer publication/digest evidence exists. `deploy.yml` publishes on qualifying master source pushes, verifies full-source-SHA tags resolve to GHCR digests and linux/arm64, and does not send a Platform handoff. Manual publication is refused unless the repository release variable is explicitly true. Do not bypass that hold or promote current broken `12d63b4` images.
- **Media Generation:** master CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) SUCCESS (historical). WF-03 is app-owned and currently supports master push/manual release, native ARM64 image builds, artifact SHA-256 checks, full-source-SHA release tags, GHCR digest verification and ARM64 manifest verification. It explicitly sends no Platform deployment dispatch. No newer publisher run is observed.
- **Authentication:** master CI [#42167100692](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42167100692) SUCCESS; Supabase Preview was SKIPPED. `release.yml` is manual-only, builds ARM64 with Buildx provenance/SBOM, verifies both full-SHA and versioned tags resolve to the same registry digest, then dispatches the digest and source run/workflow/event/head metadata to Platform. No release run or new digest/provenance was observed.
- **TCE Dashboard:** no open PR; latest master remains `512b69d`. WF-06 health is failing due inactive public services, not because the latest native schedule event was missing.
- A passing non-publishing ARM64 CI job is not a GHCR publication. A successful image build alone does not authorize GitOps promotion.

### Open safety gates and next dependency-safe actions

1. TCE owner must decide whether/when to activate TCE/Auth replicas; until then retain 0/0 and strict HTTP 200 assertions. Monitor subsequent native WF-06 schedule events separately from WF-12 fallback/heartbeat events.
2. Stock release remains gated for manual publication. Obtain explicit release authorization before dispatching; only then validate the full-SHA tag, registry digest and ARM64 manifest before considering a separate Platform promotion.
3. Media runner owner/operator must verify no job is active, then stop/disable/unregister only the dedicated Media runner and confirm no Listener remains. Never touch the shared Platform runner.
4. Repeat same-window K3s/storage preflight and obtain independent backup/external-data/DNS ownership review before the protected namespace-decommission workflow. Do not delete PVC/PV, external data, DNS, GHCR packages or application repositories.
5. Keep Auth PR #75 open: it changes docs/tests only, but owner-provided Supabase integration evidence says Deploy to production is ON for the Auth repository's `master`; exact merge-trigger side effects remain unverified. PR #76 remains draft. Do not merge or run migration/release operations until that gate is resolved.

**Ownership and safety:** app repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance verification, GitOps promotion/reconciliation, rollout and health verification. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No namespace, workload, replica, PVC/PV, external database, DNS, runner, host, image or TCE market-scan schedule was changed by this checkpoint.


## Runtime checkpoint — 2026-11-06 15:03 ICT / 08:03 UTC

This checkpoint supersedes the 13:58 ICT review wherever newer Actions API evidence exists. It is an observation and readiness update only; it does not authorize a release, scale-up, runner retirement, or namespace deletion.

### Current repository state, PRs and checks

| Repository | Default-branch SHA | Open PRs | Latest relevant checks |
|---|---|---|---|
| Platform Infra | `6687e665f1d62cbe97cff757b63ef7b1b154b4ee` | #1314 draft; #544/#541/#539 drafts | Master `validate` PASS: [#42178567534](https://github.com/phanthienquoc/platform-infra/actions/runs/42178567534). #1314 validate PASS on old head `db152c9a17416d1a7f82165597dfe478321bd055`: [#42161859747](https://github.com/phanthienquoc/platform-infra/actions/runs/42161859747). |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 native schedule #42176208184 failed four HTTP 200 probes; latest WF-12 workflow_run #42176769424 passed freshness/heartbeat at 06:48Z, but is not a native schedule tick. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | CI #42167088130 PASS (7 checks, including non-publishing ARM64 builds and release-hold contract). |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI #42136991059 PASS; historical relative to this checkpoint. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | CI #42167100692 PASS for validation and non-publishing ARM64 build; Supabase Preview SKIPPED. |

Platform Infra #1314 remains a draft, documentation-only mail-service plan and is unrelated to deployment. Its head/base are behind current master. #544/#541/#539 are old draft Keycloak PRs. Authentication #75/#76 also have old bases and stale validation evidence: #75 validation passed on 2026-10-27 and #76 on 2026-11-01; Supabase Preview was skipped on both. Do not merge these PRs as part of deployment work.

### Native schedule delivery — new stale gap

**Platform Infra:** the latest native scheduled runs in Actions history are:
- reconcile-vps #42152655025, event=schedule, 2026-11-06 02:48:33Z, SUCCESS.
- recover-stale-ops #42152661024, event=schedule, 02:48:36Z, SUCCESS.
- reconcile-schedule-watchdog #42152865619, event=schedule, 02:50:36Z, SUCCESS.
- inspect-vps #42145981473, event=schedule, 01:45:56Z, SUCCESS.

No newer native `event=schedule` runs were returned by the current Actions history. Later Platform activity is not native schedule evidence: production reconcile #42176253693 was `workflow_dispatch` at 06:43:31Z and succeeded with image changes disabled; inspection #42176445915 was also `workflow_dispatch` at 06:45:17Z; TCE heartbeat recovery #42176781772 was `repository_dispatch` at 06:48:29Z and succeeded. The later watchdog/recovery `workflow_run` events #42176809771/#42176816321 were skipped by event guards.

The workflow files still declare their intended schedules (reconcile 7/22/37/52, inspect 2/32, watchdog 12/27/42/57, recovery 10/25/40/55 UTC). Current read-only evidence does not distinguish GitHub schedule-delivery delay from a workflow-level/repository Actions setting; do not infer that the workflows are disabled. No cron change is proposed. The same scheduler cannot independently prove its own delivery; an external schedule or manual dispatch would require a separately approved operational decision.

**TCE Dashboard:** native schedule history is stale again:
- WF-06 latest native schedule #42176208184 at 06:43:04Z; failed all four public probes (TCE web, TCE API, Auth liveness/readiness returned HTTP 503).
- WF-07 latest native schedule #42176751608 at 06:48:12Z; SUCCESS.
- WF-12 latest native schedule #42158209117 at 03:43:01Z; FAILURE because WF-06 schedule delivery was stale at that time.
- WF-12 #42176769424 at 06:48:22Z was triggered by `workflow_run` after WF-07, not by schedule. It verified WF-06 age=5m and dispatched the authenticated Platform heartbeat successfully.
- WF-13 #42176787185 at 06:48:32Z was skipped because the stale condition was not met at that time.

At the 08:03Z observation time, the latest native WF-06 event was about 81 minutes old (budget 25m), WF-07 about 76 minutes old, and native WF-12 about 261 minutes old. Therefore schedule freshness is stale now, even though the 06:48 workflow_run watchdog check passed against the state at 06:48. Do not count workflow_run, repository_dispatch, or workflow_dispatch as native schedule ticks. WF-06 remains configured for `*/15 * * * *`; no TCE schedule or market-scan cadence was changed.

### Latest runtime evidence and freshness limitation

The latest available `debug/vps-latest.md` is from inspect-vps #42176445915, generated 2026-11-06T06:45:26Z. At 08:03Z it is about 78 minutes old and is not live authorization for destructive work.

That snapshot recorded:
- Node `tce-k3s-01` Ready, ARM64, K3s v1.36.3+k3s1; root disk 56%; about 19 GiB available RAM; `restart_required=yes`. No reboot/upgrade authorization.
- Media backend/frontend 1/1 Running and digest-pinned. Dedicated Media runner service active and enabled, with `Runner.Listener` still present.
- Stock Admin (two Pods) and newer Backend in ImagePullBackOff because deployed `12d63b4` images lack a matching ARM64 manifest; legacy Backend/Frontend 1/1 Running. This is an image-platform mismatch, not proof of bad GHCR credentials.
- TCE frontend/service and Auth/Keycloak desired 0/0, consistent with public HTTP 503. Do not scale them up without service-owner authorization.
- No Stock/Media PVC/PV claims or VolumeSnapshot references were listed; the only listed PVC/PV was unrelated `k3s-debug/k3s-debug-logs`. External database/object-storage backups, data retention and DNS ownership remain unproven.

### Immutable publication and release gates

- **StockDividend:** master CI #42167088130 proves build/test and non-publishing ARM64 build contracts only. The release-hold contract passed. The latest previously observed publisher remains #41563856933 (2026-11-03); no new GHCR publication, digest/provenance, or release authorization was observed. Manual publication remains gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`. Do not promote `12d63b4`.
- **Media Generation:** master CI #42136991059 is historical; no newer publisher run was observed. The app-owned WF-03 remains responsible for ARM64 build, artifact checksums, full-source-SHA tags, GHCR digest and ARM64 verification; no Platform dispatch is configured.
- **Authentication:** master CI #42167100692 includes a non-publishing ARM64 build; Supabase Preview was skipped. No manual release publisher run, registry digest/provenance or Platform promotion was observed. PR #75 remains gated by the unresolved Supabase master-push Deploy-to-production side effect; #76 remains draft.
- **TCE:** no new publisher or release promotion was observed. The last known public endpoint failure remains distinct from GitOps schedule delivery.

### Next dependency-safe actions

1. Verify GitHub Actions workflow state and repository/org Actions policy for Platform and TCE schedules, and check GitHub service health. Preserve the current cron expressions and TCE market-scan schedule; do not add a competing production apply authority.
2. Obtain a fresh read-only inspect-vps run (manual dispatch by an authorized operator if native schedule delivery remains absent) before using any runtime evidence for decommission.
3. Keep TCE/Auth at desired 0/0 and strict HTTP 200 probes until service owners authorize activation.
4. Obtain Stock release authorization before any manual publisher run; then verify full-source-SHA tag, registry digest, provenance and linux/arm64 manifest before a separate Platform promotion.
5. Retire only the dedicated Media runner after operator confirms idle, stop/disable/unregister and verifies no Listener remains; never touch the shared Platform runner.
6. Require same-window storage preflight plus independent backup/external-data/DNS ownership review before the protected Stock/Media namespace-decommission workflow.

**Ownership and safety:** app repositories own tests/builds and immutable GHCR publication; Platform Infra owns production manifests, shared GHCR pull credentials, digest/provenance validation, GitOps promotion/reconciliation, rollout and health verification. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No production workload, replica, image, credential, namespace, PVC/PV, external data, DNS, runner or host was changed in this checkpoint. TCE market-scan schedule unchanged.


## Runtime checkpoint — 2026-11-06 16:03 ICT / 09:03 UTC

A fresh repository/PR audit and source-contract review was completed. Default-branch heads: Platform Infra `f62f8a8c457cce12a9286efa246f6279129c8bab`; TCE Dashboard `512b69d837e2a65c39867a062529a7fa0eada4cc`; StockDividend `3aeaf519b7a786d13dcecee763acaca357c47ddd`; Media Generation `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Authentication `3a8031196f21c4240b617bbd0a623fce2dc56c5e`.

Open PRs remain Platform #1314/#544/#541/#539 (all drafts) and Authentication #75 (ready)/#76 (draft); TCE, Stock and Media have none. PR-head runs were retrieved: Platform #1314/#544/#541/#539 and Auth #75/#76 each show their listed validation/CI run as SUCCESS, but all are historical and the PR bases are stale relative to current master. Do not merge based on those old checks.

The latest repo-wide Actions evidence available remains the 15:03 ICT / 08:03 UTC checkpoint above. This run re-queried heads/open PRs and exact PR-head runs; default-head combined status and commit-run queries returned no records through the connected reader. Its commit-run view is PR-triggered only, so no newer repo-wide run IDs or schedule events can be asserted. This is a retrieval limitation, not evidence that scheduled workflows did not execute. The last known TCE evidence remains WF-06 native #42176208184 failed four strict HTTP 200 probes with 503, WF-07 #42176751608 passed, and WF-12 #42176769424 was a workflow_run freshness/heartbeat success rather than native schedule. Last known Platform manual reconcile #42176253693 passed with image changes disabled; last known inspection #42176445915 is now stale.

Source review confirms TCE WF-06 `*/15`, WF-12 `7,22,37,52`, Platform reconcile watchdog `12,27,42,57`; WF-13 is read-only workflow_run fallback only. No cron or market-scan schedule changed. The last K3s snapshot is generated 06:45:26Z and is about 2h18m old; do not use it for destructive authorization. Stock ARM64 image mismatch, inactive TCE/Auth replicas, and active/enabled Media runner remain the last observed gates. See [the 16:03 checkpoint](cross-repo-workflow-inventory-checkpoints/2026-11-06-1603-ict.md) for full evidence and next actions.


## Runtime checkpoint — 2026-11-06 16:58 ICT / 09:58 UTC

This checkpoint follows a fresh five-repository audit, Actions run-history inspection, exact open-PR/check review, and the latest read-only VPS snapshot. It records observed state only. It does not authorize image publication, service activation, runner retirement, namespace deletion, or host maintenance.

### Default branches, open PRs, and current checks

| Repository | Default-branch SHA | Open PRs | Latest observed CI / Actions evidence |
|---|---|---|---|
| Platform Infra | `ca49cef285c7b18136e006a928de8596a769cd59` | #1314, #544, #541, #539 (all drafts) | Scheduled inspect #42193617816 SUCCESS; watchdog #42193856388 FAILURE due stale native scheduled reconcile; recovery reconcile #42193876822 SUCCESS with no manifest drift and image changes disabled. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | WF-06 native schedule #42176208184 FAILURE (four HTTP 503 probes); WF-07 native schedule #42176751608 SUCCESS; WF-12 #42176769424 was workflow_run, not a native schedule. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | CI #42167088130 SUCCESS (7/7, including non-publishing ARM64 builds and release-hold contract). Latest observed publisher #41563856933 is 2026-11-03. |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI #42136991059 SUCCESS; no newer publisher run in the returned Actions history. |
| Authentication | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready; #76 draft | CI #42167100692 SUCCESS for validation and non-publishing ARM64 build; Supabase Preview SKIPPED; no release publisher run. |

PR check evidence remains stale on the old open heads: Platform #1314 validation #42161859747 passed on its old head; Authentication #75 validation #40446492086 and #76 validation #41329425940 passed on old heads, with Supabase Preview skipped. Their bases are behind current master. #544/#541/#539 are unrelated old Keycloak drafts. Do not merge any of these based on stale checks.

### Platform scheduled operations and recovery

- Latest native scheduled inspect is [#42193617816](https://github.com/phanthienquoc/platform-infra/actions/runs/42193617816), created 2026-11-06 09:15:08Z and completed SUCCESS. Its read-only snapshot was committed by automated inspection commit `ca49cef285c7b18136e006a928de8596a769cd59` (#1329) at 09:16:46Z.
- The latest native scheduled reconcile still observed in Actions history is #42152655025 at 02:48:33Z. The schedule freshness watchdog [#42193856388](https://github.com/phanthienquoc/platform-infra/actions/runs/42193856388) failed at 09:16:57Z because the native reconcile was 388 minutes old; its scheduled-recovery freshness check also failed. This is an intentional stale-delivery alarm, not a code-validation failure.
- The recovery controller [#42193856545](https://github.com/phanthienquoc/platform-infra/actions/runs/42193856545), triggered after the scheduled inspection, succeeded and dispatched [reconcile #42193876822](https://github.com/phanthienquoc/platform-infra/actions/runs/42193876822) at 09:17:06Z. That run used `mode=apply`, `target_app=all`, `ALLOW_IMAGE_CHANGES=false`; GHCR pull Secret and Auth runtime Secret were verified/reconciled, TCE GitOps image pairing passed, and Kubernetes diff reported no manifest drift. Therefore production manifest apply and post-apply drift steps were correctly skipped. The run is not evidence of a new image promotion or manifest apply.
- Auth and TCE deployment lanes passed their configured health gates by verifying their explicit desired-zero maintenance state and no active pods; their rollout steps were skipped because no manifest drift existed. MicroFE workload health passed. Keycloak lane was skipped. The final gate passing must not be described as TCE/Auth public service availability: their desired replicas remain 0/0 and public OIDC probes return HTTP 503.
- Recovery run [#42194042813](https://github.com/phanthienquoc/platform-infra/actions/runs/42194042813) completed SUCCESS as `workflow_dispatch`; it is not native schedule evidence. Preserve the native schedule freshness alarm and do not count fallback dispatches as cron delivery.

### Latest read-only K3s snapshot

Snapshot source: inspect-vps #42193617816; committed in `debug/vps-latest.md` at master SHA `ca49cef285c7b18136e006a928de8596a769cd59`.

- Node `tce-k3s-01`: Ready, ARM64, K3s `v1.36.3+k3s1`, containerd `2.3.2-k3s2`; the snapshot reports `restart_required=yes`. No reboot or upgrade is authorized.
- GitOps drift: clean. Media backend/frontend are 1/1 Running and digest-pinned. Stock Admin (two Pods) and the newer Stock Backend remain ImagePullBackOff because deployed tag `12d63b4` has no matching ARM64 manifest; the legacy Backend and Frontend remain 1/1 Running. The error is an image-platform mismatch, not evidence of invalid GHCR pull credentials.
- TCE frontend/service and Auth/Keycloak remain desired 0/0. Public OIDC endpoints return HTTP 503, consistent with the inactive runtime state.
- In-cluster storage lists only unrelated `k3s-debug/k3s-debug-logs`; no Stock/Media PVC/PV claims or VolumeSnapshot/VolumeSnapshotContent references are listed. This does not prove external database/object-storage backups, retention approval, or DNS ownership.
- Dedicated Media runner is still systemd active and enabled, with `/opt/media-actions-runner/bin/Runner.Listener` present. The shared Platform runner is also active. Do not stop or unregister either runner through this workflow; only the dedicated Media runner may be retired after operator confirms it is idle and explicitly completes stop/disable/unregister.

### Cross-repository deployment ownership and publication

- **StockDividend:** `.github/workflows/deploy.yml` owns ARM64 GHCR publication and verifies full-source-SHA tags, registry digest and ARM64 manifest. It contains no SSH/SCP/kubectl or Platform dispatch path. Manual publication is refused unless `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`; no current release authorization or publisher run exists. CI ARM64 checks are non-publishing and do not authorize promotion.
- **Media Generation:** WF-03 owns native ARM64 builds, checksum-verified artifacts, full-source-SHA release tags, GHCR digest and ARM64 verification. It contains no SSH/SCP/kubectl or Platform dispatch path. No newer publisher run is observed.
- **TCE Dashboard:** WF-03 is an app-owned immutable publisher and sends a digest/source-run payload to Platform Infra; Platform validates and owns promotion/reconciliation. It is not a direct SSH/Compose deployment authority.
- **Authentication:** release publisher remains manual-only, uses ARM64 Buildx provenance/SBOM and digest verification, then dispatches source/digest metadata to Platform. No publisher run or new digest was observed.
- No duplicate app-owned SSH/Compose production deployment authority was found in the inspected Stock, Media, or TCE production publisher workflows. Keep `reconcile-vps.yml` as the sole Platform production apply authority and `inspect-vps.yml` read-only.

### Next dependency-safe actions

1. Investigate why native Platform reconcile schedule delivery remains stale; keep the watchdog failure visible and retain the existing cron expressions. The recovery controller is currently providing a workflow_dispatch fallback, not native schedule proof.
2. Investigate TCE WF-06/WF-12 native schedule freshness separately from public endpoint health. Preserve strict HTTP 200 probes and the existing TCE market-scan schedule.
3. Keep TCE/Auth at 0/0 until the service owner authorizes activation.
4. Obtain Stock release authorization before any manual publisher run; then verify full-source-SHA, GHCR digest, linux/arm64 manifest and provenance before a separate Platform promotion. Do not promote `12d63b4`.
5. Operator confirms the dedicated Media runner is idle, then stops/disables/unregisters it and verifies no Listener remains. Never touch the shared Platform runner.
6. Require same-window storage inspection plus independent backup/external-data/DNS ownership review before the protected Stock/Media namespace-decommission workflow.

**No production workload, image, replica, manifest, credential, namespace, PVC/PV, external database, DNS, runner or host was mutated by this checkpoint.** TCE market-scan schedule unchanged.


## Post-checkpoint schedule update — 2026-11-06 17:03 ICT / 10:03 UTC

This short addendum supersedes the Platform native-reconcile freshness status recorded in the 16:58 ICT checkpoint. It does not change the TCE schedule diagnosis or authorize production mutation.

- Native Platform reconcile [#42199267592](https://github.com/phanthienquoc/platform-infra/actions/runs/42199267592) was delivered at 10:00:15Z and completed SUCCESS. This is a genuine `event=schedule` run, not a workflow_dispatch fallback. It ran on master SHA `ca49cef285c7b18136e006a928de8596a769cd59`.
- Native Platform recovery [#42199274660](https://github.com/phanthienquoc/platform-infra/actions/runs/42199274660) was delivered at 10:00:18Z and completed SUCCESS. Its recovery step was skipped because no stale delivery needed repair. The earlier watchdog failure #42193856388 correctly reported the prior stale interval; the native reconcile schedule has now resumed.
- Reconcile #42199267592 used `mode=apply`, `target_app=all`, `ALLOW_IMAGE_CHANGES=false`. Kubernetes diff found no manifest drift; production apply and drift verification were skipped. Auth/TCE remained in desired-zero maintenance state, MicroFE health passed, and Keycloak was skipped. This is not an image promotion or new manifest rollout.
- Latest native Platform inspect remains #42193617816 at 09:15:08Z; no newer scheduled inspection was present in the latest 100-run Actions history. Snapshot age was about 48 minutes at this addendum, within the 75-minute inspection freshness budget. Continue read-only observation; do not use it as destructive authorization.
- TCE native schedules remain stale in the returned history: WF-06 #42176208184 at 06:43:04Z (FAIL, four HTTP 503 probes), WF-07 #42176751608 at 06:48:12Z (PASS), and WF-12 #42158209117 at 03:43:01Z (FAIL). WF-12 #42176769424 at 06:48:22Z was workflow_run, not native schedule. TCE/Auth are still desired 0/0; keep HTTP 200 probes strict and do not change the TCE market-scan schedule.
- PR #1330 merged as `6bb2989ccf59cee35d2713b78684c6cad81d82e5`; exact-head validation #42199576132 and post-merge validation #42199644564 both PASS. Current Platform master is that merge SHA.

Stock ARM64 publication, Media runner retirement, external-data/backup/DNS review, and Authentication Supabase release gates are unchanged. No workload, image, replica, credential, namespace, storage, runner, DNS, database, host or TCE market-scan schedule was changed.


# Cross-repo deployment readiness — 2026-11-06 19:04 ICT / 12:04 UTC

## Current repository heads and open pull requests

| Repository | Current default-branch head | Open PRs |
|---|---|---|
| `phanthienquoc/platform-infra` | `e9401235569a75c0a5e8afc761f4389ae44b6721` | #1314, #544, #541, #539 (documentation/draft work) |
| `phanthienquoc/TCE-dashboard` | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None |
| `phanthienquoc/stockdividend` | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None |
| `phanthienquoc/media-generation` | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None |
| `phanthienquoc/phanthienquoc-authentication` | `3a8031196f21c4240b617bbd0a623fce2dc56c5e` | #75 ready, #76 draft, #89 open |

The current Authentication PR #89 is on `fix/auth-release-ref-gate-20261106-1904-ict`, exact head `019b1dc96dba3f45a6f637e3fd54059d3ee0bcc1`. It adds a mandatory zero-permission `validate-release-ref` job that rejects manual release dispatches outside `refs/heads/master`, makes verify/publish depend on that gate, and scopes `packages:write` to the publish job. It updates `scripts/validate-release-contract.mjs` and README. No publisher was dispatched and no image was published.

## Latest verifiable workflow/check evidence

- Platform Infra PR #1337 post-merge validation [#42210875736](https://github.com/phanthienquoc/platform-infra/actions/runs/42210875736) completed successfully; its `validate` job passed on the current Platform master head.
- TCE WF-06 native healthcheck [#42176208184](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176208184) failed all four public probes (TCE web/API and Auth liveness/readiness returned HTTP 503). WF-07 #42176751608 passed; WF-12 #42158209117 is the latest native schedule evidence in the prior checkpoint and failed freshness. Do not count WF-12 workflow_run #42176769424 or WF-13 workflow_run #42176787185 as native schedule delivery.
- StockDividend CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) passed all seven jobs, including tests/builds, release-hold contract and non-publishing native ARM64 image builds.
- Media Generation CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) passed its application test/build job; this is historical evidence, not a new release.
- Authentication default-branch CI [#42167100692](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42167100692) passed validation and non-publishing ARM64 build. New PR #89 CI [#42215166348](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215166348) is in progress: both `validate` and `Build production container on ARM64 without publishing` were running when inspected.

The connected GitHub status endpoint returned no combined status contexts for the five default-branch heads. The workflow-run lookup for those default-branch commits also returned no records (its exposed wrapper filters to PR-triggered runs). Therefore this checkpoint does **not** claim a complete latest repo-wide Actions history or that no newer native schedules occurred. The last schedule/reconcile evidence below remains the last independently recorded evidence in the inventory, not a fresh run-history query.

## Runtime, schedule and immutable publication gates

- Last independently recorded Platform native reconcile is #42199267592 (10:00:15Z, SUCCESS) with `ALLOW_IMAGE_CHANGES=false` and no manifest drift; native recovery #42199274660 succeeded/no-op. Later #42207918291 was a manual dispatch, not native schedule evidence. Do not infer current schedule freshness without a new Actions run listing.
- Last K3s snapshot remains inspect-vps #42208147735, generated 11:09:51Z. At 12:04Z it is about 6h54m old and must not be used for decommission approval. It recorded Media backend/frontend 1/1 Running; Stock Admin/new Backend ImagePullBackOff because deployed tag `12d63b4` lacks a linux/arm64 manifest; legacy Stock Backend/Frontend running; TCE/Auth/Keycloak desired 0/0; GitOps drift clean; only unrelated `k3s-debug/k3s-debug-logs` PVC/PV; dedicated Media runner active/enabled with `Runner.Listener`; `restart_required=yes`.
- TCE WF-06 still declares `*/15 * * * *`, requires HTTP 200 for all four public endpoints, and has no SSH/VPS inspection. WF-12 remains `7,22,37,52 * * * *`, read-only with Actions read permission. Do not change either cron or the TCE market-scan schedule.
- Stock `deploy.yml` owns three ARM64 GHCR images and full-source-SHA/digest verification. Manual publication remains gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`; no new publisher run or release authorization was verified. Do not promote `12d63b4`.
- Media `wf-03-media-production-deploy.yml` owns ARM64 build, checksum-verified artifacts, immutable full-SHA release tags and GHCR digest/ARM64 verification; no Platform dispatch is sent. No new publisher run was verified.
- Auth release remains manual-only, with full-SHA tags, BuildKit provenance/SBOM, digest verification and `auth-image-published` provenance payload. PR #89 hardens non-master dispatch rejection; its CI is still in progress. No Auth release publisher was run.
- Dedicated Media runner retirement remains blocked until operator confirms idle, stops/disables/unregisters that dedicated runner and verifies no Listener remains. Never stop or unregister the shared Platform runner.
- No Stock/Media namespace deletion until a fresh same-window K3s/storage inspection and independent external database/object-storage backup, retention and DNS ownership review pass.

## Ownership and safety

App repositories own tests, builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, publisher provenance/digest verification, GitOps promotion/reconciliation, rollout and health verification. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. Preserve useful CI, tests, security, manual/release/scheduled jobs. No duplicate direct SSH/Compose deployment authority was introduced.

No production workload, image, replica, manifest, credential, namespace, PVC/PV, external database, DNS, runner or host was mutated by this checkpoint. TCE market-scan schedule unchanged.

## Next actions

1. Finish PR #89 CI; merge only after exact-head required checks pass and re-read the current head immediately before squash merge.
2. Obtain a current Actions run listing for all five repositories, with event type, workflow path, head SHA and conclusion; classify native schedules separately from dispatch/fallback.
3. Run a fresh read-only `inspect-vps` before any decommission decision.
4. Keep Stock publication gated until explicit release authorization; require new full-SHA GHCR digest and ARM64 manifest evidence before any separate promotion.
5. Require operator-confirmed Media runner idle/stop/disable/unregister plus fresh storage/external-data/DNS review before namespace decommission.
6. Keep TCE/Auth at desired 0/0 until service-owner activation approval; retain strict HTTP 200 health gates.


## Post-merge update — 2026-11-06 19:08 ICT / 12:08 UTC

- Authentication PR [#89](https://github.com/phanthienquoc/phanthienquoc-authentication/pull/89) merged by squash as `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`. Exact PR head `019b1dc96dba3f45a6f637e3fd54059d3ee0bcc1` passed Auth CI [#42215166348](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215166348): both jobs passed, including npm test/typecheck/build, immutable release contract validation, native ARM64 non-publishing image build and local architecture verification. The merged default-branch head was independently re-read as `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`.
- The Auth release workflow now fails the workflow on any manual dispatch whose ref is not exactly `refs/heads/master`; verification and publication depend on that zero-permission gate. `packages:write` is scoped to the publish job. The manual-only release trigger, full-SHA tags, ARM64 publication, BuildKit provenance/SBOM, digest checks and provenance-bound `auth-image-published` event remain intact. No release publisher or GHCR push was triggered.
- Platform Infra PR [#1338](https://github.com/phanthienquoc/platform-infra/pull/1338) merged as `52c45b334d31ee9e00ca9be51b1c039ed0229e79`. Its exact-head `validate-manifests` run [#42215324106](https://github.com/phanthienquoc/platform-infra/actions/runs/42215324106) passed all manifest, script, Auth GitOps, rendered YAML, secret-policy and immutable-image checks. The connected Actions reader did not expose a post-merge push run; do not claim a separate post-merge workflow pass.
- Current Platform master: `52c45b334d31ee9e00ca9be51b1c039ed0229e79`. Current Auth master: `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`. Open Platform PRs remain #1314/#544/#541/#539; open Auth PRs remain #75/#76. No open PRs were found in TCE, StockDividend or Media Generation.
- The connector still does not provide repo-wide default-branch Actions run listings/status contexts; default-branch combined statuses were empty. Last-known TCE health, Stock/Media runtime and K3s evidence remain the prior checkpoint's evidence, not a fresh operational observation.

No production workload, image, replica, manifest, Secret, namespace, PVC/PV, external database, DNS, runner or host was changed. TCE market-scan schedule unchanged.


## Runtime checkpoint — 2026-11-06 19:55 ICT / 12:55 UTC

Current heads: Platform `bfb5cbcac5b8f8307d91c1e62973f0bd9f89f3f5`; TCE `512b69d837e2a65c39867a062529a7fa0eada4cc`; Stock `3aeaf519b7a786d13dcecee763acaca357c47ddd`; Media `3a8846a4f273eeb20a55b214d5ad80804c2d8d52`; Auth `3b60ff46b8959d18aee1956f99d6b62589b8b9c5`. Open PRs: Platform #1314/#544/#541/#539 (draft); Auth #75 ready/#76 draft; none in TCE/Stock/Media. Auth #75/#76 are respectively 13 commits behind current master and have only historical CI; do not merge without rebase and exact-head checks.

Platform current-head manifest validation #42215611596 PASS. Latest native schedule evidence is older: reconcile #42199267592 (10:00:15Z), recovery #42199274660 (10:00:18Z), watchdog #42201400071 (10:16:28Z), inspect #42193617816 (09:15:08Z). Manual reconcile #42211637997 and recovery #42211812418 succeeded but do not count as native schedule delivery. Watchdog URL-construction regression from #42207900645 was fixed in #6f5d329; read-only smoke #42208198166 and actionlint/regression run #42208198270 passed.

TCE WF-12 native schedule #42211610532 failed at 11:37:17Z because native WF-06 #42176208184 was 294 minutes old (25-minute budget); heartbeat dispatch succeeded. WF-13 recovery #42211627712 dispatched WF-06 fallback #42211645157, which still failed all four strict HTTP 200 endpoint probes (HTTP 503). WF-07 native #42176751608 passed. No cron changes.

Latest app CI: Stock #42167088130 PASS 7/7; Media #42136991059 PASS; Auth #42215394539 PASS on current head. Latest publishers remain historical: Stock #41563856933 (Nov 3), Media #41158598649 (Oct 31), Auth #41040510320 (Oct 30). No current-head immutable GHCR publication/digest/provenance was verified.

Latest K3s snapshot #42208147735 was a manual inspect at 11:09:51Z and is ~1h45 old. It recorded Media 1/1, Stock Admin/new Backend ImagePullBackOff on missing ARM64 manifest for tag `12d63b4`, TCE/Auth/Keycloak 0/0, clean GitOps, no Stock/Media PVC/PV or snapshots (only unrelated debug PVC), Media runner active/enabled with Listener, and restart_required=yes. External backup/data/DNS ownership remains unverified; no fresh inspect dispatch was available. Do not decommission from this snapshot.

App-owned CI/build/publish and Platform-only GitOps ownership remain unchanged. `reconcile-vps.yml` is the sole apply authority; `inspect-vps.yml` is read-only. No production mutation; TCE market-scan schedule unchanged. Full evidence: [checkpoint 2026-11-06 19:55 ICT](cross-repo-workflow-inventory-checkpoints/2026-11-06-1955-ict.md).


# Cross-repo deployment readiness — 2026-11-06 21:04 ICT / 14:04 UTC

## Current default-branch heads and open PRs

| Repository | Default-branch SHA | Open PRs | Latest default-branch CI evidence |
|---|---|---|---|
| Platform Infra | `40c9adeeefbe3c80beb3c9c97ff1bb78e85badf6` | #1314/#544/#541/#539 (draft); #1341 active implementation | Master validation [#42221880894](https://github.com/phanthienquoc/platform-infra/actions/runs/42221880894) PASS. PR #1341 exact head `67ac9bcb0e79cf1f32b57eeda08fe3a239802e88`: [validate-manifests #42230499865](https://github.com/phanthienquoc/platform-infra/actions/runs/42230499865) PASS; [validate-github-actions #42230499749](https://github.com/phanthienquoc/platform-infra/actions/runs/42230499749) PASS. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Latest WF-06 fallback [#42211645157](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42211645157) FAIL; latest native WF-12 [#42211610532](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42211610532) FAIL. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | Master CI [#42167088130](https://github.com/phanthienquoc/stockdividend/actions/runs/42167088130) PASS (7/7, including non-publishing ARM64 builds). |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | Master CI [#42136991059](https://github.com/phanthienquoc/media-generation/actions/runs/42136991059) PASS; no newer run in the inspected history. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready; #76 draft | Current master CI [#42215394539](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215394539) PASS. |

Authentication PRs are stale/diverged and were not merged: #75 is 28 commits ahead / 13 behind master; #76 is 3 ahead / 13 behind. Their historical checks are not current-head evidence.

## Concrete deployment-contract improvement

[PR #1341](https://github.com/phanthienquoc/platform-infra/pull/1341) updates `scripts/verify-workload-health.sh` and its regression suite. A deliberate zero-replica maintenance scope previously ended with the generic `Targeted workload health gate passed.` message, which could be mistaken for live service health. The helper now emits an explicit GitHub notice that the scope is in zero-replica maintenance and that no live workload health is asserted. Mixed active/maintenance scopes are reported separately. Existing fail-closed checks for replica convergence and remaining active pods are unchanged.

The first PR attempt exposed a test-fixture newline-escaping error (run #42230410219 on the earlier head); the fixture was corrected in commit `67ac9bcb0e79cf1f32b57eeda08fe3a239802e88`. Both required checks passed on that exact final head. PR #1341 remains open pending final head/check re-read and squash merge.

## Native schedule evidence (event=schedule only)

| Repository / workflow | Latest native run in the inspected 100-run history | Result |
|---|---|---|
| Platform reconcile | [#42199267592](https://github.com/phanthienquoc/platform-infra/actions/runs/42199267592), 10:00:15Z | PASS |
| Platform recovery | [#42199274660](https://github.com/phanthienquoc/platform-infra/actions/runs/42199274660), 10:00:18Z | PASS |
| Platform watchdog | [#42201400071](https://github.com/phanthienquoc/platform-infra/actions/runs/42201400071), 10:16:28Z | PASS |
| Platform inspection | [#42193617816](https://github.com/phanthienquoc/platform-infra/actions/runs/42193617816), 09:15:08Z | PASS |
| TCE WF-06 | [#42176208184](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176208184), 06:43:04Z | FAIL, public endpoints returned HTTP 503 |
| TCE WF-07 integration | [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608), 06:48:12Z | PASS |
| TCE WF-12 watchdog | [#42211610532](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42211610532), 11:37:17Z | FAIL, latest native WF-06 was 294 minutes old vs 25-minute budget |

Later Platform reconcile #42211637997 and recovery #42211812418 are workflow_dispatch events, not native schedule evidence. TCE WF-13 #42211627712 is workflow_run; its WF-06 fallback #42211645157 is workflow_dispatch. None refreshes native schedule freshness. Cron declarations and the TCE market-scan schedule remain unchanged.

## Production and runtime evidence

Latest manual Platform reconciliation [#42211637997](https://github.com/phanthienquoc/platform-infra/actions/runs/42211637997) completed successfully with `mode=apply`, `target_app=all`, and `ALLOW_IMAGE_CHANGES=false`. GHCR pull access preflight passed for Auth, MicroFE and TCE images; `ghcr-pull` reported unchanged in the checked namespaces. Auth runtime Secret provision/verification completed with values suppressed. Kubernetes diff was clean and production manifest apply was correctly skipped. This is not an image promotion or new rollout.

The same run captured a K3s pod listing at 11:37:57Z:
- Node `tce-k3s-01`: Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Media backend/frontend: 1/1 Running.
- MicroFE Shell/WS/NATS: Running.
- Stock Admin: two Pods ImagePullBackOff.
- Stock Backend: legacy Pod 1/1 Running; newer Pod ImagePullBackOff.
- Stock Frontend: 1/1 Running.

The deployed Stock Admin/new Backend tag `12d63b4` still lacks a linux/arm64 manifest; do not infer a GHCR credential problem and do not promote the tag. The latest dedicated inspect workflow remains [#42208147735](https://github.com/phanthienquoc/platform-infra/actions/runs/42208147735) at 11:09:51Z. The manual reconcile pod listing is newer, but it does not refresh storage or runner-retirement evidence. No newer same-window PVC/PV/VolumeSnapshot, external backup, DNS ownership or Media runner Listener inspection is available.

TCE/Auth desired replicas remain 0/0 by maintenance intent; WF-06 still requires HTTP 200 on all four public endpoints and currently fails HTTP 503. Do not weaken the probe or activate services without service-owner approval.

## Immutable publication and ownership

- Stock latest publisher: [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933), 2026-11-03, source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`; older than current master. Current CI ARM64 jobs are build-only.
- Media latest publisher: [#41158598649](https://github.com/phanthienquoc/media-generation/actions/runs/41158598649), 2026-10-31, source SHA `32f3bf56e1f44c65a5d98f35bed0547f398f8e90`; older than current master.
- Auth latest publisher: [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320), 2026-10-30, source SHA `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`; older than current master and the current fail-closed release gate.
- No current-master Stock/Media/Auth publisher run, digest/provenance pair or new release authorization was observed. No publisher was triggered.

App repositories continue to own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose production authority was added.

## Next dependency-safe actions

1. Re-read PR #1341 exact head and both required checks, then squash-merge only if the head is unchanged and both remain PASS.
2. Investigate TCE native WF-06 schedule delivery separately from its expected HTTP 503 maintenance probes; preserve cron and strict HTTP 200.
3. Obtain a fresh read-only inspection that includes storage and dedicated Media runner state before any decommission decision.
4. Keep Stock publication gated until explicit release authorization; require current full-source-SHA, immutable digest, provenance and ARM64 manifest before separate Platform promotion.
5. Keep Auth #75/#76 gated until they are reconciled with master and exact-head checks pass; do not run production migrations from stale PR branches.

No namespace, PVC/PV, image, replica, DNS, external database, runner or host was deleted or reconfigured by this checkpoint. The manual reconcile did run Auth runtime Secret provision/verification and confirmed GHCR pull Secrets unchanged. TCE market-scan schedule unchanged.


# Cross-repo deployment readiness — 2026-11-06 21:10 ICT / 14:10 UTC

## Repository heads and open PRs

| Repository | Default-branch SHA | Open PRs | Latest CI / operational evidence |
|---|---|---|---|
| Platform Infra | `5824a4af4dd91e498134ea8eafd2e026725344c0` | #1314/#544/#541/#539 drafts | PR #1341 merged; post-merge `validate-github-actions` #42230952977 PASS, `validate-manifests` #42230952863 PASS, production reconcile #42230952994 PASS. Inspection PR #1342 merged after exact-head validation #42231396933 PASS. |
| TCE Dashboard | `512b69d837e2a65c39867a062529a7fa0eada4cc` | None | Latest WF-12 native schedule #42211610532 FAIL; WF-06 fallback #42211645157 FAIL. |
| StockDividend | `3aeaf519b7a786d13dcecee763acaca357c47ddd` | None | CI #42167088130 PASS 7/7; latest publisher #41563856933 is old-source (Nov 3). |
| Media Generation | `3a8846a4f273eeb20a55b214d5ad80804c2d8d52` | None | CI #42136991059 PASS; latest publisher #41158598649 is old-source (Oct 31). |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready; #76 draft | CI #42215394539 PASS; latest publisher #41040510320 is old-source (Oct 30). |

Auth PR #75 remains 28 commits ahead / 13 behind master; #76 is 3 ahead / 13 behind. Do not merge either without reconciling to current master and running exact-head checks.

## Completed deployment-contract work

- Platform PR [#1341](https://github.com/phanthienquoc/platform-infra/pull/1341) squash-merged as `1e48033533d4606e8da4e54135e0167cbc787c52`. Its exact final head `d24b59bc7de12c60c813d740b2f79d92a7cc291f` passed [validate-github-actions #42230823573](https://github.com/phanthienquoc/platform-infra/actions/runs/42230823573) and [validate-manifests #42230823297](https://github.com/phanthienquoc/platform-infra/actions/runs/42230823297).
- The workload-health helper now distinguishes active workload health from intentionally zero-replica maintenance. It emits an explicit notice that no live workload health is asserted for maintenance scopes. Regression tests cover zero-only and mixed active/maintenance scopes.
- Post-merge `validate-github-actions` [#42230952977](https://github.com/phanthienquoc/platform-infra/actions/runs/42230952977) and `validate-manifests` [#42230952863](https://github.com/phanthienquoc/platform-infra/actions/runs/42230952863) both PASS.
- Post-merge push reconciliation [#42230952994](https://github.com/phanthienquoc/platform-infra/actions/runs/42230952994) completed SUCCESS with `ALLOW_IMAGE_CHANGES=false`; GitOps diff was clean and manifest apply was skipped. GHCR pull preflight passed; `ghcr-pull` was unchanged in checked namespaces. Auth runtime Secret provision/verification ran with values suppressed. TCE/Auth lanes verified zero-replica maintenance (not live health); MicroFE active workload health passed; Keycloak lane skipped.
- Recovery controller [#42231153001](https://github.com/phanthienquoc/platform-infra/actions/runs/42231153001) dispatched read-only inspection because the prior inspection snapshot was stale.
- Inspection [#42231216533](https://github.com/phanthienquoc/platform-infra/actions/runs/42231216533) generated a fresh snapshot at 14:08:18Z. Inspection PR [#1342](https://github.com/phanthienquoc/platform-infra/pull/1342), exact head `0e01eb7f5b04cb7f49409a7f490dbf6f1b57ee85`, passed [exact-head validate-manifests #42231396933](https://github.com/phanthienquoc/platform-infra/actions/runs/42231396933) and was squash-merged as `5824a4af4dd91e498134ea8eafd2e026725344c0`. PR #1342 changes inspection state only, not production manifests.

## Fresh K3s / host inspection — 2026-11-06 14:08:18 UTC

- Host is Ubuntu 22.04.5 LTS, ARM64; K3s node `tce-k3s-01` is Ready on v1.36.3+k3s1, containerd 2.3.2-k3s2.
- Memory: 23 GiB total, about 19 GiB available. Root disk: 45 GiB total, 25 GiB used (56%), normal pressure.
- `restart_required=yes`; 37 package updates were listed, including containerd 2.4.2 and Docker 29.9.3. Do not upgrade or reboot automatically; this requires a separately approved maintenance window.
- Both dedicated runners are still active and enabled: Platform `actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service` and Media `actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service`. Both Listener processes remain. Media runner retirement is blocked; never unregister the shared Platform runner.
- Media backend/frontend: 1/1 Running, digest-pinned.
- MicroFE Shell/WS/NATS: Running and healthy.
- Stock Admin: two Pods in ImagePullBackOff; new Stock Backend Pod in ImagePullBackOff. Legacy Backend and Frontend Pods are 1/1 Running.
- Stock Admin/new Backend tag `12d63b4` fails with `no match for platform in manifest`; this is missing linux/arm64 manifest evidence, not a GHCR credential failure.
- TCE frontend/service, Auth `microfe-auth`, and Keycloak are all desired 0/0. Public OIDC probes to both SSO realms return HTTP 503. Keep strict public HTTP 200 checks; do not treat zero-replica lane success as live service health and do not activate without service-owner approval.
- GitOps drift is clean. Persistent storage inventory shows only unrelated `k3s-debug/k3s-debug-logs` PVC/PV. No Stock/Media PVC/PV or VolumeSnapshot references were found.
- No K3s warning events were recorded in the last two hours. External database/object storage, backups, retention and DNS ownership are not established by this inspection.

The inspection snapshot is current for K3s workload, storage-reference and runner state. It is not a backup proof or destructive authorization; external-data ownership and recovery evidence remain separate gates.

## Native schedule evidence

Only `event=schedule` runs count as native schedule proof.

| Workflow | Latest native run in inspected history | Result |
|---|---|---|
| Platform reconcile | #42199267592, 10:00:15Z | PASS |
| Platform recovery | #42199274660, 10:00:18Z | PASS |
| Platform watchdog | #42201400071, 10:16:28Z | PASS |
| Platform inspect | #42193617816, 09:15:08Z | PASS, now superseded for runtime snapshot purposes by manual inspect #42231216533 |
| TCE WF-06 | #42176208184, 06:43:04Z | FAIL, four public HTTP 503 probes |
| TCE WF-07 | #42176751608, 06:48:12Z | PASS |
| TCE WF-12 | #42211610532, 11:37:17Z | FAIL, WF-06 native run 294 minutes old vs 25-minute budget |

Platform push reconcile #42230952994 and manual inspect #42231216533 are not native schedule events. TCE WF-13 #42211627712 is `workflow_run`; fallback WF-06 #42211645157 is `workflow_dispatch`. These do not refresh native schedule freshness. No cron or TCE market-scan schedule was changed.

## Immutable publication status

- Stock publisher [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933), source SHA `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`, is older than current Stock master. Current ARM64 CI is build-only. Manual publication remains gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`.
- Media publisher [#41158598649](https://github.com/phanthienquoc/media-generation/actions/runs/41158598649), source SHA `32f3bf56e1f44c65a5d98f35bed0547f398f8e90`, is older than current Media master. No new publisher or Platform dispatch observed.
- Auth publisher [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320), source SHA `ceb2688d6277b10f1bfe7652223d1d295b7e49d9`, predates current master and the merged non-master release-ref gate. No new publisher was triggered.
- No current-master Stock/Media/Auth publisher run, digest/provenance pair or new release authorization was observed. Do not promote old tags.

## Ownership and next actions

App repositories own tests, builds and immutable GHCR publication. Platform Infra owns production manifests, shared pull credentials, provenance/digest validation, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose production authority was added.

1. Investigate TCE native WF-06/WF-12 schedule delivery separately from the expected 0/0 maintenance health state. Preserve existing cron and strict HTTP 200.
2. Obtain explicit Stock release authorization before any publisher run; require current full-source-SHA, digest, provenance and linux/arm64 manifest before a separate Platform promotion.
3. Retire Media runner only after operator confirms it is idle, then stop/disable/unregister that dedicated runner and verify no Listener remains.
4. Require independent external database/object-storage backup, retention and DNS ownership review before any Stock/Media namespace decommission.
5. Keep TCE/Auth at 0/0 until service owners authorize activation. Do not reboot or upgrade K3s without a separate maintenance window.

No namespace, PVC/PV, workload, image, replica, DNS, external database, runner or host was deleted or reconfigured by this checkpoint. The post-merge reconcile did provision/verify the Auth runtime Secret and confirmed shared GHCR pull Secrets unchanged. TCE market-scan schedule unchanged.


---

## Cross-repo runtime checkpoint — 2026-11-06 21:56 ICT / 14:56 UTC

This checkpoint follows a fresh read of all five default branches, open PRs, recent Actions runs, the workflow inventory, the deployment tracker, the current TCE schedule declarations, and the latest committed K3s inspection plus a newer read-only pod listing from reconciliation. It records evidence only; no image publication, image promotion, workload activation, runner retirement, namespace deletion, reboot, or external-data deletion was authorized.

### Current default-branch heads and open PRs

| Repository | Current master SHA | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | 2afad0630d9f18cadd5ec238eb0fd6efcc4adca2 | #1314, #544, #541, #539 (all drafts) | Current manifest validation [#42231791306](https://github.com/phanthienquoc/platform-infra/actions/runs/42231791306) PASS. Latest reconcile is a manual dispatch; native schedule history is stale. |
| TCE Dashboard | f4240ada56da700af00100fb3f01278b9b883951 | None | PR #1027 merged; publisher permission scope tightened. Native WF-06 still fails public HTTP 503; WF-12 native schedule remains stale. |
| StockDividend | 3aeaf519b7a786d13dcecee763acaca357c47ddd | None | CI #42167088130 PASS 7/7, including non-publishing ARM64 builds. No new publisher run. |
| Media Generation | 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d | None | PR #73 merged; exact-head CI and post-merge master CI pass. No new publisher run. |
| Authentication | 3b60ff46b8959d18aee1956f99d6b62589b8b9c5 | #75 ready; #76 draft | CI #42215394539 PASS. No current-master release publisher. |

Auth #75 remains 28 commits ahead / 13 behind master; #76 remains 3 ahead / 13 behind. Their historical checks do not authorize merge. Keep both gated until they are reconciled to current master and Supabase production integration/migration side effects are reviewed.

### Completed app-repository permission hardening

**Media Generation — PR [#73](https://github.com/phanthienquoc/media-generation/pull/73)**

- Dedicated branch: fix/media-ghcr-publish-permissions-scope-20261106-2156ict.
- Exact head 32987344e8ebc10890376f4fb371a33c4160906a passed [Media CI #42238974848](https://github.com/phanthienquoc/media-generation/actions/runs/42238974848): release-contract validator, backend tests, frontend/backend typecheck and build all passed.
- Squash-merged as 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d; post-merge master CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) PASS.
- WF-03 now has only workflow-level contents: read; packages: write is scoped to publish-immutable-images. The release-contract validator asserts there is exactly one package-write grant and that it is inside the publisher job.
- Full-SHA release tags, checksum-verified artifacts, ARM64 manifest verification, publisher ownership and the explicit no-Platform-dispatch boundary are unchanged. No publisher was run and no image was pushed.

**TCE Dashboard — PR [#1027](https://github.com/phanthienquoc/TCE-dashboard/pull/1027)**

- Dedicated branch: fix/tce-ghcr-write-permissions-scope-20261106-2156ict.
- Exact head 6ae103e0d6ea4b4db7e727f20275b535b81df120 passed all PR checks:
  - [WF-01P #42239660880](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239660880) PASS, including TCE release-contract validation and frontend build.
  - [WF-08B #42239660838](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239660838) PASS, including MicroFE Auth/WS tests and the Shell/WS payload plus permission-scope regression.
  - [Backend unit tests #42239660759](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239660759) PASS.
  - [Prettier #42239660758](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239660758) PASS.
- Squash-merged as f4240ada56da700af00100fb3f01278b9b883951.
- WF-03 now has workflow-level contents: read; actions: read and packages: write are scoped to platform-infra-release only.
- WF-08B now has workflow-level contents: read; packages: write is granted only to the two publishing jobs (build-shell, build-ws). Test, handoff-validation and dispatch/verification jobs do not receive package-write permission.
- Regression checks were added to the existing TCE release validator and WF-08B PR test. Manual-only TCE WF-03, full-SHA/digest/ARM64 release checks, provenance-bound dispatch payload and the Shell/WS-only boundary remain intact.
- Post-merge push validation: backend unit tests [#42239871781](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239871781) PASS; Prettier [#42239871823](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239871823) PASS. WF-01 build/verify [#42239871779](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239871779) was still in progress at 14:56Z after release-contract and secret-presence checks passed. No production publisher or dispatch was run.
- WF-06 and WF-12 cron declarations were re-read after merge and remain */15 * * * * and 7,22,37,52 * * * *, respectively. TCE market-scan schedule is unchanged.

### Latest workflow and schedule evidence

Only event=schedule counts as native schedule evidence.

| Workflow | Latest native scheduled run observed | Result |
|---|---|---|
| Platform reconcile | [#42199267592](https://github.com/phanthienquoc/platform-infra/actions/runs/42199267592), 10:00:15Z | PASS |
| Platform recovery | [#42199274660](https://github.com/phanthienquoc/platform-infra/actions/runs/42199274660), 10:00:18Z | PASS |
| Platform watchdog | [#42201400071](https://github.com/phanthienquoc/platform-infra/actions/runs/42201400071), 10:16:28Z | PASS |
| Platform inspect | [#42193617816](https://github.com/phanthienquoc/platform-infra/actions/runs/42193617816), 09:15:08Z | PASS |
| TCE WF-06 | [#42235639842](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42235639842), 14:37:53Z | FAIL, all four public endpoints HTTP 503 |
| TCE WF-07 | [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608), 06:48:12Z | PASS |
| TCE WF-12 | [#42211610532](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42211610532), 11:37:17Z | FAIL, stale native WF-06 freshness |

- Platform reconcile [#42235712359](https://github.com/phanthienquoc/platform-infra/actions/runs/42235712359) at 14:38:22Z and recovery [#42235938727](https://github.com/phanthienquoc/platform-infra/actions/runs/42235938727) at 14:39:57Z are workflow_dispatch, not native schedule proof.
- TCE WF-12 [#42235672509](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42235672509) and WF-13 [#42235672609](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42235672609) were workflow_run events following the scheduled WF-06. They are not native WF-12 schedule delivery.
- The scheduled WF-06 run is recent, but its four independent jobs failed because tce.mrcute.space, /api/health, auth.mrcute.space/api/health and /api/ready returned HTTP 503 where HTTP 200 is required. Do not weaken the status assertion.
- The latest native Platform schedule events remain several hours old at this checkpoint. Do not count push, manual dispatch, workflow_run or repository_dispatch fallback as schedule freshness. The read-only history does not establish whether this is GitHub scheduler delay or Actions policy/configuration.

### K3s and production reconciliation evidence

**Full read-only inspection:** [inspect-vps #42231216533](https://github.com/phanthienquoc/platform-infra/actions/runs/42231216533), snapshot generated 2026-11-06 14:08:18Z and committed in debug/vps-latest.md.

- Node tce-k3s-01 is Ready, ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; Ubuntu 22.04.5 LTS.
- Root disk 45 GiB, 25 GiB used (56%); memory 23 GiB total, about 19 GiB available. restart_required=yes; Docker/containerd and OS updates are pending. Do not upgrade or reboot without a separate maintenance window.
- Platform and Media runner services are both active/enabled; both Listener processes are present. Never retire the shared Platform runner. Media retirement remains blocked until operator confirms idle state and approves stop/disable/unregister.
- Persistent storage lists only unrelated k3s-debug/k3s-debug-logs PVC/PV. No Stock/Media PVC/PV or VolumeSnapshot references were found. This is not evidence of external database/object-storage backup, retention or DNS ownership.

**Newer partial runtime listing:** reconcile [#42235712359](https://github.com/phanthienquoc/platform-infra/actions/runs/42235712359), pod listing at 14:38:47Z.

- Node remains Ready, ARM64, K3s v1.36.3+k3s1.
- Media backend/frontend are 1/1 Running; MicroFE Shell/WS/NATS are running.
- Stock Admin has two Pods in ImagePullBackOff; the new Stock Backend Pod is also ImagePullBackOff. Legacy Stock Backend and Frontend are 1/1 Running.
- Failing Admin/new Backend tag 12d63b4 explicitly reports no match for platform in manifest; this is missing linux/arm64 manifest evidence, not a shared GHCR credential failure.
- TCE frontend/service, Auth and Keycloak are desired 0/0. The zero-replica helper reports intentional maintenance and explicitly does not assert live health.
- Reconcile was mode=apply, target_app=all, ALLOW_IMAGE_CHANGES=false; shared ghcr-pull Secret was unchanged, Auth runtime Secret was provisioned/verified with values suppressed, TCE GitOps image pairing passed for prod-v0.1.0-e75e338, Kubernetes diff was clean and manifest apply was skipped. MicroFE active health passed; Keycloak lane was skipped. This was not a new rollout or image promotion.

### Immutable publication status

- Stock publisher [#41563856933](https://github.com/phanthienquoc/stockdividend/actions/runs/41563856933) is from Nov 3 and predates current Stock master. Current ARM64 CI #42167088130 is build-only. Manual publication remains gated by STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true; no current-master digest/provenance or release authorization was observed.
- Media publisher [#41158598649](https://github.com/phanthienquoc/media-generation/actions/runs/41158598649) is from Oct 31 and predates current Media master. PR #73 changed only permission scope and regression validation; no image was published.
- Auth publisher [#41040510320](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/41040510320) is from Oct 30 and predates current master/release gate. No new manual release or provenance-bound dispatch was observed.
- TCE WF-03 remains manual-only; no production publisher was triggered. TCE #1027 changed only job token permissions and regression validation.
- Do not promote old tags or reuse historical digests as current release evidence.

### Ownership and next dependency-safe actions

App repositories own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, source-run provenance/digest verification, GitOps promotion/reconciliation, rollout and health. reconcile-vps.yml remains the sole production apply authority; inspect-vps.yml remains read-only. No duplicate direct SSH/Compose production authority was introduced.

1. Investigate native TCE WF-06/WF-12 and Platform schedule delivery independently; preserve all current cron and TCE market-scan schedule declarations.
2. Keep TCE/Auth at 0/0 until service owners authorize activation; retain strict public HTTP 200.
3. Stock: require explicit release authorization, then publish current full-source-SHA images, verify registry digest/provenance and linux/arm64 before a separate Platform promotion.
4. Media: retire only the dedicated runner after operator confirms idle; stop/disable/unregister and verify no Listener remains.
5. Require same-window storage preflight plus external database/object-storage backup, retention and DNS ownership review before protected Stock/Media decommission.
6. Keep Auth #75/#76 gated until reconciled to current master and Supabase production side effects/migration are verified.
7. Schedule OS/container updates and reboot only through a separately approved maintenance window.

No workload, image, desired replica, production manifest, namespace, PVC/PV, external database, DNS, runner or host was deleted or reconfigured. The latest reconcile did provision/verify the Auth runtime Secret; shared GHCR pull Secret remained unchanged. TCE market-scan schedule unchanged.


---

## Incremental readiness update — 2026-11-06 22:11 ICT / 15:11 UTC

- Platform Infra PR [#1344](https://github.com/phanthienquoc/platform-infra/pull/1344) merged as b153defe812c20e53904ebc6ea669cdfc7654af5. Exact-head manifest validation [#42240425538](https://github.com/phanthienquoc/platform-infra/actions/runs/42240425538) PASS; post-merge validation [#42240709818](https://github.com/phanthienquoc/platform-infra/actions/runs/42240709818) PASS. It changed only tracker/inventory/checkpoint documentation.
- Stock PR [#34](https://github.com/phanthienquoc/stockdividend/pull/34) is open on branch fix/stock-ghcr-write-permissions-scope-20261106-2156ict, exact head 1dd618e42d7fb64fe048bbffc53c55eb20f3a37a, 2 commits ahead and 0 behind master. It adds workflow-level contents: read to deploy.yml and keeps packages: write only on build-and-push; the release-contract validator enforces the single publisher grant. PR CI [#42240653857](https://github.com/phanthienquoc/stockdividend/actions/runs/42240653857) was still in progress at 15:11Z: release-contract, backend test/build and scraper syntax jobs passed; ARM64 image builds, scraper container build and Admin build were still running. Do not merge until every required job passes on this exact head.
- TCE PR #1027 merged as f4240ada56da700af00100fb3f01278b9b883951. Exact-head WF-01P #42239660880, WF-08B #42239660838, backend unit tests #42239660759 and Prettier #42239660758 all passed. Post-merge WF-01 build/verify #42239871779, backend unit tests #42239871781 and Prettier #42239871823 all passed.
- Media PR #73 merged as 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d. Exact-head CI #42238974848 and post-merge master CI #42239703151 passed.
- Current heads: Platform b153defe812c20e53904ebc6ea669cdfc7654af5; TCE f4240ada56da700af00100fb3f01278b9b883951; Stock 3aeaf519b7a786d13dcecee763acaca357c47ddd; Media 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d; Auth 3b60ff46b8959d18aee1956f99d6b62589b8b9c5. Open PRs: Platform #1314/#544/#541/#539 drafts; Stock #34; Auth #75 ready/#76 draft; none in TCE or Media.
- GitHub Status summary was All Systems Operational at 14:29:25Z, with Actions marked operational and no unresolved incidents. The history lists resolved Actions incidents on Nov 5 and early Nov 6, but these do not establish the cause of the later native schedule gaps. Do not attribute schedule failures to GitHub without stronger evidence: https://www.githubstatus.com/history

Stock #34 changes only GITHUB_TOKEN permission defaults and regression validation. It does not change publication triggers, manual release authorization, immutable SHA tags, ARM64 verification, Platform handoff, production manifests or runtime state. No Stock publisher was triggered and no GHCR image was pushed.

The latest full K3s inspection remains #42231216533 (14:08:18Z); the newer partial pod listing is reconcile #42235712359 (14:38:47Z). Neither authorizes decommission. Media runner is still active/enabled with Listener present; Stock Admin/new Backend still lack ARM64 manifest for tag 12d63b4; TCE/Auth/Keycloak remain 0/0. External database/object-storage backup, retention and DNS ownership remain unverified.

TCE WF-06/WF-12 cron declarations and the TCE market-scan schedule remain unchanged. No production workload, image, replica, manifest, namespace, PVC/PV, external data, DNS, runner or host was changed by the documentation checkpoint.


---

## Cross-repo permission audit completion — 2026-11-06 22:15 ICT / 15:15 UTC

- Stock PR [#34](https://github.com/phanthienquoc/stockdividend/pull/34) merged as bc20dcfb9893ea246a5e46bef26cce1c92a940c9. Exact head 1dd618e42d7fb64fe048bbffc53c55eb20f3a37a passed all seven jobs in [CI #42240653857](https://github.com/phanthienquoc/stockdividend/actions/runs/42240653857), including the release-contract validator, Go test/build, Admin build, scraper validation/container build, and all three non-publishing native ARM64 image builds. The workflow-level default is now contents: read; packages: write exists only on build-and-push.
- Post-merge Stock CI [#42241252700](https://github.com/phanthienquoc/stockdividend/actions/runs/42241252700) was queued/in progress at 15:15Z. The deploy workflow has paths-ignore for .github/** and the release validator, so this permission-only merge is not a production publication trigger. No new deploy/publisher run or GHCR image push was observed.
- Platform PR #1345 merged as 6d08b835ddee5fe5324fe68fa825fac1a42cf43a. Exact-head validation #42241066054 PASS; post-merge validation [#42241159907](https://github.com/phanthienquoc/platform-infra/actions/runs/42241159907) PASS.
- Current default-branch heads: Platform 6d08b835ddee5fe5324fe68fa825fac1a42cf43a; TCE f4240ada56da700af00100fb3f01278b9b883951; Stock bc20dcfb9893ea246a5e46bef26cce1c92a940c9; Media 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d; Auth 3b60ff46b8959d18aee1956f99d6b62589b8b9c5.
- Open PRs: Platform #1314/#544/#541/#539 (draft); Auth #75 ready/#76 draft; none in TCE, Stock or Media.
- The app-repository GHCR permission audit is now complete: Stock deploy.yml, Media WF-03, TCE WF-03/WF-08B and Auth release.yml all use read-only workflow defaults and scope packages: write to only the image-publishing job(s). TCE WF-03 also scopes actions: read to its publisher/handoff job. Each app retains its release/provenance/ARM64 contract; no app-to-Platform direct production authority was added.

### Current native schedule and runtime state

- Latest Platform native schedule history: reconcile #42199267592 at 10:00:15Z PASS; recovery #42199274660 at 10:00:18Z PASS; watchdog #42201400071 at 10:16:28Z PASS; inspect #42193617816 at 09:15:08Z PASS. Later reconcile #42235712359 and recovery #42235938727 are manual dispatches, not schedule proof.
- Latest TCE native schedule history: WF-06 #42235639842 at 14:37:53Z FAIL (four HTTP 503 probes); WF-07 #42176751608 at 06:48:12Z PASS; WF-12 #42211610532 at 11:37:17Z FAIL (stale native WF-06 freshness). WF-12 #42235672509 and WF-13 #42235672609 are workflow_run follow-ups, not native schedule events. No newer native schedule events appeared in the latest 100-run histories.
- GitHub Status summary at 14:29:25Z showed Actions operational and no unresolved incidents. Resolved Nov 5/early Nov 6 incidents do not establish the cause of subsequent schedule gaps.
- Full K3s inspection remains #42231216533 at 14:08:18Z; partial reconcile pod listing #42235712359 at 14:38:47Z. Node Ready/ARM64; Media and MicroFE active workloads running; Stock Admin/new Backend ImagePullBackOff because tag 12d63b4 lacks linux/arm64 manifest; TCE/Auth/Keycloak desired 0/0. Media runner remains active/enabled with Listener present. Only unrelated debug PVC/PV; no Stock/Media PVC/PV or VolumeSnapshot references. External database/object-storage backup, retention and DNS ownership remain unverified.
- Reconcile #42235712359 used ALLOW_IMAGE_CHANGES=false, verified shared GHCR pull access, left ghcr-pull unchanged, provisioned/verified Auth runtime Secret with values suppressed, passed TCE image pairing, found clean GitOps diff and skipped manifest apply. No new rollout or image promotion.

No image publisher was run for Stock, Media, TCE or Auth. Historical publishers remain older than current master; do not promote old tags or digests. TCE/Auth stay at 0/0 until service-owner activation approval; public HTTP 200 checks remain strict. Media runner retirement and Stock/Media decommission remain blocked by operator idle confirmation and external-data/backup/DNS ownership review. Host package upgrades/reboot require a separate maintenance window.

TCE WF-06/WF-12 cron declarations and TCE market-scan schedule unchanged. No production workload, image, replica, manifest, namespace, PVC/PV, external data, DNS, runner or host was changed by the permission audit. The latest reconcile did provision/verify the Auth runtime Secret; shared GHCR pull Secret remained unchanged.


---

## Cross-repo readiness checkpoint — 2026-11-06 23:01 ICT / 16:01 UTC

### Repository heads and open PRs

| Repository | Default-branch head | Open PRs | Latest relevant CI evidence |
|---|---|---|---|
| Platform Infra | `1dbe10b330cd4f5ba2a271323e13cbf49cc47bcd` | #1314/#544/#541/#539 (all drafts; unrelated mail/Keycloak planning) | Manifest validation [#42241598526](https://github.com/phanthienquoc/platform-infra/actions/runs/42241598526) PASS; PR validation #42241494591 PASS. |
| TCE Dashboard | `f4240ada56da700af00100fb3f01278b9b883951` | None | WF-01 #42239871779, backend #42239871781, Prettier #42239871823 all PASS on master. |
| StockDividend | `bc20dcfb9893ea246a5e46bef26cce1c92a940c9` | None | Stock CI [#42241252700](https://github.com/phanthienquoc/stockdividend/actions/runs/42241252700) PASS on current master; exact-head PR CI #42240653857 passed 7/7. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | Media CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) PASS on current master; exact-head PR CI #42238974848 PASS. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | Auth CI [#42215394539](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215394539) PASS on master. Both PRs target stale base SHA `2189c97252bfe7ee53f50a68cf51008fa0d27c91`; do not merge without branch reconciliation and fresh checks. |

### Native scheduled delivery — current evidence and gaps

The Actions API was queried with `event=schedule` for both Platform Infra and TCE Dashboard. Manual dispatch and workflow_run events are excluded from this table.

| Repository / workflow | Latest native scheduled run | Result | Current interpretation |
|---|---|---|---|
| Platform reconcile-vps | [#42199267592](https://github.com/phanthienquoc/platform-infra/actions/runs/42199267592), 2026-11-06 10:00:15Z | PASS | No newer native schedule event in the returned 100-run history; later reconcile #42235712359 was manual. |
| Platform recovery | [#42199274660](https://github.com/phanthienquoc/platform-infra/actions/runs/42199274660), 10:00:18Z | PASS | No newer native schedule event; later #42235938727 was manual. |
| Platform freshness watchdog | [#42201400071](https://github.com/phanthienquoc/platform-infra/actions/runs/42201400071), 10:16:28Z | PASS | No newer native schedule event in returned history. |
| Platform inspect-vps | [#42193617816](https://github.com/phanthienquoc/platform-infra/actions/runs/42193617816), 09:15:08Z | PASS | No newer native schedule event; later #42231216533 was a manually initiated inspection. |
| TCE WF-06 | [#42235639842](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42235639842), 14:37:53Z | FAIL | All four public probes returned HTTP 503; no later native schedule event in returned history. At 16:01:21Z this event was ~83 minutes old. |
| TCE WF-12 | [#42211610532](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42211610532), 11:37:17Z | FAIL | Watchdog found last WF-06 schedule #42176208184 at 06:43:04Z, age 294m at that run. No later native WF-12 schedule event in returned history. |
| TCE WF-07 | [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608), 06:48:12Z | PASS | No newer native schedule event in returned history. |

Current workflow source still declares TCE WF-06 `*/15 * * * *` and WF-12 `7,22,37,52 * * * *`. Platform reconcile-vps declares `7,22,37,52 * * * *`; inspect-vps declares `2,32 * * * *`. No cron or TCE market-scan schedule was changed. The API evidence establishes missing recent schedule events, but does not establish why GitHub did not enqueue them. Do not attribute the gaps to runner outage, GitHub incident or repository settings without new evidence.

### TCE endpoint failure evidence

- WF-06 #42235639842 ran on GitHub-hosted Ubuntu 24.04 runners; it was not blocked waiting for the Platform self-hosted runner.
- The captured Auth readiness log reports `https://auth.mrcute.space/api/ready` returned HTTP 503, expected 200.
- The captured TCE web log reports `https://tce.mrcute.space/` returned HTTP 503, expected 200.
- The other two matrix jobs, TCE API and Auth liveness, also concluded failure. The public health contract remains strict HTTP 200. TCE/Auth/Keycloak were last observed at intentional 0/0, so the 503s are consistent with maintenance but are not accepted as live health.
- WF-12 #42211610532 successfully dispatched the authenticated Platform schedule heartbeat; its verify job failed because the latest WF-06 native event was stale. Heartbeat/workflow_run follow-up is not a replacement for native schedule evidence.

### Production and K3s evidence freshness

- Latest full read-only K3s inspection remains [#42231216533](https://github.com/phanthienquoc/platform-infra/actions/runs/42231216533), generated 2026-11-06 14:08:18Z. The later reconcile #42235712359 provided a Pod listing at 14:38:47Z, but was not a full inspection.
- Last full snapshot: node Ready/ARM64, disk 56%, available RAM about 19 GiB, restart required. Media backend/frontend 1/1; MicroFE Shell/WS/NATS running; Stock Admin and newer Backend ImagePullBackOff; legacy Stock Backend/Frontend running; TCE/Auth/Keycloak desired 0/0; GitOps drift clean.
- Stock image pull events explicitly identify missing linux/arm64 manifest for tag `12d63b4` (`no match for platform in manifest`). This is not evidence of shared GHCR credential failure. Do not promote that tag.
- Reconcile #42235712359 used `ALLOW_IMAGE_CHANGES=false`, verified shared GHCR pull access, left `ghcr-pull` unchanged, provisioned/verified Auth runtime Secret with values suppressed, found clean GitOps diff and skipped manifest apply. No image rollout occurred.
- Media and Platform runner services were both active/enabled with Listener processes in the 14:08 snapshot. This is stale runner evidence; do not retire either runner from this snapshot. Shared Platform runner must never be unregistered as part of Media retirement.
- Kubernetes storage showed only unrelated debug PVC/PV; no Stock/Media PVC/PV or VolumeSnapshot references. External database/object-storage backup, retention and DNS ownership remain unverified.

### Immutable publication and ownership

- App-repo GHCR permission hardening is merged: TCE WF-03/WF-08B, Stock deploy.yml, Media WF-03 and Auth release.yml default to read-only permissions and scope `packages: write` to publishing jobs only.
- Latest publisher evidence remains old-source: Stock #41563856933 (Nov 3), Media #41158598649 (Oct 31), Auth #41040510320 (Oct 30). No current-master digest/provenance/ARM64 publication was verified. TCE WF-03 remains manual-only; no publisher or Platform dispatch was invoked.
- No production image change or promotion is authorized by this checkpoint. App repos own tests/builds/immutable GHCR publication. Platform owns production manifests, shared pull credentials, digest/provenance verification, GitOps promotion/reconciliation, rollout and health.
- `reconcile-vps.yml` remains the sole production apply authority. `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority was introduced.

### Next dependency-safe actions

1. Obtain a fresh read-only K3s/runner/storage inspection through the authorized Actions operator path; current full snapshot is over two hours old. Do not infer current pod or runner state from it.
2. Investigate GitHub native schedule delivery for Platform and TCE using repository Actions settings/organization policy and scheduler telemetry. Preserve all existing cron expressions, especially TCE WF-06 and market-scan schedules.
3. Keep TCE WF-06 strict HTTP 200 and TCE/Auth/Keycloak at maintenance state until service owners authorize activation; do not convert 503 to success.
4. Keep Stock image tag `12d63b4` blocked; require an authorized current full-source-SHA linux/arm64 publication with verified digest/provenance before any promotion.
5. Retire only the dedicated Media runner after a fresh idle confirmation and stop/disable/unregister verification; preserve shared Platform runner.
6. Verify external database/object-storage backup, retention and DNS ownership before any Stock/Media decommission.
7. Reconcile Auth #75/#76 to current master, inspect Supabase production side effects and rerun exact-head checks before considering merge.

No workflow, cron, publisher, GHCR push, Platform dispatch, production manifest, image, workload, replica, namespace, PVC/PV, external database, DNS, runner or host was changed by this checkpoint. TCE market-scan schedule unchanged.


---

## Cross-repo readiness checkpoint — 2026-11-07 00:03 ICT / 2026-11-06 17:03 UTC

This checkpoint supersedes the 23:01 ICT operational snapshot where newer evidence exists. It records the fresh inspect-vps snapshot, the schedule watchdog failure, and the verified workflow_dispatch recovery path. Native schedule evidence remains distinct from fallback evidence.

### Current default-branch heads and open PRs

| Repository | Default-branch head | Open PRs | Current disposition |
|---|---|---|---|
| Platform Infra | `3776186bad238683d2ee1f5c41c182c876edd21c` | #1314/#544/#541/#539 (draft) | Inspection-state update #1348 merged; latest operational watchdog reports stale native reconcile/recovery. |
| TCE Dashboard | `f4240ada56da700af00100fb3f01278b9b883951` | None | CI passes; native WF-06/WF-12 delivery stale and WF-06 probes fail HTTP 503. |
| StockDividend | `bc20dcfb9893ea246a5e46bef26cce1c92a940c9` | None | CI 7/7 passes, including non-publishing ARM64 builds; deployed tag 12d63b4 remains incompatible with ARM64. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI passes; dedicated runner remains active and not approved for retirement. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready; #76 draft | CI passes; Supabase Preview skipped and production integration/migration side effect remains unverified. |

Platform #1314 remains a mailbox planning draft; #544/#541/#539 remain Keycloak/identity planning drafts. Auth #75/#76 target stale base SHA `2189c97252bfe7ee53f50a68cf51008fa0d27c91`; do not merge without branch reconciliation and authoritative Supabase integration-side-effect review.

### Latest current-master checks

- Platform current head #3776186 has fresh operational run activity. Schedule watchdog #42256928371 failed on stale native reconcile/recovery freshness; reconcile fallback #42256950100 and recovery #42257152475 succeeded. Manifest validation #42256836967 was on the inspection PR branch, not current master.
- TCE WF-01 #42239871779, WF-05 #42239871781, WF-02 #42239871823 passed on current master.
- Stock CI #42241252700 passed 7/7 on current master.
- Media CI #42239703151 passed on current master.
- Auth CI #42215394539 passed validation and non-publishing ARM64 build; Supabase Preview was skipped.

### Native scheduled delivery

| Workflow | Latest native scheduled run | Result |
|---|---|---|
| Platform inspect-vps | #42256652947, 16:54:09Z | PASS |
| Platform reconcile-vps | #42199267592, 10:00:15Z | PASS but 415m stale at watchdog |
| Platform recover-stale-ops | #42199274660, 10:00:18Z | PASS but 415m stale at watchdog |
| Platform schedule watchdog | #42201400071, 10:16:28Z | PASS but no newer native run |
| TCE WF-06 | #42235639842, 14:37:53Z | FAIL; HTTP 503 |
| TCE WF-12 | #42211610532, 11:37:17Z | FAIL; stale WF-06 freshness |
| TCE WF-07 | #42176751608, 06:48:12Z | PASS |

Platform watchdog workflow_run #42256928371 confirmed the native inspect event was fresh but failed reconcile/recovery freshness (both latest native events were 415m old against 45m budgets). The TCE observer warned WF-06 was 8,283 seconds old against a 1,500-second budget. This is an operational schedule-delivery signal, not a reason to weaken the gate. No cron was changed.

### Fallback reconciliation evidence

Recovery workflow_run #42256928538 dispatched the existing `reconcile-vps.yml` authority using exact payload `ref=master`, source SHA `3776186bad238683d2ee1f5c41c182c876edd21c`, `mode=apply`, `allow_image_changes=false`, `target_app=all`. It correlated the request to #42256950100.

Reconcile #42256950100 passed GHCR pull preflight, provisioned/verified Auth runtime Secret with values suppressed, left shared `ghcr-pull` unchanged, found no MicroFE/TCE image-pull failures, found clean GitOps diff and correctly skipped manifest apply. Image changes were disabled; no promotion occurred. TCE/Auth maintenance and MicroFE active health gates passed; Keycloak lane skipped. Recovery after reconcile #42257152475 succeeded. None of these workflow_dispatch/workflow_run events count as native schedule recovery.

### Fresh K3s state

Read-only inspect #42256652947 generated `debug/vps-latest.md` at 16:54:18Z. Node Ready/ARM64; K3s v1.36.3+k3s1; containerd 2.3.2-k3s2; disk 56% (21 GiB available of 45 GiB); RAM 23 GiB total/19 GiB available; host uptime about 189 days; `restart_required=yes`. Pending containerd/Docker upgrades require a separate approved maintenance window.

Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 Running. Stock Admin has two ImagePullBackOff pods; the new Backend is ImagePullBackOff; older Backend/Frontend run. The Stock failure explicitly says no linux/arm64 manifest for tag `12d63b4`, not an authentication failure. TCE/Auth/Keycloak are 0/0 maintenance. GitOps drift is clean. Platform and Media runners are active/enabled with Listener processes; no idle confirmation, so no retirement. No Stock/Media VolumeSnapshot references were listed; external backup/retention/DNS ownership remain unverified.

### Immutable publication and ownership

No current-master Stock/Media/Auth GHCR publication with verified digest/provenance was observed; TCE WF-03 remains manual-only. No publisher or promotion was triggered. App repos retain CI/build/immutable publication ownership; Platform retains manifests, shared pull credentials, digest/provenance verification, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only apply authority; `inspect-vps.yml` is read-only.

Next actions: investigate native schedule delivery without cron edits; keep TCE/Auth/Keycloak maintenance and strict HTTP 200; require authorized Stock ARM64 publication before promotion; reconcile Auth PRs and verify Supabase side effects; retire only the dedicated Media runner after operator idle confirmation; verify external backups/DNS before decommission; schedule host updates/reboot separately.

TCE market-scan schedule unchanged. The verified production secret operation was Auth runtime Secret provision/verification; shared GHCR pull Secret remained unchanged. No image, manifest, namespace, PVC/PV, external data, DNS, runner or host was deleted or reconfigured.


---

## Post-merge deployment contract update — 2026-11-07 00:13 ICT / 2026-11-06 17:13 UTC

Platform PR #1349 merged as `4267436fdc16232ccfa832e0dc83544e96516eac`; post-merge validation #42259072387 passed. Platform PR #1351 merged as `d083613ecf5a064d0c60d019ff2c173d87e68791`; exact-head and post-merge `validate-github-actions` #42259386872/#42259545328 and `validate-manifests` #42259387019/#42259545139 all passed. Duplicate PR #1350 was closed after the same change was rebased into #1351.

The guarded manual Stock/Media decommission workflow now defaults to read-only `mode=plan`, which reports runner state and runs namespace/storage inventory without deletion attestations or the production Environment. `mode=delete` remains separate and requires the production Environment, three exact operator attestations, verified Media runner retirement, a fresh same-run storage preflight and deletion limited to the two retired namespaces. The workflow remains manual-only. CI validated the contract, but plan mode was not dispatched against K3s in this checkpoint.

Stock/Media GitOps ownership is intentionally retired; do not restore their production manifests or app-to-Platform dispatches. Their app repositories remain source/CI/build/immutable publisher repositories. The namespaces still exist in K3s and must remain until the manual decommission gates are satisfied. The latest snapshot #42256652947 still shows the dedicated Media runner active and Stock tag `12d63b4` lacking linux/arm64 manifest.

Native Platform reconcile/recovery schedules and TCE WF-06/WF-12 remain stale; successful workflow_run/workflow_dispatch fallback is not native schedule proof. TCE WF-06 remains strict HTTP 200 and returns HTTP 503. No cron changed; TCE market-scan schedule unchanged.

Next: exercise plan mode read-only; resolve operator backup/external-data/DNS and runner-idle gates before deletion; investigate native schedule delivery without cron edits; require authorized Stock ARM64 digest/provenance before promotion; keep Auth PRs gated pending Supabase side-effect review.


---

# Cross-repo readiness checkpoint — 2026-11-07 00:56 ICT / 2026-11-06 17:56 UTC

This checkpoint supersedes older schedule/readiness observations where newer evidence exists. Native scheduled events are kept separate from workflow_run and workflow_dispatch fallback events. No cron, TCE market-scan schedule, image publication, image promotion, workload activation, runner retirement, namespace deletion, external-data deletion or host maintenance was authorized.

## Default-branch heads, PRs and current CI

| Repository | Default branch SHA | Open PRs | Latest current-master CI evidence |
|---|---|---|---|
| Platform Infra | `4857d666d92c96711ce7d397ec0f4019651f9ecb` | #1314/#544/#541/#539 (draft planning PRs) | PR #1352 post-merge validation [#42259845104](https://github.com/phanthienquoc/platform-infra/actions/runs/42259845104) PASS. Latest scheduled operational runs below. |
| TCE Dashboard | `f4240ada56da700af00100fb3f01278b9b883951` | None | WF-01 [#42239871779](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239871779), backend [#42239871781](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239871781), Prettier [#42239871823](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42239871823) PASS. |
| StockDividend | `bc20dcfb9893ea246a5e46bef26cce1c92a940c9` | None | CI [#42241252700](https://github.com/phanthienquoc/stockdividend/actions/runs/42241252700) PASS, 7/7 jobs. |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI [#42239703151](https://github.com/phanthienquoc/media-generation/actions/runs/42239703151) PASS. |
| Authentication | `3b60ff46b8959d18aee1956f99d6b62589b8b9c5` | #75 ready, #76 draft | CI [#42215394539](https://github.com/phanthienquoc/phanthienquoc-authentication/actions/runs/42215394539) PASS. PRs remain gated by stale base/Supabase deployment side-effect uncertainty. |

## Native schedule delivery — Platform recovery verified

Actions history was queried by event type; only `event=schedule` counts as native delivery.

| Platform workflow | Latest native run | Result |
|---|---|---|
| reconcile-vps | [#42261665655](https://github.com/phanthienquoc/platform-infra/actions/runs/42261665655), 17:26:34Z | PASS |
| recover-stale-ops | [#42261712724](https://github.com/phanthienquoc/platform-infra/actions/runs/42261712724), 17:26:53Z | PASS |
| reconcile schedule watchdog | [#42263224767](https://github.com/phanthienquoc/platform-infra/actions/runs/42263224767), 17:36:43Z | PASS |
| inspect-vps | [#42256652947](https://github.com/phanthienquoc/platform-infra/actions/runs/42256652947), 16:54:09Z | PASS; still within the 75-minute watchdog freshness budget at 17:36Z (42m old). |

The successful native reconcile and recovery events replace the older 10:00Z schedule observations. The 17:36Z watchdog log explicitly verified both native schedule runs and the latest scheduled inspection. This is a verified recovery of Platform native scheduled delivery, not merely a workflow_dispatch fallback.

The same watchdog emitted a warning-only TCE observation: latest native WF-06 [#42235639842](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42235639842) was 10,730 seconds old against a 1,500-second (25-minute) budget. TCE native WF-12 remains [#42211610532](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42211610532) FAIL; WF-07 remains [#42176751608](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42176751608) PASS. WF-06's four public endpoints still fail strict HTTP 200. The Platform observer is warn-only and cannot trigger TCE production recovery.

No cron expressions changed. TCE WF-06 remains `*/15 * * * *`; WF-12 and Platform reconcile schedules remain as committed. TCE market-scan schedule unchanged.

## Scheduled reconciliation evidence

Reconcile [#42261665655](https://github.com/phanthienquoc/platform-infra/actions/runs/42261665655) ran with `mode=apply`, `ALLOW_IMAGE_CHANGES=false`:

- GHCR pull access verified for Auth, MicroFE Shell/WS and TCE web/service packages.
- Auth runtime Secret was provisioned and verified; values were suppressed.
- Shared `ghcr-pull` Secret was unchanged in both checked namespaces.
- Core MicroFE/TCE image-pull restart check found no blocked pulls.
- TCE GitOps release pairing passed.
- K3s node reported Ready, ARM64, K3s v1.36.3+k3s1.
- GitOps diff was clean; manifest apply was correctly skipped.
- MicroFE active health passed; TCE/Auth zero-replica maintenance semantics passed without asserting live service health; Keycloak lane skipped.
- Stock Admin (two Pods) and new Backend remained ImagePullBackOff on tag `12d63b4`; this tag has no linux/arm64 manifest. Do not treat it as a pull-credential failure or promote it.

No image was published/promoted and no manifest rollout occurred.

## Latest K3s / runner / storage evidence

Full read-only snapshot [#42256652947](https://github.com/phanthienquoc/platform-infra/actions/runs/42256652947) generated `debug/vps-latest.md` at 16:54:18Z (about 62 minutes old at this checkpoint):

- Node Ready/ARM64; K3s v1.36.3+k3s1; disk 56% with about 21 GiB free; about 19 GiB RAM available; host still reports `restart_required=yes`.
- Media backend/frontend 1/1 Running; MicroFE Shell/WS/NATS running.
- Stock Admin and new Backend ImagePullBackOff due missing ARM64 manifest for `12d63b4`; legacy Backend/Frontend remain running.
- TCE/Auth/Keycloak are 0/0 maintenance; GitOps drift clean.
- Platform and dedicated Media runner services were active/enabled with Listener processes in this snapshot. This is not an idle/retirement confirmation; never unregister the shared Platform runner.
- Only the unrelated debug PVC/PV was listed; no Stock/Media PVC/PV or VolumeSnapshot references. External DB/object-storage backups, retention approval and DNS ownership remain unverified.

The snapshot is within the watchdog's 75-minute freshness budget at this checkpoint, but it is not a same-run decommission preflight. The new decommission `mode=plan` was not dispatched; no namespace/runner deletion was performed.

## Publication, promotion and ownership

No new current-master immutable GHCR publication/digest/provenance was observed for Stock, Media or Auth. TCE WF-03 remains manual-only. Latest CI runs are not publisher evidence. No publisher, repository dispatch or Platform promotion was invoked.

App repos own tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared pull credentials, provenance/digest verification, GitOps promotion/reconciliation, rollout and health. Stock/Media production GitOps manifests and app-to-Platform deployment handoffs remain intentionally retired. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority was added.

## Next dependency-safe actions

1. Continue observing Platform native reconcile/recovery/watchdog delivery; the 17:26Z and 17:36Z native runs are now verified successful.
2. Keep TCE WF-06/WF-12 blocked on stale native schedule/HTTP 503; retain strict HTTP 200 and do not change cron or market-scan.
3. Obtain a fresh authorized read-only K3s/runner/storage plan before any decommission; operator must confirm dedicated Media runner idle before stop/disable/unregister.
4. Require independent external DB/object-storage backup, retention and DNS ownership review before namespace deletion.
5. Stock: require release authorization and a current full-source-SHA linux/arm64 publication with immutable digest/provenance before any separate promotion.
6. Auth #75/#76: reconcile against current master and verify Supabase integration/migration side effects before merge.
7. Schedule Docker/containerd upgrades and reboot only in an approved maintenance window.

No production workload, image, replica, manifest, namespace, PVC/PV, external data, DNS, runner or host was deleted or reconfigured in this checkpoint. Auth runtime Secret provision/verification and read-only GHCR credential validation are recorded above. TCE market-scan schedule unchanged.
