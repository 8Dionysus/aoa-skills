---
name: aoa-decision-find
description: Find AoA decision records through workspace graph search and impact packets, then verify claims against repo-local source notes and generated decision indexes. Use when prior decision rationale, changed paths, owner surfaces, source surfaces, status, or supersession links are needed before work continues. Do not use when the task is to create or edit a decision record.
license: Apache-2.0
compatibility: Designed for Codex or similar coding agents with repository file access and an interactive shell. Network access is optional and only needed when repository validation or referenced workflows require it.
metadata:
  aoa_scope: core
  aoa_status: evaluated
  aoa_invocation_mode: explicit-preferred
  aoa_source_skill_path: skills/core/engineering/aoa-decision-find/SKILL.md
  aoa_source_repo: 8Dionysus/aoa-skills
  aoa_technique_dependencies: AOA-T-0002
  aoa_portable_profile: codex-facing-wave-3
---

# aoa-decision-find

## Intent
Use this skill to find decision rationale quickly across AoA repositories while
keeping final claims grounded in the owning repository's authored decision note.

## Trigger boundary
Use this skill when:
- the user asks what decision exists, which record explains a route, or why a boundary was chosen
- a task needs relevant prior decision context before editing code, docs, validation, MCP, skill, or repo topology
- a cross-repo comparison needs decision IDs, owner surfaces, source surfaces, statuses, or supersession links
- graph search can prevent broad manual reads across many decision lanes

Do not use this skill when:
- a new decision note must be written; use `aoa-decision-create`
- an existing note or metadata must be edited; use `aoa-decision-correct`
- the task is only source-of-truth mapping outside decision records
- the user needs a final architectural decision that has not been made yet
- the graph or indexes are enough for lookup but the answer would require source-note verification and no source read is possible

## Inputs
- query terms, touched paths, target repository, decision ID, source surface, or owner surface
- `aoa_decisions` MCP search, packet, changed-path, source-surface,
  owner-surface, repo-symmetry, issue, repo, decision, or summary tools when available
- fallback generated graph files or repo-local decision indexes
- source decision notes for final verification

## Outputs
- ranked decision matches with repo, decision ID, path, status, and reason for relevance
- source-note refs used for any claim
- note when graph data is stale, missing, or only a candidate hint
- next route if creation or correction is needed

## Procedure
1. query `aoa_decisions` first when available; choose the narrowest packet:
   changed-path for touched files, source-surface for cited inputs,
   owner-surface for ownership routes, repo for a known target repository, and
   decision for a known ID
2. check status or issues; if `issue_count > 0`, report the graph issue posture
   and treat graph matches as candidates until source notes are inspected
3. use broad graph search only when no changed path, source surface, owner
   surface, repo, or decision ID can narrow the route, or after those packets
   fail to produce a sufficient candidate; split long free-text intent into
   smaller anchors before searching
4. if MCP is unavailable, use the latest workspace graph output or repo-local
   generated indexes as a search aid
5. read the source decision note before making a rationale, authority, or
   supersession claim
6. compare source-surface lists and owner metadata against the user's target
   paths when judging relevance
7. distinguish exact matches, likely matches, weak analogies, and missing
   records
8. if no adequate record exists, route to `aoa-decision-create`; if a record is
   stale or wrong, route to `aoa-decision-correct`
9. return compact evidence: decision ID, source path, key reason, and remaining uncertainty

## Contracts
- MCP packets and graph nodes are hints until checked against source notes
- source-note claims must cite the repo and decision path
- related sibling decisions are examples, not templates to copy blindly
- missing evidence should be reported as missing, not filled with doctrine
- avoid loading unrelated decision lanes after a sufficient match is found
- graph issues reduce confidence; they do not authorize guessing

## Risks and anti-patterns
- over-answering from generated graph fields without opening the source record
- using broad graph search before available path, repo, surface, or decision
  anchors
- treating a title match as semantic equivalence
- ignoring supersession or status fields
- turning a weak sibling analogy into a target-repo rule
- searching every repo when a repo or path already narrows the route

## Verification
- confirm graph or fallback lookup path was used
- confirm changed-path/source/owner packet was used when the input made one available
- confirm broad search was needed, or skipped because a narrower packet was sufficient
- confirm final claims came from source notes, not only generated graph data
- confirm match confidence and any uncertainty are visible
- confirm missing or stale records route to create or correct instead of being hidden
- confirm the answer stays compact enough for the current task

## Technique traceability
Manifest-backed techniques:
- AOA-T-0002 from `8Dionysus/aoa-techniques` at `cd276f040d55d490bd015b8698c7a5d594b9f875` using path `techniques/instruction/docs-boundary/source-of-truth-layout/TECHNIQUE.md` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points
- MCP server and tool names
- workspace graph cache path
- repo-local index filenames and source-note metadata fields
- source reference format expected by the active chat surface
