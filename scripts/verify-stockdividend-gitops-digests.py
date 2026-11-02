#!/usr/bin/env python3
"""Verify that the StockDividend backend/admin digest pair is on GitOps master."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IMAGES = {
    "ghcr.io/phanthienquoc/stockdividend/backend",
    "ghcr.io/phanthienquoc/stockdividend/admin",
}
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def parse_pair(text: str) -> dict[str, str]:
    lines = text.splitlines()
    found: dict[str, str] = {}

    for index, line in enumerate(lines):
        match = re.match(r"^\s*-\s+name:\s*(\S+)\s*$", line)
        if not match or match.group(1) not in IMAGES:
            continue

        image = match.group(1)
        if image in found:
            raise ValueError(f"duplicate image entry: {image}")

        end = index + 1
        while end < len(lines) and not re.match(r"^\s*-\s+name:", lines[end]):
            end += 1

        fields: dict[str, str] = {}
        for field_line in lines[index + 1 : end]:
            field = re.match(r"^\s+(digest|newTag):\s*(\S+)\s*$", field_line)
            if not field:
                continue
            key, value = field.groups()
            if key in fields:
                raise ValueError(f"duplicate {key} field for {image}")
            fields[key] = value

        if "newTag" in fields or "digest" not in fields:
            raise ValueError(f"{image} must be pinned by one digest field and no tag")
        if not DIGEST.fullmatch(fields["digest"]):
            raise ValueError(f"{image} has a malformed digest")
        found[image] = fields["digest"]

    missing = IMAGES - found.keys()
    if missing:
        raise ValueError(f"missing StockDividend image entries: {', '.join(sorted(missing))}")
    return found


def verify(text: str, backend_digest: str, admin_digest: str) -> None:
    expected = {
        "ghcr.io/phanthienquoc/stockdividend/backend": backend_digest,
        "ghcr.io/phanthienquoc/stockdividend/admin": admin_digest,
    }
    for image, digest in expected.items():
        if not DIGEST.fullmatch(digest):
            raise ValueError(f"expected digest for {image} is malformed")

    actual = parse_pair(text)
    for image, digest in expected.items():
        if actual[image] != digest:
            raise ValueError(
                f"GitOps digest mismatch for {image}: expected {digest}, found {actual[image]}"
            )


def self_test() -> None:
    backend = "sha256:" + "a" * 64
    admin = "sha256:" + "b" * 64
    fixture = f"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
images:
- name: ghcr.io/phanthienquoc/stockdividend/backend
  newName: ghcr.io/phanthienquoc/stockdividend/backend
  digest: {backend}
- name: ghcr.io/phanthienquoc/stockdividend/admin
  newName: ghcr.io/phanthienquoc/stockdividend/admin
  digest: {admin}
"""
    verify(fixture, backend, admin)

    invalid_cases = (
        (fixture, "sha256:" + "c" * 64, admin),
        (fixture, backend, "sha256:" + "d" * 64),
        (fixture.replace(f"  digest: {backend}", "  newTag: abc1234"), backend, admin),
        (fixture.replace(f"  digest: {admin}", "  digest: nope"), backend, admin),
        (fixture.replace(f"- name: ghcr.io/phanthienquoc/stockdividend/admin\n  newName: ghcr.io/phanthienquoc/stockdividend/admin\n  digest: {admin}\n", ""), backend, admin),
        (fixture + f"- name: ghcr.io/phanthienquoc/stockdividend/admin\n  digest: {admin}\n", backend, admin),
    )
    for text, expected_backend, expected_admin in invalid_cases:
        try:
            verify(text, expected_backend, expected_admin)
        except ValueError:
            continue
        raise AssertionError("invalid StockDividend digest-pair fixture was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path)
    parser.add_argument("--backend-digest")
    parser.add_argument("--admin-digest")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test()
            print("StockDividend GitOps digest-pair self-tests passed.")
            return 0
        if not args.file or not args.backend_digest or not args.admin_digest:
            parser.error("--file, --backend-digest and --admin-digest are required")
        verify(args.file.read_text(encoding="utf-8"), args.backend_digest, args.admin_digest)
        if not args.quiet:
            print("StockDividend backend/admin GitOps digest pair matches the publisher handoff.")
        return 0
    except (OSError, ValueError, AssertionError) as exc:
        if not args.quiet:
            print(f"::error::{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
