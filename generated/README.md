# Generated District

`generated/` stores committed derived reader, catalog, governance, and export
surfaces built from authored sources elsewhere in the repository.

These files are useful evidence and public integration surfaces, but they are
not source truth. Change the owning skill, config, mechanic, schema, or builder,
then regenerate.

## Placement

| Surface kind | Home |
|---|---|
| Repo-wide catalog, matrix, export map, runtime manifest, or public read model | `generated/` |
| Mechanic-local generated companion that serves only one package or part | owning mechanic package |
| Skill bundle source or support artifact | `skills/<skill>/` |
| Example source object | owning `examples/` directory |

## Source Classes

| Class | Examples |
|---|---|
| Skill-derived | `skill_catalog*.json`, `skill_*_matrix.*`, `skill_graph.*` |
| Export-derived | `agent_skill_catalog*.json`, `portable_export_map.json`, `local_adapter_manifest*.json` |
| Governance-derived | `public_surface.*`, `governance_backlog.*`, `overlay_readiness.*` |
| Questbook-derived | `quest_catalog*.json`, `quest_dispatch*.json` |
| Mechanic-built root-published | Agon candidate indexes and runtime/readiness manifests that summarize repo-level source stores |

## Before Editing

1. Read `AGENTS.md`.
2. Find the source builder or authored input.
3. Regenerate with the named script.
4. Validate with the root release or generated-surface check.
