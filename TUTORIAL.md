# Build an AI content pipeline in an afternoon

*Companion tutorial to "Fear, Loathing, and AI Content Pipelines" — All Day AI, October 22, 2026.*

The talk makes one argument: the model was never the bottleneck. A prompt is not a pipeline. What makes AI-assisted content trustworthy is the stuff wrapped around the model — governed sources, bounded tasks, explicit gates, and measurement.

This tutorial walks you through building the smallest version of that pipeline that actually works. You'll end up with a working script and three plain-text files you can run against one content type, with one owner, over thirty days. No transformation program. No new tool purchase.

## What you're building

```
canonical source  →  bounded task  →  draft  →  gate  →  metrics log
   (sources/)        (task.md)        (Claude)  (human)   (metrics.csv)
```

Four moving parts, mapped to the talk:

| Part | Fixes | Rule |
|---|---|---|
| Canonical source | Fear (ungoverned sources) | One versioned document per topic, with a named owner |
| Bounded task | Fear (unverifiable claims) | If you can't describe a correct output before the model runs, it isn't bounded |
| Explicit gate | Loathing (redundant review) | One person, one written condition, one decision |
| Metrics log | Loathing (invisible work) | Measure the pipeline, not the model |

## Prerequisites

- Python 3.10+
- An Anthropic API key in your environment as `ANTHROPIC_API_KEY`
- `pip install anthropic`

That's it. The point is that the tooling takes an afternoon. The conversations about whose document wins take longer — budget for that separately.

## Step 1: Pick one workflow

Pick the content type with the highest volume and the lowest approval friction. Release notes, internal FAQ answers, policy section updates, product one-pagers. Not the CEO's keynote.

Write it down at the top of a file called `WORKFLOW.md`:

```markdown
# Workflow: Internal FAQ answers for the support team

- Owner: Jordan (support content lead)
- Volume: ~15 answers/week
- Current turnaround: unknown — see step 5
```

If you can't fill in the owner line with one name, stop here. Shared ownership is no ownership.

## Step 2: Name the canonical source

Create a `sources/` folder. Put exactly one document per topic in it. Each file gets a header block:

```markdown
---
title: Refund policy
owner: Priya Shah
version: 2026-10-14
supersedes: 2026-03-02
---

Customers may request a full refund within 30 days of purchase...
```

Three questions this header answers, which the talk says every source has to answer:

1. **Where's the current version?** This file. Not the wiki page, not the Slack thread, not the PDF someone emailed.
2. **Who owns it?** One named person, accountable for accuracy and retirement.
3. **When did it last change?** The version date. If the model can't tell which version it drew from, neither can your reviewer.

The model will only ever see what's in this folder. Nothing else. That's the whole governance model, and it fits in a directory listing.

## Step 3: Bound the task

A bounded task fails by producing nothing or by saying "the source doesn't cover this." An unbounded task fails by producing something plausible. You want the first kind of failure.

Write the task in `task.md`:

```markdown
# Task: Draft one FAQ answer

Using ONLY the source documents provided, draft an answer to the customer
question below.

Rules:
- Every factual claim must be traceable to a specific source document.
  Cite it inline as [source: filename, version].
- If the sources do not answer the question, or only partly answer it,
  say so explicitly and stop. Do not fill gaps with general knowledge.
- Any claim you cannot trace to a source must carry a visible
  [NEEDS SOURCE] tag. Do not remove or soften the tag.
- Match the plain, direct register of the source documents. No
  marketing language.
- Maximum 150 words.

A correct output is: a short answer where every claim is cited, OR a
clear statement that the sources don't cover it.
```

Notice the last paragraph. That's the test from the talk: you've described what correct looks like *before* the model runs. You're trading ceiling for floor, on purpose.

## Step 4: Run the draft step

Save this as `pipeline.py`. It loads every source, loads the task, sends both to Claude, and writes the draft to `drafts/` with the sources it saw recorded alongside.

