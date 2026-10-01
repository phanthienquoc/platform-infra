#!/usr/bin/env bash
# Reconcile trigger: health-gate policy is production-critical.
set -euo pipefail

TARGET_APP="${TARGET_APP:-all}"

case "$TARGET_APP" in
  all)
    namespaces=(tce-prod stock-prod media-prod)
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
  *)
    echo "::error::Unsupported deployment scope: $TARGET_APP" >&2
    exit 1
    ;;
esac

kubectl_bin=(sudo /usr/local/sbin/platform-kubectl)
failed=0

for namespace in "${namespaces[@]}"; do
  echo "Checking workload health in namespace: $namespace"

  deployment_rows="$("${kubectl_bin[@]}" get deployments -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\\t"}{.spec.replicas}{"\\t"}{.status.updatedReplicas}{"\\t"}{.status.availableReplicas}{"\\t"}{.metadata.generation}{"\\t"}{.status.observedGeneration}{"\\n"}{end}')"
  while IFS="$("${kubectl_bin[@]}" get pods -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.deletionTimestamp}{"\t"}{.status.phase}{"\t"}{range .status.containerStatuses[*]}{.ready}{":"}{.state.waiting.reason}{":"}{.state.terminated.reason}{" "}{end}{"\n"}{end}')"

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
  sudo /usr/local/sbin/platform-kubectl logs deployment/media-generation-frontend -n media-prod --tail=200 || true
fi

if [ "$failed" -ne 0 ]; then
  echo "Workload health gate failed; refusing to report reconciliation as healthy." >&2
  exit 1
fi

echo "Targeted workload health gate passed."
\t' read -r deployment desired updated available generation observed; do
    [ -n "$deployment" ] || continue
    desired="${desired:-0}"
    updated="${updated:-0}"
    available="${available:-0}"
    observed="${observed:-0}"
    if [ "$desired" -gt 0 ] && { [ "$updated" -ne "$desired" ] || [ "$available" -ne "$desired" ] || [ "$observed" -ne "$generation" ]; }; then
      echo "::error::Deployment $namespace/$deployment is not fully available (desired=$desired updated=$updated available=$available generation=$generation observed=$observed)." >&2
      failed=1
    fi
  done <<< "$deployment_rows"

  rows="$("${kubectl_bin[@]}" get pods -n "$namespace" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.deletionTimestamp}{"\t"}{.status.phase}{"\t"}{range .status.containerStatuses[*]}{.ready}{":"}{.state.waiting.reason}{":"}{.state.terminated.reason}{" "}{end}{"\n"}{end}')"

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
