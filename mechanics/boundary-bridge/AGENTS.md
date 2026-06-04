# AGENTS.md

## Applies to

This card applies to `mechanics/boundary-bridge/` except where a nearer card applies.

## Role

`mechanics/boundary-bridge/` owns skill-layer boundary bridges between skills, techniques, overlays, and downstream integration for the skill layer. Boundary-bridge package guidance keeps this movement bounded and reviewable.

## Read before editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/boundary-bridge/README.md`, `mechanics/boundary-bridge/DIRECTION.md`, `mechanics/boundary-bridge/PARTS.md`, `mechanics/boundary-bridge/PROVENANCE.md`, `mechanics/boundary-bridge/ROADMAP.md`, and any nearer card, `docs/AGENTS.md`, `overlays/AGENTS.md`, or `legacy/AGENTS.md`.

## Boundaries

Keep `mechanics/boundary-bridge/` focused on mechanic movement. Do not make it canonical skill content, sibling-repo technique truth, proof doctrine, or generated authority. Preserve skill intelligence, overlay, and downstream integration work as bounded local signals, not global commands.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run `PYTHONPATH=scripts python scripts/validation/validate_tiny_router_inputs.py --repo-root .`, `PYTHONPATH=scripts python scripts/builders/build_tiny_router_inputs.py --repo-root . --check`, and bridge-local tests when examples or overlays move.
For `examples/`, run the OpenAI YAML example builder over `mechanics/boundary-bridge/examples/skill_mcp_wiring.map.json` and check the generated example output.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
