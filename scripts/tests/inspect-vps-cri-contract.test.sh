#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
inspect_script="$repo_root/scripts/inspect-vps.sh"
inspect_workflow="$repo_root/.github/workflows/inspect-vps.yml"
recovery_workflow="$repo_root/.github/workflows/recover-stale-ops.yml"

grep -Fq 'grep -q "^# VPS inspection$" debug/vps-latest.md' "$inspect_workflow"
grep -Fq "sed -n '1,5p' debug/vps-latest.md" "$inspect_workflow"
grep -Fq 'name: Restore generated inspection snapshot after failed run' "$inspect_workflow"
grep -Fq 'git restore --source=HEAD --staged --worktree -- debug/vps-latest.md' "$inspect_workflow"
grep -Fq '"!scripts/tests/**"' "$recovery_workflow"
grep -Fq 'echo "Images used by active platform namespaces (repo tags, repo digests, image ID, pinned, size bytes):"' "$inspect_script"
grep -Fq 'echo "Containers in active platform namespaces (container ID, name, image reference, state):"' "$inspect_script"
grep -Fq 'keycloak_ready="$(awk' "$inspect_script"
grep -Fq 'if [[ "$keycloak_ready" =~ ^[0-9]+/([0-9]+)$ ]]' "$inspect_script"
grep -Fq 'Keycloak logs skipped: deployment is intentionally scaled to zero.' "$inspect_script"
grep -Fq 'Keycloak logs skipped: desired replica count unavailable; refusing a pod-waiting logs request.' "$inspect_script"
grep -Fq 'grep -q "^Images used by active platform namespaces (repo tags, repo digests, image ID, pinned, size bytes):$" debug/vps-latest.md' "$inspect_workflow"
grep -Fq 'grep -q "^Containers in active platform namespaces (container ID, name, image reference, state):$" debug/vps-latest.md' "$inspect_workflow"

bash -n "$inspect_script"
# The self-hosted runner reuses its checkout. Force-update only the local
# remote-tracking ref so a stale/divergent origin/master cannot block inspection.
grep -Fq "fetch --no-tags origin +refs/heads/master:refs/remotes/origin/master" "$inspect_workflow"
grep -Fq "git -c \"http.https://github.com/.extraheader=AUTHORIZATION: basic \$auth_header\" \\" "$inspect_workflow"
validator_workflow="$repo_root/.github/workflows/validate-github-actions.yml"
grep -Fq 'ACTIONLINT_VERSION: "1.7.12"' "$validator_workflow"
grep -Fq 'CHECKSUMS_SHA256: "433028cf0ba3c42163ea1a668dedce30fcdbe84fe912b1a5e288c006eab8a4f5"' "$validator_workflow"
grep -Fq 'sha256sum --check actionlint.sha256' "$validator_workflow"
grep -Fq 'CRI=/usr/local/sbin/platform-crictl' "$inspect_script"
grep -Fq "sudo \"\$CRI\" images" "$inspect_script"
grep -Fq "sudo \"\$CRI\" ps" "$inspect_script"
grep -Fq "jq -e '.images | type == \"array\"'" "$inspect_script"
grep -Fq "jq -e '.containers | type == \"array\"'" "$inspect_script"
grep -Fq '.repoTags // []' "$inspect_script"
grep -Fq '.repoDigests // []' "$inspect_script"
grep -Fq '.imageRef // ""' "$inspect_script"

if grep -Eq 'sudo[[:space:]]+(/usr/local/bin/crictl|crictl)([[:space:]]|$)' "$inspect_script"; then
  echo "Inspection must use the restricted platform-crictl wrapper, not raw crictl." >&2
  exit 1
fi
if grep -Fq 'sudo docker system df' "$inspect_script"; then
  echo "Docker diagnostics must use the runner's docker-group access, not unapproved sudo." >&2
  exit 1
fi
if grep -Fq 'sudo du -xhd1' "$inspect_script"; then
  echo "Disk diagnostics must not invoke an unapproved sudo command." >&2
  exit 1
fi

echo "VPS inspection CRI wrapper contract tests passed."

grep -Fq 'ACTIVE_NAMESPACES=(default kube-node-lease kube-public kube-system cert-manager microfe-platform tce-prod k3s-debug)' "$inspect_script"
# shellcheck disable=SC2016
grep -Fq 'get pods -n "$namespace" -o wide' "$inspect_script"
# shellcheck disable=SC2016
grep -Fq 'get events -n "$namespace"' "$inspect_script"
if grep -Eq 'get (pods|deployments|services|ingress|events|pvc) -A' "$inspect_script"; then
  echo "Inspection must restrict namespace-scoped output to the active platform allowlist." >&2
  exit 1
fi
if grep -Fq 'decommission-' "$inspect_script"; then
  echo "Generic VPS inspection must not invoke retirement helpers." >&2
  exit 1
fi
