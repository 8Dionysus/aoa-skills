# aoa-skills Questbook

No active repo-local quests.

Questbook is reserved for a durable obligation that survives the current
change, belongs to `aoa-skills`, and cannot be represented as current
capability or skill source, a decision, or an external-owner request. A live
task, raw trace, task-local DAG, and temporary follow-up are session-only.

Requested-only Agon candidates remain under `quests/agon/captured/` and their
Agon projections; they are not repo-local lifecycle quests or landed skills.

When a real obligation is admitted, add one schema-valid YAML source under
`quests/<lane>/<state>/`, list active IDs here, and rebuild
`generated/quest_catalog.min.json` plus `generated/quest_dispatch.min.json`.
Closed quests leave the active surface; Git history preserves them.
