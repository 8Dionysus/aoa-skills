# Recurrence Parts

This file maps current recurrence behavior to active `aoa-skills` parts.
It is not the AoA center recurrence part map and not a generated manifest
inventory.

## Part Map

| Part | Local function | Stronger owner route |
|---|---|---|
| [Live Observation Producers](parts/live-observation-producers/README.md) | name producer inputs that may feed skill review while keeping generated evidence advisory | `Agents-of-Abyss` owns recurrence law; `aoa-evals`, `aoa-stats`, and owner repos own proof, visibility, and accepted follow-through |
| [Review Decision Closure](parts/review-decision-closure/README.md) | close recurrence-fed beacons as review decisions without changing activation behavior | skill bundle, trigger-eval, applicability, or owner surfaces own the actual follow-through |

## Active Part Contract

Every part keeps this active-route shape:

- `## Use When`
- `## Do Not Use When`
- `## Route Check`
- `## Active Outputs`
- `## Next Route`

## Provenance Bridge

Use [PROVENANCE](PROVENANCE.md) when a recurrence source route must be audited.
Active part docs should not carry manifest snapshots, generated outputs, or raw
session history.

## Validation

Use the validation lane in [mechanics/recurrence/AGENTS.md](AGENTS.md#validation)
for package commands.
