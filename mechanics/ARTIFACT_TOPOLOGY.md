# Mechanic Artifact Topology

## Purpose

`aoa-skills` mechanics are not flat documentation bins. A mechanic may own the
schemas, examples, seed config, generated companions, scripts, tests, and
manifest records that make its local contract usable.

This topology keeps root technical districts for repository-wide contracts while
placing mechanic-owned substance beside the mechanic package or nearest part.
It owns placement law only. It does not replace package cards, provenance,
landing logs, generated read models, or canonical `skills/**/SKILL.md` bundles.

## Root Lane

Root technical districts own repo-wide contracts:

- `config/`: portable export, pack profiles, policy, project-core rings,
  runtime guardrails, trigger-eval policy, and tiny-router inputs.
- `examples/`: root-owned examples that are not owned by one mechanic.
- `generated/`: repo-wide catalogs, export maps, runtime manifests, public
  read models, and mechanic-built root-published summaries.
- `manifests/`: manifest routing cards and future root registry, not mechanic
  record storage.
- `schemas/`: repo-wide skill, export, governance, release, and public surface
  shape contracts shared across packages or readers.
- `scripts/`: deterministic root builders, validators, reports, inspectors,
  release checks, and shared helpers.
- `tests/`: root contract tests for repo-wide behavior and cross-package
  invariants.
- `quests/`: durable public obligation items organized by lifecycle state.

Root districts must not keep mechanic-owned aliases. When an artifact only makes
sense inside one mechanic or part, route callers to the owning path directly.

## Mechanic Lane

Mechanic-owned artifacts live under their package. For mechanics with active
parts, prefer the nearest owning part:

```text
mechanics/<slug>/
  parts/<part>/
    schemas/
    examples/
    config/
    generated/
    manifests/
    scripts/
    tests/
```

Use these homes when the artifact is local to the mechanic's boundary:

- Agon skill-binding and epistemic candidate contracts belong under their
  candidate bridge parts. Root `generated/agon_*.min.json` remains a
  root-published read model over those part-owned sources.
- Checkpoint note contracts belong under `mechanics/checkpoint/`.
- Method-growth owner-status, followthrough, adoption, regression, retention,
  and pattern-handoff contracts belong under `mechanics/method-growth/`.
- Experience governance, office, installation, service handoff, receipt,
  rollback, and policy-hold contracts belong under `mechanics/experience/`.
- Quest object and quest dispatch contracts belong under
  `mechanics/questbook/`, while root `quests/` remains the public item store.

When a mechanic-owned artifact moves, update callers, validators, docs, tests,
and generated builders to use the owning path. Do not leave a root copy, flat
alias, or compatibility duplicate.

Package-local `legacy/`, seed, and landing receipt districts are allowed when
they preserve source lineage without becoming alternate active routes.

## Skill Canon

Mechanic artifacts may prepare, validate, or publish evidence around skill
movement. They do not become canonical skill bundles by location. Executable
skill meaning remains under `skills/`, and the flat Codex export remains under
`.agents/skills/`.

## Questbook

Questbook is the intentional split-root case:

- `mechanics/questbook/` owns lifecycle grammar, schemas, dispatch posture,
  validation route, and package-local movement.
- `QUESTBOOK.md` stays the compact public frontier index.
- `quests/` stays the durable public item store.
- `generated/quest_*.json` stays a root-published read model over source quests.

Do not turn `quests/` into a roadmap, scratchpad, or package-local notes home.

## Validation

Use the validation lane in [mechanics/AGENTS.md](AGENTS.md#verify). When
artifact homes move, run the owning package check plus the root route checks
that consume the moved path.
