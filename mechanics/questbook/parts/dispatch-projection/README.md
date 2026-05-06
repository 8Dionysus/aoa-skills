# Dispatch Projection

## Use When

Use this part when generated quest catalog or dispatch surfaces need to be read,
validated, or kept aligned with source quest obligations.

## Do Not Use When

Do not use this part to author quest meaning in generated files, close quests
through projections, or replace source quest objects.

## Route Check

- Does the generated view derive from source quest objects?
- Is any drift routed back to source?
- Are schemas still validating catalog and dispatch shape?
- Is generated output clearly weaker than source?

## Active Outputs

- generated projection route
- validation cue
- source drift cue
- no generated authority

## Next Route

Use the existing quest catalog and dispatch builders/validators before changing
generated quest projections.

Source doc:

- [Questbook Skill Integration](../../docs/QUESTBOOK_SKILL_INTEGRATION.md)
