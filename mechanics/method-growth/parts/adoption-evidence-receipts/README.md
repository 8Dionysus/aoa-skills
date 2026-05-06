# Adoption Evidence Receipts

## Use When

Use this part when local adoption needs a reviewable owner decision or receipt
after compatibility and readiness have been checked.

## Do Not Use When

Do not use this part to manufacture consent, replace proof verdicts, skip shadow
evidence, or treat a generated report as adoption authority.

## Route Check

- Which owner decision is being recorded?
- Which evidence refs support readiness, shadow proof, rollback, and retention?
- What authority or decision refs are cited?
- Is the receipt recording acceptance, hold, rejection, escalation, quarantine,
  or retirement pressure?
- Which owner-local surface remains authoritative after the receipt?

## Active Outputs

- `skill_adoption_owner_decision`
- `skill_adoption_receipt`
- evidence-ref cue
- rollback and retention trace
- no proof, runtime activation, or owner truth outside the cited owner

## Next Route

Route regression, retention, and retirement pressure to
[Retention, Regression, Retirement](../retention-regression-retirement/README.md).
Route proof claims to `aoa-evals`, runtime behavior to runtime owners, and
release posture to release-support.
