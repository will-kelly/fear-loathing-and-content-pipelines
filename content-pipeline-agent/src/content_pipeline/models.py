"""Stage contracts.

Each stage produces exactly one of these. ``validate`` is deliberately
strict about required keys and loose about extras, so a prompt can grow
new fields without breaking downstream stages.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ContractError(ValueError):
    """Raised when a stage output is missing something the next stage needs."""


def _require(d: dict[str, Any], keys: list[str], where: str) -> None:
    missing = [k for k in keys if k not in d or d[k] in (None, "", [])]
    if missing:
        raise ContractError(f"{where} is missing required field(s): {', '.join(missing)}")


# --------------------------------------------------------------------------- #
# Stage 1: brief
# --------------------------------------------------------------------------- #


@dataclass
class Brief:
    working_title: str
    thesis: str
    audience: str
    channel: str
    register: str
    reader_problem: str
    what_changes_for_the_reader: str
    open_questions: list[str] = field(default_factory=list)
    anchors: list[str] = field(default_factory=list)  # first-hand material the writer supplied
    non_goals: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Brief":
        _require(
            d,
            ["working_title", "thesis", "audience", "channel", "register",
             "reader_problem", "what_changes_for_the_reader"],
            "Brief",
        )
        return cls(
            working_title=d["working_title"],
            thesis=d["thesis"],
            audience=d["audience"],
            channel=d["channel"],
            register=d["register"],
            reader_problem=d["reader_problem"],
            what_changes_for_the_reader=d["what_changes_for_the_reader"],
            open_questions=list(d.get("open_questions", [])),
            anchors=list(d.get("anchors", [])),
            non_goals=list(d.get("non_goals", [])),
            raw=d,
        )


# --------------------------------------------------------------------------- #
# Stage 2: claims ledger
# --------------------------------------------------------------------------- #

CLAIM_KINDS = {"observation", "anchor", "framework", "fact"}
CONFIDENCE = {"VERIFIED", "CORROBORATED", "SIGNAL", "UNSUPPORTED"}


@dataclass
class Claim:
    id: str
    kind: str          # observation | anchor | framework | fact
    text: str
    confidence: str    # VERIFIED | CORROBORATED | SIGNAL | UNSUPPORTED
    sources: list[dict[str, str]] = field(default_factory=list)  # {url,title,note}
    how_to_use: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Claim":
        _require(d, ["id", "kind", "text", "confidence"], "Claim")
        if d["kind"] not in CLAIM_KINDS:
            raise ContractError(f"Claim {d['id']}: unknown kind '{d['kind']}'")
        if d["confidence"] not in CONFIDENCE:
            raise ContractError(f"Claim {d['id']}: unknown confidence '{d['confidence']}'")
        if d["kind"] == "fact" and d["confidence"] in {"VERIFIED", "CORROBORATED"} and not d.get("sources"):
            raise ContractError(
                f"Claim {d['id']}: a {d['confidence']} fact needs at least one source"
            )
        return cls(
            id=d["id"],
            kind=d["kind"],
            text=d["text"],
            confidence=d["confidence"],
            sources=list(d.get("sources", [])),
            how_to_use=d.get("how_to_use", ""),
        )


@dataclass
class ClaimsLedger:
    claims: list[Claim]
    framework_name: str
    gaps: list[str] = field(default_factory=list)   # things the writer must supply
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ClaimsLedger":
        _require(d, ["claims", "framework_name"], "ClaimsLedger")
        claims = [Claim.from_dict(c) for c in d["claims"]]
        ids = [c.id for c in claims]
        if len(ids) != len(set(ids)):
            raise ContractError("ClaimsLedger has duplicate claim ids")
        if not any(c.kind == "framework" for c in claims):
            raise ContractError("ClaimsLedger must contain at least one 'framework' claim")
        return cls(
            claims=claims,
            framework_name=d["framework_name"],
            gaps=list(d.get("gaps", [])),
            raw=d,
        )

    def by_id(self) -> dict[str, Claim]:
        return {c.id: c for c in self.claims}

    def unsupported(self) -> list[Claim]:
        return [c for c in self.claims if c.confidence == "UNSUPPORTED"]


# --------------------------------------------------------------------------- #
# Stage 3: draft
# --------------------------------------------------------------------------- #


@dataclass
class Draft:
    title: str
    body_markdown: str
    claims_used: list[str]
    placeholders: list[str] = field(default_factory=list)
    revision: int = 0
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any], revision: int = 0) -> "Draft":
        _require(d, ["title", "body_markdown", "claims_used"], "Draft")
        return cls(
            title=d["title"],
            body_markdown=d["body_markdown"],
            claims_used=list(d["claims_used"]),
            placeholders=list(d.get("placeholders", [])),
            revision=revision,
            raw=d,
        )

    @property
    def word_count(self) -> int:
        return len(self.body_markdown.split())


# --------------------------------------------------------------------------- #
# Stage 4: review
# --------------------------------------------------------------------------- #


@dataclass
class ReviewFinding:
    check: str
    verdict: str   # PASS | FAIL | WARN
    detail: str
    fix: str = ""


@dataclass
class Review:
    score: int                       # 1..10
    verdict: str                     # PASS | FAIL
    findings: list[ReviewFinding]
    lint: dict[str, Any] = field(default_factory=dict)   # deterministic checks
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Review":
        _require(d, ["score", "findings"], "Review")
        findings = [
            ReviewFinding(
                check=f["check"],
                verdict=f["verdict"].upper(),
                detail=f.get("detail", ""),
                fix=f.get("fix", ""),
            )
            for f in d["findings"]
        ]
        return cls(score=int(d["score"]), verdict=d.get("verdict", "").upper(), findings=findings, raw=d)

    def failures(self) -> list[ReviewFinding]:
        return [f for f in self.findings if f.verdict == "FAIL"]


# --------------------------------------------------------------------------- #
# Stage 5: package
# --------------------------------------------------------------------------- #


@dataclass
class Package:
    final_markdown: str
    headline_options: list[str]
    dek: str
    channel_cuts: dict[str, str]
    seo: dict[str, Any]
    changelog: list[str]
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Package":
        _require(d, ["final_markdown", "headline_options", "dek", "channel_cuts"], "Package")
        return cls(
            final_markdown=d["final_markdown"],
            headline_options=list(d["headline_options"]),
            dek=d["dek"],
            channel_cuts=dict(d["channel_cuts"]),
            seo=dict(d.get("seo", {})),
            changelog=list(d.get("changelog", [])),
            raw=d,
        )
