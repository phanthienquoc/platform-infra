# VPS inspection

Generated: 2026-10-10T20:05:42+00:00

## Host
uname: Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       3.7Gi       517Mi        89Mi        19Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   38G  7.7G  84% /
disk_pressure: warning (84%)
 20:05:42 up 162 days,  5:56,  0 users,  load average: 0.00, 0.09, 0.13

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
571291 /opt/actions-runner/bin/Runner.Worker spawnclient 154 159
1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
1340196 /opt/media-actions-runner/bin/Runner.Listener run --startuptype service
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
containerd.io/jammy 2.4.1-2~ubuntu.22.04~jammy arm64 [upgradable from: 2.2.1-1~ubuntu.22.04~jammy]
docker-buildx-plugin/jammy 0.38.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 0.30.1-1~ubuntu.22.04~jammy]
docker-ce-cli/jammy 5:29.9.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce-rootless-extras/jammy 5:29.9.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-ce/jammy 5:29.9.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 5:29.1.3-1~ubuntu.22.04~jammy]
docker-compose-plugin/jammy 5.6.0-1~ubuntu.22.04~jammy arm64 [upgradable from: 5.0.1-1~ubuntu.22.04~jammy]
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
libxmlb2/jammy-updates 0.3.24-1~ubuntu0.22.04.1 arm64 [upgradable from: 0.3.6-2build1]
lshw/jammy-updates 02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1 arm64 [upgradable from: 02.19.git.2021.06.19.996aaad9c7-2build1]
netplan.io/jammy-updates 0.107.1-3ubuntu0.22.04.5 arm64 [upgradable from: 0.106.1-7ubuntu0.22.04.4]
nftables/jammy-updates 1.0.2-1ubuntu3.1 arm64 [upgradable from: 1.0.2-1ubuntu3]
python3-attr/jammy-updates 21.2.0-1ubuntu1 all [upgradable from: 21.2.0-1]
python3-distupgrade/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
sosreport/jammy-updates 4.11.2-0ubuntu0~22.04.1 arm64 [upgradable from: 4.9.2-0ubuntu0~22.04.1]
ubuntu-minimal/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-release-upgrader-core/jammy-updates 1:22.04.21 all [upgradable from: 1:22.04.20]
ubuntu-server/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]
ubuntu-standard/jammy-updates 1.481.5 arm64 [upgradable from: 1.481.4]

restart_required: yes

