---
name: titan-receipt
scope: project
status: scaffold
summary: Create, validate, note, or close Titan session receipts as witnesses rather than final truth.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0058
  - AOA-T-0045
  - AOA-T-0043
---

# titan-receipt

## Intent

Use this skill to manage local Titan session receipts for summon, gate, note, validation, and closeout steps.

## Trigger boundary

Use this skill when:
- a Titan session needs a receipt
- an existing receipt needs validation or a note
- a gated action or closeout must be attached to receipt state

Do not use this skill when:
- receipt state would be treated as owner truth
- the receipt path is unclear
- notes would contain secrets or unreviewed claims

## Inputs

- workspace root
- operator id
- receipt path
- note or closeout summary
- gate refs or validation command

## Outputs

- created or updated receipt
- validation result
- receipt note
- closeout state
- authority warning

## Procedure

1. identify the session, actor lane, event, or closeout moment being receipted
2. record state, source refs, gate refs, and validation refs as witness evidence
3. distinguish candidate, open, allowed, blocked, and closed receipt states
4. preserve owner-route limits and missing evidence in the receipt body
5. return the receipt path or packet and the next review action

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
- AOA-T-0058 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/continuity/handoff-continuation/receipt-confirmed-handoff-packet/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0045 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/witness-trace-as-reviewable-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0043 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/capability-boundary/multi-source-primary-input-provenance/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
