from __future__ import annotations

import copy
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml

import build_catalog
import skill_catalog_contract


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR_NAME = "skills"
DEFAULT_TECHNIQUES_REPO = REPO_ROOT.parent / "aoa-techniques"


class _IndentedSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False):  # type: ignore[override]
        return super().increase_indent(flow, False)


@dataclass(frozen=True)
class SkillTechniqueBundle:
    skill_name: str
    skill_dir: Path
    skill_md_path: Path
    techniques_path: Path
    metadata: dict[str, Any]
    body: str
    manifest: dict[str, Any]
    technique_refs: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class TechniqueDriftRecord:
    skill_name: str
    technique_id: str
    path: str
    pinned_ref: str
    target_ref: str
    state: str


def render_yaml(data: Any) -> str:
    return yaml.dump(
        data,
        Dumper=_IndentedSafeDumper,
        sort_keys=False,
        width=4096,
    ).strip() + "\n"


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def resolve_skill_names(
    repo_root: Path,
    requested_skill_names: Sequence[str] | None = None,
) -> list[str]:
    available_skill_names = build_catalog.discover_skill_names(repo_root)
    if requested_skill_names is None:
        return available_skill_names

    selected_skill_names: list[str] = []
    seen: set[str] = set()
    for skill_name in requested_skill_names:
        if skill_name in seen:
            continue
        if skill_name not in available_skill_names:
            raise ValueError(f"unknown skill '{skill_name}'")
        seen.add(skill_name)
        selected_skill_names.append(skill_name)
    return selected_skill_names


def load_skill_bundle(repo_root: Path, skill_name: str) -> SkillTechniqueBundle:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    skill_md_path = skill_dir / "SKILL.md"
    techniques_path = skill_dir / "techniques.yaml"

    metadata, body = build_catalog.parse_skill_document(skill_md_path)
    manifest = build_catalog.load_yaml(techniques_path)
    if not isinstance(manifest, dict):
        raise ValueError(f"{techniques_path} must contain a mapping")

    entry, issues = skill_catalog_contract.build_skill_entry_from_sources(
        repo_root,
        skill_name,
        metadata,
        manifest,
        skill_md_path,
        techniques_path,
    )
    if issues:
        raise ValueError(skill_catalog_contract.format_issues(issues))
    if entry is None:
        raise ValueError(f"unable to build skill entry for '{skill_name}'")

    return SkillTechniqueBundle(
        skill_name=skill_name,
        skill_dir=skill_dir,
        skill_md_path=skill_md_path,
        techniques_path=techniques_path,
        metadata=metadata,
        body=body,
        manifest=manifest,
        technique_refs=tuple(entry["technique_refs"]),
    )


def resolve_skill_bundles(
    repo_root: Path,
    requested_skill_names: Sequence[str] | None = None,
) -> list[SkillTechniqueBundle]:
    return [
        load_skill_bundle(repo_root, skill_name)
        for skill_name in resolve_skill_names(repo_root, requested_skill_names)
    ]


def is_pending_technique_ref(ref: dict[str, Any]) -> bool:
    technique_id = ref.get("id")
    path_value = ref.get("path")
    source_ref = ref.get("source_ref")
    return (
        isinstance(technique_id, str)
        and technique_id.startswith("AOA-T-PENDING-")
    ) or path_value == "TBD" or source_ref == "TBD"


def copy_manifest_with_target_ref(
    manifest: dict[str, Any],
    target_ref: str,
) -> tuple[dict[str, Any], list[tuple[str, str, str, str]]]:
    updated_manifest = copy.deepcopy(manifest)
    updated_refs: list[tuple[str, str, str, str]] = []

    techniques = updated_manifest.get("techniques")
    if not isinstance(techniques, list):
        raise ValueError("techniques.yaml must contain a techniques list")

    for technique in techniques:
        if not isinstance(technique, dict):
            raise ValueError("each techniques.yaml technique entry must be an object")

        technique_id = technique.get("id")
        path_value = technique.get("path")
        old_source_ref = technique.get("source_ref")
        if not isinstance(technique_id, str):
            raise ValueError("each techniques.yaml technique entry must define string id")
        if not isinstance(path_value, str):
            raise ValueError(f"technique '{technique_id}' must define string path")
        if not isinstance(old_source_ref, str):
            raise ValueError(
                f"technique '{technique_id}' must define string source_ref"
            )

        if is_pending_technique_ref(technique):
            continue

        if old_source_ref != target_ref:
            technique["source_ref"] = target_ref
            updated_refs.append((technique_id, path_value, old_source_ref, target_ref))

    return updated_manifest, updated_refs


