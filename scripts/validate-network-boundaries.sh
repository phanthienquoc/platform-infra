#!/usr/bin/env bash
set -euo pipefail

output="${1:-/tmp/platform-infra-network.yaml}"
kubectl kustomize environments/prod > "$output"

python3 - "$output" <<'PY'
import sys
from pathlib import Path
import yaml

path = Path(sys.argv[1])
docs = list(yaml.safe_load_all(path.read_text()))
services = [d for d in docs if isinstance(d, dict) and d.get("kind") == "Service"]
ingresses = [d for d in docs if isinstance(d, dict) and d.get("kind") == "Ingress"]

if not services:
    raise SystemExit("Expected application Services were not rendered.")

bad_services = [
    f"{d.get('metadata', {}).get('namespace', '-')}/{d.get('metadata', {}).get('name', '-')}"
    for d in services
    if d.get("spec", {}).get("type", "ClusterIP") != "ClusterIP"
]
if bad_services:
    raise SystemExit("Non-ClusterIP Services found: " + ", ".join(bad_services))

allowed_hosts = {
    "tce.mrcute.space",
    "mrcute.space",
    "www.mrcute.space",
    "admin.mrcute.space",
    "api.mrcute.space",
}
hosts = []
for ingress in ingresses:
    for rule in ingress.get("spec", {}).get("rules", []) or []:
        host = rule.get("host")
        if host:
            hosts.append(host)

unexpected = sorted(set(hosts) - allowed_hosts)
if unexpected:
    raise SystemExit("Unexpected externally routable hosts: " + ", ".join(unexpected))

if len(ingresses) != 2:
    raise SystemExit(f"Expected exactly 2 production Ingress resources, found {len(ingresses)}.")

print(
    f"Validated network boundaries in {output}: "
    f"{len(services)} Services are internal ClusterIP, "
    f"{len(ingresses)} Ingress resources expose only approved hosts."
)
PY
