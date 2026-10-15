# Gates

A gate is a written condition, not a feeling.

Every gate in this folder has the same shape:

- **Condition.** A sentence that can be answered yes or no by looking at the artifact. If the owner has to "feel good about it," the condition isn't written well enough.
- **Owner and backup.** One named person decides. The backup decides when the owner is out. Nobody else's opinion is a gate.
- **Evidence.** What the agent puts in front of the owner.
- **Decision.** `pass` or `fail`. Nothing else. "Pass with comments" is a fail with a to-do list.
- **Reopens when.** A change after the gate reopens the gate and every gate after it.
- **Override.** The owner may override a fail. The agent proceeds only once the override is in `pipeline/log.jsonl` with the owner's name and reason.

Anything outside a gate stops being a review. If someone wants a say in a piece, they get a gate or they get nothing. That's not rudeness; it's how the $300-a-piece review cost goes away.

| Gate | Name | Artifact | Owner |
|---|---|---|---|
| 0 | [Intake](gate-0-intake.md) | Brief | Priya Raman |
| 1 | [Sources](gate-1-sources.md) | Claims ledger | Topic owner from `SOURCES.yaml` |
| 2 | [Draft](gate-2-draft.md) | Draft | Will Kelly |
| 3 | [Review](gate-3-review.md) | Review report | Priya Raman |
| 4 | [Ship](gate-4-ship.md) | Package | Priya Raman (+ Legal co-sign when flagged) |
