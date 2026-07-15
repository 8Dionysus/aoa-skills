# AGENTS.md

## Applies to

This card applies to `config/`.

## Role

`config/` owns the small machine-readable policy inputs for portable export,
pack profiles, host adapters, and validation command sequences.

## Read before editing

Read root `AGENTS.md`, `config/README.md`, the consuming builder, and the
schema or test that protects the changed contract.

## Boundaries

Config is behavior. Do not promote a bundle, widen trust, hide an unavailable
dependency, or add a secret through config. Semantic meaning belongs in
capability or skill source; config may only adapt or select it explicitly.

## Validation

Run the direct consumer, its focused invariant tests, and the relevant lane in
`validation_lanes.json`. Manual outcome evidence is still required for any
lifecycle claim.

## Closeout

Report policy behavior changed, consumer rebuilt, manual case if applicable,
checks, and remaining compatibility risk.
