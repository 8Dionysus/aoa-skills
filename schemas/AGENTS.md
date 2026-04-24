# AGENTS.md

## Guidance for `schemas/`

`schemas/` holds contract surfaces for skill-adjacent examples, receipts, checkpoints, follow-through decisions, and bounded integration artifacts.

Schema edits are contract edits. Preserve `$schema`, stable `$id` or identifier posture when present, required fields, enums, and field descriptions that keep activation bounded.

Do not make a schema more permissive just to quiet an example. Change the example or document the new contract deliberately.

Pair schema changes with examples, validators, and any generated catalog surfaces that consume the contract.

Keep skill authority narrow: schema fields may describe receipts, route decisions, applicability, or closeout signals, but they do not create new execution rights outside the owning `SKILL.md`.

Verify with:

```bash
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/validate_semantic_agents.py
```
