# Boundary Bridge Provenance

This bridge records the source-to-active move for boundary and overlay surfaces.

## Moved active docs

| Former path | Current path |
|---|---|
| `docs/LAYER_POSITION.md` | `mechanics/boundary-bridge/docs/LAYER_POSITION.md` |
| `docs/BRIDGE_SPEC.md` | `mechanics/boundary-bridge/docs/BRIDGE_SPEC.md` |
| `docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md` | `mechanics/boundary-bridge/docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md` |
| `docs/TWO_STAGE_SKILL_SELECTION.md` | `mechanics/boundary-bridge/docs/TWO_STAGE_SKILL_SELECTION.md` |
| `docs/OVERLAY_SPEC.md` | `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md` |
| `docs/CODEX_SKILL_MCP_WIRING.md` | `mechanics/boundary-bridge/docs/CODEX_SKILL_MCP_WIRING.md` |
| `docs/OPENAI_SKILL_EXTENSIONS.md` | `mechanics/boundary-bridge/docs/OPENAI_SKILL_EXTENSIONS.md` |
| `docs/overlays/` | `mechanics/boundary-bridge/overlays/` |

## Preserved Skill Intelligence Strategy

The first Skill Intelligence strategy artifact is preserved as package-local
raw lineage:

| Former path | Preserved raw path | Active route |
|---|---|---|
| `legacy/2026-05-17__skill-intelligence-layer-strategy.md` | `mechanics/boundary-bridge/legacy/skill-intelligence/raw/2026-05-17__skill-intelligence-layer-strategy.md` | `docs/decisions/AOA-SK-D-0021-skill-intelligence-registry-first-slice.md` and `docs/ARCHITECTURE.md` |

The raw strategy informs registry, search, explanation, tiny-router adjacency,
and future retrieval boundaries. It does not own current generated registry
behavior or router policy.

## Stop-line

Boundary bridge makes handoffs legible. It does not absorb sibling-owner truth.
