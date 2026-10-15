# Governed content pipeline

A working example of a content pipeline where the model is the easy part.

This repo is the companion example for the talk **"Fear, Loathing, and AI Content Pipelines"** (All Day AI, October 22, 2026). It runs as a Claude Project or as a Claude Code project, and it is built around four rules:

| Antidote | What it means here |
|---|---|
| **Canonical sources** | The agent may only draw facts from `canon/`. Every source has a named owner, a version, and a status. Retired sources are refused. |
| **Bounded tasks** | Every piece starts with a brief that states what a correct output looks like. If the brief can't say that, the piece doesn't start. |
| **Explicit gates** | Five gates. Each has a written condition, a named owner with a backup, and one decision: pass or fail. A change after a gate reopens that gate. |
| **Measure the pipeline** | Every gate decision is logged. A script turns the log into the five numbers from the talk: turnaround time, approval latency, gate pass rate, reuse rate, and retrieval success. |

The one rule the human can't override: overriding a gate without the log recording it.

## The company in the examples

Everything here is about **Northfield Labs** and its product **Kestrel**, a fictional audit-log platform. The company, product, people, prices, and numbers are invented so the repo can be shown on a stage without exposing anyone's real sources. Swap `canon/` for your own and the pipeline doesn't care.

## How the pipeline runs

```
Request ──▶ Gate 0 ──▶ Gate 1 ──▶ Gate 2 ──▶ Gate 3 ──▶ Gate 4 ──▶ Shipped
           Intake     Sources    Draft      Review     Ship
           (brief)    (ledger)   (draft)    (audits)   (package)
```

1. **Intake.** A request becomes a brief: audience, channel, thesis, and a written description of a correct output. Gate 0 asks one question: is the task bounded?
2. **Sources.** Before any drafting, the agent builds a claims ledger. Every checkable fact is tied to a canon file, section, and version. Anything that isn't in canon is marked `UNSUPPORTED` and either cut or routed to a human. Gate 1 asks: does every claim have a source we can vouch for?
3. **Draft.** The agent writes only from the brief and the ledger. No new facts appear. Gate 2 asks: does the draft contain anything that isn't in the ledger?
4. **Review.** Two blind reviewers in fresh contexts (a claims auditor and a voice auditor) check the draft. A model reviewing its own draft is agreeing with itself, so the reviewers never see the drafting conversation. Gate 3 asks: did both audits pass?
5. **Ship.** The draft becomes a package with a changelog and an archive record. Gate 4 asks: does the human owner sign it?

Every gate decision, including overrides, goes to `pipeline/log.jsonl`. Run `python scripts/metrics.py` and you get the numbers.

## Run it as a Claude Project

1. Create a new Project in Claude.
2. Paste `project/system-prompt.md` into the project instructions.
3. Upload everything in `canon/` and `gates/` as project knowledge.
4. Start a chat with: *"New piece: a LinkedIn post announcing Kestrel's SOC 2 Type II report."*

The agent will walk the gates with you. It stops at each one and asks for a decision. Try asking it to quote a price from the 2025 pricing sheet and watch it refuse, because that source is marked retired in `canon/SOURCES.yaml`.

## Run it in Claude Code

```bash
git clone <this repo>
cd governed-content-pipeline
claude
```

Then: `/intake` to start a piece, `/sources` to build the ledger, `/draft`, `/review`, `/ship`. `CLAUDE.md` carries the operating rules; the skills in `.claude/skills/` carry each stage; the two reviewers in `.claude/agents/` run blind.

## See the numbers

```bash
python scripts/metrics.py
```

Reads `pipeline/log.jsonl` and prints the five numbers. The included log has one complete example run plus a few earlier pieces so the averages mean something. Add your own gate decisions with:

```bash
python scripts/log_gate.py --piece kestrel-soc2-post --gate 1 --decision pass --owner "Dana Okafor"
```

## Repo map

```
canon/                 Governed sources. One topic per file, owner and version in SOURCES.yaml.
gates/                 The five gates: condition, owner, backup, what reopens it.
.claude/skills/        One skill per stage (intake, sources, draft, review, ship).
.claude/agents/        The two blind reviewers.
project/               System prompt for running this as a Claude Project.
pipeline/              Working folders for briefs, ledgers, drafts, reviews, shipped pieces, and the gate log.
examples/              One complete run, start to finish, including a logged override.
scripts/               metrics.py (the five numbers) and log_gate.py (append a decision).
docs/talk-mapping.md   Which slide each part of this repo answers to.
```

## What to try on stage

See [`docs/demo-script.md`](docs/demo-script.md) for a five-minute walkthrough: a request, a refused source, a reopened gate, an override that lands in the log, and the metrics output.

## License

MIT. Take it, rename the company, and point it at your own canon.
