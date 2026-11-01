# VPS inspection

Generated: 2026-11-01T20:13:05+00:00

## Host
Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       3.6Gi       3.7Gi        84Mi        16Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   25G   21G  55% /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   25G   21G  55% /
disk_pressure: normal (55%)
 20:13:05 up 184 days,  6:03,  0 users,  load average: 0.92, 0.44, 0.24

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
68K	/var/log/unified-monitoring-agent
76K	/var/log/containers
132K	/var/log/apt
23M	/var/log/oracle-cloud-agent
236M	/var/lib/rancher/k3s
236M	/var/lib/rancher/k3s/data
753M	/var/log/journal
1.2G	/var/log

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
21684 /opt/media-actions-runner/bin/Runner.Listener run --startuptype service
1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
3594292 /opt/actions-runner/bin/Runner.Worker spawnclient 154 160
  actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service loaded    active   running GitHub Actions Runner (phanthienquoc-media-generation.media-generation-k3s-01)
  actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service           loaded    active   running GitHub Actions Runner (phanthienquoc-platform-infra.platform-k3s-01)
runner_service: active
runner_service_enabled: enabled

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
containerd.io/jammy 2.4.2-3~ubuntu.22.04~jammy arm64 [upgradable from: 2.2.1-1~ubuntu.22.04~jammy]
docker-buildx-plugin/jammy 0.38.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 0.30.1-1~ubuntu.22.04~jammy]
docker-ce-cli/jammy 5:29.9.2-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce-rootless-extras/jammy 5:29.9.2-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce/jammy 5:29.9.2-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-compose-plugin/jammy 5.6.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5.0.1-1~ubuntu.22.04~jammy]
fwupd/jammy-updates 2.0.20-1ubuntu2~22.04.2 arm64 [upgradable from: 1.7.9-1~22.04.3]
iproute2/jammy-updates 5.15.0-1ubuntu2.2 arm64 [upgradable from: 5.15.0-1ubuntu2]
landscape-common/jammy-updates 23.02-0ubuntu1~22.04.7 arm64 [upgradable from: 23.02-0ubuntu1~22.04.6]
libapparmor1/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
libaudit-common/jammy-updates 1:3.0.7-1ubuntu0.1 all [upgradable from: 1:3.0.7-1build1]
libaudit1/jammy-updates 1:3.0.7-1ubuntu0.1 arm64 [upgradable from: 1:3.0.7-1build1]
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
python3-distupgrade/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
snapd/jammy-updates 2.77.1+ubuntu22.04.1 arm64 [upgradable from: 2.76.3+ubuntu22.04.1]
sosreport/jammy-updates 4.11.2-0ubuntu0~22.04.1 arm64 [upgradable from: 4.9.2-0ubuntu0~22.04.1]
tmux/jammy-updates 3.2a-4ubuntu0.3 arm64 [upgradable from: 3.2a-4ubuntu0.2]
ubuntu-advantage-tools/jammy-updates 38ubuntu0~22.04 all [upgradable from: 37.2ubuntu~22.04.1]
ubuntu-minimal/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-pro-client-l10n/jammy-updates 38ubuntu0~22.04 arm64 [upgradable from: 37.2ubuntu~22.04.1]
ubuntu-pro-client/jammy-updates 38ubuntu0~22.04 arm64 [upgradable from: 37.2ubuntu~22.04.1]
ubuntu-release-upgrader-core/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
ubuntu-server/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-standard/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
restart_required: yes

