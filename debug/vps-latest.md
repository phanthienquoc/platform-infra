# VPS inspection

Generated: 2026-11-27T05:11:56+00:00

## Host
Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       3.4Gi       1.7Gi        85Mi        18Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   27G   19G  59% /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   27G   19G  59% /
disk_pressure: normal (59%)
 05:11:56 up 209 days, 15:02,  1 user,  load average: 0.63, 0.25, 0.19

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
64K	/var/log/containers
72K	/var/log/unified-monitoring-agent
200K	/var/log/apt
23M	/var/log/oracle-cloud-agent
236M	/var/lib/rancher/k3s
236M	/var/lib/rancher/k3s/data
2.3G	/var/log/journal
2.6G	/var/log
1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
3055762 /opt/actions-runner/bin/Runner.Worker spawnclient 154 161
● actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service - GitHub Actions Runner (phanthienquoc-platform-infra.platform-k3s-01)
     Loaded: loaded (/etc/systemd/system/actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2026-09-22 14:59:15 UTC; 2 months 4 days ago
   Main PID: 1309484 (runsvc.sh)
      Tasks: 46 (limit: 28686)
     Memory: 1.4G
        CPU: 15h 39min 53.702s
     CGroup: /system.slice/actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service
             ├─1309484 /bin/bash /opt/actions-runner/runsvc.sh
             ├─1309492 ./externals/node20/bin/node ./bin/RunnerService.js
             ├─1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
             ├─3055762 /opt/actions-runner/bin/Runner.Worker spawnclient 154 161
runner_service: active
runner_service_enabled: enabled
runner_policy: platform-kubectl policy: rollout-status-v15-core-workloads

## Docker
Docker version 29.1.3, build f52814d
Server=29.1.3 RootDir=/var/lib/docker
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          21        12        9.208GB   5.786GB (62%)
Containers      13        12        2.056MB   4.096kB (0%)
Local Volumes   5         3         66.2MB    66.18MB (99%)
Build Cache     31        0         519.4MB   154.4MB

## Updates
Listing...
apparmor/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
binutils-aarch64-linux-gnu/jammy-updates,jammy-security 2.38-4ubuntu2.14 arm64 [upgradable from: 2.38-4ubuntu2.12]
binutils-common/jammy-updates,jammy-security 2.38-4ubuntu2.14 arm64 [upgradable from: 2.38-4ubuntu2.12]
binutils/jammy-updates,jammy-security 2.38-4ubuntu2.14 arm64 [upgradable from: 2.38-4ubuntu2.12]
cloud-init/jammy-updates 26.1-0ubuntu1~22.04.1 all [upgradable from: 25.2-0ubuntu1~22.04.1]
containerd.io/jammy 2.4.2-4~ubuntu.22.04~jammy arm64 [upgradable from: 2.2.1-1~ubuntu.22.04~jammy]
distro-info/jammy-updates 1.1ubuntu0.3 arm64 [upgradable from: 1.1ubuntu0.2]
docker-buildx-plugin/jammy 0.39.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 0.30.1-1~ubuntu.22.04~jammy]
docker-ce-cli/jammy 5:29.10.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce-rootless-extras/jammy 5:29.10.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce/jammy 5:29.10.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-compose-plugin/jammy 5.8.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 5.0.1-1~ubuntu.22.04~jammy]
fwupd/jammy-updates 2.0.20-1ubuntu2~22.04.2 arm64 [upgradable from: 1.7.9-1~22.04.3]
iproute2/jammy-updates 5.15.0-1ubuntu2.2 arm64 [upgradable from: 5.15.0-1ubuntu2]
landscape-common/jammy-updates 23.02-0ubuntu1~22.04.7 arm64 [upgradable from: 23.02-0ubuntu1~22.04.6]
libapparmor1/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
libaudit-common/jammy-updates 1:3.0.7-1ubuntu0.1 all [upgradable from: 1:3.0.7-1build1]
libaudit1/jammy-updates 1:3.0.7-1ubuntu0.1 arm64 [upgradable from: 1:3.0.7-1build1]
libbinutils/jammy-updates,jammy-security 2.38-4ubuntu2.14 arm64 [upgradable from: 2.38-4ubuntu2.12]
libctf-nobfd0/jammy-updates,jammy-security 2.38-4ubuntu2.14 arm64 [upgradable from: 2.38-4ubuntu2.12]
libctf0/jammy-updates,jammy-security 2.38-4ubuntu2.14 arm64 [upgradable from: 2.38-4ubuntu2.12]
libglib2.0-0/jammy-updates 2.72.4-0ubuntu2.11 arm64 [upgradable from: 2.72.4-0ubuntu2.10]
libglib2.0-bin/jammy-updates 2.72.4-0ubuntu2.11 arm64 [upgradable from: 2.72.4-0ubuntu2.10]
libglib2.0-data/jammy-updates 2.72.4-0ubuntu2.11 all [upgradable from: 2.72.4-0ubuntu2.10]
libjcat1/jammy-updates 0.2.3-1~ubuntu0.22.04.1 arm64 [upgradable from: 0.1.9-1]
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
python3-jwt/jammy-updates,jammy-security 2.3.0-1ubuntu0.8 all [upgradable from: 2.3.0-1ubuntu0.7]
snapd/jammy-updates 2.78+ubuntu22.04 arm64 [upgradable from: 2.76.3+ubuntu22.04.1]
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
tce-k3s-01   Ready    control-plane   97d   v1.36.3+k3s1   10.0.0.120    <none>        Ubuntu 22.04.5 LTS   6.8.0-1049-oracle (arm64)   containerd://2.3.2-k3s2
Active platform namespaces:
NAME               STATUS   AGE
cert-manager       Active   93d
default            Active   97d
k3s-debug          Active   50d
kube-node-lease    Active   97d
kube-public        Active   97d
kube-system        Active   97d
microfe-platform   Active   52d
tce-prod           Active   97d
Pods in active platform namespaces:
-- namespace default --
-- namespace kube-node-lease --
-- namespace kube-public --
-- namespace kube-system --
NAME                                      READY   STATUS      RESTARTS      AGE   IP          NODE         NOMINATED NODE   READINESS GATES
coredns-54996dc9b4-d68pf                  1/1     Running     0             97d   10.42.0.6   tce-k3s-01   <none>           <none>
helm-install-traefik-crd-mq7w8            0/1     Completed   0             97d   10.42.0.3   tce-k3s-01   <none>           <none>
helm-install-traefik-s2twj                0/1     Completed   1 (97d ago)   97d   10.42.0.2   tce-k3s-01   <none>           <none>
local-path-provisioner-58d557dc48-jbhhp   1/1     Running     1 (97d ago)   97d   10.42.0.5   tce-k3s-01   <none>           <none>
metrics-server-6dc596dfb8-s2bzm           1/1     Running     0             97d   10.42.0.4   tce-k3s-01   <none>           <none>
svclb-traefik-859779c1-7bwx2              2/2     Running     0             97d   10.42.0.7   tce-k3s-01   <none>           <none>
traefik-59b7647586-gml84                  1/1     Running     0             97d   10.42.0.8   tce-k3s-01   <none>           <none>
-- namespace cert-manager --
NAME                                      READY   STATUS    RESTARTS      AGE   IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager-75b96c9588-lgn7d             1/1     Running   0             93d   10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager-cainjector-b644b66f7-l8jdq   1/1     Running   1 (93d ago)   93d   10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager-webhook-76d97df888-wwq49     1/1     Running   0             93d   10.42.0.99    tce-k3s-01   <none>           <none>
-- namespace microfe-platform --
NAME                             READY   STATUS    RESTARTS   AGE    IP            NODE         NOMINATED NODE   READINESS GATES
microfe-shell-7b44b44dfb-ln4sw   1/1     Running   0          26d    10.42.0.153   tce-k3s-01   <none>           <none>
microfe-ws-5bc979dd77-txd28      1/1     Running   0          26d    10.42.0.152   tce-k3s-01   <none>           <none>
mrcute-intro-6fd77b5495-tf6xj    1/1     Running   0          5h2m   10.42.0.213   tce-k3s-01   <none>           <none>
nats-7bc8d9f768-q682m            1/1     Running   0          48d    10.42.0.178   tce-k3s-01   <none>           <none>
-- namespace tce-prod --
-- namespace k3s-debug --

