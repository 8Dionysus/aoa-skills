#!/usr/bin/env python3
"""Local validator for aoa-skills bundles."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
SKILL_INDEX_NAME = "SKILL_INDEX.md"

ALLOWED_SCOPES = {"core", "project", "risk"}
ALLOWED_STATUS = {
    "scaffold",
    "linked",
    "reviewed",
    "evaluated",
    "canonical",
    "deprecated",
}
ALLOWED_INVOCATION_MODES = {
    "implicit-friendly",
    "explicit-preferred",
    "explicit-only",
}
REQUIRED_FRONTMATTER_KEYS = {
    "name",
    "scope",
    "status",
    "summary",
    "invocation_mode",
    "technique_dependencies",
}
REQUIRED_HEADINGS = {
    "Intent",
    "Trigger boundary",
    "Inputs",
    "Outputs",
    "Procedure",
    "Contracts",
    "Risks and anti-patterns",
    "Verification",
    "Adaptation points",
}
TRACEABILITY_HEADINGS = {"Technique traceability", "Future traceability"}
ALLOWED_TECHNIQUE_SECTIONS = {
    "Intent",
    "When to use",
    "When not to use",
    "Inputs",
    "Outputs",
    "Core procedure",
    "Contracts",
    "Risks",
    "Validation",
    "Adaptation notes",
    "summary",
}
REPO_NAME = "8Dionysus/aoa-techniques"


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local aoa-skills bundles.")
    parser.add_argument(
        "--skill",
        help="Validate a single skill bundle by directory name.",
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


def relative_location(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_skill_markdown(
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, set[str]]:
    try:
        text = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(skill_md_path), "file is missing"))
        return None, set()

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, set()

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "missing YAML frontmatter closing delimiter",
            )
        )
        return None, set()

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, set()

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(skill_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, set()

    headings = set(
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    )
    return metadata, headings


def find_support_artifacts(skill_dir: Path) -> list[Path]:
    artifacts: list[Path] = []
    for folder_name in ("examples", "checks"):
        folder = skill_dir / folder_name
        if folder.is_dir():
            artifacts.extend(sorted(folder.glob("*.md")))
    return artifacts


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

    if not find_support_artifacts(skill_dir):
        issues.append(
            ValidationIssue(
                relative_location(skill_dir),
                "missing support artifact under examples/*.md or checks/*.md",
            )
        )

    metadata: dict[str, Any] | None = None
    headings: set[str] = set()
    if skill_md_path.is_file():
        metadata, headings = parse_skill_markdown(skill_md_path, issues)
        if metadata is not None:
            validate_skill_frontmatter(skill_name, metadata, skill_md_path, issues)
            validate_skill_headings(headings, skill_md_path, issues)

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

    return issues


def validate_skill_frontmatter(
    skill_name: str,
    metadata: dict[str, Any],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    missing = sorted(REQUIRED_FRONTMATTER_KEYS - metadata.keys())
    for key in missing:
        issues.append(ValidationIssue(location, f"missing frontmatter key '{key}'"))

    if metadata.get("name") != skill_name:
        issues.append(
            ValidationIssue(location, "frontmatter 'name' must match the directory name")
        )

    if metadata.get("scope") not in ALLOWED_SCOPES:
        issues.append(
            ValidationIssue(
                location,
                f"frontmatter 'scope' must be one of {sorted(ALLOWED_SCOPES)}",
            )
        )

    if metadata.get("status") not in ALLOWED_STATUS:
        issues.append(
            ValidationIssue(
                location,
                f"frontmatter 'status' must be one of {sorted(ALLOWED_STATUS)}",
            )
        )

    if not isinstance(metadata.get("summary"), str) or not metadata.get("summary", "").strip():
        issues.append(
            ValidationIssue(location, "frontmatter 'summary' must be a non-empty string")
        )

    if metadata.get("invocation_mode") not in ALLOWED_INVOCATION_MODES:
        issues.append(
            ValidationIssue(
                location,
                "frontmatter 'invocation_mode' must be one of "
                f"{sorted(ALLOWED_INVOCATION_MODES)}",
            )
        )

    technique_dependencies = metadata.get("technique_dependencies")
    if not isinstance(technique_dependencies, list):
        issues.append(
            ValidationIssue(
                location,
                "frontmatter 'technique_dependencies' must be a list",
            )
        )


def validate_skill_headings(
    headings: set[str],
    skill_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(skill_md_path)
    for heading in sorted(REQUIRED_HEADINGS - headings):
        issues.append(ValidationIssue(location, f"missing required section '{heading}'"))

    if not TRACEABILITY_HEADINGS.intersection(headings):
        issues.append(
            ValidationIssue(
                location,
                "missing traceability section; expected 'Technique traceability' or "
                "'Future traceability'",
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

    for key in ("skill_name", "composition_mode", "techniques"):
        if key not in manifest:
            issues.append(ValidationIssue(location, f"missing key '{key}'"))

    if manifest.get("skill_name") != skill_name:
        issues.append(
            ValidationIssue(location, "'skill_name' must match the directory name")
        )

    if manifest.get("composition_mode") != "bounded":
        issues.append(
            ValidationIssue(location, "'composition_mode' must be 'bounded'")
        )

    techniques = manifest.get("techniques")
    if not isinstance(techniques, list) or not techniques:
        issues.append(
            ValidationIssue(location, "'techniques' must be a non-empty list")
        )
        return

    notes = manifest.get("notes")
    pending_ids: list[str] = []
    for index, technique in enumerate(techniques, start=1):
        entry_location = f"{location} [technique #{index}]"
        if not isinstance(technique, dict):
            issues.append(ValidationIssue(entry_location, "entry must be a mapping"))
            continue

        for key in ("id", "repo", "path", "use_sections"):
            if key not in technique:
                issues.append(ValidationIssue(entry_location, f"missing key '{key}'"))

        technique_id = technique.get("id")
        if not isinstance(technique_id, str) or not technique_id.strip():
            issues.append(ValidationIssue(entry_location, "'id' must be a non-empty string"))
            continue

        repo = technique.get("repo")
        if repo != REPO_NAME:
            issues.append(
                ValidationIssue(
                    entry_location,
                    f"'repo' must be '{REPO_NAME}'",
                )
            )

        path_value = technique.get("path")
        if not isinstance(path_value, str) or not path_value.strip():
            issues.append(
                ValidationIssue(entry_location, "'path' must be a non-empty string")
            )
        elif technique_id.startswith("AOA-T-PENDING-"):
            pending_ids.append(technique_id)
            if path_value != "TBD":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "pending techniques must use path 'TBD'",
                    )
                )
        elif path_value == "TBD":
            issues.append(
                ValidationIssue(
                    entry_location,
                    "published techniques cannot use path 'TBD'",
                )
            )

        use_sections = technique.get("use_sections")
        if not isinstance(use_sections, list) or not use_sections:
            issues.append(
                ValidationIssue(
                    entry_location,
                    "'use_sections' must be a non-empty list",
                )
            )
        else:
            for section in use_sections:
                if not isinstance(section, str) or section not in ALLOWED_TECHNIQUE_SECTIONS:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            f"invalid section '{section}' in 'use_sections'",
                        )
                    )

    if pending_ids and not has_pending_note(notes, pending_ids):
        issues.append(
            ValidationIssue(
                location,
                "pending techniques require a note explaining that pending IDs and "
                "path TBD must be replaced after publication",
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
    if not isinstance(policy_data, dict):
        issues.append(ValidationIssue(location, "policy file must parse to a mapping"))
        return

    policy = policy_data.get("policy")
    if not isinstance(policy, dict):
        issues.append(ValidationIssue(location, "missing mapping 'policy'"))
        return

    allow_implicit = policy.get("allow_implicit_invocation")
    if not isinstance(allow_implicit, bool):
        issues.append(
            ValidationIssue(
                location,
                "'policy.allow_implicit_invocation' must be a boolean",
            )
        )


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

    pattern = re.compile(r"^\|\s*(aoa-[a-z0-9-]+)\s*\|", flags=re.MULTILINE)
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


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_dir = repo_root / SKILLS_DIR_NAME
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"missing skills directory at {skills_dir}")
    return sorted(path.name for path in skills_dir.iterdir() if path.is_dir())


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(repo_root: Path, skill_name: str | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    all_skill_names = discover_skill_names(repo_root)
    if skill_name is not None:
        if skill_name not in all_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        target_skills = [skill_name]
        selected_skills = {skill_name}
    else:
        target_skills = all_skill_names
        selected_skills = None

    for name in target_skills:
        issues.extend(validate_skill_bundle(repo_root, name))

    issues.extend(validate_skill_index(repo_root, selected_skills=selected_skills))
    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        issues = run_validation(repo_root, skill_name=args.skill)
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
