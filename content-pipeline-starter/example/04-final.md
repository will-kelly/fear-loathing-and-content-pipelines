# What shipped

Tags stripped. This is the text that went on LinkedIn.

---

Our SOC 2 Type II report is done.

Kestrel is SOC 2 Type II audited for Security, Availability, and Confidentiality. The report is available under NDA.

Here's why that matters if you're the one running a security review. A questionnaire is a list of questions somebody answers from memory. A report is a list of controls somebody else tested. If you're evaluating Kestrel, your review can start from the second thing.

One of our customers put it better than we can:

"Our last audit took three weeks of reconstruction. This one took an afternoon." — Ingrid Solheim, Head of Platform Engineering, Halvard Logistics

If you want the report, ask. Link in the first comment.

---

## And the log row

| Piece | Channel | Requested | Shipped | Rounds | Approved by | Source version | Notes |
|---|---|---|---|---|---|---|---|
| kestrel-soc2-linkedin | LinkedIn | 2026-10-06 | 2026-10-08 | 2 | Priya Raman | 1 | Round 1 had a [?] (ISO 27001), cut. |

## What to notice

Three things happened here that wouldn't have happened without the pipeline:

1. **"Certified" never made it into a draft.** The source file said not to, so the AI never wrote it. Nobody had to catch it.
2. **The ISO line was visible.** The AI wrote it (Dana asked for it) but tagged it `[?]` and recommended cutting. A model without the tag rule would have slipped it in and it would have read fine.
3. **Priya's name is on it.** If the audit period turns out to be wrong, or the quote expires, the log says who approved it and which version of the source they approved it against.

None of that is the model being smart. It's a source file with "don't" lines, a tag rule, and a table.
