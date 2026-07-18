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
| evaluation | `core/engineering/aoa-eval` | advertised |
| verification | `core/engineering/aoa-verification` | deferred |
| stewardship | `core/stewardship/aoa-knowledge-stewardship` | advertised |
| closeout transition | `core/session-growth/aoa-checkpoint-closeout-bridge` | advertised transitional |
| first memo writeback | `core/session-growth/aoa-memo-writeback` | advertised |
| session learning | `core/session-growth/aoa-session-harvest` | advertised |
| session recovery | `core/session-growth/aoa-session-recovery` | advertised |

Each bundle contains `SKILL.md`, optional `agents/openai.yaml`, and only the
resources required by that procedure. There is no runtime `techniques.yaml`
contract. Technique lineage, if relevant, stays optional provenance in the
capability source.

## Promotion threshold

A new bundle requires a stable trigger, distinct ABI, independent composition
value, and held-out outcome benefit over both no skill and its possible parent
bundle. Until then, keep the behavior as an internal mode or capability node.

## Projection

This source repository intentionally has no `.agents/skills/*` tree. Edit the
owner source here, then use `scripts/export/build_agent_skills.py` to rebuild
metadata through a temporary portable assembly or to populate an explicit new
external consumer root. Inside a staged consumer bundle, `.agents/skills/*`
remains the logical portable layout and never becomes authority.

Target projection topology: the OS user profile projects advertised shared and
admitted owner-home bundles once into the active host's verified user skill
root. The standard Codex resolution is `$HOME/.codex/skills`; a different host
location must be selected explicitly and verified rather than inferred. A
sibling repository's `.agents/skills/*` is reserved for repository-only
procedures and must not duplicate a globally selected owner bundle. A
workspace-root projection contains only workspace-owned procedures, or remains
empty. Additional host projections are created only for an observed consumer
and never become source truth.

The shared machine grammar for an admitted sibling home is
`schemas/skill-home-port.schema.json`; the operating contract is
`docs/HOME_SKILL_PORT.md`. It is not an invitation to add empty `skills/`
directories or to move sibling procedure truth here.
