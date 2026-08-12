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

An admitted v2 owner repository contains:

```text
skills/
├── port.manifest.json
└── <bundle-name>/
    ├── SKILL.md
    └── optional owner resources

$HOME/.codex/skills/<bundle-name>/   # one OS-profile managed copy
```

`skills/<bundle-name>/` is canonical. The owner retains procedure meaning,
version, lifecycle, admission, and resources. The v2 manifest declares that
its admitted bundles are eligible for consideration by `os-user-default`; it
does not select them into the current profile or create a repository copy. The
legacy exposure-mode value `profile-selected` names this target route, not
current profile membership.

`config/os_skill_profiles.json` is the source that selects eligible shared and
owner bundles into the current user catalog. A v2 repository must not expose
the same canonical bundle again at `.agents/skills/<bundle-name>`. This
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

Do not create new v1 ports. A v2 manifest intentionally blocks this builder and
routes installation to the OS profile instead. Retire v1 after every admitted
owner has moved and fresh-session profile trials have passed.

## Owner-source check

From the matching `aoa-skills` checkout:

```bash
python scripts/validate_home_skill_port.py --owner-root /path/to/owner
```

For v2 this checks source identity, admission reference, package shape, digest,
the exact exposure-eligibility declaration, and absence of a same-name
repository projection. It does not check current profile membership. For v1 it
preserves source/projection byte and executable-bit parity during migration.

A green check does not prove trigger quality, agent benefit, safety,
fresh-session discovery, user-profile installation, or cross-model behavior.

## Lifecycle

Re-run manual isolated, negative, held-out, coexistence, and effect cases after
material skill, model, host, tool, or owner-contract changes. Improve, merge,
split, deprecate, or retire at the owner home. Update the owner admission and
reinstall the OS profile. Remove the v1 compatibility code after the migration
contract disappears; do not preserve obsolete projections or green counts.
