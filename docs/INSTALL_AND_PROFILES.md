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
python scripts/install_skill_pack.py --repo-root . --profile repo-project-core-outer-ring --dest-root /tmp/aoa-skills --mode copy --execute
python scripts/install_skill_pack.py --repo-root . --profile repo-quest-harvest-only --dest-root /tmp/aoa-skills --mode copy --execute
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --bundle-root /tmp/repo-core-only-bundle --dest-root /tmp/aoa-skills --mode copy --execute
python scripts/install_skill_pack.py --repo-root . --profile repo-core-only --bundle-archive /tmp/repo-core-only.zip --dest-root /tmp/aoa-skills --mode copy --execute
```

Stage a profile-scoped handoff bundle:

```bash
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --format json
python scripts/stage_skill_pack.py --repo-root . --profile repo-core-only --output-root /tmp/repo-core-only-bundle --execute --overwrite --format json
python scripts/stage_skill_pack.py --repo-root . --profile repo-project-core-outer-ring --output-root /tmp/repo-project-core-outer-ring-bundle --execute --overwrite --format json
python scripts/stage_skill_pack.py --repo-root . --profile repo-quest-harvest-only --output-root /tmp/repo-quest-harvest-only-bundle --execute --overwrite --format json
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
python scripts/import_skill_pack.py --repo-root . --profile repo-project-core-outer-ring --bundle-root /tmp/repo-project-core-outer-ring-bundle --dest-root /tmp/aoa-skills --mode copy --execute --format json
python scripts/import_skill_pack.py --repo-root . --profile repo-quest-harvest-only --bundle-root /tmp/repo-quest-harvest-only-bundle --dest-root /tmp/aoa-skills --mode copy --execute --format json
python scripts/import_skill_pack.py --repo-root . --profile repo-core-only --bundle-archive /tmp/repo-core-only.zip --dest-root /tmp/aoa-skills --mode copy --execute --format json
```

Verify an installed profile/root against the current portable export:

```bash
python scripts/verify_skill_pack.py --repo-root . --profile repo-default --format json
python scripts/verify_skill_pack.py --repo-root . --profile repo-core-only --install-root /tmp/aoa-skills --format json
python scripts/verify_skill_pack.py --repo-root . --profile repo-project-core-outer-ring --install-root /tmp/aoa-skills --format json
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

## Narrow rollout lane

`repo-project-core-kernel` is the canonical bounded rollout profile for
installing the permanent explicit post-session project-core kernel:

- `aoa-session-donor-harvest`
- `aoa-automation-opportunity-scan`
- `aoa-session-route-forks`
- `aoa-session-self-diagnose`
- `aoa-session-self-repair`
- `aoa-session-progression-lift`
- `aoa-quest-harvest`

- It is `repo`-scoped.
- Its authored install mode stays `symlink-preferred`.
- Cross-repo rollout should use `copy` mode so the installed surface is
  reviewable and commit-safe.
- The intended target path is `<repo>/.agents/skills/`.
- This profile is for explicit post-session rollout and does not replace
  `repo-default`.

`repo-session-harvest-family` remains available as a backward-compatible
operational alias for the same seven-skill kernel when existing rollout or
automation surfaces still name the older profile.

This kernel is also repo-wide hard-gated in `aoa-skills`:

- every kernel skill must keep both its detail receipt schema and its generic
  core receipt schema
- the portable export must carry both refs for every kernel skill
- `generated/project_core_kernel_governance.min.json` is the per-skill gate
  readout
- `python scripts/release_check.py` fails if any kernel skill drifts out of
  that contract

`repo-project-core-outer-ring` is the canonical bounded rollout profile for the
stable engineering workbench around that kernel:

- `aoa-adr-write`
- `aoa-source-of-truth-check`
- `aoa-bounded-context-map`
- `aoa-core-logic-boundary`
- `aoa-port-adapter-refactor`
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `aoa-property-invariants`
- `aoa-invariant-coverage-audit`

- It is `repo`-scoped.
- Its authored install mode stays `symlink-preferred`.
- Cross-repo rollout should use `copy` mode so the installed surface is
  reviewable and commit-safe.
- The intended target path is `<repo>/.agents/skills/`.
- This profile is soft-gated through
  `generated/project_core_outer_ring_readiness.min.json`.
- It does not replace `repo-project-core-kernel`, and it does not pull in risk
  skills or project overlays.

`repo-core-only` is now the umbrella repo surface:

- it must equal `repo-project-core-kernel + repo-project-core-outer-ring` in
  canonical order
- it keeps the project-core shape explicit without turning the outer ring into a
  second kernel

`repo-quest-harvest-only` remains the narrow leaf rollout profile for
installing just `aoa-quest-harvest`.

- It is `repo`-scoped.
- Its authored install mode stays `symlink-preferred`.
- Cross-repo rollout should use `copy` mode so the installed surface is reviewable and commit-safe.
- The intended target path is `<repo>/.agents/skills/aoa-quest-harvest`.
- This profile is for explicit post-session rollout and does not replace `repo-default`.

`repo-session-donor-harvest-only` remains the nucleus-only profile for
repositories that want just the donor-harvest entry surface without the full
kernel.

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
- some repos need one narrow post-session skill without taking the full repo-default surface
- project overlays should stay project-local

This is a packaging layer, not a new source of truth.
