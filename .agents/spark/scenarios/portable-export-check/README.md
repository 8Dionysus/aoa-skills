# Spark Scenario: portable-export-check

Use `portable-export-check` for read-only checks of generated portable skill
exports under `.agents/skills/`.

## Scope

Read one exported skill, one source skill bundle plus its exported mirror, one
support resource seam, or one adoption-facing pack slice. Editing is out of
scope unless the user explicitly asks for check plus fix.

## Done Signal

Portable export drift is scoped, the canonical source route is named, and the
needed rebuild, validator, or downstream adoption follow-up is clear.

## Stop-line

Do not hand-edit `.agents/skills/*` as canonical skill meaning.

## Handoff Route

Write a handoff when drift requires source-bundle edits, builder changes,
review evidence, downstream owner receipts, or cross-repository adoption work.

## Validation

Use this scenario's `default_validation` entry in `.agents/spark/registry.json`
and the export lane authority in `config/validation_lanes.json`. Rebuild export
surfaces only when a source or builder change requires refreshed portable
output.
