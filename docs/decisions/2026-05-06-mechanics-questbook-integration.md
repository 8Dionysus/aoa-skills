# Mechanics Questbook Integration

Date: 2026-05-06

Status: accepted

## Context

After Growth-cycle and Checkpoint gained package-local homes, the remaining
Questbook integration note was still flat in `docs/`. Direct reading showed
that the note is active mechanics guidance: it describes how deferred skill
obligations, session-harvest posture, and quest-harvest verdict pressure move
around `aoa-skills`.

The root `QUESTBOOK.md` and `quests/` surfaces have a different role. They are
public tracked obligation sources for this repository, not package internals.
Moving them in the same slice would make the package look cleaner while making
the public obligation route less honest.

## Decision

Create `mechanics/questbook/` as the owner-local mechanics package for
Questbook integration posture.

Move only the active integration note:

- `docs/QUESTBOOK_SKILL_INTEGRATION.md` -> `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md`

Keep these surfaces in their current homes:

- `QUESTBOOK.md`
- `quests/`
- quest schemas
- generated quest catalog and dispatch projections
- canonical `skills/aoa-quest-harvest/SKILL.md`

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

Verify with:

```bash
python -m pytest -q tests/test_validate_skills.py tests/test_session_checkpoint_note.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/build_catalog.py --check
python -m unittest discover -s tests
```
