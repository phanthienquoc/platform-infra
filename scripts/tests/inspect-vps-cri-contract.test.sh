#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
inspect_script="$repo_root/scripts/inspect-vps.sh"

bash -n "$inspect_script"
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
