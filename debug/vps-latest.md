# VPS inspection

Generated: 2026-11-14T16:56:20+00:00

## Host
Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       3.6Gi       2.2Gi        85Mi        17Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   26G   20G  57% /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   26G   20G  57% /
disk_pressure: normal (57%)
 16:56:20 up 197 days,  2:46,  0 users,  load average: 0.19, 0.27, 0.27

### Top disk consumers (best-effort, runner-readable paths)
4.0K	/var/lib/docker
4.0K	/var/lib/rancher/k3s/agent
4.0K	/var/lib/rancher/k3s/server
4.0K	/var/lib/rancher/k3s/storage
4.0K	/var/log/dist-upgrade
4.0K	/var/log/landscape
4.0K	/var/log/letsencrypt
4.0K	/var/log/private
4.0K	/var/log/unattended-upgrades
12K	/var/log/pods
72K	/var/log/unified-monitoring-agent
76K	/var/log/containers
172K	/var/log/apt
18M	/var/log/oracle-cloud-agent
236M	/var/lib/rancher/k3s
236M	/var/lib/rancher/k3s/data
1.7G	/var/log/journal
2.0G	/var/log

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
1057701 /opt/media-actions-runner/bin/Runner.Listener run --startuptype service
1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
1543653 /opt/actions-runner/bin/Runner.Worker spawnclient 154 161
  actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service loaded    active   running GitHub Actions Runner (phanthienquoc-media-generation.media-generation-k3s-01)
  actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service           loaded    active   running GitHub Actions Runner (phanthienquoc-platform-infra.platform-k3s-01)
runner_service: active
runner_service_enabled: enabled
runner_policy: platform-kubectl policy: rollout-status-v15-core-workloads

## Docker
Docker version 29.1.3, build f52814d
Server=29.1.3 RootDir=/var/lib/docker
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          20        11        9.195GB   5.773GB (62%)
Containers      12        12        2.052MB   0B (0%)
Local Volumes   5         3         66.2MB    66.18MB (99%)
Build Cache     31        0         519.4MB   154.4MB

## Updates
Listing...
apparmor/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
cloud-init/jammy-updates 26.1-0ubuntu1~22.04.1 all [upgradable from: 25.2-0ubuntu1~22.04.1]
containerd.io/jammy 2.4.2-4~ubuntu.22.04~jammy arm64 [upgradable from: 2.2.1-1~ubuntu.22.04~jammy]
distro-info/jammy-updates 1.1ubuntu0.3 arm64 [upgradable from: 1.1ubuntu0.2]
docker-buildx-plugin/jammy 0.39.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 0.30.1-1~ubuntu.22.04~jammy]
docker-ce-cli/jammy 5:29.9.3-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce-rootless-extras/jammy 5:29.9.3-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce/jammy 5:29.9.3-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-compose-plugin/jammy 5.7.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5.0.1-1~ubuntu.22.04~jammy]
fwupd/jammy-updates 2.0.20-1ubuntu2~22.04.2 arm64 [upgradable from: 1.7.9-1~22.04.3]
iproute2/jammy-updates 5.15.0-1ubuntu2.2 arm64 [upgradable from: 5.15.0-1ubuntu2]
landscape-common/jammy-updates 23.02-0ubuntu1~22.04.7 arm64 [upgradable from: 23.02-0ubuntu1~22.04.6]
libapparmor1/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
libaudit-common/jammy-updates 1:3.0.7-1ubuntu0.1 all [upgradable from: 1:3.0.7-1build1]
libaudit1/jammy-updates 1:3.0.7-1ubuntu0.1 arm64 [upgradable from: 1:3.0.7-1build1]
libglib2.0-0/jammy-updates 2.72.4-0ubuntu2.11 arm64 [upgradable from: 2.72.4-0ubuntu2.10]
libglib2.0-bin/jammy-updates 2.72.4-0ubuntu2.11 arm64 [upgradable from: 2.72.4-0ubuntu2.10]
libglib2.0-data/jammy-updates 2.72.4-0ubuntu2.11 all [upgradable from: 2.72.4-0ubuntu2.10]
libjcat1/jammy-updates 0.2.3-1~ubuntu0.22.04.1 arm64 [upgradable from: 0.1.9-1]
libk5crypto3/jammy-updates 1.19.2-2ubuntu0.10 arm64 [upgradable from: 1.19.2-2ubuntu0.8]
libldap-2.5-0/jammy-updates 2.5.20+dfsg-0ubuntu0.22.04.1 arm64 [upgradable from: 2.5.19+dfsg-0ubuntu0.22.04.1]
libldap-common/jammy-updates 2.5.20+dfsg-0ubuntu0.22.04.1 all [upgradable from: 2.5.19+dfsg-0ubuntu0.22.04.1]
libnetplan0/jammy-updates 0.107.1-3ubuntu0.22.04.5 arm64 [upgradable from: 0.106.1-7ubuntu0.22.04.4]
libnftables1/jammy-updates 1.0.2-1ubuntu3.1 arm64 [upgradable from: 1.0.2-1ubuntu3]
libopeniscsiusr/jammy-updates 2.1.5-1ubuntu1.3 arm64 [upgradable from: 2.1.5-1ubuntu1.1]
libxmlb2/jammy-updates 0.3.24-1~ubuntu0.22.04.1 arm64 [upgradable from: 0.3.6-2build1]
lshw/jammy-updates 02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1 arm64 [upgradable from: 02.19.git.2021.06.19.996aaad9c7-2build1]
nano/jammy-updates 6.2-1ubuntu0.3 arm64 [upgradable from: 6.2-1ubuntu0.2]
netplan.io/jammy-updates 0.107.1-3ubuntu0.22.04.5 arm64 [upgradable from: 0.106.1-7ubuntu0.22.04.4]
nftables/jammy-updates 1.0.2-1ubuntu3.1 arm64 [upgradable from: 1.0.2-1ubuntu3]
open-iscsi/jammy-updates 2.1.5-1ubuntu1.3 arm64 [upgradable from: 2.1.5-1ubuntu1.1]
open-vm-tools/jammy-updates 2:12.3.5-3~ubuntu0.22.04.4 arm64 [upgradable from: 2:12.3.5-3~ubuntu0.22.04.3]
python3-attr/jammy-updates 21.2.0-1ubuntu1 all [upgradable from: 21.2.0-1]
python3-distro-info/jammy-updates 1.1ubuntu0.3 all [upgradable from: 1.1ubuntu0.2]
python3-distupgrade/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
snapd/jammy-updates 2.78+ubuntu22.04 arm64 [upgradable from: 2.76.3+ubuntu22.04.1]
sosreport/jammy-updates 4.11.2-0ubuntu0~22.04.1 arm64 [upgradable from: 4.9.2-0ubuntu0~22.04.1]
tmux/jammy-updates 3.2a-4ubuntu0.3 arm64 [upgradable from: 3.2a-4ubuntu0.2]
ubuntu-advantage-tools/jammy-updates 38ubuntu0~22.04 all [upgradable from: 37.2ubuntu~22.04.1]
ubuntu-minimal/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-pro-client-l10n/jammy-updates 38ubuntu0~22.04 arm64 [upgradable from: 37.2ubuntu~22.04.1]
ubuntu-pro-client/jammy-updates 38ubuntu0~22.04 arm64 [upgradable from: 37.2ubuntu~22.04.1]
ubuntu-release-upgrader-core/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
ubuntu-server/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-standard/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
xfsprogs/jammy-updates 5.13.0-1ubuntu2.2 arm64 [upgradable from: 5.13.0-1ubuntu2.1]
restart_required: yes

## K3s
Client Version: v1.36.3+k3s1
Kustomize Version: v5.8.1
NAME         STATUS   ROLES           AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION              CONTAINER-RUNTIME
tce-k3s-01   Ready    control-plane   84d   v1.36.3+k3s1   10.0.0.120    <none>        Ubuntu 22.04.5 LTS   6.8.0-1049-oracle (arm64)   containerd://2.3.2-k3s2
NAME               STATUS   AGE
cert-manager       Active   81d
default            Active   84d
k3s-debug          Active   37d
kube-node-lease    Active   84d
kube-public        Active   84d
kube-system        Active   84d
media-prod         Active   45d
microfe-platform   Active   39d
stock-prod         Active   56d
tce-prod           Active   84d
NAMESPACE          NAME                                        READY   STATUS             RESTARTS      AGE   IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager       cert-manager-75b96c9588-lgn7d               1/1     Running            0             81d   10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager       cert-manager-cainjector-b644b66f7-l8jdq     1/1     Running            1 (81d ago)   81d   10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager       cert-manager-webhook-76d97df888-wwq49       1/1     Running            0             81d   10.42.0.99    tce-k3s-01   <none>           <none>
kube-system        coredns-54996dc9b4-d68pf                    1/1     Running            0             84d   10.42.0.6     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-crd-mq7w8              0/1     Completed          0             84d   10.42.0.3     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-s2twj                  0/1     Completed          1 (84d ago)   84d   10.42.0.2     tce-k3s-01   <none>           <none>
kube-system        local-path-provisioner-58d557dc48-jbhhp     1/1     Running            1 (84d ago)   84d   10.42.0.5     tce-k3s-01   <none>           <none>
kube-system        metrics-server-6dc596dfb8-s2bzm             1/1     Running            0             84d   10.42.0.4     tce-k3s-01   <none>           <none>
kube-system        svclb-traefik-859779c1-7bwx2                2/2     Running            0             84d   10.42.0.7     tce-k3s-01   <none>           <none>
kube-system        traefik-59b7647586-gml84                    1/1     Running            0             84d   10.42.0.8     tce-k3s-01   <none>           <none>
media-prod         media-generation-665d86ff54-4664l           1/1     Running            0             13d   10.42.0.155   tce-k3s-01   <none>           <none>
media-prod         media-generation-frontend-58d8bbc67-lwhhf   1/1     Running            0             13d   10.42.0.154   tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-7b44b44dfb-ln4sw              1/1     Running            0             13d   10.42.0.153   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-5bc979dd77-txd28                 1/1     Running            0             13d   10.42.0.152   tce-k3s-01   <none>           <none>
microfe-platform   nats-7bc8d9f768-q682m                       1/1     Running            0             36d   10.42.0.178   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-5864bcb497-6b6hm                0/1     ErrImagePull       0             12d   10.42.0.182   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-59cddb87b7-qgkjr                0/1     ImagePullBackOff   0             12d   10.42.0.180   tce-k3s-01   <none>           <none>
stock-prod         stock-backend-57ccb8ff6-d25jq               1/1     Running            0             56d   10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-6bc874575d-xcg2j              0/1     ImagePullBackOff   0             12d   10.42.0.183   tce-k3s-01   <none>           <none>
stock-prod         stock-frontend-79c57845df-z747s             1/1     Running            0             56d   10.42.0.56    tce-k3s-01   <none>           <none>

### Pod imageID evidence
cert-manager	cert-manager-75b96c9588-lgn7d	container	cert-manager-controller	quay.io/jetstack/cert-manager-controller:v1.21.1	quay.io/jetstack/cert-manager-controller@sha256:416a2d76870d996460e62bd7f521bf14fa017be9e3e904aab92163a331fcb61a	true	0
cert-manager	cert-manager-cainjector-b644b66f7-l8jdq	container	cert-manager-cainjector	quay.io/jetstack/cert-manager-cainjector:v1.21.1	quay.io/jetstack/cert-manager-cainjector@sha256:ccf6b919ec0500745a47a910118f834f9636d0aac1ff221245cd2557ed8c7c98	true	1
cert-manager	cert-manager-webhook-76d97df888-wwq49	container	cert-manager-webhook	quay.io/jetstack/cert-manager-webhook:v1.21.1	quay.io/jetstack/cert-manager-webhook@sha256:d8b3961b51c8c7320633f8208dc46bf88aa13804d0f7cbe48a096b2c523cee42	true	0
kube-system	coredns-54996dc9b4-d68pf	container	coredns	docker.io/rancher/mirrored-coredns-coredns:1.14.6	docker.io/rancher/mirrored-coredns-coredns@sha256:900f9c109f7a33545d3c811516e8376df9019147b750f5ce3e254468769176ea	true	0
kube-system	helm-install-traefik-crd-mq7w8	container	helm	docker.io/rancher/klipper-helm:v0.13.3-build20260727	docker.io/rancher/klipper-helm@sha256:5425a2b4613d2458dbdff99218e8d487ebb59c20e7a941f061c0777070f0aac1	false	0
kube-system	helm-install-traefik-s2twj	container	helm	docker.io/rancher/klipper-helm:v0.13.3-build20260727	docker.io/rancher/klipper-helm@sha256:5425a2b4613d2458dbdff99218e8d487ebb59c20e7a941f061c0777070f0aac1	false	1
kube-system	local-path-provisioner-58d557dc48-jbhhp	container	local-path-provisioner	docker.io/rancher/local-path-provisioner:v0.0.36	docker.io/rancher/local-path-provisioner@sha256:1eba82e9c386038b4af6d69cca7519fac738c28c42735ed48ce70c882ad0d80f	true	1
kube-system	metrics-server-6dc596dfb8-s2bzm	container	metrics-server	docker.io/rancher/mirrored-metrics-server:v0.9.0	docker.io/rancher/mirrored-metrics-server@sha256:d9862115e7c7881280d3d75ca26bda8ffc0fc213315979575bf23ce9826205c0	true	0
kube-system	svclb-traefik-859779c1-7bwx2	container	lb-tcp-443	docker.io/rancher/klipper-lb:v0.4.17	docker.io/rancher/klipper-lb@sha256:910944bb0bd94f060a82a56ca1ea1c577d3e49b3473a093a47a985f32e92d94a	true	0
kube-system	svclb-traefik-859779c1-7bwx2	container	lb-tcp-80	docker.io/rancher/klipper-lb:v0.4.17	docker.io/rancher/klipper-lb@sha256:910944bb0bd94f060a82a56ca1ea1c577d3e49b3473a093a47a985f32e92d94a	true	0
kube-system	traefik-59b7647586-gml84	container	traefik	docker.io/rancher/mirrored-library-traefik:3.7.8	docker.io/rancher/mirrored-library-traefik@sha256:4299bbed850421258fc5448c2e0e6ad350981d4d335a68de11b92448aedbefe5	true	0
media-prod	media-generation-665d86ff54-4664l	container	media-generation	ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8	ghcr.io/phanthienquoc/media-generation/backend@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d	true	0
media-prod	media-generation-frontend-58d8bbc67-lwhhf	container	media-generation-frontend	ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8	ghcr.io/phanthienquoc/media-generation/frontend@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a	true	0
microfe-platform	microfe-shell-7b44b44dfb-ln4sw	container	shell	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd	true	0
microfe-platform	microfe-ws-5bc979dd77-txd28	container	ws	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d	true	0
microfe-platform	nats-7bc8d9f768-q682m	container	nats	docker.io/library/nats:2.12-alpine	docker.io/library/nats@sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6	true	0
stock-prod	stock-admin-5864bcb497-6b6hm	container	admin	ghcr.io/phanthienquoc/stockdividend/admin:12d63b4		false	0
stock-prod	stock-admin-59cddb87b7-qgkjr	container	admin	ghcr.io/phanthienquoc/stockdividend/admin:12d63b4		false	0
stock-prod	stock-backend-57ccb8ff6-d25jq	container	backend	ghcr.io/phanthienquoc/stockdividend/backend:23b2878	sha256:bcf5f7b1b660b5b93cd9d9f4f041db7e9166c89b084412fa4f66e8e4d9a43ad1	true	0
stock-prod	stock-backend-6bc874575d-xcg2j	container	backend	ghcr.io/phanthienquoc/stockdividend/backend:12d63b4		false	0
stock-prod	stock-frontend-79c57845df-z747s	container	frontend	ghcr.io/phanthienquoc/stockdividend/user:23b2878	sha256:bca44dd31869a4874a795c6e6ace51f9362731770f3ac9ca1ee8f3e608d6bf99	true	0
NAMESPACE          NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager       cert-manager                1/1     1            1           81d
cert-manager       cert-manager-cainjector     1/1     1            1           81d
cert-manager       cert-manager-webhook        1/1     1            1           81d
kube-system        coredns                     1/1     1            1           84d
kube-system        local-path-provisioner      1/1     1            1           84d
kube-system        metrics-server              1/1     1            1           84d
kube-system        traefik                     1/1     1            1           84d
media-prod         media-generation            1/1     1            1           45d
media-prod         media-generation-frontend   1/1     1            1           45d
microfe-platform   keycloak                    0/0     0            0           29d
microfe-platform   microfe-auth                0/0     0            0           39d
microfe-platform   microfe-shell               1/1     1            1           39d
microfe-platform   microfe-ws                  1/1     1            1           39d
microfe-platform   nats                        1/1     1            1           36d
stock-prod         stock-admin                 0/1     1            0           52d
stock-prod         stock-backend               1/1     1            1           56d
stock-prod         stock-frontend              1/1     0            1           56d
tce-prod           tce-frontend                0/0     0            0           81d
tce-prod           tce-service                 0/0     0            0           81d

