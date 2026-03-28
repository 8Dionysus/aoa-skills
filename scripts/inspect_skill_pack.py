#!/usr/bin/env python3
"""Inspect a staged skill bundle directory or ZIP handoff."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping

import skill_pack_install_contract


def build_report(
    *,
    bundle_root_override: str | None,
    bundle_archive_override: str | None,
) -> dict[str, Any]:
    try:
        context = skill_pack_install_contract.bundle_inspection_context(
            bundle_root_override=bundle_root_override,
            bundle_archive_override=bundle_archive_override,
        )
    except ValueError as exc:
        raise SystemExit(str(exc))

    with context as source:
        return skill_pack_install_contract.inspect_bundle_root(
            source["inspection_root"],
            source_kind=source["source_kind"],
            bundle_archive_override=source["bundle_archive"],
        )


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        f"# Skill pack inspection: {report['profile']}",
        "",
        f"Verified: {report['verified']}",
        f"Source kind: {report['source_kind']}",
        f"Bundle root: {report['bundle_root'] or '-'}",
        f"Bundle archive: {report['bundle_archive'] or '-'}",
        f"Profile revision: {report['profile_revision']}",
        f"Skill count: {report['skill_count']}",
        f"Manifest files: {report['manifest_file_count']}",
        f"Actual files: {report['actual_file_count']}",
        f"Bundle digest: {report['bundle_digest']}",
        f"Bundle digest matches: {report['bundle_digest_matches_manifest']}",
    ]
    if report.get("archive_sha256") is not None:
        lines.extend(
            [
                f"Archive sha256: {report['archive_sha256']}",
                f"Archive bytes: {report['archive_bytes']}",
            ]
        )
    lines.extend(
        [
            "",
            f"Missing files: {', '.join(report['missing_files']) or '-'}",
            f"Mismatched files: {', '.join(report['mismatched_files']) or '-'}",
            f"Extra files: {', '.join(report['extra_files']) or '-'}",
            "",
            "## Skills",
            "",
            "| name | state | expected files | actual files |",
            "|---|---|---:|---:|",
        ]
    )
    for entry in report["skills"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(entry["name"]),
                    str(entry["skill_state"]),
                    str(entry["expected_file_count"]),
                    str(entry["actual_file_count"]),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    args = parser.parse_args()

    try:
        report = build_report(
            bundle_root_override=args.bundle_root,
            bundle_archive_override=args.bundle_archive,
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
