#!/usr/bin/env python3
"""Verify that an installed skill pack matches the current portable export."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from typing import Any, Mapping

import release_manifest_contract
import skill_pack_install_contract


def build_directory_snapshot(root_dir: pathlib.Path) -> dict[str, Any]:
    resolved_root = root_dir.resolve()
    if not resolved_root.is_dir():
        raise ValueError(f"directory snapshot requires a directory: {root_dir}")

    digest = hashlib.sha256()
    file_records: list[dict[str, Any]] = []
    ordered_paths = sorted(
        (path for path in resolved_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(resolved_root).as_posix(),
    )
    for path in ordered_paths:
        relative_path = path.relative_to(resolved_root).as_posix()
        data = release_manifest_contract.normalized_file_bytes(path)
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
        file_records.append(
            {
                "path": relative_path,
                "sha256": release_manifest_contract.sha256_bytes(data),
                "bytes": len(data),
            }
        )
    return {
        "digest": digest.hexdigest(),
        "file_count": len(file_records),
        "files": file_records,
    }


def verify_skill_install(
    *,
    skill_name: str,
    source_dir: pathlib.Path,
    target_dir: pathlib.Path,
) -> dict[str, Any]:
    if not source_dir.is_dir():
        raise ValueError(f"missing source skill export: {source_dir}")

    source_snapshot = build_directory_snapshot(source_dir)
    is_symlink = target_dir.is_symlink()

    if not target_dir.exists():
        return {
            "name": skill_name,
            "source_dir": str(source_dir),
            "target_dir": str(target_dir),
            "install_state": "missing",
            "source_file_count": source_snapshot["file_count"],
            "target_file_count": 0,
            "source_digest": source_snapshot["digest"],
            "target_digest": None,
            "is_symlink": False,
        }

    if not target_dir.resolve().is_dir():
        return {
            "name": skill_name,
            "source_dir": str(source_dir),
            "target_dir": str(target_dir),
            "install_state": "mismatch",
            "source_file_count": source_snapshot["file_count"],
            "target_file_count": 0,
            "source_digest": source_snapshot["digest"],
            "target_digest": None,
            "is_symlink": is_symlink,
        }

    target_snapshot = build_directory_snapshot(target_dir)
    install_state = (
        "ok" if source_snapshot["files"] == target_snapshot["files"] else "mismatch"
    )
    return {
        "name": skill_name,
        "source_dir": str(source_dir),
        "target_dir": str(target_dir),
        "install_state": install_state,
        "source_file_count": source_snapshot["file_count"],
        "target_file_count": target_snapshot["file_count"],
        "source_digest": source_snapshot["digest"],
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
    strict_root: bool,
) -> dict[str, Any]:
    try:
        profile = skill_pack_install_contract.load_resolved_profile(repo_root, profile_name)
    except KeyError:
        raise SystemExit(f"unknown profile: {profile_name}")

    release_manifest = skill_pack_install_contract.load_release_manifest(repo_root)
    profile_revision = skill_pack_install_contract.load_install_profile_revision(
        release_manifest,
        profile_name,
    )["profile_revision"]
    install_root = skill_pack_install_contract.resolve_install_root(
        repo_root,
        install_root_override=install_root_override,
        default_install_root=profile["install_root"],
    )
    export_root = skill_pack_install_contract.export_root(repo_root)

    skills: list[dict[str, Any]] = []
    for skill_entry in profile["skills"]:
        skill_name = skill_entry["name"]
        skills.append(
            verify_skill_install(
                skill_name=skill_name,
                source_dir=export_root / skill_name,
                target_dir=install_root / skill_name,
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
        "profile_revision": profile_revision,
        "install_root": str(install_root),
        "strict_root": strict_root,
        "verified": verified,
        "expected_skill_count": len(skills),
        "verified_skill_count": sum(1 for entry in skills if entry["install_state"] == "ok"),
        "missing_skills": missing_skills,
        "mismatched_skills": mismatched_skills,
        "extra_skill_dirs": extra_dirs,
        "release_identity": dict(skill_pack_install_contract.release_identity(release_manifest)),
        "skills": skills,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        f"# Skill pack verification: {report['profile']}",
        "",
        f"Verified: {report['verified']}",
        f"Profile revision: {report['profile_revision']}",
        f"Install root: {report['install_root']}",
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
        strict_root=args.strict_root,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report))
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
