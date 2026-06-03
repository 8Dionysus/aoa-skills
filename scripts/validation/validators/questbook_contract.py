"""Load questbook surface validation contract data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_PATH = Path(__file__).with_name("questbook_contract.json")


@dataclass(frozen=True)
class QuestbookContract:
    questbook_path: Path
    integration_path: Path
    quest_schema_path: Path
    quest_dispatch_schema_path: Path
    quest_catalog_path: Path
    quest_dispatch_path: Path
    quest_catalog_example_path: Path
    quest_dispatch_example_path: Path
    required_index_tokens: tuple[str, ...]
    closed_states: tuple[str, ...]
    lifecycle_states: tuple[str, ...]
    required_integration_tokens: tuple[str, ...]
    quest_schema_required_fields: tuple[str, ...]
    quest_dispatch_required_fields: tuple[str, ...]
    forbidden_anchors: tuple[str, ...]


def _require_mapping(payload: dict[str, Any], key: str, path: Path) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: {key} must be an object")
    return value


def _require_path(payload: dict[str, Any], key: str, path: Path) -> Path:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{path}: {key} must be a non-empty string")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"{path}: {key} must be repo-relative")
    return candidate


def _require_string_list(
    payload: dict[str, Any],
    key: str,
    path: Path,
    *,
    allow_empty: bool = False,
    require_unique: bool = False,
) -> tuple[str, ...]:
    value = payload.get(key)
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError(f"{path}: {key} must be a list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{path}: {key} must contain non-empty strings")
    if require_unique and len(value) != len(set(value)):
        raise ValueError(f"{path}: {key} must not contain duplicates")
    return tuple(value)


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> QuestbookContract:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: contract must be a JSON object")
    if payload.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")

    surface_paths = _require_mapping(payload, "surface_paths", path)
    tokens = _require_mapping(payload, "required_tokens", path)
    states = _require_mapping(payload, "states", path)
    required_fields = _require_mapping(payload, "required_fields", path)

    return QuestbookContract(
        questbook_path=_require_path(surface_paths, "questbook", path),
        integration_path=_require_path(surface_paths, "integration", path),
        quest_schema_path=_require_path(surface_paths, "quest_schema", path),
        quest_dispatch_schema_path=_require_path(surface_paths, "quest_dispatch_schema", path),
        quest_catalog_path=_require_path(surface_paths, "quest_catalog", path),
        quest_dispatch_path=_require_path(surface_paths, "quest_dispatch", path),
        quest_catalog_example_path=_require_path(surface_paths, "quest_catalog_example", path),
        quest_dispatch_example_path=_require_path(surface_paths, "quest_dispatch_example", path),
        required_index_tokens=_require_string_list(tokens, "questbook_index", path),
        closed_states=_require_string_list(states, "closed", path, require_unique=True),
        lifecycle_states=_require_string_list(states, "lifecycle", path, require_unique=True),
        required_integration_tokens=_require_string_list(tokens, "integration", path),
        quest_schema_required_fields=_require_string_list(required_fields, "quest", path),
        quest_dispatch_required_fields=_require_string_list(required_fields, "quest_dispatch", path),
        forbidden_anchors=_require_string_list(payload, "forbidden_anchors", path),
    )
