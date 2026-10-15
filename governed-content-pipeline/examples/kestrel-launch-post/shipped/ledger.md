# Claims ledger: kestrel-soc2-linkedin

Brief: examples/kestrel-launch-post/brief.md
Built: 2026-10-06

| # | Claim (as it will appear) | Status | Source file | Section | Version | Disposition / note |
|---|---|---|---|---|---|---|
| C1 | Kestrel is SOC 2 Type II audited for Security, Availability, and Confidentiality. | SUPPORTED | canon/security-faq.md | Certifications | 2.4 | Approved phrasing, verbatim |
| C2 | The audit period was April 1, 2025 to March 31, 2026. | SUPPORTED | canon/security-faq.md | Certifications | 2.4 | |
| C3 | The report is available to customers and prospects under NDA. | SUPPORTED | canon/security-faq.md | Certifications | 2.4 | |
| C4 | "Before Kestrel our change history lived in four tools and two people's memories. Our last audit took three weeks of reconstruction. This one took an afternoon." — Ingrid Solheim, Head of Platform Engineering, Halvard Logistics | SUPPORTED | canon/customer-proof.md | Quotes / Q1 | 1.6 | Verbatim. LinkedIn is in the approved channel list. Expires 2027-03-31. |
| C5 | Kestrel is fully SOC 2 compliant. | UNSUPPORTED | | | | cut: security-faq.md lists "fully compliant" as not approved. C1 covers it. |
| C6 | Pricing starts at $250 a month. | UNSUPPORTED | | | | cut: source is pricing-2025, status retired. Replacement is C7. |
| C7 | Starts at $400 a month on an annual plan. | SUPPORTED | canon/pricing-and-packaging.md | Approved price phrasing | 4.0 | Optional per Gate 0. |
| C8 | Kestrel is also pursuing ISO 27001. | UNSUPPORTED | | | | cut: security-faq.md says do not mention until updated. |
| C9 | Customers we surveyed cut median audit prep time from 9 days to 1.5 days. | SUPPORTED | canon/customer-proof.md | Outcome numbers / N1 | 1.6 | Qualifier "customers we surveyed" required and present. Not in brief's required list; added as a candidate. |
| C10 | Kestrel answers who changed what, and who said they could. | SUPPORTED | canon/product-overview.md | Positioning line (approved) | 3.2 | |
| C11 | Most customers connect more than a dozen sources in their first two months. | SUPPORTED | canon/customer-proof.md | Outcome numbers / N2 | 1.6 | Added 2026-10-09 at Dana's request after Gate 3. Reopened Gate 1. |
| C12 | There's a 14-day free trial on the Team plan, and it doesn't need a credit card. | SUPPORTED | canon/pricing-and-packaging.md | Trial | 4.0 | Added 2026-10-09 at Dana's request after Gate 3. Reopened Gate 1. |

## Refused sources

- `canon/retired/pricing-2025.md` (v3.1). Requested by Dana for the $250 figure. Status in SOURCES.yaml is `retired`, replaced by `pricing-2026`. Not used. Current figure offered as C7.

## Counts

Total: 12  Supported: 9  Unsupported: 3 (cut 3, soften 0, routed 0)

## Gate 1 decisions

**First pass.** Owner: Lena Voss (Security & Compliance; riskiest source is security-faq)  Decision: pass  Date: 2026-10-07  Reason: C1 through C3 match approved phrasing exactly. C5 and C8 correctly cut. Legal co-sign will be required at Gate 4 because security-faq is cited.

**Reopened.** Owner: Lena Voss  Decision: pass  Date: 2026-10-09  Reason: C11 and C12 added after Gate 3 passed on draft v2. Both verbatim from current canon. No security-faq change, so my earlier decision stands for C1 through C3.
