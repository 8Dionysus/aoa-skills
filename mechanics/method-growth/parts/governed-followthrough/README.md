# Governed Followthrough

## Use When

Use this part after reviewed owner-status context exists and the next question
is one bounded decision: land, stage, reanchor, prove, merge, defer, or drop.

## Do Not Use When

Do not use this part as a live queue, scheduler, hidden runner, proof verdict,
seed minter, object minter, or owner acceptance receipt.

## Route Check

- Is `candidate_ref` present?
- Is the owner repo explicit?
- Is the verdict one of the allowed decisions?
- Does the decision say why now?
- Does the decision explain why the nearest wrong target is not the route?
- Are stop conditions explicit?

## Active Outputs

- reviewed route-followthrough decision
- next artifact kind
- approval posture
- stop conditions
- owner, proof, seed, memory, stats, playbook, merge, defer, or drop hint

## Next Route

Send the next object to the named stronger owner. If the verdict later changes,
write a new reviewed decision instead of silently overwriting the old one.

Source doc:

- [Governed Followthrough](../../docs/GOVERNED_FOLLOWTHROUGH.md)
