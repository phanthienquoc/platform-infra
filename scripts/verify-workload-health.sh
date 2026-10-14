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

kubectl_bin=(sudo /usr/local/sbin/platform-kubectl)
failed=0
label_selector=""

# microfe-auth, microfe-shell, and microfe-ws share a namespace but are
# independent deployment lanes. Scope each check to its own app label.
case "$TARGET_APP" in
  auth-service) label_selector="app=microfe-auth" ;;
  keycloak) label_selector="app.kubernetes.io/name=keycloak" ;;
  keycloak) label_selector="app.kubernetes.io/name=keycloak" ;;
  microfe) label_selector='app in (microfe-shell,microfe-ws)' ;;
  *) ;;
esac

for namespace in "${namespaces[@]}"; do
  echo "Checking workload health in namespace: $namespace"

  if [ -n "$label_selector" ]; then
    rows="$("${kubectl_bin[@]}" get pods -n "$namespace" -l "$label_selector" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.deletionTimestamp}{"\t"}{.status.phase}{"\t"}{range .status.containerStatuses[*]}{.ready}{":"}{.state.waiting.reason}{":"}{.state.terminated.reason}{" "}{end}{"\n"}{end}')"
  else
    rows="$("${kubectl_bin[@]}" get pods -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.deletionTimestamp}{"\t"}{.status.phase}{"\t"}{range .status.containerStatuses[*]}{.ready}{":"}{.state.waiting.reason}{":"}{.state.terminated.reason}{" "}{end}{"\n"}{end}')"
  fi

  if [ -z "$rows" ]; then
    echo "::error::No pods found in namespace $namespace for target $TARGET_APP." >&2
    failed=1
    continue
  fi

  while IFS=$'\t' read -r pod deletion_timestamp phase containers; do
    [ -n "$pod" ] || continue

    if [ -n "$deletion_timestamp" ]; then
      echo "Skipping terminating pod $namespace/$pod."
      continue
    fi

    if [ "$phase" = "Succeeded" ]; then
      continue
    fi

    if [ "$phase" != "Running" ]; then
      echo "::error::Pod $namespace/$pod is not Running (phase=$phase)." >&2
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
