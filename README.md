# aoa-skills

Public library of reusable Codex-facing skills for coding agents and humans.

`aoa-skills` is the operational companion to `aoa-techniques`.
Where `aoa-techniques` stores public, reusable, validated engineering techniques,
`aoa-skills` stores **skill bundles** that compose one or more techniques into
bounded, reviewable workflows for Codex.

A skill here is not a random prompt and not a hidden project hack.
It is a reusable agent-facing workflow with clear trigger boundaries,
explicit contracts, risks, verification guidance, and technique traceability.

## Start here

If you are new to this repository, follow this short path:

1. Read `docs/README.md` for the docs map.
2. Read `docs/RUNTIME_PATH.md` for the runtime path: `pick -> inspect -> expand -> object use`.
3. Read `docs/EVALUATION_PATH.md` for evaluation evidence, matrix outputs, and snapshot-backed coverage.
4. Read `generated/skill_walkthroughs.md` for the current derived runtime walkthrough surface.
5. Read `generated/skill_evaluation_matrix.md` for the current derived evaluation evidence surface.
6. Read `docs/PUBLIC_SURFACE.md` for the public-product and governance signals.
7. Read `docs/ARCHITECTURE.md` for the high-level model.
8. Read `docs/BRIDGE_SPEC.md` to understand how skills relate to `aoa-techniques`.
9. Read `generated/public_surface.md` for the current derived cohort split.
10. Read `SKILL_INDEX.md` for the current skill surface.
11. Open `skills/aoa-change-protocol/SKILL.md` as the first starter skill.
12. Use `templates/SKILL.template.md`, `templates/RUNTIME_EXAMPLE.template.md`, and `templates/EVALUATION_SNAPSHOT.template.md` when authoring new skill surfaces.

## Quick routes

