# How this repo maps to the talk

"Fear, Loathing, and AI Content Pipelines," All Day AI, October 22, 2026. Through-line: the model is the easy part.

| Slide | Point | Where it lives in the repo |
|---|---|---|
| 2. Chain of custody | A document nobody owns is a liability with a filename. | `canon/SOURCES.yaml`: every source has a named owner and a backup. `examples/.../shipped/archive-record.yaml`: every shipped piece names the sources and versions it was built from. |
| 3. The tooling conversation | Draft in 9 seconds, review queue 11 days. | `scripts/metrics.py` approval latency by gate. The draft gate is not where the time goes. |
| 4. Two-axis frame | Fear from ungoverned sources and unbounded tasks; loathing from invisible decisions and unmeasured work. | Rules 1 and 2 in `CLAUDE.md` (fear). Rules 3 and 4 (loathing). |
| 5. Fear, itemized: ungoverned sources | Fluent and wrong passes every informal check. | `canon/retired/pricing-2025.md` is fluent, well-formatted, and wrong. The agent refuses it because the registry says so, not because the prose looks off. |
| 5. Fear: unverifiable claims | "The chatbot said it" was no defense. | `.claude/agents/claims-auditor.md`: three-state verdict per claim, quoting the source. `examples/.../review.md` round 1 catches a dropped qualifier and a rounded number. |
| 5. Fear: compliance exposure | Claims at speed, without the controls. | `canon/security-faq.md` approved phrasing. Gate 4 Legal co-sign when that file is cited. |
| 5. Loathing: approval queues | Afternoon of work, three weeks of waiting. | Gate owners are named in `gates/`. Anything outside a gate isn't a review. |
| 5. Loathing: redundant review | Anxiety with a calendar invite. | Two blind auditors replace four people at 45 minutes. One person reads one table at Gate 3. |
| 6. Deal Desk Assistant | "Not here, go ask a person." | `.claude/skills/sources/SKILL.md`: unsupported claims get `route to <owner>`. `CLAUDE.md`: that's a valid output. |
| 7. Throughline | A gate is a written condition, not a feeling. | `gates/README.md` and each `gate-N-*.md`. |
| 7. Bureau | Citation ledger before the draft. No invention. | `.claude/skills/sources/` runs before `.claude/skills/draft/`. The draft skill's inputs are the brief and ledger, nothing else. |
| 7. Citation Desk | A citation counts only once the source is opened. | Claims auditor opens the file, checks the section heading, checks version and status. |
| 7. Standards Desk | Diagnosis before revision. A model reviewing itself is agreeing with itself. | `.claude/agents/voice-auditor.md` diagnoses before suggesting. Both auditors run in fresh contexts with file paths, not the chat. |
| 7. The one gate you can't override | Overriding without the log recording it. | `CLAUDE.md` rule 3. `scripts/log_gate.py` refuses an override without a reason. The example run has two logged overrides for the same six words. |
| 8. Four antidotes | Canonical sources, bounded tasks, explicit gates, measure the pipeline. | The four rules in `CLAUDE.md` and the four columns of the README table. |
| 9. Gates and measurement | $300 a piece. Five numbers to track. | `scripts/metrics.py` prints exactly those five. |
| 9. A change after a gate reopens that gate | | `examples/.../draft.md` version 3: Dana's late request reopened Gates 1, 2, and 3. |
| 10. The part where I'm the one being automated | The first structural pass left. Knowing which argument is worth making stayed. | `.claude/skills/draft/SKILL.md`, last section. The thesis is decided at Gate 0 by a person; the model doesn't get to change it. |
| 11. Monday | Pick one workflow, name its source and owner, bound one task, add one gate, baseline first. | Start with `canon/SOURCES.yaml` (one row), `gates/gate-0-intake.md` (one gate), and `scripts/log_gate.py --gate request` (the baseline). |
