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

from builders import build_catalog
from skill_model import skill_artifact_contract
from skill_model import skill_boundary_surface
from skill_model import skill_catalog_contract
from skill_model import skill_composition_audit
from skill_model import skill_evaluation_contract
from skill_model import skill_governance_lane_contract
from skill_model import skill_governance_surface
from skill_model import skill_layout
from skill_model import skill_overlay_contract
from skill_model import skill_review_surface
from runtime import skill_runtime_surface
from skill_model import skill_section_contract
from skill_model import skill_source_model
from validation.validators import generated_surface, questbook_surface


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR_NAME = skill_layout.SKILLS_DIR_NAME
SKILL_INDEX_NAME = "SKILL_INDEX.md"
SCHEMAS_DIR_NAME = "schemas"
SKILL_NAME_PATTERN = r"(?:aoa|atm10|abyss|titan)-[a-z0-9-]+"
LAYER_POSITION_DOC = Path("mechanics") / "boundary-bridge" / "docs" / "LAYER_POSITION.md"
README_PATH = Path("README.md")
DOCS_README_PATH = Path("docs") / "README.md"
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"
EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"
GENERATED_SURFACE_SCHEMA_BY_PATH = generated_surface.GENERATED_SURFACE_SCHEMA_BY_PATH
QUESTBOOK_PATH = questbook_surface.QUESTBOOK_PATH
QUESTBOOK_INTEGRATION_PATH = questbook_surface.QUESTBOOK_INTEGRATION_PATH
QUEST_SCHEMA_PATH = questbook_surface.QUEST_SCHEMA_PATH
QUEST_DISPATCH_SCHEMA_PATH = questbook_surface.QUEST_DISPATCH_SCHEMA_PATH
SCHEMA_PATH_OVERRIDES = {
    "quest.schema.json": QUEST_SCHEMA_PATH,
    "quest_dispatch.schema.json": QUEST_DISPATCH_SCHEMA_PATH,
}
QUEST_CATALOG_PATH = questbook_surface.QUEST_CATALOG_PATH
QUEST_DISPATCH_PATH = questbook_surface.QUEST_DISPATCH_PATH
QUEST_CATALOG_EXAMPLE_PATH = questbook_surface.QUEST_CATALOG_EXAMPLE_PATH
QUEST_DISPATCH_EXAMPLE_PATH = questbook_surface.QUEST_DISPATCH_EXAMPLE_PATH
FOUNDATION_QUEST_IDS = questbook_surface.FOUNDATION_QUEST_IDS
QUEST_IDS = FOUNDATION_QUEST_IDS
QUESTBOOK_REQUIRED_INDEX_TOKENS = questbook_surface.QUESTBOOK_REQUIRED_INDEX_TOKENS
CLOSED_QUEST_STATES = questbook_surface.CLOSED_QUEST_STATES
QUEST_LIFECYCLE_STATES = questbook_surface.QUEST_LIFECYCLE_STATES
QUESTBOOK_REQUIRED_INTEGRATION_TOKENS = questbook_surface.QUESTBOOK_REQUIRED_INTEGRATION_TOKENS
QUEST_SCHEMA_REQUIRED_FIELDS = questbook_surface.QUEST_SCHEMA_REQUIRED_FIELDS
QUEST_DISPATCH_REQUIRED_FIELDS = questbook_surface.QUEST_DISPATCH_REQUIRED_FIELDS
QUESTBOOK_FORBIDDEN_ANCHORS = questbook_surface.QUESTBOOK_FORBIDDEN_ANCHORS

