## 2026-11-10 18:02 ICT — five-repository workflow inventory refresh

- Current master heads: Platform 53e43fc15ac58eab943c548f96ac781a831a59e3; TCE 0f71aa56eb728abbd87907e07739e08684b86724; Stock b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61; Media dcd698699c65ba6e73f6b43838975144777131c3; Authentication eab85fab32d7c9baef750c1fedbb93deb8c1333f.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 and Auth #76 (all draft). TCE, Stock and Media have no open PRs.
- Latest app CI remains green: TCE WF-01/WF-02/WF-05; Stock CI #42610360402; Media CI #42539512417; Auth CI #42654579277. Stock scraper #42457182511 remains fail-closed on missing VNSTOCK_API_KEY. Native TCE WF-06 #42799497774 fails all four strict public probes with HTTP 503; native WF-12 #42795292155 fails its stale-WF-06 delivery check.
- Platform native schedule evidence remains outside budget: reconcile #42778829676 age 11,170s/gap 25,539s; inspection #42749270072 age 27,474s/gap 24,367s; recovery #42777251549 age 11,967s/gap 26,068s; watchdog #42777386082 age 11,899s/gap 25,992s. TCE WF-06 #42799497774 age 2,026s/gap 27,892s; WF-12 #42795292155 age 3,796s/gap 27,790s. Only first-attempt master schedule events count.
- Manual reconcile #42799573178 succeeded with allow_image_changes=false; GHCR read preflight passed; Auth runtime Secret provision/verification succeeded with values suppressed; shared ghcr-pull unchanged; drift=false and production manifest apply/image promotion skipped. TCE/Auth remain 0/0 maintenance; MicroFE health passed; Keycloak skipped.
- Latest full read-only K3s snapshot #42795611235 is 60m56 old at the 11:02:41Z reference (within 75m budget, but not a native scheduled inspection). Last-known state: K3s node Ready/ARM64; Media and MicroFE core 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff; OIDC 503; Media runner service/listener active; host restart required.
- Preserve app-owned immutable publishers and useful CI/test/security/manual/release/backup/scheduled jobs. Platform remains sole production apply authority. No duplicate direct SSH/Compose authority and no workflow removal were justified.
- GitHub branch metadata reports protected=false on all five master branches; inherited ruleset coverage remains unverified due HTTP 403. Admin follow-up is issue #1575. Scheduler telemetry is issue #1497; TCE/Auth P0 is issue #872; Stock owner actions are issues #42/#43.
- No image publication/promotion, manifest apply, rollout/scaling, namespace/storage deletion, runner retirement, shared pull credential rotation, DNS/database/storage mutation or host reboot. Auth runtime Secret provision/verification did occur via Platform reconciliation. TCE market-scan schedule unchanged.

---

## 2026-11-10 17:04 ICT — workflow inventory and fresh runtime evidence

- Current `master` heads: Platform `11751365a0a68d4ec8e33cce8663927c5056dde8`; TCE `0f71aa56`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision drafts: Platform #1314/#544/#541/#539 and Auth #76. No open PRs in TCE, Stock or Media.
- Platform PR #1576 merged as `60b1d3aa`, exact-head and post-merge manifest validation PASS. Read-only inspection PR #1577 merged as `11751365`; generated from inspect fallback #42795611235, exact-head validation PASS and post-merge #42795863143 PASS.
- Latest app CI: TCE WF-01/WF-02/WF-05 PASS; Stock CI #42610360402 PASS; Media CI #42539512417 PASS; Auth CI #42654579277 PASS. Stock scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`, before dependency/browser/ingestion steps.
- Latest native TCE WF-12 #42795292155 (09:59:25Z) sent an authenticated heartbeat; Platform receipt #42795310808 verified run ID/path/event/master SHA/attempt. WF-12 failed its WF-06 freshness check because WF-06 #42744759966 was 26,122s old (435m) against 25m, with 0m queue wait. WF-12 inter-arrival gap 27,790s vs 1,500s. Keep #1497 open.
- All six native schedule gaps remain outside unchanged budgets at 10:04:20Z: Platform reconcile #42778829676 age 7,669s/gap 25,539s/budget 2,700s; inspection #42749270072 age 23,973s/gap 24,367s/budget 4,500s; recovery #42777251549 age 8,466s/gap 26,068s/budget 2,700s; watchdog #42777386082 age 8,398s/gap 25,992s/budget 2,700s; TCE WF-06 #42744759966 age 26,417s/gap 23,806s/budget 1,500s; WF-12 #42795292155 age 295s/gap 27,790s/budget 1,500s. Only native first-attempt master schedule events count.
- Fresh read-only K3s snapshot #42795611235 generated 10:01:45Z and merged in #1577. Node Ready ARM64; disk 56%/20 GiB free; RAM ~19 GiB available; restart_required=yes. Media and MicroFE core 1/1. TCE/Auth/Keycloak 0/0; Keycloak condition timeout and public OIDC HTTP 503. Stock desired Admin×2 and Backend on tag `12d63b4` fail ARM64 manifest selection; legacy Backend/Frontend 1/1. Stock/Media namespace storage preflight clean, but Media runner service/listener active and external backup/DNS/registration proof missing. GitOps drift clean.
- Recovery reconcile #42795334693 succeeded in workflow_dispatch apply mode with image changes false; GHCR preflight passed; shared `ghcr-pull` unchanged; Auth runtime Secret provision/verification step succeeded with values suppressed; drift=false; manifest apply and rollout skipped. MicroFE health passed; TCE/Auth maintenance only; Auth TLS passed.
- Branch metadata `protected=false` for all five master branches; inherited ruleset coverage unverified because rulesets API returns HTTP 403. Admin follow-up issue #1575. Preserve app-owned publishers and all useful CI/test/security/manual/release/backup/scheduled jobs. Platform remains sole production apply authority; no duplicate direct SSH/Compose deployment authority.
- No production image publication/promotion, manifest apply, workload rollout/scaling, namespace/storage deletion, runner retirement, credential rotation, DNS/database/storage mutation or host reboot. TCE market-scan schedule unchanged.

---

## 2026-11-10 17:01 ICT — native heartbeat and recovery reconciliation inventory delta

- TCE WF-12 native schedule #42795292155 ran at 09:59:25Z on master SHA `0f71aa56`, attempt 1. Heartbeat dispatch succeeded; WF-06 delivery verification failed because latest WF-06 #42744759966 was 26,122s old against 1,500s (25m), with 0m queue wait. WF-12 inter-arrival gap was 27,790s against 1,500s.
- Platform receipt #42795310808 verified source run ID/path/event/master SHA/attempt and succeeded. This is delivery identity only, not service health or cadence acceptance. Issue #1497 updated.
- Heartbeat recovery dispatched Platform reconcile #42795334693 with `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR read preflight passed for Auth/MicroFE/TCE; Auth runtime Secret verified; shared `ghcr-pull` unchanged; no image-pull failures for managed MicroFE/TCE workloads; TCE release pairing passed; drift=false and production manifest apply skipped.
- Reconcile and final lane gate passed. MicroFE health passed; TCE/Auth were classified as intentional zero-replica maintenance (no live health assertion); Auth TLS verified; Keycloak skipped. Fresh pod inventory at 10:00:07Z: K3s ARM64 node Ready; Media and MicroFE core 1/1; Stock desired Admin/Backend ImagePullBackOff; legacy Stock Backend/Frontend 1/1.
- Post-reconcile inspection recovery was still in progress at 10:01:16Z. This workflow_dispatch/recovery is not native schedule evidence.
- Branch metadata `protected=false` on all five masters; inherited ruleset status unverified due rulesets API 403. Track in Platform issue #1575. Preserve all existing publishers, backup, test/security and scheduled workflows. No TCE market-scan schedule change.

---

## 2026-11-10 16:57 ICT — five-repository workflow inventory and governance refresh

- Current `master` heads: Platform `d93292c4`; TCE `0f71aa56`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE, Stock or Media.
- Latest master CI: Platform `validate-manifests` #42787531522 PASS; TCE WF-01 #42781396893, WF-02 #42781396928, WF-05 #42781396803 PASS; Stock CI #42610360402 PASS; Media CI #42539512417 PASS; Auth CI #42654579277 PASS. Stock scraper schedule #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`, before dependency/browser/ingestion steps.
- Platform PR #1574 is merged at `d93292c4`; exact-head #42787395953 and post-merge #42787531522 manifest validation PASS. TCE PR #1035 is merged at `0f71aa56`; exact-head WF-01P/WF-02/WF-05/WF-08B and post-merge WF-01/WF-02/WF-05 PASS.
- Branch metadata reports `protected=false` for master in all five repositories. Rulesets read returned HTTP 403 due GitHub plan/feature restriction; inherited ruleset coverage is unverified, not presumed absent. No settings were changed. Track admin verification and required-check enforcement in Platform issue #1575. Until verified, retain exact-head CI and expected-head merge checks.
- Six native schedule lanes remain outside unchanged age and inter-arrival budgets at 09:57:31Z: Platform reconcile #42778829676 age 7,260s/gap 25,539s/budget 2,700s; inspection #42749270072 age 23,564s/gap 24,367s/budget 4,500s; recovery #42777251549 age 8,057s/gap 26,068s/budget 2,700s; watchdog #42777386082 age 7,989s/gap 25,992s/budget 2,700s; TCE WF-06 #42744759966 age 26,008s/gap 23,806s/budget 1,500s; WF-12 #42741584886 age 27,676s/gap 25,383s/budget 1,500s. Push/manual/workflow_run/repository_dispatch receipts do not satisfy native cadence. Keep issue #1497 open; no cron or budget changes.
- Latest scheduled reconcile #42778829676 is now older than its 45-minute runtime evidence budget. Latest full K3s inspection fallback #42774740602 is older than its 75-minute snapshot budget; native inspection is older still. No current health claim or runtime mutation is authorized.
- Preserve app-owned immutable GHCR publishers and all useful CI/test/security/manual/release/backup/scheduled workflows. Pre-push tag guards and digest verification are not proof of GHCR server-side immutable-tag enforcement. No fresh production publisher run/digest was observed.
- Platform remains sole owner of production manifests, shared pull credentials, digest/provenance promotion, GitOps reconciliation, rollout and health. `reconcile-vps.yml` is sole production apply authority; `inspect-vps.yml` is read-only. No duplicate direct SSH/Compose production authority found.
- No production publication/promotion/apply/rollout/scaling/deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-10 15:57 ICT — workflow inventory and runtime evidence refresh

- Confirmed master heads: Platform `17a27437`; TCE `0f71aa56`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE, Stock or Media.
- Platform PR #1573 is merged; exact-head and post-merge manifest validation #42781706247/#42781784063 PASS. TCE PR #1035 is merged; exact-head WF-01P/WF-02/WF-05/WF-08B and post-merge WF-01/WF-02/WF-05 all PASS.
- Latest app CI: Stock #42610360402 PASS (7/7); Media #42539512417 PASS; Authentication #42654579277 PASS. These are app CI/build results, not production release/promotion evidence.
- Stock `run_scraper.yml` remains a purposeful weekend scheduled/manual job. Its schedule `0 1 * * 0,6` is already asserted by `scripts/validate-production-release-contract.sh`. Failure #42457182511 is the expected fail-closed missing-`VNSTOCK_API_KEY` preflight; all later ingestion/browser steps were skipped. Do not alter the schedule or weaken the guard. Owner action: provision the key out-of-band, then manually run `preflight_only=true`; see issue #42.
- TCE WF-09 remains manual-only and development-source-only after PR #1035's production-authority guard. WF-03 remains app-owned ARM64 publisher/Platform handoff; WF-10 remains staging-only. SSH host-key pinning remains blocked on an owner-verified fingerprint.
- Media WF-03 and Authentication release workflow remain app-owned publishers; Stock deploy.yml remains native-ARM64 app-owned publisher. Preserve tests/builds, security, backup, release and scheduled workflows. No duplicate direct SSH/Compose production deployment authority found.
- Platform remains sole owner of production manifests, shared GHCR pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health verification. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` remains read-only.
- Six native cadence lanes remain stale at 08:57:49Z: Platform reconcile age 3,678s/gap 25,539s/budget 2,700s; inspection 19,982s/24,367s/4,500s; recovery 4,475s/26,068s/2,700s; watchdog 4,407s/25,992s/2,700s; TCE WF-06 22,426s/23,806s/1,500s; WF-12 24,094s/25,383s/1,500s. TCE heartbeat receipts prove event/source identity, not freshness or health. Keep issue #1497 open; no cron or budget changes.
- Latest scheduled reconcile #42778829676 succeeded with GHCR preflight PASS, shared pull Secret unchanged, TCE pairing PASS, drift=false and apply/rollout skipped. Its cluster inventory is now older than 45 minutes. Full inspection fallback #42774740602 is older than 75 minutes; native inspection #42749270072 is stale. Last-known workload states must not be described as current health.
- No GHCR publication/promotion, manifest apply, rollout/scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-10 15:18 ICT — TCE WF-09 development-only authority guard merged

- TCE master is `0f71aa56` after PR #1035. WF-09 remains manual-only and is explicitly labeled as uploading to the isolated development directory; `validate-tce-release-contract.sh` now enforces its trigger, single extraction target, no production Compose/Kubernetes/service mutations and always-run SSH-key cleanup.
- WF-01P now triggers on WF-09 workflow changes. Exact-head PR runs #42781237215/#42781237078/#42781237093/#42781237139 all PASS on `09f73261d632d7a9fe4bfee83b96d52183302b0a`. Post-merge WF-02 #42781396928 and WF-05 #42781396803 PASS; WF-01 #42781396893 was still running after its release-contract and required-secret preflights passed.
- WF-09's `StrictHostKeyChecking=no` remains a documented security follow-up until a verified SSH host fingerprint is supplied. WF-03 remains the app-owned manual ARM64 publisher/Platform handoff; WF-10 remains staging-only. No production SSH/Compose/Kubernetes authority was added and no workflow was removed.
- Current Platform native gaps remain reconcile 25,539s/2,700s; inspection 24,367s/4,500s; recovery 26,068s/2,700s; watchdog 25,992s/2,700s. TCE WF-06/WF-12 gaps remain 23,806s/1,500s and 25,383s/1,500s. Receipt collector runtime remains verified; receipts do not establish service health or cadence.
- Scheduled reconciliation #42778829676 passed GHCR preflight and TCE release pairing, shared `ghcr-pull` unchanged, drift=false and apply/rollout skipped. Auth/TCE remain 0/0 maintenance; MicroFE healthy. Freshness-limited full K3s snapshot is manual fallback #42774740602, not native inspection.
- Platform master `48695d2`; TCE `0f71aa56`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision PRs remain Platform #1314/#544/#541/#539 and Auth #76.
- Issue #1497 remains open for authoritative GitHub Actions enqueue/delivery telemetry. Stock issue #42 remains open for owner-provided `VNSTOCK_API_KEY` and authenticated safe preflight. Media runner unregister/backup/DNS evidence and TCE/Auth recovery approval remain owner-blocked.
- No new GHCR publication, digest promotion, manifest apply, rollout/scaling, decommission, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-10 08:20 ICT — PR #1558 merged; read-only helper path exclusion verified

- Platform master: `30e1cd22ed887d1ce35be99e8fac97e206e35aaa`; PR #1558 exact-head checks #42734643361/#42734643354 PASS and post-merge #42734770070/#42734770118 PASS.
- Post-merge watchdog push smoke #42734770430 PASS; both TCE WF-06/WF-12 observations now report explicit `missing-token` / history-unverified. The secondary WF-06 fixture-unavailable warning is no longer emitted.
- `recover-stale-ops.yml` now excludes `scripts/verify-native-schedule-gap.py` from the broad read-only helper push path; no recovery push run followed the PR #1558 merge.
- `TCE_ACTIONS_READ_TOKEN` remains empty in the Platform job environment. Owner must configure the Platform repository secret with a fine-grained PAT restricted to TCE Dashboard, Actions: read + Metadata: read only.
- Native inter-arrival gaps remain over all six budgets; Platform recovery/watchdog age also exceeds 45m. Latest K3s inspection is a fresh manual fallback, not native schedule evidence.
- App publisher and sole Platform apply authority boundaries unchanged. No production publication, promotion, apply, rollout, scaling, deletion, runner retirement or host mutation. No cron/budget or TCE market-scan schedule change.

---

## 2026-11-10 08:15 ICT — PR #1558 validation correction and operational status

- Platform master: `2c62973ff2feddcd9e3a4cec5932cd62908d43c6`; PR #1557 merged with exact-head and post-merge `validate-github-actions`/`validate-manifests` PASS.
- `TCE_ACTIONS_READ_TOKEN` is empty in the Platform job environment; WF-06/WF-12 history is warning-only/unverified until the Platform repository owner configures the least-privilege fine-grained PAT (TCE Dashboard only; Actions: read + Metadata: read).
- PR #1558 (open, head `69bc98b6209616fdf5e1604a1d7cf1dfa5d5227b`) excludes `scripts/verify-native-schedule-gap.py` from recovery push triggers and recreates the WF-06 missing-token JSON fixture in the next step.
- Initial PR #1558 `validate-manifests` passed; `validate-github-actions` failed because a new static assertion split on substring `fi` (matching `if`). Assertion corrected to split on the actual newline/indentation of the closing `fi`; exact-head validation must rerun before merge.
- Recovery push #42733984764, triggered by the helper change before the exclusion, completed without dispatch: reconcile age 19m and read-only inspection fallback age 38m were within fallback thresholds.
- At 01:14Z no new TCE WF-12 01:07 schedule event was visible. Native gaps remain above all six budgets; Platform recovery age has now crossed its 45m age budget.
- No production release, image publication, promotion, apply, rollout, scaling, deletion, runner retirement or host mutation. No cron/freshness-budget or TCE market-scan schedule change.

---

## 2026-11-10 08:12 ICT — current post-merge checks and read-only push filter follow-up

- Platform master: `2c62973ff2feddcd9e3a4cec5932cd62908d43c6`.
- PR #1557 merged; exact-head `validate-github-actions` #42733851718 and `validate-manifests` #42733852287 PASS; post-merge #42733984606 and #42733984453 PASS.
- Push smoke #42733985163 confirmed the TCE read token secret is empty. WF-06/WF-12 history remains unverified/warning-only until the Platform repository secret is configured with Actions: read + Metadata: read on TCE Dashboard only.
- WF-06 API status propagation is active; a missing-token fixture was not visible to the following step in the post-merge smoke. Follow-up branch `fix/read-only-schedule-helper-push-filter-20261110` recreates the fixture when status is `missing-token`.
- Read-only helper `scripts/verify-native-schedule-gap.py` triggered the broad `recover-stale-ops.yml` push filter. Recovery #42733984764 completed without dispatch because current reconciliation and inspection fallback were fresh. Follow-up branch excludes this helper from recovery push paths and adds validator coverage.
- `reconcile-vps.yml` uses explicit production-path filters; no competing apply authority triggered. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only.
- Native cadence gaps remain above all six budgets; latest TCE WF-12 tick was not yet visible at 01:12Z. Do not infer cause without GitHub enqueue/delivery telemetry.
- No production image publication, digest promotion, manifest apply, rollout, scaling, deletion, runner retirement or host maintenance. No cron/budget or TCE market-scan schedule changes.

---

## 2026-11-10 08:10 ICT — TCE schedule history token merged; owner configuration pending

- Platform master: `ea393a6936f96559b1da597fd3378f3e0ffe63ed`; PR #1556 merged with exact-head and post-merge `validate-github-actions`/`validate-manifests` PASS.
- The watchdog now uses step-scoped `TCE_ACTIONS_READ_TOKEN` for read-only TCE WF-06/WF-12 Actions-history queries. Missing token is warning-only/unverified and does not weaken Platform native freshness gates.
- Post-merge push smoke #42733625753 showed `TCE_ACTIONS_READ_TOKEN` empty in the job environment. Platform repository secret configuration is still required.
- Follow-up branch `fix/tce-wf06-status-propagation-20261110` exports the WF-06 API status across steps and passes it into the inter-arrival verifier, preventing missing-token from being misreported as an empty schedule history. It adds static contract assertions and a missing-token negative self-test; PR validation is pending.
- Required token scope: fine-grained PAT limited to `phanthienquoc/TCE-dashboard`, **Actions: read** + **Metadata: read** only. No Contents, Packages, or write.
- App publishers and Platform production authority boundaries are unchanged. No production image publication, digest promotion, manifest apply, rollout, scaling, deletion or host mutation. No cron/budget or TCE market-scan schedule changes.

---

## 2026-11-10 08:00 ICT — schedule-observer credential and current deployment inventory

### Current master heads and open PRs

- Platform Infra: `179c28906d7f5dbc6f2f83a8b53ecafb17ea069c`; open drafts #1314/#544/#541/#539.
- TCE Dashboard: `68660a20e5bf3472a122c59d75b49ffce16a2ce9`; no open PR.
- StockDividend: `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; no open PR.
- Media Generation: `dcd698699c65ba6e73f6b43838975144777131c3`; no open PR.
- Authentication: `eab85fab32d7c9baef750c1fedbb93deb8c1333f`; open draft #76.

### Schedule-observer credential delta

- Platform `.github/workflows/reconcile-schedule-watchdog.yml` uses the new step-scoped repository secret `TCE_ACTIONS_READ_TOKEN` for only the two read-only TCE WF-06/WF-12 Actions-history queries.
- Both requests send a Bearer authorization header. If the secret is absent, the workflow records an explicit `missing-token` warning and leaves the TCE cross-repository observation unverified; it does not issue an anonymous request.
- Minimum fine-grained PAT scope: repository access limited to `phanthienquoc/TCE-dashboard`, **Actions: read** and **Metadata: read** only. No Contents, Packages, dispatch, or write permission.
- The credential name/scope is recorded in `docs/credentials.md` and `docs/credentials-key.md`. Secret configuration is an owner action and has not been verified by the connector.
- `scripts/validate-workflow-contracts.py` enforces both step-scoped secret references, both Authorization headers, explicit missing-token branches and both credential inventory entries. `validate-github-actions.yml` already runs this contract validator.

### Current operational evidence

- Native reconcile #42731410572 SUCCESS; drift=false, apply skipped; `ALLOW_IMAGE_CHANGES=false`.
- Native Platform inter-arrival gaps: reconcile 26,769s/2,700s; inspection 39,672s/4,500s; recovery 28,020s/2,700s; watchdog 28,068s/2,700s.
- TCE WF-06/WF-12 gaps: 37,834s and 37,832s against 1,500s budgets. Strict WF-06 public probes remain HTTP 503.
- Latest K3s snapshot #42728878765 is a fresh `workflow_dispatch` fallback (not native schedule): node Ready/ARM64; Media/MicroFE core 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff on historical ARM64-incompatible `12d63b4`.
- No new GHCR publication, Platform promotion, manifest apply, scaling, deletion, runner retirement or host maintenance. Existing app publisher authority and sole Platform apply authority are unchanged.

### Authority boundary

- TCE/Stock/Media/Authentication continue to own app tests/builds and immutable GHCR publication.
- Platform continues to own production manifests, shared GHCR pull credentials, publisher provenance/digest verification, GitOps promotion/reconciliation, rollout and health.
- App-side publisher workflows remain publishers; no SSH/Compose/Kubernetes apply authority was added or removed.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only.
- Preserve existing CI/security/release/backup/scheduled jobs. No cron, freshness budget or TCE market-scan schedule changed.

---

## 2026-11-10 06:57 ICT — cross-repo workflow authority audit

- Current master heads: Platform `47c5866d`; TCE `68660a20`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open owner-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76; no TCE/Stock/Media open PRs.
- Current-head Platform `validate-manifests` #42717334146 PASS. Latest Platform `validate-github-actions` #42709336655 is on the immediately previous code head `8a603a5b`; current docs-only head adds no workflow code. TCE WF-01/02/05 pass; Stock CI 7/7 pass; Media CI pass; Auth CI pass.
- TCE WF-03 is a manual master-only app publisher: native ARM64 builds, full-source-SHA tag guard, registry digest/ARM64 verification, exact Platform dispatch. Stock `deploy.yml` is app-owned master-push GHCR publication with immutable-tag/ARM64 checks; manual publication is disabled and no Platform handoff is sent. Media WF-03 is app-owned GHCR publication with full-SHA tags/digest checks and no Platform handoff. Auth release is manual master-only app publication with exact Platform digest-promotion payload. None of these app workflows performs SSH/Compose or Kubernetes apply.
- No duplicate direct deployment authority was found in these four app publisher workflows. Keep them; do not remove by name alone. Platform `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only.
- App-level pre-push tag guards and post-push digest/ARM64 inspection do not prove GHCR server-side immutable-tag enforcement. No current production release run supplied a fresh tag-to-digest attestation.
- TCE WF-07 #42711312505 native integration check PASS (not health freshness). WF-12 #42711341231 failed stale WF-06; WF-13 #42711368741 recovery PASS; read-only WF-06 fallback #42711398985 failed all four strict HTTP 200 probes with 503.
- Six native Platform/TCE deployment lanes remain stale/outside unchanged budgets. Last native IDs: reconcile #42664347392; inspection #42694932077; recovery #42657359651; watchdog #42657625219; TCE WF-06 #42689871258; WF-12 #42681246237. Latest full K3s snapshot #42709680634 is 6,341s old (>4,500s freshness budget) and cannot authorize runtime mutation.
- Stock scraper #42457182511 failed closed on an older SHA with empty VNSTOCK_API_KEY; current secret state is not exposed. Issue #42 remains owner action. Do not repeat ingestion or expose credentials.
- Preserve CI/test/security, manual release, backup, and scheduled jobs. Do not change cron/freshness budgets or TCE market-scan schedule. No publication, dispatch, promotion, apply, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance in this checkpoint.

---

## 2026-11-10 05:14 ICT — fresh K3s inspection and cross-repo CI

- Platform master `051f7b83`; TCE `68660a20`; Stock `b1b5e177`; Media `dcd69869`; Auth `eab85fab`. Open drafts Platform #1314/#544/#541/#539 and Auth #76; no open PRs in TCE/Stock/Media.
- MicroFE WF-08B exact sender/receiver schema contracts are merged (TCE #1034, Platform #1548). Sender tests 1 positive/19 negative; receiver 1 positive/17 negative. Receiver gate is before kubectl/GHCR/provenance/promotion. TCE post-merge WF-01/02/05 all PASS; Platform post-merge validations PASS.
- Platform inspection PR #1550 merged at exact validated head after validate-manifests #42709965064 PASS. Snapshot generated 22:12:13Z: node Ready/ARM64, RAM 19 GiB available, disk 56%/20 GiB free, Docker 9.195 GB/5.773 GB reclaimable, host restart required. Media and MicroFE core pods 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend pulls fail on historical tag `12d63b4` with no ARM64 manifest. Storage preflight clean (only k3s-debug PVC/PV, no Stock/Media snapshots); Media runner service/Listener remains active. OIDC probes 503.
- Reconciliation #42709362025 used `ALLOW_IMAGE_CHANGES=false`, passed GHCR read preflight, provisioned/verified Auth runtime Secret, left shared `ghcr-pull` unchanged, passed TCE release pairing, found drift=false and skipped manifest apply.
- All six native schedule inter-arrival gaps remain above unchanged budgets; manual inspection #42709680634 does not count as a native tick. GitHub administrator enqueue/delivery evidence remains required.
- Stock scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`; issue #42 open. Media runner unregister, backup/retention and DNS ownership remain unverified. No decommission.
- No production publication, release dispatch, digest promotion, manifest apply, scaling, namespace/storage deletion, runner retirement, DNS/database mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-10 05:10 ICT — MicroFE exact dispatch and reconciliation delta

