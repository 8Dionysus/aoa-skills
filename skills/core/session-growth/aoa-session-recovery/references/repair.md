# Repair mode

### Mode: repair

Use only with a reviewed `session-diagnosis`. Return one
`repair-cycle-result`; do not manufacture missing diagnosis or authorization.

## Required output

- `diagnosis_ref`, `target_owner`, `target_surface`, and `smallest_diff`
- `execution_posture`: one value from `contract.yaml`
- `authorization`: user intent, owner policy, and required runtime approval
- `checkpoint`: pre-change identity, state, evidence, and restore anchor
- `rollback`: executable reversal, trigger, owner, and proof of availability
- `health_contract`: affected behavior, pre-state, post-change checks, acceptance
  and regression boundaries
- `attempt_limit`, `stop_conditions`, `cleanup`, and `escalation`
- `actions`: planned and actually executed actions kept distinct
- `effects`: observed writes or runtime changes, not intended effects
- `health_evidence`: actual commands/observations and outcomes, or explicit
  `not_run`; `verified` is illegal when this is missing or failed
- `result`, `remaining_uncertainty`, `next_route`, and `stop_line`

## Procedure

1. Confirm the diagnosis is reviewed, bounded, and names one target owner. If
   not, return `blocked_missing_diagnosis` or `handoff_required`.
2. Choose the smallest diff and state the initial posture. A plan is `proposed`;
   a fully executable packet with known binding/checkpoint/rollback is
   `prepared`; neither means the change happened.
3. Before mutation, resolve user authorization, owner policy, runtime approval,
   available binding, bounded attempt limit, checkpoint, rollback trigger, and
   health contract. Missing any required field blocks execution.
4. If the request authorizes execution and the binding is available, capture the
   checkpoint, set `executing`, apply one bounded change, and record actual
   effects. Use the target owner's native tools and checks.
5. Set `executed` only after the action completed. Run the affected manual health
   checks and nearby regression checks; command success alone is not health.
6. Set `verified` only when post-state evidence satisfies the health contract.
   On failure or stop condition, execute rollback, verify restored health, set
   `rolled_back` or `blocked`, and preserve the evidence.
7. Remove temporary scaffolding and state anything intentionally retained. If
   the repair grows across owners or becomes a scenario rollout, stop and hand
   off rather than widening silently.
8. If requested, prepare a bounded observation handoff for the statistics owner;
   it describes the cycle but grants no repair or proof authority.

## Stop boundary

Finish at the strongest actually evidenced posture. Never upgrade posture from
wording, intention, diff presence, command exit, or an unrelated green check.
