#!/usr/bin/env python3
"""Promote the canonical Auth image by immutable GHCR digest in one Kustomize entry."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IMAGE = "ghcr.io/phanthienquoc/auth-service/auth"
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    pass


def update_text(content: str, digest: str) -> str:
    if not DIGEST_PATTERN.fullmatch(digest):
        raise ContractError("Auth image digest must use sha256:<64 lowercase hex>.")

    lines = content.splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip() == f"- name: {IMAGE}"]
    if len(matches) != 1:
        raise ContractError(f"Expected exactly one Auth image entry, found {len(matches)}.")

    start = matches[0]
    end = start + 1
    while end < len(lines) and not lines[end].lstrip().startswith("- name:"):
        end += 1

    fields = [
        index
        for index in range(start + 1, end)
        if lines[index].strip().startswith(("newTag:", "digest:"))
    ]
    if len(fields) != 1:
        raise ContractError(f"Expected exactly one tag/digest field for {IMAGE}, found {len(fields)}.")

    field_index = fields[0]
    indent = lines[field_index][: len(lines[field_index]) - len(lines[field_index].lstrip())]
    lines[field_index] = f"{indent}digest: {digest}"
    return "\n".join(lines) + "\n"


def self_test() -> None:
    tag_fixture = (
        "resources:\n"
        "- deployment.yaml\n"
        "images:\n"
        f"- name: {IMAGE}\n"
        f"  newName: {IMAGE}\n"
        "  newTag: prod-v1.0.0-0123456789abcdef0123456789abcdef01234567\n"
    )
    digest = "sha256:" + "a" * 64
    updated = update_text(tag_fixture, digest)
    if f"  digest: {digest}\n" not in updated or "newTag:" in updated:
        raise ContractError("Auth image promotion did not replace the tag with the exact digest.")

    digest_fixture = tag_fixture.replace(
        "  newTag: prod-v1.0.0-0123456789abcdef0123456789abcdef01234567",
        f"  digest: {digest}",
    )
    if update_text(digest_fixture, digest) != digest_fixture:
        raise ContractError("Auth digest promotion is not idempotent.")

    cases = [
        ("malformed digest", lambda: update_text(tag_fixture, "sha256:bad")),
        ("missing image", lambda: update_text("images:\n- name: example/image\n  newTag: latest\n", digest)),
        ("duplicate image entry", lambda: update_text(tag_fixture + tag_fixture.split("images:\n", 1)[1], digest)),
        ("ambiguous fields", lambda: update_text(tag_fixture.replace("  newTag:", "  newTag:", 1).replace("  newTag:", "  digest: " + digest + "\n  newTag:", 1), digest)),
    ]
    for name, operation in cases:
        try:
            operation()
        except ContractError:
            continue
        raise ContractError(f"Self-test accepted invalid case: {name}.")
    print("Auth digest promotion helper self-test passed (6 cases).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--digest")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if args.file is None or args.digest is None:
        parser.error("--file and --digest are required unless --self-test is used")
    if not args.file.is_file():
        raise ContractError(f"Auth Kustomize file does not exist: {args.file}")
    updated = update_text(args.file.read_text(encoding="utf-8"), args.digest)
    args.file.write_text(updated, encoding="utf-8")
    print(f"Promoted {IMAGE} to {args.digest}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"::error::Auth digest promotion failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
