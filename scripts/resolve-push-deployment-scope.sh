#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "::error::$*" >&2
  return 1
}

resolve_scope() {
  local keycloak_changed=0
  local cluster_wide=0
  local replicas
  local path
  local scope
  local -A scopes=()

  for path in "$@"; do
    [[ -n "$path" ]] || continue
    case "$path" in
      apps/tce-vps-control-mcp/*)
        # Optional diagnostics-only MCP is not a production workload scope.
        ;;
      apps/**/*.md|apps/**/docs/*)
        # App documentation is not a production workload change, even when a
        # manifest change in the same commit causes reconciliation to run.
        ;;
      platform/microfe/*|apps/microfe/*)
        scopes[microfe]=1
        ;;
      platform/auth-service/*|apps/auth-service/*)
        scopes[auth-service]=1
        ;;
      apps/tce-dashboard/*)
        scopes[tce-dashboard]=1
        ;;
      apps/stockdividend/*|apps/media-generation/*)
        # Retired trees may only be removed in a cluster-wide GitOps change.
        cluster_wide=1
        ;;
      platform/keycloak/*.md)
        # Operator documentation beside Keycloak manifests is not a workload change.
        ;;
      platform/keycloak/*|apps/keycloak/*)
        keycloak_changed=1
        ;;
      README.md|.gitignore|environments/prod/README.md|.github/skills/*|ops/runbooks/*|scripts/inspect-vps.sh)
        # Repository/runbook/skill documentation and read-only inspection code
        # must not become an automatic production deployment scope.
        ;;
      environments/prod/*|platform/cert-manager/*|platform/k3s-debug-logs/*|scripts/reconcile-vps.sh|scripts/prepare-cert-manager-manifest.sh|scripts/guard-reconcile-images.sh|scripts/validate-ghcr-pull-access.sh|scripts/verify-workload-health.sh)
        cluster_wide=1
        ;;
      .github/workflows/*|scripts/resolve-push-deployment-scope.sh|scripts/bootstrap-runner.sh|scripts/bootstrap-media-runner.sh|scripts/decommission-stock-media-namespaces.sh|scripts/validate-*.py|scripts/validate-*.sh|scripts/verify-reconcile-lane-queue.py|scripts/verify-media-publisher-run.sh|scripts/verify-stockdividend-publisher-run.sh|scripts/verify-stockdividend-gitops-digests.py|scripts/tests/*|docs/*|debug/vps-latest.md)
        # CI, documentation, inspection snapshots and manual-only/retired helpers
        # do not introduce a production workload scope of their own. Keep the
        # shared GHCR access validator above cluster-wide because it gates apply.
        ;;
      *)
        fail "Unclassified production-trigger path '$path'; refusing broad push reconciliation."
        return 1
        ;;
    esac
  done

  if [[ "$keycloak_changed" -eq 1 ]]; then
    if [[ "$cluster_wide" -eq 1 || "${#scopes[@]}" -gt 0 ]]; then
      fail "Keycloak changes must be isolated from other application or cluster-wide changes."
      return 1
    fi
    replicas="${KEYCLOAK_REPLICAS_OVERRIDE:-}"
    if [[ -z "$replicas" ]]; then
      replicas="$(awk '
        $0 == "spec:" { in_spec = 1; next }
        in_spec && /^[^[:space:]]/ { in_spec = 0 }
        in_spec && /^  replicas:/ { print $2; exit }
      ' platform/keycloak/deployment.yaml)"
    fi
    case "$replicas" in
      0) echo "auth-shutdown" ;;
      1) echo "keycloak" ;;
      *) fail "Keycloak-only push requires replicas 0 or 1, got ${replicas:-missing}"; return 1 ;;
    esac
    return 0
  fi

  if [[ "$cluster_wide" -eq 1 ]]; then
    echo "all"
    return 0
  fi

  if [[ "${#scopes[@]}" -eq 0 ]]; then
    fail "No application scope could be resolved from the changed paths."
    return 1
  fi

  if [[ "${#scopes[@]}" -gt 1 ]]; then
    echo "all"
    return 0
  fi

  for scope in "${!scopes[@]}"; do
    echo "$scope"
    return 0
  done
}

assert_scope() {
  local expected="$1"
  shift
  local actual
  actual="$(resolve_scope "$@")"
  if [[ "$actual" != "$expected" ]]; then
    fail "Expected scope '$expected' for paths '$*', got '$actual'."
    return 1
  fi
}

assert_failure() {
  if resolve_scope "$@" >/dev/null 2>&1; then
    fail "Expected push scope resolution to fail for paths '$*'."
    return 1
  fi
}

self_test() {
  assert_scope microfe platform/microfe/kustomization.yaml
  assert_scope auth-service platform/auth-service/deployment.yaml
  assert_scope tce-dashboard apps/tce-dashboard/overlays/prod/kustomization.yaml
  assert_failure apps/tce-vps-control-mcp/package.json
  assert_scope tce-dashboard apps/tce-dashboard/overlays/prod/kustomization.yaml apps/tce-vps-control-mcp/package.json
  assert_failure .github/workflows/validate-manifests.yml scripts/validate-workflow-contracts.py docs/cross-repo-deployment-tracker.md debug/vps-latest.md
  assert_scope all environments/prod/kustomization.yaml
  assert_scope all apps/stockdividend/base/kustomization.yaml environments/prod/kustomization.yaml
  assert_scope all apps/media-generation/base/kustomization.yaml environments/prod/kustomization.yaml
  assert_scope all scripts/verify-workload-health.sh
  assert_failure scripts/resolve-push-deployment-scope.sh
  assert_scope all platform/cert-manager/kustomization.yaml scripts/prepare-cert-manager-manifest.sh
  assert_failure README.md .gitignore environments/prod/README.md .github/skills/manifest-validation/SKILL.md ops/runbooks/maintenance.md scripts/inspect-vps.sh
  assert_failure platform/keycloak/README.md
  assert_scope all scripts/verify-workload-health.sh scripts/bootstrap-runner.sh scripts/validate-recovery-readiness.sh
  assert_failure scripts/bootstrap-runner.sh scripts/validate-recovery-readiness.sh
  # Manual-only and retired helper changes must never trigger an automatic
  # production apply by themselves. When paired with the retirement manifest
  # deletion, the app-tree/environment paths still force a cluster-wide pass.
  assert_failure scripts/bootstrap-media-runner.sh scripts/decommission-stock-media-namespaces.sh scripts/validate-metrics-hpa.sh scripts/validate-metrics.sh scripts/validate-network-boundaries.sh scripts/verify-reconcile-lane-queue.py scripts/verify-media-publisher-run.sh scripts/verify-stockdividend-publisher-run.sh scripts/verify-stockdividend-gitops-digests.py
  assert_scope all apps/stockdividend/README.md apps/media-generation/README.md environments/prod/kustomization.yaml scripts/bootstrap-media-runner.sh scripts/decommission-stock-media-namespaces.sh scripts/resolve-push-deployment-scope.sh scripts/validate-metrics-hpa.sh scripts/validate-metrics.sh scripts/validate-network-boundaries.sh scripts/verify-reconcile-lane-queue.py scripts/verify-media-publisher-run.sh scripts/verify-stockdividend-publisher-run.sh scripts/verify-stockdividend-gitops-digests.py
  # Full path fixture from the merged Stock/Media retirement PR: deleted app
  # trees force cluster-wide scope, while retired helpers stay non-deploying.
  assert_scope all apps/stockdividend/base/kustomization.yaml apps/media-generation/base/kustomization.yaml environments/prod/kustomization.yaml scripts/bootstrap-media-runner.sh scripts/decommission-stock-media-namespaces.sh scripts/resolve-push-deployment-scope.sh scripts/validate-metrics-hpa.sh scripts/validate-metrics.sh scripts/validate-network-boundaries.sh scripts/verify-reconcile-lane-queue.py scripts/verify-media-publisher-run.sh scripts/verify-stockdividend-publisher-run.sh scripts/verify-stockdividend-gitops-digests.py scripts/validate-ghcr-pull-access.sh scripts/verify-workload-health.sh
  local keycloak_zero keycloak_one
  keycloak_zero="$(KEYCLOAK_REPLICAS_OVERRIDE=0 resolve_scope platform/keycloak/deployment.yaml)"
  keycloak_one="$(KEYCLOAK_REPLICAS_OVERRIDE=1 resolve_scope platform/keycloak/deployment.yaml)"
  [[ "$keycloak_zero" == "auth-shutdown" ]] || { fail "Keycloak replicas=0 must resolve to auth-shutdown."; return 1; }
  [[ "$keycloak_one" == "keycloak" ]] || { fail "Keycloak replicas=1 must resolve to keycloak."; return 1; }
  assert_failure platform/keycloak/deployment.yaml platform/microfe/kustomization.yaml
  assert_failure apps/unknown-service/overlays/prod/kustomization.yaml
  echo "Push deployment scope contract tests passed."
}

if [[ "${1:-}" == "--self-test" ]]; then
  self_test
  exit 0
fi

changed_paths=()
while IFS= read -r path; do
  [[ -n "$path" ]] && changed_paths+=("$path")
done

resolve_scope "${changed_paths[@]}"
