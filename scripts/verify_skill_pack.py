#!/usr/bin/env python3
"""Verify that an installed skill pack matches the current portable export."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Mapping

import skill_pack_install_contract


def build_report(
    *,
    repo_root: pathlib.Path,
    profile_name: str,
    install_root_override: str | None,
    bundle_root_override: str | None,
    bundle_archive_override: str | None,
    strict_root: bool,
) -> dict[str, Any]:
    return skill_pack_install_contract.build_verification_report(
        repo_root=repo_root,
        profile_name=profile_name,
        install_root_override=install_root_override,
        bundle_root_override=bundle_root_override,
        bundle_archive_override=bundle_archive_override,
        strict_root=strict_root,
    )


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        f"# Skill pack verification: {report['profile']}",
        "",
        f"Verified: {report['verified']}",
        f"Profile revision: {report['profile_revision']}",
        f"Install root: {report['install_root']}",
        f"Source kind: {report['source_kind']}",
        f"Strict root: {report['strict_root']}",
        f"Expected skills: {report['expected_skill_count']}",
        f"Verified skills: {report['verified_skill_count']}",
        "",
        f"Missing skills: {', '.join(report['missing_skills']) or '-'}",
        f"Mismatched skills: {', '.join(report['mismatched_skills']) or '-'}",
        f"Extra skill dirs: {', '.join(report['extra_skill_dirs']) or '-'}",
        "",
        "## Skills",
        "",
        "| name | state | symlink | source files | target files |",
        "|---|---|---:|---:|---:|",
    ]
    for entry in report["skills"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(entry["name"]),
                    str(entry["install_state"]),
                    str(entry["is_symlink"]).lower(),
                    str(entry["source_file_count"]),
                    str(entry["target_file_count"]),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument(
        "--profile",
        required=True,
        help="Profile name from generated/skill_pack_profiles.resolved.json",
    )
    parser.add_argument(
        "--install-root",
        default=None,
        help="Override installation root for profile verification",
    )
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
    parser.add_argument(
        "--strict-root",
        action="store_true",
        help="Fail verification when extra sibling skill dirs exist under the install root",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    try:
        report = build_report(
            repo_root=repo_root,
            profile_name=args.profile,
            install_root_override=args.install_root,
            bundle_root_override=args.bundle_root,
            bundle_archive_override=args.bundle_archive,
            strict_root=args.strict_root,
        )
    except ValueError as exc:
        raise SystemExit(str(exc))
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report))
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
