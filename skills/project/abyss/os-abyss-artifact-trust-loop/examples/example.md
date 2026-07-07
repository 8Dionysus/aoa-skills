# Example

## Scenario

An agent needs to decide whether a `public_source_seed` or `public_media_export` can be consumed or released inside OS Abyss. The checkout may be dirty, sibling repos may have moved, and the current session may or may not have the refreshed `abyss_machine` MCP artifact-trust surfaces loaded.

## Why this skill fits

The work is not a local code edit. It is an OS artifact-trust loop: class detection, requirements, producer profile, drift, durable registry evidence, trust-gate verdict, owner-local refresh if needed, and honest closeout.

## Expected inputs

- artifact class or path
- consumer intent
- source repo/ref and dirty-state note when relevant
- current `abyss-machine artifacts` outputs or MCP read surfaces
- owner route docs and producer commands
- existing registry/latest evidence refs and sidecar paths when present

## Expected outputs

- resolved artifact class and consumer intent
- requirements, producer, affected, coverage, registry/latest, trust-gate, scenarios, and validate summary
- owner route for any refresh, build, verify, sign, materialize, promote, eval, or release action
- explicit allow, warn, deny, or manual-review verdict
- remaining blockers, stale evidence, or deferred credentials
- verification summary that names CLI/MCP agreement or the reason current MCP runtime could not be used

## Boundary notes

- Use existing `abyss-machine` MCP read models or equivalent CLI commands. Do not create a second trust MCP for this loop.
- MCP access can inspect trust state; it cannot perform signing, evidence promotion, registry writes, trust-root changes, privileged host actions, or arbitrary artifact commands.
- `.aoa` may help route session evidence, but it is not trust-policy authority.
- Public media C2PA stays warn or deferred while OS Abyss lacks an accepted production trust credential.
- Dirty repo state is not a reason to stop by itself; it is evidence that must be labeled honestly if the owner route allows dirty work.

## Verification notes

- Confirm the final trust-gate verdict matches the consumer intent.
- Confirm `warn` remains visible as warn.
- Confirm owner-local validators or `aoa-evals` proof were run when the trust claim, consumer admission, or artifact policy changed.
- Confirm generated skill and MCP dependency surfaces were rebuilt after skill wiring changes.
