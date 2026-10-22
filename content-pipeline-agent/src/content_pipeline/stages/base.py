"""Shared plumbing for stages."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..config import PROMPTS_DIR, PipelineConfig
from ..llm import LLMClient, LLMResult


@dataclass
class RunContext:
    """Everything a stage needs, plus the artifacts produced so far."""

    config: PipelineConfig
    client: LLMClient
    run_dir: Path
    artifacts: dict[str, Any] = field(default_factory=dict)
    log: list[dict[str, Any]] = field(default_factory=list)

    def write(self, name: str, content: str | dict | list) -> Path:
        """Persist an artifact. JSON for dicts/lists, raw text otherwise."""
        self.run_dir.mkdir(parents=True, exist_ok=True)
        path = self.run_dir / name
        if isinstance(content, (dict, list)):
            path.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def record(self, stage: str, result: LLMResult, note: str = "") -> None:
        self.log.append(
            {
                "stage": stage,
                "usage": result.usage,
                "searches": result.searches,
                "citations": len(result.citations),
                "note": note,
            }
        )


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def render(template: str, **vars: Any) -> str:
    """Minimal ``{{var}}`` substitution. No logic, on purpose."""
    out = template
    for k, v in vars.items():
        out = out.replace("{{" + k + "}}", v if isinstance(v, str) else json.dumps(v, indent=2))
    return out


class Stage:
    name: str = "base"

    def run(self, ctx: RunContext) -> Any:  # pragma: no cover - interface
        raise NotImplementedError
