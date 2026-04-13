---
name: aoa-summon
scope: core
status: scaffold
summary: Delegate one bounded child route through quest-passport law, Codex-first local execution defaults, progression and self-agent gates, governed return, and checkpoint-aware reviewed closeout planning.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-SUMMON-LANE-SELECTION
  - AOA-T-PENDING-SUMMON-RETURN-GOVERNANCE
---

# aoa-summon

## Intent

Use this skill to decide whether and how to launch one bounded child route from
an already-anchored parent route.

The goal is not delegation theater.
The goal is to preserve quest-passport law, Codex-first local execution,
stress narrowing, progression and self-agent gates, return planning,
checkpoint-aware reviewed closeout, and owner-local publication mapping.

## Trigger boundary

Use this skill when:
- a parent route already has a real anchor and named expected outputs
- a narrower child actor would help through bounded review, evaluation, leaf
  implementation, or local verification
- the child result must map back into return, closeout, and owner-publication
  surfaces
- local Codex execution is the honest default unless a separate execution
  surface is actually required

Do not use this skill when:
- the parent route still lacks a real anchor or named outputs
- the route is `d3+` and still needs a split before any child launch
- delegation would widen authority, hide approval posture, or bypass a human
  gate
- the task is asking for a whole orchestration mesh rather than one bounded
  child route
- remote transport is being requested for prestige rather than necessity

## Inputs

- a quest passport with difficulty, risk, control mode, and delegate tier
- a summon request with desired role or child target, transport preference, one
  parent anchor (`route_anchor`, `parent_task_id`, or `session_ref`), and
  named expected outputs
- named expected outputs for the child route
- optional reviewed artifact path, stress bundle ref, checkpoint note ref,
  Codex trace ref, progression overlay ref, self-agent checkpoint ref, and
  audit refs

## Outputs

- one summon decision with allowed or blocked posture
- one chosen lane such as `codex_local_leaf`, `codex_local_reviewed`,
  `remote_reviewed`, `split_required`, or `human_gate`
- `execution_surface`, `cohort_pattern`, `reason_codes`, and `blocked_actions`
- optional `codex_local_target`
- `return_plan`, `checkpoint_bridge_plan`, `memo_export_plan`, and
  `owner_publication_plan`
- `closeout_required`, `checkpoint_required`, and `progression_required`

## Procedure

1. start from the parent anchor and quest passport, not from raw pressure to delegate
2. default `transport_preference` to `codex_local` when the request leaves it open
3. verify that expected outputs are named before picking a lane
4. classify the lane with difficulty, risk, control mode, requested role, and
   `references/passport-lane-matrix.v3.md`
5. keep low-risk `d0_probe`, `d1_patch`, and bounded `d2_slice` leaf work in
   `codex_local_leaf` when anchor and outputs are clear
6. keep local reviewer, evaluator, and architect-like narrowing work in
   `codex_local_reviewed`
7. allow `remote_reviewed` only when a separate endpoint or execution surface
   is actually required
8. if difficulty is `d3+`, return `split_required` instead of launching child execution
9. if stress posture says `stop_before_mutation`, only allow a narrowing
   non-mutating child; otherwise gate to human review
10. if `require_progression` is true or the route depends on reviewed unlock
    posture, require a reviewed progression overlay before summon
11. if the route is self-agent or policy-sensitive, require reviewed
    self-agent checkpoint posture before summon
12. emit return, checkpoint bridge, memo export, and owner publication plans
    that stay subordinate to reviewed closeout and owner truth
13. apply `references/no-raw-traces-rule.md` so child traces remain aids rather
    than proof or memo canon
14. map failed, narrowed, or blocked child states back into return posture
    instead of letting them disappear

## Contracts

- this skill governs one bounded child route; it does not grant hidden
  orchestration authority
- local Codex child targeting is the default first choice, not an afterthought
- stress may narrow or block, but it may never widen authority
- remote transport follows the same passport, return, checkpoint, and closeout
  law as local transport
- `d3+` routes split first
- progression and self-agent gates are real blockers when required evidence is
  missing
- child traces, memos, and receipts do not replace rereading the reviewed
  parent artifact
- terminal publication stays inside canonical owner families, and memo export
  stays reviewed and candidate-oriented
- failed, narrowed, or blocked child results still map into an explicit return
  surface

## Risks and anti-patterns

- treating delegation as progress without anchor or output clarity
- using a remote child route to bypass local proof, approval, or closeout
  posture
- allowing child scope to widen beyond the parent passport
- reading child traces as proof authority or memo canon
- skipping the required split for `d3+` work
- publishing terminal meaning into derived layers before owner-local landing

## Verification

- confirm the passport and parent anchor exist
- confirm expected outputs are named
- confirm the chosen lane matches difficulty, risk, control mode, and requested
  role
- confirm `d3+` routes split before summon
- confirm stress only narrows or blocks
- confirm progression and self-agent gates are not bypassed
- confirm return, checkpoint bridge, and publication plans stay explicit for
  nonterminal or failed child outcomes
- confirm terminal publication stays owner-local and memo export stays reviewed
  and candidate-oriented
- confirm traces stay subordinate to reviewed closeout and parent reread

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-SUMMON-LANE-SELECTION from `8Dionysus/aoa-techniques` at `TBD`
  using path `TBD` and sections: Intent, Inputs, Outputs, Core procedure,
  Contracts, Validation
- AOA-T-PENDING-SUMMON-RETURN-GOVERNANCE from `8Dionysus/aoa-techniques` at
  `TBD` using path `TBD` and sections: Intent, Outputs, Contracts, Risks,
  Validation

## Adaptation points

- project overlays may add local child-role labels, control modes, or transport
  labels
- project overlays may map local reviewed-closeout or checkpoint families onto
  the core summon result without weakening the gates
- project overlays may specialize owner publication families or memo candidate
  classes while keeping the parent return route explicit
