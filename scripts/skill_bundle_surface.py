from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import build_support_resources
import release_manifest_contract
import skill_catalog_contract
import skill_evaluation_surface
import skill_governance_lane_contract
import skill_governance_surface
import skill_lineage_surface
import skill_relationship_contract
import skill_runtime_surface
import skill_source_model


BUNDLE_INDEX_VERSION = 2
BUNDLE_INDEX_JSON_PATH = Path("generated") / "skill_bundle_index.json"
BUNDLE_INDEX_MARKDOWN_PATH = Path("generated") / "skill_bundle_index.md"
SKILL_GRAPH_VERSION = 2
SKILL_GRAPH_JSON_PATH = Path("generated") / "skill_graph.json"
SKILL_GRAPH_MARKDOWN_PATH = Path("generated") / "skill_graph.md"
BUNDLE_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "technique_manifest": "skills/*/techniques.yaml",
    "runtime_examples": "skills/*/examples/*.md",
    "review_checks": "skills/*/checks/review.md",
    "status_promotion_reviews": "docs/reviews/status-promotions/*.md",
    "canonical_candidate_reviews": "docs/reviews/canonical-candidates/*.md",
}


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def hash_files(repo_root: Path, file_paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    ordered_paths = sorted(
        ((relative_location(path, repo_root), path) for path in file_paths),
        key=lambda item: item[0],
    )
    for relative_path_text, path in ordered_paths:
        relative_path = relative_path_text.encode("utf-8")
        digest.update(relative_path)
        digest.update(b"\0")
        normalized_text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        digest.update(normalized_text.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def bundle_file_paths(source: skill_source_model.SkillSource) -> list[Path]:
    paths = [source.skill_md_path, source.techniques_path]
    if source.policy_path.is_file():
        paths.append(source.policy_path)

    for artifact in source.support_artifacts:
        artifact_path = artifact.get("path")
        if isinstance(artifact_path, str):
            candidate = source.skill_md_path.parents[2] / artifact_path
            if candidate.is_file():
                paths.append(candidate)
    unique_paths: dict[Path, None] = {}
    for path in paths:
        unique_paths[path] = None
    return list(unique_paths)


def bundle_entry(
    source: skill_source_model.SkillSource,
    *,
    repo_root: Path,
    public_entry: Mapping[str, Any],
    evaluation_entry: Mapping[str, Any],
    lineage_entry: Mapping[str, Any],
    relationship_entry: Mapping[str, Any],
    generated_surface_versions: Mapping[str, int],
) -> dict[str, Any]:
    file_paths = bundle_file_paths(source)
    content_hash = hash_files(repo_root, file_paths)
    return {
        "name": source.name,
        "skill_path": relative_location(source.skill_md_path, repo_root),
        "scope": source.metadata.get("scope"),
        "status": source.metadata.get("status"),
        "invocation_mode": source.metadata.get("invocation_mode"),
        "skill_revision": content_hash[:12],
        "content_hash": content_hash,
        "technique_dependencies": list(source.metadata.get("technique_dependencies", [])),
        "lineage_state": lineage_entry["lineage_state"],
        "canonical_candidate_ready": public_entry["canonical_candidate_ready"],
        "canonical_eval_ready": evaluation_entry["canonical_eval_ready"],
        "promotion_review_path": public_entry["promotion_review_path"],
        "candidate_review_path": public_entry["candidate_review_path"],
        "support_artifacts": list(source.support_artifacts),
        "bundle_files": [relative_location(path, repo_root) for path in file_paths],
        "install_profiles": list(relationship_entry["install_profiles"]),
        "artifact_group_coverage": list(relationship_entry["artifact_group_coverage"]),
        "technique_lineage": list(relationship_entry["technique_lineage"]),
        "generated_surface_versions": dict(generated_surface_versions),
    }


def entry_by_name(
    payload: Mapping[str, Any],
    skill_name: str,
) -> Mapping[str, Any]:
    for entry in payload.get("skills", []):
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
            return entry
    raise KeyError(skill_name)


def build_bundle_index_payload(
    repo_root: Path,
    skill_names: Sequence[str],
    *,
    generated_surface_versions: Mapping[str, int],
) -> dict[str, Any]:
    sources = skill_source_model.load_skill_sources(repo_root, skill_names)
    public_payload = {
        "skills": [],
    }
    evaluation_payload = skill_evaluation_surface.build_evaluation_matrix_payload(
        repo_root,
        skill_names,
    )
    lineage_payload = skill_lineage_surface.build_lineage_surface_payload(
        repo_root,
        skill_names,
    )
    fixtures = skill_source_model.load_optional_yaml(
        repo_root / skill_governance_surface.PUBLIC_SURFACE_SOURCE_OF_TRUTH["evaluation_fixtures"]
    )
    coverage_by_skill = skill_governance_surface.collect_evaluation_coverage(fixtures)
    governance_signals = skill_governance_lane_contract.governance_skill_signals(
        skill_governance_lane_contract.load_governance_lanes(repo_root)
    )
    profiles_doc = json.loads(
        (repo_root / "config" / "skill_pack_profiles.json").read_text(encoding="utf-8")
    )
    relationship_layers = skill_relationship_contract.build_skill_relationship_layers(
        sources,
        profiles_doc=profiles_doc,
        artifact_groups=release_manifest_contract.ARTIFACT_GROUPS,
        support_resource_skill_names=sorted(build_support_resources.TARGETED_SKILLS),
    )
    public_entries: list[dict[str, Any]] = []
    for source in sources:
        techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
        public_entries.append(
            skill_governance_surface.derive_public_surface_skill_entry(
                skill_name=source.name,
                metadata=source.metadata,
                headings=set(source.sections),
                techniques=techniques,
                evaluation_coverage=skill_governance_surface.coverage_for_skill(
                    coverage_by_skill,
                    source.name,
                ),
                policy_exists=source.policy_exists,
                policy_allow_implicit_invocation=source.policy_allow_implicit_invocation,
                promotion_review_path=source.promotion_review_path,
                candidate_review_path=source.candidate_review_path,
                skill_path=relative_location(source.skill_md_path, repo_root),
                governance_signals=skill_governance_lane_contract.governance_signals_for_skill(
                    governance_signals,
                    source.name,
                ),
            )
        )
    public_payload = {"skills": public_entries}

    skills: list[dict[str, Any]] = []
    for source in sources:
        skills.append(
            bundle_entry(
                source,
                repo_root=repo_root,
                public_entry=entry_by_name(public_payload, source.name),
                evaluation_entry=entry_by_name(evaluation_payload, source.name),
                lineage_entry=entry_by_name(lineage_payload, source.name),
                relationship_entry=relationship_layers[source.name],
                generated_surface_versions=generated_surface_versions,
            )
        )

    return {
        "bundle_index_version": BUNDLE_INDEX_VERSION,
        "source_of_truth": BUNDLE_SOURCE_OF_TRUTH,
        "skills": skills,
    }


def render_bundle_index_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("bundle index field 'skills' must be a list")

    lines = [
        "# Skill bundle index",
        "",
        "This derived file summarizes deterministic bundle metadata for each committed skill.",
        "It is repo-local packaging metadata, not a release or registry surface.",
        "",
        "| name | revision | status | scope | invocation | candidate ready | eval ready | profiles | artifact groups | technique lineage |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    if not skill_entries:
        lines.append("| - | - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skill_entries:
            if not isinstance(entry, Mapping):
                continue
            technique_lineage = entry.get("technique_lineage", [])
            technique_summary = ", ".join(
                f"{item['id']} ({item['lineage_state']})"
                for item in technique_lineage
                if isinstance(item, Mapping)
            ) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["skill_revision"]),
                        str(entry["status"]),
                        str(entry["scope"]),
                        str(entry["invocation_mode"]),
                        "true" if entry["canonical_candidate_ready"] else "false",
                        "true" if entry["canonical_eval_ready"] else "false",
                        ", ".join(entry.get("install_profiles", [])) or "-",
                        ", ".join(entry.get("artifact_group_coverage", [])) or "-",
                        technique_summary,
                    ]
                )
                + " |"
            )
    lines.append("")
    return "\n".join(lines)


