#!/usr/bin/env python3
"""Atomically replace the TCE production web/service image pair with registry digests."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
IMAGES = {
    "ghcr.io/phanthienquoc/tce-dashboard/web": "web",
    "ghcr.io/phanthienquoc/tce-dashboard/service": "service",
}


def promote_text(text: str, web_digest: str, service_digest: str) -> str:
    desired = {"web": web_digest, "service": service_digest}
    for component, digest in desired.items():
        if not DIGEST.fullmatch(digest):
            raise ValueError(f"Invalid TCE {component} digest: {digest!r}")

    lines = text.splitlines()
    found: set[str] = set()
    for index, line in enumerate(lines):
        stripped = line.strip()
        image = stripped.removeprefix("- name: ")
        if not stripped.startswith("- name: ") or image not in IMAGES:
            continue
        component = IMAGES[image]
        if component in found:
            raise ValueError(f"Duplicate TCE image entry: {image}")
        end = index + 1
        while end < len(lines) and not lines[end].lstrip().startswith("- name:"):
            end += 1
        fields = [i for i in range(index + 1, end) if lines[i].strip().startswith(("newTag:", "digest:"))]
        if len(fields) != 1:
            raise ValueError(f"Expected exactly one tag/digest field for {image}")
        field_index = fields[0]
        indent = lines[field_index][:len(lines[field_index]) - len(lines[field_index].lstrip())]
        lines[field_index] = f"{indent}digest: {desired[component]}"
        found.add(component)

    if found != set(IMAGES.values()):
        raise ValueError(f"Missing TCE image entries: {sorted(set(IMAGES.values()) - found)}")
    return "\n".join(lines) + "\n"


def self_test() -> None:
    fixture = """apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
images:
- name: ghcr.io/phanthienquoc/tce-dashboard/web
  newTag: prod-v0.1.0-abcdef0
- name: ghcr.io/phanthienquoc/tce-dashboard/service
  digest: sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
"""
    web = "sha256:" + "a" * 64
    service = "sha256:" + "b" * 64
    updated = promote_text(fixture, web, service)
    if f"  digest: {web}" not in updated or f"  digest: {service}" not in updated:
        raise SystemExit("TCE paired digest self-test did not update both components.")
    if "newTag:" in updated:
        raise SystemExit("TCE paired digest self-test left a mutable tag field.")
    bad_cases = [
        ("sha256:bad", service, fixture),
        (web, "sha256:bad", fixture),
        (web, service, fixture.replace("- name: ghcr.io/phanthienquoc/tce-dashboard/service", "- name: other/image")),
        (web, service, fixture.replace("  newTag: prod-v0.1.0-abcdef0", "  newTag: x\n  digest: sha256:" + "c" * 64)),
    ]
    for bad_web, bad_service, bad_fixture in bad_cases:
        try:
            promote_text(bad_fixture, bad_web, bad_service)
        except ValueError:
            continue
        raise SystemExit("TCE paired digest self-test accepted an invalid fixture.")
    print("TCE paired digest promotion self-tests passed (5 fixtures).")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--file")
    parser.add_argument("--web-digest")
    parser.add_argument("--service-digest")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not all((args.file, args.web_digest, args.service_digest)):
        parser.error("--file, --web-digest and --service-digest are required")
    path = Path(args.file)
    path.write_text(promote_text(path.read_text(), args.web_digest, args.service_digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
