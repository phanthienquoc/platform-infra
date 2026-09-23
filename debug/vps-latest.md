# VPS inspection

Generated: 2026-09-23T00:58:53+00:00

## Host
uname: Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       3.5Gi       5.6Gi        54Mi        14Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   20G   26G  43% /
 00:58:53 up 144 days, 10:49,  0 users,  load average: 0.13, 0.15, 0.17

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
github-+ 1309509  0.0  0.5    09:59:37 /opt/actions-runner/bin/Runner.Listener run --startuptype service
github-+ 1765372 66.6  0.4       00:03 /opt/actions-runner/bin/Runner.Worker spawnclient 154 159
  actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service loaded    active   running GitHub Actions Runner (phanthienquoc-platform-infra.platform-k3s-01)
runner_service: active
runner_service_enabled: enabled

## Docker
Docker version 29.1.3, build f52814d
Server=29.1.3 RootDir=/var/lib/docker

## Updates
Listing...
apparmor/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
cloud-init/jammy-updates 26.1-0ubuntu1~22.04.1 all [upgradable from: 25.2-0ubuntu1~22.04.1]
containerd.io/jammy 2.3.5-1~ubuntu.22.04~jammy arm64 [upgradable from: 2.2.1-1~ubuntu.22.04~jammy]
docker-buildx-plugin/jammy 0.37.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 0.30.1-1~ubuntu.22.04~jammy]
docker-ce-cli/jammy 5:29.8.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce-rootless-extras/jammy 5:29.8.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce/jammy 5:29.8.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-compose-plugin/jammy 5.5.1-1~ubuntu.22.04~jammy arm64 [upgradable from: 5.0.1-1~ubuntu.22.04~jammy]
fwupd/jammy-updates 2.0.20-1ubuntu2~22.04.2 arm64 [upgradable from: 1.7.9-1~22.04.3]
iproute2/jammy-updates 5.15.0-1ubuntu2.2 arm64 [upgradable from: 5.15.0-1ubuntu2]
landscape-common/jammy-updates 23.02-0ubuntu1~22.04.7 arm64 [upgradable from: 23.02-0ubuntu1~22.04.6]
libapparmor1/jammy-updates 3.0.4-2ubuntu2.5 arm64 [upgradable from: 3.0.4-2ubuntu2.4]
libjcat1/jammy-updates 0.2.3-1~ubuntu0.22.04.1 arm64 [upgradable from: 0.1.9-1]
libk5crypto3/jammy-updates 1.19.2-2ubuntu0.10 arm64 [upgradable from: 1.19.2-2ubuntu0.8]
libldap-2.5-0/jammy-updates 2.5.20+dfsg-0ubuntu0.22.04.1 arm64 [upgradable from: 2.5.19+dfsg-0ubuntu0.22.04.1]
libldap-common/jammy-updates 2.5.20+dfsg-0ubuntu0.22.04.1 all [upgradable from: 2.5.19+dfsg-0ubuntu0.22.04.1]
libnetplan0/jammy-updates 0.107.1-3ubuntu0.22.04.5 arm64 [upgradable from: 0.106.1-7ubuntu0.22.04.4]
libnftables1/jammy-updates 1.0.2-1ubuntu3.1 arm64 [upgradable from: 1.0.2-1ubuntu3]
libxmlb2/jammy-updates 0.3.24-1~ubuntu0.22.04.1 arm64 [upgradable from: 0.3.6-2build1]
linux-headers-oracle/jammy-updates 6.8.0-1062.65~22.04.1 arm64 [upgradable from: 6.8.0-1061.64~22.04.1]
linux-image-oracle/jammy-updates 6.8.0-1062.65~22.04.1 arm64 [upgradable from: 6.8.0-1061.64~22.04.1]
linux-oracle/jammy-updates 6.8.0-1062.65~22.04.1 arm64 [upgradable from: 6.8.0-1061.64~22.04.1]
linux-tools-common/jammy-updates 5.15.0-194.204 all [upgradable from: 5.15.0-191.201]
lshw/jammy-updates 02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1 arm64 [upgradable from: 02.19.git.2021.06.19.996aaad9c7-2build1]
netplan.io/jammy-updates 0.107.1-3ubuntu0.22.04.5 arm64 [upgradable from: 0.106.1-7ubuntu0.22.04.4]
nftables/jammy-updates 1.0.2-1ubuntu3.1 arm64 [upgradable from: 1.0.2-1ubuntu3]
python3-attr/jammy-updates 21.2.0-1ubuntu1 all [upgradable from: 21.2.0-1]
python3-distupgrade/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
snapd/jammy-updates 2.76.3+ubuntu22.04 arm64 [upgradable from: 2.76+ubuntu22.04.1]
sosreport/jammy-updates 4.10.2-0ubuntu0~22.04.1 arm64 [upgradable from: 4.9.2-0ubuntu0~22.04.1]
ubuntu-minimal/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-release-upgrader-core/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
ubuntu-server/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-standard/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]

restart_required: yes

