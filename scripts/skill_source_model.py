from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml

import skill_artifact_contract
import skill_catalog_contract
import skill_section_contract


SKILLS_DIR_NAME = "skills"
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"


@dataclass(frozen=True)
class SkillSource:
    name: str
    skill_dir: Path
    skill_md_path: Path
    techniques_path: Path
    policy_path: Path
    metadata: dict[str, Any]
    body: str
    sections: dict[str, str]
    manifest: dict[str, Any]
    policy_exists: bool
    policy_allow_implicit_invocation: Any
    promotion_review_path: str | None
    candidate_review_path: str | None
    support_artifacts: list[dict[str, Any]]
    selected_runtime_artifact_path: str | None


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_optional_yaml(path: Path) -> Any | None:
    if not path.is_file():
        return None
    try:
        return load_yaml(path)
    except yaml.YAMLError:
        return None


def parse_skill_document(path: Path) -> tuple[dict[str, Any], str]:
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
    body = "\n".join(lines[closing_index + 1 :])
    return metadata, body


def parse_skill_sections(body: str) -> dict[str, str]:
    return {
        heading: content_markdown
        for heading, content_markdown in skill_section_contract.extract_top_level_sections(body)
    }


def review_record_path(
    repo_root: Path,
    reviews_dir: Path,
    skill_name: str,
) -> str | None:
    review_path = repo_root / reviews_dir / f"{skill_name}.md"
    if review_path.is_file():
        return relative_location(review_path, repo_root)
    return None


def load_policy_signal(repo_root: Path, skill_name: str) -> tuple[bool, Any]:
    policy_path = repo_root / SKILLS_DIR_NAME / skill_name / "agents" / "openai.yaml"
    policy_data = load_optional_yaml(policy_path)
    if not isinstance(policy_data, dict):
        return policy_path.is_file(), None
    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        return True, None
    return True, policy.get("allow_implicit_invocation")


def selected_runtime_artifact_path(repo_root: Path, skill_name: str) -> str | None:
    selected_path = skill_artifact_contract.preferred_runtime_artifact(
        repo_root / SKILLS_DIR_NAME / skill_name
    )
    if selected_path is None:
        return None
    return relative_location(selected_path, repo_root)


def load_skill_source(repo_root: Path, skill_name: str) -> SkillSource:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    techniques_path = skill_dir / "techniques.yaml"
    policy_path = skill_dir / "agents" / "openai.yaml"

    metadata, body = parse_skill_document(skill_md_path)
    manifest = load_yaml(techniques_path)
    if not isinstance(manifest, dict):
        raise ValueError(f"{techniques_path} must parse to a mapping")

    policy_exists, policy_allow_implicit_invocation = load_policy_signal(repo_root, skill_name)
    support_artifacts = skill_artifact_contract.collect_support_artifacts(repo_root, skill_name)

    return SkillSource(
        name=skill_name,
        skill_dir=skill_dir,
        skill_md_path=skill_md_path,
        techniques_path=techniques_path,
        policy_path=policy_path,
        metadata=metadata,
        body=body,
        sections=parse_skill_sections(body),
        manifest=manifest,
        policy_exists=policy_exists,
        policy_allow_implicit_invocation=policy_allow_implicit_invocation,
        promotion_review_path=review_record_path(
            repo_root,
            STATUS_PROMOTION_REVIEWS_DIR,
            skill_name,
        ),
        candidate_review_path=review_record_path(
            repo_root,
            CANONICAL_CANDIDATES_DIR,
            skill_name,
        ),
        support_artifacts=support_artifacts,
        selected_runtime_artifact_path=selected_runtime_artifact_path(
            repo_root,
            skill_name,
        ),
    )


def load_skill_sources(
    repo_root: Path,
    skill_names: Sequence[str] | None = None,
) -> list[SkillSource]:
    selected_skill_names = (
        list(skill_names) if skill_names is not None else discover_skill_names(repo_root)
    )
    return [load_skill_source(repo_root, skill_name) for skill_name in selected_skill_names]
