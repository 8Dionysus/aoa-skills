# Releasing aoa-skills

1. Define the release scope and update `CHANGELOG.md`.
2. Rebuild capability, portable export, Questbook, and decision indexes whose
   owner sources changed.
3. Run the release sequence from `config/validation_lanes.json` and packaging
   smoke for both current profiles.
4. Inspect `generated/release_manifest.json`, source/portable hashes, profile
   revisions, and public-safety boundary.
5. Run the external `abyss-machine` artifact bundle validator when its owner
   surface is available.
6. Land through PR and required checks, then tag and publish release notes that
   state changes, validation, skipped coverage, and known limitations.

The release manifest is a generated ABI subject, not approval or semantic
proof. `main` may contain unreleased growth; a tag is the frozen release
identity. Do not publish deferred bundles as advertised without a separate
held-out lifecycle decision.
