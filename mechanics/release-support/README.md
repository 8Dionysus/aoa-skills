# Release Support

This package keeps the source-to-portable handoff reproducible:

```text
skills + capabilities + config
  -> temporary portable assembly + catalogs + release manifest
  -> profile-scoped staged directory or ZIP
  -> inspect -> install -> verify
```

`portable-consumer-advertised` transports the seven currently advertised
shared bundles to an explicit external consumer.
`portable-consumer-all-sources` transports all nine shared source bundles for
explicit research and manual trials; engineering-shape and verification remain
deferred.

The source repository keeps no `.agents/skills` projection. The logical
`.agents/skills/<name>` layout exists only inside a staged directory or ZIP
handoff. The separate `os-user-default` assembler installs shared and admitted
owner-home bundles once into the verified host user catalog.

The machine release contract is `generated/release_manifest.json`. It binds
source hashes, portable hashes, profile revisions, generated artifacts, and
changelog identity. The bundle manifest under `manifests/` adapts that subject
to the external `abyss-machine` artifact verifier.

The OS installer uses clean owner sources for the normal user destination.
Dirty candidate worktrees may be exercised only in a separate explicit
non-production destination; installation receipts remain provenance and parity
records, never routing or outcome proof.

See `docs/CODEX_PORTABLE_LAYER.md`, `docs/INSTALL_AND_PROFILES.md`, and
`docs/RELEASING.md`.
