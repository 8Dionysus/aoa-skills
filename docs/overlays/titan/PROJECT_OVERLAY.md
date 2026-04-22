# Titan overlay

## Purpose

This live scaffold overlay groups the `titan-*` skill family for the first Titan service-cohort planting. It adapts bounded skill law to Titan receipts, gates, bridge state, console state, and Memory Loom candidates. It does not change the base skill boundary.

## Authority

- overlay family: `titan`
- canonical overlay doc: `docs/overlays/titan/PROJECT_OVERLAY.md`
- base skill canon: `aoa-skills`
- role truth: `aoa-agents`
- runtime helpers: `aoa-sdk`
- memory truth: `aoa-memo`
- explicit approval rules: operator approval remains visible and repo-relative; the overlay does not redefine the base skill boundary

## Local surface

- repository-relative skill bundles: `skills/titan-*`
- repository-relative review docs: `docs/overlays/titan/REVIEW.md` and `skills/titan-*/checks/review.md`
- repository-relative generated readouts: `generated/overlay_readiness.md`, `generated/governance_backlog.md`, and `generated/skill_bundle_index.md`
- owner routes: `aoa-agents` for role and bearer identity, `aoa-sdk` for runtime helpers, `aoa-memo` for candidate memory, `aoa-evals` for proof canaries
- commands stay repo-relative, such as `python scripts/validate_skills.py` and `python scripts/build_catalog.py --check`

## Overlayed skills

- `titan-approval-ledger` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-approval-loom` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-appserver-bridge` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-appserver-plan` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-closeout` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-console` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-event-replay` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-memory-loom` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-memory-prune` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-mutation-gate` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-recall` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-receipt` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-runtime-gate` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-summon` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.
- `titan-thread-turn-binding` - Titan scaffold skill kept explicit-only for receipt, gate, bridge, console, or memory posture.

## Risks and anti-patterns

- do not widen Titan wording into hidden execution authority
- do not let receipts, replay, or memory candidates replace owner truth
- do not auto-approve Forge mutation or Delta judgment gates
- do not treat scaffold skills as reviewed or canonical until evidence exists
- do not let the overlay become a playbook, role contract, or runtime service

## Validation

- confirm the overlay does not change the base skill boundary
- confirm every listed overlay skill has a matching `skills/titan-*` bundle
- confirm every Titan skill has a bundle-local `checks/review.md`
- confirm paths and commands stay repository-relative
- confirm Forge, Delta, receipt, bridge, console, and memory authority stays explicit and bounded
