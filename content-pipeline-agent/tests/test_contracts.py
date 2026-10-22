"""Stage contracts and JSON extraction."""

import pytest

from content_pipeline.llm import extract_json
from content_pipeline.models import Claim, ClaimsLedger, ContractError


def test_extract_json_bare():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_fenced_with_prose():
    text = 'Here you go:\n```json\n{"a": [1, 2]}\n```\nLet me know if you need changes.'
    assert extract_json(text) == {"a": [1, 2]}


def test_extract_json_trailing_commentary():
    assert extract_json('{"ok": true} -- done') == {"ok": True}


def test_extract_json_raises_on_garbage():
    with pytest.raises(ValueError):
        extract_json("no json here")


def test_verified_fact_requires_source():
    with pytest.raises(ContractError):
        Claim.from_dict({"id": "C1", "kind": "fact", "text": "x", "confidence": "VERIFIED", "sources": []})


def test_signal_fact_does_not_require_source():
    c = Claim.from_dict({"id": "C1", "kind": "fact", "text": "x", "confidence": "SIGNAL"})
    assert c.confidence == "SIGNAL"


def test_ledger_requires_framework():
    with pytest.raises(ContractError, match="framework"):
        ClaimsLedger.from_dict({
            "framework_name": "x",
            "claims": [{"id": "C1", "kind": "observation", "text": "x", "confidence": "VERIFIED"}],
        })


def test_ledger_rejects_duplicate_ids():
    with pytest.raises(ContractError, match="duplicate"):
        ClaimsLedger.from_dict({
            "framework_name": "x",
            "claims": [
                {"id": "C1", "kind": "framework", "text": "x", "confidence": "VERIFIED"},
                {"id": "C1", "kind": "observation", "text": "y", "confidence": "VERIFIED"},
            ],
        })
