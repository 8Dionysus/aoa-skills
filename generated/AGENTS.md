# AGENTS.md

Guidance for coding agents and humans working under `generated/`.

## Purpose

`generated/` stores committed derived reader and governance surfaces built from authored sources elsewhere in the repository. These files are useful, public, and reviewable, but they are not the primary source of truth.

The main source-owned meaning still lives in authored inputs such as `skills/*/SKILL.md`, `skills/*/techniques.yaml`, committed review docs, and evaluation fixtures.

## Read this first

Before touching anything in `generated/`, read in this order:

1. `../AGENTS.md`
2. `../README.md`
3. `../docs/RUNTIME_PATH.md`
4. `../docs/EVALUATION_PATH.md`
5. `../docs/PUBLIC_SURFACE.md`
6. the generator entrypoint in `../scripts/build_catalog.py`
7. the authored source surface that actually owns the meaning you are trying to change

## Directory contract

This directory contains derived surfaces such as:

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
- `agon_skill_binding_candidates.min.json`
- `agent_skill_catalog.json` and `agent_skill_catalog.min.json`
- `portable_export_map.json`
- `local_adapter_manifest.json` and `local_adapter_manifest.min.json`
- `skill_trigger_eval_cases.csv` and `skill_trigger_eval_cases.jsonl`
- `skill_trigger_collision_matrix.json`

Do not hand-author files in `generated/` as if they were canonical prose. Change the owning source or the generator, then regenerate.

## Allowed changes

Safe, normal contributions here include:

- regenerating committed outputs after source changes
- fixing generator logic or contracts when a derived surface is wrong
- tightening schema or parity checks around derived surfaces
- removing stale generated drift after the owning sources were corrected

## Changes requiring extra care

Use extra caution when:

- changing the shape of a generated JSON surface
- changing wording that downstream readers may parse or rely on
- changing how walkthrough, evaluation, lineage, or governance signals are derived
- changing multiple derived surfaces without naming the owning authored cause
- changing candidate-bridge indexes in ways that would make
  `requested_not_landed` look like promoted skill truth

## Hard NO

Do not:

- manually edit a generated file and stop there
- treat a generated surface as a replacement for the authored bundle
- sneak undocumented policy changes into derived outputs
- delete generated files to hide source or generator drift

## Validation

For changes that affect derived outputs, run:

- `python scripts/build_catalog.py`
- `python scripts/build_agent_skills.py --repo-root .`
- `python scripts/validate_nested_agents.py`
- `python scripts/validate_skills.py`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/lint_trigger_evals.py --repo-root .`
- `python scripts/build_agon_skill_binding_candidates.py --check`
- `python scripts/validate_agon_skill_binding_candidates.py`
- `python scripts/build_catalog.py --check`

If a generated file changed unexpectedly, inspect the owning source before accepting the diff.

## Output expectations

When reporting work in `generated/`, include:

- which derived surfaces changed
- which authored sources caused the change
- whether any schema or contract shape changed
- what regeneration and validation commands were run
