# Telegram notification templates

The production reconciliation workflow uses these Telegram templates.

## 1. Processing

```
🔄 <b>PRODUCTION • PROCESSING</b>
📦 App          <code>${APP}</code>
🏷️ Release      <code>${RELEASE}</code>
✓ GitOps synced
✓ VPS reconciliation
⏳ Rollout in progress
```

## 2. Rollout summary

```
<pre>🚀 PRODUCTION • ROLLOUT

📦 App             ${APP}
🏷️ Release         ${RELEASE}
🎯 Scope           ${SCOPE}

🟢 Status          ${STATUS}
🔒 Isolation       ENABLED</pre>
```

For multi-application reconciliation, the summary may include one status row per targeted workload.

Rules:
- Never include tokens, secret values, connection strings, private keys, or full credential-bearing configuration.
- Release values are immutable Git SHA tags (or the existing TCE release format).
- Telegram delivery is best-effort (`continue-on-error`) and must not hide deployment failures.