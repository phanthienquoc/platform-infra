# VPS inspection

Generated: 2026-10-30T14:08:28+00:00

## Host
Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       4.6Gi       3.4Gi        86Mi        15Gi        18Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   25G   21G  55% /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   25G   21G  55% /
disk_pressure: normal (55%)
 14:08:28 up 181 days, 23:58,  5 users,  load average: 0.36, 0.94, 0.66

### Top disk consumers

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
21684 /opt/media-actions-runner/bin/Runner.Listener run --startuptype service
1061331 /opt/actions-runner/bin/Runner.Worker spawnclient 157 161
1309509 /opt/actions-runner/bin/Runner.Listener run --startuptype service
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
linux-tools-common/jammy-updates,jammy-security 5.15.0-202.212 all [upgradable from: 5.15.0-198.208]
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
tce-k3s-01   Ready    control-plane   69d   v1.36.3+k3s1   10.0.0.120    <none>        Ubuntu 22.04.5 LTS   6.8.0-1049-oracle (arm64)   containerd://2.3.2-k3s2
NAME               STATUS   AGE
cert-manager       Active   66d
default            Active   69d
k3s-debug          Active   22d
kube-node-lease    Active   69d
kube-public        Active   69d
kube-system        Active   69d
media-prod         Active   30d
microfe-platform   Active   24d
stock-prod         Active   41d
tce-prod           Active   69d
NAMESPACE          NAME                                         READY   STATUS             RESTARTS       AGE    IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager       cert-manager-75b96c9588-lgn7d                1/1     Running            0              66d    10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager       cert-manager-cainjector-b644b66f7-l8jdq      1/1     Running            1 (66d ago)    66d    10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager       cert-manager-webhook-76d97df888-wwq49        1/1     Running            0              66d    10.42.0.99    tce-k3s-01   <none>           <none>
kube-system        coredns-54996dc9b4-d68pf                     1/1     Running            0              69d    10.42.0.6     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-crd-mq7w8               0/1     Completed          0              69d    10.42.0.3     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-s2twj                   0/1     Completed          1 (69d ago)    69d    10.42.0.2     tce-k3s-01   <none>           <none>
kube-system        local-path-provisioner-58d557dc48-jbhhp      1/1     Running            1 (69d ago)    69d    10.42.0.5     tce-k3s-01   <none>           <none>
kube-system        metrics-server-6dc596dfb8-s2bzm              1/1     Running            0              69d    10.42.0.4     tce-k3s-01   <none>           <none>
kube-system        svclb-traefik-859779c1-7bwx2                 2/2     Running            0              69d    10.42.0.7     tce-k3s-01   <none>           <none>
kube-system        traefik-59b7647586-gml84                     1/1     Running            0              69d    10.42.0.8     tce-k3s-01   <none>           <none>
media-prod         media-generation-5c9b76dfb9-zh8jr            0/1     Running            0              16d    10.42.0.85    tce-k3s-01   <none>           <none>
media-prod         media-generation-646c797f66-6fwn4            0/1     Running            0              99m    10.42.0.38    tce-k3s-01   <none>           <none>
media-prod         media-generation-frontend-597b779c9d-dvrft   1/1     Running            0              16d    10.42.0.84    tce-k3s-01   <none>           <none>
microfe-platform   keycloak-68c4bc764c-4pp66                    0/1     Running            0              14d    10.42.0.124   tce-k3s-01   <none>           <none>
microfe-platform   microfe-auth-5c8cc75f5c-nbn7g                0/1     Running            0              100m   10.42.0.33    tce-k3s-01   <none>           <none>
microfe-platform   microfe-auth-7b67cd8569-gs6qs                0/1     Running            0              46m    10.42.0.66    tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-654b79579f-hqpbr               0/1     ImagePullBackOff   0              46m    10.42.0.68    tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-dbbbfdf8c-5rkwz                1/1     Running            0              21d    10.42.0.158   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-5587c8844c-rbtgx                  1/1     Running            10 (21d ago)   21d    10.42.0.157   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-76cfdd9798-tqvvw                  0/1     ImagePullBackOff   0              46m    10.42.0.67    tce-k3s-01   <none>           <none>
microfe-platform   nats-7bc8d9f768-q682m                        1/1     Running            0              21d    10.42.0.178   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-67f49fd5c5-4cq95                 0/1     ImagePullBackOff   0              46m    10.42.0.69    tce-k3s-01   <none>           <none>
stock-prod         stock-admin-7967788c6c-jg7b2                 0/1     ImagePullBackOff   0              100m   10.42.0.37    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-57ccb8ff6-d25jq                1/1     Running            0              41d    10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-866fb5fd57-zfs4m               0/1     ImagePullBackOff   0              46m    10.42.0.70    tce-k3s-01   <none>           <none>
stock-prod         stock-frontend-79c57845df-z747s              1/1     Running            0              41d    10.42.0.56    tce-k3s-01   <none>           <none>
tce-prod           tce-frontend-c8c48c548-fhx49                 1/1     Running            0              99m    10.42.0.39    tce-k3s-01   <none>           <none>
tce-prod           tce-service-69d975d9f9-fxxqj                 1/1     Running            0              160m   10.42.0.3     tce-k3s-01   <none>           <none>
tce-prod           tce-service-77dfdb7f5c-kmcz7                 0/1     Running            21 (55s ago)   99m    10.42.0.40    tce-k3s-01   <none>           <none>
NAMESPACE          NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager       cert-manager                1/1     1            1           66d
cert-manager       cert-manager-cainjector     1/1     1            1           66d
cert-manager       cert-manager-webhook        1/1     1            1           66d
kube-system        coredns                     1/1     1            1           69d
kube-system        local-path-provisioner      1/1     1            1           69d
kube-system        metrics-server              1/1     1            1           69d
kube-system        traefik                     1/1     1            1           69d
media-prod         media-generation            0/1     1            0           30d
media-prod         media-generation-frontend   1/1     1            1           29d
microfe-platform   keycloak                    0/1     1            0           14d
microfe-platform   microfe-auth                0/1     1            0           24d
microfe-platform   microfe-shell               1/1     1            1           24d
microfe-platform   microfe-ws                  1/1     1            1           24d
microfe-platform   nats                        1/1     1            1           21d
stock-prod         stock-admin                 0/1     1            0           37d
stock-prod         stock-backend               1/1     1            1           41d
stock-prod         stock-frontend              1/1     1            1           41d
tce-prod           tce-frontend                1/1     1            1           66d
tce-prod           tce-service                 1/1     1            1           66d

