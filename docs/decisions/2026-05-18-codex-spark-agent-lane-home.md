# Codex Spark Agent Lane Home

Status: accepted
Date: 2026-05-18

## Context

`aoa-skills` still had a root `Spark/` directory with a small local route card
and swarm note.

That material is agent-facing operating guidance. It is not a public root
entry surface, canonical skill bundle, mechanic package, generated reader
surface, portable skill export, or review evidence.

`Agents-of-Abyss` and `aoa-techniques` already moved Spark into
`.agents/spark/`, where model-facing lanes belong.

## Decision

Move the Spark lane to:

```text
.agents/spark/
```

Build it as a registry-backed Codex Spark fast-session lane for
GPT-5.3-Codex-Spark style work.

The lane owns launch, result, handoff, validation, and scenario packets for
short-loop skill-layer work. It does not own canonical skill meaning.

## Consequences

- The repository root no longer has a standalone `Spark/` directory.
- `.agents/` owns both the generated portable skill pack and the Spark
  agent-facing lane.
- Spark sessions must choose one registered scenario and finish as `done` or
  `handoff`.
- Release checks validate the Spark lane shape.
- Durable skill meaning remains in `skills/**`, source config, mechanics,
  builders, review records, and sibling owner repositories.

## Source Surfaces

- `.agents/AGENTS.md`
- `.agents/spark/AGENTS.md`
- `.agents/spark/README.md`
- `.agents/spark/SWARM.md`
- `.agents/spark/registry.json`
- `.agents/spark/scenarios/**`
- `.agents/spark/scripts/validate_spark_lane.py`
- `.agents/spark/tests/test_spark_lane.py`
- `scripts/release_check.py`
- `scripts/validate_agents_design.py`

## Follow-Up Route

If Spark scenarios start carrying durable process law, move that law to the
owning skill bundle, mechanic package, root surface, or sibling repository.
If the lane becomes model-agnostic, make a new decision before renaming
`.agents/spark/`.
