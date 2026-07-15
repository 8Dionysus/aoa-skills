# AGENTS.md

## Applies to

This card applies to `.agents/` and its generated skill export.

## Role

`.agents/skills/` is the flat portable projection of the seven callable source
bundles for compatible agent hosts.

## Read before editing

Read root `AGENTS.md`, `skills/AGENTS.md`, `generated/AGENTS.md`, the portable
layer release doc, and the export builder/validator.

## Boundaries

Do not hand-edit portable bundles as authority. Do not add host-only policy to
core procedure source or infer native prompt visibility from file presence.

## Validation

Change authored source or config, rebuild the export, validate parity, then use
a clean host context for prompt-visible behavior when that claim matters.

## Closeout

Report source bundle, portable files rebuilt, byte parity, host visibility
checked or skipped, and deferred behavior evidence.
