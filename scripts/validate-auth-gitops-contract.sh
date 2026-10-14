#!/usr/bin/env bash
set -euo pipefail

rendered_manifest="${1:-/tmp/platform-infra-rendered.yaml}"
if [[ ! -s "$rendered_manifest" ]]; then
  echo "Rendered manifest missing or empty: $rendered_manifest" >&2
  exit 1
fi

python3 - "$rendered_manifest" <<'PY'
from pathlib import Path
import re
import sys
import yaml

path = Path(sys.argv[1])
objects = [obj for obj in yaml.safe_load_all(path.read_text()) if isinstance(obj, dict)]

def fail(message: str) -> None:
    raise SystemExit(f"Auth manifest contract failed: {message}")

ingresses = [
    obj for obj in objects
    if obj.get("kind") == "Ingress" and obj.get("metadata", {}).get("name") == "microfe-public"
]
if len(ingresses) != 1:
    fail(f"expected exactly one microfe-public Ingress, found {len(ingresses)}")
ingress = ingresses[0]
auth_rules = [rule for rule in ingress.get("spec", {}).get("rules", []) if rule.get("host") == "auth.mrcute.space"]
if len(auth_rules) != 1:
    fail(f"expected exactly one auth.mrcute.space rule, found {len(auth_rules)}")
paths = auth_rules[0].get("http", {}).get("paths", [])
if not any(
    item.get("path") == "/" and
    item.get("backend", {}).get("service", {}).get("name") == "microfe-auth" and
    item.get("backend", {}).get("service", {}).get("port", {}).get("number") == 80
    for item in paths
):
    fail("auth.mrcute.space / route must target Service microfe-auth:80")

services = [
    obj for obj in objects
    if obj.get("kind") == "Service" and obj.get("metadata", {}).get("name") == "microfe-auth"
]
if len(services) != 1:
    fail(f"expected exactly one microfe-auth Service, found {len(services)}")
if not any(
    port.get("port") == 80 and port.get("targetPort") == 4010
    for port in services[0].get("spec", {}).get("ports", [])
):
    fail("microfe-auth Service must route port 80 to container port 4010")

deployments = [
    obj for obj in objects
    if obj.get("kind") == "Deployment" and obj.get("metadata", {}).get("name") == "microfe-auth"
]
if len(deployments) != 1:
    fail(f"expected exactly one microfe-auth Deployment, found {len(deployments)}")
deployment = deployments[0]
containers = deployment.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
auth_containers = [container for container in containers if container.get("name") == "auth"]
if len(auth_containers) != 1:
    fail(f"expected one auth container, found {len(auth_containers)}")
container = auth_containers[0]
image = container.get("image", "")
if not re.fullmatch(r"ghcr\.io/phanthienquoc/auth-service/auth:(?:prod-v[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]{7,40}|[0-9a-f]{7,64})", image):
    fail(f"effective Auth image must use an immutable SHA/versioned-SHA tag; got {image!r}")
if not any(port.get("containerPort") == 4010 for port in container.get("ports", [])):
    fail("auth container must expose port 4010")

required_secret_keys = {
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "JWT_SECRET",
    "MFA_ENCRYPTION_KEY",
}
secret_refs = {
    (entry.get("name"), entry.get("valueFrom", {}).get("secretKeyRef", {}).get("key"))
    for entry in container.get("env", [])
}
for key in required_secret_keys:
    if (key, key) not in secret_refs:
        fail(f"runtime env {key} must come from Secret microfe-auth-secrets key {key}")
if any(
    entry.get("valueFrom", {}).get("secretKeyRef", {}).get("name") != "microfe-auth-secrets"
    for entry in container.get("env", [])
    if entry.get("valueFrom", {}).get("secretKeyRef")
):
    fail("Auth runtime secret values must be sourced only from microfe-auth-secrets")

configmaps = [
    obj for obj in objects
    if obj.get("kind") == "ConfigMap" and obj.get("metadata", {}).get("name") == "microfe-auth-config"
]
if len(configmaps) != 1:
    fail(f"expected exactly one microfe-auth-config ConfigMap, found {len(configmaps)}")
config = configmaps[0].get("data", {})
if config.get("JWT_ISSUER") != "https://auth.mrcute.space":
    fail("JWT_ISSUER must match https://auth.mrcute.space")
audiences = {part.strip() for part in config.get("JWT_AUDIENCE", "").split(",") if part.strip()}
if not {"tce-dashboard", "media-generation"}.issubset(audiences):
    fail("JWT_AUDIENCE must include tce-dashboard and media-generation")

if not container.get("startupProbe") or not container.get("readinessProbe") or not container.get("livenessProbe"):
    fail("startup, readiness and liveness probes are required")
print(f"Auth GitOps contract validated. Effective image: {image}")
PY
