# Config District

`config/` holds repo-wide source inputs for portable export, pack profiles,
policy posture, project-core rings, runtime guardrails, trigger-eval policy,
validation lane command sequences, and tiny-router bands.

Mechanic-local seed configs belong under the owning mechanic package or part.
For example, Agon candidate seeds live under `mechanics/agon/parts/*/config/`,
while root `config/` keeps cross-skill export and activation policy inputs.

## Owner Route

Use [AGENTS](AGENTS.md) before editing. Check whether the config is repo-wide
or mechanic-local, keep secrets and hidden allowlists out, and regenerate
derived surfaces through the owning builder when source config changes.
