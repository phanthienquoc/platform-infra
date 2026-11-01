# VPS inspection

Generated: 2026-11-01T04:05:41+00:00

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
/dev/sda1        45G   25G   21G  54% /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   25G   21G  54% /
disk_pressure: normal (54%)
 04:05:41 up 183 days, 13:56,  0 users,  load average: 0.20, 0.23, 0.19

### Top disk consumers

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
21684 /opt/media-actions-runner/bin/Runner.Listener run --startuptype service
1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
2844935 /opt/actions-runner/bin/Runner.Worker spawnclient 155 160
  actions.runner.phanthienquoc-media-generation.media-generation-k3s-01.service loaded    active   running GitHub Actions Runner (phanthienquoc-media-generation.media-generation-k3s-01)
  actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service           loaded    active   running GitHub Actions Runner (phanthienquoc-platform-infra.platform-k3s-01)
runner_service: active
runner_service_enabled: enabled

## Docker
Docker version 29.1.3, build f52814d
Server=29.1.3 RootDir=/var/lib/docker

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
cert-manager       Active   67d
default            Active   71d
k3s-debug          Active   23d
kube-node-lease    Active   71d
kube-public        Active   71d
kube-system        Active   71d
media-prod         Active   31d
microfe-platform   Active   26d
stock-prod         Active   42d
tce-prod           Active   71d
NAMESPACE          NAME                                         READY   STATUS             RESTARTS      AGE    IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager       cert-manager-75b96c9588-lgn7d                1/1     Running            0             67d    10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager       cert-manager-cainjector-b644b66f7-l8jdq      1/1     Running            1 (67d ago)   67d    10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager       cert-manager-webhook-76d97df888-wwq49        1/1     Running            0             67d    10.42.0.99    tce-k3s-01   <none>           <none>
kube-system        coredns-54996dc9b4-d68pf                     1/1     Running            0             71d    10.42.0.6     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-crd-mq7w8               0/1     Completed          0             71d    10.42.0.3     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-s2twj                   0/1     Completed          1 (71d ago)   71d    10.42.0.2     tce-k3s-01   <none>           <none>
kube-system        local-path-provisioner-58d557dc48-jbhhp      1/1     Running            1 (71d ago)   71d    10.42.0.5     tce-k3s-01   <none>           <none>
kube-system        metrics-server-6dc596dfb8-s2bzm              1/1     Running            0             71d    10.42.0.4     tce-k3s-01   <none>           <none>
kube-system        svclb-traefik-859779c1-7bwx2                 2/2     Running            0             71d    10.42.0.7     tce-k3s-01   <none>           <none>
kube-system        traefik-59b7647586-gml84                     1/1     Running            0             71d    10.42.0.8     tce-k3s-01   <none>           <none>
media-prod         media-generation-6c68f86bf4-pl927            1/1     Running            0             33h    10.42.0.80    tce-k3s-01   <none>           <none>
media-prod         media-generation-frontend-5445d66b98-64pzz   1/1     Running            0             33h    10.42.0.79    tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-7b44b44dfb-ln4sw               1/1     Running            0             118m   10.42.0.153   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-5bc979dd77-txd28                  1/1     Running            0             118m   10.42.0.152   tce-k3s-01   <none>           <none>
microfe-platform   nats-7bc8d9f768-q682m                        1/1     Running            0             22d    10.42.0.178   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-576c4d59d6-djclc                 0/1     ImagePullBackOff   0             118m   10.42.0.151   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-85cc86b749-lvwcd                 0/1     ImagePullBackOff   0             163m   10.42.0.146   tce-k3s-01   <none>           <none>
stock-prod         stock-backend-57ccb8ff6-d25jq                1/1     Running            0             42d    10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-f59d758d4-4qnkk                0/1     ImagePullBackOff   0             118m   10.42.0.150   tce-k3s-01   <none>           <none>
stock-prod         stock-frontend-79c57845df-z747s              1/1     Running            0             42d    10.42.0.56    tce-k3s-01   <none>           <none>

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
media-prod	media-generation-6c68f86bf4-pl927	container	media-generation	ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8	ghcr.io/phanthienquoc/media-generation/backend@sha256:93ddb9448250082d6300d8fdf65074d8ab3a3234b0e8371f716b54a98a4f179d	true	0
media-prod	media-generation-frontend-5445d66b98-64pzz	container	media-generation-frontend	ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8	ghcr.io/phanthienquoc/media-generation/frontend@sha256:095c72ed8f53f19ee4213435d2ffe93c6a49964e92dc93c8e684ef22b4edcd9a	true	0
microfe-platform	microfe-shell-7b44b44dfb-ln4sw	container	shell	sha256:d6d34a138c9fb485abe5e70cf0b084e2d8cf482474be71ba0397819b2697f059	ghcr.io/phanthienquoc/microfe-shell@sha256:ae64acc032ce13d046ab78c9628b5b0b308f812b67ddfab7503d91e5a3ed8dcd	true	0
microfe-platform	microfe-ws-5bc979dd77-txd28	container	ws	sha256:a26e88e61c4420c79b2f23d6ca68b0b67880a3423cb773c48094ac77fc72aa99	ghcr.io/phanthienquoc/microfe-ws@sha256:416bc16ade0becf398b0554571f6813985c55dffaf742042a7edef10ca2ea16d	true	0
microfe-platform	nats-7bc8d9f768-q682m	container	nats	docker.io/library/nats:2.12-alpine	docker.io/library/nats@sha256:b270f5e2428354c0335612694d7dd2fb588148e567a5757fdff325ef9c9332e6	true	0
stock-prod	stock-admin-576c4d59d6-djclc	container	admin	ghcr.io/phanthienquoc/stockdividend/admin:12d63b4		false	0
stock-prod	stock-admin-85cc86b749-lvwcd	container	admin	ghcr.io/phanthienquoc/stockdividend/admin:12d63b4		false	0
stock-prod	stock-backend-57ccb8ff6-d25jq	container	backend	ghcr.io/phanthienquoc/stockdividend/backend:23b2878	sha256:bcf5f7b1b660b5b93cd9d9f4f041db7e9166c89b084412fa4f66e8e4d9a43ad1	true	0
stock-prod	stock-backend-f59d758d4-4qnkk	container	backend	ghcr.io/phanthienquoc/stockdividend/backend:12d63b4		false	0
stock-prod	stock-frontend-79c57845df-z747s	container	frontend	ghcr.io/phanthienquoc/stockdividend/user:23b2878	sha256:bca44dd31869a4874a795c6e6ace51f9362731770f3ac9ca1ee8f3e608d6bf99	true	0
NAMESPACE          NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager       cert-manager                1/1     1            1           67d
cert-manager       cert-manager-cainjector     1/1     1            1           67d
cert-manager       cert-manager-webhook        1/1     1            1           67d
kube-system        coredns                     1/1     1            1           71d
kube-system        local-path-provisioner      1/1     1            1           71d
kube-system        metrics-server              1/1     1            1           71d
kube-system        traefik                     1/1     1            1           71d
media-prod         media-generation            1/1     1            1           31d
media-prod         media-generation-frontend   1/1     1            1           31d
microfe-platform   keycloak                    0/0     0            0           15d
microfe-platform   microfe-auth                0/0     0            0           26d
microfe-platform   microfe-shell               1/1     1            1           26d
microfe-platform   microfe-ws                  1/1     1            1           26d
microfe-platform   nats                        1/1     1            1           22d
stock-prod         stock-admin                 0/1     1            0           38d
stock-prod         stock-backend               1/1     1            1           42d
stock-prod         stock-frontend              1/1     0            1           42d
tce-prod           tce-frontend                0/0     0            0           67d
tce-prod           tce-service                 0/0     0            0           67d

