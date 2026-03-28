#!/usr/bin/env python3
"""Install a resolved skill pack into a Codex skill root by copy or symlink."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
from typing import Any

import skill_pack_install_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument("--profile", required=True, help="Profile name from generated/skill_pack_profiles.resolved.json")
    parser.add_argument("--dest-root", default=None, help="Override destination root for installed skills")
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink", help="Install mode")
    parser.add_argument("--execute", action="store_true", help="Apply the install plan")
    parser.add_argument("--overwrite", action="store_true", help="Remove existing skill dirs before install")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    export_root = skill_pack_install_contract.export_root(repo_root)
    try:
        profile = skill_pack_install_contract.load_resolved_profile(repo_root, args.profile)
    except KeyError:
        raise SystemExit(f"unknown profile: {args.profile}")
    release_manifest = skill_pack_install_contract.load_release_manifest(repo_root)
    profile_revision = skill_pack_install_contract.load_install_profile_revision(
        release_manifest,
        args.profile,
    )["profile_revision"]

    dest_root = skill_pack_install_contract.resolve_install_root(
        repo_root,
        install_root_override=args.dest_root,
        default_install_root=profile["install_root"],
    )

    plan = {
        "profile": args.profile,
        "profile_revision": profile_revision,
        "scope": profile["scope"],
        "mode": args.mode,
        "source_root": str(export_root),
        "dest_root": str(dest_root),
        "execute": args.execute,
        "release_identity": dict(skill_pack_install_contract.release_identity(release_manifest)),
        "recommended_verify_command": skill_pack_install_contract.recommended_verify_command(
            profile_name=args.profile,
            install_root=dest_root,
            output_format="json",
        ),
        "steps": [],
    }

    for skill_entry in profile["skills"]:
        source_dir = export_root / skill_entry["name"]
        target_dir = dest_root / skill_entry["name"]
        plan["steps"].append(
            {
                "skill": skill_entry["name"],
                "source_dir": str(source_dir),
                "target_dir": str(target_dir),
                "exists": target_dir.exists(),
            }
        )

    if args.execute:
        dest_root.mkdir(parents=True, exist_ok=True)
        for step in plan["steps"]:
            source_dir = pathlib.Path(step["source_dir"])
            target_dir = pathlib.Path(step["target_dir"])
            if source_dir.resolve() == target_dir.resolve():
                raise SystemExit(f"target matches source for {step['skill']}: {target_dir}")
            if not source_dir.exists():
                raise SystemExit(f"missing source skill export: {source_dir}")

            if target_dir.exists():
                if not args.overwrite:
                    raise SystemExit(f"target exists: {target_dir} (use --overwrite to replace)")
                if target_dir.is_symlink() or target_dir.is_file():
                    target_dir.unlink()
                else:
                    shutil.rmtree(target_dir)

            if args.mode == "symlink":
                os.symlink(source_dir, target_dir, target_is_directory=True)
            else:
                shutil.copytree(source_dir, target_dir)

    if args.format == "json":
        print(json.dumps(plan, indent=2))
        return 0

    lines = [
        f"# Skill pack install plan: {args.profile}",
        "",
        f"Scope: {profile['scope']}",
        f"Profile revision: {profile_revision}",
        f"Mode: {args.mode}",
        f"Destination: {dest_root}",
        f"Execute: {args.execute}",
        f"Verify: {plan['recommended_verify_command']}",
        "",
        "## Steps",
    ]
    for step in plan["steps"]:
        lines.append(f"- {step['skill']}: {step['source_dir']} -> {step['target_dir']}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
