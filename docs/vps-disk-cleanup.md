# VPS disk and image cleanup

## Inspect first

```bash
df -h /
sudo du -xhd1 /var/lib/rancher/k3s /var/lib/docker /var/log 2>/dev/null | sort -h
sudo docker system df
sudo crictl images
sudo crictl ps -a
```

## Immediate conservative cleanup

The helper is dry-run by default and operates only on K3s/containerd images that:
- are not referenced by any Pod spec (init, regular, or ephemeral containers);
- are not referenced by any existing CRI container, including stopped containers;
- are not pinned;
- can be resolved unambiguously from the local CRI image inventory.

It keeps the newest 10 unused tagged images by default. It does not run Docker prune, remove volumes, remove logs, delete runner workspaces, restart services, or delete Kubernetes resources.

Run a preview:

```bash
cd /opt/platform-infra
DRY_RUN=true KEEP_UNUSED_IMAGES=10 sudo -E bash scripts/cleanup-k3s-images.sh
```

Run deletion after reviewing the preview:

```bash
DRY_RUN=false KEEP_UNUSED_IMAGES=10 sudo -E bash scripts/cleanup-k3s-images.sh
```

The weekly GitHub Actions workflow `.github/workflows/vps-image-cleanup.yml` runs in dry-run mode by default when scheduled (schedule resolves dry_run to false only if inputs missing in workflow expression—see schedule configuration). Manual dispatch defaults to dry-run. Production cleanup must remain opt-in; schedule is report-only.

## Other safe space recovery

```bash
sudo apt-get clean
sudo journalctl --vacuum-time=14d
```

Review impact before running either command. Do not use `docker system prune -a --volumes`, `crictl rmi --prune`, delete `/var/lib/rancher/k3s` manually, or remove runner work directories.