## K3s
Client Version: v1.36.3+k3s1
Kustomize Version: v5.8.1
NAME         STATUS   ROLES           AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION              CONTAINER-RUNTIME
tce-k3s-01   Ready    control-plane   31d   v1.36.3+k3s1   10.0.0.120    <none>        Ubuntu 22.04.5 LTS   6.8.0-1049-oracle (arm64)   containerd://2.3.2-k3s2
NAME              STATUS   AGE
cert-manager      Active   28d
default           Active   31d
kube-node-lease   Active   31d
kube-public       Active   31d
kube-system       Active   31d
stock-prod        Active   3d18h
tce-prod          Active   31d
NAMESPACE      NAME                                      READY   STATUS      RESTARTS      AGE     IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager   cert-manager-75b96c9588-lgn7d             1/1     Running     0             28d     10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager   cert-manager-cainjector-b644b66f7-l8jdq   1/1     Running     1 (28d ago)   28d     10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager   cert-manager-webhook-76d97df888-wwq49     1/1     Running     0             28d     10.42.0.99    tce-k3s-01   <none>           <none>
kube-system    coredns-54996dc9b4-d68pf                  1/1     Running     0             31d     10.42.0.6     tce-k3s-01   <none>           <none>
kube-system    helm-install-traefik-crd-mq7w8            0/1     Completed   0             31d     10.42.0.3     tce-k3s-01   <none>           <none>
kube-system    helm-install-traefik-s2twj                0/1     Completed   1 (31d ago)   31d     10.42.0.2     tce-k3s-01   <none>           <none>
kube-system    local-path-provisioner-58d557dc48-jbhhp   1/1     Running     1 (31d ago)   31d     10.42.0.5     tce-k3s-01   <none>           <none>
kube-system    metrics-server-6dc596dfb8-s2bzm           1/1     Running     0             31d     10.42.0.4     tce-k3s-01   <none>           <none>
kube-system    svclb-traefik-859779c1-7bwx2              2/2     Running     0             31d     10.42.0.7     tce-k3s-01   <none>           <none>
kube-system    traefik-59b7647586-gml84                  1/1     Running     0             31d     10.42.0.8     tce-k3s-01   <none>           <none>
stock-prod     stock-backend-57ccb8ff6-d25jq             1/1     Running     0             3d18h   10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod     stock-frontend-79c57845df-z747s           1/1     Running     0             3d18h   10.42.0.56    tce-k3s-01   <none>           <none>
tce-prod       tce-frontend-64f468f759-zn7g5             1/1     Running     0             25h     10.42.0.65    tce-k3s-01   <none>           <none>
tce-prod       tce-service-749db66ff5-ks4m4              1/1     Running     0             25h     10.42.0.64    tce-k3s-01   <none>           <none>
NAMESPACE      NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager   cert-manager              1/1     1            1           28d
cert-manager   cert-manager-cainjector   1/1     1            1           28d
cert-manager   cert-manager-webhook      1/1     1            1           28d
kube-system    coredns                   1/1     1            1           31d
kube-system    local-path-provisioner    1/1     1            1           31d
kube-system    metrics-server            1/1     1            1           31d
kube-system    traefik                   1/1     1            1           31d
stock-prod     stock-backend             1/1     1            1           3d18h
stock-prod     stock-frontend            1/1     1            1           3d18h
tce-prod       tce-frontend              1/1     1            1           28d
tce-prod       tce-service               1/1     1            1           28d

### GitOps drift
status: drift-detected

### Images
cert-manager   cert-manager              quay.io/jetstack/cert-manager-controller:v1.21.1
cert-manager   cert-manager-cainjector   quay.io/jetstack/cert-manager-cainjector:v1.21.1
cert-manager   cert-manager-webhook      quay.io/jetstack/cert-manager-webhook:v1.21.1
kube-system    coredns                   rancher/mirrored-coredns-coredns:1.14.6
kube-system    local-path-provisioner    rancher/local-path-provisioner:v0.0.36
kube-system    metrics-server            rancher/mirrored-metrics-server:v0.9.0
kube-system    traefik                   rancher/mirrored-library-traefik:3.7.8
stock-prod     stock-backend             ghcr.io/phanthienquoc/stockdividend/backend:23b2878
stock-prod     stock-frontend            ghcr.io/phanthienquoc/stockdividend/user:23b2878
tce-prod       tce-frontend              docker.io/library/tce-frontend:prod-v0.1.0-147cc73
tce-prod       tce-service               docker.io/library/tce-service:prod-v0.1.0-147cc73
NAMESPACE      NAME                      TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
cert-manager   cert-manager              ClusterIP      10.43.138.27    <none>        9402/TCP                     28d
cert-manager   cert-manager-cainjector   ClusterIP      10.43.135.132   <none>        9402/TCP                     28d
cert-manager   cert-manager-webhook      ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             28d
default        kubernetes                ClusterIP      10.43.0.1       <none>        443/TCP                      31d
kube-system    kube-dns                  ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       31d
kube-system    metrics-server            ClusterIP      10.43.120.41    <none>        443/TCP                      31d
kube-system    traefik                   LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   31d
stock-prod     backend                   ClusterIP      10.43.46.139    <none>        8080/TCP                     3d18h
stock-prod     stock-backend             ClusterIP      10.43.247.219   <none>        8080/TCP                     3d18h
stock-prod     stock-frontend            ClusterIP      10.43.53.102    <none>        3000/TCP                     3d18h
tce-prod       tce-frontend              ClusterIP      10.43.99.130    <none>        80/TCP                       28d
tce-prod       tce-service               ClusterIP      10.43.189.227   <none>        8210/TCP                     28d
NAMESPACE    NAME            CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
stock-prod   stock-ingress   traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   3d18h
tce-prod     tce             traefik   tce.mrcute.space                                               10.0.0.120   80, 443   28d

### Ingress hosts
stock-prod   stock-ingress   mrcute.space,www.mrcute.space,admin.mrcute.space,api.mrcute.space
tce-prod     tce             tce.mrcute.space

## K3s service
active
enabled
