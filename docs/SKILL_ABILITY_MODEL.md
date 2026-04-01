# Skill Ability Model

## Purpose

This note defines the second-wave ability reflection contract for `aoa-skills`.

It exists so that long-horizon quest work can read bounded skill bundles as active abilities without mutating the underlying skill sources.

## Core rule

A skill ability card is a derived reader surface.

It attaches to an existing skill bundle and summarizes how that bundle behaves as an executable ability.

The owner surfaces remain:

- `skills/*/SKILL.md`
- `skills/*/techniques.yaml`
- `generated/skill_evaluation_matrix.*`
- `config/skill_pack_profiles.json`
- `docs/CODEX_PORTABLE_LAYER.md`
- `docs/LOCAL_ADAPTER_CONTRACT.md`
- `docs/OVERLAY_SPEC.md`

Ability cards may help humans and agents read those sources faster. They must not replace them.

## Ability posture

A second-wave ability should stay:

- active rather than passive
- bounded rather than scenario-shaped
- reviewable through existing skill and proof surfaces
- explicit about invocation mode and risk posture
- honest about adapter and overlay constraints

## Suggested fields

A skill ability card may summarize:

- the source skill name and path
- school tags
- package kind
- invocation mode
- technique dependencies
- unlock posture derived from first-wave progression axes
- pack-profile hints
- adapter posture
- overlay posture
- evidence refs

## Unlock posture

Unlock hints should stay descriptive and evidence-backed.

Good second-wave posture:
- use first-wave rank and mastery-axis language
- name difficulty and risk ceilings
- name likely roles
- name pack profiles that fit the ability
- keep adapter posture explicit when portable use is not enough

Do not let one ability card silently overrule the underlying skill verification or trust posture.

## Boundary rules

### Skills are still skills

The source of skill meaning remains the committed skill bundle and its current evaluation / portable-layer surfaces.

### Overlays stay thin

Overlay families may appear as hints in an ability card, but they do not create a second canonical ability track.

### Playbook method stays upstream

If several abilities need choreography, route structure, or build advice, that belongs in `aoa-playbooks`, not here.

## Anti-patterns

- adding RPG lore or stat blocks to `SKILL.md` as primary meaning
- treating pack profiles as runtime equipped state
- hiding adapter requirements behind generic "can use anywhere" language
- turning a single-project overlay into a new core ability
- widening ability cards into scenario instructions that belong in playbooks
