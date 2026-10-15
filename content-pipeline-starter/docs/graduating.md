# Graduating to the full pipeline

The full version is the [governed-content-pipeline](../../governed-content-pipeline) repo. Nothing in it is a different idea from what's here. Each piece just grew up.

| Starter kit | Full pipeline | What changed, and why |
|---|---|---|
| One source file with an owner at the top | `canon/` folder plus `SOURCES.yaml` registry | More than one source means you need a registry saying which file covers which topic, who owns each, what version it's on, and whether it's current or retired. The registry is the thing that lets the agent refuse an old pricing sheet. |
| Request form with a "Point" line | Gate 0: Intake, with a written brief | Same form, plus "what a correct output looks like" as three to five bullets, and a named owner who decides whether the task is bounded. |
| `[S]` and `[?]` tags in the draft | Gate 1: Sources, with a claims ledger built *before* the draft | The tags move out of the draft and into their own table, and the table gets built first. The draft is then written from the ledger, so nothing unsourced can get in. Also, "unsupported" gets three dispositions instead of one: cut, soften, or route to the owner. |
| The draft | Gate 2: Draft, with a claim map | Same thing, plus a named owner, and a rule that any edit reopens the gate. |
| Five-question checklist, one person | Gate 3: Review, two blind auditors plus one person | The checklist's questions 1 and 2 become a claims auditor. Question 4 and a style guide become a voice auditor. Both run in fresh contexts so the model isn't reviewing its own work. The person reads one table instead of the whole draft. |
| Question 5: "would you sign it" | Gate 4: Ship, with an archive record | Still one person signing. Plus a record of every source and version the piece used, so when a source changes you can find every piece it affects. No override at this gate; there's no override for owning something. |
| `log.md` table | `pipeline/log.jsonl` plus `scripts/metrics.py` | The table becomes one JSON line per gate decision instead of one row per piece. A script turns it into five numbers: turnaround, approval latency per gate, gate pass rate, reuse rate, retrieval success. |
| "Any edit after the checklist means it runs again" | "A change after a gate reopens that gate" | Same rule, applied at every gate. |
| (nothing) | Logged overrides | The full pipeline lets an owner override a failed gate, as long as the override is in the log with their name and reason. The one thing the agent refuses is an unlogged override. The starter kit doesn't have this because with one gate and one person, an override is just "no." |

## How to know it's time

You don't graduate because the starter kit is bad. You graduate because one of these is true:

- **More than one person asks "which file is right?"** You need the registry.
- **The checker is reading whole drafts and it's taking twenty minutes.** You need the auditors.
- **Someone asked how long a piece sits waiting, and the log can't say.** You need per-gate timestamps.
- **A source changed and you can't find the pieces it affects.** You need the archive record.
- **Someone edited after the checklist and nobody noticed for a week.** You need the reopen rule enforced by the agent, not by memory.

## How to do it

Don't move everything at once. The full pipeline is built so each piece can be adopted alone:

1. Move your source file into `canon/` and write a one-row `SOURCES.yaml`. Done; now you have a registry.
2. Keep your checklist. Add `gates/gate-0-intake.md` as the only gate. Now your request form has an owner.
3. When the checker is tired, add the claims auditor. Just that one. It replaces checklist questions 1 and 2.
4. When you want numbers, switch the log to JSON lines and run the script.

Each step is a week of using it before the next one. The talk's Monday advice applies at every step: name the source, bound the task, add one gate, baseline before you change anything else.
