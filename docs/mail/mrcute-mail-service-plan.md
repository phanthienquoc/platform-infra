# mrcute.space Mail Service — Architecture & Implementation Plan

**Decision:** Managed domain mailboxes for 3–5 users.
**Preferred provider:** Zoho Mail Lite, subject to confirmation of Vietnam account/data-center availability and final checkout terms.
**Status:** Documentation planning only. No subscription purchased, mailboxes provisioned, DNS/MX records changed, credentials created, or production configuration changed.

## 1. Confirmed scope
- Domain: `mrcute.space`
- Service: real inbound/outbound human mailboxes.
- Hosting: managed provider; no self-hosted mail workload on K3s/VPS.
- Capacity: 3–5 paid mailbox users (exact seat count remains to confirm).
- Existing Resend SMTP remains separate for Keycloak/application transactional email.
- MX/DNS cutover requires a separate explicit production approval.

## 2. Provider recommendation and budget

Zoho official pricing lists Mail Lite at **US$1/user/month billed annually**, 5 GB/user; Mail Premium is US$4/user/month annually, 50 GB/user. Zoho advertises a free tier for up to five users only in select data centers; it excludes IMAP/POP/ActiveSync. Do not assume free-tier availability.

| Users | Monthly equivalent | Annual reference |
|---:|---:|---:|
| 3 | US$3 | US$36 |
| 4 | US$4 | US$48 |
| 5 | US$5 | US$60 |

Before taxes, FX and reseller fees. Confirm data-center availability, annual commitment, IMAP/mobile support and final checkout quote before purchase.

Alternatives:
- Microsoft 365 Business Basic (no Teams): US$2.70/user/month annually on the Vietnam page; five seats ≈ US$162/year before tax. Includes custom-domain email, Office web/mobile and 1 TB cloud storage/user.
- Google Workspace Business Starter: Vietnam page advertises US$3.50/user/month promotional pricing for eligible new customers (up to first 20 users added in 12 months); displayed regular price US$7. Five seats ≈ US$210/year promo or US$420/year at displayed regular price.

Sources:
- https://www.zoho.com/mail/zohomail-pricing.html
- https://www.microsoft.com/vi-vn/microsoft-365/business/microsoft-365-business-basic
- https://google.workspace.vn/bang-gia.html

**Recommendation:** Zoho Mail Lite is the cost-focused mailbox-only option. Choose Microsoft/Google if productivity-suite integration justifies the higher recurring cost.

## 3. Proposed mailbox model (not provisioned)
- `admin@mrcute.space` — restricted admin mailbox, MFA and recovery controls.
- `support@mrcute.space` — support correspondence.
- `contact@mrcute.space` — public contact.
- 1–2 named operator mailboxes, assigned to actual people.

Use aliases/groups for role addresses if supported and if shared access requirements are met. Never share a person's password. Confirm whether 3–5 means paid users or total addresses including aliases.

## 4. Architecture

```text
People / mail clients -> Managed Zoho Mail tenant
                         |-- 3–5 mailboxes
                         |-- aliases/groups (if supported)
                         |-- provider-managed storage/spam controls
                         |-- MX inbound + SPF/DKIM/DMARC
Keycloak / TCE / apps -> existing Resend SMTP (transactional, separate)
```

Managed hosting requires **0 additional K3s CPU, RAM, persistent storage or mail ports**. Provider manages mailbox infrastructure; tenant security, recovery and lifecycle still need configuration.

## 5. DNS and migration plan

**No production DNS changes are authorized by this PR.**
1. Verify domain ownership using provider-issued TXT/CNAME.
2. Export current authoritative DNS and identify existing MX, SPF, DKIM, DMARC and legitimate senders.
3. Create tenant/mailboxes before MX cutover if supported.
4. Obtain exact provider-issued MX/SPF/DKIM records; never invent values.
5. Maintain one SPF TXT policy and merge authorized senders; do not publish multiple SPF records.
6. Preserve Resend authorization while Keycloak uses Resend, including required DKIM selectors.
7. Keep DMARC monitoring and review aggregate reports before enforcement.
8. Decide whether historical mail migration is required; changing MX does not migrate old messages.
9. Prepare exact DNS diff, TTL, impact, cutover window and rollback.
10. Submit production DNS changes for separate human approval.
11. After approval, verify inbound/outbound delivery to Gmail, Outlook and another external domain, SPF/DKIM/DMARC alignment, and continued Resend delivery.

