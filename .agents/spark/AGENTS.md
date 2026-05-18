# AGENTS.md

## Applies to

This card applies to `.agents/spark/` and all descendants unless a nearer
`AGENTS.md` narrows the path.

## Role

`.agents/spark/` is the fast, interruptible Codex Spark lane for `aoa-skills`.

It is calibrated for GPT-5.3-Codex-Spark style work: short-loop edits, tight
audits, quick checks, and portable handoff packets.

Spark is an agent lane, not a skill bundle, mechanic package, generated truth,
proof authority, release authority, or sibling-owner surface. Its core
execution rule is `done-or-handoff`.

## Read before editing

Read root `AGENTS.md`, `.agents/AGENTS.md`, `DESIGN.AGENTS.md`,
`.agents/spark/README.md`, this card, `.agents/spark/registry.json`, and the
scenario `README.md` plus `PROMPT.md` for the lane being touched.

If a change touches a skill bundle, read `skills/AGENTS.md`, the target
`SKILL.md`, the target `techniques.yaml`, and the nearest support artifacts or
tests before editing.

Read `SPARK_EXTRAPOLATION_NOTEBOOK.md` when changing the lane contract,
scenario set, validator, tests, or release-check wiring.

## Boundaries

- Choose exactly one registered scenario from `.agents/spark/registry.json`.
- Keep one bounded scope per Spark loop.
- End as `done` or `handoff`; do not depend on an in-session switch to a larger
  model.
- Do not run broad tests automatically. Run validation when the user,
  scenario, or repo law asks for it; otherwise name skipped checks honestly.
- Do not let Spark-specific vocabulary become core skill wording.
- Do not use Spark to promote a skill status, invent technique truth, claim
  proof, compose playbooks, define role contracts, create memory objects, or
  alter runtime state.
- Do not hand-edit generated or exported surfaces as source truth.

## Validation

For Spark lane changes, include:

```bash
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
python scripts/validate_agents_design.py
```

For release-facing lane changes, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the restated task and touched scope, scenario chosen, files changed,
whether the change was semantic, structural, or clarity-only, validation run,
validation skipped, remaining risk, and what still needs a slower model or
human review.

## Scenario Law

Every scenario must be registered in `.agents/spark/registry.json` and must
provide:

- `README.md` with scope, done signal, stop-line, and handoff route
- `PROMPT.md` that can launch a standalone Spark session
- `templates/result.md`
- `templates/handoff.md`
- `examples/result.example.md`

## Spark Posture

Spark is strongest here for bounded skill audits, one-bundle refinements, thin
overlay scouting, portable export checks, concrete diff review, registry sync,
small tests, and release-prep passes.

Escalate when the task needs multi-hour architecture synthesis, status
promotion, broad repository redesign, cross-repo owner judgment, or durable
law outside the skill layer.
