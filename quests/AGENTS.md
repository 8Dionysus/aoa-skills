# AGENTS.md

## Guidance for `quests/`

`quests/` stores durable public-safe obligations that should survive the
current diff.

Quest sources live in lane-first lifecycle directories:
`quests/<lane>/<state>/<quest-file>`.
Do not add top-level quest aliases.

Use a quest when an obligation needs durable follow-through. Do not use this
directory for private todos, roadmap duplication, proof verdicts, runtime
state, or generated indexes.

When moving or editing a quest, keep YAML `state`, owner surface, generated
quest read models, and Questbook references aligned.

Verify with:

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
python scripts/build_catalog.py --check
```
