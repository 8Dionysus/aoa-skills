# AGENTS.md

## Applies to

This card applies to `mechanics/release-support/`.

## Role

This package owns portable export identity, profile-scoped staging, directory
and ZIP handoff, install verification, and release guidance for the seven
callable bundles.

## Read before editing

Read root and mechanics cards, `README.md`, the affected release doc,
`config/skill_pack_profiles.json`, the export/pack implementation, release
schema, and generated manifest.

## Boundaries

Authored bundle meaning remains in `skills/`. A portable hash proves byte
identity, not usefulness. Installation does not prove prompt visibility;
prompt visibility does not prove correct selection. Runtime trust and artifact
admission remain with their named owners.

## Validation

Manually inspect a staged directory and ZIP roundtrip, then run export parity,
pack smoke for both profiles, and the release lane when release identity moved.

## Closeout

Report profile, source/portable identity, transports exercised, real install or
clean-home prompt check, release validation, and unverified runtime behavior.
