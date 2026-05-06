# Growth-Cycle Parts

This file is the active map of functioning Growth-cycle parts in `aoa-skills`.

## Part Map

| Part | Local function | Stronger owner route |
|---|---|---|
| [Adaptive Orchestration](parts/adaptive-orchestration/README.md) | separate task execution, closeout, and harvest so rings and skill families are not run mechanically | canonical skills own execution; owner repos own accepted outcomes |
| [Session Kernel Maturity](parts/session-kernel-maturity/README.md) | keep packet and receipt examples bounded after `candidate_ref` already exists | session-growth skills own detail receipts; stronger owners own final truth |
| [Harvest Note Boundary](parts/harvest-note-boundary/README.md) | keep session-harvest notes public-safe and below promotion authority | method-growth, questbook, playbooks, memo, evals, and owner repos own promotion routes |

## Active Part Contract

Every part keeps this active-route shape:

- `## Use When`
- `## Do Not Use When`
- `## Route Check`
- `## Active Outputs`
- `## Next Route`

## Provenance Bridge

Use [PROVENANCE](PROVENANCE.md) when a source route must be audited. Active
part docs should not carry session note inventories or raw histories.

## Validation

Use the validation lane in [mechanics/growth-cycle/AGENTS.md](AGENTS.md#validation)
for package commands.
