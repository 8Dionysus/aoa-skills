#!/usr/bin/env python3
"""Build deterministic derived skill catalogs for routing and reader surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
GENERATED_DIR_NAME = "generated"
FULL_CATALOG_PATH = Path(GENERATED_DIR_NAME) / "skill_catalog.json"
MIN_CATALOG_PATH = Path(GENERATED_DIR_NAME) / "skill_catalog.min.json"
CATALOG_VERSION = 1
SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
}
SHORT_REPO_NAMES = {
    "aoa-techniques": "aoa-techniques",
    "aoa-skills": "aoa-skills",
    "aoa-evals": "aoa-evals",
    "aoa-memo": "aoa-memo",
}


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
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def is_repo_relative_path(path_value: Any) -> bool:
    if not isinstance(path_value, str):
        return False
    if not path_value or path_value == "TBD":
        return False
    if "\\" in path_value:
        return False
    if path_value.startswith("/") or path_value.startswith("./"):
        return False
    parts = path_value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    if ":" in parts[0]:
        return False
    return True


def normalize_repo_name(raw_repo: Any) -> str:
    if not isinstance(raw_repo, str) or not raw_repo.strip():
        raise ValueError("repo must be a non-empty string")

    candidate = raw_repo.strip().replace("\\", "/")
    if candidate.endswith(".git"):
        candidate = candidate[:-4]
    candidate = candidate.rstrip("/")

    lowered = candidate.lower()
    for short_name in SHORT_REPO_NAMES.values():
        if lowered == short_name:
            return short_name
        if lowered.endswith(f"/{short_name}"):
            return short_name
        if lowered.endswith(f":{short_name}"):
            return short_name
        if lowered.endswith(f"github.com/{short_name}"):
            return short_name
    raise ValueError(f"unsupported repo value '{raw_repo}'")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_skill_document(path: Path) -> dict[str, Any]:
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
    return metadata


def technique_ids_from_manifest(manifest: dict[str, Any]) -> list[str]:
    techniques = manifest.get("techniques", [])
    if not isinstance(techniques, list):
        raise ValueError("techniques.yaml must contain a techniques list")

    technique_ids: list[str] = []
    for technique in techniques:
        if not isinstance(technique, dict):
            raise ValueError("each techniques.yaml technique entry must be an object")
        technique_id = technique.get("id")
        if not isinstance(technique_id, str):
            raise ValueError("each techniques.yaml technique entry must define string id")
        technique_ids.append(technique_id)
    return technique_ids


def normalize_technique_refs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    techniques = manifest.get("techniques", [])
    if not isinstance(techniques, list):
        raise ValueError("techniques.yaml must contain a techniques list")

    normalized_refs: list[dict[str, Any]] = []
    for technique in techniques:
        if not isinstance(technique, dict):
            raise ValueError("each techniques.yaml technique entry must be an object")

        technique_id = technique.get("id")
        path_value = technique.get("path")
        source_ref = technique.get("source_ref")
        if not isinstance(technique_id, str):
            raise ValueError("each techniques.yaml technique entry must define string id")
        if not isinstance(path_value, str):
            raise ValueError(f"technique '{technique_id}' must define string path")
        if not isinstance(source_ref, str):
            raise ValueError(f"technique '{technique_id}' must define string source_ref")

        normalized_ref: dict[str, Any] = {
            "id": technique_id,
            "repo": normalize_repo_name(technique.get("repo")),
            "path": path_value,
            "source_ref": source_ref,
        }
        use_sections = technique.get("use_sections")
        if use_sections is not None:
            if not isinstance(use_sections, list):
                raise ValueError(
                    f"technique '{technique_id}' use_sections must be a list when present"
                )
            normalized_ref["use_sections"] = list(use_sections)
        normalized_refs.append(normalized_ref)

    return normalized_refs


def build_skill_entry(repo_root: Path, skill_name: str) -> dict[str, Any]:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    techniques_path = skill_dir / "techniques.yaml"
    metadata = parse_skill_document(skill_md_path)
    manifest = load_yaml(techniques_path)

    if not isinstance(manifest, dict):
        raise ValueError(f"{techniques_path} must parse to a mapping")

    entry = {
        "name": metadata.get("name"),
        "scope": metadata.get("scope"),
        "status": metadata.get("status"),
        "summary": metadata.get("summary"),
        "invocation_mode": metadata.get("invocation_mode"),
        "technique_dependencies": list(metadata.get("technique_dependencies", [])),
        "skill_path": relative_path(skill_md_path, repo_root),
        "composition_mode": manifest.get("composition_mode"),
        "technique_refs": normalize_technique_refs(manifest),
    }

    manifest_ids = technique_ids_from_manifest(manifest)
    if entry["technique_dependencies"] != manifest_ids:
        raise ValueError(
            f"{techniques_path} technique order does not match SKILL.md frontmatter"
        )

    return entry


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


def write_catalogs(repo_root: Path) -> tuple[Path, Path]:
    generated_dir = repo_root / GENERATED_DIR_NAME
    generated_dir.mkdir(exist_ok=True)
    full_text, min_text = build_catalog_texts(repo_root)
    full_path = repo_root / FULL_CATALOG_PATH
    min_path = repo_root / MIN_CATALOG_PATH
    full_path.write_text(full_text, encoding="utf-8", newline="\n")
    min_path.write_text(min_text, encoding="utf-8", newline="\n")
    return full_path, min_path


def check_catalogs(repo_root: Path) -> list[str]:
    problems: list[str] = []
    full_path = repo_root / FULL_CATALOG_PATH
    min_path = repo_root / MIN_CATALOG_PATH
    expected_full, expected_min = build_catalog_texts(repo_root)

    for path in (full_path, min_path):
        if not path.is_file():
            problems.append(f"missing {relative_path(path, repo_root)}")

    if full_path.is_file() and full_path.read_text(encoding="utf-8") != expected_full:
        problems.append(f"stale {relative_path(full_path, repo_root)}")

    if min_path.is_file() and min_path.read_text(encoding="utf-8") != expected_min:
        problems.append(f"stale {relative_path(min_path, repo_root)}")

    return problems


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.check:
            problems = check_catalogs(repo_root)
            if problems:
                print("Catalog check failed.")
                for problem in problems:
                    print(f"- {problem}")
                return 1
            print(f"Catalog check passed for {len(discover_skill_names(repo_root))} skills.")
            return 0

        full_path, min_path = write_catalogs(repo_root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(
        "Catalog build wrote "
        f"{relative_path(full_path, repo_root)} and {relative_path(min_path, repo_root)}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
