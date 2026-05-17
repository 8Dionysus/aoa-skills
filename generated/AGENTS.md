# AGENTS.md

## Applies to

This card applies to `generated/`.

## Role

`generated/` carries derived repository companions such as `skill_catalog.json`, matrices, route summaries, and release support outputs.

## Read before editing

Read root `AGENTS.md`, `DESIGN.AGENTS.md`, `generated/README.md`, and the builder that owns the file before touching this lane.

## Boundaries

Do not hand-author files in `generated/`. If a generated surface is wrong, change `skills/`, `config/`, schemas, templates, or the relevant builder. Generated files summarize source truth; they do not become source truth.

## Validation

Regenerate with the owning builder, commonly `python scripts/build_catalog.py`, then check freshness with `python scripts/build_catalog.py --check`. For broader generated movement, run `python scripts/release_check.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.

## Source Surfaces

Generated surfaces commonly derive from `skills/**/SKILL.md`,
`skills/**/techniques.yaml`, `docs/reviews/**`, `config/**`, schemas, templates,
and builders under `scripts/` or mechanic package `parts/`.

If any of these files change unexpectedly, inspect the owning source before
accepting the diff:

- `skill_catalog.json` and `skill_catalog.min.json`
- `skill_capsules.json`
- `skill_sections.full.json`
- `skill_walkthroughs.json` and `skill_walkthroughs.md`
- `skill_evaluation_matrix.json` and `skill_evaluation_matrix.md`
- `public_surface.json` and `public_surface.md`
- `governance_backlog.json` and `governance_backlog.md`
- `skill_bundle_index.json` and `skill_bundle_index.md`
- `skill_graph.json` and `skill_graph.md`
- `skill_boundary_matrix.json` and `skill_boundary_matrix.md`
- `skill_lineage_surface.json` and `skill_lineage_surface.md`
- `overlay_readiness.json` and `overlay_readiness.md`
- `skill_composition_audit.json` and `skill_composition_audit.md`
- `agent_skill_catalog.json` and `agent_skill_catalog.min.json`
- `portable_export_map.json`
- `local_adapter_manifest.json` and `local_adapter_manifest.min.json`
- trigger, description-trigger, runtime, support-resource, and Agon candidate
  outputs

## Hard No

Do not manually edit a generated file and stop there, delete generated files to
hide drift, sneak policy changes into derived output, or make
`requested_not_landed` candidate evidence look like accepted skill truth.
