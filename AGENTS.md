# AGENTS.md

## Applies to

This root card applies to the whole repository unless a nearer nested
`AGENTS.md` narrows the lane.

## Role

This AGENTS card keeps local work inside the `aoa-skills` bounded execution
lane, names the nearest owner boundary, and routes wider claims to the owning
surface.

It is the agent-facing route law for this repository. It does not replace
`README.md`, `CHARTER.md`, `DESIGN.md`, `DESIGN.AGENTS.md`,
`docs/ARCHITECTURE.md`, `mechanics/README.md`, or local source truth.

## Read before editing

Read this root card first. Then read the nearest nested `AGENTS.md` for every
touched path, followed by the route-mode surface and the nearest `README.md`,
`SKILL.md`, `techniques.yaml`, config, schema, builder, validator, or source
surface that owns the local claim.

For changes to `AGENTS.md` card shape, root-to-local precedence, generated
agent-facing companions, portable skill guidance, or adapter vocabulary in route
law, also read `DESIGN.AGENTS.md`.

For changes to skill-layer form, source topology, generated/export posture,
activation boundaries, or layer relationships, also read `DESIGN.md`.

For changes to repository authority, owner boundaries, root posture, or claims
about what `aoa-skills` may own, also read `CHARTER.md`.

## Boundaries

Do not use this lane to override authored skill bundles, generated-source
boundaries, sibling-repo authority, review evidence, release validation
contracts, or downstream adoption receipts.

Core skill meaning should use neutral local coding-agent language. Codex,
OpenAI, MCP, and other platform names belong where an adapter, compatibility
schema, export profile, or runtime seam actually requires them.

## Validation

Run the nearest validator named by this card or a nearer local card. For
growth-facing repository changes, use `python scripts/ci_gate.py --mode
source-fast`. For release-facing changes, use `python scripts/ci_gate.py --mode
release` or `python scripts/release_check.py --include-packaging-smoke`.

For root guidance changes, at minimum run:

```bash
python scripts/validate_agents_design.py
python scripts/validate_nested_agents.py
python scripts/build_catalog.py --check
```

## Closeout

Closeout must name changed surfaces, checks run, checks skipped, remaining risk,
decision review result, generated/export refresh result when relevant, and the
next owner route if this repository was only a waypoint.

## Purpose

`aoa-skills` is the bounded execution canon of AoA.
It stores reusable, public-safe skill bundles that package practice into
reviewable workflows a local coding agent can execute.
A skill is workflow meaning, not agent destiny.
For the full authority boundary, use `CHARTER.md`.

## Owner lane

This repository owns:

- canonical skill bundle wording and workflow structure;
- trigger boundaries, invocation posture, skill inputs and outputs;
- skill-level technique dependency declarations;
- generated catalogs, matrices, portable exports, and bridge manifests derived
  from canonical skills;
- repo-local mechanics that govern skill-layer movement, adoption, export,
  recurrence, checkpoint carry, quest integration, and review pressure.

It does not own:

- reusable technique truth in `aoa-techniques`;
- proof doctrine in `aoa-evals`;
- routing, memory, KAG, stats, playbook, or role truth in sibling repos;
- live quest state, runtime inventory, downstream adoption truth, or hidden
  control-plane authority.

## Start here

For first reading or outside orientation, use this route:

1. `README.md`
2. `CHARTER.md`
3. `DESIGN.md`
4. `SKILL_INDEX.md`
5. `docs/ARCHITECTURE.md`
6. `mechanics/boundary-bridge/docs/LAYER_POSITION.md`

For agent editing, use this route:

1. this `AGENTS.md`
2. nearest nested `AGENTS.md` for every touched path
3. route-mode surface from the table below
4. nearest local source surface: `SKILL.md`, `techniques.yaml`, package
   `README.md`, config, schema, builder, validator, test, or generated-source
   owner
5. narrowest relevant validator before broader gates

For canonical skill bundle work, also read:

1. `skills/AGENTS.md`
2. the target lane `AGENTS.md`
3. the target `skills/**/SKILL.md`
4. the target `skills/**/techniques.yaml`
5. any touched `checks/`, `examples/`, `references/`, `agents/openai.yaml`, or
   bundle-local scripts/assets

