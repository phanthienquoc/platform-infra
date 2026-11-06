# Migration runner

Migrations are explicit one-shot Jobs and are never hidden in Deployment startup.

TCE has an `apps/service` `migrate:events` script. Verify its production database contract and backup/rollback plan before enabling a migration Job.

StockDividend migration execution is outside this Platform repository; do not restore StockDividend migration Jobs or application manifests here.
