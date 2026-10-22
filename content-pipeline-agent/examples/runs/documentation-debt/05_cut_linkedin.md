A copilot told a support engineer how to rotate an API key using a runbook from 2022.

The runbook was wrong. It had been superseded when the company changed auth services. Nobody deleted it, nobody marked it stale, and its title was one word off from the current page.

Leadership called it a hallucination. It wasn't. The model retrieved exactly what was in the wiki.

Here's the thing nobody budgets for: when a person opens a stale page, they discount it without noticing. The old date in the breadcrumb, the author who left, the product's old name. By the time they finish skimming, they've trusted it at roughly zero. I call that the quiet discount.

A retrieval system can't do it. Two chunks that look the same are the same to it. The superseded page is still perfectly good text.

So "good documentation" isn't the bar anymore. The bar is: ready for a retriever, not just ready for a reader.

Before a copilot indexes a space, find the pages with no owner, the near-duplicates, and anything nobody has opened in a year. Fix or archive. It's a few days of dull work, and it would have prevented that answer.