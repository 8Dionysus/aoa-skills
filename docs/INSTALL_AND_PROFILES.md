# Install roots and skill pack profiles

Wave 3 adds explicit install profiles instead of assuming one giant skill set always belongs everywhere.

## Authoring file

`config/skill_pack_profiles.json` is the authoring surface.

Each profile declares:

- a `scope`
- an `install_mode`
- a bounded list of skills

## Generated file

`generated/skill_pack_profiles.resolved.json` resolves those profiles into concrete target roots and expected target paths.

`generated/release_manifest.json` now also records `install_profile_revisions` so the resolved profile set can be pinned as part of the repo-local portable release contract.

## Helper scripts

Dry-run or apply an install profile:

```bash
python scripts/install_skill_pack.py --repo-root . --profile user-curated-core
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --dest-root /tmp/aoa-skills --mode copy --execute
```

Render a disable snippet for a profile:

```bash
python scripts/render_codex_config.py --repo-root . --profile repo-risk-explicit
```

Lint the profile authoring:

```bash
python scripts/lint_pack_profiles.py --repo-root .
```

## Verification posture

If you need a machine-readable packaging check rather than a dry-run install plan:

- read `generated/skill_pack_profiles.resolved.json` for the concrete profile membership
- read `generated/release_manifest.json` for the current `install_profile_revisions`

That pair gives an offline verification surface for profile membership drift without introducing a separate package registry.

## Why profiles matter

Not every install root should carry the same surface:

- repo roots can afford project overlays
- user roots should prefer reusable portable skills
- explicit-only risk skills deserve a bounded posture
- project overlays should stay project-local

This is a packaging layer, not a new source of truth.
