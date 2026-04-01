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
import skill_artifact_contract
import skill_boundary_surface
import skill_catalog_contract
import skill_composition_audit
import skill_evaluation_contract
import skill_governance_backlog_surface
import skill_governance_lane_contract
import skill_governance_surface
import skill_lineage_surface
import skill_overlay_contract
import skill_review_surface
import skill_runtime_surface
import skill_section_contract
import skill_source_model
import skill_bundle_surface


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
SKILL_INDEX_NAME = "SKILL_INDEX.md"
SCHEMAS_DIR_NAME = "schemas"
SKILL_NAME_PATTERN = r"(?:aoa|atm10|abyss)-[a-z0-9-]+"
LAYER_POSITION_DOC = Path("docs") / "LAYER_POSITION.md"
README_PATH = Path("README.md")
DOCS_README_PATH = Path("docs") / "README.md"
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"
EVALUATION_FIXTURES_PATH = Path("tests") / "fixtures" / "skill_evaluation_cases.yaml"
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
QUESTBOOK_PATH = Path("QUESTBOOK.md")
QUESTBOOK_INTEGRATION_PATH = Path("docs") / "QUESTBOOK_SKILL_INTEGRATION.md"
QUEST_SCHEMA_PATH = Path("schemas") / "quest.schema.json"
QUEST_DISPATCH_SCHEMA_PATH = Path("schemas") / "quest_dispatch.schema.json"
QUEST_CATALOG_EXAMPLE_PATH = Path("generated") / "quest_catalog.min.example.json"
QUEST_DISPATCH_EXAMPLE_PATH = Path("generated") / "quest_dispatch.min.example.json"
QUEST_IDS = (
    "AOA-SK-Q-0001",
    "AOA-SK-Q-0002",
    "AOA-SK-Q-0003",
    "AOA-SK-Q-0004",
)
QUESTBOOK_REQUIRED_INDEX_TOKENS = (
    "skill/eval alignment debts",
    ".agents/skills/",
    "Frontier",
    "Near",
    "Harvest candidates",
)
CLOSED_QUEST_STATES = {"done", "dropped"}
QUESTBOOK_REQUIRED_INTEGRATION_TOKENS = (
    "generated/public_surface.md",
    "generated/governance_backlog.md",
    "generated/skill_evaluation_matrix.md",
    "docs/RUNTIME_PATH.md",
    "docs/EVALUATION_PATH.md",
    "docs/CODEX_PORTABLE_LAYER.md",
    "docs/LOCAL_ADAPTER_CONTRACT.md",
    "docs/OVERLAY_SPEC.md",
    "docs/TWO_STAGE_SKILL_SELECTION.md",
    "hidden second source of truth",
)
QUEST_SCHEMA_REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "title",
    "repo",
    "owner_surface",
    "kind",
    "state",
    "band",
    "difficulty",
    "risk",
    "control_mode",
    "delegate_tier",
    "write_scope",
    "activation",
    "anchor_ref",
    "evidence",
    "opened_at",
    "touched_at",
    "public_safe",
)
QUEST_DISPATCH_REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "repo",
    "state",
    "band",
    "difficulty",
    "risk",
    "control_mode",
    "delegate_tier",
    "split_required",
    "write_scope",
    "activation_mode",
    "public_safe",
)
QUESTBOOK_FORBIDDEN_ANCHORS = (
    "docs/overlays/atm10/PROJECT_OVERLAY.md",
    "ATM10-Agent",
)

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
    issues: list[ValidationIssue] = []
    payload = load_json_file(schema_path, issues)
    if payload is None:
        return issues
    location = relative_location(schema_path)
    if not isinstance(payload, dict):
        return [ValidationIssue(location, "schema payload must be a JSON object")]
    if payload.get("title") != title:
        issues.append(ValidationIssue(location, f"schema title must be '{title}'"))
    if payload.get("type") != "object":
        issues.append(ValidationIssue(location, "schema type must be 'object'"))
    if payload.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(location, "schema must set additionalProperties to false")
        )
    if payload.get("required") != list(required_fields):
        issues.append(
            ValidationIssue(
                location,
                "schema required fields must stay aligned with the questbook contract",
            )
        )
    properties = payload.get("properties")
    if not isinstance(properties, dict):
        issues.append(ValidationIssue(location, "schema properties must be an object"))
        return issues
    schema_version_entry = properties.get("schema_version")
    if not isinstance(schema_version_entry, dict) or schema_version_entry.get("const") != schema_version:
        issues.append(
            ValidationIssue(
                location,
                f"schema_version must stay pinned to '{schema_version}'",
            )
        )
    return issues


