---
name: titan-summon
scope: project
status: scaffold
summary: Begin an explicit Titan service-cohort session with Atlas, Sentinel, and Mneme active and Forge or Delta locked.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0060
  - AOA-T-0058
  - AOA-T-0028
---

# titan-summon

## Intent

Use this skill to begin a local coding-agent session with the first Titan service cohort after an explicit operator summon.

## Trigger boundary

Use this skill when:
- the operator explicitly requests the Titan cohort
- the session needs Atlas route, Sentinel risk, and Mneme provenance lanes
- Forge and Delta must remain locked until later gates

Do not use this skill when:
- the request asks for hidden background agents
- Forge should mutate before a target and validation exist
- Delta should issue final truth without bounded evidence

## Inputs

- workspace root
- summon prompt reference
- operator intent
- receipt output path
- initial route question

## Outputs

- summon receipt candidate
- active and locked roster state
- route, risk, and memory posture summary
- gate status
- next move

## Procedure

1. confirm explicit operator summon intent and workspace root
2. read the relevant owner docs or runbook refs for current Titan posture
3. create or update the summon receipt candidate
4. activate Atlas, Sentinel, and Mneme as service lanes only
5. keep Forge and Delta locked until separate mutation or judgment gates exist
6. return route, risk, memory posture, gate status, and the next move

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
- AOA-T-0060 from `8Dionysus/aoa-techniques` at `fe4b04ed877916c46e60e70aaa9a1d4c86e81b6e` using path `techniques/continuity/handoff-continuation/session-opening-ritual-before-work/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0058 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/continuity/handoff-continuation/receipt-confirmed-handoff-packet/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0028 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/execution/agent-workflows-core/confirmation-gated-mutating-action/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Validation

## Adaptation points

- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
