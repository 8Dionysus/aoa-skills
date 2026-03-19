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
EXPECTED_TECHNIQUE_REPO = "aoa-techniques"


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
) -> tuple[dict[str, Any] | None, set[str]]:
    try:
        text = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))
        return None, set()

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, set()

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
        return None, set()

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
        return None, set()

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, set()

    headings = set(
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    )
    return metadata, headings


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
    headings: set[str] = set()
    techniques_data: dict[str, Any] | None = None
    if skill_md_path.is_file():
        metadata, headings = parse_skill_markdown(skill_md_path, issues)
        if metadata is not None:
            validate_skill_frontmatter(skill_name, metadata, skill_md_path, issues)
            validate_skill_headings(headings, skill_md_path, issues)

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
            headings,
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

    notes = manifest.get("notes")
    pending_ids: list[str] = []
    for index, technique in enumerate(techniques, start=1):
        if not isinstance(technique, dict):
            continue
        entry_location = f"{location} [technique #{index}]"
        technique_id = technique.get("id")
        repo_name = technique.get("repo")
        path_value = technique.get("path")
        source_ref = technique.get("source_ref")
        try:
            normalized_repo_name = build_catalog.normalize_repo_name(repo_name)
        except ValueError:
            normalized_repo_name = None
        if normalized_repo_name != EXPECTED_TECHNIQUE_REPO:
            issues.append(
                ValidationIssue(
                    entry_location,
                    f"repo must resolve to '{EXPECTED_TECHNIQUE_REPO}'",
                )
            )
        if not isinstance(technique_id, str):
            continue
        if technique_id.startswith("AOA-T-PENDING-"):
            pending_ids.append(technique_id)
            if path_value != "TBD":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "pending techniques must use path 'TBD'",
                    )
                )
            if source_ref != "TBD":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "pending techniques must use source_ref 'TBD'",
                    )
                )
        elif path_value == "TBD":
            issues.append(
                ValidationIssue(
                    entry_location,
                    "published techniques cannot use path 'TBD'",
                )
            )
        elif not build_catalog.is_repo_relative_path(path_value):
            issues.append(
                ValidationIssue(
                    entry_location,
                    "published techniques must use concrete repo-relative paths",
                )
            )
        elif source_ref == "TBD":
            issues.append(
                ValidationIssue(
                    entry_location,
                    "published techniques cannot use source_ref 'TBD'",
                )
            )

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
        metadata, _ = parse_skill_markdown(
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
    skill_location = relative_location(skill_md_path)
    manifest_skill_name = manifest.get("skill_name")
    if metadata.get("name") != manifest_skill_name:
        issues.append(
            ValidationIssue(
                skill_location,
                "frontmatter 'name' must match techniques.yaml 'skill_name'",
            )
        )

    dependencies = metadata.get("technique_dependencies")
    if not isinstance(dependencies, list):
        return

    manifest_ids = technique_ids_from_manifest(manifest)
    if dependencies != manifest_ids:
        issues.append(
            ValidationIssue(
                skill_location,
                "frontmatter 'technique_dependencies' must exactly match techniques.yaml technique IDs in order",
            )
        )


def validate_generated_catalogs(repo_root: Path) -> list[ValidationIssue]:
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

    if full_data is not None and min_data is not None:
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


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(repo_root: Path, skill_name: str | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    all_skill_names = discover_skill_names(repo_root)
    if skill_name is not None:
        if skill_name not in all_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        target_skills = [skill_name]
        selected_skills = {skill_name}
    else:
        target_skills = all_skill_names
        selected_skills = None

    for name in target_skills:
        issues.extend(validate_skill_bundle(repo_root, name))

    issues.extend(validate_evaluation_floors(repo_root, target_skills))
    issues.extend(validate_skill_index(repo_root, selected_skills=selected_skills))
    if skill_name is None:
        issues.extend(validate_generated_catalogs(repo_root))
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
