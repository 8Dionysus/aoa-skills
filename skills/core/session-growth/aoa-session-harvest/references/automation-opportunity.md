# Classify an automation opportunity

### Mode: automation-opportunity

Use when reviewed evidence shows a recurring manual route and the unresolved
question is whether and how far automation is honest now.

1. Isolate the manual route as actually practiced and preserve evidence refs.
2. Classify recurrence, friction, determinism, trigger clarity, input/output
   clarity, proof surface, reversibility, secret coupling, approval sensitivity,
   rollback, and owner boundary.
3. Name the highest honest `automation_mode_posture`: `manual_only`,
   `assistant_draft`, `dry_run_preview`, `human_approved_execution`, or
   `scheduler_seed_candidate`. This is a boundary, never permission.
4. Return `seed_ready` only when trigger, inputs, outputs, risks, bounded
   activation hints, likely owner, and conservative mode are explicit;
   otherwise return `not_now` with the missing condition.
5. Mark `checkpoint_required` for self-change, hidden authority, important
   mutation, or approval-sensitive effects.
6. Choose the first honest next artifact: skill proposal, playbook seed,
   technique/procedure candidate, repair quest, quest, or defer. Reject the
   nearest wrong target.

Return one `automation-opportunity-packet` with every field below:

- `reviewed_evidence`: boundary, review ref, and exact recurrence refs
- `manual_route`: trigger, inputs, action, outputs, friction, and owner
- `readiness`: recurrence, determinism, trigger clarity, input/output clarity,
  proof surface, reversibility, secret coupling, approval sensitivity,
  rollback, and owner-boundary findings
- `automation_mode_posture`: exactly one allowed posture from step 3
- `readiness_verdict`: `seed_ready` or `not_now`, plus every missing condition
- `checkpoint_required`: explicit boolean and reason, including `false` when
  the bounded route is read-only and has no hidden authority
- `next_artifact`: exactly one artifact from step 6 and its review owner
- `rejected_nearest_target`: the closest tempting but unsupported target
- `actual_effects`: always `none`
- `stop_line`: what was not authorized and what separate owner decision would
  be required next

Do not substitute a prose recommendation that omits any packet field. The
packet is not a live schedule, mutation, background job, approval, or hidden
playbook. Optional receipts remain subordinate to an existing stats owner
contract.
