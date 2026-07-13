---
name: titan-approval-ledger
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Record explicit operator approval for Forge mutation or Delta judgment gates without treating approval records as owner truth. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/project/titan/titan-approval-ledger/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0028,AOA-T-0045,AOA-T-0058
  aoa_portable_profile: codex-facing-wave-3
---

# titan-approval-ledger

## Intent
Use this skill to record an explicit Titan approval decision for a bounded Forge mutation or Delta judgment gate.

## Trigger boundary
Use this skill when:
- an operator has approved a named Forge or Delta gate
- the approval must be attached to a receipt, console ledger, or bridge ledger
- the next step needs visible approval evidence before execution continues

Do not use this skill when:
- the request has no explicit operator approval
- the action is not tied to a Titan receipt or ledger
- approval is being inferred from silence or convenience

## Inputs
- receipt or ledger reference
- approved Titan lane
- gate kind
- operator intent text
- scope and validation expectation

## Outputs
- approval record candidate
- gate kind and target lane
- source refs for the receipt or ledger
- stop note when the approval is missing or ambiguous

## Procedure
1. identify whether the approval is for Forge mutation or Delta judgment
2. record the operator-visible approval text and timestamp or receipt ref
3. bind the approval to one target, evidence packet, and gate kind
4. mark the approval record as witness evidence rather than owner truth
5. name what remains blocked after the approval, including validation or owner review

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
- AOA-T-0045 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/witness-trace-as-reviewable-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0058 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/continuity/handoff-continuation/receipt-confirmed-handoff-packet/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