def build_expected_quest_catalog_entry(quest_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": quest_id,
        "title": payload["title"],
        "repo": payload["repo"],
        "theme_ref": payload.get("theme_ref", ""),
        "milestone_ref": payload.get("milestone_ref", ""),
        "state": payload["state"],
        "band": payload["band"],
        "kind": payload["kind"],
        "difficulty": payload["difficulty"],
        "risk": payload["risk"],
        "owner_surface": payload["owner_surface"],
        "source_path": f"quests/{quest_id}.yaml",
        "public_safe": payload["public_safe"],
    }


def build_expected_quest_dispatch_entry(
    quest_id: str,
    payload: dict[str, Any],
    actual: dict[str, Any],
) -> dict[str, Any]:
    expected = {
        "schema_version": "quest_dispatch_v1",
        "id": quest_id,
        "repo": payload["repo"],
        "state": payload["state"],
        "band": payload["band"],
        "difficulty": payload["difficulty"],
        "risk": payload["risk"],
        "control_mode": payload["control_mode"],
        "delegate_tier": payload["delegate_tier"],
        "split_required": payload.get("split_required", False),
        "write_scope": payload["write_scope"],
        "activation_mode": payload["activation"]["mode"],
        "source_path": f"quests/{quest_id}.yaml",
        "public_safe": payload["public_safe"],
    }
    if "fallback_tier" in actual:
        expected["fallback_tier"] = payload.get("fallback_tier")
    if "wrapper_class" in actual:
        expected["wrapper_class"] = payload.get("wrapper_class")
    return expected


