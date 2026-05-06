# RPG Provenance

This bridge keeps the current active route tied to the source surfaces that
landed it. Use it for auditing, not as the main entry route.

## Moved Active Docs

The first RPG package landing moved two active reader-surface docs out of flat
`docs/` and into active parts:

| Former path | Current path | Active route |
|---|---|---|
| `docs/SKILL_ABILITY_MODEL.md` | `mechanics/rpg/parts/ability-reader-boundary/README.md` | [Ability Reader Boundary](parts/ability-reader-boundary/README.md) |
| `docs/ABILITY_LOADOUT_POSTURE.md` | `mechanics/rpg/parts/loadout-posture/README.md` | [Loadout Posture](parts/loadout-posture/README.md) |

These docs were not archived as raw legacy because they remain active contract
surfaces. The move changes their route, not their authority level.

## Source And Projection Companions

Current RPG reader companions remain in:

- `skills/**/SKILL.md`
- `skills/**/techniques.yaml`
- `generated/skill_evaluation_matrix.*`
- `config/skill_pack_profiles.json`
- `config/skill_policy_matrix.json`
- `generated/skill_ability_cards.min.example.json`
- `schemas/skill_ability_catalog.schema.json`
- `mechanics/release-support/docs/CODEX_PORTABLE_LAYER.md`
- `mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md`
- `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`

This package may route to those surfaces, but it does not turn generated
ability cards into skill truth.

## Neighbor Routes

- `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md` owns
  reviewed session-growth maturity guidance.
- `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md` owns durable
  quest-shaped obligations.
- `aoa-playbooks` owns scenario builds, rotations, and campaign choreography.
- `abyss-stack` and owner projects own runtime inventory or delivery state.

## Source Bridge

Relevant external surfaces consulted for this split:

- `Agents-of-Abyss/mechanics/rpg/README.md`
- `Agents-of-Abyss/mechanics/rpg/PARTS.md`
- `aoa-techniques/mechanics/rpg/README.md`
- `aoa-techniques/mechanics/rpg/PARTS.md`

## Stop-Line

The RPG package keeps skill ability and loadout reader surfaces adjunct. It
does not rewrite skill truth, create runtime equipped state, author playbooks,
prove progression, close quests, write memory, route dispatch, or accept work
for another repository.
