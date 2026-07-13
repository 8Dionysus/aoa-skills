# Questbook Landing Log

## 2026-05-06 - Root Index Alignment

Moved the public tracked obligation index to root `QUESTBOOK.md` so this
package can stay a mechanic route rather than the public quest index itself.

Changed route:

- root `QUESTBOOK.md` is the compact public obligation index
- `mechanics/questbook/` owns integration posture, parts, provenance, roadmap,
  and generated projection boundaries
- `quests/`, schemas, and generated projections keep their existing source and
  read-model roles

Preserved stop-lines:

- no quest source object moved for symmetry
- no generated surface became authority
- no package roadmap became the public quest index

## 2026-05-06 - Integration Posture Slice

Landed the first `aoa-skills` questbook package around skill-layer questbook
integration and session-harvest posture.

Changed route:

- moved questbook integration guidance out of flat `docs/`
- added package card, direction, parts, provenance, active docs map, and three
  active parts
- updated validation source path for the integration note

Preserved stop-lines:

- the public obligation source was still inside the questbook package during
  this slice and is now root `QUESTBOOK.md`
- `quests/`, schemas, and generated projections stayed in place
- no generated surface became authority
- no quest closure, proof verdict, playbook choreography, memory canon, routing
  authority, or owner acceptance was claimed

Checks:

- skill-source validation, checkpoint and session-growth behavior, mechanics
  routes and topology, nested agent cards, and catalog parity all passed
