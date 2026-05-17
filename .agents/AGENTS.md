# AGENTS.md

## Applies to

This card applies to `.agents/` and the checked-in portable skill-pack projection under `.agents/skills/`.

## Role

`.agents/` is an install/export companion for local coding-agent skill consumption. It carries built pack surfaces; it is not the canonical source of bundle meaning.

## Read before editing

Read root `AGENTS.md`, `DESIGN.AGENTS.md`, `skills/AGENTS.md`, `generated/AGENTS.md`, and `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md` before changing this lane.

## Boundaries

Do not hand-edit `.agents/skills/*` to change a skill. Change canonical `skills/**`, config, templates, or builders, then rebuild and validate the export. Keep Codex-specific names here only when they describe adapter compatibility, install layout, or an actual local adapter seam.

## Validation

Use `python scripts/build_agent_skills.py --repo-root .`, `python scripts/validate_agent_skills.py --repo-root .`, and `python scripts/validate_support_resources.py --repo-root . --check-portable`. For release-facing pack changes, run `python scripts/release_check.py`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
