#!/usr/bin/env bash
# Reconcile trigger: health-gate policy is production-critical.
set -euo pipefail

TARGET_APP="${TARGET_APP:-all}"

case "$TARGET_APP" in
  all)
    namespaces=(tce-prod stock-prod media-prod microfe-platform)
    ;;
  tce-dashboard)
    namespaces=(tce-prod)
    ;;
  stockdividend)
    namespaces=(stock-prod)
    ;;
  media-generation)
    namespaces=(media-prod)
    ;;
  microfe|auth-service|keycloak)
    namespaces=(microfe-platform)
    ;;
  *)
    echo "::error::Unsupported deployment scope: $TARGET_APP" >&2
    exit 1
    ;;
esac

if [[ -n "${HEALTH_GATE_KUBECTL_BIN:-}" ]]; then
  # Test seam for deterministic offline health-gate tests; production uses the allowlisted sudo wrapper.
  kubectl_bin=("$HEALTH_GATE_KUBECTL_BIN")
else
  kubectl_bin=(sudo /usr/local/sbin/platform-kubectl)
fi

failed=0
label_selector=""

# microfe-auth, microfe-shell, and microfe-ws share a namespace but are
# independent deployment lanes. Scope each check to its own app label.
case "$TARGET_APP" in
  auth-service) label_selector="app=microfe-auth" ;;
  keycloak) label_selector="app.kubernetes.io/name=keycloak" ;;
  microfe) label_selector='app in (microfe-shell,microfe-ws)' ;;
  *) ;;
esac

