# VPS inspection

Generated: 2026-10-30T01:58:49+00:00

## Host
uname: Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       4.4Gi       491Mi        86Mi        18Gi        18Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   33G   13G  72% /
disk_pressure: normal (72%)
 01:58:49 up 181 days, 11:49,  0 users,  load average: 0.39, 0.18, 0.22

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
21684 /opt/media-actions-runner/bin/Runner.Listener run --startuptype service
381569 /opt/actions-runner/bin/Runner.Worker spawnclient 154 159
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
linux-tools-common/jammy-updates 5.15.0-202.212 all [upgradable from: 5.15.0-198.208]
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
cert-manager       Active   65d
default            Active   69d
k3s-debug          Active   21d
kube-node-lease    Active   69d
kube-public        Active   69d
kube-system        Active   69d
media-prod         Active   29d
microfe-platform   Active   23d
stock-prod         Active   40d
tce-prod           Active   69d
NAMESPACE          NAME                                         READY   STATUS             RESTARTS       AGE     IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager       cert-manager-75b96c9588-lgn7d                1/1     Running            0              65d     10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager       cert-manager-cainjector-b644b66f7-l8jdq      1/1     Running            1 (65d ago)    65d     10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager       cert-manager-webhook-76d97df888-wwq49        1/1     Running            0              65d     10.42.0.99    tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29888745-2sqdn            0/1     StartError         0              12m     10.42.0.230   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29888745-7zvjs            0/1     StartError         0              13m     10.42.0.227   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29888745-9cdwx            0/1     StartError         0              8m37s   10.42.0.232   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29888745-b54qg            0/1     StartError         0              13m     10.42.0.229   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29888745-g7b6p            0/1     StartError         0              13m     10.42.0.228   tce-k3s-01   <none>           <none>
k3s-debug          k3s-debug-snapshot-29888745-w84qm            0/1     StartError         0              11m     10.42.0.231   tce-k3s-01   <none>           <none>
kube-system        coredns-54996dc9b4-d68pf                     1/1     Running            0              69d     10.42.0.6     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-crd-mq7w8               0/1     Completed          0              69d     10.42.0.3     tce-k3s-01   <none>           <none>
kube-system        helm-install-traefik-s2twj                   0/1     Completed          1 (69d ago)    69d     10.42.0.2     tce-k3s-01   <none>           <none>
kube-system        local-path-provisioner-58d557dc48-jbhhp      1/1     Running            1 (69d ago)    69d     10.42.0.5     tce-k3s-01   <none>           <none>
kube-system        metrics-server-6dc596dfb8-s2bzm              1/1     Running            0              69d     10.42.0.4     tce-k3s-01   <none>           <none>
kube-system        svclb-traefik-859779c1-7bwx2                 2/2     Running            0              69d     10.42.0.7     tce-k3s-01   <none>           <none>
kube-system        traefik-59b7647586-gml84                     1/1     Running            0              69d     10.42.0.8     tce-k3s-01   <none>           <none>
media-prod         media-generation-5c9b76dfb9-zh8jr            0/1     Running            0              15d     10.42.0.85    tce-k3s-01   <none>           <none>
media-prod         media-generation-frontend-597b779c9d-dvrft   1/1     Running            0              15d     10.42.0.84    tce-k3s-01   <none>           <none>
microfe-platform   keycloak-68c4bc764c-4pp66                    0/1     Running            0              13d     10.42.0.124   tce-k3s-01   <none>           <none>
microfe-platform   microfe-auth-7944f7ffcb-gh8b7                0/1     Running            0              93m     10.42.0.193   tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-56589cd67b-42x6n               0/1     ImagePullBackOff   0              93m     10.42.0.194   tce-k3s-01   <none>           <none>
microfe-platform   microfe-shell-dbbbfdf8c-5rkwz                1/1     Running            0              20d     10.42.0.158   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-5587c8844c-rbtgx                  1/1     Running            10 (20d ago)   20d     10.42.0.157   tce-k3s-01   <none>           <none>
microfe-platform   microfe-ws-777b6d9849-h9zsb                  0/1     ImagePullBackOff   0              93m     10.42.0.192   tce-k3s-01   <none>           <none>
microfe-platform   nats-7bc8d9f768-q682m                        1/1     Running            0              20d     10.42.0.178   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-569b69c98d-9sp8w                 0/1     ImagePullBackOff   0              93m     10.42.0.195   tce-k3s-01   <none>           <none>
stock-prod         stock-admin-7db6f8fcd4-fjb9q                 0/1     ImagePullBackOff   0              5h20m   10.42.0.92    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-57ccb8ff6-d25jq                1/1     Running            0              40d     10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod         stock-backend-8579cfb48b-rrj6v               0/1     ImagePullBackOff   0              93m     10.42.0.196   tce-k3s-01   <none>           <none>
stock-prod         stock-frontend-79c57845df-z747s              1/1     Running            0              40d     10.42.0.56    tce-k3s-01   <none>           <none>
tce-prod           tce-frontend-79988675b8-86clf                1/1     Running            0              4d9h    10.42.0.128   tce-k3s-01   <none>           <none>
tce-prod           tce-service-7f44bf89c7-cvvhs                 1/1     Running            0              4d9h    10.42.0.129   tce-k3s-01   <none>           <none>
NAMESPACE          NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager       cert-manager                1/1     1            1           65d
cert-manager       cert-manager-cainjector     1/1     1            1           65d
cert-manager       cert-manager-webhook        1/1     1            1           65d
kube-system        coredns                     1/1     1            1           69d
kube-system        local-path-provisioner      1/1     1            1           69d
kube-system        metrics-server              1/1     1            1           69d
kube-system        traefik                     1/1     1            1           69d
media-prod         media-generation            0/1     1            0           29d
media-prod         media-generation-frontend   1/1     1            1           29d
microfe-platform   keycloak                    0/1     1            0           13d
microfe-platform   microfe-auth                0/1     1            0           23d
microfe-platform   microfe-shell               1/1     1            1           23d
microfe-platform   microfe-ws                  1/1     1            1           23d
microfe-platform   nats                        1/1     1            1           20d
stock-prod         stock-admin                 0/1     1            0           36d
stock-prod         stock-backend               1/1     1            1           40d
stock-prod         stock-frontend              1/1     1            1           40d
tce-prod           tce-frontend                1/1     1            1           65d
tce-prod           tce-service                 1/1     1            1           65d

