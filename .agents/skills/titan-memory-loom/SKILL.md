---
name: titan-memory-loom
description: 'Explicit activation required: do not invoke or load this skill from an implicit match; wait for explicit user or operator invocation or a source-authorized parent-route selection. Initialize or update Titan Memory Loom records as candidate memory with source refs, confidence, and authority warnings. Use when a Titan service-cohort route needs this explicit bounded step. Do not use for hidden background agents, silent mutation, unreviewed proof sovereignty, or memory canonization without owner confirmation.'
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: project
  aoa_status: scaffold
  aoa_invocation_mode: explicit-only
  aoa_source_skill_path: skills/project/titan/titan-memory-loom/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0053,AOA-T-0043,AOA-T-0045
  aoa_portable_profile: codex-facing-wave-3
---

# titan-memory-loom

## Intent
Use this skill to ingest Titan receipts or events into candidate-grade remembrance records.

## Trigger boundary
Use this skill when:
- a Titan receipt or event should become recallable later
- cross-session digest needs candidate memory entries
- Mneme needs provenance-preserving memory posture

Do not use this skill when:
- memory would be canonized without owner confirmation
- the input lacks source refs
- redaction or retention policy has not been considered for sensitive material

## Inputs
- receipt or event source
- bearer id or Titan name
- source refs
- confidence note
- redaction or retention hints

## Outputs
- candidate remembrance record
- recall authority warning
- source and confidence fields
- redaction or tombstone candidates
- digest note

## Procedure
1. identify receipt, event, or closeout sources that may become recall candidates
2. extract only bounded memory facts with source refs and confidence
3. mark every record as candidate unless an owner surface has confirmed it
4. attach redaction, retention, or tombstone hints when risk is visible
5. return recall limits and verification routes with the candidate records

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
- AOA-T-0053 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/local-first-session-index/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0043 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/capability-boundary/multi-source-primary-input-provenance/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0045 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/history/history-artifacts/witness-trace-as-reviewable-artifact/TECHNIQUE.md` and sections: Intent, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- Extract a Titan-specific reusable technique into aoa-techniques only after repeated reviewed evidence exists; do not add pending IDs as placeholders.
- Keep repo-local command examples in owner docs or examples rather than hard-coding them into skill law.
- If a Titan surface graduates from scaffold to reviewed or evaluated, add review evidence before changing status.
