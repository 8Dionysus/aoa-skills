# Spark lane for aoa-skills

This file only governs work started from `Spark/`.

The root `AGENTS.md` remains authoritative for repository identity, ownership boundaries, reading order, and validation commands. This local file only narrows how GPT-5.3-Codex-Spark should behave when used as the fast-loop lane.

If `SWARM.md` exists in this directory, treat it as queue / swarm context. This `AGENTS.md` is the operating policy for Spark work.

## Default Spark posture

- Use Spark for short-loop work where a small diff is enough.
- Start with a map: task, files, risks, and validation path.
- Prefer one bounded patch per loop.
- Read the nearest source docs before editing.
- Use the narrowest relevant validation already documented by the repo.
- Report exactly what was and was not checked.
- Escalate instead of widening into a broad architectural rewrite.

## Spark is strongest here for

- skill-bundle wording and structure cleanup
- technique-traceability refinement
- schema and generated-surface alignment
- targeted docs or test updates
- small anti-pattern, trigger-boundary, or verification-language repairs

## Do not widen Spark here into

- portfolio-wide skill redesign
- rewriting upstream technique meaning here
- rewriting eval doctrine here
- inflating a bounded skill into a playbook-shaped composition

## Local done signal

A Spark task is done here when:

- the skill remains bounded and reviewable
- technique traceability is clearer
- risk and verification posture are explicit
- generated outputs are aligned when touched
- the repo’s documented validation path was used when relevant

## Local note

Spark should treat each skill like a tight workflow contract, not like a place to invent a new canon.

## Reporting contract

Always report:

- the restated task and touched scope
- which files or surfaces changed
- whether the change was semantic, structural, or clarity-only
- what validation actually ran
- what still needs a slower model or human review
