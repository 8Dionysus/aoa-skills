"""Skill-pack profile validator for aoa-skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence


STANDARD_SCOPES = {"repo", "user", "admin"}
STANDARD_INSTALL_MODES = {"symlink-preferred", "copy"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile_sets(
    *,
    config_profile_names: set[str],
    resolved_profile_names: set[str],
    snippet_profile_names: set[str],
    errors: list[str],
) -> None:
    if config_profile_names != resolved_profile_names:
        errors.append("resolved profile set does not match config profile set")
    if config_profile_names != snippet_profile_names:
        errors.append("config snippet profile set does not match config profile set")


def validate_profile_entry(
    *,
    profile_name: str,
    profile: dict[str, Any],
    skill_names: set[str],
    errors: list[str],
) -> None:
    scope = profile.get("scope")
    install_mode = profile.get("install_mode")
    skills = profile.get("skills", [])
    if scope not in STANDARD_SCOPES:
        errors.append(f"{profile_name}: invalid scope {scope!r}")
    if install_mode not in STANDARD_INSTALL_MODES:
        errors.append(f"{profile_name}: invalid install_mode {install_mode!r}")
    if not isinstance(skills, list) or not skills:
        errors.append(f"{profile_name}: skills must be a non-empty list")
        return
    seen: set[str] = set()
    for skill_name in skills:
        if skill_name not in skill_names:
            errors.append(f"{profile_name}: unknown skill {skill_name!r}")
        if skill_name in seen:
            errors.append(f"{profile_name}: duplicate skill {skill_name!r}")
        seen.add(skill_name)


def lint(repo_root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    config_profiles = load_json(repo_root / "config" / "skill_pack_profiles.json")
    source_catalog = load_json(repo_root / "generated" / "skill_catalog.min.json")
    resolved_profiles = load_json(repo_root / "generated" / "skill_pack_profiles.resolved.json")
    snippets_doc = load_json(repo_root / "generated" / "codex_config_snippets.json")

    skill_names = {entry["name"] for entry in source_catalog["skills"]}
    config_profile_names = set(config_profiles.get("profiles", {}))
    validate_profile_sets(
        config_profile_names=config_profile_names,
        resolved_profile_names=set(resolved_profiles.get("profiles", {})),
        snippet_profile_names=set(snippets_doc.get("snippets", {})),
        errors=errors,
    )
    for profile_name, profile in config_profiles.get("profiles", {}).items():
        validate_profile_entry(
            profile_name=profile_name,
            profile=profile,
            skill_names=skill_names,
            errors=errors,
        )
    return errors, len(config_profile_names)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    errors, profile_count = lint(Path(args.repo_root).resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {profile_count} skill pack profiles")
    return 0
