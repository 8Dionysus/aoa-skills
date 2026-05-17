# AGENTS.md

## Applies to

This card applies to `mechanics/boundary-bridge/overlays/`.

## Role

Overlays describe thin overlay project-specific bridge surfaces such as `PROJECT_OVERLAY.md` and `REVIEW.md` that connect `skills/project/<family>/<skill>/` to downstream integration without owning the downstream repo.

## Read before editing

Read parent `mechanics/boundary-bridge/AGENTS.md`, overlay README if present, the target project skill bundle, and the downstream receipt or review surface being bridged.

## Boundaries

Keep overlays thin. Do not duplicate canonical `SKILL.md`, invent downstream adoption, or turn an overlay into a project skill owner.

## Validation

Run `python scripts/validate_tiny_router_inputs.py --repo-root .` and any overlay-specific review check named by the parent package.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
