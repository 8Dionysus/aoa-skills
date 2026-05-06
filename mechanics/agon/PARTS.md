# Agon Parts

Active Agon parts live here. Each part is a functioning route surface, not a
source-file inventory.

## Part map

| Part | Owns | Stronger owner route |
|---|---|---|
| [Workflow Candidate Bridge](parts/workflow-candidate-bridge/README.md) | requested-only bounded workflow candidates behind lawful moves | `Agents-of-Abyss` owns Agon law; `skills/` owns accepted bundles |
| [Candidate Validation Gate](parts/candidate-validation-gate/README.md) | deterministic candidate validation route | generated companions stay weaker than source config and review |
| [Recurrence Observation](parts/recurrence-observation/README.md) | observation-only recurrence route for this component | recurrence cannot activate skills or mutate owners |
| [Epistemic Candidate Boundary](parts/epistemic-candidate-boundary/README.md) | requested-only route for epistemic workflow pressure | proof and epistemic verdicts route to stronger owners; normal bundle review owns acceptance |

## Active part contract

Current Agon parts are README-first active contracts. Add deeper `docs/`,
`checks/`, `scripts/`, or `tests/` only when a part gains a checked artifact or
validation route that needs its own local surface.

## Provenance bridge

Use [PROVENANCE](PROVENANCE.md) when a source route or moved flat-doc path must
be audited. Active part docs should not become source-file inventories.

## Validation

Use the validation lane in [mechanics/agon/AGENTS.md](AGENTS.md#validation).
