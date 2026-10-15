# Gate 0: intake

**Question this gate answers:** Is the task bounded?

## Condition

The brief states, in writing, what a correct output looks like: channel, audience, length, thesis, the claims that must appear, the claims that must not appear, and the canon sources the piece will draw from. A reader who has never seen the request could tell a correct draft from an incorrect one using the brief alone.

## Owner

Priya Raman (Product Marketing). Backup: Will Kelly (Content).

## Evidence the agent presents

- `pipeline/briefs/<slug>.md`
- The list of `SOURCES.yaml` entries the brief depends on, with their status.

## Fails when

- The thesis is a topic, not a claim ("something about SOC 2").
- The required claims include a fact with no current canon source.
- The channel's length and format rules from `style-guide.md` aren't carried into the brief.
- The request asks for a source that is retired or draft.

## Reopens when

The brief changes for any reason. A new required claim, a different channel, a different audience: back to Gate 0.

## Override

The owner may pass an incomplete brief. Log it. The usual reason is "we'll fill in the source at Gate 1," and the usual result is a Gate 1 fail.
