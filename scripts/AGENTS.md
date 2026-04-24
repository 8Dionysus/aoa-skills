# AGENTS.md

## Guidance for `scripts/`

`scripts/` holds deterministic builders, validators, reports, and inspectors for the skill canon.

Prefer deterministic, repo-relative behavior. Scripts should not depend on hidden network state, private workspace paths, or ambient credentials unless the command explicitly documents that dependency.

When changing builders, preserve authored-source ownership: `skills/*/SKILL.md`, `techniques.yaml`, and support resources own meaning; generated catalogs, portable exports, tiny-router inputs, and reports summarize it.

When changing validators, keep failure messages actionable and tied to concrete files. Do not weaken validation to pass a broken corpus.

When changing reports, preserve bounded language. A report may expose gaps or readiness, but it must not overclaim capability.

Verify with the touched command and normally:

```bash
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/validate_semantic_agents.py
```
