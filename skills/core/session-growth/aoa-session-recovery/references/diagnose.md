# Diagnose mode

### Mode: diagnose

Use only with a closed and explicitly reviewed evidence boundary. Diagnosis is
read-only and returns one `session-diagnosis`.

## Required output

- `evidence_boundary`: review/closure posture and source refs
- `symptoms`: direct observations, each with refs and freshness
- `causes`: confirmed causes, reviewed inferences, provisional hypotheses, and
  disconfirming evidence kept distinct
- `unknowns`: missing evidence that prevents a stronger causal claim
- `drift_class`: boundary, proof, role, memory, routing, lifecycle, compaction,
  tool/runtime, ownership, or another explicitly defined class
- `owners`: immediate session owner, likely durable owner, and authority limit
- `severity`: only when supported by impact and recurrence evidence
- `repair_shape`: smallest plausible target and why it is not yet execution
- `claim_posture`: `reviewed_observation`, `reviewed_inference`, or
  `provisional_hypothesis` for every meaningful claim
- `effects: [none]`, `next_route`, and `stop_line`

## Procedure

1. Reject live/unreviewed or unbounded inputs as `blocked_unreviewed_evidence`.
2. Inventory symptoms before naming causes. Disposition checkpoint, generated,
   stale, and cross-session material as hints until corroborated.
3. Seek at least one plausible alternative or disconfirming observation for
   every structural cause; preserve `unknown` when evidence cannot decide.
4. Classify the failure and separate the immediate operating surface from the
   owner that can change durable policy or code.
5. Define the smallest plausible repair shape, required checkpoint and health
   surface, but perform no mutation and do not call the diagnosis accepted.
6. If requested, prepare a bounded observation handoff for the statistics owner;
   it remains descriptive and never proves the diagnosis.

## Stop boundary

Stop after one diagnosis. A later repair requires explicit mode selection and a
reviewed diagnosis; do not chain directly into mutation in this invocation.
