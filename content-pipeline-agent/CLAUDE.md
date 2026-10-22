# Working in this repo

- Python 3.10+, stdlib plus `anthropic`. Do not add dependencies without a reason in the PR.
- `pytest` must pass offline. Any new stage ships with a fixture in `src/content_pipeline/fixtures/` so `--dry-run` still runs end to end.
- Stages never import `anthropic`; they only see `LLMClient` from `llm.py`.
- Prompts live in `src/content_pipeline/prompts/<stage>.md`. Change the prompt and the contract in `models.py` together.
- Banned phrases are a style policy in `stages/review.py`, not a model concern. Edit the list, don't prompt around it.
- Keep `examples/runs/documentation-debt/` regenerated from `--dry-run` after fixture changes:
  `content-pipeline run examples/briefs/documentation-debt.md --dry-run --runs-dir examples/runs --name documentation-debt`
