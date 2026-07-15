# Decision Records Index

This directory is the durable decision surface for `aoa-skills`.

Use it when a future contributor needs the rationale for a route, topology,
source/export split, validator, public contract, skill-lane workflow, mechanic
package, generated read model, or owner-boundary choice.

Ordinary edit summaries, generated output, release notes, runtime logs, private
evidence, and one-off planning thoughts route to their owning surfaces instead.

## Operating Card

| Field | Route |
| --- | --- |
| role | durable decision rationale entrypoint and agent-facing index chooser |
| entry | use when a structural, topology, validation, public-contract, source/export, skill-lane, generated-index, or agent-route change needs recoverable rationale |
| input | changed source surface, owner boundary, rejected option, validation guard, or cross-surface route pressure |
| output | canonical decision note, metadata-backed lookup index, and route back to the source surface |
| owner | `docs/decisions/AGENTS.md` for lane law; canonical decision notes for rationale; generated indexes for lookup only |
| next route | source surface first, then local route card, `CHARTER.md`, `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/ARCHITECTURE.md`, generated lookup indexes, or the affected skill/mechanic owner |
| validation | decision-index freshness via `docs/decisions/AGENTS.md`, diff hygiene, and the owning validator for the changed surface |

## Authority

Decision notes explain why a route was chosen.

They are weaker than the source surface they describe:

- repository authority stays in `CHARTER.md`;
- skill-layer system form stays in `DESIGN.md`;
- agent-facing shape stays in `DESIGN.AGENTS.md` and nearest `AGENTS.md` cards;
- technical source/generated/export meaning stays in `docs/ARCHITECTURE.md`;
- semantic capability meaning stays in `capabilities/families/*.yaml`;
- independently callable procedure meaning stays in `skills/**/SKILL.md`;
- current mechanic shape stays in `mechanics/agon`, `mechanics/questbook`,
  `mechanics/release-support`, and their local route cards;
- generated readers stay derived from their builders;
- portable exports and KAG indexes stay projections, not source truth;
- sibling repositories keep their own stronger truth.

Older accepted notes may describe a topology that has since been superseded.
Use their status/current-applicability text and the newest decision for the
same owner surface; never infer current files or runtime requirements from a
historical implementation section alone.

Generated decision indexes are weaker than the decision notes. They exist to
make lookup cheaper for agents, not to carry decision rationale.

## Index Shape

Each decision owns:

- a canonical `Decision ID: AOA-SK-D-####`;
- an `## Index Metadata` block naming original date, surface classes, skill
  lanes, mechanic parents, guard families, and posture.

The lookup indexes under [indexes](indexes/README.md) are generated from that
metadata:

- [Decisions by canonical ID and number](indexes/by-number.md)
- [Decisions by date](indexes/by-date.md)
- [Decisions by surface class](indexes/by-surface.md)
- [Decisions by skill lane](indexes/by-skill-lane.md)
- [Decisions by mechanic parent](indexes/by-mechanic.md)
- [Decisions by validation or guard family](indexes/by-guard.md)

Use them in both directions:

- top down: repo route -> authority class -> operation -> skill lane or
  mechanic parent -> guard family -> decision rationale;
- bottom up: changed source surface -> local route card or generated read model
  -> validator guard -> decision rationale -> stronger owner surface.

Regenerate the read models after decision metadata changes through the focused
decision-index route named by `docs/decisions/AGENTS.md`. Full lane command
authority stays in `config/validation_lanes.json`.

## Addressing

Full canonical-ID decision paths are the active source files:

- `docs/decisions/AOA-SK-D-0001-*.md`
- `docs/decisions/AOA-SK-D-0002-*.md`
- `docs/decisions/AOA-SK-D-####-*.md`

Canonical IDs remain the stable handles. Previous date-prefixed paths are not
live files and are not preserved as a repository lookup layer. Use git history,
PRs, or release notes when old path archaeology is actually needed.

Do not recreate date-named files or generated compatibility maps for retired
paths.

## Naming

Use the full canonical decision ID as the filename prefix:

`AOA-SK-D-0027-short-decision-slug.md`

Prefer short titles that name the route, not the whole debate.

## Template

Start from [TEMPLATE.md](TEMPLATE.md) for new decisions. Keep notes concise, but
include enough context, options, rationale, consequences, index metadata, and
validation for a future agent to avoid repeating the same mistake.
