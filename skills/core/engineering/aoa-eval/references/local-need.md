# Record an owner-local evaluation need

### Mode: local-need

Use this mode when selection explicitly found no adequate surface and the
target repository already owns an admitted local eval port. The output is
pressure for review, not a suite and not proof.

Required inputs:

- explicit no-fit with rejected alternatives
- target owner and local `evals/PORT.yaml`
- bounded behavior/invariant, touched paths, evidence refs, proof limits, and
  local packet schema/validation route

Procedure:

1. Return `blocked_missing_input` if the no-fit, owner, admitted port, evidence,
   rejected alternatives, or schema cannot be established.
2. Confirm `evals/intake/` is the owner's write surface. If no local port
   exists, return route-only debt; do not invent one.
3. Shape one bounded need packet containing target behavior, evidence refs,
   owner route, rejected alternatives, proposed manual cases, and proof limits.
4. Write only when the request authorizes the owner-local effect; otherwise
   return the complete candidate packet without mutation.
5. Use the existing local-port validator if one already expresses a durable
   owner invariant. Do not create a validator for this packet.
6. Report packet path or candidate, validation posture, and review/design route.

Return a `local-eval-need-packet`. Never write central `aoa-evals/evals/**` or
use central acceptance language.
