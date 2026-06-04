# AGENTS.md

## Applies to

This card applies to `mechanics/audit/docs/`.

## Role

This lane owns audit documentation including `docs/AUDIT_CONTRACT.md`, public-surface posture, and status evidence rules.

## Read before editing

Read parent `mechanics/audit/AGENTS.md`, `mechanics/audit/docs/README.md`, and the audit script or report named by the document.

## Boundaries

Do not soften blockers into suggestions unless the audit contract and validators move together. Public status needs evidence.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

`PYTHONPATH=scripts python scripts/reports/report_skill_evaluation.py --fail-on-canonical-gaps` and `PYTHONPATH=scripts python scripts/audit/audit_skill_quality.py --repo-root . --fail-on-blocked`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
