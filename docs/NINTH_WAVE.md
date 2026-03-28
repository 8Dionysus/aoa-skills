# Ninth Wave

Wave 9 adds a tiny-router compression layer for downstream routing.

This wave does not add new skills, new activation authority, or a second router
canon inside `aoa-skills`.

It adds only skill-derived, low-context surfaces that help a downstream router
shortlist candidates before a stronger stage decides whether any skill should be
activated.

## Added surfaces

- `config/tiny_router_skill_bands.json`
- `generated/tiny_router_skill_signals.json`
- `generated/tiny_router_candidate_bands.json`
- `generated/tiny_router_capsules.min.json`
- `generated/tiny_router_eval_cases.jsonl`
- `generated/tiny_router_overlay_manifest.json`

## Boundary

`aoa-skills` owns:

- compressed skill cues
- small band groupings
- companion relationships
- manual-invocation markers
- overlay markers

`aoa-routing` owns:

- shortlist scoring
- fallback behavior
- repo-family boosts
- two-stage prompt and tool contracts
- stage wiring

Stage 1 may narrow candidates.
Stage 1 must not activate a skill.
