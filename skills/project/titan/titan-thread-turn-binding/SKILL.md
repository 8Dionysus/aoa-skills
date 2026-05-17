---
name: titan-thread-turn-binding
scope: project
status: scaffold
summary: Bind Titan bridge events, approvals, and replay state to explicit thread and turn ids for inspectable continuity.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0062
  - AOA-T-0066
  - AOA-T-0045
---

# titan-thread-turn-binding

## Intent

Use this skill to attach Titan bridge events and approvals to a specific thread and turn boundary.

## Trigger boundary

Use this skill when:
- events need a thread-turn identity
- approval or digest state must be scoped to one turn
- replay needs stable continuity keys

Do not use this skill when:
- thread or turn identifiers are missing
- the binding would collapse multiple sessions into one record
- binding would grant execution authority by itself

## Inputs

- thread id
- turn id
- event ids or payloads
- receipt ref
- bridge or console state path

## Outputs

- thread-turn binding record
- scoped event list
- approval refs
- replay key
- continuity warning

## Procedure

1. identify the thread id, turn id, receipt refs, and event refs being connected
2. bind approvals and replay state to explicit turn boundaries
3. flag missing, duplicate, or out-of-order thread and turn evidence
4. keep derived continuity state subordinate to bridge and receipt sources
5. return the binding packet and the next inspection or repair path

## Contracts

- The skill is explicit-only and must not be invoked as hidden background behavior.
- Titan role, helper/control-plane, runtime implementation, memory, proof, and public-runbook authority stays in owner repositories: aoa-agents, aoa-sdk, abyss-stack, aoa-memo, aoa-evals, and 8Dionysus.
- Receipts, bridge ledgers, console state, replay artifacts, approval records, and memory records are witnesses or candidates, not final owner truth.
- Forge mutation and Delta judgment gates must remain distinct, operator-visible, and receipt-linked.
- Missing source refs, missing approval, missing validation, or unclear owner route must be named as stop conditions.

## Risks and anti-patterns

- treating Titan vocabulary as permission to widen authority
- letting receipt, replay, console, or bridge state replace owner-repo evidence
- auto-approving Forge or Delta because a plan looks plausible
- promoting candidate memory, approvals, replay, or receipts into canon without owner review
- using the skill for an ordinary repo task that has no explicit Titan route

## Verification

- confirm direct skill invocation or explicit Titan service-cohort request is present
- confirm lane, gate, source refs, and owner surface are named when relevant
- confirm Forge or Delta locked or allowed state matches recorded approval evidence
- confirm generated artifacts are marked witness, candidate, derived, or advisory rather than final truth
- confirm next validation, replay, repair, or owner-route follow-up is named before continuation

## Technique traceability

Manifest-backed techniques:
- AOA-T-0062 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/continuity/handoff-continuation/episode-bounded-agent-loop/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0066 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/transcript-replay-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0045 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/witness-trace-as-reviewable-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
