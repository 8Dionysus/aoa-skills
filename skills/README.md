# Callable Skill Sources

`skills/` owns only independently callable portable procedures. Semantic
capabilities, internal modes, external workflows, tools, guards, adapters, and
human gates belong in the capability graph without requiring one `SKILL.md`
each.

This tree is the canonical home only for shared AoA procedures. A procedure
whose trigger, commands, facts, or lifecycle are repository-specific belongs
in that repository's admitted top-level `skills/` home. Do not copy shared
bundles into sibling source trees and do not create an empty home in advance.

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

The normal user profile projects only advertised shared bundles once. A
sibling repository's `.agents/skills/*` may project only that repository's
advertised home bundles. A workspace-root projection contains only
workspace-owned procedures, or remains empty. Additional host projections are
created only for an observed consumer and never become source truth.
