# AGENTS.md

Boundary-bridge package guidance for `aoa-skills`.

## Purpose

This package owns skill-layer boundary bridges: layer position, technique-skill
bridges, support-dir adapters, overlays, two-stage selection, MCP/OpenAI
metadata seams, and tiny downstream routing contracts.

It does not own routing policy, downstream owner truth, or generated metadata
as doctrine.

## Start here

1. `README.md`
2. `DIRECTION.md`
3. `PARTS.md`
4. the relevant active doc under `docs/`
5. `examples/README.md` for MCP/OpenAI scaffold examples
6. `overlays/AGENTS.md` for overlay family edits

## Validation

```bash
python scripts/validate_tiny_router_inputs.py --repo-root .
python scripts/validate_skill_mcp_wiring.py --workspace-config /path/to/.codex/config.toml --format text
python -m pytest -q tests/test_mechanics_topology.py
```

Use `python scripts/release_check.py` when generated export, overlays, or
portable manifests change.