### Persistent storage inventory
NAMESPACE   NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE   VOLUMEMODE
k3s-debug   k3s-debug-logs   Bound    pvc-9aed95ca-8365-46a4-a06a-d8f26d600456   1Gi        RWO            local-path     <unset>                 37d   Filesystem
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                      STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE   VOLUMEMODE
pvc-9aed95ca-8365-46a4-a06a-d8f26d600456   1Gi        RWO            Delete           Bound    k3s-debug/k3s-debug-logs   local-path     <unset>                          37d   Filesystem

### Stock/Media VolumeSnapshot references (names only)
stock-prod: none
media-prod: none

### Pod failure evidence
stock-prod	stock-admin-5864bcb497-6b6hm	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": no match for platform in manifest: not found
stock-prod	stock-admin-59cddb87b7-qgkjr	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": no match for platform in manifest: not found
stock-prod	stock-backend-6bc874575d-xcg2j	ErrImagePull	rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": no match for platform in manifest: not found

### Recent failure events

### TCE service diagnostics (last 2h; redacted)

### CRI image inventory
Images (repo tags, repo digests, image ID, pinned, size bytes):
docker.io/library/busybox:1.36	docker.io/library/busybox@sha256:73aaf090f3d85aa34ee199857f03fa3a95c8ede2ffd4cc2cdb5b94e566b11662	sha256:b7c873bd97bdc9046fc894e0b216c8aef31e0db4c5b761fb53022e40577ab6c0	false	1906887
docker.io/library/nats:2.12-alpine	docker.io/library/nats@sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6	sha256:3050faf8121e66a65fda010f7fa3d3d280a81c5c9e5e01fa2da4d2fa87ff7b6f	false	10627368
docker.io/rancher/klipper-lb:v0.4.17	docker.io/rancher/klipper-lb@sha256:910944bb0bd94f060a82a56ca1ea1c577d3e49b3473a093a47a985f32e92d94a	sha256:1084dac5ea9871ffa6d01fe67150e175df9c28579073cd40d2186c08b37aba50	false	5793195
docker.io/rancher/kubectl:v1.36.2	docker.io/rancher/kubectl@sha256:06c7a7a9772737494ae1e0c3af90f1b5385630c147e47c1c7cea92f4bed55fbe	sha256:db8edbebc7acc62dcdc839954b25da68044e942a600cc947d9ec0640d99289b2	false	16188528
docker.io/rancher/local-path-provisioner:v0.0.36	docker.io/rancher/local-path-provisioner@sha256:1eba82e9c386038b4af6d69cca7519fac738c28c42735ed48ce70c882ad0d80f	sha256:58d078c5467bf37b5bf5230f2a85dcfe40fc7042062ab8823757ec7822aaeb22	false	84943328
docker.io/rancher/mirrored-coredns-coredns:1.14.6	docker.io/rancher/mirrored-coredns-coredns@sha256:900f9c109f7a33545d3c811516e8376df9019147b750f5ce3e254468769176ea	sha256:fbccbf70a429fb9ce1cdb13a40ed96b16272ef763dafe050b2c0d121dd29811b	false	21239459
docker.io/rancher/mirrored-library-traefik:3.7.8	docker.io/rancher/mirrored-library-traefik@sha256:4299bbed850421258fc5448c2e0e6ad350981d4d335a68de11b92448aedbefe5	sha256:2eb085ca3ba80498cf1a2858ec007927bb21c81a6c6dc722a3cffe68bd78dc07	false	49364865
docker.io/rancher/mirrored-metrics-server:v0.9.0	docker.io/rancher/mirrored-metrics-server@sha256:d9862115e7c7881280d3d75ca26bda8ffc0fc213315979575bf23ce9826205c0	sha256:37ceda8805d2e3bca331bcdd659d9cf8d3b4075a68b288054c88e62232d52883	false	20915021
docker.io/rancher/mirrored-pause:3.10.2	docker.io/rancher/mirrored-pause@sha256:f548e0e8e3dc1896ca956272154dde3314e8cc4fde0a57577ee9fa1c63f5baf4	sha256:3884a337192318652b28de0de1aeb07f446a14f220feb5066f03e93f23ea3b60	false	268296
ghcr.io/phanthienquoc/auth-service/auth:prod-v1.0.0-ceb2688	ghcr.io/phanthienquoc/auth-service/auth@sha256:15bd51d68155a3b0cbc732e3baa148fc123aafb11b4290e6f66aa252969cdfc7	sha256:b247ff3f816a52c88fed8ef366c5c5996a6cdaccb89ee223701328c88d4c1b8d	false	71649563
ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8	ghcr.io/phanthienquoc/media-generation/backend@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d	sha256:9ab2f390fba17564cdffb00b1f300a093d6d615fedd4a53f027e8598cb20ed24	false	87947792
ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8	ghcr.io/phanthienquoc/media-generation/frontend@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a	sha256:03138627646b3a17cfafb2a7f01bf02aa5c22f78b63bf07d768db95f0b8c67f8	false	77140058
	ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	false	65079739
	ghcr.io/phanthienquoc/microfe-ws@sha256:92e6799bed0dcbeedc1c05575b6416e6e16d27beeab627b21cf1cc34b70ee631	sha256:20bce89a7a7eb9d16ebca87519e5c3e914d89d513db6747a27a9096aa73ba8c2	false	64949303
ghcr.io/phanthienquoc/stockdividend/backend:23b2878		sha256:bcf5f7b1b660b5b93cd9d9f4f041db7e9166c89b084412fa4f66e8e4d9a43ad1	false	14420347
ghcr.io/phanthienquoc/stockdividend/user:23b2878		sha256:bca44dd31869a4874a795c6e6ace51f9362731770f3ac9ca1ee8f3e608d6bf99	false	66238963
	ghcr.io/phanthienquoc/microfe-shell@sha256:40715628ad7572654ce35dab0835aa8b875d1bf9a20e9a13d257a173feac17ec	sha256:e4577fe7033fba879827b7e4df656e13434d7a70757a3400a8909cab95e55206	false	25830438
	ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	false	25830437
ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-48e3842	ghcr.io/phanthienquoc/tce-dashboard/service@sha256:214aee66dadaeb5e5acd7ac03da6d7461f68571ed2ba8ef3ef73384f7f26300a	sha256:924df0921bfdb32ebd65d6d4b05823d3dc80357f9ab4289d9eea991a96778931	false	457622464
ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-e75e338	ghcr.io/phanthienquoc/tce-dashboard/service@sha256:1dc9d8c2136598a748bbb0aafc615a71aeb3f2a5099c335859536212723f35f0	sha256:d16e4e0a92f04c63bd4777c1b3f967c70da62df6c2f50c796b8daef0cc2e7e09	false	457620530
ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-e75e338	ghcr.io/phanthienquoc/tce-dashboard/web@sha256:0416f01f3cce813ead623403ee354d7e5ff4160d1bfc24c020cfd9387da3ec27	sha256:3f6764e54b88e7d88ceca48e9386d4f5601332efad7b3777610453353edd5e6e	false	75833971
quay.io/jetstack/cert-manager-cainjector:v1.21.1	quay.io/jetstack/cert-manager-cainjector@sha256:ccf6b919ec0500745a47a910118f834f9636d0aac1ff221245cd2557ed8c7c98	sha256:187d7de7d1d04dd40dbc62236b0e75eea4a0ae336b0de824c6e27e28fb102381	false	11030656
quay.io/jetstack/cert-manager-controller:v1.21.1	quay.io/jetstack/cert-manager-controller@sha256:416a2d76870d996460e62bd7f521bf14fa017be9e3e904aab92163a331fcb61a	sha256:5283ffc3ebd6cf46ecf84f5e56730734b3de8d3de456c3a909f0077b5337c55d	false	22296047
quay.io/jetstack/cert-manager-webhook:v1.21.1	quay.io/jetstack/cert-manager-webhook@sha256:d8b3961b51c8c7320633f8208dc46bf88aa13804d0f7cbe48a096b2c523cee42	sha256:4694bc08f6c866b0820ff7e82d673029b6d48ba0aaf79af528987ca114f426ec	false	17710712
quay.io/keycloak/keycloak:26.8.1	quay.io/keycloak/keycloak@sha256:79c623a22abacf3fe6c00a5fb30f5b7843d717b234033b80995891c06116d244	sha256:4e8f716cccbf94c5461d9e6cb1f600bc74ac4d9bcfdf572511bbbc7d783d0ae5	false	264143474

### GHCR image digest coverage
status: warning
GHCR-tagged cached image(s) have no RepoDigest; local image IDs are not registry digests or promotion evidence:
ghcr.io/phanthienquoc/stockdividend/backend:23b2878
ghcr.io/phanthienquoc/stockdividend/user:23b2878
Containers (container ID, name, image reference, state):
206263dd20f559aac6a11c4ab7a838eafca36856566c058a47c6df3fe4bdf363	media-generation	sha256:9ab2f390fba17564cdffb00b1f300a093d6d615fedd4a53f027e8598cb20ed24	CONTAINER_RUNNING
d6f260529444ac3a2053434eab8d3461c2754b385a81554a790376756bb31570	media-generation-frontend	sha256:03138627646b3a17cfafb2a7f01bf02aa5c22f78b63bf07d768db95f0b8c67f8	CONTAINER_RUNNING
921cf16447b287444777e30ab96c083bf9530fb91e3e220fe4ffb0aa336572d3	ws	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	CONTAINER_RUNNING
534b404798d43154db54be31ecefbffc57b06f8379bc8e69a99004e87f9fd350	shell	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	CONTAINER_RUNNING
aed9bf4ba2d9611e57509e00c383cf4d40f0133529fdbc0f1be5df46f9ad219a	nats	sha256:3050faf8121e66a65fda010f7fa3d3d280a81c5c9e5e01fa2da4d2fa87ff7b6f	CONTAINER_RUNNING
0d776f21044d8b3393d00baa9c6fcb295c69aacbd61404d6d40daaa72d88d7a5	frontend	sha256:bca44dd31869a4874a795c6e6ace51f9362731770f3ac9ca1ee8f3e608d6bf99	CONTAINER_RUNNING
1856bd984eec928412495917f530d62ee4e791e9d4dde128ea142a43e40c8caa	backend	sha256:bcf5f7b1b660b5b93cd9d9f4f041db7e9166c89b084412fa4f66e8e4d9a43ad1	CONTAINER_RUNNING
c690bb61109ed926f14d0c08c50d099700b8af4a10f570a9305f7fbf48c016b6	cert-manager-cainjector	sha256:187d7de7d1d04dd40dbc62236b0e75eea4a0ae336b0de824c6e27e28fb102381	CONTAINER_RUNNING
c693f83138bbdb3627e9fee2ad4d4355aa4e85add01d7611a5ab344f5a3b6df1	cert-manager-controller	sha256:5283ffc3ebd6cf46ecf84f5e56730734b3de8d3de456c3a909f0077b5337c55d	CONTAINER_RUNNING
6fcabf226510cd39847563b8a8edd6f5385480ab295fb8cf90a9a9dce485f572	cert-manager-webhook	sha256:4694bc08f6c866b0820ff7e82d673029b6d48ba0aaf79af528987ca114f426ec	CONTAINER_RUNNING
e94dd30d06fd80099e243616c4f90590695e72f103ad61068e7d9637a903a1b9	local-path-provisioner	sha256:58d078c5467bf37b5bf5230f2a85dcfe40fc7042062ab8823757ec7822aaeb22	CONTAINER_RUNNING
2006e739e84557d548b6be08e08b04a7e0efd9c11915f1d9070c0771f9e82a42	traefik	sha256:2eb085ca3ba80498cf1a2858ec007927bb21c81a6c6dc722a3cffe68bd78dc07	CONTAINER_RUNNING
0c3e3929c0d70a8b3c4a36812d9c2a8e21724390e61b7a5c7fb9dc45b034acd7	lb-tcp-443	sha256:1084dac5ea9871ffa6d01fe67150e175df9c28579073cd40d2186c08b37aba50	CONTAINER_RUNNING
3fccbabfd90898bc736f3a606018acae11f8e4de560965cf18d6b7c0a8a7e6fd	coredns	sha256:fbccbf70a429fb9ce1cdb13a40ed96b16272ef763dafe050b2c0d121dd29811b	CONTAINER_RUNNING
0e13b0ae3af00086b1c5e69ec22f484641c81559ed0fa04c0d82d88fa4bd8332	lb-tcp-80	sha256:1084dac5ea9871ffa6d01fe67150e175df9c28579073cd40d2186c08b37aba50	CONTAINER_RUNNING
b5e1e29f04d3b0453f48436a80f45f6c1bb5f9e4bfda2f2b6e63ee3b231142f8	metrics-server	sha256:37ceda8805d2e3bca331bcdd659d9cf8d3b4075a68b288054c88e62232d52883	CONTAINER_RUNNING

