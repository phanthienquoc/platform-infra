# K3s baseline

Capture before rebuild: k3s version, systemd config, K3s config, nodes, namespaces, workloads, services, ingress, PVC/PV, CRDs and manifests directory.

The current architecture is single-node. Local-path storage is node-bound; this is not HA.

K3s packages CoreDNS, Traefik, metrics-server and local-path storage. Do not duplicate these components. Use K3s-supported configuration overrides for packaged components.
