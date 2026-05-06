# Checkpoint Provenance

This bridge keeps the current active route tied to the source surfaces that
landed it. Use it for auditing, not as the main entry route.

## Moved Active Doc

The first checkpoint package landing moved this active doc out of flat `docs/`
and into package-local active docs:

| Former path | Current path | Active route |
|---|---|---|
| `docs/CHECKPOINT_NOTE_PATH.md` | `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md` | [Checkpoint Note Lane](parts/checkpoint-note-lane/README.md), [Closeout Bridge Boundary](parts/closeout-bridge-boundary/README.md) |

This doc was not archived as raw legacy because it remains an active contract
surface. The move changes its route, not its authority level.

## Canonical Skill Companion

Canonical bridge skill meaning remains in:

- `skills/core/session-growth/aoa-checkpoint-closeout-bridge/SKILL.md`
- `skills/core/session-growth/aoa-checkpoint-closeout-bridge/references/checkpoint-closeout-execution-report-schema.yaml`
- `skills/core/session-growth/aoa-checkpoint-closeout-bridge/references/core-skill-application-receipt-schema.yaml`

This package may point to those surfaces, but it must not copy their skill
bundle meaning into mechanics.

## Schema And Example Companions

The checkpoint note route is checked by:

- `schemas/session_checkpoint_note.schema.json`
- `mechanics/checkpoint/examples/session_checkpoint_note.example.json`

## Neighbor Routes

- `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md` owns reviewed
  `candidate_ref` after donor harvest.
- `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md` owns later
  session-growth packet and receipt examples after `candidate_ref` already
  exists.
- `QUESTBOOK.md` and `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md` own durable
  obligations and quest-harvest posture.
- `aoa-sdk` owns checkpoint controls, local ledgers, and closeout-context
  builders outside this repository.

## Stop-Line

The checkpoint package preserves provisional carry and routes reviewed
closeout. It does not harvest, prove, progress, promote, remember, schedule,
or accept the candidate by itself.
