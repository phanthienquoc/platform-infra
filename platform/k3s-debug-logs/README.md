# K3s Debug Snapshots

This component keeps a rolling black-box record of the K3s cluster for troubleshooting production incidents.

## Collection

- Snapshot: every 15 minutes.
- Retention: cleanup runs daily at 00:15 Asia/Ho_Chi_Minh and removes snapshots older than 24 hours.
- Storage: \`k3s-debug/k3s-debug-logs\` PVC (1Gi), not hostPath.
- Snapshot path: \`/debug/k3s-YYYYMMDD-HHMMSS.log\`.

## What is captured

Each snapshot is intentionally focused on operational signals:

1. Collection timestamp, Kubernetes version and cluster-info.
2. Node status, conditions, capacity and \`kubectl top nodes\`.
3. All pods with phase, restart counts and images.
4. Deployments/statefulsets/daemonsets and workload-wide status.
5. Services, Endpoints and EndpointSlices.
6. Ingresses.
7. PV/PVC state.
8. Jobs/CronJobs.
9. Latest 500 cluster events.
10. cert-manager certificates, CertificateRequests, Issuers and ClusterIssuers.
11. \`kubectl top pods -A\`.
12. \`describe pod\` for non-running or restarted pods, including probe failures and recent events.
13. Deployment rollout status.
14. Last 100 lines of current container logs.
15. Last 100 lines of previous container logs for restarted pods.

The collector does **not** dump full Pod/Deployment/Job YAML or Secret objects, to avoid accidentally persisting sensitive environment/config values.

## First commands during an incident

\`\`\`bash
kubectl -n k3s-debug get cronjob,pods,jobs
kubectl -n k3s-debug exec <snapshot-pod> -- sh -c 'ls -lh /debug | tail -20'
kubectl -n k3s-debug exec <snapshot-pod> -- sh -c 'tail -n 300 /debug/k3s-YYYYMMDD-HHMMSS.log'
\`\`\`

To inspect a particular failure:

\`\`\`bash
kubectl -n k3s-debug exec <snapshot-pod> -- sh -c 'grep -nE "CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Readiness|Liveness|Startup|Failed|Back-off|OOMKilled|unhealthy|no endpoints|certificate" /debug/k3s-YYYYMMDD-HHMMSS.log'
\`\`\`

For a pod restart, inspect both:

- \`CONTAINER LOGS (CURRENT, LAST 100)\`
- \`CONTAINER LOGS (PREVIOUS, RESTARTED CONTAINERS)\`

For an ingress/auth issue, inspect:

- \`SERVICES / ENDPOINTS\`
- \`INGRESSES\`
- \`EVENTS (LATEST 500)\`
- affected pod \`describe\`
- affected pod current/previous logs

For a deployment rollout issue, inspect:

- \`DEPLOYMENTS\`
- \`NON-HEALTHY WORKLOADS: ROLLOUT STATUS\`
- pod restart/image inventory
- events

## Debug workflow

1. Pick the snapshot immediately before the incident.
2. Search the error signature first.
3. Check Events and affected Pod \`describe\`.
4. Check image/restart/probe state.
5. Check Service -> Endpoint -> Ingress chain when traffic is failing.
6. Compare with the next snapshot to see whether the condition recovered, worsened, or rolled to a new pod.
7. Only then change manifests/workflows.

This snapshot is the default first evidence source for K3s production debugging.
