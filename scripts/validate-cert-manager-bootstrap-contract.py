#!/usr/bin/env python3
"""Guard the checksum-pinned cert-manager bootstrap outside Kustomize."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
KUSTOMIZATION = ROOT / "platform/cert-manager/kustomization.yaml"
RECONCILE_SCRIPT = ROOT / "scripts/reconcile-vps.sh"

VERSION = "v1.21.1"
SHA256 = "5f6a499b8c1857d57f560f536e0dcc830914b45c420899fe7ad0692c8624e408"
RELEASE_URL = (
    "https://github.com/cert-manager/cert-manager/releases/download/"
    f"{VERSION}/cert-manager.yaml"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"cert-manager bootstrap contract failed: {message}")


def validate() -> None:
    kustomization = KUSTOMIZATION.read_text()
    reconcile = RECONCILE_SCRIPT.read_text()

    require(
        RELEASE_URL not in kustomization
        and "releases/download" not in kustomization,
        "release assets must not be declared as Kustomize resources",
    )
    require(
        "cluster-issuer.yaml" in kustomization
        and "certificates.yaml" in kustomization,
        "local ClusterIssuer and Certificate resources must remain in Kustomize",
    )
    require(
        f'CERT_MANAGER_VERSION="{VERSION}"' in reconcile,
        "reconciliation must pin the reviewed cert-manager release",
    )
    require(
        f'CERT_MANAGER_MANIFEST_SHA256="{SHA256}"' in reconcile,
        "reconciliation must pin the GitHub release asset SHA-256",
    )
    require(
        f'CERT_MANAGER_MANIFEST_URL="{RELEASE_URL}"' in reconcile,
        "reconciliation must download the exact pinned release asset",
    )
    require(
        "curl --fail --silent --show-error --location" in reconcile
        and "sha256sum --check --status" in reconcile,
        "release download must fail closed and pass SHA-256 verification",
    )

    diff_asset = reconcile.find('run_kubectl diff -f "$CERT_MANAGER_MANIFEST_FILE"')
    diff_root = reconcile.find("run_kubectl diff -k environments/prod")
    apply_asset = reconcile.find('run_kubectl apply -f "$CERT_MANAGER_MANIFEST_FILE"')
    apply_root = reconcile.find("run_kubectl apply -k environments/prod")
    require(
        0 <= diff_asset < diff_root,
        "release asset must be diffed before the production Kustomize tree",
    )
    require(
        0 <= apply_asset < apply_root,
        "cert-manager controllers/CRDs must be applied before local CR resources",
    )
    require(
        reconcile.count("prepare_cert_manager_manifest") >= 3,
        "both plan and apply paths must prepare the verified release asset",
    )
    require(
        re.search(r"trap cleanup EXIT", reconcile) is not None,
        "temporary downloaded release artifacts must be removed on exit",
    )


if __name__ == "__main__":
    validate()
    if "--self-test" in sys.argv:
        print("cert-manager bootstrap contract self-test passed.")
    else:
        print("cert-manager bootstrap contract passed.")
