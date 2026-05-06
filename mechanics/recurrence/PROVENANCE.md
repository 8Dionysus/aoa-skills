# Recurrence Provenance

This bridge keeps the current active route tied to the source surfaces that
landed it. Use it for auditing, not as the main entry route.

## Moved Active Docs

The first recurrence package landing moved two compact active surfaces out of
flat `docs/` and into active parts:

| Former path | Current path | Active route |
|---|---|---|
| `docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md` | `mechanics/recurrence/parts/live-observation-producers/README.md` | [Live Observation Producers](parts/live-observation-producers/README.md) |
| `docs/RECURRENCE_REVIEW_DECISION_CLOSURE.md` | `mechanics/recurrence/parts/review-decision-closure/README.md` | [Review Decision Closure](parts/review-decision-closure/README.md) |

These docs were not archived as raw legacy because they remain active contract
surfaces. The move changes their route, not their authority level.

## Source And Projection Companions

Current recurrence config and projection companions remain in:

- `manifests/recurrence/component.skills.bundle-and-activation-beacons.json`
- `manifests/recurrence/hooks/component.skills.bundle-and-activation-beacons.hooks.json`
- `manifests/recurrence/component.agon.skill-binding-surfaces.json`
- `manifests/recurrence/hooks/component.agon.skill-binding-surfaces.hooks.json`
- `generated/description_trigger_eval_manifest.json`
- `generated/skill_evaluation_matrix.md`
- `generated/quest_dispatch.min.json`

This package may route to those surfaces, but it does not turn generated
recurrence evidence into source truth.

## Neighbor Routes

- `mechanics/agon/parts/recurrence-observation/README.md` owns Agon-local
  recurrence observation posture.
- `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md` owns
  applicability and closeout routing before recurrence becomes review pressure.
- `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md` owns durable
  quest-shaped obligations after reviewed evidence survives.
- `docs/COMPONENT_REFRESH_LAW.md` remains broader release-support and
  downstream refresh pressure in this slice.

## Source Bridge

Relevant external surfaces consulted for this split:

- `Agents-of-Abyss/mechanics/recurrence/README.md`
- `Agents-of-Abyss/mechanics/recurrence/DIRECTION.md`
- `Agents-of-Abyss/mechanics/recurrence/PARTS.md`
- `aoa-techniques/mechanics/recurrence/README.md`
- `aoa-techniques/mechanics/recurrence/PARTS.md`
- `aoa-techniques/mechanics/recurrence/PROVENANCE.md`

## Stop-Line

The recurrence package observes repeated skill pressure and routes review. It
does not invoke skills, refresh components, mutate owners, prove claims, write
memory, or accept work for another repository.
