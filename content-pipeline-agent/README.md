# Content pipeline agent

A five-stage, claims-first editorial pipeline on the Claude API. Rough notes go in; a reviewed, publish-ready package comes out, with an evidence ledger and editorial gates in between.

```
intake ──▶ claims ──▶ draft ──▶ review ──▶ package
 brief     ledger     r0,r1…   lint+model   final + cuts
                        ▲          │
                        └── FAIL ──┘  (fail → fix → recheck, bounded)
```

Built by [Will Kelly](https://github.com/will-kelly) as a work sample. It is the engine behind the content pipelines I build for clients, stripped of anything client-specific and made to run on fixtures so you can see every stage without an API key.

## Why it's built this way

Ask a model to "write a post about X" and you get fluent prose with invented statistics. The fix isn't a better prompt. It's separating **what we're willing to assert** from **how we say it**, and putting a gate between the two.

So this pipeline:

- **Builds the claims ledger before any prose exists.** Every assertion gets a kind (observation, first-hand anchor, framework, checkable fact) and every fact gets a confidence tier (VERIFIED, CORROBORATED, SIGNAL, UNSUPPORTED). The drafter can only use what's in the ledger. If it needs something that isn't there, it writes a visible `[PLACEHOLDER]` instead of inventing a detail.
- **Reviews in two layers.** Deterministic lint runs first and is free: word count, claim-id coverage, no UNSUPPORTED claims used, framework present, banned-phrase list. Then a blind model reviewer that never saw the writer's notes grades the piece on authorship, not detection. Lint has a veto; the model can't pass a draft that lint failed.
- **Loops, but bounded.** A failed review goes back to the drafter with the findings attached. Two revision passes by default, then it stops and tells you where. A failed run leaves every artifact on disk.
- **Writes everything to disk between stages.** Each run is a directory of numbered files. You can diff `03_draft.r0.md` against `03_draft.r1.md` and see exactly what the review changed.
- **Rebuilds channel cuts instead of truncating.** The LinkedIn version is built from the sub-argument that fits LinkedIn, not the first 200 words of the newsletter.

## Try it in 60 seconds (no API key)

```bash
git clone https://github.com/will-kelly/content-pipeline-agent
cd content-pipeline-agent
pip install -e ".[dev]"

content-pipeline run examples/briefs/documentation-debt.md --dry-run
```

`--dry-run` serves canned responses from `src/content_pipeline/fixtures/`, so the full pipeline executes offline and you get a complete run directory under `runs/`. A finished example is checked in at [`examples/runs/documentation-debt/`](examples/runs/documentation-debt/).

```
run: runs/20261014-…-raw-notes-the-copilot-that-answered
brief: 'The quiet discount: why your copilot trusts the wrong runbook' -> newsletter/field-note with an argument
claims: 10 (3 gaps for the writer)
draft: 906 words, revision 0
review: PASS score=8/10 fails=none
package: 3 channel cuts, 5 headlines
status: PASSED in 0.0s

The writer still owes:
  - Confirm whether the audit figures in C3 can be printed as given…
  - Supply one sentence on what the client did after the audit…
  - If you want C10 in the piece, find a primary source; otherwise it stays out.
```

That last block is the point. The pipeline tells you what it couldn't support rather than papering over it.

## Run it for real

```bash
export ANTHROPIC_API_KEY=sk-ant-…
content-pipeline run my-notes.md
content-pipeline run my-notes.md --web-search          # claims stage can verify facts
content-pipeline run my-notes.md --voice voice/mine.md  # your voice guide
content-pipeline run my-notes.md --channels newsletter linkedin thread exec_summary
```

Model defaults to `claude-sonnet-5-5`; override with `--model` or `CONTENT_PIPELINE_MODEL`.

With `--web-search`, the claims stage gets Anthropic's server-side web search tool. Citations come back on the API response and are folded into the ledger as `search_citations`, so a source the model used but forgot to list is still on record.

Re-run just the deterministic checks on any saved draft:

```bash
content-pipeline lint runs/<run>/03_draft.r1.json
```

## What a run produces

| File | Stage | What it is |
|---|---|---|
| `00_input.md` | — | Your raw material, as given |
| `01_brief.json` | intake | Locked brief: thesis, audience, channel, register, anchors, open questions, non-goals |
| `02_claims.json` | claims | The ledger. Every claim typed and tiered; `gaps` lists what the writer still owes |
| `03_draft.rN.md` / `.json` | draft | One per revision pass. `claims_used` and `placeholders` are explicit |
| `04_review.rN.json` | review | Lint findings + model findings, merged verdict and score |
| `05_final.md` | package | Tightened piece |
| `05_cut_<channel>.md` | package | One file per channel |
| `05_package.json` | package | Headlines, dek, SEO/AEO metadata, changelog of what packaging changed |
| `05_sources.md` | package | Every URL behind a claim the draft used (only when sources exist) |
| `manifest.json` | — | Model, gates, token usage per stage, pass/fail, revisions |

## Layout

```
src/content_pipeline/
  cli.py          argparse entry point: run, lint
  pipeline.py     orchestrator and the fail-fix-recheck loop
  config.py       PipelineConfig: model, gates, channels, voice path
  llm.py          AnthropicClient (real) and FixtureClient (offline), JSON extraction
  models.py       stage contracts with strict required-field validation
  stages/         one module per stage; review.py holds the lint rules
  prompts/        one markdown system prompt per stage
  fixtures/       canned stage outputs for --dry-run and tests
voice/default.md  the voice guide injected into draft, review, and package
examples/         a sample brief and a complete checked-in run
tests/            22 tests, all offline
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the design decisions and the parts I'd change next.

## Adapting it

- **Voice.** Replace `voice/default.md` or pass `--voice`. The reviewer holds the draft to whatever is there.
- **Gates.** `--min-words`, `--max-words`, `--min-score`, `--max-revisions`. Banned phrases live at the top of `stages/review.py`.
- **Channels.** Any name works; conventions for the common ones are in `prompts/package.md`.
- **New stage.** Subclass `Stage`, write a prompt, add a contract in `models.py`, slot it into `Pipeline.run`. The fixture client needs a matching `fixtures/<stage>.json` for dry runs.
- **Different model vendor.** Implement the `LLMClient` protocol in `llm.py`. Stages never import `anthropic`.

## Tests

```bash
pytest
```

Everything runs offline. The API client is tested against stubbed responses, including `pause_turn` continuation for long search turns.

## License

MIT. See [LICENSE](LICENSE).
