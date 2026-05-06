# Method-Growth Parts

This file is the active map of functioning Method-growth parts in
`aoa-skills`.

## Part Map

| Part | Local function | Stronger owner route |
|---|---|---|
| [Candidate Lineage](parts/candidate-lineage/README.md) | mint reviewed `candidate_ref` only after donor harvest, while preserving earlier lineage refs | `aoa-sdk` owns provisional carry; final owners own accepted objects |
| [Owner Status Landing](parts/owner-status-landing/README.md) | keep first reviewed owner-local status weaker than final object truth | final owner repo owns landed truth; `Dionysus` owns seed staging |
| [Governed Followthrough](parts/governed-followthrough/README.md) | record one bounded next-step verdict without queue or scheduler authority | owner repo, `aoa-evals`, `aoa-memo`, `aoa-playbooks`, `aoa-stats`, or `Dionysus` owns the next object |
| [Adoption Boundary](parts/adoption-boundary/README.md) | require explicit owner consent, compatibility, shadow proof, rollback, and retention before durable uptake | downstream owner repos own local adoption |
| [Adoption Evidence Receipts](parts/adoption-evidence-receipts/README.md) | record owner decision and adoption receipt posture without manufacturing consent | owner repos own accepted adoption truth; `aoa-evals` owns proof verdicts |
| [Retention, Regression, Retirement](parts/retention-regression-retirement/README.md) | keep adopted behavior under regression, retention, quarantine, and retirement review | owner repos own cleanup; antifragility owns pruning route pressure |
| [Pattern Adoption Handoff](parts/pattern-adoption-handoff/README.md) | route shared patterns toward skill proposals without automatic promotion | `aoa-techniques`, `aoa-skills`, and `aoa-playbooks` own their respective canon |

## Active Part Contract

Every part keeps this active-route shape:

- `## Use When`
- `## Do Not Use When`
- `## Route Check`
- `## Active Outputs`
- `## Next Route`

## Provenance Bridge

Use [PROVENANCE](PROVENANCE.md) when a source route must be audited. Active
part docs should not carry flat docs inventories, raw session history, or old
source labels.

## Validation

Use the validation lane in [mechanics/method-growth/AGENTS.md](AGENTS.md#validation)
for package commands.