### Stock/Media protected decommission preflight (read-only)
Active production manifest tree contains no retired StockDividend/Media namespace or image references.
### Platform namespace preservation check
Preserved namespace present: tce-prod
Preserved namespace present: microfe-platform

### Namespaced objects and storage snapshot references in stock-prod (names only; no Secret/ConfigMap values)
configmap/kube-root-ca.crt
endpoints/backend
endpoints/stock-admin
endpoints/stock-backend
endpoints/stock-frontend
event/stock-admin-5864bcb497-6b6hm.18e40e634c019104
event/stock-admin-5864bcb497-6b6hm.18e40e634c027664
event/stock-admin-59cddb87b7-qgkjr.18e40d22b70f6afb
event/stock-admin-59cddb87b7-qgkjr.18e40d23268315bb
event/stock-admin-59cddb87b7-qgkjr.18e40d2349469ca6
event/stock-admin-59cddb87b7-qgkjr.18e40d234947a25e
event/stock-backend-6bc874575d-xcg2j.18e40e62dae92c45
event/stock-backend-6bc874575d-xcg2j.18e40e63478749ee
event/stock-backend-6bc874575d-xcg2j.18e40e634bfdef7a
event/stock-backend-6bc874575d-xcg2j.18e40e634bff081b
event/stock-frontend-74546898cb.18e7f4ed1675aea2
event/stock-frontend-74546898cb.18e7f5d5ebff4e9e
event/stock-frontend-74546898cb.18e7f6bec0e11e09
event/stock-frontend-74546898cb.18e7f7a795bfbb4f
event/stock-frontend-74546898cb.18e7f7b5ba55bb79
limitrange/stock-defaults
pod/stock-admin-5864bcb497-6b6hm
pod/stock-admin-59cddb87b7-qgkjr
pod/stock-backend-57ccb8ff6-d25jq
pod/stock-backend-6bc874575d-xcg2j
pod/stock-frontend-79c57845df-z747s
resourcequota/stock-budget
resourcequota/stock-quota
secret/ghcr-pull
secret/ghcr-secret
secret/stock-mrcute-tls
secret/stock-secrets
serviceaccount/default
service/backend
service/stock-admin
service/stock-backend
service/stock-frontend
order.acme.cert-manager.io/stock-mrcute-tls-1-3161958604
deployment.apps/stock-admin
deployment.apps/stock-backend
deployment.apps/stock-frontend
replicaset.apps/stock-admin-544cfc7bd
replicaset.apps/stock-admin-547b4b55f7
replicaset.apps/stock-admin-547dd7b5d4
replicaset.apps/stock-admin-5484cc6487
replicaset.apps/stock-admin-555f7f665c
replicaset.apps/stock-admin-556b57fb8f
replicaset.apps/stock-admin-556b8dd4f9
replicaset.apps/stock-admin-558cfc4457
replicaset.apps/stock-admin-558db47b8f
replicaset.apps/stock-admin-55d7c95fc
replicaset.apps/stock-admin-55dff8b6f6
replicaset.apps/stock-admin-565b8b9c8
replicaset.apps/stock-admin-566699c6ff
replicaset.apps/stock-admin-5677449bfd
replicaset.apps/stock-admin-569b69c98d
replicaset.apps/stock-admin-569cf6c8b7
replicaset.apps/stock-admin-574756b897
replicaset.apps/stock-admin-575cd8cc46
replicaset.apps/stock-admin-576c4d59d6
replicaset.apps/stock-admin-577ddc87bd
replicaset.apps/stock-admin-577f489d94
replicaset.apps/stock-admin-57897896d
replicaset.apps/stock-admin-57cdcd4d8f
replicaset.apps/stock-admin-58475cb8d
replicaset.apps/stock-admin-5858cd55c7
replicaset.apps/stock-admin-5864bcb497
replicaset.apps/stock-admin-58c5b555b6
replicaset.apps/stock-admin-58ddff88cc
replicaset.apps/stock-admin-5954dfcb77
replicaset.apps/stock-admin-5964dd4d48
replicaset.apps/stock-admin-596c9b896d
replicaset.apps/stock-admin-59cddb87b7
replicaset.apps/stock-admin-59cf77f486
replicaset.apps/stock-admin-5b5697fbc4
replicaset.apps/stock-admin-5b65d945cc
replicaset.apps/stock-admin-5b9bf8ff5f
replicaset.apps/stock-admin-5bb6bc4c75
replicaset.apps/stock-admin-5bf9bfdd76
replicaset.apps/stock-admin-5c6cbd5b8d
replicaset.apps/stock-admin-5c8975cd9b
replicaset.apps/stock-admin-5c9686fd48
replicaset.apps/stock-admin-5cd8c4bc9c
replicaset.apps/stock-admin-5cdd85cb9
replicaset.apps/stock-admin-5cf4c8d94b
replicaset.apps/stock-admin-5cf6d6f6db
replicaset.apps/stock-admin-5d775cc445
replicaset.apps/stock-admin-5d87df85b9
replicaset.apps/stock-admin-5db948fd77
replicaset.apps/stock-admin-5f5fc875
replicaset.apps/stock-admin-5f7bcc84d
replicaset.apps/stock-admin-5f94f6d4
replicaset.apps/stock-admin-5f9b976997
replicaset.apps/stock-admin-5fd6f67bc8
replicaset.apps/stock-admin-5ffbd48c8
replicaset.apps/stock-admin-6465bd7677
replicaset.apps/stock-admin-646d6b848d
replicaset.apps/stock-admin-647c878c57
replicaset.apps/stock-admin-64845b5958
replicaset.apps/stock-admin-648fcc4b6b
replicaset.apps/stock-admin-649bd5b58b
replicaset.apps/stock-admin-649ff98f94
replicaset.apps/stock-admin-64b495455f
replicaset.apps/stock-admin-64c76d46bc
replicaset.apps/stock-admin-64dc4bc47f
replicaset.apps/stock-admin-6556fc6668
replicaset.apps/stock-admin-6574b65d54
replicaset.apps/stock-admin-659c79b4f7
replicaset.apps/stock-admin-66446fd6d5
replicaset.apps/stock-admin-665dbf545b
replicaset.apps/stock-admin-66885f4997
replicaset.apps/stock-admin-66b74f766f
replicaset.apps/stock-admin-66bcb7958c
replicaset.apps/stock-admin-66cd64cb48
replicaset.apps/stock-admin-66f845774d
replicaset.apps/stock-admin-67589c8699
replicaset.apps/stock-admin-67848b9ccd
replicaset.apps/stock-admin-6788d4d554
replicaset.apps/stock-admin-67944c5f5f
replicaset.apps/stock-admin-679fdcc78c
replicaset.apps/stock-admin-67f49fd5c5
replicaset.apps/stock-admin-68fdb79c6d
replicaset.apps/stock-admin-68fdf7f778
replicaset.apps/stock-admin-68ffcb9ffc
replicaset.apps/stock-admin-694fd4db58
replicaset.apps/stock-admin-69878f6d56
replicaset.apps/stock-admin-69c6db4d7
replicaset.apps/stock-admin-69cd4d9869
replicaset.apps/stock-admin-6b4d665c8d
replicaset.apps/stock-admin-6b658cb7d
replicaset.apps/stock-admin-6b6d4c88cb
replicaset.apps/stock-admin-6b7955fbc8
replicaset.apps/stock-admin-6b79db74f7
replicaset.apps/stock-admin-6b9597bdf
replicaset.apps/stock-admin-6b95d4d66c
replicaset.apps/stock-admin-6bdc4d5469
replicaset.apps/stock-admin-6c45f7d854
replicaset.apps/stock-admin-6c686779ff
replicaset.apps/stock-admin-6c99784fb6
replicaset.apps/stock-admin-6cbf9d84d5
replicaset.apps/stock-admin-6d4f44dd57
replicaset.apps/stock-admin-6d557bddd7
replicaset.apps/stock-admin-6d6458f54d
replicaset.apps/stock-admin-6d6fbd8f75
replicaset.apps/stock-admin-6dccbcb4fd
replicaset.apps/stock-admin-6dcffcb557
replicaset.apps/stock-admin-6ddb4dff98
replicaset.apps/stock-admin-6df8479d68
replicaset.apps/stock-admin-6f4d7794cb
replicaset.apps/stock-admin-6f9666c446
replicaset.apps/stock-admin-6fb68dc964
replicaset.apps/stock-admin-6fc4d4f77f
replicaset.apps/stock-admin-6fc8bf8546
replicaset.apps/stock-admin-6ff7846b85
replicaset.apps/stock-admin-7474c88f7c
replicaset.apps/stock-admin-74855cf68f
replicaset.apps/stock-admin-749748ccbf
replicaset.apps/stock-admin-749bd84796
replicaset.apps/stock-admin-74c8df6bc9
replicaset.apps/stock-admin-74c9845cd6
replicaset.apps/stock-admin-74cb95bddc
replicaset.apps/stock-admin-74dbcff5c7
replicaset.apps/stock-admin-74f744c44
replicaset.apps/stock-admin-7574d77b96
replicaset.apps/stock-admin-76755449cb
replicaset.apps/stock-admin-76858678f9
replicaset.apps/stock-admin-76859c56b8
replicaset.apps/stock-admin-76c6699fcd
replicaset.apps/stock-admin-76cccb67f6
replicaset.apps/stock-admin-7744f896dc
replicaset.apps/stock-admin-7754bb96bf
replicaset.apps/stock-admin-77bd44d57d
replicaset.apps/stock-admin-7899977f66
replicaset.apps/stock-admin-78f96594cf
replicaset.apps/stock-admin-7967788c6c
replicaset.apps/stock-admin-797544c7c8
replicaset.apps/stock-admin-797856b9c8
replicaset.apps/stock-admin-79c498dc4d
replicaset.apps/stock-admin-79c598f7db
replicaset.apps/stock-admin-79c5b7f44f
replicaset.apps/stock-admin-7b76df95fd
replicaset.apps/stock-admin-7b84cf4877
replicaset.apps/stock-admin-7b9ddb6d8d
replicaset.apps/stock-admin-7bb4b5fb8b
replicaset.apps/stock-admin-7c46bbfcdf
replicaset.apps/stock-admin-7c4bb9dcd6
replicaset.apps/stock-admin-7ccbcdf75b
replicaset.apps/stock-admin-7cdbd6bbb5
replicaset.apps/stock-admin-7cfc47bd69
replicaset.apps/stock-admin-7d64fddf9c
replicaset.apps/stock-admin-7d76fb4c89
replicaset.apps/stock-admin-7d8f49449c
replicaset.apps/stock-admin-7db6f8fcd4
replicaset.apps/stock-admin-7dff4cc5d8
replicaset.apps/stock-admin-7f448548b9
replicaset.apps/stock-admin-7f45847d4b
replicaset.apps/stock-admin-7f66f6f765
replicaset.apps/stock-admin-7f7f76644f
replicaset.apps/stock-admin-7f8648449f
replicaset.apps/stock-admin-7fb8884696
replicaset.apps/stock-admin-7fc48f669f
replicaset.apps/stock-admin-7fd5587d5
replicaset.apps/stock-admin-7ff9bc6f4f
replicaset.apps/stock-admin-8447f484df
replicaset.apps/stock-admin-845dbb6c97
replicaset.apps/stock-admin-8467c4df74
replicaset.apps/stock-admin-8468cf49d4
replicaset.apps/stock-admin-847cfb84ff
replicaset.apps/stock-admin-849bcd6d46
replicaset.apps/stock-admin-84dc77747f
replicaset.apps/stock-admin-84f956744f
replicaset.apps/stock-admin-84f9c9d8f9
replicaset.apps/stock-admin-854657854f
replicaset.apps/stock-admin-8566b5d44
replicaset.apps/stock-admin-8566b6d7dd
replicaset.apps/stock-admin-8585c48d94
replicaset.apps/stock-admin-859995d4bf
replicaset.apps/stock-admin-85c4d7cb4d
replicaset.apps/stock-admin-85cc86b749
replicaset.apps/stock-admin-85d8994cd4
replicaset.apps/stock-admin-85dd58954c
replicaset.apps/stock-admin-864bb667ff
replicaset.apps/stock-admin-865844d8fc
replicaset.apps/stock-admin-868c4b5576
replicaset.apps/stock-admin-86c7f444c8
replicaset.apps/stock-admin-888bf5f4f
replicaset.apps/stock-admin-899bd4d7d
replicaset.apps/stock-admin-89dc549ff
replicaset.apps/stock-admin-89fdc5964
replicaset.apps/stock-admin-8b5d6d64f
replicaset.apps/stock-admin-8cbdfd755
replicaset.apps/stock-admin-8d88fd956
replicaset.apps/stock-admin-8ffb4b89f
replicaset.apps/stock-admin-94d9f4bd4
replicaset.apps/stock-admin-95bd8d945
replicaset.apps/stock-admin-9757b86
replicaset.apps/stock-admin-9bbbf8fb4
replicaset.apps/stock-admin-9c5d4c9df
replicaset.apps/stock-admin-b47f4d965
replicaset.apps/stock-admin-b8bbd5567
replicaset.apps/stock-admin-b959549d5
replicaset.apps/stock-admin-b96676888
replicaset.apps/stock-admin-bb95d4b7f
replicaset.apps/stock-admin-bc9995574
replicaset.apps/stock-admin-bdcbbf8d5
replicaset.apps/stock-admin-c5c5cf85d
replicaset.apps/stock-admin-c647b74f5
replicaset.apps/stock-admin-c8cd6d8f9
replicaset.apps/stock-admin-cd564655b
replicaset.apps/stock-admin-cd9c555d7
replicaset.apps/stock-admin-cf75f949d
replicaset.apps/stock-admin-cf8797f6
replicaset.apps/stock-admin-d5cff4d65
replicaset.apps/stock-admin-d5fdb7bc6
replicaset.apps/stock-admin-d6856495b
replicaset.apps/stock-admin-d74957fd7
replicaset.apps/stock-admin-d7dd8f8bf
replicaset.apps/stock-admin-dbb65bcd6
replicaset.apps/stock-admin-ddcd56d8b
replicaset.apps/stock-admin-f6856cfb9
replicaset.apps/stock-admin-f68578bb5
replicaset.apps/stock-admin-f7d556f95
replicaset.apps/stock-admin-f96c45bb4
replicaset.apps/stock-admin-fb87c56c8
replicaset.apps/stock-admin-fc5c79b54
replicaset.apps/stock-admin-fc97f8d44
replicaset.apps/stock-admin-fcb7d6
replicaset.apps/stock-backend-54596d99d6
replicaset.apps/stock-backend-5486b78445
replicaset.apps/stock-backend-5489c5b485
replicaset.apps/stock-backend-54975d9c57
replicaset.apps/stock-backend-549796df58
replicaset.apps/stock-backend-54cfdb7f4f
replicaset.apps/stock-backend-54fbc4cf78
replicaset.apps/stock-backend-5548bcd87f
replicaset.apps/stock-backend-5548c86b4c
replicaset.apps/stock-backend-5556848869
replicaset.apps/stock-backend-559b9b95d8
replicaset.apps/stock-backend-55bbc48776
replicaset.apps/stock-backend-55bcb746f7
replicaset.apps/stock-backend-55f85ddc45
replicaset.apps/stock-backend-55fcbb8b94
replicaset.apps/stock-backend-564bfb98d7
replicaset.apps/stock-backend-56575489f9
replicaset.apps/stock-backend-5696f55888
replicaset.apps/stock-backend-5699b96fdc
replicaset.apps/stock-backend-56c957cbfb
replicaset.apps/stock-backend-56c9db6dc8
replicaset.apps/stock-backend-56f9f6d55
replicaset.apps/stock-backend-5765d467db
replicaset.apps/stock-backend-576fb79c78
replicaset.apps/stock-backend-5796467fbd
replicaset.apps/stock-backend-57ccb8ff6
replicaset.apps/stock-backend-58464f567d
replicaset.apps/stock-backend-584bd48597
replicaset.apps/stock-backend-588d4747d6
replicaset.apps/stock-backend-589d99887c
replicaset.apps/stock-backend-5947569d87
replicaset.apps/stock-backend-594f696b46
replicaset.apps/stock-backend-594f7685d6
replicaset.apps/stock-backend-5955f998d
replicaset.apps/stock-backend-5975fd7c67
replicaset.apps/stock-backend-5998b79d76
replicaset.apps/stock-backend-59bd95c977
replicaset.apps/stock-backend-59f5f98664
replicaset.apps/stock-backend-59f7ff6fc
replicaset.apps/stock-backend-59ffbbf6dc
replicaset.apps/stock-backend-5b4548d6b4
replicaset.apps/stock-backend-5b67b496dc
replicaset.apps/stock-backend-5b6b76f694
replicaset.apps/stock-backend-5b978b44bc
replicaset.apps/stock-backend-5bb8754458
replicaset.apps/stock-backend-5bcdf9556c
replicaset.apps/stock-backend-5bff86c8c8
replicaset.apps/stock-backend-5c69c554d4
replicaset.apps/stock-backend-5c9f77fc55
replicaset.apps/stock-backend-5ccb86cfc8
replicaset.apps/stock-backend-5cd96bd67d
replicaset.apps/stock-backend-5cdb66fc67
replicaset.apps/stock-backend-5cff6d5655
replicaset.apps/stock-backend-5dc5df5bd6
replicaset.apps/stock-backend-5f45f875f
replicaset.apps/stock-backend-5f5bddf746
replicaset.apps/stock-backend-5f6dd74868
replicaset.apps/stock-backend-5fbd575b95
replicaset.apps/stock-backend-5fc566dd8f
replicaset.apps/stock-backend-5ff54f5c74
replicaset.apps/stock-backend-5ffc6fbc8
replicaset.apps/stock-backend-644699c8f8
replicaset.apps/stock-backend-646948bc9b
replicaset.apps/stock-backend-6478977f4b
replicaset.apps/stock-backend-64cfd889d8
replicaset.apps/stock-backend-64dbf998b6
replicaset.apps/stock-backend-64fd565
replicaset.apps/stock-backend-6547946847
replicaset.apps/stock-backend-65dcbc59f9
replicaset.apps/stock-backend-6647646874
replicaset.apps/stock-backend-66b579b978
replicaset.apps/stock-backend-675c44854c
replicaset.apps/stock-backend-676bbb7dd7
replicaset.apps/stock-backend-67c5f86579
replicaset.apps/stock-backend-67c9fdc489
replicaset.apps/stock-backend-68458d6cdf
replicaset.apps/stock-backend-684658f67f
replicaset.apps/stock-backend-68845c65b4
replicaset.apps/stock-backend-689694fcb
replicaset.apps/stock-backend-689b896654
replicaset.apps/stock-backend-689d78bd96
replicaset.apps/stock-backend-68f45cd6b8
replicaset.apps/stock-backend-694cfd6c85
replicaset.apps/stock-backend-695977497f
replicaset.apps/stock-backend-6975777c78
replicaset.apps/stock-backend-697db585db
replicaset.apps/stock-backend-69cbb67579
replicaset.apps/stock-backend-69dc97d89b
replicaset.apps/stock-backend-69fbc94c4b
replicaset.apps/stock-backend-6b4b9749b9
replicaset.apps/stock-backend-6bb5f79dd4
replicaset.apps/stock-backend-6bb7f8c4f
replicaset.apps/stock-backend-6bbfd66c49
replicaset.apps/stock-backend-6bc874575d
replicaset.apps/stock-backend-6bd68b7db8
replicaset.apps/stock-backend-6bd75fff54
replicaset.apps/stock-backend-6c76997988
replicaset.apps/stock-backend-6c7c47c459
replicaset.apps/stock-backend-6c8f87f9b4
replicaset.apps/stock-backend-6c9bfb65d7
replicaset.apps/stock-backend-6c9d65bb96
replicaset.apps/stock-backend-6c9dc6fdc9
replicaset.apps/stock-backend-6cdb64498b
replicaset.apps/stock-backend-6d447569b6
replicaset.apps/stock-backend-6d645cd66d
replicaset.apps/stock-backend-6d649676c4
replicaset.apps/stock-backend-6d7cd68d7f
replicaset.apps/stock-backend-6d8979fd5d
replicaset.apps/stock-backend-6dbf8c4b8
replicaset.apps/stock-backend-6df8fcc47d
replicaset.apps/stock-backend-6f68c4dbd7
replicaset.apps/stock-backend-6f776c964c
replicaset.apps/stock-backend-6f9589b578
replicaset.apps/stock-backend-6f95cc96d7
replicaset.apps/stock-backend-6fbcc7779d
replicaset.apps/stock-backend-6fcbd9768c
replicaset.apps/stock-backend-6fd58899dc
replicaset.apps/stock-backend-6fd84c544c
replicaset.apps/stock-backend-6fff8b4479
replicaset.apps/stock-backend-74466c858f
replicaset.apps/stock-backend-7454c6c585
replicaset.apps/stock-backend-747c949b4
replicaset.apps/stock-backend-74c99cd67c
replicaset.apps/stock-backend-74d958c7b
replicaset.apps/stock-backend-75947776bf
replicaset.apps/stock-backend-75fdcf6f55
replicaset.apps/stock-backend-766b4f47d6
replicaset.apps/stock-backend-76bb7d645b
replicaset.apps/stock-backend-77455f4f89
replicaset.apps/stock-backend-777bcb965b
replicaset.apps/stock-backend-777cccb4ff
replicaset.apps/stock-backend-778d89767
replicaset.apps/stock-backend-786b76d66f
replicaset.apps/stock-backend-786c7cf779
replicaset.apps/stock-backend-7884bd5b77
replicaset.apps/stock-backend-7889dcb846
replicaset.apps/stock-backend-789cc5f74f
replicaset.apps/stock-backend-789d67cb98
replicaset.apps/stock-backend-789dcd9498
replicaset.apps/stock-backend-7949978cf8
replicaset.apps/stock-backend-796464bdc5
replicaset.apps/stock-backend-7987b75cb7
replicaset.apps/stock-backend-7995d7968d
replicaset.apps/stock-backend-79bb67dbb
replicaset.apps/stock-backend-79db6d46
replicaset.apps/stock-backend-79dd6ddcbf
replicaset.apps/stock-backend-7b4578f89b
replicaset.apps/stock-backend-7b4878c955
replicaset.apps/stock-backend-7b889c5ddd
replicaset.apps/stock-backend-7b9489b7f4
replicaset.apps/stock-backend-7bd7694875
replicaset.apps/stock-backend-7c649c6fb7
replicaset.apps/stock-backend-7c6667dcf5
replicaset.apps/stock-backend-7c869f9dcc
replicaset.apps/stock-backend-7c8bc66c6b
replicaset.apps/stock-backend-7cd45fd87c
replicaset.apps/stock-backend-7d5d6fb4c9
replicaset.apps/stock-backend-7d6bb9f5dc
replicaset.apps/stock-backend-7d8f5bdfdc
replicaset.apps/stock-backend-7d94c88fb4
replicaset.apps/stock-backend-7dc87ccfc9
replicaset.apps/stock-backend-7f44bdcf68
replicaset.apps/stock-backend-7f6c9d776f
replicaset.apps/stock-backend-7fbbdb6ff8
replicaset.apps/stock-backend-7fd8b99c86
replicaset.apps/stock-backend-7ffd8b6fc6
replicaset.apps/stock-backend-844577ffc8
replicaset.apps/stock-backend-8446bcc676
replicaset.apps/stock-backend-846948869
replicaset.apps/stock-backend-847bd8dbdc
replicaset.apps/stock-backend-84c56cf67f
replicaset.apps/stock-backend-84c79458ff
replicaset.apps/stock-backend-84cd8cc96b
replicaset.apps/stock-backend-84dfdfd9b8
replicaset.apps/stock-backend-8557955595
replicaset.apps/stock-backend-8557b56859
replicaset.apps/stock-backend-8569457bbb
replicaset.apps/stock-backend-8579cfb48b
replicaset.apps/stock-backend-858f45c799
replicaset.apps/stock-backend-859d77f899
replicaset.apps/stock-backend-85bf5fc95b
replicaset.apps/stock-backend-85c6c694df
replicaset.apps/stock-backend-865b4499bf
replicaset.apps/stock-backend-866cf5498d
replicaset.apps/stock-backend-866fb5fd57
replicaset.apps/stock-backend-8686dc4fd
replicaset.apps/stock-backend-86cc69f958
replicaset.apps/stock-backend-86dbfb698
replicaset.apps/stock-backend-86f875bd4d
replicaset.apps/stock-backend-88c58d494
replicaset.apps/stock-backend-8d9d4f68d
replicaset.apps/stock-backend-8dfd4454c
replicaset.apps/stock-backend-8f7f44fcf
replicaset.apps/stock-backend-94cc499c9
replicaset.apps/stock-backend-968696496
replicaset.apps/stock-backend-977768668
replicaset.apps/stock-backend-99646ffd9
replicaset.apps/stock-backend-99b777c9
replicaset.apps/stock-backend-9b69d5db
replicaset.apps/stock-backend-9b8886fd9
replicaset.apps/stock-backend-9b9f69d99
replicaset.apps/stock-backend-9bbf9c9b9
replicaset.apps/stock-backend-9df7bdd55
replicaset.apps/stock-backend-b4859fb74
replicaset.apps/stock-backend-b64f9bdd8
replicaset.apps/stock-backend-b9564f5bf
replicaset.apps/stock-backend-b95fd5f7b
replicaset.apps/stock-backend-bbcd56c76
replicaset.apps/stock-backend-bc789675f
replicaset.apps/stock-backend-bd8dfc97b
replicaset.apps/stock-backend-bfbcf4957
replicaset.apps/stock-backend-c7b9cb8f5
replicaset.apps/stock-backend-cb75cb78c
replicaset.apps/stock-backend-cf7bb957f
replicaset.apps/stock-backend-cf8b475bd
replicaset.apps/stock-backend-cf9f49f86
replicaset.apps/stock-backend-d6b79877b
replicaset.apps/stock-backend-d6d7f7887
replicaset.apps/stock-backend-d85844b4
replicaset.apps/stock-backend-d9946b74f
replicaset.apps/stock-backend-ddb854c99
replicaset.apps/stock-backend-f45cb8fbd
replicaset.apps/stock-backend-f59d758d4
replicaset.apps/stock-backend-f7bfc6c9f
replicaset.apps/stock-backend-fb9c5dbd5
replicaset.apps/stock-backend-fbc8764b4
replicaset.apps/stock-backend-ff56f7bdb
replicaset.apps/stock-frontend-74546898cb
replicaset.apps/stock-frontend-79c57845df
certificaterequest.cert-manager.io/stock-mrcute-tls-1
certificate.cert-manager.io/stock-mrcute-tls
endpointslice.discovery.k8s.io/backend-fvv26
endpointslice.discovery.k8s.io/stock-admin-sf6kz
endpointslice.discovery.k8s.io/stock-backend-jbwqp
endpointslice.discovery.k8s.io/stock-frontend-b8rbs
event.events.k8s.io/stock-admin-5864bcb497-6b6hm.18e40e634c019104
event.events.k8s.io/stock-admin-5864bcb497-6b6hm.18e40e634c027664
event.events.k8s.io/stock-admin-59cddb87b7-qgkjr.18e40d22b70f6afb
event.events.k8s.io/stock-admin-59cddb87b7-qgkjr.18e40d23268315bb
event.events.k8s.io/stock-admin-59cddb87b7-qgkjr.18e40d2349469ca6
event.events.k8s.io/stock-admin-59cddb87b7-qgkjr.18e40d234947a25e
event.events.k8s.io/stock-backend-6bc874575d-xcg2j.18e40e62dae92c45
event.events.k8s.io/stock-backend-6bc874575d-xcg2j.18e40e63478749ee
event.events.k8s.io/stock-backend-6bc874575d-xcg2j.18e40e634bfdef7a
event.events.k8s.io/stock-backend-6bc874575d-xcg2j.18e40e634bff081b
event.events.k8s.io/stock-frontend-74546898cb.18e7f4ed1675aea2
event.events.k8s.io/stock-frontend-74546898cb.18e7f5d5ebff4e9e
event.events.k8s.io/stock-frontend-74546898cb.18e7f6bec0e11e09
event.events.k8s.io/stock-frontend-74546898cb.18e7f7a795bfbb4f
event.events.k8s.io/stock-frontend-74546898cb.18e7f7b5ba55bb79
podmetrics.metrics.k8s.io/stock-backend-57ccb8ff6-d25jq
podmetrics.metrics.k8s.io/stock-frontend-79c57845df-z747s
ingress.networking.k8s.io/stock
ingress.networking.k8s.io/stock-ingress
### Ingress hosts/TLS secret references and published addresses (names only): stock-prod
stock	admin.mrcute.space,api.mrcute.space,mrcute.space,www.mrcute.space	admin.mrcute.space,api.mrcute.space,mrcute.space,www.mrcute.space	stock-mrcute-tls	10.0.0.120
stock-ingress	admin.mrcute.space,api.mrcute.space,mrcute.space,www.mrcute.space	admin.mrcute.space,api.mrcute.space,mrcute.space,www.mrcute.space	stock-mrcute-tls	10.0.0.120
DNS ownership is not inferred; reconcile these hostnames with authoritative DNS/provider records before deletion.
### Common workload status: stock-prod
NAME                                  READY   STATUS             RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
pod/stock-admin-5864bcb497-6b6hm      0/1     ImagePullBackOff   0          12d   10.42.0.182   tce-k3s-01   <none>           <none>
pod/stock-admin-59cddb87b7-qgkjr      0/1     ImagePullBackOff   0          12d   10.42.0.180   tce-k3s-01   <none>           <none>
pod/stock-backend-57ccb8ff6-d25jq     1/1     Running            0          56d   10.42.0.55    tce-k3s-01   <none>           <none>
pod/stock-backend-6bc874575d-xcg2j    0/1     ImagePullBackOff   0          12d   10.42.0.183   tce-k3s-01   <none>           <none>
pod/stock-frontend-79c57845df-z747s   1/1     Running            0          56d   10.42.0.56    tce-k3s-01   <none>           <none>

NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE   SELECTOR
service/backend          ClusterIP   10.43.46.139    <none>        8080/TCP   56d   app=stock-backend
service/stock-admin      ClusterIP   10.43.97.150    <none>        3000/TCP   52d   app=stock-admin
service/stock-backend    ClusterIP   10.43.247.219   <none>        8080/TCP   56d   app=stock-backend
service/stock-frontend   ClusterIP   10.43.53.102    <none>        3000/TCP   56d   app=stock-frontend

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                                                SELECTOR
deployment.apps/stock-admin      0/1     1            0           52d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin
deployment.apps/stock-backend    1/1     1            1           56d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend
deployment.apps/stock-frontend   1/1     0            1           56d   frontend     ghcr.io/phanthienquoc/stockdividend/user:23b2878      app=stock-frontend

NAME                                        DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES                                                SELECTOR
replicaset.apps/stock-admin-544cfc7bd       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=544cfc7bd
replicaset.apps/stock-admin-547b4b55f7      0         0         0       19d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=547b4b55f7
replicaset.apps/stock-admin-547dd7b5d4      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=547dd7b5d4
replicaset.apps/stock-admin-5484cc6487      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5484cc6487
replicaset.apps/stock-admin-555f7f665c      0         0         0       23d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=555f7f665c
replicaset.apps/stock-admin-556b57fb8f      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=556b57fb8f
replicaset.apps/stock-admin-556b8dd4f9      0         0         0       25d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=556b8dd4f9
replicaset.apps/stock-admin-558cfc4457      0         0         0       30d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=558cfc4457
replicaset.apps/stock-admin-558db47b8f      0         0         0       17d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=558db47b8f
replicaset.apps/stock-admin-55d7c95fc       0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=55d7c95fc
replicaset.apps/stock-admin-55dff8b6f6      0         0         0       17d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=55dff8b6f6
replicaset.apps/stock-admin-565b8b9c8       0         0         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=565b8b9c8
replicaset.apps/stock-admin-566699c6ff      0         0         0       34d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=566699c6ff
replicaset.apps/stock-admin-5677449bfd      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5677449bfd
replicaset.apps/stock-admin-569b69c98d      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=569b69c98d
replicaset.apps/stock-admin-569cf6c8b7      0         0         0       35d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=569cf6c8b7
replicaset.apps/stock-admin-574756b897      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=574756b897
replicaset.apps/stock-admin-575cd8cc46      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=575cd8cc46
replicaset.apps/stock-admin-576c4d59d6      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=576c4d59d6
replicaset.apps/stock-admin-577ddc87bd      0         0         0       17d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=577ddc87bd
replicaset.apps/stock-admin-577f489d94      0         0         0       16d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=577f489d94
replicaset.apps/stock-admin-57897896d       0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=57897896d
replicaset.apps/stock-admin-57cdcd4d8f      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=57cdcd4d8f
replicaset.apps/stock-admin-58475cb8d       0         0         0       37d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=58475cb8d
replicaset.apps/stock-admin-5858cd55c7      0         0         0       32d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5858cd55c7
replicaset.apps/stock-admin-5864bcb497      1         1         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5864bcb497
replicaset.apps/stock-admin-58c5b555b6      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=58c5b555b6
replicaset.apps/stock-admin-58ddff88cc      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=58ddff88cc
replicaset.apps/stock-admin-5954dfcb77      0         0         0       26d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5954dfcb77
replicaset.apps/stock-admin-5964dd4d48      0         0         0       16d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5964dd4d48
replicaset.apps/stock-admin-596c9b896d      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=596c9b896d
replicaset.apps/stock-admin-59cddb87b7      1         1         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=59cddb87b7
replicaset.apps/stock-admin-59cf77f486      0         0         0       39d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=59cf77f486
replicaset.apps/stock-admin-5b5697fbc4      0         0         0       35d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5b5697fbc4
replicaset.apps/stock-admin-5b65d945cc      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5b65d945cc
replicaset.apps/stock-admin-5b9bf8ff5f      0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5b9bf8ff5f
replicaset.apps/stock-admin-5bb6bc4c75      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5bb6bc4c75
replicaset.apps/stock-admin-5bf9bfdd76      0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5bf9bfdd76
replicaset.apps/stock-admin-5c6cbd5b8d      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5c6cbd5b8d
replicaset.apps/stock-admin-5c8975cd9b      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5c8975cd9b
replicaset.apps/stock-admin-5c9686fd48      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5c9686fd48
replicaset.apps/stock-admin-5cd8c4bc9c      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5cd8c4bc9c
replicaset.apps/stock-admin-5cdd85cb9       0         0         0       30d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5cdd85cb9
replicaset.apps/stock-admin-5cf4c8d94b      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5cf4c8d94b
replicaset.apps/stock-admin-5cf6d6f6db      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5cf6d6f6db
replicaset.apps/stock-admin-5d775cc445      0         0         0       17d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5d775cc445
replicaset.apps/stock-admin-5d87df85b9      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5d87df85b9
replicaset.apps/stock-admin-5db948fd77      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5db948fd77
replicaset.apps/stock-admin-5f5fc875        0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5f5fc875
replicaset.apps/stock-admin-5f7bcc84d       0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5f7bcc84d
replicaset.apps/stock-admin-5f94f6d4        0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5f94f6d4
replicaset.apps/stock-admin-5f9b976997      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5f9b976997
replicaset.apps/stock-admin-5fd6f67bc8      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5fd6f67bc8
replicaset.apps/stock-admin-5ffbd48c8       0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=5ffbd48c8
replicaset.apps/stock-admin-6465bd7677      0         0         0       33d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6465bd7677
replicaset.apps/stock-admin-646d6b848d      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=646d6b848d
replicaset.apps/stock-admin-647c878c57      0         0         0       16d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=647c878c57
replicaset.apps/stock-admin-64845b5958      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=64845b5958
replicaset.apps/stock-admin-648fcc4b6b      0         0         0       32d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=648fcc4b6b
replicaset.apps/stock-admin-649bd5b58b      0         0         0       52d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=649bd5b58b
replicaset.apps/stock-admin-649ff98f94      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=649ff98f94
replicaset.apps/stock-admin-64b495455f      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=64b495455f
replicaset.apps/stock-admin-64c76d46bc      0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=64c76d46bc
replicaset.apps/stock-admin-64dc4bc47f      0         0         0       16d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=64dc4bc47f
replicaset.apps/stock-admin-6556fc6668      0         0         0       34d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6556fc6668
replicaset.apps/stock-admin-6574b65d54      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6574b65d54
replicaset.apps/stock-admin-659c79b4f7      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=659c79b4f7
replicaset.apps/stock-admin-66446fd6d5      0         0         0       23d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=66446fd6d5
replicaset.apps/stock-admin-665dbf545b      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=665dbf545b
replicaset.apps/stock-admin-66885f4997      0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=66885f4997
replicaset.apps/stock-admin-66b74f766f      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=66b74f766f
replicaset.apps/stock-admin-66bcb7958c      0         0         0       16d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=66bcb7958c
replicaset.apps/stock-admin-66cd64cb48      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=66cd64cb48
replicaset.apps/stock-admin-66f845774d      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=66f845774d
replicaset.apps/stock-admin-67589c8699      0         0         0       18d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=67589c8699
replicaset.apps/stock-admin-67848b9ccd      0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=67848b9ccd
replicaset.apps/stock-admin-6788d4d554      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6788d4d554
replicaset.apps/stock-admin-67944c5f5f      0         0         0       22d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=67944c5f5f
replicaset.apps/stock-admin-679fdcc78c      0         0         0       25d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=679fdcc78c
replicaset.apps/stock-admin-67f49fd5c5      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=67f49fd5c5
replicaset.apps/stock-admin-68fdb79c6d      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=68fdb79c6d
replicaset.apps/stock-admin-68fdf7f778      0         0         0       23d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=68fdf7f778
replicaset.apps/stock-admin-68ffcb9ffc      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=68ffcb9ffc
replicaset.apps/stock-admin-694fd4db58      0         0         0       26d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=694fd4db58
replicaset.apps/stock-admin-69878f6d56      0         0         0       35d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=69878f6d56
replicaset.apps/stock-admin-69c6db4d7       0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=69c6db4d7
replicaset.apps/stock-admin-69cd4d9869      0         0         0       25d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=69cd4d9869
replicaset.apps/stock-admin-6b4d665c8d      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b4d665c8d
replicaset.apps/stock-admin-6b658cb7d       0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b658cb7d
replicaset.apps/stock-admin-6b6d4c88cb      0         0         0       26d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b6d4c88cb
replicaset.apps/stock-admin-6b7955fbc8      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b7955fbc8
replicaset.apps/stock-admin-6b79db74f7      0         0         0       22d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b79db74f7
replicaset.apps/stock-admin-6b9597bdf       0         0         0       33d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b9597bdf
replicaset.apps/stock-admin-6b95d4d66c      0         0         0       19d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6b95d4d66c
replicaset.apps/stock-admin-6bdc4d5469      0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6bdc4d5469
replicaset.apps/stock-admin-6c45f7d854      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6c45f7d854
replicaset.apps/stock-admin-6c686779ff      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6c686779ff
replicaset.apps/stock-admin-6c99784fb6      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6c99784fb6
replicaset.apps/stock-admin-6cbf9d84d5      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6cbf9d84d5
replicaset.apps/stock-admin-6d4f44dd57      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6d4f44dd57
replicaset.apps/stock-admin-6d557bddd7      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6d557bddd7
replicaset.apps/stock-admin-6d6458f54d      0         0         0       30d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6d6458f54d
replicaset.apps/stock-admin-6d6fbd8f75      0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6d6fbd8f75
replicaset.apps/stock-admin-6dccbcb4fd      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6dccbcb4fd
replicaset.apps/stock-admin-6dcffcb557      0         0         0       19d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6dcffcb557
replicaset.apps/stock-admin-6ddb4dff98      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6ddb4dff98
replicaset.apps/stock-admin-6df8479d68      0         0         0       25d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6df8479d68
replicaset.apps/stock-admin-6f4d7794cb      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6f4d7794cb
replicaset.apps/stock-admin-6f9666c446      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6f9666c446
replicaset.apps/stock-admin-6fb68dc964      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6fb68dc964
replicaset.apps/stock-admin-6fc4d4f77f      0         0         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6fc4d4f77f
replicaset.apps/stock-admin-6fc8bf8546      0         0         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6fc8bf8546
replicaset.apps/stock-admin-6ff7846b85      0         0         0       33d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=6ff7846b85
replicaset.apps/stock-admin-7474c88f7c      0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7474c88f7c
replicaset.apps/stock-admin-74855cf68f      0         0         0       16d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=74855cf68f
replicaset.apps/stock-admin-749748ccbf      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=749748ccbf
replicaset.apps/stock-admin-749bd84796      0         0         0       33d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=749bd84796
replicaset.apps/stock-admin-74c8df6bc9      0         0         0       25d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=74c8df6bc9
replicaset.apps/stock-admin-74c9845cd6      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=74c9845cd6
replicaset.apps/stock-admin-74cb95bddc      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=74cb95bddc
replicaset.apps/stock-admin-74dbcff5c7      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=74dbcff5c7
replicaset.apps/stock-admin-74f744c44       0         0         0       19d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=74f744c44
replicaset.apps/stock-admin-7574d77b96      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7574d77b96
replicaset.apps/stock-admin-76755449cb      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=76755449cb
replicaset.apps/stock-admin-76858678f9      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=76858678f9
replicaset.apps/stock-admin-76859c56b8      0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=76859c56b8
replicaset.apps/stock-admin-76c6699fcd      0         0         0       19d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=76c6699fcd
replicaset.apps/stock-admin-76cccb67f6      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=76cccb67f6
replicaset.apps/stock-admin-7744f896dc      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7744f896dc
replicaset.apps/stock-admin-7754bb96bf      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7754bb96bf
replicaset.apps/stock-admin-77bd44d57d      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=77bd44d57d
replicaset.apps/stock-admin-7899977f66      0         0         0       23d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7899977f66
replicaset.apps/stock-admin-78f96594cf      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=78f96594cf
replicaset.apps/stock-admin-7967788c6c      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7967788c6c
replicaset.apps/stock-admin-797544c7c8      0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=797544c7c8
replicaset.apps/stock-admin-797856b9c8      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=797856b9c8
replicaset.apps/stock-admin-79c498dc4d      0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=79c498dc4d
replicaset.apps/stock-admin-79c598f7db      0         0         0       22d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=79c598f7db
replicaset.apps/stock-admin-79c5b7f44f      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=79c5b7f44f
replicaset.apps/stock-admin-7b76df95fd      0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7b76df95fd
replicaset.apps/stock-admin-7b84cf4877      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7b84cf4877
replicaset.apps/stock-admin-7b9ddb6d8d      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7b9ddb6d8d
replicaset.apps/stock-admin-7bb4b5fb8b      0         0         0       18d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7bb4b5fb8b
replicaset.apps/stock-admin-7c46bbfcdf      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7c46bbfcdf
replicaset.apps/stock-admin-7c4bb9dcd6      0         0         0       26d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7c4bb9dcd6
replicaset.apps/stock-admin-7ccbcdf75b      0         0         0       30d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7ccbcdf75b
replicaset.apps/stock-admin-7cdbd6bbb5      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7cdbd6bbb5
replicaset.apps/stock-admin-7cfc47bd69      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7cfc47bd69
replicaset.apps/stock-admin-7d64fddf9c      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7d64fddf9c
replicaset.apps/stock-admin-7d76fb4c89      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7d76fb4c89
replicaset.apps/stock-admin-7d8f49449c      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7d8f49449c
replicaset.apps/stock-admin-7db6f8fcd4      0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7db6f8fcd4
replicaset.apps/stock-admin-7dff4cc5d8      0         0         0       17d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7dff4cc5d8
replicaset.apps/stock-admin-7f448548b9      0         0         0       23d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7f448548b9
replicaset.apps/stock-admin-7f45847d4b      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7f45847d4b
replicaset.apps/stock-admin-7f66f6f765      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7f66f6f765
replicaset.apps/stock-admin-7f7f76644f      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7f7f76644f
replicaset.apps/stock-admin-7f8648449f      0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7f8648449f
replicaset.apps/stock-admin-7fb8884696      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7fb8884696
replicaset.apps/stock-admin-7fc48f669f      0         0         0       33d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7fc48f669f
replicaset.apps/stock-admin-7fd5587d5       0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7fd5587d5
replicaset.apps/stock-admin-7ff9bc6f4f      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=7ff9bc6f4f
replicaset.apps/stock-admin-8447f484df      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8447f484df
replicaset.apps/stock-admin-845dbb6c97      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=845dbb6c97
replicaset.apps/stock-admin-8467c4df74      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8467c4df74
replicaset.apps/stock-admin-8468cf49d4      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8468cf49d4
replicaset.apps/stock-admin-847cfb84ff      0         0         0       34d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=847cfb84ff
replicaset.apps/stock-admin-849bcd6d46      0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=849bcd6d46
replicaset.apps/stock-admin-84dc77747f      0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=84dc77747f
replicaset.apps/stock-admin-84f956744f      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=84f956744f
replicaset.apps/stock-admin-84f9c9d8f9      0         0         0       19d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=84f9c9d8f9
replicaset.apps/stock-admin-854657854f      0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=854657854f
replicaset.apps/stock-admin-8566b5d44       0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8566b5d44
replicaset.apps/stock-admin-8566b6d7dd      0         0         0       18d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8566b6d7dd
replicaset.apps/stock-admin-8585c48d94      0         0         0       28d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8585c48d94
replicaset.apps/stock-admin-859995d4bf      0         0         0       18d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=859995d4bf
replicaset.apps/stock-admin-85c4d7cb4d      0         0         0       33d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=85c4d7cb4d
replicaset.apps/stock-admin-85cc86b749      0         0         0       13d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=85cc86b749
replicaset.apps/stock-admin-85d8994cd4      0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=85d8994cd4
replicaset.apps/stock-admin-85dd58954c      0         0         0       35d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=85dd58954c
replicaset.apps/stock-admin-864bb667ff      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=864bb667ff
replicaset.apps/stock-admin-865844d8fc      0         0         0       26d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=865844d8fc
replicaset.apps/stock-admin-868c4b5576      0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=868c4b5576
replicaset.apps/stock-admin-86c7f444c8      0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=86c7f444c8
replicaset.apps/stock-admin-888bf5f4f       0         0         0       27d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=888bf5f4f
replicaset.apps/stock-admin-899bd4d7d       0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=899bd4d7d
replicaset.apps/stock-admin-89dc549ff       0         0         0       22d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=89dc549ff
replicaset.apps/stock-admin-89fdc5964       0         0         0       22d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=89fdc5964
replicaset.apps/stock-admin-8b5d6d64f       0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8b5d6d64f
replicaset.apps/stock-admin-8cbdfd755       0         0         0       32d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8cbdfd755
replicaset.apps/stock-admin-8d88fd956       0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8d88fd956
replicaset.apps/stock-admin-8ffb4b89f       0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=8ffb4b89f
replicaset.apps/stock-admin-94d9f4bd4       0         0         0       30d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=94d9f4bd4
replicaset.apps/stock-admin-95bd8d945       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=95bd8d945
replicaset.apps/stock-admin-9757b86         0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=9757b86
replicaset.apps/stock-admin-9bbbf8fb4       0         0         0       30d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=9bbbf8fb4
replicaset.apps/stock-admin-9c5d4c9df       0         0         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=9c5d4c9df
replicaset.apps/stock-admin-b47f4d965       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=b47f4d965
replicaset.apps/stock-admin-b8bbd5567       0         0         0       34d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=b8bbd5567
replicaset.apps/stock-admin-b959549d5       0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=b959549d5
replicaset.apps/stock-admin-b96676888       0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=b96676888
replicaset.apps/stock-admin-bb95d4b7f       0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=bb95d4b7f
replicaset.apps/stock-admin-bc9995574       0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=bc9995574
replicaset.apps/stock-admin-bdcbbf8d5       0         0         0       34d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=bdcbbf8d5
replicaset.apps/stock-admin-c5c5cf85d       0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=c5c5cf85d
replicaset.apps/stock-admin-c647b74f5       0         0         0       15d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=c647b74f5
replicaset.apps/stock-admin-c8cd6d8f9       0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=c8cd6d8f9
replicaset.apps/stock-admin-cd564655b       0         0         0       29d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=cd564655b
replicaset.apps/stock-admin-cd9c555d7       0         0         0       12d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=cd9c555d7
replicaset.apps/stock-admin-cf75f949d       0         0         0       21d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=cf75f949d
replicaset.apps/stock-admin-cf8797f6        0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=cf8797f6
replicaset.apps/stock-admin-d5cff4d65       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=d5cff4d65
replicaset.apps/stock-admin-d5fdb7bc6       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=d5fdb7bc6
replicaset.apps/stock-admin-d6856495b       0         0         0       14d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=d6856495b
replicaset.apps/stock-admin-d74957fd7       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=d74957fd7
replicaset.apps/stock-admin-d7dd8f8bf       0         0         0       31d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=d7dd8f8bf
replicaset.apps/stock-admin-dbb65bcd6       0         0         0       26d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=dbb65bcd6
replicaset.apps/stock-admin-ddcd56d8b       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=ddcd56d8b
replicaset.apps/stock-admin-f6856cfb9       0         0         0       20d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=f6856cfb9
replicaset.apps/stock-admin-f68578bb5       0         0         0       23d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=f68578bb5
replicaset.apps/stock-admin-f7d556f95       0         0         0       36d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=f7d556f95
replicaset.apps/stock-admin-f96c45bb4       0         0         0       35d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=f96c45bb4
replicaset.apps/stock-admin-fb87c56c8       0         0         0       32d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=fb87c56c8
replicaset.apps/stock-admin-fc5c79b54       0         0         0       18d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=fc5c79b54
replicaset.apps/stock-admin-fc97f8d44       0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=fc97f8d44
replicaset.apps/stock-admin-fcb7d6          0         0         0       24d   admin        ghcr.io/phanthienquoc/stockdividend/admin:12d63b4     app=stock-admin,pod-template-hash=fcb7d6
replicaset.apps/stock-backend-54596d99d6    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=54596d99d6
replicaset.apps/stock-backend-5486b78445    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5486b78445
replicaset.apps/stock-backend-5489c5b485    0         0         0       34d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5489c5b485
replicaset.apps/stock-backend-54975d9c57    0         0         0       25d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=54975d9c57
replicaset.apps/stock-backend-549796df58    0         0         0       30d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=549796df58
replicaset.apps/stock-backend-54cfdb7f4f    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=54cfdb7f4f
replicaset.apps/stock-backend-54fbc4cf78    0         0         0       16d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=54fbc4cf78
replicaset.apps/stock-backend-5548bcd87f    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5548bcd87f
replicaset.apps/stock-backend-5548c86b4c    0         0         0       33d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5548c86b4c
replicaset.apps/stock-backend-5556848869    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5556848869
replicaset.apps/stock-backend-559b9b95d8    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=559b9b95d8
replicaset.apps/stock-backend-55bbc48776    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=55bbc48776
replicaset.apps/stock-backend-55bcb746f7    0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=55bcb746f7
replicaset.apps/stock-backend-55f85ddc45    0         0         0       35d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=55f85ddc45
replicaset.apps/stock-backend-55fcbb8b94    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=55fcbb8b94
replicaset.apps/stock-backend-564bfb98d7    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=564bfb98d7
replicaset.apps/stock-backend-56575489f9    0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=56575489f9
replicaset.apps/stock-backend-5696f55888    0         0         0       35d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5696f55888
replicaset.apps/stock-backend-5699b96fdc    0         0         0       19d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5699b96fdc
replicaset.apps/stock-backend-56c957cbfb    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=56c957cbfb
replicaset.apps/stock-backend-56c9db6dc8    0         0         0       35d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=56c9db6dc8
replicaset.apps/stock-backend-56f9f6d55     0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=56f9f6d55
replicaset.apps/stock-backend-5765d467db    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5765d467db
replicaset.apps/stock-backend-576fb79c78    0         0         0       37d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=576fb79c78
replicaset.apps/stock-backend-5796467fbd    0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5796467fbd
replicaset.apps/stock-backend-57ccb8ff6     1         1         1       56d   backend      ghcr.io/phanthienquoc/stockdividend/backend:23b2878   app=stock-backend,pod-template-hash=57ccb8ff6
replicaset.apps/stock-backend-58464f567d    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=58464f567d
replicaset.apps/stock-backend-584bd48597    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=584bd48597
replicaset.apps/stock-backend-588d4747d6    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=588d4747d6
replicaset.apps/stock-backend-589d99887c    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=589d99887c
replicaset.apps/stock-backend-5947569d87    0         0         0       23d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5947569d87
replicaset.apps/stock-backend-594f696b46    0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=594f696b46
replicaset.apps/stock-backend-594f7685d6    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=594f7685d6
replicaset.apps/stock-backend-5955f998d     0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5955f998d
replicaset.apps/stock-backend-5975fd7c67    0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5975fd7c67
replicaset.apps/stock-backend-5998b79d76    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5998b79d76
replicaset.apps/stock-backend-59bd95c977    0         0         0       35d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=59bd95c977
replicaset.apps/stock-backend-59f5f98664    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=59f5f98664
replicaset.apps/stock-backend-59f7ff6fc     0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=59f7ff6fc
replicaset.apps/stock-backend-59ffbbf6dc    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=59ffbbf6dc
replicaset.apps/stock-backend-5b4548d6b4    0         0         0       39d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5b4548d6b4
replicaset.apps/stock-backend-5b67b496dc    0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5b67b496dc
replicaset.apps/stock-backend-5b6b76f694    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5b6b76f694
replicaset.apps/stock-backend-5b978b44bc    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5b978b44bc
replicaset.apps/stock-backend-5bb8754458    0         0         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5bb8754458
replicaset.apps/stock-backend-5bcdf9556c    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5bcdf9556c
replicaset.apps/stock-backend-5bff86c8c8    0         0         0       26d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5bff86c8c8
replicaset.apps/stock-backend-5c69c554d4    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5c69c554d4
replicaset.apps/stock-backend-5c9f77fc55    0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5c9f77fc55
replicaset.apps/stock-backend-5ccb86cfc8    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5ccb86cfc8
replicaset.apps/stock-backend-5cd96bd67d    0         0         0       30d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5cd96bd67d
replicaset.apps/stock-backend-5cdb66fc67    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5cdb66fc67
replicaset.apps/stock-backend-5cff6d5655    0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5cff6d5655
replicaset.apps/stock-backend-5dc5df5bd6    0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5dc5df5bd6
replicaset.apps/stock-backend-5f45f875f     0         0         0       30d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5f45f875f
replicaset.apps/stock-backend-5f5bddf746    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5f5bddf746
replicaset.apps/stock-backend-5f6dd74868    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5f6dd74868
replicaset.apps/stock-backend-5fbd575b95    0         0         0       30d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5fbd575b95
replicaset.apps/stock-backend-5fc566dd8f    0         0         0       16d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5fc566dd8f
replicaset.apps/stock-backend-5ff54f5c74    0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5ff54f5c74
replicaset.apps/stock-backend-5ffc6fbc8     0         0         0       30d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=5ffc6fbc8
replicaset.apps/stock-backend-644699c8f8    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=644699c8f8
replicaset.apps/stock-backend-646948bc9b    0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=646948bc9b
replicaset.apps/stock-backend-6478977f4b    0         0         0       22d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6478977f4b
replicaset.apps/stock-backend-64cfd889d8    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=64cfd889d8
replicaset.apps/stock-backend-64dbf998b6    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=64dbf998b6
replicaset.apps/stock-backend-64fd565       0         0         0       34d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=64fd565
replicaset.apps/stock-backend-6547946847    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6547946847
replicaset.apps/stock-backend-65dcbc59f9    0         0         0       22d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=65dcbc59f9
replicaset.apps/stock-backend-6647646874    0         0         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6647646874
replicaset.apps/stock-backend-66b579b978    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=66b579b978
replicaset.apps/stock-backend-675c44854c    0         0         0       16d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=675c44854c
replicaset.apps/stock-backend-676bbb7dd7    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=676bbb7dd7
replicaset.apps/stock-backend-67c5f86579    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=67c5f86579
replicaset.apps/stock-backend-67c9fdc489    0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=67c9fdc489
replicaset.apps/stock-backend-68458d6cdf    0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=68458d6cdf
replicaset.apps/stock-backend-684658f67f    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=684658f67f
replicaset.apps/stock-backend-68845c65b4    0         0         0       23d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=68845c65b4
replicaset.apps/stock-backend-689694fcb     0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=689694fcb
replicaset.apps/stock-backend-689b896654    0         0         0       17d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=689b896654
replicaset.apps/stock-backend-689d78bd96    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=689d78bd96
replicaset.apps/stock-backend-68f45cd6b8    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=68f45cd6b8
replicaset.apps/stock-backend-694cfd6c85    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=694cfd6c85
replicaset.apps/stock-backend-695977497f    0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=695977497f
replicaset.apps/stock-backend-6975777c78    0         0         0       33d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6975777c78
replicaset.apps/stock-backend-697db585db    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=697db585db
replicaset.apps/stock-backend-69cbb67579    0         0         0       32d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=69cbb67579
replicaset.apps/stock-backend-69dc97d89b    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=69dc97d89b
replicaset.apps/stock-backend-69fbc94c4b    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=69fbc94c4b
replicaset.apps/stock-backend-6b4b9749b9    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6b4b9749b9
replicaset.apps/stock-backend-6bb5f79dd4    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6bb5f79dd4
replicaset.apps/stock-backend-6bb7f8c4f     0         0         0       25d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6bb7f8c4f
replicaset.apps/stock-backend-6bbfd66c49    0         0         0       32d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6bbfd66c49
replicaset.apps/stock-backend-6bc874575d    1         1         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6bc874575d
replicaset.apps/stock-backend-6bd68b7db8    0         0         0       32d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6bd68b7db8
replicaset.apps/stock-backend-6bd75fff54    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6bd75fff54
replicaset.apps/stock-backend-6c76997988    0         0         0       32d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6c76997988
replicaset.apps/stock-backend-6c7c47c459    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6c7c47c459
replicaset.apps/stock-backend-6c8f87f9b4    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6c8f87f9b4
replicaset.apps/stock-backend-6c9bfb65d7    0         0         0       23d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6c9bfb65d7
replicaset.apps/stock-backend-6c9d65bb96    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6c9d65bb96
replicaset.apps/stock-backend-6c9dc6fdc9    0         0         0       16d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6c9dc6fdc9
replicaset.apps/stock-backend-6cdb64498b    0         0         0       17d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6cdb64498b
replicaset.apps/stock-backend-6d447569b6    0         0         0       34d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6d447569b6
replicaset.apps/stock-backend-6d645cd66d    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6d645cd66d
replicaset.apps/stock-backend-6d649676c4    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6d649676c4
replicaset.apps/stock-backend-6d7cd68d7f    0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6d7cd68d7f
replicaset.apps/stock-backend-6d8979fd5d    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6d8979fd5d
replicaset.apps/stock-backend-6dbf8c4b8     0         0         0       18d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6dbf8c4b8
replicaset.apps/stock-backend-6df8fcc47d    0         0         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6df8fcc47d
replicaset.apps/stock-backend-6f68c4dbd7    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6f68c4dbd7
replicaset.apps/stock-backend-6f776c964c    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6f776c964c
replicaset.apps/stock-backend-6f9589b578    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6f9589b578
replicaset.apps/stock-backend-6f95cc96d7    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6f95cc96d7
replicaset.apps/stock-backend-6fbcc7779d    0         0         0       33d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6fbcc7779d
replicaset.apps/stock-backend-6fcbd9768c    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6fcbd9768c
replicaset.apps/stock-backend-6fd58899dc    0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6fd58899dc
replicaset.apps/stock-backend-6fd84c544c    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6fd84c544c
replicaset.apps/stock-backend-6fff8b4479    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=6fff8b4479
replicaset.apps/stock-backend-74466c858f    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=74466c858f
replicaset.apps/stock-backend-7454c6c585    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7454c6c585
replicaset.apps/stock-backend-747c949b4     0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=747c949b4
replicaset.apps/stock-backend-74c99cd67c    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=74c99cd67c
replicaset.apps/stock-backend-74d958c7b     0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=74d958c7b
replicaset.apps/stock-backend-75947776bf    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=75947776bf
replicaset.apps/stock-backend-75fdcf6f55    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=75fdcf6f55
replicaset.apps/stock-backend-766b4f47d6    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=766b4f47d6
replicaset.apps/stock-backend-76bb7d645b    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=76bb7d645b
replicaset.apps/stock-backend-77455f4f89    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=77455f4f89
replicaset.apps/stock-backend-777bcb965b    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=777bcb965b
replicaset.apps/stock-backend-777cccb4ff    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=777cccb4ff
replicaset.apps/stock-backend-778d89767     0         0         0       18d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=778d89767
replicaset.apps/stock-backend-786b76d66f    0         0         0       22d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=786b76d66f
replicaset.apps/stock-backend-786c7cf779    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=786c7cf779
replicaset.apps/stock-backend-7884bd5b77    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7884bd5b77
replicaset.apps/stock-backend-7889dcb846    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7889dcb846
replicaset.apps/stock-backend-789cc5f74f    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=789cc5f74f
replicaset.apps/stock-backend-789d67cb98    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=789d67cb98
replicaset.apps/stock-backend-789dcd9498    0         0         0       52d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=789dcd9498
replicaset.apps/stock-backend-7949978cf8    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7949978cf8
replicaset.apps/stock-backend-796464bdc5    0         0         0       26d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=796464bdc5
replicaset.apps/stock-backend-7987b75cb7    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7987b75cb7
replicaset.apps/stock-backend-7995d7968d    0         0         0       19d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7995d7968d
replicaset.apps/stock-backend-79bb67dbb     0         0         0       35d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=79bb67dbb
replicaset.apps/stock-backend-79db6d46      0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=79db6d46
replicaset.apps/stock-backend-79dd6ddcbf    0         0         0       34d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=79dd6ddcbf
replicaset.apps/stock-backend-7b4578f89b    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7b4578f89b
replicaset.apps/stock-backend-7b4878c955    0         0         0       17d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7b4878c955
replicaset.apps/stock-backend-7b889c5ddd    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7b889c5ddd
replicaset.apps/stock-backend-7b9489b7f4    0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7b9489b7f4
replicaset.apps/stock-backend-7bd7694875    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7bd7694875
replicaset.apps/stock-backend-7c649c6fb7    0         0         0       23d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7c649c6fb7
replicaset.apps/stock-backend-7c6667dcf5    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7c6667dcf5
replicaset.apps/stock-backend-7c869f9dcc    0         0         0       16d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7c869f9dcc
replicaset.apps/stock-backend-7c8bc66c6b    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7c8bc66c6b
replicaset.apps/stock-backend-7cd45fd87c    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7cd45fd87c
replicaset.apps/stock-backend-7d5d6fb4c9    0         0         0       33d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7d5d6fb4c9
replicaset.apps/stock-backend-7d6bb9f5dc    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7d6bb9f5dc
replicaset.apps/stock-backend-7d8f5bdfdc    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7d8f5bdfdc
replicaset.apps/stock-backend-7d94c88fb4    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7d94c88fb4
replicaset.apps/stock-backend-7dc87ccfc9    0         0         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7dc87ccfc9
replicaset.apps/stock-backend-7f44bdcf68    0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7f44bdcf68
replicaset.apps/stock-backend-7f6c9d776f    0         0         0       21d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7f6c9d776f
replicaset.apps/stock-backend-7fbbdb6ff8    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7fbbdb6ff8
replicaset.apps/stock-backend-7fd8b99c86    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7fd8b99c86
replicaset.apps/stock-backend-7ffd8b6fc6    0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=7ffd8b6fc6
replicaset.apps/stock-backend-844577ffc8    0         0         0       30d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=844577ffc8
replicaset.apps/stock-backend-8446bcc676    0         0         0       22d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8446bcc676
replicaset.apps/stock-backend-846948869     0         0         0       18d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=846948869
replicaset.apps/stock-backend-847bd8dbdc    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=847bd8dbdc
replicaset.apps/stock-backend-84c56cf67f    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=84c56cf67f
replicaset.apps/stock-backend-84c79458ff    0         0         0       28d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=84c79458ff
replicaset.apps/stock-backend-84cd8cc96b    0         0         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=84cd8cc96b
replicaset.apps/stock-backend-84dfdfd9b8    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=84dfdfd9b8
replicaset.apps/stock-backend-8557955595    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8557955595
replicaset.apps/stock-backend-8557b56859    0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8557b56859
replicaset.apps/stock-backend-8569457bbb    0         0         0       18d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8569457bbb
replicaset.apps/stock-backend-8579cfb48b    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8579cfb48b
replicaset.apps/stock-backend-858f45c799    0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=858f45c799
replicaset.apps/stock-backend-859d77f899    0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=859d77f899
replicaset.apps/stock-backend-85bf5fc95b    0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=85bf5fc95b
replicaset.apps/stock-backend-85c6c694df    0         0         0       22d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=85c6c694df
replicaset.apps/stock-backend-865b4499bf    0         0         0       25d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=865b4499bf
replicaset.apps/stock-backend-866cf5498d    0         0         0       16d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=866cf5498d
replicaset.apps/stock-backend-866fb5fd57    0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=866fb5fd57
replicaset.apps/stock-backend-8686dc4fd     0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8686dc4fd
replicaset.apps/stock-backend-86cc69f958    0         0         0       17d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=86cc69f958
replicaset.apps/stock-backend-86dbfb698     0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=86dbfb698
replicaset.apps/stock-backend-86f875bd4d    0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=86f875bd4d
replicaset.apps/stock-backend-88c58d494     0         0         0       15d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=88c58d494
replicaset.apps/stock-backend-8d9d4f68d     0         0         0       26d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8d9d4f68d
replicaset.apps/stock-backend-8dfd4454c     0         0         0       19d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8dfd4454c
replicaset.apps/stock-backend-8f7f44fcf     0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=8f7f44fcf
replicaset.apps/stock-backend-94cc499c9     0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=94cc499c9
replicaset.apps/stock-backend-968696496     0         0         0       18d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=968696496
replicaset.apps/stock-backend-977768668     0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=977768668
replicaset.apps/stock-backend-99646ffd9     0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=99646ffd9
replicaset.apps/stock-backend-99b777c9      0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=99b777c9
replicaset.apps/stock-backend-9b69d5db      0         0         0       25d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=9b69d5db
replicaset.apps/stock-backend-9b8886fd9     0         0         0       33d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=9b8886fd9
replicaset.apps/stock-backend-9b9f69d99     0         0         0       33d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=9b9f69d99
replicaset.apps/stock-backend-9bbf9c9b9     0         0         0       19d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=9bbf9c9b9
replicaset.apps/stock-backend-9df7bdd55     0         0         0       31d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=9df7bdd55
replicaset.apps/stock-backend-b4859fb74     0         0         0       19d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=b4859fb74
replicaset.apps/stock-backend-b64f9bdd8     0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=b64f9bdd8
replicaset.apps/stock-backend-b9564f5bf     0         0         0       29d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=b9564f5bf
replicaset.apps/stock-backend-b95fd5f7b     0         0         0       12d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=b95fd5f7b
replicaset.apps/stock-backend-bbcd56c76     0         0         0       26d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=bbcd56c76
replicaset.apps/stock-backend-bc789675f     0         0         0       14d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=bc789675f
replicaset.apps/stock-backend-bd8dfc97b     0         0         0       26d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=bd8dfc97b
replicaset.apps/stock-backend-bfbcf4957     0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=bfbcf4957
replicaset.apps/stock-backend-c7b9cb8f5     0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=c7b9cb8f5
replicaset.apps/stock-backend-cb75cb78c     0         0         0       26d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=cb75cb78c
replicaset.apps/stock-backend-cf7bb957f     0         0         0       34d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=cf7bb957f
replicaset.apps/stock-backend-cf8b475bd     0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=cf8b475bd
replicaset.apps/stock-backend-cf9f49f86     0         0         0       24d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=cf9f49f86
replicaset.apps/stock-backend-d6b79877b     0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=d6b79877b
replicaset.apps/stock-backend-d6d7f7887     0         0         0       25d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=d6d7f7887
replicaset.apps/stock-backend-d85844b4      0         0         0       23d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=d85844b4
replicaset.apps/stock-backend-d9946b74f     0         0         0       19d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=d9946b74f
replicaset.apps/stock-backend-ddb854c99     0         0         0       23d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=ddb854c99
replicaset.apps/stock-backend-f45cb8fbd     0         0         0       27d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=f45cb8fbd
replicaset.apps/stock-backend-f59d758d4     0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=f59d758d4
replicaset.apps/stock-backend-f7bfc6c9f     0         0         0       17d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=f7bfc6c9f
replicaset.apps/stock-backend-fb9c5dbd5     0         0         0       13d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=fb9c5dbd5
replicaset.apps/stock-backend-fbc8764b4     0         0         0       36d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=fbc8764b4
replicaset.apps/stock-backend-ff56f7bdb     0         0         0       20d   backend      ghcr.io/phanthienquoc/stockdividend/backend:12d63b4   app=stock-backend,pod-template-hash=ff56f7bdb
replicaset.apps/stock-frontend-74546898cb   1         0         0       14d   frontend     ghcr.io/phanthienquoc/stockdividend/user:23b2878      app=stock-frontend,pod-template-hash=74546898cb
replicaset.apps/stock-frontend-79c57845df   1         1         1       56d   frontend     ghcr.io/phanthienquoc/stockdividend/user:23b2878      app=stock-frontend,pod-template-hash=79c57845df

