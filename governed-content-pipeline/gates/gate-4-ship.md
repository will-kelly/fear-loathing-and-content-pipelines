# Gate 4: ship

**Question this gate answers:** Does a human own this?

## Condition

The package in `pipeline/shipped/<slug>/` contains the final text, the changelog from Gate 2 to now, the ledger it was built from, and an archive record naming the owner, the ship date, the channel, and every canon source and version used. The owner has read the final text, not the summary, and signs it. If the ledger touched `security-faq.md`, Legal has co-signed.

## Owner

Priya Raman (Product Marketing). Backup: Dana Okafor (Revenue Operations).
Co-sign when flagged: Tom Adeyemi (Legal).

## Evidence the agent presents

- The package folder.
- The final text, in full, in the conversation. Not a link. Not a summary.
- A list of every canon source and version in the archive record, so the owner can see what this piece will be wrong about if any of those files change.

## Fails when

- The archive record is missing a source the ledger used.
- A Legal co-sign is required and absent.
- The final text differs from the text that passed Gate 3.
- Nobody will put their name on it. That's not a process failure; that's the process working.

## Reopens when

Never, for this version. A shipped piece is immutable. If canon changes and the piece is now wrong, that's a new piece with a new slug that references this one. The archive record is how you find every shipped piece that cites a source you just retired.

## Override

None. This is the gate where a human says "I own this." There is no override for owning something.