## K3s
Client Version: v1.36.3+k3s1
Kustomize Version: v5.8.1
NAME         STATUS   ROLES           AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION              CONTAINER-RUNTIME
tce-k3s-01   Ready    control-plane   49d   v1.36.3+k3s1   10.0.0.120    <none>        Ubuntu 22.04.5 LTS   6.8.0-1049-oracle (arm64)   containerd://2.3.2-k3s2
NAME               STATUS   AGE
cert-manager       Active   46d
default            Active   49d
k3s-debug          Active   2d15h
kube-node-lease    Active   49d
kube-public        Active   49d
kube-system        Active   49d
media-prod         Active   10d
microfe-platform   Active   4d17h
stock-prod         Active   21d
tce-prod           Active   49d
NAMESPACE          NAME                                         READY   STATUS             RESTARTS       AGE     IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager       cert-manager-75b96c9588-lgn7d                1/1     Running            0              46d     10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager       cert-manager-cainjector-b644b66f7-l8jdq      1/1     Running            1 (46d ago)    46d     10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager       cert-manager-webhook-76d97df888-wwq49        1/1     Running            0              46d     10.42.0.99    tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861025-2xs6z            0/1     StartError         0              15m     10.42.0.193   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861025-7852s            0/1     StartError         0              20m     10.42.0.189   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861025-gtpkw            0/1     StartError         0              19m     10.42.0.191   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861025-hf698            0/1     StartError         0              20m     10.42.0.188   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861025-knnp6            0/1     StartError         0              18m     10.42.0.192   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861025-p6796            0/1     StartError         0              20m     10.42.0.190   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861040-4d5md            0/1     StartError         0              5m11s   10.42.0.196   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861040-574cr            0/1     StartError         0              4m30s   10.42.0.197   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861040-ckjzc            0/1     StartError         0              3m9s    10.42.0.198   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861040-klnrt            0/1     StartError         0              29s     10.42.0.199   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861040-ktsgp            0/1     StartError         0              5m32s   10.42.0.195   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29861040-zqs29            0/1     StartError         0              5m43s   10.42.0.194   tce-k3s-01   <none>           <none>
kube-system        coredns-54996dc9b4-d68pf                     1/1     Running            0              49d     10.42.0.6     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-crd-mq7w8               0/1     Completed          0              49d     10.42.0.3     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-s2twj                   0/1     Completed          1 (49d ago)    49d     10.42.0.2     tce-k3s-01   <none>           <none>
kube-system        local-path-provisioner-58d557dc48-jbhhp      1/1     Running            1 (49d ago)    49d     10.42.0.5     tce-k3s-01   <none>           <none>
kube-system        metrics-server-6dc596dfb8-s2bzm              1/1     Running            0              49d     10.42.0.4     tce-k3s-01   <none>           <none>
kube-system        svclb-traefik-859779c1-7bwx2                 2/2     Running            0              49d     10.42.0.7     tce-k3s-01   <none>           <none>
kube-system        traefik-59b7647586-gml84                     1/1     Running            0              49d     10.42.0.8     tce-k3s-01   <none>           <none>
media-prod         media-generation-6f66c4dc4d-zdh7p            1/1     Running            0              4d17h   10.42.0.135   tce-k3s-01   <none>           <none>
media-prod         media-generation-frontend-667fb49d95-twxtq   1/1     Running            0              4d17h   10.42.0.136   tce-k3s-01   <none>           <none>
microfe-platform   microfe-auth-7fb9b95748-s86j9                0/1     ImagePullBackOff   0              98m     10.42.0.150   tce-k3s-01   <none>           <none>
microfe-platform   microfe-auth-bdc95699c-ftbhz                 0/1     ImagePullBackOff   0              6h6m    10.42.0.26    tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-74cb56864c-4phxl               0/1     ImagePullBackOff   0              98m     10.42.0.152   tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-dbbbfdf8c-5rkwz                1/1     Running            0              38h     10.42.0.158   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-5587c8844c-rbtgx                  1/1     Running            10 (38h ago)   38h     10.42.0.157   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-8599698dc8-ldjj4                  0/1     ImagePullBackOff   0              98m     10.42.0.151   tce-k3s-01   <none>           <none>
microfe-platform   nats-7bc8d9f768-q682m                        1/1     Running            0              38h     10.42.0.178   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-69878f6d56-ghgmx                 0/1     ImagePullBackOff   0              6h6m    10.42.0.28    tce-k3s-01   <none>           <none>
stock-prod         stock-admin-847cfb84ff-nv977                 0/1     ImagePullBackOff   0              98m     10.42.0.153   tce-k3s-01   <none>           <none>
stock-prod         stock-backend-57ccb8ff6-d25jq                1/1     Running            0              21d     10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-79dd6ddcbf-dqmgs               0/1     ImagePullBackOff   0              98m     10.42.0.154   tce-k3s-01   <none>           <none>
stock-prod         stock-frontend-79c57845df-z747s              1/1     Running            0              21d     10.42.0.56    tce-k3s-01   <none>           <none>
tce-prod           tce-frontend-f5ff9d7f5-hvpht                 1/1     Running            0              39h     10.42.0.144   tce-k3s-01   <none>           <none>
tce-prod           tce-service-54f7fd6476-lgfvj                 1/1     Running            0              39h     10.42.0.145   tce-k3s-01   <none>           <none>
NAMESPACE          NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager       cert-manager                1/1     1            1           46d
cert-manager       cert-manager-cainjector     1/1     1            1           46d
cert-manager       cert-manager-webhook        1/1     1            1           46d
kube-system        coredns                     1/1     1            1           49d
kube-system        local-path-provisioner      1/1     1            1           49d
kube-system        metrics-server              1/1     1            1           49d
kube-system        traefik                     1/1     1            1           49d
media-prod         media-generation            1/1     1            1           10d
media-prod         media-generation-frontend   1/1     1            1           10d
microfe-platform   microfe-auth                0/1     1            0           4d17h
microfe-platform   microfe-shell               1/1     1            1           4d17h
microfe-platform   microfe-ws                  1/1     1            1           4d17h
microfe-platform   nats                        1/1     1            1           38h
stock-prod         stock-admin                 0/1     1            0           17d
stock-prod         stock-backend               1/1     1            1           21d
stock-prod         stock-frontend              1/1     1            1           21d
tce-prod           tce-frontend                1/1     1            1           46d
tce-prod           tce-service                 1/1     1            1           46d

