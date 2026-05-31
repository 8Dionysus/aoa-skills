# Skills Source Topology

- Decision ID: AOA-SK-D-0015

## Index Metadata

- Original date: 2026-05-06
- Surface classes: skill source, root/topology
- Skill lanes: core/engineering, core/session-growth, risk, project
- Mechanic parents: none
- Guard families: source topology
- Posture: accepted skill source topology

Date: 2026-05-06

Status: accepted

## Context

The canonical `skills/` source tree had remained flat while the repository
around it was becoming route-oriented: mechanics gained package cards, roadmap
ownership split by package, and generated/export surfaces stayed subordinate to
authored source.

A flat source directory made every bundle look adjacent even when their
responsibilities differed sharply: portable engineering workflows, reviewed
session-growth workflows, risk guards, and project-family overlays. That shape
did not give future agents enough local orientation before editing a bundle.

The generated Codex-facing export already has a different purpose. It must stay
flat under `.agents/skills/*` for installation and runtime lookup.

## Decision

Make `skills/` a recursive source topology:

- `skills/core/engineering/` for portable engineering workflows
- `skills/core/session-growth/` for reviewed harvest, closeout, repair,
  progression, quest, and route-growth workflows
- `skills/risk/` for approval, dry-run, infra, runtime bring-up, and sanitized
  sharing guards
- `skills/project/<family>/` for owner-family overlays such as `abyss`, `atm10`,
  and `titan`

Keep the bundle identifier as the leaf directory name. Add recursive discovery
through `scripts/skill_layout.py`, and make builders and validators resolve
source bundle paths through that helper rather than assuming `skills/<name>`.

Use lane-level `AGENTS.md` files for local route law. Keep `skills/README.md`
as the one source-topology atlas; do not add lane `README.md` files by default.

Keep `.agents/skills/*` flat as the generated portable export. Do not add flat
compatibility aliases under `skills/<name>`.

## Consequences

- Future bundle edits start from `skills/AGENTS.md`, the nearest lane
  `AGENTS.md`, then `skills/README.md`, and the bundle-local `SKILL.md` plus
  `techniques.yaml`.
- Source path changes flow through generated catalogs, portable export metadata,
  support-resource manifests, runtime inspect surfaces, and review truth-sync.
- Temporary fixture repositories may still use flat `skills/<name>` layouts
  because recursive discovery accepts any bundle directory under `skills/`.
- Project overlays stay visibly separate from portable core and risk guards.
- Mechanics remain movement surfaces around the skill layer; they do not own
  skill bundle meaning.

## Verification

Verified with:

```bash
python scripts/release_check.py
```

The release check rebuilt catalogs, portable export, runtime seams,
description-trigger cases, support resources, tiny-router inputs, and then ran
the full unittest and validation sequence.
