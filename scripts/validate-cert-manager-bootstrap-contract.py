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
    reconcile_workflow = read(".github/workflows/reconcile-vps.yml")
    inspection_workflow = read(".github/workflows/inspect-vps.yml")
    recovery_workflow = read(".github/workflows/validate-recovery-readiness.yml")
    auth_test = read("scripts/tests/prepare-cert-manager-manifest-auth.test.sh")
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
        'if [[ -n "${GH_TOKEN:-}" ]]' in prepare
        and 'curl_args+=(--header "Authorization: Bearer ${GH_TOKEN}")' in prepare
        and 'curl "${curl_args[@]}" "$CERT_MANAGER_MANIFEST_URL" --output "$tmp_file"' in prepare,
        "release asset download must use an optional token to avoid anonymous API rate limits",
    )
    require(
        "GH_TOKEN=test-token" in auth_test
        and "Authorization: Bearer test-token" in auth_test
        and "never logged" in auth_test,
        "cert-manager release auth regression test must cover token use and log redaction",
    )

    def require_token_step(source: str, step_name: str, workflow_path: str) -> None:
        marker = f"      - name: {step_name}"
        start = source.find(marker)
        require(start >= 0, f"{workflow_path} is missing step {step_name}")
        end = source.find("\n      - name:", start + len(marker))
        if end < 0:
            end = len(source)
        require(
            "GH_TOKEN: ${{ github.token }}" in source[start:end],
            f"{workflow_path} step {step_name} must provide GH_TOKEN to the pinned release download",
        )

    require_token_step(workflow, "Render production manifests", ".github/workflows/validate-manifests.yml")
    require_token_step(workflow, "Validate network boundaries", ".github/workflows/validate-manifests.yml")
    require_token_step(staging, "Prepare checksum-verified cert-manager release", ".github/workflows/staging-dry-run.yml")
    require_token_step(reconcile_workflow, "Preflight diff", ".github/workflows/reconcile-vps.yml")
    require_token_step(reconcile_workflow, "Guard workload image changes", ".github/workflows/reconcile-vps.yml")
    require_token_step(reconcile_workflow, "Apply production manifests", ".github/workflows/reconcile-vps.yml")
    require_token_step(inspection_workflow, "Inspect VPS", ".github/workflows/inspect-vps.yml")
    require_token_step(recovery_workflow, "Validate recovery readiness", ".github/workflows/validate-recovery-readiness.yml")

    workflow_permissions = workflow.split("jobs:", 1)[0]
    report_job = workflow.split("  report-validation-failure:", 1)[1]
    require(
        "pull-requests: write" not in workflow_permissions
        and "needs: validate" in report_job
        and "permissions:\n      pull-requests: write" in report_job
        and 'gh pr comment "$PR_NUMBER" --repo "$GITHUB_REPOSITORY"' in report_job,
        "PR write permission must be isolated in the failure-comment job, not exposed to manifest validation code",
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
