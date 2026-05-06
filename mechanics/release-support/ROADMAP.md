# Release Support Roadmap

## Current Contour

Release-support owns portable export, install profiles, local adapters, runtime
seams, release manifests, deterministic support resources, staged bundles, ZIP
handoff, and packaging smoke for reusable skill bundles.

Active surfaces include `docs/CODEX_PORTABLE_LAYER.md`,
`docs/INSTALL_AND_PROFILES.md`, `docs/LOCAL_ADAPTER_CONTRACT.md`,
`docs/RELEASING.md`, `docs/RUNTIME_PATH.md`, `docs/RUNTIME_TOOL_CONTRACTS.md`,
`docs/SESSION_COMPACTION.md`, `docs/DETERMINISTIC_RESOURCE_BUNDLES.md`,
`generated/runtime_discovery_index.json`, `generated/skill_bundle_index.md`,
`generated/skill_graph.md`, and `generated/release_manifest.json`.

## Next Work

- Keep `generated/release_manifest.json` as the release-facing pinning contract
  for artifact groups, bundle revisions, profile revisions, and
  changelog-derived release identity.
- Keep the `v0.7` sequence on the same contract: release manifest, compatibility
  and lineage depth, profile install checks, staged bundle handoff, ZIP handoff,
  preflight inspection, one-shot import ergonomics, bundle README polish, and
  release-facing packaging smoke.
- Keep compatibility and lineage detail in `generated/skill_bundle_index.*` and
  relationship topology in `generated/skill_graph.*`; do not overload the
  release manifest with graph truth.
- Keep local adapter and compaction posture tied to
  `mechanics/release-support/docs/LOCAL_ADAPTER_CONTRACT.md` and
  `mechanics/release-support/docs/SESSION_COMPACTION.md`.
- Verify all generated release-manifest paths stay fresh after package moves.
- Keep historical wave docs in `legacy/` unless an active contract still depends
  on them.

## When Time Comes

- Add broader export/import ergonomics only after staged directory, ZIP
  transport, preflight inspection, bundle README, and release smoke are stable.
- Add a compact generated release-support index only after package-local release
  routes become hard to scan from existing docs.
- Route remote distribution or registry work only after GitHub release and local
  archive handoff stop being enough.

## Out Of Scope

- Remote registry authority, runtime deployment truth, downstream repo ownership,
  and public claims not backed by release checks.
- Another packaging-contract bootstrap when the current release-manifest
  contract is the right surface to deepen.
