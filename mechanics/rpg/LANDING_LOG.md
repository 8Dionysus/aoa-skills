# RPG Landing Log

## 2026-05-06 - Ability And Loadout Reader Slice

Landed the first `aoa-skills` RPG package around skill ability-card and loadout
reader posture.

Changed route:

- moved ability model guidance out of flat `docs/`
- moved loadout posture guidance out of flat `docs/`
- added package card, direction, parts, provenance, landing log, roadmap, and
  two active parts

Preserved stop-lines:

- skill bundles stayed under `skills/`
- generated ability cards and schemas stayed in place
- pack profiles and trust-policy surfaces stayed in place
- no runtime inventory, role canon, playbook choreography, proof verdict,
  quest closure, memory canon, routing authority, owner acceptance, or automatic
  skill promotion was claimed

Checks:

- generated-surface schemas, mechanics routes and topology, and nested agent
  cards all passed