## K3s
Client Version: v1.36.3+k3s1
Kustomize Version: v5.8.1
NAME         STATUS   ROLES           AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION              CONTAINER-RUNTIME
tce-k3s-01   Ready    control-plane   71d   v1.36.3+k3s1   10.0.0.120    <none>        Ubuntu 22.04.5 LTS   6.8.0-1049-oracle (arm64)   containerd://2.3.2-k3s2
NAME               STATUS   AGE
cert-manager       Active   68d
default            Active   71d
k3s-debug          Active   24d
kube-node-lease    Active   71d
kube-public        Active   71d
kube-system        Active   71d
media-prod         Active   32d
microfe-platform   Active   26d
stock-prod         Active   43d
tce-prod           Active   71d
NAMESPACE          NAME                                        READY   STATUS             RESTARTS      AGE    IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager       cert-manager-75b96c9588-lgn7d               1/1     Running            0             68d    10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager       cert-manager-cainjector-b644b66f7-l8jdq     1/1     Running            1 (68d ago)   68d    10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager       cert-manager-webhook-76d97df888-wwq49       1/1     Running            0             68d    10.42.0.99    tce-k3s-01   <none>           <none>
kube-system        coredns-54996dc9b4-d68pf                    1/1     Running            0             71d    10.42.0.6     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-crd-mq7w8              0/1     Completed          0             71d    10.42.0.3     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-s2twj                  0/1     Completed          1 (71d ago)   71d    10.42.0.2     tce-k3s-01   <none>           <none>
kube-system        local-path-provisioner-58d557dc48-jbhhp     1/1     Running            1 (71d ago)   71d    10.42.0.5     tce-k3s-01   <none>           <none>
kube-system        metrics-server-6dc596dfb8-s2bzm             1/1     Running            0             71d    10.42.0.4     tce-k3s-01   <none>           <none>
kube-system        svclb-traefik-859779c1-7bwx2                2/2     Running            0             71d    10.42.0.7     tce-k3s-01   <none>           <none>
kube-system        traefik-59b7647586-gml84                    1/1     Running            0             71d    10.42.0.8     tce-k3s-01   <none>           <none>
media-prod         media-generation-665d86ff54-4664l           1/1     Running            0             15h    10.42.0.155   tce-k3s-01   <none>           <none>
media-prod         media-generation-frontend-58d8bbc67-lwhhf   1/1     Running            0             15h    10.42.0.154   tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-7b44b44dfb-ln4sw              1/1     Running            0             18h    10.42.0.153   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-5bc979dd77-txd28                 1/1     Running            0             18h    10.42.0.152   tce-k3s-01   <none>           <none>
microfe-platform   nats-7bc8d9f768-q682m                       1/1     Running            0             23d    10.42.0.178   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-565b8b9c8-lvkmp                 0/1     ImagePullBackOff   0             2m3s   10.42.0.171   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-9c5d4c9df-4bb45                 0/1     ImagePullBackOff   0             3h     10.42.0.168   tce-k3s-01   <none>           <none>
stock-prod         stock-backend-57ccb8ff6-d25jq               1/1     Running            0             43d    10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-b95fd5f7b-xstft               0/1     ImagePullBackOff   0             2m3s   10.42.0.172   tce-k3s-01   <none>           <none>
stock-prod         stock-frontend-79c57845df-z747s             1/1     Running            0             43d    10.42.0.56    tce-k3s-01   <none>           <none>

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
stock-prod	stock-admin-565b8b9c8-lvkmp	container	admin	ghcr.io/phanthienquoc/stockdividend/admin:12d63b4		false	0
stock-prod	stock-admin-9c5d4c9df-4bb45	container	admin	ghcr.io/phanthienquoc/stockdividend/admin:12d63b4		false	0
stock-prod	stock-backend-57ccb8ff6-d25jq	container	backend	ghcr.io/phanthienquoc/stockdividend/backend:23b2878	sha256:bcf5f7b1b660b5b93cd9d9f4f041db7e9166c89b084412fa4f66e8e4d9a43ad1	true	0
stock-prod	stock-backend-b95fd5f7b-xstft	container	backend	ghcr.io/phanthienquoc/stockdividend/backend:12d63b4		false	0
stock-prod	stock-frontend-79c57845df-z747s	container	frontend	ghcr.io/phanthienquoc/stockdividend/user:23b2878	sha256:bca44dd31869a4874a795c6e6ace51f9362731770f3ac9ca1ee8f3e608d6bf99	true	0
NAMESPACE          NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager       cert-manager                1/1     1            1           68d
cert-manager       cert-manager-cainjector     1/1     1            1           68d
cert-manager       cert-manager-webhook        1/1     1            1           68d
kube-system        coredns                     1/1     1            1           71d
kube-system        local-path-provisioner      1/1     1            1           71d
kube-system        metrics-server              1/1     1            1           71d
kube-system        traefik                     1/1     1            1           71d
media-prod         media-generation            1/1     1            1           32d
media-prod         media-generation-frontend   1/1     1            1           32d
microfe-platform   keycloak                    0/0     0            0           16d
microfe-platform   microfe-auth                0/0     0            0           26d
microfe-platform   microfe-shell               1/1     1            1           26d
microfe-platform   microfe-ws                  1/1     1            1           26d
microfe-platform   nats                        1/1     1            1           23d
stock-prod         stock-admin                 0/1     1            0           39d
stock-prod         stock-backend               1/1     1            1           43d
stock-prod         stock-frontend              1/1     0            1           43d
tce-prod           tce-frontend                0/0     0            0           68d
tce-prod           tce-service                 0/0     0            0           68d