def resolve_techniques_repo(repo_path: Path) -> Path:
    candidate = repo_path.expanduser().resolve()
    if not candidate.exists():
        raise ValueError(f"techniques repo path does not exist: {candidate}")
    if not candidate.is_dir():
        raise ValueError(f"techniques repo path is not a directory: {candidate}")
    resolved_root = run_git_command(
        candidate,
        ["rev-parse", "--show-toplevel"],
        error_context=f"failed to resolve git repo at '{candidate}'",
    ).stdout.strip()
    return Path(resolved_root)


def resolve_git_ref(repo_root: Path, ref: str) -> str:
    return run_git_command(
        repo_root,
        ["rev-parse", f"{ref}^{{commit}}"],
        error_context=f"failed to resolve git ref '{ref}'",
    ).stdout.strip()


def ensure_commit_exists(repo_root: Path, ref: str) -> None:
    run_git_command(
        repo_root,
        ["cat-file", "-e", f"{ref}^{{commit}}"],
        error_context=f"missing git commit '{ref}'",
    )


def ensure_path_exists_at_ref(repo_root: Path, ref: str, relative_path: str) -> None:
    run_git_command(
        repo_root,
        ["cat-file", "-e", f"{ref}:{relative_path}"],
        error_context=f"missing path '{relative_path}' at ref '{ref}'",
    )


def path_changed_between_refs(
    repo_root: Path,
    start_ref: str,
    end_ref: str,
    relative_path: str,
) -> bool:
    result = run_git_command(
        repo_root,
        ["diff", "--quiet", f"{start_ref}..{end_ref}", "--", relative_path],
        check=False,
    )
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True

    detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
    raise ValueError(
        f"failed to diff path '{relative_path}' between '{start_ref}' and '{end_ref}': "
        f"{detail}"
    )


def collect_commit_summaries_for_path(
    repo_root: Path,
    start_ref: str,
    end_ref: str,
    relative_path: str,
    *,
    max_commits: int = 5,
) -> list[str]:
    result = run_git_command(
        repo_root,
        [
            "log",
            "--oneline",
            "--max-count",
            str(max_commits),
            f"{start_ref}..{end_ref}",
            "--",
            relative_path,
        ],
        error_context=(
            f"failed to read commit summary for '{relative_path}' between "
            f"'{start_ref}' and '{end_ref}'"
        ),
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def collect_drift_records(
    techniques_repo: Path,
    target_ref: str,
    bundle: SkillTechniqueBundle,
) -> list[TechniqueDriftRecord]:
    records: list[TechniqueDriftRecord] = []
    for ref in bundle.technique_refs:
        technique_id = ref["id"]
        path_value = ref["path"]
        source_ref = ref["source_ref"]

        if is_pending_technique_ref(ref):
            records.append(
                TechniqueDriftRecord(
                    skill_name=bundle.skill_name,
                    technique_id=technique_id,
                    path=path_value,
                    pinned_ref=source_ref,
                    target_ref=target_ref,
                    state="pending",
                )
            )
            continue

        ensure_commit_exists(techniques_repo, source_ref)
        ensure_path_exists_at_ref(techniques_repo, target_ref, path_value)
        state = (
            "drifted"
            if path_changed_between_refs(techniques_repo, source_ref, target_ref, path_value)
            else "clean"
        )
        records.append(
            TechniqueDriftRecord(
                skill_name=bundle.skill_name,
                technique_id=technique_id,
                path=path_value,
                pinned_ref=source_ref,
                target_ref=target_ref,
                state=state,
            )
        )

    return records


def run_git_command(
    repo_root: Path,
    args: Sequence[str],
    *,
    check: bool = True,
    error_context: str | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"failed to execute git: {exc}") from exc

    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        context = error_context or f"git {' '.join(args)} failed"
        raise ValueError(f"{context}: {detail}")

    return result
