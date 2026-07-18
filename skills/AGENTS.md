# AGENTS.md

## Applies to

This card applies to `skills/` and all callable bundle sources below it.

## Role

`skills/` owns the admitted portable callable procedures and their required
bundle-local resources.

## Read before editing

Read root `AGENTS.md`, `DESIGN.md`, `capabilities/README.md`, this card,
`skills/README.md`, the nearest lane card, the target `SKILL.md`, and its bound
capability family.

## Boundaries

- Do not create one bundle per capability or mode.
- Do not add a runtime dependency on techniques.
- Keep owner-specific facts in owner-qualified adapters, not copied into a
  generic bundle.
- `agents/openai.yaml` is a host adapter; `SKILL.md` remains portable source.
- Do not add per-bundle `AGENTS.md` without a genuine nested owner boundary.
- Raw trial evidence and task-local DAGs stay outside the repository.

## Validation

Exercise changed behavior manually first. Then run the source validator,
capability parity check, portable export builder/validator, and only focused
tests that protect stable observed invariants.

## Closeout

Report trigger and ABI changes, manual positive/negative/coexistence cases,
capability binding changes, export refresh, checks, and lifecycle consequence.
