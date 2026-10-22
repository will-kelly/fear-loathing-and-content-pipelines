# Build an AI content pipeline with no code: the Claude Project / custom GPT version

*Companion tutorial to "Fear, Loathing, and AI Content Pipelines" — All Day AI, October 22, 2026. For the Python version, see [TUTORIAL.md](TUTORIAL.md).*

The talk's argument is that a prompt is not a pipeline. The difference isn't code. It's whether your sources are governed, your task has edges, a named person owns a gate, and somebody is measuring the work.

You can build all four of those inside a Claude Project or a custom GPT without writing a line of code. This tutorial shows you how. You'll end up with an agent that drafts one content type against sources you control, refuses to invent, and feeds a gate you can actually run.

Everything here uses features both products have had for a while: a persistent set of instructions, a place to upload reference files, and a chat. Menus move around, so I describe *what* to set up rather than *where to click*.

## What you're building

```
knowledge files   →   instructions   →   chat   →   gate   →   metrics sheet
(canonical source)   (bounded task)    (draft)   (human)    (spreadsheet)
```

| Part | Fixes | Where it lives |
|---|---|---|
| Canonical source | Fear (ungoverned sources) | Files uploaded to the project or GPT |
| Bounded task | Fear (unverifiable claims) | The project / GPT instructions |
| Explicit gate | Loathing (redundant review) | A one-page checklist and a named person |
| Metrics | Loathing (invisible work) | A five-column spreadsheet |

## Step 1: Pick one workflow

Pick the content type with the highest volume and the lowest approval friction. FAQ answers, release notes, policy section updates, a recurring internal update. Not the thing the CEO reads.

Open a blank doc and write three lines:

```
Workflow: Internal FAQ answers for the support team
Owner: Jordan (support content lead)
Current turnaround: unknown — measure it in step 6
```

If you can't put one name on the owner line, stop. Shared ownership is no ownership, and no agent configuration fixes that.

## Step 2: Build the canonical source

This is the step people skip, and it's the one that fixes fear.

For each topic the agent will draft about, you need **one** document. Not the wiki page *and* the PDF *and* the Slack thread. One. Before you upload anything, give each document a header at the top:

```
Title: Refund policy
Owner: Priya Shah
Version: 2026-10-14
Supersedes: 2026-03-02
```

Then upload those documents — and only those — as the project's knowledge files (Claude: Project knowledge; ChatGPT: the GPT's Knowledge files). The model will treat these as its reference material.

Three questions every source now answers:

1. **Where's the current version?** In the project. Nowhere else.
2. **Who owns it?** The name in the header.
3. **When did it last change?** The version date. When Priya updates the policy, she replaces the file. That's the whole versioning process.

The upload takes ten minutes. Deciding whose document wins takes longer. Have that argument before you upload, not after.

## Step 3: Write the bounded task as the instructions

The instructions field is where the pipeline actually lives. Paste this in and adapt the bracketed parts. It works as Claude Project instructions or as custom GPT instructions with minor wording changes.

```
You draft [internal FAQ answers] for [the support team at Company].

SOURCES
Use ONLY the documents in your knowledge files. Treat them as the sole
source of truth. Do not use general knowledge, prior training, or
anything the user pastes into chat unless they explicitly say it is a
new approved source.

CITATION
Every factual claim must be traceable to a specific knowledge file.
Cite it inline as [source: file title, version].

WHEN THE SOURCES DON'T COVER IT
If the knowledge files do not answer the question, or only partly
answer it, say so plainly and stop. Suggest the user ask [Jordan] or
the owner named in the relevant source. Do not fill gaps with plausible
text. "The sources don't cover this" is a correct answer.

UNSOURCED CLAIMS
If you cannot trace a claim to a source, write [NEEDS SOURCE] directly
before it. Never remove or soften this tag. Never rephrase a tagged
claim so it sounds more certain.

FORMAT
Plain, direct language that matches the register of the source
documents. No marketing language. Maximum [150] words.

WHAT A CORRECT OUTPUT LOOKS LIKE
Either a short answer where every claim is cited, or a clear statement
that the sources don't cover the question. Nothing in between.
```

Read the last block again. That's the test from the talk: you've described what correct looks like *before* the model runs. A bounded task fails by producing nothing or by saying the source doesn't cover it. An unbounded task fails by producing something plausible. You want the first kind of failure.

