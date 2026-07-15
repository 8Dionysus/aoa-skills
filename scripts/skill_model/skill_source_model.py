from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml

from skill_model import skill_layout, skill_section_contract


SKILLS_DIR_NAME = skill_layout.SKILLS_DIR_NAME


@dataclass(frozen=True)
class SkillSource:
    name: str
    skill_dir: Path
    skill_md_path: Path
    policy_path: Path
    metadata: dict[str, Any]
    body: str
    sections: dict[str, str]


def relative_location(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def discover_skill_names(repo_root: Path) -> list[str]:
    return skill_layout.discover_skill_names(repo_root)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_skill_document(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} is missing frontmatter")
    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        raise ValueError(f"{path} is missing a closing frontmatter delimiter")
    metadata = yaml.safe_load("\n".join(lines[1:closing_index])) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"{path} frontmatter must parse to a mapping")
    return metadata, "\n".join(lines[closing_index + 1 :])


def parse_skill_sections(body: str) -> dict[str, str]:
    return {
        heading: content_markdown
        for heading, content_markdown in skill_section_contract.extract_top_level_sections(body)
    }


def load_skill_source(repo_root: Path, skill_name: str) -> SkillSource:
    skill_dir = skill_layout.skill_dir_path(repo_root, skill_name)
    skill_md_path = skill_layout.skill_md_path(repo_root, skill_name)
    metadata, body = parse_skill_document(skill_md_path)
    return SkillSource(
        name=skill_name,
        skill_dir=skill_dir,
        skill_md_path=skill_md_path,
        policy_path=skill_layout.policy_path(repo_root, skill_name),
        metadata=metadata,
        body=body,
        sections=parse_skill_sections(body),
    )


def load_skill_sources(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[SkillSource]:
    selected = list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    return [load_skill_source(repo_root, skill_name) for skill_name in selected]
