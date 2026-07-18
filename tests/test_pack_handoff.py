from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from bundles import skill_pack_install_contract, smoke_skill_pack_handoff


def test_pack_source_uses_the_portable_hash_and_reports_unknown_profiles_truthfully() -> None:
    with skill_pack_install_contract.skill_pack_source_context(
        REPO_ROOT,
        profile_name="portable-consumer-advertised",
    ) as source:
        release = json.loads(
            (REPO_ROOT / "generated/release_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        revision = next(
            entry
            for entry in release["skill_bundle_revisions"]
            if entry["name"] == "aoa-decision"
        )
        decision = next(
            entry for entry in source["skills"] if entry["name"] == "aoa-decision"
        )
        temporary_source_root = Path(source["source_root"])

        assert source["source_kind"] == "temporary_portable_assembly"
        assert temporary_source_root.is_dir()
        assert decision["content_hash"] == revision["portable_hash"]

    assert not temporary_source_root.exists()
    with pytest.raises(ValueError, match=r"^unknown profile: absent$"):
        with skill_pack_install_contract.skill_pack_source_context(
            REPO_ROOT,
            profile_name="absent",
        ):
            pass


def test_default_pack_round_trip_matches_the_manual_dir_and_zip_path() -> None:
    tmp_parent = Path("/srv/abyss-machine/tmp/ai")
    kwargs = {"dir": tmp_parent} if tmp_parent.is_dir() else {}
    with tempfile.TemporaryDirectory(
        prefix="aoa-skills-pack-test-",
        **kwargs,
    ) as tmpdir:
        report = smoke_skill_pack_handoff.execute_smoke(
            repo_root=REPO_ROOT,
            profile="portable-consumer-advertised",
            transport="both",
            work_root=Path(tmpdir),
        )

    assert report["verified"] is True
    assert all(step["status"] == "ok" for step in report["steps"].values())
