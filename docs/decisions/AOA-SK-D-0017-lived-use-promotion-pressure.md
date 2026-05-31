# Lived-Use Promotion Pressure

- Decision ID: AOA-SK-D-0017

## Index Metadata

- Original date: 2026-05-07
- Surface classes: public status, review/governance
- Skill lanes: none
- Mechanic parents: method-growth
- Guard families: skill maturity, evaluation/public surface
- Posture: accepted promotion pressure route

Date: 2026-05-07

Status: accepted

## Context

Some `aoa-skills` workflows are already installed across the workspace and are
selected repeatedly by Codex skill dispatch. Several are still not canonical.

Before this decision, the public governance layer answered whether a skill met
formal default-reference gates, but it did not make repeated lived use visible
as a first-class promotion-review signal. That left important scaffold or
evaluated skills dependent on manual memory.

## Decision

Add a derived promotion-pressure layer:

- `mechanics/method-growth/docs/PROMOTION_PRESSURE.md`
- `scripts/report_skill_promotion_pressure.py`
- `generated/skill_promotion_pressure.json`
- `generated/skill_promotion_pressure.md`

The report combines public status, governance backlog, skill-quality audit,
workspace adoption, real dispatch trials, local skill-dispatch reports, hook
prompts, and Codex session mentions.

It does not auto-promote skills. It classifies the next review pressure:
canonical monitor, canonical review, status/promotion review, revisit
`stay_evaluated`, blockers-first repair, overlay adoption review, overlay
watch, or watch.

## Consequences

- Repeated installed or dispatched use becomes visible without manual sweeps.
- A heavily used non-canonical skill is routed to the next honest review or
  blocker repair instead of being silently normalized.
- Runtime and local log evidence stay evidence, not source authority.
- Canonical status still requires explicit review records and maturity gates.
- Project overlays remain owner-adoption questions rather than core canonical
  promotions.

## Verification

Verify with:

```bash
python scripts/report_skill_promotion_pressure.py --repo-root . --workspace-root /srv/AbyssOS --format markdown
python -m pytest -q tests/test_skill_promotion_pressure.py
```
