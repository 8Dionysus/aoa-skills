## Prompt

The target repository is not supplied and no selection has established fit or no-fit; decide how to connect evals by inspecting existing local and central surfaces before apply, local-need, design, or session-mining.

## Expected selection

use

## Why

Decision: use `aoa-eval`, then `aoa-eval-select`. Unknown fit and missing target
evidence require selection; they do not authorize local intake.

## Expected object

One selection route or a bounded `blocked_missing_input` result from
`aoa-eval-select`; no local intake packet is created from missing evidence.

## Boundary notes

`aoa-eval-local-need` becomes eligible only after selection explicitly proves
that no existing eval, validator, test, or script fits.

## Verification hooks

Check that the router loads `aoa-eval-select`, names the missing target evidence
if selection cannot finish, and does not infer no-fit from absence alone.
