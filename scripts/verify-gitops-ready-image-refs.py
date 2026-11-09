#!/usr/bin/env python3
"""Resolve only digest-pinned GitOps images for an authenticated promotion event."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
PROD_RELEASE = re.compile(r"^prod-v[0-9]+\\.[0-9]+\\.[0-9]+-([0-9a-f]{40})$")
MICROFE_RELEASE = re.compile(r"^microfe-([0-9a-f]{7})$")

APP_IMAGES = {
    "auth-service": (
        "platform/auth-service/kustomization.yaml",
        ("ghcr.io/phanthienquoc/auth-service/auth",),
    ),
    "tce-dashboard": (
        "apps/tce-dashboard/overlays/prod/kustomization.yaml",
        (
            "ghcr.io/phanthienquoc/tce-dashboard/web",
            "ghcr.io/phanthienquoc/tce-dashboard/service",
        ),
    ),
    "microfe": (
        "platform/microfe/kustomization.yaml",
        (
            "ghcr.io/phanthienquoc/microfe-shell",
            "ghcr.io/phanthienquoc/microfe-ws",
        ),
    ),
)


class ContractError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def extract_digest(content: str, image: str) -> str:
    lines = content.splitlines()
    starts = [index for index, line in enumerate(lines) if line.strip() == f"- name: {image}"]
    require(len(starts) == 1, f"Expected exactly one GitOps image entry for {image}, found {len(starts)}.")
    start = starts[0]
    end = start + 1
    while end < len(lines) and not lines[end].lstrip().startswith("- name:"):
        end += 1
    fields = [
        lines[index].strip()
        for index in range(start + 1, end)
        if lines[index].strip().startswith(("newTag:", "digest:"))
    ]
    require(len(fields) == 1, f"Expected exactly one tag/digest field for {image}, found {len(fields)}.")
    require(fields[0].startswith("digest: "), f"{image} is not digest-pinned in the current GitOps manifest.")
    digest = fields[0].split(":", 1)[1].strip()
    require(DIGEST.fullmatch(digest) is not None, f"{image} has an invalid sha256 digest.")
    return digest


def resolve(app: str, release: str, source_commit: str, root: Path = Path(".")) -> list[tuple[str, str, str]]:
    require(app in APP_IMAGES, f"Retired or unsupported GitOps-ready application: {app!r}.")
    require(SHA.fullmatch(source_commit) is not None, "source_commit must be a full lowercase 40-character SHA.")
    if app in ("auth-service", "tce-dashboard"):
        match = PROD_RELEASE.fullmatch(release)
        require(match is not None and match.group(1) == source_commit,
                f"{app} release tag must end with the exact source_commit.")
        immutable_tag = release
    else:
        match = MICROFE_RELEASE.fullmatch(release)
        require(match is not None and match.group(1) == source_commit[:7],
                "MicroFE release label must match the source commit's first seven characters.")
        immutable_tag = source_commit

    manifest_path, images = APP_IMAGES[app]
    path = root / manifest_path
    require(path.is_file(), f"GitOps image manifest does not exist: {manifest_path}.")
    content = path.read_text(encoding="utf-8")
    return [(image, immutable_tag, extract_digest(content, image)) for image in images]


def self_test() -> None:
    source = "a" * 40
    digest_a = "sha256:" + "a" * 64
    digest_b = "sha256:" + "b" * 64
    auth_image = APP_IMAGES["auth-service"][1][0]
    tce_web, tce_service = APP_IMAGES["tce-dashboard"][1]
    microfe_shell, microfe_ws = APP_IMAGES["microfe"][1]

    auth_fixture = f"images:\\n- name: {auth_image}\\n  newName: {auth_image}\\n  digest: {digest_a}\\n"
    tce_fixture = (
        f"images:\\n- name: {tce_web}\\n  digest: {digest_a}\\n"
        f"- name: {tce_service}\\n  digest: {digest_b}\\n"
    )
    microfe_fixture = (
        f"images:\\n- name: {microfe_shell}\\n  digest: {digest_a}\\n"
        f"- name: {microfe_ws}\\n  digest: {digest_b}\\n"
    )

    require(extract_digest(auth_fixture, auth_image) == digest_a, "Auth digest fixture failed.")
    require(extract_digest(tce_fixture, tce_web) == digest_a, "TCE web digest fixture failed.")
    require(extract_digest(tce_fixture, tce_service) == digest_b, "TCE service digest fixture failed.")
    require(extract_digest(microfe_fixture, microfe_shell) == digest_a, "MicroFE Shell digest fixture failed.")
    require(extract_digest(microfe_fixture, microfe_ws) == digest_b, "MicroFE WS digest fixture failed.")

    bad_cases = [
        (auth_fixture.replace(f"  digest: {digest_a}", "  newTag: latest"), auth_image),
        (auth_fixture.replace(f"  digest: {digest_a}", f"  digest: {digest_a}\\n  digest: {digest_b}"), auth_image),
        (auth_fixture.replace(auth_image, "ghcr.io/phanthienquoc/other/image"), auth_image),
        (auth_fixture.replace(digest_a, "sha256:bad"), auth_image),
    ]
    for fixture_text, image in bad_cases:
        try:
            extract_digest(fixture_text, image)
        except ContractError:
            continue
        raise SystemExit("GitOps image-ref self-test accepted a non-digest or ambiguous manifest entry.")

    try:
        resolve("auth-service", f"prod-v1.2.3-{'b' * 40}", source)
    except ContractError:
        pass
    else:
        raise SystemExit("GitOps image-ref self-test accepted a release/source SHA mismatch.")
    try:
        resolve("stockdividend", f"prod-v1.2.3-{source}", source)
    except ContractError:
        pass
    else:
        raise SystemExit("GitOps image-ref self-test accepted a retired app.")

    print("GitOps ready image-ref self-tests passed (5 positive extraction, 6 negative contract cases).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app")
    parser.add_argument("--release")
    parser.add_argument("--source-commit")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not all((args.app, args.release, args.source_commit)):
        parser.error("--app, --release and --source-commit are required unless --self-test is used.")
    try:
        for image, tag, digest in resolve(args.app, args.release, args.source_commit, args.root):
            print(f"{image}\\t{tag}\\t{digest}")
    except (OSError, ContractError) as exc:
        print(f"::error::GitOps-ready image reference validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
