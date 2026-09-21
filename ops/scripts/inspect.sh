#!/usr/bin/env bash
set -euo pipefail
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get svc -A
kubectl get ingress -A
kubectl get pvc -A
kubectl get jobs,cronjobs -A
kubectl get certificates,issuers,clusterissuers -A 2>/dev/null || true
