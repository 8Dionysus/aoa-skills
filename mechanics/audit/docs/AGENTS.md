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

`python scripts/report_skill_evaluation.py --fail-on-canonical-gaps` and `python scripts/audit_skill_quality.py --repo-root . --fail-on-blocked`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
