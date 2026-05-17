# Skill Intelligence Registry First Slice

Date: 2026-05-17

Status: accepted

## Context

`aoa-skills` already publishes skill catalogs, runtime/export surfaces,
support-resource indexes, trigger cases, evaluation matrices, boundary maps,
and promotion-pressure reports. Those surfaces are useful, but an agent looking
for the right skill still has to hop across several generated files and then
reload the source bundle manually.

The wider workspace is moving toward richer indexing, RAG, Agentic RAG, DAG,
and graph-backed retrieval. That direction should start from the skill source
layer without making semantic infrastructure a prerequisite for basic skill
discovery.

## Decision

Add a source-derived Skill Intelligence first slice in `aoa-skills`:

- `generated/skill_intelligence_registry.json`
- `generated/skill_intelligence_registry.min.json`
- `scripts/skill_intelligence_surface.py`
- `scripts/skill_intelligence.py`
- `schemas/skill_intelligence_registry.schema.json`

The registry joins canonical skill source sections with existing generated
evidence: policy, runtime discovery, tiny-router cues, support resources,
boundary matrix, evaluation matrix, bundle index, and graph refs.

The CLI provides local read-only build/check, lexical search, candidate
explanation, and status views.

## Consequences

- Agents get one stable registry/search/explain surface before any semantic
  backend exists.
- The registry remains derived evidence, not source truth. `SKILL.md`,
  `techniques.yaml`, config, review records, and builders still own meaning.
- Search can rank and explain candidates, but it cannot activate a skill,
  promote a status, or override manual/suggest/invoke policy.
- The minified registry can travel as a portable evidence packet without full
  source text.
- Minimal test repositories can still build the surface from authored skill
  sources when richer generated inputs are absent.
- Later RAG, Agentic RAG, DAG, KAG, or SDK layers should build on this registry
  instead of replacing canonical skill bundles or generated-source boundaries.

## Verification

Verify with:

```bash
python scripts/build_catalog.py --check
python scripts/skill_intelligence.py build --check
python scripts/skill_intelligence.py query "source truth docs conflict canonical guidance" --limit 3
python scripts/skill_intelligence.py explain aoa-source-of-truth-check --intent "docs conflict over authoritative source"
python -m pytest -q tests/test_skill_intelligence_surface.py tests/test_generated_surface_schemas.py tests/test_build_catalog.py
python scripts/release_check.py
```