### Pod imageID evidence
kube-system	coredns-54996dc9b4-d68pf	container	coredns	docker.io/rancher/mirrored-coredns-coredns:1.14.6	docker.io/rancher/mirrored-coredns-coredns@sha256:900f9c109f7a33545d3c811516e8376df9019147b750f5ce3e254468769176ea	true	0
kube-system	helm-install-traefik-crd-mq7w8	container	helm	docker.io/rancher/klipper-helm:v0.13.3-build20260727	docker.io/rancher/klipper-helm@sha256:5425a2b4613d2458dbdff99218e8d487ebb59c20e7a941f061c0777070f0aac1	false	0
kube-system	helm-install-traefik-s2twj	container	helm	docker.io/rancher/klipper-helm:v0.13.3-build20260727	docker.io/rancher/klipper-helm@sha256:5425a2b4613d2458dbdff99218e8d487ebb59c20e7a941f061c0777070f0aac1	false	1
kube-system	local-path-provisioner-58d557dc48-jbhhp	container	local-path-provisioner	docker.io/rancher/local-path-provisioner:v0.0.36	docker.io/rancher/local-path-provisioner@sha256:1eba82e9c386038b4af6d69cca7519fac738c28c42735ed48ce70c882ad0d80f	true	1
kube-system	metrics-server-6dc596dfb8-s2bzm	container	metrics-server	docker.io/rancher/mirrored-metrics-server:v0.9.0	docker.io/rancher/mirrored-metrics-server@sha256:d9862115e7c7881280d3d75ca26bda8ffc0fc213315979575bf23ce9826205c0	true	0
kube-system	svclb-traefik-859779c1-7bwx2	container	lb-tcp-443	docker.io/rancher/klipper-lb:v0.4.17	docker.io/rancher/klipper-lb@sha256:910944bb0bd94f060a82a56ca1ea1c577d3e49b3473a093a47a985f32e92d94a	true	0
kube-system	svclb-traefik-859779c1-7bwx2	container	lb-tcp-80	docker.io/rancher/klipper-lb:v0.4.17	docker.io/rancher/klipper-lb@sha256:910944bb0bd94f060a82a56ca1ea1c577d3e49b3473a093a47a985f32e92d94a	true	0
kube-system	traefik-59b7647586-gml84	container	traefik	docker.io/rancher/mirrored-library-traefik:3.7.8	docker.io/rancher/mirrored-library-traefik@sha256:4299bbed850421258fc5448c2e0e6ad350981d4d335a68de11b92448aedbefe5	true	0
cert-manager	cert-manager-75b96c9588-lgn7d	container	cert-manager-controller	quay.io/jetstack/cert-manager-controller:v1.21.1	quay.io/jetstack/cert-manager-controller@sha256:416a2d76870d996460e62bd7f521bf14fa017be9e3e904aab92163a331fcb61a	true	0
cert-manager	cert-manager-cainjector-b644b66f7-l8jdq	container	cert-manager-cainjector	quay.io/jetstack/cert-manager-cainjector:v1.21.1	quay.io/jetstack/cert-manager-cainjector@sha256:ccf6b919ec0500745a47a910118f834f9636d0aac1ff221245cd2557ed8c7c98	true	1
cert-manager	cert-manager-webhook-76d97df888-wwq49	container	cert-manager-webhook	quay.io/jetstack/cert-manager-webhook:v1.21.1	quay.io/jetstack/cert-manager-webhook@sha256:d8b3961b51c8c7320633f8208dc46bf88aa13804d0f7cbe48a096b2c523cee42	true	0
microfe-platform	microfe-shell-7b44b44dfb-ln4sw	container	shell	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd	true	0
microfe-platform	microfe-ws-5bc979dd77-txd28	container	ws	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d	true	0
microfe-platform	mrcute-intro-6fd77b5495-tf6xj	container	nginx	docker.io/nginxinc/nginx-unprivileged:1.27-alpine	docker.io/nginxinc/nginx-unprivileged@sha256:65e3e85dbaed8ba248841d9d58a899b6197106c23cb0ff1a132b7bfe0547e4c0	true	0
microfe-platform	nats-7bc8d9f768-q682m	container	nats	docker.io/library/nats:2.12-alpine	docker.io/library/nats@sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6	true	0

