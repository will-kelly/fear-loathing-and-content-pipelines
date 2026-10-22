"""End-to-end runs against fixtures. No API key, no network."""

import json
import shutil
from pathlib import Path

from content_pipeline import Pipeline
from content_pipeline.config import FIXTURES_DIR, PipelineConfig
from content_pipeline.llm import FixtureClient

BRIEF = Path(__file__).resolve().parents[1] / "examples" / "briefs" / "documentation-debt.md"


def test_full_run_passes_and_writes_every_artifact(tmp_path):
    run = Pipeline(PipelineConfig(dry_run=True)).run(BRIEF.read_text(), runs_dir=tmp_path, run_name="t")
    assert run.passed
    assert run.revisions == 0
    assert run.package is not None
    assert set(run.package.channel_cuts) == {"newsletter", "linkedin", "exec_summary"}

    names = {p.name for p in (tmp_path / "t").iterdir()}
    for expected in [
        "00_input.md", "01_brief.json", "02_claims.json",
        "03_draft.r0.json", "03_draft.r0.md", "04_review.r0.json",
        "05_package.json", "05_final.md", "05_cut_linkedin.md", "manifest.json",
    ]:
        assert expected in names, expected

    manifest = json.loads((tmp_path / "t" / "manifest.json").read_text())
    assert manifest["passed"] is True
    assert [s["stage"] for s in manifest["stages"]] == ["intake", "claims", "draft", "review", "package"]


def test_stage_prompts_receive_the_right_context(tmp_path):
    client = FixtureClient()
    Pipeline(PipelineConfig(dry_run=True), client=client).run(BRIEF.read_text(), runs_dir=tmp_path)
    by_stage = {t["stage"]: t for t in client.transcript}

    # Drafter only sees the ledger as its source of truth; reviewer sees the draft.
    assert "Claims ledger" in by_stage["draft"]["user"]
    assert "quiet discount" in by_stage["review"]["user"].lower()
    # Claims stage is told web search is off, so it must not fabricate sources.
    assert "Web search is OFF" in by_stage["claims"]["user"]
    # Voice guide reaches the three stages that need it.
    for stage in ("draft", "review", "package"):
        assert "Voice guide" in by_stage[stage]["user"]


def _fixtures_with_failing_first_review(tmp_path) -> Path:
    """Copy the fixtures, then make the first review FAIL and the second PASS."""
    fx = tmp_path / "fx"
    shutil.copytree(FIXTURES_DIR, fx)
    review = json.loads((fx / "review.json").read_text())
    failing = dict(review, score=5, verdict="FAIL")
    failing["findings"] = [
        {"check": "thesis_delivery", "verdict": "FAIL", "detail": "buried", "fix": "move it up"}
    ] + review["findings"][1:]
    (fx / "review.1.json").write_text(json.dumps(failing))
    (fx / "review.2.json").write_text(json.dumps(review))
    return fx


def test_fail_fix_recheck_loop_revises_once(tmp_path):
    fx = _fixtures_with_failing_first_review(tmp_path)
    client = FixtureClient(fx)
    run = Pipeline(PipelineConfig(dry_run=True, max_revision_passes=2), client=client).run(
        BRIEF.read_text(), runs_dir=tmp_path / "runs", run_name="loop"
    )
    assert run.passed
    assert run.revisions == 1
    assert run.draft.revision == 1
    stages = [t["stage"] for t in client.transcript]
    assert stages == ["intake", "claims", "draft", "review", "draft", "review", "package"]
    # The revision prompt carried the failing finding forward.
    revision_prompt = client.transcript[4]["user"]
    assert "Revision pass 1" in revision_prompt and "buried" in revision_prompt
    names = {p.name for p in (tmp_path / "runs" / "loop").iterdir()}
    assert {"03_draft.r0.md", "03_draft.r1.md", "04_review.r0.json", "04_review.r1.json"} <= names


def test_run_stops_before_package_when_review_never_passes(tmp_path):
    fx = _fixtures_with_failing_first_review(tmp_path)
    # Make every review fail by removing the passing second fixture.
    (fx / "review.2.json").unlink()
    (fx / "review.json").write_text((fx / "review.1.json").read_text())
    client = FixtureClient(fx)
    run = Pipeline(PipelineConfig(dry_run=True, max_revision_passes=1), client=client).run(
        BRIEF.read_text(), runs_dir=tmp_path / "runs", run_name="stop"
    )
    assert not run.passed
    assert run.revisions == 1
    assert run.package is None
    assert "package" not in [t["stage"] for t in client.transcript]
    assert "STOPPED AT REVIEW" in run.summary()


def test_lint_failure_overrides_model_pass(tmp_path):
    """The model can say PASS; lint still has a veto."""
    fx = tmp_path / "fx"
    shutil.copytree(FIXTURES_DIR, fx)
    draft = json.loads((fx / "draft.json").read_text())
    draft["body_markdown"] += "\n\nThis is a game-changer that will revolutionize everything."
    (fx / "draft.json").write_text(json.dumps(draft))
    run = Pipeline(PipelineConfig(dry_run=True, max_revision_passes=0), client=FixtureClient(fx)).run(
        BRIEF.read_text(), runs_dir=tmp_path / "runs", run_name="veto"
    )
    assert not run.passed
    assert "banned_phrases" in [f.check for f in run.review.failures()]
