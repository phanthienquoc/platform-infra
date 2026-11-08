#!/usr/bin/env python3
"""Guard the checksum-pinned cert-manager bootstrap across every render/apply path."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v1.21.1"
SHA256 = "5f6a499b8c1857d57f560f536e0dcc830914b45c420899fe7ad0692c8624e408"
RELEASE_URL = "https://api.github.com/repos/cert-manager/cert-manager/releases/assets/494156333"


def read(path: str) -> str:
    return (ROOT / path).read_text()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"cert-manager bootstrap contract failed: {message}")


def validate() -> None:
    kustomization = read("platform/cert-manager/kustomization.yaml")
    prepare = read("scripts/prepare-cert-manager-manifest.sh")
    reconcile = read("scripts/reconcile-vps.sh")
    workflow = read(".github/workflows/validate-manifests.yml")
    staging = read(".github/workflows/staging-dry-run.yml")
    wrapper = read("scripts/bootstrap-runner.sh")
    recovery = read("scripts/validate-recovery-readiness.sh")
    inspection = read("scripts/inspect-vps.sh")
    gitignore = read(".gitignore")

    require(
        RELEASE_URL not in kustomization and "releases/download" not in kustomization,
        "release assets must not be declared as remote Kustomize resources",
    )
    resource_order = [
        kustomization.find("cert-manager.yaml"),
        kustomization.find("cluster-issuer.yaml"),
        kustomization.find("certificates.yaml"),
    ]
    require(
        all(index >= 0 for index in resource_order)
        and resource_order == sorted(resource_order),
        "controller bundle must precede local ClusterIssuer/Certificate resources",
    )
    require(
        f'CERT_MANAGER_VERSION="{VERSION}"' in prepare
        and f'CERT_MANAGER_MANIFEST_SHA256="{SHA256}"' in prepare
        and f'CERT_MANAGER_MANIFEST_URL="{RELEASE_URL}"' in prepare,
        "preparation script must pin the exact reviewed release and asset digest",
    )
    require(
        "curl --fail --silent --show-error --location" in prepare
        and '--header "Accept: application/octet-stream"' in prepare
        and "sha256sum --check --status" in prepare,
        "release download must fail closed and pass SHA-256 verification",
    )
    require(
        'if [[ "$DEST" != "$EXPECTED_DEST" ]]' in prepare
        and 'if [[ -e "$DEST" ]]' in prepare
        and "Refusing to overwrite an existing cert-manager manifest" in prepare,
        "preparation script must constrain the destination and refuse unverified overwrite",
    )

    require(
        'bash scripts/prepare-cert-manager-manifest.sh "$CERT_MANAGER_MANIFEST_FILE"' in reconcile
        and "CERT_MANAGER_MANIFEST_PREPARED=true" in reconcile
        and 'rm -f "$CERT_MANAGER_MANIFEST_FILE"' in reconcile
        and "trap cleanup EXIT" in reconcile,
        "GitOps reconciliation must prepare and clean the generated asset",
    )
    require(
        "run_kubectl diff -k environments/prod" in reconcile
        and "run_kubectl apply -k environments/prod" in reconcile
        and "run_kubectl diff -f" not in reconcile
        and "run_kubectl apply -f" not in reconcile,
        "production diff/apply must stay behind the existing restricted Kustomize wrapper",
    )
    plan = reconcile.split("  plan)", 1)[1].split("  apply)", 1)[0]
    apply = reconcile.split("  apply)", 1)[1].split("  *)", 1)[0]
    require(
        plan.find("prepare_cert_manager_manifest") < plan.find("run_diff")
        and apply.find("prepare_cert_manager_manifest") < apply.find("run_diff"),
        "both read-only plan and explicit apply must prepare the asset before diff",
    )

    callers = {
        "scripts/validate-manifests.sh": "kubectl kustomize environments/prod",
        "scripts/validate-network-boundaries.sh": "kubectl kustomize environments/prod",
        "scripts/validate-recovery-readiness.sh": "run_kubectl kustomize environments/prod",
        "scripts/guard-reconcile-images.sh": "sudo /usr/local/sbin/platform-kubectl diff -k environments/prod",
        "scripts/inspect-vps.sh": 'sudo "$KCTL" diff -k environments/prod',
    }
    for path, operation in callers.items():
        source = read(path)
        require(
            "bash scripts/prepare-cert-manager-manifest.sh" in source
            and operation in source,
            f"{path} must prepare the pinned asset before its production Kustomize operation",
        )

    render_step = workflow.split("- name: Render production manifests", 1)[1].split(
        "- name: Validate Auth GitOps contract validator", 1
    )[0]
    require(
        "bash scripts/prepare-cert-manager-manifest.sh" in render_step
        and "kubectl kustomize environments/prod" in render_step
        and "prepared=true" in render_step,
        "manifest validation workflow must prepare the asset before rendering",
    )
    require(
        "Prepare checksum-verified cert-manager release" in staging
        and "Clean up checksum-verified cert-manager release" in staging,
        "staging dry-run must prepare and clean the generated asset",
    )
    require(
        "bash scripts/decommission-stock-media-namespaces.sh plan" in inspection
        and "bash scripts/decommission-stock-media-namespaces.sh delete" not in inspection,
        "routine inspection may run only the read-only Stock/Media decommission preflight",
    )
    require(
        'bash scripts/prepare-cert-manager-manifest.sh "$CERT_MANAGER_MANIFEST_FILE"' in recovery
        and 'KUBECTL="${KUBECTL:-sudo /usr/local/bin/k3s kubectl}"' in recovery
        and "apply --dry-run=server -k environments/prod" in recovery
        and "apply -k environments/prod" not in recovery,
        "recovery readiness must prepare the asset and keep its only apply operation server-side dry-run",
    )
    require(
        "apply -k environments/prod" in wrapper
        and "diff -k environments/prod" in wrapper,
        "the host wrapper must retain its existing GitOps-only production operations",
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
