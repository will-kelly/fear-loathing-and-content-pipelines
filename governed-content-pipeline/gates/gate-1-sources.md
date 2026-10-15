# Gate 1: sources

**Question this gate answers:** Does every claim have a source we can vouch for?

## Condition

Every checkable claim in the ledger is tied to one canon file, one section heading, and one version, and that source's status in `SOURCES.yaml` is `current`. Every claim that could not be tied to canon is marked `UNSUPPORTED` with a disposition: `cut`, `soften`, or `route to <owner>`. No claim is marked `SUPPORTED` by anything outside `canon/`.

## Owner

The topic owner named in `SOURCES.yaml` for the sources the piece relies on most. If a piece draws on more than one topic, the owner of the riskiest topic decides (security beats pricing beats product beats proof). Backup: the backup named for that source.

## Evidence the agent presents

- `pipeline/ledgers/<slug>.md`
- A count: claims total, supported, unsupported by disposition.
- Any source the request asked for that the agent refused, and why.

## Fails when

- A claim cites a retired or draft source.
- A claim cites a section heading that doesn't exist in the file.
- A claim is marked supported but the source says something weaker (the ledger says "SOC 2 certified," the source says "audited").
- An `UNSUPPORTED` claim has no disposition.
- A customer quote is paraphrased.

## Reopens when

The ledger changes. Adding a claim at draft time is a ledger change, which means Gate 1 runs again before Gate 2 can pass.

## Override

The owner may pass a ledger with an unsupported claim left in. Log it with the reason. The claims auditor at Gate 3 will flag the same claim again, by design. The override has to be logged twice to ship. That's intentional friction.