### Pod failure evidence
stock-prod	stock-admin-565b8b9c8-lvkmp	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": no match for platform in manifest: not found
stock-prod	stock-admin-9c5d4c9df-4bb45	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": no match for platform in manifest: not found
stock-prod	stock-backend-b95fd5f7b-xstft	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": no match for platform in manifest: not found

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
	ghcr.io/phanthienquoc/microfe-shell@sha256:40715628ad7572654ce35dab0835aa8b875d1bf9a20e9a13d257a173feac17ec	sha256:e4577fe7033fba879827b7e4df656e13434d7a70757a3400a8909cab95e55206	false	25830438
	ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	false	25830437
	ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	false	65079739
	ghcr.io/phanthienquoc/microfe-ws@sha256:92e6799bed0dcbeedc1c05575b6416e6e16d27beeab627b21cf1cc34b70ee631	sha256:20bce89a7a7eb9d16ebca87519e5c3e914d89d513db6747a27a9096aa73ba8c2	false	64949303
ghcr.io/phanthienquoc/stockdividend/backend:23b2878		sha256:bcf5f7b1b660b5b93cd9d9f4f041db7e9166c89b084412fa4f66e8e4d9a43ad1	false	14420347
ghcr.io/phanthienquoc/stockdividend/user:23b2878		sha256:bca44dd31869a4874a795c6e6ace51f9362731770f3ac9ca1ee8f3e608d6bf99	false	66238963
ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-48e3842	ghcr.io/phanthienquoc/tce-dashboard/service@sha256:214aee66dadaeb5e5acd7ac03da6d7461f68571ed2ba8ef3ef73384f7f26300a	sha256:924df0921bfdb32ebd65d6d4b05823d3dc80357f9ab4289d9eea991a96778931	false	457622464
ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-e75e338	ghcr.io/phanthienquoc/tce-dashboard/service@sha256:1dc9d8c2136598a748bbb0aafc615a71aeb3f2a5099c335859536212723f35f0	sha256:d16e4e0a92f04c63bd4777c1b3f967c70da62df6c2f50c796b8daef0cc2e7e09	false	457620530
ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-e75e338	ghcr.io/phanthienquoc/tce-dashboard/web@sha256:0416f01f3cce813ead623403ee354d7e5ff4160d1bfc24c020cfd9387da3ec27	sha256:3f6764e54b88e7d88ceca48e9386d4f5601332efad7b3777610453353edd5e6e	false	75833971
quay.io/jetstack/cert-manager-cainjector:v1.21.1	quay.io/jetstack/cert-manager-cainjector@sha256:ccf6b919ec0500745a47a910118f834f9636d0aac1ff221245cd2557ed8c7c98	sha256:187d7de7d1d04dd40dbc62236b0e75eea4a0ae336b0de824c6e27e28fb102381	false	11030656
quay.io/jetstack/cert-manager-controller:v1.21.1	quay.io/jetstack/cert-manager-controller@sha256:416a2d76870d996460e62bd7f521bf14fa017be9e3e904aab92163a331fcb61a	sha256:5283ffc3ebd6cf46ecf84f5e56730734b3de8d3de456c3a909f0077b5337c55d	false	22296047
quay.io/jetstack/cert-manager-webhook:v1.21.1	quay.io/jetstack/cert-manager-webhook@sha256:d8b3961b51c8c7320633f8208dc46bf88aa13804d0f7cbe48a096b2c523cee42	sha256:4694bc08f6c866b0820ff7e82d673029b6d48ba0aaf79af528987ca114f426ec	false	17710712
quay.io/keycloak/keycloak:26.8.1	quay.io/keycloak/keycloak@sha256:79c623a22abacf3fe6c00a5fb30f5b7843d717b234033b80995891c06116d244	sha256:4e8f716cccbf94c5461d9e6cb1f600bc74ac4d9bcfdf572511bbbc7d783d0ae5	false	264143474
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