```python
"""Minimal governed AI content pipeline: draft step."""

import csv
import sys
from datetime import datetime
from pathlib import Path

import anthropic

SOURCES_DIR = Path("sources")
DRAFTS_DIR = Path("drafts")
TASK_FILE = Path("task.md")
METRICS_FILE = Path("metrics.csv")

MODEL = "claude-sonnet-5-5"  # swap for whatever your org has approved


def load_sources() -> str:
    """Concatenate every canonical source, filename and all, so the model
    can cite them. Only this folder is ever visible to the model."""
    parts = []
    for path in sorted(SOURCES_DIR.glob("*.md")):
        parts.append(f"=== SOURCE: {path.name} ===\n{path.read_text()}\n")
    if not parts:
        sys.exit("No sources found. A pipeline with no canonical source is a prompt.")
    return "\n".join(parts)


def draft(question: str) -> str:
    client = anthropic.Anthropic()
    task = TASK_FILE.read_text()
    sources = load_sources()

    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=task,
        messages=[
            {
                "role": "user",
                "content": f"{sources}\n\n=== QUESTION ===\n{question}",
            }
        ],
    )
    return response.content[0].text


def record_request(draft_id: str, question: str) -> None:
    """Log the request time so approval latency can be measured later."""
    new_file = not METRICS_FILE.exists()
    with METRICS_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(
                ["draft_id", "question", "requested_at", "gate_decided_at",
                 "decision", "revision_count", "needs_source_tags"]
            )
        writer.writerow([draft_id, question, datetime.now().isoformat(), "", "", "", ""])


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Usage: python pipeline.py "customer question here"')
    question = sys.argv[1]

    DRAFTS_DIR.mkdir(exist_ok=True)
    draft_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    text = draft(question)

    out = DRAFTS_DIR / f"{draft_id}.md"
    out.write_text(
        f"# Draft {draft_id}\n\n"
        f"**Question:** {question}\n\n"
        f"**Sources visible to model:** "
        f"{', '.join(p.name for p in sorted(SOURCES_DIR.glob('*.md')))}\n\n"
        f"---\n\n{text}\n"
    )
    record_request(draft_id, question)

    tags = text.count("[NEEDS SOURCE]")
    print(f"Draft written to {out}")
    print(f"[NEEDS SOURCE] tags: {tags}")
    if tags:
        print("Unsourced claims present. These must be resolved or cut at the gate.")


if __name__ == "__main__":
    main()
```

Run it:

```bash
python pipeline.py "Can I get a refund after 45 days?"
```

Try a question the sources *don't* answer. You want to see the model say so. If it confidently answers anyway, your task isn't bounded tightly enough — go back to `task.md` and make the rules harder to wriggle out of.

## Step 5: Add one gate

The draft now goes to one person. Not a committee. Not "whoever's around."

Create `GATE.md`:

```markdown
# Gate: FAQ answer

- Gate owner: Jordan
- Written condition: Every claim in the draft traces to a cited source
  at the current version, and there are zero [NEEDS SOURCE] tags remaining.
- Decision: PASS or RETURN. Nothing else.
- Time budget: two minutes per draft.

If a claim can't be traced, the reviewer cuts it or softens it. Unverifiable
never means false. It means it doesn't ship as a fact.
```

The condition has to be checkable in about two minutes. "Seems ready" is not a gate. "Looks good to me" is not a gate. A gate returns a verdict.

When Jordan decides, she fills in the row in `metrics.csv`: the decision time, PASS or RETURN, how many revisions it took, and how many tags were in the draft. A spreadsheet is fine. The point is the record exists.

If legal or compliance want visibility, this is what you give them: a named checkpoint where their question gets answered by a person, with a record. They don't need to trust the model. They need to trust Jordan and the log.

## Step 6: Baseline, then measure

Before you change anything else, run the pipeline for two weeks and look only at these numbers from `metrics.csv`:

1. **Turnaround time** — request to shipped
2. **Approval latency** — how long drafts sit at the gate
3. **Revision count** — passes before PASS
4. **Reuse rate** — how often the answer came from a canonical source vs. got written from scratch
5. **Retrieval success** — did the model pull the right source on the first try? Start here.

A rising gate-pass rate with a stable number of RETURNs is a working pipeline. A rising draft count with a falling pass rate means you automated your way into a review crisis.

Not on the list: benchmark scores, tokens per second, word count, "hours saved per draft." None of those tell you whether the content is any good.

## What this does and doesn't do

This is a floor, not a ceiling. It will not write your strategy. It will refuse questions your sources don't cover, which will feel limiting the first week and reassuring by the third.

It answers the question your team is actually asking — *which half of my job is this taking?* — with a specific answer: the model drafts one bounded task against sources you control. A human owns the source, a human owns the gate, a human decides what gets made in the first place. That's a case you can make to a nervous team, and it's a better case than optimism.

## Where to go next

Once one workflow runs clean for thirty days:

- Add a second gate only where risk actually lives (legal exposure, brand, factual accuracy). More review is not more quality.
- Split the review into separate passes — claim extraction, voice, a hostile-read — each with its own configuration. A model reviewing its own draft is a model agreeing with itself.
- Move the kill decision to the *front*: before drafting, decide whether this piece should exist at all.

The model is the easy part. Everything in this tutorial is workflow design, and it was workflow design before the model showed up.

---

*Will Kelly · [linkedin.com/in/willkelly](https://linkedin.com/in/willkelly)*
