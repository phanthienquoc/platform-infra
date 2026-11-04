#!/usr/bin/env python3
"""Atomically promote a complete app-owned image pair to immutable registry digests.

The helper is intentionally offline: publisher provenance and GHCR tag-to-digest
verification happen before this script is invoked. It only rewrites the two
approved image entries in the checked-out GitOps overlay.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
APP_IMAGES = {
    "stockdividend": {
        "backend": "ghcr.io/phanthienquoc/stockdividend/backend",
        "admin": "ghcr.io/phanthienquoc/stockdividend/admin",
    },
    "media-generation": {
        "backend": "ghcr.io/phanthienquoc/media-generation/backend",
        "frontend": "ghcr.io/phanthienquoc/media-generation/frontend",
    },
}


def promote_text(text: str, app: str, component_digests: dict[str, str]) -> str:
    if app not in APP_IMAGES:
        raise ValueError(f"unsupported paired-digest application: {app}")

    components = APP_IMAGES[app]
    if set(component_digests) != set(components):
        expected = ", ".join(sorted(components))
        actual = ", ".join(sorted(component_digests))
        raise ValueError(
            f"{app} requires exactly the paired components [{expected}], got [{actual}]"
        )

    desired = {image: component_digests[component] for component, image in components.items()}
    for image, digest in desired.items():
        if not DIGEST.fullmatch(digest):
            raise ValueError(f"invalid digest for {image}: {digest!r}")

    lines = text.splitlines()
    found: set[str] = set()

    for index, line in enumerate(lines):
        match = re.match(r"^\s*-\s+name:\s*(\S+)\s*$", line)
        if not match or match.group(1) not in desired:
            continue

        image = match.group(1)
        if image in found:
            raise ValueError(f"duplicate image entry: {image}")

        end = index + 1
        while end < len(lines) and not lines[end].lstrip().startswith("- name:"):
            end += 1

        fields = [
            field_index
            for field_index in range(index + 1, end)
            if lines[field_index].strip().startswith(("newTag:", "digest:"))
        ]
        if len(fields) != 1:
            raise ValueError(
                f"expected exactly one newTag or digest field for {image}; found {len(fields)}"
            )

        field_index = fields[0]
        indent = lines[field_index][: len(lines[field_index]) - len(lines[field_index].lstrip())]
        lines[field_index] = f"{indent}digest: {desired[image]}"
        found.add(image)

    missing = set(desired) - found
    if missing:
        raise ValueError(f"paired manifest entries missing: {', '.join(sorted(missing))}")

    newline = "\r\n" if "\r\n" in text else "\n"
    trailing_newline = text.endswith(("\n", "\r"))
    return newline.join(lines) + (newline if trailing_newline else "")


def promote_file(path: Path, app: str, component_digests: dict[str, str]) -> None:
    original = path.read_text(encoding="utf-8")
    promoted = promote_text(original, app, component_digests)
    mode = path.stat().st_mode

    temporary_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = temporary.name
            temporary.write(promoted)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass


def expect_rejection(text: str, app: str, digests: dict[str, str], label: str) -> None:
    try:
        promote_text(text, app, digests)
    except ValueError:
        return
    raise AssertionError(f"invalid paired-digest fixture was accepted: {label}")


def self_test() -> None:
    backend = "sha256:" + "a" * 64
    admin = "sha256:" + "b" * 64
    frontend = "sha256:" + "c" * 64
    sha = "0123456789abcdef0123456789abcdef01234567"

    stock_fixture = f"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
images:
- name: ghcr.io/phanthienquoc/stockdividend/backend
  newName: ghcr.io/phanthienquoc/stockdividend/backend
  newTag: {sha}
- name: ghcr.io/phanthienquoc/stockdividend/admin
  newName: ghcr.io/phanthienquoc/stockdividend/admin
  newTag: {sha}
- name: ghcr.io/phanthienquoc/microfe-shell
  digest: sha256:{'d' * 64}
"""
    stock_promoted = promote_text(
        stock_fixture, "stockdividend", {"backend": backend, "admin": admin}
    )
    if f"  digest: {backend}" not in stock_promoted or f"  digest: {admin}" not in stock_promoted:
        raise AssertionError("StockDividend backend/admin pair was not promoted together")
    if f"  newTag: {sha}" in stock_promoted:
        raise AssertionError("StockDividend mutable tag field was not replaced")
    if f"  digest: sha256:{'d' * 64}" not in stock_promoted:
        raise AssertionError("unrelated image entry was modified")

    media_fixture = f"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
images:
- name: ghcr.io/phanthienquoc/media-generation/backend
  newTag: prod-v1.2.3-{sha}
- name: ghcr.io/phanthienquoc/media-generation/frontend
  newTag: prod-v1.2.3-{sha}
"""
    media_promoted = promote_text(
        media_fixture, "media-generation", {"backend": backend, "frontend": frontend}
    )
    if f"  digest: {backend}" not in media_promoted or f"  digest: {frontend}" not in media_promoted:
        raise AssertionError("Media backend/frontend pair was not promoted together")

    expect_rejection(stock_fixture, "stockdividend", {"backend": "sha256:bad", "admin": admin}, "malformed digest")
    expect_rejection(stock_fixture, "stockdividend", {"backend": backend}, "missing paired component")
    expect_rejection(stock_fixture.replace("- name: ghcr.io/phanthienquoc/stockdividend/admin\n", ""), "stockdividend", {"backend": backend, "admin": admin}, "missing manifest entry")
    expect_rejection(stock_fixture + stock_fixture.split("- name: ghcr.io/phanthienquoc/stockdividend/admin", 1)[1].join(["- name: ghcr.io/phanthienquoc/stockdividend/admin", ""]), "stockdividend", {"backend": backend, "admin": admin}, "duplicate manifest entry")
    expect_rejection(stock_fixture.replace("  newTag: " + sha, "  newTag: " + sha + "\n  digest: " + backend, 1), "stockdividend", {"backend": backend, "admin": admin}, "multiple tag/digest fields")

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "kustomization.yaml"
        path.write_text(stock_fixture, encoding="utf-8")
        before = path.read_text(encoding="utf-8")
        try:
            promote_file(path, "stockdividend", {"backend": "sha256:bad", "admin": admin})
        except ValueError:
            pass
        else:
            raise AssertionError("invalid file promotion unexpectedly succeeded")
        if path.read_text(encoding="utf-8") != before:
            raise AssertionError("invalid promotion modified the source file")

    print("Paired StockDividend/Media digest-promotion self-tests passed.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path)
    parser.add_argument("--app", choices=sorted(APP_IMAGES))
    parser.add_argument("--backend-digest")
    parser.add_argument("--admin-digest")
    parser.add_argument("--frontend-digest")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test()
            return 0
        if not args.file or not args.app or not args.backend_digest:
            parser.error("--file, --app and --backend-digest are required unless --self-test is used")

        if args.app == "stockdividend":
            if not args.admin_digest or args.frontend_digest:
                parser.error("StockDividend requires --admin-digest and does not accept --frontend-digest")
            digests = {"backend": args.backend_digest, "admin": args.admin_digest}
        else:
            if not args.frontend_digest or args.admin_digest:
                parser.error("Media Generation requires --frontend-digest and does not accept --admin-digest")
            digests = {"backend": args.backend_digest, "frontend": args.frontend_digest}

        promote_file(args.file, args.app, digests)
        print(f"Promoted the complete {args.app} image pair to verified immutable digests.")
        return 0
    except (OSError, ValueError, AssertionError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