### Deployments
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
coredns                  1/1     1            1           97d
local-path-provisioner   1/1     1            1           97d
metrics-server           1/1     1            1           97d
traefik                  1/1     1            1           97d
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager              1/1     1            1           93d
cert-manager-cainjector   1/1     1            1           93d
cert-manager-webhook      1/1     1            1           93d
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
keycloak        0/0     0            0           41d
microfe-auth    0/0     0            0           52d
microfe-shell   1/1     1            1           52d
microfe-ws      1/1     1            1           52d
mrcute-intro    1/1     1            1           5h2m
nats            1/1     1            1           48d
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
tce-frontend   0/0     0            0           93d
tce-service    0/0     0            0           93d

### Persistent storage inventory
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE   VOLUMEMODE
k3s-debug-logs   Bound    pvc-9aed95ca-8365-46a4-a06a-d8f26d600456   1Gi        RWO            local-path     <unset>                 49d   Filesystem
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                      STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE   VOLUMEMODE
pvc-9aed95ca-8365-46a4-a06a-d8f26d600456   1Gi        RWO            Delete           Bound    k3s-debug/k3s-debug-logs   local-path     <unset>                          49d   Filesystem

### Pod failure evidence

### Recent failure events

### TCE service diagnostics (last 2h; redacted)

