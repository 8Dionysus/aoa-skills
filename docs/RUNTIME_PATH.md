# Runtime path

`RUNTIME_PATH.md` is the human guide for runtime skill use in `aoa-skills`.
It covers the operational path:

`pick -> inspect -> expand -> object use`

Use this guide when you are deciding what to do next inside the repository.
It is about runtime selection and bounded execution, not status signaling or derived governance.

If you need maturity, promotion, or public-product state, switch to `PUBLIC_SURFACE.md`.
If you need to judge behavior evidence, switch to `EVALUATION_PATH.md`.

The runtime path also has two derived local helpers:
- `../generated/skill_walkthroughs.md` for the human-readable walkthrough matrix
- `../scripts/inspect_skill.py --skill <name>` for read-only per-skill inspection

## Purpose

The goal of runtime inspection is to pick one bounded object, inspect only what is needed to use it safely,
expand only when the first object is not enough, and then apply that object without widening the task.

The object can be a skill, a workflow fragment, a local doc surface, or another bounded repo artifact.
The test is simple: can another agent or human still tell what object was chosen and why?

## The path

### 1. Pick

Choose the smallest object that plausibly fits the task.

Start with the target skill bundle when the task is skill-shaped.
If the task is not yet skill-shaped, choose the nearest bounded object and keep the selection explicit.

Pick using these questions:
- What is the user actually asking for?
- Which single skill or object is the closest bounded match?
- What would be the next smaller object if this one feels too large?

At this stage, do not optimize for public status, promotion readiness, or derived review artifacts.

### 2. Inspect

Read the chosen object closely enough to understand:
- intent
- trigger boundary
- inputs and outputs
- safety limits
- verification guidance
- any technique traceability that is already present

Inspect the object itself first:
- `skills/<skill-name>/SKILL.md`
- `skills/<skill-name>/techniques.yaml` or the local dependency source for that skill
- adjacent docs only if they clarify execution posture or boundary shape

Keep inspection local to the chosen object unless you hit a real boundary problem.

Useful local inspect surfaces:
- `python scripts/inspect_skill.py --skill <name> --view capsule`
- `python scripts/inspect_skill.py --skill <name> --view sections`
- `python scripts/inspect_skill.py --skill <name> --view full`
- `python scripts/inspect_skill.py --skill <name> --view walkthrough`
- `python scripts/inspect_skill.py --skill <name> --view evidence`

### 3. Expand

Expand only when the first object does not fully cover the task.

Expansion means you inspect a neighboring skill, a nearby doc, or a closely related object to sharpen the boundary.
It does not mean you widen the task into a broader program.

Good expansion looks like this:
- compare two adjacent skill boundaries
- check whether a task belongs in a sibling skill instead
- inspect a local doc that explains the repository layer you are touching

Bad expansion looks like this:
- pulling in unrelated governance state
- using public promotion signals to decide runtime execution
- turning a bounded task into a repo-wide rewrite

### 4. Object use

Use the chosen object to perform the task, then stop.

Object use should leave a clear trace:
- what object was selected
- what boundary was respected
- what changed as a result
- what was intentionally left untouched

If the object proves insufficient, return to `Pick` and choose again.
Do not keep expanding indefinitely.

## What belongs here

This guide covers runtime questions such as:
- which skill to use
- how to read a skill bundle
- how to compare neighboring skill boundaries
- how to keep an action bounded while you execute it

This guide does not cover:
- public status
- promotion rules
- evaluation evidence
- evaluated/canonical signaling
- derived review surfaces
- release metadata
- generated public-product summaries

Those belong in `EVALUATION_PATH.md`, `PUBLIC_SURFACE.md`, and the generated surface docs.

## Practical check

Before acting, confirm all three:
- the chosen object is bounded
- the trigger boundary still matches the task
- the next action is still reversible or reviewable

If any of those fail, expand the inspection step or pick a smaller object.

## Future stubs

TODO: if runtime selection ever needs a cross-repo route map, keep it as a separate routing surface rather than embedding live fetches here.

TODO: if evaluation evidence becomes part of runtime selection, reference the existing repo-local surface instead of turning this guide into promotion doctrine.

TODO: if playbook-level composition becomes necessary, keep it above the skill layer and only point here from the smallest usable object.
