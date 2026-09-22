# Self-hosted runner

This repository uses a repository-level GitHub Actions self-hosted runner on the K3s VPS.

## Bootstrap

1. In GitHub: Settings -> Actions -> Runners -> New self-hosted runner.
2. Select Linux / ARM64 and generate the short-lived registration token.
3. On the VPS, clone or update this repository on `master`.
4. Run the bootstrap command shown in the implementation handoff.

The registration token is short-lived and must never be committed or pasted into source control.

## Labels

`self-hosted`, `linux`, `arm64`, `platform-infra`, `k3s`, `vps`

## Safety

- Runner workflows target `master` only.
- Pull requests must not execute on the production runner.
- Initial cluster access is read-only through `/usr/local/sbin/platform-kubectl`.
- Reconciliation is explicitly gated and performs no mutation in this phase.
