# AGENTS.md

## Applies to

This card applies to `quests/`.

## Role

`quests/` preserves durable obligations and quest-oriented skill-layer follow-through that should survive a single chat turn.

## Read before editing

Read root `AGENTS.md`, `quests/README.md`, and the mechanic package that originated the obligation before editing.

## Boundaries

Do not turn quests into live runtime state, hidden agent destiny, or proof of completion. A quest records a reviewable obligation; completion still needs evidence in the owning surface.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the route or roadmap parity check named by the owning mechanic. If no local check exists, run `python scripts/validate_skills.py` and `git diff --check`.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
