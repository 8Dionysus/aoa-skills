# AGENTS.md

Audit package guidance for `aoa-skills`.

## Purpose

This package owns skill-layer audit posture: review routing, evaluation evidence
reading, public-status readouts, trigger-quality checks, conformance checks,
and repo-local audit contracts.

It does not own proof doctrine, verdict authority, runtime activation, or
downstream remediation truth.

## Start here

1. `README.md`
2. `DIRECTION.md`
3. `PARTS.md`
4. `docs/AUDIT_CONTRACT.md`
5. the relevant active doc under `docs/`

## Validation

Use the narrowest relevant checks:

```bash
python scripts/report_skill_evaluation.py --fail-on-canonical-gaps
python scripts/lint_trigger_evals.py --repo-root .
python scripts/lint_description_trigger_evals.py --repo-root .
python scripts/run_skills_ref_validation.py --repo-root .
python -m pytest -q tests/test_mechanics_topology.py
```

Run `python scripts/release_check.py` when generated public, evaluation,
trigger, portable, or release surfaces change.