def graph_node_id(prefix: str, raw_value: str) -> str:
    safe = raw_value.replace("-", "_").replace(":", "_").replace("/", "_")
    return f"{prefix}_{safe}"


def build_skill_graph_payload(
    repo_root: Path,
    skill_names: Sequence[str],
    *,
    generated_surface_versions: Mapping[str, int],
) -> dict[str, Any]:
    bundle_index = build_bundle_index_payload(
        repo_root,
        skill_names,
        generated_surface_versions=generated_surface_versions,
    )
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    seen_nodes: set[tuple[str, str]] = set()

    def add_node(node_type: str, node_id: str, label: str) -> None:
        key = (node_type, node_id)
        if key in seen_nodes:
            return
        seen_nodes.add(key)
        nodes.append({"id": node_id, "type": node_type, "label": label})

    for entry in bundle_index["skills"]:
        skill_id = graph_node_id("skill", entry["name"])
        add_node("skill", skill_id, entry["name"])

        status_id = graph_node_id("status", entry["status"])
        add_node("status", status_id, f"status: {entry['status']}")
        edges.append({"source": skill_id, "target": status_id, "kind": "maturity"})

        scope_id = graph_node_id("scope", entry["scope"])
        add_node("scope", scope_id, f"scope: {entry['scope']}")
        edges.append({"source": skill_id, "target": scope_id, "kind": "scope"})

        lineage_id = graph_node_id("lineage", entry["lineage_state"])
        add_node("lineage", lineage_id, f"lineage: {entry['lineage_state']}")
        edges.append({"source": skill_id, "target": lineage_id, "kind": "lineage"})

        policy_id = graph_node_id("policy", entry["invocation_mode"])
        add_node("policy", policy_id, f"invocation: {entry['invocation_mode']}")
        edges.append({"source": skill_id, "target": policy_id, "kind": "invocation_policy"})

        for technique_id in entry.get("technique_dependencies", []):
            technique_node_id = graph_node_id("technique", str(technique_id))
            add_node("technique", technique_node_id, str(technique_id))
            edges.append(
                {
                    "source": skill_id,
                    "target": technique_node_id,
                    "kind": "depends_on",
                }
            )
        for profile_name in entry.get("install_profiles", []):
            profile_node_id = graph_node_id("profile", str(profile_name))
            add_node("profile", profile_node_id, f"profile: {profile_name}")
            edges.append(
                {
                    "source": skill_id,
                    "target": profile_node_id,
                    "kind": "included_in_profile",
                }
            )
        for artifact_group in entry.get("artifact_group_coverage", []):
            artifact_group_node_id = graph_node_id("artifact_group", str(artifact_group))
            add_node(
                "artifact_group",
                artifact_group_node_id,
                f"artifact group: {artifact_group}",
            )
            edges.append(
                {
                    "source": skill_id,
                    "target": artifact_group_node_id,
                    "kind": "available_in_artifact_group",
                }
            )

    return {
        "skill_graph_version": SKILL_GRAPH_VERSION,
        "source_of_truth": BUNDLE_SOURCE_OF_TRUTH,
        "nodes": nodes,
        "edges": edges,
        "skills": bundle_index["skills"],
    }


