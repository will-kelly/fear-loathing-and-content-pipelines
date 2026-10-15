# Review: kestrel-soc2-linkedin

Draft: examples/kestrel-launch-post/draft.md (version 3; versions 1 and 2 audited first)

## Check table (final, version 3)

| Check | Result | Note |
|---|---|---|
| Sources current | PASS | security-faq 2.4, customer-proof 1.6, product-overview 3.2, pricing-2026 4.0 all `current` |
| Claims match sources | PASS | After round 1 fix to C9; C7, C11, C12 verified round 3 |
| Qualifiers present | PASS | "Customers we surveyed" restored |
| Voice | PASS | |
| Banned words and patterns | PASS | After round 1 fixes ("seamless", triplet) |
| Channel format | **FAIL → overridden** | 206 words against 200. Gate 2 override by Will Kelly, Gate 3 override by Priya Raman. Both logged. |

---

## Claims auditor report, round 1 (verbatim)

```
# Claims audit: examples/kestrel-launch-post/draft.md (version 1)

Verdict: FAIL

| # | Draft sentence | Ledger row | Verdict | Source says | Note |
|---|---|---|---|---|---|
| 1 | Kestrel is SOC 2 Type II audited for Security, Availability, and Confidentiality. | C1 | SUPPORTED | Identical to approved phrasing, security-faq.md v2.4 §Certifications | |
| 2 | The audit covered April 1, 2025 through March 31, 2026 | C2 | SUPPORTED | "for the period of April 1, 2025 to March 31, 2026" | "through" vs "to": same meaning |
| 3 | the report is available to customers and prospects under NDA | C3 | SUPPORTED | Identical | |
| 4 | "Before Kestrel our change history..." + attribution | C4 | SUPPORTED | Verbatim match, customer-proof.md v1.6 §Q1. Channel LinkedIn approved. Not expired. | |
| 5 | Kestrel answers who changed what, and who said they could. | C10 | SUPPORTED | Identical, product-overview.md v3.2 §Positioning line | |
| 6 | Customers cut audit prep from 9 days to under 2. | C9 | MISMATCH | "Customers we surveyed cut median audit prep time from 9 days to 1.5 days." Qualifier "customers we surveyed" is required per §N1. "Under 2" is a rounding of 1.5. "Median" dropped. | Fixable in draft |
| 7 | it was seamless | none | — | Not a checkable claim. Out of scope for me; flagging for voice. | |

## Unsupported (must route back to sources)
None.

## Mismatches (fixable in draft, reopens Gate 2)
Row 6. Replace with the approved phrasing from C9 exactly.
```

## Voice auditor report, round 1 (verbatim)

```
# Voice audit: examples/kestrel-launch-post/draft.md (version 1)

Verdict: FAIL

Overall read: Mostly sounds like a person. Two sentences sound like a landing page, and they're the first and the eighth, which is where readers decide.

| # | Severity | Location | Finding | Why the guide cares | Suggested fix (optional) |
|---|---|---|---|---|---|
| 1 | FAIL | Sentence 1, "and it was seamless" | Banned word: seamless | On the banned list. Also, an audit being "seamless" is a claim about the audit that nothing supports and nobody asked for. | Cut the clause. "Our SOC 2 Type II report is done." is stronger alone. |
| 2 | FAIL | Paragraph 3, "Faster, cleaner, calmer." | Banned pattern: triplet for rhythm | The guide bans triplets because they sound like a slogan and say nothing a reader can check. | Delete the sentence. The previous sentence already lands the point. |
| 3 | WARN | Paragraph 5, "Customers cut audit prep from 9 days to under 2." | Looks like a claims question (qualifier). | OUT OF SCOPE: claims auditor. Noting only. | |

Word count: 178 (range 120 to 200): PASS
Channel checks:
- No hashtags in body: PASS
- Link in first comment, not body: PASS ("Link in the first comment.")
- Sentence case: n/a, no headings
```

---

## Fix log