REQUIRED_HEADINGS = set(skill_section_contract.CANONICAL_HEADINGS)
EXPECTED_TECHNIQUE_REPO = skill_catalog_contract.EXPECTED_TECHNIQUE_REPO
EVALUATION_MATRIX_LOCATION = build_catalog.EVALUATION_MATRIX_JSON_PATH.as_posix()
EVALUATION_MATRIX_MARKDOWN_LOCATION = (
    build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH.as_posix()
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / SCHEMA_PATH_OVERRIDES.get(
        schema_name,
        Path(SCHEMAS_DIR_NAME) / schema_name,
    )
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
    parser.add_argument(
        "--skip-generated",
        action="store_true",
        help="Skip generated-surface freshness checks for growth/source-fast validation.",
    )
    parser.add_argument(
        "--with-generated",
        action="store_true",
        help="Also validate generated surfaces when validating a single skill.",
    )
    parser.add_argument(
        "--fail-on-review-truth-sync",
        action="store_true",
        help="Fail when status-promotion review records are not in sync with the current bundle facts.",
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


def load_json_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(relative_location(path), f"invalid JSON: {exc.msg}")
        )
        return None


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


def validate_quest_schema_envelope(
    repo_root: Path,
    schema_path: Path,
    *,
    title: str,
    schema_version: str,
    required_fields: tuple[str, ...],
) -> list[ValidationIssue]:
    return questbook_surface.validate_quest_schema_envelope(
        repo_root,
        schema_path,
        title=title,
        schema_version=schema_version,
        required_fields=required_fields,
    )


def validate_questbook_surface(repo_root: Path) -> list[ValidationIssue]:
    return questbook_surface.validate_questbook_surface(repo_root)


def parse_skill_markdown(
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, list[tuple[str, str]]]:
    try:
        metadata, body = skill_source_model.parse_skill_document(skill_md_path)
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))
        return None, []
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, []
    except ValueError as exc:
        message = str(exc)
        if "missing frontmatter" in message:
            issues.append(
                ValidationIssue(
                    relative_location(skill_md_path),
                    "missing YAML frontmatter opening delimiter",
                )
            )
        elif "missing a closing frontmatter delimiter" in message:
            issues.append(
                ValidationIssue(
                    relative_location(skill_md_path),
                    "missing YAML frontmatter closing delimiter",
                )
            )
        elif "frontmatter must parse to a mapping" in message:
            issues.append(
                ValidationIssue(
                    relative_location(skill_md_path),
                    "frontmatter must parse to a mapping",
                )
            )
        else:
            issues.append(ValidationIssue(relative_location(skill_md_path), message))
        return None, []

    section_pairs = skill_section_contract.extract_top_level_sections(body)
    return metadata, section_pairs


def find_support_artifacts(
    repo_root: Path,
    skill_name: str,
) -> list[dict[str, Any]]:
    return skill_artifact_contract.collect_support_artifacts(repo_root, skill_name)


def validate_skill_bundle(repo_root: Path, skill_name: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skill_dir = skill_layout.skill_dir_path(repo_root, skill_name)
    skill_md_path = skill_layout.skill_md_path(repo_root, skill_name)
    techniques_path = skill_layout.techniques_path(repo_root, skill_name)
    policy_path = skill_layout.policy_path(repo_root, skill_name)

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

    if not find_support_artifacts(repo_root, skill_name):
        issues.append(
            ValidationIssue(
                relative_location(skill_dir),
                "missing support artifact under examples/*.md, checks/review.md, or docs/reviews/*",
            )
        )
    else:
        for artifact_issue in skill_artifact_contract.collect_skill_artifact_issues(
            repo_root,
            skill_name,
        ):
            issues.append(
                ValidationIssue(artifact_issue.location, artifact_issue.message)
            )

    metadata: dict[str, Any] | None = None
    sections: dict[str, str] = {}
    techniques_data: dict[str, Any] | None = None
    if skill_md_path.is_file():
        metadata, section_pairs = parse_skill_markdown(skill_md_path, issues)
        sections = {heading: content for heading, content in section_pairs}
        if metadata is not None:
            validate_skill_frontmatter(skill_name, metadata, skill_md_path, issues)
            validate_section_contract(section_pairs, skill_md_path, issues)
            validate_capsule_source_sections(sections, skill_md_path, issues)
            validate_runtime_surface_contract(sections, skill_md_path, issues)

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


def validate_section_contract(
    section_pairs: list[tuple[str, str]],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    for contract_issue in skill_section_contract.collect_section_contract_issues(
        section_pairs,
        location=location,
    ):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))


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


def load_policy_signal(repo_root: Path, skill_name: str) -> tuple[bool, Any]:
    return skill_source_model.load_policy_signal(repo_root, skill_name)


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


def validate_review_truth_sync(
    repo_root: Path,
    skill_name: str,
    issues: list[ValidationIssue],
) -> None:
    review_path = skill_review_surface.review_record_path(repo_root, skill_name)
    if review_path is None:
        return
    try:
        truth_sync = skill_review_surface.status_promotion_review_truth_sync(repo_root, skill_name)
    except ValueError as exc:
        issues.append(ValidationIssue(review_path, str(exc)))
        return
    if truth_sync.issues:
        location = truth_sync.review_path or review_path or relative_location(
            repo_root / STATUS_PROMOTION_REVIEWS_DIR / f"{skill_name}.md"
        )
        for issue in truth_sync.issues:
            issues.append(ValidationIssue(location, issue))


