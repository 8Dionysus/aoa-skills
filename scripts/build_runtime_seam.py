#!/usr/bin/env python3
"""Build wave-4 runtime seam artifacts for dedicated-tool skill activation.

This builder keeps the Codex-facing `.agents/skills/*` export as the common
surface and emits an additional runtime seam for local-friendly adapters that
prefer a dedicated tool flow over raw file reads.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
from typing import Any

import release_manifest_contract
import yaml

PROFILE = "codex-facing-wave-4-runtime-seam"
ROOT = ".agents/skills"
SESSION_FILE_HINT = ".aoa/skill-runtime-session.json"
JSON_INDENT = 2
RUNTIME_GENERATED_FILES = [
    "generated/runtime_discovery_index.json",
    "generated/runtime_discovery_index.min.json",
    "generated/runtime_disclosure_index.json",
    "generated/runtime_activation_aliases.json",
    "generated/runtime_tool_schemas.json",
    "generated/runtime_session_contract.json",
    "generated/runtime_prompt_blocks.json",
    "generated/runtime_router_hints.json",
    "generated/runtime_seam_manifest.json",
]


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line:
            items.append(json.loads(line))
    return items


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=JSON_INDENT, ensure_ascii=False) + "\n"


def parse_frontmatter(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter start")
    try:
        _, fm_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{path}: invalid frontmatter fence structure") from exc
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must parse to a mapping")
    return data, body


def parse_sections(body: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_heading: str | None = None
    buffer: list[str] = []
    for raw_line in body.splitlines():
        if raw_line.startswith("## "):
            if current_heading is not None:
                sections.append(
                    {
                        "heading": current_heading,
                        "content": "\n".join(buffer).strip(),
                    }
                )
            current_heading = raw_line[3:].strip()
            buffer = []
            continue
        if raw_line.startswith("# "):
            continue
        if current_heading is not None:
            buffer.append(raw_line)
    if current_heading is not None:
        sections.append({"heading": current_heading, "content": "\n".join(buffer).strip()})
    return sections


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def summarize_section(content: str, limit: int = 2, max_chars: int = 280) -> str:
    bullets: list[str] = []
    lines = [line.rstrip() for line in content.splitlines()]
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            bullets.append(normalize_space(line[2:]))
        else:
            match = re.match(r"^(\d+)\.\s+(.*)$", line)
            if match:
                bullets.append(normalize_space(match.group(2)))
    if bullets:
        text = "; ".join(bullets[:limit])
    else:
        text = normalize_space(" ".join(line.strip() for line in lines if line.strip()))
    if len(text) > max_chars:
        text = text[: max_chars - 3].rstrip() + "..."
    return text


def collect_keywords(name: str, description: str, headings: list[str], scope: str) -> list[str]:
    tokens = set()
    for chunk in [name.replace("-", " "), description, scope, *headings]:
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{2,}", chunk.lower()):
            if token in {"when", "with", "from", "that", "this", "then", "into", "they", "them", "your", "have", "need", "keep", "does", "used", "more", "than", "only"}:
                continue
            tokens.add(token)
    return sorted(tokens)


def collision_maps(collision_doc: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    family_by_skill: dict[str, dict[str, Any]] = {}
    for family in collision_doc.get("families", []):
        for skill_name in family.get("skills", []):
            family_by_skill[skill_name] = family
    competing: dict[str, list[str]] = {}
    for case in collision_doc.get("cases", []):
        skill_name = case["skill_name"]
        current = competing.setdefault(skill_name, [])
        for candidate in case.get("competing_skills", []):
            if candidate not in current:
                current.append(candidate)
    return family_by_skill, competing


def eval_examples_by_skill(eval_cases: list[dict[str, Any]]) -> dict[str, dict[str, list[str]]]:
    out: dict[str, dict[str, list[str]]] = {}
    for case in eval_cases:
        bucket = out.setdefault(
            case["skill_name"],
            {
                "explicit": [],
                "implicit": [],
                "negative": [],
                "manual": [],
            },
        )
        prompt = case["prompt"]
        expected = case["expected_behavior"]
        mode = case.get("mode")
        if mode == "explicit" and expected == "invoke-skill":
            bucket["explicit"].append(prompt)
        elif mode == "implicit" and expected == "invoke-skill":
            bucket["implicit"].append(prompt)
        elif expected == "manual-invocation-required":
            bucket["manual"].append(prompt)
        else:
            bucket["negative"].append(prompt)
    return out


def dedupe_prompts(prompts: list[str], *, exclude: set[str] | None = None, limit: int | None = None) -> list[str]:
    seen = set(exclude or ())
    out: list[str] = []
    for prompt in prompts:
        if prompt in seen:
            continue
        seen.add(prompt)
        out.append(prompt)
        if limit is not None and len(out) >= limit:
            break
    return out


def explicit_handles(name: str) -> dict[str, Any]:
    return {
        "codex": {
            "mention": f"${name}",
            "browser": "/skills",
        },
        "local_wrapper": {
            "slash_alias": f"/{name}",
            "tool_call": {
                "name": "activate_skill",
                "arguments": {"skill_name": name},
            },
        },
    }


def skill_display_markdown(name: str, description: str, short_description: str, trust_posture: str, mutation_surface: str) -> str:
    return (
        f"### {name}\n"
        f"- Summary: {short_description}\n"
        f"- Use when: {description}\n"
        f"- Trust posture: {trust_posture}\n"
        f"- Mutation surface: {mutation_surface}\n"
    )


def build_prompt_blocks(discovery_min: list[dict[str, Any]]) -> dict[str, Any]:
    lines_xml = ["<available_skills>"]
    lines_md = ["Available skills:"]
    for entry in discovery_min:
        lines_xml.extend(
            [
                "  <skill>",
                f"    <name>{entry['name']}</name>",
                f"    <description>{entry['description']}</description>",
                "  </skill>",
            ]
        )
        lines_md.append(f"- {entry['name']}: {entry['description']}")
    lines_xml.append("</available_skills>")

    behavior = [
        "The following skills provide specialized instructions for specific tasks.",
        "Use discover_skills when a task is underspecified and you need a short list of relevant candidates.",
        "Use disclose_skill when you want policy, resource, or verification preview without injecting the full skill instructions.",
        "When a task matches a skill's description, call activate_skill with the skill name to load the full instructions.",
        "Avoid activating the same skill repeatedly in one session unless you need to refresh its content.",
        "Treat activated skill content as protected during context compaction, and use compact_skill_session to emit a rehydration packet when the session grows long.",
    ]
    system_prompt_block = "\n".join([*behavior, "", *lines_xml])
    tool_description_block = "\n".join([
        "List or activate AoA skills that live in the shared .agents/skills export.",
        "Use discover_skills first when the task is fuzzy, disclose_skill for a preview, and activate_skill for full instructions.",
        "",
        *lines_md,
    ])
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "behavioral_instructions": behavior,
        "catalog_xml": "\n".join(lines_xml),
        "catalog_markdown": "\n".join(lines_md),
        "system_prompt_block": system_prompt_block,
        "tool_description_block": tool_description_block,
    }


def build_tool_schemas(skill_names: list[str], trust_postures: list[str], invocation_modes: list[str], mutation_surfaces: list[str]) -> dict[str, Any]:
    tool_defs = [
        {
            "name": "discover_skills",
            "description": "Shortlist AoA skills by name, description, trust posture, or invocation mode before activation.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Optional free-text query over skill name, description, or tags."},
                    "trust_posture": {"type": "string", "enum": trust_postures},
                    "invocation_mode": {"type": "string", "enum": invocation_modes},
                    "mutation_surface": {"type": "string", "enum": mutation_surfaces},
                    "allow_implicit_invocation": {"type": "boolean"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                },
                "additionalProperties": False,
            },
            "output_ref": "generated/runtime_discovery_index.json",
        },
        {
            "name": "disclose_skill",
            "description": "Preview a specific AoA skill without injecting the full instructions. Use for policy, resource, and verification preview.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "enum": skill_names},
                },
                "required": ["skill_name"],
                "additionalProperties": False,
            },
            "output_ref": "generated/runtime_disclosure_index.json",
        },
        {
            "name": "activate_skill",
            "description": "Load the full instructions for a specific AoA skill, wrapped with runtime metadata and bundled-resource inventory.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "enum": skill_names},
                    "session_file": {"type": "string", "description": "Optional path to a JSON session file that tracks active skills."},
                    "explicit_handle": {"type": "string", "description": "Optional handle that caused activation, such as $skill-name or /skills."},
                    "include_frontmatter": {"type": "boolean", "description": "Include parsed frontmatter alongside stripped instructions."},
                    "wrap_mode": {"type": "string", "enum": ["structured", "markdown", "raw"]},
                },
                "required": ["skill_name"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_seam.py activate",
        },
        {
            "name": "skill_session_status",
            "description": "Show which skills are currently active in the runtime session and whether they are protected from compaction.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "session_file": {"type": "string"},
                },
                "required": ["session_file"],
                "additionalProperties": False,
            },
            "output_ref": "generated/runtime_session_contract.json",
        },
        {
            "name": "deactivate_skill",
            "description": "Remove a skill from the current runtime session state without deleting the underlying skill files.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "enum": skill_names},
                    "session_file": {"type": "string"},
                },
                "required": ["skill_name", "session_file"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_seam.py deactivate",
        },
        {
            "name": "compact_skill_session",
            "description": "Emit a compaction packet that preserves the active skills' must-keep state and rehydration hints for long-running sessions.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "session_file": {"type": "string"},
                },
                "required": ["session_file"],
                "additionalProperties": False,
            },
            "output_ref": "scripts/skill_runtime_seam.py compact",
        },
    ]
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "tools": tool_defs,
    }


def build_session_contract() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "session_file_hint": SESSION_FILE_HINT,
        "description": "Session contract for the dedicated-tool runtime seam that sits downstream of the Codex-facing export.",
        "behaviors": [
            "deduplicate activations by skill name within one session",
            "mark activated skills as protected_from_compaction",
            "preserve must_keep items and retain_sections during compaction",
            "retain allowlist_paths so bundled resources remain readable without extra approval prompts",
        ],
        "state_schema": {
            "required": [
                "schema_version",
                "profile",
                "session_id",
                "created_at",
                "updated_at",
                "active_skills",
                "activation_log",
            ],
            "active_skill_record": {
                "required": [
                    "name",
                    "activated_at",
                    "activation_count",
                    "protected_from_compaction",
                    "allowlist_paths",
                    "compact_summary",
                    "must_keep",
                    "rehydration_hint",
                ]
            },
        },
        "compact_output": {
            "required": ["session_id", "active_skill_packets", "reactivation_instructions"],
        },
    }


def render_or_check(path: pathlib.Path, text: str, check: bool) -> None:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            raise SystemExit(f"runtime seam drift: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--check", action="store_true", help="Check generated files instead of writing them")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    generated_dir = repo_root / "generated"

    catalog = load_json(generated_dir / "agent_skill_catalog.json")
    runtime_contracts = load_json(generated_dir / "skill_runtime_contracts.json")
    context_retention = load_json(generated_dir / "context_retention_manifest.json")
    trust_policy = load_json(generated_dir / "trust_policy_matrix.json")
    eval_cases = load_jsonl(generated_dir / "skill_trigger_eval_cases.jsonl")
    collision_doc = load_json(generated_dir / "skill_trigger_collision_matrix.json")
    runtime_by_name = {entry["name"]: entry for entry in runtime_contracts.get("skills", [])}
    context_by_name = {entry["name"]: entry for entry in context_retention.get("skills", [])}
    trust_by_name = {entry["name"]: entry for entry in trust_policy.get("skills", [])}
    family_by_skill, competing_by_skill = collision_maps(collision_doc)
    evals_by_skill = eval_examples_by_skill(eval_cases)

    discovery_records: list[dict[str, Any]] = []
    disclosure_records: list[dict[str, Any]] = []
    alias_records: list[dict[str, Any]] = []
    router_records: list[dict[str, Any]] = []

    for entry in catalog.get("skills", []):
        skill_path = repo_root / entry["path"]
        skill_dir = skill_path.parent
        frontmatter, body = parse_frontmatter(skill_path)
        sections = parse_sections(body)
        section_map = {section["heading"]: section["content"] for section in sections}
        headings = [section["heading"] for section in sections]
        openai_path = repo_root / entry["openai_config_path"]
        openai_doc = yaml.safe_load(openai_path.read_text(encoding="utf-8")) or {}
        runtime_entry = runtime_by_name.get(entry["name"], {})
        context_entry = context_by_name.get(entry["name"], {})
        trust_entry = trust_by_name.get(entry["name"], {})
        family = family_by_skill.get(entry["name"], {})
        competing = competing_by_skill.get(entry["name"], [])
        eval_bucket = evals_by_skill.get(entry["name"], {"explicit": [], "implicit": [], "negative": [], "manual": []})
        handles = explicit_handles(entry["name"])
        keywords = collect_keywords(entry["name"], entry["description"], headings, entry["scope"])

        discovery_record = {
            "name": entry["name"],
            "display_name": entry["display_name"],
            "description": entry["description"],
            "short_description": entry["short_description"],
            "path": entry["path"],
            "trust_posture": entry["trust_posture"],
            "invocation_mode": entry["invocation_mode"],
            "allow_implicit_invocation": entry["allow_implicit_invocation"],
            "mutation_surface": entry["mutation_surface"],
            "recommended_install_scopes": entry.get("recommended_install_scopes", []),
            "explicit_handles": handles,
            "keywords": keywords,
            "disclose_tool": {"name": "disclose_skill", "arguments": {"skill_name": entry["name"]}},
            "activate_tool": {"name": "activate_skill", "arguments": {"skill_name": entry["name"]}},
        }
        discovery_records.append(discovery_record)

        disclosure_record = {
            "name": entry["name"],
            "display_name": entry["display_name"],
            "description": entry["description"],
            "short_description": entry["short_description"],
            "path": entry["path"],
            "skill_dir": str(skill_dir.relative_to(repo_root).as_posix()),
            "compatibility": frontmatter.get("compatibility"),
            "metadata": frontmatter.get("metadata", {}),
            "headings_available": headings,
            "section_summaries": {
                heading: summarize_section(content)
                for heading, content in section_map.items()
            },
            "resource_inventory": entry.get("resource_inventory", {}),
            "policy": openai_doc.get("policy", {}),
            "interface": openai_doc.get("interface", {}),
            "runtime_contract_ref": f"generated/skill_runtime_contracts.json#{entry['name']}",
            "context_retention_ref": f"generated/context_retention_manifest.json#{entry['name']}",
            "trust_policy_ref": f"generated/trust_policy_matrix.json#{entry['name']}",
            "collision_family": family.get("family"),
            "collision_notes": family.get("notes", []),
            "competing_skills": competing,
            "sample_prompts": {
                "explicit": eval_bucket["explicit"][:2],
                "implicit": eval_bucket["implicit"][:2],
                "manual_invocation_required": eval_bucket["manual"][:2],
                "negative": eval_bucket["negative"][:2],
            },
            "explicit_handles": handles,
            "disclose_card_markdown": skill_display_markdown(
                entry["name"],
                entry["description"],
                entry["short_description"],
                entry["trust_posture"],
                entry["mutation_surface"],
            ),
        }
        disclosure_records.append(disclosure_record)

        alias_records.append(
            {
                "name": entry["name"],
                "codex_mention": handles["codex"]["mention"],
                "codex_browser": handles["codex"]["browser"],
                "local_slash_alias": handles["local_wrapper"]["slash_alias"],
                "tool_call": handles["local_wrapper"]["tool_call"],
            }
        )

        router_should_trigger = dedupe_prompts(eval_bucket["implicit"], limit=3)
        router_manual = dedupe_prompts(
            eval_bucket["manual"],
            exclude=set(router_should_trigger),
            limit=3,
        )
        router_negative = dedupe_prompts(
            eval_bucket["negative"],
            exclude=set(router_should_trigger) | set(router_manual),
            limit=3,
        )
        router_records.append(
            {
                "name": entry["name"],
                "description": entry["description"],
                "collision_family": family.get("family"),
                "competing_skills": competing,
                "should_trigger": router_should_trigger,
                "manual_invocation_required": router_manual,
                "negative_controls": router_negative,
                "notes": family.get("notes", []),
            }
        )

    discovery_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "root": ROOT,
        "behavioral_instructions": [
            "When a task matches a skill description, call activate_skill with the skill name.",
            "Use discover_skills to shortlist candidates and disclose_skill for a preview before full activation.",
            "Hide disabled or unavailable skills from the discovery catalog.",
        ],
        "skills": discovery_records,
    }
    discovery_min_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "root": ROOT,
        "skills": [
            {
                "name": entry["name"],
                "description": entry["description"],
                "trust_posture": entry["trust_posture"],
                "invocation_mode": entry["invocation_mode"],
                "allow_implicit_invocation": entry["allow_implicit_invocation"],
            }
            for entry in discovery_records
        ],
    }
    disclosure_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "root": ROOT,
        "skills": disclosure_records,
    }
    aliases_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "aliases": alias_records,
    }
    router_doc = {
        "schema_version": 1,
        "profile": PROFILE,
        "skills": router_records,
    }
    prompt_blocks_doc = build_prompt_blocks(discovery_min_doc["skills"])
    tool_schemas_doc = build_tool_schemas(
        skill_names=[entry["name"] for entry in discovery_records],
        trust_postures=sorted({entry["trust_posture"] for entry in discovery_records}),
        invocation_modes=sorted({entry["invocation_mode"] for entry in discovery_records}),
        mutation_surfaces=sorted({entry["mutation_surface"] for entry in discovery_records}),
    )
    session_contract_doc = build_session_contract()
    runtime_seam_manifest = {
        "schema_version": 1,
        "profile": PROFILE,
        "common_surface": ROOT,
        "dedicated_tool_pattern": True,
        "tools": {
            "discover": "scripts/skill_runtime_seam.py discover",
            "disclose": "scripts/skill_runtime_seam.py disclose",
            "activate": "scripts/skill_runtime_seam.py activate",
            "status": "scripts/skill_runtime_seam.py status",
            "deactivate": "scripts/skill_runtime_seam.py deactivate",
            "compact": "scripts/skill_runtime_seam.py compact",
        },
        "generated": {
            "discovery_index": "generated/runtime_discovery_index.json",
            "discovery_index_min": "generated/runtime_discovery_index.min.json",
            "disclosure_index": "generated/runtime_disclosure_index.json",
            "aliases": "generated/runtime_activation_aliases.json",
            "tool_schemas": "generated/runtime_tool_schemas.json",
            "session_contract": "generated/runtime_session_contract.json",
            "prompt_blocks": "generated/runtime_prompt_blocks.json",
            "router_hints": "generated/runtime_router_hints.json",
        },
        "session_file_hint": SESSION_FILE_HINT,
        "backward_compatibility": {
            "legacy_activation_tool": "scripts/activate_skill.py",
        },
    }

    file_map = {
        generated_dir / "runtime_discovery_index.json": dump_json(discovery_doc),
        generated_dir / "runtime_discovery_index.min.json": dump_json(discovery_min_doc),
        generated_dir / "runtime_disclosure_index.json": dump_json(disclosure_doc),
        generated_dir / "runtime_activation_aliases.json": dump_json(aliases_doc),
        generated_dir / "runtime_tool_schemas.json": dump_json(tool_schemas_doc),
        generated_dir / "runtime_session_contract.json": dump_json(session_contract_doc),
        generated_dir / "runtime_prompt_blocks.json": dump_json(prompt_blocks_doc),
        generated_dir / "runtime_router_hints.json": dump_json(router_doc),
        generated_dir / "runtime_seam_manifest.json": dump_json(runtime_seam_manifest),
    }

    release_doc = release_manifest_contract.build_release_manifest(
        repo_root,
        file_overrides=file_map,
    )
    file_map[generated_dir / "release_manifest.json"] = dump_json(release_doc)

    for path, text in file_map.items():
        render_or_check(path, text, args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
