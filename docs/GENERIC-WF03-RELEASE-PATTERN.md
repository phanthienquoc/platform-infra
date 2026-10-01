# Generic Production Release Pattern (WF-03)

> Reusable production release pattern for application repositories.
> Reference implementations: TCE and Media Generation.

## 1. Architecture

The application repository owns source, tests, frontend/backend builds, immutable release artifacts, GHCR publication, notifications, and dispatching the release to platform-infra.

platform-infra owns GitOps manifests, image promotion, paired-component coordination, production reconciliation, and Kubernetes rollout/health verification.

Flow:

```text
App repo
  |
  |- Verify FE/BE
  |- Resolve immutable release tag
  |- Build native ARM64 images
  |- Verify architecture
  |- Export + checksum exact images
  |- Publish exact images to GHCR
  `- repository_dispatch: <app>-release-requested
                         |
                         v
                 platform-infra
                         |
                 |- fan-out FE/BE
                 |- promote GitOps images
                 |- wait for both tags
                 `- gitops-promoted-ready
                         |
                         v
                    K3s / Production
```

## 2. Immutable release tag

Use one release identifier for the entire application release:

`text
prod-v<semver>-<git-sha>
```

Example: prod-v0.2.0-45fa9b4

Rules:
- semver comes from the application package/version.
- git-sha is the source commit SHA, normally shortened to 7 characters.
- Frontend and backend must use the same release tag.
- Never promote latest.
- Do not use independently generated FE/BE tags for one production release.

## 3. CI workflow stages

### Stage A — Notification
Send the production start notification if the repository uses the platform Telegram convention.

### Stage B — Detect release
Resolve prod-v<package-version>-<short-sha> and expose it as a job output.

### Stage C — Verify application
Run backend install/test/build and frontend install/build independently. Do not publish images when verification fails.

### Stage D — Build native ARM64 images
Use an ARM64 runner such as ubuntu-24.04-arm. Build each runtime image independently.

Example image contract:

`text
frontend -> ghcr.io/<owner>/<app>-frontend:<RELEASE_TAG>
backend  -> ghcr.io/<owner>/<app>-backend:<RELEASE_TAG>
```

### Stage E — Verify image architecture
Inspect each production image and require linux/arm64.

### Stage F — Export and checksum
For each image: docker save, calculate SHA-256, and upload the image archive plus checksum as GitHub Actions artifacts.

The publication job must validate the checksum before loading/publishing.

### Stage G — Publish exact images
Download artifacts, validate checksums, load the exact images, authenticate to GHCR, and publish the exact immutable release tags. Never rebuild during publication.

### Stage H — Dispatch platform release
After all required images are published, dispatch:

`text
event_type = <app>-release-requested
```

Payload:

```json
{
  "app": "<app-name>",
  "release": "prod-v<semver>-<git-sha>"
}
```

## 4. platform-infra release coordinator

For multi-component applications, treat the release as one paired release.

When <app>-release-requested arrives:
1. Validate app name.
2. Validate release tag format.
3. Fan out image-published events for every required component.
4. Pass the same release tag to every component.
5. Let generic GitOps promotion create/update the promotion PR.
6. Wait until every required GitOps image tag equals the requested release.
7. Emit exactly one gitops-promoted-ready event.

Required invariant:

```text
frontend GitOps tag == RELEASE
AND
backend GitOps tag == RELEASE
```

Never reconcile production from a partially promoted release.

## 5. Generic image promotion

The generic promotion job should:
- validate the target GHCR image exists
- update the production Kustomization
- create the GitOps PR
- validate required checks
- squash-merge the promotion PR
- leave the immutable tag in master

Example:

```yaml
images:
  - name: ghcr.io/<owner>/<app>-frontend
    newTag: prod-v0.2.0-45fa9b4
  - name: ghcr.io/<owner>/<app>-backend
    newTag: prod-v0.2.0-45fa9b4
```

## 6. Reconciliation

After all required image tags converge:

```text
gitops-promoted-ready
        |
        v
reconcile-vps
        |
        |- apply GitOps manifests
        |- rollout status
        |- workload health
        `- final verification
```

Production reconciliation should be app-aware. A failure in one application must not incorrectly mark unrelated applications as failed.

## 7. Kubernetes runtime contract

For each application define namespace, Deployment(s), Service(s), Ingress, resources, probes, and immutable image references.

If Traefik is the cluster ingress controller, application containers should expose their native runtime port. For Next.js standalone, use Traefik -> Service :3000 -> Next.js standalone Node :3000. Do not introduce Nginx unless required by the application.

## 8. Security and secrets

- Never commit production credentials.
- Use GitHub Secrets for CI credentials.
- Use runtime Kubernetes secrets for application secrets.
- Do not create extra personal GitHub tokens when the existing integration has sufficient permission.

## 9. Branch and merge policy

Implementation work follows:

```text
master
  |
  `- type/short-description
       |
       |- implement
       |- CI
       |- Code Review
       `- squash merge -> master
```

Never implement directly on master. Use a dedicated descriptive branch, request Code Review, fix CI/review failures, and squash task commits before merging.

## 10. Failure handling

| Failure | Required action |
|---|---|
| Build failure | Stop before image publication. |
| Architecture failure | Stop; require linux/arm64. |
| Checksum failure | Do not publish; investigate artifact integrity. |
| GHCR publication failure | Do not dispatch the platform release. |
| GitOps promotion failure | Do not reconcile production. |
| FE/BE tag mismatch | Do not emit gitops-promoted-ready. |
| Kubernetes rollout failure | Collect Deployment, Pods, Events, rollout status, logs and health data; fix and repeat. |

## 11. Definition of Done

- [ ] FE/BE verification is independent
- [ ] one immutable prod-v<semver>-<sha> release tag is generated
- [ ] production images build natively for ARM64
- [ ] image architecture is verified
- [ ] exact images are exported and checksummed
- [ ] artifacts are validated before publication
- [ ] exact images are published to GHCR
- [ ] one release event is dispatched to platform-infra
- [ ] platform-infra fans out all required components
- [ ] all GitOps tags converge to the same release
- [ ] only then is gitops-promoted-ready emitted
- [ ] K3s reconciliation runs
- [ ] rollout and workload health are verified
- [ ] production failure is isolated per application
- [ ] source SHA -> GHCR -> GitOps -> K3s is traceable

## 12. New repository adoption checklist

1. Identify runtime components.
2. Define GHCR image names.
3. Define the package/version source.
4. Add the immutable release-tag workflow.
5. Add independent FE/BE verification.
6. Add native ARM64 builds.
7. Add architecture checks.
8. Add artifact checksums.
9. Add exact GHCR publication.
10. Add <app>-release-requested.
11. Add the matching platform-infra coordinator.
12. Add paired GitOps convergence checks.
13. Add production Kustomize image entries.
14. Add rollout/health verification.
15. Run the complete release once in production.
16. Document application-specific variables only; keep the workflow generic.

## Canonical contract

```text
SOURCE
  -> VERIFY
  -> BUILD ARM64
  -> CHECK ARCHITECTURE
  -> CHECKSUM ARTIFACTS
  -> PUBLISH EXACT IMAGE
  -> REQUEST RELEASE
  -> PAIR COMPONENTS
  -> PROMOTE GITOPS
  -> WAIT FOR CONVERGENCE
  -> RECONCILE K3S
  -> VERIFY HEALTH
```

**One source commit -> one immutable release -> one paired GitOps state -> one production rollout.**