def validate_skill_composition_contract(
    repo_root: Path,
    target_skills: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    selected_skill_names = (
        list(target_skills) if target_skills is not None else discover_skill_names(repo_root)
    )
    sources: list[skill_source_model.SkillSource] = []
    source_by_name: dict[str, skill_source_model.SkillSource] = {}
    for skill_name in selected_skill_names:
        try:
            source = skill_source_model.load_skill_source(repo_root, skill_name)
        except (FileNotFoundError, ValueError):
            continue
        sources.append(source)
        source_by_name[source.name] = source

    for source in sources:
        try:
            technique_ids = skill_composition_audit.technique_ids_from_source(source)
        except ValueError as exc:
            issues.append(
                ValidationIssue(relative_location(source.techniques_path), str(exc))
            )
            continue

        review = skill_composition_audit.analyze_exception_review(repo_root, source.name)
        expected_review_location = (
            skill_composition_audit.COMPOSITION_EXCEPTION_REVIEWS_DIR
            / f"{source.name}.md"
        ).as_posix()
        if len(technique_ids) == 1:
            if review.review_path is None:
                issues.append(
                    ValidationIssue(
                        relative_location(source.skill_md_path),
                        f"single-technique skill requires a valid {expected_review_location} review record",
                    )
                )
            else:
                for issue in review.issues:
                    issues.append(ValidationIssue(review.review_path, issue))
        elif review.review_path is not None:
            issues.append(
                ValidationIssue(
                    review.review_path,
                    "skill composition exception review is only allowed for single-technique skills",
                )
            )
            for issue in review.issues:
                issues.append(ValidationIssue(review.review_path, issue))

    if target_skills is None:
        reviews_dir = repo_root / skill_composition_audit.COMPOSITION_EXCEPTION_REVIEWS_DIR
        if reviews_dir.is_dir():
            for review_path in sorted(reviews_dir.glob("*.md")):
                skill_name = review_path.stem
                if skill_name not in source_by_name:
                    issues.append(
                        ValidationIssue(
                            relative_location(review_path),
                            f"skill composition exception review references unknown skill '{skill_name}'",
                        )
                    )
    return issues


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
    if not fixtures_path.is_file():
        issues.append(ValidationIssue(relative_location(fixtures_path), "file is missing"))
        return None
    try:
        data = skill_evaluation_contract.load_evaluation_fixtures(repo_root)
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(fixtures_path),
                f"invalid YAML: {exc}",
            )
        )
        return None
    except ValueError as exc:
        issues.append(
            ValidationIssue(
                relative_location(fixtures_path),
                str(exc),
            )
        )
        return None
    if data is None:
        return None
    return data


def validate_snapshot_fixture_contract(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    fixtures_path = repo_root / EVALUATION_FIXTURES_PATH
    if not fixtures_path.is_file():
        return issues

    fixtures = load_evaluation_fixtures(repo_root, issues)
    if fixtures is None:
        return issues

    validate_against_schema(
        fixtures,
        skill_evaluation_contract.EVALUATION_FIXTURES_SCHEMA,
        relative_location(fixtures_path),
        issues,
    )
    for contract_issue in skill_evaluation_contract.validate_snapshot_case_contract(fixtures):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    for contract_issue in skill_evaluation_contract.validate_adjacency_case_contract(fixtures):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    for contract_issue in skill_evaluation_contract.validate_fixture_integrity(
        repo_root,
        fixtures,
    ):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    for contract_issue in skill_evaluation_contract.collect_snapshot_file_issues(
        repo_root,
        fixtures,
    ):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    return issues


def validate_overlay_contract(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for contract_issue in skill_overlay_contract.collect_overlay_fixture_issues(repo_root):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    for contract_issue in skill_overlay_contract.collect_live_overlay_issues(repo_root):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))
    return issues


