# Distributed Mechanics Roadmaps And Root Questbook

- Decision ID: AOA-SK-D-0001

## Index Metadata

- Original date: 2026-05-06
- Surface classes: root/topology, mechanic package, quest/lane
- Skill lanes: none
- Mechanic parents: cross-mechanic, questbook
- Guard families: questbook, docs route
- Posture: accepted distributed mechanics direction

Date: 2026-05-06

Status: accepted

## Context

`mechanics/ROADMAP.md` had accumulated repo-wide release, governance, overlay,
packaging, checkpoint, quest, growth, risk, and RPG pressure in one file. That
made it easy to keep material visible, but hard for a future agent to know
which mechanic must be updated after a change.

The Questbook public index also lived inside `mechanics/questbook/`, which made
the mechanic package look like the obligation source. In `Agents-of-Abyss`, the
root Questbook is the compact public index while `mechanics/questbook/` owns the
mechanism, parts, lifecycle law, and source/index boundary.

## Decision

Keep `mechanics/ROADMAP.md` as a route index only. Package `ROADMAP.md` files
own package future contours.

Move the public tracked obligation index to root `QUESTBOOK.md`. Keep
`mechanics/questbook/` as the owner-local mechanic for source/index boundaries,
session-harvest posture, quest dispatch projection, and `aoa-quest-harvest`
posture.

Distribute the former broad roadmap pressure by owner:

- audit: public-surface, evaluation, governance backlog, and review evidence
- boundary-bridge: overlays, bridge contracts, tiny-router, MCP/OpenAI/Codex,
  and downstream-consumption seams
- release-support: portable export, runtime seams, release manifest, staged
  bundle, ZIP, and packaging smoke
- method-growth: maturity, promotion, default-reference rationale, owner-status,
  and adoption evidence
- growth-cycle: project-core session-growth kernel and reviewed-session harvest
- checkpoint: checkpoint-note and closeout bridge boundaries
- questbook: quest index/source law, dispatch projection, and quest-harvest
  verdict posture
- agon, recurrence, rpg, antifragility, and experience: their package-local
  movement surfaces and stop-lines

## Consequences

- Future changes should update the nearest package roadmap instead of growing a
  repo-wide backlog.
- Root `QUESTBOOK.md` becomes the public obligation index; `quests/` remains the
  lane-first source store; generated quest files remain read models.
- `mechanics/questbook/QUESTBOOK.md` is no longer an active path.
- Prior decisions that kept the public Questbook inside the package are
  superseded only for this placement; their source/index and generated-readout
  stop-lines still stand.
- Validators, tests, and docs must route to root `QUESTBOOK.md`.

## Verification

Use:

```bash
python -m pytest -q tests/test_current_direction_routes.py tests/test_roadmap_parity.py tests/test_mechanics_topology.py tests/test_validate_skills.py
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/validate_nested_agents.py
python -m unittest discover -s tests
```
