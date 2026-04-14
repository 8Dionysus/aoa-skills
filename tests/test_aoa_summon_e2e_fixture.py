from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
SDK_FIXTURE_PATH = (
    WORKSPACE_ROOT / "aoa-sdk" / "examples" / "a2a" / "summon_return_checkpoint_e2e.fixture.json"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_aoa_summon_runtime_example_points_to_sdk_e2e_fixture() -> None:
    skill_text = (REPO_ROOT / "skills" / "aoa-summon" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    runtime_text = (
        REPO_ROOT / "skills" / "aoa-summon" / "examples" / "runtime.md"
    ).read_text(encoding="utf-8")

    for text in (skill_text, runtime_text):
        assert "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json" in text


def test_sdk_e2e_fixture_validates_aoa_summon_v3_contracts() -> None:
    if not SDK_FIXTURE_PATH.exists():
        pytest.skip("live aoa-sdk E2E fixture is unavailable")

    request_schema = load_json(
        REPO_ROOT / "skills" / "aoa-summon" / "references" / "summon-request-v3.schema.json"
    )
    result_schema = load_json(
        REPO_ROOT / "skills" / "aoa-summon" / "references" / "summon-result-v3.schema.json"
    )
    fixture = load_json(SDK_FIXTURE_PATH)

    request_errors = sorted(
        Draft202012Validator(request_schema).iter_errors(fixture["summon_request"]),
        key=lambda error: list(error.absolute_path),
    )
    result_errors = sorted(
        Draft202012Validator(result_schema).iter_errors(fixture["summon_result"]),
        key=lambda error: list(error.absolute_path),
    )

    assert request_errors == []
    assert result_errors == []
    assert fixture["summon_decision"]["lane"] == "codex_local_reviewed"
    assert fixture["dry_run"] is True
    assert fixture["live_automation"] is False
