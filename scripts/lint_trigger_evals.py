#!/usr/bin/env python3
"""Lint the trigger-eval dataset against invocation policy and export metadata."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        items.append(json.loads(line))
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    generated_dir = repo_root / "generated"
    source_catalog = load_json(generated_dir / "skill_catalog.min.json")
    cases = load_jsonl(generated_dir / "skill_trigger_eval_cases.jsonl")
    collision_doc = load_json(generated_dir / "skill_trigger_collision_matrix.json")

    skills = {entry["name"]: entry for entry in source_catalog["skills"]}
    case_index: dict[str, list[dict[str, Any]]] = {name: [] for name in skills}
    errors: list[str] = []

    for case in cases:
        skill_name = case.get("skill_name")
        if skill_name not in skills:
            errors.append(f"unknown skill in trigger case: {skill_name!r}")
            continue
        case_index[skill_name].append(case)
        if case.get("expected_skill") is not None and case["expected_skill"] not in skills:
            errors.append(f"case {case.get('case_id')}: unknown expected_skill {case['expected_skill']!r}")
        for competing_skill in case.get("competing_skills", []):
            if competing_skill not in skills:
                errors.append(f"case {case.get('case_id')}: unknown competing skill {competing_skill!r}")

    for skill_name, entry in skills.items():
        invocation_mode = entry.get("invocation_mode")
        skill_cases = case_index[skill_name]

        explicit_positive = [
            case for case in skill_cases
            if case.get("mode") == "explicit" and case.get("expected_behavior") == "invoke-skill"
        ]
        if not explicit_positive:
            errors.append(f"{skill_name}: missing explicit positive trigger case")

        adjacent_negative = [case for case in skill_cases if case.get("mode") == "adjacent-negative"]
        if not adjacent_negative:
            errors.append(f"{skill_name}: missing adjacent-negative control")

        implicit_positive = [
            case for case in skill_cases
            if case.get("mode") == "implicit" and case.get("expected_behavior") == "invoke-skill"
        ]
        implicit_manual = [
            case for case in skill_cases
            if case.get("mode") == "implicit" and case.get("expected_behavior") == "manual-invocation-required"
        ]

        if invocation_mode == "explicit-only":
            if implicit_positive:
                errors.append(f"{skill_name}: explicit-only skills must not have implicit positive trigger cases")
            if not implicit_manual:
                errors.append(f"{skill_name}: explicit-only skills need an implicit manual-invocation-required case")
        else:
            if not implicit_positive:
                errors.append(f"{skill_name}: implicit-preferred skills need an implicit positive trigger case")
            if implicit_manual:
                errors.append(f"{skill_name}: implicit-preferred skills should not require manual invocation in implicit base cases")

    family_skills = {
        skill_name
        for family in collision_doc.get("families", [])
        for skill_name in family.get("skills", [])
    }
    if family_skills != set(skills):
        missing = sorted(set(skills) - family_skills)
        extra = sorted(family_skills - set(skills))
        if missing:
            errors.append(f"collision matrix missing skills: {missing!r}")
        if extra:
            errors.append(f"collision matrix has unknown skills: {extra!r}")

    expected_collision_case_ids = {
        case["case_id"]
        for case in collision_doc.get("cases", [])
        if case.get("case_id")
    }
    actual_collision_case_ids = {
        case.get("case_id")
        for case in cases
        if case.get("mode") == "collision" and case.get("case_id")
    }
    if expected_collision_case_ids != actual_collision_case_ids:
        missing = sorted(expected_collision_case_ids - actual_collision_case_ids)
        extra = sorted(actual_collision_case_ids - expected_collision_case_ids)
        if missing:
            errors.append(f"trigger eval dataset missing collision cases: {missing!r}")
        if extra:
            errors.append(f"trigger eval dataset has unknown collision cases: {extra!r}")

    collision_case_count = sum(1 for case in cases if case.get("mode") == "collision")
    if collision_case_count < len(skills) // 2:
        errors.append(
            f"expected at least {len(skills) // 2} collision cases, found {collision_case_count}"
        )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(cases)} trigger cases across {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