### Pod failure evidence
microfe-platform	microfe-shell-654b79579f-hqpbr	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-shell:0.1.0": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-shell:0.1.0": failed to resolve reference "ghcr.io/phanthienquoc/microfe-shell:0.1.0": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-shell%3Apull&service=ghcr.io: 403 Forbidden
microfe-platform	microfe-ws-76cfdd9798-tqvvw	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": failed to resolve reference "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-ws%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-admin-67f49fd5c5-4cq95	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fadmin%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-admin-7967788c6c-jg7b2	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fadmin%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-backend-866fb5fd57-zfs4m	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fbackend%3Apull&service=ghcr.io: 403 Forbidden

### Recent failure events

### TCE service diagnostics (last 2h; redacted)
NAME                           READY   STATUS    RESTARTS       AGE    IP           NODE         NOMINATED NODE   READINESS GATES
tce-service-69d975d9f9-fxxqj   1/1     Running   0              160m   10.42.0.3    tce-k3s-01   <none>           <none>
tce-service-77dfdb7f5c-kmcz7   0/1     Running   21 (56s ago)   99m    10.42.0.40   tce-k3s-01   <none>           <none>
-- pod tce-service-69d975d9f9-fxxqj describe --
### current logs for tce-service-69d975d9f9-fxxqj
### previous logs for tce-service-69d975d9f9-fxxqj

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
microfe-platform   microfe-shell               ghcr.io/phanthienquoc/microfe-shell:0.1.0
microfe-platform   microfe-ws                  ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA
microfe-platform   nats                        nats:2.12-alpine
stock-prod         stock-admin                 ghcr.io/phanthienquoc/stockdividend/admin:12d63b4
stock-prod         stock-backend               ghcr.io/phanthienquoc/stockdividend/backend:12d63b4
stock-prod         stock-frontend              ghcr.io/phanthienquoc/stockdividend/user:23b2878
tce-prod           tce-frontend                ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-e75e338
tce-prod           tce-service                 ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-e75e338
NAMESPACE          NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
cert-manager       cert-manager                ClusterIP      10.43.138.27    <none>        9402/TCP                     66d
cert-manager       cert-manager-cainjector     ClusterIP      10.43.135.132   <none>        9402/TCP                     66d
cert-manager       cert-manager-webhook        ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             66d
default            kubernetes                  ClusterIP      10.43.0.1       <none>        443/TCP                      69d
kube-system        kube-dns                    ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       69d
kube-system        metrics-server              ClusterIP      10.43.120.41    <none>        443/TCP                      69d
kube-system        traefik                     LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   69d
media-prod         media-generation            ClusterIP      10.43.252.95    <none>        3000/TCP                     30d
media-prod         media-generation-frontend   ClusterIP      10.43.48.52     <none>        80/TCP                       29d
microfe-platform   keycloak                    ClusterIP      10.43.142.95    <none>        80/TCP,9000/TCP              14d
microfe-platform   microfe-auth                ClusterIP      10.43.83.168    <none>        80/TCP                       24d
microfe-platform   microfe-shell               ClusterIP      10.43.6.23      <none>        80/TCP                       24d
microfe-platform   microfe-ws                  ClusterIP      10.43.86.34     <none>        8080/TCP                     24d
microfe-platform   nats                        ClusterIP      10.43.147.69    <none>        4222/TCP,8222/TCP            21d
stock-prod         backend                     ClusterIP      10.43.46.139    <none>        8080/TCP                     41d
stock-prod         stock-admin                 ClusterIP      10.43.97.150    <none>        3000/TCP                     37d
stock-prod         stock-backend               ClusterIP      10.43.247.219   <none>        8080/TCP                     41d
stock-prod         stock-frontend              ClusterIP      10.43.53.102    <none>        3000/TCP                     41d
tce-prod           tce-frontend                ClusterIP      10.43.99.130    <none>        80/TCP                       66d
tce-prod           tce-service                 ClusterIP      10.43.189.227   <none>        8210/TCP                     66d
NAMESPACE          NAME                               CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
media-prod         media                              traefik   media.mrcute.space                                             10.0.0.120   80, 443   30d
microfe-platform   keycloak-public                    traefik   sso.mrcute.space                                               10.0.0.120   80, 443   14d
microfe-platform   keycloak-registration-rate-limit   traefik   sso.mrcute.space                                               10.0.0.120   80, 443   2d10h
microfe-platform   microfe-public                     traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space             10.0.0.120   80, 443   24d
stock-prod         stock                              traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   37d
stock-prod         stock-ingress                      traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   41d
tce-prod           tce                                traefik   tce.mrcute.space                                               10.0.0.120   80, 443   66d

