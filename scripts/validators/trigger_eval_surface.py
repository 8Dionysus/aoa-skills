"""Trigger-eval and description-trigger validators for aoa-skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from skill_activation_policy import (
    allow_implicit_invocation,
    required_case_classes as activation_required_case_classes,
    resolve_implicit_activation_policy,
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_trigger_case_refs(
    *,
    cases: Sequence[dict[str, Any]],
    skills: dict[str, Any],
    errors: list[str],
) -> dict[str, list[dict[str, Any]]]:
    case_index: dict[str, list[dict[str, Any]]] = {name: [] for name in skills}
    for case in cases:
        skill_name = case.get("skill_name")
        if skill_name not in skills:
            errors.append(f"unknown skill in trigger case: {skill_name!r}")
            continue
        case_index[skill_name].append(case)
        if case.get("expected_skill") is not None and case["expected_skill"] not in skills:
            errors.append(
                f"case {case.get('case_id')}: unknown expected_skill "
                f"{case['expected_skill']!r}"
            )
        for competing_skill in case.get("competing_skills", []):
            if competing_skill not in skills:
                errors.append(
                    f"case {case.get('case_id')}: unknown competing skill "
                    f"{competing_skill!r}"
                )
    return case_index


def validate_trigger_policy_coverage(
    *,
    skills: dict[str, Any],
    policy_doc: dict[str, Any],
    case_index: dict[str, list[dict[str, Any]]],
    errors: list[str],
) -> None:
    for skill_name in skills:
        policy_entry = policy_doc.get("skills", {}).get(skill_name)
        allow_implicit = allow_implicit_invocation(policy_entry, skill_name)
        skill_cases = case_index[skill_name]
        explicit_positive = [
            case
            for case in skill_cases
            if case.get("mode") == "explicit"
            and case.get("expected_behavior") == "invoke-skill"
        ]
        adjacent_negative = [
            case for case in skill_cases if case.get("mode") == "adjacent-negative"
        ]
        implicit_positive = [
            case
            for case in skill_cases
            if case.get("mode") == "implicit"
            and case.get("expected_behavior") == "invoke-skill"
        ]
        collision_positive = [
            case
            for case in skill_cases
            if case.get("mode") == "collision"
            and case.get("expected_behavior") == "invoke-skill"
        ]
        implicit_manual = [
            case
            for case in skill_cases
            if case.get("mode") == "implicit"
            and case.get("expected_behavior") == "manual-invocation-required"
        ]
        validate_trigger_skill_case_mix(
            skill_name=skill_name,
            allow_implicit=allow_implicit,
            explicit_positive=explicit_positive,
            adjacent_negative=adjacent_negative,
            implicit_positive=implicit_positive,
            collision_positive=collision_positive,
            implicit_manual=implicit_manual,
            errors=errors,
        )


def validate_trigger_skill_case_mix(
    *,
    skill_name: str,
    allow_implicit: bool,
    explicit_positive: Sequence[dict[str, Any]],
    adjacent_negative: Sequence[dict[str, Any]],
    implicit_positive: Sequence[dict[str, Any]],
    collision_positive: Sequence[dict[str, Any]],
    implicit_manual: Sequence[dict[str, Any]],
    errors: list[str],
) -> None:
    if not explicit_positive:
        errors.append(f"{skill_name}: missing explicit positive trigger case")
    if not adjacent_negative:
        errors.append(f"{skill_name}: missing adjacent-negative control")
    if not allow_implicit:
        if implicit_positive:
            errors.append(
                f"{skill_name}: non-invoke skills must not have implicit positive trigger cases"
            )
        if collision_positive:
            errors.append(
                f"{skill_name}: non-invoke skills must not have collision positive trigger cases"
            )
        if not implicit_manual:
            errors.append(
                f"{skill_name}: non-invoke skills need an implicit manual-invocation-required case"
            )
    else:
        if not implicit_positive:
            errors.append(f"{skill_name}: invoke-policy skills need an implicit positive trigger case")
        if implicit_manual:
            errors.append(
                f"{skill_name}: invoke-policy skills should not require manual invocation "
                "in implicit base cases"
            )


def validate_collision_matrix(
    *,
    collision_doc: dict[str, Any],
    skills: dict[str, Any],
    cases: Sequence[dict[str, Any]],
    errors: list[str],
) -> None:
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
        case["case_id"] for case in collision_doc.get("cases", []) if case.get("case_id")
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


def lint_trigger_evals(repo_root: Path) -> tuple[list[str], int, int]:
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"
    source_catalog = load_json(generated_dir / "skill_catalog.min.json")
    policy_doc = load_json(config_dir / "skill_policy_matrix.json")
    cases = load_jsonl(generated_dir / "skill_trigger_eval_cases.jsonl")
    collision_doc = load_json(generated_dir / "skill_trigger_collision_matrix.json")
    skills = {entry["name"]: entry for entry in source_catalog["skills"]}
    errors: list[str] = []
    case_index = validate_trigger_case_refs(cases=cases, skills=skills, errors=errors)
    validate_trigger_policy_coverage(
        skills=skills,
        policy_doc=policy_doc,
        case_index=case_index,
        errors=errors,
    )
    validate_collision_matrix(
        collision_doc=collision_doc,
        skills=skills,
        cases=cases,
        errors=errors,
    )
    return errors, len(cases), len(skills)


def validate_description_case_refs(
    *,
    cases: Sequence[dict[str, Any]],
    signals: dict[str, Any],
    activation_by_name: dict[str, Any],
    errors: list[str],
) -> dict[str, list[dict[str, Any]]]:
    case_index: dict[str, list[dict[str, Any]]] = {name: [] for name in signals}
    for case in cases:
        skill_name = case.get("skill_name")
        if skill_name not in signals:
            errors.append(f"unknown skill in description-trigger case: {skill_name!r}")
            continue
        case_index[skill_name].append(case)
        validate_description_case(
            case=case,
            signal=signals[skill_name],
            activation_by_name=activation_by_name,
            errors=errors,
        )
    return case_index


def validate_description_case(
    *,
    case: dict[str, Any],
    signal: dict[str, Any],
    activation_by_name: dict[str, Any],
    errors: list[str],
) -> None:
    skill_name = case["skill_name"]
    activation_policy = resolve_implicit_activation_policy(
        activation_by_name.get(skill_name),
        skill_name,
    )
    allow_implicit = allow_implicit_invocation(activation_by_name.get(skill_name), skill_name)
    if case.get("description_sha256") != signal.get("description_sha256"):
        errors.append(f"{case['case_id']}: description hash mismatch for {skill_name}")
    if case.get("implicit_activation_policy") != activation_policy:
        errors.append(f"{case['case_id']}: activation policy mismatch for {skill_name}")
    if case.get("source") not in {
        "portable-description",
        "collision-family",
        "mirrored-collision-family",
    }:
        errors.append(f"{case['case_id']}: unknown source {case.get('source')!r}")
    if case.get("case_class") == "prefer-other-skill":
        expected_skill = case.get("expected_skill")
        if not expected_skill or expected_skill == skill_name:
            errors.append(f"{case['case_id']}: prefer-other-skill must point at another skill")
        elif expected_skill not in signal.get("adjacent_skills", []):
            errors.append(
                f"{case['case_id']}: expected_skill {expected_skill!r} is not "
                f"adjacent to {skill_name}"
            )
    if not allow_implicit and case.get("case_class") == "should-trigger":
        errors.append(
            f"{case['case_id']}: non-invoke skill {skill_name} must not have "
            "should-trigger implicit cases"
        )
    if (
        allow_implicit
        and case.get("case_class") == "manual-invocation-required"
        and case.get("source") == "portable-description"
    ):
        errors.append(
            f"{case['case_id']}: invoke-policy skill {skill_name} should not require "
            "manual invocation for its base description case"
        )


def validate_description_coverage(
    *,
    signals: dict[str, Any],
    activation_by_name: dict[str, Any],
    manifest_by_name: dict[str, Any],
    case_index: dict[str, list[dict[str, Any]]],
    policy_doc: dict[str, Any],
    errors: list[str],
) -> dict[str, int]:
    total_case_counter: dict[str, int] = {}
    for skill_name, signal in signals.items():
        totals: dict[str, int] = {}
        for case in case_index[skill_name]:
            totals[case["case_class"]] = totals.get(case["case_class"], 0) + 1
            total_case_counter[case["case_class"]] = (
                total_case_counter.get(case["case_class"], 0) + 1
            )
        activation_policy = resolve_implicit_activation_policy(
            activation_by_name.get(skill_name),
            skill_name,
        )
        required = activation_required_case_classes(
            policy_doc,
            activation_policy=activation_policy,
            invocation_mode=signal["invocation_mode"],
        )
        for case_class in required:
            if totals.get(case_class, 0) < 1:
                errors.append(
                    f"{skill_name}: missing required description-trigger case class "
                    f"{case_class!r}"
                )
        validate_description_manifest_entry(
            skill_name=skill_name,
            signal=signal,
            activation_policy=activation_policy,
            totals=totals,
            manifest_by_name=manifest_by_name,
            policy_doc=policy_doc,
            errors=errors,
        )
    return total_case_counter


def validate_description_manifest_entry(
    *,
    skill_name: str,
    signal: dict[str, Any],
    activation_policy: str,
    totals: dict[str, int],
    manifest_by_name: dict[str, Any],
    policy_doc: dict[str, Any],
    errors: list[str],
) -> None:
    if (
        signal.get("family")
        and totals.get("prefer-other-skill", 0) < 1
        and activation_policy != "manual"
        and policy_doc.get("mirror_collision_cases", True)
    ):
        errors.append(f"{skill_name}: missing prefer-other-skill mirror coverage")
    manifest_entry = manifest_by_name.get(skill_name)
    if manifest_entry is None:
        errors.append(f"description_trigger_eval_manifest.json missing {skill_name}")
    elif manifest_entry.get("coverage_ok") is not True:
        errors.append(
            f"description_trigger_eval_manifest.json reports incomplete coverage for {skill_name}"
        )


def lint_description_trigger_evals(repo_root: Path) -> tuple[list[str], int, int]:
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"
    signals_doc = load_json(generated_dir / "skill_description_signals.json")
    manifest_doc = load_json(generated_dir / "description_trigger_eval_manifest.json")
    cases = load_jsonl(generated_dir / "description_trigger_eval_cases.jsonl")
    policy_doc = load_json(config_dir / "description_trigger_eval_policy.json")
    activation_policy_doc = load_json(config_dir / "skill_policy_matrix.json")
    signals = {entry["name"]: entry for entry in signals_doc.get("skills", [])}
    activation_by_name = activation_policy_doc.get("skills", {})
    manifest_by_name = {entry["name"]: entry for entry in manifest_doc.get("skills", [])}
    errors: list[str] = []
    case_index = validate_description_case_refs(
        cases=cases,
        signals=signals,
        activation_by_name=activation_by_name,
        errors=errors,
    )
    total_case_counter = validate_description_coverage(
        signals=signals,
        activation_by_name=activation_by_name,
        manifest_by_name=manifest_by_name,
        case_index=case_index,
        policy_doc=policy_doc,
        errors=errors,
    )
    if manifest_doc.get("case_class_totals") != dict(sorted(total_case_counter.items())):
        errors.append("description_trigger_eval_manifest.json case_class_totals drift")
    return errors, len(cases), len(signals)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    return parser.parse_args(argv)


def main_trigger(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    errors, case_count, skill_count = lint_trigger_evals(Path(args.repo_root).resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {case_count} trigger cases across {skill_count} skills")
    return 0


def main_description(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    errors, case_count, skill_count = lint_description_trigger_evals(
        Path(args.repo_root).resolve()
    )
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {case_count} description-trigger cases across {skill_count} skills")
    return 0
