# Schema District

`schemas/` holds repo-wide machine-readable contracts used by public examples,
generated surfaces, validators, and skill-layer integration artifacts.

Schemas constrain shape. Owning docs, skills, mechanics, builders, and
validators still own meaning.

Mechanic-local schemas may live with a mechanic or part when the contract is
private to that surface. Root schemas remain appropriate when several packages,
tests, generated outputs, or public readers share the same contract.

## Before Editing

1. Identify the owner surface for the meaning.
2. Keep schema changes paired with examples and validators.
3. Do not loosen a schema only to quiet an example.
4. Run `python scripts/validate_skills.py --fail-on-review-truth-sync`.
