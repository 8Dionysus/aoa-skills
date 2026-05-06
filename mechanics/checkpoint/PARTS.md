# Checkpoint Parts

This file is the active map of functioning Checkpoint parts in `aoa-skills`.

## Part Map

| Part | Local function | Stronger owner route |
|---|---|---|
| [Checkpoint Note Lane](parts/checkpoint-note-lane/README.md) | preserve mid-session evidence, candidate clusters, and review posture without minting candidate truth | `aoa-sdk` owns local carry controls; `Dionysus` may own explicitly promoted reviewed notes |
| [Closeout Bridge Boundary](parts/closeout-bridge-boundary/README.md) | route reviewed checkpoint hints into explicit closeout bridge execution without hiding harvest | `skills/aoa-checkpoint-closeout-bridge/SKILL.md` owns bridge workflow; core session-growth skills own their own steps |

## Active Part Contract

Every part keeps this active-route shape:

- `## Use When`
- `## Do Not Use When`
- `## Route Check`
- `## Active Outputs`
- `## Next Route`

## Provenance Bridge

Use [PROVENANCE](PROVENANCE.md) when a source route must be audited. Active
part docs should not carry runtime checkpoint histories or sibling inventories.

## Validation

Use the validation lane in [mechanics/checkpoint/AGENTS.md](AGENTS.md#validation)
for package commands.
