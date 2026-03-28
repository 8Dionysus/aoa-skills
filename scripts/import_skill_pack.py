#!/usr/bin/env python3
"""Inspect, optionally install, and optionally verify a staged skill bundle."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Mapping

import skill_pack_install_contract


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        f"# Skill pack import: {report['profile']}",
        "",
        f"Verified: {report['verified']}",
        f"Profile revision: {report['profile_revision']}",
        f"Source kind: {report['source_kind']}",
        f"Bundle root: {report['bundle_root'] or '-'}",
        f"Bundle archive: {report['bundle_archive'] or '-'}",
        f"Destination: {report['dest_root']}",
        f"Mode: {report['mode']}",
        f"Strict root: {report['strict_root']}",
        f"Execute: {report['execute']}",
        "",
        "## Inspection",
        "",
        f"- verified: {report['inspection']['verified']}",
        f"- missing files: {', '.join(report['inspection']['missing_files']) or '-'}",
        f"- mismatched files: {', '.join(report['inspection']['mismatched_files']) or '-'}",
        f"- extra files: {', '.join(report['inspection']['extra_files']) or '-'}",
        "",
        "## Install",
        "",
        f"- execute: {report['install']['execute']}",
        f"- recommended verify: {report['install']['recommended_verify_command']}",
        "",
        "## Steps",
    ]
    for step in report["install"]["steps"]:
        lines.append(f"- {step['skill']}: {step['source_dir']} -> {step['target_dir']}")
    verification = report["verification"]
    if verification is not None:
        lines.extend(
            [
                "",
                "## Verification",
                "",
                f"- verified: {verification['verified']}",
                f"- missing skills: {', '.join(verification['missing_skills']) or '-'}",
                f"- mismatched skills: {', '.join(verification['mismatched_skills']) or '-'}",
                f"- extra skill dirs: {', '.join(verification['extra_skill_dirs']) or '-'}",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root containing .agents/skills")
    parser.add_argument("--profile", required=True, help="Profile name from bundle_manifest.json")
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--bundle-root",
        default=None,
        help="Staged profile-bundle root containing bundle_manifest.json",
    )
    source_group.add_argument(
        "--bundle-archive",
        default=None,
        help="ZIP handoff archive containing one staged profile bundle",
    )
    parser.add_argument("--dest-root", default=None, help="Override destination root for imported skills")
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy", help="Install mode")
    parser.add_argument("--overwrite", action="store_true", help="Remove existing skill dirs before install")
    parser.add_argument(
        "--strict-root",
        action="store_true",
        help="Fail verification when extra sibling skill dirs exist under the install root",
    )
    parser.add_argument("--execute", action="store_true", help="Apply install and verification after inspection")
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
    except (KeyError, ValueError) as exc:
        raise SystemExit(str(exc))

    try:
        with source_context as source:
            inspection_root = source.get("inspection_root")
            if inspection_root is None:
                raise SystemExit("import_skill_pack.py requires a bundle-root or bundle-archive source")

            dest_root = skill_pack_install_contract.resolve_install_root(
                repo_root,
                install_root_override=args.dest_root,
                default_install_root=source["install_root"],
            )
            inspection = skill_pack_install_contract.inspect_bundle_root(
                inspection_root,
                source_kind=source["source_kind"],
                bundle_archive_override=source["bundle_archive"],
            )
            install = skill_pack_install_contract.build_install_plan(
                profile_name=args.profile,
                source=source,
                dest_root=dest_root,
                mode=args.mode,
                execute=args.execute,
            )
            verification = None
            report = skill_pack_install_contract.build_import_report(
                source=source,
                dest_root=dest_root,
                mode=args.mode,
                strict_root=args.strict_root,
                execute=args.execute,
                inspection=inspection,
                install=install,
                verification=verification,
            )

            if args.execute and inspection["verified"]:
                skill_pack_install_contract.execute_install_plan(
                    install,
                    overwrite=args.overwrite,
                )
                verification = skill_pack_install_contract.build_verification_report(
                    repo_root=repo_root,
                    profile_name=args.profile,
                    install_root_override=str(dest_root),
                    bundle_root_override=args.bundle_root,
                    bundle_archive_override=args.bundle_archive,
                    strict_root=args.strict_root,
                )
                report = skill_pack_install_contract.build_import_report(
                    source=source,
                    dest_root=dest_root,
                    mode=args.mode,
                    strict_root=args.strict_root,
                    execute=args.execute,
                    inspection=inspection,
                    install=install,
                    verification=verification,
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
