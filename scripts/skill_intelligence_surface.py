from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_source_model


SKILL_INTELLIGENCE_VERSION = 1
SKILL_INTELLIGENCE_PROFILE = "skill-intelligence-registry-v1"
SKILL_INTELLIGENCE_JSON_PATH = Path("generated") / "skill_intelligence_registry.json"
SKILL_INTELLIGENCE_MIN_JSON_PATH = Path("generated") / "skill_intelligence_registry.min.json"
SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/**/SKILL.md",
    "technique_manifest": "skills/**/techniques.yaml",
    "bundle_support_artifacts": "skills/**/{checks,examples,references,scripts,assets}/**/*",
    "policy_matrix": "config/skill_policy_matrix.json",
    "generated_inputs": [
        "generated/skill_bundle_index.json",
        "generated/runtime_discovery_index.min.json",
        "generated/trust_policy_matrix.json",
        "generated/tiny_router_capsules.min.json",
        "generated/support_resource_index.json",
        "generated/skill_graph.json",
        "generated/skill_boundary_matrix.json",
        "generated/skill_evaluation_matrix.json",
    ],
}
SECTION_ROLES = {
    "intent": "intent",
    "trigger_boundary": "trigger_boundary",
    "inputs": "inputs",
    "outputs": "outputs",
    "procedure": "procedure",
    "contracts": "contracts",
    "risks_and_anti_patterns": "risk",
    "verification": "verification",
    "technique_traceability": "lineage",
    "adaptation_points": "adaptation",
}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "when",
    "with",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return load_json(path)


def dump_json(data: Any, *, indent: int | None) -> str:
    return json.dumps(data, indent=indent, ensure_ascii=False) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_key(text: str) -> str:
    normalized = text.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    return normalized.strip("_")


def normalize_query_tokens(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9_-]*", text.lower())
    return [token.replace("-", " ") for token in tokens if len(token) > 2 and token not in STOPWORDS]


def by_name(payload: Mapping[str, Any], collection: str = "skills") -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    for entry in payload.get(collection, []):
        if isinstance(entry, Mapping) and isinstance(entry.get("name"), str):
            out[entry["name"]] = entry
    return out


def technique_manifest_ids(source: skill_source_model.SkillSource) -> list[str]:
    technique_ids: list[str] = []
    techniques = source.manifest.get("techniques", [])
    if not isinstance(techniques, list):
        return technique_ids
    for technique in techniques:
        if isinstance(technique, Mapping) and isinstance(technique.get("id"), str):
            technique_ids.append(technique["id"])
    return technique_ids


def load_policy_matrix_entries(repo_root: Path) -> dict[str, Mapping[str, Any]]:
    payload = load_optional_json(repo_root / "config" / "skill_policy_matrix.json")
    skills = payload.get("skills")
    if not isinstance(skills, Mapping):
        return {}
    return {
        skill_name: entry
        for skill_name, entry in skills.items()
        if isinstance(skill_name, str) and isinstance(entry, Mapping)
    }


def fallback_implicit_activation_policy(
    source: skill_source_model.SkillSource,
    policy_entry: Mapping[str, Any] | None,
) -> str:
    if isinstance(policy_entry, Mapping):
        policy_value = policy_entry.get("implicit_activation_policy")
        if policy_value in {"invoke", "suggest", "manual"}:
            return str(policy_value)

    explicit_policy = source.policy_allow_implicit_invocation
    if explicit_policy is True:
        return "invoke"
    if explicit_policy is False:
        return "manual"

    invocation_mode = source.metadata.get("invocation_mode")
    if invocation_mode == "explicit-preferred":
        return "suggest"
    return "manual"


