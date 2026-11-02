#!/usr/bin/env python3
"""Resolve and validate the paired TCE production image references in Kustomize."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

IMAGES = {
    "web": "ghcr.io/phanthienquoc/tce-dashboard/web",
    "service": "ghcr.io/phanthienquoc/tce-dashboard/service",
}
TAG = re.compile(r"^prod-v[0-9]+[.][0-9]+[.][0-9]+-[0-9a-f]{7,40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def extract_reference(text: str, image: str) -> tuple[str, str]:
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == f"- name: {image}"]
    if len(starts) != 1:
        raise ValueError(f"Expected exactly one TCE image entry for {image}; found {len(starts)}")
    start = starts[0]
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("- name:")),
        len(lines),
    )
    fields: list[tuple[str, str]] = []
    for line in lines[start + 1 : end]:
        stripped = line.strip()
        if stripped.startswith("newTag:"):
            fields.append(("tag", stripped.split(":", 1)[1].strip()))
        elif stripped.startswith("digest:"):
            fields.append(("digest", stripped.split(":", 1)[1].strip()))
    if len(fields) != 1:
        raise ValueError(f"Expected exactly one newTag or digest field for {image}; found {len(fields)}")
    kind, value = fields[0]
    if kind == "tag" and not TAG.fullmatch(value):
        raise ValueError(f"Invalid TCE release tag for {image}: {value!r}")
    if kind == "digest" and not DIGEST.fullmatch(value):
        raise ValueError(f"Invalid TCE image digest for {image}: {value!r}")
    return kind, value


def resolve_pair(text: str) -> dict[str, tuple[str, str]]:
    refs = {component: extract_reference(text, image) for component, image in IMAGES.items()}
    kinds = {kind for kind, _ in refs.values()}
    if len(kinds) != 1:
        raise ValueError("TCE web/service references must both be tags or both be digests; mixed references are forbidden")
    if kinds == {"tag"} and refs["web"][1] != refs["service"][1]:
        raise ValueError("TCE legacy web/service tags must be identical")
    return refs


def self_test() -> None:
    web_image = IMAGES["web"]
    service_image = IMAGES["service"]
    tag = "prod-v0.1.0-e75e338"
    web_digest = "sha256:" + "a" * 64
    service_digest = "sha256:" + "b" * 64
    tag_fixture = f"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
images:
- name: {web_image}
  newTag: {tag}
- name: {service_image}
  newTag: {tag}
"""
    digest_fixture = f"""apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
images:
- name: {web_image}
  digest: {web_digest}
- name: {service_image}
  digest: {service_digest}
"""
    if resolve_pair(tag_fixture)["web"] != ("tag", tag):
        raise SystemExit("Legacy TCE tag-pair self-test failed.")
    if resolve_pair(digest_fixture) != {
        "web": ("digest", web_digest),
        "service": ("digest", service_digest),
    }:
        raise SystemExit("TCE digest-pair self-test failed.")

    invalid = [
        tag_fixture.replace(f"newTag: {tag}", "newTag: prod-v0.1.0-deadbee", 1),
        digest_fixture.replace(f"digest: {web_digest}", "digest: sha256:bad", 1),
        digest_fixture.replace(f"digest: {service_digest}", "newTag: " + tag, 1),
        digest_fixture.replace(f"- name: {service_image}", "- name: ghcr.io/other/image"),
        digest_fixture.replace(f"  digest: {service_digest}", f"  digest: {service_digest}\n  newTag: {tag}"),
    ]
    for fixture in invalid:
        try:
            resolve_pair(fixture)
        except ValueError:
            continue
        raise SystemExit("TCE image-reference self-test accepted an invalid/mixed pair.")
    print("TCE GitOps image-reference self-tests passed (7 fixtures).")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--component", choices=("web", "service"))
    parser.add_argument("--validate-pair", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.file:
        parser.error("--file is required")
    text = Path(args.file).read_text(encoding="utf-8")
    if args.validate_pair:
        refs = resolve_pair(text)
        kind = refs["web"][0]
        label = refs["web"][1] if kind == "tag" else "paired sha256 digests"
        print(f"TCE GitOps release pairing passed: {kind} {label}")
        return 0
    if args.component:
        kind, value = extract_reference(text, IMAGES[args.component])
        print(f"{kind}:{value}")
        return 0
    parser.error("choose --validate-pair or --component")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
