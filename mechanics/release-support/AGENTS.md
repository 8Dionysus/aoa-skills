# AGENTS.md

Release-support package guidance for `aoa-skills`.

## Purpose

This package owns portable export, install/profile, local adapter, runtime seam,
guardrail, support-resource, release-manifest, and compaction support surfaces.

It does not own runtime infrastructure, public release approval, or generated
exports as authored skill truth.

## Start here

1. `README.md`
2. `DIRECTION.md`
3. `PARTS.md`
4. the relevant active doc under `docs/`
5. `legacy/waves/` only for historical wave accounting

## Validation

```bash
python scripts/release_check.py
python scripts/validate_agent_skills.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
python scripts/validate_tiny_router_inputs.py --repo-root .
```