### Namespaced objects and storage snapshot references in media-prod (names only; no Secret/ConfigMap values)
configmap/kube-root-ca.crt
endpoints/media-generation
endpoints/media-generation-frontend
pod/media-generation-665d86ff54-4664l
pod/media-generation-frontend-58d8bbc67-lwhhf
secret/ghcr-pull
secret/media-generation-secrets
secret/media-mrcute-tls
serviceaccount/default
service/media-generation
service/media-generation-frontend
order.acme.cert-manager.io/media-mrcute-tls-1-249384574
deployment.apps/media-generation
deployment.apps/media-generation-frontend
replicaset.apps/media-generation-557898ffc5
replicaset.apps/media-generation-5c9b76dfb9
replicaset.apps/media-generation-646c797f66
replicaset.apps/media-generation-665d86ff54
replicaset.apps/media-generation-6857cc5595
replicaset.apps/media-generation-6b6f875997
replicaset.apps/media-generation-6c68f86bf4
replicaset.apps/media-generation-6f66c4dc4d
replicaset.apps/media-generation-74bdb964d8
replicaset.apps/media-generation-86c45c6686
replicaset.apps/media-generation-8d887c6c9
replicaset.apps/media-generation-frontend-5445d66b98
replicaset.apps/media-generation-frontend-55447798b6
replicaset.apps/media-generation-frontend-58c8dd5969
replicaset.apps/media-generation-frontend-58d8bbc67
replicaset.apps/media-generation-frontend-597b779c9d
replicaset.apps/media-generation-frontend-5df46b89c
replicaset.apps/media-generation-frontend-64dfb87d84
replicaset.apps/media-generation-frontend-667fb49d95
replicaset.apps/media-generation-frontend-7d4cc58775
replicaset.apps/media-generation-frontend-867d5d8b77
replicaset.apps/media-generation-frontend-c44458c86
certificaterequest.cert-manager.io/media-mrcute-tls-1
certificate.cert-manager.io/media-mrcute-tls
endpointslice.discovery.k8s.io/media-generation-frontend-46jzx
endpointslice.discovery.k8s.io/media-generation-hqjkh
podmetrics.metrics.k8s.io/media-generation-665d86ff54-4664l
podmetrics.metrics.k8s.io/media-generation-frontend-58d8bbc67-lwhhf
ingress.networking.k8s.io/media
### Ingress hosts/TLS secret references and published addresses (names only): media-prod
media	media.mrcute.space	media.mrcute.space	media-mrcute-tls	10.0.0.120
DNS ownership is not inferred; reconcile these hostnames with authoritative DNS/provider records before deletion.
### Common workload status: media-prod
NAME                                            READY   STATUS    RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
pod/media-generation-665d86ff54-4664l           1/1     Running   0          13d   10.42.0.155   tce-k3s-01   <none>           <none>
pod/media-generation-frontend-58d8bbc67-lwhhf   1/1     Running   0          13d   10.42.0.154   tce-k3s-01   <none>           <none>

