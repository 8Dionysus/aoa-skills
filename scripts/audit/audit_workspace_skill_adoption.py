#!/usr/bin/env python3
"""Audit workspace-wide skill pack adoption without installing anything."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from bundles import skill_pack_install_contract


DEFAULT_PROFILE = "repo-project-foundation"
DEFAULT_TARGET_EXCLUDES = {
    ".aoa",
    ".codex",
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
}


def is_workspace_repo(path: Path) -> bool:
    return path.is_dir() and ((path / ".git").exists() or (path / "AGENTS.md").exists())


def discover_targets(workspace_root: Path, *, include_workspace_root: bool) -> list[Path]:
    targets: list[Path] = []
    if include_workspace_root:
        targets.append(workspace_root)
    for child in sorted(workspace_root.iterdir(), key=lambda item: item.name.lower()):
        if child.name in DEFAULT_TARGET_EXCLUDES or child.name.startswith("."):
            continue
        if is_workspace_repo(child):
            targets.append(child)
    return targets


def resolve_target_paths(workspace_root: Path, targets: Sequence[str]) -> list[Path]:
    resolved: list[Path] = []
    for target in targets:
        candidate = Path(target).expanduser()
        if not candidate.is_absolute():
            candidate = workspace_root / target
        resolved.append(candidate.resolve())
    return resolved


def installed_skill_dirs(install_root: Path) -> list[str]:
    if not install_root.is_dir():
        return []
    return sorted(path.name for path in install_root.iterdir() if path.is_dir())


def adoption_state(report: Mapping[str, Any], *, installed_count: int) -> str:
    if report["verified"]:
        if report["extra_skill_dirs"]:
            return "verified_with_extra_dirs"
        return "verified"
    if installed_count == 0:
        return "not_installed"
    if report["mismatched_skills"]:
        return "drift"
    if report["missing_skills"]:
        return "partial"
    return "blocked"


def target_id(workspace_root: Path, target_root: Path) -> str:
    if target_root == workspace_root:
        return "workspace-root"
    try:
        return target_root.relative_to(workspace_root).as_posix()
    except ValueError:
        return target_root.as_posix()


def audit_target(
    *,
    source_repo_root: Path,
    workspace_root: Path,
    target_root: Path,
    profile_name: str,
    strict_root: bool,
) -> dict[str, Any]:
    install_root = target_root / ".agents" / "skills"
    installed = installed_skill_dirs(install_root)
    report = skill_pack_install_contract.build_verification_report(
        repo_root=source_repo_root,
        profile_name=profile_name,
        install_root_override=str(install_root),
        bundle_root_override=None,
        bundle_archive_override=None,
        strict_root=strict_root,
    )
    state = adoption_state(report, installed_count=len(installed))
    return {
        "target": target_id(workspace_root, target_root),
        "target_root": str(target_root),
        "install_root": str(install_root),
        "profile": profile_name,
        "state": state,
        "verified": report["verified"],
        "expected_skill_count": report["expected_skill_count"],
        "verified_skill_count": report["verified_skill_count"],
        "installed_skill_count": len(installed),
        "missing_skill_count": len(report["missing_skills"]),
        "mismatched_skill_count": len(report["mismatched_skills"]),
        "extra_skill_count": len(report["extra_skill_dirs"]),
        "missing_skills": report["missing_skills"],
        "mismatched_skills": report["mismatched_skills"],
        "extra_skill_dirs": report["extra_skill_dirs"],
    }


def build_report(
    *,
    source_repo_root: Path,
    workspace_root: Path,
    profile_name: str,
    targets: Iterable[Path],
    strict_root: bool,
) -> dict[str, Any]:
    target_reports = [
        audit_target(
            source_repo_root=source_repo_root,
            workspace_root=workspace_root,
            target_root=target,
            profile_name=profile_name,
            strict_root=strict_root,
        )
        for target in targets
    ]
    states = Counter(entry["state"] for entry in target_reports)
    return {
        "schema_version": 1,
        "report_kind": "workspace_skill_adoption_audit",
        "source_repo_root": str(source_repo_root),
        "workspace_root": str(workspace_root),
        "profile": profile_name,
        "strict_root": strict_root,
        "target_count": len(target_reports),
        "summary": dict(sorted(states.items())),
        "targets": target_reports,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        f"# Workspace skill adoption audit: {report['profile']}",
        "",
        "This read-only report verifies real workspace install roots against the",
        "current `aoa-skills` portable export. It does not install, approve, or",
        "accept skills for any downstream owner.",
        "",
        f"- workspace root: `{report['workspace_root']}`",
        f"- source repo root: `{report['source_repo_root']}`",
        f"- strict root: `{str(report['strict_root']).lower()}`",
        f"- target count: {report['target_count']}",
        "",
        "## Summary",
        "",
    ]
    if report["summary"]:
        for state, count in report["summary"].items():
            lines.append(f"- `{state}`: {count}")
    else:
        lines.append("- no targets")
    lines.extend(
        [
            "",
            "## Targets",
            "",
            "| target | state | verified | expected | ok | installed | missing | drift | extra |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for entry in report["targets"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['target']}`",
                    f"`{entry['state']}`",
                    str(entry["verified"]).lower(),
                    str(entry["expected_skill_count"]),
                    str(entry["verified_skill_count"]),
                    str(entry["installed_skill_count"]),
                    str(entry["missing_skill_count"]),
                    str(entry["mismatched_skill_count"]),
                    str(entry["extra_skill_count"]),
                ]
            )
            + " |"
        )

    detail_rows = [
        entry
        for entry in report["targets"]
        if entry["missing_skills"] or entry["mismatched_skills"] or entry["extra_skill_dirs"]
    ]
    if detail_rows:
        lines.extend(["", "## Details", ""])
        for entry in detail_rows:
            lines.append(f"### `{entry['target']}`")
            lines.append("")
            lines.append(f"- install root: `{entry['install_root']}`")
            lines.append(f"- missing: {', '.join(entry['missing_skills']) or '-'}")
            lines.append(f"- drift: {', '.join(entry['mismatched_skills']) or '-'}")
            lines.append(f"- extra: {', '.join(entry['extra_skill_dirs']) or '-'}")
            lines.append("")
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        default=".",
        help="aoa-skills repository root containing the portable export",
    )
    parser.add_argument(
        "--workspace-root",
        default="..",
        help="Workspace root whose repo install surfaces should be audited",
    )
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        help="Resolved skill pack profile to verify against each target",
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Specific target repo/root path to audit; may be repeated",
    )
    parser.add_argument(
        "--no-workspace-root",
        action="store_true",
        help="When discovering targets, omit the workspace root install surface",
    )
    parser.add_argument(
        "--strict-root",
        action="store_true",
        help="Treat extra skill directories as verification failures",
    )
    parser.add_argument("--write-json", default=None, help="Optional JSON report path")
    parser.add_argument("--write-markdown", default=None, help="Optional Markdown report path")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Console output format",
    )
    args = parser.parse_args()

    source_repo_root = Path(args.repo_root).expanduser().resolve()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    if args.target:
        targets = resolve_target_paths(workspace_root, args.target)
    else:
        targets = discover_targets(
            workspace_root,
            include_workspace_root=not args.no_workspace_root,
        )

    report = build_report(
        source_repo_root=source_repo_root,
        workspace_root=workspace_root,
        profile_name=args.profile,
        targets=targets,
        strict_root=args.strict_root,
    )

    json_text = json.dumps(report, indent=2) + "\n"
    markdown_text = render_markdown(report) + "\n"

    if args.write_json:
        write_text(Path(args.write_json), json_text)
    if args.write_markdown:
        write_text(Path(args.write_markdown), markdown_text)

    if args.format == "json":
        print(json_text, end="")
    else:
        print(markdown_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
