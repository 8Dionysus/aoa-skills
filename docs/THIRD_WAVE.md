# Third wave for the Codex-facing portable layer

The first wave solved shape.
The second wave solved trigger quality and adapter seams.
The third wave solves operational maturity around the same generated export.

## Objectives

1. Keep the Codex-facing export cumulative and self-regenerating.
2. Make install scope and disable posture explicit.
3. Attach trust, mutation, and confirmation posture to each skill.
4. Preserve enough skill memory for wrappers or compaction-aware runtimes.
5. Add UI metadata so skills look native in Codex selectors.

## What changes in this wave

### 1. Full cumulative export

The repository keeps the full `.agents/skills/*` tree as a generated surface.
Wave 3 extends that same export instead of introducing a new canonical format.

### 2. Install profiles

`config/skill_pack_profiles.json` defines named sets of skills for different install roots:

- `repo-default`
- `repo-core-only`
- `repo-risk-explicit`
- `repo-atm10-overlay`
- `user-curated-core`

The builder resolves these into `generated/skill_pack_profiles.resolved.json`,
and `scripts/install_skill_pack.py` can dry-run or apply them.

### 3. Trust and mutation posture

`config/skill_policy_matrix.json` provides per-skill posture fields such as:

- `trust_posture`
- `mutation_surface`
- `recommended_install_scopes`
- `requires_confirmation_seam`

The builder emits generated views into `generated/trust_policy_matrix.json`
and carries the same fields into runtime contracts and local-adapter manifests.

### 4. Context retention

`generated/context_retention_manifest.json` gives each skill a compact summary,
must-keep items, and rehydration hints.
It does not replace `SKILL.md`.
It exists so wrappers and compaction-aware runtimes can keep the right fragments alive.

### 5. UI metadata and icons

Each exported skill now receives:

- `interface.icon_small`
- `interface.icon_large`
- `interface.brand_color`

The builder writes scope-based default SVG assets when canonical skill resources
do not already provide them.

## Integration posture

Keep the layers separate:

- canonical authoring
  - `skills/*/SKILL.md`
  - `generated/skill_sections.full.json`
  - `generated/skill_catalog.min.json`
- Codex-facing export
  - `.agents/skills/*`
- operational support around the export
  - install profiles
  - trust policy
  - runtime contracts
  - context retention
  - config snippets

Wave 3 does not replace the export.
It makes the export easier to install, govern, and keep stable.
`generated/release_manifest.json` inventories the portable artifacts for this layer and does not replace repo-level release identity in `CHANGELOG.md`, `docs/RELEASING.md`, the Git tag, or the GitHub release body.
