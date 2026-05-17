# Titan overlay family review

## Current status

- overlay family: `titan`
- family posture: manual scaffold overlay for the first Titan service cohort
- overlay skills: `titan-approval-ledger`, `titan-approval-loom`, `titan-appserver-bridge`, `titan-appserver-plan`, `titan-closeout`, `titan-console`, `titan-event-replay`, `titan-memory-loom`, `titan-memory-prune`, `titan-mutation-gate`, `titan-recall`, `titan-receipt`, `titan-runtime-gate`, `titan-summon`, `titan-thread-turn-binding`
- base skill canon: `aoa-skills`
- owner layers: `aoa-agents`, `aoa-sdk`, `aoa-memo`, `aoa-evals`, and `8Dionysus`

## Evidence reviewed

- `mechanics/boundary-bridge/overlays/titan/PROJECT_OVERLAY.md`
- `skills/project/titan/titan-*/SKILL.md`
- `skills/project/titan/titan-*/techniques.yaml`
- `skills/project/titan/titan-*/checks/review.md`
- Titan service-cohort, helper/control-plane, memory, proof, and public-runbook docs in `aoa-agents`, `aoa-sdk`, `aoa-memo`, `aoa-evals`, and `8Dionysus`; runtime implementation routes to `abyss-stack` when a real service/process surface is introduced

## Findings

- the family is intentionally scaffold-grade and explicit-only
- the skills preserve Titan gate, receipt, bridge, console, and memory posture without claiming owner truth
- published `aoa-techniques` refs now cover the reusable gate, receipt, provenance, replay, retention, and owner-route practices each skill composes
- Titan-specific role, helper/control-plane, runtime implementation, memory, proof, and runbook authority stays in owner repositories rather than in the technique bridge
- bundle-local review checklists give a human review surface before any status promotion

## Gaps and blockers

- no evaluation-backed promotion is claimed for these scaffold-status overlay skills yet
- any future Titan-specific reusable practice needs a reviewed extraction into `aoa-techniques`; do not reintroduce pending technique ids as placeholders
- generated catalogs are derived routing surfaces and must not become role, runtime, proof, or memory authority

## Recommendation

Keep the Titan overlay scaffold-grade, manual, and explicit-only. Promote individual skills only after review evidence, owner-repo validation, and evaluation-backed readiness exist.
