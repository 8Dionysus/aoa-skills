# AGENTS.md

## Guidance for `manifests/`

`manifests/` is the root manifest route district.
It may hold route cards or registries, but manifest records themselves belong
with the owning mechanic package or part.

Do not add component, hook, recurrence, adapter, export, or runtime manifest
records here unless the record is truly root-owned and no mechanic package owns
the behavior.

When a manifest record moves, update the owner package provenance, tests, and
any generated consumer that stores the path.

Verify with the owner package validator plus:

```bash
python scripts/validate_nested_agents.py
python scripts/validate_skills.py
```
