# skills-ref validation

Wave 7 adds a soft open-standard conformance lane using the upstream `skills-ref` reference validator.

## Intent

The AoA validators know about AoA-specific contracts.
`skills-ref` knows about the open Agent Skills surface.
Using both together gives broader coverage.

## Files

- `generated/skills_ref_validation_manifest.json`
- `scripts/run_skills_ref_validation.py`

## Local install

```bash
git clone https://github.com/agentskills/agentskills.git /tmp/agentskills
git -C /tmp/agentskills checkout 2e8b3265237b2e5f255d6e675f89ae83be572329
python -m pip install -e /tmp/agentskills/skills-ref
python scripts/run_skills_ref_validation.py --repo-root . --require-skills-ref
```

You can also point the wrapper at an explicit executable:

```bash
python scripts/run_skills_ref_validation.py --repo-root . --skills-ref-bin /path/to/skills-ref --require-skills-ref
```

## CI stance

The wrapper is meant to run in CI after the portable export is built.

Recommended order:

1. build export and downstream layers
2. run `validate_agent_skills.py`
3. run `lint_description_trigger_evals.py`
4. run `run_skills_ref_validation.py`

The repo uses this as a soft lane:

- missing validator should skip cleanly
- real validator failures should fail loudly
- AoA-specific validation remains the primary repo-owned authority

## Important note

The upstream README describes `skills-ref` as a reference library intended for demonstration purposes.
Here it is treated as a soft standards conformance lane, not as the only validator and not as a replacement for repo-owned checks.
