# OS Abyss overlay family review

## Current status

- overlay family: `os`
- family posture: scaffold overlay for OS Abyss artifact-trust routing
- scaffold skills: `os-abyss-artifact-trust-loop`
- base skill canon: `aoa-skills`
- host artifact-trust authority: `abyss-machine`
- access plane: existing read-only `abyss-machine` MCP
- proof and negative-scenario authority: `aoa-evals`
- family review surface: `mechanics/boundary-bridge/overlays/os/PROJECT_OVERLAY.md`, `mechanics/boundary-bridge/overlays/os/REVIEW.md`, `skills/project/abyss/os-abyss-artifact-trust-loop/checks/review.md`

## Evidence reviewed

- `mechanics/boundary-bridge/docs/OVERLAY_SPEC.md`
- `mechanics/boundary-bridge/overlays/os/PROJECT_OVERLAY.md`
- `skills/project/abyss/os-abyss-artifact-trust-loop/SKILL.md`
- `skills/project/abyss/os-abyss-artifact-trust-loop/techniques.yaml`
- `skills/project/abyss/os-abyss-artifact-trust-loop/checks/review.md`
- `config/openai_skill_extensions.json`
- current `abyss-machine` artifact-trust CLI and MCP read-model route requirements

## Findings

- the overlay is intentionally thin and exists to route agents through current artifact-trust surfaces, not to own OS trust policy
- `os-abyss-artifact-trust-loop` keeps MCP read-only and keeps build, verify, sign, evidence promotion, registry writes, and trust-root changes in owner-local commands
- the skill names `.aoa`, `aoa-sdk`, `aoa-evals`, `abyss-machine`, and owner repos as separate roles instead of collapsing them into one authority
- generated skill export and MCP dependency manifests must be rebuilt before the skill can be treated as portable or runtime-visible
- C2PA public media remains warn or deferred until real production trust credentials and owner acceptance exist

## Gaps and blockers

- no evaluated promotion is claimed for this scaffold skill yet
- current-session prompt visibility can only be claimed after generated export and runtime/prompt reload evidence are checked
- no downstream owner adoption is implied by this overlay alone
- public release, C2PA, TUF, SCITT, OCI, and signing posture remain artifact-class and owner-route dependent

## Recommendation

Keep the `os` overlay scaffold-grade and explicit. Promote `os-abyss-artifact-trust-loop` only after agents can complete the full loop through MCP or equivalent CLI, owner-local producers, trust gates, generated export visibility, and representative OS Abyss E2E artifact classes without guessing commands or violating authority boundaries.
