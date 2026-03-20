#!/usr/bin/env python3
"""Build deterministic derived skill catalogs and capsules for reader surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

import yaml

import skill_catalog_contract


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
GENERATED_DIR_NAME = "generated"
FULL_CATALOG_PATH = Path(GENERATED_DIR_NAME) / "skill_catalog.json"
MIN_CATALOG_PATH = Path(GENERATED_DIR_NAME) / "skill_catalog.min.json"
CAPSULE_PATH = Path(GENERATED_DIR_NAME) / "skill_capsules.json"
CATALOG_VERSION = 1
CAPSULE_VERSION = 1
SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
}
CAPSULE_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "frontmatter_fields": [
        "name",
        "scope",
        "status",
        "summary",
        "invocation_mode",
        "technique_dependencies",
    ],
    "sections": [
        "Intent",
        "Trigger boundary",
        "Inputs",
        "Outputs",
        "Procedure",
        "Risks and anti-patterns",
        "Verification",
    ],
}
CAPSULE_REQUIRED_SECTIONS = tuple(CAPSULE_SOURCE_OF_TRUTH["sections"])
SECTION_HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$")
LIST_ITEM_PATTERN = re.compile(r"^(?:[-*]|\d+\.)\s+(.*)$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
EMPHASIS_PATTERN = re.compile(r"(\*\*|\*|__|_)")
MAX_SHORT_FIELD_LENGTH = 220
MAX_WORKFLOW_SHORT_LENGTH = 260

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build derived reader catalogs for aoa-skills."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether generated catalogs are present and current.",
    )
    return parser.parse_args(argv)


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def relative_path(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def is_repo_relative_path(path_value: Any) -> bool:
    return skill_catalog_contract.is_repo_relative_path(path_value)


def normalize_repo_name(raw_repo: Any) -> str:
    return skill_catalog_contract.normalize_repo_name(raw_repo)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_skill_document(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} is missing frontmatter")

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise ValueError(f"{path} is missing a closing frontmatter delimiter")

    frontmatter_text = "\n".join(lines[1:closing_index])
    metadata = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"{path} frontmatter must parse to a mapping")
    body = "\n".join(lines[closing_index + 1 :])
    return metadata, body


def parse_skill_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []

    def flush_current() -> None:
        nonlocal current_heading, current_lines
        if current_heading is None:
            return
        sections[current_heading] = "\n".join(current_lines).strip()
        current_heading = None
        current_lines = []

    for line in body.splitlines():
        heading_match = SECTION_HEADING_PATTERN.match(line.strip())
        if heading_match:
            flush_current()
            current_heading = heading_match.group(1).strip()
            continue
        if current_heading is not None:
            current_lines.append(line)

    flush_current()
    return sections


def normalize_inline_markdown(text: str) -> str:
    normalized = MARKDOWN_LINK_PATTERN.sub(r"\1", text)
    normalized = INLINE_CODE_PATTERN.sub(r"\1", normalized)
    normalized = EMPHASIS_PATTERN.sub("", normalized)
    normalized = normalized.replace("\\", "")
    return " ".join(normalized.split())


def normalize_phrase(text: str) -> str:
    return normalize_inline_markdown(text).strip(" \t\r\n.;:")


def limit_text(text: str, limit: int) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    trimmed = collapsed[: limit - 3].rstrip(" ,;:-")
    if " " in trimmed:
        trimmed = trimmed.rsplit(" ", 1)[0]
    return f"{trimmed}..."


def ensure_sentence(text: str, limit: int) -> str:
    stripped = text.strip()
    if not stripped:
        return stripped
    if stripped[-1] not in ".!?":
        stripped += "."
    return limit_text(stripped, limit)


def extract_markdown_items(section_text: str) -> list[str]:
    items: list[str] = []
    current_item: str | None = None

    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        match = LIST_ITEM_PATTERN.match(stripped)
        if match:
            if current_item is not None:
                items.append(current_item)
            current_item = normalize_phrase(match.group(1))
            continue

        if current_item is not None and raw_line[:1].isspace():
            continuation = normalize_phrase(stripped)
            if continuation:
                current_item = f"{current_item} {continuation}".strip()
            continue

        if current_item is not None:
            items.append(current_item)
            current_item = None

        items.append(normalize_phrase(stripped))

    if current_item is not None:
        items.append(current_item)

    return [item for item in items if item]


def extract_first_sentence(section_text: str) -> str:
    normalized = normalize_inline_markdown(section_text.strip())
    if not normalized:
        return ""

    for delimiter in (". ", "! ", "? "):
        if delimiter in normalized:
            return normalized.split(delimiter, 1)[0].strip(" .!?")
    return normalized.strip(" .!?")


def extract_trigger_boundary_items(section_text: str) -> tuple[list[str], list[str]]:
    use_items: list[str] = []
    avoid_items: list[str] = []
    current_bucket: list[str] | None = None
    current_item: str | None = None

    def flush_current_item() -> None:
        nonlocal current_item
        if current_item is None or current_bucket is None:
            current_item = None
            return
        current_bucket.append(current_item)
        current_item = None

    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        normalized = normalize_inline_markdown(stripped)
        lowered = normalized.rstrip(":").lower()
        if lowered.startswith("use this skill when") or lowered.startswith("use when"):
            flush_current_item()
            current_bucket = use_items
            continue
        if lowered.startswith("do not use this skill when") or lowered.startswith("avoid when"):
            flush_current_item()
            current_bucket = avoid_items
            continue

        match = LIST_ITEM_PATTERN.match(stripped)
        if match:
            flush_current_item()
            current_item = normalize_phrase(match.group(1))
            continue

        if current_item is not None and raw_line[:1].isspace():
            continuation = normalize_phrase(stripped)
            if continuation:
                current_item = f"{current_item} {continuation}".strip()
            continue

        flush_current_item()
        if current_bucket is not None:
            current_bucket.append(normalize_phrase(normalized))

    flush_current_item()
    return [item for item in use_items if item], [item for item in avoid_items if item]


def build_compact_list_summary(
    prefix: str,
    section_text: str,
    *,
    limit: int = MAX_SHORT_FIELD_LENGTH,
    max_items: int = 4,
) -> str:
    items = extract_markdown_items(section_text)
    if items:
        text = f"{prefix}: {'; '.join(items[:max_items])}"
    else:
        sentence = extract_first_sentence(section_text)
        text = f"{prefix}: {sentence}" if sentence else prefix
    return ensure_sentence(text, limit)


def build_trigger_boundary_summary(section_text: str) -> str:
    use_items, avoid_items = extract_trigger_boundary_items(section_text)
    parts: list[str] = []
    if use_items:
        parts.append(f"Use when {'; '.join(use_items[:2])}")
    if avoid_items:
        parts.append(f"Avoid when {'; '.join(avoid_items[:2])}")
    if not parts:
        fallback = extract_first_sentence(section_text)
        parts.append(f"Use when {fallback}" if fallback else "Use when bounded context is clear")
    return ensure_sentence("; ".join(parts), MAX_SHORT_FIELD_LENGTH)


def build_intent_clause(intent_text: str) -> str:
    clause = extract_first_sentence(intent_text)
    if not clause:
        return ""

    lowered = clause.lower()
    prefixes = (
        "use this skill to ",
        "use this skill when ",
        "use ",
        "this skill helps ",
        "this skill is for ",
    )
    for prefix in prefixes:
        if lowered.startswith(prefix):
            clause = clause[len(prefix) :]
            break

    clause = normalize_phrase(clause)
    clause = re.sub(r"\bso the result\b", "to keep results", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bso that\b", "to", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bso\b", "to", clause, flags=re.IGNORECASE)
    return clause


def build_workflow_summary(intent_text: str, procedure_text: str) -> str:
    parts: list[str] = []
    intent_clause = build_intent_clause(intent_text)
    if intent_clause:
        parts.append(f"Purpose: {intent_clause}")

    steps = extract_markdown_items(procedure_text)
    if steps:
        parts.append(f"Flow: {' -> '.join(steps[:4])}")
    else:
        sentence = extract_first_sentence(procedure_text)
        if sentence:
            parts.append(f"Flow: {sentence}")

    if not parts:
        raise ValueError("workflow summary requires intent or procedure content")
    return ensure_sentence(". ".join(parts), MAX_WORKFLOW_SHORT_LENGTH)


def require_capsule_sections(skill_md_path: Path, body: str) -> dict[str, str]:
    sections = parse_skill_sections(body)
    for section_name in CAPSULE_REQUIRED_SECTIONS:
        if section_name not in sections:
            raise ValueError(
                f"{skill_md_path} capsule source section '{section_name}' is missing"
            )
        if not sections[section_name].strip():
            raise ValueError(
                f"{skill_md_path} capsule source section '{section_name}' must not be empty"
            )
    return sections


def technique_ids_from_manifest(manifest: dict[str, Any]) -> list[str]:
    return skill_catalog_contract.technique_ids_from_manifest(manifest)


def normalize_technique_refs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return skill_catalog_contract.normalize_technique_refs(manifest)


def build_skill_entry(repo_root: Path, skill_name: str) -> dict[str, Any]:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    techniques_path = skill_dir / "techniques.yaml"
    metadata, _body = parse_skill_document(skill_md_path)
    manifest = load_yaml(techniques_path)

    if not isinstance(manifest, dict):
        raise ValueError(f"{techniques_path} must parse to a mapping")

    entry, issues = skill_catalog_contract.build_skill_entry_from_sources(
        repo_root,
        skill_name,
        metadata,
        manifest,
        skill_md_path,
        techniques_path,
    )
    if issues:
        raise ValueError(skill_catalog_contract.format_issues(issues))
    if entry is None:
        raise ValueError(f"failed to build routing entry for {skill_name}")
    return entry


def build_skill_capsule_entry(repo_root: Path, skill_name: str) -> dict[str, Any]:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    metadata, body = parse_skill_document(skill_md_path)
    sections = require_capsule_sections(skill_md_path, body)

    technique_dependencies = metadata.get("technique_dependencies")
    if not isinstance(technique_dependencies, list) or not all(
        isinstance(item, str) for item in technique_dependencies
    ):
        raise ValueError(
            f"{skill_md_path} frontmatter 'technique_dependencies' must be a list of strings"
        )

    return {
        "name": metadata.get("name"),
        "scope": metadata.get("scope"),
        "status": metadata.get("status"),
        "summary": metadata.get("summary"),
        "trigger_boundary_short": build_trigger_boundary_summary(
            sections["Trigger boundary"]
        ),
        "inputs_short": build_compact_list_summary("Needs", sections["Inputs"]),
        "outputs_short": build_compact_list_summary("Produces", sections["Outputs"]),
        "workflow_short": build_workflow_summary(
            sections["Intent"],
            sections["Procedure"],
        ),
        "main_anti_patterns_short": build_compact_list_summary(
            "Avoid",
            sections["Risks and anti-patterns"],
        ),
        "verification_short": build_compact_list_summary(
            "Checks",
            sections["Verification"],
        ),
        "invocation_mode": metadata.get("invocation_mode"),
        "technique_dependencies": list(technique_dependencies),
        "skill_path": relative_path(skill_md_path, repo_root),
    }


def build_full_catalog(repo_root: Path) -> dict[str, Any]:
    skills = [
        build_skill_entry(repo_root, skill_name)
        for skill_name in discover_skill_names(repo_root)
    ]
    return {
        "catalog_version": CATALOG_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "skills": skills,
    }


def project_min_catalog(full_catalog: dict[str, Any]) -> dict[str, Any]:
    min_skills: list[dict[str, Any]] = []
    for skill in full_catalog["skills"]:
        min_skills.append(
            {
                "name": skill["name"],
                "scope": skill["scope"],
                "status": skill["status"],
                "summary": skill["summary"],
                "invocation_mode": skill["invocation_mode"],
                "technique_dependencies": skill["technique_dependencies"],
                "skill_path": skill["skill_path"],
            }
        )
    return {
        "catalog_version": full_catalog["catalog_version"],
        "source_of_truth": full_catalog["source_of_truth"],
        "skills": min_skills,
    }


def build_capsules_payload(repo_root: Path) -> dict[str, Any]:
    return {
        "capsule_version": CAPSULE_VERSION,
        "source_of_truth": CAPSULE_SOURCE_OF_TRUTH,
        "skills": [
            build_skill_capsule_entry(repo_root, skill_name)
            for skill_name in discover_skill_names(repo_root)
        ],
    }


def render_json(payload: dict[str, Any], *, indent: int | None) -> str:
    kwargs: dict[str, Any] = {
        "ensure_ascii": True,
        "sort_keys": True,
    }
    if indent is None:
        kwargs["separators"] = (",", ":")
    else:
        kwargs["indent"] = indent
    return json.dumps(payload, **kwargs) + "\n"


def build_catalog_texts(repo_root: Path) -> tuple[str, str]:
    full_catalog = build_full_catalog(repo_root)
    min_catalog = project_min_catalog(full_catalog)
    return render_json(full_catalog, indent=2), render_json(min_catalog, indent=None)


def build_capsule_text(repo_root: Path) -> str:
    return render_json(build_capsules_payload(repo_root), indent=2)


def write_catalogs(repo_root: Path) -> tuple[Path, Path]:
    generated_dir = repo_root / GENERATED_DIR_NAME
    generated_dir.mkdir(exist_ok=True)
    full_text, min_text = build_catalog_texts(repo_root)
    full_path = repo_root / FULL_CATALOG_PATH
    min_path = repo_root / MIN_CATALOG_PATH
    full_path.write_text(full_text, encoding="utf-8", newline="\n")
    min_path.write_text(min_text, encoding="utf-8", newline="\n")
    return full_path, min_path


def write_capsules(repo_root: Path) -> Path:
    generated_dir = repo_root / GENERATED_DIR_NAME
    generated_dir.mkdir(exist_ok=True)
    capsule_text = build_capsule_text(repo_root)
    capsule_path = repo_root / CAPSULE_PATH
    capsule_path.write_text(capsule_text, encoding="utf-8", newline="\n")
    return capsule_path


def check_catalogs(repo_root: Path) -> list[str]:
    problems: list[str] = []
    full_path = repo_root / FULL_CATALOG_PATH
    min_path = repo_root / MIN_CATALOG_PATH
    try:
        expected_full, expected_min = build_catalog_texts(repo_root)
    except ValueError as exc:
        return [f"source validation failed:\n{exc}"]

    for path in (full_path, min_path):
        if not path.is_file():
            problems.append(f"missing {relative_path(path, repo_root)}")

    if full_path.is_file() and full_path.read_text(encoding="utf-8") != expected_full:
        problems.append(f"stale {relative_path(full_path, repo_root)}")

    if min_path.is_file() and min_path.read_text(encoding="utf-8") != expected_min:
        problems.append(f"stale {relative_path(min_path, repo_root)}")

    return problems


def check_capsules(repo_root: Path) -> list[str]:
    problems: list[str] = []
    capsule_path = repo_root / CAPSULE_PATH
    try:
        expected_capsule = build_capsule_text(repo_root)
    except ValueError as exc:
        return [f"capsule source validation failed:\n{exc}"]

    if not capsule_path.is_file():
        problems.append(f"missing {relative_path(capsule_path, repo_root)}")
        return problems

    if capsule_path.read_text(encoding="utf-8") != expected_capsule:
        problems.append(f"stale {relative_path(capsule_path, repo_root)}")
    return problems


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.check:
            problems = check_catalogs(repo_root) + check_capsules(repo_root)
            if problems:
                print("Generated surface check failed.")
                for problem in problems:
                    print(f"- {problem}")
                return 1
            print(
                f"Generated surface check passed for {len(discover_skill_names(repo_root))} skills."
            )
            return 0

        full_path, min_path = write_catalogs(repo_root)
        capsule_path = write_capsules(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(
        "Generated surface build wrote "
        f"{relative_path(full_path, repo_root)}, "
        f"{relative_path(min_path, repo_root)}, and "
        f"{relative_path(capsule_path, repo_root)}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
