# AGENTS.md

Guidance for coding agents and humans working under `skills/`.

## Purpose

`skills/` stores the authoritative skill bundles for `aoa-skills`. The authored bundle owns skill meaning, especially `SKILL.md` and `techniques.yaml`. Generated catalogs, capsules, walkthroughs, and matrices may summarize a skill, but they do not replace the authored bundle.

## Read this first

Before editing a bundle in this directory, read in this order:

1. `../AGENTS.md`
2. `../docs/ARCHITECTURE.md`
3. `../mechanics/boundary-bridge/docs/BRIDGE_SPEC.md`
4. `../mechanics/release-support/docs/RUNTIME_PATH.md`
5. the nearest nested `AGENTS.md` for the target lane
6. `README.md`
7. the target `skills/**/<skill>/SKILL.md`
8. the target `skills/**/<skill>/techniques.yaml`
9. any touched `checks/`, `examples/`, `references/`, or `agents/openai.yaml`
10. for live overlay skills, `../mechanics/boundary-bridge/docs/OVERLAY_SPEC.md` and the matching `../mechanics/boundary-bridge/overlays/<family>/PROJECT_OVERLAY.md`

## Directory contract

Treat these as the canonical bundle surfaces when present:

- `SKILL.md`
- `techniques.yaml`
- optional `agents/openai.yaml`
- optional `checks/`, `examples/`, and `references/`

`SKILL.md` and `techniques.yaml` remain the canonical pair. Support artifacts should clarify, constrain, or verify the bundle. They should not silently override it.
The generated Codex-facing export lives separately under `.agents/skills/*`; edit the canonical bundle first, then regenerate the export.

Bundle discovery is recursive under `skills/`. Do not add flat alias
directories at `skills/<name>` for compatibility. Compatibility belongs in the
generated `.agents/skills/*` export and in deterministic builders that resolve
the canonical source path.

Do not add per-bundle `AGENTS.md` by default. A skill bundle already carries its own contract surface, and a deeper `AGENTS.md` only makes sense when there is a real local conflict that cannot be stated cleanly in the bundle itself.
Lane-level `AGENTS.md` files are expected in this topology. They own local
route law for functional branches such as core engineering, session growth,
risk, and project overlays. Do not add lane `README.md` files by default; the
root `skills/README.md` is the source topology atlas, while lane law belongs in
the nearest `AGENTS.md`.

## Allowed changes

Safe, normal contributions here include:

- refining a skill's bounded workflow wording
- tightening trigger boundaries
- improving inputs, outputs, contracts, risks, anti-patterns, and verification guidance
- adding or updating support artifacts that stay public-safe and reviewable
- aligning technique traceability with upstream canon
- adding a new skill bundle when it clearly packages upstream practice into a bounded workflow

## Changes requiring extra care

Use extra caution when:

- changing a skill identifier or directory name
- changing `scope`, `status`, `summary`, `invocation_mode`, or `technique_dependencies`
- changing the relation between a bundle and its support artifacts
- removing support artifacts referenced by generated surfaces or review docs
- turning a multi-technique skill into a single-technique exception or vice versa
- changing live overlay family relationships under `skills/project/*`
- moving a bundle between topology lanes, because generated source paths,
  support-resource manifests, catalog rows, and route docs must move with it

## Hard NO

Do not:

- put secrets, tokens, internal-only URLs, or private project runtime details here
- duplicate upstream technique doctrine that belongs in `aoa-techniques`
- widen a skill into a playbook or a downstream integration
- hide destructive or risk-heavy actions inside vague prose
- add per-bundle `AGENTS.md` as a default pattern

## Validation

When bundle sources change, run the bounded repository flow:

- `python scripts/build_catalog.py`
- `python scripts/build_agent_skills.py --repo-root .`
- `python -m unittest discover -s tests`
- `python scripts/validate_nested_agents.py`
- `python scripts/validate_skills.py`
- `python scripts/validate_agent_skills.py --repo-root .`
- `python scripts/lint_trigger_evals.py --repo-root .`
- `python scripts/build_catalog.py --check`

If only a subset of surfaces changed, still make sure the affected bundle remains bounded, public-safe, and reviewable.

## Output expectations

When reporting work in `skills/`, include:

- which skills changed
- whether bundle meaning changed or only metadata/support artifacts changed
- whether technique dependencies changed
- whether overlay relationships changed
- whether generated surfaces need to be refreshed
