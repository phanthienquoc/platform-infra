# Migration runner

Migrations are explicit one-shot Jobs and are never hidden in Deployment startup.

StockDividend source is backend/cmd/migrate/main.go. The current backend Dockerfile copies that source as migrate_src.go rather than compiling it, so migration execution is BLOCKED until the application image exposes an executable migration binary.

TCE has an apps/service migrate:events script. Verify its production database contract before enabling a migration Job.
