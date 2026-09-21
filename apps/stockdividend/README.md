# StockDividend runtime contract

Backend listens on 8080. Admin listens on 3000. Scraper API listens on 5000 and exposes /health.

The scraper has a long-running server mode and a separate one-shot scraper.py command. Production keeps the API Deployment and the weekly one-shot CronJob separate.

The current backend image does not compile the migration source into an executable binary; migration execution remains blocked until the application image is corrected.