### Pod failure evidence
microfe-platform	microfe-shell-56589cd67b-42x6n	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-shell:0.1.0": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-shell:0.1.0": failed to resolve reference "ghcr.io/phanthienquoc/microfe-shell:0.1.0": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-shell%3Apull&service=ghcr.io: 403 Forbidden
microfe-platform	microfe-ws-777b6d9849-h9zsb	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": failed to resolve reference "ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fmicrofe-ws%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-admin-569b69c98d-9sp8w	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fadmin%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-admin-7db6f8fcd4-fjb9q	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/admin:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fadmin%3Apull&service=ghcr.io: 403 Forbidden
stock-prod	stock-backend-8579cfb48b-rrj6v	ImagePullBackOff	Back-off pulling image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": ErrImagePull: failed to pull and unpack image "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": failed to resolve reference "ghcr.io/phanthienquoc/stockdividend/backend:12d63b4": failed to authorize: failed to fetch oauth token: unexpected status from GET request to https://ghcr.io/token?scope=repository%3Aphanthienquoc%2Fstockdividend%2Fbackend%3Apull&service=ghcr.io: 403 Forbidden

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
media-prod         media-generation            ghcr.io/phanthienquoc/media-generation/backend:prod-v0.3.0-58f80a8
media-prod         media-generation-frontend   ghcr.io/phanthienquoc/media-generation/frontend:prod-v0.3.0-58f80a8
microfe-platform   keycloak                    quay.io/keycloak/keycloak:26.8.1
microfe-platform   microfe-auth                ghcr.io/phanthienquoc/auth-service/auth:prod-v1.0.0-aa40d00
microfe-platform   microfe-shell               ghcr.io/phanthienquoc/microfe-shell:0.1.0
microfe-platform   microfe-ws                  ghcr.io/phanthienquoc/microfe-ws:RELEASE_SHA
microfe-platform   nats                        nats:2.12-alpine
stock-prod         stock-admin                 ghcr.io/phanthienquoc/stockdividend/admin:12d63b4
stock-prod         stock-backend               ghcr.io/phanthienquoc/stockdividend/backend:12d63b4
stock-prod         stock-frontend              ghcr.io/phanthienquoc/stockdividend/user:23b2878
tce-prod           tce-frontend                ghcr.io/phanthienquoc/tce-dashboard/web:prod-v0.1.0-5801bb2
tce-prod           tce-service                 ghcr.io/phanthienquoc/tce-dashboard/service:prod-v0.1.0-5801bb2
NAMESPACE          NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
cert-manager       cert-manager                ClusterIP      10.43.138.27    <none>        9402/TCP                     65d
cert-manager       cert-manager-cainjector     ClusterIP      10.43.135.132   <none>        9402/TCP                     65d
cert-manager       cert-manager-webhook        ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             65d
default            kubernetes                  ClusterIP      10.43.0.1       <none>        443/TCP                      69d
kube-system        kube-dns                    ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       69d
kube-system        metrics-server              ClusterIP      10.43.120.41    <none>        443/TCP                      69d
kube-system        traefik                     LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   69d
media-prod         media-generation            ClusterIP      10.43.252.95    <none>        3000/TCP                     29d
media-prod         media-generation-frontend   ClusterIP      10.43.48.52     <none>        80/TCP                       29d
microfe-platform   keycloak                    ClusterIP      10.43.142.95    <none>        80/TCP,9000/TCP              13d
microfe-platform   microfe-auth                ClusterIP      10.43.83.168    <none>        80/TCP                       23d
microfe-platform   microfe-shell               ClusterIP      10.43.6.23      <none>        80/TCP                       23d
microfe-platform   microfe-ws                  ClusterIP      10.43.86.34     <none>        8080/TCP                     23d
microfe-platform   nats                        ClusterIP      10.43.147.69    <none>        4222/TCP,8222/TCP            20d
stock-prod         backend                     ClusterIP      10.43.46.139    <none>        8080/TCP                     40d
stock-prod         stock-admin                 ClusterIP      10.43.97.150    <none>        3000/TCP                     36d
stock-prod         stock-backend               ClusterIP      10.43.247.219   <none>        8080/TCP                     40d
stock-prod         stock-frontend              ClusterIP      10.43.53.102    <none>        3000/TCP                     40d
tce-prod           tce-frontend                ClusterIP      10.43.99.130    <none>        80/TCP                       65d
tce-prod           tce-service                 ClusterIP      10.43.189.227   <none>        8210/TCP                     65d
NAMESPACE          NAME                               CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
media-prod         media                              traefik   media.mrcute.space                                             10.0.0.120   80, 443   29d
microfe-platform   keycloak-public                    traefik   sso.mrcute.space                                               10.0.0.120   80, 443   13d
microfe-platform   keycloak-registration-rate-limit   traefik   sso.mrcute.space                                               10.0.0.120   80, 443   46h
microfe-platform   microfe-public                     traefik   app.mrcute.space,auth.mrcute.space,ws.mrcute.space             10.0.0.120   80, 443   23d
stock-prod         stock                              traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   36d
stock-prod         stock-ingress                      traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   40d
tce-prod           tce                                traefik   tce.mrcute.space                                               10.0.0.120   80, 443   65d

