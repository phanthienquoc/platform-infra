# VPS inspection

Generated: 2026-09-22T14:59:42+00:00

## Host
uname: Linux chat-20260107-1525 6.8.0-1049-oracle #50~22.04.1-Ubuntu SMP Mon Apr  6 05:34:28 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
arch: aarch64
os: Ubuntu 22.04.5 LTS
hostname: chat-20260107-1525

## Resources
4
               total        used        free      shared  buff/cache   available
Mem:            23Gi       3.4Gi       2.6Gi        49Mi        17Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        45G   35G   11G  78% /
 14:59:42 up 144 days, 50 min,  1 user,  load average: 0.41, 0.25, 0.23

## Runner
uid=1002(github-runner) gid=1002(github-runner) groups=1002(github-runner),999(docker)
github-+ 1309509 11.5  0.4 273205820 113808 ?    Sl   14:59   0:03 /opt/actions-runner/bin/Runner.Listener run --startuptype service
github-+ 1310262 64.3  0.4 273285016 111872 ?    Sl   14:59   0:01 /opt/actions-runner/bin/Runner.Worker spawnclient 157 162
  actions.runner.phanthienquoc-platform-infra.platform-k3s-01.service loaded active running GitHub Actions Runner (phanthienquoc-platform-infra.platform-k3s-01)

## Docker
Docker version 29.1.3, build f52814d
Server=29.1.3 RootDir=/var/lib/docker

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
stock-prod        Active   3d8h
tce-prod          Active   31d
NAMESPACE      NAME                                      READY   STATUS      RESTARTS      AGE    IP            NODE         NOMINATED NODE   READINESS GATES
cert-manager   cert-manager-75b96c9588-lgn7d             1/1     Running     0             28d    10.42.0.98    tce-k3s-01   <none>           <none>
cert-manager   cert-manager-cainjector-b644b66f7-l8jdq   1/1     Running     1 (28d ago)   28d    10.42.0.100   tce-k3s-01   <none>           <none>
cert-manager   cert-manager-webhook-76d97df888-wwq49     1/1     Running     0             28d    10.42.0.99    tce-k3s-01   <none>           <none>
kube-system    coredns-54996dc9b4-d68pf                  1/1     Running     0             31d    10.42.0.6     tce-k3s-01   <none>           <none>
kube-system    helm-install-traefik-crd-mq7w8            0/1     Completed   0             31d    10.42.0.3     tce-k3s-01   <none>           <none>
kube-system    helm-install-traefik-s2twj                0/1     Completed   1 (31d ago)   31d    10.42.0.2     tce-k3s-01   <none>           <none>
kube-system    local-path-provisioner-58d557dc48-jbhhp   1/1     Running     1 (31d ago)   31d    10.42.0.5     tce-k3s-01   <none>           <none>
kube-system    metrics-server-6dc596dfb8-s2bzm           1/1     Running     0             31d    10.42.0.4     tce-k3s-01   <none>           <none>
kube-system    svclb-traefik-859779c1-7bwx2              2/2     Running     0             31d    10.42.0.7     tce-k3s-01   <none>           <none>
kube-system    traefik-59b7647586-gml84                  1/1     Running     0             31d    10.42.0.8     tce-k3s-01   <none>           <none>
stock-prod     stock-backend-57ccb8ff6-d25jq             1/1     Running     0             3d8h   10.42.0.55    tce-k3s-01   <none>           <none>
stock-prod     stock-frontend-79c57845df-z747s           1/1     Running     0             3d8h   10.42.0.56    tce-k3s-01   <none>           <none>
tce-prod       tce-frontend-64f468f759-zn7g5             1/1     Running     0             15h    10.42.0.65    tce-k3s-01   <none>           <none>
tce-prod       tce-service-749db66ff5-ks4m4              1/1     Running     0             15h    10.42.0.64    tce-k3s-01   <none>           <none>
NAMESPACE      NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager   cert-manager              1/1     1            1           28d
cert-manager   cert-manager-cainjector   1/1     1            1           28d
cert-manager   cert-manager-webhook      1/1     1            1           28d
kube-system    coredns                   1/1     1            1           31d
kube-system    local-path-provisioner    1/1     1            1           31d
kube-system    metrics-server            1/1     1            1           31d
kube-system    traefik                   1/1     1            1           31d
stock-prod     stock-backend             1/1     1            1           3d8h
stock-prod     stock-frontend            1/1     1            1           3d8h
tce-prod       tce-frontend              1/1     1            1           28d
tce-prod       tce-service               1/1     1            1           28d
NAMESPACE      NAME                      TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
cert-manager   cert-manager              ClusterIP      10.43.138.27    <none>        9402/TCP                     28d
cert-manager   cert-manager-cainjector   ClusterIP      10.43.135.132   <none>        9402/TCP                     28d
cert-manager   cert-manager-webhook      ClusterIP      10.43.52.112    <none>        443/TCP,9402/TCP             28d
default        kubernetes                ClusterIP      10.43.0.1       <none>        443/TCP                      31d
kube-system    kube-dns                  ClusterIP      10.43.0.10      <none>        53/UDP,53/TCP,9153/TCP       31d
kube-system    metrics-server            ClusterIP      10.43.120.41    <none>        443/TCP                      31d
kube-system    traefik                   LoadBalancer   10.43.213.239   10.0.0.120    80:30225/TCP,443:30415/TCP   31d
stock-prod     backend                   ClusterIP      10.43.46.139    <none>        8080/TCP                     3d8h
stock-prod     stock-backend             ClusterIP      10.43.247.219   <none>        8080/TCP                     3d8h
stock-prod     stock-frontend            ClusterIP      10.43.53.102    <none>        3000/TCP                     3d8h
tce-prod       tce-frontend              ClusterIP      10.43.99.130    <none>        80/TCP                       28d
tce-prod       tce-service               ClusterIP      10.43.189.227   <none>        8210/TCP                     28d
NAMESPACE    NAME            CLASS     HOSTS                                                          ADDRESS      PORTS     AGE
stock-prod   stock-ingress   traefik   mrcute.space,www.mrcute.space,admin.mrcute.space + 1 more...   10.0.0.120   80, 443   3d8h
tce-prod     tce             traefik   tce.mrcute.space                                               10.0.0.120   80, 443   28d

## K3s service
active
enabled
