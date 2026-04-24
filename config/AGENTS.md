# AGENTS.md

## Guidance for `config/`

`config/` holds portable export, policy, profile, and project-core kernel inputs for the skill layer.

Config changes are small contract changes. Keep them explicit, reviewable, and subordinate to source skill bundles and documented public-surface policy.

Use config files to describe allowed export behavior, profile defaults, project-core receipt shape, trust gates, and bounded activation policy. Do not use config to smuggle new skill meaning that belongs in `skills/*/SKILL.md`.

When touching `project_core_skill_kernel.json`, preserve receipt readability, owner-status posture, and the difference between advisory surface detection and actual skill activation authority.

No secrets, tokens, local-only absolute paths, or hidden allowlists. In lower-case too: no secrets. Prefer documented examples over private operator assumptions.

Verify with the nearest config-specific validator when present, then:

```bash
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/validate_semantic_agents.py
```
