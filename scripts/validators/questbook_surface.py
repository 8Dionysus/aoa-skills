"""Questbook surface validator for aoa-skills."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

import build_catalog
from validators.questbook_contract import QuestbookContract, load_contract


CONTRACT = load_contract()
QUESTBOOK_PATH = CONTRACT.questbook_path
QUESTBOOK_INTEGRATION_PATH = CONTRACT.integration_path
QUEST_SCHEMA_PATH = CONTRACT.quest_schema_path
QUEST_DISPATCH_SCHEMA_PATH = CONTRACT.quest_dispatch_schema_path
QUEST_CATALOG_PATH = CONTRACT.quest_catalog_path
QUEST_DISPATCH_PATH = CONTRACT.quest_dispatch_path
QUEST_CATALOG_EXAMPLE_PATH = CONTRACT.quest_catalog_example_path
QUEST_DISPATCH_EXAMPLE_PATH = CONTRACT.quest_dispatch_example_path
FOUNDATION_QUEST_IDS = build_catalog.FOUNDATION_QUEST_IDS
QUEST_IDS = FOUNDATION_QUEST_IDS
QUESTBOOK_REQUIRED_INDEX_TOKENS = CONTRACT.required_index_tokens
CLOSED_QUEST_STATES = set(CONTRACT.closed_states)
QUEST_LIFECYCLE_STATES = set(CONTRACT.lifecycle_states)
QUESTBOOK_REQUIRED_INTEGRATION_TOKENS = CONTRACT.required_integration_tokens
QUEST_SCHEMA_REQUIRED_FIELDS = CONTRACT.quest_schema_required_fields
QUEST_DISPATCH_REQUIRED_FIELDS = CONTRACT.quest_dispatch_required_fields
QUESTBOOK_FORBIDDEN_ANCHORS = CONTRACT.forbidden_anchors


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class QuestPayloadState:
    quest_ids: list[str]
    quest_payloads: dict[str, dict[str, Any]]
    active_quest_ids: list[str]
    closed_quest_ids: list[str]


def relative_location(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
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


def load_yaml_file(repo_root: Path, path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(repo_root, path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(relative_location(repo_root, path), f"invalid YAML: {exc}")
        )
        return None
    return data


def load_json_file(repo_root: Path, path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(repo_root, path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(relative_location(repo_root, path), f"invalid JSON: {exc.msg}")
        )
        return None


def load_schema(repo_root: Path, schema_name: str, contract: QuestbookContract) -> dict[str, Any]:
    schema_path_by_name = {
        "quest.schema.json": contract.quest_schema_path,
        "quest_dispatch.schema.json": contract.quest_dispatch_schema_path,
    }
    schema_path = repo_root / schema_path_by_name.get(schema_name, Path("schemas") / schema_name)
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_against_schema(
    repo_root: Path,
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    contract: QuestbookContract = CONTRACT,
) -> bool:
    validator = Draft202012Validator(load_schema(repo_root, schema_name, contract))
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
    payload = load_json_file(repo_root, schema_path, issues)
    if payload is None:
        return issues
    location = relative_location(repo_root, schema_path)
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


def validate_required_surface_files(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> None:
    required_paths = (
        repo_root / QUESTBOOK_PATH,
        repo_root / QUESTBOOK_INTEGRATION_PATH,
        repo_root / QUEST_SCHEMA_PATH,
        repo_root / QUEST_DISPATCH_SCHEMA_PATH,
        repo_root / QUEST_CATALOG_PATH,
        repo_root / QUEST_DISPATCH_PATH,
        repo_root / QUEST_CATALOG_EXAMPLE_PATH,
        repo_root / QUEST_DISPATCH_EXAMPLE_PATH,
    )
    for path in required_paths:
        if not path.is_file():
            issues.append(ValidationIssue(relative_location(repo_root, path), "file is missing"))


def validate_text_tokens(
    repo_root: Path,
    path: Path,
    *,
    required_tokens: tuple[str, ...],
    issues: list[ValidationIssue],
) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    location = relative_location(repo_root, path)
    for token in required_tokens:
        if token not in text:
            issues.append(ValidationIssue(location, f"must mention '{token}' explicitly"))
    for token in QUESTBOOK_FORBIDDEN_ANCHORS:
        if token in text:
            issues.append(ValidationIssue(location, f"must not mention '{token}'"))
    return text


def validate_schema_envelopes(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
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
    return issues


def discover_quest_paths(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> tuple[list[str], dict[str, Path], list[str]]:
    quest_ids = build_catalog.discover_quest_ids(repo_root)
    duplicate_quest_paths = build_catalog.duplicate_quest_id_paths(repo_root)
    for quest_id, paths in sorted(duplicate_quest_paths.items()):
        issues.append(
            ValidationIssue(
                f"quests/**/{quest_id}.yaml",
                "duplicate quest id files are not allowed: "
                + ", ".join(relative_location(repo_root, path) for path in paths),
            )
        )
    if duplicate_quest_paths:
        quest_paths: dict[str, Path] = {}
        for quest_path in build_catalog.discover_quest_paths(repo_root):
            quest_paths.setdefault(quest_path.stem, quest_path)
    else:
        quest_paths = build_catalog.discover_quest_path_map(repo_root)
    missing_foundation_ids = build_catalog.missing_foundation_quest_ids(quest_ids)
    return quest_ids, quest_paths, missing_foundation_ids


def load_and_validate_quest_payloads(
    repo_root: Path,
    *,
    quest_ids: list[str],
    quest_paths: dict[str, Path],
    missing_foundation_ids: list[str],
    issues: list[ValidationIssue],
) -> QuestPayloadState:
    quest_payloads: dict[str, dict[str, Any]] = {}
    active_quest_ids: list[str] = []
    closed_quest_ids: list[str] = []
    for quest_id in missing_foundation_ids:
        issues.append(ValidationIssue(f"quests/**/{quest_id}.yaml", "file is missing"))
    for quest_id in quest_ids:
        quest_path = quest_paths.get(quest_id, repo_root / "quests" / f"{quest_id}.yaml")
        payload = load_yaml_file(repo_root, quest_path, issues)
        location = relative_location(repo_root, quest_path)
        if payload is None:
            continue
        if not isinstance(payload, dict):
            issues.append(ValidationIssue(location, "quest payload must parse to a mapping"))
            continue
        schema_valid = validate_against_schema(
            repo_root,
            payload,
            "quest.schema.json",
            location,
            issues,
        )
        if payload.get("id") != quest_id:
            issues.append(ValidationIssue(location, f"id must be '{quest_id}'"))
        if payload.get("repo") != "aoa-skills":
            issues.append(ValidationIssue(location, "repo must be 'aoa-skills'"))
        if payload.get("public_safe") is not True:
            issues.append(ValidationIssue(location, "public_safe must be true"))
        path_state = quest_path.parent.name
        if path_state in QUEST_LIFECYCLE_STATES and payload.get("state") != path_state:
            issues.append(
                ValidationIssue(location, f"state must match quest path state '{path_state}'")
            )
        if quest_id == "AOA-SK-Q-0004":
            activation = payload.get("activation")
            anchor_ref = payload.get("anchor_ref")
            if not isinstance(activation, dict) or activation.get("ref") != "mechanics/boundary-bridge/docs/OVERLAY_SPEC.md":
                issues.append(
                    ValidationIssue(
                        location,
                        "AOA-SK-Q-0004 must keep activation.ref 'mechanics/boundary-bridge/docs/OVERLAY_SPEC.md'",
                    )
                )
            if not isinstance(anchor_ref, dict) or anchor_ref.get("ref") != "mechanics/boundary-bridge/docs/OVERLAY_SPEC.md":
                issues.append(
                    ValidationIssue(
                        location,
                        "AOA-SK-Q-0004 must keep anchor_ref.ref 'mechanics/boundary-bridge/docs/OVERLAY_SPEC.md'",
                    )
                )
        for token in QUESTBOOK_FORBIDDEN_ANCHORS:
            if token in quest_path.read_text(encoding="utf-8"):
                issues.append(ValidationIssue(location, f"must not mention '{token}'"))
        if schema_valid:
            quest_payloads[quest_id] = payload
        if payload.get("state") in CLOSED_QUEST_STATES:
            closed_quest_ids.append(quest_id)
        else:
            active_quest_ids.append(quest_id)
    return QuestPayloadState(
        quest_ids=quest_ids,
        quest_payloads=quest_payloads,
        active_quest_ids=active_quest_ids,
        closed_quest_ids=closed_quest_ids,
    )


def validate_questbook_index_membership(
    repo_root: Path,
    *,
    questbook_text: str,
    state: QuestPayloadState,
    issues: list[ValidationIssue],
) -> None:
    if questbook_text:
        questbook_path = repo_root / QUESTBOOK_PATH
        for quest_id in state.active_quest_ids:
            if quest_id not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, questbook_path),
                        f"must reference active quest id '{quest_id}'",
                    )
                )
        for quest_id in state.closed_quest_ids:
            if quest_id in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, questbook_path),
                        f"must not list closed quest id '{quest_id}'",
                    )
                )


def validate_catalog_surfaces(
    repo_root: Path,
    *,
    state: QuestPayloadState,
    valid_quest_ids: list[str],
    issues: list[ValidationIssue],
) -> None:
    try:
        expected_catalog = build_catalog.build_quest_catalog_payload(
            repo_root,
            payloads=state.quest_payloads,
        )
    except ValueError as exc:
        issues.append(ValidationIssue("quests", str(exc)))
        expected_catalog = None
    expected_catalog_by_id = {entry["id"]: entry for entry in expected_catalog or []}
    live_catalog_payload = load_json_file(repo_root, repo_root / QUEST_CATALOG_PATH, issues)
    if isinstance(live_catalog_payload, list) and expected_catalog is not None:
        live_catalog_by_id: dict[str, dict[str, Any]] = {}
        for entry in live_catalog_payload:
            if isinstance(entry, dict):
                entry_id = entry.get("id")
                if isinstance(entry_id, str) and entry_id in expected_catalog_by_id:
                    live_catalog_by_id[entry_id] = entry
        if any(
            live_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(repo_root, repo_root / QUEST_CATALOG_PATH),
                    "live catalog must stay aligned with quests/**/AOA-SK-Q-*.yaml",
                )
            )
    elif live_catalog_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(repo_root, repo_root / QUEST_CATALOG_PATH),
                "payload must be a JSON array",
            )
        )

    catalog_payload = load_json_file(repo_root, repo_root / QUEST_CATALOG_EXAMPLE_PATH, issues)
    if isinstance(catalog_payload, list) and expected_catalog is not None:
        catalog_by_id: dict[str, dict[str, Any]] = {}
        for entry in catalog_payload:
            if isinstance(entry, dict):
                entry_id = entry.get("id")
                if isinstance(entry_id, str) and entry_id in expected_catalog_by_id:
                    catalog_by_id[entry_id] = entry
        if any(
            catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(repo_root, repo_root / QUEST_CATALOG_EXAMPLE_PATH),
                    "example catalog must stay aligned with quests/**/AOA-SK-Q-*.yaml",
                )
            )
        else:
            live_catalog_by_id: dict[str, dict[str, Any]] = {}
            if isinstance(live_catalog_payload, list):
                for entry in live_catalog_payload:
                    if isinstance(entry, dict):
                        entry_id = entry.get("id")
                        if isinstance(entry_id, str) and entry_id in expected_catalog_by_id:
                            live_catalog_by_id[entry_id] = entry
            if any(
                catalog_by_id.get(quest_id) != live_catalog_by_id.get(quest_id)
                for quest_id in valid_quest_ids
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_CATALOG_EXAMPLE_PATH),
                        "example catalog must match generated/quest_catalog.min.json",
                    )
                )
    elif catalog_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(repo_root, repo_root / QUEST_CATALOG_EXAMPLE_PATH),
                "payload must be a JSON array",
            )
        )


def validate_dispatch_surfaces(
    repo_root: Path,
    *,
    state: QuestPayloadState,
    valid_quest_ids: list[str],
    issues: list[ValidationIssue],
) -> None:
    try:
        expected_dispatch = build_catalog.build_quest_dispatch_payload(
            repo_root,
            payloads=state.quest_payloads,
        )
    except ValueError as exc:
        issues.append(ValidationIssue("quests", str(exc)))
        expected_dispatch = None
    expected_dispatch_by_id = {entry["id"]: entry for entry in expected_dispatch or []}
    live_dispatch_payload = load_json_file(repo_root, repo_root / QUEST_DISPATCH_PATH, issues)
    live_dispatch_by_id: dict[str, dict[str, Any]] = {}
    live_dispatch_invalid_ids: set[str] = set()
    if isinstance(live_dispatch_payload, list) and expected_dispatch is not None:
        for index, entry in enumerate(live_dispatch_payload):
            entry_location = f"{relative_location(repo_root, repo_root / QUEST_DISPATCH_PATH)}[{index}]"
            if not isinstance(entry, dict):
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_DISPATCH_PATH),
                        "dispatch entries must be JSON objects",
                    )
                )
                continue
            entry_valid = validate_against_schema(
                repo_root,
                entry,
                "quest_dispatch.schema.json",
                entry_location,
                issues,
            )
            quest_id = entry.get("id")
            if not entry_valid and isinstance(quest_id, str):
                live_dispatch_invalid_ids.add(quest_id)
            if entry_valid and isinstance(quest_id, str) and quest_id not in expected_dispatch_by_id:
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_DISPATCH_PATH),
                        f"dispatch entry '{quest_id}' must map to a quest declared in quests/**/AOA-SK-Q-*.yaml",
                    )
                )
            requires_artifacts = entry.get("requires_artifacts")
            if not isinstance(requires_artifacts, list) or not requires_artifacts or not all(
                isinstance(item, str) and item for item in requires_artifacts
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_DISPATCH_PATH),
                        f"dispatch entry '{quest_id}' must keep a non-empty requires_artifacts list",
                    )
                )
            if entry_valid and isinstance(quest_id, str) and quest_id in expected_dispatch_by_id:
                live_dispatch_by_id[quest_id] = entry
        comparable_live_dispatch_ids = [
            quest_id for quest_id in valid_quest_ids if quest_id not in live_dispatch_invalid_ids
        ]
        if any(
            live_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_live_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(repo_root, repo_root / QUEST_DISPATCH_PATH),
                    "dispatch entry '"
                    + next(
                        quest_id
                        for quest_id in comparable_live_dispatch_ids
                        if live_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
                    )
                    + "' must stay aligned with quests/**/AOA-SK-Q-*.yaml",
                )
            )
    elif live_dispatch_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(repo_root, repo_root / QUEST_DISPATCH_PATH),
                "payload must be a JSON array",
            )
        )

    dispatch_payload = load_json_file(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH, issues)
    if isinstance(dispatch_payload, list) and expected_dispatch is not None:
        example_dispatch_by_id: dict[str, dict[str, Any]] = {}
        example_dispatch_invalid_ids: set[str] = set()
        for index, entry in enumerate(dispatch_payload):
            entry_location = f"{relative_location(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH)}[{index}]"
            if not isinstance(entry, dict):
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                        "dispatch entries must be JSON objects",
                    )
                )
                continue
            entry_valid = validate_against_schema(
                repo_root,
                entry,
                "quest_dispatch.schema.json",
                entry_location,
                issues,
            )
            quest_id = entry.get("id")
            if not entry_valid and isinstance(quest_id, str):
                example_dispatch_invalid_ids.add(quest_id)
            if entry_valid and isinstance(quest_id, str) and quest_id not in expected_dispatch_by_id:
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                        f"example dispatch entry '{quest_id}' must map to a quest declared in quests/**/AOA-SK-Q-*.yaml",
                    )
                )
            if entry_valid and isinstance(quest_id, str) and quest_id in expected_dispatch_by_id:
                example_dispatch_by_id[quest_id] = entry
        comparable_example_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in example_dispatch_invalid_ids
        ]
        if any(
            example_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                    "example dispatch must stay aligned with quests/**/AOA-SK-Q-*.yaml",
                )
            )
        else:
            comparable_quest_ids = [
                quest_id
                for quest_id in comparable_example_dispatch_ids
                if quest_id in example_dispatch_by_id and quest_id in live_dispatch_by_id
            ]
            if any(
                example_dispatch_by_id[quest_id] != live_dispatch_by_id[quest_id]
                for quest_id in comparable_quest_ids
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                        "example dispatch must match generated/quest_dispatch.min.json",
                    )
                )
    elif dispatch_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(repo_root, repo_root / QUEST_DISPATCH_EXAMPLE_PATH),
                "payload must be a JSON array",
            )
        )


def validate_questbook_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    validate_required_surface_files(repo_root, issues)
    questbook_text = validate_text_tokens(
        repo_root,
        repo_root / QUESTBOOK_PATH,
        required_tokens=QUESTBOOK_REQUIRED_INDEX_TOKENS,
        issues=issues,
    )
    validate_text_tokens(
        repo_root,
        repo_root / QUESTBOOK_INTEGRATION_PATH,
        required_tokens=QUESTBOOK_REQUIRED_INTEGRATION_TOKENS,
        issues=issues,
    )
    issues.extend(validate_schema_envelopes(repo_root))
    quest_ids, quest_paths, missing_foundation_ids = discover_quest_paths(repo_root, issues)
    state = load_and_validate_quest_payloads(
        repo_root,
        quest_ids=quest_ids,
        quest_paths=quest_paths,
        missing_foundation_ids=missing_foundation_ids,
        issues=issues,
    )
    validate_questbook_index_membership(
        repo_root,
        questbook_text=questbook_text,
        state=state,
        issues=issues,
    )
    valid_quest_ids = [
        quest_id for quest_id in state.quest_ids if quest_id in state.quest_payloads
    ]
    validate_catalog_surfaces(
        repo_root,
        state=state,
        valid_quest_ids=valid_quest_ids,
        issues=issues,
    )
    validate_dispatch_surfaces(
        repo_root,
        state=state,
        valid_quest_ids=valid_quest_ids,
        issues=issues,
    )
    return issues
