#!/usr/bin/env python3
"""Verify that an installed skill pack matches the current portable export."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Mapping

import skill_pack_install_contract


def build_directory_snapshot(root_dir: pathlib.Path) -> dict[str, Any]:
    if not root_dir.resolve().is_dir():
        raise ValueError(f"directory snapshot requires a directory: {root_dir}")
    payloads = skill_pack_install_contract.iter_directory_file_payloads(root_dir)
    file_records = skill_pack_install_contract.file_digests_from_payloads(payloads)
    return {
        "digest": skill_pack_install_contract.record_digest(file_records),
        "file_count": len(file_records),
        "files": file_records,
    }


def verify_skill_install(
    *,
    skill_name: str,
    source_dir: pathlib.Path,
    target_dir: pathlib.Path,
    expected_files: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    source_matches_expected = True
    if expected_files is None:
        if not source_dir.is_dir():
            raise ValueError(f"missing source skill export: {source_dir}")
        expected_files = build_directory_snapshot(source_dir)["files"]
    elif source_dir.exists() and source_dir.resolve().is_dir():
        source_matches_expected = (
            build_directory_snapshot(source_dir)["files"] == expected_files
        )
    else:
        source_matches_expected = False

    if expected_files is None:
        raise ValueError(f"missing source skill export: {source_dir}")
    is_symlink = target_dir.is_symlink()
    source_digest = skill_pack_install_contract.record_digest(expected_files)

    if not target_dir.exists():
        return {
            "name": skill_name,
            "source_dir": str(source_dir),
            "target_dir": str(target_dir),
            "install_state": "missing",
            "source_file_count": len(expected_files),
            "target_file_count": 0,
            "source_digest": source_digest,
            "target_digest": None,
            "is_symlink": False,
        }

    if not target_dir.resolve().is_dir():
        return {
            "name": skill_name,
            "source_dir": str(source_dir),
            "target_dir": str(target_dir),
            "install_state": "mismatch",
            "source_file_count": len(expected_files),
            "target_file_count": 0,
            "source_digest": source_digest,
            "target_digest": None,
            "is_symlink": is_symlink,
        }

    target_snapshot = build_directory_snapshot(target_dir)
    install_state = (
        "ok"
        if source_matches_expected and expected_files == target_snapshot["files"]
        else "mismatch"
    )
    return {
        "name": skill_name,
        "source_dir": str(source_dir),
        "target_dir": str(target_dir),
        "install_state": install_state,
        "source_file_count": len(expected_files),
        "target_file_count": target_snapshot["file_count"],
        "source_digest": source_digest,
        "target_digest": target_snapshot["digest"],
        "is_symlink": is_symlink,
    }


def extra_skill_dirs(install_root: pathlib.Path, expected_skill_names: set[str]) -> list[str]:
    if not install_root.exists() or not install_root.is_dir():
        return []
    extras: list[str] = []
    for candidate in sorted(install_root.iterdir(), key=lambda path: path.name):
        if candidate.name in expected_skill_names:
            continue
        if candidate.is_dir():
            extras.append(candidate.name)
    return extras


def build_report(
    *,
    repo_root: pathlib.Path,
    profile_name: str,
    install_root_override: str | None,
    bundle_root_override: str | None,
    strict_root: bool,
) -> dict[str, Any]:
    try:
        source = skill_pack_install_contract.load_skill_pack_source(
            repo_root,
            profile_name=profile_name,
            bundle_root_override=bundle_root_override,
        )
    except KeyError:
        raise SystemExit(f"unknown profile: {profile_name}")
    except ValueError as exc:
        raise SystemExit(str(exc))

    install_root = skill_pack_install_contract.resolve_install_root(
        repo_root,
        install_root_override=install_root_override,
        default_install_root=source["install_root"],
    )

    skills: list[dict[str, Any]] = []
    for skill_entry in source["skills"]:
        skill_name = skill_entry["name"]
        skills.append(
            verify_skill_install(
                skill_name=skill_name,
                source_dir=pathlib.Path(skill_entry["source_dir"]),
                target_dir=install_root / skill_name,
                expected_files=skill_entry["expected_files"],
            )
        )

    missing_skills = [
        entry["name"] for entry in skills if entry["install_state"] == "missing"
    ]
    mismatched_skills = [
        entry["name"] for entry in skills if entry["install_state"] == "mismatch"
    ]
    extra_dirs = extra_skill_dirs(
        install_root,
        {entry["name"] for entry in skills},
    )
    verified = not missing_skills and not mismatched_skills and (
        not strict_root or not extra_dirs
    )
    return {
        "profile": profile_name,
        "profile_revision": source["profile_revision"],
        "install_root": str(install_root),
        "source_kind": source["source_kind"],
        "bundle_root": source["bundle_root"],
        "strict_root": strict_root,
        "verified": verified,
        "expected_skill_count": len(skills),
        "verified_skill_count": sum(1 for entry in skills if entry["install_state"] == "ok"),
        "missing_skills": missing_skills,
        "mismatched_skills": mismatched_skills,
        "extra_skill_dirs": extra_dirs,
        "release_identity": dict(source["release_identity"]),
        "skills": skills,
    }


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
    parser.add_argument(
        "--bundle-root",
        default=None,
        help="Optional staged profile-bundle root containing bundle_manifest.json",
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
    report = build_report(
        repo_root=repo_root,
        profile_name=args.profile,
        install_root_override=args.install_root,
        bundle_root_override=args.bundle_root,
        strict_root=args.strict_root,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report))
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
