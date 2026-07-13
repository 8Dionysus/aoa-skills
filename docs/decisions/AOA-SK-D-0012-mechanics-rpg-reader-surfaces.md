# Mechanics RPG Reader Surfaces

- Decision ID: AOA-SK-D-0012

## Index Metadata

- Original date: 2026-05-06
- Surface classes: mechanic package, generated/readout
- Skill lanes: none
- Mechanic parents: rpg
- Guard families: generated/read-model, source topology
- Posture: accepted reader surface posture

Date: 2026-05-06

Status: accepted

## Context

Two RPG-shaped reader docs remained flat in `docs/`: ability cards and loadout
posture. Direct reading showed they are active mechanics guidance, not skill
bundle meaning. They describe how to read skill bundles through ability and
loadout vocabulary while keeping `SKILL.md`, technique refs, evaluation
evidence, pack profiles, adapter posture, and overlay posture authoritative.

`Agents-of-Abyss` owns center RPG world grammar. `aoa-techniques` already has a
local RPG package for technique-layer reflection. The `aoa-skills` slice needed
a thinner local package for ability/loadout reader posture over skill bundles.

## Decision

Create `mechanics/rpg/` and land only the ability/loadout reader slice:

- `docs/SKILL_ABILITY_MODEL.md` -> `mechanics/rpg/parts/ability-reader-boundary/README.md`
- `docs/ABILITY_LOADOUT_POSTURE.md` -> `mechanics/rpg/parts/loadout-posture/README.md`

Add a package card, direction, parts, provenance, landing log, roadmap, and
active parts.

Keep these surfaces in their current homes:

- canonical skill bundles under `skills/`
- generated ability examples and schema
- pack profiles and trust-policy config
- progression artifacts and session-growth evidence

## Consequences

- Flat `docs/` no longer owns ability/loadout reader posture.
- Ability cards remain derived reader surfaces below skill truth.
- Loadout remains pack-profile posture, not runtime equipped state.
- Scenario builds and rotations stay out of `aoa-skills` and route to
  `aoa-playbooks` when needed.

## Verification

Verification covered generated-surface schemas, mechanics routes and topology,
and nested agent cards.
