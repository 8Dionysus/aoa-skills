# Skill Collision Chaos Wave 1

This wave stays inside the existing trigger-eval and collision surfaces.
It does not add a new runtime layer to `aoa-skills`.

## What it strengthens

- explicit-only skills that still rank strongly must remain manual
- neighboring skills must be able to defer to the better owning skill
- thin one-off incident prompts must stay out of the match
- stress-era doc overlap must still resolve to source-of-truth mapping before ADR writing
- downstream tiny-router precision should inherit these boundaries instead of improvising a new lane

## Where it lands

The source-owned inputs for this wave live in:

- `generated/skill_trigger_eval_cases.jsonl`
- `generated/skill_trigger_collision_matrix.json`

The rebuilt downstream surfaces are:

- `generated/description_trigger_eval_cases.jsonl`
- `generated/description_trigger_eval_manifest.json`
- `generated/tiny_router_eval_cases.jsonl`
- `generated/tiny_router_overlay_manifest.json`

## Integration rules

- Keep the wave additive. Reuse the existing collision families and trigger classes.
- Prefer the current family nucleus when a chaos prompt already belongs to a nearby live family.
- Treat one-off incident language as negative or manual unless the owning skill genuinely allows implicit activation.
- Let `aoa-source-of-truth-check` win when stress docs, runbooks, and receipts disagree about authority.
- Keep project overlays thin. A strong overlay match still does not override explicit-only posture.

## Verify

```bash
python scripts/lint_trigger_evals.py --repo-root .
python scripts/build_description_trigger_evals.py --repo-root .
python scripts/lint_description_trigger_evals.py --repo-root .
python scripts/build_tiny_router_inputs.py --repo-root .
python scripts/validate_tiny_router_inputs.py --repo-root .
```
