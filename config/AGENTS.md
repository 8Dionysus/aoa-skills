# AGENTS.md

## Applies to

This card applies to `config/`.

## Role

`config/` owns policy matrices, install profiles, release manifests, trust gates, and other machine-readable configuration that builders use to derive portable export behavior.

## Read before editing

Read root `AGENTS.md`, `DESIGN.md`, `config/README.md`, and the schema or builder that consumes the file being changed. For kernel policy, start with `project_core_skill_kernel.json` and the relevant validator.

## Boundaries

Config changes are behavior changes. Keep portable export rules explicit, do not smuggle status promotion through config, keep trust gates reviewable, and store no secrets. If a config field changes skill meaning, update the canonical bundle or schema instead of only changing generated output.

## Validation

Run `python scripts/validate_skills.py`, the builder that consumes the changed config, and `python scripts/build_catalog.py --check` when catalog or export behavior can move.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
