# Example

## Scenario

A reporting job consumes a summary object from an internal analytics service. The summary must always include a status field, a generated timestamp, and a totals section so downstream consumers can parse the result reliably.

## Why this skill fits

- the important risk is a boundary contract between producer and consumer
- downstream assumptions need to become visible and reviewable
- validation should focus on the interface shape and behavior, not only on internals

## Expected inputs

- the boundary under review and the consuming side
- the required input or output shape of the summary object
- the current smoke or test surface for the boundary
- known downstream expectations that would break if the shape drifts

## Expected outputs

- explicit contract assumptions for the summary boundary
- tests, smoke checks, or validation notes tied to the contract
- a short downstream impact note if the contract is changed or tightened

## Boundary notes

- this example is not a broad redesign of the analytics pipeline
- the point is to make the boundary explicit, not to prove the whole system correct

## Verification notes

- verify that the summary contract is visible in tests or structured checks
- verify that missing required fields fail in a reviewable way
- verify that the report names any unchanged weak spots in downstream coverage
