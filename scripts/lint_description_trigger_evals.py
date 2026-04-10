#!/usr/bin/env python3
"""Lint the wave-7 description-trigger eval suite."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"

    signals_doc = load_json(generated_dir / "skill_description_signals.json")
    manifest_doc = load_json(generated_dir / "description_trigger_eval_manifest.json")
    cases = load_jsonl(generated_dir / "description_trigger_eval_cases.jsonl")
    policy_doc = load_json(config_dir / "description_trigger_eval_policy.json")

    signals = {entry["name"]: entry for entry in signals_doc.get("skills", [])}
    manifest_by_name = {entry["name"]: entry for entry in manifest_doc.get("skills", [])}
    case_index: dict[str, list[dict[str, Any]]] = {name: [] for name in signals}
    errors: list[str] = []

    for case in cases:
        skill_name = case.get("skill_name")
        if skill_name not in signals:
            errors.append(f"unknown skill in description-trigger case: {skill_name!r}")
            continue
        case_index[skill_name].append(case)
        signal = signals[skill_name]
        if case.get("description_sha256") != signal.get("description_sha256"):
            errors.append(f"{case['case_id']}: description hash mismatch for {skill_name}")
        if case.get("source") not in {"portable-description", "collision-family", "mirrored-collision-family"}:
            errors.append(f"{case['case_id']}: unknown source {case.get('source')!r}")
        if case.get("case_class") == "prefer-other-skill":
            expected_skill = case.get("expected_skill")
            if not expected_skill or expected_skill == skill_name:
                errors.append(f"{case['case_id']}: prefer-other-skill must point at another skill")
            elif expected_skill not in signal.get("adjacent_skills", []):
                errors.append(f"{case['case_id']}: expected_skill {expected_skill!r} is not adjacent to {skill_name}")
        if signal.get("invocation_mode") == "explicit-only" and case.get("case_class") == "should-trigger":
            errors.append(f"{case['case_id']}: explicit-only skill {skill_name} must not have should-trigger implicit cases")
        if (
            signal.get("invocation_mode") != "explicit-only"
            and case.get("case_class") == "manual-invocation-required"
            and case.get("source") == "portable-description"
        ):
            errors.append(
                f"{case['case_id']}: implicit-preferred skill {skill_name} should not require manual invocation for its base description case"
            )

    total_case_counter: dict[str, int] = {}
    for skill_name, signal in signals.items():
        skill_cases = case_index[skill_name]
        totals: dict[str, int] = {}
        for case in skill_cases:
            totals[case["case_class"]] = totals.get(case["case_class"], 0) + 1
            total_case_counter[case["case_class"]] = total_case_counter.get(case["case_class"], 0) + 1
        required = policy_doc["required_case_classes"][signal["invocation_mode"]]
        for case_class in required:
            if totals.get(case_class, 0) < 1:
                errors.append(f"{skill_name}: missing required description-trigger case class {case_class!r}")
        if (
            signal.get("family")
            and totals.get("prefer-other-skill", 0) < 1
            and signal["invocation_mode"] != "explicit-only"
            and policy_doc.get("mirror_collision_cases", True)
        ):
            errors.append(f"{skill_name}: missing prefer-other-skill mirror coverage")
        manifest_entry = manifest_by_name.get(skill_name)
        if manifest_entry is None:
            errors.append(f"description_trigger_eval_manifest.json missing {skill_name}")
        else:
            if manifest_entry.get("coverage_ok") is not True:
                errors.append(f"description_trigger_eval_manifest.json reports incomplete coverage for {skill_name}")

    if manifest_doc.get("case_class_totals") != dict(sorted(total_case_counter.items())):
        errors.append("description_trigger_eval_manifest.json case_class_totals drift")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(cases)} description-trigger cases across {len(signals)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