### Ingress hosts
media-prod         media                              media.mrcute.space
microfe-platform   keycloak-public                    sso.mrcute.space
microfe-platform   keycloak-registration-rate-limit   sso.mrcute.space
microfe-platform   microfe-public                     app.mrcute.space,auth.mrcute.space,ws.mrcute.space
stock-prod         stock                              mrcute.space,www.mrcute.space,admin.mrcute.space,api.mrcute.space
stock-prod         stock-ingress                      mrcute.space,www.mrcute.space,admin.mrcute.space,api.mrcute.space
tce-prod           tce                                tce.mrcute.space

## K3s service
active
enabled

## Keycloak diagnostics (read-only; namespace=microfe-platform)
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
keycloak   0/1     1            0           13d   keycloak     quay.io/keycloak/keycloak:26.8.1   app.kubernetes.io/name=keycloak
keycloak-68c4bc764c-4pp66        0/1     Running            0              13d   10.42.0.124   tce-k3s-01   <none>           <none>
keycloak        ClusterIP   10.43.142.95   <none>        80/TCP,9000/TCP     13d

### Keycloak recent diagnostic log lines (last 2h; redacted)
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator$ConnectionProviderJdbcConnectionAccess.obtainConnection(JdbcEnvironmentInitiator.java:508)
	at org.keycloak.quarkus.runtime.storage.database.jpa.AbstractJpaConnectionProviderFactory.getConnection(AbstractJpaConnectionProviderFactory.java:64)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.getConnection(KEYCLOAK_JDBC_PING2.java:97)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.readFromDB(KEYCLOAK_JDBC_PING2.java:207)
	at org.jgroups.protocols.JDBC_PING2.readAll(JDBC_PING2.java:339)
	at org.jgroups.protocols.JDBC_PING2.findMembers(JDBC_PING2.java:238)
