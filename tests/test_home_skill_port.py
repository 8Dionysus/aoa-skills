from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from bundles import install_os_skill_profile
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


def test_os_profile_install_is_idempotent_and_receipt_bound(tmp_path: Path) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    upgrade_owner_to_v2(owner)
    config_path = tmp_path / "os-skill-profiles.json"
    config_path.write_text(
        json.dumps(
            {
                "schema_version": "aoa_os_skill_profiles_v1",
                "profiles": {
                    "os-user-default": {
                        "runtime": "codex",
                        "scope": "user",
                        "install_root": "$HOME/.codex/skills",
                        "install_mode": "managed-copy",
                        "sources": [
                            {
                                "kind": "owner-port",
                                "repo": "aoa-stats",
                                "root": "aoa-stats",
                                "skills": ["aoa-stats"],
                            }
                        ],
                    }
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    profile, skills = install_os_skill_profile.resolve_profile(
        repo_root=Path(__file__).resolve().parents[1],
        config_path=config_path,
        profile_name="os-user-default",
        os_root=tmp_path,
        overrides={"aoa-stats": owner},
    )
    destination = tmp_path / "installed"
    plan = install_os_skill_profile.build_plan(
        profile_name="os-user-default",
        profile=profile,
        skills=skills,
        dest_root=destination,
    )
    install_os_skill_profile.execute_plan(
        plan,
        skills,
        replace_unmanaged=False,
        prune_managed=False,
        allow_dirty_source=False,
    )
    current = install_os_skill_profile.build_plan(
        profile_name="os-user-default",
        profile=profile,
        skills=skills,
        dest_root=destination,
    )
    assert install_os_skill_profile.plan_is_current(
        current,
        allow_dirty_source=False,
    )

    receipt_path = destination / install_os_skill_profile.INSTALL_RECEIPT
    receipt_before = receipt_path.read_bytes()
    install_os_skill_profile.execute_plan(
        current,
        skills,
        replace_unmanaged=False,
        prune_managed=False,
        allow_dirty_source=False,
    )
    assert receipt_path.read_bytes() == receipt_before

    receipt = json.loads(receipt_before)
    assert receipt["schema_version"] == "aoa_os_skill_install_v3"
    installed_skill = receipt["skills"][0]
    assert installed_skill["management"] == "managed-copy"
    assert installed_skill["source_fingerprint"] == installed_skill["digest"]
    assert (
        installed_skill["source_fingerprint_scope"]
        == "complete-installable-package-v1"
    )
    assert installed_skill["capability_graph_hash"] is None
    assert installed_skill["prompt_description_sha256"] == hashlib.sha256(
        b"Answer one bounded owner-local stats question."
    ).hexdigest()
    source_receipt = json.loads(
        (
            destination
            / "aoa-stats"
            / install_os_skill_profile.SOURCE_RECEIPT
        ).read_text(encoding="utf-8")
    )
    assert source_receipt["schema_version"] == "aoa_skill_source_receipt_v2"
    assert source_receipt["source_fingerprint"] == installed_skill[
        "source_fingerprint"
    ]
    assert source_receipt["prompt_description_sha256"] == installed_skill[
        "prompt_description_sha256"
    ]
    assert "capability_graph_hash" not in source_receipt
    receipt["skills"][0]["owner_ref"] = "stale-ref"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    drift = install_os_skill_profile.build_plan(
        profile_name="os-user-default",
        profile=profile,
        skills=skills,
        dest_root=destination,
    )
    assert drift["install_receipt_status"] == "drift"
    assert not install_os_skill_profile.plan_is_current(
        drift,
        allow_dirty_source=False,
    )


@pytest.mark.parametrize("retire", [False, True])
def test_owner_scoped_install_preserves_unavailable_neighbor(
    tmp_path: Path, retire: bool,
) -> None:
    owner = make_owner(tmp_path / "aoa-stats")
    upgrade_owner_to_v2(owner)
    neighbor = tmp_path / "neighbor"
    neighbor_skill = neighbor / "skills" / "neighbor-skill"
    neighbor_skill.mkdir(parents=True)
    (neighbor_skill / "SKILL.md").write_text(
        "---\nname: neighbor-skill\ndescription: Inspect a neighbor.\n---\n\n# Neighbor\n",
        encoding="utf-8",
    )
    profile = {
        "runtime": "codex", "scope": "user",
        "install_root": "$HOME/.codex/skills", "install_mode": "managed-copy",
        "sources": [
            {"kind": "owner-port", "repo": "aoa-stats", "root": "aoa-stats", "skills": ["aoa-stats"]},
            {"kind": "direct-home", "repo": "neighbor", "root": "neighbor", "skills": [
                {"name": "neighbor-skill", "path": "skills/neighbor-skill", "version": "1"},
            ]},
        ],
    }
    config_path = tmp_path / "profiles.json"

    def resolve(owners: frozenset[str] | None = None):
        config_path.write_text(json.dumps({
            "schema_version": "aoa_os_skill_profiles_v1",
            "profiles": {"os-user-default": profile},
        }), encoding="utf-8")
        return install_os_skill_profile.resolve_profile(
            repo_root=Path(__file__).resolve().parents[1], config_path=config_path,
            profile_name="os-user-default", os_root=tmp_path, overrides={},
            owner_repos=owners,
        )

    destination = tmp_path / "installed"
    resolved_profile, skills = resolve()
    initial = install_os_skill_profile.build_plan(
        profile_name="os-user-default", profile=resolved_profile,
        skills=skills, dest_root=destination,
    )
    install_os_skill_profile.execute_plan(
        initial, skills, replace_unmanaged=False, prune_managed=False,
        allow_dirty_source=False,
    )
    before = install_os_skill_profile.installed_receipt(destination)
    assert before is not None
    neighbor_receipt = next(item for item in before["skills"] if item["owner_repo"] == "neighbor")
    neighbor_target = destination / "neighbor-skill"
    neighbor_snapshot = home_skill_port.tree_snapshot(neighbor_target, label="neighbor before")
    neighbor.rename(tmp_path / "unavailable-neighbor")
    if retire:
        profile["sources"] = profile["sources"][1:]
    else:
        source = owner / "skills" / "aoa-stats" / "SKILL.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nUpdated owner guidance.\n", encoding="utf-8")

    owners = frozenset({"aoa-stats"})
    resolved_profile, skills = resolve(owners)
    plan = install_os_skill_profile.build_plan(
        profile_name="os-user-default", profile=resolved_profile,
        skills=skills, dest_root=destination, owner_repos=owners,
    )
    assert plan["stale_managed"] == (["aoa-stats"] if retire else [])
    assert plan["verification_scope"]["unselected_owners_verified"] is False
    with pytest.raises(install_os_skill_profile.ProfileError, match="unknown profile owners"):
        install_os_skill_profile.build_plan(
            profile_name="os-user-default", profile=resolved_profile,
            skills=[], dest_root=destination, owner_repos=frozenset({"typo-owner"}),
        )
    with pytest.raises(install_os_skill_profile.ProfileError, match="existing matching profile receipt"):
        install_os_skill_profile.build_plan(
            profile_name="os-user-default", profile=resolved_profile,
            skills=skills, dest_root=tmp_path / "fresh", owner_repos=owners,
        )
    install_os_skill_profile.execute_plan(
        plan, skills, replace_unmanaged=False, prune_managed=retire,
        allow_dirty_source=False,
    )
    assert (destination / "aoa-stats").exists() == (not retire)
    assert home_skill_port.tree_snapshot(neighbor_target, label="neighbor after") == neighbor_snapshot
    after = install_os_skill_profile.installed_receipt(destination)
    assert after is not None
    assert next(item for item in after["skills"] if item["owner_repo"] == "neighbor") == neighbor_receipt
    current = install_os_skill_profile.build_plan(
        profile_name="os-user-default", profile=resolved_profile,
        skills=skills, dest_root=destination, owner_repos=owners,
    )
    assert install_os_skill_profile.plan_is_current(current, allow_dirty_source=False)
    install_os_skill_profile.execute_plan(
        current, skills, replace_unmanaged=False, prune_managed=retire,
        allow_dirty_source=False,
    )
    assert install_os_skill_profile.installed_receipt(destination) == after
    with pytest.raises(install_os_skill_profile.ProfileError, match="source root is missing"):
        resolve()

    receipt_path = destination / install_os_skill_profile.INSTALL_RECEIPT
    changed = dict(after, installed_at="2026-09-07T00:00:00Z")
    receipt_path.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(install_os_skill_profile.ProfileError, match="receipt changed"):
        install_os_skill_profile.execute_plan(
            current, skills, replace_unmanaged=False, prune_managed=retire,
            allow_dirty_source=False,
        )
    assert install_os_skill_profile.installed_receipt(destination) == changed
    assert home_skill_port.tree_snapshot(neighbor_target, label="neighbor preserved") == neighbor_snapshot


def test_os_profile_observes_owner_links_without_managing_them(
    tmp_path: Path,
) -> None:
    owner = tmp_path / ".aoa"
    global_source = owner / "skills" / "aoa-session-memory-global-route"
    evidence_source = owner / "skills" / "aoa-session-memory-evidence-route"
    for name, source in (
        ("aoa-session-memory-global-route", global_source),
        ("aoa-session-memory-evidence-route", evidence_source),
    ):
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            f"description: Route one bounded {name} request.\n"
            "---\n\n"
            f"# {name}\n",
            encoding="utf-8",
        )
    config_path = tmp_path / "os-skill-profiles.json"
    config_path.write_text(
        json.dumps(
            {
                "schema_version": "aoa_os_skill_profiles_v1",
                "profiles": {
                    "os-user-default": {
                        "runtime": "codex",
                        "scope": "user",
                        "install_root": "$HOME/.codex/skills",
                        "install_mode": "managed-copy",
                        "sources": [
                            {
                                "kind": "owner-link",
                                "repo": ".aoa",
                                "root": ".aoa",
                                "owner_operation": "install-user-skill",
                                "skills": [
                                    {
                                        "name": global_source.name,
                                        "path": (
                                            f"skills/{global_source.name}"
                                        ),
                                        "version": "owner-current",
                                    },
                                    {
                                        "name": evidence_source.name,
                                        "path": (
                                            f"skills/{evidence_source.name}"
                                        ),
                                        "version": "owner-current",
                                    },
                                ],
                            }
                        ],
                    }
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    profile, skills = install_os_skill_profile.resolve_profile(
        repo_root=Path(__file__).resolve().parents[1],
        config_path=config_path,
        profile_name="os-user-default",
        os_root=tmp_path,
        overrides={".aoa": owner},
    )
    destination = tmp_path / "installed"
    destination.mkdir()
    global_target = destination / global_source.name
    evidence_target = destination / evidence_source.name
    global_target.symlink_to(global_source, target_is_directory=True)
    evidence_target.symlink_to(evidence_source, target_is_directory=True)

    plan = install_os_skill_profile.build_plan(
        profile_name="os-user-default",
        profile=profile,
        skills=skills,
        dest_root=destination,
    )
    assert {
        item["name"]: (
            item["management"],
            item["owner_operation"],
            item["status"],
        )
        for item in plan["skills"]
    } == {
        global_source.name: (
            "owner-link",
            "install-user-skill",
            "owner-current",
        ),
        evidence_source.name: (
            "owner-link",
            "install-user-skill",
            "owner-current",
        ),
    }
    install_os_skill_profile.execute_plan(
        plan,
        skills,
        replace_unmanaged=False,
        prune_managed=False,
        allow_dirty_source=False,
    )
    assert global_target.is_symlink()
    assert global_target.resolve() == global_source.resolve()
    assert evidence_target.is_symlink()
    assert evidence_target.resolve() == evidence_source.resolve()
    assert not (global_source / install_os_skill_profile.SOURCE_RECEIPT).exists()
    receipt = json.loads(
        (destination / install_os_skill_profile.INSTALL_RECEIPT).read_text(
            encoding="utf-8"
        )
    )
    assert receipt["schema_version"] == "aoa_os_skill_install_v3"
    assert {item["management"] for item in receipt["skills"]} == {"owner-link"}

    receipt["schema_version"] = "aoa_os_skill_install_v2"
    for item in receipt["skills"]:
        item.pop("management")
        item.pop("owner_operation")
    (destination / install_os_skill_profile.INSTALL_RECEIPT).write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    migration = install_os_skill_profile.build_plan(
        profile_name="os-user-default",
        profile=profile,
        skills=skills,
        dest_root=destination,
    )
    assert migration["stale_managed"] == []
    assert migration["install_receipt_status"] == "drift"
    install_os_skill_profile.execute_plan(
        migration,
        skills,
        replace_unmanaged=False,
        prune_managed=False,
        allow_dirty_source=False,
    )
    assert global_target.is_symlink()
    assert global_target.resolve() == global_source.resolve()
    assert evidence_target.is_symlink()
    assert evidence_target.resolve() == evidence_source.resolve()

    global_target.unlink()
    global_target.symlink_to(evidence_source, target_is_directory=True)
    evidence_target.unlink()
    evidence_target.mkdir()
    blocked = install_os_skill_profile.build_plan(
        profile_name="os-user-default",
        profile=profile,
        skills=skills,
        dest_root=destination,
    )
    assert {
        item["name"]: item["status"] for item in blocked["skills"]
    } == {
        global_source.name: "owner-drift",
        evidence_source.name: "owner-collision",
    }
    receipt_before = (
        destination / install_os_skill_profile.INSTALL_RECEIPT
    ).read_bytes()
    with pytest.raises(
        install_os_skill_profile.ProfileError,
        match=r"\.aoa:install-user-skill\(aoa-session-memory-global-route\)",
    ):
        install_os_skill_profile.execute_plan(
            blocked,
            skills,
            replace_unmanaged=True,
            prune_managed=True,
            allow_dirty_source=False,
        )
    assert global_target.is_symlink()
    assert global_target.resolve() == evidence_source.resolve()
    assert evidence_target.is_dir() and not evidence_target.is_symlink()
    assert (
        destination / install_os_skill_profile.INSTALL_RECEIPT
    ).read_bytes() == receipt_before
