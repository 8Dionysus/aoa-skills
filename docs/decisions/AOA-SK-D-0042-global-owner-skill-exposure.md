# Global Owner Skill Exposure

- Decision ID: AOA-SK-D-0042
- Status: Accepted
- Date: 2026-07-17
- Owner surface: `schemas/skill-home-port.schema.json`,
  `docs/HOME_SKILL_PORT.md`, and the OS user-profile contract

## Index Metadata

- Original date: 2026-07-17
- Surface classes: skill source, export/runtime, owner boundary, validation
- Skill lanes: repository-home, portable/export
- Mechanic parents: release-support, cross-mechanic
- Guard families: source topology, owner boundary, export/runtime, manual admission
- Posture: accepted global owner-skill exposure

## Context

AOA-SK-D-0040 and AOA-SK-D-0041 correctly established owner-local
`skills/` truth, but made an admitted owner bundle discoverable through a
repository `.agents/skills` copy. Fresh Codex inspection then showed that
user-level and repository-level copies with the same name both enter the
prompt-visible catalog. The owner function therefore becomes globally
discoverable only after installation, yet becomes duplicated and competing
when the agent enters its own repository.

The first real v2 consumer, `aoa-stats`, removed its duplicate repository copy
and declared `os-user-default` exposure. Its GitHub check failed because the
published common action still accepted only the v1 repository-projection
shape. A manual contract trial then established three distinct cases:

- a clean v2 owner source without a same-name repository copy is valid;
- the same v2 source with `.agents/skills/aoa-stats` is a collision and must
  fail;
- an existing exact v1 repository projection remains valid during migration.

## Options Considered

- Revert owner bundles to v1 repository-only projection and defer global
  discovery.
- Replace v1 immediately with a v2-only contract and break every owner that
  has not migrated.
- Make v2 OS-user exposure the standard, retain explicit v1 compatibility
  during migration, and reject only same-name repo duplication for v2 bundles.

## Decision

Choose the third option.

### OS user profile and same-name repository boundary

1. Canonical procedure truth remains `<owner-repo>/skills/<bundle-name>/`.
2. An admitted v2 owner manifest selects its advertised bundles for the
   `os-user-default` profile. Assembly and installation remain an
   `aoa-skills` responsibility; procedure meaning remains with the owner.
3. A v2 owner must not also expose the same canonical bundle name under its
   repository `.agents/skills`.
4. Repository-only procedures may still use their repository scope when they
   are not also selected by the OS user profile. This decision is not a ban on
   repository skills.
5. V1 remains a deprecated compatibility route with exact repo-projection
   parity until admitted owners migrate. New owner ports use v2.
6. The common validator checks owner source shape, exposure declaration, and
   same-name repo duplication. It does not claim user-profile installation,
   live discovery, routing quality, safety, or outcome benefit.
7. V1 is removed only after owner migration, clean profile installation, and
   fresh-session coexistence trials establish the replacement.

## Rationale

Global exposure preserves the functional reason for skills: a new agent can
notice `memo`, `evals`, `stats`, KAG, and other owner capabilities before it
already knows their repository. One canonical owner source prevents semantic
drift. One user-level materialization avoids same-name prompt competition.
Temporary v1 compatibility protects already admitted consumers without
turning the old topology back into the target architecture.

## Consequences

- Positive: owner functionality can become globally discoverable without
  transferring its truth to `aoa-skills`.
- Positive: entering an owner repository no longer needs to duplicate the
  globally advertised skill.
- Tradeoff: the system must carry two manifest shapes during migration.
- Tradeoff: v2 owner validation cannot prove the user profile is actually
  installed; profile assembly, install parity, and fresh-session inspection
  remain separate required evidence.
- Follow-up: land the profile assembler, migrate each admitted owner, install
  one clean OS profile, then retire v1 and its builder.

## Current Applicability

As of 2026-07-17:

- v2 source/exposure validation and same-name duplicate rejection are ready
  for owner adoption;
- v1 remains accepted only as migration compatibility;
- this change publishes the common action support needed by the staged
  `aoa-stats` v2 consumer;
- global installation and full-catalog fresh-session proof remain incomplete.

## Boundaries

Do not infer that fewer files are inherently better, that repository skills
are forbidden, that a manifest makes a bundle useful, or that a green owner
check proves global discovery. This decision changes exposure topology, not
owner admission criteria, procedure authority, or runtime safety enforcement.

## Validation

- Reproduce the clean v2, duplicate v2, and exact v1 cases manually.
- Validate both schema branches and the existing path, source, residue, and
  symlink invariants.
- Run the focused owner-port test, repository tests, decision-index parity,
  source-fast, and release lanes.
- Re-run the real `aoa-stats` GitHub consumer after pinning the landed action.
