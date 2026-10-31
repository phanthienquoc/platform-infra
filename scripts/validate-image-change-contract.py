#!/usr/bin/env python3
"""Fail closed when a PR introduces mutable production image references.

This guard deliberately checks changed lines only. Existing legacy references remain
visible as deployment blockers in the readiness tracker until a verified promotion
can replace them; unrelated documentation changes do not make validation impossible.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
STOCK_IMAGE = re.compile(
    r"^ghcr\.io/phanthienquoc/stockdividend/(?:backend|admin):([0-9a-f]{40})$"
)
STOCK_DIGEST = re.compile(
    r"^ghcr\.io/phanthienquoc/stockdividend/(?:backend|admin)@sha256:[0-9a-f]{64}$"
)
MEDIA_TAG = re.compile(
    r"^ghcr\.io/phanthienquoc/media-generation/(?:backend|frontend):prod-v[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]{40}$"
)
MEDIA_DIGEST = re.compile(
    r"^ghcr\.io/phanthienquoc/media-generation/(?:backend|frontend)@sha256:[0-9a-f]{64}$"
)
MICROFE_TAG = re.compile(
    r"^ghcr\.io/phanthienquoc/microfe-(?:shell|ws):[0-9a-f]{40}$"
)
MICROFE_DIGEST = re.compile(
    r"^ghcr\.io/phanthienquoc/microfe-(?:shell|ws)@sha256:[0-9a-f]{64}$"
)


def scalar(value: str) -> str:
    return value.strip().split("#", 1)[0].strip().strip('"').strip("'")


def validate_diff(diff: str) -> tuple[list[str], int]:
    errors: list[str] = []
    inspected = 0
    path = ""

    for raw in diff.splitlines():
        if raw.startswith("+++ b/"):
            path = raw[6:]
            continue
        if raw.startswith("+++"):
            path = ""
            continue
        if not raw.startswith("+") or raw.startswith("+++"):
            continue

        line = raw[1:].strip()
        if path.startswith("apps/stockdividend/"):
            if line.startswith("newTag:"):
                tag = scalar(line.split(":", 1)[1])
                inspected += 1
                if not FULL_SHA.fullmatch(tag):
                    errors.append(
                        f"{path}: StockDividend production newTag must be a full "
                        f"40-character lowercase source SHA, got {tag!r}"
                    )
            elif line.startswith("digest:"):
                digest = scalar(line.split(":", 1)[1])
                inspected += 1
                if not DIGEST.fullmatch(digest):
                    errors.append(
                        f"{path}: StockDividend image digest must be sha256:<64 lowercase hex>, "
                        f"got {digest!r}"
                    )
            elif line.startswith("image:"):
                image = scalar(line.split(":", 1)[1])
                if image.startswith("ghcr.io/phanthienquoc/stockdividend/"):
                    inspected += 1
                    if not (STOCK_IMAGE.fullmatch(image) or STOCK_DIGEST.fullmatch(image)):
                        errors.append(
                            f"{path}: StockDividend image must use a full source SHA "
                            f"or sha256 digest, got {image!r}"
                        )

        if path.startswith("apps/media-generation/"):
            if line.startswith("newTag:"):
                tag = scalar(line.split(":", 1)[1])
                inspected += 1
                if not re.fullmatch(r"prod-v[0-9]+\\.[0-9]+\\.[0-9]+-[0-9a-f]{40}", tag):
                    errors.append(
                        f"{path}: Media production newTag must contain the full source SHA, got {tag!r}"
                    )
            elif line.startswith("digest:"):
                digest = scalar(line.split(":", 1)[1])
                inspected += 1
                if not DIGEST.fullmatch(digest):
                    errors.append(
                        f"{path}: Media image digest must be sha256:<64 lowercase hex>, got {digest!r}"
                    )
            elif line.startswith("image:"):
                image = scalar(line.split(":", 1)[1])
                if image.startswith("ghcr.io/phanthienquoc/media-generation/"):
                    inspected += 1
                    if not (MEDIA_TAG.fullmatch(image) or MEDIA_DIGEST.fullmatch(image)):
                        errors.append(
                            f"{path}: Media image must use a full source SHA tag or sha256 digest, got {image!r}"
                        )

        if path.startswith("platform/microfe/"):
            if line.startswith("newTag:"):
                tag = scalar(line.split(":", 1)[1])
                inspected += 1
                if not FULL_SHA.fullmatch(tag):
                    errors.append(
                        f"{path}: MicroFE newTag must be a full 40-character lowercase "
                        f"source SHA; digest promotion should use a digest field, "
                        f"got {tag!r}"
                    )
            elif line.startswith("digest:"):
                digest = scalar(line.split(":", 1)[1])
                inspected += 1
                if not DIGEST.fullmatch(digest):
                    errors.append(
                        f"{path}: MicroFE image digest must be sha256:<64 lowercase hex>, "
                        f"got {digest!r}"
                    )
            elif line.startswith("image:"):
                image = scalar(line.split(":", 1)[1])
                if image.startswith("ghcr.io/phanthienquoc/microfe-shell") or image.startswith(
                    "ghcr.io/phanthienquoc/microfe-ws"
                ):
                    inspected += 1
                    if not (MICROFE_TAG.fullmatch(image) or MICROFE_DIGEST.fullmatch(image)):
                        errors.append(
                            f"{path}: MicroFE image must use a full source SHA or sha256 "
                            f"digest; placeholder/mutable references are forbidden, "
                            f"got {image!r}"
                        )

    return errors, inspected


def self_test() -> None:
    sha = "a" * 40
    digest = "sha256:" + "b" * 64
    fixtures = [
        (
            "valid StockDividend source SHA",
            f"+++ b/apps/stockdividend/overlays/prod/kustomization.yaml\n+  newTag: {sha}\n",
            True,
        ),
        (
            "valid StockDividend digest",
            f"+++ b/apps/stockdividend/overlays/prod/kustomization.yaml\n+  digest: {digest}\n",
            True,
        ),
        (
            "invalid StockDividend digest",
            "+++ b/apps/stockdividend/overlays/prod/kustomization.yaml\n+  digest: sha256:xyz\n",
            False,
        ),
        (
            "invalid abbreviated StockDividend tag",
            "+++ b/apps/stockdividend/overlays/prod/kustomization.yaml\n+  newTag: 12d63b4\n",
            False,
        ),
        (
            "valid Media digest promotion",
            f"+++ b/apps/media-generation/overlays/prod/kustomization.yaml\\n+  digest: {digest}\\n",
            True,
        ),
        (
            "invalid abbreviated Media release tag",
            "+++ b/apps/media-generation/overlays/prod/kustomization.yaml\\n+  newTag: prod-v0.3.0-58f80a8\\n",
            False,
        ),
        (
            "valid Media full-SHA release tag",
            f"+++ b/apps/media-generation/overlays/prod/kustomization.yaml\\n+  newTag: prod-v0.3.0-{sha}\\n",
            True,
        ),
        (
            "valid MicroFE digest promotion",
            f"+++ b/platform/microfe/kustomization.yaml\n+  digest: {digest}\n",
            True,
        ),
        (
            "invalid MicroFE placeholder tag",
            "+++ b/platform/microfe/kustomization.yaml\n+  newTag: RELEASE_SHA\n",
            False,
        ),
        (
            "invalid MicroFE mutable tag",
            "+++ b/platform/microfe/shell/deployment.yaml\n+          image: ghcr.io/phanthienquoc/microfe-shell:0.1.0\n",
            False,
        ),
        (
            "valid MicroFE digest image",
            f"+++ b/platform/microfe/shell/deployment.yaml\n+          image: ghcr.io/phanthienquoc/microfe-shell@{digest}\n",
            True,
        ),
    ]

    for name, diff, should_pass in fixtures:
        errors, inspected = validate_diff(diff)
        passed = not errors and inspected > 0
        if passed != should_pass:
            detail = "; ".join(errors) if errors else f"inspected={inspected}"
            raise SystemExit(f"Image-change contract self-test failed ({name}): {detail}")

    print(f"Image-change contract self-tests passed ({len(fixtures)} fixtures).")


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        self_test()
        return 0
    if len(argv) != 2:
        print(
            "Usage: validate-image-change-contract.py --self-test | <base-sha> <head-sha>",
            file=sys.stderr,
        )
        return 2

    base, head = argv
    result = subprocess.run(
        [
            "git",
            "diff",
            "--no-ext-diff",
            "--unified=0",
            base,
            head,
            "--",
            "apps/stockdividend",
            "apps/media-generation",
            "platform/microfe",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    errors, inspected = validate_diff(result.stdout)
    if errors:
        for error in errors:
            print(f"::error::{error}")
        return 1

    print(
        f"Validated {inspected} changed StockDividend/Media/MicroFE image reference(s); "
        "no abbreviated, mutable, or placeholder references were introduced."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
