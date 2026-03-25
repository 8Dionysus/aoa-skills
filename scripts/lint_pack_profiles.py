#!/usr/bin/env python3
"""Lint pack-profile authoring and resolved install-profile artifacts."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

STANDARD_SCOPES = {"repo", "user", "admin"}
STANDARD_INSTALL_MODES = {"symlink-preferred", "copy"}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    errors: list[str] = []
    config_profiles = load_json(repo_root / "config" / "skill_pack_profiles.json")
    source_catalog = load_json(repo_root / "generated" / "skill_catalog.min.json")
    resolved_profiles = load_json(repo_root / "generated" / "skill_pack_profiles.resolved.json")
    snippets_doc = load_json(repo_root / "generated" / "codex_config_snippets.json")

    skill_names = {entry["name"] for entry in source_catalog["skills"]}
    config_profile_names = set(config_profiles.get("profiles", {}))
    resolved_profile_names = set(resolved_profiles.get("profiles", {}))
    snippet_profile_names = set(snippets_doc.get("snippets", {}))

    if config_profile_names != resolved_profile_names:
        errors.append("resolved profile set does not match config profile set")
    if config_profile_names != snippet_profile_names:
        errors.append("config snippet profile set does not match config profile set")

    for profile_name, profile in config_profiles.get("profiles", {}).items():
        scope = profile.get("scope")
        install_mode = profile.get("install_mode")
        skills = profile.get("skills", [])

        if scope not in STANDARD_SCOPES:
            errors.append(f"{profile_name}: invalid scope {scope!r}")
        if install_mode not in STANDARD_INSTALL_MODES:
            errors.append(f"{profile_name}: invalid install_mode {install_mode!r}")
        if not isinstance(skills, list) or not skills:
            errors.append(f"{profile_name}: skills must be a non-empty list")
            continue

        seen: set[str] = set()
        for skill_name in skills:
            if skill_name not in skill_names:
                errors.append(f"{profile_name}: unknown skill {skill_name!r}")
            if skill_name in seen:
                errors.append(f"{profile_name}: duplicate skill {skill_name!r}")
            seen.add(skill_name)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(config_profile_names)} skill pack profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
