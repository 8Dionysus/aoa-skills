---
name: titan-runtime-gate
scope: project
status: scaffold
summary: Activate Forge mutation or Delta judgment lanes only through matching explicit runtime gates on a Titan receipt.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-0028
  - AOA-T-0058
  - AOA-T-0091
---

# titan-runtime-gate

## Intent

Use this skill when a Titan session needs to activate Forge or Delta from locked to gated state.

## Trigger boundary

Use this skill when:
- Forge needs a mutation gate
- Delta needs a judgment gate
- a receipt must record lane activation before proceeding

Do not use this skill when:
- Atlas, Sentinel, or Mneme are being gated unnecessarily
- Forge is requested with judgment or Delta with mutation
- the receipt does not exist

## Inputs

- receipt path
- requested Titan
- gate kind
- intent text
- operator approval ref

## Outputs

- updated gate state
- allowed or blocked decision
- receipt event
- lane summary
- next validation step

## Procedure

1. identify whether the requested runtime lane is Forge mutation or Delta judgment
2. bind the lane request to a receipt, operator approval, and bounded evidence packet
3. keep unmatched or stale approvals from opening the wrong lane
4. fail closed when the gate kind, actor, target, or validation is ambiguous
5. record allowed, blocked, or pending state with the next owner-visible step

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
- AOA-T-0028 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/execution/agent-workflows-core/confirmation-gated-mutating-action/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Validation
- AOA-T-0058 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/continuity/handoff-continuation/receipt-confirmed-handoff-packet/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0091 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/proof/owner-truth-closeout/workspace-root-ingress-and-mutation-gate/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
