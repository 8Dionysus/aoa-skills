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
2. Read `docs/ARCHITECTURE.md` for the high-level model.
3. Read `docs/BRIDGE_SPEC.md` to understand how skills relate to `aoa-techniques`.
4. Read `SKILL_INDEX.md` for the current skill surface.
5. Open `skills/aoa-change-protocol/SKILL.md` as the first starter skill.
6. Use `templates/SKILL.template.md` when authoring a new skill.

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

## Skill categories

- `core` — public reusable skills across many repositories
- `project` — skills shaped for a repository family such as `atm10-*` or `abyss-*`
- `risk` — operationally sensitive skills that should usually be explicit-only

## Current repository phase

This repository now has a mixed-status public core of 13 skills with first support artifacts,
honest bridge manifests with pinned source refs, and local validation for bundle shape and policy coherence.
The repository now also has its first `evaluated` skills and autonomy and trigger-boundary evaluation checks for seven representative skills.
The repository now also has a documented maturity ladder and promotion guidance.
The next focus is broadening evaluation and governance around that public core.

## Local validation

Install the validator dependency:

```bash
python -m pip install -r requirements-dev.txt
```

Run the full repository check:

```bash
python scripts/validate_skills.py
```

Run a single skill check:

```bash
python scripts/validate_skills.py --skill aoa-change-protocol
```

The validator now uses repository schemas from `schemas/` as the contract layer for
front matter, `techniques.yaml`, and `agents/openai.yaml`.

Preview a manifest-driven `SKILL.md` refresh without rewriting files:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol
```

Apply a manifest-driven refresh to one explicitly named skill:

```bash
python scripts/refresh_skill_from_manifest.py --skill aoa-change-protocol --write
```

The first write mode is intentionally bounded to a single skill per run.

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
