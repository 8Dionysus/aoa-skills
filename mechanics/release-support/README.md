# Release Support

This package keeps the source-to-portable handoff reproducible:

```text
skills + capabilities + config
  -> .agents/skills + catalogs + release manifest
  -> profile-scoped staged directory or ZIP
  -> inspect -> install -> verify
```

`repo-default` contains only the advertised `aoa-decision` bundle.
`repo-capability-sources` contains all seven bundles for explicit research and
manual trials; six remain deferred.

The machine release contract is `generated/release_manifest.json`. It binds
source hashes, portable hashes, profile revisions, generated artifacts, and
changelog identity. The bundle manifest under `manifests/` adapts that subject
to the external `abyss-machine` artifact verifier.

See `docs/CODEX_PORTABLE_LAYER.md`, `docs/INSTALL_AND_PROFILES.md`, and
`docs/RELEASING.md`.
