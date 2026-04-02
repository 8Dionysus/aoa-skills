# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-skills`.

## Purpose

`aoa-skills` is the bounded execution canon of AoA. It stores public, reusable, Codex-facing skill bundles that package reusable practice into reviewable workflows an agent can execute.

A skill is normally a multi-technique or multi-action package. A single-technique skill is allowed only as an explicit reviewed exception.

## Owns

This repository is the source of truth for:

- skill bundle wording and workflow structure
- trigger boundaries
- invocation posture
- skill-level inputs and outputs
- reviewability and anti-pattern language at the skill layer
- technique dependency declaration at the skill layer
- generated skill catalogs, capsules, portable export surfaces, and bounded bridge manifests derived from canonical skills

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering techniques in `aoa-techniques`
- proof doctrine or verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- role contracts in `aoa-agents`
- scenario composition in `aoa-playbooks`
- memory objects or recall surfaces in `aoa-memo`
- derived substrate semantics in `aoa-kag`
- private project-specific operations or unsanitized internal instructions

## Core rule

Only contribute skills that are:

- bounded
- reviewable
- public-safe
- useful to Codex
- traceable to reusable practice

A skill is not the origin of practice. If the meaning belongs upstream, route to the upstream repo instead of duplicating it here.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/BRIDGE_SPEC.md`
4. `docs/LAYER_POSITION.md`
5. the target `skills/*/SKILL.md`
6. any generated surfaces directly affected by the task

If the task touches technique dependencies, inspect the upstream technique bundles before editing.

If a deeper directory defines its own `AGENTS.md`, follow the nearest one.

## Primary objects

The most important objects in this repository are:

- canonical skill bundles under `skills/*/SKILL.md`
- dependency and policy inputs under `skills/*/techniques.yaml` and `config/`
- deterministic support resources under `skills/*/{scripts,references,assets}`
- generated catalogs, capsules, walkthroughs, export surfaces, and bridge manifests under `generated/` and `.agents/skills/`
- architecture, bridge, runtime, and portable-layer docs under `docs/`

## Hard NO

Do not:

- invent source practice here that belongs in `aoa-techniques`
- write eval doctrine here
- store role-contract meaning here
- store memory meaning here
- collapse scenario-level playbooks into the skill layer
- commit secrets, tokens, internal-only URLs, or sensitive infrastructure detail
- hide destructive workflows behind vague trigger boundaries
- silently widen scope beyond the stated task

Do not hand-edit `.agents/skills/*` unless the task is explicitly about export debugging. Canonical authoring remains in `skills/*`, `config/`, and the documented generated manifests.

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- which skill or surface family is changing
- whether trigger boundaries, contracts, or technique dependencies are changing
- whether portable export or downstream bridge surfaces will change
- what boundary risk exists

### DIFF

Keep the change focused and reviewable. Preserve portability, public hygiene, and bounded execution. Do not mix unrelated cleanup into skill meaning unless it is necessary for repository integrity.

### VERIFY

Run the smallest applicable validation set from `README.md`.

Minimum validation for canonical skill changes:

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
```

Use the full repo check when the change is broad:

```bash
python scripts/release_check.py
```

If you touched portable export, policy posture, descriptions, deterministic resources, or tiny-router bridge inputs, also run the documented build and validation commands for those families before finishing.

### REPORT

Summarize:

- what changed
- whether meaning changed or only docs, metadata, or generated surfaces changed
- whether trigger boundaries or technique dependencies changed
- whether portable export or downstream bridge surfaces changed
- what validation you actually ran
- any remaining follow-up work

## Validation

Do not claim checks you did not run.

For runtime-path debugging, prefer the documented local paths such as:

```bash
python scripts/inspect_skill.py --skill <skill-name>
python scripts/skill_runtime_guardrails.py discover --repo-root . ...
```

Those paths are for inspection and activation testing, not for replacing the canonical authoring surface.
