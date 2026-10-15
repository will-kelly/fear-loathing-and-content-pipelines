# Five-minute demo script

For the talk, or for anyone who wants to see the pipeline refuse something. Works in Claude Code (preferred, the auditors run as real subagents) or in a Claude Project (the auditors run as fresh chats).

Everything below is rehearsable from the repo as shipped; nothing depends on live network access.

## 0. Before you start (30 seconds)

Have three things open: `canon/SOURCES.yaml`, `pipeline/log.jsonl`, and a terminal in the repo root. The audience should see the registry first. Point at the `pricing-2025` entry and its `status: retired`. That's the trap.

## 1. The request (1 minute)

In Claude Code, type:

> `/intake` New piece: a LinkedIn post announcing Kestrel's SOC 2. Say we're fully compliant, use the Halvard quote, and say pricing starts at $250.

What to point at when the brief comes back:

- It refused the $250. It names the retired source, names the replacement, and offers $400. It didn't argue; it checked the registry.
- It refused "fully compliant." Not because the model knows SOC 2 law, but because `security-faq.md` says the phrase isn't approved.
- It asks Priya for a Gate 0 decision and won't move until it gets one.

Say: *"Nothing here is a smarter model. It's a registry file with a status column."*

## 2. The ledger (1 minute)

> `/sources`

Point at:

- The claims it added that nobody asked for (the audit period, the NDA line), because a draft on this thesis would naturally say them, and it would rather have them in the ledger than discover them in the draft.
- The `UNSUPPORTED → cut` rows. Three of them. Each with a reason that quotes canon.
- The count line. "10 claims, 7 supported." That's a number, and it goes in the log.

Say: *"The ledger is built before the draft. The model is not allowed to find out what it wants to say and then look for sources."*

## 3. The reopen (1 minute)

Skip the live draft (it takes a minute and the audience has seen a model write a paragraph before). Open `examples/kestrel-launch-post/draft.md` and scroll to "Why there is a version 3."

Tell the story: Gate 3 passed on v2. Sales asked for the price, the trial, and one more number. Two of those weren't in the ledger. So the pipeline reopened Gate 1, then Gate 2, then Gate 3. Nobody got to "just add a sentence."

Say: *"A change after a gate reopens the gate. That's the sentence people hate most and it's the one that makes the review cost go away, because it means nobody has to re-read the whole piece to find out what changed."*

## 4. The override (1 minute)

Still in `draft.md`, point at the Gate 2 decision on v3: `override`. 206 words against a 200 cap. Then open `review.md`, round 3: the voice auditor flagged it again, and Priya overrode it again.

Then in the terminal:

```
grep override pipeline/log.jsonl
```

Two lines. Names, timestamps, reasons.

Then try to cheat:

```
python scripts/log_gate.py --piece demo --gate 2 --decision override --owner "Will Kelly"
```

It refuses. No reason, no override.

Say: *"I can override any gate but one. The one I can't override is overriding without the log recording it."*

## 5. The numbers (1 minute)

```
python scripts/metrics.py
```

Walk down the five numbers. Three things to point at:

- **Approval latency.** Intake is under an hour. Everything else is half a day to a day. The draft was never the constraint.
- **Gate pass rate.** Gate 4 is 100%. Say it out loud: *"A gate that never says no can go. Or it's the one gate that's doing its real job, which is making someone sign. I haven't decided. That's what the number is for."*
- **Retrieval success.** One failure. A shipped blog post says "40+" where canon says "42." Nobody would ever have found that without the spot-check. Now it's a filed v2.

Close: *"Pick one workflow. Name its source and its owner. Bound one task. Add one gate. Run the baseline before you change anything. That's Monday."*

## If something goes wrong on stage

The whole example run is in `examples/kestrel-launch-post/`. Every artifact the live demo would produce already exists there. Open the file instead of running the step, and keep talking.
