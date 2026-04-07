#!/usr/bin/env python3
"""Read-only boundary report CLI for deterministic skill adjacency evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_boundary_surface
import skill_evaluation_contract
import skill_source_model


REPO_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_FORMATS = {"text", "json"}


class ReportSkillBoundariesError(ValueError):
    pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report deterministic adjacency coverage for local aoa-skills."
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
        "--fail-on-required-gaps",
        action="store_true",
        help="Return exit code 1 when canonical or default-reference-ready skills still have adjacency gaps.",
    )
    return parser.parse_args(argv)


def discover_skill_names(repo_root: Path) -> list[str]:
    return skill_source_model.discover_skill_names(repo_root)


def selected_skill_names(repo_root: Path, requested_skills: Sequence[str]) -> list[str]:
    available_skills = discover_skill_names(repo_root)
    if not requested_skills:
        return available_skills

    unknown_skills = sorted(set(requested_skills) - set(available_skills))
    if unknown_skills:
        raise ReportSkillBoundariesError(f"unknown skill '{unknown_skills[0]}'")
    return sorted(set(requested_skills))


def format_issues(issues: Sequence[Any]) -> str:
    lines: list[str] = []
    for issue in issues:
        location = getattr(issue, "location", None)
        message = getattr(issue, "message", None)
        if isinstance(location, str) and isinstance(message, str):
            lines.append(f"- {location}: {message}")
    return "\n".join(lines)


def validate_boundary_fixtures(repo_root: Path) -> Mapping[str, Any]:
    fixtures = skill_evaluation_contract.load_evaluation_fixtures(repo_root)
    if fixtures is None:
        raise ReportSkillBoundariesError("missing evaluation fixtures file")

    issues: list[Any] = []
    issues.extend(skill_evaluation_contract.validate_snapshot_case_contract(fixtures))
    issues.extend(skill_evaluation_contract.validate_adjacency_case_contract(fixtures))
    issues.extend(skill_evaluation_contract.validate_fixture_integrity(repo_root, fixtures))
    if issues:
        raise ReportSkillBoundariesError(
            "boundary fixture validation failed:\n" + format_issues(issues)
        )
    return fixtures


def build_payload(repo_root: Path, skill_names: Sequence[str]) -> Mapping[str, Any]:
    validate_boundary_fixtures(repo_root)
    payload = skill_boundary_surface.build_boundary_matrix_payload(repo_root, skill_names)
    if not isinstance(payload, Mapping):
        raise ReportSkillBoundariesError("boundary payload must be a mapping")
    return payload


def normalize_adjacent_skill_names(case: Mapping[str, Any]) -> list[str]:
    names: list[str] = []
    adjacent_skill = case.get("adjacent_skill")
    if isinstance(adjacent_skill, str) and adjacent_skill.strip():
        names.append(adjacent_skill.strip())

    adjacent_skills = case.get("adjacent_skills")
    if isinstance(adjacent_skills, list):
        for adjacent_skill_name in adjacent_skills:
            if isinstance(adjacent_skill_name, str) and adjacent_skill_name.strip():
                names.append(adjacent_skill_name.strip())

    return sorted(dict.fromkeys(names))


def selected_cases(
    payload: Mapping[str, Any],
    selected_skill_names: Sequence[str],
) -> list[Mapping[str, Any]]:
    skill_name_set = set(selected_skill_names)
    cases = payload.get("cases", [])
    if not isinstance(cases, list):
        raise ReportSkillBoundariesError("boundary payload field 'cases' must be a list")
    selected: list[Mapping[str, Any]] = []
    for case in cases:
        if not isinstance(case, Mapping):
            continue
        if case.get("skill") in skill_name_set:
            selected.append(case)
    return selected


def required_gap_skill_names(skill_entries: Sequence[Mapping[str, Any]]) -> list[str]:
    gap_names: list[str] = []
    for entry in skill_entries:
        if not isinstance(entry, Mapping):
            continue
        if entry.get("required_adjacency_coverage") and not entry.get("adjacency_ready"):
            name = entry.get("name")
            if isinstance(name, str):
                gap_names.append(name)
    return gap_names


def enrich_skill_entries(
    skill_entries: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    enriched_entries: list[dict[str, Any]] = []
    for entry in skill_entries:
        if not isinstance(entry, Mapping):
            continue
        required_gap = bool(
            entry.get("required_adjacency_coverage") and not entry.get("adjacency_ready")
        )
        blockers = entry.get("adjacency_blockers", [])
        blocker_values = [blocker for blocker in blockers if isinstance(blocker, str)]
        adjacency_case_count = int(entry.get("adjacency_use_count", 0)) + int(
            entry.get("adjacency_do_not_use_count", 0)
        )
        enriched_entries.append(
            {
                **dict(entry),
                "adjacency_case_count": adjacency_case_count,
                "required_adjacency_gap": required_gap,
                "required_gap_reasons": (
                    [skill_boundary_surface.ADJACENCY_REQUIRED_BLOCKER]
                    if required_gap
                    else []
                ),
                "adjacency_blockers": blocker_values,
                "adjacent_skill_names": sorted(
                    {
                        skill_name
                        for skill_name in (entry.get("adjacent_skill_names") or [])
                        if isinstance(skill_name, str) and skill_name.strip()
                    }
                ),
            }
        )
    return enriched_entries


def build_report_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    payload = build_payload(repo_root, skill_names)
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ReportSkillBoundariesError("boundary payload field 'skills' must be a list")

    enriched_skills = enrich_skill_entries(skill_entries)
    filtered_cases = selected_cases(payload, skill_names)
    filtered_cases = sorted(
        filtered_cases,
        key=lambda case: (
            str(case.get("skill") or ""),
            str(case.get("case_id") or ""),
        ),
    )
    required_gap_names = required_gap_skill_names(enriched_skills)
    summary = {
        "selected_skill_count": len(skill_names),
        "total_skill_count": len(enriched_skills),
        "required_skill_count": sum(
            1 for entry in enriched_skills if entry.get("required_adjacency_coverage")
        ),
        "required_gap_count": len(required_gap_names),
        "required_gap_skill_names": required_gap_names,
        "adjacency_case_count": len(filtered_cases),
    }

    return {
        "boundary_matrix_version": payload.get("boundary_matrix_version"),
        "source_of_truth": payload.get("source_of_truth"),
        "selected_skills": list(skill_names),
        "summary": summary,
        "skills": enriched_skills,
        "cases": [
            {
                **dict(case),
                "adjacent_skill_names": normalize_adjacent_skill_names(case),
            }
            for case in filtered_cases
        ],
    }


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
    cases = payload.get("cases", [])
    summary = payload.get("summary", {})
    if not isinstance(skills, list):
        raise ReportSkillBoundariesError("boundary report field 'skills' must be a list")
    if not isinstance(cases, list):
        raise ReportSkillBoundariesError("boundary report field 'cases' must be a list")
    if not isinstance(summary, Mapping):
        raise ReportSkillBoundariesError("boundary report field 'summary' must be a mapping")

    lines = [
        "# Skill boundary report",
        "",
        "## Summary",
        "",
        f"- selected skills: {summary.get('selected_skill_count', 0)}",
        f"- total skills: {summary.get('total_skill_count', 0)}",
        f"- required skills: {summary.get('required_skill_count', 0)}",
        f"- required adjacency gaps: {summary.get('required_gap_count', 0)}",
    ]
    gap_names = summary.get("required_gap_skill_names", [])
    if isinstance(gap_names, list) and gap_names:
        lines.append(f"- required gap skills: {', '.join(str(name) for name in gap_names)}")
    lines.extend(
        [
            "",
            "## Skills",
            "",
            "| name | status | scope | required coverage | cases | use | do_not_use | adjacent skills | ready | gap | blockers |",
            "|---|---|---|---|---:|---:|---:|---|---|---|---|",
        ]
    )
    if not skills:
        lines.append("| - | - | - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skills:
            if not isinstance(entry, Mapping):
                continue
            adjacent_skills = ", ".join(entry.get("adjacent_skill_names") or []) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["status"]),
                        str(entry["scope"]),
                        "true" if entry["required_adjacency_coverage"] else "false",
                        str(entry["adjacency_case_count"]),
                        str(entry["adjacency_use_count"]),
                        str(entry["adjacency_do_not_use_count"]),
                        adjacent_skills,
                        "true" if entry["adjacency_ready"] else "false",
                        "true" if entry["required_adjacency_gap"] else "false",
                        format_blockers_or_dash(entry["adjacency_blockers"]),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Adjacency cases",
            "",
            "| skill | adjacent skills | case id | expected | blockers |",
            "|---|---|---|---|---|",
        ]
    )
    if not cases:
        lines.append("| - | - | - | - | - |")
    else:
        for case in cases:
            if not isinstance(case, Mapping):
                continue
            adjacent_skills = ", ".join(case.get("adjacent_skill_names") or []) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(case.get("skill")),
                        adjacent_skills,
                        str(case.get("case_id")),
                        str(case.get("expected")),
                        format_blockers_or_dash(case.get("blockers", [])),
                    ]
                )
                + " |"
            )
    lines.append("")
    return "\n".join(lines)


def render_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.format not in SUPPORTED_FORMATS:
            raise ReportSkillBoundariesError(f"unknown format '{args.format}'")

        skill_names = selected_skill_names(repo_root, args.skill)
        payload = build_report_payload(repo_root, skill_names)

        if args.format == "json":
            sys.stdout.write(render_json(payload))
        else:
            sys.stdout.write(render_text(payload) + "\n")

        if args.fail_on_required_gaps and payload["summary"]["required_gap_count"] > 0:
            return 1
    except ReportSkillBoundariesError as exc:
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
