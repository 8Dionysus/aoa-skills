# AGENTS.md

## Applies to

This card applies to `mechanics/release-support/` except where a nearer card applies.

## Role

`mechanics/release-support/` owns portable export, component refresh law, runtime path, and legacy/waves/ release support evidence for the skill layer. Release-support package guidance keeps this movement bounded and reviewable.

## Read before editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/release-support/README.md`, `mechanics/release-support/DIRECTION.md`, `mechanics/release-support/PARTS.md`, `mechanics/release-support/PROVENANCE.md`, `mechanics/release-support/ROADMAP.md`, and any nearer card, `docs/AGENTS.md`, `legacy/AGENTS.md`.

## Boundaries

Keep `mechanics/release-support/` focused on mechanic movement. Do not make it canonical skill content, sibling-repo technique truth, proof doctrine, or generated authority. Preserve Release-support package guidance; portable export; legacy/waves/ as a bounded local signal, not a global command.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the specific CI lane or build command named by the changed support
document. Use `python scripts/ci_gate.py --mode export` for portable export
movement and `python scripts/ci_gate.py --mode release` or `python
scripts/release_check.py --include-packaging-smoke` for release-facing changes.
For direct release-support validation, `python scripts/release_check.py`
remains the legacy release audit entrypoint.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
