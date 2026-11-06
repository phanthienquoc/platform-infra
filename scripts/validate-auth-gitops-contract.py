#!/usr/bin/env python3
"""Validate the effective rendered Auth workload contract without cluster access."""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path
from typing import Any

import yaml

NAMESPACE = "microfe-platform"
IMAGE_PATTERN = re.compile(
    r"^ghcr\.io/phanthienquoc/auth-service/auth"
    r"(?::(?:prod-v[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]{7,40}|[0-9a-f]{7,64})|@sha256:[0-9a-f]{64})$"
)
REQUIRED_SECRET_KEYS = (
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "JWT_SECRET",
    "MFA_ENCRYPTION_KEY",
)


class ContractError(ValueError):
    """A rendered Auth resource violates the production contract."""


def fail(message: str) -> None:
    raise ContractError(message)


def named(objects: list[dict[str, Any]], kind: str, name: str) -> list[dict[str, Any]]:
    return [
        obj
        for obj in objects
        if obj.get("kind") == kind
        and obj.get("metadata", {}).get("name") == name
        and obj.get("metadata", {}).get("namespace") == NAMESPACE
    ]


def exactly_one(objects: list[dict[str, Any]], kind: str, name: str) -> dict[str, Any]:
    matches = named(objects, kind, name)
    if len(matches) != 1:
        fail(f"expected exactly one {NAMESPACE}/{name} {kind}, found {len(matches)}")
    return matches[0]


def validate(objects: list[dict[str, Any]]) -> str:
    ingress = exactly_one(objects, "Ingress", "microfe-public")
    rules = [
        rule
        for rule in ingress.get("spec", {}).get("rules", [])
        if rule.get("host") == "auth.mrcute.space"
    ]
    if len(rules) != 1:
        fail(f"expected exactly one auth.mrcute.space Ingress rule, found {len(rules)}")
    auth_paths = [
        item
        for item in rules[0].get("http", {}).get("paths", [])
        if item.get("path") == "/"
        and item.get("pathType") == "Prefix"
        and item.get("backend", {}).get("service", {}).get("name") == "microfe-auth"
        and item.get("backend", {}).get("service", {}).get("port", {}).get("number") == 80
    ]
    if len(auth_paths) != 1:
        fail("auth.mrcute.space / Prefix route must target Service microfe-auth:80")

    service = exactly_one(objects, "Service", "microfe-auth")
    if service.get("spec", {}).get("selector") != {"app": "microfe-auth"}:
        fail("microfe-auth Service selector must be exactly app=microfe-auth")
    service_ports = service.get("spec", {}).get("ports", [])
    if not any(port.get("port") == 80 and port.get("targetPort") == 4010 for port in service_ports):
        fail("microfe-auth Service must route port 80 to container port 4010")

    deployment = exactly_one(objects, "Deployment", "microfe-auth")
    selector = deployment.get("spec", {}).get("selector", {}).get("matchLabels", {})
    pod_spec = deployment.get("spec", {}).get("template", {}).get("spec", {})
    pod_labels = deployment.get("spec", {}).get("template", {}).get("metadata", {}).get("labels", {})
    if selector.get("app") != "microfe-auth" or pod_labels.get("app") != "microfe-auth":
        fail("microfe-auth Deployment selector and pod labels must both include app=microfe-auth")

    containers = [container for container in pod_spec.get("containers", []) if container.get("name") == "auth"]
    if len(containers) != 1:
        fail(f"expected exactly one auth container, found {len(containers)}")
    container = containers[0]
    image = container.get("image", "")
    if not IMAGE_PATTERN.fullmatch(image):
        fail(f"effective Auth image must use an immutable SHA/versioned-SHA tag; got {image!r}")
    if not any(port.get("containerPort") == 4010 for port in container.get("ports", [])):
        fail("auth container must expose container port 4010")

    env_entries = container.get("env", [])
    for key in REQUIRED_SECRET_KEYS:
        entries = [entry for entry in env_entries if entry.get("name") == key]
        if len(entries) != 1:
            fail(f"runtime env {key} must be declared exactly once")
        reference = entries[0].get("valueFrom", {}).get("secretKeyRef", {})
        if reference != {"name": "microfe-auth-secrets", "key": key}:
            fail(f"runtime env {key} must reference microfe-auth-secrets/{key}; plaintext is forbidden")

    configmap = exactly_one(objects, "ConfigMap", "microfe-auth-config")
    config = configmap.get("data", {})
    if config.get("PORT") != "4010":
        fail("microfe-auth-config PORT must be 4010")
    if config.get("JWT_ISSUER") != "https://auth.mrcute.space":
        fail("JWT_ISSUER must match https://auth.mrcute.space")
    audiences = {part.strip() for part in config.get("JWT_AUDIENCE", "").split(",") if part.strip()}
    if "tce-dashboard" not in audiences:
        fail("JWT_AUDIENCE must include tce-dashboard; the retired Media audience is not accepted")

    expected_probes = {
        "startupProbe": "/api/health",
        "readinessProbe": "/api/ready",
        "livenessProbe": "/api/health",
    }
    for probe_name, expected_path in expected_probes.items():
        probe = container.get(probe_name, {})
        http_get = probe.get("httpGet", {})
        if http_get.get("path") != expected_path or http_get.get("port") != 4010:
            fail(f"{probe_name} must use HTTP {expected_path} on port 4010")

    return image