## 6. Security and operations
- Enforce MFA for tenant admins/users where supported.
- Unique accounts; no shared passwords.
- At least two authorized recovery contacts; restrict admin roles.
- Enable available anti-spam/phishing/malware controls.
- Define forwarding restrictions, retention, offboarding and recovery.
- Keep credentials out of Git, frontend bundles and logs.
- Keep Resend as app transactional sender unless separately approved.
- Record billing owner, renewal date, seat count and cancellation terms.

## 7. Resource envelope

| Resource | Managed mailbox plan |
|---|---|
| K3s CPU/RAM | 0 additional |
| K3s persistent storage | 0 additional |
| VPS static IP / PTR / port 25 | Not required |
| Provider storage | 5 GB/user reference; 15–25 GB for 3–5 seats |
| Subscription | US$36–60/year reference for 3–5 seats, before tax/FX |
| Operations | Tenant admin, MFA, DNS cutover, account lifecycle, renewal |

## 8. Phased implementation and gates

### Phase 0 — Scope/provider readiness
- [x] Confirm mailbox-only, managed hosting, 3–5 users.
- [x] Compare providers and published reference pricing.
- [ ] Confirm exact paid-seat count and alias/group model.
- [ ] Confirm Zoho plan/data-center availability and final checkout terms.
- [ ] Decide historical mail migration.

### Phase 1 — Tenant setup (external provider)
- [ ] Admin creates Zoho organization and selects region/plan.
- [ ] Review billing commitment/tax before purchase.
- [ ] Verify domain using provider-issued TXT/CNAME.
- [ ] Create 3–5 accounts and role aliases/groups.
- [ ] Enforce MFA/recovery.
- [ ] Do not switch MX yet.

### Phase 2 — DNS proposal
- [ ] Export current DNS records.
- [ ] Collect provider-issued MX/SPF/DKIM values.
- [ ] Prepare exact diff, TTL, impact and rollback plan.
- [ ] Ensure SPF preserves Resend and all legitimate senders.
- [ ] Review DMARC reporting/policy.
- [ ] Submit separate production change for approval.

### Phase 3 — Approved cutover
- [ ] Human approves exact DNS diff and maintenance window.
- [ ] Authorized DNS operator applies MX/SPF/DKIM/DMARC.
- [ ] Verify propagation, inbound/outbound mail and client access.
- [ ] Verify Resend transactional delivery still passes.
- [ ] Document ownership, recovery and renewal.

## 9. Acceptance criteria
- 3–5 intended users provisioned with MFA.
- Domain verified in provider tenant.
- Inbound/outbound mail work after approved MX cutover.
- SPF, DKIM and DMARC align.
- Existing Resend transactional mail continues to deliver.
- Spam controls, recovery, offboarding and renewal owner documented.
- No credentials committed to Git.
- Production DNS change has separately approved diff and rollback.

## 10. Explicit non-goals / safety boundary
- No Mailu/mailcow or other self-hosted workload.
- No K3s Deployment, Service, PVC, ingress or public mail ports.
- No subscription purchase or mailbox provisioning by this PR.
- No production DNS/MX/SPF/DKIM/DMARC writes.
- No Keycloak SMTP change; Resend remains independent.
- No secrets/passwords in repository.

## 11. Remaining inputs before signup/cutover
1. Exact paid-seat count (3, 4 or 5).
2. Whether support/contact need shared multi-user access or can be aliases/groups.
3. Whether historical mail at this domain must be migrated.
4. Acceptance of Zoho Mail Lite annual billing and available data center.

## GitHub traceability
Documentation-only PR: https://github.com/phanthienquoc/platform-infra/pull/1314. Keep unmerged until reviewed. This plan does not authorize production changes.
