# Callable Skill Sources

`skills/` owns only independently callable portable procedures. Semantic
capabilities, internal modes, external workflows, tools, guards, adapters, and
human gates belong in the capability graph without requiring one `SKILL.md`
each.

## Current bundles

| Family | Bundle | Visibility |
| --- | --- | --- |
| decisions | `core/engineering/aoa-decision` | advertised |
| engineering | `core/engineering/aoa-engineering-shape` | deferred |
| evaluation | `core/engineering/aoa-eval` | deferred |
| verification | `core/engineering/aoa-verification` | deferred |
| stewardship | `core/stewardship/aoa-knowledge-stewardship` | deferred |
| session learning | `core/session-growth/aoa-session-harvest` | deferred |
| session recovery | `core/session-growth/aoa-session-recovery` | deferred |

Each bundle contains `SKILL.md`, optional `agents/openai.yaml`, and only the
resources required by that procedure. There is no runtime `techniques.yaml`
contract. Technique lineage, if relevant, stays optional provenance in the
capability source.

## Promotion threshold

A new bundle requires a stable trigger, distinct ABI, independent composition
value, and held-out outcome benefit over both no skill and its possible parent
bundle. Until then, keep the behavior as an internal mode or capability node.

## Projection

`.agents/skills/*` is the generated flat portable export. Edit source here,
then rebuild with `scripts/export/build_agent_skills.py`; never edit the export
as authority.
