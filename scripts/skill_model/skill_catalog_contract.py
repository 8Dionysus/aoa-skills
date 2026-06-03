from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


SHORT_REPO_NAMES = {
    "aoa-techniques": "aoa-techniques",
    "aoa-skills": "aoa-skills",
    "aoa-evals": "aoa-evals",
    "aoa-memo": "aoa-memo",
}
EXPECTED_TECHNIQUE_REPO = "aoa-techniques"


@dataclass(frozen=True)
class ContractIssue:
    location: str
    message: str


def relative_location(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def format_issues(issues: list[ContractIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


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


def collect_technique_ref_issues(
    manifest: dict[str, Any],
    techniques_path: Path,
    repo_root: Path,
) -> list[ContractIssue]:
    location = relative_location(techniques_path, repo_root)
    techniques = manifest.get("techniques", [])
    if not isinstance(techniques, list):
        return [ContractIssue(location, "techniques.yaml must contain a techniques list")]

    issues: list[ContractIssue] = []
    for index, technique in enumerate(techniques, start=1):
        if not isinstance(technique, dict):
            issues.append(
                ContractIssue(
                    f"{location} [technique #{index}]",
                    "each techniques.yaml technique entry must be an object",
                )
            )
            continue

        entry_location = f"{location} [technique #{index}]"
        technique_id = technique.get("id")
        path_value = technique.get("path")
        source_ref = technique.get("source_ref")

        if not isinstance(technique_id, str):
            issues.append(
                ContractIssue(
                    entry_location,
                    "each techniques.yaml technique entry must define string id",
                )
            )
            continue

        try:
            normalized_repo_name = normalize_repo_name(technique.get("repo"))
        except ValueError as exc:
            issues.append(ContractIssue(entry_location, str(exc)))
            normalized_repo_name = None

        if normalized_repo_name != EXPECTED_TECHNIQUE_REPO:
            issues.append(
                ContractIssue(
                    entry_location,
                    f"repo must resolve to '{EXPECTED_TECHNIQUE_REPO}'",
                )
            )

        if not isinstance(path_value, str):
            issues.append(
                ContractIssue(
                    entry_location,
                    f"technique '{technique_id}' must define string path",
                )
            )
        if not isinstance(source_ref, str):
            issues.append(
                ContractIssue(
                    entry_location,
                    f"technique '{technique_id}' must define string source_ref",
                )
            )

        if not isinstance(path_value, str) or not isinstance(source_ref, str):
            continue

        if technique_id.startswith("AOA-T-PENDING-"):
            if path_value != "TBD":
                issues.append(
                    ContractIssue(
                        entry_location,
                        "pending techniques must use path 'TBD'",
                    )
                )
            if source_ref != "TBD":
                issues.append(
                    ContractIssue(
                        entry_location,
                        "pending techniques must use source_ref 'TBD'",
                    )
                )
            continue

        if path_value == "TBD":
            issues.append(
                ContractIssue(
                    entry_location,
                    "published techniques cannot use path 'TBD'",
                )
            )
        elif not is_repo_relative_path(path_value):
            issues.append(
                ContractIssue(
                    entry_location,
                    "published techniques must use concrete repo-relative paths",
                )
            )

        if source_ref == "TBD":
            issues.append(
                ContractIssue(
                    entry_location,
                    "published techniques cannot use source_ref 'TBD'",
                )
            )

    return issues


def collect_skill_parity_issues(
    skill_name: str,
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    skill_md_path: Path,
    repo_root: Path,
) -> list[ContractIssue]:
    location = relative_location(skill_md_path, repo_root)
    issues: list[ContractIssue] = []

    if metadata.get("name") != skill_name:
        issues.append(
            ContractIssue(location, "frontmatter 'name' must match the directory name")
        )

    manifest_skill_name = manifest.get("skill_name")
    if manifest_skill_name != skill_name:
        issues.append(
            ContractIssue(
                location,
                "frontmatter 'name' must match techniques.yaml 'skill_name'",
            )
        )

    dependencies = metadata.get("technique_dependencies")
    if not isinstance(dependencies, list):
        issues.append(
            ContractIssue(
                location,
                "frontmatter 'technique_dependencies' must be a list",
            )
        )
        return issues

    if not all(isinstance(dependency, str) for dependency in dependencies):
        issues.append(
            ContractIssue(
                location,
                "frontmatter 'technique_dependencies' must only contain strings",
            )
        )
        return issues

    try:
        manifest_ids = technique_ids_from_manifest(manifest)
    except ValueError as exc:
        issues.append(ContractIssue(location, str(exc)))
        return issues
    if dependencies != manifest_ids:
        issues.append(
            ContractIssue(
                location,
                "frontmatter 'technique_dependencies' must exactly match techniques.yaml technique IDs in order",
            )
        )

    return issues


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


def build_skill_entry_from_sources(
    repo_root: Path,
    skill_name: str,
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    skill_md_path: Path,
    techniques_path: Path,
) -> tuple[dict[str, Any] | None, list[ContractIssue]]:
    issues = collect_skill_parity_issues(
        skill_name,
        metadata,
        manifest,
        skill_md_path,
        repo_root,
    )
    issues.extend(collect_technique_ref_issues(manifest, techniques_path, repo_root))
    if issues:
        return None, issues

    entry = {
        "name": metadata.get("name"),
        "scope": metadata.get("scope"),
        "status": metadata.get("status"),
        "summary": metadata.get("summary"),
        "invocation_mode": metadata.get("invocation_mode"),
        "technique_dependencies": list(metadata.get("technique_dependencies", [])),
        "skill_path": relative_location(skill_md_path, repo_root),
        "composition_mode": manifest.get("composition_mode"),
        "technique_refs": normalize_technique_refs(manifest),
    }
    return entry, []
