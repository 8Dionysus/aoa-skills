# AGENTS.md

## Applies to

This card applies to `.agents/` and all descendants unless a nearer
`AGENTS.md` narrows the path.

## Role

`.agents/` holds agent-facing companion lanes for `aoa-skills`.

It carries the generated portable skill pack under `.agents/skills/` and the
Codex Spark fast-session lane under `.agents/spark/`.

It is not the canonical source of bundle meaning.

## Read before editing

Read root `AGENTS.md`, `DESIGN.AGENTS.md`, and the nearest lane card before
changing files here.

For portable skill-pack work, also read `skills/AGENTS.md`,
`generated/AGENTS.md`, and
`mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md`.

For Codex Spark work, also read `.agents/spark/AGENTS.md`,
`.agents/spark/README.md`, `.agents/spark/registry.json`, and the chosen
scenario `README.md` plus `PROMPT.md`.

## Boundaries

- Do not hand-edit `.agents/skills/*` to change a skill. Change canonical
  `skills/**`, config, templates, or builders, then rebuild and validate the
  export.
- Do not make `.agents/spark/` stronger than canonical skill bundles,
  generated-source boundaries, mechanics packages, review evidence, or sibling
  owner repositories.
- Keep Codex-specific names here only when they describe adapter
  compatibility, install layout, model-facing lane behavior, or an actual
  local adapter seam.

## Validation

Run the smallest covering checks:

```bash
python scripts/build_agent_skills.py --repo-root .
python scripts/validate_agent_skills.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
```

For release-facing pack or Spark lane changes, run:

```bash
python scripts/release_check.py
```

## Closeout

Report changed agent lanes, source bundle or builder surfaces consulted,
generated or portable companions rebuilt or left untouched, validation run,
validation skipped, remaining risk, and any next owner route.
