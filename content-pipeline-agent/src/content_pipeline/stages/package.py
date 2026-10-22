"""Stage 5 - Package. Reviewed draft -> everything needed to publish.

Final tightening pass, headline options, a dek, channel-native cuts (not
truncations: each cut is rebuilt from the sub-argument that fits that
channel), SEO/AEO metadata, and a changelog of what this stage changed.
"""

from __future__ import annotations

from ..models import Brief, ClaimsLedger, Draft, Package, Review
from .base import RunContext, Stage, load_prompt, render


class PackageStage(Stage):
    name = "package"

    def run(self, ctx: RunContext) -> Package:
        brief: Brief = ctx.artifacts["brief"]
        ledger: ClaimsLedger = ctx.artifacts["ledger"]
        draft: Draft = ctx.artifacts["draft"]
        review: Review = ctx.artifacts["review"]
        cfg = ctx.config

        system = load_prompt("package")
        user = render(
            "## Brief\n\n{{brief}}\n\n"
            "## Reviewed draft (verdict {{verdict}}, score {{score}}/10)\n\n# {{title}}\n\n{{body}}\n\n"
            "## Remaining WARN findings to respect\n\n{{warns}}\n\n"
            "## Claims ledger (for source lists and the AEO answer block)\n\n{{ledger}}\n\n"
            "## Channels to cut\n\n{{channels}}\n\n"
            "## Voice guide\n\n{{voice}}",
            brief=brief.raw,
            verdict=review.verdict,
            score=str(review.score),
            title=draft.title,
            body=draft.body_markdown,
            warns=[f.__dict__ for f in review.findings if f.verdict == "WARN"],
            ledger=ledger.raw,
            channels=cfg.channels,
            voice=cfg.voice_text(),
        )
        result = ctx.client.complete(
            stage=self.name,
            system=system,
            user=user,
            max_tokens=cfg.max_tokens,
            temperature=cfg.temperature,
        )
        pkg = Package.from_dict(result.json())
        ctx.record(self.name, result, note=f"{len(pkg.channel_cuts)} channel cuts")

        ctx.write("05_package.json", pkg.raw)
        ctx.write("05_final.md", pkg.final_markdown)
        for channel, text in pkg.channel_cuts.items():
            ctx.write(f"05_cut_{channel}.md", text)

        # Sources appendix: every claim the draft used that has a URL.
        used = ledger.by_id()
        lines = ["# Sources\n"]
        for cid in draft.claims_used:
            c = used.get(cid)
            if not c:
                continue
            for s in c.sources:
                if s.get("url"):
                    lines.append(f"- [{c.id}] {s.get('title') or s['url']} — {s['url']}")
        if len(lines) > 1:
            ctx.write("05_sources.md", "\n".join(lines) + "\n")

        ctx.artifacts["package"] = pkg
        return pkg
