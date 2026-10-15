---
id: security-faq
version: 2.4
owner: Lena Voss (Security & Compliance)
backup: Tom Adeyemi (Legal)
status: current
last_reviewed: 2026-10-08
---

# Kestrel security and compliance FAQ

Claims about certifications, retention, and data handling require Legal co-sign at Gate 4. The approved phrasing below is the only phrasing. Do not strengthen it.

## Certifications

**SOC 2 Type II.** Northfield Labs completed its SOC 2 Type II audit for the period of April 1, 2025 to March 31, 2026. The report covers the Security, Availability, and Confidentiality trust service criteria. The report is available to customers and prospects under NDA.

Approved phrasing: "Kestrel is SOC 2 Type II audited for Security, Availability, and Confidentiality."

Not approved: "SOC 2 certified" (SOC 2 is an attestation, not a certification), "fully compliant," any mention of Processing Integrity or Privacy criteria (not in scope).

**ISO 27001.** In progress. Expected completion Q1 2027. Do not mention in external content until Lena Voss updates this file.

**HIPAA, FedRAMP.** Not in scope. Do not mention.

## Data handling

- Customer audit data is encrypted at rest (AES-256) and in transit (TLS 1.2 or higher).
- Data is stored in the customer's chosen region: US East, EU West (Ireland), or AP Southeast (Sydney). Data does not leave the chosen region.
- Northfield staff access to customer data requires a logged, time-limited access grant approved by the customer. These grants are visible to the customer in their own Kestrel instance.

## Retention and deletion

- Retention is configurable per source from 30 days to 7 years, subject to plan limits.
- On contract termination, customer data is deleted within 30 days. A deletion certificate is available on request.

## Incident history

Northfield Labs has had no reportable security incidents as of the last review date of this file. Do not say "never had a breach"; say "no reportable incidents as of [date]" if the claim is needed at all. Prefer not to make the claim.

## Penetration testing

Annual third-party penetration test. The most recent was completed in July 2026. Summary available under NDA.
