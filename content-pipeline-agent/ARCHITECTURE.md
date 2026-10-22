# Architecture notes

What the pipeline does is in the README. This file is about why it's shaped the way it is, what I'd defend, and what I'd change.

## The one decision everything else follows from

**Claims before prose.** Stage 2 exists so that Stage 3 is forbidden from inventing. Every other design choice (the typed ledger, `claims_used` on the draft, lint checking id coverage, the reviewer's `claims_fidelity` check, the package stage's closed ledger) is enforcement of that single rule at a different point in the flow.

I tried the obvious alternative first: one big prompt with "do not fabricate" in it. It works until the model needs a number it doesn't have, and then it produces one. Splitting the work so the drafter literally cannot see anything but the ledger is the version that held up.

## Stage contracts, not conversation

Stages don't share a chat history. Each one gets a fresh system prompt and a user message assembled from the artifacts on disk. Three reasons:

1. **The reviewer has to be blind.** If it sat in the same context as the drafter, it would grade the writer's intent instead of the page. It gets the thesis, the draft, the ledger, and the voice guide. Not the brief's rationale, not the drafter's `notes_to_editor`.
2. **Every stage is independently re-runnable.** A bad package doesn't mean re-drafting. Point the package stage at the saved `03_draft` and `04_review` and go.
3. **Context stays small.** Five short focused prompts beat one long one that has to carry everything.

The cost is that nothing "remembers" across stages except what was written to disk. That turned out to be a feature. If the artifact doesn't say it, the next stage doesn't know it, which is exactly the discipline I want.

## Two-layer review

Lint runs first and is deterministic: word count, claim ids resolve, no UNSUPPORTED claims used, framework claim present, placeholder count, banned phrases. It costs nothing and it never has a bad day.

The model reviewer runs second and is told what lint already checked, so it spends its attention on the things only a reader can judge: is the thesis delivered, does the framework carry weight or decorate, are the anchors doing the work, does the ending pay off.

Lint has a veto. The model can score a draft 9/10 and the run still fails if lint found a banned phrase. I'd rather over-fail on something checkable than let a fluent draft through on charm.

## The loop is bounded on purpose

`max_revision_passes` defaults to 2. After that the run stops with `passed: false`, every artifact on disk, and a summary that says where it stopped. An unbounded loop with a model that occasionally fails the same check the same way is a bill, not a pipeline.

The revision prompt is the draft prompt plus the previous draft plus the FAIL/WARN findings. "Fix every FAIL without introducing new claims." It does not get to re-read the raw input, so it can't go find new material to fix a problem; it has to fix it with what the ledger holds.

## Why the fixture client is a first-class citizen

`FixtureClient` is not a test double I bolted on. It is the `--dry-run` mode, it is how CI runs, and it is how someone evaluating this repo can see every stage's output without spending money. Any new stage has to ship with a fixture or dry runs break, which keeps the fixtures honest.

The fixtures are also the only place a reader can see what "good" looks like for each stage. The prompts describe the shape; the fixtures show it filled in.

## Things I'd defend if asked

- **JSON out of every stage, markdown inside the JSON for prose.** Structured enough to validate, loose enough to write in. `extract_json` tolerates fences and trailing commentary because models add both.
- **Strict required fields, loose extras.** `models.py` fails hard on a missing `thesis` and ignores a field it doesn't know. Prompts can grow without a migration.
- **The `gaps` list.** The claims stage telling the writer "you owe me a number for how long the audit took" is more useful than any amount of prose. It's the pipeline admitting what it can't do.
- **Placeholders as success.** `[PLACEHOLDER: …]` in a draft is the drafter doing its job. The alternative is a plausible detail that isn't true.

## What I'd change next

- **Parallel blind reviewers.** Right now one model reviewer covers claims, structure, and voice. Splitting it into two (a claims auditor and a voice auditor, each in a fresh context) and merging findings is the version I run for my own writing. It's cleaner and catches more; it's also twice the review cost.
- **Web fetch for anchors.** When the brief includes a URL, the claims stage should fetch it rather than rely on search.
- **Prompt caching on the voice guide and ledger.** Both are resent to several stages. Cache control on those blocks would cut input cost on long runs.
- **Streaming the draft stage.** The one place a human is actually waiting.
- **A `resume` command.** The artifacts are already there; the CLI just doesn't have a verb for "start from stage 4."
- **Structured outputs.** The JSON contract is enforced in code after the fact. A schema-constrained response would move that enforcement to the API.

## What this is not

It is not a general agent framework. There is no tool loop, no planner, no memory. It is a fixed five-stage pipeline with one bounded loop in the middle, because that is the shape editorial work actually has. Most of the content pipelines I see fail because they were built as agents when they should have been built as assembly lines.