def render_skill_graph_markdown(payload: Mapping[str, Any]) -> str:
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])
    skill_entries = payload.get("skills", [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("skill graph nodes and edges must be lists")

    mermaid_lines = ["graph TD"]
    for node in nodes:
        if not isinstance(node, Mapping):
            continue
        mermaid_lines.append(f"  {node['id']}[\"{node['label']}\"]")
    for edge in edges:
        if not isinstance(edge, Mapping):
            continue
        mermaid_lines.append(
            f"  {edge['source']} -->|{edge['kind']}| {edge['target']}"
        )

    lines = [
        "# Skill graph",
        "",
        "This derived file summarizes maturity, lineage, scope, invocation, technique, profile, and artifact-group edges for the current skill surface.",
        "",
        "```mermaid",
        *mermaid_lines,
        "```",
        "",
        "| name | status | scope | invocation | lineage | profiles | artifact groups | techniques |",
        "|---|---|---|---|---|---|---|---|",
    ]
    if not isinstance(skill_entries, list) or not skill_entries:
        lines.append("| - | - | - | - | - | - | - | - |")
    else:
        for entry in skill_entries:
            if not isinstance(entry, Mapping):
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["status"]),
                        str(entry["scope"]),
                        str(entry["invocation_mode"]),
                        str(entry["lineage_state"]),
                        ", ".join(entry.get("install_profiles", [])) or "-",
                        ", ".join(entry.get("artifact_group_coverage", [])) or "-",
                        ", ".join(entry.get("technique_dependencies", [])) or "-",
                    ]
                )
                + " |"
            )
    lines.append("")
    return "\n".join(lines)
