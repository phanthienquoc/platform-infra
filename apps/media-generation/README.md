# Media Generation

Production deployment for the media-generation API and worker.

- Namespace: media-prod
- Image: ghcr.io/phanthienquoc/media-generation
- HTTP service: 3000
- Worker is enabled in the same pod so queued Veo jobs are processed.
- Runtime credentials are provided by the media-generation-secrets Kubernetes Secret; no secret values are committed here.
