# Example

## Scenario

An inventory reservation module tracks `available`, `reserved`, and `total` item counts. The team has a few example tests, but regressions still appear because the rules need to hold across many sequences of reserve and release operations.

## Why this skill fits

- the system has stable truths that should hold across many inputs and states
- example-only testing is too narrow for the risk surface
- the important value comes from expressing invariants, not from enumerating a few happy paths

## Expected inputs

- the invariant candidates, such as `available + reserved = total`
- the current example tests and known edge cases
- the generator or input strategy for reserve and release sequences
- limits needed to keep the property checks reviewable

## Expected outputs

- explicit invariants for the reservation rules
- property-oriented tests or repeated checks over bounded generated inputs
- notes on generator assumptions and what the properties do not cover

## Boundary notes

- this example is not about UI rendering or snapshot-style presentation behavior
- the point is to encode stable truths, not to replace every concrete example test

## Verification notes

- verify that each property expresses a real invariant instead of a weak wish
- verify that the generated cases broaden coverage beyond the original handpicked examples
- verify that the report explains the invariant and the bounds of the generator strategy
