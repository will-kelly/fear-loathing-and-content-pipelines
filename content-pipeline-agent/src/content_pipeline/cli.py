"""Command-line entry point.

    content-pipeline run examples/briefs/documentation-debt.md
    content-pipeline run brief.md --web-search --channels newsletter linkedin
    content-pipeline run brief.md --dry-run          # no API key needed
    content-pipeline lint runs/<run>/03_draft.r0.json # re-run the deterministic checks
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import PipelineConfig
from .models import ClaimsLedger, Draft
from .pipeline import Pipeline
from .stages import lint


def _read(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def cmd_run(args: argparse.Namespace) -> int:
    cfg = PipelineConfig(
        model=args.model or PipelineConfig().model,
        voice_path=Path(args.voice) if args.voice else None,
        web_search=args.web_search,
        dry_run=args.dry_run,
        min_words=args.min_words,
        max_words=args.max_words,
        min_review_score=args.min_score,
        max_revision_passes=args.max_revisions,
        channels=args.channels,
    )
    raw = _read(args.input)
    pipeline = Pipeline(cfg)
    print(f"[content-pipeline] model={cfg.model} dry_run={cfg.dry_run} web_search={cfg.web_search}", file=sys.stderr)
    run = pipeline.run(raw, runs_dir=args.runs_dir, run_name=args.name)
    print(run.summary())
    if run.ledger and run.ledger.gaps:
        print("\nThe writer still owes:")
        for g in run.ledger.gaps:
            print(f"  - {g}")
    if run.draft and run.draft.placeholders:
        print("\nPlaceholders left in the draft:")
        for p in run.draft.placeholders:
            print(f"  - {p}")
    return 0 if run.passed else 2


def cmd_lint(args: argparse.Namespace) -> int:
    draft_path = Path(args.draft)
    draft = Draft.from_dict(json.loads(draft_path.read_text(encoding="utf-8")))
    ledger_path = Path(args.ledger) if args.ledger else draft_path.parent / "02_claims.json"
    ledger = ClaimsLedger.from_dict(json.loads(ledger_path.read_text(encoding="utf-8")))
    res = lint(draft, ledger, args.min_words, args.max_words)
    for f in res["findings"]:
        print(f"{f.verdict:4}  {f.check:18} {f.detail}")
    print(f"\nlint: {'OK' if res['ok'] else 'FAIL'} ({res['word_count']} words)")
    return 0 if res["ok"] else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="content-pipeline", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Run the full pipeline on a brief or raw notes")
    r.add_argument("input", help="Path to a markdown/text file, or - for stdin")
    r.add_argument("--model", default=None, help="Claude model id (default: $CONTENT_PIPELINE_MODEL or claude-sonnet-5-5)")
    r.add_argument("--voice", default=None, help="Path to a voice guide markdown file (default: voice/default.md)")
    r.add_argument("--web-search", action="store_true", help="Let the claims stage use Anthropic's web search tool")
    r.add_argument("--dry-run", action="store_true", help="Use canned fixtures instead of the API")
    r.add_argument("--runs-dir", default="runs", help="Where to write run artifacts (default: runs/)")
    r.add_argument("--name", default=None, help="Run directory name (default: timestamp + slug)")
    r.add_argument("--channels", nargs="+", default=["newsletter", "linkedin", "exec_summary"])
    r.add_argument("--min-words", type=int, default=600)
    r.add_argument("--max-words", type=int, default=1600)
    r.add_argument("--min-score", type=int, default=7)
    r.add_argument("--max-revisions", type=int, default=2)
    r.set_defaults(func=cmd_run)

    l = sub.add_parser("lint", help="Run the deterministic review checks on a saved draft")
    l.add_argument("draft", help="Path to 03_draft.rN.json")
    l.add_argument("--ledger", default=None, help="Path to 02_claims.json (default: alongside the draft)")
    l.add_argument("--min-words", type=int, default=600)
    l.add_argument("--max-words", type=int, default=1600)
    l.set_defaults(func=cmd_lint)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
