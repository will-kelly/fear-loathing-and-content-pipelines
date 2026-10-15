---
id: product-overview
version: 3.2
owner: Priya Raman (Product Marketing)
status: current
last_reviewed: 2026-09-18
---

# Kestrel product overview

## What Kestrel is

Kestrel is an audit-log platform for engineering and security teams. It collects change events from infrastructure, CI/CD, identity providers, and SaaS admin consoles, normalizes them into one schema, and keeps them queryable for as long as the customer's retention policy requires.

## The problem it solves

Teams already have logs. What they don't have is one place where "who changed what, when, and who approved it" can be answered in under a minute. Kestrel's job is to make that question boring.

## Core capabilities

### Collection
- Native integrations with 42 sources as of September 2026, including GitHub, GitLab, AWS CloudTrail, Google Cloud Audit Logs, Okta, Entra ID, Terraform Cloud, and Salesforce.
- A generic webhook receiver for anything else.

### Normalization
- Every event is mapped to the Kestrel Event Schema (KES 2.0): actor, action, target, timestamp, approval chain, source.
- Field mapping is versioned. A mapping change is itself an audit event.

### Query
- Kestrel Query Language (KQL) for ad hoc questions.
- Saved views for recurring questions ("all production IAM changes without a linked ticket").
- Median query time on a 90-day window is under 2 seconds on the Team plan and above.

### Retention and export
- Retention is set per source, from 30 days to 7 years.
- Export to S3, GCS, or Azure Blob in Parquet or JSON Lines.
- Exports are themselves logged.

## What Kestrel is not

- Not a SIEM. Kestrel does not do threat detection or alert correlation. It integrates with Splunk, Datadog, and Elastic for that.
- Not a monitoring tool. No metrics, no uptime checks.
- Not an approval system. Kestrel records approvals that happened elsewhere; it doesn't grant them.

## Positioning line (approved)

"Kestrel answers who changed what, and who said they could."

## Who buys it

Platform engineering leads and security engineering leads at companies with 200 to 5,000 employees, usually in the run-up to a compliance audit or after an incident where change history was missing.
