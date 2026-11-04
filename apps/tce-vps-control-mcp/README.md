# TCE VPS Control MCP

A host-local, Streamable HTTP MCP server for controlled operations on the TCE VPS and k3s cluster.

## Security model

- Runs as the unprivileged `tce-mcp` OS account, never as root.
- Binds to `127.0.0.1:8765` by default. Publish it only through an authenticated HTTPS reverse proxy or a supported Secure MCP Tunnel; do not expose port 8765 directly.
- Requires a 256-bit random bearer token. Keep it in `/etc/tce-vps-control-mcp/server.env`; never put it in Git, chat, workflow logs, or shell history.
- Shell execution is arbitrary within the OS permissions of `tce-mcp`, with working-directory roots, timeouts, output limits, command deny rules, and audit records. It blocks direct `sudo`, `kubectl`, and `docker` access.
- Docker is reached only through a root-owned argument-validating wrapper and a single sudoers entry. Do not add the service user to the `docker` group (Docker socket access is effectively root).
- Kubernetes uses a dedicated service account and narrow RBAC. It can inspect cluster resources and patch Deployments only for rollout restart.
- Mutating MCP tools require a `confirmedByUser: true` field. This is an additional guard, not a substitute for ChatGPT's own action approval or operator review.
- Every operation writes a JSONL audit record. Command text is hashed rather than stored.

## Tools

| Tool | Access |
|---|---|
| `host_status` | Read host uptime, memory, disk and kernel |
| `shell_execute` | Arbitrary unprivileged shell in configured working roots |
| `docker_ps` | List Docker containers |
| `docker_logs` | Read container logs |
| `docker_restart` | Restart one container (explicit confirmation required) |
| `k8s_get` | Read pods, deployments, services, nodes, namespaces, events and replicasets |
| `k8s_logs` | Read pod logs |
| `k8s_rollout_restart` | Restart a Deployment (explicit confirmation required) |
| `systemd_status` | Read status of k3s, containerd, docker, nginx or cloudflared |

The server intentionally does not expose an unrestricted root shell, arbitrary systemctl, raw Docker socket, arbitrary Kubernetes patch, secret reads, or host reboot/format operations.

## Requirements

- Ubuntu 22.04+ (tested design target)
- Node.js 22+
- npm
- systemd
- sudo
- Docker CLI/daemon for Docker tools
- kubectl and a dedicated kubeconfig for Kubernetes tools

## Install on the VPS

From a trusted checkout of `platform-infra`:

```bash
cd apps/tce-vps-control-mcp
sudo bash scripts/install.sh
```

The installer creates separate MCP and shell accounts, installs the Node app and root-owned Docker wrapper, configures sudoers, creates a random bearer token if no environment file exists, and starts the systemd service.

The installer resolves dependencies from the pinned semver ranges in `package.json` during installation. For fully reproducible production builds, generate and commit a `package-lock.json` after validating the dependency tree.

Check local health:

```bash
curl -fsS http://127.0.0.1:8765/healthz
sudo systemctl status tce-vps-control-mcp
sudo journalctl -u tce-vps-control-mcp -n 100 --no-pager
```

## Kubernetes access

Apply the RBAC manifest using an existing cluster administrator:

```bash
kubectl apply -f ops/k8s-rbac.yaml
kubectl -n tce-ops create token tce-vps-control-mcp --duration=24h
```

Create a dedicated kubeconfig at `/etc/tce-vps-control-mcp/kubeconfig` using the cluster API endpoint, CA certificate and service-account token. Do not copy the administrator kubeconfig. Set owner `root:tce-mcp`, mode `0640`, then restart the service. Rotate the token before expiry. The MCP server cannot access Kubernetes until this is configured.

## Remote ChatGPT connection

The MCP endpoint is `https://YOUR-APPROVED-HOST/mcp`. Keep the Node listener on loopback and configure an HTTPS reverse proxy or Secure MCP Tunnel. Configure bearer authentication with the token from `server.env`. Never expose the service on a public plain-HTTP port.

ChatGPT custom MCP connections are currently documented for Business and Enterprise/Edu workspaces, not personal Go accounts. Therefore this server can be built and deployed independently, but a ChatGPT Go account cannot currently connect this custom MCP directly. Verify current plan support before publishing the endpoint.

## Operational checks

```bash
sudo -u tce-mcp /usr/bin/sudo -n /usr/local/sbin/tce-mcp-docker ps
sudo -u tce-mcp test -r /etc/tce-vps-control-mcp/kubeconfig
sudo visudo -cf /etc/sudoers.d/tce-vps-control-mcp
```

Review audit events at `/var/log/tce-vps-control-mcp/audit.jsonl`. Rotate the bearer token immediately if it is exposed. Keep the server private and restrict reverse-proxy access to the intended ChatGPT integration.
