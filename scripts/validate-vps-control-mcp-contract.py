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
    "README.md",
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

    call_marker = "execFileAsync(file, args, {"
    if call_marker not in source:
        errors.append("shell runner must invoke execFileAsync with an explicit options object")
    else:
        call_options = source.split(call_marker, 1)[1].split("\n    });", 1)[0]
        if "uid: options.uid" not in call_options or "gid: options.gid" not in call_options:
            errors.append("shell runner must forward uid/gid to the child process")
    if "uid: SHELL_UID" not in source or "gid: SHELL_GID" not in source:
        errors.append("shell_execute must run with the dedicated tce-shell UID/GID")

    if not re.search(r"(?m)^SHELL_UID=.*$", installer) or not re.search(r"(?m)^SHELL_GID=.*$", installer):
        errors.append("installer must persist the dedicated shell UID/GID in server.env")

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
            'const SHELL_UID = 1001; const SHELL_GID = 1001;\n'
            'async function run(file, args, options = {}) {\n'
            '  await execFileAsync(file, args, {\n'
            '    uid: options.uid,\n'
            '    gid: options.gid\n'
            '  });\n'
            '}\n'
            'run("/bin/bash", ["-lc", "id"], { uid: SHELL_UID, gid: SHELL_GID });\n'
            'server.registerTool("k8s_get", {});\n'
        ),
        "ops/tce-mcp-docker": 'case "$action" in\n  ps) exec docker ps ;;\n  logs) exec docker logs "$1" ;;\nesac\n',
        "ops/k8s-rbac.yaml": 'verbs: ["get", "list", "watch"]\n',
        "scripts/install.sh": 'SHELL_UID="$(id -u tce-shell)"\nSHELL_GID="$(id -g tce-shell)"\n',
        "README.md": "Read-only host and Kubernetes inspection tools.\n",
    }
    if validate_files(safe):
        raise SystemExit("Self-test failed: a read-only, isolated MCP fixture was rejected.")

    unsafe = dict(safe)
    unsafe["src/index.ts"] += 'server.registerTool("docker_restart", {});\n'
    unsafe["ops/tce-mcp-docker"] += '  restart) exec docker restart "$1" ;;\n'
    unsafe["ops/k8s-rbac.yaml"] += 'verbs: ["get", "list", "watch", "patch"]\n'
    unsafe["README.md"] += "docker_restart\n"
    if not validate_files(unsafe):
        raise SystemExit("Self-test failed: mutating MCP fixture was accepted.")

    broken_identity = dict(safe)
    broken_identity["src/index.ts"] = broken_identity["src/index.ts"].replace(
        "    uid: options.uid,\n    gid: options.gid\n", ""
    ).replace("uid: SHELL_UID, gid: SHELL_GID", "")
    broken_identity["scripts/install.sh"] = "useradd tce-shell\n"
    if not validate_files(broken_identity):
        raise SystemExit("Self-test failed: missing shell UID/GID isolation was accepted.")

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
