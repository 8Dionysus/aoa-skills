---
name: aoa-decision
description: Route AoA decision-lane work by classifying the task, then select and fully read exactly one find, create, or correct child before that child performs graph lookup or a write, while keeping repo-local decision files authoritative. Use when the task mentions docs/decisions, decision indexes, decision graph, ADRs, changed paths, source-surface rationale, supersession, or cross-repo decision symmetry. Do not stop at the root after naming a child. Do not use for ordinary docs edits, unresolved source-of-truth mapping, or trivial changes that do not need durable rationale.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-decision/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0033,AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-decision

## Intent
Use this skill as the front door for AoA `docs/decisions/` work. It decides
whether the task is to find, create, or correct a decision record, uses the
workspace decision graph as the first lookup path when available, and keeps the
owning repository's decision files and validators as source truth.

## Trigger boundary
Use this skill when:
- the task mentions `docs/decisions/`, decision records, ADRs, decision indexes, decision graph, or decision-lane symmetry
- the user asks which prior decision, source surface, owner boundary, status, supersession, or rationale applies
- a new durable decision record may be needed after a structural, workflow, tooling, source/export, or authority change
- an existing decision note, index metadata, supersession, source-surface list, or generated decision index may need correction
- the work spans more than one AoA repository and graph lookup can reduce context load
- after classification, the selected find, create, or correct child must be fully read before its work begins

Do not use this skill when:
- the task is a normal docs edit with no durable decision-lane implication
- the real question is only source-of-truth ambiguity; use `aoa-source-of-truth-check`
- the real question is only whether a decision should be recorded; use `aoa-adr-write`
- the request is only to summarize code, tests, or release notes without decision rationale
- a repo-local route card forbids changing decision surfaces in the current scope

## Inputs
- user intent, target repository, touched paths, or decision ID when known
- available `aoa_decisions` MCP tools or a local graph builder fallback,
  including status, issues, changed-path, source-surface, owner-surface, and
  repo-symmetry packets
- repo-local `docs/decisions/AGENTS.md`, `README.md`, `TEMPLATE.md`, generated indexes, and nearest existing records
- optional `.aoa` session evidence through `aoa-session-memory-evidence-route`
  when the question asks how a decision, decision tool, correction, or impact
  path was used in prior sessions; prefer a usage-chain packet when the
  question is about usage, outcomes, consequences, recurrence, or nearby errors
  for a stable decision/tool/path anchor
- source surfaces that the decision record explains
- validation commands from the owning repository

## Outputs
- one chosen route: `aoa-decision-find`, `aoa-decision-create`, or `aoa-decision-correct`
- compact graph or source context used for the route decision
- explicit owner repository and source-truth surface
- validation path for any write or correction
- stop line when the graph is stale, missing, or not authoritative enough

## Procedure
1. classify the task:
   - find or understand: use `aoa-decision-find`
   - create or record a new rationale: use `aoa-decision-create`
   - correct, supersede, reindex, or repair metadata: use `aoa-decision-correct`
2. immediately select and fully read exactly one classified child before any
   graph query, source lookup, or write. The child owns the detailed route from
   this point. A find or understand task that stops at `aoa-decision`, or runs
   decision-graph lookup from the root without loading `aoa-decision-find`, is
   incomplete. Do not load the other two children.
3. through the selected child, use the `aoa_decisions` MCP first when it is
   available; request status and
   the smallest relevant packet before broad file reads:
   - graph health and blockers: `aoa_decisions_status` and
     `aoa_decisions_issues`
   - touched path: `aoa_decisions_changed_path`
   - source surface: `aoa_decisions_source_surface`
   - owner surface: `aoa_decisions_owner_surface`
   - repo comparison: `aoa_decisions_repo_symmetry`
   - decision ID or known record: `aoa_decisions_decision`
   - repo slice when the target repo is known: `aoa_decisions_repo`
4. use `aoa_decisions_search` only after the status/issues and the relevant
   changed-path, source-surface, owner-surface, repo, or decision packet is
   missing, stale, or too narrow; split a long natural-language request into
   smaller anchors before broad search
5. when the user asks about prior session behavior, correction history, tool
   usage, impact evidence, or "what happened after", use
   `aoa-session-memory-evidence-route` or the equivalent read-only
   `aoa-session-memory-mcp` packet after the decision graph route; for a stable
   decision/tool/path anchor, ask for `usage-chain` first when the question is
   how it was used, what happened after, or which failures/consequences
   followed; use `entity-dossier` when source identity,
   graph/cooccurrence/timeline context, related entities, or a heavier human
   packet is needed; expand only if the first packet is stale, truncated,
   missing refs, or too coarse; treat the packet as evidence refs only, then
   return to repo-local decision files for truth
6. if MCP is unavailable, locate `abyss-stack` in the current workspace or a
   known local checkout, then run its graph builder, such as
   `python <abyss-stack>/scripts/build_workspace_decision_graph.py --check --json`
7. if graph lookup is unavailable too, use repo-local `rg` and generated
   decision indexes, then read the source decision notes directly
8. before any write, read the target repo's decision route card and template;
   if `issue_count > 0`, inspect `aoa_decisions_issues` and do not write in a
   repo whose decision lane has unresolved graph issues
9. after any write, run the repo-local decision-index generator/check and then
   refresh or check the workspace graph and decision-graph lane when available
10. report the source decision file, graph freshness posture, validation run, and
   any remaining owner-route risk

## Contracts
- the graph accelerates lookup; it does not own decision truth
- source files in the owning repository remain stronger than MCP packets,
  generated graph nodes, and generated indexes
- `.aoa` session evidence may explain past usage or impact, but it cannot
  create, accept, supersede, or correct a decision record by itself
- the router chooses one subskill to control cost and avoid conflicting advice
- cross-repo symmetry must be appropriate to the target repo, not forced from a
  sibling template
- no MCP write tool may create, accept, or correct a decision record silently
- stale graph findings must be refreshed or downgraded before they shape a write
- graph issues block writes in the affected repo and downgrade cross-repo
  confidence elsewhere until reported

## Risks and anti-patterns
- treating the workspace graph as an authority instead of a read model
- loading every subskill for a simple lookup
- starting with broad graph search when a changed path, owner surface, source
  surface, repo, or decision ID can produce a smaller packet
- creating a decision note when a lighter source-of-truth or change summary is enough
- copying a sibling decision structure without checking the local owner surface
- updating generated indexes without the source decision note, or vice versa
- failing to refresh the workspace graph after changing decision files

## Verification
- confirm exactly one route was selected
- confirm the selected child was fully read before its graph lookup or write
  procedure began; naming a child without loading it is not a handoff
- confirm `aoa_decisions` was used first when available, or the fallback was named
- confirm graph issue posture was checked before create/correct routes
- confirm broad `aoa_decisions_search` was skipped when a narrower packet was
  sufficient, or explain why it was needed
- if `.aoa` session evidence was used, confirm the usage-chain, dossier, or
  fallback route cited raw/segment/session refs and that decision truth stayed
  with repo-local files
- confirm the owning repository and source decision surface are explicit
- confirm any write uses repo-local route law and validators
- confirm generated indexes and the workspace graph are not treated as source truth
- confirm the final report names validation and any skipped check

## Technique traceability
Manifest-backed techniques:
- AOA-T-0033 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/docs-boundary/decision-rationale-recording/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `3b1d5d623569aa4920b87280d0db0e911d2e29d5` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- stable MCP server name for the current environment
- repo-local decision ID prefix and template
- repo-local decision-index generator and validation commands
- workspace graph output path or fallback builder command
- local stop line for repositories that intentionally do not carry decisions
