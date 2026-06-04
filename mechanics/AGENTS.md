# AGENTS.md

## Applies to

This card applies to `mechanics/` except where a nearer mechanic package card applies.

## Role

`mechanics/` owns skill-layer movement surfaces: adoption, audit, bridge, checkpoint, recurrence, release support, quest integration, and related package routes around the skill canon.

## Read before editing

Read root `AGENTS.md`, `mechanics/README.md`, `mechanics/ARTIFACT_TOPOLOGY.md`, `mechanics/ROADMAP.md`, and the target package `AGENTS.md`. Package README cards use `Local owns` to name local source responsibility.

## Boundaries

`skills/` owns executable skill content. Mechanics may route, evaluate, bridge, and preserve movement, but they must not rewrite bundle truth by implication or treat generated mirrors as authority.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the target package validator first. For mesh shape, run `PYTHONPATH=scripts python scripts/validation/validate_nested_agents.py`; for release-facing changes, run `python scripts/release_check.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.

## Local Law

- `mechanics/ROADMAP.md` is a direction router; package `ROADMAP.md` files own
  package future contours.
- `mechanics/ARTIFACT_TOPOLOGY.md` owns placement law for mechanic-owned
  schemas, examples, config, generated companions, manifests, scripts, tests,
  and quests.
- Package surfaces normally split into `DIRECTION.md`, `PARTS.md`,
  `PROVENANCE.md`, `LANDING_LOG.md`, `ROADMAP.md`, `parts/`, and local
  `legacy/` when source lineage must be preserved.
- Package README cards are the first reader route for a mechanic package. Keep
  them concise and source-oriented; do not move executable command lanes or
  editing conventions out of the nearest `AGENTS.md`.
- Package README cards use this local card shape:
  `## Mechanic card`, `### Trigger`, `### Local owns`,
  `### Stronger owner split`, `### Inputs`, `### Outputs`,
  `### Must not claim`, `### Validation`, and `### Next route`.
- Package README cards should name what `aoa-skills` owns, then route stronger
  law or acceptance to `Agents-of-Abyss`, sibling repositories, review records,
  generated companions, or downstream owners only when relevant.
- Active route belongs in `README.md`, `DIRECTION.md`, `PARTS.md`, and
  `parts/`; provenance belongs in `PROVENANCE.md`; checked landing history
  belongs in `LANDING_LOG.md`; future pressure belongs in `ROADMAP.md`.
- Enter package-local `legacy/` only when preserved source lineage matters.
  Legacy is not the first route for normal package edits.
- Generated artifacts remain evidence or export companions, not authority.
- Legacy surfaces preserve lineage. They are not junk drawers, and current
  active behavior must not live only there.
- If a mechanic becomes an executable skill bundle with stable trigger
  boundaries, inputs, outputs, risks, and verification, promote it through
  `skills/` instead of letting it sprawl here.