## Route modes

Use the named route before widening a skill-layer claim:

| Route mode | Use when | First surface |
|---|---|---|
| `first-reading` | you need the shortest honest repository overview | `README.md` |
| `authority-boundary` | repository authority, owner split, or root posture changes | `CHARTER.md` |
| `system-design` | skill-layer form, topology, export posture, or layer relationship changes | `DESIGN.md` |
| `agent-surface-design` | AGENTS shape, local-card placement, route modes, closeout, or portable agent guidance changes | `DESIGN.AGENTS.md` |
| `skill-editing` | canonical skill bundle wording, trigger boundary, invocation, technique metadata, or support artifacts change | `skills/AGENTS.md` |
| `mechanic-change` | owner-local skill movement, package routes, active parts, provenance, roadmap contours, or mechanic validation change | `mechanics/README.md` |
| `direction-change` | roadmap, future contour, package priority, or durable deferred work changes | `mechanics/ROADMAP.md` |
| `bridge-boundary` | technique links, skill-technique exchange, owner split, or cross-repo boundary posture changes | `mechanics/boundary-bridge/docs/LAYER_POSITION.md` |
| `runtime-use` | selecting, inspecting, expanding, or using a skill object changes | `mechanics/release-support/docs/RUNTIME_PATH.md` |
| `export-refresh` | `.agents/skills/*`, portable projection, installed packs, support resources, or component refresh posture changes | `mechanics/release-support/docs/COMPONENT_REFRESH_LAW.md` |
| `generated-surface` | generated catalogs, manifests, matrices, runtime cards, or derived reader surfaces change | `generated/AGENTS.md` |
| `public-status` | status, governance, evaluation, promotion pressure, overlay readiness, or public claim changes | `mechanics/audit/docs/PUBLIC_SURFACE.md` |
| `low-context-agent` | a compact machine route is needed first | `SKILL_INDEX.md` |

## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for
  every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and
  the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local
  checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived,
  runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language
  must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the
  next agent should resume.

## Memory route

For skill-layer recall, continuity, compaction recovery, comparison with past
work, or preserved lessons, start with `aoa-memo` and the workspace memory map.
Session grounding routes through `.aoa`; local candidate writing routes through
this repository's `memo/` port when that port exists; durable reviewed memory
lands through `aoa-memo`.

## Decision review

After structural, ownership, workflow, route-law, validator-authority,
public-contract, export-posture, or topology changes, check whether future
agents will need a decision record to understand why the path was chosen. Use
`docs/decisions/` for repo-local decisions.

If no record is needed, say so in closeout.

## GitHub landing workflow

Root `AGENTS.md` owns the repository-wide branch, PR, CI, and merge route.
`.github/AGENTS.md` owns the GitHub-native files that support it.

When the user asks to commit, push, and merge in this repository, use this
route:

1. Start from a branch based on the current `origin/main`. If the worktree is
   already dirty, inventory it first and carry forward only the intended diff.
2. Commit the intended change with a message that names the changed surface.
3. Push the branch and open a pull request that states changed surfaces,
   validation run, skipped checks, and remaining risk.
4. Wait for GitHub `Repo Validation` and any required GitHub checks. If a check
   fails, fix the branch and wait for the new result.
5. Merge through GitHub after green validation. Use squash unless repository
   settings report a different required method; report the method that landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree
   is clean before closeout.

If GitHub status or merge permissions cannot be observed, stop the landing route
and report the exact blocker instead of guessing.

## Post-change route review

Before closeout, check whether the change actually affects these surfaces.
Update only the ones that moved; otherwise say no update was needed.

- `DESIGN.md` when skill-layer form, topology, source/export posture, adapter
  vocabulary, activation boundaries, or layer relationships changed.
- `CHARTER.md` when repository authority, owner boundaries, root posture, or
  what this repo may claim changed.
- `DESIGN.AGENTS.md` when agent-facing form, card shape, route modes, closeout
  expectations, generated companions, or portable agent guidance changed.
- `README.md` or `docs/README.md` when first-reading or docs-map routes changed.
- `docs/ARCHITECTURE.md` when the technical model or source/generated/export
  distinction changed.
