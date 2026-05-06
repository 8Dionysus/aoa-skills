# AGENTS.md

Route card for the `aoa-skills/mechanics/` surface.

## Purpose

`mechanics/` owns skill-layer movement surfaces for `aoa-skills`.
These files describe how bounded workflow candidates, support layers, export
surfaces, checkpoint carry, recurrence pressure, adoption pressure, and
downstream bridge signals move around skill canon.

Mechanics are not canonical skill bundles. They shape the route into or around
canon, while `skills/` owns executable skill content and `generated/` owns
derived reader evidence.

## Owner lane

This surface owns:

- owner-local movement grammar for candidate-to-skill flow inside the AoA
  mechanics vocabulary
- bounded skill-side candidate intake, adoption, audit, recurrence,
  checkpoint, questbook, release-support, Agon, antifragility, boundary-bridge,
  experience, growth-cycle, method-growth, and RPG routes
- public-safe stop-lines for deciding when a surface must hand off to another
  AoA repository
- package-local active parts and provenance bridges that are too procedural for
  flat `docs/` but not skill bundles

It does not own:

- canonical skill bundle meaning, which belongs under `skills/`
- generated catalogs, manifests, runtime cards, or export truth, which belongs
  under `generated/`, `.agents/skills/`, and the scripts that build them
- reusable technique truth, which belongs in `aoa-techniques`
- proof doctrine, which belongs in `aoa-evals`
- routing policy, which belongs in `aoa-routing`
- scenario composition, which belongs in `aoa-playbooks`
- role, memory, KAG, stats, runtime infrastructure, or downstream project truth

## Start here

1. Read the repository root `AGENTS.md`, `README.md`, and `ROADMAP.md`.
2. Read `docs/LAYER_POSITION.md`, `docs/ARCHITECTURE.md`,
   `docs/BRIDGE_SPEC.md`, and `docs/RUNTIME_PATH.md`.
3. Read `mechanics/README.md`.
4. Read the nearest package README, starting with its local `Mechanic card`.
5. If the package has `DIRECTION.md`, `PARTS.md`, `PROVENANCE.md`,
   `LANDING_LOG.md`, `ROADMAP.md`, or `parts/`, use those active route
   surfaces before opening historical material.
6. If a package change touches skill bundles, generated/export outputs,
   reviews, quests, or config, follow the nearest nested `AGENTS.md` there too.

## Local law

- Mechanics may route, constrain, stage, and preserve movement, but they do not
  silently promote candidates into `skills/`.
- Every cross-repo handoff must name the stronger owner and stop-line rather
  than importing that owner's authority into this repository.
- Package README cards use `Local owns`, not `Center owns`.
- Generated artifacts remain evidence or export companions, not authority.
- Legacy or source-preservation surfaces preserve lineage. They are not a junk
  drawer, and they must not be the only place current active behavior lives.
- When a mechanic grows beyond a simple README, prefer the AoA split:
  `DIRECTION.md`, `PARTS.md`, `PROVENANCE.md`, `LANDING_LOG.md`, `ROADMAP.md`,
  `parts/`, and package-local `legacy/` when source lineage must be preserved.
- If a mechanics surface becomes an executable skill bundle with stable trigger
  boundaries, inputs, outputs, risks, and verification, promote it through the
  normal `skills/` review path instead of letting it sprawl here.

## Verify

Use the root validation path after mechanics changes:

Run `python scripts/validate_nested_agents.py` whenever a mechanics `AGENTS.md`
file is added or changed.

```bash
python scripts/build_catalog.py --check
python scripts/validate_skills.py --fail-on-review-truth-sync
python scripts/validate_nested_agents.py
python -m unittest discover -s tests
```

If a package touches generated/export, recurrence, Agon, tiny-router, support
resources, or release-manifest surfaces, run the named package-local and root
validators before closeout.

## Report

Name the mechanics package changed, which active parts moved, whether skill
meaning changed, whether generated/export surfaces changed, what validation
ran, what was skipped, and where the next package should resume.
