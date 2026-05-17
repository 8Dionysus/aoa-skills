# AGENTS.md

## Applies to

This card applies to `mechanics/audit/` except where a nearer card applies.

## Role

`mechanics/audit/` owns skill-layer audit posture, public status, promotion pressure, and evidence checks for the skill layer. Audit package guidance keeps this movement bounded and reviewable.

## Read before editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/audit/README.md`, `mechanics/audit/DIRECTION.md`, `mechanics/audit/PARTS.md`, `mechanics/audit/PROVENANCE.md`, `mechanics/audit/ROADMAP.md`, and any nearer card, `docs/AGENTS.md`.

## Boundaries

Keep `mechanics/audit/` focused on mechanic movement. Do not make it canonical skill content, sibling-repo technique truth, proof doctrine, or generated authority. Preserve Audit package guidance; skill-layer audit posture; docs/AUDIT_CONTRACT.md as a bounded local signal, not a global command.

## Validation

Run `python scripts/report_skill_evaluation.py --fail-on-canonical-gaps`, `python scripts/audit_skill_quality.py --repo-root . --fail-on-blocked`, and focused tests for changed audit surfaces.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
