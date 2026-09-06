"""Small owner-local model for quest source and deterministic read models."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

from skill_model import yaml_loader


FOUNDATION_QUEST_IDS: tuple[str, ...] = ()
OUTPUT_PATHS = {
    Path("generated/quest_catalog.min.json"): False,
    Path("generated/quest_dispatch.min.json"): False,
    Path("generated/quest_catalog.min.example.json"): True,
    Path("generated/quest_dispatch.min.example.json"): True,
}


def relative_path(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def quest_id_sort_key(quest_id: str) -> tuple[int, str]:
    suffix = quest_id.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_id)
    except ValueError:
        return (sys.maxsize, quest_id)


def discover_quest_paths(repo_root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            (
                path
                for path in (repo_root / "quests").glob("**/AOA-SK-Q-*.yaml")
                if path.is_file()
            ),
            key=lambda path: quest_id_sort_key(path.stem),
        )
    )


def duplicate_quest_id_paths(repo_root: Path) -> dict[str, tuple[Path, ...]]:
    paths_by_id: dict[str, list[Path]] = {}
    for path in discover_quest_paths(repo_root):
        paths_by_id.setdefault(path.stem, []).append(path)
    return {
        quest_id: tuple(paths)
        for quest_id, paths in paths_by_id.items()
        if len(paths) > 1
    }


def ensure_unique_quest_ids(repo_root: Path) -> None:
    duplicates = duplicate_quest_id_paths(repo_root)
    if not duplicates:
        return
    details = [
        f"{quest_id}: {', '.join(relative_path(path, repo_root) for path in paths)}"
        for quest_id, paths in sorted(duplicates.items())
    ]
    raise ValueError("duplicate quest ids are not allowed: " + "; ".join(details))


def discover_quest_source_paths(repo_root: Path) -> dict[str, str]:
    ensure_unique_quest_ids(repo_root)
    return {
        path.stem: relative_path(path, repo_root)
        for path in discover_quest_paths(repo_root)
    }


def discover_quest_path_map(repo_root: Path) -> dict[str, Path]:
    ensure_unique_quest_ids(repo_root)
    return {path.stem: path for path in discover_quest_paths(repo_root)}


def discover_quest_ids(repo_root: Path) -> tuple[str, ...]:
    return tuple(path.stem for path in discover_quest_paths(repo_root))


def missing_foundation_quest_ids(quest_ids: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    quest_id_set = set(quest_ids)
    return tuple(
        quest_id for quest_id in FOUNDATION_QUEST_IDS if quest_id not in quest_id_set
    )


def load_quest_payloads(repo_root: Path) -> dict[str, dict[str, Any]]:
    quest_ids = discover_quest_ids(repo_root)
    missing = missing_foundation_quest_ids(quest_ids)
    if missing:
        raise ValueError("missing required foundation quest files: " + ", ".join(missing))
    paths = discover_quest_path_map(repo_root)
    payloads: dict[str, dict[str, Any]] = {}
    for quest_id in quest_ids:
        path = paths[quest_id]
        payload = yaml_loader.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"{relative_path(path, repo_root)} must be a YAML mapping")
        payloads[quest_id] = payload
    return payloads


def build_quest_catalog_payload(
    repo_root: Path,
    *,
    payloads: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    quest_payloads = payloads if payloads is not None else load_quest_payloads(repo_root)
    source_paths = discover_quest_source_paths(repo_root)
    return [
        {
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
            "source_path": source_paths[quest_id],
            "public_safe": payload["public_safe"],
        }
        for quest_id in discover_quest_ids(repo_root)
        if (payload := quest_payloads.get(quest_id)) is not None
    ]


def build_quest_dispatch_payload(
    repo_root: Path,
    *,
    payloads: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    quest_payloads = payloads if payloads is not None else load_quest_payloads(repo_root)
    source_paths = discover_quest_source_paths(repo_root)
    entries: list[dict[str, Any]] = []
    for quest_id in discover_quest_ids(repo_root):
        payload = quest_payloads.get(quest_id)
        if payload is None:
            continue
        source_path = source_paths[quest_id]
        activation = payload.get("activation")
        if not isinstance(activation, Mapping) or not isinstance(activation.get("mode"), str):
            raise ValueError(f"{source_path} must keep activation.mode as a string")
        requires_artifacts = (
            ["recurrence_evidence", "lifecycle_decision"]
            if payload.get("kind") == "harvest"
            else ["bounded_plan", "owner_result", "verification_result"]
        )
        entry = {
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
            "requires_artifacts": requires_artifacts,
            "activation_mode": activation["mode"],
            "source_path": source_path,
            "public_safe": payload["public_safe"],
        }
        for optional in ("fallback_tier", "wrapper_class"):
            if optional in payload:
                entry[optional] = payload[optional]
        entries.append(entry)
    return entries


def build_outputs(repo_root: Path) -> dict[Path, str]:
    catalog = build_quest_catalog_payload(repo_root)
    dispatch = build_quest_dispatch_payload(repo_root)
    payload_by_path = {
        Path("generated/quest_catalog.min.json"): catalog,
        Path("generated/quest_dispatch.min.json"): dispatch,
        Path("generated/quest_catalog.min.example.json"): catalog,
        Path("generated/quest_dispatch.min.example.json"): dispatch,
    }
    return {
        path: json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            indent=2 if OUTPUT_PATHS[path] else None,
            separators=None if OUTPUT_PATHS[path] else (",", ":"),
        )
        + "\n"
        for path, payload in payload_by_path.items()
    }
