# Growth-Cycle Session Harvest Ownership

- Decision ID: AOA-SK-D-0023

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package, memory/writeback
- Skill lanes: core/session-growth
- Mechanic parents: growth-cycle
- Guard families: source topology, memo writeback
- Posture: accepted session harvest ownership

Date: 2026-05-18

Status: accepted

## Context

Session-harvest notes were under `docs/session-harvests/`, while the active
boundary that describes what those notes are and are not lives in
`mechanics/growth-cycle/parts/harvest-note-boundary/`.

That split made `docs/` look like the owner of a Growth-cycle movement surface.
It also left the candidate-harvest template in the root `templates/` lane even
though the template is only meaningful for Growth-cycle harvest notes.

## Decision

Move the committed public-safe harvest-note lane and its template under
Growth-cycle:

- `docs/session-harvests/` -> `mechanics/growth-cycle/session-harvests/`
- `templates/SESSION_CANDIDATE_HARVEST.template.md` -> `mechanics/growth-cycle/templates/SESSION_CANDIDATE_HARVEST.template.md`

Keep `docs/` as the route map and decision/review district. Keep root
`templates/` for reusable skill and overlay source templates.

## Consequences

- Growth-cycle now owns the active harvest-note evidence lane beside the part
  that defines its boundary.
- Harvest notes remain evidence below promotion authority.
- `docs/README.md` routes to the harvest-note lane instead of owning it.
- The move does not promote harvest notes into skill, memory, proof, quest,
  playbook, or sibling-owner truth.

## Verification

Verification covered root and nested agent-card design, session-growth and
checkpoint behavior, mechanics topology, and diff hygiene.
