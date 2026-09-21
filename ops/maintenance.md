# Maintenance

Inspect first. Never delete an active Job without confirming its owner and purpose. For CronJobs use concurrencyPolicy=Forbid and a bounded activeDeadlineSeconds. For single-node K3s, schedule disruptive maintenance only with an explicit rollback plan.
