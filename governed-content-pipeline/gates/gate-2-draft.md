# Gate 2: draft

**Question this gate answers:** Does the draft say anything the ledger doesn't?

## Condition

Every factual statement in the draft maps to a `SUPPORTED` ledger entry. The draft meets the channel's length and format rules from the brief. No `UNSUPPORTED` claim with disposition `cut` appears in any form; every `soften` claim appears only in its softened form. Nothing is invented, including transitions that imply a fact ("as the industry leader in...").

## Owner

Will Kelly (Content). Backup: Priya Raman (Product Marketing).

## Evidence the agent presents

- `pipeline/drafts/<slug>.md`
- A claim map: each factual sentence in the draft, and the ledger entry it comes from.
- Word count against the brief's range.

## Fails when

- A sentence in the claim map has no ledger entry.
- A number appears without its required qualifier.
- Length is outside the brief's range.
- A customer quote differs from canon by a single word.

## Reopens when

The draft is edited. Any edit. A reviewer "just tightening a sentence" after Gate 2 has reopened Gate 2. The agent re-runs the claim map and asks for a new decision.

## Override

Rare. The usual reason is length ("it's 212 words, ship it"). Log it. The number isn't the point; the log is.
