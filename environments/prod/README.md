# Production

This is the production Kustomize entrypoint. CI validates it but does not contain cluster credentials.

Use kubectl kustomize environments/prod, kubectl diff -k environments/prod and kubectl apply -k environments/prod from an authorized operator context.
