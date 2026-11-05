#!/usr/bin/env python3
"""Keep optional VPS MCP operations read-only and subordinate to GitOps reconciliation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP_ROOT = ROOT / "apps" / "tce-vps-control-mcp"

REQUIRED_FILES = (
    "src/index.ts",
    "ops/tce-mcp-docker",
    "ops/k8s-rbac.yaml",
    "scripts/install.sh",
    "ops/tce-vps-control-mcp.sudoers",
    "ops/tce-vps-control-mcp.service",
    "README.md",
    "package.json",
)

FORBIDDEN_COMMANDS = (
    (re.compile(r"\bdocker\s+restart\b", re.IGNORECASE), "direct Docker restart"),
    (re.compile(r"\bdocker\s+compose\b", re.IGNORECASE), "Docker Compose control"),
    (re.compile(r"\bkubectl\s+(?:apply|delete|patch|scale|set\s+image)\b", re.IGNORECASE), "direct Kubernetes mutation"),
    (re.compile(r"\bkubectl\s+rollout\s+restart\b", re.IGNORECASE), "direct Kubernetes rollout restart"),
    (re.compile(r"\bssh\s", re.IGNORECASE), "direct SSH control"),
)


def validate_files(files: dict[str, str]) -> list[str]:
    """Return contract violations for an optional MCP implementation."""
    if not files:
        return []

    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not files.get(relative):
            errors.append(f"required MCP file is missing or empty: {relative}")

    source = files.get("src/index.ts", "")
    wrapper = files.get("ops/tce-mcp-docker", "")
    rbac = files.get("ops/k8s-rbac.yaml", "")
    installer = files.get("scripts/install.sh", "")
    sudoers = files.get("ops/tce-vps-control-mcp.sudoers", "")
    service = files.get("ops/tce-vps-control-mcp.service", "")
    readme = files.get("README.md", "")

    for relative, content in (
        ("src/index.ts", source),
        ("ops/tce-mcp-docker", wrapper),
    ):
        for pattern, label in FORBIDDEN_COMMANDS:
            if pattern.search(content):
                errors.append(f"{relative} exposes {label}; production mutations belong to reconcile-vps.yml")

    for tool in ("docker_restart", "k8s_rollout_restart"):
        if re.search(rf'registerTool\(\s*["\']{re.escape(tool)}["\']', source):
            errors.append(f"src/index.ts registers mutating MCP tool {tool}")
        if tool in readme:
            errors.append(f"README.md advertises mutating MCP tool {tool}")

    wrapper_cases = re.findall(r"(?m)^\s*([a-z][a-z0-9_-]*)\)", wrapper)
    if wrapper_cases and set(wrapper_cases) - {"ps", "logs"}:
        errors.append("Docker wrapper must expose only read-only ps/logs operations")

    for line in rbac.splitlines():
        if re.search(r"(?m)^\s*verbs\s*:", line) and re.search(r"\b(create|update|patch|delete)\b", line):
            errors.append("Kubernetes MCP RBAC must remain read-only (get/list/watch)")

    shell_invocation = re.search(
        r'run\("/usr/bin/sudo",\s*\["-n",\s*"-u",\s*"tce-shell",\s*"-H",\s*"--",\s*"/bin/bash",\s*"-lc",\s*command\]',
        source,
    )
    if shell_invocation is None:
        errors.append("shell_execute must run bash as the separate unprivileged tce-shell account")
    if "await realpath(requested)" not in source:
        errors.append("shell working-directory validation must resolve symlinks before checking allowed roots")
    if "mode: 0o600" not in source:
        errors.append("MCP audit records must be private to the tce-mcp account")
    if "groupadd --system tce-shell" not in installer or "useradd --system --gid tce-shell" not in installer:
        errors.append("installer must create tce-shell with a separate primary group")
    if "package-lock.json is required" not in installer or "npm ci --include=dev --ignore-scripts" not in installer:
        errors.append("installer must require a committed lockfile and use npm ci")
    if "tce-mcp ALL=(tce-shell) NOPASSWD: /bin/bash -lc *" not in sudoers:
        errors.append("sudoers must allow shell execution only as the separate tce-shell account")
    root_rules = [
        line.strip() for line in sudoers.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and "(root)" in line
    ]
    if root_rules != ["tce-mcp ALL=(root) NOPASSWD: /usr/local/sbin/tce-mcp-docker *"]:
        errors.append("tce-mcp root access must be limited to the read-only Docker wrapper")
    if "UMask=0077" not in service:
        errors.append("MCP systemd service must use a private 0077 umask")
    if "reconcile-vps.yml" not in readme:
        errors.append("README must state that production mutations remain in reconcile-vps.yml")

    return errors


def load_mcp_files() -> dict[str, str]:
    if not MCP_ROOT.exists():
        return {}
    files: dict[str, str] = {}
    for relative in REQUIRED_FILES:
        path = MCP_ROOT / relative
        if path.is_file():
            files[relative] = path.read_text(encoding="utf-8")
    return files


def self_test() -> None:
    safe = {
        "src/index.ts": (
            'async function validateCwd(requested) { return await realpath(requested); }\n'
            'await appendFile(AUDIT_FILE, record, { mode: 0o600 });\n'
            'run("/usr/bin/sudo", ["-n", "-u", "tce-shell", "-H", "--", "/bin/bash", "-lc", command]);\n'
            'server.registerTool("k8s_get", {});\n'
        ),
        "ops/tce-mcp-docker": 'case "$action" in\n  ps) exec docker ps ;;\n  logs) exec docker logs "$1" ;;\nesac\n',
        "ops/k8s-rbac.yaml": 'verbs: ["get", "list", "watch"]\n',
        "scripts/install.sh": (
            'groupadd --system tce-shell\n'
            'useradd --system --gid tce-shell tce-shell\n'
            'echo "package-lock.json is required"\n'
            'npm ci --include=dev --ignore-scripts --no-audit --no-fund\n'
        ),
        "ops/tce-vps-control-mcp.sudoers": (
            'tce-mcp ALL=(root) NOPASSWD: /usr/local/sbin/tce-mcp-docker *\n'
            'tce-mcp ALL=(tce-shell) NOPASSWD: /bin/bash -lc *\n'
        ),
        "ops/tce-vps-control-mcp.service": "UMask=0077\n",
        "README.md": "Read-only diagnostics; production changes use reconcile-vps.yml.\n",
        "package.json": '{"name":"@tce/vps-control-mcp"}',
    }
    if validate_files(safe):
        raise SystemExit("Self-test failed: a read-only, unprivileged MCP fixture was rejected.")

    unsafe = dict(safe)
    unsafe["src/index.ts"] += 'server.registerTool("docker_restart", {});\n'
    unsafe["ops/tce-mcp-docker"] += '  restart) exec docker restart "$1" ;;\n'
    unsafe["ops/k8s-rbac.yaml"] += 'verbs: ["get", "list", "watch", "patch"]\n'
    unsafe["README.md"] += "docker_restart\n"
    if not validate_files(unsafe):
        raise SystemExit("Self-test failed: mutating MCP fixture was accepted.")

    broken_identity = dict(safe)
    broken_identity["src/index.ts"] = broken_identity["src/index.ts"].replace(
        'run("/usr/bin/sudo", ["-n", "-u", "tce-shell", "-H", "--", "/bin/bash", "-lc", command]);\n',
        "",
    )
    broken_identity["scripts/install.sh"] = "useradd tce-shell\n"
    broken_identity["ops/tce-vps-control-mcp.sudoers"] = "tce-mcp ALL=(root) NOPASSWD: ALL\n"
    if not validate_files(broken_identity):
        raise SystemExit("Self-test failed: missing shell identity isolation was accepted.")

    print("VPS MCP GitOps-only/read-only contract self-test passed.")


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        self_test()
        return 0

    files = load_mcp_files()
    errors = validate_files(files)
    if errors:
        for error in errors:
            print(f"::error::{error}")
        return 1

    if files:
        print("Optional VPS MCP is read-only, GitOps-subordinate and shell-identity isolated.")
    else:
        print("Optional VPS MCP is absent; no alternate MCP production control path is present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
