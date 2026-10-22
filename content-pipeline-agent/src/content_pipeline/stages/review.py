"""Stage 4 - Review. Two layers, in order:

1. **Lint** (deterministic, free, runs first). Word count, claim coverage,
   unsupported-claim use, placeholders, and a banned-phrase list of the
   tells that make a piece read as machine output. If lint fails, the
   model reviewer still runs so the revision pass gets both lists.
2. **Blind editorial review** (model). The reviewer gets the draft, the
   ledger, and the voice guide. It does not get the writer's intent
   from the brief beyond the thesis, so it can't grade on effort.

A draft passes only when lint is clean, the model says PASS, and the
score clears ``min_review_score``.
"""

from __future__ import annotations

import re
from typing import Any

from ..models import Brief, ClaimsLedger, Draft, Review, ReviewFinding
from .base import RunContext, Stage, load_prompt, render

# Phrases that reliably mark a draft as unedited model output. Case-insensitive.
# Edit freely; this is a style policy, not a law of nature.
BANNED_PHRASES = [
    "in today's fast-paced",
    "in the ever-evolving",
    "it's important to note",
    "it is important to note",
    "game-changer",
    "game changer",
    "delve",
    "unlock the power",
    "harness the power",
    "seamlessly",
    "cutting-edge",
    "robust solution",
    "at the end of the day",
    "navigate the complexities",
    "in conclusion,",
    "let's dive in",
    "revolutionize",
    "paradigm shift",
    "synerg",
    "leverage ",  # as a verb; the noun form is fine but rare in this register
]

_PLACEHOLDER = re.compile(r"\[PLACEHOLDER:[^\]]*\]")


def lint(draft: Draft, ledger: ClaimsLedger, min_words: int, max_words: int) -> dict[str, Any]:
    """Deterministic checks. Returns findings plus a boolean ``ok``."""
    findings: list[ReviewFinding] = []
    body = draft.body_markdown
    lower = body.lower()

    # Length
    wc = draft.word_count
    if wc < min_words or wc > max_words:
        findings.append(ReviewFinding(
            check="length", verdict="FAIL",
            detail=f"{wc} words; target is {min_words}-{max_words}.",
            fix="Cut or extend to land inside the target range.",
        ))
    else:
        findings.append(ReviewFinding(check="length", verdict="PASS", detail=f"{wc} words."))

    # Claim ids resolve
    known = ledger.by_id()
    unknown = [cid for cid in draft.claims_used if cid not in known]
    if unknown:
        findings.append(ReviewFinding(
            check="claim_ids", verdict="FAIL",
            detail=f"claims_used references ids not in the ledger: {unknown}",
            fix="Remove the assertion or add it to the ledger first.",
        ))
    else:
        findings.append(ReviewFinding(check="claim_ids", verdict="PASS", detail="All claim ids resolve."))

    # No UNSUPPORTED claims in the draft
    used_unsupported = [cid for cid in draft.claims_used if cid in known and known[cid].confidence == "UNSUPPORTED"]
    if used_unsupported:
        findings.append(ReviewFinding(
            check="unsupported_claims", verdict="FAIL",
            detail=f"Draft uses UNSUPPORTED claims: {used_unsupported}",
            fix="Cut them, soften to an explicit opinion, or get a source.",
        ))
    else:
        findings.append(ReviewFinding(check="unsupported_claims", verdict="PASS", detail="No unsupported claims used."))

    # Framework coverage: the original apparatus must appear in the draft
    fw_ids = [c.id for c in ledger.claims if c.kind == "framework"]
    if fw_ids and not any(cid in draft.claims_used for cid in fw_ids):
        findings.append(ReviewFinding(
            check="framework", verdict="FAIL",
            detail=f"None of the framework claims {fw_ids} are used.",
            fix="The piece needs its original apparatus; put it back.",
        ))
    else:
        findings.append(ReviewFinding(check="framework", verdict="PASS", detail="Framework claim present."))

    # Placeholders
    ph = _PLACEHOLDER.findall(body)
    if ph:
        findings.append(ReviewFinding(
            check="placeholders", verdict="WARN",
            detail=f"{len(ph)} placeholder(s) still in the body.",
            fix="Writer must fill these before publish; the pipeline will not invent them.",
        ))
    else:
        findings.append(ReviewFinding(check="placeholders", verdict="PASS", detail="No placeholders."))

    # Banned phrases
    hits = sorted({p.strip() for p in BANNED_PHRASES if p in lower})
    if hits:
        findings.append(ReviewFinding(
            check="banned_phrases", verdict="FAIL",
            detail=f"Found: {hits}",
            fix="Rewrite each sentence that uses one; do not just delete the phrase.",
        ))
    else:
        findings.append(ReviewFinding(check="banned_phrases", verdict="PASS", detail="None found."))

    ok = not any(f.verdict == "FAIL" for f in findings)
    return {"ok": ok, "word_count": wc, "findings": findings}


class ReviewStage(Stage):
    name = "review"

    def run(self, ctx: RunContext) -> Review:
        brief: Brief = ctx.artifacts["brief"]
        ledger: ClaimsLedger = ctx.artifacts["ledger"]
        draft: Draft = ctx.artifacts["draft"]
        cfg = ctx.config

        lint_result = lint(draft, ledger, cfg.min_words, cfg.max_words)

        system = load_prompt("review")
        user = render(
            "## Thesis under review\n\n{{thesis}}\n\n"
            "## Draft\n\n# {{title}}\n\n{{body}}\n\n"
            "## Claims ledger\n\n{{ledger}}\n\n"
            "## Voice guide\n\n{{voice}}\n\n"
            "## Deterministic lint (already run; do not repeat these checks)\n\n{{lint}}",
            thesis=brief.thesis,
            title=draft.title,
            body=draft.body_markdown,
            ledger=ledger.raw,
            voice=cfg.voice_text(),
            lint=[f.__dict__ for f in lint_result["findings"]],
        )
        result = ctx.client.complete(
            stage=self.name,
            system=system,
            user=user,
            max_tokens=cfg.max_tokens,
            temperature=0.2,
        )
        review = Review.from_dict(result.json())

        # Merge: lint findings first, then the model's. Final verdict is ours.
        review.findings = lint_result["findings"] + review.findings
        review.lint = {"ok": lint_result["ok"], "word_count": lint_result["word_count"]}
        model_pass = review.verdict == "PASS" if review.verdict else not review.failures()
        passed = lint_result["ok"] and model_pass and review.score >= cfg.min_review_score
        review.verdict = "PASS" if passed else "FAIL"

        ctx.record(self.name, result, note=f"{review.verdict} score={review.score} lint_ok={lint_result['ok']}")
        ctx.write(
            f"04_review.r{draft.revision}.json",
            {
                "verdict": review.verdict,
                "score": review.score,
                "lint": review.lint,
                "findings": [f.__dict__ for f in review.findings],
                "model_output": review.raw,
            },
        )
        ctx.artifacts["review"] = review
        return review