2026-10-30 01:54:13,657 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:54:31,153 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:54:36,654 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: This connection has been closed.
2026-10-30 01:54:48,661 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:55:06,161 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:55:08,459 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (jgroups-10029,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
2026-10-30 01:55:09,566 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:55:24,876 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed reading from the DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
	at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2993)
	at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:295)
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator$ConnectionProviderJdbcConnectionAccess.obtainConnection(JdbcEnvironmentInitiator.java:508)
	at org.keycloak.quarkus.runtime.storage.database.jpa.AbstractJpaConnectionProviderFactory.getConnection(AbstractJpaConnectionProviderFactory.java:64)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.getConnection(KEYCLOAK_JDBC_PING2.java:97)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.readFromDB(KEYCLOAK_JDBC_PING2.java:207)
	at org.jgroups.protocols.JDBC_PING2.readAll(JDBC_PING2.java:339)
	at org.jgroups.protocols.JDBC_PING2.findMembers(JDBC_PING2.java:238)
2026-10-30 01:55:27,068 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:55:43,485 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
2026-10-30 01:55:44,570 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:56:00,975 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (jgroups-10034,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
2026-10-30 01:56:02,072 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:56:05,107 ERROR [org.keycloak.models.sessions.infinispan.expiration.BaseExpirationTask] (user-session-purge-expired) Unexpected error while removing expired entries from database: org.hibernate.exception.GenericJDBCException: Unable to acquire JDBC Connection [FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode] [n/a]
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
2026-10-30 01:56:19,575 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:56:19,575 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed reading from the DB: org.postgresql.util.PSQLException: FATAL: Failed to connect to database: authentication did not complete within 15000ms
	at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2993)
	at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:295)
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator$ConnectionProviderJdbcConnectionAccess.obtainConnection(JdbcEnvironmentInitiator.java:508)
	at org.keycloak.quarkus.runtime.storage.database.jpa.AbstractJpaConnectionProviderFactory.getConnection(AbstractJpaConnectionProviderFactory.java:64)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.getConnection(KEYCLOAK_JDBC_PING2.java:97)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.readFromDB(KEYCLOAK_JDBC_PING2.java:207)
	at org.jgroups.protocols.JDBC_PING2.readAll(JDBC_PING2.java:339)
	at org.jgroups.protocols.JDBC_PING2.findMembers(JDBC_PING2.java:238)
2026-10-30 01:56:37,076 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: Failed to connect to database: authentication did not complete within 15000ms
2026-10-30 01:56:37,077 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:56:54,579 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (jgroups-10030,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: Failed to connect to database: authentication did not complete within 15000ms
2026-10-30 01:56:54,579 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:57:12,080 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:57:29,583 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:57:47,086 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:57:49,674 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed reading from the DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
	at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2993)
	at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:295)
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator$ConnectionProviderJdbcConnectionAccess.obtainConnection(JdbcEnvironmentInitiator.java:508)
	at org.keycloak.quarkus.runtime.storage.database.jpa.AbstractJpaConnectionProviderFactory.getConnection(AbstractJpaConnectionProviderFactory.java:64)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.getConnection(KEYCLOAK_JDBC_PING2.java:97)
	at org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2.readFromDB(KEYCLOAK_JDBC_PING2.java:207)
	at org.jgroups.protocols.JDBC_PING2.readAll(JDBC_PING2.java:339)
	at org.jgroups.protocols.JDBC_PING2.findMembers(JDBC_PING2.java:238)
2026-10-30 01:58:07,175 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (Timer runner-2,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
2026-10-30 01:58:18,901 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:58:24,677 ERROR [org.keycloak.jgroups.protocol.KEYCLOAK_JDBC_PING2] (jgroups-10035,keycloak-68c4bc764c-4pp66-19695(v=16.0.15)) keycloak-68c4bc764c-4pp66-19695(v=16.0.15): failed writing to DB: org.postgresql.util.PSQLException: FATAL: (ECHECKOUTTIMEOUT) unable to check out connection from the pool after 15000ms in Session mode
2026-10-30 01:58:36,742 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}
2026-10-30 01:58:54,244 INFO  [io.smallrye.health] (vert.x-eventloop-thread-0) SRHCK01001: Reporting health down status: {"status":"DOWN","checks":[{"name":"Graceful Shutdown","status":"UP"},{"name":"Keycloak Initialized","status":"UP"},{"name":"Keycloak cluster health check","status":"UP"},{"name":"Keycloak database connections async health check","status":"DOWN","data":{"Failing since":"2026-10-30 01:52:46,136"}}]}

### Public OIDC endpoint probes (status and latency only; response bodies omitted)
https://sso.mrcute.space/realms/master/.well-known/openid-configuration http_code=503 time_total=0.165333s remote_ip=132.226.175.206
https://sso.mrcute.space/realms/mrcute/.well-known/openid-configuration http_code=503 time_total=0.049203s remote_ip=132.226.175.206
