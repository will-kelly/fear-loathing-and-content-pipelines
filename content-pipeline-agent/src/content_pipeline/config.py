"""Run configuration. Everything here can be set from the CLI or environment."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = PACKAGE_DIR / "prompts"
FIXTURES_DIR = PACKAGE_DIR / "fixtures"

DEFAULT_MODEL = os.environ.get("CONTENT_PIPELINE_MODEL", "claude-sonnet-5-5")


@dataclass
class PipelineConfig:
    """Knobs for a single pipeline run."""

    model: str = DEFAULT_MODEL
    max_tokens: int = 8000
    temperature: float = 0.4

    # Where the voice guide lives. Markdown; injected into draft/review prompts.
    voice_path: Path | None = None

    # Let the claims stage call Anthropic's server-side web search tool.
    web_search: bool = False
    web_search_max_uses: int = 6

    # Editorial gates. The review stage fails a draft that misses any of these.
    min_words: int = 600
    max_words: int = 1600
    min_review_score: int = 7  # out of 10
    max_revision_passes: int = 2

    # Dry-run: use canned fixture responses instead of calling the API.
    dry_run: bool = False

    # Channels to cut in the package stage.
    channels: list[str] = field(
        default_factory=lambda: ["newsletter", "linkedin", "exec_summary"]
    )

    def voice_text(self) -> str:
        if self.voice_path and Path(self.voice_path).exists():
            return Path(self.voice_path).read_text(encoding="utf-8")
        default = PACKAGE_DIR.parent.parent / "voice" / "default.md"
        if default.exists():
            return default.read_text(encoding="utf-8")
        return "Write plainly. Prefer evidence to adjectives. Avoid vendor-speak."