def validate_governance_lane_contract(
    repo_root: Path,
    target_skills: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    manifest_path = repo_root / skill_governance_lane_contract.GOVERNANCE_LANES_PATH
    location = relative_location(manifest_path)
    if manifest_path.is_file():
        payload = load_yaml_file(manifest_path, issues)
        if payload is not None:
            validate_against_schema(
                payload,
                skill_governance_lane_contract.GOVERNANCE_LANES_SCHEMA,
                location,
                issues,
            )

    try:
        contract_issues = skill_governance_lane_contract.validate_governance_lanes(
            repo_root,
            skill_names=target_skills,
        )
    except (ValueError, yaml.YAMLError) as exc:
        issues.append(ValidationIssue(location, str(exc)))
        return issues

    for contract_issue in contract_issues:
        issues.append(
            ValidationIssue(contract_issue.location, contract_issue.message)
        )
    return issues


def validate_required_adjacency_coverage(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        payload = skill_boundary_surface.build_boundary_matrix_payload(repo_root, target_skills)
    except (FileNotFoundError, ValueError) as exc:
        issues.append(
            ValidationIssue(
                build_catalog.BOUNDARY_MATRIX_JSON_PATH.as_posix(),
                f"boundary matrix source validation failed: {exc}",
            )
        )
        return issues

    if not payload.get("cases"):
        return issues

    for entry in payload.get("skills", []):
        if not isinstance(entry, dict):
            continue
        if not entry.get("required_adjacency_coverage"):
            continue
        if entry.get("adjacency_ready"):
            continue
        blockers = entry.get("adjacency_blockers", [])
        blocker_suffix = f" ({', '.join(blockers)})" if blockers else ""
        issues.append(
            ValidationIssue(
                EVALUATION_FIXTURES_PATH.as_posix(),
                f"skill '{entry.get('name')}' requires adjacency coverage for canonical/candidate-ready boundary evidence{blocker_suffix}",
            )
        )
    return issues


def validate_evaluation_floors(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    skills_requiring_evaluation: dict[str, str] = {}

    for skill_name in target_skills:
        metadata, _sections = parse_skill_markdown(
            skill_layout.skill_md_path(repo_root, skill_name),
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

    coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(fixtures)
    fixtures_location = EVALUATION_FIXTURES_PATH.as_posix()
    for skill_name, status in skills_requiring_evaluation.items():
        coverage = skill_governance_surface.coverage_for_skill(
            coverage_by_skill,
            skill_name,
        )
        if not coverage.has_autonomy_check:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires an autonomy_check entry",
                )
            )
        if coverage.use_case_count < 1:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires at least one 'use' trigger case",
                )
            )
        if coverage.do_not_use_case_count < 1:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    f"skill '{skill_name}' with status '{status}' requires at least one 'do_not_use' trigger case",
                )
            )

    return issues


