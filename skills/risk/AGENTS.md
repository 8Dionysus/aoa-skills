# AGENTS.md

Guidance for `skills/risk/`.

## Purpose

`risk/` owns portable guard skills for approval, dry-run, infrastructure,
bounded local stack bring-up, and sanitized sharing.

## Read First

1. `../AGENTS.md`
2. this file
3. `../README.md`
4. the target bundle `SKILL.md`
5. the target bundle `techniques.yaml`
6. touched `checks/`, `examples/`, `references/`, `scripts/`, or `assets/`

## Local Law

- Prefer explicit invocation for risk-heavy work.
- Keep confirmation, preview, rollback, redaction, and lifecycle boundaries
  visible.
- Do not normalize hidden destructive actions, implicit approval, or secret
  exposure.
- Project-specific stricter policy belongs in `../project/<family>/`.

## Validation

After source changes, rebuild generated surfaces and portable export. For
support bundles, also run:

```bash
python scripts/build_support_resources.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
```
