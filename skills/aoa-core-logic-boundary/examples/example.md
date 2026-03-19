# Example

## Scenario

A fulfillment module mixes shipping-eligibility rules with HTTP request parsing, retry logic, and audit logging. Reviews keep getting stuck because contributors cannot tell which parts are reusable business rules and which parts are delivery-layer glue.

## Why this skill fits

- the core problem is unclear responsibility between reusable logic and edge behavior
- the module already mixes stable rules with orchestration and I/O detail
- future changes will stay safer if the boundary is clarified before more code is added

## Expected inputs

- the target module or slice with mixed responsibilities
- the current rules that appear stable or reusable
- the surrounding glue, orchestration, and environment-specific code
- the pressure points that make reviews or tests muddy today

## Expected outputs

- a clearer statement of what belongs in the reusable core
- notes on what should remain edge-specific glue
- a bounded refactor proposal or small implementation move
- a short verification summary about improved clarity

## Boundary notes

- this example is about deciding what belongs in the core versus at the edge
- it is not yet about introducing a port around a concrete dependency once the boundary is already clear

## Verification notes

- verify that the stable eligibility rules are separated conceptually from request parsing and logging
- verify that edge-specific orchestration remains outside the reusable core
- verify that the change improves review clarity without expanding into a broad rewrite