def validate_questbook_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required_paths = (
        repo_root / QUESTBOOK_PATH,
        repo_root / QUESTBOOK_INTEGRATION_PATH,
        repo_root / QUEST_SCHEMA_PATH,
        repo_root / QUEST_DISPATCH_SCHEMA_PATH,
        repo_root / QUEST_CATALOG_EXAMPLE_PATH,
        repo_root / QUEST_DISPATCH_EXAMPLE_PATH,
    )
    for path in required_paths:
        if not path.is_file():
            issues.append(ValidationIssue(relative_location(path), "file is missing"))

    questbook_path = repo_root / QUESTBOOK_PATH
    questbook_text = ""
    if questbook_path.is_file():
        questbook_text = questbook_path.read_text(encoding="utf-8")
        for token in QUESTBOOK_REQUIRED_INDEX_TOKENS:
            if token not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path),
                        f"must mention '{token}' explicitly",
                    )
                )
        for token in QUESTBOOK_FORBIDDEN_ANCHORS:
            if token in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path),
                        f"must not mention '{token}'",
                    )
                )

    integration_path = repo_root / QUESTBOOK_INTEGRATION_PATH
    if integration_path.is_file():
        integration_text = integration_path.read_text(encoding="utf-8")
        for token in QUESTBOOK_REQUIRED_INTEGRATION_TOKENS:
            if token not in integration_text:
                issues.append(
                    ValidationIssue(
                        relative_location(integration_path),
                        f"must mention '{token}' explicitly",
                    )
                )
        for token in QUESTBOOK_FORBIDDEN_ANCHORS:
            if token in integration_text:
                issues.append(
                    ValidationIssue(
                        relative_location(integration_path),
                        f"must not mention '{token}'",
                    )
                )

    issues.extend(
        validate_quest_schema_envelope(
            repo_root,
            repo_root / QUEST_SCHEMA_PATH,
            title="aoa-skills work_quest_v1",
            schema_version="work_quest_v1",
            required_fields=QUEST_SCHEMA_REQUIRED_FIELDS,
        )
    )
    issues.extend(
        validate_quest_schema_envelope(
            repo_root,
            repo_root / QUEST_DISPATCH_SCHEMA_PATH,
            title="aoa-skills quest_dispatch_v1",
            schema_version="quest_dispatch_v1",
            required_fields=QUEST_DISPATCH_REQUIRED_FIELDS,
        )
    )

    quest_payloads: dict[str, dict[str, Any]] = {}
    active_quest_ids: list[str] = []
    closed_quest_ids: list[str] = []
    for quest_id in QUEST_IDS:
        quest_path = repo_root / "quests" / f"{quest_id}.yaml"
        payload = load_yaml_file(quest_path, issues)
        location = relative_location(quest_path)
        if payload is None:
            continue
        if not isinstance(payload, dict):
            issues.append(ValidationIssue(location, "quest payload must parse to a mapping"))
            continue
        validate_against_schema(payload, "quest.schema.json", location, issues)
        if payload.get("id") != quest_id:
            issues.append(ValidationIssue(location, f"id must be '{quest_id}'"))
        if payload.get("repo") != "aoa-skills":
            issues.append(ValidationIssue(location, "repo must be 'aoa-skills'"))
        if payload.get("public_safe") is not True:
            issues.append(ValidationIssue(location, "public_safe must be true"))
        if quest_id == "AOA-SK-Q-0004":
            activation = payload.get("activation")
            anchor_ref = payload.get("anchor_ref")
            if not isinstance(activation, dict) or activation.get("ref") != "docs/OVERLAY_SPEC.md":
                issues.append(
                    ValidationIssue(
                        location,
                        "AOA-SK-Q-0004 must keep activation.ref 'docs/OVERLAY_SPEC.md'",
                    )
                )
            if not isinstance(anchor_ref, dict) or anchor_ref.get("ref") != "docs/OVERLAY_SPEC.md":
                issues.append(
                    ValidationIssue(
                        location,
                        "AOA-SK-Q-0004 must keep anchor_ref.ref 'docs/OVERLAY_SPEC.md'",
                    )
                )
        for token in QUESTBOOK_FORBIDDEN_ANCHORS:
            if token in quest_path.read_text(encoding="utf-8"):
                issues.append(ValidationIssue(location, f"must not mention '{token}'"))
        quest_payloads[quest_id] = payload
        if payload.get("state") in CLOSED_QUEST_STATES:
            closed_quest_ids.append(quest_id)
        else:
            active_quest_ids.append(quest_id)

    if questbook_text:
        for quest_id in active_quest_ids:
            if quest_id not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path),
                        f"must reference active quest id '{quest_id}'",
                    )
                )
        for quest_id in closed_quest_ids:
            if quest_id in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path),
                        f"must not list closed quest id '{quest_id}'",
                    )
                )

    catalog_payload = load_json_file(repo_root / QUEST_CATALOG_EXAMPLE_PATH, issues)
    if isinstance(catalog_payload, list) and len(quest_payloads) == len(QUEST_IDS):
        expected_catalog = [
            build_expected_quest_catalog_entry(quest_id, quest_payloads[quest_id])
            for quest_id in QUEST_IDS
        ]
        if catalog_payload != expected_catalog:
            issues.append(
                ValidationIssue(
                    relative_location(repo_root / QUEST_CATALOG_EXAMPLE_PATH),
                    "example catalog must stay aligned with quests/*.yaml",
                )
            )
    elif catalog_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(repo_root / QUEST_CATALOG_EXAMPLE_PATH),
                "payload must be a JSON array",
            )
        )

    dispatch_payload = load_json_file(repo_root / QUEST_DISPATCH_EXAMPLE_PATH, issues)
    if isinstance(dispatch_payload, list) and len(quest_payloads) == len(QUEST_IDS):
        if len(dispatch_payload) != len(QUEST_IDS):
            issues.append(
                ValidationIssue(
                    relative_location(repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                    f"expected {len(QUEST_IDS)} dispatch examples",
                )
            )
        for entry, quest_id in zip(dispatch_payload, QUEST_IDS):
            location = relative_location(repo_root / QUEST_DISPATCH_EXAMPLE_PATH)
            if not isinstance(entry, dict):
                issues.append(
                    ValidationIssue(location, "dispatch entries must be JSON objects")
                )
                continue
            validate_against_schema(entry, "quest_dispatch.schema.json", location, issues)
            requires_artifacts = entry.get("requires_artifacts")
            if not isinstance(requires_artifacts, list) or not requires_artifacts or not all(
                isinstance(item, str) and item for item in requires_artifacts
            ):
                issues.append(
                    ValidationIssue(
                        location,
                        f"dispatch entry '{quest_id}' must keep a non-empty requires_artifacts list",
                    )
                )
            expected_entry = build_expected_quest_dispatch_entry(
                quest_id, quest_payloads[quest_id], entry
            )
            comparable_entry = {key: entry.get(key) for key in expected_entry}
            if comparable_entry != expected_entry:
                issues.append(
                    ValidationIssue(
                        location,
                        f"dispatch entry '{quest_id}' must stay aligned with quests/*.yaml",
                    )
                )
    elif dispatch_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                "payload must be a JSON array",
            )
        )

    return issues


