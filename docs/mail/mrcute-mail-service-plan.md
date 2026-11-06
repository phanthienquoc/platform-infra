# mrcute.space Mail Service — Architecture & Implementation Plan

**Status:** Proposed — planning only; no mail workload, DNS, secrets, or production settings changed.
**Scope:** A domain email capability for `mrcute.space`, distinct from transactional SMTP used by Keycloak.

## 1. Clarify the requirement

"Mail server" can mean two different services:

- **Transactional outbound email:** applications send verification, password reset, notifications, and alerts. No mailbox hosting or inbound MX required.
- **Domain mailbox service:** users can receive and send mail as `name@mrcute.space`, requiring inbound MX, mailbox storage, IMAP/webmail, SMTP submission, spam filtering, backup and abuse operations.

The existing platform already has a Resend SMTP integration for Keycloak in the `mrcute` realm. It uses `smtp.resend.com:465`, SSL, the sender from GitHub Environment variable `RESEND_SMTP_FROM`, and a protected `RESEND_SMTP_API_KEY` secret. That is an outbound provider integration, not a hosted mailbox server.

**Recommended default:** keep Resend for transactional outbound mail. Do not deploy a self-hosted full mail stack merely to provide app email delivery. Assess mailbox hosting as a separate decision if actual inboxes are needed.

## 2. Recommended logical architecture

```text
Apps / Keycloak / alerting
       |
       | SMTP over TLS (provider credentials from secret store)
       v
Resend transactional email
       |
       v
Verified mrcute.space sender domain

Optional mailbox service (separate project / decision):
Internet MX -> mail gateway -> spam / malware filtering -> mailbox storage
                                              |-> IMAP / webmail
Apps / users -> authenticated SMTP submission -+
```

Keep the identity provider and application APIs independent of the mail delivery provider. Use provider adapters/configuration per application; never expose SMTP credentials to browser code.

## 3. Provider and hosting options

| Option | What it provides | Operations/resource profile | Recommendation |
|---|---|---|---|
| Resend | Transactional outbound API/SMTP | No cluster workload; domain DNS + API key; provider handles delivery | Preferred for app/system mail |
| Hosted mailbox provider (e.g. Google Workspace, Microsoft 365, Zoho Mail) | Managed inboxes, inbound/outbound mail, admin controls | Subscription per mailbox/user; DNS onboarding; no VPS mail stack | Preferred if people need inboxes |
| Self-hosted mail stack (e.g. mailcow / Mailu) | Mailboxes, SMTP, IMAP, webmail, spam filtering | Persistent storage, memory/CPU, public IP, reverse DNS, reputation, patching, backups and 24/7 monitoring | Only if self-hosting is an explicit requirement |

Do not conflate a Resend SMTP credential with a mailbox account; it cannot provide an inbox or IMAP access.

## 4. Existing platform integration

Verified repository artifacts:

- `.github/workflows/configure-keycloak-resend-smtp.yml` — manual workflow, production Environment, requires `KEYCLOAK_ADMIN_USERNAME`, `KEYCLOAK_ADMIN_PASSWORD`, `RESEND_SMTP_API_KEY` and `RESEND_SMTP_FROM`.
- `scripts/configure-keycloak-resend-smtp.py` — tests SMTP connection before enabling verification/reset; configures host `smtp.resend.com`, port `465`, SSL, username `resend`.
- `docs/auth-central/keycloak-self-registration.md` — requires successful verification and password-reset email tests before public registration.
- `docs/auth-central/keycloak-no-email-registration.md` — documents an opt-in no-verification path; it explicitly notes password reset remains disabled when SMTP is not configured.

This project plan does not run those workflows or change realm settings.

## 5. DNS and security requirements

### Transactional outbound (Resend)

1. Add `mrcute.space` as a sending domain in the provider.
2. Publish exactly the provider-issued DNS records (domain verification, DKIM, SPF/return-path as instructed).
3. Preserve one coherent SPF policy; merge mechanisms rather than publishing multiple SPF TXT records.
4. Add DMARC initially with a monitored policy (e.g. `p=none`), inspect aggregate reports, then raise enforcement after legitimate sources are confirmed.
5. Configure a dedicated sender such as `noreply@mrcute.space`; use a separate human mailbox provider if replies/inboxes are required.
6. Verify domain/sender status and test delivery to multiple external providers.

Do not invent DNS values. The provider dashboard is authoritative for generated records.

### Hosted mailbox

- Add provider MX records exactly as supplied.
- Configure provider-required SPF, DKIM and DMARC.
- Enable MFA for administrators and users; use least-privilege admin roles.
- Configure recovery, retention, forwarding and offboarding policies.