Save the instructions. Give the project or GPT a name that says what it does and doesn't do: "FAQ Drafter — support sources only."

## Step 4: Test it to failure

Before anyone else touches it, ask it three questions in chat:

1. A question the sources answer cleanly. You should get a short answer with a citation on every claim.
2. A question the sources *partly* answer. You should get the covered part cited and the rest either tagged `[NEEDS SOURCE]` or declined.
3. A question the sources don't answer at all. You should get a refusal and a referral to the owner.

If question 3 gets a confident, fluent answer anyway, the task isn't bounded tightly enough. Go back to the instructions and make the refusal rule harder to wriggle out of. Fluent and wrong clears every casual check a human runs on autopilot — that's exactly what you're testing for.

Keep the three test questions. Re-run them any time someone edits the instructions or swaps a source file.

## Step 5: Add one gate

The draft is a draft. It goes to one person before it's used anywhere. Write the gate on a single page, pin it in the team channel, and put the same text at the bottom of the instructions so the agent reminds the user:

```
GATE — FAQ answers
Owner: Jordan
Condition: Every claim traces to a cited source at the current version,
and zero [NEEDS SOURCE] tags remain.
Decision: PASS or RETURN. Nothing else.
Time budget: two minutes.

If a claim can't be traced, cut it or soften it. Unverifiable never
means false. It means it doesn't ship as a fact.
```

The reviewer opens the cited source, confirms it says what the draft says it says, and decides. That's the entire review. One person, one written condition, one decision.

If you have four people reading every draft right now, this is the moment to ask each of them what they're checking for. If two say "just making sure it's okay," you've found the redundant review the talk describes. Keep the one whose check is written down.

Legal and compliance don't need to trust the model. They need a named checkpoint with a record. The gate page plus the spreadsheet in the next step is that record.

## Step 6: Measure the pipeline with a spreadsheet

Make a sheet with these columns and have the gate owner fill in one row per draft:

| Draft | Requested | Gate decided | Decision | Revisions | Needs-source tags | Source found first try? |
|---|---|---|---|---|---|---|

That gives you the five numbers from the talk with no tooling at all:

1. **Turnaround time** — requested to shipped
2. **Approval latency** — requested to gate decided
3. **Revision count** — how many RETURNs before PASS
4. **Reuse rate** — how many drafts came from an existing source vs. needed a new one written
5. **Retrieval success** — did the agent cite the right source on the first try? This is the number to watch first.

Fill it in for two weeks before you change anything. If you don't baseline, you will never be able to say whether it worked.

A rising pass rate with a stable number of RETURNs is a working pipeline. A rising draft count with a falling pass rate is a team that automated its way into a review crisis.

Not on the sheet: how fast the model is, how many words it wrote, how many hours it "saved." Those tell you nothing about whether the content is any good.

## Claude Project vs. custom GPT: what's different

Not much, for this. Both give you instructions plus uploaded files plus chat, and that's all this pipeline needs. Two practical notes:

- **Sharing.** If the agent is shared with a team, the instructions and sources are shared too. That's good — it's the point — but it means the source owner needs to know that replacing a file replaces it for everyone. Treat it like editing the canonical doc, because it is.
- **Pasted content.** People will paste a Slack message into chat and ask the agent to use it. The instructions above tell the model to ignore that unless the user declares it an approved source. Hold that line. The moment pasted text counts as a source, you're back to a rumor with a URL.

## What this does and doesn't do

It will refuse questions your sources don't cover. It will tag claims it can't support. It will annoy people in week one and reassure them by week three.

It answers the question your team is really asking — *which half of my job is this taking?* — specifically: the agent drafts one bounded task against sources a named person owns, and a named person decides whether it ships. Nobody is replaced by a chat window with a file upload.

## Where to go next

After thirty clean days on one workflow:

- Add a second project or GPT for a second content type. Don't widen the first one. A bounded task stays bounded.
- Build a separate reviewer agent with its own instructions — one whose only job is to extract every claim from a draft and list the source for each. A model reviewing its own draft is a model agreeing with itself. A separate configuration with a hostile-reader brief is cheap and catches more.
- Move the kill decision to the front. Before anyone opens the drafter, ask whether this piece should exist. The agent can't answer that. That's the human layer, and it's the one that matters.

The model is the easy part. Everything in this tutorial is workflow design, and you can do all of it in a text box.

---

*Will Kelly · [linkedin.com/in/willkelly](https://linkedin.com/in/willkelly)*
