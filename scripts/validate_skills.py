#!/usr/bin/env python3
"""Local validator for aoa-skills bundles."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml
from jsonschema import Draft202012Validator

import build_catalog
import skill_catalog_contract


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
SKILL_INDEX_NAME = "SKILL_INDEX.md"
SCHEMAS_DIR_NAME = "schemas"
SKILL_NAME_PATTERN = r"(?:aoa|atm10|abyss)-[a-z0-9-]+"
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"
EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"

REQUIRED_HEADINGS = {
    "Intent",
    "Trigger boundary",
    "Inputs",
    "Outputs",
    "Procedure",
    "Contracts",
    "Risks and anti-patterns",
    "Verification",
    "Adaptation points",
}
TRACEABILITY_HEADINGS = {"Technique traceability", "Future traceability"}
EXPECTED_TECHNIQUE_REPO = skill_catalog_contract.EXPECTED_TECHNIQUE_REPO


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / SCHEMAS_DIR_NAME / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local aoa-skills bundles.")
    parser.add_argument(
        "--skill",
        help="Validate a single skill bundle by directory name.",
    )
    return parser.parse_args(argv)


def load_yaml_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(relative_location(path), f"invalid YAML: {exc}")
        )
        return None
    return data


def relative_location(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    validator = get_schema_validator(schema_name)
    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def parse_skill_markdown(
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, dict[str, str]]:
    try:
        text = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))
        return None, {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, {}

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter closing delimiter",
            )
        )
        return None, {}

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, {}

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, {}

    sections = build_catalog.parse_skill_sections(body)
    return metadata, sections


def find_support_artifacts(skill_dir: Path) -> list[Path]:
    artifacts: list[Path] = []
    for folder_name in ("examples", "checks"):
        folder = skill_dir / folder_name
        if folder.is_dir():
            artifacts.extend(sorted(folder.glob("*.md")))
    return artifacts


def validate_skill_bundle(repo_root: Path, skill_name: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    techniques_path = skill_dir / "techniques.yaml"
    policy_path = skill_dir / "agents" / "openai.yaml"

    if not skill_dir.is_dir():
        issues.append(
            ValidationIssue(relative_location(skill_dir), "skill directory is missing")
        )
        return issues

    if not skill_md_path.is_file():
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))

    if not techniques_path.is_file():
        issues.append(
            ValidationIssue(relative_location(techniques_path), "file is missing")
        )

    if not find_support_artifacts(skill_dir):
        issues.append(
            ValidationIssue(
                relative_location(skill_dir),
                "missing support artifact under examples/*.md or checks/*.md",
            )
        )

    metadata: dict[str, Any] | None = None
    sections: dict[str, str] = {}
    techniques_data: dict[str, Any] | None = None
    if skill_md_path.is_file():
        metadata, sections = parse_skill_markdown(skill_md_path, issues)
        if metadata is not None:
            headings = set(sections)
            validate_skill_frontmatter(skill_name, metadata, skill_md_path, issues)
            validate_skill_headings(headings, skill_md_path, issues)
            validate_capsule_source_sections(sections, skill_md_path, issues)

    if techniques_path.is_file():
        techniques_data = load_yaml_file(techniques_path, issues)
        if techniques_data is not None:
            validate_techniques_manifest(
                skill_name,
                techniques_data,
                techniques_path,
                issues,
            )

    if policy_path.is_file():
        policy_data = load_yaml_file(policy_path, issues)
        if policy_data is not None:
            validate_policy_file(policy_data, policy_path, issues)

    if metadata and metadata.get("invocation_mode") == "explicit-only":
        validate_explicit_only_policy(policy_path, issues)

    if metadata is not None and techniques_data is not None:
        validate_skill_manifest_parity(
            skill_name,
            metadata,
            techniques_data,
            skill_md_path,
            techniques_path,
            issues,
        )
        validate_status_floors(
            repo_root,
            skill_name,
            metadata,
            set(sections),
            techniques_data,
            skill_dir,
            skill_md_path,
            techniques_path,
            issues,
        )

    return issues


def validate_skill_frontmatter(
    skill_name: str,
    metadata: dict[str, Any],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    if not validate_against_schema(metadata, "skill-frontmatter.schema.json", location, issues):
        return

    if metadata.get("name") != skill_name:
        issues.append(
            ValidationIssue(location, "frontmatter 'name' must match the directory name")
        )


def validate_skill_headings(
    headings: set[str],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    for heading in sorted(REQUIRED_HEADINGS - headings):
        issues.append(ValidationIssue(location, f"missing required section '{heading}'"))

    if not TRACEABILITY_HEADINGS.intersection(headings):
        issues.append(
            ValidationIssue(
                location,
                "missing traceability section; expected 'Technique traceability' or "
                "'Future traceability'",
            )
        )


def validate_capsule_source_sections(
    sections: dict[str, str],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    for section_name in build_catalog.CAPSULE_REQUIRED_SECTIONS:
        if section_name not in sections:
            continue
        if not sections[section_name].strip():
            issues.append(
                ValidationIssue(
                    location,
                    f"capsule source section '{section_name}' must not be empty",
                )
            )


def validate_techniques_manifest(
    skill_name: str,
    manifest: Any,
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(techniques_path)
    if not isinstance(manifest, dict):
        issues.append(ValidationIssue(location, "manifest must parse to a mapping"))
        return

    validate_against_schema(
        manifest,
        "techniques.schema.json",
        location,
        issues,
    )

    if manifest.get("skill_name") != skill_name:
        issues.append(
            ValidationIssue(location, "'skill_name' must match the directory name")
        )

    techniques = manifest.get("techniques")
    if not isinstance(techniques, list):
        return

    for contract_issue in skill_catalog_contract.collect_technique_ref_issues(
        manifest,
        techniques_path,
        techniques_path.parents[2],
    ):
        issues.append(
            ValidationIssue(contract_issue.location, contract_issue.message)
        )

    notes = manifest.get("notes")
    pending_ids: list[str] = []
    for technique in techniques:
        if not isinstance(technique, dict):
            continue
        technique_id = technique.get("id")
        if isinstance(technique_id, str) and technique_id.startswith("AOA-T-PENDING-"):
            pending_ids.append(technique_id)

    if pending_ids and not has_pending_note(notes, pending_ids):
        issues.append(
            ValidationIssue(
                location,
                "pending techniques require a note explaining that pending IDs and "
                "path/source_ref TBD must be replaced after publication",
            )
        )


def has_pending_note(notes: Any, pending_ids: Iterable[str]) -> bool:
    if not isinstance(notes, list):
        return False

    pending_tokens = [pending_id.lower() for pending_id in pending_ids]
    for note in notes:
        if not isinstance(note, str):
            continue
        lowered = note.lower()
        if "replace" not in lowered:
            continue
        if "path" not in lowered:
            continue
        if "source_ref" not in lowered:
            continue
        if "publish" not in lowered:
            continue
        if "pending" in lowered or any(token in lowered for token in pending_tokens):
            return True
    return False


def validate_policy_file(
    policy_data: Any,
    policy_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(policy_path)
    validate_against_schema(policy_data, "openai-policy.schema.json", location, issues)


def validate_explicit_only_policy(
    policy_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(policy_path)
    if not policy_path.is_file():
        issues.append(
            ValidationIssue(
                location,
                "explicit-only skills require agents/openai.yaml",
            )
        )
        return

    policy_issues: list[ValidationIssue] = []
    policy_data = load_yaml_file(policy_path, policy_issues)
    if policy_issues:
        issues.extend(policy_issues)
        return

    if not isinstance(policy_data, dict):
        issues.append(ValidationIssue(location, "policy file must parse to a mapping"))
        return

    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        issues.append(ValidationIssue(location, "missing mapping 'policy'"))
        return

    if policy.get("allow_implicit_invocation") is not False:
        issues.append(
            ValidationIssue(
                location,
                "explicit-only skills must set 'policy.allow_implicit_invocation' to false",
            )
        )


def status_requires_floor(status: str, floor: str) -> bool:
    floors = {
        "linked": {"linked", "reviewed", "evaluated", "canonical"},
        "reviewed": {"reviewed", "evaluated", "canonical"},
        "evaluated": {"evaluated", "canonical"},
        "canonical": {"canonical"},
    }
    return status in floors[floor]


def validate_status_floors(
    repo_root: Path,
    skill_name: str,
    metadata: dict[str, Any],
    headings: set[str],
    techniques_data: dict[str, Any],
    skill_dir: Path,
    skill_md_path: Path,
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    status = metadata.get("status")
    if not isinstance(status, str):
        return

    if status_requires_floor(status, "linked"):
        validate_linked_floor(status, techniques_data, techniques_path, issues)

    if status_requires_floor(status, "reviewed"):
        validate_reviewed_floor(repo_root, status, skill_name, skill_dir, skill_md_path, issues)

    if status_requires_floor(status, "canonical"):
        validate_canonical_floor(
            metadata,
            headings,
            techniques_data,
            skill_md_path,
            techniques_path,
            issues,
        )


def validate_linked_floor(
    status: str,
    techniques_data: dict[str, Any],
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(techniques_path)
    for technique in techniques_data.get("techniques", []):
        technique_id = technique.get("id", "")
        if technique_id.startswith("AOA-T-PENDING-"):
            continue
        if technique.get("source_ref") == "TBD":
            issues.append(
                ValidationIssue(
                    location,
                    f"status '{status}' requires published techniques to use concrete source_ref values",
                )
            )
            return


def has_review_evidence(repo_root: Path, skill_name: str, skill_dir: Path) -> bool:
    candidate_paths = [
        skill_dir / "checks" / "review.md",
        repo_root / STATUS_PROMOTION_REVIEWS_DIR / f"{skill_name}.md",
        repo_root / CANONICAL_CANDIDATES_DIR / f"{skill_name}.md",
    ]
    return any(path.is_file() for path in candidate_paths)


def validate_reviewed_floor(
    repo_root: Path,
    status: str,
    skill_name: str,
    skill_dir: Path,
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    if has_review_evidence(repo_root, skill_name, skill_dir):
        return

    issues.append(
        ValidationIssue(
            relative_location(skill_md_path),
            f"status '{status}' requires review evidence via checks/review.md or a public review record",
        )
    )


def validate_canonical_floor(
    metadata: dict[str, Any],
    headings: set[str],
    techniques_data: dict[str, Any],
    skill_md_path: Path,
    techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    skill_location = relative_location(skill_md_path)
    techniques_location = relative_location(techniques_path)

    dependencies = metadata.get("technique_dependencies", [])
    if any(
        isinstance(dependency, str) and dependency.startswith("AOA-T-PENDING-")
        for dependency in dependencies
    ):
        issues.append(
            ValidationIssue(
                skill_location,
                "status 'canonical' cannot use pending technique_dependencies",
            )
        )

    if "Technique traceability" not in headings or "Future traceability" in headings:
        issues.append(
            ValidationIssue(
                skill_location,
                "status 'canonical' requires 'Technique traceability' and forbids legacy 'Future traceability'",
            )
        )

    for technique in techniques_data.get("techniques", []):
        if technique.get("id", "").startswith("AOA-T-PENDING-"):
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' cannot use pending techniques in techniques.yaml",
                )
            )
            break

    for technique in techniques_data.get("techniques", []):
        if technique.get("path") == "TBD" or technique.get("source_ref") == "TBD":
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' requires concrete path and source_ref for every technique",
                )
            )
            break


def load_evaluation_fixtures(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    fixtures_path = repo_root / EVALUATION_FIXTURES_PATH
    data = load_yaml_file(fixtures_path, issues)
    if data is None:
        return None
    if not isinstance(data, dict):
        issues.append(
            ValidationIssue(
                relative_location(fixtures_path),
                "evaluation fixtures must parse to a mapping",
            )
        )
        return None
    return data


def validate_evaluation_floors(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skills_requiring_evaluation: dict[str, str] = {}

    for skill_name in target_skills:
        metadata, _sections = parse_skill_markdown(
            repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md",
            [],
        )
        if metadata is None:
            continue
        status = metadata.get("status")
        if isinstance(status, str) and status_requires_floor(status, "evaluated"):
            skills_requiring_evaluation[skill_name] = status

    if not skills_requiring_evaluation:
        return issues

    fixtures = load_evaluation_fixtures(repo_root, issues)
    if fixtures is None:
        return issues

    autonomy_skills = {
        check["skill"]
        for check in fixtures.get("autonomy_checks", [])
        if isinstance(check, dict) and isinstance(check.get("skill"), str)
    }
    trigger_case_counts: dict[str, dict[str, int]] = {}
    for case in fixtures.get("trigger_cases", []):
        if not isinstance(case, dict):
            continue
        skill_name = case.get("skill")
        expected = case.get("expected")
        if not isinstance(skill_name, str) or expected not in {"use", "do_not_use"}:
            continue
        counts = trigger_case_counts.setdefault(skill_name, {"use": 0, "do_not_use": 0})
        counts[expected] += 1

    fixtures_location = EVALUATION_FIXTURES_PATH.as_posix()
    for skill_name, status in skills_requiring_evaluation.items():
        if skill_name not in autonomy_skills:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires an autonomy_check entry",
                )
            )
        if trigger_case_counts.get(skill_name, {}).get("use", 0) < 1:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires at least one 'use' trigger case",
                )
            )
        if trigger_case_counts.get(skill_name, {}).get("do_not_use", 0) < 1:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires at least one 'do_not_use' trigger case",
                )
            )

    return issues


def validate_skill_index(
    repo_root: Path,
    selected_skills: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_path = repo_root / SKILL_INDEX_NAME
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(SKILL_INDEX_NAME, "file is missing")]

    pattern = re.compile(rf"^\|\s*({SKILL_NAME_PATTERN})\s*\|", flags=re.MULTILINE)
    names = pattern.findall(text)
    counts = Counter(names)
    location = relative_location(index_path)

    if selected_skills is None:
        skill_dirs = {
            path.name
            for path in (repo_root / SKILLS_DIR_NAME).iterdir()
            if path.is_dir()
        }
        for name, count in sorted(counts.items()):
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"skill '{name}' appears {count} times in the index",
                    )
                )

        for missing in sorted(skill_dirs - counts.keys()):
            issues.append(
                ValidationIssue(location, f"skill '{missing}' is missing from the index")
            )

        for extra in sorted(counts.keys() - skill_dirs):
            issues.append(
                ValidationIssue(
                    location,
                    f"index lists '{extra}' but no matching skill directory exists",
                )
            )
    else:
        for name in sorted(selected_skills):
            count = counts.get(name, 0)
            if count == 0:
                issues.append(
                    ValidationIssue(location, f"skill '{name}' is missing from the index")
                )
            elif count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"skill '{name}' appears {count} times in the index",
                    )
                )

    return issues


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def technique_ids_from_manifest(manifest: dict[str, Any]) -> list[str]:
    techniques = manifest.get("techniques", [])
    if not isinstance(techniques, list):
        return []
    return [technique.get("id") for technique in techniques if isinstance(technique, dict)]


def validate_skill_manifest_parity(
    skill_name: str,
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    skill_md_path: Path,
    _techniques_path: Path,
    issues: list[ValidationIssue],
) -> None:
    for contract_issue in skill_catalog_contract.collect_skill_parity_issues(
        skill_name,
        metadata,
        manifest,
        skill_md_path,
        skill_md_path.parents[2],
    ):
        if contract_issue.message == "frontmatter 'name' must match the directory name":
            continue
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))


def catalog_entries_by_name(
    catalog: dict[str, Any],
    *,
    array_key: str,
    key_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    entries = catalog.get(array_key)
    if not isinstance(entries, list):
        issues.append(
            ValidationIssue(location, f"catalog field '{array_key}' must be a list")
        )
        return {}

    entry_map: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(
                ValidationIssue(
                    location,
                    f"catalog field '{array_key}[{index}]' must be an object",
                )
            )
            continue
        name = entry.get(key_name)
        if not isinstance(name, str):
            issues.append(
                ValidationIssue(
                    location,
                    f"catalog field '{array_key}[{index}].{key_name}' must be a string",
                )
            )
            continue
        entry_map[name] = entry
    return entry_map


def validate_generated_catalogs(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / build_catalog.FULL_CATALOG_PATH
    min_path = repo_root / build_catalog.MIN_CATALOG_PATH

    full_text: str | None = None
    min_text: str | None = None
    full_data: dict[str, Any] | None = None
    min_data: dict[str, Any] | None = None

    for path in (full_path, min_path):
        if not path.is_file():
            issues.append(
                ValidationIssue(relative_location(path), "generated catalog is missing")
            )

    if full_path.is_file():
        full_text = full_path.read_text(encoding="utf-8")
        try:
            parsed = json.loads(full_text)
        except json.JSONDecodeError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(full_path),
                    f"invalid JSON: {exc.msg}",
                )
            )
        else:
            if isinstance(parsed, dict):
                full_data = parsed
            else:
                issues.append(
                    ValidationIssue(
                        relative_location(full_path),
                        "catalog must parse to an object",
                    )
                )

    if min_path.is_file():
        min_text = min_path.read_text(encoding="utf-8")
        try:
            parsed = json.loads(min_text)
        except json.JSONDecodeError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(min_path),
                    f"invalid JSON: {exc.msg}",
                )
            )
        else:
            if isinstance(parsed, dict):
                min_data = parsed
            else:
                issues.append(
                    ValidationIssue(
                        relative_location(min_path),
                        "catalog must parse to an object",
                    )
                )

    if full_data is None or min_data is None:
        return issues

    if skill_names is None:
        projected_min = build_catalog.project_min_catalog(full_data)
        if min_data != projected_min:
            issues.append(
                ValidationIssue(
                    relative_location(min_path),
                    "min catalog must be an exact projection of the full catalog",
                )
            )

        try:
            expected_full_text, expected_min_text = build_catalog.build_catalog_texts(repo_root)
        except (FileNotFoundError, ValueError):
            return issues

        if full_text is not None and full_text != expected_full_text:
            issues.append(
                ValidationIssue(
                    relative_location(full_path),
                    "generated catalog is out of date; run python scripts/build_catalog.py",
                )
            )
        if min_text is not None and min_text != expected_min_text:
            issues.append(
                ValidationIssue(
                    relative_location(min_path),
                    "generated catalog is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    full_location = relative_location(full_path)
    min_location = relative_location(min_path)
    actual_full_entries = catalog_entries_by_name(
        full_data,
        array_key="skills",
        key_name="name",
        location=full_location,
        issues=issues,
    )
    actual_min_entries = catalog_entries_by_name(
        min_data,
        array_key="skills",
        key_name="name",
        location=min_location,
        issues=issues,
    )

    for skill_name in skill_names:
        expected_full_entry = build_catalog.build_skill_entry(repo_root, skill_name)
        expected_min_entry = build_catalog.project_min_catalog(
            {
                "catalog_version": build_catalog.CATALOG_VERSION,
                "source_of_truth": build_catalog.SOURCE_OF_TRUTH,
                "skills": [expected_full_entry],
            }
        )["skills"][0]

        actual_full_entry = actual_full_entries.get(skill_name)
        actual_min_entry = actual_min_entries.get(skill_name)
        if actual_full_entry is None:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog is missing skill '{skill_name}'",
                )
            )
            continue
        if actual_min_entry is None:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog is missing skill '{skill_name}'",
                )
            )
            continue

        if actual_full_entry != expected_full_entry:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )
        if actual_min_entry != expected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )
        projected_min_entry = build_catalog.project_min_catalog(
            {
                "catalog_version": full_data.get("catalog_version"),
                "source_of_truth": full_data.get("source_of_truth"),
                "skills": [actual_full_entry],
            }
        )["skills"][0]
        if actual_min_entry != projected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{skill_name}' must stay a projection of the full catalog",
                )
            )

    return issues


def validate_capsule_catalog_alignment(
    catalog_data: dict[str, Any],
    capsule_data: dict[str, Any],
    *,
    skill_names: Sequence[str] | None,
    issues: list[ValidationIssue],
    catalog_location: str,
    capsule_location: str,
) -> None:
    starting_issue_count = len(issues)
    catalog_entries = catalog_entries_by_name(
        catalog_data,
        array_key="skills",
        key_name="name",
        location=catalog_location,
        issues=issues,
    )
    capsule_entries = catalog_entries_by_name(
        capsule_data,
        array_key="skills",
        key_name="name",
        location=capsule_location,
        issues=issues,
    )
    if len(issues) != starting_issue_count:
        return

    if skill_names is None:
        missing = sorted(set(catalog_entries) - set(capsule_entries))
        extra = sorted(set(capsule_entries) - set(catalog_entries))
        for skill_name in missing:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    f"generated capsules are missing skill '{skill_name}'",
                )
            )
        for skill_name in extra:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    f"generated capsules include unknown skill '{skill_name}'",
                )
            )
        target_names = sorted(set(catalog_entries) & set(capsule_entries))
    else:
        target_names = list(skill_names)

    shared_fields = (
        "scope",
        "status",
        "summary",
        "invocation_mode",
        "technique_dependencies",
        "skill_path",
    )
    for skill_name in target_names:
        catalog_entry = catalog_entries.get(skill_name)
        capsule_entry = capsule_entries.get(skill_name)
        if catalog_entry is None or capsule_entry is None:
            continue
        for field_name in shared_fields:
            if capsule_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        capsule_location,
                        f"generated capsule entry for '{skill_name}' must align with full catalog field '{field_name}'",
                    )
                )


def validate_generated_capsules(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    capsule_path = repo_root / build_catalog.CAPSULE_PATH

    capsule_text: str | None = None
    capsule_data: dict[str, Any] | None = None

    if not capsule_path.is_file():
        issues.append(
            ValidationIssue(relative_location(capsule_path), "generated capsules are missing")
        )
        return issues

    capsule_text = capsule_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(capsule_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                "capsules must parse to an object",
            )
        )
        return issues

    capsule_data = parsed
    if capsule_data.get("capsule_version") != build_catalog.CAPSULE_VERSION:
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                f"capsule_version must be {build_catalog.CAPSULE_VERSION}",
            )
        )
    if capsule_data.get("source_of_truth") != build_catalog.CAPSULE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                "capsule source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(capsule_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                relative_location(capsule_path),
                "capsules field 'skills' must be a list",
            )
        )
        return issues

    if skill_names is None:
        try:
            expected_capsule_text = build_catalog.build_capsule_text(repo_root)
        except (FileNotFoundError, ValueError) as exc:
            issues.append(
                ValidationIssue(
                    relative_location(capsule_path),
                    f"capsule source validation failed: {exc}",
                )
            )
            return issues

        if capsule_text != expected_capsule_text:
            issues.append(
                ValidationIssue(
                    relative_location(capsule_path),
                    "generated capsules are out of date; run python scripts/build_catalog.py",
                )
            )
    else:
        capsule_entries = catalog_entries_by_name(
            capsule_data,
            array_key="skills",
            key_name="name",
            location=relative_location(capsule_path),
            issues=issues,
        )
        for skill_name in skill_names:
            try:
                expected_capsule_entry = build_catalog.build_skill_capsule_entry(
                    repo_root, skill_name
                )
            except (FileNotFoundError, ValueError) as exc:
                issues.append(
                    ValidationIssue(
                        relative_location(capsule_path),
                        f"capsule source validation failed for '{skill_name}': {exc}",
                    )
                )
                continue

            actual_capsule_entry = capsule_entries.get(skill_name)
            if actual_capsule_entry is None:
                issues.append(
                    ValidationIssue(
                        relative_location(capsule_path),
                        f"generated capsules are missing skill '{skill_name}'",
                    )
                )
                continue
            if actual_capsule_entry != expected_capsule_entry:
                issues.append(
                    ValidationIssue(
                        relative_location(capsule_path),
                        f"generated capsule entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                    )
                )

    full_catalog_path = repo_root / build_catalog.FULL_CATALOG_PATH
    if full_catalog_path.is_file():
        try:
            full_catalog_data = json.loads(full_catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return issues
        if isinstance(full_catalog_data, dict):
            validate_capsule_catalog_alignment(
                full_catalog_data,
                capsule_data,
                skill_names=skill_names,
                issues=issues,
                catalog_location=relative_location(full_catalog_path),
                capsule_location=relative_location(capsule_path),
            )

    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(repo_root: Path, skill_name: str | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    all_skill_names = discover_skill_names(repo_root)
    bundle_issues_by_name: dict[str, list[ValidationIssue]] = {}
    if skill_name is not None:
        if skill_name not in all_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        target_skills = [skill_name]
        selected_skills = {skill_name}
    else:
        target_skills = all_skill_names
        selected_skills = None

    for name in target_skills:
        bundle_issues = validate_skill_bundle(repo_root, name)
        bundle_issues_by_name[name] = bundle_issues
        issues.extend(bundle_issues)

    issues.extend(validate_evaluation_floors(repo_root, target_skills))
    issues.extend(validate_skill_index(repo_root, selected_skills=selected_skills))
    if skill_name is None:
        issues.extend(validate_generated_catalogs(repo_root))
        issues.extend(validate_generated_capsules(repo_root))
    elif all(not bundle_issues_by_name[name] for name in target_skills):
        issues.extend(validate_generated_catalogs(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_capsules(repo_root, skill_names=target_skills))
    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        issues = run_validation(repo_root, skill_name=args.skill)
    except ValueError as exc:
        print(f"Argument error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    if issues:
        scope = args.skill if args.skill else "repository"
        print(f"Validation failed for {scope}.")
        print(format_issues(issues))
        return 1

    if args.skill:
        print(f"Validation passed for skill '{args.skill}'.")
    else:
        skill_count = len(discover_skill_names(repo_root))
        print(f"Validation passed for {skill_count} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
