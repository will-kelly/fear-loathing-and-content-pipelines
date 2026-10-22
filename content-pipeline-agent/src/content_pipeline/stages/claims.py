"""Stage 2 - Claims. Build the evidence ledger before a word of prose exists.

Why this stage exists: an LLM asked to "write a post about X" invents
statistics with total confidence. Separating *what we are willing to
assert* from *how we say it* means the drafter can only use claims the
ledger already holds, and every fact carries a confidence tier and a
source the reviewer can check.

With ``--web-search`` the model can use Anthropic's server-side search
tool; citations come back on the response and are merged into the ledger.
"""

from __future__ import annotations

from ..models import Brief, ClaimsLedger
from .base import RunContext, Stage, load_prompt, render


class ClaimsStage(Stage):
    name = "claims"

    def run(self, ctx: RunContext) -> ClaimsLedger:
        brief: Brief = ctx.artifacts["brief"]
        system = load_prompt("claims")
        user = render(
            "## Locked brief\n\n{{brief}}\n\n"
            "## Search policy\n\n{{policy}}",
            brief=brief.raw,
            policy=(
                "Web search is ON. Verify checkable facts; cite the URL for each."
                if ctx.config.web_search
                else "Web search is OFF. Mark any fact you cannot source from the brief or "
                "the writer's own material as SIGNAL or UNSUPPORTED; never fabricate a source."
            ),
        )
        result = ctx.client.complete(
            stage=self.name,
            system=system,
            user=user,
            max_tokens=ctx.config.max_tokens,
            temperature=0.2,  # low: this stage is bookkeeping, not prose
            web_search=ctx.config.web_search,
            web_search_max_uses=ctx.config.web_search_max_uses,
        )
        data = result.json()

        # Fold API-level citations into the ledger as a sidecar so nothing the
        # model saw is lost even if it forgot to list a source.
        if result.citations:
            data.setdefault("search_citations", [
                {"url": c.url, "title": c.title, "cited_text": c.cited_text}
                for c in result.citations
            ])

        ledger = ClaimsLedger.from_dict(data)
        ctx.record(self.name, result, note=f"{len(ledger.claims)} claims, {len(ledger.gaps)} gaps")
        ctx.write("02_claims.json", ledger.raw)
        ctx.artifacts["ledger"] = ledger
        return ledger
