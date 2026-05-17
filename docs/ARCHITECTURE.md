# Architecture

## Purpose

`aoa-skills` is a public repository of reusable local coding-agent skills.
It is the operational companion to `aoa-techniques`.
It is one bounded execution layer in the AoA ontology spine; see
`mechanics/boundary-bridge/docs/LAYER_POSITION.md` for the repo-owned boundary note.
Root `DESIGN.md` describes the system form of that layer; this architecture
reference explains the technical model.

- `aoa-techniques` answers: what is the reusable practice, when should it be used, what are its invariants, risks, and validation rules?
- `aoa-skills` answers: what self-contained workflow should a local coding agent execute, and how does that workflow relate to reusable practice?

## Conceptual model

### Techniques

A technique is a minimal reproducible unit of engineering practice.
It is public-safe, documented, bounded, and validated.

### Skills

A skill is an agent-facing executable guidance bundle.
It packages:
- scoped instructions
- output expectations
- references
- optional scripts
- optional assets
- invocation policy
- technique composition metadata

The committed `SKILL.md` must stand on its own. Technique links can explain
lineage, composition, decomposition, refresh pressure, or future extraction, but
they are not runtime dependencies and should not become the only evidence that a
skill is mature.

The repository may also publish a generated Codex-facing export under `.agents/skills/*`.
That export is built from the canonical authored bundle plus portable export config,
and exists to make skill discovery and activation work cleanly in Codex-compatible runtimes.
It does not replace the authored bundle as the source of truth.

The repository may also publish derived reader surfaces in `generated/`.
Those surfaces are built from committed `SKILL.md`, `techniques.yaml`, review records, and evaluation fixtures and are meant to help routing, indexing, and public governance signaling without becoming a second source of truth.
The same derived posture now applies to `.agents/skills/*`, `generated/agent_skill_catalog*.json`,
`generated/portable_export_map.json`, `generated/local_adapter_manifest*.json`,
`generated/context_retention_manifest.json`, `generated/trust_policy_matrix.json`,
`generated/skill_runtime_contracts.json`, `generated/skill_pack_profiles.resolved.json`,
`generated/codex_config_snippets.json`, `generated/mcp_dependency_manifest.json`,
`generated/runtime_discovery_index*.json`, `generated/runtime_disclosure_index.json`,
`generated/runtime_activation_aliases.json`, `generated/runtime_tool_schemas.json`,
`generated/runtime_session_contract.json`, `generated/runtime_prompt_blocks.json`,
`generated/runtime_router_hints.json`, `generated/runtime_seam_manifest.json`,
`generated/skill_intelligence_registry*.json`,
`generated/deterministic_resource_manifest.json`, `generated/support_resource_index.json`,
`generated/structured_output_schema_index.json`, `generated/support_resource_bridge_map.json`,
`generated/expected_existing_aoa_support_dirs.json`, and `generated/release_manifest.json`:
they are generated operational interfaces, not authored meaning.

A skill normally relates to one or more techniques and/or several bounded
actions, but its identity is the bounded workflow it gives an agent. A
single-technique skill is allowed only as an explicit reviewed exception.
A skill is not the home of recurring scenario method; that boundary stays in
`aoa-playbooks`.

## Layering

### Layer 1: origin project
A technique is born in a real project such as `atm10-agent` or `abyss-stack`.

### Layer 2: technique canon
The technique is sanitized, generalized, validated, and promoted into `aoa-techniques`.

### Layer 3: skill canon
A skill in `aoa-skills` is a workflow usable by a local coding agent. It may be
assembled from techniques, and it may later be decomposed into techniques when
live execution reveals reusable practice. The bridge is bidirectional:

- techniques -> skill: compose reusable practices into an executable workflow
- skill -> techniques: extract stable practice from repeated execution

The expected shape is a workflow package, not a thin mirror of one technique.
Canonical source bundles live in the recursive `skills/` topology. The source
tree groups bundles by functional lane; the flat `.agents/skills/*` tree remains
the generated portable export.

### Layer 4: project overlay
A project-local overlay adds:
- repo paths
- commands
- source-of-truth files
- risk policies
- approval gates
- runtime assumptions

## Design rules

1. skills are self-contained execution objects
2. techniques are the source of truth for reusable practice
3. technique links are adjacent bridge evidence, not live runtime dependencies
4. skills may compose techniques into workflows, and mature skill workflows may
   produce technique extraction requests
5. skills should not silently rewrite technique canon when they claim a technique bridge
6. recurring scenario method stays in `aoa-playbooks`, even when a skill is executable
7. runtime skill execution should not depend on live remote fetches
8. build-time composition is preferred over runtime remote dependency
9. project overlays should remain thin
10. dangerous or operationally sensitive skills should default to explicit invocation
11. a single-technique skill needs an explicit exception review that justifies the skill layer

## Skill categories

### Core skills
Reusable across many repositories.
Examples:
- change protocol
- TDD slice
- contract-test design
- bounded-context mapping

### Project skills
Reusable inside one project family.
Examples:
- `atm10-*`
- `abyss-*`

### Risk skills
Operational or destructive workflows that should require explicit invocation and strong guardrails.

## Build philosophy

Skills should be reviewable artifacts.
They can be generated or assembled from technique references, but the committed `SKILL.md` should remain understandable to a human reviewer without additional hidden state.
Derived catalogs should stay deterministic and disposable: if a reader surface drifts, regenerate it from the authoritative markdown and manifest inputs.
The current repo-local governance and release signaling layer should also stay derived rather than introducing a second explicit skill-metadata contract.
The Codex-facing portable layer follows the same rule: `.agents/skills/*` is a generated export,
`config/portable_skill_overrides.json`, `config/openai_skill_extensions.json`, `config/skill_pack_profiles.json`, and `config/skill_policy_matrix.json` are the repo-owned configuration seams for that export, and local-friendly runtimes should wrap the export rather than inventing a second canonical skill format.
The runtime seam follows that same layer contract: `scripts/skill_runtime_seam.py` is the primary runtime path, while `scripts/activate_skill.py` remains the compatibility shim.
The support-resource layer follows the same repo-owned posture with deterministic support bundles under canonical skill roots; `scripts/build_support_resources.py` records those resources and their bridge back to AoA-native support dirs without becoming a second portable-sync authority.
The Skill Intelligence registry is also derived: `generated/skill_intelligence_registry*.json` and `scripts/skill_intelligence.py` provide portable lexical search, explanation, and status checks over canonical skill sources and generated evidence. They do not create a semantic backend, auto-promote skill status, or replace the authored `SKILL.md` bundles.

## Versioning direction

A skill should eventually record:
- its own version or revision
- the technique IDs it depends on
- optionally the source technique commit or release reference used when the skill was generated or updated

That future versioning direction is separate from the current public-surface layer.
In the current pass, `aoa-skills` can publish repo-level GitHub releases and tags for bounded baseline cuts, but it still does not add explicit per-skill release metadata; derived public-product signals remain separate from release identity.
