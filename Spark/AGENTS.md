# AGENTS.md

## Applies to

This card applies to `Spark/`.

## Role

`Spark/` is a compatibility and companion lane for Spark-facing skill-pack or agent-use surfaces. It may help local agent operation, but it does not own canonical skill truth.

## Read before editing

Read root `AGENTS.md`, `DESIGN.AGENTS.md`, and the nearest Spark README or config before editing. If a change mirrors a skill bundle, read the canonical `skills/**/SKILL.md` first.

## Boundaries

Do not let Spark-specific vocabulary become core skill wording. Keep adapter labels at the edge, and route canonical bundle changes back to `skills/`.

## Validation

Run the nearest Spark-specific check if one exists. Otherwise run `python scripts/validate_agent_skills.py --repo-root .` for skill-pack effects and `git diff --check` for route-card or wording changes.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.

## Spark Posture

Use Spark for short-loop work where a small diff is enough: skill wording,
schema alignment, generated-surface checks, targeted docs, and narrow tests.

Start with a map: task, files, risks, and validation path. Prefer one bounded
patch per loop. Escalate instead of widening into portfolio-scale redesign,
upstream technique rewrites, eval doctrine, or playbook-shaped composition.

A Spark task is done here when the skill remains bounded and reviewable,
generated outputs are aligned when touched, validation was actually run, and
the report says what still needs slower review.