### GitOps drift
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
cert-manager       cert-manager                ClusterIP      10.43.138.27    <none>        9402/TCP                     68d
cert-manager       cert-manager-cainjector     ClusterIP      10.43.135.132   <none>        9402/TCP                     68d
cert-manager       cert-manager-webhook        ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             68d
default            kubernetes                  ClusterIP      10.43.0.1       <none>        443/TCP                      71d
kube-system        kube-dns                    ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       71d
kube-system        metrics-server              ClusterIP      10.43.120.41    <none>        443/TCP                      71d
kube-system        traefik                     LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   71d
media-prod         media-generation            ClusterIP      10.43.252.95    <none>        3000/TCP                     32d
media-prod         media-generation-frontend   ClusterIP      10.43.48.52     <none>        80/TCP                       32d
microfe-platform   keycloak                    ClusterIP      10.43.142.95    <none>        80/TCP,9000/TCP              16d
microfe-platform   microfe-auth                ClusterIP      10.43.83.168    <none>        80/TCP                       26d
microfe-platform   microfe-shell               ClusterIP      10.43.6.23      <none>        80/TCP                       26d
microfe-platform   microfe-ws                  ClusterIP      10.43.86.34     <none>        8080/TCP                     26d
microfe-platform   nats                        ClusterIP      10.43.147.69    <none>        4222/TCP,8222/TCP            23d
stock-prod         backend                     ClusterIP      10.43.46.139    <none>        8080/TCP                     43d
stock-prod         stock-admin                 ClusterIP      10.43.97.150    <none>        3000/TCP                     39d
stock-prod         stock-backend               ClusterIP      10.43.247.219   <none>        8080/TCP                     43d
stock-prod         stock-frontend              ClusterIP      10.43.53.102    <none>        3000/TCP                     43d
tce-prod           tce-frontend                ClusterIP      10.43.99.130    <none>        80/TCP                       68d
tce-prod           tce-service                 ClusterIP      10.43.189.227   <none>        8210/TCP                     68d
NAMESPACE          NAME                               CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
media-prod         media                              traefik   media.mrcute.space                                             10.0.0.120   80, 443   32d
microfe-platform   keycloak-public                    traefik   sso.mrcute.space                                               10.0.0.120   80, 443   16d
microfe-platform   keycloak-registration-rate-limit   traefik   sso.mrcute.space                                               10.0.0.120   80, 443   4d16h
microfe-platform   microfe-public                     traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space             10.0.0.120   80, 443   26d
stock-prod         stock                              traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   39d
stock-prod         stock-ingress                      traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   43d
tce-prod           tce                                traefik   tce.mrcute.space                                               10.0.0.120   80, 443   68d

## K3s service
active
enabled

### K3s recent warnings (last 2h)

## Keycloak diagnostics
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
keycloak   0/0     0            0           16d   keycloak     quay.io/keycloak/keycloak:26.8.1   app.kubernetes.io/name=keycloak
error: timed out waiting for the condition

### Public OIDC probes (status and latency only)
https://sso.mrcute.space/realms/master/.well-known/openid-configuration http_code=503 time_total=0.142724s remote_ip=132.226.175.206
https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration http_code=503 time_total=0.049700s remote_ip=132.226.175.206