### Self-hosted mailbox

- Require static public IPv4/IPv6 as appropriate and provider-supported PTR/rDNS for the mail hostname.
- Confirm port 25 inbound/outbound is not blocked by the VPS provider.
- Use a dedicated hostname (e.g. `mail.mrcute.space`) with valid TLS; do not repurpose `auth.mrcute.space` or `sso.mrcute.space`.
- Publish MX, SPF, DKIM and DMARC records only after the endpoint and egress reputation are ready.
- Protect SMTP submission with authentication and TLS; never allow open relay.
- Require anti-abuse controls, rate limiting, queue monitoring, malware/spam filtering, immutable audit trails where appropriate, patching and tested restore.

## 6. Resource estimate

These are planning estimates, not measured VPS capacity or provider quotes.

| Architecture | Compute | Memory | Persistent storage | Other dependencies |
|---|---:|---:|---:|---|
| Resend transactional only | 0 additional vCPU | 0 additional RAM | 0 | DNS records, provider account, protected secret |
| Hosted mailboxes | 0 on K3s | 0 on K3s | Provider-managed | Paid seats, DNS, admin MFA |
| Small self-hosted mailbox pilot | 2–4 vCPU recommended | 4–8 GiB recommended | Start 50–100 GiB SSD, expandable | Static IP, PTR/rDNS, ports 25/465/587/993, backups, monitoring |

The self-hosted estimate is a conservative starting envelope; actual demand depends on mailbox count, retention, attachments, spam load and stack selection. It is not evidence that the current single-node K3s node has spare capacity. Do not schedule a deployment until current CPU/RAM/disk/network/backup headroom is measured.

## 7. Delivery phases and gates

### Phase 0 — Decide product scope
- [ ] Confirm transactional-only versus human mailboxes.
- [ ] Estimate number of addresses, users, storage and retention.
- [ ] Confirm whether users need webmail, IMAP/mobile clients, shared inboxes, aliases or catch-all.
- [ ] Identify current VPS public IP, provider port-25 policy and reverse-DNS capability only if self-hosting is considered.

### Phase 1 — Transactional mail readiness (preferred)
- [ ] Verify Resend account and domain ownership.
- [ ] Publish provider-generated SPF/DKIM records.
- [ ] Set DMARC monitoring and review reports.
- [ ] Configure protected GitHub Environment secret/variables; never commit credentials.
- [ ] Run the existing Keycloak SMTP workflow only after human approval and verify real verification/reset messages.
- [ ] Document sender identities, provider limits, webhook/bounce handling and delivery monitoring.

### Phase 2 — Mailbox provider (only if inboxes are required)
- [ ] Compare costs and capabilities for hosted providers.
- [ ] Create mailboxes/aliases and admin MFA.
- [ ] Add MX/SPF/DKIM/DMARC and validate inbound/outbound delivery.
- [ ] Test spam handling, recovery, offboarding and retention.

### Phase 3 — Self-hosted deployment (only if explicitly selected)
- [ ] Measure VPS capacity and confirm static IP/PTR/port 25.
- [ ] Select and pin a maintained mail stack and OS/runtime support matrix.
- [ ] Decide dedicated VM/VPS versus K3s. Prefer an isolated host/VM over co-locating the stateful mail stack with app workloads on the existing single-node K3s.
- [ ] Design persistent storage, backups, restore drills, monitoring, upgrades and incident response.
- [ ] Review firewall, DNS, TLS, anti-open-relay, rate limits and abuse controls.
- [ ] Build non-production validation first; production cutover is a separate reviewed change.

## 8. Acceptance criteria

### Transactional
- Sender domain verified.
- SPF, DKIM and DMARC records resolve and pass external checks.
- TLS SMTP authentication works without credential leakage.
- Keycloak verification and password reset successfully reach external mailboxes.
- Bounce/complaint handling and delivery health are observable.

### Mailboxes
- Inbound MX delivery and authenticated outbound submission work.
- IMAP/webmail TLS works.
- No open relay; spam and malware filtering are active.
- MFA, mailbox quotas, backups and restore are verified.
- SPF/DKIM/DMARC alignment passes external recipient checks.

## 9. Open decision

**Required before implementation:** do you need (A) system/app emails only, or (B) actual human inboxes such as `admin@mrcute.space` and `support@mrcute.space`?

Until this is answered, the safe implementation boundary is to retain the existing Resend integration and not add a mail server workload, change MX records, or change production DNS.