def fixture() -> list[dict[str, Any]]:
    return [
        {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {"name": "microfe-public", "namespace": NAMESPACE},
            "spec": {
                "rules": [
                    {
                        "host": "auth.mrcute.space",
                        "http": {
                            "paths": [
                                {
                                    "path": "/",
                                    "pathType": "Prefix",
                                    "backend": {"service": {"name": "microfe-auth", "port": {"number": 80}}},
                                }
                            ]
                        },
                    }
                ]
            },
        },
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "microfe-auth", "namespace": NAMESPACE},
            "spec": {
                "selector": {"app": "microfe-auth"},
                "ports": [{"port": 80, "targetPort": 4010}],
            },
        },
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "microfe-auth", "namespace": NAMESPACE},
            "spec": {
                "selector": {"matchLabels": {"app": "microfe-auth"}},
                "template": {
                    "metadata": {"labels": {"app": "microfe-auth"}},
                    "spec": {
                        "containers": [
                            {
                                "name": "auth",
                                "image": "ghcr.io/phanthienquoc/auth-service/auth:prod-v1.0.0-ceb2688",
                                "ports": [{"containerPort": 4010}],
                                "env": [
                                    {
                                        "name": key,
                                        "valueFrom": {
                                            "secretKeyRef": {"name": "microfe-auth-secrets", "key": key}
                                        },
                                    }
                                    for key in REQUIRED_SECRET_KEYS
                                ],
                                "startupProbe": {"httpGet": {"path": "/api/health", "port": 4010}},
                                "readinessProbe": {"httpGet": {"path": "/api/ready", "port": 4010}},
                                "livenessProbe": {"httpGet": {"path": "/api/health", "port": 4010}},
                            }
                        ]
                    },
                },
            },
        },
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": "microfe-auth-config", "namespace": NAMESPACE},
            "data": {
                "PORT": "4010",
                "JWT_ISSUER": "https://auth.mrcute.space",
                "JWT_AUDIENCE": "tce-dashboard",
            },
        },
    ]


def self_test() -> None:
    baseline = fixture()
    image = validate(baseline)
    if not IMAGE_PATTERN.fullmatch(image):
        fail("self-test fixture image unexpectedly failed immutable-tag validation")

    digest_docs = copy.deepcopy(baseline)
    digest_image = "ghcr.io/phanthienquoc/auth-service/auth@sha256:" + "a" * 64
    digest_docs[2]["spec"]["template"]["spec"]["containers"][0]["image"] = digest_image
    if validate(digest_docs) != digest_image:
        fail("self-test rejected a digest-pinned Auth image")

    cases = [
        (
            "wrong ingress backend",
            lambda docs: docs[0]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"].update(
                {"name": "wrong-service"}
            ),
        ),
        ("wrong Service target port", lambda docs: docs[1]["spec"]["ports"][0].update({"targetPort": 8080})),
        ("wrong Deployment selector", lambda docs: docs[2]["spec"]["selector"]["matchLabels"].update({"app": "other"})),
        ("mutable image tag", lambda docs: docs[2]["spec"]["template"]["spec"]["containers"][0].update({"image": "ghcr.io/phanthienquoc/auth-service/auth:latest"})),
        ("missing runtime secret", lambda docs: docs[2]["spec"]["template"]["spec"]["containers"][0]["env"].pop()),
        ("wrong JWT issuer", lambda docs: docs[3]["data"].update({"JWT_ISSUER": "https://wrong.example"})),
        ("missing JWT audience", lambda docs: docs[3]["data"].update({"JWT_AUDIENCE": ""})),
        ("missing readiness probe", lambda docs: docs[2]["spec"]["template"]["spec"]["containers"][0].pop("readinessProbe")),
    ]
    for name, mutate in cases:
        docs = copy.deepcopy(baseline)
        mutate(docs)
        try:
            validate(docs)
        except ContractError:
            continue
        fail(f"self-test accepted invalid case: {name}")
    print(f"Auth GitOps contract self-test passed ({len(cases) + 1} cases).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rendered_manifest", nargs="?", help="kubectl-kustomize rendered YAML file")
    parser.add_argument("--self-test", action="store_true", help="run offline positive and negative regression cases")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.rendered_manifest:
        parser.error("rendered_manifest is required unless --self-test is used")

    path = Path(args.rendered_manifest)
    if not path.is_file() or path.stat().st_size == 0:
        fail(f"rendered manifest missing or empty: {path}")
    try:
        objects = [obj for obj in yaml.safe_load_all(path.read_text(encoding="utf-8")) if isinstance(obj, dict)]
    except yaml.YAMLError as exc:
        fail(f"rendered YAML could not be parsed: {exc}")
    image = validate(objects)
    print(f"Auth GitOps contract validated. Effective image: {image}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        print(f"::error::Auth GitOps contract failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