### CRI image inventory
Images used by active platform namespaces (repo tags, repo digests, image ID, pinned, size bytes):
	ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	false	25830437
	ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	false	65079739
quay.io/jetstack/cert-manager-cainjector:v1.21.1	quay.io/jetstack/cert-manager-cainjector@sha256:ccf6b919ec0500745a47a910118f834f9636d0aac1ff221245cd2557ed8c7c98	sha256:187d7de7d1d04dd40dbc62236b0e75eea4a0ae336b0de824c6e27e28fb102381	false	11030656
quay.io/jetstack/cert-manager-controller:v1.21.1	quay.io/jetstack/cert-manager-controller@sha256:416a2d76870d996460e62bd7f521bf14fa017be9e3e904aab92163a331fcb61a	sha256:5283ffc3ebd6cf46ecf84f5e56730734b3de8d3de456c3a909f0077b5337c55d	false	22296047
quay.io/jetstack/cert-manager-webhook:v1.21.1	quay.io/jetstack/cert-manager-webhook@sha256:d8b3961b51c8c7320633f8208dc46bf88aa13804d0f7cbe48a096b2c523cee42	sha256:4694bc08f6c866b0820ff7e82d673029b6d48ba0aaf79af528987ca114f426ec	false	17710712

### GHCR image digest coverage
status: all cached GHCR-tagged images have RepoDigest
Containers in active platform namespaces (container ID, name, image reference, state):

### GitOps drift
Prepared checksum-verified cert-manager v1.21.1 manifest.
status: clean

