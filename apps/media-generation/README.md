# Media Generation — production GitOps

This overlay is intentionally not included in environments/prod until the application repository publishes immutable GHCR images and the runtime secret exists.

Workload split:
- media-generation-api: NestJS HTTP API on port 3000
- media-generation-worker: asynchronous Gemini/Veo generation worker

Both workloads consume the Kubernetes Secret `media-generation-runtime`. Secret values are never stored in this repository.

Expected images:
- ghcr.io/phanthienquoc/fe-algorithm-video/api:<git-sha>
- ghcr.io/phanthienquoc/fe-algorithm-video/worker:<git-sha>
