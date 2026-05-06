# AGENTS.md

## Guidance for `tests/`

`tests/` protects root skill contracts, generated-surface parity, support
resources, trigger quality, and downstream handoff shapes.

Mechanic-local tests may live with the owning mechanic package or part. Use
`../mechanics/ARTIFACT_TOPOLOGY.md` when a test only makes sense beside one
mechanic-owned schema, seed, or builder.

Tests should exercise behavior or contract truth, not merely freeze incidental formatting. Prefer fixtures that make a boundary visible: activation, support-resource portability, technique drift, receipt shape, and trigger collision.

Do not update expected outputs without checking the authored source that owns the meaning. If generated files changed, rebuild first and then inspect the diff.

Keep tests public-safe. No secrets, private paths, live credentials, or unreduced operator data.

When a test guards a downstream seam, name the owner repo and the bounded claim the test protects.

Verify with:

```bash
python -m pytest -q tests
python -m pytest -q mechanics/agon/parts/workflow-candidate-bridge/tests mechanics/agon/parts/epistemic-candidate-boundary/tests
python scripts/validate_semantic_agents.py
```
