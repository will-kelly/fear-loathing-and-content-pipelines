# Raw notes: the copilot that answered from the wrong runbook

Voice memo transcript, lightly cleaned up. Channel: newsletter. Register: field note with an argument.

Okay so the thing I keep running into. Client last quarter, mid-size SaaS, maybe 400 people. They'd rolled out an internal copilot over their Confluence. Leadership was excited, demo went great. Three weeks in, a support engineer asks it how to rotate a customer's API key and it walks him through the procedure from the 2022 runbook. The one that was superseded when they moved to the new auth service. Nobody had deleted the old page. Nobody had marked it stale. Both pages were titled almost the same thing.

That's not an AI problem. That's a documentation problem that the AI made visible.

I did a quick audit for them after. Pulled 1,100 or so pages from the space the copilot was indexing. Rough numbers: about a third hadn't been touched in over two years. Something like 140 pages had a near-duplicate with conflicting instructions. Maybe 60 had an owner who no longer worked there.

The pattern I see over and over: AI readiness programs inventory models, vendors, and use cases. They almost never inventory the corpus the model is going to read. The readiness assessment has a slide about data quality and it means structured data, the warehouse, not the wiki.

The idea I want to land: there's a difference between documentation that's good enough for a human and documentation that's good enough for a retrieval system. A human reads the page title, sees "2022" in the breadcrumb, notices the author left, and quietly discounts it. The retriever doesn't have any of that context. It sees two chunks with high cosine similarity and picks one.

I've been calling this the "quiet discount" — all the invisible filtering humans do on stale docs that the model can't do. Could be the framework. Or something like "readiness for a reader vs readiness for a retriever."

What should people actually do? Before pointing a copilot at a space, do three things: find the pages with no owner, find the near-duplicates, find anything nobody has opened in a year. Fix or archive. It's not glamorous. It's a few days of work and it would have prevented the key rotation thing.

Don't want to do the "AI will replace technical writers" thing. Don't want to do a vendor comparison either.

Audience: the person who owns the internal AI rollout and is about to get blamed for the wiki.
