# Content pipeline starter (Claude Code)

If you're running this in Claude Code instead of a Claude Project, the rules are the same. Read `project-instructions.md` and follow everything below its horizontal line. The source file is `sources/about-kestrel.md`; the gate is `checklist.md`; the log is `log.md`.

When the user says "new piece," run the three steps from `project-instructions.md`. Write drafts to `drafts/<piece-name>.md` using the layout in `templates/draft.md`. When the checklist comes back all yes, append the row to `log.md` yourself and tell the user you did.

No skills, no subagents, no scripts. Those are in the full pipeline. This one is markdown and a person.
