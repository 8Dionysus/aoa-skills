# Seventh wave

Wave 7 turns activation quality into a first-class, testable surface.

## What changes here

Until now the repo already had trigger evals, collision matrices, and strong skill bodies.
The quiet gap was that the evaluation story was still easier to read as a general routing harness than as a strict test of the `description` field itself.

Wave 7 closes that gap by adding a dedicated description-first eval lane and a soft open-standard conformance lane.

## Additions

- `scripts/build_description_trigger_evals.py`
- `scripts/lint_description_trigger_evals.py`
- `scripts/run_skills_ref_validation.py`
- `config/description_trigger_eval_policy.json`
- `generated/skill_description_signals.json`
- `generated/description_trigger_eval_cases.jsonl`
- `generated/description_trigger_eval_cases.csv`
- `generated/description_trigger_eval_manifest.json`
- `generated/skills_ref_validation_manifest.json`

## Why this matters

Codex decides whether to load a skill from metadata first.
The main activation surface is the description, not the body.
That means a strong `Trigger boundary` section inside the body is still downstream from the first routing decision.

Wave 7 therefore treats the description as its own contract:

1. index the description into stable signal clauses
2. generate should-trigger and should-not-trigger cases from that surface
3. mirror collision prompts into defer cases for neighboring skills
4. run a soft `skills-ref` conformance lane alongside AoA-specific validation

## Design note

This wave does not replace the older trigger suite.

- wave-2 `skill_trigger_eval_cases.*` remains the seed and regression dataset
- wave-7 `description_trigger_eval_cases.*` is the stricter description-governed activation contract

## Build order

```bash
python scripts/build_agent_skills.py --repo-root .
python scripts/build_runtime_seam.py --repo-root .
python scripts/build_runtime_guardrails.py --repo-root .
python scripts/build_description_trigger_evals.py --repo-root .
python scripts/validate_agent_skills.py --repo-root .
python scripts/lint_trigger_evals.py --repo-root .
python scripts/lint_description_trigger_evals.py --repo-root .
python scripts/lint_pack_profiles.py --repo-root .
python scripts/run_skills_ref_validation.py --repo-root .
```

## Result

The portable layer now has a double spine:

- AoA-internal structural validation
- description-first activation validation plus a soft standards-conformance lane

That makes activation less mystical and more inspectable without introducing a second skill authoring format.
