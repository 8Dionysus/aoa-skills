# AGENTS.md

Root route card for `aoa-skills`.

## Purpose

`aoa-skills` is the bounded execution canon of AoA.
It stores reusable, public-safe, Codex-facing skill bundles that package practice into reviewable workflows an agent can execute.
A skill is workflow meaning, not agent destiny.

## Owner lane

This repository owns:

- canonical skill bundle wording and workflow structure
- trigger boundaries, invocation posture, skill inputs and outputs
- skill-level technique dependency declarations
- generated catalogs, matrices, portable exports, and bridge manifests derived from canonical skills

It does not own:

- reusable technique truth in `aoa-techniques`
- proof doctrine in `aoa-evals`
- routing, memory, KAG, stats, playbook, or role truth in sibling repos
- live quest state, runtime inventory, or hidden control-plane authority

## Start here

1. `README.md`
2. `ROADMAP.md`
3. `docs/ARCHITECTURE.md`
4. `docs/BRIDGE_SPEC.md`
5. `docs/LAYER_POSITION.md`
6. `docs/RUNTIME_PATH.md`
7. `docs/COMPONENT_REFRESH_LAW.md` when skills export, portable projection, or installed skill refresh is in scope
8. the target `skills/*/SKILL.md`
9. affected generated or export surfaces
10. `docs/AGENTS_ROOT_REFERENCE.md` for preserved full root branches


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Route away when

- the source practice should be extracted or changed in `aoa-techniques`
- a claim needs proof in `aoa-evals`
- scenario composition belongs in `aoa-playbooks`
- role, progression, or checkpoint posture belongs in `aoa-agents`
- memory, routing, KAG, or stats meaning belongs in its owner repo

## Verify

Minimum canonical skill validation:

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
python scripts/build_catalog.py --check
```

Use the broader validation path in `docs/AGENTS_ROOT_REFERENCE.md` when matrices, portable exports, support resources, policy posture, or downstream bridges change.

## Report

Name the skill or skill-surface family, whether trigger boundaries or technique dependencies changed, what generated or export surfaces changed, and which checks ran.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including task-specific doc branches, audit contract, review priorities, and extended validation commands.
