"""Stage 3 - Draft. Brief + ledger + voice guide -> first full draft.

The drafter may only assert what the ledger holds. Anything it needs
and doesn't have becomes a visible ``[PLACEHOLDER: ...]`` instead of an
invented detail. ``claims_used`` lets the reviewer check coverage.

The same stage handles revision passes: when a review fails, it is rerun
with the findings appended, and the revision counter increments.
"""

from __future__ import annotations

from ..models import Brief, ClaimsLedger, Draft, Review
from .base import RunContext, Stage, load_prompt, render


class DraftStage(Stage):
    name = "draft"

    def run(self, ctx: RunContext, review: Review | None = None) -> Draft:
        brief: Brief = ctx.artifacts["brief"]
        ledger: ClaimsLedger = ctx.artifacts["ledger"]
        prior: Draft | None = ctx.artifacts.get("draft")
        revision = (prior.revision + 1) if (prior and review) else 0

        system = load_prompt("draft")
        parts = [
            "## Locked brief\n\n{{brief}}",
            "## Claims ledger\n\nYou may only assert what is here. "
            "Cite claims by id in `claims_used`.\n\n{{ledger}}",
            "## Voice guide\n\n{{voice}}",
            "## Length\n\nTarget {{min_words}}-{{max_words}} words in the body.",
        ]
        vars = dict(
            brief=brief.raw,
            ledger=ledger.raw,
            voice=ctx.config.voice_text(),
            min_words=str(ctx.config.min_words),
            max_words=str(ctx.config.max_words),
        )
        if prior and review:
            parts.append(
                "## Revision pass {{revision}}\n\nThe previous draft failed review. "
                "Fix every FAIL below without introducing new claims.\n\n"
                "### Previous draft\n\n{{prior}}\n\n### Review findings\n\n{{findings}}"
            )
            vars.update(
                revision=str(revision),
                prior=prior.body_markdown,
                findings=[f.__dict__ for f in review.findings if f.verdict in {"FAIL", "WARN"}],
            )

        result = ctx.client.complete(
            stage=self.name,
            system=system,
            user=render("\n\n".join(parts), **vars),
            max_tokens=ctx.config.max_tokens,
            temperature=ctx.config.temperature,
        )
        draft = Draft.from_dict(result.json(), revision=revision)
        ctx.record(self.name, result, note=f"revision {revision}, {draft.word_count} words")
        ctx.write(f"03_draft.r{revision}.json", draft.raw)
        ctx.write(f"03_draft.r{revision}.md", f"# {draft.title}\n\n{draft.body_markdown}")
        ctx.artifacts["draft"] = draft
        return draft
