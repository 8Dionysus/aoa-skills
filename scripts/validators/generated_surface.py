"""Generated/read-model surface validators for aoa-skills."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

from jsonschema import Draft202012Validator

import build_catalog
import skill_governance_surface
import skill_layout
import skill_section_contract


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR_NAME = "schemas"
GENERATED_SURFACE_SCHEMA_BY_PATH = {
    build_catalog.PUBLIC_SURFACE_JSON_PATH: "public_surface.schema.json",
    build_catalog.WALKTHROUGHS_JSON_PATH: "skill_walkthroughs.schema.json",
    build_catalog.EVALUATION_MATRIX_JSON_PATH: "skill_evaluation_matrix.schema.json",
    build_catalog.LINEAGE_SURFACE_JSON_PATH: "skill_lineage_surface.schema.json",
    build_catalog.BOUNDARY_MATRIX_JSON_PATH: "skill_boundary_matrix.schema.json",
    build_catalog.GOVERNANCE_BACKLOG_JSON_PATH: "governance_backlog.schema.json",
    build_catalog.SKILL_COMPOSITION_AUDIT_JSON_PATH: "skill_composition_audit.schema.json",
    build_catalog.OVERLAY_READINESS_JSON_PATH: "overlay_readiness.schema.json",
    build_catalog.BUNDLE_INDEX_JSON_PATH: "skill_bundle_index.schema.json",
    build_catalog.SKILL_GRAPH_JSON_PATH: "skill_graph.schema.json",
}


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


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


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / Path(SCHEMAS_DIR_NAME) / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


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

    def project_min_catalog_safely(
        full_catalog: dict[str, Any],
        *,
        location: str,
        label: str,
    ) -> dict[str, Any] | None:
        try:
            return build_catalog.project_min_catalog(full_catalog)
        except (KeyError, TypeError):
            issues.append(
                ValidationIssue(
                    location,
                    f"{label} is malformed; min projection could not be computed",
                )
            )
            return None

    if skill_names is None:
        projected_min = project_min_catalog_safely(
            full_data,
            location=relative_location(full_path),
            label="generated catalog",
        )
        if projected_min is None:
            return issues
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
        projected_min_catalog_payload = project_min_catalog_safely(
            {
                "catalog_version": full_data.get("catalog_version"),
                "source_of_truth": full_data.get("source_of_truth"),
                "skills": [actual_full_entry],
            },
            location=full_location,
            label=f"generated catalog entry for '{skill_name}'",
        )
        if projected_min_catalog_payload is None:
            continue
        projected_min_entry = projected_min_catalog_payload["skills"][0]
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


def validate_sections_catalog_alignment(
    full_catalog_data: dict[str, Any],
    sections_data: dict[str, Any],
    *,
    skill_names: Sequence[str] | None,
    issues: list[ValidationIssue],
    catalog_location: str,
    sections_location: str,
) -> None:
    starting_issue_count = len(issues)
    catalog_entries = catalog_entries_by_name(
        full_catalog_data,
        array_key="skills",
        key_name="name",
        location=catalog_location,
        issues=issues,
    )
    section_entries = catalog_entries_by_name(
        sections_data,
        array_key="skills",
        key_name="name",
        location=sections_location,
        issues=issues,
    )
    if len(issues) != starting_issue_count:
        return

    if skill_names is None:
        missing = sorted(set(catalog_entries) - set(section_entries))
        extra = sorted(set(section_entries) - set(catalog_entries))
        for skill_name in missing:
            issues.append(
                ValidationIssue(
                    sections_location,
                    f"generated sections are missing skill '{skill_name}'",
                )
            )
        for skill_name in extra:
            issues.append(
                ValidationIssue(
                    sections_location,
                    f"generated sections include unknown skill '{skill_name}'",
                )
            )
        target_names = sorted(set(catalog_entries) & set(section_entries))
    else:
        target_names = list(skill_names)

    shared_fields = ("scope", "status", "skill_path")
    for skill_name in target_names:
        catalog_entry = catalog_entries.get(skill_name)
        section_entry = section_entries.get(skill_name)
        if catalog_entry is None or section_entry is None:
            continue
        for field_name in shared_fields:
            if section_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{skill_name}' must align with full catalog field '{field_name}'",
                    )
                )


def validate_generated_sections(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    sections_path = repo_root / build_catalog.SECTIONS_PATH
    sections_location = relative_location(sections_path)

    if not sections_path.is_file():
        issues.append(
            ValidationIssue(sections_location, "generated sections are missing")
        )
        return issues

    sections_text = sections_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(sections_text)
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(sections_location, f"invalid JSON: {exc.msg}"))
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(sections_location, "sections must parse to an object")
        )
        return issues

    sections_data = parsed
    if sections_data.get("section_version") != build_catalog.SECTION_VERSION:
        issues.append(
            ValidationIssue(
                sections_location,
                f"section_version must be {build_catalog.SECTION_VERSION}",
            )
        )
    if sections_data.get("source_of_truth") != skill_section_contract.SECTION_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                sections_location,
                "section source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(sections_data.get("skills"), list):
        issues.append(
            ValidationIssue(sections_location, "sections field 'skills' must be a list")
        )
        return issues

    if skill_names is None:
        try:
            expected_sections_text = build_catalog.build_sections_text(repo_root)
        except (FileNotFoundError, ValueError) as exc:
            issues.append(
                ValidationIssue(
                    sections_location,
                    f"section source validation failed: {exc}",
                )
            )
            return issues

        if sections_text != expected_sections_text:
            issues.append(
                ValidationIssue(
                    sections_location,
                    "generated sections are out of date; run python scripts/build_catalog.py",
                )
            )
    else:
        section_entries = catalog_entries_by_name(
            sections_data,
            array_key="skills",
            key_name="name",
            location=sections_location,
            issues=issues,
        )
        for skill_name in skill_names:
            skill_md_path = skill_layout.skill_md_path(repo_root, skill_name)
            try:
                metadata, body = build_catalog.parse_skill_document(skill_md_path)
                expected_section_entry, contract_issues = skill_section_contract.build_sections_entry(
                    repo_root,
                    metadata,
                    skill_md_path,
                    body,
                )
            except (FileNotFoundError, ValueError) as exc:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"section source validation failed for '{skill_name}': {exc}",
                    )
                )
                continue

            for contract_issue in contract_issues:
                issues.append(
                    ValidationIssue(contract_issue.location, contract_issue.message)
                )
            if contract_issues or expected_section_entry is None:
                continue

            actual_section_entry = section_entries.get(skill_name)
            if actual_section_entry is None:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated sections are missing skill '{skill_name}'",
                    )
                )
                continue
            if actual_section_entry != expected_section_entry:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                    )
                )

    full_catalog_path = repo_root / build_catalog.FULL_CATALOG_PATH
    if full_catalog_path.is_file():
        try:
            full_catalog_data = json.loads(full_catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return issues
        if isinstance(full_catalog_data, dict):
            validate_sections_catalog_alignment(
                full_catalog_data,
                sections_data,
                skill_names=skill_names,
                issues=issues,
                catalog_location=relative_location(full_catalog_path),
                sections_location=sections_location,
            )

    return issues


def validate_generated_walkthroughs(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    walkthrough_path = repo_root / build_catalog.WALKTHROUGHS_JSON_PATH
    walkthrough_markdown_path = repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH
    walkthrough_location = relative_location(walkthrough_path)
    walkthrough_markdown_location = relative_location(walkthrough_markdown_path)

    if not walkthrough_path.is_file():
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "generated walkthrough surface is missing",
            )
        )
        if not walkthrough_markdown_path.is_file():
            issues.append(
                ValidationIssue(
                    walkthrough_markdown_location,
                    "generated walkthrough markdown is missing",
                )
            )
        return issues

    if not walkthrough_markdown_path.is_file():
        issues.append(
            ValidationIssue(
                walkthrough_markdown_location,
                "generated walkthrough markdown is missing",
            )
        )
        return issues

    walkthrough_text = walkthrough_path.read_text(encoding="utf-8")
    walkthrough_markdown_text = walkthrough_markdown_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(walkthrough_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "walkthrough surface must parse to an object",
            )
        )
        return issues

    walkthrough_data = parsed
    validate_against_schema(
        walkthrough_data,
        GENERATED_SURFACE_SCHEMA_BY_PATH[build_catalog.WALKTHROUGHS_JSON_PATH],
        walkthrough_location,
        issues,
    )
    if walkthrough_data.get("walkthrough_version") != build_catalog.WALKTHROUGH_VERSION:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                f"walkthrough_version must be {build_catalog.WALKTHROUGH_VERSION}",
            )
        )
    if walkthrough_data.get("source_of_truth") != build_catalog.WALKTHROUGH_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "walkthrough source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(walkthrough_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                walkthrough_location,
                "walkthrough surface field 'skills' must be a list",
            )
        )
        return issues

    try:
        expected_walkthrough_text, expected_walkthrough_markdown_text = (
            build_catalog.build_walkthrough_texts(repo_root)
        )
        expected_walkthrough_payload = build_catalog.build_walkthrough_payload(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                walkthrough_location,
                f"walkthrough source validation failed: {exc}",
            )
        )
        return issues

    if skill_names is None:
        if walkthrough_text != expected_walkthrough_text:
            issues.append(
                ValidationIssue(
                    walkthrough_location,
                    "generated walkthrough surface is out of date; run python scripts/build_catalog.py",
                )
            )
        if walkthrough_markdown_text != expected_walkthrough_markdown_text:
            issues.append(
                ValidationIssue(
                    walkthrough_markdown_location,
                    "generated walkthrough markdown is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    actual_entries = catalog_entries_by_name(
        walkthrough_data,
        array_key="skills",
        key_name="name",
        location=walkthrough_location,
        issues=issues,
    )
    expected_entries = catalog_entries_by_name(
        expected_walkthrough_payload,
        array_key="skills",
        key_name="name",
        location=walkthrough_location,
        issues=[],
    )

    for skill_name in skill_names:
        actual_entry = actual_entries.get(skill_name)
        expected_entry = expected_entries.get(skill_name)
        if actual_entry is None:
            issues.append(
                ValidationIssue(
                    walkthrough_location,
                    f"generated walkthrough surface is missing skill '{skill_name}'",
                )
            )
            continue
        if expected_entry is None:
            continue
        if actual_entry != expected_entry:
            issues.append(
                ValidationIssue(
                    walkthrough_location,
                    f"generated walkthrough entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )

    return issues


def validate_generated_public_surface(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    public_surface_path = repo_root / build_catalog.PUBLIC_SURFACE_JSON_PATH
    public_surface_markdown_path = repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
    public_surface_location = relative_location(public_surface_path)
    public_surface_markdown_location = relative_location(public_surface_markdown_path)

    if not public_surface_path.is_file():
        issues.append(
            ValidationIssue(
                public_surface_location,
                "generated public surface is missing",
            )
        )
        if not public_surface_markdown_path.is_file():
            issues.append(
                ValidationIssue(
                    public_surface_markdown_location,
                    "generated public surface markdown is missing",
                )
            )
        return issues

    if not public_surface_markdown_path.is_file():
        issues.append(
            ValidationIssue(
                public_surface_markdown_location,
                "generated public surface markdown is missing",
            )
        )
        return issues

    public_surface_text = public_surface_path.read_text(encoding="utf-8")
    public_surface_markdown_text = public_surface_markdown_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(public_surface_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                public_surface_location,
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface must parse to an object",
            )
        )
        return issues

    public_surface_data = parsed
    validate_against_schema(
        public_surface_data,
        GENERATED_SURFACE_SCHEMA_BY_PATH[build_catalog.PUBLIC_SURFACE_JSON_PATH],
        public_surface_location,
        issues,
    )
    if public_surface_data.get("public_surface_version") != build_catalog.PUBLIC_SURFACE_VERSION:
        issues.append(
            ValidationIssue(
                public_surface_location,
                f"public_surface_version must be {build_catalog.PUBLIC_SURFACE_VERSION}",
            )
        )
    if public_surface_data.get("source_of_truth") != build_catalog.PUBLIC_SURFACE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(public_surface_data.get("cohorts"), dict):
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface field 'cohorts' must be an object",
            )
        )
    if not isinstance(public_surface_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                public_surface_location,
                "public surface field 'skills' must be a list",
            )
        )
        return issues

    try:
        expected_public_surface_text, expected_public_surface_markdown_text = (
            build_catalog.build_public_surface_texts(repo_root)
        )
        expected_public_surface_payload = build_catalog.build_public_surface_payload(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                public_surface_location,
                f"public surface source validation failed: {exc}",
            )
        )
        return issues

    if skill_names is None:
        if public_surface_text != expected_public_surface_text:
            issues.append(
                ValidationIssue(
                    public_surface_location,
                    "generated public surface is out of date; run python scripts/build_catalog.py",
                )
            )
        if public_surface_markdown_text != expected_public_surface_markdown_text:
            issues.append(
                ValidationIssue(
                    public_surface_markdown_location,
                    "generated public surface markdown is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    actual_entries = catalog_entries_by_name(
        public_surface_data,
        array_key="skills",
        key_name="name",
        location=public_surface_location,
        issues=issues,
    )
    expected_entries = catalog_entries_by_name(
        expected_public_surface_payload,
        array_key="skills",
        key_name="name",
        location=public_surface_location,
        issues=[],
    )
    actual_cohorts = public_surface_data.get("cohorts", {})
    expected_cohorts = expected_public_surface_payload.get("cohorts", {})
    cohort_names = (
        skill_governance_surface.DEFAULT_REFERENCES_COHORT,
        skill_governance_surface.CANDIDATE_READY_COHORT,
        skill_governance_surface.PENDING_LINEAGE_COHORT,
        skill_governance_surface.RISK_SURFACES_COHORT,
    )

    for skill_name in skill_names:
        actual_entry = actual_entries.get(skill_name)
        expected_entry = expected_entries.get(skill_name)
        if actual_entry is None:
            issues.append(
                ValidationIssue(
                    public_surface_location,
                    f"generated public surface is missing skill '{skill_name}'",
                )
            )
            continue
        if expected_entry is None:
            continue
        if actual_entry != expected_entry:
            issues.append(
                ValidationIssue(
                    public_surface_location,
                    f"generated public surface entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )
        for cohort_name in cohort_names:
            actual_members = actual_cohorts.get(cohort_name, [])
            expected_members = expected_cohorts.get(cohort_name, [])
            if (skill_name in actual_members) != (skill_name in expected_members):
                issues.append(
                    ValidationIssue(
                        public_surface_location,
                        f"generated public surface cohorts for '{skill_name}' are out of date; run python scripts/build_catalog.py",
                    )
                )
                break

    return issues


def validate_generated_evaluation_matrix(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    matrix_path = repo_root / build_catalog.EVALUATION_MATRIX_JSON_PATH
    matrix_markdown_path = repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH
    matrix_location = relative_location(matrix_path)
    matrix_markdown_location = relative_location(matrix_markdown_path)

    if not matrix_path.is_file():
        issues.append(
            ValidationIssue(
                matrix_location,
                "generated evaluation matrix is missing",
            )
        )
        if not matrix_markdown_path.is_file():
            issues.append(
                ValidationIssue(
                    matrix_markdown_location,
                    "generated evaluation matrix markdown is missing",
                )
            )
        return issues

    if not matrix_markdown_path.is_file():
        issues.append(
            ValidationIssue(
                matrix_markdown_location,
                "generated evaluation matrix markdown is missing",
            )
        )
        return issues

    matrix_text = matrix_path.read_text(encoding="utf-8")
    matrix_markdown_text = matrix_markdown_path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(matrix_text)
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                matrix_location,
                f"invalid JSON: {exc.msg}",
            )
        )
        return issues

    if not isinstance(parsed, dict):
        issues.append(
            ValidationIssue(
                matrix_location,
                "evaluation matrix must parse to an object",
            )
        )
        return issues

    matrix_data = parsed
    validate_against_schema(
        matrix_data,
        GENERATED_SURFACE_SCHEMA_BY_PATH[build_catalog.EVALUATION_MATRIX_JSON_PATH],
        matrix_location,
        issues,
    )
    if matrix_data.get("evaluation_matrix_version") != build_catalog.EVALUATION_MATRIX_VERSION:
        issues.append(
            ValidationIssue(
                matrix_location,
                f"evaluation_matrix_version must be {build_catalog.EVALUATION_MATRIX_VERSION}",
            )
        )
    if matrix_data.get("source_of_truth") != build_catalog.EVALUATION_MATRIX_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(
                matrix_location,
                "evaluation matrix source_of_truth does not match the expected contract",
            )
        )
    if not isinstance(matrix_data.get("skills"), list):
        issues.append(
            ValidationIssue(
                matrix_location,
                "evaluation matrix field 'skills' must be a list",
            )
        )
        return issues

    try:
        expected_matrix_text, expected_matrix_markdown_text = (
            build_catalog.build_evaluation_matrix_texts(repo_root)
        )
        expected_matrix_payload = build_catalog.build_evaluation_matrix_payload(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                matrix_location,
                f"evaluation matrix source validation failed: {exc}",
            )
        )
        return issues

    if skill_names is None:
        if matrix_text != expected_matrix_text:
            issues.append(
                ValidationIssue(
                    matrix_location,
                    "generated evaluation matrix is out of date; run python scripts/build_catalog.py",
                )
            )
        if matrix_markdown_text != expected_matrix_markdown_text:
            issues.append(
                ValidationIssue(
                    matrix_markdown_location,
                    "generated evaluation matrix markdown is out of date; run python scripts/build_catalog.py",
                )
            )
        return issues

    actual_entries = catalog_entries_by_name(
        matrix_data,
        array_key="skills",
        key_name="name",
        location=matrix_location,
        issues=issues,
    )
    expected_entries = catalog_entries_by_name(
        expected_matrix_payload,
        array_key="skills",
        key_name="name",
        location=matrix_location,
        issues=[],
    )

    for skill_name in skill_names:
        actual_entry = actual_entries.get(skill_name)
        expected_entry = expected_entries.get(skill_name)
        if actual_entry is None:
            issues.append(
                ValidationIssue(
                    matrix_location,
                    f"generated evaluation matrix is missing skill '{skill_name}'",
                )
            )
            continue
        if expected_entry is None:
            continue
        if actual_entry != expected_entry:
            issues.append(
                ValidationIssue(
                    matrix_location,
                    f"generated evaluation matrix entry for '{skill_name}' is out of date; run python scripts/build_catalog.py",
                )
            )

    return issues


def validate_generated_surface_from_spec(
    repo_root: Path,
    spec: build_catalog.GeneratedSurfaceSpec,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        expected_texts = build_catalog.build_surface_text_map(repo_root, spec)
    except (FileNotFoundError, ValueError) as exc:
        for output in spec.outputs:
            issues.append(
                ValidationIssue(
                    output.path.as_posix(),
                    f"{spec.key} source validation failed: {exc}",
                )
            )
        return issues

    for output in spec.outputs:
        path = repo_root / output.path
        location = relative_location(path)
        if not path.is_file():
            issues.append(
                ValidationIssue(
                    location,
                    f"generated {spec.key.replace('_', ' ')} artifact is missing",
                )
            )
            continue

        text = path.read_text(encoding="utf-8")
        schema_name = GENERATED_SURFACE_SCHEMA_BY_PATH.get(output.path)
        if output.is_json and schema_name is not None:
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as exc:
                issues.append(ValidationIssue(location, f"invalid JSON: {exc.msg}"))
            else:
                validate_against_schema(payload, schema_name, location, issues)

        if text != expected_texts[output.path]:
            issues.append(
                ValidationIssue(
                    location,
                    f"generated {spec.key.replace('_', ' ')} artifact is out of date; run python scripts/build_catalog.py",
                )
            )

    return issues


def validate_additional_generated_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skipped_keys = {
        "catalogs",
        "capsules",
        "sections",
        "walkthroughs",
        "public_surface",
        "evaluation_matrix",
    }
    for spec in build_catalog.generated_surface_specs(repo_root):
        if spec.key in skipped_keys:
            continue
        issues.extend(validate_generated_surface_from_spec(repo_root, spec))
    return issues
