# QUESTBOOK.md - aoa-skills

This questbook is the compact public index for durable skill-layer obligations
that should survive the current diff.

It is a root index, not a second roadmap. Current direction is routed through
`mechanics/ROADMAP.md` and the nearest mechanic package `ROADMAP.md`.
Questbook mechanism starts in `mechanics/questbook/README.md`, and lifecycle
detail lives in lane-first source files under `quests/`.

Use it for:

- skill bundle gaps that survive a bounded edit
- skill/eval alignment debts
- `.agents/skills/` portable-layer and local-adapter contract follow-through
- overlay or two-stage-routing exceptions that recur often enough to need
  harvest
- recurring cross-repo bridge refresh and review truth-sync routes that need
  explicit automation or playbook classification

Do not use it for one-off prompt tweaks, raw wrapper chatter, transient
generated noise, or replacing skill meaning that already lives in
`skills/*/SKILL.md`.

## Update Trigger

Update this root index when a durable public obligation changes band, appears,
or closes for `aoa-skills`.

Use the nearest owner route instead when the obligation is local to one mechanic
and does not need public quest tracking. Use:

- `mechanics/ROADMAP.md` for route choice across mechanics
- mechanic `ROADMAP.md` files for future contour
- mechanic `LANDING_LOG.md` files for checked landings
- `CHANGELOG.md` for released repository history
- `docs/decisions/` for durable rationale
- `quests/<lane>/<state>/` for source quest objects

If a closeout leaves a durable obligation but this file stays unchanged, say why
the obligation belongs to another owner route.

## Frontier

- `AOA-SK-Q-0003` - tighten the Codex portable layer and local adapter contract
  for `.agents/skills` export.

## Near

- `AOA-SK-Q-0004` - harvest repeated overlay-specific exceptions into stable
  skill bundles or playbooks.
- `AOA-SK-Q-0005` - reflect bounded skill bundles as abilities with
  pack-profile-aware unlock posture.
- `AOA-SK-Q-0006` - classify the cross-repo technique refresh and truth-sync
  route for bounded automation follow-through.
- `AOA-SK-Q-0008` - track checkpoint owner-promotion follow-through as an early
  skill-layer seam.

## Blocked / Reanchor

No public blocked or reanchor item is currently listed here.

## Harvest candidates

- `AOA-SK-Q-0004` - harvest repeated overlay-specific exceptions into stable
  skill bundles or playbooks.
- `AOA-SK-Q-0008` - track checkpoint owner-promotion follow-through as an early
  skill-layer seam.

## Backing Files

- `quests/**/AOA-SK-Q-*.yaml`
- `quests/agon/<state>/AOS-Q-AGON-*.md`
- `mechanics/questbook/schemas/quest.schema.json`
- `mechanics/questbook/schemas/quest_dispatch.schema.json`
- generated summaries: `generated/quest_catalog.min.json`,
  `generated/quest_dispatch.min.json`, `generated/quest_catalog.min.example.json`,
  and `generated/quest_dispatch.min.example.json`

## Rule

A quest can survive in this root index only if it is a durable public
skill-layer obligation. Package-local next work belongs to the package
roadmap; skill meaning belongs in `skills/`; generated quest views are read
models, not authority.
