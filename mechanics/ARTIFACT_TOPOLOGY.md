# Mechanic Artifact Topology

Mechanic-local schemas, examples, config, manifests, scripts, and receipts stay
inside the package that owns them. Root `generated/` may publish a compact
derived read model when multiple repository consumers need it.

- Agon candidate sources stay under `mechanics/agon/`; root `generated/agon_*`
  files remain requested-only projections.
- Quest schemas and lifecycle law stay under `mechanics/questbook/`; source
  items stay in `quests/`; root `QUESTBOOK.md` and `generated/quest_*` are read
  models.
- Release contracts, examples, and manifests stay under
  `mechanics/release-support/`; portable bytes stay in `.agents/skills/` and
  release identity in `generated/release_manifest.json`.

Do not create a root alias, generic mechanic archive, or package solely to hold
one session's artifacts. Retired source stays in Git history.
