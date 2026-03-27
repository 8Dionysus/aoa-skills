# Description trigger evals

This document defines the wave-7 activation contract.

## Core idea

Skill activation is decided before the model reads the full body.
The description therefore needs its own test surface.

Wave 7 makes that surface explicit by generating:

- a per-skill description signal index
- description-grounded positive cases
- description-grounded negative cases
- mirrored collision prompts that force neighboring skills to defer

## Files

- `generated/skill_description_signals.json`
- `generated/description_trigger_eval_cases.jsonl`
- `generated/description_trigger_eval_cases.csv`
- `generated/description_trigger_eval_manifest.json`

## Case classes

### `explicit-handle`

Direct `$skill-name` invocation.

### `should-trigger`

Implicit route that should activate the skill because the prompt matches its description.

### `manual-invocation-required`

Implicit semantic match for an explicit-only skill.
The model should recognize the fit but require a manual invocation instead of auto-loading the skill.

### `should-not-trigger`

Prompt that falls inside the description's negative boundary.

### `prefer-other-skill`

A mirrored collision case.
The prompt is valid for a neighboring skill, so this skill must defer.

## Coverage rule

Every skill must have:

- one explicit-handle case
- one description-positive case or manual case depending on invocation mode
- one description-negative case
- one defer case when the skill participates in a collision family and supports implicit invocation

## Why mirrored collision cases matter

Single-winner collision prompts are useful, but they only prove who should win.
They do not directly prove who should stay out.
Mirrored defer cases close that hole.

## Relationship to the older trigger suite

The older trigger suite remains valuable as a seed and regression source.
The wave-7 suite is the activation-governed view of that same territory.
