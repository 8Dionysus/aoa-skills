#!/usr/bin/env python3
"""Validate wave-9 tiny-router input surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROFILE = "codex-facing-wave-9-tiny-router-inputs"
REQUIRED_GENERATED_FILES = (
    "generated/tiny_router_skill_signals.json",
    "generated/tiny_router_candidate_bands.json",
    "generated/tiny_router_capsules.min.json",
    "generated/tiny_router_eval_cases.jsonl",
    "generated/tiny_router_overlay_manifest.json",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    config_path = repo_root / "config" / "tiny_router_skill_bands.json"
    if not config_path.exists():
        errors.append("Missing config/tiny_router_skill_bands.json")
        return {"status": "fail", "errors": errors, "warnings": warnings}

    for rel_path in REQUIRED_GENERATED_FILES:
        if not (repo_root / rel_path).exists():
            errors.append(f"Missing wave-9 generated file: {rel_path}")
    if errors:
        return {"status": "fail", "errors": errors, "warnings": warnings}

    policy = load_json(config_path)
    skill_catalog = load_json(repo_root / "generated" / "skill_catalog.min.json")
    description_signals = load_json(repo_root / "generated" / "skill_description_signals.json")
    signals = load_json(repo_root / "generated" / "tiny_router_skill_signals.json")
    bands = load_json(repo_root / "generated" / "tiny_router_candidate_bands.json")
    capsules = load_json(repo_root / "generated" / "tiny_router_capsules.min.json")
    eval_cases = load_jsonl(repo_root / "generated" / "tiny_router_eval_cases.jsonl")
    manifest = load_json(repo_root / "generated" / "tiny_router_overlay_manifest.json")

    for label, doc in {
        "config/tiny_router_skill_bands.json": policy,
        "generated/tiny_router_skill_signals.json": signals,
        "generated/tiny_router_candidate_bands.json": bands,
        "generated/tiny_router_capsules.min.json": capsules,
        "generated/tiny_router_overlay_manifest.json": manifest,
    }.items():
        if doc.get("profile") != PROFILE:
            errors.append(f"{label}: profile must be {PROFILE!r}")

    actual_names = {entry["name"] for entry in skill_catalog.get("skills", [])}
    description_by_name = {entry["name"]: entry for entry in description_signals.get("skills", [])}
    signal_by_name = {entry["name"]: entry for entry in signals.get("skills", [])}
    capsule_by_name = {entry["name"]: entry for entry in capsules.get("skills", [])}
    manifest_by_name = {entry["name"]: entry for entry in manifest.get("skills", [])}
    policy_names = set((policy.get("skill_overrides") or {}).keys())

    if policy_names != actual_names:
        errors.append("config/tiny_router_skill_bands.json skill set mismatch")
    if set(signal_by_name) != actual_names:
        errors.append("generated/tiny_router_skill_signals.json skill set mismatch")
    if set(capsule_by_name) != actual_names:
        errors.append("generated/tiny_router_capsules.min.json skill set mismatch")
    if set(manifest_by_name) != actual_names:
        errors.append("generated/tiny_router_overlay_manifest.json skill set mismatch")

    band_defs = {entry["id"]: entry for entry in policy.get("bands", [])}
    band_entries = {entry["id"]: entry for entry in bands.get("bands", [])}
    if set(band_defs) != set(band_entries):
        errors.append("generated/tiny_router_candidate_bands.json band set mismatch")

    positive_coverage = {name: 0 for name in actual_names}
    for case in eval_cases:
        for skill_name in case.get("expected_shortlist_includes", []):
            if skill_name not in actual_names:
                errors.append(f"generated/tiny_router_eval_cases.jsonl references unknown skill {skill_name!r}")
            else:
                positive_coverage[skill_name] += 1
        top1 = case.get("expected_top1")
        if top1 is not None and top1 not in actual_names:
            errors.append(f"generated/tiny_router_eval_cases.jsonl references unknown expected_top1 {top1!r}")
        top1_not = case.get("expected_top1_not")
        if top1_not is not None and top1_not not in actual_names:
            errors.append(f"generated/tiny_router_eval_cases.jsonl references unknown expected_top1_not {top1_not!r}")

    missing_positive = sorted(name for name, count in positive_coverage.items() if count == 0)
    if missing_positive:
        errors.append(f"generated/tiny_router_eval_cases.jsonl missing positive coverage for {', '.join(missing_positive)}")

    for skill_name in sorted(actual_names):
        source_entry = next(entry for entry in skill_catalog["skills"] if entry["name"] == skill_name)
        signal = signal_by_name.get(skill_name)
        capsule = capsule_by_name.get(skill_name)
        manifest_entry = manifest_by_name.get(skill_name)
        description_entry = description_by_name.get(skill_name)
        if signal is None or capsule is None or manifest_entry is None or description_entry is None:
            continue

        expected_band = policy["skill_overrides"][skill_name]["band"]
        expected_manual = source_entry["invocation_mode"] == "explicit-only"
        expected_overlay = source_entry["scope"] == "project"
        if signal.get("band") != expected_band:
            errors.append(f"{skill_name}: tiny_router_skill_signals.json band mismatch")
        if capsule.get("band") != expected_band:
            errors.append(f"{skill_name}: tiny_router_capsules.min.json band mismatch")
        if signal.get("manual_invocation_required") != expected_manual:
            errors.append(f"{skill_name}: tiny_router_skill_signals.json manual flag mismatch")
        if capsule.get("manual_invocation_required") != expected_manual:
            errors.append(f"{skill_name}: tiny_router_capsules.min.json manual flag mismatch")
        if signal.get("allow_implicit_invocation") != (not expected_manual):
            errors.append(f"{skill_name}: tiny_router_skill_signals.json implicit flag mismatch")
        if signal.get("project_overlay") != expected_overlay:
            errors.append(f"{skill_name}: tiny_router_skill_signals.json project_overlay mismatch")
        if capsule.get("project_overlay") != expected_overlay:
            errors.append(f"{skill_name}: tiny_router_capsules.min.json project_overlay mismatch")
        if signal.get("description_sha256") != description_entry.get("description_sha256"):
            errors.append(f"{skill_name}: tiny_router_skill_signals.json description_sha256 mismatch")
        if capsule.get("description_sha256") != description_entry.get("description_sha256"):
            errors.append(f"{skill_name}: tiny_router_capsules.min.json description_sha256 mismatch")
        if manifest_entry.get("description_sha256") != description_entry.get("description_sha256"):
            errors.append(f"{skill_name}: tiny_router_overlay_manifest.json description_sha256 mismatch")
        if len(signal.get("positive_cues", [])) < 3:
            errors.append(f"{skill_name}: too few positive cues")
        if not signal.get("cue_tokens"):
            errors.append(f"{skill_name}: cue_tokens must not be empty")
        if signal.get("companions") != policy.get("companions", {}).get(skill_name, []):
            errors.append(f"{skill_name}: companions mismatch")

    for band_id, band_entry in band_entries.items():
        signals_in_band = [entry["name"] for entry in signals.get("skills", []) if entry["band"] == band_id]
        expected_manual = sorted(
            entry["name"]
            for entry in signals.get("skills", [])
            if entry["band"] == band_id and entry["manual_invocation_required"]
        )
        expected_overlay = sorted(
            entry["name"]
            for entry in signals.get("skills", [])
            if entry["band"] == band_id and entry["project_overlay"]
        )
        if band_entry.get("skills") != signals_in_band:
            errors.append(f"{band_id}: tiny_router_candidate_bands.json skills mismatch")
        if sorted(band_entry.get("manual_only_skills", [])) != expected_manual:
            errors.append(f"{band_id}: tiny_router_candidate_bands.json manual_only_skills mismatch")
        if sorted(band_entry.get("overlay_skills", [])) != expected_overlay:
            errors.append(f"{band_id}: tiny_router_candidate_bands.json overlay_skills mismatch")

    if manifest.get("skill_count") != len(actual_names):
        errors.append("generated/tiny_router_overlay_manifest.json skill_count mismatch")
    if manifest.get("band_count") != len(band_defs):
        errors.append("generated/tiny_router_overlay_manifest.json band_count mismatch")
    if manifest.get("case_count") != len(eval_cases):
        errors.append("generated/tiny_router_overlay_manifest.json case_count mismatch")
    if "config/tiny_router_skill_bands.json" not in manifest.get("source_files", []):
        errors.append("generated/tiny_router_overlay_manifest.json must include config/tiny_router_skill_bands.json")

    return {
        "status": "ok" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate wave-9 tiny-router inputs.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    args = parser.parse_args()

    result = validate(Path(args.repo_root).resolve())
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
