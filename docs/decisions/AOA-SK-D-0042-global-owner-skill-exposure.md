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
2. An admitted v2 owner manifest declares which bundles are eligible for OS
   user exposure. Selection into `os-user-default` is a separate curated
   `aoa-skills` profile decision and may change with lifecycle, coexistence,
   routing, or context-budget evidence without revoking owner admission.
   Assembly and installation remain an `aoa-skills` responsibility; procedure
   meaning remains with the owner.
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
Admission makes a bundle eligible for that materialization; it does not make
global exposure permanent or bypass profile curation. Temporary v1
compatibility protects already admitted consumers without turning the old
topology back into the target architecture.

## Consequences

- Positive: owner functionality can become globally discoverable without
  transferring its truth to `aoa-skills`.
- Positive: entering an owner repository no longer needs to duplicate the
  globally advertised skill.
- Tradeoff: owner admission and current global selection are separate states;
  operators must inspect the current profile rather than infer installation
  from an owner manifest alone.
- Tradeoff: the system must carry two manifest shapes during migration.
- Tradeoff: v2 owner validation cannot prove the user profile is actually
  installed; profile assembly, install parity, and fresh-session inspection
  remain separate required evidence.
- Follow-up: land the profile assembler, migrate each admitted owner, install
  one clean OS profile, then retire v1 and its builder.

## Current Applicability

As of 2026-08-12:

- the owner homes in scope have landed in `aoa-evals`, `aoa-memo`,
  `aoa-stats`, `aoa-kag`, `aoa-sdk`, `aoa-agents`, `abyss-stack`,
  `abyss-machine`, and `ATM10-Agent`;
- the current `os-user-default` profile selects sixteen unique managed-copy
  front doors from shared and owner homes for `~/.codex/skills`, and verifies
  two owner-managed session-memory links without assuming authority to mutate
  them;
- every installed package and the aggregate profile receipt is current against
  its selected clean candidate source, and unrelated user entries remain
  preserved;
- `aoa-evals`, `aoa-memo`, `aoa-stats`, `aoa-kag`, progression, summon,
  Artifact Trust, diagnostic, and both local `.aoa` session-memory routes are
  included alongside the seven shared bundles;
- the three Titan owner bundles remain admitted owner-local procedures and
  represented in the semantic capability graph, but are deferred from the
  default global profile after current lifecycle and context-budget review;
- prior fresh-session Titan trials remain historical evidence for the earlier
  exposed state, not evidence that Titan is currently selected; current
  fresh-session cases continue to cover bounded `aoa-stats`, evaluation-family
  composition, and their nearest negatives;
- those trials exposed and then retested three material defects: an optional
  graph hash serialized as JSON null, eval discovery widening after an exact
  owner-port fit, and a bounded stats answer running the repository release
  gate;
- v1 remains accepted only as migration compatibility; retirement still
  requires every admitted owner to migrate and the current profile to retain
  clean installation and fresh-session coexistence evidence across supported
  hosts and models.

## Review Log

### 2026-08-12 - Separate owner admission from current profile selection

- The accepted wording incorrectly made every advertised v2 owner bundle look
  permanently selected into `os-user-default`; the actual profile is a curated
  lifecycle and coexistence surface owned by `aoa-skills`.
- The active owner-port contract and schema now state that the v2 exposure
  declaration is eligibility for the named route; current membership comes
  only from `config/os_skill_profiles.json`.
- The three Titan bundles remain valid in their owner home and semantic graph,
  but their global visibility is deferred and their managed copies are absent
  from the default profile.
- The current profile contains sixteen managed copies plus two verify-only
  owner links. This amendment preserves the original global-discovery route
  while preventing future agents from reconstructing the obsolete Titan
  exposure from an admitted owner manifest.

### 2026-07-26 - Preserve owner-installed user links in the aggregate profile

- A real post-landing check exposed an ownership collision: the aggregate
  `managed-copy` installer treated the two `aoa-session-memory` user links as
  unmanaged objects even though their owner provides the canonical
  `install-user-skill` operation.
- The OS profile now distinguishes copied packages from verify-only
  `owner-link` entries. An owner link is current only when the prompt-visible
  target is a symlink resolving exactly to the declared owner skill source.
- The aggregate installer records that observed identity but never creates,
  replaces, repairs, or prunes the owner link. Missing, conflicting, broken, or
  misdirected links stop with an owner-installer handoff before managed-copy
  mutation.
- Both advertised session-memory routers are listed so the profile verifies the
  actual global surface instead of silently preserving an untracked second
  route.

### 2026-07-23 - Repair installed-copy return before claiming global exposure

- A real non-production installation exposed an integration defect that owner
  validators had not found: the assembler emitted
  `aoa_skill_source_receipt_v2`, while nearly every admitted owner skill
  required exactly v1. Installation looked green, but returning to canonical
  owner source failed.
- The affected owner packages now accept v1 or v2. V2 requires non-empty
  package digest, source fingerprint and scope, prompt-description hash, and
  preserves the capability-graph hash when present. Missing v2 identity fails
  closed; v1 remains a bounded compatibility path.
- Manual proof used a real installed v2 `aoa-evals` package, a synthetic valid
  v1 shape, and a malformed v2 shape. The first two returned canonical source;
  the malformed v2 stopped before owner use. A separate fresh diagnostic
  session demonstrated the same v2 return in natural execution.
- The final user-root preview found three unmanaged collisions. The stale
  `aoa-decision` and `aoa-kag` projections were replaced after inspection; the
  `.aoa` route was materialized byte-identically from its local owner home.
  No `.aoa` source skill was edited.

### 2026-07-23 - Close owner landing and retest behavior, not only packaging

- All owner-home changes in this migration slice landed before their final
  references were admitted into the central capability graph.
- Natural fresh-session trials were treated as the primary behavioral
  evidence. Existing validators remained structural guards and were not
  expanded to encode the trial narratives.
- The Titan retry returned through a valid v2 source handle and stopped at a
  no-effect plan. The stats retry stayed on one bounded owner observation. The
  eval retry formed a two-node task-local DAG and ran exactly one selected
  owner validator.
- Negative cases kept exact-source reading out of KAG retrieval and ordinary
  arithmetic out of `aoa-stats`. A live, unreviewed-session promotion request
  stopped before promotion, but its session-memory router performed an
  unnecessarily broad read-only lookup; that separate owner surface was not
  changed here.
- These results establish behavior only for the exercised model, host,
  sources, and prompts. They do not establish universal routing accuracy,
  cross-model parity, or benefit for every owner bundle.

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
