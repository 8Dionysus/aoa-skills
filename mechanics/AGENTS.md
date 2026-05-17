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

Run the target package validator first. For mesh shape, run `python scripts/validate_nested_agents.py`; for release-facing changes, run `python scripts/release_check.py`.

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
- Generated artifacts remain evidence or export companions, not authority.
- Legacy surfaces preserve lineage. They are not junk drawers, and current
  active behavior must not live only there.
- If a mechanic becomes an executable skill bundle with stable trigger
  boundaries, inputs, outputs, risks, and verification, promote it through
  `skills/` instead of letting it sprawl here.
