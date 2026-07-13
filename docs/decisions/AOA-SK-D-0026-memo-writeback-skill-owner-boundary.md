# Memo Writeback Skill Owner Boundary

- Decision ID: AOA-SK-D-0026

## Index Metadata

- Original date: 2026-05-25
- Surface classes: memory/writeback, skill source, agent route
- Skill lanes: core/session-growth
- Mechanic parents: growth-cycle
- Guard families: memo writeback, source topology
- Posture: accepted memo writeback skill boundary

Date: 2026-05-25

Status: accepted

## Context

OS Abyss needs agents far from `aoa-memo` to notice when lived session evidence
should become a memory candidate, reviewed-intake export, or explicit
no-writeback stop line.

The pressure came from a gap between raw session truth and durable reviewed
memory: PRs, diffs, and commits show what landed, but the reason a route,
failure correction, owner-boundary clarification, or service contract matters
often lives in `.aoa` session evidence.

Several owner surfaces are involved:

- `.aoa` owns raw and generated session evidence.
- source repositories own local `memo/` ports and source refs.
- `aoa-memo` owns durable reviewed memory objects and generated read models.
- `aoa-evals` owns proof and memory-quality evaluation, not memo writeback
  procedure.
- `aoa-skills` owns reusable agent-facing execution workflows.

## Decision

Add `aoa-memo-writeback` as a core session-growth skill in `aoa-skills`, and
include it in the `project-core-session-growth-v1` kernel rather than leaving it
as a merely installed companion skill.

The skill owns the reusable agent procedure for deciding whether a live session,
closeout, PR, commit, review, or generated recall gap should route to:

- a local memo candidate,
- a reviewed-intake export packet,
- a route-only writeback-debt note,
- a needs-owner-review stop,
- or an explicit no-writeback stop line.

Keep the skill in `skills/core/session-growth/`, not in `aoa-memo`, because the
agent procedure must be portable and executable across owner repositories.

Keep `aoa-memo` unchanged for this slice because it already records the durable
authority boundary: local candidates and exports stay in repo-local memo ports,
session evidence stays in `.aoa` until reviewed intake, and durable memory lands
only through `aoa-memo` reviewed corpus validation.

Use suggestion-eligible activation rather than silent invocation. The skill may
surface as a candidate when semantic evidence matches, but writing a local memo
candidate remains an explicit act through the owning repo's memo port. Because
`aoa skills enter` dispatches from the project foundation profile, kernel
membership is required for agents far from memo to see the route without already
knowing the skill name.

## Consequences

- Agents can now find a compact operational route for session-to-memo writeback
  without needing to already know `aoa-memo` internals.
- `.aoa` search and retrieval are treated as evidence handles, not reviewed
  memory authority.
- `aoa-memo` remains the durable reviewed memory organ rather than becoming a
  generic live-session write path.
- `aoa-evals` remains the owner for eval harnesses and memory-quality proof,
  not for writeback workflow execution.
- The portable export, description-trigger evals, tiny-router inputs, skill
  intelligence registry, pack profiles, and support-resource surfaces now
  include the new route.
- The project foundation now exposes memo writeback through the session-growth
  kernel, so workspace dispatch can surface `aoa-memo-writeback` from intent
  text such as local memo port, reviewed intake export, or session evidence refs.
- The live workspace skill install still needs an explicit install/update step
  after source landing before future sessions will see the skill from
  `/srv/AbyssOS/.agents/skills`.

## Verification

Verified through the release lane.

The release check rebuilt generated surfaces, portable exports, trigger evals,
runtime seams, support resources, and tiny-router inputs; then it ran the full
unittest, pytest, AGENTS, skill, agent-skill, support-resource, trigger,
description-trigger, pack-profile, Spark-lane, and generated-surface checks.
