---
name: aoa-change-protocol
description: Plan and execute a bounded, non-trivial repository change with explicit verification and reporting. Use when code, config, docs, or operational surfaces change in a meaningful way and the task benefits from an explicit plan. Do not use for trivial wording fixes or when a more specific risk skill fits better.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: canonical
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/aoa-change-protocol/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0001,AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-change-protocol

## Intent
Use a visible, bounded workflow for non-trivial changes so the result remains reviewable and safer.

## Trigger boundary
Use this skill when:
- the change affects code, config, docs, or operational surfaces in a meaningful way
- the task benefits from an explicit plan and verification path
- the task touches more than a trivial wording fix

Do not use this skill when:
- the edit is tiny and has no meaningful review or operational consequence
- a more specific risk skill should be used instead

## Inputs
- target goal
- touched files or surfaces
- main risk
- intended validation path
- rollback idea

## Outputs
- explicit plan
- scoped change
- named verification result
- concise final report

## Procedure
1. state the goal and touched surfaces
2. identify the main risk and think about rollback before editing
3. prepare the smallest reviewable change
4. avoid unrelated cleanup or opportunistic refactors
5. apply the change inside the declared scope
6. run or name explicit verification
7. report what changed, what was verified, and what remains risky

## Contracts
- the change must remain reviewable
- verification must be explicit, not implied
- the change should stay inside the declared scope
- rollback thinking should exist before apply

## Risks and anti-patterns
- over-formalizing trivial edits
- symbolic verification that creates false safety
- using the report as a substitute for a readable diff
- silently expanding the task during implementation

## Verification
- confirm a plan existed before apply
- confirm the change stayed scoped
- confirm at least one explicit verification step was run or intentionally skipped with explanation
- confirm the report includes outcome and rollback thinking

## Technique traceability
Manifest-backed techniques:
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `5c6f0496edc3c2e74590baa35627c85fe58ef765` using path `techniques/docs/source-of-truth-layout/TECHNIQUE.md` and sections: summary

## Adaptation points
Project overlays should add:
- local source-of-truth files
- local validation commands
- local risk tiers
- approval or review rules
