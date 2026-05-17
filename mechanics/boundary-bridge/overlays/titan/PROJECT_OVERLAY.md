# Titan overlay

## Purpose

This manual overlay groups the `titan-*` skill family for the first Titan service cohort. It adapts bounded skill law to Titan receipts, gates, bridge state, console state, replay, approvals, and Memory Loom candidates. It does not change the base skill boundary or replace the owner repositories.

## Authority

- overlay family: `titan`
- canonical overlay doc: `mechanics/boundary-bridge/overlays/titan/PROJECT_OVERLAY.md`
- base skill canon: `aoa-skills`
- role truth: `aoa-agents`
- runtime helpers and control-plane adapters: `aoa-sdk`
- runtime implementation, services, storage, workers, and daemons: `abyss-stack` when a real service/process surface is introduced
- memory truth: `aoa-memo`
- explicit approval rules: operator approval remains visible and repo-relative; the overlay does not redefine the base skill boundary

## Local surface

- repository-relative skill bundles: `skills/project/titan/titan-*`
- repository-relative review docs: `mechanics/boundary-bridge/overlays/titan/REVIEW.md` and `skills/project/titan/titan-*/checks/review.md`
- repository-relative generated readouts: `generated/overlay_readiness.md`, `generated/governance_backlog.md`, and `generated/skill_bundle_index.md`
- owner routes: `aoa-agents` for role and bearer identity, `aoa-sdk` for helpers and control-plane adapters, `abyss-stack` for real runtime implementation, `aoa-memo` for candidate memory, `aoa-evals` for proof canaries
- commands stay repo-relative, such as `python scripts/validate_skills.py` and `python scripts/build_catalog.py --check`

## Overlayed skills

Session spine:

- `titan-summon` - starts the visible Atlas/Sentinel/Mneme service cohort while Forge and Delta remain locked.
- `titan-receipt` - records receipt state as witness evidence with source, gate, and validation refs.
- `titan-closeout` - closes a Titan session with role, risk, provenance, gate, verification, and next-owner summary.

Gate and approval surfaces:

- `titan-runtime-gate` - opens Forge mutation or Delta judgment lanes only through matching explicit runtime gates.
- `titan-mutation-gate` - gates Forge workspace-write work with target, precheck, validation, and rollback posture.
- `titan-approval-ledger` - records one operator approval without turning approval into owner truth.
- `titan-approval-loom` - maintains the bridge approval queue while keeping gate kinds separate.

Console, bridge, and replay surfaces:

- `titan-console` - keeps visible lane status and warnings without changing gate authority.
- `titan-appserver-plan` - emits an inspectable app-server launch plan without starting hidden execution.
- `titan-appserver-bridge` - relays thread, turn, event, approval, replay, and metric state as derived bridge state.
- `titan-thread-turn-binding` - binds bridge events and approvals to explicit thread and turn ids.
- `titan-event-replay` - rebuilds inspectable state from events without granting authority to the replay.

Memory and recall surfaces:

- `titan-memory-loom` - writes candidate-grade remembrance records with source refs, confidence, and authority notes.
- `titan-recall` - retrieves candidate records with verification routes instead of final claims.
- `titan-memory-prune` - proposes retain, redact, tombstone, merge, or defer actions without silent deletion.

## Risks and anti-patterns

- do not widen Titan wording into hidden execution authority
- do not let receipts, replay, or memory candidates replace owner truth
- do not auto-approve Forge mutation or Delta judgment gates
- do not treat scaffold status as reviewed or canonical until evidence exists
- do not let the overlay become a playbook, role contract, or runtime service

## Validation

- confirm the overlay does not change the base skill boundary
- confirm every listed overlay skill has a matching `skills/project/titan/titan-*` bundle
- confirm every Titan skill has a bundle-local `checks/review.md`
- confirm paths and commands stay repository-relative
- confirm Forge, Delta, receipt, bridge, console, and memory authority stays explicit and bounded