for namespace in "${namespaces[@]}"; do
  echo "Checking workload health in namespace: $namespace"

  # An explicit zero-replica Deployment is a supported maintenance state.
  # Verify the Deployment controller converged and no active pods remain before
  # skipping pod-readiness checks; never treat an unready scale-down as success.
  scale_down_rows="$("${kubectl_bin[@]}" get deployments -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"|"}{.spec.replicas}{"|"}{.status.readyReplicas}{"|"}{.status.updatedReplicas}{"\n"}{end}')"

  case "$TARGET_APP" in
    auth-service)
      scale_down_rows="$(printf '%s\n' "$scale_down_rows" | awk -F'|' '$1 == "microfe-auth"')"
      ;;
    keycloak)
      scale_down_rows="$(printf '%s\n' "$scale_down_rows" | awk -F'|' '$1 == "keycloak"')"
      ;;
    microfe)
      scale_down_rows="$(printf '%s\n' "$scale_down_rows" | awk -F'|' '$1 == "microfe-shell" || $1 == "microfe-ws"')"
      ;;
  esac

  scale_down_count=0
  scale_down_all_zero=1
  scale_down_converged=1
  while IFS='|' read -r deployment desired ready updated; do
    [ -n "$deployment" ] || continue
    scale_down_count=$((scale_down_count + 1))
    desired="${desired:-1}"
    ready="${ready:-0}"
    updated="${updated:-0}"
    if ! [[ "$desired" =~ ^[0-9]+$ && "$ready" =~ ^[0-9]+$ && "$updated" =~ ^[0-9]+$ ]]; then
      echo "::error::Deployment $namespace/$deployment returned invalid replica counts." >&2
      failed=1
      scale_down_converged=0
      scale_down_all_zero=0
      continue
    fi
    if [ "$desired" -gt 0 ]; then
      scale_down_all_zero=0
    elif [ "$ready" -ne 0 ] || [ "$updated" -ne 0 ]; then
      echo "::error::Deployment $namespace/$deployment has desired replicas 0 but has not converged (ready=$ready updated=$updated)." >&2
      failed=1
      scale_down_converged=0
    fi
  done <<< "$scale_down_rows"

  if [ "$scale_down_count" -gt 0 ] && [ "$scale_down_all_zero" -eq 1 ]; then
    if [ "$scale_down_converged" -ne 1 ]; then
      continue
    fi

    if [ -n "$label_selector" ]; then
      scale_down_pods="$("${kubectl_bin[@]}" get pods -n "$namespace" -l "$label_selector" -o jsonpath='{range .items[*]}{.metadata.name}{"|"}{.metadata.deletionTimestamp}{"|"}{.status.phase}{"\n"}{end}')"
    else
      scale_down_pods="$("${kubectl_bin[@]}" get pods -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"|"}{.metadata.deletionTimestamp}{"|"}{.status.phase}{"\n"}{end}')"
    fi

    active_scale_down_pods=0
    while IFS='|' read -r pod deletion_timestamp phase; do
      [ -n "$pod" ] || continue
      [ -n "$deletion_timestamp" ] && continue
      [ "$phase" = "Succeeded" ] && continue
      active_scale_down_pods=$((active_scale_down_pods + 1))
    done <<< "$scale_down_pods"

    if [ "$active_scale_down_pods" -gt 0 ]; then
      echo "::error::Deployment scope $namespace/$TARGET_APP is configured at zero replicas but active pods remain." >&2
      failed=1
    else
      echo "Deployment scope $namespace/$TARGET_APP is intentionally scaled to zero; no active pods remain."
    fi
    continue
  fi

  if [ -n "$label_selector" ]; then
    rows="$("${kubectl_bin[@]}" get pods -n "$namespace" -l "$label_selector" -o jsonpath='{range .items[*]}{.metadata.name}{"|"}{.metadata.deletionTimestamp}{"|"}{.status.phase}{"|"}{range .status.containerStatuses[*]}{.ready}{":"}{.state.waiting.reason}{":"}{.state.terminated.reason}{":"}{.state.waiting.message}{" [container="}{.name}{", image="}{.image}{", imageID="}{.imageID}{", last="}{.lastState.terminated.reason}{"/"}{.lastState.terminated.exitCode}{"] "}{end}{"\n"}{end}')"
  else
    rows="$("${kubectl_bin[@]}" get pods -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"|"}{.metadata.deletionTimestamp}{"|"}{.status.phase}{"|"}{range .status.containerStatuses[*]}{.ready}{":"}{.state.waiting.reason}{":"}{.state.terminated.reason}{":"}{.state.waiting.message}{" [container="}{.name}{", image="}{.image}{", imageID="}{.imageID}{", last="}{.lastState.terminated.reason}{"/"}{.lastState.terminated.exitCode}{"] "}{end}{"\n"}{end}')"
  fi

  if [ -z "$rows" ]; then
    echo "::error::No pods found in namespace $namespace for target $TARGET_APP." >&2
    failed=1
    continue
  fi

  active_pods=0
  while IFS='|' read -r pod deletion_timestamp phase containers; do
    [ -n "$pod" ] || continue

    if [ -n "$deletion_timestamp" ]; then
      echo "Skipping terminating pod $namespace/$pod."
      continue
    fi

    if [ "$phase" = "Succeeded" ]; then
      continue
    fi

    active_pods=$((active_pods + 1))

    if [ "$phase" != "Running" ]; then
      echo "::error::Pod $namespace/$pod is not Running (phase=$phase); container diagnostics: $containers" >&2
      failed=1
      continue
    fi

    if printf '%s' "$containers" | grep -Eq '(^| )false:'; then
      echo "::error::Pod $namespace/$pod has a non-ready container: $containers" >&2
      failed=1
    fi

    if printf '%s' "$containers" | grep -Eq '(ImagePullBackOff|ErrImagePull|CrashLoopBackOff|CreateContainerConfigError|CreateContainerError|RunContainerError)'; then
      echo "::error::Pod $namespace/$pod has a failed container state: $containers" >&2
      failed=1
    fi
  done <<< "$rows"

  if [ "$active_pods" -eq 0 ]; then
    echo "::error::No non-terminating workload pods found in namespace $namespace for target $TARGET_APP." >&2
    failed=1
  fi

  # Pod label selectors cannot be reused for Deployment objects unless the
  # Deployment metadata itself carries those labels. Auth/MicroFE manifests label
  # pod templates but not Deployment metadata, so list deployments and scope by
  # canonical deployment name instead.
  deployment_rows="$("${kubectl_bin[@]}" get deployments -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"|"}{.spec.replicas}{"|"}{.status.readyReplicas}{"|"}{.status.updatedReplicas}{"\n"}{end}')"

  case "$TARGET_APP" in
    auth-service)
      deployment_rows="$(printf '%s\n' "$deployment_rows" | awk -F'|' '$1 == "microfe-auth"')"
      ;;
    keycloak)
      deployment_rows="$(printf '%s\n' "$deployment_rows" | awk -F'|' '$1 == "keycloak"')"
      ;;
    microfe)
      deployment_rows="$(printf '%s\n' "$deployment_rows" | awk -F'|' '$1 == "microfe-shell" || $1 == "microfe-ws"')"
      ;;
  esac

  if [ -z "$deployment_rows" ]; then
    echo "::error::No deployments found in namespace $namespace for target $TARGET_APP." >&2
    failed=1
    continue
  fi

  deployment_count=0
  while IFS='|' read -r deployment desired ready updated; do
    [ -n "$deployment" ] || continue
    deployment_count=$((deployment_count + 1))
    desired="${desired:-1}"
    ready="${ready:-0}"
    updated="${updated:-0}"

    if ! [[ "$desired" =~ ^[0-9]+$ && "$ready" =~ ^[0-9]+$ && "$updated" =~ ^[0-9]+$ ]]; then
      echo "::error::Deployment $namespace/$deployment returned invalid replica counts." >&2
      failed=1
      continue
    fi

    if [ "$desired" -gt 0 ] && { [ "$ready" -lt "$desired" ] || [ "$updated" -lt "$desired" ]; }; then
      echo "::error::Deployment $namespace/$deployment is not fully ready (desired=$desired ready=$ready updated=$updated)." >&2
      failed=1
    fi
  done <<< "$deployment_rows"

  if [ "$deployment_count" -eq 0 ]; then
    echo "::error::No deployment records found in namespace $namespace for target $TARGET_APP." >&2
    failed=1
  fi
done

if [ "$failed" -ne 0 ] && { [ "$TARGET_APP" = "media-generation" ] || [ "$TARGET_APP" = "all" ]; }; then
  echo "Media workload diagnostic (read-only):"
  sudo /usr/local/sbin/platform-kubectl describe-media || true
fi

if [ "$failed" -ne 0 ]; then
  echo "Workload health gate failed; refusing to report reconciliation as healthy." >&2
  exit 1
fi

echo "Targeted workload health gate passed."
