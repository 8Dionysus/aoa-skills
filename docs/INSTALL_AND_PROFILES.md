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
`generated/skill_bundle_index.json` mirrors that membership back onto each skill as `install_profiles` so per-skill packaging checks do not need to reverse-read the whole profile set.

`generated/release_manifest.json` now also records `install_profile_revisions` so the resolved profile set can be pinned as part of the repo-local portable release contract.

## Helper scripts

Dry-run or apply an install profile:

```bash
python scripts/install_skill_pack.py --repo-root . --profile user-curated-core
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --dest-root /tmp/aoa-skills --mode copy --execute
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --bundle-root /tmp/repo-core-only-bundle --dest-root /tmp/aoa-skills --mode copy --execute
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --bundle-archive /tmp/repo-core-only.zip --dest-root /tmp/aoa-skills --mode copy --execute
```

Stage a profile-scoped handoff bundle:

```bash
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --format json
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --execute --overwrite --format json
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --archive-path /tmp/repo-core-only.zip --execute --overwrite --format json
```

Inspect a staged profile-scoped handoff bundle:

```bash
python scripts/inspect_skill_pack.py --bundle-root /tmp/repo-core-only-bundle --format json
python scripts/inspect_skill_pack.py --bundle-archive /tmp/repo-core-only.zip --format json
```

Import a staged profile-scoped handoff bundle with one receiver-side flow:

```bash
python scripts/import_skill_pack.py --repo-root . --profile repo-core-only --bundle-root /tmp/repo-core-only-bundle --dest-root /tmp/aoa-skills --format json
python scripts/import_skill_pack.py --repo-root . --profile repo-core-only --bundle-root /tmp/repo-core-only-bundle --dest-root /tmp/aoa-skills --mode copy --execute --format json
python scripts/import_skill_pack.py --repo-root . --profile repo-core-only --bundle-archive /tmp/repo-core-only.zip --dest-root /tmp/aoa-skills --mode copy --execute --format json
```

Verify an installed profile/root against the current portable export:

```bash
python scripts/verify_skill_pack.py --repo-root . --profile repo-default --format json
python scripts/verify_skill_pack.py --repo-root . --profile repo-core-only --install-root /tmp/aoa-skills --format json
python scripts/verify_skill_pack.py --repo-root . --profile repo-core-only --install-root /tmp/aoa-skills --strict-root --format markdown
python scripts/verify_skill_pack.py --repo-root . --profile repo-core-only --bundle-root /tmp/repo-core-only-bundle --install-root /tmp/aoa-skills --format json
python scripts/verify_skill_pack.py --repo-root . --profile repo-core-only --bundle-archive /tmp/repo-core-only.zip --install-root /tmp/aoa-skills --format json
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

If you need a machine-readable packaging check rather than only a dry-run install plan:

- read `generated/skill_pack_profiles.resolved.json` for the concrete profile membership
- read `generated/release_manifest.json` for the current `install_profile_revisions`
- read `generated/skill_bundle_index.json` when you want the inverse view: which install profiles currently include a given skill
- use `scripts/stage_skill_pack.py` when you want one repo-local, profile-scoped handoff directory with its own `bundle_manifest.json`
- use `scripts/inspect_skill_pack.py` when you want one self-contained check over a staged bundle or ZIP before any install step
- use `scripts/import_skill_pack.py` when you want one receiver-side `inspect -> install -> verify` path over a staged bundle or ZIP without stitching those steps together by hand
- use `scripts/verify_skill_pack.py` when you want to verify one real install root against either the current export, a staged bundle directory, or a staged ZIP handoff

That pair gives an offline verification surface for profile membership drift without introducing a separate package registry.

`verify_skill_pack.py` is profile-scoped by default:

- it requires every expected installed skill for the selected profile to exist
- it compares the full installed skill directory to either the current `.agents/skills/<skill>` export or the selected staged bundle with normalized text-file bytes
- it reports extra sibling skill dirs under the install root but does not fail on them unless `--strict-root` is set
- it treats copy and symlink installs the same way: pass/fail is based on exported content parity, not on symlink-target identity

`stage_skill_pack.py` is profile-scoped and plan-first:

- dry-run output gives one deterministic handoff plan with `profile_revision`, `release_identity`, `file_digests`, and `bundle_digest`
- `--execute` materializes a bundle directory containing `bundle_manifest.json`, a bundle-local `README.md`, and the staged `.agents/skills/<skill>` subset
- `--archive-path` adds an optional ZIP transport wrapper over that same staged directory without changing the bundle-local contract
- the staged bundle does not copy the repo-wide `generated/release_manifest.json` because that file describes the whole export, not one profile subset
- `README.md` is the human-facing handoff guide; `bundle_manifest.json` remains the canonical machine-readable source of truth

The ZIP handoff remains repo-local and offline:

- the staged directory stays the canonical intermediate
- the archive is only a transport wrapper with one top-level folder `aoa-skills-<profile>/`
- `inspect_skill_pack.py` validates the bundle-local manifest, file digests, bundle digest, and archive layout without consulting the live repo export
- the ZIP carries the same bundle-local `README.md` as a human-facing companion, not as a second contract
- install and verify can consume the ZIP directly; no separate unpack command is required

## Round-trip handoff

The narrow offline smoke path is:

```bash
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --execute --overwrite --format json
python scripts/inspect_skill_pack.py --bundle-root /tmp/repo-core-only-bundle --format json
python scripts/import_skill_pack.py --repo-root . --profile repo-core-only --bundle-root /tmp/repo-core-only-bundle --dest-root /tmp/aoa-skills --mode copy --execute --format json
```

That keeps the first handoff object profile-scoped, deterministic, and fully offline.

Use `install_skill_pack.py` plus `verify_skill_pack.py` directly when you want the lower-level advanced path or need to keep install and verification as separate steps.

The ZIP transport variant is:

```bash
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --archive-path /tmp/repo-core-only.zip --execute --overwrite --format json
python scripts/inspect_skill_pack.py --bundle-archive /tmp/repo-core-only.zip --format json
python scripts/import_skill_pack.py --repo-root . --profile repo-core-only --bundle-archive /tmp/repo-core-only.zip --dest-root /tmp/aoa-skills --mode copy --execute --format json
```

## Why profiles matter

Not every install root should carry the same surface:

- repo roots can afford project overlays
- user roots should prefer reusable portable skills
- explicit-only risk skills deserve a bounded posture
- project overlays should stay project-local

This is a packaging layer, not a new source of truth.
