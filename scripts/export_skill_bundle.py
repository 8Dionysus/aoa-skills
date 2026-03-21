#!/usr/bin/env python3
"""Read-only export preview for a single portable aoa-skills bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_catalog_contract
import skill_source_model


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_VERSION = 1
SUPPORTED_FORMATS = {"json", "text"}
SKILLS_DIR_NAME = "skills"
GENERATED_SURFACE_SPECS = (
    ("skill_catalog", Path("generated") / "skill_catalog.json"),
    ("skill_catalog_min", Path("generated") / "skill_catalog.min.json"),
    ("skill_capsules", Path("generated") / "skill_capsules.json"),
    ("skill_sections", Path("generated") / "skill_sections.full.json"),
    ("skill_walkthroughs", Path("generated") / "skill_walkthroughs.json"),
    ("skill_evaluation_matrix", Path("generated") / "skill_evaluation_matrix.json"),
    ("public_surface", Path("generated") / "public_surface.json"),
    ("skill_lineage_surface", Path("generated") / "skill_lineage_surface.json"),
    ("skill_boundary_matrix", Path("generated") / "skill_boundary_matrix.json"),
    ("governance_backlog", Path("generated") / "governance_backlog.json"),
    ("skill_bundle_index", Path("generated") / "skill_bundle_index.json"),
    ("skill_graph", Path("generated") / "skill_graph.json"),
)


class ExportSkillBundleError(ValueError):
    pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only export preview for a single aoa-skills bundle."
    )
    parser.add_argument(
        "--skill",
        required=True,
        help="Skill directory name to export.",
    )
    parser.add_argument(
        "--format",
        default="json",
        help="One of: json, text.",
    )
    return parser.parse_args(argv)


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json_file(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ExportSkillBundleError(f"missing generated surface at {path.as_posix()}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExportSkillBundleError(
            f"invalid JSON in {path.as_posix()}: {exc.msg}"
        ) from exc
    if not isinstance(payload, dict):
        raise ExportSkillBundleError(
            f"generated surface at {path.as_posix()} must parse to an object"
        )
    return payload


def find_named_entry(payload: Mapping[str, Any], skill_name: str) -> Mapping[str, Any] | None:
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        return None
    for entry in skills:
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
            return entry
    return None


def matching_cases(payload: Mapping[str, Any], skill_name: str) -> list[Mapping[str, Any]]:
    cases = payload.get("cases", [])
    if not isinstance(cases, list):
        return []
    matches: list[Mapping[str, Any]] = []
    for case in cases:
        if not isinstance(case, Mapping):
            continue
        if case.get("skill") == skill_name or case.get("adjacent_skill") == skill_name:
            matches.append(case)
    return matches


def matching_cohorts(payload: Mapping[str, Any], skill_name: str) -> dict[str, list[str]]:
    cohorts = payload.get("cohorts", {})
    if not isinstance(cohorts, Mapping):
        return {}
    matched: dict[str, list[str]] = {}
    for cohort_name, members in cohorts.items():
        if not isinstance(members, list):
            continue
        if skill_name in members:
            matched[str(cohort_name)] = [str(member) for member in members]
    return matched


def file_record(path: Path, repo_root: Path, *, kind: str, include_content: bool = True) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    record: dict[str, Any] = {
        "kind": kind,
        "path": relative_location(path, repo_root),
        "sha256": sha256_text(content),
    }
    if include_content:
        record["content"] = content
    return record


def file_record_if_exists(
    path: Path,
    repo_root: Path,
    *,
    kind: str,
    include_content: bool = True,
) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return file_record(path, repo_root, kind=kind, include_content=include_content)


def support_artifact_records(
    repo_root: Path,
    support_artifacts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for artifact in sorted(
        support_artifacts,
        key=lambda item: (str(item.get("type", "")), str(item.get("path", ""))),
    ):
        artifact_path = artifact.get("path")
        if not isinstance(artifact_path, str):
            continue
        path = repo_root / artifact_path
        if not path.is_file():
            continue
        artifact_type = str(artifact.get("type", "artifact"))
        if artifact_type not in {"runtime_example", "review_checklist"}:
            continue
        records.append(
            {
                "type": artifact_type,
                "path": artifact_path,
                "selected_for_runtime_inspection": bool(
                    artifact.get("selected_for_runtime_inspection")
                ),
                "sha256": sha256_text(path.read_text(encoding="utf-8")),
                "content": path.read_text(encoding="utf-8"),
            }
        )
    return records


def review_surface_records(
    repo_root: Path,
    support_artifacts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for artifact in sorted(
        support_artifacts,
        key=lambda item: (str(item.get("type", "")), str(item.get("path", ""))),
    ):
        artifact_type = artifact.get("type")
        if artifact_type not in {"promotion_review", "candidate_review"}:
            continue
        artifact_path = artifact.get("path")
        if not isinstance(artifact_path, str):
            continue
        path = repo_root / artifact_path
        if not path.is_file():
            continue
        records.append(
            {
                "type": str(artifact_type),
                "path": artifact_path,
                "sha256": sha256_text(path.read_text(encoding="utf-8")),
                "content": path.read_text(encoding="utf-8"),
            }
        )
    return records


def generated_surface_record(repo_root: Path, skill_name: str, surface_name: str, path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "name": surface_name,
        "path": relative_location(path, repo_root),
        "present": path.is_file(),
    }
    if not path.is_file():
        return record

    if path.suffix.lower() != ".json":
        content = path.read_text(encoding="utf-8")
        record["sha256"] = sha256_text(content)
        record["snippet"] = content[:1000]
        return record

    payload = load_json_file(path)
    record["sha256"] = sha256_text(path.read_text(encoding="utf-8"))
    snippet: dict[str, Any] = {}

    entry = find_named_entry(payload, skill_name)
    if entry is not None:
        snippet["entry"] = entry

    cohort_memberships = matching_cohorts(payload, skill_name)
    if cohort_memberships:
        snippet["cohorts"] = cohort_memberships

    cases = matching_cases(payload, skill_name)
    if cases:
        snippet["cases"] = cases

    if "nodes" in payload and "edges" in payload and not snippet:
        snippet["summary"] = {
            "node_count": len(payload.get("nodes", []))
            if isinstance(payload.get("nodes"), list)
            else 0,
            "edge_count": len(payload.get("edges", []))
            if isinstance(payload.get("edges"), list)
            else 0,
        }

    if "cohorts" in payload and not snippet:
        snippet["cohorts"] = payload.get("cohorts")

    if not snippet:
        snippet["keys"] = sorted(payload.keys())

    record["snippet"] = snippet
    return record


def build_export_payload(repo_root: Path, skill_name: str) -> dict[str, Any]:
    try:
        source = skill_source_model.load_skill_source(repo_root, skill_name)
    except FileNotFoundError as exc:
        raise ExportSkillBundleError(f"unknown skill '{skill_name}'") from exc

    bundle_files = [
        file_record(source.skill_md_path, repo_root, kind="skill_markdown"),
        file_record(source.techniques_path, repo_root, kind="technique_manifest"),
    ]
    if source.policy_path.is_file():
        bundle_files.append(
            file_record(source.policy_path, repo_root, kind="invocation_policy")
        )

    skill_bundle_files = [
        bundle_file
        for bundle_file in bundle_files
        if bundle_file is not None
    ]

    return {
        "export_version": EXPORT_VERSION,
        "skill": {
            "name": source.name,
            "scope": source.metadata.get("scope"),
            "status": source.metadata.get("status"),
            "summary": source.metadata.get("summary"),
            "invocation_mode": source.metadata.get("invocation_mode"),
            "skill_path": relative_location(source.skill_md_path, repo_root),
            "selected_runtime_artifact_path": source.selected_runtime_artifact_path,
            "promotion_review_path": source.promotion_review_path,
            "candidate_review_path": source.candidate_review_path,
        },
        "manifest_facts": {
            "composition_mode": source.manifest.get("composition_mode"),
            "technique_dependencies": list(source.metadata.get("technique_dependencies", [])),
            "technique_refs": skill_catalog_contract.normalize_technique_refs(
                source.manifest
            ),
        },
        "bundle_files": skill_bundle_files,
        "support_artifacts": support_artifact_records(repo_root, source.support_artifacts),
        "review_surfaces": review_surface_records(repo_root, source.support_artifacts),
        "generated_surfaces": [
            generated_surface_record(repo_root, skill_name, surface_name, path)
            for surface_name, path in GENERATED_SURFACE_SPECS
        ],
    }


def render_text(payload: Mapping[str, Any]) -> str:
    skill = payload.get("skill", {})
    bundle_files = payload.get("bundle_files", [])
    support_artifacts = payload.get("support_artifacts", [])
    review_surfaces = payload.get("review_surfaces", [])
    generated_surfaces = payload.get("generated_surfaces", [])

    lines = [
        "# Skill bundle export preview",
        "",
        f"- skill: {skill.get('name')}",
        f"- scope: {skill.get('scope')}",
        f"- status: {skill.get('status')}",
        f"- invocation mode: {skill.get('invocation_mode')}",
        f"- selected runtime artifact: {skill.get('selected_runtime_artifact_path') or '-'}",
        "",
        "## Bundle files",
        "",
    ]
    if bundle_files:
        for record in bundle_files:
            lines.append(f"- {record['kind']}: `{record['path']}`")
    else:
        lines.append("- none")

    lines.extend(["", "## Support artifacts", ""])
    if support_artifacts:
        for record in support_artifacts:
            marker = " (selected)" if record.get("selected_for_runtime_inspection") else ""
            lines.append(f"- {record['type']}{marker}: `{record['path']}`")
    else:
        lines.append("- none")

    lines.extend(["", "## Review surfaces", ""])
    if review_surfaces:
        for record in review_surfaces:
            lines.append(f"- {record['type']}: `{record['path']}`")
    else:
        lines.append("- none")

    lines.extend(["", "## Generated surfaces", ""])
    if generated_surfaces:
        for record in generated_surfaces:
            status = "present" if record.get("present") else "missing"
            lines.append(f"- {record['name']}: `{record['path']}` ({status})")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def render_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.format not in SUPPORTED_FORMATS:
        print(f"Runtime error: unknown format '{args.format}'", file=sys.stderr)
        return 2

    try:
        payload = build_export_payload(repo_root, args.skill)
        if args.format == "json":
            sys.stdout.write(render_json(payload))
        else:
            sys.stdout.write(render_text(payload) + "\n")
    except ExportSkillBundleError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive runtime guard
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