| Round | Finding | Action | Gates reopened | Re-audit result |
|---|---|---|---|---|
| 1 | Claims row 6 (MISMATCH, C9) | Replaced with ledger C9 text verbatim | Gate 2 (v1 → v2) | Claims auditor round 2: PASS |
| 1 | Voice row 1 (seamless) | Cut clause | Gate 2 (same reopening) | Voice auditor round 2: PASS |
| 1 | Voice row 2 (triplet) | Deleted sentence | Gate 2 (same reopening) | Voice auditor round 2: PASS |

Gate 2 re-run on version 2: pass, Will Kelly, 2026-10-08.

## Claims auditor report, round 2 (verbatim)

```
# Claims audit: examples/kestrel-launch-post/draft.md (version 2)
Verdict: PASS
Rows 1 through 5 unchanged from round 1. Row 6 now reads "Customers we surveyed cut median audit prep time from 9 days to 1.5 days." Identical to customer-proof.md v1.6 §N1 approved phrasing. SUPPORTED.
```

## Voice auditor report, round 2 (verbatim)

```
# Voice audit: examples/kestrel-launch-post/draft.md (version 2)
Verdict: PASS
Overall read: Sounds like an engineer. Opening line is now the strongest sentence in the piece.
No FAIL findings. Word count 166 (range 120 to 200): PASS. Channel checks: all PASS.
```

## Gate 3 decision (version 2)

Owner: Priya Raman  Decision: pass  Date: 2026-10-09  Reason: Both auditors PASS on v2. One round of fixes. The claims miss at Gate 2 was the kind the blind check exists for.

---

## Round 3: Gate 3 reopened by version 3

Dana Okafor asked for price, trial, and source coverage after Gate 3 passed. That added ledger rows C11 and C12 (Gate 1 reopened and re-passed), produced draft v3 (Gate 2 reopened; passed on override for length), and reopened this gate. Both auditors re-run blind on v3.

## Claims auditor report, round 3 (verbatim)

```
# Claims audit: examples/kestrel-launch-post/draft.md (version 3)
Verdict: PASS

Rows 1 through 6 unchanged from round 2. New rows:
| 7 | Most customers connect more than a dozen sources in their first two months. | C11 | SUPPORTED | Identical, customer-proof.md v1.6 §N2 approved phrasing | |
| 8 | Team plans start at $400 a month on an annual plan. | C7 | SUPPORTED | Approved phrasing is "Starts at $400 a month on an annual plan." Draft adds "Team plans," which §Plans supports. | |
| 9 | There's a 14-day free trial on the Team plan, and it doesn't need a credit card. | C12 | SUPPORTED | §Trial: "14-day free trial on the Team plan. No credit card required." Same meaning, no strengthening. | |
```

## Voice auditor report, round 3 (verbatim)

```
# Voice audit: examples/kestrel-launch-post/draft.md (version 3)
Verdict: FAIL

Overall read: Still sounds like a person. The new pricing paragraph reads like a different post stapled on, but the style guide doesn't have a rule for that, so it's a WARN.

| # | Severity | Location | Finding | Why the guide cares | Suggested fix (optional) |
|---|---|---|---|---|---|
| 1 | FAIL | Whole piece | 206 words, range is 120 to 200 | Channel table, LinkedIn post. Out of range is a FAIL. | Cut "on the Team plan" from the trial sentence (already said) and "to the people who run security reviews" from paragraph 3. That's 196. |
| 2 | WARN | Paragraph 6 | Pricing paragraph changes the subject from the audit to the sale | Guide says specific beats impressive; it doesn't say anything about focus. Noting it; not my call. | |

Word count: 206 (range 120 to 200): FAIL
Channel checks: hashtags PASS, link placement PASS
```

## Fix log, round 3

| Round | Finding | Action | Gates reopened | Re-audit result |
|---|---|---|---|---|
| 3 | Voice row 1 (length) | Not fixed. Owner override. | none | n/a |
| 3 | Voice row 2 (focus) | Accepted as WARN. | none | n/a |

## Gate 3 decision (version 3)

Owner: Priya Raman  Decision: **override**  Date: 2026-10-10  Reason: Length finding is correct and I'm overriding it. The voice auditor's suggested cuts are good and I'd take them on any other week, but Dana's three additions are what Sales asked for, every one of them is canon, and the claims auditor passed all three. Six words. Logged, and logged twice, which is the point of having two gates.

