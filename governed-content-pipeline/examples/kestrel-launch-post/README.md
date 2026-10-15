# Example run: kestrel-soc2-linkedin

One piece, start to finish, with the parts that make the pipeline worth having:

- **A refused source.** The request asked for a $250 price from a retired sheet. See `brief.md`, "Notes from intake."
- **A refused phrase.** "Fully compliant" isn't approved phrasing in `security-faq.md`. Cut at the ledger.
- **A blind catch.** Draft v1 dropped a required qualifier and rounded 1.5 to "under 2." Gate 2 missed it. The claims auditor didn't. See `review.md`, round 1.
- **A reopen.** After Gate 3 passed, Sales asked for three more claims. Gates 1, 2, and 3 all reopened. See `draft.md`, "Why there is a version 3."
- **A logged override. Twice.** The final draft is six words over the channel cap. Will overrode Gate 2, the voice auditor flagged it again, Priya overrode Gate 3. Both are in `pipeline/log.jsonl`.
- **A signature.** `shipped/archive-record.yaml` names the owner, the Legal co-sign, and every source and version. When any of those sources changes, this is how the piece gets found.

Files:

```
brief.md                    Gate 0 artifact
ledger.md                   Gate 1 artifact (12 rows, two added at the reopen)
draft.md                    Gate 2 artifact, versions 3, 2, 1 top to bottom
review.md                   Gate 3 artifact, three audit rounds
shipped/final.md            What went out
shipped/ledger.md           Ledger as it stood at ship
shipped/changelog.md        Every change, the gate it reopened, who decided
shipped/archive-record.yaml Chain of custody
```
