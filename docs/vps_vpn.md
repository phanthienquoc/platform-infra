# VPS VPN (WireGuard)

> **Status:** deployment guide, not a claim that VPN has been installed or tested on the VPS.
>
> The repository has Kubernetes/k3s workloads and firewall rules. Do not flush iptables/nftables, restart networking, or change cluster firewall rules as part of this setup. Run the preflight checks first and preserve an SSH session.

## Recommendation

Use **WireGuard on the VPS host** for a small personal VPN. It is lightweight and suitable for a typical Ubuntu VPS, provided the provider allows UDP ingress and the host has enough free resources. This document does not assume that the attached VPS assessment has passed; validate the actual VPS before installing.

For a host already running k3s, do not install WireGuard inside a workload pod and do not change Kubernetes pod/service CIDRs. Use a dedicated VPN subnet that does not overlap with the VPS LAN, Kubernetes pod/service ranges, or the networks used by clients.

## 1. Preflight — read-only

Run on the VPS over SSH:

```bash
set -eu
printf '\n== OS ==\n'
cat /etc/os-release
printf '\n== CPU / memory ==\n'
nproc
free -h
printf '\n== Disk ==\n'
df -h /
printf '\n== Addresses and routes ==\n'
ip -brief address
ip route
printf '\n== Existing listeners ==\n'
sudo ss -lntup
printf '\n== Firewall tools ==\n'
command -v ufw || true
command -v nft || true
command -v iptables || true
printf '\n== Kubernetes presence ==\n'
command -v kubectl || true
command -v k3s || true
```

Proceed only after confirming:
- The VPS is a supported Linux distribution (commands below target Ubuntu/Debian).
- You have provider-console access or another recovery path in case SSH/firewall access is interrupted.
- The provider firewall/security group can allow **UDP 51820**.
- You know the public IPv4 address or DNS name clients will connect to.
- The proposed VPN subnet (example below: `10.66.66.0/24`) does not overlap with existing routes.
- You have reviewed existing UFW/nftables/iptables and k3s networking. Do not reset them.

## 2. Install WireGuard

Only after preflight and firewall review:

```bash
sudo apt-get update
sudo apt-get install -y wireguard
```

Enable IPv4 forwarding persistently (needed for routing client traffic through the VPS; not required for a tunnel that only accesses the VPS itself):

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wireguard-forward.conf
sudo sysctl --system
sysctl net.ipv4.ip_forward
```

If the VPS is also an active Kubernetes node, assess forwarding and firewall implications before applying this setting. Do not add broad forwarding or NAT rules without first identifying the actual public interface and the existing firewall manager.

## 3. Generate server keys

```bash
sudo install -d -m 700 /etc/wireguard
sudo sh -c 'umask 077; wg genkey > /etc/wireguard/server.key'
sudo sh -c 'wg pubkey < /etc/wireguard/server.key > /etc/wireguard/server.pub'
sudo chmod 600 /etc/wireguard/server.key
sudo cat /etc/wireguard/server.pub
```

Keep `/etc/wireguard/server.key` private. Never commit private keys, client configuration files, QR codes, or preshared keys to GitHub.

## 4. Create the server configuration

Determine the public interface first:

```bash
ip route get 1.1.1.1
```

Create `/etc/wireguard/wg0.conf` with your editor. Replace the placeholders; do not paste literal placeholder text:

```ini
[Interface]
Address = 10.66.66.1/24
ListenPort = 51820
PrivateKey = <contents of /etc/wireguard/server.key>
# Add reviewed PostUp/PostDown firewall rules only after identifying the
# public interface and the host's existing firewall manager.
```

Secure the file:

```bash
sudo chmod 600 /etc/wireguard/wg0.conf
```

The configuration above creates the tunnel interface but intentionally does not enable client internet egress. Full-tunnel routing requires reviewed forwarding/NAT rules and a client DNS choice. For access only to the VPS or a private subnet, configure only the intended routes.

## 5. Firewall and provider network

1. In the VPS provider firewall/security group, allow inbound **UDP 51820**.
2. Keep the existing SSH port accessible from your trusted source IP before changing host firewall rules.
3. Add a narrow host-firewall rule for UDP 51820 using the firewall manager already in use.
4. Do **not** run `iptables -F`, `iptables -t nat -F`, `nft flush ruleset`, or reset UFW. These can disrupt production services and Kubernetes networking.
5. Do not expose WireGuard's private key or any client private key in command output, issue trackers, logs, or Git.

If UFW is already the intended firewall manager and you have verified its current rules, the narrow allow rule is:

```bash
sudo ufw allow 51820/udp
sudo ufw status numbered
```

Do not enable UFW blindly on a production VPS; first ensure the current SSH port and required application/Kubernetes ports are allowed. If nftables or k3s-managed rules are in use, adapt the rule to the existing configuration instead of mixing firewall managers.

## 6. Start and verify

After configuration and firewall review:

```bash
sudo systemctl enable --now wg-quick@wg0
sudo systemctl --no-pager --full status wg-quick@wg0
sudo wg show
ip address show wg0
sudo journalctl -u wg-quick@wg0 -n 100 --no-pager
```

Rollback (run from the VPS console or a stable SSH session, and only if you intend to stop this VPN):

```bash
sudo systemctl disable --now wg-quick@wg0
```

Stopping WireGuard does not remove firewall rules or undo sysctl settings. Review and remove only the specific rules/settings added for this setup.

## 7. Add a client

Generate a separate key pair per device. Keep the client private key on that device. Add the client's **public** key to the server configuration:

```ini
[Peer]
PublicKey = <client public key>
AllowedIPs = 10.66.66.2/32
```

Apply peer changes with a controlled restart or a reviewed `wg syncconf` workflow. For a single personal client, use a dedicated address for each additional device (for example, `10.66.66.3/32`).

A client configuration for a tunnel to the VPS only can follow this shape:

```ini
[Interface]
PrivateKey = <client private key>
Address = 10.66.66.2/32
DNS = <trusted DNS resolver reachable by this client>

[Peer]
PublicKey = <server public key>
Endpoint = <VPS_PUBLIC_IP_OR_DNS>:51820
AllowedIPs = 10.66.66.0/24
PersistentKeepalive = 25
```

`AllowedIPs` controls what traffic uses the tunnel. Use `0.0.0.0/0` only if you intentionally want all IPv4 traffic routed through the VPN and have configured server-side forwarding/NAT and DNS accordingly. Add IPv6 routing only if it is configured and secured end-to-end.

## 8. Acceptance checklist

- [ ] VPS OS, CPU, RAM, disk, public address, and routes checked.
- [ ] VPN subnet confirmed not to overlap with existing networks.
- [ ] Provider firewall allows UDP 51820.
- [ ] Existing SSH and production/Kubernetes firewall rules preserved.
- [ ] Server private key and config are mode-restricted and not committed.
- [ ] `wg-quick@wg0` starts and `wg show` reports the interface.
- [ ] Client handshake succeeds when the client connects.
- [ ] Only intended routes traverse the tunnel; public-IP and DNS behavior verified.
- [ ] Rollback path is available.

## Operational notes

- WireGuard does not make a VPS anonymous or guarantee access to every service; the VPS public IP becomes the apparent egress IP only for traffic routed through it.
- VPN throughput depends on VPS CPU, network limits, provider policy, and client connectivity. Measure real throughput after setup.
- This document is a guide. No VPN installation, firewall modification, or connectivity test is performed by committing this file.
