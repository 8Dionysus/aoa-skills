# AGENTS Card Design

## Purpose

`AGENTS.md` cards are routing law for agents working in the repository. They
name ownership, required local reading, boundaries, verification, and closeout.
They do not duplicate capability contracts, skill procedures, or command
inventories.

## Canonical shape

Every card begins with these non-empty sections in this order:

1. `Applies to`
2. `Role`
3. `Read before editing`
4. `Boundaries`
5. `Validation`
6. `Closeout`

Additional sections are allowed only when they carry durable local law.

## Placement

Add a nested card when a directory has a real owner boundary or a materially
different risk/verification route. Do not add one merely because a directory
exists. The root card supplies repository-wide law; the nearest nested card
narrows it.

## Content rules

- Codex concatenates applicable cards from repository root to the working
  directory. A nested card must not require rereading the root or another
  already inherited ancestor.
- Start required reading from the affected owner source. Route human overview,
  topology, and status README files on demand instead of making them universal
  prerequisites.
- Link to owner surfaces instead of copying them.
- Name the narrowest durable validator, not every command ever run.
- Keep manual outcome evidence distinct from structural checks.
- Keep platform names in adapters or export surfaces unless the core contract
  truly depends on that platform.
- Generated companions may summarize cards but never become authoritative.
- Remove cards when their owner district disappears; Git history is the archive.

## Validation

`scripts/validation/validate_agents_design.py` discovers current cards and
checks their canonical shape while requiring only the active owner-entry cards.
It intentionally does not preserve historical directories through a hardcoded
topology list.