- Platform PR #1548 and TCE PR #1034 are merged. Platform exact-head lint/manifests #42709136411/#42709136264 and post-merge #42709336655/#42709336764 PASS. TCE exact-head WF-01P/WF-02/WF-05/WF-08B #42709203603/#42709204042/#42709203626/#42709203665 PASS. Post-merge WF-02 #42709513839 PASS; WF-01 #42709513845 and WF-05 #42709513831 were still running at checkpoint.
- WF-08B MicroFE sender now validates the exact two-key sender envelope and 11-key client payload before dispatch; tests 1 positive/19 negative. Platform receiver validates the exact 11-key payload before tooling/GHCR/provenance/promotion; tests 1 positive/17 negative. Receiver CI enforces step ordering; MicroFE source run ID zero is rejected. PR checks did not publish GHCR images or dispatch production events.
- Recovery-triggered reconciliation #42709362025 completed successfully with `mode=apply`, `target=all`, `ALLOW_IMAGE_CHANGES=false`. GHCR read preflight passed for Auth, MicroFE Shell/WS and TCE web/service; Auth runtime Secret provisioned/verified; shared `ghcr-pull` unchanged; no managed image-pull failures; TCE pairing passed; drift=false, apply skipped. K3s node Ready/ARM64; Media/MicroFE workloads 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff while legacy Backend/Frontend 1/1.
- Reconcile pod readout is fresh at 22:10:30Z but does not include disk/RAM/restart-required metrics. Full inspection #42694932077 is beyond 75m freshness and cannot authorize mutation. No public HTTP 200 claim for 0/0 TCE/Auth.
- All six native schedule gaps remain above unchanged budgets; latest IDs/gaps are recorded in the deployment tracker and issue #1497. Recovery push/manual runs are not native acceptance. GitHub administrator enqueue/delivery evidence still required.
- Stock weekend scraper #42457182511 remains fail-closed on missing `VNSTOCK_API_KEY`; owner action issue #42 open. Media runner remains active; external backup/retention/DNS and remote unregister are unverified.
- No image publication, production dispatch, digest promotion, manifest apply, scaling, decommission, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-10 04:03 ICT — fresh inspection and schedule evidence

- Current master heads: Platform `827d8d442cf7de344be04a246e56ee2ee3148657`; TCE `aea2755f164186eb6172d9e11afece98227907f9`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs: Platform #1314/#544/#541/#539 (draft); Authentication #76 (draft); none in TCE/Stock/Media.
- Native Platform inspection #42694932077 succeeded at 20:38:40Z and auto-merged inspection-only PR #1546 at master SHA `827d8d44`. Snapshot `debug/vps-latest.md` generated 20:38:49Z; it was 24m26s old at checkpoint time. No production manifests changed.
- Platform workflow_dispatch reconciliation #42695326631 succeeded with `mode=apply`, `target=all`, `ALLOW_IMAGE_CHANGES=false`: GHCR read preflight passed; Auth runtime Secret provisioned/verified; shared `ghcr-pull` unchanged; managed image-pull restart found no failures; TCE release pairing passed; drift=false and manifest apply skipped. TCE/Auth 0/0 maintenance, MicroFE active health passed, Keycloak skipped. Recovery controller #42695559771 passed and avoided duplicate fallback dispatch.
- Latest native schedule IDs/gaps/budgets: reconcile #42664347392 / 37,823s / 2,700s; inspection #42694932077 / 39,672s / 4,500s; recovery #42657359651 / 37,669s / 2,700s; watchdog #42657625219 / 37,408s / 2,700s; TCE WF-06 #42689871258 / 37,834s / 1,500s; TCE WF-12 #42681246237 / 37,832s / 1,500s. All gaps exceed unchanged budgets. One fresh inspection tick is not cadence recovery. Issue #1497 remains open for administrator enqueue/delivery evidence.
- TCE native WF-06 #42689871258 and manual fallback #42689940373 both failed strict HTTP 200 probes (all four endpoints returned 503). Keep strict checks; TCE/Auth remain intentional 0/0.
- App CI: TCE WF-01/05/02 #42680305817/#42680305566/#42680305431 PASS; Stock CI #42610360402 PASS 7/7; Media CI #42539512417 PASS; Auth CI #42654579277 PASS. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; owner action issue #42.
- K3s: node Ready/ARM64; disk 56%, ~20 GiB free; ~19 GiB RAM; restart required. Media/MicroFE core 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff on historical `12d63b4`; legacy Backend/Frontend remain 1/1. Only PVC/PV is `k3s-debug`; no Stock/Media snapshot refs. Media runner service and Listener remain active; external backup/retention/DNS and remote unregister remain unverified.
- No new immutable GHCR publication or digest promotion. No production manifest apply, namespace/storage deletion, runner retirement, DNS/database mutation or host maintenance. TCE market-scan schedule unchanged.


---

## 2026-11-10 03:10 ICT — TCE native tick and controlled reconciliation