def should_validate_questbook_surface(repo_root: Path) -> bool:
    questbook_markers = (
        repo_root / QUESTBOOK_PATH,
        repo_root / QUESTBOOK_INTEGRATION_PATH,
        repo_root / "quests",
        repo_root / QUEST_SCHEMA_PATH,
        repo_root / QUEST_DISPATCH_SCHEMA_PATH,
    )
    return repo_root == REPO_ROOT or any(path.exists() for path in questbook_markers)


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
    for contract_issue in skill_overlay_contract.collect_overlay_stub_issues(repo_root):
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
        skill_md_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
        techniques_path = repo_root / SKILLS_DIR_NAME / skill_name / "techniques.yaml"
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
        if "docs/LAYER_POSITION.md" not in readme_text:
            issues.append(
                ValidationIssue(
                    relative_location(readme_path),
                    "README.md must link to docs/LAYER_POSITION.md from the public entrypoint",
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
            skill_md_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
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
    for spec in build_catalog.generated_surface_specs():
        if spec.key in skipped_keys:
            continue
        issues.extend(validate_generated_surface_from_spec(repo_root, spec))
    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(
    repo_root: Path,
    skill_name: str | None = None,
    *,
    fail_on_review_truth_sync: bool = False,
) -> list[ValidationIssue]:
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

    issues.extend(validate_skill_composition_contract(repo_root, target_skills))
    issues.extend(validate_snapshot_fixture_contract(repo_root))
    issues.extend(validate_overlay_contract(repo_root))
    issues.extend(validate_governance_lane_contract(repo_root, target_skills))
    issues.extend(validate_evaluation_floors(repo_root, target_skills))
    issues.extend(validate_canonical_status_floors(repo_root, target_skills))
    issues.extend(validate_required_adjacency_coverage(repo_root, target_skills))
    issues.extend(validate_skill_index(repo_root, selected_skills=selected_skills))
    issues.extend(validate_repo_doc_entrypoints(repo_root))
    if should_validate_questbook_surface(repo_root):
        issues.extend(validate_questbook_surface(repo_root))
    if fail_on_review_truth_sync:
        for name in target_skills:
            validate_review_truth_sync(repo_root, name, issues)
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
        issues = run_validation(
            repo_root,
            skill_name=args.skill,
            fail_on_review_truth_sync=args.fail_on_review_truth_sync,
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
