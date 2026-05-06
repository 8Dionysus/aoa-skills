# Questbook Provenance

This bridge keeps the current active route tied to the source surfaces that
landed it. Use it for auditing, not as the main entry route.

## Moved Active Doc

The first questbook package landing moved this active doc out of flat `docs/`
and into package-local active docs:

| Former path | Current path | Active route |
|---|---|---|
| `docs/QUESTBOOK_SKILL_INTEGRATION.md` | `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md` | [Session Harvest Posture](parts/session-harvest-posture/README.md), [Source Index Boundary](parts/source-index-boundary/README.md) |

This doc was not archived as raw legacy because it remains an active contract
surface. The move changes its route, not its authority level.

## Source And Projection Companions

Current questbook source and projection surfaces remain in:

- `mechanics/questbook/QUESTBOOK.md`
- `quests/*.yaml`
- `schemas/quest.schema.json`
- `schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`

This package may route to those surfaces, but it does not turn generated
quest projections into source truth.

## Skill Companion

Canonical quest-harvest skill meaning remains in:

- `skills/aoa-quest-harvest/SKILL.md`
- `skills/aoa-quest-harvest/references/quest-promotion-receipt-schema.yaml`

## Neighbor Routes

- `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md` owns the
  pre-harvest orchestration read.
- `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md` owns lower-authority
  checkpoint capture before reviewed closeout.
- `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md` owns reviewed
  `candidate_ref` after donor harvest.

## Stop-Line

The questbook package preserves public obligations and projection boundaries.
It does not close quests, prove claims, author playbooks, write memory, or
accept work for another owner.
