# AGENTS.md

Experience package guidance for `aoa-skills`.

## Purpose

This package owns owner-local Experience skill contracts: adoption consent,
office/service handoff, receipt generation, installation, rollback, stay/hold,
and governance-runtime skill boundaries.

It does not own release approval, assistant self-authority, runtime writes, or
Tree-of-Sophia meaning.

## Start here

1. `README.md`
2. `DIRECTION.md`
3. `PARTS.md`
4. the relevant active doc under `docs/`

## Validation

```bash
python -m pytest -q tests/test_experience_wave3_seed_contracts.py tests/test_mechanics_topology.py
python scripts/validate_skills.py --fail-on-review-truth-sync
```

Use `python scripts/release_check.py` when package movement touches generated,
release, or public surfaces.
