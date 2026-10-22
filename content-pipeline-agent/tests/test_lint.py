"""Deterministic review checks. These run with no model and no network."""

import json

from content_pipeline.config import FIXTURES_DIR
from content_pipeline.models import ClaimsLedger, Draft
from content_pipeline.stages import lint


def _ledger() -> ClaimsLedger:
    return ClaimsLedger.from_dict(json.loads((FIXTURES_DIR / "claims.json").read_text()))


def _draft(**overrides) -> Draft:
    d = json.loads((FIXTURES_DIR / "draft.json").read_text())
    d.update(overrides)
    return Draft.from_dict(d)


def _verdict(res, check):
    return next(f for f in res["findings"] if f.check == check).verdict


def test_fixture_draft_passes_lint():
    res = lint(_draft(), _ledger(), 600, 1600)
    assert res["ok"], [f.__dict__ for f in res["findings"] if f.verdict == "FAIL"]
    assert _verdict(res, "placeholders") == "WARN"  # fixture intentionally keeps one


def test_length_gate():
    res = lint(_draft(body_markdown="too short"), _ledger(), 600, 1600)
    assert _verdict(res, "length") == "FAIL"
    assert not res["ok"]


def test_unknown_claim_id_fails():
    res = lint(_draft(claims_used=["C1", "C99"]), _ledger(), 600, 1600)
    assert _verdict(res, "claim_ids") == "FAIL"


def test_unsupported_claim_use_fails():
    res = lint(_draft(claims_used=["C1", "C6", "C10"]), _ledger(), 600, 1600)
    assert _verdict(res, "unsupported_claims") == "FAIL"


def test_missing_framework_fails():
    res = lint(_draft(claims_used=["C1", "C2", "C3"]), _ledger(), 600, 1600)
    assert _verdict(res, "framework") == "FAIL"


def test_banned_phrase_fails():
    body = _draft().body_markdown + "\n\nIn today's fast-paced world we must leverage synergy."
    res = lint(_draft(body_markdown=body), _ledger(), 600, 1600)
    f = next(f for f in res["findings"] if f.check == "banned_phrases")
    assert f.verdict == "FAIL"
    assert "in today's fast-paced" in f.detail
