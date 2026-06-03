"""Tiny-router generated-surface validator for aoa-skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from activation.skill_activation_policy import (
    allow_implicit_invocation,
    resolve_implicit_activation_policy,
)


PROFILE = "codex-facing-wave-9-tiny-router-inputs"
REQUIRED_GENERATED_FILES = (
    "generated/tiny_router_skill_signals.json",
    "generated/tiny_router_candidate_bands.json",
    "generated/tiny_router_capsules.min.json",
    "generated/tiny_router_eval_cases.jsonl",
    "generated/tiny_router_overlay_manifest.json",
    "generated/description_trigger_eval_cases.jsonl",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_required_files(repo_root: Path, errors: list[str]) -> bool:
    config_path = repo_root / "config" / "tiny_router_skill_bands.json"
    if not config_path.exists():
        errors.append("Missing config/tiny_router_skill_bands.json")
        return False
    for rel_path in REQUIRED_GENERATED_FILES:
        if not (repo_root / rel_path).exists():
            errors.append(f"Missing wave-9 generated file: {rel_path}")
    return not errors


def validate_profiles(docs_by_label: dict[str, Any], errors: list[str]) -> None:
    for label, doc in docs_by_label.items():
        if doc.get("profile") != PROFILE:
            errors.append(f"{label}: profile must be {PROFILE!r}")


def index_defer_cases(
    description_eval_cases: Sequence[dict[str, Any]],
) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (case["skill_name"], case["prompt"]): case
        for case in description_eval_cases
        if case.get("case_class") == "prefer-other-skill"
        and isinstance(case.get("skill_name"), str)
        and isinstance(case.get("prompt"), str)
    }


def validate_skill_sets(
    *,
    actual_names: set[str],
    policy_names: set[str],
    signal_by_name: dict[str, Any],
    capsule_by_name: dict[str, Any],
    manifest_by_name: dict[str, Any],
    band_defs: dict[str, Any],
    band_entries: dict[str, Any],
    errors: list[str],
) -> None:
    if policy_names != actual_names:
        errors.append("config/tiny_router_skill_bands.json skill set mismatch")
    if set(signal_by_name) != actual_names:
        errors.append("generated/tiny_router_skill_signals.json skill set mismatch")
    if set(capsule_by_name) != actual_names:
        errors.append("generated/tiny_router_capsules.min.json skill set mismatch")
    if set(manifest_by_name) != actual_names:
        errors.append("generated/tiny_router_overlay_manifest.json skill set mismatch")
    if set(band_defs) != set(band_entries):
        errors.append("generated/tiny_router_candidate_bands.json band set mismatch")


def validate_eval_case_refs(
    *,
    eval_cases: Sequence[dict[str, Any]],
    actual_names: set[str],
    signal_by_name: dict[str, Any],
    catalog_by_name: dict[str, Any],
    activation_policy_by_name: dict[str, Any],
    defer_case_by_source_and_prompt: dict[tuple[str, str], dict[str, Any]],
    errors: list[str],
) -> dict[str, int]:
    positive_coverage = {name: 0 for name in actual_names}
    for case in eval_cases:
        for skill_name in case.get("expected_shortlist_includes", []):
            if skill_name not in actual_names:
                errors.append(
                    "generated/tiny_router_eval_cases.jsonl references unknown "
                    f"skill {skill_name!r}"
                )
            else:
                positive_coverage[skill_name] += 1
        validate_eval_case_top_expectations(case, actual_names, errors)
        validate_defer_case(
            case=case,
            signal_by_name=signal_by_name,
            catalog_by_name=catalog_by_name,
            activation_policy_by_name=activation_policy_by_name,
            defer_case_by_source_and_prompt=defer_case_by_source_and_prompt,
            errors=errors,
        )
    return positive_coverage


def validate_eval_case_top_expectations(
    case: dict[str, Any],
    actual_names: set[str],
    errors: list[str],
) -> None:
    top1 = case.get("expected_top1")
    if top1 is not None and top1 not in actual_names:
        errors.append(
            "generated/tiny_router_eval_cases.jsonl references unknown "
            f"expected_top1 {top1!r}"
        )
    top1_not = case.get("expected_top1_not")
    if top1_not is not None and top1_not not in actual_names:
        errors.append(
            "generated/tiny_router_eval_cases.jsonl references unknown "
            f"expected_top1_not {top1_not!r}"
        )


def validate_defer_case(
    *,
    case: dict[str, Any],
    signal_by_name: dict[str, Any],
    catalog_by_name: dict[str, Any],
    activation_policy_by_name: dict[str, Any],
    defer_case_by_source_and_prompt: dict[tuple[str, str], dict[str, Any]],
    errors: list[str],
) -> None:
    case_id = str(case.get("case_id", ""))
    if not case_id.startswith("tiny-defer-"):
        return
    source_skill = case_id[len("tiny-defer-") :]
    if source_skill not in signal_by_name:
        return
    source_band = signal_by_name[source_skill]["band"]
    source_signal = signal_by_name[source_skill]
    included = case.get("expected_shortlist_includes", [])
    source_defer_case = defer_case_by_source_and_prompt.get(
        (source_skill, case.get("prompt"))
    )
    expected_skill = (
        source_defer_case.get("expected_skill")
        if isinstance(source_defer_case, dict)
        else None
    )
    expected_activation = expected_defer_activation(
        expected_skill,
        activation_policy_by_name,
    )
    validate_defer_band_policy(
        case=case,
        case_id=case_id,
        source_band=source_band,
        source_signal=source_signal,
        included=included,
        expected_activation=expected_activation,
        expected_skill=expected_skill,
        catalog_by_name=catalog_by_name,
        signal_by_name=signal_by_name,
        errors=errors,
    )


def expected_defer_activation(
    expected_skill: Any,
    activation_policy_by_name: dict[str, Any],
) -> str:
    if isinstance(expected_skill, str) and expected_skill in activation_policy_by_name:
        return resolve_implicit_activation_policy(
            activation_policy_by_name.get(expected_skill),
            expected_skill,
        )
    return "manual"


def validate_defer_band_policy(
    *,
    case: dict[str, Any],
    case_id: str,
    source_band: str,
    source_signal: dict[str, Any],
    included: Sequence[str],
    expected_activation: str,
    expected_skill: Any,
    catalog_by_name: dict[str, Any],
    signal_by_name: dict[str, Any],
    errors: list[str],
) -> None:
    if case.get("expected_band") != source_band and included:
        errors.append(
            f"{case_id}: cross-band defer cases must not require "
            "expected_shortlist_includes"
        )
    if (
        case.get("expected_band") != source_band
        and source_signal.get("project_overlay")
        and not case.get("repo_family_hint")
    ):
        errors.append(f"{case_id}: cross-band overlay defer cases must set repo_family_hint")
    if case.get("expected_band") == source_band and not included and expected_activation != "manual":
        errors.append(f"{case_id}: same-band defer cases must require expected_shortlist_includes")
    if (
        case.get("expected_band") != source_band
        and isinstance(expected_skill, str)
        and expected_skill in catalog_by_name
        and catalog_by_name[expected_skill].get("scope") == "project"
        and not case.get("repo_family_hint")
    ):
        errors.append(f"{case_id}: cross-band overlay defer targets must set repo_family_hint")
    for included_skill in included:
        included_signal = signal_by_name.get(included_skill)
        if included_signal and included_signal["project_overlay"] and not case.get("repo_family_hint"):
            errors.append(f"{case_id}: overlay defer targets must set repo_family_hint")


def validate_positive_coverage(
    positive_coverage: dict[str, int],
    errors: list[str],
) -> None:
    missing_positive = sorted(
        name for name, count in positive_coverage.items() if count == 0
    )
    if missing_positive:
        errors.append(
            "generated/tiny_router_eval_cases.jsonl missing positive coverage "
            f"for {', '.join(missing_positive)}"
        )


def validate_skill_entries(
    *,
    actual_names: set[str],
    skill_catalog: dict[str, Any],
    policy: dict[str, Any],
    activation_policy_by_name: dict[str, Any],
    description_by_name: dict[str, Any],
    signal_by_name: dict[str, Any],
    capsule_by_name: dict[str, Any],
    manifest_by_name: dict[str, Any],
    errors: list[str],
) -> None:
    for skill_name in sorted(actual_names):
        source_entry = next(
            entry for entry in skill_catalog["skills"] if entry["name"] == skill_name
        )
        signal = signal_by_name.get(skill_name)
        capsule = capsule_by_name.get(skill_name)
        manifest_entry = manifest_by_name.get(skill_name)
        description_entry = description_by_name.get(skill_name)
        if signal is None or capsule is None or manifest_entry is None or description_entry is None:
            continue
        validate_single_skill_entry(
            skill_name=skill_name,
            source_entry=source_entry,
            policy=policy,
            activation_policy_by_name=activation_policy_by_name,
            description_entry=description_entry,
            signal=signal,
            capsule=capsule,
            manifest_entry=manifest_entry,
            errors=errors,
        )


def validate_single_skill_entry(
    *,
    skill_name: str,
    source_entry: dict[str, Any],
    policy: dict[str, Any],
    activation_policy_by_name: dict[str, Any],
    description_entry: dict[str, Any],
    signal: dict[str, Any],
    capsule: dict[str, Any],
    manifest_entry: dict[str, Any],
    errors: list[str],
) -> None:
    expected_band = policy["skill_overrides"][skill_name]["band"]
    policy_entry = activation_policy_by_name.get(skill_name) or {
        "implicit_activation_policy": signal.get("implicit_activation_policy")
        or description_entry.get("implicit_activation_policy")
        or ("invoke" if signal.get("allow_implicit_invocation") else "manual")
    }
    expected_activation = resolve_implicit_activation_policy(policy_entry, skill_name)
    expected_allow = allow_implicit_invocation(policy_entry, skill_name)
    expected_manual = expected_activation != "invoke"
    expected_candidate_only = expected_activation == "suggest"
    expected_overlay = source_entry["scope"] == "project"
    validate_skill_entry_fields(
        skill_name=skill_name,
        expected_band=expected_band,
        expected_activation=expected_activation,
        expected_allow=expected_allow,
        expected_manual=expected_manual,
        expected_candidate_only=expected_candidate_only,
        expected_overlay=expected_overlay,
        description_entry=description_entry,
        signal=signal,
        capsule=capsule,
        manifest_entry=manifest_entry,
        policy=policy,
        errors=errors,
    )


def validate_skill_entry_fields(
    *,
    skill_name: str,
    expected_band: str,
    expected_activation: str,
    expected_allow: bool,
    expected_manual: bool,
    expected_candidate_only: bool,
    expected_overlay: bool,
    description_entry: dict[str, Any],
    signal: dict[str, Any],
    capsule: dict[str, Any],
    manifest_entry: dict[str, Any],
    policy: dict[str, Any],
    errors: list[str],
) -> None:
    comparisons = (
        (signal.get("band"), expected_band, "tiny_router_skill_signals.json band"),
        (capsule.get("band"), expected_band, "tiny_router_capsules.min.json band"),
        (signal.get("manual_invocation_required"), expected_manual, "tiny_router_skill_signals.json manual flag"),
        (capsule.get("manual_invocation_required"), expected_manual, "tiny_router_capsules.min.json manual flag"),
        (signal.get("allow_implicit_invocation"), expected_allow, "tiny_router_skill_signals.json implicit flag"),
        (signal.get("implicit_activation_policy"), expected_activation, "tiny_router_skill_signals.json activation policy"),
        (capsule.get("implicit_activation_policy"), expected_activation, "tiny_router_capsules.min.json activation policy"),
        (manifest_entry.get("implicit_activation_policy"), expected_activation, "tiny_router_overlay_manifest.json activation policy"),
        (signal.get("candidate_only"), expected_candidate_only, "tiny_router_skill_signals.json candidate_only"),
        (capsule.get("candidate_only"), expected_candidate_only, "tiny_router_capsules.min.json candidate_only"),
        (manifest_entry.get("candidate_only"), expected_candidate_only, "tiny_router_overlay_manifest.json candidate_only"),
        (signal.get("project_overlay"), expected_overlay, "tiny_router_skill_signals.json project_overlay"),
        (capsule.get("project_overlay"), expected_overlay, "tiny_router_capsules.min.json project_overlay"),
        (signal.get("description_sha256"), description_entry.get("description_sha256"), "tiny_router_skill_signals.json description_sha256"),
        (capsule.get("description_sha256"), description_entry.get("description_sha256"), "tiny_router_capsules.min.json description_sha256"),
        (manifest_entry.get("description_sha256"), description_entry.get("description_sha256"), "tiny_router_overlay_manifest.json description_sha256"),
    )
    for actual, expected, label in comparisons:
        if actual != expected:
            errors.append(f"{skill_name}: {label} mismatch")
    if len(signal.get("positive_cues", [])) < 3:
        errors.append(f"{skill_name}: too few positive cues")
    if not signal.get("cue_tokens"):
        errors.append(f"{skill_name}: cue_tokens must not be empty")
    if signal.get("companions") != policy.get("companions", {}).get(skill_name, []):
        errors.append(f"{skill_name}: companions mismatch")


def validate_band_entries(
    *,
    bands: dict[str, Any],
    signals: dict[str, Any],
    errors: list[str],
) -> None:
    for band_id, band_entry in bands.items():
        signals_in_band = [
            entry["name"] for entry in signals.get("skills", []) if entry["band"] == band_id
        ]
        expected_manual = sorted(
            entry["name"]
            for entry in signals.get("skills", [])
            if entry["band"] == band_id and entry["manual_invocation_required"]
        )
        expected_suggest = sorted(
            entry["name"]
            for entry in signals.get("skills", [])
            if entry["band"] == band_id and entry.get("candidate_only")
        )
        expected_overlay = sorted(
            entry["name"]
            for entry in signals.get("skills", [])
            if entry["band"] == band_id and entry["project_overlay"]
        )
        if band_entry.get("skills") != signals_in_band:
            errors.append(f"{band_id}: tiny_router_candidate_bands.json skills mismatch")
        if sorted(band_entry.get("manual_only_skills", [])) != expected_manual:
            errors.append(
                f"{band_id}: tiny_router_candidate_bands.json manual_only_skills mismatch"
            )
        if sorted(band_entry.get("suggest_only_skills", [])) != expected_suggest:
            errors.append(
                f"{band_id}: tiny_router_candidate_bands.json suggest_only_skills mismatch"
            )
        if sorted(band_entry.get("overlay_skills", [])) != expected_overlay:
            errors.append(
                f"{band_id}: tiny_router_candidate_bands.json overlay_skills mismatch"
            )


def validate_manifest_summary(
    *,
    manifest: dict[str, Any],
    actual_skill_count: int,
    band_count: int,
    case_count: int,
    errors: list[str],
) -> None:
    if manifest.get("skill_count") != actual_skill_count:
        errors.append("generated/tiny_router_overlay_manifest.json skill_count mismatch")
    if manifest.get("band_count") != band_count:
        errors.append("generated/tiny_router_overlay_manifest.json band_count mismatch")
    if manifest.get("case_count") != case_count:
        errors.append("generated/tiny_router_overlay_manifest.json case_count mismatch")
    if "config/tiny_router_skill_bands.json" not in manifest.get("source_files", []):
        errors.append(
            "generated/tiny_router_overlay_manifest.json must include "
            "config/tiny_router_skill_bands.json"
        )


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not validate_required_files(repo_root, errors):
        return {"status": "fail", "errors": errors, "warnings": warnings}

    policy = load_json(repo_root / "config" / "tiny_router_skill_bands.json")
    activation_policy_path = repo_root / "config" / "skill_policy_matrix.json"
    activation_policy_doc = (
        load_json(activation_policy_path)
        if activation_policy_path.exists()
        else {"skills": {}}
    )
    skill_catalog = load_json(repo_root / "generated" / "skill_catalog.min.json")
    description_signals = load_json(repo_root / "generated" / "skill_description_signals.json")
    description_eval_cases = load_jsonl(repo_root / "generated" / "description_trigger_eval_cases.jsonl")
    signals = load_json(repo_root / "generated" / "tiny_router_skill_signals.json")
    bands = load_json(repo_root / "generated" / "tiny_router_candidate_bands.json")
    capsules = load_json(repo_root / "generated" / "tiny_router_capsules.min.json")
    eval_cases = load_jsonl(repo_root / "generated" / "tiny_router_eval_cases.jsonl")
    manifest = load_json(repo_root / "generated" / "tiny_router_overlay_manifest.json")

    validate_profiles(
        {
            "config/tiny_router_skill_bands.json": policy,
            "generated/tiny_router_skill_signals.json": signals,
            "generated/tiny_router_candidate_bands.json": bands,
            "generated/tiny_router_capsules.min.json": capsules,
            "generated/tiny_router_overlay_manifest.json": manifest,
        },
        errors,
    )
    actual_names = {entry["name"] for entry in skill_catalog.get("skills", [])}
    catalog_by_name = {entry["name"]: entry for entry in skill_catalog.get("skills", [])}
    description_by_name = {entry["name"]: entry for entry in description_signals.get("skills", [])}
    signal_by_name = {entry["name"]: entry for entry in signals.get("skills", [])}
    capsule_by_name = {entry["name"]: entry for entry in capsules.get("skills", [])}
    manifest_by_name = {entry["name"]: entry for entry in manifest.get("skills", [])}
    activation_policy_by_name = activation_policy_doc.get("skills", {})
    band_defs = {entry["id"]: entry for entry in policy.get("bands", [])}
    band_entries = {entry["id"]: entry for entry in bands.get("bands", [])}

    validate_skill_sets(
        actual_names=actual_names,
        policy_names=set((policy.get("skill_overrides") or {}).keys()),
        signal_by_name=signal_by_name,
        capsule_by_name=capsule_by_name,
        manifest_by_name=manifest_by_name,
        band_defs=band_defs,
        band_entries=band_entries,
        errors=errors,
    )
    positive_coverage = validate_eval_case_refs(
        eval_cases=eval_cases,
        actual_names=actual_names,
        signal_by_name=signal_by_name,
        catalog_by_name=catalog_by_name,
        activation_policy_by_name=activation_policy_by_name,
        defer_case_by_source_and_prompt=index_defer_cases(description_eval_cases),
        errors=errors,
    )
    validate_positive_coverage(positive_coverage, errors)
    validate_skill_entries(
        actual_names=actual_names,
        skill_catalog=skill_catalog,
        policy=policy,
        activation_policy_by_name=activation_policy_by_name,
        description_by_name=description_by_name,
        signal_by_name=signal_by_name,
        capsule_by_name=capsule_by_name,
        manifest_by_name=manifest_by_name,
        errors=errors,
    )
    validate_band_entries(bands=band_entries, signals=signals, errors=errors)
    validate_manifest_summary(
        manifest=manifest,
        actual_skill_count=len(actual_names),
        band_count=len(band_defs),
        case_count=len(eval_cases),
        errors=errors,
    )
    return {"status": "ok" if not errors else "fail", "errors": errors, "warnings": warnings}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate wave-9 tiny-router inputs.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate(Path(args.repo_root).resolve())
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0 if result["status"] == "ok" else 2