### Active platform workload images, services and ingress
-- namespace default --
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.43.0.1    <none>        443/TCP   97d
-- namespace kube-node-lease --
-- namespace kube-public --
-- namespace kube-system --
kube-system   coredns                  rancher/mirrored-coredns-coredns:1.14.6
kube-system   local-path-provisioner   rancher/local-path-provisioner:v0.0.36
kube-system   metrics-server           rancher/mirrored-metrics-server:v0.9.0
kube-system   traefik                  rancher/mirrored-library-traefik:3.7.8
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kube-dns         ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       97d
metrics-server   ClusterIP      10.43.120.41    <none>        443/TCP                      97d
traefik          LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   97d
-- namespace cert-manager --
cert-manager   cert-manager              quay.io/jetstack/cert-manager-controller:v1.21.1
cert-manager   cert-manager-cainjector   quay.io/jetstack/cert-manager-cainjector:v1.21.1
cert-manager   cert-manager-webhook      quay.io/jetstack/cert-manager-webhook:v1.21.1
NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)            AGE
cert-manager              ClusterIP   10.43.138.27    <none>        9402/TCP           93d
cert-manager-cainjector   ClusterIP   10.43.135.132   <none>        9402/TCP           93d
cert-manager-webhook      ClusterIP   10.43.52.112    <none>        443/TCP,9402/TCP   93d
-- namespace microfe-platform --
microfe-platform   keycloak        quay.io/keycloak/keycloak:26.8.1
microfe-platform   microfe-auth    ghcr.io/phanthienquoc/auth-service/auth:prod-v1.0.0-ceb2688
microfe-platform   microfe-shell   ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd
microfe-platform   microfe-ws      ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d
microfe-platform   mrcute-intro    nginxinc/nginx-unprivileged:1.27-alpine
microfe-platform   nats            nats:2.12-alpine
NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
keycloak        ClusterIP   10.43.142.95   <none>        80/TCP,9000/TCP     41d
microfe-auth    ClusterIP   10.43.83.168   <none>        80/TCP              52d
microfe-shell   ClusterIP   10.43.6.23     <none>        80/TCP              52d
microfe-ws      ClusterIP   10.43.86.34    <none>        8080/TCP            52d
mrcute-intro    ClusterIP   10.43.38.34    <none>        80/TCP              5h3m
nats            ClusterIP   10.43.147.69   <none>        4222/TCP,8222/TCP   48d
NAME                               CLASS     HOSTS                                                ADDRESS      PORTS     AGE
keycloak-public                    traefik   sso.mrcute.space                                     10.0.0.120   80, 443   41d
keycloak-registration-rate-limit   traefik   sso.mrcute.space                                     10.0.0.120   80, 443   30d
microfe-public                     traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space   10.0.0.120   80, 443   52d
mrcute-root                        traefik   mrcute.space                                         10.0.0.120   80, 443   5h3m
-- namespace tce-prod --
tce-prod   tce-frontend   ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-e75e338
tce-prod   tce-service    ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-e75e338
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
tce-frontend   ClusterIP   10.43.99.130    <none>        80/TCP     93d
tce-service    ClusterIP   10.43.189.227   <none>        8210/TCP   93d
NAME   CLASS     HOSTS              ADDRESS      PORTS     AGE
tce    traefik   tce.mrcute.space   10.0.0.120   80, 443   93d
-- namespace k3s-debug --

## K3s service
active
enabled

### K3s recent warnings (last 2h)

## Keycloak diagnostics
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
keycloak   0/0     0            0           41d   keycloak     quay.io/keycloak/keycloak:26.8.1   app.kubernetes.io/name=keycloak
Keycloak logs skipped: deployment is intentionally scaled to zero.

### Public OIDC probes (status and latency only)
https://sso.mrcute.space/realms/master/.well-known/openid-configuration http_code=503 time_total=0.108415s remote_ip=132.226.175.206
https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration http_code=503 time_total=0.052744s remote_ip=132.226.175.206
