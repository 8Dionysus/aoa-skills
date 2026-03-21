#!/usr/bin/env python3
"""Read-only report CLI for deterministic skill evaluation evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_evaluation_surface


REPO_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_FORMATS = {"text", "json"}


class ReportSkillEvaluationError(ValueError):
    pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report deterministic evaluation coverage for local aoa-skills."
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Skill directory name. Repeat to limit the report to specific skills.",
    )
    parser.add_argument(
        "--format",
        default="text",
        help="One of: text, json.",
    )
    parser.add_argument(
        "--fail-on-canonical-gaps",
        action="store_true",
        help="Return exit code 1 when canonical skills still have evaluation gaps.",
    )
    return parser.parse_args(argv)


def discover_skill_names(repo_root: Path) -> list[str]:
    return skill_evaluation_surface.discover_skill_names(repo_root)


def selected_skill_names(repo_root: Path, requested_skills: Sequence[str]) -> list[str]:
    available_skills = discover_skill_names(repo_root)
    if not requested_skills:
        return available_skills

    unknown_skills = sorted(set(requested_skills) - set(available_skills))
    if unknown_skills:
        raise ReportSkillEvaluationError(f"unknown skill '{unknown_skills[0]}'")
    return sorted(set(requested_skills))


def build_payload(repo_root: Path, skill_names: Sequence[str]) -> Mapping[str, Any]:
    return skill_evaluation_surface.build_evaluation_matrix_payload(repo_root, skill_names)


def canonical_gaps_present(payload: Mapping[str, Any]) -> bool:
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        raise ReportSkillEvaluationError("evaluation matrix field 'skills' must be a list")
    for entry in skills:
        if not isinstance(entry, Mapping):
            continue
        if entry.get("status") == "canonical" and not entry.get("canonical_eval_ready"):
            return True
    return False


def format_path_or_dash(path_value: Any) -> str:
    if isinstance(path_value, str) and path_value:
        return path_value
    return "-"


def format_blockers_or_dash(blockers: Sequence[Any]) -> str:
    blocker_values = [blocker for blocker in blockers if isinstance(blocker, str)]
    if blocker_values:
        return ", ".join(blocker_values)
    return "-"


def render_text(payload: Mapping[str, Any]) -> str:
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        raise ReportSkillEvaluationError("evaluation matrix field 'skills' must be a list")

    lines = [
        "# Skill evaluation report",
        "",
    ]
    for entry in skills:
        if not isinstance(entry, Mapping):
            continue
        lines.extend(
            [
                f"## {entry['name']}",
                "",
                f"- status: {entry['status']}",
                f"- scope: {entry['scope']}",
                f"- invocation mode: {entry['invocation_mode']}",
                f"- skill path: {entry['skill_path']}",
                (
                    "- coverage: "
                    f"autonomy={entry['autonomy_check_count']} "
                    f"use_cases={entry['use_case_count']} "
                    f"do_not_use_cases={entry['do_not_use_case_count']} "
                    f"use_snapshots={entry['use_snapshot_count']} "
                    f"do_not_use_snapshots={entry['do_not_use_snapshot_count']}"
                ),
                (
                    "- selected runtime artifact: "
                    f"{format_path_or_dash(entry['selected_runtime_artifact_path'])}"
                ),
                f"- promotion review: {format_path_or_dash(entry['promotion_review_path'])}",
                f"- candidate review: {format_path_or_dash(entry['candidate_review_path'])}",
                (
                    "- canonical eval ready: "
                    f"{'true' if entry['canonical_eval_ready'] else 'false'}"
                ),
                f"- blockers: {format_blockers_or_dash(entry['canonical_eval_blockers'])}",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def render_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.format not in SUPPORTED_FORMATS:
            raise ReportSkillEvaluationError(f"unknown format '{args.format}'")

        skill_names = selected_skill_names(repo_root, args.skill)
        payload = build_payload(repo_root, skill_names)
        if args.format == "json":
            sys.stdout.write(render_json(payload))
        else:
            sys.stdout.write(render_text(payload) + "\n")

        if args.fail_on_canonical_gaps and canonical_gaps_present(payload):
            return 1
    except ReportSkillEvaluationError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
