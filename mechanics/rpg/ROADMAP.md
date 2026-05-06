# RPG Roadmap

## Current Contour

RPG owns ability-card and loadout reader posture over skill bundles. It helps
agents read bounded skills as abilities without turning RPG language into a
second skill ontology or runtime inventory.

Active parts are `parts/ability-reader-boundary/` and
`parts/loadout-posture/`.

## Next Work

- Decide whether generated ability examples need package-local validation notes.
- Reflect bounded skill bundles as abilities with pack-profile-aware unlock
  posture while keeping canonical skill meaning in `SKILL.md`.
- Keep techniques-as-feats and broader scenario/campaign composition routed to
  the owning repo or `aoa-playbooks`.
- Keep runtime inventory, equipped-state delivery, and party composition outside
  this package until a runtime owner accepts them.

## When Time Comes

- Add generated reader surfaces only when they improve action and remain clearly
  derived.
- Add loadout checks only when pack-profile posture starts drifting from
  release-support's install/profile contract.
- Promote RPG-readable skill bundles to downstream readers only after source
  skill meaning and release packaging stay aligned.

## Out Of Scope

- A second skill ontology.
- Treating pack profiles as runtime equipped state.
- Adding lore or stat blocks to `SKILL.md` as primary meaning.
