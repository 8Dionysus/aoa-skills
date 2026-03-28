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
    parser.add_argument(
        "--bundle-root",
        default=None,
        help="Optional staged profile-bundle root containing bundle_manifest.json",
    )
    parser.add_argument("--dest-root", default=None, help="Override destination root for installed skills")
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink", help="Install mode")
    parser.add_argument("--execute", action="store_true", help="Apply the install plan")
    parser.add_argument("--overwrite", action="store_true", help="Remove existing skill dirs before install")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    try:
        source = skill_pack_install_contract.load_skill_pack_source(
            repo_root,
            profile_name=args.profile,
            bundle_root_override=args.bundle_root,
        )
    except KeyError:
        raise SystemExit(f"unknown profile: {args.profile}")
    except ValueError as exc:
        raise SystemExit(str(exc))

    dest_root = skill_pack_install_contract.resolve_install_root(
        repo_root,
        install_root_override=args.dest_root,
        default_install_root=source["install_root"],
    )

    plan = {
        "profile": args.profile,
        "profile_revision": source["profile_revision"],
        "scope": source["scope"],
        "mode": args.mode,
        "source_kind": source["source_kind"],
        "bundle_root": source["bundle_root"],
        "source_root": source["source_root"],
        "dest_root": str(dest_root),
        "execute": args.execute,
        "release_identity": dict(source["release_identity"]),
        "recommended_verify_command": skill_pack_install_contract.recommended_verify_command(
            profile_name=args.profile,
            install_root=dest_root,
            bundle_root_override=pathlib.Path(source["bundle_root"]) if source["bundle_root"] else None,
            output_format="json",
        ),
        "steps": [],
    }

    for skill_entry in source["skills"]:
        source_dir = pathlib.Path(skill_entry["source_dir"])
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
        f"Scope: {source['scope']}",
        f"Profile revision: {source['profile_revision']}",
        f"Source kind: {source['source_kind']}",
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
