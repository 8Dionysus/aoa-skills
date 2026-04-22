# Titan overlay family review

## Current status

- overlay family: `titan`
- family posture: live scaffold overlay for the first Titan service-cohort planting
- scaffold skills: `titan-approval-ledger`, `titan-approval-loom`, `titan-appserver-bridge`, `titan-appserver-plan`, `titan-closeout`, `titan-console`, `titan-event-replay`, `titan-memory-loom`, `titan-memory-prune`, `titan-mutation-gate`, `titan-recall`, `titan-receipt`, `titan-runtime-gate`, `titan-summon`, `titan-thread-turn-binding`
- base skill canon: `aoa-skills`
- owner layers: `aoa-agents`, `aoa-sdk`, `aoa-memo`, `aoa-evals`, and `Dionysus`

## Evidence reviewed

- `docs/overlays/titan/PROJECT_OVERLAY.md`
- `skills/titan-*/SKILL.md`
- `skills/titan-*/techniques.yaml`
- `skills/titan-*/checks/review.md`
- Titan seed waves in `Dionysus` and owner-local Titan docs in sibling repositories

## Findings

- the family is intentionally scaffold-grade and explicit-only
- the skills preserve Titan gate, receipt, bridge, console, and memory posture without claiming owner truth
- pending technique refs keep the technical debt visible until Titan workflow techniques are published
- bundle-local review checklists give a human review surface before any status promotion

## Gaps and blockers

- pending Titan technique ids need replacement with published `aoa-techniques` refs before status promotion
- no evaluation-backed promotion is claimed for these scaffold skills yet
- generated catalogs are derived routing surfaces and must not become role, runtime, proof, or memory authority

## Recommendation

Keep the Titan overlay as scaffold-grade and explicit-only. Promote individual skills only after published technique refs, review evidence, and owner-repo validation exist.
