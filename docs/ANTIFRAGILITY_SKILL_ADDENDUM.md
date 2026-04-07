# ANTIFRAGILITY SKILL ADDENDUM

This addendum is for future skill bundles that need explicit fallback posture.

It does not replace existing skill contracts. It is a narrow authoring overlay.

## Why this exists

A bounded execution workflow is easier to trust when its failure posture is visible before runtime.

## Suggested additions for relevant skills

Where appropriate, skill authors should make the following explicit:

- `degraded_modes`
- `fallback_tree`
- `re_ground_sources`
- `safe_stop_threshold`
- `mutation_block_conditions`
- `receipt_contract`
- `adaptation_writeback_contract`

These can be implemented as front matter, schema fields, or documented sections depending on current repo conventions.

## Minimal expectations

For any skill that can mutate state or widen authority:

1. name the conditions that trigger degraded behavior
2. name what actions become unavailable or require confirmation
3. name what source-owned receipt should be emitted
4. name what owner-local surfaces remain authoritative during degradation

## Guardrails

- a fallback tree must never silently widen the task
- degraded behavior must remain reviewable
- owner-local meaning still belongs to the owner repo
- later adaptation should be cited explicitly, not implied

## Wave 1 note

Wave 1 does not require a full new canonical skill bundle here.
A light authoring addendum is enough to prepare later adoption.
