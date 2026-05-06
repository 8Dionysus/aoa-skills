# Mechanic Artifact Topology

Date: 2026-05-06

Status: accepted

## Context

`aoa-skills` had already moved many active mechanics documents, seeds, examples,
manifests, and quests into `mechanics/`, but root technical districts still
carried several mechanic-local contracts. In particular, root `schemas/`,
`scripts/`, and `tests/` still made Agon candidate bridges, checkpoint notes,
method-growth adoption/followthrough objects, experience invocation patches,
and Questbook contracts look repo-wide.

The AoA center pattern keeps root technical districts for root-wide contracts
and moves mechanic-owned substance beside the owning package or nearest part.
`aoa-skills` needs the same placement rhythm, adapted to the skill layer:
generated root read models may stay root-published, but their source contracts
should not stay flat when a mechanic owns them.

## Decision

Add `mechanics/ARTIFACT_TOPOLOGY.md` as the placement law for mechanic-adjacent
schemas, examples, config, generated companions, manifests, scripts, tests, and
quests.

Move obvious mechanic-owned artifacts to their owners:

- Agon skill-binding and epistemic candidate schemas, examples, builders,
  validators, and tests move under their owning Agon parts.
- Checkpoint note schema moves under `mechanics/checkpoint/schemas/`.
- Method-growth owner-status, followthrough, adoption, regression, retirement,
  and pattern-handoff schemas move under `mechanics/method-growth/schemas/`.
- Experience governance, installation, office, service, receipt, rollback, and
  policy-hold schemas move under `mechanics/experience/schemas/`.
- Quest source and dispatch schemas move under `mechanics/questbook/schemas/`.

Keep root `generated/agon_*.min.json` and `generated/quest_*.json` as
root-published read models over mechanic-owned sources.

## Consequences

- Callers must use mechanic-owned paths directly. Do not add root aliases.
- Root `schemas/` remains for repo-wide skill, export, governance, release,
  evaluation, and public reader contracts.
- Root `scripts/` remains for repo-wide deterministic builders, validators,
  reports, inspectors, release checks, and shared helpers.
- Root `tests/` remains for repo-wide behavior and cross-package invariants;
  tests that only validate one mechanic-owned part may live with that part.
- Release checks and package cards must name the moved Agon builder, validator,
  and test paths.

## Verification

This decision is covered by `tests/test_mechanics_topology.py`, the moved Agon
part tests, and the release-check Agon builder/validator commands.
