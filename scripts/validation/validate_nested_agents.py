#!/usr/bin/env python3
"""Validate required nested AGENTS.md documents for aoa-skills."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT_PATH = Path("scripts") / "validation" / "validators" / "nested_agents_contract.json"


@dataclass(frozen=True)
class AgentsDocSpec:
    path: Path
    required_snippets: tuple[str, ...]


def _load_contract_payload(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: contract must be a JSON object")
    if payload.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    docs = payload.get("docs")
    if not isinstance(docs, list) or not docs:
        raise ValueError(f"{path}: docs must be a non-empty list")
    return payload


def load_contract(contract_path: Path) -> tuple[AgentsDocSpec, ...]:
    payload = _load_contract_payload(contract_path)
    specs: list[AgentsDocSpec] = []
    seen_paths: set[str] = set()
    for index, raw_spec in enumerate(payload["docs"]):
        if not isinstance(raw_spec, dict):
            raise ValueError(f"{contract_path}: docs[{index}] must be an object")
        raw_path = raw_spec.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError(f"{contract_path}: docs[{index}].path must be a non-empty string")
        if raw_path.startswith("/") or ".." in Path(raw_path).parts:
            raise ValueError(f"{contract_path}: docs[{index}].path must be repo-relative")
        if raw_path in seen_paths:
            raise ValueError(f"{contract_path}: duplicate doc path {raw_path!r}")
        seen_paths.add(raw_path)

        snippets = raw_spec.get("required_snippets")
        if not isinstance(snippets, list) or not snippets:
            raise ValueError(
                f"{contract_path}: docs[{index}].required_snippets must be a non-empty list"
            )
        if any(not isinstance(snippet, str) or not snippet for snippet in snippets):
            raise ValueError(
                f"{contract_path}: docs[{index}].required_snippets must contain non-empty strings"
            )
        specs.append(AgentsDocSpec(Path(raw_path), tuple(snippets)))
    return tuple(specs)


def default_contract(repo_root: Path = REPO_ROOT) -> tuple[AgentsDocSpec, ...]:
    return load_contract(repo_root / DEFAULT_CONTRACT_PATH)


REQUIRED_DOCS = default_contract()


def validate(
    repo_root: Path,
    specs: Sequence[AgentsDocSpec] | None = None,
) -> list[str]:
    issues: list[str] = []
    for spec in specs or REQUIRED_DOCS:
        path = repo_root / spec.path
        if not path.is_file():
            issues.append(f"{spec.path.as_posix()}: file is missing")
            continue

        text = path.read_text(encoding="utf-8")
        for snippet in spec.required_snippets:
            if snippet not in text:
                issues.append(
                    f"{spec.path.as_posix()}: missing required snippet {snippet!r}"
                )
    return issues


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Repository root.")
    parser.add_argument(
        "--contract",
        default=DEFAULT_CONTRACT_PATH.as_posix(),
        help="Repo-relative or absolute nested AGENTS contract JSON path.",
    )
    return parser.parse_args(argv)


def resolve_contract_path(repo_root: Path, raw_contract_path: str) -> Path:
    contract_path = Path(raw_contract_path)
    if not contract_path.is_absolute():
        contract_path = repo_root / contract_path
    return contract_path


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
        specs = load_contract(resolve_contract_path(repo_root, args.contract))
    except (FileNotFoundError, ValueError) as exc:
        print(f"Nested AGENTS contract error: {exc}")
        return 2

    issues = validate(repo_root, specs)
    if issues:
        print("Nested AGENTS validation failed.")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"Nested AGENTS validation passed for {len(specs)} documents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
