# Growth-Cycle Direction

This package starts with the smallest honest `aoa-skills` growth-cycle slice:
adaptive orchestration and session-growth kernel maturity.

The active route is:

```text
task execution
  -> closeout read
  -> checkpoint note or candidate harvest note
  -> explicit session-harvest family
  -> owner, proof, memory, quest, stats, or playbook route
```

## Current contour

- Skill orchestration must distinguish `apply_now`, `defer`, and `skip`.
- Closeout and harvest are separate planes.
- Session-growth kernel examples may carry existing `candidate_ref`, but they
  do not mint `seed_ref` or `object_ref`.
- Session-harvest notes remain bounded evidence, not promotion verdicts.

## Boundaries

- Checkpoint note protocol lives in `mechanics/checkpoint/`.
- Reviewed candidate identity lives in `mechanics/method-growth/`.
- Questbook obligations remain in `QUESTBOOK.md`.
- Canonical skill execution remains under `skills/`.

## Current hold

Keep `mechanics/growth-cycle/session-harvests/` as the package-local evidence
lane. If a note becomes accepted owner truth, update the owner surface and keep
the harvest note as provenance below that truth.
