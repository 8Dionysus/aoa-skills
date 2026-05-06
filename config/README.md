# Config District

`config/` holds repo-wide source inputs for portable export, pack profiles,
policy posture, project-core rings, runtime guardrails, trigger-eval policy, and
tiny-router bands.

Mechanic-local seed configs belong under the owning mechanic package or part.
For example, Agon candidate seeds live under `mechanics/agon/parts/*/config/`,
while root `config/` keeps cross-skill export and activation policy inputs.

## Before Editing

1. Check whether the config is repo-wide or mechanic-local.
2. Keep secrets, local absolute paths, and hidden allowlists out.
3. Regenerate derived surfaces when source config changes.
4. Run the nearest validator plus `python scripts/validate_agent_skills.py --repo-root .`.