NAME                                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE   SELECTOR
service/media-generation            ClusterIP   10.43.252.95   <none>        3000/TCP   45d   app=media-generation
service/media-generation-frontend   ClusterIP   10.43.48.52    <none>        80/TCP     45d   app=media-generation-frontend

NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS                  IMAGES                                                                                                                    SELECTOR
deployment.apps/media-generation            1/1     1            1           45d   media-generation            ghcr.io/phanthienquoc/media-generation/backend@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d    app=media-generation
deployment.apps/media-generation-frontend   1/1     1            1           45d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a   app=media-generation-frontend

NAME                                                   DESIRED   CURRENT   READY   AGE   CONTAINERS                  IMAGES                                                                                                                    SELECTOR
replicaset.apps/media-generation-557898ffc5            0         0         0       44d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-56179ff                                                        app=media-generation,pod-template-hash=557898ffc5
replicaset.apps/media-generation-5c9b76dfb9            0         0         0       31d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8                                                        app=media-generation,pod-template-hash=5c9b76dfb9
replicaset.apps/media-generation-646c797f66            0         0         0       15d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8                                                        app=media-generation,pod-template-hash=646c797f66
replicaset.apps/media-generation-665d86ff54            1         1         1       13d   media-generation            ghcr.io/phanthienquoc/media-generation/backend@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d    app=media-generation,pod-template-hash=665d86ff54
replicaset.apps/media-generation-6857cc5595            0         0         0       44d   media-generation            ghcr.io/phanthienquoc/media-generation-backend:prod-v0.3.0-85a354f                                                        app=media-generation,pod-template-hash=6857cc5595
replicaset.apps/media-generation-6b6f875997            0         0         0       44d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-a34d8ca                                                        app=media-generation,pod-template-hash=6b6f875997
replicaset.apps/media-generation-6c68f86bf4            0         0         0       14d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8                                                        app=media-generation,pod-template-hash=6c68f86bf4
replicaset.apps/media-generation-6f66c4dc4d            0         0         0       39d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-362cb81                                                        app=media-generation,pod-template-hash=6f66c4dc4d
replicaset.apps/media-generation-74bdb964d8            0         0         0       44d   media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-5229584                                                        app=media-generation,pod-template-hash=74bdb964d8
replicaset.apps/media-generation-86c45c6686            0         0         0       44d   media-generation            ghcr.io/phanthienquoc/media-generation-backend:prod-v0.3.0-cb5355d                                                        app=media-generation,pod-template-hash=86c45c6686
replicaset.apps/media-generation-8d887c6c9             0         0         0       44d   media-generation            ghcr.io/phanthienquoc/media-generation-backend:prod-v0.3.0-bf6c55a                                                        app=media-generation,pod-template-hash=8d887c6c9
replicaset.apps/media-generation-frontend-5445d66b98   0         0         0       14d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8                                                       app=media-generation-frontend,pod-template-hash=5445d66b98
replicaset.apps/media-generation-frontend-55447798b6   0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation-frontend:prod-v0.3.0-cc47a89                                                       app=media-generation-frontend,pod-template-hash=55447798b6
replicaset.apps/media-generation-frontend-58c8dd5969   0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation-frontend:prod-v0.3.0-85a354f                                                       app=media-generation-frontend,pod-template-hash=58c8dd5969
replicaset.apps/media-generation-frontend-58d8bbc67    1         1         1       13d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a   app=media-generation-frontend,pod-template-hash=58d8bbc67
replicaset.apps/media-generation-frontend-597b779c9d   0         0         0       31d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8                                                       app=media-generation-frontend,pod-template-hash=597b779c9d
replicaset.apps/media-generation-frontend-5df46b89c    0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-56179ff                                                       app=media-generation-frontend,pod-template-hash=5df46b89c
replicaset.apps/media-generation-frontend-64dfb87d84   0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-5229584                                                       app=media-generation-frontend,pod-template-hash=64dfb87d84
replicaset.apps/media-generation-frontend-667fb49d95   0         0         0       39d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-362cb81                                                       app=media-generation-frontend,pod-template-hash=667fb49d95
replicaset.apps/media-generation-frontend-7d4cc58775   0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-a34d8ca                                                       app=media-generation-frontend,pod-template-hash=7d4cc58775
replicaset.apps/media-generation-frontend-867d5d8b77   0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation-frontend:prod-v0.3.0-bf6c55a                                                       app=media-generation-frontend,pod-template-hash=867d5d8b77
replicaset.apps/media-generation-frontend-c44458c86    0         0         0       44d   media-generation-frontend   ghcr.io/phanthienquoc/media-generation-frontend:prod-v0.3.0-cb5355d                                                       app=media-generation-frontend,pod-template-hash=c44458c86

