# How to write a source file

A source file is the only place the AI gets facts. That's a big job for a small file, so here's how to write one that holds up.

## The rules

1. **One owner, named at the top.** A file without an owner is a file nobody will fix when it's wrong. Put a real person's name there. "The marketing team" is not a person.
2. **A date.** "Last checked" tells the next reader whether to trust it. If the date is six months old, somebody should look at it.
3. **Say the approved wording.** Where exact wording matters (security claims, prices, customer quotes), write the sentence you want used and say "use this wording." The AI will.
4. **Say what not to say.** The "don't" lines are the most useful lines in the file. "Don't say SOC 2 certified" prevents a mistake that sounds right and isn't.
5. **Leave out what you're not sure of.** A missing fact gets a `[?]` tag and a question to the owner. A wrong fact gets published. Missing is better.

## What to do when a fact is missing

The AI will tell you: "The source file doesn't cover this." That's not the AI failing. That's the pipeline working. Three options:

- **Cut the claim.** Usually fine. Most drafts have one fact too many.
- **Ask the owner to add it.** Priya adds a line, bumps the version, updates the date. Now every future piece can use it.
- **Say it anyway.** Don't. If you want it in the piece, it goes in the source file first. That's the whole idea.

## Adding a second source file

You'll want to eventually. Before you do, ask: who owns it, and what happens when it disagrees with the first one? If you can't answer both, add a section to the existing file instead. When you have three files and the answer is still unclear, read [`../docs/graduating.md`](../docs/graduating.md).
