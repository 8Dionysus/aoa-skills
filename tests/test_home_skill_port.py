from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from export import home_skill_port


def make_owner(root: Path) -> Path:
    (root / "skills" / "aoa-stats").mkdir(parents=True)
    (root / "docs" / "decisions").mkdir(parents=True)
    (root / "AGENTS.md").write_text("# owner\n", encoding="utf-8")
    (root / "docs" / "decisions" / "AOST-D-0011.md").write_text(
        "# Admit aoa-stats\n", encoding="utf-8"
    )
    (root / "skills" / "aoa-stats" / "SKILL.md").write_text(
        "---\n"
        "name: aoa-stats\n"
        "description: Answer one bounded owner-local stats question.\n"
        "---\n\n"
        "# aoa-stats\n",
        encoding="utf-8",
    )
    (root / "skills" / "aoa-stats" / "scripts").mkdir()
    helper = root / "skills" / "aoa-stats" / "scripts" / "inspect.sh"
    helper.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    helper.chmod(0o755)
    manifest = {
        "schema_version": "aoa_skill_home_port_v1",
        "contract_ref": "aoa-skills:schemas/skill-home-port.schema.json",
        "owner_repo": "aoa-stats",
        "owner_ref": "AGENTS.md",
        "bundles": [
            {
                "name": "aoa-stats",
                "path": "skills/aoa-stats",
                "version": "0.1.0",
                "lifecycle": "admitted",
                "visibility": "advertised",
                "admission_ref": "docs/decisions/AOST-D-0011.md",
            }
        ],
        "projection": {
            "runtime": "codex",
            "scope": "repo",
            "root": ".agents/skills",
            "mode": "generated-copy",
            "skills": ["aoa-stats"],
        },
    }
    (root / "skills" / "port.manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return root


def upgrade_owner_to_v2(root: Path) -> dict[str, object]:
    manifest_path = root / "skills" / "port.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    projection = manifest.pop("projection")
    manifest["schema_version"] = "aoa_skill_home_port_v2"
    manifest["exposure"] = {
        "runtime": projection["runtime"],
        "scope": "user",
        "profile": "os-user-default",
        "mode": "profile-selected",
        "skills": projection["skills"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def test_schema_is_valid(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    schema = json.loads((repo_root / "schemas" / "skill-home-port.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    owner = make_owner(tmp_path / "aoa-stats")
    manifest_path = owner / "skills" / "port.manifest.json"
    validator.validate(json.loads(manifest_path.read_text(encoding="utf-8")))
    validator.validate(upgrade_owner_to_v2(owner))


def test_projection_roundtrip_and_source_drift(tmp_path: Path) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    port = home_skill_port.load_port_definition(owner)

    preview = home_skill_port.projection_plan(port)
    assert preview["clean"] is False
    assert preview["bundles"][0]["status"] == "missing"

    built = home_skill_port.apply_projection(port)
    assert built["clean"] is True
    projected_helper = owner / ".agents" / "skills" / "aoa-stats" / "scripts" / "inspect.sh"
    assert projected_helper.stat().st_mode & 0o111

    skill_path = owner / "skills" / "aoa-stats" / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8") + "\n## Contract\n", encoding="utf-8"
    )
    drift = home_skill_port.projection_plan(port)
    assert drift["bundles"][0]["status"] == "drift"
    assert home_skill_port.apply_projection(port)["clean"] is True


def test_unexpected_projection_requires_explicit_prune(tmp_path: Path) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    port = home_skill_port.load_port_definition(owner)
    home_skill_port.apply_projection(port)
    legacy = owner / ".agents" / "skills" / "aoa-adr-write"
    legacy.mkdir()
    (legacy / "SKILL.md").write_text("legacy\n", encoding="utf-8")

    plan = home_skill_port.projection_plan(port)
    assert plan["unexpected_entries"] == ["aoa-adr-write"]
    with pytest.raises(home_skill_port.PortContractError, match="explicit --prune"):
        home_skill_port.apply_projection(port)

    final = home_skill_port.apply_projection(port, prune=True)
    assert final["clean"] is True
    assert not legacy.exists()


def test_manifest_frontmatter_and_visibility_must_agree(tmp_path: Path) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    skill_path = owner / "skills" / "aoa-stats" / "SKILL.md"
    original_skill = skill_path.read_text(encoding="utf-8")
    skill_path.write_text(
        original_skill.replace("name: aoa-stats", "name: wrong-name"),
        encoding="utf-8",
    )
    with pytest.raises(home_skill_port.PortContractError, match="frontmatter name differs"):
        home_skill_port.load_port_definition(owner)

    skill_path.write_text(original_skill, encoding="utf-8")
    manifest_path = owner / "skills" / "port.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["bundles"][0]["visibility"] = "explicit-only"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(home_skill_port.PortContractError, match="non-advertised candidates"):
        home_skill_port.load_port_definition(owner)


def test_v2_user_exposure_rejects_same_name_repo_projection(tmp_path: Path) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    manifest = upgrade_owner_to_v2(owner)
    schema = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "skill-home-port.schema.json"
        ).read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(manifest)

    port = home_skill_port.load_port_definition(owner)
    clean = home_skill_port.validation_plan(port)
    assert clean["clean"] is True
    assert clean["duplicate_repo_projections"] == []
    with pytest.raises(home_skill_port.PortContractError, match="OS user profile"):
        home_skill_port.projection_plan(port)

    repo_only = owner / ".agents" / "skills" / "repo-only"
    repo_only.mkdir(parents=True)
    (repo_only / "SKILL.md").write_text("repo-only\n", encoding="utf-8")
    assert home_skill_port.validation_plan(port)["clean"] is True

    duplicate = owner / ".agents" / "skills" / "aoa-stats"
    duplicate.mkdir()
    (duplicate / "SKILL.md").write_text("duplicate\n", encoding="utf-8")
    blocked = home_skill_port.validation_plan(port)
    assert blocked["clean"] is False
    assert blocked["duplicate_repo_projections"] == [
        ".agents/skills/aoa-stats"
    ]


def test_transient_or_symlinked_bundle_payload_is_rejected(tmp_path: Path) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    cache = owner / "skills" / "aoa-stats" / "__pycache__"
    cache.mkdir()
    (cache / "helper.pyc").write_bytes(b"cache")
    with pytest.raises(home_skill_port.PortContractError, match="transient build residue"):
        home_skill_port.load_port_definition(owner)

    (cache / "helper.pyc").unlink()
    cache.rmdir()
    external = tmp_path / "external.txt"
    external.write_text("not owner payload\n", encoding="utf-8")
    (owner / "skills" / "aoa-stats" / "external.txt").symlink_to(external)
    with pytest.raises(home_skill_port.PortContractError, match="contains a symlink"):
        home_skill_port.load_port_definition(owner)

    (owner / "skills" / "aoa-stats" / "external.txt").unlink()
    (owner / "skills").rename(owner / "real-skills")
    (owner / "skills").symlink_to("real-skills", target_is_directory=True)
    with pytest.raises(
        home_skill_port.PortContractError,
        match="path component must not be a symlink",
    ):
        home_skill_port.load_port_definition(owner)
