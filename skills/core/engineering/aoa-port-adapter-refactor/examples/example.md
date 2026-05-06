# Example

## Scenario

A notification workflow directly calls a concrete email provider client from inside application logic. Tests are brittle because they need provider-specific setup, and adding a second delivery channel would repeat the same dependency pattern again.

## Why this skill fits

- the main problem is a concrete dependency leaking into logic that should stay reusable
- the module needs a clearer seam before further change
- tests and future delivery options benefit from a narrower boundary

## Expected inputs

- the target module and the concrete dependency currently embedded in it
- the behavior the core logic actually needs from the dependency
- the desired scope of the refactor
- the validation path that will confirm behavior did not drift

## Expected outputs

- a narrower port that reflects what the core truly needs
- an adapter or equivalent seam around the concrete provider
- a clearer logic-versus-infrastructure boundary
- a short verification summary confirming behavior stayed stable

## Boundary notes

- this example assumes the logic-versus-edge boundary is already clear enough to act on
- the focus is introducing a useful seam, not renaming packages or creating abstraction for ceremony alone

## Verification notes

- verify that the new port is narrower than the original provider API
- verify that infrastructure behavior moved behind the adapter boundary
- verify that the refactor reduces coupling without changing the intended notification behavior
