# Gate 3: review

**Question this gate answers:** Did both blind audits pass?

## Condition

The claims auditor and the voice auditor have each run in a fresh context that did not see the drafting conversation, and each has returned a verdict of `PASS`. Every finding they raised has been fixed and re-audited, or has been explicitly accepted by the owner with a reason.

## Owner

Priya Raman (Product Marketing). Backup: Will Kelly (Content).

## Evidence the agent presents

- `pipeline/reviews/<slug>.md`, containing both auditor reports verbatim and the fix log.
- A six-row check table: sources, claims, voice, banned words, channel format, qualifier presence. Each row `PASS` or `FAIL`.

## Why two auditors, and why blind

A model reviewing its own draft is agreeing with itself. The auditors get the draft file, the ledger file, and the canon. They do not get the chat where the draft was made, so they can't inherit its assumptions. The claims auditor checks facts against sources. The voice auditor checks the prose against `style-guide.md` and diagnoses before it rewrites.

## Fails when

- Either auditor returns `FAIL`.
- A finding was fixed without re-running that auditor.
- The agent summarized the draft to the auditors instead of handing them the file.

## Reopens when

The draft changes after this gate. Which also reopens Gate 2. Yes, really.

## Override

The owner may accept a voice finding they disagree with (the style guide isn't scripture). Log it with the reason. The owner may not override a claims finding of `UNSUPPORTED`; that routes back to the Gate 1 owner, because it's their source that's missing.
