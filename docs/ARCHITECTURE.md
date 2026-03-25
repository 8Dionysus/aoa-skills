# Architecture

## Purpose

`aoa-skills` is a public repository of reusable Codex skills.
It is the operational companion to `aoa-techniques`.
It is one bounded execution layer in the AoA ontology spine; see
`docs/LAYER_POSITION.md` for the repo-owned boundary note.

- `aoa-techniques` answers: what is the technique, when should it be used, what are its invariants, risks, and validation rules?
- `aoa-skills` answers: how should Codex apply techniques in a concrete agent workflow?

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
- invocation policy
- technique composition metadata

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
`generated/codex_config_snippets.json`, `generated/mcp_dependency_manifest.json`, and `generated/release_manifest.json`:
they are generated operational interfaces, not authored meaning.

A skill normally relies on several techniques and/or several bounded actions.
A single-technique skill is allowed only as an explicit reviewed exception.
A skill is not the home of recurring scenario method; that boundary stays in
`aoa-playbooks`.

## Layering

### Layer 1: origin project
A technique is born in a real project such as `atm10-agent` or `abyss-stack`.

### Layer 2: technique canon
The technique is sanitized, generalized, validated, and promoted into `aoa-techniques`.

### Layer 3: skill canon
A skill in `aoa-skills` references one or more techniques and composes them into
a Codex-usable workflow. The expected shape is a package, not a 1:1 mirror of
one technique.

### Layer 4: project overlay
A project-local overlay adds:
- repo paths
- commands
- source-of-truth files
- risk policies
- approval gates
- runtime assumptions

## Design rules

1. techniques are the source of truth for reusable practice
2. skills are allowed to summarize or compose techniques, but should not silently drift from them
3. recurring scenario method stays in `aoa-playbooks`, even when a skill is executable
4. runtime skill execution should not depend on live remote fetches
5. build-time composition is preferred over runtime remote dependency
6. project overlays should remain thin
7. dangerous or operationally sensitive skills should default to explicit invocation
8. a single-technique skill needs an explicit exception review that justifies the skill layer

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

## Versioning direction

A skill should eventually record:
- its own version or revision
- the technique IDs it depends on
- optionally the source technique commit or release reference used when the skill was generated or updated

That future versioning direction is separate from the current public-surface layer.
In the current pass, `aoa-skills` can publish repo-level GitHub releases and tags for bounded baseline cuts, but it still does not add explicit per-skill release metadata; derived public-product signals remain separate from release identity.