### StorageClass inventory
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  84d
Preflight passed: target namespaces have no PVCs, PV claims or VolumeSnapshot references.
Read-only preflight complete. No Kubernetes resources were changed.
decommission_preflight_status: storage-clean

### Dedicated Media runner retirement evidence
media_runner_service=active enabled=enabled listener=present
GitHub runner registration is not inferred by this host inspection; verify it in the Media repository/organization settings.

### GitOps drift
Prepared checksum-verified cert-manager v1.21.1 manifest.
status: clean

### Images
cert-manager       cert-manager                quay.io/jetstack/cert-manager-controller:v1.21.1
cert-manager       cert-manager-cainjector     quay.io/jetstack/cert-manager-cainjector:v1.21.1
cert-manager       cert-manager-webhook        quay.io/jetstack/cert-manager-webhook:v1.21.1
kube-system        coredns                     rancher/mirrored-coredns-coredns:1.14.6
kube-system        local-path-provisioner      rancher/local-path-provisioner:v0.0.36
kube-system        metrics-server              rancher/mirrored-metrics-server:v0.9.0
kube-system        traefik                     rancher/mirrored-library-traefik:3.7.8
media-prod         media-generation            ghcr.io/phanthienquoc/media-generation/backend@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d
media-prod         media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a
microfe-platform   keycloak                    quay.io/keycloak/keycloak:26.8.1
microfe-platform   microfe-auth                ghcr.io/phanthienquoc/auth-service/auth:prod-v1.0.0-ceb2688
microfe-platform   microfe-shell               ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd
microfe-platform   microfe-ws                  ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d
microfe-platform   nats                        nats:2.12-alpine
stock-prod         stock-admin                 ghcr.io/phanthienquoc/stockdividend/admin:12d63b4
stock-prod         stock-backend               ghcr.io/phanthienquoc/stockdividend/backend:12d63b4
stock-prod         stock-frontend              ghcr.io/phanthienquoc/stockdividend/user:23b2878
tce-prod           tce-frontend                ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-e75e338
tce-prod           tce-service                 ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-e75e338
NAMESPACE          NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
cert-manager       cert-manager                ClusterIP      10.43.138.27    <none>        9402/TCP                     81d
cert-manager       cert-manager-cainjector     ClusterIP      10.43.135.132   <none>        9402/TCP                     81d
cert-manager       cert-manager-webhook        ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             81d
default            kubernetes                  ClusterIP      10.43.0.1       <none>        443/TCP                      84d
kube-system        kube-dns                    ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       84d
kube-system        metrics-server              ClusterIP      10.43.120.41    <none>        443/TCP                      84d
kube-system        traefik                     LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   84d
media-prod         media-generation            ClusterIP      10.43.252.95    <none>        3000/TCP                     45d
media-prod         media-generation-frontend   ClusterIP      10.43.48.52     <none>        80/TCP                       45d
microfe-platform   keycloak                    ClusterIP      10.43.142.95    <none>        80/TCP,9000/TCP              29d
microfe-platform   microfe-auth                ClusterIP      10.43.83.168    <none>        80/TCP                       39d
microfe-platform   microfe-shell               ClusterIP      10.43.6.23      <none>        80/TCP                       39d
microfe-platform   microfe-ws                  ClusterIP      10.43.86.34     <none>        8080/TCP                     39d
microfe-platform   nats                        ClusterIP      10.43.147.69    <none>        4222/TCP,8222/TCP            36d
stock-prod         backend                     ClusterIP      10.43.46.139    <none>        8080/TCP                     56d
stock-prod         stock-admin                 ClusterIP      10.43.97.150    <none>        3000/TCP                     52d
stock-prod         stock-backend               ClusterIP      10.43.247.219   <none>        8080/TCP                     56d
stock-prod         stock-frontend              ClusterIP      10.43.53.102    <none>        3000/TCP                     56d
tce-prod           tce-frontend                ClusterIP      10.43.99.130    <none>        80/TCP                       81d
tce-prod           tce-service                 ClusterIP      10.43.189.227   <none>        8210/TCP                     81d
NAMESPACE          NAME                               CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
media-prod         media                              traefik   media.mrcute.space                                             10.0.0.120   80, 443   45d
microfe-platform   keycloak-public                    traefik   sso.mrcute.space                                               10.0.0.120   80, 443   29d
microfe-platform   keycloak-registration-rate-limit   traefik   sso.mrcute.space                                               10.0.0.120   80, 443   17d
microfe-platform   microfe-public                     traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space             10.0.0.120   80, 443   39d
stock-prod         stock                              traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   52d
stock-prod         stock-ingress                      traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   56d
tce-prod           tce                                traefik   tce.mrcute.space                                               10.0.0.120   80, 443   81d

## K3s service
active
enabled

### K3s recent warnings (last 2h)

## Keycloak diagnostics
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
keycloak   0/0     0            0           29d   keycloak     quay.io/keycloak/keycloak:26.8.1   app.kubernetes.io/name=keycloak
error: timed out waiting for the condition

### Public OIDC probes (status and latency only)
https://sso.mrcute.space/realms/master/.well-known/openid-configuration http_code=503 time_total=0.085470s remote_ip=132.226.175.206
https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration http_code=503 time_total=0.050042s remote_ip=132.226.175.206
