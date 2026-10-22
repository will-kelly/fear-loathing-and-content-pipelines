"""Orchestrator. Runs the five stages in order with a fail-fix-recheck loop
between draft and review, and writes a run manifest at the end.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .llm import AnthropicClient, FixtureClient, LLMClient
from .models import Brief, ClaimsLedger, Draft, Package, Review
from .stages import ClaimsStage, DraftStage, IntakeStage, PackageStage, ReviewStage, RunContext


@dataclass
class PipelineRun:
    run_dir: Path
    brief: Brief | None = None
    ledger: ClaimsLedger | None = None
    draft: Draft | None = None
    review: Review | None = None
    package: Package | None = None
    passed: bool = False
    revisions: int = 0
    log: list[dict[str, Any]] = field(default_factory=list)
    seconds: float = 0.0

    def summary(self) -> str:
        lines = [f"run: {self.run_dir}"]
        if self.brief:
            lines.append(f"brief: {self.brief.working_title!r} -> {self.brief.channel}/{self.brief.register}")
        if self.ledger:
            lines.append(f"claims: {len(self.ledger.claims)} ({len(self.ledger.gaps)} gaps for the writer)")
        if self.draft:
            lines.append(f"draft: {self.draft.word_count} words, revision {self.draft.revision}")
        if self.review:
            fails = [f.check for f in self.review.failures()]
            lines.append(f"review: {self.review.verdict} score={self.review.score}/10 fails={fails or 'none'}")
        if self.package:
            lines.append(f"package: {len(self.package.channel_cuts)} channel cuts, {len(self.package.headline_options)} headlines")
        lines.append(f"status: {'PASSED' if self.passed else 'STOPPED AT REVIEW'} in {self.seconds:.1f}s")
        return "\n".join(lines)


def _slug(text: str, n: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:n] or "run"


class Pipeline:
    def __init__(self, config: PipelineConfig | None = None, client: LLMClient | None = None) -> None:
        self.config = config or PipelineConfig()
        if client is not None:
            self.client = client
        elif self.config.dry_run:
            self.client = FixtureClient()
        else:
            if not os.environ.get("ANTHROPIC_API_KEY"):
                raise RuntimeError(
                    "ANTHROPIC_API_KEY is not set. Export it, or pass --dry-run to use fixtures."
                )
            self.client = AnthropicClient(model=self.config.model)

    def run(self, raw_input: str, runs_dir: Path | str = "runs", run_name: str | None = None) -> PipelineRun:
        t0 = time.time()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        name = run_name or f"{stamp}-{_slug(raw_input.splitlines()[0] if raw_input.strip() else 'run')}"
        run_dir = Path(runs_dir) / name
        ctx = RunContext(config=self.config, client=self.client, run_dir=run_dir)
        ctx.write("00_input.md", raw_input)

        run = PipelineRun(run_dir=run_dir)

        # 1. Intake
        run.brief = IntakeStage(raw_input).run(ctx)

        # 2. Claims
        run.ledger = ClaimsStage().run(ctx)

        # 3 + 4. Draft, review, revise up to max_revision_passes times.
        drafter, reviewer = DraftStage(), ReviewStage()
        run.draft = drafter.run(ctx)
        run.review = reviewer.run(ctx)
        while run.review.verdict != "PASS" and run.revisions < self.config.max_revision_passes:
            run.revisions += 1
            run.draft = drafter.run(ctx, review=run.review)
            run.review = reviewer.run(ctx)

        run.passed = run.review.verdict == "PASS"

        # 5. Package only a passing draft. A failed run still leaves every
        #    artifact on disk so the writer can see exactly where it stopped.
        if run.passed:
            run.package = PackageStage().run(ctx)

        run.log = ctx.log
        run.seconds = time.time() - t0
        ctx.write(
            "manifest.json",
            {
                "run": name,
                "created_utc": stamp,
                "model": self.config.model,
                "dry_run": self.config.dry_run,
                "web_search": self.config.web_search,
                "passed": run.passed,
                "revisions": run.revisions,
                "seconds": round(run.seconds, 2),
                "stages": ctx.log,
                "gates": {
                    "min_words": self.config.min_words,
                    "max_words": self.config.max_words,
                    "min_review_score": self.config.min_review_score,
                    "max_revision_passes": self.config.max_revision_passes,
                },
            },
        )
        return run


def load_manifest(run_dir: Path | str) -> dict[str, Any]:
    return json.loads((Path(run_dir) / "manifest.json").read_text(encoding="utf-8"))
