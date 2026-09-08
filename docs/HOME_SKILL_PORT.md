# Repository Skill Home Port

This contract lets a repository own its admitted callable procedures while an
OS-level Codex profile makes selected owner bundles globally discoverable.
`aoa-skills` owns the common grammar and assembly route; it does not acquire
owner procedure truth.

## Admission comes first

Create a top-level `skills/` home only after manual work establishes a
repository-specific bundle with:

- a stable independent trigger and negative applicability;
- a distinct input/output contract and useful composition boundary;
- held-out benefit over no skill and the likely containing bundle;
- acceptable coexistence with the prompt-visible library;
- an owner decision that records the evidence-backed admission.

Do not create an empty port, keep candidates here, or turn ordinary
instructions, facts, tools, tests, validators, or playbooks into skills. Raw
trials and task-local DAGs remain in the session or runtime.

## Canonical owner source, OS user profile, and duplicate boundary

An admitted v2 or v3 owner repository contains:

```text
skills/
├── port.manifest.json
└── <bundle-name>/
    ├── SKILL.md
    └── optional owner resources

$HOME/.codex/skills/<bundle-name>/   # one OS-profile managed copy
```

`skills/<bundle-name>/` is canonical. The owner retains procedure meaning,
version, lifecycle, admission, and resources. A v2 manifest declares one
Codex/user eligibility contour for `os-user-default`; a v3 manifest declares
an `exposures` array of eligibility contours and may contain more than one
runtime, scope, or profile contour. Each v3 exposure names a non-empty unique
subset of the admitted bundles, while an empty array is valid for an
owner-only home. Runtime, scope, and profile are safe lowercase kebab case
identifiers; the v3 mode is the literal `profile-eligible`. The common
contract does not enumerate particular hosts.

The target Codex user-profile adapter matches
`runtime=codex`, `scope=user`, `profile=os-user-default`, and
`mode=profile-eligible` for v3. V2 keeps its legacy
`mode=profile-selected` contour and exact bundle-list semantics. An exposure
declares eligibility for a consumer contour; it does not select bundles into
the current profile or create a repository copy. A bundle may remain admitted
and represented in the capability graph while being absent from every
exposure.

To migrate a v2 manifest, wrap its single `exposure` object in an
`exposures` array, change `mode=profile-selected` to
`mode=profile-eligible`, and preserve its bundle list and profile membership.
To roll back, retain the v2 source manifest and the same prior adapter, then
validate and install through the owner installer so the install receipt remains
authoritative; do not copy files manually.

`config/os_skill_profiles.json` is the source that selects eligible shared and
owner bundles into the current user catalog. A v2 or v3 repository must not
expose the same canonical bundle again at `.agents/skills/<bundle-name>` when
a Codex/user exposure names that bundle. This
prevents the duplicate prompt-visible definitions observed when Codex entered
an owner repository. Unrelated repository-only bundles may still use
`.agents/skills` when their own owner and consumer contract requires that
scope.

The profile assembler and installer own destination collision checks,
provenance, managed-entry cleanup, and installed byte/mode parity. This owner
validator does not claim that the profile is installed or visible in a live
session.

The managed install receipt at
`$HOME/.codex/skills/.aoa-os-skill-profile.json` is the machine-local
source-return handle. Each installed entry records the owner repository,
absolute owner root, repository-relative source path, owner ref, dirty posture,
version, complete installable-package digest, prompt-description hash, and
source fingerprint. When the owner also exposes a capability home, the receipt
records that graph's source hash and its authored package fingerprint; the
latter excludes generated projections to avoid a self-referential digest.
Owners without a capability home use the complete package digest as their
source fingerprint and label that scope explicitly. A bundle must resolve back
to the same admitted owner package before owner-relative procedure or contract
reads. These identity dimensions let later reviewed evidence distinguish
source, installed, and prompt-visible state. They do not prove selection,
execution, runtime health, routing quality, or successful use. A missing,
ambiguous, dirty, or stale handle blocks source-dependent claims; it never
authorizes searching sibling repositories or temporary fixtures for a
plausible copy.

Normal installation is fail-closed for every dirty Git owner source. The
installer permits `--allow-dirty-source` only with a separate explicit
non-production `--dest-root`, so a candidate worktree cannot be installed into
the normal user catalog under that exception. The dirty posture remains in
both the per-bundle source handle and aggregate receipt.

`--check` verifies installed package bytes and executable modes, the exact
per-bundle source handle, the aggregate managed receipt, and absence of stale
managed entries. Repeating `--execute` on a current profile is a no-op and
preserves the original installation timestamp. Replacing an unrelated
same-name entry and pruning a formerly managed entry each require their own
explicit reviewed flag; unrelated names are preserved.

## Transitional v1 compatibility

`aoa_skill_home_port_v1` remains readable only while existing owners migrate.
It declares an exact generated repository copy at `.agents/skills` and keeps
the old preview, write, and explicit-prune commands:

```bash
python scripts/build_home_skill_projection.py --owner-root /path/to/v1-owner
python scripts/build_home_skill_projection.py --owner-root /path/to/v1-owner --execute
python scripts/build_home_skill_projection.py \
  --owner-root /path/to/v1-owner --execute --prune
```

Do not create new v1 ports. A v2 or v3 manifest intentionally blocks this
builder and routes installation to the OS profile instead. Retire v1 after
every admitted owner has moved and fresh-session profile trials have passed.

## Owner-source check

From the matching `aoa-skills` checkout:

```bash
python scripts/validate_home_skill_port.py --owner-root /path/to/owner
```

For v2 and v3 this checks source identity, admission reference, package shape,
digest, the exposure-eligibility declaration, and absence of a same-name
repository projection for Codex/user-exposed bundles. It does not check
current profile membership. For v1 it preserves source/projection byte and
executable-bit parity during migration.

A green check does not prove trigger quality, agent benefit, safety,
fresh-session discovery, user-profile installation, or cross-model behavior.

## Lifecycle

Re-run manual isolated, negative, held-out, coexistence, and effect cases after
material skill, model, host, tool, or owner-contract changes. Improve, merge,
split, deprecate, or retire at the owner home. Update the owner admission and
reinstall the OS profile. Remove the v1 compatibility code after the migration
contract disappears; do not preserve obsolete projections or green counts.
