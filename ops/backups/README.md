# Backup and restore

Back up K3s datastore/node configuration separately from application data.

MongoDB Atlas and Supabase remain external data dependencies and must use their provider backup/PITR facilities. Local-path volumes are node-local and require explicit backup if used.

Never commit kubeconfig, database dumps, credentials or private keys.
