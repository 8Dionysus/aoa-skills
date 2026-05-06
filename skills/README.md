# Skills Source Topology

`skills/` is the canonical source tree for AoA skill bundles.
Each bundle is still identified by its directory name and authored by the local
`SKILL.md` plus `techniques.yaml` pair, but the source tree is no longer flat.

The generated Codex-facing export stays flat under `.agents/skills/*`.
That export is for installation and runtime lookup. It is not the source home.

## Route Map

| Lane | Use for | Start here |
|---|---|---|
| `core/engineering/` | reusable engineering workflows such as source-of-truth, ADR, TDD, boundaries, ports, contracts, invariants, and change protocol | [AGENTS](core/engineering/AGENTS.md) |
| `core/session-growth/` | reviewed session-growth workflows such as harvest, route forks, repair, progression, quest harvest, closeout bridge, and summon | [AGENTS](core/session-growth/AGENTS.md) |
| `risk/` | guard skills for approval, dry-run, infra, stack bring-up, and sanitized sharing | [AGENTS](risk/AGENTS.md) |
| `project/` | project overlay skills that adapt core or risk practice to a named owner family | [AGENTS](project/AGENTS.md) |

## Bundle Contract

A skill bundle owns:

- `SKILL.md`
- `techniques.yaml`
- optional `agents/openai.yaml`
- optional `checks/`, `examples/`, `references/`, `scripts/`, or `assets/`

Do not place a skill bundle in mechanics. Mechanics explain movement around the
skill layer; source skill meaning lives here.

Lane `AGENTS.md` files own local law. This README is only the topology atlas;
do not add lane README files unless a branch grows a real non-law atlas that
cannot stay clear in this root map.

## Update Rhythm

When a bundle changes, update the authored bundle first, then rebuild generated
surfaces. When a bundle moves lanes, update route docs and generated source
paths in the same change.

The normal source-to-export path is:

1. edit `skills/**/<name>/SKILL.md`, `techniques.yaml`, or support artifacts
2. run `python scripts/build_catalog.py`
3. run `python scripts/build_agent_skills.py --repo-root .`
4. run validators named by `skills/AGENTS.md`

## Stop Lines

- Do not add flat compatibility aliases under `skills/<name>`.
- Do not hand-edit `.agents/skills/*` as source truth.
- Do not copy technique doctrine from `aoa-techniques`; cite it through
  `techniques.yaml` and the traceability section.
- Do not hide project runtime details inside public core skills.
