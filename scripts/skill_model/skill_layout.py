from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SKILLS_DIR_NAME = "skills"
SKILL_DOC_NAME = "SKILL.md"
TECHNIQUES_DOC_NAME = "techniques.yaml"


@dataclass(frozen=True)
class SkillBundlePath:
    name: str
    skill_dir: Path
    skill_md_path: Path
    techniques_path: Path
    policy_path: Path


def skills_root(repo_root: Path) -> Path:
    return repo_root / SKILLS_DIR_NAME


def _raise_for_duplicates(entries: list[SkillBundlePath]) -> None:
    by_name: dict[str, list[Path]] = {}
    for entry in entries:
        by_name.setdefault(entry.name, []).append(entry.skill_dir)
    duplicates = {
        name: paths
        for name, paths in by_name.items()
        if len(paths) > 1
    }
    if duplicates:
        details = "; ".join(
            f"{name}: {', '.join(path.as_posix() for path in paths)}"
            for name, paths in sorted(duplicates.items())
        )
        raise ValueError(f"duplicate skill bundle directories: {details}")


def discover_skill_bundle_paths(repo_root: Path) -> list[SkillBundlePath]:
    root = skills_root(repo_root)
    if not root.is_dir():
        raise FileNotFoundError(f"missing skills directory at {root}")

    entries: list[SkillBundlePath] = []
    for skill_md_path in sorted(root.rglob(SKILL_DOC_NAME)):
        skill_dir = skill_md_path.parent
        if skill_dir == root:
            continue
        entries.append(
            SkillBundlePath(
                name=skill_dir.name,
                skill_dir=skill_dir,
                skill_md_path=skill_md_path,
                techniques_path=skill_dir / TECHNIQUES_DOC_NAME,
                policy_path=skill_dir / "agents" / "openai.yaml",
            )
        )

    _raise_for_duplicates(entries)
    return sorted(entries, key=lambda entry: entry.name)


def discover_skill_path_map(repo_root: Path) -> dict[str, SkillBundlePath]:
    return {
        entry.name: entry
        for entry in discover_skill_bundle_paths(repo_root)
    }


def discover_skill_names(repo_root: Path) -> list[str]:
    return [entry.name for entry in discover_skill_bundle_paths(repo_root)]


def skill_bundle_path(repo_root: Path, skill_name: str) -> SkillBundlePath | None:
    return discover_skill_path_map(repo_root).get(skill_name)


def skill_dir_path(repo_root: Path, skill_name: str) -> Path:
    entry = skill_bundle_path(repo_root, skill_name)
    if entry is not None:
        return entry.skill_dir
    return skills_root(repo_root) / skill_name


def skill_md_path(repo_root: Path, skill_name: str) -> Path:
    entry = skill_bundle_path(repo_root, skill_name)
    if entry is not None:
        return entry.skill_md_path
    return skills_root(repo_root) / skill_name / SKILL_DOC_NAME


def techniques_path(repo_root: Path, skill_name: str) -> Path:
    entry = skill_bundle_path(repo_root, skill_name)
    if entry is not None:
        return entry.techniques_path
    return skills_root(repo_root) / skill_name / TECHNIQUES_DOC_NAME


def policy_path(repo_root: Path, skill_name: str) -> Path:
    entry = skill_bundle_path(repo_root, skill_name)
    if entry is not None:
        return entry.policy_path
    return skills_root(repo_root) / skill_name / "agents" / "openai.yaml"
