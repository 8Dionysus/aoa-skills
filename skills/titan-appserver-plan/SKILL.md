---
name: titan-appserver-plan
scope: project
status: scaffold
summary: Generate an inspectable Titan app-server launch plan as JSONL or equivalent plan output without executing Codex.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-TITAN-GATE-DISCIPLINE
  - AOA-T-PENDING-TITAN-RECEIPT-LINEAGE
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

1. collect the requested bridge launch shape
2. write or return only plan entries
3. include receipt and approval refs
4. state that no Codex process was started
5. name the validation command or manual check

## Contracts

- The skill is explicit-only and must not be invoked as hidden background behavior.
- Titan receipts, bridge ledgers, console state, and memory records are witnesses, not final owner truth.
- Forge mutation and Delta judgment gates must remain distinct and visible.
- Owner-repo validation and human judgment remain stronger than the local skill output.

## Risks and anti-patterns

- treating Titan vocabulary as permission to widen authority
- letting receipt or replay state replace owner-repo evidence
- auto-approving Forge or Delta because a plan looks plausible
- canonizing candidate memory without source-owned confirmation

## Verification

- confirm the request and outputs stayed inside the declared Titan lane
- confirm any mutation or judgment gate was explicit and recorded
- confirm source refs, receipt refs, or ledger refs are preserved when available
- confirm the result names stop lines and remaining owner validation needs

## Technique traceability

Pending Titan workflow techniques:
- AOA-T-PENDING-TITAN-GATE-DISCIPLINE
- AOA-T-PENDING-TITAN-RECEIPT-LINEAGE

## Adaptation points

- Replace pending technique refs with published aoa-techniques refs after the Titan workflow techniques are promoted.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into the skill law.
- If a Titan surface graduates from scaffold to reviewed, add review evidence before changing status.
