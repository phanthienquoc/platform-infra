#!/usr/bin/env python3
"""Guard the checksum-pinned cert-manager bootstrap outside Kustomize."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
KUSTOMIZATION = ROOT / "platform/cert-manager/kustomization.yaml"
PREPARE_SCRIPT = ROOT / "scripts/prepare-cert-manager-manifest.sh"
RECONCILE_SCRIPT = ROOT / "scripts/reconcile-vps.sh"
VALIDATION_WORKFLOW = ROOT / ".github/workflows/validate-manifests.yml"
GITIGNORE = ROOT / ".gitignore"

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
    prepare = PREPARE_SCRIPT.read_text()
    reconcile = RECONCILE_SCRIPT.read_text()
    workflow = VALIDATION_WORKFLOW.read_text()
    gitignore = GITIGNORE.read_text()

    require(
        RELEASE_URL not in kustomization and "releases/download" not in kustomization,
        "release assets must not be declared as remote Kustomize resources",
    )
    require(
        "cert-manager.yaml" in kustomization
        and "cluster-issuer.yaml" in kustomization
        and "certificates.yaml" in kustomization,
        "controller bundle and local ClusterIssuer/Certificate resources must remain in the production Kustomize tree",
    )
    require(
        f'CERT_MANAGER_VERSION="{VERSION}"' in prepare,
        "preparation script must pin the reviewed cert-manager release",
    )
    require(
        f'CERT_MANAGER_MANIFEST_SHA256="{SHA256}"' in prepare,
        "preparation script must pin the GitHub release asset SHA-256",
    )
    require(
        f'CERT_MANAGER_MANIFEST_URL="{RELEASE_URL}"' in prepare,
        "preparation script must download the exact pinned release asset",
    )
    require(
        "curl --fail --silent --show-error --location" in prepare
        and "sha256sum --check --status" in prepare,
        "release download must fail closed and pass SHA-256 verification",
    )
    require(
        'if [[ "$DEST" != "$EXPECTED_DEST" ]]' in prepare
        and 'if [[ -e "$DEST" ]]' in prepare,
        "preparation script must constrain the destination and refuse overwrite",
    )

    require(
        'bash scripts/prepare-cert-manager-manifest.sh "$CERT_MANAGER_MANIFEST_FILE"' in reconcile,
        "GitOps reconciliation must prepare the verified local resource before diff/apply",
    )
    require(
        'rm -f "$CERT_MANAGER_MANIFEST_FILE"' in reconcile
        and "trap cleanup EXIT" in reconcile,
        "generated manifest must be removed after reconciliation",
    )
    require(
        "run_kubectl diff -k environments/prod" in reconcile
        and "run_kubectl apply -k environments/prod" in reconcile,
        "production diff and apply must remain behind the existing restricted wrapper",
    )
    require(
        "run_kubectl diff -f" not in reconcile
        and "run_kubectl apply -f" not in reconcile,
        "do not introduce an unverified wrapper operation or a second apply path",
    )
    plan = reconcile.split("  plan)", 1)[1].split("  apply)", 1)[0]
    apply = reconcile.split("  apply)", 1)[1].split("  *)", 1)[0]
    require(
        plan.find("prepare_cert_manager_manifest") < plan.find("run_diff"),
        "plan must prepare the release asset before Kustomize diff",
    )
    require(
        apply.find("prepare_cert_manager_manifest") < apply.find("run_diff"),
        "apply must prepare the release asset before preflight diff",
    )

    render = workflow.split("- name: Render production manifests", 1)[1].split(
        "- name: Validate Auth GitOps contract validator", 1
    )[0]
    require(
        "bash scripts/prepare-cert-manager-manifest.sh" in render
        and "kubectl kustomize environments/prod" in render
        and "trap 'rm -f" in render,
        "offline manifest validation must prepare and clean the pinned asset before rendering",
    )
    require(
        "platform/cert-manager/cert-manager.yaml" in gitignore,
        "generated release asset must be ignored to protect the clean worktree",
    )


if __name__ == "__main__":
    validate()
    if "--self-test" in sys.argv:
        print("cert-manager bootstrap contract self-test passed.")
    else:
        print("cert-manager bootstrap contract passed.")
