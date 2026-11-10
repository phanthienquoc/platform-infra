# GitHub Actions Schedule Delivery Recovery

**Purpose:** operator procedure for restoring and proving native GitHub Actions scheduled delivery when a workflow's `event=schedule` history becomes stale.

**Status:** read-only diagnosis first. Enabling a workflow is an Actions administration change and must be performed only after confirming that the workflow is intended to remain scheduled. This runbook does not authorize production deployment, image publication, workload activation, host maintenance, or destructive changes.

## 1. Evidence rules

A run counts as native schedule evidence only when all of these are true:

- `event=schedule`
- Exact expected `path`
- `head_branch=master`
- Full 40-character `head_sha`
- Original attempt `run_attempt=1`
- Valid, monotonically increasing `created_at`

Do not count `workflow_dispatch`, `workflow_run`, `repository_dispatch`, push, rerun attempts, or a successful fallback as native schedule events. For TCE cross-repository observation only, a successful Platform `recover-stale-ops` heartbeat receipt may locate the source run; Platform re-fetches that exact TCE run ID and counts only the verified source object with `event=schedule`, the exact workflow path, `master`, full SHA, and attempt 1. The `repository_dispatch` receipt itself is transport metadata, not native schedule evidence. A manual watchdog run is diagnostic only.

Use GitHub Actions API timestamps for comparisons. Do not infer queue delay from the local runner clock.

## 2. Current scheduled workflow contract

The values below are the checked-in contracts. Do not change cron expressions or freshness budgets as a workaround for missing delivery.

### Platform Infra

| Workflow path | Cron (UTC) | Freshness / inter-arrival budget | Authority |
|---|---|---:|---|
| `.github/workflows/inspect-vps.yml` | `2,32 * * * *` | 75 minutes | Read-only VPS/K3s inspection |
| `.github/workflows/reconcile-vps.yml` | `7,22,37,52 * * * *` | 45 minutes | Sole production GitOps apply authority |
| `.github/workflows/recover-stale-ops.yml` | `10,25,40,55 * * * *` | 45 minutes | Validated recovery and fallback dispatch |
| `.github/workflows/reconcile-schedule-watchdog.yml` | `12,27,42,57 * * * *` | 45 minutes | Read-only schedule/queue enforcement |

### Cross-repo observations

| Repository | Workflow path | Cron (UTC) | Budget | Classification |
|---|---|---|---:|---|
| TCE Dashboard | `.github/workflows/wf-06-tce-healthcheck.yml` | `*/15 * * * *` | 25 minutes | Strict public HTTP 200 health contract |
| TCE Dashboard | `.github/workflows/wf-12-tce-healthcheck-schedule-watchdog.yml` | `7,22,37,52 * * * *` | 25 minutes | Schedule-delivery watchdog and Platform heartbeat |
| StockDividend | `.github/workflows/run_scraper.yml` | `0 1 * * 0,6` | Weekend event; observe delayed delivery window | App-owned data ingestion, not deployment |

TCE cross-repo observations are advisory to Platform reconciliation. The watchdog reads successful Platform-owned heartbeat receipt runs and verifies the source TCE run by ID; it does not need a cross-repository Actions-read PAT. A path-tagged receipt history needs two distinct source runs before an inter-arrival gap can be measured. Keep the TCE market-scan schedule unchanged; it is outside this recovery procedure.

## 3. Inspect workflow state before changing anything

Run with an authenticated GitHub CLI session and a token that can read Actions metadata:

```bash
gh auth status
REPO=phanthienquoc/platform-infra

for workflow in \
  reconcile-vps.yml \
  inspect-vps.yml \
  recover-stale-ops.yml \
  reconcile-schedule-watchdog.yml
do
  gh api "repos/$REPO/actions/workflows/$workflow" \
    --jq '[.id, .name, .path, .state] | @tsv'
done
```

Repeat for the two TCE workflows and Stock scraper:

```bash
REPO=phanthienquoc/TCE-dashboard
for workflow in wf-06-tce-healthcheck.yml wf-12-tce-healthcheck-schedule-watchdog.yml; do
  gh api "repos/$REPO/actions/workflows/$workflow" \
    --jq '[.id, .name, .path, .state] | @tsv'
done

REPO=phanthienquoc/stockdividend
gh api "repos/$REPO/actions/workflows/run_scraper.yml" \
  --jq '[.id, .name, .path, .state] | @tsv'
```

Interpret `state` as follows:

- `active`: continue with schedule-history and repository/org policy checks.
- `disabled_manually`: identify who disabled it and why; obtain owner approval before re-enabling.
- `disabled_inactivity`: confirm the workflow is still required, then obtain owner approval to re-enable it.
- Missing workflow, 404, or API error: stop and investigate repository/path/permissions. Do not create a replacement workflow or alter cron to mask the problem.

## 4. Re-enable only an approved disabled workflow

This is an Actions administration mutation. It requires Actions write permission and explicit owner approval. Use the workflow ID returned by the inspection above, not a guessed ID:

