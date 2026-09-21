# Operations

Sequence: render -> validate -> diff -> migration if required -> platform -> StockDividend -> rollout -> TCE -> rollout -> smoke -> record revisions.

Rollback is performed by reverting the Git image/config revision and reconciling. Avoid hot-editing live resources as the normal operating model.
