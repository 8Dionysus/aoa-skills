#!/usr/bin/env python3
"""Build wave-7 description-first trigger evals and skills-ref manifests.

This layer keeps the existing wave-2 trigger seed data, but adds a stricter
activation-contract suite derived from the portable skill descriptions.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
from typing import Any

import release_manifest_contract
import yaml

PROFILE = "codex-facing-wave-7-description-trigger-evals"
VALIDATION_PROFILE = "codex-facing-wave-7-standard-validation"
JSON_INDENT = 2
WAVE7_GENERATED_FILES = [
    "generated/skill_description_signals.json",
    "generated/description_trigger_eval_cases.jsonl",
    "generated/description_trigger_eval_cases.csv",
    "generated/description_trigger_eval_manifest.json",
    "generated/skills_ref_validation_manifest.json",
]


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=JSON_INDENT, ensure_ascii=False) + "\n"


def render_or_check(path: pathlib.Path, text: str, check: bool) -> None:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            raise SystemExit(f"wave-7 description-trigger drift: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_frontmatter(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter start")
    try:
        _, fm_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{path}: invalid frontmatter fence structure") from exc
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must parse to a mapping")
    return data, body


def split_description(description: str) -> dict[str, str]:
    summary = description
    use_when = ""
    do_not_use = ""
    if "Use when" in description:
        summary, tail = description.split("Use when", 1)
        summary = summary.strip()
        if "Do not use" in tail:
            use_when, do_not_use = tail.split("Do not use", 1)
        else:
            use_when = tail
    elif "Do not use" in description:
        summary, do_not_use = description.split("Do not use", 1)
    return {
        "summary_clause": summary.rstrip(" ."),
        "use_when_clause": use_when.strip().rstrip(" ."),
        "do_not_use_clause": do_not_use.strip().rstrip(" ."),
    }


def csv_text(rows: list[dict[str, Any]], fieldnames: list[str]) -> str:
    import io

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        flat = {key: row.get(key) for key in fieldnames}
        for key, value in list(flat.items()):
            if isinstance(value, (list, dict)):
                flat[key] = json.dumps(value, ensure_ascii=False)
        writer.writerow(flat)
    return buf.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--check", action="store_true", help="Check for drift instead of writing files")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"
    skills_root = repo_root / ".agents" / "skills"

    catalog_doc = load_json(generated_dir / "skill_catalog.min.json")
    agent_catalog = load_json(generated_dir / "agent_skill_catalog.json")
    runtime_doc = load_json(generated_dir / "skill_runtime_contracts.json")
    router_doc = load_json(generated_dir / "runtime_router_hints.json")
    base_cases = load_jsonl(generated_dir / "skill_trigger_eval_cases.jsonl")
    collision_doc = load_json(generated_dir / "skill_trigger_collision_matrix.json")
    overrides_doc = load_json(config_dir / "portable_skill_overrides.json")
    policy_doc = load_json(config_dir / "description_trigger_eval_policy.json")

    source_names = {entry["name"] for entry in catalog_doc.get("skills", [])}
    expected_sets = {
        "generated/agent_skill_catalog.json": {entry["name"] for entry in agent_catalog.get("skills", [])},
        "generated/skill_runtime_contracts.json": {entry["name"] for entry in runtime_doc.get("skills", [])},
        "generated/runtime_router_hints.json": {entry["name"] for entry in router_doc.get("skills", [])},
        ".agents/skills": {path.name for path in skills_root.iterdir() if path.is_dir()},
    }
    for label, names in expected_sets.items():
        if names != source_names:
            raise SystemExit(f"wave-7 description-trigger parity mismatch: {label}")

    override_by_name = overrides_doc.get("skills", {})
    family_by_skill: dict[str, list[str]] = {entry["name"]: [] for entry in catalog_doc.get("skills", [])}
    neighbors_by_skill: dict[str, set[str]] = {entry["name"]: set() for entry in catalog_doc.get("skills", [])}
    for family in collision_doc.get("families", []):
        members = family.get("skills", [])
        for skill_name in members:
            family_by_skill.setdefault(skill_name, []).append(family["family"])
            neighbors_by_skill.setdefault(skill_name, set()).update(name for name in members if name != skill_name)
    for collision_case in collision_doc.get("cases", []):
        skill_name = collision_case.get("skill_name")
        competing = collision_case.get("competing_skills", [])
        neighbors_by_skill.setdefault(skill_name, set()).update(competing)
        for competing_skill in competing:
            neighbors_by_skill.setdefault(competing_skill, set()).add(skill_name)
            neighbors_by_skill.setdefault(competing_skill, set()).update(
                name for name in competing if name != competing_skill
            )

    base_cases_by_skill: dict[str, list[dict[str, Any]]] = {name: [] for name in source_names}
    for case in base_cases:
        skill_name = case.get("skill_name")
        if skill_name in base_cases_by_skill:
            base_cases_by_skill[skill_name].append(case)

    description_signals: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    fieldnames = [
        "case_id",
        "suite",
        "skill_name",
        "family",
        "case_class",
        "source",
        "description_sha256",
        "invocation_mode",
        "allow_implicit_invocation",
        "expected_behavior",
        "expected_skill",
        "competing_skills",
        "prompt_origin",
        "prompt",
        "note",
    ]

    def append_case(case: dict[str, Any]) -> None:
        rows.append(case)

    for entry in catalog_doc.get("skills", []):
        skill_name = entry["name"]
        skill_md = skills_root / skill_name / "SKILL.md"
        frontmatter, _ = parse_frontmatter(skill_md)
        description = frontmatter["description"].strip()
        parts = split_description(description)
        description_sha = hashlib.sha256(description.encode("utf-8")).hexdigest()
        invocation_mode = entry.get("invocation_mode", "explicit-preferred")
        allow_implicit = invocation_mode != "explicit-only"
        required_case_classes = policy_doc["required_case_classes"][invocation_mode]
        families = sorted(family_by_skill.get(skill_name, []))
        family = families[0] if families else None
        signal = {
            "name": skill_name,
            "description": description,
            "description_sha256": description_sha,
            "summary_clause": parts["summary_clause"],
            "use_when_clause": parts["use_when_clause"],
            "do_not_use_clause": parts["do_not_use_clause"],
            "invocation_mode": invocation_mode,
            "allow_implicit_invocation": allow_implicit,
            "family": family,
            "families": families,
            "adjacent_skills": sorted(neighbors_by_skill.get(skill_name, set())),
            "default_prompt": override_by_name.get(skill_name, {}).get("default_prompt", ""),
            "required_case_classes": required_case_classes,
            "base_case_ids": [case["case_id"] for case in base_cases_by_skill.get(skill_name, [])],
            "collision_case_ids": [],
            "mirror_case_ids": [],
        }
        description_signals.append(signal)

        mode_to_case_class = {
            ("explicit", "invoke-skill"): "explicit-handle",
            ("implicit", "invoke-skill"): "should-trigger",
            ("implicit", "manual-invocation-required"): "manual-invocation-required",
            ("adjacent-negative", "do-not-invoke-skill"): "should-not-trigger",
        }
        for base_case in base_cases_by_skill.get(skill_name, []):
            key = (base_case.get("mode"), base_case.get("expected_behavior"))
            case_class = mode_to_case_class.get(key)
            if case_class is None:
                continue
            append_case(
                {
                    "case_id": f"desc-{base_case['case_id']}",
                    "suite": "description-trigger",
                    "skill_name": skill_name,
                    "family": family,
                    "case_class": case_class,
                    "source": "portable-description",
                    "description_sha256": description_sha,
                    "invocation_mode": invocation_mode,
                    "allow_implicit_invocation": allow_implicit,
                    "expected_behavior": base_case["expected_behavior"],
                    "expected_skill": base_case.get("expected_skill"),
                    "competing_skills": base_case.get("competing_skills", []),
                    "prompt_origin": "wave-2-trigger-seed",
                    "prompt": base_case["prompt"],
                    "note": base_case["note"],
                }
            )

    signals_by_name = {entry["name"]: entry for entry in description_signals}
    mirror_case_counter = 1

    for collision_case in collision_doc.get("cases", []):
        skill_name = collision_case["skill_name"]
        signal = signals_by_name[skill_name]
        primary_case_id = f"desc-collision-{collision_case['case_id']}"
        append_case(
            {
                "case_id": primary_case_id,
                "suite": "description-trigger",
                "skill_name": skill_name,
                "family": signal.get("family"),
                "case_class": (
                    "manual-invocation-required"
                    if collision_case.get("expected_behavior") == "manual-invocation-required"
                    else "should-trigger"
                ),
                "source": "collision-family",
                "description_sha256": signal["description_sha256"],
                "invocation_mode": signal["invocation_mode"],
                "allow_implicit_invocation": signal["allow_implicit_invocation"],
                "expected_behavior": collision_case["expected_behavior"],
                "expected_skill": collision_case.get("expected_skill"),
                "competing_skills": collision_case.get("competing_skills", []),
                "prompt_origin": "collision-matrix",
                "prompt": collision_case["prompt"],
                "note": collision_case["note"],
            }
        )
        signal["collision_case_ids"].append(primary_case_id)

        if not policy_doc.get("mirror_collision_cases", True):
            continue
        if collision_case.get("expected_behavior") != "invoke-skill" or not collision_case.get("expected_skill"):
            continue

        for competing_skill in collision_case.get("competing_skills", []):
            competing_signal = signals_by_name[competing_skill]
            if len(competing_signal["mirror_case_ids"]) >= policy_doc.get("max_prefer_other_cases_per_skill", 4):
                continue
            mirror_case_id = f"desc-mirror-{mirror_case_counter:03d}-{competing_skill}"
            mirror_case_counter += 1
            append_case(
                {
                    "case_id": mirror_case_id,
                    "suite": "description-trigger",
                    "skill_name": competing_skill,
                    "family": competing_signal.get("family"),
                    "case_class": "prefer-other-skill",
                    "source": "mirrored-collision-family",
                    "description_sha256": competing_signal["description_sha256"],
                    "invocation_mode": competing_signal["invocation_mode"],
                    "allow_implicit_invocation": competing_signal["allow_implicit_invocation"],
                    "expected_behavior": "defer-to-other-skill",
                    "expected_skill": collision_case["expected_skill"],
                    "competing_skills": [
                        skill_name,
                        *[name for name in collision_case.get("competing_skills", []) if name != competing_skill],
                    ],
                    "prompt_origin": "mirrored-collision-matrix",
                    "prompt": collision_case["prompt"],
                    "note": (
                        f"This near-neighbor prompt belongs to {collision_case['expected_skill']}; "
                        f"{competing_skill} should stay out of the match and defer."
                    ),
                }
            )
            competing_signal["mirror_case_ids"].append(mirror_case_id)

    rows.sort(key=lambda item: (item["skill_name"], item["case_class"], item["case_id"]))

    case_totals: dict[str, int] = {}
    per_skill_manifest: list[dict[str, Any]] = []
    for signal in description_signals:
        cases = [row for row in rows if row["skill_name"] == signal["name"]]
        class_totals: dict[str, int] = {}
        for row in cases:
            class_totals[row["case_class"]] = class_totals.get(row["case_class"], 0) + 1
            case_totals[row["case_class"]] = case_totals.get(row["case_class"], 0) + 1
        required = signal["required_case_classes"]
        per_skill_manifest.append(
            {
                "name": signal["name"],
                "invocation_mode": signal["invocation_mode"],
                "description_sha256": signal["description_sha256"],
                "family": signal.get("family"),
                "total_cases": len(cases),
                "case_class_totals": class_totals,
                "required_case_classes": required,
                "coverage_ok": all(class_totals.get(case_class, 0) >= 1 for case_class in required),
                "has_collision_coverage": bool(signal.get("collision_case_ids") or signal.get("mirror_case_ids")),
            }
        )

    manifest = {
        "schema_version": 1,
        "profile": PROFILE,
        "source_files": [
            "config/portable_skill_overrides.json",
            "config/description_trigger_eval_policy.json",
            "generated/skill_trigger_eval_cases.jsonl",
            "generated/skill_trigger_collision_matrix.json",
            "generated/agent_skill_catalog.json",
            "generated/skill_runtime_contracts.json",
            "generated/runtime_router_hints.json",
            ".agents/skills/*/SKILL.md",
        ],
        "skill_count": len(description_signals),
        "total_cases": len(rows),
        "case_class_totals": dict(sorted(case_totals.items())),
        "skills": per_skill_manifest,
    }

    validation_manifest = {
        "schema_version": 1,
        "profile": VALIDATION_PROFILE,
        "mode": "soft-conformance-lane",
        "validator": "skills-ref",
        "upstream": {
            "repository": "agentskills/agentskills",
            "subdirectory": "skills-ref",
            "installation": [
                "git clone --depth 1 https://github.com/agentskills/agentskills.git /tmp/agentskills",
                "python -m pip install -e /tmp/agentskills/skills-ref",
            ],
            "usage": "skills-ref validate path/to/skill",
            "caveat": (
                "Upstream marks skills-ref as a reference library intended for demonstration purposes; "
                "use it as a soft conformance lane alongside AoA-specific validators."
            ),
        },
        "targets": [
            {
                "skill_name": signal["name"],
                "path": f".agents/skills/{signal['name']}",
                "command": ["skills-ref", "validate", f".agents/skills/{signal['name']}"],
                "description_sha256": signal["description_sha256"],
            }
            for signal in description_signals
        ],
        "ci_steps": [
            "Build the portable export and downstream runtime layers first.",
            "Run python scripts/validate_agent_skills.py --repo-root . and python scripts/lint_description_trigger_evals.py --repo-root . in the same job.",
            "Run python scripts/run_skills_ref_validation.py --repo-root . as a soft conformance lane. Missing validator should skip cleanly; actual validator failures should fail the job.",
        ],
    }

    file_map = {
        generated_dir / "skill_description_signals.json": dump_json(
            {"schema_version": 1, "profile": PROFILE, "skills": description_signals}
        ),
        generated_dir / "description_trigger_eval_cases.jsonl": "\n".join(
            json.dumps(row, ensure_ascii=False) for row in rows
        )
        + "\n",
        generated_dir / "description_trigger_eval_cases.csv": csv_text(rows, fieldnames),
        generated_dir / "description_trigger_eval_manifest.json": dump_json(manifest),
        generated_dir / "skills_ref_validation_manifest.json": dump_json(validation_manifest),
    }
    release_doc = release_manifest_contract.build_release_manifest(
        repo_root,
        file_overrides=file_map,
    )
    file_map[generated_dir / "release_manifest.json"] = dump_json(release_doc)
    for path, text in file_map.items():
        render_or_check(path, text, args.check)

    print(f"built {len(rows)} description-trigger cases across {len(description_signals)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