## K3s service
active
enabled

### K3s recent warnings (last 2h)

## Keycloak diagnostics
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
keycloak   0/1     1            0           14d   keycloak     quay.io/keycloak/keycloak:26.8.1   app.kubernetes.io/name=keycloak
2026-10-30 14:07:48,076 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
2026-10-30 14:07:52,327 ERROR [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01000: Error processing Health Checks: java.util.concurrent.RejectedExecutionException: No executor queue space remaining
2026-10-30 14:07:52,327 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"DOWN","data":{"Failing since":"2026-10-30 12:54:00,328"}},{"name":"org.keycloak.quarkus.runtime.services.health.KeycloakReadyHealthCheck_ClientProxy","status":"DOWN","data":{"exceptionClass":"java.util.concurrent.
2026-10-30 14:07:52,328 ERROR [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01000: Error processing Health Checks: java.util.concurrent.RejectedExecutionException: No executor queue space remaining
2026-10-30 14:07:52,328 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"DOWN","data":{"Failing since":"2026-10-30 12:54:00,328"}},{"name":"org.keycloak.quarkus.runtime.services.health.KeycloakReadyHealthCheck_ClientProxy","status":"DOWN","data":{"exceptionClass":"java.util.concurrent.
2026-10-30 14:08:02,329 ERROR [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01000: Error processing Health Checks: java.util.concurrent.RejectedExecutionException: No executor queue space remaining
2026-10-30 14:08:02,329 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"DOWN","data":{"Failing since":"2026-10-30 12:54:00,328"}},{"name":"org.keycloak.quarkus.runtime.services.health.KeycloakReadyHealthCheck_ClientProxy","status":"DOWN","data":{"exceptionClass":"java.util.concurrent.
2026-10-30 14:08:03,182 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"DOWN","data":{"Failing since":"2026-10-30 12:54:00,328"}},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 13:14:59,164"}}]}
2026-10-30 14:08:05,583 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (jgroups-10449,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: Failed to connect to database: authentication did not complete within 15000ms
2026-10-30 14:08:15,250 ERROR [org.keycloak.models.sessions.infinispan.expiration.BaseExpirationTask] (user-session-purge-expired) Unexpected error while removing expired entries from database: org.hibernate.exception.GenericJDBCException: Unable to acquire JDBC Connection [FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode] [n/a]
	at org.hibernate.exception.internal.StandardSQLExceptionConverter.convert(StandardSQLExceptionConverter.java:39)
	at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:115)
	at org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:101)
	at org.hibernate.resource.jdbc.internal.LogicalConnectionManagedImpl.acquire(LogicalConnectionManagedImpl.java:190)
	at org.hibernate.resource.jdbc.internal.LogicalConnectionManagedImpl.acquireConnectionIfNeeded(LogicalConnectionManagedImpl.java:87)
	at org.hibernate.resource.jdbc.internal.LogicalConnectionManagedImpl.getPhysicalConnection(LogicalConnectionManagedImpl.java:126)
	at org.hibernate.sql.exec.internal.JdbcSelectExecutorStandardImpl.doExecuteQuery(JdbcSelectExecutorStandardImpl.java:132)
	at org.hibernate.sql.exec.internal.JdbcSelectExecutorStandardImpl.executeQuery(JdbcSelectExecutorStandardImpl.java:100)
	at org.hibernate.sql.exec.spi.JdbcSelectExecutor.scroll(JdbcSelectExecutor.java:167)
	at org.keycloak.models.jpa.JpaRealmProvider.getRealms(JpaRealmProvider.java:186)
	at org.keycloak.models.jpa.JpaRealmProvider.getRealmsStream(JpaRealmProvider.java:172)
	at org.keycloak.models.cache.infinispan.RealmCacheSession.getRealmsStream(RealmCacheSession.java:571)
Caused by: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
	at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2993)
	at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:295)
	at org.hibernate.internal.NonContextualJdbcConnectionAccess.obtainConnection(NonContextualJdbcConnectionAccess.java:62)
	at org.hibernate.resource.jdbc.internal.LogicalConnectionManagedImpl.acquire(LogicalConnectionManagedImpl.java:187)
2026-10-30 14:08:21,997 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"DOWN","data":{"Failing since":"2026-10-30 12:54:00,328"}},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 13:14:59,164"}}]}
2026-10-30 14:08:22,661 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed reading from the DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
	at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2993)
	at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:295)
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator$ConnectionProviderJdbcConnectionAccess.obtainConnection(JdbcEnvironmentInitiator.java:508)
	at org.keycloak.quarkus.runtime.storage.database.jpa.AbstractJpaConnectionProviderFactory.getConnection(AbstractJpaConnectionProviderFactory.java:64)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.getConnection(KEYCLOAK_JDBC_PING2.java:97)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.readFromDB(KEYCLOAK_JDBC_PING2.java:207)
	at org.jgroups.protocols.JDBC_PING2.readAll(JDBC_PING2.java:339)
	at org.jgroups.protocols.JDBC_PING2.findMembers(JDBC_PING2.java:238)
2026-10-30 14:08:32,329 ERROR [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01000: Error processing Health Checks: java.util.concurrent.RejectedExecutionException: No executor queue space remaining
2026-10-30 14:08:32,329 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"DOWN","data":{"Failing since":"2026-10-30 12:54:00,328"}},{"name":"org.keycloak.quarkus.runtime.services.health.KeycloakReadyHealthCheck_ClientProxy","status":"DOWN","data":{"exceptionClass":"java.util.concurrent.

### Public OIDC probes (status and latency only)
https://sso.mrcute.space/realms/master/.well-known/openid-configuration http_code=503 time_total=0.149107s remote_ip=132.226.175.206
https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration http_code=503 time_total=0.049565s remote_ip=132.226.175.206
