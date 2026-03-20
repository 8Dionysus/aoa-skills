#!/usr/bin/env python3
"""Preview or apply upstream technique refreshes for explicitly named skills."""

from __future__ import annotations

import argparse
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import refresh_skill_from_manifest
import technique_bridge_tools


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TechniqueUpdateSummary:
    technique_id: str
    path: str
    old_ref: str
    new_ref: str
    state: str
    commit_summaries: tuple[str, ...]


@dataclass(frozen=True)
class SkillRefreshResult:
    skill_name: str
    techniques_path: Path
    skill_md_path: Path
    target_ref: str
    manifest_text: str
    skill_text: str
    manifest_changed: bool
    skill_changed: bool
    bridge_coverage_complete: bool
    coverage_gaps: tuple[str, ...]
    technique_updates: tuple[TechniqueUpdateSummary, ...]
    manifest_diff: str
    skill_diff: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or apply upstream technique refreshes for named skills."
    )
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Refresh an explicitly named skill. Repeatable.",
    )
    parser.add_argument(
        "--techniques-repo",
        default=str(technique_bridge_tools.DEFAULT_TECHNIQUES_REPO),
        help="Path to the local aoa-techniques checkout.",
    )
    parser.add_argument(
        "--target-ref",
        default="HEAD",
        help="Git ref in aoa-techniques to refresh against. Defaults to HEAD.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply the refresh to the explicitly named skills.",
    )
    return parser.parse_args(argv)


def build_refresh_result(
    repo_root: Path,
    techniques_repo: Path,
    target_ref: str,
    skill_name: str,
) -> SkillRefreshResult:
    bundle = technique_bridge_tools.load_skill_bundle(repo_root, skill_name)
    metadata, frontmatter_lines, body_text = (
        refresh_skill_from_manifest.parse_skill_document(bundle.skill_md_path)
    )
    drift_records = technique_bridge_tools.collect_drift_records(
        techniques_repo,
        target_ref,
        bundle,
    )
    updated_manifest, _ = technique_bridge_tools.copy_manifest_with_target_ref(
        bundle.manifest,
        target_ref,
    )

    proposed_frontmatter_lines = (
        refresh_skill_from_manifest.replace_technique_dependencies(
            frontmatter_lines,
            [
                technique["id"]
                for technique in updated_manifest["techniques"]
            ],
        )
    )
    proposed_body = refresh_skill_from_manifest.replace_traceability_section(
        body_text,
        updated_manifest["techniques"],
    )
    proposed_skill_text = refresh_skill_from_manifest.render_skill_document(
        proposed_frontmatter_lines,
        proposed_body,
    )
    proposed_manifest_text = technique_bridge_tools.render_yaml(updated_manifest)
    coverage_gaps = refresh_skill_from_manifest.build_bridge_coverage_gaps(
        metadata,
        body_text,
        updated_manifest["techniques"],
    )

    current_manifest_text = bundle.techniques_path.read_text(encoding="utf-8")
    current_skill_text = bundle.skill_md_path.read_text(encoding="utf-8")
    manifest_diff = "\n".join(
        difflib.unified_diff(
            current_manifest_text.splitlines(),
            proposed_manifest_text.splitlines(),
            fromfile=(
                f"current/{technique_bridge_tools.relative_location(bundle.techniques_path, repo_root)}"
            ),
            tofile=(
                f"proposed/{technique_bridge_tools.relative_location(bundle.techniques_path, repo_root)}"
            ),
            lineterm="",
        )
    )
    skill_diff = "\n".join(
        difflib.unified_diff(
            current_skill_text.splitlines(),
            proposed_skill_text.splitlines(),
            fromfile=(
                f"current/{technique_bridge_tools.relative_location(bundle.skill_md_path, repo_root)}"
            ),
            tofile=(
                f"proposed/{technique_bridge_tools.relative_location(bundle.skill_md_path, repo_root)}"
            ),
            lineterm="",
        )
    )

    technique_updates: list[TechniqueUpdateSummary] = []
    for record in drift_records:
        commit_summaries: tuple[str, ...] = ()
        if record.state == "drifted":
            commit_summaries = tuple(
                technique_bridge_tools.collect_commit_summaries_for_path(
                    techniques_repo,
                    record.pinned_ref,
                    target_ref,
                    record.path,
                )
            )
        technique_updates.append(
            TechniqueUpdateSummary(
                technique_id=record.technique_id,
                path=record.path,
                old_ref=record.pinned_ref,
                new_ref=target_ref,
                state=record.state,
                commit_summaries=commit_summaries,
            )
        )

    return SkillRefreshResult(
        skill_name=skill_name,
        techniques_path=bundle.techniques_path,
        skill_md_path=bundle.skill_md_path,
        target_ref=target_ref,
        manifest_text=proposed_manifest_text,
        skill_text=proposed_skill_text,
        manifest_changed=bool(manifest_diff),
        skill_changed=bool(skill_diff),
        bridge_coverage_complete=not coverage_gaps,
        coverage_gaps=coverage_gaps,
        technique_updates=tuple(technique_updates),
        manifest_diff=manifest_diff,
        skill_diff=skill_diff,
    )


