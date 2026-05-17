# AGENTS.md

## Applies to

This card applies to `skills/` except where a nearer family card applies.

## Role

`skills/` owns canonical executable skill content: `SKILL.md`, `techniques.yaml`, optional `agents/openai.yaml`, checks, examples, references, scripts, assets, and bundle-local support files.

## Read before editing

Read root `AGENTS.md`, `DESIGN.md`, `skills/README.md`, the nearest family `AGENTS.md`, and the target bundle surfaces before editing.

## Boundaries

Do not add per-bundle `AGENTS.md` by default. Bundle truth belongs in `SKILL.md` and bundle support files. Do not move mechanic work into skills, and do not use technique links as a blocker for self-contained skill usefulness.

## Validation

Run `python scripts/validate_nested_agents.py`, `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`, and focused tests for changed bundle behavior.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.

## Bundle Contract

Treat these as canonical bundle surfaces when present:

- `SKILL.md`
- `techniques.yaml`
- optional `agents/openai.yaml`
- optional `checks/`, `examples/`, `references/`, `scripts/`, and `assets/`

`SKILL.md` and `techniques.yaml` remain the canonical pair. Support artifacts
clarify, constrain, or verify the bundle; they should not silently override it.
The generated export lives under `.agents/skills/*`; edit the canonical bundle
first, then regenerate.

Do not add flat alias directories at `skills/<name>` for compatibility.
Compatibility belongs in generated exports or deterministic builders that
resolve the canonical source path.

## Extra Care

Use extra care when changing a skill identifier or directory name, status,
summary, invocation posture, technique dependencies, support artifacts, live
overlay family relationships, or topology lane.

Never put secrets, private runtime details, upstream technique doctrine,
playbook composition, or vague destructive actions inside a skill bundle.