- if you need the upstream reusable practice canon, go to [aoa-techniques](https://github.com/8Dionysus/aoa-techniques)
- if you need portable proof surfaces for skill quality, boundaries, or regressions, go to [aoa-evals](https://github.com/8Dionysus/aoa-evals)
- if you need the smallest next object by task type, go to [aoa-routing](https://github.com/8Dionysus/aoa-routing)
- if you need explicit role contracts, handoff posture, or persona surfaces, go to [aoa-agents](https://github.com/8Dionysus/aoa-agents)
- if you need higher-level scenario composition, go to [aoa-playbooks](https://github.com/8Dionysus/aoa-playbooks)

## What belongs here

Good candidates:
- reusable Codex-facing workflows
- bounded change-protocol skills
- testing and validation skills
- architecture and context-mapping skills
- contract and invariant skills
- project overlay examples that stay thin and explicit
- skill generation or refresh helpers

Bad candidates:
- private infrastructure instructions
- secret-bearing examples
- raw project dumps
- one-off prompts without reusable boundaries
- techniques that should live in `aoa-techniques`
- undocumented scripts
- skills that silently widen the task without naming it

## Core distinction

### `aoa-techniques`
Stores the public canon of reusable engineering techniques.
A technique is a minimal reproducible unit of engineering practice.

### `aoa-skills`
Stores the Codex-facing execution layer.
A skill may depend on one or more techniques and package them into
an executable workflow for agents.

In short:

`origin project -> technique canon -> skill canon -> project overlay`

The current repo-local surface stack is:

- runtime selection and object use: `docs/RUNTIME_PATH.md`, `generated/skill_walkthroughs.*`, `scripts/inspect_skill.py`
- evaluation evidence and matrix reading: `docs/EVALUATION_PATH.md`, `generated/skill_evaluation_matrix.*`, `tests/fixtures/skill_evaluation_cases.yaml`, `scripts/report_skill_evaluation.py`
- public-product and governance signals: `docs/PUBLIC_SURFACE.md`, `generated/public_surface.*`

The runtime path for public skill use is:

`pick -> inspect -> expand -> object use`

For KAG/source-lift consumers, `AOA-T-0019` is the canonical bundle-level metadata spine and `AOA-T-0018` is the bounded section-lift layer. The authored markdown bundle still owns the meaning; derived metadata and section surfaces only help routing.

## Core principles

- techniques are the source of truth for reusable practice
- skills are the agent-facing operational interface
- public by design, sanitized by default
- bounded scope over vague power
- runtime skills should stay self-contained and reviewable
- build-time composition over runtime remote dependency
- thin overlays over hidden project assumptions
- validation matters
- traceability matters

## Repository structure

- `docs/` — architecture, bridge rules, roadmap, conventions
- `templates/` — templates for skill authoring and composition metadata
- `skills/` — skill bundles
- `generated/` — derived reader catalogs, local runtime cards, section surfaces, walkthrough surfaces, snapshot-backed evaluation matrix surfaces, and public-product surfaces built from committed skill markdown, manifests, support artifacts, review records, and evaluation fixtures
- `scripts/` — local validation and refresh helpers
- `schemas/` — machine-readable bundle contracts
- `tests/` — local validator and evaluation tests
- `SKILL_INDEX.md` — repository-wide skill map

Local working notes such as `TODO.local.md` and `PLANS.local.md` stay gitignored in each clone.
The public planning artifact for this repository is `docs/ROADMAP.md`, which remains tracked.

A typical skill bundle contains:
- `SKILL.md`
- `techniques.yaml`
- optional `agents/openai.yaml`
- optional `examples/`, `references/`, or `checks/`

`SKILL.md` and `techniques.yaml` remain authoritative.
`generated/skill_catalog.json` and `generated/skill_catalog.min.json` are derived reader surfaces for routing and indexing.
`generated/skill_capsules.json` is a derived local runtime-card surface with bounded per-skill summaries.
`generated/skill_sections.full.json` is the source-owned section payload surface for bounded expand-time reads.
`generated/skill_walkthroughs.json` and `generated/skill_walkthroughs.md` are derived runtime inspect surfaces built from skill markdown and support artifacts.
`generated/skill_evaluation_matrix.json` and `generated/skill_evaluation_matrix.md` are derived evaluation evidence surfaces built from committed fixtures, snapshot cases, runtime artifacts, and review records.
`generated/public_surface.json` and `generated/public_surface.md` are derived governance and public-product surfaces.

## Skill categories

- `core` — public reusable skills across many repositories
- `project` — skills shaped for a repository family such as `atm10-*` or `abyss-*`
- `risk` — operationally sensitive skills that should usually be explicit-only

## Current repository phase

This repository now has a mixed-status public core of 13 skills with first support artifacts, pinned bridge manifests, local validation for bundle shape and policy coherence, and source-owned section surfaces for bounded expand-time reads.
It now includes first `canonical` skills, expanded `evaluated` core and risk surfaces, autonomy and trigger-boundary evaluation checks, documented maturity and promotion guidance through `docs/PROMOTION_PATH.md`, a separate evaluation evidence layer in `docs/EVALUATION_PATH.md`, and a derived public-surface layer in `docs/PUBLIC_SURFACE.md` and `generated/public_surface.*`.
It now also includes a runtime inspection layer in `docs/RUNTIME_PATH.md`, `generated/skill_walkthroughs.*`, and `scripts/inspect_skill.py`, with `docs/EVALUATION_PATH.md` and `tests/fixtures/skill_evaluation_cases.yaml` carrying the separate evaluation evidence layer that stays distinct from the derived governance/public-surface layer.
The current focus is keeping runtime selection, evaluation evidence, and public status readable as separate derived layers while using the governance surface to clarify default references, candidate-ready skills, and pending-lineage blockers.

## When not to use this repository

Do not use `aoa-skills` as:

- the source canon for reusable techniques
- the proof layer for quality claims
- the memory layer
- the role-contract layer
- the scenario-composition layer

Use it when you need a bounded, reviewable workflow bundle that an agent can execute.

## Local validation

Install the validator dependency:

```bash
python -m pip install -r requirements-dev.txt
```

Run the full repository check:

```bash
python scripts/validate_skills.py
```

Check that all generated surfaces are current:

```bash
python scripts/build_catalog.py --check
```

Refresh the derived catalogs, capsules, sections, walkthroughs, evaluation matrix, and public surface:

```bash
python scripts/build_catalog.py
```

Inspect a skill through the runtime path:

```bash
python scripts/inspect_skill.py --skill aoa-change-protocol
```

Inspect the same skill's support artifacts and review evidence:

```bash
python scripts/inspect_skill.py --skill aoa-change-protocol --view evidence
```

Run a single skill check:

```bash
python scripts/validate_skills.py --skill aoa-change-protocol
```

The validator now uses repository schemas from `schemas/` as the contract layer for
front matter, `techniques.yaml`, and `agents/openai.yaml`.
It also checks that the generated catalogs, capsules, full section surfaces, walkthrough surfaces, evaluation matrix surfaces, and derived public-surface JSON/Markdown exist, stay current, that the min catalog is an exact projection of the full catalog, and that capsules, sections, walkthroughs, and evaluation surfaces stay aligned with the same source bundles.

Read the derived evaluation matrix directly:

```bash
python scripts/report_skill_evaluation.py
```

Fail fast if any canonical skill has snapshot-backed evaluation gaps:

```bash
python scripts/report_skill_evaluation.py --fail-on-canonical-gaps
```

Preview a manifest-driven `SKILL.md` refresh without rewriting files:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol
```

Apply a manifest-driven refresh to one explicitly named skill:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol --write
```

The first write mode is intentionally bounded to a single skill per run.

Check whether published technique refs have drifted against a local `aoa-techniques` checkout:

```bash
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques
```

Preview an upstream-driven refresh for explicitly named skills:

```bash
python scripts/refresh_skill_from_techniques.py --skill aoa-change-protocol --techniques-repo ../aoa-techniques
```

Recommended bridge refresh order:

1. `python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques`
2. `python scripts/refresh_skill_from_techniques.py --skill aoa-change-protocol --techniques-repo ../aoa-techniques`
3. manually review whether upstream technique drift requires runtime wording changes beyond traceability and pinned refs
4. `python scripts/build_catalog.py`
5. `python scripts/validate_skills.py`

The drift and refresh tools intentionally use CLI output and git diff as the review surface.
They do not add committed drift-report artifacts, and the upstream refresh flow remains bounded to explicitly named skills.

## Contribution model

A skill is usually shaped from one or more real techniques.
Those techniques are first born and validated in a real project,
then promoted into `aoa-techniques`, and only then packaged here
into a Codex-facing skill.

In short:

`project -> validation -> sanitization -> promotion -> technique canon -> skill composition`

## Intended users

- coding agents
- solo builders
- infra engineers
- product engineers
- AI workflow designers
- teams that want reusable agent workflows

## License

Apache-2.0