def default_trust_entry(
    source: skill_source_model.SkillSource,
    policy_entry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    implicit_policy = fallback_implicit_activation_policy(source, policy_entry)
    return {
        "invocation_mode": source.metadata.get("invocation_mode"),
        "implicit_activation_policy": implicit_policy,
        "trust_posture": (
            str(policy_entry.get("trust_posture"))
            if isinstance(policy_entry, Mapping) and policy_entry.get("trust_posture")
            else "source-derived-fallback"
        ),
        "mutation_surface": (
            str(policy_entry.get("mutation_surface"))
            if isinstance(policy_entry, Mapping) and policy_entry.get("mutation_surface")
            else "none"
        ),
        "requires_manual_invocation": implicit_policy != "invoke",
        "candidate_only": implicit_policy == "suggest",
        "requires_confirmation_seam": bool(
            policy_entry.get("requires_confirmation_seam")
        )
        if isinstance(policy_entry, Mapping)
        else False,
    }


def default_bundle_entry(source: skill_source_model.SkillSource) -> dict[str, Any]:
    skill_text = source.skill_md_path.read_text(encoding="utf-8")
    content_hash = sha256_text(skill_text)
    technique_dependencies = source.metadata.get("technique_dependencies")
    if not isinstance(technique_dependencies, list):
        technique_dependencies = technique_manifest_ids(source)
    return {
        "content_hash": content_hash,
        "skill_revision": content_hash[:12],
        "support_artifacts": source.support_artifacts,
        "technique_dependencies": technique_dependencies,
        "technique_lineage": [],
        "lineage_state": "source-derived-fallback",
        "install_profiles": [],
        "artifact_group_coverage": [],
    }


def default_runtime_entry(
    source: skill_source_model.SkillSource,
    trust_entry: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "description": source.metadata.get("summary"),
        "allow_implicit_invocation": trust_entry.get("implicit_activation_policy") == "invoke",
    }


def graph_refs_for_skill(graph_payload: Mapping[str, Any], skill_name: str) -> dict[str, Any]:
    node_id = f"skill_{skill_name.replace('-', '_')}"
    outgoing: dict[str, int] = defaultdict(int)
    incoming: dict[str, int] = defaultdict(int)
    for edge in graph_payload.get("edges", []):
        if not isinstance(edge, Mapping):
            continue
        kind = edge.get("kind")
        if not isinstance(kind, str):
            continue
        if edge.get("source") == node_id:
            outgoing[kind] += 1
        if edge.get("target") == node_id:
            incoming[kind] += 1
    return {
        "node_id": node_id,
        "outgoing_edge_count": sum(outgoing.values()),
        "incoming_edge_count": sum(incoming.values()),
        "outgoing_edge_kinds": dict(sorted(outgoing.items())),
        "incoming_edge_kinds": dict(sorted(incoming.items())),
    }


def support_resource_entry(
    support_by_name: Mapping[str, Mapping[str, Any]],
    skill_name: str,
) -> dict[str, Any]:
    entry = support_by_name.get(skill_name)
    if not entry:
        return {
            "targeted": False,
            "standard_dir_counts": {},
            "legacy_dir_counts": {},
        }
    return {
        "targeted": bool(entry.get("targeted")),
        "standard_dir_counts": dict(entry.get("standard_dir_counts", {})),
        "legacy_dir_counts": dict(entry.get("legacy_dir_counts", {})),
    }


def section_search_docs(
    source: skill_source_model.SkillSource,
    *,
    repo_root: Path,
) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    summary = str(source.metadata.get("summary", "")).strip()
    if summary:
        docs.append(
            search_doc(
                source.name,
                "summary",
                source.skill_md_path,
                "frontmatter.summary",
                summary,
                repo_root=repo_root,
            )
        )
    for heading, content in source.sections.items():
        key = normalize_key(heading)
        role = SECTION_ROLES.get(key, key)
        docs.append(
            search_doc(
                source.name,
                role,
                source.skill_md_path,
                f"## {heading}",
                content,
                repo_root=repo_root,
            )
        )
    return docs


def search_doc(
    skill_name: str,
    section_role: str,
    path: Path,
    anchor: str,
    text: str,
    *,
    repo_root: Path,
) -> dict[str, Any]:
    doc_id = f"skill:{skill_name}:section:{section_role}"
    source_path = skill_source_model.relative_location(path, repo_root)
    normalized_text = re.sub(r"\s+", " ", text).strip()
    return {
        "doc_id": doc_id,
        "skill_name": skill_name,
        "section_role": section_role,
        "source_path": source_path,
        "source_anchor": anchor,
        "text": normalized_text,
        "text_sha256": sha256_text(normalized_text),
        "token_count": len(normalized_text.split()),
    }


def build_skill_entry(
    source: skill_source_model.SkillSource,
    *,
    repo_root: Path,
    bundle_entry: Mapping[str, Any],
    runtime_entry: Mapping[str, Any],
    trust_entry: Mapping[str, Any],
    tiny_entry: Mapping[str, Any],
    support_entry: Mapping[str, Any],
    graph_entry: Mapping[str, Any],
    boundary_entry: Mapping[str, Any],
    evaluation_entry: Mapping[str, Any],
) -> dict[str, Any]:
    content_hash = str(bundle_entry.get("content_hash") or "")
    repo_export_path = f".agents/skills/{source.name}/SKILL.md"
    repo_export_present = (repo_root / repo_export_path).is_file()
    search_documents = section_search_docs(source, repo_root=repo_root)
    return {
        "name": source.name,
        "scope": source.metadata.get("scope"),
        "status": source.metadata.get("status"),
        "summary": source.metadata.get("summary"),
        "source": {
            "skill_path": skill_source_model.relative_location(source.skill_md_path, repo_root),
            "techniques_path": skill_source_model.relative_location(source.techniques_path, repo_root),
            "policy_path": skill_source_model.relative_location(source.policy_path, repo_root)
            if source.policy_path.is_file()
            else None,
            "content_hash": content_hash,
            "skill_revision": bundle_entry.get("skill_revision"),
        },
        "policy": {
            "invocation_mode": trust_entry.get("invocation_mode") or source.metadata.get("invocation_mode"),
            "implicit_activation_policy": trust_entry.get("implicit_activation_policy"),
            "trust_posture": trust_entry.get("trust_posture"),
            "mutation_surface": trust_entry.get("mutation_surface"),
            "requires_manual_invocation": bool(trust_entry.get("requires_manual_invocation")),
            "candidate_only": bool(trust_entry.get("candidate_only")),
            "requires_confirmation_seam": bool(trust_entry.get("requires_confirmation_seam")),
        },
        "runtime": {
            "description": runtime_entry.get("description"),
            "allow_implicit_invocation": bool(runtime_entry.get("allow_implicit_invocation")),
        },
        "tiny_router": {
            "band": tiny_entry.get("band"),
            "cue_phrases": list(tiny_entry.get("cue_phrases", [])),
            "negative_phrases": list(tiny_entry.get("negative_phrases", [])),
            "companions": list(tiny_entry.get("companions", [])),
        },
        "resources": {
            "bundle_support_artifacts": list(bundle_entry.get("support_artifacts", [])),
            "support_resource_index": dict(support_entry),
            "selected_runtime_artifact_path": source.selected_runtime_artifact_path,
        },
        "lineage": {
            "technique_dependencies": list(bundle_entry.get("technique_dependencies", [])),
            "technique_lineage": list(bundle_entry.get("technique_lineage", [])),
            "lineage_state": bundle_entry.get("lineage_state"),
        },
        "boundaries": {
            "adjacent_skill_names": list(boundary_entry.get("adjacent_skill_names", [])),
            "adjacency_ready": bool(boundary_entry.get("adjacency_ready", False)),
            "adjacency_blockers": list(boundary_entry.get("adjacency_blockers", [])),
        },
        "evaluation": {
            "canonical_eval_ready": bool(evaluation_entry.get("canonical_eval_ready", False)),
            "canonical_eval_blockers": list(evaluation_entry.get("canonical_eval_blockers", [])),
            "use_case_count": int(evaluation_entry.get("use_case_count", 0)),
            "do_not_use_case_count": int(evaluation_entry.get("do_not_use_case_count", 0)),
            "autonomy_check_count": int(evaluation_entry.get("autonomy_check_count", 0)),
            "promotion_review_path": evaluation_entry.get("promotion_review_path"),
            "candidate_review_path": evaluation_entry.get("candidate_review_path"),
        },
        "graph_refs": dict(graph_entry),
        "install_refs": {
            "repo_export_path": repo_export_path,
            "repo_export_present": repo_export_present,
            "install_profiles": list(bundle_entry.get("install_profiles", [])),
            "artifact_group_coverage": list(bundle_entry.get("artifact_group_coverage", [])),
        },
        "search_documents": search_documents,
    }


def build_skill_intelligence_registry_payload(repo_root: Path) -> dict[str, Any]:
    skill_names = skill_source_model.discover_skill_names(repo_root)
    sources = skill_source_model.load_skill_sources(repo_root, skill_names)
    generated_dir = repo_root / "generated"
    bundle_by_name = by_name(load_optional_json(generated_dir / "skill_bundle_index.json"))
    runtime_by_name = by_name(load_optional_json(generated_dir / "runtime_discovery_index.min.json"))
    trust_by_name = by_name(load_optional_json(generated_dir / "trust_policy_matrix.json"))
    policy_matrix_by_name = load_policy_matrix_entries(repo_root)
    tiny_by_name = by_name(load_optional_json(generated_dir / "tiny_router_capsules.min.json"))
    support_by_name = by_name(load_optional_json(generated_dir / "support_resource_index.json"))
    graph_payload = load_optional_json(generated_dir / "skill_graph.json")
    boundary_by_name = by_name(load_optional_json(generated_dir / "skill_boundary_matrix.json"))
    evaluation_by_name = by_name(load_optional_json(generated_dir / "skill_evaluation_matrix.json"))

    skills: list[dict[str, Any]] = []
    for source in sources:
        trust_entry = trust_by_name.get(
            source.name,
            default_trust_entry(source, policy_matrix_by_name.get(source.name)),
        )
        skills.append(
            build_skill_entry(
                source,
                repo_root=repo_root,
                bundle_entry=bundle_by_name.get(source.name, default_bundle_entry(source)),
                runtime_entry=runtime_by_name.get(
                    source.name,
                    default_runtime_entry(source, trust_entry),
                ),
                trust_entry=trust_entry,
                tiny_entry=tiny_by_name.get(source.name, {}),
                support_entry=support_resource_entry(support_by_name, source.name),
                graph_entry=graph_refs_for_skill(graph_payload, source.name),
                boundary_entry=boundary_by_name.get(source.name, {}),
                evaluation_entry=evaluation_by_name.get(source.name, {}),
            )
        )

    return {
        "skill_intelligence_registry_version": SKILL_INTELLIGENCE_VERSION,
        "profile": SKILL_INTELLIGENCE_PROFILE,
        "owner_repo": "aoa-skills",
        "source_of_truth": SOURCE_OF_TRUTH,
        "skills": skills,
    }


def build_min_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    min_skills: list[dict[str, Any]] = []
    for entry in payload.get("skills", []):
        if not isinstance(entry, Mapping):
            continue
        min_skills.append(
            {
                "name": entry["name"],
                "scope": entry["scope"],
                "status": entry["status"],
                "summary": entry.get("summary"),
                "source": entry["source"],
                "policy": entry["policy"],
                "runtime": entry["runtime"],
                "tiny_router": {
                    "band": entry["tiny_router"].get("band"),
                    "companions": entry["tiny_router"].get("companions", []),
                },
                "resources": {
                    "support_artifact_count": len(
                        entry["resources"].get("bundle_support_artifacts", [])
                    ),
                    "selected_runtime_artifact_path": entry["resources"].get(
                        "selected_runtime_artifact_path"
                    ),
                },
                "lineage": {
                    "technique_dependencies": entry["lineage"].get(
                        "technique_dependencies",
                        [],
                    ),
                    "lineage_state": entry["lineage"].get("lineage_state"),
                },
                "boundaries": entry["boundaries"],
                "evaluation": entry["evaluation"],
                "graph_refs": entry["graph_refs"],
                "install_refs": entry["install_refs"],
                "search_document_refs": [
                    {
                        "doc_id": doc["doc_id"],
                        "section_role": doc["section_role"],
                        "source_path": doc["source_path"],
                        "source_anchor": doc["source_anchor"],
                        "text_sha256": doc["text_sha256"],
                        "token_count": doc["token_count"],
                    }
                    for doc in entry.get("search_documents", [])
                    if isinstance(doc, Mapping)
                ],
            }
        )
    return {
        "skill_intelligence_registry_version": payload["skill_intelligence_registry_version"],
        "profile": payload["profile"],
        "owner_repo": payload["owner_repo"],
        "source_of_truth": payload["source_of_truth"],
        "skills": min_skills,
    }


def build_skill_intelligence_texts(repo_root: Path) -> dict[Path, str]:
    payload = build_skill_intelligence_registry_payload(repo_root)
    return {
        SKILL_INTELLIGENCE_JSON_PATH: dump_json(payload, indent=2),
        SKILL_INTELLIGENCE_MIN_JSON_PATH: dump_json(build_min_payload(payload), indent=None),
    }


def activation_class(skill_entry: Mapping[str, Any]) -> str:
    policy = skill_entry.get("policy", {})
    if not isinstance(policy, Mapping):
        return "manual"
    implicit_policy = policy.get("implicit_activation_policy")
    if implicit_policy == "invoke":
        return "invoke"
    if implicit_policy == "suggest":
        return "suggest"
    return "manual"


def search_documents(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    for skill in payload.get("skills", []):
        if not isinstance(skill, Mapping):
            continue
        for doc in skill.get("search_documents", []):
            if isinstance(doc, Mapping):
                docs.append(dict(doc))
    return docs


def _fts_query(query: str) -> str:
    tokens = normalize_query_tokens(query)
    if not tokens:
        return ""
    return " OR ".join(f'"{token}"' for token in tokens)


def skill_passes_search_filters(
    skill: Mapping[str, Any],
    *,
    scope: str | None,
    status: str | None,
    invocation_policy: str | None,
    mutation_surface: str | None,
) -> bool:
    if scope and skill.get("scope") != scope:
        return False
    if status and skill.get("status") != status:
        return False
    policy = skill.get("policy", {})
    if not isinstance(policy, Mapping):
        policy = {}
    if invocation_policy and policy.get("implicit_activation_policy") != invocation_policy:
        return False
    if mutation_surface and policy.get("mutation_surface") != mutation_surface:
        return False
    return True


def sqlite_search(
    payload: Mapping[str, Any],
    query: str,
    *,
    limit: int = 8,
    scope: str | None = None,
    status: str | None = None,
    invocation_policy: str | None = None,
    mutation_surface: str | None = None,
) -> list[dict[str, Any]]:
    skill_map = {
        entry["name"]: entry
        for entry in payload.get("skills", [])
        if isinstance(entry, Mapping) and isinstance(entry.get("name"), str)
    }
    docs = search_documents(payload)
    fts_query = _fts_query(query)
    if not fts_query:
        return []

    query_tokens = [token.replace(" ", "-") for token in normalize_query_tokens(query)]
    filtered_docs = [
        doc
        for doc in docs
        if skill_passes_search_filters(
            skill_map.get(str(doc.get("skill_name")), {}),
            scope=scope,
            status=status,
            invocation_policy=invocation_policy,
            mutation_surface=mutation_surface,
        )
    ]
    rows: list[tuple[str, str, str, str, str, float]] = []
    con: sqlite3.Connection | None = None
    try:
        con = sqlite3.connect(":memory:")
        con.execute(
            "CREATE VIRTUAL TABLE docs USING fts5(doc_id, skill_name UNINDEXED, section_role UNINDEXED, source_path UNINDEXED, text)"
        )
        con.executemany(
            "INSERT INTO docs(doc_id, skill_name, section_role, source_path, text) VALUES (?, ?, ?, ?, ?)",
            [
                (
                    doc["doc_id"],
                    doc["skill_name"],
                    doc["section_role"],
                    doc["source_path"],
                    doc["text"],
                )
                for doc in filtered_docs
            ],
        )
        rows = [
            (doc_id, skill_name, section_role, source_path, text, score)
            for doc_id, skill_name, section_role, source_path, text, score in con.execute(
                "SELECT doc_id, skill_name, section_role, source_path, text, bm25(docs) AS score FROM docs WHERE docs MATCH ? ORDER BY score LIMIT 120",
                (fts_query,),
            )
        ]
    except sqlite3.Error:
        rows = fallback_search_rows(filtered_docs, query)
    finally:
        if con is not None:
            con.close()

    grouped: dict[str, dict[str, Any]] = {}
    for doc_id, skill_name, section_role, source_path, text, score in rows:
        skill = skill_map.get(skill_name)
        if not skill:
            continue

        item = grouped.setdefault(
            skill_name,
            {
                "name": skill_name,
                "score": 0.0,
                "candidate_class": activation_class(skill),
                "policy": skill.get("policy", {}),
                "matches": [],
            },
        )
        item["score"] += document_match_score(
            skill,
            text,
            section_role,
            query_tokens,
            fts_score=float(score),
        )
        item["matches"].append(
            {
                "doc_id": doc_id,
                "section_role": section_role,
                "source_path": source_path,
            }
        )

    ranked = sorted(
        grouped.values(),
        key=lambda item: (-float(item["score"]), item["name"]),
    )
    return ranked[:limit]


def document_match_score(
    skill: Mapping[str, Any],
    text: str,
    section_role: str,
    query_tokens: Sequence[str],
    *,
    fts_score: float,
) -> float:
    text_lc = text.lower()
    skill_name = str(skill.get("name", "")).replace("-", " ").lower()
    role_weight = {
        "summary": 2.0,
        "intent": 2.0,
        "trigger_boundary": 2.2,
        "inputs": 1.0,
        "outputs": 1.0,
        "procedure": 1.0,
        "risk": 1.2,
        "verification": 1.1,
        "lineage": 0.7,
        "adaptation": 0.7,
    }.get(section_role, 1.0)
    score = 0.0
    for token in query_tokens:
        token_text = token.replace("-", " ")
        if token in text_lc or token_text in text_lc:
            score += role_weight
        if token in skill_name or token_text in skill_name:
            score += 2.5
    fts_strength = abs(fts_score)
    score += fts_strength / (1.0 + fts_strength)
    if skill.get("scope") == "core":
        score += 0.5
    if skill.get("scope") == "project":
        score -= 0.3
    return score


def fallback_search_rows(
    docs: Sequence[Mapping[str, Any]],
    query: str,
) -> list[tuple[str, str, str, str, str, float]]:
    tokens = normalize_query_tokens(query)
    rows: list[tuple[str, str, str, str, str, float]] = []
    for doc in docs:
        text = str(doc.get("text", "")).lower()
        text_with_spaces = text.replace("-", " ")
        score = sum(
            1
            for token in tokens
            if token in text_with_spaces or token.replace(" ", "-") in text
        )
        if score:
            rows.append(
                (
                    str(doc["doc_id"]),
                    str(doc["skill_name"]),
                    str(doc["section_role"]),
                    str(doc["source_path"]),
                    str(doc["text"]),
                    -float(score),
                )
            )
    return sorted(rows, key=lambda row: (row[5], row[4]))[:80]


def explain_candidate(
    payload: Mapping[str, Any],
    skill_name: str,
    *,
    intent: str = "",
    limit: int = 5,
) -> dict[str, Any]:
    skill_map = {
        entry["name"]: entry
        for entry in payload.get("skills", [])
        if isinstance(entry, Mapping) and isinstance(entry.get("name"), str)
    }
    if skill_name not in skill_map:
        raise KeyError(skill_name)
    skill = skill_map[skill_name]
    candidate_payload = {
        key: value
        for key, value in payload.items()
        if key != "skills"
    }
    candidate_payload["skills"] = [skill]
    hits = sqlite_search(candidate_payload, intent or skill_name, limit=1)
    return {
        "intent": intent,
        "candidate": skill_name,
        "candidate_class": activation_class(skill),
        "policy": skill.get("policy", {}),
        "source": skill.get("source", {}),
        "positive_evidence": (hits[0]["matches"][:limit] if hits else []),
        "negative_or_boundary_evidence": {
            "adjacent_skill_names": skill.get("boundaries", {}).get("adjacent_skill_names", []),
            "negative_phrases": skill.get("tiny_router", {}).get("negative_phrases", []),
            "adjacency_blockers": skill.get("boundaries", {}).get("adjacency_blockers", []),
        },
        "next_load_refs": [
            skill.get("source", {}).get("skill_path"),
            skill.get("source", {}).get("techniques_path"),
            skill.get("resources", {}).get("selected_runtime_artifact_path"),
        ],
        "freshness": {
            "repo_export_present": skill.get("install_refs", {}).get("repo_export_present"),
            "content_hash": skill.get("source", {}).get("content_hash"),
        },
    }


def registry_status(
    repo_root: Path,
    payload: Mapping[str, Any],
    *,
    workspace_root: Path | None = None,
) -> dict[str, Any]:
    expected_texts = build_skill_intelligence_texts(repo_root)
    registry_path = repo_root / SKILL_INTELLIGENCE_JSON_PATH
    min_registry_path = repo_root / SKILL_INTELLIGENCE_MIN_JSON_PATH
    skills = [entry for entry in payload.get("skills", []) if isinstance(entry, Mapping)]
    repo_export_present = sum(
        1
        for entry in skills
        if entry.get("install_refs", {}).get("repo_export_present") is True
    )
    workspace_present = None
    if workspace_root is not None:
        workspace_skill_root = workspace_root / ".agents" / "skills"
        workspace_present = sum(
            1
            for entry in skills
            if (workspace_skill_root / str(entry.get("name")) / "SKILL.md").is_file()
        )
    return {
        "profile": payload.get("profile"),
        "skill_count": len(skills),
        "registry_current": registry_path.is_file()
        and registry_path.read_text(encoding="utf-8")
        == expected_texts[SKILL_INTELLIGENCE_JSON_PATH],
        "min_registry_current": min_registry_path.is_file()
        and min_registry_path.read_text(encoding="utf-8")
        == expected_texts[SKILL_INTELLIGENCE_MIN_JSON_PATH],
        "repo_export_skill_count": repo_export_present,
        "workspace_install_skill_count": workspace_present,
    }
