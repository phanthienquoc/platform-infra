# Platform layer

K3s packaged components are the baseline. This repository records ownership and adds only external configuration that should be declarative.

Traefik, metrics-server and local-path are K3s-managed. cert-manager is separately managed in the cluster and its issuer contract is referenced by application ingress resources.