```bash
REPO=phanthienquoc/platform-infra
WORKFLOW_ID=<workflow_id>
gh api --method PUT "repos/$REPO/actions/workflows/$WORKFLOW_ID/enable"
gh api "repos/$REPO/actions/workflows/$WORKFLOW_ID" \
  --jq '[.id, .path, .state] | @tsv'
```

Repeat only for workflows confirmed to be intentionally scheduled. Do not enable retired, experimental, or intentionally disabled workflows. Do not change repository/org Actions policies without the relevant administrator's approval.

If state is already `active` but native events are absent, inspect repository and organization Actions policies, default branch, workflow file presence on `master`, runner availability/labels, and GitHub Actions service health. Escalate persistent scheduler delivery failures to the repository/org administrator or GitHub Support. Do not solve this by increasing cron frequency or changing freshness budgets.

## 5. Read-only diagnostics

List the latest native schedule events for one workflow:

```bash
REPO=phanthienquoc/platform-infra
WORKFLOW=reconcile-vps.yml
gh api "repos/$REPO/actions/workflows/$WORKFLOW/runs?event=schedule&branch=master&per_page=100" \
  --jq '.workflow_runs | sort_by(.created_at) | reverse | .[:5][] |
    [.id, .event, .path, .head_branch, .head_sha, .run_attempt,
     .created_at, .status, .conclusion, .html_url] | @tsv'
```

Run the existing read-only watchdog manually to inspect current native history and queue telemetry:

```bash
gh workflow run reconcile-schedule-watchdog.yml \
  --repo phanthienquoc/platform-infra --ref master
```

The manual run may fail because native history is stale; that is expected diagnostic evidence. It does not count as a scheduled run and must not be reported as schedule recovery. The watchdog reads Actions API metadata and does not apply manifests or change production workloads.

For a standalone inter-arrival check, save the API response for the target workflow and use an API-derived reference timestamp:

```bash
REPO=phanthienquoc/platform-infra
WORKFLOW=reconcile-vps.yml
gh api "repos/$REPO/actions/workflows/$WORKFLOW/runs?event=schedule&branch=master&per_page=100" \
  > /tmp/native-schedule-runs.json

WATCHDOG_ID="$(gh api "repos/$REPO/actions/runs?branch=master&per_page=100" \
  --jq '[.workflow_runs[] |
    select(.path == ".github/workflows/reconcile-schedule-watchdog.yml")] |
    sort_by(.created_at) | last | .id')"
REFERENCE_AT="$(gh api "repos/$REPO/actions/runs/$WATCHDOG_ID" --jq '.created_at')"
REFERENCE_EPOCH="$(date -u -d "$REFERENCE_AT" +%s)"

python3 scripts/verify-native-schedule-gap.py \
  --runs-file /tmp/native-schedule-runs.json \
  --workflow-path .github/workflows/reconcile-vps.yml \
  --branch master \
  --reference-epoch "$REFERENCE_EPOCH" \
  --max-gap-minutes 45
```

Repeat with the exact workflow path and budget from the tables above. The verifier requires at least two original native runs and rejects dispatch substitution, wrong branch/path, short SHA, rerun-only history, invalid timestamps, API errors, and gaps over budget. The watchdog separately enforces latest-run freshness and runner queue budgets.

## 6. Recovery acceptance criteria

Do not close the schedule-delivery incident until:

1. Every required workflow reports `state=active`.
2. Two consecutive original `event=schedule` runs exist for each required Platform workflow.
3. Each run has the exact path, `master`, full SHA, and attempt 1.
4. Inter-arrival gaps satisfy the existing 45/75-minute Platform budgets.
5. Latest-run freshness and runner queue checks pass.
6. A subsequent native watchdog run completes successfully against the recovered history.
7. TCE WF-06/WF-12 observations are recorded separately; they do not replace Platform-native evidence.
8. The next Stock weekend scraper run passes the `VNSTOCK_API_KEY` presence and authenticated non-guest entitlement checks. Do not manually dispatch the scraper merely to test the secret because it performs real ingestion/MongoDB/Telegram side effects.

## 7. Production safety boundaries

- `reconcile-vps.yml` remains the only production GitOps apply authority.
- `inspect-vps.yml` and `reconcile-schedule-watchdog.yml` are read-only.
- Recovery may dispatch only the existing, validated reconciliation/inspection workflows under their current contracts.
- Never use a schedule diagnostic to publish/promote images, apply manifests, scale TCE/Auth, delete namespaces/PVCs, retire runners, mutate DNS/database/object storage, or reboot/upgrade the host.
- Keep strict HTTP 200 health checks and existing freshness budgets.
- Preserve useful CI, security, backup, manual, release, and scheduled workflows.
- Do not add a second SSH/Compose/Kubernetes deployment authority.
- TCE market-scan schedule unchanged.

## 8. Escalation record

For every attempted recovery, record the UTC timestamp, repository, workflow path, workflow state, exact native run IDs/attempts/SHAs, inter-arrival calculation, queue result, and the approving administrator. Never record secret values or infer schedule success from a dispatch/fallback.
