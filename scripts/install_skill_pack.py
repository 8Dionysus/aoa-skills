#!/usr/bin/env python3
"""Install a resolved skill pack into a Codex skill root by copy or symlink."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
from typing import Any

STANDARD_INSTALL_ROOTS = {
    "repo": ".agents/skills",
    "user": "$HOME/.agents/skills",
    "admin": "/etc/codex/skills",
}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expand_root(root: str, repo_root: pathlib.Path) -> pathlib.Path:
    if root == STANDARD_INSTALL_ROOTS["repo"]:
        return repo_root / ".agents" / "skills"
    if root.startswith("$HOME/"):
        return pathlib.Path.home() / root.replace("$HOME/", "", 1)
    return pathlib.Path(root)


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
    export_root = repo_root / ".agents" / "skills"
    resolved_profiles = load_json(repo_root / "generated" / "skill_pack_profiles.resolved.json")
    profile = resolved_profiles.get("profiles", {}).get(args.profile)
    if profile is None:
        raise SystemExit(f"unknown profile: {args.profile}")

    default_dest = expand_root(profile["install_root"], repo_root)
    dest_root = pathlib.Path(args.dest_root).expanduser().resolve() if args.dest_root else default_dest.resolve()

    plan = {
        "profile": args.profile,
        "scope": profile["scope"],
        "mode": args.mode,
        "source_root": str(export_root),
        "dest_root": str(dest_root),
        "execute": args.execute,
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
        f"Mode: {args.mode}",
        f"Destination: {dest_root}",
        f"Execute: {args.execute}",
        "",
        "## Steps",
    ]
    for step in plan["steps"]:
        lines.append(f"- {step['skill']}: {step['source_dir']} -> {step['target_dir']}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
