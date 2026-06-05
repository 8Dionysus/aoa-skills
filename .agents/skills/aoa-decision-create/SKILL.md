---
name: aoa-decision-create
description: Create a new AoA decision record in the owning repository by checking graph status/issues, using impact packets for placement, and following repo-local decision law for the actual source note and indexes. Use when a real structural, workflow, tooling, source/export, MCP, skill, or authority decision needs durable rationale. Do not use when no decision has been made, the change is trivial, the target repo has unresolved graph issues, or an existing note only needs correction.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-decision-create/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0033,AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-decision-create

## Intent
Use this skill when a real structural, workflow, tooling, source/export, or
authority decision needs a durable repo-local `docs/decisions/` note and the
workspace graph should help find the right placement, neighbors, and ID context.

## Trigger boundary
Use this skill when:
- a change creates durable rationale that future agents need before repeating the route
- the owner repository already has or intentionally needs a `docs/decisions/` lane
- graph lookup should identify similar prior decisions, next ID, source surfaces, or symmetry constraints
- a decision note must be created alongside code, docs, MCP, skill, validator, or generated-index changes

Do not use this skill when:
- no decision has been made yet and the work is still option framing
- the change is self-evident and a commit or change summary is enough
- the target repository has no appropriate decision lane and the task does not explicitly add one
- an existing record can be corrected instead; use `aoa-decision-correct`
- the decision would copy another repo's rationale without local owner evidence

## Inputs
- chosen decision and the options that shaped it
- target repository and source surfaces changed by the decision
- graph status, issue packet, changed-path/source-surface/owner-surface packet,
  or search results for related records
- repo-local decision route card, README, template, generated indexes, and latest records
- repo-local decision-index and validation commands

## Outputs
- one new source decision note with canonical ID, status, date, owner surface, index metadata, context, options, decision, rationale, consequences, source surfaces, and follow-up route
- refreshed repo-local generated decision indexes
- refreshed or checked workspace decision graph
- validation summary and any remaining owner-route risk

## Procedure
1. confirm a real decision exists and is worth preserving
2. use `aoa_decisions` status and issues first; if the target repo has graph
   issues, stop and route to correction before creating a new record
3. use changed-path, source-surface, owner-surface, repo, and search packets to
   collect related records and repo decision-lane context
4. read the target repo's `docs/decisions/AGENTS.md`, `README.md`, `TEMPLATE.md`,
   generated index shape, and latest decision records
5. choose the next canonical ID from source files, not from memory alone
6. write the note in the target repo's established format and metadata language
7. name only the source surfaces this decision actually explains
8. keep graph, generated indexes, tests, and runtime evidence as context rather
   than decision authority
9. run the repo-local decision-index generator, then the check form and any
   affected surface validator
10. refresh or check the workspace graph and run the decision-graph lane when available
11. report the new decision path, graph freshness, and validation

## Contracts
- a decision note records why; it does not replace the active source surface
- next ID selection must be verified from source files
- sibling decisions may inform shape, but the target repo owns its own rationale
- generated indexes must be rebuilt from source metadata, not hand-edited as truth
- workspace graph refresh is part of done after creating a record
- unresolved graph issues in the target repo block creation until corrected

## Risks and anti-patterns
- creating process noise for trivial changes
- writing a decision before the choice is actually made
- copying a sibling record and leaving mismatched owner surfaces
- omitting rejected options or consequences when they shaped the choice
- forgetting generated indexes or workspace graph refresh
- using MCP output as if it created or accepted the decision
- creating a new note while unknown decision-lane surfaces are already present

## Verification
- confirm the new record has canonical ID, status, date, owner surface, and index metadata
- confirm source surfaces match the actual diff
- confirm repo-local decision indexes were regenerated and checked
- confirm graph issue posture was checked before writing
- confirm affected validators were run or explicitly skipped with reason
- confirm workspace graph refresh/check and decision-graph lane see the new record

## Technique traceability
Manifest-backed techniques:
- AOA-T-0033 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/docs-boundary/decision-rationale-recording/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- repository-specific ID prefix and numbering
- decision template fields and index metadata vocabulary
- validation commands and generated index builder path
- graph refresh command or MCP refresh tool