- `mechanics/ROADMAP.md` when direction, package priority, future contour, or
  deferred durable work changed.
- `CHANGELOG.md` when release-visible behavior, public docs, validation, or
  repository structure changed.
- `docs/decisions/` when future agents need the rationale for a route,
  ownership, workflow, validator, public-contract, export, or topology choice.
- generated surfaces, builders, validators, and tests when a source-backed
  machine capsule changed.
- mechanic `LANDING_LOG.md`, `OWNER_REQUESTS.md`, `PARTS.md`, `PROVENANCE.md`,
  or `ROADMAP.md` when a mechanic landing, owner request, active part, legacy
  bridge, or future contour changed.
- `QUESTBOOK.md` or `quests/` when a durable obligation should survive the diff.
- neighboring owner repositories when the change routes or constrains their
  truth.

## Route away when

- the source practice should be extracted or changed in `aoa-techniques`;
- a claim needs proof in `aoa-evals`;
- scenario composition belongs in `aoa-playbooks`;
- role, progression, or checkpoint posture belongs in `aoa-agents`;
- memory, routing, KAG, or stats meaning belongs in its owner repo;
- runtime budgets, service state, storage, or frontend presentation belongs in
  `abyss-stack`;
- typed helpers, compatibility, activation, or handoff tooling belongs in
  `aoa-sdk`;
- source-linked knowledge or interpretation belongs in `Tree-of-Sophia`.

## Hard no

- Do not absorb technique, proof, routing, memory, KAG, stats, playbook, role,
  runtime, downstream, or ToS source truth into `aoa-skills`.
- Do not let generated catalogs, matrices, manifests, exported packs, runtime
  cards, or derived reports masquerade as source authority.
- Do not hand-edit generated or exported files when the source, config, or
  builder should move instead.
- Do not turn a root README, docs map, roadmap, or changelog into an archive of
  every wave, package, or session note.
- Do not hide semantic changes under "docs-only", "metadata-only", or
  formatting wording.
- Do not use adapter-specific names as core skill meaning unless the surface is
  actually an adapter, compatibility, profile, or export layer.
- Do not let quest, RPG, checkpoint, recurrence, progression, or self-agency
  language imply live runtime state, ledger ownership, proof authority, or
  unreviewable autonomy.

## Review-critical drift

Treat these as high-risk findings in this repository:

- contradictions across `README.md`, `CHARTER.md`, `DESIGN.md`,
  `DESIGN.AGENTS.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `mechanics/README.md`,
  `mechanics/ROADMAP.md`, `skills/AGENTS.md`, and generated source-backed
  capsules;
- routing that points readers to the wrong owner repository or skill-layer
  surface;
- generated or exported surfaces changed without their source docs, config,
  builders, validators, or tests;
- public status, promotion, adoption, or evaluation claims that are not
  supported by review evidence;
- skill-layer claims that silently absorb sibling-owner implementation, proof,
  routing, runtime, memory, role, or scenario meaning.

## Verify

Minimum canonical skill validation:

```bash
python scripts/ci_gate.py --mode source-fast
```

Generated/readout, export, release, and nightly checks are separate lanes:

```bash
python scripts/ci_gate.py --mode generated --group all
python scripts/ci_gate.py --mode generated --group export
python scripts/ci_gate.py --mode generated --group runtime
python scripts/ci_gate.py --mode export
python scripts/ci_gate.py --mode release
python scripts/ci_gate.py --mode nightly
```

For broader validation, follow the nearest package `AGENTS.md`,
`scripts/AGENTS.md`, and `mechanics/release-support/AGENTS.md` plus the
specific owner docs they name. Use `docs/AGENTS_ROOT_REFERENCE.md` only for
preserved validation intent, not as the active command source.

Run `python scripts/validate_nested_agents.py` whenever an `AGENTS.md` card is
added or changed.

## Report

Name the skill or skill-surface family, whether trigger boundaries or technique
dependencies changed, what generated or export surfaces changed, whether
decision review changed any follow-up surface, and which checks ran.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance,
including task-specific doc branches, audit contract, review priorities, and
historical validation intent.