### Pod failure evidence
stock-prod	stock-admin-576c4d59d6-djclc	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": no match for platform in manifest: not found
stock-prod	stock-admin-85cc86b749-lvwcd	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": no match for platform in manifest: not found
stock-prod	stock-backend-f59d758d4-4qnkk	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": ErrImagePull: rpc error: code = NotFound desc = failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": no match for platform in manifest: not found

### Recent failure events

### TCE service diagnostics (last 2h; redacted)

### CRI image inventory
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: a password is required
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
sudo: a password is required

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
media-prod         media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8
media-prod         media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8
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
cert-manager       cert-manager                ClusterIP      10.43.138.27    <none>        9402/TCP                     67d
cert-manager       cert-manager-cainjector     ClusterIP      10.43.135.132   <none>        9402/TCP                     67d
cert-manager       cert-manager-webhook        ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             67d
default            kubernetes                  ClusterIP      10.43.0.1       <none>        443/TCP                      71d
kube-system        kube-dns                    ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       71d
kube-system        metrics-server              ClusterIP      10.43.120.41    <none>        443/TCP                      71d
kube-system        traefik                     LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   71d
media-prod         media-generation            ClusterIP      10.43.252.95    <none>        3000/TCP                     31d
media-prod         media-generation-frontend   ClusterIP      10.43.48.52     <none>        80/TCP                       31d
microfe-platform   keycloak                    ClusterIP      10.43.142.95    <none>        80/TCP,9000/TCP              15d
microfe-platform   microfe-auth                ClusterIP      10.43.83.168    <none>        80/TCP                       26d
microfe-platform   microfe-shell               ClusterIP      10.43.6.23      <none>        80/TCP                       26d
microfe-platform   microfe-ws                  ClusterIP      10.43.86.34     <none>        8080/TCP                     26d
microfe-platform   nats                        ClusterIP      10.43.147.69    <none>        4222/TCP,8222/TCP            22d
stock-prod         backend                     ClusterIP      10.43.46.139    <none>        8080/TCP                     42d
stock-prod         stock-admin                 ClusterIP      10.43.97.150    <none>        3000/TCP                     38d
stock-prod         stock-backend               ClusterIP      10.43.247.219   <none>        8080/TCP                     42d
stock-prod         stock-frontend              ClusterIP      10.43.53.102    <none>        3000/TCP                     42d
tce-prod           tce-frontend                ClusterIP      10.43.99.130    <none>        80/TCP                       67d
tce-prod           tce-service                 ClusterIP      10.43.189.227   <none>        8210/TCP                     67d
NAMESPACE          NAME                               CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
media-prod         media                              traefik   media.mrcute.space                                             10.0.0.120   80, 443   31d
microfe-platform   keycloak-public                    traefik   sso.mrcute.space                                               10.0.0.120   80, 443   15d
microfe-platform   keycloak-registration-rate-limit   traefik   sso.mrcute.space                                               10.0.0.120   80, 443   4d
microfe-platform   microfe-public                     traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space             10.0.0.120   80, 443   26d
stock-prod         stock                              traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   38d
stock-prod         stock-ingress                      traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   42d
tce-prod           tce                                traefik   tce.mrcute.space                                               10.0.0.120   80, 443   67d

## K3s service
active
enabled

### K3s recent warnings (last 2h)

## Keycloak diagnostics
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
keycloak   0/0     0            0           15d   keycloak     quay.io/keycloak/keycloak:26.8.1   app.kubernetes.io/name=keycloak
error: timed out waiting for the condition

### Public OIDC probes (status and latency only)
https://sso.mrcute.space/realms/master/.well-known/openid-configuration http_code=503 time_total=0.050194s remote_ip=132.226.175.206
https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration http_code=503 time_total=0.051564s remote_ip=132.226.175.206
