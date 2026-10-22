"""Stage 1 - Intake. Raw material in, locked brief out.

The brief is the contract for everything downstream. If the thesis is
mushy here, no amount of drafting fixes it, so this stage is allowed to
push back: ``open_questions`` is where it says what it still needs.
"""

from __future__ import annotations

from ..models import Brief
from .base import RunContext, Stage, load_prompt, render


class IntakeStage(Stage):
    name = "intake"

    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input

    def run(self, ctx: RunContext) -> Brief:
        system = load_prompt("intake")
        user = render(
            "## Raw material\n\n{{raw}}\n\n## Voice guide (for register decisions)\n\n{{voice}}",
            raw=self.raw_input,
            voice=ctx.config.voice_text(),
        )
        result = ctx.client.complete(
            stage=self.name,
            system=system,
            user=user,
            max_tokens=ctx.config.max_tokens,
            temperature=ctx.config.temperature,
        )
        brief = Brief.from_dict(result.json())
        ctx.record(self.name, result)
        ctx.write("01_brief.json", brief.raw)
        ctx.artifacts["brief"] = brief
        return brief
