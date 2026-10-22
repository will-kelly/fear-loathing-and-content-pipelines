# The quiet discount: why your copilot trusts the wrong runbook

Three weeks after a mid-size SaaS company pointed an internal copilot at its Confluence space, a support engineer asked it how to rotate a customer's API key. The copilot answered confidently, step by step, from the runbook. The 2022 runbook. The one that stopped being true when the company moved to a new auth service.

Nobody had deleted the old page. Nobody had marked it stale. It sat next to the current procedure with a title that differed by one word, and the copilot picked it.

Leadership's first reaction was that the AI had hallucinated. It hadn't. It had retrieved exactly what was there. The documentation problem had been sitting in that space for two years; the copilot just made it visible in a way a human reader never would have.

## What the audit found

I pulled roughly 1,100 pages from the space the copilot was indexing and ran a quick inventory. The numbers are approximate, but the shape is not.

About a third of the pages hadn't been touched in more than two years. Somewhere around 140 had a near-duplicate elsewhere in the space, and in most of those pairs the two pages disagreed about something that mattered: a port, a role name, a step that had been removed. Roughly 60 pages listed an owner who no longer worked at the company.

None of this was unusual. I've seen the same proportions in SharePoint tenants and Notion workspaces at companies half and twice this size. What was unusual was that someone had finally put a system in front of the wiki that had no idea which pages to ignore.

## The quiet discount

Here is the distinction I keep coming back to.

When a person opens a stale runbook, they apply a filter without noticing they're doing it. They see "2022" in the breadcrumb. They see that the author left last spring. They notice the product is called by its old name. They read the first two steps, feel something is off, and go ask someone. Every one of those cues shaves a little trust off the page, and by the time they've finished skimming it, they've discounted it to nearly zero.

I've started calling this the quiet discount. It is the invisible, cumulative skepticism a human reader applies to a page that is technically still there but practically dead. It happens so automatically that nobody counts it as work, which is why nobody budgets for replacing it.

A retrieval system can't apply it. From what I've watched these systems do, when two chunks look almost the same, the retriever has nothing to go on but the text, and the text of a superseded runbook is still perfectly good text. It comes back with full confidence because confidence was never the question. Relevance was, and the old page is relevant. It's just wrong.

So the distinction that matters is not "good documentation versus bad documentation." It's documentation that's ready for a reader versus documentation that's ready for a retriever. A human will quietly discount a stale page. The copilot will serve it.

## Where readiness programs look, and where they don't

This is the part that frustrates me, because it's fixable.

Every AI readiness assessment I've seen inventories the same things: which models, which vendors, which use cases, which teams. There's usually a slide on data quality. When you ask what it means, it means the warehouse. Structured data. Pipelines. Governance of tables.

The wiki doesn't make the deck. The corpus the copilot is going to read, the thing that will produce the first embarrassing answer, is treated as a given. It's already there, people already use it, so it must be fine.

It is fine. For people. People have the discount.

## Three checks before you index

What I'd do, and what I now ask clients to do before a copilot touches a space, is unglamorous:

1. **Find the pages with no current owner.** If the listed owner has left or the field is empty, the page has nobody who will notice it's wrong. Assign someone or archive it.
2. **Find the near-duplicates.** Pages with similar titles, pages copied and lightly edited, pages that both claim to be the procedure. Pick one. Delete or redirect the other. Do not leave both and hope the retriever picks well; it won't, because it isn't picking.
3. **Find anything nobody has opened in a year.** Not edited. Opened. A page no human has looked at in twelve months is a page no human has discounted either, which means the copilot will be the first reader it's had in a year.

Then fix or archive what those three checks turn up. That's it. On the client above it was a few days of work, most of it the dull kind, and it would have prevented the key rotation answer outright. [PLACEHOLDER: one sentence on what the client did after the audit, if shareable.]

You don't need a content strategy to do this. You don't need a taxonomy project. You need to accept that the quiet discount was doing a job, that the copilot can't do it, and that someone now has to do it on purpose, once, before the system goes live.

If you own the rollout, do it before the first bad answer rather than after. The wiki was always going to be the risk. The copilot just removed the thing that had been hiding it.
