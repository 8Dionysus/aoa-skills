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

Use:

```bash
python scripts/validate_agent_skills.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
```

Run `python scripts/build_agent_skills.py --repo-root .` only when a source
change or builder change requires a refreshed export.
