# Bridge from existing AoA support dirs

`aoa-skills` already uses support surfaces that are meaningful inside the repo:

- `agents/`
- `checks/`
- `examples/`

Wave 8 adds standard skill-bundle directories without discarding the existing
AoA language.

## Bridge posture

Existing AoA support surface | Wave 8 standard surface
--- | ---
`agents/openai.yaml` | remains metadata, not duplicated
`checks/review.md` | complemented by `references/*` and script validators
`examples/runtime.md` | complemented by `assets/*.template.json`

## Why bridge instead of replace

The current repo already derives governance and review surfaces from the AoA
layout. Replacing those directories would create unnecessary churn. Adding
standard support-bundle directories makes the skills easier to consume by Codex
and local runtimes while preserving repo-native semantics.

## Recommended evolution path

1. keep current `checks/` and `examples/` files
2. add `scripts/`, `references/`, and `assets/`
3. let the existing portable export builder mirror the new standard dirs into `.agents/skills/*`
4. gradually teach CI to require stronger resource bundles on high-risk skills
