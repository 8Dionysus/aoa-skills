---
name: titan-appserver-plan
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Generate an inspectable Titan app-server launch plan as JSONL or equivalent plan output without executing the local coding agent. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/project/titan/titan-appserver-plan/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0004,AOA-T-0091,AOA-T-0045
  aoa_portable_profile: codex-facing-wave-3
---

# titan-appserver-plan

## Intent
Use this skill to produce a launch plan for a Titan app-server route while leaving execution to a later explicit operator action.

## Trigger boundary
Use this skill when:
- the operator wants a visible app-server launch plan
- a console needs bridge startup commands described but not run
- risk posture requires dry-run planning before runtime action

Do not use this skill when:
- the request asks to start the server now
- required workspace or receipt refs are missing
- the plan would include secrets or hidden auto-spawn behavior

## Inputs
- workspace root
- console or bridge state ref
- desired endpoint or transport shape
- receipt path
- operator intent

## Outputs
- JSONL launch-plan entries
- required prechecks
- approval gates
- non-execution reminder
- validation command suggestion

## Procedure
1. collect workspace root, app-server command, state paths, and safety limits
2. produce a launch plan without starting the server or child agents
3. include expected receipt, bridge, approval, and validation surfaces
4. name operator confirmations required before any runtime process starts
5. return the plan artifact path or inline plan and its stop conditions

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
- AOA-T-0004 from `8Dionysus/aoa-techniques` at `a2be73594193ca1c186161dfe08a88ed19c3f624` using path `techniques/execution/intent-chain/intent-plan-dry-run-contract-chain/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Validation
- AOA-T-0091 from `8Dionysus/aoa-techniques` at `a2be73594193ca1c186161dfe08a88ed19c3f624` using path `techniques/proof/owner-truth-closeout/workspace-root-ingress-and-mutation-gate/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0045 from `8Dionysus/aoa-techniques` at `a2be73594193ca1c186161dfe08a88ed19c3f624` using path `techniques/history/history-artifacts/witness-trace-as-reviewable-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
