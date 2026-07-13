# Mechanics Questbook Integration

- Decision ID: AOA-SK-D-0010

## Index Metadata

- Original date: 2026-05-06
- Surface classes: mechanic package, quest/lane
- Skill lanes: none
- Mechanic parents: questbook
- Guard families: questbook, source topology
- Posture: accepted questbook integration

Date: 2026-05-06

Status: accepted

Superseded in part by
`AOA-SK-D-0001-distributed-mechanics-roadmaps-and-root-questbook.md`: the public
tracked obligation index now lives at root `QUESTBOOK.md`. The source/index,
generated-readout, and owner-boundary stop-lines in this decision still stand.

## Context

After Growth-cycle and Checkpoint gained package-local homes, the remaining
Questbook integration note was still flat in `docs/`. Direct reading showed
that the note is active mechanics guidance: it describes how deferred skill
obligations, session-harvest posture, and quest-harvest verdict pressure move
around `aoa-skills`.

`mechanics/questbook/QUESTBOOK.md` and `quests/` have a different role. They are
public tracked obligation sources for this repository, not package internals.
Moving them in the same slice would make the package look cleaner while making
the public obligation route less honest.

## Decision

Create `mechanics/questbook/` as the owner-local mechanics package for
Questbook integration posture.

Move only the active integration note:

- `docs/QUESTBOOK_SKILL_INTEGRATION.md` -> `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`

Keep these surfaces in their current homes:

- `mechanics/questbook/QUESTBOOK.md` (superseded placement; now root
  `QUESTBOOK.md`)
- `quests/`
- quest schemas
- generated quest catalog and dispatch projections
- canonical `skills/core/session-growth/aoa-quest-harvest/SKILL.md`

Add a package card, direction, parts, provenance, landing log, roadmap, active
docs map, and active parts for source/index boundary, session-harvest posture,
and dispatch projection.

## Consequences

- Flat `docs/` no longer owns the Questbook integration contract.
- `mechanics/questbook/` can explain movement without becoming a second
  roadmap or hidden task queue.
- Root quest sources remain stable public entrypoints.
- Generated quest views remain read models and cannot author quest meaning.
- Future questbook work must choose between source edits, package-local
  mechanics posture, generated projection repair, or sibling-owner handoff.

## Verification

Verification covered skill validation, checkpoint behavior, mechanics routes
and topology, nested agent cards, catalog parity, and the repository test
suite.
