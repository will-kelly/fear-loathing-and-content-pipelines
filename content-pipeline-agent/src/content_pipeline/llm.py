"""Thin client layer over the Claude Messages API.

Two implementations share one interface:

* ``AnthropicClient`` -- the real thing. Handles the server-side web search
  tool, ``pause_turn`` continuation, and citation collection.
* ``FixtureClient`` -- returns canned responses from ``fixtures/`` so the
  pipeline runs end-to-end offline. Used by ``--dry-run`` and the test suite.

Stages never import ``anthropic`` directly; they only see ``LLMClient``.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .config import FIXTURES_DIR


@dataclass
class Citation:
    url: str
    title: str
    cited_text: str = ""


@dataclass
class LLMResult:
    text: str
    citations: list[Citation] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)
    searches: int = 0

    def json(self) -> Any:
        return extract_json(self.text)


class LLMClient(Protocol):
    def complete(
        self,
        *,
        stage: str,
        system: str,
        user: str,
        max_tokens: int,
        temperature: float,
        web_search: bool = False,
        web_search_max_uses: int = 5,
    ) -> LLMResult: ...


# --------------------------------------------------------------------------- #
# JSON extraction
# --------------------------------------------------------------------------- #

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def extract_json(text: str) -> Any:
    """Pull a JSON object or array out of model output.

    Tolerates a ```json fence, leading prose, and trailing commentary. Raises
    ``ValueError`` when nothing parseable is found, so a stage fails loudly
    instead of continuing with garbage.
    """
    candidates: list[str] = []
    for m in _FENCE.finditer(text):
        candidates.append(m.group(1))
    candidates.append(text)

    for cand in candidates:
        cand = cand.strip()
        try:
            return json.loads(cand)
        except json.JSONDecodeError:
            pass
        # Fall back to the outermost {...} or [...] span.
        for opener, closer in (("{", "}"), ("[", "]")):
            start, end = cand.find(opener), cand.rfind(closer)
            if start != -1 and end > start:
                try:
                    return json.loads(cand[start : end + 1])
                except json.JSONDecodeError:
                    continue
    raise ValueError("No JSON object found in model output:\n" + text[:500])


# --------------------------------------------------------------------------- #
# Real client
# --------------------------------------------------------------------------- #


class AnthropicClient:
    """Wraps ``anthropic.Anthropic().messages.create``.

    The import is deferred so the package loads in environments that only
    ever run ``--dry-run`` (CI, for example).
    """

    def __init__(self, model: str, api_key: str | None = None) -> None:
        import anthropic  # local import on purpose

        self._client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
        self.model = model

    def complete(
        self,
        *,
        stage: str,
        system: str,
        user: str,
        max_tokens: int,
        temperature: float,
        web_search: bool = False,
        web_search_max_uses: int = 5,
    ) -> LLMResult:
        tools: list[dict[str, Any]] = []
        if web_search:
            tools.append(
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": web_search_max_uses,
                }
            )

        messages: list[dict[str, Any]] = [{"role": "user", "content": user}]
        text_parts: list[str] = []
        citations: list[Citation] = []
        usage: dict[str, Any] = {}
        searches = 0

        # Server tools can pause a long turn; resend the assistant message
        # unchanged to continue. Cap the loop so a runaway search can't spin.
        for _ in range(6):
            kwargs: dict[str, Any] = dict(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=messages,
            )
            if tools:
                kwargs["tools"] = tools
            response = self._client.messages.create(**kwargs)

            for block in response.content:
                btype = getattr(block, "type", None)
                if btype == "text":
                    text_parts.append(block.text)
                    for c in getattr(block, "citations", None) or []:
                        if getattr(c, "type", "") == "web_search_result_location":
                            citations.append(
                                Citation(
                                    url=c.url,
                                    title=c.title,
                                    cited_text=getattr(c, "cited_text", "") or "",
                                )
                            )
                elif btype == "server_tool_use":
                    searches += 1

            u = getattr(response, "usage", None)
            if u is not None:
                usage = {
                    "input_tokens": getattr(u, "input_tokens", None),
                    "output_tokens": getattr(u, "output_tokens", None),
                }

            if response.stop_reason == "pause_turn":
                messages.append({"role": "assistant", "content": response.content})
                continue
            break

        return LLMResult(
            text="".join(text_parts),
            citations=_dedupe(citations),
            usage=usage,
            searches=searches,
        )


def _dedupe(cites: list[Citation]) -> list[Citation]:
    seen: set[str] = set()
    out: list[Citation] = []
    for c in cites:
        if c.url not in seen:
            seen.add(c.url)
            out.append(c)
    return out


# --------------------------------------------------------------------------- #
# Fixture client (offline)
# --------------------------------------------------------------------------- #


class FixtureClient:
    """Serves canned stage outputs from a fixtures directory.

    Lookup order for stage ``review``: ``review.json``, then ``review.md``.
    A stage that is called more than once in a run (review, revise) can
    provide numbered fixtures: ``review.1.json``, ``review.2.json``.
    """

    def __init__(self, fixtures_dir: Path | None = None) -> None:
        self.dir = Path(fixtures_dir) if fixtures_dir else FIXTURES_DIR
        self._calls: dict[str, int] = {}
        self.transcript: list[dict[str, str]] = []

    def complete(
        self,
        *,
        stage: str,
        system: str,
        user: str,
        max_tokens: int,
        temperature: float,
        web_search: bool = False,
        web_search_max_uses: int = 5,
    ) -> LLMResult:
        n = self._calls.get(stage, 0) + 1
        self._calls[stage] = n
        self.transcript.append({"stage": stage, "system": system, "user": user})

        for name in (f"{stage}.{n}.json", f"{stage}.{n}.md", f"{stage}.json", f"{stage}.md"):
            path = self.dir / name
            if path.exists():
                return LLMResult(text=path.read_text(encoding="utf-8"), usage={"fixture": name})
        raise FileNotFoundError(f"No fixture for stage '{stage}' in {self.dir}")