- Platform PR #1544 merged at `a3566640`; exact-head #42689845993 and post-merge #42689926885 passed. Current heads: Platform `a3566640`, TCE `aea2755f`, Stock `b1b5e177`, Media `dcd69869`, Auth `eab85fab`. Open drafts Platform #1314/#544/#541/#539 and Auth #76; no TCE/Stock/Media open PRs.
- TCE native WF-06 #42689871258 arrived 20:07:17Z after 37,834s gap and failed all four strict HTTP 200 probes with 503. A single tick is not cadence recovery.
- Existing recovery controller dispatched reconcile-vps #42689957669 with `mode=apply`, `allow_image_changes=false`, `target_app=all`. GHCR pull preflight passed for Auth, MicroFE Shell/WS and TCE web/service; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; TCE release pairing `prod-v0.1.0-e75e338` passed. Drift=false, manifest apply skipped, image-change guard skipped. TCE/Auth intentionally 0/0 (no live health asserted); MicroFE active health passed; Keycloak skipped; final gate passed. Recovery #42690196366 passed and avoided duplicate apply/inspection due fresh reconciliation and fallback snapshot.
- K3s snapshot #42681626973 generated 19:15:47Z; age 54m13s at 20:10Z, within 75m. Node Ready/ARM64; disk 56%, ~20 GiB free; RAM ~19 GiB; host restart required. Media/MicroFE core 1/1, TCE/Auth/Keycloak 0/0, Stock desired Admin/Backend ImagePullBackOff on historical `12d63b4`. Media runner service/listener remains active; backup/retention/DNS and remote unregister unverified.
- Native schedule ages at 20:10Z: Platform reconcile 9,917s; inspection 37,952s; recovery 12,494s; watchdog 12,398s; TCE WF-06 163s; WF-12 3,408s. Inter-arrival gaps 37,823s / 27,768s / 37,669s / 37,408s / 37,834s / 37,832s vs unchanged budgets 2,700s / 4,500s / 2,700s / 2,700s / 1,500s / 1,500s. No consecutive in-budget deliveries. Evidence in [issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497#issuecomment-6750237520).
- Stock weekend scraper #42457182511 failed closed due empty `VNSTOCK_API_KEY`; owner action tracked in Stock issue #42. Do not weaken fail-closed preflight or change weekend schedule.
- No GHCR publication, release dispatch, digest promotion, production manifest apply, workload scaling, decommission, runner retirement, DNS/storage/database mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-10 03:04 ICT — Stock scraper credential blocker and schedule freshness recheck

- Platform master `6e1598c0`, TCE `aea2755f`, Stock `b1b5e177`, Media `dcd69869`, Auth `eab85fab`. Platform latest master validate-manifests #42684398108 PASS; latest app master CI evidence: TCE #42680305817/#42680305566/#42680305431 PASS, Stock #42610360402 PASS 7/7, Media #42539512417 PASS, Auth #42654579277 PASS.
- Open owner-decision drafts: Platform #1314/#544/#541/#539; Auth #76. No TCE/Stock/Media open PRs.
- Stock weekend scraper #42457182511 failed closed because `VNSTOCK_API_KEY` is empty. It stopped before dependency install, Chromium, ingestion or side effects. Existing docs prescribe safe `preflight_only=true`; owner action tracked in [Stock issue #42](https://github.com/phanthienquoc/stockdividend/issues/42). Keep cron `0 1 * * 0,6`; do not weaken fail-closed credential validation.
- K3s read-only snapshot #42681626973 generated 19:15:47Z; 48m42s old at 20:04:29Z, within 75m budget. Node Ready/ARM64; disk 56%, ~20 GiB free; RAM ~19 GiB; restart required. Media and MicroFE core pods 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend pulls fail on historical tag `12d63b4` without ARM64 manifest. Media runner service/listener still active. Only PVC is `k3s-debug`; backup/retention/DNS and remote runner unregister remain unverified.
- Native schedule latest ages at 20:04:29Z: Platform reconcile 9,586s; inspection 37,621s; recovery 12,163s; watchdog 12,067s; TCE WF-06 37,666s; WF-12 3,077s. All exceed budgets; last inter-arrival gaps are 37,823s / 27,768s / 37,669s / 37,408s / 27,454s / 37,832s against 2,700s / 4,500s / 2,700s / 2,700s / 1,500s / 1,500s. Evidence in [issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497#issuecomment-6750159483).
- TCE public health fallback #42681311390: four strict HTTP 200 probes returned 503. TCE/Auth remain intentional 0/0; no live health claim. No production publication, dispatch, digest promotion, manifest apply, rollout, scaling, decommission, runner retirement, DNS/storage/database mutation or host maintenance.
- Ownership and authority unchanged: app repos own builds/tests and immutable GHCR publication; Platform owns manifests, shared pull credentials, digest/provenance verification, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only. TCE market-scan schedule unchanged.

---

## 2026-11-10 02:28 ICT — TCE sender/receiver merged; current schedule and K3s evidence

- Platform #1539 exact TCE receiver schema and TCE #1033 exact sender/source-context contract are merged. Platform exact-head and post-merge validation runs passed; TCE exact-head WF-01P/WF-05/WF-02 and post-merge WF-01/WF-05/WF-02 passed. No production dispatch or publication was executed.
- Platform #1540 readiness docs and #1541 fresh inspection docs are merged. Latest Platform master `aa668f00`; validate-manifests #42683186419 PASS. TCE master `aea2755f`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`.
- App ownership remains unchanged: TCE/Stock/Media/Auth own tests/builds and immutable GHCR publishing; Platform owns manifests, shared pull credentials, digest/provenance verification, GitOps promotion/reconciliation, rollout and health.
- Latest app CI: TCE WF-01/02/05 #42680305817/#42680305431/#42680305566 PASS; Stock #42610360402 PASS 7/7; Media #42539512417 PASS; Auth #42654579277 PASS. These are build/validation results, not new GHCR publication evidence.
- TCE WF-06 fallback #42681311390 returned HTTP 503 on all four strict public endpoints. Native WF-12 #42681246237 heartbeat succeeded but its WF-06 freshness gate failed. TCE/Auth remain 0/0 maintenance; strict probes stay unchanged.
- Fresh read-only K3s inspection #42681626973 snapshot `2026-11-09T19:15:47Z`: node Ready/ARM64; disk 56%, ~20 GiB free; ~19 GiB RAM available; restart required; Media/MicroFE 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend image pulls fail on historical `12d63b4` without ARM64 manifest. Only PVC is `k3s-debug/k3s-debug-logs`; Media runner service/listener remains active; remote unregister, external backup/retention and DNS ownership remain unverified. No decommission.
- Native schedule age/inter-arrival evidence at 19:28:00Z is recorded in the deployment tracker and issue #1497 comment #6749394096. TCE WF-12's own run age is 888s (<1,500s) but it correctly failed because WF-06 is stale; all six inter-arrival gaps remain out of budget. GitHub administrator telemetry remains required.
- Open drafts: Platform #1314/#544/#541/#539; Authentication #76. No open PRs in TCE, Stock or Media.
- No production publication, dispatch, digest promotion, manifest apply, rollout, scaling, namespace/storage deletion, runner retirement, DNS/database mutation or host maintenance. Auth runtime Secret was provisioned in the earlier controlled reconciliation; shared `ghcr-pull` remained unchanged. No cron/freshness change; TCE market-scan schedule unchanged.

---

## 2026-11-10 02:19 ICT — TCE receiver merged; fresh K3s inspection and recovery evidence

- Platform receiver PR #1539 merged at `17b8ae2c374382fb07604a5a975dc52a242b3172`. Exact-head validate-github-actions #42681274603, validate-manifests #42681274888 and Keycloak CI #42681275045 passed; post-merge push runs #42681874018/#42681873952/#42681873949 passed. The earlier skipped-only validate-manifests anomaly did not recur.
- Platform tracker PR #1540 merged at `4cf8534d4c28f4b5d7eff8f74c08b2245bc83c2e`; inspection PR #1541 merged at `9f8f2d81859b0ff1b5d925db3cc4ad6d448ec04a` after fresh read-only inspect-vps #42681626973.
- TCE PR #1033 merged at `aea2755f164186eb6172d9e11afece98227907f9`. WF-03 now gates source context before notifications, builds and GHCR publication. Exact-head and post-merge WF-01/02/05 checks all passed.
- Controlled recovery #42681294414 used the existing `reconcile-vps.yml` authority with mode=apply, target=all and `ALLOW_IMAGE_CHANGES=false`. GHCR pull preflight passed; Auth runtime Secret provision/verification succeeded; shared `ghcr-pull` Secret was unchanged; no blocked image-pull restarts were needed for active MicroFE/Auth/TCE targets. Drift=false; production manifest apply skipped. MicroFE health passed; TCE/Auth 0/0 maintenance lanes did not assert live health; Keycloak skipped.
- Fresh K3s snapshot `2026-11-09T19:15:47Z`: node Ready/ARM64; disk 56%, 20 GiB free; RAM available ~19 GiB; host restart required; Media runner service/listener still active. Media backend/frontend and MicroFE shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend pods still ImagePullBackOff on old tag `12d63b4` with no ARM64 descriptor. Only PVC/PV is the k3s-debug log claim; no Stock/Media VolumeSnapshot refs. Cached Stock tags `23b2878` lack RepoDigest. No decommission.
- TCE WF-12 native schedule #42681246237 failed; heartbeat to Platform succeeded. WF-13 #42681277887 dispatched WF-06 fallback #42681311390, which got HTTP 503 on all four public endpoints. Do not treat zero-replica internal health lanes as public health recovery.
- Native schedule age/inter-arrival evidence remains out of budget across all six deployment lanes. Latest event IDs, gaps and issue #1497 evidence are in the deployment tracker. No cron, freshness budget or TCE market-scan schedule changed.
- No workflow removed. No production image publication, digest promotion, repository dispatch, manifest apply, workload scaling, namespace/storage deletion, runner retirement, DNS mutation or host maintenance.

---

## 2026-11-10 02:00 ICT — TCE source-context gate and receiver PR status

- TCE PR #1033 merged at `aea2755f164186eb6172d9e11afece98227907f9`. Exact-head WF-01P #42679926050, WF-05 #42679926049 and WF-02 #42679925453 passed. WF-01P executed the release contract validator and frontend build; WF-05 executed backend build/unit tests; WF-02 formatting passed.
- WF-03's first release gate now executes `scripts/verify-tce-release-source-context.sh` before notifications, builds or GHCR publication. It binds the run to `phanthienquoc/TCE-dashboard`, the exact `.github/workflows/wf-03-tce-production-deploy.yml@refs/heads/master`, manual `workflow_dispatch`, positive run ID/attempt and full source SHA. The validator tests 1 positive and 8 negative contexts. The existing exact two-key sender envelope/nine-key client payload tests remain in the release-contract validation.
- Post-merge TCE master: WF-02 #42680305431 PASS, WF-05 #42680305566 PASS, WF-01 #42680305817 was still in progress at 19:00:27Z. No production release was run.
- Platform receiver PR #1539 adds the exact nine-key TCE dispatch receiver and 1 positive/16 negative fixtures. Exact-head validate-github-actions #42672541843 and Keycloak CI #42672541506 passed. validate-manifests #42672541861 failed with only a skipped report job exposed and no validate job/logs; keep open until a real successful manifest validation is observed.
- No workflow was removed. TCE market-scan schedule, all deployment cron expressions and freshness budgets remain unchanged.

---

## 2026-11-10 00:56 ICT — native schedule and reconciliation recheck

- Current heads: Platform `4ddbcaeafe95002308cb127601445d37e74635df`; TCE `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Latest Platform scheduled reconcile #42664347392 succeeded: GHCR read preflight passed for Auth/MicroFE/TCE images; Auth runtime Secret keys verified; shared `ghcr-pull` unchanged; drift=false and apply skipped. MicroFE health passed; TCE/Auth were explicit zero-replica maintenance scopes. This is preflight/reconciliation evidence, not a production rollout.
- Latest native schedule event IDs: reconcile #42664347392; inspect #42594848960; recovery #42657359651; watchdog #42657625219; TCE WF-06 #42594757482; TCE WF-12 #42587926693. At 17:56:36Z their ages were 1,913s / 29,948s / 42,159s / 41,802s / 29,993s / 33,236s. Inter-arrival gaps were 37,823s / 27,768s / 37,669s / 37,408s / 27,454s / 25,452s against unchanged budgets 2,700s / 4,500s / 2,700s / 2,700s / 1,500s / 1,500s. Watchdog #42664637994 independently reports these gaps and fails closed. Require consecutive native runs within budget; fallbacks are not acceptance.
- Latest K3s inspection #42657403805 generated 16:42:11Z and was 74m25s old at 17:56:36Z, near the 75-minute freshness limit. A fresh read-only inspection is required before runtime mutation. Node Ready/ARM64; disk 56%, ~20 GiB free; ~19 GiB available RAM; restart required. Stock desired pods ImagePullBackOff on historical ARM64-incompatible tag; Media/MicroFE core workloads 1/1; TCE/Auth/Keycloak 0/0.
- TCE build/format/backend CI passes; public health WF-06 and freshness WF-12 fail. Stock master CI 7/7, Media master CI and Auth master CI pass. No app publisher/digest handoff was observed.
- Open drafts: Platform #1314/#544/#541/#539; Authentication #76. No open PRs in TCE, Stock or Media.
- Preserve all workflow purposes, cron expressions, freshness budgets and TCE market-scan schedule. No production publication, dispatch, promotion, apply, rollout, scaling, deletion, runner retirement or host/DNS/storage mutation.

---

## 2026-11-09 23:36 ICT — Auth receiver exact-schema contract

- Platform PR #1534 merged at `a58d801e1770fad464477729ab49da64796fd4a1` from exact head `436ad889ba1c52ea7486ea881a559746d15fda87`. Exact-head `validate-github-actions` #42656332110 and `validate-manifests` #42656332072 passed. Post-merge push validation not yet observed.
- Added `scripts/verify-auth-dispatch-payload.sh` and sixteen negative/one positive fixtures. Receiver checks the exact ten-key `client_payload`, app/component, SHA-256 digest, full source SHA/head equality, positive string run ID/attempt, approved `.github/workflows/release.yml`, `workflow_dispatch` source event and immutable full-SHA tag. It runs before resolving promotion inputs and only for `auth-image-published`.
- Tightened Auth source run ID to positive integer in both the receiver workflow and provenance helper; zero ID is covered by regression tests. Auth remains publisher owner; Platform remains promotion/apply owner. Manual workflow_dispatch path unchanged.
- Current master heads: Platform `a58d801e`; TCE `65af89f6`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`. Open drafts: Platform #1314/#544/#541/#539 and Authentication #76.
- Latest verified app checks: Auth #42654291067 and post-merge #42654579277 PASS; Stock #42610360402 PASS 7/7; Media #42539512417 PASS; TCE WF-06 #42594757482 fails four HTTP 503 probes; WF-12 #42587926693 fails freshness.
- Latest K3s snapshot generated 15:23:26Z; at 16:36:42Z it was 73m16s old (104s inside 75m budget). Node Ready/ARM64, disk 56%, ~19 GiB available RAM, restart required. Media/MicroFE 1/1; Stock desired Admin/Backend ImagePullBackOff; TCE/Auth/Keycloak 0/0. Storage-clean is not delete authorization; Media runner still active and external backup/DNS/remote unregister remain unverified.
- Latest filtered native schedule query remains #1497 comment #6745121718 at 16:18:30Z; all six deployment lanes exceed budgets. Preserve cleanup, TCE WF-07 integration/backup and mirror schedules; no cron or TCE market-scan change.
- No production publication, dispatch, digest promotion, manifest apply, rollout, scaling, deletion, runner retirement or host/DNS/storage mutation.

---

## 2026-11-09 23:26 ICT — Auth exact payload filter tests

- Authentication PR #93 merged at `eab85fab32d7c9baef750c1fedbb93deb8c1333f`. Exact PR CI #42654291067 passed tests, typecheck, build, immutable release contract, manual-only release pin validation and native ARM64 non-publishing build. Post-merge master CI #42654579277 was still in progress at 16:25:21Z.
- Auth's release-contract validator now extracts the actual jq filter from `release.yml` and executes it against one valid and eight invalid payload fixtures. The test covers exact root/client keys, event, app/component, digest, source SHA, run ID/attempt and workflow path. It runs both in CI and before the manual release workflow publishes an image.
- Auth dispatch uses the same validated JSON file via `gh api --input`; no release or repository_dispatch was triggered.
- Preserve the unrelated Platform mirror schedule; its last visible run #41737911916 failed because `PLATFORM_INFRA_MIRROR_TOKEN` is missing. The `vps-image-cleanup` schedule #42472343489 was a dry run with 8 candidates, retain 10, remove 0. TCE WF-07 integration and backup schedules remain purposeful.
- Issue #1497 comment #6745121718 contains the latest filtered native schedule evidence; all six deployment lanes remain outside budgets. Administrator delivery telemetry is still outstanding.
- K3s snapshot from 15:23:26Z is within the 4,500s budget but approaching expiry. Media runner service/listener active; remote unregister, external backup/retention and DNS ownership remain blockers. No deletion or runtime mutation.

---

## 2026-11-09 23:20 ICT — Auth dispatch payload and scheduled-job audit

- Authentication PR #92 merged at `135a60a4f0af1a74c6cd23cc5b2dc12b6a7f4a2a`. Exact PR CI #42653356621 passed, including tests/typecheck/build, immutable release contract, manual-only release pin validation and native ARM64 non-publishing build. Post-merge #42653598077 completed successfully at 16:21:09Z.
- Auth's manual publisher now builds an exact `auth-image-published` JSON payload, validates root and client-payload keys/values/provenance, writes a run summary and sends the same file using `gh api --input`. The dispatch step runs only after validation. No release or image publication was triggered.
- The unrelated scheduled mirror workflow #41737911916 failed because `PLATFORM_INFRA_MIRROR_TOKEN` is missing. Preserve the workflow; owner action is to restore the least-privilege destination-repository token or explicitly retire the mirror after confirming ownership.
- Scheduled `vps-image-cleanup` #42472343489 succeeded in dry-run mode: 8 unused images identified, retain 10, remove 0. TCE WF-07 integration and backup schedules are also purposeful and remain untouched.
- Six tracked Platform/TCE deployment freshness lanes remain beyond budget; issue #1497 comment #6745121718 contains the latest native-event ages. GitHub administrator enqueue/delivery telemetry remains outstanding.
- K3s inspection snapshot 15:23:26Z remains within freshness budget at 16:20:55Z. Media runner is still active; external backup/retention, remote unregister and DNS ownership remain blockers. No deletion, runtime mutation or schedule changes.

---

## 2026-11-09 23:12 ICT — post-merge verification

- Platform PR #1530 documentation merge at `abad728979ea245e026be7681da16a3c0dadcbbc`: exact-head `validate-manifests` #42652140427 PASS; post-merge #42652306568 PASS.
- Platform PR #1529 decommission evidence-reference code remains fully validated: exact-head `validate-github-actions` #42651633999 and `validate-manifests` #42651634041 PASS; post-merge #42651796084 and #42651796227 PASS.
- Delete mode requires stable HTTPS backup/retention and authoritative DNS evidence references before the protected production Environment gate; the references are included in the workflow summary for reviewer inspection. Existing typed confirmations, Media local/remote runner retirement, retired-manifest guard and fresh storage preflight remain required.
- K3s snapshot from 15:23:26Z is still within the 4,500s freshness budget at 16:12:17Z. Media runner service/listener remains active; external backup/retention, remote unregister and DNS ownership remain blockers.
- Issue #1497 comment #6744779547 remains the latest filtered native schedule evidence; all six tracked gaps/ages exceed budgets. Administrator delivery telemetry outstanding. No cron or TCE market-scan schedule changes.

---

## 2026-11-09 23:09 ICT — decommission evidence contract and readiness

- Platform PR #1529 merged at `9fbf172c7e0b2a60b96f6fdd75f48860aa813647`. The manual-only `decommission-stock-media.yml` workflow now requires stable HTTPS references for backup/retention and authoritative DNS/provider evidence in delete mode. The lightweight validation job checks them before the protected `production` Environment gate and records the links in the run summary. It rejects non-HTTPS, host-only, embedded credentials, query strings, fragments and whitespace. Plan mode is unchanged.
- Exact-head checks #42651633999 (`validate-github-actions`) and #42651634041 (`validate-manifests`) passed on head `9b5fcf4518fbe5b5714f71c098c55081eb867507`. Post-merge #42651796084 (`validate-manifests`) passed; #42651796227 (`validate-github-actions`) completed successfully at 16:09:40Z; post-merge Platform validation is fully green.
- Evidence URLs are auditable references only; reviewers must inspect the linked backup and DNS evidence. The workflow still requires typed confirmations, protected production Environment approval, local Media service/process retirement, GitHub runner unregister verification with the scoped audit token, the retired-manifest guard and a fresh read-only storage preflight before deletion.
- Latest read-only K3s snapshot is generated 15:23:26Z, within the 4,500s freshness budget at this checkpoint. Media runner service/listener is still active; remote registration, external backup/retention and authoritative DNS ownership remain unverified. No deletion.
- Native schedule issue #1497 updated with current filtered event evidence in comment #6744779547. All six tracked Platform/TCE gaps and ages remain outside budgets; administrator enqueue/delivery evidence is still required. Do not count fallback events as native acceptance.
- App repositories continue to own tests/builds and immutable GHCR publication; Platform alone owns production manifests, shared pull credentials, provenance/digest/ARM64 verification, GitOps promotion/reconciliation, rollout/health and protected decommission. No duplicate SSH/Compose authority; TCE market-scan schedule unchanged.

---

## 2026-11-09 22:25 ICT — Stock publisher/decommission distinction

- Stock current master `deploy.yml` is app-owned and ARM64-only: three images (scraper/admin/backend) publish full-source-SHA and version+SHA tags, reject existing immutable tags and verify linux/arm64 registry manifests/digests. CI separately builds all three ARM64 images with push=false; master CI #42610360402 PASS 7/7.
- No Platform handoff remains by design because Stock was removed from active Platform GitOps. Manual publication requires `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`.
- K3s desired tag `12d63b4` resolves to old source commit `12d63b495346dbff8fcba87e976f9e15165c0ebb` (2026-05-20) and lacks linux/arm64 manifest. Do not republish/promote while decommission is approved; complete retirement gates instead.
- Fresh K3s snapshot (15:19:13Z) is within freshness budget; storage-clean for target namespaces but Media runner active and external backup/retention, remote unregister and authoritative DNS remain blockers.
- Native schedule re-query at 15:23:42Z found no new events; issue #1497 comment #6743818812. No cron or TCE market-scan changes.

---

## 2026-11-09 22:23 ICT — native schedule recheck

- Re-query of the latest 100 master runs found no new native schedule events. Ages at 15:23:42Z: Platform reconcile 30,562s/2,700s budget; inspection 20,774s/4,500s; recovery 32,985s/2,700s; watchdog 32,628s/2,700s; TCE WF-06 20,819s/1,500s; WF-12 24,062s/1,500s. Inter-arrival gaps unchanged. Issue #1497 comment #6743818812 records this recheck. Push inspection #42643433567 is not schedule acceptance.
- Fresh K3s snapshot (15:19:13Z) is 269s old at 15:23:42Z; node Ready, 56% disk, ~21 GiB free, ~19 GiB RAM, restart required. Stock desired ARM64 pods still ImagePullBackOff; Media 1/1; MicroFE Shell/WS/NATS 1/1; TCE/Auth/Keycloak 0/0; public OIDC 503.
- Decommission storage preflight is clean, but runner service/listener remains active and backup/retention, remote unregister and DNS ownership remain unverified. No deletion.
- Platform master `0c932b81`; PR #1525 and #1526 merged. PR #1527's previous exact-head validation #42644190684 passed; new final head must be revalidated.
- No production rollout/mutation or cron/TCE market-scan schedule change.

---

## 2026-11-09 22:21 ICT — fresh inspection and decommission readiness

- Platform master `0c932b81` includes read-only inspection PR #1526, generated from run #42643433567 at 15:19:13Z and exact-head validated before squash merge. Snapshot age at 15:21:18Z was ~125 seconds (within 4,500s).
- K3s node Ready/ARM64; disk 56% (~21 GiB free), RAM available ~19 GiB; host restart required. Platform and dedicated Media runner services remain active/enabled.
- Fresh workloads: Media backend/frontend 1/1 with digest evidence; MicroFE shell/WS/NATS 1/1; Keycloak/Auth 0/0; TCE frontend/service 0/0; public SSO OIDC returns HTTP 503.
- Stock Admin (2 pods) and desired Backend (1 pod) remain ImagePullBackOff due missing linux/arm64 manifest for GHCR tag `12d63b4`; legacy Backend/Frontend remain 1/1 and do not validate the desired image.
- Decommission storage preflight: no target PVC/PV claim/VolumeSnapshot references; only `k3s-debug` PVC remains. Shared retired-manifest guard passed. Deletion remains blocked by active Media runner/listener, unverified remote runner unregister, external backup/retention and authoritative DNS ownership; namespaces still contain workloads, Services, Ingresses and Secrets.
- PR #1525 merged at `542e3d37`; exact-head and post-merge checks PASS. Scheduler evidence remains issue #1497 comment #6743653448; native schedule acceptance is still outside budgets and administrator telemetry is outstanding.
- TCE app build/format/tests PASS but strict public health checks fail HTTP 503; TCE/Auth remain intentional 0/0. Stock CI PASS 7/7 but current-master authenticated scraper preflight/digest publication unverified. Media/Auth CI PASS without current production digest handoff.
- Other master heads: TCE `65af89f6`, Stock `b1b5e177`, Media `dcd69869`, Authentication `b7183475`. Open owner-decision drafts: Platform #1314/#544/#541/#539 and Auth #76.
- No production publication/promotion/apply/rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. No cron or TCE market-scan schedule changes.

---

## 2026-11-09 22:19 ICT — decommission guard and readiness delta

- Platform master `542e3d37`; PR #1525 merged after exact-head `validate-manifests` #42643198502, `validate-github-actions` #42643198496 and `keycloak-ci` #42643198522 PASS. Post-merge #42643433458/#42643433572/#42643433668 PASS.
- New shared guard `scripts/verify-retired-production-manifests.sh` is invoked by manifest validation and by the Stock/Media namespace decommission preflight. It fails closed if `apps/stockdividend` or `apps/media-generation` reappears, if active production trees reference `stock-prod`/`media-prod`, or if retired GHCR image paths return. Regression suite: 1 positive and 5 negative fixtures PASS; workflow contract validator PASS.
- Decommission remains manual-only. The guard is not a delete authorization: backup/retention, authoritative DNS, Media runner service/process/GitHub registration, typed confirmations, production Environment and fresh storage checks remain mandatory.
- Post-merge `inspect-vps` run #42643433567 was in progress at 15:19:08Z; until it completes and publishes a new snapshot, the committed 09:37:36Z snapshot remains stale (~5h41m). Push recovery #42643433651 success is not native schedule evidence.
- Latest native schedule evidence is issue #1497 comment #6743653448. All six tracked Platform/TCE native gaps and ages remain beyond existing budgets; administrator scheduler delivery telemetry is still required. No cron or TCE market-scan changes.
- TCE application build/format/test PASS; public WF-06 probes remain HTTP 503 and WF-12 freshness is stale. Stock CI PASS 7/7 but current-master authenticated scraper preflight and production digest publication are unverified. Media and Auth CI PASS; neither has a current production digest handoff. TCE/Auth remain intentional 0/0.
- Current master heads: Platform `542e3d37`, TCE `65af89f6`, Stock `b1b5e177`, Media `dcd69869`, Authentication `b7183475`. Open drafts: Platform #1314/#544/#541/#539; Authentication #76.
- Production publication/promotion/apply/rollout, scaling, deletion, runner retirement, DNS/database/storage mutation and host maintenance were not performed. `reconcile-vps.yml` remains the only apply authority; `inspect-vps.yml` remains read-only.

---

## 2026-11-09 21:25 ICT — post-merge readiness delta

- Platform master `81191ee4`; PR #1523 exact-head validate-manifests #42634259014 and post-merge master push #42634355055 PASS. PR #1522 exact-head validate-github-actions #42633638893 / validate-manifests #42633638946 and post-merge #42633860020/#42633860140 all PASS. The GitOps-ready verifier rejects duplicate promotion-job evidence (4 positive, 26 negative self-tests). Open human-decision drafts #1314/#544/#541/#539.
- TCE master `65af89f6`; WF-01/WF-02/WF-05 PASS; native and manual WF-06 fail all four strict HTTP 200 probes with HTTP 503; native WF-12 freshness failure remains. No open PR.
- Stock master `b1b5e177`; CI #42610360402 PASS 7/7. Current-master authenticated VNSTOCK preflight and production digest publication are not verified. No open PR.
- Media master `dcd69869`; CI #42539512417 PASS; no new publisher run or Platform handoff. Runner retirement, external backup/retention and DNS ownership remain gated. No open PR.
- Authentication master `b7183475`; CI #42586362115 PASS; draft #76 remains open; no production release run.
- Issue #1497 comment #6742393810 records the current TCE schedule ages and the Platform first-page pagination limitation. Scheduler-side enqueue/delivery evidence from GitHub administrator is still outstanding. Preserve all cron/freshness budgets and TCE market-scan schedule.
- K3s inspection snapshot generated 09:37:36Z remains stale (>4,500s); no runtime mutation is authorized from it.
- App repositories own tests/builds and immutable GHCR publication; Platform alone owns manifests, shared pull credentials, provenance/digest/ARM64 verification, GitOps promotion/apply, rollout/health and protected decommission. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only; no direct SSH/Compose authority.
- No production publication/promotion/apply/rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-09 21:22 ICT — workflow ownership and readiness delta

- Platform master `49e5e764`; PR #1522 merged after exact-head `validate-github-actions` #42633638893 and `validate-manifests` #42633638946 PASS; post-merge master push #42633860020/#42633860140 PASS. The GitOps-ready dispatch verifier now requires exactly one matching completed-success promotion job for each app-specific promotion gate and rejects duplicates (4 positive, 26 negative self-test cases). Open owner-decision drafts: #1314/#544/#541/#539.
- TCE master `65af89f6`; WF-01/WF-02/WF-05 pass. Native WF-06 #42594757482 and manual WF-06 #42594805077 fail all four strict public probes with HTTP 503; native WF-12 #42587926693 fails freshness. WF-13/WF-12 workflow_run fallbacks do not count as native schedule acceptance. No open PR.
- Stock master `b1b5e177`; CI #42610360402 PASS 7/7, including scraper side-effect-free credential preflight contract and ARM64 non-publishing build. Current-master authenticated VNSTOCK credential preflight and production digest publication remain unverified. No open PR.
- Media master `dcd69869`; CI #42539512417 PASS. No new publisher run or Platform handoff; runner remote registration, external backup/retention and DNS ownership remain unverified. No open PR.
- Authentication master `b7183475`; CI #42586362115 PASS; no production release run. Draft PR #76 remains open.
- TCE native WF-06/WF-12 ages at 14:21:58Z are 17,115s/20,358s versus 1,500s budgets. Platform's latest unfiltered first page (30 items) has no schedule event; this is a pagination-limited observation, not proof of no newer event. Last fully filtered Platform evidence remains 13:04:20Z. Issue #1497 updated with comment #6742393810; administrator scheduler enqueue/delivery evidence remains required.
- K3s inspection snapshot generated 09:37:36Z is 17,062s old (>4,500s budget). Do not authorize runtime mutation from this snapshot.
- App repositories continue to own tests/builds and immutable GHCR publication; Platform alone owns production manifests, shared pull credentials, source/run-attempt provenance, digest/ARM64 verification, GitOps promotion/apply, rollout/health and protected decommission. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only; no duplicate SSH/Compose authority.
- No production publication/promotion/apply/rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-09 20:04 ICT — workflow ownership and readiness delta

- Platform master `f9984d4d`; PR #1520 exact-head validate-manifests #42614267017 and post-merge push #42614397667 PASS. Open human-decision drafts #1314/#544/#541/#539.
- TCE master `65af89f6`; WF-01P/WF-02/WF-05 pass. Native WF-06 #42594757482, manual WF-06 #42594805077 and native WF-12 #42587926693 fail. WF-06 job evidence has all four public probes failed; TCE/Auth intentional 0/0 is not live health. No open PR.
- Stock master `b1b5e177`; CI #42610360402 PASS 7/7. The older scheduled scraper failure #42457182511 used SHA `e6469ac`; current master credential state is unverified. No open PR or production publisher/digest handoff.
- Media master `dcd69869`; CI #42539512417 PASS. Latest inspection shows dedicated runner service active/enabled and listener present; remote registration, external backup/retention and DNS ownership remain unverified. No open PR.
- Auth master `b7183475`; CI #42586362115 PASS; draft PR #76 remains open.
- Native schedule API query at 13:04:20Z: Platform reconcile/inspection/recovery/watchdog gaps 24,326s/27,768s/22,459s/22,698s; ages 22,200s/12,412s/24,623s/24,266s. TCE WF-06/WF-12 gaps 27,454s/25,452s; ages 12,457s/15,700s. All exceed budgets. Issue #1497 comment #6740838807 requests authoritative administrator delivery/enqueue evidence.
- Latest K3s inspection #42594848960 is stale for rollout/decommission: snapshot generated 09:37:36Z, age 12,404s (>4,500s). Do not use it for runtime authorization.
- Scheduled reconciliation #42575932602 succeeded with no manifest drift; Auth runtime Secret provisioned/verified; shared `ghcr-pull` unchanged; no image-pull failures in MicroFE/TCE targets; production apply and rollout checks skipped. Public TCE WF-06 remains failed independently.
- App repositories continue to own tests/builds and immutable GHCR publication; Platform alone owns manifests, shared pull credentials, provenance/digest/ARM64 checks, GitOps promotion/apply, rollout/health. `reconcile-vps.yml` is sole apply authority; `inspect-vps.yml` is read-only. No duplicate SSH/Compose authority.
- No production publication/promotion/apply/rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.

---

## 2026-11-09 19:00 ICT ownership and readiness delta

- Platform master `5647035a`; PR #1519 exact-head #42610714863 and post-merge #42610795648 PASS; PR #1518 post-merge #42609219961 PASS. Open human-decision drafts #1314/#544/#541/#539.
- TCE master `65af89f6`; WF-01P/WF-02/WF-05 last verified PASS. Native WF-06 #42594757482 and manual WF-06 #42594805077 fail four strict public probes with HTTP 503; TCE/Auth intentional 0/0 is not live health. No open PR.
- Stock master `b1b5e177`; PR #41 exact-head and post-merge CI #42609809654/#42610360402 both PASS 7/7, including non-publishing ARM64 builds. No publisher/digest handoff. Current `VNSTOCK_API_KEY` state is unverified; last scraper failure used older SHA. No open PR.
- Media master `dcd69869`; CI #42539512417 PASS. Dedicated runner active/enabled/listener-present in stale snapshot; remote registration and external backup/DNS remain unverified. No open PR.
- Auth master `b7183475`; CI #42586362115 PASS; PR #76 remains draft.
- Native schedule query filtered to `event=schedule`: Platform reconcile/inspection/recovery/watchdog gaps 24,326s/27,768s/22,459s/22,698s; TCE WF-06/WF-12 gaps 27,454s/25,452s. All exceed budgets. Issue #1497 updated with current evidence; GitHub administrator must provide scheduler enqueue/delivery telemetry. No cron/freshness changes.
- Latest inspection #42594848960 snapshot generated 09:37:36Z, stale at 19:00 ICT. No runtime mutation may be authorized from it. Latest workflow_dispatch reconciliation #42595146384 had drift=false/apply skipped and no image changes; repository_dispatch recovery #42595660819 is not native acceptance.
- App repos own tests/builds and immutable GHCR publication. Platform owns manifests, shared pull credentials, digest/provenance validation, GitOps promotion/apply, rollout/health and protected decommission. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only; no direct SSH/Compose authority. TCE market-scan schedule unchanged.

## 2026-11-09 18:23 ICT ownership and readiness delta

- Platform master `43487426`; PR #1518 merged after exact-head validate-manifests #42608166754 PASS. PR #1517 final Media runner audit change is merged with exact-head and post-merge validate-github-actions/validate-manifests all PASS.
- TCE master `65af89f6`; WF-01/WF-02/WF-05 last verified PASS; WF-06 four public health probes last confirmed HTTP 503; WF-12 stale-delivery evidence remains.
- Stock master `b1b5e177`; PR #41 merged from exact head `b212fa0c`. Exact-head CI #42609809654 passed all seven jobs, including native ARM64 non-publishing builds. The release-contract validator now enforces the exact scraper step sequence and confines MongoDB/Telegram secrets to the ingestion step. No scraper dispatch or production publication.
- Media master `dcd69869`; application CI #42539512417 last verified PASS. Dedicated runner retirement and external backup/DNS prerequisites remain unresolved.
- Authentication master `b7183475`; CI #42586362115 last verified PASS; PR #76 remains draft.
- Open PRs: Platform #1314/#544/#541/#539 and Authentication #76. TCE, Stock and Media have none.
- Reconciliation #42595146384 is workflow_dispatch; recovery #42595660819 is repository_dispatch. Neither is native schedule acceptance. Auth runtime Secret provisioned/verified; shared `ghcr-pull` unchanged; drift false; apply/promotion skipped.
- Latest complete native schedule evidence is 11:17:20Z; issue #1497 remains administrator-owned. Connector master-run enumeration is incomplete; do not infer no later events. Preserve all cron/freshness budgets and TCE market-scan schedule.
- Latest K3s snapshot #1515 remains generated 09:37:36Z and is stale beyond the 75m budget. Stock tag `12d63b4` lacks ARM64 manifest; TCE/Auth/Keycloak 0/0; Media/MicroFE 1/1 in that point-in-time snapshot. No rollout/decommission authorization.
- App repos own tests/builds and immutable GHCR publication; Platform owns production manifests, shared pull credentials, digest/provenance validation, GitOps promotion/apply, rollout/health and protected decommission. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only; no direct SSH/Compose authority.

Current review: **2026-11-09 18:23 ICT**

# Cross-repo workflow inventory and deployment ownership

## 2026-11-09 18:17 ICT ownership and readiness delta

- Platform PR #1517 merged at `f480b8e3fbca130e0d64277983a9c12e55a470f7`. Exact-head validate-github-actions #42607555613 and validate-manifests #42607555700 PASS; post-merge push validate-github-actions #42607717790 and validate-manifests #42607718023 PASS.
- Final Stock/Media namespace-delete step now re-runs the dedicated Media runner local/GitHub registration audit immediately before deletion and unsets the read-only audit token before invoking the namespace script. Existing typed confirmations, production Environment, fresh storage preflight and root-owned wrapper remain mandatory. No deletion or runner retirement occurred.
- Current masters: Platform `f480b8e3`, TCE `65af89f6`, Stock `1a18cabf`, Media `dcd69869`, Auth `b7183475`. Open drafts: Platform #1314/#544/#541/#539 and Auth #76.
- Latest app CI remains PASS: TCE WF-01/WF-02/WF-05 #42586355695/#42586356008/#42586355696; Stock #42533562194 (7/7, non-publishing ARM64); Media #42539512417; Auth #42586362115.
- No new native schedule events since 11:02Z. Platform reconcile/inspection/recovery/watchdog gaps remain 24,326s/27,768s/22,459s/22,698s; TCE WF-06/WF-12 gaps remain 27,454s/25,452s. All ages/gaps exceed existing budgets. Issue #1497 remains administrator-owned; no cron/budget change.
- Platform reconciliation #42595146384 was workflow_dispatch: Auth runtime Secret provisioned/verified, shared `ghcr-pull` unchanged, no drift, apply/image promotion skipped; TCE/Auth zero-replica maintenance not live health. Recovery #42595660819 was repository_dispatch fallback.
- Stock manual `run_scraper.yml` `preflight_only=true` is available to verify current `VNSTOCK_API_KEY` and authenticated tier without ingestion; current secret state remains unverified until the owner runs it. Stock desired image still lacks ARM64 evidence.
- Latest K3s snapshot #1515 is ~100m old and beyond the 75m inspection budget. No rollout/decommission authorization is inferred. Media external backup/retention, DNS and remote runner registration remain unverified.
- App repos own tests/builds and immutable GHCR publication; Platform owns manifests, shared pull credentials, digest/provenance validation, GitOps apply, rollout and health. `reconcile-vps.yml` sole apply authority; `inspect-vps.yml` read-only; no direct SSH/Compose authority. TCE market-scan schedule unchanged.

## 2026-11-09 18:02 ICT execution and ownership refresh

- Current masters: Platform `7c6f2b32`; TCE `65af89f6`; Stock `1a18cabf`; Media `dcd69869`; Authentication `b7183475`.
- Latest master push CI: Platform #42599052606 PASS; TCE WF-01 #42586355695, WF-02 #42586356008 and WF-05 #42586355696 PASS; Stock #42533562194 PASS 7/7 with non-publishing ARM64 builds; Media #42539512417 PASS; Auth #42586362115 PASS.
- Open drafts: Platform #1314/#544/#541/#539 and Auth #76. Platform PR #1517 adds a final-step Media runner re-audit immediately before protected namespace deletion; exact-head validation pending. No app publisher PR remains open.
- Latest reconciliation #42595146384 is workflow_dispatch, not schedule: Auth runtime Secret provisioned/verified, shared `ghcr-pull` unchanged, no active MicroFE/TCE image-pull failures, drift=false, manifest apply/image promotion skipped. TCE/Auth 0/0 maintenance is not live health. Recovery #42595660819 is repository_dispatch fallback, not native acceptance.
- Native schedule gaps: Platform reconcile 24,326s / inspection 27,768s / recovery 22,459s / watchdog 22,698s; TCE WF-06 27,454s / WF-12 25,452s. All exceed existing budgets; current ages also exceed freshness budgets. Issue #1497 has been updated with exact run IDs, gaps and ages. No cron/budget or TCE market-scan changes.
- TCE WF-06 #42594757482 was delivered natively but all four public endpoints returned HTTP 503. TCE/Auth remain intentional 0/0; strict health probes remain failures.
- Latest K3s snapshot #1515 generated 09:37:36Z is 85m old and beyond the 75m inspection budget. Node Ready/ARM64, disk 56%, RAM ~19 GiB, restart required; Media/MicroFE 1/1 with digest evidence; Stock desired tag 12d63b4 fails ARM64 manifest resolution; TCE/Auth/Keycloak 0/0.
- Stock/Media decommission remains blocked by external backup/retention, authoritative DNS ownership and remote Media runner registration. PR #1517 tightens final-step runner retirement verification but performs no deletion.
- App repos continue to own tests/builds and immutable GHCR publication; Platform alone owns production manifests, shared pull credentials, digest/provenance validation, GitOps apply, rollout and health. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority.

Current review: **2026-11-09 18:17 ICT / 2026-11-09 11:17 UTC**

## 2026-11-09 17:00 ICT inspection and evidence refresh

- Platform master includes inspection snapshot #1515 at `9530a7ab`; `debug/vps-latest.md` generated 09:37:36Z. Node Ready/ARM64; disk 56%, ~21 GiB free; available RAM ~19 GiB; host restart required. Docker reports 5.773 GB reclaimable; no cleanup was run.
- Media backend/frontend and MicroFE Shell/WS/NATS are 1/1 with registry digest evidence. Stock Admin×2 and desired Backend fail to pull tag `12d63b4` because the registry manifest has no matching linux/arm64 platform. Legacy Stock Backend/Frontend remain 1/1 but lack RepoDigest evidence. TCE frontend/service, MicroFE Auth and Keycloak remain 0/0; public OIDC probes return 503.
- Stock/Media storage preflight reports no namespace PVC/PV claims or VolumeSnapshots; both namespaces still contain Secrets/TLS credentials, workloads, Services and Ingresses. DNS ownership, external backup/retention and remote Media runner registration remain unverified. Platform and Media runner services remain active/enabled.
- Platform PR #1514 exact-head validate-manifests #42591267072 PASS; PR #1512 #42587680995 PASS. TCE PR #1032 runs #42585765728/#42585765734/#42585765722/#42585765835 PASS (WF-08B publisher/dispatch skipped on PR event). Stock CI #42533247153 7/7 PASS with non-publishing ARM64 builds; Media #42539297802 PASS; Auth #42585818369 PASS.
- Correct TCE WF-08B run ID is #42585765835; the previous #42585865835 value in the 15:15 checkpoint was a typo and is corrected.
- Current master heads: Platform `9530a7ab`, TCE `65af89f6`, Stock `1a18cabf`, Media `dcd69869`, Auth `b7183475`. Open drafts: Platform #1314/#544/#541/#539; Auth #76. No open PRs in TCE/Stock/Media.
- Native schedule issue #1497 remains open; current cadence is unverified beyond the 05:02:47Z all-event evidence. No cron/freshness changes; TCE market-scan schedule unchanged.
- No production publication, promotion, apply, rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.

## 2026-11-09 16:03 ICT publisher-provenance and inspection delta

- Platform PR #1512 is merged at `296665e832964124f34fd768bafbfa8bddd925d9`; exact-head `validate-manifests` #42587680995 PASS. Documentation-only; no post-merge push result is claimed.
- Correct TCE WF-08B exact-head run ID is #42585765835. Its MicroFE test jobs passed and publish/dispatch jobs were skipped on the PR event. The previous #42585865835 reference was a typo and returned 404.
- Current masters: Platform `296665e8`, TCE `65af89f6`, Stock `1a18cabf`, Media `dcd69869`, Authentication `b7183475`.
- TCE #1032, Auth #91 and Platform #1511 are merged with exact-head validations passed. TCE WF-03/WF-08B and Auth release now emit positive `source_run_attempt`; Platform validates it against the public Actions run API and the required publisher job evidence.
- Latest inspection snapshot #1513 was generated at 08:38:41Z: node Ready/ARM64; Media and MicroFE 1/1 with digest evidence; Stock desired images ImagePullBackOff due missing ARM64 manifest; TCE/Auth/Keycloak 0/0 and public OIDC 503; Media runner service active/enabled. This is point-in-time read-only evidence, not rollout/decommission authorization.
- Native schedule issue #1497 remains open; latest authoritative all-event evidence remains 05:02:47Z and no cadence recovery is claimed. Preserve cron, budgets and TCE market-scan schedule.
- No production publication, promotion, apply, rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.

Current review: **2026-11-09 15:15 ICT / 2026-11-09 08:15 UTC**

## 2026-11-09 15:15 ICT publisher provenance delta

- TCE PR #1032 and Authentication PR #91 are squash-merged; app-side dispatches now carry positive numeric source_run_attempt values alongside run ID, workflow path, event and source SHA.
- Platform PR #1511 is squash-merged; the three active publisher lanes (TCE, MicroFE and Auth) compare the payload attempt with run_attempt returned by the public Actions run API before accepting digest promotion. Missing, malformed and mismatched attempts fail closed. Regression tests cover missing and mismatched API evidence.
- Exact-head checks: TCE #42585765728/#42585765734/#42585765722/#42585765835 PASS; Auth #42585818369 PASS; Platform #42587040047 and #42587039974 PASS.
- Current masters: Platform 3d9063a8; TCE 65af89f6; Stock 1a18cabf; Media dcd69869; Auth b7183475. PR-only run/status queries returned no post-merge entries for the merge commits; this is not evidence that push/schedule/dispatch runs do not exist.
- Native schedule issue #1497 remains open. The last authoritative all-event evidence remains the 01:59Z snapshot; no cadence recovery is claimed. Preserve all cron expressions, budgets and TCE market-scan scheduling.
- Latest K3s snapshot remains debug/vps-latest.md generated 07:10:37Z and is stale for rollout/decommission decisions. No fresh read-only inspection result was exposed in this run.
- No production dispatch, GHCR publication/promotion, manifest apply, rollout, scaling, namespace/storage deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.

## 2026-11-09 14:00 ICT execution delta

- Platform master observed at inspection commit `1a9c9b9b1c3cb550f9904f65a50ed87df0c157cb`; PR #1505 exact-head validation #42570696070 PASS and PR #1504 post-merge #42565271145 PASS. The connector does not expose all push/schedule/dispatch runs for master commits.
- TCE Dashboard master `ddf5811a`: unit test #42538802541 PASS; WF-06 #42548397383 fails all four strict public health probes (HTTP 503). Keep HTTP 200 acceptance.
- StockDividend master `1a18cabf`: CI #42533562194 PASS 7/7 with publishing disabled. Scraper #42457182511 failed on empty VNSTOCK_API_KEY at older source SHA `e6469ac`; current master secret state is unverified.
- Media master `dcd69869`: application test/build #42539512417 PASS. Authentication master `047abc08`: ARM64 non-publishing build/validation #42539350154 PASS.
- Fresh K3s snapshot #1506 generated 06:16:06Z: node Ready/ARM64; Media/MicroFE active workloads 1/1; Stock Admin desired image pull fails on missing ARM64 manifest and legacy Stock image digests are unavailable; TCE/Auth/Keycloak 0/0; OIDC 503. Media runner remains active/enabled. Stock/Media storage preflight is clean in-cluster, but namespaced Secrets/workloads remain and will be deleted with their namespaces; external backup/retention and DNS review are outstanding.
- Decommission defense-in-depth follow-up requires the runner-retirement attestation in the workflow's final delete step, namespace script and root-owned wrapper, not only the preceding workflow validation/remote audit step. Regression tests reject missing/mismatched runner attestations. Remote GitHub runner absence still comes only from the protected read-only API audit.
- Native schedule cadence remains unverified after the 05:02:47Z all-event snapshot in issue #1497. Preserve cron and budgets. TCE market-scan schedule unchanged.
- No production publication/promotion/apply/rollout/scaling, namespace or storage deletion, runner retirement, DNS/database/storage mutation, or host maintenance occurred.
- Platform PR #1507 merged at `a619815d` from exact head `e65dbb62`; exact-head `validate-github-actions` #42577373795 and `validate-manifests` #42577373702 PASS. Current master is inspection PR #1508 commit `1433711b`; the latest read-only K3s snapshot was generated 07:10:37Z. Post-merge CI for #1507 is unverified.

| Repository | App-owned workflows and release contract | Platform-owned responsibilities / boundary | Current evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives provenance-bound TCE/Auth/MicroFE digest events including exact source run-attempt attestation; owns native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `3d9063a8`; PR #1511 merged from exact head `ab8d7daa`, exact-head validate-github-actions #42587040047 and validate-manifests #42587039974 PASS. The run-attempt gate binds TCE/MicroFE/Auth payloads to public Actions run_attempt. Latest K3s snapshot remains 07:10:37Z and is stale; native schedule issue #1497 remains open. Last known workflow_dispatch reconcile #42546651537 PASS: Auth runtime Secret provisioned/verified, `ghcr-pull` unchanged, no drift, apply/promotion/rollout skipped. |
| TCE Dashboard | App-owned CI/tests; manual WF-03 ARM64 immutable web/service publisher with digest verification and provenance-bound `tce-release-requested` handoff carrying exact source_run_attempt; WF-08B MicroFE ARM64 publisher and digest-bound Platform handoff with the same attempt attestation; WF-06/WF-07/WF-12/WF-13 health, integration, watchdog and recovery. WF-09 remains a safe manual VPS utility; WF-10 remains staging-only. | No production SSH/Compose/K3s apply authority. Platform alone owns production manifests, runtime Secrets, image promotion/reconciliation and health. | Master `65af89f6`; PR #1032 merged from exact head `d9b5dc69`; WF-01P #42585765728, WF-02 #42585765734, WF-05 #42585765722 and WF-08B #42585765835 PASS. WF-06 #42548397383 still failed 4/4 HTTP 503; WF-12 #42546629459 stale-delivery failure remains latest confirmed evidence. No open PR. Market-scan schedule unchanged. |
| StockDividend | CI/tests; deploy.yml is the app-owned ARM64 GHCR publisher for Scraper/Admin/Backend, using full-SHA and version/full-SHA tags, pre-push tag-absence guard, digest equality and ARM64 checks. Weekend scraper cron remains separate and fail-closed on `VNSTOCK_API_KEY`. | Retired from active Platform GitOps; legacy namespace/workloads await protected decommission. No production SSH/Compose authority. | Master `1a18cabf`; CI #42533562194 all 7 jobs PASS, ARM64 builds use push=false. Last observed scraper #42457182511 failed closed on empty `VNSTOCK_API_KEY` on older commit `e6469ac`; current secret state is unverified. Desired Stock `12d63b4` lacks ARM64 manifest in the stale K3s snapshot. No open PR. |
| Media Generation | CI/tests; app-owned master-push/manual ARM64 publisher verifies immutable version/full-SHA images, pre-push tag absence and registry digests. No Platform handoff while retired. | No active Platform GitOps handoff; legacy namespace and dedicated runner await protected decommission. No direct SSH/Compose production authority. | Master `dcd69869`; CI #42539512417 PASS. Latest snapshot shows backend/frontend 1/1 with RepoDigest; dedicated runner active/enabled/listener-present. No open PR. Decommission still blocked by external backup/retention, DNS and runner-registration evidence. |
| Authentication | CI/tests; release.yml is workflow_dispatch-only app publisher with ARM64, provenance/SBOM, SHA/version tag preflight, digest verification and `auth-image-published` handoff carrying exact source_run_attempt. | Platform owns runtime manifests/Secrets, digest-pinned GitOps promotion/apply, rollout and health. | Master `b7183475`; PR #91 merged from exact head `00ce65bb`; auth-service-ci #42585818369 PASS. PR #76 remains draft. Auth runtime Secret verified by latest reconcile, but Auth/Keycloak remain 0/0 and no live health is asserted. |

## Previous execution evidence — 2026-11-09 08:59 ICT / 01:59 UTC (reconciliation evidence corrected in the 09:05 checkpoint below)

| Workflow | Latest native run | Previous native run | Gap | Budget |
|---|---|---|---:|---:|
| Platform reconcile | #42538596496 PASS, 00:08:54Z | #42521088881, 20:37:39Z | 12,675s | 2,700s |
| Platform inspection | #42548015626 PASS, 01:54:40Z | #42530192980, 22:25:47Z | 12,533s | 4,500s |
| Platform recovery | #42537793367 PASS, 23:59:38Z | #42520213983, 20:27:31Z | 12,727s | 2,700s |
| Platform watchdog | #42537967026 FAIL, 00:01:36Z | #42520452305, 20:30:24Z | 12,672s | 2,700s |
| TCE WF-06 | #42548397383 FAIL, 01:59:09Z | #42531446260, 22:41:01Z | 11,888s | 1,500s |
| TCE WF-12 | #42546629459 FAIL, 01:38:28Z | #42527713763, 21:56:51Z | 13,297s | 1,500s |

All six native inter-arrival gaps exceed the existing budgets. TCE WF-06 #42548397383 executed but all four public endpoints returned HTTP 503. WF-12 #42546629459 observed WF-06 age 10,647s with 0m queue wait. Platform watchdog #42548211945 failed. See [Platform issue #1497](https://github.com/phanthienquoc/platform-infra/issues/1497) for the external schedule-delivery investigation. Do not weaken budgets or count fallback events.

### Current runtime and ownership evidence

- Platform master is `e5288041`; inspection PR #1496 merged after read-only inspection #42548015626. Current `debug/vps-latest.md` was generated 01:54:48Z.
- StockDividend master CI #42533562194 passed all seven jobs, including non-publishing ARM64 builds. Scraper #42457182511 fails closed because `VNSTOCK_API_KEY` is empty. No production image publication/digest handoff is evidenced.
- Media CI #42539512417 and Authentication CI #42539350154 PASS. Auth PR #76 remains draft.
- K3s snapshot: node Ready/ARM64; Media and MicroFE active workloads 1/1; Stock Admin×2 and desired Backend are not ready because tag `12d63b4` has no matching ARM64 manifest; cached Stock `23b2878` images lack RepoDigest. TCE/Auth/Keycloak are intentional 0/0.
- Media and Platform runner services remain active/enabled with listeners present. Host restart is required; Docker reports 5.773 GB reclaimable. No runner retirement, image cleanup, package upgrade or reboot.
- Stock/Media PVC/PV and VolumeSnapshot preflight is clean in those namespaces, but external backup/retention, DNS ownership and Media remote runner registration remain unverified. Decommission remains blocked.
- Latest workflow_dispatch reconcile #42546651537: GHCR read access PASS for Auth/MicroFE/TCE; Auth runtime Secret provisioned/verified; shared `ghcr-pull` unchanged; `drift=false`; manifest apply and image promotion skipped; rollouts skipped. TCE/Auth zero-replica maintenance was recognized without asserting live health. Post-reconcile recovery #42546778524 PASS. Later TCE-heartbeat recovery #42548422877 PASS and avoided duplicate fallback because reconciliation was 19m old and inspection 4m old. Latest native scheduled reconcile remains #42538596496.

### Open PRs and owner dependencies

- Platform #1314/#544/#541/#539 remain draft; Authentication #76 remains draft. TCE, StockDividend and Media Generation have no open PRs.
- GitHub administrator: investigate native schedule delivery under issue #1497.
- Stock owner: provide `VNSTOCK_API_KEY`, run safe preflight, then approve and publish ARM64 artifacts with digest evidence.
- TCE/Auth owners: resolve four public HTTP 503 paths while keeping strict checks and 0/0 maintenance until approved.
- Media owner: verify runner registration, external backup/retention and DNS before decommission.
- Platform operator: maintenance window/rollback required before host update or reboot.

Safety: no production publish/promotion/apply/rollout, no scaling, no namespace/PVC/PV deletion, no runner retirement, no DNS/database/storage mutation. `reconcile-vps.yml` remains sole apply authority; `inspect-vps.yml` is read-only. TCE market-scan schedule unchanged.

## Latest reconciliation/recovery evidence — 2026-11-09 09:05 ICT / 02:05 UTC

- Platform PR #1498 merged at `346ecfed57fdd1179abda8c114574d9e3dd575a3`; exact-head `validate-manifests` #42548807576 PASS and post-merge #42548906576 PASS.
- Latest completed reconciliation is workflow_dispatch #42546651537 (01:38:43Z; source master `3ea55b827c85c2e2e815fecaa067a99edc0ed043`), inputs `mode=apply`, `target_app=all`, `allow_image_changes=false`. GHCR access for Auth/MicroFE/TCE passed; Auth runtime Secret was provisioned and verified; shared `ghcr-pull` remained unchanged; no drift; production manifest apply and image promotion skipped.
- MicroFE health passed. TCE/Auth lanes recognized intentional 0/0 maintenance and did not assert live health; rollouts and Keycloak lane skipped. Final deployment gate passed. Recovery controller #42546778524 passed.
- TCE heartbeat recovery #42548422877 passed for source WF-06 #42548397383. It observed reconciliation #42546651537 age 19m and inspection #42548015626 age 4m, so no duplicate fallback dispatch was needed. This does not count as native schedule acceptance.
- Latest native scheduled reconciliation remains #42538596496. The native schedule table above/below remains unchanged: all six inter-arrival gaps exceed their existing budgets. Latest TCE WF-06 #42548397383 returned HTTP 503 on all four strict endpoints.
- Latest K3s snapshot #42548015626 remains unchanged: node Ready/ARM64; Media/MicroFE 1/1; Stock Admin×2 and desired Backend fail on missing ARM64 manifest for `12d63b4`; cached `23b2878` images lack RepoDigest; TCE/Auth/Keycloak 0/0; Media runner active/enabled. Host restart required; no maintenance or decommission.
- Stock CI #42533562194 all seven jobs PASS with push=false ARM64 builds; scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`. Media #42539512417 and Auth #42539350154 PASS. Open drafts: Platform #1314/#544/#541/#539 and Auth #76.
- No production image publication/promotion, manifest apply, workload scaling, namespace/storage deletion, runner retirement, DNS/database/storage mutation or host maintenance. Auth runtime Secret provisioning is the only confirmed production mutation in the latest reconcile; shared `ghcr-pull` was unchanged. TCE market-scan schedule unchanged.

## Previous checkpoint schedule table (08:59 ICT; superseded by the 09:05 reconciliation evidence above)

## Platform workflow schedule and acceptance

| Workflow | Native cron (UTC) | Freshness budget | Latest confirmed native evidence at 08:31 ICT / inter-arrival gap |
|---|---|---:|---|
| reconcile-vps.yml | `7,22,37,52 * * * *` | 45m | #42538596496 PASS at 00:08:54Z; previous #42521088881 at 20:37:39Z; gap 12,675s (budget 2,700s). |
| inspect-vps.yml | `2,32 * * * *` | 75m | #42530192980 PASS at 22:25:47Z; previous #42510125328 at 18:27:47Z; gap 14,280s (budget 4,500s). Snapshot is stale at this review. |
| reconcile-schedule-watchdog.yml | `12,27,42,57 * * * *` | 45m | #42537967026 FAIL at 00:01:36Z; previous #42520452305 at 20:30:24Z; gap 12,672s (budget 2,700s). |
| recover-stale-ops.yml | `10,25,40,55 * * * *` | 45m | #42537793367 PASS at 23:59:38Z; previous #42520213983 at 20:27:31Z; gap 12,727s (budget 2,700s). |
| vps-image-cleanup.yml | `30 3 * * 0` | N/A (weekly dry-run) | #42472343489 PASS at 10:39:26Z, DRY_RUN=true, remove_count=0; no deletion. |

Only original `event=schedule`, master, attempt 1, exact workflow path and full source SHA count as native. Manual, push, workflow_run and repository_dispatch remain separate. Push smoke reports schedule observations as warnings; it does not assert cadence acceptance.

## Historical reconciliation, TCE health and K3s evidence — 2026-11-09 08:31 ICT

### Promotion-ready reconciliation contract

Platform PR #1493 merged at `891a07c06bc541f2df420d6d085d77f49121602d`. Exact-head #42545953263/#42545953756/#42545953254 and post-merge #42546040759/#42546040835/#42546040757 all PASS.

For a `gitops-promoted-ready` event, `reconcile-vps.yml` now requires:
- Exact completed-successful Platform promotion run on master, matching run ID, attempt, workflow path and head SHA.
- Complete Actions job evidence from `actions/runs/{run_id}/jobs?per_page=100`; `total_count` must equal returned job count.
- The expected app-specific promotion job(s) must be completed-successful (MicroFE digest promotion; both TCE promotion and coordinator; Auth promotion).
- Current GitOps manifests must contain exactly one digest-pinned entry per expected image. Immutable source tags must resolve to those exact manifest digests, and digest references must pass the existing linux/arm64 verifier.
- All checks run before Auth runtime Secret provisioning and shared `ghcr-pull` mutation.

No production ready event, image promotion, manifest apply or rollout was triggered by the merge.

### Native TCE schedule and public health

- WF-06 #42531446260 failed at 22:41:01Z; inter-arrival gap 13,481s versus the 1,500s budget. Its job logs reported HTTP 503 from TCE web, TCE API, Auth readiness and Auth liveness.
- WF-12 #42527713763 failed at 21:56:51Z; inter-arrival gap 14,317s versus the 1,500s budget. Its heartbeat succeeded but the native WF-06 freshness gate failed.
- WF-07 integration #42528513790 passed at 22:06:09Z.
- Platform native reconcile/inspection/recovery/watchdog gaps are 12,675s/14,280s/12,727s/12,672s against 2,700s/4,500s/2,700s/2,700s. Inspection queue telemetry was 0m in prior watchdog evidence; scheduler delivery remains the unresolved administrator investigation.
- Do not count manual, push, workflow_run or repository_dispatch runs as native schedule acceptance. Preserve all cron/freshness settings and the TCE market-scan schedule.

### Last known production runtime — snapshot is stale

- Reconciliation #42538596496 PASS at 00:08:54Z: GHCR read access PASS, Auth runtime Secret verified, shared `ghcr-pull` unchanged, `drift=false`, apply/promotion/rollout skipped.
- Latest committed inspection #42530192980 generated 22:25:55Z; stale at this review. It last showed K3s node Ready/ARM64, Media/MicroFE active pods 1/1, Stock Admin×2 and desired Backend ImagePullBackOff from missing ARM64 manifest, and TCE/Auth/Keycloak 0/0.
- Stock `VNSTOCK_API_KEY` remains missing; no current Stock ARM64 publication/digest handoff is evidenced.
- Media runner remains active/enabled/listener-present. Remote registration, external backup/retention and authoritative DNS ownership are unverified; decommission remains blocked.

## Historical reconciliation and production health evidence (earlier checkpoint)

- Native reconcile #42439099803 PASS but stale. Workflow_dispatch reconcile #42452324950 PASS at 05:50:26Z on prior master SHA `5513c0bc...`; GHCR preflight, Auth runtime Secret, shared pull credentials and scoped image-pull restart passed.
- Manifest apply and image-change guard skipped; no image promotion or production rollout. Recovery #42453078467 verified TCE heartbeat and avoided duplicate fallback because reconciliation and inspection were recent.
- TCE/Auth are intentional zero-replica maintenance; lane success is not live-service health. Stock/Media remain outside active rollout scope.

## Historical TCE schedule and health evidence (earlier checkpoint)

- WF-06 remains `*/15 * * * *`; latest native #42432710149 stale; manual #42452331522 failed all four strict probes with HTTP 503.
- WF-12 remains `7,22,37,52 * * * *`; native #42452308083 failed WF-06 freshness. WF-07 scheduled #42453060493 PASS; WF-12 workflow_run #42453071754 failed stale-WF-06 gate; WF-13 #42453081086 recovered; Platform heartbeat #42453078467 passed.
- Keep strict HTTP 200 checks and TCE market-scan schedule unchanged. No replica scaling without explicit owner approval.

## Historical K3s inspection and protected decommission evidence (earlier checkpoint)

- Formal read-only snapshot #42452273701 generated 05:49:48Z. Node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1, containerd 2.3.2-k3s2; RAM ~19 GiB available, disk 56%/~21 GiB free.
- Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1. Stock Admin (two pods) and desired Backend pod ImagePullBackOff on `12d63b4`; kubelet reports no matching platform manifest. Old Stock Backend and Frontend on `23b2878` remain Running.
- TCE/Auth/Keycloak remain 0/0. Stock/Media namespaces Active; no Stock/Media VolumeSnapshot references. External backup/retention and DNS ownership are unverified.
- Docker 29.1.3; 20 images/9.195 GB, ~5.773 GB reclaimable; host containerd.io 2.2.1; `restart_required=yes`. No cleanup, upgrade, reboot or decommission.
- Platform and Media runner services active/enabled; runner-registration audit remains outstanding.

## Cross-repo release boundaries

- App repositories own tests/builds and immutable GHCR publication. Platform alone owns production manifests, shared pull credentials, runtime Secrets, source/digest/provenance gates, GitOps promotion/reconciliation, rollout and health.
- TCE/Auth sender/receiver payloads remain digest-bound and statically aligned. Stock #38 contract is merged; Media/Stock have no active Platform dispatch while retired.
- No new publisher run, GHCR publication, digest handoff or production image promotion in this review.
- No duplicate direct SSH/Compose deployment authority. Stock/Media deletion remains protected by backup, DNS, runner retirement, production approval and fresh PVC/PV/VolumeSnapshot gates.


## Latest execution evidence — 2026-11-08 13:57 ICT / 06:57 UTC

- Platform master: `9f6618f8736ab14d58595436faa87944cc45bb4d`; latest push smoke #42454041525 PASS, warning-only. Native reconcile #42439099803, watchdog #42438566387 and recovery #42438384072 remain outside cadence budgets; native inspection #42452273701 is within age budget but its 21,396s inter-arrival gap exceeds the 75m cadence budget.
- TCE: WF-07 scheduled #42453060493 PASS; WF-12 #42452308083 and its workflow_run freshness check fail; WF-13 #42453081086 recovers heartbeat delivery. Manual WF-06 #42452331522 remains 4/4 HTTP 503. No TCE replicas are changed.
- Stock: master CI #42440810105 PASS. Scraper #42349150261 failed closed on empty `VNSTOCK_API_KEY`; the next Sunday scheduled run is not visible at 06:57Z, but prior Saturday delivery was delayed until 06:56:29Z, so continue observing rather than declaring a missed delivery yet.
- Media: latest recorded master CI #42239703151 PASS; no new publisher evidence.
- Authentication: master CI #42215394539 PASS; PR #75 exact-head CI #40446492086 PASS but merge remains gated by Supabase Deploy-to-production integration behavior; PR #76 exact-head CI #41329425940 PASS and remains draft.
- Open PRs: Platform #1314/#544/#541/#539; Authentication #75/#76. TCE, Stock and Media have none.
- No GHCR publish/promotion, production manifest mutation, workload scaling, decommission, DNS/database/storage change, runner retirement or host maintenance. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 15:04 ICT / 08:04 UTC

- Platform master `564d94bb9134195a0643274f8656d95161b47e02`; inspection PR #1440 merged at exact validated head `9cdfaddc66fbcb21a6ea7a78e05f44551726fa69` (merge SHA `564d94bb9134195a0643274f8656d95161b47e02`). Read-only inspection #42458425146 succeeded; exact-head manifest validation #42458510940 passed.
- Manual reconcile #42458288651: GHCR pull access and Auth runtime Secret verification passed; shared `ghcr-pull` unchanged; no manifest drift, so apply skipped. TCE/Auth are intentional zero-replica maintenance (no live health asserted); active MicroFE health passed. No image promotion.
- Platform native schedule latests: reconcile #42439099803, inspection #42452273701, watchdog #42438566387, recovery #42438384072. At 08:04Z all exceed their 45/75/45/45m freshness budgets. Manual fallback runs do not count. Cron and budgets unchanged.
- TCE WF-06 native #42458256899 failed all four strict HTTP 200 probes with HTTP 503. WF-12 workflow_run #42458270339 confirmed WF-06 active and fresh at its own run time (age/queue 0m) and delivered authenticated Platform heartbeat; by 08:04Z the 25m age budget is exceeded again. Latest native WF-12 #42452308083 remains stale/failing. WF-13 #42458270097 passed recovery.
- Stock scraper scheduled run #42457182511 failed closed before dependency installation because `VNSTOCK_API_KEY` is empty. Stock master CI #42440810105 PASS 7/7. No credential change or ingestion.
- Media CI #42239703151 and Auth CI #42215394539 remain PASS. Auth PR #75/#76 exact-head CI #40446492086/#41329425940 PASS; Supabase merge-trigger effect remains a gate.
- Fresh K3s snapshot #1440: node Ready/ARM64; Media and MicroFE workloads Running 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff for `12d63b4` (no ARM64 manifest); old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. Runner services active/enabled, registration audit outstanding. No Stock/Media VolumeSnapshot references; external backup/DNS ownership unverified. Host restart required; no maintenance performed.
- App repos retain tests/builds and immutable GHCR publication ownership. Platform retains manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication, digest handoff, production apply, scaling, decommission, DNS/database/storage change, or direct SSH/Compose authority. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 16:55 ICT / 09:55 UTC

- Platform master `1f7e5cd8`; open PR #1452 fixes the decommission preflight sudo boundary. The older docs PR #1442 is superseded by this refreshed tracker and should not be merged.
- Native Platform schedules: reconcile #42467231073 failed on the pre-fix cert-manager remote Kustomize URL; inspection #42452273701 pass but stale; watchdog #42467080859 failed; recovery #42466737776 passed. Inter-arrival gaps 24,773s / 21,396s / 25,092s / 24,958s exceed 45/75/45/45m budgets. Manual/push/workflow_run runs are not native evidence.
- Cert-manager bootstrap now downloads the pinned v1.21.1 release asset through the GitHub API and checks SHA-256 before local Kustomize rendering. Validation #42468403916/#42468403911 passed; post-fix push reconcile #42468465293 passed with no drift and apply skipped.
- Fresh inspection #42468887549 generated `debug/vps-latest.md` at 09:50:50Z. Node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS Running 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff on `12d63b4` (no matching platform manifest); old Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. Only k3s-debug PVC/PV is listed; no Stock/Media VolumeSnapshot references. Decommission preflight itself stopped on a permission error before target namespace inventory; PR #1452 fixes wrapper invocation via sudo.
- TCE WF-06 #42458256899 failed four HTTP 503 probes; WF-12 #42452308083 failed freshness; WF-07 #42453060493 passed. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; Auth PR #75/#76 remain gated by Supabase integration behavior.
- App repositories continue to own tests/builds and immutable GHCR publication. Platform alone owns manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication, digest handoff or production promotion was observed.
- No production manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE market-scan schedule unchanged.


## Latest execution evidence — 2026-11-08 17:15 ICT / 10:15 UTC

- PR #1452 merged to Platform master `7ccd527e`; exact-head `validate-github-actions` #42469900529 and `validate-manifests` #42469900449 passed. Its post-merge `validate-manifests` push #42469989585 then failed on HTTP 403 from the pinned GitHub Release asset API. PR #1453 adds optional GH_TOKEN support to the helper and every workflow caller, with a regression test and a separate PR-comment job so PR-controlled code has only `contents: read`.
- Post-merge `validate-github-actions` #42469989622 passed. Reconciliation #42469998524 passed GHCR pull preflight, Auth runtime Secret verification, shared pull credential check and targeted lanes; no drift meant no production manifest apply, image promotion or rollout.
- Native schedule evidence is unchanged: reconcile #42467231073 FAIL (09:27:03Z, ~48m old), inspection #42452273701 PASS (05:49:40Z, ~265m old), watchdog #42467080859 FAIL (09:24:53Z, ~50m old), recovery #42466737776 PASS (09:20:06Z, ~55m old). Inter-arrival gaps 24,773s / 21,396s / 25,092s / 24,958s exceed the 45/75/45/45m budgets. Manual/push/workflow_run events are not native schedule evidence.
- Latest K3s snapshot #42468887549 remains the fresh push inspection at 09:50:50Z: node Ready/ARM64; Media/MicroFE Running 1/1; Stock Admin/desired Backend ImagePullBackOff on `12d63b4`; older Stock Backend/Frontend Running; TCE/Auth/Keycloak 0/0. It predates the #1452 sudo fix; a new read-only inspection must confirm the preflight now reaches target namespace inventory.
- TCE WF-06 #42458256899 failed four HTTP 503 probes; WF-12 #42452308083 failed freshness. Stock scraper #42457182511 failed closed on missing `VNSTOCK_API_KEY`; Stock CI #42440810105 PASS 7/7. Media CI #42239703151 and Auth CI #42215394539 PASS; Auth PR #75/#76 remain gated.
- App repos retain tests/builds and immutable GHCR publication ownership. Platform retains manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health. No new GHCR publication/digest handoff, manifest apply, workload scaling, decommission, DNS/database/storage change or host maintenance. TCE market-scan schedule unchanged.


## Latest execution update — 2026-11-08 17:31 ICT / 10:31 UTC

- Platform master `ab2696c2` includes merged PR #1453. Exact-head checks #42470921373/#42470921319/#42470921336 passed. Post-merge manifest validation #42471706415 and Keycloak CI #42471706467 passed; post-merge workflow lint #42471706454 remained in progress at the review cutoff.
- The cert-manager bootstrap helper now uses optional `GH_TOKEN` for the pinned GitHub Release asset API, preserves SHA-256 verification and avoids logging the token. The validation job retains `contents: read`; PR-comment write permission is isolated in a separate job without checkout.
- Read-only inspection #42471706668 was triggered by the helper/preflight path filter and remained in progress at the `Inspect VPS` step. It must complete before claiming the #1452 sudo boundary works against live K3s inventory.
- Native schedule events remain unchanged: Platform reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776; TCE WF-06 #42458256899 and WF-12 #42452308083. Ages exceed their configured freshness budgets; push/manual/workflow_run fallbacks are not native evidence. Cron and budgets unchanged.
- No new app image publication or digest handoff. Stock scraper #42457182511 fails closed on missing `VNSTOCK_API_KEY`; TCE WF-06 has four HTTP 503 probes; Media CI and Auth CI remain last recorded PASS. No production manifest apply, image promotion, workload scaling, decommission, runner retirement or host maintenance.


## Latest execution update — 2026-11-08 17:34 ICT / 10:34 UTC

- PR #1453 merged on Platform master ab2696c2 after exact-head #42470921373/#42470921319/#42470921336 passed. Post-merge #42471706415 (manifest), #42471706454 (workflow lint) and #42471706467 (Keycloak) passed. The cert-manager helper now uses optional read-only GH_TOKEN for the pinned release asset API while preserving SHA-256 verification and isolating PR-write permission.
- Read-only inspection #42471706668 completed; exact-head inspection PR #1454 passed #42471833649 and merged at 77207c26536cb005b2cbcbaf19945ded5069c0df. The sudo decommission preflight reached both retired namespaces, confirmed preserved namespaces, and found no Stock/Media PVC/PV claims or VolumeSnapshot references. This confirms storage-clean preflight only; backup/DNS and Media runner unregistration are still missing.
- Recovery-dispatched reconcile #42471718647: target all, apply mode, image changes disabled. GHCR access and Auth runtime Secret checks passed; shared pull secret unchanged; no-op ServiceAccount/deployment patches; no active Auth/MicroFE/TCE image-pull failures; TCE release pairing passed; GitOps drift false and production apply skipped. MicroFE, TCE and Auth health lanes passed, with Auth/TCE zero-replica maintenance explicitly not represented as live health. Final deployment lane gate passed; recovery-controller notification job remained queued.
- K3s snapshot 10:30:37Z: node Ready/ARM64; Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin (2 pods) and desired Backend ImagePullBackOff on 12d63b4; older Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; public OIDC 503; GitOps drift clean.
- Native schedule latests remain Platform #42467231073/#42452273701/#42467080859/#42466737776 and TCE #42458256899/#42452308083. All relevant freshness budgets remain exceeded. No cron or freshness budget changed.
- No GHCR publication/promotion, production manifest apply, workload scaling, namespace/storage deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## Direct deployment authority audit — 2026-11-08 17:38 ICT / 10:38 UTC

- TCE WF-09 (workflow_dispatch only) performs read-only VPS inspection, creates isolated TCE directories, and uploads source only to /home/ubuntu/tce/development/source.tmp. Its own output says existing Docker containers, nginx, ports and mrcute.space are not modified. Preserve as a manual setup utility; it is not a production deployment authority.
- TCE WF-10 (workflow_call/workflow_dispatch) is explicitly commented staging-only. Its Kubernetes mutations are limited to creating/labeling namespace tce-stg and creating the tce-auth staging Secret. It does not reference tce-prod or microfe-platform. Preserve as staging bootstrap; do not route production releases through it.
- TCE WF-03 is the app-owned ARM64 immutable publisher and validated repository_dispatch sender to Platform. It does not SSH to the VPS.
- Stock deploy.yml is an app-owned ARM64 image publisher. Master pushes may publish full-SHA and version/full-SHA tags; manual publication is blocked unless the explicit repository variable is enabled. It does not hand off production deployment to Platform from this workflow.
- Media WF-03 is an app-owned ARM64 immutable publisher; Media is retired from active Platform GitOps and no Platform handoff is sent. No SSH/Compose authority is added.
- Authentication release.yml is workflow_dispatch-only and app-owned; Platform remains the sole production manifest/Secret/reconcile/rollout authority.
- No workflow was removed. Useful manual staging, release and scheduled jobs are preserved. No direct SSH/Compose production deployment authority was added; TCE market-scan schedule unchanged.


## Scheduled image cleanup safety contract — 2026-11-08 17:40 ICT / 10:40 UTC

- vps-image-cleanup.yml runs weekly Sunday 03:30 UTC. Scheduled and push-triggered runs are forced to DRY_RUN=true; only explicit workflow_dispatch can set dry_run=false.
- Latest native run #42472343489 completed PASS at 10:39:26Z, about 7h09 after the cron time. KEEP_UNUSED_IMAGES=10; script found 8 unused images and remove_count=0. No images were removed.
- The script inventories all Pods and CRI containers, protects images referenced by existing containers (including terminated ones), excludes pinned images, fails closed if a non-terminal Pod reference cannot be resolved, and rechecks Pod/container references before each deletion. The destructive manual path was not invoked.
- This workflow is purposeful maintenance, not a production deployment authority; preserve it and keep it separate from native deployment cadence acceptance.



## Media runner decommission verification contract — PR #1458 (open)

- App ownership is unchanged: Media Generation owns source/tests/builds and immutable image publication; Platform owns only the protected K3s decommission workflow after GitOps ownership retirement.
- The delete-mode workflow now runs both local checks (systemd inactive and disabled/masked/absent; no `Runner.Listener`) and a remote read-only GitHub repository runner-list check for exact runner name `media-generation-k3s-01`.
- Required Platform Actions secret: `MEDIA_RUNNER_AUDIT_TOKEN`. It must be a fine-grained token or GitHub App installation token with repository **Administration: read** on `phanthienquoc/media-generation` only. The verifier calls only `GET /repos/phanthienquoc/media-generation/actions/runners`, paginates, suppresses the token, and fails closed on missing credentials, API/JSON failure or a matching runner. It does not have or request runner deletion permission.
- Operator still performs the stop/disable and GitHub unregister flow separately. The workflow verifies the result; it never stops or unregisters the runner.
- Plan mode remains read-only and token-free. Delete mode retains production Environment approval, typed namespace/backup/DNS attestations, fresh same-run storage preflight and fixed namespace allowlist.
- PR #1458 adds regression coverage for absent/present runner, pagination, missing token and API failure. It is open pending exact-head validation; no decommission was dispatched.
- This contract does not change app publisher ownership, GHCR credentials, GitOps promotion, production apply authority, direct SSH/Compose boundaries or the TCE market-scan schedule.



## Runner audit guard — merged Platform PR #1458

- `decommission-stock-media.yml` delete mode now verifies the Media runner both locally and remotely. Local checks require the exact service to be inactive and disabled/masked/absent and no `Runner.Listener` process.
- Remote check: `GET /repos/phanthienquoc/media-generation/actions/runners`, paginated, exact runner name `media-generation-k3s-01`. It is read-only and fails closed on missing credentials, HTTP/API failure, malformed JSON or a matching runner.
- Required Platform Actions secret: `MEDIA_RUNNER_AUDIT_TOKEN`, fine-grained token/App installation token with **Administration: read** on `phanthienquoc/media-generation` only. No runner deletion permission. Secret existence is not verified by this audit.
- Operator must separately stop/disable and unregister the Media runner. The workflow does not do those actions. Plan mode remains read-only and token-free.
- PR #1458 merged at `098cf54de9e2223bc97db57cca6fbee8334fc80c`; exact-head and post-merge workflow validations passed. No decommission was dispatched.

## Latest Platform runtime evidence — 2026-11-08 18:20 ICT

- Reconcile fallback #42474936543: GHCR preflight PASS; shared `ghcr-pull` unchanged in both active GHCR namespaces; Auth runtime Secret provisioned/verified; no GitOps drift; manifest apply/image promotion skipped. Auth/MicroFE/TCE lanes passed with rollouts skipped; TCE remains zero-replica maintenance, so no live health was asserted.
- Read-only inspection #42475079478 / PR #1459: K3s node Ready ARM64; Media and MicroFE active pods 1/1; Stock Admin/new Backend ImagePullBackOff due missing ARM64 manifest for `12d63b4`; TCE/Auth/Keycloak 0/0; OIDC 503; dedicated Media runner still active/enabled; no Stock/Media PVC/PV/VolumeSnapshot references.
- PR #1459 merged at `ef7a1a15b94acdaf7c46cbecb4aa2391cb90b0f8` after exact-head manifest validation #42475211696 passed. Only `debug/vps-latest.md` changed.


## Latest review — 2026-11-08 18:55 ICT / 11:55 UTC

- Platform master is `a0c1e3ee6cf0cb3d9f168227e6fdfd1a6e5ebdfd`; latest post-merge `validate-manifests` #42475493117 passed. Open Platform PRs #1314/#544/#541/#539 remain draft planning/docs. TCE/Stock/Media have no open PRs; Authentication has #75 ready and #76 draft.
- Native Platform schedule runs remain reconcile #42467231073 (FAIL, pre-cert-manager fix), inspection #42452273701 (PASS but stale), watchdog #42467080859 (FAIL), recovery #42466737776 (PASS but stale). At 11:55Z ages are approximately 148m/365m/150m/155m against 45/75/45/45m budgets. Latest post-fix push validation is not native schedule evidence. Cron and budgets are unchanged.
- Native TCE WF-06 #42458256899 returned four HTTP 503s; WF-12 #42452308083 failed freshness; WF-07 integration #42453060493 passed. No TCE market-scan schedule changes.
- Stock scraper #42457182511 ran on schedule but failed closed due missing `VNSTOCK_API_KEY`; no ingestion. Stock CI #42440810105 is 7/7 PASS but does not publish images.
- Media runner remains active; #1458's remote registration gate is merged, but token configuration and external backup/DNS evidence are not verified. No decommission.
- Auth master CI and both PR validation runs pass; Supabase Preview is skipped. PR #75 has no migration files in its diff, but the integration's production target/merge behavior is still not authoritatively established.
- Reconciliation #42474936543 and recovery #42475042844 passed with no drift, no manifest apply and no image promotion. Read-only inspection #42475079478 passed; its snapshot is ~38m old, within the age budget but not evidence of native inspection cadence.
- No new immutable GHCR publication, digest handoff or production promotion was observed. Keep app-owned publishers and Platform-only production authority boundaries unchanged.


## Latest review — 2026-11-08 19:05 ICT / 12:05 UTC

- Platform master `25c5e390161c5410517f5360885281abd4c1ff49`; PR #1461 merged after exact-head validation #42478273907 PASS and post-merge #42478553173 PASS.
- Authentication PR #75 merged at `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` after updated exact-head validation #42478511082 passed. Auth master push CI #42478653766 is still running. PR #76 remains draft.
- Read-only Supabase recheck: project ACTIVE_HEALTHY, branch status FUNCTIONS_DEPLOYED; repository migration files and remote ledger match 84/84. No migration count change was observed after merge. The external integration run log is not available through the read-only API; do not claim it was independently inspected. No Auth release workflow was dispatched.
- Native Platform schedule events remain reconcile #42467231073, inspection #42452273701, watchdog #42467080859, recovery #42466737776; all exceed 45/75/45/45m freshness budgets. Native TCE WF-06 #42458256899 returned 4×503; WF-12 #42452308083 failed freshness; WF-07 #42453060493 passed. No cron/budget changes.
- Stock scraper #42457182511 ran but failed closed because VNSTOCK_API_KEY was empty; dependency installation, entitlement verification and ingestion were skipped. Stock CI #42440810105 is 7/7 PASS but non-publishing.
- K3s inspection #42475079478 is ~47m old and within its snapshot age budget; workload state remains Media/MicroFE 1/1, Stock Admin/desired Backend ImagePullBackOff, TCE/Auth/Keycloak 0/0. No decommission or rollout change.
- Reconciliation #42474936543 and recovery #42475042844 passed with no drift, no manifest apply and no image promotion. No new app publisher or digest handoff.
- Media runner remains active; decommission waits for audit token, external backup/retention and DNS ownership. Keep app-owned publishing and Platform-only production apply boundaries.


## Latest cross-repo execution — 2026-11-08 20:01 ICT / 13:01 UTC

### Current repository and workflow state

| Repository | Master SHA | Open PRs | Latest relevant evidence |
|---|---|---|---|
| Platform Infra | No application image builds. Receives provenance-bound TCE/Auth/MicroFE digest events; owns native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `891a07c0`; PR #1493 merged after exact-head and post-merge validation PASS. Ready-event reconciliation now attests the exact promotion run's app-specific successful jobs, complete Actions job list, current digest-pinned manifest and tag-to-digest/linux/arm64 evidence before any Secret/pull-credential mutation. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | None | WF-12 #42479336350 schedule/FAIL; WF-13 #42479348862 PASS; fallback WF-06 #42479362379 FAIL 4×503 |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | None | scraper #42457182511 fail-closed on missing `VNSTOCK_API_KEY`; CI #42440810105 PASS/non-publishing |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | None | CI #42239703151 PASS; no new publisher run |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | #76 draft | master CI #42478653766 PASS |

### Schedule, heartbeat and service health
- Platform native schedule latest evidence: reconcile #42467231073 FAIL (09:27:03Z); inspection #42452273701 PASS (05:49:40Z); watchdog #42467080859 FAIL (09:24:53Z); recovery #42466737776 PASS (09:20:06Z). All are stale against 45/75/45/45-minute budgets. No newer native schedule event appeared in the paged Actions history.- TCE WF-12 #42479336350 ran on native schedule and correctly detected stale WF-06. Its authenticated Platform heartbeat dispatch was accepted. WF-13 #42479348862 then dispatched one deduplicated read-only WF-06 fallback, correlated to exact master SHA. Fallback #42479362379 returned 503 for TCE web, TCE API, Auth liveness and Auth readiness.
- Platform receiver #42479344664 could not complete the source-run API lookup: repeated HTTP 500 from the public GitHub Actions run endpoint. It failed closed before source reconciliation/freshness recovery. Rerun attempt 2 was skipped by the first-attempt-only guard.
- A bounded retry change is proposed in branch `fix/retry-transient-tce-heartbeat-api-500-20261108-2001-ict`: four retries, 45-second retry window, 15-second request timeout and connection-refused retry; permanent 4xx remain fail-closed. No payload identity, permissions, cron, freshness budget or production authority change.
- Stock scheduled scraper ran and failed closed before ingestion because `VNSTOCK_API_KEY` is missing. No new immutable GHCR publisher/digest evidence exists for Stock, TCE, Media or Auth in this review.

### Runtime/deployment boundary

- Latest K3s snapshot #42475079478 is older than the 75-minute snapshot-age budget at this checkpoint; no current health claim should be derived from it. Last recorded workloads: Media backend/frontend and MicroFE Shell/WS/NATS 1/1; Stock Admin and desired Backend ImagePullBackOff on `12d63b4` due missing ARM64 manifest; TCE/Auth/Keycloak intentional 0/0.
- Reconciliation #42474936543 passed GHCR access and Auth runtime Secret checks, left shared `ghcr-pull` unchanged, found no GitOps drift and skipped apply/promotion/rollout.
- `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. TCE/Stock/Media/Auth app repositories own tests/builds and immutable image publication; Platform owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health verification.
- Preserve useful CI/security/test workflows and purposeful manual/release/scheduled jobs. No workflow was removed. No production mutation, scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.

- Follow-up: Platform PR [#1463](https://github.com/phanthienquoc/platform-infra/pull/1463) is open for the bounded TCE Actions API retry and tracker refresh. Initial head `b7550187f317fb36999757038ad1fa631a07a908`; exact-head validation runs #42483619147 (`validate-github-actions`) and #42483619148 (`validate-manifests`) started in progress. No merge until both pass on the latest head.

## Post-merge follow-up — 2026-11-08 20:14 ICT / 13:14 UTC

- Platform PR [#1463](https://github.com/phanthienquoc/platform-infra/pull/1463) merged by squash at `c70fc63d52d1e1dfd789e8fe7adc15a47cb9615a`; exact head was `33e61ebbbdcaf3523b008457eef71da490626d1a`.
- Exact-head `validate-github-actions` #42483745382 PASS and `validate-manifests` #42483745326 PASS. Post-merge master `validate-github-actions` #42483862284 PASS and `validate-manifests` #42483862226 PASS.
- The merged recovery receiver now retries transient GitHub Actions API 5xx/connection-refused failures with a bounded retry window, while retaining `curl --fail` and no `--retry-all-errors`; permanent 4xx/authentication failures remain fail-closed.
- A new Platform `inspect-vps.yml` native schedule run #42483869620 was created on the merge SHA and was still `in_progress` at this checkpoint. The prior native inspection #42452273701 was 05:49:40Z; the inter-arrival gap to #42483869620 is approximately 7h23m, still outside the 75-minute cadence budget. Do not claim a completed K3s snapshot until #42483869620 completes and its artifact/snapshot is validated.
- No newer native Platform reconcile/watchdog/recovery run was observed: #42467231073 FAIL, #42467080859 FAIL, #42466737776 PASS but stale. Schedule delivery remains unresolved despite the new inspection run.
- TCE WF-12 #42479336350 successfully delivered its heartbeat; Platform receiver #42479344664 failed on repeated GitHub API HTTP 500. The requested rerun was skipped at attempt 2 by the existing first-attempt-only guard. TCE WF-13 #42479348862 dispatched read-only WF-06 fallback #42479362379; all four endpoints returned HTTP 503.
- Static publisher/receiver review: TCE WF-03 and Auth release are manual app-owned ARM64 publishers with full-SHA-bound tags and digest verification before digest-bound Platform events; Stock deploy verifies full-SHA and version+SHA tags for Scraper/Admin/Backend but has no active Platform handoff while retired; Media WF-03 verifies ARM64 release digest and intentionally sends no Platform handoff while retired. Platform receiver verifies TCE/Auth source run identity, tag-to-digest mapping and ARM64 before GitOps promotion. No new publisher run or actual GHCR digest handoff was observed.
- Stock scraper #42457182511 remains fail-closed due missing `VNSTOCK_API_KEY`; Auth master CI #42478653766 PASS and PR #76 remains draft. Media CI #42239703151 PASS.
- No production manifest apply, image promotion, workload scaling, decommission, DNS/database/storage mutation, runner retirement or host maintenance occurred. TCE market-scan schedule unchanged.

## Completed K3s inspection follow-up — 2026-11-08 20:15 ICT / 13:15 UTC

- Native Platform inspection [#42483869620](https://github.com/phanthienquoc/platform-infra/actions/runs/42483869620) completed SUCCESS. It generated `debug/vps-latest.md` at 13:12:54Z and created inspection PR [#1464](https://github.com/phanthienquoc/platform-infra/pull/1464), which was validated and squash-merged at `ba01c42299490eff839c41326c894e0d59650ab6`.
- Snapshot is now fresh, but native inspection cadence is still not accepted: prior native inspection #42452273701 was 05:49:40Z; inter-arrival gap was 26,586s (~7h23m), exceeding the 4,500s/75m budget.
- K3s node `tce-k3s-01` remains Ready, ARM64, K3s `v1.36.3+k3s1`; container runtime `containerd://2.3.2-k3s2`. Disk 56% (21 GiB available), RAM 19 GiB available. Docker 29.1.3 reports 20 images/9.195 GB with 5.773 GB reclaimable; 12 containers active; no cleanup performed.
- Media backend/frontend and MicroFE Shell/WS/NATS are Running 1/1. Stock Admin (two pods) and desired Backend remain ImagePullBackOff on `12d63b4`; legacy Stock Backend and Frontend remain Running 1/1. TCE/Auth/Keycloak remain zero-replica; Keycloak readiness timed out and both public OIDC probes returned HTTP 503.
- Media runner service and Listener remain active/enabled; Platform runner is also active. In-cluster Stock/Media storage preflight remains clean (no PVC/PV claims or VolumeSnapshot references), but external backup/retention and authoritative DNS are still unverified.
- GitOps drift is clean; cert-manager v1.21.1 bootstrap manifest checksum was verified. Host reports `restart_required=yes`; containerd/Docker/OS updates are available. No upgrade/reboot authorized.
- No production manifest apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred.


## Cross-repo operational evidence — 2026-11-08 21:07 ICT / 14:07 UTC

No workflow ownership or deployment authority changed in this review. The current run evidence confirms:
- TCE WF-07 native schedule #42484929411 successfully dispatched an authenticated heartbeat; Platform recovery #42484949353 verified its exact source workflow/run/attempt/SHA and accepted the repository_dispatch payload.
- Platform native schedule cadence remains outside the existing budgets; a recent manual reconciliation and a recent native inspection are fallback/runtime evidence only, not cadence acceptance.
- TCE WF-06/WF-12 native runs remain stale; the latest fallback healthcheck returned HTTP 503 for all four public endpoints.
- Stock publisher source contract statically builds all three components on native ARM64 and verifies full-SHA/version+SHA tag digest equality; no new publisher run/digest evidence was observed. Stock scraper remains fail-closed on missing `VNSTOCK_API_KEY`.
- Media and Auth have no new publisher/deployment runs. Media runner remains active; its remote-registration audit token and external backup/DNS prerequisites remain unverified. Auth PR #76 remains draft.

Preserve the existing separation: app repos own tests/builds/immutable GHCR publication; Platform Infra alone owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health verification. Preserve useful CI/security/manual/release/scheduled jobs. No direct SSH/Compose production authority was added, no workflow was removed, and the TCE market-scan schedule is unchanged.
## Latest cross-repo execution — 2026-11-08 21:57 ICT / 14:57 UTC

- Platform master `ab458a525f18c1397fa52ca639e5a2abd6c9a536`; current open PRs #1314/#544/#541/#539 remain planning/docs. TCE/Stock/Media have no open PRs; Auth #76 remains draft.
- Inspection PR #1467 is represented on Platform master by snapshot commit `ab458a525f18c1397fa52ca639e5a2abd6c9a536`, generated 14:28:32Z. Snapshot age is ~29m. The event type and exact Actions check metadata are not exposed by the current connector lookup; do not classify it as native schedule evidence.
- New inspection contract on branch `docs/deployment-readiness-2026-11-08-2157-ict`: `scripts/inspect-vps.sh` now emits `### GHCR image digest coverage` and warns for cached GHCR tags with no RepoDigest; local image IDs are explicitly not registry digest/promotion evidence. `inspect-vps.yml` validates the section, and `validate-workflow-contracts.py` enforces the contract. PR validation pending.
- K3s node `tce-k3s-01` Ready/ARM64, K3s v1.36.3+k3s1; disk 56% (~21 GiB free), RAM ~19 GiB available. Docker 29.1.3: 20 images/9.195 GB, ~5.773 GB reclaimable. Host restart_required=yes; no cleanup/upgrade/reboot.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1. Stock Admin×2 and desired Backend ImagePullBackOff on `12d63b4`; old Backend/Frontend 1/1 on `23b2878`. CRI RepoDigest blank for cached Stock backend/user tags. TCE/Auth/Keycloak 0/0; public OIDC 503. Media runner active/enabled/listener present.
- Stock scraper #42457182511 fail-closed on missing `VNSTOCK_API_KEY`; no new publisher or registry digest proof. Media #42239703151 and Auth #42478653766 are latest recorded CI passes; no new Media/Auth publisher run.
- TCE WF-07 native #42484929411 PASS; WF-12 heartbeat #42484941935 and Platform recovery #42484949353 PASS. Native WF-06 remains #42458256899 4×503; WF-12 #42479336350 stale. Platform native reconcile/watchdog/recovery remain outside freshness budgets; inspection #1467 event provenance unknown.
- No production mutation, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. No workflow removed; no direct SSH/Compose production authority added; TCE market-scan schedule unchanged.
## Latest inspection and merge evidence — 2026-11-08 22:14 ICT / 15:14 UTC

- Platform master `819215cc0c6b295f746e1a43cd6747df4fe292b8` includes automated inspection PR #1469, snapshot generated `2026-11-08T15:10:12Z`. Event type/run ID not surfaced; do not count as native schedule evidence.
- PR #1468 merged at `45fae050df626641ddfca3ededcff3cbf9f388b3`. Exact-head `validate-github-actions` #42493255493 PASS and `validate-manifests` #42493255334 PASS. PR #1470 was closed unmerged as superseded by the new inspection commit.
- Live inspection output now contains `### GHCR image digest coverage`, `status: warning`, and two cache-only entries: `ghcr.io/phanthienquoc/stockdividend/backend:23b2878` and `ghcr.io/phanthienquoc/stockdividend/user:23b2878`. Both have blank RepoDigest; local image IDs are not registry digests or promotion proof.
- Stock Admin×2 and desired Backend remain ImagePullBackOff on `12d63b4` (no matching ARM64 manifest); legacy Backend/Frontend remain 1/1 on `23b2878`. No Stock publisher run/digest handoff is verified; `VNSTOCK_API_KEY` remains missing in last recorded scraper run #42457182511.
- Media backend/frontend and MicroFE Shell/WS/NATS 1/1. TCE/Auth/Keycloak 0/0; public OIDC 503. Media runner service/listener active. External backup, retention and authoritative DNS ownership remain unverified.
- No production apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. No workflow removed or direct SSH/Compose authority added; TCE market-scan schedule unchanged.

## Cross-repo execution evidence — 2026-11-08 22:55 ICT / 15:55 UTC

- Platform #1471 merged; exact-head `validate-manifests` #42493913586 PASS and post-merge master `validate-manifests` #42493968964 PASS. Current Platform master is `e9f079603dcdfe5ecf9c23296009bb4d3a17f9a1`. Open Platform planning PRs #1314/#544/#541/#539 remain draft.
- TCE #42489680372 is the latest native WF-06 schedule run and failed all four public HTTP probes with 503. WF-12 #42489702686 was a workflow_run, validated the scheduled source identity and delivered a heartbeat; Platform receiver #42489711753 succeeded after the bounded API retry fix. WF-13 #42489702690 dispatched fallback #42489720607, which also failed four 503 probes.
- Platform recovery #42489711753 dispatched reconciliation #42489725488 because the latest reconcile activity exceeded the 20-minute recovery budget. The exact payload used current master at dispatch time, `mode=apply`, `target_app=all`, `allow_image_changes=false`. Reconciliation passed GHCR preflight, Auth runtime Secret verification, shared pull-secret checks and TCE release pairing; cert-manager manifest bootstrap and Kubernetes diff passed with no drift. No manifest apply, image promotion or rollout occurred. TCE/Auth were recognized as zero-replica maintenance; no live health was asserted for those scopes.
- Native Platform schedule evidence remains reconcile #42467231073 FAIL, inspection #42483869620 PASS but stale, watchdog #42467080859 FAIL, recovery #42466737776 PASS but stale. A newer push-triggered inspection snapshot is not native schedule evidence. Do not change cron or budgets.
- Latest snapshot (15:10:12Z): node Ready/ARM64; Media and MicroFE 1/1; Stock Admin×2 and desired Backend ImagePullBackOff on 12d63b4; Stock cached backend/user 23b2878 lack RepoDigest; TCE/Auth/Keycloak 0/0; public OIDC 503; Media runner active/enabled. Storage preflight is clean in-cluster, but external backup/DNS evidence is missing.
- App ownership remains unchanged: TCE/Stock/Media/Auth own tests/builds and immutable GHCR publication; Platform alone owns production manifests, shared pull credentials, GitOps promotion/reconciliation, rollout and health verification. No new publisher/digest handoff, no workflow deletion and no direct SSH/Compose production authority.


## Latest observed execution — 2026-11-08 23:56 ICT / 16:56 UTC

| Repository | Current master | Latest relevant run evidence | Open PRs |
|---|---|---|---|
| Platform Infra | No application image builds. Receives provenance-bound TCE/Auth/MicroFE digest events; owns native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `891a07c0`; PR #1493 merged after exact-head and post-merge validation PASS. Ready-event reconciliation now attests the exact promotion run's app-specific successful jobs, complete Actions job list, current digest-pinned manifest and tag-to-digest/linux/arm64 evidence before any Secret/pull-credential mutation. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | WF-06 native #42489680372 FAIL (four public probes; TCE web log confirms 503); WF-12 latest native #42479336350 FAIL; WF-07 native #42484929411 PASS; no recent publisher run | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | Scraper #42457182511 FAIL closed on missing `VNSTOCK_API_KEY`; CI #42440810105 PASS; publisher #41563856933 (Nov 3) PASS with three verified ARM64 digests but is stale vs current master | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | CI #42239703151 PASS; latest publisher #41158598649 (Oct 31) PASS, no newer publication | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | CI #42478653766 PASS; latest manual release #41040510320 (Oct 30) PASS, no newer publication | #76 draft |

### Runtime/deployment ownership

- Reconcile #42499043683 verified GHCR read access, provisioned/verified Auth runtime Secret, left shared `ghcr-pull` unchanged, found no GitOps drift and skipped apply/image promotion/rollout.
- K3s snapshot from manual inspection #42498449089 (generated 16:09:45Z) is within the 75-minute snapshot-age budget at this checkpoint, but is not native inspection cadence evidence. Media/MicroFE active pods are 1/1; Stock Admin×2 and desired Backend are ImagePullBackOff/ErrImagePull on `12d63b4`; old Stock Backend/Frontend 1/1; TCE/Auth/Keycloak 0/0; OIDC 503.
- Stock's last publisher #41563856933 (source `50ba0dfb67eb3dfaa376db0c752bbef5b0817bec`) verified ARM64 full-SHA/version+SHA tag digests for Scraper/Admin/Backend. It is not current-master publication evidence; the live desired `12d63b4` tags remain invalid for ARM64. Missing `VNSTOCK_API_KEY` blocks scraper ingestion, not the image build itself.
- Media runner remains active/enabled/listener-present; remote audit token, external backup/retention and authoritative DNS ownership remain unverified. Decommission workflow remains manual-only and fail-closed.
- Native Platform schedule history shows reconcile/recovery have each resumed once after multi-hour gaps; watchdog still correctly fails the historic inter-arrival budget, and native inspection remains stale. Require another within-budget native interval before declaring cadence recovered. TCE WF-06/WF-12 native runs remain stale.
- No production manifest apply, image promotion, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. No workflow removed; no direct SSH/Compose authority added; TCE market-scan schedule unchanged.


## Latest cross-repo execution evidence — 2026-11-09 01:03 ICT / 18:03 UTC

### Current repository heads and open PRs

- Platform Infra master: b0f791422dc9fb5056a77b7dfbfb01deba36d6f2; inspection PR #1475 merged after exact-head validate-manifests #42507931004 passed. Open draft PRs #1314, #544, #541, #539 remain untouched.
- TCE Dashboard master: 7ab52078c4250829e158f05b2695ceb9d11bdbe3; no open PR.
- StockDividend master: e6469ac6617142b349144101a1192cb6aa7104ad; no open PR.
- Media Generation master: 54f3a76a5f8861842fd1bae698c4cb0fa8c9034d; no open PR.
- Authentication master: cb907a63df0e0441b54b7b930ecdbfa97a5e52e1; PR #76 remains draft.

### Latest event evidence by owner

| Owner | Latest relevant evidence | Result |
|---|---|---|
| Platform native reconcile | #42499043683 schedule | PASS; no drift |
| Platform native inspection | #42483869620 schedule | PASS but stale; manual #42507763937 produced fresh snapshot |
| Platform schedule watchdog | #42498640135 schedule | FAIL; historic inter-arrival gaps exceed budgets |
| Platform recovery | #42498266478 schedule | PASS; stale at current checkpoint |
| Platform manual reconcile | #42507600702 workflow_dispatch | PASS; GHCR/Auth Secret preflight, no drift, no apply/promotion/rollout |
| TCE WF-06 | #42489680372 schedule; fallback #42507608317 workflow_dispatch | Both FAIL; four public endpoints return HTTP 503 |
| TCE WF-12 | #42507582654 schedule | FAIL on WF-06 age 213m; heartbeat dispatch succeeded |
| TCE WF-13 | #42507595891 workflow_run | PASS; dispatched read-only WF-06 fallback |
| Stock scraper | #42457182511 schedule | FAIL closed; missing VNSTOCK_API_KEY |
| Stock CI | #42440810105 push | PASS |
| Media CI | #42239703151 push | PASS |
| Auth CI | #42478653766 push | PASS |

Platform receiver #42507589119 accepted and validated the TCE WF-12 heartbeat. It dispatched the existing reconciliation workflow with master ref, mode=apply, target_app=all and allow_image_changes=false. Reconciliation #42507600702 found no drift and skipped apply, promotion and rollout. This is runtime evidence for the heartbeat/recovery handoff, not evidence of native schedule cadence recovery.

### Publisher and image evidence

- Stock #41563856933 (2026-11-03) verified three ARM64 component digests for source 50ba0dfb67eb3dfaa376db0c752bbef5b0817bec; stale versus current master. Current 12d63b4 Admin/Backend tags fail ARM64 pulls; cached 23b2878 backend/user have blank RepoDigest.
- Media #41158598649 (2026-10-31) published ARM64 images; prior Platform promotion #41158826992 failed GitOps master convergence. Current Media pods run pinned digests.
- Auth #41040510320 (2026-10-30) published ARM64 image with digest; no new release handoff.
- TCE: no new publisher run or digest handoff.

### Runtime and ownership

Latest read-only K3s snapshot is debug/vps-latest.md, generated 2026-11-08 18:00:37Z. Node Ready/ARM64; disk 56%, ~21 GiB free; available RAM ~19 GiB; restart_required=yes. Media/MicroFE active pods 1/1. Stock Admin×2 and new Backend are ImagePullBackOff on 12d63b4; legacy Backend and frontend/user 23b2878 remain 1/1. TCE/Auth/Keycloak are 0/0; public TCE/OIDC probes return 503. Media runner service/listener remain active. External backup/retention/DNS and MEDIA_RUNNER_AUDIT_TOKEN remain unverified.

### Preservation rules

- Keep app publication in app repos and production promotion/reconciliation in Platform Infra.
- Keep reconcile-vps.yml as the only production apply authority and inspect-vps.yml read-only.
- No image promotion, manifest apply, scaling, decommission, DNS/database/storage mutation, runner retirement or host maintenance in this execution.
- No workflow deletion or direct SSH/Compose authority added.
- TCE market-scan schedule unchanged.


## Latest cross-repo execution — 2026-11-09 02:00 ICT / 19:00 UTC

| Repository | Current master | Latest relevant evidence | Open PRs |
|---|---|---|---|
| Platform Infra | No application image builds. Receives provenance-bound TCE/Auth/MicroFE digest events; owns native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `891a07c0`; PR #1493 merged after exact-head and post-merge validation PASS. Ready-event reconciliation now attests the exact promotion run's app-specific successful jobs, complete Actions job list, current digest-pinned manifest and tag-to-digest/linux/arm64 evidence before any Secret/pull-credential mutation. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | WF-06 native #42512468931 FAIL (four HTTP 503 probes); WF-12 native #42507582654 FAIL (stale WF-06); later workflow_run heartbeat path reached Platform | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | CI #42440810105 PASS; scraper #42457182511 FAIL closed on missing `VNSTOCK_API_KEY`; no current-master publisher evidence | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | CI #42239703151 PASS; no new publisher run; live images remain digest-pinned | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | CI #42478653766 PASS; no new release/promotion evidence | #76 draft |

### Schedule acceptance

- Platform native reconcile gap: 24,564s vs 2,700s budget.
- Platform native inspection gap: 18,901s vs 4,500s budget.
- Platform native recovery gap: 24,440s vs 2,700s budget.
- Platform native watchdog gap: 24,414s vs 2,700s budget; latest watchdog remains failed.
- TCE WF-06 gap: 16,293s; WF-12 gap: 20,594s; both exceed the observed 900s cadence. Do not change cron or freshness budgets. Manual, workflow_run and repository_dispatch events do not satisfy native schedule acceptance.

### Reconciliation / runtime

- Reconciliation #42512502763 ran with master, `mode=apply`, `target_app=all`, `allow_image_changes=false`; GHCR access and Auth runtime Secret checks passed, shared `ghcr-pull` unchanged, drift=false, apply/promotion/rollout skipped. TCE/Auth zero-replica maintenance was explicitly recognized; MicroFE active health passed; Keycloak skipped.
- Snapshot #42510125328 generated 18:27:55Z: node Ready/ARM64, disk 56%, ~21 GiB free, RAM ~19 GiB; restart_required=yes. Media and MicroFE workloads 1/1. Stock Admin×2 and desired Backend ImagePullBackOff on `12d63b4`; legacy Backend/Frontend 1/1. TCE/Auth/Keycloak 0/0.
- The inspection's read-only Stock/Media decommission plan reports storage-clean (no target PVC/PV/VolumeSnapshot references), but the Media runner is active/enabled/listener-present and DNS/external backup ownership are unverified. Namespaces and workloads remain present. Do not run delete mode until the remote runner audit, runner retirement, backup/retention and authoritative DNS gates are independently satisfied.

### Preservation

App repositories retain tests/builds and immutable GHCR publication. Platform Infra remains the sole owner of production manifests, shared GHCR pull credentials, digest/source verification, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose deployment authority, workflow deletion, image promotion, manifest apply, workload scaling, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.


## Latest contract changes — 2026-11-09 03:16 ICT

- `reconcile-schedule-watchdog.yml` now verifies the completed conclusion of the latest scheduled reconciliation in addition to age and queue freshness. `scripts/verify-scheduled-run-result.py` fails closed on failed/cancelled/timed-out/unknown completed results; queued/in-progress results are explicitly pending. Push-triggered read-only smoke remains warning-only.
- `validate-github-actions.yml` runs the helper's eight regression cases; `validate-workflow-contracts.py` asserts that the helper is invoked with the exact run ID, event and URL and that unknown statuses fail closed.
- `recover-stale-ops.yml` explicitly excludes `scripts/verify-scheduled-run-result.py` from the broad `scripts/**` push trigger. The workflow contract validator enforces this exclusion so read-only watchdog code cannot bootstrap production reconciliation.
- PR #1479 implemented the result gate and merged at `01a3b4ba4ebcf481bd532bbc367533da9f2791a3`; exact-head and post-merge GitHub Actions/manifest validations passed.
- PR #1480 implemented the recovery-path exclusion and merged at `9bb69b446d6aa161aae13c7efe4648af92691641`; exact-head and post-merge GitHub Actions/manifest validations passed.
- PR #1481 merged the fresh read-only K3s inspection snapshot at `5197840226b49d790cb99c4caeb8377526e6fed8`; exact inspection validation #42519280294 passed.
- The #1479 push initially matched the recovery `scripts/**` path and caused a recovery-dispatched reconciliation. That run found `drift=false`, kept `ghcr-pull` unchanged, skipped manifest apply/promotion/rollout, and did not scale TCE/Auth. PR #1480 closes this routing gap for future read-only helper changes.
- Native schedule gaps remain outside the existing budgets; manual inspections and workflow_run/repository_dispatch recoveries are not counted as native schedule evidence. Cron, freshness budgets and TCE market-scan schedule remain unchanged.


## Latest observed workflow ownership and run state — 2026-11-09 03:56 ICT

| Repository | Master SHA | Latest relevant workflow evidence | Open PRs |
|---|---|---|---|
| Platform Infra | No application image builds. Receives provenance-bound TCE/Auth/MicroFE digest events; owns native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `891a07c0`; PR #1493 merged after exact-head and post-merge validation PASS. Ready-event reconciliation now attests the exact promotion run's app-specific successful jobs, complete Actions job list, current digest-pinned manifest and tag-to-digest/linux/arm64 evidence before any Secret/pull-credential mutation. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | WF-06 schedule #42512468931 FAIL; manual fallback #42512497073 confirms four HTTP 503 endpoints; WF-12 #42507582654 FAIL stale | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | CI #42440810105 PASS; scraper #42457182511 fail-closed on missing `VNSTOCK_API_KEY`; deploy.yml has ARM64 immutable publisher and manual gate `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED` | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | CI #42239703151 PASS; no new current-master publisher run | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | CI #42478653766 PASS; no new release/promotion evidence | #76 draft |

Platform native cadence gaps from watchdog #42521222353: reconcile 15,672s/2,700s; inspection 18,901s/4,500s; recovery 15,605s/2,700s; watchdog 15,517s/2,700s. TCE WF-06/WF-12 gaps: 16,293s and 20,594s against 1,500s. Recovery delivery/result verification passed. Manual/workflow_run events are not native schedule acceptance.

Stock publication boundary: master pushes can publish immutable ARM64 artifacts without a Platform handoff when the manual-release variable is false; manual dispatch is blocked unless `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED=true`. `VNSTOCK_API_KEY` is a scraper-ingestion prerequisite, not the image publisher credential. No secret/variable was modified and no manual publication was attempted.

Latest committed K3s snapshot is PR #1484, generated 21:59:12Z; it is a successful manual recovery inspection and therefore not native cadence evidence. Stock desired ARM64 images remain failing; Media runner remains active/listener-present; external backup/DNS and runner audit prerequisites remain unverified. TCE/Auth/Keycloak remain 0/0 maintenance. No production mutation or workflow deletion occurred. App repos own tests/builds/immutable GHCR publication; Platform Infra alone owns production manifests, shared pull credentials, digest/source verification, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No SSH/Compose authority added; TCE market-scan schedule unchanged.


## Latest observed workflow ownership and run state — 2026-11-09 04:56 ICT

| Repository | Master SHA | Current workflow evidence | Open PRs |
|---|---|---|---|
| Platform Infra | No application image builds. Receives provenance-bound TCE/Auth/MicroFE digest events; owns native inspection, reconciliation, watchdog, recovery and image-cleanup dry-run. | Sole production manifests, shared GHCR pull credentials, runtime Secrets, source/digest/provenance validation, GitOps promotion/reconciliation, rollout/health and protected Stock/Media decommission. | Master `891a07c0`; PR #1493 merged after exact-head and post-merge validation PASS. Ready-event reconciliation now attests the exact promotion run's app-specific successful jobs, complete Actions job list, current digest-pinned manifest and tag-to-digest/linux/arm64 evidence before any Secret/pull-credential mutation. |
| TCE Dashboard | `7ab52078c4250829e158f05b2695ceb9d11bdbe3` | Native WF-12 #42527713763 FAIL: WF-06 #42512468931 was 180m old, queue 0m. Heartbeat job PASS. WF-13 #42527723683 PASS and fallback WF-06 #42527735064 FAIL: four HTTP 503 probes. | None |
| StockDividend | `e6469ac6617142b349144101a1192cb6aa7104ad` | CI #42440810105 PASS; scraper #42457182511 fail-closed before dependencies because `VNSTOCK_API_KEY` is missing. No current-master publisher run; workflow-only changes are excluded by `.github/**` path-ignore. | None |
| Media Generation | `54f3a76a5f8861842fd1bae698c4cb0fa8c9034d` | CI #42239703151 PASS; no new publisher. Last snapshot showed digest-resolved backend/frontend 1/1; runner active/enabled/listener-present. | None |
| Authentication | `cb907a63df0e0441b54b7b930ecdbfa97a5e52e1` | CI #42478653766 PASS; no new release/promotion; PR #76 remains draft. | #76 draft |

Platform native schedule gaps: reconcile 15,672s/2,700s; inspection 18,901s/4,500s; recovery 15,605s/2,700s; watchdog 15,517s/2,700s. Inspection runner queue telemetry was 0m, so no runner-queue cause was evidenced. TCE WF-06 gap 16,293s/1,500s; WF-12 gap 14,317s/1,500s. All cadence budgets remain violated. Manual/recovery events do not satisfy native acceptance.

The recovery-driven reconciliation payload was `ref=master`, `mode=apply`, `target_app=all`, `allow_image_changes=false`. It provisioned/verified Auth runtime Secret, verified GHCR read access, kept shared `ghcr-pull` unchanged, inspected only active MicroFE/TCE blocked-image workloads (no failures), detected `drift=false` and skipped manifest apply, image promotion and rollout. No Stock/Media workload restart or scaling occurred.

Latest committed K3s snapshot remains #1481 at 20:14:51Z and is outside the 75-minute age budget at review. Recovery inspection #42527885366 was still in progress; do not claim a fresh snapshot until it completes. TCE/Auth/Keycloak remain 0/0; Stock Admin×2 and desired Backend remain ImagePullBackOff; Media runner retirement and external backup/DNS evidence remain blocked.

Preserve app-owned tests/builds/immutable GHCR publication and Platform-owned production manifests, shared pull credentials, digest verification, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the sole production apply authority; `inspect-vps.yml` remains read-only. No cron/freshness budget change, workflow deletion, direct SSH/Compose authority, namespace/PVC/PV deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## Inspection completion — 2026-11-09 05:01 ICT

Recovery-driven inspection #42527885366 completed successfully. PR #1484 was merged at `da24edc6019ac18be2f298eed06803848362aa68`; validation #42528039006 passed. The committed snapshot generated at 21:59:12Z is fresh. It confirms the K3s node Ready, Media/MicroFE 1/1, Stock Admin×2 plus desired Backend still failing image pulls, TCE/Auth/Keycloak 0/0, Media runner active/enabled/listener-present, and Stock/Media storage preflight `storage-clean`. DNS ownership and remote runner registration are not inferred; external backup/retention remains unverified. Manual inspection is not native schedule acceptance.


## Cross-repo contract refresh — 2026-11-09 06:01 ICT

### Current ownership and publication state

- App repositories retain tests, builds and immutable GHCR publication; Platform Infra alone retains production manifests, shared GHCR pull credentials, digest/source verification, GitOps promotion/reconciliation, rollout and health verification.
- StockDividend PR #39 merged at `4be26f41072ec8d749ea8b92f1a517c714d2a214`. Its publisher performs a six-tag absence preflight (full source SHA + version/source SHA for scraper/admin/backend) before any push and serializes per source SHA. The publisher workflow still uses native ARM64 builds and registry digest verification. This is a workflow-level overwrite guard, not registry-side immutable-tag enforcement.
- StockDividend PR #40 is open at `78fe5bbffd97d999258df3a09a1e76c8d119e16b`. It removes the broad generic `not found` matcher and adds HTTP 401 plus ambiguous repository-not-found negative tests. Do not merge until exact-head CI is fully green.
- Stock publisher workflow path filters exclude workflow/script-only changes; PR #39 merge triggered CI #42533163812, not production image publication. Manual release remains explicitly gated by `STOCKDIVIDEND_PRODUCTION_RELEASE_ENABLED`.
- Stock scraper `VNSTOCK_API_KEY` is a separate ingestion credential. Missing key blocks scraper preflight only; it must not be used as an image-publisher credential.

### Schedule and runtime ownership evidence

- Native Platform reconcile/inspection/recovery/watchdog latest runs are #42521088881/#42530192980/#42520213983/#42520452305. Their observed gaps (15,672s/14,280s/15,605s/15,517s) exceed their existing budgets (2,700s/4,500s/2,700s/2,700s). Watchdog correctly fails; no cron/budget change is authorized.
- TCE native WF-06 #42531446260 and WF-12 #42527713763 remain outside the 1,500s cadence budget and fail. WF-06 logs show public HTTP 503s. WF-07 integration #42528513790 passes.
- Latest K3s inspection #42530192980 is read-only. Media/MicroFE active pods are 1/1 with registry digests; Stock desired Admin×2/Backend image `12d63b4` fails ARM64 manifest pulls; TCE/Auth/Keycloak remain 0/0 maintenance. Media runner remains active/enabled/listener-present. Stock/Media storage preflight is clean, but external data retention, DNS ownership and remote runner registration are not established.
- Manual reconciliation #42530382496 verified GHCR access and Auth runtime Secret, left shared `ghcr-pull` unchanged, found no drift and skipped manifest apply, promotion and rollout. Zero-replica Auth is not counted as live health.

Preserve purposeful CI, security, manual/release and scheduled workflows. Do not remove jobs solely because they are not part of the production apply path. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose production authority. TCE market-scan schedule unchanged.


## Stock GHCR guard follow-up — 2026-11-09 06:07 ICT

- PR #39 merged: six-tag preflight checks full source SHA and version/source SHA tags for Scraper/Admin/Backend before first push, with per-source-SHA non-cancelling concurrency. Exact-head CI #42528788805 and post-merge CI #42533163812 passed all seven jobs.
- PR #40 merged at `1a18cabf32c6cc5f85f4157b5142a6d9f0d9d9b5`: broad generic `not found` matching removed; explicit HTTP 404 and known missing-manifest responses remain the only absent-tag signals. Regression cases prove 401 and ambiguous repository-not-found responses fail closed. Exact-head CI #42533247153 passed all seven jobs, including native ARM64 builds with push=false.
- Post-merge CI #42533562194 is still running; no production publication or Platform dispatch was triggered by these workflow/script-only changes. Verify this run before marking the Stock master CI lane fully green.
- These checks are workflow-level overwrite prevention, not GHCR registry-side immutable-tag enforcement. Platform promotion must continue to use verified registry digests.

App-owned publication and Platform-owned production GitOps boundaries remain unchanged. Native Platform/TCE schedule gaps remain outside existing budgets; do not change cron or freshness thresholds. Preserve all purposeful CI/security/manual/release/scheduled workflows. No direct SSH/Compose deployment authority. TCE market-scan schedule unchanged.


## Latest execution delta — 2026-11-09 07:08 ICT

- Platform Infra: master ecafca5f594f9984baa294ee679afed6afd245bb after read-only inspection PR #1489; validation #42538111845 PASS. Open human-decision drafts #1314/#544/#541/#539 remain gated.
- TCE Dashboard: PR #1031 adds same-source-SHA non-cancelling concurrency and a fail-closed pre-push guard for web/service release tags. The guard rejects existing tags, 401/403, ambiguous repository-not-found and unknown errors; only explicit 404/known missing-manifest responses mean absent. Regression tests run through the existing WF-01P release-contract validation. WF-01P #42538473285, WF-02 #42538473275 and WF-05 #42538473166 passed; do not merge until the exact current PR head and all required checks are green. WF-03 remains manual/master-only; no publish/dispatch occurred.
- StockDividend: PRs #39/#40 merged; master CI #42533562194 PASS 7/7. The GHCR guard is workflow-level overwrite prevention, not registry-side immutable-tag enforcement. No production publication/digest handoff; scraper credential VNSTOCK_API_KEY remains missing.
- Media Generation: master CI #42239703151 PASS; backend/frontend remain digest-pinned 1/1 in the latest K3s snapshot. Dedicated runner remains active/enabled/listener-present; retirement, backup/retention and DNS evidence remain blocked.
- Authentication: master CI #42478653766 PASS; PR #76 remains draft. Auth runtime Secret is present/verified by reconciliation #42537804409, but Auth/Keycloak remain intentional 0/0 and are not live-healthy.
- Latest native schedule evidence remains outside budgets: Platform reconcile/inspection/recovery/watchdog gaps 15,672s/14,280s/12,727s/12,672s against 2,700s/4,500s/2,700s/2,700s; TCE WF-06/WF-12 gaps 13,481s/14,317s against 1,500s. Do not change cron or budgets; GitHub administrator investigation required.
- Latest read-only K3s snapshot #42537975671: node Ready/ARM64, disk 56%, RAM ~19 GiB, restart_required=yes; Media/MicroFE 1/1, Stock desired Admin/Backend image pulls failing due ARM64 manifest mismatch, TCE/Auth/Keycloak 0/0. Stock/Media storage preflight clean but external data retention, DNS and remote runner registration remain unverified.
- reconcile-vps.yml remains the only production apply authority; inspect-vps.yml remains read-only. No promotion, manifest apply, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## TCE publisher hardening merge — 2026-11-09 07:11 ICT

- TCE Dashboard PR #1031 merged by squash at ddf5811a7994aab08236028cff04e0a78ffd2e3e. Exact-head PR checks passed: WF-01P #42538473285 (release contract and mocked tag-absence tests), WF-02 #42538473275, WF-05 #42538473166; push-format/unit-test runs #42538448641/#42538448647 passed.
- WF-03 remains manual-only/master-only. It now serializes publication per source SHA and checks both web/service version+full-SHA GHCR tags before the first push. Only explicit HTTP 404/known missing-manifest responses count as absent; existing tags, 401/403, ambiguous repository-not-found and unknown errors fail closed. This is workflow-level overwrite prevention, not registry-side tag immutability.
- Post-merge TCE CI #42538802539/#42538802538/#42538802541 was still running at review. No production image publication or Platform dispatch occurred.
- Platform documentation PR #1490 records the 07:08 snapshot and this 07:11 post-merge delta; revalidate its updated exact head before merge. No cron, freshness budget or TCE market-scan schedule change.


## Publisher guard rollout update — 2026-11-09 07:18 ICT

- TCE Dashboard PR #1031 merged at ddf5811a7994aab08236028cff04e0a78ffd2e3e. Exact-head checks passed; post-merge WF-01 #42538802539, WF-02 #42538802538 and WF-05 #42538802541 all PASS. WF-03 remains manual/master-only; no publication or Platform dispatch.
- Authentication PR #90 merged at 047abc08e123d8bde7678104899d00aa8782624a. Exact-head PR CI #42539110908 passed; logs show 26 suites/135 tests, typecheck/build, native ARM64 non-publishing build and Auth GHCR guard tests passed. Post-merge #42539350154 was still in progress. No Auth release or dispatch occurred.
- Media Generation PR #74 is open at 5ed0d0bbf7bbd5942fa5a865f7e5c2de4ee72411. It adds a fail-closed pre-push check for frontend/backend release tags, same-SHA non-cancelling concurrency, negative tests and paths-ignore for guard/test-only changes. PR #42539297802 and push #42539276866 were still in progress. Media remains outside Platform GitOps; no runtime or runner changes.
- Platform latest native reconcile #42538596496 PASS at 00:08:54Z; watchdog workflow_run #42538746501 FAIL due gaps: 12,675s/14,280s/12,727s/12,672s against existing 2,700s/4,500s/2,700s/2,700s budgets. TCE WF-06/WF-12 gaps 13,481s/14,317s against 1,500s. Inspection queue wait 0m and no deployment lane >15m; investigate GitHub scheduler, do not change cron/budgets.
- Reconciliation #42538596496: shared ghcr-pull unchanged, Auth runtime Secret verified, active MicroFE/TCE scopes no image-pull failures, drift=false, apply skipped, no image changes. Auth zero-replica maintenance remains not live health.
- Platform PR #1490 validation #42538879776 passed at previous head 914f5ab; this delta requires a new exact-head validation. Latest K3s snapshot remains #42537975671 at 00:01:52Z. TCE market-scan schedule unchanged.


## Media guard merge — 2026-11-09 07:20 ICT

- Media Generation PR #74 merged at dcd698699c65ba6e73f6b43838975144777131c3 after exact-head CI #42539297802 passed. The validator log confirms mocked GHCR tag-preflight tests passed. The publisher now checks both frontend/backend release tags before the first push, binds the tag to the full source SHA, serializes same-SHA publication without cancellation, and excludes helper/test-only changes from the production publisher trigger.
- Post-merge Media CI #42539512417 was still running; release-contract validation passed and dependency installation was in progress. No production publisher run, image publication or Platform dispatch occurred. Media remains retired from Platform GitOps ownership; runner/runtime state unchanged.
- Auth PR #90 merged at 047abc08e123d8bde7678104899d00aa8782624a; post-merge CI #42539350154 PASS. TCE PR #1031 merged at ddf5811a7994aab08236028cff04e0a78ffd2e3e; post-merge WF-01/WF-02/WF-05 all PASS. Stock PR #39/#40 merged; CI #42533562194 PASS 7/7.
- Platform docs PR #1490's previous head c4f36d0db6f5ddb8f25b53baba1c3183a17ac066 was under validation #42539467189 before this delta; revalidate the new exact head before merge. TCE market-scan schedule unchanged.


## App-owned immutable tag guard rollout complete — 2026-11-09 07:22 ICT

- StockDividend: PR #39/#40 merged; six-tag preflight across Scraper/Admin/Backend, fail-closed missing-manifest classification and same-SHA serialization. Master CI #42533562194 PASS 7/7.
- TCE Dashboard: PR #1031 merged; web/service release-tag preflight and same-SHA serialization. Post-merge WF-01/WF-02/WF-05 #42538802539/#42538802538/#42538802541 all PASS.
- Authentication: PR #90 merged; raw-SHA and version/full-SHA preflight before Buildx push. Exact-head PR CI passed 26 suites/135 tests plus typecheck/build/ARM64 non-publishing build; post-merge #42539350154 PASS.
- Media Generation: PR #74 merged; frontend/backend release-tag preflight, same-SHA serialization, helper/test path exclusions. Exact-head CI and post-merge #42539512417 PASS. No Platform dispatch was reintroduced; Media remains retired from Platform GitOps ownership.
- All guards are workflow-level overwrite prevention, not GHCR server-side immutability. Registry digest verification and digest-pinned Platform promotion remain mandatory. Guard-only changes did not publish images or dispatch production promotion.

Platform master dd1bca11e3c59c92f920ec5e4896fb8d643be272 after PR #1490; exact-head validation #42539583925 and post-merge validation #42539638207 PASS. Open human-decision drafts: Platform #1314/#544/#541/#539 and Auth #76. Native Platform/TCE schedule cadence remains outside budget; queue telemetry does not show saturation. TCE market-scan schedule unchanged.


## Cross-repo release and dispatch boundary update — 2026-11-09 07:57 ICT

- App-owned workflow-level immutable-tag guards are merged in StockDividend #39/#40, TCE Dashboard #1031, Authentication #90 and Media Generation #74. These guards block workflow-level overwrites and ambiguous registry errors; they do not provide GHCR server-side immutability. Platform must continue verifying tag-to-digest mapping, ARM64 descriptors and digest-pinned manifests.
- The dedicated Platform branch `fix/gitops-promotion-dispatch-provenance-20261109-0757-ict` strengthens the final production handoff. MicroFE, TCE and Auth producers attach source commit plus the Platform promotion run ID/attempt, workflow path and head SHA. The sole apply workflow validates those values against the Actions API and the exact completed-successful master promotion run before it proceeds with repository-dispatch apply/image-change behavior.
- The payload validator accepts only Auth/TCE/MicroFE and their expected components/release formats; StockDividend and Media Generation remain retired from active Platform GitOps. Unknown payload keys, mismatched source SHA/release, non-master run, wrong workflow/head/attempt, incomplete run or failed conclusion are rejected.
- The validator is read-only and its path is excluded from recovery push bootstrap. Existing `validate-github-actions` runs its positive/negative regression tests. Exact-head CI is required before merge; no production image publication or dispatch was executed by this code change.
- App repositories continue to own tests/builds and immutable GHCR publication. Platform Infra alone owns production manifests, shared pull credentials, digest/source verification, GitOps promotion/reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only. No direct SSH/Compose authority.
- Native schedule cadence remains outside existing budgets; manual/recovery events are not native acceptance. No cron/freshness change and no TCE market-scan schedule change.


## Promotion-run execution attestation — 2026-11-09 08:10 ICT

- PR #1492 now requires each `gitops-promoted-ready` event to reference a completed successful Platform promotion workflow run on master with exact run ID, attempt, workflow path and head SHA.
- Follow-up PR #1493 closes the remaining no-op-run case: the reconcile gate also fetches the exact run's Actions jobs and requires the app-specific promotion work to have completed successfully. MicroFE requires its digest-promotion job; TCE requires both paired-promotion and coordinator jobs; Auth requires its Auth promotion job.
- A completed-successful workflow with the relevant job skipped, absent or failed is rejected. This is separate from source app publisher provenance, which remains validated in the promotion workflow, and from registry tag-to-digest/ARM64 checks.
- No direct application deployment is introduced. The app repositories still own builds/tests and immutable GHCR publication; Platform alone owns GitOps manifests, shared pull credentials, digest promotion, apply, rollout and health.
- The read-only validator remains excluded from recovery push bootstrap. No cron, freshness budget or TCE market-scan schedule changed.


## Ready-event registry binding — 2026-11-09 08:14 ICT

- The final `gitops-promoted-ready` gate now has three independent checks: strict payload/source-SHA validation; exact originating promotion run and app-specific job success; current GitOps manifest digest and GHCR tag-to-digest/ARM64 validation.
- `verify-gitops-ready-image-refs.py` allowlists only Auth/TCE/MicroFE and requires every expected image entry to be digest-pinned. It rejects missing/duplicate image entries, tag-only `newTag`, duplicate tag/digest fields and malformed digest values.
- Reconcile re-reads each immutable source tag using the expected manifest digest and then reads the digest reference itself through `validate-ghcr-image-reference.sh`. This prevents a successful but unrelated/replayed promotion run from authorizing an arbitrary manifest image change.
- This registry check runs after GHCR read-access preflight and before runtime Secret provisioning or shared pull-credential mutation. It is read-only and does not change the normal scheduled reconciliation path.
- The image-ref helper is self-tested in GitHub Actions and excluded from recovery push bootstrap. No cron, freshness budget or TCE market-scan schedule change.


## GitOps manifest image-identity hardening — 2026-11-09 10:04 ICT

- Platform PR #1500 is open from `fix/gitops-ready-image-identity-20261109-1004-ict` (base master `c0c4417c8b317ced59444d61d2671edf879f646a`); exact-head validation is pending.
- The ready-event manifest validator now checks that each app's entire Kustomize image set exactly equals the allowlist. Extra, missing, duplicate or malformed `- name:` entries are rejected.
- If `newName:` is present, it must equal the allowlisted GHCR repository associated with the verified immutable tag/digest. A redirect to another repository or duplicate/malformed override is rejected.
- Self-test target is 5 positive extraction cases and 12 negative contract cases. The GitHub Actions workflow already invokes this helper and workflow-contract validator.
- This closes a repository-identity gap: previously the preflight could verify `image:$immutable_tag` in the allowlisted repository while Kustomize rendered a different `newName`.
- No production dispatch, publication, promotion, apply, rollout or credential mutation. Auth/TCE tag-only manifests continue to fail the ready-event gate until their own promotion workflows merge digest pins; MicroFE remains digest-pinned.
- Issue #1497 remains the administrator-owned native schedule investigation. Cron, freshness budgets and TCE market-scan schedule unchanged.


## Post-merge image identity contract — 2026-11-09 10:12 ICT

- Platform PR #1500 merged at `640eab00e13ff1460c47f394138598da98e096cb`, exact head `046d323593c0546a5119895c77ff945456874b54`.
- Exact-head `validate-github-actions` #42555164957 and `validate-manifests` #42555164890 PASS. The Actions log confirms 5 positive / 12 negative GitOps image-ref tests and the workflow-contract validator passed.
- The GitOps-ready image validator now requires an exact app-specific image set and binds optional `newName:` to the allowlisted GHCR repository. Additional/missing/duplicate image entries and repository redirects fail closed.
- Master is `640eab00e13ff1460c47f394138598da98e096cb`. No post-merge workflow run was visible at checkpoint time; post-merge CI remains unverified.
- Auth/TCE current manifests are tag-pinned until a promotion PR merges digest pins; ready-event validation intentionally blocks before production mutation. MicroFE remains digest-pinned.
- Native schedule investigation remains issue #1497. No cron/freshness changes and no TCE market-scan schedule change.


## Root-scoped GitOps image-ref contract — merged Platform PR #1502 (2026-11-09 11:00 ICT)

- PR [#1502](https://github.com/phanthienquoc/platform-infra/pull/1502) merged by squash at \`f23f272a746dd1991f868630c57c914f2ebac1b4\` from exact head \`51dd0b5e1c1bc804a0a24b4b57437175f19176f7\`.
- \`verify-gitops-ready-image-refs.py\` now scopes extraction to exactly one root-level \`images:\` block. It no longer counts unrelated \`- name:\` entries from \`configMapGenerator\` or other root sections.
- Nested/mis-scoped entries, empty image blocks, unsupported fields, malformed indentation, duplicate fields, image-set mismatches and repository redirects fail closed. Existing per-app allowlists and digest-only ready-event requirements remain.
- Regression coverage: 5 positive digest extractions, 1 section-scope isolation case, 16 negative cases.
- Exact-head \`validate-github-actions\` #42559803093 PASS and \`validate-manifests\` #42559803103 PASS. The superseded earlier head had a self-test failure, corrected before merge. No post-merge push run was exposed by the connector at checkpoint time; post-merge CI remains unverified.
- Current heads: Platform \`f23f272a\`, TCE \`ddf5811a\`, Stock \`1a18cabf\`, Media \`dcd69869\`, Authentication \`047abc08\`. Open drafts: Platform #1314/#544/#541/#539 and Authentication #76; no app publisher PR remains open.
- Auth/TCE production manifests remain tag-pinned until digest promotion; their ready events remain fail-closed. MicroFE remains digest-pinned. Stock/Media remain retired from Platform GitOps.
- Native schedule issue #1497 remains open; latest K3s snapshot is stale (>3h at checkpoint). Stock ARM64 publication/credential, TCE/Auth owner approvals, Media runner retirement and external backup/DNS evidence remain blockers.
- App-owned GHCR guards are workflow-level overwrite prevention, not registry-side immutable-tag enforcement. No production image publication/promotion, apply, rollout, scaling, deletion or credential mutation. No cron/freshness or TCE market-scan schedule changes.


## Observed execution state — 2026-11-09 12:02 ICT / 05:02 UTC

- Current master heads: Platform 4e5d77df98fd86adac8670170440c0201d6f2be5; TCE ddf5811a7994aab08236028cff04e0a78ffd2e3e; Stock 1a18cabf32c6cc5f85f4157b5142a6d9d9b5; Media dcd698699c65ba6e73f6b43838975144777131c3; Authentication 047abc08e123d8bde7678104899d00aa8782624a.
- Platform PR #1502 post-merge validate-github-actions #42559897903 and validate-manifests #42559897980 PASS; PR #1503 post-merge validate-manifests #42560097448 PASS.
- TCE latest master unit-test lane #42538802541 PASS; native WF-06 #42548397383 and WF-12 #42546629459 FAIL. WF-06 has four strict public health probes failing (TCE web/API and Auth liveness/readiness) while TCE/Auth are intentional 0/0.
- Stock master CI #42533562194 PASS 7/7. Scheduled scraper #42457182511 stops at missing VNSTOCK_API_KEY preflight before dependency installation or scrape.
- Media master CI #42539512417 PASS; Authentication master CI #42539350154 PASS. App-owned GHCR guards remain merged; no current production image publication/digest handoff.
- Open drafts: Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE, Stock or Media.
- Native schedule latest events as of 05:02:47Z: Platform reconcile #42538596496 (17,633s gap), inspection #42548015626 (11,287s), recovery #42537793367 (18,189s), watchdog #42537967026 (18,071s); TCE WF-06 #42548397383 (11,018s), WF-12 #42546629459 (12,259s). All exceed existing budgets. Platform issue #1497 updated with fresh evidence; administrator action required.
- K3s snapshot #42548015626 / debug/vps-latest.md generated 01:54:48Z and is stale at this checkpoint. Node Ready, disk 56%, RAM ~19 GiB, restart_required=yes; Media/MicroFE 1/1, Stock desired Admin/Backend image pulls failing (12d63b4), TCE/Auth/Keycloak 0/0. Media and Platform runner services active. Do not use this stale snapshot for rollout/decommission authorization.
- Auth/TCE manifests remain tag-pinned; ready-event remains fail-closed until app-owned digest publication and Platform promotion. MicroFE is digest-pinned. Stock/Media remain retired from Platform GitOps.
- No production publication, promotion, apply, rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## Execution evidence — 2026-11-09 13:00 ICT

- Platform PR #1504 exact-head validation #42565213174 and post-merge validation #42565271145 both completed successfully. Post-merge rendered 78 Kubernetes objects and passed manifest, Auth GitOps, secret, immutable-image, Keycloak and network-boundary validation.
- TCE #42538802541 backend unit tests PASS; native WF-06 #42548397383 has four failed public health jobs. Do not treat the service-health failure as a scheduler-delivery measurement.
- Stock #42533562194 passed all seven CI jobs. The last observed scraper failure #42457182511 checked out older commit `e6469ac`; its empty secret observation does not establish current master secret state.
- Media #42539512417 application test/build PASS. Authentication #42539350154 ARM64 non-publishing build and validation PASS.
- The available commit-workflow-runs connector is PR-only; empty master queries do not prove no newer workflow runs. The complete latest native schedule event list and a fresh K3s inspection were not available in this execution.
- Preserve strict production gates, exact app/Platform ownership, and the TCE market-scan schedule.


## Execution evidence — 2026-11-09 23:56 ICT / 16:56 UTC

- Current default-branch heads: Platform `c3522e4452f95350610f8c6fc3dcea6d2860427f`; TCE `65af89f69ffe0d844a9b63e2434bc3f8cedfebb7`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open human-decision drafts: Platform #1314/#544/#541/#539 and Authentication #76. No open PRs in TCE, Stock or Media.
- Platform push manifest validation #42656964670 PASS. Native recovery schedule #42657359651 PASS; native freshness watchdog #42657625219 FAILs correctly on the historical cadence gaps; read-only inspection #42657403805 PASS (workflow_dispatch); recovery workflow_run #42657691775 PASS. These events are distinct; only #42657359651 and #42657625219 count as native schedule events.
- TCE master build #42586355695, format #42586356008 and backend tests #42586355696 PASS. Native WF-06 #42594757482 and WF-12 #42587926693 remain failures; manual WF-06 #42594805077 fails four public HTTP 200 probes.
- Stock master CI #42610360402 PASS 7/7, including safe preflight contract and ARM64 non-publishing build. Historical scheduled scraper failure #42457182511 uses old SHA `e6469ac`; current master credential state is not verified.
- Media master CI #42539512417 PASS. Authentication master CI #42654579277 PASS; Auth dispatch fixture PR run #42654291067 PASS. No production app publisher or dispatch run was observed.
- Native schedule partial resumption: Platform recovery #42657359651 at 16:41:46Z and watchdog #42657625219 at 16:43:22Z are new original schedule events. Historical gaps remain 37,669s and 37,408s respectively; Platform reconcile/inspection and both TCE health lanes remain stale. The watchdog failure is correct strict behavior. GitHub administrator enqueue/delivery evidence remains required.
- Fresh read-only K3s inspection #42657403805 PASS, snapshot 16:42:11Z. Node Ready/ARM64; disk 56% (~20 GiB free); RAM available 19 GiB; restart_required=yes. Media and MicroFE core workloads 1/1; Stock Admin×2 and one desired Backend pod ImagePullBackOff on historical tag `12d63b4` lacking ARM64 descriptor; older Backend and Frontend remain available; TCE/Auth/Keycloak remain 0/0; public OIDC 503. Platform and Media runner services remain active/enabled.
- Stock/Media storage preflight is clean for PVC/PV/VolumeSnapshot references; only PVC is in `k3s-debug`. Production manifests contain no active Stock/Media references. This does not prove external backup/retention/DNS ownership or remote Media runner unregistration. No delete plan/action.
- Auth receiver exact schema merged in Platform #1534; Auth master CI fixtures PASS. Auth/TCE remain tag-pinned pending app publication and Platform digest promotion. MicroFE remains digest-pinned. Stock/Media remain retired from active GitOps but workloads are not deleted.
- No production image publication/promotion, apply, rollout, scaling, deletion, runner retirement, DNS/database/storage mutation or host maintenance. No cron/freshness change; TCE market-scan schedule unchanged.


## Cross-repo execution inventory — 2026-11-10 06:00 ICT / 2026-11-09 23:00 UTC

### Verified current repository heads and workflow state

| Repository | Master SHA | Open PRs | Latest master CI evidence |
|---|---|---|---|
| `platform-infra` | `5a97c734db120c8cea76a3971e01d2a2ef3b84e8` | #1314/#544/#541/#539 (drafts) | `validate-manifests` #42710407011 PASS |
| `TCE-dashboard` | `68660a20e5bf3472a122c59d75b49ffce16a2ce9` | none | WF-01 #42709513845, WF-02 #42709513839, WF-05 #42709513831 PASS |
| `stockdividend` | `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61` | none | CI #42610360402 PASS 7/7 |
| `media-generation` | `dcd698699c65ba6e73f6b43838975144777131c3` | none | CI #42539512417 PASS |
| `phanthienquoc-authentication` | `eab85fab32d7c9baef750c1fedbb93deb8c1333f` | #76 (draft) | CI #42654579277 PASS |

### Workflow event classification and latest operational evidence

- TCE native WF-07 #42711312505 succeeded; it is a third-party integration schedule and not a WF-06/WF-12 deployment-health freshness event.
- TCE WF-12 #42711341231 is a `workflow_run` watchdog failure caused by stale native WF-06 delivery. Its Platform heartbeat dispatch succeeded.
- TCE WF-13 #42711368741 successfully dispatched a deduplicated read-only WF-06 fallback; fallback #42711398985 failed all four public HTTP 200 probes with HTTP 503.
- Platform recovery #42711357014 succeeded on the exact TCE heartbeat. It did not dispatch duplicate reconciliation or inspection because recent runs existed.
- Latest reconciliation #42709362025 passed GHCR read preflight, Auth runtime Secret verification/provisioning, shared pull-credential reconciliation, managed image-pull checks and TCE tag pairing. `ALLOW_IMAGE_CHANGES=false`; image promotion and production manifest apply were skipped.
- Latest K3s snapshot is #42709680634 (`workflow_dispatch`, not native schedule), generated 22:12:13Z. Media/MicroFE core workloads are 1/1; TCE/Auth/Keycloak are 0/0; Stock desired Admin/Backend pods still fail ARM64 image pull on `12d63b4`; public OIDC is HTTP 503. Host restart is required but not authorized.
- Native freshness lanes remain outside budget: Platform reconcile #42664347392 (gap 37,823s), inspection #42694932077 (39,672s), recovery #42657359651 (37,669s), watchdog #42657625219 (37,408s), TCE WF-06 #42689871258 (37,834s), WF-12 #42681246237 (37,832s). Budgets remain 2,700s / 4,500s / 2,700s / 2,700s / 1,500s / 1,500s respectively. Do not count manual, workflow_run, repository_dispatch or WF-07 runs as acceptance for these lanes.

### Ownership and preserved workflows

- App repositories own tests/builds and immutable GHCR image publication: TCE, StockDividend, Media Generation and Authentication.
- Platform Infra owns production manifests, shared GHCR pull credentials, publisher provenance/digest verification, GitOps promotion/reconciliation, rollout and health verification.
- Preserve CI/test/security workflows and purposeful manual/release/scheduled jobs. Keep TCE WF-06 strict HTTP 200 probes and its separate WF-12/WF-13 stale-schedule watchdog/recovery. Keep Stock's weekend scraper fail-closed; the current missing-secret owner action is tracked in Stock issue #42.
- StockDividend and Media Generation stay retired from active Platform GitOps until an explicit reactivation decision; do not delete namespaces or retire the dedicated Media runner without backup, retention, DNS and remote-registration evidence.
- `reconcile-vps.yml` remains the sole production apply authority. `inspect-vps.yml` is read-only. Do not add direct SSH/Compose deployment authorities.

### Outstanding owner/operator dependencies

1. GitHub administrator: schedule enqueue/delivery telemetry for Platform issue #1497.
2. TCE/Auth owners: recovery/rollback approval, app-owned release digests and live HTTP 200 health evidence.
3. Stock owner: private `VNSTOCK_API_KEY` configuration and authenticated `preflight_only=true`.
4. Media owner: remote runner unregister proof, external backup/retention and authoritative DNS ownership.
5. Platform operator: approved maintenance window and rollback plan for host package updates/restart.

No production release, digest promotion, manifest apply, scaling, deletion, credential rotation, runner retirement or host maintenance was performed. TCE market-scan schedule unchanged.


## 2026-11-10 09:04 ICT — TCE backup workflow classification and current readiness

### Purposeful backup workflow — preserve

- TCE Dashboard `.github/workflows/wf-07-tce-backup.yml` is a distinct scheduled/manual backup job (`30 18 * * *` UTC), separate from `.github/workflows/wf-07-tce-integration-check.yml`.
- Native backup run [#42737399806](https://github.com/phanthienquoc/TCE-dashboard/actions/runs/42737399806) succeeded on master SHA `68660a20e5bf3472a122c59d75b49ffce16a2ce9`. Its job log confirms an SSH tar backup of TCE development/staging/production directories and seven-day archive retention cleanup.
- This is backup/retention only: it does not run Compose, kubectl, Kustomize, GitOps promotion, rollout or manifest apply. Keep it; do not classify it as a competing deployment authority or as WF-06/WF-12 health freshness evidence.
- Security follow-up: it currently disables SSH host-key checking. Before changing it, obtain and verify the authoritative VPS host key from the owner; do not trust an unverified `ssh-keyscan` result. The Actions log does not prove archive restoreability.

### Current readiness evidence

- Current master heads: Platform `8e5ed100`, TCE `68660a20`, Stock `b1b5e177`, Media `dcd69869`, Authentication `eab85fab`. Open owner-decision drafts: Platform #1314/#544/#541/#539; Authentication #76. No open PRs in TCE/Stock/Media.
- Native schedule freshness remains out of budget for all six monitored lanes. The TCE WF-07 Backup schedule is deliberately excluded from the WF-06/WF-12 health lanes.
- Platform `TCE_ACTIONS_READ_TOKEN` remains absent; TCE Actions history is warning-only/unverified inside Platform until a read-only fine-grained PAT is configured.
- Latest scheduled reconcile #42731410572 passed GHCR pull preflight, provisioned/verified Auth runtime Secret, left shared `ghcr-pull` unchanged, found no active TCE/MicroFE image-pull failures, confirmed TCE release pairing and drift=false, and skipped manifest apply.
- Stock desired Admin/Backend pods remain ImagePullBackOff on historical ARM64-incompatible tag `12d63b4`; do not rotate shared credentials or republish a mutable tag as a workaround.
- TCE/Auth are intentional 0/0 maintenance; HTTP 503 remains a real health failure. The latest full K3s snapshot is manual and stale at this checkpoint. No runtime change is authorized from it.



## Cross-repo workflow inventory checkpoint — 2026-11-10 09:59 ICT / 02:59:54 UTC

### Current heads and open PRs

| Repository | Current master | Open PRs | Latest relevant evidence |
|---|---|---|---|
| `platform-infra` | `80f137db` | #1562 health-state contract; drafts #1314/#544/#541/#539 | Reconcile #42744815372 SUCCESS; inspection #42741845747 SUCCESS; recovery #42744976026 SUCCESS |
| `TCE-dashboard` | `68660a20` | none | WF-06 schedule #42744759966 FAILURE (HTTP 503); WF-12 schedule #42741584886 FAILURE; WF-07 backup #42737399806 SUCCESS |
| `stockdividend` | `b1b5e177` | none | CI #42610360402 PASS 7/7; Stock issue #42 still awaits owner credential preflight |
| `media-generation` | `dcd69869` | none | CI #42539512417 PASS; runtime remains active but remote runner unregister/backup/DNS evidence is incomplete |
| `phanthienquoc-authentication` | `eab85fab` | draft #76 | CI #42654579277 PASS; production runtime remains intentional 0/0 maintenance |

### Authority boundaries and preserved workflows

- App repositories own application tests/builds and immutable GHCR publication. Platform Infra owns production manifests, shared GHCR pull credentials, publisher provenance/digest verification, GitOps promotion/reconciliation, rollout and health verification.
- `reconcile-vps.yml` remains the only production apply authority. `inspect-vps.yml` remains read-only. Do not introduce direct SSH/Compose deploy authorities.
- Preserve TCE WF-06 strict HTTP 200 checks, WF-12 schedule watchdog, WF-13 read-only fallback, and the separate WF-07 backup/retention workflow. WF-07 backup is not a deployment authority or health freshness lane.
- Preserve Stock weekend scraper fail-closed credential preflight. The historical missing-secret observation is on older SHA `e6469ac`; current `VNSTOCK_API_KEY` state is not established by that run.
- StockDividend and Media Generation remain retired from active Platform GitOps; existing workloads/namespaces are not deleted. The observed Stock ARM64 image failure is not a reason to rotate shared GHCR credentials.

### New machine-readable workload health contract (PR #1562)

- `verify-workload-health.sh` emits `health_state=healthy|maintenance|partial-maintenance`, `active_scopes`, and `maintenance_scopes` to `GITHUB_OUTPUT` only after all active-scope checks pass.
- All four deployment jobs expose the outputs. `deployment-lane-summary` distinguishes live health from zero-replica maintenance and rejects absent/unknown state. This prevents an intentional 0/0 lane from being reported as live healthy while keeping maintenance non-blocking.
- `verify-workload-health.test.sh` covers healthy, all-maintenance and mixed scopes. `validate-workflow-contracts.py` enforces output wiring and summary semantics. PR #1562 is pending exact-head checks; no merge yet.

### Native schedule and production readiness

- All six monitored native inter-arrival gaps remain above existing budgets. Latest TCE WF-06 is now fresh by age but failed all four HTTP 200 probes with 503; latest native WF-12 remains stale. Platform's latest confirmed native reconcile/inspection/recovery/watchdog events remain stale. Do not count manual, workflow_run, repository_dispatch or WF-07 backup events as native acceptance.
- Last verified Platform `TCE_ACTIONS_READ_TOKEN` was empty in smoke #42734770430. GitHub administrator telemetry and owner provisioning remain outstanding.
- Latest K3s snapshot #42741845747 is a fresh manual inspection (generated 02:18:38Z; 2,476s old at checkpoint). Node Ready; Media/MicroFE core workloads healthy; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ARM64 image pulls fail on `12d63b4`; public OIDC 503; Media runner active.
- No production image publication/promotion, manifest apply, rollout, scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.


## Post-merge workflow inventory checkpoint — 2026-11-10 10:12 ICT / 03:12:17 UTC

### Health-state reporting contract is merged and exercised

- Platform PR [#1562](https://github.com/phanthienquoc/platform-infra/pull/1562) merged at `03:10:23Z`, squash SHA `79df5adabf5e2060d94ececcf02f0b3bd97a9ca6`. Exact-head `validate-github-actions` #42747586573, `validate-manifests` #42747586404 and `keycloak-ci` #42747586455 passed; post-merge #42747680413/#42747679518/#42747679458 also passed.
- The first post-merge `reconcile-vps.yml` push run [#42747679517](https://github.com/phanthienquoc/platform-infra/actions/runs/42747679517) completed SUCCESS. `TARGET_APP=all`, `ALLOW_IMAGE_CHANGES=false`; GHCR preflight passed; Auth runtime Secret verified; shared `ghcr-pull` unchanged; TCE release pairing passed; `drift=false`; production apply and rollout were skipped.
- The new machine-readable output was exercised against the real cluster: Auth=`maintenance` (0 active/1 maintenance scope), TCE=`maintenance` (0 active/1 maintenance scope), MicroFE=`healthy` (1 active scope), Keycloak skipped for target `all`. The final summary explicitly reports Auth/TCE as intentional zero-replica maintenance with no live health asserted, and MicroFE as live health verified.

### Workflow ownership and follow-up

- No competing deploy workflow was introduced or removed. App repositories remain responsible for tests/builds and immutable GHCR publication; Platform remains responsible for production manifests, shared GHCR pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health verification.
- TCE WF-07 Backup remains preserved as backup/retention-only SSH. TCE WF-06/WF-12/WF-13 remain separate health/schedule-monitoring lanes. The TCE market-scan schedule and all cron expressions remain unchanged.
- All six monitored native schedule ages and inter-arrival gaps are now outside their existing budgets at 03:12:17Z. TCE WF-06 latest native run #42744759966 failed HTTP 503 and is now older than its 1,500-second age budget; WF-12 #42741584886 is also stale. Platform's latest confirmed native lanes remain stale. Manual and `workflow_run` fallbacks do not count as native acceptance.
- Latest manual K3s inspection #42741845747 remains within its 75-minute snapshot budget but does not satisfy native inspection cadence. TCE/Auth/Keycloak remain 0/0; Stock desired Admin/Backend remain blocked by ARM64 image-manifest incompatibility; Media runner retirement evidence is incomplete.
- Owner dependencies remain: Platform `TCE_ACTIONS_READ_TOKEN` (last verified empty in #42734770430), GitHub Actions schedule delivery telemetry, TCE/Auth recovery approval and app-owned digests, Stock private `VNSTOCK_API_KEY` preflight, Media runner unregister/backup/DNS proof, and Platform maintenance-window approval.

No production image publication/promotion, manifest apply, rollout, scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance occurred. Auth runtime Secret was provisioned/verified and shared `ghcr-pull` was unchanged. `reconcile-vps.yml` remains the sole production apply authority.


## Operational checkpoint — 2026-11-10 10:56 ICT / 03:56:08 UTC

- Current master heads: Platform `67d16f7a` (scheduled inspection PR #1564 merged); TCE `68660a20`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`.
- Open owner-decision drafts: Platform #1314/#544/#541/#539; Authentication #76. No open PRs in TCE, Stock or Media.
- Platform latest operational runs: native inspection #42749270072 SUCCESS (03:24:47Z); recovery observer #42749529310 SUCCESS; watchdog observer #42749529614 FAILURE; follow-on observer runs #42749554598/#42749575865 SKIPPED. Inspection PR #1564 merged at exact validated head as commit #67d16f7a and changed only `debug/vps-latest.md`.
- TCE latest native health runs remain WF-06 #42744759966 FAILURE (02:44:03Z) and WF-12 #42741584886 FAILURE (02:16:15Z). WF-06 manual fallback #42744807014 also failed. WF-12/WF-13 `workflow_run` runs are not native schedule evidence. TCE master CI and the latest Stock, Media and Authentication CI remain PASS on the inspected master heads; Stock's latest CI is #42610360402 (7/7).
- Six native schedule inter-arrival gaps remain over budget: Platform reconcile 26,769s / 2,700s; inspection 24,367s / 4,500s; recovery 28,020s / 2,700s; watchdog 28,068s / 2,700s; TCE WF-06 23,806s / 1,500s; WF-12 25,383s / 1,500s. At 03:56:08Z, five current ages also exceed budget; inspection age is 1,881s and within 4,500s, but its historical gap still fails cadence acceptance.
- Watchdog logs explicitly show Platform gap failures and TCE history `missing-token` / unverified because Platform `TCE_ACTIONS_READ_TOKEN` is empty. Do not claim schedule delivery root cause without GitHub administrator enqueue/delivery telemetry.
- Fresh scheduled K3s snapshot #42749270072 / `debug/vps-latest.md` generated 03:24:55Z: node Ready/ARM64; K3s v1.36.3+k3s1; disk 56% (~20 GiB free); ~19 GiB RAM available; restart required. Media and MicroFE core are 1/1; Auth/Keycloak/TCE are 0/0; Stock Admin×2 and desired Backend are ImagePullBackOff on historical ARM64-incompatible `12d63b4`; legacy Stock Backend/Frontend 1/1; public OIDC 503; Media runner still active.
- Last confirmed reconciliation #42731410572 had GHCR preflight PASS, Auth runtime Secret verified, shared `ghcr-pull` unchanged, TCE pairing PASS, drift=false and apply skipped; it is now stale. No new image publication/promotion or rollout.
- Preserve TCE WF-06 strict HTTP 200 probes, WF-12/WF-13 schedule monitoring, and separate WF-07 backup/retention. App repos own builds/tests/immutable GHCR publication; Platform owns manifests, shared pull credentials, provenance/digest promotion, GitOps apply and health. `reconcile-vps.yml` remains the sole apply authority; `inspect-vps.yml` is read-only.
- Owner dependencies: GitHub schedule delivery telemetry; Platform `TCE_ACTIONS_READ_TOKEN`; TCE/Auth recovery and rollback approval plus immutable digests; Stock private `VNSTOCK_API_KEY` and safe preflight; Media remote runner unregister/backup/DNS proof; Platform host maintenance approval.
- No production publication, dispatch, promotion, apply, scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## 2026-11-10 12:02 ICT / 05:02:17 UTC — current readiness and cadence checkpoint

- Master heads: Platform `e69d92e6`; TCE `68660a20`; Stock `b1b5e177`; Media `dcd69869`; Authentication `eab85fab`.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 (draft); Authentication #76 (draft). No open PRs in TCE, Stock or Media.
- Latest CI evidence: Platform `validate-manifests` #42752967420 PASS (docs-only master push); TCE build/format/backend checks previously PASS, while WF-06/WF-12 health/schedule checks fail; Stock CI #42610360402 PASS 7/7; Media CI #42539512417 PASS; Auth CI #42654579277 PASS.
- Six native schedule lanes are all outside current-age and inter-arrival budgets at 05:02:17Z: Platform reconcile #42731410572 age 15,085s/gap 26,769s/budget 2,700s; inspection #42749270072 age 5,850s/gap 24,367s/budget 4,500s; recovery #42728605270 age 16,411s/gap 28,020s/budget 2,700s; watchdog #42728915720 age 16,267s/gap 28,068s/budget 2,700s; TCE WF-06 #42744759966 age 8,294s/gap 23,806s/budget 1,500s; WF-12 #42741584886 age 9,962s/gap 25,383s/budget 1,500s. Do not count manual, workflow_run, repository_dispatch, WF-07 backup or integration runs as native acceptance.
- Latest confirmed Platform reconciliation #42731410572 is 15,085s old and outside the 45-minute budget. It passed GHCR preflight, verified Auth runtime Secret, left shared `ghcr-pull` unchanged, confirmed TCE release pairing and drift=false, and skipped apply with `ALLOW_IMAGE_CHANGES=false`.
- Latest K3s snapshot #42749270072 was generated 03:24:55Z and is 5,842s old, beyond the 4,500s budget. Last-known workload posture: Media/MicroFE core 1/1; TCE/Auth/Keycloak 0/0; Stock desired Admin/Backend ImagePullBackOff on historical ARM64-incompatible `12d63b4`; OIDC 503; Media runner active. No runtime mutation is authorized from this stale snapshot.
- TCE WF-07 Backup #42737399806 succeeded as a purposeful backup/retention workflow; it is not a deploy authority or WF-06/WF-12 health freshness lane. Its SSH host-key bypass remains a security follow-up requiring an owner-verified host key.
- App repos continue to own tests/builds and immutable GHCR publication. Platform remains the sole owner of production manifests, shared pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health verification. `reconcile-vps.yml` is the only production apply authority; `inspect-vps.yml` remains read-only.
- Owner dependencies: GitHub schedule telemetry; Platform `TCE_ACTIONS_READ_TOKEN`; TCE/Auth recovery and rollback approval; Stock `VNSTOCK_API_KEY` safe preflight; Media runner unregister/backup/DNS proof; Platform host maintenance approval; TCE verified SSH host key.
- No new publication, promotion, apply, rollout, scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## 2026-11-10 13:31 ICT — receipt-backed TCE schedule evidence and authority checkpoint

- Platform master: `6c5579c4602a11c50bcb4da5bd765c64a5bbd5b3`; PR #1567 merged after exact-head `validate`/`lint` PASS. Post-merge `validate-github-actions` #42768692687, `validate-manifests` #42768692740 and push diagnostic watchdog #42768692778 PASS. Push diagnostics skip receipt collection by design; runtime receipt collection awaits the next scheduled/manual watchdog run.
- TCE WF-12's existing `PLATFORM_INFRA_TOKEN` dispatches `tce-schedule-heartbeat` receipts. Platform `recover-stale-ops.yml` validates payload identity and fetches source/heartbeat run metadata by ID. `reconcile-schedule-watchdog.yml` reads its own successful receipt history; `verify-tce-heartbeat-receipts.py` verifies source path, event=schedule, master, attempt 1, full SHA, receipt/source timestamps and deduplicates source IDs. Legacy path-less receipts are accepted only after run-by-ID source path verification.
- The obsolete Platform `TCE_ACTIONS_READ_TOKEN` PAT dependency has been removed from current credential guidance. Do not provision a new PAT for this path. Historical checkpoint references are superseded.
- Example evidence: WF-06 source #42744759966 → successful Platform receipt #42744797670; WF-12 source #42741584886 → successful Platform receipt #42741600132. Both source runs failed their health/watchdog jobs; the successful receipt proves schedule event/source identity, not service health.
- TCE WF-12 run #42744783670 confirms `Notify Platform Infra — TCE schedule heartbeat` and its dispatch step succeeded. No new TCE native schedule event has occurred since the source runs above.
- At 06:31:04Z, all six monitored native schedule ages and inter-arrival gaps remain outside unchanged budgets. Latest runs: Platform reconcile #42731410572, inspection #42749270072, recovery #42728605270, watchdog #42728915720; TCE WF-06 #42744759966 and WF-12 #42741584886. Do not count push/manual/workflow_run/repository_dispatch as native schedule acceptance.
- Latest K3s inspection #42749270072 and reconciliation #42731410572 are both stale at this checkpoint (11,177s and 20,412s old respectively). Do not authorize rollout or runtime mutation from their last-known state.
- Preserve app-owned publisher workflows and Platform's single production apply authority. No GHCR release/promotion, manifest apply, rollout, scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.


## 2026-11-10 14:22 ICT — receipt selector hardening and fresh inspection

- Master heads: Platform `183781fe03aa3786cac63cef6db7e2aac5427179`; TCE `68660a20e5bf3472a122c59d75b49ffce16a2ce9`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 (draft), Authentication #76 (draft). No open PRs in TCE, Stock or Media.
- Platform inspection PR #1569 merged from exact validated head `d25d8f8498c32727ada9cb28ab6520b7928b2008` as `183781fe`; it changes only the read-only debug snapshot. Exact-head manifest validation #42774949320 PASS.
- Reconciliation fallback #42774512102 SUCCESS: GHCR preflight passed for Auth/MicroFE/TCE, Auth runtime Secret verified, shared `ghcr-pull` unchanged, TCE release pairing passed, drift=false, apply skipped with `ALLOW_IMAGE_CHANGES=false`. Health outputs: Auth/TCE maintenance, MicroFE healthy, Keycloak skipped.
- Fresh manual K3s inspection #42774740602 generated snapshot 07:21:49Z. Node Ready/ARM64; disk 56%, ~19 GiB RAM available; Media/MicroFE core 1/1; TCE/Auth/Keycloak 0/0; Stock Admin and desired Backend ImagePullBackOff on historical ARM64-incompatible `12d63b4`; public OIDC 503; Media runner service/listener active. Storage preflight `storage-clean` is not runner-unregister/backup/DNS evidence.
- New native TCE WF-07 integration event #42774461163 successfully forwarded through TCE WF-12 workflow_run #42774478939 to Platform receiver #42774493174. The receiver validates source run ID/path/SHA/attempt. This is WF-07 schedule-delivery evidence only, not WF-06/WF-12 freshness or service health.
- New branch `fix/filter-untracked-tce-heartbeat-receipts-20261110-1422-ict` fixes a receipt-history selection defect: the collector previously capped the latest eight receipts before filtering non-monitored WF-07 path-bearing receipts. The new selector keeps WF-06/WF-12 receipts and legacy path-less receipts before the cap; static workflow-contract validation enforces ordering. Exact-head checks pending.
- Native WF-06 #42744759966 and WF-12 #42741584886 remain the latest known native health schedule runs; the latest manual WF-06 #42774522833 reports 275m schedule age with 0m queue wait and fails the existing 25m freshness check. Platform native lanes also remain stale; manual recovery/inspection runs are not native acceptance.
- App repositories still own builds/tests and immutable GHCR publication. Platform remains sole owner of manifests, shared pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health. `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` is read-only.
- No GHCR publication/promotion, manifest apply, rollout, scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. Cron/freshness budgets and TCE market-scan schedule unchanged.


## 2026-11-10 14:38 ICT — PR #1570 merged and publisher/authority audit

- Platform master `356ffe8e26f736b6ed58033db1bdcf8126a5c5f6`; PR #1570 exact head `62a548497e79bb1171b074b497f4b905c796dcd4` merged as `356ffe8e`.
- Exact-head validation #42776322203/#42776322272 PASS; post-merge validation #42776664379/#42776664027 PASS. Push diagnostic watchdog #42776663992 SUCCESS and explicitly skipped receipt collection because push events are diagnostics only.
- Receipt collector now filters explicit WF-06/WF-12 path-bearing receipts before the bounded last-eight cap and retains legacy path-less receipts for run-by-ID source verification. WF-07 integration receipts remain valid receiver events but cannot crowd monitored WF-06/WF-12 history.
- Runtime sender/receiver evidence: TCE WF-07 native #42774461163 → TCE WF-12 workflow_run #42774478939 heartbeat sender SUCCESS → Platform receipt #42774493174 SUCCESS. This proves WF-07 receipt delivery only; the post-merge collector still awaits a schedule/manual watchdog run.
- Latest native TCE WF-06 #42744759966 and WF-12 #42741584886 remain stale; WF-12 workflow_run #42774478939 reports WF-06 age 275m and queue wait 0m. Manual WF-06 #42774522833 returns HTTP 503 for all four strict public probes.
- Post-merge Platform push watchdog confirms native gaps: reconcile 26,769s/2,700s; inspection 24,367s/4,500s; recovery 28,020s/2,700s; watchdog 28,068s/2,700s. Push/manual/receipt events do not satisfy native cadence.
- Reconciliation fallback #42774512102 is read-only in effect: `ALLOW_IMAGE_CHANGES=false`, GHCR preflight PASS, Auth runtime Secret verified, shared pull Secret unchanged, TCE pairing PASS, drift=false and apply skipped. Latest K3s snapshot #42774740602 is a manual read-only fallback; it shows TCE/Auth/Keycloak 0/0, Stock historical ARM64 image pull failures, Media/MicroFE core 1/1, OIDC 503 and Media runner still active.
- Stock `deploy.yml` is confirmed app-owned ARM64 image publication, not direct SSH/Compose deployment: native ARM64 runner; full-SHA/version+SHA immutable tags; pre-push tag absence; linux/arm64 and digest-equality verification for scraper/admin/backend. Keep it; no duplicate production apply authority.
- App repos own builds/tests and immutable GHCR publication; Platform owns production manifests, shared pull credentials, provenance/digest promotion, GitOps reconciliation, rollout and health. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` remains read-only.
- No production publication/promotion/apply/rollout/scaling/deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. No cron/freshness-budget or TCE market-scan schedule change.


## 2026-11-10 15:01 ICT — receipt selector runtime verified; native cadence gaps persist

- Platform master is `482b6c92e3898ab9dd3b4c704655627a41d312ac`; TCE `68660a20e5bf3472a122c59d75b49ffce16a2ce9`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open owner-decision PRs: Platform #1314/#544/#541/#539 (draft); Authentication #76 (draft). TCE, Stock and Media have no open PRs.
- PR #1570 merged the receipt-path filter; PR #1571 merged the prior tracker/inventory checkpoint. Native watchdog #42777386082 ran after #1570 and exercised the collector: logs report 3 verified heartbeat receipts each for WF-06 and WF-12, with source metadata verified by run ID. This completes runtime exercise of the merged selector; it does not make stale source runs fresh.
- Latest scheduled reconcile #42778829676 SUCCESS (07:56:31Z): target all, `ALLOW_IMAGE_CHANGES=false`; GHCR read preflight passed for Auth/MicroFE/TCE packages; shared `ghcr-pull` unchanged; TCE tag pairing `prod-v0.1.0-e75e338` passed; drift=false; apply/rollout skipped. Auth/TCE are maintenance 0/0, MicroFE healthy, Keycloak skipped.
- Its 07:56:53Z cluster inventory: K3s node Ready/ARM64; Media and MicroFE core 1/1; Stock Admin and desired Backend ImagePullBackOff; existing Stock Backend/frontend 1/1. No workload mutation occurred.
- Six native inter-arrival gaps remain outside unchanged budgets: Platform reconcile 25,539s/2,700s; inspection 24,367s/4,500s; recovery 26,068s/2,700s; watchdog 25,992s/2,700s; TCE WF-06 23,806s/1,500s; WF-12 25,383s/1,500s. At 08:01:44Z, Platform reconcile/recovery/watchdog current ages are within budget, while inspection and both TCE lanes remain stale by age. New Platform native events at 07:43–07:56Z demonstrate resumed delivery after long gaps, not cadence recovery.
- Watchdog #42777386082 and follow-on observer #42779022182 fail on Platform native inter-arrival gaps. TCE WF-06/WF-12 latest native source runs remain #42744759966/#42741584886 and failed; strict public HTTP 200 checks remain unchanged.
- The read-only `debug/vps-latest.md` snapshot generated 07:21:49Z is 2,395s old at this checkpoint (within 4,500s); disk 56%, ~20 GiB free, ~19 GiB RAM available, restart required, Media runner active/enabled. Last OIDC observation in that snapshot was HTTP 503. No fresh OIDC probe was performed by reconcile #42778829676.
- Stock historical `12d63b4` image manifest remains ARM64-incompatible; do not rotate shared GHCR credentials. No new immutable image publication or digest promotion.
- App repos own builds/tests and immutable GHCR publication. Platform owns manifests, shared GHCR pull credentials, digest/provenance promotion, GitOps reconciliation, rollout and health. `reconcile-vps.yml` remains sole production apply authority; `inspect-vps.yml` is read-only. Preserve TCE WF-07 backup and all useful CI/security/release workflows.
- Owner dependencies: GitHub Actions enqueue/delivery telemetry; TCE/Auth recovery approval and immutable digests; Stock `VNSTOCK_API_KEY` safe preflight and ARM64 release; Media runner unregister/backup/DNS proof; Platform maintenance approval; TCE verified SSH host key.
- No production image publication/promotion, apply, rollout/scaling, deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.


## 2026-11-10 19:01 ICT — current workflow inventory delta

- Current Platform master is `a49cedc3b91ff2506085f9fa8f253e57c686b995`; scheduled inspection PR #1580 changed only `debug/vps-latest.md`, passed exact-head `validate-manifests` #42809513153, and was squash-merged from exact head.
- Current TCE/Stock/Media/Auth master heads: `0f71aa56eb728abbd87907e07739e08684b86724`, `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`, `dcd698699c65ba6e73f6b43838975144777131c3`, `eab85fab32d7c9baef750c1fedbb93deb8c1333f`. Open owner-decision PRs remain Platform #1314/#544/#541/#539 and Auth #76; no PRs are open in TCE, Stock or Media.
- Latest relevant build/test evidence remains TCE WF-01/WF-02/WF-05 #42781396893/#42781396928/#42781396803 PASS, Stock CI #42610360402 PASS, Media CI #42539512417 PASS and Auth CI #42654579277 PASS. TCE public health remains failing: native WF-06 #42799497774 and manual #42799558399 return HTTP 503 from all four strict probes; native WF-12 #42795292155 fails freshness.
- Platform native schedule latest runs: reconcile #42778829676, inspection #42809278936, recovery #42777251549, watchdog #42777386082. TCE native latest: WF-06 #42799497774 and WF-12 #42795292155. At 12:01:42Z, all six inter-arrival gaps exceed the unchanged 2,700/4,500/1,500-second budgets. Current-age exception: only inspection remains within budget.
- Configured cron expressions remain reconcile `7,22,37,52`, inspection `2,32`, recovery `10,25,40,55`, watchdog `12,27,42,57`, TCE WF-06 `*/15`, TCE WF-12 `7,22,37,52` (all hourly minute fields). Do not change TCE market-scan scheduling or count manual/workflow_run/repository_dispatch events as native acceptance.
- Manual Platform reconcile #42809629336 succeeded with `ALLOW_IMAGE_CHANGES=false`: GHCR read preflight PASS; Auth runtime Secret provisioned/verified with values suppressed; shared `ghcr-pull` unchanged; scoped restart helper found no failures in allowlisted MicroFE/TCE workloads; TCE release pairing PASS; GitOps drift=false; manifest apply/image promotion/rollout skipped.
- Fresh read-only K3s snapshot #42809278936 at 11:39:49Z: ARM64 node Ready; disk 56% (~20 GiB free); host restart required; Media and MicroFE core 1/1; TCE/Auth/Keycloak 0/0; Stock Admin/desired Backend ImagePullBackOff on ARM64-incompatible historical `12d63b4`; OIDC 503; Media runner active/listener present; storage preflight clean; GitOps drift clean.
- Preserve app-owned immutable publishers and CI/security/release/backup workflows. Platform remains the only production apply and shared pull-credential authority. No workflow removal was justified.
- Outstanding external gates: GitHub scheduler telemetry and branch ruleset verification (#1497/#1575); TCE/Auth owner-approved recovery and immutable digests (#872); Stock API key/preflight and ARM64 release (#42/#43); Media unregister/backup/DNS proof; Platform maintenance approval and TCE SSH host fingerprint.
- No GHCR publication/promotion, manifest apply, workload rollout/scaling, destructive storage/namespace operation, runner retirement, credential rotation, DNS/database mutation or host reboot. Auth runtime Secret provisioning occurred via the approved reconcile; values suppressed. TCE market-scan schedule unchanged.


## 2026-11-10 20:04 ICT — workflow inventory and readiness delta

- Repository heads: Platform `dbd52d190cb52a580baf55f4a01092439f58295d`; TCE `0f71aa56eb728abbd87907e07739e08684b86724`; Stock `b1b5e177c9983ecdbbec2f2ead2d54f63b90ca61`; Media `dcd698699c65ba6e73f6b43838975144777131c3`; Authentication `eab85fab32d7c9baef750c1fedbb93deb8c1333f`.
- Open PRs remain Platform #1314/#544/#541/#539 (all drafts, stale base SHAs) and Authentication #76 (draft); no open PRs in TCE, Stock or Media. Combined commit-status queries returned no legacy status contexts for these PR heads; no draft was merged.
- Latest app CI evidence remains TCE WF-01/WF-02/WF-05 #42781396893/#42781396928/#42781396803 PASS; Stock CI #42610360402 PASS; Media CI #42539512417 PASS; Auth CI #42654579277 PASS. TCE native WF-06 #42799497774 fails health probes; native WF-12 #42795292155 fails freshness. Manual WF-06 #42799558399 also fails all four endpoint jobs; WF-12 workflow_run #42799530489 succeeds but is not a native schedule.
- Platform latest master validation #42813391103 PASS. Latest watchdog #42809593761 fails native inter-arrival checks. All six schedule current ages and inter-arrival gaps exceed the unchanged budgets at 13:04:19Z. No native run after the six listed in the readiness tracker was observed.
- Latest inspection #42809278936 is 5,078s old (over 4,500s); latest reconcile #42809629336 is 4,922s old (over 2,700s). Treat K3s/GitOps posture as last-known, not live. No rollout authorization.
- Preserve TCE WF-06 strict HTTP 200 probes, WF-12/WF-13 heartbeat/recovery, WF-07 backup, WF-03 publisher, WF-09 manual development utility and WF-10 staging utility. Preserve Stock and Media app-owned immutable publishers and Authentication release/CI. Platform `reconcile-vps.yml` remains the only production apply authority; `inspect-vps.yml` remains read-only.
- Outstanding external gates remain GitHub schedule telemetry and effective branch rulesets (#1497/#1575); TCE/Auth runtime recovery and immutable digests (#872); Stock `VNSTOCK_API_KEY` and ARM64 release (#42/#43); Media remote runner unregister/backup/DNS proof; Platform host maintenance approval; TCE verified SSH fingerprint.
- No workflow removal was justified. No publication, promotion, apply, rollout/scaling, deletion, runner retirement, shared credential rotation, DNS/database/storage mutation or host maintenance occurred. TCE market-scan schedule unchanged.

 
## 2026-11-10 20:16 ICT — merged TCE healthcheck contract and readiness delta

- Platform PR #1582 merged at `18d07f2b09dd02cb923af666b1f135f91ee8d45c`; exact-head validation #42822159770 and post-merge #42822299182 passed.
- TCE PR #1036 merged at `c4602be3b0a7b624bdb9cd41519cfc70a14d92ab`; exact-head WF-05 #42822645162, WF-02 #42822644739, WF-08B #42822644695 and post-merge WF-05 #42822853137/WF-02 #42822853121 all passed.
- New TCE contract in `scripts/validate-wf-06-healthcheck-contract.sh` requires exactly four approved public-smoke endpoints and `expected_status: "200"` for each. Existing WF-05 invokes it unconditionally. No health endpoint, workflow YAML, schedule, heartbeat payload or recovery path changed.
- Latest app CI evidence: TCE post-merge WF-05/WF-02 PASS; Stock #42610360402 PASS; Media #42539512417 PASS; Authentication #42654579277 PASS. TCE public runtime remains unverified/failed: latest native WF-06 #42799497774 and manual #42799558399 fail; latest native WF-12 #42795292155 fails freshness.
- All six native schedule ages and inter-arrival gaps remain outside existing budgets at 13:16:15Z. Manual, workflow_run and repository_dispatch events are excluded.
- Latest K3s inspection #42809278936 (5,194s old) and reconciliation #42809629336 (5,038s old) exceed their freshness budgets; do not authorize rollout from last-known snapshots.
- Preserve app-owned immutable publishers and Platform's single production apply authority. No workflow removal was justified.
- Owner dependencies remain scheduler telemetry/effective branch rulesets (#1497/#1575), TCE/Auth recovery and immutable digests (#872), Stock credential/ARM64 release (#42/#43), Media runner unregister/backup/DNS, Platform maintenance approval and TCE verified SSH fingerprint.
- No publication/promotion/apply/rollout/scaling/deletion, runner retirement, credential rotation, DNS/database/storage mutation or host maintenance. TCE market-scan schedule unchanged.
