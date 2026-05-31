# Spark Extrapolation Notebook

This notebook records the adaptation pass that moved `aoa-skills` Spark work
from root `Spark/` into `.agents/spark/`.

It is not the daily authority for Spark use. The active contract lives in
`AGENTS.md`, `README.md`, `registry.json`, scenario packets, the validator, and
tests.

## Source Studied

Primary pattern:

- `Agents-of-Abyss/.agents/AGENTS.md`
- `Agents-of-Abyss/.agents/spark/AGENTS.md`
- `Agents-of-Abyss/.agents/spark/README.md`
- `Agents-of-Abyss/.agents/spark/SWARM.md`
- `Agents-of-Abyss/.agents/spark/registry.json`
- `Agents-of-Abyss/.agents/spark/scenarios/**`
- `Agents-of-Abyss/.agents/spark/schemas/**`
- `Agents-of-Abyss/.agents/spark/scripts/validate_spark_lane.py`
- `Agents-of-Abyss/.agents/spark/tests/test_spark_lane.py`
- `Agents-of-Abyss/docs/decisions/2026-05-13-codex-spark-agent-lane-home.md`

Local constraints:

- `AGENTS.md`
- `CHARTER.md`
- `DESIGN.md`
- `DESIGN.AGENTS.md`
- `.agents/AGENTS.md`
- `docs/ARCHITECTURE.md`
- `skills/AGENTS.md`
- `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`
- `mechanics/audit/docs/PUBLIC_SURFACE.md`
- `mechanics/boundary-bridge/docs/LAYER_POSITION.md`
- `SKILL_INDEX.md`

## Pattern Preserved

The center pattern is not just prompt text.

- `.agents/spark/` is the durable home.
- Spark is Codex-model-facing agent material, not a mechanic package or root
  district.
- A Spark loop chooses one registered scenario and one bounded scope.
- The core rule is `done-or-handoff`.
- Each scenario has `README.md`, `PROMPT.md`, result and handoff templates, and
  one result example.
- The registry names scenario paths, prompt refs, packet refs, default
  validation, done signal, and stop-line.
- Results and handoffs have explicit homes, but ordinary closeout stays in the
  conversation or PR unless a packet helps future sessions.
- Validation checks registry shape, scenario files, packet markers,
  registered-vs-discovered parity, and shared release-lane wiring.

## Codex 5.3 Spark Calibration

The lane is shaped for GPT-5.3-Codex-Spark style work: short, interruptible,
real-time coding loops where a small model should either finish the bounded
scenario or leave a portable handoff for a slower session.

Local consequence:

- default to targeted reads, small patches, tight audits, and narrow checks;
- do not turn Spark into a long-running autonomous worker;
- do not require broad tests unless the user, scenario, or repo route asks for
  them;
- do not depend on switching models inside the same Spark session;
- escalate or hand off when the task needs deeper architecture, owner judgment,
  status promotion, or cross-repo synthesis.

## Skill-Canon Adaptation

`aoa-skills` cannot copy the center scenarios blindly. This repository owns
bounded execution workflows, not AoA center doctrine.

Spark here should help with:

- read-only skill audits;
- one-bundle skill refinements;
- project-overlay or mechanic-local scout passes;
- portable export parity checks;
- concrete diff review;
- registry and lane-contract sync;
- small tests for existing contracts;
- release-prep checks before publication or landing.

Spark must not:

- promote skill status by proximity;
- turn a skill into a technique, eval, route, playbook, role, memory object, or
  runtime behavior;
- smuggle private donor residue, host paths, raw logs, or project folklore into
  public skill text;
- hand-edit `.agents/skills/*` as canonical skill meaning;
- treat generated catalogs or exported packs as authored truth;
- invent validation commands not named by the owner surface.

## Local Shape

The adapted lane owns:

```text
.agents/spark/
  AGENTS.md
  README.md
  SWARM.md
  registry.json
  handoffs/
  results/
  scenarios/
    skill-audit/
    skill-refinement/
    overlay-scout/
    portable-export-check/
    diff-review/
    registry-sync/
    test-factory/
    release-prep/
  schemas/
  scripts/validate_spark_lane.py
  tests/test_spark_lane.py
```

The root `Spark/` directory is intentionally retired.

## Scenario Notes

`skill-audit` is read-only and routes findings to bundles, mechanics,
validators, generated builders, or sibling owners.

`skill-refinement` makes one source-backed patch to one existing skill bundle
or thin support surface.

`overlay-scout` maps donor, overlay, legacy, or mechanic-local material before
deeper skill-layer work.

`portable-export-check` inspects `.agents/skills/*` parity and adoption-facing
drift without treating exports as source.

`diff-review` reviews a concrete diff or PR without rewriting it.

`registry-sync` aligns `.agents/spark/` docs, registry, validator, tests, and
release gate.

`test-factory` adds bounded tests for an existing source-backed contract.

`release-prep` checks release readiness without publishing, tagging, pushing,
or merging.

## Future Rule

If Spark scenarios start carrying durable process law, move that law to the
owning skill bundle, mechanic package, root surface, or sibling repository. If
the lane becomes model-agnostic, make a new decision before renaming
`.agents/spark/`.
