#!/usr/bin/env bash
set -euo pipefail
NS=${1:?namespace}
IMAGE=${2:?immutable image}
JOB=migration-$(date -u +%Y%m%d%H%M%S)
kubectl -n "$NS" create job "$JOB" --image="$IMAGE" -- /bin/sh -c 'echo app-specific migration command required'
kubectl -n "$NS" wait --for=condition=complete job/"$JOB" --timeout=15m
kubectl -n "$NS" logs job/"$JOB"