def validate_canonical_status_floors(
    repo_root: Path,
    target_skills: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    canonical_skills: list[
        tuple[str, dict[str, Any], set[str], dict[str, Any], Path, Path]
    ] = []

    for skill_name in target_skills:
        skill_md_path = skill_layout.skill_md_path(repo_root, skill_name)
        techniques_path = skill_layout.techniques_path(repo_root, skill_name)
        metadata, section_pairs = parse_skill_markdown(skill_md_path, [])
        if metadata is None or metadata.get("status") != "canonical":
            continue

        manifest_issues: list[ValidationIssue] = []
        techniques_data = load_yaml_file(techniques_path, manifest_issues)
        if manifest_issues or not isinstance(techniques_data, dict):
            continue

        canonical_skills.append(
            (
                skill_name,
                metadata,
                {heading for heading, _content in section_pairs},
                techniques_data,
                skill_md_path,
                techniques_path,
            )
        )

    if not canonical_skills:
        return issues

    fixtures = load_evaluation_fixtures(repo_root, [])
    coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(fixtures)
    snapshot_coverage_by_skill = skill_evaluation_contract.collect_snapshot_coverage(
        repo_root,
        fixtures,
    )
    fixtures_location = EVALUATION_FIXTURES_PATH.as_posix()
    snapshots_location = skill_evaluation_contract.EVALUATION_SNAPSHOTS_DIR.as_posix()

    for (
        skill_name,
        metadata,
        headings,
        techniques_data,
        skill_md_path,
        techniques_path,
    ) in canonical_skills:
        policy_exists, policy_allow_implicit_invocation = load_policy_signal(
            repo_root,
            skill_name,
        )
        blockers = skill_governance_surface.derive_canonical_candidate_blockers(
            status="canonical",
            headings=headings,
            technique_dependencies=list(metadata.get("technique_dependencies", [])),
            techniques=skill_catalog_contract.normalize_technique_refs(techniques_data),
            evaluation_coverage=skill_governance_surface.coverage_for_skill(
                coverage_by_skill,
                skill_name,
            ),
            invocation_mode=metadata.get("invocation_mode"),
            policy_exists=policy_exists,
            policy_allow_implicit_invocation=policy_allow_implicit_invocation,
        )
        skill_location = relative_location(skill_md_path)
        techniques_location = relative_location(techniques_path)

        if skill_governance_surface.BLOCKER_PENDING_TECHNIQUE_DEPENDENCIES in blockers:
            issues.append(
                ValidationIssue(
                    skill_location,
                    "status 'canonical' cannot use pending technique_dependencies",
                )
            )
        if skill_governance_surface.BLOCKER_MISSING_TRACEABILITY_HEADING in blockers:
            issues.append(
                ValidationIssue(
                    skill_location,
                    "status 'canonical' requires 'Technique traceability' and forbids legacy 'Future traceability'",
                )
            )
        if skill_governance_surface.BLOCKER_PENDING_TECHNIQUE_ENTRIES in blockers:
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' cannot use pending techniques in techniques.yaml",
                )
            )
        if skill_governance_surface.BLOCKER_TBD_TECHNIQUE_REFS in blockers:
            issues.append(
                ValidationIssue(
                    techniques_location,
                    "status 'canonical' requires concrete path and source_ref for every technique",
                )
            )
        eval_blockers = skill_evaluation_contract.derive_canonical_eval_blockers(
            snapshot_coverage_by_skill,
            skill_name,
        )
        if skill_evaluation_contract.BLOCKER_MISSING_USE_SNAPSHOT in eval_blockers:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    "status 'canonical' requires at least one 'use' snapshot case",
                )
            )
        if skill_evaluation_contract.BLOCKER_MISSING_DO_NOT_USE_SNAPSHOT in eval_blockers:
            issues.append(
                ValidationIssue(
                    fixtures_location,
                    "status 'canonical' requires at least one 'do_not_use' snapshot case",
                )
            )
        if skill_evaluation_contract.BLOCKER_MISSING_SNAPSHOT_FILE in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires referenced snapshot files to exist",
                )
            )
        if skill_evaluation_contract.BLOCKER_SNAPSHOT_HEADING_CONTRACT_VIOLATION in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires snapshot files to satisfy the canonical heading contract",
                )
            )
        if skill_evaluation_contract.BLOCKER_SNAPSHOT_MISSING_REQUIRED_PHRASE in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires snapshot files to contain every required output phrase",
                )
            )
        if skill_evaluation_contract.BLOCKER_SNAPSHOT_CONTAINS_FORBIDDEN_PHRASE in eval_blockers:
            issues.append(
                ValidationIssue(
                    snapshots_location,
                    "status 'canonical' requires snapshot files to avoid forbidden output phrases",
                )
            )

    return issues


