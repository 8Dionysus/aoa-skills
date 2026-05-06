# Retention, Regression, Retirement

## Use When

Use this part when an adopted skill or pattern needs regression coverage,
retention watch, quarantine fallback, deprecation, or retirement.

## Do Not Use When

Do not use this part to delete a skill without source-linked evidence, erase
provenance, bypass via negativa review, or declare a proof verdict.

## Route Check

- What regression case protects the adopted behavior?
- What retention signal would keep, hold, quarantine, or retire the adoption?
- Is rollback available before persistent behavior changes?
- Does this need antifragility pruning, audit evidence, owner-local cleanup, or
  release-support handling instead?

## Active Outputs

- `skill_adoption_regression_case`
- `skill_adoption_retirement`
- retention-watch cue
- quarantine or rollback cue
- no deletion approval by itself

## Next Route

Route pruning pressure to `mechanics/antifragility/parts/via-negativa-pruning/README.md`.
Route evaluation proof to `aoa-evals` and release-facing deprecation to
release-support.