### Pod failure evidence
microfe-platform	microfe-auth-7fb9b95748-s86j9	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-auth:0.1.0": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-auth:0.1.0": failed to resolve reference "ghcr.io/phanthienquoc/microfe-auth:0.1.0": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-auth%3Apull&service=ghcr.io: 403 Forbidden
microfe-platform	microfe-auth-bdc95699c-ftbhz	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-auth:0.1.0": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-auth:0.1.0": failed to resolve reference "ghcr.io/phanthienquoc/microfe-auth:0.1.0": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-auth%3Apull&service=ghcr.io: 403 Forbidden
microfe-platform	microfe-shell-74cb56864c-4phxl	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-shell:0.1.0": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-shell:0.1.0": failed to resolve reference "ghcr.io/phanthienquoc/microfe-shell:0.1.0": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-shell%3Apull&service=ghcr.io: 403 Forbidden
microfe-platform	microfe-ws-8599698dc8-ldjj4	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": failed to resolve reference "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-ws%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-admin-69878f6d56-ghgmx	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fadmin%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-admin-847cfb84ff-nv977	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fadmin%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-backend-79dd6ddcbf-dqmgs	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fbackend%3Apull&service=ghcr.io: 403 Forbidden

### Recent failure events

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
media-prod         media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-362cb81
media-prod         media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-362cb81
microfe-platform   microfe-auth                ghcr.io/phanthienquoc/microfe-auth:0.1.0
microfe-platform   microfe-shell               ghcr.io/phanthienquoc/microfe-shell:0.1.0
microfe-platform   microfe-ws                  ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA
microfe-platform   nats                        nats:2.12-alpine
stock-prod         stock-admin                 ghcr.io/phanthienquoc/stockdividend/admin:12d63b4
stock-prod         stock-backend               ghcr.io/phanthienquoc/stockdividend/backend:12d63b4
stock-prod         stock-frontend              ghcr.io/phanthienquoc/stockdividend/user:23b2878
tce-prod           tce-frontend                ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-7cdf711
tce-prod           tce-service                 ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-7cdf711
NAMESPACE          NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
cert-manager       cert-manager                ClusterIP      10.43.138.27    <none>        9402/TCP                     46d
cert-manager       cert-manager-cainjector     ClusterIP      10.43.135.132   <none>        9402/TCP                     46d
cert-manager       cert-manager-webhook        ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             46d
default            kubernetes                  ClusterIP      10.43.0.1       <none>        443/TCP                      49d
kube-system        kube-dns                    ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       49d
kube-system        metrics-server              ClusterIP      10.43.120.41    <none>        443/TCP                      49d
kube-system        traefik                     LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   49d
media-prod         media-generation            ClusterIP      10.43.252.95    <none>        3000/TCP                     10d
media-prod         media-generation-frontend   ClusterIP      10.43.48.52     <none>        80/TCP                       10d
microfe-platform   microfe-auth                ClusterIP      10.43.83.168    <none>        80/TCP                       4d17h
microfe-platform   microfe-shell               ClusterIP      10.43.6.23      <none>        80/TCP                       4d17h
microfe-platform   microfe-ws                  ClusterIP      10.43.86.34     <none>        8080/TCP                     4d17h
microfe-platform   nats                        ClusterIP      10.43.147.69    <none>        4222/TCP,8222/TCP            38h
stock-prod         backend                     ClusterIP      10.43.46.139    <none>        8080/TCP                     21d
stock-prod         stock-admin                 ClusterIP      10.43.97.150    <none>        3000/TCP                     17d
stock-prod         stock-backend               ClusterIP      10.43.247.219   <none>        8080/TCP                     21d
stock-prod         stock-frontend              ClusterIP      10.43.53.102    <none>        3000/TCP                     21d
tce-prod           tce-frontend                ClusterIP      10.43.99.130    <none>        80/TCP                       46d
tce-prod           tce-service                 ClusterIP      10.43.189.227   <none>        8210/TCP                     46d
NAMESPACE          NAME             CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
media-prod         media            traefik   media.mrcute.space                                             10.0.0.120   80, 443   10d
microfe-platform   microfe-public   traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space             10.0.0.120   80, 443   4d16h
stock-prod         stock            traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   17d
stock-prod         stock-ingress    traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   21d
tce-prod           tce              traefik   tce.mrcute.space                                               10.0.0.120   80, 443   46d

### Ingress hosts
media-prod         media            media.mrcute.space
microfe-platform   microfe-public   app.mrcute.space,auth.mrcute.space,ws.mrcute.space
stock-prod         stock            mrcute.space,www.mrcute.space,admin.mrcute.space,api.mrcute.space
stock-prod         stock-ingress    mrcute.space,www.mrcute.space,admin.mrcute.space,api.mrcute.space
tce-prod           tce              tce.mrcute.space

## K3s service
active
enabled