def build_preview_report(
    techniques_repo: Path,
    results: list[SkillRefreshResult],
) -> str:
    lines = [f"Techniques repo: {techniques_repo}"]
    for result in results:
        lines.extend(
            [
                "",
                f"Skill: {result.skill_name}",
                f"Target ref: {result.target_ref}",
                (
                    "Refresh status: needs refresh"
                    if result.manifest_changed or result.skill_changed
                    else "Refresh status: already aligned"
                ),
                (
                    "Bridge coverage: complete"
                    if result.bridge_coverage_complete
                    else "Bridge coverage: gaps detected"
                ),
            ]
        )
        if result.coverage_gaps:
            lines.append("Coverage gaps:")
            lines.extend(f"- {gap}" for gap in result.coverage_gaps)

        lines.append("Technique refs:")
        for update in result.technique_updates:
            lines.append(
                "- "
                f"{update.technique_id} | path={update.path} | "
                f"old_ref={update.old_ref} | new_ref={update.new_ref} | "
                f"state={update.state}"
            )
            if update.commit_summaries:
                lines.append("  Upstream commits:")
                lines.extend(f"  - {summary}" for summary in update.commit_summaries)

        lines.append("Manifest diff:")
        lines.append(result.manifest_diff or "Status: already aligned")
        lines.append("Skill diff:")
        lines.append(result.skill_diff or "Status: already aligned")
    return "\n".join(lines)


def build_write_report(
    techniques_repo: Path,
    results: list[SkillRefreshResult],
    repo_root: Path,
) -> str:
    lines = [f"Techniques repo: {techniques_repo}"]
    for result in results:
        lines.extend(
            [
                "",
                f"Skill: {result.skill_name}",
                f"Target ref: {result.target_ref}",
                (
                    "Write result: refreshed"
                    if result.manifest_changed or result.skill_changed
                    else "Write result: already aligned"
                ),
                (
                    "Bridge coverage: complete"
                    if result.bridge_coverage_complete
                    else "Bridge coverage: gaps detected"
                ),
            ]
        )
        if result.coverage_gaps:
            lines.append("Coverage gaps:")
            lines.extend(f"- {gap}" for gap in result.coverage_gaps)
        if result.manifest_changed:
            lines.append(
                "Updated manifest: "
                f"{technique_bridge_tools.relative_location(result.techniques_path, repo_root)}"
            )
        if result.skill_changed:
            lines.append(
                "Updated skill: "
                f"{technique_bridge_tools.relative_location(result.skill_md_path, repo_root)}"
            )
    return "\n".join(lines)


def write_results(results: list[SkillRefreshResult]) -> None:
    for result in results:
        if result.manifest_changed:
            result.techniques_path.write_text(
                result.manifest_text,
                encoding="utf-8",
                newline="\n",
            )
        if result.skill_changed:
            refresh_skill_from_manifest.write_skill_document(
                result.skill_md_path,
                result.skill_text,
            )


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if not args.skills:
            print(
                "Runtime error: refresh requires --skill so the workflow stays bounded "
                "to explicitly named bundles.",
                file=sys.stderr,
            )
            return 2

        techniques_repo = technique_bridge_tools.resolve_techniques_repo(
            Path(args.techniques_repo)
        )
        target_ref = technique_bridge_tools.resolve_git_ref(
            techniques_repo,
            args.target_ref,
        )
        skill_names = technique_bridge_tools.resolve_skill_names(repo_root, args.skills)
        results = [
            build_refresh_result(repo_root, techniques_repo, target_ref, skill_name)
            for skill_name in skill_names
        ]
        if args.write:
            write_results(results)
            print(build_write_report(techniques_repo, results, repo_root))
            return 0
    except (RuntimeError, ValueError, FileNotFoundError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(build_preview_report(techniques_repo, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
