# TCE runtime contract

Frontend image exposes port 80. Service image exposes port 8210 and reports health at /api/health.

The service uses NestJS ScheduleModule and contains the engine runtime in the service process. There is no evidence that engines require an independent Deployment; keep one service Deployment until runtime profiling proves a separate worker boundary is needed.

The current service image must be published to GHCR before the production overlay tag can be reconciled.
