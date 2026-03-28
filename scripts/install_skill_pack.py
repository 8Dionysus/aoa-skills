#!/usr/bin/env python3
"""Install a resolved skill pack into a Codex skill root by copy or symlink."""

from __future__ import annotations

import argparse
import json
import pathlib

import skill_pack_install_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument("--profile", required=True, help="Profile name from generated/skill_pack_profiles.resolved.json")
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--bundle-root",
        default=None,
        help="Optional staged profile-bundle root containing bundle_manifest.json",
    )
    source_group.add_argument(
        "--bundle-archive",
        default=None,
        help="Optional ZIP handoff archive containing one staged profile bundle",
    )
    parser.add_argument("--dest-root", default=None, help="Override destination root for installed skills")
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink", help="Install mode")
    parser.add_argument("--execute", action="store_true", help="Apply the install plan")
    parser.add_argument("--overwrite", action="store_true", help="Remove existing skill dirs before install")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    try:
        source_context = skill_pack_install_contract.skill_pack_source_context(
            repo_root,
            profile_name=args.profile,
            bundle_root_override=args.bundle_root,
            bundle_archive_override=args.bundle_archive,
        )
    except KeyError:
        raise SystemExit(f"unknown profile: {args.profile}")
    except ValueError as exc:
        raise SystemExit(str(exc))

    try:
        with source_context as source:
            dest_root = skill_pack_install_contract.resolve_install_root(
                repo_root,
                install_root_override=args.dest_root,
                default_install_root=source["install_root"],
            )
            plan = skill_pack_install_contract.build_install_plan(
                profile_name=args.profile,
                source=source,
                dest_root=dest_root,
                mode=args.mode,
                execute=args.execute,
            )

            if args.execute:
                skill_pack_install_contract.execute_install_plan(
                    plan,
                    overwrite=args.overwrite,
                )

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
    except ValueError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
