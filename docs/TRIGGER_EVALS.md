# Trigger evals and collision tests

This wave replaces the first-wave trigger CSV with a richer JSONL dataset.

## Why the format changed

The old shape was enough for a first pass.
It was not enough for policy-aware evaluation.

We now need to distinguish:

- explicit invocation
- implicit positive routing
- adjacent negative controls
- collision prompts against nearby skills
- explicit-only skills that should require manual invocation even when the semantic match is strong

## Dataset fields

Each JSONL object includes:

- `case_id`
- `skill_name`
- `mode`
- `expected_behavior`
- `expected_skill`
- `competing_skills`
- `invocation_mode`
- `prompt`
- `note`

## `expected_behavior`

Possible values:

- `invoke-skill`
- `do-not-invoke-skill`
- `manual-invocation-required`

`manual-invocation-required` is the key addition for explicit-only skills.

## Collision families

The collision matrix groups the skills most likely to blur together.
These prompts are designed to reveal description drift and routing overlap, not just activation success.

## Maintenance rule

When any of these change, update the trigger evals in the same pull request:

- skill description
- invocation mode
- a major trigger boundary
- a major “do not use” boundary
- overlay activation conditions

Then run:

```bash
python scripts/lint_trigger_evals.py --repo-root .
```
