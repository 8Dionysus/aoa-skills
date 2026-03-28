#!/usr/bin/env python3
"""Build wave-9 tiny-router input surfaces from aoa-skills sources.

This builder compresses current skill meaning into a low-context, stage-1
shortlist surface for downstream routing. It does not activate skills and it
does not own scoring or dispatch logic.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import release_manifest_contract


PROFILE = "codex-facing-wave-9-tiny-router-inputs"
JSON_INDENT = 2
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "bounded",
    "by",
    "can",
    "change",
    "changes",
    "clearly",
    "code",
    "config",
    "current",
    "do",
    "docs",
    "explicit",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "its",
    "local",
    "main",
    "meaningful",
    "need",
    "needs",
    "not",
    "of",
    "on",
    "only",
    "or",
    "rather",
    "repo",
    "repository",
    "should",
    "surface",
    "surfaces",
    "task",
    "tasks",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "this",
    "through",
    "to",
    "use",
    "when",
    "with",
    "work",
    "workflow",
    "you",
    "your",
}
GENERATED_FILES = {
    "signals": "generated/tiny_router_skill_signals.json",
    "bands": "generated/tiny_router_candidate_bands.json",
    "capsules": "generated/tiny_router_capsules.min.json",
    "eval_cases": "generated/tiny_router_eval_cases.jsonl",
    "manifest": "generated/tiny_router_overlay_manifest.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=JSON_INDENT, ensure_ascii=False) + "\n"


def dump_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def render_or_check(path: Path, text: str, check: bool, repo_root: Path) -> None:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            raise SystemExit(f"{path.relative_to(repo_root).as_posix()} is out of date")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def normalize(text: str) -> str:
    normalized = text.lower()
    normalized = normalized.replace("aoa-", "aoa ")
    normalized = normalized.replace("atm10-", "atm10 ")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def tokenize(text: str) -> list[str]:
    return [token for token in normalize(text).split() if len(token) > 2 and token not in STOPWORDS]


def overlay_family_hint(skill_name: str, project_overlay: bool) -> str | None:
    if not project_overlay:
        return None
    return skill_name.split("-", 1)[0]


def phrase_tokens(phrases: list[str]) -> list[str]:
    seen: dict[str, None] = {}
    for phrase in phrases:
        for token in tokenize(phrase):
            seen.setdefault(token, None)
    return list(seen)


def auto_tokens(*parts: str) -> list[str]:
    counts: defaultdict[str, int] = defaultdict(int)
    for part in parts:
        for token in tokenize(part):
            counts[token] += 1
    ranked = sorted(counts, key=lambda token: (-counts[token], token))
    return ranked[:14]


def short_summary(text: str, limit: int = 140) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit].rstrip()
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


def choose_case(
    cases: list[dict[str, Any]],
    *,
    preferred_classes: list[str] | None = None,
    preferred_modes: list[str] | None = None,
    expected_behavior: str | None = None,
) -> dict[str, Any] | None:
    for case in cases:
        if preferred_classes is not None and case.get("case_class") not in preferred_classes:
            continue
        if preferred_modes is not None and case.get("mode") not in preferred_modes:
            continue
        if expected_behavior is not None and case.get("expected_behavior") != expected_behavior:
            continue
        return case
    return None


def build_documents(repo_root: Path) -> dict[Path, str]:
    generated_dir = repo_root / "generated"
    config_dir = repo_root / "config"

    catalog_doc = load_json(generated_dir / "skill_catalog.min.json")
    capsule_doc = load_json(generated_dir / "skill_capsules.json")
    local_manifest = load_json(generated_dir / "local_adapter_manifest.json")
    description_signals = load_json(generated_dir / "skill_description_signals.json")
    base_cases = load_jsonl(generated_dir / "skill_trigger_eval_cases.jsonl")
    description_cases = load_jsonl(generated_dir / "description_trigger_eval_cases.jsonl")
    policy = load_json(config_dir / "tiny_router_skill_bands.json")

    catalog_by_name = {entry["name"]: entry for entry in catalog_doc.get("skills", [])}
    capsule_by_name = {entry["name"]: entry for entry in capsule_doc.get("skills", [])}
    local_by_name = {entry["name"]: entry for entry in local_manifest.get("skills", [])}
    description_by_name = {entry["name"]: entry for entry in description_signals.get("skills", [])}
    base_cases_by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    description_cases_by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in base_cases:
        base_cases_by_skill[case["skill_name"]].append(case)
    for case in description_cases:
        description_cases_by_skill[case["skill_name"]].append(case)

    band_definitions = {entry["id"]: entry for entry in policy.get("bands", [])}
    band_by_skill = {name: entry["band"] for name, entry in policy.get("skill_overrides", {}).items()}
    source_names = set(catalog_by_name)
    if (
        set(capsule_by_name) != source_names
        or set(local_by_name) != source_names
        or set(description_by_name) != source_names
        or set(band_by_skill) != source_names
    ):
        raise SystemExit("wave-9 tiny-router inputs are out of parity with current skill surfaces")

    signals: list[dict[str, Any]] = []
    capsules_min: list[dict[str, Any]] = []
    eval_cases: list[dict[str, Any]] = []

    for skill_name in sorted(source_names):
        catalog_entry = catalog_by_name[skill_name]
        capsule_entry = capsule_by_name[skill_name]
        local_entry = local_by_name[skill_name]
        description_entry = description_by_name[skill_name]
        override = policy["skill_overrides"][skill_name]
        band_id = band_by_skill[skill_name]
        band_entry = band_definitions[band_id]
        skill_description_cases = description_cases_by_skill.get(skill_name, [])
        skill_base_cases = base_cases_by_skill.get(skill_name, [])
        allow_implicit = bool(local_entry["allow_implicit_invocation"])
        positive_case = choose_case(
            skill_description_cases,
            preferred_classes=["should-trigger", "manual-invocation-required", "explicit-handle"],
        ) or choose_case(
            skill_base_cases,
            preferred_modes=["implicit", "explicit"],
            expected_behavior="invoke-skill",
        )
        negative_case = choose_case(
            skill_description_cases,
            preferred_classes=["should-not-trigger"],
        ) or choose_case(
            skill_base_cases,
            preferred_modes=["adjacent-negative"],
        )
        defer_case = choose_case(skill_description_cases, preferred_classes=["prefer-other-skill"])

        positive_cues = list(dict.fromkeys([*override["positive_cues"], *band_entry["cues"]]))
        negative_cues = list(dict.fromkeys(override["negative_cues"]))
        signal = {
            "name": skill_name,
            "band": band_id,
            "band_summary": band_entry["summary"],
            "scope": catalog_entry["scope"],
            "status": catalog_entry["status"],
            "invocation_mode": catalog_entry["invocation_mode"],
            "allow_implicit_invocation": allow_implicit,
            "manual_invocation_required": not allow_implicit,
            "project_overlay": catalog_entry["scope"] == "project",
            "summary": catalog_entry["summary"],
            "summary_short": short_summary(catalog_entry["summary"], 118),
            "description": local_entry["description"],
            "description_sha256": description_entry["description_sha256"],
            "positive_cues": positive_cues[:10],
            "negative_cues": negative_cues[:6],
            "cue_tokens": phrase_tokens(positive_cues)[:18],
            "negative_tokens": phrase_tokens(negative_cues)[:12],
            "auto_tokens": auto_tokens(
                skill_name,
                local_entry["description"],
                catalog_entry["summary"],
                capsule_entry["trigger_boundary_short"],
                positive_case["prompt"] if positive_case else "",
                negative_case["prompt"] if negative_case else "",
            ),
            "companions": policy.get("companions", {}).get(skill_name, []),
            "primary_positive_prompt": positive_case["prompt"] if positive_case else "",
            "primary_negative_prompt": negative_case["prompt"] if negative_case else "",
            "primary_defer_prompt": defer_case["prompt"] if defer_case else "",
        }
        signals.append(signal)
        capsules_min.append(
            {
                "name": skill_name,
                "band": band_id,
                "summary_short": signal["summary_short"],
                "cue_phrases": signal["positive_cues"][:6],
                "cue_tokens": signal["cue_tokens"][:8],
                "negative_phrases": signal["negative_cues"][:3],
                "manual_invocation_required": signal["manual_invocation_required"],
                "project_overlay": signal["project_overlay"],
                "companions": signal["companions"][:3],
                "description_sha256": signal["description_sha256"],
            }
        )

        if positive_case is not None:
            eval_cases.append(
                {
                    "case_id": f"tiny-positive-{skill_name}",
                    "stage": "stage-1-shortlist",
                    "prompt": positive_case["prompt"],
                    "expected_band": band_id,
                    "expected_top1": skill_name,
                    "expected_shortlist_includes": [skill_name],
                    "expected_manual_invocation": signal["manual_invocation_required"],
                    "repo_family_hint": overlay_family_hint(
                        skill_name,
                        signal["project_overlay"],
                    ),
                }
            )
        if negative_case is not None:
            eval_cases.append(
                {
                    "case_id": f"tiny-negative-{skill_name}",
                    "stage": "stage-1-shortlist",
                    "prompt": negative_case["prompt"],
                    "expected_band": None,
                    "expected_top1_not": skill_name,
                    "expected_shortlist_excludes": [skill_name],
                    "expected_manual_invocation": False,
                    "repo_family_hint": None,
                }
            )
        if defer_case is not None and defer_case.get("expected_skill") and defer_case["expected_skill"] != skill_name:
            eval_cases.append(
                {
                    "case_id": f"tiny-defer-{skill_name}",
                    "stage": "stage-1-shortlist",
                    "prompt": defer_case["prompt"],
                    "expected_band": band_id,
                    "expected_top1_not": skill_name,
                    "expected_shortlist_includes": [defer_case["expected_skill"]],
                    "expected_shortlist_excludes": [skill_name],
                    "expected_manual_invocation": False,
                    "repo_family_hint": overlay_family_hint(
                        skill_name,
                        signal["project_overlay"],
                    ),
                }
            )

    band_entries: list[dict[str, Any]] = []
    for band in policy.get("bands", []):
        skills = [entry for entry in signals if entry["band"] == band["id"]]
        band_entries.append(
            {
                "id": band["id"],
                "summary": band["summary"],
                "cues": band["cues"],
                "skills": [entry["name"] for entry in skills],
                "manual_only_skills": [entry["name"] for entry in skills if entry["manual_invocation_required"]],
                "overlay_skills": [entry["name"] for entry in skills if entry["project_overlay"]],
            }
        )

    manifest = {
        "schema_version": 1,
        "profile": PROFILE,
        "source_files": [
            "generated/skill_capsules.json",
            "generated/skill_catalog.min.json",
            "generated/local_adapter_manifest.json",
            "generated/skill_trigger_eval_cases.jsonl",
            "generated/description_trigger_eval_cases.jsonl",
            "config/tiny_router_skill_bands.json",
        ],
        "skill_count": len(signals),
        "band_count": len(band_entries),
        "case_count": len(eval_cases),
        "skills": [
            {
                "name": entry["name"],
                "band": entry["band"],
                "manual_invocation_required": entry["manual_invocation_required"],
                "project_overlay": entry["project_overlay"],
                "description_sha256": entry["description_sha256"],
            }
            for entry in signals
        ],
    }

    return {
        repo_root / GENERATED_FILES["signals"]: dump_json(
            {
                "schema_version": 1,
                "profile": PROFILE,
                "skill_count": len(signals),
                "band_count": len(band_entries),
                "skills": signals,
            }
        ),
        repo_root / GENERATED_FILES["bands"]: dump_json(
            {
                "schema_version": 1,
                "profile": PROFILE,
                "band_count": len(band_entries),
                "bands": band_entries,
            }
        ),
        repo_root / GENERATED_FILES["capsules"]: dump_json(
            {
                "schema_version": 1,
                "profile": PROFILE,
                "skill_count": len(capsules_min),
                "skills": capsules_min,
            }
        ),
        repo_root / GENERATED_FILES["eval_cases"]: dump_jsonl(eval_cases),
        repo_root / GENERATED_FILES["manifest"]: dump_json(manifest),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build wave-9 tiny-router input surfaces.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--check", action="store_true", help="Check whether generated outputs are current.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    file_map = build_documents(repo_root)
    release_doc = release_manifest_contract.build_release_manifest(
        repo_root,
        file_overrides=file_map,
    )
    file_map[repo_root / "generated" / "release_manifest.json"] = dump_json(release_doc)
    for path, text in file_map.items():
        render_or_check(path, text, args.check, repo_root)
    print(json.dumps({"status": "ok", "repo_root": str(repo_root), "check": args.check}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