def validate_runtime_surface_contract(
    sections: dict[str, str],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    trigger_boundary_text = sections.get("Trigger boundary")
    outputs_text = sections.get("Outputs")
    if trigger_boundary_text is None or outputs_text is None:
        return
    for contract_issue in skill_runtime_surface.collect_runtime_surface_issues(
        location=location,
        trigger_boundary_text=trigger_boundary_text,
        outputs_text=outputs_text,
    ):
        issues.append(ValidationIssue(contract_issue.location, contract_issue.message))


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
        skill_dirs = set(skill_layout.discover_skill_names(repo_root))
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


def validate_repo_doc_entrypoints(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    layer_position_path = repo_root / LAYER_POSITION_DOC
    readme_path = repo_root / README_PATH
    docs_readme_path = repo_root / DOCS_README_PATH

    readme_exists = readme_path.is_file()
    docs_readme_exists = docs_readme_path.is_file()
    if not readme_exists and not docs_readme_exists:
        return issues

    if not layer_position_path.is_file():
        issues.append(
            ValidationIssue(relative_location(layer_position_path), "file is missing")
        )
        return issues

    if readme_exists:
        readme_text = readme_path.read_text(encoding="utf-8")
        if "mechanics/boundary-bridge/docs/LAYER_POSITION.md" not in readme_text:
            issues.append(
                ValidationIssue(
                    relative_location(readme_path),
                    "README.md must link to mechanics/boundary-bridge/docs/LAYER_POSITION.md from the public entrypoint",
                )
            )

    if docs_readme_exists:
        docs_readme_text = docs_readme_path.read_text(encoding="utf-8")
        if "LAYER_POSITION.md" not in docs_readme_text:
            issues.append(
                ValidationIssue(
                    relative_location(docs_readme_path),
                    "docs/README.md must link to LAYER_POSITION.md from the docs map",
                )
            )

    return issues


def discover_skill_names(repo_root: Path) -> list[str]:
    return skill_source_model.discover_skill_names(repo_root)


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


def _coerce_generated_issues(
    issues: Sequence[generated_surface.ValidationIssue],
) -> list[ValidationIssue]:
    return [ValidationIssue(issue.location, issue.message) for issue in issues]


def validate_generated_catalogs(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_generated_catalogs(repo_root, skill_names=skill_names)
    )


def validate_generated_capsules(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_generated_capsules(repo_root, skill_names=skill_names)
    )


def validate_generated_sections(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_generated_sections(repo_root, skill_names=skill_names)
    )


def validate_generated_walkthroughs(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_generated_walkthroughs(repo_root, skill_names=skill_names)
    )


def validate_generated_public_surface(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_generated_public_surface(repo_root, skill_names=skill_names)
    )


def validate_generated_evaluation_matrix(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_generated_evaluation_matrix(repo_root, skill_names=skill_names)
    )


def validate_additional_generated_surfaces(repo_root: Path) -> list[ValidationIssue]:
    return _coerce_generated_issues(
        generated_surface.validate_additional_generated_surfaces(repo_root)
    )


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(
    repo_root: Path,
    skill_name: str | None = None,
    *,
    fail_on_review_truth_sync: bool = False,
    validate_generated: bool | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        all_skill_names = discover_skill_names(repo_root)
    except FileNotFoundError:
        issues.append(ValidationIssue(SKILLS_DIR_NAME, "directory is missing"))
        all_skill_names = []
    bundle_issues_by_name: dict[str, list[ValidationIssue]] = {}
    if skill_name is not None:
        if skill_name not in all_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        target_skills = [skill_name]
        selected_skills = {skill_name}
    else:
        target_skills = all_skill_names
        selected_skills = None

    if validate_generated is None:
        validate_generated = skill_name is None

    for name in target_skills:
        bundle_issues = validate_skill_bundle(repo_root, name)
        bundle_issues_by_name[name] = bundle_issues
        issues.extend(bundle_issues)

    issues.extend(validate_skill_composition_contract(repo_root, target_skills))
    issues.extend(validate_snapshot_fixture_contract(repo_root))
    issues.extend(validate_overlay_contract(repo_root))
    issues.extend(validate_governance_lane_contract(repo_root, target_skills))
    issues.extend(validate_evaluation_floors(repo_root, target_skills))
    issues.extend(validate_canonical_status_floors(repo_root, target_skills))
    issues.extend(validate_required_adjacency_coverage(repo_root, target_skills))
    issues.extend(validate_skill_index(repo_root, selected_skills=selected_skills))
    issues.extend(validate_repo_doc_entrypoints(repo_root))
    issues.extend(validate_questbook_surface(repo_root))
    if fail_on_review_truth_sync:
        for name in target_skills:
            validate_review_truth_sync(repo_root, name, issues)
    if not validate_generated:
        return issues
    if skill_name is None:
        issues.extend(validate_generated_catalogs(repo_root))
        issues.extend(validate_generated_capsules(repo_root))
        issues.extend(validate_generated_sections(repo_root))
        issues.extend(validate_generated_walkthroughs(repo_root))
        issues.extend(validate_generated_public_surface(repo_root))
        issues.extend(validate_generated_evaluation_matrix(repo_root))
        issues.extend(validate_additional_generated_surfaces(repo_root))
    elif all(not bundle_issues_by_name[name] for name in target_skills):
        issues.extend(validate_generated_catalogs(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_capsules(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_sections(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_walkthroughs(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_public_surface(repo_root, skill_names=target_skills))
        issues.extend(validate_generated_evaluation_matrix(repo_root, skill_names=target_skills))
        issues.extend(validate_additional_generated_surfaces(repo_root))
    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.skip_generated and args.with_generated:
            raise ValueError("--skip-generated and --with-generated cannot be combined")
        validate_generated = args.with_generated if args.skill else not args.skip_generated
        issues = run_validation(
            repo_root,
            skill_name=args.skill,
            fail_on_review_truth_sync=args.fail_on_review_truth_sync,
            validate_generated=validate_generated,
        )
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
